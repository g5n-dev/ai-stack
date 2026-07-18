---
title: AI 对话应用之 JS 的流式接口数据处理
date: 2026-03-17 18:33:56+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Java
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7618115042275606543
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:c53f2257ca59c6fb15526fd03e1fada6b3a6ee68536092f027ef0d4c698fb02a
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 21
captured_at: '2026-07-18T04:19:21.234509Z'
source_capture_sha256: sha256:16a5c177394154663b44a9939c86c9bbb31fc89754422f3b55f312040a70cc86
source_capture_chars_original: 4801
source_publication_excerpt_chars: 537
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7618115042275606543](<https://juejin.cn/post/7618115042275606543>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 需求背景
> 市面上的 AI 聊天软件基本上都是不断地向页面渲染出来 AI 思考的内容，传统的 web 网络 request 接口并不适合这种 ai 不断思考，不断输出内容的场景。而这种不断输出内容的应用场景最适合使用流式数据传输这种技术这不仅能够提升用户体验，还能优化数据传输效率，增强系统的可靠性和安全性；通过流式数据传输方案，满足用户对AI对话的多样化需求。
> 技术选型
> 而网页前端 js 当中针对流式数据的接收处理主流有以下几种形式：
> Server-Sent Events \(SSE\)
> WebSocket
> fetch API + stream API
> 虽然有很多种 AI 对话处理的技术选型，但是其实还是取决于后台这次使用 java 的 Spring AI 返回的是 Stream 形式的数据，因此最后的技术选型使用的是
> fetch API + stream API
> 。
> 具体实现与封装
> 原生 fetch api
> 其实使用 XMLRequest 也是能够实现接收 stream 流式数据的接口请求，只需要通过 api 当中的 onprogress 对接口返回的数据进行监听则可以实现；但是已经是现代化的应用了，我们可以使用更加现代化的 fetch api 进行开发处理。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
