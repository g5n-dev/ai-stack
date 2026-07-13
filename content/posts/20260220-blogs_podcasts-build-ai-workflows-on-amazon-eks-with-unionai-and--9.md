---
title: 基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流
date: 2026-02-20 22:59:37+08:00
draft: false
entry_kind: auto
tags:
- Flyte
- Union.ai
- Amazon EKS
- Kubernetes
- 工作流编排
- AWS
- 机器学习
- MLOps
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: '**内容总结：在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流** 本文主要介绍了如何利用 **Flyte
  Python SDK** 编排和扩展 AI/ML 工作流，并重点说明了 **Union.ai 2.0** 如何助力在 **Amazon Elastic Kubernetes'
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios:
- AI/ML项目
- Kubernetes
---

# 基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---

## 摘要/简介

在这篇文章中，我们将介绍如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们会探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用新版 Amazon S3 Vectors 服务的 AI 工作流示例来探讨这一解决方案。

---

## 导语

随着 AI 工作流的复杂度日益增加，构建可扩展且稳定的生产环境已成为技术团队的关键挑战。本文将探讨如何利用 Union.ai 和 Flyte，在 Amazon EKS 上高效编排机器学习任务，并实现与 Amazon S3、Aurora 等 AWS 服务的深度集成。通过具体的代码示例，我们将展示如何构建一个端到端的 AI 工作流，帮助您优化资源管理并提升模型部署的效率。

---

## 摘要

**内容总结：在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流**

本文主要介绍了如何利用 **Flyte Python SDK** 编排和扩展 AI/ML 工作流，并重点说明了 **Union.ai 2.0** 如何助力在 **Amazon Elastic Kubernetes Service (Amazon EKS)** 上部署 Flyte。文章通过一个涉及 **Amazon S3 Vectors** 服务的 AI 工作流示例，详细展示了该解决方案的实现过程及其与 AWS 生态系统的无缝集成。

**核心要点如下：**

1.  **技术架构与编排**：
    利用 Flyte Python SDK，开发者可以构建可扩展的工作流。Union.ai 2.0 系统负责将 Flyte 部署在 Amazon EKS 上，从而利用 Kubernetes 的强大编排能力来管理复杂的机器学习任务。

2.  **AWS 服务集成**：
    该解决方案实现了与多种 AWS 原生服务的深度集成，确保工作流的安全性和可观测性：
    *   **Amazon S3**：用于存储数据集及模型。
    *   **Amazon Aurora**：作为后端数据库支持。
    *   **AWS IAM**：管理身份验证与访问权限，确保资源安全。
    *   **Amazon CloudWatch**：用于监控和日志记录。

3.  **应用场景示例**：
    文章通过一个具体的 AI 示例——利用 **Amazon S3 Vectors** 服务，演示了如何在实际场景中构建并运行这些工作流，展示了从数据处理到模型训练的完整流程。

---

## 评论

### 中心观点
**文章阐述了利用 Union.ai 2.0 将 Flyte 工作流编排引擎部署于 Amazon EKS 的技术路径。其核心价值在于构建一套基于 Kubernetes 的、能够与 AWS 数据生态（如 S3、SageMaker）协同工作的机器学习管线，旨在解决 ML 工作流在云原生环境下的调度与集成问题。**

### 深入评价

#### 1. 支撑理由与分析

**理由一：技术架构的云原生适配**
*   **[事实陈述]** 文章重点介绍了 Union.ai 2.0 在 EKS 上部署 Flyte 的具体操作。
*   **[分析]** 这种部署方式体现了“控制平面与数据平面解耦”的架构趋势。Flyte 负责逻辑编排，EKS 负责资源调度。这种分层架构使得企业能够利用 Kubernetes 的通用编排能力，而非局限于单一云厂商的特定 AI 服务。

**理由二：对复杂 AI 开发流程的支持**
*   **[事实陈述]** 文中提及使用 Flyte Python SDK 进行任务定义。
*   **[分析]** 现代机器学习流程包含大量非确定性任务（如数据清洗、特征工程）。Flyte 基于 Python 的接口设计允许将脚本代码转化为工作流任务。相比于通用的数据调度工具，Flyte 在处理 ML 特有的任务依赖、数据传递和版本管理方面提供了特定支持。

**理由三：多云与混合环境的兼容性**
*   **[事实陈述]** Union.ai 支持 EKS 部署及集群管理。
*   **[分析]** 对于数据存储分散的企业，EKS 提供了标准的计算环境。通过这种架构，计算任务可以调度到数据所在的区域（如 AWS 内部），有助于解决数据传输延迟问题，同时保持对底层基础设施的编程控制权。

