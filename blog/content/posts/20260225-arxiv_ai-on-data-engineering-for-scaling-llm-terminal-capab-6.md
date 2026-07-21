---
title: On Data Engineering for Scaling LLM Terminal Capabilities
date: 2026-02-25 23:30:40+08:00
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
external_url: https://arxiv.org/abs/2602.21193v1
aliases:
- /posts/20260226-arxiv_ai-on-data-engineering-for-scaling-llm-terminal-capab-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2e5ba8ee7ea4744df59a1b3b43925ec945019ed549a2d926909bd23da6c757b0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
captured_at: '2026-07-18T04:16:49.996029Z'
source_capture_sha256: sha256:f0e5ef4271ce4b3d463c39000d515a259864d7cbd724a3a7bb11d511820b941d
source_capture_chars_original: 1230
source_publication_excerpt_chars: 1230
observation_id: obs_6b8016f68103ab575a89620d18bec7327d89594d0ceba19ee11db8a836db99e3
revision_id: rev_cfa755690012ad2c70ebe84a95690b8e089f1e528478efe04249f7d28d70dc20
event_id: evt_d936a9f93d166f1b9163fad72e95ea8b7218ce9a02cfbbe5ede3ce352a495d4e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T06:28:27Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21193v1](<https://arxiv.org/abs/2602.21193v1>)
- **作者**: Renjie Pi, Grace Lam, Mohammad Shoeybi, Pooya Jannaty, Bryan Catanzaro, Wei Ping
- **分类**: cs.CL
- **论文时间**: 2026-02-24T18:51:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21193v1.pdf](<https://arxiv.org/pdf/2602.21193v1.pdf>)

## 来源摘要/节选

> Despite rapid recent progress in the terminal capabilities of large language models, the training data strategies behind state-of-the-art terminal agents remain largely undisclosed. We address this gap through a systematic study of data engineering practices for terminal agents, making two key contributions: \(1\) Terminal-Task-Gen, a lightweight synthetic task generation pipeline that supports seed-based and skill-based task construction, and \(2\) a comprehensive analysis of data and training strategies, including filtering, curriculum learning, long context training, and scaling behavior. Our pipeline yields Terminal-Corpus, a large-scale open-source dataset for terminal tasks. Using this dataset, we train Nemotron-Terminal, a family of models initialized from Qwen3\(8B, 14B, 32B\) that achieve substantial gains on Terminal-Bench 2.0: Nemotron-Terminal-8B improves from 2.5% to 13.0% Nemotron-Terminal-14B improves from 4.0% to 20.2%, and Nemotron-Terminal-32B improves from 3.4% to 27.4%, matching the performance of significantly larger models. To accelerate research in this domain, we open-source our model checkpoints and most of our synthetic datasets at https://huggingface.co/collections/nvidia/nemotron-terminal.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
