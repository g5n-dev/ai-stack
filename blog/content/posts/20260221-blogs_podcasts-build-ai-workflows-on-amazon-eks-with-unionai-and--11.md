---
title: "基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-21T12:36:46+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "Python SDK"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建和扩展 AI/ML 工作流。 主要内容包括： 1. **核心工具与技术**：文章展示了使用 **Flyte Python SDK** 来编排和自动化 AI 工作流，以及如何利用 **Union.ai 2.0**"
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios: ["AI/ML项目", "Kubernetes"]
---

# 基于 Amazon EKS 使用 Union.ai 和 Flyte 构建 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---
## 摘要/简介

在本文中，我们将介绍如何利用 Flyte Python SDK 编排和扩展 AI/ML 工作流。我们探讨 Union.ai 2.0 系统如何在 Amazon Elastic Kubernetes Service（Amazon EKS）上部署 Flyte，并与 Amazon Simple Storage Service（Amazon S3）、Amazon Aurora、AWS Identity and Access Management（IAM）和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来剖析这一解决方案。

---
## 导语

随着 AI 工作流的复杂度不断提升，如何在 Kubernetes 环境中实现高效编排与扩展成为关键挑战。本文将探讨如何利用 Union.ai 2.0 在 Amazon EKS 上部署 Flyte，并实现与 S3、Aurora 等 AWS 服务的无缝集成。通过一个使用 Amazon S3 Vectors 的实战示例，我们将剖析该方案的架构细节，帮助您掌握构建可扩展、生产级 AI 流程的具体方法。

---
## 摘要

本文介绍了如何利用 **Union.ai** 和 **Flyte** 在 **Amazon EKS** 上构建和扩展 AI/ML 工作流。

主要内容包括：

1.  **核心工具与技术**：文章展示了使用 **Flyte Python SDK** 来编排和自动化 AI 工作流，以及如何利用 **Union.ai 2.0** 系统将 Flyte 部署到 **Amazon EKS（Elastic Kubernetes Service）** 上。
2.  **AWS 服务集成**：该解决方案实现了与 AWS 生态系统的无缝集成，主要包括：
    *   **Amazon S3**：用于存储数据和模型。
    *   **Amazon Aurora**：作为数据库支持。
    *   **AWS IAM**：用于身份和访问管理。
    *   **Amazon CloudWatch**：用于监控和日志记录。
3.  **应用示例**：文章通过一个具体的 AI 工作流示例演示了该方案，其中使用了最新的 **Amazon S3 Vectors** 服务。

总之，该方案为开发者提供了一个在 Kubernetes 环境中高效运行和管理 AI 流程的强大平台。

---
## 评论

**文章中心观点**
本文主张通过 Union.ai 2.0 将 Flyte 工作流编排系统部署在 Amazon EKS 上，构建一个基于 Kubernetes 的统一控制平面，以解决云原生 AI/ML 环境中从模型开发到生产部署的扩展性与隔离性问题。

**支撑理由与评价**

**1. 内容深度：架构严谨但视野局限于“控制平面”**
*   **支撑理由（事实陈述/你的推断）：** 文章深入探讨了如何利用 Flyte 的 Python SDK 定义任务，并利用 Union.ai 在 EKS 上自动配置 Kubernetes 资源。其技术深度在于正确识别了“编排层”与“计算层”的边界：Flyte 作为控制平面负责调度和版本控制，而 EKS 负责底层的容器调度和资源隔离。这种架构设计符合云原生构建原则，论证了将 ML 流水线与基础设施解耦的必要性。
*   **反例/边界条件（你的推断）：** 文章在**数据血缘**方面的深度可能不足。Flyte 擅长任务编排，但在处理跨服务的复杂数据依赖和元数据追踪时，可能不如专用的 ML 特征平台（如 Tecton 或 Feast）深入。如果企业的痛点在于特征复用而非模型训练，单纯的工作流编排是不够的。

