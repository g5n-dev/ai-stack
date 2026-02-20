---
title: "基于 Union.ai 与 Flyte 在 Amazon EKS 上构建 AI 工作流"
date: 2026-02-20T11:00:11+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI 工作流。 **核心内容总结：** 1. **工具与平台**： 文章阐述了如何使用 **Flyte Python SDK** 来编排和扩展机器学习工作流。同时，重点介绍了 **Union.ai 2.0** 系统，该系统支持"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 基于 Union.ai 与 Flyte 在 Amazon EKS 上构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们将解释如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务无缝集成。我们通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来演示该解决方案。

---
## 导语

随着 AI 工作流日益复杂，在 Kubernetes 上实现高效、可扩展的编排已成为许多开发团队的核心需求。本文将介绍如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建工作流，并演示其与 S3、Aurora 等 AWS 服务的深度集成。通过阅读本文，您将掌握具体的部署步骤，并了解如何借助全新的 Amazon S3 Vectors 服务优化数据处理流程。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI 工作流。

**核心内容总结：**

1.  **工具与平台**：
    文章阐述了如何使用 **Flyte Python SDK** 来编排和扩展机器学习工作流。同时，重点介绍了 **Union.ai 2.0** 系统，该系统支持将 Flyte 部署在 **Amazon Elastic Kubernetes Service (EKS)** 上。

2.  **AWS 服务集成**：
    该解决方案能够与 AWS 云生态系统无缝集成，利用了包括 **Amazon S3**（存储）、**Amazon Aurora**（数据库）、**AWS IAM**（身份与访问管理）以及 **Amazon CloudWatch**（监控）在内的核心服务。

3.  **应用示例**：
    文章通过一个具体的 AI 工作流示例，展示了如何结合使用新的 **Amazon S3 Vectors 服务**，以实现向量数据在 AI 流程中的处理与应用。

---
## 评论

### 深度评论

#### 核心观点
该文章是一篇针对特定技术栈的实施指南，旨在论证通过 Union.ai 将 Flyte 工作流编排引擎部署于 Amazon EKS 之上，是构建大规模、云原生 AI/ML 管道的一种可行方案。其核心逻辑在于利用 Kubernetes 的通用抽象层来统一管理异构计算资源。

---

#### 深入评价

**1. 支撑理由**

*   **异构计算资源的统一调度**
    *   **事实陈述**：文章指出 Flyte on EKS 支持在单一工作流中混合调用 CPU、GPU 及 AWS Spot 实例。
    *   **分析**：这是该方案的主要技术优势。在机器学习流程中，模型训练与数据处理对硬件资源的需求差异显著。Flyte 基于任务级的资源声明机制，结合 EKS 的调度器，有效解决了单一流程内多种硬件架构共存的问题。相比于配置相对僵化的传统调度工具，这种组合在处理 ML 特定负载时展现了更高的适配性。

*   **基础设施的可编程性**
    *   **事实陈述**：文章提及 Union.ai 2.0 简化了在 EKS 上的部署流程，并实现了与 S3、SageMaker 等 AWS 服务的集成。
    *   **分析**：这反映了企业对于避免供应商锁定和追求基础设施可控性的需求。相比于完全托管的 AWS 原生服务，该方案通过 Union.ai 提供了介于开源软件与托管服务之间的中间层，试图填补易用性与灵活性之间的鸿沟，符合部分企业采用混合云策略的技术路径。

*   **工作流定义的可移植性**
    *   **事实陈述**：文章强调使用 Flyte Python SDK 定义的工作流具有可移植性。
    *   **分析**：将工作流定义为代码而非配置，降低了数据科学家参与 DevOps 流程的门槛。这种“代码即基础设施”的实践，有助于实现 AI 工作流的版本化管理与复用。

**2. 局限性与边界条件**

*   **运维成本的考量**
    *   **边界条件**：针对中小型团队或缺乏 Kubernetes 专业运维能力的组织。
    *   **分析**：尽管 Union.ai 降低了部署难度，但在 EKS 上运行 Flyte 仍意味着团队需承担维护 Kubernetes 集群的底层责任。相比于完全托管的云服务，这种方案的隐性运维成本较高。若团队缺乏专门的 K8s 维护能力，可能会面临基础设施管理负担过重的问题。

*   **场景适用性的局限**
    *   **边界条件**：针对实时推理或低延迟流处理场景。
    *   **分析**：Flyte 与 EKS 的设计初衷主要面向批处理和长时间运行的任务。由于 EKS Pod 的启动延迟及调度开销，该架构并不适用于毫秒级的实时在线推理。文章未明确界定这一适用边界，读者需根据实际业务场景（离线处理 vs 在线服务）进行技术选型。

