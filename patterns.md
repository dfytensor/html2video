# Composition Patterns

Read this file when structuring multi-element HTML pages — PPT slides, flowcharts, or mixed layouts.

---

## Pattern 1: Title Card

Full-screen title with centered text, decorative background, and fade entrance.

```html
<div class="slide title-card">
  <div class="bg-layer">
    <div class="gradient-orb"></div>
    <div class="noise-overlay"></div>
  </div>
  <div class="content">
    <h1 class="title">Main Title</h1>
    <p class="subtitle">Subtitle or Tagline</p>
  </div>
</div>
```

```css
.title-card {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
}
.title { font-size: 56px; font-weight: 900; }
.subtitle { font-size: 28px; font-weight: 300; opacity: 0.8; margin-top: 16px; }
```

GSAP entrance:
```javascript
tl.from(".title", { y: 40, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
tl.from(".subtitle", { y: 20, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.5);
```

---

## Pattern 2: Two-Column Comparison (VS)

Side-by-side comparison with contrasting colors, used for debate/compare content.

```html
<div class="slide vs-card">
  <div class="vs-left">
    <div class="vs-label">Option A</div>
    <ul class="vs-points">...</ul>
  </div>
  <div class="vs-divider">
    <span class="vs-text">VS</span>
  </div>
  <div class="vs-right">
    <div class="vs-label">Option B</div>
    <ul class="vs-points">...</ul>
  </div>
</div>
```

```css
.vs-card {
  display: flex;
  gap: 0;
}
.vs-left, .vs-right {
  flex: 1;
  padding: 40px;
}
.vs-left { background: rgba(231, 76, 60, 0.1); }
.vs-right { background: rgba(46, 204, 113, 0.1); }
.vs-divider {
  display: flex;
  align-items: center;
  padding: 0 20px;
}
.vs-text {
  font-size: 32px;
  font-weight: 900;
  color: rgba(255,255,255,0.3);
}
```

---

## Pattern 3: Step Flow (Horizontal)

Horizontal step-by-step flow with connecting lines/arrows.

```html
<div class="slide step-flow">
  <div class="step" data-step="1">
    <div class="step-icon">01</div>
    <div class="step-title">Step One</div>
    <div class="step-desc">Description</div>
  </div>
  <div class="step-arrow">→</div>
  <div class="step" data-step="2">
    <div class="step-icon">02</div>
    <div class="step-title">Step Two</div>
    <div class="step-desc">Description</div>
  </div>
  <div class="step-arrow">→</div>
  <div class="step" data-step="3">
    <div class="step-icon">03</div>
    <div class="step-title">Step Three</div>
    <div class="step-desc">Description</div>
  </div>
</div>
```

```css
.step-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 40px;
}
.step {
  flex: 1;
  text-align: center;
  padding: 24px;
  border: 2px solid rgba(255,255,255,0.1);
  border-radius: 12px;
}
.step-icon {
  font-size: 48px;
  font-weight: 900;
  color: #4caf50;
}
```

GSAP with stagger:
```javascript
tl.from(".step", { y: 40, opacity: 0, duration: 0.5, stagger: 0.2, ease: "power2.out" }, 0.2);
tl.from(".step-arrow", { scaleX: 0, opacity: 0, duration: 0.3, stagger: 0.2, ease: "power2.out" }, 0.6);
```

---

## Pattern 4: Data Dashboard

Grid of metric cards with large numbers and labels.

```html
<div class="slide dashboard">
  <h2 class="section-title">Key Metrics</h2>
  <div class="metric-grid">
    <div class="metric-card">
      <div class="metric-value" data-target="95">0</div>
      <div class="metric-label">Accuracy (%)</div>
    </div>
    <div class="metric-card">
      <div class="metric-value" data-target="3.2">0</div>
      <div class="metric-label">Parameters (M)</div>
    </div>
  </div>
</div>
```

```css
.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}
.metric-value {
  font-size: 64px;
  font-weight: 900;
  color: #4caf50;
  font-variant-numeric: tabular-nums;
}
```

