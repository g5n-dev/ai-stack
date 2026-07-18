---
title: Tokenisation via Convex Relaxations
date: 2026-05-22 21:33:49+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 自然语言处理
categories:
- 论文
scenarios:
- AI/ML项目
- 自然语言处理
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.22821v1
aliases:
- /posts/20260523-arxiv_ai-tokenisation-via-convex-relaxations-0/
- /posts/20260524-arxiv_ai-tokenisation-via-convex-relaxations-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c8997c5133152fc9bb10060154325190f2ad895b83db8107d92fbcb27b61e362
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:29:43.284780Z'
source_capture_sha256: sha256:c6141642e9dee7efaaade69ca22b99c209c2aa044302e56f048c5fe77fb74758
source_capture_chars_original: 816
source_publication_excerpt_chars: 816
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.22821v1](<https://arxiv.org/abs/2605.22821v1>)
- **作者**: Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel
- **分类**: cs.CL
- **论文时间**: 2026-05-21T17:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](<https://arxiv.org/pdf/2605.22821v1.pdf>)

## 来源摘要/节选

> Tokenisation is an integral part of the current NLP pipeline. Current tokenisation algorithms such as BPE and Unigram are greedy algorithms -- they make locally optimal decisions without considering the resulting vocabulary as a whole. We instead formulate tokeniser construction as a linear program and solve it using convex optimisation tools, yielding a new algorithm we call ConvexTok. We find ConvexTok consistently improves intrinsic tokenisation metrics and the bits-per-byte \(BpB\) achieved by language models; it also improves downstream task performance, but less consistently. Furthermore, ConvexTok allows the user to certify how far their tokeniser is from optimal, with respect to a certain objective, via a lower bound, and we empirically find it to be within 1\\% of optimal at common vocabulary sizes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
