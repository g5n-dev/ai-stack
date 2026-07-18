---
title: Spring AI 实战：用 JdbcChatMemory + MySQL 给 AI 接上「长期记忆」
date: 2026-05-17 09:17:44+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Java
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7640275639350951936
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:ee1654d29a8ea1bb56a836146e56b631ebc69d7c818e7e2facab86e68f27be42
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 51
captured_at: '2026-07-18T04:21:25.184007Z'
source_capture_sha256: sha256:d4d12cf036b086eca865c57a86eb8470f6b6173a8232fec607d805bc266f99ea
source_capture_chars_original: 4218
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7640275639350951936](<https://juejin.cn/post/7640275639350951936>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Spring AI 实战：用 JdbcChatMemory + MySQL 给 AI 接上「长期记忆」
> 环境：Spring Boot 3.4.5 · Spring AI 1.1.6 · MySQL 8.x · Java 17
> 一、为什么需要对话记忆？
> 默认情况下，
> ChatClient
> 每次调用都是
> 无状态
> 的。你问 AI「我叫什么名字？」，它永远回答「我不知道」——因为上一句「我叫张三」已经消失了。
> 要实现真正的多轮对话，就需要把历史消息随每次请求一起发送给模型。Spring AI 提供了
> ChatMemory
> 体系来解决这个问题，而
> JdbcChatMemory
> 则把记忆持久化到关系型数据库，让服务重启后历史不丢失。
> 二、核心概念
> 在动手之前，先理清三个核心类的职责：
> ┌─────────────────────────────────────────────────────────┐
> │                       ChatClient                        │
> │                                                         │
> │
> prompt
> \(\)
> .user
> \("..."\)
> .advisors
> \(...\)
> .call
> \(\)
> .content
> \(\)    │
> └──────────────────────┬──────────────────────────────────┘
>                        │ 挂载
>                        ▼
> ┌─────────────────────────────────────────────────────────┐
> │              MessageChatMemoryAdvis…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
