---
title: "Designer-RSI: Evolving Procedural Memory from User Traffic for Agentic Graphic Design"
date: 2026-09-21T13:02:12+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:246a9bbcf563cdfa5b14aafa3aaf0619e0e0fa21b660e0da43bd7250d6b13fd8"
source_payload_sha256: "sha256:49b121ddaa3451862dba9113c9d4741aea9d20124f12fb40d1d412ce2dba0669"
observation_id: obs_720616ae89f96ce67b822b258696e841f479b58b3d41928381393f7cd297e00c
event_id: evt_e3e858f008344d3535100948dc29c6bb8dcc01ecbfed9332bbe05e8333bc890a
revision_id: rev_28e9f3d6f19bb294ee825f324ff44cab5c5795c15253b4e23448a230f7ba04b0
source_published_at: 2026-09-18T17:59:56Z
first_seen_at: 2026-09-21T05:00:06.391901Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
interpretation_sha256: "sha256:e8ce0b3123f4538297911bba87b13f8960779e690c2dc8d3433a54dab60da56a"
description: "该内容介绍一种持续适应框架，冻结的前沿模型通过大量工具操作专业设计软件，同时外部程序记忆以自然语言形态积累并细化可复用的设计流程。框架通过获取新子任务的流程并基于成功与失败执行结果修订已有流程，配合匹配的 replay 门只保留修复失败且不回归成功的改动。"
external_url: http://arxiv.org/abs/2609.22086v1
parent_observation_id: null
last_seen_at: 2026-09-21T05:00:06.391901Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.22086v1](http://arxiv.org/abs/2609.22086v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Hongyang Du、Lan Yan、Christian Flores 等

## 要点解读

### 这是什么
该内容介绍一种持续适应框架，冻结的前沿模型通过大量工具操作专业设计软件，同时外部程序记忆以自然语言形态积累并细化可复用的设计流程。框架通过获取新子任务的流程并基于成功与失败执行结果修订已有流程，配合匹配的 replay 门只保留修复失败且不回归成功的改动。

### 用在哪里
适用于需要自动化完成长期、互相依赖的专业图形设计任务的系统，或在缺乏可靠程序化评估指标的设计场景中为代理提供经验驱动的流程库。对关注代理持续学习和稳定性提升的研发团队有帮助。

### 可以推断的
推测：在用户需求多样且不断演进的场景中，基于外部记忆的增量更新方式可能比持续微调模型更具成本效益。  
推测：Replay 门的过滤机制有望在设计迭代过程中降低灾难性回归的风险。

## 来源摘要/节选

> Professional graphic design is a long-horizon agentic task in which structured, editable artifacts emerge from many interdependent actions, yet outcomes admit no reliable programmatic oracle. We introduce a continual adaptation framework in which a frozen frontier model operates professional design software through more than 230 tools, while an external procedural memory of natural-language skills accumulates and refines reusable design procedures from experience. The memory widens by acquiring procedures for recurring uncovered subtasks and deepens by revising existing procedures against their own successful and failed executions, while a matched replay gate admits only changes that repair failures without regressing observed successes. Five rounds over 1,406 real user briefs and 1,869 automatically graded trajectories, with no weight updates and no human labels, grow the bank from 76 documentation-derived skills to 139 and raise GenEval2 execution success on Claude-Sonnet-4 from 72.7% to 99.3% (+11.99 points in generation quality), with 61.8% and 67.6% win rates against the no-skill agent across four specialized design benchmarks on Claude-Sonnet-4 and Claude-Opus-4.6. We further show the two mechanisms are effective in combination: on 200 held-out briefs from user-traffic benchmark, widening or deepening alone reaches a 49.4% / 48.6% win rate over the no-skill agent, while their combination reaches 58.5% (p = 0.025). Procedural memory offers a practical route to continual adaptation of agents under noisy, unverifiable feedback.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。