---
title: "Structural Silence: When AI Infrastructure Fails Speakers of Underrepresented Languages"
date: 2026-08-13T23:17:46+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2da2815534937386537949910ed0fe8641d33ecee92a53c285669503946dfed6"
source_payload_sha256: "sha256:1ed7ad34a75ec787303842224cbf6eb3b5008317237fa46f00d17772adbf7376"
observation_id: obs_816a41bfe0244d2e89c65a4c3873e11f118968c384048561ac2f80a75bbdcb7e
event_id: evt_b8abdcc49a196e7348410aaaaf7c37e050e5c91077b5b0bbf782772b58b05294
revision_id: rev_78af4f68a70cfe15396c210f16523caebd7405743c802614ec45bd7bb43d73c9
source_published_at: 2026-08-12T17:17:25Z
first_seen_at: 2026-08-13T15:27:24Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
interpretation_sha256: "sha256:a7620fc2b9c2fc81103155fc958f948105abd10505f5f49a1f01b7f16c93a992"
description: "文章分析了在资源不足语言社区中，AI 教育工具因底层基础设施的系统性缺陷而对使用者产生不利影响，包括网络内容稀缺、训练语料不平衡、分词导致的 token 费用以及网络接入差异，指出这些都是结构性障碍，并主张离线优先的设计是实现公平的途径。"
external_url: http://arxiv.org/abs/2608.12278v1
parent_observation_id: null
last_seen_at: 2026-08-13T15:15:00.676326Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12278v1](http://arxiv.org/abs/2608.12278v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Avijit Roy、Proma Roy

## 要点解读

### 这是什么
文章分析了在资源不足语言社区中，AI 教育工具因底层基础设施的系统性缺陷而对使用者产生不利影响，包括网络内容稀缺、训练语料不平衡、分词导致的 token 费用以及网络接入差异，指出这些都是结构性障碍，并主张离线优先的设计是实现公平的途径。

### 用在哪里
适用于关注语言技术公平性、研究低资源语言处理、或在网络受限地区规划教育 AI 项目的政策制定者与技术研发人员。

### 可以推断的
推测：若要在类似环境取得成效，需要投入大量本地数据采集与离线模型适配工作。  
推测：此类结构性问题的解决可能促使 AI 研发规范中加入对语言覆盖率的硬性要求。

## 来源摘要/节选

> Artificial intelligence tools for education and language support are increasingly framed as scalable responses to access gaps in under-resourced communities. Yet the infrastructure underlying these tools, including training corpora, tokenization schemes, evaluation benchmarks, and deployment architectures, can systematically disadvantage speakers of underrepresented languages before a model is trained.
> This paper examines these structural barriers through Bengali, one of the world's most widely spoken languages, focusing on AI-assisted education in low-connectivity environments. We identify four interlocking failures: a severe web presence gap, with Bengali accounting for less than 0.5% of global web content despite representing nearly 4% of the global population; a 67:1 training-token deficit between English and Bengali in major multilingual corpora; a tokenization penalty associated with Bengali's alphasyllabary script that compounds the data deficit through higher token fertility; and connectivity exclusion, with individual internet penetration at 36.5% in rural areas compared with 71.4% in urban areas.
> These failures reflect longstanding resource-allocation decisions, institutional priorities, and design defaults that did not center underrepresented languages in mainstream AI development. We argue that dataset scarcity should be understood as a structural barrier rather than an isolated technical limitation, and that offline-first design should be treated as an equity-oriented infrastructure strategy. We conclude with directions for linguistics and AI research aimed at reducing these structural inequalities.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。