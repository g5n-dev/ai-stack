---
title: 'Robustness Is a Function, Not a Number: A Factorized Comprehensive Study of
  OOD Robustness in Vision-Based Driving'
date: 2026-02-10 22:46:04+08:00
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
external_url: https://arxiv.org/abs/2602.09018v1
aliases:
- /posts/20260211-arxiv_ai-robustness-is-a-function-not-a-number-a-factorized-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7bd1da39c766c7aa3ddc93a7d97fae27a711d03d1cc3da7d055db7ca226598a6
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 114
captured_at: '2026-07-18T04:14:36.051132Z'
source_capture_sha256: sha256:56b4096f96c3798a905d5e1b189ed7af3cde3b7b59d5dc5fcc0ef31f8d2d60d1
source_capture_chars_original: 1916
source_publication_excerpt_chars: 1916
observation_id: obs_8fd7f783b41d81859e30f8762c09322d7a55bd884708d4f96d472f2505fd1836
revision_id: rev_bbe166a595b83d0490680ca3b3c6a400274a3b0b110bc7c93a5169ad65177dd1
event_id: evt_272c422c007789f03a8a0aa64345e8f2eedc4da6aceb38be87c54e3e8fec5146
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09018v1](<https://arxiv.org/abs/2602.09018v1>)
- **作者**: Amir Mallak, Alaa Maalouf
- **分类**: cs.RO
- **论文时间**: 2026-02-09T18:59:03Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09018v1.pdf](<https://arxiv.org/pdf/2602.09018v1.pdf>)

## 来源摘要/节选

> Out of distribution \(OOD\) robustness in autonomous driving is often reduced to a single number, hiding what breaks a policy. We decompose environments along five axes: scene \(rural/urban\), season, weather, time \(day/night\), and agent mix; and measure performance under controlled $k$-factor perturbations \($k \\in \\\{0,1,2,3\\\}$\). Using closed loop control in VISTA, we benchmark FC, CNN, and ViT policies, train compact ViT heads on frozen foundation-model \(FM\) features, and vary ID support in scale, diversity, and temporal context. \(1\) ViT policies are markedly more OOD-robust than comparably sized CNN/FC, and FM features yield state-of-the-art success at a latency cost. \(2\) Naive temporal inputs \(multi-frame\) do not beat the best single-frame baseline. \(3\) The largest single factor drops are rural $\\rightarrow$ urban and day $\\rightarrow$ night \($\\sim 31\\%$ each\); actor swaps $\\sim 10\\%$, moderate rain $\\sim 7\\%$; season shifts can be drastic, and combining a time flip with other changes further degrades performance. \(4\) FM-feature policies stay above $85\\%$ under three simultaneous changes; non-FM single-frame policies take a large first-shift hit, and all no-FM models fall below $50\\%$ by three changes. \(5\) Interactions are non-additive: some pairings partially offset, whereas season-time combinations are especially harmful. \(6\) Training on winter/snow is most robust to single-factor shifts, while a rural+summer baseline gives the best overall OOD performance. \(7\) Scaling traces/views improves robustness \($+11.8$ points from $5$ to $14$ traces\), yet targeted exposure to hard conditions can substitute for scale. \(8\) Using multiple ID environments broadens coverage and strengthens weak cases \(urban OOD $60.6\\% \\rightarrow 70.1\\%$\) with a small ID drop; single-ID preserves peak performance but in a narrow domain. These results yield actionable design rules for OOD-robust driving policies.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
