---
title: 'When to Align, When to Predict: A Phase Diagram for Multimodal Learning'
date: 2026-06-10 22:19:43+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.11190v1
aliases:
- /posts/20260611-arxiv_ai-when-to-align-when-to-predict-a-phase-diagram-for--0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:982b6e89d049c91f31ec57073fef801bf837bfdc3161b4231b37506c12ff5f98
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:30:02.047374Z'
source_capture_sha256: sha256:472bcf9e3ca76827265fd27dc083090aff7faaf6bef26b9affab24e34dd7851f
source_capture_chars_original: 1767
source_publication_excerpt_chars: 1767
observation_id: obs_32d3d574932a0f91d8434bcc4134fa7d0683f9fe05a822c61951d90419aacd96
revision_id: rev_4a5991ef298f7f61b84361bf3ee2dd03cc1964e4b05996b3c31e27cbe4ccef7e
event_id: evt_725fa3480655cdc5a7bfbf6daa44c529ca96c63bbbfe590d527e0c7089f74d4f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.11190v1](<https://arxiv.org/abs/2606.11190v1>)
- **作者**: Ilay Kamai, Hugues Van Assel, Aviv Regev, Hagai B. Perets, Randall Balestriero
- **分类**: cs.LG
- **论文时间**: 2026-06-09T17:59:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.11190v1.pdf](<https://arxiv.org/pdf/2606.11190v1.pdf>)

## 来源摘要/节选

> Cross-modal alignment \(CA\) and cross-modal prediction \(CP\) are the dominant paradigms for multimodal representation learning, yet there is no systematic understanding of when each succeeds, when each fails, and when cross-modal training helps at all -- a gap that leaves practitioners, especially in scientific domains like biomedicine or astrophysics, with heterogeneous instruments and multiple levels of organization and measurement, unable to diagnose why standard methods underperform the best single modality. We develop a unified linear framework that addresses both questions. Under a spiked signal-plus-noise model with structured cross-modal nuisance correlation, we derive separation ratios for both objectives that expose complementary failure modes: alignment whitens each modality and fails when nuisance is strongly correlated across views; prediction encodes whatever is cross-predictable through a one-sided whitening, with recovery governed by source-modality quality. The resulting phase diagram partitions multimodal problems into four regimes: Both, CA only, CP only, and Neither. We present a data-driven procedure to locate real-world datasets in this diagram using a small labeled subsample, identifying the preferred objective and prediction direction before any cross-modal training. Experiments on synthetic data, stereo-vision benchmarks, image-caption pairs, and real astrophysical data validate the predictions in the nonlinear regime, including the Neither regime where cross-modal training is actively harmful. Our framework lets practitioners diagnose their multimodal problem and choose the right objective before committing to training. Code to reproduce the results is available at https://github.com/IlayMalinyak/mm\_align\_vs\_pred.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
