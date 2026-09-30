---
title: "A Spectral Theory of Distortion in LLM Graph Reconstruction: Sharp Bounds and Empirical Characterization"
date: 2026-10-01T07:52:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6811b9e9414d646dd5aa8940c35629a863a46a37a9f001630387977f2c1b0ff7"
source_payload_sha256: "sha256:f88b475034882a8a1a888990a9f65911f8a2ef0a14cc4e9aade61f3716f9a301"
observation_id: obs_a2faa0bf7f15f17301c0ecf499d8d439495bcb0c75a59dbbe886c20f72f48033
event_id: evt_c4c42903634d4b7fe9ef0b708b0d85b89639a91cb00dad33df8b03868c168164
revision_id: rev_42ae367980539bbcb2eb6109593167b1ed61069ec348e3d7ee19fa914fa22edf
source_published_at: 2026-09-29T17:59:16Z
first_seen_at: 2026-09-30T23:48:23.935441Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.38161v1
parent_observation_id: null
last_seen_at: 2026-09-30T23:48:23.935441Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.38161v1](http://arxiv.org/abs/2609.38161v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Jianru Shen

## 来源摘要/节选

> Evaluations of graph reconstruction by language models typically report a single aggregate distance between the original and the reconstructed graph. We prove that for the Wasserstein distance between Laplacian spectra such a summary is bracketed by two edge counts, the net change in edge number from below and the symmetric difference from above, each scaled by $2/n$ where $n$ is the number of vertices. The bracket is sharp: its two ends coincide exactly when the reconstruction only adds edges or only deletes them, and on that class the distance is a rescaled edge count that says nothing about which edges changed. When the ends differ, the residual between the distance and the lower end is positive only if the reconstruction both invented and lost edges, which turns it into a certificate of mixed editing computable from the reported summaries alone. We characterize these regimes in 135 reconstructions produced by three open-weight models over 45 synthetic graphs. Seventy-seven outputs are one-sided and 29 mixed outputs have $X &gt; 0$, including cases where edge count is exactly preserved while nineteen edges were simultaneously invented and lost. The three models differ in editing policy, ranging from copying the input to attempting completion at the cost of large hallucination volume, a distinction that aggregate distortion does not reveal.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。