---
title: 利用vLLM在SageMaker AI与Bedrock上高效托管多LoRA模型
date: 2026-02-26 20:32:57+08:00
draft: false
entry_kind: auto
tags:
- vLLM
- LoRA
- SageMaker
- Bedrock
- MoE
- 模型推理
- 模型微调
- 内核优化
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 本文介绍了如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 高效服务数十个微调模型。文章详细阐述了针对混合专家模型实现多
  LoRA 推理的方法，描述了内核级别的优化措施，并以 GPT-OSS 20B 为例展示了该工作的实际效益。
external_url: https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock
scenarios:
- 大语言模型
---

# 利用vLLM在SageMaker AI与Bedrock上高效托管多LoRA模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T20:56:13+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)

---

## 摘要/简介

在本文中，我们将解释我们如何在 vLLM 中为混合专家（MoE）模型实现多 LoRA 推理，描述我们在内核层面所做的优化，并展示如何从中受益。本文将全程以 GPT-OSS 20B 为主要示例。

---

## 导语

随着大模型应用场景的细分，同时部署数十个微调模型往往面临高昂的资源成本与延迟挑战。本文将深入探讨如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 实现多 LoRA 推理，并解析针对混合专家（MoE）模型的内核级优化细节。通过阅读本文，您将掌握以 GPT-OSS 20B 为例的具体实践，从而在保证性能的前提下，显著提升模型服务的吞吐效率与资源利用率。

---

## 摘要

本文介绍了如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 高效服务数十个微调模型。文章详细阐述了针对混合专家模型实现多 LoRA 推理的方法，描述了内核级别的优化措施，并以 GPT-OSS 20B 为例展示了该工作的实际效益。

---

## 评论

**中心观点**
该文章阐述了通过在 vLLM 中实现 Multi-LoRA 服务与内核级优化，并结合 Amazon SageMaker/Bedrock 的基础设施，从而在单一 GPU 实例上高效托管数十个微调模型，旨在解决大模型规模化部署中成本与延迟的结构性矛盾。

**支撑理由与深度评价**

**1. 架构层面的资源集约化（事实陈述 + 作者观点）**
文章的核心技术路径是利用 LoRA（Low-Rank Adaptation）的特性，即冻结基础模型权重，仅通过微小的适配器层注入特定领域知识。
*   **深度分析**：从技术角度看，这解决了“一任务一模型”带来的巨大显存冗余。传统的部署方式下，部署 10 个 20B 参数的模型需要数百 GB 的显存，而通过共享 Base Model 并动态加载 LoRA 适配器，显存占用大幅降低。文章提到的“Multi-LoRA Serving”不仅是逻辑上的隔离，更是物理显存的复用，这是该方案具有商业价值的技术基石。
*   **边界条件/反例**：这种高效性极度依赖于 LoRA 适配器的体积。如果微调任务需要对全量参数或大量层进行大幅调整（例如跨领域的剧烈知识迁移），LoRA 的低秩假设可能失效，导致模型效果下降，此时强行使用 LoRA 架构会牺牲模型质量以换取部署效率。

**2. 内核级优化与 PagedAttention 的工程实践（事实陈述 + 你的推断）**
文章强调了“kernel-level optimizations”，这通常涉及 CUDA 算子的融合与显存管理机制的改进。
*   **深度分析**：vLLM 的核心竞争力在于 PagedAttention（分页注意力），该技术借鉴了操作系统的虚拟内存管理，解决了 KV Cache（键值缓存）碎片化问题。在 Multi-LoRA 场景下，不同请求的上下文长度差异极大，极易导致显存浪费。文章隐含的观点是：通过内核优化，可以最小化不同 LoRA 请求切换时的调度开销。这不仅是算法的胜利，更是系统工程（System Engineering）的胜利，表明 AI 推理已进入“精耕细作”的阶段。
*   **边界条件/反例**：内核级别的优化往往与硬件强耦合。vLLM 的优化主要针对 NVIDIA GPU（特别是 Ampere 和 Hopper 架构）。如果用户在非 NVIDIA 硬件（如 AMD ROCm 或 AWS Trainium/Inferentia）上运行，这些特定的内核优化可能无法直接迁移，性能提升将大打折扣。

