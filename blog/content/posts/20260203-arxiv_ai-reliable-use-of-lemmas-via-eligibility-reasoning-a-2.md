---
title: Reliable Use of Lemmas via Eligibility Reasoning and Section$-$Aware Reinforcement
  Learning
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
external_url: https://arxiv.org/abs/2602.00998v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2f13440d268ba6f9923b14040fb88003fcf8cb3e1f5cf31b9baf9d017c30c76d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
captured_at: '2026-07-18T04:10:30.388786Z'
source_capture_sha256: sha256:5e894d625b1ca882d235a93e86292928bfa96a1dae3617629b7b978d75843826
source_capture_chars_original: 1204
source_publication_excerpt_chars: 1204
observation_id: obs_37c6d935715b7ba7c38fe0b950c77bb1d99e1d0440ae9419bc44bdff86664899
revision_id: rev_4ca1dc9a734cec181caebd2f34cbfca560ba41e200a906412fac4494bfef3252
event_id: evt_5d2c28a5b441ed16e1c50f2e33c68406161736e372ebb999597ef3f5c9b57093
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.00998v1](<https://arxiv.org/abs/2602.00998v1>)
- **作者**: Zhikun Xu, Xiaodong Yu, Ben Zhou, Jiang Liu, Jialian Wu, Ze Wang, Ximeng Sun, Hao Chen, Zicheng Liu
- **分类**: cs.CL
- **论文时间**: 2026-02-01T03:34:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.00998v1.pdf](<https://arxiv.org/pdf/2602.00998v1.pdf>)

## 来源摘要/节选

> Recent large language models \(LLMs\) perform strongly on mathematical benchmarks yet often misapply lemmas, importing conclusions without validating assumptions. We formalize lemma$-$judging as a structured prediction task: given a statement and a candidate lemma, the model must output a precondition check and a conclusion$-$utility check, from which a usefulness decision is derived. We present RULES, which encodes this specification via a two$-$section output and trains with reinforcement learning plus section$-$aware loss masking to assign penalty to the section responsible for errors. Training and evaluation draw on diverse natural language and formal proof corpora; robustness is assessed with a held$-$out perturbation suite; and end$-$to$-$end evaluation spans competition$-$style, perturbation$-$aligned, and theorem$-$based problems across various LLMs. Results show consistent in$-$domain gains over both a vanilla model and a single$-$label RL baseline, larger improvements on applicability$-$breaking perturbations, and parity or modest gains on end$-$to$-$end tasks; ablations indicate that the two$-$section outputs and section$-$aware reinforcement are both necessary for robustness.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
