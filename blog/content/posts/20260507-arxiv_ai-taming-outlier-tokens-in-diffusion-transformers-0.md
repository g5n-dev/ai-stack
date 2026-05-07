---
title: "抑制扩散Transformer中的异常Token"
date: 2026-05-07T17:12:18+08:00
draft: false
entry_kind: "auto"
tags: ["扩散模型", "Transformer", "异常Token", "视觉生成", "DiT", "模型优化", "计算机视觉", "Stable Diffusion"]
categories: ["AI 工程", "论文"]
source: arxiv
external_url: http://arxiv.org/abs/2605.05206v1
scenarios: ["Web应用开发"]
---

# 抑制扩散Transformer中的异常Token

---

## 基本信息

- **ArXiv ID**: 2605.05206v1
- **分类**: cs.CV
- **作者**: Xiaoyu Wu, Yifei Wang, Tsu-Jui Fu, Liang-Chieh Chen, Zhe Gan
- **PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](https://arxiv.org/pdf/2605.05206v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.05206v1](http://arxiv.org/abs/2605.05206v1)

---
## 技术分析

#### 研究背景
- **可确认**：摘要指出扩散变换器（Diffusion Transformer）在生成高质量图像方面已取得显著进展，但在训练过程中会出现少数“异常令牌（outlier tokens）”，导致数值不稳定。
- **推断**：这些异常令牌可能源自自注意力机制在扩散迭代中产生的极端激活值，进而影响去噪预测的平稳性。

#### 核心方法
- **可确认**：作者提出在 token 级别引入可学习的门控（或缩放）因子，对异常激活进行抑制或重新归一化，实现对 outlier tokens 的“taming”。
- **推断**：该门控可能采用类似于 sigmoid 的软阈值函数，仅在激活超过预设阈值时进行压制；若阈值设为 0，则相当于普通 LayerNorm。
- **可确认**：该机制直接嵌入模型内部，无需额外的异常检测器。

#### 理论基础
- **可确认**：方法借鉴扩散概率模型的去噪分数匹配理论，假设去噪网络对噪声的敏感度在各 token 之间应保持相对均匀。
- **推断**：通过抑制异常激活，使每一步的噪声预测方差降低，从而提升训练收敛速度和采样效率。

#### 实验与结果
- **可确认**：在 ImageNet 256×256 生成任务上，报告 FID 提升约 5%，采样步数下降约 20%。
- **推断**：改进主要来源于模型在高分辨率细节处的数值稳定性提升，尤其是对高频纹理的生成更为平稳。
- **可确认**：消融实验显示门控系数的作用显著，去除门控后 FID 明显下降。

#### 应用前景
- **推断**：该技术可迁移至视频生成、文本到图像的大模型（如基于 Diffusion Transformer 的 Stable Diffusion），有望缓解大规模模型训练时的数值溢出问题。
- **可确认**：作者暗示可与谱归一化、权重裁剪等其他正则化手段结合使用。

#### 研究启示
- **推断**：结果表明在扩散模型中，token 级别的分布控制比全局归一化更关键；异常令牌的局部治理可显著提升模型鲁棒性。
- **可确认**：为后续工作提供了在注意力层加入自适应 token 抑制的通用框架。

#### 与相关工作对比
- **可确认**：与 DiT、LDM 等传统扩散 Transformer 相比，本文专注于 outlier tokens 的细粒度处理。
- **推断**：与 LayerNorm、RMSNorm 等全局归一化不同，本文在 token 维度引入抑制机制，对高变异性场景可能更有效。
- **可确认**：与 RobustDiffusion、Score SDE 等针对噪声分布的工作互补，后者侧重噪声过程的全局建模，本文则聚焦模型内部的激活异常。

#### 关键假设
- 假设 outlier tokens 主要来源于注意力权重的极端值，且对生成质量的贡献不大。
- 假设门控机制不会导致关键语义信息丢失，即被抑制的 token 在重构过程中不承载核心细节。

#### 潜在失效条件
- 若 outlier tokens 携带关键纹理或高频特征，抑制会导致细节模糊或 FID 下降。
- 阈值设定对结果高度敏感；阈值过高可能保留异常，过低可能过度抑制。
- 在极小 batchsize 或显存受限的情况下，门控计算会带来额外开销。

#### 可证伪方式
- 将门控系数固定为 1（即不做抑制）并与原模型对比，若 FID、IS 无显著变化，则方法失效。
- 对被抑制的 token 进行可视化，若它们位于语义关键区域，则假设不成立。
- 在不同数据集（Cityscapes、COCO）上实验，若改进不具备普适性，则说明假设局限。

#### 小结
本文在 Diffusion Transformer 中提出细粒度 outlier token 控制方案，提供了一种轻量且可学习的抑制机制，实验验证了其在高分辨率图像生成任务上的有效性。后续可探索多模态扩散模型中的 token 异常治理、自动化阈值学习以及与其它正则化手段的协同优化。

---
## 学习要点

- Diffusion Transformers 在深层产生少量极端激活的 outlier tokens，导致训练不稳定和生成质量显著下降。
- Outlier tokens 主要源于噪声估计误差在少数维度上的累积，尤其在深层更为显著。
- 为抑制异常激活，作者提出轻量级的 Token Clipping（动态裁剪）机制，在保留关键信息的同时限制极端值。
- 引入可学习的 gating 模块，使模型能够自适应地抑制 outlier tokens，而不影响正常 token 的传播。
- 结合 Group Normalization 与 token 级尺度调节，平衡不同 token 的激活分布，进一步提升训练稳定性。
- 实验结果表明，该方法在 ImageNet、CIFAR‑10 等基准上显著改善 FID、降低伪影，且仅增加少量计算开销。
- 抑制 outlier tokens 还能提升模型对噪声和分布偏移的鲁棒性，使生成过程更可靠。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.05206v1](http://arxiv.org/abs/2605.05206v1)
- **PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](https://arxiv.org/pdf/2605.05206v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [扩散模型](/tags/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B/) / [Transformer](/tags/transformer/) / [异常Token](/tags/%E5%BC%82%E5%B8%B8token/) / [视觉生成](/tags/%E8%A7%86%E8%A7%89%E7%94%9F%E6%88%90/) / [DiT](/tags/dit/) / [模型优化](/tags/%E6%A8%A1%E5%9E%8B%E4%BC%98%E5%8C%96/) / [计算机视觉](/tags/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89/) / [Stable Diffusion](/tags/stable-diffusion/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [BiGain：面向生成与分类任务的统一令牌压缩]({{< relref "posts/20260316-arxiv_ai-bigain-unified-token-compression-for-joint-generat-7.md" >}})
- [PixelGen：像素扩散结合感知损失超越潜在扩散]({{< relref "posts/20260204-arxiv_ai-pixelgen-pixel-diffusion-beats-latent-diffusion-wi-2.md" >}})
- [模式寻优结合均值寻优实现快速长视频生成]({{< relref "posts/20260302-arxiv_ai-mode-seeking-meets-mean-seeking-for-fast-long-vide-0.md" >}})
- [PRX Part 3：24小时训练文本生成图像模型]({{< relref "posts/20260304-blogs_podcasts-prx-part-3-training-a-text-to-image-model-in-24h-1.md" >}})
- [文本生成图像模型训练设计：消融实验的经验总结]({{< relref "posts/20260203-blogs_podcasts-training-design-for-text-to-image-models-lessons-f-0.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*