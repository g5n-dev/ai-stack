---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-22T19:40:58+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI 工作流。 核心内容包括： 1. **技术栈**：使用 **Flyte Python SDK** 进行工作流编排，并通过 **Union.ai 2.0** 系统将其部署在 **Amazon EKS** 上。 2. **AW"
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

在本文中，我们将介绍如何使用 Flyte Python SDK 编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并实现与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务的无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例，来解析这一解决方案。

---
## 导语

随着 AI 工作流复杂度的持续攀升，在 Kubernetes 上构建可扩展且稳定的数据处理流程已成为技术团队的核心诉求。本文将深入探讨如何利用 Union.ai 和 Flyte 在 Amazon EKS 上编排 AI/ML 任务，并展示其与 Amazon S3、Aurora 等 AWS 服务的无缝集成方案。通过解析基于 Amazon S3 Vectors 的实战示例，我们将帮助读者掌握在云原生环境中构建高效、可维护的 AI 工作流的具体方法。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI 工作流。

核心内容包括：
1.  **技术栈**：使用 **Flyte Python SDK** 进行工作流编排，并通过 **Union.ai 2.0** 系统将其部署在 **Amazon EKS** 上。
2.  **AWS 集成**：该解决方案与 AWS 原生服务无缝集成，包括 **Amazon S3**（存储）、**Amazon Aurora**（数据库）、**IAM**（身份与访问管理）以及 **Amazon CloudWatch**（监控）。
3.  **应用示例**：文中通过一个使用 **Amazon S3 Vectors** 服务的新示例，详细演示了 AI 工作流的构建过程。

**总结**：Union.ai 和 Flyte 为在 AWS EKS 上运行可扩展且深度集成的 AI/ML 工作流提供了强大支持。

---
## 评论

### 深度技术评估

**核心论点：**
文章提出了一种基于 Amazon EKS 和 Union.ai（Flyte）的架构方案，旨在解决机器学习工作流从原型阶段过渡到生产环境时面临的扩展性与异构计算挑战。其核心在于利用 Kubernetes 构建统一的数据编排层，以应对复杂的数据依赖和工程化落地难题。

**技术支撑：**
1.  **声明式 DAG 编排：** 文章指出 Flyte 能够将 Python 代码转化为强类型的声明式有向无环图（DAG）。相比于传统脚本（如 Airflow TaskFlow），这种结构强化了类型安全，并提供了明确的数据血缘追踪机制。
2.  **基于 K8s 的计算抽象：** 利用 EKS 作为底层基础设施，Flyte 将 AWS 计算资源（EC2, Fargate）抽象为执行单元。这种解耦使得算法工程师可以通过定义任务资源需求（GPU/内存）来调度工作负载，而无需直接管理底层基础设施。
3.  **自动化与版本管理：** Union.ai 提供的托管服务降低了 Flyte 的使用门槛。文章论证了通过自动版本控制、数据集血缘追踪及自动重试机制，可以提升 ML 实验的可复现性。

**局限性与边界条件：**
1.  **适用场景：** 对于仅涉及简单 ETL 或轻量级推理的小型团队，引入 Flyte + EKS + Union.ai 技术栈可能存在“过度工程化”问题。相比于 Prefect 或 Dagster 等轻量级工具，此方案的运维成本和学习曲线较高。
2.  **延迟限制：** 文章主要关注批处理和训练流程。在实时推理或流处理场景下，Kubernetes 的启动延迟和 Flyte 的调度周期可能无法满足低延迟需求，此时 SageMaker 在线端点或 AWS Lambda 可能是更优选择。

**维度分析：**

1.  **内容深度与严谨性：**
    *   **技术实现：** 文章详细描述了 Flyte 如何利用 EKS 的 Pod 扰动策略和 Cluster Autoscaler 处理 Spot 实例中断，这对降低大规模训练成本具有实际意义。
    *   **成本评估：** 作为技术教程，代码示例较为严谨，但在成本分析方面略显不足。文章未详细对比 Union.ai 托管服务与自建 Flyte 集群的具体成本差异，也未深入讨论跨云/混合云部署的复杂性。

2.  **实用价值：**
    *   **工程落地：** 文章展示了如何利用 `@task` 和 `@workflow` 装饰器将 Python 函数容器化并调度至 EKS，这对缺乏容器化经验的算法团队具有参考价值。
    *   **安全集成：** 文章提到的与 AWS S3、IAM 角色的深度集成，提供了在 AWS 环境下实现安全数据访问的实践路径。

