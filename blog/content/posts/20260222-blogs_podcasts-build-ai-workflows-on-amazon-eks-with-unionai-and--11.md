---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-22T21:21:13+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Amazon S3"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS**（亚马逊弹性 Kubernetes 服务）上构建和扩展 AI 工作流。 主要内容包括： 1. **核心工具**：使用 **Flyte Python SDK** 来编排和扩展 AI/ML 工作"
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

在本文中，我们将解释如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用新型 Amazon S3 Vectors 服务的 AI 工作流示例来探讨这一解决方案。

---
## 导语

随着 AI 工作流的复杂度日益提升，如何基于 Kubernetes 实现高效、可扩展的编排已成为工程团队的关键挑战。本文将详细介绍如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建生产级工作流，并展示其与 S3、Aurora 等 AWS 服务的无缝集成。通过阅读本文，您将掌握使用 Flyte Python SDK 编排任务的具体方法，并了解如何借助 Amazon S3 Vectors 服务优化数据处理流程。

---
## 摘要

以下是对该内容的中文总结：

本文介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS**（亚马逊弹性 Kubernetes 服务）上构建和扩展 AI 工作流。

主要内容包括：
1.  **核心工具**：使用 **Flyte Python SDK** 来编排和扩展 AI/ML 工作流。
2.  **部署架构**：借助 **Union.ai 2.0** 系统，用户可以在 Amazon EKS 上部署 Flyte。
3.  **AWS 集成**：该解决方案实现了与多项 AWS 服务的原生集成，包括 **Amazon S3**（存储）、**Amazon Aurora**（数据库）、**AWS IAM**（身份与访问管理）以及 **Amazon CloudWatch**（监控）。
4.  **应用示例**：文中通过一个具体的 AI 工作流示例，演示了该解决方案的实际应用，其中结合了全新的 **Amazon S3 Vectors** 服务。

---
## 评论

**中心观点**
该文章的核心观点是：利用 Union.ai 2.0 将 Flyte 工作流编排系统部署在 Amazon EKS 上，能够为企业构建一个既具备云原生弹性与可扩展性，又能无缝集成 AWS 数据生态（S3, SageMaker 等）的高可用 AI/ML 基础设施平台。

**支撑理由与评价**

**1. 内容深度：架构耦合度与控制力**
*   **支撑理由（事实陈述）：** 文章深入探讨了“控制平面”与“用户工作负载”的分离架构。这是云原生 MLOps 的关键痛点。文章论证了 Union.ai 如何通过在 EKS 上运行 Flyte，允许用户利用 Kubernetes 的复杂调度能力（如节点亲和性、资源配额），同时保持对 AWS 生态（如 IAM 角色、S3 挂载）的深度集成。这比通用的 Kubeflow 或 Airflow 部署更具针对性地解决了混合云环境下的数据访问控制问题。
*   **支撑理由（作者观点）：** 文章暗示了“单一控制平面”的重要性。通过 Union.ai 托管控制平面，企业可以避免维护复杂的 etcd 和 FlyteAdmin 数据库，这是极具深度的架构取舍，将运维重心从“维护编排工具本身”转移到了“维护业务工作流”上。

**2. 实用价值：解决“最后一公里”的扩展难题**
*   **支撑理由（事实陈述）：** 文章展示了 Flyte Python SDK 的具体用法，特别是如何将 Python 函数直接声明为任务并自动容器化。这对数据科学家极具实用价值，因为它掩盖了 Docker 和 Kubernetes 的复杂性。
*   **支撑理由（你的推断）：** 结合实际案例，对于拥有大量遗留 Python 脚本（如 Pandas/NumPy 处理逻辑）的团队，该方案提供了一条低迁移成本的路径。文章提到的“利用 Spot 实例”进行批处理推理，直接对应了降低 AI 基础设施成本的刚性需求，具有很高的财务指导意义。

