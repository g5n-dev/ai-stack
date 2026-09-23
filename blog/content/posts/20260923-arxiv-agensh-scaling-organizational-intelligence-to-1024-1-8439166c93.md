---
title: "Agensh: Scaling Organizational Intelligence to 1,024 Agents"
date: 2026-09-23T19:36:51+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8700ed59689004c310143c18cfc232c3908cd95875658c66ab277ed2c1366a8e"
source_payload_sha256: "sha256:0be8d0b8829349df61a3feafe95323c5062e02693c7e5e65553791aeae6b6e43"
observation_id: obs_8439166c9314ca5e67cdd77cb141d9943edba2181a6cd53a2b9bf060fe8b6579
event_id: evt_3812a39a9d8cb5176c9adf0501c89e1db13ede343b64af4d6846c500b53b1f11
revision_id: rev_91f7a334efc8774d577751757e1e8d0a2811437fc837aa81068293650b017233
source_published_at: 2026-09-22T17:56:25Z
first_seen_at: 2026-09-23T11:47:53Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:086846e367307f34c891fd209c21ce7337aa3579fea54020e1506e7b41edc7cb"
description: "Agensh 是一个去中心化的多智能体框架，让大量工作单元通过共享工作区、消息接口和公共上下文自行组织、竞争和协作完成任务，而无需统一的调度者。"
external_url: http://arxiv.org/abs/2609.26781v1
parent_observation_id: null
last_seen_at: 2026-09-23T11:34:11.031525Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.26781v1](http://arxiv.org/abs/2609.26781v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Zhihao Zhan、Ting Song、Li Dong 等

## 要点解读

### 这是什么  
Agensh 是一个去中心化的多智能体框架，让大量工作单元通过共享工作区、消息接口和公共上下文自行组织、竞争和协作完成任务，而无需统一的调度者。  

### 用在哪里  
该方案适合需要高并发、低时延且任务可拆分的复杂场景，尤其在算力或时间预算紧张时，可通过扩大智能体规模来提升整体效能。  

### 可以推断的  
- 推测：在没有中心调度的情况下，任务分解、自我认领和结果验证的循环机制是实现大规模并发的关键。  
- 推测：随着智能体数量增多，组织内部会逐步形成标准化的协作模式，从而进一步提升任务完成率。

## 来源摘要/节选

> A multi-agent system can reduce latency on complex tasks by executing work concurrently. Several pioneering harness frameworks support multi-agent systems. However, the scalability of current multi-agent harnesses is often constrained by a central orchestrator's capacity to allocate tasks and coordinate workers. To address this limitation, we introduce Agensh, a scalable self-organized multi-agent harness without a central orchestrator: concurrent workers execute a multi-agent cooperation loop, continuously gathering context, claiming and self-assigning sub-tasks, taking action and sharing findings, verifying results, and merging progress in an asynchronous manner. The loop is supported by the agentic organization infrastructure comprising three components: a shared workspace holds proposed, ongoing, and completed work; a message interface lets workers communicate; and shared context retains reusable findings and work intentions. To test the scalability of Agensh, we evaluate it on the five hardest ProgramBench tasks with GPT-5.6-sol (high). Scaling from 1 to 128 agents raises the mean final test-pass rate from 19.31% to 28.78%, an approximately 49% relative improvement. Larger organizations reach comparable test-pass rates earlier. On pandoc, scaling from 1 to 1,024 agents raises the final test-pass rate from 33.89% to 55.06%. Worker trajectories further show that different forms of self-organized cooperation gradually emerges and standardizes as the organization grows. These results reveal the number of agents as a new scaling dimension for multi-agent organizations to expand the frontier of general intelligence, offering a practical solution for complex tasks under hard latency constraints or time budgets.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。