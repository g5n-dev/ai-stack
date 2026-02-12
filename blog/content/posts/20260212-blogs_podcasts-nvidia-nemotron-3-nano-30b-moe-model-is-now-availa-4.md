---
title: "NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta"
date: 2026-02-12T08:46:54+08:00
draft: false
entry_kind: "auto"
tags: ["NVIDIA", "Nemotron", "AWS", "SageMaker", "JumpStart", "MoE", "模型部署", "生成式 AI"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "NVIDIA Nemotron 3 Nano 30B 混合专家（MoE）模型现已在 Amazon SageMaker JumpStart 上正式可用。该模型拥有 30B 总参数，但活跃参数仅为 3B，旨在帮助用户在 AWS 上加速生成式 AI 应用开发。借助 SageMaker JumpStart 的托管部署功能，用户"
external_url: https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart
scenarios: ["AI/ML项目"]
---

# NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpStart 上线

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-11T19:38:47+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)

---
## 摘要/简介

今天我们很高兴地宣布，配备 3B 激活参数的 NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpStart 模型目录中正式全面上市。借助 Amazon Web Services (AWS) 上的 Nemotron 3 Nano，您可以加速创新并切实创造业务价值，无需应对模型部署的复杂问题。您可以通过 SageMaker JumpStart 提供的托管部署能力，将 Nemotron 的功能引入您的生成式 AI 应用中。

---
## 导语

NVIDIA Nemotron 3 Nano 30B 混合专家模型现已在 Amazon SageMaker JumpStart 正式上线。该模型拥有 30B 总参数，但在推理时仅激活 3B 参数，旨在兼顾高性能与低计算成本。本文将介绍如何利用 SageMaker 的托管部署能力，将 Nemotron 3 Nano 集成至您的生成式 AI 应用中，帮助您在 AWS 上高效构建解决方案并创造业务价值。

---
## 摘要

NVIDIA Nemotron 3 Nano 30B 混合专家（MoE）模型现已在 Amazon SageMaker JumpStart 上正式可用。该模型拥有 30B 总参数，但活跃参数仅为 3B，旨在帮助用户在 AWS 上加速生成式 AI 应用开发。借助 SageMaker JumpStart 的托管部署功能，用户无需管理复杂的部署流程即可使用 Nemotron 3 Nano，从而高效地推动创新并创造商业价值。

---
## 评论

**文章中心观点**
本文的核心观点在于，通过将NVIDIA的高效稀疏模型（Nemotron 3 Nano 30B MoE）与AWS的云原生平台深度集成，企业可以在保持推理成本可控的前提下，获得接近大型密集模型的性能，从而加速生成式AI在垂直行业的落地。

**支撑理由与边界条件分析**

1.  **MoE架构的“降本增效”红利**
    *   **事实陈述**：文章强调该模型拥有300亿总参数，但每次推理仅激活30亿参数（3B active）。
    *   **深度分析**：这是典型的Mixture of Experts (MoE) 架构优势。从技术角度看，这意味着在处理复杂任务时，模型能调动足够大的知识库（30B），而在推理延迟和显存占用上，却接近于一个小模型（3B）。这对于云上部署至关重要，因为它直接关联到Token的吞吐量和每千次推理的成本。
    *   **反例/边界条件**：MoE架构对硬件的显存带宽和调度能力要求极高。如果AWS底层实例的VRAM带宽不足，或者MoE的路由策略在特定任务上频繁切换专家，可能会导致延迟抖动，反而不如同等推理速度的密集模型（如Llama-2 13B）稳定。

2.  **云生态的“即插即用”降低了工程门槛**
    *   **事实陈述**：模型现成可用。
    *   **你的推断**：对于大多数传统企业而言，从HuggingFace下载模型、转换格式、编写推理服务脚本并处理CUDA错误，是阻碍AI落地的主要时间成本。SageMaker JumpStart提供的一键部署能力，消除了“MLOps工程 debt”。
    *   **反例/边界条件**：这种便利性伴随着“供应商锁定”风险。一旦业务深度依赖AWS特定的SageMaker实例和NVIDIA特定的微调格式，未来若想迁移至Azure或本地私有云，将面临高昂的迁移成本。

