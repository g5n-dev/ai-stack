---
title: 'Assigning Confidence: K-partition Ensembles'
date: 2026-02-23 22:40:51+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.18435v1
aliases:
- /posts/20260224-arxiv_ai-assigning-confidence-k-partition-ensembles-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:29aacd60a78a9fd57b1b3402b0209993919d401d41dc68ef90267a6b9b4ee2e1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:16:23.555947Z'
source_capture_sha256: sha256:a52a6709ccd670bf15cba153a39f98cff2193f1180f060e658613f070f68318c
source_capture_chars_original: 1362
source_publication_excerpt_chars: 1362
observation_id: obs_ca0551211e2fa1309d78637094c6eaf3520ee9ab17d744c7f64e6e4e0d7d3eb8
revision_id: rev_6a7a4cad27ec9d92c17b8c2bfe4fbed47c3b1eb6a48f39e39c807875554bb1da
event_id: evt_cf8e6d77c21aa19f9be6c674e1a15bd0037f49d5033a71a597e4a0a1a840cf1d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.18435v1](<https://arxiv.org/abs/2602.18435v1>)
- **作者**: Aggelos Semoglou, John Pavlopoulos
- **分类**: cs.LG
- **论文时间**: 2026-02-20T18:59:53Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.18435v1.pdf](<https://arxiv.org/pdf/2602.18435v1.pdf>)

## 来源摘要/节选

> Clustering is widely used for unsupervised structure discovery, yet it offers limited insight into how reliable each individual assignment is. Diagnostics, such as convergence behavior or objective values, may reflect global quality, but they do not indicate whether particular instances are assigned confidently, especially for initialization-sensitive algorithms like k-means. This assignment-level instability can undermine both accuracy and robustness. Ensemble approaches improve global consistency by aggregating multiple runs, but they typically lack tools for quantifying pointwise confidence in a way that combines cross-run agreement with geometric support from the learned cluster structure. We introduce CAKE \(Confidence in Assignments via K-partition Ensembles\), a framework that evaluates each point using two complementary statistics computed over a clustering ensemble: assignment stability and consistency of local geometric fit. These are combined into a single, interpretable score in \[0,1\]. Our theoretical analysis shows that CAKE remains effective under noise and separates stable from unstable points. Experiments on synthetic and real-world datasets indicate that CAKE effectively highlights ambiguous points and stable core members, providing a confidence ranking that can guide filtering or prioritization to improve clustering quality.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
