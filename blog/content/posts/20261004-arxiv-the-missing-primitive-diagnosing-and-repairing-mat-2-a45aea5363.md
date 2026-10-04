---
title: "The Missing Primitive: Diagnosing and Repairing Mathematical Reasoning in Large Language Models"
date: 2026-10-04T10:40:54+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:50339550ce63834c6726c6e1a106f48d4773df35b84ca96439e9fc829bd52628"
source_payload_sha256: "sha256:4808d303d7c502c14d26b93c783749e86cbf87a4dad316f51044606d42985e99"
observation_id: obs_a45aea53630e7e1b98f29f10aba2d00610ab745fc7ccb20ca4d4767e02a24dd7
event_id: evt_4f9ea06df1f8b625e3733f428cb71c8795384b2238490ebe538ba58ef8faac33
revision_id: rev_ec44b17bcc50b1049ab7deddad6d4231ceea5023cc45f7cb54eda32323111f9c
source_published_at: 2026-10-01T17:59:32Z
first_seen_at: 2026-10-04T02:38:08.445744Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2610.02191v1
parent_observation_id: null
last_seen_at: 2026-10-04T02:38:08.445744Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02191v1](http://arxiv.org/abs/2610.02191v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Shuo Xing、Zilin Dai、Chengyuan Qian 等

## 来源摘要/节选

> While Large Language Models (LLMs) have demonstrated striking capabilities on frontier mathematical problems, it remains unclear whether they possess the structural mathematical understanding underlying their solutions. In this paper, we take a first step toward systematically studying mathematical understanding in LLMs, from diagnosing its distinct capabilities to leveraging these findings to improve post-training. First, we introduce the notion of Mathematical Primitive to probe structural mathematical understanding and propose \hlei{}, a novel benchmark that evaluates mathematical reasoning along four distinct dimensions: Discovery, Generation, Digestion, and Execution. Second, our systematic diagnosis shows that solution accuracy masks distinct capability profiles, primitives unlock substantial latent execution capacity, and Discovery is the dominant bottleneck in mathematical reasoning. Our post-training analysis further shows that discovery-limited failures are particularly amenable to repair. Finally, building on these findings, we introduce \abs{}, a primitive-privileged self-distillation framework that selectively transfers primitive-guided reasoning into the student model. Extensive experiments demonstrate that \abs{} consistently improves mathematical reasoning over baselines across model scales and challenging benchmarks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。