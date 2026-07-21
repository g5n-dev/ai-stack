---
title: 'KAN-FIF: Spline-Parameterized Lightweight Physics-based Tropical Cyclone Estimation
  on Meteorological Satellite'
date: 2026-02-13 03:01:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12117v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:02f9121886278b510addb1bdf1bb527f592c8e2dff6d5e97d5fa88cdfdb9b6ff
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 111
captured_at: '2026-07-18T04:15:06.314161Z'
source_capture_sha256: sha256:d2f50e5eb55d5d5687c28cd03a845d227e8d714e033561f9208fada44c644ece
source_capture_chars_original: 1563
source_publication_excerpt_chars: 1563
observation_id: obs_22ec0a87c422368cf5a547fa4b376c3bd26e8a879e07e61e90721ff57847e69d
revision_id: rev_b9b532e9e1285963e80490d15ecd2ab78efcd2dac67d9689b273bc7a206051cd
event_id: evt_2d4b4e35c785f920ca82ffaadb826146df42f63ef84475544bac46c367d41f2d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12117v1](<https://arxiv.org/abs/2602.12117v1>)
- **作者**: Jiakang Shen, Qinghui Chen, Runtong Wang, Chenrui Xu, Jinglin Zhang, Cong Bai, Feng Zhang
- **分类**: cs.LG
- **论文时间**: 2026-02-12T16:07:39Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12117v1.pdf](<https://arxiv.org/pdf/2602.12117v1.pdf>)

## 来源摘要/节选

> Tropical cyclones \(TC\) are among the most destructive natural disasters, causing catastrophic damage to coastal regions through extreme winds, heavy rainfall, and storm surges. Timely monitoring of tropical cyclones is crucial for reducing loss of life and property, yet it is hindered by the computational inefficiency and high parameter counts of existing methods on resource-constrained edge devices. Current physics-guided models suffer from linear feature interactions that fail to capture high-order polynomial relationships between TC attributes, leading to inflated model sizes and hardware incompatibility. To overcome these challenges, this study introduces the Kolmogorov-Arnold Network-based Feature Interaction Framework \(KAN-FIF\), a lightweight multimodal architecture that integrates MLP and CNN layers with spline-parameterized KAN layers. For Maximum Sustained Wind \(MSW\) prediction, experiments demonstrate that the KAN-FIF framework achieves a $94.8\\%$ reduction in parameters \(0.99MB vs 19MB\) and $68.7\\%$ faster inference per sample \(2.3ms vs 7.35ms\) compared to baseline model Phy-CoCo, while maintaining superior accuracy with $32.5\\%$ lower MAE. The offline deployment experiment of the FY-4 series meteorological satellite processor on the Qingyun-1000 development board achieved a 14.41ms per-sample inference latency with the KAN-FIF framework, demonstrating promising feasibility for operational TC monitoring and extending deployability to edge-device AI applications. The code is released at https://github.com/Jinglin-Zhang/KAN-FIF.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
