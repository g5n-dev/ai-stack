---
title: Neuron-Aware Data Selection In Instruction Tuning For Large Language Models
date: 2026-03-16 23:16:09+08:00
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
external_url: https://arxiv.org/abs/2603.13201v1
aliases:
- /posts/20260317-arxiv_ai-neuron-aware-data-selection-in-instruction-tuning--3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:512bc08e2128feda93e7c6c11340ff2bcbd9db49dcc1665efd03a7ca17b33de3
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
captured_at: '2026-07-18T04:28:19.053555Z'
source_capture_sha256: sha256:21d7701d87da70bf0a3b1ecbfd559b1cb37b839e551eb0de07a0de2809a570f5
source_capture_chars_original: 1768
source_publication_excerpt_chars: 1768
observation_id: obs_c3934b7be08db96e136ffbe7a36e3290c2ea2cbefc9591d12d85fa8aa779569d
revision_id: rev_ceab0182533eab55be3e944c30f53c14289293075c07d9096d548ce1205c0092
event_id: evt_4877d433c44c137f6758efdde2f2740f96f9d2dc09604c11d3bb0e6747e01b65
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.13201v1](<https://arxiv.org/abs/2603.13201v1>)
- **作者**: Xin Chen, Junchao Wu, Shu Yang, Runzhe Zhan, Zeyu Wu, Min Yang, Shujian Huang, Lidia S. Chao, Derek F. Wong
- **分类**: cs.CL
- **论文时间**: 2026-03-13T17:39:03Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.13201v1.pdf](<https://arxiv.org/pdf/2603.13201v1.pdf>)

## 来源摘要/节选

> Instruction Tuning \(IT\) has been proven to be an effective approach to unlock the powerful capabilities of large language models \(LLMs\). Recent studies indicate that excessive IT data can degrade LLMs performance, while carefully selecting a small subset of high-quality IT data can significantly enhance their capabilities. Therefore, identifying the most efficient subset data from the IT dataset to effectively develop either specific or general abilities in LLMs has become a critical challenge. To address this, we propose a novel and efficient framework called NAIT. NAIT evaluates the impact of IT data on LLMs performance by analyzing the similarity of neuron activation patterns between the IT dataset and the target domain capability. Specifically, NAIT captures neuron activation patterns from in-domain datasets of target domain capabilities to construct reusable and transferable neuron activation features. It then evaluates and selects optimal samples based on the similarity between candidate samples and the expected activation features of the target capabilities. Experimental results show that training on the 10\\% Alpaca-GPT4 IT data subset selected by NAIT consistently outperforms methods that rely on external advanced models or uncertainty-based features across various tasks. Our findings also reveal the transferability of neuron activation features across different capabilities of LLMs. In particular, IT data with more logical reasoning and programmatic features possesses strong general transferability, enabling models to develop stronger capabilities across multiple tasks, while a stable core subset of data is sufficient to consistently activate fundamental model capabilities and universally improve performance across diverse tasks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
