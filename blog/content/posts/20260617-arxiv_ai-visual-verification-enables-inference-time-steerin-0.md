---
title: Visual Verification Enables Inference-time Steering and Autonomous Policy Improvement
date: 2026-06-17 23:45:46+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.18247v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:59dce16bafa1d31b3eb72613f81ff77097db38de2723f4e632426225e5afc28f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:30:09.568344Z'
source_capture_sha256: sha256:7445ad8141eda62646ed0c4d106087e6caff15049570067f52c941c945b7f572
source_capture_chars_original: 1234
source_publication_excerpt_chars: 1234
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.18247v1](<https://arxiv.org/abs/2606.18247v1>)
- **作者**: Mingtong Zhang, Dhruv Shah
- **分类**: cs.RO
- **论文时间**: 2026-06-16T17:59:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.18247v1.pdf](<https://arxiv.org/pdf/2606.18247v1.pdf>)

## 来源摘要/节选

> Robots deployed in the real world should learn from their experience and improve over time. This requires a mechanism of practicing and learning from feedback. In this paper, we propose VERITAS, a generator-verifier framework for generalist robot policies for inference-time policy steering and self-improvement. We use a pre-trained generalist robot policy as a \`\`generator'' and pair it with a gradient-free \`\`visual verifier'' that evaluates actions at inference time. This framework enables inference-time steering that improves policy performance without additional training. We demonstrate that inference-time verification consistently outperforms vanilla generalists without training on additional demonstration data. Additionally, we demonstrate that the verified rollouts provide effective supervision for offline policy improvement: policies fine-tuned on verified self-generated trajectories achieve consistent performance gains. Notably, we find that post-training with verified rollouts achieves comparable efficiency to expert demonstrations, while requiring no human interventions. Our results highlight inference-time verification as a practical and scalable mechanism for improving robotic policies during deployment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
