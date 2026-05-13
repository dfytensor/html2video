<div align="center">

# AI-Animation.skill

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

[快速开始](#快速开始) · [模板总览](#模板总览) · [效果示例](#效果示例) · [视频导出](#视频导出) · [更新日志](CHANGELOG.md)

</div>

---

## 它能做什么

输入一段技术科普文本，AI 自动生成演示动画，并可选导出为视频：

```
用户输入：OSI 七层模型是什么？(相关科普文档)

阶段一（HTML 生成）：
  模式一（默认）：科普文本 → 生成基础 HTML → Level2 PPT 模板重构 → 炫酷演示文件
  模式二（可选）：已生成的 HTML → Animation 流程图模板重构 → 平面 UI 风格

阶段二（视频导出）：
  HTML 文件 → Playwright 截图 → Edge TTS 配音 → ffmpeg 合成 → MP4 视频
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
pip install edge-tts playwright moviepy pillow
python -m playwright install chromium
```

### 使用

**模式一（PPT 演示）：**
1. 在对话中输入科普内容，说「帮我生成PPT」
2. Skill 自动生成基础 HTML → 选择 Level2 模板重构
3. 输出炫酷演示文件

**模式二（流程图）：**
1. 先完成模式一，生成 AI_Animation.html
2. 说「生成流程图」
3. Skill 自动选择 Animation 模板重构为平面 UI 风格

**导出视频：**
```bash
# 使用 Skill 说「生成视频」自动调用，或手动运行：
python scripts/html2video.py AI_Animation.html
python scripts/html2video.py AI_Animation.html -o output.mp4 --width 1920 --height 1080
```

---

## 蒸馏了什么

| 类别            | 内容                           |
| ------------- | ---------------------------- |
| **PPT Level2 模板** | 26 个高质量 HTML 轮播演示模板（含选择指南 SUMMARY.md） |
| **PPT 基础模板**  | 4 个可复用的 HTML 轮播演示模板          |
| **Animation 模板**  | 14 个流程图风格的 HTML 模板（含选择指南 SUMMARY.md） |
| **视频转换工具** | html2video.py：HTML → Playwright截图 → TTS配音 → MP4 |
| **工作流**       | 文本 → HTML → 模板重构 → 流程图 → 视频 的完整链路 |

---

## 项目结构

```
AI-Animation-Skill/
├── SKILL.md                              # Skill 主文件（全流程定义）
├── README.md                             # 本文件
├── LICENSE                               # MIT 开源协议
├── scripts/
│   └── html2video.py                     # HTML → 视频转换脚本
└── assets/
    └── templates/
        ├── PPT Template-level2/          # PPT 高级模板（优先选用，26 个）
        │   ├── SUMMARY.md                #   AI 选模板参考文档
        │   ├── 1.html ~ 9-3.html         #   9 个系列 26 个模板
        ├── PPT/                          # PPT 基础模板（回退选用，4 个）
        │   ├── PPT-Generate-1.html
        │   ├── PPT-Generate-2.html
        │   ├── PPT-Generate-3.html       #   基础回退推荐
        │   └── PPT-Generate-4.html
        └── Animation/                    # 流程图模板（14 个）
            ├── SUMMARY.md                #   AI 选模板参考文档
            ├── RNN-2.html ~ RNN-7.html   #   RNN 系列（6 个）
            ├── LSTM-1.html               #   LSTM 三阶段
            ├── Comprehension.html         #   架构理解
            ├── GPU.html                   #   计算硬件
            ├── word2vec-1.html            #   词向量
            ├── onehot.html / onehot-drawback.html  # One-hot 编码
            ├── The fatal flaw of DNN.html #   DNN 缺陷
            └── Cross-modal disentanglement - 2.html  # 跨模态
```

---

## 视频导出

### 技术架构

```
HTML 动画页（CSS 动画）
        │
        ├── Playwright 逐帧截图（每个 slide 多帧 PNG）
        │
        ├── Edge TTS 语音合成（每页解说 → MP3）
        │
        ├── PIL 字幕图片生成
        │
        └── ffmpeg 合成（PNG + 字幕 + MP3 → MP4）
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | （必填） | 输入 HTML 文件路径 |
| `-o` | 同目录 `_video.mp4` | 输出 MP4 路径 |
| `--width` | 1080 | 视频宽度 |
| `--height` | 1920 | 视频高度 |
| `--voice` | `zh-CN-YunxiNeural` | TTS 语音 |
| `--fps` | 24 | 视频帧率 |
| `--frames` | `0.5,1.5,2.5,3.5,4.5` | 截图时间点 |
| `--no-subtitle` | - | 禁用字幕 |

### 常用命令

```bash
# 基础：竖屏 1080x1920
python scripts/html2video.py demo.html

# 横屏 1920x1080
python scripts/html2video.py demo.html --width 1920 --height 1080

# 女声配音
python scripts/html2video.py demo.html --voice zh-CN-XiaoxiaoNeural

# 30fps
python scripts/html2video.py demo.html --fps 30
```

---

## 模板总览

### PPT Level2 模板（26 个，优先选用）

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

| 模板                 | 特点         | 说明     |
| ------------------ | ---------- | ------ |
| PPT-Generate-1     | 简洁风格       | 基础演示   |
| PPT-Generate-2     | 图表丰富       | 数据类内容  |
| **PPT-Generate-3** | **视觉效果最佳** | **通用推荐** |
| PPT-Generate-4     | 布局灵活       | 复杂内容   |

### Animation 流程图模板（14 个）

| 模板        | 特点       | 适用场景     |
| --------- | -------- | -------- |
| **RNN-3** | **分层卡片** | **通用推荐（默认）** |
| RNN-2     | 分步展示     | RNN 原理   |
| RNN-4     | 标准化流程    | 22 种动画，最密 |
| RNN-5     | 致命缺陷     | 问题/解决对比  |
| RNN-6     | 梯度爆炸警示   | explode 动画 |
| RNN-7     | 双问题对比    | 梯度消失+爆炸  |
| LSTM-1    | 三阶段门控    | LSTM 展示  |
| onehot    | 编码介绍     | 离散特征     |
| onehot-drawback | 编码缺陷 | 稀疏性问题    |
| word2vec-1 | 语义身份证  | 词向量      |
| Comprehension | 理解架构 | 认知类      |
| GPU       | 计算节点     | 硬件展示     |
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
- **动画**：CSS Animation / Keyframes / 3D Transform / Canvas 粒子
- **视频**：Python 3.10+ / Playwright / Edge TTS / ffmpeg / Pillow
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
