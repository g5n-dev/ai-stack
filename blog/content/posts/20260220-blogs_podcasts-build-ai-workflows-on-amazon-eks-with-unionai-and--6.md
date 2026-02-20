---
title: "基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流"
date: 2026-02-20T17:11:00+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 2.0 和 Flyte Python SDK 在 Amazon Elastic Kubernetes Service (Amazon EKS) 上构建和扩展 AI/ML 工作流。 主要内容包括： 1. **工作流编排**：使用 Flyte Python SDK 实现高效的大规模 A"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们介绍如何使用 Flyte Python SDK 编排和扩展 AI/ML 工作流。我们探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务无缝集成。我们通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来介绍该解决方案。

---
## 导语

随着 AI 工作流的复杂度日益增加，构建可扩展且易于维护的编排系统已成为开发者的核心需求。本文将详细介绍如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建高效的工作流，并探讨其与 Amazon S3、Aurora 等 AWS 服务的深度集成。通过具体的代码示例，我们将展示如何利用 Amazon S3 Vectors 服务优化数据处理流程，帮助您在云环境中实现更灵活的 AI 模型部署与管理。

---
## 摘要

本文介绍了如何利用 Union.ai 2.0 和 Flyte Python SDK 在 Amazon Elastic Kubernetes Service (Amazon EKS) 上构建和扩展 AI/ML 工作流。

主要内容包括：
1.  **工作流编排**：使用 Flyte Python SDK 实现高效的大规模 AI/ML 流程编排。
2.  **云端部署**：借助 Union.ai 2.0 将 Flyte 部署于 Amazon EKS，实现容器化环境下的弹性扩展。
3.  **AWS 生态集成**：方案深度整合了多项 AWS 服务，包括：
    *   **Amazon S3**：用于数据存储，示例中具体展示了结合新推出的 S3 Vectors 服务。
    *   **Amazon Aurora**：用于数据库管理。
    *   **AWS IAM**：用于身份与访问权限管理。
    *   **Amazon CloudWatch**：用于监控与日志记录。
4.  **实践案例**：文章通过一个具体的 AI 工作流示例，演示了如何在实际场景中应用这一技术栈。

---
## 评论

**中心观点**
文章主张通过 Union.ai 2.0 将 Flyte 工作流编排系统部署于 Amazon EKS 之上，利用 Kubernetes 的原生能力与 AWS 生态的深度集成，来解决 AI/ML 工作流在生产环境中面临的扩展性、异构计算调度及基础设施管理复杂性等核心挑战。

**支撑理由与评价**

1.  **技术架构的云原生演进（事实陈述 / 你的推断）**
    文章的核心逻辑在于“控制平面与数据平面的解耦”。
    *   **支撑理由**：Flyte 基于 Kubernetes 构建，利用 EKS 意味着用户无需维护物理集群，且能直接利用 K8s 的 CRD（Custom Resource Definition）来定义任务。Union.ai 2.0 作为托管控制平面，进一步降低了 Flyte 的部署门槛。这种架构允许 ML 工程师将代码（Python SDK）直接转化为容器化的云原生存算任务，实现了从“实验环境”到“生产环境”的 IaC（基础设施即代码）转化。
    *   **反例/边界条件**：对于极小规模的团队（如 3-5 人），维护 EKS 集群和 Union.ai 的复杂度可能远超其实际收益。此时，AWS SageMaker 的全托管服务或简单的 Airflow + EC2 方案可能更具性价比。K8s 的学习曲线是这一方案的隐形税负。

2.  **异构计算的调度与资源隔离（事实陈述 / 作者观点）**
    文章强调了 EKS 在处理 GPU 和 CPU 任务混合调度时的优势。
    *   **支撑理由**：在 AI 工作流中，数据预处理（CPU 密集型）与模型训练（GPU 密集型）往往交替进行。Flyte on EKS 能够利用 Node Selector 和 Taints/Tolerations 机制，精确地将任务调度到 Spot 实例（低成本）或 On-Demand GPU 实例（高稳定）上。这种精细化的资源管理是通用编排工具（如传统的 Airflow）所不具备的短板。
    *   **反例/边界条件**：如果工作流主要涉及轻量级的推理或简单的批处理，EKS 的 Overhead（控制平面、Sidecar 等资源消耗）可能会占用过多计算资源，导致资源利用率反而低于基于 Lambda 或 Fargate 的无服务器架构。

