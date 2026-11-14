---
title: "CoReMem: Cost-Internalizing Memory for Successive Coding Tasks with Prospective Valuation"
date: 2026-11-15T05:29:47+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9c4a0136c7aa8154b1cab24a5405208e04621744eef21a1825af298d23ac5256"
source_payload_sha256: "sha256:9f81f5b78d8075d963638ea9d09deada4bc2feaf3974ec4d0431ba3868fc31e7"
observation_id: obs_21fb7be8e1ad838382dac69bd380e79bc41ed2c103bc993095e2b1120932de21
event_id: evt_155205a4f5d7b2566ae335294c006f4b5c3d321a75bbada04827a522ad888bcd
revision_id: rev_541191e878afec0ad82e8191125e5684c5d3554ff35e4ed5c8d91adbd902a8d5
source_published_at: 2026-11-12T18:58:22Z
first_seen_at: 2026-11-14T21:28:36.481647Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
interpretation_sha256: "sha256:7fd47996a2e65659a6ebcc6730653f5d5c5ebbdc38fc492be2094f165e3843d7"
description: "CoReMem 是一种面向连续编程任务的记忆框架，在写入、读取记忆时权衡成本与未来收益。它通过比较下一任务在不同记忆条件下的表现，筛选更有价值的代码库位置与可执行检查。"
external_url: http://arxiv.org/abs/2611.17316v1
parent_observation_id: null
last_seen_at: 2026-11-14T21:28:36.481647Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.17316v1](http://arxiv.org/abs/2611.17316v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Peiwen Li、Harshit Verma、Sophia Zhou 等

## 要点解读

### 这是什么
CoReMem 是一种面向连续编程任务的记忆框架，在写入、读取记忆时权衡成本与未来收益。它通过比较下一任务在不同记忆条件下的表现，筛选更有价值的代码库位置与可执行检查。

### 用在哪里
适用于需要在一个持续演化的代码仓库上连续处理任务、并把先前修改和经验传递给后续任务的编程智能体。ChainSWE 实验中，27B 编程智能体的解决率从 21.0% 提升至 25.7%，同时减少了步骤数和缓存感知令牌消耗。

### 可以推断的
- 推测：对于任务目标尚不明确的连续编程场景，按实际收益筛选记忆可能比无条件保留全部经验更节省计算资源。
- 推测：把记忆内容限定为代码库位置和可执行检查，可能有助于增强记忆与后续修改之间的可验证性。

## 来源摘要/节选

> Coding agents tackle successive tasks on an evolving repository, carrying forward edits and writing memory before the next task is known. Selecting memory for unknown next tasks requires balancing future usefulness against the costs of writing and reading it. The actor must also decide when acting on available memory saves effort as the task unfolds. We introduce Coding-Repository Memory (CoReMem), a cost-internalizing framework that guides memory design and actor adaptation through measured memory value on the next task. Prospective segment valuation compares runs of the next task with and without individual trajectory segments from the same inherited repository state, guiding a compact memory built around anchors: repository locations and executable checks. Actor adaptation estimates on-policy memory value within rollout groups with and without memory, using a reward that prioritizes resolution and penalizes step count in successful runs. Provenance-gated value credit assigns the additional value term to steps identified as using memory-supplied anchors, while every step retains outcome credit. On ChainSWE, CoReMem raises the 27B actor's resolve rate from 21.0% to 25.7%, with 17% fewer steps and 11% fewer total cache-aware tokens, including memory-module calls, relative to the untrained actor model without memory.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。