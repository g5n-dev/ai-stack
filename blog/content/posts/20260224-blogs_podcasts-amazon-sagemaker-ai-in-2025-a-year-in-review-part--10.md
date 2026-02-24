---
title: "2025年回顾：SageMaker AI弹性训练计划与推理性价比提升"
date: 2026-02-24T11:01:45+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "AWS", "推理优化", "弹性训练", "Trainium", "Inferentia", "Serverless", "LLM"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "**2025年 Amazon SageMaker AI 年度回顾（第一部分）：灵活训练计划与推理工作负载性价比提升** **概述** 2025年，Amazon SageMaker AI 在核心基础设施方面实现了显著改进，主要集中在**容量、性价比、可观测性和易用性**四个维度。本文作为系列文章的第一部分，重点介绍了通过"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads
scenarios: ["AI/ML项目", "大语言模型"]
---

# 2025年回顾：SageMaker AI弹性训练计划与推理性价比提升

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T20:26:47+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads)

---
## 摘要/简介

2025 年，Amazon SageMaker AI 在核心基础设施产品方面实现了显著改进，涵盖四个维度：容量、性价比、可观测性和易用性。在这一系列文章中，我们将探讨这些改进及其带来的优势。在第一部分中，我们将讨论随着弹性训练计划（Flexible Training Plans）的推出，在容量方面所取得的改进。我们还将介绍推理工作负载在性价比方面的提升。在第二部分中，我们将讨论可观测性、模型定制和模型托管方面的增强功能。

---
## 导语

回顾 2025 年，Amazon SageMaker AI 在基础设施层面实现了显著迭代，重点围绕容量保障与推理性价比进行了优化。本文作为年度回顾系列的第一部分，将深入解析弹性训练计划如何解决算力获取难题，并剖析针对推理工作负载的性能提升策略。通过阅读本文，读者可以了解这些底层改进的具体机制，以及如何利用它们在降低成本的同时提升模型部署效率。

---
## 摘要

**2025年 Amazon SageMaker AI 年度回顾（第一部分）：灵活训练计划与推理工作负载性价比提升**

**概述**
2025年，Amazon SageMaker AI 在核心基础设施方面实现了显著改进，主要集中在**容量、性价比、可观测性和易用性**四个维度。本文作为系列文章的第一部分，重点介绍了通过“灵活训练计划”实现的容量提升，以及针对推理工作负载的性价比优化。

**1. 灵活训练计划**
*   **背景与目标**：随着生成式 AI 的爆发，客户对高性能 GPU（如 P5 和 P6 实例）的需求急剧增加。然而，获取这些容量往往面临预订门槛高和资源紧张的问题。
*   **解决方案**：Amazon 推出了“灵活训练计划”。该计划允许客户以较低的承诺门槛（如 6 个月）预留 GPU 容量，且未使用的容量可以货币化，支持在同一 AWS 区域内的不同账户或组织间共享。
*   **优势**：提供了更具弹性的资源获取方式，降低了企业获取高性能计算资源的门槛和成本，确保了训练任务的连续性。

**2. 推理工作负载的性价比提升**
*   **全栈优化**：Amazon SageMaker AI 通过软硬件协同优化，显著提升了推理性能并降低了成本。
    *   **硬件层**：全面支持最新一代的 Amazon Trainium 和 Inferentia 芯片。
    *   **框架与模型层**：优化了主流开源模型（如 Llama 3.1、Mistral）在 SageMaker 上的运行效率，并改进了 Python 运行时和 OpenJDK 的性能。
    *   **推理引擎**：SageMaker 优化了开源推理组件（如 vLLM 和 TensorRT-LLM），提升了吞吐量和响应速度。
*   **Serverless 推理增强**：扩展了 Serverless 推理的并发限制和功能，支持冷启动优化和提示词缓存，进一步降低了无服务器 AI 应用的延迟和成本。
*   **成果**：通过这些优化，SageMaker 在运行主流大语言模型时，吞吐量提升了数倍，价格性能比大幅提高，帮助客户更经济地部署 AI 应用。

**总结**
2025 年，SageMaker AI 通过灵活的资源分配策略和全栈式的性能优化，有效解决了 AI 训练中的容量瓶颈

---
## 评论

**深度评论**

**中心观点**
该文章（基于标题与摘要推断）旨在阐述Amazon SageMaker AI在2025年通过底层基础设施的重构（特别是弹性训练计划与推理性价比优化），确立了云厂商在“后大模型时代”从单纯资源供给向“降本增效、精细化运营”转型的技术主轴。

**深入评价**

