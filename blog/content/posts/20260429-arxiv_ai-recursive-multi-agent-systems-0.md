---
title: Recursive Multi-Agent Systems
date: 2026-04-29 23:26:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2604.25917v1
aliases:
- /posts/20260430-arxiv_ai-recursive-multi-agent-systems-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:314baa376bba181c92e5bf79062a880fd32ff4e8db52323f3290fa1b70650324
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:29:27.867360Z'
source_capture_sha256: sha256:71146d0f9aa473c54c2df74ecd84605419d8d8a6d153f98348b771806ea6f915
source_capture_chars_original: 1588
source_publication_excerpt_chars: 1588
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.25917v1](<https://arxiv.org/abs/2604.25917v1>)
- **作者**: Xiyuan Yang, Jiaru Zou, Rui Pan, Ruizhong Qiu, Pan Lu, Shizhe Diao, Jindong Jiang, Hanghang Tong, Tong Zhang, Markus J. Buehler, Jingrui He, James Zou
- **分类**: cs.AI
- **论文时间**: 2026-04-28T17:59:34Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.25917v1.pdf](<https://arxiv.org/pdf/2604.25917v1.pdf>)

## 来源摘要/节选

> Recursive or looped language models have recently emerged as a new scaling axis by iteratively refining the same model computation over latent states to deepen reasoning. We extend such scaling principle from a single model to multi-agent systems, and ask: Can agent collaboration itself be scaled through recursion? To this end, we introduce RecursiveMAS, a recursive multi-agent framework that casts the entire system as a unified latent-space recursive computation. RecursiveMAS connects heterogeneous agents as a collaboration loop through the lightweight RecursiveLink module, enabling in-distribution latent thoughts generation and cross-agent latent state transfer. To optimize our framework, we develop an inner-outer loop learning algorithm for iterative whole-system co-optimization through shared gradient-based credit assignment across recursion rounds. Theoretical analyses of runtime complexity and learning dynamics establish that RecursiveMAS is more efficient than standard text-based MAS and maintains stable gradients during recursive training. Empirically, we instantiate RecursiveMAS under 4 representative agent collaboration patterns and evaluate across 9 benchmarks spanning mathematics, science, medicine, search, and code generation. In comparison with advanced single/multi-agent and recursive computation baselines, RecursiveMAS consistently delivers an average accuracy improvement of 8.3%, together with 1.2$\\times$-2.4$\\times$ end-to-end inference speedup, and 34.6%-75.6% token usage reduction. Code and Data are provided in https://recursivemas.github.io.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
