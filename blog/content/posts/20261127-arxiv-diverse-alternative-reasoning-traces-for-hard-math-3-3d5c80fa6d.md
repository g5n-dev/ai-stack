---
title: "Diverse Alternative Reasoning Traces for Hard Math Problems"
date: 2026-11-27T16:28:10+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2bdb60e9fe6c87f1e44c83e19e6ddc8f31a7c9b77c396682fc8792b8b84f8205"
source_payload_sha256: "sha256:3a9c24e68e3fbca1cc9301d04a44e74fdea24657d74f26049bbda3bacfe7bb84"
observation_id: obs_3d5c80fa6d956b0a36e56ba82880a4d210303ede50abf415f3afb3b994b37ab7
event_id: evt_c77d116333744c8c667e8e84c8b02e0d4c05bcb2950aa4f5dc321b3973e8cd6a
revision_id: rev_fe4b7011219d0d9ad241097761bd46e766ed98e6fc666038120cf59ae083b9b6
source_published_at: 2026-11-25T18:59:11Z
first_seen_at: 2026-11-27T08:26:19.546331Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:3560e16a00cd325153fd6d50cb1f50c49c94c7fc286497b1cb613451e39a9711"
description: "DART 是一种面向困难数学题的推理轨迹挖掘方法：从被拒绝的轨迹出发，拆分并定位高不确定步骤，再生成不同候选路径并补全轨迹。实验显示，它能扩大可求解题目覆盖范围，并为大语言模型的后训练提供数据。"
external_url: http://arxiv.org/abs/2611.34928v1
parent_observation_id: null
last_seen_at: 2026-11-27T08:26:19.546331Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.34928v1](http://arxiv.org/abs/2611.34928v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Lukas Aichberger、Adam Golinski、Arno Blaas 等

## 要点解读

### 这是什么
DART 是一种面向困难数学题的推理轨迹挖掘方法：从被拒绝的轨迹出发，拆分并定位高不确定步骤，再生成不同候选路径并补全轨迹。实验显示，它能扩大可求解题目覆盖范围，并为大语言模型的后训练提供数据。

### 用在哪里
适用于需要通过采样生成数学推理训练数据的后训练流程，尤其适合正确推理轨迹稀缺、常规蒙特卡洛采样效率不足的场景。研究人员可参考其轨迹分解、步骤排序与候选生成思路。

### 可以推断的
- 推测：对正确性验证成本较高的数学任务，保留并改造失败轨迹可能比单纯增加采样次数更有效。
- 推测：多样化推理轨迹或许能减少后训练数据过度集中于单一解法的问题。

## 来源摘要/节选

> Post-training large language models (LLMs) for mathematical reasoning often relies on accepted traces whose final answers pass a verifier. For hard math problems, however, such traces can be rare under independent Monte Carlo (MC) sampling. To address this, we propose Diverse Alternative Reasoning Traces (DART), a trace-mining method that starts from a rejected trace, decomposes it into reasoning steps, and ranks them by position-weighted uncertainty. It then generates deliberately distinct alternative candidates for highly ranked steps using reference-answer guidance and a meta-thought before completing the resulting traces. On greedy-unsolved DeepMath-103K problems, DART recovers 37% more problems than MC sampling at a matched number of generated traces. Its estimated generation cost per recovered problem is nearly identical, while its cost per accepted trace is 30% lower. Post-training Llama-3.1-8B-Instruct on traces mined by DART achieves the highest point estimate in five of six evaluations across MATH-500 and AIME benchmarks. These results demonstrate that revisiting rejected traces with DART can expand problem coverage and provide effective post-training data.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。