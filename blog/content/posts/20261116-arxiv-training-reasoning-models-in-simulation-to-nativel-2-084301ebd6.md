---
title: "Training Reasoning Models in Simulation to Natively Use Real Robots"
date: 2026-11-16T17:40:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a342268501f1d3ff05847ead856374341f437fa5e0459da9874ffcbaf175d4db"
source_payload_sha256: "sha256:aa806dbd73dbcecdc36369ffd6199e2666473f5a274256426e0775f87232dc1a"
observation_id: obs_084301ebd6f9e5a465f93c04978347e6359694c288d5461e34fa2decd9106f92
event_id: evt_5e22b24ddc6dc9f11c3a9a5db79f693deb049ce9ebd3e0aebd96c58530f0e162
revision_id: rev_732c596e4dd5e11745187733d7ef711830819c217d5111d6153677ceb980988e
source_published_at: 2026-11-13T18:59:02Z
first_seen_at: 2026-11-16T09:49:35Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
interpretation_sha256: "sha256:78c7970f8225d57f4fb00a4aedaaf146cb083bb66ad0e8e1115d38877079a35e"
description: "这项研究提出 PEAR，通过机器人使用强化学习（RURL），仅在仿真环境中、无需示范数据地训练 27B 开源权重推理模型，使其能够直接为真实机器人生成末端执行器位姿。"
external_url: http://arxiv.org/abs/2611.18562v1
parent_observation_id: null
last_seen_at: 2026-11-16T09:38:50.691982Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.18562v1](http://arxiv.org/abs/2611.18562v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Jiaming Tang、Zhuoyang Zhang、Junxian Guo 等

## 要点解读

### 这是什么
这项研究提出 PEAR，通过机器人使用强化学习（RURL），仅在仿真环境中、无需示范数据地训练 27B 开源权重推理模型，使其能够直接为真实机器人生成末端执行器位姿。

### 用在哪里
它适用于通用机器人控制、双臂操作，以及需要为开源模型进行机器人能力后训练的研究场景。训练覆盖 LIBERO、RoboDojo 等仿真任务，并验证了向未见机器人、真实环境和新指令的迁移。

### 可以推断的
- 推测：纯仿真训练有望减少机器人后训练对真实交互数据和人工示范的依赖。
- 推测：强化学习与任务变化鲁棒性相结合，可能有助于提升模型面对非标准指令时的适应性。

## 来源摘要/节选

> Robot-use agents (RUAs) have emerged as a promising approach to general-purpose robot control. However, strong performance has so far been achieved only by frontier proprietary models such as GPT-6 Astra and Claude Fable 5.2, whereas open-weight models remain substantially less capable. We show that an open-weight 27B reasoning model can be trained to use real robots natively through reinforcement learning, entirely in simulation and without demonstrations. Like a computer-use agent (CUA), the model observes the environment, reasons in a chain of thought, and generates the next end-effector pose, without any harness. We build a Post-training Engine for Agentic Robotics (PEAR) and use it to train the model on simulated robot tasks at scale with robot-use reinforcement learning (RURL), mirroring how frontier models acquire computer use. We find that the skills acquired in simulation generalize well beyond the training tasks: they transfer to an unseen robot, to the real world, and to novel instructions. After training on LIBERO and RoboDojo in simulation, the model succeeds in 60% of our trials on a real dual-arm robot, whereas the base model succeeds in none. On LIBERO, training raises the success rate from 1.6% to 74.4%, approaching GPT-6 Astra and GPT-6.1 Sol at maximum reasoning effort. Compared with $π_{0.5}$, a vision-language-action model fine-tuned on demonstrations, our model is substantially more robust to changes in the task itself. On LIBERO-Pro, $π_{0.5}$ succeeds in only 0.75% of episodes when assigned a new task in a familiar scene whereas our model succeeds in 57.4%. Finally, the model retains its general capabilities, with no measurable degradation on nine reasoning, coding and vision benchmarks. These results highlight robot-use reinforcement learning as a promising component of foundation-model post-training.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。