---
title: "NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt"
date: 2026-02-13T01:06:49+08:00
draft: false
entry_kind: "auto"
tags: ["NVIDIA", "Nemotron", "AWS", "SageMaker", "MoE", "模型部署", "生成式AI", "推理优化"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "NVIDIA 宣布其 Nemotron 3 Nano 30B 混合专家（MoE）模型现已在 Amazon SageMaker JumpStart 上正式推出。 该模型拥有 300 亿个参数，但在实际推理中仅激活 30 亿个参数。通过 AWS 的 SageMaker JumpStart，用户无需处理复杂的模型部署流程，即"
external_url: https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart
scenarios: ["AI/ML项目"]
---

# NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpStart

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-11T19:38:47+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)

---
## 摘要/简介

今天我们很高兴地宣布，配备 3B 活跃参数的 NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpStart 模型目录中正式全面推出。借助 Amazon Web Services (AWS) 上的 Nemotron 3 Nano，您无需处理模型部署的复杂问题，即可加速创新并带来实实在在的商业价值。利用 SageMaker JumpStart 提供的托管式部署能力，您可以将 Nemotron 的强大功能注入您的生成式 AI 应用。

---
## 导语

NVIDIA Nemotron 3 Nano 30B 混合专家模型现已在 Amazon SageMaker JumpStart 正式上线。该模型拥有 300 亿总参数，但仅需激活 30 亿参数即可运行，旨在平衡性能与成本。借助 AWS 托管式部署能力，开发者无需处理底层运维复杂度，即可快速将该模型集成至生成式 AI 应用中。本文将介绍如何利用这一方案加速开发并实现商业价值。

---
## 摘要

NVIDIA 宣布其 Nemotron 3 Nano 30B 混合专家（MoE）模型现已在 Amazon SageMaker JumpStart 上正式推出。

该模型拥有 300 亿个参数，但在实际推理中仅激活 30 亿个参数。通过 AWS 的 SageMaker JumpStart，用户无需处理复杂的模型部署流程，即可轻松利用 Nemotron 3 的能力加速生成式 AI 应用的创新，并创造商业价值。

---
## 评论

基于您提供的标题和摘要，这是一篇典型的云服务提供商与硬件巨头合作推广特定AI模型的宣发类技术文章。以下是从技术与行业角度的深入评价：

### 核心评价

这篇文章的核心观点是：**通过将NVIDIA的高效MoE架构大模型集成至AWS SageMaker，企业可以在降低算力成本的同时，利用云端的便捷性快速落地生成式AI应用。**

---

### 深度分析

#### 1. 内容深度：侧重工程落地，缺乏原理剖析
*   **事实陈述**：文章明确指出了模型的核心参数配置（30B总参数，3B激活参数）。这是典型的MoE（混合专家）架构优势，即在使用时仅激活部分参数，从而在保持大模型推理能力的同时，显著降低显存占用和推理延迟。
*   **作者观点**：文章倾向于强调“开箱即用”的便利性，但对于模型底层的训练数据来源、安全性护栏、以及具体的MoE路由机制等技术细节往往一笔带过。对于架构师而言，这种深度是不够的，因为MoE模型在微调时的不稳定性是一个已知的技术难题。
*   **你的推断**：文章暗示该模型主要针对企业级RAG（检索增强生成）或摘要任务，而非通用推理，因为Nano系列通常针对特定垂直场景进行了指令微调。

#### 2. 实用价值：降低试错门槛，但存在隐性成本
*   **支撑理由**：对于没有强大GPU集群的中型企业，SageMaker JumpStart提供了从部署到调优的一站式环境。3B的激活参数意味着相比Llama 2 70B等全参数模型，其推理成本大幅下降，适合高并发场景。
*   **边界条件/反例**：虽然推理成本降低，但MoE模型对内存带宽要求较高。如果在AWS实例选择上不当（例如使用网络带宽过低的实例），可能会导致推理速度反而不如7B/13B的稠密模型。此外，30B的总参数量意味着加载模型仍需大量显存，硬件门槛并未完全消失。

#### 3. 创新性：架构复用，渠道创新
*   **事实陈述**：Nemotron 3 Nano 30B本身并非架构创新（MoE技术已存在多年），其创新点在于“参数效率”与“特定任务优化”的平衡。
*   **作者观点**：真正的创新点在于商业模式的整合——NVIDIA提供核心资产（模型权重），AWS提供分发渠道。这种“软硬结合”的生态捆绑策略，正在重塑AI模型的分发方式，迫使开发者更深度地绑定在特定的CUDA和AWS生态上。

