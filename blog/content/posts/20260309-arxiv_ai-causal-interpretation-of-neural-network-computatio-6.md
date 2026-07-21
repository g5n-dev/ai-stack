---
title: Causal Interpretation of Neural Network Computations with Contribution Decomposition
date: 2026-03-09 21:48:42+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.06557v1
aliases:
- /posts/20260310-arxiv_ai-causal-interpretation-of-neural-network-computatio-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:987bf817afec83cf0250923c7411925c438929e18e60471fe39e660ed3724c2c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
captured_at: '2026-07-18T04:27:20.159062Z'
source_capture_sha256: sha256:495c3e7d0405ab6a90a6104c82c1e5a23d3c8f3406750157627701a2415f4b12
source_capture_chars_original: 1642
source_publication_excerpt_chars: 1642
observation_id: obs_f0038f4aeb07c3dbc6b2fa2fe913c54cba2ae2f1a0cfd93ac508312f02ebbf14
revision_id: rev_10ebddba1238d6d11eb25a57c2b3b185a8b4847775c40fe9c6ee64e785235a87
event_id: evt_3b8a698e2c98e9e21829781bf94e576b37703c0665d656db13b3f0a94ccb789d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T03:53:15Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.06557v1](<https://arxiv.org/abs/2603.06557v1>)
- **作者**: Joshua Brendan Melander, Zaki Alaoui, Shenghua Liu, Surya Ganguli, Stephen A. Baccus
- **分类**: cs.LG
- **论文时间**: 2026-03-06T18:46:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.06557v1.pdf](<https://arxiv.org/pdf/2603.06557v1.pdf>)

## 来源摘要/节选

> Understanding how neural networks transform inputs into outputs is crucial for interpreting and manipulating their behavior. Most existing approaches analyze internal representations by identifying hidden-layer activation patterns correlated with human-interpretable concepts. Here we take a direct approach to examine how hidden neurons act to drive network outputs. We introduce CODEC \(Contribution Decomposition\), a method that uses sparse autoencoders to decompose network behavior into sparse motifs of hidden-neuron contributions, revealing causal processes that cannot be determined by analyzing activations alone. Applying CODEC to benchmark image-classification networks, we find that contributions grow in sparsity and dimensionality across layers and, unexpectedly, that they progressively decorrelate positive and negative effects on network outputs. We further show that decomposing contributions into sparse modes enables greater control and interpretation of intermediate layers, supporting both causal manipulations of network output and human-interpretable visualizations of distinct image components that combine to drive that output. Finally, by analyzing state-of-the-art models of neural activity in the vertebrate retina, we demonstrate that CODEC uncovers combinatorial actions of model interneurons and identifies the sources of dynamic receptive fields. Overall, CODEC provides a rich and interpretable framework for understanding how nonlinear computations evolve across hierarchical layers, establishing contribution modes as an informative unit of analysis for mechanistic insights into artificial neural networks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
