---
title: 'CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance'
date: 2026-03-04 22:47:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03281v1
aliases:
- /posts/20260305-arxiv_ai-cfg-ctrl-control-based-classifier-free-diffusion-g-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:80f19d337dd3492aa6d48436421de94b27b76b15e44937adc7ffe149e57109dd
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
captured_at: '2026-07-18T04:26:38.668400Z'
source_capture_sha256: sha256:05ca281a866b2334e378a019e0b19853008e3ad85ee8d9e558d9551842b4234b
source_capture_chars_original: 1475
source_publication_excerpt_chars: 1475
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03281v1](<https://arxiv.org/abs/2603.03281v1>)
- **作者**: Hanyang Wang, Yiyang Liu, Jiawei Chi, Fangfu Liu, Ran Xue, Yueqi Duan
- **分类**: cs.CV
- **论文时间**: 2026-03-03T18:59:48Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03281v1.pdf](<https://arxiv.org/pdf/2603.03281v1.pdf>)

## 来源摘要/节选

> Classifier-Free Guidance \(CFG\) has emerged as a central approach for enhancing semantic alignment in flow-based diffusion models. In this paper, we explore a unified framework called CFG-Ctrl, which reinterprets CFG as a control applied to the first-order continuous-time generative flow, using the conditional-unconditional discrepancy as an error signal to adjust the velocity field. From this perspective, we summarize vanilla CFG as a proportional controller \(P-control\) with fixed gain, and typical follow-up variants develop extended control-law designs derived from it. However, existing methods mainly rely on linear control, inherently leading to instability, overshooting, and degraded semantic fidelity especially on large guidance scales. To address this, we introduce Sliding Mode Control CFG \(SMC-CFG\), which enforces the generative flow toward a rapidly convergent sliding manifold. Specifically, we define an exponential sliding mode surface over the semantic prediction error and introduce a switching control term to establish nonlinear feedback-guided correction. Moreover, we provide a Lyapunov stability analysis to theoretically support finite-time convergence. Experiments across text-to-image generation models including Stable Diffusion 3.5, Flux, and Qwen-Image demonstrate that SMC-CFG outperforms standard CFG in semantic alignment and enhances robustness across a wide range of guidance scales. Project Page: https://hanyang-21.github.io/CFG-Ctrl

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
