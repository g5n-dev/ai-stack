---
title: "MeanFlowNFT: Bringing Forward-Process RL to Average-Velocity Generators"
date: 2026-07-18T06:09:31+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b9611bace4203fb8055ba0c9cb0a92b92450c884fd869c734cd92c3bc2e39650"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.15273v1
observation_id: obs_ae3c665a0d7ffba7d40a732b8fb67d27129d44cbd908ca1c3aa19723d8afb90a
revision_id: rev_87af617e01a5483e64ee7d779b8e6b031e9176ecdc353de976a3d541118f4685
event_id: evt_e69759416757c39a807a03e0c0b16e71f4488e1d5ee23dfdf032cd0d236a3a1a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-17T22:11:02Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.15273v1](http://arxiv.org/abs/2607.15273v1)

## 来源摘要/节选

> MeanFlow generators achieve fast few-step sampling by predicting average velocities over time intervals, making them attractive for efficient generation. Reinforcement learning (RL) has become a powerful way to align diffusion and flow models with human preferences and task-specific objectives. In particular, DiffusionNFT offers an efficient forward-process RL framework that does not require reverse-process trajectories or likelihood estimation. However, applying such RL methods to MeanFlow remains underexplored. DiffusionNFT optimizes instantaneous velocities, whereas MeanFlow samples with average velocities. To bridge this gap, we introduce MeanFlowNFT. Inspired by the MeanFlow identity, which bridges average and instantaneous velocities, we construct an induced instantaneous-velocity predictor. We apply the DiffusionNFT objective to this predictor, making reward optimization well-defined for MeanFlow. Sampling remains based on the average velocity, preserving MeanFlow's fast few-step generation. We further prove that MeanFlowNFT inherits DiffusionNFT's strict policy-improvement guarantee. Experiments on image and video generation show that MeanFlowNFT consistently improves baselines. Moreover, it outperforms prior state-of-the-art RL-tuned few-step generators on most metrics ($6$ of $8$ on SD3.5-M), and can even surpass multi-step RL-tuned diffusion while using only a few sampling steps. For instance, on Wan 2.1, $4$-step MeanFlowNFT reaches a VBench score of $84.33$, surpassing $50$-step LongCat-Video RL ($82.57$).

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。