# Visual Styles

Named visual identities for different content types. Use these when the user specifies a style preference or when the content naturally fits one of these categories.

Read this file when the user wants a specific visual style or when re-structuring content in Step 3.

---

## Style 1: Deep Green Science (Default for Animation Mode)

| Property | Value |
|---|---|
| Background | `radial-gradient(ellipse at center, #1a3a2a 0%, #0a1628 100%)` |
| Text | `#e8f5e9` (light green-white) |
| Accent | `#4caf50` (green), `#81c784` (light green) |
| Cards | Semi-transparent `rgba(255,255,255,0.05)` with border `rgba(255,255,255,0.1)` |
| Icons | SVG line icons in `#4caf50` |
| Particles | Canvas particle system, 14-18 particles, slow drift |
| Noise | SVG `feTurbulence` subtle texture overlay |
| Best for | Technical deep-dives, RNN/LSTM, neural networks |

---

## Style 2: Clean Corporate (PPT Default)

| Property | Value |
|---|---|
| Background | White `#ffffff` or light gray `#f5f6fa` |
| Text | `#2d3436` (dark charcoal) |
| Accent | `#0984e3` (blue), `#6c5ce7` (purple) |
| Cards | White with `box-shadow: 0 2px 8px rgba(0,0,0,0.1)` |
| Gradients | Subtle blue-to-purple for title backgrounds |
| Best for | Business presentations, general education, concept explanations |

---

## Style 3: Warning Alert

| Property | Value |
|---|---|
| Background | Dark `#1a1a2e` with red pulse overlay |
| Text | `#ffffff` (white) |
| Accent | `#e74c3c` (red), `#ff6b6b` (light red) |
| Animations | `shake`, `explode`, `heartbeat`, `pulse` |
| Icons | Warning triangles, exclamation marks in red |
| Best for | Danger warnings, failure analysis, risk communication |

---

## Style 4: Code Lab

| Property | Value |
|---|---|
| Background | Dark `#0d1117` (GitHub dark) |
| Text | `#c9d1d9` (light gray) |
| Accent | `#58a6ff` (blue), `#7ee787` (green), `#f0883e` (orange) |
| Code blocks | `#161b22` background with syntax highlighting |
| Font | Monospace for code, sans-serif for explanations |
| Animations | Typewriter effect, code rain, terminal cursor |
| Best for | Programming tutorials, code demonstrations, technical walkthroughs |

---

## Style 5: Minimal Elegant

