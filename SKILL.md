---
name: science-content-video
description: |
  Convert science/tech text to animated HTML demo pages and optionally export to MP4 video.
  Triggered when the user provides educational content and wants PPT slides, flowcharts,
  demo pages, or video output. Trigger phrases: "generate PPT", "generate demo page",
  "generate flowchart", "generate video", "export video", "convert to video",
  "design script", "semi-auto mode", "image prompts", "口播稿", "半自动".
  Full pipeline: text → HTML (PPT or flowchart mode) → video (MP4).
  Semi-auto pipeline: text → script design + TTS + image prompts → user images → video (MP4).
  Enhanced with narrative-hook-adapter: multi-slide hook system, three-act structure,
  inter-slide hook propagation, storyboard animation planning, and enhanced TTS narration.
---

# Science Content Video Skill

Convert science/tech text to animated HTML demos and MP4 video.
Supports both fully-automatic (HTML→video) and semi-automatic (script→user images→video) modes.

---

## Pipeline Overview

```
User provides science/tech text
        |
        +---> Mode 1/2: Fully-Automatic Pipeline ────────────────────+
        |                                                              |
        |   Phase 0: Narrative Planning (NEW)                          |
        |      Hook density + three-act structure + storyboard          |
        |              |                                               |
        |   Phase 1: Generate HTML demo page                           |
        |      Mode 1 (default): PPT carousel                          |
        |      Mode 2 (user triggers): Flowchart / flat UI             |
        |              |                                               |
        |              v                                               |
        |   Phase 2: HTML → Video                                      |
        |      Playwright screenshots (PNG)                            |
        |      Edge TTS narration with hook bridges (MP3)              |
        |      ffmpeg composition (PNG + MP3 → MP4)                    |
        |              |                                               |
        |              v                                               |
        |   Output: MP4 video file                                     |
        |                                                              |
        +---> Mode 3: Semi-Automatic Pipeline ───────────────+         |
                                                                |         |
            Step 1: Script Design (enhanced with hooks)         |         |
                口播稿 + scene descriptions + hook propagation  |         |
                Output: _script_design.json                     |         |
                     |                                        |         |
                     v                                        |         |
            Step 2: TTS Generation (enhanced VO)               |         |
                Per-scene voiceover with bridge/hook-forward    |         |
                Output: tts_000.mp3, tts_001.mp3, ...          |         |
                     |                                        |         |
                     v                                        |         |
            Step 3: Image Prompt Document                     |         |
                Per-scene prompts with shot/camera direction    |         |
                Output: _image_prompts.md                      |         |
                     |                                        |         |
                     v                                        |         |
            [User generates images externally]                 |         |
                     |                                        |         |
                     v                                        |         |
            Step 4: Image-to-Video Composition <──────────────+         |
                User provides image paths → video                       |
                Output: MP4 video file                                  |
```

---

## Visual Identity Gate

<HARD-GATE>
Before writing ANY HTML, you MUST have a visual identity defined. Do NOT write pages with default or generic colors.

Check in this order:

1. **User specified a style?** → Read [visual-styles.md](visual-styles.md) for named styles (Deep Green Science, Clean Corporate, Shadow Cut tiers, etc.). Apply the matching style's palette and typography.
2. **Content naturally fits a style?** → Use the Style Selection Matrix in [visual-styles.md](visual-styles.md) to pick the best match.
3. **None of the above?** → Ask the user 3 questions before writing any HTML:
   - What's the mood? (technical / corporate / dramatic / warm / playful)
   - Light or dark background?
   - Any specific brand colors or visual references?
   Then declare a palette (bg, fg, accent) before writing code.

Every page must trace its palette and typography back to a visual style, explicit user direction, or a deliberate choice documented in the HTML. If you're reaching for `#333`, `#3b82f6`, or `Roboto` — you skipped this step.
</HARD-GATE>

For motion defaults, sizing, entrance patterns, and easing — follow [house-style.md](house-style.md). The house style handles HOW things move. The visual style handles WHAT things look like.

---

## <HARD-GATE> Before Generating HTML

Check ALL of the following before producing any HTML output:

1. **No emoji** — All emoji must be replaced with vector UI icons (Font Awesome, Remix Icon, Lucide, Tabler, IconPark, etc.). See [references/icons.md](references/icons.md) for the full library catalog, CDN links, and emoji-to-icon mapping. Scan for residual emoji after generation.
2. **Animation class names** — All animated elements must use class `an` or `anim-item` for the animation reset logic.
3. **Animation reset JS** — The cloneNode fix must be inserted before `</body>` in every generated HTML (see `references/prompt-templates.md`).
4. **Code volume** — Generated HTML should be **800+ lines**. If the model outputs fewer, request expansion or multi-step generation.
5. **Video-ready text** — Minimum body text 18px, minimum titles 32px. Use bold, underline, color highlights for emphasis.

---

## Layout Before Animation

Position every element where it should be at its **most visible moment** — the frame where it's fully entered, correctly placed, and not yet exiting. Write this as static HTML+CSS first. No GSAP/animation yet.

**Why this matters:** If you position elements at their animated start state (offscreen, scaled to 0, opacity 0) and tween them to where you think they should land, you're guessing the final layout. Overlaps are invisible until the video renders. By building the end state first, you can see and fix layout problems before adding any motion.

### The process

1. **Identify the hero frame** for each slide — the moment when the most elements are simultaneously visible. This is the layout you build.
2. **Write static CSS** for that frame. Content containers should fill available space using `width: 100%; height: 100%; padding: Npx;` with `display: flex; flex-direction: column; gap: Npx; box-sizing: border-box`. Use padding to push content inward — avoid `position: absolute; top: Npx` on content containers (they overflow when content is taller than remaining space). Reserve `position: absolute` for decorative elements only.
3. **Add entrances with `gsap.from()`** — animate FROM offscreen/invisible TO the CSS position. The CSS position is the ground truth; the tween describes the journey to get there.
4. **Add exits with `gsap.to()`** — only on the final slide.

### When elements share space across time

If element A exits before element B enters in the same area, both should have correct CSS positions for their respective hero frames. The timeline ordering guarantees they never visually coexist — but if you skip the layout step, you won't catch accidental overlaps due to timing errors.

---

## Phase 1: Generate HTML Demo Page

### Mode 1: PPT Carousel (Default)

**Trigger:** User provides science content and wants a demo page/PPT.

#### Step 1 — Generate Prompt

Read `references/prompt-templates.md` and apply the **Mode 1, Step 1** prompt template to the user's input text.

#### Step 2 — Generate HTML

Use the prompt from Step 1 to have the model generate complete HTML. **Mandatory: append both constraints (emoji replacement + unified animation classes) and insert the animation reset JS.**

See `references/prompt-templates.md` for exact constraint text and JS code.

**Output path:** User-specified, or default `/home/mt/桌面/AI_Animation.html`.

#### Step 3 — Restructure with PPT Template

<HARD-GATE> AI must first read `assets/templates/PPT Template-level2/SUMMARY.md` to select the best template.

**Template priority:**
1. `assets/templates/PPT Template-level2/` — 25 templates, AI selects by content type
2. `assets/templates/PPT/` — fallback (PPT-Generate-1 through 4)

Read `references/template-selection.md` for the quick selection guide.

**Prompt template:** See `references/prompt-templates.md` → Mode 1, Step 3.

**After restructure:** Verify the animation reset JS is present. If missing, insert it.

---

### Mode 2: Flowchart / Flat UI

**Trigger:** User explicitly says "generate flowchart" after Mode 1 is complete.

<HARD-GATE> Mode 2 does NOT generate new content. It restructures existing PPT HTML into flat UI style. Mode 1 must be completed first.

#### Step 1 — Select Template

Read `assets/templates/Animation/SUMMARY.md`, then select the best Animation template.

Read `references/template-selection.md` → Animation Template Selection for the quick guide.

**Default:** `assets/templates/Animation/RNN-3.html`

#### Step 2 — Restructure

Apply the **Mode 2, Step 2** prompt template from `references/prompt-templates.md`.

---

## Phase 2: HTML → Video

**Trigger:** User says "generate video", "export video", "convert to video".
**Prerequisite:** Phase 1 must be complete with a valid HTML file.

### Dependencies

```bash
pip install edge-tts playwright moviepy pillow
python -m playwright install chromium
```

### Pipeline Architecture (Divide & Conquer)

```
Phase 1 — Screenshots
    HTML → Playwright screenshots (PNG) + text extraction
    (runs in executor, isolated from TTS)

Phase 2 — TTS (Divide & Conquer)
    Per-slide text → individual TTS generation
    ├── Per-file timeout (default 60s, configurable)
    ├── Automatic retry (default 2 attempts)
    ├── Disk cache (opt-in with --tts-cache, reuse across runs)
    └── Graceful fallback: failed TTS → silent slide

Phase 3 — Compose
    Screenshots + audio + subtitles → per-slide MP4 segments

Phase 4 — Concat
    All segments → final MP4
```

**Why divide & conquer?** The original pipeline ran TTS as a single blocking step — if one TTS call hung (network issue, long text, Edge service latency), the entire process would stall indefinitely. The D&C approach isolates each TTS call with its own timeout and retry, so a single failure cannot kill the entire pipeline. Failed slides degrade gracefully to silent mode rather than crashing.

### Script

```bash
python scripts/html2video.py input.html [options]
```

### Key Parameters

