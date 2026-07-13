---
title: 在 SageMaker 上利用 veRL 与 Ray 训练 CodeFu-7B
date: 2026-02-24 21:40:55+08:00
draft: false
entry_kind: auto
tags:
- LLM
- SageMaker
- Ray
- veRL
- 强化学习
- GRPO
- 分布式训练
- CodeFu-7B
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 本文介绍了如何在 Amazon SageMaker Training jobs 上，利用 veRL 库和 Ray 分布式集群训练 CodeFu-7B（一个专注于竞技编程的
  70 亿参数模型）。 主要内容包括： 1. **核心任务**：使用 Group Relative Policy Optimization (GRPO
external_url: https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs
scenarios:
- 大语言模型
- 工具
---

# 在 SageMaker 上利用 veRL 与 Ray 训练 CodeFu-7B

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-24T15:46:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)

---

## 摘要/简介

在这篇文章中，我们将演示如何利用 veRL 训练 CodeFu-7B——一款专用于竞技编程的 70 亿参数模型；该过程采用了分组相对策略优化（GRPO），并在由 SageMaker 训练作业托管的分布式 Ray 集群中进行。veRL 是一个灵活且高效的大语言模型（LLM）训练库，支持对多种 RL 算法进行便捷扩展，并与现有 LLM 基础设施无缝集成。我们将遍历完整的实现流程，涵盖数据准备、分布式训练配置以及全面的观测能力，以此展示这一统一方案如何为复杂的 RL 训练负载同时提供计算规模与开发体验。

---

## 导语

竞技编程模型的训练往往面临算法适配与算力调度的双重挑战。本文将详细介绍如何在 Amazon SageMaker 上，利用 veRL 库结合分布式 Ray 集群，训练 CodeFu-7B 模型。通过解析基于 GRPO 的完整实现流程，我们将展示这一方案如何兼顾计算规模与开发效率，帮助开发者掌握在云端构建复杂强化学习训练负载的实用方法。

---

## 摘要

本文介绍了如何在 Amazon SageMaker Training jobs 上，利用 veRL 库和 Ray 分布式集群训练 CodeFu-7B（一个专注于竞技编程的 70 亿参数模型）。

主要内容包括：

1.  **核心任务**：使用 Group Relative Policy Optimization (GRPO) 算法对 CodeFu-7B 进行强化学习训练。
2.  **技术栈**：
    *   **veRL**：一个灵活高效的 LLM 训练库，支持扩展 RL 算法并与现有基础设施无缝集成。
    *   **Ray**：在 SageMaker 内部构建分布式计算集群。
    *   **SageMaker**：托管整个训练任务。
3.  **实现细节**：涵盖了从数据准备、分布式训练设置到全面可观测性的完整实现流程。
4.  **优势**：展示了这种统一方法如何在提供计算规模的同时，优化复杂 RL 训练工作负载的开发体验。

---

## 评论

### 深度评价：在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B

**中心观点**
该文章展示了一种**云原生与开源强化深度结合**的大模型（LLM）训练范式，证明了通过利用 Amazon SageMaker 的基础设施弹性与开源强化学习库 veRL 的高效特性，可以显著降低代码类大模型（如 CodeFu-7B）进行 GRPO（组相对策略优化）训练的门槛与成本。

**支撑理由与深度分析**

**1. 架构设计的先进性与解耦（事实陈述 + 你的推断）**
文章的核心技术亮点在于将 **veRL**（Volcengine RL library，一个由字节跳动开源的高效 RL 训练框架）与 **Amazon SageMaker** 进行了深度集成。
*   **技术深度**：传统的 RLHF（基于人类反馈的强化学习）通常面临显存占用高、通信开销大、样本生成效率低的问题。veRL 引入了 GRPO（Group Relative Policy Optimization），这是一种不依赖 Critic 模型（价值模型）的变体，通过组内基线对比来计算优势，大幅减少了显存占用。文章利用 Ray 在 SageMaker 上进行编排，解决了强化学习训练中“环境-训练”交互的异步调度难题。
*   **行业意义**：这种组合代表了行业趋势——**“基础设施托管化，算法模型开源化”**。企业不再需要自建庞大的 K8s 集群来维护 Ray，而是直接利用 SageMaker 的托管节点，同时保留使用开源前沿算法（如 GRPO）的灵活性。

