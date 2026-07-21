---
title: 'The Geometry of Noise: Why Diffusion Models Don''t Need Noise Conditioning'
date: 2026-02-23 22:40:51+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.18428v1
aliases:
- /posts/20260224-arxiv_ai-the-geometry-of-noise-why-diffusion-models-dont-ne-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:dee8894c1c8f79b3badd98c04be9fb6740d872ccca1ecf3d1e1b5de48dd5461f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
captured_at: '2026-07-18T04:16:23.555947Z'
source_capture_sha256: sha256:918c9f67f0e060d0f256b1d77e7e989abb935519b893f2b76d52bb4c4bc3c967
source_capture_chars_original: 1911
source_publication_excerpt_chars: 1911
observation_id: obs_9e1cec03eac6ef542b7376362bd44e8bd37009e8def33f5a985ec5e8b5aac2fb
revision_id: rev_a2711fb411cde73d4204676c9ecc3434bb7f3804d021d1ee4b319e161d2cc8a7
event_id: evt_2b25576c22e4042406e4f36c91b87c2a9d93ae1d36820b077358ec16eb8ca8af
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-23T03:53:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.18428v1](<https://arxiv.org/abs/2602.18428v1>)
- **作者**: Mojtaba Sahraee-Ardakan, Mauricio Delbracio, Peyman Milanfar
- **分类**: cs.LG
- **论文时间**: 2026-02-20T18:49:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.18428v1.pdf](<https://arxiv.org/pdf/2602.18428v1.pdf>)

## 来源摘要/节选

> Autonomous \(noise-agnostic\) generative models, such as Equilibrium Matching and blind diffusion, challenge the standard paradigm by learning a single, time-invariant vector field that operates without explicit noise-level conditioning. While recent work suggests that high-dimensional concentration allows these models to implicitly estimate noise levels from corrupted observations, a fundamental paradox remains: what is the underlying landscape being optimized when the noise level is treated as a random variable, and how can a bounded, noise-agnostic network remain stable near the data manifold where gradients typically diverge? We resolve this paradox by formalizing Marginal Energy, $E\_\{\\text\{marg&#125;&#125;\(\\mathbf\{u\}\) = -\\log p\(\\mathbf\{u\}\)$, where $p\(\\mathbf\{u\}\) = \\int p\(\\mathbf\{u\}|t\)p\(t\)dt$ is the marginal density of the noisy data integrated over a prior distribution of unknown noise levels. We prove that generation using autonomous models is not merely blind denoising, but a specific form of Riemannian gradient flow on this Marginal Energy. Through a novel relative energy decomposition, we demonstrate that while the raw Marginal Energy landscape possesses a $1/t^p$ singularity normal to the data manifold, the learned time-invariant field implicitly incorporates a local conformal metric that perfectly counteracts the geometric singularity, converting an infinitely deep potential well into a stable attractor. We also establish the structural stability conditions for sampling with autonomous models. We identify a \`\`Jensen Gap'' in noise-prediction parameterizations that acts as a high-gain amplifier for estimation errors, explaining the catastrophic failure observed in deterministic blind models. Conversely, we prove that velocity-based parameterizations are inherently stable because they satisfy a bounded-gain condition that absorbs posterior uncertainty into a smooth geometric drift.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
