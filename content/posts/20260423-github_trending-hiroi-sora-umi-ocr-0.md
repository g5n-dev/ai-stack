---
title: "Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别"
date: 2026-04-23T23:27:59+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "开源", "离线", "PDF识别", "截屏OCR", "二维码", "Python", "Qt"]
categories: ["开源生态", "开发工具"]
source: github_trending
description: "项目简介 Umi‑OCR 是由 **hiroi‑sora** 开发的一款开源、免费、离线的 OCR（光学字符识别）工具。项目使用 Python 编写，仓库星标数已超过 4.3 万，属于热门的开源项目。 主要功能 - **截屏 OCR**：快速捕获屏幕内容并识别文字。 - **批量图片 OCR**：一次性导入多张图片，批"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的开源OCR软件。支持截屏/批量导入图片、PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 43,588 (+48 stars today)
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

Umi-OCR 是一款基于 Python 的免费、离线开源 OCR 工具，支持截屏、批量图片和 PDF 文档的文字识别，并可自动排除水印、页眉页脚以及扫描/生成二维码。该项目内置多语言库，适合需要在无网络环境或对数据安全有要求的情况下快速提取文本的用户。本文将介绍其核心功能、部署方式、常用操作技巧以及在实际场景中的表现评估。

---
## 摘要

#### 项目简介
Umi‑OCR 是由 **hiroi‑sora** 开发的一款开源、免费、离线的 OCR（光学字符识别）工具。项目使用 Python 编写，仓库星标数已超过 4.3 万，属于热门的开源项目。

#### 主要功能
- **截屏 OCR**：快速捕获屏幕内容并识别文字。
- **批量图片 OCR**：一次性导入多张图片，批量输出识别结果。
- **文档 OCR**：支持 PDF 等文档格式的文字提取。
- **二维码识别与生成**：内置 QR 码解析与生成功能。
- **多语言支持**：内置多国语言库，能够处理多语种文本。

#### 技术特点
- **完全离线**：所有模型与处理均在本地完成，无需网络连接。
- **跨平台**：支持 Windows 与 Linux 系统。
- **模块化架构**：各功能以独立模块实现，便于扩展和维护。
- **界面友好**：基于 Qt 的图形界面，提供直观的使用体验。
- **自定义配置**：可排除水印、页眉页脚等干扰元素，提升识别准确率。

#### 项目状态
代码托管于 GitHub，拥有活跃的社区与持续的更新。用户可根据需求直接下载可执行文件或自行编译。

---
## 评论

#### 总体判断
Umi-OCR 是一款面向普通用户的免费离线 OCR 工具，界面简洁、功能完整，能够满足日常截屏、批量图片和 PDF 的文字提取需求，整体评价为“实用、易上手”。

#### 依据与功能
- 事实：项目使用 Python + Qt 开发，支持截屏、批量导入、PDF 解析、二维码识别及多语言库；仓库星标 43k，说明社区认可度高。
- 推断：基于源码目录结构，文字识别大概率基于本地轻量模型（如 Tesseract）或自行封装的推理框架，实现离线运行。

#### 适用场景
1. 需要在无网络环境下快速提取截图或扫描件的文字；
2. 对隐私要求高、不能上传图片到云端的内部文档处理；
3. 批量处理少量（几十张）图片或 PDF 的日常办公场景；
4. 同时需要读取二维码/条形码信息的轻量需求。

#### 局限与风险
- 对极端倾斜、低分辨率或严重噪声的图片识别率会下降；
- 多语言支持受限于预置模型库，非主流语言可能出现漏识别或错字；
- 大批量（上百张）处理时，速度受 CPU 单核限制，可能出现卡顿；
- 由于是开源项目，更新维护依赖社区，长时间不更新可能导致兼容性问题。

#### 验证方式
- 使用公开的 OCR 标准数据集（如 COCO‑Text）对比识别率；
- 在同一硬件环境下与在线 OCR（如百度、腾讯）进行速度与准确率对比；
- 测试 PDF 与二维码的实际提取效果，评估水印/页眉过滤是否有效。

---
## 技术分析

#### 架构设计

##### 模块化架构

