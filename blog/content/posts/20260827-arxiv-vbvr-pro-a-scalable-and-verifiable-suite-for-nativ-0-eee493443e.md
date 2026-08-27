---
title: "VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning"
date: 2026-08-27T17:49:49+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c5ee1f9ae5fbfb8cb94b404a63a8947cc646c23831d9562958ff89f59bf380fe"
source_payload_sha256: "sha256:62f4b86c49fa7752dc57e728b166ed5de93419fa26b3333f606db783b7c34da2"
observation_id: obs_eee493443e25d74b97dd80d3c99df6adebe5db2f6610f1a7f0b6ae4cb9dbd9d9
event_id: evt_708cd8ef931916a70bd846ad761733ac6b159f55ba7e9f439a8865138aaac837
revision_id: rev_6f107b1c99296fdedbd4be5ada657f57e06d1fee2be01ef25ec44b08436f4ccf
source_published_at: 2026-08-26T17:59:51Z
first_seen_at: 2026-08-27T09:46:59.577351Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
interpretation_sha256: "sha256:7d47f484f5c6ec3b956ee781982a873995fdbab7a083d1a1f47c3365d9c9b080"
description: "VBVR-Pro 是一个闭环测试平台，旨在把视觉生成本身作为推理介质，实现视觉推理任务的可训练、可验证和可优化。平台提供可扩展的任务集、基于确定性规则的奖励评分器，并支持对多种生成模型进行机制分析。"
external_url: http://arxiv.org/abs/2608.26105v1
parent_observation_id: null
last_seen_at: 2026-08-27T09:46:59.577351Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.26105v1](http://arxiv.org/abs/2608.26105v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Junxiang Xu、Ruisi Wang、Fanyi Pu 等

## 要点解读

### 这是什么  
VBVR-Pro 是一个闭环测试平台，旨在把视觉生成本身作为推理介质，实现视觉推理任务的可训练、可验证和可优化。平台提供可扩展的任务集、基于确定性规则的奖励评分器，并支持对多种生成模型进行机制分析。

### 用在哪里  
适合从事多模态大模型、视觉推理以及强化学习研究的团队，尤其是需要构建可控训练任务、设计可靠奖励信号或比较不同生成范式表现的研究者。

### 可以推断的  
推测：平台开放的数据、模型、评分器和代码或能让研究者在已有基准上快速实验，降低自行搭建评测环境的成本。  
推测：通过对图像、视频以及交错生成方式的对比，团队能够直观了解不同生成模式在需要时空状态跟踪的视觉推理任务中的优势。

## 来源摘要/节选

> Native visual reasoning treats visual generation as the medium of reasoning itself: visual states (i.e. images and videos) are not merely inputs to be understood or outputs to be rendered, but first-class substrates for problem solving beyond language. Yet progress remains bottlenecked by the lack of scalable training tasks, reliable feedback, and controlled comparisons across generative substrates. In this work, we introduce VBVR-Pro, a closed-loop testbed that makes native visual reasoning through generation trainable, verifiable, optimizable, and experimentally controllable. 1) Task scaling. VBVR-Pro turns visual reasoning into a controlled task space of 300 procedurally generated tasks. Models trained on VBVR-Pro show strong transfer beyond the proposed suite across seven external visual reasoning benchmarks such as RISE-Video, MME-CoF-Pro, and BabyVision. 2) Verifiable rewards. VBVR-Pro provides verifiable reward scorers for task-grounded evaluation. Through a systematic study of leading MLLMs as judges, we identify recurring failure modes of the prevalent VLM-as-a-judge paradigm. In contrast, the proposed scorers are grounded in deterministic, task-specific rules, achieve fine-grained alignment with human judgments. Importantly, they serve as reliable reward signals for large-scale multi-task reinforcement learning and demonstrate stronger post-RL performance across visual reasoning tasks. 3) Mechanism study. VBVR-Pro enables controlled modality studies across more than 30 image, video, and interleaved generators. Our analysis shows that video generation remains strongest for tasks requiring persistent spatiotemporal state tracking, while interleaved generation provides a compute-efficient alternative. Critically, ablations and probing suggest the presence of vision-native trajectories that are crucial to visual reasoning. We release all data, models, scorers, and code.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。