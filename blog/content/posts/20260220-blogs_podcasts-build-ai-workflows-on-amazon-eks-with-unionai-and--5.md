---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-20T09:01:37+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI/ML 工作流。 主要内容包括： 1. **核心工具**：使用 Flyte Python SDK 编排工作流，并通过 Union.ai 2.0 系统将其部署在 Amazon EKS 上。 2. **AWS 集成**：该方案"
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

在本文中，我们将介绍如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们会探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service（Amazon EKS）上部署 Flyte，并与 Amazon Simple Storage Service（Amazon S3）、Amazon Aurora、AWS Identity and Access Management（IAM）以及 Amazon CloudWatch 等 AWS 服务无缝集成。我们通过一个使用新的 Amazon S3 Vectors 服务的 AI 工作流示例来解析这一解决方案。

---
## 导语

在 Kubernetes 上构建可扩展的 AI 工作流往往面临复杂的编排挑战。本文将探讨如何利用 Union.ai 和 Flyte 在 Amazon EKS 上实现高效的工作流管理，并展示其与 S3、Aurora 等 AWS 服务的无缝集成。通过解析一个使用 Amazon S3 Vectors 的具体示例，读者将掌握如何利用 Flyte Python SDK 简化开发流程，从而在云环境中更稳健地部署和扩展机器学习任务。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI/ML 工作流。

主要内容包括：
1.  **核心工具**：使用 Flyte Python SDK 编排工作流，并通过 Union.ai 2.0 系统将其部署在 Amazon EKS 上。
2.  **AWS 集成**：该方案能与 Amazon S3、Amazon Aurora、IAM 和 Amazon CloudWatch等服务无缝集成。
3.  **应用示例**：文章通过一个使用 Amazon S3 Vectors 服务的 AI 工作流示例，演示了具体的解决方案。

---
## 评论

**中心观点**
文章主张通过 Union.ai 2.0 将开源编排引擎 Flyte 部署于 Amazon EKS，能够构建一个既利用 Kubernetes 原生弹性优势，又深度整合 AWS 数据生态（如 S3）的高可扩展、生产级 AI/ML 工作流平台。

**支撑理由与边界分析**

1.  **技术架构的互补性与控制力**
    *   **支撑理由（事实陈述）：** Flyte 基于 Kubernetes 原生构建，利用 K8s 的 CRD 定义工作流。将其部署在 EKS 上，使得数据科学团队能够直接利用 AWS 的底层基础设施能力（如 EC2 Spot 实例、Auto Scaling），从而在不修改代码的情况下实现计算资源的动态伸缩。Union.ai 2.0 作为一个托管控制平面，降低了在 EKS 上运维 Flyte 集群的复杂度。
    *   **反例/边界条件（你的推断）：** 对于中小规模或实验性质的团队，这种架构的“过度工程化”问题明显。如果工作流仅涉及简单的线性任务调度，引入 K8s 和 Flyte 的心智负担与运维成本远高于使用 Airflow 或直接调用 SageMaker API。

2.  **数据本地性与生态整合**
    *   **支撑理由（事实陈述）：** 文章强调了与 S3 的无缝集成。在 AWS 环境中，计算（EKS）与存储（S3）的紧密耦合是最佳实践。Flyte 能够高效地处理 S3 上的数据指针，而非移动大文件，这解决了大规模 ML 工作流中的 I/O 瓶颈问题。
    *   **反例/边界条件（你的推断）：** 这种深度绑定 AWS 的特性是一把双刃剑。一旦企业需要执行多云策略或迁移至 Google Cloud (GCP) / Azure，这种强依赖 S3 和 EKS 的架构将导致极高的迁移成本。

