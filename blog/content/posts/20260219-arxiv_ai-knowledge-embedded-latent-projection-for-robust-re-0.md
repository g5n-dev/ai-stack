---
title: Knowledge-Embedded Latent Projection for Robust Representation Learning
date: 2026-02-19 22:55:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.16709v1
aliases:
- /posts/20260220-arxiv_ai-knowledge-embedded-latent-projection-for-robust-re-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7556c2f3cd298377a0d2dbdcc59793ca618a39a5cfaff486afbcfadd7c05c92e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:16:00.196393Z'
source_capture_sha256: sha256:bdaef1a0825917a101d6a169f9b329f911dc1ece140a682beee442dd83033b0c
source_capture_chars_original: 1534
source_publication_excerpt_chars: 1534
observation_id: obs_968b58332c28b78a1cc83e5be25873ff4ecb88de215efcf5fedcdcc5423bb861
revision_id: rev_81ba1aa56910d951785fbbf8fea8d95d027d498c8809309ca73a36ef31253d77
event_id: evt_262d8cdeb92bce938f2f9af12bdd94fa57ec918e1e6c3721f4fa1adccf1a6f5c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.16709v1](<https://arxiv.org/abs/2602.16709v1>)
- **作者**: Weijing Tang, Ming Yuan, Zongqi Xia, Tianxi Cai
- **分类**: cs.LG
- **论文时间**: 2026-02-18T18:58:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.16709v1.pdf](<https://arxiv.org/pdf/2602.16709v1.pdf>)

## 来源摘要/节选

> Latent space models are widely used for analyzing high-dimensional discrete data matrices, such as patient-feature matrices in electronic health records \(EHRs\), by capturing complex dependence structures through low-dimensional embeddings. However, estimation becomes challenging in the imbalanced regime, where one matrix dimension is much larger than the other. In EHR applications, cohort sizes are often limited by disease prevalence or data availability, whereas the feature space remains extremely large due to the breadth of medical coding system. Motivated by the increasing availability of external semantic embeddings, such as pre-trained embeddings of clinical concepts in EHRs, we propose a knowledge-embedded latent projection model that leverages semantic side information to regularize representation learning. Specifically, we model column embeddings as smooth functions of semantic embeddings via a mapping in a reproducing kernel Hilbert space. We develop a computationally efficient two-step estimation procedure that combines semantically guided subspace construction via kernel principal component analysis with scalable projected gradient descent. We establish estimation error bounds that characterize the trade-off between statistical error and approximation error induced by the kernel projection. Furthermore, we provide local convergence guarantees for our non-convex optimization procedure. Extensive simulation studies and a real-world EHR application demonstrate the effectiveness of the proposed method.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
