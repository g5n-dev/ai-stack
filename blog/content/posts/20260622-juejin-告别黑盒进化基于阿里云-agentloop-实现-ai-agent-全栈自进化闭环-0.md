---
title: 告别“黑盒进化”：基于阿里云 AgentLoop 实现 AI Agent 全栈自进化闭环
date: 2026-06-22 04:39:42+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7653777184240468022
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:4b258169280daafeaf44da34f3ac4de05502e45fda76b5d6cc24d78514d0659c
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:21:44.631614Z'
source_capture_sha256: sha256:b8b6d6cc292407f5132a055e7f64aca40f97136b6862ab613fcd72cc2589b17c
source_capture_chars_original: 5647
source_publication_excerpt_chars: 752
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_87d74a8742569e02725970de3704d1adbfb42a17a2f3fb554f9b8dbccd3eede6
revision_id: rev_90d88bdc73b2442836f8f72b4502c7543bbc7b3d07210cc8f38cb8c8acff190d
event_id: evt_eb298b00900eb87a148ec67e8528a2dc1378db6578061bb1a2ae475ab93ca12a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-21T20:39:42Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7653777184240468022](<https://juejin.cn/post/7653777184240468022>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 作者：望宸、涯海
> 当我们谈 Agent 进化的时候，通常涵盖两类场景。一种是
> 员工办公场景
> ，通过 Coding Agent 或通用 Agent 的记忆、协作风格、用户画像等能力，让 Agent 越用越聪明、越用越懂用户。另一种是
> 企业的业务场景
> ，比如企业对外提供的客服 Agent，对内提供智能分析的 Data Agent。关于前者，Anthropic 发布的 Economic Index 给过一个有意思的对照，使用 Claude 6 个月以上的老用户，对话成功率比新用户高 3–5 个百分点。可见，Coding Agent、通用 Agent 已经在加速进化，用户越用越喜欢。而后者，仍处于各个企业手搓观测、评估、优化，各自积累业务实践经验的阶段。
> 本文要聊的是后者。
> 企业手搓 Agent 进化飞轮的现状
> 进化飞轮通常分为数据采集、数据集构建、效果评估、进化资产沉淀 4 个步骤。虽然模型和 Agent 进化飞轮的流水线类似，但影响 Agent 行为的因素更多。
> 模型任务，是指一次模型的调用，包括对模型的输入和模型的输出。Agent 任务，则是一条带拓扑结构的线，甚至是一张网络图，因为除了模型调用，还有检索、规划、工具调用、浏览器访问、中间状态、反思和决策、回退，甚至还有多个并行子任务等。
> 由于影响 Agent 行为的因素更多，导致进化飞轮带来的新工程难点，是以往的 LLM-as-Judge 的范式所难以应对的。
> 数据采集难：单点变拓扑，schema 不再稳定
> LLM-as-Judge 的范式采集的是 \(prompt, completion\) 二元组，schema 干净，存日志就够。Agent 行为评估要采集的是一条 trajectory（执行轨迹）：每一步的输入输出形状都不一样。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