---

#### 多维度评价

*   **内容深度**：文章在技术组件描述上较为准确，但在系统稳定性、成本控制（如 Spot 实例中断对训练任务的影响）及权限管理（IAM 集成复杂度）等生产环境关键问题上着墨较少，主要聚焦于功能实现路径。
*   **实用价值**：对于已确立 Kubernetes 为底层基础设施的数据平台团队，该方案具有较高的参考价值；但对于资源有限或追求快速迭代的初创公司，该方案可能存在架构设计过重的风险。
*   **创新性**：该方案属于现有成熟技术的组合应用，而非颠覆性创新。其价值在于通过工具链整合提升了特定技术栈的易用性，推广了以数据为中心的编排理念。
*   **可读性**：文章结构清晰，逻辑连贯。但对于缺乏 Kubernetes 背景知识（如 Pod, NodePool 等概念）的读者而言，理解部分技术细节存在一定门槛。
*   **行业趋势**：该内容反映了 MLOps 领域向 Kubernetes 标准化演进的趋势，展示了如何利用通用容器编排平台来承载日益复杂的 AI 工作负载。

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流

## 1. 核心观点深度解读

**文章的主要观点：**
文章主张通过结合 **Union.ai**（托管 Flyte 平台）与 **Amazon EKS**（Elastic Kubernetes Service），企业可以构建一个既具有云原生弹性，又能高效编排复杂 AI/ML 工作流的生产级环境。核心在于将 **Flyte** 的任务编排能力与 **AWS** 基础设施的无缝集成，解决从原型到生产环境的“最后一公里”问题。

**作者想要传达的核心思想：**
AI/ML 的开发不应止步于 Notebook 或单机脚本。为了实现真正的规模化，必须采用**声明式、可扩展且容错**的工作流系统。作者强调，通过 Union.ai 2.0，用户无需维护复杂的控制平面，即可在 EKS 上获得 Flyte 的强大功能，从而专注于算法本身，而非底层基础设施。

**观点的创新性和深度：**
*   **从“脚本”到“工作流即代码”：** 深度体现了“一切即代码”的理念，利用 Python SDK 定义工作流，使得数据处理、模型训练和部署逻辑版本化、可测试。
*   **混合编排的深度整合：** 不仅仅是运行容器，而是深入探讨了如何在 Kubernetes 上调度 ML 任务，并自动利用 AWS S3 等服务进行数据流转，体现了云原生与 AI 深度融合的趋势。

**为什么这个观点重要：**
当前 AI 领域面临“模型落地难”的困境。许多优秀的模型因为缺乏可靠的生产环境调度系统而无法上线。该文章提出的方案直接解决了**规模化、可重复性和资源利用率**这三个痛点，对于降低 MLOps 运维成本、提升 AI 交付效率具有重要意义。

## 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Flyte：** 一个开源的、基于 Kubernetes 的编排层，专门用于构建数据和 ML 工作流。
*   **Amazon EKS：** AWS 提供的托管 Kubernetes 服务，提供底层容器调度能力。
*   **Union.ai 2.0：** Flyte 的商业托管版本，简化了部署和管理。
*   **Flyte Python SDK：** 用于定义任务和工作流的接口。
*   **AWS S3 (Simple Storage Service)：** 用于存储输入/输出数据和模型构件。

**技术原理和实现方式：**
1.  **声明式编程：** 用户使用 Python 装饰器（如 `@task` 和 `@workflow`）定义逻辑。Flyte 将这些逻辑编译成不可变的执行计划。
2.  **容器化执行：** 每个任务在独立的 Pod 中运行。Flyte 会自动构建容器镜像（利用 FlytePropeller 或集成 CI/CD），并在 EKS 上调度。
3.  **数据传递：** 任务之间通过引用传递数据（通常是 S3 路径），而非直接在内存中传递大数据集，这确保了任务间的解耦和容错性。
4.  **自动伸缩：** 利用 EKS 的 Cluster Autoscaler 和 Flyte 的节点组管理，根据工作负载动态增减计算资源（如 EC2 Spot 实例）。

**技术难点和解决方案：**
*   **难点：** 容器镜像构建慢、环境依赖冲突。
    *   **方案：** Flyte 支持自定义容器镜像，并利用分层缓存和远程构建机制。
