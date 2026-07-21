---
title: 'Scaling Vision Transformers: Evaluating DeepSpeed for Image-Centric Workloads'
date: 2026-02-25 02:57:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21081v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1828795790169ff823aeec7f58e7067ee0f745c7217ef73e8c5d714f72833d8d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:16:57.484529Z'
source_capture_sha256: sha256:4c9f28459e8f8f36555564b8696a103762ebad7aed6865b438b16d85960d4b8e
source_capture_chars_original: 1254
source_publication_excerpt_chars: 1254
observation_id: obs_fa2c4947ffe7c25fc8352c1abcf5e6c1cca8e971dcd953c3d901f1cd120d4066
revision_id: rev_c887c038bfdbf679c0f8281e4c064b41022b1b74ebcc27bca499a14fdf78f9f9
event_id: evt_c3891ae3c91955f94002df47db4ea413672ee6c6c5cc3856f7dc28b6e59125c1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T03:56:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21081v1](<https://arxiv.org/abs/2602.21081v1>)
- **作者**: Huy Trinh, Rebecca Ma, Zeqi Yu, Tahsin Reza
- **分类**: cs.LG
- **论文时间**: 2026-02-24T16:45:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21081v1.pdf](<https://arxiv.org/pdf/2602.21081v1.pdf>)

## 来源摘要/节选

> Vision Transformers \(ViTs\) have demonstrated remarkable potential in image processing tasks by utilizing self-attention mechanisms to capture global relationships within data. However, their scalability is hindered by significant computational and memory demands, especially for large-scale models with many parameters. This study aims to leverage DeepSpeed, a highly efficient distributed training framework that is commonly used for language models, to enhance the scalability and performance of ViTs. We evaluate intra- and inter-node training efficiency across multiple GPU configurations on various datasets like CIFAR-10 and CIFAR-100, exploring the impact of distributed data parallelism on training speed, communication overhead, and overall scalability \(strong and weak scaling\). By systematically varying software parameters, such as batch size and gradient accumulation, we identify key factors influencing performance of distributed training. The experiments in this study provide a foundational basis for applying DeepSpeed to image-related tasks. Future work will extend these investigations to deepen our understanding of DeepSpeed's limitations and explore strategies for optimizing distributed training pipelines for Vision Transformers.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
