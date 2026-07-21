---
title: 'MovieTeller: Tool-augmented Movie Synopsis with ID Consistent Progressive
  Abstraction'
date: 2026-02-27 02:54:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23228v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9525db058cca5ef09893329647f751fb80ea4ba9b2fbcecb0a34399969760c60
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:30:40.966842Z'
source_capture_sha256: sha256:9d2452c15f080d05234f6aad59165218b44ebd7b482035d9c1b05fbb1a26f31f
source_capture_chars_original: 1683
source_publication_excerpt_chars: 1683
observation_id: obs_42f21c97122bfbacd1779c3eb74455fc656cf54d96db793e9223286eb136483b
revision_id: rev_48ccb64c2bc23b7d0ed6e861e27309872aa263f31dcac920dc808ae7a98ff38f
event_id: evt_b22154929d8dddeb2a569a956c24779ce8b4d2a80d1cf6aa549583d2af14cede
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23228v1](<https://arxiv.org/abs/2602.23228v1>)
- **作者**: Yizhi Li, Xiaohan Chen, Miao Jiang, Wentao Tang, Gaoang Wang
- **分类**: cs.CV
- **论文时间**: 2026-02-26T17:08:08Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23228v1.pdf](<https://arxiv.org/pdf/2602.23228v1.pdf>)

## 来源摘要/节选

> With the explosive growth of digital entertainment, automated video summarization has become indispensable for applications such as content indexing, personalized recommendation, and efficient media archiving. Automatic synopsis generation for long-form videos, such as movies and TV series, presents a significant challenge for existing Vision-Language Models \(VLMs\). While proficient at single-image captioning, these general-purpose models often exhibit critical failures in long-duration contexts, primarily a lack of ID-consistent character identification and a fractured narrative coherence. To overcome these limitations, we propose MovieTeller, a novel framework for generating movie synopses via tool-augmented progressive abstraction. Our core contribution is a training-free, tool-augmented, fact-grounded generation process. Instead of requiring costly model fine-tuning, our framework directly leverages off-the-shelf models in a plug-and-play manner. We first invoke a specialized face recognition model as an external "tool" to establish Factual Groundings--precise character identities and their corresponding bounding boxes. These groundings are then injected into the prompt to steer the VLM's reasoning, ensuring the generated scene descriptions are anchored to verifiable facts. Furthermore, our progressive abstraction pipeline decomposes the summarization of a full-length movie into a multi-stage process, effectively mitigating the context length limitations of current VLMs. Experiments demonstrate that our approach yields significant improvements in factual accuracy, character consistency, and overall narrative coherence compared to end-to-end baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
