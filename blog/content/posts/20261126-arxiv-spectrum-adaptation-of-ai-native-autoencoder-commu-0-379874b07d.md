---
title: "Spectrum Adaptation of AI-Native Autoencoder Communications with Transfer Learning"
date: 2026-11-26T13:01:54+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.NI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8ab5d9e17df6b2f1b8538cb86402215329a2ddea0b971f0ce0fa0aedae5a0874"
source_payload_sha256: "sha256:396b988074d6fb0770dcbbf9f984d538053f6abb94d5715a7660b00aba66ef1a"
observation_id: obs_379874b07d1f442cab9ae511af4d68a0aee1fd36880937393292c3083c8baf5a
event_id: evt_2c2b49b08a3e6a1207aecd04e70047ed6f8916a0cafa474865887377bd65b4c7
revision_id: rev_af11ec624928ebc030c39c7bb6c9045e2823799fcbf1a05183a8f97522b6ef79
source_published_at: 2026-11-25T18:59:57Z
first_seen_at: 2026-11-26T05:00:40.404336Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
interpretation_sha256: "sha256:eb209382537697fc1497d96d6de17ad26ad99065bb1ba572e1df85c8e9e2b3be"
description: "该研究针对物理层自编码器通信在训练信道与实际信道不一致时误码率恶化的问题，提出迁移学习式适配方法：从 AWGN 预训练模型出发，仅更新部分收发端层，其余参数保持冻结。"
external_url: http://arxiv.org/abs/2611.34942v1
parent_observation_id: null
last_seen_at: 2026-11-26T05:00:40.404336Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.34942v1](http://arxiv.org/abs/2611.34942v1)
- **发布域名**: arxiv.org
- **分类**: cs.NI
- **作者**: Yalin E. Sagduyu、Tugba Erpek

## 要点解读

### 这是什么
该研究针对物理层自编码器通信在训练信道与实际信道不一致时误码率恶化的问题，提出迁移学习式适配方法：从 AWGN 预训练模型出发，仅更新部分收发端层，其余参数保持冻结。

### 用在哪里
适用于需要在 Rayleigh 衰落及射频前端损伤等实际条件下调整 AI 原生通信系统的人，尤其适合关注低时延、低训练开销和受限计算资源的场景。

### 可以推断的
- 推测：相较于每次从头训练，局部层微调可能更适合信道条件频繁变化但计算资源有限的通信系统。
- 推测：该方法也可用于其他存在训练—部署环境差异的自编码器任务，但实际效果仍取决于任务与适配条件。

## 来源摘要/节选

> End-to-end physical-layer learning replaces separate modulation, coding, and detection operations with an autoencoder (AE) that consists of a jointly trained encoder-decoder pair at the transmitter and the receiver. This paper studies AI-native communications with AEs and quantifies the sensitivity to training-test mismatch in channel models. Models trained only on an AWGN channel achieve low bit error rates (BERs) under matched conditions but degrade severely on Rayleigh fading with practical front-end impairments. To reduce the time and energy required to adapt to new channel conditions, we propose a low-latency transfer-learning procedure that starts from an AWGN-pretrained system and fine-tunes only a small subset of transmitter and receiver layers while freezing the remainder. We further formulate layer selection as a budget-constrained optimization problem that identifies the most informative parameters to update during adaptation. This preserves the learned signal geometry and the deep decision structure while adapting lightweight front ends to fading- and impairment-induced mixing. For AE communications, we show that partial updates remove the mismatch-induced error floor and approach the BER of fully retrained models. We provide a layer-wise study and quantify resource-performance trade-offs, showing that modest adaptation substantially reduces BER while cutting training time, multiply-accumulate (MAC) operations, energy consumption, and the fraction of updated parameters for resource-efficient implementation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。