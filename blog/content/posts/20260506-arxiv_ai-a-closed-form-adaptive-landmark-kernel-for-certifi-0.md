---
title: A Closed-Form Adaptive-Landmark Kernel for Certified Point-Cloud and Graph
  Classification
date: 2026-05-06 22:15:44+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.04046v1
aliases:
- /posts/20260507-arxiv_ai-a-closed-form-adaptive-landmark-kernel-for-certifi-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bb3170e6b0821816183d4ad9120a2ef84115911b6a6dac8949ea5fb8f795a47e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:29:31.582048Z'
source_capture_sha256: sha256:45c42082e74ef5226efbcc07f2c46b120dba247a28589936bea93f2df2e9c4f2
source_capture_chars_original: 1752
source_publication_excerpt_chars: 1752
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.04046v1](<https://arxiv.org/abs/2605.04046v1>)
- **作者**: Sushovan Majhi, Atish Mitra, Žiga Virk, Pramita Bagchi
- **分类**: cs.LG
- **论文时间**: 2026-05-05T17:59:18Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.04046v1.pdf](<https://arxiv.org/pdf/2605.04046v1.pdf>)

## 来源摘要/节选

> We introduce PALACE \(Persistence Adaptive-Landmark Analytic Classification Engine\), the data-adaptive companion to PLACE, paying a small cross-validation tier on three knobs \(budget, radii, bandwidth; $\\leq 5$ choices each\). A cover-theoretic core \(Lebesgue-number criterion on the landmark cover\) yields four closed-form guarantees. \(i\) A structural lower distortion bound $λ\(τ;ν\)$ on $\\mathcal\{D\}\_n$ under cross-diagram non-interference, with a $\(D/L\)^2$ budget reduction over the uniform grid when diagrams concentrate. \(ii\) Equal weights $w\_k = K^\{-1/2\}$ maximizing $λ$, and farthest-point-sampling positions $2$-approximating the optimal $k$-center covering radius; both derived from training labels alone, no gradient training. \(iii\) A kernel-RKHS classification rate $O\(\(k-1\)\\sqrt\{K\}/\(γ\\sqrt\{m\_\{\\min&#125;&#125;\)\)$ with binary necessity threshold $m = Ω\(\\sqrt K/γ\)$ from a matching Le Cam lower bound, and a closed-form filtration-selection rule. The kernel-Mahalanobis margin $\\hatρ\_\{\\mathrm\{Mah&#125;&#125;$ is the strongest closed-form ranker across the chemical-graph pool \(mean Spearman $ρ\\approx +0.60$\); the isotropic surrogate $\\hatγ/\\sqrt\{K\}$ admits a selection-consistency rate, and $\\widehatλ$ from \(i\) provides an independent data-level signal \(positive on COX2 and PTC\). \(iv\) A per-prediction certificate, in non-asymptotic Pinelis and asymptotic Gaussian forms, with no calibration split. Empirically, PALACE is the strongest closed-form diagram-based method on Orbit5k \($91.3 \\pm 1.0\\%$, matching Persformer\), leads every diagram-based competitor on COX2 and MUTAG, and is competitive on DHFR \(within 1 pp of ECP\). At $8\\times$ domain inflation, adaptive placement maintains $94\\%$ while the uniform grid collapses to chance \($25\\%$ on 4-class data\).

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
