---
title: Do LLMs Benefit From Their Own Words?
date: 2026-03-02 23:25:37+08:00
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
external_url: https://arxiv.org/abs/2602.24287v1
aliases:
- /posts/20260303-arxiv_ai-do-llms-benefit-from-their-own-words-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a76ccf592b99810c7105059cb1345a0deee53b9d93ed277d5360ba0985e1a055
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:26:12.126510Z'
source_capture_sha256: sha256:e674c400d0cc689c8bf030bf7d6ba7b6aab88fadfb112e85d8750fed6099114d
source_capture_chars_original: 1520
source_publication_excerpt_chars: 1520
observation_id: obs_e6bd89ed054c4b4591cad85b9a8481a91c8b968d64d7ffbd432ef682a26dfaa9
revision_id: rev_f7c5c1c0ac3972f4eea6f2659173eb616fa77bf84fab76a61d125f67976fe1d9
event_id: evt_16200897124a1eb8ef773f4eaff87cd33558e0d59c122544546008092493e453
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24287v1](<https://arxiv.org/abs/2602.24287v1>)
- **作者**: Jenny Y. Huang, Leshem Choshen, Ramon Astudillo, Tamara Broderick, Jacob Andreas
- **分类**: cs.CL
- **论文时间**: 2026-02-27T18:58:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24287v1.pdf](<https://arxiv.org/pdf/2602.24287v1.pdf>)

## 来源摘要/节选

> Multi-turn interactions with large language models typically retain the assistant's own past responses in the conversation history. In this work, we revisit this design choice by asking whether large language models benefit from conditioning on their own prior responses. Using in-the-wild, multi-turn conversations, we compare standard \(full-context\) prompting with a user-turn-only prompting approach that omits all previous assistant responses, across three open reasoning models and one state-of-the-art model. To our surprise, we find that removing prior assistant responses does not affect response quality on a large fraction of turns. Omitting assistant-side history can reduce cumulative context lengths by up to 10x. To explain this result, we find that multi-turn conversations consist of a substantial proportion \(36.4%\) of self-contained prompts, and that many follow-up prompts provide sufficient instruction to be answered using only the current user turn and prior user turns. When analyzing cases where user-turn-only prompting substantially outperforms full context, we identify instances of context pollution, in which models over-condition on their previous responses, introducing errors, hallucinations, or stylistic artifacts that propagate across turns. Motivated by these findings, we design a context-filtering approach that selectively omits assistant-side context. Our findings suggest that selectively omitting assistant history can improve response quality while reducing memory consumption.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