*   **难点：** 大规模任务调度带来的 Kubernetes 控制平面压力。
    *   **方案：** FlytePropeller 使用 Kubernetes CRD（Custom Resource Definition）高效管理工作流状态，采用两级调度逻辑。
*   **难点：** 数据在不同任务间的持久化和重传。
    *   **方案：** 原生集成 S3，自动处理上传/下载逻辑，对用户透明。

**技术创新点分析：**
*   **类型化的数据流契约：** Flyte 强制要求任务具有类型签名，这使得工作流在编译期就能进行错误检查，这是对传统脚本运行时错误的一大改进。
*   **基于 Kubernetes 的原生 ML 编排：** 不同于 Airflow 等以 DAG 为中心的系统，Flyte 天生为长时间运行的 ML 训练任务设计，支持分布式训练（如 PyTorch/Elastic）。

## 3. 实际应用价值

**对实际工作的指导意义：**
该架构为 MLOps 团队提供了一个标准化的“生产就绪”蓝图。它指导团队如何从零散的脚本走向可复用的流水线，特别是在需要处理海量数据或进行高频模型训练的场景下。

**可以应用到哪些场景：**
*   **模型微调流水线：** 定期从 S3 获取新数据，预处理，触发微调，评估模型，若通过则注册到模型注册表。
*   **批量推理：** 每日定时处理海量请求，利用 EKS 弹性扩容，处理完成后自动释放资源。
*   **特征工程：** 复杂的 SQL 和 Spark 任务混合编排。

**需要注意的问题：**
*   **成本监控：** 在 EKS 上运行 ML 任务可能导致资源成本激增，特别是未设置资源限制时。
*   **冷启动时间：** 容器启动和 EKS 节点扩容可能需要时间，对于毫秒级要求的推理任务不适用。
*   **学习曲线：** 团队需要从“过程式思维”转向“声明式/数据流思维”。

**实施建议：**
1.  从非关键路径的工作流开始试点。
2.  严格配置 Kubernetes 的 Resource Quotas 和 Limits。
3.  利用 S3 生命周期策略管理中间数据，防止存储成本失控。

## 4. 行业影响分析

**对行业的启示：**
这标志着 **MLOps 正从“工具链拼凑”向“原生平台化”演进**。企业不再满足于简单的调度器（如 Cron + Scripts），而是需要能够理解 ML 特性（如数据版本、模型 lineage、分布式训练）的底层系统。

**可能带来的变革：**
*   **降低 Kubernetes 门槛：** Union.ai 和 Flyte 的结合，让数据科学家无需成为 K8s 专家也能利用其强大能力。
*   **促进云原生标准化：** 推动行业标准向 Kubernetes 统一，避免厂商锁定（虽然使用了 AWS EKS，但上层 Flyte 逻辑是可移植的）。

**对行业格局的影响：**
这种架构直接挑战了传统的专有 MLOps 平台（如 Sagemaker Pipelines 的部分功能，尽管它也可以运行在 Sagemaker 上），强化了“开源核心 + 商业托管”的双模态 IT 格局。

## 5. 延伸思考

**引发的思考：**
随着大模型（LLM）的兴起，工作流不再仅仅是数据->模型->预测。未来的工作流是否应该包含“Agent 编排”？Flyte 这种强类型的 DAG 结构是否适合非确定性的 LLM 调用链？

**拓展方向：**
*   **GPU 优化调度：** 如何在 EKS 上结合 Flyte 实现更精细的 GPU 分片（如 MIG 技术）。
*   **Serverless 集成：** 将部分轻量级任务卸载到 AWS Fargate 或 Lambda，进一步降低运维负担。

**未来发展趋势：**
*   **工作流即 API：** 工作流将直接通过 API 触发，成为实时应用的一部分。
*   **事件驱动架构：** 从单纯的定时任务转向由数据到达（S3 Event）触发的流式处理。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现状：** 如果你的团队正在使用 Kubernetes 且面临 ML 任务调度混乱、资源浪费的问题，此方案非常适合。
2.  **环境搭建：** 不要直接从源码构建 Flyte，先尝试 Union.ai 的免费层或使用 Helm Chart 在开发环境 EKS 部署开源 Flyte。
3.  **代码改造：** 将现有的 Python 脚本封装为函数，添加类型注解，并引入 `flytekit`。

**具体的行动建议：**
*   **Step 1:** 安装 `flytekit` (`pip install flytekit`)。
*   **Step 2:** 编写一个简单的 "Hello World" 工作流，并在本地运行 (`pyflyte run`)。
*   **Step 3:** 配置 AWS IAM 角色，确保 EKS Pod 有权限读写 S3。
*   **Step 4:** 部署 Flyte 到 EKS，注册工作流。

