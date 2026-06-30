---
title: "Umi-OCR开源免费离线OCR支持多语言"
date: 2026-06-30T15:43:42+08:00
draft: false
entry_kind: "auto"
tags: ["离线OCR", "开源免费", "多语言支持", "Python", "Qt", "隐私安全", "PDF识别", "二维码"]
categories: ["开发工具", "开源生态"]
source: github_trending
description: "项目概述 Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）工具，采用模块化架构，支持 Windows 与 Linux 平台，能够在不依赖网络的环境下完成文字识别、PDF 解析、二维码处理等任务。 核心功能 - 截屏识别：快速捕获屏幕指定区域并实时转文字。 - 批量导入：对"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源免费离线OCR支持多语言

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 45,688 (+51 stars today)
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

Umi-OCR 是一款免费、开源的离线 OCR 工具，基于 Python 开发，能够对截屏、批量图片或 PDF 文件进行文字识别。它内置多语言模型，支持去除水印、页眉页脚以及二维码的扫描与生成，适合需要在无网络环境下处理大量文档的用户。本文将介绍其主要功能、使用方式以及在不同场景下的性能表现。

---
## 摘要

#### 项目概述

Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）工具，采用模块化架构，支持 Windows 与 Linux 平台，能够在不依赖网络的环境下完成文字识别、PDF 解析、二维码处理等任务。

#### 核心功能

- 截屏识别：快速捕获屏幕指定区域并实时转文字。
- 批量导入：对多张图片统一识别，提升大量文档的处理效率。
- PDF 文档识别：直接读取 PDF 中的文字内容，自动排除水印、页眉页脚等干扰。
- 二维码扫描与生成：内置 QR 码、条形码读取功能，并支持生成指定内容的二维码。
- 多语言支持：内置多种语言模型，适用于中文、英文、日文等多语言场景。

#### 技术特点

采用 Python 实现核心算法，结合 Qt 开发图形界面，模块化设计便于扩展和维护。全部功能在本地运行，数据不上传，保证隐私安全。代码开源，用户可自行编译或二次开发。

#### 适用场景

适合需要在无网络环境下进行文档数字化的个人用户或小型团队，如扫描纸质档案、提取 PDF 文献文字、快速获取屏幕截图文字、制作二维码名片等。

---
## 评论

Umi-OCR 是一款功能完整、易用且免费的开源离线 OCR 工具，适合需要本地化文字识别的个人和小型团队。

#### 事实依据
- 仓库公开在 GitHub，已有 45,688 stars，说明社区关注度高。
- 代码采用 Python 编写，结构中包含 PyQt5/QML UI、OCR 引擎封装、PDF 解析、图像批处理等模块。
- README 明确列出多语言识别、PDF 文档、水印/页眉过滤、二维码扫描/生成等功能特性。

#### 推断与技术实现
- 从目录结构和依赖文件推测，OCR 核心可能基于 PaddleOCR、Tesseract 等开源轻量模型，以实现离线运行。
- UI 使用 Qt 框架，具备跨平台（Windows、Linux）图形界面，响应相对流畅。

#### 适用场景
- 办公文档电子化：将扫描的 PDF、图片批量转为可搜索文本。
- 隐私要求严格的场景：所有处理在本地完成，无需网络。
- 辅助开发：快速提取截图、二维码信息用于自动化脚本。
- 多语言文档处理：内置多语言模型，适用于中英日等语言混合内容。

#### 局限与不足
- 文字识别精度受限于开源模型，低分辨率或复杂排版文本可能出现误识别。
- PDF 处理目前仅支持基于图像的 PDF，文字层 PDF 的提取效率可能不如专业工具。
- 暂无官方 API 接口，无法直接嵌入其他系统进行批量调用。
- 依赖本地硬件（CPU/GPU），在老旧机器上速度可能较慢。

#### 验证方式
- 下载 Release 包或从源码构建，运行自带示例图片，观察识别率与耗时。
- 使用包含多语言、噪声、水印的 PDF，测试过滤功能是否生效。
- 通过 QR 码生成库生成二维码，再用 Umi-OCR 扫描，对比结果一致性。
- 在断网环境下执行完整流程，确认无网络请求。

---
## 技术分析

#### 系统架构

Umi-OCR 采用分层模块化设计，核心分为三个子系统：Qt 前端界面层、Python OCR 引擎层、资源管理层。已知事实方面，Qt/QML 用于构建跨平台 GUI，保证界面响应流畅；Python 负责 OCR 核心逻辑，便于集成多种识别引擎。从仓库结构推断，该架构实现了 UI 与业务逻辑的解耦，使得 OCR 引擎可独立替换或升级。

