---
title: "SPO++: Stream-Aligned Policy Optimization for Asynchronous Agentic RL"
date: 2026-08-26T12:08:19+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b243d4440f3c83e90db8a4c7bb89db6a79bc52a104c6a6b95548ffd97eccda5a"
source_payload_sha256: "sha256:c2acbb7bb5e9949e08fec35835179f9b3ffe9e838e8aa24e8a57ba9aee1135db"
observation_id: obs_25cc3281d030fe4c9bf6bece93c3c6b0a84feb4bf24ce934993170887c28fc7f
event_id: evt_ee4417d3e1736b7a08ac473b76c1a68fc21e3fe76a0813b91fd56588576b51a8
revision_id: rev_b6725c1781e309b133d4559b3e3a03f3b118b439491840257f1328c4094e2efe
source_published_at: 2026-08-25T17:52:19Z
first_seen_at: 2026-08-26T04:06:08.369746Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
interpretation_sha256: "sha256:1ca7e10d715f0fc463428afcfc13f0e6bc93981ea62aef43bb882417169babea"
description: "该研究提出一种改进的策略优化方法，修复了传统单流策略优化中终局优势在动作令牌空间的失配问题，并通过在策略事件层面组织提示信息来提升学习效率。"
external_url: http://arxiv.org/abs/2608.24870v1
parent_observation_id: null
last_seen_at: 2026-08-26T04:06:08.369746Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24870v1](http://arxiv.org/abs/2608.24870v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Kai Ruan、Jinghao Lin、Qianshan Wei 等

## 要点解读

### 这是什么
该研究提出一种改进的策略优化方法，修复了传统单流策略优化中终局优势在动作令牌空间的失配问题，并通过在策略事件层面组织提示信息来提升学习效率。

### 用在哪里
适用于需要处理长且可变工具使用轨迹的异步强化学习系统，尤其是研究语言模型与工具交互或任务规划的团队。

### 可以推断的
推测：该方法在不同模型规模上的实验结果保持一致，暗示其对模型容量的敏感性较低。  
推测：动作令牌衡量的优势标准化可能是该方法提升在线学习效率的核心因素。

## 来源摘要/节选

> Group-relative reinforcement learning waits for sibling rollouts of the same prompt, which is costly for long and variable tool-use trajectories. Single-stream Policy Optimization (SPO) removes this dependency with a persistent prompt-level value estimate, but its recipe whitens one advantage per trajectory before optimizing a token-mean actor loss. We show that trajectory centering generally does not center the token-weighted quantity consumed by the actor, and fix the mismatch by standardizing terminal-outcome advantages under the action-token measure. We additionally organize prompt evidence by the policy event that generated it rather than learner receipt order. Across matched runs on ALFWorld at two model scales and on Math-TIR, SPO++ improves online learning efficiency over SPO. A paired ablation identifies action-token-measure normalization as the strongest tested component.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。