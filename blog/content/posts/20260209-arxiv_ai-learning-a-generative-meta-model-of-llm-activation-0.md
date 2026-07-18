---
title: Learning a Generative Meta-Model of LLM Activations
date: 2026-02-09 23:42:37+08:00
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
external_url: https://arxiv.org/abs/2602.06964v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0c7467e2e1bb4dc7fa27d97aa9cff7dccd95128542b494c83de029951cff9f8d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 51
captured_at: '2026-07-18T04:11:23.963527Z'
source_capture_sha256: sha256:445d04f18969e7fe187a266094fdb3546cf20bd48b2b4e8d9dcae7303d56a7d6
source_capture_chars_original: 1040
source_publication_excerpt_chars: 1040
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06964v1](<https://arxiv.org/abs/2602.06964v1>)
- **作者**: Grace Luo, Jiahai Feng, Trevor Darrell, Alec Radford, Jacob Steinhardt
- **分类**: cs.LG
- **论文时间**: 2026-02-06T18:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06964v1.pdf](<https://arxiv.org/pdf/2602.06964v1.pdf>)

## 来源摘要/节选

> Existing approaches for analyzing neural network activations, such as PCA and sparse autoencoders, rely on strong structural assumptions. Generative models offer an alternative: they can uncover structure without such assumptions and act as priors that improve intervention fidelity. We explore this direction by training diffusion models on one billion residual stream activations, creating "meta-models" that learn the distribution of a network's internal states. We find that diffusion loss decreases smoothly with compute and reliably predicts downstream utility. In particular, applying the meta-model's learned prior to steering interventions improves fluency, with larger gains as loss decreases. Moreover, the meta-model's neurons increasingly isolate concepts into individual units, with sparse probing scores that scale as loss decreases. These results suggest generative meta-models offer a scalable path toward interpretability without restrictive structural assumptions. Project page: https://generative-latent-prior.github.io.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