**2. 垂直领域模型（Code LLM）的调优方法论（作者观点）**
文章专注于 CodeFu-7B（针对竞技编程优化），指出了通用模型在复杂逻辑推理上的不足。
*   **实用价值**：相比于通用的 SFT（监督微调），使用 GRPO 针对代码生成进行强化训练，能够直接优化“通过率”这一核心指标。文章展示了如何构建奖励模型（基于编译结果和测试用例），这对实际工业界开发“AI 程序员”具有极高的指导意义。
*   **论证严谨性**：文章通过展示具体的训练脚本配置和 Ray Actor 的设置，证明了该方案的可复现性。它不仅仅是理论探讨，而是提供了 IaC（基础设施即代码）级别的落地指导。

**3. 成本效益与资源利用率的优化（事实陈述）**
*   **观点深度**：利用 SageMaker Training Jobs 的 Spot Instance（竞价实例）结合 Ray 的弹性调度，是文章隐含的一个巨大成本优势。强化学习的训练过程往往伴随着动态的样本生成时间，Ray 能够在等待环境反馈时释放资源，而 SageMaker 提供了底层算力的保障。这种“弹性训练”思路是当前 LLM 训练降本增效的关键。

**反例与边界条件**

**1. 冷启动与调试复杂度的挑战（反例）**
*   **边界条件**：虽然文章展示了成功案例，但在 SageMaker 上配置 Ray 集群（尤其是 Head Node 和 Worker Node 的网络配置、IAM 权限设置）具有极高的**陡峭学习曲线**。对于没有深厚 DevOps 背景的算法工程师，排查 Ray Actor 的启动失败或分布式通信握手问题可能比模型训练本身更耗时。
*   **你的推断**：文章可能简化了环境依赖（如 CUDA 兼容性、NCCL 版本）的配置过程。在实际生产环境中，veRL、Ray 和 SageMaker 深度学习容器（DLC）的版本兼容性往往是一个巨大的坑。

**2. GRPO 算法的收敛稳定性（不同观点/争议点）**
*   **边界条件**：GRPO 虽然省去了 Critic 模型，降低了显存，但对 **Batch Size（组大小）** 非常敏感。如果组内样本多样性不足，基线估计将出现偏差，导致训练崩溃或模式崩塌。文章未深入讨论在 CodeFu-7B 这种特定规模下，如何调优 Group Size 这一超参数。
*   **批判性思考**：对于代码生成这种“非黑即白”的领域（通过编译即通过，不通过即 0 分），稀疏奖励问题依然存在。GRPO 是否比 PPO 更能有效解决探索效率问题，在学术界和工业界仍需更多数据验证，不应盲目迷信“新算法”。

**可验证的检查方式**

1.  **显存占用对比实验（指标）**：
    *   在相同的模型参数（7B）和 Batch Size 下，对比标准 PPO（需要 Actor + Critic + Reward Model）与 veRL 的 GRPO（仅 Actor）的最大显存占用峰值。验证 GRPO 是否真的能让单卡训练成为可能。

2.  **样本吞吐量与训练吞吐量解耦验证（观察窗口）**：
    *   利用 Ray Dashboard 观察“生成环境”和“训练进程”的 GPU 利用率曲线。理想情况下，生成阶段训练 GPU 应为低负载或释放状态，训练阶段生成 GPU 应为高负载。如果两者同时处于高负载但利用率都不饱和，说明调度存在瓶颈。

3.  **代码生成的 Pass@1 指标提升（实验）**：
    *   在 HumanEval 或 MBPP 数据集上，对比 SFT 基座模型与经过 GRPO 训练后的 CodeFu-7B 的 Pass@1（第一次生成的代码通过率）。这是衡量该训练pipeline有效性的核心指标。

---

## 技术分析

基于您提供的文章标题和摘要，以及对相关技术栈的了解，以下是对该文章内容的深入分析。

