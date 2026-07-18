---
title: 'CM2: Reinforcement Learning with Checklist Rewards for Multi-Turn and Multi-Step
  Agentic Tool Use'
date: 2026-02-13 23:30:43+08:00
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
external_url: https://arxiv.org/abs/2602.12268v1
aliases:
- /posts/20260214-arxiv_ai-cm2-reinforcement-learning-with-checklist-rewards--9/
- /posts/20260215-arxiv_ai-cm2-reinforcement-learning-with-checklist-rewards--9/
- /posts/20260216-arxiv_ai-cm2-reinforcement-learning-with-checklist-rewards--9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:cec62d60e4a5f4307030019690e96b8f23ac9ef6c8e199735ce907d7ce4c776b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 97
captured_at: '2026-07-18T04:15:06.314161Z'
source_capture_sha256: sha256:a2c7166f28c87f1d857162a3b734bb05152338f60a802efdb98506376f545d35
source_capture_chars_original: 1647
source_publication_excerpt_chars: 1647
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12268v1](<https://arxiv.org/abs/2602.12268v1>)
- **作者**: Zhen Zhang, Kaiqiang Song, Xun Wang, Yebowen Hu, Weixiang Yan, Chenyang Zhao, Henry Peng Zou, Haoyun Deng, Sathish Reddy Indurthi, Shujian Liu, Simin Ma, Xiaoyang Wang, Xin Eric Wang, Song Wang
- **分类**: cs.AI
- **论文时间**: 2026-02-12T18:55:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12268v1.pdf](<https://arxiv.org/pdf/2602.12268v1.pdf>)

## 来源摘要/节选

> AI agents are increasingly used to solve real-world tasks by reasoning over multi-turn user interactions and invoking external tools. However, applying reinforcement learning to such settings remains difficult: realistic objectives often lack verifiable rewards and instead emphasize open-ended behaviors; moreover, RL for multi-turn, multi-step agentic tool use is still underexplored; and building and maintaining executable tool environments is costly, limiting scale and coverage. We propose CM2, an RL framework that replaces verifiable outcome rewards with checklist rewards. CM2 decomposes each turn's intended behavior into fine-grained binary criteria with explicit evidence grounding and structured metadata, turning open-ended judging into more stable classification-style decisions. To balance stability and informativeness, our method adopts a strategy of sparse reward assignment but dense evaluation criteria. Training is performed in a scalable LLM-simulated tool environment, avoiding heavy engineering for large tool sets. Experiments show that CM2 consistently improves over supervised fine-tuning. Starting from an 8B Base model and training on an 8k-example RL dataset, CM2 improves over the SFT counterpart by 8 points on tau^-Bench, by 10 points on BFCL-V4, and by 12 points on ToolSandbox. The results match or even outperform similarly sized open-source baselines, including the judging model. CM2 thus provides a scalable recipe for optimizing multi-turn, multi-step tool-using agents without relying on verifiable rewards. Code provided by the open-source community: https://github.com/namezhenzhang/CM2-RLCR-Tool-Agent.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
