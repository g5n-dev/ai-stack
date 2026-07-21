---
title: 'From Core to Detail: Unsupervised Disentanglement with Entropy-Ordered Flows'
date: 2026-02-09 23:42:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06940v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:62a2e5b5bd7a5119f35acfa3b56ab2b4874684b26d02f110b9ad75e3377ee111
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:11:23.963527Z'
source_capture_sha256: sha256:2db479eaca0ec75993a31a935866edd7e3a4188ae913ccd7324ed38e4a8f4f00
source_capture_chars_original: 1083
source_publication_excerpt_chars: 1083
observation_id: obs_26842b1d8348d23742d78f79d75b53c763c7512ab3936ad45338b5af26303f17
revision_id: rev_45d0af3991b781a4d0978779ffbf2d4d599e931d1eb15341c8529e41fd58e138
event_id: evt_f3886376e5fa2472fbcf47b8a43afaf7074016300742ea489999ede35398e871
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06940v1](<https://arxiv.org/abs/2602.06940v1>)
- **作者**: Daniel Galperin, Ullrich Köthe
- **分类**: cs.LG
- **论文时间**: 2026-02-06T18:41:03Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06940v1.pdf](<https://arxiv.org/pdf/2602.06940v1.pdf>)

## 来源摘要/节选

> Learning unsupervised representations that are both semantically meaningful and stable across runs remains a central challenge in modern representation learning. We introduce entropy-ordered flows \(EOFlows\), a normalizing-flow framework that orders latent dimensions by their explained entropy, analogously to PCA's explained variance. This ordering enables adaptive injective flows: after training, one may retain only the top C latent variables to form a compact core representation while the remaining variables capture fine-grained detail and noise, with C chosen flexibly at inference time rather than fixed during training. EOFlows build on insights from Independent Mechanism Analysis, Principal Component Flows and Manifold Entropic Metrics. We combine likelihood-based training with local Jacobian regularization and noise augmentation into a method that scales well to high-dimensional data such as images. Experiments on the CelebA dataset show that our method uncovers a rich set of semantically interpretable features, allowing for high compression and strong denoising.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
