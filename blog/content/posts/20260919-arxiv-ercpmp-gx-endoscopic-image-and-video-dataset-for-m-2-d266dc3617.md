---
title: "ERCPMP-Gx: Endoscopic Image and Video Dataset for Morphological, Histopathological, and Genomic Characterization of Colorectal Polyposis"
date: 2026-09-19T02:30:37+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b5b1354e8b4c4fcb326e7ef9a70be29b2fbed7ae07ea0094fada399ae50c9191"
source_payload_sha256: "sha256:17dccbcd874d6ca47c07f1b8590b3b3edfbf6615274e54203d37f23a9ded52ab"
observation_id: obs_d266dc36176b04cb22e9cee53723559d434f5b7649b8ded46b309e80215b5b86
event_id: evt_e8e443268679124b863996314507c97d7e1f300a9785c365ac03f0497355d7fa
revision_id: rev_e32c077b951e687f8760bd1a55d4ef9f0efb09a1ee243ad967908dad2f36809f
source_published_at: 2026-09-17T17:59:28Z
first_seen_at: 2026-09-18T18:41:58Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 136
interpretation_sha256: "sha256:9867f62952f2ce38a06f60cfdf6029337dec5f9e85470f2d2c3c85739a7c0145"
description: "这是一份结合了结肠镜图像、视频、组织病理学和胚系基因信息的多模态数据集，旨在支持人工智能在结直肠息肉病识别和分类中的应用。"
external_url: http://arxiv.org/abs/2609.20815v1
parent_observation_id: null
last_seen_at: 2026-09-21T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20815v1](http://arxiv.org/abs/2609.20815v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Zahra Ghaffari、Massih Bahar、Mojgan Forootan 等

## 要点解读

### 这是什么
这是一份结合了结肠镜图像、视频、组织病理学和胚系基因信息的多模态数据集，旨在支持人工智能在结直肠息肉病识别和分类中的应用。

### 用在哪里
适用于医学影像与AI交叉领域的研究团队，用于开发、训练和验证能够区分遗传性息肉综合征与非遗传性息肉的算法；也可供临床医生评估AI辅助诊断的可行性。

### 可以推断的
推测：该数据集的多模态标注能够促进跨模态特征学习，提升模型在复杂临床场景中的鲁棒性。  
推测：基于患者层面的关联信息，模型有望实现更具临床意义的个体化风险评估。

## 来源摘要/节选

> Hereditary polyposis syndromes can be precursor lesions to colorectal cancer and are associated with a broad spectrum of extracolonic tumors. Early identification and accurate classification of these syndromes are essential for timely diagnosis, individualized patient management, and targeted surveillance strategies for affected families. However, public endoscopic datasets are largely organized around the individual sporadic polyp, and none links the polyposis phenotype to histopathology and germline findings at the patient level. Here, we present ERCPMP-Gx, an endoscopic, histopathological, and genomic dataset developed to support the application of artificial intelligence (AI) in the recognition, characterization, and classification of colorectal polyposis. Most procedures were performed using the Olympus EVIS X1 system with white-light endoscopy (WLE), narrow-band imaging (NBI), magnifying NBI (M-NBI), and NBI with near focus modes, yielding 160 images and accompanying video clips. Approximately eighty percent of cases represent clinically and/or genetically confirmed hereditary polyposis syndromes (PG), including familial adenomatous polyposis (FAP), Peutz-Jeghers syndrome (PJS), juvenile polyposis syndrome (JPS), and ganglioneuroma syndrome (GNS), while the remaining twenty percent comprise non-hereditary polyps and polyp-mimicking lesions with overlapping morphological features (Non-PG), included to support differential classification. Each released record is linked, where available, to standardized endoscopic annotations, representative histopathology, and clinically reported germline findings, forming an AI-ready, patient-level annotation framework. The dataset is publicly accessible at Mendeley (https://doi.org/10.17632/nzyfc544bx.2). For the latest updates and further information, readers are referred to the DataBioX website: https://databiox.com.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。