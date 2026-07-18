---
title: 'KVSlimmer: Theoretical Insights and Practical Optimizations for Asymmetric
  KV Merging'
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
external_url: https://arxiv.org/abs/2603.00907v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4a0ad49cfd8fb3a2b1b1f1d2d92b94e28b87ba4b1117907788bdf7046ae89ad9
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:26:23.368833Z'
source_capture_sha256: sha256:c8947605bd227d7c01abfbc9a84a51f14a52ab7e90c5dd97727001d2b3fc951c
source_capture_chars_original: 1274
source_publication_excerpt_chars: 1274
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.00907v1](<https://arxiv.org/abs/2603.00907v1>)
- **作者**: Lianjun Liu, Hongli An, Weiqi Yan, Xin Du, Shengchuan Zhang, Huazhong Liu, Yunshan Zhong
- **分类**: cs.CL
- **论文时间**: 2026-03-01T04:07:36Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.00907v1.pdf](<https://arxiv.org/pdf/2603.00907v1.pdf>)

## 来源摘要/节选

> The growing computational and memory demands of the Key-Value \(KV\) cache significantly limit the ability of Large Language Models \(LLMs\). While KV merging has emerged as a promising solution, existing methods that rely on empirical observations of KV asymmetry and gradient-based Hessian approximations lack a theoretical foundation and incur suboptimal compression and inference overhead. To bridge these gaps, we establish a theoretical framework that characterizes this asymmetry through the spectral energy distribution of projection weights, demonstrating that concentrated spectra in Query/Key weights induce feature homogeneity, whereas dispersed spectra in Value weights preserve heterogeneity. Then, we introduce KVSlimmer, an efficient algorithm that captures exact Hessian information through a mathematically exact formulation, and derives a closed-form solution utilizing only forward-pass variables, resulting in a gradient-free approach that is both memory- and time-efficient. Extensive experiments across various models and benchmarks demonstrate that KVSlimmer consistently outperforms SOTA methods. For instance, on Llama3.1-8B-Instruct, it improves the LongBench average score by 0.92 while reducing memory costs and latency by 29% and 28%, respectively.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
