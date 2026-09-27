---
title: "A Living Benchmark for Information Retrieval from Electronic Health Records"
date: 2026-09-27T22:01:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6dfd7da115ff417aca6dd346580ca17fc82c6a949a98ecdc0cf3395cc041235c"
source_payload_sha256: "sha256:8be23ff7eaca772f415b28143e286ca8124f7d8d360f1dd90ab8e4ea8ad40bbe"
observation_id: obs_6c78261af7548cefb72dcc29eb305fbadd612a887ced852c285a5e97999908f9
event_id: evt_6e9793040fc6e58a92149ca307efee26604f7ded1a4f706e87358d45ea2a48ad
revision_id: rev_ed3ace13f81548d6eb37378a6f6a55f819e747670a7c444e648dabcc182bc3c4
source_published_at: 2026-09-24T17:41:16Z
first_seen_at: 2026-09-27T13:58:03.933116Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
interpretation_sha256: "sha256:01dff1bd9f6ea83c11cfe68fd9e006dbfabbfbb39241f7e0a5c8cee06914c3f5"
description: "该研究提出一种可扩展的自动生成框架，从纵向电子健康记录中产出问答对，并经临床医生验证后形成可持续更新的评估数据集（BRIE），用于衡量临床语言模型在信息检索任务上的表现。"
external_url: http://arxiv.org/abs/2609.30205v1
parent_observation_id: null
last_seen_at: 2026-09-27T13:58:03.933116Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30205v1](http://arxiv.org/abs/2609.30205v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Jordan L. Cahoon、Chloe O. Stanwyck、Sulaiman Somani 等

## 要点解读

### 这是什么  
该研究提出一种可扩展的自动生成框架，从纵向电子健康记录中产出问答对，并经临床医生验证后形成可持续更新的评估数据集（BRIE），用于衡量临床语言模型在信息检索任务上的表现。

### 用在哪里  
该基准适用于构建或评估基于大语言模型的临床助理系统的研发团队，帮助他们检测模型在跨文档、跨就诊信息综合检索时的准确性，并支持在技术快速迭代过程中持续更新测试内容。

### 可以推断的  
- 推测：该框架通过临床医生验证生成过程，可生成多条符合不同临床思维的答案，提升评估的鲁棒性。  
- 推测：伴随模型和推理策略的不断演进，现有静态评估集容易失效，持续生成新题的机制有助于防止评估泄露并保持与实际部署环境的一致性。

## 来源摘要/节选

> Large language model (LLM)-based clinical assistants are increasingly being integrated into electronic health record (EHR) systems, transforming how clinicians retrieve and synthesize information from patient records. Their safety and utility depend on rigorous evaluation, yet existing benchmarks are manually curated, costly to update, and rapidly become obsolete with evolving technological advancements. We present a scalable framework that automatically generates question--answer pairs from longitudinal EHR notes. Nineteen clinicians validate the benchmark generator, producing the Benchmark for Retrieving Information in EHRs (BRIE), a continuously maintainable evaluation dataset. Across nine LLMs and five inference strategies, state-of-the-art systems frequently omit clinically important information, particularly for questions requiring synthesis across multiple documents and encounters. Because the generator itself is validated, BRIE supports evaluations that static benchmarks cannot, including the generation of multiple answers that reflect variation in clinician reasoning for robust performance assessment and continuously refreshing benchmark content to guard against leakage. Our results demonstrate that scalable benchmark generation enables rigorous, up-to-date evaluation of clinical LLMs as they are deployed in rapidly evolving healthcare settings.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。