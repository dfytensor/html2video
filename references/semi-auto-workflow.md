# Semi-Automatic Workflow (Mode 3)

Detailed reference for the semi-automatic pipeline: script design → TTS → image prompts → user images → video.

---

## When to Use Mode 3

| Scenario | Use Mode 3? |
|---|---|
| Want higher quality visuals than HTML screenshots | Yes |
| Want to use Midjourney/DALL-E/Stable Diffusion for images | Yes |
| Want to control image style precisely | Yes |
| Content is ready, just need a quick video | No, use Mode 1/2 (faster) |
| Need interactive/animated HTML demos | No, use Mode 1/2 |

---

## Complete Workflow

### Phase A: AI Design & Generate

#### Step 1: Script Design (口播稿)

AI analyzes user's content and produces:

1. **Scene breakdown** — Content divided into logical scenes (6-15 for short-form, 15-30 for long-form)
2. **Per-scene voiceover** — Natural spoken Chinese narration (50-200 chars each)
3. **Per-scene visual description** — What the viewer should see
4. **Duration estimates** — Based on voiceover length

**Output:** `_script_design.json`

The AI should:
- Follow the 3-Second Hook Rule for Scene 0 (same as Mode 1/2)
- Write voiceover in natural spoken language (口语化), NOT academic/written style
- Keep each scene focused on ONE visual concept
- Ensure smooth transitions between scenes

#### Step 2: TTS Generation

Generate voiceover audio from the script design:

```bash
python scripts/html2video.py --script-only project_script_design.json --tts-output ./project_tts/
```

**Output:** `tts_000.mp3`, `tts_001.mp3`, ... (one per scene)

**Voice selection tips:**
- `zh-CN-YunxiNeural` — Male, warm, educational (default)
- `zh-CN-XiaoxiaoNeural` — Female, bright, conversational
- `zh-CN-YunjianNeural` — Male, energetic, dramatic
- See `references/tts.md` for full voice catalog

#### Step 3: Image Prompt Document

AI generates detailed image prompts for each scene:

**Output:** `_image_prompts.md`

Each scene's prompt section includes:
- Filename convention (`scene_NNN_name.png`)
- Primary image generation prompt (model-agnostic)
- Negative prompt
- Visual description
- Style notes
- Aspect ratio specification

### Human Step: Generate Images

The user:
1. Reads `_image_prompts.md`
2. Copies prompts to their preferred image generation tool
3. Generates images following the naming convention
4. Places all images in a folder (e.g., `project_images/`)

**Critical naming rule:** `scene_NNN_brief_name.png`

```
project_images/
├── scene_000_hook_cover.png       # Scene 0 — hook cover
├── scene_001_intro.png            # Scene 1 — introduction
├── scene_002_core_concept.png     # Scene 2 — core concept
├── scene_003_data_visual.png      # Scene 3 — data visualization
├── scene_004_comparison.png       # Scene 4 — comparison
├── scene_005_summary.png          # Scene 5 — summary
└── scene_006_cta.png              # Scene 6 — call to action
```

### Phase B: AI Video Composition

#### Step 4: Verify & Compose

User tells AI the images are ready:

> "图片已准备好，在 `project_images/` 目录下"

AI verifies:
1. All scene images exist and match naming convention
2. Image resolution matches video dimensions (1080×1920 or 1920×1080)
3. No missing scenes (reports gaps if any)

Then composes:

```bash
python scripts/html2video.py \
  --script project_script_design.json \
  --images-dir project_images/ \
  --tts-dir ./project_tts/ \
  -o project_video.mp4
```

Or without pre-generated TTS (regenerates on the fly):

```bash
python scripts/html2video.py \
  --script project_script_design.json \
  --images-dir project_images/ \
  -o project_video.mp4
```

**Output:**
- `project_video.mp4` — Final video
- `project_video_title.txt` — Hook title for social media
- `project_video_cover.png` — Cover thumbnail (from Scene 0 image)