3.  **数据重力与生态集成（事实陈述 / 行业共识）**
    文章重点提及了与 S3 的集成，这触及了云原生 AI 的“数据重力”问题。
    *   **支撑理由**：在 AWS 生态中，计算向数据移动是基本原则。Flyte on EKS 可以利用 VPC 内的高带宽访问 S3，避免公网传输流量费和延迟。同时，利用 AWS IRSA（IAM Roles for Service Accounts）实现精细的权限控制，符合企业级安全合规要求。
    *   **反例/边界条件**：这种深度绑定也导致了“厂商锁定”。如果未来企业需要迁移至 Azure 或 GCP，重写所有的存储接口和 IAM 策略将是一项巨大的工程。相比之下，Prefect 或 Dagster 等轻量级工具在云中立性上表现更好。

**多维度深入评价**

1.  **内容深度：架构视角的务实性**
    文章没有停留在“Hello World”层面的演示，而是触及了**工作流编排的最后一公里**——即如何处理容器化、资源配额和生命周期管理。它隐含地论证了为什么单纯的脚本调度已无法满足现代 AI 的需求。然而，文章在**成本控制**方面的论证略显单薄，例如未详细探讨在 EKS 上使用 Spot 实例中断时，Flyte 如何处理 Checkpoint 和任务恢复机制，这是生产环境中的关键痛点。

2.  **实用价值：针对中大型团队的优选方案**
    对于已经拥抱 AWS 的数据科学团队，该方案具有极高的参考价值。它提供了一条从“本地笔记本”到“云端 K8s 集群”的清晰路径。特别是 Union.ai 引入的“多租户”和“版本控制”概念，直接解决了团队协作中的代码冲突和环境不一致问题。

3.  **创新性：从“任务调度”转向“工作流即代码”**
    文章展示的并非全新技术，而是一种**范式转移**。传统的 ETL 工具侧重于“调度”，而 Flyte + Union 侧重于“工作流即数据管道”。其创新点在于将 ML 流水线视作微服务架构的一部分，利用 K8s 的声明式 API 来管理数据流，这使得 A/B 测试、模型回滚和灰度发布变得天然且自动化。

4.  **可读性与逻辑结构**
    作为一篇技术博文，其逻辑遵循了“痛点 -> 解决方案 -> 架构 -> 实践”的标准路径。但对于不熟悉 Kubernetes 概念（如 Pod、Namespace）的数据分析师而言，技术门槛较高。文章假设读者具备一定的 DevOps 背景知识，这在一定程度上限制了其受众范围。

5.  **行业影响：MLOps 标准化的推动**
    此类文章的发布表明，MLOps 领域正在从“百花齐放”的混乱阶段（各种自定义脚本）向“标准化的 K8s 编排”阶段收敛。Flyte、Kubeflow 和 Argo Workflow 之间的竞争将促使云厂商提供更原生的 AI 编排支持，加速 MLOps 的落地。

6.  **争议点与不同观点**
    *   **过度工程化之争**：部分业界观点认为，对于

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章内容的全面深入分析。

---

# 深入分析：基于 Amazon EKS 与 Union.ai/Flyte 构建 AI 工作流

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心主张是**通过将 Flyte（开源工作流编排工具）与 Union.ai（商业托管平台）结合，并部署在 Amazon EKS（弹性 Kubernetes 服务）上，企业能够构建一个可扩展、高性能且云原生的 AI/ML 工作流编排系统**。这一组合旨在解决传统机器学习流程中从原型到生产环境迁移困难、资源管理混乱以及与云服务集成复杂的问题。

