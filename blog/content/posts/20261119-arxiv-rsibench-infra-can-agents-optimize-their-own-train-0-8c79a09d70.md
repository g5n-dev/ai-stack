---
title: "RSIBench-Infra: Can Agents Optimize Their Own Training and Inference Infrastructure at Production Scale?"
date: 2026-11-19T11:26:03+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:906a5f12715650cceed97d91042f36f5d2161651061be89c40f8e70782d27870"
source_payload_sha256: "sha256:13e41ba0bb941983806823271e9d5d935ced0e80f40ac7ff1c48a70d017b54c3"
observation_id: obs_8c79a09d70d62ee0814db31ff9e3de6e1393ced1da7b00a3a2357c1f6648181c
event_id: evt_1b92b6a5b5a4e3a75354136cb1383cf4a613d6896b05d2ff1d58043148f1ca63
revision_id: rev_33fe0a74690e3c29e4b63c017f72bb53342e18e69573f2c817988bee053955ed
source_published_at: 2026-11-18T13:29:44Z
first_seen_at: 2026-11-19T03:24:34.578469Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
interpretation_sha256: "sha256:c9aa039fda04387b3494c1b585320d4bfbe6edb54712ada65165f19fbb6c5104"
description: "RSIBench-Infra 是面向生产级训练与推理优化的基准，包含20项任务，允许代理跨引擎、内核和指令层修改软件栈。评测在任务质量约束下衡量端到端性能，并使用 OCI 镜像层协议记录改动以便复现部署。"
external_url: http://arxiv.org/abs/2611.24395v1
parent_observation_id: null
last_seen_at: 2026-11-19T03:24:34.578469Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.24395v1](http://arxiv.org/abs/2611.24395v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Hanlin Wu、Yifei Wang、Zhicheng Cai 等

## 要点解读

### 这是什么
RSIBench-Infra 是面向生产级训练与推理优化的基准，包含20项任务，允许代理跨引擎、内核和指令层修改软件栈。评测在任务质量约束下衡量端到端性能，并使用 OCI 镜像层协议记录改动以便复现部署。

### 用在哪里
它适用于评估 AI 代理能否在真实生产负载下提升训练和推理效率，尤其适合需要跨软件层验证优化效果的团队。全部任务中，66.2% 实现了超过 1.10 倍的经验证加速。

### 可以推断的
- 推测：端到端评测有助于识别局部优化无法稳定转化为整体收益的情况。
- 推测：统一的镜像层提交方式可能降低部署和复现实验的集成成本。

## 来源摘要/节选

> Improving the efficiency of training and inference infrastructure is a practical component of recursive self-improvement. Existing benchmarks for agent-driven optimization largely focus on individual software layers such as kernel, leaving unclear whether agents can deliver end-to-end performance gains under production workloads. We introduce RSIBench-Infra, a benchmark of 20 training and inference tasks spanning diverse model families and modalities, with deployments of up to 32 accelerators on NVIDIA GPUs and Ascend NPUs. Agents start from runnable baselines derived from official recipes and can modify the software stack across engine, kernel, and instruction levels. An OCI image-layer submission protocol captures these changes for reproducible deployment, while independent evaluation measures end-to-end performance under task-specific quality constraints. Across all task results, 66.2% exceed $1.10\times$ validated speedup. These results demonstrate that current agents can improve production-scale training and inference performance, but identifying effective optimization strategies and consistently translating local improvements into end-to-end gains remain challenging.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。