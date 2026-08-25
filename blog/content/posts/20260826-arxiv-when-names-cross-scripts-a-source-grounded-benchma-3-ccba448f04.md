---
title: "When Names Cross Scripts: A Source-Grounded Benchmark for Historical Entity Reconciliation in the Mongol World"
date: 2026-08-26T04:48:01+08:00
draft: false
entry_kind: "auto"
tags: ["自然语言处理", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cafa55926523f9a8402e3acbdb5ab7094c87af6fd3fa713454c9d19a9e987e39"
source_payload_sha256: "sha256:d96ccca5da4ae943e5ec14696f7bf2e128d1dcd91036f315fd07768097961d44"
observation_id: obs_ccba448f04547e5193fe00fe81192c51d7033e0f7695e62cc35216b31df9420d
event_id: evt_e0353895dfb84f742a4cc9249a0fcd008a8880bdfafa09cd4add8e2bc577acc6
revision_id: rev_21eb01f6d043a6724c7ca500c71fe2447b260f227dd7dfaaa8cd2a2ab4e8c6e4
source_published_at: 2026-08-24T17:10:36Z
first_seen_at: 2026-08-25T20:58:37Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 110
interpretation_sha256: "sha256:0bc4212c218e8915f270a8ba67e45e10242028c71dd83ea1c35ba40b81aed091"
description: "该内容介绍一种针对蒙古世界中历史人物姓名的跨语言、跨文字对齐评估基准，提供基于来源证据的成对身份验证任务和仅基于姓名的对照测试集。"
external_url: http://arxiv.org/abs/2608.23507v1
parent_observation_id: null
last_seen_at: 2026-08-25T20:45:35.583042Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23507v1](http://arxiv.org/abs/2608.23507v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Xiang Chen、Zeyu Zhang

## 要点解读

### 这是什么  
该内容介绍一种针对蒙古世界中历史人物姓名的跨语言、跨文字对齐评估基准，提供基于来源证据的成对身份验证任务和仅基于姓名的对照测试集。  

### 用在哪里  
适用于开发或评估能够处理古代文献、跨语言、跨文字记载的自然语言处理系统，尤其是需要区分同名不同人的研究项目。  

### 可以推断的  
推测：该基准可以帮助判断生成系统在缺乏表面名称信息时，是否能够利用历史上下文进行正确的人物身份消歧。  
推测：在实际历史研究中，若需将不同文字来源的同名人物区分开来，可借助该基准检验模型利用证据的能力。

## 来源摘要/节选

> Historical people may appear under different languages, scripts, and transcription traditions, while distinct individuals may share highly similar or even identical names. This makes historical identity reconciliation more than a problem of string matching or transliteration. We introduce MHER, a provenance-controlled benchmark for pairwise reconciliation of person-name attestations from the Mongol world. MHER contains a balanced 396-pair Name-only core over 84 primary historical persons and a stricter 160-pair Source-grounded subset constructed from mention-by-source evidence, with entity-disjoint development and test splits.
> Across five generative systems, correctly Source-grounded evidence improves paired TEST accuracy by 12.96 to 94.44 percentage points relative to Name-only input. On five identical-surface different-person cases, all models fail under names alone (0/25 model-item decisions), whereas Source-grounded evidence yields 24/25 correct resolutions, with the remaining output an abstention. Context-only ablations show that historical descriptions often carry substantial identity information, while explicitly signaled misgrounding controls produce substantially lower performance. We also find that names are not uniformly beneficial: for Qwen3-8B, restoring surface forms converts ten otherwise correct Context-only distinctions into false identity merges.
> These results show that historical entity reconciliation depends not only on surface correspondence, but on whether identity judgments respond appropriately to provenance-controlled historical evidence. MHER therefore provides a controlled framework for studying evidence use, abstention, and failure modes in historical NLP.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。