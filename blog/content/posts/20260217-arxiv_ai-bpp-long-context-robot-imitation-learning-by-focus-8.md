---
title: 'BPP: Long-Context Robot Imitation Learning by Focusing on Key History Frames'
date: 2026-02-17 22:35:47+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15010v1
aliases:
- /posts/20260218-arxiv_ai-bpp-long-context-robot-imitation-learning-by-focus-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b78da209d3b0d7ab7dd9c316406a0fbf2ef4a404d23430bf9563fe35d83ea042
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:15:33.978565Z'
source_capture_sha256: sha256:ac163f5c55d870e2c272ee9733940b459faddb4e9136763c1d5f55121ecbb445
source_capture_chars_original: 1467
source_publication_excerpt_chars: 1467
observation_id: obs_c9a5b5ecd52b1678b55f57ed2c18dafdc21f3a9ab41637c94acb943b3a6d3aa1
revision_id: rev_27bebbfdc70d5b32e6fbe4311041f2275212e86bbec36a8a3c71d325ea9b48be
event_id: evt_1da877403dceaea107caa3ac44c83fefa712318c04ce0b03462e5f90a1567b70
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-17T09:52:08Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15010v1](<https://arxiv.org/abs/2602.15010v1>)
- **作者**: Max Sobol Mark, Jacky Liang, Maria Attarian, Chuyuan Fu, Debidatta Dwibedi, Dhruv Shah, Aviral Kumar
- **分类**: cs.RO
- **论文时间**: 2026-02-16T18:49:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15010v1.pdf](<https://arxiv.org/pdf/2602.15010v1.pdf>)

## 来源摘要/节选

> Many robot tasks require attending to the history of past observations. For example, finding an item in a room requires remembering which places have already been searched. However, the best-performing robot policies typically condition only on the current observation, limiting their applicability to such tasks. Naively conditioning on past observations often fails due to spurious correlations: policies latch onto incidental features of training histories that do not generalize to out-of-distribution trajectories upon deployment. We analyze why policies latch onto these spurious correlations and find that this problem stems from limited coverage over the space of possible histories during training, which grows exponentially with horizon. Existing regularization techniques provide inconsistent benefits across tasks, as they do not fundamentally address this coverage problem. Motivated by these findings, we propose Big Picture Policies \(BPP\), an approach that conditions on a minimal set of meaningful keyframes detected by a vision-language model. By projecting diverse rollouts onto a compact set of task-relevant events, BPP substantially reduces distribution shift between training and deployment, without sacrificing expressivity. We evaluate BPP on four challenging real-world manipulation tasks and three simulation tasks, all requiring history conditioning. BPP achieves 70% higher success rates than the best comparison on real-world evaluations.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
