# Prompt Templates

Read this file when generating HTML from user content (Phase 1).

---

## Mode 1, Step 1 — PPT Prompt Generation

Apply this template to the user's input text to generate a comprehensive PPT prompt.

### Step 1a — Generate Hook Title & Video Title

Before generating the full prompt, rewrite the topic into a hook cover. The title IS the hook — not separate from it. Read the user's topic and derive:

1. **Hook title (HTML `<h1>`)** — Rewrite the topic as a provocative question, surprising claim, or dramatic framing (max 15 chars Chinese / 8 words English). This becomes the cover page's main title.
2. **Tension subtitle (HTML)** — A secondary line that deepens curiosity or raises stakes (NOT a plain topic description).
3. **Hook visual** — Describe the visual: oversized number, icon, or contrast element that appears on the cover.
4. **Video title (publish caption)** — A separate hook title for the video's social media post (max 30 chars). Format: `{hook claim} | {tension payoff}`. Example: "95%的人都理解错了TCP | 你可能也是其中之一". This gets written to `_title.txt` by html2video.py.
5. **Topic intro (Slide 2)** — The actual definition/overview that follows, where the hook's question is answered.

### Step 1b — Full Generation Prompt

```
根据以下内容生成基于纯前端页面单页布局仿PPT换页轮播进行直观图形化可视化的介绍，加大文字大小，并运用加粗、下划线、斜体、文字颜色、文字背景等强调方式方便进行视频演示。添加每次切换页面时页面中的各个元素依次"缓入"出现的动画效果(细化到每行文字)。

【关键：封面/标题页本身就是钩子】
第一页（封面页）的标题必须能制造好奇心或冲击力，不是普通的"XXX详解"式标题。要求：
- 标题用令人惊讶的数字、反直觉的结论、或挑衅性的问题（例如标题："95%的人都理解错了"，副标题："关于TCP你可能也是其中之一"）
- 绝对禁止使用"今天我们来了解XXX"、"XXX详解"、"XXX简介"这类无聊标题
- 封面标题不直接给出答案，只制造悬念
- 封面必须有强烈的视觉元素：超大字号（64-120px）、高对比色、戏剧性图标或数字
- 封面动画必须快速有力：0.15秒内第一个元素可见，1秒内所有元素可见
- 第二页才是正式的主题介绍页，用来回应封面制造的悬念
- 后续页面正常展开科普内容

---
{用户输入的科普内容文本}
---
```

---

## Mode 1, Step 2 — Mandatory Constraints

**Append these two constraints to every HTML generation prompt:**

### Constraint A: Replace Emoji with UI Icons

```
将emoji图标换成平面ui库的图标。

图标来源优先级（按主题选择）：

【A】CDN 图标库（在线加载，无需下载）：
1. Font Awesome（已加载）：使用 <i class="fa-solid fa-xxx"> 格式
2. Remix Icon（科学/科技推荐）：CDN https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css
3. Tabler Icons（最大图标集）：CDN https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.4.0/dist/tabler-icons.min.css
4. Lucide / IconPark / Phosphor / Bootstrap Icons 等，详见 references/icons.md

【B】本地主题图标（需先运行下载脚本）：
如果内容涉及以下主题，优先使用本地 SVG 图标（无需加载额外 CDN）：
- 修仙/玄幻/武侠 → 先运行 python scripts/download-icons.py --category nature
  引用方式：<img src="assets/icons/element/fire.svg" style="width:64px;height:64px;filter:invert(1)">
  完整目录：references/cultivation-icons.md（43 icons, 8 categories）
- 化学/生物/硬件/能源/金融/气象/工业 → 先运行 python scripts/download-icons.py --category chemistry
  完整目录：references/themed-icons.md（55 icons, 7 categories）

【C】全部下载：
python scripts/download-icons.py --test    # 下载全部89个图标 + 生成测试页

规则：
- 每页最多加载2个CDN图标库。如需更多，下载SVG内联使用
- 暗色背景用 filter:invert(1) 将黑色SVG转为白色；可用 sepia+saturate+hue-rotate 着色
- 完整映射表见 references/icons.md
- 添加完成后检查页面中是否还有残留的emoji字符，如有则全部替换
```

### Constraint A2: Text Animation Effects

```
标题、章节标题、钩子封面等文字元素应使用入场动画效果。

效果选择（按主题匹配）：
- 修仙/传统 → Stroke Draw（描边绘制）+ Scale Pop（缩放弹入）
- 科技/赛博 → Typewriter（打字机）+ Glitch（故障）
- 企业/商务 → Slide + Fade（滑入淡入）
- 高能/游戏 → Bounce In（弹跳入场）+ Scale Pop
- 暗色/电影 → Split Reveal（分割揭示）+ Stroke Draw
- 自然/有机 → Wave（波浪）+ Slide Fade

完整效果目录（10种）：references/text-animations.md
每种效果含 GSAP 代码示例、参数范围和适用场景。
```

### Constraint B: Unified Animation Class Names

```
所有动画元素的class名统一使用 an 或 anim-item，以便后续动画重置逻辑能正确识别并处理。
```

---

## Mode 1, Step 3 — PPT Template Restructure Prompt

