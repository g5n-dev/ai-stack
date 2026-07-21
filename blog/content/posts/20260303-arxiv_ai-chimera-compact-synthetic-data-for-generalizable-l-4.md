---
title: 'CHIMERA: Compact Synthetic Data for Generalizable LLM Reasoning'
date: 2026-03-03 02:52:12+08:00
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
external_url: https://arxiv.org/abs/2603.00889v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d0ceee91e462ffb38170236024564b6aaa53e65debe5210d0a841819729318a4
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:26:23.368833Z'
source_capture_sha256: sha256:da3a6e6f15db42c6cc0719d841aee8453ec2930d9c4d879f862325347ab962bb
source_capture_chars_original: 1864
source_publication_excerpt_chars: 1864
observation_id: obs_555ef6970b68ed46392256597a1783b1fb2eeb0d70c399c9030604ce058e0911
revision_id: rev_902197f13e8a01357e94b9ac532d2fc2efe438cd516eee47b343a6f78a601edb
event_id: evt_3119fd51a9bd4a48428ff546b1ca666c7760bba6d942c0529496256788f40f1b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.00889v1](<https://arxiv.org/abs/2603.00889v1>)
- **作者**: Xinyu Zhu, Yihao Feng, Yanchao Sun, Xianzhi Du, Pingzhi Li, Olli Saarikivi, Yun Zhu, Yu Meng
- **分类**: cs.CL
- **论文时间**: 2026-03-01T03:23:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.00889v1.pdf](<https://arxiv.org/pdf/2603.00889v1.pdf>)

## 来源摘要/节选

> Large Language Models \(LLMs\) have recently exhibited remarkable reasoning capabilities, largely enabled by supervised fine-tuning \(SFT\)- and reinforcement learning \(RL\)-based post-training on high-quality reasoning data. However, reproducing and extending these capabilities in open and scalable settings is hindered by three fundamental data-centric challenges: \(1\) the cold-start problem, arising from the lack of seed datasets with detailed, long Chain-of-Thought \(CoT\) trajectories needed to initialize reasoning policies; \(2\) limited domain coverage, as most existing open-source reasoning datasets are concentrated in mathematics, with limited coverage of broader scientific disciplines; and \(3\) the annotation bottleneck, where the difficulty of frontier-level reasoning tasks makes reliable human annotation prohibitively expensive or infeasible. To address these challenges, we introduce CHIMERA, a compact synthetic reasoning dataset comprising 9K samples for generalizable cross-domain reasoning. CHIMERA is constructed with three key properties: \(1\) it provides rich, long CoT reasoning trajectories synthesized by state-of-the-art reasoning models; \(2\) it has broad and structured coverage, spanning 8 major scientific disciplines and over 1K fine-grained topics organized via a model-generated hierarchical taxonomy; and \(3\) it employs a fully automated, scalable evaluation pipeline that uses strong reasoning models to cross-validate both problem validity and answer correctness. We use CHIMERA to post-train a 4B Qwen3 model. Despite the dataset's modest size, the resulting model achieves strong performance on a suite of challenging reasoning benchmarks, including GPQA-Diamond, AIME 24/25/26, HMMT 25, and Humanity's Last Exam, approaching or matching the reasoning performance of substantially larger models such as DeepSeek-R1 and Qwen3-235B.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
