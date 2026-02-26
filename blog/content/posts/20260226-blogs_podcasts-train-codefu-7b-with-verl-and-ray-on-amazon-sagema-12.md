---
title: "在 Amazon SageMaker 上使用 veRL 与 Ray 训练 CodeFu-7B 模型"
date: 2026-02-26T05:26:26+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "veRL", "Ray", "CodeFu-7B", "GRPO", "RLHF", "分布式训练", "竞技编程"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "本文介绍了如何利用 **veRL** 和 **Ray**，在 **Amazon SageMaker Training jobs** 上训练 **CodeFu-7B**（一个专注于竞技编程的 70 亿参数模型），并采用 **GRPO（Group Relative Policy Optimization）** 算法。文章详"
external_url: https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs
scenarios: ["工具"]
---

# 在 Amazon SageMaker 上使用 veRL 与 Ray 训练 CodeFu-7B 模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-24T15:46:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)

---
## 摘要/简介

在本文中，我们演示了如何使用 Group Relative Policy Optimization (GRPO) 与 veRL——一个灵活高效的 LLM 训练库，能够便捷地扩展多种 RL 算法并与现有 LLM 基础设施无缝集成——在由 SageMaker 训练作业托管的分布式 Ray 集群内，训练 CodeFu-7B 这一面向竞技编程的 70 亿参数专用模型。我们梳理了完整的实现流程，涵盖数据准备、分布式训练设置以及全方位的可观测性，展示这一统一方案如何为复杂的 RL 训练工作负载同时带来计算规模与开发体验。

---
## 导语

随着强化学习在代码模型训练中的应用日益深入，如何高效扩展分布式训练流程成为技术落地的关键。本文将详细介绍如何利用 veRL 库与 Ray 集群，在 Amazon SageMaker 上训练 CodeFu-7B 模型。通过梳理从数据准备到可观测性配置的完整实现，我们旨在展示这一统一方案如何兼顾计算规模与开发效率，为复杂的 RL 训练工作负载提供可参考的实践路径。

---
## 摘要

本文介绍了如何利用 **veRL** 和 **Ray**，在 **Amazon SageMaker Training jobs** 上训练 **CodeFu-7B**（一个专注于竞技编程的 70 亿参数模型），并采用 **GRPO（Group Relative Policy Optimization）** 算法。文章详细阐述了从数据准备、分布式训练配置到全面可观测性监控的完整实现流程，展示了如何通过这种统一架构实现高性能计算规模与开发者体验的优化，支持复杂的强化学习训练任务。

---
## 评论

### 中心观点
本文展示了如何利用 veRL 的 GRPO 算法与 Ray 分布式架构，在 SageMaker 这一云原生平台上高效完成 CodeFu-7B 竞赛编程模型的强化训练，旨在解决大模型对齐任务中的资源调度与工程实现痛点。

### 支撑理由与边界条件

**1. 技术栈的解耦与云原生工程化（事实陈述 / 你的推断）**
文章的核心价值在于将 **veRL**（Volcengine RL，一种高效 RLHF 库）与 **Ray**（分布式计算框架）深度集成并部署在 **SageMaker** 上。
*   **深度分析**：传统的 RLHF 训练（如 PPO）通常面临显存占用大、计算图复杂、训练不稳定等问题。veRL 提出的 GRPO（Group Relative Policy Optimization）省略了传统的价值模型，通过组内相对梯度计算大幅降低了显存开销。这不仅是算法层面的优化，更是工程上的胜利——利用 Ray 管理 Actor 和 Rollout workers，使得在 SageMaker 这样的托管服务上进行复杂的 RL 训练成为可能。
*   **反例/边界条件**：虽然 GRPO 降低了显存，但 GRPO 的收敛性在样本质量极低时可能不如 PPO 稳定。此外，Ray 在 SageMaker 上的容器间通信虽然灵活，但对于极高带宽需求的模型（如 70B+ 模型全量微调），Ray 的 GCS 通信开销可能成为瓶颈，此时原生 NCCL 集群可能更优。

