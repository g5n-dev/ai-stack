---
title: 'Beyond the Illusion of Consensus: From Surface Heuristics to Knowledge-Grounded
  Evaluation in LLM-as-a-Judge'
date: 2026-03-12 21:14:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.11027v1
aliases:
- /posts/20260313-arxiv_ai-beyond-the-illusion-of-consensus-from-surface-heur-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4f59f83c67809f169096c6358177f77ef0eb9a524d3fadc055750cb4efeefe6d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
captured_at: '2026-07-18T04:27:47.713351Z'
source_capture_sha256: sha256:2e5dc8405c72fa66c84417e678225536a22373374c48ea851a2c5306cb6326c0
source_capture_chars_original: 1669
source_publication_excerpt_chars: 1669
observation_id: obs_418ed6894dff67ae987ba8b462a9b432f70efbe5174067fd8d19b88548f57e20
revision_id: rev_21fd07f1c96110e91a7167235d1ddacdf44c9a0f15c29cf440a21dd36b957f5f
event_id: evt_3ce047b582b18ae036536769713599435745666eec7346a1f98ec8f055d10672
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.11027v1](<https://arxiv.org/abs/2603.11027v1>)
- **作者**: Mingyang Song, Mao Zheng, Chenning Xu
- **分类**: cs.CL
- **论文时间**: 2026-03-11T17:50:38Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.11027v1.pdf](<https://arxiv.org/pdf/2603.11027v1.pdf>)

## 来源摘要/节选

> The paradigm of LLM-as-a-judge relies on a critical assumption, namely that high inter-evaluator agreement indicates reliable and objective evaluation. We present two complementary findings that challenge this assumption. \\textbf\{First\}, we demonstrate that this consensus is frequently illusory. We identify and formalize \\textbf\{Evaluation Illusion\}, a phenomenon where LLM judges generate sophisticated critiques yet anchor scores on shared surface heuristics rather than substantive quality. Through a large-scale study of 105,600 evaluation instances \(32 LLMs $\\times$ 3 frontier judges $\\times$ 100 tasks $\\times$ 11 temperatures\), we show that model-level agreement \(Spearman $ρ= 0.99$\) masks fragile sample-level agreement \(Pearson $\\bar\{r\} = 0.72$; absolute agreement ICC $= 0.67$\), that merely sharing rubric structure restores 62\\% of total agreement, and that high-quality outputs paradoxically receive the \\textit\{least\} consistent evaluations. \\textbf\{Second\}, we demonstrate that dynamically generating evaluation rubrics grounded in domain knowledge produces more meaningful assessment. We introduce MERG \(Metacognitive Enhanced Rubric Generation\), a knowledge-driven rubric generation framework whose domain-selective effects confirm this. Agreement \\textit\{increases\} in codified domains \(Education +22\\%, Academic +27\\%\) where knowledge anchors evaluators on shared standards, while it decreases in subjective domains where genuine evaluative pluralism emerges. These findings suggest that evaluation rubrics should be dynamically enriched with expert knowledge rather than relying on generic criteria, with implications for reward modeling in RLAIF.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
