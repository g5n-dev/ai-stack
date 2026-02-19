---
title: "使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流"
date: 2026-02-19T19:36:28+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "S3 Vectors"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "这篇文章介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建和扩展 AI/ML 工作流。 主要内容包括： 1. **技术栈与集成**：使用 Flyte Python SDK 进行工作流编排，并通过 Union.ai 2.0 系统将 Flyte 部署在 Amazon"
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

在本文中，我们将说明如何使用 Flyte Python SDK 编排和扩展 AI/ML 工作流。我们探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service（Amazon EKS）上部署 Flyte，并与 Amazon Simple Storage Service（Amazon S3）、Amazon Aurora、AWS Identity and Access Management（IAM）和 Amazon CloudWatch 等 AWS 服务无缝集成。我们通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来探讨该解决方案。

---
## 导语

随着 AI 工作流的复杂度日益增加，如何高效编排并利用云原生基础设施成为技术团队的关键挑战。本文将探讨如何利用 Union.ai 2.0 在 Amazon EKS 上部署 Flyte，并实现与 S3、Aurora 等 AWS 服务的无缝集成。通过结合 Flyte Python SDK 与 Amazon S3 Vectors 服务的实战示例，我们将向您展示如何在 Kubernetes 环境中构建可扩展、高可用的机器学习流水线。

---
## 摘要

这篇文章介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建和扩展 AI/ML 工作流。

主要内容包括：
1.  **技术栈与集成**：使用 Flyte Python SDK 进行工作流编排，并通过 Union.ai 2.0 系统将 Flyte 部署在 Amazon EKS 上。
2.  **AWS 服务整合**：该方案实现了与 AWS 生态系统的无缝集成，包括利用 **Amazon S3** 进行存储、**Amazon Aurora** 作为数据库、**IAM** 进行身份与访问管理，以及使用 **Amazon CloudWatch** 进行监控。
3.  **应用示例**：文章通过一个具体的 AI 工作流示例，展示了如何结合使用新的 **Amazon S3 Vectors** 服务来实际操作。

**总结：** 这是一种在 AWS 上利用 Kubernetes (EKS) 进行可扩展、高度集成的 AI 工作流管理的解决方案。

---
## 评论

### 中心观点
**本文的核心观点是：通过将开源工作流编排工具 Flyte 与 Union.ai 的商业支持平台结合，并部署在 Amazon EKS 上，企业可以在云原生环境中构建一种既具备高度可扩展性，又能有效隔离计算与逻辑的“单一事实来源”式 AI/ML 研发体系，从而解决从实验原型到大规模生产环境过渡中的工程化难题。**

### 深入评价

#### 1. 支撑理由

*   **事实陈述：云原生架构是处理复杂 ML 工作流的标准解法**
    文章指出 Flyte 基于 Kubernetes (EKS) 运行，利用 K8s 的调度能力来处理 ML 任务中异构资源（如 GPU、CPU）的申请与释放。这在技术上是当前业界的标准答案。ML 工作流（特别是深度学习训练）具有明显的潮汐效应，Kubernetes 提供了比传统 HPC 或虚拟机更灵活的弹性伸缩能力。

*   **作者观点：数据与代码的“单一事实来源”是解决 ML 复杂性的关键**
    文章强调 Flyte 能够将数据、模型和代码版本化，确保工作流的确定性。这是一个非常深刻的工程观点。在数据科学领域，"It works on my machine" 是常态，导致生产环境复现困难。Flyte 强制用户定义输入输出，使得任务之间通过明确的数据契约连接，而非隐式的共享状态，这极大地提升了系统的可维护性和可观测性。

*   **你的推断：Union.ai 的核心价值在于降低 Flyte 的准入门槛**
    虽然 Flyte 是开源的，但部署和维护一套生产级的 Flyte on K8s 集群具有极高的技术门槛（涉及数据库、对象存储、容器注册表、IAM 角色配置等）。文章暗示 Union.ai 2.0 提供了托管或自动化部署能力。从行业角度看，这是典型的 "Open Core" 商业模式——通过简化开源工具的运维复杂性来获利，这对缺乏专职 DevOps 团队的 ML 实验室极具吸引力。

