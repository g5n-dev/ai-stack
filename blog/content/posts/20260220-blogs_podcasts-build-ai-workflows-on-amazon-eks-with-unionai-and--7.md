---
title: "使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流"
date: 2026-02-20T19:03:21+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何使用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建、编排和扩展 AI/ML 工作流。 主要内容总结如下： 1. **核心工具**： * **Flyte Python SDK**：用于编写工作流代码，实现对 AI/ML 流程的编排。 * **Union.ai 2"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们说明如何使用 Flyte Python SDK 编排并扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来深入探讨该解决方案。

---
## 导语

在 Amazon EKS 上构建可扩展的 AI 工作流是企业级机器学习落地的重要环节。本文将详细介绍如何利用 Union.ai 和 Flyte 编排复杂任务，并实现与 Amazon S3、Aurora 等 AWS 服务的原生集成。通过解析具体的 AI 工作流示例，读者将掌握在 Kubernetes 环境中高效部署与管理 AI 流程的实践方法。

---
## 摘要

本文介绍了如何使用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建、编排和扩展 AI/ML 工作流。

主要内容总结如下：

1.  **核心工具**：
    *   **Flyte Python SDK**：用于编写工作流代码，实现对 AI/ML 流程的编排。
    *   **Union.ai 2.0**：该系统支持将 Flyte 部署在 **Amazon EKS**（弹性 Kubernetes 服务）上，从而利用 Kubernetes 的强大扩展能力。

2.  **AWS 服务集成**：
    该解决方案能与 AWS 生态无缝集成，主要涉及以下服务：
    *   **Amazon S3**：用于存储工作流中的数据和模型。
    *   **Amazon Aurora**：提供数据库支持。
    *   **AWS IAM**：管理身份与访问权限。
    *   **Amazon CloudWatch**：用于监控和日志记录。

3.  **应用示例**：
    文章通过一个具体的 AI 工作流示例，演示了如何利用 **Amazon S3 Vectors** 服务来实现该解决方案。

**总结**：通过结合 Union.ai、Flyte 和 Amazon EKS，开发者可以构建高性能、可扩展的 AI 工作流，并充分利用 AWS 的云服务基础设施。

---
## 评论

### 深度评价：基于 Amazon EKS 与 Union.ai 构建 AI 工作流

**文章中心观点：**
通过 Union.ai 2.0 将 Flyte 工作流引擎部署于 Amazon EKS，能够为数据科学和 AI 团队提供一个基于 Kubernetes 的、可扩展的、且能与 AWS 原生服务深度集成的标准化生产级平台，旨在解决从本地实验到云端部署的工程化鸿沟。

**支撑理由与深度分析：**

**1. 内容深度与严谨性：**
*   **理由：** 文章触及了当前 MLOps 领域的核心痛点——**环境异构性与资源编排**。Flyte 作为一个基于 Kubernetes 的开源工作流编排工具，其核心价值在于将数据、模型和计算任务（容器化）进行版本化管理。文章论证了利用 Union.ai（Flyte 的商业托管版）可以降低在 EKS 上部署和维护 Flyte 集群的复杂度，这是一个严谨的技术路径。
*   **你的推断：** 文章隐含了一个前提，即企业已经具备或愿意构建基于 Kubernetes 的基础设施。对于这类企业，将 AI 工作流 K8s 化是走向云原生的必经之路。
*   **事实陈述：** Flyte 确实提供了对 Python 的深度支持（Flytekit），并且能够原生处理 S3 上的数据传递。

**2. 实用价值与行业痛点：**
*   **理由：** 文章的实用价值在于提供了一个**“样板架构”**。对于许多试图摆脱“数据科学家的 Jupyter Notebook 无法上线”困境的团队，该方案提供了一个具体的实现路径：利用 EKS 的弹性扩缩容能力应对模型训练和推理的波峰，利用 S3 实现数据与计算的分离。
*   **作者观点：** 这种架构特别适合需要处理大规模数据处理（ETL）与模型训练串联的场景。相比于 Airflow 或 Prefect，Flyte 在处理大数据传递和分布式任务调度上具有原生优势，因为它诞生于 Lyft 和 Spotify，专为高吞吐量 ML 设计。

