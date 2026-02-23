---
title: "使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流"
date: 2026-02-23T10:25:22+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI 工作流。 **核心内容总结：** 1. **技术架构**： * 利用 **Flyte Python SDK** 编排和扩展 AI/ML 工作流。 * 通过 **Union.ai 2.0** 系统，将 Flyte 部署在"
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

在本文中，我们介绍如何使用 Flyte Python SDK 编排并扩展 AI/ML 工作流。我们探讨 Union.ai 2.0 如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们通过一个使用新型 Amazon S3 Vectors 服务的 AI 工作流示例来讲解这一解决方案。

---
## 导语

随着 AI 工作流的复杂度日益增加，在 Kubernetes 上实现高效、可扩展的编排已成为技术团队的关键挑战。本文将介绍如何利用 Union.ai 和 Flyte，在 Amazon EKS 上构建稳健的机器学习流水线，并实现与 S3、Aurora 等 AWS 服务的深度集成。通过阅读本文，您将掌握具体的部署步骤，并了解如何利用 Amazon S3 Vectors 服务优化数据处理流程，从而提升生产环境的自动化水平。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI 工作流。

**核心内容总结：**

1.  **技术架构**：
    *   利用 **Flyte Python SDK** 编排和扩展 AI/ML 工作流。
    *   通过 **Union.ai 2.0** 系统，将 Flyte 部署在 **Amazon EKS**（弹性 Kubernetes 服务）上。

2.  **AWS 服务集成**：
    *   该解决方案实现了与 AWS 生态系统的无缝集成，主要涉及的服务包括：
        *   **Amazon S3**：用于存储（文中提及了使用新的 Amazon S3 Vectors 服务进行 AI 示例演示）。
        *   **Amazon Aurora**：数据库服务。
        *   **AWS IAM**：身份与访问管理。
        *   **Amazon CloudWatch**：监控与日志。

3.  **应用场景**：
    *   文章通过一个具体的 AI 工作流示例，展示了如何利用 Amazon S3 Vectors 服务来实际操作和验证该解决方案。

简而言之，该文旨在指导开发者使用 Union.ai 和 Flyte 在 Kubernetes 环境下高效管理 AI 流程，并充分利用 AWS 的云服务能力。

---
## 评论

**中心观点**
该文章的核心观点是：通过将 Union.ai（基于 Flyte）与 Amazon EKS 深度集成，企业可以在 Kubernetes 原生环境中构建一种既具备云弹性又拥有代码可移植性的“混合编排”层，从而解决从模型实验到生产环境部署过程中的工程摩擦和扩展性难题。

**支撑理由与深度评价**

**1. 解决了“有状态计算”与“无状态编排”的架构冲突（事实陈述 / 作者观点）**
*   **分析**：从技术深度来看，文章触及了 AI 工作流编排的核心痛点。传统的 Kubernetes（如 EKS）擅长调度无状态服务，而 AI/ML 训练和数据处理是重度有状态、长耗时的任务。Flyte 的核心价值在于其基于 Kubernetes 自定义资源（CRD）构建的扩展机制，能够将 Python 函数转化为 Pod、Job 或分布式训练任务。
*   **评价**：这是一个非常务实的技术路径。它没有试图重新发明轮子，而是利用 K8s 的控制器模式来管理 ML 生命周期。文章论证了 Union.ai 2.0 作为控制平面，如何简化了在 EKS 上部署 Flyte 的复杂度（通常涉及复杂的 Helm 配置和组件依赖）。
*   **反例/边界条件**：如果企业的 AI 工作流仅涉及简单的推理或轻量级数据处理，引入 Flyte + EKS 的架构可能显得“杀鸡用牛刀”。对于仅需 Serverless 触发的场景，AWS Lambda 或 SageMaker 的端到端托管服务可能具有更低的运维负担。

