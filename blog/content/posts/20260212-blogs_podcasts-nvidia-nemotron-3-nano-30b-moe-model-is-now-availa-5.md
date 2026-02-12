---
title: "NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta"
date: 2026-02-12T15:02:46+08:00
draft: false
entry_kind: "auto"
tags: ["NVIDIA", "Nemotron", "AWS", "SageMaker", "MoE", "LLM", "模型部署", "生成式AI"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "以下是对该内容的中文简洁总结： **NVIDIA Nemotron 3 Nano 30B 模型现已登陆 Amazon SageMaker JumpStart** 今日，NVIDIA 宣布 **NVIDIA Nemotron 3 Nano 30B** 模型在 **Amazon SageMaker JumpStart**"
external_url: https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart
scenarios: ["大语言模型", "AI/ML项目"]
---

# NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpStart 上线

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-11T19:38:47+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)

---
## 摘要/简介

今天我们很高兴地宣布，配备 3B 激活参数的 NVIDIA Nemotron 3 Nano 30B 模型现已登陆 Amazon SageMaker JumpStart 模型目录，正式向公众开放。您可以在 Amazon Web Services (AWS) 上借助 Nemotron 3 Nano 加速创新并创造切实的业务价值，而无需应对模型部署的复杂性。借助 SageMaker JumpStart 提供的托管部署功能，您可以将 Nemotron 的能力融入您的生成式 AI 应用，为其提供强大动力。

---
## 导语

NVIDIA Nemotron 3 Nano 30B 模型现已登陆 Amazon SageMaker JumpStart，这是一款具备 30B 总参数量但仅需激活 3B 参数的混合专家模型。它在保持高性能的同时显著降低了计算成本，非常适合在资源受限的环境中构建生成式 AI 应用。本文将介绍如何利用 SageMaker 的托管部署功能快速集成该模型，帮助您在 AWS 上简化运维流程并加速业务创新。

---
## 摘要

以下是对该内容的中文简洁总结：

**NVIDIA Nemotron 3 Nano 30B 模型现已登陆 Amazon SageMaker JumpStart**

今日，NVIDIA 宣布 **NVIDIA Nemotron 3 Nano 30B** 模型在 **Amazon SageMaker JumpStart** 模型库中正式全面可用。

该模型采用混合专家（MoE）架构，拥有 **300 亿参数**，但每次推理仅激活 **30 亿参数**。

**主要优势：**
1.  **简化部署与管理：** 用户无需处理复杂的模型部署流程，即可在 AWS 云平台上快速使用该模型。
2.  **加速业务创新：** 通过利用 Nemotron 模型的生成式 AI 能力，企业可以加速开发进程并创造实际的商业价值。
3.  **托管服务：** 借助 SageMaker JumpStart 的托管部署功能，用户可以更轻松地为生成式 AI 应用程序提供强大支持。

---
## 评论

**中心观点**
这篇文章标志着云服务巨头与AI芯片霸主在“高效能大模型”落地层面的深度整合，旨在通过软硬协同（NVIDIA架构+AWS基础设施）降低企业部署生成式AI的算力门槛，但本质上仍是对现有MoE（混合专家）技术栈的工程化封装，而非算法层面的根本性突破。

**支撑理由与边界分析**

**1. 稀疏激活的工程化落地：从“暴力美学”到“精准手术”**
*   **事实陈述**：Nemotron 3 Nano 30B 采用了30B的总参数量，但在推理过程中仅激活3B参数。这是一种典型的混合专家模型架构。
*   **深度分析**：文章的核心价值在于将MoE架构进行了“云原生化”。对于行业而言，这解决了一个关键痛点：大模型的高昂推理成本。通过在AWS SageMaker JumpStart中提供此模型，企业无需自建复杂的MoE路由系统，即可获得接近30B模型智能水平，但仅需支付3B模型计算成本的体验。这是将学术界的MoE理论转化为商业生产力的典型案例。
*   **反例/边界条件**：MoE架构并非银弹。在显存受限的边缘设备上，加载30B的模型权重（即使只激活3B）仍然对显存（VRAM）有较高要求。对于极低延迟需求的场景，MoE模型在专家路由切换时产生的通信延迟可能会抵消掉计算量减少带来的优势。

