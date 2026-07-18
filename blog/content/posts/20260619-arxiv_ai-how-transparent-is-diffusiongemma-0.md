---
title: How Transparent is DiffusionGemma?
date: 2026-06-19 23:23:51+08:00
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
external_url: https://arxiv.org/abs/2606.20560v1
aliases:
- /posts/20260620-arxiv_ai-how-transparent-is-diffusiongemma-0/
- /posts/20260621-arxiv_ai-how-transparent-is-diffusiongemma-0/
- /posts/20260622-arxiv_ai-how-transparent-is-diffusiongemma-0/
- /posts/20260623-arxiv_ai-how-transparent-is-diffusiongemma-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:72212a24baae50f7558a353f7a4c5edbe23fccc3d308e298ccf35e6d8d013562
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 34
captured_at: '2026-07-18T04:30:09.568344Z'
source_capture_sha256: sha256:a76afbdb84b46ad5c5378daf8a1193b58b892e214a15db4f00da0294efa22b63
source_capture_chars_original: 1869
source_publication_excerpt_chars: 1869
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.20560v1](<https://arxiv.org/abs/2606.20560v1>)
- **作者**: Joshua Engels, Callum McDougall, Bilal Chughtai, Janos Kramar, Senthoran Rajamanoharan, Cindy Wu, Arthur Conmy, Asic Q Chen, Jean Tarbouriech, Min Ma, Brendan O'Donoghue, João Gabriel Lopes de Oliveira, Rohin Shah, Neel Nanda
- **分类**: cs.LG
- **论文时间**: 2026-06-18T17:59:46Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.20560v1.pdf](<https://arxiv.org/pdf/2606.20560v1.pdf>)

## 来源摘要/节选

> LLM reasoning transparency is a critical affordance for understanding model decisions, mitigating misuse and misalignment, and debugging surprising model behaviors. However, DiffusionGemma performs a larger fraction of its computation in a continuous latent space; does this make its reasoning less transparent? We study this question by decomposing transparency into two components: variable transparency, whether we understand intermediate snapshots of a model's computational state; and algorithmic transparency, whether we can use these snapshots to reconstruct the process by which the model arrived at its outputs. Naively, DiffusionGemma has poor variable transparency: its opaque serial depth, the amount of serial computation that occurs in between interpretable model states, seems at first 28.6X higher than the corresponding autoregressive Gemma 4 model. However, we show that we can map the information flowing between denoising steps through an interpretable token bottleneck with no decrease in downstream performance. Treating these intermediate states as interpretable reduces the opaque serial depth to just 1.1X that of Gemma 4. Algorithmic transparency is harder for diffusion models than for autoregressive models because all token predictions in the canvas can change at every denoising step, giving the model the power to implement complicated distributed algorithms during the denoising process. To begin bridging this gap, we conduct a suite of interpretability case studies, uncovering initial evidence of novel diffusion-specific phenomena such as non-chronological reasoning, token and sequence smearing, and intermediate-context reasoning. Finally, we test monitorability, a key application of transparency that measures whether model outputs are useful for downstream tasks. We find that DiffusionGemma is similarly monitorable to Gemma 4.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
