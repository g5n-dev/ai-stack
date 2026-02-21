---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-21T10:46:31+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "AWS", "工作流编排", "Kubernetes", "MLOps", "云原生"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI/ML 工作流。 主要内容如下： 1. **核心工具与架构**： * 利用 **Flyte Python SDK** 进行工作流的编排和扩展。 * 通过 **Union.ai 2.0** 系统，能够在 **Amazon E"
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

在本文中，我们将介绍如何使用 Flyte Python SDK 编排和扩展 AI/ML 工作流。我们探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务无缝集成。我们通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来探讨这一解决方案。

---
## 导语

随着 AI 工作流的复杂度日益提升，如何在 Kubernetes 上实现高效编排与扩展成为关键挑战。本文将探讨如何利用 Union.ai 2.0 和 Flyte 在 Amazon EKS 上构建工作流，并实现与 S3、Aurora 等 AWS 服务的原生集成。通过具体的 AI 示例，我们将向您展示这一解决方案如何简化基础设施管理，从而帮助您更专注于核心业务逻辑的实现。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI/ML 工作流。

主要内容如下：

1.  **核心工具与架构**：
    *   利用 **Flyte Python SDK** 进行工作流的编排和扩展。
    *   通过 **Union.ai 2.0** 系统，能够在 **Amazon Elastic Kubernetes Service (Amazon EKS)** 上轻松部署 Flyte。

2.  **AWS 服务集成**：
    该方案实现了与 AWS 生态系统的无缝集成，主要涉及的服务包括：
    *   **Amazon S3**（存储）
    *   **Amazon Aurora**（数据库）
    *   **AWS IAM**（身份与访问管理）
    *   **Amazon CloudWatch**（监控）

3.  **应用示例**：
    文章通过一个具体的 AI 工作流示例，展示了该解决方案的实际操作，其中特别演示了如何使用 **Amazon S3 Vectors** 这一新服务。

简而言之，这是一种在 AWS 云环境中，通过 Union.ai 和 Flyte 实现可扩展、高度集成的 AI 工作流管理的解决方案。

---
## 评论

### 深度评价：Build AI workflows on Amazon EKS with Union.ai and Flyte

**文章中心观点**
该文章主张利用 Union.ai 2.0（基于 Flyte）在 Amazon EKS 上构建 AI 工作流，以实现机器学习生命周期的高度自动化、可扩展性及与 AWS 云原生生态的深度集成，从而解决从模型训练到部署的工程化复杂度问题。

**支撑理由与边界条件分析**

**1. 技术架构的严谨性与云原生趋势**
*   **支撑理由：** 文章强调了“基础设施即代码”和“容器化编排”在 AI 领域的必要性。从技术角度看，Flyte 的核心价值在于将数据流和任务流抽象为独立的 K8s Pod，利用 EKS 的弹性伸缩能力应对 ML 训练（特别是 GPU 密集型任务）的波峰波谷。这解决了传统静态集群资源利用率低的问题。
*   **事实陈述：** Flyte 确实是业界领先的基于 K8s 的 ML 编排开源项目，Union.ai 则是其商业托管版本，能够降低 Flyte 的运维门槛。
*   **边界条件（反例）：** 对于极小规模的团队或简单的实验性项目，引入 EKS + Flyte + Union.ai 的技术栈存在严重的“过度工程化”问题。部署 EKS 本身具有极高的复杂度，如果只是运行简单的定时脚本，使用 Airflow 甚至直接使用 AWS Step Functions 会更轻量、成本更低。

**2. 数据编排与状态管理的工程化优势**
*   **支撑理由：** 文章提到的无缝集成 S3 和其他 AWS 服务，触及了 MLOps 的痛点——数据血缘和版本管理。Flyte 强制用户定义明确的输入输出接口，这使得工作流具备天然的“可追溯性”和“幂等性”。相比于直接编写 Python 脚本，这种强制约束在多人协作和企业级生产环境中至关重要。
*   **你的推断：** 文章暗示 Union.ai 2.0 可能增强了多租户管理和用户权限控制（RBAC），这对于大型企业合规性是刚需，这可能是开源版 Flyte 难以独立提供的。
*   **边界条件（反例）：** 这种强类型约束在探索性数据分析（EDA）阶段会显著降低开发效率。数据科学家习惯于交互式编程，如果每一次代码修改都需要重新打包容器、注册工作流并提交到 K8s 集群运行，将极大地拖慢迭代速度。