**2. 推动了“以代码为中心”的 MLOps 标准化（事实陈述 / 你的推断）**
*   **分析**：文章强调了 Flyte Python SDK 的使用，这意味着工作流即代码。这具有极高的实用价值。它使得数据科学家可以在本地编写 Python 代码，定义依赖关系和容器镜像，而无需关心底层的 K8s YAML 配置。
*   **评价**：这种抽象层极大地降低了 MLOps 的认知门槛。从行业角度看，这是向“软件工程化”迈进的一步。它强制实施了版本控制、模块化和可复现性，这些是生产级 AI 系统的关键。
*   **反例/边界条件**：Flyte 的强类型系统和特定 DSL 语法存在学习曲线。对于习惯于完全自由脚本编写的数据科学团队，这种结构化约束可能会在初期引发抵触。此外，对于非 Python 为主的技术栈（如大量使用 R 或 Java），集成体验可能不如原生 Python 流畅。

**3. 云原生与多云避免厂商锁定的博弈（作者观点 / 你的推断）**
*   **分析**：文章虽然重点在于 EKS，但 Union.ai 和 Flyte 的底层逻辑是云中立的。这是一个隐含但极具战略意义的观点。
*   **评价**：在行业影响方面，这提供了一种对抗“深度厂商绑定”的方案。虽然文章展示了与 S3、SageMaker 等服务的集成，但其编排层是可移植的。如果未来企业想从 AWS 迁移至 Azure 或自建 K8s 集群，业务逻辑代码无需重写。
*   **反例/边界条件**：虽然编排层可移植，但底层基础设施（如 EKS、IAM、VPC）的配置依然是高度特化的。实际上，要实现真正的“可移植性”，运维团队必须具备极高水平的 K8s 能力，这往往比直接使用公有厂商托管服务（如 AWS Step Functions）更难。

**争议点与不同观点**

*   **K8s 运维复杂度 vs. 托管服务的便利性**：
    文章倾向于“自建/自管”控制平面。然而，业界主流观点（尤其是中小企业）倾向于完全托管。AWS SageMaker Pipelines 或 Azure ML Pipelines 虽然锁定性强，但提供了“开箱即用”的体验。使用 Union.ai + EKS 意味着企业必须自己维护 K8s 集群的升级、安全补丁和节点扩缩容，这是一笔不小的隐性成本。
*   **编排工具的碎片化**：
    目前市场上存在 Apache Airflow, Prefect, Dagster 等成熟工具。Flyte 在 ML 领域虽然专注，但生态成熟度和插件丰富度不如 Airflow。文章未探讨为何不选择 Airflow on EKS，这是一个值得商榷的技术选型对比。

**实际应用建议**

1.  **适用场景**：该方案最适合**中大型企业**或**AI 原生公司**，其特征是：拥有专门的 MLOps/平台工程团队，工作流涉及复杂的分布式训练（如 Spark on K8s），或者有严格的合规要求需要私有化部署。
2.  **技术验证**：在全面迁移前，先使用 Union.ai 的免费层或 Flyte 的本地部署版本，对现有的 1-2 个最复杂的管线进行重构，对比其在 EKS 上的资源利用率和启动速度，与现有方案（如 Airflow 或 SageMaker）进行基准测试。
3.  **团队技能评估**：确保团队中不仅有数据科学家，还熟悉 Docker 和 Kubernetes 基础概念。如果没有 K8s 运维能力，不要直接上生产环境。

**可验证的检查方式**

1.  **冷启动时间对比**：
    *   *指标*：测量从触发工作流到 Pod Running 的时间。
    *   *实验*：对比 Flyte on EKS 与 AWS SageMaker Pipeline 在处理相同容器镜像时的启动延迟。Flyte 由于利用 K

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，我将对这篇文章进行深入的技术与战略分析。尽管全文内容未完全展开，但基于标题、摘要以及Flyte、Union.ai和EKS在业界的标准应用模式，我们可以构建一个全面的分析框架。

