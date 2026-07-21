---
title: 'A recipe for scalable attention-based MLIPs: unlocking long-range accuracy
  with all-to-all node attention'
date: 2026-03-09 21:48:42+08:00
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
external_url: https://arxiv.org/abs/2603.06567v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:428c0fa979d66f41fb3da8b4bb069cb2ff77aa933a57a5ca59a3ae43b5c3442d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 105
captured_at: '2026-07-18T04:27:20.159062Z'
source_capture_sha256: sha256:81f4a54461ad6373550ac2b0b6ed4389223a20fe6eb12f9e89b329b013dd163f
source_capture_chars_original: 1263
source_publication_excerpt_chars: 1263
observation_id: obs_0d37a22473d84093305a221cb951374d9f41ff199f790c261880ac6e863c57db
revision_id: rev_c1b83bc9f7320c004a8dfc46749af9c922a3adb2d288f48b1d6c29330a8b0cc9
event_id: evt_941f606fc7be8cb11dcee82c838dc108e3e0948b1e256653425523594a0486e2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T03:53:15Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.06567v1](<https://arxiv.org/abs/2603.06567v1>)
- **作者**: Eric Qu, Brandon M. Wood, Aditi S. Krishnapriyan, Zachary W. Ulissi
- **分类**: cs.LG
- **论文时间**: 2026-03-06T18:57:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.06567v1.pdf](<https://arxiv.org/pdf/2603.06567v1.pdf>)

## 来源摘要/节选

> Machine-learning interatomic potentials \(MLIPs\) have advanced rapidly, with many top models relying on strong physics-based inductive biases. However, as models scale to larger systems like biomolecules and electrolytes, they struggle to accurately capture long-range \(LR\) interactions, leading current approaches to rely on explicit physics-based terms or components. In this work, we propose AllScAIP, a straightforward, attention-based, and energy-conserving MLIP model that scales to O\(100 million\) training samples. It addresses the long-range challenge using an all-to-all node attention component that is data-driven. Extensive ablations reveal that in low-data/small-model regimes, inductive biases improve sample efficiency. However, as data and model size scale, these benefits diminish or even reverse, while all-to-all attention remains critical for capturing LR interactions. Our model achieves state-of-the-art energy/force accuracy on molecular systems, as well as a number of physics-based evaluations \(OMol25\), while being competitive on materials \(OMat24\) and catalysts \(OC20\). Furthermore, it enables stable, long-timescale MD simulations that accurately recover experimental observables, including density and heat of vaporization predictions.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
