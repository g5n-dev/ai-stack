---
title: Pushing the Frontier of Black-Box LVLM Attacks via Fine-Grained Detail Targeting
date: 2026-02-20 22:59:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.17645v1
aliases:
- /posts/20260221-arxiv_ai-pushing-the-frontier-of-black-box-lvlm-attacks-via-7/
- /posts/20260222-arxiv_ai-pushing-the-frontier-of-black-box-lvlm-attacks-via-7/
- /posts/20260223-arxiv_ai-pushing-the-frontier-of-black-box-lvlm-attacks-via-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9bda6a61e4e33bc95af2f65b32797b6b94ae53befc025b9dd81ef51e23b1dfee
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:16:19.911759Z'
source_capture_sha256: sha256:561b7f323e43b0711734773f7255fe2bc0e307356a1dfe1e248f5a161902f9b0
source_capture_chars_original: 1705
source_publication_excerpt_chars: 1705
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.17645v1](<https://arxiv.org/abs/2602.17645v1>)
- **作者**: Xiaohan Zhao, Zhaoyi Li, Yaxin Luo, Jiacheng Cui, Zhiqiang Shen
- **分类**: cs.LG
- **论文时间**: 2026-02-19T18:54:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.17645v1.pdf](<https://arxiv.org/pdf/2602.17645v1.pdf>)

## 来源摘要/节选

> Black-box adversarial attacks on Large Vision-Language Models \(LVLMs\) are challenging due to missing gradients and complex multimodal boundaries. While prior state-of-the-art transfer-based approaches like M-Attack perform well using local crop-level matching between source and target images, we find this induces high-variance, nearly orthogonal gradients across iterations, violating coherent local alignment and destabilizing optimization. We attribute this to \(i\) ViT translation sensitivity that yields spike-like gradients and \(ii\) structural asymmetry between source and target crops. We reformulate local matching as an asymmetric expectation over source transformations and target semantics, and build a gradient-denoising upgrade to M-Attack. On the source side, Multi-Crop Alignment \(MCA\) averages gradients from multiple independently sampled local views per iteration to reduce variance. On the target side, Auxiliary Target Alignment \(ATA\) replaces aggressive target augmentation with a small auxiliary set from a semantically correlated distribution, producing a smoother, lower-variance target manifold. We further reinterpret momentum as Patch Momentum, replaying historical crop gradients; combined with a refined patch-size ensemble \(PE+\), this strengthens transferable directions. Together these modules form M-Attack-V2, a simple, modular enhancement over M-Attack that substantially improves transfer-based black-box attacks on frontier LVLMs: boosting success rates on Claude-4.0 from 8% to 30%, Gemini-2.5-Pro from 83% to 97%, and GPT-5 from 98% to 100%, outperforming prior black-box LVLM attacks. Code and data are publicly available at: https://github.com/vila-lab/M-Attack-V2.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
