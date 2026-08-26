---
title: "Parameterized Complexity of $L_p$-Lipschitz Constants for Input Convex Neural Networks and $L_p$-Norm Maximization over Zonotopes"
date: 2026-08-26T12:58:10+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CC", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8155197d4fb14dfbfffb1409d5cd9e63f9979c2f26d7158ec90488a6cab68264"
source_payload_sha256: "sha256:d0da1dd25e24c65d2217e610afa20b76af670abe27ee9f489c72f837ba99d930"
observation_id: obs_a52c390e958313150a45197d131fc9244132a7ab3bf4443f44f860a5a33b249b
event_id: evt_95de69cf6a29afc38015b3d4834d06866fc4375250dcea17debae15ee6fe12e6
revision_id: rev_dd6dffc7845935781b17a7d8f1203e97ad4709a05190adfaba1a6bb98ced7de4
source_published_at: 2026-08-25T17:47:37Z
first_seen_at: 2026-08-26T14:06:05.473824Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 129
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.24865v1
parent_observation_id: null
last_seen_at: 2026-08-26T04:55:29.051134Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24865v1](http://arxiv.org/abs/2608.24865v1)
- **发布域名**: arxiv.org
- **分类**: cs.CC
- **作者**: Aritra Das、Vincent Froese、Moritz Grillo 等

## 来源摘要/节选

> Lipschitz constants are a standard way to quantify the sensitivity of neural networks to small input perturbations, but computing them is difficult even for shallow ReLU networks. We study this problem for two-layer input-convex neural networks (ICNNs), a restricted architecture where nonnegative output weights enforce convexity. Computing the $L_p$-Lipschitz constant for these networks is equivalent to maximizing the dual norm over a zonotope. While $L_1$- and $L_\infty$-norm maximization on zonotopes admit fixed-parameter and polynomial-time algorithms, respectively, the parameterized complexity of the remaining $L_p$-norms was open. We prove that, for every fixed $p\in (1,\infty)\cap \mathbb{Q}$, maximizing the $L_p$-norm over a zonotope in $\mathbb{R}^d$ is W[1]-hard with respect to the dimension $d$. Moreover, our hardness results imply that brute-force enumeration algorithms are essentially optimal for this problem under the Exponential Time Hypothesis. By duality, the same hardness results hold for computing the $L_p$-Lipschitz constant of two-layer ReLU ICNNs. Our proof first establishes the result for the $L_2$-norm and then transfers the construction to arbitrary fixed $p\in (1,\infty)\cap\mathbb{Q}$ using a suitable Taylor approximation. These results resolve the corresponding questions regarding the parameterized complexity status for zonotope norm maximization and two-layer ICNN Lipschitz constants.
> Our paper resolves an open problem posted at COLT'25. There are several independent concurrent papers resolving the same problem. Our paper prioritizes a clear exposition of the underlying mathematics and conceptual intuitions behind the proof. Additionally, we explicitly describe our research process including the use of LLMs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。