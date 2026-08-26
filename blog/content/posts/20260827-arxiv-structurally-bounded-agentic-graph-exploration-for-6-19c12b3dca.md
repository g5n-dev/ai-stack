---
title: "Structurally-bounded Agentic Graph Exploration for Evidence-Grounded Scholarly DeepSearch"
date: 2026-08-27T03:23:03+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:50024f3d286348f3616204f31f2a5b0a01735d61291ff19ad6b347b901ada304"
source_payload_sha256: "sha256:2444137f48322e1c0fb123e4b42970a0b7853a6836baa80226bfeff29006922e"
observation_id: obs_19c12b3dca90a3237b327b7c1c83b61ac606482b2edf552aca795ddbce86dafb
event_id: evt_947488c65bcca42bc041a275555e58bde01bfb4a99216a48c7398307e2b1eafa
revision_id: rev_ad25e10bffd0ea77594ecf703e3e010afeba799f41bd356c13dabc5f86a6b699
source_published_at: 2026-08-25T16:51:26Z
first_seen_at: 2026-08-26T19:19:46.686455Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
interpretation_sha256: "sha256:36dd1d672d56df2bb3d6d6cf9aee5b4dd64a815db32c7e1200b297d1a524405c"
description: "该系统采用一次查询生成种子文献，再沿 1.5 跳引用网络扩展，并对缺乏 entailment 支持的引用边进行剪枝，最后用考虑新近度的随机游走对文献进行排序，从而在搜索前就把候选集合、保留理由和停止条件固定下来。"
external_url: http://arxiv.org/abs/2608.24809v1
parent_observation_id: null
last_seen_at: 2026-08-26T19:19:46.686455Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24809v1](http://arxiv.org/abs/2608.24809v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Rima Hazra、Sayan Layek、Somnath Banerjee 等

## 要点解读

### 这是什么
该系统采用一次查询生成种子文献，再沿 1.5 跳引用网络扩展，并对缺乏 entailment 支持的引用边进行剪枝，最后用考虑新近度的随机游走对文献进行排序，从而在搜索前就把候选集合、保留理由和停止条件固定下来。

### 用在哪里
适用于需要在大规模学术文献集合中进行证据驱动的检索任务，适合希望控制搜索成本并提升结果可追溯性的研究者或平台。

### 可以推断的
推测：该方法通过限制搜索深度和显式剪枝，可显著降低计算资源消耗，适合资源受限的环境。  
推测：基于引用结构的扩展方式能够捕捉相关工作的时间演变，从而在快速变化的学科中提供更及时的文献覆盖。

## 来源摘要/节选

> We present Crase, a bounded and inspectable alternative to deep research agents for scholarly search. Instead of an open-ended search loop, Crase queries a search engine once for seed papers, expands them along their 1.5-hop citation neighborhood, prunes citation edges whose claims lack entailment support, and ranks the remaining papers with a recency-aware random walk. This makes the candidate set, the reason each paper is kept, and the stopping condition explicit and fixed before inference. On LitSearch and one further benchmarks over a 500K-paper arXiv corpus, Crase outperforms deep research agents built on proprietary models by up to 3$\times$ recall@50 at roughly a third of the cost.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。