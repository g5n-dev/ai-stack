---
title: "A Framework for Context Enrichment and Selective Robustness in LLM Social Agents"
date: 2026-11-06T08:15:05+08:00
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
first_seen_at: 2026-11-06T00:14:02.485368Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
interpretation_sha256: "sha256:b46da40dfbd50d4ff4fd092dc0e5d94931c07560c0808b25ed1a19500c05e4cd"
description: "这篇论文研究如何通过有控制地补充提示上下文，减少大语言模型智能体在语义不变改写下行为的波动，同时保持对社会环境变化的合理响应。作者提出“上下文增强”和“选择性稳健性”框架，并在囚徒困境类博弈中进行了验证。"
external_url: http://arxiv.org/abs/2611.06914v1
parent_observation_id: null
last_seen_at: 2026-11-06T00:14:02.485368Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.06914v1](http://arxiv.org/abs/2611.06914v1)
- **发布域名**: arxiv.org
- **分类**: cs.MA
- **作者**: Mattia Greiche、Reihaneh Rabbany、Maximilian Puelma Touzel

## 要点解读

### 这是什么
这篇论文研究如何通过有控制地补充提示上下文，减少大语言模型智能体在语义不变改写下行为的波动，同时保持对社会环境变化的合理响应。作者提出“上下文增强”和“选择性稳健性”框架，并在囚徒困境类博弈中进行了验证。

### 用在哪里
该方法适用于社会模拟、智能体行为评估以及提示设计，尤其适合需要检验模型决策是否稳定、是否对重要环境变化敏感的研究者。

### 可以推断的
- 推测：增加上下文并不必然提升稳健性，背景补充的具体方式可能比信息量本身更关键。
- 推测：同一套上下文增强策略在不同模型上的效果可能不同，跨模型应用时需要单独验证。

## 来源摘要/节选

> Researchers use large language models as agents in social simulations, where agents are prompted with observations and background information intended to shape their actions. Yet LLM agents have been shown to substantially change their behavior under meaning-preserving prompt variations, creating a validation problem for social simulation. One plausible hypothesis is that this brittleness reflects a lack of grounding and can be reduced by enriching the context provided to the agents. Whether richer context improves robustness remains unclear, in part because context richness and robustness are rarely defined in ways that support controlled comparisons. We address the first need with controlled context enrichment, a set of prompt substitution rules that systematically enriches distinct types of context: neutral padding, generic social background, descriptive decision grounding, and normative decision grounding. We address the second by introducing selective robustness as a validation criterion: insensitivity to meaning-preserving prompt variation combined with a directional response to decision-relevant changes in the social world. We demonstrate the framework in a Prisoner's Dilemma-like game, showing how it can be used to identify which forms of context enrichment produce more desirable and robust agent behavior. We find that these forms of enrichment produce distinct behavioral patterns that vary between the two models tested.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。