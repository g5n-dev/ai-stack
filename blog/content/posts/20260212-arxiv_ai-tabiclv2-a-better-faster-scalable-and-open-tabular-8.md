---
title: 'TabICLv2: A better, faster, scalable, and open tabular foundation model'
date: 2026-02-12 23:40:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11139v1
aliases:
- /posts/20260213-arxiv_ai-tabiclv2-a-better-faster-scalable-and-open-tabular-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:20c31781686b0024c54277374cec280ccd2d8d7589948b7f79f82c7187a213d7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:15:02.573604Z'
source_capture_sha256: sha256:33c769e4451f1caa6e7873c01af116ec758def36aacc80677e6fba4f13ddf8fb
source_capture_chars_original: 1302
source_publication_excerpt_chars: 1302
observation_id: obs_1427a260c9604320522dc22b512fef7a476aba1816c2e66b35ac131b87e17c4a
revision_id: rev_41ae2e12ce0efe8ebaaabbf8d1e6582a4ac7304ab86ab2e2985ba7479c0842cc
event_id: evt_6e7bcf389e64705b2b67035a5825499087aa7a94fdbf910e515952e8c4df6bb5
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11139v1](<https://arxiv.org/abs/2602.11139v1>)
- **作者**: Jingang Qu, David Holzmüller, Gaël Varoquaux, Marine Le Morvan
- **分类**: cs.LG
- **论文时间**: 2026-02-11T18:51:02Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11139v1.pdf](<https://arxiv.org/pdf/2602.11139v1.pdf>)

## 来源摘要/节选

> Tabular foundation models, such as TabPFNv2 and TabICL, have recently dethroned gradient-boosted trees at the top of predictive benchmarks, demonstrating the value of in-context learning for tabular data. We introduce TabICLv2, a new state-of-the-art foundation model for regression and classification built on three pillars: \(1\) a novel synthetic data generation engine designed for high pretraining diversity; \(2\) various architectural innovations, including a new scalable softmax in attention improving generalization to larger datasets without prohibitive long-sequence pretraining; and \(3\) optimized pretraining protocols, notably replacing AdamW with the Muon optimizer. On the TabArena and TALENT benchmarks, TabICLv2 without any tuning surpasses the performance of the current state of the art, RealTabPFN-2.5 \(hyperparameter-tuned, ensembled, and fine-tuned on real data\). With only moderate pretraining compute, TabICLv2 generalizes effectively to million-scale datasets under 50GB GPU memory while being markedly faster than RealTabPFN-2.5. We provide extensive ablation studies to quantify these contributions and commit to open research by first releasing inference code and model weights at https://github.com/soda-inria/tabicl, with synthetic data engine and pretraining code to follow.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
