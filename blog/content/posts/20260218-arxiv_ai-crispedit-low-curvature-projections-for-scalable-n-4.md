---
title: 'CrispEdit: Low-Curvature Projections for Scalable Non-Destructive LLM Editing'
date: 2026-02-18 21:10:38+08:00
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
external_url: https://arxiv.org/abs/2602.15823v1
aliases:
- /posts/20260219-arxiv_ai-crispedit-low-curvature-projections-for-scalable-n-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:95116b339f853aff35e14d49c10dd139157b63f00ed80ce883298ea568fde0c9
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:15:52.664467Z'
source_capture_sha256: sha256:ea94fb68cf0c50704530c53fe46cc3b6e65fd250f1c863cda9587f4b0e16f1af
source_capture_chars_original: 1296
source_publication_excerpt_chars: 1296
observation_id: obs_b64e9b07c88d3100fb6782f17cda4e53d93b3d0d38056b374a7bdd693ee9bc71
revision_id: rev_e5805d105ca3fbfe0241745a8d6ce9353f5631a856eb50a212521059aa27cb46
event_id: evt_7b470626d2f3213130cc7b87fe6858f03bf172734188651fe3a9af7c57b971d9
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-18T03:49:38Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15823v1](<https://arxiv.org/abs/2602.15823v1>)
- **作者**: Zarif Ikram, Arad Firouzkouhi, Stephen Tu, Mahdi Soltanolkotabi, Paria Rashidinejad
- **分类**: cs.LG
- **论文时间**: 2026-02-17T18:58:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15823v1.pdf](<https://arxiv.org/pdf/2602.15823v1.pdf>)

## 来源摘要/节选

> A central challenge in large language model \(LLM\) editing is capability preservation: methods that successfully change targeted behavior can quietly game the editing proxy and corrupt general capabilities, producing degenerate behaviors reminiscent of proxy/reward hacking. We present CrispEdit, a scalable and principled second-order editing algorithm that treats capability preservation as an explicit constraint, unifying and generalizing several existing editing approaches. CrispEdit formulates editing as constrained optimization and enforces the constraint by projecting edit updates onto the low-curvature subspace of the capability-loss landscape. At the crux of CrispEdit is expressing capability constraint via Bregman divergence, whose quadratic form yields the Gauss-Newton Hessian exactly and even when the base model is not trained to convergence. We make this second-order procedure efficient at the LLM scale using Kronecker-factored approximate curvature \(K-FAC\) and a novel matrix-free projector that exploits Kronecker structure to avoid constructing massive projection matrices. Across standard model-editing benchmarks, CrispEdit achieves high edit success while keeping capability degradation below 1% on average across datasets, significantly improving over prior editors.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
