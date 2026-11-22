---
title: "Bio-PM-Guided Synthetic IMU Generation"
date: 2026-11-22T11:11:17+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:813d931c724ac391150a3ac6aab658a57bf942127f22582ea13368ecc25cfd81"
source_payload_sha256: "sha256:c5e2ae652ca8c5e36aa1ed725d97febc9c27f80c0573b0e3c6621d4f11141649"
observation_id: obs_6ec98b90f583a282500f2bc2198c561cbf264e8c3e0746add2f7d6aec6b48f94
event_id: evt_a3dc0d3c2055297ef90934eb7836bd213b47c1a157a8d5ae3e5741819aeffde1
revision_id: rev_f50f8abac9a12f6753f1a7d8fa8239dd7dd854627612298773972a722aeda23e
source_published_at: 2026-11-19T18:56:25Z
first_seen_at: 2026-11-22T03:10:08.163659Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 38
interpretation_sha256: "sha256:23130f5c006c09415aa8a523418423d34460544168d2a17e4f65f8a203d55786"
description: "研究在预训练生物信号编码器 Bio-PM 的表示空间中生成合成 IMU 数据，分别采用自回归 Transformer 和扩散解码器生成类别条件 token 序列，并评估其真实性及对下游分类的帮助。"
external_url: http://arxiv.org/abs/2611.26607v1
parent_observation_id: null
last_seen_at: 2026-11-22T03:10:08.163659Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26607v1](http://arxiv.org/abs/2611.26607v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Deepali Singh、Deepesh Parpani、Aviral Gupta

## 要点解读

### 这是什么
研究在预训练生物信号编码器 Bio-PM 的表示空间中生成合成 IMU 数据，分别采用自回归 Transformer 和扩散解码器生成类别条件 token 序列，并评估其真实性及对下游分类的帮助。

### 用在哪里
适用于采集和标注 IMU 人体活动识别数据成本较高、需要改善跨个体泛化的场景。生成的 token 可用于训练数据增强，并与重力感知特征结合以提升活动分类效果。

### 可以推断的
- 推测：在表示空间生成数据，可能比直接生成原始信号更容易保留与活动类别相关的结构。
- 推测：对于动态相似或跨个体差异较大的活动，定向的数据增强可能更有助于分类器泛化。

## 来源摘要/节选

> Collecting and labeling inertial measurement unit (IMU) data for human activity recognition (HAR) is expensive, and models trained on one group of subjects often fail to generalize to unseen individuals. Even with balanced data, classifiers struggle to distinguish dynamically similar activity classes and benefit from targeted augmentation. We explore whether synthetic IMU data generated in the representation space of a pretrained biosignal encoder, Bio-PM \cite{b1}, can serve as a practical augmentation source. Rather than synthesizing raw signals, we leverage Bio-PM's frozen encoder to convert 10-second IMU windows into token embedding sequences and train class-conditional decoders in this space: (1) an autoregressive transformer decoder that predicts tokens sequentially, and (2) a diffusion decoder that learns the token distribution through a denoising objective. We analyze generation realism through distributional metrics and embedding-space visualizations, evaluate downstream utility through leave-one-subject-out HAR classification, and present a PatchDecoder for approximate raw waveform reconstruction. Our diffusion decoder achieves a Train-on-Synthetic-Test-on-Real (TSTR) macro-F1 of 0.68, demonstrating that generated tokens are realistic enough to train a classifier that transfers to real data. Combining synthetic-token augmentation with a 320-dimensional gravity-aware feature representation raises LOSO macro-F1 from 0.729 to 0.809 over a real-only baseline across 51 subjects on the WISDM benchmark, with statistically significant gains concentrated in the most challenging activity classes. These results demonstrate that high-fidelity generation in a pretrained encoder's representation space is achievable and practically useful for cross-subject HAR augmentation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。