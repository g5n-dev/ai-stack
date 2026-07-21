---
title: 'JUCAL: Jointly Calibrating Aleatoric and Epistemic Uncertainty in Classification
  Tasks'
date: 2026-02-24 23:13:49+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.20153v1
aliases:
- /posts/20260225-arxiv_ai-jucal-jointly-calibrating-aleatoric-and-epistemic--2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bb36712b7640c1b4163ffc71b62e3b268f5b0c5cb6fd5c131a41dd6c2d4a4164
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
captured_at: '2026-07-18T04:16:34.952314Z'
source_capture_sha256: sha256:97045fd90232fce042304038ee5f0b406915903fef6d350fe94abe22b45b8326
source_capture_chars_original: 1865
source_publication_excerpt_chars: 1865
observation_id: obs_59ade1a5c81565a23ceeed3bd2f40546ff0d20e00e0b8907dacfd5af6c12588b
revision_id: rev_2315bf29d9970605c9df588318c1f7e64bc338be0aa4d2b467c0bcf21f7c59a0
event_id: evt_1f20df5624fcf0457c21216d04d99c569b3adffe8634af76083f34718eb74ba1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-24T06:21:29Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.20153v1](<https://arxiv.org/abs/2602.20153v1>)
- **作者**: Jakob Heiss, Sören Lambrecht, Jakob Weissteiner, Hanna Wutte, Žan Žurič, Josef Teichmann, Bin Yu
- **分类**: stat.ML
- **论文时间**: 2026-02-23T18:59:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.20153v1.pdf](<https://arxiv.org/pdf/2602.20153v1.pdf>)

## 来源摘要/节选

> We study post-calibration uncertainty for trained ensembles of classifiers. Specifically, we consider both aleatoric \(label noise\) and epistemic \(model\) uncertainty. Among the most popular and widely used calibration methods in classification are temperature scaling \(i.e., pool-then-calibrate\) and conformal methods. However, the main shortcoming of these calibration methods is that they do not balance the proportion of aleatoric and epistemic uncertainty. Not balancing these uncertainties can severely misrepresent predictive uncertainty, leading to overconfident predictions in some input regions while being underconfident in others. To address this shortcoming, we present a simple but powerful calibration algorithm Joint Uncertainty Calibration \(JUCAL\) that jointly calibrates aleatoric and epistemic uncertainty. JUCAL jointly calibrates two constants to weight and scale epistemic and aleatoric uncertainties by optimizing the negative log-likelihood \(NLL\) on the validation/calibration dataset. JUCAL can be applied to any trained ensemble of classifiers \(e.g., transformers, CNNs, or tree-based methods\), with minimal computational overhead, without requiring access to the models' internal parameters. We experimentally evaluate JUCAL on various text classification tasks, for ensembles of varying sizes and with different ensembling strategies. Our experiments show that JUCAL significantly outperforms SOTA calibration methods across all considered classification tasks, reducing NLL and predictive set size by up to 15% and 20%, respectively. Interestingly, even applying JUCAL to an ensemble of size 5 can outperform temperature-scaled ensembles of size up to 50 in terms of NLL and predictive set size, resulting in up to 10 times smaller inference costs. Thus, we propose JUCAL as a new go-to method for calibrating ensembles in classification.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
