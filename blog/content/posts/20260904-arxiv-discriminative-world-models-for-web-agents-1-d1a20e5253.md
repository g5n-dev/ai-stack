---
title: "Discriminative World Models for Web Agents"
date: 2026-09-04T02:40:59+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5a006e574906f0f50db54d52bc88da4498aad50fda89f93ae05dace9b4435781"
source_payload_sha256: "sha256:8703474cb4f577b307731cf1a986f76f800470fde625b6ca4b3569d30e74f903"
observation_id: obs_d1a20e5253c90dfb70b95c24fa13a2c67ca793bf716085ac93f46089089a46a7
event_id: evt_1c7427e610b1ad4015af45ff7b6b04f83bf88922e02c970d46b0f82c68528cb3
revision_id: rev_580dff0b07bd947a96174277acafbfdf114226723681cbd3f349dea7f423e56f
source_published_at: 2026-09-02T17:59:40Z
first_seen_at: 2026-09-03T18:38:14.535178Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 42
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.02885v1
parent_observation_id: null
last_seen_at: 2026-09-03T18:38:14.535178Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.02885v1](http://arxiv.org/abs/2609.02885v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Kelvin Li、Dhruv Pendharkar、Anish Pahilajani 等

## 来源摘要/节选

> Recent web agents use world models for test-time action selection by sampling candidate actions, predicting the resulting web states, and ranking them with a ranker model or a Process Reward Model (PRM). These world models are typically trained via supervised next-state prediction to generate fixed representations like HTML or AXTree snapshots. However, this objective is misaligned with the downstream ranker, which relies on predicted states being discriminative across candidates to accurately score them. To address this, we introduce predicted-state matching, a training objective where the predicted representation must distinguish the true resulting state from those reached by alternative actions. We train these models using a branching web-agent dataset derived from WebArena Go-Browse trajectories, where every decision point contains multiple alternative actions and their resulting states. Experiments on our held-out predicted-state matching benchmark show that our approach outperforms world models trained with supervised next-state prediction. We further show that our approach improves PRM-style action ranking on WebPRMBench compared with action-only PRMs and PRMs augmented with supervised-next-state world models. Finally, on WebArena-Lite, using our world model for test-time action selection improves end-to-end task success. Our project page is available at: https://dhruvpendharkar.github.io/dwm/.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。