---
title: "Toward Skill-Native LLMs: Skill Entropy for Benchmarking and Training Long-Horizon Reasoning"
date: 2026-08-06T17:52:54+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a9be959d177ab8ca9adaa44a6fab8299fc4a5bac5d389d6f115b03da8e1a4464"
source_payload_sha256: "sha256:b66b7b179f6a764c938fdac6488819abc519ca012710f59ce4e053425e58d8bd"
observation_id: obs_7b6085fd248fee2308ff1b2e6cdb1b2dd150989f06adde5239ef0a2feb7bea43
event_id: evt_fe2738fc7f35759fe0641cfd84148039e51dfcbcdf56c91a3c325e069fa2dac2
revision_id: rev_63c626b0fa4d4ed634cde60376cc73683716df6d75b6c98615938779917a3060
source_published_at: 2026-08-05T17:57:16Z
first_seen_at: 2026-08-06T10:02:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
interpretation_sha256: "sha256:e7d30bf68fde3260ae053d0f99dd8d1fea21480de09c7489be8ce0a7ccdbab91"
description: "该内容提出一种量化推理过程中技能切换难度的指标，并在此基础上构建了包含跨技能长时推理任务的评测基准，同时将该指标转化为强化学习训练信号，用于提升模型在复杂推理链中的技能切换能力。"
external_url: http://arxiv.org/abs/2608.05139v1
parent_observation_id: null
last_seen_at: 2026-08-07T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.05139v1](http://arxiv.org/abs/2608.05139v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yinghui He、Ling Yang、Jiarui Liu 等

## 要点解读

### 这是什么

该内容提出一种量化推理过程中技能切换难度的指标，并在此基础上构建了包含跨技能长时推理任务的评测基准，同时将该指标转化为强化学习训练信号，用于提升模型在复杂推理链中的技能切换能力。

### 用在哪里

适用于对大语言模型多步推理能力进行标准化评估的研究场景，以及需要改进模型在多技能协同任务中表现的训练流程设计。相关工作对关注模型工具调用、任务规划或复杂问题分解能力的研究者和工程师具有参考价值。

### 可以推断的

推测：在实际应用中，需要频繁切换技能的任务（如先执行计算再进行逻辑推理）往往更容易出错，该指标或方法有望帮助定位模型在这类场景下的薄弱环节。

推测：若该评测框架和训练方法被后续研究广泛采用，可能会成为评估长时推理模型能力的新标准之一，影响相关模型优化的方向。

## 来源摘要/节选

> Long-horizon reasoning in recent LLMs demands that the model switch between distinct skills inside a reasoning chain, such as first doing a math derivation, then using the result to plan a schedule. We call such problems cross-skill long-horizon tasks: multi-step tasks whose steps require different reasoning skills and depend on earlier outputs. Existing benchmarks often evaluate individual skills, lacking a principled way to measure how well a model switches between skills. We address this gap from both the evaluation and training sides. We introduce Skill Entropy, a measure of the difficulty of switching from one skill to another. We then propose Skill^2-Bench, a benchmark of cross-skill long-horizon tasks built over 558 skills across 9 verifiable and open-ended domains. Each task is assigned a task-level skill-entropy score and grouped into three difficulty levels. Evaluating 8 frontier and 4 open-source models on Skill^2-Bench reveals a skill-switching gap: accuracy decreases on higher-entropy tasks. We then turn skill entropy from a benchmark scale into a training signal. We propose Skill-Entropy RL, an RL framework where the model predicts not only the answer at each step but also the skill used to produce it. The reward combines step-level correctness with a skill-entropy reward that measures the alignment between the model-predicted skill sequence and the gold skill sequence. On Qwen3-4B-Instruct and Qwen3-1.7B, Skill-Entropy RL improves the Skill^2-Bench score from 34.4% to 68.4% and from 14.6% to 40.1%, respectively, outperforming competitive baselines. The same pipeline can be applied to off-the-shelf training data such as OpenR1-Math, indicating that skill entropy is a reusable training signal. Code available at: https://github.com/Gen-Verse/Skill-Entropy-RL

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。