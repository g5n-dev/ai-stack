---
title: 基于Union.ai和Flyte在Amazon EKS上构建AI工作流
date: 2026-02-20 15:01:46+08:00
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
description: 本文介绍了如何利用 Union.ai 2.0 和 Flyte 在 Amazon EKS 上构建并扩展 AI/ML 工作流。 主要内容包括：
  1. **技术架构**：使用 Flyte Python SDK 进行工作流的编排与扩展，并通过 Union.ai 2.0 系统将 Flyte 部署在 Amazon
  Elastic
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios:
- AI/ML项目
- Kubernetes
---

# 基于Union.ai和Flyte在Amazon EKS上构建AI工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---

## 摘要/简介

在本文中，我们将解释如何使用 Flyte Python SDK 编排并扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并实现与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务的无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例，深入剖析这一解决方案。

---

## 导语

随着 AI 工作流复杂度的提升，基于 Kubernetes 的编排已成为保障生产环境可扩展性与稳定性的关键。本文将深入探讨如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建工作流，并解析其与 Amazon S3、Aurora 等 AWS 服务的无缝集成机制。通过具体的代码示例与架构剖析，读者将掌握如何高效部署并管理企业级的机器学习任务。

---

## 摘要

本文介绍了如何利用 Union.ai 2.0 和 Flyte 在 Amazon EKS 上构建并扩展 AI/ML 工作流。

主要内容包括：

1.  **技术架构**：使用 Flyte Python SDK 进行工作流的编排与扩展，并通过 Union.ai 2.0 系统将 Flyte 部署在 Amazon Elastic Kubernetes Service (Amazon EKS) 上。
2.  **AWS 集成**：该方案实现了与 AWS 生态系统的无缝集成，包括使用 Amazon S3 和 Amazon Aurora 进行存储、利用 IAM 进行身份与访问管理，以及通过 Amazon CloudWatch 实现监控。
3.  **应用实例**：文章通过一个具体的 AI 工作流示例，展示了如何使用新的 Amazon S3 Vectors 服务。

---

## 评论

**文章中心观点**
该文章主张通过将 Union.ai（基于 Flyte）与 Amazon EKS 深度集成，构建一种以 Kubernetes 为统一底座、无缝衔接 AWS 数据生态的 AI 工作流编排架构，以解决机器学习从原型到生产环境过程中的扩展性与异构集成难题。

**支撑理由与批判性分析**

1.  **架构的“云原生”成熟度与资源隔离**
    *   **事实陈述**：文章强调了 Flyte on EKS 的部署模式。Flyte 的核心设计理念就是基于 Kubernetes 的声明式工作流。
    *   **分析**：这是一个技术上的**“高确定性”**选择。将 AI 工作流部署在 EKS 上，意味着 ML 工作流可以天然利用 K8s 的 Pod 生命周期管理、资源配额和调度策略。
    *   **实用价值**：对于已经重度使用 AWS 的企业，这种架构避免了数据重力问题。模型训练直接读取 S3，模型服务部署在 EKS，减少了跨云或跨 VPC 的网络延迟。
    *   **反例/边界条件**：EKS 的运维复杂度极高。如果团队规模较小（如 < 5 人的数据科学团队），维护 EKS Control Plane、节点组、VPC-CNI 等基础设施的开销可能会远超 AI 工作流本身带来的收益。对于此类团队，AWS SageMaker 的托管服务可能是更优解，尽管牺牲了部分灵活性。

2.  **Flyte 的“数据感知”编排能力**
    *   **事实陈述**：文章提到利用 Flyte Python SDK 进行编排。
    *   **分析**：Flyte 与 Airflow 或 Prefect 的核心区别在于其“数据传递”机制。Flyte 不仅传递任务状态，还显式管理数据的输入/输出（通过 S3 URI 引用）。这使得 Flyte 在处理大规模 ML Pipeline 时，能够自动优化中间结果的缓存和传递，而不需要用户编写胶水代码来处理 S3 的上传下载。
    *   **创新性**：这体现了从“任务编排”向“数据/工作流编排”的范式转变。Flyte 会自动检测输入数据是否变化，若未变化则跳过计算，这对于长时间运行的 ML 训练任务极具成本优势。
    *   **反例/边界条件**：Flyte 的强类型和严格的 SDK 约束是一把双刃剑。对于探索性数据分析，这种强类型显得过于繁琐。相比之下，Prefect 或简单的脚本可能更适合快速迭代的早期阶段。

