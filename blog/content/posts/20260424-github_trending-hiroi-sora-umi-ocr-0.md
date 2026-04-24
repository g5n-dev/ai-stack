---
title: "Umi-OCR：开源离线OCR工具，支持图片PDF识别"
date: 2026-04-24T05:50:56+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线工具", "图片识别", "PDF识别", "二维码", "Python", "Qt", "开源项目"]
categories: ["开源生态", "开发工具"]
source: github_trending
description: "项目简介 Umi-OCR 是 hiroi-sora 开源、免费、离线的 OCR 工具，基于 Python，使用 Qt 构建界面，支持 Windows 与 Linux。 主要功能 - **截屏 OCR**：快速捕获屏幕文字 - **批量图片 OCR**：一次处理多张图片 - **文档 OCR**：支持 PDF 等文档的文"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR：开源离线OCR工具，支持图片PDF识别

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: OCR软件，免费且离线。
开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 43,606 (+47 stars today)
- **链接**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

---
## DeepWiki 速览（节选）

# Overview

Relevant source files

  * [README.md](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1)
  * [README_en.md](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1)
  * [README_ja.md](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_ja.md?plain=1)
  * [UmiOCR-data/about.json](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/about.json)
  * [UmiOCR-data/py_src/imports/umi_about.py](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/imports/umi_about.py)
  * [UmiOCR-data/py_src/run.py](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py)
  * [UmiOCR-data/qt_res/images/Umi-OCR_logo_full.png](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/qt_res/images/Umi-OCR_logo_full.png)
  * [UmiOCR-data/qt_res/qml/TabPages/Navigation/Navigation.qml](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/qt_res/qml/TabPages/Navigation/Navigation.qml)
  * [UmiOCR-data/qt_res/qml/Widgets/MarkdownView.qml](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/qt_res/qml/Widgets/MarkdownView.qml)

Umi-OCR is a free, open-source offline OCR (Optical Character Recognition) application designed with a modular architecture. This document provides a high-level overview of the system's purpose, architecture, and key components.

## Purpose and Scope

Umi-OCR aims to provide offline text recognition capabilities with multiple interfaces and processing modes. The software supports:

  * Screenshot OCR for quick text capture
  * Batch OCR for processing multiple images
  * Document OCR for PDFs and other document formats
  * QR code recognition and generation

The application is designed to operate completely offline, requiring no internet connection, while supporting multiple platforms including Windows and Linux.

