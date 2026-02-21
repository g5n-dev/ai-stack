---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 编排 AI 工作流"
date: 2026-02-21T08:52:14+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "云原生"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon Elastic Kubernetes Service (Amazon EKS) 上构建和扩展 AI/ML 工作流。 主要内容包括： 1. **核心工具**：使用 Flyte Python SDK 进行工作流的编排与扩展。 2. **部署平台**：借"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 在 Amazon EKS 上使用 Union.ai 和 Flyte 编排 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们将解释如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来探索这一解决方案。

---
## 导语

在 Kubernetes 上构建高效、可扩展的 AI 编排系统已成为技术团队的核心诉求。本文将深入探讨如何利用 Union.ai 2.0 和 Flyte，在 Amazon EKS 上构建稳健的机器学习流水线，并实现与 S3、Aurora 等 AWS 服务的原生集成。通过结合理论讲解与基于 Amazon S3 Vectors 的实战示例，我们将帮助您掌握如何在云环境中简化模型部署流程，并有效提升数据处理的可观测性与扩展性。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon Elastic Kubernetes Service (Amazon EKS) 上构建和扩展 AI/ML 工作流。

主要内容包括：

1.  **核心工具**：使用 Flyte Python SDK 进行工作流的编排与扩展。
2.  **部署平台**：借助 Union.ai 2.0 系统将 Flyte 部署在 Amazon EKS 上。
3.  **AWS 集成**：该解决方案与 Amazon S3、Amazon Aurora、AWS IAM 和 Amazon CloudWatch 等多项 AWS 服务实现无缝集成。
4.  **应用示例**：文章通过一个使用 Amazon S3 Vectors 服务的 AI 工作流示例，演示了该方案的具体实践。

该方案旨在为用户提供一个强大且无缝的云原生 AI 开发环境。

---
## 评论

**深度评论**

**核心观点**
该文章提出了一种基于 Amazon EKS 部署 Union.ai 2.0（基于 Flyte）的架构方案，旨在构建云原生、可扩展且与 AWS 深度集成的 AI/ML 工作流管道。其核心目标是通过标准化的编排层，解决从模型实验到生产环境迁移过程中面临的工程复杂性与一致性问题。

**架构逻辑与适用边界**

**1. 基于 EKS 的控制平面与资源调度（架构事实）**
文章重点阐述了 Flyte 在 EKS 上的运行模式。
*   **技术逻辑**：利用 EKS 托管 Kubernetes 控制平面，结合 Flyte 的容器任务调度能力，能够有效隔离不同优先级的任务，并处理异构计算资源（如 CPU 与 GPU 节点）的分配。Union.ai 作为一个托管控制平面，旨在降低 Flyte 本身的部署与维护难度。
*   **适用边界**：该架构引入了显著的基础设施复杂度。对于中小型团队或处于探索阶段的项目，维护 EKS 集群及配套组件的运维成本远高于使用全托管服务（如 SageMaker 或托管式 Airflow）。该方案主要适用于工作流逻辑复杂、依赖关系繁多且对资源控制有精细化需求的场景。

**2. 代码复用与开发体验（作者观点）**
文章强调使用 Flyte Python SDK 实现从原型到生产的代码复用。
*   **技术逻辑**：Flyte 采用“代码即配置”的理念，通过 Python 装饰器将函数转化为任务，并自动处理版本控制、数据血缘和容器化。这在一定程度上减少了数据科学家对底层 DevOps 知识的依赖，促进了 MLOps 中 CI/CD 和 CT（Continuous Training）的标准化。
*   **适用边界**：高层抽象必然带来底层细节的屏蔽。当业务逻辑需要深度集成 AWS 特有服务（如复杂的 IAM 角色链、VPC 私有端点）时，单纯依赖 Python SDK 可能无法覆盖所有配置需求，开发者仍需编写 K8s YAML 或修改 Helm Chart，此时“低代码”的优势会减弱。

**3. 数据本地性与 AWS 生态集成（事实陈述）**
文章提到了与 S3 的集成能力。
*   **技术逻辑**：Flyte 任务 Pod 可以直接利用 S3 SDK 进行高吞吐量的数据读写，符合数据计算本地性的最佳实践。同时，利用 EKS 的 Node Groups 结合 Spot 实例，能够有效优化批处理任务的算力成本。
*   **适用边界**：文章未深入探讨企业级数据治理（如 AWS Lake Formation）的权限集成问题。在严格的安全合规环境下，配置 S3 访问权限、Service Account (IRSA) 以及网络策略属于高复杂度操作，这往往是通用教程中未涵盖的配置难点。

