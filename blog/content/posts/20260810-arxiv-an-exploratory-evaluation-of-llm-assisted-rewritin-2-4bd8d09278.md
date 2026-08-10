---
title: "An Exploratory Evaluation of LLM-Assisted Rewriting of Moderate-Complexity Financial Sentences for DisCoCat-Based Sentiment Analysis"
date: 2026-08-10T23:18:51+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Prompt 工程", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:233dce88f5e0d1731a97f71429d1293d684cfe0e60428ee9abb53245652b0c3c"
source_payload_sha256: "sha256:9fe1dd341bdd55cf319971f440f10e46db1e2af1e393587b08a298adfdf36a63"
observation_id: obs_4bd8d09278568231fdab08a0d94a62f27be76ed1c59da8cf8c8a294b28eeb671
event_id: evt_fd03e80d9c894fce2febc12189548f2f7c5fbc5d6a28161cc4663931b63e7421
revision_id: rev_7fb96562f28f695ff633ca12672fb6d1b199e2fddf3f76dbecd6d6ede09bb8de
source_published_at: 2026-08-07T17:23:01Z
first_seen_at: 2026-08-10T17:08:08.063325Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 132
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.07439v1
parent_observation_id: null
last_seen_at: 2026-08-10T15:16:38.814841Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07439v1](http://arxiv.org/abs/2608.07439v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Brian Llinas、Nikos Chrisochoides

## 来源摘要/节选

> Quantum natural language processing (QNLP) provides a grammar-aware framework for text modeling, and Distributional Compositional Categorical (DisCoCat) is one of its theoretically grounded formulations. Prior work on financial sentiment analysis has identified practical limitations of DisCoCat, including parser sensitivity, high simulation cost, and difficulty handling longer sentences. We study an LLM-assisted preprocessing workflow that uses controlled rewriting to compress, simplify, or decompose moderate-complexity financial sentiment sentences into parser-compatible, circuit-efficient variants while preserving sentiment-bearing meaning. We compare prompting strategies, language models, and filtering configurations with the low-complexity-only DisCoCat baseline of Stein et al. At the circuit level, the strongest compression variants reduce average qubit and gate counts by more than 70 percent relative to the raw moderate-complexity subset. Across repeated training runs, GPT-4.1-mini with Prompt B achieves the highest observed mean accuracy, $0.550 \pm 0.035$, compared with $0.521 \pm 0.050$ for the baseline. Larger training splits do not necessarily improve downstream performance; across evaluated configurations, training-split size has a moderately negative association with accuracy (Pearson $r=-0.446$). These results provide exploratory evidence that LLM-assisted rewriting can make some moderate-complexity inputs usable within the evaluated DisCoCat configuration, while highlighting prompt design, filtering, and circuit-aware preprocessing as considerations for more scalable QNLP-based financial sentiment analysis.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。