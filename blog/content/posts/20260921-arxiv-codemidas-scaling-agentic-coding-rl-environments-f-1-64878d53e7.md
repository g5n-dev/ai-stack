---
title: "CodeMidas: Scaling Agentic Coding RL Environments from Code Itself"
date: 2026-09-21T18:45:07+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:411d483029d9e64255783e1e0d80ebf857ce5938b6b7bb7a3b850774cec14007"
source_payload_sha256: "sha256:1a7093a1dd4bd0b758b42b5d31231f9fd7ab1a74f47e5607d0371fb647c1f64e"
observation_id: obs_64878d53e7a8d0ca9cac85d0702d51e7d9185a1e7575ad6839776f7430648460
event_id: evt_2118a5c4257d603d33c3badaa14da82a6ec2a47ce2394a21306c00036ca5ecde
revision_id: rev_caa050b4d56c8ef656cf7e0e2b7038140aeb8228f305a16d8577e1781772f22a
source_published_at: 2026-09-18T17:55:17Z
first_seen_at: 2026-09-21T10:55:34Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
interpretation_sha256: "sha256:ee798d7bffa1ec08340b473cc315498e7e2d6e7a5221cf154adc6ced45a53736"
description: "CodeMidas 将开源代码库中已实现的功能转化为可执行的强化学习环境，用代理探索代码行为、自动生成测试并筛选任务，形成覆盖多种语言和领域的大规模训练数据集，用于提升编码代理在问题修复、整体程序构建以及终端工作等任务上的表现。"
external_url: http://arxiv.org/abs/2609.22068v1
parent_observation_id: null
last_seen_at: 2026-09-21T10:42:52.966512Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.22068v1](http://arxiv.org/abs/2609.22068v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Bowen Ye、Lei Li、Shicheng Li 等

## 要点解读

### 这是什么
CodeMidas 将开源代码库中已实现的功能转化为可执行的强化学习环境，用代理探索代码行为、自动生成测试并筛选任务，形成覆盖多种语言和领域的大规模训练数据集，用于提升编码代理在问题修复、整体程序构建以及终端工作等任务上的表现。

### 用在哪里
适用于需要大量多样化编程任务的强化学习训练场景，特别是想从真实代码库快速构建训练数据的研究者和团队。

### 可以推断的
推测：自动化生成任务和测试能够显著降低人工标注成本，并提升任务的可执行性。  
推测：任务数量和质量的提升有助于增强代理在真实开发环境中的适应能力和问题解决范围。

## 来源摘要/节选

> Training capable coding agents via reinforcement learning (RL) requires diverse tasks with reliable verifiers. Open-source codebases offer a rich source of such tasks, while existing methods typically rely on development artifacts such as issues and commits, limiting the range of tasks that can be extracted. To better scale RL environments, we present CodeMidas, an agentic pipeline that turns implemented functionality in existing codebases into executable RL environments using source code as its only task-specific input. CodeMidas allocates agentic compute to every stage of environment construction: agents explore implemented functionality to formulate behavioral specifications, construct tests grounded in execution of the original code, and validate and filter candidate tasks through execution checks and repeated solution rollouts. The resulting dataset has 5,545 training tasks from 3,185 open-source codebases spanning 23 programming languages and 15 technical domains. Training MiMo-V2.5 on these tasks with GRPO improves performance on all five diverse benchmarks, covering issue repair (DeepSWE + 11.7%), whole-program construction (ProgramBench +17%), and terminal work (Terminal-Bench v2.1 +8.5%). Ablations show that increasing the number of high-quality training tasks improves performance. Trajectory analysis shows the RL-trained agent demonstrates better behaviors like increasing codebase exploration and more diverse self-verification. These results establish source code as a scalable foundation for constructing RL environments that improve coding agents across diverse software tasks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。