**3. 行业影响：推动 MLOps 的“标准化”与“商品化”**
*   **支撑理由（作者观点）：** 此类文章的发布标志着 MLOps 领域正在从“百花齐放”的混乱阶段向“标准化基础设施”阶段过渡。Union.ai 与 AWS 的深度绑定，实际上是在试图确立“企业级 AI 编排”的事实标准。
*   **支撑理由（你的推断）：** 这可能会加速 Airflow 在纯 AI/ML 场景下的替代进程。Airflow 虽然生态成熟，但在处理大规模数据传递和容器原生调度时显得笨重，而 Flyte on EKS 的方案直击这一痛点。

**反例与边界条件**

1.  **过度工程化陷阱（事实陈述）：** 对于初创公司或数据团队少于 5 人的组织，引入 EKS + Union.ai + Flyte 的技术栈过于复杂。维护 Kubernetes 集群（即使是托管版 EKS）的学习曲线和成本，远高于直接使用 SageMaker Pipelines 或甚至简单的 Airflow on EC2。
2.  **供应商锁定风险（你的推断）：** 虽然文章强调云原生，但 Union.ai 的商业版服务本身形成了一种新的锁定。如果用户未来希望脱离 AWS 或更换编排工具，迁移存储在 Union 控制平面中的工作流定义和元数据将面临巨大挑战。
3.  **实时性短板（技术事实）：** Flyte 是基于“批处理”思维设计的。文章未提及该架构在“实时推理”或“流式处理”场景下的局限性。对于毫秒级延迟要求的在线推荐系统，EKS 上的 Flyte 工作流并非最佳选择，此时直接使用 KServe 或 AWS Lambda 更为合适。

**可验证的检查方式**

1.  **成本效益实验（指标）：** 在相同负载下（例如每日处理 10TB 数据），对比“Flyte on EKS (利用 Spot 实例)”与“SageMaker Processing Job”的运行成本。观察 Flyte 的混合调度策略是否能带来 30% 以上的成本节省。
2.  **冷启动延迟测试（观察窗口）：** 部署一个包含深度依赖（如需下载大型模型文件）的 Flyte 任务，测量从触发工作流到 Pod 实际运行的时间。如果冷启动超过 2 分钟，则证明该架构不适用于对延迟敏感的近实时场景。
3.  **扩展性压力测试（指标）：** 模拟并发提交 1000 个工作流实例，观察 EKS 集群的 API Server 响应以及 Flyte 控制平面的数据库写入性能。检查是否存在因控制平面瓶颈导致的任务排队积压。

**总结**
该文章是一篇典型的“架构落地指南”，虽然带有明显的 Union.ai 和 AWS 推广色彩，但准确地抓住了当前企业级 AI 从“实验”走向“生产”过程中的核心痛点——即如何在不牺牲云原生弹性的前提下，实现复杂计算逻辑的编排。对于成熟的数据工程团队，这是一个极具参考价值的架构蓝图；但对于追求快速迭代的早期团队，这可能是一剂“过度设计”的毒药。

---
## 技术分析

# 技术分析：在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流

## 1. 核心架构与设计理念

### 架构定位
文章探讨了一种基于 Kubernetes 的 MLOps 架构模式，即利用 **Union.ai**（作为 Flyte 的托管控制平面）在 **Amazon EKS** 上编排机器学习工作流。该架构旨在解决机器学习生命周期中从开发环境到生产环境的部署一致性问题。

### 核心设计思想
该技术方案体现了 **计算与存储分离** 以及 **声明式工作流** 的设计原则：
*   **基础设施解耦**：通过 Flyte 的 Python SDK 定义业务逻辑，底层的资源调度、容器编排和扩展工作由 EKS 接管。这使得算法工程师无需关注底层基础设施细节。
*   **数据与计算分离**：利用 AWS S3 存储数据集和模型制品，计算资源（EKS Pod）按需启动和销毁，避免了数据与计算节点的强绑定。

---

## 2. 关键技术组件与机制

### 核心组件
1.  **Flyte**：开源的工作流编排框架，基于 Kubernetes 构建，专注于数据和 ML 流程的自动化。
2.  **Union.ai**：提供 Flyte 的托管控制平面，负责管理工作流的调度、版本控制和用户权限，降低了自建控制平面的运维负担。
3.  **Amazon EKS**：提供底层容器编排环境，负责 Pod 的生命周期管理、自动伸缩和节点调度。
4.  **Flyte Python SDK**：允许开发者使用 Python 函数和装饰器（如 `@task`, `@workflow`）定义 DAG（有向无环图）。

