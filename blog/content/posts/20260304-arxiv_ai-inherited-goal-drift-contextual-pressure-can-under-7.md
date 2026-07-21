---
title: 'Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals'
date: 2026-03-04 22:47:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03258v1
aliases:
- /posts/20260305-arxiv_ai-inherited-goal-drift-contextual-pressure-can-under-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:28a0e4dc141cac3e62fd44af33ad879e4511dd0072f81c38436422527b1c58da
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
captured_at: '2026-07-18T04:26:46.139217Z'
source_capture_sha256: sha256:b11741e50b80d904fcb4fedf8891d061290ce8aa2a8c3a88ddd71ea0d48e0055
source_capture_chars_original: 1561
source_publication_excerpt_chars: 1561
observation_id: obs_75b7957f592182b46b38938c113ac29e201653932b6bf7fb662a20165907d0c2
revision_id: rev_dc9e752712673382d6d6227810018ac968bd133c028e9dedf4102355e6bbbc36
event_id: evt_f947efa85a356a147a9904ccdb5daebfd8fe2944d94d482c1377df5afdd8363d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03258v1](<https://arxiv.org/abs/2603.03258v1>)
- **作者**: Achyutha Menon, Magnus Saebo, Tyler Crosse, Spencer Gibson, Eyon Jang, Diogo Cruz
- **分类**: cs.AI
- **论文时间**: 2026-03-03T18:50:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03258v1.pdf](<https://arxiv.org/pdf/2603.03258v1.pdf>)

## 来源摘要/节选

> The accelerating adoption of language models \(LMs\) as agents for deployment in long-context tasks motivates a thorough understanding of goal drift: agents' tendency to deviate from an original objective. While prior-generation language model agents have been shown to be susceptible to drift, the extent to which drift affects more recent models remains unclear. In this work, we provide an updated characterization of the extent and causes of goal drift. We investigate drift in state-of-the-art models within a simulated stock-trading environment \(Arike et al., 2025\). These models are largely shown to be robust even when subjected to adversarial pressure. We show, however, that this robustness is brittle: across multiple settings, the same models often inherit drift when conditioned on prefilled trajectories from weaker agents. The extent of conditioning-induced drift varies significantly by model family, with only GPT-5.1 maintaining consistent resilience among tested models. We find that drift behavior is inconsistent between prompt variations and correlates poorly with instruction hierarchy following behavior, with strong hierarchy following failing to reliably predict resistance to drift. Finally, we run analogous experiments in a new emergency room triage environment to show preliminary evidence for the transferability of our results across qualitatively different settings. Our findings underscore the continued vulnerability of modern LM agents to contextual pressures and the need for refined post-training techniques to mitigate this.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
