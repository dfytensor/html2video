# Transition Catalog

Hard rules, scene template, and routing to implementation code. Read the reference file for the transition type you need — don't load all of them.

## Hard Rules (CSS)

These cause real bugs if violated.

**Scene visibility:** Scene 1 visible by default (no `opacity: 0`). Scenes 2+ have `opacity: 0` on the CONTAINER div. GSAP reveals them.

**Overlay elements:**
- Staggered blocks = full-screen, NOT thin strips
- Glitch RGB overlays = normal blending at 35% opacity, NOT `mix-blend-mode: multiply` (invisible on dark backgrounds)
- Light leak overlays = larger than the frame (2400px+), never a visible shape
- Overexposure = use `filter: brightness()` on the scene, not just a white overlay

**VHS tape:** Clone actual scene content with `cloneNode(true)`, NOT colored bars. Each strip wider than frame (2020px at left:-50px). Seeded PRNG for deterministic random offsets.

**Z-index:** Gravity drop, zoom out, diagonal split need outgoing scene ON TOP (`zIndex: 10`) so it exits while revealing the new scene behind (`zIndex: 1`).

**Blinds count by energy:** Calm: 4h/6v. Medium: 6-8h/8v. High: 12-16h/16v.

**Don't use:** Star iris (polygon interpolation broken), tilt-shift (no selective CSS blur), lens flare (visible shape), hinge/door (distorts too fast).

## Scene Template

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #000;
        font-family: "YOUR FONT", sans-serif;
      }
      .scene {
        position: absolute;
        top: 0;
        left: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      #scene1 { z-index: 1; background: #color; }
      #scene2 { z-index: 2; background: #color; opacity: 0; }
    </style>
  </head>
  <body>
    <div class="root-container">
      <div id="scene1" class="scene"><!-- visible --></div>
      <div id="scene2" class="scene"><!-- hidden --></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });
      // Transition code here
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

Every transition follows: position new scene → animate outgoing → swap → animate incoming → clean up overlays.

## CSS Transition Types

All code examples use `old` for the outgoing scene-inner selector and `new` for the incoming, with `T` as the transition start time.

| Type | Transitions | Implementation |
|---|---|---|
| **Push** | Push slide, vertical push, elastic push, squeeze | See [transitions.md](../transitions.md) for push/slide code |
| **Scale / Zoom** | Zoom through, zoom out | See [transitions.md](../transitions.md) for zoom code |
| **Reveal / Mask** | Circle iris, diamond iris, diagonal split | See [transitions.md](../transitions.md) for iris code |
| **Dissolve** | Crossfade, blur crossfade, focus pull, color dip | See [transitions.md](../transitions.md) for crossfade code |
| **Cover** | Staggered blocks, horizontal blinds, vertical blinds | See [transitions.md](../transitions.md) for blocks code |
| **Light** | Light leak, overexposure burn, film burn | See [transitions.md](../transitions.md) for light leak code |
| **Distortion** | Glitch, chromatic aberration, ripple, VHS tape | Custom implementation per type |
| **Pattern** | Grid dissolve, morph circle | Custom implementation per type |
| **Mechanical** | Shutter, clock wipe | Custom implementation per type |
| **Destruction** | Page burn | Custom implementation per type |

### Detailed Implementations

For detailed per-type GSAP code, read the specific sections in [transitions.md](../transitions.md). The main file contains ready-to-use code for:
- Crossfade, blur crossfade, push slide, zoom through
- Staggered blocks, light leak, circle iris

### Additional CSS Transitions

These require custom implementation. Key notes:

**Glitch:**
- Create RGB channel copies with `mix-blend-mode: screen`
- Offset each channel by 2-8px in random directions (seeded PRNG)
- Duration: 0.15-0.25s for high energy, 0.3-0.5s for medium

**Chromatic Aberration:**
- Three copies of the scene at different `left` offsets
- Red channel: `left: -Npx`, Blue channel: `left: +Npx`
- Blend with screen mode, opacity 35%
- Quick in, quick out: 0.2-0.3s total

**Gravity Drop:**
- Outgoing scene drops off bottom: `y: 1080, rotation: 2`
- Incoming scene slides up: `y: -20` → `y: 0`
- Outgoing scene needs higher z-index

**Grid Dissolve:**
- NxM grid of colored squares (cycle 5 palette colors)
- Squares scale in with stagger, then scale out
- Energy determines grid size: calm=3x2, medium=5x3, high=8x5

**Clock Wipe:**
- Use `clip-path: polygon()` with 9+ points
- Animate through 4 quadrants with separate tweens
- Rotation direction matches content flow

**Film Burn:**
- Warm color overlay (orange-red gradient)
- Overlay expands from center, then contracts
- Scene swap at peak brightness
- Duration: 0.6-1.0s for dramatic, 0.3-0.4s for snappy
