---
title: 仿淘宝 AI 推荐：用 Next.js 构建入门智能水果推荐 Demo
date: 2026-03-14 15:31:04+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616702701867794458
aliases:
- /posts/20260314-juejin-仿淘宝-ai-推荐用-nextjs-构建入门智能水果推荐-demo-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:dc40326f2ab0e506ae06b0a979107147d72b491f112f77916ca2e6e4fa48a1b6
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:19:14.466881Z'
source_capture_sha256: sha256:d9a4d8ed911072d454650981c4241e606086a2993e4c3aafac61c933db9f1d5a
source_capture_chars_original: 5863
source_publication_excerpt_chars: 621
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f79c8aa771219a52395770963154257981589d56b1152d9f3bfcbb14eedd8bb0
revision_id: rev_a1fc45a707af6bc7b0d087625f17fd84e988fbcc56c33e020e7477a666f781ee
event_id: evt_55febbf41a51e5c69516a919ef1fbca188a19b885e5e69e56531ca61c8d0e60f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-14T07:31:04Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616702701867794458](<https://juejin.cn/post/7616702701867794458>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，我是印刻君。平时逛淘宝的时候，不知道大家有没有体验过平台的 AI 搜索功能。它能结合你的需求，做相对精准的商品推荐。
> 今天我想和大家分享一个
> 入门级别的 Demo
> ，用 Next.js 简单实现类似的推荐助手，内容偏基础。
> 我们最终实现的 Demo 视频如下，它主要就 3 项基础功能：
> 基础的 AI 聊天对话，支持流式消息回复；
> 简易的水果价格查询，支持价格升序、降序查询；
> 对话过程中嵌入商品卡片，引导用户购买。
> 视频链接：
> mp.weixin.qq.com/s/pousaUIg7…
> 一、先搭建基础的聊天机器人
> 在实现推荐功能之前，我们先搭建一个基础的 AI 聊天机器人。本次 Demo 以接入 DeepSeek 大模型为例，整体可以分为 4 个关键步骤：
> 1.1 设计聊天界面
> 一个聊天界面包括两大核心部分，
> \*\*消息展示区：\*\*是用户消息和 AI 消息的列表，常规布局是 AI 消息靠左展示，用户消息靠右展示；
> 下方的输入框
> ：包括文本输入框和发送按钮，一直固定在页面底部。
> UI 布局很常规，我们不详细展开介绍，重点分析一个
> 智能滚动
> 交互——当消息增多时，消息展示区应该会自动滚动到底部，确保用户能第一时间查看到最新的回复。
> 要实现这个效果，我们可以在聊天消息列表的底部放一个元素，借助 useRef 绑定它，并配合 useEffect 监听消息。当消息变化时，通过 scrollIntoView 方法，触发自动滚动。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