### 工作流原理
*   **定义与编译**：用户使用 Python 代码定义任务。Flyte 将这些函数编译为不可变的 DAG 结构，并生成执行计划。
*   **容器化调度**：工作流提交后，Union 控制平面指示 EKS 启动相应的 Pod。每个任务在独立的容器中运行，实现了环境隔离。
*   **数据传递机制**：任务之间的数据传递通过**引用传递**实现。实际数据（如大文件）上传至 S3，任务间仅传递 S3 的 URI 指针。这种机制减少了网络 I/O 开销，避免了数据在节点间的冗余拷贝。

---

## 3. 技术难点与应对策略

### 容错与资源管理
在 Kubernetes 上运行长时间运行的 ML 任务（如模型训练）面临节点失效（尤其是使用 Spot 实例时）的风险。
*   **解决方案**：FlytePropeller（Flyte 在 EKS 侧的组件）持续监控任务状态。一旦检测到节点故障或 Pod 驱逐，它会自动在其他可用节点上重新调度任务，确保工作流的完整性。

### 依赖管理与环境一致性
ML 项目常面临复杂的 Python 依赖冲突（例如不同的 PyTorch 版本）。
*   **解决方案**：采用容器化技术。每个任务可以指定自定义容器镜像。Flyte 支持在任务级别覆盖镜像，确保了特定任务运行在精确依赖的环境中，而不影响其他任务。

### 类型安全
Python 作为动态语言在大型工程中容易产生类型错误。
*   **解决方案**：Flyte 引入了强类型签名。在定义任务时必须指定输入输出类型，Flyte 会在运行前检查类型兼容性，提前拦截潜在的数据流转错误。

---

## 4. 技术优势评估

*   **可移植性**：由于工作流定义基于标准的 Python 和容器镜像，该架构允许工作流在不同的 Kubernetes 环境之间迁移，不仅限于 AWS。
*   **扩展性**：结合 EKS 的 Cluster Autoscaler 和 Karpenter，该架构能够根据工作流的队列长度自动调整计算节点规模，适用于从数据处理到大规模模型训练的各种负载。
*   **开发体验**：通过将工作流定义为代码，开发者可以利用现有的 Git 工具进行版本控制和 CI/CD 集成，实现了“基础设施即代码”在 ML 领域的延伸。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建容器化且模块化的任务

**说明**: 在 Union.ai 和 Flyte 环境中，工作流由多个任务组成。最佳实践是确保每个任务都是独立的、容器化的，并且只做一件事。这种单一职责原则使得任务更易于测试、调试和重用。容器镜像应保持精简，仅包含运行代码所需的必要依赖，以减少启动时间。

**实施步骤**:
1. 为每个工作流任务创建独立的 Dockerfile，利用多阶段构建减小镜像体积。
2. 将业务逻辑代码与 Flyte 装饰器分离，确保代码可以在本地运行以便调试。
3. 在 `@task` 装饰器 中指定容器镜像，并配置必要的资源请求和限制。

**注意事项**: 避免在容器镜像中包含不必要的数据集或大型模型文件，应使用 S3 或 EFS 等存储服务进行数据加载。

---

### 实践 2：利用 Spot 实例优化成本

**说明**: AI 和机器学习工作流通常包含大量的计算任务。利用 Amazon EKS 的 Spot 实例可以显著降低基础设施成本。Flyte 和 Union.ai 允许用户为特定任务配置可中断的节点池。对于容错性较好的训练任务或数据预处理，应优先使用 Spot 实例。

**实施步骤**:
1. 在 EKS 集群中配置包含 Spot 实例的节点组，并为其添加适当的标签（如 `spot: true`）。
2. 在 Flyte 任务定义中，通过 `node_selector` 或 `tolerations` 将特定任务调度到 Spot 节点上。
3. 结合 Flyte 的重试机制，设置合理的重试次数，以应对 Spot 实例可能被中断的情况。

**注意事项**: 确保任务实现了检查点 保存功能，以便在实例中断时能够从上次的位置恢复，而不是从头开始。

