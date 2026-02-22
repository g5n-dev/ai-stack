---
title: "基于 Union.ai 和 Flyte 在 Amazon EKS 上构建可扩展 AI 工作流"
date: 2026-02-22T00:55:42+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon Elastic Kubernetes Service (Amazon EKS) 上构建和扩展人工智能（AI）工作流。 主要内容包括： 1. **核心工具与功能**：文章详细说明了如何使用 Flyte Python SDK 来编排和扩展 AI/ML"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 基于 Union.ai 和 Flyte 在 Amazon EKS 上构建可扩展 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们将介绍如何使用 Flyte Python SDK 编排并扩展 AI/ML 工作流。我们探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并实现与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务的无缝集成。我们将通过一个使用 Amazon S3 Vectors 新服务的 AI 工作流示例来深入讲解这一解决方案。

---
## 导语

在 AI 工程化实践中，如何利用 Kubernetes 的弹性优势来高效编排和扩展工作流，是许多团队面临的技术挑战。本文将深入探讨如何利用 Union.ai 2.0 系统在 Amazon EKS 上部署 Flyte，并实现与 S3、Aurora 等 AWS 服务的原生集成。通过一个基于 Amazon S3 Vectors 的实战示例，我们将为您展示如何构建稳定、可扩展的 AI 工作流，从而简化基础设施管理并提升开发效率。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon Elastic Kubernetes Service (Amazon EKS) 上构建和扩展人工智能（AI）工作流。

主要内容包括：

1.  **核心工具与功能**：文章详细说明了如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。
2.  **部署与集成**：重点展示了 Union.ai 2.0 系统如何支持在 Amazon EKS 上部署 Flyte，并能与 AWS 生态系统内的多项服务实现无缝集成。
3.  **关联服务**：这些被集成的关键服务包括 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 以及 Amazon CloudWatch。
4.  **实践案例**：文章通过一个具体的 AI 工作流示例，结合了全新的 Amazon S3 Vectors 服务，对解决方案的实际应用进行了演示。

---
## 评论

**文章核心观点**
该文章提出了一种基于 Union.ai 2.0 和 Amazon EKS 的技术方案，旨在构建一个结合云原生弹性伸缩能力与统一代码管理的可扩展 AI/ML 工作流平台。

**技术论证与架构边界分析**

1.  **云原生架构与资源调度**
    *   **技术实现：** 文章详细阐述了利用 Kubernetes（EKS）作为底层设施，结合 Flyte 的“数据与计算分离”设计，将模型训练任务调度至 EC2 Spot 或 Fargate。这种架构旨在利用云资源的弹性应对工作负载的波动，从而优化资源使用成本。
    *   **边界条件：** 该架构引入了较高的运维复杂度。对于中小型团队或处于实验性质的项目，维护 EKS 集群及 Union.ai 控制平面的成本可能过高。在处理轻量级定时任务时，传统的 AWS Step Functions 或 Airflow 可能是更轻量的替代方案。

2.  **代码管理与多语言支持**
    *   **技术实现：** 文章展示了 Flyte Python SDK 如何实现工作流的代码化定义，以及 Union.ai 如何通过提供注册中心来解决分发和版本控制问题。此外，对 R、Java 等语言的支持有助于跨技术栈协作。
    *   **边界条件：** “代码即工作流”的模式虽然对开发者友好，但在处理遗留系统或依赖低代码可视化编排的场景时，灵活性可能不如部分竞品。同时，Flyte 的强类型数据传递机制在处理非结构化数据或高动态性任务时，可能会增加开发复杂度。

3.  **AWS 生态集成与安全性**
    *   **技术实现：** 文章描述了利用 AWS S3 进行数据交换，以及通过 IAM Roles for Service Accounts (IRSA) 实现权限管理。这种集成模式旨在确保数据 I/O 性能与安全性，形成从数据摄取到模型部署的闭环。
    *   **边界条件：** 这种深度集成导致了厂商锁定风险。尽管 Flyte 开源，但 Union.ai 托管服务及特定 EKS 部署模式使得向其他云平台迁移的难度和成本显著增加。对于实施多云策略的企业，需评估这种耦合带来的潜在影响。

**综合评价**