**2. 生态锁定与“软硬解耦”的悖论**
*   **作者观点**：文章极力渲染“开箱即用”的便捷性，但这背后是NVIDIA与AWS构建的深度护城河。
*   **深度分析**：从行业角度看，这是一种典型的生态捆绑策略。Nemotron模型针对NVIDIA GPU（如AWS上的实例）进行了底层算子优化。这种优化虽然能带来极致的性能，但也增加了用户的迁移成本。企业一旦基于此模型开发业务逻辑，未来若想迁移至非NVIDIA硬件（如AMD、AWS自研芯片或TPU），将面临显著的兼容性挑战。
*   **反例/边界条件**：如果开源社区（如Llama 3或Mistral）推出了同等量级的MoE模型，并且性能接近Nemotron，那么企业可能会放弃这种半商业化的封闭生态，转而拥抱更灵活的开源方案，因为开源方案通常拥有更广泛的社区支持和更少的供应商锁定风险。

**3. “通用可用”与“垂直落地”的鸿沟**
*   **事实陈述**：文章提到模型可用于“加速创新和交付商业价值”。
*   **你的推断**：虽然Nemotron 3 Nano可能在通用基准测试上表现优异，但在具体的垂直行业（如医疗、法律、金融）中，直接使用该预训练模型的效果可能有限。
*   **深度分析**：文章的实用价值在于其作为“基座模型”的潜力。对于拥有私有数据的AWS客户，利用SageMaker的微调能力对这30B参数进行指令微调，是比直接使用API更具有数据隐私保障和定制化潜力的路径。这反映了行业从“拼参数量”向“拼垂直适配度”的转变。
*   **反例/边界条件**：对于知识密集型任务，较小的活跃参数（3B active）可能存在“知识容量瓶颈”。相比激活全部参数的稠密模型，稀疏模型在处理需要调用大量隐性知识的复杂推理任务时，可能会出现幻觉或知识召回不足的情况。

**评价维度总结**

*   **内容深度**：文章作为技术公告，深度适中。它清晰地解释了模型特性（30B/3B）和部署路径，但未深入探讨模型训练数据的合规性、具体的对齐算法或路由机制。
*   **实用价值**：极高。对于已经在AWS生态内的开发者，这提供了一条低成本试水高性能大模型的捷径。
*   **创新性**：中等。MoE并非新技术，但在公有云平台上以“一键部署”的形式提供高性能MoE，属于工程创新。
*   **可读性**：结构清晰，技术指标明确，目标用户定位精准。
*   **行业影响**：加剧了云厂商在AI模型层的竞争。AWS与NVIDIA的这种深度绑定，可能会挤压其他小型模型提供商的生存空间。

**可验证的检查方式**

1.  **性能基准对比实验**：
    *   **指标**：在MMLU、GSM8K等基准测试中，对比Nemotron 3 Nano 30B (3B active) 与 稠密模型（如Llama-3-8B或Mistral-7B）的得分与推理延迟。
    *   **验证点**：验证在同等计算资源下，MoE架构是否真正实现了“吞吐量x性能”的最优解。

2.  **端到端延迟与吞吐量测试**：
    *   **实验**：在AWS SageMaker上使用相同的GPU实例（如g5.xlarge），分别运行Nemotron 3 Nano和一个7B的稠密模型。
    *   **验证点**：观察Token生成的首字延迟（TTFT）和吞吐量。如果MoE模型的通信开销过大，其延迟可能高于预期。

3.  **微调后的灾难性遗忘观察**：
    *   **指标**：对模型进行垂直领域（如客服对话）的全量微调（Full Fine-tuning）或LoRA微调。
    *   **验证点**：观察微调后模型在通用任务上的表现是否大幅下降（灾难

---
## 技术分析

