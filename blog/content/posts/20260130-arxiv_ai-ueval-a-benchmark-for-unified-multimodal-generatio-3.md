---
title: 'UEval: A Benchmark for Unified Multimodal Generation'
date: 2026-01-30 23:03:03+08:00
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
external_url: https://arxiv.org/abs/2601.22155v1
aliases:
- /posts/20260131-arxiv_ai-ueval-a-benchmark-for-unified-multimodal-generatio-3/
- /posts/20260201-arxiv_ai-ueval-a-benchmark-for-unified-multimodal-generatio-3/
- /posts/20260202-arxiv_ai-ueval-a-benchmark-for-unified-multimodal-generatio-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:eee2679b7de6fcedeef4ada53a5d83d4296a5e84691cec9a235893923385cec5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
captured_at: '2026-07-18T04:10:00.628947Z'
source_capture_sha256: sha256:5e103ce06092947959202c28a7d7e7859fd8bef5ebf719b7e345bc91aa4def5e
source_capture_chars_original: 1422
source_publication_excerpt_chars: 1422
observation_id: obs_84c2e8a319b93657753aefe6a61c780f76d6d9309e0ccec65154adfa4d99b5d3
revision_id: rev_6b9e81e11604530aad6dcce32edc1488dfc1a0f06ce84e6793de591133ca7571
event_id: evt_b315e661db6a05851c49f15dc2297456ff08e06d308c862028531a24d3cb7dff
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22155v1](<https://arxiv.org/abs/2601.22155v1>)
- **作者**: Bo Li, Yida Yin, Wenhao Chai, Xingyu Fu, Zhuang Liu
- **分类**: cs.CV
- **论文时间**: 2026-01-29T18:59:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22155v1.pdf](<https://arxiv.org/pdf/2601.22155v1.pdf>)

## 来源摘要/节选

> We introduce UEval, a benchmark to evaluate unified models, i.e., models capable of generating both images and text. UEval comprises 1,000 expert-curated questions that require both images and text in the model output, sourced from 8 real-world tasks. Our curated questions cover a wide range of reasoning types, from step-by-step guides to textbook explanations. Evaluating open-ended multimodal generation is non-trivial, as simple LLM-as-a-judge methods can miss the subtleties. Different from previous works that rely on multimodal Large Language Models \(MLLMs\) to rate image quality or text accuracy, we design a rubric-based scoring system in UEval. For each question, reference images and text answers are provided to a MLLM to generate an initial rubric, consisting of multiple evaluation criteria, and human experts then refine and validate these rubrics. In total, UEval contains 10,417 validated rubric criteria, enabling scalable and fine-grained automatic scoring. UEval is challenging for current unified models: GPT-5-Thinking scores only 66.4 out of 100, while the best open-source model reaches merely 49.1. We observe that reasoning models often outperform non-reasoning ones, and transferring reasoning traces from a reasoning model to a non-reasoning model significantly narrows the gap. This suggests that reasoning may be important for tasks requiring complex multimodal understanding and generation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
