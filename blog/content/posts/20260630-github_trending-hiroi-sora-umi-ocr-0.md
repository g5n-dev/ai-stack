---
title: "Umi-OCR开源离线OCR 支持截屏批量识别PDF二维码"
date: 2026-06-30T20:26:03+08:00
draft: false
entry_kind: "auto"
tags: ["离线OCR", "开源工具", "PDF识别", "二维码", "多语言", "批量处理", "截屏识别", "水印去除"]
categories: ["开发工具"]
source: github_trending
description: "项目概述 Umi-OCR 是一款免费、开源的离线 OCR 工具，使用 Python 开发，可在 Windows、Linux 等平台完整运行。软件支持截屏识别、批量图片处理、PDF 文档识别，能够自动去除水印、页眉页脚，并内置二维码扫描/生成功能和多语言文字库。 核心功能 - 截屏 OCR：快速捕获屏幕文字，适合即时翻译"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "效率工具", "桌面应用"]
---

# Umi-OCR开源离线OCR 支持截屏批量识别PDF二维码

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 45,692 (+30 stars today)
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

Umi-OCR 是一款免费、离线的 OCR 软件，支持截屏、批量导入图片和 PDF 文档，能够排除水印和页眉页脚，并内置多语言文字库，适合需要本地处理文本提取且对数据隐私有要求的用户。本文将介绍其安装与配置方法、核心功能的使用技巧以及常见问题的排查方案。阅读完本文后，读者可以快速上手，实现本地高效的文字识别与批量处理。

---
## 摘要

#### 项目概述
Umi-OCR 是一款免费、开源的离线 OCR 工具，使用 Python 开发，可在 Windows、Linux 等平台完整运行。软件支持截屏识别、批量图片处理、PDF 文档识别，能够自动去除水印、页眉页脚，并内置二维码扫描/生成功能和多语言文字库。

#### 核心功能
- 截屏 OCR：快速捕获屏幕文字，适合即时翻译或记录
- 批量图片识别：一次性处理多张图片，提高效率
- PDF 文档识别：直接读取 PDF 并提取文本，支持去除水印、页眉页脚
- 二维码识别与生成：内置 QR 码功能，满足条码需求
- 多语言支持：内置多种语言的 OCR 模型，适用于国际化文档

#### 技术特点
- 完全离线运行，无需网络连接
- 模块化架构，便于功能扩展与二次开发
- 基于 Python，跨平台兼容性好
- 社区活跃，星标约 45,700，持续更新维护

#### 适用场景
适用于需要对本地文档、图片或 PDF 进行文字提取、去水印、批量处理以及二维码操作的个人或企业用户，尤其适合对数据隐私和离线使用有要求的场景。

---
## 评论

#### 总体判断

Umi-OCR是一款成熟度较高的开源离线OCR工具，在同类开源项目中具有较高的完成度和实用性。其星标数达45,692，表明项目获得了社区的广泛认可。作为纯本地运行的软件，它在数据隐私保护方面具有天然优势，适合对云端处理存在顾虑的用户。

#### 技术优势与事实依据

根据项目README文档，该工具基于Python开发，采用Qt框架构建图形界面，支持截屏识别、批量图片导入以及PDF文档OCR处理。内置多国语言库是一大亮点，可满足国际化使用需求。官方明确标注支持排除水印、页眉页脚等功能，这表明开发者在文档处理细节上有针对性优化。从项目结构看，使用QML编写界面组件，体现了现代桌面应用的开发思路。

#### 适用场景推断

对于需要频繁处理扫描文档、截图文字提取或批量图片OCR的用户，该工具具有较高的实用价值。在没有网络连接或不便使用云服务的工作环境中，离线特性尤为重要。从社区反馈推断，其对中文识别进行了专项优化，在处理中文文档时可能优于通用型OCR服务。

#### 局限性说明

需要注意的是，作为开源项目，其OCR核心引擎的性能可能受限于开源模型的固有局限。离线运行虽然保障了隐私，但在复杂版式或低质量图像的处理精度上，可能不及商业云端服务。项目未明确标注其OCR引擎来源，这使得对识别效果的预判存在一定不确定性。

#### 验证建议

建议在正式使用前，准备若干实际业务中的典型样本进行测试，重点关注：复杂版式的表格识别准确率、手写字体的识别效果、PDF扫描件的水印排除能力。官方仓库提供了详细文档，可作为快速上手的参考。

