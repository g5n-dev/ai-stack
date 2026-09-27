---
title: "Underwater C3-JEPA: An Object-Centric Cross-View World Model for ROV Salvage"
date: 2026-09-27T09:28:48+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9f5cc48f7ab0bdadb71126f9301a3ce2a1a9d7bd8d50d131f1238058e92b701b"
source_payload_sha256: "sha256:b0b996745d08716a84a2aa3a9dd8a8a2f8ef698059a6de08d0a73cfee16af5dd"
observation_id: obs_5dec3dc8c15fa141912780095b8a11fea78e7f8049bbb9143058c91a21a37422
event_id: evt_ec2a4196b7a65859d3593b38945241b3cb408be1746b8e447bb9b5efd4eb7639
revision_id: rev_91217ee0882cf8375075f0ea3406dec6c78ddd2c51fbb98e290987fa7005865c
source_published_at: 2026-09-24T17:45:42Z
first_seen_at: 2026-09-27T01:26:31.077214Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
interpretation_sha256: "sha256:63c3fb83f3004baff01b256c1d2bc0ca1a63afdafede2253815b44eb67b39992"
description: "该工作提出一种面向近场重载水下遥控潜水器（ROV）打捞的目标中心化多视角预测世界模型（C³‑JEPA），利用同步的多摄像头RGB图像与车辆控制信号，在隐空间直接预测任务‑目标状态在接触交互和水体动力滞后下的变化。"
external_url: http://arxiv.org/abs/2609.30214v1
parent_observation_id: null
last_seen_at: 2026-09-27T01:26:31.077214Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30214v1](http://arxiv.org/abs/2609.30214v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Yuncong Yang、Jinlong Li、Yulong Xue 等

## 要点解读

### 这是什么
该工作提出一种面向近场重载水下遥控潜水器（ROV）打捞的目标中心化多视角预测世界模型（C³‑JEPA），利用同步的多摄像头RGB图像与车辆控制信号，在隐空间直接预测任务‑目标状态在接触交互和水体动力滞后下的变化。

### 用在哪里
适用于水下打捞任务中缺少接触传感器的场景，为模型预测控制（MPC）候选方案评估和想象式行为‑智能体训练提供预测接口。相关研究者和机器人系统开发者可借此实现更稳健的状态估计与运动规划。

### 可以推断的
推测：在水体浑浊、光照不均的环境下，多视角融合能够弥补单目视觉的模糊和遮挡，提高目标定位的可靠性。  
推测：轻量化的预测网络使该方法在计算资源受限的机载平台上具备实时运行潜力，适合现场部署。

## 来源摘要/节选

> We present Underwater C$^{3}$-JEPA (cross-view, control-conditioned, context-extended), an object-centric multi-view predictive world model for near-field heavy-load underwater ROV salvage. Without contact sensors, it predicts in latent space how the task-object state evolves through contact interaction and under the hydrodynamic lag of the vehicle, from synchronized multi-view RGB observations and vehicle control signals. C$^{3}$-JEPA encodes multi-camera observations into task-object and context tokens, fuses cross-camera evidence through held-out-view attention, and directly predicts future states conditioned on control. Weak binding anchors the target and gripper at low annotation cost, while SIGReg sharpens the geometric representation. Experiments show that the learned representation transfers substantially more task-relevant information to downstream probes than a reconstruction-free latent baseline, while keeping the predictor lightweight. The resulting predictive interface supports model-predictive-control (MPC) candidate evaluation and imagined-rollout behavior-agent training. Validation on real underwater video shows the same architecture recovering a withheld camera's object state and staying ahead of persistence, so the recipe transfers beyond simulation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。