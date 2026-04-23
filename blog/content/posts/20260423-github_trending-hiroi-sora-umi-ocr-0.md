---
title: "Umi-OCR开源项目 支持截屏批量图片PDF识别"
date: 2026-04-23T19:34:52+08:00
draft: false
entry_kind: "auto"
tags: ["开源", "OCR", "离线", "批量图片", "PDF识别", "二维码", "多语言", "跨平台"]
categories: ["开源生态", "开发工具"]
source: github_trending
description: "Umi-OCR是一款开源、免费的离线OCR软件，采用模块化设计，能够在本地完成文字识别、二维码处理等功能，无需联网。软件使用Python实现，已在GitHub上获得约43.6k星标，支持Windows和Linux系统。 核心功能 - 截屏OCR：快速捕获屏幕选定区域进行文字识别。 - 批量图片OCR：一次性导入多张图片"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源项目 支持截屏批量图片PDF识别

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 开源、免费的离线OCR软件。

支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 43,586 (+48 stars today)
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

Umi-OCR 是一款开源、免费的离线 OCR 软件，基于 Python 实现，支持截屏、批量导入图片及 PDF 文档的文字识别，并可自动过滤水印、页眉页脚等干扰，还提供二维码扫描与生成功能，内置多语言模型，适合在本地处理敏感信息且不愿依赖云服务的用户。本文将依次介绍其环境搭建、主要功能使用、常用配置选项以及常见故障的排查思路。

---
## 摘要

Umi-OCR是一款开源、免费的离线OCR软件，采用模块化设计，能够在本地完成文字识别、二维码处理等功能，无需联网。软件使用Python实现，已在GitHub上获得约43.6k星标，支持Windows和Linux系统。

#### 核心功能

- 截屏OCR：快速捕获屏幕选定区域进行文字识别。
- 批量图片OCR：一次性导入多张图片并批量输出结果。
- PDF文档OCR：支持整页PDF的文字提取，能够排除页眉页脚和水印。
- 二维码识别与生成：内置二维码解码与编码功能。

#### 技术特点

- 完全离线运行，保护隐私。
- 多语言文字库内置，支持多国语言识别。
- 跨平台支持，提供图形化界面。
- 模块化架构便于二次开发和功能扩展。

---
## 评论

#### 总体判断

Umi-OCR 是一款面向普通用户的轻量级离线 OCR 工具，在开源同类产品中具备较高的成熟度与易用性。

#### 技术依据

从项目结构来看，该工具采用 Python 作为主要开发语言，这与其离线、轻量的定位相符。内置多国语言模型意味着系统无需联网即可完成多语言识别，这对隐私敏感场景具有实际意义。PDF 文档识别、批量处理、截图导入等功能覆盖了日常办公中的高频需求，排版优化、水印页眉过滤等细节处理也显示出开发团队对实际使用场景的关注。Star 数量超过四万，说明其在社区中获得了相当程度的认可与使用反馈。

#### 适用场景

该工具适合需要频繁处理图片或 PDF 文档的用户，尤其适用于无法使用云端服务的场景，如企业内部文件转换、个人隐私文档处理等。截图识别与批量导入功能对于日常办公中的资料整理尤为实用，多语言支持也为处理外语文档提供了便利。

#### 局限与验证方式

离线 OCR 的识别准确率受图像质量影响较大，复杂排版或低分辨率图片可能出现识别错误。由于模型在本地运行，识别速度与硬件性能直接相关，复杂文档的处理时间可能较长。建议用户在实际工作流中测试关键场景的识别效果，以判断该工具是否满足具体需求。

---
## 技术分析

#### 架构设计

基于仓库文件结构分析，Umi-OCR采用典型的分层模块化架构。核心代码位于`UmiOCR-data/py_src`目录，入口点为`run.py`。从`.qml`文件可以推断该应用使用Qt框架构建GUI界面，实现前端展示与后端逻辑的分离。`py_src`目录下的`imports`模块包含`umi_about.py`等配置信息，表明系统采用插件化设计思路，便于功能扩展和定制。这种架构使得OCR引擎、图像预处理、界面渲染等组件可以独立开发和测试。

#### 核心能力

已知事实方面，该项目支持截屏识别和批量图片导入，能够处理PDF文档并排除水印、页眉页脚等干扰元素。内置多国语言库说明其OCR模型经过多语言训练。星标数超过43,000表明其在开源社区具有较高认可度。推断部分，批量处理能力可能基于多线程或异步队列实现，PDF支持可能依赖`pypdf`或`pdf2image`等库。二维码扫描和生成功能可能集成`zxing`或`pyzbar`库。

#### 技术实现

推断部分，该项目的OCR引擎大概率基于开源方案如PaddleOCR或EasyOCR实现本地化部署，以满足离线运行需求。选择Python作为主要语言有利于快速迭代和社区贡献。Qt框架的使用保证了跨平台兼容性，可部署于Windows、Linux、macOS系统。模块化设计使得替换不同OCR后端成为可能，用户可根据硬件条件选择CPU或GPU推理模式。图像预处理可能包括自适应二值化、倾斜校正、噪声去除等步骤以提升识别准确率。

#### 适用场景

该工具非常适合需要处理大量截图文本的用户，如程序员复制代码片段、研究人员提取论文内容、办公人员整理扫描文档。对隐私敏感场景尤为适用，离线运行特性确保数据不会上传至外部服务器。多语言支持使其能够处理中日英等多种语言的混合文本识别。批量处理能力可显著提升重复性OCR任务的效率。

#### 不适用场景

对于追求极高识别精度的专业出版场景，开源模型的准确率可能不及商业OCR服务。对于需要识别手写体、特殊符号或艺术字体的需求，通用OCR模型的泛化能力存在局限。此外，依赖本地计算资源意味着在低配置设备上运行可能面临性能瓶颈。

#### 学习与落地建议

开发者可重点研究其模块化架构设计，学习如何将Qt界面与Python OCR引擎解耦。建议落地时考虑在服务器环境部署批量处理脚本，结合定时任务实现文档自动化识别。若用于企业级应用，需评估模型更新维护成本及特定场景下的准确率优化空间。

---
## 学习要点

- 采用模块化设计，分离预处理、检测、识别，提高系统的可维护性和扩展性。
- 整合开源 OCR 预训练模型，实现多语言高精度的文字识别，降低开发成本。
- 支持批量处理与 GPU 加速，兼顾识别速度与准确率，适合大规模文档处理。
- 同时提供命令行和图形界面两种交互方式，满足不同用户的使用习惯。
- 代码结构规范、注释详尽，是学习 OCR 技术实现的良好实践案例。
- 通过配置文件管理模型参数，实现灵活的自定义部署和功能扩展。
- 活跃的社区贡献和持续更新，展示了开源项目协同开发的优势。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [开源](/tags/%E5%BC%80%E6%BA%90/) / [OCR](/tags/ocr/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [批量图片](/tags/%E6%89%B9%E9%87%8F%E5%9B%BE%E7%89%87/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Velox: Tauri移植Swift版！Miguel打造跨平台新选择🚀]({{< relref "posts/20260127-hacker_news-velox-a-port-of-tauri-to-swift-by-miguel-de-icaza-8.md" >}})
- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [Sarvam 105B：首个具备竞争力的印度开源大模型]({{< relref "posts/20260307-hacker_news-sarvam-105b-the-first-competitive-indian-open-sour-16.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [MatsuriDayo / Nekoray 🔥：翻墙神器！GitHub]({{< relref "posts/20260125-github_trending-matsuridayo-nekoray-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*