**3. 创新性与行业趋势：**
*   **理由：** 文章虽未提出全新的算法，但在**工程范式**上具有前瞻性。它强调了“工作流即代码”和“声明式基础设施”。Union.ai 2.0 作为一个控制平面，实际上是在推广一种**“多租户、多云”的 AI 治理理念**。它试图将 AI 工程从“脚本运行”提升到“微服务编排”的高度。
*   **你的推断：** 这种方案正在挑战传统的单体 AI 平台（如 SageMaker Studio 的全托管模式），给予用户更底层的控制权，同时保留了云原生生态的灵活性。

**反例与边界条件：**

1.  **运维复杂度的陷阱：**
    *   **反例：** 对于初创公司或缺乏专职 Kubernetes 运维工程师的团队，部署 EKS + Flyte + Union.ai 可能是**过度工程化**的灾难。
    *   **边界条件：** 如果团队规模较小（<5人），且任务主要是简单的定时推理，直接使用 AWS Step Functions 或完全托管的 SageMaker Pipelines 效率更高。K8s 的学习曲线极其陡峭，Flyte 虽然封装了部分逻辑，但排查 Pod 启动失败、CNI 网络配置等问题仍需深厚功底。

2.  **延迟与成本考量：**
    *   **反例：** 对于毫秒级要求的实时在线推理，EKS + Flyte 并非最佳选择。
    *   **边界条件：** Flyte 更适合批处理和离线训练/微调。如果业务逻辑是低延迟的在线请求，应直接使用 Sagemaker Endpoints 或 AWS Lambda。此外，EKS 节点的持续运行成本（即使是 EC2 Spot 实例）对于低频任务可能比 Serverless 工作流更昂贵。

**可验证的检查方式：**

1.  **性能指标测试：**
    *   在 EKS 上部署该架构，使用 `flytekit` 运行包含 1000 个并发任务的 Fan-in/Fan-out 工作流。
    *   **观察窗口：** 记录从任务提交到第一个 Pod 启动的延迟以及整体工作流的总耗时。对比使用 AWS Step Functions 或 Airflow on EC2 的资源利用率和启动速度。

2.  **集成性验证：**
    *   验证 Flyte 任务与 AWS S3、Glue、Redshift 的交互深度。
    *   **检查方式：** 尝试在 Flyte 任务失败时，是否能够自动且精细地清理 S3 上的中间数据（缓存管理），以及是否能够利用 IRSA（IAM Roles for Service Accounts）实现细粒度的 AWS 权限控制。

**实际应用建议：**

*   **不要盲目上马 K8s：** 除非你的团队有明确的计划需要自定义底层运行时环境（如特殊的 CUDA 驱动、依赖冲突极其严重的多语言环境），否则不要为了用 K8s 而用 K8s。SageMaker 的全托管服务在 80% 的常规场景下更省心。
*   **关注冷启动：** 在 EKS 上使用 Flyte 时，务必配置好 Cluster Autoscaler 和 Karpenter。对于短任务，要注意 Pod 冷启动带来的时间损耗，可能需要配合 Node Template 或热池策略。
*   **利用 Union 的多租户特性：** 如果采用 Union.ai 的 SaaS 或自托管版，重点利用其“项目”

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 1. 核心观点深度解读

**文章的主要观点：**
文章主张在构建和扩展生产级 AI/ML 工作流时，不应仅依赖单一的平台或手工脚本，而应采用**基于 Kubernetes 的声明式工作流编排系统**。具体而言，通过在 **Amazon EKS** 上部署 **Union.ai（Flyte 的商业托管版）**，利用 **Flyte Python SDK**，可以实现高性能、可扩展且与 AWS 云原生生态深度集成的机器学习流水线。

