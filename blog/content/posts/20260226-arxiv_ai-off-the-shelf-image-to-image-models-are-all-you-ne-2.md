---
title: Off-The-Shelf Image-to-Image Models Are All You Need To Defeat Image Protection
  Schemes
date: 2026-02-26 23:29:19+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 生成式 AI
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.22197v1
aliases:
- /posts/20260227-arxiv_ai-off-the-shelf-image-to-image-models-are-all-you-ne-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:127bf58a400310d93ae9926dfc2c87542684e4ef5b8a4440de2e5381111c3bb8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:30:29.635417Z'
source_capture_sha256: sha256:ee0d6743a8e00fc737d9dcdcd2407dd1cce62d2aea0101648ca367cc1e8f7b92
source_capture_chars_original: 1271
source_publication_excerpt_chars: 1271
observation_id: obs_69dedf38c673788b2c69671e9cf8ba08c608529c7b3d802a1a3718eb75f36b4d
revision_id: rev_8dcf3f0b9820421665c45196cf5e7db7e14f03a29b2e4424e0dc370df18f1db8
event_id: evt_e01c72be160bbd9f01055eb43f7f38d3c9da9372543e457ecf673761038021a3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.22197v1](<https://arxiv.org/abs/2602.22197v1>)
- **作者**: Xavier Pleimling, Sifat Muhammad Abdullah, Gunjan Balde, Peng Gao, Mainack Mondal, Murtuza Jadliwala, Bimal Viswanath
- **分类**: cs.CV
- **论文时间**: 2026-02-25T18:46:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.22197v1.pdf](<https://arxiv.org/pdf/2602.22197v1.pdf>)

## 来源摘要/节选

> Advances in Generative AI \(GenAI\) have led to the development of various protection strategies to prevent the unauthorized use of images. These methods rely on adding imperceptible protective perturbations to images to thwart misuse such as style mimicry or deepfake manipulations. Although previous attacks on these protections required specialized, purpose-built methods, we demonstrate that this is no longer necessary. We show that off-the-shelf image-to-image GenAI models can be repurposed as generic \`\`denoisers" using a simple text prompt, effectively removing a wide range of protective perturbations. Across 8 case studies spanning 6 diverse protection schemes, our general-purpose attack not only circumvents these defenses but also outperforms existing specialized attacks while preserving the image's utility for the adversary. Our findings reveal a critical and widespread vulnerability in the current landscape of image protection, indicating that many schemes provide a false sense of security. We stress the urgent need to develop robust defenses and establish that any future protection mechanism must be benchmarked against attacks from off-the-shelf GenAI models. Code is available in this repository: https://github.com/mlsecviswanath/img2imgdenoiser

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
