---
title: "Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation"
date: 2026-09-18T12:52:29+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "Prompt 工程", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:492305f85ca830f66b6c284ccc3e83fceb5969f4a1e7282ebc67609fb2f32f46"
source_payload_sha256: "sha256:da5263f57e6437a4612a68669ed92aefa3dcaebd4796c96f9ee5a82ec6d8fd9a"
observation_id: obs_e738f009e4d5f367618176a26eabaec69353ea1a79bbfad285810f08d52839b8
event_id: evt_cdd4e91118152304d7e2db3b877cafb1ba5443e23d21c65d65795bc176762e3c
revision_id: rev_3e2862ddeaf94d1b6f5835e215b2de307c98749dd1d3a882b2f1a6486d7094c0
source_published_at: 2026-09-17T17:59:58Z
first_seen_at: 2026-09-18T05:01:01Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:f59e873bb7d7c21ae3293e27c758416bef94d1cc1ae4c38210ec79d41dbcd385"
description: "该研究评估了代码生成式机器人在必须避开障碍物的任务中的安全表现，发现现有系统在规划时倾向于只关注任务完成而忽视避障。通过将操控分解为路径阶段和接触阶段，提出了名为 SafeHarness 的框架，分别为路径规划和接触执行配备障碍感知模块，使安全约束能够被优先考虑。"
external_url: http://arxiv.org/abs/2609.20822v1
parent_observation_id: null
last_seen_at: 2026-09-21T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20822v1](http://arxiv.org/abs/2609.20822v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Bingxin Xu、Yuzhang Shang、Zhen Dong 等

## 要点解读

### 这是什么  
该研究评估了代码生成式机器人在必须避开障碍物的任务中的安全表现，发现现有系统在规划时倾向于只关注任务完成而忽视避障。通过将操控分解为路径阶段和接触阶段，提出了名为 SafeHarness 的框架，分别为路径规划和接触执行配备障碍感知模块，使安全约束能够被优先考虑。

### 用在哪里  
适用于利用大语言模型生成控制代码的机器人研发团队，尤其是需要在程序化控制下实现安全避障的系统。安全关键的自动化装配、物流分拣或人机协作场景的设计者也可参考此方法进行安全约束的集成与验证。

### 可以推断的  
推测：引入障碍感知模块后，智能体在规划阶段可能需要额外的计算资源来生成和验证多条候选路径。  
推测：该方案有望迁移到其他类型的约束（如力度限制或姿态约束），只要在路径和接触层面分别加入相应的感知模块。

## 来源摘要/节选

> Coding agents have emerged as a promising paradigm for robot manipulation: a language model writes the robot controller as a program, and agents built in this way now operate robots without robot-specific training.Whether this paradigm is also safe, however, has not been asked. We evaluate coding agent under a safety constraint, where each task pairs a manipulation goal with an obstacle the robot must not touch. The agent pursues the goal but collides with the obstacle in most cases, treating task completion as its sole objective while neglecting safety. The agent reasons about the obstacle in its traces, and the prompt already forbids touching it, so neither perception nor instruction is at fault; the fault lies in the planning, where the stated constraint never becomes a priority. By decomposing manipulation into a route phase and a contact-rich moment, we locate the source of the failure. Along the route, the model cannot prioritize the safety constraint, having no notion of a clearing route and none of replanning once a chosen route becomes infeasible. At the contact, it is unaware that contact execution is bounded by the same constraint. To close this gap, we present SafeHarness, which equips the model with two obstacle-aware harnesses that enable it to prioritize the safety constraint. Obstacle-aware route planning grounds the objects as bounding boxes and draws candidate routes over them as sequences of waypoints. The agent then plans a route in advance, verifies it, replans when necessary, and only then executes it. Obstacle-aware contact execution instead selects the contact position so that the contact itself avoids the obstacle. SafeHarness attains 71.9% task success and 87.5% collision avoidance, surpassing the previous SOTA by 6.5% and 27.0%, respectively. These results are $2.3\times$ and $1.5\times$ those of the same agent without harnesses.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。