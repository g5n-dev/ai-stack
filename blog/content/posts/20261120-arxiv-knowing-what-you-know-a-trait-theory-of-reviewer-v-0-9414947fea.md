---
title: "Knowing What You Know: A Trait Theory of Reviewer Value in Human-AI Cognitive Systems"
date: 2026-11-20T05:31:59+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:fde38d6af03976326ba0cda0caaccf6928e4a6da2c294f6826b0a79c7a980041"
source_payload_sha256: "sha256:0446486c93f45b696f7e0fef16850aeab4bd7278a1ca99d2b7da4ad17f2ce48f"
observation_id: obs_9414947fea04778a1da2a02a7792e341671207fa6e9840f40c066c3ff9a02268
event_id: evt_c494d2f950725add78e5ac9d0efcf0bf1fc10ec6af034b14b90c908013ec93bb
revision_id: rev_e21399b53327eb32b752d77ec2b58ee3f79a7b8e3b47839d910545305c4851d8
source_published_at: 2026-11-18T18:55:07Z
first_seen_at: 2026-11-19T21:30:49.876536Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
interpretation_sha256: "sha256:32ed643321695f9b861a8892d669d1c7048241b54520e73dfa1c501982d816a3"
description: "这篇论文提出“评审者价值”理论：人机共同决策时，人类能否持续创造价值，关键在于其信心与判断正确率是否匹配，即元认知校准。论文结合 AI 辅助会计系统六个月的生产数据，对该理论及其边界进行分析。"
external_url: http://arxiv.org/abs/2611.24932v1
parent_observation_id: null
last_seen_at: 2026-11-19T21:30:49.876536Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.24932v1](http://arxiv.org/abs/2611.24932v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Priyanka Sinha、Sugam Pandey

## 要点解读

### 这是什么
这篇论文提出“评审者价值”理论：人机共同决策时，人类能否持续创造价值，关键在于其信心与判断正确率是否匹配，即元认知校准。论文结合 AI 辅助会计系统六个月的生产数据，对该理论及其边界进行分析。

### 用在哪里
它适用于评估人类评审者与模型各自的价值，以及设计人机协作中的分工与复核机制。研究者也可借此分析应将哪些判断交给人或模型，或如何将人工精力集中到真正的错误上。

### 可以推断的
- 推测：评估人机协作效果时，单看活跃度、速度、资历或与模型的一致程度，可能不足以判断谁更可靠。
- 推测：在具体任务上动态选择更校准的一方，可能比固定由人或模型负责更合理。

## 来源摘要/节选

> When a capable model and a human reviewer cooperate on the same decision, which human still adds value? We argue this is a question about a single cognitive trait, metacognitive calibration: the alignment between a reviewer's behavioral confidence and the actual correctness of their judgments. We develop a trait theory of reviewer value to make it precise. The theory makes five claims: value is governed by calibration rather than by activity, speed, agreement, or tenure; calibration leaves observable traces in behavioral telemetry; those traces are non-diagnostic on their own, because the fast, low-revision signature of a calibrated expert is indistinguishable from that of a confident novice until it is gated by outcomes; human calibration and a model's self-knowledge are the same construct, so the joint system should defer to whichever agent is better calibrated on each item; and individual calibration is causally identifiable only above the level of the single judgment. We ground each claim in a six-month production window of an AI-assisted accounting system (541621 reviewer events, 483 reviewers), and find that a purely behavioral expertise profile inverts the ground truth, scoring an overconfident cohort (5.2 percent correction survival) higher than genuine experts (99.2 percent); that reviewer quality is flat across tenure, so the trait is not learned on the job; and that the same calibration logic that separates good from bad reviewers, applied to the model, concentrates 92.5 percent of human effort on genuine errors. We close with the boundary the theory must respect: under majority-vote aggregation, individual causal value is unidentifiable.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。