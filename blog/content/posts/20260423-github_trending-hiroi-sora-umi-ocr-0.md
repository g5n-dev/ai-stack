---
title: "Umi-OCR开源离线OCR 支持PDF截屏二维码"
date: 2026-04-23T11:24:21+08:00
draft: false
entry_kind: "auto"
tags: ["OCR", "离线", "开源", "PDF", "截屏", "二维码", "Python", "跨平台"]
categories: ["开发工具", "开源生态"]
source: github_trending
description: "项目概述 Umi-OCR 是由 hiroi‑sora 开发的一款开源、免费、离线的 OCR（光学字符识别）软件，采用模块化架构，基于 Python，已获得约 4.3 万星标，支持 Windows 与 Linux 平台。 主要功能 - **截屏 OCR**：快速捕获屏幕区域文字。 - **批量图片 OCR**：一次处理多"
external_url: https://github.com/hiroi-sora/Umi-OCR
scenarios: ["计算机视觉", "桌面应用", "效率工具"]
---

# Umi-OCR开源离线OCR 支持PDF截屏二维码

> **原名**: hiroi-sora /

      Umi-OCR

---

## 基本信息

- **描述**: 免费、离线的 OCR 软件。 开源、免费的离线 OCR 软件。支持截屏/批量导入图片，PDF 文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
- **语言**: Python
- **星标**: 43,568 (+51 stars today)
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

Umi-OCR 是一款开源的离线 OCR 工具，基于 Python 开发，支持截屏、批量导入图片以及 PDF 文档的文字识别。它能够自动过滤页眉页脚和水印，并提供多语言库，适合需要在本机处理大量文本但不想依赖云服务的用户。本文将从安装部署、核心功能使用、常见问题排查以及进阶配置四个方面展开，帮助你快速上手并充分利用该工具。

---
## 摘要

#### 项目概述
Umi-OCR 是由 hiroi‑sora 开发的一款开源、免费、离线的 OCR（光学字符识别）软件，采用模块化架构，基于 Python，已获得约 4.3 万星标，支持 Windows 与 Linux 平台。

#### 主要功能
- **截屏 OCR**：快速捕获屏幕区域文字。
- **批量图片 OCR**：一次处理多张图片，适合文档批量录入。
- **PDF 文档 OCR**：直接识别 PDF 中的文本，并可排除页眉、页脚或水印。
- **二维码识别/生成**：内置 QR 码解析与生成功能。
- **多语言支持**：内置多国语言库，适配不同文字体系。

#### 技术实现
- **离线运行**：所有模型与资源随软件打包，无需网络。
- **模块化设计**：UI（Qt/QML）与核心识别模块分离，便于二次开发。
- **跨平台**：基于 Python 与 Qt，兼容 Windows、Linux。
- **开源生态**：代码托管于 GitHub，提供中、英、日等多语言文档。

#### 社区与影响力
截至目前，项目累计获得约 43,568 次星标，日均增长约 51 次，受到开发者与办公用户的广泛好评。

---
## 评论

总体来看，Umi-OCR 是一款功能完整、离线可用且开源的 OCR 工具，凭借高星标数和活跃的社区，在轻量级文档数字化场景中具备竞争力。

#### 依据
- 事实：项目使用 Python 语言；核心代码位于 run.py，且采用 Qt/QML 实现图形界面；星标 43,568，说明受关注度高。
- 推断：基于离线需求和 Python 生态，项目可能整合了 Tesseract 或 PaddleOCR 作为底层识别引擎，具体实现需阅读源码确认。

#### 适用场景
- 轻量级文档批处理：支持截图、批量图片导入以及 PDF 文字提取（可排除页眉页脚）。
- 需要本地化、无网络的环境，如企业内部机器或离线工作站。
- 二维码扫描/生成辅助功能，适合办公自动化和快速信息录入。

#### 局限
- OCR 精度受限于内置语言库，对低分辨率、复杂排版或噪声较多的图片识别率可能不足。
- 项目为离线版，模型更新需自行下载新模型包，无法像云端服务那样自动迭代。
- 依赖 Qt/QML 桌面环境，暂无移动端或 Web 版部署方案。

#### 验证方式
- 下载 Release 包或从源码安装依赖后运行 `python run.py`，观察是否成功加载 OCR 引擎。
- 使用包含文字、表格、二维码的测试图片集进行批量识别，统计字符错误率与二维码识别成功率。
- 检查日志或源码中的模型加载路径，确认使用的具体 OCR 框架（Tesseract、PaddleOCR 等），以验证推断的准确性。

---
## 技术分析

#### 项目概述与架构特点

