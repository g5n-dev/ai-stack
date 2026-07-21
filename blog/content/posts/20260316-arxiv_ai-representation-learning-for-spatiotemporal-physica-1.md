---
title: Representation Learning for Spatiotemporal Physical Systems
date: 2026-03-16 23:16:09+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.13227v1
aliases:
- /posts/20260317-arxiv_ai-representation-learning-for-spatiotemporal-physica-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:092c6446bc06e31aa5b389ddc927529fe4bd7be27319b4d2d606667918042fdc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
captured_at: '2026-07-18T04:28:19.053555Z'
source_capture_sha256: sha256:43545c2adb4ddd1b083579f959b2aa089cd929d26dcb526af008bfb0502ccee7
source_capture_chars_original: 1232
source_publication_excerpt_chars: 1232
observation_id: obs_db85e44616e2adf6ed182eb790184f2787b2dba442db5a925a48dae8b4ae9d45
revision_id: rev_cd38813cc5bf43fa19f06b42774948d053299e046dff2ff83bf78fcb48dd7406
event_id: evt_8765f862174b4bcc5f431f11cd57e0150d2aae483e3d8fae705197e8feea83bd
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.13227v1](<https://arxiv.org/abs/2603.13227v1>)
- **作者**: Helen Qu, Rudy Morel, Michael McCabe, Alberto Bietti, François Lanusse, Shirley Ho, Yann LeCun
- **分类**: cs.LG
- **论文时间**: 2026-03-13T17:59:51Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.13227v1.pdf](<https://arxiv.org/pdf/2603.13227v1.pdf>)

## 来源摘要/节选

> Machine learning approaches to spatiotemporal physical systems have primarily focused on next-frame prediction, with the goal of learning an accurate emulator for the system's evolution in time. However, these emulators are computationally expensive to train and are subject to performance pitfalls, such as compounding errors during autoregressive rollout. In this work, we take a different perspective and look at scientific tasks further downstream of predicting the next frame, such as estimation of a system's governing physical parameters. Accuracy on these tasks offers a uniquely quantifiable glimpse into the physical relevance of the representations of these models. We evaluate the effectiveness of general-purpose self-supervised methods in learning physics-grounded representations that are useful for downstream scientific tasks. Surprisingly, we find that not all methods designed for physical modeling outperform generic self-supervised learning methods on these tasks, and methods that learn in the latent space \(e.g., joint embedding predictive architectures, or JEPAs\) outperform those optimizing pixel-level prediction objectives. Code is available at https://github.com/helenqu/physical-representation-learning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
