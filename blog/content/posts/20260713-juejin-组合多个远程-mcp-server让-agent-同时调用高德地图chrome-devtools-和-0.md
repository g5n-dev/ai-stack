---
title: 组合多个远程 MCP Server：让 Agent 同时调用高德地图、Chrome DevTools 和文件系统
date: 2026-07-13 10:49:59+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- JavaScript
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7661821409981153315
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d34b1d7a309215d7797fe052b572f6d83b831b3d8fef67b3f5f98c1cfa171772
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 56
captured_at: '2026-07-18T04:21:53.764140Z'
source_capture_sha256: sha256:b622f92310874d3246e3d67bbd66281da5e2cd9896734567e15ccede5c5ebe46
source_capture_chars_original: 2949
source_publication_excerpt_chars: 543
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7661821409981153315](<https://juejin.cn/post/7661821409981153315>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 组合多个远程 MCP Server：让 Agent 同时调用高德地图、Chrome DevTools 和文件系统
> 摘要
> ：一个 Agent 如果能同时调用高德地图查位置、用 Chrome DevTools 打开网页、用 FileSystem 写入文件，它就能完成多么复杂的任务？本文用 LangChain 的 MultiServerMCPClient 连接多个 MCP Server——本地、远程 HTTP、stdio 三种方式全涵盖——构建一个能跨进程调用多种工具的 Agent。
> 📑 目录
> MCP 的核心价值：跨进程调用
> 项目目标：两个任务，展示 MCP 的组合威力
> 环境准备与依赖包详解
> MultiServerMCPClient：同时连接多个 Server
> 配置详解：本地、远程 HTTP、stdio 三种方式
> Agent 循环：处理不同类型的 Tool 返回值
> 任务一：搜索酒店 + 浏览器展示图片
> 任务二：搜索酒店 + 路线规划 + 保存文档
> 一点总结
> 互动讨论
> MCP 的核心价值：跨进程调用
> MCP（Model Context Protocol）的本质还是 Tool，但它给 Tool 包了一层进程，可以通过 stdio 或 HTTP 来
> 跨进程访问
> 。
> 这意味着什么？…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
