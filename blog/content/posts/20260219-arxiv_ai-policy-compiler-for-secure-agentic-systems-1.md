---
title: Policy Compiler for Secure Agentic Systems
date: 2026-02-19 22:55:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- AI 安全
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.16708v1
aliases:
- /posts/20260220-arxiv_ai-policy-compiler-for-secure-agentic-systems-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9d6a3fa65e221f7ac970b130f2f1f50df926c6b89ac9cb1a998a3090b70fde18
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 42
captured_at: '2026-07-18T04:16:04.060671Z'
source_capture_sha256: sha256:c3b12784752a1546f7cdcc8b5f9a421d484bdcad07e7ffcb5c3fb37cff85ff0f
source_capture_chars_original: 1525
source_publication_excerpt_chars: 1525
observation_id: obs_529a7c24c1440423b4b14a995ea3ef07c108aecd7ed4a5593bf3ac0c50d2b682
revision_id: rev_6e15630f20387b7c45987c26fd3af8ad065c497a846ab95318b0cfc57861eebb
event_id: evt_2058201c1e80e6477f2cdb9b9d217aa99642cce87a839250fce5f396499443db
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-19T06:45:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.16708v1](<https://arxiv.org/abs/2602.16708v1>)
- **作者**: Nils Palumbo, Sarthak Choudhary, Jihye Choi, Prasad Chalasani, Mihai Christodorescu, Somesh Jha
- **分类**: cs.CR
- **论文时间**: 2026-02-18T18:57:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.16708v1.pdf](<https://arxiv.org/pdf/2602.16708v1.pdf>)

## 来源摘要/节选

> LLM-based agents are increasingly being deployed in contexts requiring complex authorization policies: customer service protocols, approval workflows, data access restrictions, and regulatory compliance. Embedding these policies in prompts provides no enforcement guarantees. We present PCAS, a Policy Compiler for Agentic Systems that provides deterministic policy enforcement. Enforcing such policies requires tracking information flow across agents, which linear message histories cannot capture. Instead, PCAS models the agentic system state as a dependency graph capturing causal relationships among events such as tool calls, tool results, and messages. Policies are expressed in a Datalog-derived language, as declarative rules that account for transitive information flow and cross-agent provenance. A reference monitor intercepts all actions and blocks violations before execution, providing deterministic enforcement independent of model reasoning. PCAS takes an existing agent implementation and a policy specification, and compiles them into an instrumented system that is policy-compliant by construction, with no security-specific restructuring required. We evaluate PCAS on three case studies: information flow policies for prompt injection defense, approval workflows in a multi-agent pharmacovigilance system, and organizational policies for customer service. On customer service tasks, PCAS improves policy compliance from 48% to 93% across frontier models, with zero policy violations in instrumented runs.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
