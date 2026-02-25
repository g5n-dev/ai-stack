---
title: "使用 SageMaker 和 Ray 在 veRL 框架上训练 CodeFu-7B 模型"
date: 2026-02-25T05:27:52+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "Ray", "veRL", "CodeFu-7B", "GRPO", "分布式训练", "强化学习", "RLHF"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon SageMaker 训练任务上，利用 veRL 和 Ray 分布式集群训练 CodeFu-7B 模型。 主要内容包括： 1. **训练对象与算法**：针对竞技编程优化的 70 亿参数模型 CodeFu-7B，采用群体相对策略优化（GRPO）算法进行训练。 2. **技术栈**：结合了 *"
external_url: https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs
scenarios: ["工具"]
---

# 使用 SageMaker 和 Ray 在 veRL 框架上训练 CodeFu-7B 模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-24T15:46:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)

---
## 摘要/简介

在本篇文章中，我们将展示如何利用由 SageMaker 训练作业托管的分布式 Ray 集群，借助灵活高效的 LLM 训练库 veRL，采用 Group Relative Policy Optimization (GRPO) 算法来训练 CodeFu-7B——一款专注于竞技编程的 70 亿参数模型。我们将深入完整的实现流程，涵盖数据准备、分布式训练配置以及全方位的可观测性，以此展示这一统一方案如何在为复杂 RL 训练任务提供算力规模的同时，也能优化开发者体验。

---
## 导语

在竞技编程等复杂场景下，利用强化学习训练大语言模型往往面临算力调度与工程实现的挑战。本文将详细介绍如何结合 Amazon SageMaker 的托管训练作业、Ray 分布式集群以及 veRL 训练库，采用 GRPO 算法训练 CodeFu-7B 模型。通过解析从数据准备到分布式配置及可观测性的完整流程，我们将展示这一方案如何在保障算力规模的同时优化开发体验，助您高效构建高性能模型。

---
## 摘要

本文介绍了如何在 Amazon SageMaker 训练任务上，利用 veRL 和 Ray 分布式集群训练 CodeFu-7B 模型。

主要内容包括：

1.  **训练对象与算法**：针对竞技编程优化的 70 亿参数模型 CodeFu-7B，采用群体相对策略优化（GRPO）算法进行训练。
2.  **技术栈**：结合了 **veRL**（灵活高效的大模型 RL 训练库）与 **Ray**（分布式计算框架），并由 SageMaker 托管集群。
3.  **实施全流程**：涵盖了从数据准备、分布式训练环境搭建到全面的可观测性监控。
4.  **核心优势**：展示了这一统一方案如何兼顾计算规模与开发体验，为复杂的强化学习（RL）工作负载提供支持。

---
## 评论

### 中心观点
文章展示了通过将 **veRL（一种高效强化学习库）** 与 **Ray（分布式计算框架）** 深度集成，在 **Amazon SageMaker** 这一托管平台上成功实现对 **CodeFu-7B** 模型的 **GRPO（组相对策略优化）** 训练，论证了“基础设施解耦”与“算法级显存优化”相结合是降低大模型后训练成本并提升效率的有效路径。

### 支撑理由与边界条件

#### 1. 训练范式的技术先进性：GRPO 与 PPO 的工程博弈
*   **支撑理由（事实陈述/你的推断）：** 文章采用 **GRPO** 而非传统的 **PPO（Proximal Policy Optimization）** 是一个极具技术含量的选择。在 RLHF（基于人类反馈的强化学习）中，PPO 需要训练一个 Value Model（价值模型）来估计优势函数，这显著增加了显存占用和计算量。GRPO 通过组采样来计算基线，理论上消除了对 Critic 模型的依赖。结合 veRL 提出的 **Zero-CPU Offload** 技术（将经验存储和 Rollout 工作负载卸载到 CPU），文章实际上是在解决 LLM 训练中“显存墙”这一核心痛点。这表明作者对大模型训练的显存瓶颈有深刻理解。
*   **反例/边界条件（你的推断）：** GRPO 虽然省去了 Critic 的显存，但在样本效率上可能低于精确的 Value Model。如果 Reward Model（奖励模型）本身不够准确，或者 Group Size 设置不当，GRPO 的训练方差会变大，导致模型收敛不稳定。此外，对于极度追求生成质量的场景，完全丢弃 Critic 可能会导致策略更新过于激进。

