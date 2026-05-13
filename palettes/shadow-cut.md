# Shadow Cut

Cinematic dark-mode palette with three intensity tiers: Dark (deep shadows), Epic (grand scale), Dramatic (high contrast theater).

Select a tier based on content theme — see `visual-styles.md` → Style 6: Shadow Cut for the selection matrix.

---

## Tier 1: Dark (深色)

Deep blacks, muted highlights, whispers of color. Feels enclosed, intimate, dangerous.

```
#0A0A0A #121212 #1E1E1E #2C2C2C #3A3A3A
#0D0D0D #1A1A2E #16213E #0F3460 #E94560
#0A0A0F #141422 #1F1F38 #2D2D55 #C4B5FD
#050505 #0B0C10 #1F2833 #45A29C #66FCF1
#0C0C0C #1A1A1A #333333 #C0C0C0 #F5F5F5
```

| Role | Value | Usage |
|---|---|---|
| Background | `#0A0A0A` | Near-black canvas |
| Surface | `#121212` / `#1E1E1E` | Cards, panels, subtle lift |
| Text primary | `#F5F5F5` | Headings — almost white |
| Text secondary | `#C0C0C0` | Body text, muted silver |
| Accent | `#E94560` (crimson) or `#66FCF1` (cyan) | Single color pop, sparingly |
| Shadow glow | `rgba(233,69,96,0.15)` | Card edge glow on hover |

---

## Tier 2: Epic (史诗感)

Deep navy base, gold and amber accents, sweeping gradients. Feels vast, ancient, powerful.

```
#020814 #0A1628 #14213D #1B3A5C #FCA311
#000000 #0D1B2A #1B263B #415A77 #E0E1DD
#001219 #005F73 #0A9396 #94D2BD #E9D8A6
#10002B #240046 #3C096C #5A189A #FF6D00
#000814 #001D3D #003566 #FFC300 #FFD60A
```

| Role | Value | Usage |
|---|---|---|
| Background | `#020814` → `#0A1628` | Deep navy radial gradient |
| Surface | `#14213D` / `#1B263B` | Card backgrounds, panels |
| Text primary | `#FFC300` (gold) or `#E0E1DD` (pale) | Titles glow gold, body is pale |
| Text secondary | `#415A77` | Muted annotations |
| Accent | `#FCA311` (amber) + `#FFC300` (gold) | Dual warm accent |
| Shadow glow | `rgba(252,163,17,0.2)` | Golden rim light on cards |
| Gradient accent | `linear-gradient(135deg, #FCA311, #FF6D00)` | Hero elements, buttons |

---

## Tier 3: Dramatic (戏剧性)

Stark black-white contrast, bold red/crimson slashes, theatrical lighting. Feels tense, confrontational, stage-lit.

```
#000000 #0A0A0A #1A1A1A #FFFFFF #F5F5F5
#000000 #141414 #DC2626 #EF4444 #FCA5A5
#000000 #0F0F0F #D4AF37 #FFD700 #FFF8DC
#050505 #1C1C1C #8B0000 #B91C1C #FEE2E2
#000000 #111111 #FF1744 #FF5252 #FFE0E0
```

| Role | Value | Usage |
|---|---|---|
| Background | `#000000` → `#0A0A0A` | Pure black with subtle gradient |
| Surface | `#141414` / `#1A1A1A` | Cards, raised surfaces |
| Text primary | `#FFFFFF` | Stark white — maximum contrast |
| Text secondary | `#A3A3A3` | Gray secondary |
| Accent | `#DC2626` (red) + `#D4AF37` (gold) | Red for danger/conflict, gold for grandeur |
| Slash line | `#DC2626` 2-3px | Diagonal accent lines, dividers |
| Shadow glow | `rgba(220,38,38,0.25)` | Red glow behind hero elements |
| Spot gradient | `radial-gradient(ellipse at 50% 0%, rgba(220,38,38,0.15), transparent 60%)` | Top-down spotlight effect |

---

## Shadow Cut Theme Selection Matrix

| Content Theme | Tier | Why |
|---|---|---|
| Horror / thriller / mystery | Dark | Enclosed shadows, minimal color = unease |
| Cybersecurity / hacking / dark web | Dark | Near-black + cyan accent = digital underworld |
| Space / cosmos / astrophysics | Epic | Deep navy + gold = cosmic vastness |
| History / mythology / ancient civilizations | Epic | Amber + navy = ancient grandeur |
| War / military / revolution | Epic | Gold on dark = honor and gravitas |
| Biography / life story / legacy | Dramatic | High contrast = spotlight on a subject |
| Conflict / debate / controversy | Dramatic | Red vs white = confrontation |
| Emotion / psychology / inner struggle | Dramatic | Light and shadow interplay = duality |
| Film / cinema / stage arts | Dramatic | Theatrical lighting = stage aesthetic |
| Noir / detective / crime | Dark | Shadows and whispers of crimson |
| Religion / philosophy / existential | Epic | Vast dark + golden light = the sublime |
| AI / deep tech / quantum computing | Dark | Minimal + single accent = futuristic precision |
