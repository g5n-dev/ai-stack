---
title: MCP 工具集成：外部工具变 Eino Tool
date: 2026-07-01 04:20:27+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7657147946866786313
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:630b2ae2ed882801ce20f3c52056fd317201ff08343ee2b105162f92e00645d0
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 24
captured_at: '2026-07-18T04:21:48.980794Z'
source_capture_sha256: sha256:b7c321520d9f9968c17c15dd250f2caf2d481e2e993dfa3673313a4b4176933b
source_capture_chars_original: 1767
source_publication_excerpt_chars: 497
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7657147946866786313](<https://juejin.cn/post/7657147946866786313>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 系列「企业级 AI Agent 实现拆解」E25 篇。上一篇讲了
> 中间件系统：在 Agent 执行流中插入自定义逻辑
> 。这篇讲
> MCP 工具集成
> ——把遵守 MCP 协议的任意外部工具，直接变成 Eino Agent 能用的 Tool，以及 DeepFlux 在此基础上额外做了什么。
> 读完这篇你会知道
> MCP 是什么：JSON-RPC 2.0 打底，三种传输方式
> Eino 的 Tool 接口体系：
> BaseTool
> /
> InvokableTool
> 两层
> GetTools\(\)
> 的核心逻辑：30 行代码里发生了什么
> Schema 转换：MCP 的
> InputSchema
> 怎么变成 Eino 的
> \*jsonschema.Schema
> 两套 MCP SDK 适配的区别：mark3labs vs 官方 SDK
> ToolCallResultHandler
> ：工具返回后的拦截钩子
> DeepFlux 双向桥接：出方向把 KB/Memory 暴露给外部 MCP 客户端
> 一、MCP 协议是什么
> MCP 全称 Model Context Protocol，规定了 AI 模型和外部工具之间的通信格式。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
