---
title: 'MXNorm: Reusing MXFP block scales for efficient tensor normalisation'
date: 2026-03-16 23:16:09+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 深度学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.13180v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:dc47d006d68f72302d5161981087fbd7d446033571e185d49a57ecc102deeaa8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:28:19.053555Z'
source_capture_sha256: sha256:a7f0fff4c6351d9ffffbc2702fff7f07ac6d37edf8afc51f3d6ff194484fb4f8
source_capture_chars_original: 1053
source_publication_excerpt_chars: 1053
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.13180v1](<https://arxiv.org/abs/2603.13180v1>)
- **作者**: Callum McLean, Luke Y. Prince, Alexandre Payot, Paul Balança, Carlo Luschi
- **分类**: cs.LG
- **论文时间**: 2026-03-13T17:14:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.13180v1.pdf](<https://arxiv.org/pdf/2603.13180v1.pdf>)

## 来源摘要/节选

> Matrix multiplication performance has long been the major bottleneck to scaling deep learning workloads, which has stimulated the design of new accelerators that use increasingly low-precision number formats. However, improvements in matrix multiplication performance have far outstripped improvements in performance on reductions and elementwise computations, which are still being performed in higher precision. In this work, we propose MXNorm, a drop-in replacement for RMSNorm that estimates the RMS using only the block scales calculated as part of the MXFP8 cast and enables a 32x decrease in the size of reduction needed for normalization. We validate our approximation method on pre-training of Llama 3 models of 125M, 1B and 8B parameters, finding minimal loss of training accuracy compared to a baseline using RMSNorm with MXFP8 matmuls. We also show practical kernel speedups using only torch.compile of up to 2.4x for MXNorm over RMSNorm, corresponding to a 1.3% speedup in Llama 3 8B transformer layers in MXFP8 and a 2.6% speedup in NVFP4.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