基于您提供的文章标题和摘要，以下是对 **NVIDIA Nemotron 3 Nano 30B 模型在 Amazon SageMaker JumpStart 上线** 这一事件的深度分析。

---

# 深度分析：NVIDIA Nemotron 3 Nano 30B 与 AWS SageMaker 的结合

## 1. 核心观点深度解读

**主要观点**
文章的核心观点是宣布 **NVIDIA Nemotron 3 Nano 30B** 模型正式入驻 **Amazon SageMaker JumpStart**。这标志着企业用户现在可以在 AWS 云平台上，通过极简的部署流程，使用到一个具备“大模型逻辑能力”但仅消耗“小模型资源”的高效生成式 AI 模型。

**核心思想**
作者（NVIDIA 与 AWS 技术团队）想要传达的核心思想是 **“效率与可及性的民主化”**。
*   **效率：** 通过 **Mixture of Experts (MoE)** 架构，实现了 30B 参数级别的智能，但在推理时仅激活 3B 参数。这意味着用户无需为庞大的参数量支付全额计算成本，却能获得高质量的生成结果。
*   **可及性：** 借助 SageMaker JumpStart，开发者无需从零开始构建基础设施或处理复杂的模型兼容性问题，即可将这一先进技术集成到实际业务中。

**创新性与深度**
*   **架构创新：** 传统的稠密模型在推理时需要激活所有参数。Nemotron 3 Nano 30B 采用稀疏 MoE 架构，将模型规模与计算成本解耦。这是一种在“云端推理”场景下极具深度的优化策略，旨在解决大模型落地昂贵的关键痛点。
*   **平台深度：** 将 NVIDIA 优化的模型无缝集成到 AWS 的生态系统中，体现了软硬协同的深度。

**重要性**
这一观点之所以重要，是因为它击中了当前生成式 AI 落地的最大阻碍——**性价比（ROI）**。许多企业因为大模型微调和推理的高昂成本而犹豫不决。Nemotron 3 Nano 30B 提供了一条“低成本、高性能”的中间路径，特别适合资源有限但追求高质量的企业级应用。

---

## 2. 关键技术要点

**涉及的关键技术**
1.  **Mixture of Experts (MoE, 混合专家模型)：** 这是 Nemotron 3 Nano 的核心架构。
2.  **Active Parameters (激活参数)：** 模型总共有 300 亿参数，但在处理任何特定输入 token 时，只有 30 亿参数被激活。
3.  **Amazon SageMaker JumpStart：** AWS 提供的机器学习即服务（MLaaS）平台，提供预训练模型、算法和解决方案。

**技术原理与实现**
*   **稀疏激活：** MoE 模型包含多个“专家”子网络。在推理过程中，一个门控网络决定将输入数据路由到哪几个最相关的专家。这使得模型可以拥有巨大的知识库（总参数大），但每次计算只消耗少量算力（激活参数小）。
*   **NVIDIA 优化：** 该模型很可能经过了 TensorRT-LLM 等工具的优化，以确保在 AWS GPU 实例上的显存占用和延迟达到最优。

**技术难点与解决方案**
*   **难点：** MoE 模型通常对显存带宽要求高，且在分布式训练和推理中调度复杂。
*   **解决方案：** NVIDIA 与 AWS 的深度合作解决了底层驱动和兼容性问题，通过 SageMaker 提供的一键部署封装了这些复杂性，用户无需手动处理张量并行或流水线并行。

**技术创新点分析**
*   **30B vs 3B 的平衡：** 30B 参数量保证了模型在复杂逻辑推理、多轮对话中的理解能力优于 7B 或 13B 的稠密模型；而 3B 的激活参数量则将推理成本和延迟降低到了接近小型模型的水平。这是一种针对特定商业场景的“甜点区”设计。

---

## 3. 实际应用价值

**对实际工作的指导意义**
对于 AI 工程师和企业 CTO 而言，这一发布意味着在模型选型时多了一个极具竞争力的选项。它打破了“要么用小模型（效果差），要么用大模型（成本高）”的二元对立。

