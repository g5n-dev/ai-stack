---
title: 'ASMR-Bench: Auditing for Sabotage in ML Research'
date: 2026-04-20 23:05:01+08:00
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
external_url: https://arxiv.org/abs/2604.16286v1
aliases:
- /posts/20260421-arxiv_ai-asmr-bench-auditing-for-sabotage-in-ml-research-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a497c769d9f6c90510ac55640760f4cd46cbe70cec1a79d07b6624d6759a423a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:29:16.028975Z'
source_capture_sha256: sha256:a21360657f731e6c61e70a51521c836a49cdcb7777d69e317f1dee4177948da4
source_capture_chars_original: 1146
source_publication_excerpt_chars: 1146
observation_id: obs_fb92feae50bb1618865c26f6c6fd703d000086efaf9d18c7f1ce1d6234a18b92
revision_id: rev_0aa2b5fc6a00a2469fd90187248fbc54b9ac7e5d36cacb1d20baa989905e91dc
event_id: evt_a097aeb63af0dc93d4d8a693f08e1b38b2f63e47494d1d71102fae3e77674114
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-20T03:34:18Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.16286v1](<https://arxiv.org/abs/2604.16286v1>)
- **作者**: Eric Gan, Aryan Bhatt, Buck Shlegeris, Julian Stastny, Vivek Hebbar
- **分类**: cs.AI
- **论文时间**: 2026-04-17T17:47:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.16286v1.pdf](<https://arxiv.org/pdf/2604.16286v1.pdf>)

## 来源摘要/节选

> As AI systems are increasingly used to conduct research autonomously, misaligned systems could introduce subtle flaws that produce misleading results while evading detection. We introduce ASMR-Bench \(Auditing for Sabotage in ML Research\), a benchmark for evaluating the ability of auditors to detect sabotage in ML research codebases. ASMR-Bench consists of 9 ML research codebases with sabotaged variants that produce qualitatively different experimental results. Each sabotage modifies implementation details, such as hyperparameters, training data, or evaluation code, while preserving the high-level methodology described in the paper. We evaluated frontier LLMs and LLM-assisted human auditors on ASMR-Bench and found that both struggled to reliably detect sabotage: the best performance was an AUROC of 0.77 and a top-1 fix rate of 42%, achieved by Gemini 3.1 Pro. We also tested LLMs as red teamers and found that LLM-generated sabotages were weaker than human-generated ones but still sometimes evaded same-capability LLM auditors. We release ASMR-Bench to support research on monitoring and auditing techniques for AI-conducted research.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
