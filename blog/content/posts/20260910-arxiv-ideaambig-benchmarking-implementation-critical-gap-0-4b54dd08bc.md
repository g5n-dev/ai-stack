---
title: "IdeaAMBIG: Benchmarking Implementation-Critical Gaps in Research-Idea Specifications"
date: 2026-09-10T12:46:48+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b9cc98640325a5a12bd847b6f9d7abaa6e657907299360b199777e223bfae003"
source_payload_sha256: "sha256:18c17ae38d56cc60c1765b3db302786229350adfe1e332ffa01b0842b30e9d20"
observation_id: obs_4b54dd08bc885b615a97145dbd129ee81eeb1bb256414db9beb0bd9776ad0902
event_id: evt_4ea3a333ea688af5cb95dd3dbc488a72aa1baf7870f406b4db348423b04f46be
revision_id: rev_e9939ce548e1b14daad3e1394b8210a5a8e3a33c203497c0c8951320836e7d9a
source_published_at: 2026-09-09T17:59:04Z
first_seen_at: 2026-09-10T04:56:23Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
interpretation_sha256: "sha256:34cdc59314881c95a8b5cac3ce8f150867066684fa46e303b7e52e021d5f802b"
description: "IdeaAMBIG 是一个评估科研方法规范是否具备足够实现细节的基准，包含从论文、代码库、issue 等来源构建的实例，衡量模型在评估准备度、定位缺陷和生成澄清动作三项能力上的表现。"
external_url: http://arxiv.org/abs/2609.10539v1
parent_observation_id: null
last_seen_at: 2026-09-10T04:43:50.364393Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.10539v1](http://arxiv.org/abs/2609.10539v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yiling Ma、Yilun Zhao、Sihong Wu 等

## 要点解读

### 这是什么
IdeaAMBIG 是一个评估科研方法规范是否具备足够实现细节的基准，包含从论文、代码库、issue 等来源构建的实例，衡量模型在评估准备度、定位缺陷和生成澄清动作三项能力上的表现。

### 用在哪里
适用于希望提升方法描述完整性的研究者，或在构建自动检查和补全科研代码规范的工具时使用，也可用于评估 LLM 在科研实现细节理解上的能力。

### 可以推断的
推测：在现有模型中，仅凭规范文本定位缺失细节十分困难，加入标注缺陷后澄清生成效果大幅提升。  
推测：大量科研方法的实现细节在实际文献中仍不足以直接生成可运行代码，需借助外部资源或人工补充。

## 来源摘要/节选

> A research idea may be novel, coherent, and scientifically plausible, yet its proposed method may remain insufficiently specified for faithful implementation. We study the codification readiness of implementation-facing research-method specifications, defined by whether they provide sufficient methodological information for a competent implementer or coding agent to construct the intended method without unsupported assumptions. We construct evidence-grounded specifications and their supported resolutions from papers, codebases, issue threads, and reproduction artifacts. We introduce IdeaAMBIG, a benchmark of 660 evidence-grounded instances: 163 real-world gaps from reproducibility reports and GitHub issues, and 497 controlled synthetic gaps injected into codification-ready references. IdeaAMBIG evaluates three capabilities: codification-readiness assessment, defect localization, and clarification action generation. Defect localization receives only the specification, whereas clarification additionally receives the annotated defect. Across 13 LLMs, the best model achieves 9.6% Macro Defect Recovery Rate on real-world instances but 80.6% Macro Clarification Action Success Rate when given the defect. In an oracle study, supplying the gold resolution raises the downstream codification-ready rate from 14% to 98%. Across all evaluated models, defect localization is the main bottleneck, with stronger clarification given the defect.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。