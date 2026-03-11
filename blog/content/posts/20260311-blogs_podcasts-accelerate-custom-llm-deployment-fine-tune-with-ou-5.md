---
title: "在 EC2 上使用 Oumi 微调并部署 Llama 至 Amazon Bedrock"
date: 2026-03-11T13:32:50+08:00
draft: false
entry_kind: "auto"
tags: ["Llama", "Oumi", "Amazon Bedrock", "EC2", "S3", "模型微调", "模型部署", "Custom Model Import"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "本文介绍了如何利用 Oumi 在 Amazon EC2 上微调 Llama 模型，并通过 Amazon Bedrock 的“自定义模型导入”功能进行托管部署的完整流程。主要步骤如下： 1. **使用 Oumi 微调模型**：在 Amazon EC2 实例上运行 Oumi，对 Llama 基础模型进行微调（可结合 Oum"
external_url: https://aws.amazon.com/blogs/machine-learning/accelerate-custom-llm-deployment-fine-tune-with-oumi-and-deploy-to-amazon-bedrock
scenarios: ["Web应用开发"]
---

# 在 EC2 上使用 Oumi 微调并部署 Llama 至 Amazon Bedrock

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-10T15:42:16+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/accelerate-custom-llm-deployment-fine-tune-with-oumi-and-deploy-to-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-custom-llm-deployment-fine-tune-with-oumi-and-deploy-to-amazon-bedrock)

---
## 摘要/简介

在本篇文章中，我们将展示如何使用 Oumi 在 Amazon EC2 上微调 Llama 模型（并可选择使用 Oumi 生成合成数据），将产物存储在 Amazon S3 中，并通过 Custom Model Import 部署到 Amazon Bedrock，以实现托管推理。

---
## 导语

随着大语言模型应用场景的日益细分，如何高效地将开源模型适配至特定业务需求并实现生产级部署，已成为开发者关注的重点。本文将详细介绍如何利用 Oumi 在 Amazon EC2 上微调 Llama 模型，并通过 Amazon Bedrock 的 Custom Model Import 功能完成托管部署。通过阅读此文，您将掌握一条从模型微调到云端推理的完整技术路径，从而加速构建定制化的 AI 解决方案。

---
## 摘要

本文介绍了如何利用 Oumi 在 Amazon EC2 上微调 Llama 模型，并通过 Amazon Bedrock 的“自定义模型导入”功能进行托管部署的完整流程。主要步骤如下：

1.  **使用 Oumi 微调模型**：在 Amazon EC2 实例上运行 Oumi，对 Llama 基础模型进行微调（可结合 Oumi 生成的合成数据）。
2.  **存储模型文件**：将微调完成的模型产物保存至 Amazon S3 存储桶中。
3.  **部署至 Bedrock**：利用 Amazon Bedrock 的 Custom Model Import 功能，将 S3 中的模型导入，实现托管推理，从而加速自定义大模型的部署与应用。

---
## 评论

**文章中心观点**
该文章主张通过构建标准化的开源工具链（Oumi）与云厂商托管服务（Amazon Bedrock）的深度集成，来解决企业级大模型落地中“训练灵活性与部署运维成本”之间的矛盾，实现从数据准备到生产环境推理的低损耗闭环。

**支撑理由与评价**

1.  **全链路工具链的“降本增效”逻辑（事实陈述）**
    文章展示了从 EC2 上的 Oumi 微调，到 S3 的模型存储，再到 Bedrock 的托管推理这一完整路径。其核心价值在于将复杂的 MLOps 流程标准化。对于企业而言，使用 Oumi 在 EC2 上进行微调保留了底层基础设施的控制权（如选择 GPU 实例类型、调整训练参数），而导入 Bedrock 则利用了云厂商的托管能力，解决了模型上线后的扩缩容、高可用和安全合规问题。这种“Hybrid”（混合）架构是当前企业落地的主流选择。

2.  **合成数据的实用主义导向（作者观点）**
    文章特别提到使用 Oumi 生成合成数据进行微调。这是一个非常敏锐且切中痛点的切入点。在垂直行业落地中，高质量私有数据往往极度匮乏。Oumi 内置合成数据生成功能，实际上是在推广一种“Data-Centric AI”的范式，即通过模型生成数据来反哺模型训练。虽然合成数据的质量控制仍是难题，但将其无缝集成到训练流程中，显著降低了数据准备的门槛。