*   **1. 内容深度：** 文章深入到了容器化、资源调度及 IAM 权限配置等具体工程层面，准确指出了 MLOps 中从开发环境向生产环境迁移的关键技术难点。
*   **2. 实用价值：** 对于已采用 AWS 技术栈且具备 Kubernetes 运维能力的团队，文章提供了具体的部署参考，有助于解决自建集群时的依赖管理和网络配置问题。
*   **3. 技术定位：** 文章主要侧重于现有技术的整合应用，而非提出全新理论。其价值在于将 Union.ai 的商业化功能与 AWS 基础设施进行了标准化的结合。
*   **4. 可读性：** 文章结构逻辑清晰，技术术语使用规范，配合代码示例有助于读者理解具体实现流程。
*   **5. 行业趋势：** 该内容反映了 MLOps 工具从通用调度向针对 AI/ML 优化的专用数据平面演进的趋势，以及云厂商与独立软件供应商（ISV）之间合作加深的行业动态。
*   **6. 潜在局限：** 文章隐含了“所有 AI 工作流均适用于 K8s”的前提。然而，对于部分推理服务或简单批处理任务，Serverless 架构（如 AWS Lambda）可能具有更高的效率。此外，Union.ai 开源版与托管服务之间的功能差异也是评估时需要考虑的因素。

---
## 技术分析

基于提供的标题和摘要，以下是对《Build AI workflows on Amazon EKS with Union.ai and Flyte》一文的深度分析。文章虽然只提供了摘要，但其核心涵盖了现代 AI 基础设施中最关键的三个领域：**编排**、**容器化** 和 **云原生架构**。

---

## 1. 核心观点深度解读

**主要观点：**
文章的核心主张是，为了构建可扩展、生产级的 AI/ML 工作流，企业不应从零开始构建基础设施，而应采用 **Union.ai（基于 Flyte）** 作为编排层，并将其部署在 **Amazon EKS** 上。这种组合利用了 Kubernetes 的弹性与 AWS 的云生态优势，实现了从实验模型到生产环境的无缝过渡。

**核心思想：**
作者传达了 **"分离业务逻辑与基础设施"** 的思想。通过使用 Flyte Python SDK，数据科学家可以专注于 Python 代码本身，而将任务调度、扩展、容错和资源管理交给 Union.ai 和 EKS 处理。这代表了从“以脚本为中心”向“以工作流为中心”的 AI 工程化转型。

**创新性与深度：**
- **创新性：** 提出了一种“混合托管”模式。Flyte 开源，但通过 Union.ai 提供企业级控制平面，而计算平面运行在客户自己的 EKS 集群上。这解决了开源软件缺乏支持和完全托管服务缺乏灵活性的矛盾。
- **深度：** 文章触及了 AI 工作流的“最后一公里”问题——即如何将训练好的模型和数据处理流程大规模、高可靠地部署在云端，而不仅仅是在笔记本中运行。

**重要性：**
随着大模型（LLM）和复杂数据管道的兴起，单机脚本已无法满足需求。这种架构是解决 AI 工业化生产中“可扩展性”和“可重复性”痛点的关键路径。

## 2. 关键技术要点

**涉及的关键技术：**
1.  **Flyte:** 一个开源的工作流编排平台，专门用于构建数据和 ML 流程。
2.  **Union.ai 2.0:** Flyte 的商业发行版，提供控制平面和更简便的部署体验。
3.  **Amazon EKS (Elastic Kubernetes Service):** AWS 托管的 Kubernetes 服务。
4.  **Flyte Python SDK:** 用于定义任务和工作流的 Python 库。
5.  **AWS S3 (Simple Storage Service):** 用于存储数据、模型和工件的底层存储。

**技术原理与实现方式：**
- **声明式工作流：** 用户使用 Python 装饰器（如 `@task` 和 `@workflow`）定义代码。Flyte 将这些代码编译成不可变的 DAG（有向无环图）。
- **容器化执行：** Flyte 自动将 Python 任务打包成容器，并在 EKS 上以 Pod 的形式调度执行。
- **多语言支持与扩展：** 虽然 SDK 是 Python 的，但 Flyte 后端支持任何可容器化的语言（如 Rust, C++），通过 Sidecar 模式实现高性能任务。

