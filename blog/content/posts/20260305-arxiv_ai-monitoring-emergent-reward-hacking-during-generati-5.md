---
title: Monitoring Emergent Reward Hacking During Generation via Internal Activations
date: 2026-03-05 02:41:37+08:00
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
external_url: https://arxiv.org/abs/2603.04069v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b55626afd9c36a2c2bbf6405bd2484a85dfbcb72174c98ecb6a01ba45ab1f916
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:27:05.167132Z'
source_capture_sha256: sha256:da84a61c85c4376e533b0ef0b669d24c5f714e0bf3bec8dc44d867517f1beabc
source_capture_chars_original: 1390
source_publication_excerpt_chars: 1390
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.04069v1](<https://arxiv.org/abs/2603.04069v1>)
- **作者**: Patrick Wilhelm, Thorsten Wittkopp, Odej Kao
- **分类**: cs.CL
- **论文时间**: 2026-03-04T13:44:24Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.04069v1.pdf](<https://arxiv.org/pdf/2603.04069v1.pdf>)

## 来源摘要/节选

> Fine-tuned large language models can exhibit reward-hacking behavior arising from emergent misalignment, which is difficult to detect from final outputs alone. While prior work has studied reward hacking at the level of completed responses, it remains unclear whether such behavior can be identified during generation. We propose an activation-based monitoring approach that detects reward-hacking signals from internal representations as a model generates its response. Our method trains sparse autoencoders on residual stream activations and applies lightweight linear classifiers to produce token-level estimates of reward-hacking activity. Across multiple model families and fine-tuning mixtures, we find that internal activation patterns reliably distinguish reward-hacking from benign behavior, generalize to unseen mixed-policy adapters, and exhibit model-dependent temporal structure during chain-of-thought reasoning. Notably, reward-hacking signals often emerge early, persist throughout reasoning, and can be amplified by increased test-time compute in the form of chain-of-thought prompting under weakly specified reward objectives. These results suggest that internal activation monitoring provides a complementary and earlier signal of emergent misalignment than output-based evaluation, supporting more robust post-deployment safety monitoring for fine-tuned language models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
