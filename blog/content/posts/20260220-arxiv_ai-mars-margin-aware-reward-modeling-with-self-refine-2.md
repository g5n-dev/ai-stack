---
title: 'MARS: Margin-Aware Reward-Modeling with Self-Refinement'
date: 2026-02-20 22:59:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.17658v1
aliases:
- /posts/20260221-arxiv_ai-mars-margin-aware-reward-modeling-with-self-refine-2/
- /posts/20260222-arxiv_ai-mars-margin-aware-reward-modeling-with-self-refine-2/
- /posts/20260223-arxiv_ai-mars-margin-aware-reward-modeling-with-self-refine-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1e3891a8a875a569549c502adf884b02069c200cc1074a7e616bb3e4fc8a7b9e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
captured_at: '2026-07-18T04:16:04.060671Z'
source_capture_sha256: sha256:ece08b1533c938ba40ea3ba4d6263e5ddff00f662e9275bbbb49802c5c12829f
source_capture_chars_original: 1140
source_publication_excerpt_chars: 1140
observation_id: obs_1740812b961fbf3eaeffacee8c0bf552f219c29fe0a18306c8d30e39a20a2f2b
revision_id: rev_8a96b978c8e1eaeb93dd796c689737c56f02f8eef16b06ac2767776131110f5b
event_id: evt_806428fa30302bc7c7923f1a9a1cb00ee21db726a8b60e98adafd6a6e583d864
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-20T03:54:51Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.17658v1](<https://arxiv.org/abs/2602.17658v1>)
- **作者**: Payel Bhattacharjee, Osvaldo Simeone, Ravi Tandon
- **分类**: cs.LG
- **论文时间**: 2026-02-19T18:59:03Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.17658v1.pdf](<https://arxiv.org/pdf/2602.17658v1.pdf>)

## 来源摘要/节选

> Reward modeling is a core component of modern alignment pipelines including RLHF and RLAIF, underpinning policy optimization methods including PPO and TRPO. However, training reliable reward models relies heavily on human-labeled preference data, which is costly and limited, motivating the use of data augmentation. Existing augmentation approaches typically operate at the representation or semantic level and remain agnostic to the reward model's estimation difficulty. In this paper, we propose MARS, an adaptive, margin-aware augmentation and sampling strategy that explicitly targets ambiguous and failure modes of the reward model. Our proposed framework, MARS, concentrates augmentation on low-margin \(ambiguous\) preference pairs where the reward model is most uncertain, and iteratively refines the training distribution via hard-sample augmentation. We provide theoretical guarantees showing that this strategy increases the average curvature of the loss function hence enhance information and improves conditioning, along with empirical results demonstrating consistent gains over uniform augmentation for robust reward modeling.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
