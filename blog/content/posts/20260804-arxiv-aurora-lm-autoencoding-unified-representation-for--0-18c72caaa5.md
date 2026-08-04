---
title: "AURORA-LM: Autoencoding Unified Representation for Continuous-Latent Diffusion Language Modeling"
date: 2026-08-04T11:39:28+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:24a888b037a01fd2627baf5533da89a59c73373a59967b7b5cb4320c16d15dff"
source_payload_sha256: "sha256:f34293d80c3bcb5973c49a5617365e0827a54955ddbb0049b02b732522dc46c8"
observation_id: obs_18c72caaa5b5944ce65d36f0cd1748f74f27feda0174a618d15b0162fb4ea242
event_id: evt_8a2a35e856d77a346b6c7a29d1d6ce0a02091405aaecca25af3a2133bc93e239
revision_id: rev_172b442f092e842977dafa9e92bd46b9d0e7eee076549c7020510921a151cc49
source_published_at: 2026-08-03T17:59:50Z
first_seen_at: 2026-08-04T03:36:26.798172Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
interpretation_sha256: "sha256:7a226ee64abeee3def0df657bf9d0e2a4bab8f2a98087cac67d1ad698fb19997"
description: "AURORA-LM 是一种在连续潜空间使用扩散技术进行文本生成的语言模型，通过查询式编码器‑解码器将文本映射为高容量可解码的潜码，并利用块因果扩散Transformer学习该潜码的分布。"
external_url: http://arxiv.org/abs/2608.02602v1
parent_observation_id: null
last_seen_at: 2026-08-04T03:36:26.798172Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.02602v1](http://arxiv.org/abs/2608.02602v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Jiajun Liang、Yucheng Liao、Yukang Cao 等

## 要点解读

### 这是什么
AURORA-LM 是一种在连续潜空间使用扩散技术进行文本生成的语言模型，通过查询式编码器‑解码器将文本映射为高容量可解码的潜码，并利用块因果扩散Transformer学习该潜码的分布。

### 用在哪里
适用于对生成质量要求较高的自由文本生成或摘要任务，尤其是想探索连续潜空间扩散语言模型的研发人员和工程师。

### 可以推断的
推测：扩散过程在连续潜码上通常比离散 token 模型需要更多的计算和迭代步数。  
推测：在需要保持语言细节或提升生成逼真度的场景，这类模型可能更具优势。

## 来源摘要/节选

> Language remains an outlier in generative modeling: while images, video, and audio are increasingly modeled in continuous latent spaces, text generation still relies predominantly on discrete tokens. Existing continuous language models either inherit embedding spaces not designed for joint generation and decoding, or compress autoencoded latents to ease diffusion, sacrificing token-level fidelity. Instead of simplifying the representation to suit the generative model, we preserve a high-capacity, decodable text latent and design the diffusion model to learn its distribution directly.
> We introduce AURORA-LM, a continuous-latent diffusion language model that separates the construction of a decodable text representation from the modeling of its distribution. A Query-based Encoder-Decoder organizes text into a high-capacity, prefix-aligned latent sequence, and a Block-causal Diffusion Transformer learns its distribution through flow matching, generating blocks left to right while denoising positions within each block in parallel. Because such a latent is harder for diffusion to model, AURORA-LM restricts only the noisy-input pathway while retaining the full clean-latent prediction target, accommodating full-width latents without reducing decoder-facing capacity. We further calibrate the noise-level distribution to the latent width, and introduce self-trajectory consistency to bridge independently sampled training noise and iterative denoising at inference.
> AURORA-LM achieves the strongest performance among evaluated continuous and diffusion-based language models on OpenWebText free generation and XSum summarization. Scaling to 1B parameters with about 1500 EFLOPs of total compute yields further gains, surpassing a larger publicly released latent-diffusion language model under a matched evaluation protocol. All experiments are conducted on Ascend NPUs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。