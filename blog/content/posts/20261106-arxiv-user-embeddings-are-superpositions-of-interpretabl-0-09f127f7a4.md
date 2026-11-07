---
title: "User Embeddings are Superpositions of Interpretable Behavioral Modes"
date: 2026-11-06T14:46:58+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:3466add1726cc2d7587854364b6452dcf8fbfe8b1fe1ae0d723ab79458e0e6ae"
source_payload_sha256: "sha256:82f5aaac6367ad97a7d7c0cab90e948e390f8a34f860de92685ea6b0eb331866"
observation_id: obs_09f127f7a40f1050025630fd5eebfef83ca47717fd49e5b0233525a6b7be686f
event_id: evt_7afa0a47ee3433df8133b4a671a4c32630877f06df65bb52e3724944d73c9d1b
revision_id: rev_db96c2fdf1cd77ee7da56a098c6390fa5a2aa9475211c2463e29c4c3bdf472e4
source_published_at: 2026-11-05T18:59:42Z
first_seen_at: 2026-11-06T06:57:16Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
interpretation_sha256: "sha256:26542f74e322a42287b2a02bd1fbecb1ac52b5bdea90c04b459b3927a5bdc0da"
description: "这项研究提出：用户向量可视为多个可解释行为模式的稀疏叠加，并通过稀疏字典学习（如稀疏自编码器）提取这些模式，再为其生成自然语言标签。"
external_url: http://arxiv.org/abs/2611.08487v1
parent_observation_id: null
last_seen_at: 2026-11-07T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08487v1](http://arxiv.org/abs/2611.08487v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Jonathan Kozaczuk、Zheng Dong、Noyan Evirgen 等

## 要点解读

### 这是什么
这项研究提出：用户向量可视为多个可解释行为模式的稀疏叠加，并通过稀疏字典学习（如稀疏自编码器）提取这些模式，再为其生成自然语言标签。

### 用在哪里
适用于推荐系统、个性化服务与用户行为建模，帮助团队解释已有用户向量，或按行为特征进行受众检索与群体刻画。该方法是事后分析，无需改动上游嵌入模型。

### 可以推断的
- 推测：这种表示分解可能有助于降低用户向量的黑盒性，使行为模式更容易被审查、比较和复用。
- 推测：自然语言标签与零样本检索的结合，可能减少额外训练文本标签模型的需求。

## 来源摘要/节选

> User embeddings are central components of modern recommendation, personalization, and behavioral modeling systems. Though these embeddings can compactly encode rich behavioral information, they are inherently dense and opaque, limiting interpretability. To address this gap, we argue that user embeddings can be understood as sparse superpositions of interpretable behavioral modes. This structure is directly predicted by generative models of user behavior for linear embeddings and extends approximately to deep-learning representations by the superposition hypothesis. Superimposed modes can naturally be recovered by sparse dictionary learning methods, such as sparse autoencoders (SAEs), and recovered modes can be automatically named and queried in natural language. We validate mode recovery against known ground truth on synthetic data, where SAEs recover modes better than classical sparse baselines, including on transformer-encoded embeddings. We then apply the method to classical and transformer-based user embeddings from two real-world datasets. We also show how the corresponding natural-language labels enable zero-shot audience retrieval and characterization over embeddings never trained on text. The framework is post-hoc and model-agnostic, requiring no modification to the upstream embedding system.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。