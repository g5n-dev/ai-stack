---
title: "Umi-OCR：免费开源离线OCR支持多语言"
date: 2026-04-23T17:40:12+08:00
draft: false
entry_kind: "auto"
tags: ["OCR文字识别", "离线", "开源", "Python", "多语言", "二维码", "PDF", "截屏"]
categories: ["开源生态", "开发工具"]
source: github_trending
description: "Umi-OCR是一款开源、免费、完全离线的OCR（光学字符识别）软件，基于Python实现，采用模块化架构。它提供截屏OCR、批量图片OCR、PDF文档识别以及二维码扫描/生成等多种功能，并内置多语言文字库，支持Windows和Linux平台，无需网络连接即可工作。项目目前在GitHub上拥有约43,582颗星，受到广"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR：免费开源离线OCR支持多语言

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 43,582 (+48 stars today)
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

Umi-OCR是一款基于Python开发的免费开源离线OCR工具。它不依赖网络即可完成图片文字识别、PDF文档解析以及二维码处理，适合对数据隐私有要求或需要在本地批量处理文本的用户。本文将逐一展示其核心功能、操作方式及进阶应用。

---
## 摘要

Umi-OCR是一款开源、免费、完全离线的OCR（光学字符识别）软件，基于Python实现，采用模块化架构。它提供截屏OCR、批量图片OCR、PDF文档识别以及二维码扫描/生成等多种功能，并内置多语言文字库，支持Windows和Linux平台，无需网络连接即可工作。项目目前在GitHub上拥有约43,582颗星，受到广泛关注和好评。

#### 主要功能
- 截屏OCR：快速捕获屏幕上的文字。
- 批量图片OCR：一次处理多张图片，适合大量文档电子化。
- PDF文档OCR：识别PDF中的文字，自动排除水印、页眉页脚等干扰。
- 二维码识别与生成：支持扫描和生成QR码。

#### 技术特点
- 完全离线运行，保护用户隐私。
- 模块化设计，便于功能扩展和二次开发。
- 基于Python配合Qt图形界面，提供友好的交互体验。
- 多语言支持，覆盖全球主要语言的文字识别。

#### 平台与社区
- 支持Windows、Linux两大主流操作系统。
- 社区活跃，累计星标数约为43,582，说明其在开源社区的认可度较高。
- 开源项目，欢迎开发者贡献代码或提出改进建议。

---
## 评论

#### 总体判断
Umi‑OCR 是一款在开源生态中表现突出的离线 OCR 工具，兼具图形化界面与多语言支持，适合对隐私、网络依赖有要求的用户。

#### 技术依据与实现（事实 / 推断）
- 事实：仓库使用 Python 作为核心语言，UI 基于 Qt 框架，提供截屏、批量图片导入、PDF 文字抽取、二维码识别等功能；README 中明确列出离线运行、多语言库、星标 43,582，表明社区活跃。
- 推断：从源码结构看，项目将模型推理封装在独立模块中，极可能采用 ONNX Runtime 或 PaddleOCR 等开源 OCR 引擎，以实现无需网络的离线推理。

#### 适用场景
1. 个人或小型团队在无外网环境下快速提取图片、扫描件中的文字；
2. 批量处理大量截图或 PDF，要求统一输出文本或结构化数据；
3. 对文档水印、页眉页脚进行自动排除或过滤的场景；
4. 需要本地生成或识别二维码的轻量级工作流。

#### 局限与不足（事实 / 推断）
- 事实：项目依赖本地模型文件，语言包体积随支持语言数量增长，可能占用数百 MB 存储；
- 推断：在 CPU 环境下，处理高分辨率 PDF 或大规模图片时速度可能不及商业云 OCR；在极低分辨率或噪声严重的图像上，识别错误率可能上升。

#### 验证方式
- 使用公开 OCR 评估集（如 ICDAR2015）测试准确率，与 Tesseract、PaddleOCR 等基准进行对比；
- 在同一硬件（CPU/GPU）上测量批量图片的平均处理耗时；
- 通过切换不同语言包检查语言覆盖度和识别质量；
- 检查软件在 Windows、Linux 等系统上的兼容性与依赖完整性。

---
## 技术分析

#### 架构特点

