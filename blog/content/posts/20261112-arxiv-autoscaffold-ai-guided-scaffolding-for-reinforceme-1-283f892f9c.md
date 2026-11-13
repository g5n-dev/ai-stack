---
title: "AutoScaffold: AI-Guided Scaffolding for Reinforcement Learning of Language Models"
date: 2026-11-12T10:59:23+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:fc84b93ad531339b95163bb741e13447904bee11f9c6f0a9853ac46bc9ff5bb8"
source_payload_sha256: "sha256:bb88790944f35e596f15a953230ebcfbc292eb4cb27e36321e5250b00c23beb1"
observation_id: obs_283f892f9c4f657a50323449300c5e6de7e0f8c29be06b2e06c04cf6c3632ef6
event_id: evt_c72da122802c78cfeb42acc15d57a8ffa56c6bba7956625ffe0559f88634a1c4
revision_id: rev_4d1849270a5fac435417522f125598991412e36df5af6c48645fac38f173706b
source_published_at: 2026-11-10T18:58:46Z
first_seen_at: 2026-11-12T03:09:22Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
interpretation_sha256: "sha256:d3dcb8e08090fe5cb1bd670b87774b5d793bead7ee63af98eefb1da1aa55e0d9"
description: "AutoScaffold 是一种面向强化学习的自适应辅助框架：由冻结的教师模型分析学生的训练经验，诊断不同任务中的瓶颈，并动态设计通用策略或针对性提示。辅助内容会在评估阶段移除，训练后的学生模型在四个任务领域均优于对应的强化学习基线。"
external_url: http://arxiv.org/abs/2611.14515v1
parent_observation_id: null
last_seen_at: 2026-11-13T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.14515v1](http://arxiv.org/abs/2611.14515v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Zijian Zhang、Rizhen Hu、Jiangweizhi Peng 等

## 要点解读

### 这是什么
AutoScaffold 是一种面向强化学习的自适应辅助框架：由冻结的教师模型分析学生的训练经验，诊断不同任务中的瓶颈，并动态设计通用策略或针对性提示。辅助内容会在评估阶段移除，训练后的学生模型在四个任务领域均优于对应的强化学习基线。

### 用在哪里
它适用于通过可验证奖励训练语言模型的场景，尤其适合需要从失败经验中提取策略、再将其转化为训练提示的研究者。实验覆盖 ALFWorld、搜索式问答、数学推理和 GPU 内核生成。

### 可以推断的
- 推测：相比依赖人工为每个领域设计训练提示，这种自动生成并调整辅助内容的方式可能减少训练阶段的人工干预。
- 推测：对于既关注最终奖励、又希望利用中间失败信息的团队，AutoScaffold 可能具有较高的实验价值。

## 来源摘要/节选

> Reinforcement learning with verifiable rewards (RLVR) produces rich training experience, yet outcome rewards reduce each attempt to a single number and leave most of this information unused. Training-time scaffolds, such as strategies or hints added to the prompt during training, offer a natural way to turn this information into guidance, but their design and adaptation are largely left to humans and tailored to specific domains. We introduce AutoScaffold, a unified AI-for-AI framework that turns a student's training experience into adaptive scaffolds, with minimal domain-specific information and no human intervention during training. A frozen teacher periodically examines this experience, diagnoses bottlenecks, and designs scaffolds in two forms: (i) strategies shared across a class of tasks and (ii) hints for individual hard tasks, adjusting the content and amount of support as the student learns. The scaffolds are removed at evaluation. We apply the same framework to ALFWorld, search-based QA, mathematical reasoning, and GPU kernel generation. When evaluated without scaffolds, students trained with AutoScaffold outperform those trained with the corresponding RL baselines in all four domains, with gains of 7.2 points in ALFWorld success and 4.0 points in average QA exact match. On GPU kernel generation, AutoScaffold increases the fraction of tasks with a correct kernel that runs faster than the PyTorch reference by up to 5.0 points. On math, our student surpasses QuestA's reported accuracy using approximately one-third as many student training steps. Analyses show that the teacher identifies a different failure in each task class and shifts its scaffolds from step-by-step workflows to targeted fixes as the student improves, and that its revised scaffolds help the student learn more than keeping the previous scaffold or using no scaffold.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。