**作者想要传达的核心思想：**
AI 工作流不仅仅是运行代码，更是**数据、计算和模型的工程化调度**。核心思想在于“**编排**”与“**基础设施解耦**”。
1.  **编排的标准化**：将 ML 生命周期中的数据预处理、训练、微调、评估和部署等步骤，抽象为可复用、可组合的任务。
2.  **云原生的弹性**：利用 EKS 的容器编排能力，解决 ML 工作负载（特别是分布式训练）对算力的弹性需求。
3.  **无缝集成**：ML 工程不应是孤岛，必须与 S3 等存储服务和 IAM 等安全服务原生打通。

**观点的创新性和深度：**
*   **从“脚本”到“工作流即代码”**：Flyte 强调使用 Python SDK 定义工作流，这使得数据科学家无需学习复杂的 YAML 或特定领域的 DSL，即可利用 Python 的原生能力构建复杂的 DAG（有向无环图）。
*   **Union Serverless 架构**：Union.ai 2.0 引入了一种新的架构，允许 Flyte 控制平面与计算平面解耦。这意味着用户可以在自己的 AWS 账户（EKS）中运行计算任务，数据不离开用户的控制边界，同时享受 Union.ai 托管的控制平面服务。

**为什么这个观点重要：**
随着大模型（LLM）和复杂 ML 模型的普及，单机训练已无法满足需求。企业面临的主要痛点从“如何写模型”转变为“如何可靠、大规模地运行模型”。该方案提供了一条将实验性代码转化为生产级系统的标准化路径，降低了 MLOps 的准入门槛和运维成本。

---

# 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Flyte**：一个开源的工作流编排平台，专为 ML 和数据编排设计。
*   **Union.ai**：Flyte 的商业创建者，提供 Union Serverless（托管控制平面）和 Union Cloud。
*   **Amazon EKS (Elastic Kubernetes Service)**：AWS 托管的 Kubernetes 服务。
*   **Flyte Python SDK**：用于定义任务和工作流的 Python 库。
*   **AWS S3 (Simple Storage Service)**：用于存储数据集、模型和中间产物。

**技术原理和实现方式：**
1.  **工作流定义**：用户使用 Python 装饰器（如 `@task` 和 `@workflow`）编写代码。Flyte 编译器将这些代码编译成中间表示（IR），并在 Flyte 后端注册。
2.  **容器化与调度**：当工作流被触发时，Flyte Propeller（EKS 中的核心组件）会根据工作流定义，在 EKS 集群上创建 Pod 来执行各个任务。
3.  **数据传递**：Flyte 自动处理任务间的数据传递。对于大型文件，它利用 S3 进行中转；任务 A 将输出上传至 S3，任务 B 从 S3 下载输入，从而避免 Pod 之间直接传输大数据的压力。
4.  **弹性伸缩**：结合 EKS 的 Cluster Autoscaler 和 Karpenter，Flyte 可以根据任务队列的长度和资源需求，动态调整节点数量。

**技术难点和解决方案：**
*   **难点：异构计算支持**。ML 任务可能需要 CPU（数据处理）、GPU（训练）或高内存（推理）。
    *   **解决方案**：Flyte 允许在任务级别指定资源请求（如 `limits=mem="10Gi", gpu="1"`）。EKS 会根据这些请求调度到合适的节点池。
*   **难点：状态管理与容错**。长时间运行的训练任务可能因节点故障而中断。
    *   **解决方案**：Flyte 原生支持重试、检查点和断点续传。如果节点失败，Flyte 会自动在另一个节点上重新启动任务。

**技术创新点分析：**
*   **Type-Safe 工作流**：Flyte 强类型系统确保了数据流在编译期就能被检查，减少了运行时错误。
*   **Execution Abstraction**：代码在本地运行和在云端运行是完全一致的，这种“本地即云端”的体验极大地加速了迭代。

---

# 3. 实际应用价值

**对实际工作的指导意义：**
该架构为数据科学和工程团队提供了一个统一的平台。它消除了“我在本地能跑，但在云端跑不通”的常见问题，并建立了一个标准化的模型注册表和任务仓库。