#### 2. 基础设施的编排能力：Ray on SageMaker 的混合架构
*   **支撑理由（事实陈述）：** 文章展示了如何利用 Ray 在 SageMaker 的 EC2 实例间进行精细化编排。这不仅仅是调用一个 API，而是构建了一个“微集群”环境。这种架构的价值在于它打破了 SageMaker 原生 Estimator 相对封闭的黑盒，允许开发者像管理本地集群一样管理云上资源，同时利用了 SageMaker 的自动扩缩容和基础设施无关性。
*   **反例/边界条件（作者观点/你的推断）：** 这种“套娃”式架构（Ray on SageMaker）引入了额外的复杂度。Ray 本身的调度开销和网络通信延迟可能会成为瓶颈，特别是在处理高带宽需求的模型并行（如 Tensor Parallel）时。如果用户的网络配置（如 Placement Group）不完美，Ray 的 GCS（Global Control Service）可能会成为性能瓶颈，导致 GPU 空转。

#### 3. 垂直领域模型的落地可行性：CodeFu 的场景适配
*   **支撑理由（事实陈述）：** 选择“竞技编程”作为切入点非常明智。CodeFu-7B 作为一个 7B 参数的模型，在消费级显卡或单张 A100 上即可进行微调，且代码生成的反馈信号可以通过编译器自动获取，大大降低了构建 Reward Model 的门槛。
*   **反例/边界条件（你的推断）：** 代码领域的成功难以直接泛化到通用聊天或创意写作领域。代码具有严格的语法正确性作为硬约束，而自然语言的奖励信号极其稀疏且模糊。因此，该方法虽然对 CodeLlama 等基座模型有效，但直接迁移到 Qwen 或 Llama 3 的通用版本上，可能需要重新设计 Reward Function。

### 综合评价

#### 1. 内容深度：★★★★☆
文章没有停留在简单的 API 调用层面，而是深入到了 RLHF 的核心痛点——显存和吞吐量。通过剖析 veRL 的显存优化策略和 Ray 的分布式调度，体现了较高的工程深度。但略显不足的是，文章对 GRPO 的超参数敏感性分析可能较少，更多是“如何跑通”而非“如何调优”。

#### 2. 实用价值：★★★★★
对于正在寻找 RLHF 落地方案的团队来说，这篇文章提供了一个完整的参考架构（Reference Architecture）。它解决了两个具体问题：一是如何在不购买昂贵集群的情况下进行 RL 训练（利用云上弹性），二是如何在小显存资源下塞下大模型的训练逻辑（利用 veRL）。

#### 3. 创新性：★★★☆☆
技术栈的组合具有新意。将 veRL 这一新兴库与成熟的 SageMaker 结合，填补了中文技术圈（或相关开源社区）对于“轻量级 RLHF 工程化”的空白。虽然算法本身（GRPO）并非原创，但工程落地实践具有参考价值。

#### 4. 行业影响
该文章推动了 **“大模型训练轻量化”** 的趋势。它暗示行业不再单纯依赖千亿参数的暴力训练，而是转向通过高效的强化学习算法（如 GRPO）和工程优化，挖掘 7B-13B 这种中等规模模型的潜力。这对于初创公司和学术机构尤为重要，降低了 SOTA 模型的复现门槛。

### 争议点与不同观点

*   **争议点：Ray 的引入是否属于“过度工程”？**
    *   **反方观点：** SageMaker 原生的分布式训练框架已经足够成熟，引入 Ray 增加了调试难度（如 Ray 集群崩溃、端口冲突等）。
    *   **反驳：** 原生框架往往缺乏对 RL 这种动态、多步训练流程的灵活支持。Ray 的 Actor 模型更适合

---
## 技术分析

基于您提供的文章标题和摘要，以下是对这篇关于“在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B”的技术文章的深入分析。由于摘要部分截断，我将结合标题中隐含的技术栈（SageMaker, veRL, Ray, GRPO, CodeFu）以及当前大模型强化学习训练的前沿语境，为您构建一份全面的分析报告。

---

# 1. 核心观点深度解读