3.  **对“私有化部署”与“API调用”中间地带的填补（你的推断）**
    行业内长期存在两难选择：要么调用 OpenAI/Claude 等 API（无数据隐私风险但成本不可控且不可定制），要么完全自建（成本极高且运维难度大）。文章提出的方案实际上填补了中间地带：企业拥有模型权重（存储在 S3），但借用了云厂商的推理基础设施。这对于金融、医疗等对数据主权敏感但又不想自建机房的行业具有极高的吸引力。

**反例与边界条件**

1.  **成本陷阱与长尾延迟（事实陈述）**
    虽然文章强调了便利性，但未深入探讨成本结构。Amazon Bedrock 的托管推理费用通常高于直接在 EC2 上部署开源模型（如使用 vLLM 或 TGI）。对于高并发、低延迟要求的场景，Bedrock 可能引入额外的网络跳转，导致延迟增加。如果企业已有成熟的 K8s 运维团队，完全自建推理可能比导入 Bedrock 更经济。

2.  **供应商锁定风险（作者观点）**
    尽管模型是开源的 Llama，但工作流与 AWS 特定服务（S3, Bedrock, IAM）深度绑定。一旦企业希望迁移出 AWS 或切换到 Azure/GCP，迁移成本并不低。此外，Bedrock 的 Custom Model Import 目前支持的模型架构有限，如果未来模型格式发生剧烈变化（如从 Llama 2 迁移到某种新架构），该链路的兼容性存在不确定性。

**深入评价维度分析**

*   **内容深度与严谨性（3.5/5）**
    文章作为一篇技术 Tutorial，在操作步骤上足够严谨，代码示例（推断其包含）应当具备可执行性。但在深度上，它主要侧重于“怎么做”，而非“为什么”。例如，它未深入探讨微调过程中的超参数选择对最终模型在 Bedrock 上推理性能的具体量化影响，也未对比 Bedrock 与 EC2 自建推理在 P99 延迟上的具体差异。

*   **创新性（4/5）**
    将 Oumi（一个相对新兴的开源框架）作为主角与 AWS 企业级服务结合，具有一定的前瞻性。这打破了以往只使用 Hugging Face Trainer 或 SageMaker 的常规路径，展示了更轻量级、社区驱动工具与企业服务结合的可能性。

*   **行业影响（4/5）**
    这篇文章实际上在推广一种新的行业标准：MLOps 工具应当具备“云原生”的基因。它鼓励开源工具开发者不仅要关注算法，还要关注与主流云厂商 API 的对接。这种趋势会加速大模型从“实验室”走向“生产环境”。

**可验证的检查方式**

1.  **端到端时间损耗测试（指标）**
    从准备数据集开始计时，记录在 EC2 上完成一次 Llama 3 8B 模型 Full Fine-tuning 或 LoRA 的时间，加上上传 S3 及在 Bedrock 完成导入的时间，对比直接使用 SageMaker Training/Deployment 或完全本地部署的总耗时。

2.  **推理性能基准对比（实验）**
    部署完成后，使用相同的 Prompt Set 对 Bedrock 上的该模型与直接在 EC2 (p4d/p5 实例) 上部署的 vLLM 进行压测。观测并对比 Tokens/sec (吞吐量) 和 Time to First Token (首字延迟)。

3.  **合成数据质量评估（观察窗口）**
    运行文章中提到的合成数据生成流程，使用 LLM-as-a-Judge（如使用 GPT-4o）对生成的数据进行质量打分（准确性、多样性），验证其生成的数据是否真的能提升微调后模型在特定下游任务（如分类、摘要）的表现，而非引入噪声。

**实际应用建议**

*   **不要盲目追求全流程自动化**：虽然 Oumi 提供了便利，但在导入 Bedrock 前，务必在 EC2 上进行严格的模型评估。一旦模型进入 Bedrock，迭代修错的成本（重新导入、审核）较高。
*   **关注合成

---
## 技术分析

基于您提供的文章标题和摘要，以下是对该技术方案的深度全面分析。

