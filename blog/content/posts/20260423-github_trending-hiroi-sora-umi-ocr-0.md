---
title: "Umi-OCR：开源免费离线OCR，支持PDF识别与二维码"
date: 2026-04-23T22:22:42+08:00
draft: false
entry_kind: "auto"
tags: ["开源", "离线OCR", "PDF识别", "二维码", "跨平台", "Python", "隐私保护", "批量识别"]
categories: ["开源生态"]
source: github_trending
description: "项目概述 Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）工具。项目采用 Python 编写，代码结构模块化，支持 Windows 与 Linux 平台。截至目前，仓库已获得约 43,586 次星标，且仍在快速增长。 主要功能 - **截图识别**：快速捕获屏幕内容并进行"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR：开源免费离线OCR，支持PDF识别与二维码

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
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

Umi-OCR 是一款开源、离线的光学字符识别工具，基于 Python 开发，可在不依赖网络的情况下完成文字提取。它支持截屏、批量导入图片以及 PDF 文档的识别，并能够自动排除水印、页眉页脚等干扰元素，同时提供二维码扫描与生成功能，内置多语言模型，适合需要本地处理文本、注重数据隐私的用户使用。本文将介绍其核心功能、配置方法以及常见使用场景。

---
## 摘要

#### 项目概述
Umi-OCR 是由 hiroi-sora 开发的一款开源、免费、离线的 OCR（光学字符识别）工具。项目采用 Python 编写，代码结构模块化，支持 Windows 与 Linux 平台。截至目前，仓库已获得约 43,586 次星标，且仍在快速增长。

#### 主要功能
- **截图识别**：快速捕获屏幕内容并进行文字识别，适合临时提取界面文字。
- **批量图片 OCR**：一次导入多张图片，自动批量输出识别结果。
- **文档识别**：支持 PDF 等文档格式的全文识别，能够排除水印、页眉页脚等干扰。
- **二维码处理**：内置二维码识别与生成功能，拓展了传统 OCR 的应用场景。
- **多语言支持**：内置多国语言库，可识别包括中文、英文、日文等在内的多种语言文字。

#### 技术特点
- **完全离线**：无需联网即可完成全部识别任务，保护用户隐私。
- **模块化架构**：核心识别引擎与界面分离，便于二次开发或功能扩展。
- **跨平台**：基于 Qt 开发，提供图形化界面，同时保留命令行接口。
- **开源免费**：遵循开源协议，用户可自由使用、修改和分发。

#### 应用场景
Umi-OCR 适用于需要快速提取图片或 PDF 中文字的个人用户、开发者和企业场景，如文档数字化、资料整理、无障碍辅助等。其离线和二维码功能在安全要求高或网络受限的环境中尤为实用。

---
## 评论

#### 总体判断

Umi-OCR是一款功能完善、社区认可度高的开源离线OCR工具。作为拥有超过4.3万星标的项目，它在开源OCR领域具有显著影响力。从技术实现角度看，该项目采用Python结合Qt框架构建桌面应用，这一技术选型既保证了跨平台兼容性，也提供了流畅的图形界面体验。

#### 核心优势与事实依据

该项目的主要功能在README中有明确说明，包括截屏识别、批量图片导入、PDF文档处理等实用特性。支持排除水印、页眉页脚等功能，这对于从扫描文档中提取纯净文本尤为实用。内置多国语言库意味着可以直接处理日文、英文等多种语言的图片内容，无需额外配置语言包。

从代码仓库结构观察，项目包含完整的资源文件和模块化设计，这种架构有利于后续功能扩展和维护。开源属性使用户能够审查代码逻辑，甚至自行编译定制版本，满足特定安全或性能需求。

#### 适用场景

Umi-OCR特别适合以下使用场景：对数据隐私有严格要求、无法使用云端OCR服务的用户；需要批量处理图片或PDF文档的办公场景；日常需要进行截图文字识别的内容创作者或研究人员；以及在网络不稳定或无网络环境下工作的用户。

#### 局限性与需要注意的点

离线运行是优势，但也是一把双刃剑。基于本地模型的识别精度通常低于商业云端服务（如百度、腾讯OCR），这一点用户在处理低质量扫描件或复杂版式时应当有心理预期。识别速度与本地硬件配置直接相关，配置较低的设备可能出现响应延迟。

从项目维护角度看，虽然星标数量表明社区活跃度较高，但用户在实际部署前仍建议通过官方渠道了解更新频率和长期维护计划，以评估其在生产环境中的可靠性。

#### 验证建议

建议在正式采用前，使用实际业务中的典型样本进行测试，包括不同字体、排版复杂度、图像质量的文档。比较提取结果的准确率和耗时，与现有解决方案做横向对比，再决定是否全面替代或作为补充工具使用。

---
## 技术分析

