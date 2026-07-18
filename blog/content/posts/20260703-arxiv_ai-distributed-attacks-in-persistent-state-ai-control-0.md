---
title: Distributed Attacks in Persistent-State AI Control
date: 2026-07-03 23:19:23+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 命令行工具
categories:
- 论文
scenarios:
- AI/ML项目
- 命令行工具
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2607.02514v1
aliases:
- /posts/20260704-arxiv_ai-distributed-attacks-in-persistent-state-ai-control-0/
- /posts/20260705-arxiv_ai-distributed-attacks-in-persistent-state-ai-control-0/
- /posts/20260706-arxiv_ai-distributed-attacks-in-persistent-state-ai-control-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4bb05335955f5fd7f75ed0250371f6b5b7e8f1cc6389f442f73e40ff77c8b204
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 50
captured_at: '2026-07-18T04:30:14.398876Z'
source_capture_sha256: sha256:5ec6938b158a4e2891a06f7953687b7a82c39113ac138ad3a9870a6336ca97e9
source_capture_chars_original: 1916
source_publication_excerpt_chars: 1916
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.02514v1](<https://arxiv.org/abs/2607.02514v1>)
- **作者**: Josh Hills, Ida Caspary, Asa Cooper Stickland
- **分类**: cs.AI
- **论文时间**: 2026-07-02T17:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.02514v1.pdf](<https://arxiv.org/pdf/2607.02514v1.pdf>)

## 来源摘要/节选

> As AI coding agents become more autonomous, they increasingly ship code iteratively, with the codebase persisting across sessions. This persistence creates a new attack surface: a misaligned or prompt-injected agent can distribute attacks across pull requests \(PRs\) and time its payload for the PR with the best natural cover. To study the resulting dynamics, we introduce Iterative VibeCoding, a setting for AI control, the study of safely deploying capable but potentially untrusted AI. In Iterative VibeCoding, a coding agent builds software over a sequence of PRs in a persistent codebase while pursuing a covert side task. Our benchmark includes two task families: CLI tools and Flask web services, across 20 total task variations. We use Claude Sonnet 4.5 as the attack agent and GPT-4o as the monitor. We compare gradual attacks, which distribute the side task across PRs, against non-gradual attacks concentrated in a single PR. No single monitor is robust to both: which strategy evades best \(success while evading the monitor\) depends on the monitor type, so a defender cannot close off both gradual and non-gradual attacks with any one monitor. High evasion \(&gt;= 65%\) generalizes across model attack agent backends \(Sonnet 4.5, Gemini 3.1 Pro, Kimi K2.5\), confirming this is a property of the persistent-state attack surface rather than a single model's capability. Evasion also remains high across state-of-the-art monitor models and the gap between gradual and non-gradual evasion widens for more capable models. We introduce a stateful link-tracker monitor that tracks suspicious buildup across PRs. On both task families, it detects gradual attacks substantially better than diff monitors that merely see more accumulated history. Combining this stronger monitor with trajectory monitors in a four-monitor ensemble reduces gradual-attack evasion from 93% under the weakest standard diff monitor to 47%.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
