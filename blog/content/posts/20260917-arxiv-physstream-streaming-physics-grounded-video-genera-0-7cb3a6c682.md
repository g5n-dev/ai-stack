---
title: "PhysStream: Streaming Physics-Grounded Video Generation with Structured Scene Memory and Fine-Grained Motion Control"
date: 2026-09-17T06:59:28+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:48ff022044bd9fb421b35677f9b87a8027ddaefd9756af587b2c41eca7b17ab0"
source_payload_sha256: "sha256:664b557524659876028e4e300c9c141fd5f19892558b80da1676a0a0f4969f49"
observation_id: obs_7cb3a6c68227e8b7371b89c1ac7fc8dd45e28596157c752b06812df500c38231
event_id: evt_64f937e727bb5963c60a8267e9512a28f62f72eac28418df006ffc5696d9c333
revision_id: rev_3b6f0116746d575ded1054de9f147b6f1766be6791cf798d0364e937de8fae04
source_published_at: 2026-09-15T17:55:13Z
first_seen_at: 2026-09-16T22:56:21.108006Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 116
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.17521v1
parent_observation_id: null
last_seen_at: 2026-09-16T22:56:21.108006Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.17521v1](http://arxiv.org/abs/2609.17521v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Chuhao Chen、Peter Wonka、Chaoyang Wang 等

## 来源摘要/节选

> Interactive control for video generation is moving from coarse prompts toward fine-grained, physically meaningful manipulation of dynamic scenes. Yet existing controllable methods either require the full control schedule before generation starts, or use pixel-space signals that dictate object positions rather than physical dynamics. To address these limitations, we propose PhysStream, an autoregressive model for physics-grounded image-to-video synthesis that incorporates structured scene memory---positional maps and object tracking maps derived online from previously generated frames---and supports fine-grained motion control via sparse velocity-increment signals that encode physical quantities, letting the model learn the underlying dynamics. We train our model in two stages: a bidirectional model is first finetuned with motion-control conditioning, then a causal autoregressive model is trained with additional structured scene memory, further improving physical consistency. PhysStream enables interactive, mid-generation control over multi-object tabletop rigid-body scenes---a capability not supported by prior methods---reducing motion distribution distance (FVMD) by 33% and trajectory error by 12% over the strongest baselines on synthetic benchmarks, and is preferred by human evaluators in over 85% of in-the-wild comparisons. Please check our website for more details: https://czzzzh.github.io/PhysStream

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。