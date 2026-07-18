---
title: 'Optimal Turkish Subword Strategies at Scale: Systematic Evaluation of Data,
  Vocabulary, Morphology Interplay'
date: 2026-02-09 23:42:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06942v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:69f641feceb2d8346a39622a6b5b650c5ee82383e2c524d2e696bbd77e7504fc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
captured_at: '2026-07-18T04:11:23.963527Z'
source_capture_sha256: sha256:48b86ff1ff3e33b95b29a6d5a0add090c769b30214e9e06ebfb2bb8aae38452e
source_capture_chars_original: 1917
source_publication_excerpt_chars: 1917
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06942v1](<https://arxiv.org/abs/2602.06942v1>)
- **作者**: Duygu Altinok
- **分类**: cs.CL
- **论文时间**: 2026-02-06T18:41:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06942v1.pdf](<https://arxiv.org/pdf/2602.06942v1.pdf>)

## 来源摘要/节选

> Tokenization is a pivotal design choice for neural language modeling in morphologically rich languages \(MRLs\) such as Turkish, where productive agglutination challenges both vocabulary efficiency and morphological fidelity. Prior studies have explored tokenizer families and vocabulary sizes but typically \(i\) vary vocabulary without systematically controlling the tokenizer's training corpus, \(ii\) provide limited intrinsic diagnostics, and \(iii\) evaluate a narrow slice of downstream tasks. We present the first comprehensive, principled study of Turkish subword tokenization; a "subwords manifest", that jointly varies vocabulary size and tokenizer training corpus size \(data and vocabulary coupling\), compares multiple tokenizer families under matched parameter budgets \(WordPiece, morphology level, and character baselines\), and evaluates across semantic \(NLI, STS, sentiment analysis, NER\), syntactic \(POS, dependency parsing\), and morphology-sensitive probes. To explain why tokenizers succeed or fail, we introduce a morphology-aware diagnostic toolkit that goes beyond coarse aggregates to boundary-level micro/macro F1, decoupled lemma atomicity vs. surface boundary hits, over/under-segmentation indices, character/word edit distances \(CER/WER\), continuation rates, and affix-type coverage and token-level atomicity. Our contributions are fourfold: \(i\) a systematic investigation of the vocabulary-corpus-success triad; \(ii\) a unified, morphology-aware evaluation framework linking intrinsic diagnostics to extrinsic outcomes; \(iii\) controlled comparisons identifying when character-level and morphology-level tokenization pay off; and \(iv\) an open-source release of evaluation code, tokenizer pipelines, and models. As the first work of its kind, this "subwords manifest" delivers actionable guidance for building effective tokenizers in MRLs and establishes a reproducible foundation for future research.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