Count-up animation:
```javascript
document.querySelectorAll(".metric-value").forEach(function(el) {
  var target = parseFloat(el.dataset.target);
  var counter = { val: 0 };
  tl.to(counter, {
    val: target,
    duration: 1.5,
    ease: "power2.out",
    onUpdate: function() { el.textContent = counter.val.toFixed(1); }
  }, 0.3);
});
```

---

## Pattern 5: Architecture Diagram

Box-and-line diagram showing system components and connections.

```html
<div class="slide architecture">
  <div class="arch-node" id="node-a">
    <div class="arch-icon"><i class="fas fa-database"></i></div>
    <div class="arch-label">Database</div>
  </div>
  <svg class="arch-connections" viewBox="0 0 800 400">
    <line x1="200" y1="200" x2="400" y2="200" class="arch-line"/>
    <line x1="400" y1="200" x2="600" y2="200" class="arch-line"/>
  </svg>
  <div class="arch-node" id="node-b">
    <div class="arch-icon"><i class="fas fa-server"></i></div>
    <div class="arch-label">Server</div>
  </div>
</div>
```

GSAP draw-line animation:
```javascript
document.querySelectorAll(".arch-line").forEach(function(line) {
  var length = Math.sqrt(
    Math.pow(line.x2.baseVal.value - line.x1.baseVal.value, 2) +
    Math.pow(line.y2.baseVal.value - line.y1.baseVal.value, 2)
  );
  line.style.strokeDasharray = length;
  line.style.strokeDashoffset = length;
  tl.to(line, { strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }, 0.4);
});
```

---

## Pattern 6: Quote / Highlight

Full-screen quote with large text, attribution, and minimal decoration.

```html
<div class="slide quote-card">
  <div class="quote-mark">"</div>
  <blockquote class="quote-text">
    To be or not to be, that is the question.
  </blockquote>
  <cite class="quote-author">— Shakespeare</cite>
</div>
```

```css
.quote-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 120px;
}
.quote-mark {
  font-size: 120px;
  line-height: 1;
  color: rgba(255,255,255,0.1);
}
.quote-text {
  font-size: 36px;
  font-weight: 300;
  line-height: 1.5;
  max-width: 800px;
}
```

---

## Pattern 7: Timeline / History

Vertical or horizontal timeline with events.

```html
<div class="slide timeline">
  <div class="timeline-line"></div>
  <div class="timeline-event" data-year="2018">
    <div class="timeline-dot"></div>
    <div class="timeline-year">2018</div>
    <div class="timeline-desc">Event description</div>
  </div>
</div>
```

---

## Data in Motion

When displaying data, stats, or infographics in video:

### Visual Continuity

When successive stats belong to the same concept (Q1 → Q2 → Q3 → Q4, or three metrics for the same product), keep them in the same visual space with the same aesthetic. Only the VALUE changes. An aesthetic change should signal a new concept, not just a new number.

### Numbers Need Visual Weight

A number on its own floats in empty space. Pair every metric with a visual element that gives it presence — a proportional fill bar, a background color shift, a shape that represents the value, a progress ring. The visual doesn't need to be a chart — it just needs to fill the frame and make the data feel tangible.

### Avoid Web Patterns

- **No pie charts** — hard to compare, looks like PowerPoint
- **No multi-axis charts** — viewer can't study intersections in a 3-second window
- **No 6-panel dashboards** — 2-3 related metrics side-by-side is fine, 6+ is a web pattern
- **No gridlines, tick marks, or legends** — visual noise that adds nothing in motion
- **No chart library output** — build with GSAP + SVG/CSS, not D3 or Chart.js

---

## Pattern Selection

| Content Type | Pattern | Notes |
|---|---|---|
| Cover / intro | Title Card | Centered, dramatic |
| Comparison / debate | VS Card | Side-by-side, contrasting colors |
| Process / steps | Step Flow | Horizontal or vertical, connected |
| Data / statistics | Dashboard | Grid of metric cards |
| System / architecture | Architecture Diagram | Box-and-line with SVG |
| Quote / key statement | Quote Card | Minimal, large text |
| History / progression | Timeline | Vertical with dots and line |
