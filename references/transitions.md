# Scene Transitions

Read this file when building multi-scene HTML pages with GSAP or CSS transitions between slides.

A transition tells the viewer how two scenes relate. A crossfade says "this continues." A push slide says "next point." A blur crossfade says "drift with me." Choose transitions that match what the content is doing emotionally, not just technically.

---

## Non-Negotiable Rules

1. **Every multi-slide page uses transitions.** No exceptions. Slides without transitions feel like jump cuts.
2. **Every slide uses entrance animations.** Elements animate IN via `gsap.from()` or CSS `@keyframes`. No element may appear fully-formed.
3. **Exit animations are BANNED** except on the final slide. The transition IS the exit. Outgoing content must be fully visible when the transition starts.
4. **Final slide exception:** MAY fade elements out (e.g., fade to black). This is the ONLY slide where exit animations are allowed.

---

## Energy → Transition Selection

| Energy | Primary Transition | Duration | Easing |
|---|---|---|---|
| **Calm** (wellness, luxury) | Blur crossfade, focus pull | 0.5-0.8s | `sine.inOut`, `power1` |
| **Medium** (corporate, explainer) | Push slide, crossfade | 0.3-0.5s | `power2`, `power3` |
| **High** (promos, launch) | Zoom through, glitch | 0.15-0.3s | `power4`, `expo` |

Pick ONE primary (60-70% of transitions) + 1-2 accents. Never use a different transition for every slide.

---

## Mood → Transition Type

Think about what the transition _communicates_, not just what it looks like.

| Mood | Transitions | Why |
|---|---|---|
| **Warm / inviting** | Light leak, blur crossfade, focus pull | Soft edges, warm color washes |
| **Cold / clinical** | Squeeze, zoom out, blinds | Mechanical transforms |
| **Editorial** | Push slide, vertical push, diagonal split | Like turning a page |
| **Tech / futuristic** | Grid dissolve, glitch, chromatic aberration | Data-driven, digital |
| **Tense / edgy** | Glitch, VHS, chromatic aberration, ripple | Instability, distortion |
| **Playful / fun** | Elastic push, 3D flip, circle iris, morph circle | Overshoot, bounce, expansion |
| **Dramatic / cinematic** | Zoom through, gravity drop, overexposure | Scale, weight, light extremes |
| **Premium / luxury** | Focus pull, blur crossfade, color dip to black | Restraint |
| **Retro / analog** | Film burn, light leak, VHS, clock wipe | Organic imperfection |

---

## Narrative Position

| Position | Use | Why |
|---|---|---|
| **Opening** | Most distinctive transition, 0.4-0.6s | Sets visual language for entire piece |
| **Between related points** | Primary transition, consistent, ~0.3s | Content is continuing, don't distract |
| **Topic change** | Different from primary (staggered blocks, shutter) | Signals "new section" — brain resets |
| **Climax / hero** | Boldest accent, fastest or most dramatic | This is the payoff |
| **Wind-down** | Gentle, blur crossfade, 0.5-0.7s | Let the viewer exhale |
| **Outro** | Slowest, simplest, 0.6-1.0s | Closure |

---

## Blur Intensity by Energy

| Energy | Blur | Duration | Hold |
|---|---|---|---|
| Calm | 20-30px | 0.8-1.2s | 0.3-0.5s |
| Medium | 8-15px | 0.4-0.6s | 0.1-0.2s |
| High | 3-6px | 0.2-0.3s | 0s |

---

## Presets

| Preset | Duration | Easing |
|---|---|---|
| `snappy` | 0.2s | `power4.inOut` |
| `smooth` | 0.4s | `power2.inOut` |
| `gentle` | 0.6s | `sine.inOut` |
| `dramatic` | 0.5s | `power3.in` → out |
| `instant` | 0.15s | `expo.inOut` |
| `luxe` | 0.7s | `power1.inOut` |

---

## CSS Transitions for Slide Navigation

### Crossfade (Simplest)

```css
.slide {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.slide.active {
  opacity: 1;
}
```

### Push Slide (Left/Right)

```javascript
function transitionPush(fromSlide, toSlide, direction) {
  var sign = direction === 'next' ? 1 : -1;
  gsap.set(toSlide, { xPercent: sign * 100, opacity: 1 });
  gsap.to(fromSlide, { xPercent: -sign * 100, duration: 0.5, ease: "power2.inOut" });
  gsap.to(toSlide, { xPercent: 0, duration: 0.5, ease: "power2.inOut" });
}
```