**应用场景**
1.  **企业知识库问答 (RAG)：** 需要较好的理解能力来解析复杂文档，但预算有限。
2.  **多轮对话客服：** 需要低延迟以保证用户体验，30B 的智能度足以应对大部分通用问题。
3.  **代码生成与辅助：** 30B 规模的模型在代码逻辑生成上通常表现优于小模型，且成本可控。
4.  **内容摘要与提炼：** 处理长文本时，大参数量有助于保持上下文连贯性。

**需要注意的问题**
*   **微调成本：** 虽然推理激活参数少，但全参数微调 30B 模型依然需要昂贵的 GPU 资源（如 AWS `p4` 实例）。建议采用 LoRA 或 P-Tuning 等高效微调技术。
*   **显存占用：** 即使推理只激活 3B，加载整个 30B 模型仍需占用一定的显存（尽管可以通过量化技术缓解）。

**实施建议**
*   利用 SageMaker JumpStart 的“一键部署”功能进行 PoC（概念验证）。
*   对比该模型与 Llama-2-70B 或 Mistral-7B 在特定业务数据上的表现与成本账单。

---

## 4. 行业影响分析

**对行业的启示**
*   **模型架构转变：** 行业正从稠密模型向稀疏模型转变。NVIDIA 此举是在向开发者证明，MoE 不仅仅是 Google (GPT-4) 的专利，也是企业级落地的可行方案。
*   **云厂商竞争加剧：** AWS 与 NVIDIA 的深度绑定展示了“硬件厂商+云厂商”联合生态的优势，这对依赖自研芯片的云厂商或其他云平台构成了竞争压力。

**可能带来的变革**
*   **AI 应用开发的“精细化”：** 开发者将不再盲目追求参数量，而是开始关注“激活参数量”与“单位智能成本”的比率。

**发展趋势**
*   **API 服务化与私有化部署并重：** 企业既可以选择 API 调用，也可以通过 SageMaker 将 Nemotron 部署在 VPC 内（私有化），满足数据隐私需求，这将是金融和医疗行业的首选。

---

## 5. 延伸思考

**引发的思考**
*   **“小模型”的重新定义：** 随着量化技术和 MoE 的普及，我们评价模型的标准是否应该从“参数总量”转向“推理所需的实际算力”？
*   **边缘计算的可能性：** 如果推理仅需 3B 激活参数，经过极度压缩后，此类模型未来是否有潜力在高端边缘设备上运行，同时保持云端级的智能？

**拓展方向**
*   **多模态扩展：** Nemotron 系列未来是否会集成视觉编码器，成为多模态 MoE？
*   **动态路由的可解释性：** 研究模型在处理不同任务时激活了哪些专家，这将有助于 AI 的可解释性研究。

---

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估阶段：** 在 AWS SageMaker 中创建 Notebook Instance，从 JumpStart 部署 Nemotron 3 Nano 30B。
2.  **基准测试：** 准备 50-100 条业务相关的 Prompt，同时测试 Nemotron、Mistral-7B 和 Llama-2-70B。
3.  **成本分析：** 记录各模型的 Latency（延迟）和 Throughput（吞吐量），计算每 1000 次 Token 生成的大致成本。

**具体行动建议**
*   **数据准备：** 清洗企业专有数据，准备用于 SFT（监督微调）的数据集。
*   **安全审查：** 启用 SageMaker 的 VPC-only 访问，确保模型流量不流出公网。

**需补充的知识**
*   学习 **PEFT (Parameter-Efficient Fine-Tuning)** 方法，因为微调 30B 模型通常需要这些技术。
*   了解 **AWS Spot Instances** 的使用，以降低微调过程中的计算成本。

---

## 7. 案例分析

**成功案例（假设性推演）**
*   **场景：** 某跨国企业的内部 IT 助手。
*   **挑战：** 之前的 7B 模型无法理解复杂的 IT 架构文档，而 70B 模型推理太慢且昂贵。
*   **应用：** 引入 Nemotron 3 Nano 30B。利用其 30B 的知识库理解复杂文档，利用 3B 的激活参数保持低延迟。
*   **结果：** 准确率提升 20%，同时推理成本比使用 70B 模型降低了 60%。

