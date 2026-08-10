---
title: "SABRE: Scalable and Automated Benchmarking of VLMs under Stress"
date: 2026-08-11T04:07:33+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:572bf9e1b2e1d26edd23a928fc627ca49346752c9ae73b76e626e1e32453adf5"
source_payload_sha256: "sha256:c41ddb26d9719ca3b4c697ad31a3040573887dfe096f386dbb7db33a9b4d369b"
observation_id: obs_175de40b92df1b2ea6d884c76739435592f66f22b5f62ee5fddd297d9f3bf02b
event_id: evt_58e7a39efe452ec2635cf883e581c0413e813bd8dcd8a9a24ff8346d3c874a41
revision_id: rev_e416c56aa1ce61fefb8ceeac857be75b93c7946e804139f47f038dcce93ca03f
source_published_at: 2026-08-07T17:21:04Z
first_seen_at: 2026-08-10T21:02:06.430219Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
interpretation_sha256: "sha256:c4c6ff831a4b87b3ab177a8a65a2c2993b0a38238b1fd0a6ae9ce13b289bc01f"
description: "SABRE 是一个可扩展的自动化流水线，将结构化的任务说明转化为图像与问答对，并通过过滤和人工审查剔除模型轻易答对的样本，以构建针对视觉‑语言模型的抗压基准。"
external_url: http://arxiv.org/abs/2608.07435v1
parent_observation_id: null
last_seen_at: 2026-08-10T20:03:45.150860Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07435v1](http://arxiv.org/abs/2608.07435v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Zixuan Lan、Luzhe Sun、Matthew R. Walter 等

## 要点解读

### 这是什么
SABRE 是一个可扩展的自动化流水线，将结构化的任务说明转化为图像与问答对，并通过过滤和人工审查剔除模型轻易答对的样本，以构建针对视觉‑语言模型的抗压基准。

### 用在哪里
适用于需要系统化评估视觉‑语言模型在违背常规先验条件下表现的科研团队和基准制定者；也可用于在模型迭代期间快速生成新测试样例。

### 可以推断的
推测：随着模型规模提升，研究者会更频繁地依赖此类自动化工具来保持基准的时效性。  
推测：在实际部署中，模型若无法抵御先验误导，可能导致在真实场景中出现系统性错误。

## 来源摘要/节选

> Vision-language models (VLMs) are improving rapidly, but benchmark development lags behind, making weaknesses hard to identify. Building stress tests is costly: samples must satisfy controlled conditions, remain answerable, and challenge current models. We present SABRE, a scalable, automated pipeline that converts a Test Primer (a Markdown Task Design with Data Schema) into structured specifications, generated or edited images, and question-answer pairs. Automated filtering removes candidates solved by a Filtering VLM, while human review verifies candidate validity and supports annotation correction and localized image repair. We instantiate SABRE-Prior to test whether VLMs follow visual evidence instead of relying on world priors -- learned expectations about familiar objects and scenes. Its 600 images and 1,000 questions span Context (unexpected entities in familiar scenes), Texture (counterfactual materials), Attribute (noncanonical component counts), and Language Elicitation (answers suggested by language but unsupported by the image). Across six VLMs, macro-average accuracy ranges from 17.8% to 31.3% (22.6% mean). A real-image Attribute control is comparably difficult for the Filtering VLM. SABRE-Counting and SABRE-Spatial pilots show that the workflow supports other stress-test settings. These results establish SABRE as a reusable framework for constructing and refreshing VLM stress tests rather than a single fixed benchmark.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。