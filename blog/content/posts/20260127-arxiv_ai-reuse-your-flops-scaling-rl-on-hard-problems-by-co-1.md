---
title: 'Reuse your FLOPs: Scaling RL on Hard Problems by Conditioning on Very Off-Policy
  Prefixes'
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
external_url: https://arxiv.org/abs/2601.18795v1
aliases:
- /posts/20260128-arxiv_ai-reuse-your-flops-scaling-rl-on-hard-problems-by-co-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:76e07cb3d0b9c4dcfbeb259743748fd9b24c12f12c32459a71c39c68c62795be
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:09:18.936370Z'
source_capture_sha256: sha256:904bcce8c4c4f7bd02d5aa26acb5ad2a3676194fa22e22e4bbba358265430bad
source_capture_chars_original: 1642
source_publication_excerpt_chars: 1642
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.18795v1](<https://arxiv.org/abs/2601.18795v1>)
- **作者**: Amrith Setlur, Zijian Wang, Andrew Cohen, Paria Rashidinejad, Sang Michael Xie
- **分类**: cs.LG
- **论文时间**: 2026-01-26T18:57:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.18795v1.pdf](<https://arxiv.org/pdf/2601.18795v1.pdf>)

## 来源摘要/节选

> Typical reinforcement learning \(RL\) methods for LLM reasoning waste compute on hard problems, where correct on-policy traces are rare, policy gradients vanish, and learning stalls. To bootstrap more efficient RL, we consider reusing old sampling FLOPs \(from prior inference or RL training\) in the form of off-policy traces. Standard off-policy methods supervise against off-policy data, causing instabilities during RL optimization. We introduce PrefixRL, where we condition on the prefix of successful off-policy traces and run on-policy RL to complete them, side-stepping off-policy instabilities. PrefixRL boosts the learning signal on hard problems by modulating the difficulty of the problem through the off-policy prefix length. We prove that the PrefixRL objective is not only consistent with the standard RL objective but also more sample efficient. Empirically, we discover back-generalization: training only on prefixed problems generalizes to out-of-distribution unprefixed performance, with learned strategies often differing from those in the prefix. In our experiments, we source the off-policy traces by rejection sampling with the base model, creating a self-improvement loop. On hard reasoning problems, PrefixRL reaches the same training reward 2x faster than the strongest baseline \(SFT on off-policy data then RL\), even after accounting for the compute spent on the initial rejection sampling, and increases the final reward by 3x. The gains transfer to held-out benchmarks, and PrefixRL is still effective when off-policy traces are derived from a different model family, validating its flexibility in practical settings.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
