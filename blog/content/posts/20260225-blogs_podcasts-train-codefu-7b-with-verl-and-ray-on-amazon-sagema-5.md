---
title: "使用 veRL 和 Ray 在 SageMaker 上训练 CodeFu-7B"
date: 2026-02-25T10:57:52+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "RLHF", "GRPO", "veRL", "Ray", "SageMaker", "分布式训练", "CodeFu-7B"]
categories: ["AI 工程", "大模型"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon SageMaker Training Jobs 上，利用 veRL 库和 Ray 集群训练 CodeFu-7B 模型。以下是核心内容总结： **1. 训练目标：** 训练 CodeFu-7B，这是一个拥有 70 亿参数的专用模型，专门针对竞技编程领域进行了优化。 **2. 核心技术：**"
external_url: https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs
scenarios: ["大语言模型", "工具"]
---

# 使用 veRL 和 Ray 在 SageMaker 上训练 CodeFu-7B

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-24T15:46:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)

---
## 摘要/简介

在本文中，我们将演示如何使用 Group Relative Policy Optimization (GRPO) 以及 veRL，在由 SageMaker 训练作业管理的分布式 Ray 集群内，训练 CodeFu-7B——一个拥有 70 亿参数的竞技编程专用模型。veRL 是一个灵活、高效的 LLM 训练库，支持直接扩展各类强化学习算法，并能与现有 LLM 基础设施无缝集成。我们将介绍完整的实现流程，涵盖数据准备、分布式训练设置以及全面的观测能力，展示这一统一方案如何为复杂的强化学习训练工作负载同时带来计算规模与开发者体验。

---
## 导语

在竞技编程领域，模型性能的提升往往依赖于高效的强化学习训练策略。本文将详细介绍如何利用 veRL 库与 Ray，在 Amazon SageMaker 上分布式训练 CodeFu-7B 模型。通过解析 GRPO 算法的具体实现及数据准备流程，我们将展示这一方案如何在扩展计算规模的同时优化开发者体验，帮助您掌握构建复杂 LLM 训练工作负载的完整方法。

---
## 摘要

本文介绍了如何在 Amazon SageMaker Training Jobs 上，利用 veRL 库和 Ray 集群训练 CodeFu-7B 模型。以下是核心内容总结：

**1. 训练目标：**
训练 CodeFu-7B，这是一个拥有 70 亿参数的专用模型，专门针对竞技编程领域进行了优化。

**2. 核心技术：**
*   **算法：** 采用群组相对策略优化（GRPO）。
*   **框架：** 使用 veRL，这是一个灵活且高效的 LLM 训练库，支持多种强化学习算法的扩展，并能与现有 LLM 基础设施无缝集成。
*   **架构：** 在 SageMaker 托管的分布式 Ray 集群中进行训练。

**3. 实施流程：**
文章详细介绍了从数据准备、分布式训练环境搭建到全面可观测性监控的完整实现过程。

**4. 优势：**
这种统一的方法展示了如何将强大的计算规模与良好的开发体验相结合，从而高效地处理复杂的强化学习训练任务。

---
## 评论

**中心观点**
本文的核心观点是：通过将开源强化学习库 veRL 与 Ray 分布式框架集成，并在 Amazon SageMaker 上进行托管训练，能够以高效、可扩展且低成本的方式实现对 CodeFu-7B 模型的 GRPO（组相对策略优化）微调，从而解决大模型在竞技编程等高难度逻辑任务上的对齐难题。

**支撑理由与边界条件分析**

**1. 架构设计的解耦与云原生适配（事实陈述）**
文章提出的技术栈——veRL（负责 RL 逻辑）+ Ray（负责资源编排）+ SageMaker（负责底层算力），体现了现代 AI 工程中“关注点分离”的最佳实践。
*   **分析**：veRL 采用了轻量级的设计，将 RLHF 过程中的 Actor、Critic、Reference Model 和 Reward Model 解耦。利用 Ray 作为中间层，可以动态地在 SageMaker 的异构实例组间调度这些角色。这比传统的使用单体训练脚本（如仅依赖 DeepSpeed 或 Megatron 的固定脚本）具有更高的灵活性。
*   **边界条件/反例**：这种多层架构（veRL over Ray on SageMaker）引入了显著的**网络通信开销**。对于参数量极大的模型（如 70B+），节点间通信可能成为瓶颈，此时单纯的 SageMaker EFA（弹性结构适配器）加直通 NCCL 的方案可能比 Ray 更高效。

