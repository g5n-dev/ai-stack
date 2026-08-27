---
title: "A Visual Dependence-Aware Framework for Multimodal Unsupervised Continual Post-Training"
date: 2026-08-28T04:33:19+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:dafd65a3b78a652445c83b68b2614530ecf1332885f7843e196969690443ef9f"
source_payload_sha256: "sha256:d183f55e01e048c7c6e11b7aec1f809cda5396aa8dccdc8ed7c4ff8363c99200"
observation_id: obs_6cd28eb2e7ea7825c7cd77aa3135b925aa1eeffa057acece7f9308f6a12feff3
event_id: evt_1209f21d41b4aab4a692b78ff8dababc02fa9f1548a565d39ad28746881ccbc0
revision_id: rev_8b75ad94eab50fe75ab4bdbda9125add55730917f66a8759856c97eaa5564fe6
source_published_at: 2026-08-26T17:57:04Z
first_seen_at: 2026-08-27T20:30:11.125207Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
interpretation_sha256: "sha256:89e53006b805eb379ac51cf5ac6b56428f76ddc5dca75888e3596b85562d69bf"
description: "该研究提出一种在多模态大模型持续后训练中，利用视觉依赖信息来平衡旧任务保持与新任务学习的框架，包含视觉约束的最优传输和视觉调制的适应两部分。"
external_url: http://arxiv.org/abs/2608.26095v1
parent_observation_id: null
last_seen_at: 2026-08-27T20:30:11.125207Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.26095v1](http://arxiv.org/abs/2608.26095v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Kaichen Li、Zhilin Zhu、Jianhao Huang 等

## 要点解读

### 这是什么
该研究提出一种在多模态大模型持续后训练中，利用视觉依赖信息来平衡旧任务保持与新任务学习的框架，包含视觉约束的最优传输和视觉调制的适应两部分。

### 用在哪里
适用于需要从无标签流数据中不断更新多模态模型的部署场景，例如实时视频分析、跨模态检索或持续学习的移动端应用。对关注模型长期可维护性和跨模态灾难性遗忘的研发团队有参考价值。

### 可以推断的
推测：该方法对视觉注意的量化较为敏感，实现时可能需要额外的可视化或特征提取工具来捕捉 token 级的视觉依赖。  
推测：在资源受限的终端上运行时，视觉约束的最优传输计算开销可能导致延迟，需要在精度和效率之间做权衡。

## 来源摘要/节选

> In this paper, we explore a novel task of Multimodal Unsupervised Continual Post-Training (MU-CPT), enabling deployed MLLMs to continually evolve from streaming unlabeled data. Existing unsupervised post-training methods for MLLMs typically optimize target tokens uniformly, overlooking their heterogeneous visual dependence (VD). However, we reveal that token-level VD is crucial for MU-CPT. Specifically, its structural distortion serves as an indicator of cross-modal catastrophic forgetting, and its inherent heterogeneity acts as a compass to guide new-task learning. Leveraging this property, we propose a Visual Dependence-Aware (VDA) framework with two main components. First, Visually Constrained Optimal Transport (VC-OT) formulates the VD structural distortion of old-task VD during new-task learning as an optimal transport problem to mitigate cross-modal forgetting. By designing a region-aware ground cost and a dependence-stratified transport penalty, it prevents global shifts in visual focus while strictly prohibiting visual reliance from degenerating into language bias. Second, Visually Modulated Adaptation (VMA) exploits VD heterogeneity to emphasize visually grounded new-task learning, promoting new-task plasticity. Together, our method simultaneously maintains old-task stability and new-task plasticity during challenging MU-CPT. Extensive experiments under our MU-CPT setting validate the effectiveness of VDA.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。