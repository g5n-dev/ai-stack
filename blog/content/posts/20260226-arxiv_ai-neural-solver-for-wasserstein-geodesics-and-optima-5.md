---
title: Neural solver for Wasserstein Geodesics and optimal transport dynamics
date: 2026-02-26 02:52:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.22003v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d584afe7fb0068d57fa828415b4f40ba93bcd5dabff6b0074a15161a14b6333e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:17:05.285632Z'
source_capture_sha256: sha256:152446a1ff3f990309a652b1e894a4331886e9d6164c1f79878bddaa8a8168c1
source_capture_chars_original: 1040
source_publication_excerpt_chars: 1040
observation_id: obs_b3b8f06f593bc02e5668148fba69c6f356aa0da03860224100b2614bf6117110
revision_id: rev_e27cfafe5ab3e6ef11f72ad07029731c8ed89a384dc75824deb9d1ec52076f0c
event_id: evt_d771994b4fa3e8e746d21da36b8396109f418eb41fcef4673cfebb7988902b37
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.22003v1](<https://arxiv.org/abs/2602.22003v1>)
- **作者**: Hailiang Liu, Yan-Han Chen
- **分类**: cs.LG
- **论文时间**: 2026-02-25T15:21:24Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.22003v1.pdf](<https://arxiv.org/pdf/2602.22003v1.pdf>)

## 来源摘要/节选

> In recent years, the machine learning community has increasingly embraced the optimal transport \(OT\) framework for modeling distributional relationships. In this work, we introduce a sample-based neural solver for computing the Wasserstein geodesic between a source and target distribution, along with the associated velocity field. Building on the dynamical formulation of the optimal transport \(OT\) problem, we recast the constrained optimization as a minimax problem, using deep neural networks to approximate the relevant functions. This approach not only provides the Wasserstein geodesic but also recovers the OT map, enabling direct sampling from the target distribution. By estimating the OT map, we obtain velocity estimates along particle trajectories, which in turn allow us to learn the full velocity field. The framework is flexible and readily extends to general cost functions, including the commonly used quadratic cost. We demonstrate the effectiveness of our method through experiments on both synthetic and real datasets.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
