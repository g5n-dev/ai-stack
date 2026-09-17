---
title: "Learning to Program Adaptive Non-Local Observables for Machine Learning"
date: 2026-09-17T09:27:58+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:52f14215c5479b69a2b075a0c4dec839cbaff6575f76ec5cf103783bb98e0905"
source_payload_sha256: "sha256:e3ac855e6875769be55e8d25af030b467f25b3eb822f4841fa0d791e8497c41a"
observation_id: obs_cc6a7e063dce79b8a4c22bc21f1e26a52cde511393bd4ad3622eb896f95ecd12
event_id: evt_e29e28026659af4b0b0565ff768520f61f3277fefcbd9ab4ed67520b9f8afaae
revision_id: rev_bba6797123423e568a91e5463aeae14deaf6ce53a8c5f48742a104e1e442c710
source_published_at: 2026-09-16T13:35:31Z
first_seen_at: 2026-09-17T01:24:52.004987Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
interpretation_sha256: "sha256:b919241b7c70fb81d107099c3e22d44b3a5a91a4abd6b6d14be00621b63e722c"
description: "该研究提出一种通过经典超网络动态调节量子变分电路参数和非局部观测量的架构，以克服传统量子神经网络只能使用固定局部测量的局限。"
external_url: http://arxiv.org/abs/2609.18655v1
parent_observation_id: null
last_seen_at: 2026-09-17T01:24:52.004987Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.18655v1](http://arxiv.org/abs/2609.18655v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Yu-Ting Lee、Samuel Yen-Chi Chen、Huan-Hsin Tseng

## 要点解读

### 这是什么
该研究提出一种通过经典超网络动态调节量子变分电路参数和非局部观测量的架构，以克服传统量子神经网络只能使用固定局部测量的局限。

### 用在哪里
适用于需要在量子机器学习模型中对每个输入进行自适应观测的场景，例如多元时间序列预测和强化学习任务。

### 可以推断的
推测：该方法在需要灵活测量策略的其他量子学习任务中同样具有应用潜力。  
推测：在实际量子硬件上运行时，噪声和测量成本可能影响其效果。

## 来源摘要/节选

> Quantum neural networks (QNNs) are typically built from variational quantum circuits (VQCs), which are limited by local measurements. Adaptive non-local observables (ANO) address this by jointly optimizing circuit parameters and multi-qubit measurements. However, existing ANO-based VQCs learn only a single static observable that remains invariant across all inputs. We propose QFWP-ANO, a novel architecture which employs a classical hypernetwork to dynamically program VQC parameters and/or non-local observables conditioned on each input. On multivariate time-series forecasting across four ETT datasets, QFWP-ANO achieves the lowest MSE in 16 of 20 settings and second-lowest in the remaining four, surpassing ANO-based and other strong baselines. On reinforcement learning tasks, QFWP-ANO consistently surpasses ANO-VQCs. Our results establish input-conditioned ANO as an effective approach for enhancing QNNs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。