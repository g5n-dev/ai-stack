---
title: 'AgentDrive: An Open Benchmark Dataset for Agentic AI Reasoning with LLM-Generated
  Scenarios in Autonomous Systems'
date: 2026-01-26 22:15:20+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16964v1
aliases:
- /posts/20260127-arxiv_ai-agentdrive-an-open-benchmark-dataset-for-agentic-a-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c1f03701acbba52828d07ee3d3c0ceebbbd6205abe150f5ee3232c02bec2f5d7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 113
captured_at: '2026-07-18T04:09:03.986411Z'
source_capture_sha256: sha256:c2aa30db342e37e3059afa00238995dc78ba863a78650fcc8f708200ac82ebe0
source_capture_chars_original: 1635
source_publication_excerpt_chars: 1635
observation_id: obs_f67f6e7e182dee9d084972970dda9044c231ebf58f995a74c1d4bf19c48d2fed
revision_id: rev_5a61975289e4e5146c9099d023fe98c5df2df6eb9b4ec123c69aa5df72a24f26
event_id: evt_57657cefb989e3a5e14c77092101bad5c877c7009826a5f1e665627e17787d1a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16964v1](<https://arxiv.org/abs/2601.16964v1>)
- **作者**: Mohamed Amine Ferrag, Abderrahmane Lakas, Merouane Debbah
- **分类**: cs.AI
- **论文时间**: 2026-01-23T18:33:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16964v1.pdf](<https://arxiv.org/pdf/2601.16964v1.pdf>)

## 来源摘要/节选

> The rapid advancement of large language models \(LLMs\) has sparked growing interest in their integration into autonomous systems for reasoning-driven perception, planning, and decision-making. However, evaluating and training such agentic AI models remains challenging due to the lack of large-scale, structured, and safety-critical benchmarks. This paper introduces AgentDrive, an open benchmark dataset containing 300,000 LLM-generated driving scenarios designed for training, fine-tuning, and evaluating autonomous agents under diverse conditions. AgentDrive formalizes a factorized scenario space across seven orthogonal axes: scenario type, driver behavior, environment, road layout, objective, difficulty, and traffic density. An LLM-driven prompt-to-JSON pipeline generates semantically rich, simulation-ready specifications that are validated against physical and schema constraints. Each scenario undergoes simulation rollouts, surrogate safety metric computation, and rule-based outcome labeling. To complement simulation-based evaluation, we introduce AgentDrive-MCQ, a 100,000-question multiple-choice benchmark spanning five reasoning dimensions: physics, policy, hybrid, scenario, and comparative reasoning. We conduct a large-scale evaluation of fifty leading LLMs on AgentDrive-MCQ. Results show that while proprietary frontier models perform best in contextual and policy reasoning, advanced open models are rapidly closing the gap in structured and physics-grounded reasoning. We release the AgentDrive dataset, AgentDrive-MCQ benchmark, evaluation code, and related materials at https://github.com/maferrag/AgentDrive

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
