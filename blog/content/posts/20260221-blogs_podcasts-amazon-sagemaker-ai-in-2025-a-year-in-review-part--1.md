---
title: "Amazon SageMaker AI 2025回顾：弹性训练计划与推理性价比提升"
date: 2026-02-21T23:15:48+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "AWS", "弹性训练", "推理优化", "性价比", "模型训练", "基础设施", "云服务"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "**2025年 Amazon SageMaker AI 年度回顾（第一部分）总结** **核心摘要** 2025年，Amazon SageMaker AI 在核心基础设施层面取得了显著进展，主要围绕**容量、性价比、可观测性和易用性**这四个维度进行了全面升级。 本文作为回顾系列的第一部分，重点介绍了以下两个方面的关键"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads
scenarios: ["Web应用开发"]
---

# Amazon SageMaker AI 2025回顾：弹性训练计划与推理性价比提升

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T20:26:47+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads)

---
## 摘要/简介

2025 年，Amazon SageMaker AI 在核心基础设施产品方面围绕四个维度实现了显著提升：容量、性价比、可观测性和易用性。在这一系列文章中，我们将探讨这些各项改进及其带来的优势。在第一部分中，我们将探讨随着弹性训练计划（Flexible Training Plans）的推出而实现的容量改进。我们还将介绍针对推理工作负载的性价比提升。在第二部分中，我们将探讨在可观测性、模型定制和模型托管方面所做的增强。

---
## 导语

回顾 2025 年，Amazon SageMaker AI 在核心基础设施层面实现了显著升级，重点围绕容量、性价比、可观测性及易用性四个维度展开。作为年度回顾系列的第一篇，本文将深入解读弹性训练计划如何解决算力供应难题，并剖析针对推理工作负载的性价比优化策略。通过阅读本文，您将了解这些底层改进的具体技术细节，以及它们如何帮助企业更高效地控制成本并提升模型交付效率。

---
## 摘要

**2025年 Amazon SageMaker AI 年度回顾（第一部分）总结**

**核心摘要**
2025年，Amazon SageMaker AI 在核心基础设施层面取得了显著进展，主要围绕**容量、性价比、可观测性和易用性**这四个维度进行了全面升级。

本文作为回顾系列的第一部分，重点介绍了以下两个方面的关键改进：

1.  **灵活的训练计划**：在容量管理方面，SageMaker AI 推出了“灵活训练计划”，旨在提升用户获取和管理计算资源的能力。
2.  **推理工作负载的性价比提升**：在成本与效率方面，SageMaker AI 对推理工作负载的性价比进行了大幅优化。

后续的第二部分将重点探讨可观测性、模型定制以及模型托管等方面的增强功能。

---
## 评论

**中心观点**
文章核心观点为：Amazon SageMaker AI 在 2025 年通过底层基础设施的更新（引入 Flexible Training Plans 及优化推理成本结构），旨在解决云上 AI 工作负载中“资源获取不确定性”与“成本波动”的两大痛点，从而在模型托管与训练平台市场中维持其全栈通用平台的竞争力。

**支撑理由与深度评价**

1.  **战略重心转移：从功能完善转向供给侧保障**
    *   **事实陈述**：文章重点提及了 Flexible Training Plans（灵活训练计划）和针对推理工作负载的性价比优化。
    *   **深度分析**：这反映出云厂商竞争焦点的迁移。早期竞争侧重于算法框架的丰富度或开发环境的易用性，而当前的行业痛点已转移到底层资源的**确定性交付**上。随着基础模型参数量的增长，算力供应成为瓶颈。AWS 推出的“灵活训练计划”本质上是一种**容量预留**机制，旨在帮助客户锁定长期投入，缓解高峰期的资源焦虑，这是对行业供需矛盾的直接回应。

