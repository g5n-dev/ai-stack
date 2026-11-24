---
title: "Pruning Autonomous Driving VLAs: What to Preserve for Reasoning and Action"
date: 2026-11-25T01:41:20+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:236c771297c53bdde3f5f832f7ca42425b4c85a35ee7b65c4d9189c3739e3452"
source_payload_sha256: "sha256:3dfd1a85df8cb2363709c28931c4dd553be6308796c102ebe31415172725972d"
observation_id: obs_82e438455d2233dc0c6fba4568e164ef5ec973caae25617dfda97c637204df46
event_id: evt_ab40dddabf7e8d539a8f5ff5bbc35ec9024b668c5b055f12c0643474926d3838
revision_id: rev_a0785d254522e0268cff92ebe51022bd351adfd7d30e0db1ffb39e300020d4cc
source_published_at: 2026-11-23T18:59:52Z
first_seen_at: 2026-11-24T17:40:17.069566Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:fb3e0b47ebf460a615f049b0287f6872bf4f47d352f4c2ce4ddad20ce2de2484"
description: "该研究针对自动驾驶视觉-语言-动作模型中的高计算与显存开销，提出结构化剪枝方法 MoOP，在尽量保留场景理解和轨迹预测能力的同时压缩模型。"
external_url: http://arxiv.org/abs/2611.31240v1
parent_observation_id: null
last_seen_at: 2026-11-24T17:40:17.069566Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.31240v1](http://arxiv.org/abs/2611.31240v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Seongchan Kim、Soowon Son、Sangoh Kim 等

## 要点解读

### 这是什么
该研究针对自动驾驶视觉-语言-动作模型中的高计算与显存开销，提出结构化剪枝方法 MoOP，在尽量保留场景理解和轨迹预测能力的同时压缩模型。

### 用在哪里
适用于需要部署推理型自动驾驶 VLA、同时关注推理速度与显存占用的研究团队和工程人员，尤其适合无法对剪枝模型进行额外微调的场景。

### 可以推断的
- 推测：同时兼顾推理与动作目标，可能比只针对单一能力进行剪枝更适合需要完整决策链路的自动驾驶任务。
- 推测：在更高压缩率下保持推理能力，可能有助于降低模型规模增大时的部署成本与性能退化风险。

## 来源摘要/节选

> Reasoning vision-language-action (VLA) models for autonomous driving use chain-of-thought (CoT) reasoning to guide action generation, but incur substantial memory and computational costs. We study structured pruning for these models, focusing on preserving both scene understanding and trajectory prediction. Our analysis of Taylor importance in Alpamayo-1.5-10B shows that reasoning and trajectory objectives assign different importance to the same vision-language model (VLM) structures. In the action expert, MLP channels exhibit more stable importance rankings across denoising steps than query heads, and a small fraction of channels accounts for most of the measured importance. Based on these findings, we propose MoOP, which combines importance ranks from both objectives for VLM pruning and aggregates stepwise importance to select a fixed subset of expert MLP channels. At 24.0% total parameter reduction, VLM-only pruning with MoOP performs comparably to or slightly better than the strongest baselines in driving, while retaining 94.0% of the dense model's LingoQA score, far above all other methods. At a higher reduction of 30.0%, MoOP degrades much less than every other method, as it is the only one whose reasoning does not collapse. Removing 93.75% of expert MLP channels increases total parameter reduction to 39.4%, with nearly unchanged open-loop errors relative to VLM-only pruning and competitive closed-loop performance. The resulting model achieves a 1.37x end-to-end inference speedup and 36.6% lower peak memory than the dense model, without post-pruning fine-tuning.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。