---
title: Improved Regret Guarantees for Online Mirror Descent using a Portfolio of Mirror
  Maps
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
external_url: https://arxiv.org/abs/2602.13177v1
aliases:
- /posts/20260217-arxiv_ai-improved-regret-guarantees-for-online-mirror-desce-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c5f9d690676cfbae3175ba97db78d9fc7157f6ebd092b06a7ef319b1dcb197ae
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:15:26.440768Z'
source_capture_sha256: sha256:4a08dc3f874eaa8b626ae26eeebd237b9b2b275b4cb5cad6dc550090c3fd8a72
source_capture_chars_original: 1887
source_publication_excerpt_chars: 1887
observation_id: obs_8e991ae09078578aadf65a6baca3d6423cd9e953893bd42f58937b5998d78dea
revision_id: rev_9f3a91ade5089f19af439f3369147314b486898018b08f5bd4938ad313ca9f34
event_id: evt_f363d688e95223a3b479faea708cbc36d1d4e0e4eed57f91a015ce13fb451dec
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-16T23:12:02Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.13177v1](<https://arxiv.org/abs/2602.13177v1>)
- **作者**: Swati Gupta, Jai Moondra, Mohit Singh
- **分类**: math.OC
- **论文时间**: 2026-02-13T18:37:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.13177v1.pdf](<https://arxiv.org/pdf/2602.13177v1.pdf>)

## 来源摘要/节选

> OMD and its variants give a flexible framework for OCO where the performance depends crucially on the choice of the mirror map. While the geometries underlying OPGD and OEG, both special cases of OMD, are well understood, it remains a challenging open question on how to construct an optimal mirror map for any given constrained set and a general family of loss functions, e.g., sparse losses. Motivated by parameterizing a near-optimal set of mirror maps, we consider a simpler question: is it even possible to obtain polynomial gains in regret by using mirror maps for geometries that interpolate between $L\_1$ and $L\_2$, which may not be possible by restricting to only OEG \($L\_1$\) or OPGD \($L\_2$\). Our main result answers this question positively. We show that mirror maps based on block norms adapt better to the sparsity of loss functions, compared to previous $L\_p$ \(for $p \\in \[1, 2\]$\) interpolations. In particular, we construct a family of online convex optimization instances in $\\mathbb\{R\}^d$, where block norm-based mirror maps achieve a provable polynomial \(in $d$\) improvement in regret over OEG and OPGD for sparse loss functions. We then turn to the setting in which the sparsity level of the loss functions is unknown. In this case, the choice of geometry itself becomes an online decision problem. We first show that naively switching between OEG and OPGD can incur linear regret, highlighting the intrinsic difficulty of geometry selection. To overcome this issue, we propose a meta-algorithm based on multiplicative weights that dynamically selects among a family of uniform block norms. We show that this approach effectively tunes OMD to the sparsity of the losses, yielding adaptive regret guarantees. Overall, our results demonstrate that online mirror-map selection can significantly enhance the ability of OMD to exploit sparsity in online convex optimization.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
