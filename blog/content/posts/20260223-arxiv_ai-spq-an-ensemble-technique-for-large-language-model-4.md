---
title: 'SPQ: An Ensemble Technique for Large Language Model Compression'
date: 2026-02-23 22:40:51+08:00
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
external_url: https://arxiv.org/abs/2602.18420v1
aliases:
- /posts/20260224-arxiv_ai-spq-an-ensemble-technique-for-large-language-model-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6a9082277e9f2187477f5207b152517b129877962f40fc4504e3fd4f6e64b9cb
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:16:23.555947Z'
source_capture_sha256: sha256:d924759e88bfc7e2346ce3c73f8f61b246abbb9a44a8b050661d5e91653b7950
source_capture_chars_original: 1479
source_publication_excerpt_chars: 1479
observation_id: obs_9f50eb45762cdbfa152a482e40f1a650f3eff85d42effd864b5b17903a451b9c
revision_id: rev_3225ffa989cad02de4ae03d0784fe9f64eaac8d53d1f610826a0c1cbcf3ef067
event_id: evt_7ab5e62fd817cbadb6034e93c9bda50ac0cc886efff3a21c0bb301514e898d9c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-23T03:53:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.18420v1](<https://arxiv.org/abs/2602.18420v1>)
- **作者**: Jiamin Yao, Eren Gultepe
- **分类**: cs.CL
- **论文时间**: 2026-02-20T18:44:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.18420v1.pdf](<https://arxiv.org/pdf/2602.18420v1.pdf>)

## 来源摘要/节选

> This study presents an ensemble technique, SPQ \(SVD-Pruning-Quantization\), for large language model \(LLM\) compression that combines variance-retained singular value decomposition \(SVD\), activation-based pruning, and post-training linear quantization. Each component targets a different source of inefficiency: i\) pruning removes redundant neurons in MLP layers, ii\) SVD reduces attention projections into compact low-rank factors, iii\) and 8-bit quantization uniformly compresses all linear layers. At matched compression ratios, SPQ outperforms individual methods \(SVD-only, pruning-only, or quantization-only\) in perplexity, demonstrating the benefit of combining complementary techniques. Applied to LLaMA-2-7B, SPQ achieves up to 75% memory reduction while maintaining or improving perplexity \(e.g., WikiText-2 5.47 to 4.91\) and preserving accuracy on downstream benchmarks such as C4, TruthfulQA, and GSM8K. Compared to strong baselines like GPTQ and SparseGPT, SPQ offers competitive perplexity and accuracy while using less memory \(6.86 GB vs. 7.16 GB for GPTQ\). Moreover, SPQ improves inference throughput over GPTQ, achieving up to a 1.9x speedup, which further enhances its practicality for real-world deployment. The effectiveness of SPQ's robust compression through layer-aware and complementary compression techniques may provide practical deployment of LLMs in memory-constrained environments. Code is available at: https://github.com/JiaminYao/SPQ\_LLM\_Compression/

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
