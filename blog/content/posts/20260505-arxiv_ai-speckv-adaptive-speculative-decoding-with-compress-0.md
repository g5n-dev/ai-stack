---
title: 'SpecKV: Adaptive Speculative Decoding with Compression-Aware Gamma Selection'
date: 2026-05-05 23:13:55+08:00
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
external_url: https://arxiv.org/abs/2605.02888v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:091ae2668a20c14ae0407d4bffb19cb67bee07f86383566427d1a877ddc95c36
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:29:31.582048Z'
source_capture_sha256: sha256:49b9ffe5c949206285d2a50048b61e62639d0b9c74662c8d359b3a33fbdd14c3
source_capture_chars_original: 1500
source_publication_excerpt_chars: 1500
observation_id: obs_29a9eccf3a766ac2a9f9e0bf40b96aabb6eef9ac95948d94592a34bbac36f5ba
revision_id: rev_c881a85dcc16179ba6b9046a83193f1cbb9e143b4a945fafa2f035191ab9d169
event_id: evt_dcca64f1f8f564da0094e52b32fbe5a71f5bfff9307b9306657484d7a81c7cad
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.02888v1](<https://arxiv.org/abs/2605.02888v1>)
- **作者**: Shikhar Shukla
- **分类**: cs.LG
- **论文时间**: 2026-05-04T17:55:05Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.02888v1.pdf](<https://arxiv.org/pdf/2605.02888v1.pdf>)

## 来源摘要/节选

> Speculative decoding accelerates large language model \(LLM\) inference by using a small draft model to propose candidate tokens that a larger target model verifies. A critical hyperparameter in this process is the speculation length~$γ$, which determines how many tokens the draft model proposes per step. Nearly all existing systems use a fixed~$γ$ \(typically~4\), yet empirical evidence suggests that the optimal value varies across task types and, crucially, depends on the compression level applied to the target model. In this paper, we present \\textbf\{SpecKV\}, a lightweight adaptive controller that selects~$γ$ per speculation step using signals extracted from the draft model itself. We profile speculative decoding across 4~task categories, 4~speculation lengths, and 3~compression levels \(FP16, INT8, NF4\), collecting 5,112 step-level records with per-step acceptance rates, draft entropy, and draft confidence. We demonstrate that the optimal~$γ$ shifts across compression regimes and that draft model confidence and entropy are strong predictors of acceptance rate \(correlation~$\\approx 0.56$\). SpecKV uses a small MLP trained on these signals to maximize expected tokens per speculation step, achieving a 56.0\\% improvement over the fixed-$γ$=4 baseline with only 0.34\\,ms overhead per decision \($&lt;$0.5\\% of step time\). The improvement is statistically significant \($p &lt; 0.001$, paired bootstrap test\). We release all profiling data, trained models, and notebooks as open-source artifacts.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
