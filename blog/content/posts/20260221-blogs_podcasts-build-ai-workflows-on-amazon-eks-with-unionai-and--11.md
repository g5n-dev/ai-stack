---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-21T05:16:27+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "S3 Vectors"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建和扩展 AI/ML 工作流。 文章主要探讨了以下核心内容： 1. **工具与技术栈**：使用 Flyte Python SDK 编排和扩展 AI/ML 工作流。 2. **部署平台**：利用 Union.ai"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们将介绍如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并实现与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 以及 Amazon CloudWatch 等 AWS 服务的无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例，深入剖析这一解决方案。

---
## 导语

随着 AI 工作流的复杂度日益增加，在 Kubernetes 上构建可扩展且具备生产级可靠性的编排系统已成为关键需求。本文将详细介绍如何利用 Union.ai 和 Flyte 在 Amazon EKS 上部署工作流，并实现与 Amazon S3 及 IAM 等 AWS 服务的原生集成。通过阅读本文，您将掌握具体的架构配置方法，并通过一个使用 Amazon S3 Vectors 的示例，了解如何高效构建和管理端到端的 AI 流程。

---
## 摘要

本文介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建和扩展 AI/ML 工作流。

文章主要探讨了以下核心内容：
1.  **工具与技术栈**：使用 Flyte Python SDK 编排和扩展 AI/ML 工作流。
2.  **部署平台**：利用 Union.ai 2.0 系统将 Flyte 部署在 Amazon EKS（亚马逊弹性 Kubernetes 服务）上。
3.  **AWS 生态集成**：该方案能够与多项 AWS 服务实现无缝集成，包括 **Amazon S3**（存储）、**Amazon Aurora**（数据库）、**AWS IAM**（身份与访问管理）以及 **Amazon CloudWatch**（监控）。
4.  **实践示例**：文章通过一个具体的 AI 工作流示例演示了该解决方案，该示例使用了新的 **Amazon S3 Vectors** 服务。

---
## 评论

### 深度评价：基于 Amazon EKS 构建 Union.ai 与 Flyte AI 工作流

**中心观点**
该文章主张通过 Union.ai 2.0 平台将 Flyte 工作流引擎部署于 Amazon EKS 之上，利用云原生架构的弹性与 Kubernetes 的编排能力，解决大规模 AI/ML 工作流在生产环境中的可移植性、可扩展性与异构资源调度难题。

**支撑理由与深度分析**

**1. 内容深度：云原生与 AI 工作流的深度融合**
*   **事实陈述**：文章详细描述了 Flyte 如何基于 EKS 运行，并利用 S3 进行数据交换。这触及了当前 MLOps 的核心痛点——即如何将模型训练（GPU 密集型）与数据处理（CPU/IO 密集型）在同一个工作流中进行异构调度。
*   **深度分析**：文章的深度在于它没有停留在“容器化”这一表层，而是深入到了“工作流即代码”的层面。通过 Union.ai 托管 Flyte，实际上是在解决 Kubernetes 上手门槛高的问题。Kubernetes 原生 API 对数据科学家过于复杂，Flyte 提供的 Python 抽象层屏蔽了底层 K8s 的复杂性（如 Pod 配置、资源限额），这是一种**架构上的深度**。它论证了“控制平面”与“计算平面”分离的必要性，这是构建企业级 AI 平台的关键。

**2. 实用价值：解决“最后一公里”的部署难题**
*   **作者观点**：文章暗示使用 Union.ai 可以显著简化在 AWS 上部署 Flyte 的过程。
*   **实际指导意义**：对于许多中型团队而言，直接维护开源 Flyte 集群的运维成本极高。文章展示的方案提供了一条从“本地开发”平滑过渡到“云端生产”的路径。特别是对于需要频繁迭代模型的数据科学团队，这种架构支持代码版本化、数据追踪和自动重试，直接提升了工程化效率。它不仅是一个技术栈的介绍，更是一份**降低 MLOps 落地摩擦**的实操指南。

