---
title: 'The Diffusion Duality, Chapter II: $Ψ$-Samplers and Efficient Curriculum'
date: 2026-02-25 23:30:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21185v1
aliases:
- /posts/20260226-arxiv_ai-the-diffusion-duality-chapter-ii-ψ-samplers-and-ef-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:66d61ab7d15017d20664a9a68c06fd0b7463f35e025b23d18238fb7702c9a040
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
captured_at: '2026-07-18T04:16:57.484529Z'
source_capture_sha256: sha256:246b53f156e90a4e1c3f400d82e204aa41bf05929a261154bac5ac8c5dc2d05a
source_capture_chars_original: 1297
source_publication_excerpt_chars: 1297
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21185v1](<https://arxiv.org/abs/2602.21185v1>)
- **作者**: Justin Deschenaux, Caglar Gulcehre, Subham Sekhar Sahoo
- **分类**: cs.LG
- **论文时间**: 2026-02-24T18:35:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21185v1.pdf](<https://arxiv.org/pdf/2602.21185v1.pdf>)

## 来源摘要/节选

> Uniform-state discrete diffusion models excel at few-step generation and guidance due to their ability to self-correct, making them preferred over autoregressive or Masked diffusion models in these settings. However, their sampling quality plateaus with ancestral samplers as the number of steps increases. We introduce a family of Predictor-Corrector \(PC\) samplers for discrete diffusion that generalize prior methods and apply to arbitrary noise processes. When paired with uniform-state diffusion, our samplers outperform ancestral sampling on both language and image modeling, achieving lower generative perplexity at matched unigram entropy on OpenWebText and better FID/IS scores on CIFAR10. Crucially, unlike conventional samplers, our PC methods continue to improve with more sampling steps. Taken together, these findings call into question the assumption that Masked diffusion is the inevitable future of diffusion-based language modeling. Beyond sampling, we develop a memory-efficient curriculum for the Gaussian relaxation training phase, reducing training time by 25% and memory by 33% compared to Duo while maintaining comparable perplexity on OpenWebText and LM1B and strong downstream performance. We release code, checkpoints, and a video-tutorial on: https://s-sahoo.com/duo-ch2

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