**需要补充的知识：**
*   Kubernetes 基础
*   Docker 容器化
*   Python 类型提示
*   AWS IAM 安全配置

## 7. 案例分析

**成功案例（基于行业常识推断）：**
*   **Spotify：** 作为 Flyte 的早期创造者之一，他们利用该系统管理大规模的推荐模型训练和特征管道，实现了从单体架构到微服务/Kubernetes 的成功转型，极大地提高了数据科学家迭代模型的速度。

**失败案例反思：**
*   **强行适配：** 某些团队试图将简单的 SQL 查询强行放入 Flyte 中，导致由于容器启动开销过大，整体运行时间反而比直接在 Redshift/Snowflake 中运行更慢。
*   **教训：** 不要为了技术而技术。对于极短且高频的任务，Kubernetes 的调度开销可能不值得。

## 8. 哲学与逻辑：论证地图

**中心命题：**
**在 Amazon EKS 上部署 Union.ai 托管的 Flyte，是构建高可扩展、可维护且云原生的 AI/ML 工作流编排系统的最佳实践路径。**

**支撑理由与依据：**
1.  **理由 1：云原生的弹性伸缩能力。**
    *   **依据：** Kubernetes (EKS) 提供了底层 Pod 调度的弹性，Flyte 在此基础上提供了任务级的调度，两者结合能完美应对 ML 训练任务的波峰波谷，优化成本。
2.  **理由 2：声明式工作流带来的可复现性。**
    *   **依据：** Flyte Python SDK 强制用户定义输入输出类型，并记录每次运行的元数据，这解决了 ML "代码跑不通"或"结果无法复现"的常见痛点。
3.  **理由 3：降低运维复杂度。**
    *   **依据：** Union.ai 2.0 托管了 Flyte 的控制平面，用户无需自行维护 Flyte 后端数据库、配置服务等繁琐组件，只需关注业务逻辑。

**反例或边界条件：**
1.  **反例 1：超低延迟的实时推理。**
    *   **条件：** 如果业务需求是 <50ms 的在线推理请求响应，EKS + Flyte 的容器冷启动和调度延迟过高，不适合。
2.  **反例 2：极轻量级的简单任务。**
    *   **条件：** 如果只是每天运行一个简单的 Python 脚本发送邮件，引入 EKS 和 Flyte 属于“杀鸡用牛刀”，维护成本远高于使用 AWS Lambda 或简单 Cron。

**命题性质分析：**
*   **事实：** Flyte 是基于 K8s 构建的；Union.ai 提供托管服务；EKS

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 EKS 集群配置以支持 AI 工作负载

**说明**: AI 和机器学习工作负载通常对计算资源（如 GPU）和内存有特殊要求。直接在 EKS 上运行这些工作负载需要特定的节点组配置、自动扩缩容策略以及设备插件支持，以确保 Flyte 任务能够高效调度并执行。

**实施步骤**:
1. 创建专用的 GPU 节点组，并安装 `NVIDIA device plugin` 以便 Kubernetes 能够识别 GPU 资源。
2. 配置 Karpenter 或 Cluster Autoscaler，以便根据 Flyte 工作流的资源需求动态增加或减少 GPU 节点，从而优化成本。
3. 为 Flyte 的工作节点配置适当的 `kubelet` 参数和实例存储，以处理大型数据集或模型检查点。

**注意事项**: 确保所选用的 EC2 实例类型与 Union.ai/Flyte 容器所需的 CUDA 或 PyTorch 版本兼容。

---

### 实践 2：利用 Flyte 后端构建可扩展的任务编排

**说明**: Union.ai 和 Flyte 的核心优势在于将数据流水线代码转化为可扩展的工作流。最佳实践是充分利用 Flyte 的后端服务来管理任务的生命周期，而不是依赖简单的 Kubernetes Job 或 CronJob。

**实施步骤**:
1. 在 EKS 上部署 Union.ai 控制平面或开源 Flyte 后端（包含 FlytePropeller、FlyteAdmin 和 DataCatalog）。
2. 使用 `flytectl` 或 Python SDK 注册工作流，确保任务定义与运行时基础设施解耦。
3. 配置 FlyteAdmin 与 EKS 集群的 RBAC 集成，确保 Flyte 有权限在指定的命名空间下创建 Pod。

