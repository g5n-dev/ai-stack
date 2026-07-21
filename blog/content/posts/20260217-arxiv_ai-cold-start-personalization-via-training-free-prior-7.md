---
title: Cold-Start Personalization via Training-Free Priors from Structured World Models
date: 2026-02-17 22:35:47+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15012v1
aliases:
- /posts/20260218-arxiv_ai-cold-start-personalization-via-training-free-prior-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:34eeb2e8142213c26a03f49ce2a5ca0d09733c2b8046c6b2bcc8ea2232d4320c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:15:33.978565Z'
source_capture_sha256: sha256:4f98aea56fd9cafd0e0e2ecc06caa5a731a7abef75ccdb7410b5d0ac84d88b41
source_capture_chars_original: 1689
source_publication_excerpt_chars: 1689
observation_id: obs_90c05c96b732ff104c883a1f137d8ffd5db68c086128c27a92427820757238da
revision_id: rev_ec10538b0e416607ab9e51463aa926f1feb1fb909d8addf9958bd02e16952cc9
event_id: evt_0507b4a1f061c59b98795642f856a0d8fd5029b1e02bdb03fc653f80bf5a147c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-17T09:52:08Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15012v1](<https://arxiv.org/abs/2602.15012v1>)
- **作者**: Avinandan Bose, Shuyue Stella Li, Faeze Brahman, Pang Wei Koh, Simon Shaolei Du, Yulia Tsvetkov, Maryam Fazel, Lin Xiao, Asli Celikyilmaz
- **分类**: cs.CL
- **论文时间**: 2026-02-16T18:52:13Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15012v1.pdf](<https://arxiv.org/pdf/2602.15012v1.pdf>)

## 来源摘要/节选

> Cold-start personalization requires inferring user preferences through interaction when no user-specific historical data is available. The core challenge is a routing problem: each task admits dozens of preference dimensions, yet individual users care about only a few, and which ones matter depends on who is asking. With a limited question budget, asking without structure will miss the dimensions that matter. Reinforcement learning is the natural formulation, but in multi-turn settings its terminal reward fails to exploit the factored, per-criterion structure of preference data, and in practice learned policies collapse to static question sequences that ignore user responses. We propose decomposing cold-start elicitation into offline structure learning and online Bayesian inference. Pep \(Preference Elicitation with Priors\) learns a structured world model of preference correlations offline from complete profiles, then performs training-free Bayesian inference online to select informative questions and predict complete preference profiles, including dimensions never asked about. The framework is modular across downstream solvers and requires only simple belief models. Across medical, mathematical, social, and commonsense reasoning, Pep achieves 80.8% alignment between generated responses and users' stated preferences versus 68.5% for RL, with 3-5x fewer interactions. When two users give different answers to the same question, Pep changes its follow-up 39-62% of the time versus 0-28% for RL. It does so with ~10K parameters versus 8B for RL, showing that the bottleneck in cold-start elicitation is the capability to exploit the factored structure of preference data.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
