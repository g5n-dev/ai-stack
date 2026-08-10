---
title: "CreativeInstruct: Scalably Teaching LLMs to Balance Quality, Creativity, and Diversity"
date: 2026-08-10T12:56:59+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c2430c44b0191e42a83986415dc0579fa7f859b3f7a263449ca2015a43d9e0ef"
source_payload_sha256: "sha256:4bf935d2e5883658aa3e338f76e427fb53dc9457fd197f526f551e0393ccff71"
observation_id: obs_ead38ea357176a2a8c0ba6932bc3fb0527b70991573bf39770c80b4d80246ef7
event_id: evt_d6ebcfe59daeba76a56b4dffb75e8ce16f1317ee5c0859efd8f29f055d69c902
revision_id: rev_155dde63fedb0d9675e80d9a386f48dcb67c9504006a0a5c6c03e813adf42388
source_published_at: 2026-08-07T17:55:48Z
first_seen_at: 2026-08-10T05:06:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.07460v1
parent_observation_id: null
last_seen_at: 2026-08-10T04:53:40.223459Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07460v1](http://arxiv.org/abs/2608.07460v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Ananya Sahu、Mohit Bansal、Elias Stengel-Eskin

## 来源摘要/节选

> While post-training improves the capabilities of large language models (LLMs), it generally lowers their output diversity and creativity, negatively impacting tasks that explicitly require creativity (e.g., story generation) as well as those that require it implicitly, e.g., reinforcement learning (RL). We instead propose CreativeInstruct, a scalable instruction-tuning method that teaches LLMs to balance creative, base-model-like generations with the quality of post-trained models, by learning to inject special [StartCreativity] spans that bias generation toward creativity. Furthermore, we introduce a structural diversity metric based on graph edit distance, which captures narrative level variation missed by purely lexical and semantic metrics. On narrative generation, CreativeInstruct matches or exceeds the diversity of both multi-model baselines and distilled variants of their outputs, without sacrificing quality or requiring multiple models at inference time. These results are mirrored in our human evaluation, where we find that annotators rate CreativeInstruct generations as more creative than the post-trained LLMs' generations in 70.3% of cases. We also show the benefits of creative models as a substrate for RL: GRPO applied to a CreativeInstruct checkpoint improves by ~4% on AMC and ~5% points on MATH over the same training applied to the post-trained checkpoint.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。