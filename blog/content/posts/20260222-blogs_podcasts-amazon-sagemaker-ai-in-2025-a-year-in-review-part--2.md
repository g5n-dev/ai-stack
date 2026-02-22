---
title: "2025年SageMaker AI回顾：可观测性提升与模型定制托管增强"
date: 2026-02-22T19:40:58+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "AWS", "可观测性", "模型托管", "模型定制", "CloudWatch", "生成式AI", "推理优化"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文总结了 Amazon SageMaker AI 在 2025 年发布的系列更新第二部分，主要聚焦于**可观测性**、**模型定制**以及**模型托管**三大领域的增强功能。这些改进旨在简化生成式 AI 工作负载的训练、调优和部署流程。 主要更新内容如下： **1. 增强的可观测性** 为了更好地监控和管理模型，Sa"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-2-improved-observability-and-enhanced-features-for-sagemaker-ai-model-customization-and-hosting
scenarios: ["AI/ML项目"]
---

# 2025年SageMaker AI回顾：可观测性提升与模型定制托管增强

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T20:26:30+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-2-improved-observability-and-enhanced-features-for-sagemaker-ai-model-customization-and-hosting](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-2-improved-observability-and-enhanced-features-for-sagemaker-ai-model-customization-and-hosting)

---
## 摘要/简介

2025 年，Amazon SageMaker AI 进行了多项改进，旨在帮助您训练、调优和托管生成式 AI 工作负载。在本系列的第一部分中，我们介绍了灵活的训练计划以及对推理组件所做的性价比改进。在本文中，我们将探讨在可观测性、模型定制和模型托管方面的增强功能。这些改进使得能够在 SageMaker AI 上托管全新的一类客户用例。

---
## 导语

回顾 2025 年，Amazon SageMaker AI 在可观测性、模型定制与托管领域进行了多项关键更新。这些增强功能旨在解决生成式 AI 工作负载在实际落地中的复杂性，帮助企业更精准地调优模型并优化基础设施成本。通过本文，您将深入了解 SageMaker 如何利用这些新特性支持更多样化的客户用例，从而提升模型管理的透明度与部署效率。

---
## 摘要

本文总结了 Amazon SageMaker AI 在 2025 年发布的系列更新第二部分，主要聚焦于**可观测性**、**模型定制**以及**模型托管**三大领域的增强功能。这些改进旨在简化生成式 AI 工作负载的训练、调优和部署流程。

主要更新内容如下：

**1. 增强的可观测性**
为了更好地监控和管理模型，SageMaker AI 引入了新的工具：
*   **Amazon CloudWatch 数据自动导出：** 针对 SageMaker Inference，系统现在支持自动将推理指标、日志和平台数据导出到 CloudWatch。这一功能简化了数据流向，使用户无需进行繁琐的手动设置，即可实现自动化的模型监控和故障排查。

**2. 模型定制能力的提升**
为了加速开发生成式 AI 应用，SageMaker 优化了其定制功能：
*   **推理组件的灵活训练计划：** 延续了第一部分提到的灵活性，针对推理组件进行了专门优化，使得模型调优过程更加灵活且符合成本效益。
*   **提示词词库管理：** 引入了 Prompt Management 功能，允许用户存储和管理多个版本的提示词。这有助于开发者进行 A/B 测试和快速迭代，以找到最优的模型输入。
*   **知识库检索：** 增强了与知识库的集成，使得模型在生成回复时能够更准确地引用外部数据源，提高了 RAG（检索增强生成）应用的准确性和可靠性。

**3. 模型托管与部署的增强**
在托管服务方面，SageMaker AI 引入了新功能以支持更复杂的用例：
*   **多模型/多容器支持：** 增强了托管能力，允许在同一个终端节点上更高效地部署多个模型或容器，从而提高资源利用率并降低成本。
*   **推理组件改进：** 进一步优化了推理组件的性能，使得模型在处理高并发请求时表现更稳定，延迟更低。

**总结**
2025 年 Amazon SageMaker AI 的这些更新，特别是针对可观测性自动化、提示词工程管理以及托管灵活性的改进，显著降低了生成式 AI 的落地门槛，使得客户能够更轻松地在 SageMaker 平台上构建和托管新一类的 AI 应用。

