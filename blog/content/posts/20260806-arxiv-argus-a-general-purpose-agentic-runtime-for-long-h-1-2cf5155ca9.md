---
title: "Argus: A General-Purpose Agentic Runtime for Long-Horizon Reasoning"
date: 2026-08-06T11:37:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d85485a4d69a811dea0dfb94942c04bd36a2cc933a0ca018481bd44eb998102c"
source_payload_sha256: "sha256:c3c38a95afe22064ca8051394d9d0fe00e95e848cd9c863c5b3daad7516f46d5"
observation_id: obs_2cf5155ca9444c932c4dc993f2b718bea076e6e1a79152ee06019150231a0cfb
event_id: evt_0a35f9d363a4901a9f53e04e89203a7f965680ca7089f9631ed99875abb1fd02
revision_id: rev_970ecb1dbfc75fc8318f680c32b45c8948a48f2bf46832ef501a6159daa1b8b8
source_published_at: 2026-08-05T17:58:58Z
first_seen_at: 2026-08-06T03:46:00Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
interpretation_sha256: "sha256:ccc321d7826e87edbc5611fab18ea8824cefb11e05db4f1e5277a27abbcff591"
description: "Argus 是一种持续、自我进化的智能体运行时，采用 Manager、Planner、Engineer、Reviewer 四类角色在项目状态上进行有界任务执行。它将用户意图与具体目标、约束及验证条件分离，在模型权重保持不变的前提下通过持久化的运行时状态和控制策略实现自我演化。"
external_url: http://arxiv.org/abs/2608.05144v1
parent_observation_id: null
last_seen_at: 2026-08-07T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.05144v1](http://arxiv.org/abs/2608.05144v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Boxiu Li、Zimo Wen、Yijia Fan 等

## 要点解读

### 这是什么
Argus 是一种持续、自我进化的智能体运行时，采用 Manager、Planner、Engineer、Reviewer 四类角色在项目状态上进行有界任务执行。它将用户意图与具体目标、约束及验证条件分离，在模型权重保持不变的前提下通过持久化的运行时状态和控制策略实现自我演化。

### 用在哪里
适用于需要跨阶段、长周期推理并能够自动纠错的复杂软件工程或数学任务。对于希望在保持模型不变的情况下，通过流程优化和验证驱动提升效率的团队或个人，这种运行时提供了可追溯的决策链和自动化的自我改进机制。

### 可以推断的
推测：在代码调试、系统级优化或大规模数学证明等需要反复验证和回滚的场景中，这种角色分离与验证门控的设计可能带来更高的任务完成率。  
推测：由于自我演化依赖于持久化的运行时状态而非模型权重，组织内部可以更灵活地部署和迭代工作流，而无需频繁重新训练模型。

## 来源摘要/节选

> Long-horizon reasoning requires an agentic runtime that can persist when evidence supports its current approach and pivot when measurements reveal failure, hidden constraints, or a misspecified objective. We present Argus, a persistent, self-evolving runtime in which Manager, Planner, Engineer, and Reviewer execute bounded missions over durable project state. Argus separates stable user intent from operational objectives, constraints, and verification criteria, and admits memories, skills, procedures, verifiers, routing decisions, and rejected routes only after role-owned review and, when available, task-native verification. Model weights remain fixed; self-evolution occurs through persistent runtime state and control policy, with autonomous execution between operator-owned escalation points. Across seven GPT-5.5 benchmark arenas, Argus achieves about 78% on SWE-Bench Pro versus 59% for Direct Copilot while using 1.41 times the aggregate tokens. After verification-gated self-evolution, mature SWE-Bench waves use 21% fewer solve-input tokens and 15% less active workflow time per task than startup waves, while recording 34 verifier recoveries and 22 strict review-loop rescues. Argus also reaches 76.8% on AARRI-Bench and a 28.0-point gap on mathematical data synthesis, with competitive GPU-kernel and language-model-training results. Beyond benchmarks, an optimized RWKV6 kernel was merged upstream; a multi-day mathematics campaign retained falsified routes and proof-backed frontier updates; and six paper pipelines completed 254 missions with 16 stage rollbacks. These results show that a fixed-weight, self-evolving harness can revise, recover, and accumulate verified approaches while producing structured trajectories for future supervised and reinforcement learning.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。