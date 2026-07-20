---
title: 从零用 Python 实现最基础的MCP协议
date: 2026-04-29 06:27:23+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7633696737098809385
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:c836793a4ecb6963e65aa3f89ae634b9712f83aa23b56cd6e730e2f953f6e800
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 22
captured_at: '2026-07-18T04:19:44.773238Z'
source_capture_sha256: sha256:90cda5fa7c3df09d297d8971373ab6458512b2a57a1e9ade4fa4c3753e23136c
source_capture_chars_original: 3550
source_publication_excerpt_chars: 793
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e9e6af1245bd77d0d83a56cb64a5bc8ca10050288c9c8ec6cc93fb75df895578
revision_id: rev_bcf3c72e9b2668dd844501d185fee327d1243db93b993679ef0014434e60b331
event_id: evt_dcd80336e6f2c134a5fae7feffa712f54d5b83381158b60aa8fe612543fbd4df
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-28T22:27:23Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7633696737098809385](<https://juejin.cn/post/7633696737098809385>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 模型上下文协议（MCP, Model Context Protocol）是 Anthropic 在2024年提出的一种开放标准协议，用于标准化 AI 模型与外部工具和数据源的集成方式。
> 可以将 MCP 类比为 AI 世界中的 “USB-C 接口”：它为大型语言模型（LLM）连接各种工具和数据源提供了一种统一的方法。
> MCP 使用 JSON-RPC 2.0 作为消息格式，在客户端和服务器之间传递请求和响应。
> 本示例将展示如何使用 Python 实现一个最基础的 MCP 协议，包括 MCP 服务器和 MCP 客户端两部分。
> 我们将支持
> discovery（发现）
> invoke（调用）
> retrieve（获取）
> 等基本操作，并通过一个简单的“计算器”工具（支持加法和乘法）演示协议的工作原理。
> 背景和设计概述
> MCP 协议采用
> 客户端-服务器
> 架构。
> MCP服务器提供一组工具（tools）或资源（resources），MCP客户端可以发现服务器提供的功能并进行调用 。
> 两者之间通过JSON-RPC进行通信，以标准的请求/响应消息交换指令和数据。
> 按照 MCP 规范：
> 发现（Discovery）
> ：客户端能够查询服务器，获取其提供的工具列表、资源列表等。这通常通过调用
> tools/list
> 或
> resources/list
> 等方法实现。
> 调用（Invoke）
> ：客户端可以请求执行服务器上的某个工具功能，例如调用计算器的加法或乘法操作。规范中约定使用
> tools/call
> 方法来调用指定名称的工具，并传递所需参数。
> 获取（Retrieve）
> ：客户端能够检索数据内容，例如获取某个资源的具体内容。规范中提供了如
> resources/read
> 等方法用于检索资源内容。
> 在简单工具调用场景下，调用的结果会直接作为响应返回；但对于长任务或资源内容，常采用单独的检索步骤获取结果。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
