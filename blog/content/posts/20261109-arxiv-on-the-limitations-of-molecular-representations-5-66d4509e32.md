---
title: "On the limitations of molecular representations"
date: 2026-11-09T05:11:03+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:635fe70f4c91965fde9e3f44e9cd7e8e7ea85f42063ae14ff5175ae6be277039"
source_payload_sha256: "sha256:e27f69aa00ccfb60d2155636b404ef49bf120dba0f0b0b1587309ba1766832c8"
observation_id: obs_66d4509e328b015ac0e2da269af5528d551496c43b9adaeccc7dcb8c365cea37
event_id: evt_17d0530e3edf75c33bce4657b5bc86e0e3bcc11f89f25690fd2c883b23b12bda
revision_id: rev_2d0d57a6fce19b006951feafd0d6dec4932147d3a85a0899395c18a65be501db
source_published_at: 2026-11-05T18:19:19Z
first_seen_at: 2026-11-08T21:09:34.939959Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 47
interpretation_sha256: "sha256:c36ccf5075201f93f96bb96d5e4f06e58471602e3c9c34774cc0c55397917faf"
description: "这项研究系统比较了分子指纹、学习型嵌入和理化描述符，发现现有先进嵌入模型在捕捉分子图结构、三维形状及 ADMET 终点相似性方面并未优于传统方法。研究还指出，分子表示的碰撞可能影响虚拟筛选。"
external_url: http://arxiv.org/abs/2611.08420v1
parent_observation_id: null
last_seen_at: 2026-11-08T21:09:34.939959Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08420v1](http://arxiv.org/abs/2611.08420v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Acer Blake、Fergus Imrie、Charlotte M. Deane

## 要点解读

### 这是什么
这项研究系统比较了分子指纹、学习型嵌入和理化描述符，发现现有先进嵌入模型在捕捉分子图结构、三维形状及 ADMET 终点相似性方面并未优于传统方法。研究还指出，分子表示的碰撞可能影响虚拟筛选。

### 用在哪里
内容适用于化学信息学和小分子机器学习，可用于理解聚类、数据集划分、虚拟筛选等任务中输入表示的局限，也可帮助研究者选择或改进分子编码方式。

### 可以推断的
- 推测：在虚拟筛选中，非唯一表示可能增加区分相似候选分子的难度。
- 推测：评估新分子编码时，不能只看下游模型表现，还应考察其对结构、三维形状和 ADMET 相似性的表达能力。

## 来源摘要/节选

> Molecular representations such as fingerprints and learned embeddings play a central role in cheminformatics and small-molecule machine learning. They serve as the primary input for a diverse array of tasks, including clustering, dataset splitting, and virtual screening, yet their evaluation is often limited to downstream model performance on narrow benchmark tasks. We carried out a systematic investigation of the quality of molecular representations, finding that none of the state-of-the-art molecular embedding models capture graph structure, 3D shape, or ADMET endpoint similarity better than fingerprints or physicochemical descriptors. However, classical fingerprints also revealed their own material limitations. For example, we show that depending on the representation, between 225M and $\sim$4B molecules have non-unique representations in the 10.8B Enamine REAL database, with implications for virtual screening. Our findings provide an insight into the current limitations of molecular representations, outlining future research directions for the development of more robust encodings of small molecules.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。