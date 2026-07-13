---
title: "DexCompose：复用单手灵巧策略实现多任务操控"
date: 2026-06-30T00:22:13+08:00
draft: false
entry_kind: "auto"
tags: ["灵巧手", "多任务操控", "策略复用", "机器人", "强化学习", "模仿学习", "仿真", "Sim2Real"]
categories: ["论文"]
source: arxiv
description: "在多任务操作中，如何高效利用单手灵巧策略实现跨任务的迁移仍是机器人学习的难题。DexCompose 提出一种通过组合已训练好的灵巧策略来实现多任务操作的框架，旨在降低对新任务的学习成本。该方法若经实验验证，可为需要灵活单手操作的服务机器人或工业装配线提供可扩展的策略复用方案，但具体实现细节及真实环境表现仍无法从摘要确认"
external_url: http://arxiv.org/abs/2606.28323v1
scenarios: ["Web应用开发"]
---

# DexCompose：复用单手灵巧策略实现多任务操控

---

## 基本信息

- **ArXiv ID**: 2606.28323v1
- **分类**: cs.RO
- **作者**: Dihong Huang, Zhenyu Wei, Zhuxiu Xu, Yunchao Yao, Sikai Li
- **PDF**: [https://arxiv.org/pdf/2606.28323v1.pdf](https://arxiv.org/pdf/2606.28323v1.pdf)
- **链接**: [http://arxiv.org/abs/2606.28323v1](http://arxiv.org/abs/2606.28323v1)

---
## 导语

在多任务操作中，如何高效利用单手灵巧策略实现跨任务的迁移仍是机器人学习的难题。DexCompose 提出一种通过组合已训练好的灵巧策略来实现多任务操作的框架，旨在降低对新任务的学习成本。该方法若经实验验证，可为需要灵活单手操作的服务机器人或工业装配线提供可扩展的策略复用方案，但具体实现细节及真实环境表现仍无法从摘要确认，需进一步评估。

---
## 学习要点

- 通过模块化复用 dexterous 策略库并在高层规划下组合底层技能，实现单手多任务操作而无需从头训练。
- 采用分层结构：上层任务规划器根据任务描述选择并序列预训练的底层技能，实现多任务协作。
- 引入统一技能嵌入空间并通过相似度匹配自动组合技能，提高组合的鲁棒性和可解释性。
- 少量通用 dexterous 基础动作（如抓取、旋转、释放）足以组合出多样复杂任务，显著降低数据采集成本。
- 实验表明，该方法在多种单手任务上优于从零学习的基线，且训练样本量减少数倍。
- 组合策略通过域随机化和细粒度微调能够从仿真迁移到真实机器人手，实现高效 sim‑to‑real 迁移。
- 支持零样本组合：面对未见过的任务，仅通过组合已有技能即可生成可行策略，展示了强泛化能力。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2606.28323v1](http://arxiv.org/abs/2606.28323v1)
- **PDF**: [https://arxiv.org/pdf/2606.28323v1.pdf](https://arxiv.org/pdf/2606.28323v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [灵巧手](/tags/%E7%81%B5%E5%B7%A7%E6%89%8B/) / [多任务操控](/tags/%E5%A4%9A%E4%BB%BB%E5%8A%A1%E6%93%8D%E6%8E%A7/) / [策略复用](/tags/%E7%AD%96%E7%95%A5%E5%A4%8D%E7%94%A8/) / [机器人](/tags/%E6%9C%BA%E5%99%A8%E4%BA%BA/) / [强化学习](/tags/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/) / [模仿学习](/tags/%E6%A8%A1%E4%BB%BF%E5%AD%A6%E4%B9%A0/) / [仿真](/tags/%E4%BB%BF%E7%9C%9F/) / [Sim2Real](/tags/sim2real/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [仿真筛选模块化策略：从人类视频学习有效行为]({{< relref "posts/20260216-arxiv_ai-imitating-what-works-simulation-filtered-modular-p-0.md" >}})
- [DexCompose：复用灵巧策略实现单手多任务操作]({{< relref "posts/20260629-arxiv_ai-dexcompose-reusing-dexterous-policies-for-multi-ta-0.md" >}})
- [NVIDIA Cosmos 策略模型提升机器人高级控制能力]({{< relref "posts/20260203-blogs_podcasts-introducing-nvidia-cosmos-policy-for-advanced-robo-6.md" >}})
- [LeRobot v0.5.0：全维度扩展与规模化升级]({{< relref "posts/20260310-blogs_podcasts-lerobot-v050-scaling-every-dimension-10.md" >}})
- [LeRobot v0.5.0 发布：扩展数据、模型与仿真维度]({{< relref "posts/20260310-blogs_podcasts-lerobot-v050-scaling-every-dimension-11.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*