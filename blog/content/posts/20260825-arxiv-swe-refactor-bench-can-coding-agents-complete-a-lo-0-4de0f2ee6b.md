---
title: "SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration?"
date: 2026-08-25T13:50:13+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0ebe3d3da09f32abd6266fbfcd73be8c25b530b83d2442c12f0366c3718fbeba"
source_payload_sha256: "sha256:af06cbf6908613be7cd87733203f1480194858961c6b6b2b6bc44c2eaae9fff3"
observation_id: obs_4de0f2ee6b155385d102dae21cda1272f544c5358d20d95a137a695eac7ce348
event_id: evt_86cd5dd6d929298afafe7ef46767ce4e6f1f0f94d9c856b815ec065101288d78
revision_id: rev_1eba9a57e29c68e42044162157af5cf4418ddf060a77172b91329e95e2837fd3
source_published_at: 2026-08-24T17:59:04Z
first_seen_at: 2026-08-25T16:54:57.529141Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
interpretation_sha256: "sha256:6c8efcb9e035afc8475beef6b3b18f5d770504bd241e80bfdb143bfc281a5cc7"
description: "SWE Refactor Bench 是一个评测基准，旨在检验代码生成代理能否自主完成整体仓库的栈迁移。它包含 20 项迁移任务，覆盖四类技术债务，并通过三阶段评估同时衡量迁移的完整性和行为的一致性。"
external_url: http://arxiv.org/abs/2608.23564v1
parent_observation_id: null
last_seen_at: 2026-08-25T05:47:09.180211Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23564v1](http://arxiv.org/abs/2608.23564v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Deyao Hong、Yizhe Chi、Wenyi Li 等

## 要点解读

### 这是什么  
SWE Refactor Bench 是一个评测基准，旨在检验代码生成代理能否自主完成整体仓库的栈迁移。它包含 20 项迁移任务，覆盖四类技术债务，并通过三阶段评估同时衡量迁移的完整性和行为的一致性。

### 用在哪里  
该基准适用于希望验证自动化重构工具在真实大型代码库中可行性的研究者与开发者，也用于对比不同代码生成模型在长时域、全仓库迁移任务上的表现。

### 可以推断的  
推测：仅靠行为测试通过并不能保证迁移实际执行，需要专门阶段确认迁移是否发生。  
推测：不同类别的迁移（如构建工具链重写与语言升级）对代理的完成度影响可能存在显著差异。

## 来源摘要/节选

> Modern software systems accumulate technical debt over decades of development, which makes migration expensive and largely manual. As coding agents become increasingly capable at bug fixing, can they autonomously perform such migrations? Existing benchmarks cannot answer this question because they evaluate only behavioural correctness, not whether the migration actually occurred. This leads an easy hack: agents copy the original implementation to make tests pass. We call this Blindness. To address this problem, we introduce SWE Refactor Bench, a benchmark comprising 20 whole-repository migrations, covering 4 kinds of technical debt. A three-stage evaluation protocol measures both migration completeness and behavioural correctness. (1) Migration Audit verifies that the migration occurred. (2) Behavioural Tests measure correctness with a fixed test suite. (3) Agentic Verification uses 6 independent coding agents to generate targeted tests for hidden behavioural differences. Across 520 runs from 8 frontier models and 26 model-effort configurations, only 28 of 520 runs ($5.4\%$) pass all three stages, 13 of the 20 tasks receive no accepted solution, and the best model (claude-opus-5) scores $47.0/100$. Migration completeness and behavioural correctness are distinct abilities: a few runs preserve behaviour by skipping the migration and are stopped at Migration Audit; most attempt it and break behaviour, and are stopped at Behavioural Tests. Agents cannot deliver a perfect migration: among the 340 runs that pass Migration Audit, $58\%$ reach $99\%$ of the fixed checks, yet only $26\%$ reach $100\%$. Agent capability differs across migration categories: agents score $31.4$ on build toolchain rewrites but only $5.6$ on language rewrites. Together, these findings position SWE Refactor Bench as a rigorous testbed for developing coding agents for reliable whole-repository migrations.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。