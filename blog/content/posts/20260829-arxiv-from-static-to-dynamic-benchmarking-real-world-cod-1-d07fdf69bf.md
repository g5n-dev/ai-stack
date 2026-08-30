---
title: "From Static to Dynamic: Benchmarking Real-World Code Review with MCR-Bench"
date: 2026-08-29T17:06:42+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:512af8443b36b93147a052e268ab165f3736bc6cf7fb306cdf56ed6826ff2f32"
source_payload_sha256: "sha256:d783b6d133764218666c6358640ddc358b4bff43a01e7a6815fb28239c216fab"
observation_id: obs_d07fdf69bf1a83c6b01679f7262836af5cf9105ceaad262a2daa1b57ee075964
event_id: evt_6e2c3d8a5f085a89c0c625796bbef70a677bf9b59e087486df2444ed61c45863
revision_id: rev_2f35c9af695fd0aa24b44b3a9e2d082256906a4f53ef43c07e0a93f2079067b5
source_published_at: 2026-08-27T17:56:24Z
first_seen_at: 2026-08-29T09:16:11Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:7723e3f84fc41131f67620b907f818a4b23965c14e29d6c92f6322aa6c4f6971"
description: "该内容介绍了一个面向真实多轮代码审查的评测基准，覆盖五种常用编程语言，包含两千余条真实审查任务，并为每条任务标注了缺陷的细粒度属性和跨轮次状态。"
external_url: http://arxiv.org/abs/2608.27442v1
parent_observation_id: null
last_seen_at: 2026-08-30T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27442v1](http://arxiv.org/abs/2608.27442v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Dewu Zheng、Yanlin Wang、Xiwen Wang 等

## 要点解读

### 这是什么
该内容介绍了一个面向真实多轮代码审查的评测基准，覆盖五种常用编程语言，包含两千余条真实审查任务，并为每条任务标注了缺陷的细粒度属性和跨轮次状态。

### 用在哪里
适用于想要评估或改进大语言模型在迭代式代码审查中表现的研究者和工程师，尤其是关注缺陷检测、状态追踪和多轮交互的系统设计。

### 可以推断的
- 推测：在实际工具中实现跨轮记忆和状态对齐是提升审查质量的关键方向。  
- 推测：针对不同类型和严重程度的缺陷进行专项训练可能有助于模型捕捉低显著性缺陷。

## 来源摘要/节选

> In real-world software development, code review typically involves iterative interactions between developers and reviewers to improve software quality, making the process costly and time-consuming. Although recent work explores large language models (LLMs) for automated code review, most approaches oversimplify code review into a single-round, static decision task, which fails to capture the multi-round interactive nature and the complex problem-solving processes inherent in realistic review scenarios. To bridge this gap, we introduce MCR-Bench, the first defect state-aware benchmark designed for realistic multi-round code review. MCR-Bench covers five commonly-used programming languages and consists of 2,269 real-world multi-round code review tasks, each of which is annotated with fine-grained defect information and cross-round state labels. Each task in MCR-Bench is equipped with fine-grained defect metadata (e.g., description, type, severity) alongside dynamic state annotations, capturing the complete evolutionary trajectory of a defect throughout the multi-round process. We obtain several findings through extensive experiments on MCR-Bench with mainstream LLMs. (1) Limited overall capability: experiments reveal that mainstream LLMs exhibit limited overall performance in defect detection and defect lifecycle state tracking, with performance degrading significantly as the number of interaction rounds increases; (2) Defect-sensitive performance: LLMs' performance varies substantially across different defect types and severity levels, with semantically complex or low-salience defects being significantly more likely to be missed; (3) Underlying Failure Mechanisms: our in-depth error analysis dissects the distinct drivers of false positives and false negatives, revealing critical weaknesses such as cross-round temporal misalignment and inadequate long-range memory.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。