#### 4. 行业影响：推动“小参数激活”成为主流
*   **事实陈述**：行业正在从单纯追求“万亿参数”转向追求“每美元性能”。
*   **行业影响**：该文章的发布标志着MoE架构正在从Mistral、Mixtral等开源先锋向企业级商业化产品渗透。这将迫使其他云厂商（Google Cloud, Azure）加速引入类似的稀疏模型，否则将在性价比比拼中处于劣势。
*   **争议点**：业界对于“30B总参数/3B激活”的实际效果仍有争议。部分观点认为，在处理复杂逻辑推理任务时，MoE模型往往不如同等推理成本下的稠密模型稳定，容易产生“知识遗忘”或专家协同性差的问题。

#### 5. 实际应用建议与验证
*   **建议**：不要直接将其用于通用聊天机器人。建议将其应用于特定领域的知识提取、文档摘要或作为RAG的后端重排序器。
*   **支撑理由**：Nano系列通常针对特定任务进行了指令微调，其泛化能力可能弱于经过RLHF（人类反馈强化学习）的通用模型（如GPT-4或Llama 3）。

---

### 验证与检查方式

为了验证文章中关于“加速创新”和“业务价值”的说法是否属实，建议进行以下检查：

1.  **基准测试**：
    *   **指标**：在SageMaker上部署该模型，对比Llama-3-8B或Mistral-7B在相同数据集上的**Time-to-First-Token (TTFT)** 和 **Tokens-per-second (TPS)**。
    *   **验证逻辑**：如果30B MoE的推理速度接近7B模型且精度显著更高，则文章宣称的效率成立；否则可能存在营销夸大。

2.  **成本效益分析**：
    *   **实验**：在AWS计算器中模拟运行100万次请求的成本。
    *   **验证逻辑**：检查“3B active parameters”是否真的转化为了更低的小时费率。MoE模型往往需要更高的内存来加载所有专家，即使只激活一部分，实例成本可能并未线性下降。

3.  **微调稳定性测试**：
    *   **观察窗口**：尝试使用SageMaker的微调功能对该模型进行领域适配。
    *   **验证逻辑**：观察Loss曲线是否剧烈震荡。MoE模型在微调时容易出现灾难性遗忘，如果微调后模型性能崩塌，说明文章中“deliver business value”的前提在需要定制化的场景下难以成立。

4.  **幻觉率测试**：
    *   **指标**：使用RAG-as-a-Service框架（如NVIDIA RAG）测试模型在回答事实性问题时的准确率。
    *   **验证逻辑**：30B的参数规模决定了其知识库的截止日期和广度，需验证其是否会产生过时的幻觉。

###

---
## 技术分析

基于您提供的标题和摘要，这篇文章主要介绍了**NVIDIA Nemotron 3 Nano 30B 模型**正式入驻 **Amazon SageMaker JumpStart** 这一技术事件。尽管全文未完全给出，但基于标题中的关键技术指标（30B MoE架构、3B激活参数）和发布平台，我们可以进行深度的技术剖析与行业解读。

以下是对该文章核心观点和技术要点的深入分析：

---

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**“高效能的大语言模型（LLM）正在通过云平台实现普及化与工业化落地”**。NVIDIA Nemotron 3 Nano 30B 的发布，标志着模型架构设计从单纯追求参数量级转向追求“推理效率与性能的平衡”，并通过 AWS SageMaker JumpStart 实现了“开箱即用”的便捷性。

**核心思想：**
作者传达了**“小即是美，快即是值”**的工程哲学。在保持 300亿（30B）参数总量所带来的知识广度的同时，利用混合专家架构仅激活 30亿（3B）参数，旨在大幅降低推理成本和延迟，消除企业采用生成式 AI 的基础设施门槛。

**观点的创新性与重要性：**
*   **创新性：** 打破了“越大越好”的迷信。在当前 LLM 领域，通过稀疏激活来模拟密集模型的性能，是一种极具性价比的技术路径。
*   **重要性：** 对于企业客户而言，这是将 AI 从“玩具”转化为“生产力工具”的关键一步。高昂的 GPU 推理成本一直是阻碍企业大规模部署 AI 的主要瓶颈，该模型直接针对这一痛点。

## 2. 关键技术要点

**涉及的关键技术：**
*   **MoE (Mixture of Experts，混合专家模型)：** 这是该模型的核心架构。
*   **Active Parameters (激活参数)：** 3B active parameters 是关键指标。
*   **SageMaker JumpStart：** AWS 提供的模型即服务 平台。

