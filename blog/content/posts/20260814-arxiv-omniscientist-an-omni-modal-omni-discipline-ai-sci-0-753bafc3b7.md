---
title: "OmniScientist: An Omni-Modal Omni-Discipline AI Scientist"
date: 2026-08-14T13:04:03+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0719a5354a3ec48bbff348b1a8300768d7876c43950236b6d41be1337f249cb8"
source_payload_sha256: "sha256:7a2caaaab5e3129291739df08db32168716cd129b5480d432945f25dfcd4dc4b"
observation_id: obs_753bafc3b7c8c6251088583ebe14c97b14bdb8c193982514711a20ac663abb25
event_id: evt_e868b3418709031f80d30fe3b2b09f808ff45ca802d27af23bf6622fe6bd2382
revision_id: rev_a6c5fadb69cc8c3a84b55416c8eb95dda1072b6edb565530d3501560244257ec
source_published_at: 2026-08-13T17:59:52Z
first_seen_at: 2026-08-14T05:13:34Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:9499400e4aae81ad612922ee60201e3fd79f3ef989f273c4a3692cc7aa7a4e27"
description: "OmniScientist是一种端到端的多模态AI科学家系统，能够直接利用图像、音频、视频、3‑D结构等多种原始证据开展跨学科研究，并通过感知层与三个自主代理在确定性流水线中完成创意生成、实验执行和文稿撰写，同时在代码层面实现创新性筛选、统计有效性检查和数值追溯。"
external_url: http://arxiv.org/abs/2608.13558v1
parent_observation_id: null
last_seen_at: 2026-08-14T05:02:01.039695Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.13558v1](http://arxiv.org/abs/2608.13558v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Bobo Li、Hao Fei、Tianjie Ju 等

## 要点解读

### 这是什么
OmniScientist是一种端到端的多模态AI科学家系统，能够直接利用图像、音频、视频、3‑D结构等多种原始证据开展跨学科研究，并通过感知层与三个自主代理在确定性流水线中完成创意生成、实验执行和文稿撰写，同时在代码层面实现创新性筛选、统计有效性检查和数值追溯。

### 用在哪里
适合需要从异构数据全链路自动化科研流程的团队，或希望提升AI在科学发现中对原始证据感知能力的研究者。

### 可以推断的
推测：在缺乏预计算特征的盲测情况下，仅使用标量特征会导致评估指标下降，说明直接感知对提升系统表现至关重要。  
推测：虽然系统已在多个真实案例中完成从原始数据到论文的全流程，但其实际性能仍受数据质量和领域差异的影响。

## 来源摘要/节选

> Recent advances in foundation models have enabled AI scientists to automate increasingly complete research workflows, from hypothesis generation and code execution to manuscript preparation. Yet workflow coverage alone does not provide access to the full evidence on which scientific discovery depends. Existing systems typically reason over text, code, labels, or precomputed summaries, leaving scientifically decisive spatial, temporal, cross-channel, and procedural relations unavailable to the agent. We introduce OmniScientist, an end-to-end, omni-modal AI scientist that conducts multidisciplinary research directly from heterogeneous raw evidence. A perception layer and 3 autonomous agents for ideation, experiment, and writeup operate within a deterministic pipeline, allowing observations to shape research questions, experimental decisions, and final claims throughout the research lifecycle. By running idea, rigour, and claim checks in code, the system enforces novelty screening, statistical validity, execution provenance, and numerical traceability. We evaluate OmniScientist on 36 real-data cases spanning 5 discipline families, 4 families of scientific evidence, and modalities including images, signals, audio, video, 3-D structures, trajectories, tables, formulae, and graphs. The system completes the full path from raw data to a compiled manuscript in all 36 cases and achieves a mean overall paper score of 6.3 with the reference reasoning backbone. In paired comparisons against a blind variant that receives only precomputed scalar features, direct perception improves all 7 evaluation dimensions and wins 85% of head-to-head judgments. These results show that lifecycle-wide perception is essential for evidence-grounded scientific discovery and provides a practical path toward broadly capable AI scientists.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。