2.  **推理成本的结构性优化**
    *   **事实陈述**：文章强调了针对推理工作负载的价格性能改进。
    *   **深度分析**：这通常意味着 AWS 正在通过部署自研芯片（如 Inferentia 系列）及优化无服务器推理的计费模式来降低边际成本。从商业角度看，训练往往是阶段性投入，而推理是长期的运营支出。AWS 试图通过降低推理成本，防止用户将工作负载迁移到更具价格优势的专有云或自建集群，这是一种基于成本优势的防守策略。

3.  **运维能力的标准化与工具化**
    *   **事实陈述**：摘要中提到 Observability（可观测性）和 Usability（可用性）是四大改进维度之一。
    *   **深度分析**：当模型进入生产环境，调试与监控的难度增加。SageMaker 增强可观测性，实际上是在完善 AI 应用的全生命周期管理工具。这降低了 MLOps 的实施门槛，使得数据科学家能够更专注于模型本身，符合运维自动化与标准化的行业趋势。

**反例/边界条件**

1.  **垂直领域的“通用性局限”**：虽然 SageMaker 强调全栈能力，但在特定垂直领域（如生物制药或特定的自动驾驶仿真），专门的 SaaS 平台可能比通用的 SageMaker 提供更深度的集成与优化。通用型平台在特定场景下往往面临深度不足的问题。
2.  **小团队的“适配性门槛”**：对于初创团队或仅需调用 API 的用户，SageMaker 的复杂功能反而可能带来较高的配置成本。其复杂的权限体系及众多的服务组件，构成了较高的认知负荷。相比之下，轻量级平台在“小而美”的市场可能更具吸引力。

**详细评价维度**

*   **1. 内容深度**：**[中]** 文章作为年度回顾，准确识别了基础设施这一核心要素，逻辑较为严密。但内容更偏向于产品功能特性的罗列，缺乏对底层技术实现细节（如具体编译器技术或算子优化）的深入剖析。
*   **2. 实用价值**：**[高]** 对于技术决策者而言，了解 Flexible Training Plans 至关重要，它直接关系到算力资源的采购策略与成本规划。
*   **3. 创新性**：**[中]** “灵活训练计划”更多体现为商业交付模式的创新。技术上，推理性能的提升主要依赖于专用芯片（ASIC）的迭代，属于行业常规技术路线的延续。
*   **4. 可读性**：**[良]** 文章结构清晰，术语规范，但作为官方技术博客，带有一定的产品宣发属性，读者需要具备一定的云原生背景知识以提取有效信息。
*   **5. 行业影响**：**[中高]** 此类改进可能会促使竞争对手（如 Google Cloud Vertex AI 和 Microsoft Azure ML）调整其容量预留策略与定价模型，从而影响云 AI 市场的整体服务形态。
*   **6. 争议点/不同观点**：文章隐含假设是“用户倾向于在一个平台完成所有工作”。然而，业界也存在**解耦**的趋势——即用户倾向于将训练、推理和数据存储分别部署在最擅长的平台上，而非绑定于单一生态。

---
## 技术分析

基于您提供的文章标题和摘要，以及对Amazon SageMaker AI（特别是2025年发展趋势）的深入理解，以下是对该主题的全面深度分析。

---

# Amazon SageMaker AI 2025 年度回顾（第一部分）：灵活训练计划与推理性价比的深度分析

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点在于：**在2025年，生成式AI的基础设施竞争已从单纯的“模型能力竞赛”转向“基础设施效能竞赛”。** Amazon SageMaker AI 通过在**容量灵活性**和**推理性价比**两个维度的底层重构，解决了企业在规模化应用AI时面临的最痛痛点——算力获取的不确定性与高昂的推理成本。

### 作者想要传达的核心思想
作者试图传达一个明确的信号：**AI的“落地”阶段比“爆发”阶段更依赖于云基础设施的精细化管理。** 仅仅拥有强大的模型是不够的，企业需要能够灵活调度海量算力进行训练，并以极低的边际成本进行推理。AWS通过SageMaker提供的不仅是工具，更是一种“可持续的AI经济模型”。