**3. 创新性：对“单一编排标准”的探索**
*   **你的推断**：虽然 Flyte 本身并非全新技术，但文章强调的“无缝集成 AWS 服务”以及 Union.ai 的 SaaS 化交付，代表了一种从“自建平台”向“采购云原生能力”的范式转移。
*   **创新点**：文章隐含地提出了“工作流的可移植性”优于“锁定特定云厂商 AI 服务”的观点。通过使用 EKS 和 Flyte，用户可以在保留 AWS 基础设施优势（如 EC2 Spot 实例、S3）的同时，避免完全被 SageMaker 等黑盒服务绑定，保留了通过 Kubernetes YAML 进行底层定制的权利。这是一种**混合云架构策略**的创新体现。

**反例与边界条件**

**1. 边界条件一：运维成本的“隐形转移”**
*   **事实陈述**：虽然 Union.ai 简化了控制平面，但底层的 EKS 集群维护、节点组管理、VPC 网络配置仍需用户负责。
*   **批判性观点**：对于缺乏 Kubernetes 运维能力的纯算法团队，这套方案的**总拥有成本（TCO）**可能高于直接使用 Amazon SageMaker 或 Vertex AI。文章可能低估了在 EKS 上调试网络策略或存储驱动（如 CSI driver）的复杂性。

**2. 边界条件二：轻量级任务的“过度工程”**
*   **你的推断**：如果只是进行简单的周期性批处理或小规模推理，引入 Flyte + EKS + Union.ai 的架构属于“重型坦克打蚊子”。
*   **反例**：对于低延迟、高并发的在线推理服务，Flyte 这种面向批处理的编排系统并非最佳选择，直接使用 KServe 或 Seldon Core 更为合适。文章未明确界定 Flyte 作为“批处理编排器”与在线服务之间的边界，可能导致读者误将其作为万能方案。

**可验证的检查方式**

1.  **性能基准测试（指标）**：
    *   在相同规模的 EKS 集群上，对比使用 Flyte 编排的 Ray/PyTorch 任务与直接使用 AWS Batch 或 SageMaker 的启动延迟。检查“冷启动”时间是否因为 K8s Pod 调度而显著增加（预期增加 10-30%）。

2.  **成本效益分析（实验）**：
    *   设定一个包含 1000 个节点的模拟工作流，分别计算“纯 EC2 + 自建脚本”与“EKS + Flyte + Spot 实例”两种模式下的资源利用率。验证 Flyte 对 Spot 实例中断的处理是否能真正带来成本下降（目标：节省 30%-60% 算力成本）。

3.  **故障恢复演练（观察窗口）**：
    *   在工作流执行过程中人为强制终止 Pod（模拟节点故障）。观察 Flyte 的自动重试机制是否会导致数据重复处理或 S3 临时文件堆积，验证其“Exactly-Once”语义的可靠性。

**实际应用建议**

*   **适用场景**：建议将此架构应用于**多阶段流水线**（ETL -> 特征工程 -> 模型训练 -> 批量推理），特别是那些需要混合使用 CPU 和 GPU 资源，且对成本敏感（需大量使用 Spot 实例）的离线任务。
*   **架构优化**：不要盲目

---
## 技术分析

# 技术分析

## 核心架构与设计理念

文章探讨了一种基于 Amazon EKS 的机器学习工作流构建方案，核心在于利用 **Union.ai（基于开源项目 Flyte）** 作为编排层，与 AWS 的 Kubernetes 基础设施相结合。

*   **关注点分离**：该架构强调将业务逻辑（Python 代码）与底层基础设施管理解耦。数据科学家使用 Flyte Python SDK 定义任务，无需直接处理 Kubernetes 的复杂性（如 Pod 配置、资源调度等）。
*   **声明式工作流**：通过将 ML 流水线定义为代码，实现了版本控制和可重复性。Flyte 将这些定义编译为在 EKS 上执行的规范，利用 K8s 的能力进行实际的容器调度。
*   **云原生适配**：文章指出，EKS 提供了托管的控制平面，减少了运维负担，而 Flyte 则在此基础上提供了针对 ML 场景优化的任务调度和数据处理能力。

