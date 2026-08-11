---
title: "ArchAgent v2: A Case Study with the Data Prefetching Championship"
date: 2026-08-12T05:07:10+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9b9ce869524852a9c5737f713ce9f84044fb5be1e943ca10fcb6d453a011d6c2"
source_payload_sha256: "sha256:09780cbdf9bf2991fbb9f170641775f88bb3fdd57c33e92cc58a36ba78f4bb0e"
observation_id: obs_9f170982707acaf9c8957b5ae9733f5129cb0bf30c96218be5ae5df48aa4caa3
event_id: evt_7318699391a835ef13be34a813aa29a936cbabb2890d6b7e37e1ac79923ee4c4
revision_id: rev_85e4a5c40fc7750ef6bf390609f7840e849553f3fc52ed8a622b36e02f6536a3
source_published_at: 2026-08-10T17:28:05Z
first_seen_at: 2026-08-11T21:03:41.055607Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:5e7831bc0b8d1ed15be3c81244d8f704804adc732ea8404b325cd56284497911"
description: "ArchAgent v2 是面向多层次数据预取的自动化微架构搜索框架。它采用分层演化搜索和硬件可实现性反馈，将搜索能力从单层扩展到三级预取，并在同等比赛规则下生成的策略优于手工设计的最优方案。"
external_url: http://arxiv.org/abs/2608.09874v1
parent_observation_id: null
last_seen_at: 2026-08-11T21:03:41.055607Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09874v1](http://arxiv.org/abs/2608.09874v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Abraham Gonzalez、Raghav Gupta、Akanksha Jain 等

## 要点解读

### 这是什么
ArchAgent v2 是面向多层次数据预取的自动化微架构搜索框架。它采用分层演化搜索和硬件可实现性反馈，将搜索能力从单层扩展到三级预取，并在同等比赛规则下生成的策略优于手工设计的最优方案。

### 用在哪里
适合计算机架构研究者用于探索缓存层级和预取算法，也适用于需要在真实硬件约束下快速生成高效预取逻辑的开发者。

### 可以推断的
推测：分层冻结部分搜索空间的方式可能显著提升搜索效率。  
推测：仿真耗时仍是制约因素，在仿真资源有限时搜索速度会受到限制。

## 来源摘要/节选

> Agentic artificial intelligence has shown great promise in automating algorithm design, but scaling similar techniques to computer microarchitecture discovery remains challenging due to vast search spaces, strict hardware budgets, and long simulation times. In this work, we present ArchAgent v2, a framework which scales automated microarchitecture search to multi-level data prefetching. While the original ArchAgent successfully discovered single-level cache replacement policies in competition settings, it does not scale to multi-level prefetching where the design space and degrees of freedom are larger. To overcome this, we introduce two new additions to ArchAgent: a cascaded evolutionary search that subdivides the design space by sequentially evolving and freezing prefetchers at individual cache levels, and a hardware-realizability feedback loop that embeds real-time size-estimation directly into the evolution process.
> Evaluated under identical rules of the 4th Data Prefetching Championship (DPC4), ArchAgent v2 automatically designs a three-level prefetcher that outperforms the winning hand-designed solution, further demonstrating automated agentic discovery as a useful tool for computer architects. Our discovered policy achieves a 3.8\% geometric mean IPC speedup over the baseline overall and a 0.3\% improvement over the prior champion, BertiGO. On low-bandwidth single-core configurations, our policy yields a 4.6\% performance speedup compared to only 2.6\% for BertiGO. However, multi-core evolution still remains a significant challenge due to simulation latency impeding evolution speed. Finally, our profiling of an ArchAgent evolution of over 12,000 candidate designs provides key insights into how automated evolutionary agents explore and synthesize complex microarchitectural logic.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。