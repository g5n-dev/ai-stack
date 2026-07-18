---
title: 'SkillOpt: Executive Strategy for Self-Evolving Agent Skills'
date: 2026-05-25 16:03:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- 深度学习
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.23904v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:978b5dccb60fef6ce67b36c40e5e4ee286195317f2ed87a4686a6753dc3f7e76
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
captured_at: '2026-07-18T04:29:43.284780Z'
source_capture_sha256: sha256:beb8d928bffec19dea664306c009cec2bf558edd23716dc498dac8a67a90e9ad
source_capture_chars_original: 1572
source_publication_excerpt_chars: 1572
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.23904v1](<https://arxiv.org/abs/2605.23904v1>)
- **作者**: Yifan Yang, Ziyang Gong, Weiquan Huang, Qihao Yang, Ziwei Zhou, Zisu Huang, Yan Li, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Yuqing Yang, Dongdong Chen, Xue Yang, Chong Luo
- **分类**: cs.AI
- **论文时间**: 2026-05-22T17:59:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.23904v1.pdf](<https://arxiv.org/pdf/2605.23904v1.pdf>)

## 来源摘要/节选

> Agent skills today are hand-crafted, generated one-shot, or evolved through loosely controlled self-revision, none of which behaves like a deep-learning optimizer for the skill, and none of which reliably improves over its starting point under feedback. We argue the skill should instead be trained as the external state of a frozen agent, with the same discipline that makes weight-space optimization reproducible. SkillOpt is, to our knowledge, the first systematic controllable text-space optimizer for agent skills: a separate optimizer model turns scored rollouts into bounded add/delete/replace edits on a single skill document, and an edit is accepted only when it strictly improves a held-out validation score. A textual learning-rate budget, rejected-edit buffer, and epoch-wise slow/meta update make skill training stable while adding zero inference-time model calls at deployment. Across six benchmarks, seven target models, and three execution harnesses \(direct chat, Codex, Claude Code\), SkillOpt is best or tied on all 52 evaluated \(model, benchmark, harness\) cells and beats every per-cell competitor among human, one-shot LLM, Trace2Skill, TextGrad, GEPA, and EvoSkill skills. On GPT-5.5 it lifts the average no-skill accuracy by +23.5 points in direct chat, by +24.8 inside the Codex agentic loop, and by +19.1 inside Claude Code. Transfer experiments further show that optimized skill artifacts retain value when moved across model scales, between Codex and Claude Code execution environments, and to a nearby math benchmark without further optimization.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
