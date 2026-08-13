---
title: "A Cascaded Unsupervised-Supervised NLP Pipeline for Detecting Accusatory Language in Public Procurement"
date: 2026-08-14T06:06:12+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "自然语言处理", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ce34ea94378e7e7e39a434f51b26448d9342877e7e5f69f2a8ee9a3b4078d90e"
source_payload_sha256: "sha256:42892463864dea2e799de88e1e1a7862eddf541dd3287e2fdf519ce44fdfbfc3"
observation_id: obs_628431c73f3782f18fdd0002f9841186f5d63999cd17c890545a636755d15430
event_id: evt_cb1c1ae6895e0e801fd748859e75d6da238712ae031f06300057ba9e003bae59
revision_id: rev_ef8c01ba2453cab7fb9854792a1703754818bc9c16a44bc1db592d4ad016e16c
source_published_at: 2026-08-12T17:09:14Z
first_seen_at: 2026-08-13T22:15:17Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 103
interpretation_sha256: "sha256:c92af1d730c0cc1e936780da22344c4c76cce2ae3ae246b8bb07325c79c93d6e"
description: "该研究提出一种结合无监督聚类与有监督分类的 NLP 流程，从政府采购系统的参与者在预合同阶段的评论中挖掘潜在异常，识别指控性或举报式语言。"
external_url: http://arxiv.org/abs/2608.12269v1
parent_observation_id: null
last_seen_at: 2026-08-13T22:02:34.872181Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12269v1](http://arxiv.org/abs/2608.12269v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Bryan Torres、Daniel Riofrío、José Vega-Sánchez 等

## 要点解读

### 这是什么
该研究提出一种结合无监督聚类与有监督分类的 NLP 流程，从政府采购系统的参与者在预合同阶段的评论中挖掘潜在异常，识别指控性或举报式语言。

### 用在哪里
适用于政府采购监管、审计或透明度提升项目，需要在大量公开评论中快速筛查出可能存在违规倾向的文本；可帮助监管部门提前预警或进行风险评估。

### 可以推断的
推测：该流程在缺少大量标注数据的情况下，可先通过无监督聚类发现异常评论群，再利用少量标注数据进行有监督分类，从而降低人工标注成本。  
推测：轻量级的领域适配模型能够在资源受限

## 来源摘要/节选

> Public procurement involves the allocation of substantial financial resources; therefore, continuous oversight through audits, controls, and monitoring mechanisms is essential. However, stakeholder comments and publicly available government data are often underutilized, despite their potential to reveal procedural irregularities. To address this gap, this paper analyzes metadata from Ecuador's Sistema Oficial de Contratación Pública (SOCE, Official Public Procurement System), with particular emphasis on participant comments generated during the pre-contractual phase. We propose a hybrid modeling framework that integrates unsupervised clustering and supervised classification within a natural language processing (NLP) pipeline to uncover latent patterns and detect potentially irregular procurement processes. Semantic embeddings are generated using Word2Vec, LLaMA, and RoBERTa, followed by Gaussian Mixture Models (GMMs) for unsupervised clustering. A supervised classification stage is then applied to identify accusatory or whistleblowing-style comments. Experimental results show that the combination of domain-trained Word2Vec embeddings, GMM-based clustering, and a Random Forest classifier achieves high precision and recall, even under severe class imbalance. These findings demonstrate that lightweight, domain-adapted NLP architectures can effectively support risk identification and enhance transparency in public procurement systems without requiring large-scale computational infrastructure.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。