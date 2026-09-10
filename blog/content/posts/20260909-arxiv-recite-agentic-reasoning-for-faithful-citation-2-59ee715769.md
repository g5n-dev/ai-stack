---
title: "ReCite: Agentic Reasoning for Faithful Citation"
date: 2026-09-09T12:44:34+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f67ea66f0d413858eb93d6b0d4114eebec581886fc5a5e72f99ac16c02d82037"
source_payload_sha256: "sha256:1a5f6ec205988e16267206dbd022a1facd75601a1e565bd8b1d8c5ef6413a134"
observation_id: obs_59ee71576933ba44ca24941f87eefb8623559cc02c933c4478b756248b291a4c
event_id: evt_fefd0e051341b23094773c885101b55cbc711d97948a289e5ab33ebf75e41254
revision_id: rev_c942a2655fe0235249c81953d967a269613c6c31d28b0a01268037489db97d98
source_published_at: 2026-09-08T17:59:50Z
first_seen_at: 2026-09-09T04:55:31Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 47
interpretation_sha256: "sha256:c008037da6e06790cf1a7df08764efd047f4ee10caa856ffc248c91b61eca755"
description: "ReCite 是一种解耦的代理式框架，利用位置感知、意图感知的查询规划以及反思式验证来确保引用在逻辑上支撑论点。它通过合成的推理轨迹检验论点‑证据一致性，并在检索结果不支持时触发自我修正。"
external_url: http://arxiv.org/abs/2609.09156v1
parent_observation_id: null
last_seen_at: 2026-09-10T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.09156v1](http://arxiv.org/abs/2609.09156v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yuyang Huang、Bobo Li、Jiajia Song 等

## 要点解读

### 这是什么
ReCite 是一种解耦的代理式框架，利用位置感知、意图感知的查询规划以及反思式验证来确保引用在逻辑上支撑论点。它通过合成的推理轨迹检验论点‑证据一致性，并在检索结果不支持时触发自我修正。

### 用在哪里
适用于自动化学术写作、文献检索与引用推荐系统，尤其在需要严格检查引用准确性的场景中对研究者和平台有帮助。

### 可以推断的
推测：轻量化实现使框架能够在资源受限的环境中部署。  
推测：与大规模生成模型协同时，自修正循环可能进一步提升引用准确度。

## 来源摘要/节选

> Accurate citations are the foundation of academic writing, tracing intellectual origins and substantiating core claims. However, manually navigating the growing volume of scientific literature is increasingly difficult, prompting reliance on automatic citation recommendation. While modern retrieval-augmented architectures have largely mitigated the fabrication of non-existent papers, current systems relying on semantic similarity struggle with misattribution, often citing authentic papers that fail to logically support the author's claim. To address this challenge, we argue that accurate citation requires a shift from similarity-based search to active, claim-level reasoning. We propose ReCite, a decoupled agentic framework that orchestrates location perception, intent-aware query planning, and reflective verification. Trained on synthesized reasoning trajectories, our agent verifies claim-evidence consistency and triggers self-correction loops when retrieved candidates lack logical support. Experiments demonstrate that our lightweight framework outperforms state-of-the-art massive generative models in strict citation accuracy. By grounding literature matching in verifiable logic rather than semantic overlap, ReCite establishes a reliable foundation for automated academic writing.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。