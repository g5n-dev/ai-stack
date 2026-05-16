---
title: "EntityBench：多镜头长视频生成中的实体一致性评估"
date: 2026-05-16T08:19:20+08:00
draft: false
entry_kind: "auto"
tags: ["视频生成", "实体一致性", "多镜头", "基准", "数据集", "长视频", "跨镜头", "评估指标"]
categories: ["论文", "数据"]
source: arxiv
description: "研究背景 多镜头视频生成将单镜头生成扩展为连贯的视觉叙事，但在长序列中保持角色、物体和场景的一致性仍是难题。现有评估往往使用独立的提示集，覆盖实体有限且度量简单，难以进行标准化比较。 核心贡献 提出 EntityBench，一个包含140部剧集、共2,491个镜头的基准。数据来源于真实叙事媒体，并为每个镜头提供实体调度"
external_url: http://arxiv.org/abs/2605.15199v1
scenarios: ["Web应用开发"]
---

# EntityBench：多镜头长视频生成中的实体一致性评估

---

## 基本信息

- **ArXiv ID**: 2605.15199v1
- **分类**: cs.CV
- **作者**: Ruozhen He, Meng Wei, Ziyan Yang, Vicente Ordonez
- **PDF**: [https://arxiv.org/pdf/2605.15199v1.pdf](https://arxiv.org/pdf/2605.15199v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.15199v1](http://arxiv.org/abs/2605.15199v1)

---
## 导语

多镜头视频生成需在长序列中维持角色、物体和场景的一致性，这仍是当前技术面临的主要挑战。为系统评估模型的实体一致性保持能力，研究者提出EntityBench基准，包含140部剧集共2,491个镜头，按难度分级并配套三支柱评估体系，同时提出记忆增强的EntityMem方法。实验表明随复发距离增加，一致性性能急剧下降，EntityMem在角色忠实度上取得显著提升。该基准为视频生成与评估提供了新的参考。

---
## 摘要

#### 研究背景
多镜头视频生成将单镜头生成扩展为连贯的视觉叙事，但在长序列中保持角色、物体和场景的一致性仍是难题。现有评估往往使用独立的提示集，覆盖实体有限且度量简单，难以进行标准化比较。

#### 核心贡献
提出 EntityBench，一个包含140部剧集、共2,491个镜头的基准。数据来源于真实叙事媒体，并为每个镜头提供实体调度表，覆盖角色、物体和场景，分为易/中/难三档：最长50镜头、13个跨镜头角色、8个跨镜头场景、22个跨镜头物体，以及最远48镜头间隔的复发缺口。

#### 评估体系
基准配套三支柱评估套件：镜头内质量、提示遵循度以及跨镜头一致性，并加入保真门机制，仅对准确出现的实体计入跨镜头得分，以防止错误实体误导评估。

#### 基线模型
在生成前，EntityMem 将已验证的每实体视觉特征存入持久记忆库，实现记忆增强的视频生成。

#### 实验结果
对比主流方法发现，随着复发距离增加，跨镜头实体一致性急剧下降。EntityMem 在角色忠实度上取得最高效应量（Cohen's d = +2.33），并在实体出现率上领先。代码与数据已开源于 GitHub（https://github.com/Catherine-R-He/EntityBench/）。

---
## 学习要点

- EntityBench首次提出针对长程多镜头视频生成中实体一致性的系统性评估框架，为模型提供明确的性能基准。
- 通过定义实体一致性分数（ECS）等专用指标，弥补了传统视频质量指标（如FID）在身份保持方面的不足。
- 该基准包含多样化场景、角色及相机切换，覆盖真实世界复杂交互，以全面检验模型的鲁棒性。
- 实验结果显示，当前主流视频生成模型在高时长或多镜头切换后仍出现显著的外观漂移和身份错误。
- 为提升实体一致性，模型需引入跨帧记忆机制和细粒度特征对齐结构，这一发现指明了后续架构改进方向。
- EntityBench提供开源评测脚本和公开数据集，使研究者能够快速复现并对比不同方法的实体保持能力。
- 基准测试还揭示了光照变化、遮挡和大幅度姿态变化对实体一致性的影响，为后续数据集扩充和难点突破提供依据。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.15199v1](http://arxiv.org/abs/2605.15199v1)
- **PDF**: [https://arxiv.org/pdf/2605.15199v1.pdf](https://arxiv.org/pdf/2605.15199v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/) / [数据](/categories/%E6%95%B0%E6%8D%AE/)
- 标签： [视频生成](/tags/%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90/) / [实体一致性](/tags/%E5%AE%9E%E4%BD%93%E4%B8%80%E8%87%B4%E6%80%A7/) / [多镜头](/tags/%E5%A4%9A%E9%95%9C%E5%A4%B4/) / [基准](/tags/%E5%9F%BA%E5%87%86/) / [数据集](/tags/%E6%95%B0%E6%8D%AE%E9%9B%86/) / [长视频](/tags/%E9%95%BF%E8%A7%86%E9%A2%91/) / [跨镜头](/tags/%E8%B7%A8%E9%95%9C%E5%A4%B4/) / [评估指标](/tags/%E8%AF%84%E4%BC%B0%E6%8C%87%E6%A0%87/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [模式寻优结合均值寻优实现快速长视频生成]({{< relref "posts/20260302-arxiv_ai-mode-seeking-meets-mean-seeking-for-fast-long-vide-0.md" >}})
- [模式寻优与均值寻优结合实现快速长视频生成]({{< relref "posts/20260303-arxiv_ai-mode-seeking-meets-mean-seeking-for-fast-long-vide-0.md" >}})
- [评估学习表征可识别性的挑战与难点]({{< relref "posts/20260303-arxiv_ai-who-guards-the-guardians-the-challenges-of-evaluat-6.md" >}})
- [🔍脑电+情感=超强分析！MEG数据解锁情绪新维度]({{< relref "posts/20260127-arxiv_ai-megnifying-emotion-sentiment-analysis-from-annotat-2.md" >}})
- [基于相机-IMU融合的鲁棒路面分类数据集与框架]({{< relref "posts/20260129-arxiv_ai-a-new-dataset-and-framework-for-robust-road-surfac-6.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*