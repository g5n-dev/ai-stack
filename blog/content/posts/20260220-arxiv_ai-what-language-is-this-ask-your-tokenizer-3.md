---
title: What Language is This? Ask Your Tokenizer
date: 2026-02-20 22:59:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
- 自然语言处理
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 自然语言处理
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.17655v1
aliases:
- /posts/20260221-arxiv_ai-what-language-is-this-ask-your-tokenizer-3/
- /posts/20260222-arxiv_ai-what-language-is-this-ask-your-tokenizer-3/
- /posts/20260223-arxiv_ai-what-language-is-this-ask-your-tokenizer-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7b63c266612449a0c91f2d804c7aabdc3f67920398fe555048fac08e15cdc46c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:16:19.911759Z'
source_capture_sha256: sha256:a0a11e70c53eeed9ccdfc21dd23a5e02906fb8f3e32c067bdc01e896a31d058c
source_capture_chars_original: 1320
source_publication_excerpt_chars: 1320
observation_id: obs_59984a4dd47361ec11f71f9002229e3f2d52134b5703e8f0493e9b0cbcda6eca
revision_id: rev_fcb21cc748776bd856ee2bc035d218de109d6d2b35744f7abcfb6cf58fd17c12
event_id: evt_b6df79e4ccb75474954337c396ed5d9e01d962a893286065280814eab64ab031
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-20T03:54:51Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.17655v1](<https://arxiv.org/abs/2602.17655v1>)
- **作者**: Clara Meister, Ahmetcan Yavuz, Pietro Lesci, Tiago Pimentel
- **分类**: cs.CL
- **论文时间**: 2026-02-19T18:58:39Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.17655v1.pdf](<https://arxiv.org/pdf/2602.17655v1.pdf>)

## 来源摘要/节选

> Language Identification \(LID\) is an important component of many multilingual natural language processing pipelines, where it facilitates corpus curation, training data analysis, and cross-lingual evaluation of large language models. Despite near-perfect performance on high-resource languages, existing systems remain brittle in low-resource and closely related language settings. We introduce UniLID, a simple and efficient LID method based on the UnigramLM tokenization algorithm, leveraging its probabilistic framing, parameter estimation technique and inference strategy. In short, we learn language-conditional unigram distributions over a shared tokenizer vocabulary but treat segmentation as a language-specific phenomenon. Our formulation is data- and compute-efficient, supports incremental addition of new languages without retraining existing models, and can naturally be integrated into existing language model tokenization pipelines. Empirical evaluations against widely used baselines, including fastText, GlotLID, and CLD3, show that UniLID achieves competitive performance on standard benchmarks, substantially improves sample efficiency in low-resource settings - surpassing 70% accuracy with as few as five labeled samples per language - and delivers large gains on fine-grained dialect identification.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
