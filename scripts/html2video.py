#!/usr/bin/env python3
"""
html2video.py — HTML to Video Converter (Divide & Conquer Pipeline)

Converts HTML slide presentations to MP4 video with TTS narration.

Pipeline:
    Phase 1 — Screenshots: HTML → Playwright screenshots + text extraction
    Phase 2 — TTS (D&C):  Per-slide TTS with timeout, cache, and resume
    Phase 3 — Compose:     Screenshots + audio + subtitles → per-slide MP4
    Phase 4 — Concat:      All segments → final MP4

Usage:
    python html2video.py input.html
    python html2video.py input.html -o output.mp4 --width 1920 --height 1080
    python html2video.py input.html --voice zh-CN-XiaoxiaoNeural --fps 30
"""

import argparse
import asyncio
import functools
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil
import hashlib
import time
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Error: pillow not installed. Run: pip install pillow")

try:
    import edge_tts
except ImportError:
    sys.exit("Error: edge-tts not installed. Run: pip install edge-tts")

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = shutil.which("ffmpeg")
    if not FFMPEG:
        sys.exit("Error: ffmpeg not found. Run: pip install imageio-ffmpeg")


DEFAULT_VOICE = "zh-CN-YunxiNeural"
DEFAULT_FPS = 24
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1920
DEFAULT_FRAME_TIMES = [0.5, 1.5, 2.5, 3.5, 4.5]
HOOK_FRAME_TIMES = [0.1, 0.3, 0.5, 1.0, 2.0, 3.5]
DEFAULT_FONT = "C:/Windows/Fonts/msyh.ttc" if sys.platform == "win32" else "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

TTS_PER_FILE_TIMEOUT = 60
TTS_MAX_RETRIES = 2
TTS_CACHE_DIR_NAME = ".tts_cache"


def parse_args():
    parser = argparse.ArgumentParser(description="Convert HTML slides to MP4 video (or semi-auto: script + images → video)")
    parser.add_argument("input", nargs="?", default=None, help="Input HTML file path (optional for --script-only / --images-dir mode)")
    parser.add_argument("-o", "--output", help="Output MP4 file path")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Video width (default: 1080)")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Video height (default: 1920)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"TTS voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--rate", default="+0%", help="TTS rate adjustment (e.g. +20%%)")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help=f"Video FPS (default: {DEFAULT_FPS})")
    parser.add_argument("--frames", default=None, help="Comma-separated frame capture times in seconds (default: 0.5,1.5,2.5,3.5,4.5)")
    parser.add_argument("--font", default=DEFAULT_FONT, help="Subtitle font path")
    parser.add_argument("--no-subtitle", action="store_true", help="Disable subtitle overlay")
    parser.add_argument("--no-voice", action="store_true", help="Skip TTS narration — output video without audio")
    parser.add_argument("--export-script", action="store_true", help="Export narration script (TXT) and exit — no video generated")
    parser.add_argument("--script-output", default=None, help="Output path for narration script (default: same dir as input, _script.txt)")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary files")
    parser.add_argument("--slide-selector", default=".slide", help="CSS selector for slides (default: .slide)")
    parser.add_argument("--title", default=None, help="Override hook video title (default: auto from Slide 1 text)")
    parser.add_argument("--cover-frame", type=int, default=None, help="Slide 1 frame index to use as cover thumbnail (default: auto-select best frame)")
    parser.add_argument("--tts-timeout", type=int, default=TTS_PER_FILE_TIMEOUT, help=f"Per-file TTS timeout in seconds (default: {TTS_PER_FILE_TIMEOUT})")
    parser.add_argument("--tts-retries", type=int, default=TTS_MAX_RETRIES, help=f"Max retries per TTS file (default: {TTS_MAX_RETRIES})")
    parser.add_argument("--tts-cache", action="store_true", help="Enable TTS disk cache (reuse across runs)")

    mode3 = parser.add_argument_group("Mode 3: Semi-Automatic (script design + user images → video)")
    mode3.add_argument("--script-only", default=None, metavar="SCRIPT_JSON",
                       help="Generate TTS audio from _script_design.json only (no HTML needed)")
    mode3.add_argument("--tts-output", default=None,
                       help="Output directory for TTS files in --script-only mode")
    mode3.add_argument("--script", default=None, metavar="SCRIPT_JSON",
                       help="Path to _script_design.json for Mode 3 video composition")
    mode3.add_argument("--images-dir", default=None,
                       help="Directory with user-generated images (auto-discovered by scene_NNN_* pattern)")
    mode3.add_argument("--images-map", default=None,
                       help="JSON file mapping scene index to explicit image path")
    mode3.add_argument("--tts-dir", default=None,
                       help="Directory with pre-generated TTS audio files")
    return parser.parse_args()


