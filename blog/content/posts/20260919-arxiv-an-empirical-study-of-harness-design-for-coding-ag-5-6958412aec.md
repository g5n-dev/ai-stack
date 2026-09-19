---
title: "An Empirical Study of Harness Design for Coding Agents"
date: 2026-09-19T08:23:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a1e40e738f2e711e902ba0faee914d5eb6ead79a35d7aca765aae06795ef894b"
source_payload_sha256: "sha256:c0f02c75ed974d389b446917f8e82abd0c975f9d410cbb0dfd096385a5c91e36"
observation_id: obs_6958412aecc59af7231b0bb23bec5de6488ebb69a83989185ed6189bcf3f525a
event_id: evt_65addc563842625cd32542df97ab893a751e160c792be789d6636eee6654c7cc
revision_id: rev_69c0caa270f256c4362896f96c1e6a7d2953a4e69b7747311f477c9a5a033a87
source_published_at: 2026-09-17T17:58:07Z
first_seen_at: 2026-09-19T00:20:33.278857Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
interpretation_sha256: "sha256:90964300149cd05a8f8e14d19b451f795429c759ed112733be920e5d12c7dfa6"
description: "该研究把编码智能体的评测框架拆分为规划、动作空间和上下文管理三个可独立替换的模块，在不同上下文窗口预算下系统比较它们的独立作用，并给出各组件对性能和成本的影响趋势。"
external_url: http://arxiv.org/abs/2609.20804v1
parent_observation_id: null
last_seen_at: 2026-09-19T00:20:33.278857Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20804v1](http://arxiv.org/abs/2609.20804v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Run-Ze Fan、Zihao Zhang、Simin Ma 等

## 要点解读

### 这是什么
该研究把编码智能体的评测框架拆分为规划、动作空间和上下文管理三个可独立替换的模块，在不同上下文窗口预算下系统比较它们的独立作用，并给出各组件对性能和成本的影响趋势。

### 用在哪里
适用于想要评估或优化智能体评测框架的研究者和工程师，尤其是关注不同模型在资源受限环境下的行为差异和成本控制的场景。

### 可以推断的
- 推测：在上下文窗口预算受限的情况下，优化上下文管理的策略会显著提升任务完成率。  
- 推测：规划的作用会随模型强弱而变化，较弱模型主要依赖规划提升准确率，而较强模型则倾向于使用规划降低调用成本。

## 来源摘要/节选

> Coding harnesses shape how autonomous coding agents translate model capabilities into long-horizon software-engineering performance, yet existing work typically evaluates harnesses as monolithic systems, leaving the effectiveness of individual components unclear. To enable component-level comparisons, we study this question with a lightweight coding harness whose execution loop is fixed while three components are varied: planning, action space, and context management. Across four models evaluated on SWE-Bench Verified and Terminal-Bench 2.1, we evaluate 176 matched settings spanning five context-management strategies, four context-window budgets, and targeted ablations of planning and action space. We find that: (1) Context management becomes increasingly valuable as the context-window budget tightens, with most of its benefit coming from preventing context-overflow failures. (2) Staging rule-based elision before LLM-based summarization provides the strongest overall efficiency among the context-management strategies, whereas making elided content recoverable adds machinery that models rarely use and yields no accuracy gain. (3) Planning shifts from an accuracy scaffold for weaker models to a cost saver for stronger models, with little change in accuracy. (4) Predefined tools improve performance for models with weaker bash proficiency, whereas bash-capable models can operate effectively with a bash-only interface and achieve substantially lower cost, especially on command-line-centric tasks. Trajectory-level analysis explains these effects: context management extends execution trajectories without substantially altering agent behavior, planning changes where trajectories stop, and the action space changes the granularity at which code is written. These findings inform model- and budget-aware harness design and provide a modular framework for evaluating future harness components.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。