**可以应用到哪些场景：**
1.  **大模型微调**：周期性地从 S3 读取数据，启动分布式 GPU 训练，评估模型，并将模型回写 S3。
2.  **批预测**：每天定时处理海量数据，生成预测结果。
3.  **特征工程**：ETL 流水线，清洗原始数据并生成特征。

**需要注意的问题：**
*   **冷启动时间**：每次任务启动都需要拉取容器镜像，对于毫秒级任务，这可能开销过大。Flyte 适合分钟级或更长周期的任务。
*   **成本控制**：在 EKS 上运行需要精心配置节点自动伸缩，否则闲置节点会产生高昂费用。

**实施建议：**
*   从简单的 ETL 工作流开始，逐步迁移核心训练逻辑。
*   利用 Flyte 的缓存机制，对于相同输入的任务直接返回缓存结果，节省计算成本。

---

# 4. 行业影响分析

**对行业的启示：**
这标志着 **MLOps 正在从“工具链组合”向“原生平台化”演进**。过去企业需要自己拼凑 Airflow + Kubernetes + MLflow，现在像 Flyte + Union.ai 这样的融合平台提供了开箱即用的体验。

**可能带来的变革：**
*   **降低云原生门槛**：数据科学家不需要成为 Kubernetes 专家就能利用 K8s 的强大能力。
*   **加速 AI 落地**：标准化的流程使得 AI 模型从实验室到生产环境的周期大幅缩短。

**相关领域的发展趋势：**
*   **Serverless MLOps**：计算与控制平面分离，用户只为实际计算时间付费，无需维护复杂的控制平面集群。
*   **多云/混合云支持**：基于 K8s 的标准使得工作流可以在 AWS、Azure 或私有云之间无缝迁移。

---

# 5. 延伸思考

**引发的其他思考：**
随着模型越来越大，数据传输可能成为瓶颈。未来的工作流引擎是否应该支持更智能的数据感知调度，即“计算向数据移动”而非传统的“数据向计算移动”？

**可以拓展的方向：**
*   **与 Ray 集成**：Flyte 与 Ray 的结合是目前的热点，用于处理更复杂的分布式强化学习或超参数调优。
*   **LLM 特定编排**：如何利用 Flyte 编排 Agent 工作流（如 LangChain 应用），这需要更好的状态管理和流式处理支持。

**未来发展趋势：**
工作流引擎将逐渐具备“推理”能力，即不仅仅是执行预定义的步骤，还能根据中间结果动态调整下一步的执行计划。

---

# 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现有痛点**：如果团队正面临脚本管理混乱、资源利用率低、模型复现难等问题，引入 Flyte 是合适的。
2.  **环境准备**：在 AWS 上建立 EKS 集群，配置好 IAM Role for Service Accounts (IRSA)，确保 Pod 可以直接访问 S3 而无需硬编码密钥。

**具体的行动建议：**
*   **第一步**：安装 `flytekit`，在本地编写一个简单的 `@task` 和 `@workflow`。
*   **第二步**：使用 `flytectl` 将工作流部署到 demo 集群或 Union Cloud 免费层。
*   **第三步**：构建自定义容器镜像，将项目依赖打包，并在 Flyte 中注册。

**需要补充的知识：**
*   **Docker/Container**：理解镜像构建和优化。
*   **Kubernetes 基础**：理解 Pod, Node, Namespace, Resource Quota。
*   **Python 类型提示**：Flyte 强依赖 Python 类型。

**实践中的注意事项：**
*   避免在 `@task` 中执行非常轻量级的操作（如加法运算），因为容器调度的开销远大于计算本身。应尽量合并任务。
*   注意 S3 的数据一致性，确保任务写入的数据对下游任务是可见的。

---

# 7. 案例分析