**技术原理与实现：**
*   **稀疏激活：** 传统的 30B 模型在处理任何 Token 时都会加载全部 30B 参数进行计算。Nemotron 3 Nano 30B 虽然拥有 30B 的总知识库，但在处理单个输入时，只通过路由网络激活其中特定的 3B 参数。
*   **推理优化：** 这种机制意味着显存占用和计算量大幅下降。在 AWS 环境下，这意味着可以在更便宜的 GPU 实例上运行，或者获得更高的吞吐量。

**技术难点与解决方案：**
*   **难点：** MoE 模型通常对显存带宽敏感，且在分布式训练和推理中负载均衡难以控制（容易造成专家塌陷）。
*   **解决：** NVIDIA 通常利用其 Transformer Engine 和专门的通信优化库来解决 MoE 的通信瓶颈；在 JumpStart 中，AWS 和 NVIDIA 预配置了环境，解决了部署复杂的难题。

**技术创新点：**
*   **Nano 定位：** NVIDIA 将其定义为 "Nano" 系列，暗示了其针对边缘计算或低延迟场景的特殊优化，不仅仅是模型权重的压缩，更可能是架构级的精简。

## 3. 实际应用价值

**对实际工作的指导意义：**
企业 CTO 和架构师在选型时，不再需要在“巨大的模型（如 GPT-4 类）”和“微小的模型（如 7B）”之间二选一。Nemotron 3 Nano 30B 提供了一个**中间地带**：拥有接近大模型的智能，却只有小模型的成本。

**可应用场景：**
*   **实时对话系统：** 需要低延迟响应的场景。
*   **RAG (检索增强生成) 应用：** 需要模型具备较强的语言理解能力，同时控制成本。
*   **多语言任务：** Nemotron 系列通常对多语言支持较好，适合跨国企业的客服或文档分析。

**需要注意的问题：**
*   **Token 限制：** 需确认上下文窗口大小是否满足长文档处理需求。
*   **MoE 的显存瓶颈：** 虽然激活参数少，但加载整个 30B 模型仍需一定的显存（尽管可以使用 offloading 技术），需评估目标 GPU 实例的显存容量。

## 4. 行业影响分析

**对行业的启示：**
*   **模型商品化：** 基础模型正在变成像数据库一样的标准组件。NVIDIA 卖模型，AWS 卖算力，这种“软硬结合”的生态壁垒正在加固。
*   **成本结构变革：** AI 应用的边际成本将大幅下降，推动 AI 从“演示项目”走向“生产环境”。

**行业格局影响：**
*   这对开源社区（如 Llama 2 70B）构成了直接竞争。Nemotron 3 Nano 30B 如果能在 3B 激活参数下跑赢 13B 甚至 30B 的密集模型，将重新定义性价比标准。
*   加速了 MaaS (Model as a Service) 市场的细分，市场将不再按参数大小划分，而是按“每美元智能密度”划分。

## 5. 延伸思考

**引发的其他思考：**
*   **量化与剪枝的极限：** 既然 MoE 可以只激活 1/10 的参数，那么结合 4-bit 量化，是否可以在单张消费级显卡（如 RTX 4090）上运行 30B 级别的企业级模型？
*   **路由机制的黑盒：** 我们如何知道模型在处理特定任务时激活了哪个专家？这种可解释性对于金融或医疗领域至关重要。

**未来发展趋势：**
*   **动态 MoE：** 未来的模型可能会根据任务难度动态调整激活的参数量（简单问题用 1B，复杂问题用 10B）。
*   **端侧 MoE：** 这种 Nano 级别的 MoE 架构非常适合未来的 PC 端 AI（如搭载 RTX 的 AI Workstations）。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **基准测试：** 在 SageMaker JumpStart 中启动该模型，选取 50-100 条公司特有的业务数据（如客服日志），对比其与现用的 7B 或 13B 模型的表现。
2.  **成本测算：** 使用 AWS Pricing Calculator 计算 Nemotron 3 Nano 的推理成本，与现有的密集模型（如 Llama 2 70B）进行对比，重点关注“每 1000 个 Token 的成本”。

**具体行动建议：**
*   **POC 验证：** 不要直接替换生产环境。先在 SageMaker 上搭建一个沙盒环境，测试其 API 的延迟和吞吐量。
*   **Prompt 适配：** MoE 模型可能对 Prompt 的格式敏感，需要针对该模型微调 Prompt 模板。

**需补充的知识：**
*   学习如何在 SageMaker 中配置 Real-time Endpoints。
*   了解 vLLM 或 TensorRT-LLM 等推理加速引擎，因为 MoE 模型的高吞吐量极度依赖后端优化。