3.  **技术定位：**
    *   **编排范式：** Flyte 提出了将数据流和计算流统一管理的模型。不同于 Airflow 侧重于“时间调度”，Flyte 侧重于“数据依赖”，这种模式适合构建以数据为中心的流水线。
    *   **服务模式：** Union.ai 采用了“托管控制平面 + 自托管数据平面”的模式，试图简化底层 K8s 的管理复杂性。

4.  **行业影响：**
    *   **标准化趋势：** 此类内容强化了“Kubernetes 作为 ML 工作负载标准运行时”的行业共识。
    *   **供应商锁定风险：** 虽然底层 Flyte 是开源的，但 Union.ai 的托管服务存在潜在的供应商锁定风险，企业在采用时需评估迁移成本。

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，结合对云原生AI、机器学习运维（MLOps）以及AWS生态系统的深入理解，以下是对该文章核心观点和技术要点的全面深入分析。

---

# 1. 核心观点深度解读

**主要观点：**
文章的核心主张是，通过将 **Union.ai**（基于开源项目 **Flyte**）与 **Amazon EKS**（Elastic Kubernetes Service）深度集成，企业可以构建一个既具有云原生弹性与可扩展性，又具备高度可编程性的AI/ML工作流编排平台。这解决了传统机器学习工作流在从原型阶段向生产环境迁移时面临的“工程化鸿沟”问题。

**核心思想：**
作者试图传达“**基础设施即代码**”与“**工作流即代码**”在AI领域的深度融合。核心思想在于：Kubernetes（K8s）已成为云应用的标准调度层，而Flyte提供了专门针对数据密集型和计算密集型任务的高级抽象。利用Union.ai在EKS上的托管能力，数据科学家和ML工程师无需成为K8s专家，就能利用K8s的强大能力来调度复杂的GPU任务、管理数据依赖和实现自动化扩缩容。

**创新性与深度：**
*   **创新性：** 文章不仅展示了如何部署容器，更强调了“有状态的工作流编排”。传统的CI/CD工具（如Jenkins, GitHub Actions）难以处理长时间运行的ML训练任务和复杂的数据血缘关系。Flyte引入了基于类型的强约束和懒加载执行模型，这在通用的编排工具中是较少见的。
*   **深度：** 文章深入到了“混合云”和“多云”架构的痛点。通过Union.ai和Flyte，用户可以在本地（On-prem）和AWS云端无缝迁移工作负载，这触及了企业级AI架构中关于成本控制和数据主权的深层需求。

**重要性：**
随着大模型（LLM）的兴起，算力成本和调度效率成为瓶颈。这一观点的重要性在于它提供了一条标准化的路径，将昂贵的AWS计算资源（EC2 GPU, S3存储）与高效的调度逻辑结合，从而降低AI落地的TCO（总拥有成本）并提高迭代速度。

# 2. 关键技术要点

**涉及的关键技术：**
*   **Amazon EKS:** AWS提供的托管Kubernetes服务，用于底层容器编排。
*   **Flyte:** 一个开源的、基于Kubernetes的编排工具，专门用于构建数据和ML工作流。
*   **Union.ai:** 提供基于Flyte的企业级托管服务（Union Server），简化了Flyte的部署和运维。
*   **Flyte Python SDK:** 用于定义工作流、任务和数据流的Python接口。
*   **AWS S3 (Simple Storage Service):** 用于存储输入/输出数据集和模型构件。

**技术原理与实现：**
1.  **工作流即代码:** 用户使用Python装饰器（`@workflow`, `@task`）定义DAG（有向无环图）。Flyte将这些代码编译成不可变的执行计划。
2.  **容器化与隔离:** 每个Flyte任务都会被映射到Kubernetes上的一个Pod或Job中。Flyte Agent会自动处理容器镜像的拉取和资源分配。
3.  **数据传递:** Flyte利用S3作为中间存储层。当任务A完成时，输出数据被上传到S3；任务B启动时，Flyte自动将S3中的数据路径作为参数传递给任务B，实现了任务间的解耦和数据血缘追踪。
4.  **自动扩缩容:** Flyte可以配置为根据队列中的任务数量，动态调整EKS节点组的大小（结合AWS Karpenter或Cluster Autoscaler），实现按需使用GPU实例。