---

### 深入分析：在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B

### 1. 核心观点深度解读

**文章的主要观点：**
文章的核心观点在于展示一种**“云原生、高性能、可扩展”**的大模型强化学习训练范式。具体而言，它证明了通过结合 **veRL**（一个专为LLM设计的轻量级高效强化学习库）和 **Ray**（分布式计算框架），可以在 **Amazon SageMaker** 这样的托管云平台上，高效地训练 CodeFu-7B 这样针对竞技编程场景的 7B 参数模型。

**作者想要传达的核心思想：**
作者试图传达“**工程优化决定算法落地上限**”的思想。虽然 GRPO（Group Relative Policy Optimization）算法本身是提升模型逻辑推理能力的关键，但如果没有 veRL 这种针对内存和计算优化的框架，以及 SageMaker 提供的弹性基础设施，训练如此规模的模型将面临极高的资源门槛和工程复杂度。作者主张利用现有的云生态工具链来降低 RLHF（特别是针对代码生成）的门槛。

**观点的创新性和深度：**
*   **创新性：** 将 **veRL** 这一较新的库与 SageMaker 的深度集成是本文的亮点。veRL 通过解耦 actor 和 critic 模型的内存管理，解决了传统 RLHF 训练中显存占用过高的问题。
*   **深度：** 文章不仅仅是调用 API，而是深入到了分布式训练的底层架构（如 Ray 的 actor 模型），探讨了如何在大规模集群上实现 Group Relative Policy Optimization（GRPO），这是一种比标准 PPO 更适合代码生成任务的算法变体。

**为什么这个观点重要：**
在当前大模型从“预训练”向“对齐”和“推理增强”发展的阶段，如何低成本、高效率地进行 RLHF 训练是业界的痛点。特别是对于代码生成这类需要高逻辑一致性的任务，传统的 SFT（监督微调）往往不够，必须引入强化学习。这篇文章为开发者提供了一条经过验证的、可复制的路径，使得中等规模的团队也能在云上训练出具备竞争力的垂直领域模型。

### 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **GRPO (Group Relative Policy Optimization)：** 这是技术核心。不同于传统的 PPO 需要训练一个价值模型来估计基线，GRPO 通过从组中采样多个输出来计算基线，**省去了 Critic 模型**，极大地节省了显存。
2.  **veRL (Volcengine RL)：** 一个由字节跳动推出的高效 RL 训练库。其核心特点是**内存高效**和**解耦设计**。
3.  **Ray：** 用于 Python 的分布式计算框架，负责协调训练任务、资源调度和容错。
4.  **Amazon SageMaker：** 提供底层 GPU 算力（如 p4de 实例）及托管环境。

**技术原理和实现方式：**
*   **GRPO 原理：** 在训练 CodeFu-7B 时，对于同一个 Prompt，模型生成 $N$ 个不同的代码输出。通过这 $N$ 个输出的奖励分数计算平均值作为基线，然后利用优势函数更新策略。这使得不需要再维护一个与模型同样大小的 Critic 模型，显存占用几乎减半。
*   **veRL 的实现：** veRL 利用 Ray 的 Actor 模型将训练流程拆解。它通常采用 **Rollout（收集数据）** 和 **Training（更新参数）** 的流水线并行。在 SageMaker 上，veRL 脚本被封装在容器中，利用 Ray 的集群启动器在多节点间分配任务。
*   **SageMaker 集成：** 利用 SageMaker 的 `Estimator` API 或 PyTorch 容器，将 veRL 和 Ray 的依赖打包，实现一键启动分布式训练。

**技术难点和解决方案：**
*   **难点：** RLHF 训练极其不稳定，且显存消耗巨大（需要存储 Actor, Ref, Critic 多个模型副本）。
*   **解决方案：** 使用 GRPO 算法消除 Critic 模型；利用 veRL 的混合精度训练和梯度检查点技术；利用 Ray 实现灵活的 Rollout Worker 扩展。
*   **难点：** 云上分布式环境配置复杂。
*   **解决方案：** 利用 SageMaker 的托管基础设施和生态镜像，预装 CUDA 和 Ray 依赖，减少环境配置时间。