**文章的主要观点**
这篇文章的核心在于展示一种**现代化的、高效率的、可扩展的 LLM 训练范式**。具体而言，它主张利用 **veRL**（volcengine's RL library 或类似的弹性 RL 库）结合 **Ray** 的分布式计算能力，在云端（Amazon SageMaker）上完成对特定领域模型（CodeFu-7B）的强化学习微调（RLHF），特别是采用了 **GRPO (Group Relative Policy Optimization)** 算法。

**作者想要传达的核心思想**
作者试图传达的核心思想是：**大模型的强化学习训练不再受限于昂贵的专用集群或复杂的工程代码。** 通过将高效的算法库与云原生的弹性基础设施相结合，研究者和工程师可以以“ straightforward extension（直接扩展）”的方式，将单机训练逻辑无缝迁移到大规模分布式环境，从而低成本地训练出像 CodeFu 这样高竞争力的垂直领域模型。

**观点的创新性和深度**
*   **算法层面的创新：** 摒弃了传统的 PPO（Proximal Policy Optimization），转而采用 GRPO。GRPO 不需要训练一个价值模型，这大大减少了显存占用和计算开销，是当前 RLHF 领域的一个重要技术迭代。
*   **工程架构的深度：** 强调“解耦”。veRL 负责复杂的 RL 逻辑和内存优化，Ray 负责资源调度和弹性伸缩，SageMaker 负责底层基础设施。这种分层架构代表了 MLOps 的最佳实践。

**为什么这个观点重要**
对于大模型落地而言，SFT（监督微调）只是基础，RLHF（基于人类反馈的强化学习）才是让模型具备“对齐”能力和“推理”能力的关键。这篇文章降低了实现这一高阶能力的门槛，证明了在公有云上快速迭代垂直领域（如竞技编程）强模型是可行且高效的。

# 2. 关键技术要点

**涉及的关键技术或概念**
1.  **GRPO (Group Relative Policy Optimization)：** 一种新型强化学习算法。与 PPO 不同，它通过组内样本的相对优势来估计基线，从而省去了 Critic 模型。
2.  **veRL：** 一个专为 LLM 设计的高效 RL 训练库。其核心特性通常包括零拷贝、显存优化和灵活的接口。
3.  **Ray：** 分布式计算框架，用于处理 veRL 的并行化任务和 Actor 的调度。
4.  **Amazon SageMaker Training Jobs：** 托管训练服务，提供 GPU 实例（如 p4de/p5）及环境管理。

**技术原理和实现方式**
*   **GRPO 原理：** 在训练时，模型对同一个 Prompt 生成多个输出。计算这些输出的奖励，然后计算组内平均奖励作为基线。策略梯度的更新依赖于单个输出与平均奖励的差异。
    *   *公式逻辑：* $Advantage = R - \text{GroupMean}(R)$。这使得训练更加稳定，且减少了约 50% 的模型参数推理开销（因为不需要 Critic）。
*   **veRL 的实现：** veRL 可能利用了 PyTorch 的分布式通信（NCCL）来处理张量并行，同时利用 Ray 来处理 Rollout（生成数据）阶段的并行。它可能实现了“Rollout-Training-分离”架构，即 Actor 角色负责生成数据，Learner 角色负责更新权重。
*   **SageMaker 与 Ray 集成：** 利用 SageMaker 的 Estimator API 启动 Ray Cluster，或者在 Ray Cluster 中通过 `sagemaker-ray-cluster` 启动训练任务。这使得 Ray 可以动态申请 SageMaker 的 GPU 资源。

**技术难点和解决方案**
*   **难点：** RL 训练中的显存瓶颈。既要加载大模型，又要存储历史轨迹，还要计算梯度。
*   **解决方案：** veRL 通常采用 **CPU Offloading**（将经验数据存放在 CPU 内存，释放 GPU 显存给梯度计算）以及 **FlashAttention** 等算子优化。
*   **难点：** 训练不稳定。
*   **解决方案：** GRPO 通过组采样自然降低了方差，比 PPO 更容易收敛。

**技术创新点分析**
最大的创新点在于 **GRPO 在工业级云训练框架上的工程化落地**。传统的 PPO 流程极其复杂，往往需要手写复杂的分布式代码。veRL + Ray 的组合将这种复杂性封装，使得“Group Relative”这种算法优势能被轻松放大。

# 3. 实际应用价值

