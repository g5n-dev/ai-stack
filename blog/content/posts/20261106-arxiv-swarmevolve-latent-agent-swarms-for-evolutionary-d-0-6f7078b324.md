---
title: "SwarmEvolve: Latent Agent Swarms for Evolutionary Discovery and Optimization"
date: 2026-11-06T23:02:42+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ed08745ff4036b45f6fd33d7bb756ef27801522e83bdc81e4419dfe895221336"
source_payload_sha256: "sha256:5d0eb79fa395242bca9c1bd2f8fa9301c3fc8d257833f237aaf4cf8b300e0e48"
observation_id: obs_6f7078b324b1954466218c0ab514603989f805fdd1c106f8621d9fda98e8288f
event_id: evt_68cee360942b7e8efa12f49664464d286d4222103c8afad6fa67d9b2060e61b1
revision_id: rev_48cd81362568848a44e06c379142e5a02354f8e0bedb831f85795ce718d6f2a1
source_published_at: 2026-11-05T18:59:29Z
first_seen_at: 2026-11-06T15:10:15Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
interpretation_sha256: "sha256:ba4fb45bc327064080e3a2139fcbaedf0e7092d695272a592ba23f7dfc153023"
description: "SwarmEvolve 是一种利用大规模智能体群体进行进化式搜索的方法，让智能体在隐空间协作、共享 KV 缓存信息，并结合新颖性筛选与隐式交叉来生成和优化程序。实验显示，它在数学发现与科学计算任务上以更短时间取得了较高平均分。"
external_url: http://arxiv.org/abs/2611.08483v1
parent_observation_id: null
last_seen_at: 2026-11-06T15:01:36.718405Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08483v1](http://arxiv.org/abs/2611.08483v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Qile Jiang、George Em Karniadakis

## 要点解读

### 这是什么
SwarmEvolve 是一种利用大规模智能体群体进行进化式搜索的方法，让智能体在隐空间协作、共享 KV 缓存信息，并结合新颖性筛选与隐式交叉来生成和优化程序。实验显示，它在数学发现与科学计算任务上以更短时间取得了较高平均分。

### 用在哪里
该方法适合需要反复生成、评估和改进程序解的数学发现与科学计算任务。研究自动算法搜索、程序优化及多智能体协作的团队可以关注。

### 可以推断的
- 推测：隐空间通信与缓存复用可能显著减少重复生成文本推理带来的时间成本。
- 推测：按不同角度组织智能体群体，可能有助于扩大候选方案的多样性并提升搜索效率。

## 来源摘要/节选

> LLM-guided evolutionary search uses AI agents to improve programs for mathematical and computational problems by iteratively refining solutions and combining high-scoring methods. However, the process is often slow because the LLM generates a long textual chain of thought for each round and must repeat this generation many times to maintain population diversity. We present SwarmEvolve, a framework in which hundreds of low-cost agents per round work in swarms, reason in latent space without decoding to text, and share information by passing KV caches. Each swarm studies the problem from a different angle. A novelty filter keeps the most distinct agent ideas by directly measuring the distances between the agents' hidden state vectors. Crossover of ideas happens naturally in latent space, as a summarizer agent receives the combined KV caches of all swarm members. On 21 problems in mathematical discovery and scientific computing, SwarmEvolve gets the highest average score and needs a median of only 3 to 8 minutes to reach the best scores that other state-of-the-art frameworks reach in 60 minutes. On several problems, SwarmEvolve with Qwen3 8B improves on the solutions that AlphaEvolve first found with frontier LLMs. Our work shows that agent swarms that communicate in latent space offer a fast, low-cost approach to program search for scientific problems.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。