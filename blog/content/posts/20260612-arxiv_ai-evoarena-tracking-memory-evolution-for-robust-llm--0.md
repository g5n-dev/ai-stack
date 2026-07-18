---
title: 'EvoArena: Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments'
date: 2026-06-12 23:39:03+08:00
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
external_url: https://arxiv.org/abs/2606.13681v1
aliases:
- /posts/20260613-arxiv_ai-evoarena-tracking-memory-evolution-for-robust-llm--0/
- /posts/20260614-arxiv_ai-evoarena-tracking-memory-evolution-for-robust-llm--0/
- /posts/20260615-arxiv_ai-evoarena-tracking-memory-evolution-for-robust-llm--0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:406d5e4e1424efabe82fe0f27055cf9b2448c8bf1bfaf3646e165764c5e10f1c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
captured_at: '2026-07-18T04:30:02.047374Z'
source_capture_sha256: sha256:39684f13b65b1b7aaedfd5ee09d03b89941c021da64fd3ed37a212747ef2d9f2
source_capture_chars_original: 1508
source_publication_excerpt_chars: 1508
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.13681v1](<https://arxiv.org/abs/2606.13681v1>)
- **作者**: Jundong Xu, Qingchuan Li, Jiaying Wu, Yihuai Lan, Shuyue Stella Li, Huichi Zhou, Bowen Jiang, Lei Wang, Jun Wang, Anh Tuan Luu, Caiming Xiong, Hae Won Park, Bryan Hooi, Zhiyuan Hu
- **分类**: cs.CL
- **论文时间**: 2026-06-11T17:59:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.13681v1.pdf](<https://arxiv.org/pdf/2606.13681v1.pdf>)

## 来源摘要/节选

> Large language model \(LLM\) agents have achieved strong performance on a wide range of benchmarks, yet most evaluations assume static environments. In contrast, real-world deployment is inherently dynamic, requiring agents to continually align their knowledge, skills, and behavior with changing environments and updated task conditions. To address this gap, we introduce EvoArena, a benchmark suite that models environment changes as sequences of progressive updates across terminal, software, and social domains. We further propose EvoMem, a patch-based memory paradigm that records memory evolution as structured update histories, enabling agents to reason about environmental evolution through changes in their memory. Experiments show that current agents struggle on EvoArena, achieving an average accuracy of 39.6% across evolving terminal, software, and social-preference domains. EvoMem consistently improves performance, yielding an average gain of 1.5% on EvoArena and also improving standard benchmarks such as GAIA and LoCoMo by 6.1% and 4.8%. Beyond individual tasks, EvoMem further improves chain-level accuracy by 3.7% on EvoArena, where success requires completing a consecutive sequence of related evolutionary subtasks. Mechanistic analysis shows that EvoMem improves evidence capture in the memory, indicating better preservation of complete evolving environment states. Our results highlight the importance of modeling evolution in both evaluation and memory for reliable agent deployment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
