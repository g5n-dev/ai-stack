---
title: 'Data Science and Technology Towards AGI Part I: Tiered Data Management'
date: 2026-02-10 22:46:04+08:00
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
external_url: https://arxiv.org/abs/2602.09003v1
aliases:
- /posts/20260211-arxiv_ai-data-science-and-technology-towards-agi-part-i-tie-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6fecb4ac40995a513db0a64553c8244396e3802b45be737fa7ee5d084cd4ae46
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:14:24.737190Z'
source_capture_sha256: sha256:8f8cc71ed0a93be2c8cc8540c013eac6d1882516eea14eea63f419aa24193fc4
source_capture_chars_original: 1918
source_publication_excerpt_chars: 1918
observation_id: obs_000a583d1852efc8561ca8d4694632023095d2d033a41de733f2251e2a683e9b
revision_id: rev_3bd9284597d94fc0df83ebaa078850707203df843b128897f500d486975eaa4b
event_id: evt_f89581d27e90595716d28116e371f872fd024c3e1f472f1cd86df8650ff741ba
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09003v1](<https://arxiv.org/abs/2602.09003v1>)
- **作者**: Yudong Wang, Zixuan Fu, Hengyu Zhao, Chen Zhao, Chuyue Zhou, Xinle Lin, Hongya Lyu, Shuaikang Xue, Yi Yi, Yingjiao Wang, Zhi Zheng, Yuzhou Zhang, Jie Zhou, Chaojun Xiao, Xu Han, Zhiyuan Liu, Maosong Sun
- **分类**: cs.AI
- **论文时间**: 2026-02-09T18:47:51Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09003v1.pdf](<https://arxiv.org/pdf/2602.09003v1.pdf>)

## 来源摘要/节选

> The development of artificial intelligence can be viewed as an evolution of data-driven learning paradigms, with successive shifts in data organization and utilization continuously driving advances in model capability. Current LLM research is dominated by a paradigm that relies heavily on unidirectional scaling of data size, increasingly encountering bottlenecks in data availability, acquisition cost, and training efficiency. In this work, we argue that the development of AGI is entering a new phase of data-model co-evolution, in which models actively guide data management while high-quality data, in turn, amplifies model capabilities. To implement this vision, we propose a tiered data management framework, designed to support the full LLM training lifecycle across heterogeneous learning objectives and cost constraints. Specifically, we introduce an L0-L4 tiered data management framework, ranging from raw uncurated resources to organized and verifiable knowledge. Importantly, LLMs are fully used in data management processes, such as quality scoring and content editing, to refine data across tiers. Each tier is characterized by distinct data properties, management strategies, and training roles, enabling data to be strategically allocated across LLM training stages, including pre-training, mid-training, and alignment. The framework balances data quality, acquisition cost, and marginal training benefit, providing a systematic approach to scalable and sustainable data management. We validate the effectiveness of the proposed framework through empirical studies, in which tiered datasets are constructed from raw corpora and used across multiple training phases. Experimental results demonstrate that tier-aware data utilization significantly improves training efficiency and model performance. To facilitate further research, we release our tiered datasets and processing tools to the community.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