## 7. 案例分析

**结合实际案例说明：**
*   **成功案例（假设性）：** 某跨国电商构建智能客服助手。此前使用 13B 密集模型，响应延迟 800ms，成本高昂。切换至 Nemotron 3 Nano 30B 后，利用其 30B 的丰富知识库处理多语言咨询，由于只有 3B 激活参数，延迟降至 300ms，且因模型总参数大，对长尾问题的回答准确率提升了 15%。
*   **失败反思：** 如果企业盲目追求“大”而忽视了“微调”，直接使用 Base Model 而不进行 SFT（监督微调），可能会发现 MoE 模型在特定垂直领域的表现不如专门微调过的小模型（如 7B）。MoE 的优势在于通用知识的广度，而非单一领域的深度（除非经过微调）。

## 8. 哲学与逻辑：论证地图

**中心命题:**
> **在 AWS SageMaker 上部署 NVIDIA Nemotron 3 Nano 30B 模型，是目前企业实现高性能与低成本平衡的最佳生成式 AI 落地方案。**

**支撑理由与依据:**
1.  **理由 1 (成本效益)：** 该模型采用 MoE 架构，推理时仅激活 3B 参数。
    *   *依据：* MoE 架构原理表明计算量与激活参数成正比；AWS 按计算时间计费，计算量少即费用低。
2.  **理由 2 (性能保持)：** 总参数 30B 保证了模型的知识容量和逻辑推理能力。
    *   *依据：* 缩放定律 指出模型性能与总参数量相关；30B 通常优于 7B/13B 的模型能力上限。
3.  **理由 3 (部署便捷)：** SageMaker JumpStart 提供了预配置的基础设施。
    *   *依据：* 平台抽象化了底层 MLOps 流程，缩短了从实验到上线的时间。

**反例或边界条件:**
1.  **显存瓶颈：** 虽然激活参数少，但加载 30B 模型仍需约 60GB+ 显存（FP16），可能无法在 AWS 最小规格的实例上运行，限制了极低成本场景的适用性。
2.  **微调复杂性：** MoE 模型的微调通常比密集模型更难收敛，且需要更多显存，如果客户需要深度定制，可能会遇到技术挑战。

**事实与价值判断:**
*   *事实：* Nemotron 3 Nano 30B 拥有 3B 激活参数；SageMaker JumpStart 支持该模型。
*   *价值判断：* “最佳方案”是主观判断，取决于具体业务对延迟、成本和精度的加权。
*   *可检验预测：* 使用该模型处理特定 NLP 任务时，其推理速度应接近 3B 密集模型，而准确率接近 30B 密集模型。

**立场与验证方式:**
*   *立场：* 支持该命题，认为这是目前性价比极高的技术路径，但需警惕微调门槛。
*   *验证方式：*
    *   **指标：** 对比 Benchmark（如 MMLU, GSM8K）得分与推理延迟。
    *   **实验：** 在 AWS 上部署该模型与 Llama-2-13B chat，运行相同并发量的 RAG 请求，记录端到端延迟与每小时 AWS 账单。
    *   **观察窗口：** 持续观察 1 个月，评估模型在生产环境下的稳定性与幻觉率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：充分利用 MoE 架构进行高效推理

**说明**:
Nemotron 3 Nano 30B 采用了混合专家架构，虽然拥有 300 亿参数的总规模，但在推理过程中仅激活部分参数。这意味着在保持高性能的同时，显著降低了计算延迟和显存占用。理解这一特性对于配置推理实例至关重要。

**实施步骤**:
1. 在部署模型前，评估应用场景对延迟与吞吐量的具体需求。
2. 在 SageMaker JumpStart 中选择支持 MoE 推理优化的实例类型（如基于 NVIDIA GPU 的计算优化型实例）。
3. 配置 SageMaker 异步推理端点，以处理高并发请求，充分利用 MoE 模型的稀疏激活特性。

**注意事项**:
不要仅根据总参数量（30B）来估算资源需求，应参考活跃参数量来预估显存使用，从而优化成本。

---

### 实践 2：利用 SageMaker JumpStart 进行一键式微调

**说明**:
该模型在 JumpStart 中可用，意味着可以通过预置的脚本轻松进行微调。针对特定领域（如金融、医疗或客服）的数据进行微调，可以显著提升模型在特定任务上的表现。

