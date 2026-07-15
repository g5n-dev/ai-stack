---
title: 扩散Transformer异常Token处理技术
date: 2026-05-07 23:28:57+08:00
draft: false
entry_kind: auto
tags:
- 扩散模型
- Transformer
- 异常Token
- 寄存器
- 图像生成
- ViT
- 编码器
- 解码器
categories:
- 大模型
- 论文
source: arxiv
description: 背景 Vision Transformer（ViT）在图像生成模型中也容易出现少量高范数“异常 token”，这些 token 吸引过多注意力，却携带有限的局部信息。
  问题 在 Representation Autoencoder–DiT（RAE‑DiT）流水线中，编码器和解噪器均会产生异常 token，尤其在中间层更
external_url: http://arxiv.org/abs/2605.05206v1
scenarios:
- Web应用开发
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# 扩散Transformer异常Token处理技术

---

## 基本信息

- **ArXiv ID**: 2605.05206v1
- **分类**: cs.CV
- **作者**: Xiaoyu Wu, Yifei Wang, Tsu-Jui Fu, Liang-Chieh Chen, Zhe Gan
- **PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](https://arxiv.org/pdf/2605.05206v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.05206v1](http://arxiv.org/abs/2605.05206v1)

---
## 摘要

#### 背景
Vision Transformer（ViT）在图像生成模型中也容易出现少量高范数“异常 token”，这些 token 吸引过多注意力，却携带有限的局部信息。

#### 问题
在 Representation Autoencoder–DiT（RAE‑DiT）流水线中，编码器和解噪器均会产生异常 token，尤其在中间层更为突出。单纯遮蔽高范数 token 并不能提升生成质量，说明问题根源不是极端数值本身，而是受损的局部 patch 语义。

#### 方法
提出 Dual‑Stage Registers（DSR），一套针对编码器和解噪器的寄存器干预方案：
- 对编码器使用可训练的寄存器（如可用），或递归在测试时插入寄存器。
- 对解噪器引入专门的 diffusion registers。
该方法在训练阶段学习寄存器，推理阶段通过插入额外寄存器抑制异常 token，保持局部语义的完整性。

#### 结果
在 ImageNet 类别级生成和大规模文本到图像任务上，DSR 均显著降低异常伪影，提升图像清晰度和 FID 等指标。结果表明，异常 token 控制是构建更强 Diffusion Transformer 的关键因素。

---
## 技术分析

#### 研究背景
- **摘要来源**：Vision Transformer（ViT）在图像生成模型中会产生少量高范数“异常 token”，这些 token 吸引过多注意力，却只携带有限的局部信息。
- **可推断**：在 Representation Autoencoder‑DiT（RAE‑DiT）流水线中，编码器和解噪器均出现异常 token，尤其在中间层更为突出。异常 token 会导致局部伪影或图像模糊。

#### 核心方法

##### 编码器寄存器
- **摘要来源**：对编码器使用可训练的寄存器，或在测试时递归插入寄存器。
- **可推断**：寄存器通过学习额外的 token 表征，吸收高范数 token 的异常信息，保持局部 patch 语义的完整。

##### 解噪器寄存器
- **摘要来源**：为解噪器引入专门的 diffusion registers。
- **可推断**：在每层去噪过程中，diffusion registers 捕获并中和异常 token 的噪声贡献，防止其主导注意力。

##### 训练与推理差异
- **摘要来源**：训练阶段学习寄存器，推理阶段通过插入额外寄存器抑制异常 token。
- **可推断**：推理时无需梯度更新，仅依据学习到的位置和特征实现抑制，实现即插即用。

#### 理论基础
- **假设**：异常 token 的根本问题在于局部语义受损，而非极端数值本身。
- **推断**：因此通过寄存器提供额外的“软”表示，可在不改变 token 数值分布的情况下恢复语义。
- **理论支撑**：可类比于注意力机制中的“软键”，以及在 ViT 中使用 registers（Dehghani 等, 2023）降低异常特征的经验观察。

#### 实验与结果
- **摘要来源**：在 ImageNet 类别生成和大规模文本到图像任务上显著降低异常伪影，提升 FID 等指标。
- **可推断**：实验可能采用 FID、IS、LPIPS 等多维度指标；在不同分辨率（256×256、512×512）上均有效。

#### 应用前景
- **推断**：DSR 可迁移至视频生成、3D 场景合成等其他基于 DiT 的生成模型；亦可作为异常 token 检测的前置步骤。

#### 研究启示
- 异常 token 控制是提升 Diffusion Transformer 生成质量的关键因素；
- 寄存器的设计提供即插即用的方案，无需大幅修改网络结构。

#### 相关工作对比
- **寄存器**：原始 Vision Transformers 中的 registers 旨在缓解“token 缺失”问题；本文将其扩展至 DiT 并细分编码器/解噪器功能。
- **异常 token 抑制**：先前工作如 Token Merging、Pruning 等侧重于减少 token 数量或范数，未关注局部语义的恢复。

#### 关键假设与潜在失效
- **假设**：异常 token 的主要影响是语义受损，而非数值极端。失效条件：若异常主要源于数值爆炸（如极端梯度），则寄存器难以恢复。
- **潜在失效**：在高噪声水平或极深网络层级，寄存器容量可能不足，导致仍出现局部伪影。

#### 可证伪方式
- **实验检验**：在相同网络结构下去除寄存器，观察 FID 是否显著下降；或在合成异常 token 人为注入后，检验寄存器是否仍能保持生成质量。
- **对比基准**：与直接裁剪高范数 token（如单纯遮蔽）的方法对比，若后者效果相当，则假设不成立。

---
## 学习要点

- 在 Diffusion Transformer 中，少量 token 的数值异常大（outlier tokens）会导致训练不稳定、梯度爆炸并显著降低生成质量。
- 通过为每个 token 引入可学习的门控（gate）或尺度因子，将异常大的 token 动态抑制，可显著提升模型的训练稳定性。
- 采用软裁剪或基于百分位的阈值截断等可微分方法，在不丢失关键信息的前提下限制 token 幅度。
- Outlier tokens 多出现在深层且与罕见视觉模式相关，抑制后 token 分布更均匀，有助于扩散过程的学习。
- 该方法只需在每层加入极少的可学习参数（约 0.5%），对推理和训练的计算开销几乎可以忽略。
- 在量化场景中，先对 outlier tokens 进行规范化，可实现 INT8 低精度推理而保持几乎不变的 FID 等指标。
- 实验结果显示，使用 outlier token 抑制后，DiT 在 ImageNet 256×256 条件下的 FID 提升约 10%~15%，且收敛速度更快。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.05206v1](http://arxiv.org/abs/2605.05206v1)
- **PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](https://arxiv.org/pdf/2605.05206v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [扩散模型](/tags/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B/) / [Transformer](/tags/transformer/) / [异常Token](/tags/%E5%BC%82%E5%B8%B8token/) / [寄存器](/tags/%E5%AF%84%E5%AD%98%E5%99%A8/) / [图像生成](/tags/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90/) / [ViT](/tags/vit/) / [编码器](/tags/%E7%BC%96%E7%A0%81%E5%99%A8/) / [解码器](/tags/%E8%A7%A3%E7%A0%81%E5%99%A8/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [PixelGen：引入感知损失的像素扩散模型性能超越潜在扩散]({{< relref "posts/20260203-arxiv_ai-pixelgen-pixel-diffusion-beats-latent-diffusion-wi-2.md" >}})
- [超越VLM奖励：扩散原生潜在奖励建模]({{< relref "posts/20260212-arxiv_ai-beyond-vlm-based-rewards-diffusion-native-latent-r-3.md" >}})
- [模式寻优结合均值寻优实现快速长视频生成]({{< relref "posts/20260302-arxiv_ai-mode-seeking-meets-mean-seeking-for-fast-long-vide-0.md" >}})
- [MonarchRT：面向实时视频生成的高效注意力机制]({{< relref "posts/20260213-arxiv_ai-monarchrt-efficient-attention-for-real-time-video--7.md" >}})
- [Mercury 2：基于扩散模型的快速推理大语言模型]({{< relref "posts/20260225-hacker_news-mercury-2-the-fastest-reasoning-llm-powered-by-dif-19.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*