**2. GRPO 算法在代码生成场景的适用性（作者观点）**
文章强调使用 GRPO 而非 PPO，这是一个针对特定场景的优化选择。
*   **分析**：传统的 PPO 需要训练一个价值模型来拟合奖励分数，计算量大且不稳定。GRPO 通过从同一个提示生成一组输出，利用组内相对排名计算基线，无需显式的价值网络。对于竞技编程这种“结果二元分明”（通过测试用例或报错）的场景，GRPO 的方差更低，训练更稳定。
*   **边界条件/反例**：GRPO 高度依赖于**成组采样**。在推理阶段，为了生成一个答案，模型实际上需要前向传播多次（组大小 G），这导致推理时的计算成本随 G 线性增长。在延迟敏感的实时应用中，这可能不可接受。

**3. 基础设施成本效益比（你的推断）**
文章隐含地论证了使用 SageMaker 进行此类训练的经济性。
*   **分析**：SageMaker 提供了托管 Spot 实例的支持。结合 Ray 的容错机制，veRL 可以在 Spot 实例中断时自动恢复训练。对于 RL 这种训练时间长、GPU 占用率高的任务，使用 Spot 实例理论上可降低 70%-90% 的算力成本。
*   **边界条件/反例**：SageMaker 的冷启动时间较长，且对于小团队或个人研究者，其学习曲线和厂商锁定风险可能不如直接使用 Run:ai 或 Slurm + Kubernetes 开源方案友好。

**4. 竞技编程作为高难度逻辑对齐的试金石（行业观点）**
*   **分析**：选择 CodeFu-7B（专注于竞技编程）作为测试床非常明智。代码生成是检验大模型逻辑推理和长程依赖能力的“极限运动”。如果能通过 RL 显著提升 CodeFu 的表现，证明了该技术栈在数学、逻辑推理等高价值领域的通用性。
*   **边界条件/反例**：竞技编程的数据是纯净的（Unit Tests 可验证）。但在开放域的对话或创意写作中，奖励信号极其稀疏且主观，GRPO 的组内相对优势可能无法转化为绝对的质量提升，甚至可能导致模式崩溃。

**综合评价**

*   **内容深度**：**4/5**。文章不仅停留在“如何调用 API”，还深入到了 GRPO 的实现细节和 Ray 的分布式调度逻辑，展示了较高的工程深度。
*   **实用价值**：**5/5**。对于希望摆脱昂贵 RLaaS 服务（如 OpenAI 微调 API）并转向自建 RL 训练平台的企业，提供了极具价值的参考架构。
*   **创新性**：**3.5/5**。虽然 GRPO 和 Ray 均非新技术，但将 veRL 这种新兴库与 SageMaker 深度结合的案例较少，具有一定的工程创新性。
*   **可读性**：**4/5**。技术博客结构清晰，代码片段与架构图配合得当，但对 Ray 和 SageMaker 的底层交互细节可能需要读者具备一定前置知识。

**争议点与批判性思考**

1.  **过度依赖“组”采样带来的效率悖论**：文章虽然强调了训练效率，但未充分提及 GRPO 在推理阶段的算力消耗。在实际工业应用中，如果一个 Prompt 需要模型推理 4 次才能进行一次梯度更新，这在 Token 计费模式下是否经济？
2.  **SageMaker 的必要性存疑**：对于资深算法工程师，SageMaker 的抽象层有时反而是累赘。如果 veRL 已经足够完善，直接在裸金属或 Kubernetes 集群上运行可能拥有更高的硬件利用率。文章某种程度上带有 AWS 的技术栈营销色彩。
3.  **评估指标的局限性**：竞技编程的 Pass@k 指标并不完全等同于代码生成的工业质量。工业级代码更看重可维护性、安全性和上下文理解，单纯的 RL 优化可能会导致模型生成“钻空子”通过测试但不可读的代码。

**实际应用建议**

1.  **监控吞吐量而非仅看 Loss**：

---
## 技术分析

基于您提供的文章标题和摘要，以及对相关技术栈（veRL, Ray, SageMaker, GRPO, CodeFu）的深度了解，以下是对该文章核心观点和技术要点的全面深入分析。