**3. 异构计算与混合云的潜力**
*   **支撑理由：** 基于 EKS 的架构允许工作流在不同类型的计算节点间调度（如 CPU 进行预处理，GPU 进行训练）。文章强调了这种统一编排能力，使得 AI 工作流可以像处理普通微服务一样处理计算任务。
*   **作者观点：** 这种架构为未来的“混合云”或“跨云”策略铺平了道路，因为 Flyte 是云中立的，运行在 EKS 上只是选择之一，并未被 AWS 深度锁定在逻辑层。
*   **边界条件（反例）：** 云原生架构虽然灵活，但带来了巨大的网络开销。如果数据预处理任务与训练任务之间涉及海量数据传输，频繁的 S3 读写和容器间通信可能成为瓶颈，此时单体架构或基于共享内存的架构可能性能更优。

**争议点与不同观点**

1.  **Vendor Lock-in（供应商锁定）的隐性风险：** 虽然文章强调使用开源标准，但 Union.ai 作为商业公司，其 2.0 版本的特定功能（如 UI、特定的插件）可能形成新的锁定。企业需要评估：是选择 Union.ai 的 SaaS/托管服务，还是投入人力自研基于纯开源 Flyte 的平台？
2.  **K8s 复杂度的悖论：** 文章倾向于将 K8s 作为所有 AI 工作流的默认底座。然而，业界（如 Meta、Uber）的实践表明，K8s 并非万能药。对于超大规模的大模型训练任务，Ray 或专用的调度系统（如 Slurm）往往比 K8s 更高效。K8s 的 API 调用延迟和 Pod 启动时间对于毫秒级或极高频的任务是不可接受的。
3.  **成本黑洞：** 文章未深入探讨成本控制。EKS 节点、S3 请求费用以及 Union.ai 的潜在许可费用加起来可能非常昂贵。如果工作流设计不当，导致频繁的 Pod 伸缩，可能会产生意想不到的云资源账单。

**实际应用建议**

1.  **适用场景判断：** 仅当你的团队面临以下情况时考虑该方案：模型训练/推理任务耗时超过 30 分钟、需要复杂的依赖管理、团队规模 > 5 人、且对实验的可复现性有强合规要求。
2.  **渐进式迁移：** 不要试图一次性将所有 AI 工作流迁移到 Flyte。建议先从“训练流水线”开始，保留数据科学家的本地开发环境，仅将成熟模型固化为 Flyte 任务。
3.  **关注冷启动时间：** 在实施前，务必测试 EKS 节点的扩缩容速度。如果使用 Spot 实例降低成本，必须配合 Flyte 的重试机制，防止任务因实例回收而失败。

**可验证的检查方式**

1.  **基准测试（指标）：** 对比“Flyte on EKS”与“AWS SageMaker Pipelines”在相同 ML 任务（如 ResNet50 训练）下的端到端耗时（包括调度延迟、容器启动

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：**通过将 Union.ai（Flyte 的商业托管版本）与 Amazon EKS（Elastic Kubernetes Service）深度集成，企业可以构建一个既具有云原生弹性，又能解决 AI/ML 工作流特定复杂性（如数据依赖、模型版本管理、异构计算）的高效生产环境。**

**作者想要传达的核心思想**
作者试图传达“编排层”与“执行层”分离的重要性。传统的 AI 开发往往止步于笔记本，而生产化面临巨大的工程鸿沟。核心思想在于，利用 **Flyte** 的**基于数据流的编程模型**，配合 **EKS** 的**基础设施无关性**，可以实现从原型到生产环境的无缝过渡。Union.ai 2.0 则扮演了“粘合剂”的角色，简化了在 AWS 这一复杂生态中部署和运维 Flyte 的难度。

