---
title: Pseudo-Invertible Neural Networks
date: 2026-02-06 23:01:34+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06042v1
aliases:
- /posts/20260207-arxiv_ai-pseudo-invertible-neural-networks-1/
- /posts/20260208-arxiv_ai-pseudo-invertible-neural-networks-1/
- /posts/20260209-arxiv_ai-pseudo-invertible-neural-networks-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6360b1b58cbdebd0a09dd14c7e640fee1d2e755c9f7ede0d3750b7c86643a24c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 33
captured_at: '2026-07-18T04:11:12.826784Z'
source_capture_sha256: sha256:c13cced7ad992a3feef432b7d400b30355f140e2e9832db44ceb470bfd0ec6d1
source_capture_chars_original: 1412
source_publication_excerpt_chars: 1412
observation_id: obs_27d5d3f3f862aa908c8f8c9fc09536b386d2e3bbc06bf023af896cbec151e2e3
revision_id: rev_a1d164193ebb945fa8d3caa008c2c84545ae764dd4c49edc4e301e374aafb24a
event_id: evt_788e5a035015a73b14e0f6ddebad60e2f5eda0bf99a443dbad42415ab97e31d5
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-06T05:25:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06042v1](<https://arxiv.org/abs/2602.06042v1>)
- **作者**: Yamit Ehrlich, Nimrod Berman, Assaf Shocher
- **分类**: cs.LG
- **论文时间**: 2026-02-05T18:59:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06042v1.pdf](<https://arxiv.org/pdf/2602.06042v1.pdf>)

## 来源摘要/节选

> The Moore-Penrose Pseudo-inverse \(PInv\) serves as the fundamental solution for linear systems. In this paper, we propose a natural generalization of PInv to the nonlinear regime in general and to neural networks in particular. We introduce Surjective Pseudo-invertible Neural Networks \(SPNN\), a class of architectures explicitly designed to admit a tractable non-linear PInv. The proposed non-linear PInv and its implementation in SPNN satisfy fundamental geometric properties. One such property is null-space projection or "Back-Projection", $x' = x + A^\\dagger\(y-Ax\)$, which moves a sample $x$ to its closest consistent state $x'$ satisfying $Ax=y$. We formalize Non-Linear Back-Projection \(NLBP\), a method that guarantees the same consistency constraint for non-linear mappings $f\(x\)=y$ via our defined PInv. We leverage SPNNs to expand the scope of zero-shot inverse problems. Diffusion-based null-space projection has revolutionized zero-shot solving for linear inverse problems by exploiting closed-form back-projection. We extend this method to non-linear degradations. Here, "degradation" is broadly generalized to include any non-linear loss of information, spanning from optical distortions to semantic abstractions like classification. This approach enables zero-shot inversion of complex degradations and allows precise semantic control over generative outputs without retraining the diffusion prior.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