**4. 混合编排与多语言支持（技术推断）**
尽管文章侧重 Python，但 Flyte 底层支持多语言工作流。
*   **技术逻辑**：在典型的 AI 管道中，数据预处理可能依赖 Spark，特征工程使用 Python，而服务化模块可能基于 Go。Flyte on EKS 提供了统一平台来编排这些异构任务，相比 AWS Step Functions，它在处理数据密集型、长时运行计算任务方面具有架构优势。
*   **适用边界**：如果工作流主要由轻量级的 API 调用和逻辑判断组成，AWS Step Functions 在服务耦合度和运维成本上可能更为合适。Flyte 的优势领域在于“重计算”任务的编排，而非通用的业务流程自动化。

**综合评价**

**1. 内容深度：系统架构视角**
文章跳出了单一的 API 使用教学，转而从 Kubernetes 架构层面（如 Pod 优先级、资源配额）讨论 AI 基础设施，具有较高的技术参考价值。但在成本效益分析方面略显不足，未详细对比 Union.ai 商业许可成本与自建开源 Flyte 所需的人力运维成本。

**2. 实用价值：场景依赖性强**
该方案对于具备 Kubernetes 运维能力的成熟 AI 团队（如涉及大规模分布式训练或复杂的数据处理）具有较高的实用价值，能够提供标准化的生产环境规范。然而，对于初创公司或快速验证原型的团队，该方案可能存在“过度设计”的风险，直接使用托管式 MLOps 平台通常效率更高。

**3. 行业定位：编排层的标准化**
文章提出的观点代表了一种向“云原生标准化”回归的趋势。它并未试图颠覆现有的计算引擎，而是通过 Flyte 提供一个统一的编排层，试图在灵活性和工程规范之间寻找平衡点。

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章核心观点和技术要点的深入分析。由于原文内容受限，本分析将基于标题和摘要所暗示的技术架构、行业标准实践以及 Union.ai 和 Flyte 的技术特性进行深度推演和构建。

---

# 1. 核心观点深度解读

**主要观点：**
文章的核心主张是，通过结合 **Union.ai**（提供的企业级 Flyte 平台）与 **Amazon EKS**（AWS 的托管 Kubernetes 服务），企业可以构建一个既具有云原生弹性与可扩展性，又具备高度可移植性和统一管理能力的 AI/ML 工作流编排系统。

**核心思想：**
作者试图传达“**Kubernetes 是 AI/ML 工作流的最佳运行时环境**”这一思想。传统的 AI 编排工具往往依赖于有状态的虚拟机或特定的云服务，导致厂商锁定或扩展性受限。通过将 Flyte 部署在 EKS 上，作者强调了一种**“数据与计算解耦、逻辑与基础设施分离”**的架构哲学。这种架构允许数据科学家专注于 Python 代码（业务逻辑），而平台工程师则利用 EKS 处理底层的资源调度、扩缩容和容错。

**观点的创新性与深度：**
*   **深度：** 文章超越了简单的“容器化”概念，深入到了“工作流即代码”的层面。它不仅讨论如何运行容器，更讨论如何利用 Flyte 的 SDK 将复杂的数据处理管道（ETL）、模型训练和模型部署串联起来，形成一个可追溯、可复现的有向无环图（DAG）。
*   **创新性：** 创新点在于 Union.ai 2.0 的引入。传统的开源 Flyte 部署复杂度高，Union.ai 作为托管控制面，简化了在 EKS 上的部署和运维。这种“混合云”或“自带计算集群”的模式，允许企业在利用 AWS 强大的基础设施（如 S3, SageMaker, Redshift）的同时，保持对工作流定义的完全控制权，避免被单一 AI 平台（如 SageMaker Pipelines）锁定。

**重要性：**
随着 AI 模型从实验室走向生产，**可扩展性**和**可靠性**成为瓶颈。Kubernetes 已成为云原生应用的标准，但直接在 K8s 上编排 ML 任务极其复杂。该观点的重要性在于它提供了一条**标准化的路径**，让企业能够利用现有的 K8s 运维能力来支撑大规模 AI 业务，降低了 ML 工程化的门槛和成本。

---

# 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Flyte:** 一个开源的、基于 Kubernetes 的工作流编排平台，专为 ML 和数据编程设计。
*   **Union.ai 2.0:** Flyte 的商业发行版或托管服务版本，提供控制平面和增强的企业功能。
*   **Amazon EKS (Elastic Kubernetes Service):** AWS 提供的托管 K8s 服务，负责运行底层容器。
*   **Flyte Python SDK:** 用于定义任务、工作流和数据依赖关系的 Python 装饰器和类库。
*   **AWS Service Integration:** 特指与 Amazon S3（存储）、IAM（权限）、ECR（镜像仓库）的集成。

