---
title: 'PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization'
date: 2026-03-16 23:16:09+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.13228v1
aliases:
- /posts/20260317-arxiv_ai-physmodpo-physically-plausible-humanoid-motion-wit-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1076ca8a9ac7393c894c7dc6fcd99fd3e15c564b8b7e5a70db18b65c76676cb8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:28:19.053555Z'
source_capture_sha256: sha256:9143b24f1f8b6b6dbb8fc7d664a159fa1834f34d6074d290a6d9240fa6d3d9d1
source_capture_chars_original: 1369
source_publication_excerpt_chars: 1369
observation_id: obs_a8ec751fb4ba4fb5cc9c42295a463acdc03f4c670e096e162974c91dc3c6149c
revision_id: rev_187265234adb4ffe40c01e20cb3a0339e35e5bff64eb4779c098325d274e3809
event_id: evt_2cae66cbbd59b7042bdcf250b367a10e5a14518d44f1c4b2e69f26f10b23182e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.13228v1](<https://arxiv.org/abs/2603.13228v1>)
- **作者**: Yangsong Zhang, Anujith Muraleedharan, Rikhat Akizhanov, Abdul Ahad Butt, Gül Varol, Pascal Fua, Fabio Pizzati, Ivan Laptev
- **分类**: cs.LG
- **论文时间**: 2026-03-13T17:59:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.13228v1.pdf](<https://arxiv.org/pdf/2603.13228v1.pdf>)

## 来源摘要/节选

> Recent progress in text-conditioned human motion generation has been largely driven by diffusion models trained on large-scale human motion data. Building on this progress, recent methods attempt to transfer such models for character animation and real robot control by applying a Whole-Body Controller \(WBC\) that converts diffusion-generated motions into executable trajectories. While WBC trajectories become compliant with physics, they may expose substantial deviations from original motion. To address this issue, we here propose PhysMoDPO, a Direct Preference Optimization framework. Unlike prior work that relies on hand-crafted physics-aware heuristics such as foot-sliding penalties, we integrate WBC into our training pipeline and optimize diffusion model such that the output of WBC becomes compliant both with physics and original text instructions. To train PhysMoDPO we deploy physics-based and task-specific rewards and use them to assign preference to synthesized trajectories. Our extensive experiments on text-to-motion and spatial control tasks demonstrate consistent improvements of PhysMoDPO in both physical realism and task-related metrics on simulated robots. Moreover, we demonstrate that PhysMoDPO results in significant improvements when applied to zero-shot motion transfer in simulation and for real-world deployment on a G1 humanoid robot.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
