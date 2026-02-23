---
title: "使用 Union.ai 在 Amazon EKS 上构建 AI 工作流"
date: 2026-02-23T05:53:06+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "AWS", "工作流编排", "MLOps", "Kubernetes", "Amazon S3"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "以下是内容的中文简洁总结： 本文介绍了如何利用 **Flyte Python SDK** 和 **Union.ai 2.0**，在 **Amazon EKS** 上构建和编排可扩展的 AI/ML 工作流。 核心要点如下： 1. **技术栈集成**：Union.ai 2.0 支持将 Flyte 部署在 Amazon EK"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 使用 Union.ai 在 Amazon EKS 上构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们将介绍如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来演示该解决方案。

---
## 导语

随着 AI 工作流的复杂度日益增加，在 Kubernetes 上实现高效、可扩展的编排已成为技术团队的关键需求。本文将深入探讨如何利用 Union.ai 2.0 在 Amazon EKS 上部署 Flyte，并演示其与 S3、Aurora 等 AWS 服务的原生集成方式。通过具体的代码示例与架构解析，读者将掌握构建端到端 AI 流程的实用技巧，从而在云环境中更稳健地落地机器学习项目。

---
## 摘要

以下是内容的中文简洁总结：

本文介绍了如何利用 **Flyte Python SDK** 和 **Union.ai 2.0**，在 **Amazon EKS** 上构建和编排可扩展的 AI/ML 工作流。

核心要点如下：

1.  **技术栈集成**：Union.ai 2.0 支持将 Flyte 部署在 Amazon EKS 上，并能与 AWS 生态系统无缝集成。
2.  **关键 AWS 服务**：工作流能够深度整合 Amazon S3（存储）、Amazon Aurora（数据库）、IAM（身份与访问管理）以及 Amazon CloudWatch（监控）等服务。
3.  **实践示例**：文章通过一个具体的 AI 工作流案例，演示了如何利用新推出的 **Amazon S3 Vectors** 服务来实现相关功能。

---
## 评论

**文章中心观点**
该文章主张通过 Union.ai 2.0 将 Flyte 工作流编排系统部署在 Amazon EKS 上，利用 Kubernetes 的原生能力与 AWS 生态（S3, SageMaker 等）的深度集成，来解决大规模 AI/ML 工作流中的 orchestration（编排）与 scalability（扩展性）难题。

**支撑理由与边界条件分析**

1.  **基础设施的统一性与资源隔离**
    *   **[事实陈述]** 文章强调了利用 EKS 部署 Flyte 的优势。从技术角度看，这解决了 MLOps 中常见的“资源孤岛”问题。将训练和数据处理任务与推理服务运行在同一个 Kubernetes 集群中（或通过 EKS 联邦管理），可以实现统一的资源调度和配额管理。
    *   **[你的推断]** 这对于已经重度投资 Kubernetes 的企业极具吸引力，因为它避免了为维护独立的 Airflow 或 Yarn 集群而产生的额外运维开销。

2.  **Flyte 的“数据感知”编排能力**
    *   **[事实陈述]** 文章提到了 Flyte Python SDK 的使用。Flyte 的核心优势在于其基于“数据类型”而非单纯基于“任务”的依赖管理。它能自动追踪输入输出（存储在 S3），并根据数据变化自动触发工作流或缓存中间结果。
    *   **[作者观点]** 这种“以数据为中心”的抽象层比传统的 DAG（有向无环图）更符合 ML 的迭代特性，极大地简化了版本管理和实验复现。

3.  **Union.ai 2.0 提供的“开箱即用”体验**
    *   **[事实陈述]** Union.ai 提供了商业版和控制平面，降低了在 EKS 上部署和运维 Flyte 的门槛。
    *   **[你的推断]** 开源 Flyte 的部署复杂度极高（涉及 Helm charts, cert-manager, Spark operator 等）。Union.ai 实际上是在卖“运维自动化”和“企业级安全/管控”，这对于没有专职 Platform Engineer 团队的 AI Lab来说是刚需。

