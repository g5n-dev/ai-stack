---
title: Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning
  and Execution
date: 2026-07-15 11:26:59+08:00
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
external_url: https://arxiv.org/abs/2607.13034v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:88fc0b7ec3eb8e673c09f52d1b7f0857c19fdf8bc30bf944296ce169aa7428f6
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
captured_at: '2026-07-18T04:30:29.635417Z'
source_capture_sha256: sha256:dcad273ee29ee08a8f21a1dad1afd4fcc637140efbb0917987712c972c4cd05b
source_capture_chars_original: 1844
source_publication_excerpt_chars: 1844
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.13034v1](<https://arxiv.org/abs/2607.13034v1>)
- **作者**: Junjie Yin, Xinyu Feng
- **分类**: cs.AI
- **论文时间**: 2026-07-14T17:59:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.13034v1.pdf](<https://arxiv.org/pdf/2607.13034v1.pdf>)

## 来源摘要/节选

> Large language model \(LLM\) agents increasingly automate multi-step engineering and informatics workflows, yet they rarely ask how much effort a task actually requires. They often follow a maximum-context-first strategy--re-reading files and dependencies they have already seen--turning a one-line edit into a small code-base audit. We argue the missing capability is task-aware execution-scope estimation: judging a task's difficulty, the information it truly needs, and the shortest reliable path before committing budget. We formalize minimum-sufficient execution and the Agent Cognitive Redundancy Ratio \(ACRR\), and propose E3 \(Estimate, Execute, Expand\): the agent estimates an initial operating point, executes a minimum viable path, and expands scope only when verification fails. On MSE-Bench--a deterministic benchmark of 121 edits in a capability-controlled simulator--E3 matches the strongest baseline's 100% success while cutting cost by 85%, tokens by 91%, and inspected files by 92%, and further beats a strong adaptive retrieval baseline by 16%; the gains survive held-out instruction wording and essentially every cost weighting. A companion real-model harness \(LLM-Case\) corroborates the effect on a live gpt-4o agent editing a real open-source library, with every candidate patch graded by actually running the project's real pytest suite against a measured oracle: the over-reading is milder but real, and E3 is the leanest and fastest policy at comparable task success--its one shortfall a provider rate-limit, not a wrong edit. We frame this as a controlled probe of execution redundancy, not a measurement of any deployed agent, and position task-aware execution as a step toward engineering-grounded AI \(EGAI\)--agents whose effort is anchored in the engineering reality of the task. We release the framework and benchmark.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
