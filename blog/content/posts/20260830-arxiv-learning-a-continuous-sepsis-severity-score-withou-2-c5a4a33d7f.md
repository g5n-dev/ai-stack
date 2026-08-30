---
title: "Learning a Continuous Sepsis Severity Score Without Hour-by-Hour Supervision: A Two-Site Retrospective Study"
date: 2026-08-30T20:56:26+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0a777de505ed08a96faa2cd3669181f19bf29cf20d11583bc5f2f28514cbc4a5"
source_payload_sha256: "sha256:f2b3981c81c5c75edec29e08912b7e766262c65522785e8b42bbfcbc03196ad8"
observation_id: obs_c5a4a33d7fada8322197ce7cefb3ebfb9cffe1b1de78e7a8546dd2e4fd7e9f1f
event_id: evt_3101e35feba9e99bbe5d271ba0db84cca2e4f34bfd96ab1c483f62e1f507d398
revision_id: rev_f24652eedc9390120f131caa4f6e88b6f02ed8df09cc4fb0e32c5baf537148f9
source_published_at: 2026-08-27T17:46:21Z
first_seen_at: 2026-08-30T13:06:05Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.27421v1
parent_observation_id: null
last_seen_at: 2026-08-30T12:53:27.105747Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27421v1](http://arxiv.org/abs/2608.27421v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Kevin Zhu、Ryan Zhang、Baraa Abed 等

## 来源摘要/节选

> Currently used sepsis severity indices rely on fixed variables and weights established decades ago, which are coarsely discretized and calibrated to a cohort that no longer reflects contemporary critical care. No alternative learned directly from patient trajectories is in routine use. We conducted a retrospective two-cohort study on a total of 29,116 and 7,691 adult patients meeting Sepsis-3 criteria from two hospital systems in Massachusetts and Georgie, respectively.
> We developed a sepsis index using 43 routinely charted variables over a 72-hour treatment window. Unlike previous studies, we use mortality as a treatment-level ranking signal rather than a per-state target, allowing credit to be redistributed non-uniformly across timesteps. Evaluation was done on a permanent 20% test holdout, using clinical vignettes and Spearman correlation. Uncertainty intervals were obtained by bootstrap resampling of whole patients. Under this ranking scheme, non-survivors scored 1.19-1.64 points higher than survivors on a 0-10 scale within all strata of baseline SOFA-2, with similar results stratifying within lactate, mean arterial pressure (MAP), and creatinine. Within-patient change in the index correlated with change in lactate (Spearman rho = 0.39; n = 1,854). Similar, weaker correlations were found for MAP and creatinine. On a cohort level, cross-institutional agreement measured by Spearman correlation between models trained on different sites, were 70-77% of same-site correlation. External within-patient correlations were 0.54 and 0.59 against ceilings of 0.92 and 0.90. Our index also correlated with established indices, while null controls stayed near zero.
> Our index demonstrated hourly prognostic information that meaningfully separates patient outcomes and is consistent with clinical expectation, indicating potential as a decision support tool complementing clinical judgement.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。