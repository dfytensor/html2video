# Video Pipeline Reference

Read this file when the user requests video export ("生成视频", "导出视频", "转为视频").

---

## Prerequisites

```bash
pip install edge-tts playwright moviepy pillow
python -m playwright install chromium
```

`moviepy` auto-downloads `imageio_ffmpeg` (static ffmpeg binary), so manual ffmpeg installation is not required.

---

## Script Location

`scripts/html2video.py`

---

## Usage

```bash
# Basic: auto-generate video from HTML
python scripts/html2video.py input.html

# Specify output path
python scripts/html2video.py input.html -o output.mp4

# Resolution (default 1080x1920 portrait)
python scripts/html2video.py input.html --width 1920 --height 1080

# TTS voice (default: Yunxi male voice)
python scripts/html2video.py input.html --voice zh-CN-XiaoxiaoNeural

# Frame capture timestamps (default 5 frames)
python scripts/html2video.py input.html --frames 0.5,1.5,2.5,3.5,4.5

# Frame rate (default 24fps)
python scripts/html2video.py input.html --fps 30

# Silent video — no TTS narration
python scripts/html2video.py input.html --no-voice

# Export narration script only — no video generated
python scripts/html2video.py input.html --export-script

# Export narration script to custom path
python scripts/html2video.py input.html --export-script --script-output my_script.txt

# Keep temp files for debugging
python scripts/html2video.py input.html --keep-temp

# Custom slide CSS selector
python scripts/html2video.py input.html --slide-selector ".page"

# Full parameter example
python scripts/html2video.py AI_Animation.html \
    -o video.mp4 \
    --width 1080 --height 1920 \
    --voice zh-CN-YunxiNeural \
    --fps 24 \
    --frames 0.5,1.5,2.5,3.5,4.5

# Silent video with subtitles
python scripts/html2video.py AI_Animation.html --no-voice
```

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `input` | (required) | Input HTML file path |
| `-o / --output` | Same dir as input, `_video.mp4` suffix | Output MP4 file path |
| `--width` | 1080 | Video width (px) |
| `--height` | 1920 | Video height (px) |
| `--voice` | `zh-CN-YunxiNeural` | Edge TTS voice name |
| `--rate` | `+0%` | Speech rate adjustment (e.g. `+20%`) |
| `--fps` | 24 | Output video frame rate |
| `--frames` | `0.5,1.5,2.5,3.5,4.5` | Screenshot timestamps per slide (seconds) |
| `--subtitle` | True | Burn in subtitles |
| `--font` | `C:/Windows/Fonts/msyh.ttc` | Subtitle font path |
| `--no-subtitle` | - | Disable subtitle overlay |
| `--no-voice` | - | Skip TTS narration — output silent video (no audio track) |
| `--export-script` | - | Export narration script (TXT) and exit. No video generated. |
| `--script-output` | Same dir as input, `_script.txt` | Custom output path for narration script |
| `--keep-temp` | False | Keep temp files after completion |
| `--slide-selector` | `.slide` | CSS selector for slide elements |
| `--title` | Auto from Slide 1 text | Override hook video title (written to `_title.txt`) |
| `--cover-frame` | Auto (Slide 1, Frame 2) | Slide 1 frame index to use as cover thumbnail |

---

## Output Files

Every video export produces 3 files:

| File | Description |
|---|---|
| `{name}_video.mp4` | The video file |
| `{name}_title.txt` | Hook video title for social media publishing |
| `{name}_cover.png` | Cover thumbnail image for video platform |

---

## Internal Pipeline

```
HTML file
    |
    +-- inject_slide_nav_js() --> modified HTML with navigation JS
    |
    +-- Playwright screenshots (per slide, N frames each) --> PNG files
    |
    +-- Edge TTS (per slide text, max 200 chars) --> MP3 files
    |
    +-- PIL subtitle images (120px semi-transparent bar) --> PNG files
    |
    +-- ffmpeg per-slide composition (frames + subtitle + audio) --> segment MP4s
    |
    +-- ffmpeg concat --> final output.mp4
```

### Step Details

1. **Parse HTML:** Read HTML file, detect all `.slide` elements, extract text per slide as TTS narration
2. **Playwright Screenshot:**
   - **Slide 1 (hook slide):** Uses denser capture timing `[0.1, 0.3, 0.5, 1.0, 2.0, 3.5]` — 6 frames instead of 5, with more frames concentrated in the first second to capture the fast hook animation. This ensures the first 3 seconds of video contain rapid visual changes that hold viewer attention.
   - **Slides 2+:** Uses the standard `--frames` parameter (default 5 frames at `0.5, 1.5, 2.5, 3.5, 4.5`)
   - Each frame captures the CSS/GSAP animation at a specific timestamp
3. **Edge TTS Synthesis:** Send each slide's text to Edge TTS, generate MP3 audio. Hook slide (Slide 1) text should be short (under 30 chars) for fast delivery.
4. **PIL Subtitle Generation:** Generate bottom subtitle bar PNG for each slide (120px height, semi-transparent black background, white text)
5. **ffmpeg Composition:**
   - Divide audio duration evenly across screenshot frames
   - Hook slide has 6 frames → shorter duration per frame → more visual changes per second
   - Create video segment per frame (looped PNG scaled to target resolution)
   - Overlay subtitle image at bottom
   - Merge TTS audio track
   - Concatenate all segments into final MP4

### Hook Slide Capture Strategy

The first slide's 6-frame capture is intentional — it produces a video opening with rapid visual progression:

```
Frame 0 (0.1s) → Background + first decorative element
Frame 1 (0.3s) → Hero element popping in
Frame 2 (0.5s) → Hook text visible, ambient motion starting
Frame 3 (1.0s) → Scene settled, ambient motion continues
Frame 4 (2.0s) → Ambient motion progression
Frame 5 (3.5s) → Final state before transition
```

This creates a visually dynamic first 3 seconds compared to the old 5-frame uniform spacing.

### Single-Page HTML (No Slides)

If the HTML contains no `.slide` elements (e.g., flowchart mode output), the script treats the entire page as one slide:
- Captures frames at multiple timestamps to show different CSS animation stages
- Merges all text into a single TTS narration
- Generates a single-segment video

### Silent Mode (--no-voice)

Skips Edge TTS entirely. Each slide defaults to 5 seconds duration. Output MP4 has no audio track (`-an` flag in ffmpeg). Useful when:
- User wants to add custom audio/music later
- Content is text-only and doesn't need narration
- Quick preview without waiting for TTS generation

### Script Export (--export-script)

Extracts narration text from each slide and writes a TXT file, then exits without generating video. Output format:

```
[Page 1]
Slide 1 narration text here...

[Page 2]
Slide 2 narration text here...

```

Default output: same directory as input HTML, `_script.txt` suffix. Override with `--script-output`.

Useful when:
- User wants to review/edit narration text before recording
- Translating content or preparing scripts for human voice-over
- Using an external TTS tool instead of Edge TTS

### Caching

Screenshots (PNG) and audio (MP3) are cached in a temp directory. Existing files are skipped on re-run for faster iteration.
