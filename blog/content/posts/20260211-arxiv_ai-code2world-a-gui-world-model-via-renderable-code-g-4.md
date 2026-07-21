---
title: 'Code2World: A GUI World Model via Renderable Code Generation'
date: 2026-02-11 03:18:02+08:00
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
external_url: https://arxiv.org/abs/2602.09856v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:62eb2d188752827b2339886ca3787b9726ebe74f065a102939d4f2beb5c9ae11
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
captured_at: '2026-07-18T04:14:39.893621Z'
source_capture_sha256: sha256:55287e2fe8a5e94671e4aab8e9d4a907ba9b6c83306d9b3f61b74adccd5c5059
source_capture_chars_original: 1438
source_publication_excerpt_chars: 1438
observation_id: obs_3bcbf8fc27eb2b70ce4ec6e7f75fe0c8a526166269a94b87da6771b6b0899fb9
revision_id: rev_724f5d510adb8ef019d8d66b4936b5ee2f1636c4bf2283fb94880839515a1834
event_id: evt_f80087f587d8c5475d45a4ebe046ada0cea02a1eeb8d980090a2f68fcd063fd1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09856v1](<https://arxiv.org/abs/2602.09856v1>)
- **作者**: Yuhao Zheng, Li'an Zhong, Yi Wang, Rui Dai, Kaikui Liu, Xiangxiang Chu, Linyuan Lv, Philip Torr, Kevin Qinghong Lin
- **分类**: cs.CV
- **论文时间**: 2026-02-10T14:56:19Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09856v1.pdf](<https://arxiv.org/pdf/2602.09856v1.pdf>)

## 来源摘要/节选

> Autonomous GUI agents interact with environments by perceiving interfaces and executing actions. As a virtual sandbox, the GUI World model empowers agents with human-like foresight by enabling action-conditioned prediction. However, existing text- and pixel-based approaches struggle to simultaneously achieve high visual fidelity and fine-grained structural controllability. To this end, we propose Code2World, a vision-language coder that simulates the next visual state via renderable code generation. Specifically, to address the data scarcity problem, we construct AndroidCode by translating GUI trajectories into high-fidelity HTML and refining synthesized code through a visual-feedback revision mechanism, yielding a corpus of over 80K high-quality screen-action pairs. To adapt existing VLMs into code prediction, we first perform SFT as a cold start for format layout following, then further apply Render-Aware Reinforcement Learning which uses rendered outcome as the reward signal by enforcing visual semantic fidelity and action consistency. Extensive experiments demonstrate that Code2World-8B achieves the top-performing next UI prediction, rivaling the competitive GPT-5 and Gemini-3-Pro-Image. Notably, Code2World significantly enhances downstream navigation success rates in a flexible manner, boosting Gemini-2.5-Flash by +9.5% on AndroidWorld navigation. The code is available at https://github.com/AMAP-ML/Code2World.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
