---
title: 'CLI-Gym: Scalable CLI Task Generation via Agentic Environment Inversion'
date: 2026-02-12 02:48:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 命令行工具
categories:
- 论文
scenarios:
- AI/ML项目
- 命令行工具
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10999v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:90aed281c1fe7cba45abf1d2ba2d833d769cc83964a142f7cb5f57108bf7c9c9
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:14:51.451682Z'
source_capture_sha256: sha256:f0b094cc2a94826d7f9acbfb0930a6065bf7bc1908136dfce7b6162276dd3c92
source_capture_chars_original: 1179
source_publication_excerpt_chars: 1179
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10999v1](<https://arxiv.org/abs/2602.10999v1>)
- **作者**: Yusong Lin, Haiyang Wang, Shuzhe Wu, Lue Fan, Feiyang Pan, Sanyuan Zhao, Dandan Tu
- **分类**: cs.AI
- **论文时间**: 2026-02-11T16:22:18Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10999v1.pdf](<https://arxiv.org/pdf/2602.10999v1.pdf>)

## 来源摘要/节选

> Agentic coding requires agents to effectively interact with runtime environments, e.g., command line interfaces \(CLI\), so as to complete tasks like resolving dependency issues, fixing system problems, etc. But it remains underexplored how such environment-intensive tasks can be obtained at scale to enhance agents' capabilities. To address this, based on an analogy between the Dockerfile and the agentic task, we propose to employ agents to simulate and explore environment histories, guided by execution feedback. By tracing histories of a healthy environment, its state can be inverted to an earlier one with runtime failures, from which a task can be derived by packing the buggy state and the corresponding error messages. With our method, named CLI-Gym, a total of 1,655 environment-intensive tasks are derived, being the largest collection of its kind. Moreover, with curated successful trajectories, our fine-tuned model, named LiberCoder, achieves substantial absolute improvements of +21.1% \(to 46.1%\) on Terminal-Bench, outperforming various strong baselines. To our knowledge, this is the first public pipeline for scalable derivation of environment-intensive tasks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
