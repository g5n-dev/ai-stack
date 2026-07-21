---
title: 'ZipMap: Linear-Time Stateful 3D Reconstruction with Test-Time Training'
date: 2026-03-05 20:54:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.04385v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:510cee691519648939890622947580b0af100e09674b329bb3b7ff345207ea0b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:27:08.846828Z'
source_capture_sha256: sha256:18605e00066f3176e8a321dd9cf0ca8d3404b901eef7d58ce16d65b191716f59
source_capture_chars_original: 1003
source_publication_excerpt_chars: 1003
observation_id: obs_7887e170e47f9e7d6361188c0cac334bab31c7870ae38545788424415f87745e
revision_id: rev_08754bb4b82c25f7fa65a5b1e406b1c3ca4bb992f8d506308a750dfbdd04e2d7
event_id: evt_61e8e210378df5dffe9da779b0025481ccb041bf1c9715557a56acd258d15fe8
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-05T22:01:23Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.04385v1](<https://arxiv.org/abs/2603.04385v1>)
- **作者**: Haian Jin, Rundi Wu, Tianyuan Zhang, Ruiqi Gao, Jonathan T. Barron, Noah Snavely, Aleksander Holynski
- **分类**: cs.CV
- **论文时间**: 2026-03-04T18:49:37Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.04385v1.pdf](<https://arxiv.org/pdf/2603.04385v1.pdf>)

## 来源摘要/节选

> Feed-forward transformer models have driven rapid progress in 3D vision, but state-of-the-art methods such as VGGT and $π^3$ have a computational cost that scales quadratically with the number of input images, making them inefficient when applied to large image collections. Sequential-reconstruction approaches reduce this cost but sacrifice reconstruction quality. We introduce ZipMap, a stateful feed-forward model that achieves linear-time, bidirectional 3D reconstruction while matching or surpassing the accuracy of quadratic-time methods. ZipMap employs test-time training layers to zip an entire image collection into a compact hidden scene state in a single forward pass, enabling reconstruction of over 700 frames in under 10 seconds on a single H100 GPU, more than $20\\times$ faster than state-of-the-art methods such as VGGT. Moreover, we demonstrate the benefits of having a stateful representation in real-time scene-state querying and its extension to sequential streaming reconstruction.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
