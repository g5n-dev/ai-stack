---
title: 'Teaching Models to Teach Themselves: Reasoning at the Edge of Learnability'
date: 2026-01-27 23:10:51+08:00
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
external_url: https://arxiv.org/abs/2601.18778v1
aliases:
- /posts/20260128-arxiv_ai-teaching-models-to-teach-themselves-reasoning-at-t-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:143ae46f0d8023e92869edb679e82352f2ebc9c26429fe5e971356b2e6c5efb5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:09:18.936370Z'
source_capture_sha256: sha256:2a80e7d3d51a67d00a06d9b7938186da55649cacb4774089a9733a5a5cedb57b
source_capture_chars_original: 1618
source_publication_excerpt_chars: 1618
observation_id: obs_2990ecbde249b8cbc9ce66d6c35d247f99edb00acdb3e07acbe4ba3fa79c7a09
revision_id: rev_e6e65cb6c48911bdc8b95bf3b90baede35e5367f5bbbeb39069a4e43a8f15ad8
event_id: evt_95994deede71b8599de070493ab1a5039562280bc9219e9964363956ec75243e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-27T11:03:30Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.18778v1](<https://arxiv.org/abs/2601.18778v1>)
- **作者**: Shobhita Sundaram, John Quan, Ariel Kwiatkowski, Kartik Ahuja, Yann Ollivier, Julia Kempe
- **分类**: cs.LG
- **论文时间**: 2026-01-26T18:46:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.18778v1.pdf](<https://arxiv.org/pdf/2601.18778v1.pdf>)

## 来源摘要/节选

> Can a model learn to escape its own learning plateau? Reinforcement learning methods for finetuning large reasoning models stall on datasets with low initial success rates, and thus little training signal. We investigate a fundamental question: Can a pretrained LLM leverage latent knowledge to generate an automated curriculum for problems it cannot solve? To explore this, we design SOAR: A self-improvement framework designed to surface these pedagogical signals through meta-RL. A teacher copy of the model proposes synthetic problems for a student copy, and is rewarded with its improvement on a small subset of hard problems. Critically, SOAR grounds the curriculum in measured student progress rather than intrinsic proxy rewards. Our study on the hardest subsets of mathematical benchmarks \(0/128 success\) reveals three core findings. First, we show that it is possible to realize bi-level meta-RL that unlocks learning under sparse, binary rewards by sharpening a latent capacity of pretrained models to generate useful stepping stones. Second, grounded rewards outperform intrinsic reward schemes used in prior LLM self-play, reliably avoiding the instability and diversity collapse modes they typically exhibit. Third, analyzing the generated questions reveals that structural quality and well-posedness are more critical for learning progress than solution correctness. Our results suggest that the ability to generate useful stepping stones does not require the preexisting ability to actually solve the hard problems, paving a principled path to escape reasoning plateaus without additional curated data.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
