---
title: 'Code-A1: Adversarial Evolving of Code LLM and Test LLM via Reinforcement Learning'
date: 2026-03-17 20:30:33+08:00
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
external_url: https://arxiv.org/abs/2603.15611v1
aliases:
- /posts/20260318-arxiv_ai-code-a1-adversarial-evolving-of-code-llm-and-test--3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b0f30a31c457828d677081d114523f65f5e0d17f63c0d9cd276d27da8c944bb0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
captured_at: '2026-07-18T04:28:30.264258Z'
source_capture_sha256: sha256:12f1c17608a4a1ed3b76d56c663d3141aa72e8e2dd7baa8e840754a845662ad8
source_capture_chars_original: 1318
source_publication_excerpt_chars: 1318
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.15611v1](<https://arxiv.org/abs/2603.15611v1>)
- **作者**: Aozhe Wang, Yuchen Yan, Nan Zhou, Zhengxi Lu, Weiming Lu, Jun Xiao, Yueting Zhuang, Yongliang Shen
- **分类**: cs.CL
- **论文时间**: 2026-03-16T17:58:13Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.15611v1.pdf](<https://arxiv.org/pdf/2603.15611v1.pdf>)

## 来源摘要/节选

> Reinforcement learning for code generation relies on verifiable rewards from unit test pass rates. Yet high-quality test suites are scarce, existing datasets offer limited coverage, and static rewards fail to adapt as models improve. Recent self-play methods unify code and test generation in a single model, but face a inherent dilemma: white-box access leads to self-collusion where the model produces trivial tests for easy rewards, yet black-box restriction yields generic tests that miss implementation-specific bugs. We introduce Code-A1, an adversarial co-evolution framework that jointly optimizes a Code LLM and a Test LLM with opposing objectives. The Code LLM is rewarded for passing more tests, while the Test LLM is rewarded for exposing more defects. This architectural separation eliminates self-collusion risks and safely enables white-box test generation, where the Test LLM can inspect candidate code to craft targeted adversarial tests. We further introduce a Mistake Book mechanism for experience replay and a composite reward balancing test validity with adversarial difficulty. Experiments on Qwen2.5-Coder models demonstrate that Code-A1 achieves code generation performance matching or exceeding models trained on human-annotated tests, while significantly improving test generation capability.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
