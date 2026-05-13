# Motion Principles

Read this file when designing animations for HTML slides or interactive demos.

---

## Guardrails

You know these rules but you violate them. Stop.

- **Don't use the same ease on every tween.** You default to `power2.out` on everything. Vary eases like you vary font weights — no more than 2 independent tweens with the same ease in a scene.
- **Don't use the same speed on everything.** You default to 0.4-0.5s for everything. The slowest scene should be 3× slower than the fastest. Vary duration deliberately.
- **Don't enter everything from the same direction.** You default to `y: 30, opacity: 0` on every element. Vary: from left, from right, from scale, opacity-only, letter-spacing.
- **Don't use the same stagger on every scene.** Each scene needs its own rhythm.
- **Don't use ambient zoom on every scene.** Pick different ambient motion per scene: slow pan, subtle rotation, scale push, color shift, or nothing. Stillness after motion is powerful.
- **Don't start at t=0.** Offset the first animation 0.1-0.3s. Zero-delay feels like a jump cut. **Exception: Slide 1 hook** — see below.

---

## Hook Cover (Slide 1) — Fast Impact Animation

Slide 1 is the cover/title page, and its title IS the hook. This cover must create visual impact within 0.3 seconds.

### Timing

| Time | What Must Be Happening |
|---|---|
| 0.0s | Background + decorative elements already visible (no fade-in) |
| 0.05-0.15s | First hero element arrives (fast scale pop or slide-in) |
| 0.3s | All key elements visible |
| 0.5s | Ambient motion begins (particle burst, glow pulse, etc.) |
| 1.0s | Scene fully settled, ambient motion continues |

### Easing for Hook Cover

Use `expo.out` (authoritative snap) or `back.out(1.2)` (slight overshoot = energy). NOT `sine`, NOT `power1` — these feel sluggish on a hook.

```javascript
// Good: fast, confident hook cover entrance
tl.from(".cover-title", { scale: 0, opacity: 0, duration: 0.2, ease: "back.out(1.5)" }, 0.05);
tl.from(".cover-subtitle", { y: 30, opacity: 0, duration: 0.25, ease: "expo.out" }, 0.15);
tl.from(".cover-accent", { scale: 0.5, opacity: 0, duration: 0.2, ease: "back.out(1.2)" }, 0.2);

// Good: ambient energy starts fast
tl.to(".particle-burst", { scale: 1.5, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.3);
tl.to(".glow-accent", { scale: 1.005, duration: 1.5, repeat: -1, yoyo: true, ease: "sine.inOut" }, 0.5);
```

```javascript
// Bad: standard slow stagger on cover — viewer already left
tl.from(".title", { y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.3);
tl.from(".subtitle", { y: 30, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.5);
```

### Hook Cover Ambient Motion

The cover must feel alive, not static. Add one or more:

- **Scale pulse** on accent elements (1.003-1.008 scale, 2-3s cycle)
- **Color shift** on gradient (subtle hue rotation, 3-4s cycle)
- **Particle system** — canvas particles or floating dots
- **Glow breathing** — radial glow opacity oscillation

### Contrast with Slide 2

Slide 2 should feel calmer than the hook cover. The viewer has been hooked; now they need space to absorb. Slide 2 uses standard timing (0.1-0.3s offset, 0.4-0.6s duration, `power3.out`). The contrast between the fast hook cover and the calmer second slide creates a rhythm that holds attention.

---

## Easing is Emotion

The easing is the adverb. Same motion, different meaning:

| Easing | Emotion | Use for |
|---|---|---|
| `expo.out` | Confident | Authoritative entrances |
| `sine.inOut` | Dreamy | Calm transitions |
| `elastic.out` | Playful | Fun elements, social content |
| `power3.out` | Professional | Corporate, educational |
| `back.out(1.7)` | Surprising | Key reveals |
| `power4.in` | Urgent | Warnings, alerts |
| `none` | Mechanical | Technical, data-driven |

**Direction rules (non-optional):**
- `.out` for entrances (starts fast, decelerates). This is your default.
- `.in` for exits (starts slow, accelerates away).
- `.inOut` for moving between positions.

You get this backwards constantly. Ease-in for entrances feels sluggish. Ease-out for exits feels reluctant.

---

## Speed Communicates Weight

| Speed | Duration | Feels Like |
|---|---|---|
| Fast | 0.15-0.3s | Energy, urgency, confidence |
| Medium | 0.3-0.5s | Professional, most content |
| Slow | 0.5-0.8s | Gravity, luxury, contemplation |
| Very slow | 0.8-2.0s | Cinematic, emotional |

---