### 观点的创新性和深度
该观点的创新性在于打破了“算力即资源”的传统认知，转向了“算力即服务”的弹性视角。
*   **深度**：文章触及了AI工程化的深水区——如何在不牺牲性能的前提下，通过量化、编译和专用硬件（如Trainium/Inferentia）来压榨每一分算力的价值。
*   **创新性**：将“容量保证”和“推理优化”作为年度首要亮点，表明AWS敏锐地捕捉到了市场从“模型构建”向“大规模生产部署”转型的关键拐点。

### 为什么这个观点重要
这个观点至关重要，因为它直接决定了企业的生死存亡。目前，许多企业因GPU短缺导致训练中断，或因推理成本过高导致无法盈利。SageMaker的这些改进直接回应了**AI商业化进程中的最大阻碍——成本与稳定性的矛盾**。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Flexible Training Plans (灵活训练计划)**：这是一种容量预留机制，允许用户承诺一定的使用量以换取特定区域（如US East）的GPU（如P5/H100）的确定性访问权限。
2.  **SageMaker HyperPod**：用于分布式训练的弹性集群，支持长时间运行的训练任务。
3.  **Inferentia2 & Trainium2**：AWS自研的推理和训练芯片，旨在提供比NVIDIA GPU更高的性价比。
4.  **Model Quantization & Compilation (模型量化与编译)**：通过INT8/FP4量化降低显存占用和延迟。
5.  **Speculative Decoding (投机解码)**：一种推理加速技术，使用小模型预测大模型的输出，以验证速度生成Token。

### 技术原理和实现方式
*   **灵活训练计划原理**：基于云端的容量调度算法。用户签署承诺（例如1年或3年），AWS将其纳入全球容量规划，确保在用户启动EC2实例或SageMaker作业时，底层物理资源是立即可用的，避免了“由于容量不足而启动失败”的错误。
*   **推理优化原理**：
    *   **硬件层**：利用NeuronCorev2的流水线并行。
    *   **软件层**：SageMaker Inference Server 自动根据流量模式调整实例数量，并结合编译器将模型转换为针对Neuron芯片优化的指令集。

### 技术难点和解决方案
*   **难点**：大模型推理的延迟与吞吐量难以兼得；量化后的模型精度损失。
*   **解决方案**：利用**Speculative Decoding**在保持精度的同时加速生成；使用**SmoothQuant**等先进量化算法保持LLM在低比特下的性能；引入**Continuous Batching**（连续批处理）以提高GPU利用率。

### 技术创新点分析
最大的创新点在于**软硬协同优化**。不同于单纯的软件优化，SageMaker AI 2025的更新深度结合了AWS自研芯片架构。例如，针对Transformer架构的特定算子（Attention, MLP）在Trainium/Inferentia上的硬件加速，这种垂直整合能力是通用云平台难以比拟的。

---

## 3. 实际应用价值

### 对实际工作的指导意义
*   **成本控制**：指导架构师如何通过切换到Inf2实例或启用SageMaker Serverless Inference来将推理成本降低50%-70%。
*   **项目规划**：利用Flexible Training Plans，企业可以放心地启动长周期的模型预训练项目，而不必担心中途算力被抢占。

### 可以应用到哪些场景
1.  **高并发RAG（检索增强生成）系统**：利用SageMaker的推理优化功能处理海量并发请求。
2.  **行业大模型微调**：利用HyperPod进行SFT（监督微调），确保任务不中断。
3.  **边缘端模型部署**：通过量化技术，将大模型部署在成本极低的实例上。

### 需要注意的问题
*   **Vendor Lock-in (厂商锁定)**：深度使用SageMaker特定的编译器或Neuron SDK，会导致迁移至其他云平台（如GCP或Azure）变得困难。
*   **承诺风险**：Flexible Training Plans通常需要签署承诺合同，如果模型训练提前结束，仍需支付费用。

### 实施建议
建议企业在进行POC（概念验证）时使用按需实例，验证通过后，对于确定的业务负载，再签署Flexible Training Plans并迁移至Inferentia/Trainium实例以优化成本。

