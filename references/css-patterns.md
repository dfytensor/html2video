# CSS Marker Patterns

Read this file when you need beyond-color emphasis on text: highlights, circles, scribbles, etc.

These patterns use CSS + GSAP for deterministic, fully seekable marker effects.

---

## 1. Highlight (Yellow Bar Sweep)

A colored bar sweeps across the text from left to right.

```html
<span class="marker-highlight" data-color="#FFBE0B">Key Concept</span>
```

```css
.marker-highlight {
  position: relative;
  display: inline;
  background: linear-gradient(to right, var(--marker-color, #FFBE0B) 50%, transparent 50%);
  background-size: 200% 100%;
  background-position: 100% 0;
}
.marker-highlight.active {
  background-position: 0% 0;
}
```

```javascript
gsap.to(".marker-highlight", {
  backgroundPosition: "0% 0",
  duration: 0.4,
  ease: "power2.out",
  stagger: 0.15
});
```

---

## 2. Circle (Hand-Drawn Ellipse)

SVG ellipse that scales in around the text.

```html
<span class="marker-circle-wrap">
  <span class="marker-circle-text">Important</span>
  <svg class="marker-circle-svg" viewBox="0 0 200 60" preserveAspectRatio="none">
    <ellipse cx="100" cy="30" rx="95" ry="25" fill="none" stroke="#FFBE0B" stroke-width="3" class="marker-ellipse"/>
  </svg>
</span>
```

```css
.marker-circle-wrap {
  position: relative;
  display: inline-block;
}
.marker-circle-svg {
  position: absolute;
  top: -10px; left: -10px;
  width: calc(100% + 20px);
  height: calc(100% + 20px);
  pointer-events: none;
}
.marker-ellipse {
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
}
```

```javascript
gsap.to(".marker-ellipse", {
  strokeDashoffset: 0,
  duration: 0.6,
  ease: "power2.out",
  stagger: 0.2
});
```

---

## 3. Burst (Radiating Lines)

Short lines radiate outward from the center of the text.

```html
<span class="marker-burst" data-count="8">Emphasis</span>
```

```javascript
function createBurstLines(el, count) {
  for (let i = 0; i < count; i++) {
    const line = document.createElement("div");
    const angle = (360 / count) * i;
    line.style.cssText = `
      position: absolute; top: 50%; left: 50%;
      width: 2px; height: 0; background: #FFBE0B;
      transform-origin: center bottom;
      transform: translate(-50%, -100%) rotate(${angle}deg);
    `;
    el.style.position = "relative";
    el.appendChild(line);
    gsap.to(line, { height: 20, duration: 0.3, ease: "power2.out", delay: i * 0.03 });
  }
}
```

---

## 4. Scribble (Wavy Underline)

SVG wavy line drawn beneath text using stroke-dashoffset animation.

```html
<span class="marker-scribble-wrap">
  <span>Concept</span>
  <svg class="marker-scribble" viewBox="0 0 200 20" preserveAspectRatio="none">
    <path d="M0,10 Q25,0 50,10 Q75,20 100,10 Q125,0 150,10 Q175,20 200,10"
          fill="none" stroke="#FFBE0B" stroke-width="2.5"/>
  </svg>
</span>
```

```css
.marker-scribble {
  position: absolute;
  bottom: -4px; left: 0;
  width: 100%; height: 20px;
  pointer-events: none;
}
.marker-scribble path {
  stroke-dasharray: 300;
  stroke-dashoffset: 300;
}
```

```javascript
gsap.to(".marker-scribble path", {
  strokeDashoffset: 0,
  duration: 0.5,
  ease: "power2.out",
  stagger: 0.15
});
```

---

## 5. Sketchout (Cross-Hatch Lines)

Multiple angled lines drawn through the text, like a sketch mark.

```html
<span class="marker-sketchout">Removed</span>
```

```css
.marker-sketchout {
  position: relative;
  display: inline-block;
}
```

```javascript
function createSketch(el) {
  const lines = 5;
  for (let i = 0; i < lines; i++) {
    const line = document.createElement("div");
    line.style.cssText = `
      position: absolute; top: -2px; left: -4px; right: -4px;
      height: 2px; background: #e74c3c;
      transform: rotate(${-30 + (60 / (lines - 1)) * i}deg) scaleX(0);
      transform-origin: left center;
    `;
    el.appendChild(line);
    gsap.to(line, { scaleX: 1, duration: 0.15, delay: i * 0.04, ease: "power3.out" });
  }
}
```

---

## Quick Selection

| Marker | Feel | Best for |
|---|---|---|
| Highlight | Clean, editorial | Definitions, key phrases |
| Circle | Hand-drawn, organic | Emphasis, attention |
| Burst | Energetic, explosive | Important numbers, reveals |
| Scribble | Casual, annotated | Annotations, notes |
| Sketchout | Crossed-out, removed | Errors, deprecated info |

All markers are deterministic (no `Math.random()`), seekable (work with GSAP timeline scrubbing), and nestable.
