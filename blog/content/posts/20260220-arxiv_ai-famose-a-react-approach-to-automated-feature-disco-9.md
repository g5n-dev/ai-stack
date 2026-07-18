---
title: 'FAMOSE: A ReAct Approach to Automated Feature Discovery'
date: 2026-02-20 22:59:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- 机器学习
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.17641v1
aliases:
- /posts/20260221-arxiv_ai-famose-a-react-approach-to-automated-feature-disco-9/
- /posts/20260222-arxiv_ai-famose-a-react-approach-to-automated-feature-disco-9/
- /posts/20260223-arxiv_ai-famose-a-react-approach-to-automated-feature-disco-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:79571b66cfe8f3e5f22ed2308377ca9322afd258e7c539edca60a14e3e041067
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
captured_at: '2026-07-18T04:16:04.060671Z'
source_capture_sha256: sha256:6f94d44e9c102b14daec3b18935d92057f29fde86ef609d77df905c696404896
source_capture_chars_original: 1514
source_publication_excerpt_chars: 1514
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.17641v1](<https://arxiv.org/abs/2602.17641v1>)
- **作者**: Keith Burghardt, Jienan Liu, Sadman Sakib, Yuning Hao, Bo Li
- **分类**: cs.LG
- **论文时间**: 2026-02-19T18:53:15Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.17641v1.pdf](<https://arxiv.org/pdf/2602.17641v1.pdf>)

## 来源摘要/节选

> Feature engineering remains a critical yet challenging bottleneck in machine learning, particularly for tabular data, as identifying optimal features from an exponentially large feature space traditionally demands substantial domain expertise. To address this challenge, we introduce FAMOSE \(Feature AugMentation and Optimal Selection agEnt\), a novel framework that leverages the ReAct paradigm to autonomously explore, generate, and refine features while integrating feature selection and evaluation tools within an agent architecture. To our knowledge, FAMOSE represents the first application of an agentic ReAct framework to automated feature engineering, especially for both regression and classification tasks. Extensive experiments demonstrate that FAMOSE is at or near the state-of-the-art on classification tasks \(especially tasks with more than 10K instances, where ROC-AUC increases 0.23% on average\), and achieves the state-of-the-art for regression tasks by reducing RMSE by 2.0% on average, while remaining more robust to errors than other algorithms. We hypothesize that FAMOSE's strong performance is because ReAct allows the LLM context window to record \(via iterative feature discovery and evaluation steps\) what features did or did not work. This is similar to a few-shot prompt and guides the LLM to invent better, more innovative features. Our work offers evidence that AI agents are remarkably effective in solving problems that require highly inventive solutions, such as feature engineering.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
