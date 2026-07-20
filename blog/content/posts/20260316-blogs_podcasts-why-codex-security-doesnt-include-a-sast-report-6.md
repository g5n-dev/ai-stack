---
title: Why Codex Security Doesn’t Include a SAST Report
date: 2026-03-16 23:16:10+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- AI Agent
- Python
categories:
- AI 工程
scenarios:
- AI/ML项目
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://openai.com/index/why-codex-security-doesnt-include-sast
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:94816306e525954f6960897111876b5fd28466fdeea8ae32d966054a461e7451
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:19:18.743416Z'
source_capture_sha256: sha256:56b17d959567b283f94802b99258a12c35acfd0e176ac131b4a2ed6d393192a9
source_capture_chars_original: 5919
source_publication_excerpt_chars: 702
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
observation_id: obs_8a8601b30dd910cc816f9fa480fa0e35c54c207c03a9d5352126640837ee966a
revision_id: rev_0788027b34ffddfe021d1d3de56b0bd0dc487362d3daeb9de1a5d4f1f205e926
event_id: evt_671f74c1c2c4224c382d5d98f126865f24a385e42cd2dcf85b9730a68d8ba5a2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://openai.com/index/why-codex-security-doesnt-include-sast](<https://openai.com/index/why-codex-security-doesnt-include-sast>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> For decades, static application security testing \(SAST\) has been one of the most effective ways security teams scale code review.
>
> But when we built Codex Security, we made a deliberate design choice: we didn’t start by importing a static analysis report and asking the agent to triage it. We designed the system to start with the repository itself—its architecture, trust boundaries, and intended behavior—and to validate what it finds before it asks a human to spend time on it.
>
> The reason is simple: the hardest vulnerabilities usually aren’t dataflow problems. They happen when code appears to enforce a security check, but that check doesn’t actually guarantee the property the system relies on.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
