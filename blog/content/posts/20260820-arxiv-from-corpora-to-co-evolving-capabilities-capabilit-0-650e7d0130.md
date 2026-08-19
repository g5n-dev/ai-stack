---
title: "From Corpora to Co-Evolving Capabilities: Capability-Centric Data Design for Generalist Image Generation"
date: 2026-08-20T03:42:41+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b3821d2af7e084a9c2c3d61cec96afc084c5a0cae9b56525669e0c4d78630dea"
source_payload_sha256: "sha256:d8269e0f34547ef74a625c31a0f95b7330cb8a2c65c79f363a0b704993894f1a"
observation_id: obs_650e7d01305bf7ec657d52d5ba8e4c3f070071c330a47e3318d588bb941e1e68
event_id: evt_6cda86fe10ae217e834c0b19a39cc24829663398604b90072987b3de96228da4
revision_id: rev_06a0a93a75cc3b3756eb2845d30bfdd9cff96e7f0cfcd2146eeee544824eb102
source_published_at: 2026-08-18T17:59:01Z
first_seen_at: 2026-08-19T19:40:26.020038Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
interpretation_sha256: "sha256:8debe1219fa8bb780452b098149c467609bca58254a7c133d9ba2a23f1693940"
description: "该研究提出一种以能力为中心的数据基础设施，将能力特定的监督构建与课程调度相结合，构建文本‑图像对齐、图像间转换和图像‑知识关联三类互补的监督，并通过多阶段课程逐步提升数据组成和质量。"
external_url: http://arxiv.org/abs/2608.18076v1
parent_observation_id: null
last_seen_at: 2026-08-19T19:40:26.020038Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.18076v1](http://arxiv.org/abs/2608.18076v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Xingjian Wang、Zhao Wang、Taihang Hu 等

## 要点解读

### 这是什么
该研究提出一种以能力为中心的数据基础设施，将能力特定的监督构建与课程调度相结合，构建文本‑图像对齐、图像间转换和图像‑知识关联三类互补的监督，并通过多阶段课程逐步提升数据组成和质量。

### 用在哪里
适用于大规模文本到图像及编辑模型的训练与数据管理，帮助研究团队或工程团队统一组织多样化的生成能力数据。

### 可以推断的
- 推测：通过能力维度的课程安排，模型有望在不同生成任务上逐步提升表现。  
- 推测：能力感知的评估与检索机制或能在实际使用中快速定位模型短板并进行针对性补足。

## 来源摘要/节选

> Large-scale image generation has benefited from advances in data scale, quality, rebalancing, and recaptioning, yet conventional pipelines typically optimize task-specific datasets in isolation. A central challenge is not only how to curate each task-specific corpus, but also how to organize heterogeneous supervision according to the dependencies among generative capabilities. We present a \textbf{capability-driven data infrastructure} that couples capability-specific supervision construction with capability-aligned curriculum scheduling. Its three specialized yet interoperable data engines build complementary relational supervision for text-image grounding, inter-image transformation, and image-knowledge association, while caption experts align T2I and editing supervision across tasks and granularities. A multi-stage curriculum jointly evolves task composition, visual-concept distribution, data quality, and image resolution along the dependency order of capability acquisition, with capability-aware evaluation closing the loop through targeted retrieval, expert construction, and gap-aware resampling. At scale, the framework curates a 440M-image T2I corpus, 120M editing pairs, and over 27M image-entity pairs. With this infrastructure, we train multimodal diffusion models at two scales from scratch, with 3B and 6B sizes respectively. We conduct quantitative evaluation on CPI-Bench, along with qualitative evaluations across diverse text-to-image and editing scenarios. Experimental results present broad visual coverage, versatile rendering, and effective transfer across generative capabilities.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。