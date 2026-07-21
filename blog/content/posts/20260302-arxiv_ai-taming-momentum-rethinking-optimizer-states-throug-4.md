---
title: 'Taming Momentum: Rethinking Optimizer States Through Low-Rank Approximation'
date: 2026-03-02 23:25:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24283v1
aliases:
- /posts/20260303-arxiv_ai-taming-momentum-rethinking-optimizer-states-throug-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8958cee23935cdc111f109e6151ef79b646b7f88ff3cd67b6cba85e8fccadcaa
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
captured_at: '2026-07-18T04:26:19.677155Z'
source_capture_sha256: sha256:8e5728584d561b0455781a3c84b62d96a2d26d27523652477129a3b955b2c479
source_capture_chars_original: 1585
source_publication_excerpt_chars: 1585
observation_id: obs_4d7697a780e712c6f9df2ad1779d12c755a5704a69a267af3bb8fad87002bbd9
revision_id: rev_0faebf8e45c979df5e9b0f3eb0d0cf628b5d628f2ee7367b522f11c060f5c892
event_id: evt_b1f0d51db94f6ab0f112b5391f5d0dd386c998c3fd8d1579d4274d8c3aedcb54
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-02T06:24:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24283v1](<https://arxiv.org/abs/2602.24283v1>)
- **作者**: Zhengbo Wang, Jian Liang, Ran He, Zilei Wang, Tieniu Tan
- **分类**: cs.LG
- **论文时间**: 2026-02-27T18:57:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24283v1.pdf](<https://arxiv.org/pdf/2602.24283v1.pdf>)

## 来源摘要/节选

> Modern optimizers like Adam and Muon are central to training large language models, but their reliance on first- and second-order momenta introduces significant memory overhead, which constrains scalability and computational efficiency. In this work, we reframe the exponential moving average \(EMA\) used in these momenta as the training of a linear regressor via online gradient flow. Building on this equivalence, we introduce LoRA-Pre, a novel low-rank optimizer designed for efficient pre-training. Specifically, LoRA-Pre reduces the optimizer's memory footprint by decomposing the full momentum matrix into a compact low-rank subspace within the online linear learner, thereby maintaining optimization performance while improving memory efficiency. We empirically validate LoRA-Pre's efficacy by pre-training models from the Llama architecture family, scaling from 60M to 1B parameters. LoRA-Pre achieves the highest performance across all model sizes. Notably, LoRA-Pre demonstrates remarkable rank efficiency, achieving comparable or superior results using only 1/8 the rank of baseline methods. Beyond pre-training, we evaluate LoRA-Pre's effectiveness in fine-tuning scenarios. With the same rank, LoRA-Pre consistently outperforms all efficient fine-tuning baselines. Specifically, compared to standard LoRA, LoRA-Pre achieves substantial improvements of 3.14 points on Llama-3.1-8B and 6.17 points on Llama-2-7B, validating our approach's effectiveness across both pre-training and fine-tuning paradigms. Our code is publicly available at https://github.com/mrflogs/LoRA-Pre.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