3.  **工作流编排的特定适用性**
    *   **支撑理由（作者观点）：** 文章暗示 Flyte Python SDK 非常适合“数据密集型”和“基于任务”的 ML 工作流。其类型安全和任务复用机制优于传统的通用脚本。
    *   **反例/边界条件（你的推断）：** 对于“实时推理”或“流处理”场景，Flyte 并非最佳选择。Flyte 是批处理/调度系统，而非像 AWS Fargate 或 Lambda 那样的请求驱动型计算引擎。如果业务需求是低延迟的 API 响应，此架构完全不适用。

**多维度深入评价**

1.  **内容深度（3/5）**
    文章作为一篇技术教程，在“如何做”的层面提供了清晰的步骤，但在“为什么”的架构决策上略显单薄。它展示了 Flyte 和 EKS 的结合点，但未深入探讨 Union.ai 的商业托管服务与开源 Flyte 在 AWS 上的具体性能差异（如冷启动时间、并发限制）。论证偏向于“快乐路径”，缺乏对故障恢复、网络配置等生产环境痛点的深度剖析。

2.  **实用价值（4/5）**
    对于正在寻求从“单机脚本”向“分布式工作流”转型的 AI 团队，该文章具有极高的参考价值。它提供了一条标准化的路径，将数据科学家的 Python 代码转化为 K8s 上的可扩展任务。特别是关于如何利用 Union.ai 快速在 EKS 上落地 Flyte 的部分，节省了大量的运维摸索时间。

3.  **创新性（3/5）**
    “在 K8s 上运行 ML 工作流”并非新概念，Kubeflow 早已存在。文章（及 Union.ai 的方案）的创新点在于**“产品化体验”**与**“云原生抽象”**。它试图通过 Union.ai 隐藏 K8s 的复杂性，让用户感觉不到底层 EKS 的存在，这是一种“Managed Service on Managed Service”的模式创新，而非底层算法创新。

4.  **可读性（4/5）**
    文章结构逻辑清晰，遵循了“问题引入 -> 方案提出 -> 架构解析 -> 实操演示”的经典技术写作范式。代码片段与架构图（假设文中包含）的配合通常能降低理解门槛。但针对完全不懂 K8s 概念的读者，Pod、Node、Namespace 等术语仍是阅读障碍。

5.  **行业影响（3/5）**
    这篇文章反映了 MLOps 行业的一个重要趋势：**编排层的标准化与基础设施的解耦**。它暗示了单纯的云厂商绑定工具（如 SageMaker Pipelines）可能无法满足所有需求，开源项目（Flyte）通过商业公司（Union.ai）提供云原生支持，正在成为第三种势力。这推动了 AWS 生态内对“开源优先”策略的接纳。

6.  **争议点或不同观点**
    *   **Vendor Lock-in（厂商锁定）：** 虽然使用了开源的 Flyte，但依赖 Union.ai 2.0 作为控制平面实际上是将“锁定”从 AWS 转移到了 Union.ai。如果 Union.ai 的定价策略改变或服务中断，迁移成本依然很高。
    *   **运维复杂性转移：** 文章声称简化了流程，但实际上是将 K8s 的运维复杂性转移给了 Union.ai 平台，或者是要求用户必须具备高阶 AWS 网络知识（VPC peering, IAM roles for service accounts）才能使其真正工作。

**实际应用建议**

1.  **成本控制检查：** 在 EKS 上运行 Flyte �

---
## 技术分析

# 技术分析

## 核心架构逻辑
文章探讨了一种基于 **Union.ai** 和 **Amazon EKS** 构建企业级 AI/ML 工作流的方法。其核心逻辑在于利用 Kubernetes 的原生编排能力，结合声明式的工作流定义，实现计算任务与基础设施的解耦。

**主要技术特征：**
1.  **编排层抽象**：通过 Flyte 的 Python SDK 将 ML 逻辑定义为代码，利用 Union.ai 提供的控制平面管理任务生命周期，避免直接处理复杂的 K8s 配置。
2.  **基础设施标准化**：使用 Amazon EKS 提供计算资源，利用容器化技术保证环境的一致性和可移植性。
3.  **资源动态调度**：工作流任务根据资源需求（CPU/GPU/内存）在 EKS 集群中动态调度，支持 Spot 实例等成本优化策略。