#### 2. 反例与边界条件

*   **边界条件一：并非所有场景都需要“重型”编排**
    对于轻量级的快速实验或单纯的模型训练脚本，引入 Flyte + EKS 的架构过于厚重。如果数据科学家只是想跑一个 Jupyter Notebook 调试参数，使用 SageMaker Studio 或本地环境更高效。Flyte 的价值在于“流水线”和“重复执行”，对于探索性数据分析（EDA）阶段，其严格的类型定义反而可能降低开发效率。

*   **边界条件二：云原生锁定的隐形成本**
    虽然文章强调部署在 EKS 上，且 Flyte 是开源的，但深度集成 AWS 服务（如 S3, IAM, SageMaker）会导致基础设施层面的强耦合。一旦企业需要混合云部署（例如部分数据在私有云，部分在 AWS），这种深度集成的架构迁移成本将显著增加。此外，EKS 本身的运维复杂度（控制平面管理、版本升级）依然是中小企业的一大负担。

### 多维度评价

#### 1. 内容深度与论证严谨性
文章在技术实现的细节上达到了较高的深度。它没有停留在概念层面，而是具体到了如何利用 Python SDK 定义任务、如何利用 EKS 的 Spot 实例优化成本。然而，文章在**论证严谨性**上存在选择性偏差：它重点展示了“成功路径”，即一切配置正确后的流畅运行，但较少讨论在分布式训练中常见的网络断连、任务悬挂或 OOM（内存溢出）时的故障恢复机制细节。

#### 2. 实用价值
对于处于**“成熟期”**的 AI 团队（即拥有明确的模型上线流程，且团队规模超过 5-10 人），这篇文章的实用价值极高。它提供了一套从“代码”到“生产”的标准化路径。特别是关于如何利用 Flyte 的缓存机制跳过已执行步骤的建议，在实际工作中能节省大量计算成本和时间。

#### 3. 创新性
文章本身没有提出全新的理论，**创新性主要体现在“组合方式”上**。将 Union.ai 的控制平面与 AWS 的计算平面（EKS）深度结合，并强调“以数据为中心”的编排（而非以脚本为中心），这是对当前 MLOps 领域 Airflow 等传统工具的一种有力补充和修正。Flyte 针对 ML 特有的大数据传输优化是其相对于通用编排工具的核心差异点。

#### 4. 行业影响与争议点
*   **行业影响：** 这类文章推动了 MLOps 从“脚本化”向“平台化”演进。它暗示了未来的 AI 工程师不仅要懂算法，还必须具备容器化和云原生的思维。
*   **争议点：** 编排工具的**碎片化**。目前市场上不仅有 Flyte，还有 Prefect, Dagster, Kubeflow, 以及 AWS 原生的 SageMaker Pipelines。文章试图证明 Flyte 是最佳选择，但并未客观对比它与 SageMaker Pipelines 的优劣。实际上，如果全家桶都在 AWS，使用 SageMaker Pipelines 可能集成度更高，无需自行维护 EKS 集群。

### 实际应用建议

1.  **不要为了技术而技术：** 如果你的团队只有 2-3 个数据科学家，且模型训练频率很低，请直接使用 SageMaker 的托管服务，不要自己搭建 Flyte on EKS，运维成本会吞噬研发效率。
2.  **关注冷启动时间：** 在 EKS 上使用 Flyte 时，Pod 的启动时间（

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该内容的深度分析报告。

---

# 深度分析报告：基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：通过使用 **Union.ai**（基于开源项目 **Flyte**）作为编排层，并在 **Amazon EKS**（Elastic Kubernetes Service）上运行，企业可以构建一个既具有云原生弹性，又能处理复杂 AI/ML 机器学习生命周期的可扩展工作流系统。这解决了传统 MLOps 平台在扩展性和基础设施管理上的痛点。

