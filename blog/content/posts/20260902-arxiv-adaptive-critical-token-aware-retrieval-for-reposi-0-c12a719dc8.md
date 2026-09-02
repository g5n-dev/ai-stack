---
title: "Adaptive Critical Token-Aware Retrieval for Repository-Level Code Generation"
date: 2026-09-02T22:32:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f8fbc39d5cf978b03af2645dfd64fbb029eaba560fd3515137d255f861c3a617"
source_payload_sha256: "sha256:d18d292f17e3740e1e4e54daa27826172b3353ab3365978dde73979c53e0834b"
observation_id: obs_c12a719dc8aff2f414c5d7aee4c988012afd954a482bc851c6b8cc4a546ecdb2
event_id: evt_d5d17c86e27842ab4ad09922328e8ac81bd18f73943e383e484c11fef0a119be
revision_id: rev_4c9d1f0798dfdd06a47e8591e56eb1c7ef1781814ba9a9cde3ec98a7351a611d
source_published_at: 2026-09-01T17:59:39Z
first_seen_at: 2026-09-02T14:29:08.202126Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
interpretation_sha256: "sha256:caddc9b073e9a381dd982cfc04762aa8d7afc49117d1a3a846a23955da6c057d"
description: "该研究提出一种在代码生成过程中自适应识别关键 token 并在需要时检索仓库上下文的方法，以提升生成质量。"
external_url: http://arxiv.org/abs/2609.01601v1
parent_observation_id: null
last_seen_at: 2026-09-02T14:29:08.202126Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.01601v1](http://arxiv.org/abs/2609.01601v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Kefeng Duan、Dewu Zheng、Yanlin Wang 等

## 要点解读

### 这是什么
该研究提出一种在代码生成过程中自适应识别关键 token 并在需要时检索仓库上下文的方法，以提升生成质量。

### 用在哪里
适用于需要从大型代码仓库中生成代码的场景，尤其是模型输入长度受限的情况。开发代码补全或自动化编程工具的研究者和工程师会关注此类技术。

### 可以推断的
- 推测：该方法能够在生成时动态决定检索时机，从而减少不必要的检索开销。  
- 推测：通过准确定位关键 token，可降低生成错误在后续代码中的扩散，提高整体功能的正确性。

## 来源摘要/节选

> The repository-level code generation task requires synthesizing code that satisfies task requirements while remaining consistent with the target repository context. Since real-world repositories often exceed the input length limits of LLMs, existing approaches commonly adopt retrieval-augmented generation (RAG) to provide repository-specific context. Despite improving repository-context retrieval, existing methods typically provide context as task-level support, without explicitly identifying the critical tokens that require fine-grained repository context during generation. During the autoregressive generation process of LLMs, errors often concentrate at a small number of decisive positions: once such tokens are generated incorrectly, subsequent code may follow an incorrect semantic path and eventually lead to functional failure. We refer to these positions as "critical tokens". In this paper, we propose ACToR, an adaptive critical token-aware retrieval framework for repository-level code generation. ACToR identifies critical tokens during generation and triggers targeted retrieval on demand to provide repository context at these decisive positions. In addition, we design a position-aware weighting method for dense retrievers to prioritize context that is more informative for generation. We evaluate ACToR on two representative repository-level benchmarks, RepoExec and CoderEval. Experimental results show that ACToR consistently outperforms state-of-the-art methods, achieving relative improvements of 8.4% on RepoExec and 15.4% on CoderEval. Beyond performance gains, we systematically quantify the impact of critical tokens, revealing their central role in major generation failures and highlighting the necessity of targeted retrieval strategies. We provide the code and data at https://github.com/DeepSoftwareAnalytics/ACToR.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。