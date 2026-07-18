---
title: 'Curvature-Weighted Capacity Allocation: A Minimum Description Length Framework
  for Layer-Adaptive Large Language Model Optimization'
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
external_url: https://arxiv.org/abs/2603.00910v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f55794a0162bdcb19eb6bfc6d8d73f32258bc75d2bffe3bb75e8795c4f212f09
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 131
captured_at: '2026-07-18T04:26:23.368833Z'
source_capture_sha256: sha256:1c52234ab81a6f27c200a9749a49c43245aab89f5d61bc3cefd5ac0ceeda1ad0
source_capture_chars_original: 1793
source_publication_excerpt_chars: 1793
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.00910v1](<https://arxiv.org/abs/2603.00910v1>)
- **作者**: Theophilus Amaefuna, Hitesh Vaidya, Anshuman Chhabra, Ankur Mali
- **分类**: cs.IT
- **论文时间**: 2026-03-01T04:14:15Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.00910v1.pdf](<https://arxiv.org/pdf/2603.00910v1.pdf>)

## 来源摘要/节选

> Layer-wise capacity in large language models is highly non-uniform: some layers contribute disproportionately to loss reduction while others are near-redundant. Existing methods for exploiting this non-uniformity, such as influence-function-based layer scoring, produce sensitivity estimates but offer no principled mechanism for translating them into allocation or pruning decisions under hardware constraints. We address this gap with a unified, curvature-aware framework grounded in the Minimum Description Length \(MDL\) principle. Our central quantity is the curvature-adjusted layer gain $ζ\_k^2 = g\_k^\\top \\widetilde\{H\}\_\{kk\}^\{-1\} g\_k$, which we show equals twice the maximal second-order reduction in empirical risk achievable by updating layer $k$ alone, and which strictly dominates gradient-norm-based scores by incorporating local curvature. Normalizing these gains into layer quality scores $q\_k$, we formulate two convex MDL programs: a capacity allocation program that distributes expert slots or LoRA rank preferentially to high-curvature layers under diminishing returns, and a pruning program that concentrates sparsity on low-gain layers while protecting high-gain layers from degradation. Both programs admit unique closed-form solutions parameterized by a single dual variable, computable in $O\(K \\log 1/\\varepsilon\)$ via bisection. We prove an $O\(δ^2\)$ transfer regret bound showing that source-domain allocations remain near-optimal on target tasks when curvature scores drift by $δ$, with explicit constants tied to the condition number of the target program. Together, these results elevate layer-wise capacity optimization from an empirical heuristic to a theoretically grounded, computationally efficient framework with provable optimality and generalization guarantees.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
