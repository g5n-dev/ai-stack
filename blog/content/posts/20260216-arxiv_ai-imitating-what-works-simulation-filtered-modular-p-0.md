---
title: 'Imitating What Works: Simulation-Filtered Modular Policy Learning from Human
  Videos'
date: 2026-02-16 23:54:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.13197v1
aliases:
- /posts/20260217-arxiv_ai-imitating-what-works-simulation-filtered-modular-p-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:99c3530ce62b0d8f27231bf7b01ef7d40851feaf87eaff9be3894a33f21bf614
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
captured_at: '2026-07-18T04:15:26.440768Z'
source_capture_sha256: sha256:4c50d680ad3705c84fc895a839b5fbd6463cb0720f14327b9695d66aead42e88
source_capture_chars_original: 1344
source_publication_excerpt_chars: 1344
observation_id: obs_17149c3514220d35f7f14cd0213b8c119f240df077421ac62ee546ede0aecf50
revision_id: rev_0156b3003844ea0a0b9db2fd7cc2c939f5ed9d3ec066c629941a4ce6422c1b56
event_id: evt_d10db967313886b57f694c351dcffc35e22e751d952064ca9823483d95a0de01
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-16T03:51:58Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.13197v1](<https://arxiv.org/abs/2602.13197v1>)
- **作者**: Albert J. Zhai, Kuo-Hao Zeng, Jiasen Lu, Ali Farhadi, Shenlong Wang, Wei-Chiu Ma
- **分类**: cs.RO
- **论文时间**: 2026-02-13T18:59:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.13197v1.pdf](<https://arxiv.org/pdf/2602.13197v1.pdf>)

## 来源摘要/节选

> The ability to learn manipulation skills by watching videos of humans has the potential to unlock a new source of highly scalable data for robot learning. Here, we tackle prehensile manipulation, in which tasks involve grasping an object before performing various post-grasp motions. Human videos offer strong signals for learning the post-grasp motions, but they are less useful for learning the prerequisite grasping behaviors, especially for robots without human-like hands. A promising way forward is to use a modular policy design, leveraging a dedicated grasp generator to produce stable grasps. However, arbitrary stable grasps are often not task-compatible, hindering the robot's ability to perform the desired downstream motion. To address this challenge, we present Perceive-Simulate-Imitate \(PSI\), a framework for training a modular manipulation policy using human video motion data processed by paired grasp-trajectory filtering in simulation. This simulation step extends the trajectory data with grasp suitability labels, which allows for supervised learning of task-oriented grasping capabilities. We show through real-world experiments that our framework can be used to learn precise manipulation skills efficiently without any robot data, resulting in significantly more robust performance than using a grasp generator naively.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