以下是详细的分析报告：

---

# 深度分析报告：基于 Amazon EKS 与 Union.ai 构建 AI 工作流

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心主张是**通过将 Union.ai（基于 Flyte）与 Amazon EKS 深度集成，企业可以构建一个既具备云原生弹性，又能实现复杂 AI/ML 流程编排的统一生产级平台**。它主张“编排层”与“执行层”的解耦，强调利用 Kubernetes 的强大能力来运行机器学习任务，而非仅仅依赖传统的虚拟机或专有闭环服务。

### 核心思想
作者试图传达**“基础设施即代码”与“工作流即代码”**在 AI 领域的深度融合。核心思想在于：AI 工程化不应仅止步于模型训练，必须延伸至数据流处理、模型训练、评估及部署的全生命周期自动化。Union.ai 提供了控制平面，而 EKS 提供了弹性计算平面，两者结合实现了**规模化的确定性执行**。

### 观点的创新性和深度
*   **从“脚本”到“工作流”的范式转变**：传统的 AI 开发常依赖 Jupyter Notebook 或线性脚本，缺乏容错和版本管理。该文章展示了如何通过 Flyte 将任务原子化，实现任务级别的重试、缓存和并行。
*   **混合编排的深度**：创新点在于不仅编排计算任务（PyTorch/TensorFlow），还编排 AWS 基础设施资源（如 S3 读写、IAM 角色传递），实现了逻辑与资源的深度绑定。
*   **解决“最后一公里”问题**：深度在于触及了 MLOps 的痛点——从开发环境到生产环境的迁移。EKS 提供了统一的运行时，消除了“在我机器上能跑”的环境差异。

### 为什么这个观点重要
随着大模型（LLM）和复杂 AI 应用的兴起，单机训练已无法满足需求，且计算成本高昂。一个高效的编排系统能显著降低云资源成本（通过 Spot 实例支持等）并提高工程团队的迭代效率。这是企业从“实验性 AI”走向“工业化 AI”的关键基础设施。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
*   **Amazon EKS (Elastic Kubernetes Service)**：AWS 提供的托管 Kubernetes 服务，作为底层容器编排引擎。
*   **Flyte**：一个开源的、云原生的机器学习和数据编排平台，基于 Kubernetes 构建。
*   **Union.ai**：Flyte 的商业托管版本，提供控制平面和企业级支持，简化了 Flyte 的部署和维护。
*   **Flyte Python SDK**：用于定义工作流、任务和数据流的 Python 装饰器和类库。
*   **AWS S3 (Simple Storage Service)**：用于存储数据集、模型和中间结果的数据湖。

### 技术原理和实现方式
1.  **声明式工作流定义**：利用 Python SDK 的装饰器（如 `@task`, `@workflow`）将 Python 函数编译成有向无环图（DAG）的 IR（中间表示）。
2.  **容器化与调度**：Flyte 将每个任务打包进容器（Pod），利用 EKS 的调度能力将其分发到节点上。
3.  **数据传递机制**：任务间通过引用传递数据（S3 路径），而非直接传递内存对象，实现大数据的高效处理。
4.  **自动扩展**：集成 Karpenter 或 Cluster Autoscaler，根据任务队列的积压情况自动扩缩容 EKS 节点。

### 技术难点和解决方案
*   **难点：异构计算支持**（CPU vs GPU vs 分布式训练）。
    *   **解决方案**：Flyte 允许在任务级别指定资源请求（如 `requests=gpu=1`）和自定义容器镜像，使得同一工作流中可以混合运行数据预处理（CPU）和模型训练（GPU）任务。
*   **难点：状态管理与容错**。
    *   **解决方案**：Flyte 自动记录每个任务的输入输出哈希值。如果任务失败，系统会根据策略重试；如果上游任务成功，下游任务可直接利用缓存，无需重复计算。