**3. 云原生生态的战略捆绑（事实陈述 + 你的推断）**
文章特意强调了在 Amazon SageMaker AI 和 Bedrock 上的实现。
*   **深度分析**：从行业角度看，这展示了云厂商“模型+基础设施”的垂直整合能力。Bedrock 提供了托管服务的便利性，屏蔽了底层 vLLM 的复杂性，使得企业无需维护 MLOps 团队即可使用 MoE 能力。这实际上是在推销一种“Serverless MoE”的愿景。
*   **边界条件/反例**：这种深度绑定带来了供应商锁定风险。虽然 vLLM 是开源的，但在 SageMaker 上部署的具体 Docker 镜像、启动脚本及与 Bedrock 的对接逻辑是专有的。如果企业需要将 workload 迁移回私有云或其他公有云，迁移成本可能不低，且可能失去 Bedrock 提供的特定企业级功能（如 Fine-grained access control）。

**4. MoE（混合专家）架构的重新定义（作者观点）**
文章使用 GPT-OSS 20B 作为示例，并将 Multi-LoRA 服务与 MoE 模型联系起来。
*   **深度分析**：这里存在一个概念上的微妙转换。传统的 MoE（如 Mixtral 8x7B）是指模型内部的稀疏激活层。而本文描述的架构更接近于“宏观层面的 MoE”，即路由层将用户请求分发至不同的 LoRA 适配器。这种“LoRA as a Service”的架构，实际上是将 MoE 的粒度从“神经元”提升到了“模型实例”。
*   **边界条件/反例**：这种架构的瓶颈在于路由策略。如果路由逻辑过于简单（例如仅基于 API 路径），则无法利用模型间的互补性；如果路由是一个上层的神经网络模型，则又会引入额外的推理延迟和故障点。

**实际应用建议与验证方式**

**1. 检查方式与指标**
*   **显存利用率监控**：在部署多个 LoRA 时，观察 GPU Memory Usage。如果随着 LoRA 数量增加，显存呈线性甚至亚线性增长，说明共享机制生效；如果呈指数级增长，说明可能发生了显存泄漏或未正确共享 Base Model。
*   **首字节延迟（TTFT）测试**：在并发请求不同 LoRA 模型时，测量 TTFT。如果频繁出现毛刺，说明可能在 Kernel 切换或 KV Cache 分配上存在竞争条件。
*   **吞吐量衰减曲线**：逐步增加并发请求数，记录 Tokens/Second 的变化。观察在达到瓶颈前，性能是否保持平稳。

**2. 综合评价**
*   **内容深度**：文章在工程实现上具备较高深度，特别是对 vLLM 内部机制的利用，但在理论算法层面的创新较少。
*   **实用价值**：极高。对于多租户 SaaS 应用或需要同时服务多个垂直领域的企业，这是降本增效的必经之路。
*   **创新性**：属于工程集成创新，将开源框架与云

---

## 技术分析

以下是对文章《Efficiently serve dozens of fine-tuned models with vLLM on Amazon SageMaker AI and Amazon Bedrock》的深入分析。

---

### 深度分析报告：基于 vLLM 的高效多 LoRA 推理服务

### 1. 核心观点深度解读

**主要观点与核心思想**
文章的核心观点在于：**通过在 vLLM 框架中实现针对混合专家模型的多 LoRA（Low-Rank Adaptation）动态推理服务，可以打破“一个模型对应一个部署实例”的传统资源限制，从而在单一 GPU 实例上高效、低成本地同时服务数十个微调模型。**

