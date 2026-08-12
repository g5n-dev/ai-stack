---
title: "Beyond a Bag of Features: Set-Level Instability in Sparse Autoencoders"
date: 2026-08-12T14:44:11+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:757aa33355a6f5264eaf5694dad9d04a52bd2900d8b470366687c06dd94ff05d"
source_payload_sha256: "sha256:7b0c2cce68ab0aed3901935a6b6012b89d3b0a79121432d6fdedebc36dadced4"
observation_id: obs_bd2604015493cf75d124a36aefd5ba9c94620da5a58157192bd2c34eb5eb4066
event_id: evt_04ec7cad2c727e307cb4a1af67e688d47db2d02d62d79d4fcaad7f7c6048303f
revision_id: rev_4318c078bb4d469437fb9769ef535a1ff4bde2b456c7d4aeae41d480830f7be4
source_published_at: 2026-08-11T17:55:59Z
first_seen_at: 2026-08-12T17:11:57.823805Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
interpretation_sha256: "sha256:689f867a398483049d4b6ee9afedcab51dea1dc88c844cbe6d70d70fd6ccad43"
description: "这是一项关于稀疏自编码器（SAE）激活集合在语言模型中表示语义相似性的研究，比较了基于集合重叠的相似度与传统密集嵌入的相似度，发现SAE集合不能更准确地反映人类对类别边界和典型性的判断。"
external_url: http://arxiv.org/abs/2608.11197v1
parent_observation_id: null
last_seen_at: 2026-08-12T06:41:59.416901Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11197v1](http://arxiv.org/abs/2608.11197v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Nikolai Bolik、Lennart Stöpler、Artur Andrzejak

## 要点解读

### 这是什么
这是一项关于稀疏自编码器（SAE）激活集合在语言模型中表示语义相似性的研究，比较了基于集合重叠的相似度与传统密集嵌入的相似度，发现SAE集合不能更准确地反映人类对类别边界和典型性的判断。

### 用在哪里
适用于从事大语言模型可解释性、概念对齐或基于激活模式的模型分析的研究者和工程师，帮助评估在特定任务中是否应采用稀疏特征集合而非密集表示。

### 可以推断的
推测：在需要模型行为与人类概念对齐的场景下，直接使用SAE激活集合可能导致偏差，需结合其他相似度指标进行校正。  
推测：SAE特征的组合可能不遵循简单的集合叠加原则，想要利用它们解释复杂语义变化可能需要引入额外的结构化规则。

## 来源摘要/节选

> Shani et al. (2026) show that LLM representations broadly recover human category boundaries, while failing to reflect fine-grained typicality structure. Their analysis uses cosine similarity over dense model representations. We revisit their approach using overlap over active sparse autoencoder (SAE) latent sets as a more interpretable similarity measure. We first verify that this set-level measure is meaningful: SAE latent sets can recover union-like compositional structure in controlled toy models and induce semantically coherent neighborhoods in natural text. Extending the human-concepts analysis to SAE set similarities, we find that SAE activation sets do not recover human category boundaries or within-category typicality more faithfully than dense embeddings or residual-stream states, but instead track model-internal similarity structure. To probe this gap further, we study active latent sets under well-controlled semantic modifications, revealing a substantial mismatch between human judgements of conceptual change and change in the SAE active set. We interpret this as evidence that, outside idealised settings, SAE features do not compose via simple bag-of-features semantics.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。