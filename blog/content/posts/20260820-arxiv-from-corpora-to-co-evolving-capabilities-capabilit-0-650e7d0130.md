---
title: "From Corpora to Co-Evolving Capabilities: Capability-Centric Data Design for Generalist Image Generation"
date: 2026-08-20T02:54:22+08:00
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
first_seen_at: 2026-08-19T18:53:05.327963Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
interpretation_sha256: "sha256:ed7e2ebe70d1203a65e6336ba34d444c4735671336832f7932b5c6c0556ddcae"
description: "该研究提出一种以能力为中心的数据基础设施，将针对不同生成能力（如文本‑图像对应、图像间转换、图像‑知识关联）的监督信号与能力顺序的课程调度相结合，形成协同演化的训练框架。"
external_url: http://arxiv.org/abs/2608.18076v1
parent_observation_id: null
last_seen_at: 2026-08-19T18:53:05.327963Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.18076v1](http://arxiv.org/abs/2608.18076v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Xingjian Wang、Zhao Wang、Taihang Hu 等

## 要点解读

### 这是什么  
该研究提出一种以能力为中心的数据基础设施，将针对不同生成能力（如文本‑图像对应、图像间转换、图像‑知识关联）的监督信号与能力顺序的课程调度相结合，形成协同演化的训练框架。

### 用在哪里  
适用于大规模文生图及编辑模型的研发流程，帮助数据团队在多任务场景下系统化构建、对齐和调度监督数据，尤其在需要统一质量与分布的图像生成项目中具有参考价值。

### 可以推断的  
推测：该框架通过能力感知评估与针对性检索，可在数据稀缺或分布不均时实现高效补全，提升模型在细粒度任务上的表现。  
推测：随着监督信号与课程计划的协同进化，模型在不同生成能力之间的迁移成本有望降低，从而简化多任务模型的训练路径。

## 来源摘要/节选

> Large-scale image generation has benefited from advances in data scale, quality, rebalancing, and recaptioning, yet conventional pipelines typically optimize task-specific datasets in isolation. A central challenge is not only how to curate each task-specific corpus, but also how to organize heterogeneous supervision according to the dependencies among generative capabilities. We present a \textbf{capability-driven data infrastructure} that couples capability-specific supervision construction with capability-aligned curriculum scheduling. Its three specialized yet interoperable data engines build complementary relational supervision for text-image grounding, inter-image transformation, and image-knowledge association, while caption experts align T2I and editing supervision across tasks and granularities. A multi-stage curriculum jointly evolves task composition, visual-concept distribution, data quality, and image resolution along the dependency order of capability acquisition, with capability-aware evaluation closing the loop through targeted retrieval, expert construction, and gap-aware resampling. At scale, the framework curates a 440M-image T2I corpus, 120M editing pairs, and over 27M image-entity pairs. With this infrastructure, we train multimodal diffusion models at two scales from scratch, with 3B and 6B sizes respectively. We conduct quantitative evaluation on CPI-Bench, along with qualitative evaluations across diverse text-to-image and editing scenarios. Experimental results present broad visual coverage, versatile rendering, and effective transfer across generative capabilities.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。