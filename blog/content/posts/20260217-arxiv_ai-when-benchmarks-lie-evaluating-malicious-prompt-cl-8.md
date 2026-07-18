---
title: 'When Benchmarks Lie: Evaluating Malicious Prompt Classifiers Under True Distribution
  Shift'
date: 2026-02-17 03:10:02+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- AI 安全
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.14161v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9427df3cc7c183b3455aebf926e74f49748760d6c4df95e7aa037b2dda4058c2
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
captured_at: '2026-07-18T04:15:48.934783Z'
source_capture_sha256: sha256:68c451d702d29c1004ebcba8ea68542f9886b053f66f139d4434b16e45c3746d
source_capture_chars_original: 1773
source_publication_excerpt_chars: 1773
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.14161v1](<https://arxiv.org/abs/2602.14161v1>)
- **作者**: Max Fomin
- **分类**: cs.LG
- **论文时间**: 2026-02-15T14:21:43Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.14161v1.pdf](<https://arxiv.org/pdf/2602.14161v1.pdf>)

## 来源摘要/节选

> Detecting prompt injection and jailbreak attacks is critical for deploying LLM-based agents safely. As agents increasingly process untrusted data from emails, documents, tool outputs, and external APIs, robust attack detection becomes essential. Yet current evaluation practices and production systems have fundamental limitations. We present a comprehensive analysis using a diverse benchmark of 18 datasets spanning harmful requests, jailbreaks, indirect prompt injections, and extraction attacks. We propose Leave-One-Dataset-Out \(LODO\) evaluation to measure true out-of-distribution generalization, revealing that the standard practice of train-test splits from the same dataset sources severely overestimates performance: aggregate metrics show an 8.4 percentage point AUC inflation, but per-dataset gaps range from 1% to 25% accuracy-exposing heterogeneous failure modes. To understand why classifiers fail to generalize, we analyze Sparse Auto-Encoder \(SAE\) feature coefficients across LODO folds, finding that 28% of top features are dataset-dependent shortcuts whose class signal depends on specific dataset compositions rather than semantic content. We systematically compare production guardrails \(PromptGuard 2, LlamaGuard\) and LLM-as-judge approaches on our benchmark, finding all three fail on indirect attacks targeting agents \(7-37% detection\) and that PromptGuard 2 and LlamaGuard cannot evaluate agentic tool injection due to architectural limitations. Finally, we show that LODO-stable SAE features provide more reliable explanations for classifier decisions by filtering dataset artifacts. We release our evaluation framework at https://github.com/maxf-zn/prompt-mining to establish LODO as the appropriate protocol for prompt attack detection research.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