---
## 评论

**中心观点**
亚马逊在2025年对SageMaker AI的升级战略，标志着云厂商从单纯比拼“模型训练算力”向“生产级全链路工程化”的深度转型，核心在于通过可观测性增强和定制化工具链的精细化，解决大模型从实验室走向商业落地的“最后一公里”稳定性与成本控制难题。

**支撑理由与深度评价**

**1. 从“黑盒监控”向“白盒诊断”的可观测性进化**
*   **事实陈述**：文章提到SageMaker AI在2025年增强了模型可观测性功能。
*   **深度分析**：在生成式AI（GenAI）时代，传统的基于准确率的监控指标已失效。SageMaker此次升级大概率引入了针对LLM的特定指标，如Token吞吐量、首字延迟（TTFT）以及更细粒度的GPU显存碎片化监控。这不仅是功能的增加，更是运维范式的转移——从“资源是否存活”转向“模型生成质量与系统健康的双重监控”。
*   **行业价值**：这直接击中了企业用户的痛点。在RAG（检索增强生成）架构中，模型回答错误往往源于检索层而非模型本身，增强的可观测性如果能深入到Prompt和Context的监控层面，将极大提升故障排查效率。

**2. 模型定制化的“低门槛”与“高精度”平衡**
*   **事实陈述**：文章强调了SageMaker在模型定制和托管方面的增强功能。
*   **作者观点**：这里的“定制化”不仅仅指Fine-tuning（微调），更可能包含Prompt Engineering管理和持续预训练的工程化封装。2025年的趋势是将复杂的微调过程（如QLoRA参数配置）自动化，降低对算法工程师的依赖。
*   **实用价值**：对于非互联网传统行业（如金融、医疗），数据敏感且算力有限。SageMaker如果提供了更高效的定制化流水线，意味着企业可以用更少的数据和更低的算力成本，获得比通用模型更专业的垂直领域模型。

**3. 托管服务的“弹性”与“成本优化”**
*   **事实陈述**：文章提及了托管服务的改进。
*   **你的推断**：结合Part 1提到的推理组件价格性能比，Part 2的托管改进极有可能涉及“多模型共用算力”或“动态分离式部署”技术。即在一个实例上动态加载不同模型，或者根据请求量自动扩缩容推理节点。
*   **行业影响**：这种技术路线能够有效降低“模型闲置”带来的高昂成本。在当前大模型API价格战（如DeepSeek引发的低价潮）背景下，云厂商必须通过技术手段降低托管成本，才能防止客户流失到自建机房或更便宜的竞争对手。

**反例与边界条件**
尽管文章描绘了积极的技术图景，但存在以下局限性与挑战：

1.  **云厂商锁定风险**：
    *   **边界条件**：虽然SageMaker提供了无缝的定制和托管体验，但这是一种深度生态绑定。一旦企业使用了SageMaker特有的Observability SDK或专有的训练格式，未来若想迁移至Azure ML或Google Vertex AI，迁移成本将极高。
    *   **反例**：对于追求架构中立性或采用多云策略的大型企业，过度依赖这些特定增强功能可能会被视为“技术负债”。

2.  **开源工具链的竞争**：
    *   **边界条件**：SageMaker的许多功能（如实验跟踪、模型注册）在开源界有强大的替代品（如Weights & Biases, MLflow, Hugging Face TGI）。
    *   **反例**：如果SageMaker的增强功能仅仅是“追赶”了开源工具的水平，而没有提供数量级上的性能提升或易用性突破，技术团队可能会因为灵活性而选择开源方案自建，而非付费使用托管服务。

3.  **边缘侧与端侧模型的脱节**：
    *   **边界条件**：文章聚焦于云端托管。然而，2025年的趋势之一是模型的小型化和端侧化。
    *   **反例**：如果SageMaker的定制化工具仅服务于云端大模型，而无法便捷地导出模型适配到边缘设备（如手机、汽车），那么它在物联网和边缘计算领域的应用价值将大打折扣。

**验证检查方式**