从仓库结构分析，该项目采用典型的模块化分层架构。核心层由 Python 实现，负责 OCR 引擎调用和业务逻辑处理；表现层使用 Qt/QML 构建跨平台图形界面。项目中 qt_res 目录存放 QML 资源文件，py_src 目录包含 Python 源代码，这种前后端分离的设计便于维护和扩展。推测其架构遵循 MVC 模式，QML 负责视图渲染，Python 后端处理数据和控制逻辑，通过信号槽机制实现解耦。

#### 核心能力

基于仓库描述，该工具提供以下核心功能：支持截屏即时识别和图片批量导入，可处理 PDF 文档并排除水印、页眉页脚等干扰元素，内置二维码扫描与生成能力，预置多国语言识别模型。43,582 的星标数量表明其在开源社区具有较高认可度，功能完整性得到广泛验证。

#### 技术实现

推断其技术栈包含以下关键组件：底层 OCR 引擎可能基于 PaddleOCR 或 Tesseract 等成熟开源方案，支持离线运行意味着模型已本地化部署；Qt 框架保证跨平台兼容性，可部署于 Windows、Linux、macOS 系统；PDF 处理可能集成 pdf2image 或 PyMuPDF 等库；二维码功能可能采用 zxing 或 pyzbar。模块化设计使各功能组件可独立替换，便于后期升级优化。

#### 适用场景

该工具适合需要本地化文档数字化的个人用户或小型团队，尤其适用于网络受限环境下的批量图片文字提取、教育资料整理、无纸化办公流程构建。其离线特性确保数据隐私，适合处理敏感文档。二维码功能可满足轻量级标签生成与批量扫描需求。

#### 不适用场景

对于需要云端 AI 辅助的高精度识别、专业印刷体排版分析、复杂表格结构提取等场景，该工具可能存在局限。其设计目标侧重于通用场景，对于专业出版级 OCR 需求，建议考虑商业解决方案。此外，若需要实时多语言互译或与云服务深度集成，该离线工具并非最优选择。

#### 学习建议

对于希望深入研究的开发者，建议重点关注以下方面：模块化架构的接口设计模式、Qt/QML 与 Python 的交互机制、离线模型的压缩与部署策略、二维码识别算法的优化方法。可通过阅读 py_src 目录下的源码理解业务逻辑实现，qt_res 目录学习界面开发实践。

#### 落地考虑

企业引入前应评估：现有 IT 环境的兼容性测试、批量部署的自动化方案、与现有系统的数据流对接方式。43k 星标的项目在稳定性和社区支持方面具备优势，但建议进行概念验证测试以确认特定使用场景的适配性。对于大规模部署，需考虑并发处理能力和结果导出格式的定制化需求。

---
## 学习要点

- Umi-OCR 是一款免费、开源、轻量化的离线 OCR 工具，支持 Windows 平台，无需联网即可运行。
- 采用深度学习模型，提供高识别准确率和快速处理速度，适用于大规模批量图片识别。
- 支持多语言识别，包括中文、英文、日文、韩文等常见语言，能够自动检测语言进行混合识别。
- 多种输入方式：截图快捷键、拖拽文件、剪贴板粘贴以及批量处理文件夹或 PDF，满足不同使用场景。
- 输出灵活，可直接生成纯文本或结构化 JSON，方便后续编辑或程序对接。
- 完全离线运行，保护用户隐私，且无广告、无捆绑软件，使用体验清爽。
- 活跃的社区维护，持续更新功能并提供详细的使用文档和示例代码，便于二次开发。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [OCR文字识别](/tags/ocr%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [Python](/tags/python/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [PDF](/tags/pdf/) / [截屏](/tags/%E6%88%AA%E5%B1%8F/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [crawl4ai：面向AI时代的LLM友好型数据采集工具]({{< relref "posts/20260226-juejin-crawl4aiai时代的数据采集利器从入门到实战-0.md" >}})
- [面向智能体的音频工具包]({{< relref "posts/20260301-hacker_news-show-hn-audio-toolkit-for-agents-9.md" >}})
- [Sarvam 105B：首个具备竞争力的印度开源大模型]({{< relref "posts/20260307-hacker_news-sarvam-105b-the-first-competitive-indian-open-sour-16.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*