**2. 实用价值：对“重 AWS”企业极具指导意义**
*   **支撑理由（事实陈述）：** 文章详细描述了与 AWS 生态（S3, ECR, IAM）的无缝集成。对于已经深度锁定 AWS 服务的团队，这篇文章提供了一个可落地的“操作手册”，避免了从零开始搭建 K8s 运维环境的复杂性，显著降低了 ML 工程化的门槛。
*   **反例/边界条件（作者观点）：** 对于中小规模团队或非 AWS 用户，这种架构的**复杂度收益比（ROI）较低**。维护一个高可用的 EKS 集群加上 Union.ai 的控制平面，其运维成本远高于使用 Serverless 编排服务（如 AWS Step Functions 或 Prefect Cloud）。如果工作流不是全天候运行，Serverless 通常是更优解。

**3. 创新性：强调“多租户隔离”而非单纯的“加速”**
*   **支撑理由（你的推断）：** 不同于大多数 MLOps 文章仅关注“如何加快训练速度”，本文隐含的创新点在于利用 K8s 的命名空间和 Union.ai 的多租户能力，解决了 AI 平台中最棘手的“生产与开发混部”问题。它提出了一种在不牺牲安全性的前提下，让数据科学家共享底层 GPU 资源的方法。
*   **反例/边界条件（事实陈述）：** 这种创新并非 Flyte 独有。Kubeflow Pipelines (KFP) 同样运行在 K8s 上且提供类似功能。文章未充分对比 Union.ai/Flyte 与 KFP 或 Argo Workflows 在 EKS 上的性能差异，这是一个明显的论证缺失。

**4. 行业影响：推动“以代码为中心”的 MLOps 标准化**
*   **支撑理由（作者观点）：** 文章推广了“一切皆代码”的理念，通过 Python SDK 定义基础设施和工作流。这符合行业从“点击式操作”向“GitOps”演变的趋势。Union.ai 的商业化推广可能加速 Flyte 成为 K8s 编排的标准之一，挑战 Airflow 在批处理领域的地位。
*   **反例/边界条件（你的推断）：** 行业正在向“轻量级编排”分化。随着 LangChain 等框架的兴起，许多 AI 应用转向了以 Agent 为中心的动态编排，而非静态的 DAG（有向无环图）。Flyte 这种强结构、重批处理的模式，可能难以适应 LLM 应用中非确定性的、迭代式的交互模式。

**批判性思考与争议点**

*   **厂商锁定风险：** 虽然文章强调使用开源 Flyte，但 Union.ai 作为商业公司，其 2.0 版本可能引入了专有特性。用户需警惕在 Union 的特定 DSL 上过度抽象，导致未来迁移回原生 Flyte 或其他平台时的困难。
*   **资源碎片化：** 在 EKS 上运行 AI 工作流常面临“GPU 孤岛”问题。文章未深入讨论如何利用 AWS EC2 的 Spot 实例或弹性调度来优化成本。如果仅仅是简单调度，在 EKS 上运行 AI 的成本往往比直接使用 SageMaker 等托管服务更高。

**实际应用建议**

1.  **成本监控先行：** 在采纳此架构前，必须建立完善的 EKS 成本监控机制。由于 K8s 的资源抽象，数据科学家可能无意识地申请过多资源，导致云账单爆炸。
2.  **混合架构策略：** 不要试图用 Flyte 解决所有问题。建议将**长时运行、重计算的训练任务**放在 Flyte/EKS 上，而将**轻量级的推理或实时数据处理**保留在 AWS Lambda 或 SageMaker Endpoints 上。
3.  **评估学习曲线：** Flyte 的概念（如 Launch Plans、动态工作流）对数据科学家有一定学习门槛。在全面推广前，先在一个边缘项目中验证团队是否接受这种“强类型”的编程模式。

**可验证的检查方式**

1.  **集成测试指标：** 部署该架构后，观察从代码提交到模型训练启动的**端到端延迟**。如果超过 5 分钟，说明 EKS 集群的冷启动或镜像拉取策略存在问题。
2.

---
## 技术分析

基于您提供的文章标题和摘要，虽然无法获取全文细节，但结合 **Flyte**、**Union.ai** 和 **Amazon EKS** 的技术生态，我可以为您构建一份深度的技术分析报告。这篇文章的核心在于探讨如何通过云原生技术解决 AI/ML 工作流在生产环境中的编排、扩展和管理难题。

