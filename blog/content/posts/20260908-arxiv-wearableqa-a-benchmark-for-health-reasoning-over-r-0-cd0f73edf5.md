---
title: "WearableQA: A Benchmark for Health Reasoning over Real-World Wearable Data"
date: 2026-09-08T06:53:36+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d9eb330458784019104c558451f595836c147a0a9a164800d38f9cd12856ced4"
source_payload_sha256: "sha256:1fbf0d73f0b4c8f9369f96819e4c541e045faa0df64680d0c459d981fa3ce51c"
observation_id: obs_cd0f73edf5a8fc191bf037b130c0c6fe6fb1d9b2b4fec0dbd8b2d345daa014ea
event_id: evt_036bfcc609ebb0a67f07c91c9a7ce0c20a2aa303bc23b65a0562098a87fd214d
revision_id: rev_55a806c77753b745cec33c4d0812ad031818c16febdd2574f0456873704e4ec0
source_published_at: 2026-09-04T17:52:37Z
first_seen_at: 2026-09-07T22:50:55.041857Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.05405v1
parent_observation_id: null
last_seen_at: 2026-09-07T22:50:55.041857Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.05405v1](http://arxiv.org/abs/2609.05405v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Ji Soo Lee、Xilun Chen、Pierce Chuang 等

## 来源摘要/节选

> Recent advances in wearable sensing enable continuous monitoring of physiological and behavioral signals, yet existing benchmarks rarely evaluate whether AI systems can reason over a real user's longitudinal wearable record. We introduce WearableQA, a benchmark comprising 4,084 10-option multiple-choice questions constructed from the wearable time series, blood biomarkers, and demographics of 200 real users, each with up to 500 days of daily measurements. WearableQA preserves authentic wearable distributions that include device noise and inter-individual variability. To evaluate distinct reasoning capabilities, we introduce 16 question types organized along two complementary axes: data versus health reasoning, which distinguishes computation over longitudinal measurements from physiological interpretation; and single- versus cross-signal reasoning, which separates reasoning about individual signals from the integration of multiple signals. To construct reliable questions at scale, we adopt a dual-grounding framework that combines literature-grounded physiological findings with statistically validated population-grounded physiological patterns. This enables the capture of meaningful relationships observed in real-world wearable data. Evaluation of 14 proprietary and open-source LLMs demonstrates that WearableQA effectively differentiates model capabilities, with performance ranging from 19.6% to 72.9% against a 10% chance baseline. Moreover, WearableQA remains far from solved: most models achieve accuracies below 60%. Overall, WearableQA provides a realistic and diagnostic benchmark for evaluating LLM reasoning over real-world wearable data.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。