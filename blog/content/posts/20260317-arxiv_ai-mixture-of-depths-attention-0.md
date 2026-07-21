---
title: Mixture-of-Depths Attention
date: 2026-03-17 20:30:33+08:00
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
external_url: https://arxiv.org/abs/2603.15619v1
aliases:
- /posts/20260318-arxiv_ai-mixture-of-depths-attention-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:219b15e308f02cf1d78b77ae7e04222efe894f3ddeef72165385c54529bdf0b6
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:28:34.236322Z'
source_capture_sha256: sha256:7f51e1c6444b26df1601f4ea511887fa0613f90d588c3227c1cec977e4512d76
source_capture_chars_original: 1191
source_publication_excerpt_chars: 1191
observation_id: obs_2ba359646368cf1f3cadb1f9ee984e3d7110f42955ebbf9acedd81bd53bfb307
revision_id: rev_e51a58a491b3b7884ead114bd0adf9fd0d077d8e81d09dcb6fc73231dcde1cc9
event_id: evt_0aa82f9f1c2925b738c9767feed54b904a30a44b964042c5ae6a39b48afc5384
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-17T06:47:02Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.15619v1](<https://arxiv.org/abs/2603.15619v1>)
- **作者**: Lianghui Zhu, Yuxin Fang, Bencheng Liao, Shijie Wang, Tianheng Cheng, Zilong Huang, Chen Chen, Lai Wei, Yutao Zeng, Ya Wang, Yi Lin, Yu Li, Xinggang Wang
- **分类**: cs.CL
- **论文时间**: 2026-03-16T17:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.15619v1.pdf](<https://arxiv.org/pdf/2603.15619v1.pdf>)

## 来源摘要/节选

> Scaling depth is a key driver for large language models \(LLMs\). Yet, as LLMs become deeper, they often suffer from signal degradation: informative features formed in shallow layers are gradually diluted by repeated residual updates, making them harder to recover in deeper layers. We introduce mixture-of-depths attention \(MoDA\), a mechanism that allows each attention head to attend to sequence KV pairs at the current layer and depth KV pairs from preceding layers. We further describe a hardware-efficient algorithm for MoDA that resolves non-contiguous memory-access patterns, achieving 97.3% of FlashAttention-2's efficiency at a sequence length of 64K. Experiments on 1.5B-parameter models demonstrate that MoDA consistently outperforms strong baselines. Notably, it improves average perplexity by 0.2 across 10 validation benchmarks and increases average performance by 2.11% on 10 downstream tasks, with a negligible 3.7% FLOPs computational overhead. We also find that combining MoDA with post-norm yields better performance than using it with pre-norm. These results suggest that MoDA is a promising primitive for depth scaling. Code is released at https://github.com/hustvl/MoDA .

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
