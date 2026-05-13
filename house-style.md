# House Style

Default creative direction when no specific visual style is requested.

Read this file when generating HTML content and the user has not specified a visual preference.

---

## Before Writing HTML

1. **Interpret the prompt.** Generate real content. A recipe lists real ingredients. A network diagram has real protocols.
2. **Pick a palette.** Light or dark? Declare bg, fg, accent before writing code.
3. **Pick typefaces.** Run the font discovery script in [references/typography.md](references/typography.md) — or pick a font you already know that fits the theme.

## Lazy Defaults to Question

These patterns are AI design tells — the first thing every LLM reaches for. If you're about to use one, pause and ask: is this a deliberate choice for THIS content, or am I defaulting?

- Gradient text (`background-clip: text` + gradient)
- Left-edge accent stripes on cards/callouts
- Cyan-on-dark / purple-to-blue gradients / neon accents
- Pure `#000` or `#fff` (tint toward your accent hue instead)
- Identical card grids (same-size cards repeated)
- Everything centered with equal weight (lead the eye somewhere)
- Banned fonts (see [references/typography.md](references/typography.md) for full list)

If the content genuinely calls for one of these — centered layout for a solemn closing, cards for a real product UI mockup, a banned font because it's the perfect thematic match — use it. The goal is intentionality, not avoidance.

## Color Strategy

| Role | Value | Usage |
|---|---|---|
| Primary | `#2d3436` | Headings, key text |
| Accent | `#0984e3` | Links, highlights, CTAs |
| Background | `#ffffff` | Page background |
| Surface | `#f5f6fa` | Cards, panels |
| Text | `#2d3436` | Body text |
| Muted | `#636e72` | Captions, secondary text |

- Match light/dark to content: food, wellness, kids → light. Tech, cinema, finance → dark.
- One accent hue. Same background across all slides.
- Tint neutrals toward your accent (even subtle warmth/coolness beats dead gray).
- Declare palette up front. Don't invent colors per-element.
- **Contrast:** enforced by `contrast-report.py` (WCAG AA). Text must be readable with decoratives removed.

**PPT Mode:** Prefer gradient backgrounds (linear-gradient or radial-gradient). Use dark text on light cards.

**Animation Mode:** Deep green radial gradient background (`#0a1628` to `#1a3a2a`) with SVG noise texture and canvas particle system.

---

## Background Layer Requirements

Every slide or scene needs visual depth — persistent decorative elements that stay visible while content animates in. Without these, scenes feel empty during entrance staggering.

Include **2-5 decorative background elements** (mix and match):

- Radial glows (accent-tinted, low opacity, breathing scale)
- Ghost text (theme words at 3-8% opacity, very large, slow drift)
- Accent lines (hairline rules, subtle pulse)
- Subtle gradient overlays
- Geometric shapes (circles, lines) at low opacity
- SVG noise or dot patterns
- Blurred color blobs
- Canvas particle system (Animation mode)
- Thematic decoratives (orbit rings for space, grid lines for data, node connections for networks)

All decoratives should have slow ambient GSAP animation — breathing, drift, pulse. Static decoratives feel dead.

---

## Typography Quick Rules

| Context | Font | Weight | Size |
|---|---|---|---|
| Slide title | System sans-serif | 700 (bold) | 32-48px |
| Subtitle | System sans-serif | 600 | 24-32px |
| Body text | System sans-serif | 400 | 18-24px |
| Caption / annotation | Monospace | 400 | 14-16px |
| Emphasis keywords | System sans-serif | 700 | Same as parent + color highlight |

**For video optimization:**
- Minimum body text size: **18px** (readable at 1080p)
- Minimum title size: **32px**
- Use `font-weight: 700` for key terms
- Use `text-decoration: underline` for critical points
- Use `background-color` highlight strips for definitions

See [references/typography.md](references/typography.md) for full typography rules, banned fonts, and font discovery.

---

## Animation Quick Rules

| Rule | Description |
|---|---|
| Entrance only | Elements animate in, never out (unless it is the final slide) |
| Stagger | Items enter sequentially with 100-200ms delay |
| Duration | 400-800ms for entrance animations |
| Easing | `ease-out` or `cubic-bezier(0.25, 0.46, 0.45, 0.94)` for entrances |
| No flash | Never use `blink` or rapid color cycling |
| Reset on nav | Animations must replay when returning to a slide |
| Offset first | First animation 0.1-0.3s after slide appears, not t=0 |
| Vary eases | Use at least 3 different eases per slide |

For animated text effects (titles, hooks, section headers), see [references/text-animations.md](references/text-animations.md) for 10 effect types with GSAP code, theme matching, and prompt templates.

See [references/motion-principles.md](references/motion-principles.md) for full motion rules and [references/motion-principles.md](references/motion-principles.md) for the build/breathe/resolve scene structure.

---

## Icon Rules

