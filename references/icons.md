# Vector Icon Libraries Reference

Read this file when selecting icons for generated HTML — replacing emoji, decorating slides, or building architecture diagrams.

---

## Quick Selection Guide

| Library | Icons | Style | Best For | CDN Load |
|---|---|---|---|---|
| **Font Awesome 6** | 2,000+ | Solid / Regular / Brands | General purpose, established patterns | CSS only |
| **Lucide** | 1,500+ | Stroke (line) | Clean UI, modern, lightweight | JS + inline SVG |
| **Remix Icon** | 2,800+ | Neutral / filled / line | Versatile, good science/tech coverage | CSS only |
| **IconPark** (ByteDance) | 2,658+ | Outlined / filled / two-tone | Rich categories (science, data, hardware) | SVG inline or CSS |
| **Tabler Icons** | 6,100+ | Stroke (line) | Largest free stroke set, consistent | CSS only |
| **Phosphor Icons** | 7,000+ | 6 weights (thin→fill) | Maximum variety, flexible weight | CSS only |
| **Bootstrap Icons** | 2,000+ | Filled + outline | Bootstrap ecosystem, classic shapes | CSS only |
| **Material Symbols** | 2,500+ | Rounded / sharp / outlined | Google ecosystem, familiar | Font CSS |
| **IconBuddy** | 200,000+ | Mixed (aggregator) | Rare/specific icons, download SVG | SVG download |
| **Heroicons** | 300+ | Outline / solid / mini | Tailwind ecosystem, minimal | Inline SVG only |
| **Feather Icons** | 280+ | Stroke (line) | Ultra-minimal, consistent | Inline SVG or JS |

---

## Library Details & CDN Setup

### 1. Font Awesome 6 (Primary — Already Configured)

The default icon library in this project. All templates already load it.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
```

**Usage:**
```html
<i class="fa-solid fa-database"></i>
<i class="fa-solid fa-server"></i>
<i class="fa-solid fa-brain"></i>
<i class="fa-solid fa-bolt"></i>
<i class="fa-solid fa-shield-halved"></i>
<i class="fa-solid fa-robot"></i>
<i class="fa-solid fa-code"></i>
<i class="fa-solid fa-network-wired"></i>
<i class="fa-solid fa-microchip"></i>
<i class="fa-solid fa-satellite-dish"></i>
<i class="fa-solid fa-fire"></i>
<i class="fa-solid fa-rocket"></i>
<i class="fa-solid fa-chart-line"></i>
<i class="fa-solid fa-globe"></i>
<i class="fa-solid fa-lock"></i>
<i class="fa-solid fa-lightbulb"></i>
<i class="fa-brands fa-github"></i>
<i class="fa-brands fa-python"></i>
<i class="fa-brands fa-docker"></i>
```

**Style prefixes:**
- `fa-solid` (or `fas`) — Filled solid icons
- `fa-regular` (or `far`) — Outlined icons
- `fa-brands` (or `fab`) — Brand logos (GitHub, Python, Docker, etc.)
- `fa-light` (or `fal`) — Thin icons (Pro only)

---

### 2. Remix Icon

Open source, neutral style. Excellent science/tech coverage with 2,800+ icons. Single CSS file, no JS needed.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css">
```

**Usage:**
```html
<i class="ri-database-2-line"></i>
<i class="ri-cpu-line"></i>
<i class="ri-brain-line"></i>
<i class="ri-flashlight-line"></i>
<i class="ri-shield-check-line"></i>
<i class="ri-robot-line"></i>
<i class="ri-code-s-slash-line"></i>
<i class="ri-global-line"></i>
<i class="ri-lock-line"></i>
<i class="ri-lightbulb-line"></i>
<i class="ri-fire-line"></i>
<i class="ri-rocket-line"></i>
<i class="ri-line-chart-line"></i>
<i class="ri-server-line"></i>
<i class="ri-security-shield-line"></i>
```

**Style suffixes:**
- `-line` — Outlined (stroke)
- `-fill` — Filled (solid)
- Neither — Default (usually outlined)

