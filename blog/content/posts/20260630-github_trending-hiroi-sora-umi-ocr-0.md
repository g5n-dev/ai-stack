---
title: "Umi-OCR开源免费离线OCR支持截图PDF识别"
date: 2026-06-30T18:24:54+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线识别", "开源", "Python", "Qt", "跨平台", "批量图片", "PDF识别"]
categories: ["开发工具", "开源生态"]
source: github_trending
description: "项目概述 Umi‑OCR 是由 hiroi‑sora 开发的开源、免费离线 OCR 软件，基于 Python，主要运行于 Windows 与 Linux，支持多语言文字识别。 核心功能 - 截屏 OCR，快速捕获屏幕文字 - 批量图片导入批量识别 - PDF 文档 OCR，自动排除水印、页眉页脚 - 二维码识别与生成"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源免费离线OCR支持截图PDF识别

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的OCR软件。开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 45,687 (+51 stars today)
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

Umi-OCR 是一款开源、免费的离线 OCR 工具，采用 Python 开发，适合需要在本地处理文字识别的用户。它支持截屏、批量导入图片以及 PDF 文档识别，并能自动排除水印、页眉页脚等干扰元素。该工具内置多国语言库，同时提供二维码扫描与生成功能，无需依赖网络即可完成全部操作。本文将介绍其主要功能特性、使用场景以及安装配置方法。

---
## 摘要

#### 项目概述
Umi‑OCR 是由 hiroi‑sora 开发的开源、免费离线 OCR 软件，基于 Python，主要运行于 Windows 与 Linux，支持多语言文字识别。

#### 核心功能
- 截屏 OCR，快速捕获屏幕文字
- 批量图片导入批量识别
- PDF 文档 OCR，自动排除水印、页眉页脚
- 二维码识别与生成
- 完全离线，无需网络

#### 技术特点
- 模块化架构，代码结构清晰，易于扩展
- 内置多国语言库（简体中文、英文、日文等）
- 使用 Qt（QML）构建跨平台 UI
- 支持自定义工作流和插件扩展

#### 项目数据
- 编程语言：Python
- GitHub 星标：约 45,687（截至 2025‑09‑25）
- 仓库地址：hiroi‑sora/Umi‑OCR

#### 发展现状
项目保持活跃维护，持续更新多语言模型与功能迭代，适合个人和企业用户的离线文字识别需求。

---
## 评论

#### 总体判断

Umi-OCR 是一款功能完整、面向实际工作流的开源离线 OCR 工具，在开源社区拥有超过 45k 星标，表明其获得了相当程度的认可与使用。从技术实现看，它采用 Python 语言，结合 Qt 框架构建图形界面，实现了无需联网即可完成文字识别的核心能力，同时整合了 PDF 解析、二维码处理等辅助功能，形成了相对完整的文档处理闭环。

#### 技术与实用评估

**架构设计**：基于 Python 的 OCR 实现通常依赖 PaddleOCR 或 Tesseract 等开源识别引擎。Umi-OCR 的离线特性意味着所有模型推理在本地完成，这保证了数据隐私性，也使其在网络受限环境中可用。Qt 框架的使用为其提供了跨平台桌面应用的图形交互能力。

**功能完整性**：支持的截屏与批量导入覆盖了常见图片获取方式；PDF 文档识别扩展了应用范围；排除水印、页眉页脚的功能针对扫描文档优化，体现了对实际场景痛点的关注；二维码扫描与生成功能则拓展了工具的可用性边界。

**多语言支持**：内置多国语言库是 OCR 工具的核心竞争力之一，这一特性使其能够处理多语种文档。

#### 适用场景

该工具特别适合以下场景：对数据隐私有要求的文档处理（如企业内部资料、医疗记录）；缺乏稳定网络连接的离线工作环境；需要批量处理图片或 PDF 的重复性 OCR 任务；以及需要从扫描文档中提取结构化文本同时排除版面干扰信息的用户。

#### 局限性

纯离线设计意味着无法利用云端大模型的最新能力，在复杂版式或低质量图像的识别准确率上可能逊于商业云服务。多语言支持的具体范围和识别效果需实际测试验证。Python 实现的性能在处理大规模文档时可能受限。

#### 验证方式

建议通过官方 README 中的示例图片或自有文档样本进行实际测试，重点验证目标语言与版式的识别效果、批量处理性能以及 PDF 解析的准确性。

---
## 技术分析

#### 技术架构分析

基于仓库文件结构推断，该项目采用模块化架构设计，主要由以下核心组件构成：

