---
title: 'RLAnything: Forge Environment, Policy, and Reward Model in Completely Dynamic
  RL System'
date: 2026-02-03 23:08:59+08:00
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
external_url: https://arxiv.org/abs/2602.02488v1
aliases:
- /posts/20260204-arxiv_ai-rlanything-forge-environment-policy-and-reward-mod-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e81c8081f791a22dcd477e6d0dce0c2dcc9389301ce0d94681a3e90ebb6e48f2
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:10:41.702374Z'
source_capture_sha256: sha256:e204926c9ba757629b55d909558707ac6861af53b26986bca76ab667e5196005
source_capture_chars_original: 1108
source_publication_excerpt_chars: 1108
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02488v1](<https://arxiv.org/abs/2602.02488v1>)
- **作者**: Yinjie Wang, Tianbao Xie, Ke Shen, Mengdi Wang, Ling Yang
- **分类**: cs.LG
- **论文时间**: 2026-02-02T18:59:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02488v1.pdf](<https://arxiv.org/pdf/2602.02488v1.pdf>)

## 来源摘要/节选

> We propose RLAnything, a reinforcement learning framework that dynamically forges environment, policy, and reward models through closed-loop optimization, amplifying learning signals and strengthening the overall RL system for any LLM or agentic scenarios. Specifically, the policy is trained with integrated feedback from step-wise and outcome signals, while the reward model is jointly optimized via consistency feedback, which in turn further improves policy training. Moreover, our theory-motivated automatic environment adaptation improves training for both the reward and policy models by leveraging critic feedback from each, enabling learning from experience. Empirically, each added component consistently improves the overall system, and RLAnything yields substantial gains across various representative LLM and agentic tasks, boosting Qwen3-VL-8B-Thinking by 9.1% on OSWorld and Qwen2.5-7B-Instruct by 18.7% and 11.9% on AlfWorld and LiveBench, respectively. We also that optimized reward-model signals outperform outcomes that rely on human labels. Code: https://github.com/Gen-Verse/Open-AgentRL

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