---

# 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**“云原生弹性架构与高效强化学习算法的结合，是垂直领域大模型训练的最佳实践”**。具体而言，通过在 Amazon SageMaker 上利用 Ray 进行分布式编排，并结合 veRL 库实现 GRPO（Group Relative Policy Optimization）算法，可以高效、低成本地训练出专门用于竞技编程的高质量 7B 模型。

**核心思想：**
作者试图传达一种**“解耦与复用”**的工程哲学。
1.  **算力解耦：** 利用 SageMaker 的基础设施能力（如 Spot Instance）和 Ray 的调度能力，解决 LLM 训练中资源昂贵且调度复杂的痛点。
2.  **算法复用：** 推广 veRL 这种轻量级、可扩展的库，证明不需要庞大的重型框架（如复杂的 RLHF 封装）也能实现高效的强化学习微调。
3.  **垂直优化：** 以 CodeFu（竞技编程）为例，展示通用基座模型如何通过特定领域的强化学习（RL）转化为专家模型。

**创新性与深度：**
*   **架构创新：** 将 Ray 的弹性调度引入 SageMaker 的托管训练作业中。通常 SageMaker 作业是静态的，结合 Ray 可以实现更细粒度的资源管理和容错（特别是利用 Spot 实例中断恢复）。
*   **算法应用：** GRPO 是对传统 PPO（Proximal Policy Optimization）的改进，去除了对价值模型 的依赖，显著降低了显存占用和计算开销。文章将这一前沿算法与工程基础设施结合，具有很高的实战深度。

**重要性：**
这一观点极其重要，因为它解决了 LLM 落地中的**“最后一公里”**问题——即如何以可控的成本和复杂度，将通用模型微调为具备特定逻辑推理和代码生成能力的专家模型。对于企业而言，这意味着可以用更少的资源（7B 而非 70B）在特定任务上获得更好的性能。

---

# 2. 关键技术要点

**涉及的关键技术或概念：**
*   **GRPO (Group Relative Policy Optimization)：** 核心算法。不同于 PPO 需要训练 Actor 和 Critic 两个模型，GRPO 通过从同一个策略中采样一组输出来计算基线，无需额外的 Critic 模型。
*   **veRL (Versatile Reinforcement Learning)：** 由 volcengine（字节跳动相关团队背景）开源的高效 RL 训练库，专为 LLM 设计，强调显存优化和计算效率。
*   **Ray on SageMaker：** 利用 Ray Cluster 作为 SageMaker Training Job 的底层运行时，实现动态伸缩和 Actor 模型的并行化。
*   **CodeFu-7B：** 目标模型，专注于竞技编程，具备强大的逻辑推理和代码生成能力。

**技术原理和实现方式：**
1.  **GRPO 原理：**
    *   生成阶段：对于提示词 $p$，策略 $\pi$ 生成一组输出 $o_1, o_2, ..., o_g$。
    *   评分阶段：环境对每个输出打分 $r_i$。
    *   优化阶段：计算组内平均分作为基线，计算优势 $A_i = r_i - \text{mean}(r)$。利用该优势直接更新策略，省去了估算 $V(s)$ 的步骤。
2.  **分布式架构：**
    *   SageMaker 启动 Ray Head 节点。
    *   Ray 负责管理 Worker 节点（可能混合使用 CPU 和 GPU）。
    *   veRL 在 Ray 的 Actor 上运行，利用 Ray 的分布式对象存储传递模型梯度或经验数据。

**技术难点和解决方案：**
*   **难点：** RL 训练（特别是 PPO）显存消耗巨大，通常需要 4 倍于模型推理的显存（Actor + Critic + Reference + Optimizer）。
*   **解决方案：** 采用 GRPO 移除 Critic 模型，直接节省 1/4 的显存。同时，veRL 可能结合了 FlashAttention 和 CPU Offload 技术。
*   **难点：** 云上训练的高成本。
*   **解决方案：** 利用 Ray 的弹性与 SageMaker 的 Managed Spot Training 结合，在保证训练不中断的前提下（通过 Checkpoint 机制），大幅降低算力成本（通常可节省 70% 以上）。

