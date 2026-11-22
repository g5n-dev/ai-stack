---
title: "Depth Pro 2: Sharp and Temporally Consistent Metric Monocular Depth"
date: 2026-11-22T19:21:00+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:41f311818fff58ed68edca45c278ab819e09aa9f69a21654b13f3de47ec5b76c"
source_payload_sha256: "sha256:2c0139e6a526958ce09eedf87ada7eda835e989b47329e69968510fb2474d271"
observation_id: obs_e4d0d396cf363875a182053931a97ab4a2faa029b83ef9d24a319276b1d77de6
event_id: evt_fbd061522b681cdcfaf559930b266b45954b370655b75b4d5f7992933f877858
revision_id: rev_d942eace8942a171266769ce3f144c4826b284b7e9ec18d9b7bc04d839a8acb5
source_published_at: 2026-11-19T18:55:41Z
first_seen_at: 2026-11-22T11:31:46Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
interpretation_sha256: "sha256:4a6912ec07f25c829b0f55d87165d1451c173b50e1b6ab671397b4bfe6cbb1bb"
description: "Depth Pro 2 是一种单目度量深度估计方法，能够从图像或视频中生成全分辨率的稠密深度图，同时兼顾边界清晰度与时间一致性。论文还发布了多个模型，以及代码和权重。"
external_url: http://arxiv.org/abs/2611.26603v1
parent_observation_id: null
last_seen_at: 2026-11-22T11:19:33.141616Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26603v1](http://arxiv.org/abs/2611.26603v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Peiyun Hu、Marko Mihajlovic、Lyndon Duong 等

## 要点解读

### 这是什么
Depth Pro 2 是一种单目度量深度估计方法，能够从图像或视频中生成全分辨率的稠密深度图，同时兼顾边界清晰度与时间一致性。论文还发布了多个模型，以及代码和权重。

### 用在哪里
它适用于需要从单张图像或连续视频中获取深度信息的视觉任务，尤其适合同时要求空间细节和帧间稳定性的场景。研究人员或开发者也可用于模型复现与集成。

### 可以推断的
- 推测：原生分辨率输出可能有利于保留物体边界等空间细节。
- 推测：兼顾清晰度与时间一致性，可能有助于降低不同应用中的取舍成本。

## 来源摘要/节选

> We present Depth Pro 2, an approach to estimating dense metric depth for images and video at full resolution. By analyzing prior methods for monocular depth estimation, we find that they commonly trade off temporal consistency and boundary sharpness: multi-frame methods favor consistency, single-frame methods favor sharpness. To overcome this trade-off, we train a single, scalable network that processes both images and video and predicts depth maps at native resolution. Depth Pro 2 produces depth maps that are metrically accurate, sharp, and temporally consistent all at once, outperforming prior work in all of these dimensions. We release a family of models that define a new Pareto frontier in terms of metric accuracy, sharpness, temporal consistency, and runtime. We release code and weights at https://apple-aiml-research.github.io/ml-depth-pro-2/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。