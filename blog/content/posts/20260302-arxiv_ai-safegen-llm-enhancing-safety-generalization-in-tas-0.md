---
title: 'SafeGen-LLM: Enhancing Safety Generalization in Task Planning for Robotic
  Systems'
date: 2026-03-02 02:56:17+08:00
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
external_url: https://arxiv.org/abs/2602.24235v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:aaf23797db7dc2334f440f6b45868ec35ec43b22b3032c0bee55ef16cf23acd0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
captured_at: '2026-07-18T04:26:12.126510Z'
source_capture_sha256: sha256:a992f88fd8dd6b34b25325ecc138a634697f97bf1c544e3d977f9176ceb16621
source_capture_chars_original: 1204
source_publication_excerpt_chars: 1204
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24235v1](<https://arxiv.org/abs/2602.24235v1>)
- **作者**: Jialiang Fan, Weizhe Xu, Mengyu Liu, Oleg Sokolsky, Insup Lee, Fanxin Kong
- **分类**: cs.RO
- **论文时间**: 2026-02-27T18:06:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24235v1.pdf](<https://arxiv.org/pdf/2602.24235v1.pdf>)

## 来源摘要/节选

> Safety-critical task planning in robotic systems remains challenging: classical planners suffer from poor scalability, Reinforcement Learning \(RL\)-based methods generalize poorly, and base Large Language Models \(LLMs\) cannot guarantee safety. To address this gap, we propose safety-generalizable large language models, named SafeGen-LLM. SafeGen-LLM can not only enhance the safety satisfaction of task plans but also generalize well to novel safety properties in various domains. We first construct a multi-domain Planning Domain Definition Language 3 \(PDDL3\) benchmark with explicit safety constraints. Then, we introduce a two-stage post-training framework: Supervised Fine-Tuning \(SFT\) on a constraint-compliant planning dataset to learn planning syntax and semantics, and Group Relative Policy Optimization \(GRPO\) guided by fine-grained reward machines derived from formal verification to enforce safety alignment and by curriculum learning to better handle complex tasks. Extensive experiments show that SafeGen-LLM achieves strong safety generalization and outperforms frontier proprietary baselines across multi-domain planning tasks and multiple input formats \(e.g., PDDLs and natural language\).

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