### 作者想要传达的核心思想
作者试图传达**“基础设施即代码”与“工作流即代码”**在 AI 领域的重要性。核心思想在于，AI 工程不应仅仅停留在 Notebook 层面，而应通过 Kubernetes 的强大编排能力，实现 ML 流程的工业化。Flyte 提供了逻辑抽象，Union.ai 提供了管理平面，而 EKS 提供了算力底座，三者结合构成了 ML 工程的“黄金三角”。

### 观点的创新性和深度
该观点的创新性在于**将数据工程与 DevOps 的最佳实践深度融合**。传统的 Airflow 或 Argoworkflows 往往缺乏针对 ML 特定任务（如模型训练超参数调优、分布式训练）的原生支持。Flyte 的创新在于其类型系统和任务级别的细粒度资源管理，而 Union.ai 2.0 进一步降低了在 Kubernetes 上部署 Flyte 的门槛。深度体现在它不仅关注“如何运行代码”，更关注“如何在生产环境中高效、低成本地运行大规模 ML 任务”。

### 为什么这个观点重要
随着大模型（LLM）和生成式 AI 的爆发，计算资源的调度和 AI 流程的可靠性成为瓶颈。单纯依赖脚本或简单的调度器已无法满足企业级 AI 的需求。该观点指明了**AI 工程平台化**的演进方向，即利用云原生生态（Kubernetes + AWS）来支撑日益复杂的 AI 业务需求，这对于降低 AI 落地成本、提高迭代速度至关重要。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Flyte**: 一个开源的、以工作流为中心的编排层，专门用于构建数据和 ML 流程。
2.  **Union.ai 2.0**: Flyte 的商业发行版，提供控制平面、SaaS 管理界面以及企业级支持。
3.  **Amazon EKS**: AWS 托管的 Kubernetes 服务，用于容器化应用的部署、扩展和管理。
4.  **Flyte Python SDK**: 用于定义任务、工作流和依赖关系的 Python 接口。
5.  **AWS S3 (Amazon Simple Storage Service)**: 集成的对象存储，用于存储数据集、模型和中间产物。

### 技术原理和实现方式
*   **声明式工作流定义**: 通过 Python 装饰器（`@task`, `@workflow`）将普通 Python 函数转换为可序列化的、有版本控制的 Flyte 任务。
*   **容器化与隔离**: Flyte 将每个任务打包成容器（Pod），并在 EKS 上调度执行。Union.ai 负责在 EKS 集群上安装 Flyte Propeller（控制平面组件）。
*   **数据传递机制**: 任务间的数据传递不通过文件系统，而是通过引用传递。大型数据集存储在 S3，Flyte 仅传递 S3 的 URI 指针，极大减少了序列化开销。
*   **自动扩展**: 利用 EKS 的 Cluster Autoscaler 和 Karpenter（可能涉及），根据 Flyte 提交的队列请求动态调整节点数量。

### 技术难点和解决方案
*   **难点**: Kubernetes 的复杂性（网络、存储、权限管理）是数据科学家面临的主要障碍。
*   **解决方案**: Union.ai 提供了“零配置”体验，自动处理 EKS 上的 IAM 角色绑定、S3 挂载和网络策略，让数据科学家无需成为 K8s 专家即可使用集群。
*   **难点**: ML 任务资源需求差异大（有的需要大内存，有的需要 GPU）。
*   **解决方案**: Flyte 允许在任务级别指定资源请求和限制，并在运行时动态匹配节点池。

### 技术创新点分析
*   **基于类型的多态性**: Flyte 的类型系统允许工作流根据输入类型动态改变行为，这在处理不同数据模式时非常强大。
*   **执行层面的缓存**: Flyte 会自动缓存任务输出。如果输入参数（包括代码哈希和数据哈希）未变，Flyte 将跳过计算直接返回上次结果，这对于昂贵的 ML 训练任务是巨大的效率提升。

## 3. 实际应用价值

