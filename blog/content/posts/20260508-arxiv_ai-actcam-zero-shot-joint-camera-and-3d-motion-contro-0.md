---
title: 'ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation'
date: 2026-05-08 08:02:39+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.06667v1
aliases:
- /posts/20260509-arxiv_ai-actcam-zero-shot-joint-camera-and-3d-motion-contro-0/
- /posts/20260510-arxiv_ai-actcam-zero-shot-joint-camera-and-3d-motion-contro-0/
- /posts/20260511-arxiv_ai-actcam-zero-shot-joint-camera-and-3d-motion-contro-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:965a4d763dcbb07a23dfb3a49328ece6a7d369cdc7a4e04ad300c8df66fc4f60
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
captured_at: '2026-07-18T04:29:31.582048Z'
source_capture_sha256: sha256:39923350fa843971c61ddad958687b59459d9a35e1ca099a1c40becdb302afe2
source_capture_chars_original: 1504
source_publication_excerpt_chars: 1504
observation_id: obs_a511eb39a48046e20733ba7e450aaa59f4c13c19f172f4bb7daebeaeba2cf47d
revision_id: rev_9d63e22a4d727b45ac8969b3fb2bcd380a4578928a4318bbc1633e117fe165ab
event_id: evt_c9f82bd37a5be0f8aee6c8c3eb4b0d30a9bbe27f33f5a2cb5d7fd4fba4034de2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.06667v1](<https://arxiv.org/abs/2605.06667v1>)
- **作者**: Omar El Khalifi, Thomas Rossi, Oscar Fossey, Thibault Fouque, Ulysse Mizrahi, Philip Torr, Ivan Laptev, Fabio Pizzati, Baptiste Bellot-Gurlet
- **分类**: cs.CV
- **论文时间**: 2026-05-07T17:59:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.06667v1.pdf](<https://arxiv.org/pdf/2605.06667v1.pdf>)

## 来源摘要/节选

> For artistic applications, video generation requires fine-grained control over both performance and cinematography, i.e., the actor's motion and the camera trajectory. We present ActCam, a zero-shot method for video generation that jointly transfers character motion from a driving video into a new scene and enables per-frame control of intrinsic and extrinsic camera parameters. ActCam builds on any pretrained image-to-video diffusion model that accepts conditioning in terms of scene depth and character pose. Given a source video with a moving character and a target camera motion, ActCam generates pose and depth conditions that remain geometrically consistent across frames. We then run a single sampling process with a two-phase conditioning schedule: early denoising steps condition on both pose and sparse depth to enforce scene structure, after which depth is dropped and pose-only guidance refines high-frequency details without over-constraining the generation. We evaluate ActCam on multiple benchmarks spanning diverse character motions and challenging viewpoint changes. We find that, compared to pose-only control and other pose and camera methods, ActCam improves camera adherence and motion fidelity, and is preferred in human evaluations, especially under large viewpoint changes. Our results highlight that careful camera-consistent conditioning and staged guidance can enable strong joint camera and motion control without training. Project page: https://elkhomar.github.io/actcam/.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