**失败/反思案例**
*   **潜在陷阱：** 某团队试图在显存较小的实例（如 `ml.g5.xlarge` 24GB）上加载未量化的 30B 模型，导致 OOM (Out of Memory) 错误。
*   **教训：** 忽视了“总参数量”对显存加载的需求，只关注了“激活参数量”对计算速度的影响。必须配置足够的显存（如使用多 GPU 或量化版本）。

---

## 8. 哲学与逻辑：论证地图

**中心命题**
**NVIDIA Nemotron 3 Nano 30B 在 AWS SageMaker 上的可用性，为企业级生成式 AI 提供了最佳的“性能-成本”平衡点。**

**支撑理由**
1.  **经济性：** MoE 架构将推理成本降低至接近 3B 模型水平。
    *   *依据：* MoE 的稀疏激活特性，每次仅激活部分网络。
2.  **高性能：** 30B 总参数提供了比 7B/13B 模型更强的逻辑与推理能力。
    *   *依据：* 缩放定律表明，参数总量越大，模型的知识容量和潜在智能上限越高。
3.  **易用性：** SageMaker JumpStart 消除了部署的工程复杂性。
    *   *依据：* 预置的容器镜像和配置，实现了“一键部署”。

**反例与边界条件**
1.  **显存瓶颈：** 虽然推理计算量小，但加载模型仍需较大显存（30B 权重加载），不适合显存受限的边缘设备或低成本实例。
2.  **微调门槛：** 相比于真正的小模型（如 3B），全量微调 30B 模型依然需要昂贵的硬件资源。

**命题分类**
*   **事实：** 模型已上线，支持 MoE 架构，推理激活 3B 参数。
*   **价值判断：** “最佳平衡点”、“加速创新”（这是主观的商业价值判断）。
*   **可检验预测：** 该模型在同等推理成本下，性能将优于 7B 稠密模型；在同等性能下，成本将低于 70B 稠密模型。

**立场与验证**
*   **立场：** 支持该模型作为企业通用 AI 任务的优选方案，

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 SageMaker JumpStart 进行快速部署与验证

**说明**:
Nemotron 3 Nano 30B 是一个混合专家模型，参数量虽大但推理速度快。通过 SageMaker JumpStart，您可以以零代码方式快速部署该模型，验证其在特定业务场景（如摘要、问答、代码生成）中的表现，从而避免前期昂贵的本地环境配置成本。

**实施步骤**:
1. 登录 Amazon SageMaker 控制台，进入 "JumpStart" 页面。
2. 在搜索栏中输入 "Nemotron 3 Nano 30B" 或 "NVIDIA"。
3. 选择对应的模型卡片，点击 "Deploy"（部署）。
4. 配置实例类型（推荐使用 `ml.g5` 或 `ml.p4` 系列实例以获得最佳性价比）。
5. 部署完成后，使用控制台提供的测试界面输入 Prompt 进行验证。

**注意事项**:
JumpStart 默认配置可能并非针对所有任务的最优解，验证通过后，建议进入下一阶段进行微调或超参数调整。

---

### 实践 2：针对特定领域数据进行模型微调

**说明**:
虽然基础模型能力强大，但在垂直领域（如医疗、金融、法律）中，直接使用通用模型可能产生幻觉或术语不准确。利用 SageMaker 提供的微调功能，使用专有数据集对 Nemotron 3 Nano 进行训练，可以显著提升模型在特定任务上的准确性和相关性。

**实施步骤**:
1. 准备高质量的指令微调数据集（JSONL 格式），包含输入指令和期望输出。
2. 在 SageMaker JumpStart 模型页面，选择 "Train"（训练）选项卡。
3. 上传训练数据集至 S3 存储桶。
4. 设置超参数（如学习率、Epoch 数），由于是 MoE 模型，注意监控显存使用。
5. 启动训练任务，SageMaker 会自动处理基础设施配置。