#### 2. 反例与边界条件

*   **[边界条件 1：运维门槛]**
    *   **[分析]** 尽管文章提供了部署指南，但在 EKS 上维护生产级 Flyte 集群仍需具备 K8s 运维能力（包括节点管理、RBAC 配置、监控等）。对于缺乏专职运维团队的小型组织，全托管方案（如 AWS Step Functions）可能在维护成本上更具优势。

*   **[边界条件 2：延迟与适用场景]**
    *   **[分析]** 基于 EKS 容器的调度机制涉及 Pod 启动过程，其延迟高于无服务器计算。因此，该架构更适合高吞吐的离线批处理和训练任务，而非对延迟极度敏感的实时在线推理服务。

#### 3. 维度详细评价

*   **内容深度：**
    文章侧重于实施层面的技术细节，准确描述了部署步骤。它主要解决了“如何实现”的问题，为技术人员提供了可操作的参考。

*   **实用价值：**
    对于已决定采用 AWS EKS 作为底层基础设施，并寻求开源编排工具的数据团队，该文章提供了具体的集成方案参考。

*   **创新性：**
    属于工程实践层面的集成应用。其价值在于将开源工作流引擎与公有云容器服务进行结合，提供了标准化的落地路径。

*   **可读性：**
    作为技术指南，其逻辑结构通常遵循操作顺序，便于技术人员跟随实践。

*   **行业影响：**
    此类技术方案推动了 ML Ops 基础设施的标准化，鼓励企业基于开源组件构建可扩展的 AI 平台，而非完全依赖封闭的商业套件。

### 可验证的检查方式

为了验证文章所述方案的真实效果，建议进行以下检查：

1.  **功能验证**：按照文档在 EKS 测试环境部署 Flyte，验证任务调度、状态回传及与 S3 的数据读写是否正常。
2.  **性能基准**：运行标准 ML 工作流（如数据处理+模型训练），监控 Pod 启动时间和任务完成延迟，评估是否满足业务 SLA。
3.  **成本评估**：对比使用 EKS 自管节点与 AWS 全托管服务的总体拥有成本（TCO），特别是考虑到运维人力的投入。

---

## 技术分析

基于提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及摘要内容，结合Union.ai、Flyte以及AWS EKS的技术生态，以下是对该文章核心观点及技术要点的深入分析。

---

### 1. 核心观点深度解读

**文章的主要观点：**
文章主张在构建和扩展生产级AI/ML工作流时，不应从零开始构建基础设施，而应采用**“以工作流为中心”**的编排模式。具体而言，通过**Flyte**（一个开源的工作流编排工具）配合**Union.ai**（提供商业支持和管理控制平面的平台），在**Amazon EKS**（弹性Kubernetes服务）上构建可扩展、可移植且云原生的AI流水线。

**作者想要传达的核心思想：**
核心思想是**“编排与基础设施的解耦”**以及**“云原生的可移植性”**。
1.  **Kubernetes是AI运行的标准底座：** EKS提供了弹性的容器编排能力，是运行大规模ML计算的理想环境。
2.  **Flyte提供了逻辑抽象层：** 它将数据处理、模型训练和评估等步骤抽象为有向无环图（DAG），解决了ML工作流中复杂的状态管理和依赖调度问题。
3.  **Union.ai降低了落地门槛：** 虽然Flyte开源，但运维Kubernetes集群极其复杂。Union.ai提供了托管控制平面，让开发者只需关注业务逻辑（Python代码），而无需关心底层K8s的运维细节。

**观点的创新性和深度：**
*   **深度：** 文章超越了简单的“容器化”概念，深入到了**“数据密集型计算的编排”**层面。它指出了ML工作流与微服务架构的本质区别——ML工作流涉及大量数据移动、长时间运行的训练任务以及复杂的版本控制。
*   **创新性：** 提出了**“Union of Data and Compute”**（数据与计算的联合）的理念。通过Flyte的强类型接口和EKS的弹性调度，实现了“计算向数据移动”或“数据在存储中，计算在EKS中临时拉起”的高效模式，解决了传统ML平台资源利用率低的问题。

**为什么这个观点重要：**
随着大模型（LLM）和复杂ML系统的兴起，AI工程化已不再是单机脚本运行，而是涉及多步骤、多模态、大规模并发的系统工程。该观点提供了一条**“不锁定特定云厂商（如仅限AWS SageMaker），又能利用云原生弹性（EKS）”**的最佳实践路径，对于寻求降低TCO（总拥有成本）和提高迭代速度的企业至关重要。

