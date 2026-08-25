---
title: "EG-ARSA: An Expert-Grounded Open Model for Visual Road Safety Auditing in Low-Resource Settings"
date: 2026-08-25T15:09:41+08:00
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
first_seen_at: 2026-08-25T07:07:53.020716Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:12c27a433a60f073c95fed24db194d565756d155770eca34822cf4aeede01eeb"
description: "该研究提出一种将专家道路安全知识转移到轻量级视觉语言模型的技术框架，通过专家校准的教师模型生成监督信号，再蒸馏到学生模型中，使其能够对道路图像进行风险评估。此外还公开了相应的数据集和预训练模型。"
external_url: http://arxiv.org/abs/2608.23563v1
parent_observation_id: null
last_seen_at: 2026-08-25T07:07:53.020716Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23563v1](http://arxiv.org/abs/2608.23563v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Md Thamed Bin Zaman Chowdhury、Moazzem Hossain

## 要点解读

### 这是什么

该研究提出一种将专家道路安全知识转移到轻量级视觉语言模型的技术框架，通过专家校准的教师模型生成监督信号，再蒸馏到学生模型中，使其能够对道路图像进行风险评估。此外还公开了相应的数据集和预训练模型。

### 用在哪里

适用于中低收入国家或地区的道路安全评估工作。交通管理部门、道路建设规划单位或进行道路安全审计的非专业人员可能从中受益，帮助他们在缺乏专业审计人员的情况下进行大规模的道路安全隐患排查。

### 可以推断的

推测：该技术框架在其他视觉语言任务中可能具有迁移价值。由于采用了轻量级模型和知识蒸馏策略，它可能在类似的资源受限场景中发挥作用，例如灾害评估、建筑安全检查等领域。推测：模型的实际部署效果会受限于输入图像的质量和多样性。如果道路图像存在遮挡、光照条件差或拍摄角度不规范等情况，评估准确性可能出现明显下降，这对现场采集流程提出了一定的要求。

## 来源摘要/节选

> Road traffic injuries remain a major challenge in low- and middle-income countries, where proactive road safety auditing is limited by incomplete crash records, shortages of qualified auditors, and the high cost of large-scale field inspections. To address this problem, we propose Expert-Grounded Distillation (EGD), a novel artificial intelligence framework that transfers institutional road safety expertise into a compact vision-language model for scalable visual road safety auditing. The key innovation is a quantified expert-grounding stage in which the teacher vision-language model is calibrated against authoritative field audits. Large-scale annotation is permitted only after the teacher reaches substantial agreement with expert risk assessments (Cohen's kappa = 0.74). The calibrated teacher then generates structured supervision that is distilled into an 8-billion-parameter student vision-language model using Low-Rank Adaptation and a single leakage-free prompt. We also introduce Bangladesh Road Safety Audit (BD-ARSA), the first open, expert-grounded Bangladeshi visual road safety audit dataset containing 21,947 image-audit records with near-national coverage, and Expert-Grounded Road Safety Auditor (EG-ARSA), the first vision-language model developed specifically for this task. Experimental results show that grounded fine-tuning substantially improves ordinal risk assessment over the zero-shot baseline, while blind expert evaluation demonstrates that the compact student outperforms both its 31 billion-parameter teacher and Gemini-2.5-Flash. These findings demonstrate that EGD provides an effective and scalable engineering solution for proactive road safety auditing in resource-constrained environments.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。