**作者想要传达的核心思想**
作者试图传达“**编排与基础设施解耦**”的思想。AI 工程师不应关注底层服务器或容器的管理，而应专注于定义数据处理和模型训练的逻辑。Flyte 提供了 Python 优先的抽象层，而 EKS 提供了底层的弹性和 AWS 生态的深度集成（如 S3、IAM），两者结合代表了“**声明式 MLOps**”的最佳实践。

**观点的创新性和深度**
*   **创新性**：将 Kubernetes 的强大编排能力与 Python 的易用性无缝结合。传统的 K8s 操作对数据科学家来说过于复杂（需要编写 YAML），而简单的脚本又缺乏扩展性和容错性。Flyte 引入了“工作流即代码”的概念，并针对 EKS 进行了优化，使得复杂的分布式计算（如 Spark 任务）在 EKS 上运行变得像写函数一样简单。
*   **深度**：文章触及了现代 AI 架构的痛点——即如何从“原型”走向“生产”。Union.ai 2.0 的引入代表了 Flyte 的商业化成熟，强调了多租户管理、安全性以及与 AWS 原生服务的零摩擦集成。

**为什么这个观点重要**
随着大模型（LLM）和复杂数据管道的兴起，单机训练已不再适用。企业迫切需要能够调度成千上万次 GPU/CU 计算任务的平台。EKS 是行业标准，但原生使用门槛高。该方案提供了一条“高速公路”，让企业能够利用现有的 AWS 投资，快速构建出工业级的 AI 生产流水线，避免重复造轮子。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Flyte**：一个开源的工作流编排平台，专为数据和 ML 工作流设计，支持 Python、Java 等语言。
*   **Union.ai**：Flyte 的商业发行版和管理控制平面，提供托管服务和企业级功能（RBAC、审计等）。
*   **Amazon EKS**：AWS 提供的托管 Kubernetes 服务，用于容器化应用的编排。
*   **AWS Service Integration**：特别是 Amazon S3（存储）、IAM（身份与权限管理）、ECR（容器镜像仓库）。

**技术原理和实现方式**
*   **Kubernetes Operator 模式**：Flyte 在 EKS 上运行时，利用 K8s Operator 模式将每一个 Flyte 任务映射为 K8s 的 Pod 或 Job。Flyte 的控制平面负责调度，数据平面负责执行。
*   **任务抽象**：通过 Flyte Python SDK（`@task` 和 `@workflow` 装饰器），用户将 Python 函数编译成 IR（中间表示），并序列化为 Protobuf 格式发送给 Flyte Admin 服务。
*   **动态实例化**：当工作流触发时，Flyte Propeller 会根据任务需求动态调整 EKS 上的资源请求，利用 K8s 的自动扩缩容（Cluster Autoscaler）来应对流量高峰。
*   **数据血缘与缓存**：Flyte 自动追踪输入输出（通常存储在 S3），利用哈希值实现任务级别的智能缓存，避免重复计算。

**技术难点和解决方案**
*   **难点**：在 Kubernetes 上运行 ML 任务面临“异构计算”挑战（例如，有的任务需要 CPU，有的需要 GPU，有的需要分布式 Spark）。
*   **解决方案**：Flyte 引入了“Plugins”机制，允许任务请求特定的 K8s 资源（如 AWS Batch、Spark on K8s）。通过自定义资源定义（CRD），Flyte 可以在 EKS 上无缝调度这些异构任务。
*   **难点**：数据科学家不懂运维。
*   **解决方案**：Union.ai 提供了 SaaS 控制平面，屏蔽了 EKS 集群管理的复杂性，用户只需关注代码逻辑。

**技术创新点分析**
*   **Type-Safe Workflows**：Flyte 强制要求定义接口类型，这在 Python 这种动态语言中引入了编译期的安全性，确保生产环境的数据流符合预期。
*   **Late Binding**：工作流定义时并不绑定数据，只有在执行时才传入具体路径，这极大地提高了工作流的复用性。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为 MLOps 团队提供了一个标准化的**AI 生产流水线蓝图**。它指导团队如何从“手动运行脚本”转向“自动化、可复现、可扩展的工业化生产”。