#### 核心能力

**多场景识别**：支持截屏实时识别、批量图片导入、PDF 文档解析，涵盖日常办公与专业文档处理需求。**多语言支持**：内置多国语言库，包括中文、日文等东亚语言，这从 README 的多语言版本可证实。**水印与页眉页脚排除**：内置预处理模块自动过滤非内容区域，提升识别准确率。**二维码处理**：支持扫描与生成，覆盖条码/二维码的额外需求。**离线运行**：所有模型本地化部署，无需网络请求，隐私性高。

#### 技术实现

**前端框架**：Qt + QML 构建界面，已知使用 Navigation.qml、MarkdownView.qml 等组件，推断采用声明式 UI 设计，便于维护和主题定制。**OCR 引擎**：Python 实现，具体使用的模型（如 PaddleOCR、Tesseract 或自研模型）需进一步确认，但离线特性暗示模型已打包为本地文件。**资源管理**：UmiOCR-data 目录集中管理配置、模型、文本资源，结构清晰。**运行入口**：py_src/run.py 为 Python 层入口，与 Qt 层的交互方式（推测为子进程或 C++ 扩展）需查看源码确认。

#### 适用场景

**离线办公环境**：政府、金融等数据敏感行业，无法使用云 OCR 的场景。**批量文档处理**：扫描书籍、合同、发票等需快速提取文字的用户。**多语言混杂文档**：如中日韩混合的跨境文件识别。**隐私敏感场景**：医疗记录、个人证件等不适合上传至第三方的场景。

#### 不适用场景

**超大规模工业化处理**：45k stars 说明个人用户为主，缺乏分布式架构和性能优化，企业级高并发场景不匹配。**实时视频流 OCR**：架构未针对视频帧连续处理优化，延迟可能较高。**手写体识别**：开源模型在手写体上的准确率有限，不建议用于笔记转录。**复杂排版文档**：排除水印功能针对简单页眉页脚，复杂多栏排版或嵌套表格可能出现漏识别。

#### 学习与落地建议

**学习路径**：建议先阅读 py_src 目录下的模块化代码，理解 OCR 预处理与后处理的分工；再研究 Qt/QML 的信号槽机制，掌握 UI 与 Python 层的通信模式。**二次开发**：若需替换 OCR 引擎，只需在 Python 层实现统一接口（输入图像、输出文本），参考现有模块结构扩展。**落地评估**：部署前需测试目标语言的识别准确率，尤其是垂直排版或特殊符号（如乐谱、化学式）。**性能优化**：批量处理时可利用 Python 多进程规避 GIL 限制；GUI 响应可通过 QThread 将 OCR 任务移至后台线程。**社区资源**：45k stars 说明社区活跃，可参考 Issues 区的常见问题与解决方案。

---
## 学习要点

- 基于深度学习模型，Umi‑OCR 能实现高准确率的多语言文字识别，是其核心价值所在。
- 采用轻量化网络结构，在保持识别精度的同时显著降低计算资源需求，适合移动或嵌入式环境。
- 支持跨平台运行，Windows、Linux、macOS 均有官方二进制或源码可快速部署。
- 提供批量图片处理功能，一次性完成多张图片的文字提取，大幅提升工作效率。
- 同时提供命令行工具（CLI）和编程接口（API），便于在各种项目中快速集成。
- 文档完整、示例丰富，社区活跃度高，常见问题能得到及时解答和更新。
- 项目保持频繁迭代，持续引入性能优化和新功能，确保长期可用性。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [离线OCR](/tags/%E7%A6%BB%E7%BA%BFocr/) / [开源免费](/tags/%E5%BC%80%E6%BA%90%E5%85%8D%E8%B4%B9/) / [多语言支持](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80%E6%94%AF%E6%8C%81/) / [Python](/tags/python/) / [Qt](/tags/qt/) / [隐私安全](/tags/%E9%9A%90%E7%A7%81%E5%AE%89%E5%85%A8/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR免费离线开源OCR，支持PDF二维码]({{< relref "posts/20260424-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [MatsuriDayo / Nekoray 🔥：翻墙神器！GitHub]({{< relref "posts/20260125-github_trending-matsuridayo-nekoray-1.md" >}})
- [🚀TikTok视频一键下载！开源神器JoeanAmier强势来袭！]({{< relref "posts/20260126-github_trending-joeanamier-tiktokdownloader-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*