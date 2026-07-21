---
title: Sink-Aware Pruning for Diffusion Language Models
date: 2026-02-20 22:59:37+08:00
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
external_url: https://arxiv.org/abs/2602.17664v1
aliases:
- /posts/20260221-arxiv_ai-sink-aware-pruning-for-diffusion-language-models-0/
- /posts/20260222-arxiv_ai-sink-aware-pruning-for-diffusion-language-models-0/
- /posts/20260223-arxiv_ai-sink-aware-pruning-for-diffusion-language-models-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:3306f33da9d00bc15ec342ec4c1f9bd5c62f7b52edd549d00f7266a5d90259ab
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:16:19.911759Z'
source_capture_sha256: sha256:c99aa7b1dc1dca848cb2dbbae94c904ba38652500467468329b1018fa66b8e93
source_capture_chars_original: 1011
source_publication_excerpt_chars: 1011
observation_id: obs_45f9b3e98b29b3ddcad8904f78030ca201c242b10851a3754452f7d371650e80
revision_id: rev_c7a1d9ce97ec711cf35f5083bd19fbadb1c1f5864188afee3ab48d9ae450e2eb
event_id: evt_8e7e65e72a174af50bb11385e3a3f911716cc86931c9a9eb52a4c5d2356e0a27
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-20T03:54:51Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.17664v1](<https://arxiv.org/abs/2602.17664v1>)
- **作者**: Aidar Myrzakhan, Tianyi Li, Bowei Guo, Shengkun Tang, Zhiqiang Shen
- **分类**: cs.CL
- **论文时间**: 2026-02-19T18:59:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.17664v1.pdf](<https://arxiv.org/pdf/2602.17664v1.pdf>)

## 来源摘要/节选

> Diffusion Language Models \(DLMs\) incur high inference cost due to iterative denoising, motivating efficient pruning. Existing pruning heuristics largely inherited from autoregressive \(AR\) LLMs, typically preserve attention sink tokens because AR sinks serve as stable global anchors. We show that this assumption does not hold for DLMs: the attention-sink position exhibits substantially higher variance over the full generation trajectory \(measured by how the dominant sink locations shift across timesteps\), indicating that sinks are often transient and less structurally essential than in AR models. Based on this observation, we propose $\{\\bf \\texttt\{Sink-Aware Pruning&#125;&#125;$, which automatically identifies and prunes unstable sinks in DLMs \(prior studies usually keep sinks for AR LLMs\). Without retraining, our method achieves a better quality-efficiency trade-off and outperforms strong prior pruning baselines under matched compute. Our code is available at https://github.com/VILA-Lab/Sink-Aware-Pruning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
