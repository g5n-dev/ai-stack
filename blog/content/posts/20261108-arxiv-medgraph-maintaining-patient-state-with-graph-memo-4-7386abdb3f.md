---
title: "MedGraph: Maintaining Patient State with Graph Memory for Long-Term Medical Dialogue"
date: 2026-11-08T10:29:42+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2da54566ec4a137c14f0a7fd23a7e02367f447d19afed4617e76d453655d5a5c"
source_payload_sha256: "sha256:df73465eaba79f1730f109bf412047da990d96e076ec5281282ca1db846cc4ae"
observation_id: obs_7386abdb3f6e339849832071858eb2ebc72326ee114db3431f3e08612b35afc1
event_id: evt_900b4a716d23eeeba1fc1f3ed0745e9bf2849307f36b22634bfd8f18b5762017
revision_id: rev_0fe6942e4ccf7d8fdcdfa24d9f84611495ae740f475f7153ffa7d507e3117343
source_published_at: 2026-11-05T18:27:20Z
first_seen_at: 2026-11-08T02:41:01Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
interpretation_sha256: "sha256:6731169724bef9d70b0b802c0ad059ecaf5058dd3ad18173e492a87981fda109"
description: "MedGraph 是一种面向长期医疗对话的图记忆方法，通过按患者归属事实、链接用药、诊断和测量记录，检索与问题时间相匹配的患者状态。它针对证据过时、混入他人健康信息及遗漏关键安全信息三类记忆错误进行改进。"
external_url: http://arxiv.org/abs/2611.08433v1
parent_observation_id: null
last_seen_at: 2026-11-08T02:28:05.366115Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08433v1](http://arxiv.org/abs/2611.08433v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Donghua Zhang、Zizheng Wang、Ze Dong 等

## 要点解读

### 这是什么
MedGraph 是一种面向长期医疗对话的图记忆方法，通过按患者归属事实、链接用药、诊断和测量记录，检索与问题时间相匹配的患者状态。它针对证据过时、混入他人健康信息及遗漏关键安全信息三类记忆错误进行改进。

### 用在哪里
适用于需要跨多次就诊持续跟踪患者的医疗助手，也可用于需要处理时间变化、关联临床记录和安全信息的纵向医疗对话系统。

### 可以推断的
- 推测：按患者和事件链组织记忆，可能有助于减少跨患者信息混淆，并提高历史状态检索的一致性。
- 推测：集中呈现安全相关事实，可能支持助手在回答涉及用药、诊断或指标的问题时进行更完整的风险检查。

## 来源摘要/节选

> LLM-based medical assistants that follow a patient across visits need a memory that keeps the patient's clinical state correct as it changes. We examine the errors of five memory systems on longitudinal medical dialogue and find three recurring causes: the retrieved evidence gives an outdated state, includes another person's health facts, or lacks a safety fact the answer depends on. We present MedGraph, a graph memory built for these three cases. Construction extracts dated facts from each session, attributes each fact to the person it describes, and links medication, diagnosis, and measurement records into chains that keep earlier states. Retrieval ranks the patient's chains as units, reads each chain at the time the question asks about, and adds the original dialogue text; a patient profile lists every recorded safety fact with every question. On MedMemoryBench, MedGraph has the highest overall accuracy with both a GPT and a Qwen backbone, 10.5 and 10.4 points above the strongest of five baselines, with efficient memory construction and answering in the GPT setting.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。