**实施步骤**:
1. 准备高质量的指令微调数据集，确保数据格式符合 SageMaker JumpStart 的输入要求（通常是 JSONL 格式）。
2. 在 SageMaker Studio 中导航到 JumpStart，选择 Nemotron 3 Nano 30B 模型，并点击“Train”按钮。
3. 配置超参数（如学习率、Epoch 数），启动分布式微调作业。

**注意事项**:
微调大模型需要消耗大量计算资源。建议使用 SageMaker 的托管 Spot Training 来降低微调成本，并设置检查点以便在中断时恢复。

---

### 实践 3：优化提示词工程以适配模型特性

**说明**:
Nemotron 3 系列模型通常对特定的提示词格式响应更好。虽然这是一个 Nano 版本，但它继承了基础模型的指令遵循能力。通过精心设计的提示词，可以激发模型的最佳性能。

**实施步骤**:
1. 参考 NVIDIA 提供的官方提示词模板，构建包含系统指令、用户输入和期望输出格式的 Prompt。
2. 在推理端点上进行小批量测试，调整上下文长度和指令清晰度。
3. 实施少样本学习，在 Prompt 中提供 2-3 个具体的问答示例。

**注意事项**:
避免在输入 Prompt 中包含过多无关信息，虽然模型支持较大的上下文窗口，但精简的输入有助于提高推理速度和答案准确性。

---

### 实践 4：配置模型监控与漂移检测

**说明**:
部署模型后，持续监控其性能和预测分布对于生产环境至关重要。SageMaker Model Monitor 可以帮助检测概念漂移或数据漂移，确保模型输出质量随时间推移保持稳定。

**实施步骤**:
1. 在部署模型端点后，启用 Amazon SageMaker Model Monitor。
2. 定义基线数据，捕获模型在正常情况下的响应分布和延迟指标。
3. 设置告警阈值，当模型输出的置信度下降或响应时间异常时触发 Amazon CloudWatch 告警。

**注意事项**:
对于生成式模型，除了常规指标外，建议监控生成文本的毒性分数或幻觉率，确保输出内容的安全性和合规性。

---

### 实践 5：实施成本优化策略

**说明**:
虽然 MoE 模型在推理上比同等参数量的稠密模型更高效，但在生产环境中大规模运行仍会产生成本。通过合理的资源管理，可以在不牺牲性能的前提下控制支出。

**实施步骤**:
1. 根据实际流量模式，配置 SageMaker 自动扩缩容，设置最小和最小实例数量，在低流量期自动缩减至零。
2. 对于非实时性要求的任务（如批处理文档摘要），使用 Serverless Inference 或异步推理端点。
3. 利用 SageMaker Inference Recommender 工具，对模型进行压力测试，找出性价比最高的实例类型。

**注意事项**:
在切换实例类型前，务必进行充分的性能测试，确保所选实例的显存足以容纳 MoE 模型的专家权重。

---

### 实践 6：确保数据隐私与安全合规

**说明**:
在处理敏感数据时，利用 SageMaker 的安全功能来保护数据隐私。由于模型可能部署在多租户环境中，必须确保输入数据和模型权重的安全。

**实施步骤**:
1. 启用 VPC（虚拟私有云）端点，确保模型推理端点不直接暴露于公网。
2. 对传输中和静态的数据启用加密。
3. 利用 Amazon Bedrock 或 SageMaker 的数据脱敏功能，在将数据发送给模型前屏蔽 PII（个人身份信息）。

**注意事项**:
检查企业的数据驻留合规性要求，确保模型推理所在的区域符合当地法律法规。

---
## 学习要点

- Amazon SageMaker JumpStart 现已提供 NVIDIA Nemotron-3 Nano 30B MoE 模型，开发者可轻松访问并部署这一高性能大语言模型。
- 该模型采用混合专家（MoE）架构，通过稀疏激活机制在保持 30B 级别性能的同时显著降低推理成本与延迟。
- 用户可以利用 SageMaker JumpStart 的预置容器和配置，实现模型的一键部署，从而大幅简化机器学习工作流的集成过程。
- 该模型针对企业级生成式 AI 应用进行了优化，能够在文本生成、摘要提取及对话系统等复杂任务中提供卓越表现。
- 借助 Amazon SageMaker 的基础设施，用户可以高效地对模型进行微调（Fine-tuning），以适应特定的业务场景和数据需求。
- 此次集成体现了 NVIDIA 与亚马逊云科技的深度合作，旨在为企业客户提供更优性价比的生成式 AI 解决方案。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [NVIDIA](/tags/nvidia/) / [Nemotron](/tags/nemotron/) / [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [MoE](/tags/moe/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [生成式AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8Fai/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-10.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-7.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-0.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-4.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*