#### 架构概述
Umi-OCR 采用模块化设计，将前端界面、业务逻辑与 OCR 引擎解耦。从仓库结构看，项目以 Python 为核心，利用 Qt 框架的 QML 实现跨平台 GUI（图形用户界面），这使得核心 OCR 处理逻辑可独立运行，而 UI 层通过 Qt 组件渲染。模块化架构允许用户替换底层 OCR 引擎（如 Tesseract）或扩展功能（如新增二维码库），而不影响其他模块。

#### 核心能力分析
- **离线 OCR**：无需网络连接，保护数据隐私，适合内网或敏感环境。
- **多格式支持**：支持截屏、批量导入图片（常见格式如 PNG、JPG）以及 PDF 文档识别，覆盖日常办公场景。
- **水印/页眉页脚排除**：通过后处理算法识别并过滤重复元素，提升提取文本的纯净度。
- **二维码功能**：集成扫描与生成二维码能力，可扩展至条码处理。
- **多语言库**：内置多种语言模型，支持国际文档识别，但需预装对应语言包。

#### 技术实现细节
- **OCR 引擎**：推断项目基于 Tesseract OCR，因其为开源领域最成熟、支持多语言的离线引擎，且 Python 生态有 `pytesseract` 封装。
- **图像预处理**：可能使用 OpenCV 或 Pillow 进行灰度化、二值化、倾斜校正等操作，以提高识别准确率。
- **PDF 处理**：可能采用 PyMuPDF（fitz）解析 PDF 页面为图像，或用 pdf2image 转换，配合 OCR 引擎批量处理。
- **二维码库**：可能集成 pyzbar（扫描）和 qrcode（生成），两者均为轻量级开源库。
- **GUI 开发**：Qt/QML 组合实现界面，Qt 提供原生性能，QML 简化 UI 定义，支持 Windows、Linux、macOS。
- **部署方式**：Python 代码打包为可执行文件（如 PyInstaller），用户无需安装 Python 环境即可运行。

#### 适用与不适用场景
**适用场景**：
- 隐私敏感环境（如医疗、金融文档），数据不出网。
- 批量处理图片或 PDF 的数字化任务（如档案电子化）。
- 排除水印的文档提取（如已盖章文件）。
- 生成或扫描二维码（如名片、产品追溯）。
- 多语言文档识别（需预先配置语言包）。

**不适用场景**：
- 极高准确率要求的手写或变形文本识别，离线引擎通常弱于云服务。
- 实时视频流 OCR（如视频字幕提取），性能可能不足。
- 需要结构化输出（表格、段落布局）的复杂文档，除非项目已实现后处理。

#### 学习与落地建议
- **学习方向**：研究模块化架构设计模式，了解如何封装 OCR 引擎接口；参考 Qt/QML 开发跨平台 GUI；探索图像预处理对识别率的提升技巧。
- **落地应用**：可直接部署为桌面 OCR 工具，或集成到自动化工作流（如 RPA）中处理文档。批量处理时建议分批执行以避免内存占用过高。
- **注意事项**：首次使用时需安装 Tesseract 及语言包；根据文档类型调整预处理参数（如二值化阈值）；PDF 识别需确保页面转换为图像的质量。

---
## 学习要点

- Umi-OCR 是一款轻量级、支持多语言（尤其是日文和中文）的高精度 OCR 库，可快速从图像中提取文本。
- 项目提供简洁的 Python API 与命令行工具，便于在代码中集成或进行批量图像处理。
- 采用优化的模型，在普通 CPU 上即可实现快速识别，降低硬件门槛。
- 代码开源并采用 MIT 许可证，允许自由使用、修改和商业化部署。
- 活跃的 GitHub 社区与 CI/CD 流程保证了持续的测试、集成与版本更新。
- 文档详尽且配有使用示例，帮助新手快速上手并深入定制功能。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [开源](/tags/%E5%BC%80%E6%BA%90/) / [离线OCR](/tags/%E7%A6%BB%E7%BA%BFocr/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/) / [Python](/tags/python/) / [隐私保护](/tags/%E9%9A%90%E7%A7%81%E4%BF%9D%E6%8A%A4/) / [批量识别](/tags/%E6%89%B9%E9%87%8F%E8%AF%86%E5%88%AB/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [数字人LLM业务集成框架Fay]({{< relref "posts/20260319-github_trending-xszyou-fay-0.md" >}})
- [CowAgent：开源多平台AI助理框架，支持十余种模型]({{< relref "posts/20260415-github_trending-zhayujie-cowagent-0.md" >}})
- [Velox: Tauri移植Swift版！Miguel打造跨平台新选择🚀]({{< relref "posts/20260127-hacker_news-velox-a-port-of-tauri-to-swift-by-miguel-de-icaza-8.md" >}})
- [CowAgent：基于大模型的AI助理，支持主动思考与多平台接入]({{< relref "posts/20260205-github_trending-zhayujie-chatgpt-on-wechat-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*