## Scene Structure: Build / Breathe / Resolve

Every slide has three phases. You dump everything in the build and leave nothing for breathe or resolve.

### Build (0-30%) — Elements Enter

Staggered entrances. Don't dump everything at once.

```javascript
// Good: staggered, varied
tl.from(".title", { y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.1);
tl.from(".subtitle", { y: 30, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.3);
tl.from(".card", { scale: 0.8, opacity: 0, duration: 0.4, stagger: 0.1, ease: "back.out(1.7)" }, 0.5);
```

```javascript
// Bad: everything at once, same ease
tl.from(".title, .subtitle, .card", { y: 30, opacity: 0, duration: 0.5, stagger: 0.1, ease: "power2.out" });
```

### Breathe (30-70%) — Ambient Motion

Subtle continued movement that keeps the scene alive:
- Slow scale pulse on accent elements (0.3% scale, 3-5s cycle)
- Gentle color shift on gradients
- Particle movement
- Floating elements with sine-wave y-offset

```javascript
// Ambient pulse
tl.to(".accent-circle", { scale: 1.003, duration: 2, repeat: 3, yoyo: true, ease: "sine.inOut" }, 0.8);
```

### Resolve (70-100%) — Settle

Stop ambient motion. Everything reaches rest. The scene feels "done" — ready for transition.

---

## Entrance Patterns

### Standard Slide-In

```javascript
gsap.from(".element", { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" });
```

### Scale Pop (For emphasis)

```javascript
gsap.from(".keyword", { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(1.7)" });
```

### Typewriter

```javascript
gsap.to("#text", { text: { value: "Hello World" }, duration: 1.2, ease: "none" });
```

### Stagger Cards

```javascript
gsap.from(".card", {
  y: 60, opacity: 0,
  duration: 0.5,
  stagger: { amount: 0.4, from: "center" },
  ease: "power2.out"
});
```

### Draw SVG Lines

```javascript
gsap.from("svg line, svg path", {
  strokeDashoffset: function(i, el) { return el.getTotalLength(); },
  duration: 0.8,
  stagger: 0.1,
  ease: "power2.out"
});
```

### Number Count-Up

```javascript
var counter = { val: 0 };
gsap.to(counter, {
  val: 2024,
  duration: 1.5,
  ease: "power2.out",
  onUpdate: function() { el.textContent = Math.round(counter.val); }
});
```

---

## Choreography = Hierarchy

The element that moves first is perceived as most important. Stagger in order of importance, not DOM order. Don't wait for completion — overlap entries. Total stagger sequence under 500ms regardless of item count.

1. **Most important** enters first or biggest
2. **Supporting** enters second, smaller
3. **Decorative** enters last, subtlest

---

## Transitions are Meaning

- **Crossfade** = "this continues"
- **Hard cut** = "wake up" / disruption
- **Slow dissolve** = "drift with me"

You crossfade everything. Use hard cuts for disruption and register shifts.

---

## Asymmetry

Entrances need longer than exits. A card takes 0.4s to appear but 0.25s to disappear.

---

## Visual Composition

You build for the web. Video frames are not pages.

- **Two focal points minimum per scene.** The eye needs somewhere to travel. Never a single text block floating in empty space.
- **Fill the frame.** Hero text: 60-80% of width. You will try to use web-sized elements. Don't.
- **Three layers minimum per scene.** Background treatment (glow, oversized faded type, color panel). Foreground content. Accent elements (dividers, labels, data bars).
- **Background is not empty.** Radial glows, oversized faded type bleeding off-frame, subtle border panels, hairline rules. Pure solid #000 reads as "nothing loaded."
- **Anchor to edges.** Pin content to left/top or right/bottom. Centered-and-floating is a web pattern.
- **Split frames.** Data panel on the left, content on the right. Top bar with metadata, full-width below. Zone-based layouts, not centered stacks.
- **Use structural elements.** Rules, dividers, border panels. They create paths for the eye and animate well (scaleX from 0).
- **Never have more than 3 simultaneous animations** visible at once.
- **Vary direction** — if one enters from left, the next enters from bottom.
- **Static elements ground the scene** — at least 30% of the scene should be still.

---

## Animation Reset (For CSS Mode)

When NOT using GSAP, CSS animations need the cloneNode reset:

```javascript
document.querySelectorAll('.slide').forEach(function(s) {
  s.querySelectorAll('.an, .anim-item, [style*="animation"]').forEach(function(item) {
    var clone = item.cloneNode(true);
    item.parentNode.replaceChild(clone, item);
  });
});
```

When using GSAP, use `tl.restart()` instead — no cloneNode needed.
