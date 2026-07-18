---
title: 'Character as a Latent Variable in Large Language Models: A Mechanistic Account
  of Emergent Misalignment and Conditional Safety Failures'
date: 2026-02-02 02:57:13+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
- AI 安全
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.23081v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:30879b5d8d48c644d9c6f281bcf251348304006b3703bce824d9a33aa13ce481
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 135
captured_at: '2026-07-18T04:10:04.354932Z'
source_capture_sha256: sha256:18cd91b40ae8d0ac888274b06152b67d8a8f50f3a9d34cf4e898a2d4c994d6e4
source_capture_chars_original: 1231
source_publication_excerpt_chars: 1231
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23081v1](<https://arxiv.org/abs/2601.23081v1>)
- **作者**: Yanghao Su, Wenbo Zhou, Tianwei Zhang, Qiu Han, Weiming Zhang, Nenghai Yu, Jie Zhang
- **分类**: cs.CL
- **论文时间**: 2026-01-30T15:28:42Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23081v1.pdf](<https://arxiv.org/pdf/2601.23081v1.pdf>)

## 来源摘要/节选

> Emergent Misalignment refers to a failure mode in which fine-tuning large language models \(LLMs\) on narrowly scoped data induces broadly misaligned behavior. Prior explanations mainly attribute this phenomenon to the generalization of erroneous or unsafe content. In this work, we show that this view is incomplete. Across multiple domains and model families, we find that fine-tuning models on data exhibiting specific character-level dispositions induces substantially stronger and more transferable misalignment than incorrect-advice fine-tuning, while largely preserving general capabilities. This indicates that emergent misalignment arises from stable shifts in model behavior rather than from capability degradation or corrupted knowledge. We further show that such behavioral dispositions can be conditionally activated by both training-time triggers and inference-time persona-aligned prompts, revealing shared structure across emergent misalignment, backdoor activation, and jailbreak susceptibility. Overall, our results identify character formation as a central and underexplored alignment risk, suggesting that robust alignment must address behavioral dispositions rather than isolated errors or prompt-level defenses.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
