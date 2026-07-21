---
title: 'FineInstructions: Scaling Synthetic Instructions to Pre-Training Scale'
date: 2026-01-30 23:03:03+08:00
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
external_url: https://arxiv.org/abs/2601.22146v1
aliases:
- /posts/20260131-arxiv_ai-fineinstructions-scaling-synthetic-instructions-to-7/
- /posts/20260201-arxiv_ai-fineinstructions-scaling-synthetic-instructions-to-7/
- /posts/20260202-arxiv_ai-fineinstructions-scaling-synthetic-instructions-to-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:88676f28da688d649c45942963d7fe1f18c17de692fdd0a2bd910ed1b3ce403e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:09:48.978849Z'
source_capture_sha256: sha256:6d10721c58a4916740e11c92c81e5572a55dab24fa7fd609673bba4242d376a3
source_capture_chars_original: 1450
source_publication_excerpt_chars: 1450
observation_id: obs_80f61413df55467d89f9a9e233f6d383d2a34260b3442c1116f37c17b09deb6e
revision_id: rev_89a99b5d4b652f5d3d43ff3f84917729319c79e2a96d431f1a1b58e094dfe787
event_id: evt_58d95e967c9cf6c3241cfd7847661a89cf51e6d7c3ee4b05ad9200a8e391b452
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-30T05:20:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22146v1](<https://arxiv.org/abs/2601.22146v1>)
- **作者**: Ajay Patel, Colin Raffel, Chris Callison-Burch
- **分类**: cs.CL
- **论文时间**: 2026-01-29T18:58:47Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22146v1.pdf](<https://arxiv.org/pdf/2601.22146v1.pdf>)

## 来源摘要/节选

> Due to limited supervised training data, large language models \(LLMs\) are typically pre-trained via a self-supervised "predict the next word" objective on a vast amount of unstructured text data. To make the resulting model useful to users, it is further trained on a far smaller amount of "instruction-tuning" data comprised of supervised training examples of instructions and responses. To overcome the limited amount of supervised data, we propose a procedure that can transform the knowledge in internet-scale pre-training documents into billions of synthetic instruction and answer training pairs. The resulting dataset, called FineInstructions, uses ~18M instruction templates created from real user-written queries and prompts. These instruction templates are matched to and instantiated with human-written source documents from unstructured pre-training corpora. With "supervised" synthetic training data generated at this scale, an LLM can be pre-trained from scratch solely with the instruction-tuning objective, which is far more in-distribution with the expected downstream usage of LLMs \(responding to user prompts\). We conduct controlled token-for-token training experiments and find pre-training on FineInstructions outperforms standard pre-training and other proposed synthetic pre-training techniques on standard benchmarks measuring free-form response quality. Our resources can be found at https://huggingface.co/fineinstructions .

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
