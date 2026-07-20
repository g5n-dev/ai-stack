---
title: 'PEFT-Arena: Understanding Parameter-Efficient Finetuning from a Stability-Plasticity
  Perspective'
date: 2026-05-28 23:45:22+08:00
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
external_url: https://arxiv.org/abs/2605.28819v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f422157d8504316f594f82978999d6d6530dd5a797d7de929269bbfc7483b38d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:29:43.284780Z'
source_capture_sha256: sha256:6316eb422ff01da06724627012cb7d01dcb8484b9f474c98b7c1e23d39c7dec1
source_capture_chars_original: 1260
source_publication_excerpt_chars: 1260
observation_id: obs_9b8b67c71f447b6cb1fda0536f85f29a60e125204604221b76807b7185530115
revision_id: rev_1a7dd21d8152c50e1022c54b1db2d3c4ce81e3cf96b851c77d35a19c91877980
event_id: evt_2ccf76183e4830d0da2bb75539d30091a203ef349401fbb39c34cfccd232dffe
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.28819v1](<https://arxiv.org/abs/2605.28819v1>)
- **作者**: Yangyi Huang, Ruotian Peng, Zeju Qiu, Jiale Kang, Yandong Wen, Bernhard Schölkopf, Weiyang Liu
- **分类**: cs.LG
- **论文时间**: 2026-05-27T17:59:51Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.28819v1.pdf](<https://arxiv.org/pdf/2605.28819v1.pdf>)

## 来源摘要/节选

> Parameter-efficient finetuning \(PEFT\) has become the standard approach for adapting large language models, yet evaluations largely emphasize downstream accuracy while overlooking the retention of pretrained capabilities. We argue that PEFT should be assessed through the stability-plasticity dilemma: the trade-off between target-task adaptation and resistance to forgetting. We introduce PEFT-Arena, a benchmark that jointly measures downstream performance and general capability retention. Across methods, we find distinct stability-plasticity profiles; under comparable parameter budgets, orthogonal finetuning achieves the most favorable Pareto frontier. To explain these differences, we analyze PEFT updates from two geometric perspectives. In weight space, spectral analysis reveals how parameterizations interact with the pretrained singular-value structure. In activation space, retention metrics show whether finetuning preserves or distorts general-capability representations, with forgetting linked to non-isometric representation distortion. Finally, an analysis shows that final SFT checkpoints often overshoot a better target-retention operating point. Inspired by this, we present case studies of a post-hoc improvement with path-wise rewinding.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
