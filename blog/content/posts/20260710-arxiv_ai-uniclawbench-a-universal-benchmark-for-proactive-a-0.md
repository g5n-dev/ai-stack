---
title: 'UniClawBench: A Universal Benchmark for Proactive Agents on Real-World Tasks'
date: 2026-07-10 22:22:15+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- Docker
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2607.08768v1
aliases:
- /posts/20260711-arxiv_ai-uniclawbench-a-universal-benchmark-for-proactive-a-0/
- /posts/20260712-arxiv_ai-uniclawbench-a-universal-benchmark-for-proactive-a-0/
- /posts/20260713-arxiv_ai-uniclawbench-a-universal-benchmark-for-proactive-a-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f8e2a5697c32185de68dc0f158eb58e18a7480e8a2e60263e2ac685bc6865ec5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:30:25.647174Z'
source_capture_sha256: sha256:ba10828ed4aea0fe7907bcb3c98b3e6deca1e314aa1ff54310d6da506aedefcf
source_capture_chars_original: 1821
source_publication_excerpt_chars: 1821
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.08768v1](<https://arxiv.org/abs/2607.08768v1>)
- **作者**: Zhekai Chen, Chengqi Duan, Kaiyue Sun, Bohao Li, Yuqing Wang, Manyuan Zhang, Xihui Liu
- **分类**: cs.CL
- **论文时间**: 2026-07-09T17:59:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.08768v1.pdf](<https://arxiv.org/pdf/2607.08768v1.pdf>)

## 来源摘要/节选

> The rapid development of large language models and multimodal large language models has accelerated the emergence of proactive agents capable of operating everyday tools and assisting users in real-world environments. However, existing benchmarks struggle to evaluate such agents effectively, as they often rely on sandboxed environments and single-turn evaluation paradigms. Moreover, their scenario-based task taxonomies mix multiple model capabilities within the same task category, making it difficult to identify the root causes of agent failures. To address these limitations, we introduce UniClawBench, the first capability-driven benchmark designed to evaluate proactive agents in dynamic, real-world settings. UniClawBench is built around five foundational model capabilities: Skill Usage, Exploration, Long-Context Reasoning, Multimodal Understanding, and Cross-Platform Coordination. Based on these capabilities, we design 400 bilingual real-world tasks. Unlike previous benchmarks that rely on static, pre-recorded answers, our benchmark evaluates agents in live Docker containers using fine-grained, step-by-step completion checkpoints. Furthermore, we design a closed-loop evaluation strategy comprising an executor agent, a hidden supervisor agent, and a user agent to simulate realistic multi-turn human feedback without leaking grading criteria. To disentangle base model capabilities from framework-level design choices, we evaluate state-of-the-art models under multiple agent frameworks. Through comprehensive comparisons across both models and frameworks, we show how base model capabilities and agent framework designs jointly shape performance in real-world environments. To facilitate future research, we make our benchmark and code publicly available at https://github.com/HKU-MMLab/UniClawBench.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