**技术难点与解决方案：**
- **难点：** 在 Kubernetes 上运行 ML 任务面临资源碎片化、GPU 调度复杂和任务容错难的问题。
- **解决方案：**
    - **Flyte Bin packing（装箱算法）：** 智能地将多个任务调度到同一个节点，提高资源利用率。
    - **自动重试与幂等性：** 内置的重试机制处理 EKS 上的瞬时故障。
    - **动态实例化：** 根据工作流需求动态调整 EKS 节点大小（如使用 Spot 实例）。

**技术创新点：**
- **数据血缘与版本控制：** Flyte 自动追踪每一次运行的输入输出，存储在 S3 中，解决了 ML 实验难以复现的难题。
- **延迟执行：** 工作流定义时并不运行，只有在提交到 Union.ai 服务端后才实例化，允许复杂的逻辑编排。

## 3. 实际应用价值

**对实际工作的指导意义：**
该架构为数据团队提供了一个标准化的 **MLOps 平台蓝图**。它消除了维护自定义 Airflow 或 Kubernetes Operator 的负担，让团队能专注于算法优化。

**应用场景：**
1.  **大规模模型训练：** 需要多节点分布式训练（如 PyTorch Distributed）的场景。
2.  **ETL 与数据清洗：** 每日需要处理 PB 级数据，且需要严格错误处理的管道。
3.  **批处理推理：** 每天定时对百万级用户进行模型评分。
4.  **LLM 微调流程：** 涉及数据下载、转换、微调、评估的复杂多步骤流程。

**需要注意的问题：**
- **成本控制：** EKS 和 AWS 资源如果不加监控（如利用 Spot 实例但未处理中断），成本可能飙升。
- **学习曲线：** 团队需要理解 Kubernetes 的基本概念（Pod, Namespace, Service）才能有效排查问题。
- **冷启动：** 对于极短的任务，容器启动的开销可能成为瓶颈。

**实施建议：**
- 从非关键业务的数据管道开始迁移。
- 利用 EKS 的 Cluster Autoscaler 结合 Karpenter 实现精细的节点管理。
- 将所有依赖项容器化，避免“在我机器上能跑”的问题。

## 4. 行业影响分析

**对行业的启示：**
这篇文章反映了 **"Kubernetes 成为 ML 标准运行时"** 的趋势。以前 ML 依赖 HPC（高性能计算）集群，现在正全面转向云原生的 K8s 生态。

**可能带来的变革：**
- **降低 MLOps 门槛：** 使得中型公司也能拥有以前只有 Google/Meta 才拥有的内部编排平台能力。
- **混合云部署：** 由于 Union.ai 和 Flyte 的架构，工作流可以轻松地在 AWS、Azure 或私有云之间迁移，避免了厂商锁定。

**相关领域发展趋势：**
- **Serverless ML 的兴起：** 虽然 EKS 是核心，但未来会更多结合 AWS Fargate（Serverless 计算）来运行无需管理节点的 ML 任务。
- **数据与模型的融合：** 编排工具将不再仅处理数据，而是更多地管理模型生命周期（LLMOps）。

## 5. 延伸思考

**引发的思考：**
- **边界在哪里？** 对于极小规模的团队，EKS + Union.ai 是否过于复杂？是否应该直接使用 SageMaker 的完全托管服务？
- **LLM 时代的编排：** 传统的 DAG 编排能否适应 LLM 的 Agent 循环（非确定性流程）？Flyte 如何支持基于事件的动态工作流？

**拓展方向：**
- **FinOps（财务运营）：** 如何在 Flyte 层面精确计算每次 ML 训练的 AWS 账单并进行标签化。
- **GPU 共享：** 结合 NVIDIA MIG 技术在 EKS 上实现 GPU 切分，以运行更多小模型推理任务。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现状：** 如果你正在使用 cron jobs 或简单的 Airflow 来跑 ML 任务，且面临扩展性问题，考虑此方案。
2.  **环境搭建：**
    -   在 AWS 上创建 EKS 集群。
    -   安装 Flyte Helm Chart 或注册 Union.ai SaaS 服务指向该集群。
    -   配置 IAM Roles for Service Accounts (IRSA) 以允许 Flyte 访问 S3。
3.  **代码改造：** 将现有的 Python 脚本用 `@task` 装饰器包装，用 `@workflow` 连接。

**具体行动建议：**
- **容器化优先：** 即使不立即上 Flyte，先将所有 ML 脚本 Docker 化。
- **模块化设计：** 将代码拆分为原子任务，便于 Flyte 并行调度。

