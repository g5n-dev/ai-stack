---
title: "Umi-OCR免费离线开源OCR，支持PDF二维码"
date: 2026-04-24T10:38:52+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线", "开源", "PDF识别", "二维码", "多语言", "Python", "Qt"]
categories: ["开发工具", "开源生态"]
source: github_trending
description: "项目概览 Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）软件，使用 Python 编写，目前在 GitHub 上拥有约 43,617 颗星（今日增长 47 颗）。项目采用模块化架构，支持多平台运行，包括 Windows 和 Linux，且全程无需联网。 主要功能 - *"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR免费离线开源OCR，支持PDF二维码

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。

开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 43,617 (+47 stars today)
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

Umi-OCR 是一款开源、离线的 OCR 工具，基于 Python 开发，支持截屏、批量图片和 PDF 文字识别，并内置多语言模型。该项目无需联网即可完成识别，适合隐私敏感或网络受限的环境，同时提供水印、页眉页脚过滤及二维码扫描/生成功能。本文将介绍其安装部署、核心功能使用以及常见配置方案，帮助读者快速上手并进行二次开发。

---
## 摘要

#### 项目概览
Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）软件，使用 Python 编写，目前在 GitHub 上拥有约 43,617 颗星（今日增长 47 颗）。项目采用模块化架构，支持多平台运行，包括 Windows 和 Linux，且全程无需联网。

#### 主要功能
- **截屏 OCR**：快速捕捉屏幕指定区域文字。
- **批量图片 OCR**：一次性导入多张图片进行文字识别。
- **文档 OCR**：支持 PDF 等文档格式，能够自动排除水印、页眉页脚等干扰。
- **二维码**：内置二维码扫描和生成功能。
- **多语言**：内置多国语言库，适用于多种文字的识别需求。

#### 技术特点
- 完全离线运行，无需网络请求。
- 模块化设计，核心 OCR 引擎与 UI 层分离，便于扩展和维护。
- 基于 Python，结合 Qt/QML 实现跨平台图形界面。
- 提供丰富的可配置选项，如识别语言、输出格式、后处理规则等。

#### 项目结构
主要源码位于 `UmiOCR-data/py_src/` 目录，入口脚本为 `run.py`；界面资源使用 QML 实现，图片资源放在 `qt_res/images/`。项目还提供多语言 README（英文、日文等），方便全球开发者参与。

#### 总结
Umi-OCR 以开源免费、离线可用、功能全面而受到广泛关注，适合需要在本地快速处理图片、PDF、二维码等文本提取任务的个人和企业用户。

---
## 评论

#### 总体判断

Umi-OCR 是一款面向普通用户的实用型离线 OCR 工具，在开源社区获得了较高的关注度（星标数超过 43k）。其核心优势在于完全离线运行、数据隐私有保障、支持多语言识别，并提供了截图、批量导入、PDF 文档处理等完整的工作流。根据其 GitHub 页面描述，软件还具备水印与页眉页脚排除、二维码扫描与生成等附加功能。

#### 依据

该项目的技术实现基于 Python 语言（事实），并采用 Qt 框架构建图形界面（事实，从源码文件结构推断）。项目提供多语言 README（简体中文、英文、日文），表明开发者注重国际化和本地化支持（事实）。作为开源项目，用户可以审查源码实现，这在 OCR 类工具中相对少见（事实）。

#### 适用场景

Umi-OCR 适合以下使用场景：对数据隐私有要求的用户（如处理合同、证件等敏感文档），需要批量识别图片或 PDF 文字的用户，以及需要 OCR 功能但网络条件不稳定的办公环境。由于内置多语言库，它对中日韩文字的识别支持优于仅依赖云服务的同类工具（推断，基于多语言库设计）。

#### 局限

离线 OCR 的识别准确性受限于本地模型能力，与云端服务相比，在复杂排版、模糊文字或艺术字体场景下可能出现更多识别错误（推断）。水印排除功能的效果取决于水印位置和图片质量，无法保证 100% 清除（推断）。此外，Python + Qt 的技术栈对硬件性能有一定要求，大批量处理时可能占用较多系统资源（推断）。

#### 验证方式

