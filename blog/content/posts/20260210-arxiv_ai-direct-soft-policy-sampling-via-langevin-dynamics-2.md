---
title: Direct Soft-Policy Sampling via Langevin Dynamics
date: 2026-02-10 03:34:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.07873v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:42abda9d4c494d21ddf163104290f1fea8ef69a7f02fbc5afb14c4c0ef6ef755
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
captured_at: '2026-07-18T04:14:24.737190Z'
source_capture_sha256: sha256:f94f41f82724df52edea5d5a8d0439c99988254ff6d6fc31aae59089175e12be
source_capture_chars_original: 1463
source_publication_excerpt_chars: 1463
observation_id: obs_3dd752501e84134249cefc4871e196a4b9cf7eac60e335cfdf43abfd78e3f4d2
revision_id: rev_48b061a9aee30654e5cbb2267902ae77a7971c8e64e97fd871b75d877875e290
event_id: evt_5a4fd2b80e32664f5516a07b6ddf1ddb61ce3d346c98619c5bbd969485129e61
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-10T04:25:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.07873v1](<https://arxiv.org/abs/2602.07873v1>)
- **作者**: Donghyeon Ki, Hee-Jun Ahn, Kyungyoon Kim, Byung-Jun Lee
- **分类**: cs.LG
- **论文时间**: 2026-02-08T09:01:54Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.07873v1.pdf](<https://arxiv.org/pdf/2602.07873v1.pdf>)

## 来源摘要/节选

> Soft policies in reinforcement learning define policies as Boltzmann distributions over state-action value functions, providing a principled mechanism for balancing exploration and exploitation. However, realizing such soft policies in practice remains challenging. Existing approaches either depend on parametric policies with limited expressivity or employ diffusion-based policies whose intractable likelihoods hinder reliable entropy estimation in soft policy objectives. We address this challenge by directly realizing soft-policy sampling via Langevin dynamics driven by the action gradient of the Q-function. This perspective leads to Langevin Q-Learning \(LQL\), which samples actions from the target Boltzmann distribution without explicitly parameterizing the policy. However, directly applying Langevin dynamics suffers from slow mixing in high-dimensional and non-convex Q-landscapes, limiting its practical effectiveness. To overcome this, we propose Noise-Conditioned Langevin Q-Learning \(NC-LQL\), which integrates multi-scale noise perturbations into the value function. NC-LQL learns a noise-conditioned Q-function that induces a sequence of progressively smoothed value landscapes, enabling sampling to transition from global exploration to precise mode refinement. On OpenAI Gym MuJoCo benchmarks, NC-LQL achieves competitive performance compared to state-of-the-art diffusion-based methods, providing a simple yet powerful solution for online RL.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
