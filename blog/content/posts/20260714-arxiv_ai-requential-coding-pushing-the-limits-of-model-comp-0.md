---
title: 'Requential Coding: Pushing the Limits of Model Compression with Self-Generated
  Training Data'
date: 2026-07-14 23:29:48+08:00
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
external_url: https://arxiv.org/abs/2607.11883v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:190997724ca70d742afe0901127fb53eaea497e8ddd22340fd1a60471d54c204
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
captured_at: '2026-07-18T04:30:25.647174Z'
source_capture_sha256: sha256:8c2a8c3d63594c2478d6dfca235f95f5ed3f8f9b5ddc78673cb8df341041cfdd
source_capture_chars_original: 1919
source_publication_excerpt_chars: 1919
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.11883v1](<https://arxiv.org/abs/2607.11883v1>)
- **作者**: Shikai Qiu, Marc Finzi, Yujia Zheng, Kun Zhang, Andrew Gordon Wilson
- **分类**: cs.LG
- **论文时间**: 2026-07-13T17:58:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.11883v1.pdf](<https://arxiv.org/pdf/2607.11883v1.pdf>)

## 来源摘要/节选

> Compression is fundamental to intelligence. A model that can represent its training data as a short code has discovered regularities that enable generalization. Large neural networks may learn functions far simpler than their parameter counts suggest, but it is challenging to construct codes that realize this simplicity. Parameter-based methods such as quantization produce code lengths that scale with model size, insensitive to how much information the parameters store. Prequential coding bypasses this issue by compressing the training trajectory, but codes the exact data sequence regardless of how much the model learns, yielding large codes when the data has high entropy. We introduce requential coding, where a teacher model selects training samples drawn from the student's own distribution. The student's code records only these selections, which cost bits only where teacher and student disagree. The resulting code length is independent of parameter count and data entropy, and often orders of magnitude shorter than the prequential counterpart, with an advantage that grows with scale. This compression sheds light on phenomena inaccessible to prior compressors. Holding loss fixed, larger models and ensembles compress to much smaller sizes despite more parameters. Plugged into a PAC-Bayes bound, the requential code yields state-of-the-art generalization guarantees for billion-parameter LLMs, outperforming bounds built on aggressive post-training quantization even granted zero error. The bound tightens with scale in the compute-optimal regime, as models become increasingly compressible relative to dataset size. The same code predicts that models gradually overfit when trained for multiple epochs. It also isolates the learnable information in a dataset from its unpredictable, random content, revealing that lower-entropy text holds far more learnable structure than higher-entropy image data.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
