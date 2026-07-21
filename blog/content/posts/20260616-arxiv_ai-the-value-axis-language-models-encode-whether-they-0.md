---
title: 'The Value Axis: Language Models Encode Whether They''re on the Right Track'
date: 2026-06-16 22:35:39+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.17056v1
aliases:
- /posts/20260617-arxiv_ai-the-value-axis-language-models-encode-whether-they-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:5f7838c249f545fda004d70157c62431e0ab9eea053c18395753091b9945acc8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
captured_at: '2026-07-18T04:30:09.568344Z'
source_capture_sha256: sha256:ea7fb6bb2b2388b240d7d07e0e26e48f8e471a7924663109bd30f9c257d2fe34
source_capture_chars_original: 1227
source_publication_excerpt_chars: 1227
observation_id: obs_a11f22ad34b92c172e1c4a021e4c93be05060b992819e7d986e6531390cf57a6
revision_id: rev_ac17aad497d76f1f541006c17f0900fd3882f718d01499d677f1a49f729a1c53
event_id: evt_df4ba6c0f48349ab8434383e1d3170f6189d720c0d171338b4df3391ae0bf1ee
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-16T05:18:54Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.17056v1](<https://arxiv.org/abs/2606.17056v1>)
- **作者**: Nick Jiang, Isaac Kauvar, Jack Lindsey
- **分类**: cs.CL
- **论文时间**: 2026-06-15T17:59:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.17056v1.pdf](<https://arxiv.org/pdf/2606.17056v1.pdf>)

## 来源摘要/节选

> We investigate whether language models internally track the value of their current trajectory, defined as the likelihood that their ongoing strategy will achieve their goals. Using synthetic, in-context reinforcement learning data, we construct a "value" axis for Qwen3-8B. We find that activations along this axis distinguish between high vs. low verbalized confidence, rollouts without and with backtracking, and correct vs. corrupted code. Steering towards high value causally suppresses self-correction and reduces explanatory verbosity, while steering towards low value induces backtracking and exploration. We demonstrate that direct preference optimization \(DPO\) can increase the internal value of rewarded behaviors \(e.g. use a certain word\), causing the model to act more confidently after exhibiting them. Finally, we apply the value axis to study in-the-wild settings. For example, we find that Qwen assigns low value to politically sensitive chat queries after post-training and that supervised fine-tuning increases internal confidence within the training domain. Our results suggest that language models linearly encode an estimate of expected goal success that modulates their confidence in pursuing a direction.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
