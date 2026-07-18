---
title: 'CATTO: Balancing Preferences and Confidence in Language Models'
date: 2026-02-02 02:57:13+08:00
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
external_url: https://arxiv.org/abs/2601.23096v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:5d02db49639203226c40780342da5305129fcacef1e08e5e422c7c3152af3933
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
captured_at: '2026-07-18T04:10:00.628947Z'
source_capture_sha256: sha256:25a13e8026cc78f8e1aa96e51bf9d63120b87295d16f8fc6c2cee09045146cf8
source_capture_chars_original: 1250
source_publication_excerpt_chars: 1250
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23096v1](<https://arxiv.org/abs/2601.23096v1>)
- **作者**: Nisarg Parikh, Kunjal Panchal, Ananya Sai, Pannaga Shivaswamy, Andrew Lan
- **分类**: cs.LG
- **论文时间**: 2026-01-30T15:43:38Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23096v1.pdf](<https://arxiv.org/pdf/2601.23096v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) often make accurate next token predictions but their confidence in these predictions can be poorly calibrated: high-confidence predictions are frequently wrong, and low-confidence predictions may be correct. This miscalibration is exacerbated by preference-based alignment methods breaking the link between predictive probability and correctness. We introduce a Calibration Aware Token-level Training Objective \(CATTO\), a calibration-aware objective that aligns predicted confidence with empirical prediction correctness, which can be combined with the original preference optimization objectives. Empirically, CATTO reduces Expected Calibration Error \(ECE\) by 2.22%-7.61% in-distribution and 1.46%-10.44% out-of-distribution compared to direct preference optimization \(DPO\), and by 0.22%-1.24% in-distribution and 1.23%-5.07% out-of-distribution compared to the strongest DPO baseline. This improvement in confidence does not come at a cost of losing task accuracy, where CATTO maintains or slightly improves multiple-choice question-answering accuracy on five datasets. We also introduce Confidence@k, a test-time scaling mechanism leveraging calibrated token probabilities for Bayes-optimal selection of output tokens.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
