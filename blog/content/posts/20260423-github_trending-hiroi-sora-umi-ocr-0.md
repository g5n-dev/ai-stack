---
title: Umi-OCR：开源免费离线OCR工具，支持PDF文档与二维码识别
date: 2026-04-23 23:27:59+08:00
draft: false
entry_kind: auto
tags:
- 离线OCR
- PDF识别
- 二维码
- 开源工具
- 跨平台
- 多语言
- Python
- 批量处理
categories:
- 开发工具
- 开源生态
source: github_trending
description: Umi-OCR是一款开源、离线的OCR工具，基于Python开发，提供截屏、批量图片导入以及PDF文档的文字识别功能。它在本地完成识别，不依赖云服务，适合对数据隐私有要求或需要在无网络环境下工作的用户。项目内置多语言库，支持排除水印、页眉页脚以及二维码的扫描与生成。本文将依次介绍安装部署、核心功能使用以及进阶配置，帮助读者快速上手并充分利用该工具。
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios:
- 计算机视觉
- 桌面应用
- 效率工具
aliases:
- /posts/20260424-github_trending-hiroi-sora-umi-ocr-0/
- /posts/20260630-github_trending-hiroi-sora-umi-ocr-0/
- /posts/20260701-github_trending-hiroi-sora-umi-ocr-0/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR工具。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 45,696 (+30 stars today)
- **链接**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

---

## Overview

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

Umi-OCR是一款开源、离线的OCR工具，基于Python开发，提供截屏、批量图片导入以及PDF文档的文字识别功能。它在本地完成识别，不依赖云服务，适合对数据隐私有要求或需要在无网络环境下工作的用户。项目内置多语言库，支持排除水印、页眉页脚以及二维码的扫描与生成。本文将依次介绍安装部署、核心功能使用以及进阶配置，帮助读者快速上手并充分利用该工具。

---
## 摘要

#### 项目概述
Umi‑OCR（仓库 hiroi‑sora/Umi‑OCR）是一款开源、免费、离线的 OCR 工具，使用 Python 编写，GitHub 约 45,700 星。项目旨在提供无需网络的文字识别能力，支持截屏、批量图片、PDF 文档以及二维码处理。

#### 核心功能
- **截屏 OCR**：快速捕获屏幕文本，适合即时翻译或信息提取。
- **批量 OCR**：一次导入多张图片，自动排队识别，提升批量处理效率。
- **文档 OCR**：支持 PDF、电子书等文档，能够排除水印、页眉页脚等干扰。
- **二维码**：内置识别与生成功能，可处理常见的 QR 码。
- **多语言**：内置多国语言模型，覆盖简体中文、繁体中文、日文、英文等常见语言。

#### 技术特点
- **完全离线**：所有模型和资源随软件打包，无需联网。
- **模块化架构**：核心识别、界面、插件分离，便于二次开发和功能扩展。
- **跨平台**：支持 Windows 与 Linux，系统要求低，部署简便。
- **可配置**：用户可自定义识别区域、过滤规则、输出格式等参数。

#### 使用场景
适用于个人笔记、文档数字化、无网络环境的办公或科研场景，亦可作为二次开发者的 OCR 引擎集成到其他应用中。

该软件以易用性、灵活性和可扩展性为卖点，是当前开源社区中较受欢迎的离线 OCR 解决方案之一。

---
## 评论

#### 总体判断
Umi‑OCR是一款成熟、功能完整的开源离线OCR工具，拥有45 k+星标，社区认可度高。基于Python实现并使用Qt构建界面，提供截屏、批量图片、PDF识别、二维码扫描等实用特性，适合隐私或网络受限环境使用。

#### 技术依据与推断
* **事实**：仓库使用Python语言，代码结构清晰；README系列提供中、英、日多语言说明，UI采用Qt/QML实现。官方文档列出了截屏、批量导入、PDF解析、水印/页眉排除、二维码识别等功能。
* **推断**：从源码的依赖声明和OCR模块命名可推断可能基于Tesseract或类似开源引擎进行封装，从而实现离线识别。实际识别精度需在实际运行中测评。

#### 适用场景
1. **隐私或安全要求高的环境**——无需网络即可完成文字提取。
2. **日常文档批处理**——批量导入图片或PDF，排除页眉页脚，提高效率。
3. **快速截图OCR**——支持即时截取屏幕并输出文本，适合研发、客服等岗位。
4. **二维码/条形码识别**——内置功能可一次性处理多种码制。

#### 局限与风险
* **模型依赖**：离线模型对特殊字体、手写体或低分辨率图片的识别率可能下降，需自行替换或训练模型。
* **功能深度**：不支持表格结构化输出、版面布局分析等高级特性，若需复杂排版文档需配合其他工具。
* **更新频率**：开源项目更新依赖作者个人维护，长期兼容性需关注版本发布。