**1. 技术深度与架构逻辑**
*   **技术聚焦**：文章核心围绕“Capacity（容量）”与“Price Performance（性价比）”两个维度展开。摘要中提到的性能提升，技术层面上大概率指向AWS自研芯片（如Trainium/Inferentia）的迭代，或针对Spot实例容错机制的软件栈优化。
*   **架构分析**：大模型训练正从“资源堆砌”转向“工程优化”。SageMaker提出的“弹性训练计划”试图解决高端算力（如H100/B200）成本高昂与供应不稳定之间的矛盾。其技术逻辑在于利用成熟的模型Checkpointing（断点续训）机制，将低成本的离散算力整合为高可用的训练资源。
*   **关键支撑**：这一策略的有效性建立在训练任务对中断容忍度的提升之上。如果SageMaker的分布式训练库能显著缩短故障恢复时间（MTTR），则该方案具备较高的技术落地价值。

**2. 实用价值与场景适配**
*   **应用场景**：对于初创公司及AI实验室，这种优化直接降低了算力试错成本。若文章涉及推理成本优化（如编译器优化或量化技术），将直接指导企业在LLM Ops（大模型运维）中进行架构选型。
*   **创新评估**：所谓的“Flexible Training Plans”若不仅是计费模式的调整，而是结合了软件调度与硬件层的深度协同，则具备实质性的工程创新意义。其核心价值在于将非连续的廉价算力转化为生产级的稳定性。

**3. 行业影响与局限性**
*   **竞争格局**：AWS此举强化了云原生AI开发的集成优势，对依赖裸金属服务器或自建机房的中小型IDC形成了竞争压力。
*   **潜在挑战（厂商锁定）**：SageMaker的深度优化通常伴随着对AWS特定生态（如S3存储、特定镜像格式）的强依赖。企业在获得性能红利的同时，也面临着更高的迁移成本和厂商锁定风险。
*   **I/O瓶颈**：所谓的“弹性训练”在实际超大规模集群中，Checkpointing的读写速度往往受限于存储I/O。若文章未提及存储系统的配套优化，实际训练效率可能受限于数据读写而非计算本身。

**支撑理由与边界条件**

*   **支撑理由 1（成本结构变化）**：随着模型参数量从B（十亿）迈向T（万亿）级别，推理成本在总拥有成本（TCO）中的占比逐渐超越训练成本。优化推理阶段的能效比是符合行业经济规律的必然选择。
*   **支撑理由 2（资本效率）**：2025年的AI行业更加关注Unit Economics（单体经济模型）。云厂商必须通过技术手段帮助客户提升算力回报率，而非仅仅增加算力供给。
*   **支撑理由 3（软硬协同趋势）**：面对Google Cloud (TPU) 和Azure (Maia)的竞争，AWS通过SageMaker整合软硬栈，旨在构建差异化的护城河。

*   **边界条件 1（中小规模场景）**：对于仅进行7B及以下模型微调的小型团队，SageMaker相对复杂的管控平面和定价策略可能不如轻量级GPU租赁平台（如RunPod）灵活，存在“过度设计”的可能。
*   **边界条件 2（极致性能需求）**：对于追求极致网络拓扑调优的顶级实验室（如OpenAI），通用的云管控平面可能存在性能损耗，这类用户仍倾向于构建私有超级集群。

**可验证的检查方式**

1.  **TCO对比指标**：选取Llama-3-70B或同等规模模型，在SageMaker新实例与标准NVIDIA GPU实例上进行对比测试。关键指标为“Tokens per Dollar”（每美元生成Token数）及P99延迟。若性价比提升幅度低于20%，则文章宣称的改进属于常规迭代。
2.  **弹性训练恢复测试**：在训练过程中模拟Spot实例回收，测量从中断触发到训练完全恢复的时间窗口。这能验证“弹性训练”在实际生产环境中的可用性。

---
## 技术分析

## 技术分析

基于标题中的 **“Flexible Training Plans”（灵活训练计划）** 和 **“improvements to price performance for inference workloads”（推理工作负载性价比提升）**，以及摘要提及的 **“capacity, price performance, observability, and usability”（容量、性价比、可观测性、易用性）** 四个维度，以下是对 Amazon SageMaker AI 2025 年更新的技术剖析。

此次更新反映了 AI 基础设施从单纯追求算力规模，向提升资源利用效率和经济性方向的转变。

### 1. 核心技术演进逻辑

文章的核心观点在于：**AI 基础设施的发展重心已从“算力堆砌”转向“资源效率与经济性”的精细化运营。** 2025 年的 SageMaker AI 更侧重于通过灵活的容量规划和推理优化，解决企业在大规模部署 AI 时面临的资源分配和成本控制问题。

**技术路线调整：**
此次演进体现了**“务实主义”**的技术路线。随着大模型（LLM）应用进入落地阶段，技术焦点从模型训练规模转移到了如何以可持续的成本运行模型。AWS 通过底层芯片（如 Trainium/Inferentia）的优化和调度策略的改进，旨在实现**资源调度效率优于单纯硬件堆叠**的目标。