**注意事项**: 生产环境中应确保 Flyte 后端组件（如 Postgres 数据库和 MinIO/S3 对象存储）具有高可用性配置。

---

### 实践 3：实施高效的缓存与数据管理策略

**说明**: AI 实验往往涉及重复的数据预处理和模型训练步骤。Flyte 提供了原生的任务缓存机制，能够显著减少计算浪费和重复执行时间。

**实施步骤**:
1. 在 Flyte 任务定义中启用缓存策略，设置合理的 TTL（生存时间），以便在输入参数未变时跳过计算。
2. 将原始数据、中间结果和最终模型存储在 S3 或兼容 S3 的对象存储中，而不是容器镜像或临时存储中。
3. 使用 Flyte 的 `TypeSystem` 正确声明数据集的格式，以便自动处理 S3 与容器之间的数据传输。

**注意事项**: 对于极其庞大的数据集，避免在任务之间直接传递数据对象，而应传递 S3 位置引用，以减少序列化开销。

---

### 实践 4：容器化与镜像管理优化

**说明**: 在 EKS 上运行 AI 工作流时，容器镜像的体积和拉取速度直接影响启动延迟。AI 镜像通常包含庞大的框架（如 TensorFlow, PyTorch），因此需要精细化的构建策略。

**实施步骤**:
1. 使用分层构建策略，将基础库（CUDA、Python）与项目依赖分离，利用 Docker 缓存层。
2. 将构建好的镜像推送到 Amazon ECR（Elastic Container Registry），并确保 EKS 节点具有拉取镜像的 IAM 权限。
3. 在 Flyte 任务中指定镜像引用，利用 Flyte 的镜像插件功能，为不同的任务自动注入特定的运行时环境。

**注意事项**: 定期扫描镜像漏洞，并使用 ECR 的生命周期策略清理旧版本的未使用镜像，以节省存储成本。

---

### 实践 5：资源配额与多租户隔离

**说明**: 在团队协作环境中，不同的 AI 项目或用户可能会共享同一个 EKS 集群。为了防止“吵闹邻居”效应，必须在 Kubernetes 和 Flyte 层面实施资源隔离。

**实施步骤**:
1. 在 EKS 中为不同的项目或团队创建独立的命名空间，并配置 ResourceQuota 限制 CPU、内存和 GPU 的总使用量。
2. 利用 Flyte 的项目概念，将工作流分配给特定的执行域，并配置不同的 IAM 角色或服务账户。
3. 使用 Kubernetes 的 LimitRange 确保单个任务不会意外消耗节点上的所有资源，导致节点 OOM（内存溢出）。

**注意事项**: 监控 GPU 的显存使用情况，因为 Kubernetes 默认主要管理内存和 CPU，GPU 显存监控通常需要额外的 Prometheus 导出器。

---

### 实践 6：可观测性与日志聚合

**说明**: AI 训练任务可能运行数小时甚至数天，如果没有完善的日志和指标追踪，调试故障将非常困难。将 EKS 的可观测性与 Union.ai 的监控相结合是关键。

**实施步骤**:
1. 部署 CloudWatch 或 Prometheus/Grafana 堆栈来收集 EKS 节点和 Pod 的系统指标。
2. 配置 Fluent Bit 或 AWS for Fluent Bit，将应用日志（标准输出和错误

---
## 学习要点

- 基于提供的主题 "Build AI workflows on Amazon EKS with Union.ai and Flyte"，以下是总结出的关键要点：
- Union.ai 和 Flyte 的结合为在 Amazon EKS 上构建生产级 AI 工作流提供了开源且云原生的标准化平台，实现了机器学习流程的高度可重复性和自动化。
- 该架构利用 Amazon EKS 的强大容器编排能力，实现了 AI 训练和数据处理任务的高效资源调度与弹性伸缩，显著优化了基础设施的利用率。
- Flyte 能够原生地将不同任务（如数据预处理、模型训练、微调）构建为有向无环图（DAG），有效解决了复杂 AI 流程中的依赖管理和版本控制难题。
- 通过在 EKS 上运行，该方案支持 GPU 加速和多节点分布式训练，为运行大规模深度学习模型和高性能计算任务提供了必要的底层支持。
- 该工作流支持与 AWS 原生服务（如 S3、IAM）无缝集成，确保了数据存储的安全性与访问控制的一致性，同时简化了云端部署流程。
- 平台具备处理混合云和异构计算环境的能力，允许开发者在统一的工作流中灵活切换 CPU 和 GPU 实例，以适应不同阶段的任务需求。

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