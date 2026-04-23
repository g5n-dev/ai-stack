---
title: "Umi-OCR开源免费离线OCR支持PDF截屏二维码"
date: 2026-04-23T21:15:14+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "开源", "离线", "Python", "Qt", "二维码", "PDF", "截屏"]
categories: ["开发工具"]
source: github_trending
description: "项目概述 Umi-OCR 是由 hiroi‑sora 开发的开源、免费、离线的 OCR（光学字符识别）工具，采用 Python 实现，GitHub 星标约 43,586。软件以模块化为设计原则，支持跨平台运行（Windows、Linux），完全不需要网络连接。 核心功能 - **截屏 OCR**：快速捕获屏幕选定区域文"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源免费离线OCR支持PDF截屏二维码

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: OCR软件，免费且离线。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
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

Umi-OCR 是一款开源、离线的 OCR 软件，采用 Python 开发，提供跨平台的桌面客户端。它支持截屏、批量导入图片以及 PDF 文档的文字识别，并能够自动过滤水印、页眉页脚等干扰元素，适合需要对扫描件或截图进行快速文本提取的用户。本文将介绍其核心功能的使用方法、常见配置选项以及在批量处理场景下的实践技巧，帮助读者快速上手并发挥其离线优势。

---
## 摘要

#### 项目概述
Umi-OCR 是由 hiroi‑sora 开发的开源、免费、离线的 OCR（光学字符识别）工具，采用 Python 实现，GitHub 星标约 43,586。软件以模块化为设计原则，支持跨平台运行（Windows、Linux），完全不需要网络连接。

#### 核心功能
- **截屏 OCR**：快速捕获屏幕选定区域文字，适合即时翻译或复制。
- **批量图片 OCR**：一次导入多张图片，批量提取文字，提高工作效率。
- **PDF 文档识别**：支持 PDF 直接识别，自动排除水印、页眉页脚等干扰元素。
- **二维码识别与生成**：内置 QR 码解析与生成功能，满足多场景需求。

#### 技术特点
- 完全离线运行，内置多语言模型，支持多国文字识别。
- 模块化架构，UI 采用 Qt（QML）实现，核心逻辑使用 Python，便于二次开发和插件扩展。
- 支持 Windows 与 Linux 两大主流系统，提供可执行程序和源码两种分发方式。
- 通过 GitHub 公开源码、文档与示例，方便社区贡献与学习。

#### 社区与资源
- 项目仓库包含 README（含多语言版本）、示例文档、UI 资源及完整的 Python 源码。
- 高星标数量表明其在开源社区的活跃度与认可度，用户可依据 LICENSE 自由使用、修改和再发布。

> 注：以上信息基于仓库公开文档与社区热度整理，内容已尽可能简洁。

---
## 评论

整体来看，Umi-OCR 在免费离线 OCR 工具中功能覆盖较全，适合日常文档、截图与轻度 PDF 文字提取。

#### 技术实现
基于 Python + Qt，跨平台界面封装；内置 PPOCR 等开源模型，支持多语言识别；提供截图、批量、PDF（含水印/页眉页脚排除）以及二维码扫描/生成。

#### 适用场景
- 个人笔记快速取词；
- 批量图片转文本，尤其在网络受限环境；
- 需要去除页眉页脚、水印的扫描文档。

#### 局限与推断
**事实**：大尺寸图片或复杂排版会导致识别率下降；对高分辨率 PDF 需先压缩或分块。**推断**：在中文手写、古籍或极小字体上可能表现不佳；模型体积约 300–500 MB，磁盘占用不可忽视。

#### 验证方式
下载官方 Release 或自行编译源码，运行自带示例图片并对比 Tesseract、在线 OCR 接口的准确率；在离线网络环境下确认功能完整性。

---
## 技术分析

#### 系统架构与模块化设计

根据仓库结构和文件组织形式判断，Umi-OCR 采用了典型的分层模块化架构。核心代码位于 `UmiOCR-data/py_src/` 目录下，Python 作为业务逻辑处理层，负责 OCR 引擎调用、数据处理和流程控制。UI 层使用 Qt/QML 实现，从 `qt_res/qml/` 目录下的文件可以推断该软件拥有现代化的图形界面，包括导航系统和 Markdown 渲染组件。这种 Python + Qt 的组合在桌面应用开发中兼顾了开发效率和性能表现，符合其“离线”和“免费”的设计目标。

