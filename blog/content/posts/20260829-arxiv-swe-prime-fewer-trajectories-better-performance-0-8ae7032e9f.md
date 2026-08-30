---
title: "SWE-Prime: Fewer Trajectories, Better Performance"
date: 2026-08-29T10:14:23+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:38c11ec41715d9ece467dd8bf4656a759bf361343ea9053f567599a38cad7064"
source_payload_sha256: "sha256:25b044ce0b67a203ff17d11d88c991e3de4fd02ab3bc2f3bcad2e7a15e55f115"
observation_id: obs_8ae7032e9f0cdd88e88844039c76e0f298b19952af60016f5d91beca2d9ecfc2
event_id: evt_599655d1c50c05363e99904aeb7aca07f4795a5115e27510d49cfebe961795c4
revision_id: rev_2d27fae85c297e60975c5cf797cd708d4f421daf1a889920fbc2d89a8016d974
source_published_at: 2026-08-27T17:58:10Z
first_seen_at: 2026-08-29T02:22:56Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
interpretation_sha256: "sha256:6fe802d196325503b1dcec3a119495eab56f036d9dc1f86d584fd3f0f7f6d744"
description: "SWE-Prime 是一种两阶段的有监督微调数据筛选方法。它先在轨迹层面依据过程质量、结果质量及数据代表性进行过滤，随后在段层面依据对最终方案的贡献度、可学习性和潜在风险进行细选，只让被选中的段参与损失计算。"
external_url: http://arxiv.org/abs/2608.27449v1
parent_observation_id: null
last_seen_at: 2026-08-30T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27449v1](http://arxiv.org/abs/2608.27449v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Dewu Zheng、Ruizhe Ye、Yanlin Wang 等

## 要点解读

### 这是什么
SWE-Prime 是一种两阶段的有监督微调数据筛选方法。它先在轨迹层面依据过程质量、结果质量及数据代表性进行过滤，随后在段层面依据对最终方案的贡献度、可学习性和潜在风险进行细选，只让被选中的段参与损失计算。

### 用在哪里
适用于需要用少量高质量轨迹微调语言模型以解决实际软件问题的研究团队和工程团队。对关注训练数据噪声控制和筛选策略的从业者同样有参考价值。

### 可以推断的
推测：在实际软件问题解决轨迹中，常包含冗余或无效步骤，这类噪声会影响模型的学习效果。  
推测：通过在轨迹和段两级进行质量评估与筛选，可显著提升监督信号的质量，从而在不增加模型规模的情况下提升性能。

## 来源摘要/节选

> To improve large language models' ability to resolve real-world software issues, prior work has focused on constructing large-scale agent trajectory datasets and performing supervised fine-tuning (SFT) on successful trajectories. However, task success does not guarantee high-quality supervision: successful trajectories may still contain ineffective, redundant, or risky steps. Directly using such trajectories for SFT can introduce noisy supervision and encourage models to imitate undesirable problem-solving behaviors. Therefore, we propose SWE-Prime, a multi-granularity, two-stage SFT data selection method that progressively filters training data at the trajectory and segment levels. Specifically, the first stage performs trajectory-level screening based on process quality, result quality, and data representativeness, selecting a high-quality and representative subset of successful trajectories. The second stage performs segment-level selection by grouping consecutive steps into semantic segments and assessing each segment based on its contribution to the final solution, learnability, and potential risks. During SFT, all segments remain in the sequence to preserve context, while only selected segments contribute to the loss computation. Experiments on SWE-Bench Pro and SWE-Bench Verified show that training on the 10% trajectory subset selected by SWE-Prime outperforms training on the full resolved dataset, yielding relative performance gains of up to 12.2% and 24.2%, respectively.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。