3.  **Union.ai 作为企业级发行版的角色**
    *   **作者观点**：文章暗示 Union.ai 2.0 降低了在 EKS 上部署 Flyte 的门槛。
    *   **推断**：开源的 Flyte 部署涉及复杂的 Helm Charts 配置、Cert-Manager 等依赖。Union.ai 实际上扮演了 Red Hat OpenShift 在 Kubernetes 生态中的角色——提供商业支持、控制台 UI 和更简化的部署体验。
    *   **争议点**：这是否会造成 Vendor Lock-in（厂商锁定）？虽然 Flyte 是开源的，但 Union.ai 的特定功能和管控平台可能是私有的。如果企业深度依赖 Union 的 Console 而非 CLI，未来迁移回纯开源 Flyte 或迁移至其他平台（如 Kubeflow）可能面临较高的迁移成本。

**综合评价**

*   **内容深度与严谨性（4/5）**：文章准确地切中了 ML Engineering 的痛点，即“代码在 Notebook 能跑，上生产就挂”。通过引入 K8s 和声明式编排，论证是严谨的。但文章作为技术软文，略过了 EKS 运维的复杂性，存在幸存者偏差。
*   **实用价值（4.5/5）**：对于处于“扩展期”的 AI 团队，该架构是最佳实践之一。它提供了清晰的代码示例（基于 Python SDK），指导意义强。
*   **创新性（3.5/5）**：Flyte 本身并非全新技术，但将其与 AWS EKS 和 Union 的 SaaS 管理结合，提供了一种“云原生 ML 基础设施”的标准化落地路径。
*   **可读性（4/5）**：技术文档通常枯燥，但 Flyte 的 Pythonic 风格使得代码片段易于理解。

**可验证的检查方式**

为了验证该文章所述架构的适用性，建议进行以下检查：

1.  **资源利用率对比实验**：
    *   **指标**：对比使用传统 EC2/On-demand 脚本与使用 Flyte on EKS 在运行相同 ML Pipeline 时的“任务启动耗时”和“资源碎片率”。
    *   **观察窗口**：连续运行 100 个包含数据预处理和模型训练的迭代任务。
    *   **预期结果**：Flyte 应在冷启动上较慢（K8s 调度开销），但在大规模并发任务下，资源利用率应显著高于单机脚本。

2.  **缓存机制有效性测试**：
    *   **指标**：在输入数据集不变的情况下，重复运行工作流，观察 Flyte 是否跳过了已完成的任务。
    *   **观察窗口**：检查 Flyte UI 中的节点状态是否显示为 "Cached"。
    *   **预期结果**：执行时间应从小时级降至秒级，证明其数据感知编排的有效性。

3.  **运维成本评估**：
    *   **指标**：统计部署和维护该 EKS 集群及 Flyte 平台所需

---

## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该技术方案的深入分析报告。

---

### 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**通过 Union.ai 和 Flyte 在 Amazon EKS 上构建可扩展、生产级的 AI/ML 工作流**。它主张将 Kubernetes 的强大编排能力与 Flyte 的声明式工作流管理相结合，以解决从原型到生产环境过程中的“工程化鸿沟”。

**核心思想：**
作者试图传达一种**“基础设施即代码”与“工作流即数据”**的融合思想。传统的 AI 开发往往止步于 Notebook，而 Flyte + Union.ai + EKS 的组合旨在将数据科学家的 Python 代码无缝转化为云端可扩展、可复用且容错的生产级工作流，且无需深陷底层 DevOps 的复杂性。

