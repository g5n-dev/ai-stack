---
title: Constrained Group Relative Policy Optimization
date: 2026-02-06 03:10:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.05863v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f7d65bf4031279915a2679b3594afcf1169b9ed87cfbb45aec65da7a6fa1c972
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:11:05.007784Z'
source_capture_sha256: sha256:82624ea870ac010afe60f6299dbff200601219fc5ed85123f1a5058535e4fdc6
source_capture_chars_original: 1361
source_publication_excerpt_chars: 1361
observation_id: obs_8a41594ef69e3c0f9d6d3b46125c4a7363f2ae9bc3ecade56384e7cb16562f06
revision_id: rev_29713c33207089a18b5912cda0add7d2f3d957242738b7b604511b662f9dd797
event_id: evt_59b1995b5778eada50fa36b3baec3c96de382728ab5de9bdfc2f248b94bdb06e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.05863v1](<https://arxiv.org/abs/2602.05863v1>)
- **作者**: Roger Girgis, Rodrigue de Schaetzen, Luke Rowe, Azalée Robitaille, Christopher Pal, Liam Paull
- **分类**: cs.LG
- **论文时间**: 2026-02-05T16:44:23Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.05863v1.pdf](<https://arxiv.org/pdf/2602.05863v1.pdf>)

## 来源摘要/节选

> While Group Relative Policy Optimization \(GRPO\) has emerged as a scalable framework for critic-free policy learning, extending it to settings with explicit behavioral constraints remains underexplored. We introduce Constrained GRPO, a Lagrangian-based extension of GRPO for constrained policy optimization. Constraints are specified via indicator cost functions, enabling direct optimization of violation rates through a Lagrangian relaxation. We show that a naive multi-component treatment in advantage estimation can break constrained learning: mismatched component-wise standard deviations distort the relative importance of the different objective terms, which in turn corrupts the Lagrangian signal and prevents meaningful constraint enforcement. We formally derive this effect to motivate our scalarized advantage construction that preserves the intended trade-off between reward and constraint terms. Experiments in a toy gridworld confirm the predicted optimization pathology and demonstrate that scalarizing advantages restores stable constraint control. In addition, we evaluate Constrained GRPO on robotics tasks, where it improves constraint satisfaction while increasing task success, establishing a simple and effective recipe for constrained policy optimization in embodied AI domains that increasingly rely on large multimodal foundation models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
