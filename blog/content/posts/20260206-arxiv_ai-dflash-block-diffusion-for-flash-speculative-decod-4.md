---
title: 'DFlash: Block Diffusion for Flash Speculative Decoding'
date: 2026-02-06 23:01:34+08:00
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
external_url: https://arxiv.org/abs/2602.06036v1
aliases:
- /posts/20260207-arxiv_ai-dflash-block-diffusion-for-flash-speculative-decod-4/
- /posts/20260208-arxiv_ai-dflash-block-diffusion-for-flash-speculative-decod-4/
- /posts/20260209-arxiv_ai-dflash-block-diffusion-for-flash-speculative-decod-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c04e712a702b797a97b81242b2daebed8e7c12459a53cdfa85042c8d30072efc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
captured_at: '2026-07-18T04:11:05.007784Z'
source_capture_sha256: sha256:e9b1899e67f5662b7339f40fec672ecf19f28f738c8b6f685cb9d95da8262cec
source_capture_chars_original: 1167
source_publication_excerpt_chars: 1167
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06036v1](<https://arxiv.org/abs/2602.06036v1>)
- **作者**: Jian Chen, Yesheng Liang, Zhijian Liu
- **分类**: cs.CL
- **论文时间**: 2026-02-05T18:59:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06036v1.pdf](<https://arxiv.org/pdf/2602.06036v1.pdf>)

## 来源摘要/节选

> Autoregressive large language models \(LLMs\) deliver strong performance but require inherently sequential decoding, leading to high inference latency and poor GPU utilization. Speculative decoding mitigates this bottleneck by using a fast draft model whose outputs are verified in parallel by the target LLM; however, existing methods still rely on autoregressive drafting, which remains sequential and limits practical speedups. Diffusion LLMs offer a promising alternative by enabling parallel generation, but current diffusion models typically underperform compared with autoregressive models. In this paper, we introduce DFlash, a speculative decoding framework that employs a lightweight block diffusion model for parallel drafting. By generating draft tokens in a single forward pass and conditioning the draft model on context features extracted from the target model, DFlash enables efficient drafting with high-quality outputs and higher acceptance rates. Experiments show that DFlash achieves over 6x lossless acceleration across a range of models and tasks, delivering up to 2.5x higher speedup than the state-of-the-art speculative decoding method EAGLE-3.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
