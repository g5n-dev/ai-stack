---
title: Demystifing Video Reasoning
date: 2026-03-18 08:22:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.16870v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2218bb541ebf8713852da43c90379400270a5c7ad26f38e555a83e3acedd6f9e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:28:41.690884Z'
source_capture_sha256: sha256:0167ce730698122f537998ca06d0dc966f7d3fdf09e8807d88308a2cde624932
source_capture_chars_original: 1830
source_publication_excerpt_chars: 1830
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.16870v1](<https://arxiv.org/abs/2603.16870v1>)
- **作者**: Ruisi Wang, Zhongang Cai, Fanyi Pu, Junxiang Xu, Wanqi Yin, Maijunxian Wang, Ran Ji, Chenyang Gu, Bo Li, Ziqi Huang, Hokin Deng, Dahua Lin, Ziwei Liu, Lei Yang
- **分类**: cs.CV
- **论文时间**: 2026-03-17T17:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.16870v1.pdf](<https://arxiv.org/pdf/2603.16870v1.pdf>)

## 来源摘要/节选

> Recent advances in video generation have revealed an unexpected phenomenon: diffusion-based video models exhibit non-trivial reasoning capabilities. Prior work attributes this to a Chain-of-Frames \(CoF\) mechanism, where reasoning is assumed to unfold sequentially across video frames. In this work, we challenge this assumption and uncover a fundamentally different mechanism. We show that reasoning in video models instead primarily emerges along the diffusion denoising steps. Through qualitative analysis and targeted probing experiments, we find that models explore multiple candidate solutions in early denoising steps and progressively converge to a final answer, a process we term Chain-of-Steps \(CoS\). Beyond this core mechanism, we identify several emergent reasoning behaviors critical to model performance: \(1\) working memory, enabling persistent reference; \(2\) self-correction and enhancement, allowing recovery from incorrect intermediate solutions; and \(3\) perception before action, where early steps establish semantic grounding and later steps perform structured manipulation. During a diffusion step, we further uncover self-evolved functional specialization within Diffusion Transformers, where early layers encode dense perceptual structure, middle layers execute reasoning, and later layers consolidate latent representations. Motivated by these insights, we present a simple training-free strategy as a proof-of-concept, demonstrating how reasoning can be improved by ensembling latent trajectories from identical models with different random seeds. Overall, our work provides a systematic understanding of how reasoning emerges in video generation models, offering a foundation to guide future research in better exploiting the inherent reasoning dynamics of video models as a new substrate for intelligence.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
