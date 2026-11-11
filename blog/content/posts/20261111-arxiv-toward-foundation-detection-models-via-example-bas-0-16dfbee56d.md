---
title: "Toward Foundation Detection Models via Example-Based Grounding in EM-DETR"
date: 2026-11-11T22:20:31+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6a97b054954b183a0eb9c5be91f5b84709ee7100459b0252c86a8bd88f20530c"
source_payload_sha256: "sha256:5ee41e0afd5301fce9f15d4c872672994463c0c24282d6c81813197a934835b2"
observation_id: obs_16dfbee56de33db2dfda3d59931f1172a7b5afaec5e3c1b6e65ccd055a53c798
event_id: evt_2a52ab19c2ffb090334e16fc7c9a3ec9237de3e67eb5ed7a96f2ed7aef17a70e
revision_id: rev_9fd7a3394a4cd1b337d4f2628eaf82d54143aa42190d4251aa6ebe329d1b3cff
source_published_at: 2026-11-10T18:59:17Z
first_seen_at: 2026-11-11T14:18:40.632061Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:acab1957ccfa27fa8b80e2b6cf39ec8581a8d6cd3ceec69055aa941a74985018"
description: "该研究提出一种面向病灶检测的多域基础模型构建方法，通过师生训练与基于示例的 EM-DETR 框架，融合不同医学影像数据集及异构标注空间。其在胸片和乳腺影像任务上取得领先结果，并缓解联合训练中的灾难性遗忘问题。"
external_url: http://arxiv.org/abs/2611.14518v1
parent_observation_id: null
last_seen_at: 2026-11-11T14:18:40.632061Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.14518v1](http://arxiv.org/abs/2611.14518v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Sheethal Bhat、Bogdan Georgescu、Awais Mansoor 等

## 要点解读

### 这是什么
该研究提出一种面向病灶检测的多域基础模型构建方法，通过师生训练与基于示例的 EM-DETR 框架，融合不同医学影像数据集及异构标注空间。其在胸片和乳腺影像任务上取得领先结果，并缓解联合训练中的灾难性遗忘问题。

### 用在哪里
适用于医疗影像 CAD 系统、病灶检测模型，以及需要整合多个数据集进行训练的研究团队，尤其适合处理标注体系和数据分布不一致的场景。

### 可以推断的
- 推测：师生训练策略可能有助于降低多数据集联合训练时对单一数据分布的依赖。
- 推测：细粒度的示例驱动检测思路，可能为跨模态医学影像检测模型的构建提供参考。

## 来源摘要/节选

> DeepLearning (DL)-based Computer-Aided Diagnostic (CAD) systems have shown great promise in supporting clinicians, but their performance heavily depends on the availability of large, well-annotated datasets. In medical lesion detection, the scarcity of comprehensive, stan dardized annotations and the heterogeneity of existing datasets limit the development of robust foundation models. In this work, we introduce a novel approach to building a multi-domain foundation model for le sion detection by integrating diverse medical image datasets annotated for both anatomical structures and abnormalities. We first propose a student-teacher training strategy to effectively combine datasets with heterogeneous label spaces, mitigating catastrophic forgetting, and im proving feature learning. In addition, building on our previously pro posed example-based EM-DETR framework, we adapt it to jointly learn from multiple domain-specific datasets, enabling fine-grained, example driven detection across modalities. Our model achieves state-of-the-art (SOTA) results, with image-level AUC scores exceeding previous SOTA by 1% point on four key findings in CXRs. We achieve a leading mAP50 in CXRs and mammography, surpassing EM-DETR trained on a single dataset by 2-3% points. This approach paves the way for scalable foundation models in medical imaging that leverage heterogeneous data while maintaining robust and generalizable performance.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。