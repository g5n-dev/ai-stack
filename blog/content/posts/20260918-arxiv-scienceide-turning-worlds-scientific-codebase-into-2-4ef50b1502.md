---
title: "ScienceIDE: Turning World's Scientific Codebase into Agent Learnable Environments"
date: 2026-09-18T05:23:23+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4deb7d131d37a1ad7399fa2cb906050876f8059ef56595202e6b0ecd593a6cc4"
source_payload_sha256: "sha256:e646d6f4081a9eac3cde782f91a1af11f4425c8ab9e913bf4edb38d715cd6c39"
observation_id: obs_4ef50b1502c20a327d1d537d097240b2bfa294eaa9798cbb5c33c9dd83917f4d
event_id: evt_d16d5e3466fc1c3c3d33ac5a2b2195001d5d39c329755efceeed5e5c13d30ced
revision_id: rev_ca3b3b12c2f5cec4731cfcd41a185ea0e17120f3c85b8b032517906912c73c68
source_published_at: 2026-09-16T17:55:47Z
first_seen_at: 2026-09-17T21:32:20Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
interpretation_sha256: "sha256:185f2dd9c6726e13159e188a73c31b2ff31439cb6dcedd711fa47f81c40ec47b"
description: "ScienceIDE 是一种基础设施，把全球的科学代码库转化为可供 Agent 编程和执行的环境。它依据专家设定的案例与验收标准，让 Agent 将代码库自动生成可运行、可验证的任务。"
external_url: http://arxiv.org/abs/2609.19134v1
parent_observation_id: null
last_seen_at: 2026-09-18T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.19134v1](http://arxiv.org/abs/2609.19134v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Hejia Geng、Zesen Huang、Haoyang Li 等

## 要点解读

### 这是什么
ScienceIDE 是一种基础设施，把全球的科学代码库转化为可供 Agent 编程和执行的环境。它依据专家设定的案例与验收标准，让 Agent 将代码库自动生成可运行、可验证的任务。

### 用在哪里
适用于构建科研智能体的研发平台、需要自动化测试与验证代码的实验室，以及希望把科学软件纳入训练流程的团队。

### 可以推断的
推测：该框架可以显著降低为科学任务生成高质量训练样本的人工成本。  
推测：如果得到广泛采用，可能促使科学代码的复用和标准化进入新的阶段。

## 来源摘要/节选

> Scientific code repositories encode decades of human knowledge in executable models, methods, and tools. Yet fragmented toolchains, implicit domain conventions, and specialized correctness criteria make this knowledge difficult to convert into reliable learning experience-a challenge we call the scientific experience bottleneck. We introduce ScienceIDE, infrastructure for turning the world's scientific code into programmable environments for scientific agents. Guided by expert-defined scientific cases and acceptance criteria, agents transform repositories into executable environments that support task generation, execution, and scientific verification. These environments provide a shared foundation for supervised fine-tuning, reinforcement learning, and evaluation. Using verified interaction trajectories, we train PhAI-IDE-72B, PhAI-IDE-9B, and PhAI-IDE-4B. The model family shows gains in held-out scientific-code repair and across selected general-purpose benchmarks in code, reasoning, and knowledge, providing evidence of positive transfer from scientific experience to broader capabilities. ScienceIDE lays the foundation for an integrated workspace for agent learning and scientific practice, making humanity's scientific software a shared substrate for developing scientific intelligence. Code: https://github.com/aitofound/ScienceIDE

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。