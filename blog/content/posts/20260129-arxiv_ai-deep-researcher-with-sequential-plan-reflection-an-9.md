---
title: Deep Researcher with Sequential Plan Reflection and Candidates Crossover (Deep
  Researcher Reflect Evolve)
date: 2026-01-29 22:59:16+08:00
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
external_url: https://arxiv.org/abs/2601.20843v1
aliases:
- /posts/20260130-arxiv_ai-deep-researcher-with-sequential-plan-reflection-an-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bfacb219f34ff385dd4402ce37fd4994a694b1c1f5a2b7bac74e21226b9a9694
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 105
captured_at: '2026-07-18T04:09:30.311520Z'
source_capture_sha256: sha256:3a748a097cac4ead1a02dc36d1a1a71d68e49e9371168a73c485414ccef459a9
source_capture_chars_original: 1757
source_publication_excerpt_chars: 1757
observation_id: obs_fd3e515733e688329d9f422d21b67b4e1e6961568074cb39ffcbebe58515cbf6
revision_id: rev_fb2ddf455f00fa5561bc62b8dc9e108643ca1ac1953ec689d9e2766a4c97ee1b
event_id: evt_b9f197edb927cb7647a919be2e8cd537d7685837991c8ac8576b3d46cba8dcb7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.20843v1](<https://arxiv.org/abs/2601.20843v1>)
- **作者**: Saurav Prateek
- **分类**: cs.AI
- **论文时间**: 2026-01-28T18:45:39Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.20843v1.pdf](<https://arxiv.org/pdf/2601.20843v1.pdf>)

## 来源摘要/节选

> This paper introduces a novel Deep Researcher architecture designed to generate detailed research reports on complex PhD level topics by addressing the inherent limitations of the Parallel Scaling paradigm. Our system utilizes two key innovations: Sequential Research Plan Refinement via Reflection and a Candidates Crossover algorithm. The sequential refinement process is demonstrated as an efficient method that allows the agent to maintain a centralized Global Research Context, enabling it to look back at current progress, reason about the research plan, and intelligently make changes at runtime. This dynamic adaptation contrasts with parallel approaches, which often suffer from siloed knowledge. The Candidates Crossover algorithm further enhances search efficiency by deploying multiple LLM candidates with varied parameters to explore a larger search space, with their findings synthesized to curate a comprehensive final research response. The process concludes with One Shot Report Generation, ensuring the final document is informed by a unified narrative and high fact density. Powered by the Gemini 2.5 Pro model, our Deep Researcher was evaluated on the DeepResearch Bench, a globally recognized benchmark of 100 doctoral level research tasks. Our architecture achieved an overall score of 46.21, demonstrating superior performance by surpassing leading deep research agents such as Claude Researcher, Nvidia AIQ Research Assistant, Perplexity Research, Kimi Researcher and Grok Deeper Search present on the DeepResearch Bench actively running leaderboard. This performance marginally exceeds our previous work, Static DRA, and reinforces the finding that sequential scaling consistently outperforms the parallel self consistency paradigm.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
