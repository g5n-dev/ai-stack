---
title: "Procedural Graphs: Self-Evolving Execution Structures for LLM Agents"
date: 2026-09-10T02:38:15+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:020548df1793d2e67dce6cb4559994ed5ee481f25bb0d73d822ce8e43425f174"
source_payload_sha256: "sha256:e05380d97fb22085abb2a7a59c3ede8b6551ea3ae16a0d3e17d46ccd8de5fac4"
observation_id: obs_72fa48e079e0107a8627771fd8d9ec4ae3a9ca2be94e93d11e43bcc7a11ae264
event_id: evt_c470ff331532853725c29b1e303e9d55b248ef804c6676e696b71d5d478cd97c
revision_id: rev_f5408b8c4ea0ea1cc7f7f2dcef8940d12d355c100222a741795eeb1df508ffd7
source_published_at: 2026-09-08T17:59:41Z
first_seen_at: 2026-09-09T18:48:45Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
interpretation_sha256: "sha256:1f62ff777470e2a767ed36eeb2d7a313c788cb991e4a78c1644270cd8a400648"
description: "该研究提出一种名为“程序图”的结构，将流程性知识表示为（步骤，关系，步骤）的三元组，用于在每个决策点为大型语言模型提供情境指导，并通过自进化机制在成功与失败轨迹的对比中自动更新图的拓扑与属性。"
external_url: http://arxiv.org/abs/2609.09153v1
parent_observation_id: null
last_seen_at: 2026-09-09T18:35:42.790606Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.09153v1](http://arxiv.org/abs/2609.09153v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Yuxing Lu、Yicheng Chen、Shanchan Wu 等

## 要点解读

### 这是什么
该研究提出一种名为“程序图”的结构，将流程性知识表示为（步骤，关系，步骤）的三元组，用于在每个决策点为大型语言模型提供情境指导，并通过自进化机制在成功与失败轨迹的对比中自动更新图的拓扑与属性。

### 用在哪里
适用于需要长期规划并调用外部工具的智能体系统，可帮助开发者在构建自动化任务流时提升执行顺序的正确性并抑制重复操作。

### 可以推断的
推测：在需要频繁调整业务流程的实际应用中，这种自进化图结构有望降低人工设计的成本。  
推测：在实际部署时，图的规模与推理时延之间可能需要权衡。

## 来源摘要/节选

> Large language models are increasingly deployed as agents that plan over long horizons and act through external tools. Most agents select actions through unconstrained generation over an accumulating history, leaving implicit the procedural knowledge of what to do, in what order, and under which conditions. As trajectories lengthen, agents can lose track of their objectives, invoke tools out of order, and repeat unproductive actions. We introduce the Procedural Graph: just as a knowledge graph organizes factual knowledge into (entity, relation, entity) triplets for what-is questions, a Procedural Graph organizes procedural knowledge into (procedure, relation, procedure) triplets for what-to-do questions. At each decision step, the framework localizes the agent's active node, and a guidance model translates the surrounding subgraph into step-level situational guidance that biases the solver's next action without dictating it. The graph is self-evolving: an LLM refiner contrasts failed trajectories with successful ones and edits the graph's topology and attributes, committing edits that preserve or improve held-out validation performance while retaining rejected ones to discourage repetition. Starting from a minimal skeleton, the loop builds graphs that match or surpass hand-designed ones. It can also repair a flawed expert prior. Across multiple datasets, task types, and LLMs, the Procedural Graph delivers consistent gains over memory-based baselines, and self-evolution further improves performance without manual engineering.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。