---
title: Exploring Transformer Placement in Variational Autoencoders for Tabular Data
  Generation
date: 2026-01-29 22:59:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.20854v1
aliases:
- /posts/20260130-arxiv_ai-exploring-transformer-placement-in-variational-aut-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:cef0b328558ce73a9e4f5f6630b6894366f0a6f243ed1367ccb0d37244408088
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:09:34.038253Z'
source_capture_sha256: sha256:abe21f377d61678fbf47df076d3b41915489029a745a9d7509c43f184a03973d
source_capture_chars_original: 986
source_publication_excerpt_chars: 986
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.20854v1](<https://arxiv.org/abs/2601.20854v1>)
- **作者**: Aníbal Silva, Moisés Santos, André Restivo, Carlos Soares
- **分类**: cs.LG
- **论文时间**: 2026-01-28T18:54:27Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.20854v1.pdf](<https://arxiv.org/pdf/2601.20854v1.pdf>)

## 来源摘要/节选

> Tabular data remains a challenging domain for generative models. In particular, the standard Variational Autoencoder \(VAE\) architecture, typically composed of multilayer perceptrons, struggles to model relationships between features, especially when handling mixed data types. In contrast, Transformers, through their attention mechanism, are better suited for capturing complex feature interactions. In this paper, we empirically investigate the impact of integrating Transformers into different components of a VAE. We conduct experiments on 57 datasets from the OpenML CC18 suite and draw two main conclusions. First, results indicate that positioning Transformers to leverage latent and decoder representations leads to a trade-off between fidelity and diversity. Second, we observe a high similarity between consecutive blocks of a Transformer in all components. In particular, in the decoder, the relationship between the input and output of a Transformer is approximately linear.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
