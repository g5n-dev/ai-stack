---
title: "PDMD: Projected Distribution Matching Distillation for Video Diffusion Models"
date: 2026-09-30T04:48:56+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f2194ddc4a6c996aeec4f727d6d0db22839e73d2d4a5329e722af72237230380"
source_payload_sha256: "sha256:8c398dbe7e9cc3515dac082ada81b8fdceb00d88e5e11dd5d94cc361ac487830"
observation_id: obs_a3ec0d34f67725e0144b7efdd803b91777f37233528b80249686bb9158b43074
event_id: evt_74ac7625f37b0766907e172cff1f63fb8968a4581c60f0b0d368baa861243236
revision_id: rev_6b3d57f3a80ec870c68d9c0d17f6b59f87be89dd7e832eade5f056acdf30b497
source_published_at: 2026-09-28T17:59:52Z
first_seen_at: 2026-09-29T20:46:35.164371Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
interpretation_sha256: "sha256:7ad2efc8ae062a5c87e18d0d581a2728b019e8f969697a83c979ca3c4ea1b4ea"
description: "PDMD 是一种针对视频扩散模型的知识蒸馏技术，通过在更新过程中过滤评论者（critic）引入的错误来提升训练稳定性，从而在减少函数评估次数的同时生成更高质量的视频样本。该方法仅需对现有框架做极小改动，无需额外的网络或数据。"
external_url: http://arxiv.org/abs/2609.35768v1
parent_observation_id: null
last_seen_at: 2026-09-29T20:46:35.164371Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.35768v1](http://arxiv.org/abs/2609.35768v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Zimo Wang、Junkun Yuan、Angtian Wang 等

## 要点解读

### 这是什么
PDMD 是一种针对视频扩散模型的知识蒸馏技术，通过在更新过程中过滤评论者（critic）引入的错误来提升训练稳定性，从而在减少函数评估次数的同时生成更高质量的视频样本。该方法仅需对现有框架做极小改动，无需额外的网络或数据。

### 用在哪里
该技术适用于需要加速视频扩散模型推理或降低计算成本的研究与工程场景，例如实时视频生成、长视频合成或多模态（视频-音频）内容创作。从业者包括视频生成研究人员、AI 应用开发者以及对模型效率有较高要求的团队。

### 可以推断的
推测：PDMD 所提出的过滤评论者错误的方法可能具有良好的通用性，未来有望被应用于其他生成模型（如图像或音频扩散模型）的蒸馏过程中，以解决类似的训练不稳定问题。  
推测：随着视频生成需求的增长，类似 PDMD 的高效蒸馏技术可能成为将大型扩散模型部署到资源受限设备（如移动端或嵌入式系统）的重要手段。

## 来源摘要/节选

> Modern video diffusion models require tens of denoising evaluations over long spatiotemporal token sequences. Distribution Matching Distillation (DMD) reduces the number of function evaluations (NFE) to just a few. However, DMD samples can degrade during training, exhibiting progressive oversaturation and artifacts. We trace this instability to critic errors, which enter successive student updates and accumulate over time. We introduce Projected Distribution Matching Distillation (PDMD) to filter critic errors. PDMD projects out the component of the DMD update parallel to the student-critic endpoint residual. At a fixed noisy query, we prove that this residual is an unbiased estimate of the critic's endpoint error. Under high-dimensional assumptions, this projection removes a constant fraction of critic error while discarding only a vanishing fraction of ideal DMD signal. Empirically, the projection stabilizes training and improves sample quality where DMD degrades and develops unnatural textures. PDMD requires only a one-line code change to DMD, with no extra loss, network, data, model pass, or multi-stage training. With Wan2.1, PDMD achieves a VBench total score of 83.73 at 4 NFE, surpassing matched DMD by 1.03 points. On MiniMax-H3 joint video-audio generation, PDMD achieves a VideoGen-Eval visual total score of 83.17, 0.41 points above the strongest distilled baseline. PDMD also achieves the best performance on all six audio metrics among the compared 4-NFE models. Qualitative comparisons and user studies favor PDMD over the distilled baselines in visual quality, motion, and audio quality. Code and models are available at https://pdmd2026.github.io/.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。