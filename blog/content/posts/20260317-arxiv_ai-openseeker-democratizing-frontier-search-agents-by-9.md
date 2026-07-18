---
title: 'OpenSeeker: Democratizing Frontier Search Agents by Fully Open-Sourcing Training
  Data'
date: 2026-03-17 20:30:33+08:00
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
external_url: https://arxiv.org/abs/2603.15594v1
aliases:
- /posts/20260318-arxiv_ai-openseeker-democratizing-frontier-search-agents-by-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b3acce606044bbd2f7fc9a670ce7161a31efc25a067133eabcb8ccf71872b642
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:28:34.236322Z'
source_capture_sha256: sha256:a99d2d765ffa6f14f8befd61a401b1188fff21de6245348a1073f5b2b9c5165d
source_capture_chars_original: 1780
source_publication_excerpt_chars: 1780
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.15594v1](<https://arxiv.org/abs/2603.15594v1>)
- **作者**: Yuwen Du, Rui Ye, Shuo Tang, Xinyu Zhu, Yijun Lu, Yuzhu Cai, Siheng Chen
- **分类**: cs.AI
- **论文时间**: 2026-03-16T17:52:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.15594v1.pdf](<https://arxiv.org/pdf/2603.15594v1.pdf>)

## 来源摘要/节选

> Deep search capabilities have become an indispensable competency for frontier Large Language Model \(LLM\) agents, yet the development of high-performance search agents remains dominated by industrial giants due to a lack of transparent, high-quality training data. This persistent data scarcity has fundamentally hindered the progress of the broader research community in developing and innovating within this domain. To bridge this gap, we introduce OpenSeeker, the first fully open-source search agent \(i.e., model and data\) that achieves frontier-level performance through two core technical innovations: \(1\) Fact-grounded scalable controllable QA synthesis, which reverse-engineers the web graph via topological expansion and entity obfuscation to generate complex, multi-hop reasoning tasks with controllable coverage and complexity. \(2\) Denoised trajectory synthesis, which employs a retrospective summarization mechanism to denoise the trajectory, therefore promoting the teacher LLMs to generate high-quality actions. Experimental results demonstrate that OpenSeeker, trained \(a single training run\) on only 11.7k synthesized samples, achieves state-of-the-art performance across multiple benchmarks including BrowseComp, BrowseComp-ZH, xbench-DeepSearch, and WideSearch. Notably, trained with simple SFT, OpenSeeker significantly outperforms the second-best fully open-source agent DeepDive \(e.g., 29.5% v.s. 15.3% on BrowseComp\), and even surpasses industrial competitors such as Tongyi DeepResearch \(trained via extensive continual pre-training, SFT, and RL\) on BrowseComp-ZH \(48.4% v.s. 46.7%\). We fully open-source the complete training dataset and the model weights to democratize frontier search agent research and foster a more transparent, collaborative ecosystem.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