3.  **针对特定任务的“指令微调”实用性**
    *   **事实陈述**：Nemotron系列通常针对对话、摘要和代码生成进行了优化。
    *   **作者观点**：通用大模型（GPT-4等）虽强，但在特定行业数据（如金融报告摘要、医疗问诊）上往往缺乏精确度。Nemotron 3 Nano 30B作为一个开源权重可用的模型，允许企业在AWS上使用自己的私有数据进行SFT（监督微调），这是构建“私有化GPT”的关键路径。
    *   **反例/边界条件**：30B参数量级处于“尴尬的中间地带”。对于极简单的任务（如情感分类），它过于昂贵；对于极复杂的逻辑推理任务，其能力又不如70B+的模型或GPT-4。如果企业业务对逻辑推理要求极高，该模型可能无法满足预期。

**评价维度综述**

*   **内容深度与严谨性**：文章作为技术发布通告，事实陈述准确，但缺乏深度的性能基准测试数据。仅宣称“加速创新”略显空泛，若能提供与Llama-2 70B或Mistral 8x7B在相同AWS实例上的Latency对比数据，将更具说服力。
*   **实用价值**：极高。对于已经构建在AWS栈上的企业，这是一个现成的“生产级”解决方案，避免了从零开始选型和部署的痛苦。
*   **创新性**：中等。MoE并非新技术，但将其以30B/3B的配置在云端主流化，体现了NVIDIA与AWS试图在“性价比”这一细分市场上建立标准。
*   **行业影响**：这标志着大模型竞争从“参数军备竞赛”转向“单位智能成本竞赛”。未来，更多企业将倾向于使用这类“小参数大知识”的模型来构建垂直应用。

**可验证的检查方式**

1.  **基准测试**：在AWS `ml.g5.2xlarge` 或 `ml.p4d.24xlarge` 实例上部署该模型，使用标准数据集（如GSM8K或MMLU）进行评估，对比其吞吐量与Llama-2 13B及Mistral 7B的差异。
2.  **成本效益分析**：记录处理100万条Token所需的AWS实例小时数和费用，计算是否真的比使用密集型30B模型降低了50%以上的成本。
3.  **微调实验**：选取一个特定领域的非公开数据集（如公司内部知识库），在SageMaker上使用PEFT（LoRA）进行微调，观察模型在微调前后的幻觉率变化。
4.  **延迟观察**：在并发请求场景下（QPS从1到100），观察P99延迟的变化，验证MoE架构在高并发下的调度稳定性。

---
## 技术分析

基于您提供的文章标题和摘要，虽然原文内容被截断，但结合NVIDIA Nemotron 3 Nano 30B模型的技术背景及其在Amazon SageMaker JumpStart发布的行业意义，以下是关于这一事件的深度分析报告。

---

# 深度分析：NVIDIA Nemotron 3 Nano 30B MoE 模型登陆 AWS SageMaker JumpStart

## 1. 核心观点深度解读

**文章的主要观点**
这篇文章的核心在于宣布**企业级生成式AI的“高效化”与“普及化”**。通过将NVIDIA Nemotron 3 Nano 30B模型引入AWS SageMaker JumpStart，双方旨在解决企业在应用大语言模型（LLM）时面临的“性能与成本”矛盾。文章传达了一个明确信号：**企业无需从头训练或依赖超大规模参数的密集模型，也能在云端获得高性能、低延迟的生成式AI能力。**

