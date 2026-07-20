---
title: 'Learning from Trials and Errors: Reflective Test-Time Planning for Embodied
  LLMs'
date: 2026-02-25 23:30:40+08:00
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
external_url: https://arxiv.org/abs/2602.21198v1
aliases:
- /posts/20260226-arxiv_ai-learning-from-trials-and-errors-reflective-test-ti-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2d397bc159d485fa9e221971673ceeca7a883e0abec70f41a6bd522761767ca8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:16:49.996029Z'
source_capture_sha256: sha256:eef2d23df95adbbd9f0144d7a79f7c728a249568639411fc799291ba5a2a3078
source_capture_chars_original: 1240
source_publication_excerpt_chars: 1240
observation_id: obs_f2a873723a2eaf30547834b8d19895cb5002a8b18f1c0dbf197c10aa44331492
revision_id: rev_bd8378ceb0e4d1d019f684b300dc908b1d6bf145c0343a11dd21bdf86c374902
event_id: evt_84e9e056e1f64b35539039172c0568019ffb33f5172d558f9b7b4626e1085a4e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21198v1](<https://arxiv.org/abs/2602.21198v1>)
- **作者**: Yining Hong, Huang Huang, Manling Li, Li Fei-Fei, Jiajun Wu, Yejin Choi
- **分类**: cs.LG
- **论文时间**: 2026-02-24T18:55:18Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21198v1.pdf](<https://arxiv.org/pdf/2602.21198v1.pdf>)

## 来源摘要/节选

> Embodied LLMs endow robots with high-level task reasoning, but they cannot reflect on what went wrong or why, turning deployment into a sequence of independent trials where mistakes repeat rather than accumulate into experience. Drawing upon human reflective practitioners, we introduce Reflective Test-Time Planning, which integrates two modes of reflection: \\textit\{reflection-in-action\}, where the agent uses test-time scaling to generate and score multiple candidate actions using internal reflections before execution; and \\textit\{reflection-on-action\}, which uses test-time training to update both its internal reflection model and its action policy based on external reflections after execution. We also include retrospective reflection, allowing the agent to re-evaluate earlier decisions and perform model updates with hindsight for proper long-horizon credit assignment. Experiments on our newly-designed Long-Horizon Household benchmark and MuJoCo Cupboard Fitting benchmark show significant gains over baseline models, with ablative studies validating the complementary roles of reflection-in-action and reflection-on-action. Qualitative analyses, including real-robot trials, highlight behavioral correction through reflection.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