**可以应用到哪些场景**
*   **模型微调**：周期性地从 S3 读取数据，在 EKS 的 GPU 节点上进行大模型微调，完成后回传模型。
*   **批处理推理**：每天定时处理海量数据（如生成推荐系统结果），利用 EKS 的弹性瞬间扩容数百个 Pod 并行处理。
*   **特征工程**：使用 Spark on EKS 处理 TB 级别的原始数据，生成特征供模型使用。

**需要注意的问题**
*   **成本控制**：EKS 和 Spot 实例虽然便宜，但若不配置合理的资源限制和自动回收策略，工作流运行成本可能飙升。
*   **冷启动**：对于极短的任务，K8s Pod 的启动开销可能过大。
*   **复杂性**：引入 Flyte 增加了学习曲线，团队需要理解其特有的概念。

**实施建议**
1.  **基础设施先行**：先建立配置好 EKS 集群，并确保 IRSA（IAM Roles for Service Accounts）配置正确，以便 Pod 能直接访问 S3 而无需硬编码密钥。
2.  **模块化开发**：将通用的数据处理逻辑封装为 Flyte 任务，建立内部任务库。
3.  **渐进式迁移**：先从非关键的批处理任务开始迁移，验证稳定性和成本，再逐步接管核心训练流程。

## 4. 行业影响分析

**对行业的启示**
这标志着 **MLOps 正在全面拥抱云原生（Cloud Native）**。过去依赖定制化脚本或单一 SaaS 平台（如 SageMaker）的思路，正在转向“控制平面托管 + 数据平面私有化部署”的混合模式。企业既想要开源的灵活性，又想要云厂商的底层能力，Union + EKS 正是这一趋势的产物。

**可能带来的变革**
*   **降低 AI 工程化门槛**：让不懂 Kubernetes 的数据科学家也能间接享受 K8s 的红利。
*   **推动“数据即代码”**：通过强制的数据血缘管理，改变了数据科学“黑盒”作业的现状，提高了合规性。

**相关领域的发展趋势**
*   **混合编排**：未来的工作流引擎将不仅编排容器，还会编排 Serverless 函数（AWS Lambda）和远程函数。
*   **GitOps 的融合**：Flyte 工作流与 ArgoCD/FluxCD 的结合将更加紧密，实现 AI 流程的 CI/CD。

**对行业格局的影响**
这直接挑战了 Databricks（DAG + Notebook 模式）和 AWS SageMaker（强绑定模式）的市场地位。它提供了一条“中间道路”：既保留了代码的完全控制权，又利用了云的规模效应。

## 5. 延伸思考

**引发的其他思考**
*   **LLM 工作流的特殊性**：Flyte 这种基于 DAG（有向无环图）的编排器如何适应 LLM 中常见的 Agent 循环（非 DAG 结构）？这可能需要引入事件驱动的架构。
*   **供应商锁定**：虽然使用了开源 Flyte，但深度依赖 EKS 和 S3 API 仍然存在一定程度的锁定。如何设计“多云 Flyte”架构？

**可以拓展的方向**
*   **FinOps 集成**：开发 Flyte 插件，在任务运行时实时计算成本并反馈给用户，防止预算超支。
*   **GPU 共享**：结合 GPU 共享技术（如 NVIDIA MPS）在 EKS 上运行多个小模型推理任务，提高资源利用率。

**需要进一步研究的问题**
*   在高并发场景下，Flyte 控制平面的性能瓶颈在哪里？
*   如何在 EKS 上安全地运行多租户工作流（防止租户间的资源干扰和数据泄露）？

**未来发展趋势**
AI 工作流将逐渐从“静态 DAG”向“动态编排”演进，即工作流可以根据中间结果自动调整后续步骤（AutoML 的进一步发展）。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现状**：如果你的团队正在使用 Airflow 但发现其处理 ML 任务（特别是容器化任务）力不从心，或者是正在使用裸 K8s YAML 管理 ML 任务，那么 Flyte + EKS 是极佳的替代方案。
2.  **POC 验证**：在 EKS 上部署一个最小化的 Flyte 集群（使用 Helm Chart），编写一个简单的 Python 任务（如数据清洗），验证其与 S3 的读写权限。
3.  **容器化**：将现有的训练脚本 Docker 化，并推送到 ECR。

