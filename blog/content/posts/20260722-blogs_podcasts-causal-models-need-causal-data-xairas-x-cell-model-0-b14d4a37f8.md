---
title: "🔬Causal Models Need Causal Data - Xaira’s X-Cell model for Drug Discovery (Bo Wang & Ci Chu, Chief Discovery Officer & Chief AI Scientist)"
date: 2026-07-22T20:07:05+08:00
draft: false
entry_kind: "auto"
tags: ["博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d5dc0a7da052c4744536484b6488547ecf234ebbef5912814d9a1a8aee795a6d"
source_payload_sha256: "sha256:421e47e39f37d3841852d9b53c6946ac088af873c3c3eac73e4c9f504d4b4b09"
observation_id: obs_b14d4a37f8759b625bbb314848aaa00fea1017721e9d95430ded81a0058906fa
event_id: evt_337708874bca2e1fe778453d6931ba86cb28cb7d0a732dd08b5ba196d72379a0
revision_id: rev_7770c984a357ea11aeeee97afbb80892c5eb1180484c3b97f8ae0b7d0041dbfe
source_published_at: 2026-07-21T19:34:06Z
first_seen_at: 2026-07-22T12:06:25.098856Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 138
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/xaira
parent_observation_id: null
last_seen_at: 2026-07-22T12:06:25.098856Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/xaira](https://www.latent.space/p/xaira)

## 来源摘要/节选

> Bet on information
>
> If test loss flatlines after 1.5B parameters while training loss continues to drop as you scale, that tells you that your model is limited by the amount of information in your data.
>
> Training on a single, smallish data set exposed an information gap: the 3.1B model falls off the scaling trend. Neither parameters nor compute will improve performance past this wall. For predicting changes to gene expression, you need more information rich data.
>
> This is what Chu and Bo’s teams have done, and here is what ~30x the information buys you:
>
> Now we can scale with parameters and training compute! We don’t know how much this effort costed, but we can guess that data collection experiments and infrastructure was a few tens of millions, and compute + headcount + research was a few million. The budget looks like a RL rollout budget, rather than a data rich pre-training one.
>
> We were lucky enough to have the two central figures in this story on our podcast. Taking the lead from Ci Chu and Bo Wang, Xaira Therapeutics is betting that information rich data is the key to AI-driven drug development. Chu was recently promoted to Chief Discovery Officer and Bo to Chief AI Scientist1, underscoring just how strategic Xaira considers this bet.
>
> Reverse engineering the human cell
>
> If you had to figure out how a human cell works, what would you do? A good place to start might be by documenting what genes are expressed (e.g. what RNA is floating around) in different kinds of cells, in different circumstances.
>
> That is CELLxGENE, a database of 168M cells built by Chan Zuckerberg Institute that maps each cell to a count of how many times 20K-30K genes were detected in that cell, plus detailed metadata about every cell. A ~4 trillion-entry matrix.
>
> If the Protein Data Bank (PDB) unlocked structural biology models (Boltz Episode, ESM/BioHub Episode), CELLxGENE has done the same thing for Virtual Cell models. Like PDB, CELLxGENE has inspired a zoo of AI models of RNA expression; so much so that RNA expression models have become synonymous with Virtual Cell models. Bo Wang built one of the most influential, scGPT, that became the starting point for Xaira’s new model.
>
> RNA expression ≠ Virtual Cell
>
> Models trained on CELLxGENE describe the relationship between cell types and cell states, but they are not good at predicting what will happen if we make changes to RNA expression. Changes in gene expression are highly correlated, and its is difficult (impossible) to figure out what causes what in most cases.
>
> If you could “turn the dial down” on one gene at a time, however, then you would be able to observe what is upstream and downstream of a given gene2. You could tell if A → B &amp; C or B → A &amp; C or B → A, C → B → … If you did this for all of the genes, then maybe you could train a model that could predict what would happen to a cell if you change a gene (e.g. with a drug or a gene edit). Or maybe you could figure out the least invasive way to change a particular gene’s expression.
>
> X-Atlas → X-Cell
>
> This is exactly what Chu and Bo’s teams have done. The data set is called X-Atlas and the model is called X-Cell.
>
> In this episode, we discuss:
>
> Why the team abandoned autoregression for diffusion
>
> The CRISPR-based experiments that run millions of tests in parallel, and generate the raw data for X-Atlas and X-cell
>
> Generalization to real lab experiments in real human cells
>
> Beating the linear baseline that has outperformed previous models
>
> Justifying a kitchen-sink of priors, and how that stacks up vs. data and architecture
>
> Bo also shared with us some of the (major) advantages he has as an academic vs. industry leader, and how his labs keep up with the breakneck pace of AI innovation.
>
> Check out the full episode on YouTube, or your favorite podcasting platform!
>
> 1
>
> These promotions happened after we recorded the episode
>
> 2
>
> There can be cycles in the chain reaction, of course, and there can be second, third, etc. order effects (meaning things that only happen when multiple genes change at once), but the first order effects are a great place to start, and might tell us a lot of what we need to know.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。