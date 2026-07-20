---
title: 'FISMO: Fisher-Structured Momentum-Orthogonalized Optimizer'
date: 2026-01-30 03:54:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.21750v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:5de76e2dace64d9bb614706c2ac6a8fe4ba0f6be8c18ee3f71b44cf8de8b6c28
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
captured_at: '2026-07-18T04:09:52.752345Z'
source_capture_sha256: sha256:7934d75743a0c7ac86a54f815e9c9fd67f0a9c0c1816fe8d8c138a840e19b241
source_capture_chars_original: 1490
source_publication_excerpt_chars: 1490
observation_id: obs_1cfee884c9e7ac3b737a8842a984b50941d161f1aa2ead641de178dd2947319a
revision_id: rev_8824088570ea1598d31037c3b7c1fd59cc7ab92999f80659269bda960f0cce0a
event_id: evt_5a68269be3fb9ec101dcf2278ed0cb140a9b93308efca53db710c5dcc5b2441f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21750v1](<https://arxiv.org/abs/2601.21750v1>)
- **作者**: Chenrui Xu, Wenjing Yan, Ying-Jun Angela Zhang
- **分类**: cs.LG
- **论文时间**: 2026-01-29T14:05:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21750v1.pdf](<https://arxiv.org/pdf/2601.21750v1.pdf>)

## 来源摘要/节选

> Training large-scale neural networks requires solving nonconvex optimization where the choice of optimizer fundamentally determines both convergence behavior and computational efficiency. While adaptive methods like Adam have long dominated practice, the recently proposed Muon optimizer achieves superior performance through orthogonalized momentum updates that enforce isotropic geometry with uniform singular values. However, this strict isotropy discards potentially valuable curvature information encoded in gradient spectra, motivating optimization methods that balance geometric structure with adaptivity. We introduce FISMO \(Fisher-Structured Momentum-Orthogonalized\) optimizer, which generalizes isotropic updates to incorporate anisotropic curvature information through Fisher information geometry. By reformulating the optimizer update as a trust-region problem constrained by a Kronecker-factored Fisher metric, FISMO achieves structured preconditioning that adapts to local loss landscape geometry while maintaining computational tractability. We establish convergence guarantees for FISMO in stochastic nonconvex settings, proving an $\\mathcal\{O\}\(1/\\sqrt\{T\}\)$ rate for the expected squared gradient norm with explicit characterization of variance reduction through mini-batching. Empirical evaluation on image classification and language modeling benchmarks demonstrates that FISMO achieves superior training efficiency and final performance compared to established baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