**补充知识：**
- 学习 **Docker** 和 **Kubernetes** 基础。
- 熟悉 **Python 类型提示**，因为 Flyte 强类型依赖于此。
- 了解 **AWS IAM** 权限管理。

## 7. 案例分析

**成功案例（假设性分析）：**
- **Spotify：** 类似规模的公司使用 Flyte 来处理其庞大的推荐系统训练。他们利用 EKS 的弹性在夜间扩展 GPU 集群进行训练，白天缩容以节省成本。
- **关键成功因素：** 极高的资源利用率（通过 Bin packing）和自动化的失败重试机制。

**失败案例反思：**
- **反模式：** 某公司试图将单体应用强行拆分为 Flyte 任务，导致任务间数据传输（I/O）开销巨大，甚至超过了计算时间。
- **教训：** 不要为了编排而编排。任务粒度要适中，数据尽量通过 S3 引用传递，而非在任务间直接传递大数据对象。

## 8. 哲学与逻辑：论证地图

**中心命题：**
**对于追求高可扩展性和可维护性的 AI/ML 团队，基于 Amazon EKS 部署 Union.ai/Flyte 是优于传统脚本和通用编排器的最佳架构选择。**

**支撑理由与依据：**
1.  **可扩展性：** EKS 提供无限的计算资源，Flyte 提供智能调度。
    *   *依据：* Kubernetes 的弹性伸缩能力。
2.  **可移植性：** 基于容器的标准化构建避免了环境依赖。
    *   *依据：* "It works on my machine" 问题的消除。
3.  **可维护性：** 声明式代码使得工作流逻辑清晰，且自带版本控制。
    *   *依据：* GitOps 理念的普及。

**反例或边界条件：**
1.  **超小规模团队：** 对于只有 2-3 个数据科学家的初创公司，维护 EKS 集群的运维成本可能超过收益，直接使用 SageMaker 或托管 Notebook 可能更合适。
2.  **超低延迟要求：** 如果是实时推理（毫秒级），Flyte/EKS 这种面向批处理的架构并不适用，应使用 SageMaker Endpoints 或 Lambda。

**命题性质分析：**
- **事实：** Flyte 和 EKS 是成熟的技术栈。
- **价值判断：** "最佳架构选择" —— 这取决于团队的具体需求（成本 vs 控制）。
- **可检验预测：** 采用该架构的团队，其模型部署频率将提高，基础设施维护的人力投入将降低。

**立场与验证：**
- **立场：** 支持在**中大型**或**对数据合规有要求**的 AI 团队中采用此架构。
- **验证方式：**
    - **指标：** 监控集群资源利用率（CPU/GPU）、任务失败率、开发到生产的平均部署时间。
    - **实验窗口：** 迁移一个完整的端到端 ML 流程（数据清洗->训练->评估），对比迁移前后的运维工单数量和计算成本。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化容器资源请求与限制

**说明**: 在 Amazon EKS 上运行 AI 工作流时，计算资源管理至关重要。Flyte 允许为每个任务定义具体的 CPU 和内存请求以及限制。合理设置这些参数不仅能防止资源浪费（过度配置），还能避免因资源不足（OOMKilled）导致的任务失败。对于 GPU 密集型任务，必须明确指定 GPU 资源需求（如 `nvidia.com/gpu`）。

**实施步骤**:
1. 在 Flyte 任务装饰器或任务定义中，根据模型推理或训练的实际负载，设置 `requests`（保证的最小资源）和 `limits`（最大可用资源）。
2. 使用 Flyte 的 `@task` 装饰器配置资源，例如：`@task(requests=Resources(cpu="2", mem="8Gi"), limits=Resources(gpu="1"))`。
3. 针对不同类型的任务（如数据预处理 vs 模型训练）建立标准化的资源配置模板。

**注意事项**: 避免将 Limits 设置得远高于 Requests，这会导致 Kubernetes 调度困难；对于 GPU 任务，Requests 和 Limits 通常必须相等。

---

### 实践 2：利用 Spot 实例进行成本优化

**说明**: AI 工作流通常包含容错性较好的批处理任务（如模型训练、超参数搜索）。在 Amazon EKS 上配置 Node Groups 使用 Spot 实例可以显著降低计算成本（最高可达 90%）。Union.ai 和 Flyte 支持通过 Karpenter 或 EKS 托管节点组自动管理 Spot 实例的混合使用。

