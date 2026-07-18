---
title: 🚀 Vercel AI SDK 使用指南： 消息元数据 (Message Metadata)
date: 2026-02-16 07:50:12+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- TypeScript
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606354588692217882
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fea6a9d3e310e98ac2d4b3f86b09205a3badbd97ea477958d0aef3f6e1c346d4
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:17:21.349755Z'
source_capture_sha256: sha256:c7f55764cd6315b19119ed8a6e73623a1934a02d3b8a7dc9dec395178163bcf5
source_capture_chars_original: 4165
source_publication_excerpt_chars: 736
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606354588692217882](<https://juejin.cn/post/7606354588692217882>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在构建 AI 聊天应用时，我们经常需要传递一些
> 不属于消息内容本身
> 的额外信息。例如：
> 🕒
> 时间戳
> ：消息生成的时间。
> 🤖
> 模型信息
> ：使用的是 GPT-4 还是 Claude 3.5。
> 💰
> Token 用量
> ：当前对话消耗了多少 Token。
> 🆔
> 用户上下文
> ：Session ID 或用户 ID。
> Vercel AI SDK 提供了
> Message Metadata（消息元数据）
> 功能来解决这个问题。它允许我们在消息级别（Message Level）附加自定义数据，这些数据不会作为 prompt 的一部分发送给大模型，而是专门用于 UI 展示或逻辑处理。
> 本文将带你通过三个步骤，实现一个带有时间戳和 Token 统计功能的聊天应用。
> 1. 定义类型 \(Type Safety\)
> 为了在前后端获得完整的 TypeScript 类型提示，我们首先需要定义元数据的 Schema。这里使用
> zod
> 来定义结构。
> 新建
> app/types.ts
> ：
> TypeScript
> // app/types.ts
> import
> \{
> UIMessage
> \}
> from
> 'ai'
> ;
> import
> \{ z \}
> from
> 'zod'
> ;
> // 1. 定义元数据 Schema
> // 这里我们定义了创建时间、模型名称和 Token 用量
> export
> const
> messageMetadataSchema = z.
> object
> \(\{
> createdAt
> : z.
> number
> \(\).
> optional
> \(\),
> model
> : z.
> string
> \(\).
> optional
> \(\),
> totalTokens
> : z.
> number
> \(\).
> optional
> \(\),
> \}\);
> // 2.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