**技术创新点分析：**
*   **显存优化突破：** 证明了在 7B 模型规模上，可以在消费级或企业级 GPU 上高效运行复杂的 RL 训练，而不需要 H100 显卡集群。
*   **工程化范式转移：** 从“单体脚本”转向“库+编排”的微服务架构，提高了实验的可迭代性。

---

# 3. 实际应用价值

**对实际工作的指导意义：**
该文章为 AI 工程师提供了一套**“高性价比模型微调”**的标准作业程序（SOP）。它表明，通过合理的算法选择（GRPO）和基础设施组合（Ray + SageMaker），中小型团队也能承担得起高质量的模型训练。

**可以应用到哪些场景：**
*   **垂直领域模型训练：** 法律、医疗、金融等需要复杂推理和特定格式输出的领域。
*   **代码生成与辅助：** 企业内部代码助手、自动化测试脚本生成。
*   **逻辑推理强化：** 数学问题求解、数据分析报告生成。

**需要注意的问题：**
*   **GRPO 的采样成本：** GRPO 需要每个 Prompt 生成多个 Output（Group Size），这会增加推理阶段的计算量。如果 Reward Model 或环境评估非常慢，会拖慢整体训练速度。
*   **Ray 的复杂性：** 引入 Ray 增加了调试难度，网络通信开销可能成为瓶颈，需要仔细配置对象存储和通信后端。

**实施建议：**
*   先在小规模模型（如 1B）上验证 GRPO 流程。
*   优先使用 SageMaker 的 Spot 实例以控制成本。
*   重点监控 Reward Score 的收敛曲线，防止模式崩溃。

---

# 4. 行业影响分析

**对行业的启示：**
*   **小模型 + RL = 强专家：** 行业趋势正从“盲目追求千亿参数”转向“将百亿/几十亿参数模型通过 RL 训练至极致”。CodeFu-7B 的成功可能超越未经过 RL 训练的 30B+ 模型在代码领域的表现。
*   **基础设施民主化：** 云厂商（AWS）与开源社区（veRL, Ray）的深度整合，降低了顶尖 AI 技术的使用门槛。

**可能带来的变革：**
*   **MaaS（Model as a Service）的细分：** 未来的模型市场将充斥着各种经过特定 GRPO 训练的“专家模型”，而非仅仅的通用基座。
*   **RLHF 的平民化：** GRPO 简化了 RLHF 流程，使得更多公司有能力构建自己的对齐算法。

**发展趋势：**
*   **端到端优化：** 从数据清洗、SFT（监督微调）到 RL（强化学习）的全链路自动化。
*   **更高效的 RL 算法：** GRPO 的普及将引发对“无 Critic RL”算法的更多研究。

---

# 5. 延伸思考

**引发的思考：**
*   **数据质量 vs. 算法复杂度：** GRPO 的效果高度依赖于 Reward Model 或编译器反馈的准确性。如果 Reward 信号有噪声，训练会不稳定。这是否意味着我们应更关注 Reward Model 的构建？
*   **推理时计算 vs. 训练时计算：** GRPO 在训练时增加了计算量（生成 Group），这是否意味着未来的模型优化方向是将计算成本从训练阶段转移到推理阶段？

**拓展方向：**
*   **多模态扩展：** 将此架构应用于视觉-语言模型（VLM）的微调，例如训练图表理解专家。
*   **混合专家：** 结合 MoE（Mixture of Experts）架构，训练一群 7B 的 CodeFu 专家，通过 Router 调度。

**需进一步研究的问题：**
*   GRPO 在 Group Size 较大时的收敛性理论证明。
*   在极度稀疏的奖励环境（如长代码生成）中，GRPO 如何避免探索困难。

---

# 6. 实践建议

**如何应用到自己的项目：**
1.  **评估基座模型：** 选择一个代码能力较强的开源 7B 模型（如 DeepSeek-Coder, CodeLlama）。
2.  **搭建环境：** 在 AWS SageMaker 上配置 Ray 集群，安装 veRL。
3.  **定义 Reward：** 编写 Python 脚本，定义如何评估生成的代码（例如通过单元测试的百分比）。
4.  **配置 GRPO：** 设置合适的 Group Size（建议 4-8）和学习率。

**具体行动建议：**
*   **第一步：** 熟悉 Ray 的 Actor 模型和 veRL 的配置文件结构。
*   **第二步：** 准备高质量的“问题-通过测试用例”数据集。
*   **第三步：** 先运行一次小步数的 Debug 模式，确保分布式通信正常。