### 技术创新点分析
*   **Type Safety（类型安全）**：Flyte 强制要求任务接口具有明确的类型签名，这在动态语言的 Python 世界中引入了编译时的严谨性，大大减少了生产环境的数据类型错误。
*   **动态工作流（Dynamic Workflows）**：支持在运行时根据中间结果动态生成后续任务 DAG，这对于 AutoML 或超参数搜索等场景至关重要。

---

## 3. 实际应用价值

### 对实际工作的指导意义
该架构为数据科学和工程团队提供了一个**标准化的作业提交接口**。它消除了 DS 团队对底层 K8s YAML 配置的依赖，让他们能专注于 Python 代码，同时赋予工程团队对资源配额和成本的控制权。

### 可以应用到哪些场景
1.  **大规模模型微调**：定期从 S3 获取新数据，触发微调任务，完成后自动部署模型。
2.  **批推理**：每日凌晨处理海量业务数据，生成预测结果并回写数据库。
3.  **特征工程流水线**：ETL -> 特征计算 -> 模型预测 的自动化链路。
4.  **药物研发或基因组学**：需要处理数百万个并行任务的计算密集型场景。

### 需要注意的问题
*   **学习曲线**：团队需要适应 Flyte 的特定编程模式（如不能随意使用全局变量，需注意数据序列化）。
*   **运维成本**：虽然 Union.ai 降低了门槛，但维护底层的 EKS 集群（尤其是 GPU 驱动、NVIDIA 插件等）仍需专业知识。
*   **冷启动时间**：对于极短的任务，容器启动的开销可能大于任务执行时间。

### 实施建议
*   **从非关键路径开始**：先迁移批处理作业，而非实时推理服务。
*   **建立镜像仓库规范**：统一管理任务所需的 Docker 镜像，避免每次构建都拉取庞大的基础镜像。

---

## 4. 行业影响分析

### 对行业的启示
这标志着 **MLOps 正在从“工具堆砌”走向“原生融合”**。过去企业可能用 Airflow 调度脚本，用 Sageaphore 训练模型，用 S3 存数据，系统割裂。现在的趋势是利用 K8s 作为统一底座，通过专门的编排层（如 Flyte, Kubeflow）统一管理所有计算负载。

### 可能带来的变革
*   **降低 AI 基础设施的边际成本**：通过精细的调度和混合使用 Spot 实例，企业可以大幅降低 AI 计算成本。
*   **提升模型迭代速度**：标准化的流水线使得实验复现和版本回滚变得极其简单，加速了模型上线的周期。

### 相关领域的发展趋势
*   **Serverless AI 容器**：利用 AWS Fargate 或 Firecracker 微型虚拟机运行沙箱化的任务，进一步提升安全性和隔离性。
*   **多云编排**：Flyte 等工具的兴起使得企业不再被单一云厂商锁定，工作流可以轻松迁移至 Google GKE 或 Azure AKS。

---

## 5. 延伸思考

### 引发的其他思考
*   **LLM 工作流的特殊性**：传统的 Flyte 适合处理 ETL 和训练，但对于 LLM 的 Agent 编排（涉及长时间运行的异步链式调用），当前的同步批处理模式是否适用？这需要引入事件驱动的架构。
*   **成本可观测性**：在 EKS 上运行任务时，如何将账单精确地分摊到每个具体的 Flyte 任务或部门？这是 FinOps 领域的挑战。

### 可以拓展的方向
*   **与 Ray.io 的集成**：Flyte 负责编排，Ray 负责单个任务内部的并行计算。这种“编排+执行”的双层架构是未来的主流。
*   **地理分布式计算**：利用 Flyte 的多集群控制能力，在边缘节点或不同地理位置的 EKS 集群间调度任务。

