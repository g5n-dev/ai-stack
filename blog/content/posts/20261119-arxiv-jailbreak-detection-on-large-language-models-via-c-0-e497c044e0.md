---
title: "Jailbreak Detection on Large Language Models via Contrastive Prototype Structures"
date: 2026-11-19T21:02:28+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2b22bf169423d9753b95f9e5faa918badf69c4602248a071382ed6ee09855293"
source_payload_sha256: "sha256:15bb6646271bc39c2606e146971146b1cdaa8650d70d79ce04b8a812792eb5fa"
observation_id: obs_e497c044e025058b98ff0f2ed7fa4061c988e4d36320dd440cdbb8d0967cda10
event_id: evt_e8696bb89c1fefb43c9a297fc45456113b9b513836f67a51271f974ce37a3576
revision_id: rev_7fe0f2b8d399dd9fc613b5dfcd661f43e932f7908cebc68564f7cfc91c94f8cf
source_published_at: 2026-11-18T18:56:12Z
first_seen_at: 2026-11-19T13:12:50Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
interpretation_sha256: "sha256:365d2acd8196d14440d8dc6ea9e09e25ef381281f22c825e47da8b1dd9604b00"
description: "JDPI 通过对比学习构造“有害”和“良性”原型，再依据样本与两类原型的距离进行越狱检测，无需额外训练下游分类器。该方法在多个基准上提高了检测准确率，并在跨数据集测试中表现出更强的稳健性。"
external_url: http://arxiv.org/abs/2611.24936v1
parent_observation_id: null
last_seen_at: 2026-11-19T13:01:04.512566Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.24936v1](http://arxiv.org/abs/2611.24936v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yan Qiu、Yuanyuan Li

## 要点解读

### 这是什么
JDPI 通过对比学习构造“有害”和“良性”原型，再依据样本与两类原型的距离进行越狱检测，无需额外训练下游分类器。该方法在多个基准上提高了检测准确率，并在跨数据集测试中表现出更强的稳健性。

### 用在哪里
它适用于大语言模型部署前的越狱与有害提示检测，也适合需要处理多轮对话安全风险的场景。对于标注样本有限、希望减少单独分类器训练开销的团队，这种方法具有参考价值。

### 可以推断的
- 推测：在标注数据有限的安全检测任务中，基于原型距离的判定方式可能更容易快速落地，因为无需再单独训练一个下游分类器。
- 推测：将累计对话历史纳入检测，可能比只检查当前轮次更适合识别连续交互中的越狱行为。

## 来源摘要/节选

> Jailbreak attempts and harmful prompts remain a challenge for the safe deployment of large language models. We study whether contrastively learned representations can support safety detection without training an additional downstream classifier. We propose Jailbreak Detection with Prototype Inference (JDPI), which uses binary safety labels to construct harmful and benign prototypes and makes predictions from relative prototype distances. JDPI uses only binary safety labels for encoder adaptation, prototype construction, and validation. In our setup, it uses fewer labeled examples than the classifier baseline (Method A) by avoiding the separate split used to train the downstream classifier. Across four benchmarks covering different input formats, contrastive fine-tuning improves JDPI's detection accuracy by 9.1-18.0 percentage points. Using the same encoder, JDPI achieves slightly higher ROC-AUC on one benchmark and stays within 0.017 of the baseline across all four. With dataset-specific adaptation, JDPI exceeds the released Llama Guard 3-8B baseline by 0.173-0.310 in ROC-AUC across the four benchmarks. In multi-turn replay on TomGibbs, JDPI uses accumulated user history as the conversation unfolds, achieving higher conversation-level accuracy than when it uses the current turn alone. Across 12 directed transfers, JDPI outperforms the classifier by an average of 1.59 percentage points in accuracy, demonstrating stronger cross-dataset robustness.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。