**结合实际案例说明：**
某金融科技公司利用该架构构建信用评分模型。
*   **过去**：使用 Airflow on EC2，每次运行需手动维护 Python 环境，GPU 训练任务需单独启动，难以并行。
*   **现在**：使用 Flyte on EKS。
    *   **数据预处理**：在 CPU 节点上并行处理数百万条交易记录。
    *   **训练**：任务自动调度到 p3.2xlarge (GPU) 节点。
    *   **评估**：训练结束后自动触发评估任务。

**成功案例分析：**
Spotify 是 Flyte 的早期采用者和主要贡献者。他们利用 Flyte 管理其庞大的推荐系统训练流水线，实现了每天数万个任务的调度，极大地提高了数据科学家的工作效率，使他们无需关心底层基础设施。

**失败案例反思：**
一些团队试图将微服务架构也放入 Flyte 中管理。这是一个反模式。Flyte 适合批处理和有向无环图任务，不适合长时间运行的无状态 HTTP 服务（这应由标准 Deployment 处理）。混淆两者会导致资源浪费和架构混乱。

**经验教训总结：**
*   **边界清晰**：Flyte 负责“跑完即止”的作业，K8s Deployment 负责“常驻”的服务。
*   **依赖管理**：不要在 Flyte 任务中动态 `pip install` 库，这会导致极慢的启动速度。必须预构建镜像。

---

# 8. 哲学与逻辑：论证地图

**中心命题:**
在构建现代 AI/ML 工作流时，采用 **"基于 Amazon EKS 的 Flyte + Union.ai"** 架构，相比于传统脚本或单一云服务，能提供更优的**可扩展性**、**可移植性**和**工程效率**。

**支撑理由:**
1.  **资源弹性与异构计算支持:**
    *   *依据:* EKS 提供了底层容器编排能力，Flyte 能够基于任务类型（CPU/GPU/高内存）动态调度资源，解决了静态资源分配浪费和异构任务难以调度的问题。
2.  **工作流即代码:**
    *   *依据:* Flyte Python SDK 允许使用原生 Python 构建工作流，利用了类型安全和模块化，使得代码版本控制、单元测试和复用

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建容器化的模块化工作流

**说明**:
利用 Union.ai 和 Flyte 的核心能力，将 AI/ML 工作流拆解为独立、可复用的任务（容器）。每个任务应包含特定的逻辑（如数据预处理、模型训练或评估），并打包为容器镜像。这种模块化设计提高了代码的可维护性和复用性，同时利用 EKS 的弹性进行高效调度。

**实施步骤**:
1. 定义工作流逻辑，将其分解为独立的函数或脚本。
2. 为每个任务编写 Dockerfile，并构建包含所需依赖项（如 PyTorch, TensorFlow, Scikit-learn）的容器镜像。
3. 将镜像推送到 Amazon ECR（弹性容器注册表）。
4. 在 Flyte 代码中注册这些任务，并使用 `@task` 和 `@workflow` 装饰器定义依赖关系。

**注意事项**:
- 确保容器镜像尽可能小（使用多阶段构建），以加快 EKS 上的 Pod 启动速度。
- 在 Dockerfile 中明确指定基础镜像的版本标签，避免使用 `latest`，以确保构建的可重现性。

---

### 实践 2：优化 EKS 节点配置与 Spot 实例使用

**说明**:
AI 工作流通常包含计算密集型任务（如训练）和 I/O 密集型任务（如数据转换）。在 EKS 上，应针对不同类型的任务配置不同的节点组。特别是对于容错性较好的开发、测试或训练任务，应积极利用 Amazon EC2 Spot 实例，以显著降低计算成本。

**实施步骤**:
1. 在 EKS 集群中创建专用的节点组，例如配置 GPU 实例组用于训练，配置 CPU 实例组用于数据处理。
2. 启用托管节点组，并混合使用 On-Demand 和 Spot 实例。
3. 在 Flyte 任务定义中，通过修改任务模板或使用 Flyte 的资源需求配置，指定特定任务应调度到具有特定标签（如 GPU）的节点上。

