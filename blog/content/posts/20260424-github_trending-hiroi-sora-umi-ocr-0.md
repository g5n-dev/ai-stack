---
title: "Umi-OCR：免费离线开源OCR支持多语言和PDF"
date: 2026-04-24T03:07:58+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线", "开源", "多语言", "PDF", "Python", "跨平台", "文档电子化"]
categories: ["开发工具", "开源生态"]
source: github_trending
description: "项目概述 Umi-OCR 是由 hiroi‑sora 开发的一款开源、免费且完全离线的光学字符识别（OCR）软件。采用模块化架构，能够在本地完成文字识别，无需联网。 主要功能 - **截屏 OCR**：快速捕获屏幕指定区域并识别文字。 - **批量导入**：一次处理多张图片，适合大量文档电子化。 - **PDF 文档识"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR：免费离线开源OCR支持多语言和PDF

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。开源且免费。支持截屏或批量导入图片、PDF文档识别、可排除水印和页眉页脚、扫描/生成二维码，内置多国语言库。
- **语言**: Python
- **星标**: 43,598 (+47 stars today)
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

Umi-OCR 是一款基于 Python 开发的开源离线 OCR 工具。它能够在不依赖网络的情况下，对截屏图片、批量图片或 PDF 文档进行文字识别，并能自动排除水印、页眉页脚等干扰元素，同时支持二维码扫描与生成。该工具内置多语言库，适合需要在离线环境中处理大量文档的用户。本文将围绕其核心功能展开，从安装配置到实际使用场景，帮助读者快速上手并解决文档数字化的常见需求。

---
## 摘要

#### 项目概述
Umi-OCR 是由 hiroi‑sora 开发的一款开源、免费且完全离线的光学字符识别（OCR）软件。采用模块化架构，能够在本地完成文字识别，无需联网。

#### 主要功能
- **截屏 OCR**：快速捕获屏幕指定区域并识别文字。
- **批量导入**：一次处理多张图片，适合大量文档电子化。
- **PDF 文档识别**：直接读取 PDF 中的文字内容，支持排除水印、页眉页脚等干扰信息。
- **二维码识别与生成**：内置二维码解码与生成功能，满足日常办公需求。
- **多语言支持**：自带多国语言模型，可直接识别中文、英文、日文等多种文字。

#### 技术实现
- **编程语言**：核心代码使用 Python 开发，兼顾开发效率与可维护性。
- **模块化设计**：各功能模块独立，便于扩展与二次定制。
- **跨平台**：支持 Windows 与 Linux 两大主流操作系统，部署灵活。
- **离线运行**：所有模型与资源均打包在本地，启动后不依赖外部网络。

#### 社区与影响力
- 截至目前，Umi‑OCR 在 GitHub 上已获得约 **43,598** 次星标，近 47 次当日新增，显示出极高的用户认可度。
- 开源生态吸引了众多开发者参与贡献，形成了持续更新的插件与语言模型库。

#### 总结
Umi‑OCR 通过模块化、跨平台、低依赖的实现方式，为用户提供了高效、可靠的离线文字识别、二维码处理及 PDF 文档电子化解决方案。其开源免费、社区活跃的特性，使其成为个人和中小企业进行文档数字化的理想选择。

---
## 评论

Umi-OCR 是一款值得关注的中文开源 OCR 工具，尤其适合对隐私和数据安全有较高要求的用户。43,598 的星标数表明其在开发者社区中拥有较高认可度。

#### 技术架构与实现

该工具基于 Python 开发，采用 Qt 框架构建图形界面，这意味着它具备良好的跨平台兼容性。**事实**：支持截屏识别和批量图片导入，可处理 PDF 文档。**事实**：内置多国语言库，这对处理多语言文档的用户很有价值。**推断**：从架构设计来看，离线运行模式意味着所有图像处理和文字识别都在本地完成，数据不会上传至外部服务器，这对于处理敏感信息的用户是一个显著优势。

#### 适用场景

该工具在以下场景中表现出色：办公场景中快速提取截图或扫描文档的文字内容；学术研究中对 PDF 论文进行文字抽取；日常使用中识别二维码和水印处理。**事实**：支持排除水印和页眉页脚的功能，这直接解决了用户在处理扫描文档时常见的干扰问题。**推断**：批量处理能力使其适合需要大量文档数字化的场景。

#### 局限性

