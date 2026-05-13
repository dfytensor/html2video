# Captions & Subtitles

Read this file when the user requests video export with subtitles, or wants advanced caption styling.

---

## Language Rule (Non-Negotiable)

If using whisper-based transcription, **never use `.en` models unless the user explicitly states the audio is English.** `.en` models TRANSLATE non-English audio into English instead of transcribing it.

1. User says the language → use multilingual model with `--language <code>`
2. User says English → use `.en` model
3. Language unknown → use multilingual model without `--language` — auto-detects

---

## Default Subtitle System (html2video.py)

The built-in `scripts/html2video.py` generates fixed subtitle bars:
- 120px semi-transparent black bar at bottom
- 36px white text, auto-wrapped
- Font: Microsoft YaHei (Windows) / WenQuanYi Micro Hei (Linux)

This works for most use cases. See `references/video-pipeline.md` for parameters.

---

## Advanced Caption System (GSAP + HTML)

For custom caption styling beyond the built-in system, generate captions directly in the HTML with GSAP timelines.

### Transcript Source

```json
[
  { "text": "Hello", "start": 0.0, "end": 0.5 },
  { "text": "world.", "start": 0.6, "end": 1.2 }
]
```

For transcription commands, see [transcript-guide.md](transcript-guide.md).

### Style Detection (When No Style Specified)

Read the full transcript before choosing. Four dimensions:

**1. Visual feel** — corporate→clean; energetic→bold; storytelling→elegant; technical→precise; social→playful.

**2. Color palette** — dark+bright for energy; muted for professional; high contrast for clarity; one accent color.

**3. Font mood** — heavy/condensed for impact; clean sans for modern; rounded for friendly; serif for elegance.

**4. Animation character** — scale-pop for punchy; gentle fade for calm; word-by-word for emphasis; typewriter for technical.

### Per-Word Styling

Scan for words deserving distinct treatment:

- **Brand/product names** — larger size, unique color
- **ALL CAPS** — scale boost, flash, accent color
- **Numbers/statistics** — bold weight, accent color
- **Emotional keywords** — exaggerated animation (overshoot, bounce)
- **Call-to-action** — highlight, underline, color pop
- **Marker highlight** — for beyond-color emphasis, see [css-patterns.md](css-patterns.md)

### Script-to-Style Mapping

| Tone         | Font mood                | Animation                          | Color                       | Size    |
| ------------ | ------------------------ | ---------------------------------- | --------------------------- | ------- |
| Hype/launch  | Heavy condensed, 800-900 | Scale-pop, back.out(1.7), 0.1-0.2s | Bright on dark              | 72-96px |
| Corporate    | Clean sans, 600-700      | Fade+slide, power3.out, 0.3s       | White/neutral, muted accent | 56-72px |
| Tutorial     | Mono/clean sans, 500-600 | Typewriter/fade, 0.4-0.5s          | High contrast, minimal      | 48-64px |
| Storytelling | Serif/elegant, 400-500   | Slow fade, power2.out, 0.5-0.6s    | Warm muted tones            | 44-56px |
| Social       | Rounded sans, 700-800    | Bounce, elastic.out, word-by-word  | Playful, colored pills      | 56-80px |

### Word Grouping

- **High energy:** 2-3 words. Quick turnover.
- **Conversational:** 3-5 words. Natural phrases.
- **Measured/calm:** 4-6 words. Longer groups.

Break on sentence boundaries, 150ms+ pauses, or max word count.

### Caption Structure

```html
<div class="caption-container">
  <div class="caption-group" id="cg-0">
    <span class="caption-word">Hello</span>
    <span class="caption-word accent">world</span>
  </div>
</div>
```

```css
.caption-container {
  position: absolute;
  bottom: 80px;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 50;
}
.caption-group {
  display: inline-flex;
  gap: 8px;
}
.caption-word {
  font-size: 64px;
  font-weight: 800;
  color: #fff;
}
.caption-word.accent {
  color: #FFBE0B;
  font-size: 72px;
}
```

### GSAP Timeline Caption Animation

