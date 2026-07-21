---
title: 'Agent World Model: Infinity Synthetic Environments for Agentic Reinforcement
  Learning'
date: 2026-02-11 23:34:28+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- 数据库
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10090v1
aliases:
- /posts/20260212-arxiv_ai-agent-world-model-infinity-synthetic-environments--7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e2726876ae3f638348a3b91f018a24d2daef52cb63a2e48ed34356dc3d9be6d7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:14:36.051132Z'
source_capture_sha256: sha256:5640e55e007f3dd22b5bdf042826336f15732bd40f90d8bc5329fe275d675f8b
source_capture_chars_original: 1365
source_publication_excerpt_chars: 1365
observation_id: obs_eef56d044eafdbc39a5bb5a7b5ad5e6faff01638322d77fd1cefb8f13b90fa44
revision_id: rev_03a2600b78da0133ca697497d2bcbd1174ee93cba5918bb3ef13e8556987d605
event_id: evt_cff608afb56439c5f3ed97fc1b753d8a8c40e84f9ef775c841fbb57bc8fd0455
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-11T17:11:39Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10090v1](<https://arxiv.org/abs/2602.10090v1>)
- **作者**: Zhaoyang Wang, Canwen Xu, Boyi Liu, Yite Wang, Siwei Han, Zhewei Yao, Huaxiu Yao, Yuxiong He
- **分类**: cs.AI
- **论文时间**: 2026-02-10T18:55:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10090v1.pdf](<https://arxiv.org/pdf/2602.10090v1.pdf>)

## 来源摘要/节选

> Recent advances in large language model \(LLM\) have empowered autonomous agents to perform complex tasks that require multi-turn interactions with tools and environments. However, scaling such agent training is limited by the lack of diverse and reliable environments. In this paper, we propose Agent World Model \(AWM\), a fully synthetic environment generation pipeline. Using this pipeline, we scale to 1,000 environments covering everyday scenarios, in which agents can interact with rich toolsets \(35 tools per environment on average\) and obtain high-quality observations. Notably, these environments are code-driven and backed by databases, providing more reliable and consistent state transitions than environments simulated by LLMs. Moreover, they enable more efficient agent interaction compared with collecting trajectories from realistic environments. To demonstrate the effectiveness of this resource, we perform large-scale reinforcement learning for multi-turn tool-use agents. Thanks to the fully executable environments and accessible database states, we can also design reliable reward functions. Experiments on three benchmarks show that training exclusively in synthetic environments, rather than benchmark-specific ones, yields strong out-of-distribution generalization. The code is available at https://github.com/Snowflake-Labs/agent-world-model.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
