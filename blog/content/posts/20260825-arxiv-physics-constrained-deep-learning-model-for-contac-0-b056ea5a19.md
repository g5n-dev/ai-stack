---
title: "Physics-Constrained Deep Learning Model for Contactless Blood Pressure Monitoring from Triaxial Bodyseismography"
date: 2026-08-25T17:02:01+08:00
draft: false
entry_kind: "auto"
tags: ["深度学习", "eess.SP", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d752af04f6c62eac8da6f85e5a5c23543980d8d3bae91bd4ca8756df095c31aa"
source_payload_sha256: "sha256:d9ef3012df3a750df5eec7ab2eacdddaa4aea119e69a31f53d6039cf0c6697ec"
observation_id: obs_b056ea5a196146d20deb9f3cd07fda6a5f10ee79eecf9321d4c7ac2fffb51d9f
event_id: evt_b3dfe5b49731213a01e4cd27684bd704709808b9c955fb5c63892cace15b2675
revision_id: rev_37a65d8f8d436ad0ce675ec267dcc76587c5a56701381af45e4f2ceedb7cdd60
source_published_at: 2026-08-24T17:58:35Z
first_seen_at: 2026-08-25T16:54:57.529377Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 112
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.23562v1
parent_observation_id: null
last_seen_at: 2026-08-25T08:59:53.016114Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23562v1](http://arxiv.org/abs/2608.23562v1)
- **发布域名**: arxiv.org
- **分类**: eess.SP
- **作者**: Yuanyuan Zhang、Yida Zhang、Jiahui Li 等

## 来源摘要/节选

> Ballistocardiography (BCG) is promising for unobtrusive long-term blood pressure (BP) monitoring in laboratory settings, but traditional BCG signals are vulnerable to the variations in body-bed interaction with shifted fiducial points in temporal or amplitude axis, and BP varies with personal hemodynamic changes, causing misaligned representations that affect model generalizability and robustness. In this work, we propose a non-invasive BP estimation framework, Phy-BP, based on triaxial bodyseismography (BSG) as an extension of BCG. Firstly, an adaptive quality-control algorithm is designed to select BSG segments enriched with cardiogenic components by jointly considering neighboring beat patterns and universal cardiogenic templates. Furthermore, a physical model is established to describe 3D wave propagation in the body-bed system and is subsequently embedded into the deep learning model to characterize the intrinsic coupling among triaxial BSG signals driven by a single cardiogenic excitation. Thus, multi-axis features are aligned during model training, improving robustness against distortions in real scenarios. Experiments on a 162-hour hospital dataset collected from 21 subjects reveal that the proposed Phy-BP can dynamically filter out low-quality measurements, and the deep learning model training is constrained by physical consistency across different axes to provide faithful BP monitoring, especially when training samples are limited.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。