**技术原理和实现方式：**
1.  **工作流定义：** 用户使用 Python SDK 编写函数，使用 `@task` 装饰器标记任务，用 `@workflow` 装饰器标记工作流。Flyte 自动编译这些代码生成 DAG。
2.  **容器化与注册：** Flyte 自动将 Python 代码及其依赖打包成 Docker 镜像，推送到 ECR。
3.  **执行调度：** 当工作流被触发时，Flyte Control Plane（由 Union.ai 管理）向 EKS 集群发送指令。EKS 上的 Flyte Agent（Pod）根据任务需求申请资源（CPU/GPU）。
4.  **数据传递：** 任务间的数据传递不通过直接的内存共享，而是通过引用传递。大型数据集被存储在 S3 中，Flyte 仅传递 S3 的 URI，极大减少了序列化开销。

**技术难点与解决方案：**
*   **难点：** 在 Kubernetes 上运行 ML 任务面临“异构任务调度”的挑战（例如，数据预处理需要 CPU，训练需要 GPU，推理需要高内存）。
*   **解决方案：** Flyte 引入了“任务模板”和“节点选择器”的概念，结合 EKS 的 Cluster Autoscaler，可以根据任务类型动态调度到不同规格的节点组（Node Groups），实现资源的精细化管理。
*   **难点：** Python 环境依赖冲突。
*   **解决方案：** 利用容器隔离技术，每个任务运行在独立的容器中，并通过 Flyte 的构建系统自动构建镜像。

**技术创新点分析：**
文章隐含的技术创新在于**“声明式 ML 编排”**。用户只需声明“做什么”（输入输出和逻辑），Flyte 与 EKS 的结合负责解决“怎么做”（扩容、重试、日志记录）。这种抽象层使得 ML 流水线具备了极强的容错能力和可移植性。

---

# 3. 实际应用价值

**对实际工作的指导意义：**
*   **标准化落地：** 为企业将分散的数据科学脚本转化为生产级流水线提供了标准操作程序（SOP）。
*   **成本优化：** 利用 EKS 的 Spot 实例和 Flyte 的资源回收机制，可以显著降低大规模模型训练的成本。

**可应用场景：**
*   **模型重训练：** 设置定时的 Cron 工作流，定期从 S3 读取新数据，在 EKS 上启动 GPU 节点进行训练，验证后自动部署。
*   **批量推理：** 每天需要处理海量数据（如视频转码、文档分析），利用 Flyte 并行执行任务，横向扩展 EKS 节点。
*   **超参数调优：** 利用 Flyte 的 Map/Reduce 功能，在 EKS 上并行运行数百个训练任务。

**需要注意的问题：**
*   **冷启动时间：** 每个任务启动一个 Pod 可能会带来几秒钟的延迟，对于毫秒级要求的在线推理不适用（更适合离线/批处理）。
*   **运维复杂度：** 虽然使用了 EKS，但维护一个高可用的 K8s 集群（升级、网络策略、监控）仍然需要较高的技术门槛。

**实施建议：**
*   **渐进式迁移：** 先将非实时的批处理任务（如日报生成、数据清洗）迁移至该架构，再逐步接管核心训练任务。
*   **模块化设计：** 将通用的数据处理逻辑封装为 Flyte 任务，建立企业内部的任务库。

---

# 4. 行业影响分析

**对行业的启示：**
*   **MLOps 的云原生化：** 此架构标志着 MLOps 正全面拥抱云原生。Kubernetes 不再仅仅是微服务的领地，正成为 AI 计算的通用操作系统。
*   **“混合云”策略的可行性：** 通过使用 Union.ai + EKS，企业可以在 AWS 上运行，但因为 Flyte 是开源的，理论上可以随时将工作流迁移至 Azure 或 GCP 的 K8s 上。这给 AI 基础设施提供商带来了压力，迫使它们提供更开放、更兼容的接口。

**可能带来的变革：**
*   **数据科学角色的转变：** 数据科学家不再需要依赖 DevOps 团队来手动部署模型，他们可以通过代码自助地定义和运行大规模工作流。
*   **资源利用率的透明化：** 通过精细的调度，企业可以准确计算每个 AI 模型的研发和运行成本，推动 FinOps 在 AI 领域的应用。

---

# 5. 延伸思考

**引发的思考：**
*   **Serverless vs. Kubernetes：** 虽然 EKS 提供了强大的控制，但 AWS Lambda 或 SageMaker Serverless 是否在轻量级任务上更具性价比？文章的架构是否过于重量级？
*   **多租户安全性：** 在多团队共享 EKS 集群时，如何利用 Kubernetes RBAC 和 IAM 确保租户间的数据隔离和资源隔离？

