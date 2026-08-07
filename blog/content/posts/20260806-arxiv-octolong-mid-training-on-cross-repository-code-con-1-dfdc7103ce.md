---
title: "OctoLong: Mid-Training On Cross-Repository Code Contexts Enhances Long-Context Modeling"
date: 2026-08-06T14:49:17+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cbd93df1811c24e05b7d23aa127c7905b97ffa94029141abd175ebbb6cd7e508"
source_payload_sha256: "sha256:8059b04f5fcb9e2368db686379874784b65c84b219aa6842241ce7fa629b3c3e"
observation_id: obs_dfdc7103ce69f17230c229e69df76598d8a39744f641f42dad0479bcd46e2acb
event_id: evt_5e22e4433f13136e78bd7b2bacae9e61b7540126917e2eb91ebe6952ee2557bf
revision_id: rev_e409eb36749b9ff47d6c4e621075823013adca21f483d60f0753c503739a2b5a
source_published_at: 2026-08-05T17:58:15Z
first_seen_at: 2026-08-06T06:59:40Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.05141v1
parent_observation_id: null
last_seen_at: 2026-08-07T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.05141v1](http://arxiv.org/abs/2608.05141v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Indraneil Paul、Falko Helm、Goran Glavaš 等

## 来源摘要/节选

> Context lengths of language models (LMs) have dramatically increased, driven by the demands for in-context learning, self-improvement, and long-horizon agentic workflows. Existing long-context corpora, however, are dominated by books, academic articles, and code repositories, which are finite resources and often scarce in long-distance dependencies. In this work, we introduce OctoLong, a context engineering pipeline that instruments an AST parser, a language server backend, and a package manager to facilitate the recursive retrieval of code references, enabling the curation of dependency-rich code contexts of millions of tokens in length. We then train OctoLong-Instruct, a suite of capable long-context open LMs, derived from base models ranging in size from 600M to 14B parameters, via context-extension mid-training on a ~50B-token mixture containing ~6.2B tokens of OctoLong code contexts, followed by ~10B tokens of instruction tuning. Our training ablations and experimental evaluations against 18 state-of-the-art open-weight long-context LMs show that supplanting just 12% of traditional context-extension corpora with OctoLong data yields substantial gains in long-range retrieval, long-term state tracking, repository-level code understanding, and downstream agentic tasks, while also enhancing API usage in short-context coding scenarios.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。