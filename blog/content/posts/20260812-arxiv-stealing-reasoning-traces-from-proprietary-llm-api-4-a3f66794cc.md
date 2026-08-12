---
title: "Stealing Reasoning Traces from Proprietary LLM APIs"
date: 2026-08-12T08:01:44+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Prompt 工程", "cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d33ec08c5ff74ed267f66469c34acf9e88b5c8e34f89a553f33a24f04ec4be8e"
source_payload_sha256: "sha256:94a89859c4e45a4b68edd13d60156924d88b93efe79b16927eedc8150439417a"
observation_id: obs_a3f66794ccd26d9a54ab9cdcff437c26b51d66c14cf843c80567cf318c10e06c
event_id: evt_5a251ea672e8a80f1e7f612faa1bbd4856baab52c263035633cb4f06062657e6
revision_id: rev_ede56f3e1c6f310f4b824d2dbf3588b05177572053f946cfcb9a68f914d02d00
source_published_at: 2026-08-10T17:24:50Z
first_seen_at: 2026-08-11T23:59:39.120641Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 51
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.09867v1
parent_observation_id: null
last_seen_at: 2026-08-11T23:59:39.120641Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09867v1](http://arxiv.org/abs/2608.09867v1)
- **发布域名**: arxiv.org
- **分类**: cs.CR
- **作者**: Alexander Panfilov、David Schmotz、Ilia Shumailov 等

## 来源摘要/节选

> Leading large language model providers now conceal their models' step-by-step reasoning, or chain-of-thought, to protect intellectual property and limit information leakage. Rather than storing these traces server-side, providers return them to the client as blocks of encrypted text, which the client passes back with each subsequent request. Building on prior research, we identify an architectural vulnerability: these encrypted blocks are fully compatible and interchangeable across different sessions, users, and models within a provider's ecosystem. We exploit this compatibility to develop a scalable decryption jailbreak. By injecting an encrypted reasoning trace from a given model into a weaker, and less safeguarded model from the same provider, we force it to decode and output the trace verbatim in plaintext, without ever jailbreaking the more capable model directly. This vulnerability enables four distinct attack vectors. First, it circumvents anti-distillation mechanisms, allowing adversaries to extract a proprietary model's reasoning, as we demonstrate across Anthropic, OpenAI, and Google. Second, it allows for large-scale private data extraction. Developers frequently share session logs publicly, unaware of contents of the encrypted blocks. By decoding 315,320 reasoning blocks scraped from public repositories, we recovered 367 Personally Identifiable Information (PII) artifacts and 182 credentials. Third, it inadvertently reveals hazardous information hidden within the reasoning process, even in cases where the model's final, visible output safely rejects a malicious request. Fourth, attackers can leverage this flaw to execute invisible prompt injections, embedding malicious payloads entirely within encrypted blocks to poison public agentic rollouts. Following responsible disclosure, we propose concrete cryptographic and system-level mitigations to secure client-side reasoning.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。