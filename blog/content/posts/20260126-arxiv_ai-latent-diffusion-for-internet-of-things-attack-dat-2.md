---
title: Latent Diffusion for Internet of Things Attack Data Generation in Intrusion
  Detection
date: 2026-01-26 22:15:20+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16976v1
aliases:
- /posts/20260127-arxiv_ai-latent-diffusion-for-internet-of-things-attack-dat-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8e7dd5807d6db7b5deb67a7cdf424fc23d8a125c4f03a5e3c57d6d7b21773500
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:09:03.986411Z'
source_capture_sha256: sha256:6e5e5d9d0677dc65305c301c62e26e4ba510ee24a9aedfba8b267eecfeb5279e
source_capture_chars_original: 1723
source_publication_excerpt_chars: 1723
observation_id: obs_844a3e6fb3929d5f3663009f9cbdfdc6e08c8eaaea679f6f509bb38aec71a45d
revision_id: rev_d7e693cc27a1389f1f63ca4569c51460c8221e6c390af3884235db3d5ad08723
event_id: evt_fefc631032dffa14d3597e72e5ee4d5fb6f0ee75ecf0c9e08876ccbdecc52cad
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16976v1](<https://arxiv.org/abs/2601.16976v1>)
- **作者**: Estela Sánchez-Carballo, Francisco M. Melgarejo-Meseguer, José Luis Rojo-Álvarez
- **分类**: cs.LG
- **论文时间**: 2026-01-23T18:55:07Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16976v1.pdf](<https://arxiv.org/pdf/2601.16976v1.pdf>)

## 来源摘要/节选

> Intrusion Detection Systems \(IDSs\) are a key component for protecting Internet of Things \(IoT\) environments. However, in Machine Learning-based \(ML-based\) IDSs, performance is often degraded by the strong class imbalance between benign and attack traffic. Although data augmentation has been widely explored to mitigate this issue, existing approaches typically rely on simple oversampling techniques or generative models that struggle to simultaneously achieve high sample fidelity, diversity, and computational efficiency. To address these limitations, we propose the use of a Latent Diffusion Model \(LDM\) for attack data augmentation in IoT intrusion detection and provide a comprehensive comparison against state-of-the-art baselines. Experiments were conducted on three representative IoT attack types, specifically Distributed Denial-of-Service \(DDoS\), Mirai, and Man-in-the-Middle, evaluating both downstream IDS performance and intrinsic generative quality using distributional, dependency-based, and diversity metrics. Results show that balancing the training data with LDM-generated samples substantially improves IDS performance, achieving F1-scores of up to 0.99 for DDoS and Mirai attacks and consistently outperforming competing methods. Additionally, quantitative and qualitative analyses demonstrate that LDMs effectively preserve feature dependencies while generating diverse samples and reduce sampling time by approximately 25\\% compared to diffusion models operating directly in data space. These findings highlight latent diffusion as an effective and scalable solution for synthetic IoT attack data generation, substantially mitigating the impact of class imbalance in ML-based IDSs for IoT scenarios.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
