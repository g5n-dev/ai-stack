---
title: "Cognitive Extensions for Dual-Process Language Agents: Memory and Self-Reflection in Interactive Environments"
date: 2026-09-18T08:20:37+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b3d68ffca888d9348d5b09b57812db9b2f399b267d866f5282cd27d4a5e89e08"
source_payload_sha256: "sha256:47264145bca95a4744671b4b71a7eaecb27ccf50ee74a246e795df4cfaf53f08"
observation_id: obs_f4668fa23ffd4d9617fe8da123feeedc461e18ab2bb57cf68bdc81f06f82fbad
event_id: evt_78e942facd336c3b660737719c3da1208664cebe0e2fd46a417274c62f71af44
revision_id: rev_a0d341cf5c27a83ab076f3c6ad4670ec425680ef085d3a010d336916fa6aefd5
source_published_at: 2026-09-16T17:50:42Z
first_seen_at: 2026-09-18T00:17:34.819841Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 109
interpretation_sha256: "sha256:0cb2d51028b7b9d3b67e2e27f10df9259efcda93cde885bf030bed478e9b7340"
description: "这项研究在双进程语言代理框架中加入记忆与自我反思两个模块，以提升在交互环境中的长时程状态跟踪、动作执行和错误恢复能力。"
external_url: http://arxiv.org/abs/2609.19128v1
parent_observation_id: null
last_seen_at: 2026-09-18T00:17:34.819841Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.19128v1](http://arxiv.org/abs/2609.19128v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: João Meneses dos Santos、Arlindo L. Oliveira

## 要点解读

### 这是什么
这项研究在双进程语言代理框架中加入记忆与自我反思两个模块，以提升在交互环境中的长时程状态跟踪、动作执行和错误恢复能力。

### 用在哪里
适用于需要在动态环境中持续跟踪状态并纠正错误的语言代理系统，例如交互式模拟任务的评估平台。

### 可以推断的
推测：加入自我反思机制后，系统对运行时长的控制得到加强，从而整体表现更稳健。  
推测：当执行流程已经稳定后，记忆模块的作用会更加突出，可用于后续情境的快速复用。

## 来源摘要/节选

> Language agents remain brittle in interactive environments, where success requires long-horizon state tracking, valid action execution, and recovery from failed steps. We extend SwiftSage, a dual-process agent that combines a fast action proposer with a slower planner, using two modular cognitive extensions: an Adaptive Memory Module (AMM) for salience-gated episodic storage and trigger-driven retrieval, and a Self-Reflection Module (SRM) for bounded execution-time validation and corrective intervention. Both modules are implemented as feature-flagged extensions over the same execution substrate, enabling controlled ablations on ScienceWorld. Across four configurations---baseline, baseline+AMM, baseline+SRM, and the full system---the full system achieves the best mean final score (64.62), success rate (43.17%), and successful-step efficiency (19.33 steps), while SRM is the strongest standalone contributor. The results suggest that execution-time control is the dominant bottleneck in this setting, while episodic memory becomes most useful once the runtime loop is stabilized.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。