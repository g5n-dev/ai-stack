---
title: "The Low Frequency Trap: Video Language Models Fail at Simple Event Bookkeeping"
date: 2026-08-07T19:09:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ac9fc4fee1dd5447e909272174d9eb82f75d02e14b77a014ca649cdb1ae1f47d"
source_payload_sha256: "sha256:2aeba64f8dd4d0f864263bfab05650d189b4c7a74284f4335bf28166b176c953"
observation_id: obs_a8836da2d99c26e1c1df55c76953cc37b83027443d9cc5005a8b4fc42b8ac1b2
event_id: evt_6cb4105b7092de965a1908799a56efbca6d16c0f26f2e00784110779a350332e
revision_id: rev_5b8e61218bd3ef87e048172e766690cb19a73748bb78032e8048a5f7d5411921
source_published_at: 2026-08-06T17:57:06Z
first_seen_at: 2026-08-07T11:06:58.381433Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
interpretation_sha256: "sha256:d19dc314fe64ad756cf36e4d9c6e4da0f13076e5379c370910e84263315a5b1d"
description: "这是一篇关于视频语言模型在计数、频率和状态转换等简单事件上表现的评估研究，提出基于可执行事件轨迹的分析方法，揭示模型在时序信息处理上的阶段性失效。"
external_url: http://arxiv.org/abs/2608.06361v1
parent_observation_id: null
last_seen_at: 2026-08-07T11:06:58.381433Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06361v1](http://arxiv.org/abs/2608.06361v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Sarvesh Baskar、Zikui Cai、Shayan Shabihi 等

## 要点解读

### 这是什么
这是一篇关于视频语言模型在计数、频率和状态转换等简单事件上表现的评估研究，提出基于可执行事件轨迹的分析方法，揭示模型在时序信息处理上的阶段性失效。

### 用在哪里
适用于视频模型评测框架的设计者和对时序推理能力有需求的开发者，尤其在需要区分事件持久性与瞬时性的任务中。

### 可以推断的
推测：在此类基准上，模型对瞬时事件的感知往往比持续状态更受限。  
推测：提升采样率可能提升计数精度，但并不等价于事件序列的真实恢复。

## 来源摘要/节选

> Real-world video benchmarks provide broad coverage, but their fixed clips entangle event count, rate, duration, and visual complexity, making failure modes hard to isolate. While existing programmatic benchmarks offer better control, they score only the final answer rather than auditing reported events against executable ground truth. To bridge this gap, we introduce trace-grounded parametric profiling for event counting in three controlled video tasks: bouncing-ball wall contacts, visual blinks, and categorical state transitions. Across 2,190 videos, we vary event count N and frequency F while holding rendering fixed. Each video includes an executable event trace for capability-surface estimation and timestamp-level evaluation. Our results reveal a staged temporal failure. At an 80% reliability threshold, Gemini 3.6 Flash reliably counts persistent state transitions up to 12 events at 0.5 and 1.0 Hz, yet demonstrates no reliable positive-count region for transient blinking events. Thus, event representation dictates whether a model initially accesses evidence -- a limitation that compounds as count and frequency increase. In the high-count, high-frequency regime, only 0.2% of final counts are correct and the model recovers just 18.1% of true events. To test if visual access is the primary bottleneck, we increase sampling rate. Although this boosts Bounce Ball accuracy from 19.6% to 29.3%, the reported sequence agrees with ground truth only 3.7% of the time. Extra frames can therefore inflate final scores without producing faithful event recovery. Different prompting strategies yield similarly limited gains, and real-world video evaluations show the same concentration of success at low event counts. Ultimately, trace-grounded profiling shifts video evaluation from aggregate accuracy metrics to a detailed diagnostic of where temporal reasoning fails.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。