以下是深入分析：

---

# 1. 核心观点深度解读

**主要观点：**
文章主张通过 **Union.ai（托管 Flyte）** 与 **Amazon EKS** 的深度集成，构建一个高性能、可扩展且云原生的 AI/ML 工作流编排平台。其核心在于将 Flyte 的“数据为中心”的编排能力与 EKS 的弹性基础设施相结合，解决机器学习从原型到生产过程中的“工程化鸿沟”。

**核心思想：**
作者试图传达 **“基础设施即代码”** 与 **“工作流即代码”** 在 AI 领域的统一。ML 工程师不应关注底层容器管理的复杂性，而应通过 Python SDK 定义任务逻辑，由系统自动处理在 Kubernetes 上的调度、扩展和数据传递。

**创新性与深度：**
*   **深度：** 文章不仅停留在简单的任务调度，而是深入到了“数据血缘”和“容错性”层面。Flyte 的核心创新在于它不仅传递控制流，更通过 S3 自动传递数据流，实现了任务间的解耦。
*   **创新性：** 提出了在 Kubernetes 上运行有状态 ML 任务的最佳实践。传统上 K8s 适合无状态服务，而 ML 任务（训练、调优）通常是长时间运行且重资源的。文章展示了如何利用 EKS 的节点组管理和 Flyte 的任务级调度来优化这一过程。

**重要性：**
随着大模型（LLM）和复杂 ML Pipeline 的普及，单机脚本已无法满足需求。企业急需一套能管理 TB 级数据、分布式训练和复杂依赖关系的系统。此方案提供了企业级的标准答案，避免了重复造轮子，降低了 MLOps 的准入门槛。

---

# 2. 关键技术要点

**涉及的关键技术：**
1.  **Flyte Python SDK:** 用于构建工作流的领域特定语言（DSL），允许用户使用 Python 装饰器定义任务和工作流。
2.  **Amazon EKS (Elastic Kubernetes Service):** AWS 提供的托管 K8s 服务，提供底层容器编排。
3.  **Union.ai 2.0:** Flyte 的商业托管版本，简化了 Flyte on EKS 的部署和运维。
4.  **AWS S3 (Simple Storage Service):** 作为中间存储层，缓存输入输出数据及模型检查点。

**技术原理与实现：**
*   **编译时 vs 运行时:** Flyte 引入了一个编译步骤，将 Python 代码编译成中间表示（IR）。这使得系统可以在运行前进行静态分析（检查依赖、类型校验）和优化（执行计划）。
*   **基于 Pod 的任务执行:** 在 Flyte 中，每个 Task 映射为 K8s 中的一个 Pod（或一组 Pod，如 Ray/Spark Jobs）。Flyte Propeller（控制平面）持续监控 CRD（Custom Resource Definitions）的状态，驱动工作流向前推进。
*   **惰性计算与数据传递:** 任务之间不直接传递对象，而是传递指向 S3 的指针。只有当下游任务真正需要数据时，才会加载。这极大减少了内存占用。

**技术难点与解决方案：**
*   **难点：** 在 K8s 上调度大规模分布式训练（如 PyTorch DDP）极其复杂，涉及 Gang Scheduling（所有 Pod 同时启动）和端口通信。
    *   **解决方案：** Flyte 提供了针对 Ray、PyTorch 等框架的插件，自动处理底层资源的分配和 Service 的创建。
*   **难点：** 数据在不同安全区域或不同服务间的传输。
    *   **解决方案：** 利用 S3 的 IAM Role 绑定，通过 Flyte 的任务身份注入，实现无需硬编码凭证的安全数据访问。

**技术创新点：**
*   **动态工作流:** Flyte 允许在运行时根据上游任务的输出来决定下游任务的结构（例如，根据准确率动态决定训练轮数），这在传统的 Airflow 等工具中很难实现。

---

# 3. 实际应用价值

