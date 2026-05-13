# Cultivation / Xianxia Icon Set

Read this file when generating HTML for cultivation (修仙), xianxia (仙侠), wuxia (武侠), or fantasy (玄幻) themed content.

---

## Setup

```bash
python scripts/download-cultivation-icons.py --test
```

Downloads 43 SVG icons to `assets/icons/cultivation/` and generates a test page at `test-cultivation-icons.html`.

---

## Icon Catalog (43 icons, 8 categories)

### Usage Pattern

```html
<img src="assets/icons/cultivation/cauldron.svg"
     alt="丹炉" style="width:64px;height:64px;filter:invert(1);">
```

Use `filter:invert(1)` on dark backgrounds to convert black SVG to white. Or override `fill`:

```html
<img src="assets/icons/cultivation/fire.svg"
     alt="火" style="width:48px;height:48px;filter:invert(1) sepia(1) saturate(5) hue-rotate(0deg);">
```

### Inline SVG (for color control and animation)

```javascript
fetch("assets/icons/cultivation/lotus.svg")
  .then(r => r.text())
  .then(svg => {
    document.getElementById("icon-container").innerHTML = svg;
    document.querySelector("#icon-container svg path").setAttribute("fill", "#8b5cf6");
  });
```

---

### Weapon (武器) — 4 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `crossed-swords` | 双剑 | 交叉双剑 | game-icons.net/lorc (CC BY 3.0) |
| `sword-wound` | 剑伤 | 剑击伤痕 | game-icons.net/lorc (CC BY 3.0) |
| `pointy-sword` | 尖剑 | 尖头长剑 | game-icons.net/lorc (CC BY 3.0) |
| `hook-swords` | 钩剑 | 双钩, 武术兵器 | hand-crafted |

### Alchemy (炼丹) — 5 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `cauldron` | 丹炉 | 炼丹炉/坩埚 | game-icons.net/lorc (CC BY 3.0) |
| `potion-ball` | 丹药 | 圆球形丹药 | game-icons.net/lorc (CC BY 3.0) |
| `drink-me` | 灵液 | 药瓶/灵液 | game-icons.net/lorc (CC BY 3.0) |
| `bubbling-flask` | 灵瓶 | 冒泡的药瓶 | game-icons.net/lorc (CC BY 3.0) |
| `round-bottom-flask` | 炼药瓶 | 圆底烧瓶 | game-icons.net/lorc (CC BY 3.0) |

### Nature (自然) — 6 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `lotus-flower` | 莲花 | 莲花, 佛教/修仙象征 | game-icons.net/lorc (CC BY 3.0) |
| `lotus` | 莲 | 睡莲/冥想莲 | game-icons.net/lorc (CC BY 3.0) |
| `mushroom` | 灵芝 | 蘑菇/灵芝 | game-icons.net/lorc (CC BY 3.0) |
| `sun` | 太阳 | 太阳/阳 | game-icons.net/lorc (CC BY 3.0) |
| `crescent-moon` | 弯月 | 新月/阴 | hand-crafted |
| `mountains` | 群山 | 连绵山脉 | game-icons.net/lorc (CC BY 3.0) |

### Beast (灵兽) — 5 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `dragon-head` | 龙头 | 龙头/龙族 | game-icons.net/lorc (CC BY 3.0) |
| `dragon-breath` | 龙息 | 龙吐息/龙焰 | game-icons.net/lorc (CC BY 3.0) |
| `phoenix-flaming` | 凤凰 | 浴火凤凰 | hand-crafted |
| `snake` | 蛇 | 蛇/蛟龙前身 | game-icons.net/lorc (CC BY 3.0) |
| `tortoise` | 玄武 | 龟/玄武 | hand-crafted |

### Element (五行) — 5 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `fire` | 火 | 火焰 | hand-crafted |
| `water-drop` | 水 | 水滴 | hand-crafted |
| `lightning-frequency` | 雷 | 雷电/天劫 | game-icons.net/lorc (CC BY 3.0) |
| `thunderball` | 雷球 | 雷球/雷劫 | game-icons.net/lorc (CC BY 3.0) |
| `windmill` | 风 | 风/风元素 | hand-crafted |

### Spiritual (修为) — 6 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `meditation` | 打坐 | 冥想/打坐修炼 | game-icons.net/lorc (CC BY 3.0) |
| `aura` | 灵气 | 光环/灵气外放 | game-icons.net/lorc (CC BY 3.0) |
| `telepathy` | 神识 | 心电感应/神识传音 | game-icons.net/lorc (CC BY 3.0) |
| `portal` | 传送门 | 传送门/秘境入口 | game-icons.net/lorc (CC BY 3.0) |
| `energy-shield` | 护体真气 | 能量护盾 | game-icons.net/lorc (CC BY 3.0) |
| `yin-yang` | 阴阳 | 阴阳太极 | hand-crafted |

