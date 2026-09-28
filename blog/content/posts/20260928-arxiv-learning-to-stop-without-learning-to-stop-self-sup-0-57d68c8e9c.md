---
title: "Learning to Stop without Learning to Stop: Self-Supervised Confidence Training Improves Reasoning Efficiency"
date: 2026-09-28T14:56:22+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0a99c4208a0e9521db65fc513d33d858a4db6a681bfcdb2374ba62afc2244f27"
source_payload_sha256: "sha256:c88f7c33f2674f3fe8634f5436331030c31d72dada39d0e70078ed69349abc55"
observation_id: obs_57d68c8e9cde29aa159c8525f3e9c8d7c81c634eff0ab96b082e13f99654d5b0
event_id: evt_f6971cffb354adf2a347a3e441e171b819f51295aaf391a2bc668d1f33fb59df
revision_id: rev_0b6a747ab6351fe43ba3d9d7ab471c54d9d00eb7ef3ac9cc33a88c4a60fe8566
source_published_at: 2026-09-25T17:59:52Z
first_seen_at: 2026-09-28T06:52:36.328453Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.31619v1
parent_observation_id: null
last_seen_at: 2026-09-28T06:52:36.328453Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.31619v1](http://arxiv.org/abs/2609.31619v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Parsa Hosseini、Akasha Tigalappanavara、Sumit Nawathe 等

## 来源摘要/节选

> Reasoning models often generate very long reasoning traces, making inference computationally expensive. Existing approaches typically improve efficiency either through inference-time early-stopping mechanisms or by explicitly encouraging shorter reasoning during training, for example through reinforcement learning with length penalties. We show that substantial efficiency gains can instead emerge from a different kind of supervision: \textit{confidence}. Using a self-supervised procedure, we fine-tune reasoning models to predict their confidence in the answer at intermediate points along their own reasoning trajectories using only 600 training problems. Confidence is used only as a training target: the loss contains no objective for reasoning length, efficiency, or stopping. At inference, the fine-tuned models use the standard generation procedure, with no confidence elicitation or early-stopping mechanism. Despite this, self-supervised confidence fine-tuning makes reasoning more efficient, reducing generated tokens by up to 25\% at matched accuracy across Gemma, Qwen, Nemotron, and GPT-OSS models on mathematical, scientific, and coding reasoning benchmarks, with efficiency gains comparable to methods that explicitly optimize for shorter reasoning. Analysis of reasoning episodes further shows that confidence supervision largely preserves the base models' high-level reasoning composition rather than selectively suppressing particular behaviors. Our results suggest that efficient reasoning may emerge as a downstream consequence of learning metacognitive signals, without being directly optimized.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。