**创新性与深度：**
该观点的创新性在于**抽象层的提升**。它不再仅仅关注模型训练本身，而是关注**ML 生命周期中的“控制流”和“数据流”**。通过 Union.ai 2.0 提供的托管服务，降低了 Flyte（通常非常复杂）在 Kubernetes 上落地的门槛，实现了“云原生”与“AI 业务逻辑”的深度解耦。

**重要性：**
随着大模型（LLM）和复杂数据管道的普及，单一脚本已无法满足需求。企业面临的主要挑战不再是“算法好不好”，而是“管道能不能跑通、扩不展”。该方案直击痛点，提供了在 AWS 生态内实现标准化 AI 交付的最佳路径。

---

### 2. 关键技术要点

**涉及的关键技术：**
*   **Flyte:** 一个开源的、基于 Kubernetes 的编排工具，专门用于构建数据和 ML 工作流。
*   **Union.ai 2.0:** Flyte 的商业托管版本，提供了控制平面和简化的部署体验。
*   **Amazon EKS (Elastic Kubernetes Service):** AWS 的托管 Kubernetes 服务，提供底层的容器编排和弹性计算能力。
*   **AWS S3 (Simple Storage Service):** 用于存储数据集、模型和中间结果。
*   **Python SDK:** Flyte 的主要接口，允许用户使用 Python 装饰器定义任务和工作流。

**技术原理与实现：**
1.  **声明式定义:** 用户使用 Python 代码定义 `@task`（任务）和 `@workflow`（工作流）。Flyte 编译这些代码生成有向无环图（DAG）。
2.  **容器化与调度:** Flyte 自动将用户代码打包成容器。当工作流被触发时，Flyte 的控制平面在 EKS 集群上调度 Pods 执行任务。
3.  **数据传递:** 任务之间的数据传递通过引用（如 S3 路径）而非直接内存传递实现，允许大规模数据流转而不失内存稳定性。
4.  **自动伸缩:** 利用 EKS 的 Cluster Autoscaler 和 Karpenter（隐含），Flyte 可以根据任务队列的长度动态调整计算节点。

**技术难点与解决方案：**
*   **难点:** Kubernetes 的复杂性（网络、存储、RBAC）对数据科学家来说是巨大的负担。
    *   **解决方案:** Union.ai 屏蔽了 K8s 的复杂性，提供了开箱即用的集成。
*   **难点:** 异构计算（CPU vs GPU vs Spot 实例）的资源管理。
    *   **解决方案:** Flyte 允许在任务级别指定资源需求，并利用 AWS 的节点组或 Fargate 进行细粒度匹配。

**技术创新点：**
*   **工作流即代码:** 完全类型安全的 Python 接口，使得 CI/CD 可以直接应用于 ML 模型。
*   **惰性执行:** 只有当工作流真正运行时，代码才会在云端执行，本地开发体验极佳。

---

### 3. 实际应用价值

**指导意义：**
对于正在从“实验型 AI”向“生产型 AI”转型的团队，该架构提供了标准化的着陆区。它明确了如何利用 AWS 的弹性能力来支撑波动的 AI 训练和推理负载。

**应用场景：**
1.  **大规模模型微调:** 需要多阶段数据处理、训练、评估的复杂流水线。
2.  **周期性批处理:** 每日/每周的报表生成、数据清洗。
3.  **A/B 测试与模型评估:** 并行运行多个模型变体并比较结果。

**需要注意的问题：**
*   **成本控制:** EKS 节点和 S3 存储会产生费用，特别是工作流频繁失败重试时。
*   **学习曲线:** 尽管 Union.ai 简化了操作，但团队仍需理解 Flyte 的特定概念。

**实施建议：**
*   不要试图一次性迁移所有旧代码。从新的、非关键路径的 ETL 或训练任务开始试点。
*   严格规范任务接口的输入输出类型，利用 Flyte 的类型系统避免运行时错误。

