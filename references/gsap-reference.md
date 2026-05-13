# GSAP Animation Reference

Read this file when generating GSAP-powered animations for HTML demo pages or when the user requests advanced animation beyond CSS-only.

---

## Setup

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>
  gsap.registerPlugin(TextPlugin);
</script>
```

---

## Core Tween Methods

- **gsap.to(targets, vars)** — animate from current state to `vars`. Most common.
- **gsap.from(targets, vars)** — animate from `vars` to current state (entrances).
- **gsap.fromTo(targets, fromVars, toVars)** — explicit start and end.
- **gsap.set(targets, vars)** — apply immediately (duration 0).

Always use **camelCase** property names (e.g. `backgroundColor`, `rotationX`).

## Common vars

| Property | Description |
|---|---|
| `duration` | seconds (default 0.5) |
| `delay` | seconds before start |
| `ease` | `"power1.out"` (default), `"power3.inOut"`, `"back.out(1.7)"` |
| `stagger` | number `0.1` or object `{ amount: 0.3, from: "center" }` |
| `overwrite` | `false` (default), `true`, or `"auto"` |
| `repeat` | number or `-1` for infinite. `yoyo` alternates direction |
| `onComplete` / `onStart` / `onUpdate` | callbacks |

## Transform Aliases (Prefer Over Raw CSS)

| GSAP Property | Equivalent |
|---|---|
| `x`, `y`, `z` | translateX/Y/Z (px) |
| `xPercent`, `yPercent` | translateX/Y in % |
| `scale`, `scaleX`, `scaleY` | scale |
| `rotation` | rotate (deg) |
| `rotationX`, `rotationY` | 3D rotate |
| `skewX`, `skewY` | skew |
| `transformOrigin` | transform-origin |

- **autoAlpha** — prefer over `opacity`. At 0: also sets `visibility: hidden`.
- **clearProps** — `"all"` or comma-separated; removes inline styles on complete.

## Function-Based Values

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  stagger: 0.1,
});
```

## Easing

Built-in: `power1`-`power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`.
Each has `.in`, `.out`, `.inOut`.

**Direction rules:**
- `.out` for elements entering (starts fast, decelerates) — **default**
- `.in` for elements leaving (starts slow, accelerates)
- `.inOut` for elements moving between positions

## Defaults

```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

## Timelines

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 }).to(".b", { y: 50 }).to(".c", { opacity: 0 });
```

### Position Parameter

- **Absolute**: `1` — at 1s
- **Relative**: `"+=0.5"` — after end; `"-=0.2"` — before end
- **Label**: `"intro"`, `"intro+=0.3"`
- **Alignment**: `"<"` same start as previous; `">"` after previous ends

### Labels

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
```

### Nesting

```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
```

### Playback

`tl.play()`, `tl.pause()`, `tl.reverse()`, `tl.restart()`, `tl.time(2)`, `tl.progress(0.5)`, `tl.kill()`.

## Performance

- Animate `x`, `y`, `scale`, `rotation`, `opacity` (compositor). Avoid `width`, `height`, `top`, `left`.
- Use `stagger` instead of separate tweens with manual delays.
- `will-change: transform` only on elements that actually animate.
- Pause or kill off-screen animations.

## Effects

### Typewriter (with TextPlugin)

```javascript
const text = "Hello, world!";
const cps = 10;
tl.to("#typed-text", {
  text: { value: text },
  duration: text.length / cps,
  ease: "none"
}, startTime);
```

| CPS | Feel | Good for |
|---|---|---|
| 3-5 | Slow, deliberate | Dramatic reveals, suspense |
| 8-12 | Natural typing | Dialogue, narration |
| 15-20 | Fast, energetic | Tech demos, code |
| 30+ | Near-instant | Filling long blocks |

### Blinking Cursor

```html
<span id="typed-text"></span><span id="cursor" class="cursor-blink">|</span>
```

```css
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.cursor-blink { animation: blink 0.8s step-end infinite; }
.cursor-solid { animation: none; opacity: 1; }
.cursor-hide  { animation: none; opacity: 0; }
```

Pattern: blink → solid (typing starts) → type → solid → blink (typing done).

### Stagger Entrance

```javascript
gsap.from(".card", {
  y: 60,
  opacity: 0,
  duration: 0.6,
  stagger: { amount: 0.4, from: "start" },
  ease: "power3.out"
});
```

### Scale Pop (For emphasis)

```javascript
gsap.from(".keyword", {
  scale: 0,
  opacity: 0,
  duration: 0.4,
  stagger: 0.08,
  ease: "back.out(1.7)"
});
```

---

## GSAP + Slide Navigation (For PPT Mode)

When using GSAP with slide-based PPT navigation, register timelines per slide:

```javascript
window.__timelines = window.__timelines || {};

document.querySelectorAll('.slide').forEach(function(slide, idx) {
  var tl = gsap.timeline({ paused: true });
  var elements = slide.querySelectorAll('.an, .anim-item');

  tl.from(elements, {
    y: 30,
    opacity: 0,
    duration: 0.5,
    stagger: 0.1,
    ease: "power2.out"
  });

  window.__timelines["slide-" + idx] = tl;
});

function goToSlide(n) {
  document.querySelectorAll('.slide').forEach(function(s, i) {
    s.style.display = i === n ? 'block' : 'none';
  });
  if (window.__timelines["slide-" + n]) {
    window.__timelines["slide-" + n].restart();
  }
}
```

This replaces the CSS animation + cloneNode approach with deterministic GSAP timelines.

---

## Do Not

- Animate layout properties (`width`/`height`/`top`/`left`) when transforms suffice
- Use both `svgOrigin` and `transformOrigin` on the same SVG element
- Chain animations with `delay` when a timeline can sequence them
- Create tweens before the DOM exists
- Use `repeat: -1` — calculate exact repeats from duration
- Use `Math.random()` or `Date.now()` — must be deterministic
