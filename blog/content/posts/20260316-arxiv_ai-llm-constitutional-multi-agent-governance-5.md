---
title: LLM Constitutional Multi-Agent Governance
date: 2026-03-16 23:16:09+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.13189v1
aliases:
- /posts/20260317-arxiv_ai-llm-constitutional-multi-agent-governance-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1bfa961d33711a361d76991fc3f1a34e8764d87c71f477c03f7939d4bbfa6f97
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:28:15.328315Z'
source_capture_sha256: sha256:e969b4b974767e664af3bcb879f2ecae10415d747be5d586ab2fabf8ebed6204
source_capture_chars_original: 1859
source_publication_excerpt_chars: 1859
observation_id: obs_39282ec92926ce649ab8054d6c93cc9e0d3d7f89e3e4152f573b856bba8ce525
revision_id: rev_53ae16c93a5bd096c65e21d7151101c1b87a56de32bd277e79710e672bb9fd5d
event_id: evt_2d16295798a6e039c0338e7b9df8585f2685fa4ada8e2859594533097092f5bc
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-16T07:19:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.13189v1](<https://arxiv.org/abs/2603.13189v1>)
- **作者**: J. de Curtò, I. de Zarzà
- **分类**: cs.MA
- **论文时间**: 2026-03-13T17:21:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.13189v1.pdf](<https://arxiv.org/pdf/2603.13189v1.pdf>)

## 来源摘要/节选

> Large Language Models \(LLMs\) can generate persuasive influence strategies that shift cooperative behavior in multi-agent populations, but a critical question remains: does the resulting cooperation reflect genuine prosocial alignment, or does it mask erosion of agent autonomy, epistemic integrity, and distributional fairness? We introduce Constitutional Multi-Agent Governance \(CMAG\), a two-stage framework that interposes between an LLM policy compiler and a networked agent population, combining hard constraint filtering with soft penalized-utility optimization that balances cooperation potential against manipulation risk and autonomy pressure. We propose the Ethical Cooperation Score \(ECS\), a multiplicative composite of cooperation, autonomy, integrity, and fairness that penalizes cooperation achieved through manipulative means. In experiments on scale-free networks of 80 agents under adversarial conditions \(70% violating candidates\), we benchmark three regimes: full CMAG, naive filtering, and unconstrained optimization. While unconstrained optimization achieves the highest raw cooperation \(0.873\), it yields the lowest ECS \(0.645\) due to severe autonomy erosion \(0.867\) and fairness degradation \(0.888\). CMAG attains an ECS of 0.741, a 14.9% improvement, while preserving autonomy at 0.985 and integrity at 0.995, with only modest cooperation reduction to 0.770. The naive ablation \(ECS = 0.733\) confirms that hard constraints alone are insufficient. Pareto analysis shows CMAG dominates the cooperation-autonomy trade-off space, and governance reduces hub-periphery exposure disparities by over 60%. These findings establish that cooperation is not inherently desirable without governance: constitutional constraints are necessary to ensure that LLM-mediated influence produces ethically stable outcomes rather than manipulative equilibria.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
