---
title: 'POPE: Learning to Reason on Hard Problems via Privileged On-Policy Exploration'
date: 2026-01-27 23:10:51+08:00
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
external_url: https://arxiv.org/abs/2601.18779v1
aliases:
- /posts/20260128-arxiv_ai-pope-learning-to-reason-on-hard-problems-via-privi-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:37d6b57fbd254765b7c0ba425a357fa9f1704fa39f3250e6906a26d53099a880
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:09:18.936370Z'
source_capture_sha256: sha256:16e925829a5908fe36f7e2cfd73476ee9571f9bf06ca889cf48168fb898293bf
source_capture_chars_original: 1642
source_publication_excerpt_chars: 1642
observation_id: obs_bfe403b36ce9fd78dac34339258e163d037acd16233e4cb84e61ff8f7205c90f
revision_id: rev_bbb1738450ce6efcb6907393d4b64801245ba5b2b16318286d0bf87bbe2b342c
event_id: evt_821c139fbf7e52cdd3063f91ace26078d2c42336b44c6e79283bf24960e4df7c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.18779v1](<https://arxiv.org/abs/2601.18779v1>)
- **作者**: Yuxiao Qu, Amrith Setlur, Virginia Smith, Ruslan Salakhutdinov, Aviral Kumar
- **分类**: cs.LG
- **论文时间**: 2026-01-26T18:47:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.18779v1.pdf](<https://arxiv.org/pdf/2601.18779v1.pdf>)

## 来源摘要/节选

> Reinforcement learning \(RL\) has improved the reasoning abilities of large language models \(LLMs\), yet state-of-the-art methods still fail to learn on many training problems. On hard problems, on-policy RL rarely explores even a single correct rollout, yielding zero reward and no learning signal for driving improvement. We find that natural solutions to remedy this exploration problem from classical RL, such as entropy bonuses, more permissive clipping of the importance ratio, or direct optimization of pass@k objectives, do not resolve this issue and often destabilize optimization without improving solvability. A natural alternative is to leverage transfer from easier problems. However, we show that mixing easy and hard problems during RL training is counterproductive due to ray interference, where optimization focuses on already-solvable problems in a way that actively inhibits progress on harder ones. To address this challenge, we introduce Privileged On-Policy Exploration \(POPE\), an approach that leverages human- or other oracle solutions as privileged information to guide exploration on hard problems, unlike methods that use oracle solutions as training targets \(e.g., off-policy RL methods or warmstarting from SFT\). POPE augments hard problems with prefixes of oracle solutions, enabling RL to obtain non-zero rewards during guided rollouts. Crucially, the resulting behaviors transfer back to the original, unguided problems through a synergy between instruction-following and reasoning. Empirically, POPE expands the set of solvable problems and substantially improves performance on challenging reasoning benchmarks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
