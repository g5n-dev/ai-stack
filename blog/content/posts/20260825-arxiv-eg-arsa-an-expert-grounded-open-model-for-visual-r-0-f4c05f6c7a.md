---
title: "EG-ARSA: An Expert-Grounded Open Model for Visual Road Safety Auditing in Low-Resource Settings"
date: 2026-08-25T15:59:55+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:25380b923afe036d6f6ca67a24b02a832e190a77ab4943316fcfd3aa5ba9fd2b"
source_payload_sha256: "sha256:6a017c5a69c07fa81c24af81a07182491d6781c8d9a4dd783c707e8370c002b6"
observation_id: obs_f4c05f6c7afe23690233e2a5090bf342edda16445de5664eac1d13b7df5c91f8
event_id: evt_3d5bcfedf2f5a1ee5def60afb078ab638b571b373d8548066eebcd7a001fc9e8
revision_id: rev_0dbb46ae547c0f364b7a1d56fc6335695390de39ea04822bd3c464d913ed5b53
source_published_at: 2026-08-24T17:58:41Z
first_seen_at: 2026-08-25T08:09:04Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:6f1318f8546a31dc223daf9f79a400c612c3173bda7cdb1f64f57872d66d06e4"
description: "这是一个将专家道路安全评估知识迁移到轻量级视觉语言模型的框架，通过专家校准的教师模型生成监督信号来训练更小的学生模型，用于可扩展的道路安全视觉审计。"
external_url: http://arxiv.org/abs/2608.23563v1
parent_observation_id: null
last_seen_at: 2026-08-25T07:57:54.617724Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23563v1](http://arxiv.org/abs/2608.23563v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Md Thamed Bin Zaman Chowdhury、Moazzem Hossain

## 要点解读

### 这是什么
这是一个将专家道路安全评估知识迁移到轻量级视觉语言模型的框架，通过专家校准的教师模型生成监督信号来训练更小的学生模型，用于可扩展的道路安全视觉审计。

### 用在哪里
适用于中低收入国家或地区的道路安全管理，这些地方缺乏完整的交通事故记录和专业审计人员。该框架可以帮助相关部门对道路安全风险进行大规模评估和筛查。

### 可以推断的
推测：该方法采用了模型蒸馏技术，这种技术通常用于在保持性能的前提下降低模型的计算资源需求，说明设计者考虑了实际部署环境的硬件限制。

推测：使用专家校准的方式来生成训练数据，能够在缺乏大规模标注数据的领域提供相对可靠的监督信号，这对于资源受限地区的应用具有重要价值。

## 来源摘要/节选

> Road traffic injuries remain a major challenge in low- and middle-income countries, where proactive road safety auditing is limited by incomplete crash records, shortages of qualified auditors, and the high cost of large-scale field inspections. To address this problem, we propose Expert-Grounded Distillation (EGD), a novel artificial intelligence framework that transfers institutional road safety expertise into a compact vision-language model for scalable visual road safety auditing. The key innovation is a quantified expert-grounding stage in which the teacher vision-language model is calibrated against authoritative field audits. Large-scale annotation is permitted only after the teacher reaches substantial agreement with expert risk assessments (Cohen's kappa = 0.74). The calibrated teacher then generates structured supervision that is distilled into an 8-billion-parameter student vision-language model using Low-Rank Adaptation and a single leakage-free prompt. We also introduce Bangladesh Road Safety Audit (BD-ARSA), the first open, expert-grounded Bangladeshi visual road safety audit dataset containing 21,947 image-audit records with near-national coverage, and Expert-Grounded Road Safety Auditor (EG-ARSA), the first vision-language model developed specifically for this task. Experimental results show that grounded fine-tuning substantially improves ordinal risk assessment over the zero-shot baseline, while blind expert evaluation demonstrates that the compact student outperforms both its 31 billion-parameter teacher and Gemini-2.5-Flash. These findings demonstrate that EGD provides an effective and scalable engineering solution for proactive road safety auditing in resource-constrained environments.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。