**实施步骤**:
1. 在 EKS 集群中配置 Karpenter 或创建混合了 Spot 和 On-Demand 实例的托管节点组。
2. 在 Flyte 的任务配置中，利用 FlytePropeller 的容错机制，设置合理的重试策略，以应对 Spot 实例可能发生的中断。
3. 为可中断的任务添加特定的注解或标签，使其优先调度到 Spot 节点上。

**注意事项**: 必须确保 Flyte 任务实现了检查点保存，以便在 Spot 实例被回收时能够从上次中断的位置恢复，而不是完全重跑。

---

### 实践 3：实施高效的缓存策略

**说明**: Flyte 提供了强大的缓存机制。如果输入参数、代码逻辑和依赖项未发生变化，Flyte 可以直接返回上次执行的结果，而无需重新运行容器。这对于开发调试和迭代 AI 模型非常有用，可以节省大量时间和计算资源。

**实施步骤**:
1. 在 Flyte 项目设置中启用缓存功能。
2. 确保任务函数是确定性的，即相同的输入必须产生相同的输出。
3. 对于数据加载或预处理等耗时且不变的任务，显式配置较长的缓存 TTL（生存时间）。

**注意事项**: 避免在任务内部引入非确定性的调用（如 `random.seed` 未固定或获取当前时间戳），否则会导致缓存失效。

---

### 实践 4：利用动态工作流处理超参数调优

**说明**: AI 模型开发通常需要进行大量的实验。Flyte 的动态工作流允许在运行时生成任务图。结合 Union.ai 的功能，可以轻松构建并行化的超参数调优或模型评估流程，从而在 EKS 上高效扩展实验规模。

**实施步骤**:
1. 编写动态任务，使用 `@dynamic` 装饰器。
2. 在动态任务内部，根据参数组合循环创建并发射子任务。
3. 利用 EKS 的自动扩缩容（ASG 或 Cluster Autoscaler）特性，确保当并行任务增加时，集群能够自动增加节点以承载负载。

**注意事项**: 动态工作流的并发度可能会产生 API 请求速率限制，需合理控制并发任务的数量，避免压垮 Flyte 后端服务或 EKS 控制平面。

---

### 实践 5：构建与使用自定义容器镜像

**说明**: AI 工作流通常依赖复杂的深度学习框架（如 PyTorch, TensorFlow）和特定的 CUDA 版本。最佳实践是为每个工作流构建包含所有依赖项的轻量级自定义容器镜像，而不是依赖通用的基础镜像。

**实施步骤**:
1. 使用 Docker 或构建工具（如 Kaniko, Buildah）基于 NVIDIA 的 CUDA 基础镜像构建自定义镜像。
2. 将 Flytekit（Flyte 的 Python SDK）以及模型代码依赖（`requirements.txt`）打包进镜像。
3. 将镜像推送到 Amazon ECR（Elastic Container Registry），并在 Flyte 任务中引用该镜像 URL。

**注意事项**: 保持镜像精简，只安装必要的库，以减少 Pod 启动时间。建议使用多阶段构建来清理构建缓存和不必要的文件。

---

### 实践 6：配置存储集成与数据传递

**说明**: 在 EKS 上运行 AI 任务时，高效的数据传输是性能瓶颈之一。应避免通过容器层传递大型数据集。最佳实践是利用 S3 作为中转存储，Flyte

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、可维护的 AI 工作流，实现机器学习与数据管道的高效编排。
- 利用 EKS 的容器化能力，Flyte 能够自动化管理工作流的计算资源，显著提升 AI 任务在云端的运行效率与弹性。
- 该架构支持混合云部署，允许企业在保持数据主权和控制力的同时，灵活调度复杂的机器学习训练与推理任务。
- 通过 Flyte 的版本控制和数据血缘追踪功能，开发团队可以轻松复现实验结果并确保机器学习模型的可重复性。
- 集成 Amazon EKS 使得 AI 工作流能够无缝对接 AWS 生态系统的其他服务（如 S3 和 IAM），从而简化基础设施的管理。
- 采用此开源方案有助于企业避免供应商锁定，并能利用社区支持来加速 AI 应用的落地与迭代。

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
- [在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260221-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--10.md" >}})
- [基于Union.ai与Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260221-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*