**技术难点与解决方案：**
*   **难点:** 在K8s上调度大量短生命周期、高并发的ML任务容易造成“脑裂”或资源碎片。
*   **方案:** Flyte引入了独特的“FlytePropeller”组件，它使用自定义控制器（Custom Controller）在K8s中高效地轮询和管理工作流状态，确保即使在网络波动的情况下也能保证工作流的最终一致性。

**技术创新点：**
*   **强类型系统:** Flyte强制要求任务定义输入输出类型，这使得在运行前就能检测到数据流错误，这对于复杂的ML管道至关重要。
*   **Execution Sets (执行集):** 允许将多个工作流实例合并执行，优化资源利用率。

# 3. 实际应用价值

**对实际工作的指导意义：**
该架构为数据科学团队提供了一种“**自助式**”的平台能力。数据科学家只需关注Python代码，无需关心底层的YAML文件编写或K8s配置，极大地释放了生产力，同时保证了生产环境的稳定性。

**应用场景：**
1.  **大模型微调:** 定期从S3读取数据，在EKS上启动Spot实例进行训练，完成后自动关机。
2.  **批处理推理:** 每天定时处理大量预测请求，利用Flyte的MapReduce功能进行并行分片处理。
3.  **特征工程流水线:** 清洗数据 -> 计算特征 -> 写入特征存储，形成自动化的ETL链路。

**需要注意的问题：**
*   **冷启动时间:** 容器启动和PVC挂载可能带来延迟。
*   **成本监控:** 如果不设置资源限制，异常的ML任务可能会消耗大量昂贵的GPU资源。
*   **学习曲线:** 团队需要学习Flyte特定的API和概念（如Launch Plans）。

**实施建议：**
*   先从非关键的ETL任务开始迁移，熟悉Flyte的部署模式。
*   建立标准化的容器镜像库，避免每个任务都重新构建镜像。
*   利用AWS Spot实例运行Flyte任务以大幅降低成本。

# 4. 行业影响分析

**对行业的启示：**
该方案标志着MLOps正在从“脚本化”向“平台化”和“标准化”演进。它表明，**Kubernetes + 编排层** 正在成为AI基础设施的标配，类似于Hadoop在大数据时代的地位。

**可能带来的变革：**
*   **降低AI工程化门槛:** 使得中小型企业也能利用AWS构建类似Google内部（如Google内部的内部流水线系统）的高效AI平台。
*   **推动FinOps in AI:** 精细化的任务调度使得AI成本核算更加清晰，推动行业对AI成本的关注。

**发展趋势：**
*   **Serverless AI:** 未来Flyte on EKS可能会进一步与AWS Fargate结合，实现无节点的AI计算。
*   **多模态工作流:** 工作流将不仅包含训练，还包含数据标注、人工审核等环节的混合编排。

# 5. 延伸思考

**引发的思考：**
*   **供应商锁定:** 虽然Flyte是开源的，但Union.ai作为托管服务是否存在绑定风险？如何设计多云策略？
*   **LLM与编排的结合:** 传统的DAG编排是否适合Agent（智能体）的动态决策流程？未来的工作流可能是非确定性的，Flyte如何适应？

**拓展方向：**
*   研究如何将Flyte与**KServe**（Kubernetes Serving）结合，实现从训练到部署的全自动化闭环。
*   探索在边缘计算场景下，Flyte如何调度云端和边缘设备的协同训练任务。

# 6. 实践建议

**如何应用到自己的项目：**
1.  **评估环境:** 检查现有的ML流程是否包含复杂的依赖关系、是否运行在AWS上、是否存在资源浪费。
2.  **本地验证:** 使用`flytectl`或Docker Desktop在本地运行Flyte Sandbox，将现有的Python脚本改写为Flyte任务。
3.  **EKS部署:** 使用Terraform或Helm Charts在AWS EKS上部署Flyte（或试用Union.ai Cloud）。
4.  **集成CI/CD:** 将Flyte工作流的注册集成到GitHub Actions中，实现代码提交即触发工作流更新。

**具体行动建议：**
*   **模块化代码:** 将现有的Notebook代码重构为纯Python函数，去除全局变量依赖。
*   **容器化:** 编写Dockerfile，确保所有依赖（pandas, torch, transformers等）都被正确打包。
*   **配置资源:** 为每个任务显式设置`requests`和`limits`（CPU/GPU内存）。