**Recommended for:** Science content, data visualization, network diagrams. Strong category coverage in: arrows, buildings, business, communication, design, development, finance, health, map, media, system, weather.

---

### 3. IconPark (ByteDance)

ByteDance's icon library with 2,658+ icons. Rich categories including: science, data, charts, hardware, energy, industry, constellation, money, etc.

**Option A: SVG Inline (recommended for video — no external dependency)**

Download individual SVGs from https://iconpark.oceanengine.com/official and embed inline:

```html
<svg viewBox="0 0 48 48" width="32" height="32" fill="none" stroke="currentColor" stroke-width="3">
  <path d="..."/>
</svg>
```

**Option B: NPM/CDN package**

```html
<!-- Via jsDelivr (individual SVG files) -->
<img src="https://cdn.jsdelivr.net/npm/@icon-park/core/icons/outline/database.svg" width="32" alt="">
<img src="https://cdn.jsdelivr.net/npm/@icon-park/core/icons/outline/server.svg" width="32" alt="">
```

**Option C: IconPark React/Vue components (not for static HTML)**

**Browse icons:** https://iconpark.oceanengine.com/official

**Key icon categories for science/tech content:**

| Category | Examples |
|---|---|
| Base | aiming, bookmark, camera, config, lightning, power, search, setting, share |
| Datas | bar-chart, line-chart, pie-chart, data-display, data-server |
| Hardware | cpu, display, hard-drive, keyboard, memory, motherboard |
| Charts | analysis, bubble-chart, cumulative, diagram, fund, stock |
| Energy | battery-full, charge, electric, lightning, nuclear, solar-energy |
| Connect | bluetooth, cell-signal, download, link, upload, wifi |
| Arrows | all direction arrows, expand, shrink, sort |

**Recommended for:** Science/tech diagrams, hardware illustrations, data visualization, architecture diagrams. Excellent for replacing domain-specific emoji.

---

### 4. Lucide Icons

Modern, lightweight stroke icons. Built as a community fork of Feather Icons with 1,500+ icons.

```html
<script src="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js"></script>
```

**Usage (requires JS initialization):**
```html
<i data-lucide="database"></i>
<i data-lucide="server"></i>
<i data-lucide="cpu"></i>
<i data-lucide="brain"></i>
<i data-lucide="zap"></i>
<i data-lucide="shield"></i>
<i data-lucide="code"></i>
<i data-lucide="globe"></i>
<i data-lucide="lock"></i>
<i data-lucide="lightbulb"></i>
<i data-lucide="rocket"></i>
<i data-lucide="activity"></i>

<script>lucide.createIcons();</script>
```

**Alternative — SVG sprite (no JS needed):**
```html
<svg width="24" height="24">
  <use href="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.svg#database"/>
</svg>
```

**Recommended for:** Clean modern look, UI controls, lightweight pages. Best when paired with GSAP animations since individual icons can be targeted as SVG elements.

---

### 5. Tabler Icons

6,100+ free stroke icons — the largest free stroke icon set. All designed on a 24x24 grid with 2px stroke.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.4.0/dist/tabler-icons.min.css">
```

**Usage:**
```html
<i class="ti ti-database"></i>
<i class="ti ti-server"></i>
<i class="ti ti-brain"></i>
<i class="ti ti-bolt"></i>
<i class="ti ti-shield-check"></i>
<i class="ti ti-robot"></i>
<i class="ti ti-code"></i>
<i class="ti ti-world"></i>
<i class="ti ti-lock"></i>
<i class="ti ti-bulb"></i>
<i class="ti ti-rocket"></i>
<i class="ti ti-chart-line"></i>
<i class="ti ti-cpu"></i>
<i class="ti ti-device-router"></i>
<i class="ti ti-microchip"></i>
```

**Recommended for:** Maximum icon variety when Font Awesome or Remix Icon don't have the specific icon needed. Excellent coverage for: devices, networking, development, science, medical, math.

---

### 6. Phosphor Icons

7,000+ icons in 6 weights (thin, light, regular, bold, fill, duotone). Most flexible icon family.

```html
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/bold/style.css">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/fill/style.css">
```

**Usage:**
```html
<i class="ph ph-database"></i>
<i class="ph ph-bold ph-server"></i>
<i class="ph ph-fill ph-brain"></i>
<i class="ph ph-bolt"></i>
<i class="ph ph-shield-check"></i>
<i class="ph ph-robot"></i>
<i class="ph ph-code"></i>
<i class="ph ph-globe"></i>
<i class="ph ph-lock"></i>
<i class="ph ph-lightbulb"></i>
```

**Weight classes:** `ph` (regular), `ph-bold`, `ph-fill`, `ph-thin`, `ph-light`

**Recommended for:** When you need weight consistency with other visual elements (e.g., matching icon stroke weight to UI borders). Good for brand-consistent iconography.

---

### 7. Bootstrap Icons

2,000+ free icons by the Bootstrap team. Classic shapes, good coverage.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
```

