---
title: "Deep Learning-Based Detection of Electrical Faults and Power Quality Disturbances in Aerospace Power Systems"
date: 2026-09-11T05:41:26+08:00
draft: false
entry_kind: "auto"
tags: ["深度学习", "eess.SP", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:48a389873f0c29ddd2c080d10413f497d90426eeb86ea16ede411a09d40c3696"
source_payload_sha256: "sha256:76e993d4e6b2a26643aa84cccf59ab22e3f97f0faa36b5c6adfa47728581796a"
observation_id: obs_58489fe3c32482de40823fc0d097e121baadc39b0477a78dca8633fd723f77a7
event_id: evt_8767ec1c851a3e9ab6bc953c29df979ed656a19608a0096e56c9411bb80926ea
revision_id: rev_733bbb836afbaac4c27dbb117906d6860824fd47f46b50037c3ebbeee6d118d1
source_published_at: 2026-09-09T17:19:14Z
first_seen_at: 2026-09-10T21:37:56.640868Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.10479v1
parent_observation_id: null
last_seen_at: 2026-09-10T21:37:56.640868Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.10479v1](http://arxiv.org/abs/2609.10479v1)
- **发布域名**: arxiv.org
- **分类**: eess.SP
- **作者**: Ian C. Guzmán、Radu Babiceanu、Berker Peköz

## 来源摘要/节选

> More Electric Aircraft require fast and reliable monitoring of high-frequency electrical networks, yet most power quality disturbance and fault diagnosis methods are developed for conventional 50 or 60 Hz grids. This work presents a hardware-aware deep learning framework for multiclass detection of electrical faults and power quality disturbances in a 400 Hz aerospace power system. A high-fidelity simulation model inspired by the Boeing 787 electrical architecture generates voltage and current waveforms for 21 normal, disturbance, switching, open-circuit, and short-circuit conditions. Two datasets, each containing 73,500 samples, are formed from one-dimensional time-series signals and short-time Fourier transform time-frequency representations. Signal-processing augmentation, domain randomization, and class-specific generative adversarial networks increase waveform diversity, and the time-series dataset is released through IEEE DataPort. We compare 1D and 2D convolutional neural networks, long short-term memory networks, CNN-LSTM hybrids, ResNet, MobileNet, and VGG models under common training conditions. A compact ResNet provides the best accuracy-complexity tradeoff, achieving 96.94 percent software test accuracy with 175,685 parameters. After 8-bit quantization and deployment on a Xilinx Zynq UltraScale Plus MPSoC ZCU102, the model achieves 95.87 percent accuracy and a measured mean neural-network accelerator latency of 6.90 ms per input record. The results establish simulation-based, accelerator-level feasibility for embedded edge AI in aircraft electrical health monitoring and motivate future end-to-end data acquisition and experimental validation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。