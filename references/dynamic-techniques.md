# Dynamic Caption Techniques

Read this file before writing advanced caption animation code. Pick your technique combination from the table below based on the energy level, then implement using standard GSAP patterns.

## Technique Selection by Energy

| Energy level | Highlight                             | Exit                | Cycle pattern                             |
| ------------ | ------------------------------------- | ------------------- | ----------------------------------------- |
| High         | Karaoke with accent glow + scale pop  | Scatter or drop     | Alternate highlight styles every 2 groups |
| Medium-high  | Karaoke with color pop                | Scatter or collapse | Alternate every 3 groups                  |
| Medium       | Karaoke (subtle, white only)          | Fade + slide        | Alternate every 3 groups                  |
| Medium-low   | Karaoke (minimal scale change)        | Fade                | Single style, vary ease per group         |
| Low          | Karaoke (warm tones, slow transition) | Collapse            | Alternate every 4 groups                  |

**All energy levels use karaoke highlight as the baseline.** The difference is intensity — high energy gets accent color + glow + 15% scale pop on active words, low energy gets a gentle white shift with 3% scale.

**Emphasis words always break the pattern.** When a word is flagged as emphasis (emotional keyword, ALL CAPS, brand name), give it a stronger animation than surrounding words (larger scale, accent color, overshoot ease). This creates contrast.

**Marker highlight modes add a visual layer on top of karaoke.** For emphasis words that need more than color/scale, add a marker-style effect — highlight sweep, circle, burst, or scribble — using [css-patterns.md](css-patterns.md). Match mode to energy: burst for hype, circle for key terms, highlight for standard, scribble for subtle.

---

## Audio-Reactive Captions (Mandatory for Music)

**If the source audio is music (vocals over instrumentation, beats, any musical content), you MUST extract audio data and add audio-reactive animations.** This is not optional — music without audio reactivity looks disconnected.

The group loop already iterates over every caption group. At that point, read the audio data for each group's time range and modulate the group's animation intensity with regular GSAP tweens:

```js
var AUDIO = JSON.parse(audioDataJson); // { fps, totalFrames, frames: [{ bands: [...] }] }

groups.forEach(function (group, gi) {
  var groupEl = document.getElementById("cg-" + gi);
  if (!groupEl) return;

  var startFrame = Math.floor(group.start * AUDIO.fps);
  var endFrame = Math.min(Math.floor(group.end * AUDIO.fps), AUDIO.totalFrames - 1);
  var peakBass = 0;
  var peakTreble = 0;
  for (var f = startFrame; f <= endFrame; f++) {
    var frame = AUDIO.frames[f];
    if (!frame) continue;
    peakBass = Math.max(peakBass, frame.bands[0] || 0, frame.bands[1] || 0);
    peakTreble = Math.max(peakTreble, frame.bands[6] || 0, frame.bands[7] || 0);
  }

  // Louder groups enter bigger and glowier
  tl.to(
    groupEl,
    {
      scale: 1 + peakBass * 0.06,
      textShadow:
        "0 0 " + Math.round(peakTreble * 12) + "px rgba(255,255,255," + peakTreble * 0.4 + ")",
      duration: 0.3,
      ease: "power2.out",
    },
    group.start,
  );

  // Reset at exit
  tl.set(groupEl, { scale: 1, textShadow: "none" }, group.end - 0.15);
});
```

This shapes the animation at build time, not playback time — no per-frame callbacks, no `tl.call()` loops, no async fetch timing issues.

Keep audio reactivity subtle — 3-6% scale variation and soft glow. Heavy pulsing makes text unreadable.

To generate the audio data file:

```bash
python scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json
```

---

## Combining Techniques

Don't use the same highlight animation on every group — cycle through styles using the group index. Don't combine multiple competing animations on the same word at the same timestamp. Vary techniques across groups to match the content's pace changes.

**Marker highlight effects** (from [css-patterns.md](css-patterns.md)) layer well with karaoke — use karaoke for the word-by-word reveal, then add a marker effect on emphasis words only. For example: karaoke highlights each word in white, but brand names get a yellow highlight sweep and stats get a red circle.

---

## Slam Entrance

Words slam in from above with a bounce:

```js
tl.from(groupEl, {
  y: -80,
  opacity: 0,
  scale: 1.3,
  duration: 0.25,
  ease: "back.out(2)",
}, group.start);
```

Best for: hype content, product names, statistics.

---

## Scatter Exit

Words scatter in random directions (using seeded PRNG for determinism):

```js
function mulberry32(a) {
  return function() {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    var t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

var rng = mulberry32(42);
var words = groupEl.querySelectorAll(".caption-word");
words.forEach(function(word) {
  var angle = rng() * Math.PI * 2;
  var distance = 50 + rng() * 100;
  tl.to(word, {
    x: Math.cos(angle) * distance,
    y: Math.sin(angle) * distance,
    opacity: 0,
    rotation: (rng() - 0.5) * 90,
    duration: 0.4,
    ease: "power2.in",
  }, group.end - 0.4);
});
```

Best for: high energy exits, topic transitions.

---

## Elastic Spring

Word bounces with elastic easing:

```js
tl.from(groupEl, {
  scale: 0.3,
  opacity: 0,
  duration: 0.6,
  ease: "elastic.out(1, 0.5)",
}, group.start);
```

Best for: playful content, social media, consumer apps.

---

## 3D Rotation

Word rotates in from 3D perspective:

```css
.caption-group {
  perspective: 800px;
}
.caption-word {
  transform-style: preserve-3d;
}
```

```js
tl.from(groupEl, {
  rotationX: -90,
  opacity: 0,
  transformOrigin: "center bottom",
  duration: 0.5,
  ease: "power3.out",
}, group.start);
```

Best for: dramatic reveals, tech content.

---

## Clip-Path Reveal

Text revealed through expanding clip-path:

```js
tl.from(groupEl, {
  clipPath: "inset(0 100% 0 0)",
  duration: 0.4,
  ease: "power2.out",
}, group.start);
```

Best for: clean, editorial content. Works well with karaoke.
