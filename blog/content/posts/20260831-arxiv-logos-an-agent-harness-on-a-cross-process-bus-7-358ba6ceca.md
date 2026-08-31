---
title: "Logos: An Agent Harness on a Cross-Process Bus"
date: 2026-08-31T13:35:18+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2cac918cc5dbc5a3d4efe3de1d570b2a07da43419706625db18f5387318540b4"
source_payload_sha256: "sha256:a31f3f90ad83a2125423df6a4ecf04ef5e3223a0e7029d6fdccaccc7944ea6bb"
observation_id: obs_358ba6ceca331fee578ec048c294efe61dc9b59275813c04a8634ca2d7d0d448
event_id: evt_3d8e2e7dcefe3d731f2c531cb915e1380e68b1064686093ce8248b910aba00c8
revision_id: rev_42a1283bd877589b6453c1b13d0be03b0262ac0dcfdd9f2836109b3fcf85038f
source_published_at: 2026-08-28T17:30:10Z
first_seen_at: 2026-08-31T05:32:51.648990Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
interpretation_sha256: "sha256:7f41ab43591cedacccaebe779703ecb10437c2c1eca4dbf482ff12db99b867ac"
description: "Logos 是一个跨进程的智能体框架，采用插件即进程的设计，插件之间只通过只追加的日志共享信息。"
external_url: http://arxiv.org/abs/2608.28553v1
parent_observation_id: null
last_seen_at: 2026-08-31T05:32:51.648990Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.28553v1](http://arxiv.org/abs/2608.28553v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Hanzhang Jia、Liheng Zeng、Hao Cheng 等

## 要点解读

### 这是什么
Logos 是一个跨进程的智能体框架，采用插件即进程的设计，插件之间只通过只追加的日志共享信息。

### 用在哪里
适用于需要在运行时动态组合多个语言模型能力、对故障隔离有严格要求的场景，例如多步骤工具调用的自动化工作流。

### 可以推断的
推测：将每个插件隔离为独立进程后，单个插件的故障不会导致整个系统被挂起。  
推测：系统依赖只追加的日志来维护跨步骤状态，从而保证可追溯性和一致性。

## 来源摘要/节选

> Modern agent systems assemble capabilities at runtime, and this dynamic composition has recently received a complete formal treat ment in the spatiotemporal-composability calculus, in which a capability is a component carrying a tracked inverse, and agents are assembled as plugins. This plugin form is carried by a single process sharing one context, a carrier that places all components in one physical failure domain, a fault suspends every component at once, and process death interrupts every session the process hosts. This paper shows that neither the modeling nor the calculus binds an agent to one process, the statelessness of the language model keeps all cross-step state outside the model, and the soundness invariant is defined on the state space alone. These observations condense into four lemmas whose premises are the hypotheses of the calculus and the statelessness of language-model inference. On these lemmas this paper constructs Logos, a ROS-like cross process agent harness in which a plugin is a process and the only shared state is an append-only transcript. Eighty sessions resume with no repeated effect after kills placed at the four boundaries of the tool-call cycle, and a same-fault comparison with a single process reference configuration shows one fault interrupting every co-resident session while under the peer-process construction one fault ends at one node.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。