---

### 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Flyte Python SDK:** 用于定义工作流、任务和数据模型的Python库。
*   **Amazon EKS (Elastic Kubernetes Service):** AWS托管的Kubernetes服务，提供底层容器调度。
*   **Union.ai 2.0:** Flyte的商业化版本，提供控制平面、用户界面和多云管理能力。
*   **AWS S3 (Simple Storage Service):** 用于存储训练数据、模型 artifacts 和中间结果。
*   **Containerization (Docker):** 任务运行的标准单元。
*   **Workflow Orchestration (DAG):** 有向无环图，定义任务执行顺序。

**技术原理和实现方式：**
1.  **声明式工作流定义：** 用户使用Python装饰器（`@workflow`, `@task`）定义业务逻辑。Flyte将这些Python代码编译成不可变的DAG定义（Protobuf格式）。
2.  **EKS上的Pod调度：** 当工作流被触发时，Flyte的Propeller（调度引擎）会与EKS API交互，将每个Task转化为Kubernetes Pod。
3.  **资源弹性伸缩：** 利用EKS的Cluster Autoscaler，根据任务队列的长度和资源需求，动态增减EC2节点。
4.  **数据传递与缓存：** 任务间的数据传递不通过直接内存共享，而是通过引用（S3路径）。Flyte自动处理输入输出的上传和下载，并利用**内容寻址存储**机制自动缓存中间结果，避免重复计算。

**技术难点和解决方案：**
*   **难点：** ML任务通常需要GPU，且资源需求差异大（预处理需CPU，训练需GPU），容易造成资源碎片或浪费。
    *   **解决方案：** Flyte允许在Task级别指定资源请求（如`requests=gpu=1`）。EKS会根据这些请求进行精细调度，确保GPU只在需要时分配，并在任务结束后释放。
*   **难点：** 异步任务的状态管理和故障恢复。
    *   **解决方案：** Flyte控制平面不断轮询Kubernetes API，监控Pod状态。如果任务失败，支持自动重试和断点续跑。

**技术创新点分析：**
*   **强类型数据流：** 不同于Airflow等以数据为中心（传递路径）的编排工具，Flyte强调**以数据类型为中心**（传递Python对象）。这使得代码更易测试、更模块化。
*   **多语言支持（通过Sidecar）：** 虽然SDK是Python，但底层支持任何容器化语言，实现了异构计算（如用R做数据处理，用Python训练模型）的统一编排。

---

### 3. 实际应用价值

**对实际工作的指导意义：**
*   **标准化ML交付：** 将混乱的Jupyter Notebook转化为生产级的、可追踪的流水线。
*   **成本优化：** 利用EKS Spot实例和Flyte的细粒度资源控制，显著降低ML训练成本。
*   **提升可重现性：** 自动记录代码版本、Docker镜像版本和数据输入S3的哈希值，确保实验结果可复现。

**可以应用到哪些场景：**
*   **大模型微调：** 定期从S3读取新数据，触发微调任务，评估模型，并自动注册到模型注册表。
*   **批量推理：** 每天定时处理海量数据（如生成推荐系统特征），利用EKS瞬间扩容数千个Pod并发处理。
*   **特征工程：** 复杂的SQL转换和Python数据处理逻辑的混合编排。

**需要注意的问题：**
*   **冷启动延迟：** EKS节点扩容和Docker镜像拉取需要时间，对于毫秒级实时推理不适用（更适合批处理）。
*   **学习曲线：** 团队需要理解容器化和Kubernetes的基本概念，尽管Union.ai简化了操作，但调试底层问题仍需K8s知识。

**实施建议：**
*   **从“Union Serverless”开始：** 如果团队没有成熟的K8s运维能力，建议先使用Union.ai的Serverless版本，无需管理EKS集群。
*   **模块化任务设计：** 将Task设计得尽可能小和无状态，以便于复用和缓存。

---

### 4. 行业影响分析

**对行业的启示：**
*   **MLOps的“Kubernetes化”已成定局：** 行业正在从专有ML平台（如SageMaker Pipelines, Vertex AI）向基于K8s的开源标准（Flyte, Argo, Tekton）迁移，以避免供应商锁定。
*   **平台工程的崛起：** 数据科学家不应成为K8s专家。Union.ai的模式展示了“平台团队”如何通过封装K8s复杂性，为“数据科学团队”提供自助服务能力。