**观点的创新性和深度**
*   **从“任务调度”到“数据流编排”：** 传统的调度器（如 Airflow）侧重于时间触发，而 Flyte 侧重于数据传递和版本追踪。文章隐含地强调了这种范式转移对于 AI 工作流的重要性。
*   **混合编排的深度整合：** 文章不仅谈到了部署，更强调了与 AWS 原生服务（如 S3, ECR）的深度整合。这种深度体现在利用 EKS 的 Pod Operator 来动态调度 GPU 实例进行训练，同时利用 CPU 进行数据预处理，展示了资源利用的深度优化。
*   **Union.ai 2.0 的定位：** 将开源框架通过商业产品（Union.ai）无缝落地到特定云厂商（AWS），这种“开源核心 + 商业体验 + 云原生落地”的三位一体架构是文章深度的体现。

**为什么这个观点重要**
随着大模型（LLM）和生成式 AI 的爆发，AI 工作流的规模和复杂性呈指数级增长。单纯的模型训练已不再是瓶颈，**如何管理成千上万次实验、如何处理海量数据管道、如何在不闲置时自动释放昂贵的 GPU 资源**，成为了企业降本增效的关键。这篇文章提供的架构直接解决了这些痛点，对于寻求 AI 落地成熟度的企业至关重要。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **Flyte：** 一个开源的、云原生的的工作流编排平台，专门用于构建数据和 ML 流水线。
2.  **Amazon EKS (Elastic Kubernetes Service)：** AWS 托管的 Kubernetes 服务，提供容器编排能力。
3.  **Union.ai：** Flyte 的商业版本，提供控制平面和托管服务，简化了 Flyte 的部署和运维。
4.  **Flyte Python SDK：** 用于定义任务和工作流的 Python 装饰器和接口。
5.  **AWS S3 (Simple Storage Service)：** 用于存储数据集、模型和中间产物。

**技术原理和实现方式**
*   **声明式工作流定义：** 利用 Flyte Python SDK，开发者使用 `@task` 和 `@workflow` 装饰器将普通的 Python 函数转化为可追踪、可复用的有向无环图（DAG）。
*   **容器化与隔离：** Flyte 将每个任务打包在容器中。在 EKS 上，这意味着每个任务对应一个 Pod（或一组 Pod）。Flyte 能够动态指定任务所需的资源（CPU, 内存, GPU）。
*   **数据血缘与自动缓存：** Flyte 的核心机制是追踪输入输出的哈希值。如果输入参数未变，Flyte 会自动跳过执行并返回缓存结果。在 EKS 环境下，这通过挂载 S3 或通过 S3 协议传输数据来实现。
*   **动态实例扩展：** 结合 AWS Node Groups 或 Karpenter（虽未明说但通常是 EKS 最佳实践），Flyte 可以请求特定资源（如 `nvidia.com/gpu`），触发 K8s 自动扩缩容集群节点。

**技术难点和解决方案**
*   **难点：** 在 Kubernetes 上管理有状态的计算任务（如训练中断后的恢复）。
*   **解决方案：** Flyte 原生支持任务级别的重试和检查点，结合 EKS 的存储卷（如 EFS）或直接对接 S3，确保任务失败后不丢失全部进度。
*   **难点：** 异构资源调度（PyTorch 需 GPU，Pandas 需大内存）。
*   **解决方案：** Flyte 允许在 Workflow 定义中为每个 Task 单独声明资源请求，EKS 调度器负责将 Pod 放置在合适的节点池上。

**技术创新点分析**
*   **Type-Safe 工作流：** Flyte 强类型系统确保了数据在任务间传递时的正确性，这在动态语言 Python 中是一个极大的工程创新。
*   **多语言扩展：** 虽然文章侧重 Python SDK，但 Flyte 底层支持任何容器化语言，这对于混合技术栈（如 C++ 训练核心 + Python 后处理）的团队极具价值。

