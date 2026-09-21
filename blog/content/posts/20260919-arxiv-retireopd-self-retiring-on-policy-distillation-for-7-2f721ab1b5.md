---
title: "RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning"
date: 2026-09-19T13:56:21+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9ac4ce53dd5fe04fb27e6da96a01a78e0f37ef5a228ffc090adf5c0213b83ed5"
source_payload_sha256: "sha256:ecc810acb70e08775c645e201af6cc3acaf06cdec71ccde86a5c27f09a5ec39c"
observation_id: obs_2f721ab1b590614f25eb3c1224b109c5ee106054ea82841cdba5faa7cf448114
event_id: evt_a4423403c1c30c4a0fdc50801ee7d53b0e6ece3406c0ce619686c6687c778d1c
revision_id: rev_5dc774e6190953c30298618d1d73e228d36d71bf9b8d560b7123fc1206712704
source_published_at: 2026-09-17T17:52:08Z
first_seen_at: 2026-09-19T06:06:33Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.20784v1
parent_observation_id: null
last_seen_at: 2026-09-21T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20784v1](http://arxiv.org/abs/2609.20784v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yan Yu、Zhengxi Lu、Yizhou Liu 等

## 来源摘要/节选

> Multi-turn agents trained with reinforcement learning (RL) receive a single scalar reward per trajectory, which motivates self on-policy distillation (OPD) to supply dense token-level supervision from a self-teacher with privileged task skills, letting a skill-free student internalize them. This recipe, however, is undermined by two findings in agentic tasks: privileged information alone does not always make a teacher reliable, and the benefit of teacher supervision is stage-dependent. We therefore propose RetireOPD (Self-Retiring On-Policy Distillation), which first optimizes a decoupled, skill-conditioned teacher with environment rewards and then trains a skill-free student jointly with RL and OPD. Rather than following a predefined distillation schedule, RetireOPD adopts Adaptive Retirement: the student drops the teacher on its own once their discrepancy stops shrinking and it reaches a target fraction of the teacher's success rate, after which training proceeds with RL alone. Across Qwen2.5 models from 1.5B to 7B, RetireOPD improves ALFWorld success rate over RL baseline by 14.1% to 18.8% and WebShop accuracy by 11.8% to 19.0%, and surpasses its own skill-conditioned teacher in every setting.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。