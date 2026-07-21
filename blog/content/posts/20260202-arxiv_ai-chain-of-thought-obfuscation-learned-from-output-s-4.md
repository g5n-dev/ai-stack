---
title: Chain-of-thought obfuscation learned from output supervision can generalise
  to unseen tasks
date: 2026-02-02 02:57:13+08:00
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
external_url: https://arxiv.org/abs/2601.23086v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ab1834a5cb3437799136da8368028d39612877a15fa872046db6a1adab0af0ce
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
captured_at: '2026-07-18T04:10:04.354932Z'
source_capture_sha256: sha256:0c6d7b9ce7b71ff02394ed007aa23f0f062736e84c5dc5b7d6f07900f8273cbe
source_capture_chars_original: 1130
source_publication_excerpt_chars: 1130
observation_id: obs_7709ea5da688fbd40849e8f7aa00d4e2bf6638e02fbdcf91282a73c2c326958f
revision_id: rev_47f6d4a889a7f9b38a0e5146bde6e41a0de91720d4825deda053b02a581187b8
event_id: evt_b58c80a631445fb8465fd8803c344f6dc2620f6c5dae02091606c9cf75b76091
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23086v1](<https://arxiv.org/abs/2601.23086v1>)
- **作者**: Nathaniel Mitrani Hadida, Sassan Bhanji, Cameron Tice, Puria Radmard
- **分类**: cs.AI
- **论文时间**: 2026-01-30T15:34:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23086v1.pdf](<https://arxiv.org/pdf/2601.23086v1.pdf>)

## 来源摘要/节选

> Chain-of-thought \(CoT\) reasoning provides a significant performance uplift to LLMs by enabling planning, exploration, and deliberation of their actions. CoT is also a powerful tool for monitoring the behaviours of these agents: when faithful, they offer interpretations of the model's decision making process, and an early warning sign for dangerous behaviours. However, optimisation pressures placed on the CoT may cause the model to obfuscate reasoning traces, losing this beneficial property. We show that obfuscation can generalise across tasks; models that learn to obfuscate reasoning involving reward hacking \(e.g. accessing and utilising leaked information\) generalise both the reward hacking behaviour and its obfuscation in CoT to unseen reward hacking settings. Most worryingly, we show that obfuscation of CoT reasoning, and its generalisation across tasks, also follows when we penalise only the model's final actions after closing its CoT. Our findings suggest that current practices of penalising harmful generations may inadvertently lead to a reduction in the broader monitorability of LLMs in unpredictable ways.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
