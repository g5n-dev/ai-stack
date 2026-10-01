---
title: "Ranking-Aware Prompt Optimization for Multimodal Clinical Diagnosis"
date: 2026-10-01T13:53:37+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c69cd8f75ddf9d5a6edca5ea553a2927eedc38ade2ee4c417eeaba00971a99da"
source_payload_sha256: "sha256:034b6453e83fed340948245a4949263cf003902195387b3f5a6000ad30bd43c3"
observation_id: obs_056f5eda779dfe99bf00b3f503100750e79de873277faa3330b40b19a2401518
event_id: evt_43f012647a4066f31ba761afcf8a1a7b0d528c55f4e2ace453ff3decc46077f4
revision_id: rev_4db958d3fdc9bab3bad45f0ed8b493d0051066f9dbaaf19993637f9e5d600014
source_published_at: 2026-09-30T17:59:56Z
first_seen_at: 2026-10-01T06:03:14Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.40361v1
parent_observation_id: null
last_seen_at: 2026-10-01T05:50:49.396058Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.40361v1](http://arxiv.org/abs/2609.40361v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Tian Xia、Minghao Liu、Yiqing Liang 等

## 来源摘要/节选

> Multimodal large language models (MLLMs) are rapidly advancing clinical diagnosis, yet their adaptation pipelines remain anchored to accuracy-based objectives. Clinical data are heavily class-imbalanced: a constant-majority predictor can score above 90% accuracy while being clinically useless. We therefore evaluate and optimize for AUROC, a threshold-free score that ranks positives above negatives and is invariant to class balance. We focus on prompt optimization in MLLMs. Reflective methods such as GEPA use a binary scores matrix with one row per evaluation instance and one column per candidate prompt; cells record per-instance correctness, so the column average is accuracy and drives candidate selection. We introduce pair-level Pareto prompt evolution (Ranking-PE), which replaces each correctness row with a pairwise-ordering row over (positive, negative) instance pairs: the cell is 1 if the candidate scores the positive higher than the paired negative. The column average then equals empirical AUROC (by the Wilcoxon-Mann-Whitney identity). We apply this swap at all three layers the prompt evolution search reads from - the scores matrix that decides Pareto dominance, the per-example feedback to the reflection LM, and final candidate selection - at no extra model calls and with no surrogate loss. Across three diseases on MIMIC, accuracy-based prompt evolution can degrade ranking; Ranking-PE reverses this, beating the accuracy-based recipe by +5.8 AUROC pp on fine-tuned Qwen3-VL-8B and +16.2 pp on MedGemma-4B. Ablations examine each design component and show that a medical-grade visual backbone - via vision-encoder-tuned SFT or medical pretraining - is a prerequisite that prompt search cannot replace - our recipe extends reflective prompt evolution from text-only data to multimodal clinical decision-making.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。