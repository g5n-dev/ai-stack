---
title: "AgentRoboCritic: Understanding the Capability of Frontier Agents on Direct Robot Control"
date: 2026-11-22T07:15:21+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:bced8495dab7f3e125238dce97db46684266e8d9bf5ec764677ec5ff59b2a43d"
source_payload_sha256: "sha256:0a5f5aa9a37f193632f0be434c192b566c3da24f43ddfd61f0f776f8801f9ec9"
observation_id: obs_107bf7631dd21fedffe20e388530bc64f2e5e240fd9b264bb87fefdd9dd571ad
event_id: evt_a0b2991be2e7686f7e580e786b527cc826ec85df98154994659baa5a14e82d09
revision_id: rev_2d47b8d7a45ee7fbe65e477626391e09f76ea94c7cea107d11a783aef014b878
source_published_at: 2026-11-19T18:57:25Z
first_seen_at: 2026-11-21T23:13:45.656484Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
interpretation_sha256: "sha256:9c95014dd810c20929374be8c64f039e067bd0e7b5a72247ab6cd5ccfaed5492"
description: "AgentRoboCritic 从动作层分析多模态语言智能体直接控制机器人的表现：策略智能体为每个动作说明局部意图，评论器据此判断执行结果与失败原因。研究覆盖 12 个操作基准，并发布 12,844 条动作标注数据及微调后的开源评论器 Muse-Glimmer-30B。"
external_url: http://arxiv.org/abs/2611.26613v1
parent_observation_id: null
last_seen_at: 2026-11-21T23:13:45.656484Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26613v1](http://arxiv.org/abs/2611.26613v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Yiyang Du、Yuxuan Kuang、Qitao Zhao 等

## 要点解读

### 这是什么
AgentRoboCritic 从动作层分析多模态语言智能体直接控制机器人的表现：策略智能体为每个动作说明局部意图，评论器据此判断执行结果与失败原因。研究覆盖 12 个操作基准，并发布 12,844 条动作标注数据及微调后的开源评论器 Muse-Glimmer-30B。

### 用在哪里
它适合用于评估机器人操作智能体的执行能力、定位失败环节，以及研究闭环纠错和零样本泛化表现。低成本动作级评论器也可用于机器人控制系统的开发与评测。

### 可以推断的
- 推测：动作级评论可能比单纯的整段任务成功率更有助于定位具体改进方向。
- 推测：公开标注数据和开源评论器，可能成为机器人智能体评测方法比较的基础资源。

## 来源摘要/节选

> Frontier multimodal language agents such as GPT-6 Astra have demonstrated strong capabilities in controlling robots directly via low-level numerical actions without high-level primitives. However, existing benchmarks report only episode-level success rates, which show neither how these agents succeed nor where they fail. In this paper, we present a systematic action-level analysis of frontier agents on direct robot control across 12 manipulation benchmarks. We introduce AgentRoboCritic, an intent-grounded critique framework in which the policy agent states a local intent alongside each action, and a critic evaluates the action's outcome and failure mode against this intent. Our action-level analysis demonstrates the promising capabilities of frontier agents on direct robot control, including closed-loop recovery from local execution failures, reliable semantic grounding across diverse scenes, and strong zero-shot manipulation without task-specific adaptation. It also identifies their current limitations, including task-relevant physical execution bottlenecks such as grasping and alignment, and uneven recovery across failure modes. Finally, we validate our critic on a 400-action human-annotated benchmark and release a dataset of 12,844 annotated actions alongside a fine-tuned open-source critic, Muse-Glimmer-30B, whose failure-mode accuracy rises from 32.58% to 74.24%, enabling low-cost action-level analysis.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。