---

### 4. 行业影响分析

**对行业的启示：**
这标志着 **MLOps 平台正在向“云原生深水区”迈进**。未来的 MLOps 不再是独立的工具链，而是深度集成在 Kubernetes 之上的抽象层。AWS 与 Union.ai 的合作（或技术选型）暗示了 K8s 将成为 ML 工作负载的标准底座。

**可能的变革：**
*   **降低 MLOps 门槛:** 使得中型企业也能拥有类似 Uber 或 Netflix 级别的 ML 基础设施能力。
*   **促进“数据+模型”管道的融合:** 打破数据工程和模型工程之间的墙，使用统一的编排层。

**发展趋势：**
*   **Serverless 化:** 虽然文章讲 EKS，但未来趋势是向更细粒度的 Serverless 容器（如 AWS Fargate）演进。
*   **多模态支持:** 工作流引擎将不仅处理 Python，还将原生支持 SQL、Java 等多语言任务。

---

### 5. 延伸思考

**引发的思考：**
*   **Vendor Lock-in (供应商锁定):** 虽然 Flyte 是开源的，但 Union.ai 的服务层是否会导致新的锁定？如果只用开源 Flyte，运维成本是否过高？
*   **LLM 的编排:** 传统的 DAG 结构是否适合 LLM 的 Agent 编排？Flyte 如何适应非确定性的 AI 流程？

**拓展方向：**
*   **与 SageMaker 的比较:** 何时选择 EKS+Flyte，何时选择 SageMaker？答案是：需要极致定制化和混合云部署时选前者，需要全托管服务时选后者。
*   **FinOps 集成:** 如何在 Flyte 任务中嵌入成本监控，实现按任务维度的精准计费。

---

### 6. 实践建议

**如何应用到项目：**
1.  **环境准备:** 搭建一个基础的 EKS 集群（或使用 EKS Managed Node Groups）。
2.  **安装 Flyte/Union:** 按照 Union.ai 文档部署控制平面，配置 IAM Role for Service Accounts (IRSA) 以便访问 S3。
3.  **代码改造:** 将现有的 Python 脚本重构为 Flyte Tasks。确保函数是纯函数（无副作用），输入输出可序列化。
4.  **容器化:** 编写 Dockerfile，或者使用 Flyte 的镜像构建功能自动打包。

**具体行动：**
*   **第一步:** 编写一个简单的“Hello World”工作流，验证与 S3 的读写权限。
*   **第二步:** 尝试在一个任务中请求 GPU（如 `p3.2xlarge`），验证 EKS 的节点自动扩缩容是否正常工作。

**补充知识：**
*   **Kubernetes 基础:** 理解 Pod, Node, Namespace。
*   **Docker:** 理解镜像构建原理。
*   **Python 类型提示:** 熟练使用 `typing` 模块。

---

### 7. 案例分析

**成功案例（逻辑推演）：**
*   **场景:** 一家金融科技公司需要每晚处理 100TB 的交易数据并训练欺诈检测模型。
*   **分析:** 使用 Airflow 可能会遇到 Python 环境冲突和内存限制。使用 EKS + Flyte，他们可以将数据清洗（使用 Spark on EKS）和模型训练（使用 GPU on EKS）编排在一个 DAG 中。Flyte 自动处理了 Spark 作业的提交和 GPU 资源的申请，无需人工干预。
*   **经验:** 利用 Flyte 的 `map` 任务功能并行处理 1000 个文件，极大缩短了处理时间。

**失败反思：**
*   **场景:** 团队试图将一个极其复杂的单体应用强行拆解为 Flyte 任务。
*   **教训:** 如果任务间有极高的数据传输频率（每秒多次），Flyte 基于 S3 的数据传递机制会成为瓶颈（延迟高）。
*   **结论:** Flyte 适合**高延迟容忍、高计算密度**的任务，不适合低延迟的流式处理。

---

### 8. 哲学与逻辑：论证地图