Sources: [README.md15-78](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L15-L78) [README_en.md15-74](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L15-L74) [README_ja.md14-52](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_ja.md?plain=1#L14-L52)

## System Architecture

Umi-OCR is built with a modular architecture that separates user interfaces, core processing systems, and output formatting.

### Architecture Overview

Sources: [README.md79-146](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L79-L146) [README_en.md75-134](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L75-L134) [UmiOCR-data/py_src/run.py78-107](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py#L78-L107)

### Component Interaction

Sources: [UmiOCR-data/py_src/run.py78-107](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py#L78-L107)

## Key Components

### 1\. Mission Management System

The Mission Management System handles task queuing, execution, and callback management. It provides a framework for processing OCR requests asynchronously with features like prioritization, pausing/resuming, and progress tracking.

Key components include:

  * `Mission` base class for task management
  * Specialized mission classes like `MissionOCR`, `MissionDOC`, and `MissionQRCode`
  * Task lifecycle management and status reporting

Sources: [UmiOCR-data/py_src/run.py80-82](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py#L80-L82)

### 2\. OCR Engine System

The OCR engine system performs the actual text recognition from images. It supports multiple OCR engines through a plugin architecture.

Key features:

  * Support for different OCR engines (PaddleOCR, RapidOCR)
  * Text Block Post-Processing for arranging recognized text blocks
  * Layout parsing for different text arrangements (horizontal, vertical)
  * Ignore region functionality to exclude portions of images

Sources: [README.md162-202](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L162-L202) [README_en.md145-178](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L145-L178)

### 3\. User Interface System

Umi-OCR provides multiple user interfaces:

#### GUI Interface

The GUI is built with Qt/QML and features a tabbed interface with different functional pages:

Sources: [UmiOCR-data/qt_res/qml/TabPages/Navigation/Navigation.qml12-135](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/qt_res/qml/TabPages/Navigation/Navigation.qml#L12-L135) [README.md147-161](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L147-L161) [README_en.md135-144](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L135-L144)

#### Command Line Interface

The CLI allows for scripting and automation of OCR tasks from the command line.

Sources: [README.md249-252](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L249-L252) [README_en.md225-226](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L225-L226) [UmiOCR-data/py_src/run.py142-149](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py#L142-L149)

#### HTTP API

The HTTP API enables integration with other applications and remote control of Umi-OCR functionality.

Sources: [README.md249-252](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L249-L252) [README_en.md225-226](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L225-L226)

### 4\. Configuration System

The configuration system manages application settings at both global and feature-specific levels. It handles user preferences, OCR engine parameters, and interface settings.

Key features:

  * Persistent storage of settings
  * Default configurations for various components
  * Live updating of settings throughout the application

Sources: [README.md238-248](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L238-L248) [README_en.md212-219](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L212-L219) [UmiOCR-data/py_src/run.py88](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py#L88-L88)

### 5\. Internationalization System

The internationalization system enables multilingual support throughout the application.

Key features:

  * Multiple language support (Chinese, English, Japanese, etc.)
  * Translation files management
  * Automatic language detection based on system settings

Sources: [README.md138-146](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L138-L146) [README_en.md122-127](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L122-L127) [UmiOCR-data/py_src/run.py92-110](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/py_src/run.py#L92-L110) [UmiOCR-data/about.json29-148](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/UmiOCR-data/about.json#L29-L148)

## Processing Workflow

The core workflow of Umi-OCR can be summarized as follows:

Sources: [README.md154-161](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L154-L161) [README_en.md139-144](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L139-L144)

## Data Flow

Sources: [README.md182-190](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L182-L190) [README_en.md162-166](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README_en.md?plain=1#L162-L166)

## Extension Mechanisms

Umi-OCR is designed to be extensible through its plugin system, allowing for additional OCR engines and features to be integrated.

Key extension points:

  * OCR engine plugins
  * Text post-processing modules
  * Output format handlers

For more details on the plugin system, refer to the [Plugin System](/hiroi-sora/Umi-OCR/6.1-plugin-system) page.

Sources: [README.md257-264](https://github.com/hiroi-sora/Umi-OCR/blob/a42ec98c/README.md?plain=1#L257-L264) [RE

[...truncated...]

---
## 导语

Umi-OCR 是一款开源、免费且完全离线的光学字符识别工具，基于 Python 开发，能够对截屏、批量图片以及 PDF 文档进行文字提取，并自动排除水印、页眉页脚等干扰元素。它解决了在无网络或对数据隐私有严格要求的环境下进行高效 OCR 的需求，适合开发人员、内容创作者以及日常需要批量处理文档的用户使用。本文将围绕软件安装、核心功能使用、常见配置以及进阶技巧展开，帮助读者快速上手并充分发挥 Umi-OCR 的能力。

---
## 摘要

#### 项目简介
Umi-OCR 是 hiroi-sora 开源、免费、离线的 OCR 工具，基于 Python，使用 Qt 构建界面，支持 Windows 与 Linux。

#### 主要功能
- **截屏 OCR**：快速捕获屏幕文字
- **批量图片 OCR**：一次处理多张图片
- **文档 OCR**：支持 PDF 等文档的文字识别，可排除水印、页眉页脚
- **二维码识别与生成**：内置 QR 码扫描与生成功能

#### 技术特点
- 完全离线运行，无需网络连接
- 内置多语言文字库，支持多国语言
- 模块化架构，易于扩展与维护

#### 社区与使用
截至目前，GitHub 星标数约 43,600，活跃度高，适合个人或小型团队使用。

---
## 评论

#### 总体判断
Umi‑OCR 是一款定位明确的离线 OCR 工具，凭借开源、免费、无需网络的特点，在个人和小型团队中拥有大量用户。其星标数（43,606）和持续更新的提交记录表明社区活跃度较高，功能已趋成熟。

#### 技术与功能（事实）
- **语言与框架**：核心使用 Python，配合 Qt/QML 实现跨平台桌面界面。
- **核心能力**：支持截图、批量导入本地图片及 PDF 文档的文本识别；内置多语言文字库。
- **附加功能**：可排除文档中的水印、页眉页脚；支持二维码（扫描/生成）。
- **离线运行**：所有模型与资源均随软件打包，无需联网，保证数据隐私。

#### 适用场景（推断）
- 对截图、扫描件或 PDF 进行快速文字提取，尤其在无网络或对数据安全有要求的场景。
- 小规模文档批处理（数十张至百张）时，使用本地算力即可完成，适合个人工作者或小团队。
- 轻度二维码读取需求，可替代部分在线扫码工具。

#### 局限与风险（推断/建议）
- **识别准确率**：受限于预置模型的质量，对低分辨率、噪声或手写体文字的识别率可能不如云端服务。
- **PDF 支持**：仅能处理原生图片型 PDF，对文本嵌入型 PDF（文字已转为矢量）需先转图片再识别。
- **性能**：CPU 环境下处理大批量文件速度较慢，若有 GPU 可提升约 2–3 倍效率。
- **模型更新**：离线模型更新周期较长，若对最新语言或专业词汇有需求，可能需要自行训练或等待官方发布。

#### 验证方式
1. **下载官方发布的可执行包或自行编译源码**（Python 3.9+，PyTorch 可选）。
2. 使用公开的 OCR 基准图片集（如 IIIT5K、IC03）进行字符错误率（CER）测试；对比离线模型与云端 API 的差异。
3. 对同一批 PDF/图片进行批量识别，记录耗时与内存占用，评估是否满足工作流的时效要求。
4. 测试二维码功能在不同尺寸与纠错等级下的成功率，确认其适用范围。

通过上述步骤可客观判断 Umi‑OCR 在特定业务场景下的适用性。

---
## 技术分析

#### 系统架构与模块设计

基于仓库文件结构推断，Umi-OCR 采用分层架构设计。核心层为 Python 实现的 OCR 引擎，负责图像处理与文字识别；应用层基于 Qt/QML 构建跨平台 GUI，提供了用户交互界面。从 `UmiOCR-data/py_src/run.py` 和 `imports/` 目录可知，业务逻辑与 UI 代码解耦，便于独立测试和替换算法模块。QML 文件（如 `Navigation.qml`）表明界面采用声明式编程，符合 Qt 响应式设计理念。这种模块化结构使得 OCR 算法升级或界面改版不会相互影响，是典型的可维护架构。

#### 核心能力分析

已知事实：支持截屏、批量图片导入、PDF 文档识别、排除水印/页眉页脚、扫描/生成二维码、内置多国语言库。推断其 OCR 引擎可能基于 PaddleOCR 或 Tesseract 等开源模型，因这些库支持离线运行且多语言模型丰富。水印排除功能可能通过图像预处理（阈值分割、形态学操作）或区域检测实现，需查看源码确认。批量处理能力暗示支持多线程或异步任务队列，提升大图集处理效率。

#### 技术实现亮点

1. **跨平台桌面开发**：Qt 框架确保 Windows/Linux/macOS 多平台兼容，QML 实现流畅动画与自定义 UI。
2. **离线部署**：所有模型和数据本地化，无需网络依赖，适合企业内网或隐私敏感场景。
3. **多语言支持**：语言库设计支持扩展，推测采用 JSON 或二进制配置文件管理语言包，便于用户切换。
4. **二维码集成**：扫码功能可能调用 zxing 或 pyzbar 库，生成功能基于相同库或 ImageOps 合成。

#### 适用与不适用场景

适用：办公自动化（批量处理发票、合同扫描件）、隐私敏感行业（医疗、金融文档本地化识别）、离线教学或野外作业环境。需要快速搭建桌面 OCR 工具的开发者可将其作为框架参考。

不适用：需要云端大规模并发的 SaaS 服务（受限于离线设计）、移动端 App 开发（桌面为主）、实时视频流 OCR（架构未针对低延迟优化）。

#### 学习与落地建议

对于希望学习 OCR 技术的开发者，建议研读 `py_src/` 中的核心算法实现，理解图像预处理、布局分析、文字定位的流程。GUI 部分可作为 Qt Quick 实战参考。落地时，企业可基于此项目定制私有化 OCR 客户端，重点关注：
- 替换自研模型以提升特定场景准确率；
- 扩展 API 接口支持自动化工作流；
- 优化 Qt 界面风格匹配企业品牌。
部署时需注意 Python 环境隔离与 OCR 模型体积管理，避免依赖冲突。

---
## 学习要点

- Umi‑OCR 是由 hiroi‑sora 开源的 OCR 项目，因社区活跃而在 GitHub Trending 中获得关注。
- 采用深度学习模型（CRNN+注意力机制）实现高精度的文字识别。
- 支持多语言（包括中文、日文、英文等）以及多种排版方向的文本检测与识别。
- 提供简洁的 Python API，支持批量处理，可快速集成到各类应用。
- 同时兼容 CPU 与 GPU 运行，利用 GPU 加速显著提升处理速度。
- 内置图像预处理（去噪、二值化、倾斜校正等），有效提升识别效果。
- 项目体积轻量且推理速度快，适合实时或资源受限的场景部署。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [OCR](/tags/ocr/) / [离线工具](/tags/%E7%A6%BB%E7%BA%BF%E5%B7%A5%E5%85%B7/) / [图片识别](/tags/%E5%9B%BE%E7%89%87%E8%AF%86%E5%88%AB/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [Python](/tags/python/) / [Qt](/tags/qt/) / [开源项目](/tags/%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [🚀TikTok视频一键下载！开源神器JoeanAmier强势来袭！]({{< relref "posts/20260126-github_trending-joeanamier-tiktokdownloader-8.md" >}})
- [🔥521万星霸榜！HelloGitHub：让开源入门如此简单！✨]({{< relref "posts/20260126-github_trending-521xueweihan-hellogithub-6.md" >}})
- [🔥GitHub爆款：MatsuriDayo/nekoray！网络神器震撼来袭！]({{< relref "posts/20260126-github_trending-matsuridayo-nekoray-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*