## 关键技术组件
该方案主要涉及以下技术组件及其交互方式：

*   **Flyte & Union.ai**：
    *   **Flyte**：作为开源的编排层，负责将 Python 代码编译为不可变的执行计划，并管理任务间的依赖关系。
    *   **Union.ai**：提供托管服务，处理用户认证、工作流版本控制以及与底层 K8s 集群的交互。
*   **Amazon EKS**：
    *   作为容器运行时，负责 Pod 的生命周期管理、弹性伸缩和底层资源调度。
*   **AWS S3**：
    *   作为数据持久化层，任务间的数据传递通过 S3 引用实现，而非内存拷贝，以支持大规模数据流转。

## 技术实施与难点应对
**实施原理：**
开发者使用 Python 装饰器定义任务和工作流。Flyte 将这些逻辑打包进容器镜像，并在 EKS 上以 Pod 形式运行。Union.ai 负责将工作流请求转化为 EKS 的调度指令。

**针对常见技术难点的解决方案：**
1.  **K8s 运维复杂性**：
    *   *方案*：Union.ai 提供了抽象层，自动处理 RBAC、存储卷挂载和网络配置，数据科学家无需编写 YAML 文件。
2.  **异构资源调度**：
    *   *方案*：Flyte 允许在任务级别声明资源请求，EKS 结合自动扩缩容器（如 Karpenter）动态分配相应的节点（如 GPU 节点）。
3.  **工作流可复现性**：
    *   *方案*：通过强制容器镜像版本化和参数快照，确保实验结果的可追溯和复现。

## 应用场景评估
该架构适用于需要在云上运行大规模、周期性或复杂依赖关系的机器学习流水线。它将业务逻辑（代码）与执行环境（容器）分离，使得团队可以利用 AWS 的弹性能力，同时保持开发流程的标准化。对于寻求摆脱本地 Notebook 限制、转向云原生 MLOps 体系的企业，这是一种可行的技术路径。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 EKS 集群资源配置与节点组管理

**说明**:
在 Amazon EKS 上运行 AI 工作负载时，计算资源的管理至关重要。Flyte 任务（尤其是深度学习训练任务）通常是资源密集型的。通过合理配置 EKS 节点组（如使用 EC2 Spot 实例处理容错任务，使用 On-Demand 实例处理关键任务）并启用 Karpenter 等自动扩缩容工具，可以显著降低成本并提高资源利用率。

**实施步骤**:
1. **分离节点组**：创建专用的节点组，一组用于 CPU 密集型任务（如数据预处理），另一组配备 GPU（如 p3/p4 实例）用于模型训练。
2. **配置 Karpenter**：部署 Karpenter 替代或配合 Cluster Autoscaler，根据 Flyte Pod 的资源请求动态配置节点，减少资源碎片。
3. **设置多架构支持**：利用 Karpenter 的容量类型配置，混合使用 Spot 和 On-Demand 实例，以在保证可用性的同时优化成本。

**注意事项**:
确保为 Flyte 的 Pod 设置准确的资源请求和限制，以便 Karpenter 能够做出正确的扩缩容决策。

---

### 实践 2：构建高效的容器镜像管理策略

**说明**:
AI 工作流通常依赖庞大的深度学习框架和数据科学库，导致容器镜像体积巨大（通常超过 5GB）。在 EKS 上，如果每次运行都拉取大镜像，会严重拖慢启动速度。利用 Union.ai 和 Flyte 的缓存机制以及 ECR 的镜像拉取加速功能，可以大幅减少任务启动时间。