**注意事项**:
- 使用 Spot 实例时，必须确保工作流支持检查点和恢复机制，以防实例中断。
- 合理配置 Pod 的资源请求和限制，以配合 Kubernetes Cluster Autoscaler 自动扩展节点。

---

### 实践 3：实施动态资源分配与自动扩缩容

**说明**:
AI 工作流的资源需求波动很大。Flyte 与 EKS 的集成允许根据任务的实际需求动态分配资源。应配置 Cluster Autoscaler 以处理 Pod 的Pending状态，同时利用 Flyte 的原生能力在任务完成后自动释放资源，避免资源闲置浪费。

**实施步骤**:
1. 在 EKS 上安装并配置 Cluster Autoscaler，使其能够根据 Pod 的资源请求自动增加或减少节点数量。
2. 在 Flyte 任务定义中，明确指定 `requests`（保证的最小资源）和 `limits`（最大可用资源）。
3. 对于分布式训练任务，利用 Flyte 的 MPI 运算符支持，动态请求多个 GPU 或节点协同工作。

**注意事项**:
- 监控集群的扩缩容事件，确保扩容速度能满足工作流的启动时间要求。
- 避免设置过高的 `requests`，这可能导致资源碎片化，使 Pod 无法调度。

---

### 实践 4：建立高性能数据存储与缓存策略

**说明**:
在 EKS 上运行 AI 工作流时，I/O 性能往往是瓶颈。直接从 S3 读取海量数据集可能导致速度缓慢。最佳实践包括使用 Amazon FSx for Lustre 创建高性能文件系统，或利用 EBS CSI Driver 提供持久化存储，并结合 S3 生命周期策略管理数据。

**实施步骤**:
1. 创建 Amazon FSx for Lustre 文件系统，并将其与 S3 存储桶关联，用于高频读取训练数据。
2. 配置 EBS 存储类，为需要持久化的中间结果提供高性能卷（如 io2 或 gp3）。
3. 在 Flyte 任务中，通过动态挂载（Dynamic Pod Overwrites）或持久卷声明（PVC）将高性能存储挂载到容器中。

**注意事项**:
- 确保存储卷的吞吐量与计算节点的处理能力相匹配，避免存储成为瓶颈。
- 在任务完成后清理临时数据，防止存储成本失控。

---

### 实践 5：集中式日志记录与可观测性集成

**说明**:
为了调试复杂的 AI 工作流和监控 EKS 集群健康状况，必须建立统一的可观测性平台。将 Flyte 的用户级日志与 EKS 的系统级日志（通过 CloudWatch）以及指标（通过 Prometheus/Grafana）整合起来，以便快速定位故障。

**实施步骤**:
1. 部署 Amazon CloudWatch Container Insights 或使用 AWS for Fluent Bit DaemonSet 来收集 EKS 的标准输出日志和指标。
2. 在 Flyte 配置中，确保任务日志被正确捕获并转发到 CloudWatch Logs。
3. 集成 Prometheus 和 Grafana（可

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、可维护且生产就绪的 AI 工作流，实现机器学习生命周期的自动化管理。
- 利用 Amazon EKS 的托管 Kubernetes 服务，可以为 AI 工作流提供强大的容器编排能力，从而高效处理大规模计算资源和异构硬件（如 GPU）。
- Flyte 的数据感知型工作流引擎具备容错和重试机制，能够确保长时间运行的 AI 训练任务和复杂的数据处理管道的稳定性。
- 该架构支持将模型开发与部署无缝集成，通过统一的工作流定义实现从数据处理、模型训练到推理服务的端到端自动化。
- 借助 Union.ai 的平台能力，团队可以在云端轻松协作、复用工作流组件，并利用 Union Server 集中管理和调度跨多个云环境的任务。
- 这种云原生解决方案通过容器化和微服务架构，显著提高了 AI 基础设施的资源利用率，并降低了运维成本和复杂性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [Kubernetes](/tags/kubernetes/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [AWS](/tags/aws/) / [MLOps](/tags/mlops/) / [Python SDK](/tags/python-sdk/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--6.md" >}})
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*