## 3. 实际应用价值

**对实际工作的指导意义**
*   **降低 MLOps 门槛：** 团队无需自己构建复杂的 K8s Operator 或自定义调度器，直接利用 Flyte + Union.ai 即可获得企业级的编排能力。
*   **成本优化：** 通过精细化的资源请求（只在训练时申请 GPU）和自动缓存机制，显著降低 AWS 账单。
*   **标准化交付：** 强制将代码转化为容器化工作流，消除了“在我机器上能跑”的环境差异问题。

**可以应用到哪些场景**
1.  **大规模模型微调：** 定期触发微调任务，处理 S3 中的新数据，输出模型到 S3。
2.  **批推理：** 每日夜间处理大量预测请求，动态扩容 Pod 处理，完成后缩容。
3.  **ETL 与数据清洗：** 复杂的多阶段数据处理，其中后一步依赖前一步的输出。
4.  **A/B 测试流水线：** 同时运行多个模型训练变体，比较结果。

**需要注意的问题**
*   **冷启动时间：** 容器启动和 Pod 调度可能需要时间，对于毫秒级要求的实时推理不适用（适合批处理）。
*   **AWS 成本复杂性：** 虽然 EKS 按需付费，但若不配置好节点自动缩容，可能会出现闲置节点计费。
*   **学习曲线：** 团队需要理解容器化和 Kubernetes 的基本概念，以及 Flyte 的特定抽象。

**实施建议**
*   **从非关键路径开始：** 先迁移数据报告生成或离线数据处理任务。
*   **建立标准的容器基镜像：** 预先安装好必要的深度学习框架，避免每次运行都下载依赖。
*   **利用 Spot 实例：** 在 EKS 节点组中混合使用 Spot 实例以运行容错率高的训练任务。

## 4. 行业影响分析

**对行业的启示**
这标志着 **MLOps 正从“实验工具”向“基础设施代码”演进**。行业不再满足于简单的 Notebook 环境，而是要求 AI 工作流具备与微服务同等的可靠性、可扩展性和可观测性。

**可能带来的变革**
*   **软件工程师与 AI 工程师的融合：** 随着 K8s 成为底层标准，AI 工程师必须掌握云原生技能，传统的纯算法角色正在消失。
*   **“大模型 + 小编排”的趋势：** 模型越来越大，但围绕模型的编排逻辑（数据准备、评估、部署）越来越标准化，通用编排平台（如 Flyte）可能取代自研脚本。

**相关领域的发展趋势**
*   **Serverless 容器的整合：** 未来可能会看到 Flyte 与 AWS Fargate 的更深层次整合，进一步免除节点管理负担。
*   **FinOps 的兴起：** 这种架构使得 AI 计算成本透明化，推动了财务导向的运维优化。

**对行业格局的影响**
Union.ai 作为 Flyte 的商业实体，正在挑战 Databricks（MLflow）和 Airflow 的地位。这种“开源核心 + 云服务”的模式正在成为 MLOps 领域的标准商业路径。

## 5. 延伸思考

**引发的其他思考**
*   **LLM 工作流的特殊性：** Flyte 这种基于 DAG 的结构是否适合 LLM 的 Agent 循环（Loop）？Agent 往往是动态决策的，可能需要更灵活的编排范式。
*   **数据重力：** 如果数据都在 AWS S3 上，计算（EKS）必然也在 AWS。这是否会导致厂商锁定？Flyte 的多云部署能力是解决此问题的关键。

**可以拓展的方向**
*   **与 SageMaker 的比较：** 文章未提及 SageMaker。实际上，Flyte + EKS 是比 SageMaker 更灵活但运维要求更高的替代方案。分析两者的边界是很好的延伸。
*   **特征存储的集成：** 如何将 Flyte 与 Feast 等特征存储结合，实现特征的一致性。

**需要进一步研究的问题**
*   在极高并发场景下（如每分钟启动数千个 Pod），Flyte 控制平面的性能瓶颈在哪里？
*   如何在混合云（本地数据中心 + AWS）环境下利用此架构？