```
以页面 {模板相对路径} 为模板重构 {用户指定的输出路径}。

请将AI_Animation.html的内容按照指定PPT模板的布局、样式和轮播机制进行重构，保持科普内容不变，优化视觉效果使其更适合视频演示。

【重要：封面必须保留钩子标题】
重构时必须保留封面的钩子设计：
- 封面标题保持好奇心/冲击力（反直觉结论、挑衅性问题、惊人数字），不允许改为普通的"XXX详解"式标题
- 封面副标题保持悬念感，不允许改为普通的主题描述
- 封面的动画保持快速（0.15-0.35秒），使用expo.out或back.out缓动
- 封面必须有强烈的视觉元素（超大字号、高对比色、戏剧性图标）
- 第二页才是正式的主题介绍，用来回应封面的悬念
- 后续页面遵循模板原有的布局和动画风格
```

**Template path examples:**
- Level2 (preferred): `assets/templates/PPT Template-level2/3-1.html`
- Fallback: `assets/templates/PPT/PPT-Generate-3.html`

**Before using this prompt, AI must read `assets/templates/PPT Template-level2/SUMMARY.md` to select the best template.**

---

## Mode 2, Step 2 — Animation Restructure Prompt

```
将 {用户指定的输出路径} 网页的每相邻的两页的内容合并后按照指定网页的平面UI样式进行视觉重构，保持现有颜色方案不变。

具体实施要求包括：
1. 精确还原模板中的布局结构、元素间距、字体样式、图标设计和视觉层次
2. 确保所有交互元素（按钮、表单、导航等）的视觉表现与参考网页一致
3. 维持原有的颜色值和配色方案
4. 保证修改后的页面在不同设备和浏览器上具有良好的响应式表现
5. 优化DOM结构以匹配UI设计，同时保持原有功能完整性和交互逻辑不变

完成后需进行视觉一致性检查，确保实现效果与参考网页达到95%以上的相似度。

模板路径：{模板相对路径，默认 assets/templates/Animation/RNN-3.html}
```

---

## Animation Reset JS (Insert Before `</body>`)

```javascript
(function() {
    document.querySelectorAll('.slide').forEach(function(s) {
        s.querySelectorAll('.an, .anim-item, [style*="animation"]').forEach(function(item) {
            var clone = item.cloneNode(true);
            item.parentNode.replaceChild(clone, item);
        });
    });
})();
```

**When to insert:** After every HTML generation or restructure that includes CSS animations with slide navigation.

---

## Mode 3 — Semi-Automatic Pipeline Prompts

### Mode 3, Step 1 — Script Design Prompt

Apply this template when the user triggers semi-auto mode:

```
根据以下内容，设计一个完整的视频口播稿和场景规划。

要求：
1. 将内容分为 {6-15} 个场景（根据内容量调整）
2. 每个场景包含：
   - 场景标题：简短的中文标题（4-8字）
   - 口播稿：自然口语化的旁白文本（50-200字），像在跟朋友聊天一样
   - 视觉描述：观众应该看到的画面描述（布局、关键元素、数据等）
   - 预估时长：基于口播稿长度

【关键：第一场景必须是钩子封面】
- 场景0的标题必须是钩子式标题（令人惊讶的数字、反直觉结论、或挑衅性问题）
- 场景0的口播稿第一句必须是音频钩子（不能是"今天我们来了解"这类开场白）
- 场景0的视觉描述必须有强烈的视觉冲击力（超大数字、戏剧性对比、高对比色彩）
- 场景1才是正式的主题介绍，用来回应钩子封面的悬念

【口播稿写作规则】
- 使用自然口语，不要书面语
- 每段口播稿应该听起来像在说话，不像在读论文
- 避免使用"首先"、"其次"、"最后"这类过渡词
- 用短句为主，每句不超过25字
- 可以用反问句、感叹句增加节奏感

【视觉风格】
- 整体风格：{从 visual-styles.md 选择，或询问用户}
- 配色方案：{从 palettes/ 选择，或询问用户}
- 画面比例：9:16（竖屏短视频）

---
{用户输入的内容文本}
---

请以JSON格式输出，格式如下：
{
  "project": "项目名称",
  "title": "钩子视频标题（用于社交媒体发布）",
  "total_scenes": N,
  "voice": "zh-CN-YunxiNeural",
  "rate": "+0%",
  "resolution": {"width": 1080, "height": 1920},
  "fps": 24,
  "global_style": "整体视觉风格描述",
  "global_palette": "配色方案描述",
  "scenes": [
    {
      "index": 0,
      "title": "钩子标题",
      "voiceover": "口语化旁白文本...",
      "visual_description": "视觉描述...",
      "duration_estimate": 5.0,
      "image_filename": "scene_000_hook_cover.png"
    },
    ...
  ]
}
```

### Mode 3, Step 3 — Image Prompt Document Prompt

Apply this template after the script design is complete to generate image prompts:

```
根据以下场景规划JSON，为每个场景生成详细的图像生成提示词。

要求：
1. 每个场景的提示词必须是模型无关的（可用于 Midjourney / DALL-E / Stable Diffusion / Flux）
2. 提示词结构：[主体/场景], [构图/布局], [风格/美学], [配色], [光照/氛围], [质量修饰词]
3. 每个场景提供正向提示词和负向提示词
4. 所有场景保持风格一致性（使用 global_style 和 global_palette）
5. 画面比例统一为 9:16（竖屏）
6. 图像中不要包含文字（除非特别说明）— 文字会在后期制作时叠加

【图像命名规则】
- 格式：scene_NNN_brief_name.png
- NNN: 三位数字（000, 001, 002, ...）
- brief_name: 英文小写，下划线分隔，2-4个词

【场景规划JSON】
{script_design.json 内容}

请生成Markdown格式的图像提示词文档，包含：
1. 命名规则说明
2. 全局风格说明
3. 每个场景的详细提示词（含正向和负向）
4. Midjourney 特定的 --ar 和 --v 参数
5. 视觉描述和注意事项
```
