---
title: 'UPA: Unsupervised Prompt Agent via Tree-Based Search and Selection'
date: 2026-02-02 19:22:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.23273v1
aliases:
- /posts/20260203-arxiv_ai-upa-unsupervised-prompt-agent-via-tree-based-searc-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4b3cf54d663ac90c8b7e9548f1dec15a31babd6845c65f9163668e89a395e052
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:10:19.257843Z'
source_capture_sha256: sha256:1f949f2af0d451c452db9b888507f88d95178476f714828334e8ceaae4ff7c84
source_capture_chars_original: 1421
source_publication_excerpt_chars: 1421
observation_id: obs_51ec4b21267bc6c35bb92f3e7cfa1f4f0695acbed75168f66f7343ada874d7ac
revision_id: rev_4d66ceff855286948ea956ce4228274a49e2c708af6c839d3f33b1497780bef5
event_id: evt_86d27c3d30ab0e63c20105284e04ec8f6404c153bb565d159e07cdf17f804231
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23273v1](<https://arxiv.org/abs/2601.23273v1>)
- **作者**: Siran Peng, Weisong Zhao, Tianyu Fu, Chenxu Zhao, Tianshuo Zhang, Haoyuan Zhang, Xiangyu Zhu, Minghui Wu, Zhen Lei
- **分类**: cs.CL
- **论文时间**: 2026-01-30T18:39:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23273v1.pdf](<https://arxiv.org/pdf/2601.23273v1.pdf>)

## 来源摘要/节选

> Prompt agents have recently emerged as a promising paradigm for automated prompt optimization, framing refinement as a sequential decision-making problem over a structured prompt space. While this formulation enables the use of advanced planning algorithms, these methods typically assume access to supervised reward signals, which are often unavailable in practical scenarios. In this work, we propose UPA, an Unsupervised Prompt Agent that realizes structured search and selection without relying on supervised feedback. Specifically, during search, UPA iteratively constructs an evolving tree structure to navigate the prompt space, guided by fine-grained and order-invariant pairwise comparisons from Large Language Models \(LLMs\). Crucially, as these local comparisons do not inherently yield a consistent global scale, we decouple systematic prompt exploration from final selection, introducing a two-stage framework grounded in the Bradley-Terry-Luce \(BTL\) model. This framework first performs path-wise Bayesian aggregation of local comparisons to filter candidates under uncertainty, followed by global tournament-style comparisons to infer latent prompt quality and identify the optimal prompt. Experiments across multiple tasks demonstrate that UPA consistently outperforms existing prompt optimization methods, showing that agent-style optimization remains highly effective even in fully unsupervised settings.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
