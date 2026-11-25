---
title: "OmniAct: One Policy, One Million Embodiments"
date: 2026-11-25T20:51:49+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ac99013c018fbc6cf052391596e489675d5714ea19ea0da5359913b27ea42fb0"
source_payload_sha256: "sha256:4dbc1a81ee88d3625118c2d5651d3332714473bfba21d1c7dd8a4d0834944465"
observation_id: obs_39e67b1b4a7b61b89e7aa34be89f70e34ebda609f661ff3472aea61bfa00183f
event_id: evt_dfb393d1c0c1c6e928e73ee74ed7148f92822a79e339723894d03a7030490eae
revision_id: rev_c9b0727cf75c6e7499662c5dfe69d5145ad23f4a8f81d9093e69ee332af0bdea
source_published_at: 2026-11-24T18:59:58Z
first_seen_at: 2026-11-25T12:50:23.399678Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
interpretation_sha256: "sha256:3614ac1c5b73e9b46160675addd213c3ec73169cacfa6de9f99b2bc70fb55623"
description: "OmniAct 是一种跨不同机器人形态的通用操作策略，直接依据机器人关节位置、运动轴及与视觉场景的连接关系，生成适合各自身体结构的相对关节运动。其训练覆盖一百万种经程序生成与筛选的可行机器人形态。"
external_url: http://arxiv.org/abs/2611.33158v1
parent_observation_id: null
last_seen_at: 2026-11-25T12:50:23.399678Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.33158v1](http://arxiv.org/abs/2611.33158v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Xiang Fan、Yuheng Wang、Jiayuan Yan 等

## 要点解读

### 这是什么
OmniAct 是一种跨不同机器人形态的通用操作策略，直接依据机器人关节位置、运动轴及与视觉场景的连接关系，生成适合各自身体结构的相对关节运动。其训练覆盖一百万种经程序生成与筛选的可行机器人形态。

### 用在哪里
它适用于需要用同一套策略控制多种机器人、执行不同形态下的抓取与操作任务的场景，尤其面向机器人策略研发者、仿真训练平台及多形态机器人系统团队。

### 可以推断的
- 推测：把形态信息直接纳入策略，可能减少针对每种机器人分别设计动作表示或适配控制逻辑的工作。
- 推测：在仿真中扩展到大量形态后训练，可能有助于策略迁移到训练阶段未出现的真实机器人。

## 来源摘要/节选

> A single policy that controls diverse robots must not only transfer task knowledge across embodiments, but also adapt its behavior to each robot's capabilities. Existing approaches facilitate transfer through shared action representations, but these representations do not necessarily capture how differences in robot morphology should shape manipulation strategies. We introduce OmniAct, a cross-embodiment manipulation policy that conditions directly on each robot's kinematics in a specific scene to produce embodiment-specific behavior. This kinematic graph represents the robot's joint positions, motion axes, and connectivity to its visual observation, allowing the policy to account for how its embodiment related to objects and surfaces in the scene. A flow-matching policy predicts relative joint motions for each node, enabling control across robots with different degrees of freedom and kinematic configurations. To learn how physical structure shapes behavior at scale, we procedurally design and filter one million physically feasible robot embodiments; next, we develop algorithms to generate robot trajectories in simulation for all embodiments; finally, we train across diverse simulated manipulation tasks. On 2,000 embodiment-scene-held-out evaluation episodes, OmniAct achieves 63.0% success, compared to 17.8% for pi 0.5 and 57.9% for the strongest baseline; on the task families GPT-6 Astra was evaluated on, it achieves 64.7% against GPT-6 Astra's 41.1%. On a previously unseen real-world robot, it achieves nearly twice the success rate of the next best method, MolmoAct2. Beyond task success, we observe that OmniAct learns distinct manipulation strategies that exploit the capabilities and accommodate the limitations of different morphologies. Project: https://omniact.github.io/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。