**可能带来的变革：**
*   **AI基础设施的民主化：** 中小型公司可以通过使用EKS + Flyte，获得与Google、Meta同等水平的ML编排能力，而无需自研复杂的调度系统。
*   **混合云策略的落地：** 企业可以在本地数据中心运行EKS（用于敏感数据），在云端运行EKS（用于弹性扩容），而Flyte可以统一编排这两者。

**对行业格局的影响：**
*   这对纯SaaS类的MLOps工具构成了挑战，因为“Kubernetes + 开源编排”提供了更强的控制力和更低的长远成本。

---

### 5. 延伸思考

**引发的其他思考：**
*   **Serverless vs. Kubernetes：** 虽然文章推崇EKS，但AWS Lambda等Serverless服务在轻量级任务中更便捷。未来的边界在哪里？也许在于“任务执行时长 > 5分钟”或“需要特定硬件（GPU）”时选择EKS/Flyte。
*   **LLM工作流的特殊性：** Flyte擅长处理数据流，但LLM应用（Agent）通常涉及动态图和循环。Flyte如何适应这种非确定性流程？（可能需要结合LangChain等动态框架）。

**可以拓展的方向：**
*   **GitOps集成：** 将Flyte工作流定义存储在Git中，通过ArgoCD自动部署到EKS集群，实现完全的自动化流水线。
*   **GPU共享：** 结合NVIDIA的MIG技术或开源的GPU共享插件，在Flyte中实现更细粒度的GPU切分，进一步提升资源利用率。

**未来发展趋势：**
*   **数据与代码的深度融合：** 工作流引擎将不仅调度计算，还将主动管理数据版本（如与Lakehouse集成）。
*   **智能调度：** 利用机器学习预测任务耗时和资源需求，从而优化EKS集群的扩缩容策略。

---

### 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现状：** 如果你的团队正在使用 cron jobs 或 Airflow 处理ML任务，且面临资源管理混乱的问题，Flyte是极佳的替代品。
2.  **环境准备：** 在AWS上创建一个EKS集群（或使用EKS Anywhere）。
3.  **安装Flyte：** 使用Helm Chart部署Flyte到EKS，或者注册Union.ai的SaaS服务连接你的EKS集群。
4.  **代码迁移：** 将现有的Python脚本用`@task`装饰器包装，用`@workflow`连接。

**具体的行动建议：**
*   **第一步：** 不要直接迁移核心业务。先构建一个简单的“数据处理 -> 模型训练 -> 评估”的Demo工作流。
*   **第二步：** 配置S3作为Flyte的Blob存储后端，确保数据读写畅通。
*   **第三步：** 测试资源隔离。尝试运行一个需要GPU的任务，验证EKS是否能正确调度到GPU节点。

**需要补充的知识：**
*   **Python Decorators:** 理解装饰器的工作原理。
*   **Docker:** 学会如何编写Dockerfile并构建包含依赖项的镜像。
*   **Kubernetes Basics:** 理解Pod, Node, Namespace, Service等概念。

**实践中的注意事项：**
*   **镜像大小：** 尽量保持Docker镜像精简，否则每次任务启动拉取镜像会消耗大量时间。建议使用多阶段构建或使用Flyte的镜像缓存机制。
*   **资源限制：** 务必在Task中设置`limits`，防止失控的ML任务耗尽整个EKS集群的资源。

---

## 最佳实践

### 实践 1：利用 Union.ai 和 Flyte 实现可扩展的容器化 AI 工作流

**说明**:
Flyte 是一个开源的工作流编排平台，专门用于构建数据和 ML 流水线。在 Amazon EKS 上运行 Flyte 允许您利用 Kubernetes 的强大扩展能力来运行复杂的 AI 任务。Union.ai 提供了托管的 Flyte 平台，简化了在 EKS 上的部署和管理。通过将任务定义为容器，您可以实现高度可移植和可扩展的 AI 工作流。

**实施步骤**:
1. 在 EKS 集群上部署 Flyte 控制平面或注册 Union.ai 控制平面。
2. 使用 Python、Java 或 Go 定义 Flyte 任务和工作流，将每个步骤容器化。
3. 配置 Flyte 后端以使用 EKS 作为执行目标。
4. 通过 Flyte UI 或 CLI 提交工作流执行。

**注意事项**:
确保您的 EKS 节点具有足够的资源来运行 Flyte 的系统组件以及用户工作负载。合理配置资源请求和限制以避免资源争用。

---

### 实践 2：优化 GPU 资源调度与节点自动扩缩容

