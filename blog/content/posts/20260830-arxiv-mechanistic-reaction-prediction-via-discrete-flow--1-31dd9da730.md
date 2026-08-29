---
title: "Mechanistic Reaction Prediction via Discrete Flow Matching on Graph-Structured Electron Occupation"
date: 2026-08-30T02:32:12+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7b4496ac82851c61765c769233e8e2aadbcbd22315d06f825b3faeb3f89361c5"
source_payload_sha256: "sha256:142034c9b44e1de6c713f0ace58169606938bde1ed37fc9784a3676bb11e0d2d"
observation_id: obs_31dd9da730e8ce58e425df34ffc91f69651a19979c86932081da80f6247e023f
event_id: evt_24989a3fd405ab34baad066c0011c2494a73c704728b4eb9a43ae49081ca4ec8
revision_id: rev_bcdf5c0b01b318f3d56a5ef21d1273939d22c66191c15d26e04d30556c451358
source_published_at: 2026-08-27T17:50:44Z
first_seen_at: 2026-08-29T18:28:26.486591Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:6cbc54f254122fb97fce93a857dac127c7c7380e51e6efdcea7f442991818095"
description: "该研究将化学反应视为电子在化学键、非键和氢位点上的重新分布，采用离散流匹配在电子占据向量上进行建模，并通过连续时间马尔可夫链结合最优传输构造出一系列可解释的编辑步骤。"
external_url: http://arxiv.org/abs/2608.27429v1
parent_observation_id: null
last_seen_at: 2026-08-29T18:28:26.486591Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27429v1](http://arxiv.org/abs/2608.27429v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Nguyen Xuan-Vu、Octavian Susanu、Daniel Armstrong 等

## 要点解读

### 这是什么
该研究将化学反应视为电子在化学键、非键和氢位点上的重新分布，采用离散流匹配在电子占据向量上进行建模，并通过连续时间马尔可夫链结合最优传输构造出一系列可解释的编辑步骤。

### 用在哪里
适用于需要预测反应产物、揭示反应机理以及生成副产物的计算化学和药物设计场景，尤其在结构复杂或反应类型未知的情况下进行评估时。

### 可以推断的
推测：在结构复杂度和反应类型变化的分布外测试中，所提方法能够保持较好的预测水平，而现有方法在此类情况下表现下降。  
推测：由于直接学习电子重新分配的全过程，模型能够自然产生与已知化学规律一致的机理轨迹。

## 来源摘要/节选

> Chemical reactions are fundamentally transformations in electron space, yet most machine learning approaches model them either through \textit{de novo} generation of product molecules or through heuristic graph edits that operate directly on molecular topology.
> We introduce MAELLE (\textbf{M}ech\textbf{A}nistic \textbf{E}dit f\textbf{L}ow-matching on e\textbf{L}ectron r\textbf{E}arrangements), which instead models reactions as discrete flow matching over electron occupation vectors.
> Concretely, we formulate the reactant-to-product mapping as a Continuous-time Markov Chain (CTMC) over the graph-structured integer-valued electron occupation space defined on all bonding, non-bonding, and hydrogen sites.
> To construct the intermediate edit trajectories, we generalize the discrete flow matching mixture path to discrete electron rearrangements using Optimal Transport, yielding a sequence of mechanistically interpretable edit moves without requiring elementary step annotations.
> MAELLE achieves competitive performance on the USPTO-480K benchmark compared with leading reaction prediction models.
> Beyond in-distribution accuracy, we evaluate robustness across two out-of-distribution settings - structural complexity and reaction type - and find that MAELLE maintains strong performance where existing methods degrade.
> Finally, because the learned flow operates over the full electron redistribution, MAELLE naturally recovers mechanistic trajectories that align with known chemistry and can predict side products of a reaction.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。