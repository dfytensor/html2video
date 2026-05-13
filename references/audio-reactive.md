# Audio-Reactive Animation

Read this file when creating animations that respond to audio data — for example, syncing canvas particles to narration or creating music-driven visuals.

---

## Audio Data Extraction

Use `scripts/extract-audio-data.py` to pre-extract per-frame amplitude and frequency data from audio/video files:

```bash
python scripts/extract-audio-data.py audio.mp3 -o audio-data.json
python scripts/extract-audio-data.py video.mp4 --fps 30 --bands 16 -o audio-data.json
```

### Data Format

```json
{
  "fps": 30,
  "totalFrames": 5415,
  "frames": [
    { "time": 0.0, "rms": 0.42, "bands": [0.8, 0.6, 0.3, 0.1, ...] }
  ]
}
```

- **rms** (0-1): overall loudness, normalized across track
- **bands[]** (0-1): frequency magnitudes. Index 0 = bass, higher = treble

### Band Count Guide

| Bands | Detail | Good for |
|---|---|---|
| 4 | Low | Background glow, pulsing |
| 8 | Medium | Bar charts, basic spectrum |
| 16 | High | Detailed EQ (default) |
| 32 | Very high | Dense radial layouts |

---

## Loading Audio Data

```javascript
// Option A: inline (small files, under ~500KB)
var AUDIO_DATA = { /* paste audio-data.json contents */ };

// Option B: sync XHR (large files — MUST be synchronous)
var xhr = new XMLHttpRequest();
xhr.open("GET", "audio-data.json", false);
xhr.send();
var AUDIO_DATA = JSON.parse(xhr.responseText);
```

**Do NOT use async `fetch()`.** The timeline must be fully constructed synchronously.

---

## Mapping Audio to Visuals

| Audio Property | Visual Mapping | Example |
|---|---|---|
| Bass (bands[0-2]) | Scale, glow, position shifts | `gsap.to(el, { scale: 1 + frame.bands[0] * 0.3 })` |
| Treble (bands[8+]) | Shimmer, flicker, edge effects | `gsap.to(el, { borderColor: frame.bands[10] > 0.5 ? accent : muted })` |
| RMS | Background brightness, overall energy | `canvas.style.opacity = 0.3 + frame.rms * 0.7` |

Any GSAP-tweenable property works — `clipPath`, `filter`, SVG attributes, CSS custom properties.

**Pick 2-3 properties to animate.** More looks noisy.

---

## Content, Not Medium

Audio provides **timing and intensity**. The visual vocabulary comes from the narrative.

**Never add:** equalizer bars, spectrum analyzers, waveform displays, musical notes clip art, generic particle systems, rainbow color cycling, strobing white on beats, abstract pulsing orbs.

**Instead:** Let content guide the visual and audio drive its behavior. Bass makes warmth _swell_. Treble sharpens _contrast_. The visual choice comes from "what does this piece feel like?"

---

## Sampling Pattern

Audio reactivity requires per-frame sampling via a `for` loop with `tl.call()`, not a single tween:

```js
// Correct — sample every frame
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        draw(frame);
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}

// Wrong — single tween, doesn't react to audio
gsap.to(".el", { scale: 1.2, duration: totalDuration });
```

Without per-frame sampling, the composition doesn't actually react to audio.

---

## textShadow Gotcha

`textShadow` on a parent container with semi-transparent children (e.g., inactive caption words at `rgba(255,255,255,0.3)`) renders a visible glow rectangle behind all children. Fix: apply `scale` to the container for beat pulse, but apply `textShadow` to individual active words only.

---

## Canvas 2D Rendering (Most Common)

```javascript
var canvas = document.getElementById("visualizer");
var ctx = canvas.getContext("2d");

for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(function(frameIdx) {
    var frame = AUDIO_DATA.frames[frameIdx];
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var barW = canvas.width / frame.bands.length;
    frame.bands.forEach(function(band, i) {
      var h = band * canvas.height * 0.8;
      ctx.fillStyle = "rgba(76, 175, 80, " + (0.3 + band * 0.7) + ")";
      ctx.fillRect(i * barW, canvas.height - h, barW - 2, h);
    });
  }, [f], f / AUDIO_DATA.fps);
}
```

---

## Smoothing

Raw audio data is jittery. Apply exponential smoothing:

```javascript
var prev = null;
var smoothing = 0.25; // 0.1-0.2 snappy, 0.3-0.5 flowing

function smooth(f) {
  var raw = AUDIO_DATA.frames[f];
  if (!prev) {
    prev = { rms: raw.rms, bands: raw.bands.slice() };
    return prev;
  }
  prev = {
    rms: prev.rms * smoothing + raw.rms * (1 - smoothing),
    bands: prev.bands.map(function(b, i) {
      return prev.bands[i] * smoothing + b * (1 - smoothing);
    })
  };
  return prev;
}
```

---

## Layering for Depth

Use multiple canvases with different z-index:

```html
<canvas id="bg-layer" style="position:absolute;top:0;left:0;z-index:1;"></canvas>
<canvas id="main-layer" style="position:absolute;top:0;left:0;z-index:2;"></canvas>
```

- Background layer: bass/rms driven (slow, broad)
- Foreground layer: individual bands (fast, detailed)

---

## Guidelines

- **Subtlety for text** — 3-6% scale variation, soft glow. Heavy pulsing makes text unreadable.
- **Go bigger on non-text** — backgrounds and shapes can handle 10-30% swings.
- **Match the energy** — corporate = subtle; music video = dramatic.
- **Deterministic** — pre-extracted data, no Web Audio API, no runtime analysis.
- **Content-not-medium principle** — the viewer should notice the content first, the reactivity second.

---

## Constraints

- All audio data must be pre-extracted (use `scripts/extract-audio-data.py`)
- No `Math.random()` or `Date.now()`
- Audio reactivity runs on the same GSAP timeline as everything else