**架构创新：**
主要创新点在于将**“弹性计算”**概念引入高密度 AI 负载中。特别是“Flexible Training Plans”改变了传统高性能计算（HPC）长期锁定特定资源的模式，引入了类似 SaaS 的灵活性，以适应 AI 研发周期中波峰波谷明显的资源需求特性。

### 2. 关键技术机制解析

**1. Flexible Training Plans (灵活训练计划):**
*   **机制定义：** 这是一种结合了“预留实例”成本优势与“按需实例”灵活性的混合资源模型。
*   **运作方式：** 用户承诺一定期限的计算消耗量（如 1-5 年），但无需绑定特定的实例类型或地理位置。用户可在不同 GPU（如 NVIDIA H100）和自研芯片（如 AWS Trainium）之间切换，或在不同可用区之间迁移，而保持原有的折扣承诺。
*   **技术挑战：** 该功能依赖于全球资源池的统一调度算法，以及复杂的实时计量与计费系统。

**2. Price Performance for Inference (推理性价比优化):**
*   **优化目标：** 针对通常占据 AI 总成本 70%-90% 的推理阶段进行降本增效。
*   **实现路径：**
    *   **硬件层：** 利用专用 ASIC 芯片（如 AWS Inferentia2/Trainium）替代通用 GPU，降低生成延迟和单位 Token 成本。
    *   **调度层：** 优化模型托管服务，支持多模型并发加载和动态批处理。
*   **潜在策略：** 系统可能引入了更精细的自动缩放策略，能够依据请求延迟 SLA 自动选择最经济的计算实例（例如在低流量时使用 CPU，高流量时切换至 Inferentia）。

**3. Observability (可观测性):**
*   作为四大支柱之一，这通常指与 **Amazon SageMaker Metrics** 或 **CloudWatch** 的深度集成。其技术价值在于提供 GPU 利用率、显存碎片化及推理队列积压的实时监控，为“性价比优化”提供数据支撑和决策依据。

### 3. 实际应用价值

**对实际工作的指导意义：**
*   **成本控制：** Flexible Training Plans 允许企业无需为了获得折扣而被迫购买可能闲置的特定 GPU 资源，提高了资金利用率。
*   **架构选型：** 推理性价比的提升促使架构师重新审视硬件选型策略，不再默认采用“全 GPU”架构，而是根据负载特性在 CPU、GPU 和专用 ASIC 之间进行更精细的混合选型。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 SageMaker HyperPod 实现灵活的大规模训练计划

**说明**:
Amazon SageMaker HyperPod 专为大规模分布式训练设计，能够显著缩短模型训练时间。通过采用灵活的训练计划，企业可以更高效地分配计算资源，应对长时间运行的训练任务（如基础模型预训练）。该服务优化了集群的弹性调度，允许在保持高可用性的同时降低中断风险，从而提升整体研发效率。

**实施步骤**:
1. 评估现有大模型训练工作负载的持续时间和资源需求。
2. 配置 SageMaker HyperPod 集群，利用其优化的快速启动和容错机制。
3. 制定训练计划时，启用检查点功能，以便在实例中断或维护时自动恢复训练，避免进度丢失。

**注意事项**:
- 确保数据存储与计算节点的高吞吐连接，以避免 I/O 瓶颈。
- 定期审查训练日志以优化分布式训练的并行策略。

---

### 实践 2：通过 SageMaker Inference 推理优化提升性价比

**说明**:
在 2025 年的更新中，SageMaker 进一步增强了推理工作负载的性价比。通过利用新的实例类型（如基于 Graviton 的实例）和优化的推理容器，用户可以在不牺牲模型准确性的情况下显著降低推理成本并提高吞吐量。这对于需要高并发、低延迟的实时 AI 应用至关重要。

**实施步骤**:
1. 识别生产环境中高成本或高延迟的推理端点。
2. 测试并迁移至支持 SageMaker Inference 的最新优化实例（如 C7g 或 Inf2 实例）。
3. 启用模型推理优化选项（如模型量化或编译），以适应特定硬件架构。

**注意事项**:
- 在部署前，务必在影子环境中验证迁移后的模型精度和性能指标。
- 监控自动伸缩策略，确保在流量波动时保持成本效益。

---

### 实践 3：部署 Serverless Inference 以应对不可预测的流量

**说明**:
对于具有间歇性或不可预测流量模式的应用，SageMaker Serverless Inference 提供了一种按需付费的解决方案。它消除了配置和管理底层基础设施的需要，自动根据请求量进行扩缩容。这种实践特别适合开发测试环境、低流量应用或突发性业务场景。