## 关键技术组件与实现机制

该技术方案主要涉及以下组件的协同工作：

1.  **编排层**
    *   **Flyte**：基于 Kubernetes 的开源工作流编排平台。它允许用户使用 Python 装饰器定义任务和工作流（DAG）。
    *   **Union.ai**：提供基于 Flyte 的托管服务和企业级功能，简化了 Flyte 的部署、升级和管理。

2.  **基础设施层**
    *   **Amazon EKS**：作为计算底座，负责运行容器化的 ML 任务。EKS 提供了高可用性和弹性伸缩能力。
    *   **AWS S3**：作为数据持久化层，用于存储输入数据集、训练输出的模型文件以及中间检查点。

3.  **工作原理**
    *   **任务定义**：用户使用 Python SDK 编写函数，通过 `@task` 和 `@workflow` 装饰器声明依赖关系。
    *   **执行流程**：Flyte 编译器将代码转化为执行规范，提交给运行在 EKS 上的 Flyte 后端。Flyte Propeller（控制器）负责根据规范在 EKS 上创建和管理 Pod。
    *   **数据传递**：任务间的数据传递通过引用（如 S3 路径）实现，而非直接在内存中传递大数据集，以此优化性能并减少网络开销。

## 技术优势与适用场景

*   **抽象化底层复杂度**：通过 Flyte 的插件系统和任务模板，用户无需编写复杂的 YAML 文件即可配置 GPU 资源、环境变量和容器镜像。
*   **资源弹性利用**：结合 EKS 的节点组（Node Groups）和自动伸缩，工作流可以根据任务负载（如训练阶段需要 GPU，推理阶段需要 CPU）动态申请和释放资源。
*   **可移植性**：由于 Flyte 运行在标准的 Kubernetes 上，定义的工作流可以跨不同的云环境或本地数据中心迁移，避免了单一供应商锁定。

---
## 最佳实践

## 最佳实践指南

### 实践 1：容器化与资源优化

**说明**: 
在 Amazon EKS 上运行 AI 工作流时，容器镜像的大小和启动速度直接影响工作流的执行效率。Union.ai 和 Flyte 的工作流通常涉及多个任务，每个任务都在独立的容器中运行。优化镜像可以减少冷启动时间并降低网络传输开销。

**实施步骤**:
1. 使用多阶段构建，仅保留运行时必需的依赖库。
2. 利用 ECR 的缓存机制，并确保使用特定版本标签而非 `latest`。
3. 为 Flyte 任务配置合理的资源限制（CPU 和内存），基于实际负载分析进行设置。

**注意事项**: 
避免在镜像中包含不必要的数据集或模型权重，建议使用 S3 或其他对象存储服务进行数据传递。

---

### 实践 2：利用 Spot 实例降低成本

**说明**: 
AI 训练和数据处理任务通常具有容错性或可恢复性。在 EKS 节点组中使用 EC2 Spot 实例可以显著降低计算成本。Flyte 原生支持重试机制，结合 Spot 实例的中断通知，可以在保证任务完成的同时最大化成本效益。

**实施步骤**:
1. 配置 EKS 托管节点组，混合使用 On-Demand 和 Spot 实例。
2. 在 Flyte 任务中配置适当的重试策略，以应对 Spot 实例回收。
3. 使用 Karpenter 等自动扩缩容工具，更灵活地供应 Spot 容量。

**注意事项**: 
确保任务具有幂等性，以便在 Spot 实例中断导致任务重启时不会产生数据不一致。

---

### 实践 3：数据本地化与缓存策略

**说明**: 
频繁从 S3 下载相同的数据集会导致 I/O 瓶颈和增加成本。利用 Flyte 的缓存机制和 EKS 的节点亲和性，可以将计算任务调度到已存储数据的节点上，或利用临时存储缓存中间结果。