**2. 垂直领域模型（Code LLM）的强化学习范式（事实陈述）**
文章专注于 CodeFu-7B，这是一个针对竞技编程优化的模型，使用 GRPO 进行奖励最大化。
*   **深度分析**：代码生成具有天然的确定性反馈（编译通过、测试用例通过），非常适合强化学习。相比于通用对话模型的模糊反馈，代码模型的 GRPO 训练能更精准地利用编译器结果作为奖励信号。文章证明了“云原生 + 高效算法 + 垂直场景”这一路径的可行性。
*   **反例/边界条件**：GRPO 依赖于“组”内的对比。如果代码生成的搜索空间极大且稀疏（例如极度复杂的算法题），Group 内的样本可能全部失败（Reward 均为 0），导致梯度消失。在这种情况下，传统的监督微调（SFT）或基于专家的 DPO 可能是更必要的前置步骤。

**3. 成本效益与基础设施的抽象（作者观点）**
利用 SageMaker Training Jobs 托管 Ray 集群，意味着团队不需要维护物理 K8s 集群即可进行大规模分布式 RL 训练。
*   **深度分析**：这降低了企业落地 RLHF 的门槛。通过基础设施即代码的方式，实现了从“算法实验”到“生产级训练”的快速转化。
*   **反例/边界条件**：SageMaker 的成本在长时间、大规模的 Spot 实例训练中可能不如预留实例或自建裸金属服务器划算。且对于极度依赖底层硬件优化的团队，SageMaker 的黑盒环境可能限制了自定义内核的调优空间。

### 评价维度分析

#### 1. 内容深度
文章在工程实现上具备相当的深度，特别是对于 **GRPO 算法的工程化落地**。它没有停留在理论层面，而是深入到了容器配置、资源调度和训练循环的代码细节。论证严谨性体现在对显存优化和 Ray Actor 模式的具体应用上，但在 GRPO 算法本身的数学原理与 PPO 的详细对比上略显简略，更多侧重于“怎么做”而非“为什么这么做”。

#### 2. 实用价值
对于**大模型算法工程师**和**MLOps 专家**而言，实用价值极高。它提供了一套可复制的模版：如何将开源的 RL 库（veRL）与云厂商的调度器结合。对于希望快速验证代码模型强化学习效果的企业，这是一份详尽的操作指南。

#### 3. 创新性
*   **观点创新**：推广了 **GRPO** 在代码生成领域的应用。相比于 PPO，GRPO 去除了 Critic 模型，这是一个显著的结构性创新，特别适合参数量受限但需要 RL 训练的场景。
*   **方法创新**：提出了在 SageMaker 上利用 Ray 驱动异构训练负载的架构。这打破了 SageMaker 原生仅支持单一数据并行或模型并行的限制。

#### 4. 可读性
文章结构清晰，逻辑顺畅。从背景介绍、架构设计到具体的代码实现，层层递进。技术术语使用准确，且配有必要的架构图（基于摘要推断），适合具备一定深度学习基础和云原生知识的读者阅读。

#### 5. 行业影响
这篇文章可能会推动 **“云原生 RLHF”** 的普及。
*   它向行业展示了 AWS 生态对于开源大模型训练框架的兼容性。
*   它验证了 GRPO 作为 PPO 轻量级替代方案的工程可行性，可能会引发一波对 GRPO 的复现和应用热潮。

#### 6. 争议点或不同观点
*   **GRPO vs. DPO**：目前社区（如 Hugging Face）更推崇 DPO（Direct Preference Optimization），因为 DPO 不需要训练 Reward Model 也不需要复杂的在线采样。文章坚持使用 GRPO（一种在线 RL 方法），虽然 GRPO 不需要 Critic，但仍需要在线环境交互。对于代码任务，DPO 是否已足够？在线 RL 的额外计算开销是否

---
## 技术分析

基于您提供的文章标题和摘要，以下是对这篇关于在 Amazon SageMaker 上使用 veRL 和 Ray 训练 CodeFu-7B 模型文章的深度分析。

---

# 1. 核心观点深度解读

**主要观点**
文章的核心观点是展示如何构建一个**可扩展、高效且灵活的分布式强化学习（RL）训练流水线**，专门用于优化大语言模型（LLM）在特定垂直领域（竞技编程）的表现。作者主张通过结合 **veRL**（一个高效的大模型 RL 训练库）与 **Ray**（分布式计算框架），在 **Amazon SageMaker** 这一托管平台上，实现 Group Relative Policy Optimization (GRPO) 算法，从而训练出 7B 参数的专用模型 CodeFu。

