---
title: 'Biases in the Blind Spot: Detecting What LLMs Fail to Mention'
date: 2026-02-11 23:34:28+08:00
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
external_url: https://arxiv.org/abs/2602.10117v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c337c001a139ce22cf55e797c99efe087b12c2bee17e80760cc64424d288723f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:14:36.051132Z'
source_capture_sha256: sha256:dd6b3974f681b2b65e9e138411bb0047428dc2bcd58acbca1d0b3c5c5b56f5bb
source_capture_chars_original: 1412
source_publication_excerpt_chars: 1412
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10117v1](<https://arxiv.org/abs/2602.10117v1>)
- **作者**: Iván Arcuschin, David Chanin, Adrià Garriga-Alonso, Oana-Maria Camburu
- **分类**: cs.LG
- **论文时间**: 2026-02-10T18:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10117v1.pdf](<https://arxiv.org/pdf/2602.10117v1.pdf>)

## 来源摘要/节选

> Large Language Models \(LLMs\) often provide chain-of-thought \(CoT\) reasoning traces that appear plausible, but may hide internal biases. We call these \*unverbalized biases\*. Monitoring models via their stated reasoning is therefore unreliable, and existing bias evaluations typically require predefined categories and hand-crafted datasets. In this work, we introduce a fully automated, black-box pipeline for detecting task-specific unverbalized biases. Given a task dataset, the pipeline uses LLM autoraters to generate candidate bias concepts. It then tests each concept on progressively larger input samples by generating positive and negative variations, and applies statistical techniques for multiple testing and early stopping. A concept is flagged as an unverbalized bias if it yields statistically significant performance differences while not being cited as justification in the model's CoTs. We evaluate our pipeline across six LLMs on three decision tasks \(hiring, loan approval, and university admissions\). Our technique automatically discovers previously unknown biases in these models \(e.g., Spanish fluency, English proficiency, writing formality\). In the same run, the pipeline also validates biases that were manually identified by prior work \(gender, race, religion, ethnicity\). More broadly, our proposed approach provides a practical, scalable path to automatic task-specific bias discovery.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
