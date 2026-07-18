---
title: Causality is Key for Interpretability Claims to Generalise
date: 2026-02-19 22:55:31+08:00
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
external_url: https://arxiv.org/abs/2602.16698v1
aliases:
- /posts/20260220-arxiv_ai-causality-is-key-for-interpretability-claims-to-ge-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b5c3bb02a86bee556a99b28f90c6f345a835441894d53aa877a43284ab2f4692
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
captured_at: '2026-07-18T04:16:00.196393Z'
source_capture_sha256: sha256:554f2aded8889d8327c8047c2e0873f7f7af3666e3af15611a5dfb03e2450555
source_capture_chars_original: 1342
source_publication_excerpt_chars: 1342
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.16698v1](<https://arxiv.org/abs/2602.16698v1>)
- **作者**: Shruti Joshi, Aaron Mueller, David Klindt, Wieland Brendel, Patrik Reizinger, Dhanya Sridhar
- **分类**: cs.LG
- **论文时间**: 2026-02-18T18:45:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.16698v1.pdf](<https://arxiv.org/pdf/2602.16698v1.pdf>)

## 来源摘要/节选

> Interpretability research on large language models \(LLMs\) has yielded important insights into model behaviour, yet recurring pitfalls persist: findings that do not generalise, and causal interpretations that outrun the evidence. Our position is that causal inference specifies what constitutes a valid mapping from model activations to invariant high-level structures, the data or assumptions needed to achieve it, and the inferences it can support. Specifically, Pearl's causal hierarchy clarifies what an interpretability study can justify. Observations establish associations between model behaviour and internal components. Interventions \(e.g., ablations or activation patching\) support claims how these edits affect a behavioural metric \(\\eg, average change in token probabilities\) over a set of prompts. However, counterfactual claims -- i.e., asking what the model output would have been for the same prompt under an unobserved intervention -- remain largely unverifiable without controlled supervision. We show how causal representation learning \(CRL\) operationalises this hierarchy, specifying which variables are recoverable from activations and under what assumptions. Together, these motivate a diagnostic framework that helps practitioners select methods and evaluations matching claims to evidence such that findings generalise.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