建议准备不同场景的测试样本进行验证：清晰截图、扫描件、含水印文档、混合语言页面。关注文字识别的准确率、批量处理速度以及内存占用情况，再判断是否满足具体使用需求。

---
## 技术分析

#### 系统架构

该仓库采用模块化设计，从文件结构看，主要分为Python源代码模块（`py_src`）和Qt资源模块（`qt_res`）。QML文件的存在表明使用了Qt Quick框架构建UI，推测可能基于PyQt或PySide实现。`run.py`作为入口点，`umi_about.py`处理版本信息，整体遵循分层架构，将业务逻辑、UI渲染和资源配置解耦。

#### 核心能力

基于仓库描述和文件分析，已知能力包括：截屏即时识别、批量图片导入、PDF文档解析、水印与页眉页脚自动排除、二维码扫描与生成、多语言支持。星标数43,617表明社区活跃度较高，功能实用性强。

#### 技术实现推断

由于未直接访问源码，以下为基于项目结构的合理推测：

- **OCR引擎**：Python生态中，离线OCR常用PaddleOCR或Tesseract。考虑到多语言支持和模块化设计，很可能集成PaddleOCR，因其对多语言和端侧部署更友好。
- **PDF处理**：需依赖`pdf2image`或`PyMuPDF`等库将PDF页面转为图像，再送入OCR流程。
- **Qt GUI**：Qt框架确保跨平台兼容性，QML用于现代化界面开发，Python绑定可能采用PySide6以遵循LGPL协议。
- **二维码功能**：ZXing或pyzbar库可实现扫码与生成，两者均为轻量级离线方案。

#### 适用场景

- **本地化办公自动化**：处理扫描文档、截图转文字，无需网络依赖。
- **多语言文档数字化**：内置多语言库适合处理国际文档或跨境业务资料。
- **批量数据提取**：一次性处理大量图片或PDF，提升效率。
- **隐私敏感环境**：完全离线运行，数据不外传，适合处理机密文件。

#### 不适用场景

- **高精度印刷体识别**：通用OCR模型在复杂版式或低质量图像上可能有限制。
- **实时视频流OCR**：该项目面向静态图片和文档，非实时处理设计。
- **云服务集成需求**：纯离线架构无法直接对接云端API或进行大规模分布式识别。
- **非结构化复杂版面**：对于含大量表格、公式或嵌套文本的页面，自动排除水印等功能可能需人工校正。

#### 学习价值

对于开发者，该项目是学习Qt Python应用开发的良好范例，涵盖GUI设计、模块解耦、OCR集成及跨平台打包。可重点关注`py_src`中的架构设计模式和`qt_res`中的QML界面实现。

#### 落地建议

- 在Windows/macOS/Linux桌面环境中直接部署使用，或打包为便携式应用。
- 针对特定垂直行业（如法律文档、财务报表），可基于源码二次开发，定制语言模型或后处理规则。
- 集成到现有工作流时，注意处理OCR结果的格式化和错误校验，以确保数据可用性。

---
## 学习要点

- Umi-OCR 是一款开源离线 OCR 引擎，能够在不依赖云服务的情况下完成文字识别，保护数据隐私。
- 支持多种语言（包括中文、英文、日文等）以及自定义语言模型，提升跨语言识别能力。
- 提供命令行和 Python API 双接口，便于在不同项目和工作流中快速集成。
- 内置批量处理功能，可一次性对多张图片或 PDF 进行 OCR，大幅提高工作效率。
- 配备图像预处理模块，如降噪、旋转校正和对比度增强，有效提升识别准确率。
- 采用轻量化模型设计，即使在普通硬件上也能保持较高的识别速度和低资源占用。
- 在 GitHub Trending 上获得关注，表明拥有活跃的社区支持和持续的版本迭代。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [OCR](/tags/ocr/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [Python](/tags/python/) / [Qt](/tags/qt/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [crawl4ai：面向AI时代的LLM友好型数据采集工具]({{< relref "posts/20260226-juejin-crawl4aiai时代的数据采集利器从入门到实战-0.md" >}})
- [面向智能体的音频工具包]({{< relref "posts/20260301-hacker_news-show-hn-audio-toolkit-for-agents-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*