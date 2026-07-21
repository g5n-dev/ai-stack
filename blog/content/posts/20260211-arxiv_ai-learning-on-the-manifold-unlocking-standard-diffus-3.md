---
title: 'Learning on the Manifold: Unlocking Standard Diffusion Transformers with Representation
  Encoders'
date: 2026-02-11 23:34:28+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10099v1
aliases:
- /posts/20260212-arxiv_ai-learning-on-the-manifold-unlocking-standard-diffus-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:73700d193fcd5df2a2a4b76e7e3eb4bf541e1bb48cf27ab14e2f9cb1e631ac82
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:14:39.893621Z'
source_capture_sha256: sha256:2b5e73313ed49d3410504dba519bcf2d645f2afe2e7b014f2a2645d41b8772f4
source_capture_chars_original: 1152
source_publication_excerpt_chars: 1152
observation_id: obs_fa8b8ec20fc995861c456bc5313946c3e665027bafc103f696ed8a7d7a9791ad
revision_id: rev_8622ea71fc3bf4dfb57d06e23c0353ebd3a5e2cb27374ab5360d8aeab1a5b892
event_id: evt_d422ba40292171dc4dd25b295d85033233ec6e044a6fbe76203175785fed12b2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10099v1](<https://arxiv.org/abs/2602.10099v1>)
- **作者**: Amandeep Kumar, Vishal M. Patel
- **分类**: cs.LG
- **论文时间**: 2026-02-10T18:58:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10099v1.pdf](<https://arxiv.org/pdf/2602.10099v1.pdf>)

## 来源摘要/节选

> Leveraging representation encoders for generative modeling offers a path for efficient, high-fidelity synthesis. However, standard diffusion transformers fail to converge on these representations directly. While recent work attributes this to a capacity bottleneck proposing computationally expensive width scaling of diffusion transformers we demonstrate that the failure is fundamentally geometric. We identify Geometric Interference as the root cause: standard Euclidean flow matching forces probability paths through the low-density interior of the hyperspherical feature space of representation encoders, rather than following the manifold surface. To resolve this, we propose Riemannian Flow Matching with Jacobi Regularization \(RJF\). By constraining the generative process to the manifold geodesics and correcting for curvature-induced error propagation, RJF enables standard Diffusion Transformer architectures to converge without width scaling. Our method RJF enables the standard DiT-B architecture \(131M parameters\) to converge effectively, achieving an FID of 3.37 where prior methods fail to converge. Code: https://github.com/amandpkr/RJF

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
