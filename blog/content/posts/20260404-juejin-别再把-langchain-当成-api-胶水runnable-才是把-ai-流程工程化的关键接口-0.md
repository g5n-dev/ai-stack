---
title: 别再把 LangChain 当成 API 胶水：Runnable 才是把 AI 流程工程化的关键接口
date: 2026-04-04 15:53:08+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7624461069679738889
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:4dce842003033c4f5df48ccf68c2357475e4393982c6f52c1521b7906f71dd71
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 50
captured_at: '2026-07-18T04:19:27.418224Z'
source_capture_sha256: sha256:b7757003c8b5b84559953f1e7c00ebb2c157da40d3f24c22ab782e36616e54fd
source_capture_chars_original: 6000
source_publication_excerpt_chars: 799
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_59e219d84aba44e0f15af2421dad7e9aa18e1e4afad193b661fad18eacd97848
revision_id: rev_c02e768a49d88d1215e11f4c96b3c7c446354126bc5b4843d678199fc8cf76cf
event_id: evt_0b83aae84df43fa540074e5e23080b088c35ac881e4dfa3dc97d8ce6b714bccb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-04T07:53:08Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7624461069679738889](<https://juejin.cn/post/7624461069679738889>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 很多人第一次接触 LangChain，会把它理解成一组“帮你调模型”的工具类：
> PromptTemplate
> 负责拼 prompt，
> ChatOpenAI
> 负责调模型，
> OutputParser
> 负责解析结果。这样理解没错，但只对了一半。
> 真正到了工程里，问题很快就不是“怎么调一次模型”，而是“怎么把一条会持续演化的 AI 流程组织好”。
> 比如一个看起来简单的企业问答助手，往往很快就会长成这样：
> 先清洗用户问题
> 再决定这是闲聊、任务型问题，还是知识问答
> 不同类型走不同 prompt
> 有的分支要结构化输出
> 有的分支要保留上下文
> 有的步骤能并行，有的步骤必须串行
> 这时候如果还沿用最原始的命令式写法，代码通常不会因为“模型调用”而失控，而是会因为“流程编排”而失控。
> 这正是 Runnable 的价值所在。
> 这篇文章的核心结论只有一句：
> Runnable 的真正意义，不是少写几行 LangChain 代码，而是把 AI 应用从一堆分散的调用，提升成一条可组合、可复用、可切换执行模式的数据流。
> 理解了这一点，你才会知道为什么 LCEL 值得学，也才知道什么时候该用
> RunnableSequence
> 、什么时候该分支、什么时候该并行、什么时候该保留原始输入。
> 为什么 AI 应用一复杂，命令式写法就开始失控
> 先看最常见的一类代码：模板格式化一次，模型调用一次，解析一次。
> const
> formattedPrompt =
> await
> prompt.
> format
> \(input\);
> const
> rawResponse =
> await
> model.
> invoke
> \(formattedPrompt\);
> const
> result =
> await
> parser.
> invoke
> \(rawResponse\);
> 这段代码的问题，不在于它不能跑，而在于它只适合“单段流程、单次调用、无分支、无复用”的场景。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