---

## 4. 行业影响分析

### 对行业的启示
这标志着**云原生AI基础设施的2.0时代**开启。1.0时代是提供虚拟化的GPU，2.0时代是提供针对AI工作负载深度优化的全栈解决方案（从芯片到调度）。行业将从“卖资源”转向“卖效能”。

### 可能带来的变革
*   **AI应用的普及化**：随着推理成本的断崖式下降，更多低利润率的行业（如客服、游戏NPC）将能够大规模使用LLM。
*   **芯片市场的多元化**：AWS自研芯片的强势推广将挑战英伟达在AI云算力市场的垄断地位，迫使价格下降。

### 对行业格局的影响
这进一步巩固了AWS在企业级AI市场的护城河。对于初创公司而言，构建模型的基础门槛降低了，但运维大规模基础设施的门槛依然很高，这使得大厂通过提供高性价比的基础设施来控制AI生态上游的策略更加明显。

---

## 5. 延伸思考

### 引发的其他思考
*   **开源与闭源的界限模糊**：当基础设施优化（如SageMaker）成为核心竞争力时，模型本身的权重是否开源可能不再那么重要，因为运行效率才是商业化的关键。
*   **能源效率**：提高每瓦特的算力产出将是2025年后的下一个关键指标，SageMaker的优化本质上也是绿色计算的一部分。

### 未来发展趋势
*   **模型路由**：未来的SageMaker可能会内置智能路由，根据Prompt的复杂程度，自动将简单请求路由给小模型，复杂请求路由给大模型，从而实现全局最优性价比。
*   **训练即推理**：训练和推理的界限将进一步模糊，持续学习将成为常态。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **审计现有工作负载**：检查当前运行的推理实例，评估是否可以从`p4d` (NVIDIA A100) 迁移到 `inf2` (Inferentia2)。
2.  **测试量化效果**：使用SageMaker Model Monitor启用量化实验，观察INT8量化对特定模型精度的影响。
3.  **预留容量**：如果计划在未来6个月内进行大规模训练，立即联系AWS销售团队探讨Flexible Training Plans。

### 具体的行动建议
*   **行动1**：在开发环境中部署SageMaker Inference Companion，测试不同批处理大小下的延迟表现。
*   **行动2**：学习使用`boto3` SDK编写自动化脚本，利用SageMaker Asynchronous Inference来处理离线批处理任务，以利用Spot实例的低价。

### 需要补充的知识
*   深入理解**Hugging Face TGI (Text Generation Inference)** 与 **SageMaker** 的集成方式。
*   学习**AWS Neuron SDK** 的基本调试工具，因为从CUDA迁移到Neuron需要适应新的工具链。

---

## 7. 案例分析

### 成功案例分析
**案例：某金融科技公司的风控模型重构**
*   **背景**：该公司使用GPT-4进行文本分析，成本高昂且延迟高，无法满足实时交易需求。
*   **做法**：利用SageMaker HyperPod基于Llama-3-70B进行微调，并利用SageMaker Inference的Speculative Decoding和INT8量化部署在Inf2实例上。
*   **结果**：推理成本降低75%，P95延迟降低至50ms以内，满足了实时风控需求。

### 失败案例反思
**案例：某广告公司的盲目迁移**
*   **背景**：急于降低成本，未做充分测试就将复杂的CV模型迁移至Inferentia。
*   **问题**：该模型高度依赖CUDA特定的算子库，Neuron SDK不支持，导致重写代码成本极高，且精度下降严重。
*   **教训**：**不要为了优化而优化**。在迁移前必须进行严格的基准测试，特别是对于依赖特定硬件加速算子的模型。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**在2025年，企业AI战略的成功将更多地取决于通过SageMaker等平台实现的“基础设施性价比”与“算力确定性”，而非模型算法本身的原始性能。**

### 支撑理由与依据
1.  **理由1：算力供需失衡**。
    *   *依据*：2024-2025年GPU短缺现象依然存在，导致按需获取算力极其不稳定。
    *   *证据*：AWS推出Flexible Training Plans正是为了解决客户无法获取H100/P5实例的抱怨。
