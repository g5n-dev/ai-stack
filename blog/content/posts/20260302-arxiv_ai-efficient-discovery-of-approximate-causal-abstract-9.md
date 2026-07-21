---
title: Efficient Discovery of Approximate Causal Abstractions via Neural Mechanism
  Sparsification
date: 2026-03-02 23:25:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24266v1
aliases:
- /posts/20260303-arxiv_ai-efficient-discovery-of-approximate-causal-abstract-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d83f3ba9e3591dead7ae0b6959326ae853a0c639ab063ddccdccfe4cbc14e56b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
captured_at: '2026-07-18T04:26:12.126510Z'
source_capture_sha256: sha256:28695dcd16da141a4bbe9fd2dde0e98167f79a5f19503acc0f0437d75c4fff7b
source_capture_chars_original: 976
source_publication_excerpt_chars: 976
observation_id: obs_66d63df6e68e96ca2ccc4ee70f6dd6d71db41188b7782d4da92a7a5f765fd719
revision_id: rev_707dac58407840567005798fc84e0da32651d965ff1f08983ddfcd9846d2d0f7
event_id: evt_6f76c6ba91bb8b89e282ed62217cab6a74c18bce5248d06114d9d6b5912b16cb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24266v1](<https://arxiv.org/abs/2602.24266v1>)
- **作者**: Amir Asiaee
- **分类**: cs.LG
- **论文时间**: 2026-02-27T18:35:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24266v1.pdf](<https://arxiv.org/pdf/2602.24266v1.pdf>)

## 来源摘要/节选

> Neural networks are hypothesized to implement interpretable causal mechanisms, yet verifying this requires finding a causal abstraction -- a simpler, high-level Structural Causal Model \(SCM\) faithful to the network under interventions. Discovering such abstractions is hard: it typically demands brute-force interchange interventions or retraining. We reframe the problem by viewing structured pruning as a search over approximate abstractions. Treating a trained network as a deterministic SCM, we derive an Interventional Risk objective whose second-order expansion yields closed-form criteria for replacing units with constants or folding them into neighbors. Under uniform curvature, our score reduces to activation variance, recovering variance-based pruning as a special case while clarifying when it fails. The resulting procedure efficiently extracts sparse, intervention-faithful abstractions from pretrained networks, which we validate via interchange interventions.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
