---
title: BoxAgnts 工具系统（6）——多 Provider 适配与 Agent 查询循环
date: 2026-06-13 08:07:43+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Python
- Rust
- Java
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7650412625085038592
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:117f3bf04bd666c8a702baa124540fb299dad0d8e255be896b382239a34c072f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:21:40.322675Z'
source_capture_sha256: sha256:d657c36b2b0f3af0c7044ed2ea1e809e250f296e3acfeeac0ead59b30584558d
source_capture_chars_original: 5130
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7650412625085038592](<https://juejin.cn/post/7650412625085038592>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> BoxAgnts 的工具系统从底层的 WASM 沙箱到上层的 Tool trait，解决了"工具怎么安全地跑"。但工具最终要被 AI 模型调用——这就涉及两个工程问题：不同 AI 厂商的 API 格式完全不兼容，以及对话流与工具执行的交替编排。这两个问题分别由 Provider 抽象层和 Agent 查询循环解决。
> Provider 抽象：做一个 LLM 厂商不可知论者
> 不同类型的 AI 模型 API 在请求格式、响应格式和错误处理上差异很大。
> 先看请求侧。Anthropic 把角色分为
> user
> 和
> assistant
> ，系统 Prompt 是一个独立的顶层字段
> system
> ；OpenAI 把系统 Prompt 当作一个
> role: "system"
> 的消息；Google Gemini 把
> system\_instruction
> 放在请求体顶层但格式又和 Anthropic 不同。如果让上层的 Agent 循环直接处理这些差异，代码会变成一个巨大的
> match provider\_id \{ ... \}
> 分支。
> BoxAgnts 的解法是引入三层抽象：
> 第一层：ProviderRequest / ProviderResponse 统一数据模型
> // provider\_types.rs
> pub
> struct
> ProviderRequest
> \{
> pub
> messages:
> Vec
> &lt;ApiMessage&gt;,
> pub
> system:
> Option
> &lt;
> String
> &gt;,
> pub
> tools:
> Vec
> &lt;ApiToolDefinition&gt;,
> pub
> max\_tokens:
> u32
> ,
> pub
> temperature:
> Option
> &lt;
> f32
> &gt;,
> \}
> pub
> struct
> ProviderResponse
> \{
> pub
> content:
> Vec
> &lt;ContentBlock&gt;,
> p…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