**反例/边界条件：**

1.  **运维复杂度的边界**
    *   **[你的推断]** 虽然文章强调了部署的便捷性，但 EKS 本身的复杂度不容忽视。对于小规模团队（例如只有 2-3 个数据科学家），维护一个高可用的 EKS 集群 + Flyte Control Plane 的成本可能远高于使用 Sagemaker Pipelines 或 Managed Airflow（MWAA）。如果工作流不涉及复杂的跨服务调用或大规模并行数据处理，Flyte 可能属于“杀鸡用牛刀”。

2.  **供应商锁定与迁移成本**
    *   **[事实陈述]** 文章大力推崇与 AWS S3、IAM 等服务的深度集成。
    *   **[你的推断]** 这种深度集成虽然带来了性能红利，但也导致了特定于 AWS 的逻辑渗透到了工作流代码中（例如在 Flyte tasks 中直接调用 Boto3 或使用 AWS 特定的容器镜像）。未来若要迁移至 GCP 或 Azure，重构代码和重新配置 IAM 权限的成本将非常高昂。

**多维度评价**

1.  **内容深度：**
    文章属于典型的“技术落地指南”。它没有停留在理论层面，而是触及了 EKS 上容器化 ML 工作流的痛点。然而，文章可能略过了 Flyte 在处理异构计算（如同时调度 GPU 训练任务和 CPU 数据清洗任务）时的具体资源调优策略，这部分往往是生产环境中最棘手的。

2.  **实用价值：**
    对于正在构建“Platform Engineering”或“Internal AI Platform”的团队，该文章提供了清晰的架构蓝图。它展示了如何将 Flyte 作为“编译器”，将 Python 代码“编译”为 K8s Pod，这种模式对算法工程师非常友好，无需学习 K8s 的 YAML 配置即可利用云原生资源。

3.  **创新性：**
    文章的核心创新点不在于单个技术，而在于组合：**Union.ai (SaaS/Control Plane) + Flyte (Engine) + EKS (Compute)**。这种模式挑战了 Databricks 或 SageMaker Studio 提供的“全托管封闭生态”，转而提倡一种“开放但需自控”的架构。它强调了 Workflow as Code 的理念，即通过 Python SDK 定义基础设施，这是现代 DevOps 的重要趋势。

4.  **可读性：**
    作为技术文档，结构清晰，逻辑链条明确。但这类文章通常容易陷入“配置步骤”的泥潭，缺乏对“为什么选择 Flyte 而非 Airflow/Kubeflow”的深刻对比分析，可能会让决策者感到困惑。

5.  **行业影响：**
    这篇文章反映了 MLOps 行业的一个明显趋势：**从“单一平台垄断”向“可组合架构”转变**。企业不再希望被一家云厂商绑定所有工具，而是倾向于使用开源的编排层（如 Flyte）来调度底层云厂商（AWS）的计算资源。这有助于推动 MLOps 标准化的进程。

**可验证的检查方式**

1.  **成本效率对比实验：**
    *   *指标：* 对比在相同吞吐量下，使用 Union.ai on EKS 与使用 AWS SageMaker Pipelines 的总拥有成本（TCO）。
    *   *观察窗口：* 连续运行 3 个月的混合工作负载（包含高频小任务和低频大任务）。

2.  **冷启动延迟测试：**
    *   *指标：* 测试 Flyte 在 E

---
## 技术分析

# 技术分析

## 1. 核心架构与逻辑

文章主要探讨了一种基于云原生架构的机器学习工作流管理方案，即利用 Union.ai 将 Flyte 编排平台部署于 Amazon EKS 之上。

*   **架构定位**：该方案将 Flyte 作为任务编排层，Amazon EKS 作为底层容器调度基础设施，Union.ai 则提供管理平面。这种分层设计旨在实现计算逻辑与基础设施的解耦。
*   **核心逻辑**：通过 Kubernetes 的容器化能力，Flyte 将数据处理、模型训练和部署等环节标准化为可复用的任务单元。EKS 提供了所需的弹性伸缩和高可用性支持，而 Union.ai 简化了这一技术栈的部署与运维复杂度。

