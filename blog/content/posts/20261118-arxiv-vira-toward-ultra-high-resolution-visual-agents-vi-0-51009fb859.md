---
title: "ViRA: Toward Ultra-High-Resolution Visual Agents via Cross-Input Relative Policy Optimization"
date: 2026-11-18T06:21:53+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e2734676de8b8f3179cfbdcc66d172e3e14458793f982878e65af575d4a7dd4a"
source_payload_sha256: "sha256:beb61ad3094043ccdf60dc5ee58f98a59bb4cd4d2f8f191a3d71d0314a111cfc"
observation_id: obs_51009fb859c1b51e38a4b6a73e59273e7d2a9ad7bec47f9e9cda8bfa869b4fff
event_id: evt_319b25ba2c0eeac770f0c2fe4598a32101d72d351f10a9e6b7dcb45a8aa5c881
revision_id: rev_7b8890ed95502231efc12864ab374288cb4accfb61f56871c35ea119e54cb2a2
source_published_at: 2026-11-16T18:59:04Z
first_seen_at: 2026-11-17T22:20:38.812922Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
interpretation_sha256: "sha256:2f7dfaba74a2eee5b2328bd31ae0964b4828f9b1720fc15f6ec087b92ac10f61"
description: "这篇工作提出 CrossRPO，通过对比不同版本的图像训练视觉智能体，使模型必须定位并读取局部证据，才能完成整组问答。作者据此构建了 ViRA-Train、ViRA-Bench 和 ViRA-Bench-Real，并训练出 ViRA-9B 与 ViRA-27B。"
external_url: http://arxiv.org/abs/2611.21605v1
parent_observation_id: null
last_seen_at: 2026-11-17T22:20:38.812922Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.21605v1](http://arxiv.org/abs/2611.21605v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Huawei Lin、Jinting Liu、Tongyan Wang 等

## 要点解读

### 这是什么
这篇工作提出 CrossRPO，通过对比不同版本的图像训练视觉智能体，使模型必须定位并读取局部证据，才能完成整组问答。作者据此构建了 ViRA-Train、ViRA-Bench 和 ViRA-Bench-Real，并训练出 ViRA-9B 与 ViRA-27B。

### 用在哪里
它适用于超高清照片的视觉问答、细节定位与证据读取任务，也可用于评估模型是否会依赖常识猜测。研究多模态智能体、强化学习训练和视觉推理评测的人会对此感兴趣。

### 可以推断的
- 推测：在超高清图像问答中，要求模型对一组局部变化都给出正确判断，可能比只奖励单个最终答案更能抑制“凭常识猜对”的现象。
- 推测：基于真实拍摄的 ViRA-Bench-Real 有助于检验模型是否真正理解图像中的局部证据，而不是识别编辑痕迹。

## 来源摘要/节选

> Visual agents answer questions about ultra-high-resolution photos by zooming into the relevant regions. However, existing agents often answer from common sense instead of reading the evidence. Reinforcement learning (RL) on the final answer cannot correct this, because a guess earns the same reward as reading. We propose Cross-Input Relative Policy Optimization (CrossRPO), which trains agents on contrast sets. A contrast set asks one question about several versions of an image that differ only in a small region with the evidence and have different answers, so only reading the evidence solves the whole set. CrossRPO rewards solving the whole set, and we prove that it does not reinforce a set answered from common sense. We build contrast sets for training (ViRA-Train) and evaluation (ViRA-Bench) by editing one small object in images of 21 to 120 megapixels, and we photograph further sets with real changes (ViRA-Bench-Real) to exclude editing traces. We train two Visual Reasoning Agents, ViRA-9B and ViRA-27B, with CrossRPO on only about 3,500 items of ViRA-Train each. CrossRPO achieves 63.3% set accuracy on ViRA-Bench at the maximum resolution, against 59.3% for GRPO. ViRA-9B is the most accurate open model of its size on all benchmarks, and ViRA-27B outperforms Claude Haiku 5.5 and GPT-6-Luna, both at their highest thinking level, on most benchmarks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。