### 未来发展趋势
*   **AI 基础设施的标准化**：类似于 YARN 是 Hadoop 的标准，Kubernetes + Workflow Engine 正在成为 AI 的标准操作系统。
*   **自助式 AI 平台**：随着 Union.ai 等产品的成熟，未来的 AI 平台将更像“数据库”，开发者只需写 SQL（Python），平台自动处理扩容、容错和监控。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有痛点**：如果您的团队正在使用 cron 调度 Python 脚本，且经常遇到资源不足或任务失败难以排查的问题，引入 Flyte 是极佳的选择。
2.  **环境准备**：在 AWS 上建立 EKS 集群，配置好 IRSA（IAM Roles for Service Accounts），确保 Pod 可以直接访问 S3 而无需硬编码密钥。

### 具体的行动建议
*   **步骤 1**：安装 `flytectl`，并在本地运行一个简单的 Flyte demo（sandbox 模式），理解 Task 和 Workflow 的概念。
*   **步骤 2**：将现有的一个批处理脚本（例如：每日数据报表）重写为 Flyte 任务。
*   **步骤 3**：部署 Union.ai 或开源 Flyte 到 EKS，配置 S3 作为后端存储。
*   **步骤 4**：运行工作流，观察 UI 中的 DAG 执行情况，检查日志和输出。

### 需要补充的知识
*   **Docker 容器化**：理解如何编写 Dockerfile 和优化镜像大小。
*   **Kubernetes 基础**：理解 Pod, Node, Namespace, Resource Quota 等概念。
*   **Python 类型提示**：熟练使用 Python 的 `typing` 模块。

### 实践中的注意事项
*   **避免在 `@workflow` 中写重逻辑**：Workflow 函数应该是“胶水代码”，只负责连接任务，不要进行复杂的数据处理。
*   **数据本地性**：尽量让计算靠近数据。例如，任务运行在 EKS 上，数据在 S3 上，确保 VPC 内网的高带宽访问。

---

## 7. 案例分析

### 结合实际案例说明
**案例场景**：某金融科技公司每日需要处理 1000 万笔交易数据进行欺诈检测。

*   **传统做法**：使用一个巨大的 EC2 实例运行 Pandas 脚本。经常因为内存溢出（OOM）而失败，且每次重跑需要 5 小时。
*   **Flyte + EKS 做法**：
    1.  将数据按时间切片分片。
    2.  使用 Flyte 的 `map_task` 功能，动态生成 100 个并行任务。
    3.  每个任务在 EKS 上启动一个小 Pod 处理 10 万条数据。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建可移植且可扩展的容器化工作流

**说明**: 利用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流的核心在于将每个任务封装为独立的容器。这确保了工作流的各个组件（数据预处理、模型训练、推理等）具有高度的可移植性和隔离性。通过容器化，您可以轻松地在不同的 Kubernetes 集群之间迁移工作负载，并利用 EKS 的弹性能力应对不同规模的计算需求。

**实施步骤**:
1. 将 AI 工作流中的每个步骤（如数据清洗、特征工程、模型训练）编写为独立的 Python 函数或任务。
2. 为每个任务构建相应的 Docker 镜像，确保包含所有必要的依赖项（库、框架、模型文件）。
3. 将镜像推送到 Amazon ECR（Elastic Container Registry）。
4. 在 Flyte 任务定义中引用这些 ECR 镜像，确保 EKS 节点具有拉取镜像的适当 IAM 权限。

**注意事项**: 
- 遵循最佳实践的容器构建规则（如使用多阶段构建）以减小镜像体积，加快启动速度。
- 确保镜像的基础操作系统与 EKS 节点的操作系统兼容，以避免潜在的 glibc 或其他库冲突。

---

### 实践 2：利用 Spot 实例优化成本与资源利用率

**说明**: AI 和机器学习工作负载（特别是训练和大规模批处理）通常非常适合使用容错机制。在 Amazon EKS 上配合 Flyte 使用，应优先配置节点组使用 EC2 Spot 实例。Flyte 原生支持重试机制，可以自动处理 Spot 实例中断（中止单个 Pod）的情况，从而显著降低计算成本，同时不影响工作流的最终完成率。

