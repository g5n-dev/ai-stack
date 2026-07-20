---
title: 'Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning'
date: 2026-01-25 12:39:55+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16163v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:04a2108954538fe7d33b146ae58ad1cfb2ed5f755ebed3bcfdfd9b986d5ae56e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
captured_at: '2026-07-18T04:08:52.620209Z'
source_capture_sha256: sha256:90eb8f0078d6339f5b81011d547b410614eb07d493f4a8fd7947b084ebfb1cf1
source_capture_chars_original: 1894
source_publication_excerpt_chars: 1894
observation_id: obs_fce2b8074078e09e3debcdaacdd5357112a55b8b21a7b896043259c7b92530da
revision_id: rev_5d19e27acf91323b5eb11c8cb92738fd279241a2250ab05db4ad0939f73e7c43
event_id: evt_37e2545f5918592beea3aaf3afb5fd8cecf0d3fbda5195559bfbc87f6a70e46b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16163v1](<https://arxiv.org/abs/2601.16163v1>)
- **作者**: Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, Jinwei Gu
- **分类**: cs.AI
- **论文时间**: 2026-01-22T18:09:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16163v1.pdf](<https://arxiv.org/pdf/2601.16163v1.pdf>)

## 来源摘要/节选

> Recent video generation models demonstrate remarkable ability to capture complex physical interactions and scene evolution over time. To leverage their spatiotemporal priors, robotics works have adapted video models for policy learning but introduce complexity by requiring multiple stages of post-training and new architectural components for action generation. In this work, we introduce Cosmos Policy, a simple approach for adapting a large pretrained video model \(Cosmos-Predict2\) into an effective robot policy through a single stage of post-training on the robot demonstration data collected on the target platform, with no architectural modifications. Cosmos Policy learns to directly generate robot actions encoded as latent frames within the video model's latent diffusion process, harnessing the model's pretrained priors and core learning algorithm to capture complex action distributions. Additionally, Cosmos Policy generates future state images and values \(expected cumulative rewards\), which are similarly encoded as latent frames, enabling test-time planning of action trajectories with higher likelihood of success. In our evaluations, Cosmos Policy achieves state-of-the-art performance on the LIBERO and RoboCasa simulation benchmarks \(98.5% and 67.1% average success rates, respectively\) and the highest average score in challenging real-world bimanual manipulation tasks, outperforming strong diffusion policies trained from scratch, video model-based policies, and state-of-the-art vision-language-action models fine-tuned on the same robot demonstrations. Furthermore, given policy rollout data, Cosmos Policy can learn from experience to refine its world model and value function and leverage model-based planning to achieve even higher success rates in challenging tasks. We release code, models, and training data at https://research.nvidia.com/labs/dir/cosmos-policy/

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
