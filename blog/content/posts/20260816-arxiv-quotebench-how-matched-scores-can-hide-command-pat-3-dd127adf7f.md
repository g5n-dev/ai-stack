---
title: "QuoteBench: How Matched Scores Can Hide Command-Path Failures"
date: 2026-08-16T11:15:17+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e58d4c1cce6391561d77f530dd5debd657f8ab005a4d32694c3fa6024dd1fb5d"
source_payload_sha256: "sha256:6c8709149aca92c260d56e79060640299e3941dc539ccaa03a65be372172ee5f"
observation_id: obs_dd127adf7fc228f1bf5179b71421c24068ea574777f91d3b8d6d12ba96685b40
event_id: evt_a0b9ddf9f3f2df7c8bf0f2cca05a64e330696eb2053babee876243bb21030a5f
revision_id: rev_f4cf26f8b18ef7dd1fa7902c584132eaa823036ff7d6f9c85bc72e4cf93ccbc8
source_published_at: 2026-08-13T17:57:20Z
first_seen_at: 2026-08-16T03:12:53.073967Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:c82c455c0e6e2d3996580b08fbeddc59c217ce638d0eb3bef58e415878b8e586"
description: "该研究提出了一个评估框架，用于区分大语言模型在生成命令行时产生的原始错误与后续执行环节引入的故障，并通过特定任务集合检验模型在透明化执行边界前后的性能差异。"
external_url: http://arxiv.org/abs/2608.13547v1
parent_observation_id: null
last_seen_at: 2026-08-16T03:12:53.073967Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.13547v1](http://arxiv.org/abs/2608.13547v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Shangao Li、Yao Zhang、Volker Tresp 等

## 要点解读

### 这是什么
该研究提出了一个评估框架，用于区分大语言模型在生成命令行时产生的原始错误与后续执行环节引入的故障，并通过特定任务集合检验模型在透明化执行边界前后的性能差异。

### 用在哪里
适用于自动化代码生成、命令行助手以及需要评估语言模型在实际部署环境中可靠性的研究与工程实践，帮助从业者识别评测指标可能掩盖的真实问题。

### 可以推断的
推测：在实际的模型部署中，单纯的匹配分数容易忽略掉执行链路中新增解析器等因素带来的干扰，导致对模型能力的评估存在偏差。  
推测：若披露执行边界信息后模型性能显著提升，说明模型具备根据环境约束调整输出的潜力，这对后续优化方向有指导意义。

## 来源摘要/节选

> LLM coding agents issue Bash commands through interfaces that may serialize, wrap, and reparse model output. Matched execution scores alone cannot distinguish command-generation errors from failures introduced after generation. QuoteBench measures this boundary with exact final-state validation on 56 one-shot tasks from 14 incident-derived families, crossing the generation contract with the execution transport around one deliberately unescaped added parser. Escaping at the interpolation point reproduces each replayed reply's raw-path outcome, so any recovery under a disclosed boundary must come from the model changing its generation. Across eight same-window configurations, replaying the same reply through the added parser lowers success by 55.4 to 73.2 percentage points; disclosure recovers 30.4 to 60.7 points for six configurations, and zero or slightly negative for the other two. Raw generation is nearly saturated at the frontier; boundary adaptation is what still separates models. GPT-5.6-sol's matched gap of -3.6 points hides -64.3 points of damage and +60.7 points of compensation. The deployment configuration reorders models: one reversal among 26 comparable pairs is unambiguous and four more sit on single-task margins. Evaluations of command-issuing agents should report the model configuration, generation contract, execution path, operating point, and final-state validator rather than treat a matched score as an intrinsic model property.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。