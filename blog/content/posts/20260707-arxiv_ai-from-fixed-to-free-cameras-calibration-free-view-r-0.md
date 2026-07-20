---
title: 'From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action
  Model'
date: 2026-07-07 23:27:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2607.05396v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e872772d21b9c1fc43e717a13f2ac8265999988f7fc231d09b965cde59d7dba8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:30:25.647174Z'
source_capture_sha256: sha256:941da7bc3cca738f928e18fcd36d55b9a6790a17b3df83390b9f9e85fbec3d4e
source_capture_chars_original: 1433
source_publication_excerpt_chars: 1433
observation_id: obs_3df162d16c331baab109fe57113eb22b063c8f82223457772edce31e13fafcc1
revision_id: rev_3403e01b599b77fce7efd41843d0c5b403184cfcc847251455f09a7147a8ceb2
event_id: evt_675b648cec7c2bacb2ef440324ed23c9be203c1f3f37ad809b06b7c73d9c9bd2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.05396v1](<https://arxiv.org/abs/2607.05396v1>)
- **作者**: Wenhao Li, Xueying Jiang, Quanhao Qian, Deli Zhao, Shijian Lu, Gongjie Zhang, Ran Xu
- **分类**: cs.CV
- **论文时间**: 2026-07-06T17:59:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.05396v1.pdf](<https://arxiv.org/pdf/2607.05396v1.pdf>)

## 来源摘要/节选

> Real-world robot deployment rarely maintains the training-stage camera setup, where cameras often experience repositioning or remounting depending on actual scenarios. Existing view-robust Vision-Language-Action \(VLA\) policies tolerate such camera variations only when the camera extrinsics are explicitly provided, making them fragile and hard to use especially when view robustness is critical. We argue that the policy should not be told where the camera is, but rather figure it out by itself. To this end, we introduce Camera-Centric VLA \(CamVLA\), a new VLA model that decouples manipulation controls from camera geometry by predicting \(i\) a camera-centric end-effector action expressed in the local camera frame, and \(ii\) a 6-DoF hand-eye matrix relating cameras to the robot base. A deterministic geometric transformation composes the two predictions into a robot base-frame action. This disentangles how I should move in pose-independent camera-centric action generation from where I am looking from in camera-perspective geometric grounding. The resulting policy is calibration-free, depth-free, and single-view, requiring only a single monocular RGB image as the visual observation and task instruction at deployment. Evaluations in both simulation and real-world robot data show that CamVLA consistently improves success rates across diverse unseen viewpoints. Project page: https://alibaba-damo-academy.github.io/CamVLA/.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