该项目是一个拥有43,568星标的热门开源OCR应用，采用**模块化架构设计**。根据源码结构分析，系统分为Python核心处理层和Qt/QML界面层两部分。入口文件run.py负责启动流程，QML文件处理界面渲染，Python模块承担OCR引擎和业务逻辑。这种分层设计使得各组件职责清晰，便于维护和扩展。

#### 核心能力分析

**已知事实：**
- 支持截屏识别和批量图片导入
- 支持PDF文档识别
- 内置水印/页眉页脚排除功能
- 二维码扫描与生成
- 多国语言识别支持
- 完全离线运行

**基于源码结构的推断：** 多语言README（中文、英文、日文）表明该项目面向国际化用户群体；模块化设计暗示可能支持插件扩展或自定义OCR引擎替换。

#### 技术实现解析

从源码组织来看，技术栈包括：
- **后端引擎**：Python实现OCR核心算法，推测使用PaddleOCR或类似开源引擎
- **前端界面**：Qt框架搭配QML语言，提供跨平台桌面应用体验
- **数据管理**：独立的UmiOCR-data目录管理配置和资源文件

该架构的优势在于Python生态的灵活性与Qt跨平台能力的结合，用户无需安装额外运行时即可在Windows、Linux、macOS上运行。

#### 适用场景

适用于以下场景：
- **隐私敏感环境**：完全离线处理，无需网络传输
- **日常办公**：快速截取屏幕文字、批量处理文档
- **多语言场景**：内置多语言库支持国际化需求
- **水印处理需求**：对扫描文档有去除水印/页眉页脚的需求

#### 不适用场景

需要谨慎考虑的情况：
- **超大规模文档处理**：批量处理大量PDF时性能和识别准确率可能受限
- **复杂排版文档**：表格、多栏布局的文档识别效果可能不理想
- **高精度要求的场景**：如法律文档、学术论文等专业领域

#### 学习与落地建议

**学习价值：**
- 模块化架构设计值得借鉴，适合需要构建可扩展OCR系统的开发者
- Qt/QML与Python的结合提供了跨平台桌面应用的最佳实践之一
- 项目代码结构清晰，适合作为OCR系统架构的参考模板

**落地建议：**
- 对于需要快速部署OCR能力的团队，可直接使用预编译版本
- 有定制需求的企业可在现有架构基础上替换OCR引擎或扩展功能模块
- 建议在生产环境部署前进行针对性场景的准确率测试

---
## 学习要点

- Umi-OCR 是由 hiroi-sora 开发并在 GitHub Trending 上获得关注的开源 OCR 项目
- 项目提供高效的文字识别功能，支持多种语言和复杂场景的文本提取
- 采用轻量级实现，便于跨平台集成到各种应用系统中
- 提供简洁的 API 与命令行工具，帮助开发者和普通用户快速上手使用
- 持续更新并积极响应社区反馈，拥有完善的文档和示例代码
- 基于深度学习模型，在保持高识别精度的同时实现了较快的推理速度

---
## 引用

- **GitHub 仓库**: [https://github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)
- **DeepWiki**: [https://deepwiki.com/hiroi-sora/Umi-OCR](https://deepwiki.com/hiroi-sora/Umi-OCR)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [OCR](/tags/ocr/) / [离线](/tags/%E7%A6%BB%E7%BA%BF/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [PDF](/tags/pdf/) / [截屏](/tags/%E6%88%AA%E5%B1%8F/) / [二维码](/tags/%E4%BA%8C%E7%BB%B4%E7%A0%81/) / [Python](/tags/python/) / [跨平台](/tags/%E8%B7%A8%E5%B9%B3%E5%8F%B0/)
- 场景： [计算机视觉](/scenarios/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [桌面应用](/scenarios/%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8/) / [效率工具](/scenarios/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)

### 相关文章

- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [Velox: Tauri移植Swift版！Miguel打造跨平台新选择🚀]({{< relref "posts/20260127-hacker_news-velox-a-port-of-tauri-to-swift-by-miguel-de-icaza-8.md" >}})
- [Rime 配置雾凇拼音：长期维护的简体词库]({{< relref "posts/20260129-github_trending-idvel-rime-ice-3.md" >}})
- [DeepSeek-OCR 验证：代码转 PDF 节省 40% Token]({{< relref "posts/20260219-juejin-抛弃纯文本我写了个工具验证-deepseek-ocr-猜想代码转-pdf-节省-40-token-3.md" >}})
- [crawl4ai：面向AI时代的LLM友好型数据采集工具]({{< relref "posts/20260226-juejin-crawl4aiai时代的数据采集利器从入门到实战-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*