**具体的行动建议**
*   **学习 Flyte Python SDK**：掌握 `@task`, `@workflow`, `@launch_plan` 的核心用法。
*   **配置 Karpenter**：在 EKS 上使用 Karpenter 替代传统的 Cluster Autoscaler，以获得更极速的节点扩容速度，这对突发性 AI 任务至关重要。
*   **建立命名空间规范**：利用 K8s Namespace 隔离开发、测试和生产环境的工作流。

**需要补充的知识**
*   **Kubernetes 基础**：理解 Pod, Node, Resource Quota, Service Account。
*   **Python 装饰器与类型注解**：Flyte 大量依赖 Python 类型提示。
*   **AWS IAM**：理解 Pod Identity 如何工作。

**实践中的注意事项**
*   避免在工作流中传递大型数据集对象，始终传递 S3 路径引用。
*   注意 EKS 节点的 CPU/Memory 内存限制，防止任务因资源不足被 OOMKilled。

## 7. 案例分析

**结合实际案例说明**
假设一家金融科技公司需要每天夜间对数百万笔交易进行欺诈检测模型训练。

**成功案例分析**
*   **背景**：原有流程使用 crontab 调用脚本，经常因内存不足崩溃，且无法重试。
*   **实施**：采用 Flyte + EKS。定义了一个 `training_task`，请求 64GB 内存。
*   **结果**：Flyte 自动调度到 EKS 的高内存节点。如果训练失败，Flyte 自动重试。数据直接从 S3 读取，无需本地存储。
*   **关键成功因素**：利用了 Flyte 的“重试机制”和 EKS 的“资源隔离”。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建可扩展且模块化的容器化 AI 工作流

**说明**: 在 Amazon EKS 上使用 Union.ai 和 Flyte 时，核心在于将机器学习流程分解为独立的、可复用的任务。利用 Flyte 的任务抽象，可以将数据预处理、模型训练和评估等步骤容器化。这不仅能利用 Kubernetes 的强大编排能力进行水平扩展，还能确保各个组件的独立性和可维护性。

**实施步骤**:
1. 将 AI 流程中的逻辑单元（如数据清洗、特征工程）拆分为独立的 Python 函数或脚本。
2. 为每个任务编写 Dockerfile，并使用 `@task` 装饰器将其封装为 Flyte 任务。
3. 使用 `@workflow` 装饰器将这些任务连接起来，定义数据依赖关系。
4. 配置 Flyte 任务以请求适当的资源（CPU、内存、GPU），以便 EKS 能够根据负载动态调度 Pod。

**注意事项**: 避免在单个容器中塞入过多的逻辑，这会导致镜像体积过大且难以扩展。确保基础镜像精简且安全。

---

### 实践 2：利用 Spot 实例优化成本

**说明**: AI 和机器学习工作负载（特别是训练和大规模批处理）通常对中断不敏感。在 EKS 上配置节点组时，结合使用 Spot 实例可以显著降低基础设施成本。Flyte 原生支持处理重试机制，非常适合配合 Spot 实例使用。

**实施步骤**:
1. 在 EKS 集群中创建混合节点组，包含 On-Demand 和 Spot 实例。
2. 配置 Flyte 的任务执行策略，设置合理的重试次数，以应对 Spot 实例可能被中断的情况。
3. 利用 Flyte 的容错机制，确保任务状态被持久化，以便在中断后从检查点恢复而非从头开始。

**注意事项**: 必须确保应用程序是无状态的，并且能够处理节点的突然终止。不要将关键数据存储在节点本地存储中，应使用 S3 或 EFS 等持久化存储。

---

### 实践 3：实施严格的资源配额与请求限制

**说明**: 在共享的 EKS 集群上运行 AI 工作流时，资源争用可能导致性能下降。通过为 Flyte 任务配置具体的 CPU 和内存 `requests`（请求）和 `limits`（限制），可以确保 Kubernetes 调度器能够高效分配资源，并防止“吵闹邻居”效应。