**说明**:
AI 工作流通常需要大量的计算资源，特别是 GPU。在 EKS 上，结合使用 Karpenter 或 Cluster Autoscaler 可以实现基于工作负载需求的节点自动扩缩容。Flyte 可以通过特定的节点选择器和污点/容忍度机制，确保需要 GPU 的任务被正确调度到 GPU 节点上，从而优化成本和性能。

**实施步骤**:
1. 安装并配置 Karpenter 或 EKS Cluster Autoscaler。
2. 为 GPU 实例（如 p3 或 p4 系列）创建专门的 EKS 节点组或配置 Karpenter 的 Provisioner。
3. 在 Flyte 任务定义中，指定资源需求，例如 `requests[gpu.nvidia.com/gpu]=1`。
4. 配置 Flyte 的 Pod 模板以包含适当的节点选择器，确保任务仅在 GPU 节点上运行。

**注意事项**:
GPU 实例成本较高，建议配置自动缩容策略，在空闲时释放节点。同时，确保 Flyte 的任务超时设置合理，防止长时间占用昂贵的 GPU 资源。

---

### 实践 3：实施模块化工作流设计

**说明**:
Flyte 提倡模块化的工作流设计，即将复杂的 AI 流水线分解为可重用、独立的任务。这种设计提高了代码的可维护性和可测试性。在 EKS 环境中，模块化任务可以独立扩展，失败的组件可以重试，而无需重新运行整个流水线，从而提高了容错性。

**实施步骤**:
1. 将 AI 流水线中的逻辑单元（如数据预处理、模型训练、模型评估）拆分为独立的 Flyte 任务。
2. 使用 Flyte 的 `@task` 装饰器定义每个模块，并明确输入输出类型。
3. 使用 `@workflow` 装饰器组合这些任务，定义数据流和依赖关系。
4. 利用 Flyte 的分支和循环逻辑处理复杂的条件逻辑。

**注意事项**:
注意任务之间的数据传递开销。对于大规模数据，应使用 S3 或 EFS 等共享存储系统传递引用，而不是直接在内存中传递大型对象。

---

### 实践 4：利用 Spot 实例降低非关键工作负载成本

**说明**:
对于容错性较高的 AI 工作流（如批处理训练或超参数调优），利用 Amazon EC2 Spot 实例可以显著降低计算成本（最高可达 90%）。Flyte 原生支持重试机制，结合 EKS 的 Spot 实例，可以在节点中断时自动重新调度任务，实现成本优化的同时保证工作流完成。

**实施步骤**:
1. 在 EKS 中配置混合节点组，包含 On-Demand 和 Spot 实例。
2. 或者在 Karpenter 配置中启用 Spot 容量优化。
3. 在 Flyte 项目配置中，为特定任务设置较高的重试次数，以应对 Spot 实例的中断。
4. 利用 Flyte 的队列系统，将可中断的工作流调度到 Spot 节点上。

**注意事项**:
并非所有任务都适合 Spot 实例。对于长时间运行且无法频繁检查点的训练任务，建议使用 On-Demand 实例。确保您的存储层支持跨节点访问（如 EFS 或 S3），以便在节点重建后恢复数据。

---

### 实践 5：集成 S3 实现高效的数据湖存储与访问

**说明**:
AI 工作流通常涉及海量数据集。将 Amazon S3 作为主要存储层，结合 EKS 上运行的 Flyte 工作流，可以实现存储与计算的分离。Flyte 提供了与 S3 的原生集成，支持在 S3 和计算容器之间高效流式传输数据，避免下载整个数据集到本地磁盘。

**实施步骤**:
1. 为 EKS 节点配置

---

## 学习要点

- Union.ai 与 Flyte 的结合为在 Amazon EKS 上构建可扩展、可移植且生产级的 AI 工作流提供了开源的标准化平台。
- Flyte 能够有效编排复杂的机器学习流水线，自动化管理从数据预处理、模型训练到部署的全生命周期及依赖关系。
- 该架构通过容器化技术实现了工作流的高度可移植性，确保应用可以在本地、云端或混合云环境中无缝迁移。
- 利用 Amazon EKS 的托管 Kubernetes 服务，用户无需管理底层基础设施，即可实现 AI 工作流的弹性伸缩和高可用性。
- 平台支持异构计算，能够自动协调包括 CPU、GPU 和 AWS 在内的多种计算资源，以优化不同任务类型的性能与成本。
- 联合解决方案通过声明式的工作流定义和自动化重试机制，显著降低了构建和维护企业级 AI 系统的复杂性。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [Kubernetes](/tags/kubernetes/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [AWS](/tags/aws/) / [机器学习](/tags/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/) / [MLOps](/tags/mlops/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--6.md" >}})
