---
title: 节省Token的8种方案
date: 2026-04-15 03:25:27+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7628442107121598479
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:26f8f54e573ab61af7512f1c1343aada762fc97838935b44a57ace02a0496b9a
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 12
captured_at: '2026-07-18T04:19:34.279724Z'
source_capture_sha256: sha256:ae5b73462f75e8aa1776e9424fb5224500c9d86d9c3e69c459d4aa5d76b29910
source_capture_chars_original: 6000
source_publication_excerpt_chars: 730
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_37c3d8ba79b531a3ed571381c61e96b9051e656d00a793e8faefdcf5f77d3687
revision_id: rev_0e2c12e51afa14e014a4d9f2c7803fa156c7e8e5bc2c6a913f27ce2a902a5a04
event_id: evt_4cbd1b2425ca3eebb2bbb64f7950d18af43d362dafd8cbe0fac76faab26fb36d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-14T19:25:27Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7628442107121598479](<https://juejin.cn/post/7628442107121598479>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> 最近有球友问：“三哥，我们团队在做AI客服，对话一长token消耗扛不住。有没有一种方案，既能保留完整上下文记忆，又能省token？”
> 这位朋友的问题，恰恰戳中了当下AI应用开发最头疼的痛点。
> 既要马儿跑得快，又要马儿不吃草。
> 这听起来像是矛盾，但经过这两年的摸索，我发现在某些条件下，确实存在“相对两全”的解法。
> 今天这篇文章就专门跟大家一起聊聊这个话题，希望对你会有所帮助。
> 更多项目实战在Java突击队网：susan.net.cn
> 一、为什么记忆必然消耗token？
> 很多小伙伴可能觉得，大模型就像一个人，你说过的话它应该天然记得住。
> 错！
> 大模型本质上是一个
> 无状态的函数。
> 每次调用都是独立的，它没有任何“记忆细胞”。
> 为了让AI记住之前聊过什么，唯一的办法就是：
> 把历史对话拼接到下一次请求里
> 。
> 这就是所谓的“上下文注入”。
> 看到没？
> 第N次请求携带的历史，是前N-1轮的总和
> 。
> token消耗随着对话轮数线性增长——更准确地说，是O\(n\)级别的增长。
> 但事情没这么简单。
> Transformer模型的核心是
> 自注意力机制
> ，它的计算复杂度是
> O\(n²\)
> 。
> 也就是说，输入长度翻一倍，计算量翻四倍。
> 更可怕的是，当输入过长时，模型会患上“中间迷失症”——位于长文本中间的信息被严重忽略。
> 所以，我们的真实困境是：
> 保留全部历史 → token爆炸 + 注意力稀释 → 又贵又笨
> 丢弃历史 → 信息丢失 → AI变“金鱼脑”
> 有没有一条中间道路？
> 有。
> 下面我会介绍8种方案，从简单到复杂，从廉价到智能，你可以根据自己的场景按需选择。
> 二、方案一：全量记忆
> 简单粗暴，但不推荐。
> 这是最直觉的实现：把所有对话都存下来，每次请求全部带上。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
