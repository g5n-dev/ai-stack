---
title: 'MoECLIP: Patch-Specialized Experts for Zero-shot Anomaly Detection'
date: 2026-03-04 03:29:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03101v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:31c26e597f2130ca71ec2603f4b484a19a429f215e680f1e0fb6f3e9ab2b001a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:26:46.139217Z'
source_capture_sha256: sha256:541d169fb022f1b2ef00e187a8fd7bab4d6ba01790c42bb58a1177b9d10be545
source_capture_chars_original: 1389
source_publication_excerpt_chars: 1389
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03101v1](<https://arxiv.org/abs/2603.03101v1>)
- **作者**: Jun Yeong Park, JunYoung Seo, Minji Kang, Yu Rang Park
- **分类**: cs.CV
- **论文时间**: 2026-03-03T15:36:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03101v1.pdf](<https://arxiv.org/pdf/2603.03101v1.pdf>)

## 来源摘要/节选

> The CLIP model's outstanding generalization has driven recent success in Zero-Shot Anomaly Detection \(ZSAD\) for detecting anomalies in unseen categories. The core challenge in ZSAD is to specialize the model for anomaly detection tasks while preserving CLIP's powerful generalization capability. Existing approaches attempting to solve this challenge share the fundamental limitation of a patch-agnostic design that processes all patches monolithically without regard for their unique characteristics. To address this limitation, we propose \\textbf\{MoECLIP\}, a Mixture-of-Experts \(MoE\) architecture for the ZSAD task, which achieves patch-level adaptation by dynamically routing each image patch to a specialized Low-Rank Adaptation \(LoRA\) expert based on its unique characteristics. Furthermore, to prevent functional redundancy among the LoRA experts, we introduce \(1\) Frozen Orthogonal Feature Separation \(FOFS\), which orthogonally separates the input feature space to force experts to focus on distinct information, and \(2\) a simplex equiangular tight frame \(ETF\) loss to regulate the expert outputs to form maximally equiangular representations. Comprehensive experimental results across 14 benchmark datasets spanning industrial and medical domains demonstrate that MoECLIP outperforms existing state-of-the-art methods. The code is available at https://github.com/CoCoRessa/MoECLIP.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
