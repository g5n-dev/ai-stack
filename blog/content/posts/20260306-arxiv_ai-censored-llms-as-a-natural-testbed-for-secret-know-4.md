---
title: Censored LLMs as a Natural Testbed for Secret Knowledge Elicitation
date: 2026-03-06 23:44:05+08:00
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
external_url: https://arxiv.org/abs/2603.05494v1
aliases:
- /posts/20260307-arxiv_ai-censored-llms-as-a-natural-testbed-for-secret-know-4/
- /posts/20260308-arxiv_ai-censored-llms-as-a-natural-testbed-for-secret-know-4/
- /posts/20260309-arxiv_ai-censored-llms-as-a-natural-testbed-for-secret-know-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:360c589c9cace6233cef2978f7103008e297885df4b8e37cea026555edb7f7f5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:27:08.846828Z'
source_capture_sha256: sha256:73740c56020b41b339212e68094cb84e9faa0395c34dd039c5bef997979f7a69
source_capture_chars_original: 1434
source_publication_excerpt_chars: 1434
observation_id: obs_95a565179d37638ab0c9f06a98edc573147d21723c6850aa43056c2769c0cfb1
revision_id: rev_88d84dc714cf0d90865de959853c9963dcf2fee0e8b38efd272059ceba9c79f9
event_id: evt_b40949b5d369efc658b818514d8f473cd2dbe851cc4caa661a48f811ebe05c38
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-06T06:19:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.05494v1](<https://arxiv.org/abs/2603.05494v1>)
- **作者**: Helena Casademunt, Bartosz Cywiński, Khoi Tran, Arya Jakkli, Samuel Marks, Neel Nanda
- **分类**: cs.LG
- **论文时间**: 2026-03-05T18:58:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.05494v1.pdf](<https://arxiv.org/pdf/2603.05494v1.pdf>)

## 来源摘要/节选

> Large language models sometimes produce false or misleading responses. Two approaches to this problem are honesty elicitation -- modifying prompts or weights so that the model answers truthfully -- and lie detection -- classifying whether a given response is false. Prior work evaluates such methods on models specifically trained to lie or conceal information, but these artificial constructions may not resemble naturally-occurring dishonesty. We instead study open-weights LLMs from Chinese developers, which are trained to censor politically sensitive topics: Qwen3 models frequently produce falsehoods about subjects like Falun Gong or the Tiananmen protests while occasionally answering correctly, indicating they possess knowledge they are trained to suppress. Using this as a testbed, we evaluate a suite of elicitation and lie detection techniques. For honesty elicitation, sampling without a chat template, few-shot prompting, and fine-tuning on generic honesty data most reliably increase truthful responses. For lie detection, prompting the censored model to classify its own responses performs near an uncensored-model upper bound, and linear probes trained on unrelated data offer a cheaper alternative. The strongest honesty elicitation techniques also transfer to frontier open-weights models including DeepSeek R1. Notably, no technique fully eliminates false responses. We release all prompts, code, and transcripts.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
