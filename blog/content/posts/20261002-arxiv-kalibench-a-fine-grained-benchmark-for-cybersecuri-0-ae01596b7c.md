---
title: "KaliBench: A Fine-Grained Benchmark for Cybersecurity Tool Use on Kali Linux with Runtime-Free Verifiable Rewards"
date: 2026-10-02T16:36:32+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:3adf50ca3da0d13ba8016e2d31f8763d07fb7cda78d1fcec326b9df16848bba5"
source_payload_sha256: "sha256:33bdcbab637b0eeedbd7fcb6aad4d8d7c57d597ddcdd7ca70f1b0799531fd2fe"
observation_id: obs_ae01596b7ceef23a4dfc8c08a5534e2142bd24863457ccd9e9dbab4e41f69659
event_id: evt_10d37f23af2b0daee8fdda9f9f281ccbc8967d1ab6e533adee4cdd5993d8b584
revision_id: rev_f119a883e32dbd8cf5b17d8f6bed4b2e5aa2a9c1624b6531115b07ab32de9e7f
source_published_at: 2026-10-01T17:59:55Z
first_seen_at: 2026-10-02T08:33:55.646939Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 113
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2610.02206v1
parent_observation_id: null
last_seen_at: 2026-10-02T08:33:55.646939Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02206v1](http://arxiv.org/abs/2610.02206v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Pengfei Li、Naufal Suryanto、Sicheng Zhang 等

## 来源摘要/节选

> LLMs are increasingly applied to cybersecurity workflows, where they are expected to translate analysts' intent into tool invocations. However, existing evaluations focus on knowledge-based assessments or end-to-end agentic tasks, and do not directly measure LLMs' ability to generate executable commands for real-world cybersecurity tools. This gap is critical because cybersecurity operations rely on strict command-line interfaces (CLIs), where minor syntax errors, incorrect flag--value bindings, or argument misordering can invalidate execution. We introduce KaliBench, a fine-grained benchmark and dataset for natural-language--to--CLI translation on Kali Linux, comprising 8,504 query--command pairs spanning 1,642 tools across 23 capability dimensions and 5 security phases. KaliBench is constructed via a manuscript-grounded pipeline with deterministic canonicalization and alias-aware evaluation, enabling precise and reproducible assessment of tool selection and argument construction. To ensure both semantic correctness and practical executability, we develop a multi-stage verification pipeline that combines LLM-based validation, sandboxed terminal execution, and human-in-the-loop refinement. Building on these fine-grained, deterministic signals, KaliBench further enables runtime-free verifiable rewards for training. Across three evaluation modes and 24 configurations of general-purpose and security-focused open-weight models, no open-weight model exceeds 42% exact-command accuracy in the unrestricted setting, highlighting the difficulty of accurate CLI-based cybersecurity tool use without explicit tool hints. We further show that supervised fine-tuning and reinforcement learning with verifiable rewards derived from KaliBench significantly improve an 8B model and achieve performance comparable to a 685B MoE model.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。