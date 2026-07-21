---
title: Towards Provably Unbiased LLM Judges via Bias-Bounded Evaluation
date: 2026-03-06 23:44:05+08:00
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
external_url: https://arxiv.org/abs/2603.05485v1
aliases:
- /posts/20260307-arxiv_ai-towards-provably-unbiased-llm-judges-via-bias-boun-6/
- /posts/20260308-arxiv_ai-towards-provably-unbiased-llm-judges-via-bias-boun-6/
- /posts/20260309-arxiv_ai-towards-provably-unbiased-llm-judges-via-bias-boun-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6ac8babb9b3794421eb9bb65c6b8f79772f40b42953ed7e2233d444dbc67b9a0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
captured_at: '2026-07-18T04:27:20.159062Z'
source_capture_sha256: sha256:86ebcb8b54830af4a9f62d358d9b075491553ca58e04866025ff4ae06884f370
source_capture_chars_original: 1183
source_publication_excerpt_chars: 1183
observation_id: obs_8b734e871746d44739961ca5c87dec8609fa62a7775e1cdafb4c451515995dfb
revision_id: rev_72c848690bf27ff6272dda8804253ba128962b1ff518aaa19da64ebb67bbc80d
event_id: evt_6a51d86f3c6943879b4c5f5ca24929070b17de31dcf5f03358c6af7275e00501
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.05485v1](<https://arxiv.org/abs/2603.05485v1>)
- **作者**: Benjamin Feuer, Lucas Rosenblatt, Oussama Elachqar
- **分类**: cs.AI
- **论文时间**: 2026-03-05T18:52:28Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.05485v1.pdf](<https://arxiv.org/pdf/2603.05485v1.pdf>)

## 来源摘要/节选

> As AI models progress beyond simple chatbots into more complex workflows, we draw ever closer to the event horizon beyond which AI systems will be utilized in autonomous, self-maintaining feedback loops. Any autonomous AI system will depend on automated, verifiable rewards and feedback; in settings where ground truth is sparse or non-deterministic, one practical source of such rewards is an LLM-as-a-Judge. Although LLM judges continue to improve, the literature has yet to introduce systems capable of enforcing standards with strong guarantees, particularly when bias vectors are unknown or adversarially discovered. To remedy this issue, we propose average bias-boundedness \(A-BB\), an algorithmic framework which formally guarantees reductions of harm/impact as a result of any measurable bias in an LLM judge. Evaluating on Arena-Hard-Auto with four LLM judges, we achieve \(tau=0.5, delta=0.01\) bias-bounded guarantees while retaining 61-99% correlation with original rankings across formatting and schematic bias settings, with most judge-bias combinations exceeding 80%. The code to reproduce our findings is available at https://github.com/penfever/bias-bounded-evaluation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
