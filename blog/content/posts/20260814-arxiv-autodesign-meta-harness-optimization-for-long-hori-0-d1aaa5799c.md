---
title: "AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design"
date: 2026-08-14T10:47:35+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:46e9d0e0e78b50d325cf345c56f15ce3c4db3ae8ea9ffc6da1d44cec22af84de"
source_payload_sha256: "sha256:4efb311c73d666c1021ade5276b6bc50a4b004f46050217520ffccffb4bab572"
observation_id: obs_d1aaa5799cdcf146d77a1b15b31b040c24db5dc9cd0a54b42cd538fa2b6b0eb4
event_id: evt_8b0e196cbd35a2f4c8adea8151ccbd699f47bc979fa9db26b76571459ab674c3
revision_id: rev_43bb2ae86ddf04b77085ddf3be8e8f026a07d6e66c358e7805abef48477f2b8a
source_published_at: 2026-08-13T17:59:57Z
first_seen_at: 2026-08-14T02:56:40Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
interpretation_sha256: "sha256:c02264b4d0b367a4721e3dfed4d490741d1c58937bf48a3da17ddb518f359f11"
description: "AutoDesign 是一个让元‑框架优化器指导代码代理依据 rollout 反馈递归改进系统结构的框架，聚焦于从学术论文自动生成海报的任务，并配套提供 PosterBench 评测集。"
external_url: http://arxiv.org/abs/2608.13560v1
parent_observation_id: null
last_seen_at: 2026-08-16T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.13560v1](http://arxiv.org/abs/2608.13560v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yaxin Luo、Haobin Jiang、Jialv Zou 等

## 要点解读

### 这是什么
AutoDesign 是一个让元‑框架优化器指导代码代理依据 rollout 反馈递归改进系统结构的框架，聚焦于从学术论文自动生成海报的任务，并配套提供 PosterBench 评测集。

### 用在哪里
适用于需要把大量文本素材快速转化为视觉呈现的研究或产品场景，尤其在多学科论文转海报的过程中追求高质量、低成本输出的团队。

### 可以推断的
推测：该框架的核心思路——通过元优化器结合人类设计先验进行递归调优——或可迁移至其他需要逐步优化生成流程的任务，如文档自动排版或交互原型生成。  
推测：把人类设计偏好与自动化调优相结合的机制，可能会提升长时程、多轮交互式系统的鲁棒性与生成质量。

## 来源摘要/节选

> Transforming multimodal sources into condensed and structured media outputs can be fundamentally conceptualized as a long-horizon agentic process centered on a model-harness system. While an ideal harness system should align with human design priors and accumulate reusable experience through empirical exploration to drive recursive self-improvement, existing paradigms remain static and fall short of this capability. In this paper, we present AutoDesign, a framework that aligns with human design priors, where a meta-harness optimizer guides a code agent to recursively improve harness based on rollout feedback. To instantiate and evaluate this framework, we focus on the academic paper-to-poster generation task and introduce PosterBench, comprising a 100-paper Main Track spanning five disciplines and PosterBench-mini, a shared 10-paper subset for controlled evaluation. On the PosterBench Main Track, AutoDesign achieves the highest score of 78.32, surpassing the closed-source commercial system Claude Design by 7.45 points. Across seven controlled code-agent-model configurations, integrating the learned DesignHarness consistently improves performance, increasing the average PosterBench Score from 54.99 to 67.39 (+12.4%). In a fully autonomous long-horizon loop, it executes 253 tool calls and 11 editing turns within 40 minutes for under $3, reaching average conference-poster quality in human evaluation. A system-blind human study further demonstrates that AutoDesign achieves the highest human preference among evaluated systems.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。