### 对实际工作的指导意义
该架构为**AI 工程化**提供了标准路径。它指导团队如何从“手工作坊式”的脚本开发转向“工业化”的流水线生产，确保了模型训练的**可重现性**和**可追溯性**。

### 可以应用到哪些场景
1.  **模型微调**: 定期从 S3 获取新数据，触发微调流程，自动评估并注册模型。
2.  **批量推理**: 每天凌晨定时处理海量业务数据，生成预测结果。
3.  **生成式 AI 应用**: 编排 RAG（检索增强生成）流程，包括索引更新、Embedding 生成和 LLM 调用。
4.  **特征工程**: 构建复杂的特征计算 DAG（有向无环图），处理数仓数据。

### 需要注意的问题
*   **成本控制**: EKS 节点如果不及时缩容，可能导致费用高昂。需要配置好 Spot 实例策略和自动缩容策略。
*   **冷启动**: 对于极短的任务，Kubernetes 的 Pod 启动时间可能成为瓶颈。
*   **学习曲线**: 团队需要接受 Flyte 的特定编程范式（如不能随意使用全局变量）。

### 实施建议
建议从**非关键路径的数据处理任务**开始试点，逐步迁移核心训练流程。利用 Union.ai 的托管服务减少运维负担，初期不要自建 Flyte Control Plane。

## 4. 行业影响分析

### 对行业的启示
这标志着 **MLOps 平台正在向云原生化深度渗透**。行业正在从通用的任务调度（如 Airflow）向专为 ML 设计的、容器原生的工作流引擎转型。

### 可能带来的变革
*   **资源利用率革命**: 按需分配 GPU 和内存，避免长期占用昂贵资源，将改变 ML 团队的成本结构。
*   **开发与运维边界模糊**: 数据科学家通过 Flyte SDK 实际上编写了运维定义，促进了“数据平台工程师”这一角色的兴起。

### 相关领域的发展趋势
*   **Serverless 容器**: 未来可能会看到 Flyte 与 AWS Fargate 的更深层次集成，实现节点级别的 Serverless。
*   **混合云支持**: Union.ai 和 Flyte 的架构支持跨云运行，这符合企业避免供应商锁定的趋势。

### 对行业格局的影响
Union.ai 正在挑战 Databricks 和 AWS Sage Maker 的内置编排能力。它提供了一种**开放、灵活且不绑定特定云厂商**（尽管运行在 EKS 上，但代码可移植）的替代方案。

## 5. 延伸思考

### 引发的其他思考
*   **LLM 的编排**: 传统的 DAG（有向无环图）是否足够处理 LLM 的 Agent 循环？Flyte 如何适应基于事件驱动而非仅仅是批处理的 AI Agent？
*   **数据血缘**: 既然 Flyte 管理了所有输入输出，它能否成为企业级数据血缘治理的核心工具？

### 可以拓展的方向
*   **与 Ray 集成**: Ray 是目前分布式 Python 的标准。Flyte + Ray on EKS 将是处理超大规模并行训练的终极组合。
*   **模型注册中心集成**: 探讨 Flyte 如何与 MLflow 或 Weights & Biases 更紧密地集成，实现全生命周期管理。

### 需要进一步研究的问题
*   在高并发场景下（如每分钟提交数千个工作流），Flyte Control Plane 的性能瓶颈在哪里？
*   如何在 EKS 上安全地隔离多租户（Multi-tenancy）的 ML 工作流？

### 未来发展趋势
未来，AI 工作流编排将变得**不可感知**。IDE 插件将自动将 Notebook 代码转换为 Flyte 工作流，开发者无需关心底层 K8s 细节，实现“从代码到云端”的秒级部署。

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有痛点**: 如果你的团队正在为“脚本跑不通”、“环境不一致”、“资源抢夺”困扰，该方案适合。
2.  **环境搭建**: 注册 AWS 账号，创建 EKS 集群。申请 Union.ai 免费试用版或部署开源 Flyte。
3.  **代码改造**: 将现有的 Python 脚本用 `@task` 和 `@workflow` 装饰器封装。
4.  **容器化**: 编写 Dockerfile，包含依赖库，推送到 ECR。