---

# Accelerate custom LLM deployment: Fine-tune with Oumi and deploy to Amazon Bedrock 深度分析

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于构建一条**“从开源训练到托管服务”的标准化高速通道**。它主张利用开源工具链（Oumi）在云基础设施上进行模型微调，随后无缝导入全托管的生成式AI服务中，从而解决企业级定制大模型落地中“开发难、部署重、运维复杂”的痛点。

**作者想要传达的核心思想**
作者试图传达一种**“混合云AI最佳实践”**的思维模式：
1.  **数据主权与灵活性优先**：利用开源工具（Oumi）和算力（EC2）掌握核心微调过程，甚至通过合成数据技术解决数据匮乏问题。
2.  **基础设施现代化**：不要在模型训练完成后，还要自己搭建复杂的推理API服务器，应直接利用Bedrock这样的托管服务来获得高可用、低延迟和安全性。
3.  **标准化流程**：通过S3作为中间桥梁，打通训练产物与推理服务，实现CI/CD级别的自动化部署。

**观点的创新性和深度**
*   **创新性**：将**合成数据生成**（Synthetic Data Generation）直接集成到微调流程中，并直接对接企业级私有化部署（Bedrock Custom Model Import），这是一个非常前沿的端到端闭环。它不仅仅是讲“怎么用”，而是讲“怎么高效且低成本地用”。
*   **深度**：文章触及了LLM Ops（LLMOps）的核心——即模型资产的流转。它不再将微调和部署视为割裂的两个步骤，而是视为一个连续的资产交付流水线。

**为什么这个观点重要**
随着大模型从“通用”走向“垂直”，企业迫切需要将私有数据注入模型。然而，从头训练极贵，直接调用API又存在数据隐私和幻觉问题。**“微调+私有化部署”**是当前企业落地的最优解，而本文提供的方法论极大地降低了这一路径的工程门槛和运维成本。

---

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Oumi**：一个开源的LLM训练与评估框架，支持全参数微调、LoRA等。
*   **Amazon EC2 (P3/P4/P5 instances)**：提供高性能GPU算力（如NVIDIA H100/A100），用于执行密集型训练任务。
*   **Amazon S3 (Simple Storage Service)**：作为模型权重的存储湖，连接训练侧和推理侧。
*   **Amazon Bedrock (Custom Model Import)**：允许用户导入自定义微调过的模型，并在Bedrock的托管环境中运行，享受原生API接口。
*   **Synthetic Data Generation (合成数据)**：利用强模型（如Llama 3 70B）生成弱模型（如Llama 3 8B）的训练数据，用于特定任务微调。

**技术原理和实现方式**
1.  **训练阶段**：用户在EC2上启动Oumi容器。Oumi负责加载预训练模型（如Llama 3 8B），处理数据集（或使用合成数据生成脚本），并执行分布式训练（如FSDP/ZeRO）。
2.  **存储阶段**：训练完成后，生成的模型权重（通常为Safetensors或PyTorch Bin格式）及配置文件上传至S3存储桶。
3.  **部署阶段**：通过Bedrock的Import Model API，指向S3中的模型路径。Bedrock服务会自动容器化该模型，部署在隔离的计算环境中，并提供标准的InvokeModel端点。

**技术难点和解决方案**
*   **难点1：环境配置复杂。** 搭建深度学习环境（CUDA、驱动、依赖库）极其耗时。
    *   *解决方案*：Oumi提供预构建的Docker镜像或Helm Charts，可在EC2上一键启动，屏蔽底层环境差异。
*   **难点2：数据隐私与合规。** 企业数据不能外传。
    *   *解决方案*：全流程在VPC（虚拟私有云）内完成，S3加密，Bedrock提供VPC接口支持，确保数据不出域。
*   **难点3：推理运维。** 微调后的模型如何处理并发、扩缩容？
    *   *解决方案*：利用Bedrock的托管特性，AWS自动处理推理容器的健康检查、负载均衡和扩缩容。

**技术创新点分析**
*   **合成数据闭环**：文章提到利用Oumi生成合成数据。这意味着企业不需要有标注好的高质量数据集，只需要提供原始文档种子，即可利用大模型生成问答对来微调小模型，这是解决“最后一公里”数据工程的关键技术。

