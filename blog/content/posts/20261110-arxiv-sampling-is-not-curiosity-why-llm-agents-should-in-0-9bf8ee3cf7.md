---
title: "Sampling Is Not Curiosity: Why LLM Agents Should Investigate"
date: 2026-11-10T10:07:47+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:86aae4313803fa4d2e90e0cb0456a535ede9e1b541c367ec9ca01b9c53109c26"
source_payload_sha256: "sha256:2bca3abcbba9e3dee1495433b4f2b966b0d2cfa60390f856c96e592f217d8b8a"
observation_id: obs_9bf8ee3cf74288a31c86d214fac38cb139d30b2db159eecd0521043bf3466ca5
event_id: evt_046948033f609193161b1cdd8dc7915cb3fd94f413db4c18afa644c97a4cb051
revision_id: rev_c1f3443b739e51bc9e3c4c41b56d2eee5bc4b63655f6c3cfcc73ca5df7508c5a
source_published_at: 2026-11-07T06:02:37Z
first_seen_at: 2026-11-10T02:06:19.665531Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
interpretation_sha256: "sha256:acb8fc6fe52b9028504c00ba2a9f3e518165736aaeec5fbac3ec8a611e537c09"
description: "这篇论文区分了 LLM 智能体的随机探索与真正的“好奇心”：温度、best-of-N、树搜索或 RAG 只能改变采样方式或条件，不会更新智能体对环境的认识。作者提出界定好奇心的框架，强调从交互中在线改进的环境预测、用预期改进指导行动，以及跨上下文窗口保留学习结果。"
external_url: http://arxiv.org/abs/2611.10501v1
parent_observation_id: null
last_seen_at: 2026-11-10T02:06:19.665531Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.10501v1](http://arxiv.org/abs/2611.10501v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Alfonso Amayuelas、Piotr Piękos、Xin Eric Wang 等

## 要点解读

### 这是什么
这篇论文区分了 LLM 智能体的随机探索与真正的“好奇心”：温度、best-of-N、树搜索或 RAG 只能改变采样方式或条件，不会更新智能体对环境的认识。作者提出界定好奇心的框架，强调从交互中在线改进的环境预测、用预期改进指导行动，以及跨上下文窗口保留学习结果。

### 用在哪里
适用于设计和评估开放式研究任务中的 LLM 智能体，尤其是需要自主决定调查方向并持续与环境交互的系统。它也为如何让这类智能体具备严格意义上的好奇心提供了研究框架。

### 可以推断的
- 推测：这篇论文主要提出概念定义和研究方向，而非给出完整的智能体实现。
- 推测：若系统仅增加采样随机性或搜索强度，却没有从交互中更新对环境的预测，就不符合论文给出的好奇心标准。

## 来源摘要/节选

> LLM agents are increasingly used for open-ended tasks, very common in research scenarios where they are required to explore, investigate, or act curiously. At inference time, an LLM is a fixed map from context to next-token distribution, the pretrained weights determine the function, and only its conditioning changes as context accumulates. Mechanisms like temperature, best-of-N, tree search, or RAG vary how the distribution is sampled or what it is conditioned on, but do not update the agent's model of the environment. We argue that current LLM agents do not explore curiously; they explore stochastically. From how curiosity is understood in the RL literature, it requires a predictive structure over how the environment responds to the agent's actions, which improves online from current interaction, drives action selection through its predicted improvement, and persists beyond the context window. Additionally, in its open-ended form, the agent should intrinsically originate what to investigate. Thus, we propose a framework defining curiosity in LLM agents, reserving the term for systems that satisfy it. In doing so, we identify the research directions its implementation opens up.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。