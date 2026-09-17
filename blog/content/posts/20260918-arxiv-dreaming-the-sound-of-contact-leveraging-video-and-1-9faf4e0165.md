---
title: "Dreaming the Sound of Contact: Leveraging Video and Audio Generation for Zero-Shot Force-Aware Manipulation and Data Generation"
date: 2026-09-18T02:15:52+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:eed9d31842d9d8439b6944bf70c4f8b5bde088093515ed69b13c364bf1101c6a"
source_payload_sha256: "sha256:77d4a169f877df22e0366faf4561593734b62beeb7e3005d2073b3f0a1057f46"
observation_id: obs_9faf4e0165bb4543a8a1e5c6b0d1a713e2f9ec78e55721fa9a50a402376c1a28
event_id: evt_2cf2111903508d8c1406a6409e8e8020acc24cd13897ccc66b53b3663950d462
revision_id: rev_5f6b3f5a484cd31819dcee071444fee0223bc720158beeb5109654738d7b2563
source_published_at: 2026-09-16T17:56:44Z
first_seen_at: 2026-09-17T18:12:54.596827Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 127
interpretation_sha256: "sha256:f2bc3493e1711c28ac06a752c76dd472460ea7775f18223bbe15cadba0ac4c83"
description: "该研究利用视频和音频的联合生成，把音频的响度映射为随时间变化的期望力轮廓，从而得到兼具运动和力信息的轨迹，并在机器人上通过闭环力调节器实现接触任务。"
external_url: http://arxiv.org/abs/2609.19137v1
parent_observation_id: null
last_seen_at: 2026-09-17T18:12:54.596827Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.19137v1](http://arxiv.org/abs/2609.19137v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Guanhua Ji、Tianyu Li、Dayoon Suh 等

## 要点解读

### 这是什么
该研究利用视频和音频的联合生成，把音频的响度映射为随时间变化的期望力轮廓，从而得到兼具运动和力信息的轨迹，并在机器人上通过闭环力调节器实现接触任务。

### 用在哪里
适用于需要精准控制接触力的机器人操作，如抓取、装配或表面处理等；也可为从事零样本学习、数据增强及力‑视觉‑听觉融合研究的开发者提供参考。

### 可以推断的
- 推测：音频响度与接触力在感知层面存在关联，因此可以借助生成的音效来间接表达力的变化趋势。  
- 推测：在缺乏大规模标注接触力数据时，使用生成的声音作为软标签是一种可行的训练数据来源。

## 来源摘要/节选

> Recent advances in video generation allow robots to learn manipulation trajectories from generated videos. However, these approaches produce purely kinematic trajectories that lack force information, causing failures in contact-rich tasks where appropriate contact forces are essential for success. In this work, we explore augmenting generated video with audio to shape a bounded, time-varying desired-force profile using the loudness of generated contact sounds. We present a pipeline that jointly leverages generated video and audio to derive motion trajectories and corresponding desired-force profiles from a structured natural-language task prompt. We execute these force-aware trajectories on a Franka Panda robot using a closed-loop force regulator that tracks the audio-shaped force profile during contact. We evaluate our pipeline on multiple tasks that require making contact and demonstrate successful manipulation where a kinematic-only baseline fails. We also use the pipeline as a data generation engine to train policies that achieve the tasks in a closed-loop manner. Project website, videos, and dataset: https://dreamingcontactsound.github.io/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。