作者传达的核心思想是“**共享与隔离的统一**”。在传统的 AI 部署中，如果你有 50 个针对不同客户或任务微调的模型（例如基于 GPT-NeoX 20B），你需要部署 50 个常驻模型实例，这带来了巨大的显存和计算成本。文章提出，利用 MoE（混合专家）架构的思想，将 LoRA 权重视为“专家”，在推理时动态加载到基础模型中，实现了基础模型参数的共享与任务特定参数（LoRA）的按需调度。

**观点的创新性与重要性**
*   **创新性**：将 LoRA 技术从单纯的“微调手段”提升为“服务形态”。通常 LoRA 用于节省训练显存，而文章将其用于解决**推理侧的规模化部署难题**。此外，文章强调了**内核级优化**，解决了多 LoRA 并发请求时的显存碎片和计算调度瓶颈。
*   **重要性**：随着企业级 AI 落地，千人千面的定制化模型需求激增。如果每个定制模型都需要独占一张 A100/H100，成本将不可控。该方案直接降低了 SaaS 平台和企业内部 AI 中台运营大模型的边际成本，使得“为每个用户提供专属微调模型”在商业上变得可行。

### 2. 关键技术要点

**涉及的关键技术**
*   **vLLM**：一个具有高吞吐量和显存管理效率的 LLM 推理引擎，核心技术是 PagedAttention。
*   **LoRA (Low-Rank Adaptation)**：通过冻结基础模型权重，仅注入低秩矩阵来适应特定任务。
*   **MoE (Mixture of Experts) 推理范式**：借鉴 MoE 的路由机制，将不同的 LoRA 视为不同的专家，根据请求动态选择激活哪个 LoRA。
*   **GPT-OSS 20B**：作为基础模型示例，这是一个 200 亿参数的开源模型，对显存要求较高。

**技术原理与实现方式**
1.  **权重融合**：在推理计算 Attention 或 FFN 层时，公式为 $y = (W_{base} + \Delta W) x$。其中 $\Delta W = BA$（LoRA 的低秩分解）。vLLM 需要在 Kernel 层面高效地完成 $W_{base}x$ 和 $BAx$ 的加法。
2.  **动态显存管理**：利用 vLLM 的 PagedAttention 机制，将 LoRA 权重也视为可分页的 KV Cache 类似的资源。当请求 A（需要 LoRA-1）和请求 B（需要 LoRA-2）同时到达时，系统动态调度 GPU 显存，加载对应的 LoRA 权重。
3.  **批处理优化**：难点在于同一个 Batch 内可能包含需要不同 LoRA 的请求。文章提到的内核级优化允许在同一个 GPU Kernel 启动中处理多个不同的 LoRA 组，而不是串行处理。

**技术难点与解决方案**
*   **难点**：多 LoRA 服务会导致显存碎片化；频繁的权重加载可能导致延迟增加；Batch 内的计算密度不均（有的请求长，有的短）。
*   **解决方案**：
    *   **预分配与缓存**：将热门 LoRA 权重常驻显存。
    *   **自定义 CUDA Kernel**：优化了 GEMM（矩阵乘法）操作，使得在计算 $W_{base}$ 的同时，能以极低开销叠加计算 $\Delta W$，避免了多次 Kernel 启动的开销。

### 3. 实际应用价值

**指导意义与场景**
*   **场景**：
    *   **SaaS 多租户平台**：一家提供 AI 写作助手的公司，为不同行业（医疗、法律、金融）提供不同风格的模型。
    *   **企业私有化部署**：企业内部不同部门（HR、财务、研发）共用一个基座模型，但挂载各自的微调权重。
    *   **A/B 测试**：同时运行同一个模型的 10 个不同微调版本，测试哪个效果最好。
*   **指导意义**：它证明了不需要为了服务特定任务而牺牲基础模型的通用性，也不需要为此牺牲数倍的硬件成本。

