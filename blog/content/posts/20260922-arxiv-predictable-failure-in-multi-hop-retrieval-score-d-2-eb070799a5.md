---
title: "Predictable Failure in Multi-Hop Retrieval: Score-Distributional Confidence Scoring and Abstention"
date: 2026-09-22T08:08:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.IR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a4eb9a6505f0d5da7ed7b83bd80d8fe46382183ba2e4d7946e9328fd68e83996"
source_payload_sha256: "sha256:baace38f1baedf3eba5e2e8e3a07918ae572a95400c3cf20015e0e5203c14f1e"
observation_id: obs_eb070799a5a92ac05eb6cbba770c9e6e95c734111ac08b0d5bf6ccadd78f55e5
event_id: evt_b5aaca2a75918a84f17ebe28ad6c60a62ec9cffe4216ff7bc1f89c783a386204
revision_id: rev_d6313a489299232962c86770f0d6dbe5935f2e029442510f4dc76be13d46030e
source_published_at: 2026-09-18T17:48:15Z
first_seen_at: 2026-09-22T00:06:44.957934Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:1de229eb03604be78fd53449642812dc8fdf3c729f3ded4a23a4c7e3a048ab1c"
description: "这项研究指出多跳检索系统的失败并非随机出现，而是集中在某些可预测的查询类型中。研究提供了理论分析，说明在特定条件下可以通过查询的结构特征来识别可能的失败，并通过一个基于多个查询-检索特征计算置信度分数的方法，在不需要额外语言模型调用的情况下实现校准的放弃策略。"
external_url: http://arxiv.org/abs/2609.22056v1
parent_observation_id: null
last_seen_at: 2026-09-22T00:06:44.957934Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.22056v1](http://arxiv.org/abs/2609.22056v1)
- **发布域名**: arxiv.org
- **分类**: cs.IR
- **作者**: Andre Bacellar

## 要点解读

### 这是什么
这项研究指出多跳检索系统的失败并非随机出现，而是集中在某些可预测的查询类型中。研究提供了理论分析，说明在特定条件下可以通过查询的结构特征来识别可能的失败，并通过一个基于多个查询-检索特征计算置信度分数的方法，在不需要额外语言模型调用的情况下实现校准的放弃策略。

### 用在哪里
该研究适合检索系统开发者和评估人员参考，特别是在构建需要高可靠性多跳问答系统的场景。对于关注检索系统置信度评估和失败检测的研究者，其理论框架和评估指标设计也具有参考价值。

### 可以推断的
推测：在实际部署中，通过分析查询的表面特征来预测检索失败可能成为提升系统鲁棒性的低成本方案，尤其适用于对延迟敏感或调用成本较高的生产环境。

推测：研究强调的特征互补性意味着，单一的检索评分机制难以覆盖所有失败模式，实际系统可能需要结合多种信号来评估检索质量。

## 来源摘要/节选

> Multi-hop retrieval failures are not uniformly distributed across queries: they cluster in structurally predictable subpopulations. We prove two results formalizing this structure. First (CWAR Reducibility): confident-failure reduction is achievable if and only if retrieval features carry mutual information about success, a condition satisfied by LLM-judge pipelines but substantially weaker in dense-only settings, explaining the AUC-AC gap between regimes. Second (Feature Regime Complementarity): no single ANN score feature achieves best predictive performance across all failure regimes; the dominant feature differs between datasets (query length on MuSiQue, hop-1 concentration on HoVer), and a constructive witness pair shows each is necessary in one regime and non-contributory in the other. We instantiate these principles in RegimeAbstain, which computes a Retrieval Confidence Score (RCS), a logistic function of up to nine query-ANN structural features, all available without any additional LLM call, and uses it to implement a calibrated abstention policy. We define the Confident-Wrong-Answer Rate (CWAR) metric and evaluate across three multi-hop benchmarks (MuSiQue, 2WikiMultiHopQA, HoVer) and two retrieval architectures (LLM-judge and dense-only), covering five failure regimes with CWAR from 14.5% to 62.1%. RCS achieves best or co-best AUC-AC in all five conditions against eight confidence baselines. On MuSiQue (LLM-judge), RCS reduces CWAR from 39.5% to 20.6% at 50% coverage (47.8% relative reduction), with ECE=0.035. A model trained on MuSiQue transfers to 2WikiMultiHopQA with only -0.5pp AUC loss, confirming the domain-agnostic structure of regime features.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。