| Property | Value |
|---|---|
| Background | Clean white or `#fafafa` |
| Text | `#333333` |
| Accent | Single accent color (user's choice, default `#2d3436`) |
| Cards | Border-only, no fill |
| Typography | Large, generous spacing, centered |
| Animations | Subtle fade-in only, no flashy effects |
| Best for | Simple explanations, quotes, high-level overviews, 5-page-or-less presentations |

---

## Style 6: Shadow Cut (深色剪影风格)

A cinematic dark-mode system with three intensity tiers. Select the tier based on content theme — see the Theme → Tier matrix below.

Read `palettes/shadow-cut.md` for full color swatches and role assignments.

---

### Tier 1: Dark (深色) — Shadows and Whispers

| Property | Value |
|---|---|
| Background | `#0A0A0A` — near-black with subtle radial lift to `#121212` |
| Text | `#F5F5F5` (primary), `#C0C0C0` (secondary) |
| Accent | `#E94560` (crimson) or `#66FCF1` (cyan) — pick ONE per page |
| Cards | `#1E1E1E` with `1px solid rgba(255,255,255,0.06)` and subtle glow |
| Noise | SVG `feTurbulence` at low opacity (0.03-0.05) for film grain |
| Particles | Slow-drift motes, 6-10 particles, very low opacity (0.1-0.2) |
| Typography | Light weight headings (300-400), wide letter-spacing, uppercase labels |
| Animations | Slow fade-ins (0.6-1.0s), `sine.inOut`, `power1.out` — restrained |
| Transitions | Blur crossfade, focus pull — see `references/transitions.md` |
| Best for | Horror, thriller, mystery, cybersecurity, dark tech, noir |

---

### Tier 2: Epic (史诗感) — Vast and Golden

| Property | Value |
|---|---|
| Background | `radial-gradient(ellipse at 50% 30%, #0A1628 0%, #020814 100%)` |
| Text | `#FFC300` (gold titles), `#E0E1DD` (pale body) |
| Accent | `#FCA311` (amber) + `#FFC300` (gold) — warm dual accent |
| Cards | `#14213D` with `1px solid rgba(252,163,17,0.15)` and golden rim glow |
| Decorative | Canvas star field or floating golden particles (10-16), slow pulse |
| Noise | SVG `feTurbulence` subtle texture + golden vignette overlay |
| Typography | Serif for titles (Cinzel, Playfair), sans-serif for body, generous spacing |
| Animations | Grand scale-ins (0.8-1.5s), `expo.out`, `power3.out` — majestic |
| Transitions | Zoom through, circle iris, light leak — see `references/transitions.md` |
| Best for | History, mythology, space, war, ancient civilizations, religion, philosophy |

---

### Tier 3: Dramatic (戏剧性) — Spotlight and Contrast

| Property | Value |
|---|---|
| Background | `#000000` with `radial-gradient` top-down spotlight in crimson or white |
| Text | `#FFFFFF` (primary), `#A3A3A3` (secondary) — maximum contrast |
| Accent | `#DC2626` (red) + `#D4AF37` (gold) — red for conflict, gold for grandeur |
| Cards | `#141414` with red or gold border accent, `box-shadow` glow |
| Decorative | Diagonal slash lines (2-3px red), spot gradient overlays |
| Noise | Optional — keep backgrounds clean for maximum impact |
| Typography | Heavy weight (700-900), condensed or display fonts, tight tracking |
| Animations | Sharp snaps (0.15-0.3s), `power4.in`, `back.out(1.7)` — punchy, decisive |
| Transitions | Glitch, chromatic aberration, gravity drop — see `references/transitions.md` |
| Best for | Biography, conflict, debate, emotion, psychology, cinema, stage arts |

---

## Shadow Cut Theme → Tier Selection

| Content Theme | Tier | Key Traits |
|---|---|---|
| Horror / thriller / mystery | Dark | Enclosed shadows, minimal color, slow reveals |
| Cybersecurity / hacking | Dark | Near-black + single cyan accent, digital precision |
| AI / deep tech / quantum | Dark | Minimal + futuristic, clean geometric |
| Noir / detective / crime | Dark | Shadow play, crimson whispers |
| Space / cosmos / astrophysics | Epic | Deep navy + gold, cosmic vastness, star particles |
| History / mythology / ancient | Epic | Amber + navy, serif titles, ancient grandeur |
| War / military / revolution | Epic | Gold on dark, honor and gravitas, sweeping motion |
| Religion / philosophy / existential | Epic | Vast dark + golden light, the sublime |
| Biography / life story / legacy | Dramatic | Spotlight effect, high contrast, theatrical |
| Conflict / debate / controversy | Dramatic | Red vs white, confrontation, punchy animations |
| Emotion / psychology / struggle | Dramatic | Light and shadow interplay, duality |
| Film / cinema / stage arts | Dramatic | Stage lighting, slash lines, bold typography |

---

## Style Selection Matrix

| Content Type | Recommended Style |
|---|---|
| Neural networks / AI internals | Deep Green Science |
| Business / general education | Clean Corporate |
| Security / failure / risk | Warning Alert |
| Programming / code | Code Lab |
| Quick overview / summary | Minimal Elegant |
| Comparison / debate | Clean Corporate (with dual-color cards) |
| Historical / timeline | Clean Corporate (with flowchart elements) |
| Horror / thriller / mystery | Shadow Cut: Dark |
| Cybersecurity / hacking / dark tech | Shadow Cut: Dark |
| Space / cosmos / astrophysics | Shadow Cut: Epic |
| History / mythology / ancient | Shadow Cut: Epic |
| War / military / revolution | Shadow Cut: Epic |
| Biography / life story | Shadow Cut: Dramatic |
| Conflict / debate (theatrical) | Shadow Cut: Dramatic |
| Emotion / psychology / inner struggle | Shadow Cut: Dramatic |
| Film / cinema / stage arts | Shadow Cut: Dramatic |
