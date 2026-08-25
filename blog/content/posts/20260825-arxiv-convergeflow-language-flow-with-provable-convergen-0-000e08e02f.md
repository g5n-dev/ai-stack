---
title: "ConvergeFlow: Language Flow with Provable Convergence to Token Embeddings"
date: 2026-08-25T19:46:16+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7dc10de16cfd9b6b229b4b60dd7e87211d090cf8d8a18c7f5439a4a3e9b06af1"
source_payload_sha256: "sha256:cdd619da2668fd5bcfc5d64b1bb86a13a3c9a232913f3e09e936c9649fe7ff50"
observation_id: obs_000e08e02f99ed7ccd97191a2cd2d53315346bb394204dde5b5b11ffb2d5964c
event_id: evt_5d3f0430dd910e03730ceec09f934c7f65774a6e14afa5826834efd857ef09de
revision_id: rev_f2149986431436ab0675b57423e754e7fa8680876b3107dc1320ff55321d9f8d
source_published_at: 2026-08-24T17:54:14Z
first_seen_at: 2026-08-25T17:45:45.166136Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:88c82ee3badbc5f9d6c3c11f98092a632d0c8062377859d578d3367aba3f8083"
description: "ConvergeFlow 是一种在嵌入空间进行流式建模的语言模型，它把数据预测器限制在词向量凸包内，仅使用流匹配诱导的均方误差进行训练，实现流向有效词向量的收敛，从而可以在不依赖交叉熵监督解码器的情况下直接预测词。"
external_url: http://arxiv.org/abs/2608.23551v1
parent_observation_id: null
last_seen_at: 2026-08-25T11:43:10.090779Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23551v1](http://arxiv.org/abs/2608.23551v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Na Li、Yuchen Jiao、Changxiao Cai 等

## 要点解读

### 这是什么
ConvergeFlow 是一种在嵌入空间进行流式建模的语言模型，它把数据预测器限制在词向量凸包内，仅使用流匹配诱导的均方误差进行训练，实现流向有效词向量的收敛，从而可以在不依赖交叉熵监督解码器的情况下直接预测词。

### 用在哪里
该研究适用于从事文本生成和流模型研究的科研人员与工程师，尤其是想摆脱对交叉熵解码器依赖、探索连续扩散与流式语言模型实际应用的人群。

### 可以推断的
推测：在保持生成质量的前提下，使用均方误差训练可能简化模型的优化过程并提升训练稳定性。  
推测：该方法的收敛保证如果在更大规模数据或更长序列上得到验证，可能为工业级流式文本生成系统提供可行的技术路径。

## 来源摘要/节选

> Recent advances in continuous diffusion and flow-based language models (LMs) have achieved performance competitive with discrete LMs. However, existing continuous frameworks still rely on decoders supervised with cross entropy (CE) because the flow trajectories are not guaranteed to terminate at valid token embeddings. Motivated by this limitation, we introduce \textbf{ConvergeFlow}, an embedding-space flow-based LM, which constrains the data predictor to the convex hull of token embeddings and trains it solely with the mean squared error objective induced by flow matching. Under suitable regularity conditions, we prove that the resulting flow converges to valid token embeddings despite errors in the data predictor, enabling direct token prediction without a CE-supervised decoder. We further develop three sampling mechanisms for controlling the trade-off between the generative perplexity and entropy. Experiments on OpenWebText demonstrate that ConvergeFlow achieves performance competitive with existing continuous and discrete diffusion LMs. These findings demonstrate the potential of the flow-based paradigm for language modeling. Our code is available at https://github.com/Na-Li66/ConvergeFlow.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。