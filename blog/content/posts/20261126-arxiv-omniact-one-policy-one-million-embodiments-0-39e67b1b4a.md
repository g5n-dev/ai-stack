---
title: "OmniAct: One Policy, One Million Embodiments"
date: 2026-11-26T06:31:51+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ac99013c018fbc6cf052391596e489675d5714ea19ea0da5359913b27ea42fb0"
source_payload_sha256: "sha256:4dbc1a81ee88d3625118c2d5651d3332714473bfba21d1c7dd8a4d0834944465"
observation_id: obs_39e67b1b4a7b61b89e7aa34be89f70e34ebda609f661ff3472aea61bfa00183f
event_id: evt_dfb393d1c0c1c6e928e73ee74ed7148f92822a79e339723894d03a7030490eae
revision_id: rev_c9b0727cf75c6e7499662c5dfe69d5145ad23f4a8f81d9093e69ee332af0bdea
source_published_at: 2026-11-24T18:59:58Z
first_seen_at: 2026-11-25T22:30:13.685151Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.33158v1
parent_observation_id: null
last_seen_at: 2026-11-25T22:30:13.685151Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.33158v1](http://arxiv.org/abs/2611.33158v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Xiang Fan、Yuheng Wang、Jiayuan Yan 等

## 来源摘要/节选

> A single policy that controls diverse robots must not only transfer task knowledge across embodiments, but also adapt its behavior to each robot's capabilities. Existing approaches facilitate transfer through shared action representations, but these representations do not necessarily capture how differences in robot morphology should shape manipulation strategies. We introduce OmniAct, a cross-embodiment manipulation policy that conditions directly on each robot's kinematics in a specific scene to produce embodiment-specific behavior. This kinematic graph represents the robot's joint positions, motion axes, and connectivity to its visual observation, allowing the policy to account for how its embodiment related to objects and surfaces in the scene. A flow-matching policy predicts relative joint motions for each node, enabling control across robots with different degrees of freedom and kinematic configurations. To learn how physical structure shapes behavior at scale, we procedurally design and filter one million physically feasible robot embodiments; next, we develop algorithms to generate robot trajectories in simulation for all embodiments; finally, we train across diverse simulated manipulation tasks. On 2,000 embodiment-scene-held-out evaluation episodes, OmniAct achieves 63.0% success, compared to 17.8% for pi 0.5 and 57.9% for the strongest baseline; on the task families GPT-6 Astra was evaluated on, it achieves 64.7% against GPT-6 Astra's 41.1%. On a previously unseen real-world robot, it achieves nearly twice the success rate of the next best method, MolmoAct2. Beyond task success, we observe that OmniAct learns distinct manipulation strategies that exploit the capabilities and accommodate the limitations of different morphologies. Project: https://omniact.github.io/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。