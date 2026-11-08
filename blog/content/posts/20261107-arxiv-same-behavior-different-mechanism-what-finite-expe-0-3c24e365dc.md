---
title: "Same Behavior, Different Mechanism: What Finite Experiments Can Certify About Integrated Information"
date: 2026-11-07T15:09:13+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:14ac50c28ebc950c69aca426ed13f56d65835f976c83c9f679b68c6de0372223"
source_payload_sha256: "sha256:5e510529c6892a4c467e5b474e6b7329c2bad657fef7604d4cce500106612278"
observation_id: obs_3c24e365dcd0b526902e73ac659b8a6deffee737e86f4b30edc3f660c1ab008c
event_id: evt_12ea0e95eef93c30f3f0e7941fc271467be74e541d682b9b6725e420fc55a80e
revision_id: rev_eba475af4725f3e70c56e8138309766a4313d98d48dc7c142e4f07a920fdd6d3
source_published_at: 2026-11-05T18:55:31Z
first_seen_at: 2026-11-07T07:19:35Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 100
interpretation_sha256: "sha256:f5c3beedecd780198632f75f6592b3e5ad35d97c83a4b85d7e45e677eb56ec0a"
description: "这项工作研究：仅凭有限、部分且带噪声的实验数据，能否可靠识别系统的机制级指标——整合信息论中的整合信息 \\(\\varphi\\)。文章在四、五单元随机网络中分析可辨识性、数据可认证性、误差边界及参数变化导致的突变。"
external_url: http://arxiv.org/abs/2611.08469v1
parent_observation_id: null
last_seen_at: 2026-11-08T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08469v1](http://arxiv.org/abs/2611.08469v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Linqian Wu、Diaoxuan He

## 要点解读

### 这是什么
这项工作研究：仅凭有限、部分且带噪声的实验数据，能否可靠识别系统的机制级指标——整合信息论中的整合信息 \(\varphi\)。文章在四、五单元随机网络中分析可辨识性、数据可认证性、误差边界及参数变化导致的突变。

### 用在哪里
适用于需要从有限实验评估内部机制而非只看输出的场景，例如可解释性分析、AI 审计、机器意识评估，以及实验访问方式和采样方案设计。

### 可以推断的
- 推测：内部记录、干预方式和实验预算会直接影响机制级指标能否被可信地测得。
- 推测：若研究目标只要求判断 \(\varphi\) 是否高于某一阈值，有限数据仍可能提供可认证的单侧结论。

## 来源摘要/节选

> Interpretability, AI auditing and assessments of machine consciousness increasingly rest on mechanism-level quantities: functionals of a system's causal transition law that describe how it computes, not what it outputs. Experiments see that law only through finite, partial and noisy interventions. We ask when such a quantity is identifiable from an experiment's access, continuous in the mechanism and certifiable from finite data, and answer exactly for a deliberately demanding case - the integrated information $\varphi$ of integrated information theory - in stochastic networks of four and five units with known ground truth. Behavior can be silent: a recurrent and a feed-forward network with identical input-output laws at their response delay carry 0.28 and 0 bits, yet internal recordings separate them within 4-53 trials. Partial access can be just as blind: in our examples, units left out of a one-step recording impose precision floors of 0.30-1.02 bits that no sample size lowers, and in all-but-self parity networks, recordings of any length see several hidden units only through the product of their fidelities - a symmetry that one intervention broke in exact checks. The measure has sharp edges: because $\varphi$ selects a partition, and the cause and effect it specifies, by one criterion and reports another, infinitesimal changes of mechanism that cross an edge change it by 25-100% at 99% of the edges we found in random networks, and about 1% of surrogate models that fit interventional data almost perfectly misreport it by more than 20%. One-sided claims survive: the same data certify a lower bound on both sides of an edge, and we prove $\varphi&gt;1.004$ bits throughout a 64-dimensional region of mechanisms and certify it from about $10^7$ controlled transitions with false-certificate probability at most $α$. Measurability is thus a design question with computable answers.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。