### Blur Crossfade

```javascript
function transitionBlur(fromSlide, toSlide) {
  gsap.to(fromSlide, { filter: "blur(20px)", opacity: 0, duration: 0.6, ease: "power2.inOut" });
  gsap.fromTo(toSlide, { filter: "blur(20px)", opacity: 0 }, { filter: "blur(0px)", opacity: 1, duration: 0.6, ease: "power2.inOut" });
}
```

### Zoom Through

```javascript
function transitionZoom(fromSlide, toSlide) {
  gsap.to(fromSlide, { scale: 3, opacity: 0, duration: 0.4, ease: "power3.in" });
  gsap.fromTo(toSlide, { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "power3.out", delay: 0.2 });
}
```

### Staggered Blocks

```javascript
function transitionBlocks(fromSlide, toSlide) {
  var blocks = [];
  var cols = 6, rows = 4;
  var blockW = 100 / cols, blockH = 100 / rows;

  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      var block = document.createElement('div');
      block.style.cssText = 'position:absolute;left:' + (c*blockW) + '%;top:' + (r*blockH) + '%;width:' + blockW + '%;height:' + blockH + '%;background:#000;z-index:100;transform:scaleX(0);';
      toSlide.parentNode.appendChild(block);
      blocks.push(block);
    }
  }

  gsap.to(blocks, { scaleX: 1, duration: 0.3, stagger: { amount: 0.2, from: "random" }, ease: "power4.inOut",
    onComplete: function() {
      fromSlide.style.opacity = 0;
      toSlide.style.opacity = 1;
      gsap.to(blocks, { scaleX: 0, duration: 0.3, stagger: { amount: 0.2 }, ease: "power4.inOut",
        onComplete: function() { blocks.forEach(function(b) { b.remove(); }); }
      });
    }
  });
}
```

### Light Leak

```javascript
function transitionLightLeak(fromSlide, toSlide) {
  var leak = document.createElement('div');
  leak.style.cssText = 'position:absolute;top:-50%;left:-50%;width:300%;height:300%;background:radial-gradient(circle,rgba(255,200,50,0.6),transparent 70%);z-index:100;opacity:0;';
  toSlide.parentNode.appendChild(leak);

  gsap.to(leak, { opacity: 1, duration: 0.3, ease: "power2.in",
    onComplete: function() {
      fromSlide.style.opacity = 0;
      toSlide.style.opacity = 1;
    }
  });
  gsap.to(leak, { opacity: 0, duration: 0.4, ease: "power2.out", delay: 0.4,
    onComplete: function() { leak.remove(); }
  });
}
```

### Circle Iris

```javascript
function transitionIris(fromSlide, toSlide) {
  gsap.set(toSlide, { clipPath: "circle(0% at 50% 50%)", opacity: 1 });
  gsap.to(toSlide, { clipPath: "circle(75% at 50% 50%)", duration: 0.6, ease: "power2.inOut",
    onComplete: function() {
      fromSlide.style.opacity = 0;
      toSlide.style.clipPath = "none";
    }
  });
}
```

---

## Transition Catalog

| Category | Transitions |
|---|---|
| Push/slide | Push slide, vertical push, elastic push, squeeze |
| Scale/zoom | Zoom through, zoom out, gravity drop, 3D flip |
| Reveal/mask | Circle iris, diamond iris, diagonal split, clock wipe |
| Dissolve | Crossfade, blur crossfade, focus pull, color dip |
| Cover | Staggered blocks, horizontal blinds, vertical blinds |
| Light | Light leak, overexposure, film burn |
| Distortion | Glitch, chromatic aberration, ripple, VHS |
| Pattern | Grid dissolve, morph circle |

---

## Visual Pattern Warning

Avoid transitions that create visible repeating geometric patterns — grids of tiles, hexagonal cells, uniform dot arrays, evenly-spaced blob circles. These look cheap and artificial regardless of the math behind them. Organic noise (FBM, domain warping) is good because it's irregular. Geometric repetition is bad because the eye instantly sees the grid.

---

## Transitions That Don't Work in CSS

Avoid: star iris (polygon interpolation broken), tilt-shift (no selective CSS blur), lens flare (visible shape, not optical), hinge/door (distorts too fast).
