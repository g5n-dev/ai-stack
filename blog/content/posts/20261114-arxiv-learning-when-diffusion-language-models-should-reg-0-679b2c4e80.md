---
title: "Learning When Diffusion Language Models Should Regenerate"
date: 2026-11-14T18:23:58+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b4c58af77ad49bf8c1a2b64e56ac4289db8ea716e6dabda76878a56eeeec6d46"
source_payload_sha256: "sha256:d8ebddcecd8174afec752cfaf228716e31bc10b9d03a33156b87ece3a5a9dd2f"
observation_id: obs_679b2c4e802619e66091284b57e41fd2b8a1bcb0d7f83f75f393dcc7cb4f709f
event_id: evt_a86f58c2c89a93d60749f9d64189631cce670634544fe4ba71049ad36244dea7
revision_id: rev_2093b61038f14a7c3e84bb027f3ebb776fe7d0711bc4bb2ca7e88b80f42783f6
source_published_at: 2026-11-12T18:58:50Z
first_seen_at: 2026-11-14T10:22:45.783425Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:325566c459461bb0b52ca74d671d28fa403823e1697e8877208a90d66e3244cd"
description: "该工作提出一种名为 DiVR 的验证器，用于判断扩散语言模型的部分生成结果是否可能得到正确答案，并据此决定是否重生成文本块及保留哪个候选方案。生成器本身无需改变。"
external_url: http://arxiv.org/abs/2611.17320v1
parent_observation_id: null
last_seen_at: 2026-11-14T10:22:45.783425Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.17320v1](http://arxiv.org/abs/2611.17320v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Minhae Oh、Jeonghye Kim、Jinwoo Koo 等

## 要点解读

### 这是什么
该工作提出一种名为 DiVR 的验证器，用于判断扩散语言模型的部分生成结果是否可能得到正确答案，并据此决定是否重生成文本块及保留哪个候选方案。生成器本身无需改变。

### 用在哪里
适用于扩散语言模型的推理生成、答案纠错和文本修订场景，尤其适合需要根据中间生成状态决定是否重新生成的任务。

### 可以推断的
- 推测：把重生成时机判断与生成模型分离，可能便于在现有系统上增加纠错环节，而不必改动主生成流程。
- 推测：这类方法可能提升推理任务的可靠性，但其额外计算成本会影响实际部署取舍。

## 来源摘要/节选

> Remasking allows diffusion language models to revisit generated text, but effective correction requires knowing when and what to revise. Our diagnosis on Sudoku reveals two gaps. Hidden states contain error information that token confidence does not reliably expose, and remasking an isolated error usually reproduces it when the surrounding context remains fixed. These findings motivate DiVR , a verifier that predicts whether a partially generated sequence will reach a correct answer. Trained on the final correctness of the model's own trajectories, DiVR decides when to regenerate a block and which alternative to retain, while the generator itself stays unchanged. On five reasoning benchmarks with LLaDA-8B-Base, DiVR raises the average accuracy of the fine-tuned generator from 35.3\% to 43.4\% at $1.9$-$3.5\times$ the cost of greedy decoding, above search baselines that use $3.8$-$7.4\times$. It also complements post-training such as supervised fine-tuning and reinforcement learning, and generalizes to other generators, including Dream.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。