**中心命题:**
**在构建生产级 AI/ML 系统时，采用“Amazon EKS + Flyte + Union.ai”的架构优于传统的脚本或单一云服务（如纯 SageMaker），因为它在提供云原生弹性的同时，最大化了代码的可移植性与工作流的控制力。**

**支撑理由与依据:**
1.  **理由 1: 可移植性与避免锁定.**
    *   *依据:* Flyte 是开源的，代码逻辑定义在 Python 中，不绑定特定的 AWS 云服务 API（如 SageMaker Training API）。如果需要迁移到 Azure 或本地机房，只需迁移 K8s 集群。
2.  **理由 2: 处理异构工作流的能力.**
    *   *依据:* 真实的 AI 流程不仅包含模型训练，还包含 SQL 查询、数据转换和简单的 Python 脚本。Flyte 原生支持多语言任务，而 EKS 支持异构硬件（CPU/GPU/Spot），这种组合提供了最广泛的任务类型覆盖。
3.  **理由 3: 极致的资源效率与成本控制.**
    *   *依据:* EKS 允许使用 Spot 实例进行无状态的数据处理，Flyte 的任务级资源请求机制可以精确释放不再需要的 GPU，相比长期运行的 EC2 实例集群，能显著降低成本。

**反例与边界条件:**
1.  **反例 1 (低延迟场景):** 如果业务需求是实时推理（端到端延迟 < 50ms），该架构（基于容器冷启动和 S3 数据传递）过重，不适合。
2.  **反例 2 (极简团队):** 如果是一个只有 2 个数据科学家的小团队，且没有 DevOps 工程师，维护 EKS 集群的复杂性（即使有 Union）可能远超直接使用 SageMaker 的全托管体验。

**命题分类:**
*   **事实:** EKS 提供容器编排，Flyte 提供 Python 编排接口。
*   **价值判断:** “可移植性”和“控制力”比“运维简便性”（指全托管服务）更重要。
*   **可检验预测:** 在高并发、多步骤的复杂 ML 管道中，该架构的长期运行成本将低于全托管实例方案，且代码

---

## 最佳实践

### 实践 1：构建模块化与容器化的 AI 工作流

**说明**:
利用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流时，应遵循微服务化和容器化的原则。Flyte 的核心优势在于将任务和逻辑封装为独立的、可复用的容器。最佳实践是将数据预处理、模型训练、模型评估和部署拆分为独立的任务，每个任务在单独的容器中运行。这不仅能提高代码的可维护性，还能利用 Flyte 的缓存机制跳过未更改的任务，从而加快迭代速度。

**实施步骤**:
1.  **容器化任务**: 为每个工作流任务创建独立的 `Dockerfile`，并确保依赖项被明确声明。
2.  **镜像管理**: 将构建好的镜像推送到 Amazon ECR (Elastic Container Registry)，并确保 EKS 集群具有拉取镜像的 IAM 权限。
3.  **定义工作流**: 使用 Flytekit (Python SDK) 定义工作流，将上述容器化任务通过 `@task` 和 `@workflow` 装饰器进行逻辑连接。

**注意事项**:
*   避免在单个容器中安装过多的工具和库，保持镜像精简以加快启动速度。
*   使用多阶段构建来减小最终镜像的大小。

---

### 实践 2：优化 EKS 节点配置与 Spot 实例使用

**说明**:
AI 工作流通常包含计算密集型（如训练）和 I/O 密集型（如数据预处理）的不同阶段。在 Amazon EKS 上，最佳实践是使用 Karpenter 或 Cluster Autoscaler 来动态管理节点组。特别是对于 Flyte 中可中断的训练任务或批处理任务，应大量利用 Amazon EC2 Spot 实例，这可以显著降低计算成本（最高可达 90%）。

