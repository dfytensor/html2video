#!/usr/bin/env python3
"""
capture_gsap.py — GSAP timeline video capture via Playwright recording

Uses window.__timelines[].seek() + real-time playback with Playwright's
built-in video recording for maximum quality and speed.

Usage:
    python capture_gsap.py input.html [-o output.mp4] [--no-voice] [options]
"""

import argparse
import asyncio
import functools
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = shutil.which("ffmpeg")
    if not FFMPEG:
        sys.exit("pip install imageio-ffmpeg")

DEFAULT_FPS = 24
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1920
DEFAULT_FONT = "C:/Windows/Fonts/msyh.ttc" if sys.platform == "win32" else "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"


def parse_args():
    parser = argparse.ArgumentParser(description="GSAP seek-based HTML to video")
    parser.add_argument("input", help="Input HTML with window.__timelines")
    parser.add_argument("-o", "--output", help="Output MP4 path")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--voice", default="zh-CN-YunxiNeural")
    parser.add_argument("--rate", default="+0%")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS)
    parser.add_argument("--font", default=DEFAULT_FONT)
    parser.add_argument("--no-subtitle", action="store_true")
    parser.add_argument("--no-voice", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--playback-speed", type=float, default=1.0, help="Timeline playback speed (1.0=realtime, 2.0=2x)")
    parser.add_argument("--export-script", action="store_true")
    parser.add_argument("--script-output", default=None)
    parser.add_argument("--timeline-id", default=None, help="Timeline ID (auto-detect if omitted)")
    parser.add_argument("--slide-selector", default=".slide", help="CSS selector for slides")
    return parser.parse_args()


def capture_video_sync(html_path, temp_dir, width, height, fps, args):
    from playwright.sync_api import sync_playwright

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    modified_path = os.path.join(temp_dir, "_modified.html")
    with open(modified_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_url = Path(modified_path).as_uri()
    video_path = os.path.join(temp_dir, "raw_video.webm")

    result_info = {"texts": [], "total_slides": 0, "duration": 0}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": width, "height": height},
            record_video_dir=temp_dir,
            record_video_size={"width": width, "height": height},
        )
        page = ctx.new_page()
        page.goto(file_url, wait_until="load", timeout=60000)
        page.wait_for_timeout(3000)

        total_slides = page.evaluate(f"""
            () => document.querySelectorAll('{args.slide_selector}').length
        """)

        timeline_id = args.timeline_id
        if not timeline_id:
            registered = page.evaluate("() => Object.keys(window.__timelines || {})")
            if registered:
                timeline_id = registered[0]

        duration = 0
        if timeline_id:
            duration = page.evaluate(f"""
                () => window.__timelines['{timeline_id}'].duration()
            """)

        print(f"[INFO] Timeline: {timeline_id}, duration: {duration:.1f}s, slides: {total_slides}")
        result_info["total_slides"] = total_slides
        result_info["duration"] = duration

        slide_texts = []
        for i in range(total_slides):
            text = page.evaluate(f"""
                () => document.querySelectorAll('{args.slide_selector}')[{i}].innerText.trim()
            """)
            slide_texts.append(text)
        result_info["texts"] = slide_texts

        if timeline_id:
            speed = args.playback_speed
            page.evaluate(f"""
                () => {{
                    var tl = window.__timelines['{timeline_id}'];
                    tl.timeScale({speed});
                    tl.play(0);
                }}
            """)
            wait_ms = int(duration * 1000 / speed) + 2000
            print(f"[INFO] Playing timeline at {speed}x speed, waiting {wait_ms}ms...")
            page.wait_for_timeout(wait_ms)
        else:
            sd = 5.0
            for i in range(total_slides):
                page.evaluate(f"""
                    () => {{
                        var slides = document.querySelectorAll('{args.slide_selector}');
                        slides.forEach(s => {{ s.style.opacity = '0'; s.style.pointerEvents = 'none'; }});
                        slides[{i}].style.opacity = '1';
                        slides[{i}].style.pointerEvents = 'auto';
                    }}
                """)
                page.wait_for_timeout(int(sd * 1000))

        page.close()
        ctx.close()
        browser.close()

        raw_video = os.path.join(temp_dir, "_modified.webm")
        if not os.path.exists(raw_video):
            for f in os.listdir(temp_dir):
                if f.endswith(".webm"):
                    raw_video = os.path.join(temp_dir, f)
                    break

        if os.path.exists(raw_video):
            result_info["video_path"] = raw_video
        else:
            print(f"[ERROR] No video file found in {temp_dir}")
            result_info["video_path"] = None

    return result_info


def get_audio_duration(audio_path):
    if not audio_path or not os.path.exists(audio_path):
        return 0
    try:
        cmd = [FFMPEG, "-i", audio_path, "-hide_banner"]
        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+)\.(\d+)", result.stderr)
        if m:
            h, mi, s, ms = m.groups()
            return int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 100
    except Exception:
        pass
    return 5


