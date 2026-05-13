# Typography

Read this file when generating HTML content that will be rendered as slides or exported to video.

---

## Banned Fonts

Training-data defaults that produce monoculture. Do NOT use:

Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne

**Syne in particular** is the most overused "distinctive" display font. It is an instant AI design tell.

---

## Guardrails

- **Don't pair two sans-serifs.** Cross the boundary: serif + sans, or sans + mono.
- **One expressive font per scene.** One performs, one recedes.
- **Weight contrast must be extreme.** Video needs 300 vs 900, not 400 vs 700. The difference must be visible in motion at a glance.
- **Video sizes, not web sizes.** Body: 20px minimum. Headlines: 60px+. Data labels: 16px. You will try to use 14px. Don't.

---

## Selection Thinking

Don't pick fonts by category reflex (editorial → serif, tech → mono, modern → geometric sans). That's pattern matching, not design.

1. **Name the register.** What voice is the content speaking in? Institutional authority? Personal confession? Technical precision? Casual irreverence? The register narrows the field more than the category.
2. **Think physically.** Imagine the font as a physical object — a museum exhibit caption, a hand-painted shop sign, a 1970s mainframe terminal manual, a fabric label inside a coat. Whichever physical object fits the register is pointing at the right _kind_ of typeface.
3. **Reject your first instinct.** The first font that feels right is usually your training-data default for that register. If you picked it last time too, find something else.
4. **Cross-check the assumption.** An editorial brief does NOT need a serif. A technical brief does NOT need a sans. The most distinctive choice often contradicts the category expectation.

---

## Similar-Font Pairing

Never pair two fonts that are similar but not identical — two geometric sans-serifs, two transitional serifs, two humanist sans. They create visual friction without clear hierarchy. The viewer senses something is "off" but can't articulate it. Either use one font at two weights, or pair fonts that contrast on multiple axes: serif + sans, condensed + wide, geometric + humanist.

---

## Chinese Font Pairing

