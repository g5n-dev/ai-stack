---
title: "Umi-OCR：开源免费离线OCR支持PDF截屏识别"
date: 2026-07-01T04:20:27+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线识别", "开源工具", "Python", "Qt", "PDF识别", "隐私保护", "跨平台"]
categories: ["开发工具", "开源生态"]
source: github_trending
description: "项目概述 Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）软件，采用模块化架构，支持 Windows 与 Linux 平台，完全不依赖网络。编程语言为 Python，已获得约 45,700 星标，近 期每日增长约 34 星。 主要功能 - **截屏 OCR**：快速捕获屏"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR：开源免费离线OCR支持PDF截屏识别

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的 OCR 软件。 开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 45,703 (+34 stars today)
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

Umi-OCR 是一款免费、开源、离线的 OCR 软件，支持截屏、批量导入图片以及 PDF 文档的文字识别，并内置多国语言库，可自动过滤水印、页眉页脚，还具备二维码扫描和生成功能。该工具无需联网，适合对数据隐私有要求或需要在本地快速处理大量文本的用户。本文将介绍其安装方法、主要界面操作、常用配置以及实际场景的使用示例。

---
## 摘要

#### 项目概述
Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）软件，采用模块化架构，支持 Windows 与 Linux 平台，完全不依赖网络。编程语言为 Python，已获得约 45,700 星标，近 期每日增长约 34 星。

#### 主要功能
- **截屏 OCR**：快速捕获屏幕区域并即时识别文字。
- **批量图片 OCR**：一次性导入多张图片，统一处理并输出文本。
- **文档 OCR**：支持 PDF 等文档格式，可排除水印、页眉页脚等干扰。
- **二维码**：内置 QR 码扫描与生成功能。
- **多语言**：预置多国语言模型，满足不同文字识别需求。

#### 技术特点
- 完全离线运行，无需网络请求，保护隐私。
- 模块化设计，插件式扩展，方便二次开发与功能升级。
- 使用 Qt 框架构建 GUI，提供跨平台一致的交互体验。
- 支持自定义预处理（去噪、倾斜校正等）和后处理（语言模型校正），提升识别准确率。
- 代码结构清晰，源码公开在 GitHub，具备良好的文档与社区支持。

#### 适用场景
- 桌面文档数字化、截图文字提取、无网络环境下的 OCR 需求。
- 对隐私敏感或需要本地化处理的个人用户与企业。

Umi-OCR 兼具易用性、灵活性与可扩展性，是目前较为热门的开源离线 OCR 解决方案之一。

---
## 评论

#### 总体判断
Umi-OCR 作为一款开源、离线的 OCR 工具，在同类项目中具备较高的完成度与社区认可度。其开源免费、隐私友好、功能覆盖全面的定位，适合对本地化文字识别有需求的用户群体。

#### 事实依据
项目采用 Python 语言开发，星标数达 45,703，表明其在开源社区中拥有较大的用户基数。核心功能包括截屏识别、批量图片导入、PDF 文档处理、水印与页眉页脚排除、二维码扫描与生成、内置多语言库等，均已在仓库描述中明确列出。作为离线工具，所有数据处理均在本地完成，无需网络传输，这一特性可从其架构推断。

#### 适用场景
该工具在以下场景中具有明显优势：处理涉及敏感信息的文档时，本地识别可避免数据上传；预算有限或偏好开源解决方案的用户可免费使用；需要批量处理图片或 PDF 的重复性工作场景；以及对多语言文档的识别需求。内置二维码功能也可满足日常轻度使用。

#### 局限与注意事项
离线架构在保护隐私的同时，也意味着依赖本地模型能力上限，识别精度可能不及调用云端大模型的商业 OCR 服务。PDF 功能对纯图片型扫描文档的支持效果，取决于内置 OCR 引擎的版本与训练数据。用户应通过实际样本测试来验证具体场景的适用性。

#### 验证方式
建议下载最新发行版，使用不同分辨率、背景复杂度、文字排版的图片与 PDF 进行对照测试，重点评估识别准确率、排版保留程度及批处理速度，二维码功能则可选取不同格式进行扫描验证。

---
## 技术分析

#### 系统架构

从仓库结构和代码组织来看，Umi-OCR采用了典型的分层模块化架构。核心代码位于`UmiOCR-data/py_src/`目录下，通过`imports`模块管理依赖关系。主入口`run.py`负责应用启动流程，而Qt框架相关的资源文件（QML、图像资源）则独立存放于`qt_res`目录中。这种设计将业务逻辑与界面表现分离，便于维护和扩展。