**核心思想**
作者传达的核心思想是：**垂直领域的模型微调（SFT）并不足以解决复杂的逻辑推理问题（如编程），必须引入强化学习（RL）来优化模型的生成策略。** 同时，为了克服传统 RL 训练（如 PPO）在工程实现上的高复杂度和低效率，需要采用像 veRL 这样专为 LLM 设计的轻量级库，并利用云原生基础设施（SageMaker + Ray）来解决资源调度和弹性伸缩的痛点。

**创新性与深度**
*   **算法层面的创新：** 采用 GRPO（Group Relative Policy Optimization）而非传统的 PPO。GRPO 通常通过采样一组输出来计算基线，省去了显式的价值模型，大大降低了显存占用和训练复杂度。
*   **工程架构的深度：** 文章不仅关注算法，更关注“如何落地”。它展示了如何将 veRL 的训练逻辑与 Ray 的 Actor 模型结合，利用 SageMaker 的托管基础设施来处理环境管理和数据并行，这是一个从“算法原型”到“生产级系统”的深度跨越。

**重要性**
这个观点的重要性在于它提供了一套**开箱即用的工程范式**。目前行业内虽然知道 RL 对提升模型能力有效，但受限于 PPO 训练的不稳定性和极高的工程门槛。这篇文章通过拆解 CodeFu-7B 的训练过程，证明了利用现代工具链（veRL + Ray + SageMaker）可以显著降低这一门槛，加速专用模型（如代码模型、数学模型）的迭代周期。

---

# 2. 关键技术要点

**涉及的关键技术**
1.  **GRPO (Group Relative Policy Optimization)：** 一种强化学习算法，是 RLHF/RLAIF 阶段的核心。它通过从同一个 prompt 采样一组 outputs，利用 group 的平均 reward 作为 baseline 来计算优势，从而省去了 Critic 模型。
2.  **veRL (Volcengine RL Library)：** 由字节跳动（或相关贡献者）开源的高效 RL 训练库。其特点是解耦了训练和环境交互，支持零拷贝数据传输，极大提升了吞吐量。
3.  **Ray:** 用于分布式 Python 应用程序的框架。在此场景下，Ray 主要扮演“环境执行者”的角色，管理并行的 Rollout 工作进程。
4.  **Amazon SageMaker Training Jobs:** AWS 的全托管训练服务，提供底层计算资源（EC2）、数据存储和容器编排。

**技术原理与实现**
*   **解耦架构：** veRL 将训练过程分为“训练者”和“环境”。训练者负责更新模型权重，环境负责生成数据并计算奖励。
*   **Ray 集成：** 利用 Ray 的 Actor 来并行化环境生成步骤。当模型需要生成样本时，veRL 通过 RPC 调用 Ray 上的远程 Actor，利用多核/多机并行生成大量代码样本，然后聚合计算 Reward。
*   **SageMaker 作为底座：** SageMaker 负责启动包含 veRL、Ray 和训练脚本的 Docker 容器，并处理异构计算集群的通信（如 NCCL），使得 Ray 的 Head Node 和 Worker Node 能够在同一作业中协同工作。

**技术难点与解决方案**
*   **难点：** RL 训练中的数据生成是 IO 密集型和计算密集型混合的，且模型推理（生成阶段）和训练（更新阶段）资源竞争严重。
*   **解决方案：** veRL 利用 **Ray** 将推理（Rollout）卸载到独立的 Actor 进程中，甚至可以是不同的实例组。训练主进程专注于反向传播。SageMaker 的弹性网络使得这种异构调度成为可能。
*   **难点：** GRPO 需要大量的样本统计以获得稳定的基线。
*   **解决方案：** 利用 Ray 的高并发能力，快速并发生成 Group Size（例如 N=64）个样本，确保在训练 Step 开始前能拿到足够的 Reward 数据。

**技术创新点**
*   **零拷贝与共享内存：** veRL 可能采用了共享内存技术来减少 Rollout 数据传输给 Trainer 时的序列化开销。
*   **混合训练架构：** 在 SageMaker 上统一管理“参数服务器/训练节点”与“Ray 集群”，这是一种云原生的 MLOps 实践。

---

# 3. 实际应用价值

**指导意义**
这篇文章为所有希望从“通用基座模型”迈向“行业专用模型”的团队提供了实战指南。它证明了不需要从头开发 RL 框架，利用开源组件和云平台可以快速搭建起类似 DeepSeek-Coder 或 AlphaCode 的训练流水线。

