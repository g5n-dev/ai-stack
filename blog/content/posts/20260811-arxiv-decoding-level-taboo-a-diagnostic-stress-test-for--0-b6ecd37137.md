---
title: "Decoding-Level Taboo: A Diagnostic Stress Test for LLM Robustness"
date: 2026-08-11T21:45:23+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Prompt 工程", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:35ecb1312a67ae7b6d8e190b625432340cb5633742e744f2f2062c77b0f39383"
source_payload_sha256: "sha256:7f1919a5d94292d41cb5241464199835641f607a5a63a6a5ac982f3b1c51d8c5"
observation_id: obs_b6ecd3713775f72f66cbda875304dde5a8067c201e9468f4ed480095e204c9fd
event_id: evt_83d9dbbbdc8328f28fe9ab611b19fc50dd259139c418ecd9daf6d746c605b648
revision_id: rev_8f631c371a32243a9c5c67f0428bda1b432abda29fe689398dff0555c5f98367
source_published_at: 2026-08-10T17:47:24Z
first_seen_at: 2026-08-11T13:42:17.585710Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:7974d2d200c456bdb30852ca92a1af2ae933cb37b254b1bf083171d7305f9498"
description: "一种在模型解码阶段直接干预概率分布的零提示诊断测试，通过在词边界动态屏蔽主要候选标记，强迫模型产生迂回表达，从而评估其在非正常生成路径下的鲁棒性。"
external_url: http://arxiv.org/abs/2608.09900v1
parent_observation_id: null
last_seen_at: 2026-08-11T13:42:17.585710Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09900v1](http://arxiv.org/abs/2608.09900v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Tadanobu Chuyo Kamijo、Ori Rottenstreich、Javier Conde 等

## 要点解读

### 这是什么
一种在模型解码阶段直接干预概率分布的零提示诊断测试，通过在词边界动态屏蔽主要候选标记，强迫模型产生迂回表达，从而评估其在非正常生成路径下的鲁棒性。

### 用在哪里
适用于模型研发和安全审计阶段，可用于生成多样化合成数据、检验运行时安全护栏以及在真实部署前对模型可靠性进行压力测试。

### 可以推断的
推测：规模更大的模型在面对强制偏离常规生成路径的干预时往往保持更好的鲁棒性。  
推测：经过指令对齐训练的模型在解码层面的干预下更少出现失效。

## 来源摘要/节选

> Large language model evaluations typically focus on performance under nominal conditions, creating an illusion of capability where models comfortably walk a narrow, highly optimized generation corridor. In real-world deployments, however, complex system prompts, safety guardrails, and structural constraints continuously force models off this nominal path, driving a divergence between benchmark scores and deployment performance. To address this issue, we introduce Decoding-Level Taboo, a zero-prompt diagnostic stress test that intervenes directly in logit space at runtime, forcing models out of their nominal paths. By dynamically masking primary candidate tokens at word boundaries, Taboo forces machine circumlocution.
> Evaluating Taboo across several open-weight model families reveals that off-path robustness is heavily influenced by both parameter scale and post-training instruction alignment, with robustness generally improving with model size and alignment. Beyond the results presented in this paper, Taboo provides a novel primitive for generating diverse synthetic datasets, stress-testing runtime safety guardrails, and auditing model reliability prior to real-world deployment.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。