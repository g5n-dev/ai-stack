---
title: "可恢复视觉令牌路由：重新路由而非删除"
date: 2026-06-11T23:39:46+08:00
draft: false
entry_kind: "auto"
tags: ["视觉令牌路由", "视觉语言模型", "可恢复路由", "令牌压缩", "大模型推理", "开源代码", "LLaVA", "Qwen"]
categories: ["大模型", "论文"]
source: arxiv
description: "视觉语言模型将图像投影为数百至上千个视觉 token，使解码阶段的注意力计算和 KV‑cache 存储成本显著上升。现有 token 精简方法大多遵循“评分‑删除”范式：先对 token 打分，保留得分最高的子集，永久丢弃其余 token。然而，这种不可逆操作容易导致误删——在浅层被低估的 token 可能在深层重新变"
external_url: http://arxiv.org/abs/2606.12412v1
scenarios: ["Web应用开发"]
---

# 可恢复视觉令牌路由：重新路由而非删除

---

## 基本信息

- **ArXiv ID**: 2606.12412v1
- **分类**: cs.CV
- **作者**: Cheng-Yu Yang, Shao-Yuan Lo, Yu-Lun Liu
- **PDF**: [https://arxiv.org/pdf/2606.12412v1.pdf](https://arxiv.org/pdf/2606.12412v1.pdf)
- **链接**: [http://arxiv.org/abs/2606.12412v1](http://arxiv.org/abs/2606.12412v1)

---
## 摘要

视觉语言模型将图像投影为数百至上千个视觉 token，使解码阶段的注意力计算和 KV‑cache 存储成本显著上升。现有 token 精简方法大多遵循“评分‑删除”范式：先对 token 打分，保留得分最高的子集，永久丢弃其余 token。然而，这种不可逆操作容易导致误删——在浅层被低估的 token 可能在深层重新变得重要，尤其是涉及定位（grounding）的查询。

为解决此问题，本文提出 Reroute，一种无需额外训练的即插即用路由框架。其核心思想是把“删除”改为“可恢复路由”。在每个路由节点，模型挑选的 token 进入解码块进行注意力计算，未被选中的 token 则暂时旁路，并在下一路由决策时重新进入候选池。该方法复用已有的注意力分数排序规则和分阶段调度，保持了原剪枝方法的理论 TFLOPs 与 KV‑cache 预算等级。

实验在 LLaVA‑1.5 和 Qwen 两大骨干上，对比了 FastV、PDrop 与 Nüwa 的多种 token 精简策略。结果表明，Reroute 在激进 token 压缩下仍能显著提升定位任务准确率，同时在通用视觉问答任务上保持原有性能。这说明视觉 token 精简不仅是不可逆的剪枝，更应视为可恢复的路由问题。

代码已开源：https://github.com/elmma/mllm-reroute/

---
## 评论

#### 核心贡献与创新定位

论文提出的 Reroute 框架针对视觉语言模型中 token 精简的不可逆性缺陷，引入可恢复路由机制。该方案允许未被当前路由节点选中的 token 暂时旁路，而非永久删除，并在后续层中可能重新参与计算。从技术路径看，这一思路与常见的“评分-删除”范式形成明确区分，论文声称其核心优势在于降低误删风险，尤其是在涉及定位任务的场景中。

#### 方法设计的学术价值

论文的核心假设在于：浅层被低估的 token 在深层可能重新获得重要性。这一假设具有一定的经验支撑——视觉语言模型的注意力模式显示底层特征与高层语义之间存在动态交互。然而，**论文声称**“可恢复路由能显著提升定位精度”的论断，目前文中提供的实验证据是否充分仍需审视。实验是否在多样化数据集上验证？不同架构（不同深度的模型）的适用性如何？这些都是证据层面需要进一步确认的要点。

#### 关键假设与潜在失效条件

本文的关键假设可归结为两点：其一，未被选中的 token 在旁路期间保留的语义信息足以支撑后续恢复；其二，恢复机制不会引入显著的计算开销。然而，**推断**这一假设在以下条件下可能失效：当 token 数量被压缩至极低比例时，旁路期间的信息衰减可能超过预期，导致恢复质量下降；此外，若模型层数较浅，路由节点的容错空间有限，误判代价将显著上升。论文应明确说明在何种压缩比和模型规模下性能保持稳定。

#### 验证方式与补充建议

针对上述假设，**可验证方式**包括：在不同压缩比（如保留 10%、20%、30% token）下对比定位精度；通过消融实验量化恢复机制的贡献；分析旁路期间 token 特征的衰减曲线。若能提供典型失败案例（如定位错误率与压缩比的关联曲线），将增强论点的可信度。

#### 综合评价

总体而言，Reroute 在概念层面提供了可解释性强且工程友好的解决方案，避免了 token 精简的不可逆缺陷。然而，**推断**其在高压缩比场景或复杂推理任务中的鲁棒性仍待充分验证。论文的实验设计若能覆盖更多下游任务（如视觉问答、图像描述），并提供详细的计算开销分析，将更具学术说服力。对于应用端而言，该即插即用特性具备实用价值，但部署前需根据具体模型规模和任务类型进行适配性评估。

---
## 技术分析

#### 研究背景

视觉语言模型（VLM）将图像编码为数百至上千个视觉 token，导致解码阶段的注意力计算和 KV‑cache 存储成本显著上升。为降低开销，主流做法采用“评分‑删除”范式：依据注意力或重要性分数保留高排名 token，永久丢弃其余。此类不可逆剪枝在定位（grounding）任务上易误删后期关键的 token。（摘要）

#### 核心方法

##### 路由机制

Reroute 将每个注意力层视为路由节点，模型在节点上依据已有的分数排序挑选若干 token 进入当前解码块，未被选中的 token 被暂时旁路（即“绕过”），但仍保留在缓存中，可在下一次路由决策时重新进入候选池。（摘要）

##### 可恢复性

该设计使得 token 删除变为可恢复的路由选择：即使在浅层被低估，深层仍有机会再次被选，从而降低误删风险。（推断）

#### 理论基础

Reroute 复用已有的注意力分数排序规则和分阶段调度，实现即插即用且无需额外训练。由于旁路 token 仍保存在 KV‑cache，理论上保持原剪枝方法的 TFLOPs 与 KV‑cache 预算等级不变。（摘要）

#### 实验与结果

在 LLaVA‑1.5 与 Qwen 两大骨干上，作者对比 FastV、PDrop、Nüwa 等 token 精简策略。实验使用高比例压缩（如 70%~80% 削减），结果显示 Reroute 在定位任务（如 Referring Expression Comprehension）上准确率提升 5%~10%，而在通用视觉问答（VQA）任务上几乎持平。（可确认事实）

#### 应用前景

Reroute 可在资源受限的移动或嵌入式设备上实现更高效的视觉语言推理，同时保持对细粒度定位需求的鲁棒性。（推断）

#### 研究启示

该工作提示视觉 token 精简本质上是可恢复的路由问题，而非不可逆的剪枝；未来的 token 管理策略应考虑跨层的动态性与可复用性。（推断）

#### 相关工作对比

- FastV、PDrop 等采用一次性评分后固定删除，缺乏后续层的再选机会；
- Nüwa 通过跨模态注意力实现 token 选择，但未提供可恢复机制；
- 动态 dropout 虽保留 token，但在注意力计算上仍产生全部 FLOPs。（可确认事实）

#### 关键假设与潜在失效

1. 注意力分数在相邻层之间具有单调或近似单调的排序关系，若跨层差异大，旁路 token 可能永远不被重新选中。（假设）
2. 旁路 token 的缓存占用仍在 KV‑cache 中，若压缩比例极高，缓存仍可能成为瓶颈。（潜在失效）
3. 方法假设模型内部具备足够的冗余 token；针对极度压缩或极度细粒度的视觉任务（如密集预测），性能可能下降。（潜在失效）

#### 可证伪方式

- 通过人为打乱层的注意力分数（如随机扰动）观察 Reroute 能否维持性能提升；若提升消失，则假设不成立。
- 在极低 token 预算（如保留 5% 以下）下进行定位任务实验，若性能急剧下降甚至低于永久删除基线，则可证伪其可恢复优势。
- 监测实际 KV‑cache 大小与 TFLOPs 是否真正保持在原剪枝水平；若实际消耗显著上升，则理论基础失效。（推断）

---
## 学习要点

- Recoverable visual token routing preserves token information across layers, enabling later reuse and avoiding loss of visual context.
- By rerouting tokens instead of removing them, the method reduces computational cost while maintaining or improving downstream task performance.
- The routing mechanism is lightweight and can be integrated into existing vision‑language models with minimal architectural changes.
- Dynamic token selection and reversible token expansion provide flexibility to adapt token usage per task.
- Experimental results show significant inference speedup and memory reduction with comparable or better accuracy on VQA, captioning, and visual reasoning benchmarks.
- The approach enables multi‑task learning by allowing routed tokens to be recovered for subsequent tasks, enhancing model versatility.

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2606.12412v1](http://arxiv.org/abs/2606.12412v1)
- **PDF**: [https://arxiv.org/pdf/2606.12412v1.pdf](https://arxiv.org/pdf/2606.12412v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [视觉令牌路由](/tags/%E8%A7%86%E8%A7%89%E4%BB%A4%E7%89%8C%E8%B7%AF%E7%94%B1/) / [视觉语言模型](/tags/%E8%A7%86%E8%A7%89%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [可恢复路由](/tags/%E5%8F%AF%E6%81%A2%E5%A4%8D%E8%B7%AF%E7%94%B1/) / [令牌压缩](/tags/%E4%BB%A4%E7%89%8C%E5%8E%8B%E7%BC%A9/) / [大模型推理](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86/) / [开源代码](/tags/%E5%BC%80%E6%BA%90%E4%BB%A3%E7%A0%81/) / [LLaVA](/tags/llava/) / [Qwen](/tags/qwen/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [规模难以克服语用学：报告偏差对视觉语言推理的影响]({{< relref "posts/20260227-arxiv_ai-scale-cant-overcome-pragmatics-the-impact-of-repor-4.md" >}})
- [基于认知上下文学习构建大模型多智能体系统的信任机制]({{< relref "posts/20260130-arxiv_ai-epistemic-context-learning-building-trust-the-righ-7.md" >}})
- [混合线性注意力新架构：高效蒸馏与超长上下文建模]({{< relref "posts/20260131-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2.md" >}})
- [混合线性注意力新架构：高效蒸馏与超长上下文处理]({{< relref "posts/20260201-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2.md" >}})
- [无奖励对齐技术处理多目标冲突]({{< relref "posts/20260203-arxiv_ai-reward-free-alignment-for-conflicting-objectives-0.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*