**Usage:**
```html
<i class="bi bi-database"></i>
<i class="bi bi-server"></i>
<i class="bi bi-cpu"></i>
<i class="bi bi-lightning"></i>
<i class="bi bi-shield-check"></i>
<i class="bi bi-robot"></i>
<i class="bi bi-code-slash"></i>
<i class="bi bi-globe"></i>
<i class="bi bi-lock"></i>
<i class="bi bi-lightbulb"></i>
<i class="bi bi-rocket"></i>
<i class="bi bi-graph-up"></i>
```

**Recommended for:** When already using Bootstrap CSS in the page. Classic, well-known icon shapes.

---

### 8. Material Symbols (Google)

Google's Material Design icons. Familiar to most users.

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0">
```

**Usage:**
```html
<span class="material-symbols-outlined">database</span>
<span class="material-symbols-outlined">dns</span>
<span class="material-symbols-outlined">memory</span>
<span class="material-symbols-outlined">bolt</span>
<span class="material-symbols-outlined">shield</span>
<span class="material-symbols-outlined">smart_toy</span>
<span class="material-symbols-outlined">code</span>
<span class="material-symbols-outlined">public</span>
<span class="material-symbols-outlined">lock</span>
<span class="material-symbols-outlined">lightbulb</span>
```

**Recommended for:** Android/Material Design themed pages. Variable font technology allows weight/fill/grade adjustment via CSS.

---

### 9. IconBuddy (Aggregator)

Not a library — an icon search engine aggregating 200,000+ icons from multiple open source sets. Use for finding rare or specific icons.

**Website:** https://iconbuddy.com/

**Usage:** Search → Download SVG → Embed inline in HTML:

```html
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2">
  <path d="...downloaded SVG path..."/>
</svg>
```

**Recommended for:** When no icon library has the exact icon you need. Download SVG and embed directly. Always free, no attribution required for most icons.

---

### 10. Heroicons (Tailwind)

300+ hand-crafted icons by the Tailwind CSS team. Minimal, clean design.

**No CDN webfont — SVG inline only:**

```html
<!-- Download from https://heroicons.com/ and embed -->
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
     stroke-width="1.5" stroke="currentColor" width="24" height="24">
  <path stroke-linecap="round" stroke-linejoin="round" d="M..."/>
</svg>
```

**Recommended for:** Tailwind-themed pages. Small set but very high quality.

---

### 11. Feather Icons

280+ simply beautiful stroke icons. The original minimal icon set.

```html
<script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
```

**Usage:**
```html
<i data-feather="database"></i>
<i data-feather="server"></i>
<i data-feather="cpu"></i>
<i data-feather="zap"></i>
<i data-feather="shield"></i>
<i data-feather="code"></i>
<i data-feather="globe"></i>
<i data-feather="lock"></i>
<i data-feather="lightbulb"></i>

