---
title: "How to Verify Consistency of Probabilistic Claims"
date: 2026-08-12T23:15:56+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.CC", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:35510e126116e47c00bc6c3d284fe552ac3e0aad12affc3ce31d632d980669f2"
source_payload_sha256: "sha256:8709efce189c1d702727a7908e6f1ac7b2c83f77be7be5c6aaf56414f9893d25"
observation_id: obs_214ab41720b12a51030035dd1d17628daa9da117ceedee4ac9a89b84aa358a40
event_id: evt_4b54c10d161e2e84b80c3c62b8e083d38e1a845aa01f21810d9148c5c2c9984f
revision_id: rev_d24b2ea92ccd2ce91111ff96ace1eab16bd5015093affa78c68ca4f1549d6d6a
source_published_at: 2026-08-11T17:41:39Z
first_seen_at: 2026-08-12T15:14:24.324442Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
interpretation_sha256: "sha256:6c2c0bf4b03f40c77b6662c19b1d6452de5c92d637e0022b290c45b3bcf179e9"
description: "该文提出一种交互式 PCP 框架，能够在多项式时间内检验由概率电路和置信度电路构成的模型，对其产生的众多条件概率回答是否近似一致，并通过稀疏的见证分布作为证明来辅助验证。"
external_url: http://arxiv.org/abs/2608.11181v1
parent_observation_id: null
last_seen_at: 2026-08-12T15:14:24.324442Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11181v1](http://arxiv.org/abs/2608.11181v1)
- **发布域名**: arxiv.org
- **分类**: cs.CC
- **作者**: Orr Paradise、Oliver Richardson、Yoshua Bengio 等

## 要点解读

### 这是什么  
该文提出一种交互式 PCP 框架，能够在多项式时间内检验由概率电路和置信度电路构成的模型，对其产生的众多条件概率回答是否近似一致，并通过稀疏的见证分布作为证明来辅助验证。

### 用在哪里  
适用于需要对大规模概率预测系统进行可信度审查的场景，尤其是 AI 安全性研究中对模型诚实性进行形式化验证的学者，或在实际部署前想确保预测不会自相矛盾的工程师。

### 可以推断的  
推测：此类验证技术若成熟，可为监管机构提供对概率模型输出的可验证保证手段。  
推测：实现该协议需要构造稀疏的见证分布，可能在资源受限的环境下带来实现难度。

## 来源摘要/节选

> When a probabilistic predictor answers many conditional-probability queries, are its answers self-consistent, and can this be verified in polynomial time? This problem is of interest for AI safety, where safety is derived from honesty about probabilistic predictions of unwanted outcomes potentially caused by an AI action. We construct an interactive PCP as follows. Let a predictive model be specified by a probability circuit P and a circuit Q which outputs confidence in predictions. Together, P and Q implicitly specify exponentially many probabilistic claims. We show a protocol in which a polynomial-time verifier can verify the approximate consistency of (P,Q). The verifier is given the pair of circuits (P,Q), which it evaluates at only a few points; alongside them it is given a proof oracle, an encoding of a witnessing probability distribution allegedly consistent with the predictions of (P,Q), which it reads at a few locations while interacting with a single untrusted prover. En route, we must ensure the existence of a sparse witnessing distribution consistent with the model's predictions. To do so, we first consider witness distributions for the consistency of explicit probabilistic claims, rather than claims specified by a predictor: say m claims, each of the form Pr[Y = 1 | X = x] = p, over n Boolean variables. Building on work initiated by Nilsson (Artif. Intell., 1986), we place l_2-approximate probabilistic consistency of explicit claims in NP, with certificates of length O(mn + log B) in the input bit-precision B; we further show how a small additive completeness-soundness gap removes the dependence on B. Together these results provide a complexity-theoretic foundation for certifying the self-consistency of probabilistic predictors. We view our interactive PCP as a first step toward training predictive models to prove their own consistency.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。