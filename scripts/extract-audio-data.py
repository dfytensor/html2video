#!/usr/bin/env python3
"""
extract-audio-data.py — Extract per-frame RMS amplitude and frequency band data.

Outputs JSON with fps, totalFrames, and per-frame rms/bands arrays.
Audio data can drive GSAP animations via timeline.call().

Usage:
    python scripts/extract-audio-data.py audio.mp3 -o audio-data.json
    python scripts/extract-audio-data.py video.mp4 --fps 30 --bands 16 -o audio-data.json

Requirements:
    pip install numpy
    ffmpeg must be available in PATH (or imageio_ffmpeg will provide it)
"""

import argparse
import json
import math
import os
import struct
import subprocess
import sys


def get_ffmpeg_path():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    return "ffmpeg"


def get_duration(input_path, ffmpeg_path):
    cmd = [ffmpeg_path, "-i", input_path, "-f", "null", "-"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = result.stderr
    for line in output.split("\n"):
        if "Duration:" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = time_str.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return None


def extract_pcm(input_path, ffmpeg_path, sample_rate=44100):
    cmd = [
        ffmpeg_path,
        "-i", input_path,
        "-vn",
        "-ac", "1",
        "-ar", str(sample_rate),
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        "-"
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        sys.exit(f"ffmpeg error: {result.stderr.decode('utf-8', errors='replace')[:500]}")
    return result.stdout


def compute_frames(pcm_bytes, sample_rate, fps, bands_count):
    try:
        import numpy as np
    except ImportError:
        sys.exit("Error: numpy not installed. Run: pip install numpy")

    samples = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float64)
    samples = samples / 32768.0

    samples_per_frame = int(sample_rate / fps)
    total_frames = int(len(samples) / samples_per_frame)

    global_rms_values = []

    for f in range(total_frames):
        start = f * samples_per_frame
        end = start + samples_per_frame
        frame_samples = samples[start:end]
        rms = float(np.sqrt(np.mean(frame_samples ** 2)))
        global_rms_values.append(rms)

    max_rms = max(global_rms_values) if global_rms_values else 1.0
    if max_rms == 0:
        max_rms = 1.0

    frames_data = []
    for f in range(total_frames):
        start = f * samples_per_frame
        end = start + samples_per_frame
        frame_samples = samples[start:end]

        rms = global_rms_values[f] / max_rms

        fft = np.abs(np.fft.rfft(frame_samples))
        fft_len = len(fft)
        band_size = max(1, fft_len // bands_count)

        band_values = []
        for b in range(bands_count):
            band_start = b * band_size
            band_end = min((b + 1) * band_size, fft_len)
            if band_start < fft_len and band_end > band_start:
                band_val = float(np.mean(fft[band_start:band_end]))
            else:
                band_val = 0.0
            band_values.append(band_val)

        max_band = max(band_values) if band_values else 1.0
        if max_band > 0:
            band_values = [b / max_band for b in band_values]
        else:
            band_values = [0.0] * bands_count

        frames_data.append({
            "time": round(f / fps, 4),
            "rms": round(rms, 4),
            "bands": [round(b, 4) for b in band_values]
        })

    return {
        "fps": fps,
        "totalFrames": total_frames,
        "duration": round(total_frames / fps, 2),
        "frames": frames_data
    }


def main():
    parser = argparse.ArgumentParser(description="Extract audio amplitude/frequency data to JSON")
    parser.add_argument("input", help="Input audio/video file path")
    parser.add_argument("-o", "--output", help="Output JSON path (default: <input>_audio-data.json)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    parser.add_argument("--bands", type=int, default=16, help="Frequency band count (default: 16)")
    parser.add_argument("--sample-rate", type=int, default=44100, help="Sample rate (default: 44100)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"Error: {args.input} not found")

    ffmpeg_path = get_ffmpeg_path()

    print(f"Extracting audio from: {args.input}")
    print(f"FFmpeg: {ffmpeg_path}")
    print(f"FPS: {args.fps}, Bands: {args.bands}")

    pcm_bytes = extract_pcm(args.input, ffmpeg_path, args.sample_rate)
    print(f"PCM samples extracted: {len(pcm_bytes) // 2} samples")

    data = compute_frames(pcm_bytes, args.sample_rate, args.fps, args.bands)
    print(f"Total frames: {data['totalFrames']}, Duration: {data['duration']}s")

    output_path = args.output
    if not output_path:
        base = os.path.splitext(args.input)[0]
        output_path = base + "_audio-data.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    file_size = os.path.getsize(output_path)
    print(f"Output: {output_path} ({file_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