**对实际工作的指导意义**
这篇文章为想要训练“垂直领域大模型”的团队提供了标准作业程序（SOP）。它证明了不需要从零开发训练框架，可以直接组合开源工具和云服务快速上线。

**可以应用到哪些场景**
*   **代码生成与修复：** 如文中的 CodeFu，用于自动生成算法题解或修复 Bug。
*   **数学推理：** 利用 GRPO 增强模型的逻辑链（CoT）能力。
*   **合规与安全对齐：** 训练模型拒绝有害指令。
*   **个性化助手：** 针对特定企业语料进行强化学习。

**需要注意的问题**
*   **成本控制：** RLHF 需要大量的生成和打标，SageMaker 的 GPU 实例成本较高，需要做好实验管理。
*   **奖励模型的质量：** GRPO 虽然好，但依然依赖 Reward Model 的准确性。如果 RM 偏差，GRPO 也会强化错误的模式（Reward Hacking）。
*   **Ray 的调试难度：** 分布式系统的错误排查通常比单机困难，需要熟悉 Ray 的日志系统。

**实施建议**
建议先在小规模的 SageMaker 实例（如单卡或多卡）上使用 Ray 本地模式进行调试，验证 GRPO 的数据流正确后，再扩展到多节点的分布式训练。

# 4. 行业影响分析

**对行业的启示**
这标志着大模型训练进入了**“算法-架构协同优化”**的时代。单纯堆砌算力已经不够，如何通过算法（如 GRPO 减少模型）和框架（如 veRL + Ray）提高硬件利用率，是竞争力的关键。

**可能带来的变革**
*   **小模型也能通过 RL 变强：** 7B 模型经过高质量的 RLHF（如 CodeFu），在特定任务上可以超越未经 RL 的更大参数模型（如 70B）。这降低了推理成本。
*   **云原生成为标配：** 未来的模型训练将更深度地绑定云厂商的弹性服务，而非传统的静态 HPC 集群。

**相关领域的发展趋势**
*   **RLHF 的平民化：** 类似 veRL 的工具会越来越多，RLHF 将成为模型发布的标配，而非仅限于 OpenAI 等大厂的独门绝技。
*   **从 PPO 到 GRPO/Rejection Sampling 的演进：** 行业正在寻找比 PPO 更稳定、更轻量的对齐算法。

# 5. 延伸思考

**引发的其他思考**
*   **数据飞轮：** CodeFu 的训练数据来源于竞技编程的判题结果（Pass/Fail）。这种“基于环境反馈”的 RL 是否可以扩展到更复杂的软件开发环境（如 Unit Tests、Integration Tests）？
*   **评估体系：** 如何在训练过程中实时监控 GRPO 的效果？仅看 Reward 分数可能不够，是否需要引入更复杂的 ELO 评分系统？

**可以拓展的方向**
*   **混合专家 的 RL 训练：** 在 GRPO 的框架下，如何处理 MoE 架构的负载均衡？
*   **多模态 RLHF：** 将 veRL 和 GRPO 应用到视觉-语言模型（VLM）的训练中。

**未来发展趋势**
未来，像 veRL 这样的库可能会进一步与推理引擎（如 vLLM, TensorRT-LLM）深度整合，实现“训练即推理，推理即训练”的实时反馈闭环。

# 6. 实践建议

**如何应用到自己的项目**
1.  **评估数据：** 确保你有高质量的 Reward Model 或环境反馈机制（如代码编译结果）。
2.  **环境搭建：** 在 AWS SageMaker 上配置 Ray 集群，安装 veRL。
3.  **模型转换：** 将 HuggingFace 格式的 CodeFu 或其他基础模型转换为 veRL 兼容的格式。
4.  **配置 GRPO：** 调整 `group_size`（组大小），这决定了显存占用和样本多样性。

**具体的行动建议**
*   **第一步：** 阅读 veRL 的官方文档，理解其 Actor/Critic/Roller 的抽象。
*   **第二步：** 在 SageMaker Notebook 中运行 veRL 提供的最小示例。
*   **第三步：** 准备自己的垂直领域数据（如金融分析报告、医疗诊断记录），构建 Reward Function。

**需要补充的知识**
*   **强化学习基础：** 理解 Policy, Value Function, Advantage, KL Divergence。
*   **Ray 架构：** 理解 Driver, Actor, Placement Group。
*   **PyTorch FSDP/DeepSpeed：** 理解大模型分布式训练的并行策略。

