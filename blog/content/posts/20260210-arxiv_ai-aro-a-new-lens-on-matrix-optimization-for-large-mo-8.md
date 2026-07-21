---
title: 'ARO: A New Lens On Matrix Optimization For Large Models'
date: 2026-02-10 22:46:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.09006v1
aliases:
- /posts/20260211-arxiv_ai-aro-a-new-lens-on-matrix-optimization-for-large-mo-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:40a56c00cc0476f0d736aa321898fbeaeabe603fae4acaff8aa12055cc63d0b9
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
captured_at: '2026-07-18T04:14:24.737190Z'
source_capture_sha256: sha256:08a84a9e6ac71fe366cbe8cda5f457b6c4206357cc92a510a903060cc311b573
source_capture_chars_original: 1464
source_publication_excerpt_chars: 1464
observation_id: obs_5c9e31c7b018b8c21eb61e8bdadba3561a68b180302c3a13f72349e45a75dfda
revision_id: rev_a80f4de637beb4a85fa4aa5c873eef9996570febdb300c9809955e0237e2100b
event_id: evt_aa3720f4ccb748510156fa6864f650cb6075834abb9322d6ab49ac83ec63cc0c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09006v1](<https://arxiv.org/abs/2602.09006v1>)
- **作者**: Wenbo Gong, Javier Zazo, Qijun Luo, Puqian Wang, James Hensman, Chao Ma
- **分类**: cs.LG
- **论文时间**: 2026-02-09T18:51:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09006v1.pdf](<https://arxiv.org/pdf/2602.09006v1.pdf>)

## 来源摘要/节选

> Matrix-based optimizers have attracted growing interest for improving LLM training efficiency, with significant progress centered on orthogonalization/whitening based methods. While yielding substantial performance gains, a fundamental question arises: can we develop new paradigms beyond orthogonalization, pushing the efficiency frontier further? We present \\textbf\{Adaptively Rotated Optimization \(ARO\}, a new matrix optimization framework that treats gradient rotation as a first class design principle. ARO accelerates LLM training by performing normed steepest descent in a rotated coordinate system, where the rotation is determined by a novel norm-informed policy. This perspective yields update rules that go beyond existing orthogonalization and whitening optimizers, improving sample efficiency in practice. To make comparisons reliable, we propose a rigorously controlled benchmarking protocol that reduces confounding and bias. Under this protocol, ARO consistently outperforms AdamW \(by 1.3 $\\sim$1.35$\\times$\) and orthogonalization methods \(by 1.1$\\sim$1.15$\\times$\) in LLM pretraining at up to 8B activated parameters, and up to $8\\times$ overtrain budget, without evidence of diminishing returns. Finally, we discuss how ARO can be reformulated as a symmetry-aware optimizer grounded in rotational symmetries of residual streams, motivating advanced designs that enable computationally efficient exploitation of cross-layer/cross module couplings.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
