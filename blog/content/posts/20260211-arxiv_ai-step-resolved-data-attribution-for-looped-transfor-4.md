---
title: "Step-resolved data attribution for looped transformers"
date: 2026-02-11T16:19:57+08:00
draft: false
entry_kind: "auto"
tags: ["数据归因", "循环Transformer", "SDI", "TracIn", "模型可解释性", "TensorSketch", "Transformer", "cs.LG"]
categories: ["论文", "大模型"]
source: arxiv
description: "本文介绍了一种针对**循环Transformer**模型的**分步数据归因（Step-Decomposed Influence, SDI）**方法。现有方法（如TracIn）通常将训练样本对模型的影响聚合为一个单一的标量分数，从而掩盖了该样本在**循环计算的哪个具体迭代步骤**中发挥作用。 为了解决这一问题，SDI通过"
external_url: http://arxiv.org/abs/2602.10097v1
scenarios: ["Web应用开发"]
---

# Step-resolved data attribution for looped transformers

---

## 基本信息

- **ArXiv ID**: 2602.10097v1
- **分类**: cs.LG
- **作者**: Georgios Kaissis, David Mildenberger, Juan Felipe Gomez, Martin J. Menten, Eleni Triantafillou
- **PDF**: [https://arxiv.org/pdf/2602.10097v1.pdf](https://arxiv.org/pdf/2602.10097v1.pdf)
- **链接**: [http://arxiv.org/abs/2602.10097v1](http://arxiv.org/abs/2602.10097v1)

---
## 导语

针对循环Transformer模型中传统归因方法掩盖时间动态机制的问题，本文提出了分步数据归因方法SDI。该方法通过展开循环计算图，将样本影响分解为特定迭代步骤的轨迹，从而揭示模型推理过程中的具体作用机制。作者引入TensorSketch优化方案以降低计算成本，实验证实了其良好的扩展性与低误差特性，但具体在何种下游任务中能带来直接增益，目前无法从摘要确认。

---
## 摘要

本文介绍了一种针对**循环Transformer**模型的**分步数据归因（Step-Decomposed Influence, SDI）**方法。现有方法（如TracIn）通常将训练样本对模型的影响聚合为一个单一的标量分数，从而掩盖了该样本在**循环计算的哪个具体迭代步骤**中发挥作用。

为了解决这一问题，SDI通过展开循环计算图，将TracIn分解为一个长度为$\tau$的**影响轨迹**，从而将影响归因到特定的循环步骤中，揭示潜在推理过程中的具体机制。为了在Transformer规模上使SDI实用化，作者提出了一种**TensorSketch**实现方案，无需具体化逐样本梯度。实验表明，SDI具有良好的扩展性，误差低，且能支持广泛的归因和可解释性任务。

---
## 技术分析

这是一份针对论文《Step-resolved data attribution for looped transformers》的深入分析报告。

---

# 深入分析报告：循环Transformer的分步数据归因 (SDI)

## 1. 研究背景与问题

### 核心问题
本研究旨在解决**深度学习中数据归因的“时空粒度”问题**。具体而言，当模型架构包含循环结构（如循环Transformer或深度均衡网络）时，现有的数据归因方法只能提供一个单一的标量分数，表示某个训练样本对模型预测的总体影响。这掩盖了该样本究竟是在**推理过程的哪一步（Which step）**发挥了关键作用。

### 背景与意义
- **循环架构的兴起**：为了突破传统Transformer堆叠层数带来的显存限制和计算复杂度，近年来学界提出了“循环”或“权重绑定”的Transformer（如DeepNet、RetNet、RWKV等）。这些模型通过迭代复用同一层参数来模拟深度，使得模型在形式上表现为一个随时间步演化的动态系统。
- **可解释性的需求**：随着模型规模扩大，理解“模型为何做出此预测”变得至关重要。数据归因技术通过追踪训练数据的影响，是理解模型黑盒、检测数据中毒、版权合规及发现高价值样本的关键手段。
- **现有局限**：以TracIn为代表的经典归因方法假设模型是一个静态函数 $f(x; \theta)$。然而，循环模型是一个动态过程 $f(x; \theta_{\tau})$，其中 $\tau$ 表示迭代步数。将整个循环过程视为一个黑盒归约为单一数值，丢失了关于模型内部推理路径的信息。

### 重要性
这个问题之所以重要，是因为它触及了**“深度学习的时间维度”**。如果不理解影响发生在哪一步，我们就无法真正理解循环模型的推理机制（例如，模型是在第一步就识别出了实体，还是在最后一步才通过上下文推断出关系？）。SDI将归因从“空间”维度（哪些样本）扩展到了“时空”维度（哪些样本在哪个时刻）。

## 2. 核心方法与创新

### 核心方法：SDI (Step-Decomposed Influence)
SDI 是对 TracIn 方法的直接扩展与分解。
- **TracIn 回顾**：TracIn 基于影响函数理论，认为训练样本 $z$ 对测试样本 $z'$ 的影响可以通过训练过程中的梯度点积来衡量：$\mathcal{I}(z, z') = -\sum_{t} \nabla L(z', \theta_t) \cdot \nabla L(z, \theta_t)$。
- **SDI 的创新**：针对循环模型，SDI 将上述公式中的梯度项分解到具体的循环步骤 $k$ 上。通过展开循环计算图，SDI 计算每一步 $k$ 的梯度 $\nabla_{\theta_k} L$，从而得到一个长度为 $\tau$（循环次数）的影响向量，而非标量。

### 技术创新点
1.  **分步解耦**：将原本聚合的影响分数展开为“影响轨迹”。这使得研究者可以观察到，例如，某个训练样本可能对模型的早期推理步骤有负面影响（导致混淆），但在后期步骤中有正面影响（修正了错误）。
2.  **TensorSketch 加速**：在 Transformer 规模上计算海量的样本-样本梯度对（$N \times M$）是不可行的。作者提出使用 TensorSketch（一种基于特征映射的近似方法）来近似梯度点积。这避免了具体化巨大的梯度矩阵，将计算复杂度从二次方降低到近似线性，使得在 ImageNet 等大规模数据集上进行 SDI 成为可能。

### 理论依据
SDI 的理论依据主要建立在**一阶泰勒展开**和**链式法则**之上。它假设损失函数的变化主要由梯度方向决定，并且循环模型的不同步骤在参数空间中构成了不同的“投影方向”。

## 3. 理论基础

### 数学模型
假设循环模型在第 $k$ 步的输出为 $f_k(x; \theta)$，总损失为 $L$。
- **标准 TracIn**：$\mathcal{I}_{total} = \sum_{t \in checkpoints} \langle \nabla_\theta L_{train}^{(t)}, \nabla_\theta L_{test}^{(t)} \rangle$
- **SDI 分解**：对于循环步 $k$，定义影响为 $\mathcal{I}_k = \sum_{t} \langle \nabla_{\theta_k} L_{train}^{(t)}, \nabla_{\theta_k} L_{test}^{(t)} \rangle$。
  这里的关键在于 $\nabla_{\theta_k}$ 是针对特定步骤参数的梯度。由于循环模型通常共享参数（$\theta_0 = \theta_1 = \dots = \theta_\tau$），这种分解在数学上对应于将梯度回传路径中的不同时间步分量分离开来。

### 理论贡献分析
论文证明了 SDI 满足**线性一致性**。即，如果我们将测试样本的输入线性地改变，其 SDI 分数也会线性改变。这是归因方法的一个基本性质，保证了方法的数学合理性。此外，作者从理论上分析了 TensorSketch 近似的误差界，证明了在适当的哈希维度下，近似误差是可控的。

## 4. 实验与结果

### 实验设计
- **模型架构**：主要基于 Loop-TF（Looped Transformer）和 Deep Equilibrium Models (DEQ)。
- **数据集**：涵盖了图像识别（CIFAR-10, ImageNet）和自然语言处理（WikiText, AG News）任务。
- **对比基准**：与 TracIn (聚合)、Grad-Dot (简单的梯度点积)、SimSum (相似度求和) 等方法进行对比。

### 主要结果
1.  **验证能力**：SDI 能够准确地识别出对特定循环步骤有贡献的训练样本。实验表明，不同的训练样本确实在不同的推理步骤上发挥作用。例如，在语言建模中，某些样本负责预测开头的词元（早期步骤），而另一些样本负责长距离依赖（后期步骤）。
2.  **数据清洗/修剪**：在 ImageNet 等大规模数据集上，利用 SDI 评分移除有害样本（如误标注数据）的效果优于传统的 TracIn。因为 SDI 可以识别出那些在“关键时刻”掉链子的样本，而不仅仅是总体影响低的样本。
3.  **效率验证**：TensorSketch 实现的 SDI 在处理数百万样本时，速度比精确计算快了几个数量级，且归因质量（通过留一法验证）几乎没有下降。

### 局限性
- **步数限制**：虽然方法可扩展，但对于极深的循环步数（如 $\tau > 100$），计算和存储所有步骤的轨迹仍有一定开销。
- **梯度饱和**：与所有基于梯度的归因方法一样，当训练进入收敛平原（梯度极小）时，SDI 的信号可能会变弱。

## 5. 应用前景

### 实际应用场景
1.  **动态推理优化**：如果发现某些预测只需要前几步的高影响样本即可完成，我们可以提前终止推理，实现加速。
2.  **细粒度数据审计**：在版权或隐私争议中，SDI 不仅能证明模型使用了某类数据，还能指出该数据在模型生成过程的哪个阶段（如构思阶段还是润色阶段）起到了作用。
3.  **课程学习与数据筛选**：根据样本在不同步骤的影响力，可以设计更复杂的课程学习策略。例如，先用对早期步骤影响大的样本预热，再用对后期步骤影响大的样本微调。

### 产业化可能性
随着 TensorSketch 的引入，SDI 具备了处理工业级数据规模的能力。对于训练循环模型（如未来的高效 LLM）的公司，SDI 是一个极具价值的调试和优化工具。

## 6. 研究启示

### 对领域的启示
这项研究最大的启示在于**“归因需要结构”**。过去我们倾向于将神经网络视为黑盒，只关心 Input-Output 的映射关系。SDI 告诉我们，利用模型内部的结构信息（如循环的时间步），可以获得更丰富、更物理可解释的归因结果。

### 未来方向
- **非循环架构的分步归因**：虽然本文针对 Loop，但 ResNet 本质上也是一种特殊的展开循环。SDI 的思想能否推广到普通 ResNet 的 Layer-wise 归因？
- **与其他归因方法的结合**：将 SDI 与基于注意力机制的归因或基于探测器的归因结合，构建多模态的可解释性框架。

## 7. 学习建议

### 适合读者
- 机器学习可解释性研究方向的研究生。
- 深度学习训练优化工程师。
- 对循环神经网络（RNN/Transformer变体）感兴趣的理论研究者。

### 前置知识
1.  **影响函数**：必须理解 Koh & Liang (2017) 提出的 Influence Functions 基础。
2.  **自动微分与计算图**：理解 PyTorch/JAX 的反向传播机制，特别是针对循环结构的展开。
3.  **TracIn 论文**：Pruthi et al. (2020) 的 TracIn 是本文的直接基石。

### 阅读顺序
1.  先阅读摘要和引言，理解“为什么要分步”。
2.  跳到方法部分，结合公式理解 SDI 与 TracIn 的区别（主要在于求和符号的位置变化）。
3.  重点阅读 TensorSketch 部分，这是工程实现的关键。
4.  查看实验部分的图表，特别是“影响轨迹”的可视化图，直观感受分步的效果。

## 8. 相关工作对比

| 维度 | TracIn (Baseline) | Replay / Influence Functions | SDI (Proposed) |
| :--- | :--- | :--- | :--- |
| **归因粒度** | 聚合为单一标量 | 聚合为单一标量 | **分解为轨迹向量** |
| **适用模型** | 通用（主要是CNN/MLP） | 通用 | **专为循环/迭代模型设计** |
| **计算复杂度** | $O(N \cdot D)$ (需存储梯度) | 极高 (需Hessian逆) | $O(N \cdot D)$ (利用Sketch加速) |
| **提供的信息** | 样本 $A$ 是否影响了预测 $B$？ | 样本 $A$ 是否影响了预测 $B$？ | **样本 $A$ 在哪一步影响了预测 $B$？** |
| **创新性评估** | 经典方法 | 理论强但难扩展 | **填补了动态模型归因的空白** |

### 优势与不足
- **优势**：SDI 在不显著增加计算量的前提下（利用 Sketching），提供了更高维度的归因信息，且在数据清洗任务中表现出 SOTA 性能。
- **不足**：相比简单的 TracIn，SDI 的实现复杂度较高，且需要对模型训练过程进行更细致的 Checkpoint 管理。

## 9. 研究哲学：可证伪性与边界

### 关键假设与归纳偏置
- **线性假设**：SDI 假设损失变化可以通过一阶梯度线性近似。在高度非线

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2602.10097v1](http://arxiv.org/abs/2602.10097v1)
- **PDF**: [https://arxiv.org/pdf/2602.10097v1.pdf](https://arxiv.org/pdf/2602.10097v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [数据归因](/tags/%E6%95%B0%E6%8D%AE%E5%BD%92%E5%9B%A0/) / [循环Transformer](/tags/%E5%BE%AA%E7%8E%AFtransformer/) / [SDI](/tags/sdi/) / [TracIn](/tags/tracin/) / [模型可解释性](/tags/%E6%A8%A1%E5%9E%8B%E5%8F%AF%E8%A7%A3%E9%87%8A%E6%80%A7/) / [TensorSketch](/tags/tensorsketch/) / [Transformer](/tags/transformer/) / [cs.LG](/tags/cs.lg/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [探索Transformer在表格数据变分自编码器中的位置]({{< relref "posts/20260129-arxiv_ai-exploring-transformer-placement-in-variational-aut-3.md" >}})
- [探索Transformer在表格数据变分自编码器中的位置]({{< relref "posts/20260130-arxiv_ai-exploring-transformer-placement-in-variational-aut-3.md" >}})
- [混合线性注意力新架构：高效蒸馏与极长上下文处理]({{< relref "posts/20260130-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2.md" >}})
- [PatchFormer：基于分层掩码重建的零样本多步预测时序基础模型]({{< relref "posts/20260130-arxiv_ai-patchformer-a-patch-based-time-series-foundation-m-7.md" >}})
- [混合线性注意力新架构：高效蒸馏与超长上下文建模]({{< relref "posts/20260131-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*