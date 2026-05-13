# Text Animation Effects

Read this file when generating animated text for titles, hooks, section headers, or standalone text slides.

Source: inspired by [svganimate.ai](https://svganimate.ai/zh/tools/text-svg-animation) prompt patterns.

---

## Prompt Formula

Every text animation prompt should include:

```
Subject (text content) + Action (animation type) + Details (duration, easing, color, timing)
```

**Bad:** "让标题有动画"  
**Good:** "标题'道生一'从左滑入，0.4s，expo.out，每个字延迟0.08s，金色#FFBE0B"

---

## Effect Catalog

### 1. Typewriter (打字机)

Characters appear one by one with a blinking cursor.

```javascript
var text = "Hello, World!";
var el = document.getElementById("typewriter-target");
var tl = gsap.timeline({ paused: true });
tl.set(el, { textContent: "" });
for (var i = 0; i < text.length; i++) {
  tl.set(el, { textContent: text.substring(0, i + 1) }, i * 0.06);
}
tl.to({}, { duration: 0.6, repeat: 2 }); // blink pause
```

Or use GSAP TextPlugin:
```javascript
tl.to("#typewriter-target", {
  text: { value: "Hello, World!", delimiter: "" },
  duration: 1.2,
  ease: "none"
}, 0.2);
```

**Best for:** Slide titles, code display, hook cover text.  
**Timing:** 0.04-0.08s per character. Chinese characters 0.08-0.12s each.

---

### 2. Glitch (故障/毛刺)

Text flickers, shifts, and distorts with color channel separation.

```css
.glitch-text {
  position: relative;
  font-size: 64px;
  font-weight: 900;
  color: #fff;
}
.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
.glitch-text::before { color: #ff0040; clip-path: inset(0 0 60% 0); }
.glitch-text::after { color: #00ffff; clip-path: inset(40% 0 0 0); }
```

```javascript
var tl = gsap.timeline({ repeat: -1, repeatDelay: 3 });
tl.to(".glitch-text::before", {
  x: gsap.utils.wrap([-4, 4, -2, 3, 0]),
  duration: 0.1,
  repeat: 5,
  ease: "steps(1)"
}, 0);
tl.to(".glitch-text::after", {
  x: gsap.utils.wrap([3, -3, 2, -4, 0]),
  duration: 0.1,
  repeat: 5,
  ease: "steps(1)"
}, 0.05);
```

**Best for:** Tech/cyberpunk themes, warning slides, dramatic reveals.  
**Duration:** 0.4-0.8s glitch burst, then 3-5s calm before next burst.

---

### 3. Wave (波浪)

Each character oscillates vertically in a sine wave pattern.

```javascript
var text = "波浪文字动画";
var container = document.getElementById("wave-target");
text.split("").forEach(function(char, i) {
  var span = document.createElement("span");
  span.textContent = char;
  span.style.display = "inline-block";
  container.appendChild(span);
  gsap.to(span, {
    y: -20,
    duration: 0.6,
    ease: "sine.inOut",
    repeat: -1,
    yoyo: true,
    delay: i * 0.08
  });
});
```

**Best for:** Energetic titles, playful content, wave/water themes.  
**Timing:** 0.06-0.1s stagger, 0.5-0.8s per oscillation, y offset 15-25px.

---

### 4. Stroke Draw (描边绘制)

Text outline draws itself from left to right, then fills with color.

```css
.stroke-draw {
  font-size: 80px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 2px var(--accent);
  stroke-dasharray: 100%;
  stroke-dashoffset: 100%;
}
```

```javascript
var tl = gsap.timeline({ paused: true });
tl.to(".stroke-draw", {
  strokeDashoffset: 0,
  duration: 1.5,
  ease: "power2.out",
  // Then fill
  onComplete: function() {
    gsap.to(".stroke-draw", { color: "var(--accent)", duration: 0.4, ease: "power2.out" });
  }
}, 0.2);
```

Alternative with SVG `<text>`:
```html
<svg viewBox="0 0 800 120">
  <text x="50%" y="80" text-anchor="middle" font-size="80" font-weight="900"
        fill="none" stroke="#a78bfa" stroke-width="2"
        stroke-dasharray="2000" stroke-dashoffset="2000"
        class="draw-text">
    道生一
  </text>
</svg>
```
```javascript
tl.to(".draw-text", { strokeDashoffset: 0, duration: 2, ease: "power2.out" }, 0.1);
tl.to(".draw-text", { fill: "#a78bfa", duration: 0.5 }, 1.8);
```

**Best for:** Elegant reveals, calligraphy themes, cultivation/traditional content.  
**Duration:** 1.5-2.5s draw + 0.3-0.5s fill. Use `power2.out` or `circ.out`.

---

### 5. Neon Glow (霓虹灯)

Text glows with a pulsating neon light effect.

```css
.neon-text {
  font-size: 72px;
  font-weight: 900;
  color: #fff;
  text-shadow:
    0 0 7px #fff,
    0 0 10px #fff,
    0 0 21px #fff,
    0 0 42px #a78bfa,
    0 0 82px #a78bfa,
    0 0 92px #a78bfa;
}
```

```javascript
var glow = { intensity: 0 };
gsap.to(glow, {
  intensity: 1,
  duration: 1.5,
  repeat: -1,
  yoyo: true,
  ease: "sine.inOut",
  onUpdate: function() {
    var blur = 7 + glow.intensity * 40;
    document.querySelector(".neon-text").style.textShadow =
      "0 0 7px #fff, 0 0 " + blur + "px #a78bfa, 0 0 " + (blur * 2) + "px #a78bfa";
  }
});
```

**Best for:** Night/urban themes, gaming, cyberpunk, neon-electric palette.  
**Duration:** 1.5-3s per pulse cycle. Match to beat if audio-reactive.

---

### 6. Bounce In (弹跳入场)

Characters drop in from above with elastic bounce.

```javascript
var text = "弹跳入场";
var container = document.getElementById("bounce-target");
text.split("").forEach(function(char, i) {
  var span = document.createElement("span");
  span.textContent = char;
  span.style.display = "inline-block";
  container.appendChild(span);
  gsap.from(span, {
    y: -80,
    opacity: 0,
    duration: 0.6,
    ease: "back.out(1.7)",
    delay: 0.1 + i * 0.06
  });
});
```

**Best for:** Energetic hooks, game-style content, bold-energetic palette.  
**Timing:** 0.05-0.08s stagger, `back.out(1.5-2.0)` easing, y offset 60-100px.

---

### 7. Scale Pop (缩放弹入)

Text scales from 0 to full size with overshoot.

```javascript
tl.from(".pop-text", {
  scale: 0,
  opacity: 0,
  rotation: -5,
  duration: 0.4,
  ease: "back.out(2)",
  transformOrigin: "center center"
}, 0.1);
```

**Best for:** Hook cover hero text, numbers/stats, dramatic reveals.  
**Duration:** 0.3-0.5s. Use `back.out(1.5-2.5)` for punchy feel.

---

### 8. Slide + Fade (滑入淡入)

Classic entrance: slide from edge with simultaneous fade.

```javascript
// From left
tl.from(".slide-text", { x: -60, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.2);
// From bottom
tl.from(".slide-up-text", { y: 40, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.3);
// From right
tl.from(".slide-right-text", { x: 60, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.4);
```

**Best for:** Body text, subtitles, section titles. Default entrance for most text.  
**Duration:** 0.4-0.6s. Offset 15-60px from direction of travel.

---

### 9. Rotate In (旋转入场)

Text rotates in from an angle while scaling up.

```javascript
tl.from(".rotate-text", {
  rotation: -15,
  scale: 0.8,
  opacity: 0,
  duration: 0.5,
  ease: "power3.out",
  transformOrigin: "left center"
}, 0.2);
```

**Best for:** Badge/tag labels, emphasized keywords, accent text.  
**Duration:** 0.4-0.6s, rotation 10-20 degrees, scale from 0.7-0.9.

---

### 10. Split Reveal (分割揭示)

Text splits vertically and reveals from center.

```css
.split-reveal {
  clip-path: inset(0 50% 0 50%);
}
.split-reveal.active {
  clip-path: inset(0 0 0 0);
}
```

```javascript
tl.to(".split-reveal", {
  clipPath: "inset(0% 0% 0% 0%)",
  duration: 0.6,
  ease: "power3.inOut"
}, 0.2);
```

**Best for:** Cinematic reveals, premium/dark themes, dramatic pauses.  
**Duration:** 0.5-0.8s, `power3.inOut` or `circ.inOut`.

---

## Effect Selection by Theme

| Theme / Palette | Recommended Effect | Duration |
|---|---|---|
| Cultivation (修仙) | Stroke Draw + Scale Pop | 1.5s draw + 0.3s pop |
| Cyberpunk / Neon | Glitch + Neon Glow | 0.6s glitch burst |
| Clean Corporate | Slide + Fade | 0.5s per element |
| Bold Energetic | Bounce In + Scale Pop | 0.4s per character |
| Dark Premium | Split Reveal + Stroke Draw | 0.6-1.5s |
| Science / Tech | Typewriter + Glitch | 0.06s/char |
| Nature / Organic | Wave + Slide Fade | 0.8s oscillation |
| Game / Playful | Bounce In + Rotate In | 0.3-0.5s |

---

## Prompt Templates for AI Generation

When asking AI to generate animated text, use these templates:

### Hook Cover Title (钩子封面标题)

```
生成标题"{标题文字}"的入场动画：
- 效果：[从上表选择效果]
- 时长：[0.3-0.6s]
- 缓动：[expo.out / back.out(1.5) / power3.out]
- 颜色：[主色]
- 每个字延迟：[0.05-0.1s]
- 背景装饰：[发光/粒子/渐变脉冲]
```

### Section Title (章节标题)

```
生成章节标题"{标题}"的入场动画：
- 效果：Slide + Fade
- 方向：从[左/下/右]滑入
- 时长：0.5s
- 缓动：power3.out
- 前导元素：左侧6px竖线从0高度展开到满高
```

### Stats / Numbers (数据数字)

```
生成数字{数字}的入场动画：
- 效果：Scale Pop（从scale:0弹入）
- 时长：0.4s
- 缓动：back.out(2)
- 颜色：[强调色]
- 入场后：持续[3s]的呼吸脉冲（scale 1.0→1.05→1.0）
```

---

## Good vs Bad Prompts

| Bad | Good |
|---|---|
| 让标题动起来 | 标题"修仙体系"从下方滑入，0.5s，power3.out，金色#FFBE0B，每个字延迟0.08s |
| 做个酷炫的文字效果 | 故障效果：标题先显示红色偏移-4px，0.1s后切到青色偏移+3px，持续0.6s |
| 文字要有动画 | 打字机效果逐字显示"Hello World"，0.06s/字，expo.out，完成后光标闪烁3次 |
| 让数字动起来 | 数字从0跳到95，1.5s，power2.out，tabular-nums，入场前scale从0弹入0.4s |

---

## Integration with House Style

These effects complement the house style in `house-style.md`:

- **Hook cover** → Use Scale Pop or Stroke Draw for the hero title
- **Section titles** → Use Slide + Fade or Rotate In
- **Stats/numbers** → Use Scale Pop + count-up
- **Body text** → Use Slide + Fade (standard entrance, already in templates)
- **Decorative text** → Use Wave or Neon for ambient background elements