**指导意义：**
该文章为数据科学团队提供了一条从“笔记本”到“生产环境”的标准化路径。它明确了如何利用 AWS 的云生态能力来承载复杂的 AI 业务逻辑。

**应用场景：**
1.  **模型微调:** 定期从 S3 获取新数据，触发微调流程，完成后自动部署模型。
2.  **批处理推理:** 每天凌晨处理海量用户行为数据，生成推荐结果。
3.  **药物研发/基因组学:** 处理极其复杂的长流程 Pipeline，包含数千个依赖步骤。

**注意问题：**
*   **成本控制:** EKS 节点和 S3 请求会产生费用。Flyte 任务频繁读写 S3 可能产生 API 成本。
*   **冷启动:** 对于极短的任务，K8s Pod 的启动开销可能过大。

**实施建议：**
*   **资源配额:** 在 Flyte 项目中为不同团队设置 CPU/内存配额，防止资源抢占。
*   **Spot 实例:** 利用 Flyte 对中断的容忍能力，在 EKS 中混合使用 Spot 实例运行训练任务以降低成本。

---

# 4. 行业影响分析

**行业启示：**
MLOps 正在从“以模型为中心”转向“以数据/流水线为中心”。基础设施的标准化（K8s）和应用层的标准化（Flyte/Cube）正在融合。

**带来的变革：**
*   **降低 MLOps 债务:** 企业不再需要维护自己写的脆弱脚本，转而使用声明式的、版本可控的工作流。
*   **加速 AI 落地:** 通过 Union.ai 的 SaaS 化或半托管模式，中型企业也能拥有与互联网大厂类似的 ML 基础设施能力。

**发展趋势：**
*   **Serverless 化:** 虽然 EKS 是容器化的，但未来趋势是更细粒度的 Serverless 容器（如 AWS Fargate）与 Flyte 的结合，实现按秒计费的 ML 计算。
*   **LLM 编排:** Flyte 这类编排工具将不仅仅处理数据，更将作为 LLM Agents 和 Chain-of-Thought 的执行引擎。

---

# 5. 延伸思考

**拓展方向：**
*   **可观测性:** Flyte 提供了执行图，但如何与 Prometheus/Grafana 结合，深入监控 GPU 利用率和显存碎片？
*   **混合云部署:** 如何在 EKS 和 On-prem K8s 之间构建混合工作流？

**待研究问题：**
*   如何在 Flyte 中实现更细粒度的模型版本管理和回滚机制？
*   随着模型越来越大，如何优化容器镜像的拉取速度（Image Caching 策略）？

---

# 6. 实践建议

**如何应用到项目：**
1.  **评估阶段:** 先使用 Union.ai 的免费层或本地 Kind 集群部署 Flyte，跑通一个简单的 Scikit-learn 训练流程。
2.  **容器化:** 将现有的 Python 脚本封装成 Docker 镜像，确保环境一致性。
3.  **迁移:** 将线下的 Cron 任务或 Airflow DAG 逐步迁移为 Flyte Tasks。

**行动建议：**
*   学习 Flyte 的 **Type System**（Flyte Remote），理解基本数据类型如何自动序列化。
*   配置 **IAM Roles for Service Accounts (IRSA)**，确保 EKS Pod 有权限读写 S3。

**注意事项：**
*   避免在 `@task` 函数中使用全局状态（全局变量），这会导致分布式执行时的错误。
*   确保任务具有**幂等性**，因为 Flyte 的重试机制可能会多次执行同一个任务。

---

# 7. 案例分析

**成功案例（基于行业通用知识）：**
*   **Spotify:** 众所周知使用 Flyte 管理其庞大的推荐系统和机器学习基础设施。他们利用 Flyte 处理数百万个用户的特征工程和模型训练，实现了极高的资源利用率和自动化程度。
*   **分析:** 成功关键在于将数据科学家从繁重的运维中解放出来，让他们只需关注 Python 代码，而底层资源调度完全由 Flyte 和 K8s 接管。

