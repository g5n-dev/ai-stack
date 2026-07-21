---
title: 'Matching Features, Not Tokens: Energy-Based Fine-Tuning of Language Models'
date: 2026-03-13 23:24:24+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.12248v1
aliases:
- /posts/20260314-arxiv_ai-matching-features-not-tokens-energy-based-fine-tun-4/
- /posts/20260315-arxiv_ai-matching-features-not-tokens-energy-based-fine-tun-4/
- /posts/20260316-arxiv_ai-matching-features-not-tokens-energy-based-fine-tun-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6c044b82b068d98e9786a2e1dbc23793a689565595d15832bd2a07dd133786f3
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:28:07.966279Z'
source_capture_sha256: sha256:4e6043277a42db058db3143634f86b6a96bc2b64bfa718ccf0c8272b0cfeb133
source_capture_chars_original: 1085
source_publication_excerpt_chars: 1085
observation_id: obs_b57605ec2adde2ffc1d9ad9241bfe33988908035fe32b6f104edfcb29828fcca
revision_id: rev_fcda2dc097307bf90b8d00a668ff9ffa324e0d65667004a810395092af78ca85
event_id: evt_a4fa6105913add908422a9be2f8f3ebaad823efb454959d16b88548da36e3a89
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12248v1](<https://arxiv.org/abs/2603.12248v1>)
- **作者**: Samy Jelassi, Mujin Kwun, Rosie Zhao, Yuanzhi Li, Nicolo Fusi, Yilun Du, Sham M. Kakade, Carles Domingo-Enrich
- **分类**: cs.LG
- **论文时间**: 2026-03-12T17:57:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12248v1.pdf](<https://arxiv.org/pdf/2603.12248v1.pdf>)

## 来源摘要/节选

> Cross-entropy \(CE\) training provides dense and scalable supervision for language models, but it optimizes next-token prediction under teacher forcing rather than sequence-level behavior under model rollouts. We introduce a feature-matching objective for language-model fine-tuning that targets sequence-level statistics of the completion distribution, providing dense semantic feedback without requiring a task-specific verifier or preference model. To optimize this objective efficiently, we propose energy-based fine-tuning \(EBFT\), which uses strided block-parallel sampling to generate multiple rollouts from nested prefixes concurrently, batches feature extraction over these rollouts, and uses the resulting embeddings to perform an on-policy policy-gradient update. We present a theoretical perspective connecting EBFT to KL-regularized feature-matching and energy-based modeling. Empirically, across Q&amp;A coding, unstructured coding, and translation, EBFT matches RLVR and outperforms SFT on downstream accuracy while achieving a lower validation cross-entropy than both methods.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