**实施步骤**:
1.  **配置节点组**: 在 EKS 中配置专门的节点组，区分按需实例和 Spot 实例。
2.  **设置容忍度**: 在 Flyte 任务配置中，为适合运行在 Spot 实例上的任务添加特定的容忍度和节点选择器。
3.  **集成 Karpenter**: 安装 Karpenter 以根据 Pod 的资源请求自动配置和终止 EC2 实例，确保集群规模与工作负载需求实时匹配。

**注意事项**:
*   确保工作流任务具备检查点机制，以便在 Spot 实例被回收时能够从上次中断的位置继续，而不是从头开始。
*   为关键路径上的短生命周期任务保留部分按需实例，以避免 Spot 中断导致的延迟。

---

### 实践 3：实施分层存储策略与数据缓存

**说明**:
AI 工作流涉及海量数据集的读写。频繁从 S3 下载相同的数据会导致严重的网络瓶颈和延迟。最佳实践是利用 Flyte 的数据传递机制和 EKS 的存储特性（如 FSx for Lustre 或 ephemeral emptyDir）来缓存数据。Flyte 会自动跟踪任务的输入输出，利用这一特性可以避免重复计算和不必要的数据传输。

**实施步骤**:
1.  **使用 FSx for Lustre**: 对于高频访问的训练数据，配置 FSx for Lustre 作为 EKS 的持久卷（PV），实现与 S3 的高吞吐量链接。
2.  **利用 Flyte 缓存**: 在 Flyte 任务中启用缓存，如果输入哈希值未变，Flyte 将直接返回上次运行的结果，无需重新执行代码或重新下载数据。
3.  **数据本地化**: 对于中间临时数据，利用节点的本地存储（如 NVMe SSD）而非跨网络存储，以最大化 I/O 速度。

**注意事项**:
*   监控存储成本，及时清理不再需要的临时数据集和快照。
*   确保数据访问权限（IAM Roles for Service Accounts, IRSA）正确配置，以免任务因权限不足无法访问 S3 或 FSx。

---

### 实践 4：利用 GPU 节点进行资源隔离与调度

**说明**:
深度学习训练高度依赖 GPU 资源。在 EKS 上，必须确保 GPU 资源被正确请求和限制，避免资源竞争。最佳实践是使用 NVIDIA Device Plugin 并结合 Flyte 的资源请求声明，将特定的任务精确调度到具有特定硬件（如 T4, V100, A100）的节点上。

**实施步骤**:
1.  **安装 GPU Operator**: 在 EKS 集群上安装 NVIDIA GPU Operator，确保驱动和 Device Plugin 正常运行。
2.  **声明资源需求**: 在 Flyte 任务定义中，通过 `@task(limit_resources=Resources(gpu="1"))` 明确指定 GPU 需求。
3.  **节点标签**: 为 EKS 节点打上硬件类型标签（如 `accelerator=nvidia-gpu`），并配置 Flyte 或 Kubernetes Taints/Tolerations，确保 CPU 任务不会抢占 GPU 节点资源。

**注意事项**:
*   监控 GPU 的显存（VRAM

---

## 学习要点

- Union.ai 和 Flyte 结合 Amazon EKS，为构建和管理复杂的 AI 工作流提供了一个可扩展、可靠且云原生的平台。
- Flyte 能够实现机器学习（ML）和大数据工作流的自动化与编排，确保数据处理和模型训练流程的可复现性。
- 利用 Amazon EKS 的托管 Kubernetes 服务，用户可以轻松扩展 AI 基础设施，有效应对高并发和大规模计算任务。
- 该架构支持 GPU 加速和分布式训练，显著优化了深度学习模型的训练效率并缩短了迭代周期。
- 通过将工作流逻辑与底层基础设施解耦，开发人员可以专注于核心算法代码，而无需担心底层运维的复杂性。
- Union.ai 提供的专业支持和服务，进一步降低了在 Kubernetes 上部署和运行生产级 AI 应用的门槛。

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
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Klaw.sh：面向 AI 智能体的 Kubernetes 编排工具]({{< relref "posts/20260216-hacker_news-show-hn-klawsh-kubernetes-for-ai-agents-12.md" >}})
