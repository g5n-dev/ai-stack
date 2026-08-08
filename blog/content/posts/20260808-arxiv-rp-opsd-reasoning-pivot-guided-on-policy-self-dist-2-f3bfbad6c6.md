---
title: "RP-OPSD: Reasoning-Pivot-Guided On-Policy Self-Distillation for Multilingual Reasoning Transfer"
date: 2026-08-08T00:14:26+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:681cd8a9fc1c71b1e855901ad6625bb29023cdab9ee8c0439000dfc4a2452355"
source_payload_sha256: "sha256:69988cf65372a881e0fbe877fc85e226ec02048a049f3c042856d6cc6af0d8d5"
observation_id: obs_f3bfbad6c6a2f27ca529c0e123ac7855a13329201f0f31a48098f53643a17a89
event_id: evt_f909c98b7046c6b81a8851cbd52e99566e3cf882dd9a4cb8786cae26d2f60a09
revision_id: rev_4b8db6de448453c54279e67fe93d6cc28a987ea826276ed65b48aebd4d1406a2
source_published_at: 2026-08-06T17:52:06Z
first_seen_at: 2026-08-07T16:23:12Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:6efd7620ac922a509aacd4f750c7d45a59f404055d6a06677d6e72ad0ed138c3"
description: "RP-OPSD 是一种在多语言推理迁移中使用的自蒸馏方法，通过识别推理过程中的关键转折点（推理枢轴）来引导特权蒸馏。它利用教师在有无英文参考答案两种视图之间的分布差异来调节蒸馏信号，并在数学推理基准上取得了对多种语言和难度的性能提升。"
external_url: http://arxiv.org/abs/2608.06347v1
parent_observation_id: null
last_seen_at: 2026-08-08T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06347v1](http://arxiv.org/abs/2608.06347v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Xinye Wang、Junxiao Liu、Shujian Huang

## 要点解读

### 这是什么  
RP-OPSD 是一种在多语言推理迁移中使用的自蒸馏方法，通过识别推理过程中的关键转折点（推理枢轴）来引导特权蒸馏。它利用教师在有无英文参考答案两种视图之间的分布差异来调节蒸馏信号，并在数学推理基准上取得了对多种语言和难度的性能提升。  

### 用在哪里  
适用于需要把大语言模型的推理能力从高资源语言扩展到低资源语言的研发团队，也适合在多语言教育、自动解题或智能辅导等场景中部署。  

### 可以推断的  
推测：关注推理枢轴的做法可能帮助模型在语言结构差异较大的情况下保持推理链的连贯性。  
推测：在新语言缺乏大量标注数据时，利用教师提供的参考答案进行特权蒸馏有望缓解数据稀缺带来的性能瓶颈。

## 来源摘要/节选

> Multilingual reasoning transfer is crucial for extending reasoning capabilities of large language models (LLMs) beyond high-resource languages. On-policy self-distillation (OPSD) and its variants have emerged as a promising paradigm, providing dense token-level supervision on student-generated rollouts, yet their objectives do not explicitly prioritize reasoning signals most critical to cross-lingual transfer. We characterize that target-language reasoning comprises the generation of both surface text and reasoning pivots, which are decisions that advance or redirect the reasoning process and shape subsequent inference. This motivates concentrating privileged distillation around such pivots. We therefore propose RP-OPSD, Reasoning-Pivot-guided On-Policy Self-Distillation, using the distributional shift between matched teacher views with and without an English reference solution as an operational proxy to guide privileged distillation and reference anchoring. Experiments on mathematical reasoning benchmarks covering 17 languages and multiple difficulty levels show that our method outperforms strong multilingual reasoning baselines and OPSD variants. Further analysis reveals that RP-OPSD concentrates privileged distillation on reasoning-control and problem-condistioned state-update tokens, while downweighting it for tokens that mainly support surface realization. Our code is available at https://github.com/NJUNLP/RP-OPSD.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。