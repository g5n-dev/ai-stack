---
title: LangChain 加持：后端 AI 流式对话的优雅实现
date: 2026-05-13 21:11:45+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- JavaScript
- Docker
categories: []
scenarios:
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7639265898831691817
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:c9d69726466762dcd5dc96a6aee064a72fb1bf796cab527236ac4966e27570b2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 28
captured_at: '2026-07-18T04:21:23.471454Z'
source_capture_sha256: sha256:4cc00cfc49670ea28b826d1f59e89680e39bfd33d86fabb8f34bd553996cb913
source_capture_chars_original: 5999
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_5b308625c0542166d9848fede0e195b01c0537b3ea29e3f90dd527f30d0e0bdb
revision_id: rev_d2048fe1f49f8e4a9a7c96d60e5790ceee5e8737daad99d9eadb9b9b507bb6be
event_id: evt_69d69e9931451034c6b96e72cc3338737bd7b8fd3de706f2cd63a1dbcfc77e97
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-13T13:11:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7639265898831691817](<https://juejin.cn/post/7639265898831691817>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> LangChain 加持：后端 AI 流式对话的优雅实现
> 从 mock 到后端：为什么要把 AI 调用搬到服务端
> 上一篇文章我们聊了通过 mock 文件在 Vite 开发服务器里转发 DeepSeek 请求。但那只是开发阶段的权宜之计。真正上线时，AI 调用必须放在后端，原因很直接：
> API Key 绝不能被带到浏览器
> 。mock 文件跑在 Node.js 里，Key 是安全的；但如果前端直接调 DeepSeek，Key 就暴露在了每个用户的浏览器里
> 前端不应该关心 AI 模型的具体实现
> 。换模型、调参数、加缓存，这些都是后端的事
> 真正的业务逻辑需要在服务端做
> 。比如对话历史存库、内容审核、用量计费
> 所以我们在 NestJS 后端用
> LangChain
> 框架封装了 AI 对话能力。LangChain 在这里扮演的角色是"万能插座"——今天接 DeepSeek，明天换成 OpenAI 或 Claude，业务代码一行不用改。
> 文件结构一览
> backend/posts/src/ai/
> ├── ai.module.ts
> # NestJS 模块注册
> ├── ai.controller.ts
> # 路由 + SSE 响应头 + 格式转换
> ├── ai.service.ts
> # LangChain 调用核心逻辑
> └── dto/
>     └── chat.dto.ts
> # 请求参数校验
> 数据流方向：
> 浏览器 → NestJS Controller → Service → LangChain → DeepSeek
> │
>                                             SSE 流返回
>                                                     │
> 浏览器 ← Controller（边收边写）  ←  Servi…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