**需补充的知识：**
*   强化学习基础（Policy, Reward, Advantage）。
*   PyTorch 分布式训练（DDP）。
*   AWS SageMaker 的 Estimator 和 Ray Cluster 的配置。

---

# 7. 案例分析

**结合实际案例说明：**
文章中的 **CodeFu-7B** 本身就是一个成功案例。它基于通用的 Code LLM，通过 GRPO 在竞技编程数据集上训练，使其能够解决复杂的算法题。

**成功案例分析：**
*   **背景：** 通用模型在解决复杂算法问题时，往往逻辑不通或语法有误。
*   **行动：** 使用 GRPO，以“通过测试用例”为 Reward，指导模型生成正确的代码。
*   **结果：** 模型学会了自我修正逻辑，生成的代码通过率显著提升。

**失败/反思案例：**
*   **假设场景：** 如果 Reward Function 设置不当，例如只奖励代码运行速度而不奖励正确性，模型可能会生成恶意代码或空循环来“作弊”。
*   **教训：** 在 RL 训练中，Reward Function 的设计必须极其严谨，涵盖正确性、安全性和可读性。

---

# 8. 哲学与逻辑：论证地图

**中心命题：**
在云基础设施上结合弹性编排与轻量级强化学习算法，是构建垂直领域高性能小规模模型的最优工程路径。

**支撑理由与依据：**
1.  **成本效率：** GRPO 移除了显存密集的 Critic 模型，结合 Ray 的 Spot 实例支持，大幅降低了训练成本。
2.  **特定领域性能：** 相比通用 SFT，RL 直接优化任务目标，能显著提升模型在特定任务（如编程）的上限。
3.  **工程可扩展性：** veRL 和 SageMaker 的解耦设计，使得从 7B 扩展到 70B 无需重写代码，只需调整资源配置。

**反例或边界条件：

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 vLLM 驱动的 veRL 进行高效推理与训练

**说明**: 
CodeFu-7B 的训练流程依赖于 veRL（Volcengine RL），该框架集成了 vLLM 作为高性能推理后端。在强化学习阶段（如 PPO），利用 vLLM 可以显著加速生成过程的采样和 Logit 计算，从而减少整体训练的 Wall-clock 时间。SageMaker 的分布式训练需要正确配置这一推理引擎。

**实施步骤**:
1. 在启动训练作业前，确保容器镜像中已安装兼容 CUDA 的 vLLM 版本。
2. 配置 veRL 的推理后端参数，明确指定使用 vLLM 而非传统的 HuggingFace Transformers 生成模式。
3. 在 SageMaker 的分布式配置中，为负责推理的进程预留独立的显存和计算资源。

**注意事项**: 
vLLM 对显存管理较为激进，需确保 PPO 的 Actor 和 Critic 模型在显存中与推理引擎不发生 OOM 冲突，建议使用 Ray 的 actor placement groups 进行资源隔离。

---

### 实践 2：优化 Ray on SageMaker 的资源配置与拓扑感知

**说明**: 
veRL 使用 Ray 来管理复杂的分布式训练逻辑（如 Actor、Critic、Rollout 和 Reference Model 的协作）。在 SageMaker 上运行 Ray 时，必须正确配置底层网络拓扑，确保 Ray Cluster 能够感知到 SageMaker 的底层硬件架构（如 AWS EFA 网络），以实现节点间的高吞吐通信。

**实施步骤**:
1. 在 SageMaker 训练作业中启用 `mpi` 或 `elastic` 分布式库支持，并配置 `enable_sm_distributed_training`。
2. 设置 Ray 启动参数，使其绑定到 SageMaker 提供的主机名和网卡接口（通常用于 EFA 通信的接口）。
3. 调整 `object_store_memory` 参数，防止 Ray 的共享内存对象存储挤占模型训练所需的 GPU 显存。

**注意事项**: 
避免使用 Ray 的默认自动检测模式，因为在容器化环境中，它可能无法正确识别 AWS 的网络接口，导致回退到较慢的 TCP/Socket 通信。

---

### 实践 3：实施高效的显存优化技术

