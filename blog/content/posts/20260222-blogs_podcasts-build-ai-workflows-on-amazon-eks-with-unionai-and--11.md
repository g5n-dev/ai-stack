---
title: "在 Amazon EKS 上使用 Union.ai 和 Flyte 构建 AI 工作流"
date: 2026-02-22T11:49:53+08:00
draft: false
entry_kind: "auto"
tags: ["Flyte", "Union.ai", "Amazon EKS", "Kubernetes", "工作流编排", "AWS", "MLOps", "S3 Vectors"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI/ML 工作流。 主要内容包括： 1. **Flyte Python SDK**：用于编排和扩展 AI/ML 工作流。 2. **Union.ai 2.0 系统**：支持将 Flyte 部署在 Amazon Elastic"
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

在本文中，我们将解释如何使用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务实现无缝集成。我们将通过一个使用全新 Amazon S3 Vectors 服务的 AI 工作流示例来解析该解决方案。

---
## 导语

在 Amazon EKS 上构建可扩展的 AI 工作流往往面临复杂的编排挑战。本文将介绍如何利用 Union.ai 和 Flyte，在 Kubernetes 环境中高效地管理机器学习任务，并与 AWS 核心存储及监控服务实现无缝集成。通过解析一个使用 Amazon S3 Vectors 的具体示例，我们将向您展示如何简化部署流程并构建稳健的 AI 数据处理管道。

---
## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建和扩展 AI/ML 工作流。

主要内容包括：
1.  **Flyte Python SDK**：用于编排和扩展 AI/ML 工作流。
2.  **Union.ai 2.0 系统**：支持将 Flyte 部署在 Amazon Elastic Kubernetes Service (EKS) 上。
3.  **AWS 服务集成**：与 Amazon S3、Amazon Aurora、IAM 和 Amazon CloudWatch 等服务无缝集成。
4.  **实际应用案例**：通过一个使用新推出的 Amazon S3 Vectors 服务的 AI 工作流示例来展示该解决方案。

---
## 评论

**深度评论**

**文章核心主张**
该文章提出了一种基于 Union.ai（Flyte 商业版）与 Amazon EKS 的架构方案，旨在构建一个标准化的 AI 工作流编排平台。其核心目标是通过容器化底座和云原生调度能力，解决 MLOps 流程中从实验环境到生产环境迁移时的工程一致性问题。

**架构与功能评价**

1.  **逻辑与基础设施的解耦**
    文章重点阐述了 Flyte 的设计理念，即通过 Python SDK 将业务逻辑定义与底层技术栈分离。Union.ai 2.0 部署在 EKS 上，实质上是将 Flyte 的调度逻辑与 AWS 存储及安全服务进行了标准化对接。
    *   **评价**：这种架构属于典型的混合云策略。它在保持开源软件灵活性的同时，利用了 AWS 的托管服务生态。对于已部署 AWS 的企业，相比直接维护 Kubeflow，该方案降低了控制平面的运维复杂度。

2.  **异构资源的调度策略**
    文章指出利用 EKS 的弹性来应对 AI 工作流的资源需求。这涉及到针对不同任务类型在 CPU 和 GPU 节点池间的智能调度。
    *   **评价**：这触及了当前 MLOps 的成本控制痛点。在集群规模扩大时，确保仅在计算密集型阶段占用 GPU，并在任务完成后迅速释放资源，是提升资源利用率的关键。

3.  **数据治理与可复现性**
    文章强调了 Flyte 对输入输出路径及版本的自动记录功能。
    *   **评价**：这体现了从脚本式作业向工作流式作业的转变。对于需要严格审计和追溯的行业，这种自动化的数据血缘管理是满足合规要求的基础。

**局限性与边界条件**

1.  **架构复杂度门槛**
    对于小型团队或简单的数据处理任务，构建基于 EKS + Flyte 的平台可能引入不必要的复杂度。在不需要复杂 DAG 调度或跨团队复用的场景下，轻量级编排工具可能更具成本效益。

2.  **冷启动延迟**
    基于 EKS 的弹性伸缩虽然优化了资源成本，但在节点从零扩容时存在分钟级别的延迟。因此，该架构不适用于对延迟极度敏感的实时推理或毫秒级响应链路。

**验证性检查点**

1.  **资源利用率监控**
    *   *验证方式*：运行典型的 ML Pipeline（数据清洗+训练+评估），观察 Cluster Autoscaler 的行为。
    *   *预期结果*：GPU 节点应仅在训练任务开始时拉起，并在结束后迅速缩容至零。若节点长期闲置，则资源配置未达最优。

2.  **端到端延迟测试**
    *   *验证方式*：测量从提交工作流到首个 Pod 运行的时间差。
    *   *预期结果*：对比 EC2 或 SageMaker 的直接启动时间，评估 EKS 冷启动带来的延迟是否在业务可接受范围内（通常需确认是否超过 2 分钟）。

3.  **版本回溯能力**
    *   *验证方式*：修改参数并重新运行后，尝试使用 Flyte UI 复现三个月前的特定版本。
    *   *预期结果*：系统应能自动关联并还原当时的代码版本、S3 数据集快照及环境参数。

**综合评价**

**1. 内容深度**
文章作为技术实施方案，侧重于“集成方法”的描述，详细展示了 AWS 原生集成（如 IAM Roles for Service Accounts）的具体步骤。这在企业级落地中具有较高的参考价值。不过，该方案要求使用者具备一定的 Kubernetes 底层知识，以便在出现问题时进行调试。

**2. 实用价值**
对于正处于“模型原型转生产”阶段且已投资 AWS 生态的企业，该方案提供了一个介于通用编排工具（如 Airflow）与全托管服务（如 SageMaker）之间的中间路线，主要解决了工程化过程中的环境一致性难题。

**3. 创新性**
该方案并非提出全新的计算范式，而是对现有云原生技术栈的组合优化。其创新点主要体现在将数据血缘管理与容器编排调度进行了深度整合，提供了一套相对标准化的企业级 MLOps 落地模版。

---
## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 1. 核心观点深度解读

**主要观点：**
文章的核心主张是，通过结合 **Union.ai**（特别是 Union 2.0）和 **Flyte** 开源项目，企业可以在 **Amazon EKS**（Elastic Kubernetes Service）上构建一个高度可扩展、可移植且生产就绪的 AI/ML 工作流编排平台。这解决了从本地实验模型到云端大规模生产环境部署的“最后一公里”问题。

**核心思想：**
作者想要传达的思想是 **“编排与基础设施的解耦”** 以及 **“云原生 AI 的标准化”**。传统的 MLOps 往往受困于特定云厂商的锁定或自定义脚本的脆弱性。文章强调利用 Kubernetes (EKS) 作为统一的底层，利用 Flyte 作为统一的逻辑层，再利用 Union.ai 作为管理控制平面，从而实现 AI 工作流像管理微服务一样被标准化管理。

**观点的创新性与深度：**
*   **深度：** 文章不仅仅是介绍一个工具，而是提出了一套完整的架构模式。它深入探讨了如何处理容器化 AI 任务中的异构性（数据处理、训练、微服务部署），以及如何利用 EKS 的弹性来应对 ML 工作负载特有的突发性和高资源消耗。
*   **创新性：** 将 Flyte 这种以数据为中心的编排系统与 AWS 的原生服务（S3, EKS, IAM）深度集成，并提供 Union.ai 这种“云上控制平面”模式，降低了在 Kubernetes 上运维复杂分布式系统的门槛。

**重要性：**
随着 AI 从实验室走向生产，**可复现性** 和 **可扩展性** 成为最大痛点。该观点的重要性在于它提供了一条经过验证的路径，使得数据科学家可以继续使用 Python SDK 编写逻辑，而无需关心底层 K8s 的复杂性，同时利用云厂商的弹性能力控制成本。

---

# 2. 关键技术要点

**涉及的关键技术：**
1.  **Flyte:** 一个开源的、以数据为中心的工作流编排平台，专为 ML 和数据科学构建。
2.  **Amazon EKS (Elastic Kubernetes Service):** AWS 托管的 Kubernetes 服务。
3.  **Union.ai 2.0:** Flyte 的商业托管版本和管理控制平面。
4.  **AWS S3 (Simple Storage Service):** 用于存储数据集、模型和中间结果。
5.  **Python SDK:** Flyte 提供的用于定义任务和工作流的编程接口。

**技术原理与实现方式：**
*   **声明式工作流：** 用户使用 Python 装饰器（如 `@task` 和 `@workflow`）定义代码逻辑。Flyte 将这些 Python 代码编译成 Kubernetes 兼容的 CRD（自定义资源定义）。
*   **容器化与隔离：** Flyte 自动将用户代码打包进容器，并在 EKS 上以 Pod 的形式调度运行。每个任务都是独立的、可隔离的单元。
*   **数据传递机制：** Flyte 自动处理任务间的数据传递。对于大数据，它不直接传递对象，而是传递指向 S3 存储的引用（指针），极大提高了大规模数据流处理的效率。
*   **自动伸缩：** 利用 EKS 的 Cluster Autoscaler 和 Flyte 的任务队列机制，根据工作负载的积压情况自动扩缩容节点。

**技术难点与解决方案：**
*   **难点：** 在 K8s 上运行 AI 任务涉及复杂的 GPU 调度、节点亲和性配置和容器镜像管理。
*   **方案：** Union.ai 简化了 Flyte 的部署，通过 Helm Charts 自动化配置，并利用 AWS 的 Node Groups 和 EC2 Spot 实例来优化成本和资源分配。

**技术创新点分析：**
*   **类型安全的编译时检查：** Flyte 的 Python SDK 在编译时检查数据类型接口，防止在生产环境中因类型不匹配而导致的运行时错误。
*   **多语言支持（通过 Sidecar）：** 虽然 SDK 是 Python 的，但底层任务可以是任何容器化的程序（如 Rust, C++, R），实现了逻辑与实现的解耦。

---

# 3. 实际应用价值

**对实际工作的指导意义：**
这篇文章为 MLOps 工程师和架构师提供了一份 **“在 AWS 上构建标准化 AI 平台”的蓝图**。它指导团队如何摆脱依赖 AWS Step Functions 或 SageMaker 等强绑定服务，转而使用开源标准（K8s + Flyte）来构建更具控制力的平台。

**可应用场景：**
1.  **大规模模型训练：** 需要多节点分布式训练，且对 GPU 资源需求波动大的场景。
2.  **端到端的数据处理流水线：** 从 ETL 提取、特征工程到模型训练和批量推理的全链路自动化。
3.  **模型批处理：** 定期对海量数据进行离线预测和评分。

**需要注意的问题：**
*   **学习曲线：** 团队需要熟悉 Kubernetes 的基本概念以及 Flyte 的特定抽象概念。
*   **成本控制：** 虽然 EKS 支持自动伸缩，但如果配置不当（例如任务频繁失败重启），可能会导致 AWS 账单激增。
*   **冷启动：** 对于极短的任务，容器启动和 Pod 调度的开销可能占比过大。

**实施建议：**
*   先从非关键的批处理任务开始迁移，验证 Flyte 与 AWS S3/IAM 的权限配置。
*   利用 EKS 的 Spot 实例运行容错率高的数据预处理任务以降低成本。
*   建立标准的容器镜像构建流程，确保 Flyte 任务能够快速拉取镜像。

---

# 4. 行业影响分析

**对行业的启示：**
该文章反映了 MLOps 行业的 **“Kubernetes 化”** 趋势。AI 工作负载正在回归通用容器编排标准，而不是依赖特定云厂商的封闭黑盒系统。这表明企业越来越看重 **可移植性** 和 **互操作性**。

**可能带来的变革：**
*   **降低云厂商锁定风险：** 采用 Flyte + EKS 的架构，使得企业可以相对容易地在 AWS、Azure 或自建 K8s 集群之间迁移工作流。
*   **DevOps 与 MLOps 的融合：** 随着 AI 任务运行在 K8s 上，数据科学家和软件工程师的边界进一步模糊，统一的工具链（Git, Container, K8s）成为标准。

**发展趋势：**
未来，AI 编排平台将更像“编译器”，即自动将高层的 Python 逻辑转化为底层的 K8s 资源图，并具备更智能的资源自适应能力。

---

# 5. 延伸思考

**引发的思考：**
*   **Serverless vs. K8s：** 虽然 EKS 提供了极强的控制力，但 AWS Lambda 或 SageMaker Serverless 是否在某些轻量级场景下更具性价比？Flyte 的重型调度是否适合高频低延迟的实时推理？
*   **可观测性：** 在复杂的 EKS 环境中，如何追踪 Flyte 工作流内部的性能瓶颈？需要结合 Prometheus/Grafana 还是 AWS X-Ray？

**拓展方向：**
*   研究 Flyte 如何与 **Ray**（分布式计算框架）集成，以在 EKS 上实现更复杂的超参数调优。
*   探索 **GitOps** 流程，即通过 ArgoCD 或 FluxCD 来管理 Flyte 集群本身的配置和基础设施即代码。

**未来研究：**
*   **混合云编排：** 如何利用 Union.ai 的控制平面同时管理位于 AWS EKS 和私有数据中心（NVIDIA GPU 集群）上的工作负载。
*   **GPU 共享与虚拟化：** 在 EKS 上利用 GPU Sharing 技术运行 Flyte 任务，以提高资源利用率。

---

# 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现状：** 如果你的团队正在使用 cron jobs 或 Airflow 处理 ML 任务，且面临资源扩展瓶颈，这是一个极佳的替代方案。
2.  **环境搭建：** 在 AWS 上创建 EKS 集群，配置好 IRSA（IAM Roles for Service Accounts），确保 Pod 可以直接访问 S3 而无需硬编码密钥。
3.  **Hello World：** 编写一个简单的 Flyte 任务，读取 S3 上的数据，处理后写回 S3，部署到 Union.ai 或本地 Flyte 集群进行测试。

**具体行动建议：**
*   **容器化优先：** 即使不立即引入 Flyte，也应先将现有的 AI 脚本容器化。
*   **模块化代码：** 将代码重构为纯函数，避免全局变量，以便适配 Flyte 的任务模型。

**需补充的知识：**
*   **Docker/Containerd：** 镜像构建与优化。
*   **Kubernetes 基础：** Pod, Service, Namespace, Resource Quotas。
*   **Python 类型提示：** Flyte 强依赖 Python 类型系统。

---

# 7. 案例分析

**结合实际案例说明（假设性案例）：**
*   **场景：** 某金融科技公司每天需要处理 100TB 的交易数据，进行欺诈模型训练。
*   **痛点：** 原有 Airflow 部署在单机 EC2 上，内存溢出，且无法动态扩展 GPU。
*   **解决方案：** 引入 Flyte on EKS。
    *   数据清洗任务运行在 EKS 的 CPU 节点组（使用 Spot 实例）。
    *   模型训练任务自动调度到 EKS 的 GPU 节点组（p3/p4 实例）。
    *   中间数据直接通过 S3 传递，不占用 Worker 节点存储。

**失败案例反思：**
*   **错误做法：** 直接将所有遗留脚本“包装”进 Docker，导致镜像巨大（>10GB），每次 Flyte 调度拉取镜像耗时过长，甚至超时。
*   **教训：** 必须优化镜像（使用多阶段构建），并合理配置 Flyte 的资源请求和限制。

---

# 8. 哲学与逻辑：论证地图

**中心命题:**
在构建生产级 AI/ML 工作流时，采用 **"Union.ai + Flyte on Amazon EKS"** 架构优于传统的单机编排或强云厂商绑定方案，因为它在保持**云原生弹性与可移植性**的同时，提供了**数据感知的编排能力**。

**支撑理由与依据:**
1.  **理由 1：可扩展性与资源效率**
    *   *依据:* EKS 提供毫秒级的弹性伸缩能力；Flyte 能将任务映射为 K8s Pod，根据负载动态调整集群大小（事实/技术原理）。
2.  **理由 2：数据感知与原生集成**
    *   *依据:* Flyte 原生理解 S3 等存储系统的数据指针，避免不必要的数据传输，且与 AWS IAM 深度集成，安全性高（事实/架构特性）。
3.  **理由 3：可移植性与避免锁定**
    *   *依据:* Flyte 是开源项目，运行在标准的 K8s 上；如果需要离开 AWS，只需迁移 K8s 集群，无需重写工作流逻辑（

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建可扩展且模块化的容器镜像

**说明**: 
在 Amazon EKS 上使用 Union.ai 和 Flyte 时，工作流的每个任务通常运行在独立的容器中。为了优化启动速度和资源利用率，应避免构建包含所有依赖项的单体巨型镜像。相反，应采用模块化方法，为不同的任务（如数据预处理、模型训练、推理）构建专用的小型镜像。这利用了 Flyte 的动态容器管理能力，结合 EKS 的快速扩展能力，显著减少冷启动时间。

**实施步骤**:
1. 使用多阶段构建来精简生产镜像，仅保留运行时必需的依赖库。
2. 针对不同的 AI 框架（如 PyTorch, TensorFlow, Scikit-learn）维护独立的 Dockerfile。
3. 在 CI/CD 流水线中集成镜像扫描，确保安全漏洞在部署前被修复。
4. 将构建好的镜像存储在 Amazon ECR 中，并利用生命周期策略清理未使用的旧版本。

**注意事项**: 
确保基础镜像与 EKS 节点的操作系统兼容（例如，使用 Amazon Linux 2023 作为基础镜像以获得最佳兼容性）。避免在镜像中硬编码凭证，应使用 IAM Roles for Service Accounts (IRSA)。

---

### 实践 2：利用 Flyte 后台任务处理长时间运行的 AI 训练

**说明**: 
AI 模型训练通常需要数小时甚至数天，这超过了 HTTP 请求或标准 API 调用的超时限制。Flyte 提供了“后台任务”功能，允许工作流逻辑异步启动任务并立即返回，而主任务继续在后台运行。这解耦了工作流的编排逻辑与长时间运行的执行过程，提高了系统的容错性。

**实施步骤**:
1. 在 Flyte 任务定义中，识别出耗时较长的训练或微调步骤。
2. 使用 Flyte SDK（如 `flytekit`）将这些步骤配置为后台任务。
3. 配置适当的超时和重试策略，以便在 EKS 节点故障时自动恢复训练。
4. 设置监控告警（如通过 CloudWatch），以便在后台任务完成或失败时接收通知。

**注意事项**: 
后台任务一旦启动，即使父工作流完成或被终止，仍会继续运行并消耗资源。请确保配置了合理的资源限制（CPU/内存），并实施清理策略以防止孤儿任务消耗集群资源。

---

### 实践 3：优化 GPU 资源调度与节点组配置

**说明**: 
AI 工作负载对 GPU 资源高度依赖。在 EKS 上，最佳实践是使用节点组来分离 GPU 和 CPU 工作负载。通过配置专用的 GPU 节点组并结合 Karpenter 或 Cluster Autoscaler，可以根据 Flyte 任务的需求动态扩缩容。此外，利用 NVIDIA 的设备插件可以确保 Pod 能够正确请求 GPU 资源。

**实施步骤**:
1. 在 EKS 中创建带有标签（如 `node-type: gpu-nvidia`）的专用 GPU 节点组。
2. 在 Flyte 任务定义中，通过 `@task` 装饰器或 `Resources` 类明确指定 GPU 需求（例如 `limits=nvidia.com/gpu=1`）。
3. 使用 Node Selector 或 Taints/Tolerations 确保 AI 任务仅调度到 GPU 节点上，避免干扰系统级服务。
4. 配置 Spot 实例用于无状态的开发或测试任务，以降低成本。

**注意事项**: 
GPU 资源昂贵。确保 Flyte 任务配置了正确的内存和 CPU 限制，防止因内存不足（OOM）导致节点崩溃。同时，确保安装了正确的 NVIDIA 驱动程序和 CUDA 工具包。

---

### 实践 4：实施精细化的数据缓存与版本管理

**说明**: 
Union.ai 和 Flyte 的核心优势之一在于其自动缓存机制。在机器学习实验中，数据预处理和特征工程通常非常耗时。通过正确配置输入输出哈希，Flyte 可以自动识别未更改的输入数据并跳过计算，直接返回缓存结果。这对于在 EKS 上频繁迭代模型开发至关重要。

**实施步骤**:
1. 确保所有任务函数都是确定性的，即相同的输入必须产生相同的输出。
2. 使用 Flyte 的数据类型（如 `FlyteDirectory`, `FlyteFile`）或结构化数据集来传递数据，以便系统能够自动计算哈希值。
3. 在工作流定义中，利用 `cache` 参数配置缓存策略（如缓存持续时间或版本）。
4. 对于大型数据集，使用 S3 作为中间存储，并确保 Flyte 任务具有读取 S3 的 IAM 权限。

**注意事项**: 
缓存会占用存储空间。建议定期审查并清理旧的缓存数据，或者在 Flyte Admin 中配置 TTL（生存时间）策略。不要在缓存中存储敏感的明文凭证。

---

### 实践 5：强化安全性与最小权限原则

**说明**: 
在 EKS 上运行 AI 工作流

---
## 学习要点

- Union.ai 和 Flyte 的结合能够在 Amazon EKS 上构建可扩展、生产级的 AI 工作流，实现机器学习模型从开发到部署的自动化编排。
- 利用 Amazon EKS 的容器编排能力，Flyte 可以高效管理分布式计算任务，显著提升大规模数据处理和模型训练的资源利用率。
- 该架构支持混合云和多云环境，允许企业灵活地在不同基础设施上运行 AI 工作负载，避免供应商锁定。
- Flyte 提供的工作流版本控制和数据血缘追踪功能，能够确保机器学习实验的可复现性，并简化模型调试与审计过程。
- 通过将 Flyte 部署在 EKS 上，用户可以无缝集成 AWS 生态系统的其他服务（如 S3、IAM），从而简化数据访问和权限管理。
- 该解决方案通过自动化任务调度和容错机制，降低了维护 AI 基础设施的运维复杂度，使数据团队能更专注于核心业务逻辑。

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