---
title: 'FOCUS: DLLMs Know How to Tame Their Compute Bound'
date: 2026-02-02 19:22:59+08:00
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
external_url: https://arxiv.org/abs/2601.23278v1
aliases:
- /posts/20260203-arxiv_ai-focus-dllms-know-how-to-tame-their-compute-bound-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d9059cd72ff0d1c40833e98ce4ec1cec39bcb6e8b1cdc05430e80a5395dabae1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
captured_at: '2026-07-18T04:10:04.354932Z'
source_capture_sha256: sha256:1f3035e35cd0afda382b4f390004c316c414bb1393b4149b470ce1f88fb2d601
source_capture_chars_original: 1111
source_publication_excerpt_chars: 1111
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23278v1](<https://arxiv.org/abs/2601.23278v1>)
- **作者**: Kaihua Liang, Xin Tan, An Zhong, Hong Xu, Marco Canini
- **分类**: cs.LG
- **论文时间**: 2026-01-30T18:52:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23278v1.pdf](<https://arxiv.org/pdf/2601.23278v1.pdf>)

## 来源摘要/节选

> Diffusion Large Language Models \(DLLMs\) offer a compelling alternative to Auto-Regressive models, but their deployment is constrained by high decoding cost. In this work, we identify a key inefficiency in DLLM decoding: while computation is parallelized over token blocks, only a small subset of tokens is decodable at each diffusion step, causing most compute to be wasted on non-decodable tokens. We further observe a strong correlation between attention-derived token importance and token-wise decoding probability. Based on this insight, we propose FOCUS -- an inference system designed for DLLMs. By dynamically focusing computation on decodable tokens and evicting non-decodable ones on-the-fly, FOCUS increases the effective batch size, alleviating compute limitations and enabling scalable throughput. Empirical evaluations demonstrate that FOCUS achieves up to 3.52$\\times$ throughput improvement over the production-grade engine LMDeploy, while preserving or improving generation quality across multiple benchmarks. The FOCUS system is publicly available on GitHub: https://github.com/sands-lab/FOCUS.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
