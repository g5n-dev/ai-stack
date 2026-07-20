---
title: 基于 Cloudflare 生态的 AI Agent 实现
date: 2026-03-20 04:08:50+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
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
external_url: https://juejin.cn/post/7618852263628701759
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:56ec704087a8168d1774536744f7d3bc380b914169de2133ab2b33e19d8b4277
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:19:26.279189Z'
source_capture_sha256: sha256:4e8ddb9b7ceaf5744576126c8353e9cb9ba250523aa1dede73edcf65cf26cb5a
source_capture_chars_original: 5999
source_publication_excerpt_chars: 720
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e46860f3b5dbff5c37fe326408b4a17d5389c46e2849da4caf3631e4e01ed289
revision_id: rev_f8067070cd593205aad3474255843e3b2e1e840fc60db427b7483a494ec83926
event_id: evt_0d5cf544efe65aa77fae3824193a2ea4f806ab83016c6c1c446a85ec202be5c0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-19T20:08:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7618852263628701759](<https://juejin.cn/post/7618852263628701759>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 2026 新年的一个夜晚，窗外炮竹烟花争相闪耀，脑海里灵光一闪：我这快十年的老博客能不能也赶一波时髦，实现一个真正「有用」的智能助手？
> 有用
> 的意思是，它不能是一个只会随便聊天的机器人，而是一个
> 真正了解我（博主）、了解博客内容
> 的 AI 分身。它最好能事无巨细地知道我写过哪些文章，了解我的观点、立场和经历，能根据访客的问题去知识库里精准地找到最相关的内容，再结合上下文给出自然又富有意义的回答。
> 它应该是一张鲜活、灵动的个人名片。
> 这并不是一个多么复杂的需求，开源工具和商业基建也已经很成熟了，但真正开始实现之后，还是免不了踩了许多坑，走了很多弯路。而这篇文章，记录的正是 Surmon.me 的 AI Agent 从萌芽到成熟的完整历程。
> 需求梳理拆分
> 在这套博客生态中，我把 AI 的业务能力拆分为两个部分：
> 面向管理员的内容生成服务。
> 主要包含：帮管理员生成文章摘要、生成文章点评、自动回复用户评论。
> 面向前台用户的智能对话服务。
> 用户应该可以通过 Agent 窗口得到网站已经存在的绝大部分信息，不限于文章本身，还应该包含许多静态页面的个人简介、社交动态、社区成就……
> 管理员侧的 AI 能力，本质是
> 工具调用
> 。输入一篇文章，输出摘要或点评，短上下文，明确的输入输出，不需要状态存储，直接通过 API 调用 Cloudflare AI Gateway 来访问 LLM 就可以了，这部分直接集成在 NodePress（博客的后端服务）里是最自然的。
> 而面向前台用户的 AI 对话，是
> 完全不同的业务场景
> ：需要 RAG 知识库、需要持久化对话记录、需要限流、需要管理员可以查看所有人的聊天记录，
> 涉及的基础设施也完全不一样
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