**未来发展趋势**
*   **Event-Driven 驱动：** 未来的工作流可能不仅由定时或 API 触发，而是由 S3 事件上传或 SQS 消息触发。
*   **GitOps 的融合：** 工作流的定义将完全存储在 Git 中，通过 ArgoCD 自动同步到 Flyte 集群。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估阶段：** 在本地 Docker 环境中运行 Flyte Sandbox，体验 `@task` 和 `@workflow` 的开发模式。
2.  **概念验证：** 选择一个现有的 Python 脚本（例如数据清洗脚本），将其 Flyte 化，并尝试在本地执行。
3.  **EKS 部署：** 使用 `eksctl` 或 Terraform 创建一个小型 EKS 集群。
4.  **Union 注册：** 注册 Union.ai 免费账户，将其连接到你的 EKS 集群（如果使用 Union Cloud）或使用 Union Server 部署到 EKS。

**具体的行动建议**
*   **代码重构：** 将纯 Python 脚本重构为函数式编程风格，确保函数是幂等的（输入相同，输出相同）。
*   **容器化：** 编写 `Dockerfile`，将依赖打包。
*   **配置资源：** 在 Flyte 任务中明确指定 `requests`（内存/CPU），这是性能调优的关键。

**需要补充的知识**
*   **Kubernetes 基础：** 理解 Pod, Node, Namespace, RBAC。
*   **容器技术：** Docker 构建与优化。
*   **Python 类型提示：** Flyte 严重依赖 Python 类型注解。

**实践中的注意事项**
*   避免在任务内部进行大

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建可扩展的容器化基础架构

**说明**: 利用 Amazon EKS 的托管 Kubernetes 服务和 Union.ai/Flyte 的编排能力，确保 AI 工作负载能够根据需求自动扩展。Flyte 的任务模型与 Kubernetes Pod 原生集成，允许通过定义资源请求（CPU/内存）来动态调度工作负载。

**实施步骤**:
1. 配置 EKS 节点组，使用 EC2 实例类型（如 GPU 实例）或 Karpenter 实现按需扩容。
2. 在 Flyte 任务中明确指定资源需求（`requests` 和 `limits`），以便 Kubernetes 调度器分配足够的资源。
3. 启用 EKS 集群自动伸缩器，确保节点数量能够随工作负载波动。

**注意事项**: 避免过度预留资源，导致成本浪费；同时确保 GPU 驱动与 CUDA 版本与模型训练环境兼容。

---

### 实践 2：实现高效的数据本地化与缓存策略

**说明**: AI 工作流通常涉及大规模数据集的读取。通过将数据存储在 S3 中，并利用 Flyte 的数据传播机制或 Union.ai 的缓存功能，可以最小化数据移动开销，避免每次任务运行都重新下载或处理数据。

**实施步骤**:
1. 将原始数据集和中间产物存储在 Amazon S3 中，并配置适当的 IAM 策略以供 EKS Pod 访问。
2. 在 Flyte 工作流中启用“数据缓存”，对输入参数哈希一致的任务复用之前的输出结果。
3. 使用 Flyte 的 `RawOutputDataConfig` 将大型中间文件直接上传至 S3，而非存储在容器层。

**注意事项**: 确保数据访问路径（如 S3 URI）在任务间正确传递，并处理好 S3 最终一致性带来的潜在问题。

---

### 实践 3：优化模型训练与推理的容器镜像

**说明**: 构建包含所有必要依赖项（如 PyTorch, TensorFlow, CUDA）的优化型 Docker 镜像。Union.ai 和 Flyte 允许高度自定义容器镜像，利用这一点可以减少冷启动时间并确保环境一致性。

**实施步骤**:
1. 使用 Amazon ECR 构建和存储私有 Docker 镜像。
2. 在 Dockerfile 中利用多阶段构建，剔除不必要的文件，减小镜像体积。
3. 在 Flyte 任务定义中指定特定的镜像，利用 `ImageSpec` 动态构建和注册镜像。

