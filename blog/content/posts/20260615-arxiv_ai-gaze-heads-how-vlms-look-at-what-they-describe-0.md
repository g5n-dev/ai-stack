---
title: 'Gaze Heads: How VLMs Look at What They Describe'
date: 2026-06-15 23:58:25+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.14703v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c3df27acb5fceb7952a07a47b8ca258a9e238316fd32051a0062fdc57a8a20fa
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 47
captured_at: '2026-07-18T04:30:02.047374Z'
source_capture_sha256: sha256:4d0112eaff3b48f05662eaa1d7a4f68d9b95287820eef20e51739cdf166812ed
source_capture_chars_original: 1679
source_publication_excerpt_chars: 1679
observation_id: obs_b556c52fa8f71f27b5a6d44556d9e017a3127ec39229a05f420ab1ac483efd58
revision_id: rev_68e2f18a773e25723aabddf7d68b4847a4572753a1c5687689455d4eeb9df4f9
event_id: evt_1cc2ec8738420b8f09a7bd348c6a7aa394003b783ac96c27395910128204f7e9
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-15T07:30:54Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.14703v1](<https://arxiv.org/abs/2606.14703v1>)
- **作者**: Rohit Gandikota, David Bau
- **分类**: cs.CV
- **论文时间**: 2026-06-12T17:59:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.14703v1.pdf](<https://arxiv.org/pdf/2606.14703v1.pdf>)

## 来源摘要/节选

> How a vision-language model internally solves the task of describing an image is far from obvious. We find that the model develops a specific mechanism for this: a small set of attention heads in its language-model backbone, which we call gaze heads, whose attention tracks the image region the model is currently describing. We find them with a simple correlation score from a few forward passes, using comic strips as a controlled testbed where narrative order is laid out spatially. These gaze heads do not just track the image tokens being described: redirecting their attention to a chosen region forces the VLM to describe that region instead. A single attention-mask intervention on the top-100 gaze heads, fewer than 9% of all heads, steers the model's answer to any chosen comic panel at 83.1% accuracy, while the same intervention on random heads fails to redirect the answer, and intervening on all heads destroys generation. The same lever also extends to continuous control: switching the gaze target mid-generation makes the model wrap up its current panel description and move to the new one within a few tokens. Beyond comics, the same intervention redirects answers to chosen regions in natural COCO images. The mechanism further recurs across model sizes from 2B to 32B parameters and across other VLM architectures, although some frozen-encoder families show no comparable head set. More broadly, this shows that targeted edits identified through mechanistic analysis can serve as practical inference-time levers for steering multimodal model behavior, without any retraining. Our code, interactive demo, and datasets are available at https://gaze.baulab.info/

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
