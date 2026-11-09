---
title: "ReproBridge: Building Reproducibility into ML Research Artifacts"
date: 2026-11-08T02:48:23+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "机器学习", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d76cb6320633943e30648ef793ece8e2f75bd54bd894b0b634c110f2ac406a41"
source_payload_sha256: "sha256:c0aaca2d49200fca8f1cf8854e6253d1636dc976e23d54c6c9491dcd5870b410"
observation_id: obs_5d920b8c0784633371b19f05fcbc35b545ad7b7b847e7f7676f28bda4f20be55
event_id: evt_d9826a69ee6bd32f994d304dae3fc4640f1d9d54e6bf7c49de5340934fde7cc0
revision_id: rev_19e4a1f42ab57fc2360ebb5597a3d5da847d9d392332c0fee46628b98ea9b72b
source_published_at: 2026-11-05T18:45:36Z
first_seen_at: 2026-11-07T18:57:49Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:e377c429348ba2df3dc572ab0d112e6da175ce480420bc53eb98fcf2546d75e3"
description: "ReproBridge 将代码、环境配置、实验启动器和复现指南整合成标准化制品，并通过智能体工作流保存实验过程中的操作知识与决策。其目标是提升机器学习实验的独立复现成功率。"
external_url: http://arxiv.org/abs/2611.08452v1
parent_observation_id: null
last_seen_at: 2026-11-09T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08452v1](http://arxiv.org/abs/2611.08452v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Yubo Wang、Rui Meng、Jaehyun Nam 等

## 要点解读

### 这是什么
ReproBridge 将代码、环境配置、实验启动器和复现指南整合成标准化制品，并通过智能体工作流保存实验过程中的操作知识与决策。其目标是提升机器学习实验的独立复现成功率。

### 用在哪里
该方法适用于需要从论文及配套代码中重建实验流程的编码智能体，也可用于评估和改进机器学习研究制品的可复现性。实验中，标准化制品将四个模型的平均复现成功率从 76.4% 提升至 92.6%，并使平均 API 成本下降 19.7%。

### 可以推断的
- 推测：在实验信息分散于论文、代码和辅助文件时，完整保存执行步骤可能比单纯提供原始代码更有利于稳定复现。
- 推测：对研究制品进行标准化整理，可能降低不同模型在复现任务上的表现差异，并减少因补充缺失细节产生的额外调用成本。

## 来源摘要/节选

> Reproducing machine learning experiments requires reconstructing procedures from information scattered across papers, released code, and supporting artifacts. For coding agents, reproduction success can therefore depend on their ability to fill in missing details, rather than on the released artifacts alone. We ask whether preserving recovered procedures and decisions improves subsequent independent reproduction. We define a standardized artifact design comprising a refined codebase, environment setup, experiment launchers, and a reproduction guide, and introduce ReproBridge, an agent workflow for constructing these refined reproducible artifacts. ReproBridge-Bench provides 1,029 tasks from 387 experiments across 36 papers, anchored by five human-verified reference scores per task. Agents attempt tasks in fresh sessions with raw code or refined artifacts; a separate Auditor checks execution evidence. Across four evaluated models, refined artifacts raise mean reproduction success from 76.4% to 92.6% and reduce downstream API spending by 19.7% on average. The cross-model success-rate spread narrows from 21.6 to 3.9 percentage points, with all four models achieving mean success rates above 90%. Removing any component reduces success in the ablation study, with the largest losses from code and environment removal. These results suggest that preserving execution knowledge helps even models with lower raw-code success reproduce experiments more reliably and at lower API cost.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。