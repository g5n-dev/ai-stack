---
title: Training LLMs for Divide-and-Conquer Reasoning Elevates Test-Time Scalability
date: 2026-02-03 23:08:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.02477v1
aliases:
- /posts/20260204-arxiv_ai-training-llms-for-divide-and-conquer-reasoning-ele-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2fbeb1580eefc3fbe3b1b9d22c3fb6430027a85d7ee85ea6b848cbfe8a771142
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:10:41.702374Z'
source_capture_sha256: sha256:f70b792922b85a99ed1a37fc786f9bab2357e19c1651bba2e5601d5b67f58ff4
source_capture_chars_original: 1321
source_publication_excerpt_chars: 1321
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02477v1](<https://arxiv.org/abs/2602.02477v1>)
- **作者**: Xiao Liang, Zhong-Zhi Li, Zhenghao Lin, Eric Hancheng Jiang, Hengyuan Zhang, Yelong Shen, Kai-Wei Chang, Ying Nian Wu, Yeyun Gong, Weizhu Chen
- **分类**: cs.CL
- **论文时间**: 2026-02-02T18:54:54Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02477v1.pdf](<https://arxiv.org/pdf/2602.02477v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) have demonstrated strong reasoning capabilities through step-by-step chain-of-thought \(CoT\) reasoning. Nevertheless, at the limits of model capability, CoT often proves insufficient, and its strictly sequential nature constrains test-time scalability. A potential alternative is divide-and-conquer \(DAC\) reasoning, which decomposes a complex problem into subproblems to facilitate more effective exploration of the solution. Although promising, our analysis reveals a fundamental misalignment between general-purpose post-training and DAC-style inference, which limits the model's capacity to fully leverage this potential. To bridge this gap and fully unlock LLMs' reasoning capabilities on the most challenging tasks, we propose an end-to-end reinforcement learning \(RL\) framework to enhance their DAC-style reasoning capacity. At each step, the policy decomposes a problem into a group of subproblems, solves them sequentially, and addresses the original one conditioned on the subproblem solutions, with both decomposition and solution integrated into RL training. Under comparable training, our DAC-style framework endows the model with a higher performance ceiling and stronger test-time scalability, surpassing CoT by 8.6% in Pass@1 and 6.3% in Pass@32 on competition-level benchmarks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
