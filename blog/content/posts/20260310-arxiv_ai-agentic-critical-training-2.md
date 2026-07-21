---
title: Agentic Critical Training
date: 2026-03-10 23:05:53+08:00
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
external_url: https://arxiv.org/abs/2603.08706v1
aliases:
- /posts/20260311-arxiv_ai-agentic-critical-training-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:66176ff594440182189b5d01d1634a6c8089e284014ca12291f4c560c649d3a3
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 25
captured_at: '2026-07-18T04:27:31.441787Z'
source_capture_sha256: sha256:79d86d0c1dbcaa4594c158e2a0cbbb21755cc0a8e03f75082c5ae33c12a8f61b
source_capture_chars_original: 1703
source_publication_excerpt_chars: 1703
observation_id: obs_f1b33835c7e855d9170266c7913675d3b92e44431391e123ff72e3e6bce12d52
revision_id: rev_08f6afc03019137d5a1aed538a61ff3ecfe1940a7978a0407155be1dc44d24a7
event_id: evt_c56b7ee4c768d1a71c20ee502fceda0d0b593c0af9ed5c1318873a67b08a2807
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-10T06:16:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08706v1](<https://arxiv.org/abs/2603.08706v1>)
- **作者**: Weize Liu, Minghui Liu, Sy-Tuyen Ho, Souradip Chakraborty, Xiyao Wang, Furong Huang
- **分类**: cs.AI
- **论文时间**: 2026-03-09T17:58:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08706v1.pdf](<https://arxiv.org/pdf/2603.08706v1.pdf>)

## 来源摘要/节选

> Training large language models \(LLMs\) as autonomous agents often begins with imitation learning, but it only teaches agents what to do without understanding why: agents never contrast successful actions against suboptimal alternatives and thus lack awareness of action quality. Recent approaches attempt to address this by introducing self-reflection supervision derived from contrasts between expert and alternative actions. However, the training paradigm fundamentally remains imitation learning: the model imitates pre-constructed reflection text rather than learning to reason autonomously. We propose Agentic Critical Training \(ACT\), a reinforcement learning paradigm that trains agents to identify the better action among alternatives. By rewarding whether the model's judgment is correct, ACT drives the model to autonomously develop reasoning about action quality, producing genuine self-reflection rather than imitating it. Across three challenging agent benchmarks, ACT consistently improves agent performance when combined with different post-training methods. It achieves an average improvement of 5.07 points over imitation learning and 4.62 points over reinforcement learning. Compared to approaches that inject reflection capability through knowledge distillation, ACT also demonstrates clear advantages, yielding an average improvement of 2.42 points. Moreover, ACT enables strong out-of-distribution generalization on agentic benchmarks and improves performance on general reasoning benchmarks without any reasoning-specific training data, highlighting the value of our method. These results suggest that ACT is a promising path toward developing more reflective and capable LLM agents.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
