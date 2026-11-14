---
title: "ArchSpace: Recording, Reviewing, and Referencing LLM Architecture Research"
date: 2026-11-14T00:20:58+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c02a91648292c346c8b3173b5db2365e0704d16855760beb280574b4e5e3252f"
source_payload_sha256: "sha256:43735462be1406f0a8f0f33008102534437552f084da70d6fdc59b02df5ee288"
observation_id: obs_a630d99dd60c5344c4ab1a2f081ac9d958832586d4e36d9f8f05178c57379b27
event_id: evt_7e18e66e7450fe664cc3b4ce25f06cd8b9a90330ad2931bd25b7d3f28015218f
revision_id: rev_aa7e7935a1d1e9cefd5d9e92faddd501f1425ef95f778ce13cbddac7714c2502
source_published_at: 2026-11-12T18:59:52Z
first_seen_at: 2026-11-13T16:32:05Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:4653c0b47fafbb4dd81806349a1094fefb912f6182de63c91d63b7940250e6cd"
description: "ArchSpace 是一个面向大语言模型架构研究的公开平台，用于记录研究提案、实验过程与推理，并通过社区评审和后续引用形成可追溯的积累。它还用缩放定律从较小规模实验预测更大规模的模型损失，以辅助早期评估。"
external_url: http://arxiv.org/abs/2611.17332v1
parent_observation_id: null
last_seen_at: 2026-11-14T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.17332v1](http://arxiv.org/abs/2611.17332v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Jie Wang、Tong Zhu、JiaHao Kuang 等

## 要点解读

### 这是什么
ArchSpace 是一个面向大语言模型架构研究的公开平台，用于记录研究提案、实验过程与推理，并通过社区评审和后续引用形成可追溯的积累。它还用缩放定律从较小规模实验预测更大规模的模型损失，以辅助早期评估。

### 用在哪里
该平台适合希望在投入大规模训练前验证架构想法的研究人员与模型开发团队，也可用于查找可复用的训练配方、基线和经过评审的研究记录。

### 可以推断的
- 推测：这种公开记录与评审机制可能有助于减少不同研究之间的重复尝试，并提升架构实验的可复现性。
- 推测：基于缩放定律的预测可作为筛选候选方案的参考，但最终效果仍可能需要更大规模训练验证。

## 来源摘要/节选

> Model architecture shapes the scaling behavior, training efficiency, and inference cost of LLMs, making it a central focus of both industry and academia. In industry, teams such as those behind DeepSeek, Qwen, and Kimi routinely introduce architectural innovations, yet public reports rarely document which ideas succeeded, which were abandoned, and why. In academia, limited compute and inconsistent baselines often restrict evaluations to small-scale, single-point comparisons, making it difficult to establish whether improvements hold at larger scales or translate into broader impact. ArchSpace addresses both gaps as a public platform for Recording, Reviewing, and Referencing Architecture Researc}: each proposal is recorded with its experiments and reasoning, reviewed by the community, and referenced by later work. To evaluate ideas before costly large-scale training, ArchSpace leverages scaling laws to predict model loss at larger scales from smaller experiments, a practice widely adopted in industry. We provide initial references that make the platform usable: Qwen3.5 and OLMo3 baselines, fitted scaling laws, and a reusable training recipe. Ideas validated through this review can in turn become new baselines, and ArchSpace thereby aims to broaden the range of ideas that shape the next generation of models.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。