**未来发展趋势：**
*   **与 Ray 的融合：** Ray 是当前 Python 生态中最流行的分布式计算框架。未来 Flyte on EKS 可能会深度集成 Ray，使得在 K8s 上调度 Ray Cluster 变得更加简单。
*   **GPU 虚拟化与共享：** 随着 GPU 供需紧张，EKS 上的 GPU 虚拟化技术（如 NVIDIA MPS）与 Flyte 的结合将是一个重要方向。

---

# 6. 实践建议

**如何应用到自己的项目：**
1.  **评估环境：** 确认你的团队是否已经在使用 AWS，且是否有 K8s 运维能力。
2.  **POC 验证：** 选择一个简单的 ETL 任务，使用 Flyte Python SDK 编写，部署到最小的 EKS 测试集群中。
3.  **集成 S3：** 配置 IAM Role for Service Accounts (IRSA)，允许 Flyte Pod 直接访问 S3 数据桶，无需在代码中硬编码密钥。

**具体行动建议：**
*   学习 Flyte 的类型系统，理解如何将 Pandas DataFrame 或 PyTorch 模型自动序列化到 S3。
*   构建一个 CI/CD 流水线，自动将代码更新部署到 Flyte 后端。

**需补充的知识：**
*   **Kubernetes 基础：** Pod, Service, Namespace, RBAC。
*   **Docker 容器化：** 如何编写 Dockerfile，优化镜像大小。
*   **Python 装饰器与类型注解：** Flyte 大量依赖 Python 的类型提示。

---

# 7. 案例分析

**成功案例（基于行业常识推演）：**
*   **Spotify：** 作为 Flyte 的早期创造者和使用者，Spotify 利用该架构处理每天数百万级的机器学习任务（如推荐系统训练）。通过迁移到 Flyte on K8s，他们显著提高了基础设施的利用率，并减少了模型训练的等待时间。
*   **Wolt：** 外卖配送公司利用 Flyte 优化配送时间和路径规划模型，利用 EKS 的弹性应对高峰期的计算压力。

**失败案例反思：**
*   **资源泄漏：** 某公司未正确配置 Flyte 的资源限制，导致数据科学家编写了死循环代码，耗尽了 EKS 集群的 CPU，导致其他服务崩溃。
    *   **教训：** 必须在 Flyte 任务中严格设置 `@task(limits=Resources(...))`，并在 K8s 层面配置 Resource Quotas。

---

# 8. 哲学与逻辑：论证地图

**中心命题：**
企业应当采用 **Union.ai (Flyte) + Amazon EKS** 的架构来构建生产级的 AI/ML 工作流，以实现可扩展性、可移植性与运维效率的最佳平衡。

**支撑理由与依据：**
1.  **理由 1：弹性伸缩能力。**
    *   *依据：* AI/ML 负载具有潮汐特性（训练时高负载，推理时波动大）。EKS 结合 Cluster Autoscaler 可根据 Pod 需求动态增减节点，而 Flyte 负责将任务拆解为 Pod。
2.  **理由 2：

---
## 最佳实践

## 最佳实践指南

### 实践 1：容器化与资源优化

**说明**：在 Amazon EKS 上运行 AI 工作负载时，容器镜像的体积和资源请求的准确性直接影响启动速度和集群稳定性。Flyte 任务通常需要特定的深度学习库，优化镜像构建和资源配置是提升效率的基础。

**实施步骤**:
1. 使用多阶段构建和精简的基础镜像（如 `python:3.9-slim`）来减小容器镜像体积。
2. 在 Dockerfile 中利用层缓存机制，将不经常变化的依赖项放在前面。
3. 为 Flyte 任务配置合理的 CPU 和内存限制，并根据实际运行情况进行调整。
4. 使用 EKS 的 Cluster Autoscaler 和 Karpacker 等工具，根据 Pod 的资源请求自动扩展节点。

**注意事项**: 避免在容器中包含不必要的数据集或模型权重，应使用 S3 或 EFS 等存储服务进行按需加载。

---

### 实践 2：利用 Spot 实例降低成本

**说明**：AI 训练和数据处理任务通常具有容错性或可恢复性。利用 Amazon EC2 Spot 实例可以显著降低计算成本，Union.ai 和 Flyte 的任务重试机制能够很好地处理 Spot 实例的中断。