```javascript
var tl = gsap.timeline({ paused: true });

var groups = [
  { text: "Hello world", start: 0.0, end: 1.5 },
  { text: "This is AI", start: 1.6, end: 3.0 },
];

groups.forEach(function(group, gi) {
  var el = document.getElementById("cg-" + gi);

  // Entrance
  tl.from(el, {
    opacity: 0,
    y: 20,
    duration: 0.2,
    ease: "power2.out"
  }, group.start);

  // Hard kill at end (non-negotiable)
  tl.to(el, {
    opacity: 0,
    scale: 0.95,
    duration: 0.12,
    ease: "power2.in"
  }, group.end - 0.12);
  tl.set(el, {
    opacity: 0,
    visibility: "hidden"
  }, group.end);
});

window.__timelines["captions"] = tl;
```

### Caption Exit Guarantee

Every group **must** have a hard kill after exit animation:

```js
tl.to(groupEl, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, group.end - 0.12);
tl.set(groupEl, { opacity: 0, visibility: "hidden" }, group.end);
```

Self-lint after building timeline — place **before** `window.__timelines[id] = tl`:

```js
groups.forEach(function (group, gi) {
  var el = document.getElementById("cg-" + gi);
  if (!el) return;
  tl.seek(group.end + 0.01);
  var computed = window.getComputedStyle(el);
  if (computed.opacity !== "0" && computed.visibility !== "hidden") {
    console.warn(
      "[caption-lint] group " + gi + " still visible at t=" + (group.end + 0.01).toFixed(2) + "s"
    );
  }
});
tl.seek(0);
```

---

## Karaoke Highlight Effect

```html
<div class="caption-group" id="cg-0">
  <span class="karaoke-word" data-text="Hello">Hello</span>
  <span class="karaoke-word" data-text="World">World</span>
</div>
```

```css
.karaoke-word {
  position: relative;
  display: inline-block;
  color: rgba(255,255,255,0.3);
}
.karaoke-word::after {
  content: attr(data-text);
  position: absolute;
  left: 0; top: 0;
  color: #FFBE0B;
  clip-path: inset(0 100% 0 0);
}
```

```javascript
tl.to("#cg-0 .karaoke-word:nth-child(1)::after", {
  clipPath: "inset(0 0% 0 0)",
  duration: 0.5,
  ease: "none"
}, 0.0);
```

---

## Positioning

- **Landscape (1920x1080):** Bottom 80-120px, centered
- **Portrait (1080x1920):** Lower middle ~600-700px from bottom, centered
- **Square (1080x1080):** Bottom 60-80px, centered

Never cover the subject's face. Use `position: absolute`. One caption group visible at a time.

**Container pattern:** Full-width absolute container, centered. Do **not** use `left: 50%; transform: translateX(-50%)` — causes clipping at composition edges.

---

## Text Overflow Prevention

```css
.caption-group {
  max-width: 90%;
  overflow: visible; /* NOT hidden — clips scaled emphasis words */
  position: absolute;
}
```

For auto-sizing, use iterative shrink:
```javascript
function fitText(el, maxWidth, baseSize, minSize) {
  var size = baseSize;
  el.style.fontSize = size + "px";
  while (el.scrollWidth > maxWidth && size > minSize) {
    size -= 2;
    el.style.fontSize = size + "px";
  }
}
```

When per-word styling uses `scale > 1.0`, compute `maxWidth = safeWidth / maxScale` to leave headroom.

---

## Further References

- [dynamic-techniques.md](dynamic-techniques.md) — karaoke, clip-path reveals, slam words, scatter exits, elastic, 3D rotation
- [transcript-guide.md](transcript-guide.md) — transcription commands, whisper models, quality checks
- [css-patterns.md](css-patterns.md) — CSS+GSAP marker highlighting (deterministic, fully seekable)

---

## Constraints

- Deterministic — no `Math.random()`, no `Date.now()`
- Sync to transcript timestamps
- One group visible at a time
- Every group must have a hard `tl.set` kill at `group.end`
- Minimum readable size: 42px for video
