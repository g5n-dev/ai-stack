---
title: "Ambient LLMs: Data-Efficient Supervised Fine-tuning via Temperature Matching"
date: 2026-11-18T12:19:39+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:73b35de8841f54600f0e97c042e0976970446f856fda1f0e9b3c7ee3594aefce"
source_payload_sha256: "sha256:230b159c71934e15ad4c84292ac35d7ec110a885f51587a2fa3879aaaadf89f1"
observation_id: obs_50180643bbe51e702fabc8e72ae1982bb3f6a4ac8ccdda20d3ac8a3261917d42
event_id: evt_4088d5afe80376af69365e0eb686ba8972971936abe3440d7125d9d4ca80c724
revision_id: rev_b63eed9ad2fbf611be7b8fae72e4fb3c6011da27555261c6b6335a49c1909b4d
source_published_at: 2026-11-17T18:59:37Z
first_seen_at: 2026-11-18T04:30:28Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
interpretation_sha256: "sha256:a981148c0a4ff48c76a0e177bc3c852523b58e8e15b77235109242d4a07d2e0e"
description: "Ambient SFT 是一种监督微调方法：让微调后的模型在高温条件下逼近冻结的预训练模型分布，以利用不完美预测扩充训练信号，降低过拟合和数据分布尾部遗忘。"
external_url: http://arxiv.org/abs/2611.23229v1
parent_observation_id: null
last_seen_at: 2026-11-18T04:18:09.867340Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.23229v1](http://arxiv.org/abs/2611.23229v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Giannis Daras、Marios Papachristou、Adam Klivans 等

## 要点解读

### 这是什么
Ambient SFT 是一种监督微调方法：让微调后的模型在高温条件下逼近冻结的预训练模型分布，以利用不完美预测扩充训练信号，降低过拟合和数据分布尾部遗忘。

### 用在哪里
适用于大语言模型后训练场景，包括领域适配、指令微调和推理任务，尤其适合高质量后训练数据有限且希望改善数据利用效率的团队。

### 可以推断的
- 推测：高温匹配可在保留预训练模型已有能力与学习新任务之间提供连续调节。
- 推测：若方法能跨领域适配、指令微调和推理保持优势，它可能具有较广的后训练应用潜力。

## 来源摘要/节选

> Collecting large-scale, diverse, and high-quality post-training datasets for autoregressive language models is challenging. Consequently, Supervised Fine-Tuning (SFT) is typically applied to datasets significantly smaller than those used for pre-training, which leads to overfitting and the catastrophic forgetting of the tails of the data distribution. To prevent this collapse, we introduce Ambient SFT, a principled framework for leveraging imperfect predictions to augment the fine-tuning set. In our method, a "frozen" version of the pre-trained model serves as a noisy teacher that the fine-tuned model must match at a coarse level. In particular, we require that the high-temperature versions of the conditional distributions produced by the post-training model should match the high-temperature versions of the pre-training ones. The temperature hyperparameter controls the level of trust in the pre-trained model, with the limit $T\to \infty$ reverting back to regular SFT and $T=1$ to knowledge distillation. We demonstrate that our approach outperforms standard SFT across domain adaptation, instruction-tuning, and reasoning, leading for up to $21\%$ average relative improvement to standard SFT.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。