---
## 技术分析

#### 系统架构

基于仓库文件结构分析，该项目采用模块化设计，主代码位于 `UmiOCR-data/py_src/` 目录。GUI层使用Qt框架（从 `.qml` 文件可知），实现了界面与逻辑的分离。核心OCR功能通过Python实现，这种架构既保证了跨平台兼容性，又便于后续功能扩展。

#### 核心能力

**文字识别**：支持截图和批量图片导入，能够处理PDF文档，并具备排除水印、页眉页脚等干扰元素的功能。内置多国语言库是重要特性，说明其语言模型经过针对性训练。

**二维码处理**：集成扫描和生成功能，扩展了传统OCR工具的应用边界，适合需要处理混合内容（文字+二维码）的场景。

**离线运行**：作为核心卖点，用户无需依赖云服务即可完成识别，数据全程本地处理。

#### 技术实现

从文件结构推断，该项目可能采用了以下技术方案：

**OCR引擎**：基于开源的PaddleOCR或类似框架，配合自定义的训练优化以提升识别准确率。多语言支持表明使用了多语言预训练模型。

**图像预处理**：包含水印和页眉页脚排除功能，可能通过图像处理算法（如边缘检测、版式分析）实现自动区域划分。

**GUI框架**：Qt QML的运用说明界面具有良好的响应式设计和流畅的动画效果，符合现代桌面应用体验。

#### 适用场景

- 需要处理敏感文档且禁止数据外传的政府部门或企业
- 个人用户批量识别截图、扫描件的日常办公场景
- 开发者集成OCR功能到本地工作流中
- 跨语言文档处理需求（项目内置多语言支持）

#### 不适用场景

- 超大规模文档处理（离线性能受限于本地硬件）
- 实时性要求极高的流式视频文字识别
- 需要持续更新模型以适应新字体、新语言的场景
- 复杂版式文档的全自动结构化提取（现有功能侧重文本提取）

#### 学习与落地建议

对于开发者而言，该项目是学习OCR工程化落地的良好范例。建议重点关注：模块化设计如何平衡功能扩展与代码维护性、离线场景下的性能优化策略、Qt界面与Python后端的高效交互模式。

企业落地时，可考虑将Umi-OCR部署为内部文档处理工具的基础平台，利用其开源特性进行定制化开发。需评估现有文档的格式复杂度和语言覆盖需求，必要时在现有模型基础上进行微调训练。

---
## 学习要点

- 基于深度学习的 OCR 引擎，支持日语、中文等多语言文字识别。
- 可离线运行，兼容 Windows、Linux 和 macOS，无需联网。
- 提供图形化界面（GUI）和命令行工具，满足不同使用场景。
- 支持批量图片处理和多页 PDF 文档，提升工作效率。
- 支持 CPU 与 GPU 推理，兼具高效与灵活的资源利用。
- 轻量级模型设计，安装与部署简便，适合嵌入式和移动端。
- 开源活跃，文档齐全并持续更新，社区贡献丰富。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [离线OCR](/tags/%E7%A6%BB%E7%BA%BFocr/) / [开源工具](/tags/%E5%BC%80%E6%BA%90%E5%B7%A5%E5%85%B7/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [批量处理](/tags/%E6%89%B9%E9%87%8F%E5%A4%84%E7%90%86/) / [截屏识别](/tags/%E6%88%AA%E5%B1%8F%E8%AF%86%E5%88%AB/) / [水印去除](/tags/%E6%B0%B4%E5%8D%B0%E5%8E%BB%E9%99%A4/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/)

### 相关文章

- [Umi-OCR免费离线开源OCR，支持PDF二维码]({{< relref "posts/20260424-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [🚀测速神器！Cloudflare优选IP，一键提速你的网络🔥]({{< relref "posts/20260126-github_trending-xiu2-cloudflarespeedtest-5.md" >}})
- [🚀 Cloudflare测速神器！秒级优选最快IP，网速飞起！🔥]({{< relref "posts/20260127-github_trending-xiu2-cloudflarespeedtest-5.md" >}})
- [🚀网站合规必备！首个欧盟主权审计工具，你的网站合规了吗？]({{< relref "posts/20260127-hacker_news-show-hn-we-built-the-1-eu-sovereignty-audit-for-we-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*