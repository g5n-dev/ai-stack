---
title: "AD-WM: Action-Discriminative World Models for Counterfactual Model Predictive Control"
date: 2026-09-25T21:49:34+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b1be16fed0a17ee89dc97b31a51ced55f2382113f8adb7a87c2b28e8c21504fc"
source_payload_sha256: "sha256:83ca1412c3ee07170682ff5d4d997469e6bbfd7cf8e901d6dd5afaae49af4d15"
observation_id: obs_ca8e22822c4fa752ce3fdc15484d46a322b53bf6a1d48e9fbcf57a80fa264c35
event_id: evt_56eddef13518a014afb4b25b640ecea32ae96444675765809443e8da60f3bc4b
revision_id: rev_13f671170e06efecbfe306906c381d3e295712f32759c0f399dc895d6baf5fdb
source_published_at: 2026-09-24T17:59:41Z
first_seen_at: 2026-09-25T14:00:51Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.30264v1
parent_observation_id: null
last_seen_at: 2026-09-25T13:46:23.046294Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30264v1](http://arxiv.org/abs/2609.30264v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Jiabin Qiu、Zixuan Chen、Hongye Cao 等

## 来源摘要/节选

> Latent world models are typically trained to predict factual transitions, whereas model predictive control (MPC) must compare alternative actions from the same state. A model can therefore achieve low factual prediction error yet poorly distinguish candidate actions. We introduce AD-WM, an action-discriminative joint-embedding world model for counterfactual MPC. AD-WM combines residual latent dynamics with predictor-level action-recovery regularization, using inverse dynamics and a normalized recovery objective motivated by conditional mutual information. Both objectives encourage planning transitions to preserve action information; their auxiliary heads are discarded at test time, leaving MPC unchanged. On OGBench-Cube, AD-WM improves hard-start success from 3.7% to 52.0% over a matched LeWM baseline and improves mean success over the reproduced baseline in four of five simulation environments. Planning diagnostics show that factual prediction error and whole-bank action ranking do not follow the closed-loop success ordering, whereas CEM-aligned elite regret tracks success more closely. With a frozen V-JEPA 2 encoder and matched DROID post-training, AD-WM also improves zero-shot transfer to our Franka setup, increasing basic pick-and-place success from 42.2% to 71.1% without lab-specific adaptation. These results suggest that world models for planning should preserve action-dependent differences needed for counterfactual selection, rather than optimize factual prediction accuracy alone. More videos and code are available at https://ad-wm.github.io/.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。