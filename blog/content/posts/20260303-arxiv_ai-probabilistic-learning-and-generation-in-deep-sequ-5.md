---
title: Probabilistic Learning and Generation in Deep Sequence Models
date: 2026-03-03 02:52:12+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.00888v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d140c194d0f75891cc3896be56126e3b9dd6d60333aa66482b951a8588959d7e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:26:34.932328Z'
source_capture_sha256: sha256:b9540a6fee2efae10afcd3f3f84c14efe2cf256569946efe8cde4e3330b414de
source_capture_chars_original: 1911
source_publication_excerpt_chars: 1911
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.00888v1](<https://arxiv.org/abs/2603.00888v1>)
- **作者**: Wenlong Chen
- **分类**: cs.LG
- **论文时间**: 2026-03-01T03:22:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.00888v1.pdf](<https://arxiv.org/pdf/2603.00888v1.pdf>)

## 来源摘要/节选

> Despite exceptional predictive performance of Deep sequence models \(DSMs\), the main concern of their deployment centers around the lack of uncertainty awareness. In contrast, probabilistic models quantify the uncertainty associated with unobserved variables with rules of probability. Notably, Bayesian methods leverage Bayes' rule to express our belief of unobserved variables in a principled way. Since exact Bayesian inference is computationally infeasible at scale, approximate inference is required in practice. Two major bottlenecks of Bayesian methods, especially when applied in deep neural networks, are prior specification and approximation quality. In Chapter 3 &amp; 4, we investigate how the architectures of DSMs themselves can be informative for the design of priors or approximations in probabilistic models. We first develop an approximate Bayesian inference method tailored to the Transformer based on the similarity between attention and sparse Gaussian process. Next, we exploit the long-range memory preservation capability of HiPPOs \(High-order Polynomial Projection Operators\) to construct an interdomain inducing point for Gaussian process, which successfully memorizes the history in online learning. In addition to the progress of DSMs in predictive tasks, sequential generative models consisting of a sequence of latent variables are popularized in the domain of deep generative models. Inspired by the explicit self-supervised signals for these latent variables in diffusion models, in Chapter 5, we explore the possibility of improving other generative models with self-supervision for their sequential latent states, and investigate desired probabilistic structures over them. Overall, this thesis leverages inductive biases in DSMs to design probabilistic inference or structure, which bridges the gap between DSMs and probabilistic models, leading to mutually reinforced improvement.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
