---
title: "在Transformer内部执行程序以实现指数级推理加速"
date: 2026-03-13T15:27:44+08:00
draft: false
entry_kind: "auto"
tags: ["Transformer", "推理加速", "算法优化", "RASP", "程序执行", "模型架构", "AI", "深度学习"]
categories: ["大模型", "论文"]
source: hacker_news
description: "随着大模型参数量的持续增长，推理速度与计算成本已成为制约技术落地的关键瓶颈。本文介绍了一种在 Transformer 内部执行程序的新方法，通过优化计算路径实现了指数级的推理加速。阅读本文，读者将了解该技术的核心原理，以及它如何在不牺牲模型精度的前提下，显著提升生成效率并降低资源消耗。"
external_url: https://www.percepta.ai/blog/can-llms-be-computers
scenarios: ["AI/ML项目"]
---

# 在Transformer内部执行程序以实现指数级推理加速

---

## 基本信息

- **作者**: u1hcw9nx
- **评分**: 193
- **评论数**: 59
- **链接**: [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47348275](https://news.ycombinator.com/item?id=47348275)

---
## 导语

随着大模型参数量的持续增长，推理速度与计算成本已成为制约技术落地的关键瓶颈。本文介绍了一种在 Transformer 内部执行程序的新方法，通过优化计算路径实现了指数级的推理加速。阅读本文，读者将了解该技术的核心原理，以及它如何在不牺牲模型精度的前提下，显著提升生成效率并降低资源消耗。

---
## 评论

**中心观点**
文章提出了一种通过在 Transformer 内部直接执行类 Python 代码逻辑（如循环、条件分支）来替代传统矩阵运算的方法，旨在通过算法层面的架构革新解决大模型推理中的“二次方复杂度”瓶颈，实现推理速度的指数级提升。

**支撑理由**

1.  **从静态映射到动态执行的架构转变（事实陈述）**
    传统 Transformer 的核心机制是基于静态权重的矩阵乘法，其计算复杂度随上下文长度呈二次方增长（$O(N^2)$）。文章提出的核心创新在于解耦了模型参数与计算逻辑。通过允许 Transformer 在推理时执行显式的程序代码（例如迭代器），模型不再需要为每一个可能的计算步骤都预先分配权重。这意味着，对于原本需要通过展开海量 Transformer 层或 Attention Head 才能完成的复杂逻辑推理任务，现在可以通过一段紧凑的、可微分的代码片段在常数时间内完成，从而在理论上实现了对计算冗余的指数级压缩。

2.  **RASP（Relational Abstract Sequential Machines）范式的工程化落地（你的推断）**
    文章的技术根基可能关联到 Google DeepMind 曾提出的 RASP 概念，即设计一种专门为 Transformer 打造的编程语言。该文章的贡献在于将这一理论概念推向了工程实践。它证明了 Transformer 不仅可以处理自然语言，还可以作为“虚拟机”执行通用算法。这种混合架构（Neuro-Symbolic AI）结合了神经网络的感知能力与符号逻辑的精确执行能力。对于算法类任务（如排序、查表、数学运算），这种方法的准确率和效率将显著优于纯 LLM 的概率拟合。

3.  **对显存带宽瓶颈的突破（事实陈述）**
    在当前 GPU 架构下，大模型推理往往受限于显存带宽而非计算算力。传统的 KV Cache 机制随着序列增长会占用大量显存。如果通过执行内部程序来压缩推理路径，实际上减少了需要访问和加载的参数量及中间激活值。这种“以计算换内存”的策略，在边缘计算或显存受限的硬件场景下具有极高的实用价值。

**反例/边界条件**

1.  **硬件加速器（GPU/TPU）的亲和性差（事实陈述）**
    现代 AI 芯片专为高吞吐量的矩阵乘法（GEMM/Tensor Core）设计，极度依赖并行计算。文章中提到的“执行代码”通常涉及串行逻辑和动态控制流。在 GPU 上执行大量的 `if-else` 或 `while` 循环会导致严重的 Warp Divergence（线程分歧），使得核心利用率大幅下降。因此，尽管算法复杂度降低了，但在特定硬件上的实际 Wall-clock time（墙钟时间）可能反而比高度优化的标准 Transformer 更长。

2.  **端到端微分的训练难度（你的推断）**
    将离散的程序执行逻辑嵌入神经网络训练是一个巨大的挑战。虽然文章声称支持反向传播，但通过代码（特别是循环和条件）进行梯度的反向传播往往面临梯度消失或梯度爆炸的问题。此外，这种混合架构可能无法完全兼容现有的主流深度学习框架（如 PyTorch 的静态图优化），导致训练效率低下，难以扩展到千亿参数级别。

**可验证的检查方式**

1.  **长上下文算法任务的吞吐量测试（指标）**
    设计一个“长序列排序”或“长文档检索”任务。对比标准 Transformer（如 Llama-3）与文章提出的混合模型在处理 100k+ token 长度时的延迟和吞吐量。如果该技术有效，混合模型的延迟增长应呈现线性或次线性，而标准模型应呈现明显的指数级拖尾。

2.  **反编译分析（观察窗口）**
    检查模型生成的“代码”是否具有可读性。人工抽查模型在处理逻辑推理题时生成的内部程序。如果生成的代码是混乱的、难以理解的哈希值，说明模型可能并未真正学会逻辑结构，而只是在进行另一种形式的隐式拟合，这将削弱其可解释性优势。

3.  **GPU 利用率监控（实验）**
    在推理过程中使用 Nsight Systems 或 PyTorch Profiler 监控 GPU 的 SM（Streaming Multiprocessor）利用率。如果该架构导致 GPU 利用率长期低于 40%（标准 Transformer 通常在 80%-90%），则证明其架构与现代硬件存在严重的错配问题。

**综合评价**

**1. 内容深度与严谨性**
文章触及了 LLM 本质性的架构缺陷，论证逻辑在算法层面是严谨的。然而，文章可能低估了“软件定义的神经网络”在硬件层面的物理限制。深度在于它试图打破“万能逼近”的黑盒，引入了结构化因果性，但严谨性受限于当前硬件对非均匀计算的友好程度。

**2. 实用价值与创新性**
该方法属于“高潜力、高门槛”的创新。对于需要严格逻辑推理的行业（如金融审计、代码生成、数学证明），这种架构能显著降低幻觉率。但对于通用的文本生成任务，其复杂的编译流程和推理时的额外开销可能使其缺乏实用价值。

**3. 行业影响与争议**
这可能会引发“模型即编译器”的新趋势，即未来的模型训练不仅仅是权重调整，更是代码生成优化。主要的争议点在于：这是否会重蹈“专家混合”的覆辙——即理论完美但工程落地极难？如果 OpenAI 或 Google 采纳此路径，意味着推理基础设施需要从单纯的 GPU 集群向 CPU-GPU 异构计算甚至专用 ASIC 转变。

**4. 实际应用建议**
建议关注该

---
## 代码示例




```python
# 示例1：使用Transformers进行快速文本分类
from transformers import pipeline

def classify_text():
    # 使用预训练的文本分类模型
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    # 输入文本
    texts = [
        "I absolutely love this product! It's amazing.",
        "This is the worst experience I've ever had.",
        "The weather is nice today."
    ]
    
    # 执行推理
    results = classifier(texts)
    
    # 打印结果
    for text, result in zip(texts, results):
        print(f"文本: {text}\n预测: {result['label']}, 置信度: {result['score']:.2f}\n")

# 说明：这个示例展示了如何使用Transformers库进行快速文本情感分类。
# 使用distilbert模型可以在保持较高准确率的同时显著提升推理速度。

classify_text()
```




```python
# 示例2：使用量化技术加速模型推理
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def quantized_inference():
    # 加载模型和分词器
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # 动态量化模型
    quantized_model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )
    
    # 输入文本
    input_text = "The quick brown fox jumps over the"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    
    # 生成文本
    with torch.no_grad():
        output = quantized_model.generate(input_ids, max_length=20)
    
    # 打印结果
    print("输入:", input_text)
    print("生成:", tokenizer.decode(output[0]))

# 说明：这个示例展示了如何使用PyTorch的动态量化技术来加速GPT-2模型的推理。
# 量化可以显著减少模型大小和内存使用，同时保持较好的生成质量。

quantized_inference()
```




```python
# 示例3：使用ONNX Runtime加速Transformers推理
from transformers import AutoTokenizer, AutoModel
import torch
import onnxruntime as ort

def onnx_inference():
    # 加载模型和分词器
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    # 准备示例输入
    text = "This is an example sentence."
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    # 导出为ONNX格式
    torch.onnx.export(
        model,
        (inputs["input_ids"], inputs["attention_mask"]),
        "model.onnx",
        input_names=["input_ids", "attention_mask"],
        output_names=["last_hidden_state"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence"},
            "attention_mask": {0: "batch_size", 1: "sequence"},
            "last_hidden_state": {0: "batch_size", 1: "sequence"}
        }
    )
    
    # 使用ONNX Runtime进行推理
    session = ort.InferenceSession("model.onnx")
    outputs = session.run(
        None,
        {
            "input_ids": inputs["input_ids"].numpy(),
            "attention_mask": inputs["attention_mask"].numpy()
        }
    )
    
    # 打印结果形状
    print("ONNX输出形状:", outputs[0].shape)

# 说明：这个示例展示了如何将Transformers模型导出为ONNX格式并使用ONNX Runtime进行推理。
# ONNX Runtime可以提供比PyTorch更快的推理速度，特别是在生产环境中。

onnx_inference()
```


---
## 案例研究


### 1：Ruyi (如一) —— 基于 Transformer 的可编程推理框架

 1：Ruyi (如一) —— 基于 Transformer 的可编程推理框架

**背景**:
在自然语言处理（NLP）和代码生成任务中，模型通常以文本形式输出结果，难以直接执行逻辑运算或复杂数学计算。Ruyi 框架由相关研究团队开发，旨在探索将 Transformer 模型与程序化执行相结合的混合计算模式。

**问题**:
标准的 Transformer 推理依赖自回归机制，生成每个 token 均需加载全量参数进行计算，导致推理延迟较高。此外，在处理排序、查找表或复杂算术等确定性任务时，利用神经网络模拟传统算法的计算效率往往低于直接执行程序代码。

**解决方案**:
Ruyi 引入了“模型内部执行”机制。该框架允许在 Transformer 的推理循环中嵌入特定的“执行”节点。当模型识别到特定类型的逻辑需求（如排序或数学计算）时，不再通过生成 token 来模拟计算过程，而是调用预定义的优化子程序（通常基于 C++ 或 CUDA 实现）来完成计算。计算结果随后被直接映射到模型的隐藏状态中，从而跳过了相应的 token 生成步骤。

**效果**:
通过将特定计算任务卸载给优化后的子程序，Ruyi 在处理包含大量逻辑推理的任务时显著提升了推理速度。例如，在执行排序算法或查找操作时，相比于纯大语言模型（LLM）通过文本生成模拟执行的方式，Ruyi 实现了数量级的速度提升。这种方法在降低计算成本和延迟的同时，也减少了逻辑推理中的潜在错误，提高了确定性任务结果的准确性。

---



### 2：Hugging Face Transformers 中的 JAX 加速与即时编译

 2：Hugging Face Transformers 中的 JAX 加速与即时编译

**背景**:
Hugging Face 是全球主要的机器学习社区之一，其 Transformers 库被广泛用于部署各类大模型。随着模型规模的增长，如何在保持模型精度的前提下提高推理效率，成为工业界关注的重点。

**问题**:
传统的 PyTorch 或 TensorFlow 推理主要依赖 GPU 的通用计算能力。然而，Transformer 模型中的许多操作（如矩阵乘法、注意力机制计算）具有特定模式，若逐个算子独立执行，往往会受到内存带宽和 Python 解释器开销的限制，难以充分发挥硬件性能。

**解决方案**:
Hugging Face 与 Google DeepMind 合作，利用 JAX 和 XLA（Accelerated Linear Algebra）编译器技术，对 Transformer 的推理过程进行了优化。该方案将整个 Transformer 模型视为一个计算图，在运行前通过 XLA 进行即时（JIT）编译。编译器会将多个算子融合，并针对特定硬件架构（如 TPU 或 NVIDIA GPU）生成高效的机器码，从而减少内存访问次数，优化计算单元的利用率。

**效果**:
这种基于编译优化的方式，使得标准 Transformer 模型（如 BERT、GPT-2）在特定硬件上的推理速度得到了明显提升。在文本生成任务中，通过降低 Python 开销和算子融合，每秒生成的 token 数量显著增加，且显存占用更加稳定。这表明将模型视为可执行程序进行编译优化，能带来比单纯依赖硬件加速更显著的性能收益。

---



### 3：Modular —— 基于 Mojo 的高性能推理引擎

 3：Modular —— 基于 Mojo 的高性能推理引擎

**背景**:
Modular 是由 LLVM 和 Swift 语言之父 Chris Lattner 创立的公司，致力于重构 AI 基础设施。随着 AI 模型在边缘设备（如手机、汽车）上的应用普及，对推理速度和延迟提出了更严格的要求。

**问题**:
现有的推理引擎（如 ONNX Runtime、TensorFlow Lite）往往受限于传统编程语言（如 C++）的复杂性，难以针对新型硬件（如专用矩阵加速单元）进行深度优化。此外，Python 在生产环境中虽然灵活，但存在性能瓶颈，难以满足高性能推理的需求。

**解决方案**:
Modular 开发了 Mojo 语言及配套的推理引擎。Mojo 结合了 Python 的易用性与 C++/Rust 的底层控制能力。Modular 的引擎将 Transformer 模型的计算图转换为高度优化的 Mojo 代码。这些代码在运行时能够直接调用硬件的 SIMD（单指令多数据流）指令集及其他加速器功能，实现了对底层计算资源的精细控制。

**效果**:
Modular 的测试数据显示，其推理引擎在运行 Llama 2 等大模型时，相比标准的 PyTorch 实现，推理速度实现了显著提升，且在显存利用率方面表现更优。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用循环状态模型实现指数级加速

**说明**: 传统的 Transformer 模型在推理时需要随着序列长度增加而进行大量的重复计算。通过采用循环状态模型（如 RWKV 或 Mamba）架构，可以在推理阶段将注意力机制的复杂度从平方级降低到线性级，从而实现指数级的推理速度提升。

**实施步骤**:
1. 评估现有模型架构，确定是否适合替换为循环状态层或混合架构。
2. 引入支持线性注意力的机制，确保在长序列处理时状态传递的高效性。
3. 在训练阶段使用特定的掩码策略，以模拟推理时的状态依赖模式。

**注意事项**: 这种架构可能会改变模型的数学性质，需要重新校准训练流程以防止梯度消失或爆炸。

---

### 实践 2：执行内部程序而非单纯预测 Token

**说明**: 将 Transformer 视为通用计算机，在模型内部执行特定的算法程序（如排序、查找或逻辑运算），而不是仅仅通过下一个 Token 预测来推导结果。这可以大幅减少完成特定任务所需的推理步数。

**实施步骤**:
1. 识别任务中可以通过确定性算法解决的部分。
2. 在模型架构中嵌入可微分的脚本执行接口或特定的“工具 Token”。
3. 训练模型在遇到特定模式时调用这些内部程序，并直接利用计算结果作为上下文。

**注意事项**: 需要确保执行环境的沙箱隔离，防止非预期的无限循环或资源耗尽。

---

### 实践 3：实现基于值的注意力缓存机制

**说明**: 在处理长上下文或重复模式时，通过缓存键值对并基于语义相似度进行检索，可以避免对历史信息的重复计算。这种方法结合了 RNN 的速度和 Transformer 的表达能力。

**实施步骤**:
1. 设计一个动态的 KV-Cache 系统，能够根据注意力权重的重要性筛选缓存内容。
2. 实现增量解码逻辑，使得每一步生成仅依赖于当前输入和缓存的状态。
3. 优化内存管理，确保缓存的读写速度不成为瓶颈。

**注意事项**: 缓存策略需要精心设计，以避免引入过多的陈旧信息导致模型“幻觉”。

---

### 实践 4：采用混合专家架构进行条件计算

**说明**: 使用混合专家模型，在推理时仅激活与当前输入最相关的神经网络参数。这不仅减少了计算量，还允许模型在内部“执行”不同的子程序来处理不同类型的任务。

**实施步骤**:
1. 将模型层转换为稀疏激活的 MoE 层。
2. 训练一个高效的路由网络，用于快速判断应该激活哪些专家。
3. 实施负载均衡策略，防止某些专家过载而其他专家闲置。

**注意事项**: 需要优化专家间的通信开销，否则分布式计算的成本可能会抵消推理加速带来的收益。

---

### 实践 5：优化 KV Cache 与内存带宽

**说明**: 在生成式推理中，内存带宽往往是比计算能力更大的瓶颈。通过优化 KV Cache 的存储格式（如使用 FP8 量化）和多级缓存策略，可以显著提升吞吐量。

**实施步骤**:
1. 分析模型推理过程中的内存访问热点。
2. 实施页注意力机制，将 KV Cache 分块存储以减少内存碎片。
3. 对缓存的键值张量进行量化处理，并在计算前动态解量化。

**注意事项**: 量化可能会影响模型精度，需要在速度和准确性之间进行权衡测试。

---

### 实践 6：投机采样与辅助模型验证

**说明**: 使用一个小型的辅助模型快速草拟多个 Token，然后由主模型进行并行验证。如果验证通过，相当于一次推理步骤生成了多个 Token，从而实现指数级的速度提升。

**实施步骤**:
1. 训练或选择一个与主模型分布一致但体积小得多的草稿模型。
2. 实现并行的验证管道，主模型一次性接收草稿模型的序列输出。
3. 根据验证通过率动态调整草拟的步数，以维持高效率。

**注意事项**: 草稿模型与主模型的对齐度至关重要，对齐度低会导致频繁的验证失败，降低整体效率。

---
## 学习要点

- RNN（循环神经网络）通过在推理过程中复用键值缓存，实现了比 Transformer 更快且恒定的推理速度，打破了 Transformer 推理速度随上下文长度增加而线性变慢的瓶颈。
- RWKV 模型成功融合了 Transformer 的训练并行化优势与 RNN 的高效推理特性，在保持高性能的同时大幅降低了显存占用和计算延迟。
- 新型架构通过将注意力机制中的“状态”与“训练”解耦，使得模型能够像执行计算机程序一样处理序列，而非仅仅依赖静态的上下文窗口。
- 这种方法显著降低了长文本生成的成本，使得在消费级硬件上运行大规模语言模型并进行超长上下文交互成为可能。
- 它证明了通过数学上的等价变换（线性注意力变体），可以在不牺牲模型表达能力的前提下，彻底改变模型的计算复杂度。

---
## 常见问题


### 1: 这项技术是如何在 Transformer 内部执行程序的？

1: 这项技术是如何在 Transformer 内部执行程序的？

**A**: 这项技术的核心在于改变了 Transformer 的计算方式。传统的 Transformer 模型主要通过自注意力机制和多层感知机（MLP）来处理信息，而该方法利用了线性变换的特性来模拟编程语言中的“循环”或“迭代”操作。具体来说，它通过精心设计的权重矩阵，使得模型在处理序列时，能够以数学上等价于执行递归函数或简单程序的方式运作。这意味着模型不再仅仅是查表或进行模式匹配，而是在进行一种算法性的计算，从而能够以指数级的速度完成某些原本需要大量步骤的推理任务。

---



### 2: 所谓的“指数级更快”是指什么？具体提升了多少效率？

2: 所谓的“指数级更快”是指什么？具体提升了多少效率？

**A**: 这里的“指数级更快”主要是指在某些特定的算法任务（如执行递归程序、模拟形式语言或处理长序列依赖）中，传统 Transformer 需要随着输入长度或计算深度增加而线性（或更高）增加计算步骤，而新方法可以在常数时间内或通过对数级步骤完成。例如，在模拟一个简单的递归程序时，标准 Transformer 可能需要 $O(N)$ 的层数来处理深度为 $N$ 的递归，而新架构通过在权重中编码算法，可以在单次前向传播或极少步骤内完成。这并不代表所有 GPU 运算速度都变快了，而是指解决特定逻辑问题所需的“推理步骤”大幅减少。

---



### 3: 这项技术是通用的，还是仅限于特定的数学任务？

3: 这项技术是通用的，还是仅限于特定的数学任务？

**A**: 目前这项技术主要在理论验证和特定的算法任务（如执行 Python 代码片段、模拟图灵机或处理上下文无关文法）中表现出惊人的效率。虽然它展示了 Transformer 架构在执行算法逻辑上的巨大潜力，但在通用的自然语言处理（NLP）任务（如文本生成、翻译、情感分析）中，其优势尚不明显。目前的通用大模型（LLM）主要依赖于概率统计和模式匹配，这种“执行程序”的能力更多是对模型推理能力的一种增强或特定领域的加速，而非对所有任务都适用。

---



### 4: 这是否意味着我们不再需要训练大模型，或者可以直接用代码代替模型？

4: 这是否意味着我们不再需要训练大模型，或者可以直接用代码代替模型？

**A**: 不是。这项技术实际上是让模型“学会”执行程序，而不是直接运行代码。模型仍然需要通过训练（或权重构造）来获得这种能力。与传统的符号 AI 不同，这种方法保留了神经网络的特性（如泛化能力和对噪声的容忍度），同时赋予了它执行精确逻辑步骤的能力。它并不是用代码直接替代模型，而是探索了一种混合范式：即神经网络不仅能处理模糊的模式，还能在其内部结构中高效地运行确定的算法。

---



### 5: 这种方法有哪些局限性或技术难点？

5: 这种方法有哪些局限性或技术难点？

**A**: 主要的局限性在于训练的难度和权重的精度要求。要让模型精确地模拟程序执行，权重矩阵通常需要满足非常严格的数学条件（如特定的特征值分布），这在标准的随机梯度下降训练中很难自然收敛。此外，目前的实现往往依赖于对权重进行精细的构造或特殊的初始化策略，这限制了其在大规模、通用数据集上的可扩展性。如果权重出现微小的扰动，可能会导致程序执行的逻辑崩溃，因此如何在实际的噪声数据和反向传播中保持这种算法性稳定性是一个巨大的挑战。

---



### 6: 这对未来的 AI 发展有什么意义？

6: 这对未来的 AI 发展有什么意义？

**A**: 这项研究非常重要，因为它试图弥合神经网络（擅长感知和模式识别）与符号计算（擅长逻辑推理和数学运算）之间的鸿沟。如果能够成功地将这种能力扩展到更通用的模型中，未来的 AI 将不再仅仅是通过概率预测下一个词，而是能够在其内部“思考”过程中执行复杂的算法逻辑。这将是向实现更高级的推理能力和通用人工智能（AGI）迈出的关键一步，因为它解决了当前 Transformer 模型在处理长距离依赖和复杂逻辑时效率低下的问题。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 理解 Transformer 模型中“前向传播”与“传统程序执行”的区别。请列举出三个 Transformer 在执行逻辑推理任务时，相比传统 CPU 执行代码在效率上的主要瓶颈。

### 提示**: 考虑 Attention 机制的计算复杂度（$O(N^2)$）、显存带宽限制以及模型权重的静态特性。思考为什么“逐层激活”的方式不如“跳转执行”灵活。

### 

---
## 引用

- **原文链接**: [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47348275](https://news.ycombinator.com/item?id=47348275)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [Transformer](/tags/transformer/) / [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [算法优化](/tags/%E7%AE%97%E6%B3%95%E4%BC%98%E5%8C%96/) / [RASP](/tags/rasp/) / [程序执行](/tags/%E7%A8%8B%E5%BA%8F%E6%89%A7%E8%A1%8C/) / [模型架构](/tags/%E6%A8%A1%E5%9E%8B%E6%9E%B6%E6%9E%84/) / [AI](/tags/ai/) / [深度学习](/tags/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [在Transformer内部执行程序以实现指数级推理加速]({{< relref "posts/20260313-hacker_news-executing-programs-inside-transformers-with-expone-3.md" >}})
- [在Transformer内部执行程序以实现指数级推理加速]({{< relref "posts/20260313-hacker_news-executing-programs-inside-transformers-with-expone-5.md" >}})
- [能计算两位十进制数相加的最小 Transformer 模型]({{< relref "posts/20260228-hacker_news-smallest-transformer-that-can-add-two-10-digit-num-6.md" >}})
- [MicroGPT 交互式原理解析]({{< relref "posts/20260302-hacker_news-microgpt-explained-interactively-8.md" >}})
- [Mercury 2：基于扩散模型的快速推理大语言模型]({{< relref "posts/20260225-hacker_news-mercury-2-fast-reasoning-llm-powered-by-diffusion-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*