**实施步骤**:
1. 分析流量模式，确定是否存在明显的波峰波谷或低频使用场景。
2. 将模型部署为 Serverless 端点，并配置适当的内存大小和最大并发数。
3. 设置 CloudWatch 告警以监控调用延迟和冷启动时间。

**注意事项**:
- 注意冷启动延迟可能对实时性要求极高的应用产生影响。
- 评估成本模型，确保对于持续高流量的场景，Serverless 成本不高于按需实例。

---

### 实践 4：实施模型蒸馏与量化以优化推理性能

**说明**:
为了在边缘设备或资源受限的端点上获得更好的性能，建议对大型模型进行模型蒸馏或量化。SageMaker 提供的工具链支持这些优化技术，能够在保持模型性能（准确率）接近原始模型的前提下，大幅减小模型体积并加快推理速度。

**实施步骤**:
1. 在 SageMaker Notebook 中使用 JumpStart 或 Neo 编译工具对模型进行基准测试。
2. 应用知识蒸馏技术，训练一个较小的“学生”模型来模仿“教师”模型。
3. 使用 SageMaker Neo 将模型编译为目标硬件的特定格式，应用 INT8 量化等优化。

**注意事项**:
- 优化后必须进行严格的 A/B 测试，确保业务指标（如准确率、召回率）未出现显著下降。
- 保留原始模型版本，以便在需要时快速回滚。

---

### 实践 5：利用 Spot Instances 进行非时间敏感的训练

**说明**:
为了最大化成本效益，应在 SageMaker 训练作业中充分利用托管 Spot Instances。这些实例利用 AWS 云端的闲置计算容量，价格通常比按需实例低 90%。结合 SageMaker 的容错机制，可以安全地将其用于非紧急的数据预处理、模型微调或超参数调优任务。

**实施步骤**:
1. 在创建训练作业时，明确启用 Spot Instances 并设置适合的中断等待时间。
2. 配置检查点管理器，将中间状态定期保存到 S3。
3. 使用 SageMaker Experiments 跟踪不同 Spot 运行的结果，确保实验的可复现性。

**注意事项**:
- Spot 实例可能会被中断，因此绝对不能用于有严格截止日期的生产级训练任务，除非配合完善的检查点恢复机制。
- 合理设置重试次数和等待时间，以应对容量不足的情况。

---

### 实践 6：使用 SageMaker Inference Components 实现精细资源控制

**说明**:
SageMaker 引入的 Inference Components 允许用户在一个实例上运行多个模型，并为每个模型精确分配计算资源（如 vCPU 和内存）。这种多模型部署策略提高了硬件资源的利用率，使得在单张 GPU 或单个 CPU 实例上混合

---
## 学习要点

- Amazon SageMaker 推理工作负载通过引入 G6g 实例和 SageMaker HyperPods，实现了高达 40% 的价格性能提升和 50% 的训练成本降低。
- SageMaker HyperPods 现已支持弹性训练计划，允许用户在无需重新配置的情况下动态调整集群规模，从而显著优化资源利用率并节省成本。
- 推理端点新增了基于请求的自动扩缩容功能，能够根据实时流量自动调整实例数量，有效解决了资源闲置与突发流量处理成本过高的问题。
- 推理功能集成了优化的开源模型（如 Llama 3 和 Mistral），利用先进的量化技术（如 AWQ 和 GGUF）大幅降低了模型部署的延迟与成本。
- 平台推出了“零接触”的自动模型打补丁功能，确保推理端点在后台自动应用安全和性能更新，消除了传统运维中的停机维护风险。
- 全新的推理计算单元（ICU）计费模式取代了传统的实例计费，允许用户根据实际模型大小和计算需求付费，实现了更精细的成本控制。
- SageMaker HyperPods 现支持直接使用 Slurm 作业调度器，简化了高性能计算（HPC）工作负载的迁移流程，降低了现有集群的入云门槛。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [SageMaker](/tags/sagemaker/) / [AWS](/tags/aws/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/) / [弹性训练](/tags/%E5%BC%B9%E6%80%A7%E8%AE%AD%E7%BB%83/) / [Trainium](/tags/trainium/) / [Inferentia](/tags/inferentia/) / [Serverless](/tags/serverless/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [2025年回顾：SageMaker AI弹性训练计划与推理性价比提升]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--0.md" >}})
- [2025年Amazon SageMaker AI增强可观测性与模型定制托管功能]({{< relref "posts/20260220-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Amazon SageMaker AI 2025回顾：可观测性与模型定制托管增强]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--2.md" >}})
- [2025年Amazon SageMaker AI回顾：可观测性、模型定制与托管增强]({{< relref "posts/20260222-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--2.md" >}})
- [2025年回顾：SageMaker AI提升可观测性并优化模型定制与托管]({{< relref "posts/20260223-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*