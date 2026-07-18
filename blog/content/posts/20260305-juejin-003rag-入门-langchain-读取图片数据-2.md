---
title: 003：RAG 入门-LangChain 读取图片数据
date: 2026-03-05 05:14:19+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613258078369595398
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b7678ccf2b8ce08c6ce9430d6ff56e3ef38dbf25bfe6952a9e2f7c952dd67fb2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:18:36.000259Z'
source_capture_sha256: sha256:7d037008fbdc9626a43e1918b8225cf2171191ed0a841fb90a64fb97247b0f3a
source_capture_chars_original: 5885
source_publication_excerpt_chars: 657
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613258078369595398](<https://juejin.cn/post/7613258078369595398>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> LangChain 读取图片数据
> 本文是
> refine-rag
> 系列教程的第三篇，教你如何使用 LangChain 处理图片和 PPT 等多媒体数据。
> 目录
> 前言
> 环境准备
> 读取图片中的文字（OCR）
> 读取 PPT 文档
> 多模态 RAG 的应用场景
> 常见问题
> 下一步学习
> 前言
> 在前面的文章中，我们学习了如何读取纯文本数据。但在实际应用中，很多重要信息都存储在图片、PPT、扫描件等非文本格式中。比如：
> 产品宣传图中的文字说明
> PPT 演示文稿中的内容
> 扫描的合同和发票
> 截图中的代码和配置
> 这些数据如果不能被 RAG 系统处理，就会造成信息的缺失。本文将介绍如何使用 Unstructured 库来处理这些多媒体数据。
> 环境准备
> 1. 安装依赖包
> # 基础依赖
> pip install langchain langchain-community
> # Unstructured 完整版（包含图片处理）
> pip install
> "unstructured\[all-docs\]"
> # OCR 依赖（用于图片文字识别）
> pip install pdfminer.six
> # 如果需要更好的 OCR 效果，可以安装 Tesseract
> # macOS: brew install tesseract
> # Ubuntu: sudo apt-get install tesseract-ocr
> # Windows: 下载安装包 https://github.com/UB-Mannheim/tesseract/wiki
> 2.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