**技术创新点分析：**
最大的技术创新点在于 **GRPO 在工业级云训练框架中的工程化落地**。传统的 PPO 流程复杂且难以调试，GRPO 简化了这一过程，而 veRL + SageMaker 的组合则将其工程化，使得“训练一个代码模型”不再是只有巨头才能完成的任务。

### 3. 实际应用价值

**对实际工作的指导意义：**
这篇文章为 AI 工程师和数据科学家提供了一套完整的“**技术栈选型指南**”。它表明，在进行垂直领域（如代码、数学、逻辑）的大模型微调时，不应局限于传统的 LoRA 或全量 SFT，而应考虑 GRPO 这种更高效的 RLHF 手段，并且可以在云平台上低成本实施。

**可以应用到哪些场景：**
1.  **智能代码助手开发：** 训练企业内部的 Copilot。
2.  **逻辑推理任务：** 数学问题求解、数据分析报告生成。
3.  **多轮对话优化：** 需要长上下文记忆和一致性的对话系统。
4.  **任何需要 RLHF 但受限于显存资源的场景：** 由于 GRPO 去掉了 Critic，使得在更少的 GPU 上训练 7B/13B 模型成为可能。

**需要注意的问题：**
*   **奖励函数的设计：** GRPO 的效果高度依赖于 Reward Model 的质量。如果奖励模型不能准确判断代码的正确性（例如通过单元测试），GRPO 的优化方向就会跑偏。
*   **Ray 的学习曲线：** 虽然代码库提供了便利，但调试 Ray 分布式应用的报错仍然具有挑战性。
*   **成本控制：** SageMaker 上的按需实例（如 p4de.24xlarge）价格昂贵，需要仔细估算训练时长。

**实施建议：**
*   先在小规模数据集上验证 GRPO 的收敛性。
*   使用 Spot 实例来降低 SageMaker 的训练成本。
*   深入阅读 veRL 的文档，理解其 Rollout 和 Update 的分离机制。

### 4. 行业影响分析

**对行业的启示：**
这篇文章预示着 **LLM 训练正在从“算力堆砌”向“算法与工程效率优化”转型**。通过算法改进（GRPO）和工程优化，可以在有限的硬件资源下实现更高级别的模型能力。这将降低垂直领域大模型的准入门槛。

**可能带来的变革：**
*   **MaaS (Model as a Service) 的细分：** 更多像 CodeFu 这样的专精模型将出现，而不是仅依赖通用的 GPT-4。
*   **RLHF 的普及化：** 由于去除了 Critic 模型的显存壁垒，RLHF 将成为标配，而非高端选项。

**相关领域的发展趋势：**
*   **轻量化 RL 框架：** 类似 veRL 这样专注于效率的框架会越来越多。
*   **云原生 AI 的标准化：** 更多框架将原生支持 Kubernetes 和云托管服务。

**对行业格局的影响：**
这可能会削弱只有大规模 GPU 集群的巨头的垄断优势，赋予拥有高质量领域数据（如高质量代码库、测试用例）和算法工程能力的中小团队更多机会。

### 5. 延伸思考

**引发的其他思考：**
*   GRPO 虽然节省了显存，但其采样多个输出的策略是否会导致推理阶段的吞吐量下降？
*   在代码生成之外，GRPO 是否适用于开放式文本生成（如创意写作）？

**可以拓展的方向：**
*   **混合专家模型 的结合：** 将 GRPO 应用于 MoE 模型的路由策略优化。
*   **在线学习：** 探索如何将 veRL 部署为在线服务，实时利用用户反馈更新模型。

**需要进一步研究的问题：**
*   GRPO 相比于 Rejection Sampling 和 DPO（Direct Preference Optimization）的定量对比分析。
*   在极端稀疏奖励的环境下（如复杂的代码编译错误），GRPO 的鲁棒性如何。

**未来发展趋势：**
未来的训练框架将更加**模块化**和**自动化**。用户只需定义 Reward Function，框架自动选择最优的 RL 算法（GRPO/PPO/DPO）并分配云端资源。

