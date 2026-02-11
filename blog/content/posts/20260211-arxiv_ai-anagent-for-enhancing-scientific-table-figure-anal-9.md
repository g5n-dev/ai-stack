---
title: "用于增强科学图表分析的Agent框架"
date: 2026-02-11T10:45:51+08:00
draft: false
entry_kind: "auto"
tags: ["Anagent", "多智能体", "科学图表", "AnaBench", "SFT", "强化学习", "多模态", "长上下文"]
categories: ["大模型", "论文"]
source: arxiv
description: "本文介绍了一种名为 **Anagent** 的多智能体框架，旨在提升对科学图表（Tables & Figures）的分析能力。以下是内容的简要总结： **1. 研究背景与挑战** 科学研究中的图表分析需要准确解读复杂的多模态知识、整合不同来源的证据，并结合领域知识进行推理。然而，目前的 AI 系统在面对结构各异、复杂多"
external_url: http://arxiv.org/abs/2602.10081v1
scenarios: ["Web应用开发"]
---

# 用于增强科学图表分析的Agent框架

---

## 基本信息

- **ArXiv ID**: 2602.10081v1
- **分类**: cs.CL
- **作者**: Xuehang Guo, Zhiyong Lu, Tom Hope, Qingyun Wang
- **PDF**: [https://arxiv.org/pdf/2602.10081v1.pdf](https://arxiv.org/pdf/2602.10081v1.pdf)
- **链接**: [http://arxiv.org/abs/2602.10081v1](http://arxiv.org/abs/2602.10081v1)

---
## 导语

针对当前 AI 系统难以有效解析复杂科学图表的挑战，本文提出了 Anagent，这是一个包含规划、专家、解决及评判四个模块的多智能体协作框架。作者还构建了覆盖多学科的大规模基准 AnaBench 以验证其性能。该框架展示了通过多智能体分工处理长上下文与多模态信息的潜力，但其在真实科研工作流中的具体效能尚无法从摘要确认。

---
## 摘要

本文介绍了一种名为 **Anagent** 的多智能体框架，旨在提升对科学图表（Tables & Figures）的分析能力。以下是内容的简要总结：

**1. 研究背景与挑战**
科学研究中的图表分析需要准确解读复杂的多模态知识、整合不同来源的证据，并结合领域知识进行推理。然而，目前的 AI 系统在面对结构各异、复杂多变且包含长上下文的科学图表时，仍面临巨大困难。

**2. 新基准：AnaBench**
为了量化这些挑战，研究团队推出了 **AnaBench**，这是一个包含 63,178 个实例的大规模基准测试，覆盖九个科学领域，并系统性地沿七个复杂性维度进行了分类。

**3. 解决方案：Anagent 框架**
Anagent 是一个包含四个专门智能体的多智能体框架，通过协作解决问题：
*   **Planner（规划者）：** 将任务分解为可执行的子任务。
*   **Expert（专家）：** 通过执行特定工具检索任务相关信息。
*   **Solver（解决者）：** 综合信息以生成连贯的分析结果。
*   **Critic（评判者）：** 通过五维质量评估进行迭代优化。

**4. 训练策略与成果**
研究还开发了模块化训练策略，结合监督微调（SFT）和专门的强化学习来优化各智能体的能力及协作效果。在 170 个子领域的综合评估中，Anagent 表现出色：
*   在**无训练**（Training-free）设置下，性能提升最高达 **13.43%**。
*   在**微调**（Finetuning）后，性能提升最高达 **42.12%**。

**结论**
结果表明，面向任务的推理和上下文感知的问题解决对于高质量的科学图表分析至关重要。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2602.10081v1](http://arxiv.org/abs/2602.10081v1)
- **PDF**: [https://arxiv.org/pdf/2602.10081v1.pdf](https://arxiv.org/pdf/2602.10081v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [Anagent](/tags/anagent/) / [多智能体](/tags/%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93/) / [科学图表](/tags/%E7%A7%91%E5%AD%A6%E5%9B%BE%E8%A1%A8/) / [AnaBench](/tags/anabench/) / [SFT](/tags/sft/) / [强化学习](/tags/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/) / [多模态](/tags/%E5%A4%9A%E6%A8%A1%E6%80%81/) / [长上下文](/tags/%E9%95%BF%E4%B8%8A%E4%B8%8B%E6%96%87/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Kimi K2.5震撼开源！视觉SOTA Agent模型，性能炸裂🔥]({{< relref "posts/20260127-hacker_news-kimi-released-kimi-k25-open-source-visual-sota-age-2.md" >}})
- [基于认知上下文学习构建大模型多智能体系统的信任机制]({{< relref "posts/20260130-arxiv_ai-epistemic-context-learning-building-trust-the-righ-7.md" >}})
- [RE-TRAC：面向深度搜索智能体的递归轨迹压缩方法]({{< relref "posts/20260203-arxiv_ai-re-trac-recursive-trajectory-compression-for-deep--4.md" >}})
- [视觉语言模型能否通过交互学习直觉物理]({{< relref "posts/20260206-arxiv_ai-can-vision-language-models-learn-intuitive-physics-5.md" >}})
- [视觉语言模型能否通过交互学习直观物理]({{< relref "posts/20260207-arxiv_ai-can-vision-language-models-learn-intuitive-physics-5.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*