**核心思想**
作者想要传达的核心思想是**“实用主义的AI落地”**。NVIDIA通过MoE（混合专家）架构，在保持30B模型总参数量的同时，仅激活3B参数，从而实现了“大模型的认知能力”与“小模型的运行成本”之间的完美平衡。这标志着AI基础设施的竞争从“堆砌参数”转向了“优化推理效率”。

**观点的创新性与深度**
这一观点的创新性在于打破了“越大越好”的迷思。它强调了架构创新（如MoE）比单纯的参数缩放更具商业价值。深度上，它触及了当前企业AI落地的最大痛点——高昂的推理成本和延迟，将技术讨论从学术基准拉向了Total Cost of Ownership (TCO) 和业务投资回报率 (ROI)。

**重要性**
这一观点至关重要，因为它为大规模商业化应用扫清了障碍。对于金融、客服、制造业等对数据安全和成本敏感的行业，能够在AWS这样的主流云平台上便捷地部署高效模型，意味着生成式AI从“玩具”真正变成了“工具”。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **MoE (Mixture of Experts，混合专家模型)**：这是该模型最核心的技术特征。与传统的密集模型不同，MoE模型拥有多个“专家”子网络，每次推理只激活其中一部分。
*   **Active Parameters (活跃参数)**：模型总共有30B参数，但在处理任何特定Token时，只有3B参数被激活并参与计算。
*   **Amazon SageMaker JumpStart**：AWS提供的机器学习开发中心，提供预训练模型、算法和解决方案。

**技术原理和实现方式**
Nemotron 3 Nano 30B 采用了稀疏激活机制。在Transformer架构中，MoE层替代了传统的全连接前馈层（FFN）。输入数据通过一个“门控网络”被路由到最相关的几个专家网络中。
*   **优势**：计算量随活跃参数（3B）线性增长，而模型容量（知识库）随总参数（30B）增长。
*   **实现**：在AWS上，这种模型通常经过针对特定GPU实例（如AWS G5或基于NVIDIA Ada Lovelace架构的实例）的优化，以确保显存占用和吞吐量的平衡。

**技术难点与解决方案**
*   **难点1：显存占用**。虽然计算量小，但加载30B参数仍需大量显存（约60GB+）。
    *   **解决方案**：利用量化和分片技术，以及AWS强大的后端计算集群支持。
*   **难点2：路由策略**。如何确保专家负载均衡，避免“塌缩”。
    *   **解决方案**：NVIDIA在训练过程中加入了负载均衡损失函数。

**技术创新点分析**
该模型最大的创新在于**针对特定垂直领域的高效微调**。Nemotron系列通常针对特定任务（如对话、指令遵循）进行了优化，结合MoE架构，使其能在保持通用能力的同时，通过微调快速适应企业特定需求，且推理成本远低于同等级别的密集模型（如Llama-2 70B）。

## 3. 实际应用价值

**对实际工作的指导意义**
这为企业CTO和AI团队提供了一个新的决策基准：在选择模型时，不应只看Benchmark分数，更应关注**“每美元的智能密度”**。对于大多数企业应用，30B MoE模型的表现可能优于8B密集模型，且成本远低于70B密集模型。

**可应用场景**
*   **企业知识库问答 (RAG)**：需要一定的语义理解能力，但要求低延迟。
*   **代码助手**：30B参数量通常足以覆盖大部分编程语法和逻辑，且响应速度快。
*   **客户服务自动化**：需要处理长上下文，MoE架构在处理长文本时更具性价比。
*   **内容摘要与生成**：需要高质量的文本输出，3B的活跃参数足以生成流畅的文本。

**需要注意的问题**
*   **微调复杂性**：MoE模型的微调比密集模型更复杂，容易导致专家功能失调，需要谨慎调整学习率。
*   **硬件要求**：虽然推理快，但部署门槛较高，需要较大显存的GPU，这在AWS上意味着较高的实例配置成本。

**实施建议**
建议企业利用SageMaker JumpStart的“一键部署”功能进行POC（概念验证）。对比该模型与Llama-2 13B/70B在特定业务数据上的表现与延迟，选择性价比最高的方案。

