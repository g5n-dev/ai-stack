---
title: "SynCo: Learning Cross-Modal Synergy by Contrasting Interaction Residuals"
date: 2026-09-29T09:59:43+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d6d7cb83f59d46e2ce6e60484b283a2f2e344671eb897acd7f63c476534611bd"
source_payload_sha256: "sha256:57ca08faab422b74164af8896c12ca5734a5e1ba476590ec1ef161673ed0ee93"
observation_id: obs_a2e3f27c58065dc98362f5ed1ecaa3f795046f2efaa2a556b6728ed4ad595cf6
event_id: evt_ea98ed2125a895831b411b4d5b83d22b27be44dff414f33b69f7ea1deb694ac8
revision_id: rev_6ab0a91ce28fe80c580824140e774e1e1f5ec94c96d2c9af28d44a419d35a854
source_published_at: 2026-09-26T18:19:41Z
first_seen_at: 2026-09-29T01:56:54.407370Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:a51f31c19e3d253c01f9639034209cf3eec99f30b6165b0e5be38ef65d85e51f"
description: "SynCo 是一种针对多模态对比学习中协同信息训练不足的问题，通过在学习过程中引入交互残差的专门对比监督来提升协同信息捕获的方法。它使用线性投影预测融合表示，并将残差作为独立的对比目标。"
external_url: http://arxiv.org/abs/2609.32846v1
parent_observation_id: null
last_seen_at: 2026-09-29T01:56:54.407370Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.32846v1](http://arxiv.org/abs/2609.32846v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yavuz Yarici、Ghassan AlRegib

## 要点解读

### 这是什么
SynCo 是一种针对多模态对比学习中协同信息训练不足的问题，通过在学习过程中引入交互残差的专门对比监督来提升协同信息捕获的方法。它使用线性投影预测融合表示，并将残差作为独立的对比目标。

### 用在哪里
适用于需要在多种模态间提取仅在联合观测时出现的协同信息的研发场景，尤其是已有对比学习框架希望在不改变融合结构的前提下进行增强的科研与工程团队。该方法已在受控 Trifeature 基准和真实数据集合 MultiBench、DARai、MM-IMDb 等上验证。

### 可以推断的
推测：在协同信息对任务性能贡献较大的跨模态理解任务（如多模态检索或情感分析）中，SynCo 可能带来显著提升。  
推测：由于该方法以插件形式集成，对现有系统的接入成本较低，可在实际产品中快速实验并迭代。

## 来源摘要/节选

> Multimodal contrastive learning is a dominant paradigm for learning transferable representations from unlabeled data, but standard objectives primarily capture information that is redundant between modalities. Partial Information Decomposition (PID) shows that task-relevant information in multimodal data decomposes into three components: redundancy shared between modalities, uniqueness specific to each modality, and synergy available only from their joint observation. Recent frameworks extend contrastive learning to capture all three components, yet synergy remains undertrained in practice. We propose SynCo (Synergy Contrastive Learning), a method that directly addresses synergy undertraining through dedicated supervision on an interaction residual. SynCo fits a linear projector to predict the fused representation from independently computed unimodal features, and the resulting interaction residual, which removes the linearly unimodal-predictable component, receives dedicated contrastive supervision at negligible computational cost. On the controlled Trifeature benchmark, SynCo achieves state-of-the-art synergy capture with a $+5.98\%$ gain over the baseline, and on real-world benchmarks from MultiBench, DARai, and MM-IMDb, SynCo consistently outperforms or matches prior methods across diverse modality combinations and task types. The method operates as a plug-in to existing contrastive multimodal frameworks without modifying the underlying fusion architecture and can further improve synergy capture when combined with other methods.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。