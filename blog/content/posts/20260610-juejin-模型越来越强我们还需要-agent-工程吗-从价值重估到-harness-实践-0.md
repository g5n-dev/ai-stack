---
title: 模型越来越强，我们还需要 Agent 工程吗？—— 从价值重估到 Harness 实践
date: 2026-06-10 22:19:44+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 命令行工具
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7649642814956568628
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:0b3d958a0df643442fa4d7ce6efeb0694aeacb6847850064f617a3c55bafce71
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:21:38.932073Z'
source_capture_sha256: sha256:482de06da3ea9f096c1be9d8c5e151c520856404c9f83205c0f5b3effebf439e
source_capture_chars_original: 3209
source_publication_excerpt_chars: 792
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_1ae0052493c14d84a87ee07986ffede55cb81070568cda68c507be5ca66d8b81
revision_id: rev_6f1736b488263b6bbe0fad0b10f10e0f3d911d3f463930b99ab2fcc54cece968
event_id: evt_94806073cfd21b6104beb04255b24a4d1c54b5ceb5d3fb6194a239712ab386c6
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-10T14:19:44Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7649642814956568628](<https://juejin.cn/post/7649642814956568628>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 从前端工程向 AI 应用工程师转型快一年了，最近突然想写一点自己的感受和一些想法。这里就来跟大家聊一下，既然模型会越来越强，我们这些所谓的 AI 应用工程师做的事情，还有存在的必要吗
> 核心探讨：AI 应用工程的本质矛盾
> 随着基础模型能力的不断跃升，很多 AI 应用开发者都会产生一个真实的焦虑：
> 我们这么努力地优化 Agent 工程，是不是不如模型侧的一次升级？
> 比如在代码编写和分析场景中，模型之所以能知道如何使用工具读写代码，本质是因为训练数据中包含了大量代码和工具使用的 RLHF（基于人类反馈的强化学习）。如果给模型一些相对冷门的工具，它甚至不会去使用。
> 这种现象说明，
> 很多 Agent 工程的努力，本质上是在对冲模型的不足
> 。模型变强，这部分工程价值似乎就会被压缩。
> 然而，这个问题的答案并非非此即彼，而是需要理解两者在价值链上所处的位置。
> 模型提供概率，工程提供确定性
> 第一，模型升级的速度不均匀，工程填补的是“当下的缺口”。今天某个模型在长上下文推理上有缺陷，明天另一个模型补上了，但又在工具调用稳定性上出现了新问题。工程层永远在填补“此时此刻”的缺口，这个需求不会消失，只是内容在变。
> 第二，模型解决的是通用能力，工程解决的是特定场景的可靠性。一个模型能“大概率”写出正确代码，和一个系统能“在生产环境稳定地”完成代码审查任务，是两件事。后者需要错误重试、上下文管理、工具编排、结果验证等。
> 模型提供概率，工程提供确定性。
> 第三，真正的壁垒在于“冷门”工具和私有数据。如果一个工具已经在模型训练数据里，它的使用门槛极低，竞争激烈，利润薄。真正有壁垒的业务场景，往往是那些“冷门”的、私有的、领域专属的工具和数据。让模型学会用这些工具，才是应用层工程师的核心竞争力。
> 第四，模型升级本身也需要应用层来“接住”。模型是基础设施，应用工程是把基础设施变成用户价值的桥梁。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