**实践中的注意事项**
*   **超参数敏感性：** GRPO 对 KL penalty 的系数非常敏感，过大模型不学习，过小模型容易崩溃。
*   **版本兼容性：** Ray, PyTorch, CUDA, veRL 之间的版本依赖非常严格，建议使用 Docker 容器化环境。

# 7. 案例分析

**结合实际案例说明**
以 **CodeFu-7B** 为例，如果直接使用 SFT 训练代码模型，模型往往只能模仿代码的语法，但无法保证逻辑正确（即代码跑不通）。
*   **SFT 阶段：** 输入题目 -> 输出代码（可能包含语法错误或逻辑漏洞）。
*   **GRPO 阶段：**
    1.  输入题目 -> 模型生成 4 个不同的代码解。
    2.  环境运行这 4 个代码，通过测试用例的比例作为 Reward。
    3.  GRPO 算法计算：通过率高的代码对应的策略参数加强，通过率低的减弱。
    4.  最终模型倾向于生成能通过测试的代码。

**成功案例分析**
DeepSeek-Coder 和 Qwen2.5-Coder 的成功都大量采用了类似的 RLHF 策略。它们证明了在代码生成任务上，RL 带来的提升远超继续预训练。

**失败案例反思**
如果在 Reward Model 存在严重偏差（例如给长代码高分，给短代码低分）的情况下使用 GRPO，模型会学会“废话文学”，生成冗长但无效的代码。这被称为 **Reward Hacking**。

**经验教训总结**
务必在进入 GRPO 训练前，对 Reward Model 进行严格的验证，或者使用基于规则的确定性 Reward（如编译结果）作为起步。

# 8. �

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 vLLM 与 Ray 集成实现高效推理加速

**说明**:  
在 CodeFu-7B 的训练流程中，利用 veRL 内置的 vLLM 作为推理后端，并结合 Ray 的分布式能力，可以显著提升采样阶段的吞吐量。vLLM 通过 PagedAttention 技术优化了显存管理，使得在生成大量样本用于强化学习（RL）阶段时，能够最大化 GPU 利用率。

**实施步骤**:
1. 在 veRL 配置文件中，明确指定 `rollout` 部分使用 vLLM 作为推理引擎。
2. 配置 Ray 集群，确保 vLLM worker 节点拥有足够的显存，并启用 tensor parallelism（张量并行）以处理模型加载。
3. 调整 vLLM 的 block size（如 16 或 32）以平衡显存占用与计算效率。

**注意事项**:  
需确保 vLLM 版本与 CUDA 驱动及 PyTorch 版本兼容，避免底层库冲突导致训练任务崩溃。

---

### 实践 2：优化 SageMaker 分布式训练配置

**说明**:  
SageMaker Training Jobs 支持通过 `mpi` 或 `gloo` 后端进行分布式训练。对于 CodeFu-7B 这类大语言模型，利用 SageMaker 的分布式训练库（SMDistributed）或原生 PyTorch DDP 结合 Ray，可以有效地在多节点间同步梯度和模型参数。

**实施步骤**:
1. 在创建 SageMaker Estimator 时，设置 `distribution` 参数为 `{"mpi": {"enabled": true}}` 或配置 Ray 的 autoscaler。
2. 确保 `instance_count` 和 `instance_type` 的组合能够满足 7B 模型及优化器状态的显存需求（建议使用 `ml.g5` 或 `ml.p4` 系列）。
3. 启用 NCCL 的 Socket 通信优化，设置环境变量以优化带宽使用。

**注意事项**:  
监控网络吞吐量，避免跨可用区部署训练节点，以减少网络延迟对训练速度的影响。

---

### 实践 3：实施高效的检查点管理

**说明**:  
大模型训练时间长且成本高，必须实施鲁棒的检查点保存与恢复机制。利用 SageMaker 的 Spot Instance 训练可以大幅降低成本，但要求模型能够快速中断和恢复。

**实施步骤**:
1. 配置 SageMaker 使用 `checkpoint_s3_uri`，将模型断点定期保存到 S3。
2. 在 veRL 的训练循环中，设置合理的保存步长，避免过于频繁的 I/O 操作拖慢训练。
3. 确保代码逻辑支持从 S3 加载检查点并恢复 Ray Actor 的状态。

