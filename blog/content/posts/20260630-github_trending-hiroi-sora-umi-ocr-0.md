---
title: "Umi-OCR开源免费离线文字识别工具支持多语言"
date: 2026-06-30T22:01:46+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线识别", "开源工具", "多语言", "文字识别", "Qt", "二维码", "PDF"]
categories: ["开源生态", "开发工具"]
source: github_trending
description: "项目概述 Umi‑OCR 是由 hiroi‑sora 开发的开源、免费、离线 OCR 工具，采用模块化架构，基于 Python 编写，支持 Windows 与 Linux 两大平台。截至目前，GitHub 星标数约 45.7k。 主要功能 - **截屏 OCR**：快速捕获屏幕内容并识别文字。 - **批量图片 OCR"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源免费离线文字识别工具支持多语言

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费且离线的 OCR 软件。开源、免费的离线 OCR 软件。支持截屏/批量导入图片，PDF 文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 45,694 (+30 stars today)
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

Umi-OCR 是一款开源、免费且完全离线的 OCR 工具，基于 Python 开发。它支持截屏、批量导入图片以及 PDF 文档识别，并能够自动去除水印、页眉页脚等干扰元素，适合在无网络或隐私要求严格的场景下使用。此外，内置多语言模型实现二维码的扫描与生成，兼容多种文字体系。本文将围绕其安装部署、核心功能实操以及常见问题的排查进行详细说明。

---
## 摘要

#### 项目概述
Umi‑OCR 是由 hiroi‑sora 开发的开源、免费、离线 OCR 工具，采用模块化架构，基于 Python 编写，支持 Windows 与 Linux 两大平台。截至目前，GitHub 星标数约 45.7k。

#### 主要功能
- **截屏 OCR**：快速捕获屏幕内容并识别文字。
- **批量图片 OCR**：一次导入多张图片，统一处理。
- **文档 OCR**：支持 PDF 等文档格式，可自动排除水印、页眉页脚。
- **二维码识别与生成**：内置 QR 码解码与生成功能。
- **多语言支持**：内置多国语言库，适用于不同文字体系。

#### 技术特点
- 完全离线运行，无需网络。
- 采用模块化设计，易于扩展和维护。
- 使用 Qt 构建图形界面，提供跨平台体验。
- 支持命令行与 GUI 两种交互方式。

#### 资源与社区
项目源码托管于 GitHub，包含 README、英文、日文等多语言说明文档，提供丰富的使用示例与插件接口，方便二次开发与社区贡献。

---
## 评论

#### 总体判断

Umi-OCR 作为一款拥有超过45,000星标的开源项目，其技术成熟度和社区认可度都达到了较高水平。推断其成功主要源于两个因素：一是精准定位了“离线免费OCR”这一细分需求，二是通过 Qt 框架实现了跨平台友好的图形界面。该工具在保证基础文字识别功能的同时，还加入了水印排除、PDF转文本、二维码处理等实用功能，形成了差异化的功能矩阵。事实层面，其架构采用 Python 语言配合 Qt/QML 实现，确保了代码的可维护性和界面的响应速度。

#### 技术实现

从源码结构来看，Umi-OCR 使用了模块化的设计思路，将 OCR 引擎、界面渲染、文件处理等组件解耦。基于 Python 的生态优势，该项目能够灵活集成多种开源 OCR 引擎（如 PaddleOCR、Tesseract 等），具体实现方式可能因版本而异。事实表明，采用 Qt 框架是该项目的关键技术选择，这使其具备原生级的性能表现和一致的跨平台体验。

#### 适用场景

推断以下场景能够充分发挥该工具的价值：办公场景中频繁处理扫描文档、截图转文字、批量图片数字化等需求；隐私敏感环境下（如企业内部文档、医疗记录）无法使用云端 OCR 服务的情况；以及需要长期归档大量纸质材料但网络条件不稳定的场景。对于日常偶尔使用的轻度用户，其截屏快捷识别的功能设计也提供了便捷的入口。

#### 局限与验证方式

需要客观认识其局限性：推断 OCR 的识别准确率仍受限于图片质量、字体复杂度和语言支持范围，具体表现需要实际测试。事实层面，离线部署虽然保障了数据安全，但也意味着无法享受云端服务的持续模型迭代带来的精度提升。建议用户从三个维度验证其实用性：首先测试常见文档（黑白打印、彩色杂志、网页截图）的识别准确率；其次验证批量处理大文件时的性能表现和资源占用；最后确认特定功能（如表格还原、多语言混排）是否符合预期需求。