**需要注意的问题**
*   **基础模型版本必须一致**：所有 LoRA 必须基于同一个 Base Model Checkpoint 微调而来。
*   **显存容量限制**：虽然比部署 N 个模型省资源，但如果并发请求涉及的 LoRA 种类过多，显存仍可能成为瓶颈（需要存储所有活跃 LoRA 的权重）。
*   **延迟抖动**：如果某个 LoRA 权重不在显存中，需要从 CPU 内存加载，首次请求延迟会较高。

### 4. 行业影响分析

**对行业的启示**
*   **MaaS (Model as a Service) 的精细化运营**：云厂商（如 AWS Bedrock）可以不再只提供几个大模型，而是提供“基座模型 + 模型商店（LoRA Hub）”的模式。用户上传自己的 LoRA，云端动态挂载。
*   **推理架构的演进**：传统的推理引擎（如 Triton, TorchServe）主要解决模型生命周期管理，而 vLLM 这种针对 Transformer 架构深度优化的引擎，正在定义下一代 AI 基础设施的标准。
*   **边缘计算的潜力**：虽然文章主要讲云端，但这种技术下沉到边缘设备（如自动驾驶、机器人）同样重要，即在有限算力下支持多任务切换。

**发展趋势**
*   **推理与训练的界限模糊**：LoRA 本质上是训练的产物，但其应用变成了推理时的动态组件。
*   **Serverless 推理的普及**：多 LoRA 服务是实现 Serverless GPU 推理的关键技术之一，因为请求来了才挂载权重，极其适合按需计费。

### 5. 延伸思考

**引发的思考**
*   **LoRA 的安全性**：如果所有用户的 LoRA 都在同一个显存空间中调度，是否存在侧信道攻击的风险？（即通过计时攻击推断出其他用户的 LoRA 权重）。
*   **路由策略的智能化**：目前是基于用户指定 LoRA。未来是否可以引入一个“路由模型”，自动判断用户的 Prompt 应该由哪个 LoRA 来处理？（即 Auto-MoE）。
*   **全参数微调的替代性**：LoRA 虽好，但对于某些需要大幅度改变模型能力的任务（例如学习一门新语言），LoRA 的容量可能不足。多 LoRA 服务是否能支持混合 Adapter（如 LoRA + Full Finetune 部分层）？

**未来方向**
*   **跨基础模型的 LoRA**：如果基础模型升级了（例如从 Llama 2 升级到 Llama 3），旧的 LoRA 能否复用或低成本迁移？
*   **量化感知的多 LoRA**：在 4bit 量化模型上运行多 LoRA 是一个巨大的挑战，也是降本的关键。

### 7. 案例分析

**成功案例逻辑推演**
*   **场景**：一家跨国企业内部的 AI 助手。
*   **背景**：该企业有 50 个子公司，每个子公司有自己的行话和知识库。
*   **传统做法**：部署 50 个 Sagemaker Endpoint，使用 `ml.g5.12xlarge` 实例。成本：$50 \times \$4/hr = \$200/hr$。
*   **多 LoRA 方案**：部署 1 个 Endpoint，加载 1 个 Base Model + 50 个 LoRA Adapter。成本：$1 \times \$4/hr + 少量显存开销$。
*   **结果**：成本降低 98%，且管理复杂度大幅下降（只需维护一个 Base Model 的版本）。

**潜在失败反思**
*   **失败场景**：如果这 50 个任务差异极大（例如一个是写代码，一个是医疗诊断，一个是情感陪聊），单一的 Base Model 可能无法通过简单的 LoRA 覆盖所有领域，导致效果下降。此时强行合并反而会损害用户体验。

### 8. 哲学与逻辑：论证地图

**中心命题**
通过在 vLLM 中实现多 LoRA 动态服务，企业可以在不牺牲推理性能的前提下，以接近单一模型的成本服务海量定制化模型，从而实现 AI 应用的规模化落地。

