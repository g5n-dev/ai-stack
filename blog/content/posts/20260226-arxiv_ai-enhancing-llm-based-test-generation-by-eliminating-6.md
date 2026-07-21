---
title: Enhancing LLM-Based Test Generation by Eliminating Covered Code
date: 2026-02-26 02:52:57+08:00
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
external_url: https://arxiv.org/abs/2602.21997v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:3e9472ceb7eeae2acda8bf863c62272d29ad32271f06ce943076e7f562fef2a6
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:17:01.203007Z'
source_capture_sha256: sha256:1c4ff95af2556708cb9e219174f033c62cc4da00934af7261a181ad855d01631
source_capture_chars_original: 1356
source_publication_excerpt_chars: 1356
observation_id: obs_c81ec02cd1dacbd44e8fabb9c0cb314604a4ebc7eb16271dc7a0a34a6c367269
revision_id: rev_17f7ba84f2d46b1d79a91a0f390e47a8462b8c79b586a1dc6574af8574847305
event_id: evt_beae71e902aab2c8791ec2278723d3157c37978f6db72e301165b4d4f08ec61a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-26T03:54:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21997v1](<https://arxiv.org/abs/2602.21997v1>)
- **作者**: WeiZhe Xu, Mengyu Liu, Fanxin Kong
- **分类**: cs.SE
- **论文时间**: 2026-02-25T15:16:43Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21997v1.pdf](<https://arxiv.org/pdf/2602.21997v1.pdf>)

## 来源摘要/节选

> Automated test generation is essential for software quality assurance, with coverage rate serving as a key metric to ensure thorough testing. Recent advancements in Large Language Models \(LLMs\) have shown promise in improving test generation, particularly in achieving higher coverage. However, while existing LLM-based test generation solutions perform well on small, isolated code snippets, they struggle when applied to complex methods under test. To address these issues, we propose a scalable LLM-based unit test generation method. Our approach consists of two key steps. The first step is context information retrieval, which uses both LLMs and static analysis to gather relevant contextual information associated with the complex methods under test. The second step, iterative test generation with code elimination, repeatedly generates unit tests for the code slice, tracks the achieved coverage, and selectively removes code segments that have already been covered. This process simplifies the testing task and mitigates issues arising from token limits or reduced reasoning effectiveness associated with excessively long contexts. Through comprehensive evaluations on open-source projects, our approach outperforms state-of-the-art LLM-based and search-based methods, demonstrating its effectiveness in achieving high coverage on complex methods.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
