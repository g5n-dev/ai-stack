---
title: 面试官：你知道 MCP、Skill、Function Call 这三个的区别吗？
date: 2026-02-27 08:07:36+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7611084174967210019
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:85d9d8724ff1a0f962fac345ff9e273d97395bfd39c3e8813747bc67caa931e8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 40
captured_at: '2026-07-18T04:18:22.508475Z'
source_capture_sha256: sha256:aecc84e0babbb7ea639a7a57c40b1a915a9dc0d9f1654f4b6695a803211158a8
source_capture_chars_original: 2199
source_publication_excerpt_chars: 706
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_738e96ebfa8e560a1b624322053607db06535f57b79d581e1c5e77b3e6c4b140
revision_id: rev_63af5eb7446b33b95492c229bddc81febbd46d84de39179063a70c829271218f
event_id: evt_250d3d70f71e150110f01eaffdc1e54c33ab3b5705310f7fcfa92fcf797aa7ce
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T00:07:36Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7611084174967210019](<https://juejin.cn/post/7611084174967210019>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 最近翻后台留言，发现好多朋友都在吐槽：现在后端面试，AI 相关的题目已经成了高频必考点，没提前准备很容易被问懵。
> 所以我后面计划陆续更新 AI 大模型开发相关的面试题系列，帮大家提前攒好干货、做好储备，面试的时候能从容跟面试官对线。
> 那么这次就来学习这一题面试真题！
> 「
> 你知道 MCP、Skill、Function Call 这三个的区别吗？
> 」
> 简要回答
> 这三个概念其实分别处在不同的层次上。
> Function Call是大模型调用外部工具的底层技术实现，让模型能够主动发起函数调用。
> Skill可以理解为对一组相关Function的业务封装，比如"邮件处理技能"里可能包含发送、查询、删除等多个函数。
> 而MCP是Anthropic最近推出的模型上下文协议，它本质上是想建立一套标准化的通信规范，让不同的模型、工具和数据源之间能够更顺畅地互通互联。
> 简单来说，Function Call解决"怎么调"，Skill解决"调什么"，MCP解决"按什么规矩调"。
> 详细回答
> Function Call
> 我先从最底层的
> Function Call
> 说起吧。Function Call其实是OpenAI在GPT-3.5和GPT-4时代引入的核心能力，它让大模型不再只是一个"聊天机器人"，而是可以主动识别用户意图并调用外部工具的智能体。
> 具体来说，当我们在调用API时，会在请求里传入一个functions参数，告诉模型现在有哪些可用的工具以及每个工具需要什么参数。
> 模型理解用户输入后，如果判断需要调用工具，就会返回一个结构化的JSON对象，里面包含函数名和参数值，然后我们的代码再根据这个返回去真正执行那个函数。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