<script>feather.replace();</script>
```

**Recommended for:** Ultra-minimal aesthetic. Most icons are available in larger libraries (Lucide is a superset).

---

## Strategy: Which Library to Use

### Default (No Decision Needed)

Use **Font Awesome** — it's already loaded in all templates. Don't add extra icon libraries unless needed.

### When to Add a Second Library

| Situation | Add Library | Reason |
|---|---|---|
| Science/tech icons missing | Remix Icon | Best science category coverage |
| Need a specific tech icon | IconPark or Tabler | Largest tech-specific sets |
| Want stroke-consistent design | Lucide or Tabler | All stroke, no fill inconsistency |
| Only need 1-2 rare icons | IconBuddy SVG | Download and inline, no library load |
| Building architecture diagrams | IconPark + Font Awesome | Best hardware/system icons |
| Clean modern UI aesthetic | Lucide or Feather | Minimal stroke weight |

### Performance Guidelines

| Approach | HTTP Requests | Use When |
|---|---|---|
| Font Awesome only (default) | 1 CSS file | 90% of cases |
| FA + 1 additional CSS library | 2 CSS files | Need specific icon coverage |
| FA + JS library (Lucide/Feather) | 1 CSS + 1 JS | Need SVG manipulation |
| Inline SVG (no library) | 0 | Only 1-3 custom icons needed |

**Rule: Never load more than 2 icon libraries per page.** If you need icons from 3+ sources, download the SVGs and inline them.

---

## Emoji → Icon Mapping (Common Replacements)

When replacing emoji in generated HTML, use this mapping:

| Emoji | Icon (Font Awesome) | Icon (Remix Icon) | Icon (Lucide) |
|---|---|---|---|
| ⚡ | `fa-bolt` | `ri-flashlight-line` | `zap` |
| 🔥 | `fa-fire` | `ri-fire-line` | `flame` |
| 🚀 | `fa-rocket` | `ri-rocket-line` | `rocket` |
| 💡 | `fa-lightbulb` | `ri-lightbulb-line` | `lightbulb` |
| 🧠 | `fa-brain` | `ri-brain-line` | `brain` |
| 🤖 | `fa-robot` | `ri-robot-line` | `bot` |
| 🔒 | `fa-lock` | `ri-lock-line` | `lock` |
| 🌐 | `fa-globe` | `ri-global-line` | `globe` |
| 📊 | `fa-chart-bar` | `ri-bar-chart-line` | `bar-chart-2` |
| 📈 | `fa-chart-line` | `ri-line-chart-line` | `trending-up` |
| 💻 | `fa-laptop-code` | `ri-computer-line` | `laptop` |
| 🗄️ | `fa-database` | `ri-database-2-line` | `database` |
| 🔗 | `fa-link` | `ri-link` | `link` |
| ⚙️ | `fa-gear` | `ri-settings-3-line` | `settings` |
| ✅ | `fa-circle-check` | `ri-check-line` | `check-circle` |
| ❌ | `fa-circle-xmark` | `ri-close-line` | `x-circle` |
| ⚠️ | `fa-triangle-exclamation` | `ri-alert-line` | `alert-triangle` |
| 🎯 | `fa-bullseye` | `ri-focus-3-line` | `target` |
| 🔑 | `fa-key` | `ri-key-line` | `key` |
| 🛡️ | `fa-shield-halved` | `ri-shield-check-line` | `shield-check` |
| 📡 | `fa-satellite-dish` | `ri-signal-tower-line` | `radio` |
| 🔬 | `fa-microscope` | `ri-microscope-line` | `microscope` |
| 🧪 | `fa-flask` | `ri-flask-line` | `flask-conical` |
| ⏱️ | `fa-stopwatch` | `ri-timer-line` | `timer` |
| 🏗️ | `fa-building` | `ri-building-line` | `building` |
| 💰 | `fa-coins` | `ri-money-dollar-circle-line` | `coins` |
| 📱 | `fa-mobile-screen` | `ri-smartphone-line` | `smartphone` |
| ☁️ | `fa-cloud` | `ri-cloud-line` | `cloud` |
| 🔍 | `fa-magnifying-glass` | `ri-search-line` | `search` |
| 🎨 | `fa-palette` | `ri-palette-line` | `palette` |
| 📦 | `fa-box` | `ri-box-3-line` | `box` |
| ⭐ | `fa-star` | `ri-star-line` | `star` |
| ❤️ | `fa-heart` | `ri-heart-line` | `heart` |
| 👁️ | `fa-eye` | `ri-eye-line` | `eye` |
| 🎓 | `fa-graduation-cap` | `ri-graduation-cap-line` | `graduation-cap` |
| 📝 | `fa-pen-to-square` | `ri-edit-line` | `edit` |
| 🏠 | `fa-house` | `ri-home-line` | `home` |
| ⬆️ | `fa-arrow-up` | `ri-arrow-up-line` | `arrow-up` |
| ✨ | `fa-wand-magic-sparkles` | `ri-magic-line` | `sparkles` |
| 🧩 | `fa-puzzle-piece` | `ri-puzzle-line` | `puzzle` |

---

## SVG Inline Pattern (Library-Free)

When you only need a few custom icons (from IconBuddy, Heroicons, or manual SVG), use this pattern:

```html
<div class="icon-svg" style="width:32px;height:32px;">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       stroke-linecap="round" stroke-linejoin="round" width="100%" height="100%">
    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
    <path d="M2 17l10 5 10-5"/>
    <path d="M2 12l10 5 10-5"/>
  </svg>