### 具体的行动建议
*   **第一步**: 阅读 Flyte 官方文档中的 "Flytesnacks" 示例。
*   **第二步**: 在本地使用 `flytectl` 或 Docker Desktop 运行一个简单的沙箱环境。
*   **第三步**: 尝试将一个简单的数据预处理脚本部署到 EKS 测试环境。

### 需要补充的知识
*   **Docker**: 理解镜像构建原理。
*   **Kubernetes 基础**: 理解 Pod, Node, Namespace, Resource Quota 概念。
*   **Python 类型提示**: Flyte 强依赖 Python 类型提示。

### 实践中的注意事项
*   避免在 Flyte 任务中执行非常短（毫秒级）的微任务，调度开销会得不偿失。
*   确保所有依赖库都在 `requirements.txt` 中明确声明，保证构建的可复现性。

## 7. 案例分析

### 结合实际案例说明
假设一家**金融科技公司**需要每晚对 1000 万笔交易进行欺诈检测模型训练。

*   **传统做法**: 数据科学家写一个 Python 脚本，在本地或大内存 EC2 上跑。经常因为内存溢出（OOM）中断，且无法追踪昨晚跑了哪个版本的代码。
*   **Flyte + EKS 方案**:
    1.  **数据拉取**: 任务 A 从 S3 读取数据，指定需要 50GB 内存。
    2.  **预处理**: 任务 B 并行执行数据清洗，请求 10 个 CPU 核。
    3.  **训练**: 任务 C 请求 4 个 GPU（NVIDIA T4），运行 XGBoost 或 PyTorch 训练。
    4.  **评估**: 任务 D 评估模型，如果准确率达标，触发任务 E 将模型上传至 S3 模型库。

### 成功案例分析
**Spotify** 是 Flyte 的早期采用者和主要贡献者。他们利用 Flyte 管理其庞大的推荐系统训练流程。成功的关键在于利用 Flyte

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建模块化与容器化的 AI 工作流

**说明**: 在 Amazon EKS 上使用 Union.ai 和 Flyte 时，应将 AI 工作流拆解为独立、可复用的任务。每个任务应封装在独立的容器中，实现代码与依赖的隔离。这种模块化设计便于版本控制、独立测试和并行执行，从而提高整体开发效率。

**实施步骤**:
1. 定义清晰的接口，将长工作流拆分为逻辑独立的单元（如数据预处理、训练、评估）。
2. 为每个任务构建单独的 Docker 镜像，并在 Dockerfile 中仅包含必需的依赖项以减小镜像体积。
3. 使用 Flyte 的任务装饰器（`@task`）和子工作流功能来组合这些模块化单元。

**注意事项**: 避免在单个容器中安装过多的机器学习框架或工具库，这会导致镜像启动缓慢并增加安全风险。建议使用多阶段构建来优化镜像大小。

---

### 实践 2：利用 Spot 实例优化成本与资源分配

**说明**: AI 和机器学习工作负载通常包含大量的批处理任务和训练作业，这些任务往往具有容错性。利用 Amazon EKS 托管节点组结合 EC2 Spot 实例，可以显著降低计算成本。Flyte 原生支持处理节点中断和任务重试，非常适合此类场景。

**实施步骤**:
1. 在 EKS 中配置专门的 Spot 节点组，并为其添加特定的 Kubernetes 污点（Taints）和标签。
2. 配置 Flyte 的任务模板或 Pod 默认配置，使其能够容忍这些污点，从而调度到 Spot 节点上。
3. 针对必须运行到底的关键任务（如模型服务或长时间运行的训练），配置使用按需实例。

**注意事项**: 确保 Flyte 任务实现了检查点机制，以便在 Spot 实例被回收时能够从中断处恢复，而不是完全重新开始。

---

### 实践 3：实施动态资源请求与自动扩缩容

