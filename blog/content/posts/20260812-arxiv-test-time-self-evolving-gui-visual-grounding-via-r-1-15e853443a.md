---
title: "Test-Time Self-Evolving GUI Visual Grounding via Reflection-Guided On-Policy Self-Distillation"
date: 2026-08-12T21:48:28+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:fbd9fafe9bdb82b96527b749d6ab96cce6b43d7c37c718d4666b4cec2ca3325c"
source_payload_sha256: "sha256:a973f0bd8b1fef4601ab686274591905753c33f6360beb3a497d1b7a3343e226"
observation_id: obs_15e853443ae6687e4cf0a9f1aca5005f7264d0c3011dc5ee5f8050dd53c22442
event_id: evt_3d9c1fafe3e737eda4233a6b267fd66576b3a8a9fbe2ddd6abedfc27aaf2e9df
revision_id: rev_d20a9597f5350941f8e667118fd7ca9d5372adcddfb0674e934dbacf58454e2d
source_published_at: 2026-08-11T17:50:25Z
first_seen_at: 2026-08-12T13:58:13Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 94
interpretation_sha256: "sha256:04a1038013884c79861a3a403294d16c4855a624031221bc1932bddab0ec055b"
description: "该研究提出一种测试时自进化框架，使 GUI 视觉定位模型在部署后能够通过探索、评估、反思和内部化的闭环过程自行改进。框架中引入基于多模态大模型的评估器提供推理反馈，并通过有条件的自教师把高层反思转化为细粒度的 token 级监督，同时使用对比校准防止错误前缀破坏监督信号。"
external_url: http://arxiv.org/abs/2608.11191v1
parent_observation_id: null
last_seen_at: 2026-08-12T13:46:13.798922Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11191v1](http://arxiv.org/abs/2608.11191v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Shiyu Xuan、Zechao Li

## 要点解读

### 这是什么  
该研究提出一种测试时自进化框架，使 GUI 视觉定位模型在部署后能够通过探索、评估、反思和内部化的闭环过程自行改进。框架中引入基于多模态大模型的评估器提供推理反馈，并通过有条件的自教师把高层反思转化为细粒度的 token 级监督，同时使用对比校准防止错误前缀破坏监督信号。

### 用在哪里  
适用于需要模型在真实环境中不断适配新界面或新布局的场景，例如自动化 UI 测试、虚拟助手或跨平台界面理解等任务，尤其在缺乏人工标注的情况下能发挥作用。

### 可以推断的  
- 推测：该方法在测试时进行自蒸馏和策略采样，可能会带来额外的计算和内存开销，因而更适用于算力充足的服务器端部署，而非资源受限的移动端。  
- 推测：其核心的反思机制可迁移到其他需要视觉定位且环境频繁变化的领域，如机器人视觉或增强现实中的目标定位。

## 来源摘要/节选

> GUI Visual Grounding is a fundamental capability for GUI agents. Existing models typically freeze their parameters after deployment, limiting their ability to adapt to unseen interfaces. Although recent methods attempt to adapt models via test-time reinforcement learning, they cannot reflect upon failed exploration. To overcome this, we propose a Test-Time Self-Evolving framework that enables models to improve after deployment without human-annotated ground truth. It constructs a closed-loop of Exploration, Evaluation, Reflection, and Internalization. Specifically, the agent first explores unseen interfaces by predicting grounding coordinates for given instructions. To evaluate these explorations, we introduce an MLLM-based Reflector to assess the generated results and provide the corresponding reasoning reflections. To internalize reflection knowledge into the model weights, we propose Reflection-Guided On-Policy Self-Distillation, which translates high-level reasoning into dense token-level supervision via a conditioned self-teacher. Furthermore, we design a Contrastive Calibration method to prevent incorrect auto-regressive prefixes from corrupting the supervisory signals during failed explorations. Extensive experiments across six benchmarks demonstrate our framework's effectiveness, achieving an average accuracy improvement of 7.4% over the base model. To the best of our knowledge, this is the first work to successfully exploit on-policy self-distillation for test-time adaptation in GUI visual grounding. By filling the gap in post-deployment adaptation, our framework completes the self-evolving capability of GUI agents. The code will be released.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。