| Parameter | Default | Description |
|---|---|---|
| `-o` | Same dir, `_video.mp4` suffix | Output MP4 path |
| `--width / --height` | 1080 × 1920 | Video resolution (portrait) |
| `--voice` | `zh-CN-YunxiNeural` | Edge TTS voice |
| `--rate` | `+0%` | Speech rate (e.g. `+20%`) |
| `--fps` | 24 | Output frame rate |
| `--frames` | `0.5,1.5,2.5,3.5,4.5` | Screenshot timestamps per slide |
| `--no-subtitle` | (off) | Disable subtitle overlay |
| `--no-voice` | (off) | Skip TTS narration — silent video |
| `--export-script` | (off) | Export narration script (TXT) and exit |
| `--script-output` | Same dir, `_script.txt` | Custom path for narration script |
| `--keep-temp` | (off) | Keep temp files for debugging |
| `--slide-selector` | `.slide` | CSS selector for slide elements |
| `--tts-timeout` | 60 | Per-file TTS timeout in seconds |
| `--tts-retries` | 2 | Max retries per TTS file |
| `--tts-cache` | (off) | Enable TTS disk cache (reuse across runs) |

### TTS Divide & Conquer Details

The TTS generation follows a robust per-slide isolation strategy:

1. **Independent generation**: Each slide's TTS is generated as a standalone file (`tts_000.mp3`, `tts_001.mp3`, ...)
2. **Per-file timeout**: Each `edge_tts.Communicate.save()` call is wrapped in `asyncio.wait_for()` with a configurable timeout (default 60s). If a single TTS call hangs, it is cancelled without affecting others.
3. **Automatic retry**: Failed TTS calls are retried up to `--tts-retries` times (default 2). Each retry is a fresh connection to the Edge TTS service.
4. **Disk cache** (`--tts-cache`): Generated TTS files are cached by content hash (`MD5(text|voice|rate)`). On subsequent runs with the same content, cached files are reused instantly — zero TTS calls needed. Cache is stored in `<temp_dir>/.tts_cache/`.
5. **Graceful degradation**: If all retries fail for a slide, that slide becomes silent (no audio). The video is still generated with the remaining slides having audio.

**Typical performance** (13 slides, ~200 chars each):
- Without cache: ~35 seconds total TTS
- With cache (repeat run): <1 second (all cache hits)

### Troubleshooting TTS

| Problem | Cause | Fix |
|---|---|---|
| "TIMEOUT" on all slides | Network/firewall blocking Edge TTS | Check internet, try `--tts-timeout 120` |
| "TIMEOUT" on specific slides | Very long text (>200 chars truncated) | Reduce slide text or increase `--tts-timeout` |
| Partial TTS failure | Intermittent network | Increase `--tts-retries 3`, use `--tts-cache` |
| TTS too slow overall | Network latency | Use `--tts-cache` to reuse on repeat runs |

Full pipeline details: read `references/video-pipeline.md`.

---

## Mode 3: Semi-Automatic Pipeline (Script Design + Image Prompts → User Images → Video)

**Trigger:** User says "design script", "semi-auto mode", "口播稿设计", "半自动", "image prompts", or wants to use external image generation tools.
**Prerequisite:** User provides science/tech text content (same as Mode 1).

### Overview

Mode 3 is a **two-phase workflow** separated by a human-in-the-loop step:

1. **Phase A (AI generates):** Script design, TTS audio, and image prompt documents
2. **Human step:** User generates images using Midjourney/DALL-E/Stable Diffusion/etc. based on the prompts
3. **Phase B (AI composites):** User provides image paths → AI composes final video

This mode is for users who want **higher quality visuals** than HTML-rendered screenshots, or who want to use specialized image generation models.

```
User provides text content
        |
        v
  Phase A: AI Design & Generate
     Step 1: Script Design (口播稿 + scene breakdown)
     Step 2: TTS Audio Generation (per-scene voiceover)
     Step 3: Image Prompt Document (per-scene prompts for image gen models)
     Output: _script_design.json + _image_prompts.md + tts_*.mp3
        |
        v
  [USER STEP: Generate images using external tools]
     User reads _image_prompts.md
     User generates images named per convention: scene_NNN_name.png
     User places images in designated folder
        |
        v
  Phase B: AI Video Composition
     User tells AI image paths or folder location
     Step 4: Images + TTS → per-scene MP4 segments
     Step 5: Concatenate → final MP4
     Output: MP4 video file
```

### Step 1 — Script Design (口播稿 + Scene Breakdown)

<HARD-GATE>
Before generating any output, the AI MUST design the complete script structure. This includes:

1. **Scene count** — Determine how many scenes/pages the content naturally divides into (typically 6-15 scenes for short-form video, 15-30 for long-form)
2. **Per-scene voiceover script (口播稿)** — Write natural spoken-language narration for each scene. NOT the same as written text — it must sound natural when spoken aloud. Each scene's narration should be 50-200 characters (Chinese) or 20-80 words (English).
3. **Per-scene visual description** — Describe what the viewer should see: layout, key visual elements, data points, diagrams, etc.
4. **Per-scene hook title** — Short title for each scene (used as the display title in the image prompt and as internal reference)
5. **Scene duration estimate** — Based on voiceover length (typically 3-8 seconds per scene)
</HARD-GATE>

**Output format:** `_script_design.json`

```json
{
  "project": "项目名称",
  "total_scenes": 8,
  "voice": "zh-CN-YunxiNeural",
  "rate": "+0%",
  "resolution": { "width": 1080, "height": 1920 },
  "fps": 24,
  "scenes": [
    {
      "index": 0,
      "title": "钩子标题",
      "voiceover": "口播稿文本，自然口语化的旁白内容...",
      "visual_description": "场景视觉描述：布局、关键元素、数据点、图示等",
      "duration_estimate": 5.0,
      "image_filename": "scene_000_hook_cover.png",
      "act": "起因",
      "hook_type": "STAT",
      "hook_role": "opening",
      "hook_forward": "此场景结尾向下一场景传递的钩子/悬念",
      "shot_size": "CU",
      "camera_move": "quick_push"
    },
    {
      "index": 1,
      "title": "主题介绍",
      "voiceover": "第二段口播稿...",
      "visual_description": "场景视觉描述...",
      "duration_estimate": 6.5,
      "image_filename": "scene_001_topic_intro.png",
      "act": "起因",
      "hook_type": "CHALLENGE",
      "hook_role": "problem_framing",
      "hook_forward": "向下一场景的悬念句",
      "shot_size": "MS",
      "camera_move": "tracking"
    }
  ]
}
```

**New fields explained:**

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `act` | Yes | `"起因"` / `"经过"` / `"结果"` | Which act this scene belongs to (three-act structure) |
| `hook_type` | Yes | `STAT`, `COUNTER`, `MYSTERY`, `CHALLENGE`, `RESULT`, `PROMISE` | Tech-adapted hook type for this scene |
| `hook_role` | Yes | `opening`, `problem_framing`, `mid_escalation`, `development`, `payoff`, `closing` | This scene's role in the hook propagation chain |
| `hook_forward` | Yes | Free text (1-2 sentences) | The curiosity gap / half-result / bridge planted at end of this scene for the next |
| `shot_size` | Recommended | `ELS`, `LS`, `FS`, `MS`, `MCU`, `CU`, `ECU` | Virtual shot size — guides image composition and animation scale |
| `camera_move` | Recommended | `fixed`, `push`, `pull`, `pan`, `tilt`, `tracking`, `quick_push`, `quick_pull`, `handheld` | Virtual camera movement — guides animation direction |

