---
title: 'Stop Unnecessary Reflection: Training LRMs for Efficient Reasoning with Adaptive
  Reflection and Length Coordinated Penalty'
date: 2026-02-13 03:01:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12113v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0141022f923f99db004f3b498aa18fd77bc45201bc3823d8ee8b20a6975ff75e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 122
captured_at: '2026-07-18T04:15:22.283119Z'
source_capture_sha256: sha256:19db2e7ffe60c7311e91216740bdbc79e19cd306b995fbe4d0689b4a4b6de3cd
source_capture_chars_original: 1696
source_publication_excerpt_chars: 1696
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12113v1](<https://arxiv.org/abs/2602.12113v1>)
- **作者**: Zewei Yu, Lirong Gao, Yuke Zhu, Bo Zheng, Sheng Guo, Haobo Wang, Junbo Zhao
- **分类**: cs.AI
- **论文时间**: 2026-02-12T16:04:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12113v1.pdf](<https://arxiv.org/pdf/2602.12113v1.pdf>)

## 来源摘要/节选

> Large Reasoning Models \(LRMs\) have demonstrated remarkable performance on complex reasoning tasks by employing test-time scaling. However, they often generate over-long chains-of-thought that, driven by substantial reflections such as repetitive self-questioning and circular reasoning, lead to high token consumption, substantial computational overhead, and increased latency without improving accuracy, particularly in smaller models. Our observation reveals that increasing problem complexity induces more excessive and unnecessary reflection, which in turn reduces accuracy and increases token overhead. To address this challenge, we propose Adaptive Reflection and Length Coordinated Penalty \(ARLCP\), a novel reinforcement learning framework designed to dynamically balance reasoning efficiency and solution accuracy. ARLCP introduces two key innovations: \(1\) a reflection penalty that adaptively curtails unnecessary reflective steps while preserving essential reasoning, and \(2\) a length penalty calibrated to the estimated complexity of the problem. By coordinating these penalties, ARLCP encourages the model to generate more concise and effective reasoning paths. We evaluate our method on five mathematical reasoning benchmarks using DeepSeek-R1-Distill-Qwen-1.5B and DeepSeek-R1-Distill-Qwen-7B models. Experimental results show that ARLCP achieves a superior efficiency-accuracy trade-off compared to existing approaches. For the 1.5B model, it reduces the average response length by 53.1% while simultaneously improving accuracy by 5.8%. For the 7B model, it achieves a 35.0% reduction in length with a 2.7% accuracy gain. The code is released at https://github.com/ZeweiYu1/ARLCP .

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
