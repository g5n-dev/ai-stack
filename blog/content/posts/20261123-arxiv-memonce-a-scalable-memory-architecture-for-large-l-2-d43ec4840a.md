---
title: "MemOnce: A Scalable Memory Architecture for Large Language Models"
date: 2026-11-23T17:01:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2e199caeb735c41d59b5b8ff7895da77f0b30a426fd51189f27f765e9ca00cdc"
source_payload_sha256: "sha256:703c038b7af28f6bb6568aef36c9e166a8db01d116d8540914372b980b155f0e"
observation_id: obs_d43ec4840a23ed16923215a7f5983744f593890d4f947024b519f1c7efdaf903
event_id: evt_430e34f4b1cc1178c17e04a7eb875790b6af77d65449e485503fdb496dba50b5
revision_id: rev_05b1a5663252764e6348472e515445ccd2014a3b7ae8a07cd16b7449da21450e
source_published_at: 2026-11-20T18:51:29Z
first_seen_at: 2026-11-23T09:13:15Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:2430e8b3d806a22827d5b915ddb670b71fafacc49179a2b0a4f437dac66c212b"
description: "MemOnce 是一种面向大语言模型的可扩展记忆架构，通过压缩并按需恢复记忆状态，减少 KV 缓存带来的显存占用与计算开销。"
external_url: http://arxiv.org/abs/2611.27973v1
parent_observation_id: null
last_seen_at: 2026-11-23T09:00:27.718221Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.27973v1](http://arxiv.org/abs/2611.27973v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Chang Nie、Chaoyou Fu、Songlin Liu 等

## 要点解读

### 这是什么
MemOnce 是一种面向大语言模型的可扩展记忆架构，通过压缩并按需恢复记忆状态，减少 KV 缓存带来的显存占用与计算开销。

### 用在哪里
它适用于需要超长上下文、持续交互或长期复用历史状态的应用，例如长时间运行的模型服务、记忆资源受限的部署环境，以及需要兼顾吞吐和响应速度的推理系统。

### 可以推断的
- 推测：该架构可能特别适合需要在高并发服务中控制显存占用的团队。
- 推测：其稀疏注意力机制可能有助于降低长上下文检索时的延迟。

## 来源摘要/节选

> Deploying large language models (LLMs) in long-horizon and continual interactions requires maintaining reusable memory states for future inference, posing challenges for existing architectures. Standard Transformers accumulate layer-wise, token-level KV caches, incurring linear GPU memory growth and quadratic computational complexity as the context expands. In contrast, linear-time architectures compress history into fixed-size states, but struggle to retain fine-grained details. We introduce MemOnce, a foundation architecture that learns scalable memory states for language models. MemOnce is based on two core designs: (a) Memory encoder-decoder: it caches only a small subset of final-layer hidden states as compact memory representations and dynamically decodes them back into KV caches for attention layers; (b) Memory sparse attention: for each continual input, MemOnce adaptively retrieves relevant memory representations, with the sparse indices computed only once across layers. Coupling these two designs enables efficient on-the-fly memory loading and KV cache decoding, drastically reducing the GPU memory footprint and achieving linear-time complexity. We conduct extensive experiments to show that MemOnce outperforms Transformers and other architectures across varying model sizes, context lengths, and training paradigms (pretraining and post-training adaptation). In particular, adapting Qwen3.5-4B with MemOnce reduces memory state cache by 1313$\times$ and prefill latency by 6.9$\times$ at 1M context, and improves throughput by 3.5$\times$ and overall memory performance by +5.77%. Finally, MemOnce generalizes zero-shot to downstream representation tasks, achieving competitive results against specialized models.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。