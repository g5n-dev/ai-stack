---
title: Lightweight User-Personalization Method for Closed Split Computing
date: 2026-03-17 03:25:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.14958v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:841d6488eacb36a5146c4338aa6276116ee3b7f4447f4174c4114fb881223cd1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:28:34.236322Z'
source_capture_sha256: sha256:02625062ae01618ea5c74e2496ab9e642483b50aeb64effe3be9deff4de2d540
source_capture_chars_original: 1639
source_publication_excerpt_chars: 1639
observation_id: obs_373b2ee70ffb271235b294375c02e13571dd1a165580f3c2c36f707a0cbd015e
revision_id: rev_9850a1c8f0949622aa2e7b0eaa04cd7d6c8727e61c6e7b44640c4305dd8fcaf4
event_id: evt_7448b56ed7a15e5b07e9b6bd30e2b35f6d36106b41af15d2ab9c470e89052e16
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.14958v1](<https://arxiv.org/abs/2603.14958v1>)
- **作者**: Yuya Okada, Takayuki Nishio
- **分类**: cs.LG
- **论文时间**: 2026-03-16T08:16:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.14958v1.pdf](<https://arxiv.org/pdf/2603.14958v1.pdf>)

## 来源摘要/节选

> Split Computing enables collaborative inference between edge devices and the cloud by partitioning a deep neural network into an edge-side head and a server-side tail, reducing latency and limiting exposure of raw input data. However, inference performance often degrades in practical deployments due to user-specific data distribution shifts, unreliable communication, and privacy-oriented perturbations, especially in closed environments where model architectures and parameters are inaccessible. To address this challenge, we propose SALT \(Split-Adaptive Lightweight Tuning\), a lightweight adaptation framework for closed Split Computing systems. SALT introduces a compact client-side adapter that refines intermediate representations produced by a frozen head network, enabling effective model adaptation without modifying the head or tail networks or increasing communication overhead. By modifying only the training conditions, SALT supports multiple adaptation objectives, including user personalization, communication robustness, and privacy-aware inference. Experiments using ResNet-18 on CIFAR-10 and CIFAR-100 show that SALT achieves higher accuracy than conventional retraining and fine-tuning while significantly reducing training cost. On CIFAR-10, SALT improves personalized accuracy from 88.1% to 93.8% while reducing training latency by more than 60%. SALT also maintains over 90% accuracy under 75% packet loss and preserves high accuracy \(about 88% at sigma = 1.0\) under noise injection. These results demonstrate that SALT provides an efficient and practical adaptation framework for real-world Split Computing systems.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
