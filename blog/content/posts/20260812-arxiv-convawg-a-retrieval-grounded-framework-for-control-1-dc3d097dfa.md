---
title: "ConVAWG: A Retrieval-Grounded Framework for Controlled Synthetic Dialogue Generation in Violence Against Women and Girls"
date: 2026-08-12T13:04:56+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:87e7f2c38bb475ad945aebdcd2b0d4fb34a31678946b121e28173dec8d5d678f"
source_payload_sha256: "sha256:32257e61172d8bbee92bc9edf9427cf3eb611a3131bafac17e8f6ca2d5a23444"
observation_id: obs_dc3d097dfa491be5791901a9daa672a696a8b5f31dba89b76d31880f1e331853
event_id: evt_225cac9d1b48cd76f9a727586250946341ccb4c78aa2898ea2c6a24681eb612e
revision_id: rev_ad99bb42c2727f2290bed7b1c32497e06941b24ef37324d0b8708bf92380e3aa
source_published_at: 2026-08-11T17:57:34Z
first_seen_at: 2026-08-12T17:11:57.823676Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 120
interpretation_sha256: "sha256:bcabd611da7456c1de8a1fd5d2e6d1eb215e437dbf6388050886c3883510dc49"
description: "ConVAWG 是一个基于检索的框架，用于生成受控的合成对话，模拟针对妇女和儿童的暴力场景，以多轮对话形式呈现。"
external_url: http://arxiv.org/abs/2608.11200v1
parent_observation_id: null
last_seen_at: 2026-08-12T05:01:46.810800Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11200v1](http://arxiv.org/abs/2608.11200v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Chen Lyu、Xingwei Tan、Simon Cullen 等

## 要点解读

### 这是什么
ConVAWG 是一个基于检索的框架，用于生成受控的合成对话，模拟针对妇女和儿童的暴力场景，以多轮对话形式呈现。

### 用在哪里
适用于研究对话中虐待行为的研究者、需要训练或评估虐待检测模型的技术团队，以及制定预防政策的机构。

### 可以推断的
推测：该数据集能够帮助构建更贴近真实情境的虐待语言检测系统。  
推测：生成的对话可用于分析暴力行为的时序演变，为干预措施提供参考。

## 来源摘要/节选

> Synthetic dialogue generation offers a way to study conversational dynamics in sensitive domains where real data are difficult to access, release, or annotate. The underlying abuse may occur online or offline: threats and coercion can appear directly in messages, while behaviours such as surveillance, isolation, stalking, and physical violence may be planned, disclosed, or referred to conversationally. Privacy and legal constraints make it difficult the release of large-scale real conversation datasets; existing work has mostly focused on sentence-level toxicity of online abuses, leaving a gap in modelling abuse as a relational and temporally unfolding phenomenon. In this work, we focus on modelling Violence Against Women and Girls (VAWG) scenarios as multi-turn dialogues. We introduce ConVAWG, a retrieval-grounded framework for generating CPS-aligned synthetic VAWG chat dialogues. ConVAWG builds scenarios from persona seeds, demographic patterns reported by the UK Office for National Statistics, official crime definitions, and retrieved Domestic Homicide Review cases; converts them into hierarchical event timelines; generates multi-scene role-play dialogues; and applies targeted activation-steered toxicity control to appropriate utterances. We release over 6,000 multi-turn dialogue events across 200 scenarios with rich scenario-, event-, and turn-level metadata. Extensive human evaluation, LLM-as-Judge assessment, ablations, and downstream tasks show strong dialogue quality and domain fidelity.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。