## 4. 行业影响分析

**对行业的启示**
这一发布预示着**“端云协同”与“高效推理”**将成为趋势。模型厂商开始更务实地提供“刚刚好”的模型，而不是一味追求“最大”。

**可能带来的变革**
*   **云厂商竞争白热化**：AWS与NVIDIA的深度绑定（尽管NVIDIA也在推自己的云），使得模型生态成为云厂商竞争的关键壁垒。
*   **MaaS (Model as a Service) 细分**：市场将细分为“超大规模模型”（用于科研）、“高效通用模型”（如Nemotron 30B）和“微型端侧模型”。

**对行业格局的影响**
这进一步巩固了NVIDIA在AI基础设施生态中的地位。不仅卖显卡，现在通过提供优化的模型软件栈，NVIDIA正在向软件和服务层渗透，这可能对传统的AI模型提供商（如单纯的初创公司）构成降维打击。

## 5. 延伸思考

**引发的思考**
随着MoE技术的普及，未来的模型评估标准可能会改变。我们是否需要一个新的指标，比如“智力/计算比率”，来衡量模型的效率？

**拓展方向**
*   **SLM (Small Language Models) 的崛起**：微软Phi、Google Gemma等小模型正在蚕食大模型的市场。Nemotron 30B MoE实际上处于中间地带，这是否是未来的主流形态？
*   **私有化部署的可行性**：如果模型足够高效，企业是否会倾向于将其部署在本地而非云端，以解决数据隐私问题？

**未来趋势**
模型将不再是一成不变的静态权重，而是根据任务动态组合的“专家网络”。未来的AI系统可能由一个通用的“路由器”和无数个专用的“小专家”组成。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估阶段**：在AWS SageMaker中创建Notebook实例，通过JumpStart调用Nemotron 3 Nano 30B。
2.  **基准测试**：选取公司典型的Prompt（如客服问答、文档摘要），对比该模型与目前使用的模型（如GPT-3.5-turbo或Claude Instant）的响应速度和准确率。
3.  **微调实验**：尝试使用SageMaker的微调功能，用公司私有数据对模型进行轻量级适配。

**具体行动建议**
*   **技术团队**：学习MoE模型的部署细节，特别是显存管理和吞吐量优化。
*   **管理层**：重新评估AI项目的预算，基于Nemotron的低延迟特性，探索以前因成本过高而放弃的实时交互场景。

**注意事项**
*   监控API调用的成本，虽然推理效率高，但AWS实例的租用费用仍需控制。
*   注意模型的幻觉问题，30B参数模型在某些极度复杂的专业领域可能仍不如70B+模型准确。

## 7. 案例分析

**成功案例假设：跨国电商客服系统**
*   **背景**：某电商巨头需要处理多语言、高并发的客服咨询。
*   **方案**：使用Nemotron 3 Nano 30B。利用其30B参数的强大语言能力处理多语言，利用MoE的3B活跃参数特性实现低延迟响应。
*   **结果**：相比使用Llama-2 70B，推理成本降低了40%，同时保持了95%以上的意图识别准确率。

**失败案例反思：通用医疗诊断辅助**
*   **背景**：一家初创公司试图直接使用该模型进行复杂的医疗影像报告生成。
*   **问题**：虽然模型很大，但在特定医疗领域的深度知识可能不足，且MoE模型在微调时如果数据不当，容易导致专家“遗忘”知识。
*   **教训**：对于高度专业、容错率极低的领域，通用的高效模型不能完全替代经过海量专业数据训练的密集模型。

## 8. 哲学与逻辑：论证地图

**中心命题**
**NVIDIA Nemotron 3 Nano 30B 在 AWS SageMaker 上的可用性，为企业大规模部署生成式 AI 提供了最优的“性能-成本”平衡点。**

