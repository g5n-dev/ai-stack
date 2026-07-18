---
title: 'PLATE: Plasticity-Tunable Efficient Adapters for Geometry-Aware Continual
  Learning'
date: 2026-02-04 23:12:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.03846v1
aliases:
- /posts/20260205-arxiv_ai-plate-plasticity-tunable-efficient-adapters-for-ge-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6b3ce335e6e1d16a14c3d95af62d5f1decf4788231deb80c4cffdd4e7a53d39c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:10:41.702374Z'
source_capture_sha256: sha256:6df2b4b7db3b516909f7aa1d759ad634223fda4f0e4637ee2c475defb4c0ba45
source_capture_chars_original: 1411
source_publication_excerpt_chars: 1411
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.03846v1](<https://arxiv.org/abs/2602.03846v1>)
- **作者**: Romain Cosentino
- **分类**: cs.LG
- **论文时间**: 2026-02-03T18:59:42Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.03846v1.pdf](<https://arxiv.org/pdf/2602.03846v1.pdf>)

## 来源摘要/节选

> We develop a continual learning method for pretrained models that \\emph\{requires no access to old-task data\}, addressing a practical barrier in foundation model adaptation where pretraining distributions are often unavailable. Our key observation is that pretrained networks exhibit substantial \\emph\{geometric redundancy\}, and that this redundancy can be exploited in two complementary ways. First, redundant neurons provide a proxy for dominant pretraining-era feature directions, enabling the construction of approximately protected update subspaces directly from pretrained weights. Second, redundancy offers a natural bias for \\emph\{where\} to place plasticity: by restricting updates to a subset of redundant neurons and constraining the remaining degrees of freedom, we obtain update families with reduced functional drift on the old-data distribution and improved worst-case retention guarantees. These insights lead to \\textsc\{PLATE\} \(\\textbf\{Pla\}sticity-\\textbf\{T\}unable \\textbf\{E\}fficient Adapters\), a continual learning method requiring no past-task data that provides explicit control over the plasticity-retention trade-off. PLATE parameterizes each layer with a structured low-rank update $ΔW = B A Q^\\top$, where $B$ and $Q$ are computed once from pretrained weights and kept frozen, and only $A$ is trained on the new task. The code is available at https://github.com/SalesforceAIResearch/PLATE.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
