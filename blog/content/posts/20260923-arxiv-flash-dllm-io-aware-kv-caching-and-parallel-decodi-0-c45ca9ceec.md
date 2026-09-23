---
title: "Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs"
date: 2026-09-23T14:01:21+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f98bdd8167cabfcbefdc3c87e300d2189df992feed10acbf10377097b2dc82f1"
source_payload_sha256: "sha256:36d9260015e510c4d871dfaca9e84cb579478d2d33456f51de52ba2779e57cd8"
observation_id: obs_c45ca9ceec83f5bcf4f447fffad2e57ed68001231a537be0cfc8500ed37b2dc9
event_id: evt_84aa093610752f16d5c8fca4804b6b78780d4ed57ede5ce9bdae9e49965058c4
revision_id: rev_e4f7d9ea0f64b0b501f4cbeb58bc98845d6fb1c859d80e4ecec6c85a8013b180
source_published_at: 2026-09-22T17:59:57Z
first_seen_at: 2026-09-23T06:12:07Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:8a94754890bec2d3c9adb4a247566d5f2a825b536939a3a6ffa237a039257344"
description: "该内容介绍了一种无需额外训练即可加速扩散语言模型推理的框架。它通过 I/O 感知的融合 KV‑缓存内核降低冗余内存搬运，并利用模型自身承担起草和验证的并行解码，实现更快的生成速度和更低的显存占用。"
external_url: http://arxiv.org/abs/2609.26796v1
parent_observation_id: null
last_seen_at: 2026-09-23T05:58:23.026959Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.26796v1](http://arxiv.org/abs/2609.26796v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Quan Nguyen-Tri、Mukul Ranjan、Zhiqiang Shen

## 要点解读

### 这是什么
该内容介绍了一种无需额外训练即可加速扩散语言模型推理的框架。它通过 I/O 感知的融合 KV‑缓存内核降低冗余内存搬运，并利用模型自身承担起草和验证的并行解码，实现更快的生成速度和更低的显存占用。

### 用在哪里
适用于在 GPU 环境下部署扩散语言模型进行文本生成的研究者和工程师，尤其在需要提升推理吞吐量或降低显存占用的场景，如大规模并行生成或长序列任务。

### 可以推断的
推测：该方案的效果高度依赖于 GPU 内存带宽和缓存层级，可能在带宽受限的硬件上收益有限。  
推测：由于不需要辅助模型或额外训练，可直接嵌入现有推理引擎，便于快速原型和实验。

## 来源摘要/节选

> Diffusion Large Language Models (dLLMs) have recently emerged as a promising alternative to autoregressive LLMs by enabling non-autoregressive text generation. However, their practical deployment remains limited by inefficient inference, largely due to the absence of effective Key-Value (KV) caching and scalable parallel decoding mechanisms. Existing acceleration methods typically study KV caching and parallel decoding in isolation, overlooking the I/O bottlenecks that arise when cache reuse and parallel token verification are jointly applied. In this work, we introduce $\textbf{Flash-dLLM}$, a training-free inference acceleration framework for fast and memory-efficient dLLMs. Flash-dLLM first identifies GPU memory I/O as a dominant bottleneck in KV-cache-enabled dLLM inference and addresses it with an I/O-aware fused KV-cache kernel that reduces redundant memory movement. Building on this optimized cache mechanism, Flash-dLLM further proposes an efficient KV-cache-driven draft-and-verify decoding strategy, where the dLLM itself serves as both drafter and verifier without requiring an auxiliary model. This unified design enables faster decoding while preserving generation quality and improving scalability to longer sequences and larger batch size. Extensive experiments on mathematical reasoning and code-generation benchmarks demonstrate that Flash-dLLM consistently outperforms existing state-of-the-art dLLM acceleration methods in both inference speed and memory efficiency. In particular, it achieves $5.1\times$ and $11.0\times$ speedups over prior strongest baseline Elastic-Cache on GSM8K and HumanEval, respectively.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。