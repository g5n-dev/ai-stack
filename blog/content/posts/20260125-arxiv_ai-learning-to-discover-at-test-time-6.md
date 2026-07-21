---
title: Learning to Discover at Test Time
date: 2026-01-25 12:39:55+08:00
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
external_url: https://arxiv.org/abs/2601.16175v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b164262ea826304d2798936403a2de8ed87bd1b43c4f2853868b4f1a2412aafc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 33
captured_at: '2026-07-18T04:08:52.620209Z'
source_capture_sha256: sha256:e6e76138c5440818c324a1e3595184b85ef4fccb49625cd35c928e0c842227e0
source_capture_chars_original: 1600
source_publication_excerpt_chars: 1600
observation_id: obs_8414abf811c5d584d7f4af282dfeb87eec1e92b7486ab4e6c804d577c43a6b15
revision_id: rev_9a1ee6bb7ba974ee5491d1ee78ff385dc8c654a18b2007a5b5327a45216d7f00
event_id: evt_d1f8d09dda13b470aba804708c00a7c72fd923c008c4179af4b4ff1e7a071f6c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-25T12:41:54Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16175v1](<https://arxiv.org/abs/2601.16175v1>)
- **作者**: Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan Kautz, Yejin Choi, James Zou, Carlos Guestrin, Yu Sun
- **分类**: cs.LG
- **论文时间**: 2026-01-22T18:24:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16175v1.pdf](<https://arxiv.org/pdf/2601.16175v1.pdf>)

## 来源摘要/节选

> How can we use AI to discover a new state of the art for a scientific problem? Prior work in test-time scaling, such as AlphaEvolve, performs search by prompting a frozen LLM. We perform reinforcement learning at test time, so the LLM can continue to train, but now with experience specific to the test problem. This form of continual learning is quite special, because its goal is to produce one great solution rather than many good ones on average, and to solve this very problem rather than generalize to other problems. Therefore, our learning objective and search subroutine are designed to prioritize the most promising solutions. We call this method Test-Time Training to Discover \(TTT-Discover\). Following prior work, we focus on problems with continuous rewards. We report results for every problem we attempted, across mathematics, GPU kernel engineering, algorithm design, and biology. TTT-Discover sets the new state of the art in almost all of them: \(i\) Erdős' minimum overlap problem and an autocorrelation inequality; \(ii\) a GPUMode kernel competition \(up to $2\\times$ faster than prior art\); \(iii\) past AtCoder algorithm competitions; and \(iv\) denoising problem in single-cell analysis. Our solutions are reviewed by experts or the organizers. All our results are achieved with an open model, OpenAI gpt-oss-120b, and can be reproduced with our publicly available code, in contrast to previous best results that required closed frontier models. Our test-time training runs are performed using Tinker, an API by Thinking Machines, with a cost of only a few hundred dollars per problem.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