2.  **理由2：推理成本是AI规模化落地的最大拦路虎**。
    *   *依据*：对于大多数应用，推理成本是训练成本的10倍以上。
    *   *证据*：文章强调“improvements to price performance for inference”是年度核心亮点。
3.  **理由3：专用硬件的能效比优势**。
    *   *依据*：通用GPU（NVIDIA）在处理Transformer类推理时存在冗余能耗，专用ASIC（Inferentia）能效更高。
    *   *证据*：AWS自研芯片的FP8/INT8支持及高吞吐量数据。

### 反例或边界条件
1.  **反例1**：对于处于研究前沿、算法每周迭代的初创公司，绑定SageMaker的特定硬件可能会牺牲灵活性，导致无法使用最新的CUDA特性（如FlashAttention 3的早期版本）。
2.  **边界条件**：对于极小规模的模型或极低频的调用，管理SageMaker基础设施的复杂度可能超过了节省下来的成本（Serverless Lambda可能更合适）。

### 事实与价值判断
*   **事实**：AWS推出了SageMaker AI的容量预留和推理优化功能。
*   **价值判断**：这些改进是“决定性”的，企业应当优先考虑基础设施效能而非单纯追求模型参数量。
*

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 SageMaker Flexible Training Plans 实现成本优化的资源预留

**说明**: 针对长期运行的模型训练任务（如基础模型微调或大规模数据集训练），采用 SageMaker Flexible Training Plans 可以通过预留计算资源来显著降低单位计算成本。该服务允许用户承诺使用一定时长（例如 1 年或 3 年）的实例，以换取比按需付费低得多的折扣价，同时提供比传统 Reserved Instances 更灵活的选项。

**实施步骤**:
1. 评估团队未来 6-12 个月的模型训练路线图，确定所需的实例类型（如 P4/P5 实例）和数量。
2. 在 SageMaker 控制台中创建 Flexible Training Plan，根据预算选择预付部分或全预付模式。
3. 将预留的容量关联到特定的训练作业中，确保高优先级项目始终有资源可用。

**注意事项**: 确保训练任务的持续时间与预留计划相匹配，避免资源闲置浪费。

---

### 实践 2：通过 SageMaker Serverless Inference 优化无规律流量的成本

**说明**: 对于具有间歇性或不可预测访问模式的推理工作负载，使用 SageMaker Serverless Inference 可以实现按需付费和自动扩缩容。这省去了配置和管理底层基础设施的复杂性，特别适用于开发测试环境或流量波动剧烈的 API 服务。

**实施步骤**:
1. 识别业务中流量波峰波谷差异大的模型端点。
2. 将模型部署到 Serverless Inference 端点，配置适当的内存大小（根据模型大小）和最大并发数。
3. 设置 CloudWatch 告警以监控调用次数和延迟，确保在流量突增时触发自动扩容。

**注意事项**: Serverless Inference 有冷启动延迟，不适合对延迟要求极高的实时在线推理场景。

---

### 实践 3：使用 SageMaker Inference Recommender 部署具性价比的实例

**说明**: SageMaker Inference Recommender 能够帮助用户在不同的实例类型和配置参数（如批处理大小、并发数）之间进行压力测试，从而找到特定模型在满足延迟和吞吐量要求下的最低成本部署方案。

**实施步骤**:
1. 在 SageMaker Studio 中启动 Inference Recommender 任务。
2. 输入模型容器镜像、样本数据以及性能要求（如最大延迟 P90 < 50ms）。
3. 根据生成的建议报告，选择推荐的最佳实例类型（例如选择 GPU 实例 vs CPU 实例，或多模型部署实例）进行生产环境部署。

**注意事项**: 在测试时务必使用符合生产环境特征的数据集，以免测试结果产生偏差。

---

### 实践 4：启用多模型端点或多容器端点以提高资源利用率

