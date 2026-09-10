---
title: "Studying Image Tokenizers as Visual Languages in Unified Multimodal Models"
date: 2026-09-10T08:17:00+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5cf97196595c8817e349470d27da3c7ac05b198ccb884f5b88499c86e6b17a9d"
source_payload_sha256: "sha256:9250132de3fb4362abea443b8a1c213b27c11ffb0a318a32ab56e2fcfeca4b4d"
observation_id: obs_e283fdb6a4169f23844c01bd611a4229aeba1ec325a0c3edc16bf1af70a76aba
event_id: evt_c6b612eca17868a3a85a843e1696f0899bf5248e08531eb15e652e7bec8db257
revision_id: rev_b5e55acac468b94fe5a19824d1007d8ee6a358dc644aa3cf8866f14d140af5cb
source_published_at: 2026-09-08T17:57:53Z
first_seen_at: 2026-09-10T00:14:42.948507Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:fd263b64cfa8c73b63743f7cc9baf5ed81225e5628d99367efed7cd82a99c442"
description: "该研究通过构建受控的纯自回归测试环境，系统评估图像分词器在联合文本与图像的多模态预训练中的表现，揭示分词器设计与下游任务效果之间的关联。"
external_url: http://arxiv.org/abs/2609.09143v1
parent_observation_id: null
last_seen_at: 2026-09-10T00:14:42.948507Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.09143v1](http://arxiv.org/abs/2609.09143v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Siting Li、Zhengyang Wang、Simon Shaolei Du 等

## 要点解读

### 这是什么
该研究通过构建受控的纯自回归测试环境，系统评估图像分词器在联合文本与图像的多模态预训练中的表现，揭示分词器设计与下游任务效果之间的关联。

### 用在哪里
适用于从事多模态大模型研发的研究人员，以及需要选择或设计图像分词器的工程师，尤其当关注文本与图像联合建模效果时。

### 可以推断的
推测：不同任务的损失值需单独分析才能准确评估分词器性能，跨任务使用统一指标可能导致误判。
推测：仅优化重建质量不足以保证分词器在生成或理解任务中的有效性，设计时需兼顾下游应用场景。

## 来源摘要/节选

> Image tokenizers define the ``visual language'' of unified multimodal models, yet are commonly studied through isolated metrics or generation-/understanding-only evaluations. These evaluations do not fully capture how visual tokens behave when modeled jointly with text. We build a controlled pure-autoregressive testbed and track task-specific validation losses during multimodal continual pretraining across text, image, text-to-image (T2I), and image-to-text (I2T) prediction. We examine how these losses scale and relate to downstream performance, then use them to study multimodal learnability---how well image and text tokens are jointly modeled---and tokenizer design. We find that (1) losses should be analyzed by task, since they exhibit distinct scaling behavior and rank tokenizers differently. (2) The loss--performance relationship depends on the predicted token space: for a fixed tokenizer, T2I and I2T losses correlate with generation quality, but across tokenizers, the T2I loss--performance relationship shifts with the image-token space, whereas I2T loss, computed over a shared text vocabulary, provides a more consistent signal. I2T loss also correlates with both generation and visual understanding performance after supervised finetuning. Using losses as a lens, we show that (3) better reconstruction does not necessarily yield lower task-specific losses or stronger downstream performance, and that (4) image tokenizer choice can affect text modeling under joint optimization. As case studies, we revisit three tokenizer design axes---the discriminator, semantic supervision, and vocabulary size---to examine their effects on joint modeling and downstream performance. Together, our testbed offers a complementary perspective on image tokenizers as visual languages, highlighting their interplay with text in joint multimodal training.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。