为了验证文章所述改进的实际效能，建议进行以下检查：

1.  **延迟基准测试**：
    *   **指标**：在启用新的可观测性功能后，测量推理请求的P95和P99延迟。
    *   **验证点**：观察Observability Agent本身是否引入了显著的性能损耗（Sidecar模式通常会增加5%-10%的延迟）。如果延迟增加超过15%，则该功能在高并发场景下不可用。

2.  **成本效益分析实验**：
    *   **实验**：选取同一模型（如Llama-3-70B），分别使用SageMaker新的托管方式和传统的EC2自建部署方式。
    *   **观察窗口**：持续运行一个月，模拟真实的潮汐流量。
    *   **指标**：对比每百万Token的综合成本。验证“价格性能改进”是否真的比手动管理基础设施更省钱。

3.  **定制化模型精度验证**：
    *   **方法**：使用SageMaker的AutoTune功能对特定领域数据集（如法律合同）进行微调。
    *   **指标**：对比微调前后模型在特定测试集上的Rouge分数或BertScore。
    *   **验证点**：

---
## 技术分析

# Amazon SageMaker AI 2025 技术分析：生产环境下的可观测性与资源管理

## 1. 核心技术演进逻辑

### 技术重心转移
从技术发展的角度来看，2025年 SageMaker AI 的更新反映了生成式AI从实验验证向大规模生产部署的过渡。文章指出，技术重心已从单纯的模型基础能力构建，转向了**生产环境治理**与**资源利用率优化**。这标志着企业级应用对 GenAI 的要求从“能用”转变为“可控”和“经济”。

### 工程化系统视角
文章传达的核心技术思想是将大模型纳入传统的 MLOps 治理框架。这意味着 GenAI 不再是独立的黑盒系统，而是需要具备标准软件工程特征的系统组件。通过增强可观测性和托管控制，SageMaker 试图解决模型在实际业务流中缺乏透明度和资源调度僵化的问题。

### 技术价值分析
这一技术演进的重要性在于解决了企业落地的两个主要瓶颈：
1.  **可观测性缺失**：无法量化模型输出的质量和风险，导致业务不敢上线。
2.  **资源成本过高**：粗放式的 GPU 资源分配导致部署成本居高不下。

---

## 2. 关键技术特性解析

### 生成式 AI 可观测性
这是指对 LLM 应用全生命周期的监控能力，区别于传统机器学习的指标监控。

*   **LLM-as-a-Judge (自动化评估)**：
    *   **原理**：利用参数量较大、能力较强的参考模型（如 GPT-4 或 Claude 3.5），对目标模型的输出进行打分。
    *   **实现**：构建评估流水线，定义评分维度（如准确性、相关性），由 Judge 模型生成结构化反馈。
*   **Groundness Checks (真实性核查)**：
    *   **原理**：针对 RAG（检索增强生成）架构，检测模型生成的最终答案是否严格依赖于检索到的上下文，而非模型自身的训练数据幻觉。
    *   **实现**：计算生成答案与上下文片段的语义相似度或包含关系。
*   **Trace Data (链路追踪)**：
    *   **功能**：记录从 Prompt 输入、Context 检索到模型 Response 输出的完整链路数据，用于调试和性能分析。

### SageMaker Inference Components (推理组件)
这是一项针对计算资源精细化管理的技术，旨在改变以往以“实例”为单位的粗放调度模式。

*   **资源解耦与共享**：
    *   **原理**：允许将一个物理 GPU 实例的计算资源（显存、算力）切分给多个模型副本，或者将一个大型模型分布到多个实例上。
    *   **技术实现**：基于容器化技术和显存虚拟化（如 NVIDIA MIG 或类似 vLLM 的内存管理机制），使得多个推理工作负载可以在同一物理资源上共存且互不干扰。
*   **独立扩缩容**：
    *   **功能**：每个推理组件可以配置独立的副本数量和扩缩容策略，无需为了扩容某一个模型而整体扩容实例，从而提高资源利用率。

### 模型定制
*   **Fine-tuning & Distillation (微调与蒸馏)**：支持基于特定私有数据集的持续训练，以适应特定领域任务。
*   **PEFT 支持 (如 LoRA)**：支持参数高效微调，降低训练成本和存储开销，实现一个基础模型支撑多个定制化 LoRA 适配器。