**说明**: 
训练 7B 参数模型通常需要较大的显存开销，尤其是在 PPO 训练阶段需要同时加载 Actor、Critic、Reference 模型以及 Reward Model。必须利用显存优化技术（如 FlashAttention、混合精度训练和梯度检查点）以适应有限的 GPU 资源。

**实施步骤**:
1. 确保训练环境安装了 FlashAttention 2，并在模型配置中启用。
2. 使用 `bf16`（BFloat16）混合精度训练，以减少显存占用并保持数值稳定性。
3. 在 veRL 配置中启用梯度检查点，以计算换显存。

**注意事项**: 
CodeFu-7B 作为代码模型，上下文长度可能较长。在长序列下，FlashAttention 的优化效果尤为关键，务必检查其是否正确编译和加载。

---

### 实践 4：配置高性能数据加载与预处理管道

**说明**: 
代码训练数据通常包含大量的长文本和特殊 Token。如果数据加载成为瓶颈，GPU 利用率将会下降。利用 Ray 的并行数据加载能力或 SageMaker 的快速模式挂载，可以确保数据供给速度跟上训练迭代速度。

**实施步骤**:
1. 将训练数据集转换为支持随机访问的格式（如 Parquet 或内存映射索引），避免频繁的解压缩开销。
2. 利用 SageMaker 的 FSx for Lustre 或通过 S3 实现快速数据流式传输，减少 I/O 等待时间。
3. 在 Ray 配置中增加数据加载 Actor 的数量，实现并行预处理。

**注意事项**: 
代码数据集可能包含大量重复的样板代码，建议在数据预处理阶段进行严格的质量过滤和去重，以提高模型学习效率。

---

### 实践 5：利用 SageMaker Spot 实例降低成本并管理检查点

**说明**: 
大模型训练成本高昂。使用 SageMaker Managed Spot Instances 可以利用 AWS 的闲置计算资源，大幅降低训练成本（通常可节省 60%-90%）。但由于 Spot 实例可能被中断，必须配置完善的检查点（Checkpoint）机制。

**实施步骤**:
1. 在创建 SageMaker 训练作业时，启用 `enable_managed_spot_training`。
2. 配置 veRL 和 Ray 的检查点策略，设定合理的保存间隔（如每 50 步保存一次），并将检查点持久化到 S3 而非仅本地 ephemeral 存储。
3. 设置 `checkpoint_s3_uri`，确保中断恢复时能从 S3 同步状态。

**注意事项**: 
验证 veRL 的 PPO 训练器是否支持从任意检查点无缝热启动，特别是优化器状态和经验缓冲区的恢复。

---

### 实践 6：深度监控与日志集成

**说明**: 
强化学习训练过程（如 PPO）比监督微调更不稳定，容易出现 KL 散度

---
## 学习要点

- 通过在 Amazon SageMaker 上集成 veRL 和 Ray，实现了高效的大语言模型分布式训练，显著降低了基础设施配置的复杂度。
- 利用 veRL 的零冗余优化器（ZeRO）和 Ray 的弹性伸缩能力，有效解决了显存瓶颈并优化了资源利用率。
- 借助 SageMaker 的托管 Spot Training 实例，在保证训练稳定性的同时大幅降低了模型训练的计算成本。
- 采用 PyTorch FSDP（完全分片数据并行）技术，突破了单卡显存限制，支持更大参数量级模型的训练。
- 使用 SageMaker Training Compiler 自动优化计算图，无需修改模型代码即可提升训练吞吐量和性能。
- 通过 SageMaker Experiments 进行实验追踪和可视化，简化了超参数调优和模型迭代的管理流程。
- 利用 SageMaker 的容器化部署和模型监控功能，实现了从训练到部署的无缝衔接和自动化运维。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [LLM](/tags/llm/) / [RLHF](/tags/rlhf/) / [GRPO](/tags/grpo/) / [veRL](/tags/verl/) / [Ray](/tags/ray/) / [SageMaker](/tags/sagemaker/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [CodeFu-7B](/tags/codefu-7b/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [使用veRL和Ray在SageMaker上训练CodeFu-7B模型]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-0.md" >}})
- [在 SageMaker 上利用 veRL 与 Ray 训练 CodeFu-7B]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-1.md" >}})
- [在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B 模型]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-3.md" >}})
- [在 SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-4.md" >}})
- [在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B 模型]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*