---
## 技术分析

#### 架构特点

基于仓库结构分析，Umi-OCR采用模块化分层设计。核心层由Python实现，负责OCR引擎调用和数据处理；界面层使用Qt/QML构建跨平台图形交互。这种设计将识别算法与用户界面解耦，便于独立升级维护。从目录结构看，资源文件与源码分离，包含多语言说明文档和独立的数据配置，说明项目在国际化方面有系统性考虑。

#### 核心能力

已知事实方面，该项目支持截屏识别和批量图片导入，能够处理PDF文档并具备二维码扫描生成功能。内置多国语言库使其可应对跨语言场景。仓库描述中提到的“水印/页眉页脚排除”功能暗示具备版面分析能力，可智能区分主体内容与干扰元素。这些能力组合起来，覆盖了日常办公和轻度文档数字化的主流需求。

#### 技术实现推断

从技术栈推断，Python作为主语言大概率用于调用PaddleOCR或类似开源OCR引擎实现文字识别。Qt框架负责GUI渲染，可能采用QML实现现代化界面。离线特性意味着所有模型文件预装在本地，这对部署体积和内存占用有一定要求。项目采用打包成可执行文件的分发方式，降低了用户的使用门槛。

#### 适用场景

隐私敏感环境是首选场景，如企业内部文档、医疗记录、金融凭证等不宜上传云端的材料处理。批量自动化场景同样契合，支持文件夹监控或脚本调用实现无人值守处理。开发者和研究者可用于学习OCR技术原理，快速验证算法效果。此外，对网络不稳定或完全离线的特殊工作环境（如野外作业）具有独特价值。

#### 不适用场景

复杂排版或艺术字体识别效果可能有限，依赖底层模型能力而非该项目优化。超大规模工业化OCR处理（如每日百万级文档）应考虑商业方案或自建云服务。实时视频流文字识别并非设计目标，缺乏帧处理优化。表格结构还原需求需要额外开发，当前仅提供文字提取。

#### 学习与落地建议

学习路径上，建议从源码结构入手，理解模块间数据流设计；重点研究OCR引擎封装层如何实现参数配置和结果后处理；Qt/QML部分可作为桌面应用开发参考。落地应用时，可结合企业现有工作流进行定制开发，例如集成到内部系统的文档上传环节；利用其批量处理能力构建自动化归档工具；对于多语言场景，可测试中文简繁体和日文混合文档的识别效果。项目开源特性允许在合规前提下进行二次开发或技术借鉴。

---
## 学习要点

- Umi-OCR 是一款开源离线 OCR 工具，支持多语言文字识别，适合快速提取图像中的文字。
- 项目基于 Python 与深度学习框架（如 PaddleOCR）实现，具备高识别准确率和跨平台运行能力。
- 提供图形界面和命令行两种使用方式，便于批量处理图片或集成到自动化流程中。
- 通过 GPU 加速显著提升 OCR 速度，同时兼容 CPU 环境，满足不同硬件需求。
- 代码采用模块化和插件化设计，使新增语言或模型非常简单，降低二次开发门槛。
- 项目使用 MIT 许可证，文档详尽并配有示例，帮助新手快速上手并参与贡献。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [OCR](/tags/ocr/) / [离线识别](/tags/%E7%A6%BB%E7%BA%BF%E8%AF%86%E5%88%AB/) / [开源工具](/tags/%E5%BC%80%E6%BA%90%E5%B7%A5%E5%85%B7/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [文字识别](/tags/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB/) / [Qt](/tags/qt/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [PDF](/tags/pdf/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR免费离线开源OCR，支持PDF二维码]({{< relref "posts/20260424-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [PP-OCRv6登陆Hugging Face：支持50语言OCR]({{< relref "posts/20260622-blogs_podcasts-pp-ocrv6-on-hugging-face-50-language-ocr-from-15m--0.md" >}})
- [DeepSeek-OCR 验证：代码转 PDF 节省 40% Token]({{< relref "posts/20260219-juejin-抛弃纯文本我写了个工具验证-deepseek-ocr-猜想代码转-pdf-节省-40-token-3.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*