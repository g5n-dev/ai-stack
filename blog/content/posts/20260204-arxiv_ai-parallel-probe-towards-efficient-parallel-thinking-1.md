---
title: 'Parallel-Probe: Towards Efficient Parallel Thinking via 2D Probing'
date: 2026-02-04 23:12:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.03845v1
aliases:
- /posts/20260205-arxiv_ai-parallel-probe-towards-efficient-parallel-thinking-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:89776e3cec29f9a486f49361b58f860b0ef6f93e6cfef643c8d9b40a0215f4b6
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:10:41.702374Z'
source_capture_sha256: sha256:9fbf93e6a5b9c215442df79fa4207c413d4e2ea6180520a02dc7a95af5fdf3b5
source_capture_chars_original: 1246
source_publication_excerpt_chars: 1246
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.03845v1](<https://arxiv.org/abs/2602.03845v1>)
- **作者**: Tong Zheng, Chengsong Huang, Runpeng Dai, Yun He, Rui Liu, Xin Ni, Huiwen Bao, Kaishen Wang, Hongtu Zhu, Jiaxin Huang, Furong Huang, Heng Huang
- **分类**: cs.CL
- **论文时间**: 2026-02-03T18:59:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.03845v1.pdf](<https://arxiv.org/pdf/2602.03845v1.pdf>)

## 来源摘要/节选

> Parallel thinking has emerged as a promising paradigm for reasoning, yet it imposes significant computational burdens. Existing efficiency methods primarily rely on local, per-trajectory signals and lack principled mechanisms to exploit global dynamics across parallel branches. We introduce 2D probing, an interface that exposes the width-depth dynamics of parallel thinking by periodically eliciting intermediate answers from all branches. Our analysis reveals three key insights: non-monotonic scaling across width-depth allocations, heterogeneous reasoning branch lengths, and early stabilization of global consensus. Guided by these insights, we introduce $\\textbf\{Parallel-Probe\}$, a training-free controller designed to optimize online parallel thinking. Parallel-Probe employs consensus-based early stopping to regulate reasoning depth and deviation-based branch pruning to dynamically adjust width. Extensive experiments across three benchmarks and multiple models demonstrate that Parallel-Probe establishes a superior Pareto frontier for test-time scaling. Compared to standard majority voting, it reduces sequential tokens by up to $\\textbf\{35.8\}$% and total token cost by over $\\textbf\{25.8\}$% while maintaining competitive accuracy.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
