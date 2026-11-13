---
title: "Pyrite: Building and Benchmarking Protein-Ligand Pose Ranking Agents"
date: 2026-11-13T02:54:53+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8c25097f6c3499799d440d8ee5bf13e454b5ca11116c5c1cc21b598834287af8"
source_payload_sha256: "sha256:c0f909258ad78a86ae2830e1f25b1a6d0bc61d1b0d3f312c2348ba3726cead28"
observation_id: obs_57d7d2f6b4aa20be2834015865dea887cbf8be89f9724b5395fb34f3c536100c
event_id: evt_1c1d3cbb4c57dec1c8416b056f3b0531555a5b726d5fb643b6ac574b7d881ec2
revision_id: rev_1228b69d53a5489e021a1918bc1a02965d5ce1b7f8ec904f64c205851f34c472
source_published_at: 2026-11-10T18:56:32Z
first_seen_at: 2026-11-12T19:05:28Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
interpretation_sha256: "sha256:89ff903225f860b117c00dc3bb89d90c01702e2e87124b25e0e637b231589d62"
description: "Pyrite 是蛋白质—配体结合姿态排序基准，包含 1,500 组姿态对。它结合结构化分子表示 PyriteRep，以及直接比较姿态的 PyriteReasoner 和生成特征代码的 PyriteFeaturizer 两类 LLM 智能体。"
external_url: http://arxiv.org/abs/2611.14511v1
parent_observation_id: null
last_seen_at: 2026-11-13T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.14511v1](http://arxiv.org/abs/2611.14511v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Megha Srivastava、Michael H. Lim、Allison M. Keys 等

## 要点解读

### 这是什么
Pyrite 是蛋白质—配体结合姿态排序基准，包含 1,500 组姿态对。它结合结构化分子表示 PyriteRep，以及直接比较姿态的 PyriteReasoner 和生成特征代码的 PyriteFeaturizer 两类 LLM 智能体。

### 用在哪里
该基准适用于药物发现中评估、筛选共折叠模型生成的候选结合姿态，也可用于比较直接推理、代码生成特征和 GRPO 训练对排序效果的影响。

### 可以推断的
- 推测：该任务可能比单次姿态生成更能检验模型是否真正整合了分子几何与化学评分信号。
- 推测：将计算化学工具输出转化为可学习特征，可能比单纯依靠文本推理更适合姿态排序。

## 来源摘要/节选

> Predicting how a ligand binds to its target is central to small-molecule drug discovery. Modern cofolding models can generate diverse candidate poses, but reliably ranking these candidates remains challenging. We introduce Pyrite, a pairwise pose-ranking benchmark comprising 1,500 pose pairs across diverse protein-ligand complexes. Expert chemists equipped with 3D visualization tools and physics-based scores perform near chance, highlighting the difficulty of interpreting available chemical signals. To investigate automated ranking, we introduce PyriteRep, a structured representation of molecular geometry, protein-ligand interactions, and physicochemical scores, and develop two LLM-based agents: PyriteReasoner, which directly compares poses through text-based reasoning, and PyriteFeaturizer, which generates executable code to construct features for logistic regression, optionally incorporating features derived from LLM subcalls. These agents achieve up to 67% and 74% accuracy, respectively, exceeding observed expert performance. LLM-guided feature discovery generally outperforms direct reasoning, while Group Relative Policy Optimization (GRPO) improves open-weight models, enabling them to match or surpass closed-source frontier models in our evaluations. These results establish Pyrite as a challenging test of pose-ranking ability and highlight LLM-guided feature discovery as a promising approach to interpret and combine the outputs of computational chemistry tools.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。