#### 验证方式
* 使用公开基准图片集（如ICDAR 2013）和自备的业务PDF，统计字符错误率（CER）和准确率。
* 对比相同图片在Umi‑OCR与在线OCR服务（如百度OCR）之间的差异。
* 在不同操作系统（Windows、Linux）下安装运行，检查依赖冲突与性能表现。

整体而言，Umi‑OCR在免费、离线、易用三个维度具备竞争力，适合对数据隐私有要求且对文字识别精度要求不是极其苛刻的用户。

---
## 技术分析

#### 架构特点

从仓库结构分析，Umi-OCR 采用分层模块化架构设计。核心代码位于 `UmiOCR-data/py_src/` 目录，其中 `imports/` 目录存放核心功能模块，`run.py` 作为主入口。界面层使用 QML（Qt Meta-object Language）实现，位于 `qt_res/qml/` 目录，这表明项目采用 Qt 框架构建跨平台图形界面。这种架构的优势在于业务逻辑与界面表现分离，便于后续功能扩展和维护。

#### 核心能力

基于仓库描述，该工具具备以下核心能力：支持截屏和批量导入图片进行 OCR 识别；能够处理 PDF 文档并提取文本；内置水印和页眉页脚排除功能，这对于从扫描文档中提取纯净文本尤为重要；集成二维码扫描和生成功能；内置多国语言识别库。从 45,696 的星标数来看，该项目在开源社区具有较高的认可度，成熟度相对较高。

#### 技术实现

从技术栈推断，项目主要使用 Python 作为后端开发语言，Qt 框架用于跨平台桌面应用开发。OCR 引擎方面，很可能集成了 PaddleOCR 或 EasyOCR 等开源方案，这些方案均支持离线运行且识别效果较好。二维码功能可能基于 zxing-cpp 或 pyzbar 库实现。模块化设计使得 OCR 引擎、图像预处理、文本后处理等环节相互独立，便于针对不同场景进行优化和替换。

#### 适用场景

该工具非常适合以下应用场景：对数据隐私有严格要求，需要离线处理敏感文档的政府或企业；个人用户需要快速从截图、扫描件中提取文字；需要批量处理图片或 PDF 文档的办公场景；需要排除页眉页脚干扰，提取文档主体内容；支持多语言文档识别的国际化业务需求。由于完全免费且开源，适合个人开发者和小型团队零成本部署。

#### 不适用场景

需要注意其局限性：对于需要处理极其复杂排版（如嵌套表格、多栏混合排版）的文档，识别效果可能不稳定；不提供云端 API 接口，无法直接集成到大型分布式系统中；对于实时视频流 OCR 处理场景，该桌面应用架构并非最优选择；项目维护依赖社区驱动，商业级技术支持有限。

#### 学习与落地建议

对于开发者而言，建议首先阅读 `README.md` 了解项目整体设计思路，然后深入 `py_src/` 目录研究核心 OCR 流程的实现。落地部署时可考虑以下方向：将 OCR 模块封装为微服务，提供 API 接口供其他系统调用；针对特定垂直行业（如发票识别、合同提取）开发定制化识别模板；利用其多语言支持能力，为跨国业务提供本地化解决方案。部署环境建议使用 Python 3.8 以上版本，确保 Qt 依赖库正确安装即可实现稳定运行。

---
## 学习要点

- Umi-OCR 是一款开源 OCR 项目，能够从图片和 PDF 中快速提取文字。
- 基于深度学习模型，提供高精度的中英文识别效果。
- 支持本地离线运行，数据无需上传云端，保护隐私安全。
- 提供命令行和 Python API 两种使用方式，便于集成到自动化流程。
- 内置批量处理功能，可高效处理大量文档，提升数字化效率。
- 支持 Windows、Linux、macOS 多平台，部署灵活便捷。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [离线OCR](/tags/%E7%A6%BB%E7%BA%BFocr/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [开源工具](/tags/%E5%BC%80%E6%BA%90%E5%B7%A5%E5%85%B7/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/) / [多语言](/tags/%E5%A4%9A%E8%AF%AD%E8%A8%80/) / [Python](/tags/python/) / [批量处理](/tags/%E6%89%B9%E9%87%8F%E5%A4%84%E7%90%86/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR免费离线开源OCR，支持PDF二维码]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [🚀Mootdx：Python金融数据神器！行情/财报/选股一站式搞定！💰]({{< relref "posts/20260126-github_trending-mootdx-mootdx-7.md" >}})
- [Claude-File-Recovery：恢复 ~/.claude 会话中的文件]({{< relref "posts/20260227-hacker_news-show-hn-claude-file-recovery-recover-files-from-yo-11.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*