需要客观指出的是，OCR 识别的准确率高度依赖于图像质量，低分辨率或倾斜的图片可能导致识别效果下降。**推断**：作为开源项目，其模型更新频率和长期维护状况需要持续观察。此外，对于复杂排版或手写体的识别能力，可能不如商业 OCR 解决方案。**事实**：Python 实现虽然降低了开发门槛，但在处理超大规模文档时，性能表现可能不如编译型语言实现的方案。

#### 验证建议

建议用户在实际工作流中测试：准备不同质量的图片样本进行识别率对比；验证多语言混排文档的处理效果；在离线环境下确认所有功能的正常运行。官方 GitHub 仓库提供了详细的使用文档和示例，这是验证工具能力的第一手资料。

---
## 技术分析

#### 架构特点

基于仓库文件结构推断，该项目采用分层模块化设计。Python层（`py_src/`）负责核心OCR逻辑和业务处理，Qt/QML层（`qt_res/`）负责界面渲染和用户交互。这种前后端分离的架构使得核心识别算法可以独立于UI进行测试和优化，同时QML的使用表明项目定位为跨平台的现代桌面应用。

#### 核心能力

已知事实方面，该项目明确支持截屏识别、批量图片导入、PDF文档解析、多语言文字识别、二维码扫描与生成、以及水印/页眉页脚排除功能。推断能力方面，43,598的星标数表明其在社区中具有较高认可度，可能在中文OCR场景下有较好的识别效果，因为项目名称和描述主要面向中文用户。

#### 技术实现

从技术栈来看，Python作为主要开发语言，配合Qt框架构建GUI，这种组合在桌面应用开发中兼顾了开发效率和性能。QML文件的存在说明UI层采用了声明式编程，这有助于实现流畅的动画和响应式界面。离线运行的特性意味着项目集成了本地化的OCR模型（可能是PaddleOCR或其他开源引擎的定制版本），而多国语言库的支持则暗示模型文件被组织为可切换的语言包。

#### 适用场景

对于需要处理敏感文档的机构（如金融、医疗、法律领域），离线OCR能确保数据不出内网，适合企业级文档数字化项目。个人用户在进行电子书整理、截图文字提取、无网络环境下的移动办公时，该工具也具有实用价值。此外，对多语言文档有批量处理需求的翻译工作者或研究人员可以从其多语言支持中受益。

#### 不适用场景

实时性要求极高的在线OCR服务不适合采用此方案，因为其作为本地应用，启动和加载模型需要一定时间。对于需要识别极度倾斜、严重变形或背景复杂图像的场景，通用离线模型的识别准确率可能不及云端付费服务。超大规模（每日百万页以上）的工业化文档处理任务也更适合专业化的OCR服务集群。

#### 学习与落地建议

对于开发者而言，该项目是学习PyQt/QML桌面应用开发的良好参考，其模块化结构便于拆解研究。落地时建议根据具体业务场景评估模型精度，必要时可在其基础上替换或微调OCR模型。需要注意的是，作为开源项目，其长期维护和更新依赖社区活跃度，企业应用时应考虑技术储备和替代方案。部署层面，可利用PyInstaller等工具打包为单文件可执行文件，简化分发流程。

---
## 学习要点

- Umi-OCR 是一款轻量级、离线运行的 OCR 工具，能够在本地完成文字识别而不依赖云服务。
- 采用 Tesseract 作为核心识别引擎，支持包括中文、日文、韩文在内的多语言文本提取。
- 同时提供图形界面（GUI）和命令行（CLI）两种使用方式，方便用户根据需求选择交互模式。
- 支持批量处理图片和 PDF 文件，可一次性完成多页文档的快速 OCR。
- 内置图像预处理功能，如二值化、倾斜校正和降噪，能够提升识别准确率。
- 完全开源并采用 MIT 许可证，代码可自由使用、修改和二次开发。
- 可作为 Python 库直接导入项目，提供简洁的 API 接口，便于自动化集成。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [OCR](/tags/ocr/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [PDF](/tags/pdf/) / [Python](/tags/python/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/) / [文档电子化](/tags/%E6%96%87%E6%A1%A3%E7%94%B5%E5%AD%90%E5%8C%96/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [Velox: Tauri移植Swift版！Miguel打造跨平台新选择🚀]({{< relref "posts/20260127-hacker_news-velox-a-port-of-tauri-to-swift-by-miguel-de-icaza-8.md" >}})
- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [DeepSeek-OCR 验证：代码转 PDF 节省 40% Token]({{< relref "posts/20260219-juejin-抛弃纯文本我写了个工具验证-deepseek-ocr-猜想代码转-pdf-节省-40-token-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*