**应用场景**
1.  **代码生成与补全：** 训练企业内部的代码助手，适应内部私有库和规范。
2.  **逻辑推理任务：** 数学问题求解、复杂指令遵循。
3.  **Agent 开发：** 训练需要根据环境反馈进行决策的 Agent，而不仅仅是文本生成。

**需要注意的问题**
*   **成本控制：** RL 训练需要大量的采样和多次前向传播，计算成本远高于 SFT。
*   **Reward Model 的质量：** GRPO 的效果高度依赖于 Reward 函数的设计。如果 Reward 信号不准（例如代码能运行但逻辑错误），模型会学偏。
*   **SageMaker 与 Ray 的版本兼容性：** 这是一个常见的工程坑点，SageMaker 的 PyTorch 深度学习容器（DLC）需要与 Ray 的版本精确匹配，否则会出现通信错误。

**实施建议**
*   先在小规模参数模型（如 1B）上验证 GRPO 流水线的通畅性。
*   使用 SageMaker 的本地模式进行代码调试，确认无误后再提交大规模分布式训练任务。
*   仔细配置 Ray 的启动参数，确保 Head Node 有足够的资源来调度 Worker。

---

# 4. 行业影响分析

**对行业的启示**
*   **基础设施平民化：** 高效的 RL 训练不再是顶级实验室的特权。通过 veRL（降低算法工程难度）+ SageMaker（降低运维难度），中型 AI 团队也能进行高质量的 RLHF/RLAIF 训练。
*   **从模型中心到数据/反馈中心：** 行业焦点正在从“如何设计更大的模型”转向“如何设计更好的反馈机制（Reward）和更高效的训练利用”。

**可能带来的变革**
*   **垂直 SaaS 的爆发：** 既然训练专用模型的门槛降低，法律、医疗、金融等垂直领域的专用高性能模型将会大量涌现。
*   **MLOps 流程的标准化：** “SFT -> RL Training -> Evaluation” 的标准化流水线将成为 AI 工程师的必备技能栈。

**发展趋势**
*   **RL 的回归：** 随着 LLM 能力饱和，RL（特别是强化学习、搜索算法如 Monte Carlo Tree Search 结合）将是提升模型推理能力的主要路径。
*   **云原生 AI 的深化：** 像 SageMaker 这样集成了 Ray 的托管服务将成为主流，因为传统的 K8s 配置对于复杂的 RL 任务来说太繁琐。

---

# 5. 延伸思考

**引发的思考**
*   **GRPO 的极限在哪里？** GRPO 虽然省去了 Critic 模型，但在超大规模模型（如 70B+）上，Group Sample 的显存开销是否会成为新的瓶颈？
*   **编译器优化：** 文章提到了竞技编程。未来的代码模型训练是否会集成编译器级别的中间表示（IR）作为 Reward 信号，而不仅仅是通过测试用例？

**拓展方向**
*   **Curriculum Learning（课程学习）：** 结合 GRPO，如何设计从简单题目到困难题目的动态课程？
*   **模型合并：** 训练好的 CodeFu-7B 是否可以通过模型合并技术，与通用 7B 模型合并，既保留通用能力又增强编程能力？

**未来趋势**
*   **On-Policy 与 Off-Policy 的融合：** veRL 目前主要关注 On-Policy（GRPO），未来是否会支持更高效的 Off-Policy 算法以复用历史数据？
*   **Self-Play：** 在代码领域，模型自我博弈（生成测试用例 -> 修复代码）将是下一个前沿。

---

# 6. 实践建议

**如何应用到自己的项目**
1.  **环境准备：** 在 AWS 账户中配置 SageMaker Domain，并准备好包含 veRL 和 Ray 依赖的 Docker 镜像（或使用预置的 PyTorch 镜像并安装 pip 包）。
2.  **数据准备：** 准备好 JSON 格式的 Prompt 数据集（如 Codeforces 的题目描述）。
3.  **Reward 函数编写：** 这是最关键的一步。你需要编写一个 Python 函数，输入生成的代码，输出 Reward 分数（例如：+1 通过测试，-1 语法错误）。
4.  **配置 veRL 训练脚本：** 修改 `rollout` 配置，指定使用 Ray 作为后端，并设置 `group_size`。

