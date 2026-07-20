---
title: A Scalable Measure of Loss Landscape Curvature for Analyzing the Training Dynamics
  of LLMs
date: 2026-01-26 22:15:20+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16979v1
aliases:
- /posts/20260127-arxiv_ai-a-scalable-measure-of-loss-landscape-curvature-for-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:43f65b9f5d263bca0e656d64dd1a119d137cf4d55e15356311b31101c8e6d6c3
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
captured_at: '2026-07-18T04:08:56.487166Z'
source_capture_sha256: sha256:bec34245e38e1b80bc9fd5b76a6d230e60e36a6be5bf7939e59faef06a3f8e40
source_capture_chars_original: 1520
source_publication_excerpt_chars: 1520
observation_id: obs_cdc143c9b4005d859a36f26494a91459f8c2b546193944503ce16f04142f450a
revision_id: rev_cf939260a850bae711ea437f947cab705b9212656688fecf434b286e2033b049
event_id: evt_0ae238b5fbac5c5525f18d901a504583a2bcea95fe8ad5e64d2648bb5d533a53
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16979v1](<https://arxiv.org/abs/2601.16979v1>)
- **作者**: Dayal Singh Kalra, Jean-Christophe Gagnon-Audet, Andrey Gromov, Ishita Mediratta, Kelvin Niu, Alexander H Miller, Michael Shvartsman
- **分类**: cs.LG
- **论文时间**: 2026-01-23T18:59:40Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16979v1.pdf](<https://arxiv.org/pdf/2601.16979v1.pdf>)

## 来源摘要/节选

> Understanding the curvature evolution of the loss landscape is fundamental to analyzing the training dynamics of neural networks. The most commonly studied measure, Hessian sharpness \($λ\_\{\\max\}^H$\) -- the largest eigenvalue of the loss Hessian -- determines local training stability and interacts with the learning rate throughout training. Despite its significance in analyzing training dynamics, direct measurement of Hessian sharpness remains prohibitive for Large Language Models \(LLMs\) due to high computational cost. We analyze $\\textit\{critical sharpness\}$ \($λ\_c$\), a computationally efficient measure requiring fewer than $10$ forward passes given the update direction $Δ\\mathbfθ$. Critically, this measure captures well-documented Hessian sharpness phenomena, including progressive sharpening and Edge of Stability. Using this measure, we provide the first demonstration of these sharpness phenomena at scale, up to $7$B parameters, spanning both pre-training and mid-training of OLMo-2 models. We further introduce $\\textit\{relative critical sharpness\}$ \($λ\_c^\{1\\to 2\}$\), which quantifies the curvature of one loss landscape while optimizing another, to analyze the transition from pre-training to fine-tuning and guide data mixing strategies. Critical sharpness provides practitioners with a practical tool for diagnosing curvature dynamics and informing data composition choices at scale. More broadly, our work shows that scalable curvature measures can provide actionable insights for large-scale training.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