---

## 3. 技术挑战与应对

### 评估指标的标准化难题
*   **难点**：LLM 输出为非结构化文本，传统的准确率/召回率指标难以直接套用，且人工评估成本高昂、标准不一。
*   **技术应对**：引入基于 RAGAS (Retrieval Augmented Generation Assessment) 框架的自动化指标，如 Faithfulness（忠实度）和 Answer Relevance（答案相关性），将非结构化评估转化为可计算的数值指标。

### 资源管理的复杂性
*   **难点**：在多模型共享资源时，如何防止“吵闹邻居”效应，即一个高负载模型挤占其他模型的资源，导致延迟抖动。
*   **技术应对**：通过推理组件级别的资源隔离和调度策略，确保不同优先级的业务流量能够获得稳定的计算资源保障。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Amazon SageMaker Inference 推理器实现模型部署的标准化与自动化

**说明**:
SageMaker Inference 推理器是 2025 年引入的重要功能，它通过标准化容器与模型资产的交互方式，简化了模型部署流程。使用推理器可以自动处理模型加载、预测前处理和后处理逻辑，无需编写自定义的推理脚本。这有助于减少代码维护负担，并确保部署环境的一致性。

**实施步骤**:
1. 确定您的模型框架（如 Hugging Face, PyTorch, TensorFlow 等）是否受 SageMaker 内置推理器支持。
2. 在创建 SageMaker 模型对象时，直接引用 `InferenceSpec` 类或使用预构建的容器 URI，而不是指向传统的 `entry_point` 脚本。
3. 将模型工件上传至 S3，并在部署时配置正确的 `ModelData` 参数。
4. 部署到终端节点并验证推理输出格式是否符合预期。

**注意事项**:
如果您的业务逻辑包含极其复杂的预处理或后处理步骤，且无法通过标准推理器实现，可能仍需使用自定义推理脚本。但在大多数情况下，应优先尝试使用推理器以降低运维复杂度。

---

### 实践 2：应用 Prompt 飞行管理和 Prompt 变体管理优化 LLM 定制

**说明**:
针对大语言模型（LLM）的定制，2025 年的最佳实践已从单纯的微调转向更灵活的 Prompt 工程。SageMaker 提供的 Prompt 飞行管理功能允许开发者创建和管理多个 Prompt 版本（变体），并通过 A/B 测试来评估哪种 Prompt 或基础模型组合在特定任务上表现最佳。这是一种低成本、高效率的模型优化手段。

**实施步骤**:
1. 在 SageMaker JumpStart 或 Studio 中定义您的任务目标，并创建多个 Prompt 模板变体。
2. 配置 Prompt 变体管理参数，设置不同的超参数或上下文示例。
3. 设置自动化评估流程，利用预定义的数据集对不同 Prompt 变体进行打分。
4. 根据评估指标选择表现最佳的 Prompt 版本用于生产环境部署。

**注意事项**:
Prompt 变体的评估数据集应具有高度的代表性，以避免“过拟合”到测试集而导致生产环境性能下降。同时，定期审查 Prompt 的有效性，因为模型更新可能会改变其对特定 Prompt 的响应。

---

### 实践 3：启用可观测性功能以实时监控模型性能与系统健康

**说明**:
2025 年的 SageMaker 更新极大地增强了模型托管的可观测性。最佳实践要求在生产环境中全面启用 Model Monitor 和数据捕获功能，以实时检测数据漂移、模型性能退化以及系统资源异常。这对于保持 LLM 和传统 ML 模型的可靠性至关重要。

**实施步骤**:
1. 在模型终端节点配置中开启 `DataCaptureConfig`，记录输入请求和输出响应。
2. 配置 SageMaker Model Monitor，设定基线约束条件，定义数据漂移和模型质量偏差的阈值。
3. 设置 CloudWatch 告警，以便在检测到异常（如延迟增加、错误率上升或 F1 分数下降）时触发通知。
4. 定期审查监控仪表盘，并利用捕获的数据重新训练或调整模型。

