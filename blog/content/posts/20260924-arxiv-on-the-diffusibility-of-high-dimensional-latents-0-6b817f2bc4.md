---
title: "On the Diffusibility of High-Dimensional Latents"
date: 2026-09-24T12:51:57+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a52d37a091e966942a20229c6a82e6acb2c9675b8b633480f37c6979d49e0af2"
source_payload_sha256: "sha256:a635d96745e6540d77e5080f65c7188877c787f856f937c7f78e15d5d80b74e4"
observation_id: obs_6b817f2bc4e02aea4826074607cd0f2316da75c5f28a19039eb5302e96059ceb
event_id: evt_e3a48130be432146ca9e44c2d0df211176fff9824b16bd336f81840b89f2e711
revision_id: rev_ed14995f102f38cbb3cce550df29da682564d119060c4fd6fde70558492765c1
source_published_at: 2026-09-23T17:59:56Z
first_seen_at: 2026-09-24T04:48:34.540444Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
interpretation_sha256: "sha256:caaac3c275901e6e78d743906ff22bf40fa3a1e17feb4f3eeb8d6776e8e3e006"
description: "- 该研究指出，对用于图像重建的预训练视觉编码器进行微调会压缩其表示的有效维度，进而影响扩散模型在高层特征空间中的生成效率。 - 为解决这一问题，文中建议在高层空间中放弃常规的速度预测，转而采用直接预测原始数据的 x₀ 参数化，使学习集中在信号流形上。"
external_url: http://arxiv.org/abs/2609.28473v1
parent_observation_id: null
last_seen_at: 2026-09-24T04:48:34.540444Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.28473v1](http://arxiv.org/abs/2609.28473v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Chao Feng、Zhiyang Xu、Bowei Chen 等

## 要点解读

### 这是什么  
- 该研究指出，对用于图像重建的预训练视觉编码器进行微调会压缩其表示的有效维度，进而影响扩散模型在高层特征空间中的生成效率。  
- 为解决这一问题，文中建议在高层空间中放弃常规的速度预测，转而采用直接预测原始数据的 x₀ 参数化，使学习集中在信号流形上。

### 用在哪里  
- 适用于在文本转图像生成任务中结合预训练视觉编码器与扩散模型的研究团队。  
- 对关注表征维度变化对生成质量和训练效率影响的开发者也有参考价值。

### 可以推断的  
- 推测：在高层特征空间里，优化目标的选择对收敛速度和最终效果有显著影响。  
- 推测：x₀ 参数化在类似的表示压缩场景中可能带来更稳定的训练过程。

## 来源摘要/节选

> Representation Autoencoders (RAEs) enable diffusion models to operate in the feature spaces of pretrained visual encoders. However, many off-the-shelf encoders are not optimized for faithful reconstruction, discarding fine-grained visual details. As expected, finetuning these encoders for image reconstruction recovers such details. However, perhaps counterintuitively, this procedure reduces the effective dimensionality of the resulting representation, and the altered geometry has downstream effects on generation. Specifically, we show that using the standard velocity prediction in flow matching in this high-dimensional space requires the model to fit orthogonal noise directions outside the low-dimensional signal manifold, making optimization inefficient. This motivates using the clean data parameterization ($\boldsymbol{x}_{0}$-prediction) instead, which focuses learning on the underlying signal manifold. Across experiments with multiple strong-reconstruction encoders, we show that $\boldsymbol{x}_{0}$-prediction consistently improves text-to-image generation performance.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。