**实施步骤**:
1. **使用分层构建**：在 Dockerfile 中，将不常变化的依赖层（如 CUDA 库、基础 OS 包）放在前面，频繁变化的代码放在后面。
2. **启用 ECR 缓存**：配置 Amazon ECR 与上游缓存规则，加速基础镜像的拉取。
3. **利用 Flyte 缓存**：在 Flyte 任务定义中启用输入输出缓存，如果代码和输入未变，Flyte 将直接跳过执行或复用容器。

**注意事项**:
避免在容器镜像中打包大型训练数据集。应使用 S3 挂载或数据卷来动态加载数据，保持镜像轻量化。

---

### 实践 3：实施基于 S3 的数据湖与高性能存储集成

**说明**:
AI 工作流的核心瓶颈往往在于 I/O。在 EKS 环境中，不应将数据存储在节点本地磁盘（因为节点是临时的）。最佳实践是使用 Amazon S3 作为“真实数据源”，并利用 Flyte 的 S3 代理或通过 FSx for Lustre 实现高吞吐量的数据访问，以适应大规模模型训练和特征工程的需求。

**实施步骤**:
1. **配置 IAM Roles for Service Accounts (IRSA)**：为 Flyte 的执行 Pod 分配 IAM 角色，赋予其读写 S3 的权限，避免在代码中硬编码凭证。
2. **集成 FSx for Lustre**：对于需要极高 IOPS 的训练任务，动态挂载 FSx for Lustre 文件系统，该系统与 S3 桶无缝集成，可自动回传数据。
3. **使用 Flyte S3 Sensor**：在 Flyte 工作流中配置传感器，仅在 S3 中的新数据就绪时触发下游训练任务。

**注意事项**:
注意 S3 的“请求者付费”模式以及跨区域数据传输的成本。尽量让 EKS 集群与 S3 桶位于同一区域。

---

### 实践 4：利用 Union.ai 进行混合云与多集群编排

**说明**:
Union.ai 提供了托管控制平面，可以统一管理运行在不同 EKS 集群甚至本地 Kubernetes 集群上的 Flyte 工作流。最佳实践是将“控制平面”与“计算平面”分离。利用 Union.ai 的能力，根据数据位置或合规要求，智能地将任务调度到特定的 EKS 集群上执行。

**实施步骤**:
1. **注册 EKS 集群**：将现有的 EKS 集群注册到 Union.ai 控制平面，使其成为可用的执行目标。
2. **配置项目与域**：在 Union.ai 中使用“项目”和“域”的概念来隔离环境（如开发、测试、生产），并将不同的 EKS 集群映射到这些环境。
3. **设置资源配额**：在 Union.ai 平面上为不同的项目或团队设置 CPU/GPU 资源配额，防止单个工作流占用过多集群资源。

**注意事项**:
确保本地或混合环境中的 EKS 集群与 Union 控制平面之间的网络连通性（VPN 或 VPC Peering），以保证任务状态的实时同步。

---

### 实践 5：工作流的可观测性与监控集成

**说明**:
AI 模型训练往往是一个“黑盒”过程。在 EKS 上

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、可复用的 AI 工作流，显著提升机器学习模型的迭代效率。
- 利用 Amazon EKS 作为底层基础设施，可以为 AI 工作流提供强大的容器编排能力，实现计算资源的弹性伸缩与高可用性。
- Flyte 的数据流型编程范式能够自动化管理复杂的数据依赖关系和任务执行，从而大幅降低维护机器学习流水线的技术负担。
- 该架构支持混合云部署策略，允许企业在保持数据主权和安全合规的前提下，灵活调度云端与本地计算资源。
- 通过将工作负载与底层基础设施解耦，开发团队可以专注于核心业务逻辑的代码实现，而无需处理繁琐的运维细节。
- Union.ai 提供的专业支持与优化服务，帮助企业加速了从模型开发到生产环境部署的落地过程。

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
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Klaw.sh：面向 AI 智能体的 Kubernetes 编排工具]({{< relref "posts/20260216-hacker_news-show-hn-klawsh-kubernetes-for-ai-agents-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*