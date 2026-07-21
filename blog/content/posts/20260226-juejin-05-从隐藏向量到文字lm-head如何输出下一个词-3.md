---
title: 05-从隐藏向量到文字：LM Head如何输出"下一个词"？
date: 2026-02-26 05:26:26+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7610629556069417023
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:707e5c46bb0533d0eb3272db3e443e170461dbc48ed0342a29742e9857557924
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:18:19.486668Z'
source_capture_sha256: sha256:c13963b7e52d7f61edea17bc41ea9d63312cf61a3efcef7cd8bd008b4f9341b8
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_8eb542cb43fb1e997ca5e8a285952333f988595fe86aa73862f06140c62dd9e3
revision_id: rev_ea572882e2ca2c9f434a1f0f5183fce4537aacaab455e6038b09dc98c48ce7f9
event_id: evt_d3e888dded4891ae3766afbac479db4aa153d74c47a1597f32678295bb73dd05
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T21:26:26Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7610629556069417023](<https://juejin.cn/post/7610629556069417023>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 回顾：大模型的完整流程
> 在前面的章节中，我们学习了Transformer的各个组件。现在让我们回顾一下完整流程：
> 输入：
> "今天天气"
> ↓
> （Tokenization + Embedding）
> Token表示：
> X
> ∈
> R
> n
> ×
> d
> model
> ↓
> （位置编码）
> 加入位置：
> X
> +
> PE
> ↓
> （多层Transformer）
> Layer 1：
> Attention + MLP + Residual + LN
> Layer 2：
> Attention + MLP + Residual + LN
> ⋮
> Layer N：
> Attention + MLP + Residual + LN
> ↓
> 最终隐藏状态：
> H
> ∈
> R
> n
> ×
> d
> model
> \\begin\{aligned\}
> &amp;\\text\{输入：\} \\quad \\text\{"今天天气"\} \\\\
> &amp;\\quad \\downarrow \\text\{（Tokenization + Embedding）\} \\\\
> &amp;\\text\{Token表示：\} \\quad X \\in \\mathbb\{R\}^\{n \\times d\_\{\\text\{model&#125;&#125;\} \\\\
> &amp;\\quad \\downarrow \\text\{（位置编码）\} \\\\
> &amp;\\text\{加入位置：\} \\quad X + \\text\{PE\} \\\\
> &amp;\\quad \\downarrow \\text\{（多层Transformer）\} \\\\
> &amp;\\text\{Layer 1：\} \\quad \\text\{Attention + MLP + Residual + LN\} \\\\
> &amp;\\text\{Layer 2：\} \\quad \\text\{Attention + MLP + Residual + LN\} \\\\
> &amp;\\quad \\vdots \\\\
> &amp;\\text\{Layer N：\} \\quad \\text\{Attention + M…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
