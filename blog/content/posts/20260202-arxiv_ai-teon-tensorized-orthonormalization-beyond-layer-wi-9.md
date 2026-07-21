---
title: 'TEON: Tensorized Orthonormalization Beyond Layer-Wise Muon for Large Language
  Model Pre-Training'
date: 2026-02-02 19:22:59+08:00
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
external_url: https://arxiv.org/abs/2601.23261v1
aliases:
- /posts/20260203-arxiv_ai-teon-tensorized-orthonormalization-beyond-layer-wi-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a2ddb325583e2071f31fff6598075a322ad3bb49b49bbd8d37f638f884245ebe
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:10:19.257843Z'
source_capture_sha256: sha256:c89076e9ceb91a45a8af6320230f355ccc422f65889cb9cbfce2e2684570bf4e
source_capture_chars_original: 953
source_publication_excerpt_chars: 953
observation_id: obs_f86fc383902d57ee8fd9e1ad89e415a1c5b9ead673c91c229c90ce133e16ba4c
revision_id: rev_0d3fc8a04cf2b623c36d2af34f6067ae21a74955dc9d17e7a2f2c1f71d03190d
event_id: evt_d9bd498f40dd6cd68b9f4a62fd9d814deb4d857dbc1e5011733bc41ea781cc6c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-02T05:34:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23261v1](<https://arxiv.org/abs/2601.23261v1>)
- **作者**: Ruijie Zhang, Yequan Zhao, Ziyue Liu, Zhengyang Wang, Dongyang Li, Yupeng Su, Sijia Liu, Zheng Zhang
- **分类**: cs.LG
- **论文时间**: 2026-01-30T18:30:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23261v1.pdf](<https://arxiv.org/pdf/2601.23261v1.pdf>)

## 来源摘要/节选

> The Muon optimizer has demonstrated strong empirical performance in pre-training large language models by performing matrix-level gradient \(or momentum\) orthogonalization in each layer independently. In this work, we propose TEON, a principled generalization of Muon that extends orthogonalization beyond individual layers by modeling the gradients of a neural network as a structured higher-order tensor. We present TEON's improved convergence guarantee over layer-wise Muon, and further develop a practical instantiation of TEON based on the theoretical analysis with corresponding ablation. We evaluate our approach on two widely adopted architectures: GPT-style models, ranging from 130M to 774M parameters, and LLaMA-style models, ranging from 60M to 1B parameters. Experimental results show that TEON consistently improves training and validation perplexity across model scales and exhibits strong robustness under various approximate SVD schemes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
