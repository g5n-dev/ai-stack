---
title: "A Framework for Context Enrichment and Selective Robustness in LLM Social Agents"
date: 2026-11-06T02:45:06+08:00
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
first_seen_at: 2026-11-05T18:44:08.981479Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
interpretation_sha256: "sha256:bd199909e7342b791240c04280830cfd15bd91f48707728011ff261ce387e9d7"
description: "这项研究提出受控上下文 enrichment 方法，用来检验不同类型的背景信息能否让 LLM 社会智能体在面对含义不变的提示变化时保持稳定，同时对真正影响决策的社会变化作出正确响应。"
external_url: http://arxiv.org/abs/2611.06914v1
parent_observation_id: null
last_seen_at: 2026-11-05T18:44:08.981479Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.06914v1](http://arxiv.org/abs/2611.06914v1)
- **发布域名**: arxiv.org
- **分类**: cs.MA
- **作者**: Mattia Greiche、Reihaneh Rabbany、Maximilian Puelma Touzel

## 要点解读

### 这是什么
这项研究提出受控上下文 enrichment 方法，用来检验不同类型的背景信息能否让 LLM 社会智能体在面对含义不变的提示变化时保持稳定，同时对真正影响决策的社会变化作出正确响应。

### 用在哪里
适用于构建或验证社会模拟中的 LLM 智能体，尤其适合需要比较“补充上下文是否真的提升可靠性”的研究者。

### 可以推断的
- 推测：评估社会智能体时，应分别检验其对无关措辞变化和关键情境变化的反应，避免把上下文更丰富直接等同于行为更可靠。
- 推测：由于不同模型呈现出不同的行为模式，上下文 enrichment 的效果可能需要针对具体模型单独验证。

## 来源摘要/节选

> Researchers use large language models as agents in social simulations, where agents are prompted with observations and background information intended to shape their actions. Yet LLM agents have been shown to substantially change their behavior under meaning-preserving prompt variations, creating a validation problem for social simulation. One plausible hypothesis is that this brittleness reflects a lack of grounding and can be reduced by enriching the context provided to the agents. Whether richer context improves robustness remains unclear, in part because context richness and robustness are rarely defined in ways that support controlled comparisons. We address the first need with controlled context enrichment, a set of prompt substitution rules that systematically enriches distinct types of context: neutral padding, generic social background, descriptive decision grounding, and normative decision grounding. We address the second by introducing selective robustness as a validation criterion: insensitivity to meaning-preserving prompt variation combined with a directional response to decision-relevant changes in the social world. We demonstrate the framework in a Prisoner's Dilemma-like game, showing how it can be used to identify which forms of context enrichment produce more desirable and robust agent behavior. We find that these forms of enrichment produce distinct behavioral patterns that vary between the two models tested.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。