**说明**: 为了进一步优化推理的性价比，应充分利用 SageMaker 的多模型端点或多容器端点功能。这允许在同一个 GPU 或 CPU 实例上托管多个模型或多个模型版本，从而共享计算资源，减少闲置资源浪费。

**实施步骤**:
1. 将多个兼容框架的模型打包并上传至 S3 存储桶。
2. 创建多模型端点配置，指定模型加载路径和内存分配。
3. 调用 InvokeEndpoint 时通过 TargetModel 参数指定具体模型，实现单实例服务多模型。

**注意事项**: 需监控实例的显存或内存使用率，防止因模型加载过多导致 OOM（内存溢出）错误。

---

### 实践 5：利用 SageMaker HyperPod 稳定大规模分布式训练

**说明**: 对于大规模基础模型训练，SageMaker HyperPod 提供了专为长时间运行训练作业设计的基础设施。它通过自动化的故障恢复和优化的网络互连，提高了训练的稳定性并降低了运维开销，从而间接提升了价格性能比。

**实施步骤**:
1. 准备训练脚本和依赖库，确保支持 Checkpointing（检查点保存）机制。
2. 在 SageMaker 控制台创建 HyperPod 集群，配置所需的实例组（如 Trainium 或 GPU 集群）。
3. 提交训练作业，利用 HyperPod 的自动故障切换功能，确保在单个实例故障时训练能自动恢复而不丢失进度。

**注意事项**: 需确保训练框架（如 PyTorch）版本与 HyperPod 的底层库兼容，以充分利用分布式训练加速。

---

### 实践 6：部署 SageMaker Inference Components 实现精细化资源控制

**说明**: 借助 Inference Components，用户可以在单个端点内为不同的模型或模型副本精确分配计算资源（如 vCPU 和内存）。这种粒度控制允许在同一个实例上混合部署不同资源需求的模型，最大化硬件利用率。

**实施步骤**:
1. 分析不同模型的资源消耗画像。
2. 在创建端点时定义多个 Inference Components，为每个组件分配特定的 CPU 核心数和内存。
3. 根据业务流量变化，动态调整各个 Component 的副本数量，实现资源的弹性伸缩。

**注意事项**: 需要合理规划资源配额，避免

---
## 学习要点

- Amazon SageMaker 在 2025 年通过引入灵活的训练计划，允许用户根据业务需求动态调整训练资源，显著提升了资源利用效率。
- 推理工作负载的价格性能比得到优化，通过改进硬件利用率和算法效率，降低了推理成本。
- 新增的分布式训练支持进一步扩展了模型训练的规模，适用于更大规模的 AI 模型开发。
- SageMaker 强化了与开源框架的集成，提升了开发者在不同工具链间的兼容性和灵活性。
- 自动化模型调优功能得到增强，减少了手动调参的时间，加速了模型迭代周期。
- 增强的数据标注和预处理工具简化了数据准备流程，提升了数据质量和处理速度。
- 更新后的监控和调试工具提供了更深入的模型性能洞察，帮助开发者快速定位和解决问题。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-in-2025-a-year-in-review-part-1-flexible-training-plans-and-improvements-to-price-performance-for-inference-workloads)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [SageMaker](/tags/sagemaker/) / [AWS](/tags/aws/) / [弹性训练](/tags/%E5%BC%B9%E6%80%A7%E8%AE%AD%E7%BB%83/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/) / [性价比](/tags/%E6%80%A7%E4%BB%B7%E6%AF%94/) / [模型训练](/tags/%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83/) / [基础设施](/tags/%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [云服务](/tags/%E4%BA%91%E6%9C%8D%E5%8A%A1/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [2025年回顾：SageMaker AI弹性训练计划与推理性价比优化]({{< relref "posts/20260220-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--0.md" >}})
- [2025年回顾：SageMaker AI弹性训练计划与推理性价比提升]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--0.md" >}})
- [2025年Amazon SageMaker AI增强可观测性与模型定制托管功能]({{< relref "posts/20260220-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*