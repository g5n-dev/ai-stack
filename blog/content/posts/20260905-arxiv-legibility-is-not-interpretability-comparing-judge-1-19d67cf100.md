---
title: "Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning"
date: 2026-09-05T05:31:02+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7acda65d96061dbea73256ea85c26f3f9ddf34d566e91b6c95a557a533cb9e8b"
source_payload_sha256: "sha256:c0922f6d70dd80ee7e475c381ef41ca3068f2f2503ba6897547cd4cda93c7d25"
observation_id: obs_19d67cf100a7db2dcb176b19d2faae16aac6082741f4f557fff80a6fdd122c33
event_id: evt_9d0f0522b4933f87c62ec9f55f0ba70afcd44140c9cb41811f65d31a3b282f53
revision_id: rev_f8551c4e3d703128ccf00f9e0a084eebe03566815f13c3865ffae47ba8dec684
source_published_at: 2026-09-03T17:59:08Z
first_seen_at: 2026-09-04T21:41:03Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.04194v1
parent_observation_id: null
last_seen_at: 2026-09-05T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04194v1](http://arxiv.org/abs/2609.04194v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Kevin Du、Alexander Hoyle、Laura Ruis 等

## 来源摘要/节选

> Reasoning traces from chain-of-thought models appear to offer a legible window into how a model arrives at its answer. A growing body of work treats them as such, using LLM judges to diagnose errors, evaluate faithfulness, and provide step-level supervision via process reward models and generative critics. These practices rely on the text of a reasoning step carrying information about its functional role. But does the text actually encode information about which reasoning steps matter? We operationalize the importance of a reasoning step as its advantage: the change in expected reward, e.g., producing the correct final answer, from including that step, estimated via Monte Carlo rollouts. Basing ground truth on these estimates, we evaluate whether LLM judges can identify high-advantage steps and find that sufficiently capable LLMs can outperform a prevalence baseline but fall well short of a noise ceiling. Fine-tuning a model as a step-level critic yields strong improvement for incorrect responses but remains distant from ceiling for correct responses, suggesting that step importance is only partially recoverable from the text of the reasoning trace. Our findings contribute to a growing body of chain-of-thought faithfulness work that cautions against treating the legibility of reasoning traces as interpretability, especially with implications for process reward modeling.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。