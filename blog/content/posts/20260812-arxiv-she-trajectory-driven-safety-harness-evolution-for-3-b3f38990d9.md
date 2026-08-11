---
title: "SHE: Trajectory-driven Safety Harness Evolution for LLM Agents"
date: 2026-08-12T01:14:08+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4bdb7d8f2256e3c374ad90d8bb561cdabbf20b9c39b6f26a2208a8a644eda8f3"
source_payload_sha256: "sha256:3b58d5771fac8c7cce21ba161069c4b683456db91405c535fdb60c18eeda49da"
observation_id: obs_b3f38990d9b119745c4a2115d2a1100ac229bb9fb0d5f819114843904a4c2183
event_id: evt_86d334dafc73bd2a4995c3027dbbd81cb0befb4dce19fefb64c88f44bfa798a6
revision_id: rev_7a345d41d45c87c77f3d7942abf1f087498d33e26e6247432dec2243e7b921de
source_published_at: 2026-08-10T17:35:08Z
first_seen_at: 2026-08-11T17:23:48Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:d6cbe849832927aea4cf97358b0aae4b1992ed107ab2ea8d9a54b8a6e52d0379"
description: "该研究提出一种通过学习交互轨迹动态演进 LLM Agent 安全护栏的框架。将护栏拆分为系统提示、规则库、安全记忆和工具策略四个组件，并构建属性导向的演进循环，把轨迹失败转化为结构化诊断并在各组件上局部优化，从而在保持功能效用的同时提升安全性。"
external_url: http://arxiv.org/abs/2608.09885v1
parent_observation_id: null
last_seen_at: 2026-08-11T17:12:16.973050Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09885v1](http://arxiv.org/abs/2608.09885v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Wanying Qu、Qinghua Mao、Yu Li 等

## 要点解读

### 这是什么
该研究提出一种通过学习交互轨迹动态演进 LLM Agent 安全护栏的框架。将护栏拆分为系统提示、规则库、安全记忆和工具策略四个组件，并构建属性导向的演进循环，把轨迹失败转化为结构化诊断并在各组件上局部优化，从而在保持功能效用的同时提升安全性。

### 用在哪里
适用于需要在部署后持续适应新风险且不愿更换底层模型的 LLM Agent 系统，尤其适合安全关键的客服、自动化决策或工具调用场景。

### 可以推断的
- 推测：模块化拆分后，安全策略的调试与升级可以针对单个组件进行，降低了全局改动的风险。  
- 推测：基于轨迹的诊断与局部优化机制，使护栏在不同规模的 Agent 上迁移时可能保留一定的适应性。

## 来源摘要/节选

> The safety of large language model (LLM) agents depends not only on model weights but also on the agent harness that manages context, memory, tools, permissions, and runtime control. Existing safety mechanisms often treat the harness as a fixed deployment artifact, limiting their ability to evolve with emerging risks. Moreover, coupled functions across harness components obscure safety responsibility attribution, making localized evolution difficult. We propose Safety Harness Evolution (SHE), a framework that learns evolving safe boundaries from rollout trajectories. SHE decomposes the harness into four artifacts with explicit safety responsibilities, including the System Prompt, Rule Bank, Safety Memory, and Tool Policy, defining clear functional boundaries for localized evolution. Based on this decomposition, SHE introduces an attribution-guided evolution loop that converts trajectory failures into structured diagnoses, learns artifact-specific boundary refinements, and selects evolved harnesses through safety-utility validation. Experiments on Agent-SafetyBench demonstrate that SHE effectively enhances safety through harness evolution, achieving a 3.1x ASR reduction compared with static SafeHarness, while also improving benign utility. The evolved harness further generalizes to unseen risks on the held-out AgentHarm benchmark and transfers across agent models without additional evolution.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。