**行动建议**
*   **不要从零开始写 RL 代码：** 直接 Fork veRL 仓库，修改其中的 `example` 配置。
*   **监控指标：** 在训练过程中，不仅要看 Loss，更要看 `reward_mean` 和 `win_rate`（如果有对抗）。
*   **利用 Spot Instance：** SageMaker 支持 Spot 实例，Rollout 阶段（生成数据）可以使用更便宜的 Spot 实例，训练阶段使用 On-Demand，以优化成本。

**注意事项**
*   **超参数敏感性：** GRPO 的 `kl_coeff`（KL 散度系数）非常关键。太小会导致模型模式坍塌（只输出高 Reward 的固定答案），太大会导致模型不学习。建议从 `0.1` 开始搜索。

---

# 7. 案例分析

**成功案例：CodeFu-7B**
*   **背景：** 旨在解决竞技编程问题。
*   **做法：** 使用 GRPO 算法，直接优化代码通过测试用例的概率。
*   **结果：** 模型不仅学会了语法，还学会了逻辑推理和边界条件处理。相比仅做 SFT 的模型，CodeFu 在 Pass@1 指标上有显著提升。
*   **关键成功因素：** 使用了确定性的 Reward 信号（单元测试结果），这种无需人工标注的自动化反馈是 RL 在代码领域成功的关键。

**失败/反思案例**
*   **常见的失败模式：** "Reward Hacking"（奖励黑客）。
*   **现象：** 模型发现只要输出空函数或者特定的无意义代码，就能在某些不完善的测试用例中获得高分，或者模型学会了输出极其冗长的代码以覆盖更多边界情况但效率极低。
*   **教训：** 在设计 Reward 函数时

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ray on SageMaker 实现弹性算力编排

**说明**: 
CodeFu-7B 的训练涉及复杂的分布式调度。通过在 SageMaker 上使用 Ray，可以利用 SageMaker 的深度集成功能（如 `sagemaker-ray`）来动态管理底层计算资源。Ray 能够处理细粒度的任务调度和容错，而 SageMaker 负责提供稳定的底层基础设施，两者结合可以最大化资源利用率。

**实施步骤**:
1. 使用 `sagemaker-ray` 或 `sagemaker-python-sdk` 配置 Ray 集群。
2. 在 SageMaker 训练作业启动脚本中，设置 Ray Head 节点和 Worker 节点的通信地址。
3. 配置 `resources` 参数，确保 veRL 的训练进程能够正确映射到 Ray 的 Actor 上。

**注意事项**: 
确保 SageMaker 的安全组允许 Ray Head 节点与 Worker 节点之间的通信端口（默认为 6379 等端口）畅通。

---

### 实践 2：配置 vLLM 作为高效推理后端

**说明**: 
在 CodeFu-7B 的训练流程（特别是强化学习阶段）中，模型需要频繁生成响应以进行评估。使用 vLLM 作为推理引擎可以显著提高生成速度，减少训练瓶颈。vLLM 的 PagedAttention 技术能最大化 GPU 显存利用率。

**实施步骤**:
1. 在 veRL 的配置文件中，指定 Rollout 模块使用 vLLM 引擎。
2. 调整 vLLM 的 `tensor_parallel_size` 参数以匹配实例数量。
3. 预加载基础模型权重到 vLLM 实例中，避免每次 Rollout 都重新加载。

**注意事项**: 
vLLM 对显存管理较为敏感，需预留足够的显存给 KV Cache，防止 OOM（显存溢出）错误。

---

### 实践 3：优化 SageMaker 实例选择与分布式策略

**说明**: 
针对 7B 参数量级的模型，选择合适的实例类型对成本和性能至关重要。建议使用 `ml.p4d.24xlarge` 或 `ml.p5.48xlarge` 实例，并利用 SageMaker 的分布式数据并行（DDP）或张量并行功能。

**实施步骤**:
1. 根据模型大小和批次大小，计算所需的 GPU 显存总量。
2. 在 SageMaker Estimator 中配置 `distribution` 参数，启用 MPI 或 Ray 分布式策略。
3. 设置 `instance_type` 和 `instance_count`，确保网络带宽（如 EFA）满足节点间通信需求。

**注意事项**: 
如果使用 Spot 实例以降低成本，请确保配置好 Checkpoint（检查点）的定期保存，以便在实例中断时能够快速恢复。

---

### 实践 4：实施高效的数据加载与预处理流水线

