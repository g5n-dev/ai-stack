---
title: Discovering Hidden Gems in Model Repositories
date: 2026-01-30 23:03:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.22157v1
aliases:
- /posts/20260131-arxiv_ai-discovering-hidden-gems-in-model-repositories-1/
- /posts/20260201-arxiv_ai-discovering-hidden-gems-in-model-repositories-1/
- /posts/20260202-arxiv_ai-discovering-hidden-gems-in-model-repositories-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:30cd095908984c702ce9fb2747050513bd87d6f50d5c443f76418f41ef338909
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 45
captured_at: '2026-07-18T04:09:48.978849Z'
source_capture_sha256: sha256:2f0ddc10cd33a7fcbefa61930fba941090cb5254ad673c64bd94675c1064d75e
source_capture_chars_original: 1049
source_publication_excerpt_chars: 1049
observation_id: obs_a977b4d0ae13e5edfed4037a174498660d50d409d9457b2f1c6313ec159d4973
revision_id: rev_157ff0c5b04ec1d21bef9b1dd6e550332200509a5a7bf28c4877623744f80e07
event_id: evt_ef07cf32ea13069462131d8e3eb97bfbe54e1f07a27ef8e54b8cef1712f3bbe2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-30T05:20:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22157v1](<https://arxiv.org/abs/2601.22157v1>)
- **作者**: Jonathan Kahana, Eliahu Horwitz, Yedid Hoshen
- **分类**: cs.LG
- **论文时间**: 2026-01-29T18:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22157v1.pdf](<https://arxiv.org/pdf/2601.22157v1.pdf>)

## 来源摘要/节选

> Public repositories host millions of fine-tuned models, yet community usage remains disproportionately concentrated on a small number of foundation checkpoints. We investigate whether this concentration reflects efficient market selection or if superior models are systematically overlooked. Through an extensive evaluation of over 2,000 models, we show the prevalence of "hidden gems", unpopular fine-tunes that significantly outperform their popular counterparts. Notably, within the Llama-3.1-8B family, we find rarely downloaded checkpoints that improve math performance from 83.2% to 96.0% without increasing inference costs. However, discovering these models through exhaustive evaluation of every uploaded model is computationally infeasible. We therefore formulate model discovery as a Multi-Armed Bandit problem and accelerate the Sequential Halving search algorithm by using shared query sets and aggressive elimination schedules. Our method retrieves top models with as few as 50 queries per candidate, accelerating discovery by over 50x.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