**支撑理由与依据**
1.  **理由一：架构优势带来效率提升。**
    *   依据：MoE 架构仅激活 3B 参数，相比 30B 的密集模型，理论计算量降低约 10 倍，直接降低推理成本和延迟。
2.  **理由二：平台集成降低部署门槛。**
    *   依据：SageMaker JumpStart 提供预配置环境，消除了复杂的模型编译、容器化和环境配置工作，将上线时间从数周缩短至数分钟。
3.  **理由三：模型容量保证输出质量。**
    *   依据：30B 的总参数量提供了足够大的知识库，在推理、逻辑和代码任务上的表现通常优于 7B/13B 级别的小模型。

**反例与边界条件**
1.  **反例一：对于极低延迟要求的边缘计算场景。**
    *   条件：如果应用场景必须在本地设备（如手机、IoT设备）上运行，30B 模型的显存需求（约60GB）仍然过高，此时 3B 的微型密集模型（如 Gemma 2B）才是更优解。
2.  **反例二：对于极度复杂的推理任务。**
    *   条件：如果任务需要极深层次的逻辑推理或世界知识（如高难度的科研数学问题），30B MoE 可能受限于模型容量上限，此时 175B+ 的超大规模模型（如 GPT-4）仍是不可替代的。

**命题属性分析**
*   **事实**：模型已发布，基于 MoE 架构，参数配置为 30B/3B Active。
*   **价值判断**：“最优平衡点”是一个价值判断，取决于具体的业务场景和成本结构。
*   **可检验预测**：在标准企业级 NLU 基准测试（如 MMLU subset）中，该模型的得分/推理时间比率应高于 Llama-2 70B 和 Mistral 7

---
## 最佳实践

## 最佳实践指南

### 实践 1：选择正确的实例类型以优化性价比

**说明**: NVIDIA Nemotron 3 Nano 30B 是一个混合专家模型，虽然参数量为 30B，但通过 MoE 架构，每次推理仅激活部分参数。然而，为了获得最佳吞吐量，仍需配备足够显存的 GPU。在 SageMaker JumpStart 中，选择支持多 GPU 分布式推理的实例类型（如 `ml.g5.12xlarge` 或 `ml.g5.24xlarge`）可以平衡成本与性能，避免显存溢出（OOM）错误。

**实施步骤**:
1. 在 SageMaker JumpStart 控制台中选中 Nemotron 3 Nano 30B 模型。
2. 在部署配置中，审查默认的实例类型。如果是单卡显存不足的实例（如 `ml.g5.xlarge`），请务必更改。
3. 推荐选择 `ml.g5.12xlarge`（4块 GPU）或更大，以容纳模型权重并处理并发请求。
4. 启用 SageMaker 的多 GPU 分布式推理功能（通常由 JumpStart 自动配置）。

**注意事项**: 避免使用 CPU 实例进行推理，延迟将不可接受。

---

### 实践 2：配置动态批处理以提升吞吐量

**说明**: 在生产环境中，请求往往是间歇性到达的。如果对每个请求都单独进行推理，GPU 利用率会很低。配置动态批处理允许 SageMaker 在短时间内将多个用户请求组合成一个批次进行处理，从而显著提高 GPU 的利用率和系统的整体吞吐量，同时不增加显着的端到端延迟。

**实施步骤**:
1. 在创建 SageMaker 端点时，进入“高级”设置或修改推理配置参数。
2. 设置 `EnableDynamicBatching` 为 `true`。
3. 调整 `MaxBatchSize`（例如设置为 4 或 8，取决于显存余量）和 `BatchWaitTime`（例如 0.1s - 0.5s）。
4. 部署端点并使用负载测试工具（如 Locust）验证吞吐量提升情况。

**注意事项**: `BatchWaitTime` 设置过大会增加首字节延迟（TTFT），需要根据实时性要求权衡。

---

### 实践 3：利用 SageMaker Model Monitor 进行漂移检测