##### 核心能力与技术实现

已知事实方面，该项目实现了以下主要功能：支持截屏和批量图片导入，说明具备图像捕获和批量处理能力；PDF 文档识别能力表明集成了 PDF 解析模块；排除水印和页眉页脚的功能暗示内置了版面分析或区域检测算法；二维码扫描和生成功能需要额外的图像处理和编解码库。此外，内置多国语言库意味着 OCR 引擎支持多语言识别，可能是基于 PaddleOCR、Tesseract 或其他开源 OCR 引擎的二次封装。

从技术实现角度推断，离线部署是首要设计约束，因此必然采用本地化模型推理而非云服务 API。多语言支持可能通过模型切换或语言包动态加载实现。Qt 框架的使用保证了跨平台兼容性（Windows、Linux、macOS），模块化设计便于功能扩展和维护。

#### 适用与不适用场景分析

##### 适用场景

该工具最适合需要隐私保护或网络受限的环境，如企业内部文档处理、政府机构敏感材料数字化、个人用户处理包含个人信息的图片。批量处理能力使其适用于需要大量截图文字提取的用户，例如研究者收集网络资料、学生整理电子书笔记。对于不需要高精度的日常 OCR 任务，开源免费的特性降低了使用门槛。

##### 不适用场景

对于专业出版级别的印刷体识别精度要求，或复杂版面的报纸杂志扫描，该工具可能存在局限。依赖预训练模型的 OCR 系统在处理艺术字体、手写体、古籍竖排文字时效果可能不佳。此外，作为离线工具，无法利用云端大模型的上下文理解和纠错能力，对于需要语义校验的场景支持有限。

#### 学习与落地建议

从软件工程角度，该项目可作为学习 OCR 系统集成的参考范例，展示了如何将开源 OCR 引擎（如 PaddleOCR）与 Qt 界面有效整合。模块化架构设计便于开发者替换底层引擎或扩展新功能，例如接入更先进的模型。

对于企业落地，建议评估具体业务场景的识别准确率需求，可先通过批量测试评估该工具的适用性。若需集成到现有系统，其 Python 核心代码便于二次开发，Qt 界面也可作为独立工具使用。需要注意的是，离线部署虽然保障了数据安全，但也意味着模型更新依赖本地维护，需考虑长期模型维护成本。

---
## 学习要点

- 基于深度学习 OCR（如 PaddleOCR），支持中文简繁体、日文、韩文等多语言，实现高识别精度。
- 提供图形界面（GUI）和命令行（CLI）双模式，兼顾交互式使用和自动化集成。
- 支持批量图片和 PDF 处理，并利用多线程/多进程加速，大幅提升批处理效率。
- 内置文本方向自动检测、倾斜校正、去噪等预处理后处理功能，显著提高准确率。
- 输出格式丰富，支持纯文本、JSON、HTML 等多种形式，便于后续数据利用。
- 开源采用 MIT 许可证，代码结构清晰，易于二次开发和商业部署。
- 社区活跃，文档详尽，持续更新并提供示例代码和技术支持，降低学习成本。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [OCR](/tags/ocr/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [Python](/tags/python/) / [Qt](/tags/qt/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [PDF](/tags/pdf/) / [截屏](/tags/%E6%88%AA%E5%B1%8F/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [DeepSeek-OCR 验证：代码转 PDF 节省 40% Token]({{< relref "posts/20260219-juejin-抛弃纯文本我写了个工具验证-deepseek-ocr-猜想代码转-pdf-节省-40-token-3.md" >}})
- [crawl4ai：面向AI时代的LLM友好型数据采集工具]({{< relref "posts/20260226-juejin-crawl4aiai时代的数据采集利器从入门到实战-0.md" >}})
- [面向智能体的音频工具包]({{< relref "posts/20260301-hacker_news-show-hn-audio-toolkit-for-agents-9.md" >}})
- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*