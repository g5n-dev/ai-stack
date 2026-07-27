---
title: "SM4RT: Learning Structured Motion Geometry for 4D Reconstruction"
date: 2026-07-27T19:41:52+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4d57aa39da8c5eecf09d5c1806575742eafe966e6e808745e282721ce4df9e2a"
source_payload_sha256: "sha256:8fbd2b33b9453dbf8cd6e12c5ab0f7e8a70a3ebbd16948aed2d8640027c59cd3"
observation_id: obs_4dcf849c3d15c3b95df14f6eee9009354e46420c39896b5ce8e2d0ff6dd52205
event_id: evt_f39dd568f2518a96e87b2bc998142d4fb5e462665bfc7e8794eccfac2609127f
revision_id: rev_e1bbf47a6ad5f382202b3b46413857866a18cd5f6efb3a44af36209ec815e75c
source_published_at: 2026-07-24T17:59:51Z
first_seen_at: 2026-07-27T11:41:02.365376Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.22534v1
parent_observation_id: null
last_seen_at: 2026-07-27T11:41:02.365376Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.22534v1](http://arxiv.org/abs/2607.22534v1)

## 来源摘要/节选

> Geometry Foundation Models (GFMs) have substantially advanced monocular 3D reconstruction, yet extending this capability to 4D dynamic understanding remains a fundamental challenge. Most existing motion perception methods (e.g., sparse tracking, dense point-wise flow) treat motion as independent point-wise displacements, ignoring the structured nature of physical motion. However, real-world objects usually obey rigid-body kinematics, and points thus usually move collectively, not in isolation. Motion itself possesses geometric structure: physical objects undergo a set of rigid-body transformations governed by SE(3), rather than unstructured point-wise displacements. Building on this insight, we propose SM4RT, a Structured Motion 4D Reconstruction Transformer for end-to-end 3D reconstruction and structured motion perception. SM4RT introduces Structure-of-Motion to represent scene dynamics, where scene motion is decomposed into a compact set of motion bases, each represented as a temporal sequence of 6D twists in SE(3). Dense scene motion is then recovered by sparse, time-shared per-pixel assignment weights over these bases, ensuring points on the same object share a common rigid-body motion trajectory. SM4RT introduces a parallel motion geometry encoder and decoder that jointly infer 3D geometry, world-coordinate motion, and scene kinematic structure in a single forward pass from monocular RGB video. SM4RT achieves strong motion reconstruction performance while preserving the geometric structure of scene motion.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。