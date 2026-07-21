---
title: Skills 是什么？如何用于 Agent 开发？
date: 2026-03-09 01:01:37+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- RAG
- AI Agent
- 大语言模型
- Python
- 命令行工具
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7614331029458026531
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:eb20176b3e81b30a0c0433b76ae3d49ea4aad0472f4d28e55e99b8c2bc971f41
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 25
captured_at: '2026-07-18T04:18:44.764571Z'
source_capture_sha256: sha256:01fbe8361d2130be613d0a4287ef35f4e72dad826bc1cef01726e19478aa60c0
source_capture_chars_original: 5687
source_publication_excerpt_chars: 728
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_5ca5a0847c044dbd600cd942190b11fb060a668eea96ac1b58821f89245802b0
revision_id: rev_bb4722e0f91b9307bc018cc9af17b716dc80e0a6a83946adb8d7c4a0f4f5829d
event_id: evt_b71e463621390afbd7b4945c139ef11c868ec6cb9ee66f17a108879bf2355c38
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-08T17:01:37Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614331029458026531](<https://juejin.cn/post/7614331029458026531>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，我是双越。
> wangEditor
> 作者，前百度 滴滴 资深前端工程师，慕课网金牌讲师，PMP，
> 前端面试派
> 作者。
> 我正致力于两个项目的开发和升级，感兴趣的可以私信我，加入项目小组。
> 划水AI
> Node 全栈 AIGC 知识库，包括 AI 写作、多人协同编辑。复杂业务，真实上线。
> 智语
> AI Agent 智能体项目。一个智能面试官，可以优化简历、模拟面试、解答题目等。
> 本文总结了我最近调研和学习 SKILLS 的一些记录，帮助大家对 SKILLS 全面的学习和理解。
> SKILLS 是什么
> SKILLS 本质上就是组织 prompt 提示词。
> 不仅 SKILLS，很多包装得很复杂的 Agent 框架，剥开来看确实都在做"往 Prompt 里塞什么、怎么塞"这件事。
> SKILLS 比传统 prompt 多了一个：按需注入。这样就能极大减少 token 使用量，关键是
> 能省钱
> 。
> 基于什么发展而来？
> Skills 的概念来源于以下几个演进脉络：
> 1. Prompt Engineering 的沉淀
> 早期开发者发现，同样的任务，提示词写法不同，结果差异巨大。经过大量试错后，好的提示策略需要被
> 复用和共享
> ，Skills 就是这种沉淀的容器。
> 2. RAG（检索增强生成）的思路迁移
> RAG 是在运行时动态注入外部知识，Skills 借鉴了这个思路——在任务执行前动态注入
> 过程性知识
> （How-to），而不仅仅是事实性知识。
> 3. Tool Use / Function Calling 的延伸
> LLM 有了调用工具的能力后，下一步自然是让 Agent 知道\*\*"什么场景用什么工具、怎么用得好"\*\*，这正是 Skill 要解决的事。
> 4.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
