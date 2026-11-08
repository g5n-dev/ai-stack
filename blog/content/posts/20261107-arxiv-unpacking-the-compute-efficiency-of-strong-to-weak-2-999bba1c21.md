---
title: "Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO"
date: 2026-11-07T22:01:19+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:53a37aed76bb66606099361b254cee36a7a1c292140d8ff21a23cf59eacc83ae"
source_payload_sha256: "sha256:d5984bbb9228dd358c28ca36a66178af28fba16db3d82ba3a5aae9a717ef5b31"
observation_id: obs_999bba1c21a9ca3ceecb9334d087cda7ab890933324b23644b993319674ecfbe
event_id: evt_e7f975eb2b13ce071edddab905442afea6f798e119aa5cf7542a674d39dd1a98
revision_id: rev_d10388aadf6e4c5e2dcb339935ce121a677a673a2ff77aeeee4191f99039f191
source_published_at: 2026-11-05T18:47:05Z
first_seen_at: 2026-11-07T14:10:28Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
interpretation_sha256: "sha256:d51c2383ceca4eeba39bc59fc57de4f12af5881182764c36e2e5afb7bff04fa5"
description: "这项工作比较了 on-policy distillation（OPD）与 GRPO 在达到目标精度时的训练 FLOPs，并考察教师来源、模型规模、任务难度和领域等因素。结果表明，教师是否就是学生自身的 GRPO 检查点，会显著影响蒸馏的计算效率。"
external_url: http://arxiv.org/abs/2611.08453v1
parent_observation_id: null
last_seen_at: 2026-11-08T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08453v1](http://arxiv.org/abs/2611.08453v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Zeyu Leo Liu、Yang Li、Bo Pang 等

## 要点解读

### 这是什么
这项工作比较了 on-policy distillation（OPD）与 GRPO 在达到目标精度时的训练 FLOPs，并考察教师来源、模型规模、任务难度和领域等因素。结果表明，教师是否就是学生自身的 GRPO 检查点，会显著影响蒸馏的计算效率。

### 用在哪里
适合研究大模型强化学习、策略蒸馏或训练成本优化的团队，用于判断应继续进行 GRPO 训练，还是利用已有检查点开展蒸馏。对于需要整合多个领域专家能力的场景，也可参考多教师蒸馏方案。

### 可以推断的
- 推测：若已拥有目标能力对应的检查点，将其作为教师进行 OPD，可能比继续用 GRPO 达到同等精度更节省训练计算。
- 推测：当不同领域分别由不同检查点提供能力时，多教师蒸馏可能比依赖单一检查点更适合完成能力整合。

## 来源摘要/节选

> On-policy distillation (OPD) trains a student on its own rollouts under a frozen teacher's per-token supervision. Does this dense signal reduce the training FLOPs needed to reach a target accuracy compared with reinforcement learning? We systematically compare vanilla reverse-KL OPD with Group Relative Policy Optimization (GRPO) across task difficulty, student and teacher size, domain, and optimization choices, measuring held-out accuracy against training FLOPs. With an external post-trained teacher, OPD generally loses to GRPO in accuracy per training FLOP at matched settings, even when the teacher is further trained with GRPO, and often suffers response-length inflation. Yet a different teacher changes the picture: when the teacher is the student's own GRPO checkpoint, OPD recovers that checkpoint's accuracy on math with $50\times$ fewer distillation FLOPs than GRPO needs to reach the same accuracy. Following the same teacher setting, we consistently observe this high efficiency with a larger student, on code, and in a second model family. On a single domain, however, the GRPO checkpoint is already the desired model, so distilling it adds to total compute. Across domains, separate GRPO checkpoints hold different capabilities, and no single checkpoint serves every domain. Multi-teacher OPD (DeepSeek-AI, 2026) consolidates per-domain GRPO experts into a single student that matches each expert's accuracy, with the distillation stage costing only 5.2% (on 2 domains) and 8.0% (on 4 domains) of the specialist training FLOPs. Counting specialist training and distillation together, this pipeline reaches joint GRPO's performance on the 2-domain mix with 42.0% fewer total FLOPs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。