**支撑理由与依据**
1.  **资源复用**：基础模型参数占据显存的 90% 以上，LoRA 仅占极小部分。
    *   *依据*：参数量级对比（20B 模型 vs 20B x 0.01% LoRA）。
2.  **计算效率**：vLLM 的 PagedAttention 和自定义 Kernel 优化了显存访问和计算调度。
    *   *依据*：vLLM 官方 Benchmark 显示其吞吐量是 HuggingFace Transformers 的数倍。
3.  **MoE 架构的适配性**：Transformer 架构天然适合通过 Adapter 模式进行功能扩展。
    *   *依据*：Google 和 Mixtral 的 MoE 模型在业界的效果验证。

**反例与边界条件**
1.  **显存带宽瓶颈**：如果 LoRA 数量极其庞大（如数千个），且请求极其随机，导致频繁在 CPU-GPU 间搬运权重，PCIe 带宽将成为瓶颈，导致性能崩塌。
2.  **任务冲突**：如果不同 LoRA 需要完全不同的系统提示词或解码策略，单一服务实例难以协调。

---

## 最佳实践

### 实践 1：利用 vLLM 的连续批处理和 PagedAttention 技术

**说明**:
vLLM 的核心优势在于其高性能的推理引擎。通过使用连续批处理，vLLM 可以在同一个批次中同时处理处于不同生成阶段的请求，从而显著提高 GPU 的利用率。结合 PagedAttention 技术，可以将 KV 缓存像操作系统管理内存一样进行分页管理，有效减少内存碎片，提高显存使用效率，特别是在处理长文本或高并发请求时效果显著。

**实施步骤**:
1. 在构建 SageMaker 推理容器或 Bedrock 自定义模型导入作业时，确保使用官方支持或优化过的 vLLM Docker 镜像。
2. 在启动参数中启用连续批处理（通常在 vLLM 中默认开启，需确认未禁用）。
3. 根据模型大小和 GPU 显存，合理配置 `gpu_memory_utilization` 参数（建议设置为 0.9 左右），为 PagedAttention 预留足够空间。

**注意事项**:
- 需要根据具体的实例类型（如 `ml.g5` 或 `ml.p4d`）调整显存利用率，避免 OOM（显存溢出）错误。
- 监控推理吞吐量和延迟，以验证连续批处理带来的性能提升。

---

### 实践 2：采用多实例部署与动态负载均衡

**说明**:
为了高效服务数十个微调模型，单一实例往往难以承载所有模型的加载和并发请求。最佳实践是利用 SageMaker 的多实例自动扩缩容或 Bedrock 的基础模型管理能力，将不同的模型部署在不同的实例组上，或者利用多模型服务功能。通过配置动态负载均衡，将请求路由到负载较低的实例，确保高可用性和低延迟。

**实施步骤**:
1. 在 SageMaker 中，为不同的微调模型配置独立的终端节点，或者使用 SageMaker Multi-Model Endpoints (MME) 加载 vLLM 兼容的模型。
2. 设置自动扩缩容策略，基于 CPU/GPU 利用率或请求数量动态调整实例数量。
3. 使用 Application Load Balancer (ALB) 或 SageMaker 的路由策略将流量分发至不同的模型终端节点。

**注意事项**:
- 冷启动时间：如果使用 MME 或按需扩容，模型加载可能需要时间，需评估业务对延迟的容忍度。
- 成本控制：多实例部署会增加成本，建议在非高峰期自动缩减实例数量。

---

### 实践 3：优化模型量化以降低显存占用

**说明**:
微调模型通常保留了全精度的权重，这会占用大量显存，限制了在单张 GPU 上部署的模型数量或并发能力。使用量化技术（如 AWQ、GPTQ 或 vLLM 原生支持的量化格式）可以将模型转换为 4-bit 或 8-bit 格式，在几乎不损失模型精度的情况下，大幅减少显存占用，从而在单个 GPU 上加载更多模型或处理更大的上下文窗口。