- **Never use emoji characters** in generated HTML
- **Primary library:** Font Awesome 6 (`<i class="fas fa-xxx">`) — already loaded in all templates
- **Additional libraries** (load only when needed, max 2 icon libraries per page):
  - **Remix Icon** — best science/tech icon coverage (2,800+ icons)
  - **Lucide** — clean modern stroke icons (1,500+ icons, requires JS)
  - **Tabler Icons** — largest free stroke set (6,100+ icons)
  - **IconPark** (ByteDance) — rich science/hardware/data categories (2,658+ icons)
  - **Phosphor Icons** — 6 weight options (7,000+ icons)
  - **Bootstrap Icons** — classic shapes (2,000+ icons)
  - **IconBuddy** — 200k+ icon aggregator, download individual SVGs
- **Full catalog:** See [references/icons.md](references/icons.md) for CDN links, usage patterns, emoji-to-icon mapping, and library selection strategy
- After generation, scan for residual emoji and replace with corresponding UI icons

---

## Slide Structure Template

```
[Slide 1 — Hook Cover (标题页即钩子)]
  [Frame 0 — Visual Punch: oversized number/dramatic icon/split screen, high contrast, NOT gradient-only]
  [0.05-0.15s — Hook Title arrives: fast scale pop or snap-in, curiosity-triggering]
  [0.15-0.3s — Tension Subtitle: deepens mystery, NOT description]
  [0.3-0.5s — Accent elements + ambient motion begins]
  [Background Layer: gradient + bold decorative elements, visible at frame 0]
  [Hook Title: curiosity-triggering, uses one of 12 hook patterns — this IS the <h1>]
  [Tension Subtitle: deepens the curiosity gap or raises stakes]
  [Visual Hero: oversized number/icon with high contrast]
  [Animation: fast (0.15-0.35s), expo.out or back.out, first element at 0.05s]
  [Audio Hook: TTS first sentence reinforces hook, NOT "今天我们来了解..."]
  [Layout: Asymmetric — pin title to corner/edge, negative space]

[Slide 2 — Topic Reveal (回应封面悬念)]
  [Transition: most energetic transition of the video — zoom through / glitch / light leak]
  [Background Layer: matches overall palette]
  [Content Layer: definition + overview structure — answers the cover's question]
  [Animation: standard (0.3-0.5s), power3.out, offset 0.1-0.3s]

[Slide 3+ — Content Slides]
  [Background Layer: gradient + decorative elements]
  [Content Layer: title + body + highlights]
  [Animation Layer: entrance animations via CSS or GSAP]
```

### Hook Cover Visual Requirements

The cover page's title must grab attention immediately. It's not a template title — it's a billboard:

- **Hook title typography**: Title at 64-120px. This is the hook — rewrite the topic as a question/claim/number, not "XXX详解". Must use one of the 12 hook patterns from SKILL.md.
- **Tension subtitle**: A line that deepens the mystery (e.g. "99% 的程序员解释不清楚"), NOT a plain topic description.
- **Visual punch at frame 0**: Oversized number, dramatic icon, split-screen contrast, or result showcase. Must stop the scroll BEFORE any animation plays.
- **High contrast**: The hero element must contrast sharply with the background. No subtle-on-subtle.
- **Asymmetric layout**: Never center-everything. Pin the hook title to a corner or edge, use negative space.
- **Bold accent color**: Use the palette's accent at full saturation on the hero element.
- **Visible at frame 0**: Background treatment (gradient, glow, pattern) must render instantly — no fade-in on the background itself. Content animates on top of an already-established visual environment.
- **Motion by 0.3s**: At least one element visibly animating within 0.3s. Fast, snappy entrance (0.15-0.25s duration).
- **Audio hook**: First TTS sentence reinforces the visual hook. No preamble, no definitions, no "今天我们来了解".

## Palettes

Declare one background, one foreground, one accent before writing HTML.

| Category          | Use for                                       | File                                                       |
| ----------------- | --------------------------------------------- | ---------------------------------------------------------- |
| Bold / Energetic  | Product launches, social media, announcements | [palettes/bold-energetic.md](palettes/bold-energetic.md)   |
| Warm / Editorial  | Storytelling, documentaries, case studies     | [palettes/warm-editorial.md](palettes/warm-editorial.md)   |
| Dark / Premium    | Tech, finance, luxury, cinematic              | [palettes/dark-premium.md](palettes/dark-premium.md)       |
| Clean / Corporate | Explainers, tutorials, presentations          | [palettes/clean-corporate.md](palettes/clean-corporate.md) |
| Nature / Earth    | Sustainability, outdoor, organic              | [palettes/nature-earth.md](palettes/nature-earth.md)       |
| Neon / Electric   | Gaming, tech, nightlife                       | [palettes/neon-electric.md](palettes/neon-electric.md)     |
| Pastel / Soft     | Fashion, beauty, lifestyle, wellness          | [palettes/pastel-soft.md](palettes/pastel-soft.md)         |
| Jewel / Rich      | Luxury, events, sophisticated                 | [palettes/jewel-rich.md](palettes/jewel-rich.md)           |
| Monochrome        | Dramatic, typography-focused                  | [palettes/monochrome.md](palettes/monochrome.md)           |
| Shadow Cut        | Dark/epic/dramatic with tier selection        | [palettes/shadow-cut.md](palettes/shadow-cut.md)           |

Or derive from OKLCH — pick a hue, build bg/fg/accent at different lightnesses, tint everything toward that hue.
