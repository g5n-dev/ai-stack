---
title: "Sketching Language Models for Context Attribution"
date: 2026-11-15T09:54:54+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.DS", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:db8e3b74c3928ba445cb336a49f81dc09032a02d6b9dd525983a896736449b8f"
source_payload_sha256: "sha256:0578621657121b95069cdc7738a4835b521862ccaa9de35a5a6d9d7c1a3fb0e6"
observation_id: obs_b4bd2b3d3086544b7a49e9a20b99c089921bf4d769234974456f02617288d8e5
event_id: evt_cc35f2055265cec5c87c995ac7fdd0cf1c69771137e8d31f5ce8eefc016dcc30
revision_id: rev_223c831e1be2cfb8ce178428743f7ffdc283949868a40c2712b10c5ba4309e48
source_published_at: 2026-11-12T18:57:48Z
first_seen_at: 2026-11-15T01:53:42.120665Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
interpretation_sha256: "sha256:a0fe3bd46dd75041b2ad01e38139c10bfde7f76a60360ddb0cc3b6c1f817b0d8"
description: "这篇论文研究如何高效计算语言模型提示中各部分对输出的 leave-one-out（LOO）归因值。在稳定性假设下，算法用 sketching 估计所有归因值，并给出匹配的查询次数下界。"
external_url: http://arxiv.org/abs/2611.17313v1
parent_observation_id: null
last_seen_at: 2026-11-15T01:53:42.120665Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.17313v1](http://arxiv.org/abs/2611.17313v1)
- **发布域名**: arxiv.org
- **分类**: cs.DS
- **作者**: Christopher Liaw、Aranyak Mehta、Grigoris Velegkas 等

## 要点解读

### 这是什么
这篇论文研究如何高效计算语言模型提示中各部分对输出的 leave-one-out（LOO）归因值。在稳定性假设下，算法用 sketching 估计所有归因值，并给出匹配的查询次数下界。

### 用在哪里
它适用于需要判断提示中哪些 token 或片段影响模型输出的场景，例如提示归因、模型行为分析或检索任务中的贡献度评估。研究语言模型可解释性、归因算法与 sketch 技术的读者可能会关注。

### 可以推断的
- 推测：在需要同时分析大量提示片段时，sketching 方法可能比逐一移除并重新评估更节省模型调用。
- 推测：该方法的关键价值不只在计算效率，也在于论文同时给出了理论上匹配的下界，便于判断改进空间。

## 来源摘要/节选

> Context attribution asks how removing parts of a prompt changes a language model's output. We study leave-one-out (LOO) attribution for a prompt of $n$ tokens and a fixed measurement function. Computing all LOO values directly requires $n$ model evaluations. Under a stability assumption, our algorithm estimates all LOO values to error proportional to $\varepsilon$ with constant probability using $O(\sqrt{\log(1/\varepsilon)}/\varepsilon)$ evaluation calls. To complement our upper bound, we prove a matching $Ω(\sqrt{\log(1/\varepsilon)}/\varepsilon)$ lower bound on the number of evaluation calls in an oracle model. Empirically, we verify coefficient decay consistent with stability and evaluate the performance of our sketching algorithm on a small language-model retrieval task.
> Technically, our result is based on a sketching algorithm for arithmetic circuits whose Taylor coefficients satisfy the stability condition recently introduced by Gunn [Gun26]. A direct adaptation of their forward differentiation sketches would require $\widetilde{O}(\log(n)/\varepsilon^2)$ evaluation calls. Our key observation is that we can apply forward differentiation to the backpropagation circuit, with only constant overhead over a forward sketch of the same Taylor degree. This reduces the variance of the sketches and is key to our improved evaluation bound. Our lower bound builds on the techniques of Amsel, Chen, Duman Keles, Halikias, Musco, and Musco [ACDH+26, SIAM Journal on Matrix Analysis and Applications] for lower bounding the number of matrix-vector queries to estimate the diagonal elements of random matrices.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。