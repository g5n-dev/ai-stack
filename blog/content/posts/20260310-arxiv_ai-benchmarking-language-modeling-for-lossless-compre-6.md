---
title: Benchmarking Language Modeling for Lossless Compression of Full-Fidelity Audio
date: 2026-03-10 23:05:53+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.08683v1
aliases:
- /posts/20260311-arxiv_ai-benchmarking-language-modeling-for-lossless-compre-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1509414632e89c7f187e0da547d2a557d377fac41207b0f76ef63405f89ec135
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:27:31.441787Z'
source_capture_sha256: sha256:b493ad8127c1bf89e89320dbfae6f2158d0a0c2cd36db8f7c9c00bea6d3e8dbd
source_capture_chars_original: 975
source_publication_excerpt_chars: 975
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08683v1](<https://arxiv.org/abs/2603.08683v1>)
- **作者**: Phillip Long, Zachary Novack, Chris Donahue
- **分类**: cs.SD
- **论文时间**: 2026-03-09T17:52:02Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08683v1.pdf](<https://arxiv.org/pdf/2603.08683v1.pdf>)

## 来源摘要/节选

> Autoregressive "language" models \(LMs\) trained on raw waveforms can be repurposed for lossless audio compression, but prior work is limited to 8-bit audio, leaving open whether such approaches work for practical settings \(16/24-bit\) and can compete with existing codecs. We benchmark LM-based compression on full-fidelity audio across diverse domains \(music, speech, bioacoustics\), sampling rates \(16kHz-48kHz\), and bit depths \(8, 16, 24-bit\). Standard sample-level tokenization becomes intractable at higher bit depths due to vocabulary size \(65K for 16-bit; 16.7M for 24-bit\). We propose Trilobyte, a byte-level tokenization schema for full resolution audio, improving vocabulary scaling from $O\(2^\{b\}\)$ to $O\(1\)$ and enabling the first tractable 24-bit LM-based lossless compression. While LMs consistently outperform FLAC and yield state-of-the-art compression at 8-bit and 16-bit, we observe that compression gains become more modest as bit depth increases beyond 8-bit.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