- **Qt框架**：从仓库中的QML文件和Qt相关资源可以确认，前端界面采用Qt框架实现跨平台桌面应用开发。QML的使用表明界面层与业务逻辑层实现了较好分离。
- **Python核心**：主业务逻辑使用Python实现，便于集成各类OCR引擎和图像处理库。
- **资源模块化**：`UmiOCR-data/`目录采用分离设计，将配置、数据和源码分开管理，提高了可维护性。

#### 核心能力评估

**已知事实：**

- 支持截屏识别和批量图片导入
- PDF文档文本识别
- 内置多国语言识别库
- 二维码扫描与生成功能
- 水印、页眉页脚排除机制

**推断能力：**

- 采用本地OCR引擎实现完全离线运行，数据无需上传云端
- 模块化设计支持功能扩展和自定义配置
- 图形界面提供直观操作，降低使用门槛

#### 技术实现细节

基于仓库文件分析，技术实现包含以下关键层面：

- **OCR引擎集成**：推断采用开源OCR引擎（如PaddleOCR、Tesseract等），具体实现细节需进一步阅读源码确认
- **图像预处理**：批量处理流程中可能包含图像增强、降噪、二值化等预处理步骤
- **多线程设计**：run.py的存在暗示程序采用多线程或异步机制处理批量任务，保证界面响应性
- **跨平台支持**：Qt框架天然支持Windows、Linux、macOS多平台部署

#### 适用场景

- **离线办公环境**：政府、金融、医疗等对数据安全有严格要求的场景
- **批量文档数字化**：需要快速处理大量扫描件、截图的场景
- **个人隐私保护**：不希望图片上传至云端的用户
- **多语言文档处理**：支持跨国业务文档的本地化识别

#### 不适用场景

- **移动端需求**：该项目为桌面应用，无法直接在手机或平板上使用
- **超大规模工业化处理**：45K星标表明社区活跃度高，但相比商业级OCR服务，吞吐量可能受限
- **实时流媒体识别**：静态图片处理为主，非视频流实时OCR
- **复杂排版文档**：高度复杂的多栏排版或艺术字识别效果可能不稳定

#### 学习与落地建议

**学习价值：**

- 研究Qt+QML的现代化桌面应用开发模式
- 理解OCR引擎与业务逻辑的解耦设计
- 借鉴开源项目的多语言国际化实现

**企业落地注意事项：**

- 部署前需进行识别准确率测试，特别是针对实际业务文档类型
- 评估批量处理性能是否满足生产环境需求
- 考虑与企业现有系统的API对接开发成本
- 关注项目维护活跃度和社区支持情况

**二次开发方向：**

- 基于模块化架构扩展特定行业识别模型
- 开发命令行接口用于自动化流水线集成
- 根据企业品牌需求定制UI界面

---
## 学习要点

- Umi-OCR 是 hiroi-sora 开源的轻量级离线 OCR 工具，专注于从图片中快速提取文字。
- 支持多语言（尤其是日语、中文、英文），并针对日文文档做了专门优化。
- 采用纯 Python 实现，无需 GPU，能在 CPU 环境快速运行。
- 提供简洁的 GUI 与命令行接口，支持批量处理图片或 PDF。
- 开源 MIT 许可证，允许自由集成到个人或商业项目。
- 项目活跃度高，已在 GitHub Trending 上获得关注，持续更新改进。
- 设计强调低资源消耗与高识别准确率，适合在资源受限的设备上部署。

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [OCR](/tags/ocr/) / [离线识别](/tags/%E7%A6%BB%E7%BA%BF%E8%AF%86%E5%88%AB/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [Python](/tags/python/) / [Qt](/tags/qt/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/) / [批量图片](/tags/%E6%89%B9%E9%87%8F%E5%9B%BE%E7%89%87/) / [PDF识别](/tags/pdf%E8%AF%86%E5%88%AB/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Umi-OCR开源软件：免费离线OCR，支持PDF截屏批量识别]({{< relref "posts/20260423-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [Umi-OCR免费离线开源OCR，支持PDF二维码]({{< relref "posts/20260424-github_trending-hiroi-sora-umi-ocr-0.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [MatsuriDayo / Nekoray 🔥：翻墙神器！GitHub]({{< relref "posts/20260125-github_trending-matsuridayo-nekoray-1.md" >}})
- [🚀 MatsuriDayo / Nekoray：GitHub趋势第一！超强工具神器✨]({{< relref "posts/20260126-github_trending-matsuridayo-nekoray-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*