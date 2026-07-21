---
title: 'AutoDex: An Automated Real-World System for Dexterous Grasping Data Collection'
date: 2026-06-23 22:43:33+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 数据库
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.23689v1
aliases:
- /posts/20260624-arxiv_ai-autodex-an-automated-real-world-system-for-dextero-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d0b2a056ecff0982c26e4e47cd30bda138eab31369c425bcd39f26a679f4b980
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:30:09.568344Z'
source_capture_sha256: sha256:e099b54db0a366e46ec011355948451d7eb5f70f10cd1a7d52dddd8a60203362
source_capture_chars_original: 1551
source_publication_excerpt_chars: 1551
observation_id: obs_e8f9ae16c2b0bed64b1a2c6e8a5e3b20fb7d214b48fb973754697158f8478cd4
revision_id: rev_cfa6f9288867bbdc97a4d7ec6daf304e4e2dc7f18c1c1d37cbd44b3be6233338
event_id: evt_1e1a5af2fccdf58761bc1ef33d613255ac3b4a3d864b10729e21965963c8ba7a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-23T10:46:35Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.23689v1](<https://arxiv.org/abs/2606.23689v1>)
- **作者**: Mingi Choi, Gunhee Kim, Jisoo Kim, Taeksoo Kim, Taeyun Ha, Jongbin Lim, Hanbyul Joo
- **分类**: cs.RO
- **论文时间**: 2026-06-22T17:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.23689v1.pdf](<https://arxiv.org/pdf/2606.23689v1.pdf>)

## 来源摘要/节选

> Learning robust dexterous grasping requires real-world data that records the physical outcomes of grasp attempts. Such data is hard to obtain at scale: teleoperation yields valid physical outcomes but is slow and operator-biased, while simulation-based generation is cheap and scalable but cannot certify contact validity. A natural solution is to generate candidate grasps and verify them on real hardware, but this scales only if the entire collection loop \(perception, execution, labeling, and reset\) runs without human intervention. We present AutoDex, an automated real-world data-collection system that closes this loop: for each candidate from a replaceable generator, it localizes the object under severe hand-object occlusion with dense 20-camera perception, executes collision-monitored robot motions, labels lift-and-hold success or failure, and actively resets the object between trials to expose additional candidates across stable poses. The result is a reusable database of physically labeled grasp trials that downstream systems can query by retrieval and feasibility filtering. Using AutoDex, we collect 3,593 grasp trials across Allegro and Inspire hands on 100 diverse objects, with synchronized multi-view observations and robot-state logs. For a matched 500-trajectory collection, AutoDex requires 10.3 h versus 49.4 h for teleoperation, yielding a 4.8x throughput improvement, and grasps retrieved from the AutoDex-validated database succeed 76% versus 34% for simulation-only validation. Code and data will be publicly released.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
