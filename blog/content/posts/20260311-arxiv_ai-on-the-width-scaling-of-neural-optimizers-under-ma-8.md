---
title: 'On the Width Scaling of Neural Optimizers Under Matrix Operator Norms I: Row/Column
  Normalization and Hyperparameter Transfer'
date: 2026-03-11 22:41:14+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 深度学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.09952v1
aliases:
- /posts/20260312-arxiv_ai-on-the-width-scaling-of-neural-optimizers-under-ma-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d5721f6f1c26a3879b846f7bdf6c143b46f1e6908ddb3aa6e006103507250ba1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 125
captured_at: '2026-07-18T04:27:47.713351Z'
source_capture_sha256: sha256:53886e19f05c1c0659efb921589d1323566e3a4776921fdc8c5d9f68a543f31f
source_capture_chars_original: 1861
source_publication_excerpt_chars: 1861
observation_id: obs_c35b1331e73700a32e733f13a4b8d6220971afb283339703fb36833ff2a1f8ea
revision_id: rev_22c6f369d266725c1f35fa26f75ee2e1be98bd35c8312d523c595ba8e6115616
event_id: evt_69b3279a28295f8f973c92b947460731dbaa55ccb560cc1280ca0005d9b24b7b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-11T04:17:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.09952v1](<https://arxiv.org/abs/2603.09952v1>)
- **作者**: Ruihan Xu, Jiajin Li, Yiping Lu
- **分类**: cs.LG
- **论文时间**: 2026-03-10T17:49:19Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.09952v1.pdf](<https://arxiv.org/pdf/2603.09952v1.pdf>)

## 来源摘要/节选

> A central question in modern deep learning is how to design optimizers whose behavior remains stable as the network width $w$ increases. We address this question by interpreting several widely used neural-network optimizers, including \\textrm\{AdamW\} and \\textrm\{Muon\}, as instances of steepest descent under matrix operator norms. This perspective links optimizer geometry with the Lipschitz structure of the network forward map, and enables width-independent control of both Lipschitz and smoothness constants. However, steepest-descent rules induced by standard $p \\to q$ operator norms lack layerwise composability and therefore cannot provide width-independent bounds in deep architectures. We overcome this limitation by introducing a family of mean-normalized operator norms, denoted $\\pmean \\to \\qmean$, that admit layerwise composability, yield width-independent smoothness bounds, and give rise to practical optimizers such as \\emph\{rescaled\} \\textrm\{AdamW\}, row normalization, and column normalization. The resulting learning rate width-aware scaling rules recover $μ$P scaling~\\cite\{yang2021tensor\} as a special case and provide a principled mechanism for cross-width learning-rate transfer across a broad class of optimizers. We further show that \\textrm\{Muon\} can suffer an $\\mathcal\{O\}\(\\sqrt\{w\}\)$ worst-case growth in the smoothness constant, whereas a new family of row-normalized optimizers we propose achieves width-independent smoothness guarantees. Based on the observations, we propose MOGA \(Matrix Operator Geometry Aware\), a width-aware optimizer based only on row/column-wise normalization that enables stable learning-rate transfer across model widths. Large-scale pre-training on GPT-2 and LLaMA shows that MOGA, especially with row normalization, is competitive with Muon while being notably faster in large-token and low-loss regimes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
