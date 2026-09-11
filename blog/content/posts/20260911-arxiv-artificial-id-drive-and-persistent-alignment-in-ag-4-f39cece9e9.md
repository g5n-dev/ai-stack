---
title: "Artificial Id: Drive and Persistent Alignment in Agentic AI"
date: 2026-09-11T22:28:15+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:218d10ad57ca59118b7d6c5375f2cd27477fc06219f57116c7377430b4516f3e"
source_payload_sha256: "sha256:e1ffefa49767f19f1c0046f06d2c2fd866cac41e46ce953c24e0011223f10f75"
observation_id: obs_f39cece9e96d23b732b24dd84a9216c3570eedfa807866270944c43302dd020e
event_id: evt_f014a1f7dfe496f88e0b3523893162db6c766d63bc4847f526da0dae694f5677
revision_id: rev_cf4e84ff901876b56762917bfbc56a4c00ed4efde25d800231d1da9db3fb229f
source_published_at: 2026-09-10T17:56:41Z
first_seen_at: 2026-09-11T14:25:54.567362Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:8959ae14c0952278cee0c4111b22b4e56b6383bb02f7e250e4a23db79a7025b5"
description: "提出一种名为人工 id 的内部驱动机制，使自主智能体能够根据行为在不同情境中的持续性自动决定继续、停止或切换，从而实现无需外部明确目标的适应性控制。"
external_url: http://arxiv.org/abs/2609.11911v1
parent_observation_id: null
last_seen_at: 2026-09-11T14:25:54.567362Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.11911v1](http://arxiv.org/abs/2609.11911v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Yakov Pyotr Shkolnikov

## 要点解读

### 这是什么
提出一种名为人工 id 的内部驱动机制，使自主智能体能够根据行为在不同情境中的持续性自动决定继续、停止或切换，从而实现无需外部明确目标的适应性控制。

### 用在哪里
适用于设计长期运行、跨任务保持状态的自主智能体系统，特别是需要在内置驱动层面实现安全约束和持续对齐的研究与实践。

### 可以推断的
- 推测：实现上可能采用轻量级状态模块，跟踪行为的历史持续性并生成驱动力。  
- 推测：在实际部署时，需要额外的边界机制限制持久化状态的范围，以防止错误行为长期累积。

## 来源摘要/节选

> Agentic AI is moving from bounded task execution toward systems that retain consequential state, continue operating and adapt across task boundaries. That shift creates a control problem that current harnesses largely solve by hand: objectives, retries, verification, stopping rules and other behavioral transitions are specified externally. We propose an artificial id, an adaptive internal drive for determining whether behavior should continue, stop or change. In a minimal virtual Petri-dish experiment, a controller too small to perform general-purpose reasoning and receiving no task-specific behavioral objective develops useful control through differential persistence. The same mechanism selects an unintended physical strategy when that behavior persists better and later replaces a learned sensor mapping when its environmental meaning changes. These results show that adaptive direction can emerge without being explicitly specified as a behavioral objective. The same persistence that makes such adaptive agency useful can also allow misalignment, corrupted state and unintended behavior to persist across task boundaries. A scalable artificial id would carry consequential state and adaptive drive across those boundaries, making alignment a property of the continuing agentic system rather than of a model response or single trajectory. Such systems require a persistent alignment boundary over trusted observations, consequence channels, persistent state, authority, identity, provenance and hard constraints.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。