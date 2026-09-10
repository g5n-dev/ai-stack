---
title: "Cross-Model Agreement as a Deployment-Time Reliability Signal for Automatic Polyp Segmentation"
date: 2026-09-10T22:29:01+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e116c30d99a0da7075cc57e4c2224df5d392b0592c692650ff6a27c887274fb6"
source_payload_sha256: "sha256:a683ceab1559eab028feca8b3d1d945518f474e3014e8b6fc2cf2d508a7bf5d1"
observation_id: obs_83b71cdb98436cf267a306b58aa11f9923cd9f99898b64025e45714d71173513
event_id: evt_507f31ccef2e8c1d3cceb508eec16bea5ff44f55b5f6c4bff5258f3920a24923
revision_id: rev_06b4af7076ed5ae90542a9aadefafee86fd82698c39b1ea097e482b70aa0184d
source_published_at: 2026-09-09T17:32:43Z
first_seen_at: 2026-09-10T14:39:41Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 94
interpretation_sha256: "sha256:bfae098ea97e763cf778db78ceac86bf74853079a2f7c262d2f52edfb9c3c7e2"
description: "该研究提出一种无需标注即可评估结肠镜实时图像中息肉分割模型可靠性的框架。它利用一个独立训练的裁判模型在同一样本上进行分割，通过比较两者的输出一致性来形成可靠性信号，并据此判断主模型是否可能出错。"
external_url: http://arxiv.org/abs/2609.10495v1
parent_observation_id: null
last_seen_at: 2026-09-10T14:26:16.255519Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.10495v1](http://arxiv.org/abs/2609.10495v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Siddharth Gupta、Jitin Singla

## 要点解读

### 这是什么
该研究提出一种无需标注即可评估结肠镜实时图像中息肉分割模型可靠性的框架。它利用一个独立训练的裁判模型在同一样本上进行分割，通过比较两者的输出一致性来形成可靠性信号，并据此判断主模型是否可能出错。

### 用在哪里
适用于需要在推理阶段自动感知模型输出可信度的临床辅助系统，尤其是实时结肠镜检查场景。对从事医学图像分割算法研发或想在部署阶段进行自检的团队有帮助。

### 可以推断的
推测：在缺乏人工标注的部署环境中，使用第二个独立模型作为裁判可以在几乎不增加计算成本的情况下提供实时的可靠性评估。  
推测：该一致性评估思路或可迁移至其他医学影像分割任务，如肿瘤或器官分割，从而帮助构建自动化的质量控制流程。

## 来源摘要/节选

> In real-time colonoscopy, ground-truth annotations are unavailable at inference, so polyp segmentation models can fail silently. We propose Referee-Based Quality Estimation (RBQE), a reference-free framework measuring agreement between a primary segmentation model and an independently trained referee on the same image. RBQE is evaluated on a standardized 1,223-image external benchmark drawn from four public datasets, using four referee configurations chosen to separate two design axes: referee independence and architectural diversity. Using a common Agreement Dice descriptor, a same-architecture referee differing from the primary model only in random initialization already yields a useful reliability signal (ROC-AUC = 0.923), showing that independent training alone is sufficient. Cross-architecture referees improve further: SegFormer-B0 achieves the strongest performance (ROC-AUC = 0.960), significantly outperforming the same-architecture control and UNet++, and exceeding a representative Test-Time Augmentation baseline by 0.055 ROC-AUC under an identical protocol, whereas a prompt-coupled MedSAM referee underperforms despite maximal architectural diversity. Because empty-mask agreement is trivially separable, we also report a restricted evaluation excluding such cases: ROC-AUC falls to 0.876 (SegFormer-B0, 1,046 images) and 0.783 (same-architecture control, 975 images), yet RBQE's margin over both baselines widens on this identical subset. RBQE additionally increases the mean Dice of retained predictions as low-agreement cases are progressively rejected, supporting selective prediction, and requires only one additional deterministic referee forward pass at inference. Our study therefore supports cross-model agreement as a practical, interpretable reliability framework for automated polyp segmentation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。