**Script design rules:**
- Scene 0 (cover) MUST follow the 3-Second Hook Rule (same as Mode 1/2)
- Voiceover text should be natural spoken language, NOT written/academic style
- Each scene should have one clear visual focus (don't overload a single scene)
- Scene transitions should feel natural (not abrupt topic jumps)
- Total voiceover duration should match target video length (30s-3min for short-form, 5-15min for long-form)

### Step 2 — TTS Audio Generation

Generate voiceover audio for each scene from the script design.

```bash
python scripts/html2video.py --script-only _script_design.json --tts-output ./output_tts/
```

Or AI does it automatically during Phase A.

**Output:** `tts_000.mp3`, `tts_001.mp3`, `tts_002.mp3`, ... (one per scene)

**Note:** The `--script-only` flag tells the pipeline to ONLY generate TTS from the script design JSON, without needing an HTML file. See script usage below.

### Step 3 — Image Prompt Document

<HARD-GATE>
The image prompt document MUST be detailed enough for a user to copy-paste into any image generation tool (Midjourney, DALL-E, Stable Diffusion, Flux, etc.) and get usable results.

Each scene's prompt MUST include:
1. **Subject** — What is the main visual element
2. **Composition** — Layout, framing, positioning
3. **Style** — Art style, aesthetic direction
4. **Color palette** — Specific colors or mood
5. **Text overlay notes** — Any text that should appear on the image (or note that text will be added in post)
6. **Aspect ratio** — Always specify (9:16 for portrait video, 16:9 for landscape)
7. **Negative prompt** (optional) — Things to avoid
</HARD-GATE>

**Output format:** `_image_prompts.md`

```markdown
# Image Prompt Document: {项目名称}

## Image Naming Convention

All images MUST follow this naming pattern:
  scene_{NNN}_{brief_name}.png

Examples:
- scene_000_hook_cover.png
- scene_001_topic_intro.png
- scene_002_detail_diagram.png
- scene_003_comparison.png
- scene_004_summary.png
- scene_005_cta.png

Rules:
- NNN: zero-padded 3-digit scene index (000, 001, 002, ...)
- brief_name: lowercase English, underscore-separated, descriptive (2-4 words)
- Format: PNG (lossless, best for video composition)
- Resolution: 1080×1920 (portrait) or 1920×1080 (landscape) — match video resolution
- NO text overlays unless explicitly noted — TTS subtitles are added during video composition

## Global Style

- Style: [e.g., "clean flat illustration, corporate infographics, soft gradients"]
- Color palette: [e.g., "deep green #1a4a3a, accent gold #d4a843, white text"]
- Typography notes: [e.g., "text will be overlaid in post-production, images should be text-free"]
- Aspect ratio: 9:16 (portrait, 1080×1920)

---

## Scene 000: {钩子标题/cover}

**Filename:** `scene_000_hook_cover.png`
**Scene duration:** ~5.0s (TTS: {口播稿前30字}...)

### Image Generation Prompt

> [Detailed prompt for Midjourney/DALL-E/SD]
>
> Example: "A dramatic split-screen composition, left side showing a dark chaotic network
> with red warning symbols, right side showing a clean organized network with green checkmarks,
> bold contrast, cinematic lighting, ultra-detailed infographic style, dark background with
> neon accent colors, 9:16 aspect ratio --ar 9:16 --v 6.0"

### Negative Prompt

> text, watermark, blurry, low quality, deformed, realistic photo

### Visual Description

{Detailed description of what this scene should look like}

### Notes

- This is the HOOK COVER — it MUST grab attention immediately
- Use high contrast, bold colors, dramatic composition
- NO text on the image (subtitle added in post)

---

## Scene 001: {主题介绍}

**Filename:** `scene_001_topic_intro.png`
... (repeat for each scene)
```

**Prompt design rules:**
- Prompts should be **model-agnostic** — usable with Midjourney, DALL-E, SD, Flux, etc.
- Include `--ar 9:16` or `--ar 16:9` suffix for Midjourney compatibility
- For text-heavy scenes, note that text will be added in post-production (AI image generators struggle with text)
- Provide style consistency notes so all images have a cohesive visual identity
- Reference the Global Style section in each prompt for consistency

### Image Naming Convention (Non-Negotiable)

<HARD-GATE>
All user-provided images MUST follow this naming convention. The video composition pipeline depends on it.

**Pattern:** `scene_{NNN}_{brief_name}.png`

| Component | Rule | Example |
|---|---|---|
| `scene_` | Fixed prefix | `scene_` |
| `{NNN}` | Zero-padded 3-digit index matching scene index in `_script_design.json` | `000`, `001`, `012` |
| `_` | Separator | `_` |
| `{brief_name}` | Lowercase English, 2-4 underscore-separated words describing the scene | `hook_cover`, `intro`, `detail_chart` |
| `.png` | Fixed extension (PNG required for lossless quality) | `.png` |

**Valid examples:**
- `scene_000_hook_cover.png` — Scene 0, the hook/cover
- `scene_001_intro.png` — Scene 1, introduction
- `scene_005_architecture_diagram.png` — Scene 5, architecture diagram
- `scene_012_summary.png` — Scene 12, summary

**Invalid examples:**
- `cover.png` — Missing scene prefix and index
- `scene1_cover.png` — Index not zero-padded
- `scene_001_这是一个很长的中文描述.png` — Non-ASCII characters in name
- `scene_001.jpg` — Wrong format (must be PNG)

**Why this matters:** The `--images-dir` mode automatically discovers images by matching the `scene_NNN_*` pattern and sorts them by scene index. Incorrect naming = missing scenes in the final video.
</HARD-GATE>

### Step 4 — User Provides Images (Human-in-the-Loop)

After the user generates images using external tools:

**Option A: Place images in a folder**
```
output_images/
├── scene_000_hook_cover.png
├── scene_001_intro.png
├── scene_002_core_concept.png
├── scene_003_data_chart.png
├── scene_004_comparison.png
└── scene_005_summary.png
```

Then tell AI: "Images are ready at `output_images/`"

**Option B: Provide explicit mapping**
Tell AI: "Here are my images: scene 0 = `path/to/cover.png`, scene 1 = `path/to/intro.png`, ..."

**Option C: Tell AI image paths directly**
Tell AI: "My images: `D:/images/cover.png`, `D:/images/intro.png`, `D:/images/concept.png`, ..."

AI will ask for confirmation before proceeding to video composition.

### Step 5 — Image-to-Video Composition

Once images are provided, compose the final video:

```bash
python scripts/html2video.py --images-dir ./output_images/ --script _script_design.json -o output_video.mp4
```

**Pipeline:**
1. Load `_script_design.json` for scene metadata and TTS mapping
2. Discover images from `--images-dir` matching `scene_NNN_*` pattern
3. Use previously generated TTS audio (or regenerate from script)
4. For each scene: image + TTS audio → per-scene MP4 segment
5. Concatenate all segments → final MP4
6. Generate hook title (`_title.txt`) and cover thumbnail (`_cover.png`)

**Parameters for semi-auto mode:**

| Parameter | Description |
|---|---|
| `--script` | Path to `_script_design.json` from Step 1 |
| `--images-dir` | Directory containing user-generated images (auto-discovered by naming pattern) |
| `--images-map` | JSON file mapping scene index to explicit image path (overrides `--images-dir`) |
| `--tts-dir` | Directory containing pre-generated TTS audio (from Step 2). If omitted, TTS is regenerated |

### Semi-Auto Mode — Complete Workflow Example

**User input:** "帮我用半自动模式做一个关于TCP三次握手的科普视频"

**AI Phase A:**
1. Designs 8 scenes with voiceover scripts
2. Generates `_script_design.json` with all scene metadata
3. Generates TTS audio for each scene → `tts_000.mp3` ... `tts_007.mp3`
4. Generates `_image_prompts.md` with detailed image generation prompts for each scene
5. Tells user: "Script design and TTS are ready. Please generate images using the prompts in `_image_prompts.md`. Place images in a folder named `tcp_images/` following the naming convention."

**Human step:**
6. User copies prompts to Midjourney/DALL-E/SD
7. User generates 8 images, names them correctly, places in `tcp_images/`

**AI Phase B:**
8. User says: "Images ready at `tcp_images/`"
9. AI verifies all 8 images exist and match naming convention
10. AI runs: `python scripts/html2video.py --images-dir tcp_images/ --script tcp_script_design.json -o tcp_video.mp4`
11. AI delivers final MP4 video

### Semi-Auto Mode — Trigger Phrases

| User says | AI should |
|---|---|
| "半自动模式" / "semi-auto" | Enter Mode 3, start from Step 1 |
| "设计口播稿" / "design script" | Enter Mode 3, focus on Step 1-2 |
| "生成图片提示词" / "image prompts" | If script exists, proceed to Step 3; otherwise start from Step 1 |
| "图片已准备好" / "images ready" | Proceed to Step 5 (video composition) |
| "合成视频" with images | Verify images exist, proceed to Step 5 |

---

## Rules (Non-Negotiable)

1. **Never use emoji** in generated HTML — replace with vector UI icons (Font Awesome, Remix Icon, Lucide, Tabler, IconPark, etc.). See [references/icons.md](references/icons.md) for the full library catalog, CDN links, and emoji-to-icon mapping.
2. **Always insert animation reset JS** before `</body>` — cloneNode fix for CSS mode; `tl.restart()` for GSAP mode
3. **Mode 2 requires Mode 1 first** — flowchart mode only restructures, never creates new content
4. **Deterministic output** — no `Math.random()`, no `Date.now()` in generated code. Use a seeded PRNG (e.g. mulberry32) if you need pseudo-random values
5. **Entrance animations only** — elements animate in; exit animations forbidden except on the final slide
6. **Code volume minimum** — target 800+ lines of HTML for substantive content
7. **Video-safe typography** — body ≥18px, titles ≥32px, high contrast colors
8. **Read SUMMARY.md before template selection** — AI must always read the template guide before choosing a template
9. **Vary easing and speed** — no more than 2 tweens with the same ease in a scene; slowest scene 3x slower than fastest
10. **Build / Breathe / Resolve** — every scene has three phases; don't dump everything in the build
11. **Quality check before video** — run `animation-map.py` and `contrast-report.py` before exporting MP4
12. **Layout before animation** — build the hero frame as static CSS first, then animate FROM offscreen TO those positions
13. **<HARD-GATE> 3-Second Hook Rule** — the first slide MUST capture attention within the first 3 seconds of video playback. This means: (a) visual punch at frame 0, (b) motion within 0.3s, (c) curiosity-gap title by 1.0s, (d) audio hook as first TTS sentence. ALL four sub-conditions are mandatory. See [3-Second Hook Rule](#3-second-hook-rule) below
14. **<HARD-GATE> Audio Hook** — the first sentence of TTS narration for Slide 1 must be a hook (shock/question/challenge/promise), NOT an introduction or definition. BANNED openings: "今天我们来了解", "让我们学习", "下面介绍", "XXX是一种"
15. **Mode 3 image naming** — user-provided images MUST follow `scene_NNN_brief_name.png` convention. No exceptions. Incorrect naming = video composition failure.
16. **Mode 3 script design before prompts** — the script design JSON (`_script_design.json`) MUST be completed before generating the image prompt document (`_image_prompts.md`). Image prompts derive from scene descriptions.
17. **Mode 3 image verification** — before composing video from user images, AI MUST verify: (a) correct file naming, (b) correct resolution (match video dimensions), (c) all scenes have corresponding images. Report missing/malformed images to user before proceeding.
18. **Mode 3 voiceover is spoken language** — 口播稿 must use natural spoken Chinese, NOT written/academic style. Read it aloud mentally — if it sounds like a textbook, rewrite it.
19. **<HARD-GATE> Hook density for 5+ slides** — every video with 5+ slides must have: (a) opening hook (Slide 1), (b) mid-escalation hook (40-60% range), (c) closing hook (last slide). No flat middle sections allowed.
20. **<HARD-GATE> Inter-slide hook propagation** — every slide (except the last) must plant a curiosity gap for the next slide via TTS bridge, visual tease, question carry, or half-result. No isolated "next slide please" transitions.
21. **<HARD-GATE> Three-act structure for 6+ slides** — slides must be organized into 起因(~25%) → 经过(~50%) → 结果(~25%). Each act's purpose must be fulfilled.
22. **Animation speed matches narrative act** — Act 1 fast emphasis (0.15-0.35s), Act 2 medium flow (0.3-0.6s), Act 3 slow resolution (0.5-1.0s). Hook reveals use quick push/pull.

---

## 3-Second Hook Rule

<HARD-GATE>
The first slide is the most important slide. If the viewer is not hooked within 3 seconds, they leave. This rule is non-negotiable and overrides all other style/animation preferences for Slide 1.

**Three-layer hook enforcement:** The hook must work at THREE levels simultaneously:
1. **Frame 0 (0.0s)** — Visual punch: what the viewer sees BEFORE anything moves
2. **Frame 1 (0.3s)** — Motion hook: what grabs them through dynamic energy
3. **Frame 2 (1.0-3.0s)** — Content hook: the title/subtitle that plants the curiosity gap

All three layers are mandatory. A beautiful frame with no motion feels static. Fast motion with no visual punch feels chaotic. A great title with a boring first frame gets scrolled past before it's read.
</HARD-GATE>

### The Problem

Typical AI-generated videos open with a gentle title slide: text fades in over 2 seconds with soft music. By the time content appears, the viewer has already scrolled away. The 3-second hook rule ensures the first frame demands attention.

**Why 3 seconds?** Short video platforms (抖音/快手/B站) auto-play content in a feed. The viewer's thumb hovers over the scroll gesture. You have roughly 1-3 seconds to:
1. Stop the thumb from scrolling (visual punch at frame 0)
2. Convince the brain this is worth watching (motion energy at 0.3s)
3. Plant a question the viewer needs answered (curiosity gap by 1.0-3.0s)

### Slide 1 — Hook Cover Construction

The first slide IS the cover/title page — but it must be a **hook cover**, not a boring title card. The cover itself must trigger curiosity, shock, or recognition in under 1 second. The title IS the hook.

**Structure (all required, all layers enforced):**

1. **Hook Title (primary)** — The main title must create a curiosity gap. Rewrite the topic into a provocative question, surprising claim, or dramatic framing. The title IS the hook — not separate from it.
2. **Visual punch (frame 0)** — The very first rendered frame must contain a striking visual element: oversized number, provocative question, dramatic contrast, or vivid icon. No gentle gradients or empty backgrounds. This is what stops the scroll BEFORE any animation plays.
3. **Motion within 0.3s** — At least one element must be visibly moving/changing by 0.3 seconds into the slide. NOT waiting for 0.5s+ delays. Use fast, high-energy entrance (0.15-0.25s duration).
4. **Subtitle with tension** — A secondary line that deepens the curiosity gap or raises the stakes, NOT a plain topic description.
5. **No full reveal** — The cover must withhold the answer/definition. It creates tension that can only be resolved by watching the next slide.
6. **Audio hook (TTS/voice)** — The first sentence of narration MUST reinforce the hook, not introduce the topic. Start with the provocative claim, shocking statistic, or question — NOT "今天我们来了解...".

### Hook Title Patterns (Expanded — 12 Types)

Use one pattern. This IS the page title. The hook title pattern determines the entire emotional strategy of the cover.

| # | Pattern | Title (Hook) | Subtitle (Deepen Tension) | Emotion |
|---|---|---|---|---|
| 1 | Surprising statistic | "95% 的人都理解错了" | "关于 TCP，你可能也是其中之一" | Shock + exclusion |
| 2 | Provocative question | "如果没有 TCP，互联网会怎样？" | "答案可能让你后背发凉" | Curiosity + dread |
| 3 | Counterintuitive claim | "WiFi 根本不是无线" | "信号的背后，全是线" | Cognitive dissonance |
| 4 | Dramatic number | "7 层，3 次崩溃" | "OSI 模型背后的血泪史" | Scale + tragedy |
| 5 | "你不知道的" | "被遗忘了 30 年的天才" | "WiFi 之父从未拿到一分钱" | Injustice + mystery |
| 6 | Direct challenge | "你能解释清楚 OSI 吗？" | "99% 的程序员做不到" | Challenge + social proof |
| 7 | Fear/loss framing | "面试必挂的协议题" | "TCP 三次握手，你真的懂吗？" | Fear of failure |
| 8 | Before/after contrast | "从月入3千到年入百万" | "他只改了一个习惯" | Aspiration + simplicity |
| 9 | Result-first reveal | "这个效果，居然是 CSS 做的" | "没有一行 JavaScript" | Surprise + skepticism |
| 10 | Benefit promise | "3 分钟学会 TCP" | "别人花了 3 年才搞懂" | Efficiency + superiority |
| 11 | Authority flex | "大厂面试官揭秘" | "TCP 这道题，他看了 10000 份答案" | Authority + insider |
| 12 | Story cliffhanger | "凌晨 3 点，服务器全崩了" | "原因竟然是一个标点符号" | Urgency + absurdity |

### Visual Punch Techniques (Frame 0 — What Stops the Scroll)

The visual punch must work at frame 0 — before any animation plays. Choose at least ONE:

| Technique | Implementation | Example |
|---|---|---|
| **Oversized number** | 120-200px stat in accent color, pinned to edge | Giant "95%" at left, faded to 30% opacity |
| **Provocative text fragment** | 2-3 word hook in 80-100px, cropped by frame edge | "你错了" bleeding off top of frame |
| **Before/after split** | Frame split 50/50 with contrasting colors/imagery | Left half dark "BEFORE", right half bright "AFTER" |
| **Result showcase** | Final/finished result displayed prominently at frame 0 | The polished UI the tutorial will build |
| **Dramatic icon** | Single large icon (SVG) at 200-400px, accent color | Warning triangle filling 40% of frame |
| **Redacted/blurred element** | Key information obscured, labeled with "?" | Blurred card with "??? " overlay |
| **Extreme contrast** | Black frame with single neon word, or white frame with red number | Pure black, single "7" in crimson 180px |
| **Split-screen conflict** | Two opposing visual elements side by side | "TCP" vs "UDP" in opposing colors |

### Audio Hook Strategy (TTS Narration for Slide 1)

The first sentence of TTS narration must be a hook, not an introduction. The viewer hears this while seeing the hook cover.

**Audio hook patterns (choose one):**

| Pattern | First Sentence | BANNED Alternative |
|---|---|---|
| Shock opening | "95%的程序员都答错了这道面试题" | "今天我们来学习TCP协议" |
| Question opening | "如果没有TCP，你现在能刷到这条视频吗？" | "TCP是一种传输层协议" |
| Claim opening | "WiFi信号的本质，其实全是线" | "WiFi是无线局域网技术" |
| Challenge opening | "你能用一句话解释清楚TCP三次握手吗？" | "下面我们详细讲解TCP" |
| Story opening | "凌晨三点，某大厂的服务器突然全部宕机" | "让我们了解一个网络案例" |
| Promise opening | "三分钟之后，TCP对你不再有任何秘密" | "本视频将介绍TCP的基础知识" |

**Rule:** The first TTS sentence must be a complete hook on its own. Even without the visual, hearing this sentence should make the viewer want to continue.

### BANNED Cover Patterns (Skip Triggers — Zero Tolerance)

These patterns are PROVEN to lose viewers in the first second. If you generate any of these, the hook has failed:

- "今天我们来了解/学习/探讨..." (boring preamble — the viewer already left)
- "XXX 详解" / "XXX 简介" / "XXX 入门" (encyclopedia title — no emotional hook)
- "XXX 是一种..." (dictionary definition as subtitle — kills curiosity)
- Pure centered title + subtitle on gradient background with no visual punch
- Any cover where the viewer's first thought is "我已经知道了" (I already know this)
- Cover animations that take > 1.0s to show all elements
- Cover where the largest text element is a plain topic name (not a hook)
- Cover with no contrasting colors (monotone = invisible in feed)
- TTS opening with "今天"/"让我们"/"下面我们" (instant scroll-away)

### Slide 1 — Animation Rules

| Rule | Requirement | Why |
|---|---|---|
| First element visible | ≤ 0.15s after slide appears | The viewer's thumb is already moving to scroll |
| All hero elements visible | ≤ 1.0s | The hook must be fully readable within 1 second |
| Animation duration | 0.15-0.35s (fast, snappy) | Slow animations feel like loading, not energy |
| Easing | `expo.out` or `back.out(1.2)` (confident, punchy) | `sine`/`power1` feel sluggish on a hook |
| Ambient motion | Start by 0.5s — particle burst, scale pulse, color shift | Static covers look like screenshots, not video |
| Background | NEVER pure solid or simple gradient | Must have decorative elements visible at frame 0 |
| Hero element scale | Title at 64-120px, accent at full saturation | Small text = invisible on mobile |
| Asymmetric layout | Pin hook title to corner or edge, use negative space | Centered-everything = wallpaper, not billboard |

### Slide 1 — Frame-by-Frame Breakdown

| Time | What the viewer sees | What they feel |
|---|---|---|
| 0.0s | Background + visual punch (oversized number, dramatic icon, split screen) | "Wait, what is this?" → thumb pauses |
| 0.05-0.15s | Hook title arrives (fast scale pop or snap-in) | "Oh, this looks interesting" |
| 0.2-0.3s | Subtitle/tension line appears | "I need to know the answer" |
| 0.3-0.5s | Accent elements arrive, ambient motion starts | "This is dynamic, not a slideshow" |
| 0.5-1.0s | Scene settles, ambient motion continues | Hook is planted, viewer committed |
| 1.0-3.0s | TTS narration delivers audio hook | "I'm definitely watching this" |

### Slide 2 — "Now Explain" Slide

Slide 2 is where the actual topic introduction belongs. The hook cover has set the tension; now deliver the payoff:
- Reveal the answer to the hook's question / explain the surprising claim
- Provide context / definition / structure overview
- Begin the educational content

This two-slide pattern (hook cover → explanation) ensures the viewer is invested before the educational content begins.

**Slide 2 transition:** Use the most distinctive/energetic transition of the entire video from Slide 1 → Slide 2. This is the moment the viewer decides to keep watching. Recommended: zoom through, glitch, or light leak (0.15-0.3s, `power4` or `expo`). See [references/transitions.md](references/transitions.md).

### Video Pipeline — First Slide Capture

The first slide's screenshot timing is critical. See `references/video-pipeline.md` for the modified capture strategy that uses denser early frames for the hook slide.

**Hook slide capture density:** Slide 1 uses 6 frames @ 0.1s/0.3s/0.5s/1.0s/2.0s/3.5s (vs. standard 5 frames for other slides). This ensures the hook's fast animations are properly captured at peak visual impact.

### Hook Video Title & Cover Thumbnail

When generating video for publishing (B站/抖音/快手等), the video's **publish title** and **cover thumbnail** are the first things users see — before they even click play. Both must be hooks.

<HARD-GATE>
Every video export MUST also output:
1. A hook video title file (`_title.txt`) — the publish caption for social media
2. A hook cover thumbnail (`_cover.png`) — the cover frame for the video platform
</HARD-GATE>

#### Hook Video Title (`_title.txt`)

Derive from the hook cover's title/subtitle. The video title (publish caption) is what users read before deciding to click — it must be a hook too.

**Title format:** `{hook claim/question} | {tension payoff}`

| From Cover | Video Title |
|---|---|
| "95% 的人都理解错了" + "关于TCP" | 95%的人都理解错了TCP \| 你可能也是其中之一 |
| "WiFi 根本不是无线" | WiFi根本不是无线？信号背后的真相 |
| "7层，3次崩溃" | 7层网络3次崩溃 \| OSI模型背后的血泪史 |
| "面试必挂的协议题" | 面试必挂！TCP三次握手你真的懂吗？ |
| "从月入3千到年入百万" | 月入3千到年入百万\| 他只改了一个习惯 |
| "凌晨3点，服务器全崩了" | 凌晨3点服务器全崩\| 原因竟然是一个标点 |

**Rules:**
- Under 30 characters (platform limit for most short video apps)
- Must include curiosity gap or emotional trigger
- BANNED: "XXX详解", "XXX教程", "带你了解XXX"
- First 10 characters must contain the hook — platforms truncate long titles

The title is auto-generated by `html2video.py` using the first slide's extracted text, or can be overridden with `--title`.

#### Hook Cover Thumbnail (`_cover.png`)

The cover is **independently generated** by `generate_cover_image()` — NOT extracted from slide screenshots. It is a programmatically designed image with 3D perspective, hook emphasis, and conflict composition.

**Auto-generated by `html2video.py` as `{output_name}_cover.png`.** No HTML content dependency — the cover works even without screenshots.

##### Cover Style Types

`generate_cover_image()` supports multiple visual styles via the `style` parameter:

| Style | Key | Visual Effect | Best For |
|---|---|---|---|
| **Impact 3D** | `"impact_3d"` (default) | Per-character size gradient (small→large), color shift (blue→gold), diagonal baseline, hook-word boost 1.4x | Shock hooks, numbers, short punchy titles |
| **Cinematic Epic** | `"cinematic"` | Serif gold title on deep navy, star-field particles, golden glow orbs, dramatic vignette | History, mythology, war, religion |
| **Warning Alert** | `"warning"` | Red/black high-contrast, pulsing danger ring, diagonal slashes, oversized warning icon | Danger, failure, risk, security |
| **Split Conflict** | `"split"` | Frame split 50/50 with opposing colors, "VS" layout, two contrasting text blocks | Debate, comparison, A/B topics |
| **Minimal Bold** | `"minimal"` | Single centered oversized word, extreme contrast, no decoration, pure typography | Short titles (1-4 chars), stark impact |

**Style selection rules:**
- Default: `"impact_3d"` — works for all hook patterns
- Match to Shadow Cut tier if one is active (Epic → `"cinematic"`, Dramatic → `"warning"`)
- Mode 3 script design can specify `"cover_style"` in `_script_design.json`
- Override via `--cover-style` CLI argument

##### Impact 3D Style — Technical Details (Default)

The default style renders each character independently with progressive 3D depth:

**Per-character 3D rendering:**
- Font size gradient: `min_fs` → `max_fs` (e.g., 38px → 160px) with `t^0.8` curve
- Hook word detection: digits `% ！ ！？ ？` → 1.4x size boost
- Diagonal baseline: small chars high-left (far), large chars low-right (near)
- Color gradient: cool blue `(60,100,230)` → hot gold `(255,195,0)` reinforces depth
- Per-character 3D extrusion: depth proportional to font size, dark offset layers
- Per-character glow: large/hook chars get warm radial glow behind them
- Auto-scaling: if total width exceeds canvas, all sizes scale down proportionally

**10 visual layers (bottom to top):**
1. Background gradient (deep navy → black)
2. Top spotlight (crimson radial glow)
3. Perspective floor grid (vanishing point convergence)
4. Atmospheric glow orbs (red vs blue — conflict)
5. Per-character 3D title with depth extrusion
6. Floating shadow under title
7. Conflict diagonal slash
8. Tension subtitle
9. Perspective particles (far=small/dim, near=big/bright)
10. Side accent lines + bottom vignette

### Hook Quality Checklist (Self-Audit Before Output)

Before finalizing any Slide 1, answer ALL of these. If any answer is "No", the hook has failed:

| # | Question | Pass Criteria |
|---|---|---|
| 1 | Would a viewer scrolling at 2x speed still notice frame 0? | Visual punch is high-contrast and large enough |
| 2 | Can the hook title be read in under 1 second? | Title ≤ 8 characters or uses pattern recognition |
| 3 | Does the title create a "I need to know" feeling? | Uses one of the 12 hook patterns, not a description |
| 4 | Is there visible motion by 0.3s? | At least one element animating, not waiting |
| 5 | Does the subtitle deepen tension instead of explaining? | No definitions, no "is a", no topic description |
| 6 | Is the first TTS sentence a hook on its own? | Not "今天我们来了解", not a definition |
| 7 | Is the background NOT a plain gradient? | Has decorative elements at frame 0 |
| 8 | Does the cover withhold the answer? | Viewer must watch Slide 2+ to resolve curiosity |
| 9 | Is the layout asymmetric? | Not centered-everything with equal weight |
| 10 | Would this cover stand out in a feed of 20 similar videos? | Unique visual, not generic template look |

---

## Slide-Level Hook System (Adapted from Narrative Hook Adapter)

The 3-Second Hook Rule governs **Slide 1 only**. This section governs **all remaining slides** — ensuring every slide has a narrative function, every transition creates momentum, and the viewer never feels "this is the boring middle part."

### Tech-Adapted Hook Types

The narrative-hook-adapter defines six hook types (INFO, FATE, REL, TRUTH, TWIST, TIME). For science/tech video, adapt these:

| Hook Type | Code | Core Emotion | Example (Tech Video) |
|-----------|------|-------------|----------------------|
| Surprising Stat | STAT | Shock + exclusion | "Most people think JPEG is the best — it's not even close" |
| Counterintuitive | COUNTER | Cognitive dissonance | "Adding MORE data can make your model WORSE" |
| Hidden Mechanism | MYSTERY | Curiosity + discovery | "The real magic isn't in the algorithm — it's in what happens AFTER quantization" |
| Direct Challenge | CHALLENGE | Challenge + social proof | "Can you explain backpropagation in one sentence? 99% can't" |
| Result Reveal | RESULT | Surprise + payoff | "The result? +11.86 dB — without increasing file size" |
| Future Promise | PROMISE | Aspiration + efficiency | "And this is just v10. Wait until you see what's coming next" |

### Hook Lifecycle in Video Context

```
Hook Introduced (curiosity gap opens)
    ↓
Hook Developed (information builds, tension rises) ← content slides
    ↓
Hook Resolved
    ├── Full Result → viewer satisfied + new hook introduced
    └── Half-Result → suspense preserved + new hook → NEXT SLIDE
```

### Hook Density Rules (Per Video)

<HARD-GATE>
Every video with 5+ slides MUST satisfy ALL three density requirements. Videos with fewer than 5 slides must still satisfy the opening and closing hook requirements.
</HARD-GATE>

| Position | Requirement | Timing | Minimum |
|----------|-------------|--------|---------|
| **Opening Hook** | Slide 1 (covered by 3-Second Hook Rule) | 0-3s | 1 hook |
| **Mid-Escalation Hook** | A slide in the middle 40-60% range that raises stakes or reveals a twist | Middle slides | 1 hook per 4 slides |
| **Closing Hook** | Final slide ends with a forward-looking hook (PROMISE or MYSTERY) | Last slide | 1 hook |

**Mid-Escalation Hook Examples:**

| Situation | Mid-Hook Pattern | Implementation |
|-----------|-----------------|----------------|
| Performance benchmarks | "But here's what nobody expected..." | Reveal counterintuitive result |
| Architecture walkthrough | "This is where most implementations fail" | Show failure point before solution |
| Version evolution | "v9 was good. v10 broke everything — then fixed it better" | Contrast + turnaround |
| Comparison | "You might think Method A is better. The data says otherwise" | Challenge assumption |

### Hook Propagation Between Slides (Inter-Slide Hooks)

Slides are not isolated — they form a **hook propagation chain**:

```
Slide 1: Opening Hook A → Half-Result A + Hook B
Slide 2: Hook B (carries A's tension) → Full Result B + Hook C
Slide 3: Hook C → Half-Result C + Hook D
...
Slide N: Hook X → Full Result (payoff) + PROMISE hook (future/CTA)
```

**Inter-slide hook implementation:**

| Technique | How | Example |
|-----------|-----|---------|
| **Cliffhanger TTS** | End a slide's narration with an unfinished thought | "But the real breakthrough wasn't the architecture — it was..." (next slide reveals) |
| **Visual tease** | Show a blurred/obscured element that promises revelation next | Grayed-out chart with "the result will surprise you" |
| **Question carry** | Ask a question at end of slide, answer at start of next | "Why does 8b outperform 6b by such a huge margin?" → Next slide: quantization analysis |
| **Contrast setup** | Present "before" state, promise "after" in next slide | "This was v7's result..." → Next slide: "And this is v10" |

**BANNED inter-slide patterns:**
- "Next, let's look at..." (boring transition)
- "Moving on to..." (no tension)
- Any transition that feels like a PowerPoint deck, not a story

### Half-Result Hook Design (Between Slides)

Adapted from the narrative-hook-adapter's half-result patterns:

| Pattern | How It Works | Video Example |
|---------|-------------|---------------|
| **Answer half, ask more** | Resolve question A but reveal bigger question B | "We solved quality — but at what cost? The BPP is still too high..." |
| **False resolution** | Seemingly solved, but a trap | "v10 clean model hits 40 dB! ...But the robust model completely fails at 100 epochs" |
| **Cost resolution** | Solved but at a price | "Hybrid strategy works beautifully — but you need TWO models loaded simultaneously" |
| **Perspective flip** | Resolved from one angle, new crisis from another | "From the encoder's perspective, everything works. From the decoder's perspective..." |
| **Time lock** | Resolved but sets new constraint | "10b quantization works — but only if you can afford 44 BPP" |

---

## Three-Act Video Structure (起因→经过→结果)

<HARD-GATE>
Videos with 6+ slides MUST follow the three-act structure. The proportion is a guideline (±10% deviation allowed). What matters is that each act's PURPOSE is fulfilled.
</HARD-GATE>

Map the narrative-hook-adapter's 三段叙事 (setup-development-result) to video slide layout:

| Act | Proportion | Purpose | Slide Position | Hook Requirement |
|-----|-----------|---------|---------------|-----------------|
| **起因 (Setup)** | ~25% | Hook + problem + context | Slides 1-2 | Opening hook (Slide 1) + problem framing (Slide 2) |
| **经过 (Development)** | ~50% | Technical deep-dive + escalating complexity + mid-escalation hook | Slides 3 to N-2 | Mid-escalation hook at peak complexity slide |
| **结果 (Result)** | ~25% | Resolution + payoff + future hook | Last 1-2 slides | Closing PROMISE/MYSTERY hook |

### Act 1 — 起因 (Setup, ~25%)

**Slides 1-2** (or first ~25% of slides)

| Slide | Function | Content | Hook Role |
|-------|----------|---------|-----------|
| Slide 1 | Hook cover | Visual punch + hook title + tension subtitle | 3-Second Hook Rule (existing) |
| Slide 2 | Problem reveal | Answer the hook's question / reveal the problem / define scope | Resolve Slide 1 hook, plant Slide 3 curiosity |

**Narrative arc:** "Here's something surprising/challenging/important" → "Here's why it matters"

### Act 2 — 经过 (Development, ~50%)

**Middle ~50% of slides**

This is where the existing Mode 1/Mode 2 content generation shines — technical details, architecture, data, comparisons. But it must maintain narrative tension.

| Technique | Purpose | When to Use |
|-----------|---------|-------------|
| **Complexity escalation** | Each slide raises the technical bar | Architecture → Implementation → Quantization → Results |
| **Mid-escalation hook** | A surprise/twist at the 50-60% mark | "v10's robust model FAILED — but that failure led to the breakthrough" |
| **Tension-release rhythm** | Alternate dense data slides with visual payoff slides | Data chart → Result visualization → More data → Comparison |
| **Partial reveals** | Don't show the full picture until Act 3 | Show components individually, combine in the result |

**Development slide ordering principles:**
1. Start with what the viewer understands (familiar concepts)
2. Build toward what they don't (new innovation)
3. Insert the mid-escalation hook when complexity peaks
4. End Act 2 with a setup for the Act 3 payoff

### Act 3 — 结果 (Result, ~25%)

**Last 1-2 slides** (or final ~25%)

| Slide | Function | Content | Hook Role |
|-------|----------|---------|-----------|
| N-1 | Payoff | Best results / summary / "the answer" | Full resolution of all major hooks |
| N | Forward hook | Recommendations / future directions / CTA | Closing PROMISE or MYSTERY hook |

**Narrative arc:** "And here's what we achieved" → "And here's what's coming next"

**Result slide MUST:**
1. Pay off the opening hook's promise (if Slide 1 asked a question, answer it here)
2. Show the "after" to contrast with Slide 2's "before"
3. End with a forward-looking hook (PROMISE: "next version will...", or MYSTERY: "but one question remains...")

---

## Storyboard Animation Planning (分镜→动画映射)

Adapt the narrative-hook-adapter's shot/camera concepts to HTML animation direction. Before writing HTML, plan each slide's "virtual camera" to guide animation choices.

### Shot Size → Animation Scale Mapping

| Shot Size | Abbreviation | HTML Animation Equivalent | Emotional Effect | When to Use |
|-----------|-------------|--------------------------|-----------------|-------------|
| Extreme Long Shot | ELS | Full-page entrance, elements tiny/subtle | Scale, context | Environment setup, data overview |
| Long Shot | LS | Container-level entrance, all elements visible | Establishing | Slide intro, layout reveal |
| Medium Shot | MS | Group entrance (cards, sections) | Conversational | Comparisons, feature lists |
| Medium Close-Up | MCU | Single element entrance with detail | Focused attention | Key metric, important statement |
| Close-Up | CU | Large single element (oversized text, icon) | Emphasis | Hook statement, critical number |
| Extreme Close-Up | ECU | Single character/number at 120-200px | Maximum emphasis | Hook number, shocking stat |

### Camera Movement → CSS/GSAP Animation Mapping

| Camera Move | HTML Animation | Easing | Emotional Effect | When to Use |
|------------|---------------|--------|-----------------|-------------|
| Fixed (固定) | `opacity: 0→1` fade | `power2.out` | Stable, objective | Data display, calm narration |
| Push in (推) | `scale(0.7)→scale(1)` + `opacity` | `expo.out` | Focus, tension | Key revelation, important detail |
| Pull out (拉) | `scale(1.2)→scale(1)` + `opacity` | `power2.out` | Reveal, context | Showing full picture after detail |
| Pan (摇) | `translateX(±80px)→0` + `opacity` | `power3.out` | Directional flow | Process flow, comparison |
| Tilt (俯摇) | `translateY(±80px)→0` + `opacity` | `power3.out` | Vertical hierarchy | Hierarchies, layer stacks |
| Tracking (跟) | `translateX/Y` stagger | `power2.out` with stagger | Dynamic, sequential | Step-by-step processes |
| Quick push (急推) | `scale(0.3)→scale(1.05)→scale(1)` | `back.out(1.5)` | Shock, emphasis | Mid-escalation hook, surprise reveal |
| Quick pull (急拉) | `scale(1.5)→scale(1)` | `expo.out` | Reveal after tension | Result reveal, "the answer is..." |
| Handheld (手持) | `rotation(±2deg)` subtle oscillation | `sine.inOut` loop | Urgency, realism | Problem slides, warning content |

### Per-Act Animation Rhythm

| Act | Dominant Camera | Animation Speed | Easing Character | Reason |
|-----|----------------|----------------|-----------------|--------|
| Act 1 (Setup) | Push in, Quick push | Fast (0.15-0.35s) | `back.out`, `expo.out` | Grab attention, create urgency |
| Act 2 (Development) | Mixed, Tracking | Medium (0.3-0.6s) | `power2.out`, `power3.out` | Build understanding, maintain flow |
| Act 3 (Result) | Pull out, Fixed | Slow (0.5-1.0s) | `power1.out`, `sine.out` | Resolution, satisfaction, calm |

### Storyboard Planning Template

Before generating HTML, complete this per-slide plan:

| Slide | Act | Shot Size | Camera Move | Hook Type | Animation Notes |
|-------|-----|-----------|-------------|-----------|-----------------|
| 1 | 起因 | CU→LS | Quick push + pull | STAT | Oversized number hooks, then reveal full layout |
| 2 | 起因 | MS | Fixed + tracking | CHALLENGE | Cards stagger in, problem framing |
| 3 | 经过 | LS | Pan | MYSTERY | Architecture flow left→right |
| 4 | 经过 | MCU→CU | Push in | COUNTER | Mid-hook: counterintuitive result |
| 5 | 经过 | MS | Tracking | RESULT | Data comparison stagger |
| N-1 | 结果 | CU→ELS | Quick pull | RESULT | Big number then full picture |
| N | 结果 | MCU | Fixed | PROMISE | Calm summary, forward-looking |

---

## TTS Narration Script Design (Enhanced)

### Per-Slide VO Structure

Each slide's TTS narration should follow a micro three-act structure:

| VO Section | Proportion | Purpose | Example |
|-----------|-----------|---------|---------|
| **Bridge** | ~20% | Connect to previous slide / maintain continuity | "But here's what makes v10 different..." |
| **Core content** | ~60% | Deliver the slide's information | "The ResBlock encoder uses 4 residual blocks with learnable scaling..." |
| **Hook forward** | ~20% | Plant curiosity for the next slide | "And the results? Let me show you something that surprised even us." |

### Inter-Slide VO Bridge Patterns

| Pattern | Usage | Example |
|---------|-------|---------|
| **Question bridge** | Ask a question at end of slide, answer in next | "So how much does this actually improve? [next slide: +11.86 dB]" |
| **Contrast bridge** | Set up a contrast resolved in next slide | "v9 got us to +8 dB. But we wanted more. [next: v10 results]" |
| **Suspense bridge** | Hint at a surprising reveal | "And then we tried something that shouldn't have worked. [next: hybrid strategy]" |
| **Definition bridge** | Define a concept needed for next slide | "This is what we call hybrid inference. Here's why it matters. [next: dual-model details]" |

### VO Hook Language Rules

<HARD-GATE>
These rules apply to ALL slides' TTS narration, not just Slide 1.
</HARD-GATE>

| Rule | BANNED Pattern | Required Pattern |
|------|---------------|-----------------|
| First sentence hooks | "接下来我们看..." / "这一页介绍..." | Use a bridge from previous slide or a micro-hook |
| Last sentence teases | "以上就是..." / "总结一下..." | End with a forward-looking question or promise |
| No dead transitions | "好的" / "那么" as sentence starters | Cut filler words, start with content |
| Emotional variety | Flat monologue throughout all slides | Alternate: excitement (results) → calm explanation (architecture) → tension (problems) → payoff (resolution) |

### VO Emotional Curve

| Slide Position | VO Emotion | Speaking Style | Example Tone |
|---------------|-----------|---------------|-------------|
| Slide 1 (Hook) | High energy, urgency | Fast, punchy, dramatic | "95% of approaches FAIL at this step!" |
| Slide 2 (Problem) | Serious, weighty | Measured, emphatic | "Traditional codecs cap out at just 28.76 dB..." |
| Act 2 slides | Varies with content | Technical but engaged | Clear explanation with moments of surprise |
| Mid-hook slide | Excited, dramatic | Speed up, emphasis | "But here's what NOBODY expected..." |
| Result slide | Triumphant, satisfied | Proud, confident | "40.62 dB. That's nearly 12 dB better than baseline." |
| Final slide | Forward-looking, inspiring | Calm but energized | "And this is just the beginning..." |

---

## Scene Transitions (Non-Negotiable)

Every multi-slide page MUST follow ALL of these rules:

1. **ALWAYS use transitions between slides.** No jump cuts. No exceptions.
2. **ALWAYS use entrance animations on every slide.** Every element animates IN via `gsap.from()` or CSS `@keyframes`. No element may appear fully-formed. If a slide has 5 elements, it needs 5 entrance animations.
3. **NEVER use exit animations** except on the final slide. No `gsap.to()` that animates opacity to 0, y offscreen, scale to 0, or any other "out" animation before a transition fires. The transition IS the exit. The outgoing slide's content MUST be fully visible at the moment the transition starts.
4. **Final slide only:** The last slide may fade elements out (e.g., fade to black). This is the ONLY slide where `gsap.to(..., { opacity: 0 })` is allowed.
5. **Hook → Slide 2 transition:** Use the most distinctive/energetic transition of the entire video here. This is the moment the viewer decides to keep watching. Recommended: zoom through, glitch, or light leak (0.15-0.3s, `power4` or `expo`). See [references/transitions.md](references/transitions.md) for the full transition catalog and implementation code.

---

## Animation Guardrails

- Offset first animation 0.1-0.3s (not t=0). Zero-delay feels like a jump cut.
- Vary eases across entrance tweens — use at least 3 different eases per scene
- Don't repeat an entrance pattern within a scene
- Avoid full-screen linear gradients on dark backgrounds (H.264 banding — use radial or solid + localized glow)
- 60px+ headlines, 20px+ body, 16px+ data labels for rendered video
- `font-variant-numeric: tabular-nums` on number columns

When no visual style is provided, follow [house-style.md](house-style.md) for aesthetic defaults.

---

## Do Not

1. Do not skip the animation reset JS — it is the only reliable cross-browser fix (CSS mode)
2. Do not use `animation-fill-mode: forwards` without the cloneNode reset
3. Do not generate video without first verifying the HTML renders correctly
4. Do not use moviepy `CompositeVideoClip` for large resolutions — use ffmpeg directly
5. Do not call `sync_playwright()` inside an asyncio event loop — use `run_in_executor`
6. Do not use `repeat: -1` in CSS animations — calculate exact repeats from duration
7. Do not include Chinese characters in ffmpeg concat file paths without using forward slashes
8. Do not pair two sans-serif fonts — cross the boundary: serif + sans, or sans + mono
9. Do not use the same ease/direction/speed on every element — vary deliberately
10. Do not animate layout properties (width/height/top/left) when transforms suffice
11. Do not use `<br>` in content text — forced line breaks don't account for rendered font width. Use `max-width` instead
12. Do not use gradient text (`background-clip: text`) or cyan-on-dark as default — these are AI design tells
13. Do not run TTS without per-file timeout — always use `asyncio.wait_for()` to prevent a single hung TTS call from stalling the entire pipeline
14. Do not compose video from user images without verifying naming convention and completeness — always check `scene_NNN_*` pattern before running ffmpeg
15. Do not generate image prompts without first completing the script design JSON — prompts derive from scene descriptions, not the other way around
16. Do not proceed to Phase B (video composition) until the user explicitly confirms their images are ready — the human-in-the-loop step is mandatory in Mode 3
17. Do not create a flat middle section — every video with 5+ slides must have a mid-escalation hook (STAT, COUNTER, MYSTERY, or CHALLENGE) at the 40-60% mark
18. Do not use dead transition phrases in TTS — banned: "接下来我们看", "好的那么", "以上就是", "下面介绍"
19. Do not let all slides have the same animation speed — Act 1 must be faster than Act 3
20. Do not end a slide (except the last) without planting a hook forward to the next slide

---

## Real-World Example (OSI Seven-Layer Model)

**User input:** A paragraph explaining the OSI seven-layer network model.

**Execution:**
1. Mode 1, Step 1a → Derive hook title: "7层，3次崩溃" with subtitle "OSI 模型背后的血泪史", oversized "7" visual
2. Mode 1, Step 1b → Generate PPT prompt with hook-cover instruction
3. Mode 1, Step 2 → model generates complete HTML (13 slides, slide 1 = hook cover, slide 2 = intro/definition)
4. Mode 1, Step 3 → restructure with Level2 PPT template (e.g., `3-2.html` for flowchart-style layers), preserving hook cover title
5. User says "generate flowchart" → Mode 2 restructures to flat UI with `RNN-3.html` style
6. User says "generate video" → `html2video.py` produces MP4 with TTS narration

**Hook cover example (Slide 1):**
- Background: dark gradient with oversized faded "7" at 5% opacity
- Title (hook): "7层，3次崩溃" at 120px, accent color, `back.out(1.5)` scale pop at 0.05s
- Subtitle: "OSI 模型背后的血泪史" at 32px, `expo.out` at 0.15s
- Accent line: "99% 的程序员解释不清楚" at 20px, `power3.out` at 0.3s
- Ambient: glow pulse starting at 0.5s
- Frame capture: 6 frames @ [0.1, 0.3, 0.5, 1.0, 2.0, 3.5]

**Outputs:**
- HTML (PPT mode): Hook cover + 12-page carousel with definition, overview, 7-layer details, protocol comparison
- HTML (flowchart mode): Horizontal 7-layer flow cards, deep green flat UI
- MP4: Video with narration and subtitles, hook cover grabs attention in first 3 seconds

---

## Animation Engine Options

### Option A: CSS Animation (Default, Built-In)

All existing templates use pure CSS `@keyframes` + Canvas particles. Requires the cloneNode animation reset JS. Simpler, no external dependencies.

### Option B: GSAP Timeline (Advanced)

For more complex animation choreography, transitions, and deterministic control, use GSAP. Read `references/gsap-reference.md` for the full API.

**GSAP advantages:**
- Deterministic `tl.restart()` replaces cloneNode hack
- Timeline labels and position parameter for precise sequencing
- Built-in easing library (`power1`-`power4`, `back`, `elastic`, `expo`)
- Stagger, TextPlugin (typewriter), and function-based values

**When to use GSAP:**
- Multi-scene compositions with transitions (`references/transitions.md`)
- Per-word caption animation (`references/captions.md`)
- Audio-reactive animations (`references/audio-reactive.md`)
- Complex choreography with staggered entrances (`references/motion-principles.md`)

**Setup:**
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>gsap.registerPlugin(TextPlugin);</script>
```

**GSAP Rules:**
- All timelines start `{ paused: true }` — the player/script controls playback
- Register every timeline: `window.__timelines["<id>"] = tl`
- Never animate `visibility`, `display`, or call `video.play()`/`audio.play()`
- Never animate the same property on the same element from multiple timelines simultaneously
- Never use `repeat: -1` — calculate exact repeats: `repeat: Math.ceil(duration / cycleDuration) - 1`
- Build timelines synchronously — never inside `async`/`await`, `setTimeout`, or Promises
- Never use `gsap.set()` on elements that don't exist yet — use `tl.set(selector, vars, timePosition)` at or after the element's start time instead

---

## Quality Assurance

Before finalizing HTML or generating video, run these audit scripts:

### Animation Map — Detect issues in animated HTML

```bash
python scripts/animation-map.py input.html
```

Checks: offscreen elements, collisions, invisible animations, missing animation reset, emoji residue, empty GSAP timelines. Outputs `_animation-map.json`.

### Contrast Report — WCAG accessibility audit

```bash
python scripts/contrast-report.py input.html
```

Checks: text contrast ratios against WCAG AA (4.5:1 normal, 3:1 large) and AAA standards. Outputs `_contrast-report.json`.

If warnings appear:
- On dark backgrounds: brighten the failing color until it clears 4.5:1 (normal text) or 3:1 (large text, 24px+ or 19px+ bold)
- On light backgrounds: darken it
- Stay within the palette family — don't invent a new color, adjust the existing one
- Re-run until clean

### Audio Data Extraction — For audio-reactive animations

```bash
python scripts/extract-audio-data.py audio.mp3 -o audio-data.json --bands 16
```

Extracts per-frame RMS amplitude and frequency bands. Used with GSAP timeline for audio-driven visuals. See `references/audio-reactive.md`.

---

## Typography and Assets

- **Fonts:** Add `crossorigin="anonymous"` to external media. The video pipeline handles font embedding.
- **Text overflow prevention:** Use `max-width` on text containers so content wraps naturally. Never use `<br>` for layout breaks — let CSS handle wrapping.
- All files live at the project root alongside the HTML file; sub-compositions use `../`

---

## Editing Existing Compositions

- Read the full composition first — match existing fonts, colors, animation patterns
- Only change what was requested
- Preserve timing of unrelated elements

---

## Output Checklist

### Hook Verification (Slide 1 — Must ALL pass)

- [ ] **Cover title (Slide 1) is a hook** — uses one of the 12 hook patterns, NOT "XXX详解"
- [ ] **Cover subtitle creates tension** — deepens curiosity gap, NOT a plain topic description
- [ ] **Cover has visual punch at frame 0** — oversized number, dramatic icon, split screen, or extreme contrast (no empty/gradient-only first frame)
- [ ] **Cover animation completes within 1.0s** — first element at ≤0.15s, all visible by ≤1.0s
- [ ] **Visible motion by 0.3s** — at least one element animating, not waiting for 0.5s+
- [ ] **Layout is asymmetric** — hook title pinned to corner/edge, not centered-everything
- [ ] **Background has decorative elements at frame 0** — no plain solid or simple gradient
- [ ] **First TTS sentence is an audio hook** — NOT "今天我们来了解" or any definition/preamble
- [ ] **Cover withholds the answer** — viewer must watch Slide 2+ to resolve curiosity
- [ ] **Hook video title generated** — `_title.txt` with compelling publish caption (max 30 chars, first 10 chars contain hook)
- [ ] **Cover thumbnail extracted** — `_cover.png` with best hook frame from Slide 1

### Narrative Hook Verification (All Slides — for videos with 5+ slides)

- [ ] **Opening hook present** — Slide 1 satisfies 3-Second Hook Rule (above)
- [ ] **Mid-escalation hook present** — at least one slide in the 40-60% range raises stakes with STAT, COUNTER, MYSTERY, or CHALLENGE hook
- [ ] **Closing hook present** — final slide ends with PROMISE or MYSTERY hook (forward-looking)
- [ ] **Hook propagation chain intact** — each slide (except last) plants curiosity for the next slide via bridge, tease, or half-result
- [ ] **No dead transitions** — no slide starts with "接下来我们看" or ends with "以上就是"
- [ ] **Three-act structure followed** — slides organized into 起因(~25%) → 经过(~50%) → 结果(~25%)

### TTS Narration Quality

- [ ] **Per-slide VO has bridge** — each slide (except Slide 1) starts with a connection to previous slide
- [ ] **Per-slide VO has hook forward** — each slide (except last) ends with curiosity-gap sentence
- [ ] **VO emotional curve varies** — not flat monologue; alternates excitement/calm/tension/payoff
- [ ] **No banned VO patterns** — no "接下来", "好的", "那么", "以上就是" as transitions

### Storyboard Consistency

- [ ] **Animation speed matches act** — Act 1 fast (0.15-0.35s), Act 2 medium (0.3-0.6s), Act 3 slow (0.5-1.0s)
- [ ] **Hook slides use emphasis animations** — quick push, quick pull, or scale pop for hook reveals
- [ ] **At least 3 different easing functions** across the entire video

### Technical Quality (All Slides)

- [ ] `animation-map.py` passes, or every reported issue is intentional
- [ ] `contrast-report.py` passes, or warnings are addressed
- [ ] No emoji residue in generated HTML
- [ ] Animation reset JS present and correct
- [ ] All slides have entrance animations (no fully-formed elements)
- [ ] Transitions between all slides (no jump cuts)
- [ ] Exit animations only on final slide
- [ ] Slide 1 → Slide 2 transition is the most energetic transition of the video

---

## References (Loaded on Demand)

Read these files when the corresponding situation arises:

### Core Workflow

| File | Read When |
|---|---|
| `references/template-selection.md` | Selecting a PPT or Animation template (Step 3 / Mode 2 Step 1) |
| `references/prompt-templates.md` | Generating HTML or restructuring content (all steps, all modes including Mode 3 prompts) |
| `references/video-pipeline.md` | User requests video export; need full parameter docs or pipeline details |
| `references/semi-auto-workflow.md` | User wants Mode 3 (semi-auto); detailed workflow, image prompt guidelines, JSON schema, CLI reference |
| `references/troubleshooting.md` | Encountering issues with animation, TTS, ffmpeg, encoding, or screenshots |
| `references/tts.md` | Generating narration with Edge TTS; voice selection, speed tuning, multilingual support |
| `references/transcript-guide.md` | Transcribing audio/video for captions; model selection, quality checks |

### Visual Design

| File | Read When |
|---|---|
| `house-style.md` | Generating HTML without a user-specified visual style |
| `visual-styles.md` | User wants a specific visual style or content fits a named identity (including Shadow Cut tier selection) |
| `references/typography.md` | Choosing fonts, sizing text for video, Chinese font pairing, font discovery |
| `references/icons.md` | Selecting icons, replacing emoji, configuring icon libraries (Font Awesome, Remix Icon, Lucide, Tabler, IconPark, Phosphor, etc.) |
| `references/cultivation-icons.md` | Generating cultivation/xianxia/wuxia/fantasy themed content — run `python scripts/download-icons.py --category element` first |
| `references/themed-icons.md` | Generating science/tech themed content (chemistry, biology, hardware, energy, finance, weather, industry) — run `python scripts/download-icons.py --category chemistry` first |
| `patterns.md` | Structuring slide layouts (VS card, step flow, dashboard, architecture, quote, timeline) |

### Animation & Motion

| File | Read When |
|---|---|
| `references/gsap-reference.md` | Using GSAP instead of CSS animations; tween methods, timelines, easing, effects |
| `references/transitions.md` | Building transitions between slides (crossfade, push, blur, zoom, blocks, etc.) |
| `references/motion-principles.md` | Designing animation choreography; easing = emotion, build/breathe/resolve scene structure |
| `references/captions.md` | Advanced per-word subtitle animation, karaoke highlight, caption styling |
| `references/dynamic-techniques.md` | Dynamic caption animation techniques (karaoke, clip-path, slam, scatter, elastic, 3D) |
| `references/css-patterns.md` | Text marker effects (highlight, circle, burst, scribble, sketchout) |
| `references/text-animations.md` | Animated text for titles, hooks, section headers (typewriter, glitch, wave, stroke-draw, neon, bounce, split reveal) — prompt templates and effect selection by theme |
| `references/audio-reactive.md` | Animations driven by audio data (bass → scale, treble → shimmer) |

### Palettes

| File | Read When |
|---|---|
| `palettes/bold-energetic.md` | High-energy content: launches, social media |
| `palettes/clean-corporate.md` | Professional content: explainers, tutorials |
| `palettes/dark-premium.md` | Cinematic content: tech, finance, luxury |
| `palettes/jewel-rich.md` | High-end content: events, sophisticated |
| `palettes/monochrome.md` | Dramatic content: typography-focused, serious |
| `palettes/nature-earth.md` | Organic content: sustainability, wellness |
| `palettes/neon-electric.md` | Gaming, nightlife, Gen Z |
| `palettes/pastel-soft.md` | Lifestyle content: beauty, wellness |
| `palettes/shadow-cut.md` | Shadow Cut: dark/epic/dramatic — cinematic dark-mode with theme-based tier selection |
| `palettes/warm-editorial.md` | Narrative content: storytelling, documentaries |

### Template Metadata

| File | Read When |
|---|---|
| `assets/templates/PPT Template-level2/SUMMARY.md` | Selecting a Level2 PPT template (25 templates with detailed metadata) |
| `assets/templates/Animation/SUMMARY.md` | Selecting an Animation template (14 templates with detailed metadata) |

---

## Parameter Quick Reference

| Parameter | Default | Description |
|---|---|---|
| PPT template | AI-selected from Level2 | Mode 1 restructure template |
| Animation template | `assets/templates/Animation/RNN-3.html` | Mode 2 restructure template |
| Output HTML | `/home/mt/桌面/AI_Animation.html` | Generated HTML file |
| Output video | Same dir as HTML, `_video.mp4` | Generated MP4 file |
| Hook video title | Same dir, `_title.txt` | Hook publish title for social media |
| Cover thumbnail | Same dir, `_cover.png` | Cover frame image for video platform |
| Video resolution | 1080×1920 (9:16 portrait) | Adjustable via `--width` / `--height` |
| Video FPS | 24 | Adjustable via `--fps` |
| TTS voice | `zh-CN-YunxiNeural` (Yunxi male) | Any Edge TTS voice |
| Frames per slide | 5 @ 0.5s/1.5s/2.5s/3.5s/4.5s | Slides 2+. **Slide 1 uses 6 frames @ 0.1s/0.3s/0.5s/1.0s/2.0s/3.5s** for hook impact |
| Silent mode | `--no-voice` | Skip TTS, export video without audio |
| Script export | `--export-script` | Export narration text file, no video |
| TTS timeout | `--tts-timeout 60` | Per-file TTS timeout (seconds) |
| TTS retries | `--tts-retries 2` | Max retries per TTS file |
| TTS cache | `--tts-cache` | Enable disk cache for TTS reuse |
| Animation reset | Built into templates | cloneNode fix for CSS animation replay |
| **Mode 3: Semi-Auto** | | |
| `--script-only` | (off) | Mode 3: Generate TTS from `_script_design.json` only, no HTML needed |
| `--script` | (none) | Path to `_script_design.json` for Mode 3 video composition |
| `--images-dir` | (none) | Directory with user-generated images (auto-discovered by `scene_NNN_*` pattern) |
| `--images-map` | (none) | JSON file mapping scene index → explicit image path (overrides `--images-dir`) |
| `--tts-dir` | (none) | Directory with pre-generated TTS audio (from Step 2). If omitted, TTS is regenerated |
