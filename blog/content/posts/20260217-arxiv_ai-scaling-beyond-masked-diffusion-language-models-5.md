---
title: Scaling Beyond Masked Diffusion Language Models
date: 2026-02-17 22:35:47+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15014v1
aliases:
- /posts/20260218-arxiv_ai-scaling-beyond-masked-diffusion-language-models-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:42239d98de56886dd5d0143edf554808621b3c1337c59bcba7ce2b136a7befcf
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 47
captured_at: '2026-07-18T04:15:48.934783Z'
source_capture_sha256: sha256:d395b1c08774fbb5602fd0adf9e9ac4d8016daddfc985af4c2982a8c18a85631
source_capture_chars_original: 1323
source_publication_excerpt_chars: 1323
observation_id: obs_a6e98141120020908c5fb14f8fe128f20959a898364633e321c7f25c2d55cb3b
revision_id: rev_701693cd7beb4f97c0976ff2a36b460c73fc448b39008b81c3227ec54b522dae
event_id: evt_13794155f9df8fad3158717cfffe52877326540b1d1bc319ad9e16e5b2d21910
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-17T09:52:08Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15014v1](<https://arxiv.org/abs/2602.15014v1>)
- **作者**: Subham Sekhar Sahoo, Jean-Marie Lemercier, Zhihan Yang, Justin Deschenaux, Jingyu Liu, John Thickstun, Ante Jukic
- **分类**: cs.LG
- **论文时间**: 2026-02-16T18:54:47Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15014v1.pdf](<https://arxiv.org/pdf/2602.15014v1.pdf>)

## 来源摘要/节选

> Diffusion language models are a promising alternative to autoregressive models due to their potential for faster generation. Among discrete diffusion approaches, Masked diffusion currently dominates, largely driven by strong perplexity on language modeling benchmarks. In this work, we present the first scaling law study of uniform-state and interpolating discrete diffusion methods. We also show that Masked diffusion models can be made approximately 12% more FLOPs-efficient when trained with a simple cross-entropy objective. We find that perplexity is informative within a diffusion family but can be misleading across families, where models with worse likelihood scaling may be preferable due to faster and more practical sampling, as reflected by the speed-quality Pareto frontier. These results challenge the view that Masked diffusion is categorically the future of diffusion language modeling and that perplexity alone suffices for cross-algorithm comparison. Scaling all methods to 1.7B parameters, we show that uniform-state diffusion remains competitive on likelihood-based benchmarks and outperforms autoregressive and Masked diffusion models on GSM8K, despite worse validation perplexity. We provide the code, model checkpoints, and video tutorials on the project page: http://s-sahoo.github.io/scaling-dllms

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