**实施步骤**:
1. 在模型训练完成后或部署前，使用量化工具（如 AutoGPTQ 或 vLLM 内置量化脚本）将模型权重转换为 AWQ 或 GPTQ 格式。
2. 在 vLLM 启动命令中指定量化格式和配置文件。
3. 在测试环境中验证量化后的模型输出质量与性能指标。

**注意事项**:
- 并非所有模型架构都完美支持量化，需提前验证兼容性。
- 量化可能会轻微影响模型精度，对于对准确性要求极高的任务，需进行充分的 A/B 测试。

---

### 实践 4：配置高效的张量并行 (Tensor Parallelism) 策略

**说明**:
对于参数量较大的模型（如 70B+），单个 GPU 的显存可能无法容纳。vLLM 提供了优秀的张量并行（TP）支持，可以将模型切分到多个 GPU 上运行。正确配置 TP 策略不仅能让大模型跑起来，还能通过多 GPU 并行计算提升推理速度。在 SageMaker 上选择 `ml.g5.12xlarge` 或 `ml.p4d.24xlarge` 等多 GPU 实例是实施此策略的基础。

**实施步骤**:
1. 根据模型大小选择合适的实例类型（例如，70B 模型通常需要 4 张或 8 张 A10 或 A100 GPU）。
2. 在 vLLM 启动参数中设置 `tensor_parallel_size`（TP size），使其等于实例拥有的 GPU 数量。
3. 确保网络带宽足够高（如使用 AWS 的 EFA 或实例内部的高速互联），以减少多 GPU 通信带来的延迟。

**注意事项**:
- 张量并行会增加通信开销，对于小模型，单 GPU 或多实例并行可能比单实例多 GPU 更高效。
- 确保 vLLM 版本与底层 CUDA 和 PyTorch 版本兼容，以获得最佳并行性能。

---

## 学习要点

- vLLM 与 Amazon SageMaker AI 及 Bedrock 的集成实现了数十个微调模型的高效并发服务，显著降低了多模型部署的延迟和资源成本。
- vLLM 的连续批处理和 PagedAttention 技术优化了 GPU 显存管理，在提升吞吐量的同时保持了极低的推理延迟。
- 利用 Amazon SageMaker 的多模型端点功能，可以在单一基础设施上动态加载和切换不同的微调模型，极大简化了运维复杂度。
- 通过 Amazon Bedrock 提供的完全托管服务，企业无需管理底层基础设施即可通过 API 调用高性能的定制模型。
- 该解决方案通过将模型计算与存储分离，实现了跨不同微调模型（如 LoRA 适配器）的快速切换和灵活部署。
- 在该架构中应用多轮对话和长上下文处理能力，确保了在复杂业务场景下微调模型的高性能表现。
- 这种云原生的部署策略为企业在保持私有数据安全的前提下，规模化落地生成式 AI 应用提供了标准路径。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [vLLM](/tags/vllm/) / [LoRA](/tags/lora/) / [SageMaker](/tags/sagemaker/) / [Bedrock](/tags/bedrock/) / [MoE](/tags/moe/) / [模型推理](/tags/%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86/) / [模型微调](/tags/%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83/) / [内核优化](/tags/%E5%86%85%E6%A0%B8%E4%BC%98%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [在 SageMaker AI 与 Bedrock 上利用 vLLM 高效部署多 LoRA 模型]({{< relref "posts/20260225-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-0.md" >}})
- [利用vLLM在SageMaker与Bedrock上高效部署多LoRA及MoE模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-1.md" >}})
- [在 SageMaker 与 Bedrock 上利用 vLLM 实现多 LoRA 推理及内核优化]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-11.md" >}})
- [在 SageMaker AI 与 Amazon Bedrock 上使用 vLLM 高效部署多 LoRA 模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-4.md" >}})
- [在SageMaker AI与Bedrock上利用vLLM高效部署多LoRA及MoE模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-3.md" >}})
