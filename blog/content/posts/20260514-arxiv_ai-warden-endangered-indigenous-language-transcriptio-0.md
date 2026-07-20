---
title: 'WARDEN: Endangered Indigenous Language Transcription and Translation with
  6 Hours of Training Data'
date: 2026-05-14 23:14:11+08:00
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
external_url: https://arxiv.org/abs/2605.13846v1
aliases:
- /posts/20260515-arxiv_ai-warden-endangered-indigenous-language-transcriptio-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e1bf24f15b721078500ea0bb5fdd5772fa1ec43d51a9a2e014200165a1db4f13
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
captured_at: '2026-07-18T04:29:39.576255Z'
source_capture_sha256: sha256:56c3a857401eb965c66dcd4f888ebb1517e53adf353ec9a341e5a94273902a6e
source_capture_chars_original: 1483
source_publication_excerpt_chars: 1483
observation_id: obs_7df6aecda04d7347a493220575de3388e8703b14f73d725a015d1fe8ceb94201
revision_id: rev_1634475c7e34686cf26f3d6514ce3e601406a2c9c7e8ccc536b5abbf2c1bcfa8
event_id: evt_2219f8572d0e16a42d717212000efc8f3b10f5b75a1ca87b734688b8837c31bf
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.13846v1](<https://arxiv.org/abs/2605.13846v1>)
- **作者**: Ziheng Zhang, Yunzhong Hou, Naijing Liu, Liang Zheng
- **分类**: cs.CL
- **论文时间**: 2026-05-13T17:59:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.13846v1.pdf](<https://arxiv.org/pdf/2605.13846v1.pdf>)

## 来源摘要/节选

> This paper introduces WARDEN, an early language model system capable of transcribing and translating Wardaman, an endangered Australian indigenous language into English. The significant challenge we face is the lack of large-scale training data: in fact, we only have 6 hours of annotated audio. Therefore, while it is common practice to train a single model for transcription and translation using large datasets \(like English to French\), this practice is no longer viable in the Wardaman to English context. To tackle the low-resource challenge, we design WARDEN to have separate transcription and translation models: WARDEN first turns a Wardaman audio input into phonemic transcription, and then the transcription into English translation. Further, we propose two useful techniques to enhance performance. For transcription, we initialize the Wardaman token from Sundanese, a language that shares similar phonemes with Wardaman, to accelerate fine-tuning of the transcription model. For translation, we compile a Wardaman-English dictionary from expert annotations, and provide this domain-specific knowledge to a large language model \(LLM\) to reason and decide the final output. We empirically demonstrate that this two-stage design works better than data-hungry unified approaches in extremely low data settings. Using a mere 6 hours of annotated data, WARDEN outperforms larger open-source and proprietary models and establishes a strong baseline. Data and code are available.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
