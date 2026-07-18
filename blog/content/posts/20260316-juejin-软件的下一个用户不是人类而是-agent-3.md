---
title: 软件的下一个用户不是人类，而是 Agent
date: 2026-03-16 08:20:51+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- Python
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7617459773345071140
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:86687ff6b8fb4c9b47abf531c15827f755d510f526386d86a290ff3c9db5914b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 21
captured_at: '2026-07-18T04:19:19.817922Z'
source_capture_sha256: sha256:d449d0637c27b79745d4345b0b178df5cb61bfd6707999632e5ba6ff26cbcac9
source_capture_chars_original: 6000
source_publication_excerpt_chars: 775
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617459773345071140](<https://juejin.cn/post/7617459773345071140>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> "Today's Software Serves Humans. Tomorrow's Users will be Agents." —— CLI-Anything
> 阅读时长
> : ~10 min |
> 难度
> : 进阶 |
> 前置知识
> : 对 AI Agent（如 Claude Code、Cursor）有基本了解，了解 CLI 的基本概念
> 读完本文你将
> :
> 能够清晰阐述软件界面从 GUI → API → CLI → Agent-Native 的演进逻辑，以及为什么 CLI 是当前 Agent 与软件交互的最佳协议
> 理解 CLI-Anything 项目的 7 阶段流水线如何让 AI Agent 自动将任意 GUI 软件转化为可编程工具
> 获得一个判断框架：面对"让 Agent 操控软件"这个需求，什么时候该用 GUI Agent、什么时候该用 MCP、什么时候该用 CLI
> TL;DR
> : AI Agent 正在成为软件的新用户，但今天 99% 的软件是为人类设计的 GUI 程序。CLI-Anything 提出了一条务实的路径：用 AI Agent 分析软件源码，自动生成生产级 CLI，让 Agent 通过结构化命令操控 GIMP、Blender、LibreOffice 等专业软件——不是模拟点击，不是重新造轮子，而是直接调用真实软件后端。这种"Agent-Native"的思路，可能比 GUI Agent 和 MCP 更接近未来软件生态的实际样貌。
> 为什么聊这个
> 前段时间，我在用 Cursor 做一个数据可视化项目时，想让 Agent 帮我批量处理一些 SVG 图表——调整颜色、导出 PNG、统一尺寸。Cursor 能轻松帮我写代码，但当我说"帮我用 Inkscape 打开这个 SVG 并导出 300dpi 的 PNG"时，它就懵了。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
