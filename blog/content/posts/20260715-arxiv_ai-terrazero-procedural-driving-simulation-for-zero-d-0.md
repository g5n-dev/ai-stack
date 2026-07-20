---
title: 'TerraZero: Procedural Driving Simulation for Zero-Demonstration Self-Play
  at Scale'
date: 2026-07-15 16:55:26+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2607.13028v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:858afce00e4896a8baf7797153d882ccb699395245dee53428aa4a1ef4bacc6b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:30:29.635417Z'
source_capture_sha256: sha256:b809de27cdb8796814e6dbec864b0dfa110970b4d8d7f7ec7fb0b06242f6df49
source_capture_chars_original: 1919
source_publication_excerpt_chars: 1919
observation_id: obs_13920c7606064f656cd0eb3efaf848542f5d82ffa9fee2918a68701401b5d492
revision_id: rev_ce7af2f892df717f48d0d38acfa67f8787babc52d624d8ab924f660f99729202
event_id: evt_d4fe9e5f101b30739db7a549450faed06b7b4280b24027fb6704497e88fe966d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-15T08:56:23Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.13028v1](<https://arxiv.org/abs/2607.13028v1>)
- **作者**: Zhouchonghao Wu, Akshay Rangesh, Weixin Li, Wei-Jer Chang, Zachary Lee, Tim Wang, Wei Zhan
- **分类**: cs.LG
- **论文时间**: 2026-07-14T17:59:02Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.13028v1.pdf](<https://arxiv.org/pdf/2607.13028v1.pdf>)

## 来源摘要/节选

> Training robust autonomous driving agents requires a simulator that is fast enough for reinforcement learning at scale, realistic enough to ground behavior in real-world map structure, and diverse enough to cover the safety-critical long tail that logged data rarely contains. We present TerraZero, a procedural driving simulator and self-play training stack. A configurable C engine runs simulation on the CPU and policy inference on the GPU over a zero-copy path, sustaining 1.3M agent-steps per second on a single server-grade GPU, far faster than existing object-level simulators, while keeping fidelity lighter single-agent systems omit: heterogeneous agents, multiple dynamics models, and full traffic-rule enforcement. TerraZero treats logged data only as a source of real-world map geometry, populating each map with randomized rule-based road users and signal controllers and randomizing agent dynamics, rewards, and sizes per episode, so a map yields an unbounded set of scenarios. Every reported policy trains from scratch by reinforcement learning alone on a compute-efficient self-play recipe across GPUs, with zero human demonstrations and no fallback planner at inference. Policies generalize zero-shot across cities and datasets, including emergent left-hand-traffic driving without explicit supervision. As an ego policy, TerraZero is the first fully learned policy to top the InterPlan long-tail benchmark, ahead of larger learned planners; on routine-driving val14 it ranks among the best approaches and is the safest, posting the best collision and time-to-collision scores. On Waymo Open Sim Agents realism the same recipe outperforms other demonstration-free methods and is competitive with the strongest reference-anchored self-play method. One stack serves both roles: driving policies across dynamics for cars and trucks, and sim agents that jointly control vehicles, pedestrians, and cyclists.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
