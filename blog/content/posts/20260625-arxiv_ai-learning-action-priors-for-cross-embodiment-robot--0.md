---
title: Learning Action Priors for Cross-embodiment Robot Manipulation
date: 2026-06-25 23:42:10+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.26095v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2a5d0efcd9567d8c89d1b54c2054d15bff28692a69b336da2fbf49a49756498b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
captured_at: '2026-07-18T04:30:14.398876Z'
source_capture_sha256: sha256:eed0568165925873d21c7a10c892018ed07e579197e6bdb25cf43d4931d7f36f
source_capture_chars_original: 1915
source_publication_excerpt_chars: 1915
observation_id: obs_56b63530c20f5755479a4b2244e073d0ae9a6db172e18c726c6df69fe643e7aa
revision_id: rev_a37abcff7be0cdd20f9f35636d5f65f43fb0b449b455784ac654a89f900d865c
event_id: evt_689f9e2f90cb59d23b91fee9ebd861531a235f39b9e7e364b14cd9f9e7549528
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-25T09:02:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.26095v1](<https://arxiv.org/abs/2606.26095v1>)
- **作者**: Dong Jing, Tianqi Zhang, Jiaqi Liu, Jinman Zhao, Zelong Sun, Li Erran Li, Zhiwu Lu, Mingyu Ding
- **分类**: cs.RO
- **论文时间**: 2026-06-24T17:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.26095v1.pdf](<https://arxiv.org/pdf/2606.26095v1.pdf>)

## 来源摘要/节选

> Most Vision-Language-Action \(VLA\) models build on a Vision-Language Model \(VLM\) backbone by attaching an action module and optimizing the full policy jointly. This design inherits strong visual and linguistic priors from the VLM, but leaves the action module to learn physical motion almost from scratch. As a result, the policy lacks an explicit motion prior, forcing early optimization to simultaneously discover temporal action dynamics and cross-modal alignment, a challenge further amplified in cross-embodiment settings. In this work, we propose to pretrain the action module with motion priors before cross-modal VLA alignment. Specifically, we introduce a two-stage training framework that equips the action module with cross-embodiment temporal motion structure before VLA training begins. In Stage~1, a lightweight flow-matching-based encoder-decoder action module efficiently learns temporal motion structure solely from unconditioned action trajectories, without processing visual or language tokens. In Stage~2, this learned prior is transferred to VLA training through decoder reuse and early-stage latent distillation, aligning visual-language features with the action embedding space while still allowing end-to-end policy refinement. In addition, the trained encoder serves as a compact history compressor, summarizing state-action histories into a single temporal context token for history-aware modeling at negligible cost. Extensive experiments across 13 diverse cross-embodiment tasks on both simulated and real-world platforms validate the effectiveness of our approach. Compared with VLA training without action priors, our model achieves faster convergence, higher success rates, and substantially stronger performance on data-scarce real-world tasks. Moreover, scaling up the action data in Stage~1 yields a more generalizable action prior that directly improves downstream VLA performance.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
