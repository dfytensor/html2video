# Science/Tech Themed Icon Sets

Read this file when generating HTML for chemistry, biology, hardware, energy, finance, weather, or industry themed content.

---

## Setup

```bash
python scripts/download-themed-icons.py --test
```

Downloads 55 SVG icons to `assets/icons/{category}/` and generates `test-themed-icons.html`.

---

## Catalog (55 icons, 7 categories)

### Usage Pattern

```html
<img src="assets/icons/chemistry/flask.svg"
     alt="烧瓶" style="width:64px;height:64px;filter:invert(1);">
```

On dark backgrounds, use `filter:invert(1)` to convert black SVG to white.

For color tinting:
```css
/* Blue tint for chemistry */
filter: invert(1) sepia(1) saturate(5) hue-rotate(180deg);
/* Green tint for biology */
filter: invert(1) sepia(1) saturate(5) hue-rotate(90deg);
/* Red tint for finance */
filter: invert(1) sepia(1) saturate(5) hue-rotate(330deg);
```

---

### Chemistry (化学) — 8 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `chemical-drop` | 化学液滴 | game-icons.net |
| `chemical-arrow` | 反应箭头 | game-icons.net |
| `acid` | 酸液 | hand-crafted |
| `flask` | 烧瓶 | game-icons.net |
| `bubbling-flask` | 冒泡烧瓶 | game-icons.net |
| `test-tubes` | 试管 | game-icons.net |
| `beaker` | 烧杯 | hand-crafted |
| `molecule` | 分子 | hand-crafted |

### Biology (生物) — 7 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `dna` | DNA双螺旋 | hand-crafted |
| `cell` | 细胞 | hand-crafted |
| `microscope` | 显微镜 | hand-crafted |
| `seedling` | 幼苗 | hand-crafted |
| `flower` | 花朵 | game-icons.net |
| `autism` | 基因 | hand-crafted |
| `heartbeat` | 心跳 | hand-crafted |

### Hardware (硬件) — 9 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `cpu-shot` | CPU | game-icons.net |
| `processor` | 处理器 | game-icons.net |
| `motherboard` | 主板 | hand-crafted |
| `ram-rows` | 内存 | hand-crafted |
| `hard-drive` | 硬盘 | hand-crafted |
| `desktop` | 台式机 | hand-crafted |
| `laptop` | 笔记本 | hand-crafted |
| `router` | 路由器 | hand-crafted |
| `server-rack` | 服务器 | hand-crafted |

### Energy (能源) — 8 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `nuclear-plant` | 核能 | hand-crafted |
| `solar-power` | 太阳能 | hand-crafted |
| `battery-pack` | 电池 | hand-crafted |
| `electric` | 电力 | game-icons.net |
| `fire-flower` | 火力 | hand-crafted |
| `water-drop-energy` | 水力 | hand-crafted |
| `wind-turbine` | 风力 | hand-crafted |
| `oil-rig` | 石油 | hand-crafted |

### Finance (金融) — 8 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `chart-up` | 上涨 | hand-crafted |
| `chart-down` | 下跌 | hand-crafted |
| `coins` | 金币 | hand-crafted |
| `money-stack` | 资金 | hand-crafted |
| `bank` | 银行 | hand-crafted |
| `safe` | 保险箱 | hand-crafted |
| `candlestick` | K线图 | hand-crafted |
| `exchange` | 汇率 | hand-crafted |

### Weather (气象) — 7 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `typhoon` | 台风 | hand-crafted |
| `earthquake` | 地震 | hand-crafted |
| `satellite` | 卫星 | hand-crafted |
| `thermometer` | 温度计 | hand-crafted |
| `rain` | 降雨 | hand-crafted |
| `snowflake` | 降雪 | hand-crafted |
| `tornado` | 龙卷风 | hand-crafted |

### Industry (工业) — 8 icons

| Key | Chinese | Source |
|-----|---------|--------|
| `gears` | 齿轮组 | hand-crafted |
| `robot-antenna` | 工业机器人 | hand-crafted |
| `conveyor` | 流水线 | hand-crafted |
| `factory` | 工厂 | hand-crafted |
| `wrench` | 扳手 | game-icons.net |
| `assembly` | 装配 | game-icons.net |
| `3d-hammer` | 锤子 | hand-crafted |
| `mining` | 采矿 | hand-crafted |

---

## Emoji → Themed Icon Mapping

| Emoji | Icon | Category |
|-------|------|----------|
| 🧪 | `flask` / `test-tubes` | chemistry |
| 🔬 | `microscope` | biology |
| 🧬 | `dna` | biology |
| 🦠 | `cell` | biology |
| 💻 | `laptop` | hardware |
| 🖥️ | `desktop` | hardware |
| 💾 | `hard-drive` | hardware |
| 🔌 | `electric` | energy |
| ⚡ | `battery-pack` | energy |
| ☢️ | `nuclear-plant` | energy |
| ☀️ | `solar-power` | energy |
| 💰 | `coins` / `money-stack` | finance |
| 📈 | `chart-up` | finance |
| 📉 | `chart-down` | finance |
| 🏦 | `bank` | finance |
| 🌪️ | `typhoon` / `tornado` | weather |
| 🌧️ | `rain` | weather |
| ❄️ | `snowflake` | weather |
| 🌡️ | `thermometer` | weather |
| 🛰️ | `satellite` | weather |
| ⚙️ | `gears` / `assembly` | industry |
| 🏭 | `factory` | industry |
| 🤖 | `robot-antenna` | industry |

---

## GSAP Animation Examples

```javascript
// DNA rotation
gsap.to(".dna-icon", { rotation: 360, duration: 10, repeat: -1, ease: "none" });

// Heartbeat pulse
gsap.to(".heartbeat-icon", { scale: 1.2, duration: 0.3, repeat: -1, yoyo: true, ease: "power1.inOut" });

// Chart line draw
tl.from(".chart-icon", { scaleX: 0, transformOrigin: "left center", duration: 0.8, ease: "power2.out" });

// Gears spin
gsap.to(".gears-icon", { rotation: 360, duration: 4, repeat: -1, ease: "none" });

// Tornado rotation
gsap.to(".tornado-icon", { rotation: 720, duration: 3, repeat: -1, ease: "none" });

// Battery charging
gsap.fromTo(".battery-icon", { clipPath: "inset(50% 0 0 0)" }, { clipPath: "inset(0% 0 0 0)", duration: 1.5, ease: "power2.out" });
```

---

## Source & License

| Source | License | Icons |
|--------|---------|-------|
| game-icons.net (Lorc) | CC BY 3.0 | 12 icons |
| Hand-crafted | CC0 | 43 icons |

---

## Script Commands

```bash
python scripts/download-themed-icons.py --test           # download all + test HTML
python scripts/download-themed-icons.py --list           # list all
python scripts/download-themed-icons.py --category chemistry  # one category
python scripts/download-themed-icons.py --force          # re-download
python scripts/download-themed-icons.py --html-only      # generate HTML only
```