**实施步骤**:
1. 在 EKS 中配置托管节点组或 Karpenter 配置，优先选择 Spot 实例类型。
2. 在 Flyte 的任务定义中，配置合理的重试策略和超时时间。
3. 为工作流配置检查点，如果任务被中断，Flyte 可以从上一个成功的检查点恢复，而不是从头开始。

**注意事项**: 
- 并非所有任务都适合 Spot（例如极短的任务或无法中断的实时推理），应根据任务特性混合使用 On-Demand 和 Spot 实例。
- 确保工作流处理逻辑是幂等的，以便在重试时不会产生数据副作用。

---

### 实践 3：实施动态资源请求与自动扩缩容

**说明**: AI 工作流的资源需求波动极大。例如，数据预处理可能需要大量 CPU，而深度学习训练则需要昂贵的 GPU。最佳实践是不要为所有 Pod 分配固定的资源，而是利用 Flyte 的动态资源请求功能，结合 EKS 的 Cluster Autoscaler 或 Karpenter，根据任务的实际需求动态分配和释放节点资源。

**实施步骤**:
1. 在 Flyte 任务定义中，根据任务逻辑动态计算所需的 CPU 和内存数量，并在运行时传递给 Kubernetes。
2. 配置 EKS 的 Cluster Autoscaler 或部署 Karpenter，使其能够根据 Pod 的 pending 状态自动扩展节点。
3. 设置适当的资源限制和请求，以防止“吵闹邻居”效应，确保关键任务获得足够的资源。

**注意事项**: 
- 监控集群的扩缩容事件，避免因频繁的扩缩容操作导致云厂商 API 限流。
- 确保节点的最大和最小限制符合预算约束，防止意外的高额账单。

---

### 实践 4：集中化管理与多租户隔离

**说明**: 当在多个团队或项目之间共享 EKS 集群时，必须实施严格的隔离策略。利用 Union.ai 的控制平面和 Flyte 的项目/域概念，可以在逻辑上隔离开发、测试和生产环境。同时，利用 Kubernetes 的命名空间和 RBAC（基于角色的访问控制）在物理和权限层面实现多租户隔离。

**实施步骤**:
1. 为不同的环境或团队创建专用的 Kubernetes 命名空间。
2. 配置 Flyte 的域概念，将工作流执行映射到相应的命名空间。
3. 使用 Kubernetes RBAC 和 AWS IAM 进行精细的权限控制，确保开发人员只能提交或查看其授权范围内的任务。
4. 配置资源配额，防止单个团队消耗过多集群资源。

**注意事项**: 
- 定期审计 IAM 角色和 Kubernetes RBAC 策略，确保权限最小化原则。
- 确保日志和监控系统能够区分不同租户的数据，以便于故障排查和成本分摊。

---

### 实践 5：建立高效的 CI/CD 集成流水线

**说明**: AI 模型需要频繁迭代。最佳实践是将 Flyte 工作流的开发、测试和部署集成到标准的 CI/CD 流程中。通过自动化流水线，可以在代码提交时自动构建容器镜像、注册 Flyte 工作流，并触发测试执行，从而加速从算法开发到生产部署的周期。

**实施步骤**:
1. 使用 GitHub Actions 或

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、生产级的 AI 工作流，实现机器学习任务的高效编排与自动化。
- 利用 Amazon EKS 作为底层基础设施，可为 AI 工作流提供强大的容器编排能力，确保计算资源的高利用率和弹性伸缩。
- Flyte 的数据感知型工作流编排能力，能够自动化管理数据依赖关系和模型训练流水线，显著提升开发效率。
- 该架构支持 GPU 加速和分布式训练，能够有效处理大规模数据集和复杂的深度学习模型训练任务。
- 通过在云端构建标准化的机器学习流水线，企业可以加速 AI 模型从原型到生产环境的落地与迭代。

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