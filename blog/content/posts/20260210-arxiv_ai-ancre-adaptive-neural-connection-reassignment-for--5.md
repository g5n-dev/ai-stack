---
title: 'ANCRe: Adaptive Neural Connection Reassignment for Efficient Depth Scaling'
date: 2026-02-10 14:00:18+08:00
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
external_url: https://arxiv.org/abs/2602.09009v1
aliases:
- /posts/20260211-arxiv_ai-ancre-adaptive-neural-connection-reassignment-for--5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:cc15fd8fd74883191f678e32ca1a4423fb98046368b0d28ff6a5682c8d5d2f90
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:14:24.737190Z'
source_capture_sha256: sha256:f577312add3803ad8bb92daf1e44baf26b1f03bf0bd7b11af600d41271c8be4b
source_capture_chars_original: 1088
source_publication_excerpt_chars: 1088
observation_id: obs_a36df5af0e52950a4744bfc6728e139c4fe6d3e0fb95a803dedd4b9649c9c62a
revision_id: rev_e7bda76e3d5c6b3ed5db9e8ebf38a55d1ea4aaefca673aee06a97406c61e0422
event_id: evt_3fe89970de580216e1facb0b32b71870eef18fd99a318bb97cc44ec957dedde2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-10T12:04:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09009v1](<https://arxiv.org/abs/2602.09009v1>)
- **作者**: Yilang Zhang, Bingcong Li, Niao He, Georgios B. Giannakis
- **分类**: cs.LG
- **论文时间**: 2026-02-09T18:54:18Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09009v1.pdf](<https://arxiv.org/pdf/2602.09009v1.pdf>)

## 来源摘要/节选

> Scaling network depth has been a central driver behind the success of modern foundation models, yet recent investigations suggest that deep layers are often underutilized. This paper revisits the default mechanism for deepening neural networks, namely residual connections, from an optimization perspective. Rigorous analysis proves that the layout of residual connections can fundamentally shape convergence behavior, and even induces an exponential gap in convergence rates. Prompted by this insight, we introduce adaptive neural connection reassignment \(ANCRe\), a principled and lightweight framework that parameterizes and learns residual connectivities from the data. ANCRe adaptively reassigns residual connections with negligible computational and memory overhead \($&lt;1\\%$\), while enabling more effective utilization of network depth. Extensive numerical tests across pre-training of large language models, diffusion models, and deep ResNets demonstrate consistently accelerated convergence, boosted performance, and enhanced depth efficiency over conventional residual connections.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
