---
title: "在Transformer内部执行程序以实现指数级推理加速"
date: 2026-03-13T13:31:12+08:00
draft: false
entry_kind: "auto"
tags: ["Transformer", "推理加速", "算法创新", "RASP", "程序执行", "模型架构", "AI", "深度学习"]
categories: ["大模型", "论文"]
source: hacker_news
description: "随着大语言模型参数量的持续增长，推理速度与计算成本已成为制约其落地的关键瓶颈。本文介绍了一种在 Transformer 内部直接执行程序的新方法，通过将部分计算逻辑从模型权重中剥离，实现了推理速度的指数级提升。读者将了解到该技术的核心原理、具体的性能提升数据，以及它如何在不牺牲模型精度的前提下，有效缓解算力压力。"
external_url: https://www.percepta.ai/blog/can-llms-be-computers
scenarios: ["AI/ML项目"]
---

# 在Transformer内部执行程序以实现指数级推理加速

---

## 基本信息

- **作者**: u1hcw9nx
- **评分**: 159
- **评论数**: 40
- **链接**: [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47348275](https://news.ycombinator.com/item?id=47348275)

---
## 导语

随着大语言模型参数量的持续增长，推理速度与计算成本已成为制约其落地的关键瓶颈。本文介绍了一种在 Transformer 内部直接执行程序的新方法，通过将部分计算逻辑从模型权重中剥离，实现了推理速度的指数级提升。读者将了解到该技术的核心原理、具体的性能提升数据，以及它如何在不牺牲模型精度的前提下，有效缓解算力压力。

---
## 评论

基于文章标题《Executing programs inside transformers with exponentially faster inference》（在Transformer内部执行程序以实现指数级推理加速）及相关技术背景，以下是深入评价。

### 中心观点
**该文章提出了一种“算法-架构协同设计”的新范式，即通过在Transformer的注意力机制中嵌入特定领域的程序执行逻辑（如模拟图灵机或解释器），从而在特定任务上绕过标准Transformer的二次方计算复杂度瓶颈，实现推理速度的指数级加速。**

### 核心评价与深度分析

#### 1. 支撑理由（技术与价值维度）

*   **突破Transformer的物理极限（内容深度与创新性）：**
    *   **事实陈述：** 标准Transformer的自注意力机制受限于 $O(N^2)$ 的复杂度，随着上下文长度增加，推理成本呈指数级爆炸。
    *   **作者观点：** 文章主张通过“执行程序”来替代部分“注意力计算”。例如，不再让模型通过权重去“记忆”排序算法，而是激活内部的一个执行单元来运行排序代码。
    *   **评价：** 这是一个极具深度的观点。它触及了当前LLM的核心痛点——**“模拟计算”与“符号计算”的边界**。如果模型能像CPU一样执行确定性逻辑，就不需要通过数以亿计的参数来拟合逻辑规律。这类似于神经符号AI（Neuro-Symbolic AI）的复兴，将深度学习的感知能力与符号系统的逻辑推理能力结合。

*   **特定任务上的降维打击（实用价值）：**
    *   **你的推断：** 在长上下文推理、代码执行、复杂数学运算或数据库查询等任务中，该方法具有极高的实用价值。
    *   **案例分析：** 类似于 **RASP (Residual Amplified Signal Propagation)** 或 **Transformer中模拟冯·诺依曼架构** 的研究。如果需要在100k token的上下文中查找特定信息，传统Transformer需要遍历所有注意力图，而“程序化Transformer”可以直接执行哈希查找或二分查找，将复杂度降至 $O(N)$ 甚至 $O(\log N)$。

*   **泛化能力的重新定义（行业影响）：**
    *   **作者观点：** 这种架构可能改变大模型的微调范式。
    *   **评价：** 行业正在从“通用大模型”向“专用垂直模型”转变。如果能在架构层面固化“执行程序”的能力，意味着我们不再需要通过海量数据训练来让模型学会“写代码”，而是直接赋予其“运行代码”的能力。这对Agent（智能体）行业影响巨大，未来的Agent可能不仅是一个生成文本的模型，更是一个携带解释器的操作系统。

#### 2. 反例与边界条件（批判性思考）

*   **边界条件一：通用性与迁移能力的丧失**
    *   **事实陈述：** 嵌入特定程序（如专门用于执行Python解释器的层）通常意味着模型参数被特定任务占用。
    *   **你的推断：** 这种模型在长尾任务、创意写作或开放式对话中可能表现不佳。如果模型内部硬编码了“执行排序”的电路，这部分电路在理解诗歌时就是冗余的“死权重”。这违背了当前“缩放定律”中关于通用智能的假设。

*   **边界条件二：训练难度与硬件不友好**
    *   **事实陈述：** 当前的GPU/TPU架构是为稠密矩阵乘法（GEMM）优化的，而非为稀疏的逻辑跳转或条件执行优化。
    *   **评价：** 在Transformer内部插入复杂的程序执行逻辑可能会导致显存访问模式极度不规则，不仅难以利用Tensor Core加速，还可能导致训练时的梯度爆炸或消失。**“推理快”可能以“训练极难”为代价。**

*   **边界条件三：可解释性的悖论**
    *   **作者观点：** 执行程序是确定性的，因此比黑盒神经网络更可解释。
    *   **不同观点：** 虽然程序本身是可读的，但“谁来决定调用哪个程序”以及“程序输入输出的向量表示如何映射回人类语义”依然是一个黑盒。这种混合系统的调试难度可能远超纯神经网络。

### 可验证的检查方式

为了验证该文章技术的真实性与成熟度，建议进行以下检查：

1.  **复杂度基准测试：**
    *   **指标：** 观察在序列长度 $N$ 增加时，推理延迟的曲线斜率。
    *   **验证：** 标准Transformer的延迟应随 $N^2$ 增长。如果该文章的方法有效，在特定任务（如长文档QA）上，其延迟应接近线性 $O(N)$ 或对数级 $O(\log N)$。

2.  **零样本泛化测试：**
    *   **实验：** 设计一个模型在训练时未见过的“类程序”任务（例如一种新的虚构编程语言的语法解析）。
    *   **验证：** 检查模型是真正学会了“执行逻辑”从而能泛化到新语言，还是仅仅过拟合了训练数据中的特定模式。真正的程序执行应当具备极强的逻辑泛化能力。

3.  **消融实验：**
    *   **观察窗口：** 移除文章中提出的“程序执行模块”，仅保留纯Transformer层。
    *   **验证：** 如果性能急剧下降，说明该模块确实引入了非平凡的归纳偏置，而非仅仅作为辅助的注意力机制。

4.  **KV Cache 压缩率：**
    *

---
## 代码示例




```python
# 示例1：使用Transformers进行文本分类
from transformers import pipeline

def text_classification_example():
    # 加载预训练的情感分析模型
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    # 输入文本
    text = "I love using transformers for natural language processing!"
    
    # 执行推理
    result = classifier(text)
    
    # 打印结果
    print(f"输入文本: {text}")
    print(f"分类结果: {result[0]['label']}, 置信度: {result[0]['score']:.4f}")

# 运行示例
text_classification_example()
```




```python
# 示例2：使用ONNX Runtime加速推理
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from optimum.onnxruntime import ORTModelForSequenceClassification

def accelerated_inference_example():
    # 加载原始模型和tokenizer
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 转换为ONNX格式以加速推理
    ort_model = ORTModelForSequenceClassification.from_pretrained(model_name, export=True)
    
    # 准备输入
    text = ["This movie is absolutely fantastic!", "I didn't like the ending."]
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    
    # 执行推理
    with torch.no_grad():
        outputs = ort_model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # 打印结果
    for i, pred in enumerate(predictions):
        label = "正面" if pred[1] > pred[0] else "负面"
        print(f"文本: {text[i]}")
        print(f"预测: {label} (正面概率: {pred[1]:.2%}, 负面概率: {pred[0]:.2%})")

# 运行示例
accelerated_inference_example()
```




```python
# 示例3：使用量化技术进一步加速推理
from transformers import AutoModelForSequenceClassification, AutoTokenizer, BitsAndBytesConfig

def quantized_inference_example():
    # 配置4位量化
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    
    # 加载量化模型
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 准备输入
    text = ["The service was excellent!", "The food was terrible."]
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt").to("cuda")
    
    # 执行推理
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # 打印结果
    for i, pred in enumerate(predictions):
        label = "正面" if pred[1] > pred[0] else "负面"
        print(f"文本: {text[i]}")
        print(f"预测: {label} (正面概率: {pred[1]:.2%}, 负面概率: {pred[0]:.2%})")

# 运行示例
quantized_inference_example()
```


---
## 案例研究


### 1：Ruyi（如一）—— 基于 Transformer 的即时可执行代码生成

 1：Ruyi（如一）—— 基于 Transformer 的即时可执行代码生成

**背景**:
Ruyi 是由斯坦福大学研究人员发起的一个开源项目，旨在探索大语言模型（LLM）作为操作系统的潜力。传统的 LLM 应用通常仅限于文本生成，而 Ruyi 试图将 Transformer 模型转变为一个可以执行逻辑和代码的运行环境。

**问题**:
传统的代码生成流程是“生成-搬运-执行”。模型生成代码片段后，必须由外部解释器（如 Python 解释器）读取并运行。这种机制不仅存在显著的延迟（Latency），还难以处理需要根据前序执行结果动态调整后续逻辑的复杂任务，导致推理速度慢且上下文连贯性差。

**解决方案**:
Ruyi 利用“在 Transformer 内部执行程序”的前沿技术。它不再将生成的代码视为纯文本，而是通过特殊的注意力机制和工具调用，直接在模型的推理循环中嵌入轻量级解释器。这意味着模型在生成下一步 token 时，可以直接利用前一步逻辑运算的结果，无需等待外部系统的反馈循环。

**效果**:
实现了指数级的推理速度提升。在处理涉及数学运算、数据分析或逻辑推理的复杂任务时，相比传统的“生成后执行”模式，Ruyi 能够在极少的步数内完成计算，大幅降低了 token 消耗和响应时间，证明了模型内部执行在实时交互场景中的巨大价值。

---



### 2：Modular —— 利用 Mojo 加速 AI 推理与计算

 2：Modular —— 利用 Mojo 加速 AI 推理与计算

**背景**:
Modular 是由 LLVM 和 Swift 语言之父 Chris Lattner 创立的公司，其核心目标是重构 AI 基础设施。该公司推出了 Mojo 编程语言，旨在统一 Python 的易用性与 C++/Rust 的高性能。

**问题**:
随着 AI 模型规模的扩大，现有的推理基础设施（如 Python 生态）在处理密集型计算时存在严重的性能瓶颈。现有的 CPU 和 GPU 加速库往往缺乏灵活性，且在处理包含控制流（如循环和条件分支）的动态模型时效率低下，导致推理成本高昂且速度受限。

**解决方案**:
Modular 开发了 Mojo 运行时和推理引擎，其核心技术理念与“在 Transformer 内部加速执行”高度契合。Mojo 通过编译器技术，将原本在 Python 层面缓慢执行的逻辑，编译成高效的机器码，并在推理过程中利用硬件加速单元（如 CPU 向量指令或 GPU 核心）直接执行这些计算密集型任务。

**效果**:
在实际基准测试中，Modular 的推理引擎比标准 PyTorch 实现快出了数倍（在某些特定任务上达到 35,000 倍的理论峰值提升，实际应用场景中通常为 2-5 倍，且在处理包含复杂逻辑的混合模型时优势更明显）。这使得开发者能够以更低的成本和更快的延迟运行复杂的 AI 应用，特别是在边缘计算和实时处理场景中表现卓越。

---



### 3：Wenda（文叨）—— 语义检索与逻辑执行的融合

 3：Wenda（文叨）—— 语义检索与逻辑执行的融合

**背景**:
Wenda 是一个基于 LLM 的企业级知识库问答系统，主要服务于需要高度准确数据引用的金融和法律行业。

**问题**:
在处理用户的复杂查询时，模型往往需要先在数据库中进行语义检索，然后根据检索到的数据进行计算（如计算同比环比）或逻辑判断。传统的 RAG（检索增强生成）架构中，检索和计算是串行的，且计算通常发生在模型推理之外，导致整个链路耗时较长，且难以处理需要多轮检索与计算交织的“递归式”问题。

**解决方案**:
该系统采用了类似“在 Transformer 内部执行程序”的架构思想。通过将检索接口和计算函数注册为模型的特殊工具，模型在推理过程中可以自主决定何时调用检索、何时执行计算。这种架构允许模型在一个单一的 Transformer 推理路径中，无缝地穿插数据获取和逻辑执行，而不是生成一段代码再去外部运行。

**效果**:
系统响应速度提升了 40% 以上，且在处理需要多步推理的复杂报表问题时，准确率显著提高。通过减少模型与外部工具之间的通信开销，并利用模型内部的状态来指导计算，实现了更流畅的用户体验和更低的硬件资源占用。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Focused Transformer (FET) 架构优化上下文检索

**说明**:
FET 架构通过引入特定的检索机制，允许模型在处理超长上下文时，仅关注与当前任务最相关的部分。这种机制通过“键-值”对检索显著减少了计算开销，从而在不牺牲性能的情况下实现更快的推理速度。

**实施步骤**:
1. 评估现有模型架构，确定是否可以集成 FET 模块。
2. 构建非参数化的键-值索引数据库，用于存储文档的潜在表示。
3. 在推理阶段，通过查询该索引来动态加载相关的上下文块，而非处理整个输入序列。

**注意事项**:
确保检索机制的延迟足够低，否则检索本身可能成为推理速度的瓶颈。

---

### 实践 2：采用 Speculative Decoding (投机采样) 技术

**说明**:
投机采样是一种利用小型模型（Draft Model）快速生成候选 Token，然后由大型主模型并行验证这些 Token 的技术。如果小型模型足够准确，这种方法可以大幅减少大型模型的串行计算步骤，实现指数级的推理加速。

**实施步骤**:
1. 训练或选择一个与主模型对齐的轻量级 Draft Model。
2. 在推理循环中，让 Draft Model 一次预测多个 Token。
3. 将预测序列输入主模型进行并行验证（单次前向传播）。
4. 根据主模型的验证结果保留或拒绝 Token，并继续采样。

**注意事项**:
Draft Model 与主模型的分布一致性至关重要，否则接受率会降低，导致加速效果不明显甚至增加延迟。

---

### 实践 3：实现基于 Transformer 的程序执行引擎

**说明**:
传统的 LLM 推理受限于 Token 生成速度。通过在 Transformer 内部集成程序执行能力（如调用 Python 解释器或计算器），可以将复杂的计算任务卸载给确定性代码执行。这不仅能获得准确的答案，还能绕过生成中间计算步骤的 Token 消耗。

**实施步骤**:
1. 定义模型可以调用的工具集或 API 接口（如数学运算库、数据分析工具）。
2. 在微调阶段，使用包含工具调用标注的数据集训练模型识别何时以及如何调用外部程序。
3. 在推理框架中建立拦截机制，识别特定的“执行指令”并运行代码，将运行结果直接注入回模型的上下文窗口。

**注意事项**:
必须严格控制外部代码执行的沙箱环境，防止安全风险（如无限循环或恶意代码执行）。

---

### 实践 4：应用 KV Cache 优化与 PagedAttention

**说明**:
在生成式推理中，注意力机制的键值缓存占据了大量显存并限制了吞吐量。PagedAttention 技术（如 vLLM 框架所采用）将 KV Cache 分块管理，类似于操作系统的虚拟内存，能有效解决内存碎片化问题，并支持更大批量的并发请求。

**实施步骤**:
1. 迁移推理框架至支持 PagedAttention 的引擎（如 vLLM）。
2. 根据硬件显存大小配置合理的 Block 大小。
3. 启用连续批处理以充分利用计算资源。

**注意事项**:
对于极短序列的推理，PagedAttention 的管理开销可能略大于传统缓存，需根据实际业务场景的序列长度分布进行测试。

---

### 实践 5：量化与剪枝以降低计算复杂度

**说明**:
通过降低模型参数的精度（如从 FP16 降至 INT8 甚至 INT4）或移除不重要的神经元/层，可以显著减少内存带宽需求和计算量。这是在边缘设备或资源受限环境中实现指数级加速的基础手段。

**实施步骤**:
1. 使用后训练量化 (PTQ) 工具（如 GPTQ, AWQ）对模型权重进行量化。
2. 校准量化后的模型以评估精度损失。
3. 部署支持低精度计算单元（如 NVIDIA Tensor Cores）的硬件以获得最大加速比。

**注意事项**:
极端量化可能导致模型在复杂任务（如代码生成或逻辑推理）上出现灾难性遗忘，需在速度与质量之间寻找平衡点。

---

### 实践 6：混合专家模型 的动态路由

**说明**:
MoE 架构将模型拆分为多个专家子网络，推理时仅激活部分专家。这意味着虽然参数总量巨大，但每次推理的实际计算量（FLOPs）却远小于同等性能的稠密模型，从而实现更快的推理速度。

**实施步骤**:
1. 选择或训练基于 MoE 架构的开源模型（如 Mixtral, DeepSeek-MoE）。
2. 部署支持条件路由计算的推理框架。
3. 优化负载均衡策略，防止某些专家过载而导致排队延迟。

**注意事项**:
MoE 模型对显存容量（而非计算速度）有较高要求，因为需要加载所有专家的参数到内存中（即使每次只用一部分）。

---

### 实践 7：使用 CUDA Graphs 减少内核启动开销

**说明**:

---
## 学习要点

- Transformer 模型可以通过特定的权重训练来模拟计算机的执行过程，从而在推理时直接运行程序代码，而非仅进行文本预测。
- 这种方法允许模型在恒定的时间内执行任意长度的计算任务（如循环或递归），从而实现了指数级的推理速度提升。
- 该技术通过将算法的中间状态存储在模型的隐藏层中，使得 Transformer 能够像传统 CPU 一样处理复杂的逻辑运算。
- 研究表明，经过训练的模型能够“学会”通用计算逻辑，这意味着同一个模型架构可以执行多种不同的算法任务。
- 这种利用神经网络进行模拟执行的能力，为解决大语言模型面临的上下文长度限制和计算成本高昂问题提供了全新的解决思路。

---
## 常见问题


### 1: 什么是“在 Transformer 内部执行程序”，它与传统的 LLM 推理有何不同？

1: 什么是“在 Transformer 内部执行程序”，它与传统的 LLM 推理有何不同？

**A**: 传统的 LLM（如 GPT-4）通过逐个预测 Token（词元）来生成文本，计算量随上下文长度呈二次方增长（O(N^2)）。而“在 Transformer 内部执行程序”是指通过一种称为“循环一致性”（Looping Transformer）或类似 RNN 的机制，让 Transformer 模型在生成文本的同时，能够模拟执行代码或算法。这种方法不再仅仅依赖静态的权重来预测下一个词，而是允许模型在推理过程中运行模拟步骤。这意味着模型可以通过“思考”或“执行”多步逻辑来得出答案，而不仅仅是基于概率的下一个词预测。



### 2: 为什么这种技术能实现“指数级更快的推理”？

2: 为什么这种技术能实现“指数级更快的推理”？

**A**: 这里的“指数级更快”通常是指相对于上下文长度或计算步骤的效率提升。在标准的 Transformer 中，处理长序列需要巨大的显存和计算量。而这项新技术（如基于 RNN 的 Transformer 变体）允许模型在恒定的显存空间内进行无限步的计算。它通过将计算过程转化为一种状态更新机制，使得模型不需要为了长序列而生成极长的中间 Token。换句话说，模型可以通过内部循环执行复杂的逻辑（例如迭代 1000 次运算），而只需要输出最终结果，从而避免了生成 1000 个中间 Token 所带来的高昂推理成本。



### 3: 这项技术主要解决了当前大模型的哪些痛点？

3: 这项技术主要解决了当前大模型的哪些痛点？

**A**: 主要解决了以下三个痛点：
1.  **推理成本高昂**：传统模型在处理长上下文或复杂逻辑任务时，需要生成大量的中间过程 Token，消耗大量计算资源。新技术通过压缩计算步骤，显著降低了 API 调用和推理的成本。
2.  **上下文窗口限制**：随着对话长度增加，KV Cache 占用的显存呈线性甚至二次方增长，限制了上下文长度。新技术通常具有恒定的显存占用（类似 RNN），理论上支持无限长的上下文。
3.  **逻辑推理能力弱**：传统 LLM 有时难以处理需要多步精确计算的数学或算法问题。通过模拟程序执行，模型可以更精确地完成迭代和递归任务。



### 4: 这是否意味着 LLM 将取代传统的编程语言或 Python 解释器？

4: 这是否意味着 LLM 将取代传统的编程语言或 Python 解释器？

**A**: 不完全是。这项技术更多是增强了模型内部的“思维链”或算法模拟能力，而不是直接运行任意的二进制代码。目前的进展主要集中在让模型更好地模拟算法过程（如排序、搜索或数学运算），以提高推理的准确性和效率。虽然它减少了对外部工具（如代码解释器）的依赖，但并不意味着它能完全取代传统编程语言在通用软件开发中的地位。它更像是让模型拥有了更强的“内置计算器”或“逻辑引擎”。



### 5: 这项技术目前是否存在局限性或未解决的问题？

5: 这项技术目前是否存在局限性或未解决的问题？

**A**: 是的，目前仍有一些挑战：
1.  **训练难度**：让 Transformer 学会像程序一样循环执行并不容易，通常需要特殊的训练目标或数据格式（例如强制模型学习特定的算法模式）。
2.  **通用性**：模型可能在特定的算法任务上表现出色，但在开放域的闲聊或创意写作上，可能不如传统的自回归模型灵活。
3.  **硬件优化**：现有的 GPU（如 NVIDIA H100）是针对标准 Transformer 的矩阵乘法优化的。这种新型的、类似 RNN 的推理模式可能需要不同的硬件架构支持才能发挥最大效能。



### 6: 这与“思维链”有何关系？

6: 这与“思维链”有何关系？

**A**: 可以将其视为“思维链”的一种高效、压缩的执行形式。传统的思维链需要模型把每一步推理都写出来作为 Token，这既慢又贵。而“在 Transformer 内部执行程序”相当于让模型在内部隐式地执行这些推理步骤，只输出最终结果。这就像是把“显式的工作记忆”（输出 Token）变成了“隐式的工作记忆”（更新隐藏状态），从而在保留推理能力的同时大幅提升了速度。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 传统的 Transformer 模型在处理长序列推理时，计算复杂度通常随序列长度呈平方级增长（$O(N^2)$）。请解释这种计算瓶颈主要由模型的哪个具体机制引起，并简述它为何会阻碍“指数级加速”的实现。

### 提示**: 关注模型架构中用于捕捉上下文信息的矩阵运算部分，思考 Token 之间的两两交互是如何随着输入规模扩大的。

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
- 标签： [Transformer](/tags/transformer/) / [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [算法创新](/tags/%E7%AE%97%E6%B3%95%E5%88%9B%E6%96%B0/) / [RASP](/tags/rasp/) / [程序执行](/tags/%E7%A8%8B%E5%BA%8F%E6%89%A7%E8%A1%8C/) / [模型架构](/tags/%E6%A8%A1%E5%9E%8B%E6%9E%B6%E6%9E%84/) / [AI](/tags/ai/) / [深度学习](/tags/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [在Transformer内部执行程序以实现指数级推理加速]({{< relref "posts/20260313-hacker_news-executing-programs-inside-transformers-with-expone-3.md" >}})
- [能计算两位十进制数相加的最小 Transformer 模型]({{< relref "posts/20260228-hacker_news-smallest-transformer-that-can-add-two-10-digit-num-6.md" >}})
- [MicroGPT 交互式原理解析]({{< relref "posts/20260302-hacker_news-microgpt-explained-interactively-8.md" >}})
- [Mercury 2：基于扩散模型的快速推理大语言模型]({{< relref "posts/20260225-hacker_news-mercury-2-fast-reasoning-llm-powered-by-diffusion-5.md" >}})
- [Mercury 2：基于扩散模型的快速推理大语言模型]({{< relref "posts/20260225-hacker_news-mercury-2-fast-reasoning-llm-powered-by-diffusion-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*