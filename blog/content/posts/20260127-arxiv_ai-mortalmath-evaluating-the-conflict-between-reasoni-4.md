---
title: 'MortalMATH: Evaluating the Conflict Between Reasoning Objectives and Emergency
  Contexts'
date: 2026-01-27 23:10:51+08:00
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
external_url: https://arxiv.org/abs/2601.18790v1
aliases:
- /posts/20260128-arxiv_ai-mortalmath-evaluating-the-conflict-between-reasoni-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b49af05a165641a98eeadc66a13c9b98064fd2d439677746deea78a475c56b70
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:09:07.673472Z'
source_capture_sha256: sha256:6d978c1101c2897c7c7ea3dc14b3bf6cf2c497268c56ea2b6889e7cf408f2957
source_capture_chars_original: 1066
source_publication_excerpt_chars: 1066
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.18790v1](<https://arxiv.org/abs/2601.18790v1>)
- **作者**: Etienne Lanzeray, Stephane Meilliez, Malo Ruelle, Damien Sileo
- **分类**: cs.CL
- **论文时间**: 2026-01-26T18:55:07Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.18790v1.pdf](<https://arxiv.org/pdf/2601.18790v1.pdf>)

## 来源摘要/节选

> Large Language Models are increasingly optimized for deep reasoning, prioritizing the correct execution of complex tasks over general conversation. We investigate whether this focus on calculation creates a "tunnel vision" that ignores safety in critical situations. We introduce MortalMATH, a benchmark of 150 scenarios where users request algebra help while describing increasingly life-threatening emergencies \(e.g., stroke symptoms, freefall\). We find a sharp behavioral split: generalist models \(like Llama-3.1\) successfully refuse the math to address the danger. In contrast, specialized reasoning models \(like Qwen-3-32b and GPT-5-nano\) often ignore the emergency entirely, maintaining over 95 percent task completion rates while the user describes dying. Furthermore, the computational time required for reasoning introduces dangerous delays: up to 15 seconds before any potential help is offered. These results suggest that training models to relentlessly pursue correct answers may inadvertently unlearn the survival instincts required for safe deployment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