---

## Image Prompt Design Guidelines

### Structure of a Good Image Prompt

```
[Subject/Scene], [Composition/Layout], [Style/Aesthetic], [Color Palette],
[Lighting/Atmosphere], [Quality Modifiers] --ar 9:16
```

### Style Keywords by Content Type

| Content Type | Style Keywords |
|---|---|
| Tech/Science | "clean flat illustration, infographic style, data visualization, modern UI" |
| Business | "corporate infographic, professional, clean lines, subtle gradients" |
| Drama/Story | "cinematic, dramatic lighting, dark atmosphere, high contrast" |
| Education | "colorful illustration, friendly, approachable, flat design" |
| Nature | "organic, soft gradients, nature-inspired palette, watercolor touches" |

### Aspect Ratios

| Video Mode | Aspect Ratio | Resolution | Image Prompt Flag |
|---|---|---|---|
| Portrait (short video) | 9:16 | 1080×1920 | `--ar 9:16` |
| Landscape (presentation) | 16:9 | 1920×1080 | `--ar 16:9` |
| Square (social) | 1:1 | 1080×1080 | `--ar 1:1` |

### Text Handling

AI image generators struggle with text. For scenes that need text:
- **Option A:** Generate image WITHOUT text, add text overlay in post-production
- **Option B:** Use very simple, short text (1-3 words) in the prompt
- **Option C:** Use images with designated "text areas" (blank regions for later overlay)

Always note in the prompt document whether text should be in the image or added later.

---

## Script Design JSON Schema

```json
{
  "project": "string — project name",
  "title": "string — hook video title for social media",
  "total_scenes": "integer",
  "voice": "string — TTS voice name (default: zh-CN-YunxiNeural)",
  "rate": "string — TTS rate (default: +0%)",
  "resolution": {
    "width": "integer — video width (default: 1080)",
    "height": "integer — video height (default: 1920)"
  },
  "fps": "integer — video FPS (default: 24)",
  "global_style": "string — visual style description for consistency",
  "global_palette": "string — color palette description",
  "scenes": [
    {
      "index": "integer — scene number (0-based)",
      "title": "string — short scene title",
      "voiceover": "string — 口播稿 (natural spoken narration)",
      "visual_description": "string — what the viewer should see",
      "duration_estimate": "float — estimated seconds",
      "image_filename": "string — scene_NNN_name.png"
    }
  ]
}
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| "No images found" | Wrong naming or directory | Check `scene_NNN_*.png` pattern and directory path |
| "Missing images for scenes: [0, 3]" | Some scenes have no images | Generate missing images, or those scenes will be skipped |
| Image looks blurry in video | Source image too small | Regenerate at 1080×1920 (or higher) |
| TTS mismatch with image duration | Voiceover too long/short for image | Adjust voiceover text or use `--rate` to speed up/slow down |
| ffmpeg error on concat | Path with Chinese characters | Use `--keep-temp` to debug; ensure paths use forward slashes |
| TTS timeout | Network issues | Use `--tts-timeout 120` and `--tts-cache` |

---

## CLI Reference (Mode 3)

### Generate TTS only from script

```bash
python scripts/html2video.py --script-only script_design.json --tts-output ./tts/
```

### Compose video from images + script

```bash
python scripts/html2video.py --script script_design.json --images-dir ./images/ -o output.mp4
```

### Compose video with explicit image mapping

```bash
python scripts/html2video.py --script script_design.json --images-map images_map.json -o output.mp4
```

### Compose video with pre-generated TTS

```bash
python scripts/html2video.py --script script_design.json --images-dir ./images/ --tts-dir ./tts/ -o output.mp4
```

### Images map JSON format

```json
{
  "0": "/path/to/scene_000_cover.png",
  "1": "/path/to/scene_001_intro.png",
  "2": "/path/to/scene_002_concept.png"
}
```
