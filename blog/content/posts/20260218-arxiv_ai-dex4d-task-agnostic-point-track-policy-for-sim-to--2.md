---
title: 'Dex4D: Task-Agnostic Point Track Policy for Sim-to-Real Dexterous Manipulation'
date: 2026-02-18 21:10:38+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15828v1
aliases:
- /posts/20260219-arxiv_ai-dex4d-task-agnostic-point-track-policy-for-sim-to--2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a74fb08be4aef4bce72cfa3560f9af3ead26ae1acdc7b3e5df1ce0b7e6e8b5d4
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:15:52.664467Z'
source_capture_sha256: sha256:94928275a9d6fa098cce83db70c3662260bf295b1e6063b986cf83ff90a96d76
source_capture_chars_original: 1618
source_publication_excerpt_chars: 1618
observation_id: obs_c63feb724afebb2d5fd12faf93e9f6b8b63b3ec8a49c20d28d0224a3a2946546
revision_id: rev_6fc3e9804568fb4daaecc884d1b718ce5a63f67a8757b526e33d1be518f6e94b
event_id: evt_ba0e2d1d6063281d5dd890bf29120795a1faf94d50e51da067dde90e935f59b6
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15828v1](<https://arxiv.org/abs/2602.15828v1>)
- **作者**: Yuxuan Kuang, Sungjae Park, Katerina Fragkiadaki, Shubham Tulsiani
- **分类**: cs.RO
- **论文时间**: 2026-02-17T18:59:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15828v1.pdf](<https://arxiv.org/pdf/2602.15828v1.pdf>)

## 来源摘要/节选

> Learning generalist policies capable of accomplishing a plethora of everyday tasks remains an open challenge in dexterous manipulation. In particular, collecting large-scale manipulation data via real-world teleoperation is expensive and difficult to scale. While learning in simulation provides a feasible alternative, designing multiple task-specific environments and rewards for training is similarly challenging. We propose Dex4D, a framework that instead leverages simulation for learning task-agnostic dexterous skills that can be flexibly recomposed to perform diverse real-world manipulation tasks. Specifically, Dex4D learns a domain-agnostic 3D point track conditioned policy capable of manipulating any object to any desired pose. We train this 'Anypose-to-Anypose' policy in simulation across thousands of objects with diverse pose configurations, covering a broad space of robot-object interactions that can be composed at test time. At deployment, this policy can be zero-shot transferred to real-world tasks without finetuning, simply by prompting it with desired object-centric point tracks extracted from generated videos. During execution, Dex4D uses online point tracking for closed-loop perception and control. Extensive experiments in simulation and on real robots show that our method enables zero-shot deployment for diverse dexterous manipulation tasks and yields consistent improvements over prior baselines. Furthermore, we demonstrate strong generalization to novel objects, scene layouts, backgrounds, and trajectories, highlighting the robustness and scalability of the proposed framework.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
