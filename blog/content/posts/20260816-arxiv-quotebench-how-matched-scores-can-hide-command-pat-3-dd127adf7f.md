---
title: "QuoteBench: How Matched Scores Can Hide Command-Path Failures"
date: 2026-08-16T17:44:47+08:00
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
first_seen_at: 2026-08-16T09:41:16.686402Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:8e7aa0b26d095cb1abc0990de3325862c442bb6821b4686f9e8722105b459e38"
description: "该内容提出一种名为 QuoteBench 的评估方法，用于检测 LLM 代码生成 agent 在生成 Bash 命令后经过传输和再次解析的过程中，匹配的执行分数是否能真实反映模型的生成质量。它通过在生成契约与执行路径之间加入额外的解析器，考察模型在明确边界披露前后的成功差异。"
external_url: http://arxiv.org/abs/2608.13547v1
parent_observation_id: null
last_seen_at: 2026-08-16T09:41:16.686402Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.13547v1](http://arxiv.org/abs/2608.13547v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Shangao Li、Yao Zhang、Volker Tresp 等

## 要点解读

### 这是什么
该内容提出一种名为 QuoteBench 的评估方法，用于检测 LLM 代码生成 agent 在生成 Bash 命令后经过传输和再次解析的过程中，匹配的执行分数是否能真实反映模型的生成质量。它通过在生成契约与执行路径之间加入额外的解析器，考察模型在明确边界披露前后的成功差异。

### 用在哪里
适用于研究 LLM agent 在命令行交互场景下的鲁棒性，评估不同模型在命令生成与执行边界的表现，以及为构建更可靠的评测框架提供参考。

### 可以推断的
推测：即使模型在原始生成阶段表现接近上限，实际部署时若执行路径加入了额外的解析或转义步骤，仍可能导致显著的成功率下降。  
推测：单纯依赖匹配的执行分数可能导致对模型真实能力的误判，加入最终状态校验并公开解析边界才能得到更公平的对比结果。

## 来源摘要/节选

> LLM coding agents issue Bash commands through interfaces that may serialize, wrap, and reparse model output. Matched execution scores alone cannot distinguish command-generation errors from failures introduced after generation. QuoteBench measures this boundary with exact final-state validation on 56 one-shot tasks from 14 incident-derived families, crossing the generation contract with the execution transport around one deliberately unescaped added parser. Escaping at the interpolation point reproduces each replayed reply's raw-path outcome, so any recovery under a disclosed boundary must come from the model changing its generation. Across eight same-window configurations, replaying the same reply through the added parser lowers success by 55.4 to 73.2 percentage points; disclosure recovers 30.4 to 60.7 points for six configurations, and zero or slightly negative for the other two. Raw generation is nearly saturated at the frontier; boundary adaptation is what still separates models. GPT-5.6-sol's matched gap of -3.6 points hides -64.3 points of damage and +60.7 points of compensation. The deployment configuration reorders models: one reversal among 26 comparable pairs is unambiguous and four more sit on single-task margins. Evaluations of command-issuing agents should report the model configuration, generation contract, execution path, operating point, and final-state validator rather than treat a matched score as an intrinsic model property.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。