根据仓库信息，Umi-OCR采用模块化架构设计，这是其核心设计理念。系统将OCR识别、图像预处理、输出处理等环节解耦为独立模块，便于功能扩展和维护。从目录结构来看，主要代码位于UmiOCR-data/py_src目录下，run.py作为入口文件协调各模块运行。

##### 技术栈

该项目的技术选型为Python+Qt/QML。Python作为主开发语言，负责核心OCR逻辑；Qt/QML用于构建图形界面，提供现代化的人机交互体验。这种组合既能利用Python丰富的机器学习生态，又保证桌面应用的专业用户体验。

#### 核心能力与技术实现

##### OCR识别能力

Umi-OCR的核心能力是离线文字识别。根据描述，它支持多国语言识别，这意味着内置了相应的语言模型。离线特性表明其使用了本地部署的OCR模型，而非调用云服务API。具体模型选择（如PaddleOCR、EasyOCR等）需要进一步查看源码确认。

##### 多功能性集成

项目不仅提供基础OCR功能，还集成了以下能力：截屏识别（实时捕获屏幕区域）、批量图片导入处理、PDF文档解析、二维码扫描与生成、水印/页眉页脚排除。这些功能的实现应该是通过Qt的图像处理模块结合专用算法库完成。

##### 离线运行机制

离线运行意味着所有模型和数据都打包在软件包内，无需网络连接。这对于隐私敏感场景（如处理内部文档、商业机密）具有重要价值。

#### 适用与不适用场景

##### 适用场景

该工具非常适合以下情况：个人或小型团队日常文档电子化、隐私要求严格的机构处理敏感材料、缺乏稳定网络环境的工作站、需要对大量截图进行文字提取的工作流程。特别是其批量处理能力和水印排除功能，对于资料整理和知识管理很有帮助。

##### 不适用场景

存在以下限制：不建议用于对识别精度要求极高的专业出版领域（相比商业OCR解决方案可能存在差距）；不支持在线API调用的云端协作场景；超大规模文档处理（百万页级别）可能面临性能瓶颈；复杂版面的学术论文或杂志排版可能需要人工校对。

#### 学习与落地建议

##### 代码学习建议

对于希望学习该项目的技术开发者，建议重点关注：模块间的接口设计如何实现解耦、Qt/QML界面与Python业务逻辑的交互模式、OCR模型本地化部署的工程实践。可以从run.py入手，理解整体流程后再深入各子模块。

##### 实际应用建议

落地部署时需要考虑：Windows/Linux/Mac不同平台的打包分发策略、OCR模型的持续更新机制、与现有工作流的集成方式（如文件监控、快捷键触发）。对于企业用户，建议评估长期维护成本和版本兼容性。由于是开源项目，可根据具体需求进行二次开发，但需遵守相应的开源协议。

---
## 学习要点

- Umi-OCR 是由 hiroi‑sora 开发的高性能开源 OCR 项目，专注于中文文本识别。
- 该项目在 GitHub Trending 上获得关注，说明它在开发者社区的流行度和活跃度不断提升。
- 提供简洁的 API 接口，便于在 Python 项目中快速集成和使用。
- 支持多种图片格式和批量处理，显著提升大规模文档数字化的效率。
- 通过模型与算法的优化，实现了较高的识别准确率和较快的处理速度。
- 采用开源许可证，鼓励社区贡献和二次开发，提升了项目的可持续性。
- 具备可配置的后处理选项，能够根据不同场景需求进行灵活调整。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [OCR](/tags/ocr/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/) / [截屏OCR](/tags/%E6%88%AA%E5%B1%8Focr/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [Python](/tags/python/) / [Qt](/tags/qt/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [crawl4ai：面向AI时代的LLM友好型数据采集工具]({{< relref "posts/20260226-juejin-crawl4aiai时代的数据采集利器从入门到实战-0.md" >}})
- [面向智能体的音频工具包]({{< relref "posts/20260301-hacker_news-show-hn-audio-toolkit-for-agents-9.md" >}})
- [数字人LLM业务集成框架Fay]({{< relref "posts/20260319-github_trending-xszyou-fay-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*