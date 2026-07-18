---
title: 'In-Context Autonomous Network Incident Response: An End-to-End Large Language
  Model Agent Approach'
date: 2026-02-16 23:54:05+08:00
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
external_url: https://arxiv.org/abs/2602.13156v1
aliases:
- /posts/20260217-arxiv_ai-in-context-autonomous-network-incident-response-an-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e7e4d00db09c8759a1be8982cc8f3a1f935ef3afad993b84690ad10896c02eed
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
captured_at: '2026-07-18T04:15:33.978565Z'
source_capture_sha256: sha256:b88840cb5797df24c39c05ec612f6e4514cdd86da274f403fc7cd71d75de0e5c
source_capture_chars_original: 1520
source_publication_excerpt_chars: 1520
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.13156v1](<https://arxiv.org/abs/2602.13156v1>)
- **作者**: Yiran Gao, Kim Hammar, Tao Li
- **分类**: cs.CR
- **论文时间**: 2026-02-13T18:09:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.13156v1.pdf](<https://arxiv.org/pdf/2602.13156v1.pdf>)

## 来源摘要/节选

> Rapidly evolving cyberattacks demand incident response systems that can autonomously learn and adapt to changing threats. Prior work has extensively explored the reinforcement learning approach, which involves learning response strategies through extensive simulation of the incident. While this approach can be effective, it requires handcrafted modeling of the simulator and suppresses useful semantics from raw system logs and alerts. To address these limitations, we propose to leverage large language models' \(LLM\) pre-trained security knowledge and in-context learning to create an end-to-end agentic solution for incident response planning. Specifically, our agent integrates four functionalities, perception, reasoning, planning, and action, into one lightweight LLM \(14b model\). Through fine-tuning and chain-of-thought reasoning, our LLM agent is capable of processing system logs and inferring the underlying network state \(perception\), updating its conjecture of attack models \(reasoning\), simulating consequences under different response strategies \(planning\), and generating an effective response \(action\). By comparing LLM-simulated outcomes with actual observations, the LLM agent repeatedly refines its attack conjecture and corresponding response, thereby demonstrating in-context adaptation. Our agentic approach is free of modeling and can run on commodity hardware. When evaluated on incident logs reported in the literature, our agent achieves recovery up to 23% faster than those of frontier LLMs.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
