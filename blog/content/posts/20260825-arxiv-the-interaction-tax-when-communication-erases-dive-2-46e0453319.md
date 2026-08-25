---
title: "The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams"
date: 2026-08-25T22:06:13+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.MA", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b355e57921e2431b33d49cdae6ae192e934ef0fb14f430e131e116050dd752f8"
source_payload_sha256: "sha256:932ff5933a84c73f3e936ee3dc16f7a66498c236a13c488ac5a57e27be03e24b"
observation_id: obs_46e0453319385edf26c4d13c6616fa4684478d4c89ffafe513eae48b32f19c12
event_id: evt_e001b631c5d7b6bddb6f8b18a7057e369f9981383cd69cb2028ea53ed7a71398
revision_id: rev_447fd4670be1ebc8af514eb4a7c094b0f8dbf0d6850513ff93c466086ff909e4
source_published_at: 2026-08-24T17:45:15Z
first_seen_at: 2026-08-25T14:15:51Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
interpretation_sha256: "sha256:75870c4b32cc35b7f959820b1daef8a7584f1a519fcf9bcdf578b541a903a6f5"
description: "该文提出“多交互税”（interaction tax）概念：当多个大语言模型代理相互读取完整答案时，方案在单轮内趋于相同，失去多样性。作者在匹配预算的若干验证任务上比较全答案交互与独立生成，发现全答案交互效果弱，独立生成可保持思路分散，从而避免多样性崩溃。"
external_url: http://arxiv.org/abs/2608.23541v1
parent_observation_id: null
last_seen_at: 2026-08-25T14:03:36.677635Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23541v1](http://arxiv.org/abs/2608.23541v1)
- **发布域名**: arxiv.org
- **分类**: cs.MA
- **作者**: Summer Eunhyung Ann、Haokun Liu、Chenhao Tan

## 要点解读

### 这是什么
该文提出“多交互税”（interaction tax）概念：当多个大语言模型代理相互读取完整答案时，方案在单轮内趋于相同，失去多样性。作者在匹配预算的若干验证任务上比较全答案交互与独立生成，发现全答案交互效果弱，独立生成可保持思路分散，从而避免多样性崩溃。

### 用在哪里
适用于研究多智能体协同、系统设计以及评估大语言模型协作策略的研究者和工程师，尤其在需要保持方案多样性的场景（如辩论、审查循环、混合代理合成）中，可帮助判断信息共享方式对最终性能的影响。

### 可以推断的
推测：在需要多种解决思路的任务中，避免直接让代理共享完整答案有助于保留各自独特的方法。  
推测：若必须进行交互，仅传递关键约束或错误提示而非全部输出，可能在保持效率的同时防止思路趋同。

## 来源摘要/节选

> Does multi-agent LLM interaction help or hurt? Some work reports gains from debate (Du et al., 2024), critique loops (Chen et al., 2025), and mixture-of-agents synthesis (Wang et al., 2025), while other work finds that interaction adds cost without improving quality under equal budgets (Tran &amp; Kiela, 2026; Xu et al., 2026; Jarrett et al., 2025), or that independent sampling already captures multi-agent gains (Li et al., 2024). We argue this contradiction partly reflects a missing distinction, because not all multi-agent communication is equal. Different model families find structurally different solutions, but when agents read each other's complete outputs, their proposals converge within one round, erasing the diversity that motivates using multiple models. We call this the interaction tax. We test 11 verifier-scored optimization tasks under matched budgets and find that full-solution interaction is a weak default. Independent proposal generation avoids this collapse. Full-solution interaction mainly makes agents stay close to the first solution they see instead of trying different approaches, and critique helps only if the violated rule is easy for the LLM to find and fix. These results suggest that multi-agent performance depends less on the number of agents than on the information they exchange, and interaction helps only when agents share the right information at the right time.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。