async def generate_tts(text, output_path, voice, rate):
    if not edge_tts:
        return None
    if not text.strip():
        return None
    text = text.strip()
    if len(text) > 200:
        text = text[:200]
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))
    return str(output_path)


def concat_audio_files(audio_paths, output_path):
    valid = [p for p in audio_paths if p and os.path.exists(p)]
    if not valid:
        return None
    if len(valid) == 1:
        shutil.copy2(valid[0], output_path)
        return output_path

    filter_parts = []
    inputs = []
    for i, p in enumerate(valid):
        inputs.extend(["-i", p])
        filter_parts.append(f"[{i}:a]")
    filter_str = "".join(filter_parts) + f"concat=n={len(valid)}:v=0:a=1[outa]"
    cmd = [FFMPEG, "-y", *inputs, "-filter_complex", filter_str,
           "-map", "[outa]", "-c:a", "aac", output_path]
    subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    return output_path if os.path.exists(output_path) else None


def add_audio_to_video(video_path, audio_path, output_path, fps):
    if audio_path and os.path.exists(audio_path):
        cmd = [FFMPEG, "-y", "-i", video_path, "-i", audio_path,
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
               "-c:a", "aac", "-shortest", output_path]
    else:
        cmd = [FFMPEG, "-y", "-i", video_path,
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
               "-an", output_path]
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print(f"[FFMPEG STDERR] {result.stderr[:500]}")
        return False
    return True


async def convert(args):
    html_path = os.path.abspath(args.input)
    if not os.path.exists(html_path):
        sys.exit(f"Not found: {html_path}")

    output_path = os.path.abspath(args.output) if args.output else os.path.splitext(html_path)[0] + "_video.mp4"
    temp_dir = tempfile.mkdtemp(prefix="gsap_capture_")

    print(f"[INFO] Input:    {html_path}")
    print(f"[INFO] Output:   {output_path}")
    print(f"[INFO] Temp:     {temp_dir}")
    print(f"[INFO] Size:     {args.width}x{args.height}")
    print(f"[INFO] FPS:      {args.fps}")
    print(f"[INFO] Mode:     GSAP timeline playback + Playwright recording")
    print(f"[INFO] Voice:    {'(disabled)' if args.no_voice else args.voice}")

    try:
        print("\n[STEP 1] Capturing video via GSAP playback...")
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(
            None, functools.partial(
                capture_video_sync,
                html_path, temp_dir, args.width, args.height, args.fps, args
            )
        )

        if not info.get("video_path"):
            print("[ERROR] Video capture failed")
            return

        print(f"[OK] Captured {info['duration']:.1f}s, {info['total_slides']} slides")
        print(f"     Raw video: {info['video_path']}")

        if args.export_script:
            script_path = os.path.abspath(args.script_output) if args.script_output else os.path.splitext(html_path)[0] + "_script.txt"
            with open(script_path, "w", encoding="utf-8") as f:
                for i, t in enumerate(info["texts"]):
                    f.write(f"[Page {i+1}]\n{t}\n\n")
            print(f"\n[DONE] Script: {script_path}")
            if not args.keep_temp:
                shutil.rmtree(temp_dir, ignore_errors=True)
            return

        audio_path = None
        if not args.no_voice and edge_tts:
            print("\n[STEP 2] TTS audio...")
            tts_paths = []
            for i, text in enumerate(info["texts"]):
                ap = os.path.join(temp_dir, f"tts_{i:03d}.mp3")
                result = await generate_tts(text, ap, args.voice, args.rate)
                tts_paths.append(result)
                status = f"{text[:40]}..." if result else "(empty)"
                print(f"  [{i+1}/{info['total_slides']}] {status}")

            combined_audio = os.path.join(temp_dir, "combined_audio.mp3")
            audio_path = concat_audio_files(tts_paths, combined_audio)
            if audio_path:
                dur = get_audio_duration(audio_path)
                print(f"[OK] Combined audio: {dur:.1f}s")
            else:
                print("[WARN] No audio generated")
        else:
            print("\n[STEP 2] Skipping voice (disabled or edge-tts not installed)")

        print("\n[STEP 3] Encoding final video...")
        success = add_audio_to_video(info["video_path"], audio_path, output_path, args.fps)

        if success and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"\n[DONE] {output_path} ({size_mb:.1f} MB)")
        else:
            print("\n[ERROR] Output not created")

    finally:
        if not args.keep_temp:
            shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    args = parse_args()
    asyncio.run(convert(args))


if __name__ == "__main__":
    main()