**注意事项**:
在捕获数据时，务必确保符合数据隐私和合规性要求（如 PII 数据脱敏），避免在生产日志中存储敏感信息。

---

### 实践 4：利用 SageMaker HyperPod 针对定制化模型进行高效预训练

**说明**:
对于需要基于专有数据进行基础模型定制或持续预训练的场景，SageMaker HyperPod 提供了优化的基础设施。最佳实践是利用 HyperPod 来加速大规模分布式训练任务，特别是在处理数十亿参数规模的模型时，它能显著缩短训练时间并降低成本。

**实施步骤**:
1. 评估现有数据集规模和模型参数量，确定是否需要使用 HyperPod 的分布式训练能力。
2. 配置 HyperPod 集群，选择合适的实例类型（如基于 Trainium 或 GPU 的实例）。
3. 利用 SageMaker 的训练编排工具设置检查点和容错机制，确保长时间训练任务的稳定性。
4. 使用 SageMaker Experiments 跟踪训练指标和超参数，以便在训练过程中进行迭代优化。

**注意事项**:
HyperPod 适用于大规模任务。对于小规模微调任务，使用标准的 SageMaker Training Jobs 或 Spot Instances 可能更具成本效益。务必根据实际工作负载选择正确的工具。

---

### 实践 5：通过多模型托管和序列化推理优化成本与延迟

**说明**:
为了提高资源利用率，2025 年的最佳实践鼓励在单个终端节点上部署多个模型（特别是多个适配器或 LoRA 模型）。SageMaker 支持在同一个 GPU 实例上动态加载和卸载模型，从而显著降低托管成本并简化架构。

**实施步骤**:
1. 将多个相关的小型模型或模型适配器（Adapters）打包并存储在 S3 中。
2. 在创建终端节点时，

---
## 学习要点

- Amazon SageMaker AI 在 2025 年显著增强了可观测性功能，通过集成 Amazon CloudWatch 和 SageMaker Metrics，实现了对模型训练、部署和推理全链路的实时监控与性能瓶颈分析。
- 推出了针对大语言模型（LLM）定制化的新功能，特别是对 NeMo 框架的支持得到了增强，使得开发者能够更高效地进行模型微调和持续预训练。
- 引入了 SageMaker Inference 的增强特性，包括对 Llama 3 等热门模型的优化支持以及多模型/多容器的部署能力，从而显著降低了推理成本并提升了部署灵活性。
- 集成了 Amazon Bedrock 与 SageMaker，允许用户利用 SageMaker 的强大托管能力来部署和微调 Bedrock 中的基础模型，打通了两大关键服务的界限。
- 发布了新的模型评估工具，旨在帮助开发者自动化评估模型质量并降低幻觉风险，这对于构建负责任的 AI 应用至关重要。
- 改进了数据标注和特征工程流程，通过 SageMaker Ground Truth Plus 等服务减少了人工标注的工作量，加速了模型定制的数据准备阶段。
- 扩展了基础设施选项，支持最新的 GPU 实例类型（如基于 NVIDIA 和 AWS 自研芯片的实例），为计算密集型的模型定制和托管任务提供了更高的性能与性价比。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-2-improved-observability-and-enhanced-features-for-sagemaker-ai-model-customization-and-hosting](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-2-improved-observability-and-enhanced-features-for-sagemaker-ai-model-customization-and-hosting)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [SageMaker](/tags/sagemaker/) / [AWS](/tags/aws/) / [可观测性](/tags/%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7/) / [模型托管](/tags/%E6%A8%A1%E5%9E%8B%E6%89%98%E7%AE%A1/) / [模型定制](/tags/%E6%A8%A1%E5%9E%8B%E5%AE%9A%E5%88%B6/) / [CloudWatch](/tags/cloudwatch/) / [生成式AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8Fai/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [2025年Amazon SageMaker AI增强可观测性与模型定制托管功能]({{< relref "posts/20260220-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Amazon SageMaker AI 2025回顾：可观测性与模型定制托管增强]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--2.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-10.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-7.md" >}})
- [2025年回顾：SageMaker AI弹性训练计划与推理性价比提升]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*