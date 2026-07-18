---
title: Enhancing Predictability of Multi-Tenant DNN Inference for Autonomous Vehicles'
  Perception
date: 2026-02-12 02:48:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11004v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a366c5a382b911ef50edbdc3ae96962d65299b7eab837483cdb264e95b47130c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
captured_at: '2026-07-18T04:14:55.115056Z'
source_capture_sha256: sha256:2a8c834f2c7f412a1e7e6853202539eb33236a789bfbca3cbc273ca9f78c4c06
source_capture_chars_original: 1909
source_publication_excerpt_chars: 1909
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11004v1](<https://arxiv.org/abs/2602.11004v1>)
- **作者**: Liangkai Liu, Kang G. Shin, Jinkyu Lee, Chengmo Yang, Weisong Shi
- **分类**: cs.CV
- **论文时间**: 2026-02-11T16:25:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11004v1.pdf](<https://arxiv.org/pdf/2602.11004v1.pdf>)

## 来源摘要/节选

> Autonomous vehicles \(AVs\) rely on sensors and deep neural networks \(DNNs\) to perceive their surrounding environment and make maneuver decisions in real time. However, achieving real-time DNN inference in the AV's perception pipeline is challenging due to the large gap between the computation requirement and the AV's limited resources. Most, if not all, of existing studies focus on optimizing the DNN inference time to achieve faster perception by compressing the DNN model with pruning and quantization. In contrast, we present a Predictable Perception system with DNNs \(PP-DNN\) that reduce the amount of image data to be processed while maintaining the same level of accuracy for multi-tenant DNNs by dynamically selecting critical frames and regions of interest \(ROIs\). PP-DNN is based on our key insight that critical frames and ROIs for AVs vary with the AV's surrounding environment. However, it is challenging to identify and use critical frames and ROIs in multi-tenant DNNs for predictable inference. Given image-frame streams, PP-DNN leverages an ROI generator to identify critical frames and ROIs based on the similarities of consecutive frames and traffic scenarios. PP-DNN then leverages a FLOPs predictor to predict multiply-accumulate operations \(MACs\) from the dynamic critical frames and ROIs. The ROI scheduler coordinates the processing of critical frames and ROIs with multiple DNN models. Finally, we design a detection predictor for the perception of non-critical frames. We have implemented PP-DNN in an ROS-based AV pipeline and evaluated it with the BDD100K and the nuScenes dataset. PP-DNN is observed to significantly enhance perception predictability, increasing the number of fusion frames by up to 7.3x, reducing the fusion delay by &gt;2.6x and fusion-delay variations by &gt;2.3x, improving detection completeness by 75.4% and the cost-effectiveness by up to 98% over the baseline.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
