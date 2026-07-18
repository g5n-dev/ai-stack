---
title: 'Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation'
date: 2026-02-13 03:01:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12125v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:01b0ccbe5350cbaca6fa836def56f2579a408c9aa4df4f0541c41ca4b42414b0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:15:06.314161Z'
source_capture_sha256: sha256:502a7c7de16a150adf93d44d4dabacffb6b09b5ea6306b2027541ec9ed22aae4
source_capture_chars_original: 1890
source_publication_excerpt_chars: 1890
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12125v1](<https://arxiv.org/abs/2602.12125v1>)
- **作者**: Wenkai Yang, Weijie Liu, Ruobing Xie, Kai Yang, Saiyong Yang, Yankai Lin
- **分类**: cs.LG
- **论文时间**: 2026-02-12T16:14:29Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12125v1.pdf](<https://arxiv.org/pdf/2602.12125v1.pdf>)

## 来源摘要/节选

> On-policy distillation \(OPD\), which aligns the student with the teacher's logit distribution on student-generated trajectories, has demonstrated strong empirical gains in improving student performance and often outperforms off-policy distillation and reinforcement learning \(RL\) paradigms. In this work, we first theoretically show that OPD is a special case of dense KL-constrained RL where the reward function and the KL regularization are always weighted equally and the reference model can by any model. Then, we propose the Generalized On-Policy Distillation \(G-OPD\) framework, which extends the standard OPD objective by introducing a flexible reference model and a reward scaling factor that controls the relative weight of the reward term against the KL regularization. Through comprehensive experiments on math reasoning and code generation tasks, we derive two novel insights: \(1\) Setting the reward scaling factor to be greater than 1 \(i.e., reward extrapolation\), which we term ExOPD, consistently improves over standard OPD across a range of teacher-student size pairings. In particular, in the setting where we merge the knowledge from different domain experts, obtained by applying domain-specific RL to the same student model, back into the original student, ExOPD enables the student to even surpass the teacher's performance boundary and outperform the domain teachers. \(2\) Building on ExOPD, we further find that in the strong-to-weak distillation setting \(i.e., distilling a smaller student from a larger teacher\), performing reward correction by choosing the reference model as the teacher's base model before RL yields a more accurate reward signal and further improves distillation performance. However, this choice assumes access to the teacher's pre-RL variant and incurs more computational overhead. We hope our work offers new insights for future research on OPD.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
