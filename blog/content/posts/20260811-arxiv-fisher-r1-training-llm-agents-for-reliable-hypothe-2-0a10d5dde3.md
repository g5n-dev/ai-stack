---
title: "Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing"
date: 2026-08-11T02:06:28+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d830458d8a792bb5f0b5b8dc5d070c3e9d9df2f2b0139147235e7e950f24f369"
source_payload_sha256: "sha256:df26a42809640fd232fe3ebeed25e20a030752ddbcc65b69167a811816a37ce6"
observation_id: obs_0a10d5dde3c98c3a19ab70b9704bc9ccfbb1dd6c299ab80328fe249a2e3786c4
event_id: evt_ab3e68002951bfb5dcb3f11a385c5e4c12fcb768befb2a4f6054451933eb8170
revision_id: rev_ca88d6424f8595c1d707504ebdfa8554289959746b3034e1ab778adf329e3167
source_published_at: 2026-08-07T17:22:00Z
first_seen_at: 2026-08-10T18:03:23.202318Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.07437v1
parent_observation_id: null
last_seen_at: 2026-08-10T18:03:23.202318Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07437v1](http://arxiv.org/abs/2608.07437v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Jiacheng Miao、Jin Mu、Guanhua Chen 等

## 来源摘要/节选

> Reliable hypothesis testing is the foundation of many empirical scientific claims. Large language model (LLM) agents are increasingly used to automate this process, as they can inspect datasets, generate code, and produce analyses end-to-end. However, we show that they frequently make subtle inferential errors that lead to incorrect conclusions despite correctly executed analyses. Existing benchmarks fail to capture this failure mode, as they rarely assess whether a reported p-value is statistically valid given the assumptions underlying the data. We address this gap by building P-Bench, a benchmark comprising 425 open-ended, realistic hypothesis-testing tasks spanning economics, biology, and medicine. Each task requires an agent to select a statistical method, compute a p-value, and draw a conclusion given only a scientific hypothesis and a dataset. We further introduce Fisher-R1, an open-weight LLM agent trained for rigorous hypothesis testing using synthetic tasks and reinforcement learning. On P-Bench, Fisher-R1-14B substantially improves over its backbone and outperforms strong proprietary and open-source baselines, including GPT-5.4 and DeepSeekV4-Pro, achieving a 21% average relative improvement in single-trial success over DeepSeek-V4-Pro, with gains up to 26% on the most challenging tasks. Our results demonstrate that current LLM agents lack reliable statistical reasoning for hypothesis testing and that reinforcement learning on tasks with verified statistical reward substantially improves reliability.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。