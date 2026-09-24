---
title: "Cross-Scale Transfer Learning for Depression Severity Prediction: From PHQ-8 to HAMD-17 Across Languages and Clinical Paradigms"
date: 2026-09-25T06:26:43+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:80c2345f025c138b02382237054256c631adadc7dd2f4a1bb6fdbd7926d4c06a"
source_payload_sha256: "sha256:6773eac47736b85bb205939674068f26fe333e2ae019a3a94d6c7e234c412942"
observation_id: obs_7d398d2fe2db5a93fdd8aeaa720d0b589b52b26431f08de946285c122949abe2
event_id: evt_1b752249ef8daaca4f0d15e93d0f1bf22d70527040688631cdc05c6638ce40b4
revision_id: rev_fcbf46c58785eb7ca14ba7454d59db87766e784471df7cca93f52ca17959dc89
source_published_at: 2026-09-23T17:30:07Z
first_seen_at: 2026-09-24T22:23:57.522004Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 127
interpretation_sha256: "sha256:3dd2c5ca0cbadbbb96bb1f6ebfd5db95b14b40cedf97e7e45c0dd211f24a90d1"
description: "该研究提出一种跨规模迁移学习方案，通过在大型语言模型上顺序使用低秩适配，实现从英语评估量表到中文评估量表的抑郁严重度连续评分预测。在公开临床访谈数据集上进行分层交叉验证，评估其在不同规模模型上的预测误差与分类性能。"
external_url: http://arxiv.org/abs/2609.28430v1
parent_observation_id: null
last_seen_at: 2026-09-24T22:23:57.522004Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.28430v1](http://arxiv.org/abs/2609.28430v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Wenjie Feng、Sahba Zojaji、Satoshi Nakamura

## 要点解读

### 这是什么
该研究提出一种跨规模迁移学习方案，通过在大型语言模型上顺序使用低秩适配，实现从英语评估量表到中文评估量表的抑郁严重度连续评分预测。在公开临床访谈数据集上进行分层交叉验证，评估其在不同规模模型上的预测误差与分类性能。

### 用在哪里
适用于在数据稀缺的临床环境中快速构建抑郁评估模型的研究者或临床机构。对探索跨语言、跨评估尺度迁移的学术工作也有参考价值。

### 可以推断的
推测：在该实验条件下，先利用高资源语言进行适配再迁移到低资源语言的顺序可能更具优势。  
推测：若在类似任务中直接使用目标语言的原生文本，可能比机器翻译后的输入获得更稳定的性能。

## 来源摘要/节选

> This work addresses continuous depression-severity score prediction from clinical interview transcripts under data scarcity. We propose a sequential low-rank adaptation (LoRA) protocol for cross-scale transfer: a Qwen3 backbone with a bounded regression head is first fine-tuned on the English DAIC-WOZ dataset (189 avatar-mediated sessions, PHQ-8), and the adapter then initializes fine-tuning on the Chinese PDCH dataset (100 real clinical consultations, HAMD-17), where a reinitialised, scale-specific head predicts the clinician-assigned score. All configurations use patient-level stratified 5-fold, 2-repeat cross-validation. On the data-scarce HAMD-17 target, the sequential protocol attains the best point-estimate MAE , RMSE, and macro-$F_1$ on both 0.6B and 1.7B backbones, outperforming target-only training and non-LLM baselines---4.96/6.59/0.36 with Qwen3-0.6B and 4.38/5.62/0.46 with Qwen3-1.7B. Ablations suggest that correctly aligned source supervision gives the best point estimates (unsupervised exposure and shuffled-label controls also show partial gains), that native-Chinese target input outperforms machine-translated English input, and that the reversed order yields no clear gain within run-to-run variance. The study is an exploratory, single-site internal evaluation: it does not establish screening or diagnostic utility, nor separately identify the contribution of the scale, language, or paradigm shifts. To our knowledge, no prior study evaluates this specific DAIC-WOZ-to-PDCH sequential transfer setting.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。