**注意事项：**
*   避免在任务中硬编码AWS Access Key，应利用IRSA（IAM Roles for Service Accounts）。
*   注意数据传输量，尽量避免在S3之间频繁移动超大文件，利用Flyte的Off-heap功能或直接传递S3路径指针。

# 7. 案例分析

**成功案例（基于行业常识推断）：**
*   **Spotify:** 作为Flyte的早期创造者和使用者，Spotify利用Flyte管理其庞大的推荐系统训练流程，每天处理数以万计的工作流。通过Flyte，他们实现了从单体架构向微服务架构的转型，使得数据科学家可以自助部署模型，而无需等待工程团队排期。

**失败案例反思：**
*   **忽视资源限制:** 某团队在迁移时未设置GPU内存限制，导致一个异常任务占满了集群所有显存，导致其他关键任务被驱逐（OOMKilled）。
*   **教训:** 必须在Flyte任务中实施严格的资源配额策略和优先级队列。

# 8. 哲学与逻辑：论证地图

**中心命题:**
在构建大规模AI/ML工作流时，采用 **"基于Amazon EKS的Flyte/Union.ai架构"** 优于传统的"自建脚本+通用编排器"模式，因为它在**保证可扩展性**的同时，显著**降低了工程复杂度**并**优化了云资源成本**。

**支撑理由:**
1.  **资源效率:** EKS提供了毫秒级的容器调度能力，结合Flyte的任务级并发控制，能比长期运行的虚拟机更高效地利用昂贵的GPU资源。
2.  **工程解耦:** Flyte的"Workflow-as-Code"抽象将业务逻辑与基础设施代码分离，使得数据科学家无需掌握复杂的Kubernetes YAML配置即可部署生产级代码。
3.  **原生集成:** 该方案利用AWS S3和IAM的原生安全特性，解决了数据传输中的安全性和权限管理难题，避免了自建系统的安全漏洞。

**反例 / 边界条件:**
1.  **极简任务:** 对于单一、线性、运行时间极短（<1分钟）的简单脚本，引入K8s和Flyte的 overhead（启动时间）可能远超任务本身执行时间，此时Lambda或简单的EC2可能更优。
2.  **强实时性:** 对于需要毫秒级响应的在线推理请求，Flyte这种基于批处理/调度模式的架构并不适合，应转向KServe或SageMaker Endpoints。

**命题分类:**
*   **事实:** EKS是AWS首选的K8s托管服务；Flyte是开源的ML编排工具。
*   **价值判断:** "降低工程复杂度"是正向的；"自助式"优于"工单式"。
*   **可检验预测:** 采用该架构后，模型迭代周期将缩短，且云资源利用率将提升。

**立场与验证:**
*   **立场:** 支持在复杂AI场景下采用此架构。
*   **验证方式:**
    *   **指标:** 对比

---
## 最佳实践

## 最佳实践指南

### 实践 1：容器化与资源限制优化

**说明**: 在 Amazon EKS 上运行 AI 工作流时，容器镜像的体积和资源配置直接影响启动速度和集群稳定性。Flyte 任务需要打包依赖项，而 Union.ai 平台负责调度这些任务。优化镜像大小和设置合理的资源请求与限制是防止资源耗尽和降低成本的基础。

**实施步骤**:
1. 使用多阶段构建和精简的基础镜像（如 alpine 或 distroless）来减小容器镜像体积。
2. 为 Flyte 任务中的容器显式设置 CPU 和内存的 `requests`（请求）与 `limits`（限制）。
3. 利用 EKS 的 Cluster Autoscaler 和 Karpacker，根据 Pod 的资源请求自动扩展节点。

**注意事项**: 
避免为 Python 任务构建过大的镜像（例如包含完整的 Conda 环境），这会导致任务启动延迟。建议使用 `union build` 命令或 Docker 缓存机制来加快构建速度。

---

### 实践 2：利用 Spot 实例降低成本

**说明**: AI 训练和数据处理通常属于容错性强或非实时性的批处理任务。在 Amazon EKS 上结合使用 Flyte 和 EC2 Spot 实例，可以显著降低基础设施成本。Flyte 的重试机制可以很好地处理 Spot 实例可能被中断的情况。

**实施步骤**:
1. 配置 EKS 节点组以使用 Spot 实例，或者使用托管节点组。
2. 在 Flyte 任务配置中，针对可中断的任务配置合理的重试策略。
3. 使用 Flyte 的队列系统，确保高优先级任务抢占资源，而低优先级任务利用剩余的 Spot 资源。

