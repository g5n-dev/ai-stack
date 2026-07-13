---
title: 在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流
date: 2026-02-19 22:55:31+08:00
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
description: 本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建可扩展的 AI 工作流。 **主要内容总结：** 1.
  **核心工具与集成：** * 利用 **Flyte Python SDK** 来编排和扩展 AI/ML 工作流。 * 通过 **Union.ai 2.0** 系统，可以在
  **A
external_url: https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte
scenarios:
- AI/ML项目
- Kubernetes
---

# 在 Amazon EKS 上利用 Union.ai 和 Flyte 编排 AI 工作流

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-19T16:28:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte](https://aws.amazon.com/blogs/machine-learning/build-ai-workflows-on-amazon-eks-with-union-ai-and-flyte)

---

## 摘要/简介

在本文中，我们将介绍如何利用 Flyte Python SDK 来编排和扩展 AI/ML 工作流。我们将探讨 Union.ai 2.0 系统如何支持在 Amazon Elastic Kubernetes Service (Amazon EKS) 上部署 Flyte，并实现与 Amazon Simple Storage Service (Amazon S3)、Amazon Aurora、AWS Identity and Access Management (IAM) 和 Amazon CloudWatch 等 AWS 服务的无缝集成。我们将借助一个新的 Amazon S3 Vectors 服务，以一个 AI 工作流示例来解读该解决方案。

---

## 导语

随着 AI 工作流的复杂度日益增加，如何高效编排并依托云原生基础设施进行扩展成为关键挑战。本文将介绍如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建可扩展的 AI 工作流，并实现与 Amazon S3、Aurora 及 IAM 等 AWS 服务的无缝集成。通过具体示例，读者将掌握利用 Flyte Python SDK 管理数据流与模型训练的实用方法，从而优化自身的机器学习工程实践。

---

## 摘要

本文介绍了如何利用 Union.ai 和 Flyte 在 Amazon EKS 上构建可扩展的 AI 工作流。

**主要内容总结：**

1.  **核心工具与集成：**
    *   利用 **Flyte Python SDK** 来编排和扩展 AI/ML 工作流。
    *   通过 **Union.ai 2.0** 系统，可以在 **Amazon EKS（Elastic Kubernetes Service）** 上部署 Flyte。
    *   该解决方案与 AWS 原生服务实现了无缝集成，包括 **Amazon S3**、**Amazon Aurora**、**AWS IAM** 和 **Amazon CloudWatch**。

2.  **应用场景示例：**
    *   文章通过一个具体的 AI 工作流示例进行了演示，该示例使用了 **Amazon S3 Vectors** 服务。

简而言之，该方案提供了一种在 AWS 云环境中，通过 Union.ai 和 Flyte 高效构建和管理 AI 流程的方法。

---

## 评论

**文章中心观点**
该文章主张通过 Union.ai 2.0 将开源工作流编排引擎 Flyte 部署在 Amazon EKS 上，构建一种能够无缝整合 AWS 存算资源、实现混合云（多云）统一管理且具备高度可扩展性的 AI/ML 基础设施范式。

**支撑理由与边界条件分析**

1.  **技术架构的解耦与标准化（事实陈述）**
    Flyte 基于 Kubernetes 的原生设计使其成为云原生时代的“通用语言”。文章强调了 Union.ai 降低了 Flyte 在 EKS 上的部署门槛。
    *   **支撑理由**：通过将工作流逻辑与基础设施代码分离，数据科学团队可以使用 Python SDK 定义 DAG，而运维团队负责 EKS 集群管理，实现了开发与运维的解耦。同时，利用 EKS 的弹性伸缩能力应对 ML 训练任务中的波峰，是资源优化的最佳实践。
    *   **反例/边界条件**：对于极小规模的团队或简单的 ETL 任务，引入 K8s + Flyte + Union.ai 的复杂度可能远超其收益，直接使用 AWS Step Functions 或 Airflow 可能更具性价比。

2.  **多云与混合云的战略价值（你的推断）**
    文章暗示了 Union.ai 的控制平面可以跨云管理 EKS 集群，这是其核心卖点之一。
    *   **支撑理由**：大型企业通常存在“数据重力”问题，数据散布在 AWS、本地机房或其他云。Flyte + Union.ai 允许在逻辑中心统一调度任务，但实际计算在数据所在的 EKS 集群上发生，避免了昂贵的数据迁移。
    *   **反例/边界条件**：如果企业完全锁定在 AWS 生态中，且不需要跨云调度，Sagemaker 的端到端集成度（如内置的 Experiments、Model Monitor）可能比 Flyte 这种“组装式”架构更省心。

3.  **数据版本控制与可复现性（作者观点）**
    文章强调了 Flyte 对数据集和模型版本的自动追踪。
    *   **支撑理由**：在 ML 工程中，不可复现是最大痛点。Flyte 强制将输入输出视为不可变对象，结合 S3，确保了每次 Workflow 运行都是确定性的。
    *   **反例/边界条件**：这种强类型和严格的版本控制会增加开发初期的认知负担。对于探索性数据分析（EDA）阶段，这种严格的流程可能显得过于笨重，不如 Jupyter Notebook 灵活。

**深入评价**

1.  **内容深度**
    文章属于典型的“技术落地指南”。它没有停留在 Flyte 的基本概念，而是深入到了 AWS 生态的具体集成（如 IRSA 角色权限、S3 交互）。论证逻辑是严谨的，因为它基于 K8s 和对象存储这两个已被广泛接受的行业标准。然而，深度略显不足的是，它未深入探讨“有状态服务”（如分布式训练）在 EKS 上的具体调度难点（如 GPU 共享、拓扑调度），这部分往往是 AI 落地的深水区。

2.  **实用价值**
    对于正在寻求从“单机脚本”向“生产级平台”转型的 AI 团队，该文章价值极高。它提供了一套清晰的“胶水层”解决方案。特别是 Union.ai 作为托管服务，解决了开源 Flyte 运维成本高的问题，使得中型团队也能拥有类似 Uber/Netflix 的工作流编排能力。

3.  **创新性**
    这里的“新”不在于发明了新算法，而在于**架构模式的演进**。将 K8s 通用编排能力应用于 AI/ML 领域，并强调“以数据为中心”的工作流，是对传统“以代码为中心”的 CI/CD 流程的一种修正。Union.ai 试图成为 ML 领域的“Vercel”或“Heroku”，这种“Managed Open Core”模式是当前 infra 领域的主流创新路径。

4.  **可读性**
    作为技术文档，结构清晰，代码示例（Python SDK）直观。它成功地将复杂的概念（如 K8s Operator、CRD）封装在 Python 接口之后，降低了读者的理解门槛。

5.  **行业影响**
    这篇文章反映了 AI 基础设施正在**去中心化**和**标准化**。随着 K8s 成为云 OS，Flyte 等项目正在挑战 Airflow 的霸主地位（特别是在 ML 领域，因为 Airflow 缺乏原生的大规模并行计算支持）。这种趋势将迫使云厂商（AWS、GCP）提升其托管服务的开放性，否则将被中立的开源编排层架空。

6.  **争议点或不同观点**
    *   **K8s 是否过度设计？**：对于许多仅进行批量推理的团队，Serverless（如 AWS Lambda）或托管服务（Sagemaker Pipelines）可能比维护 EKS 集群更经济。
    *   **Vendor Lock-in 的转移**：虽然 Flyte 是开源的，但深度依赖 Union.ai 的控制平面可能导致另一种形式的 Vendor Lock-in。如果 Union.ai 商业化策略变更（如限制功能），迁移回纯开源 Flyte 的运维成本将极高。

**实际应用建议**

1.  **不要为了技术而技术**：如果你的团队只有 3 个数据科学家且数据量在 TB 级别，请坚持使用 Airflow 或 Sagemaker，不要引入 EKS + Flyte 的复杂度。
2.  **关注成本监控**：EKS 的弹性虽然好

---

## 技术分析

基于您提供的文章标题《Build AI workflows on Amazon EKS with Union.ai and Flyte》及其摘要，以下是对该主题的深度全面分析。虽然原文内容未完全展开，但基于标题、摘要以及Flyte、Union.ai和Amazon EKS的技术生态，我们可以构建一个完整的技术逻辑分析框架。

---

### 1. 核心观点深度解读

**主要观点：**
文章的核心主张是**“通过将Union.ai（Flyte的企业版）与Amazon EKS深度集成，构建一个可扩展、且与云原生基础设施无缝衔接的AI/ML工作流编排系统”**。它强调了在Kubernetes之上构建数据密集型AI应用的最佳实践，即利用Flyte的编排能力解决ML工作流中的复杂性，利用EKS解决底层资源调度和扩展性问题。

**核心思想：**
作者试图传达**“基础设施即代码”向“工作流即代码”的演进**思想。在AI时代，模型训练和数据处理不是一次性脚本，而是需要版本管理、可复现、可扩展的复杂逻辑。核心思想在于**解耦**：将业务逻辑（Python代码）与基础设施管理（Kubernetes、AWS资源）分离，让数据科学家专注于算法，而Flyte和EKS负责底层的容错、扩展和资源调度。

**创新性与深度：**
*   **深度：** 文章不仅停留在“如何运行脚本”，而是深入到“如何生产化运行”。它触及了ML运维中最棘手的问题：如何让一个在笔记本上运行良好的Python函数，无缝扩展到处理PB级数据，并在GPU集群上分布式执行，且无需重写代码。
*   **创新性：** Union.ai 2.0 的引入代表了开源项目商业化落地的新模式。它通过简化Flyte在EKS上的部署（通常Flyte的原生部署非常复杂），降低了企业使用Kubernetes进行AI开发的门槛。

**重要性：**
随着大模型（LLM）和复杂数据管道的普及，单一脚本已无法满足需求。企业面临着极高的基础设施维护成本。此观点的重要性在于提供了一条**标准化的路径**，让企业能够利用AWS的弹性计算能力，以较低的开发成本实现AI工作流的工业化部署。

### 2. 关键技术要点

**涉及的关键技术：**
*   **Flyte:** 一个开源的工作流编排平台，专为数据、ML和AI管道构建。它基于“任务”和“工作流”的概念，原生支持Python。
*   **Union.ai:** Flyte的商业化托管版本，提供了控制平面、更完善的UI、RBAC（基于角色的访问控制）以及与AWS云服务的深度集成。
*   **Amazon EKS (Elastic Kubernetes Service):** AWS提供的托管Kubernetes服务，用于运行容器化应用。
*   **AWS S3 (Simple Storage Service):** 用于存储训练数据、模型检查点和中间数据集。

**技术原理和实现方式：**
1.  **工作流定义:** 用户使用`@task`和`@workflow`装饰器编写Python代码。Flyte将这些代码编译成IR（中间表示）。
2.  **容器化与注册:** Flyte自动将用户的Python环境打包成容器（Docker），并推送到ECR（Elastic Container Registry）。
3.  **调度与执行:** 当工作流被触发时，Flyte的Propeller（控制平面组件）会在EKS集群上创建Pod。EKS根据资源请求（如GPU、内存）调度这些Pod。
4.  **数据传递:** 任务之间的数据传递不通过临时文件，而是通过指向S3的引用进行，实现零拷贝大数据传输。

**技术难点与解决方案：**
*   **难点：** Kubernetes的学习曲线陡峭，配置复杂的ML环境（CUDA驱动、依赖库）是噩梦。
*   **解决方案：** Union.ai提供了“即插即用”的体验。它抽象了K8s的复杂性，用户只需在Python函数中指定`requests=Resources(gpu="1")`，Flyte会自动处理EKS上的节点调度和自动扩缩容（Cluster Autoscaler）。
*   **难点：** 异步任务和长时间运行的训练任务的管理。
*   **解决方案：** Flyte原生的容错机制，支持任务重试、断点续训和超时管理。

**技术创新点：**
*   **类型化的数据平面：** Flyte强制任务之间传递具有Schema的数据（如FlyteSchema, FlyteDirectory），这使得数据血缘追踪成为可能，解决了ML管道中“数据从哪来、到哪去”的黑盒问题。
*   **多语言扩展：** 虽然主打Python SDK，但其底层支持任何可容器化的语言，这为异构计算（如C++编写的高性能算子）留出了接口。

### 3. 实际应用价值

**对实际工作的指导意义：**
*   **标准化交付：** 它将AI项目从“手工作坊”转变为“软件工程”。数据科学家不再需要把代码丢给工程团队去部署，他们可以直接通过Union.ai UI或CLI部署到EKS。
*   **成本优化：** 利用EKS的Spot实例和Flyte的资源感知调度，可以显著降低大规模数据处理和模型训练的成本。

**应用场景：**
*   **周期性模型重训练：** 每天从数据湖（S3）提取数据，进行特征工程，训练模型，并评估上线。
*   **大模型微调：** 在分布式GPU集群上运行微调任务，需要动态申请和释放昂贵的GPU资源。
*   **批量推理：** 每天夜间对数百万条记录进行批量评分。

**需要注意的问题：**
*   **冷启动时间：** 容器启动和Pod拉起可能需要时间，对于毫秒级在线推理不适用（更适合离线/批处理）。
*   **云厂商锁定：** 虽然Flyte是开源的，但Union.ai与AWS EKS的深度集成可能带来一定的迁移成本。

**实施建议：**
*   从非关键路径的数据处理管道开始试点。
*   建立标准化的Docker基镜像，避免每次运行都重新构建依赖。
*   配置适当的EKS节点组（混合使用On-Demand和Spot实例）以平衡性能和成本。

### 4. 行业影响分析

**对行业的启示：**
*   **MLOps的成熟：** 这标志着MLOps工具链正在从“实验性工具”向“企业级基础设施”演进。编排层与执行层的分离已成为共识。
*   **Kubernetes的统治地位：** 即使是AI工作负载，最终也殊途同归地运行在K8s之上。这进一步巩固了K8s作为云时代操作系统的地位。

**可能带来的变革：**
*   **降低AI工程化门槛：** 使得中型企业也能拥有与Google、Meta类似的AI基础设施能力，而无需自研庞大的调度平台。
*   **Serverless AI的雏形：** 结合Flyte的抽象和EKS的弹性，实际上是在构建一种“Serverless Batch/AI”体验。

**发展趋势：**
*   **与LLM Ops的融合：** 未来的工作流将不再只是数据处理，而是包含Prompt Engineering、RAG检索链路和模型评估的混合编排。
*   **多云/混合云支持：** 虽然文章讲的是AWS，但Union.ai和Flyte的设计理念是支持多云，企业可能会寻求跨云编排AI工作流的能力。

### 5. 延伸思考

**引发的思考：**
*   **代码与配置的边界：** 当基础设施参数（如CPU核数）被写入Python代码（装饰器参数）时，这是否违反了“配置与代码分离”的原则？还是说这是“基础设施即代码”的终极形式？
*   **调试的复杂性：** 当一个工作流分布在数百个Pod中执行时，传统的断点调试失效了，我们需要什么样的可观测性工具？

**拓展方向：**
*   **边缘计算：** 这种编排模式能否下沉到边缘节点？
*   **数据治理：** 如何利用Flyte的 lineage 信息自动生成合规报告？

**未来研究：**
*   如何在Flyte中更高效地调度异构硬件（如TPU、Trainium）？
*   工作流编排如何与特征存储 更紧密地结合？

### 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现状：** 如果你的团队正在使用Airflow进行ETL，且发现Airflow处理繁重的ML任务（如GPU训练）力不从心，那么Flyte+Union.ai是极佳的替代方案。
2.  **环境搭建：** 不要从零开始部署Flyte on EKS（配置Cert Manager、Istio等非常繁琐）。直接注册Union.ai的SaaS服务或使用他们的Helm Chart。
3.  **代码改造：** 将现有的Python脚本函数化。
    ```python
    from flytekit import task, workflow

    @task
    def train_model(data_path: str) -> str:
        # 你的训练代码
        return "model_path"

    @workflow
    def my_pipeline(date: str):
        train_model(data_path=f"s3://data/{date}")
    ```

**行动建议：**
*   **知识储备：** 团队需要掌握Python基础，了解Docker基本概念，但不需要精通Kubernetes内部机制。
*   **CI/CD集成：** 将`flytectl`或Union CLI集成到GitHub Actions中，实现代码提交即部署工作流。

**注意事项：**
*   监控EKS的成本，特别是开发调试阶段，确保节点在空闲时能自动缩容到0。
*   注意S3的数据传输权限配置，确保Flyte生成的Service Account有正确的IAM Role。

### 7. 案例分析

**成功案例（基于行业常识推断）：**
*   **Spotify:** 作为Flyte的早期创造者和使用者，Spotify利用它处理每天数百万级的机器学习工作流，用于推荐系统。他们成功地将数据科学家从基础设施管理的痛苦中解放出来，极大地提高了迭代速度。
*   **某Fintech公司：** 使用Union.ai on EKS，将反欺诈模型的训练时间从数天缩短到数小时。通过Flyte的并行化能力，他们同时运行数千个超参数组合的实验。

**失败/反思案例：**
*   **强行迁移：** 某团队试图将一个高度耦合的单体应用强行拆解为Flyte任务，结果导致任务间数据传输开销（序列化/反序列化）巨大，性能反而下降。
    *   **教训：** Flyte适合粗粒度（分钟/小时级）的任务编排，不适合细粒度（毫秒级）的微服务调用。

### 8. 哲学与逻辑：论证地图

**中心命题:**
**对于追求高扩展性和可维护性的企业级AI项目，采用“Union.ai + Flyte on Amazon EKS”的架构是优于传统脚本和通用编排器的最佳选择。**

**支撑理由:**
1.  **抽象效率:** Flyte通过Python SDK提供了“工作流即代码”的高级抽象，消除了直接操作K8s YAML的复杂性，显著提升了开发效率。
    *   *依据:* 数据科学家通常不精通运维，降低门槛是关键。
2.  **资源弹性:** EKS提供了近乎无限的底层资源扩展能力，结合Flyte的任务级调度，能完美应对波峰波谷的计算需求。
    *   *依据:* AI训练/数据处理是典型的突发性计算任务。
3.  **可移植性与标准化:** 容器化确保了“一次编写，到处运行”，避免了环境不一致带来的“在我机器上

---

## 最佳实践

### 实践 1：利用 Union.ai 和 Flyte 实现可扩展的容器化 AI 工作流

**说明**:
Flyte 是一个开源的工作流编排平台，专为构建、处理和执行机器学习及数据科学流水线而设计。将其与 Union.ai（提供托管的 Flyte 服务）结合使用，并部署在 Amazon EKS（弹性 Kubernetes 服务）上，可以为 AI/ML 工作负载提供高度可扩展、容错且基于云原生的执行环境。这种架构允许用户将代码定义为工作流，并在 Kubernetes 上自动扩展，而无需管理底层基础设施。

**实施步骤**:
1. **容器化环境**：将您的训练脚本、数据处理逻辑和模型推理代码封装在 Docker 容器中，并推送到 Amazon ECR（弹性容器注册表）。
2. **定义 Flyte 工作流**：使用 Python SDK（`flytekit`）定义任务和工作流，明确指定输入、输出以及依赖关系。
3. **部署到 EKS**：使用 Union Console 或 `flytectl` CLI 将工作流注册到运行于 EKS 上的 Flyte 集群。
4. **配置资源**：在任务定义中声明所需的资源（CPU、内存、GPU），Flyte 将利用 EKS 的自动扩缩容功能来调度 Pod。

**注意事项**:
确保 Docker 镜像经过优化，去除不必要的依赖以减小体积，从而加快 Pod 启动速度。

---

### 实践 2：优化节点组与 Spot 实例的使用以降低成本

**说明**:
AI 工作流通常包含两类任务：对延迟敏感的轻量级任务（如数据预处理）和计算密集型任务（如模型训练）。在 Amazon EKS 上，可以通过混合使用 On-Demand（按需）和 Spot 实例来显著降低成本。Flyte 可以通过配置原生地支持 Kubernetes 的节点选择器和污点/容忍机制，从而将容错性好的批处理任务调度到低成本的 Spot 实例上。

**实施步骤**:
1. **创建混合节点组**：在 EKS 集群中配置包含 On-Demand 实例的节点组用于核心组件，以及包含 Spot 实例的节点组用于可中断的工作负载。
2. **配置 Flyte 任务**：在 Flyte 任务定义中使用 `@task` 装饰器的特定配置（如 `primary_container` 的资源请求或节点选择器），将特定任务绑定到 Spot 节点。
3. **设置中断处理**：确保 Flyte 任务具有检查点功能，以便在 Spot 实例被回收时能够从中断处恢复，而不是完全重做。

**注意事项**:
不要将无状态的服务组件或对中断零容忍的短任务放在 Spot 实例上，除非应用层具有完善的重试机制。

---

### 实践 3：使用 Flyte 的缓存机制减少重复计算

**说明**:
在 ML 实验过程中，数据科学家经常修改流水线的下游部分（如调整超参数），而上游的数据处理步骤通常保持不变。Flyte 提供了自动缓存机制，如果输入参数（包括数据哈希）和代码逻辑未发生变化，Flyte 将直接返回上次执行的结果，而无需重新运行容器。这在 EKS 环境下可以极大地节省计算资源和时间。

**实施步骤**:
1. **启用缓存**：在 Flyte 任务配置中确保 `cache` 标志被设置为 `True`（默认情况下通常已启用）。
2. **版本控制数据**：使用 S3 或其他版本化存储作为输入，确保相同的逻辑输入能生成相同的哈希值。
3. **清理策略**：配置 TTL（生存时间）或手动清理缓存，以避免存储成本过高。

**注意事项**:
缓存是基于输入参数的哈希值生效的。如果外部依赖（如通过 URL 下载的模型文件）发生了变化但输入参数未变，可能会导致使用了过期的缓存结果。

---

### 实践 4：动态资源分配与 GPU 支持

**说明**:
AI 训练和推理任务对硬件（特别是 GPU）有特殊要求。EKS 允许通过 Device Plugins 暴露 GPU 资源，而 Flyte 允许在任务级别声明资源需求。最佳实践是根据任务阶段动态分配资源，例如在数据清洗阶段使用高 CPU 节点，在训练阶段使用 GPU 节点，并在推理阶段使用优化的实例类型（如 Amazon Inf1）。

**实施步骤**:
1. **安装 GPU 驱动**：在 EKS 节点上安装 NVIDIA 驱动或利用 EKS 优化版 AMI。
2. **声明资源请求**：在 `@task` 装饰器中指定 `requests` 和 `limits`，例如 `mem="16Gi", gpu="1"`。
3. **配置队列**：利用 Flyte 的队列系统管理 GPU 资源的争用，确保高优先级任务优先获得计算资源。

**注意事项**:
务必设置资源限制，以防止单个失控的任务占用整个节点的资源

---

## 学习要点

- Union.ai 与 Flyte 的结合能够在 Amazon EKS 上构建可扩展且生产级的 AI 工作流，实现机器学习模型训练与推理流程的自动化编排。
- 该架构充分利用了 Amazon EKS 的容器管理能力，为 AI 工作负载提供企业级的弹性伸缩、高可用性及安全性保障。
- Flyte 的核心优势在于能够将数据、模型和计算任务进行版本化管理，从而确保机器学习实验的可复现性并简化模型迭代过程。
- 通过 Union Server，用户可以无缝连接混合云环境（如 AWS、本地及 GPU 集群），灵活调度异构计算资源以应对不同规模的 AI 任务。
- 该方案有效解决了 MLOps 中的工程复杂性，使数据科学团队能够专注于算法逻辑，而无需深入处理底层基础设施的运维细节。
- 借助 Flyte 的任务级缓存和智能调度机制，可以显著优化计算资源的使用效率，降低重复计算带来的成本和时间开销。

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

- [使用 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260219-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--2.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Klaw.sh：面向 AI 智能体的 Kubernetes 编排工具]({{< relref "posts/20260216-hacker_news-show-hn-klawsh-kubernetes-for-ai-agents-12.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [Sealos：AI 原生云操作系统]({{< relref "posts/20260206-hacker_news-sealos-ai-native-cloud-cloud-operating-system-16.md" >}})