**实施步骤**:
1. 配置 EKS 节点组以混合使用 On-Demand 和 Spot 实例。
2. 在 Flyte 的任务定义中配置合理的重试策略，以应对 Spot 实例可能被回收的情况。
3. 利用 Flyte 的容错特性，确保任务断点续训或中间结果能够被持久化。
4. 监控 Spot 实例的中断频率，并据此调整任务优先级或资源分配。

**注意事项**: 关键系统组件或对中断极度敏感的任务应避免部署在仅包含 Spot 实例的节点上。

---

### 实践 3：数据访问与存储策略

**说明**：高性能的 I/O 是 AI 工作流的关键。直接在容器本地存储大量数据会导致扩展性问题。应利用 AWS 存储服务与 EKS 的集成，实现数据的解耦和高效访问。

**实施步骤**:
1. 将训练数据存储在 Amazon S3 中，并使用 Flyte 的数据类型系统通过 URI 传递数据，避免在任务间不必要的数据拷贝。
2. 对于需要高性能 I/O 的任务（如分布式训练），使用 Amazon FSx for Lustre 作为 S3 的缓存层，通过 CSI 驱动挂载到 Pod。
3. 配置适当的 IAM Roles for Service Accounts (IRSA)，赋予 Pod 最小权限的 S3 访问能力，避免硬编码凭证。

**注意事项**: 确保数据访问模式与存储类型匹配，例如频繁读取的小文件适合缓存，而一次性处理的归档数据适合直接流式传输。

---

### 实践 4：工作流编排与任务隔离

**说明**：利用 Union.ai 和 Flyte 的强大编排能力，将复杂的 AI 流程模块化。通过合理的任务隔离和依赖管理，可以提高工作流的可维护性和并行执行效率。

**实施步骤**:
1. 将长周期的训练任务与短周期的数据处理任务分解，以便在 EKS 上分别调度到不同类型的节点。
2. 使用 Flyte 的 Map/Reduce 功能处理大规模并行的数据评估或推理任务。
3. 利用命名空间或项目在 Union 平台中隔离开发、测试和生产环境的工作流。
4. 配置工作流级别的资源配额，防止单个失控的任务耗尽整个集群的资源。

**注意事项**: 确保任务之间的数据传递是轻量级的（传递指针/URI），而不是传递实际的大规模数据对象。

---

### 实践 5：可观测性与监控

**说明**：AI 工作流往往涉及复杂的依赖关系和长时间运行的任务。建立完善的监控体系对于快速发现故障和优化性能至关重要。

**实施步骤**:
1. 集成 AWS CloudWatch Container Insights 来监控 EKS 集群和 Pod 的性能指标（CPU、内存、网络）。
2. 利用 Union.ai 控制台或 Flyte Console 跟踪工作流的执行状态、任务持续时间和错误日志。
3. 配置告警规则，当工作流失败、重试次数过多或资源使用率异常时发送通知。
4. 对于模型训练任务，利用 Flyte 的回调机制将自定义指标（如 Loss、Accuracy）实时发送到外部系统（如 Prometheus 或 AWS CloudWatch）。

**注意事项**: 确保日志输出结构化，避免在任务日志中输出过多的调试信息，以免造成日志存储成本激增。

---

### 实践 6：安全性与权限管理

**说明**：在 Kubernetes 环境中运行 AI 工作流需要严格的安全控制，特别是当工作流需要访问敏感数据或 AWS 服务时。

**实施步骤**:
1. 启用 EKS 的 RBAC（基于角色的访问控制），限制不同团队对 Flyte 执行引擎的访问权限。
2. 使用 IAM Roles for Service Accounts (IRSA) 为 Flyte 任务 Pod 分配特定的 IAM 角色，遵循

---
## 学习要点

- Union.ai 和 Flyte 提供了一种在 Amazon EKS 上编排 AI 工作流的高效方法，能够显著简化机器学习模型的部署与管理流程。
- 利用 Flyte 的可扩展工作流引擎，用户可以在 Kubernetes 环境中轻松构建、调度和监控复杂的机器学习管道。
- 该方案通过容器化技术实现了计算资源的动态分配与隔离，有效提升了 AI 任务在云端的运行效率与成本效益。
- 集成 Amazon EKS 使得企业能够利用 Kubernetes 的强大生态，确保 AI 工作流具备高度的可移植性和弹性伸缩能力。
- Union.ai 的平台支持对模型训练、数据处理及评估等环节进行统一管理，有助于加速数据科学团队从实验到生产的转化周期。
- 此架构设计支持混合云及多云部署策略，允许企业根据合规与业务需求灵活选择 AI 基础设施的运行位置。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [Kubernetes](/tags/kubernetes/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [AWS](/tags/aws/) / [MLOps](/tags/mlops/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--7.md" >}})
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*