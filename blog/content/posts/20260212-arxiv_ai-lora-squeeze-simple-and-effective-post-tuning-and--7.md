---
title: 'LoRA-Squeeze: Simple and Effective Post-Tuning and In-Tuning Compression of
  LoRA Modules'
date: 2026-02-12 02:48:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10993v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2c1f4d70c1e8f9c2c303ce11dea9186ffdf11df70705342ec60c594cdc9fe521
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
captured_at: '2026-07-18T04:14:55.115056Z'
source_capture_sha256: sha256:8df1f27dec59b65656bdf3d21774d0e6afa4b9918b52774e007e7ef5ee72e5dc
source_capture_chars_original: 1459
source_publication_excerpt_chars: 1459
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10993v1](<https://arxiv.org/abs/2602.10993v1>)
- **作者**: Ivan Vulić, Adam Grycner, Quentin de Laroussilhe, Jonas Pfeiffer
- **分类**: cs.CL
- **论文时间**: 2026-02-11T16:19:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10993v1.pdf](<https://arxiv.org/pdf/2602.10993v1.pdf>)

## 来源摘要/节选

> Despite its huge number of variants, standard Low-Rank Adaptation \(LoRA\) is still a dominant technique for parameter-efficient fine-tuning \(PEFT\). Nonetheless, it faces persistent challenges, including the pre-selection of an optimal rank and rank-specific hyper-parameters, as well as the deployment complexity of heterogeneous-rank modules and more sophisticated LoRA derivatives. In this work, we introduce LoRA-Squeeze, a simple and efficient methodology that aims to improve standard LoRA learning by changing LoRA module ranks either post-hoc or dynamically during training\}. Our approach posits that it is better to first learn an expressive, higher-rank solution and then compress it, rather than learning a constrained, low-rank solution directly. The method involves fine-tuning with a deliberately high\(er\) source rank, reconstructing or efficiently approximating the reconstruction of the full weight update matrix, and then using Randomized Singular Value Decomposition \(RSVD\) to create a new, compressed LoRA module at a lower target rank. Extensive experiments across 13 text and 10 vision-language tasks show that post-hoc compression often produces lower-rank adapters that outperform those trained directly at the target rank, especially if a small number of fine-tuning steps at the target rank is allowed. Moreover, a gradual, in-tuning rank annealing variant of LoRA-Squeeze consistently achieves the best LoRA size-performance trade-off.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