</div>
```

**CSS for consistent sizing:**
```css
.icon-svg {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.icon-svg svg {
  color: inherit;
}
```

---

## Icon Sizing for Video

Icons in video must be large enough to be readable:

| Context | Size | Font Awesome Class |
|---|---|---|
| Inline with body text | 20-24px | `fa-lg` or style `font-size:20px` |
| Card header icon | 32-40px | `fa-2x` or style `font-size:32px` |
| Step flow number | 48-56px | style `font-size:48px` |
| Hero visual icon | 64-120px | style `font-size:80px` |
| Background decorative | 120-200px | style `font-size:160px; opacity:0.1` |

**GSAP animation for icons:**
```javascript
tl.from(".hero-icon", {
  scale: 0,
  rotation: -180,
  duration: 0.6,
  ease: "back.out(1.7)"
}, 0.1);
```

---

## CDN Links Summary

Copy-paste ready CDN links. Only add what you need.

```html
<!-- Font Awesome 6 (PRIMARY - always include) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<!-- Remix Icon -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css">

<!-- Tabler Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.4.0/dist/tabler-icons.min.css">

<!-- Phosphor Icons (regular weight) -->
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">

<!-- Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<!-- Material Symbols -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0">

<!-- Lucide (requires JS) -->
<script src="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js"></script>
<script>lucide.createIcons();</script>

<!-- Feather Icons (requires JS) -->
<script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
<script>feather.replace();</script>

<!-- IconPark (individual SVG files via CDN) -->
<img src="https://cdn.jsdelivr.net/npm/@icon-park/core/icons/outline/database.svg" width="32" alt="">
```

---

## Themed Icon Sets

### Cultivation / Xianxia / Wuxia (修仙 / 仙侠 / 武侠)

43 SVG icons covering cultivation, alchemy, beasts, five elements, spiritual practice, and treasures.

**Setup:**
```bash
python scripts/download-cultivation-icons.py --test
```

**Usage:**
```html
<img src="assets/icons/cultivation/cauldron.svg" alt="丹炉"
     style="width:64px;height:64px;filter:invert(1);">
```

**Categories:** Weapon (武器), Alchemy (炼丹), Nature (自然), Beast (灵兽), Element (五行), Spiritual (修为), Treasure (宝物), Body (肉身)

**Full catalog:** See [references/cultivation-icons.md](cultivation-icons.md) for complete icon list, emoji mapping, GSAP animation examples, and source attribution.

### Science/Tech Themed Sets (化学/生物/硬件/能源/金融/气象/工业)

55 SVG icons for 7 science/tech domains that Font Awesome doesn't fully cover.

**Setup:**
```bash
python scripts/download-themed-icons.py --test
```

**Categories:** Chemistry (化学, 8), Biology (生物, 7), Hardware (硬件, 9), Energy (能源, 8), Finance (金融, 8), Weather (气象, 7), Industry (工业, 8)

**Usage:**
```html
<img src="assets/icons/chemistry/flask.svg" alt="烧瓶"
     style="width:64px;height:64px;filter:invert(1);">
```

**Full catalog:** See [references/themed-icons.md](themed-icons.md) for complete icon list, emoji mapping, and GSAP examples.
