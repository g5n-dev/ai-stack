---
title: 'From Data Statistics to Feature Geometry: How Correlations Shape Superposition'
date: 2026-03-11 22:41:14+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.09972v1
aliases:
- /posts/20260312-arxiv_ai-from-data-statistics-to-feature-geometry-how-corre-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ccc12c55f40dde330d11d26edb095a2ca76e1d71a9bc05797308ea0e1439cb5b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:27:42.897478Z'
source_capture_sha256: sha256:0935cf1469e2bb31fc5ace10eda323c0365edc01d05de44813ed61113d05368e
source_capture_chars_original: 1535
source_publication_excerpt_chars: 1535
observation_id: obs_9c87eddd6cb185ee7d355b12f9b7cc1d741f81239d111c91e08b0d53b4ddac09
revision_id: rev_f33ef0e75be66a964292eab3e55b298358a482298df260b9da31401ffda9f9d6
event_id: evt_d5606749d1a594b5ef5a90ecd68845289d7b9dc12d28bbf987febcfcc2c6d4ed
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.09972v1](<https://arxiv.org/abs/2603.09972v1>)
- **作者**: Lucas Prieto, Edward Stevinson, Melih Barsbey, Tolga Birdal, Pedro A. M. Mediano
- **分类**: cs.LG
- **论文时间**: 2026-03-10T17:59:02Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.09972v1.pdf](<https://arxiv.org/pdf/2603.09972v1.pdf>)

## 来源摘要/节选

> A central idea in mechanistic interpretability is that neural networks represent more features than they have dimensions, arranging them in superposition to form an over-complete basis. This framing has been influential, motivating dictionary learning approaches such as sparse autoencoders. However, superposition has mostly been studied in idealized settings where features are sparse and uncorrelated. In these settings, superposition is typically understood as introducing interference that must be minimized geometrically and filtered out by non-linearities such as ReLUs, yielding local structures like regular polytopes. We show that this account is incomplete for realistic data by introducing Bag-of-Words Superposition \(BOWS\), a controlled setting to encode binary bag-of-words representations of internet text in superposition. Using BOWS, we find that when features are correlated, interference can be constructive rather than just noise to be filtered out. This is achieved by arranging features according to their co-activation patterns, making interference between active features constructive, while still using ReLUs to avoid false positives. We show that this kind of arrangement is more prevalent in models trained with weight decay and naturally gives rise to semantic clusters and cyclical structures which have been observed in real language models yet were not explained by the standard picture of superposition. Code for this paper can be found at https://github.com/LucasPrietoAl/correlations-feature-geometry.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