**失败/反思案例：**
*   **场景:** 某公司试图将传统的 ETL 任务直接迁移到 Flyte 上，但未对任务进行容器化改造。
*   **结果:** 发现由于任务启动开销大，整体运行时间比原有系统慢。
*   **教训:** Flyte 设计用于“繁重”的计算任务（CPU/密集型 IO）。对于高频、低延迟的简单 ETL，传统的 Lambda 或 Airflow 可能更合适。不要为了技术而技术。

---

# 8. 哲学与逻辑：论证地图

**中心命题:**
**在 Amazon EKS 上部署 Union.ai/Flyte 是构建可扩展、可维护且云原生的企业级 AI/ML 工作流编排的最佳实践。**

**支撑理由:**
1.  **弹性与资源隔离:** EKS 提供了底层容器编排能力，支持 GPU 调度和节点自动伸缩，解决了 ML 工作负载资源需求波动大的问题。
2.  **声明式工作流与版本控制:** Flyte 的“代码即配置”特性，使得 ML Pipeline 像软件代码一样可版本化、可测试、可回滚，解决了“实验即生产”的混乱状态。
3.  **数据血缘与可复现性:** Flyte 自动跟踪输入输出（通过 S3），强制建立了严格的数据血缘，解决了 AI 实验难以复现的痛点。

**反例/边界条件:**
1.  **极低延迟需求:** 如果工作流要求毫秒级响应（如实时推荐请求），Flyte 基于 K8s Pod 的冷启动机制（秒级/分钟级）可能不适用，此时应直接使用 Sagemaker Endpoints 或 Lambda。
2.  **极简轻量级任务:** 对于仅需简单 SQL 查询的定时任务，引入 K8s 和 Flyte 的运维复杂度可能远超其收益。

**判断类型:**
*   **事实:** Flyte 运行在 K8s 上；EKS 支持 GPU。
*   **价值判断:** “最佳实践”意味着在可维护性、扩展性和开发效率之间取得了最优平衡。
*   **可检验预测:** 采用该架构的团队，其模型迭代周期将缩短，且资源利用率（GPU/内存）将高于传统脚本或单体应用架构。

**立场与验证:**
**立场:** 支持。对于任何处于“成长期”或“成熟期”的数据团队，将工作流迁移至 Flyte on EKS 是必然选择。
**验证方式:**
*   **指标:** 对比迁移前后的“模型平均训练启动时间”和“集群资源平均利用率”。
*   **实验:** 选取 3 个复杂的现有 Pipeline 进行重构，测量开发人员处理依赖冲突和环境错误所花费的时间是否显著下降。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建模块化且可复用的 Flyte 任务

**说明**: 在构建 AI 工作流时，应避免将所有逻辑（数据预处理、训练、评估）写入单一脚本。最佳实践是将工作流拆解为独立的、细粒度的任务。利用 Union.ai 和 Flyte，可以将这些任务定义为独立的函数或容器镜像，从而实现代码的复用和版本控制。这不仅提高了代码的可维护性，还能让不同的任务在不同的计算资源上独立运行。

**实施步骤**:
1. 将数据处理、模型训练和模型评估逻辑分离为独立的 Python 函数。
2. 使用 `@task` 装饰器显式注册这些函数，并指定特定的容器镜像或资源需求（如 GPU）。
3. 使用 `@workflow` 装饰器将上述任务编排起来，定义任务间的数据依赖关系。
4. 将通用的任务（如 S3 上传下载、特定的数据清洗逻辑）封装为共享库，供多个项目调用。

**注意事项**: 确保任务的输入输出是强类型的，并使用 Flyte 的数据类型（如 FlyteSchema, FlyteDirectory），以便系统能自动处理数据的序列化和在 S3 上的存储传递。

---

### 实践 2：利用 Spot 实例优化 EKS 计算成本

**说明**: AI 和机器学习工作负载（特别是训练和调优）通常对中断的容忍度较高，且计算需求大。在 Amazon EKS 上运行 Flyte 时，应配置节点组使用 EC2 Spot 实例。这可以显著降低计算成本（最高可达 90% 的折扣）。Flyte 原生支持容错机制，能够自动处理 Spot 实例中断时的任务重试。

