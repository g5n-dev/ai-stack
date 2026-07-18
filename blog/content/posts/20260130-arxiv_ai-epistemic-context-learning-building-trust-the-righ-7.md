---
title: 'Epistemic Context Learning: Building Trust the Right Way in LLM-Based Multi-Agent
  Systems'
date: 2026-01-30 03:54:32+08:00
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
external_url: https://arxiv.org/abs/2601.21742v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2b69a14ee99ea03f9c202e3b5764849c189221d82612fcc69efd2983c5144e79
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:09:48.978849Z'
source_capture_sha256: sha256:771088596d8f9d87e7bbf2b518601894194ac35133977b71814bfca329a0cd2e
source_capture_chars_original: 1255
source_publication_excerpt_chars: 1255
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21742v1](<https://arxiv.org/abs/2601.21742v1>)
- **作者**: Ruiwen Zhou, Maojia Song, Xiaobao Wu, Sitao Cheng, Xunjian Yin, Yuxi Xie, Zhuoqun Hao, Wenyue Hua, Liangming Pan, Soujanya Poria, Min-Yen Kan
- **分类**: cs.AI
- **论文时间**: 2026-01-29T13:59:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21742v1.pdf](<https://arxiv.org/pdf/2601.21742v1.pdf>)

## 来源摘要/节选

> Individual agents in multi-agent \(MA\) systems often lack robustness, tending to blindly conform to misleading peers. We show this weakness stems from both sycophancy and inadequate ability to evaluate peer reliability. To address this, we first formalize the learning problem of history-aware reference, introducing the historical interactions of peers as additional input, so that agents can estimate peer reliability and learn from trustworthy peers when uncertain. This shifts the task from evaluating peer reasoning quality to estimating peer reliability based on interaction history. We then develop Epistemic Context Learning \(ECL\): a reasoning framework that conditions predictions on explicitly-built peer profiles from history. We further optimize ECL by reinforcement learning using auxiliary rewards. Our experiments reveal that our ECL enables small models like Qwen 3-4B to outperform a history-agnostic baseline 8x its size \(Qwen 3-30B\) by accurately identifying reliable peers. ECL also boosts frontier models to near-perfect \(100%\) performance. We show that ECL generalizes well to various MA configurations and we find that trust is modeled well by LLMs, revealing a strong correlation in trust modeling accuracy and final answer quality.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