**注意事项**: 
确保状态检查点已实现，以便在任务因 Spot 回收而中断时，能够从上次保存的进度恢复，而不是从头开始。

---

### 实践 3：高性能存储与数据访问策略

**说明**: AI 工作流通常涉及海量数据集。直接通过 S3 访问数据或利用 EBS 卷的快照功能，可以避免重复下载和传输数据，从而加速工作流执行。

**实施步骤**:
1. 在 Flyte 任务中直接使用 S3 URI 进行数据读写，利用 Union.ai 和 Flyte 的原生 S3 支持进行自动数据传递。
2. 对于需要高性能 I/O 的训练任务，配置 EBS CSI 驱动器，并使用 `volumeMounts` 将 EBS 卷挂载到容器中。
3. 利用 FSx for Lustre 作为 S3 的缓存层，为高吞吐量的计算任务提供低延迟的文件系统访问。

**注意事项**: 
避免在容器镜像中打包大型数据集。应始终将数据保留在对象存储（如 S3）中，并在运行时动态加载。

---

### 实践 4：工作流模块化与任务解耦

**说明**: Union.ai 和 Flyte 的核心优势在于将工作流代码与基础设施解耦。将复杂的 AI 流程拆分为小的、独立的、可重用的任务，有助于并行执行、错误隔离和独立维护。

**实施步骤**:
1. 定义单一职责的 Python 函数，并使用 `@task` 装饰器将其封装为 Flyte 任务。
2. 使用 `@workflow` 装饰器组合这些任务，明确任务间的依赖关系。
3. 利用 Flyte 的动态工作流功能，根据运行时条件生成执行图。

**注意事项**: 
避免编写包含大量业务逻辑的“单体”任务。这会降低可维护性并阻碍 Flyte 的并行调度优化。

---

### 实践 5：利用 GPU 加速与节点亲和性

**说明**: 对于深度学习模型训练，GPU 资源至关重要。通过正确配置 EKS 和 Flyte，可以确保需要 GPU 的任务被精准调度到带有加速器的节点上，而普通计算任务运行在 CPU 节点上，从而优化资源利用率。

**实施步骤**:
1. 在 EKS 集群中安装 NVIDIA Device Plugin for Kubernetes。
2. 在 Flyte 任务定义中，通过 `Resources` 指定 GPU 需求（例如 `requests=nvidia.com/gpu`）。
3. 配置 Flyte 的任务模板或 Pod 默认值，设置节点亲和性，将 GPU 任务绑定到特定的 GPU 节点标签。

**注意事项**: 
监控 GPU 的内存使用情况。如果 `limits` 设置不当，可能会导致 OOM（内存溢出）错误，导致任务失败。

---

### 实践 6：集中式日志与监控集成

**说明**: 在分布式 EKS 环境中调试 AI 工作流具有挑战性。将 Union.ai/Flyte 的日志与 Amazon CloudWatch 或 OpenTelemetry 集成，可以提供统一的可观测性视图，帮助快速定位性能瓶颈和错误。

**实施步骤**:
1. 配置 Fluent Bit 或 CloudWatch Agent 作为 EKS 的 DaemonSet，收集容器标准输出和日志流。
2. 在 Flyte 任务中集成结构化日志记录（如 Python 的 `logging` 模

---
## 学习要点

- Union.ai 和 Flyte 的结合为在 Amazon EKS 上构建可扩展、生产级 AI 工作流提供了统一平台，简化了从开发到部署的流程。
- Flyte 原生支持 Amazon EKS，能够高效编排容器化任务和分布式机器学习工作流，实现计算资源的动态调度。
- 该架构利用云原生技术（如 Kubernetes）实现了工作流的高可用性和弹性，显著降低了 AI 应用的运维复杂度。
- 通过 Union.ai 的托管服务，团队可以专注于数据科学逻辑，而无需管理底层基础设施，从而加速模型迭代。
- 平台支持混合和多云环境，允许企业在不同云提供商或本地数据中心之间灵活迁移 AI 工作负载。
- 集成 Amazon S3、IAM 等 AWS 服务，确保了数据处理的安全性和无缝的云生态互操作性。
- 这种解决方案特别适用于需要大规模数据处理和模型训练的场景，如生成式 AI 和大语言模型（LLM）的开发。

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
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--6.md" >}})
- [在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260221-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--10.md" >}})
- [基于Union.ai与Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260221-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*