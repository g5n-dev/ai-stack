---
title: "Molecular Déjà Vu: Digit-Level Retrieval of Published Values in Frontier Language Models"
date: 2026-09-09T08:16:31+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Prompt 工程", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:fc25c88d9e252929e979e58431f4c6a5caf510c93d68fe88bfa9c37572c31abe"
source_payload_sha256: "sha256:53244c5d709f69ea286bf15eebc523d8b98ca39977baff96e964d7e520c6b377"
observation_id: obs_8d70f60d09d2aa5f2953489a117f8f12b0762267fb507127b6c15eab4d9754ad
event_id: evt_bb7b27f60f531efebb90b330122033e4492bc877ef61a3ac97a071463cd53bf8
revision_id: rev_6158d58338ec668e161b2429b094a84d2f815d25c4271d4e0e593eec1c466018
source_published_at: 2026-09-04T17:32:48Z
first_seen_at: 2026-09-09T00:14:06.983788Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
interpretation_sha256: "sha256:ace16f0b46c91abf607980736e5044ccc43bb29d33202779db0220c64e50f945"
description: "该内容报告了对前沿语言模型在分子属性回归基准上是否会逐字检索已发布数值的研究。作者对多个模型在多个基准上进行审计，比较模型在相同分子和相同提示下的输出与已有文献数值的匹配程度，并分析了推理层次对检索行为的影响。"
external_url: http://arxiv.org/abs/2609.05381v1
parent_observation_id: null
last_seen_at: 2026-09-09T00:14:06.983788Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.05381v1](http://arxiv.org/abs/2609.05381v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Matthias Busch、Marius Tacke、Sviatlana V. Lamaka 等

## 要点解读

### 这是什么  
该内容报告了对前沿语言模型在分子属性回归基准上是否会逐字检索已发布数值的研究。作者对多个模型在多个基准上进行审计，比较模型在相同分子和相同提示下的输出与已有文献数值的匹配程度，并分析了推理层次对检索行为的影响。

### 用在哪里  
适用于分子性质预测任务的模型评估与基准设计，尤其是需要区分模型真实学习能力与记忆已有数据的研究者和工程师；也可供关注大模型训练数据泄露问题的 AI 安全与公平性研究参考。

### 可以推断的  
推测：在使用更高级的推理策略时，模型更容易触发对已有文献数据的检索，使得相同输入在低层次推理下不出现匹配而在高层次推理下出现匹配。  
推测：若在评估或部署阶段抑制直接检索，模型的预测误差在不同模型之间可能趋于接近，从而更真实地反映其学习到的泛化能力。

## 来源摘要/节选

> Large language models (LLMs) are increasingly evaluated on molecular property benchmarks, but accuracy cannot distinguish a model that predicts a property from one that retrieves a published number. We audit 22 frontier models on 12 regression benchmarks for verbatim retrieval and find that it is widespread but relatively benchmark-specific: on five datasets more than $50\%$ of the LLMs show verbatim retrieval, while on the remaining datasets it appears only in isolated cells. We run our experiments at two reasoning levels and find that reasoning changes retrieval. The same experiments, on the same molecules and with the same prompt, are flagged $89\%$ more often at the higher reasoning level than at the lowest one. Finally, we test a way to interrupt retrieval in our most contaminated cases, and find that the strongest models in some cases still recognise a combination of transformed SMILES strings and original labels. Furthermore, suppressing retrieval moves the prediction errors of the different models closer together in relative terms, while their differing use of verbatim retrieval spreads them apart. This indicates that the general predictive capability of an LLM is not determined solely by the amount of memorised values. This work provides an overview of the amount and depth of verbatim retrieval in molecular regression benchmarks using LLMs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。