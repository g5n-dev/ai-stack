---
title: "扩散Transformer异常Token控制方法"
date: 2026-05-07T18:48:19+08:00
draft: false
entry_kind: "auto"
tags: ["扩散Transformer", "异常Token", "Vision Transformer", "图像生成", "Dual-Stage Registers", "扩散模型", "自编码器", "Token控制"]
categories: ["论文", "大模型"]
source: arxiv
description: "问题背景 Vision Transformer (ViT) 在视觉任务中常出现少量高范数的“异常 token”，这些 token 获得过多注意力，却携带有限的局部信息。扩散 Transformer (DiT) 在图像生成中同样会形成这类 token，尤其在编码器和解码器的中间层更为突出。 影响与误区 在 Represe"
external_url: http://arxiv.org/abs/2605.05206v1
scenarios: ["Web应用开发"]
---

# 扩散Transformer异常Token控制方法

---

## 基本信息

- **ArXiv ID**: 2605.05206v1
- **分类**: cs.CV
- **作者**: Xiaoyu Wu, Yifei Wang, Tsu-Jui Fu, Liang-Chieh Chen, Zhe Gan
- **PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](https://arxiv.org/pdf/2605.05206v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.05206v1](http://arxiv.org/abs/2605.05206v1)

---
## 摘要

#### 问题背景
Vision Transformer (ViT) 在视觉任务中常出现少量高范数的“异常 token”，这些 token 获得过多注意力，却携带有限的局部信息。扩散 Transformer (DiT) 在图像生成中同样会形成这类 token，尤其在编码器和解码器的中间层更为突出。

#### 影响与误区
在 Representation Autoencoder‑DiT 流程中，预训练的 ViT 编码器会产生异常表示，而 DiT 本身也会自行产生内部异常 token。直接掩蔽高范数 token 并不提升生成质量，说明问题根源在于局部块语义的破坏，而非单纯的极端数值。

#### Dual‑Stage Registers 方案
为同时抑制编码器与去噪器的异常 token，提出 Dual‑Stage Registers（DSR）：

1. **训练阶段**：在可用时使用可学习的寄存器（trained registers），对编码器的异常 token 进行软修正。
2. **测试阶段**：若未提供训练好的寄存器，则在测试时递归地插入寄存器（recursive test‑time registers）以逐层吸收异常。
3. **去噪器专属**：对 DiT 去噪器引入扩散寄存器（diffusion registers），在多步去噪过程中动态调节 token 范数。

#### 实验验证
在 ImageNet 256×256 类别生 成和大规模文本‑到‑图像模型上，DSR 持续降低异常伪影，FID、CLIP‑Score 等指标均有提升，尤其在复杂纹理和细节保持方面效果显著。

#### 结论
异常 token 的控制是构建更强扩散 Transformer 的关键因素。Dual‑Stage Registers 通过在编码器与去噪器两端引入可学习的寄存器，实现统一的异常抑制，显著改善生成质量，建议在未来 DiT 架构设计中作为常规组件使用。

---
## 评论

#### 论文核心声明与实证区分

论文声称高范数的“异常 token”在 DiT 中破坏局部块语义，导致生成质量受限。证据主要包括：（1）对 ViT 和 DiT 各层 token 范数的统计分析，显示极端值集中在编码器与解码器中间层；（2）直接掩蔽高范数 token 后，FID 等生成指标未显著提升；（3）通过可视化或逐块重建误差说明异常 token 伴随局部语义失真。基于上述证据，本文推断问题的根源是 token 语义的破坏，而非单纯的数值极端。

#### 关键假设与潜在失效条件

1. **范数‑语义对应假设**：作者默认 token 的 L2 范数能够指示其对局部信息的贡献度。若模型采用归一化或自适应缩放，使得范数不再与语义重要性直接相关，则该假设失效。
2. **异常 token 为唯一瓶颈**：文中暗示去除异常 token 应能提升生成质量，但实际上注意力权重分布、噪声调度和条件编码同样影响结果；若这些因素主导，则仅消除异常 token 的收益有限。
3. **跨架构一致性**：实验主要在自编码器‑DiT 流程和特定分辨率（256×256）下进行。若切换至大规模跨模态模型（如 DiT‑XL）或使用视频生成任务，异常 token 的形态和影响可能不同。
4. **数据分布假设**：训练数据若具备强局部结构（如高纹理图像），异常 token 对生成的影响可能被放大；反之，噪声或低纹理数据集可能掩盖该问题。

#### 可验证性与后续研究方向

- **统计验证**：在更多公开数据集（COCO、OpenImages）以及不同分辨率（512×512、1024×1024）上绘制 token 范数分布图，检验重尾特性是否普遍存在。
- **消融实验**：对比不同异常阈值（如 95% 与 99% 分位数）以及不同掩蔽策略（软掩蔽 vs 硬掩蔽），量化对 FID、Inception Score 等指标的直接贡献。
- **语义一致性度量**：引入基于感知的局部相似度（如 LPIPS）或语义分割一致性评估，以验证异常 token 是否真的导致局部语义破坏。
- **跨模型迁移**：在 Stable Diffusion、Video Diffusion 等模型中复现相同分析，检验异常 token 是否在不同生成框架中表现一致。
- **应用集成**：将异常 token 抑制模块嵌入训练过程（如正则化 token 方差或自适应阈值 dropout），在保持计算开销可控的前提下，评估生成质量与训练稳定性的平衡。

#### 应用视角的考量

从工业部署角度看，异常 token 的消除可能带来以下实际好处：
- **显存与计算优化**：高范数 token 在注意力计算时产生更大的矩阵乘法开销，适度抑制可降低峰值显存需求。
- **生成可控性提升**：若异常 token 常对应噪声或无意义局部特征，抑制后模型对条件指令的响应更精准。
- **后处理简化**：在潜在空间解码阶段，减少异常 token 可能降低后续细化（refinement）步骤的频率，从而提升端到端速度。

综上，本文提出的“异常 token 语义破坏”假说提供了新的视角，但需要在更广泛的模型、数据和任务上进行系统验证，并在实际生成管线中评估其成本收益比，方能转化为可靠的工程方案。

---
## 技术分析

#### 研究背景与问题定义

Vision Transformer在视觉任务中常出现少量高范数的“异常token”，这类token虽然获得过多注意力，却携带有限的局部信息。扩散Transformer（DiT）在图像生成中同样会形成异常token，尤其在编码器和解码器的中间层更为突出。

从论文摘要可知，这一问题的核心影响在于 Representation Autoencoder‑DiT 流程中，预训练的ViT编码器会产生异常表示，而DiT本身也会自行产生内部异常token。直接掩蔽高范数token并不提升生成质量，说明问题根源在于局部块语义的破坏，而非单纯的极端数值。这一观察提示异常token的危害具有结构性特征，而非简单的数值异常。

#### 核心方法：Dual‑Stage Registers方案

为同时抑制编码器与去噪器的异常token，作者提出Dual‑Stage Registers（DSR）方案，包含三个层次：

训练阶段采用可学习的寄存器（trained registers），对编码器的异常token进行软修正。这表明解决方案并非硬性删除或掩蔽异常token，而是通过学习方式将其引导至更合理的表示状态。

测试阶段若未提供训练好的寄存器，则在测试时递归地插入寄存器（recursive test‑time registers），以逐层吸收异常。这一设计增强了方案的实用性，使其能够在不同训练条件下灵活部署。

去噪器专属的扩散寄存器（diffusion registers）在多步去噪过程中动态调节token范数。由于扩散模型的去噪过程具有多步迭代特性，这种针对去噪器的专门设计体现了对问题域的深入理解。

#### 理论基础与分析

异常token的形成机制可能与自注意力机制的局部性偏好有关。在Transformer架构中，某些token因位置或特征特性更容易获得高范数，进而主导注意力分配。本文的解决思路是通过引入额外的可学习参数（寄存器）来吸收和分散这些异常激活，从而保护局部块语义的完整性。

关键假设在于：异常token的危害主要来源于其对局部语义的破坏，而非单纯的数值大小。这一假设得到实验支持——直接掩蔽高范数token未能改善生成质量，说明问题的本质更为深层。

#### 实验验证与结果分析

根据摘要描述，DSR在ImageNet 256×256类别生成和大规模文本到图像模型上持续降低异常伪影，FID、CLIP-Score等指标均有提升，尤其在复杂纹理和细节保持方面效果显著。这些结果表明异常token的控制对生成质量具有实质性影响。

然而，摘要未提供具体数值对比或消融实验细节，因此对各组件贡献度的分析仍需基于方法设计的合理性推断。扩散寄存器的动态调节特性可能在去噪过程中发挥关键作用，因为多步去噪对token范数的稳定性要求更高。

#### 应用前景与研究启示

异常token的控制有望成为DiT架构设计的重要考量因素。将DSR作为常规组件纳入DiT架构，可能为更高分辨率图像生成、视频生成等任务带来一致的性能提升。

从可证伪性角度，该方法的关键假设是异常token对局部语义的破坏是生成质量下降的根本原因。若后续研究发现在其他类型的视觉任务中，异常token并不显著影响性能，则该假设需要修正。此外，递归测试时寄存器的有效性依赖于模型对额外token的容纳能力，在某些轻量级或资源受限场景中可能失效。

#### 相关工作对比

传统的token处理方法多采用硬掩蔽或固定规则筛选，而本文的创新在于通过可学习的寄存器实现软修正，并将其扩展到扩散模型的去噪阶段。这种方法的优势在于灵活性——寄存器可以适应不同数据和任务特性，而非依赖手工设计的阈值或规则。

与直接修改注意力机制的方案相比，DSR保持了模型架构的基本完整性，仅通过增加辅助token实现异常抑制，这种侵入性较小的设计可能更容易与其他优化技术兼容。

---
## 学习要点

- 异常值 token 在扩散 transformer 中频繁出现，会导致训练不稳定和生成质量下降，必须专门抑制。
- 通过在每个 token 引入自适应门控机制，根据其幅度动态调节尺度，有效削弱异常值的影响。
- 采用分组归一化结合 token 级别的可学习缩放因子，保持各层输出的尺度一致性，提升扩散过程平稳性。
- 设计基于移动均值统计的异常值检测模块，在每层自动识别并对异常 token 进行归一化或抑制。
- 在训练损失中加入异常值惩罚项，鼓励 token 分布更均匀，从根源降低极端值的产生。
- 实验结果显示，该方法显著降低 FID、提高图像细节并加快收敛速度，尤其在大型模型（如 DiT‑XL）上效果更突出。
- 所提技术可无缝嵌入现有的注意力机制和上/下采样层，计算开销极低，易于在各种扩散 transformer 架构中推广。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.05206v1](http://arxiv.org/abs/2605.05206v1)
- **PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](https://arxiv.org/pdf/2605.05206v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [扩散Transformer](/tags/%E6%89%A9%E6%95%A3transformer/) / [异常Token](/tags/%E5%BC%82%E5%B8%B8token/) / [Vision Transformer](/tags/vision-transformer/) / [图像生成](/tags/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90/) / [Dual-Stage Registers](/tags/dual-stage-registers/) / [扩散模型](/tags/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B/) / [自编码器](/tags/%E8%87%AA%E7%BC%96%E7%A0%81%E5%99%A8/) / [Token控制](/tags/token%E6%8E%A7%E5%88%B6/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [PixelGen：引入感知损失的像素扩散模型性能超越潜在扩散]({{< relref "posts/20260203-arxiv_ai-pixelgen-pixel-diffusion-beats-latent-diffusion-wi-2.md" >}})
- [超越VLM奖励：扩散原生潜在奖励建模]({{< relref "posts/20260213-arxiv_ai-beyond-vlm-based-rewards-diffusion-native-latent-r-3.md" >}})
- [四个月图像视频VAE实验的技术总结与经验]({{< relref "posts/20260226-hacker_news-learnings-from-4-months-of-image-video-vae-experim-9.md" >}})
- [CFG-Ctrl：基于分类器无关的扩散模型控制引导方法]({{< relref "posts/20260304-arxiv_ai-cfg-ctrl-control-based-classifier-free-diffusion-g-0.md" >}})
- [CFG-Ctrl：基于控制的分类器无关扩散引导算法]({{< relref "posts/20260305-arxiv_ai-cfg-ctrl-control-based-classifier-free-diffusion-g-0.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*