def read_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


def inject_slide_nav_js(html_content, selector=".slide"):
    has_goToSlide = "function goToSlide" in html_content

    extra_js = ""
    if not has_goToSlide:
        extra_js = f"""
function goToSlide(n) {{
    var slides = getSlideElements();
    for (var i = 0; i < slides.length; i++) {{
        slides[i].classList.remove('active');
        if (i === n) {{
            slides[i].classList.add('active');
        }}
    }}
    window.__currentSlide = n;
    var active = slides[n];
    if (active) {{
        active.querySelectorAll('.an, .anim, .anim-item').forEach(function(item) {{
            item.classList.remove('show', 'visible');
            void item.offsetWidth;
            item.classList.add('show', 'visible');
        }});
        active.querySelectorAll('[style*="animation"]').forEach(function(item) {{
            var clone = item.cloneNode(true);
            item.parentNode.replaceChild(clone, item);
        }});
    }}
}}
"""

    nav_js = f"""
<script>
function getSlideElements() {{
    var container = document.querySelector('.ppt-container') || document.querySelector('.slide-container');
    if (container) {{
        return container.querySelectorAll(':scope > .slide');
    }}
    return document.querySelectorAll('{selector}');
}}
window.__totalSlides = getSlideElements().length;
window.__currentSlide = 0;
function getSlideText(n) {{
    var slides = getSlideElements();
    if (n < slides.length) {{
        return slides[n].innerText.trim();
    }}
    return document.body.innerText.trim();
}}
{extra_js}
if (typeof goToSlide === 'function' && !window.__customGoToSlide) {{
    goToSlide(0);
}} else if (window.__customGoToSlide) {{
    goToSlide(0);
}}
</script>
"""
    if "</body>" in html_content:
        html_content = html_content.replace("</body>", nav_js + "\n</body>")
    else:
        html_content += nav_js
    return html_content


# ============================================================
# Phase 1: Screenshots
# ============================================================