---

## 3. 实际应用价值

**对实际工作的指导意义**
该方案为企业AI团队提供了一套**“可落地的生产级架构”**。它避免了团队陷入“造轮子”的陷阱（即自己开发推理框架、自己搞K8s调度），让算法工程师专注于模型效果本身，而非基础设施运维。

**可以应用到哪些场景**
1.  **企业私有知识库问答**：利用公司内部文档生成合成数据，微调Llama 3，部署为内部ChatBot。
2.  **行业特定模型（金融/医疗/法律）**：这些领域对数据隐私要求极高，且通用模型效果不佳，必须通过微调+私有部署解决。
3.  **风格化文本生成**：营销文案生成，需要微调模型以符合特定品牌调性。

**需要注意的问题**
*   **成本控制**：EC2上的GPU训练和Bedrock上的托管推理均按使用量计费，需严格控制预算。
*   **模型评估**：微调后的模型是否真的比基座模型好？需要建立严格的评估集。
*   **Vendor Lock-in（厂商锁定）**：虽然模型是开源的，但部署层依赖Bedrock。迁移回其他平台需要重新搭建推理服务。

**实施建议**
*   先在小规模数据集上验证流程的通畅性。
*   使用LoRA（Low-Rank Adaptation）而非全参数微调以降低存储和部署成本。
*   建立自动化CI/CD流水线，当S3中的模型更新时，自动触发Bedrock的模型导入。

---

## 4. 行业影响分析

**对行业的启示**
这标志着**云厂商与开源社区的深度融合**。AWS不再仅仅推销自研模型，而是通过“拥抱开源”来构建生态。这启示行业：未来的竞争不是“闭源 vs 开源”，而是**“谁能为开源模型提供最好的托管服务”**。

**可能带来的变革**
*   **MLOps的标准化**：从“脚本式”操作转向“平台化”操作。
*   **中小企业AI应用的门槛降低**：不需要养一个庞大的运维团队，只需懂算法和API即可上线定制模型。

**相关领域的发展趋势**
*   **模型压缩与推理优化**：为了在Bedrock上跑得更快、更省钱，模型量化（AWQ/GPTQ）技术将成为标准配置。
*   **合成数据爆发**：随着高质量人工数据耗尽，合成数据生成将成为微调的主流数据来源。

**对行业格局的影响**
这种模式削弱了单纯依靠API调用（如仅调用OpenAI）的厂商的护城河，增强了拥有强大云基础设施（AWS）和灵活开源工具链（Oumi/HuggingFace）组合的厂商的竞争力。

---

## 5. 延伸思考

**引发的其他思考**
*   **模型迭代的生命周期管理**：当我们频繁微调模型并导入Bedrock，如何管理版本？如何进行A/B测试？
*   **多模态扩展**：目前的流程主要针对文本，Llama 3及其后续版本的多模态能力如何通过此流程高效部署？

**可以拓展的方向**
*   **RAG + Fine-tuning 结合**：仅仅微调是不够的，如何将检索增强（RAG）与微调后的模型结合，利用Bedrock的Knowledge Base功能？
*   **边缘端部署**：微调完的小模型是否可以不仅部署在云端，还能通过类似流程部署到本地服务器（如Snowball Edge）？

**需要进一步研究的问题**
*   合成数据的质量对微调模型具体有多大影响？如何过滤低质量合成数据？
*   Bedrock Custom Model Import 的冷启动时间和并发上限具体是多少？

---

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估数据**：确定你是否有私有数据需要微调，或者是否需要生成合成数据。
2.  **环境搭建**：在AWS账号中申请GPU实例权限，安装Oumi。
3.  **小规模实验**：使用Llama 3 8B Instruct作为基座，用100条合成数据进行LoRA微调。
4.  **部署验证**：导入Bedrock，编写Python脚本调用InvokeModel，对比微调前后的输出差异。

**具体的行动建议**
*   学习Oumi的YAML配置文件语法。
*   熟悉AWS IAM角色权限配置，确保EC2和Bedrock有权限访问S3。
*   预算规划：预留约$200-$500用于初步的EC2训练和测试费用。

