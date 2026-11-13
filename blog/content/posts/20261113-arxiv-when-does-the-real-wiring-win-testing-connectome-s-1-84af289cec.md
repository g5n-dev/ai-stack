---
title: "When Does the Real Wiring Win? Testing connectome structure-function claims against unmeasured physiology"
date: 2026-11-13T08:21:05+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:688099b06debba03b729024c0366b8a968f702b888e188aaf036d2e71cee4c4a"
source_payload_sha256: "sha256:0dfeab233468b9773345e2615d1756ec06acd49bd6dfafc58fc49f256b7e164f"
observation_id: obs_84af289cec5a501bf6aa758ab328ce33e3fbacdaa20180b63448ffd878895c78
event_id: evt_dc58728fdb34835cc7302873dbedf788913ebe6cb9c8cfb424b0612320c9ad77
revision_id: rev_5f278954bc2aaf71adb7b4b7b70c36ef062a02cac8a328618ec7cdf05ce25232
source_published_at: 2026-11-10T18:55:48Z
first_seen_at: 2026-11-13T00:20:06.145014Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 105
interpretation_sha256: "sha256:cc1b2e735b2c73003dd72f1849b99a84608403430284d8ed701709c992f7b91e"
description: "这项研究检验神经连接组约束模型的表现优势究竟来自真实布线，还是来自更充分的调参与参数选择。比较区分了迁移生理参数、各自调参以及受独立数据约束三种方案，并用合成真值、安慰剂对照和果蝇回路模型验证。"
external_url: http://arxiv.org/abs/2611.14508v1
parent_observation_id: null
last_seen_at: 2026-11-13T00:20:06.145014Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.14508v1](http://arxiv.org/abs/2611.14508v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Yeyuan Liu

## 要点解读

### 这是什么
这项研究检验神经连接组约束模型的表现优势究竟来自真实布线，还是来自更充分的调参与参数选择。比较区分了迁移生理参数、各自调参以及受独立数据约束三种方案，并用合成真值、安慰剂对照和果蝇回路模型验证。

### 用在哪里
适用于评估“连接结构塑造神经功能”类主张，尤其适合神经回路建模、连接组研究，以及存在基线调参偏差的机器学习比较。

### 可以推断的
- 推测：仅以真实布线优于打乱布线作为证据，可能不足以支持结构决定功能的结论。
- 推测：加入独立生理数据约束并匹配优化强度后，部分原本成立的结构性主张可能暴露出模型本身的不足。

## 来源摘要/节选

> Connectome-constrained models are often used to argue that a measured wiring diagram outperforms shuffled or rewired wiring, and hence that structure shapes function. Such comparisons can confound wiring with how the models are tuned: a connectome fixes who connects to whom, not the excitability, gains or plasticity rates the model also needs, and modellers often tune these until the real-wiring model works. We separate three estimands: physiology tuned on the real wiring and transferred to nulls (P1), each wiring tuned on its own (P2), and P2 restricted to physiology consistent with independent data (P3). The biases involved are known in machine learning (under-tuned baselines, inherited weights, winner's curse); we measure what they do to biological conclusions, using synthetic ground truth, placebo nulls and three Drosophila circuit models. Some claims survive every protocol we test: segregated reward and punishment dopamine improves learning, and head-direction topography is required for a persistent bump. Others do not. In the mushroom body, the real Kenyon-cell output wiring beats a cross-subtype identity shuffle by 0.09 under P1 and P2 but loses to it by 0.09 under P3 (95% CIs exclude zero; held-out runs confirm). The verdict is set by the share of alpha'beta' cells among active Kenyon cells, which P1 selects low; at the share implied by imaging (about 44%) the real-wiring model fails to learn, exposing a model inadequacy rather than a deficit of the fly's wiring. In flyvis, P1 penalises a mirrored connectome, which has a constructed solution within 0.07 (median) of the real error, more than a spatially shuffled one in 50 of 50 members; the ranking survives ten-fold longer retraining but depends on the checkpoint at fifty-fold. A credible structural claim needs matched optimisation, data-constrained physiology and a model that still works there.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。