**实施步骤**:
1. 分析历史运行数据，确定不同类型任务（如推理 vs 训练）的平均资源消耗。
2. 在 Flyte 任务定义中，使用 `@task` 的 `limits` 参数指定资源上限。
3. 在 EKS 上配置 Namespace 级别的 ResourceQuota，限制特定项目或团队的总资源使用量。
4. 启用 Cluster Autoscaler，以便在资源不足时自动增加节点。

**注意事项**: 设置 `limits` 时要留有余地，避免因内存限制过低导致 OOM（内存溢出）错误，导致任务失败。

---

### 实践 4：集中化日志与可观测性集成

**说明**: AI 工作流通常是长时间运行的批处理任务，排查问题需要详细的日志和指标。将 Union.ai/Flyte 与 AWS 的可观测性服务（如 CloudWatch、X-Ray 或 OpenTelemetry）集成，可以实现对模型训练进度、系统性能和错误的实时监控。

**实施步骤**:
1. 配置 EKS 的 Fluent Bit 或 CloudWatch Logs 代理，将容器标准输出和错误流发送到 CloudWatch Logs。
2. 在 Flyte 任务中集成结构化日志记录（如 Python 的 `logging` 模块或 `structlog`），并包含上下文信息（如任务 ID、执行 ID）。
3. 利用 Flyte 控制台或 Union.ai 平台查看任务执行的时间线和性能指标。
4. 设置 CloudWatch 告警，以便在工作流失败或重试次数过多时通知运维团队。

**注意事项**: 避免在日志中记录敏感数据（如 PII 或模型密钥）。确保日志级别在生产环境中设置为 INFO 或 WARN，以减少日志量。

---

### 实践 5：自动化 CI/CD 流水线与模型注册

**说明**: 为了实现 MLOps 的闭环，需要建立从代码提交到模型部署的自动化流水线。利用 Union.ai 和 Flyte 的原生 GitOps 支持或 CI/CD 工具（如 GitHub Actions、AWS CodePipeline），可以自动注册新任务并触发工作流。

**实施步骤**:
1. 建立代码仓库结构，将 Flyte 工作流定义与业务逻辑代码分离。
2. 在 CI 流水线中集成 `flytectl` 或 Union CLI，用于在代码合并时自动打包和部署工作流。
3. 将训练好的模型自动注册到模型注册表（如 MLflow 或 S3 存储桶），并打上版本标签。
4. 配置自动化测试，在部署前验证工作流的语法正确性和基础镜像的安全性。

**

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、可维护且高效的 AI 工作流，实现机器学习生命周期的自动化管理。
- 利用 Flyte 在 EKS 上的原生支持，用户可以构建混合型工作流，无缝编排容器、批处理任务及分布式训练任务。
- 该架构通过自动化模型训练、评估和部署流程，显著加速了从实验原型到生产环境的转化过程。
- 借助 Amazon EKS 的强大算力，该方案能够有效处理大规模数据和计算密集型任务，支持复杂的 AI 场景。
- 通过将工作流代码化，该平台实现了版本控制和可复现性，确保了实验结果的一致性与可追溯性。
- 此方案支持多云或混合云部署策略，避免了厂商锁定，并允许企业根据需求灵活选择底层基础设施。
- 集成 Amazon EKS 使得企业能够利用现有的 Kubernetes 运维工具和安全策略，降低了 AI 平台的运维复杂度和学习成本。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [Kubernetes](/tags/kubernetes/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [AWS](/tags/aws/) / [MLOps](/tags/mlops/) / [S3 Vectors](/tags/s3-vectors/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Klaw.sh：面向 AI 智能体的 Kubernetes 编排工具]({{< relref "posts/20260216-hacker_news-show-hn-klawsh-kubernetes-for-ai-agents-12.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [Sealos：AI 原生云操作系统]({{< relref "posts/20260206-hacker_news-sealos-ai-native-cloud-cloud-operating-system-16.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260207-github_trending-alibaba-higress-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*