---
title: "Necessary or Sufficient? Evaluating LLM Explanations With Behavioural Evidence"
date: 2026-09-09T02:43:01+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:624590f7d8cfc953d142edc68e270bebdb86f257bb4e13f2b32b5b231e155016"
source_payload_sha256: "sha256:d2c81bc08ee6b44d796b4ffb9da8a2fc239c925d534da1bd8b5febeefe0ba86f"
observation_id: obs_eb6fbda78057317da7e1ae25dbc32e2c465b19127fe4d6b3d5558b20c568bcc2
event_id: evt_58b887b188c21f738ae7303a0c1258c6bbc2b89938c1c821c386f5219a8d2ad6
revision_id: rev_6596a0135d3250fd696aea9193be3c8a0cf8811c9394c73186e494740b4422f0
source_published_at: 2026-09-04T17:37:17Z
first_seen_at: 2026-09-08T18:53:36Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
interpretation_sha256: "sha256:4975469d7b8737be8448eb1177ac465f35ed4b11b61d67f98492507ffa619854"
description: "该研究通过黑盒干预衡量语言模型生成的因素解释是否满足必要性（改变该因素会导致输出变化）或充分性（保留该因素而移除其他可变信息仍能保持输出），并把解释排名与实验得分进行相关性分析，涉及两类合成任务。"
external_url: http://arxiv.org/abs/2609.05385v1
parent_observation_id: null
last_seen_at: 2026-09-08T18:39:56.160717Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.05385v1](http://arxiv.org/abs/2609.05385v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Urja Pawar、Rajitha Ramanayake、Nabeel Kemal 等

## 要点解读

### 这是什么  
该研究通过黑盒干预衡量语言模型生成的因素解释是否满足必要性（改变该因素会导致输出变化）或充分性（保留该因素而移除其他可变信息仍能保持输出），并把解释排名与实验得分进行相关性分析，涉及两类合成任务。  

### 用在哪里  
适用于在开发或审查基于语言模型的代理系统时，需要验证模型提供的解释是否可靠的研发人员和安全审查人员，尤其是负责监控、调试或对模型输出进行人工复核的角色。  

### 可以推断的  
- 推测：模型列出的前三位因素并不总是能够准确指向实际影响输出的关键因素。  
- 推测：任务类型可能导致解释可信度差异，例如风险或危害判断类任务的解释相对更贴近实际影响力。

## 来源摘要/节选

> LLM decision components that can operate within agent workflows often produce action-relevant recommendations or judgements together with explanations. Operators may use the named factors to monitor a system, diagnose errors, or decide when to escalate an output. Such use assumes that the explanations agree with the component's observable decision behaviour. We test two interpretations of the named factors: necessity, meaning that changing a factor would change the output, and sufficiency, meaning that retaining it while removing other changeable information would preserve the output. We evaluate these interpretations in two synthetic use cases: recommending advisors to clients and judging prompts for harmfulness or risk. Models return an output and the top three factors that most influenced it. Controlled black-box interventions estimate a necessity score for each factor by measuring how often changing it changes the output, and a sufficiency score by measuring how often retaining it preserves the output. Across eight models from the Claude, GPT, and Gemini families, the mean Spearman correlations between the cited ranking and the necessity and sufficiency scores are 0.349 and 0.354 for advisor recommendation, and 0.431 and 0.580 for prompt monitoring. Furthermore, an uncited factor scores above the lowest-scoring cited factor in 57.6% of advisor responses under necessity and 58.1% under sufficiency; the corresponding prompt-monitoring rates are 25.8% and 8.9%. The cited top three contain useful information but do not reliably identify the three factors with the strongest measured influence under necessity or sufficiency. The framework provides a black-box reliability check for explanations used in agent oversight while remaining scoped to individual LLM decisions.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。