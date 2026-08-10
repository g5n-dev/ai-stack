---
title: "SkillProx: Self-Evolving Agent Skills via Proximal Textual Gradient Descent"
date: 2026-08-10T18:39:03+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e23fd9c8362c2737334ff4f0985b813c124b4873ede66b183ae602cd327edd53"
source_payload_sha256: "sha256:f2baac66af2e7c9290a78678a159ff759af47fd8ec5654a56938ba1b26ab8ca1"
observation_id: obs_ff08aa5a73b95fa0bedef8b8555bd305c3690a99a5fe81391c53085209417dbc
event_id: evt_8f977553ab5554ab6ffffa54ce6d9dd4a9d5c95ec69ab59d566c55a048fd698c
revision_id: rev_599f76cfdb9094f77c19367809f5f652b700a438ae1ffe8add958219f2b4c02b
source_published_at: 2026-08-07T17:40:33Z
first_seen_at: 2026-08-10T10:48:27Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.07449v1
parent_observation_id: null
last_seen_at: 2026-08-10T10:36:15.135141Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07449v1](http://arxiv.org/abs/2608.07449v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Mingxuan Zheng、Yujin Zhou、Chuxue Cao 等

## 来源摘要/节选

> LLM agents increasingly adapt to recurring tasks by accumulating procedural knowledge in skills. These skills are lightweight, reusable textual artifacts that are loaded into the agent's context without weight updates. Recent methods refine skills through iterative task execution, failure diagnosis, and trajectory-guided text-space updates. However, existing frameworks lack explicit diagnosis--outcome feedback and treat deletion as a generic edit operation rather than a dedicated mechanism for consolidating accumulated knowledge. We introduce SkillProx, a proximal-gradient-inspired forward--backward framework that couples closed-loop diagnostic evolution with utility-aware proximal refinement. Motivated by a composite objective balancing task loss and skill complexity, the forward stage re-executes diagnosis-driven edits on the same task batch, rolls back regressions, and feeds measured outcomes into subsequent diagnoses. The backward stage decomposes the resulting skill into auditable knowledge units, estimates their contributions using a frozen leave-one-out utility audit, and applies validation-gated consolidation, demotion, or removal. Experiments on in-distribution and out-of-distribution benchmarks across multiple backbone LLMs show that SkillProx improves average accuracy by 3.0 percentage points over the strongest gradient-based baseline. Component ablations demonstrate the complementary effects of closed-loop diagnosis and proximal refinement.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。