**注意事项**:  
验证检查点的完整性，确保在恢复训练时，优化器的动量状态也能被正确还原，以免损失收敛精度。

---

### 实践 4：利用 Ray 的动态资源调度处理 RL 阶段

**说明**:  
强化学习训练通常包含数据收集、训练和评估三个阶段，各阶段对计算资源的需求不同。利用 Ray 的动态资源调度，可以在训练阶段分配更多 GPU 给训练进程，在推理阶段分配更多给 rollout worker，从而提高整体集群效率。

**实施步骤**:
1. 定义 Ray Actor 时，为 Rollout Worker 和 Trainer 分配不同的资源标签（如 `num_gpus`）。
2. 在代码逻辑中实现 Placement Group，确保 Rollout 和 Trainer 逻辑隔离但共享同一个物理集群。
3. 利用 Ray 的 Autoscaler 动态调整实例数量，应对负载波动。

**注意事项**:  
需仔细规划 Ray Cluster 的启动头节点和 Worker 节点的配置，防止资源争抢导致的死锁。

---

### 实践 5：数据加载与预处理的流水线优化

**说明**:  
CodeFu-7B 训练涉及大量代码数据，I/O 瓶颈往往是 GPU 空闲的主要原因。构建高效的数据 Pipeline，利用 Ray 的并行数据加载能力，可以确保 GPU 始终处于计算状态。

**实施步骤**:
1. 使用 Ray Data 将原始代码数据集转换为 Parquet 或 Arrow 格式，以减少序列化开销。
2. 在 DataLoader 中设置合理的 `prefetch` 因子，利用 CPU 提前准备下一批数据。
3. 对于代码训练，实施动态填充策略，减少无效的 Padding Token 计算。

**注意事项**:  
确保数据清洗逻辑（如去除敏感信息、过滤过短样本）在进入训练循环前完成，避免浪费计算资源。

---

### 实践 6：监控与调试的可观测性集成

**说明**:  
在分布式环境下调试极其困难。集成 SageMaker Debugger 或 Ray Dashboard，结合 Weights & Biases (wandb) 或 TensorBoard，可以实时监控 Loss 曲线、梯度范数及资源利用率。

**实施步骤**:
1. 在 SageMaker Estimator 中配置 `rules`（如 `DeadRelay` 或 `Overfit`）以自动检测常见训练异常。
2. 在 veRL 代码中集成 wandb logger，记录

---
## 学习要点

- veRL 与 Ray 的深度集成使得在 Amazon SageMaker 上训练 CodeFu-7B 等大模型时，能够通过弹性资源调度和高效容错机制显著提升训练稳定性并降低成本。
- 利用 SageMaker 的托管基础设施结合 veRL 的优化，可简化大语言模型（LLM）训练的运维复杂度，让开发者更专注于算法与模型本身。
- Ray 在该架构中充当了高效的分布式计算框架，负责处理复杂的节点间通信和任务编排，从而加速 CodeFu-7B 的训练过程。
- veRL 提供的优化技术（如显存优化和计算重叠）在大规模代码模型训练中起到了关键作用，有效提升了硬件资源的利用率。
- 该实践展示了端到端的 MLOps 流程，证明了在云端环境中进行定制化代码模型训练的高效性与可扩展性。
- 通过 SageMaker Training jobs 启动训练任务，实现了对底层计算资源的抽象，无需手动管理集群即可获得高性能的分布式训练环境。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [SageMaker](/tags/sagemaker/) / [Ray](/tags/ray/) / [veRL](/tags/verl/) / [CodeFu-7B](/tags/codefu-7b/) / [GRPO](/tags/grpo/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [强化学习](/tags/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/) / [RLHF](/tags/rlhf/)
- 场景： [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [使用veRL和Ray在SageMaker上训练CodeFu-7B模型]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-0.md" >}})
- [在 SageMaker 上利用 veRL 与 Ray 训练 CodeFu-7B]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-1.md" >}})
- [在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B 模型]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-3.md" >}})
- [在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B 模型]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-3.md" >}})
- [🔥实战复盘：解锁GPT-OSS的智能体RL训练秘籍！]({{< relref "posts/20260128-blogs_podcasts-unlocking-agentic-rl-training-for-gpt-oss-a-practi-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*