For Chinese-language content (this skill's primary audience):

| Role | Recommended Fonts | Fallback |
|---|---|---|
| Headings | `PingFang SC`, `Microsoft YaHei UI`, `Noto Sans SC` weight 700-900 | `sans-serif` |
| Body | `PingFang SC`, `Microsoft YaHei`, `Noto Sans SC` weight 400-500 | `sans-serif` |
| Code/mono | `Source Code Pro`, `JetBrains Mono`, `Fira Code` | `monospace` |
| Accent/number | `DIN Alternate`, `Oswald`, `Barlow Condensed` | `sans-serif` |

**Font stack example:**
```css
body {
  font-family: "PingFang SC", "Microsoft YaHei UI", "Noto Sans SC", sans-serif;
}
.code-block {
  font-family: "Source Code Pro", "Fira Code", monospace;
}
.stat-number {
  font-family: "Oswald", "Barlow Condensed", "PingFang SC", sans-serif;
}
```

---

## Sizing for Video

| Element | Minimum | Recommended | Notes |
|---|---|---|---|
| Slide title | 32px | 40-56px | Bold, high contrast |
| Subtitle | 24px | 28-36px | Semi-bold |
| Body text | 18px | 20-28px | Regular |
| Caption/annotation | 14px | 16-20px | Monospace for code |
| Data/stat number | 36px | 48-72px | Heavy weight |
| TTS narration text | 16px | 20-24px | Readable on screen |

**Fixed reading time:** 3 seconds on screen = must be readable in 2. Fewer words, larger type.

---

## Emphasis Techniques for Video

| Technique | CSS | When to use |
|---|---|---|
| **Bold** | `font-weight: 700-900` | Key terms, definitions |
| **Underline** | `text-decoration: underline; text-decoration-color: accent` | Critical points |
| **Color highlight** | `color: accent` or `background-color` strip | Keywords, emphasis |
| **Italic** | `font-style: italic` | Foreign terms, emphasis |
| **Scale up** | `font-size: 1.2em` | Numbers, stats |
| **Background strip** | `background: linear-gradient(transparent 60%, accent 60%)` | Key phrases |
| **Monospace** | `font-family: monospace` | Code, technical terms |

---

## OpenType Features for Data

Most fonts ship with OpenType features that are off by default. Turn them on for data compositions:

```css
/* Tabular numbers — digits align vertically in columns */
.stat-value,
.timer,
.data-column {
  font-variant-numeric: tabular-nums;
}

/* Diagonal fractions — renders 1/2 as ½ */
.recipe-amount,
.ratio {
  font-variant-numeric: diagonal-fractions;
}

/* Small caps for abbreviations — less visual shouting */
.abbreviation,
.unit {
  font-variant-caps: all-small-caps;
}

/* Disable ligatures in code — fi, fl, ffi should stay separate */
code,
.code {
  font-variant-ligatures: none;
}
```

`tabular-nums` is essential any time numbers are stacked vertically — stat callouts, timers, scoreboards, data tables. Without it, digits have proportional widths and columns don't align.

---

## Dark Background Compensation

Light text on dark backgrounds creates optical illusions:

- **Increased apparent weight.** Light-on-dark reads heavier than dark-on-light at the same `font-weight`. Use 350 instead of 400 for body text. Headlines are less affected because size compensates.
- **Tighter apparent spacing.** Light halos around letterforms reduce perceived gaps. Increase `line-height` by 0.05-0.1 beyond your light-background value. For display sizes, add 0.01em `letter-spacing` to counteract.

```css
.dark-bg {
  color: #e8f5e9;
  font-weight: 350;
  line-height: 1.6;
  letter-spacing: 0.01em;
}
```

---

## Tracking for Video

- Display text (48px+): `-0.03em` to `-0.05em` (tighter than web)
- Body text (18-28px): `0` to `0.01em`
- Video encoding compresses letter detail, so tighter tracking reads better.

---

## Finding Fonts

Save this script to `/tmp/fontquery.py` and run with `curl -s 'https://fonts.google.com/metadata/fonts' > /tmp/gfonts.json && python3 /tmp/fontquery.py /tmp/gfonts.json`:

```python
import json, sys, random
from collections import OrderedDict

random.seed()

with open(sys.argv[1]) as f:
    data = json.load(f)
fonts = data.get("familyMetadataList", [])

ban = {"Inter","Roboto","Open Sans","Noto Sans","Lato","Poppins","Source Sans 3",
       "PT Sans","Nunito","Outfit","Sora","Playfair Display","Cormorant Garamond",
       "Bodoni Moda","EB Garamond","Cinzel","Prata","Arimo","Source Sans Pro","Syne"}
skip_pfx = ("Roboto","Noto ","Google Sans","Bpmf","Playwrite","Anek","BIZ ",
            "Nanum","Shippori","Sawarabi","Zen ","Kaisei","Kiwi ","Yuji ","Radio ")

def ok(f):
    if f["family"] in ban: return False
    if any(f["family"].startswith(b) for b in skip_pfx): return False
    if "latin" not in (f.get("subsets") or []): return False
    return True

seen = set()
R = OrderedDict()

R["Trending Sans"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") in ("Sans Serif","Display") and f.get("dateAdded","") >= "2022-01-01" and f.get("popularity",9999) < 300:
        R["Trending Sans"].append(f); seen.add(f["family"])

R["Trending Serif"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Serif" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Trending Serif"].append(f); seen.add(f["family"])

R["Monospace"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Monospace" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Monospace"].append(f); seen.add(f["family"])

R["Impact & Condensed"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    has_heavy = any(k in list(f.get("fonts",{}).keys()) for k in ("800","900"))
    is_display = f.get("category") in ("Sans Serif","Display")
    if has_heavy and is_display and f.get("popularity",9999) < 400:
        R["Impact & Condensed"].append(f); seen.add(f["family"])

R["Script & Handwriting"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Handwriting" and f.get("popularity",9999) < 300:
        R["Script & Handwriting"].append(f); seen.add(f["family"])

for cat in R:
    R[cat].sort(key=lambda x: x.get("popularity",9999))
    top5 = R[cat][:5]
    rest = R[cat][5:]
    random.shuffle(top5)
    R[cat] = top5 + rest
limits = {"Trending Sans":15,"Trending Serif":12,"Monospace":8,
          "Impact & Condensed":12,"Script & Handwriting":10}
for cat in R:
    items = R[cat][:limits.get(cat,10)]
    if not items: continue
    print(f"--- {cat} ({len(items)}) ---")
    for ff in items:
        var = "VAR" if ff.get("axes") else "   "
        print(f'  {ff.get("popularity"):4d} | {var} | {ff["family"]}')
    print()
```

Five categories: trending sans, trending serif, monospace, impact/condensed, script/handwriting. All dynamically filtered from Google Fonts metadata — no hardcoded font names. Cross classification boundaries when pairing.