### Treasure (宝物) — 8 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `crystal-cluster` | 灵石 | 水晶簇/灵石矿 | game-icons.net/lorc (CC BY 3.0) |
| `crystal-bars` | 灵晶 | 灵晶/晶体 | game-icons.net/lorc (CC BY 3.0) |
| `diamond-hard` | 钻石 | 钻石/坚硬法器 | game-icons.net/lorc (CC BY 3.0) |
| `gem-chain` | 灵珠 | 灵珠链 | game-icons.net/lorc (CC BY 3.0) |
| `scroll-unfurled` | 功法卷轴 | 展开的卷轴/功法 | game-icons.net/lorc (CC BY 3.0) |
| `tied-scroll` | 密封卷轴 | 封印的卷轴/秘籍 | game-icons.net/lorc (CC BY 3.0) |
| `star-prominences` | 星辰 | 星辰之力/星宿 | game-icons.net/lorc (CC BY 3.0) |
| `beams-aurora` | 极光 | 极光/天象异变 | hand-crafted |

### Body (肉身) — 4 icons

| Key | Chinese | Description | Source |
|-----|---------|-------------|--------|
| `bleeding-eye` | 天眼 | 血眼/天眼 | game-icons.net/lorc (CC BY 3.0) |
| `half-heart` | 道心 | 半心/道心 | game-icons.net/lorc (CC BY 3.0) |
| `chained-heart` | 锁心 | 锁链之心/心魔 | game-icons.net/lorc (CC BY 3.0) |
| `shield-echoes` | 护盾 | 回声护盾 | game-icons.net/lorc (CC BY 3.0) |

---

## Emoji → Cultivation Icon Mapping

| Emoji | Meaning | Cultivation Icon |
|-------|---------|-----------------|
| ⚔️ | 战斗 | `crossed-swords` |
| 🔥 | 火焰 | `fire` |
| 💧 | 水 | `water-drop` |
| ⚡ | 雷电/天劫 | `lightning-frequency` |
| 🌪️ | 风 | `windmill` |
| 🐉 | 龙 | `dragon-head` |
| 🦅 | 凤凰 | `phoenix-flaming` |
| 🐢 | 玄武 | `tortoise` |
| 🐍 | 蛇/蛟 | `snake` |
| 🌸 | 莲花 | `lotus-flower` |
| 🍄 | 灵芝 | `mushroom` |
| 💊 | 丹药 | `potion-ball` |
| 🏔️ | 山脉/仙山 | `mountains` |
| 🌙 | 月/阴 | `crescent-moon` |
| ☀️ | 太阳/阳 | `sun` |
| ☯️ | 阴阳 | `yin-yang` |
| 💎 | 灵石/灵晶 | `crystal-cluster` |
| 📜 | 功法/秘籍 | `scroll-unfurled` |
| 🧘 | 打坐修炼 | `meditation` |
| 👁️ | 天眼 | `bleeding-eye` |
| 🌀 | 传送门 | `portal` |
| ⭐ | 星辰 | `star-prominences` |
| 💗 | 道心 | `half-heart` |

---

## GSAP Animation Examples

```javascript
// Sword slash entrance
tl.from(".sword-icon", {
  rotation: -45, scale: 0, opacity: 0,
  duration: 0.5, ease: "back.out(1.7)"
}, 0.2);

// Lotus bloom
tl.from(".lotus-icon", {
  scale: 0, rotation: 180, opacity: 0,
  duration: 0.8, ease: "elastic.out(1, 0.5)"
}, 0.1);

// Fire flicker
gsap.to(".fire-icon", {
  scale: 1.05, duration: 0.3, repeat: -1,
  yoyo: true, ease: "power1.inOut"
});

// Thunder strike
tl.from(".thunder-icon", {
  scaleY: 0, transformOrigin: "top center",
  duration: 0.2, ease: "power4.out"
}, 0.1);

// Dragon breath pulse
gsap.to(".dragon-icon", {
  filter: "drop-shadow(0 0 12px #f97316)",
  duration: 0.8, repeat: -1, yoyo: true
});

// Meditation aura expand
tl.from(".meditation-icon", {
  scale: 0.5, opacity: 0,
  duration: 1.2, ease: "power2.out"
}, 0.1);
gsap.to(".meditation-icon", {
  scale: 1.05, duration: 3, repeat: -1,
  yoyo: true, ease: "sine.inOut"
});

// Yin-yang rotate
gsap.to(".yinyang-icon", {
  rotation: 360, duration: 8,
  repeat: -1, ease: "none"
});
```

---

## Source & License

| Source | License | Icons |
|--------|---------|-------|
| game-icons.net (Lorc) | CC BY 3.0 | 34 icons |
| Hand-crafted | CC0 | 9 icons |

Attribution for game-icons.net: "Icons by Lorc, CC BY 3.0, https://game-icons.net/"

---

## Script Commands

```bash
# Download all icons + generate test HTML
python scripts/download-cultivation-icons.py --test

# List all icons
python scripts/download-cultivation-icons.py --list

# Download specific category
python scripts/download-cultivation-icons.py --category weapon

# Re-download (force overwrite)
python scripts/download-cultivation-icons.py --force

# Generate test HTML only (icons must already exist)
python scripts/download-cultivation-icons.py --html-only
```