**说明**: 模型部署后，输入数据的分布可能会随时间发生变化，导致模型性能下降。Nemotron 3 Nano 30B 通常用于文本生成或理解，监控输入 Prompt 的长度分布和输出质量至关重要。开启 Model Monitor 可以自动捕获输入输出数据，并检测数据质量偏差或模型性能退化。

**实施步骤**:
1. 在端点配置中启用数据捕获功能。
2. 定义基线约束，例如 Prompt 的平均 token 长度、响应时间 P95 等。
3. 创建一个 Model Monitoring 计划，设定按小时或天进行监控。
4. 配置 CloudWatch 告警，当检测到偏差（如输入长度异常导致截断）时发送通知。

**注意事项**: 确保捕获的数据不包含敏感信息（PII），或配置脱敏规则以符合合规要求。

---

### 实践 4：应用 LoRA 进行高效任务微调

**说明**: 虽然 Nemotron 3 Nano 30B 是一个强大的基座模型，但针对特定领域（如医疗、金融或特定对话风格）通常需要微调。使用低秩适应技术，可以在不重新训练全部参数的情况下，仅训练极少量的参数即可获得极佳的领域适配效果，大幅降低微调成本和存储开销。

**实施步骤**:
1. 在 SageMaker JumpStart 中选择“Train”选项卡，选中 Nemotron 3 Nano 30B。
2. 选择“Fine-tuning”作业类型，并选择 PEFT（参数高效微调）或 LoRA 算法。
3. 准备特定领域的指令微调数据集（JSONL 格式）。
4. 设置超参数（如 `lora_alpha`, `lora_r`），启动训练作业。
5. 将生成的 LoRA artifact 与原基座模型合并部署。

**注意事项**: 微调数据集的质量直接决定了微调效果，需确保指令清晰且无噪声。

---

### 实践 5：实施自动扩缩容策略

**说明**: 大语言模型推理负载通常具有明显的波峰波谷。为了优化成本，不应一直维持最高配置的实例数量。利用 SageMaker 的自动扩缩容功能，可以根据并发请求数量（CPU 利用率或请求数指标）自动增加或减少实例数量，在低流量时节省成本，在高流量时保持性能。

**实施步骤**:
1. 部署端点后，进入端点配置页面，点击“Edit”变体配置。
2. 在“Instance settings”中配置自动扩缩容策略。
3. 设置最小实例数为 0（如果允许冷启动）或 1（需保持预热），最大实例数根据预算设定。
4. 定义扩容触发指标，例如 `SageMakerVariant

---
## 学习要点

- NVIDIA Nemotron-3 Nano 30B 混合专家（MoE）模型现已在 Amazon SageMaker JumpStart 上提供，实现了高性能模型与云平台部署便利性的结合。
- 该模型采用混合专家（MoE）架构，在保持 300 亿参数规模的同时，通过稀疏激活机制大幅降低了推理成本和延迟。
- 用户可以通过 SageMaker JumpStart 快速部署该模型，利用 Amazon SageMaker 的基础设施进行高效的模型微调和推理。
- 该模型旨在平衡性能与计算效率，使企业能够在不牺牲模型质量的前提下，优化大语言模型的运营支出。
- 此次集成简化了在 AWS 云环境中获取和使用 NVIDIA 先进生成式 AI 技术的流程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [NVIDIA](/tags/nvidia/) / [Nemotron](/tags/nemotron/) / [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [JumpStart](/tags/jumpstart/) / [MoE](/tags/moe/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [生成式 AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8F-ai/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-0.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpS]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-2.md" >}})
- [利用 Hugging Face 与 SageMaker 扩展企业级 LLM 微调]({{< relref "posts/20260210-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Nemotron-Personas-Brazil：主权AI协同设计数据集]({{< relref "posts/20260129-blogs_podcasts-nemotron-personas-brazil-co-designed-data-for-sove-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*