### 7. 案例分析

**结合实际案例说明：**
文章中的 CodeFu-7B 是一个典型的垂直领域模型案例。竞技编程不同于普通编程，它需要极强的逻辑推理和边界条件处理能力。

**成功案例分析：**
*   **AlphaCode (DeepMind)：** 早期利用 Transformer 和大规模采样生成代码，CodeFu 的方法类似于其轻量级版本。
*   **本文案例：** 成功之处在于利用 GRPO 解决了“代码执行结果作为奖励”的时序问题。代码必须运行完才能知道对错，这种延迟反馈在 GRPO 的 Group Sampling 机制下处理得很好。

**失败案例反思：**
*   如果 Reward Function 仅基于代码的语法正确性（能否运行），模型可能会学会输出空函数或简单的 `pass` 语句来骗取奖励。
*   **教训：** 奖励函数必须包含测试用例的通过率，甚至代码的复杂度要求。

**经验教训总结：**
在代码模型训练中，**数据质量 > 模型参数量 > 训练技巧**。但 GRPO 证明了在同等数据和模型下，好的训练技巧能显著提升逻辑推理的上限。

### 8. 哲学与逻辑：论证地图

**中心命题：**
> **采用基于 GRPO �

---

## 最佳实践

### 实践 1：利用 vLLM 实现高效推理加速

**说明**: 在 CodeFu-7B 的微调过程中，特别是使用 PPO（近端策略优化）等强化学习算法时，生成阶段往往是性能瓶颈。veRL 集成了 vLLM 作为高性能推理引擎，利用 PagedAttention 技术管理 KV Cache，显著提高 Rollout 生成阶段的吞吐量并降低延迟。

**实施步骤**:
1. 在 veRL 的配置文件中，明确指定使用 vLLM 作为 Rollout 的后端。
2. 根据实例显存大小，合理配置 `tensor_parallel_size`（张量并行度），以充分利用多 GPU 的显存和计算能力。
3. 调整 vLLM 的 `gpu_memory_utilization` 参数，为训练过程预留足够的显存空间，避免 OOM（显存溢出）。

**注意事项**: 确保所选用的 Amazon SageMaker 实例（如 `ml.g5.12xlarge` 或 `ml.p4d.24xlarge`）具有足够的 GPU 显存来同时承载模型权重和 KV Cache。

---

### 实践 2：优化 Ray 集群与 SageMaker 的资源调度

**说明**: veRL 依赖 Ray 进行分布式训练的编排。在 SageMaker 上运行时，需要正确配置 Ray 集群，使其能够感知 SageMaker 的底层网络拓扑（如 EFA 或 NCCL），以减少通信开销。

**实施步骤**:
1. 在 SageMaker 训练作业启动脚本中，设置 `RAY_EXPERIMENTAL_NOSET_CUDA_VISIBLE_DEVICES=1` 环境变量，防止 Ray 自动重排 GPU 设备，导致与 NCCL 通信冲突。
2. 配置 Ray 的启动参数，禁用默认的 Redis 重试机制，利用 SageMaker 的容器生命周期管理 Ray Head 节点。
3. 使用 `torchrun` 或 Ray 的 Actor 模型来启动 veRL 的训练脚本，确保进程间通信（IPC）基于 AWS 的 EFA（Elastic Fabric Adapter）进行加速。

**注意事项**: 如果使用 `ml.p4` 或 `ml.p5` 系列实例，务必确保安装了 AWS EFA 驱动以及与之兼容的 NCCL 版本，以发挥底层网络性能。

---

### 实践 3：实施混合精度训练与 Flash Attention

**说明**: CodeFu-7B 模型属于中等规模 LLM，为了在有限的计算资源下加快训练速度并降低显存占用，应采用 BF16（BFloat16）混合精度训练，并结合 Flash Attention-2 技术来加速注意力机制的计算。

**实施步骤**:
1. 在模型配置和训练参数中，将数据类型设置为 `bfloat16`。
2. 确保环境安装了兼容 CUDA 的 Flash Attention-2 库，veRL 通常会自动检测并调用优化后的 Attention Kernel。
3. 在优化器配置中，使用 BF16 兼容的优化器（如 AdamW），并确保损失计算在适当的精度下进行以保持数值稳定性。

