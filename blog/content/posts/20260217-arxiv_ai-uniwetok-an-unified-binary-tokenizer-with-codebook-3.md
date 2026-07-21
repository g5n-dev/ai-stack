---
title: 'UniWeTok: An Unified Binary Tokenizer with Codebook Size $\mathit{2^{128｝｝$
  for Unified Multimodal Large Language Model'
date: 2026-02-17 03:10:02+08:00
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
external_url: https://arxiv.org/abs/2602.14178v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:29f8fae2a7c0f8d9adf467f36a1b676135222df0975ad247347d509134821d48
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 119
captured_at: '2026-07-18T04:15:48.934783Z'
source_capture_sha256: sha256:0de81530b825f36f58144510293e53ec1337207fe245c91fb1cef7d4714a0433
source_capture_chars_original: 1764
source_publication_excerpt_chars: 1764
observation_id: obs_3cf6b6473ee104f4dc3b2e744c3a03cda869d64af77983bf3b453e0a36f810f2
revision_id: rev_ac6171139eab46f2a16286b0ec12b86adc24a9e20740dc7a2734e3d32c943793
event_id: evt_80d275d1e191dcfea6b8947536bec12670aa4e3f4c750ec1a8c3a5d09fcea802
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-17T04:06:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.14178v1](<https://arxiv.org/abs/2602.14178v1>)
- **作者**: Shaobin Zhuang, Yuang Ai, Jiaming Han, Weijia Mao, Xiaohui Li, Fangyikang Wang, Xiao Wang, Yan Li, Shanchuan Lin, Kun Xu, Zhenheng Yang, Huaibo Huang, Xiangyu Yue, Hao Chen, Yali Wang
- **分类**: cs.CV
- **论文时间**: 2026-02-15T15:07:19Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.14178v1.pdf](<https://arxiv.org/pdf/2602.14178v1.pdf>)

## 来源摘要/节选

> Unified Multimodal Large Language Models \(MLLMs\) require a visual representation that simultaneously supports high-fidelity reconstruction, complex semantic extraction, and generative suitability. However, existing visual tokenizers typically struggle to satisfy these conflicting objectives within a single framework. In this paper, we introduce UniWeTok, a unified discrete tokenizer designed to bridge this gap using a massive binary codebook \($\\mathit\{2^\{128&#125;&#125;$\). For training framework, we introduce Pre-Post Distillation and a Generative-Aware Prior to enhance the semantic extraction and generative prior of the discrete tokens. In terms of model architecture, we propose a convolution-attention hybrid architecture with the SigLu activation function. SigLu activation not only bounds the encoder output and stabilizes the semantic distillation process but also effectively addresses the optimization conflict between token entropy loss and commitment loss. We further propose a three-stage training framework designed to enhance UniWeTok's adaptability cross various image resolutions and perception-sensitive scenarios, such as those involving human faces and textual content. On ImageNet, UniWeTok achieves state-of-the-art image generation performance \(FID: UniWeTok 1.38 vs. REPA 1.42\) while requiring a remarkably low training compute \(Training Tokens: UniWeTok 33B vs. REPA 262B\). On general-domain, UniWeTok demonstrates highly competitive capabilities across a broad range of tasks, including multimodal understanding, image generation \(DPG Score: UniWeTok 86.63 vs. FLUX.1 \[Dev\] 83.84\), and editing \(GEdit Overall Score: UniWeTok 5.09 vs. OmniGen 5.06\). We release code and models to facilitate community exploration of unified tokenizer and MLLM.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
