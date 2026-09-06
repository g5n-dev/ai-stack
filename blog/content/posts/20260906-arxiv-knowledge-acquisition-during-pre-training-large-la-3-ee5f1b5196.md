---
title: "Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views"
date: 2026-09-06T00:07:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c9aa25e53ce9770537b6664d44b40cd8b6adc533d3b698d2cdfd41f8a4692a6a"
source_payload_sha256: "sha256:fc82f995a4fdee50ccbc8b072ad890a8203ffa8be595d2db6ef434110cfdc5b2"
observation_id: obs_ee5f1b5196f646e9d00f7d30a45a733bb10a436091fd489d303823cea0d2e057
event_id: evt_0f269d2613eec28b60aad8a49e8af004b7763b1295fa0b6207ceced160058abe
revision_id: rev_27904db40ee2ab6b129e21041c243e46bc465211976b4dabf5f1fbae6dc881a6
source_published_at: 2026-09-03T17:57:02Z
first_seen_at: 2026-09-05T16:17:10Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:aa2a47eaaec19325c21d79074fd41ae2f9c8b722b7869ba6d19669f357ae835d"
description: "本文通过受控实验表明，预训练阶段使用知识的多种辅助表述能够提升模型的学习效果，即使在相同的 token 预算下也能改善事实记忆。"
external_url: http://arxiv.org/abs/2609.04180v1
parent_observation_id: null
last_seen_at: 2026-09-06T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04180v1](http://arxiv.org/abs/2609.04180v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Joseph Lee、Yidi Huang、Dokyoon Kim 等

## 要点解读

### 这是什么
本文通过受控实验表明，预训练阶段使用知识的多种辅助表述能够提升模型的学习效果，即使在相同的 token 预算下也能改善事实记忆。

### 用在哪里
适合大模型研发团队、数据策展人员以及关注知识获取机制的研究者，用于在设计预训练数据或评估数据多样性时提供参考。

### 可以推断的
推测：在保持总 token 量不变的前提下，用多样化的表述替代部分重复文本，有望在同等计算资源下提升模型性能。  
推测：模型的层级结构对辅助视图的利用可能表现出偏向，某些层对信息的压缩更为敏感。

## 来源摘要/节选

> Gaps remain in our understanding of how large language models (LLMs) acquire knowledge during pre-training. We posit that auxiliary views, reformulations of knowledge, are causally helpful for learning. We design controlled experiments to isolate this. First, we confirm that repetition is necessary for acquisition and clarify that paraphrasing helps only at smaller batch sizes. Second, holding the token budget fixed, allocating tokens from document repetition to auxiliary views improves learning, counterintuitively, even for factual recall. Third, the effectiveness of auxiliary views is not contingent on the strength of the teacher model that generates them. Fourth, we identify forms of knowledge, contextual and foundational, that aid learning in the presence of prior knowledge gaps. Finally, we examine how these effects manifest mechanistically via layer-wise biases and compression. Together, our findings suggest that auxiliary representations of knowledge, which arise naturally in large pre-training corpora, are a key factor in the success of pre-training and offer a plausible explanation for why data diversity matters.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。