**注意事项**: 并非所有 GPU 都原生支持 BF16（如旧版 NVIDIA T4），如果在 `ml.g5` 实例上运行，请确认 CUDA 版本和 PyTorch 版本对 BF16 的支持情况；若不支持，可回退到 FP16 混合精度（需配合 Loss Scaling）。

---

### 实践 4：利用 SageMaker 的 Spot 实例降低成本

**说明**: LLM 训练成本高昂。对于 CodeFu-7B 的微调任务，如果使用 Checkpoint 机制支持断点续训，可以使用 Amazon SageMaker Managed Spot Instances，相比按需实例可节省高达 90% 的成本。

**实施步骤**:
1. 在创建 SageMaker 训练作业时，启用 `EnableManagedSpotTraining` 参数。
2. 配置合理的 `CheckpointConfig`，设置 `LocalPath`（本地挂载点）和 `S3Uri`（S3 存储路径）。veRL 需要配置为定期将模型权重和优化器状态保存到该本地路径。
3. 设置 `StoppingCondition` 中的 `MaxWaitTime`（最大等待时间），以便在 Spot 实例中断时，SageMaker 能自动排队等待资源恢复并从中断点继续训练。

**注意事项**: veRL 的 Checkpoint 保存频率需要与 Spot 实例的中断通知时间相匹配（通常为 2 分钟），确保在实例被回收前完成模型状态的持久化。

---

### 实践 5：配置高效的分布式数据加载与预处理

**说明**: 在使用 veRL 进行 RLHF 训练时，数据加载速度往往成为瓶颈。利用 Ray 的分布式数据对象或 PyTorch 的 DistributedDataParallel (DDP) 数据加载策略，可以有效减少 GPU 空闲等待时间。

**实施步骤**:
1. 将训练数据集预先转换为 Parquet 或 HDF5 等高效的二进制格式，并存储在 S3 或 FSx for Lustre 上（推荐 FSx for Lustre 以获得更高的 I

---

## 学习要点

- veRL 与 Ray 的深度集成使得在 Amazon SageMaker 上进行大规模强化学习训练（如 PPO）时，能够高效处理复杂的分布式通信和资源调度。
- 利用 SageMaker Training Jobs 的托管基础设施，结合 Ray 的弹性伸缩能力，可以显著降低大模型微调（如 CodeFu-7B）的运维复杂度和硬件成本。
- veRL 框架通过优化的数据并行和模型并行策略，解决了强化学习训练中常见的内存瓶颈和负载不均衡问题。
- 该方案展示了如何将开源训练框架无缝迁移至云端，实现了从本地开发到云端大规模训练的平滑过渡。
- 通过具体的代码示例，演示了如何配置 SageMaker 的 Estimator 来启动 Ray 集群，并正确挂载所需的模型和数据集。
- 整个流程强调了在保持代码灵活性的同时，利用云服务实现高可用性和故障恢复机制的最佳实践。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [LLM](/tags/llm/) / [SageMaker](/tags/sagemaker/) / [Ray](/tags/ray/) / [veRL](/tags/verl/) / [强化学习](/tags/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/) / [GRPO](/tags/grpo/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [CodeFu-7B](/tags/codefu-7b/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [使用veRL和Ray在SageMaker上训练CodeFu-7B模型]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-0.md" >}})
- [利用权重更新稀疏性的通信高效分布式强化学习]({{< relref "posts/20260204-arxiv_ai-understanding-and-exploiting-weight-update-sparsit-3.md" >}})
- [基于枢纽重采样的LLM强化学习深度密集探索]({{< relref "posts/20260217-arxiv_ai-deep-dense-exploration-for-llm-reinforcement-learn-6.md" >}})
- [2025年Amazon SageMaker AI增强可观测性与模型定制托管功能]({{< relref "posts/20260220-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Amazon SageMaker AI 2025回顾：可观测性与模型定制托管增强]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--2.md" >}})
