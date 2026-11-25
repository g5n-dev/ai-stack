---
title: "RepoEviAgent: Scalable Synthesis of Evidence-Grounded Repository-Level Question Answering Tasks"
date: 2026-11-25T10:26:12+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d4d388913d2c4780e1257ff840d936b1ee33f44e10eb309d9beb99ac51a926e2"
source_payload_sha256: "sha256:fd89f89522b33004f7dc9d862d7093b031014fa8221057f3f53859a5af9e7e6b"
observation_id: obs_2b2797e6aae214b602200b7c9ab7991d8e015209ca970b760e01168552c805c8
event_id: evt_d49cab985e4d761ccd2daf309c9fa4155442119463cbbe82d1e46170f40297fa
revision_id: rev_9ffe2f3fd0f2140e9f43224cb3b831470d61173c37dee396bda4f9ef2acdb434
source_published_at: 2026-11-24T03:24:30Z
first_seen_at: 2026-11-25T02:24:51.979378Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:aa6e8dbcb1a2956f7789462904f589c3266d9a9958c96e6fa519ef4e345ff1a4"
description: "RepoEviAgent 是一种可扩展的软件工程数据构建框架，通过质量筛选和多智能体协作，生成有代码仓库证据支撑的问答任务。其配套基准 RepoEviQA 覆盖五种编程语言，并包含 334 个任务。"
external_url: http://arxiv.org/abs/2611.31873v1
parent_observation_id: null
last_seen_at: 2026-11-25T02:24:51.979378Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.31873v1](http://arxiv.org/abs/2611.31873v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Aoqi Hu、Yueao Xing

## 要点解读

### 这是什么
RepoEviAgent 是一种可扩展的软件工程数据构建框架，通过质量筛选和多智能体协作，生成有代码仓库证据支撑的问答任务。其配套基准 RepoEviQA 覆盖五种编程语言，并包含 334 个任务。

### 用在哪里
它适用于构造软件工程智能体的训练与评测数据，也可用于评估模型理解仓库结构、跨模块依赖和运行时行为的能力。

### 可以推断的
- 推测：这类“证据支撑”的问答任务，可能比仅考察单文件或单函数的问题更接近真实软件工程场景。
- 推测：多语言、分类别评测有助于识别模型在不同技术栈或任务类型上的能力差异。

## 来源摘要/节选

> Real-world software engineering (SWE) tasks require agents to understand repository structures, cross-module dependencies, and runtime behaviors, posing significant challenges for constructing high-quality training and evaluation data. To address this, we propose RepoEviAgent, a scalable SWE data construction framework that integrates quality-aware data curation and role-specialized multi-agent task synthesis. Starting from 8,477 open-source repositories and approximately 2.48 million pull request records, we employ semantic alignment, complexity constraints, and multidimensional quality assessment to identify valuable SWE data. We further develop a sandbox-based multi-agent framework that integrates automated environment construction, execution validation, repository exploration, and evidence-grounded Q&amp;A synthesis. Based on this framework, we construct RepoEviQA, a benchmark for Repository-Level Evidence-Grounded Question Answering, comprising 334 tasks across five programming languages and diverse SWE categories, with rigorous rubric-based evaluation. We evaluate five frontier coding models on RepoEviQA, revealing substantial performance differences across task categories and programming languages.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。