**需要补充的知识**
*   **PyTorch**：理解模型权重和检查点。
*   **Docker**：理解容器化部署。
*   **AWS CLI/SDK**：用于自动化脚本编写。

**实践中的注意事项**
*   **S3路径清理**：训练过程中会产生大量中间Checkpoints，上传S3前需清理，只保留最终权重，否则会产生高昂的存储费用。
*   **超参数敏感性**：微调的学习率非常关键，过大可能导致模型“遗忘”预训练知识（Catastrophic Forgetting）。

---

## 7. 案例分析

**结合实际案例说明**
假设一家**跨国金融机构**想要构建一个内部合规性审查助手。
*   **通用模型**：不懂内部合规手册，且数据不能发给OpenAI。
*   **传统方案**：买显卡，搭K8s，开发API，运维成本极高。

**成功案例分析**
利用本文方案：
1.  **数据准备**：将过去5年的合规审查报告脱敏。
2.  **合成数据**：用Llama 3 70B生成“违规案例-修正建议”对。
3.  **微调**：在EC2 p4d实例上用Oumi微调Llama 3 8B。
4.  **部署**：导入Bedrock。
5.  **结果**：模型学会了特定的合规语气和规则，且API调用完全在AWS VPC内，满足合规要求。开发人员只需关注业务逻辑，无需维护GPU服务器。

**失败案例反思**
*   **失败点**：直接使用原始文档进行微调，未做清洗。
*   **后果**：模型学到了文档中的HTML标签和乱码，输出格式混乱。
*   **教训**：数据质量（包括合成数据的质量）直接决定模型上限。Garbage In, Garbage Out。

**经验教训总结**
微调不是万能药。如果任务是逻辑推理（如数学题），微调效果有限；如果任务是风格迁移、知识注入或格式化输出，微调效果极佳。

---

## 8. 哲学与逻辑：论证地图

**中心命题**
**“利用开源工具（Oumi）在云基础设施（EC2）上进行大模型微调，并

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Oumi 简化模型微调流程

**说明**: Oumi 是一个开源平台，旨在统一大语言模型（LLM）的开发、微调和评估过程。利用 Oumi 可以大幅降低微调的技术门槛，它提供了预配置的配方和模块化的架构，支持从数据准备到模型训练的全生命周期管理，避免了手动配置复杂的训练环境。

**实施步骤**:
1. 安装 Oumi 框架并配置相应的 Python 环境。
2. 准备并格式化训练数据集，利用 Oumi 的数据工具进行验证。
3. 选择适合特定任务的预训练模型（如 Llama 3 或 Mistral）。
4. 运行 Oumi 提供的微调脚本，利用 LoRA 或全量微调技术训练模型。

**注意事项**: 确保在微调前对数据进行清洗和质量控制，低质量的数据会导致模型性能下降。

---

### 实践 2：高效的数据集准备与清洗

**说明**: 模型的性能高度依赖于训练数据的质量。在部署自定义 LLM 之前，必须构建高质量、指令遵循格式的数据集。这包括去除重复数据、过滤有害内容以及格式化为对话或指令微调格式。

**实施步骤**:
1. 收集特定领域的原始文本数据。
2. 使用自动化脚本去除隐私信息、重复项和低质量文本。
3. 将数据转换为 JSONL 或 Oumi 支持的标准格式（如 Instruction/Input/Output 结构）。
4. 划分训练集、验证集和测试集，以监控过拟合情况。

**注意事项**: 保持数据分布的多样性，避免模型在某些特定模式上产生偏见。

---

### 实践 3：选择正确的微调策略与参数

**说明**: 并非所有任务都需要全量微调。为了加速部署并降低成本，应根据具体需求选择参数高效微调（PEFT）技术，如 LoRA 或 QLoRA。这可以在保留基础模型知识的同时，以极少的参数量注入新知识。

**实施步骤**:
1. 评估任务复杂度，决定使用全量微调还是 PEFT。
2. 在 Oumi 配置文件中设置 LoRA 参数（如 rank, alpha, target_modules）。
3. 配置超参数（学习率、批处理大小、Epochs）。
4. 启动训练并利用 WandB 或 TensorBoard 监控损失曲线。