## 2. 关键技术机制

*   **工作流编排**：
    Flyte 采用“工作流即代码”的模式，允许开发者使用 Python SDK 定义任务和工作流。系统将这些代码构建为有向无环图（DAG），由 Flyte Propeller 负责在 Kubernetes 集群上进行调度和执行。
*   **数据传递与存储**：
    在任务间的数据传递上，Flyte 避免了直接传输大型数据集。它将数据存储在 Amazon S3 等后端存储系统中，任务之间仅传递数据的引用（指针）。这种机制减少了序列化开销和网络传输压力，适合处理大规模数据集。
*   **资源调度与弹性**：
    基于 EKS，该方案支持动态资源分配。通过集成 Karpenter 或 Cluster Autoscaler，集群可以根据待处理任务的资源需求（如 CPU/GPU）自动调整节点数量。此外，Flyte 支持在任务级别配置不同的计算资源，例如利用 Spot 实例进行成本优化。

## 3. 工程价值与应用场景

*   **标准化与可复现性**：
    该方案将分散的脚本转化为结构化的流水线，解决了从本地开发环境迁移到生产环境时可能出现的依赖冲突和环境不一致问题，提升了 AI 项目的工程化标准。
*   **成本与效率优化**：
    通过任务级别的缓存机制，系统在输入参数未变更时可直接复用历史执行结果，避免重复计算。结合 EKS 的弹性伸缩能力，企业可以按需使用计算资源，降低持续运维和大规模训练的成本。
*   **适用场景**：
    该技术栈适用于需要处理复杂依赖关系的机器学习流水线，包括数据预处理、大规模模型训练以及周期性的批量推理任务。

---
## 最佳实践

## 最佳实践指南

### 实践 1：容器化与资源优化

**说明**: 在 Amazon EKS 上运行 AI 工作负载时，容器镜像的大小和启动速度直接影响工作流的执行效率。使用轻量级基础镜像（如 Minimal Python 或 Alpine）并合理配置 Flyte 任务资源请求与限制，可以避免资源浪费并提高集群吞吐量。

**实施步骤**:
1. 使用多阶段构建优化 Dockerfile，仅保留运行时必需的依赖。
2. 为 Flyte 任务设置合理的 `memory` 和 `cpu` 限制（通过 `@task` 装饰器或 Flyte propeller 配置）。
3. 利用 EKS 的 Cluster Autoscaler 和 Karpacker 配合 Spot 实例以优化成本。

**注意事项**: 避免在容器镜像中打包大型数据集，应使用 S3 或 EFS 进行数据挂载。

---

### 实践 2：利用 Flyte 后端插件实现高性能数据访问

**说明**: AI 工作流通常涉及大量数据传输。直接在容器内传递数据会导致序列化开销和性能瓶颈。最佳做法是利用 Flyte 的后端插件（如 S3）将大型数据集、模型权重和中间结果直接传递到对象存储，任务之间仅传递指针。

**实施步骤**:
1. 配置 Flyte 的 `raw-output-prefix` 指向 Amazon S3 路径。
2. 在任务定义中，使用 `FlyteFile` 和 `FlyteDirectory` 类型注解来处理大型文件。
3. 确保执行 Pod 的 IAM Role（通过 IRSA）具有读写 S3 的权限。

**注意事项**: 确保数据存储与 EKS 集群处于同一区域以减少网络延迟和跨区域传输成本。

---

### 实践 3：构建可扩展的模型训练与推理任务

**说明**: Union.ai 和 Flyte 支持 MPI（消息传递接口）和分布式训练框架（如 PyTorch DDP, Ray）。对于大规模模型训练，不应局限于单 Pod 任务，而应利用 Flyte 的分布式任务插件在 EKS 上启动多 Pod 副本进行并行计算。