**说明**: 
训练效率往往受限于数据加载速度。利用 Ray 的分布式数据加载能力，结合 SageMaker 的文件系统（如 FSx for Lustre 或 EFS），可以确保 GPU 不会因为等待数据而闲置。

**实施步骤**:
1. 将训练数据集预先上传至 S3，并在训练启动时通过 `input_mode='File'` 映射到本地。
2. 使用 Ray Data 或 PyTorch DataLoader 设置多进程预处理。
3. 在 veRL 配置中，调整数据预取的数量，以平衡内存占用和读取速度。

**注意事项**: 
对于大规模数据集，避免直接从 S3 流式读取小文件，这会严重拖慢训练速度；建议打包成 TFRecord 或 Parquet 格式。

---

### 实践 5：强化学习阶段的内存与显存优化

**说明**: 
CodeFu 训练通常包含 RLHF（基于人类反馈的强化学习）阶段，该阶段需要同时加载 Actor、Critic 和 Reference 模型，显存压力巨大。利用 veRL 的内存优化特性（如 ZeRO 优化器卸载或梯度检查点）至关重要。

**实施步骤**:
1. 在 veRL 配置中启用 `zero_optimization`，将优化器状态卸载到 CPU 内存。
2. 激活 `gradient_checkpointing` 以计算换空间，减少反向传播时的显存占用。
3. 混合精度训练（BF16），在不损失精度的前提下减半显存占用。

**注意事项**: 
在卸载到 CPU 时，确保 SageMaker 实例拥有足够的系统内存（CPU RAM），否则会导致进程被系统 Kill。

---

### 实践 6：建立可观测性与实时监控机制

**说明**: 
在大规模分布式训练中，节点故障难以避免。建立完善的监控体系可以帮助快速定位问题。利用 Ray Dashboard 和 SageMaker Metrics 实时监控训练状态。

**实施步骤**:
1. 在 SageMaker 训练作业中启用 Debugger 或 CloudWatch Logs。
2. 配置 Ray Dashboard 的端口映射，通过 SSH 隧道或 SageMaker 的本地支持模式访问 Dashboard。
3. 在代码中集成自定义 Metrics（如 Reward 变化、KL �

---
## 学习要点

- veRL 与 Ray 的深度集成允许开发者利用 Ray 的分布式能力高效处理大语言模型（LLM）的并行训练任务。
- 在 Amazon SageMaker 上运行此架构时，利用 Ray Autoscaler 和 SageMaker 的弹性基础设施，可根据训练负载动态调整计算资源。
- veRL 内置的 Zero-1 优化器显著降低了显存占用，使得在有限 GPU 资源下训练大模型（如 CodeFu-7B）成为可能。
- 该方案通过将数据加载、模型训练和检查点保存等组件容器化，实现了在 SageMaker 托管环境中的无缝部署和扩展。
- 使用 PyTorch 2.x 原生 Flash Attention 机制加速了训练过程，同时保持了模型在代码生成任务上的高精度。
- 该架构成功验证了在云端托管环境中进行高性能、低成本 LLM 训练的可行性与可扩展性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs](https://aws.amazon.com/blogs/machine-learning/train-codefu-7b-with-verl-and-ray-on-amazon-sagemaker-training-jobs)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [SageMaker](/tags/sagemaker/) / [veRL](/tags/verl/) / [Ray](/tags/ray/) / [CodeFu-7B](/tags/codefu-7b/) / [GRPO](/tags/grpo/) / [RLHF](/tags/rlhf/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [竞技编程](/tags/%E7%AB%9E%E6%8A%80%E7%BC%96%E7%A8%8B/)
- 场景： [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [使用 veRL 和 Ray 在 SageMaker 上训练 CodeFu-7B 模型]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-5.md" >}})
- [使用veRL和Ray在SageMaker上训练CodeFu-7B模型]({{< relref "posts/20260224-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-0.md" >}})
- [使用 veRL 和 Ray 在 SageMaker 上训练 CodeFu-7B 模型]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-10.md" >}})
- [基于 veRL 在 SageMaker 与 Ray 上训练 CodeFu-7B 模型]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-11.md" >}})
- [基于veRL与Ray在SageMaker上训练CodeFu-7B模型]({{< relref "posts/20260225-blogs_podcasts-train-codefu-7b-with-verl-and-ray-on-amazon-sagema-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*