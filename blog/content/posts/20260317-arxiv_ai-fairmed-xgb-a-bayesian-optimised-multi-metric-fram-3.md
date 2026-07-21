---
title: 'FairMed-XGB: A Bayesian-Optimised Multi-Metric Framework with Explainability
  for Demographic Equity in Critical Healthcare Data'
date: 2026-03-17 03:25:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.14947v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e651da8585569f4d444cd558ed9c8a30a8f52fc7fb3ebd3f61c65ef7742e951e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 127
captured_at: '2026-07-18T04:28:30.264258Z'
source_capture_sha256: sha256:88752db0c49451868b48e70a7317b50da4e7a90bf887bf9071aa864f86dd590c
source_capture_chars_original: 1427
source_publication_excerpt_chars: 1427
observation_id: obs_fe11ecf12877e291d66aaca00f9228816f1d0c79f62d9f2d2d66934887ab505f
revision_id: rev_078bbb4d28d61f1bbc3db1c78c57cecf0b5108f4b6fcfc8744f83b2f689983d3
event_id: evt_09b84f10f1afb40eec5b2d7c69f48048a3018ceb44c7c407a2367f140c58acd7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.14947v1](<https://arxiv.org/abs/2603.14947v1>)
- **作者**: Mitul Goswami, Romit Chatterjee, Arif Ahmed Sekh
- **分类**: cs.LG
- **论文时间**: 2026-03-16T07:57:40Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.14947v1.pdf](<https://arxiv.org/pdf/2603.14947v1.pdf>)

## 来源摘要/节选

> Machine learning models deployed in critical care settings exhibit demographic biases, particularly gender disparities, that undermine clinical trust and equitable treatment. This paper introduces FairMed-XGB, a novel framework that systematically detects and mitigates gender-based prediction bias while preserving model performance and transparency. The framework integrates a fairness-aware loss function combining Statistical Parity Difference, Theil Index, and Wasserstein Distance, jointly optimised via Bayesian Search into an XGBoost classifier. Post-mitigation evaluation on seven clinically distinct cohorts derived from the MIMIC-IV-ED and eICU databases demonstrates substantial bias reduction: Statistical Parity Difference decreases by 40 to 51 percent on MIMIC-IV-ED and 10 to 19 percent on eICU; Theil Index collapses by four to five orders of magnitude to near-zero values; Wasserstein Distance is reduced by 20 to 72 percent. These gains are achieved with negligible degradation in predictive accuracy \(AUC-ROC drop &lt;0.02\). SHAP-based explainability reveals that the framework diminishes reliance on gender-proxy features, providing clinicians with actionable insights into how and where bias is corrected. FairMed-XGB offers a robust, interpretable, and ethically aligned solution for equitable clinical decision-making, paving the way for trustworthy deployment of AI in high-stakes healthcare environments.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
