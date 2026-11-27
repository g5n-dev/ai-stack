---
title: "Diverse Alternative Reasoning Traces for Hard Math Problems"
date: 2026-11-28T02:58:34+08:00
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
first_seen_at: 2026-11-27T18:57:10.882955Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:068d5269d95f3096a9882504fcd451eb328afc5abb6685b741f2d29e55dd3bcc"
description: "DART 从被拒绝的数学推理轨迹中拆解步骤，按位置加权的不确定性排序，再借助参考答案和元思考生成多样化替代步骤。它扩大了高难度数学问题的可解覆盖面，并可生成用于大语言模型后训练的推理数据。"
external_url: http://arxiv.org/abs/2611.34928v1
parent_observation_id: null
last_seen_at: 2026-11-27T18:57:10.882955Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.34928v1](http://arxiv.org/abs/2611.34928v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Lukas Aichberger、Adam Golinski、Arno Blaas 等

## 要点解读

### 这是什么
DART 从被拒绝的数学推理轨迹中拆解步骤，按位置加权的不确定性排序，再借助参考答案和元思考生成多样化替代步骤。它扩大了高难度数学问题的可解覆盖面，并可生成用于大语言模型后训练的推理数据。

### 用在哪里
适用于数学推理模型的后训练数据构建，尤其是独立采样难以获得正确答案、接受轨迹稀缺的高难度问题。

### 可以推断的
- 推测：与其重复随机采样，从失败轨迹中寻找可替换的关键步骤，可能更适合提升难题的数据覆盖率。
- 推测：DART 在相同生成预算下减少问题，并降低单条接受轨迹的成本，因此值得在数据规模受限时进一步评估。

## 来源摘要/节选

> Post-training large language models (LLMs) for mathematical reasoning often relies on accepted traces whose final answers pass a verifier. For hard math problems, however, such traces can be rare under independent Monte Carlo (MC) sampling. To address this, we propose Diverse Alternative Reasoning Traces (DART), a trace-mining method that starts from a rejected trace, decomposes it into reasoning steps, and ranks them by position-weighted uncertainty. It then generates deliberately distinct alternative candidates for highly ranked steps using reference-answer guidance and a meta-thought before completing the resulting traces. On greedy-unsolved DeepMath-103K problems, DART recovers 37% more problems than MC sampling at a matched number of generated traces. Its estimated generation cost per recovered problem is nearly identical, while its cost per accepted trace is 30% lower. Post-training Llama-3.1-8B-Instruct on traces mined by DART achieves the highest point estimate in five of six evaluations across MATH-500 and AIME benchmarks. These results demonstrate that revisiting rejected traces with DART can expand problem coverage and provide effective post-training data.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。