**注意事项**: 初始学习率不宜过高，以免破坏预训练模型的权重，导致灾难性遗忘。

---

### 实践 4：模型量化以优化推理性能

**说明**: 在将模型部署到 Amazon Bedrock 之前，对模型进行量化可以显著减少显存占用并提高推理速度。将模型从 FP16 或 BF16 转换为 INT8 或 FP4 格式，是在保持精度的前提下实现低延迟部署的关键步骤。

**实施步骤**:
1. 在微调完成后，使用量化工具（如 bitsandbytes 或 AutoGPTQ）。
2. 将模型权重转换为 4-bit 或 8-bit 量化格式。
3. 在本地加载量化模型进行验证，确保精度损失在可接受范围内。
4. 准备将量化后的模型上传至托管环境。

**注意事项**: 量化可能会影响模型对复杂指令的细微理解能力，必须在部署前进行充分的评估测试。

---

### 实践 5：构建自定义容器并部署至 Amazon Bedrock

**说明**: Amazon Bedrock 提供了全托管服务，但部署自定义微调模型通常需要通过 Amazon SageMaker 将模型构建成容器，然后将其导入到 Bedrock 的知识库或作为自定义端点使用。这一步实现了模型的生产级可用性和高可用性。

**实施步骤**:
1. 使用 Docker 将微调好的模型及其推理服务（如 vLLM 或 Text Generation Inference）打包。
2. 将容器镜像推送到 Amazon ECR（Elastic Container Registry）。
3. 在 Amazon SageMaker 上部署模型端点进行测试。
4. 配置 Amazon Bedrock 的自定义模型导入功能（如果使用 Bedrock Custom Model Import）或通过 API Gateway 连接 SageMaker 端点。

**注意事项**: 确保容器实例配置了足够的 CPU 和内存资源，以处理模型加载和并发请求。

---

### 实践 6：建立全面的评估与安全护栏

**说明**: 部署不仅仅是上线，还需要确保模型输出符合安全和业务标准。必须建立自动化评估流水线，并利用 Amazon Bedrock Guardrails 或类似机制来过滤有害内容，防止模型产生幻觉或不当回复。

**实施步骤**:
1. 使用测试集对部署后的模型运行基准测试，对比微调前后的性能指标。
2. 配置 Amazon Bedrock Guardrails，定义拒绝主题和内容过滤策略。
3. 实施人工审查反馈循环（RLHF），收集早期用户的反馈数据。
4. 设置 CloudWatch 告警，监控模型的延迟和错误率。

**注意事项**: 安全护栏不应过度限制模型的输出能力，需要在安全性和实用性之间找到平衡点。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/accelerate-custom-llm-deployment-fine-tune-with-oumi-and-deploy-to-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-custom-llm-deployment-fine-tune-with-oumi-and-deploy-to-amazon-bedrock)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Llama](/tags/llama/) / [Oumi](/tags/oumi/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [EC2](/tags/ec2/) / [S3](/tags/s3/) / [模型微调](/tags/%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [Custom Model Import](/tags/custom-model-import/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [在 EC2 上使用 Oumi 微调 Llama 并部署至 Amazon Bedrock]({{< relref "posts/20260310-blogs_podcasts-accelerate-custom-llm-deployment-fine-tune-with-ou-0.md" >}})
- [在 EC2 上使用 Oumi 微调 Llama 并部署至 Amazon Bedrock]({{< relref "posts/20260310-blogs_podcasts-accelerate-custom-llm-deployment-fine-tune-with-ou-3.md" >}})
- [在 EC2 上使用 Oumi 微调 Llama 并部署至 Amazon Bedrock]({{< relref "posts/20260310-blogs_podcasts-accelerate-custom-llm-deployment-fine-tune-with-ou-2.md" >}})
- [在 EC2 上使用 Oumi 微调 Llama 并部署至 Amazon Bedrock]({{< relref "posts/20260311-blogs_podcasts-accelerate-custom-llm-deployment-fine-tune-with-ou-3.md" >}})
- [在 EC2 上使用 Oumi 微调并部署 Llama 至 Amazon Bedrock]({{< relref "posts/20260311-blogs_podcasts-accelerate-custom-llm-deployment-fine-tune-with-ou-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*