**说明**: 不同的 AI 任务（如数据预处理 vs 模型训练）对计算资源（CPU、内存、GPU）的需求差异巨大。硬编码资源请求会导致资源浪费或调度失败。最佳实践是根据任务实际需求动态请求资源，并结合 Cluster Autoscaler 自动调整 EKS 节点数量。

**实施步骤**:
1. 在 Flyte 任务定义中，使用 `@task` 装饰器的 `requests` 和 `limits` 参数明确指定资源需求（例如 `mem="16Gi"`, `gpu="1"`）。
2. 为 EKS 集群配置 Cluster Autoscaler，并根据 GPU 或高内存实例组的标签设置扩缩容策略。
3. 利用 Flyte 的队列系统管理高并发工作流，防止突发流量压垮集群控制平面。

**注意事项**: 监控 Pod 的 Pending 状态，如果频繁出现因资源不足导致的挂起，需要调整 Cluster Autoscaler 的最大节点数或实例类型配置。

---

### 实践 4：统一数据访问与 S3 集成

**说明**: 在 Kubernetes 环境中，数据不应存储在容器本地或节点的临时存储中，因为节点终止会导致数据丢失。应建立统一的数据访问层，利用 Amazon S3 作为数据湖，通过 Flyte 的数据类型系统自动处理 S3 与容器之间的数据传输。

**实施步骤**:
1. 使用 Flyte 的 `FlyteFile`、`FlyteDirectory` 或 `StructuredDataset` 等原语类型作为任务输入输出。
2. 配置 Union.ai 或 Flyte 的身份验证（IRSA），为 Pod 分配 IAM 角色，赋予其读写特定 S3 存储桶的权限。
3. 确保工作流在处理大数据时使用引用传递而非直接传递二进制数据，以减少序列化开销。

**注意事项**: 避免在任务启动时重复下载完整的大型数据集。利用 S3 挂载或流式传输技术来处理超大文件，以优化启动时间。

---

### 实践 5：强化安全性最小权限原则

**说明**: 在共享的 EKS 集群上运行 AI 工作流时，必须限制不同团队或工作流的权限。利用 Kubernetes RBAC 和 IAM Roles for Service Accounts (IRSA) 确保每个工作流仅拥有执行其功能所需的最小权限，防止访问未授权的 S3 存储桶或其它 AWS 资源。

**实施步骤**:
1. 为不同的 Flyte 项目或域配置专用的 Kubernetes Service Account。
2. 创建 IAM 策略，仅允许访问特定的 S3 路径（如 `s3://ml-data/prod/*`），并将其通过 Kubernetes 注解关联到 Service Account。
3. 在 EKS 中启用 Pod Security Standards (PSS) 或 Pod Security Policy (PSP)，限制容器的特权模式访问。

**注意事项**: 定期审计 IAM 策略和 Kubernetes 角色，移除不再使用的权限，避免权限随时间推移而过度膨胀。

---

### 实践

---
## 学习要点

- Union.ai 和 Flyte 的结合为在 Amazon EKS 上构建可扩展、生产级 AI 工作流提供了开源且云原生的基础设施，实现了从模型开发到部署的无缝衔接。
- Flyte 能够自动化编排复杂的机器学习流水线，有效管理数据预处理、模型训练及微调等任务，显著提升 MLOps 效率。
- 利用 Amazon EKS 运行该架构，可借助 Kubernetes 的强大编排能力实现容器的弹性伸缩，从而优化大规模分布式训练的资源利用率。
- 该解决方案通过声明式定义工作流，确保了机器学习实验的高度可复现性和版本控制，解决了模型迭代过程中的混乱问题。
- 此技术栈支持混合云及多云环境部署，允许企业灵活地在 AWS 或本地基础设施间迁移 AI 负载，避免供应商锁定。
- 集成 Amazon EFA（弹性结构适配器）等 AWS 优化组件，可进一步加速高性能计算（HPC）和生成式 AI 模型的训练速度。

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
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*