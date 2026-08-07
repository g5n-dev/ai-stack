---
title: "CalibForge: Adversarial Solver Calibration for Scaling Learnable Terminal Tasks"
date: 2026-08-07T21:41:07+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7a0bdf6e3df669dbaeb7cb6a16c8ba68d615f064912b49cdc68e627d553f53c7"
source_payload_sha256: "sha256:12a260fdea475e262d0ab33cec597e2a63fded73b8560e29ebaddf069bf72510"
observation_id: obs_e5f19d16b8924d9cc490ab6de80aae3e046b4686c36b25e1288cab326c0ac9f6
event_id: evt_5f35974e2f46d3b32244d75dfe79ac78b4294b5b8ac25745e28cf73f1c0c96e2
revision_id: rev_f6f8c2c8ec1e16bfdcb2a0cc6d029b124da13f3108b80902a9f4edf484e2f976
source_published_at: 2026-08-06T17:53:18Z
first_seen_at: 2026-08-07T13:38:29.396217Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
interpretation_sha256: "sha256:8ff9ab88bc30987ddac5b12af8196b9df3db859dd2946ae0d5cc110a30b29a8e"
description: "CalibForge 是一种自动化终端任务合成系统，通过验证过的求解器行为对候选任务进行对抗性校准，使任务难度与求解器能力相匹配。"
external_url: http://arxiv.org/abs/2608.06352v1
parent_observation_id: null
last_seen_at: 2026-08-07T13:38:29.396217Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06352v1](http://arxiv.org/abs/2608.06352v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Fanzhe Meng、Guoxin Chen、Jiale Zhao 等

## 要点解读

### 这是什么
CalibForge 是一种自动化终端任务合成系统，通过验证过的求解器行为对候选任务进行对抗性校准，使任务难度与求解器能力相匹配。

### 用在哪里
适用于需要构建可验证且具有适当挑战性的终端任务，以提升终端智能体的训练效果和数据可迁移性。开发者或研究者可利用它生成高质量训练样本，尤其在需要跨不同求解器保持一致表现的项目中。

### 可以推断的
推测：通过让任务难度随求解器表现动态调整，训练得到的智能体在面对能力不同的求解器时更可能保持鲁棒。  
推测：在多求解器环境中进行校准，意味着该方法有助于提升任务在不同工具链或平台之间的通用性。

## 来源摘要/节选

> Training terminal agents requires executable and verifiable tasks that are not merely solvable, but appropriately challenging for learning. Executable validation establishes feasibility, yet does not reveal how a task behaves relative to a given solver setting. In this paper, we present CalibForge, an autonomous terminal-task synthesis system that uses verified solver behavior to revise candidate tasks through adversarial solver calibration. Multi-solver calibration targets disagreement within a heterogeneous solver pool, whereas contrastive solver calibration targets a designated strong-pass/weak-fail relation; both operationalize a solver-relative learnable zone anchored in demonstrated solvability. Using CalibForge, we construct 5,431 calibrated terminal tasks. Our ablations show that both strategies yield more effective supervision than authoring and validation alone or ordinary single-solver feedback. Models trained on the full collection achieve 32.58% and 47.57% on Terminal-Bench 2.0. The largest improvements over the corresponding base model reach 24.71 percentage points on Terminal-Bench 2.0, 27.68 points on SWE-bench Pro, and 30.04 points on Doc2Repo. Together, these results support solver-relative learnability as a practical target for constructing effective and transferable agent training data.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。