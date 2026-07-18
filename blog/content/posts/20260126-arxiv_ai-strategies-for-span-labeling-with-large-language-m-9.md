---
title: Strategies for Span Labeling with Large Language Models
date: 2026-01-26 22:15:20+08:00
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
external_url: https://arxiv.org/abs/2601.16946v1
aliases:
- /posts/20260127-arxiv_ai-strategies-for-span-labeling-with-large-language-m-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4c36268b2599f8f3994487f24c8471498e830bf36212e16ec8be4108c718c80b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
captured_at: '2026-07-18T04:09:07.673472Z'
source_capture_sha256: sha256:fd19438244acaed68a3a0afd4cf5a55546a5480d999e843c260fe533f90c3e4c
source_capture_chars_original: 946
source_publication_excerpt_chars: 946
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16946v1](<https://arxiv.org/abs/2601.16946v1>)
- **作者**: Danil Semin, Ondřej Dušek, Zdeněk Kasner
- **分类**: cs.CL
- **论文时间**: 2026-01-23T18:03:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16946v1.pdf](<https://arxiv.org/pdf/2601.16946v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) are increasingly used for text analysis tasks, such as named entity recognition or error detection. Unlike encoder-based models, however, generative architectures lack an explicit mechanism to refer to specific parts of their input. This leads to a variety of ad-hoc prompting strategies for span labeling, often with inconsistent results. In this paper, we categorize these strategies into three families: tagging the input text, indexing numerical positions of spans, and matching span content. To address the limitations of content matching, we introduce LogitMatch, a new constrained decoding method that forces the model's output to align with valid input spans. We evaluate all methods across four diverse tasks. We find that while tagging remains a robust baseline, LogitMatch improves upon competitive matching-based methods by eliminating span matching issues and outperforms other strategies in some setups.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