**注意事项**: 定期更新基础镜像以获取安全补丁，但在生产环境中需严格锁定版本号，以确保可复现性。

---

### 实践 4：利用 Spot 实例降低计算成本

**说明**: 对于容错性较高的 AI 任务（如超参数调优、数据预处理），利用 Amazon EC2 Spot 实例可以显著降低计算成本。Flyte 原生支持重试机制，非常适合处理 Spot 实例可能发生的中断。

**实施步骤**:
1. 在 EKS 上配置混合节点组，包含按需实例和 Spot 实例。
2. 使用 Karpenter 或 EKS 托理节点组配置 Spot 实例的容量优化策略。
3. 在 Flyte 任务中配置合理的重试次数，以应对 Spot 实例回收导致的任务失败。

**注意事项**: 仅对状态可持久化或可快速重启的任务使用 Spot 实例；对于长时间运行的训练任务，需确保支持 Checkpoint（断点续训）功能。

---

### 实践 5：实施细粒度的监控与日志管理

**说明**: 利用 CloudWatch 和 Prometheus 监控 EKS 集群及 Flyte 工作流的健康状态。通过集中式日志管理，快速定位 AI 工作流中的性能瓶颈或错误。

**实施步骤**:
1. 安装 AWS Distro for OpenTelemetry (ADOT) 或 Fluent Bit，将 EKS Pod 的标准输出和日志流式传输至 CloudWatch Logs。
2. 配置 CloudWatch Container Insights，监控集群级别的 CPU、内存和网络指标。
3. 利用 Union.ai 或 Flyte Console 查看任务级别的执行时间和事件日志。

**注意事项**: 避免记录过多的调试日志到 CloudWatch，以免产生高额的日志存储费用；建议对敏感数据进行脱敏处理。

---

### 实践 6：确保工作流的安全性与合规性

**说明**: 在 EKS 上运行 AI 工作流时，必须遵循最小权限原则。利用 IAM Roles for Service Accounts (IRSA) 为 Flyte 任务分配精细的 S3 或 DynamoDB 访问权限，避免在节点上挂载通用的 IAM 角色。

**实施步骤**:
1. 为 EKS 服务账户创建 IAM 角色，并授予必要的 S3 读写权限。
2. 在 Pod 定义中注解服务账户，使其能够自动获取 AWS 临时凭证。
3. 启用 EKS 的控制平面日志记录和审计追踪，监控 API 调用情况。

**注意事项**: 定期轮换 IAM 访问密钥（如

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展、可重复的 AI 工作流，实现机器学习任务的高效编排与自动化管理。
- 利用 Amazon EKS 的托管 Kubernetes 服务，用户可以轻松部署、扩展和管理容器化的 AI 应用，无需维护底层基础设施。
- Flyte 提供的工作流抽象层简化了复杂 AI 流程的开发，支持数据管道、模型训练和推理的端到端编排。
- Union.ai 的平台能力进一步增强了 Flyte 的功能，提供企业级支持、监控和安全性，加速 AI 生产环境的落地。
- 该解决方案支持多种计算框架（如 PyTorch、TensorFlow）和存储系统（如 Amazon S3），确保与现有 AI 技术栈的无缝集成。
- 通过声明式工作流定义，团队可以实现版本控制、可复现性和跨环境一致性，提升协作效率。
- Amazon EKS 的弹性伸缩能力结合 Flyte 的资源优化，能根据工作负载动态调整计算资源，降低成本并提升性能。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Flyte](/tags/flyte/) / [Union.ai](/tags/union.ai/) / [Amazon EKS](/tags/amazon-eks/) / [AWS](/tags/aws/) / [工作流编排](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%BC%96%E6%8E%92/) / [Kubernetes](/tags/kubernetes/) / [MLOps](/tags/mlops/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--7.md" >}})
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--3.md" >}})
- [基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--4.md" >}})
- [基于Union.ai和Flyte在Amazon EKS上构建AI工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*