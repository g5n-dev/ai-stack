---
title: Rethinking Diffusion Models with Symmetries through Canonicalization with Applications
  to Molecular Graph Generation
date: 2026-02-17 22:35:47+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15022v1
aliases:
- /posts/20260218-arxiv_ai-rethinking-diffusion-models-with-symmetries-throug-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:85fd6de48588b452e77fb6fe518f5ecb83b949ba3b455b0731e0748d89ca6613
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 116
captured_at: '2026-07-18T04:15:48.934783Z'
source_capture_sha256: sha256:35338b209dd2241561cc4bb0e2c54202cda0017ea3030d8b2cd4b0fd98d18e9b
source_capture_chars_original: 1694
source_publication_excerpt_chars: 1694
observation_id: obs_c419c48ec6967700aa8935555d22a927492fe164b46f516b2e7ec9f5f6dabce3
revision_id: rev_8e7548a1abd1205d92ce74716f147f005c0a7532a89a2d5a71c4d3c3ef1eee02
event_id: evt_8a2128a291ba10c1ead837a01fc2cf63c01cb359be3a3139cc9d21dde21ec6e9
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15022v1](<https://arxiv.org/abs/2602.15022v1>)
- **作者**: Cai Zhou, Zijie Chen, Zian Li, Jike Wang, Kaiyi Jiang, Pan Li, Rose Yu, Muhan Zhang, Stephen Bates, Tommi Jaakkola
- **分类**: cs.LG
- **论文时间**: 2026-02-16T18:58:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15022v1.pdf](<https://arxiv.org/pdf/2602.15022v1.pdf>)

## 来源摘要/节选

> Many generative tasks in chemistry and science involve distributions invariant to group symmetries \(e.g., permutation and rotation\). A common strategy enforces invariance and equivariance through architectural constraints such as equivariant denoisers and invariant priors. In this paper, we challenge this tradition through the alternative canonicalization perspective: first map each sample to an orbit representative with a canonical pose or order, train an unconstrained \(non-equivariant\) diffusion or flow model on the canonical slice, and finally recover the invariant distribution by sampling a random symmetry transform at generation time. Building on a formal quotient-space perspective, our work provides a comprehensive theory of canonical diffusion by proving: \(i\) the correctness, universality and superior expressivity of canonical generative models over invariant targets; \(ii\) canonicalization accelerates training by removing diffusion score complexity induced by group mixtures and reducing conditional variance in flow matching. We then show that aligned priors and optimal transport act complementarily with canonicalization and further improves training efficiency. We instantiate the framework for molecular graph generation under $S\_n \\times SE\(3\)$ symmetries. By leveraging geometric spectra-based canonicalization and mild positional encodings, canonical diffusion significantly outperforms equivariant baselines in 3D molecule generation tasks, with similar or even less computation. Moreover, with a novel architecture Canon, CanonFlow achieves state-of-the-art performance on the challenging GEOM-DRUG dataset, and the advantage remains large in few-step generation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
