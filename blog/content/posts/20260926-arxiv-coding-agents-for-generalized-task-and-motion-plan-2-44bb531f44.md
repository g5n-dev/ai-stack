---
title: "Coding Agents for Generalized Task and Motion Planning Problems"
date: 2026-09-26T21:07:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:40c4142563c9554fd6b2db0f9a9f9fc24e5dc21a4464b754aaae8a413419a4e7"
source_payload_sha256: "sha256:aefa22907b422cf8c095091f0e1e0918c0d0138ca45a68d1733a1c70e24f6a31"
observation_id: obs_44bb531f443ceb5140b460fa71e2e28d5420408a56410c95a0495fd4f52389f8
event_id: evt_7109c4e5783d94f89dd0df9e35cabc47329ed866482f40b972dfe9a9b536cea5
revision_id: rev_8def3a4675ce69e897af4773f1f9253f952ae3fb77e5432c8da9cf444510b00a
source_published_at: 2026-09-24T17:53:35Z
first_seen_at: 2026-09-26T13:17:23Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
interpretation_sha256: "sha256:a7f2673ea41dca8d5646429016475ef9ed4721479b9ca4ffca6c24a677674766"
description: "该研究探讨了编码代理能否通过合成可在不同问题实例间复用的程序，来降低任务与运动规划的计算复杂度。实验对比了代理生成程序与手工规划器的表现。"
external_url: http://arxiv.org/abs/2609.30233v1
parent_observation_id: null
last_seen_at: 2026-09-26T13:04:50.528015Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30233v1](http://arxiv.org/abs/2609.30233v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Matteo Merler、Bowen Li、Josh Roy 等

## 要点解读

### 这是什么
该研究探讨了编码代理能否通过合成可在不同问题实例间复用的程序，来降低任务与运动规划的计算复杂度。实验对比了代理生成程序与手工规划器的表现。

### 用在哪里
适合关注机器人规划、智能体程序合成或大语言模型实际应用的研究者和工程师阅读。涉及模拟环境中的任务规划与程序泛化能力评估。

### 可以推断的
推测：编码代理在生成可复用的规划程序上展现出优势，尤其在问题规模扩大时，相比传统规划器能更高效地完成任务。  
推测：代理程序通过与环境交互进行调试和优化的策略，可能是其优于一次性生成方法的关键因素。

## 来源摘要/节选

> Task and motion planning (TAMP) problems remain difficult even with full observability and object-centric states because discrete decisions are tightly coupled to geometric, kinematic, and dynamic constraints. Generalized TAMP addresses this difficulty by exploiting regularities across problem instances to reduce planning effort on new instances. However, existing methods require substantial TAMP-specific engineering. We investigate whether coding agents can automate this process by synthesizing programs that generalize across instances. Given a task description and simulator access, each agent chooses how to interact with the environment while developing a program within a fixed synthesis budget. The program is then frozen and evaluated on unseen instances. We evaluate Claude Code (Opus 5) and Codex (GPT-5.6 Sol and GPT-6 Astra) on 28 simulated environments from KinDER and PDDLStream, with object counts beyond those evaluated in the original benchmark. Across all program synthesis methods, we evaluate 980 generated programs on 100 held-out instances each, 98,000 evaluation episodes in total. Overall, we find that coding agents are surprisingly effective at generalized TAMP: all three agent configurations outperform hand-engineered planners, one-shot generation, and an LLM-based generalized planning baseline in mean success (56% to 95% versus 47% for the planners, on the 16 environments where a planner is available). As object counts grow, the agents' programs maintain higher success than the planner, using an order of magnitude less computation per instance on average. Logs show agents using interaction to calibrate physical models, test edge cases, and refine strategies. We release all code, including the full prompts given to the agents. These findings suggest that coding agents are a strong baseline for generalized TAMP.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。