**已知事实**：项目使用Python作为主要开发语言，Qt/QML用于构建跨平台图形界面，支持多语言文档（中文、英文、日文README）。

**推断**：模块化设计暗示该系统具备良好的可插拔性，可能便于后续集成新的OCR引擎或处理插件。

#### 核心能力

该OCR系统的功能边界相当清晰，主要聚焦于文档数字化处理流程：

**图像输入**方面，支持截屏实时捕获和批量图片导入，兼容PDF文档的页面级识别。**文本后处理**能力包括水印去除、页眉页脚自动排除，以及多语言文本的混合识别。**扩展功能**涵盖了二维码的扫描与生成，显示出该工具定位为综合性文档处理套件而非单一OCR工具。

**推断**：排除水印/页眉页脚的实现可能依赖于图像处理算法或模板匹配技术，而非简单的文本区域屏蔽。

#### 技术实现

基于仓库信息和Python语言选择，可以推断其技术栈可能包含以下关键组件：

**已知事实**：Python生态提供了丰富的OCR工具选择，如PaddleOCR、EasyOCR、Tesseract等开源项目。结合项目支持离线运行的特性，大概率采用本地化部署的OCR引擎而非云端API。

**推断**：考虑到45,703的星标数和离线特性，可能集成了轻量级的深度学习模型（如CRNN+CTC架构），以平衡识别准确率与运行效率。Qt/QML界面的选择可能基于跨平台需求（Windows/Linux/macOS）和对高性能渲染的追求。

**技术亮点推测**：多语言库的内置支持暗示项目可能实现了语言检测与模型动态加载机制，在启动时根据用户需求加载对应语言包以控制内存占用。

#### 适用场景

该工具在以下场景中具有明显优势：**办公自动化**场景下，可批量处理扫描文档、截图、PDF文件，提取关键信息用于后续编辑；**无网络环境**中，离线特性保证了数据隐私和持续可用性；**跨语言文档处理**，多语言库支持使其能够应对国际化办公需求；**结构化信息提取**，如从合同、发票、报告等固定格式文档中抽取目标字段。

#### 不适用场景

**高精度印刷体识别**：相比商业云服务，自训练模型的准确率可能存在差距，对极小字号或复杂排版的处理能力有限。**实时视频流处理**：OCR本质上是静态图像处理，不适合连续视频的文字实时叠加。**复杂表格结构恢复**：仅凭文本区域识别难以保证表格单元格的一一对应。**多语言混合排版**：当文档包含多种文字且混合穿插时，识别和断句可能出现问题。

#### 学习与落地建议

**学习价值**：该项目是了解OCR工程落地的优秀案例，涵盖图像预处理、文本识别、后处理的全流程设计。建议重点研究其模块间接口定义和资源管理策略。

**落地建议**：对于企业内部数字化转型，可将该工具作为文档扫描环节的预处理组件；教育机构可用于构建本地化学术资料库；在部署时建议评估具体语种的识别准确率，必要时进行针对性模型微调或混合使用商业OCR服务补充。

---
## 学习要点

- Umi-OCR 是一款轻量级、离线的 OCR（光学字符识别）工具，能够直接从图片中提取文字。
- 该项目基于深度学习框架（如 PaddleOCR）实现，提供高识别精度，尤其在中文和日文上表现优秀。
- 支持批量处理多张图片和 PDF 文件，适合大规模文档数字化的需求。
- 提供简洁的图形化用户界面（GUI），无需命令行即可完成 OCR 操作。
- 输出格式灵活，支持 TXT、JSON、Markdown 等多种文本格式，便于后续编辑和存档。
- 跨平台运行（Windows、Linux），并且代码开源免费，适合个人和商业项目使用。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [OCR](/tags/ocr/) / [离线识别](/tags/%E7%A6%BB%E7%BA%BF%E8%AF%86%E5%88%AB/) / [开源工具](/tags/%E5%BC%80%E6%BA%90%E5%B7%A5%E5%85%B7/) / [Python](/tags/python/) / [Qt](/tags/qt/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [隐私保护](/tags/%E9%9A%90%E7%A7%81%E4%BF%9D%E6%8A%A4/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR免费离线开源OCR，支持PDF二维码]({{< relref "posts/20260424-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR：开源免费离线OCR工具，支持PDF文档与二维码识别]({{< relref "posts/20260630-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [MatsuriDayo / Nekoray 🔥：翻墙神器！GitHub]({{< relref "posts/20260125-github_trending-matsuridayo-nekoray-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*