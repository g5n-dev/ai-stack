---
title: Towards Real-Time ECG and EMG Modeling on $μ$ NPUs
date: 2026-04-21 02:50:20+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2604.18067v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:db9f2091f720744c0c82b88cd8fdf79a8acf0940d95b61530f19a87d37e65b95
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 50
captured_at: '2026-07-18T04:29:16.028975Z'
source_capture_sha256: sha256:dce8d65260a1a50c52563d48490f2c97e1146651b394e991af4d7882e8aaba6d
source_capture_chars_original: 1243
source_publication_excerpt_chars: 1243
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.18067v1](<https://arxiv.org/abs/2604.18067v1>)
- **作者**: Josh Millar, Ashok Samraj Thangarajan, Soumyajit Chatterjee, Hamed Haddadi
- **分类**: cs.LG
- **论文时间**: 2026-04-20T10:35:33Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.18067v1.pdf](<https://arxiv.org/pdf/2604.18067v1.pdf>)

## 来源摘要/节选

> The miniaturisation of neural processing units \(NPUs\) and other low-power accelerators has enabled their integration into microcontroller-scale wearable hardware, supporting near-real-time, offline, and privacy-preserving inference. Yet physiological signal analysis has remained infeasible on such hardware; recent Transformer-based models show state-of-the-art performance but are prohibitively large for resource- and power-constrained hardware and incompatible with $μ$ NPUs due to their dynamic attention operations. We introduce PhysioLite, a lightweight, NPU-compatible model architecture and training framework for ECG/EMG signal analysis. Using learnable wavelet filter banks, CPU-offloaded positional encoding, and hardware-aware layer design, PhysioLite reaches performance comparable to state-of-the-art Transformer-based foundation models on ECG and EMG benchmarks, while being &lt;10% of the size \($\\sim$370KB with 8-bit quantization\). We also profile its component-wise latency and resource consumption on both the MAX78000 and HX6538 WE2 $μ$ NPUs, demonstrating its viability for signal analysis on constrained, battery-powered hardware. We release our model\(s\) and training framework at: https://github.com/j0shmillar/physiolite.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