**实施步骤**:
1. 在 Flyte 项目中启用任务级缓存，对于相同输入参数的任务直接返回缓存结果。
2. 使用 EBS 卷或 EFS 缓存高频访问的数据集到节点本地。
3. 配置 Flyte 的数据代理，利用 S3 直传功能减少 Pod 层的数据拷贝。

**注意事项**: 
需权衡存储成本与计算速度，及时清理过期的缓存数据以防止存储空间耗尽。

---

### 实践 4：工作流模块化与可移植性

**说明**: 
Union.ai 和 Flyte 的核心优势在于将工作流代码与基础设施解耦。最佳实践是将复杂的 AI 流程拆解为独立、可测试、可复用的任务组件。这不仅便于调试，还能在不同环境（开发、测试、生产）之间轻松迁移。

**实施步骤**:
1. 定义清晰的接口，每个 Flyte 任务只负责单一逻辑功能。
2. 使用 Union.ai 的控制平面进行多环境管理，确保工作流定义在不同 Kubernetes 集群间一致。
3. 将业务逻辑与基础设施配置分离，利用 Flytekit 进行代码开发。

**注意事项**: 
避免在任务代码中硬编码基础设施连接信息，应使用 Flyte 的 Secrets 管理或环境变量注入。

---

### 实践 5：安全性与访问控制

**说明**: 
AI 工作流通常涉及敏感数据和模型权限。在 EKS 上实施最小权限原则，结合 IAM Roles for Service Accounts (IRSA)，确保 Flyte Pod 仅能访问其所需的 AWS 资源。

**实施步骤**:
1. 为 Flyte 执行的特定任务创建专用的 IAM 角色，并限制 S3 读写路径。
2. 启用 EKS 的 RBAC 控制，限制开发人员对生产命名空间的直接访问权限。
3. 使用 Union.ai 的项目域概念，隔离不同团队或项目的工作流执行环境。

**注意事项**: 
定期轮换访问密钥，并审计 Pod 的权限范围，防止权限过度授予。

---

### 实践 6：监控与可观测性集成

**说明**: 
AI 工作流的失败可能源于代码错误、资源不足或数据问题。集成 CloudWatch、Prometheus 等监控工具，结合 Flyte 的 UI 控制台，可以实现对任务性能、资源使用率和业务指标的全面监控。

**实施步骤**:
1. 部署 AWS Distro for OpenTelemetry (ADOT) 收集 EKS 集群指标。
2. 在 Flyte 任务中输出自定义指标，将模型训练损失或验证精度发送到 CloudWatch。
3. 配置告警策略，针对工作流失败、节点压力或任务超时设置通知。

**注意事项**: 
避免采集过高粒度的日志导致存储成本激增，应合理配置日志保留策略和采样率。

---
## 学习要点

- 基于您提供的内容来源（Build AI workflows on Amazon EKS with Union.ai and Flyte），以下是总结出的关键要点：
- Union.ai 和 Flyte 的结合能够在 Amazon EKS 上构建可扩展、高可用且具备容错能力的 AI 工作流，解决了传统机器学习流程在编排和扩展性上的痛点。
- 通过将 Flyte 部署在 Amazon EKS 上，用户可以利用 Kubernetes 的强大编排能力来管理复杂的 AI 和数据管道，实现计算资源的动态调度与高效利用。
- 该架构支持混合云和多云环境，允许工作负载在不同的云提供商或本地数据中心之间灵活迁移，从而避免了供应商锁定。
- Flyte 提供了针对数据密集型和机器学习工作负载的原生支持，能够自动化处理模型训练、数据预处理和超参数调优等繁琐的迭代过程。
- 利用 Amazon EKS 的托管服务特性，用户可以大幅降低基础设施的运维负担，无需管理底层控制平面即可专注于核心业务逻辑的开发。
- 该解决方案集成了 AWS 的各项安全与治理功能（如 IAM 和 VPC），确保 AI 工作流在处理敏感数据时符合企业的安全合规标准。

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

- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*