---
title: "QuoteBench: How Matched Scores Can Hide Command-Path Failures"
date: 2026-08-15T23:37:20+08:00
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
first_seen_at: 2026-08-15T15:34:40.197595Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:7c63f9465890a97b2a2fa742c3e7bc85e6c0539c63a26f77835d957bc9833ecf"
description: "QuoteBench 是一种基准测试，通过在 LLM 生成 Bash 命令后加入未转义的解析层并对比最终执行状态，衡量生成阶段与传输/执行阶段之间误差的界限。它使用 56 项一次性任务，任务来源于 14 个事故家族，帮助区分模型本身产生的错误和后续包装、解析引入的错误。"
external_url: http://arxiv.org/abs/2608.13547v1
parent_observation_id: null
last_seen_at: 2026-08-15T15:34:40.197595Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.13547v1](http://arxiv.org/abs/2608.13547v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Shangao Li、Yao Zhang、Volker Tresp 等

## 要点解读

### 这是什么
QuoteBench 是一种基准测试，通过在 LLM 生成 Bash 命令后加入未转义的解析层并对比最终执行状态，衡量生成阶段与传输/执行阶段之间误差的界限。它使用 56 项一次性任务，任务来源于 14 个事故家族，帮助区分模型本身产生的错误和后续包装、解析引入的错误。

### 用在哪里
适用于评估在复杂包装或重解析环境中运行的命令行代理的鲁棒性，帮助研发团队辨别模型真实能力与传输链路带来的偏差。也为评测平台提供如何报告模型配置、生成契约、执行路径、运行点和最终状态验证器的参考。

### 可以推断的
- 推测：在同一模型配置下，若不记录生成契约和执行路径，匹配分数可能掩盖因额外解析层导致的大幅成功率变化。  
- 推测：模型在边界适应上的差异是影响最终表现的重要因素，同一模型在不同执行窗口中可能展现出显著的成功率波动。

## 来源摘要/节选

> LLM coding agents issue Bash commands through interfaces that may serialize, wrap, and reparse model output. Matched execution scores alone cannot distinguish command-generation errors from failures introduced after generation. QuoteBench measures this boundary with exact final-state validation on 56 one-shot tasks from 14 incident-derived families, crossing the generation contract with the execution transport around one deliberately unescaped added parser. Escaping at the interpolation point reproduces each replayed reply's raw-path outcome, so any recovery under a disclosed boundary must come from the model changing its generation. Across eight same-window configurations, replaying the same reply through the added parser lowers success by 55.4 to 73.2 percentage points; disclosure recovers 30.4 to 60.7 points for six configurations, and zero or slightly negative for the other two. Raw generation is nearly saturated at the frontier; boundary adaptation is what still separates models. GPT-5.6-sol's matched gap of -3.6 points hides -64.3 points of damage and +60.7 points of compensation. The deployment configuration reorders models: one reversal among 26 comparable pairs is unambiguous and four more sit on single-task margins. Evaluations of command-issuing agents should report the model configuration, generation contract, execution path, operating point, and final-state validator rather than treat a matched score as an intrinsic model property.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。