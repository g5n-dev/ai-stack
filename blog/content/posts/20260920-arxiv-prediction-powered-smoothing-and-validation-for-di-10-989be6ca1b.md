---
title: "Prediction-Powered Smoothing and Validation for Disaggregated AI Evaluation"
date: 2026-09-20T02:05:14+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "stat.ML", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9ba7fed0e5af286a1189048b5f89c614d7c86c37a6787c2202f0c08609a4bfa8"
source_payload_sha256: "sha256:01a358278d7cb6f56084c599086b2f921ec1268287a14c0527ef8fe57b3667eb"
observation_id: obs_989be6ca1bd187d7233f3ed1d0d6da84ac92f416ebd2855e369248e8c291ca35
event_id: evt_62879ec5975917845cbef422d32fa4843c4e05e826299624228276e825de6f92
revision_id: rev_8da2e04d881b64d57c6abce6ce1a14b34ccf948e454e0ac58bfcc7cf6504fa57
source_published_at: 2026-09-17T17:42:29Z
first_seen_at: 2026-09-19T18:16:18Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.20758v1
parent_observation_id: null
last_seen_at: 2026-09-20T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20758v1](http://arxiv.org/abs/2609.20758v1)
- **发布域名**: arxiv.org
- **分类**: stat.ML
- **作者**: Sho Kawano、Zehang Richard Li、Paul A. Parker

## 来源摘要/节选

> Evaluating an AI system requires disaggregated assessment, as performance varies across domains such as benchmark task types or conversation types in deployed agents. Exhaustive testing is expensive, so evaluation rests on a sample of labeled units. We treat the evaluation set as a finite population and seek accurate point and interval estimates of each domain mean. Direct estimators, including prediction-powered inference (PPI), use only a domain's own labels and are imprecise where labels are few. Small area estimation addresses this problem, and we build on it to develop an integrated workflow for estimation and validation. For estimation, we propose prediction-powered smoothing (PP-S), a Bayesian model fit to each domain's prediction-powered estimate, with an extension that borrows strength across a reporting taxonomy (PP-TS). For validation, we derive a new, approximately unbiased design-based cross-validation score for choosing among direct and smoothed estimators. We study a curated benchmark with verifiable grading and deployed agent traffic graded by humans, each with every outcome observed. In both, the proposed estimators improve on the direct estimators in point and interval estimation, with near-nominal coverage. At the same sampling budget, our score selects as well as an independent validation sample does and estimates the selected estimator's error far more accurately.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。