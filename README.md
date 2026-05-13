<div align="center">

# html2video

> *使用 AI 生成 HTML 演示动画并导出视频的工具集，让视频创作者能够快速将科普文本转换为带语音解说的演示视频。*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai/)
[![HTML5](https://img.shields.io/badge/HTML5-Demo-orange)](assets/templates/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](scripts/)

<br>

**不是模板合集，是可运行的 AI 动画视频生成工作流。**

<br>

基于整理好的 Prompt 模板集成的 Skill，
配合 OpenClaw、Workbuddy、QClaw 等 AI 使用，
自动完成「科普文本 → 炫酷动画 HTML → 视频(MP4)」的全流程。

支持三种模式：全自动 HTML→视频、半自动 口播稿+用户图片→视频、纯 HTML 动画生成。

[快速开始](#快速开始) · [三种模式](#三种模式) · [模板总览](#模板总览) · [效果示例](#效果示例) · [视频导出](#视频导出) · [更新日志](CHANGELOG.md)

</div>

---

## 它能做什么

输入一段技术科普文本，AI 自动生成演示动画，并可选导出为视频：

```
用户输入：OSI 七层模型是什么？(相关科普文档)

模式一（全自动 — PPT 演示，默认）：
  科普文本 → 生成基础 HTML → Level2 PPT 模板重构 → 炫酷演示文件 → MP4 视频

模式二（全自动 — 流程图）：
  已生成的 HTML → Animation 流程图模板重构 → 平面 UI 风格 → MP4 视频

模式三（半自动 — 用户图片合成）：
  科普文本 → 口播稿设计 → TTS 配音 → 图片提示词 → [用户生成图片] → MP4 视频
```

<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/c09e0f57-7f5a-4014-8809-b5e99d11e9f5" />

适用于 B 站视频素材、课堂教学、技术分享、抖音/快手短视频等场景。

---

## 快速开始

### 安装 (例：Workbuddy)

```
1. 下载本项目
2. 将 AI-Animation-Skill 文件夹复制到 ~/.workbuddy/skills/ 目录
3. 重启 WorkBuddy
```

### 视频导出依赖

```bash
pip install edge-tts playwright moviepy pillow imageio-ffmpeg
python -m playwright install chromium
```

### 使用

**模式一（PPT 演示）：**
1. 在对话中输入科普内容，说「帮我生成PPT」
2. Skill 自动生成基础 HTML → 选择 Level2 模板重构
3. 输出炫酷演示文件
4. 说「生成视频」→ 自动导出 MP4

**模式二（流程图）：**
1. 先完成模式一，生成 AI_Animation.html
2. 说「生成流程图」
3. Skill 自动选择 Animation 模板重构为平面 UI 风格

**模式三（半自动）：**
1. 说「半自动模式」或「设计口播稿」
2. AI 生成口播稿 + TTS 配音 + 图片提示词文档
3. 你用 Midjourney/DALL-E/SD 生成图片
4. 告诉 AI「图片已准备好」→ 自动合成视频

**导出视频：**
```bash
python scripts/html2video.py AI_Animation.html
python scripts/html2video.py AI_Animation.html -o output.mp4 --width 1920 --height 1080
```

---

## 三种模式

| 模式 | 触发方式 | 流程 | 适用场景 |
|------|---------|------|---------|
| **模式一：PPT** | 「生成PPT」「生成演示」 | 文本 → HTML → 模板重构 → 视频 | 通用科普、技术讲解 |
| **模式二：流程图** | 「生成流程图」（需先完成模式一） | HTML → Animation 模板重构 → 视频 | 架构图、原理流程 |
| **模式三：半自动** | 「半自动模式」「设计口播稿」 | 文本 → 口播稿 → TTS → 图片提示词 → [用户图片] → 视频 | 高质量视觉、定制图片 |

---

## 核心特性

### 3-Second Hook Rule

第一张幻灯片必须在前 3 秒内抓住观众注意力。三层钩子机制：

| 时间层 | 目标 | 实现方式 |
|--------|------|---------|
| Frame 0 (0.0s) | 视觉冲击 | 超大数字、戏剧性图标、极端对比 |
| Frame 1 (0.3s) | 动态能量 | 快速入场动画（0.15-0.35s） |
| Frame 2 (1.0-3.0s) | 好奇心缺口 | 钩子标题 + TTS 音频钩子 |

### Visual Identity Gate

每个 HTML 必须有明确的视觉身份，不允许使用默认/通用颜色。支持多种预设风格：

| 风格 | 适用场景 |
|------|---------|
| Deep Green Science | 技术深潜、神经网络（动画模式默认） |
| Clean Corporate | 商务演示、概念讲解（PPT 默认） |
| Warning Alert | 危险警告、失败分析 |
| Shadow Cut | 电影级暗色主题 |

详见 `visual-styles.md` 和 `palettes/` 目录（10 种调色板）。

### 动画引擎

| 引擎 | 特点 |
|------|------|
| **CSS Animation（默认）** | 内置于模板，cloneNode 动画重置 |
| **GSAP Timeline（高级）** | 精确时间线控制、转场动画、字幕动画、音频驱动动画 |

### QA 工具

```bash
python scripts/animation-map.py input.html      # 检测动画问题
python scripts/contrast-report.py input.html     # WCAG 对比度审计
python scripts/extract-audio-data.py audio.mp3   # 音频数据提取（用于音频驱动动画）
```

---

## 蒸馏了什么

| 类别 | 内容 |
| --- | --- |
| **PPT Level2 模板** | 25 个高质量 HTML 轮播演示模板（含选择指南 SUMMARY.md） |
| **PPT 基础模板** | 4 个可复用的 HTML 轮播演示模板 |
| **Animation 模板** | 14 个流程图风格的 HTML 模板（含选择指南 SUMMARY.md） |
| **视频转换工具** | html2video.py：HTML → Playwright截图 → TTS配音 → MP4 |
| **QA 审计工具** | animation-map.py、contrast-report.py、extract-audio-data.py |
| **调色板** | 10 种预设调色板（bold-energetic、clean-corporate、shadow-cut 等） |
| **参考文档** | 20+ 参考文档覆盖模板选择、GSAP、转场、字幕、排版、图标等 |
| **工作流** | 三种模式完整链路：全自动 PPT、全自动流程图、半自动用户图片 |

---

## 项目结构

```
AI-Animation-Skill/
├── SKILL.md                              # Skill 主文件（全流程定义，三种模式）
├── README.md                             # 本文件
├── LICENSE                               # MIT 开源协议
├── visual-styles.md                      # 视觉风格定义（Deep Green、Clean Corporate 等）
├── house-style.md                        # 动画与排版默认规范
├── patterns.md                           # 幻灯片布局模式（VS卡、步骤流、仪表盘等）
├── scripts/
│   ├── html2video.py                     # HTML → 视频转换（Divide & Conquer TTS）
│   ├── animation-map.py                  # 动画问题检测
│   ├── contrast-report.py                # WCAG 对比度审计
│   ├── extract-audio-data.py             # 音频数据提取
│   ├── capture_gsap.py                   # GSAP 动画截图工具
│   └── download-icons.py                 # 图标下载脚本
├── assets/
│   ├── templates/
│   │   ├── PPT Template-level2/          # PPT 高级模板（优先选用，25 个）
│   │   │   ├── SUMMARY.md                #   AI 选模板参考文档
│   │   │   ├── 1.html ~ 9-3.html         #   9 个系列 25 个模板
│   │   ├── PPT/                          # PPT 基础模板（回退选用，4 个）
│   │   │   ├── PPT-Generate-1~4.html
│   │   └── Animation/                    # 流程图模板（14 个）
│   │       ├── SUMMARY.md                #   AI 选模板参考文档
│   │       └── RNN/LSTM/GPU/word2vec...  #   14 个模板
│   └── icons/                            # 主题图标资源
├── palettes/                             # 10 种预设调色板
│   ├── bold-energetic.md
│   ├── clean-corporate.md
│   ├── dark-premium.md
│   ├── shadow-cut.md
│   └── ...
└── references/                           # 参考文档（20+）
    ├── template-selection.md             #   模板快速选择指南
    ├── prompt-templates.md               #   Prompt 模板（所有模式）
    ├── video-pipeline.md                 #   视频管线详细文档
    ├── semi-auto-workflow.md             #   半自动模式详细流程
    ├── gsap-reference.md                 #   GSAP API 参考
    ├── transitions.md                    #   转场动画目录
    ├── captions.md                       #   字幕动画
    ├── motion-principles.md              #   动画编排原则
    ├── icons.md                          #   图标库目录
    ├── typography.md                     #   排版指南
    ├── tts.md                            #   TTS 语音合成
    └── ...
```

---

## 视频导出

### 技术架构（Divide & Conquer）

```
HTML 动画页（CSS/GSAP 动画）
        │
        ├── Phase 1: Playwright 逐帧截图（每个 slide 多帧 PNG）
        │             Slide 1: 6帧 @ 0.1/0.3/0.5/1.0/2.0/3.5s（Hook 密集捕捉）
        │             Slide 2+: 5帧 @ 0.5/1.5/2.5/3.5/4.5s
        │
        ├── Phase 2: Edge TTS 语音合成（独立超时 + 重试 + 磁盘缓存）
        │             每个 slide 独立生成，失败自动降级为静音
        │
        ├── Phase 3: ffmpeg 合成（PNG + 字幕 + MP3 → MP4）
        │
        └── Phase 4: 所有片段拼接 → 最终 MP4
                      + Hook 视频标题（_title.txt）
                      + 封面缩略图（_cover.png）
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | （必填） | 输入 HTML 文件路径 |
| `-o` | 同目录 `_video.mp4` | 输出 MP4 路径 |
| `--width / --height` | 1080 × 1920 | 视频分辨率（竖屏） |
| `--voice` | `zh-CN-YunxiNeural` | TTS 语音 |
| `--rate` | `+0%` | 语速调节（如 `+20%`） |
| `--fps` | 24 | 视频帧率 |
| `--frames` | `0.5,1.5,2.5,3.5,4.5` | 截图时间点 |
| `--no-subtitle` | - | 禁用字幕 |
| `--no-voice` | - | 跳过 TTS，静音视频 |
| `--export-script` | - | 导出旁白文本文件 |
| `--tts-timeout` | 60 | 单个 TTS 超时（秒） |
| `--tts-retries` | 2 | TTS 最大重试次数 |
| `--tts-cache` | - | 启用 TTS 磁盘缓存 |
| `--keep-temp` | - | 保留临时文件（调试用） |
| `--slide-selector` | `.slide` | Slide CSS 选择器 |

### 半自动模式参数

| 参数 | 说明 |
|------|------|
| `--script-only` | 仅从 `_script_design.json` 生成 TTS，无需 HTML |
| `--script` | 指定 `_script_design.json` 路径 |
| `--images-dir` | 用户图片目录（自动发现 `scene_NNN_*` 命名） |
| `--images-map` | JSON 文件映射场景索引到图片路径 |
| `--tts-dir` | 预生成 TTS 音频目录 |

### 常用命令

```bash
# 基础：竖屏 1080x1920
python scripts/html2video.py demo.html

# 横屏 1920x1080
python scripts/html2video.py demo.html --width 1920 --height 1080

# 女声配音
python scripts/html2video.py demo.html --voice zh-CN-XiaoxiaoNeural

# 启用 TTS 缓存（重复运行秒出）
python scripts/html2video.py demo.html --tts-cache

# 半自动模式：从用户图片合成视频
python scripts/html2video.py --images-dir ./output_images/ --script _script_design.json -o output.mp4
```

### TTS 稳定性

采用 Divide & Conquer 策略，每个 slide 独立生成 TTS：

| 特性 | 说明 |
|------|------|
| 独立超时 | 每个 TTS 调用 60s 超时，不会卡死整个流程 |
| 自动重试 | 失败自动重试 2 次 |
| 磁盘缓存 | `--tts-cache` 按内容哈希缓存，重复运行零 TTS 调用 |
| 优雅降级 | 单个 slide TTS 失败 → 该 slide 静音，视频仍正常生成 |

---

## 模板总览

### PPT Level2 模板（25 个，优先选用）

> 模型根据科普内容类型自动选择最合适的模板，详见 `SUMMARY.md`

| 系列 | 模板数 | 适用场景 | 亮点 |
|------|--------|---------|------|
| **1** | 1 | 概念引入、对比 | VS 对比卡片 + SVG 流程图 |
| **2** | 1 | 概念定义、层级结构 | 13 种动画，最多元化 |
| **3** | 3 | 轻量/步骤/极简 | 3-3 仅 331 行最轻量 |
| **4** | 3 | 案例/实验/代码 | 代码雨动画 |
| **5** | 4 | 警示/失败/危险 | 5-4 达 15 种动画 + 13 页 |
| **6** | 4 | 护栏/架构/反馈 | 6-2 红绿 VS 对比（15 种动画） |
| **7** | 4 | 追踪/上下文/Doom Loop | 7-2 达 17 种动画 |
| **8** | 3 | 辩论/对比/融合 | 8-3 达 30 组 VS 对比 |
| **9** | 3 | 总结/共识/精炼 | 9-3 仅 5 页最精炼 |

### PPT 基础模板（4 个，回退选用）

| 模板 | 特点 | 说明 |
| --- | --- | --- |
| PPT-Generate-1 | 简洁风格 | 基础演示 |
| PPT-Generate-2 | 图表丰富 | 数据类内容 |
| **PPT-Generate-3** | **视觉效果最佳** | **通用推荐** |
| PPT-Generate-4 | 布局灵活 | 复杂内容 |

### Animation 流程图模板（14 个）

| 模板 | 特点 | 适用场景 |
| --- | --- | --- |
| **RNN-3** | **分层卡片** | **通用推荐（默认）** |
| RNN-2 | 分步展示 | RNN 原理 |
| RNN-4 | 标准化流程 | 22 种动画，最密 |
| RNN-5 | 致命缺陷 | 问题/解决对比 |
| RNN-6 | 梯度爆炸警示 | explode 动画 |
| RNN-7 | 双问题对比 | 梯度消失+爆炸 |
| LSTM-1 | 三阶段门控 | LSTM 展示 |
| onehot | 编码介绍 | 离散特征 |
| onehot-drawback | 编码缺陷 | 稀疏性问题 |
| word2vec-1 | 语义身份证 | 词向量 |
| Comprehension | 理解架构 | 认知类 |
| GPU | 计算节点 | 硬件展示 |
| Cross-modal disentanglement - 2 | 跨模态解耦 | 多模态 |
| The fatal flaw of DNN | DNN 缺陷 | 深度学习问题 |

---

## 效果示例

### PPT 风格（Level2 模板重构后）

<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/e28ccecf-2632-40f3-b239-c0dd7909af97" />
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/9efad557-81e2-49d3-9226-d6ce98b84075" />

<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/8b1be8cc-8293-4893-8b56-b695e5daf6fe" />

### 流程图风格（Animation 模板重构后）

<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/a565dd82-b690-4d1a-87ba-1b619b01273" />
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/f7481d36-44b1-439e-8565-c6def4795e1" />

---

## 技术栈

- **前端**：HTML5 + CSS3 + JavaScript（原生，无框架依赖）
- **动画**：CSS Animation / GSAP / Keyframes / 3D Transform / Canvas 粒子
- **视频**：Python 3.10+ / Playwright / Edge TTS / ffmpeg / Pillow
- **QA**：WCAG 对比度审计 / 动画碰撞检测 / 音频数据提取
- **兼容性**：现代浏览器（Chrome、Firefox、Safari、Edge）

---

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

---

## 开源协议

本项目采用 [MIT License](LICENSE)。

---

<div align="center">

**如果对你有帮助，欢迎 Star ⭐**

</div>
