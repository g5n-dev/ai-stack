---
title: "AV-AIVAT: 74x Cheaper Agent Evaluation with Certified Anytime-Valid Stopping in Imperfect-Information Games"
date: 2026-08-07T18:12:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.GT", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:46c1acf274935d47d858d28834d86a85c1a595083ec0211b845cc102c04d19ac"
source_payload_sha256: "sha256:7eadec463fa871dc3c9f930d5c95b1d92258efec96f0592d41e92f5013a029a4"
observation_id: obs_9a329caf0ae8fa25feda9b1d23a3268bee5b2e31e46b7d31a95b50c497d91e80
event_id: evt_9119cf0fb233b2262f34c649098f2f07df548382697b84efa5616b7e0d0bbb42
revision_id: rev_4fc496f40fed7aef5601e361775de3d998f7a6509e11aa429d0ea925ed9054f4
source_published_at: 2026-08-06T17:57:11Z
first_seen_at: 2026-08-07T10:10:10.537434Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 107
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.06362v1
parent_observation_id: null
last_seen_at: 2026-08-07T10:10:10.537434Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06362v1](http://arxiv.org/abs/2608.06362v1)
- **发布域名**: arxiv.org
- **分类**: cs.GT
- **作者**: Boning Li、Yu Chen、Longbo Huang

## 来源摘要/节选

> Deciding which of two agents is stronger means playing games until skill outweighs luck, and every game costs money, model inference, or expert time. Since the number of games needed is unknown, fixed-budget evaluations either keep paying after the result is settled or stop before the agents can be told apart, while naive optional stopping with an ordinary confidence interval invalidates the stated level. We make such an evaluation stop as soon as its evidence suffices, with the guarantee intact. The Action-Informed Value Assessment Tool (AIVAT) reduces variance in imperfect-information games through conditional mean-zero corrections, by a median $54\times$ across 15 LLM agent configurations spanning 71,439 paired Heads-Up No-Limit Hold'em (HUNL) hands, but does not say when to stop. We combine AIVAT with continuously monitored Confidence Sequences (CSs) into anytime-valid AIVAT (AV-AIVAT), whose online value model learns only from past games so that no game scores its own correction. At the nominal 95\% level and a target precision of $\pm1$ Big Blind, raw outcomes need a median $74\times$ as many hands as AIVAT-corrected outcomes to stop under the Asymptotic CS (AsympCS). Exact finite-sample certification uses the Empirical-Bernstein CS (EB-CS), which needs an independently justified bound on corrected payoffs. We establish such a bound structurally for Leduc hold'em and characterize a width floor set by the CS's bet cap and that bound, which governs how much of a variance gain becomes earlier stopping; the descriptive HUNL EB-CS runs show a median $1.37\times$ stopping-time ratio. AV-AIVAT turns variance reduction into efficient, auditable early stopping while separating asymptotic screening from exact certification, so an evaluation can stop the moment its evidence suffices and hand a third party everything needed to recheck the verdict at that very stopping time.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。