def screenshot_slides_sync(html_path, output_dir, width, height, frame_times, selector=".slide"):
    from playwright.sync_api import sync_playwright

    html_content = read_html(html_path)
    html_content = inject_slide_nav_js(html_content, selector)
    modified_path = os.path.join(output_dir, "_modified.html")
    with open(modified_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    screenshots = {}
    slide_texts = []
    file_url = Path(modified_path).as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(file_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)

        total_slides = page.evaluate("window.__totalSlides || 0")

        if total_slides > 0:
            for slide_idx in range(total_slides):
                page.evaluate(f"goToSlide({slide_idx})")
                page.wait_for_timeout(300)
                text = page.evaluate(f"getSlideText({slide_idx})")
                slide_texts.append(text)
                current_frames = HOOK_FRAME_TIMES if slide_idx == 0 else frame_times
                slide_screenshots = []
                for ft_idx, ft in enumerate(current_frames):
                    out_path = os.path.join(output_dir, f"slide_{slide_idx:03d}_frame_{ft_idx:02d}.png")
                    page.wait_for_timeout(int(ft * 1000))
                    page.screenshot(path=out_path)
                    slide_screenshots.append(out_path)
                screenshots[slide_idx] = slide_screenshots
        else:
            text = page.evaluate("document.body.innerText.trim()")
            slide_texts.append(text)
            slide_screenshots = []
            for ft_idx, ft in enumerate(HOOK_FRAME_TIMES):
                out_path = os.path.join(output_dir, f"slide_000_frame_{ft_idx:02d}.png")
                page.wait_for_timeout(int(ft * 1000))
                page.screenshot(path=out_path)
                slide_screenshots.append(out_path)
            screenshots[0] = slide_screenshots

        browser.close()

    return screenshots, slide_texts


# ============================================================
# Phase 2: TTS (Divide & Conquer)
# ============================================================

def tts_cache_key(text, voice, rate):
    payload = f"{text}|{voice}|{rate}"
    return hashlib.md5(payload.encode("utf-8")).hexdigest()[:12]


def tts_cache_dir(base_dir):
    d = os.path.join(base_dir, TTS_CACHE_DIR_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def tts_cache_path(cache_dir, key):
    return os.path.join(cache_dir, f"{key}.mp3")


def tts_cached(cache_dir, key, min_size=500):
    path = tts_cache_path(cache_dir, key)
    if os.path.exists(path) and os.path.getsize(path) >= min_size:
        return path
    return None


async def generate_tts_single(text, output_path, voice, rate, timeout_sec):
    if not text.strip():
        return None
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await asyncio.wait_for(communicate.save(str(output_path)), timeout=timeout_sec)
    return str(output_path)


async def generate_tts_batch(slide_texts, output_dir, voice, rate, timeout_sec, max_retries, use_cache):
    audio_paths = {}
    total = len(slide_texts)
    cache_d = tts_cache_dir(output_dir) if use_cache else None

    for slide_idx in range(total):
        text = slide_texts[slide_idx].strip() if slide_idx < len(slide_texts) else ""
        if not text:
            audio_paths[slide_idx] = None
            print(f"  [TTS] Page {slide_idx + 1}/{total}: (empty, skipped)")
            continue

        truncated = text[:200]
        key = tts_cache_key(truncated, voice, rate)

        if cache_d:
            cached = tts_cached(cache_d, key)
            if cached:
                final_path = os.path.join(output_dir, f"tts_{slide_idx:03d}.mp3")
                shutil.copy2(cached, final_path)
                audio_paths[slide_idx] = final_path
                print(f"  [TTS] Page {slide_idx + 1}/{total}: (cache hit)")
                continue

        final_path = os.path.join(output_dir, f"tts_{slide_idx:03d}.mp3")
        success = False

        for attempt in range(1, max_retries + 1):
            try:
                t0 = time.time()
                result = await generate_tts_single(truncated, final_path, voice, rate, timeout_sec)
                elapsed = time.time() - t0
                if result and os.path.exists(result) and os.path.getsize(result) > 100:
                    success = True
                    if cache_d:
                        shutil.copy2(final_path, tts_cache_path(cache_d, key))
                    safe = truncated[:50].encode("ascii", errors="replace").decode("ascii")
                    dur = get_audio_duration(final_path)
                    print(f"  [TTS] Page {slide_idx + 1}/{total}: {elapsed:.1f}s ({dur:.1f}s audio) - {safe}...")
                    break
                else:
                    print(f"  [TTS] Page {slide_idx + 1}/{total}: attempt {attempt} produced empty file")
            except asyncio.TimeoutError:
                print(f"  [TTS] Page {slide_idx + 1}/{total}: attempt {attempt}/{max_retries} TIMEOUT ({timeout_sec}s)")
            except Exception as e:
                print(f"  [TTS] Page {slide_idx + 1}/{total}: attempt {attempt}/{max_retries} ERROR: {e}")

        if success:
            audio_paths[slide_idx] = final_path
        else:
            audio_paths[slide_idx] = None
            print(f"  [TTS] Page {slide_idx + 1}/{total}: FAILED after {max_retries} retries, using silent")

    return audio_paths


# ============================================================
# Shared utilities
# ============================================================

def get_audio_duration(audio_path):
    if audio_path is None or not os.path.exists(audio_path):
        return 0
    try:
        cmd = [FFMPEG, "-i", audio_path, "-hide_banner"]
        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
        duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+)\.(\d+)", result.stderr)
        if duration_match:
            h, m, s, ms = duration_match.groups()
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 100
    except Exception:
        pass
    return 3


def create_subtitle_image(text, width, height, font_path, output_path):
    if not text.strip():
        return None
    img = Image.new("RGBA", (width, 120), (0, 0, 0, 180))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(font_path, 36)
    except Exception:
        font = ImageFont.load_default()

    max_chars = max(1, (width - 40) // 36)
    lines = []
    current_line = ""
    for char in text:
        current_line += char
        bbox = font.getbbox(current_line)
        if bbox[2] - bbox[0] > width - 60:
            lines.append(current_line[:-1])
            current_line = char
    if current_line:
        lines.append(current_line)

    y_offset = max(5, (120 - len(lines) * 44) // 2)
    for line in lines:
        bbox = font.getbbox(line)
        tw = bbox[2] - bbox[0]
        x = (width - tw) // 2
        draw.text((x, y_offset), line, fill=(255, 255, 255, 255), font=font)
        y_offset += 44

    img.save(output_path)
    return output_path


def generate_hook_title(slide_text, override=None):
    if override:
        title = override.strip()
    else:
        text = slide_text.strip().replace("\n", " ")
        if len(text) > 30:
            text = text[:30]
        title = text
    if not title:
        title = "Untitled"
    return title


def extract_cover_thumbnail(screenshots, cover_frame=None, output_path=None, slide_idx=0):
    slides = screenshots.get(slide_idx, [])
    if not slides:
        return None
    if cover_frame is not None:
        idx = min(cover_frame, len(slides) - 1)
    else:
        idx = min(1, len(slides) - 1)
    src = slides[idx]
    if output_path and os.path.exists(src):
        shutil.copy2(src, output_path)
        return output_path
    return src


# ============================================================
# Phase 3: Per-slide video composition
# ============================================================

def build_slide_video(screenshots, audio_path, subtitle_path, output_path, fps, width, height, no_voice=False):
    has_audio = (not no_voice) and audio_path and os.path.exists(audio_path)
    if has_audio:
        duration = get_audio_duration(audio_path)
    else:
        duration = 5
    if duration <= 0:
        duration = 3

    num_frames = len(screenshots)
    frame_duration = duration / num_frames

    segment_files = []
    for i, ss_path in enumerate(screenshots):
        segment_path = output_path.replace(".mp4", f"_seg_{i}.mp4")

        inputs = ["-loop", "1", "-i", ss_path]
        filter_complex = None
        audio_map = []

        if subtitle_path and os.path.exists(subtitle_path):
            inputs += ["-loop", "1", "-i", subtitle_path]
            filter_complex = (
                f"[0:v]fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[bg];"
                f"[1:v]scale={width}:120[sub];"
                f"[bg][sub]overlay=0:{height - 120}[vout]"
            )
            map_arg = ["-map", "[vout]"]
        else:
            filter_complex = (
                f"[0:v]fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[vout]"
            )
            map_arg = ["-map", "[vout]"]

        cmd = [
            FFMPEG, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            *map_arg,
            "-t", str(round(frame_duration, 2)),
            "-pix_fmt", "yuv420p",
            "-c:v", "libx264",
            segment_path
        ]

        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
        if os.path.exists(segment_path) and os.path.getsize(segment_path) > 0:
            segment_files.append(segment_path)
        else:
            print(f"    [DBG] seg {i} failed: {result.stderr[:200] if result.stderr else 'unknown'}")

    if not segment_files:
        return False

    inputs = []
    for sf in segment_files:
        inputs.extend(["-i", sf])

    n_video = len(segment_files)
    has_audio = (not no_voice) and audio_path and os.path.exists(audio_path)

    concat_inputs = "".join(f"[{i}:v]" for i in range(n_video))
    filter_str = f"{concat_inputs}concat=n={n_video}:v=1:a=0[outv]"

    audio_args = []
    if has_audio:
        inputs.extend(["-i", audio_path])
        filter_str += f";[{n_video}:a]asetpts=PTS-STARTPTS[outa]"
        audio_args = ["-map", "[outa]"]

    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[outv]",
        *audio_args,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
    ]
    if has_audio:
        cmd.extend(["-c:a", "aac", "-shortest"])
    else:
        cmd.append("-an")
    cmd.append(output_path)

    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode != 0 and not os.path.exists(output_path):
        print(f"    [DBG] concat failed: {result.stderr[:300] if result.stderr else 'unknown'}")

    for sf in segment_files:
        if os.path.exists(sf):
            os.remove(sf)

    return os.path.exists(output_path) and os.path.getsize(output_path) > 0


# ============================================================
# Phase 4: Final concatenation
# ============================================================

def concat_segments(segment_videos, output_path, has_audio):
    if len(segment_videos) == 1:
        shutil.move(segment_videos[0], output_path)
        return True

    concat_file = os.path.join(os.path.dirname(segment_videos[0]), "concat_list.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for sv in segment_videos:
            f.write(f"file '{Path(sv).as_posix()}'\n")

    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
    ]
    if has_audio:
        cmd.extend(["-c:a", "aac"])
    else:
        cmd.append("-an")
    cmd.append(output_path)

    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print(f"[WARN] ffmpeg concat error: {result.stderr[:500]}")
        return False
    return True


# ============================================================
# Mode 3: Semi-Automatic Pipeline
# ============================================================

SCENE_IMAGE_PATTERN = re.compile(r"^scene_(\d{3})_.+\.png$", re.IGNORECASE)


def load_script_design(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def discover_images(images_dir):
    discovered = {}
    if not os.path.isdir(images_dir):
        sys.exit(f"Error: Images directory not found: {images_dir}")
    for fname in sorted(os.listdir(images_dir)):
        m = SCENE_IMAGE_PATTERN.match(fname)
        if m:
            idx = int(m.group(1))
            fpath = os.path.join(images_dir, fname)
            discovered[idx] = fpath
    return discovered


def load_images_map(map_path):
    with open(map_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    mapping = {}
    for k, v in raw.items():
        idx = int(k)
        if not os.path.exists(v):
            print(f"[WARN] Image not found for scene {idx}: {v}")
            continue
        mapping[idx] = os.path.abspath(v)
    return mapping


def verify_images(images_map, total_scenes):
    missing = []
    for i in range(total_scenes):
        if i not in images_map:
            missing.append(i)
    if missing:
        print(f"[WARN] Missing images for scenes: {missing}")
    found = len(images_map)
    print(f"[INFO] Images found: {found}/{total_scenes}")
    return len(missing) == 0


async def generate_tts_from_script(script_data, output_dir, voice, rate, timeout_sec, max_retries, use_cache):
    scenes = script_data.get("scenes", [])
    texts = [s.get("voiceover", "").strip() for s in scenes]
    voice_override = script_data.get("voice", voice)
    rate_override = script_data.get("rate", rate)
    os.makedirs(output_dir, exist_ok=True)
    print(f"[MODE3-SCRIPT-ONLY] Generating TTS for {len(texts)} scenes...")
    audio_paths = await generate_tts_batch(
        texts, output_dir, voice_override, rate_override,
        timeout_sec, max_retries, use_cache
    )
    return audio_paths


async def images_to_video(args):
    script_path = os.path.abspath(args.script)
    if not os.path.exists(script_path):
        sys.exit(f"Error: Script design JSON not found: {script_path}")

    script_data = load_script_design(script_path)
    scenes = script_data.get("scenes", [])
    total_scenes = len(scenes)

    if total_scenes == 0:
        sys.exit("Error: Script design has no scenes")

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        base, _ = os.path.splitext(script_path)
        output_path = base + "_video.mp4"

    temp_dir = tempfile.mkdtemp(prefix="html2video_m3_")

    width = args.width
    height = args.height
    voice = args.voice
    rate = args.rate

    if "resolution" in script_data:
        width = script_data["resolution"].get("width", width)
        height = script_data["resolution"].get("height", height)
    if "voice" in script_data:
        voice = script_data["voice"]
    if "rate" in script_data:
        rate = script_data["rate"]

    print(f"[MODE3] Script:   {script_path}")
    print(f"[MODE3] Output:   {output_path}")
    print(f"[MODE3] Scenes:   {total_scenes}")
    print(f"[MODE3] Size:     {width}x{height}")
    print(f"[MODE3] Voice:    {voice}")

    try:
        images_map = {}
        if args.images_map:
            images_map = load_images_map(args.images_map)
            print(f"[MODE3] Images from map: {len(images_map)} files")
        elif args.images_dir:
            images_dir = os.path.abspath(args.images_dir)
            images_map = discover_images(images_dir)
            print(f"[MODE3] Images discovered: {len(images_map)} files in {images_dir}")
        else:
            sys.exit("Error: Mode 3 requires --images-dir or --images-map")

        all_ok = verify_images(images_map, total_scenes)
        if not all_ok:
            print("[MODE3] WARNING: Some scenes have no images. Those scenes will be skipped.")

        voiceover_texts = [s.get("voiceover", "").strip() for s in scenes]

        audio_paths = {}
        if args.no_voice:
            print("[MODE3] TTS skipped (--no-voice)")
        elif args.tts_dir:
            tts_dir = os.path.abspath(args.tts_dir)
            for i in range(total_scenes):
                candidate = os.path.join(tts_dir, f"tts_{i:03d}.mp3")
                if os.path.exists(candidate):
                    audio_paths[i] = candidate
            print(f"[MODE3] TTS from dir: {len(audio_paths)} files found in {tts_dir}")
        else:
            print(f"[MODE3] Generating TTS for {total_scenes} scenes...")
            audio_paths = await generate_tts_batch(
                voiceover_texts, temp_dir, voice, rate,
                args.tts_timeout, args.tts_retries, args.tts_cache
            )
            n_ok = sum(1 for v in audio_paths.values() if v)
            print(f"[MODE3] TTS complete: {n_ok}/{total_scenes} scenes have audio")

        hook_title = script_data.get("title", "")
        if not hook_title and scenes:
            hook_title = scenes[0].get("title", "Untitled")
        title_path = os.path.splitext(output_path)[0] + "_title.txt"
        with open(title_path, "w", encoding="utf-8") as f:
            f.write(hook_title)
        print(f"[HOOK] Video title: {hook_title}")

        if 0 in images_map and os.path.exists(images_map[0]):
            cover_output = os.path.splitext(output_path)[0] + "_cover.png"
            img = Image.open(images_map[0])
            img = img.resize((width, height), Image.LANCZOS)
            img.save(cover_output)
            print(f"[HOOK] Cover thumbnail: {cover_output}")

        print("\n[MODE3] Composing per-scene video segments...")
        subtitle_paths = {}
        if not args.no_subtitle:
            for i in range(total_scenes):
                text = voiceover_texts[i] if i < len(voiceover_texts) else ""
                text = text.strip()
                if not text:
                    continue
                sub_path = os.path.join(temp_dir, f"sub_{i:03d}.png")
                result = create_subtitle_image(text, width, height, args.font, sub_path)
                if result:
                    subtitle_paths[i] = result

        segment_videos = []
        for i in range(total_scenes):
            img_path = images_map.get(i)
            if not img_path or not os.path.exists(img_path):
                print(f"  [SKIP] Scene {i}: no image")
                continue

            resized_path = os.path.join(temp_dir, f"img_{i:03d}.png")
            img = Image.open(img_path)
            img = img.resize((width, height), Image.LANCZOS)

            screenshots = {i: [resized_path]}
            audio = audio_paths.get(i)
            subtitle = subtitle_paths.get(i)
            seg_path = os.path.join(temp_dir, f"scene_{i:03d}.mp4")

            success = build_slide_video(
                [resized_path], audio, subtitle, seg_path,
                args.fps, width, height, no_voice=args.no_voice
            )
            if success:
                dur = get_audio_duration(seg_path)
                segment_videos.append(seg_path)
                scene_title = scenes[i].get("title", f"Scene {i}")
                print(f"  [OK] Scene {i}/{total_scenes} \"{scene_title}\" ({dur:.1f}s)")
            else:
                print(f"  [FAIL] Scene {i}/{total_scenes}")

        if not segment_videos:
            print("\n[ERROR] No video segments generated")
            return

        print(f"\n[MODE3] Concatenating {len(segment_videos)} segments...")
        has_any_audio = not args.no_voice and any(audio_paths.get(i) for i in range(total_scenes))
        concat_segments(segment_videos, output_path, has_any_audio)

        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            duration = get_audio_duration(output_path)
            print(f"\n[DONE] Video saved: {output_path}")
            print(f"       Size: {size_mb:.1f} MB | Duration: {duration:.1f}s")
        else:
            print(f"\n[ERROR] Output file not created")

    finally:
        if not args.keep_temp:
            print(f"[CLEANUP] Removing temp dir: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print(f"[KEEP] Temp files: {temp_dir}")


# ============================================================
# Main pipeline
# ============================================================

async def convert_html_to_video(args):
    html_path = os.path.abspath(args.input)
    if not os.path.exists(html_path):
        sys.exit(f"Error: Input file not found: {html_path}")

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        base, _ = os.path.splitext(html_path)
        output_path = base + "_video.mp4"

    frame_times = DEFAULT_FRAME_TIMES
    if args.frames:
        frame_times = [float(t) for t in args.frames.split(",")]

    temp_dir = tempfile.mkdtemp(prefix="html2video_")
    print(f"[INFO] Input:    {html_path}")
    print(f"[INFO] Output:   {output_path}")
    print(f"[INFO] Temp:     {temp_dir}")
    print(f"[INFO] Size:     {args.width}x{args.height}")
    print(f"[INFO] Voice:    {'(disabled)' if args.no_voice else args.voice}")
    print(f"[INFO] FPS:      {args.fps}")
    print(f"[INFO] Frames:   {frame_times}")
    print(f"[INFO] TTS D&C:  timeout={args.tts_timeout}s, retries={args.tts_retries}, cache={'on' if args.tts_cache else 'off'}")

    try:
        # ── Phase 1: Screenshots ──
        print("\n[PHASE 1] Screenshots + text extraction...")
        t_start = time.time()
        loop = asyncio.get_event_loop()
        screenshots, slide_texts = await loop.run_in_executor(
            None,
            functools.partial(
                screenshot_slides_sync,
                html_path, temp_dir, args.width, args.height, frame_times, args.slide_selector
            )
        )
        total_pages = len(screenshots)
        print(f"[OK] {total_pages} pages, {sum(len(v) for v in screenshots.values())} frames ({time.time()-t_start:.1f}s)")
        for i, t in enumerate(slide_texts):
            preview = (t[:80].replace("\n", " ") if t else "(empty)")
            preview = preview.encode("ascii", errors="replace").decode("ascii")
            print(f"  Page {i+1}: {preview}")

        hook_title = generate_hook_title(slide_texts[0] if slide_texts else "", args.title)
        title_path = os.path.splitext(output_path)[0] + "_title.txt"
        with open(title_path, "w", encoding="utf-8") as f:
            f.write(hook_title)
        print(f"\n[HOOK] Video title: {hook_title}")
        print(f"       Saved: {title_path}")

        cover_output = os.path.splitext(output_path)[0] + "_cover.png"
        cover_result = extract_cover_thumbnail(
            screenshots, args.cover_frame, cover_output, slide_idx=0
        )
        if cover_result:
            print(f"[HOOK] Cover thumbnail: {cover_result}")

        if args.export_script:
            if args.script_output:
                script_path = os.path.abspath(args.script_output)
            else:
                base, _ = os.path.splitext(html_path)
                script_path = base + "_script.txt"
            with open(script_path, "w", encoding="utf-8") as f:
                for i, t in enumerate(slide_texts):
                    label = f"[Page {i+1}]"
                    f.write(f"{label}\n{t}\n\n")
            print(f"\n[DONE] Narration script saved: {script_path}")
            print(f"       {total_pages} pages exported")
            if not args.keep_temp:
                shutil.rmtree(temp_dir, ignore_errors=True)
            return

        # ── Phase 2: TTS (Divide & Conquer) ──
        print(f"\n[PHASE 2] TTS generation (divide & conquer)...")
        audio_paths = {}

        if args.no_voice:
            print("  (Skipped --no-voice mode)")
        else:
            t_tts_start = time.time()
            audio_paths = await generate_tts_batch(
                slide_texts, temp_dir, args.voice, args.rate,
                args.tts_timeout, args.tts_retries, args.tts_cache
            )
            n_ok = sum(1 for v in audio_paths.values() if v)
            n_fail = sum(1 for v in audio_paths.values() if v is None)
            print(f"  TTS complete: {n_ok} ok, {n_fail} silent ({time.time()-t_tts_start:.1f}s)")

        # ── Phase 3: Per-slide composition ──
        print("\n[PHASE 3] Composing per-slide video segments...")
        t_comp_start = time.time()
        subtitle_paths = {}
        if not args.no_subtitle:
            for slide_idx in range(total_pages):
                text = slide_texts[slide_idx] if slide_idx < len(slide_texts) else ""
                text = text.strip()
                sub_path = os.path.join(temp_dir, f"sub_{slide_idx:03d}.png")
                result = create_subtitle_image(text, args.width, args.height, args.font, sub_path)
                if result:
                    subtitle_paths[slide_idx] = result

        segment_videos = []
        for slide_idx in range(total_pages):
            ss_list = screenshots.get(slide_idx, [])
            audio = audio_paths.get(slide_idx)
            subtitle = subtitle_paths.get(slide_idx)
            seg_path = os.path.join(temp_dir, f"page_{slide_idx:03d}.mp4")

            if not ss_list:
                continue

            success = build_slide_video(
                ss_list, audio, subtitle, seg_path, args.fps, args.width, args.height,
                no_voice=args.no_voice
            )
            if success:
                dur = get_audio_duration(seg_path)
                segment_videos.append(seg_path)
                print(f"  [OK] Page {slide_idx + 1}/{total_pages} ({dur:.1f}s)")
            else:
                print(f"  [FAIL] Page {slide_idx + 1}/{total_pages}")

        print(f"  Composition complete ({time.time()-t_comp_start:.1f}s)")

        # ── Phase 4: Final concatenation ──
        if len(segment_videos) == 0:
            print("\n[ERROR] No video segments generated")
            return

        print(f"\n[PHASE 4] Concatenating {len(segment_videos)} segments...")
        has_any_audio = not args.no_voice and any(audio_paths.get(i) for i in range(total_pages))
        concat_segments(segment_videos, output_path, has_any_audio)

        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            duration = get_audio_duration(output_path)
            total_time = time.time() - t_start if 't_start' in dir() else 0
            print(f"\n[DONE] Video saved: {output_path}")
            print(f"       Size: {size_mb:.1f} MB | Duration: {duration:.1f}s")
        else:
            print(f"\n[ERROR] Output file not created")

    finally:
        if not args.keep_temp:
            print(f"[CLEANUP] Removing temp dir: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print(f"[KEEP] Temp files: {temp_dir}")


def main():
    args = parse_args()

    if args.script_only:
        script_path = os.path.abspath(args.script_only)
        if not os.path.exists(script_path):
            sys.exit(f"Error: Script JSON not found: {script_path}")
        script_data = load_script_design(script_path)
        tts_dir = args.tts_output or os.path.join(os.path.dirname(script_path), "tts_output")
        asyncio.run(generate_tts_from_script(
            script_data, tts_dir, args.voice, args.rate,
            args.tts_timeout, args.tts_retries, args.tts_cache
        ))
        return

    if args.images_dir or args.images_map:
        if not args.script:
            sys.exit("Error: Mode 3 requires --script (path to _script_design.json)")
        asyncio.run(images_to_video(args))
        return

    if not args.input:
        sys.exit("Error: Input HTML file required (or use --script-only / --images-dir for Mode 3)")

    asyncio.run(convert_html_to_video(args))


if __name__ == "__main__":
    main()
