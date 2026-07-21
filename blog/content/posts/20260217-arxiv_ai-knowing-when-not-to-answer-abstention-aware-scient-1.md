---
title: 'Knowing When Not to Answer: Abstention-Aware Scientific Reasoning'
date: 2026-02-17 03:10:02+08:00
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
external_url: https://arxiv.org/abs/2602.14189v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b218c360b6552456506f2cefbdb65f09f9a621da8ee05b61acef5897f91608e1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
captured_at: '2026-07-18T04:15:37.655804Z'
source_capture_sha256: sha256:218e015bc10ccae006fc8c605ce6384ddbad8e4460d0ffadbddddf9f4b4bc22a
source_capture_chars_original: 1681
source_publication_excerpt_chars: 1681
observation_id: obs_b16557520cc68cb695c8506b7ad2d8b6d637ac338526d6d2842518f645793c08
revision_id: rev_85106d7cd7c9cf78545f91d4c4d3b0c29ef8bdcba092522dc9de1646f3624e1f
event_id: evt_b27cac4c7772e597623d09bee2defba8c63f4c08518222c682dc0fa1ce757145
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-17T04:06:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.14189v1](<https://arxiv.org/abs/2602.14189v1>)
- **作者**: Samir Abdaljalil, Erchin Serpedin, Hasan Kurban
- **分类**: cs.CL
- **论文时间**: 2026-02-15T15:29:43Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.14189v1.pdf](<https://arxiv.org/pdf/2602.14189v1.pdf>)

## 来源摘要/节选

> Large language models are increasingly used to answer and verify scientific claims, yet existing evaluations typically assume that a model must always produce a definitive answer. In scientific settings, however, unsupported or uncertain conclusions can be more harmful than abstaining. We study this problem through an abstention-aware verification framework that decomposes scientific claims into minimal conditions, audits each condition against available evidence using natural language inference \(NLI\), and selectively decides whether to support, refute, or abstain. We evaluate this framework across two complementary scientific benchmarks: SciFact and PubMedQA, covering both closed-book and open-domain evidence settings. Experiments are conducted with six diverse language models, including encoder-decoder, open-weight chat models, and proprietary APIs. Across all benchmarks and models, we observe that raw accuracy varies only modestly across architectures, while abstention plays a critical role in controlling error. In particular, confidence-based abstention substantially reduces risk at moderate coverage levels, even when absolute accuracy improvements are limited. Our results suggest that in scientific reasoning tasks, the primary challenge is not selecting a single best model, but rather determining when available evidence is sufficient to justify an answer. This work highlights abstention-aware evaluation as a practical and model-agnostic lens for assessing scientific reliability, and provides a unified experimental basis for future work on selective reasoning in scientific domains. Code is available at https://github.com/sabdaljalil2000/ai4science .

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
