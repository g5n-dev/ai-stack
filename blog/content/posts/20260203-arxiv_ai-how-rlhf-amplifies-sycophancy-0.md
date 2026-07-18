---
title: How RLHF Amplifies Sycophancy
date: 2026-02-03 03:49:30+08:00
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
external_url: https://arxiv.org/abs/2602.01002v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:de7ab53e98b321cd78aef5a0e1038870dc285addf0820234d8a9b5544b2fc875
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:10:26.671991Z'
source_capture_sha256: sha256:c1c4bf88997e5c2703d19502eda237de08af2ae2f6f5d16269339be6f580b39a
source_capture_chars_original: 1444
source_publication_excerpt_chars: 1444
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.01002v1](<https://arxiv.org/abs/2602.01002v1>)
- **作者**: Itai Shapira, Gerdus Benade, Ariel D. Procaccia
- **分类**: cs.AI
- **论文时间**: 2026-02-01T03:46:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.01002v1.pdf](<https://arxiv.org/pdf/2602.01002v1.pdf>)

## 来源摘要/节选

> Large language models often exhibit increased sycophantic behavior after preference-based post-training, showing a stronger tendency to affirm a user's stated or implied belief even when this conflicts with factual accuracy or sound judgment. We present a formal analysis of how alignment from human feedback can increase this failure mode by identifying an explicit amplification mechanism that causally links optimization against a learned reward to bias in the human preference data used for alignment. We show that the direction of behavioral drift is determined by a covariance under the base policy between endorsing the belief signal in the prompt and the learned reward, and that the first-order effect reduces to a simple mean-gap condition. We then analyze reward learning from pairwise comparisons under random utility models like Bradley-Terry and characterize when bias in human annotators' preferences induces this reward gap. Next, we propose a training-time intervention designed to neutralize the amplification mechanism itself. Among all post-trained policies that prevent sycophantic behavior from increasing, we characterize the unique policy closest in KL divergence to the unconstrained post-trained policy, and derive the corresponding minimal reward correction as a closed-form agreement penalty. Computational experiments find that reward gaps are common and cause behavioral drift in all the configurations considered.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
