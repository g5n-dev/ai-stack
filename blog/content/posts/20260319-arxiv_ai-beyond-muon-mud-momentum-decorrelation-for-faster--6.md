---
title: 'Beyond Muon: MUD (MomentUm Decorrelation) for Faster Transformer Training'
date: 2026-03-19 18:55:56+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.17970v1
aliases:
- /posts/20260320-arxiv_ai-beyond-muon-mud-momentum-decorrelation-for-faster--6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:90e0bb7fcfd8f6707fcf7bc17f3e5760ea3d6ebc44ff3f77e6dcda33f6d06c95
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
captured_at: '2026-07-18T04:28:45.482788Z'
source_capture_sha256: sha256:1d54426e23e139810f5d5e930b6fc988865efa9cc97cf39510d59c2406968607
source_capture_chars_original: 1343
source_publication_excerpt_chars: 1343
observation_id: obs_ea08aee9d98447ceb98b845e1bee5bc05a70d44b1f7f4aef9be8b97263adaea6
revision_id: rev_3918ac964e9b5cae07518eaa768e93b0d7fdbb52802f72e98e335b1ceee4aeb3
event_id: evt_fb0ded62b669cc5c628e3c25c36dc70532561362b26880591ce4a60ba70e8dfe
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.17970v1](<https://arxiv.org/abs/2603.17970v1>)
- **作者**: Ben S. Southworth, Stephen Thomas
- **分类**: cs.LG
- **论文时间**: 2026-03-18T17:37:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.17970v1.pdf](<https://arxiv.org/pdf/2603.17970v1.pdf>)

## 来源摘要/节选

> Orthogonalized-momentum optimizers such as Muon improve transformer training by approximately whitening/orthogonalizing matrix-valued momentum updates via a short polar-decomposition iteration. However, polar-factor approximations typically require multiple large matrix multiplications, and the resulting overhead can be substantial and hardware-dependent. We introduce MUD \(MomentUm Decorrelation\), a complementary whitening approach that replaces Muon's polar update with a triangular \(Cholesky-like\) whitening surrogate inspired by classical Gram--Schmidt and Gauss-Seidel ideas. We show that row-orthonormal matrices are fixed points of the MUD map, relate the inner step to symmetric Gauss-Seidel preconditioning of the Gram matrix, and prove quadratic local convergence near the fixed point. In terms of time-to-perplexity, MUD yields consistent 10-50\\% wall-clock improvements over tuned AdamW and Muon in time-to-perplexity, typically converging slightly slower per step than Muon but with substantially lower optimizer overhead -- relative to Muon, MUD improves peak tokens/s by roughly $1.3-2.6\\times$ across most settings and up to nearly $3\\times$ on GPT-2 large on an A100. We also demonstrate training a ESM-2 150M protein language model, where MUD matches Muon-level validation perplexity in significantly less wall-clock time.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
