---
title: "The Physics of Multi-Turn Long-Horizon Planning: From Pre-training to Post-training via Single- and Multi-Teacher On-Policy Agentic Distillation"
date: 2026-07-29T08:15:51+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5fd142b28144e9474c4d6785ec2ccc01b6c7d6dd74d22c48ba9018a053c1e170"
source_payload_sha256: "sha256:c94a1a2780ae2ffe6acce3b8388ed55c45e454200a91fab6975da076716969a9"
observation_id: obs_4e457fdcc117e370eaceb710e6e12005618252b4265f965bb26de91e97e79ae9
event_id: evt_2e6760a29b72761b52a1420509312a3af5cc719f7ad28049f4b3b881652527da
revision_id: rev_916fe8ea92922b6654f8cad6e7da8432cd63b53d4324f345964aa122666e4c9e
source_published_at: 2026-07-27T17:55:03Z
first_seen_at: 2026-07-29T00:14:49.994715Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 144
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.24720v1
parent_observation_id: null
last_seen_at: 2026-07-29T00:14:49.994715Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.24720v1](http://arxiv.org/abs/2607.24720v1)

## 来源摘要/节选

> Multi-turn long-horizon planning is critical for foundation model agents, yet how to fundamentally improve it remains unclear. Existing models are trained on uncontrollable and opaque Internet data, making it difficult to identify how planning ability is acquired, shaped, and integrated. To address this challenge, we introduce a unified and controlled multi-turn environment that enables precise control. It allows systematically study long-horizon planning across three stages. (1) Planning ability acquisition during pre-training. We study data format, distribution, and quality. Explicit world model construction through CoT state transition modeling yields stronger long-horizon generalization. Atomic skills alone are insufficient for compositional generalization, whereas a litte long-horizon data works. Moreover, suboptimal trajectories severely impair performance because errors amplify over long horizons. (2) Planning ability shaping via GRPO and OPD post-training. Through mutual information, we distinguish general planning patterns from task-specific planning knowledge. For planning patterns, we identify three application regions of post-training: unnecessary, effective, and unsupported. OPD has a broader effective region than GRPO under low-quality and long-horizon settings, as it provides more consistent update directions. For planning knowledge, distilling unseen procedures from a teacher with different knowledge may impair student's prior world modeling without fully establishing new knowledge. (3) Planning ability integration through MOPD post-training. We show that multi-teacher on-policy distillation (MOPD) integrates capabilities by converging to shared planning-pattern across environments. Compatible patterns enable cross-environment generalization, partially shared patterns support continual learning, while completely conflicting patterns cause severe interference.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。