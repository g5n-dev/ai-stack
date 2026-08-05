---
title: "SocietyBench: Forecasting Counterfactual Social-World Evolution"
date: 2026-08-05T14:44:05+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f3566ff1893bdb6573151624f545d2cc84bc5cc35e32a38e099ca7bfc54e275f"
source_payload_sha256: "sha256:5c1a78839a140fc0ea74eb1459fd94ad99460836dca89b945ba818ecd30e6651"
observation_id: obs_4a45358a628b1ee84b21b70472b0216e6b4b7d3aa2ebcea02191c27197403f3f
event_id: evt_93a0e260aeeec7bdf2a3f94a28fa4ceddcd48df628915464ad64b88fe26b5ec4
revision_id: rev_b5cb2dc5018ccfbcc2c669fa4fa2c120ffdf0dcd1232c9f2040c024556b995cd
source_published_at: 2026-08-04T17:59:56Z
first_seen_at: 2026-08-05T06:53:04Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
interpretation_sha256: "sha256:3555737f351b31fcd584835fa1a478fc28241cf43185cef9dbb6f84e00d7ee3d"
description: "该基准把真实社交事件的新闻和社交媒体内容整合成时间线，并将其转化为去标识化的反事实情境，用以评估语言模型在**概率校准**和**时间准确性**两个维度上的预测表现。"
external_url: http://arxiv.org/abs/2608.04009v1
parent_observation_id: null
last_seen_at: 2026-08-05T06:41:35.489568Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.04009v1](http://arxiv.org/abs/2608.04009v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Zhenran Wang、Zhonghan Bian、Jinsong Li 等

## 要点解读

### 这是什么
该基准把真实社交事件的新闻和社交媒体内容整合成时间线，并将其转化为去标识化的反事实情境，用以评估语言模型在**概率校准**和**时间准确性**两个维度上的预测表现。

### 用在哪里
适用于研究团队系统测评大模型对社会事件走向的理解与预测能力，也可帮助平台构建跨平台事件流的评测框架。

### 可以推断的
- 推测：模型在概率校准和时间准确性上可能出现权衡，单一模型难以同时在两方面取得高分。  
- 推测：不同事件上得分波动较大，说明跨事件的泛化仍是模型评估的主要挑战。

## 来源摘要/节选

> Large language models (LLMs), and the agents built on top of them, are now benchmarked heavily on whether they can finish a task -- fix a bug, drive a browser, operate a GUI. A complementary social ability, namely how well a model understands and forecasts the way real social events unfold, has barely been measured. We introduce SocietyBench, an end-to-end benchmark that takes a one-line event topic, collects Web news and social-media posts across five platforms, distills them into a date-indexed timeline that keeps factual events and a public-opinion layer separate, and then turns every cutoff date on that timeline into an audited bank of forecasting questions. Questions are scored on two orthogonal 100-point axes: probability calibration and temporal accuracy. Before any model sees a timeline, a three-phase procedure replaces every named entity and shifts every date by a per-event constant, turning a real arc into a counterfactual social world -- structurally identical to what happened, but stripped of the surface labels a model could match against pre-training memory. On five heterogeneous events and 125 prediction points in Chinese and English editions, the strongest of six frontier LLMs reaches only 75.0 out of 100, against a trivial anchor of 50. The two axes come apart: a model can be calibration-strong but time-weak, or the reverse. Three agent frameworks built on a shared base model fail to improve on that base, and two model-free heuristics trail every LLM. Per-event gaps reach 21.4 points on a single axis, which is our main argument for evaluating on several events rather than one. All anonymized timelines, question banks, ground truth, and scoring code are released.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。