**注意事项**:
微调 MoE 模型需要较大的显存资源，建议使用多 GPU 实例（如 `ml.g5.12xlarge` 或 `ml.g5.24xlarge`）以确保训练稳定性。

---

### 实践 3：优化推理实例选择以平衡成本与延迟

**说明**:
Nemotron 3 Nano 30B MoE 模型在推理时具有独特的激活特性。选择合适的实例类型对于控制成本和维持低延迟至关重要。NVIDIA GPU 对 Tensor Core 的优化能显著加速 MoE 模型的推理过程。

**实施步骤**:
1. 评估业务对延迟的要求（实时交互 vs 批处理）。
2. 对于实时应用，优先考虑配备 NVIDIA A10G 或 T4 GPU 的 `ml.g5` 实例。
3. 对于高吞吐量批处理，可考虑 `ml.p4` 实例。
4. 利用 SageMaker Inference Recommender 工具，输入模型 ID 和流量模式，获取最佳实例推荐。
5. 开启 SageMaker 的多模型适配或模型并行功能（如果模型尺寸超过单卡显存）。

**注意事项**:
MoE 模型虽然参数总量大，但每次推理只激活部分参数，因此显存占用主要取决于加载的模型权重而非激活值，但仍需确保实例显存足以容纳完整的 30B 权重。

---

### 实践 4：实施严格的提示词工程与安全防护

**说明**:
大语言模型对输入提示词非常敏感。为了确保 Nemotron 3 Nano 输出高质量且安全的内容，必须设计结构化的提示词模板，并利用 Guardrails 机制防止生成有害或有偏见的内容。

**实施步骤**:
1. 设计包含 "角色设定"、"任务描述"、"上下文" 和 "输出格式" 的结构化 Prompt 模板。
2. 在 SageMaker 端点配置中启用 Amazon Bedrock Guardrails（如果集成）或自行实现输入输出过滤层。
3. 针对常见攻击（如提示词注入）建立测试用例库。
4. 在生产环境中监控异常输入和输出日志。

**注意事项**:
不要仅依赖模型本身的安全对齐，必须在应用层构建双重防护，特别是当模型面向公众用户开放时。

---

### 实践 5：利用 MLOps 流程实现模型监控与版本管理

**说明**:
模型上线不是终点。利用 Amazon SageMaker 的 MLOps 功能（如 Model Registry 和 Pipelines），可以持续监控 Nemotron 3 模型的性能漂移、数据漂移以及异常行为，确保业务连续性。

**实施步骤**:
1. 将训练好的最佳模型注册到 SageMaker Model Registry 中。
2. 配置模型监控计划，定期捕获实时端点的输入输出数据。
3. 定义关键性能指标（KPI），如响应时间、错误率或输出质量评分。
4. 设置 CloudWatch 告警，当模型漂移指标超过阈值时触发通知。
5. 建立自动化 CI/CD 流水线，当新数据到来时自动触发重新训练和

---
## 学习要点

- NVIDIA Nemotron-3 Nano 30B 混合专家 (MoE) 模型现已在 Amazon SageMaker JumpStart 上正式提供，方便开发者快速部署。
- 该模型采用混合专家架构，在保持 300 亿参数规模的高性能同时，显著降低了推理成本和延迟。
- 开发者可以通过 SageMaker JumpStart 一键微调 (Fine-tune) 该模型，以适应特定的业务场景和私有数据。
- 模型针对商业应用进行了优化，特别适合企业级客户构建高效的生成式 AI 应用。
- 用户能够利用 Amazon SageMaker 的全托管基础设施，轻松实现模型的训练、部署和扩展管理。
- 此次合作进一步整合了 NVIDIA 的软件生态与 AWS 的云服务，降低了大语言模型的应用门槛。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [NVIDIA](/tags/nvidia/) / [Nemotron](/tags/nemotron/) / [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [MoE](/tags/moe/) / [LLM](/tags/llm/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [生成式AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8Fai/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-4.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-0.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpS]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-2.md" >}})
- [利用 Hugging Face 与 SageMaker 扩展企业级 LLM 微调]({{< relref "posts/20260210-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*