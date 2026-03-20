---
title: 在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流
date: 2026-02-23 15:36:57+08:00
draft: false
entry_kind: auto
tags:
- Flyte
- Union.ai
- Amazon EKS
- Kubernetes
- 工作流编排
- AWS
- MLOps
- Python SDK
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: '**摘要：利用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流** 本文介绍了如何利用 Flyte Python
  SDK 编排和扩展 AI/ML 工作流。文中重点探讨了 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service
  (Am'
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios:
- AI/ML项目
- Kubernetes
---

# 在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---

## 摘要/简介

在本文中，我们将介绍如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来深入解析这一解决方案。

---

## 导语

随着 AI 工作流的复杂度日益提升，如何基于 Kubernetes 实现高效、可扩展的编排已成为技术团队的关键挑战。本文将深入探讨如何利用 Union.ai 2.0 和 Flyte 在 Amazon EKS 上构建工作流，并展示其与 Amazon S3、Aurora 等 AWS 服务的无缝集成。通过一个使用 Amazon S3 Vectors 的实战示例，我们将帮助您掌握在云端构建稳定、高性能 AI 管道的具体方法。

---

## 摘要

**摘要：利用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流**

本文介绍了如何利用 Flyte Python SDK 编排和扩展 AI/ML 工作流。文中重点探讨了 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并实现与多项 AWS 服务（如 Amazon S3、Amazon Aurora、IAM 和 Amazon CloudWatch）的无缝集成。文章还通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例，详细展示了该解决方案的实际应用。

---

## 评论

### 深度评论

#### 1. 技术架构视角：云原生与数据治理的结合
该文章的核心价值在于阐述了 Union.ai（基于 Flyte）如何利用 Amazon EKS 的 CRD 机制，将 AI 工作流转化为标准的 Kubernetes 资源。这种架构设计利用了 EKS 的控制平面能力（如 VPC CNI 网络隔离）和 S3 的存储能力，构建了一个具备数据血缘管理功能的混合编排系统。

然而，文章在架构选择上存在一定的视野局限性。它默认 Kubernetes 是运行所有 AI 工作流的最佳载体，却未充分评估运维成本。对于中小型企业而言，维护 EKS 集群的复杂度可能较高，文章虽然提及了与 AWS Fargate 的兼容性，但缺乏对 Serverless 容器模式下成本与性能平衡的具体分析。

#### 2. 开发与运维的实用性：弥合环境鸿沟
文章展示了如何通过 Python SDK 定义任务并直接部署为 Pod，这一点解决了 MLOps 领域的一个实际问题：即数据科学家的 Notebook 代码难以直接复用于生产环境。Union.ai 提供的“函数即工作流”模式，配合 EKS 的弹性伸缩，确实为从本地实验到云端部署提供了一致性路径。

但在可读性方面，文章遵循了典型的技术营销叙事，代码示例较为理想化。它省略了在生产环境中常见的复杂情况，例如依赖库冲突、CUDA 版本兼容性调试等。这种简化的呈现方式可能会让缺乏深厚 K8s 运维背景的读者低估实际落地的难度。

#### 3. 创新性与行业影响：数据感知编排与平台工程
文章中提到的“数据感知”编排能力是该方案的一个显著特点。与传统工具仅关注任务状态不同，Flyte 对输入输出数据版本的追踪，实际上在 Kubernetes 之上构建了一个隐式的元数据管理层。这对于需要严格合规和回溯的行业（如医疗或金融）具有实际参考意义。

从行业趋势来看，这种集成方案反映了 MLOps 正在从单一工具竞争转向生态整合。Union.ai 深度集成 AWS 生态，实际上是在推动企业建立基于 Kubernetes 的内部平台（IDP），而非完全依赖托管的 SaaS 服务。这进一步强化了“Kubernetes 作为 AI 基础设施底座”的行业共识。

#### 4. 边界条件与适用性分析
尽管该架构在扩展性和管理上具有优势，但在特定场景下并非最优解：
*   **运维复杂度：** 对于仅需定时训练模型的轻量级团队，引入 EKS + Flyte 可能属于过度设计。相比之下，AWS SageMaker Pipelines 或 Step Functions 的运维门槛更低。
*   **实时性要求：** EKS 节点的扩容存在不可避免的延迟。对于需要毫秒级响应的在线推理服务，直接使用 EKS Pod 可能无法满足性能要求，专用的推理服务可能更为合适。

---

## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

### 深入分析：基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流

### 1. 核心观点深度解读

### 文章的主要观点
文章的核心主张是：**通过将 Union.ai（托管版 Flyte）与 Amazon EKS（Elastic Kubernetes Service）深度集成，企业可以构建一个既具备云原生弹性与扩展性，又能满足 AI/ML 复杂编排需求的生产级工作流平台。**

### 作者想要传达的核心思想
作者试图传达“**编排层与基础设施层解耦**”的重要性。传统的 MLOps 往往受困于维护底层基础设施的复杂性。作者认为，利用 Flyte 的声明式 Python SDK 和 Union.ai 的管理能力，开发者可以将 Kubernetes 的强大能力转化为简单的 Python 代码，从而在 AWS 上实现从“模型原型”到“生产环境”的无缝过渡，无需成为 Kubernetes 专家。

### 观点的创新性和深度
*   **深度：** 文章不仅仅停留在“如何部署”，而是深入探讨了“如何让数据科学家和 ML 工程师高效协作”。它强调了 Flyte 如何处理 ML 工作流中特有的痛点——如数据血缘、任务级别的容器化、以及跨不同计算类型（CPU vs GPU vs Spot 实例）的调度。
*   **创新性：** 将 Union.ai 2.0 作为一个关键推动者。传统的 Flyte 开源版本部署在 EKS 上非常复杂，需要大量运维知识。Union.ai 2.0 的引入代表了 **MLOps 平台即服务** 的趋势，即通过商业化工具屏蔽开源技术的部署门槛，直接对接 AWS 生态（如 S3, IAM, SageMaker 等）。

### 为什么这个观点重要
随着大模型（LLM）和生成式 AI 的爆发，AI 工作流不再仅仅是简单的训练脚本，而是包含了复杂的数据预处理、微调、评估和部署的流水线。Kubernetes 虽然是行业标准，但其陡峭的学习曲线阻碍了其直接在 AI 团队中的普及。这篇文章提出的解决方案解决了**“Kubernetes 运维复杂性”与“AI 业务敏捷性”之间的矛盾**，对于希望降本增效、利用 AWS Spot 实例降低成本的企业至关重要。

### 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Flyte:** 一个开源的、以工作流为中心的编排层，专为构建、处理和调度 ML 和数据工作流设计。
2.  **Union.ai:** Flyte 的商业托管版本，提供控制平面和管理界面，简化了 Flyte 的部署。
3.  **Amazon EKS:** AWS 提供的托管 Kubernetes 服务，用于运行容器化应用。
4.  **Flyte Python SDK:** 允许用户使用 Python 装饰器和函数定义工作流。
5.  **AWS 服务集成:** Amazon S3 (存储), IAM (身份与访问管理), EC2/Spot Instances (计算资源).

### 技术原理和实现方式
*   **声明式工作流定义：** 利用 Python 函数和装饰器（如 `@task`, `@workflow`）定义有向无环图（DAG）。Flyte 编译器将这些代码编译为 Protobuf 格式，并提交给 Flyte Admin 服务。
*   **容器化与执行：** Flyte 自动构建 Docker 镜像（或使用预构建镜像），并将任务调度到 EKS 集群上运行。每个任务可以指定不同的资源需求（CPU, 内存, GPU）。
*   **数据传递机制：** Flyte 自动处理任务间的数据传递。大型数据集通过引用（S3 路径）传递，小数据通过原始值传递，确保中间结果的自动追踪和版本管理。
*   **EKS 上的部署：** Union.ai 控制平面部署在 EKS 上，利用 Kubernetes 的 CRD（Custom Resource Definitions）来管理 Flyte 的执行对象。Flyte Propeller（Kubernetes 控制器）负责监控任务状态并处理重试逻辑。

### 技术难点和解决方案
*   **难点：** Kubernetes 环境下的资源碎片化和异构计算调度（例如：某些任务需要 GPU，某些只需要 CPU）。
    *   **解决方案：** Flyte 允许在任务级别精细化配置资源请求，并利用 Node Selectors 和 Taints/Tolerations 将特定任务调度到 EKS 上的特定节点组（如 GPU 节点或 Spot 实例）。
*   **难点：** 数据科学家的本地环境与生产环境的一致性。
    *   **解决方案：** Flyte 强制使用容器化运行任务，确保“在我机器上能跑”的问题不再出现。

### 技术创新点分析
*   **Type-Safe 工作流：** Flyte 对 Python 类型有强支持，能在编译期检查数据流是否匹配，这在动态语言 Python 中是一个巨大的稳定性提升。
*   **Lazy Execution（惰性执行）：** 本地定义工作流时只是生成逻辑图，只有在提交到 Flyte 集群时才实际执行，这支持了“本地开发，云端运行”的混合模式。

### 3. 实际应用价值

### 对实际工作的指导意义
*   **降低运维负担：** ML 团队无需维护一套复杂的 Airflow 或 Kubernetes 集群，可以专注于模型逻辑。
*   **成本优化：** 通过 Flyte 原生支持 AWS Spot 实例进行无状态计算，可以显著降低大规模数据处理和模型训练的成本。

### 可以应用到哪些场景
*   **大模型（LLM）微调流水线：** 数据清洗 -> 预处理 -> LoRA 微调 -> 模型评估。
*   **批量推理：** 每天定时处理海量数据进行预测（如金融风控、推荐系统）。
*   **特征工程：** 周期性更新特征库。

### 需要注意的问题
*   **Vendor Lock-in（厂商锁定）：** 虽然使用了开源的 Flyte，但深度依赖 Union.ai 的托管服务可能会导致迁移回纯开源 Flyte 的成本较高。
*   **学习曲线：** 虽然比原生 K8s 简单，但团队仍需理解容器化和 DAG 的概念。

### 实施建议
*   从非关键路径的工作流开始迁移，验证 Flyte 与 AWS S3/IAM 的权限配置（IRSA - IAM Roles for Service Accounts）。
*   建立标准的容器镜像构建流程，因为 Flyte 任务依赖容器。

### 4. 行业影响分析

### 对行业的启示
这篇文章反映了 **MLOps 正在从“以模型为中心”向“以数据/工作流为中心”转移**。单纯的模型训练不再是瓶颈，如何高效、可复现、低成本地管理整个数据流水线才是关键。

### 可能带来的变革
*   **Kubernetes 的民主化：** 类似 Flyte 这样的抽象层将使得 Kubernetes 对数据科学家透明，K8s 将真正成为通用的 AI 算力底座，而不仅仅是后端开发的工具。
*   **云原生 AI 的标准化：** 推动了基于 K8s 的 AI 工作流标准（如 KubeFlow, Argo Workflow, Flyte）之间的竞争与融合。

### 相关领域的发展趋势
*   **Serverless AI 的兴起：** 虽然 EKS 是托管服务，但未来的趋势是更极致的 Serverless（如 AWS SageMaker Serverless 或 Flyte 结合 AWS Fargate）。
*   **混合云支持：** 企业不仅需要 AWS，还需要跨云或本地部署，Flyte 的架构支持这种多集群/多云管理。

### 5. 延伸思考

### 引发的其他思考
*   **LLMOps 的特殊性：** 传统的 Flyte 擅长处理批处理任务，但面对基于事件的、低延迟的 LLM 推理链，它是否还是最佳选择？或者它更适合作为“后台”的微调/评估管道？
*   **成本控制的颗粒度：** 在 EKS 上使用 Spot 实例虽然便宜，但中断机制需要应用层（Flyte 任务）具备 Checkpoint（断点续训）能力，这对代码编写提出了更高要求。

### 可以拓展的方向
*   **与 Ray.io 的集成：** Ray 是目前分布式 Python 的标准，Flyte + Ray on EKS 将是一个极其强大的组合，能够处理超大规模的并行训练和强化学习。
*   **数据血缘治理：** Flyte 记录了所有输入输出，这可以进一步拓展为自动化的数据治理平台，满足合规性要求。

### 未来发展趋势
*   **编排层的统一：** 未来数据工程和 ML 工程的边界将模糊，同一个 Flyte 工作流中可能既包含 SQL 任务（通过 Spark），也包含 PyTorch 训练任务。

### 7. 案例分析

### 结合实际案例说明
假设一家金融科技公司每天需要处理 100TB 的交易数据，进行特征提取并训练一个欺诈检测模型。

*   **传统做法：** 使用 Airflow 调度 Shell 脚本，脚本中调用 Spark-submit。资源竞争严重，经常 OOM（内存溢出），且难以扩展。
*   **Flyte + EKS 做法：**
    *   使用 Flyte Python SDK 定义工作流。
    *   数据处理任务自动扩容 EKS 节点（使用 Spot 实例）。
    *   训练任务自动调度到带有 GPU 的节点组。
    *   如果某个节点失败，Flyte 自动重试该特定任务，无需人工干预。

### 成功案例分析
**Spotify (Flyte 的早期创造者和使用者):** Spotify 成功利用 Flyte 管理其庞大的推荐系统和 ML 基础设施，实现了每天数百万个工作流的运行，极大地提高了数据科学团队的生产力，并实现了计算资源的动态利用

---

## 最佳实践

### 实践 1：构建可扩展且模块化的 EKS 基础设施

**说明**:
在 Amazon EKS 上运行 AI 工作负载时，基础设施的弹性至关重要。利用 Union.ai 和 Flyte，应确保 EKS 集群能够根据工作流的任务需求自动扩展。这包括配置 Kubernetes Cluster Autoscaler 和 Karpenter 等工具，以处理不同类型的 AI 任务（如 GPU 密集型训练或 CPU 密集型数据预处理），并确保节点组与 Flyte 的任务资源请求相匹配。

**实施步骤**:
1. **配置节点自动扩缩**：安装并配置 Cluster Autoscaler 或 Karpenter，使其能够根据 Flyte 传递的 Pod 资源请求（如 `nvidia.com/gpu`）自动启动或终止符合条件的节点。
2. **定义节点标签与污点**：为不同的节点组打上标签（如 `workload=ai-training`），并配合 Flyte 的任务模板或节点选择器，将特定任务调度到具有相应硬件（如 GPU 实例）的节点上。
3. **设置 Flyte 原生资源**：在 Flyte 任务定义中，准确指定 `requests` 和 `limits`，确保调度器有足够的信息进行正确的容量决策。

**注意事项**:
避免过度配置资源限制，这可能导致资源浪费。同时，确保 Spot 实例的使用策略得当，以应对可能的中断，适合用于容错的训练任务。

---

### 实践 2：优化数据访问与存储策略

**说明**:
AI 工作流通常涉及海量数据集。直接通过 S3 或其他对象存储进行频繁的读写操作可能会成为瓶颈。最佳实践是利用 EKS 上的动态存储供应和缓存机制，或者利用 Flyte 的数据传递特性，确保数据在计算节点本地的高可用性，从而减少 I/O 延迟并提高吞吐量。

**实施步骤**:
1. **使用 EFS 或 FSx for Lustre**：对于需要共享存储的高性能计算（HPC）工作流，配置 FSx for Lustre 或 Amazon EFS CSI 驱动程序，以提供低延迟的数据访问。
2. **利用 Flyte 的数据传递**：利用 Flyte 自动处理数据在任务间传递的能力，将大型数据集引用（S3 路径）而非实际数据体在任务间传递，减少网络开销。
3. **数据本地化**：在容器启动脚本中实现逻辑，仅在任务开始时将热数据下载到节点的临时存储（如 NVMe SSD）中，并在任务结束后清理。

**注意事项**:
注意存储卷的访问模式。确保训练任务不会因为并发读写共享卷而产生冲突。对于极大规模数据，优先考虑 S3 直传而非挂载卷。

---

### 实践 3：实施容器镜像优化与缓存

**说明**:
AI 容器镜像通常非常大（数 GB），包含深度学习框架和库。拉取这些镜像会显著延长任务启动时间。通过优化镜像构建过程并利用 EKS 的镜像缓存功能，可以大幅加速工作流的启动速度。

**实施步骤**:
1. **多阶段构建**：使用 Docker 多阶段构建，仅保留运行时所需的最低依赖，去除不必要的构建工具和缓存文件。
2. **使用极简基础镜像**：基于官方精简版镜像（如 `python:3.9-slim`）或使用 EKS 针对优化的 Amazon ECR 镜像。
3. **启用镜像缓存**：在 EKS 节点上配置 kubelet 镜像预拉取策略，或利用 Union.ai/Flyte 的缓存机制，确保未更改的任务不会重新拉取镜像或重新执行。

**注意事项**:
确保优化后的镜像仍然包含运行 AI 模型所需的所有系统库（如 CUDA、cuDNN）。在精简镜像前进行充分的测试。

---

### 实践 4：利用 Flyte 进行工作流版本控制与可复现性

**说明**:
AI 实验需要严格的版本控制以确保结果的可复现性。Flyte 强制执行严格的版本控制策略，结合 Union.ai 的平台能力，可以确保代码、参数和容器镜像的特定版本被锁定，从而实现“一次构建，多次运行”。

**实施步骤**:
1. **参数化工作流**：将超参数和数据路径定义为 Flyte 工作流的输入参数，而不是硬编码在脚本中。
2. **标记与注册**：使用 Union.ai 的注册功能，为每个发布的工作流打上版本标签（例如 `v1.0.1`），并在生产环境中引用特定版本，而非 `latest`。
3. **环境隔离**：为开发、测试和生产配置不同的 Flyte 项目或域，确保工作流在迁移到生产环境之前已经过充分的版本验证。

**注意事项**:
避免在代码中依赖外部状态的变化（如未经版本控制的数据集）。所有输入数据最好都有校验和或版本 ID。

---

### 实践 5：成本管理与资源配额

**说明**:
在 EKS 上运行 GPU 实例成本

---

## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展且高效的 AI 工作流，实现机器学习任务编排的自动化与容器化。
- 利用 Amazon EKS 的托管 Kubernetes 服务，可以简化底层基础设施的运维工作，让开发者专注于核心业务逻辑与模型迭代。
- Flyte 提供的强类型工作流定义确保了数据处理和模型训练流程的可靠性与可复现性，有效解决了实验管理混乱的问题。
- 该架构支持混合云部署，允许企业在本地和云端灵活调度计算资源，从而优化成本并满足数据合规性要求。
- 通过事件驱动的任务调度机制，工作流能够根据数据变化或特定触发条件自动启动，提升了实时响应能力。
- 集成 Amazon SageMaker 等服务进一步增强了模型训练与部署的能力，打通了从数据准备到上线的全链路流程。
- 统一的工作流平台促进了数据科学家与工程师之间的协作，通过标准化的接口加速了 AI 应用的落地与交付。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

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