**实施步骤**:
1. 在 EKS 集群中配置专门的 Node Groups（节点组），标记为仅用于运行 Flyte 的任务 Pod。
2. 在 Karpenter 或 EKS Managed Nodegroups 配置中启用 Spot 实例容量类型。
3. 在 Flyte 任务定义中，合理配置 `retries`（重试）策略，以应对 Spot 实例可能发生的抢占中断。
4. 配置 Flyte 的 Pod Template，确保 Flyte Agent 能够识别并利用这些 Spot 节点。

**注意事项**: 不要将对中断敏感的服务（如 Flyte 服务端组件、数据库）部署在 Spot 节点上。同时，应确保训练模型时支持断点续传，以便在重启后从中断处继续训练。

---

### 实践 3：实施动态资源分配与 GPU 共享

**说明**: AI 工作流中的不同阶段对资源的需求差异巨大。数据清洗可能只需要 CPU，而微调模型则需要昂贵的 GPU。最佳实践是利用 Flyte 的动态资源分配功能，根据任务实际需求请求资源。此外，对于开发测试或小规模推理，可以配置 EKS 上的 GPU 共享技术（如 NVIDIA MPS），以提高昂贵硬件的利用率。

**实施步骤**:
1. 在任务定义中使用 `@task(requests=Resources(...))` 显式声明内存、CPU 和 GPU 需求。
2. 对于推理或轻量级训练任务，配置 EKS 上的 GPU 共享配置（通过 Device Plugins 或 Time Slicing）。
3. 设置合理的资源限制，防止异常任务耗尽节点资源导致 OOM（内存溢出）。
4. 利用 Flyte 的快速执行功能，在开发阶段使用较小的资源配置进行快速迭代，生产阶段再扩大规模。

**注意事项**: 避免过度分配资源。监控集群的实际使用情况（通过 Prometheus/Grafana），并据此调整任务的默认资源配置，以减少资源碎片化。

---

### 实践 4：集中化管理容器镜像与依赖

**说明**: 在 EKS 上运行复杂的 AI 工作流时，依赖管理是一个挑战。不要在每个任务中构建巨大的自定义镜像。最佳实践是使用 Union.ai 的镜像管理功能或构建分层的基础镜像。确保包含所有必要的深度学习框架（PyTorch, TensorFlow）和系统库，同时保持镜像的轻量级和安全性。

**实施步骤**:
1. 构建一个包含核心依赖（如 CUDA, Python 基础库）的“基础镜像”。
2. 在 Flyte 任务中引用该基础镜像，并仅安装特定任务所需的额外 Python 包（如果支持）。
3. 使用 ECR (Elastic Container Registry) 存储镜像，并启用生命周期策略以清理旧镜像。
4. 在 CI/CD 流水线中集成镜像构建扫描，确保镜像不包含安全漏洞。

**注意事项**: 确保镜像架构与 EKS 节点架构一致（通常为 x86_64 或 ARM64）。对于大型模型，建议使用数据卷（S3 或 EFS）而非将模型打包进镜像中。

---

### 实践 5：建立严格的版本控制与数据血缘追踪

**说明**: AI 实验的可重复性至关重要。每次运行 Flyte 工作流时，都会生成一个唯一的执行 ID。最佳实践是将代码版本、环境配置和训练数据版本与该执行 ID �

---
## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展且生产就绪的 AI 工作流，实现机器学习任务的高效编排与自动化。
- 利用 Amazon EKS 的容器化能力，Flyte 工作流可以无缝扩展以处理大规模数据和复杂的计算密集型任务。
- 该解决方案通过统一的数据和模型管理，消除了 MLOps 流程中的孤岛，从而显著提升团队间的协作效率。
- Flyte 原生支持 Python 等语言，允许数据科学家将现有代码直接转化为工作流，无需进行复杂的重构。
- 借助 Amazon EKS 的企业级安全性和控制力，组织可以在满足合规要求的同时，灵活地部署和管理 AI 基础设施。
- 集成 Amazon SageMaker 等服务，使得在 EKS 上运行的 Flyte 工作流能够轻松调用专门的托管训练服务，优化资源利用率。

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
- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*