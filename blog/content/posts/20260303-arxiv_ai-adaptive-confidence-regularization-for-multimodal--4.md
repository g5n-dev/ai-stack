---
title: Adaptive Confidence Regularization for Multimodal Failure Detection
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02200v1
aliases:
- /posts/20260304-arxiv_ai-adaptive-confidence-regularization-for-multimodal--4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:fd4898dc440e00ae1addc3571cb1df0dd1c5bd74ac94af9d63d5606440201510
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:26:19.677155Z'
source_capture_sha256: sha256:9c88a71452b1d5349560c4684ec815e07d54dd6d40d6cea1de8c3e1487ff9c66
source_capture_chars_original: 1302
source_publication_excerpt_chars: 1302
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02200v1](<https://arxiv.org/abs/2603.02200v1>)
- **作者**: Moru Liu, Hao Dong, Olga Fink, Mario Trapp
- **分类**: cs.CV
- **论文时间**: 2026-03-02T18:56:38Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02200v1.pdf](<https://arxiv.org/pdf/2603.02200v1.pdf>)

## 来源摘要/节选

> The deployment of multimodal models in high-stakes domains, such as self-driving vehicles and medical diagnostics, demands not only strong predictive performance but also reliable mechanisms for detecting failures. In this work, we address the largely unexplored problem of failure detection in multimodal contexts. We propose Adaptive Confidence Regularization \(ACR\), a novel framework specifically designed to detect multimodal failures. Our approach is driven by a key observation: in most failure cases, the confidence of the multimodal prediction is significantly lower than that of at least one unimodal branch, a phenomenon we term confidence degradation. To mitigate this, we introduce an Adaptive Confidence Loss that penalizes such degradations during training. In addition, we propose Multimodal Feature Swapping, a novel outlier synthesis technique that generates challenging, failure-aware training examples. By training with these synthetic failures, ACR learns to more effectively recognize and reject uncertain predictions, thereby improving overall reliability. Extensive experiments across four datasets, three modalities, and multiple evaluation settings demonstrate that ACR achieves consistent and robust gains. The source code will be available at https://github.com/mona4399/ACR.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