**实施步骤**:
1. 在 Flyte 任务中启用分布式训练插件，配置 `num_nodes` 和 `gpus_per_node`。
2. 使用 EBS CSI 驱动器提供的动态置备功能，为训练任务挂载高性能 EBS 卷（如 io2 或 gp3）。
3. 利用 Node Groups 或 Karpacker 配置支持 GPU 的实例组（如 p4d 或 g5）。

**注意事项**: 监控 GPU 利用率，确保 NCCL 或 PyTorch 的网络通信配置正确，特别是在使用 VPC CNI 进行 Pod 间通信时。

---

### 实践 4：工作流版本控制与不可变性

**说明**: 在生产环境中，必须确保工作流的定义和代码是可追溯且不可变的。Flyte 将工作流定义注册在控制平面中，与代码解耦。最佳实践是使用特定的项目/域命名约定，并确保容器镜像标签与 Git Commit SHA 绑定。

**实施步骤**:
1. 在 CI/CD 流水线中构建镜像时，使用 Git Commit Hash 作为镜像标签，而非 `latest`。
2. 使用 `flytectl` 或 Union CLI 注册工作流，明确指定 `--project` 和 `--domain`（如 `development`, `staging`, `production`）。
3. 启用 Flyte 的沙箱功能，确保生产环境的任务无法随意修改代码或配置。

**注意事项**: 避免在任务定义中使用硬编码的配置，应通过 Flyte 的默认输入或运行时参数传递配置。

---

### 实践 5：利用 Spot 实例优化成本

**说明**: AI 实验和训练任务通常具有容错性，适合使用 Amazon EC2 Spot 实例来显著降低计算成本。通过合理配置 EKS 节点组和 Flyte 的重试策略，可以在保证任务完成的同时最大化成本效益。

**实施步骤**:
1. 创建专门的 EKS 节点组或托管节点组，仅包含 Spot 实例。
2. 在 Flyte 任务配置中，结合 Spot 实例的中断通知设置合理的重试次数。
3. 使用 Flyte 的 `on_failure` 回调机制或 Union.ai 的监控工具处理节点抢占事件。

**注意事项**: 确保检查点机制已就绪，以便在 Spot 实例被回收时能够从最近的检查点恢复训练，而不是从头开始。

---

### 实践 6：安全性与 IAM 权限管理

**说明**: 在 EKS 上运行 AI 工作流需要访问 AWS 资源（如 S3, DynamoDB, SQS）。最佳安全实践是遵循最小权限原则，使用 IAM Roles for Service Accounts (IRSA) 为特定的 Flyte 任务或工作流分配精细的 IAM 权限，而不是为整个节点组分配全局权限。

**实施步骤**:
1. 创建 OIDC 提供商并配置 EKS 集群以支持 IRSA。
2. 为不同的

---
## 学习要点

- 基于您提供的主题 "Build AI workflows on Amazon EKS with Union.ai and Flyte"，以下是总结出的关键要点：
- Flyte 与 Union.ai 的结合为在 Amazon EKS 上构建、编排和管理复杂的 AI 及机器学习工作流提供了一套可扩展且生产级的开源架构。
- 该解决方案通过容器化技术实现了工作流的版本控制、可复现性以及混合云部署，有效解决了 AI 实验室环境与生产环境之间的差异问题。
- 利用 Amazon EKS 的强大算力，该架构能够无缝处理 GPU 加速任务和大规模分布式数据作业，满足高性能计算需求。
- Flyte 的声明式工作流定义将数据流水线与底层基础设施代码解耦，使数据科学家能够专注于业务逻辑而无需管理复杂的运维细节。
- 通过 Union.ai 提供的托管服务或工具，团队可以降低在 Kubernetes 上调度和监控长时间运行的 AI 任务的操作复杂度。
- 该技术栈支持构建“数据感知”的工作流，能够自动追踪数据血缘关系，并智能地跳过已执行的计算步骤以优化资源使用和成本。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [AWS](/tags/aws/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [MLOps](/tags/mlops/) / [Kubernetes](/tags/kubernetes/) / [Amazon S3](/tags/amazon-s3/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*