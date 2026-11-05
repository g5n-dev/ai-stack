---
title: "A Framework for Context Enrichment and Selective Robustness in LLM Social Agents"
date: 2026-11-05T17:08:16+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "cs.MA", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:52f38482c710206d483021c7e793701b2120f5da6a7c69b04585d73c28abdc7a"
source_payload_sha256: "sha256:19a68cc17394bd15ce06496ebbc5adcfa9e77726603cd699c14b19b333250eba"
observation_id: obs_1ba2bc1e6399e93d4fd435a7c22726067a41e0e5dc538d05675de7d9f0122609
event_id: evt_6946cf536ab340e76842588cd231fa56c3c087cc3499c2db340bd1952f46e8f6
revision_id: rev_ead2c1cd509fc98e579041956d166473843e5e9e94c57320a6901c99c4efc374
source_published_at: 2026-11-04T18:58:23Z
first_seen_at: 2026-11-05T09:06:32.511252Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
interpretation_sha256: "sha256:74abb25a8f853933c0470b074a522730288dc7ce26e043efa7bbd046d09377a2"
description: "该研究提出一套面向大语言模型社会智能体的上下文增强与选择性稳健性评估框架。它通过受控替换不同类型的提示上下文，并结合“面对等价改写保持稳定、对社会环境中的关键变化产生合理响应”来检验智能体行为。"
external_url: http://arxiv.org/abs/2611.06914v1
parent_observation_id: null
last_seen_at: 2026-11-05T09:06:32.511252Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.06914v1](http://arxiv.org/abs/2611.06914v1)
- **发布域名**: arxiv.org
- **分类**: cs.MA
- **作者**: Mattia Greiche、Reihaneh Rabbany、Maximilian Puelma Touzel

## 要点解读

### 这是什么
该研究提出一套面向大语言模型社会智能体的上下文增强与选择性稳健性评估框架。它通过受控替换不同类型的提示上下文，并结合“面对等价改写保持稳定、对社会环境中的关键变化产生合理响应”来检验智能体行为。

### 用在哪里
该框架适合用于社会模拟研究中的提示设计、行为验证和上下文增强策略比较，尤其适用于囚徒困境类互动游戏中的智能体评估。

### 可以推断的
- 推测：增加上下文信息不必然带来更稳健的行为，关键可能在于信息与决策的关联方式。
- 推测：理想的智能体既要避免被无关措辞扰动，也不能忽视会改变决策的社会情境变化。

## 来源摘要/节选

> Researchers use large language models as agents in social simulations, where agents are prompted with observations and background information intended to shape their actions. Yet LLM agents have been shown to substantially change their behavior under meaning-preserving prompt variations, creating a validation problem for social simulation. One plausible hypothesis is that this brittleness reflects a lack of grounding and can be reduced by enriching the context provided to the agents. Whether richer context improves robustness remains unclear, in part because context richness and robustness are rarely defined in ways that support controlled comparisons. We address the first need with controlled context enrichment, a set of prompt substitution rules that systematically enriches distinct types of context: neutral padding, generic social background, descriptive decision grounding, and normative decision grounding. We address the second by introducing selective robustness as a validation criterion: insensitivity to meaning-preserving prompt variation combined with a directional response to decision-relevant changes in the social world. We demonstrate the framework in a Prisoner's Dilemma-like game, showing how it can be used to identify which forms of context enrichment produce more desirable and robust agent behavior. We find that these forms of enrichment produce distinct behavioral patterns that vary between the two models tested.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。