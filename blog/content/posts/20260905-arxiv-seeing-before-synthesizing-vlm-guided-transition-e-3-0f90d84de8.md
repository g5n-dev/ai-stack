---
title: "Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"
date: 2026-09-05T20:45:49+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2c9b11218c4137eed8705321702ad48b9e75278594236f535b603e56e37a537d"
source_payload_sha256: "sha256:46cecec631c3f4e88ebe58cc751bf2a50f5ac55de03f2bf38ec7d011901224de"
observation_id: obs_0f90d84de873f3ec1a050864364a15762a63bd8107544d6190393c8770eb7a04
event_id: evt_63a4d45bd8dd363d73ac37a56f73d2ab4b4d65ace95d46fc4fdffc97273f8ccc
revision_id: rev_4d8f88055d3c1c8295d1b7c4b0795efcd33f705008a713b1069bd8b289d849b5
source_published_at: 2026-09-03T17:58:02Z
first_seen_at: 2026-09-05T12:42:36.965354Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 110
interpretation_sha256: "sha256:1becc8fc4dd3a85e92aad7e501ebb7aa0bb6a82df4359560edf067dc8262edb5"
description: "该框架利用视觉语言模型在视频的间隔区段生成帧级叙事，并通过检测语义变化来定位事件转换，仅凭有序的事件描述即可在弱监督下完成稠密视频字幕和事件定位。"
external_url: http://arxiv.org/abs/2609.04183v1
parent_observation_id: null
last_seen_at: 2026-09-05T12:42:36.965354Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04183v1](http://arxiv.org/abs/2609.04183v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Ye-Chan Kim、Seunghee Choi、SeungJu Cha 等

## 要点解读

### 这是什么  
该框架利用视觉语言模型在视频的间隔区段生成帧级叙事，并通过检测语义变化来定位事件转换，仅凭有序的事件描述即可在弱监督下完成稠密视频字幕和事件定位。  

### 用在哪里  
适用于在未剪辑的长视频中自动发现并描述多个事件的应用，如视频检索、监控和教育内容的结构化。面向从事视频理解、弱监督学习以及多模态模型研发的科研人员和工程师。  

### 可以推断的  
推测：采用语义变化点划分事件边界可能提升定位的精度。  
推测：逐帧叙事生成会增加计算开销，需要在资源消耗与性能之间做权衡。

## 来源摘要/节选

> Weakly-Supervised Dense Video Captioning aims to localize and describe multiple events in untrimmed videos given only an ordered set of event-level captions per video. Recent work synthesizes auxiliary transition captions via LLM to provide additional vision-language alignment, but these captions lack visual grounding and are rigidly assigned to every inter-event gap at a fixed location and duration. To address these, we propose Seeing Before Synthesizing (SBS), a framework that adaptively provides visually grounded linguistic guidance only where warranted. Leveraging a VLM, we generate frame-level narratives for the inter-event gaps and detect transitions from the semantic variation across them. For identified transitions, we then refine inter-event temporal masks by blending the temporal midpoint with the semantic change point and selecting the width that maximizes vision-language alignment. Experiments on ActivityNet Captions and YouCook2 demonstrate state-of-the-art performance in both captioning and localization.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。