---

### 实践 3：实现动态资源分配

**说明**: 不同的 AI 工作负载对资源（CPU、内存、GPU）的需求差异巨大。硬编码资源配置会导致资源浪费或任务失败。最佳实践是根据输入数据的大小或模型复杂度，在运行时动态调整任务所需的资源。

**实施步骤**:
1. 使用 Flyte 的 `Resources` 类在任务内部定义资源需求逻辑。
2. 利用 Python 的 `@dynamic` 工作流或任务参数，根据输入参数动态计算并传递 `mem`、`cpu` 和 `gpu` 的请求值。
3. 在 EKS 端，确保安装了 Cluster Autoscaler，以便根据 Pod 的资源请求自动扩展节点。

**注意事项**: 监控集群的资源利用率，避免设置过高或过低的资源限制，导致任务被 OOMKilled 或节点资源碎片化。

---

### 实践 4：管理数据依赖与缓存

**说明**: AI 工作流通常涉及大规模数据传输。频繁的数据移动会增加延迟和成本。Flyte 提供了自动缓存机制，如果输入参数和代码未更改，它将跳过执行并返回先前缓存的结果。

**实施步骤**:
1. 确保所有数据通过 Flyte 的数据类型传递（如 `FlyteDirectory`, `FlyteFile`），而不是硬编码路径。
2. 在开发阶段，利用 Flyte 的缓存功能加快迭代速度，避免重复执行耗时任务。
3. 对于大型数据集，使用 S3 直传功能，让任务直接从 S3 读写数据，避免通过 Flyte Propeller 中转。

**注意事项**: 在处理不可变数据引用时，明确数据的版本控制，以确保实验的可复现性。

---

### 实践 5：配置 GPU 支持与共享

**说明**: 深度学习训练和推理通常需要 GPU 加速。在 EKS 上，最佳实践包括正确安装 GPU 驱动插件（如 NVIDIA Device Plugin），并配置 GPU 共享以优化利用率。

**实施步骤**:
1. 在 EKS 节点上安装 NVIDIA Device Plugin 和必要的驱动程序。
2. 在 Flyte 项目配置中，启用对 GPU 的支持，并在任务中指定 `gpu` 资源数量和限制（例如 `limits={"gpu": "1"}`）。
3. 考虑使用 GPU 共享技术（如 Time-slicing），让多个轻量级推理任务共享同一个 GPU。

**注意事项**: 确保容器镜像中包含与 EKS 节点驱动兼容的 CUDA 库，否则会导致任务无法调度或运行失败。

---

### 实践 6：集中式日志与可观测性集成

**说明**: 在分布式 EKS 环境中运行 AI 工作流时，调试可能非常困难。最佳实践是将 Flyte 的日志与 Amazon CloudWatch 或 OpenSearch 集成，实现集中式日志管理和指标监控。

**实施步骤**:
1. 配置 EKS 集群的 Fluent Bit 或 CloudWatch Agent，将容器标准输出和错误日志发送到 CloudWatch Logs。
2. 在 Union.ai/Flyte 控制台中配置外部链接，允许用户直接跳转到对应的

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、可维护且高效的 AI 工作流，实现机器学习生命周期的自动化管理。
- 利用 Amazon EKS 的容器编排能力，Flyte 可以无缝调度和管理复杂的 ML 及数据科学流水线，确保资源的高效利用。
- 该架构支持混合云和多云环境，允许企业在不锁定特定云厂商的情况下，灵活部署和运行 AI 任务。
- 通过 Flyte 的声明式工作流定义，数据科学家可以使用 Python 构建可重复且版本化的任务，显著提升模型迭代和实验的效率。
- 集成 Amazon EKS 使得 AI 工作流能够原生利用 AWS 生态系统（如 S3、IAM），增强了安全性与互操作性。
- Union.ai 提供的企业级支持与 Flyte 的开源特性相结合，为大规模 AI 工程化提供了兼顾成本效益与性能的解决方案。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [Kubernetes](/tags/kubernetes/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [AWS](/tags/aws/) / [MLOps](/tags/mlops/) / [Amazon S3](/tags/amazon-s3/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*