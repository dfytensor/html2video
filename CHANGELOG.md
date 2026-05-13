# 更新日志

所有重要变更均记录在此文件中。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

---

## v3.0.0 — 2026-04-28

**重大升级：全流程 HTML → 视频生成能力**

### 新增

- **html2video.py**：新增 HTML 到视频的完整转换脚本（`scripts/html2video.py`）
  - Playwright 逐帧截图（每个 slide 多帧 PNG，捕获 CSS 动画不同阶段）
  - Edge TTS 语音合成（支持多种中文语音、语速调节）
  - PIL 字幕图片生成（自动中文分换行）
  - ffmpeg 合成 MP4（PNG + 字幕 + MP3 → MP4）
  - 支持竖屏/横屏、自定义帧率、语音、字幕开关
  - 缓存机制：截图和音频自动复用
- **阶段二工作流**：SKILL.md 新增「阶段二：HTML → 视频生成」完整流程定义
- **Q4~Q7 踩坑记录**：asyncio+Playwright 冲突、moviepy 内存溢出、Windows 编码、ffmpeg 中文路径

### 变更

- **Skill 重命名**：`science-content-ppt` → `science-content-video`，反映视频生成能力
- **SKILL.md 重构**：分为「阶段一：HTML 生成」和「阶段二：视频导出」两大阶段
- **README.md 更新**：新增视频导出章节、技术架构说明、常用命令示例
- **视频批量生成方案.md** 内容已整合进 SKILL.md

---

## v2.0.0 — 2025-04-15

**重大重构：模板体系升级 + 工作流优化**

### 新增

- 🆕 **PPT Level2 模板**：新增 26 个高质量模板（`assets/templates/PPT Template-level2/`），按主题分 9 个系列，覆盖对比/步骤/概念/案例/警示/辩论等场景
- 🆕 **SUMMARY.md 选择指南**：Level2 和 Animation 各自新增 AI 选模板参考文档，模型可根据科普内容类型自动匹配最佳模板
- 🆕 **已知问题 FAQ**：SKILL.md 新增 Q1~Q3 实操踩坑总结（动画不重触发、代码量不足、流程图模式说明）
- 🆕 **参数说明表**：SKILL.md 新增清晰的参数默认值和说明

### 变更

- 📁 **目录重构**：`templates/` → `assets/templates/`，结构更规范
  - `templates/PPT-Template/` → `assets/templates/PPT/`（基础模板，回退选用）
  - `templates/RNN-Template/` → `assets/templates/Animation/`（更准确的命名）
- 🔄 **Skill 重命名**：`AI-Animation` → `science-content-ppt`，更准确描述能力边界
- 🔄 **工作流精简**：原三步流程优化为两步模式（PPT 模式 + 流程图模式），Level2 模板替代原 Step 2
- 🔄 **模板优先级调整**：PPT Level2 模板优先，基础 PPT 模板回退
- 🔄 **emoji → UI 图标**：Step 2 强制将 emoji 替换为 Font Awesome / Lucide 图标库
- 🔄 **动画重置修复**：新增 cloneNode 动画重置 JS，解决切换页面后动画不复发的 bug

### 删除

- ❌ `references/workflow.md`（工作流内容已整合进 SKILL.md）
- ❌ PPT-Generate-5/6/7.html（被 Level2 模板替代）

---

## v1.0.0 — 2025-03-XX

**初始发布**

- 基础 PPT 模板（PPT-Generate-1~7）
- RNN 系列 Animation 模板
- 三步工作流：文本 → 基础 HTML → PPT 模板重构 → 流程图重构
- Skill 定义文件 SKILL.md
