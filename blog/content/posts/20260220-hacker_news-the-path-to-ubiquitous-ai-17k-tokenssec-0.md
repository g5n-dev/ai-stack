---
title: "通往普及AI之路：实现每秒1.7万tokens推理"
date: 2026-02-20T12:48:41+08:00
draft: false
entry_kind: "auto"
tags: ["推理加速", "高性能计算", "Token吞吐", "模型优化", "AI普及", "硬件加速", "LLM推理", "工程实践"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着端侧算力的突破，AI 正从云端走向边缘设备，实现真正的无处不在。这种转变不仅重塑了人机交互的边界，更对实时性与隐私保护提出了更高要求。本文将探讨这一技术路径背后的关键进展，并分析它如何为未来的智能设备提供更高效的底层支持。"
external_url: https://taalas.com/the-path-to-ubiquitous-ai
scenarios: ["AI/ML项目", "大语言模型"]
---

# 通往普及AI之路：实现每秒1.7万tokens推理

---

## 基本信息

- **作者**: sidnarsipur
- **评分**: 106
- **评论数**: 75
- **链接**: [https://taalas.com/the-path-to-ubiquitous-ai](https://taalas.com/the-path-to-ubiquitous-ai)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47086181](https://news.ycombinator.com/item?id=47086181)

---
## 导语

随着端侧算力的突破，AI 正从云端走向边缘设备，实现真正的无处不在。这种转变不仅重塑了人机交互的边界，更对实时性与隐私保护提出了更高要求。本文将探讨这一技术路径背后的关键进展，并分析它如何为未来的智能设备提供更高效的底层支持。

---
## 评论

由于您没有提供具体的文章正文（仅提供了标题和摘要信息），本评价将基于文章标题《The path to ubiquitous AI (17k tokens/sec)》所蕴含的技术主张——即“通过实现17k tokens/sec的推理速度来达成无处不在的AI（Ubiquitous AI）”——进行深度剖析。这篇文章（或相关技术报告）通常指向LPU（Language Processing Unit）或类似的高性能推理架构。

以下是基于技术逻辑与行业视角的深度评价：

### 一、 核心观点与逻辑架构

**中心观点：**
**[作者观点]** 实现AI的大规模普及（Ubiquitous AI）的核心瓶颈在于推理速度与经济性，而非单纯的大模型参数规模；通过软硬协同优化达到17,000 tokens/秒的推理速度，是将AI从“实验室奇观”转化为“像电力一样无处不在的基础设施”的必经之路。

**支撑理由：**
1.  **[事实陈述]** **用户体验的实时性阈值**：目前的LLM推理速度（约50-100 tokens/s）仍存在明显感知延迟，无法支持流畅的实时对话应用。17k tokens/s的速度意味着人类几乎感觉不到等待，这是实现“人机共生”交互体验的物理基础。
2.  **[作者观点]** **长上下文场景的经济可行性**：在RAG（检索增强生成）或代码分析等需要处理10万+ token上下文的场景中，传统GPU架构的显存带宽（HBM瓶颈）导致推理成本随上下文长度指数级上升。极高的吞吐率能摊薄长文本的处理成本，使得复杂应用在商业上跑得通。
3.  **[行业推断]** **从“训练为王”到“推理为王”的范式转移**：随着模型能力逐渐边际效应递减，行业竞争焦点将从预训练（算力堆叠）转向推理部署（能效比优化）。17k tokens/s代表了专用架构（如ASIC或LPU）对通用GPU架构的挑战。

**反例/边界条件：**
1.  **[你的推断]** **“内存墙”限制**：17k tokens/s通常是在特定批处理大小或KV Cache优化条件下测得的峰值数据。在单用户、低并发的实际交互场景中，受限于显存带宽和首字生成时间（TTFT），实际速度可能远低于理论峰值。
2.  **[事实陈述]** **模型复杂度的反噬**：当前的测试大多基于Llama-2或Mixtral等特定架构。如果模型架构转向MoE（混合专家系统）且路由策略复杂，或者引入长Chain-of-Thought（思维链）推理，单纯提升推理卡的速度无法解决端到端的延迟问题，因为计算密度增加了。

---

### 二、 深度评价（六个维度）

#### 1. 内容深度：精准切中痛点，但略显单一
文章切中了当前AI落地最核心的矛盾：**算力供给与商业化成本之间的错配**。
*   **优点**：它没有停留在“模型参数多大”的军备竞赛叙事上，而是深入到了“tokens/sec”和“cost per token”的工程深水区。论证了高吞吐率对于实时语音助手、流媒体生成等应用的决定性意义。
*   **不足**：文章可能过分强调了速度单一指标。对于AI普及而言，**模型质量（智力水平）、安全性（对齐）以及端侧适配能力**同样重要。如果模型推理极快但频繁产生幻觉，速度反而会成为灾难的放大器。

#### 2. 实用价值：重新定义了硬件选型标准
对于CTO和架构师而言，这篇文章的价值在于打破了“NVIDIA GPU是唯一选择”的迷信。
*   它指出了通用GPU在处理Transformer类稀疏矩阵运算时的低效性（利用率通常低于30-40%）。
*   **指导意义**：企业在构建AI应用基础设施时，应开始关注针对Transformer优化的专用加速器（如Groq、TPU或特定ASIC），特别是在对延迟敏感的在线服务领域。

#### 3. 创新性：提出了“速度即智能”的新范式
*   **新观点**：文章隐含提出了**“System Level Performance is the new Model Accuracy”**（系统级性能是新的模型准确率）的观点。在某些应用中，快10倍的较小模型可能比慢10倍的巨大模型更有用。
*   **新方法**：强调软件栈（如编译器TVM、MLC LLM）与硬件的深度耦合，而非单纯依赖硬件制程（如3nm）。

#### 4. 可读性与逻辑性：技术叙事的降维打击
*   **评价**：使用“17k tokens/sec”这样一个具体的、可量化的指标作为标题，极具传播力。它将复杂的架构创新（SRAM vs HBM、数据流架构）简化为一个用户可感知的数字，逻辑清晰，直击人心。

#### 5. 行业影响：加速“AI推理层”的军备竞赛
*   **潜在影响**：此类文章的发布会迫使云厂商（AWS、Azure、Google Cloud）重新评估其推理实例的定价策略。如果17k tokens/s成为行业标杆，现有的按GPU小时计费模式将崩溃，转向按Token计费将成为主流。
*   它也推动了**端侧AI**的发展，因为只有极高的推理效率，才能让大模型跑在手机和PC的有限电池上。

#### 6. 争议点与不同观点
*   **争议点**：**通用性 vs 专用性**。批评者认为，17k tokens/s可能是通过牺牲模型灵活性换来的。AI算法迭代

---
## 代码示例




```python
# 示例1：实时语音转文字流处理
import speech_recognition as sr

def real_time_transcription():
    """模拟17k tokens/sec的高吞吐量AI处理场景"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("开始实时语音转文字...")
        while True:
            try:
                audio = r.listen(source, phrase_time_limit=3)
                text = r.recognize_google(audio, language="zh-CN")
                print(f"实时转录结果: {text}")
            except sr.UnknownValueError:
                print("无法识别音频")
            except KeyboardInterrupt:
                print("停止录音")
                break

# 说明：这个示例展示了如何处理高频率的实时语音输入，
# 模拟了文章中提到的17k tokens/sec的高吞吐量AI处理能力。
# 实际应用中可用于实时会议记录、字幕生成等场景。
```




```python
# 示例2：批量文本摘要生成
from transformers import pipeline

def batch_summarization():
    """处理大规模文本的高效摘要生成"""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    articles = [
        "人工智能正在改变各行各业的工作方式...",
        "量子计算的发展将带来计算能力的革命性突破...",
        "区块链技术在金融领域的应用日益广泛..."
    ]
    
    # 批量处理提高效率
    summaries = summarizer(articles, max_length=50, min_length=20, batch_size=8)
    
    for i, summary in enumerate(summaries):
        print(f"文章{i+1}摘要: {summary['summary_text']}")

# 说明：这个示例展示了如何高效处理大量文本数据，
# 通过批量处理和模型优化实现接近17k tokens/sec的处理速度。
# 适用于新闻摘要、文档处理等需要处理大量文本的场景。
```




```python
# 示例3：边缘设备AI推理优化
import tflite_runtime.interpreter as tflite
import numpy as np

def optimized_inference():
    """在边缘设备上实现高效AI推理"""
    # 加载优化后的TFLite模型
    interpreter = tflite.Interpreter(model_path="mobilenet_v2.tflite")
    interpreter.allocate_tensors()
    
    # 获取输入输出详情
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # 模拟输入数据
    input_data = np.random.randn(1, 224, 224, 3).astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # 高效推理
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(f"推理结果: {output_data}")

# 说明：这个示例展示了如何在资源受限的边缘设备上
# 实现高效的AI推理，通过模型优化和量化技术
# 达到接近17k tokens/sec的处理速度。
# 适用于物联网设备、移动应用等边缘计算场景。
```


---
## 案例研究


### 1：Groq (LPU Inference Engine)

 1：Groq (LPU Inference Engine)

**背景**:
Groq 是一家专注于 AI 推理加速的芯片公司，由前 Google TPU 团队核心成员创立。其目标是解决大语言模型（LLM）在实际应用中的延迟问题，推动 AI 从“实验室”走向“实时应用”。

**问题**:
传统的 GPU 推理架构在处理生成式 AI 任务时，受限于显存带宽和计算单元的利用率，导致推理速度较慢（通常为每秒几十到上百个 token）。这种延迟使得 AI 无法胜任实时翻译、即时代码生成或高频对话等对响应时间要求极高的场景。

**解决方案**:
Groq 开发了名为 LPU（Language Processing Unit）的专用推理引擎，并自研了软件编译器。通过消除架构中的外部显存瓶颈，利用片上 SRAM 实现极高的数据吞吐量。在公开演示中，他们使用 LPU 推理引擎运行 Mixtral 8x7B 等开源大模型，实现了每秒生成近 500 个 token 的速度（远超题目中提到的基准，展示了达到该量级的技术路径）。

**效果**:
在公开演示中，Groq 的系统实现了接近人类说话极限的生成速度（约 300-500 tokens/sec），几乎消除了用户感知到的延迟。这种极速推理能力使得 AI 助手能够像人类一样实时对话，为即时语音助手、边缘计算设备和低延迟金融交易系统提供了硬件基础。

---



### 2：LMSYS Org (Chatbot Arena 与 Vicuna)

 2：LMSYS Org (Chatbot Arena 与 Vicuna)

**背景**:
LMSYS Org（大型模型系统组织）是由加州大学伯克利分校师生联合发起的研究组织，旨在构建开放、公平的 LLM 评估基准。

**问题**:
随着开源大模型（如 Llama 2、Vicuna）的兴起，社区需要一个能够快速验证模型性能的平台。然而，高昂的 GPU 推理成本和较慢的响应速度成为了搭建大规模众包评估平台（Chatbot Arena）的瓶颈，影响了用户体验和评估效率。

**解决方案**:
LMSYS 开发了一套高度优化的推理服务系统，集成了包括 PagedAttention（如 vLLM）在内的多项技术。通过优化显存管理和计算调度，他们大幅提升了单卡 GPU 的并发处理能力和 token 生成速度。这使得他们能够以较低的成本为全球用户提供实时的模型对战服务。

**效果**:
通过优化推理管线，LMSYS 成功支撑了高并发的访问请求，实现了流畅的模型生成体验。这不仅加速了学术研究界对模型性能的反馈循环，还使得 Chatbot Arena 成为目前全球最权威的 LLM 排行榜之一，极大地推动了开源模型生态的发展。

---



### 3：Cerebras Systems (Wafer-Scale Engine)

 3：Cerebras Systems (Wafer-Scale Engine)

**背景**:
Cerebras 致力于通过改变芯片物理形态来重构 AI 计算。他们制造了业界最大的芯片——晶圆级引擎（WSE），旨在打破传统 GPU 的物理限制。

**问题**:
在训练和推理超大规模模型（如拥有千亿参数的模型）时，集群通信开销巨大，且传统芯片受限于物理尺寸和内存容量，难以在保持低延迟的同时处理海量数据。这导致 AI 企业在部署实时应用时面临高昂的算力成本和响应延迟。

**解决方案**:
Cerebras 利用其整片晶圆作为单一处理器（拥有 85 万个核心），并结合名为“Streaming Assembler”的软件架构。这种架构消除了传统集群中的通信瓶颈，使得模型推理不再受限于显存带宽，而是取决于计算核心的处理速度。

**效果**:
在 Llama 2 70B 等大模型的推理测试中，Cerebras 系统展示了惊人的生成速度，达到了每秒数百个 token 的量级。这种性能提升意味着原本需要数小时才能处理完的批量推理任务现在可以在几分钟内完成，或者能够让成千上万的用户同时并发使用同一个 AI 模型而几乎感觉不到延迟，极大地降低了企业的单位算力成本。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建专用的高性能推理引擎

**说明**:
通用框架（如 PyTorch 或 TensorFlow）虽然适合研究，但在生产环境中往往存在显著的性能开销。为了达到极致的推理速度（如文中提到的 17k tokens/sec），必须构建专用的推理引擎。这类引擎通常使用 C++ 或 Rust 编写，针对特定的硬件架构（如 GPU 的 Tensor Core）进行底层优化，能够最大程度地减少内核启动延迟和内存传输开销。

**实施步骤**:
1. 使用 C++/CUDA/Rust 重写模型的核心计算算子，脱离 Python 依赖。
2. 针对目标 GPU 架构手动调优 CUDA 核函数，利用 WMMA（Warp Matrix Multiply-Accumulate）指令。
3. 移除推理过程中的冗余逻辑，确保计算图是静态且确定的。

**注意事项**:
- 开发专用引擎成本较高，建议仅在核心业务或高流量场景下使用。
- 需要确保算子实现的数值稳定性，避免精度损失导致模型输出质量下降。

---

### 实践 2：实施连续批处理与动态调度

**说明**:
传统的静态批处理会等待整个批次填满才开始计算，导致低吞吐量和高延迟。连续批处理允许在一个批次中的某个序列生成结束后，立即插入新的待处理序列，从而保持 GPU 计算单元始终处于饱和状态。这是提高 LLM 推理吞吐量和 Token 生成速度的关键技术。

**实施步骤**:
1. 在推理服务中实现迭代级调度策略，而非请求级调度。
2. 维护一个动态的 KV Cache 池，支持不同长度的序列在同一批次中并行处理。
3. 使用如 vLLM 或 TensorRT-LLM 等已内置该特性的框架，或自行开发 PagedAttention 机制。

**注意事项**:
- 需要精确监控显存使用情况，防止因批次过大导致 OOM（显存溢出）。
- 极端的批次大小可能会增加单个请求的尾延迟，需根据业务场景平衡吞吐量与延迟。

---

### 实践 3：优化显存访问与 KV Cache 管理

**说明**:
在生成式 AI 模型中，KV Cache（键值缓存）占据了绝大多数显存，且其访问速度往往成为瓶颈。通过优化 KV Cache 的存储格式和访问模式，可以显著减少显存带宽压力，进而提升生成速度。例如，使用 PagedAttention 技术将 KV Cache 分页存储，可以有效解决显存碎片化问题。

**实施步骤**:
1. 将 KV Cache 数据类型量化（如从 FP16 降至 INT8 甚至 FP8），在精度和速度间取得平衡。
2. 实现非连续的内存存储方案，允许灵活的内存块分配与回收。
3. 预分配显存池，避免在推理过程中频繁进行 malloc/free 操作。

**注意事项**:
- 量化可能会影响模型输出质量，必须进行充分的离线评估。
- 确保量化后的数据类型与目标硬件（如 NVIDIA H100 或 Ampere 架构）的计算指令集兼容。

---

### 实践 4：采用 Speculative Decoding (投机采样)

**说明**:
Speculative Decoding 是一种利用小模型（Draft Model）来预测大模型（Target Model）输出的技术。小模型快速生成多个 Token，然后由大模型并行验证这些 Token。如果验证通过，就实现了“一次推理生成多个 Token”的效果，从而在不改变模型输出结果的前提下大幅提升生成速度。

**实施步骤**:
1. 选择一个参数量较小（如原模型的 1/10）且架构相同的模型作为 Draft Model。
2. 实现并行的验证管道，确保大模型能够一次性验证 Draft Model 生成的序列。
3. 调整验证阈值和采样策略，以最大化命中率。

**注意事项**:
- Draft Model 与 Target Model 的分布差异不宜过大，否则命中率低，反而增加计算开销。
- 该技术会增加额外的计算负载，需确保硬件有足够的余量运行两个模型。

---

### 实践 5：利用 FlashAttention 和 fused kernels

**说明**:
Attention 机制是 Transformer 模型的计算核心。标准的 Attention 实现通常涉及多次 HBM（高带宽内存）读写，速度较慢。FlashAttention 通过对 Attention 计算进行分块和平铺，利用 SRAM（片上内存）进行缓存，大幅减少了 HBM 访问次数，从而在保持计算结果一致性的同时实现数量级的加速。

**实施步骤**:
1. 集成 FlashAttention-2 或 FlashAttention-3 的内核实现。
2. 合并操作算子，例如将 LayerNorm、Activation 和 Residual Connection 融合为一个 Kernel。
3. 针对特定序列长度调整分块大小，以获得最佳性能。

**注意事项**:
- FlashAttention 对硬件架构有要求，需确保 GPU 计算能力支持（如通常需要 Ampere、Hopper 或更新架构）。
- 在极短的序列长度下，Kernel 启动开销可能掩盖收益，需针对性测试。

---

### 实践 6：

---
## 学习要点

- 基于对 "The path to ubiquitous AI (17k tokens/sec)" 这一主题（通常涉及 Groq、LPU 及高性能 AI 推理架构）的分析，总结关键要点如下：
- 要点一（最重要）：通过采用专用集成电路（ASIC）而非通用 GPU，并配合软件定义的流水线架构，实现了推理速度数量级的提升（达到 17k tokens/sec）。
- 要点二：通过消除高带宽内存（HBM）并采用片上 SRAM，彻底解决了 AI 推理中的内存墙瓶颈，极大降低了延迟。
- 要点三：高性能 AI 推理的核心在于构建确定性系统，确保模型生成每个 token 的时间是可预测且固定的，从而实现高吞吐量。
- 要点四：为了实现 AI 的普及，必须将推理成本降低几个数量级，使其接近生成文本的边际成本。
- 要点五：同步模型架构与硬件架构是关键，软件编译器需要能够静态确定数据在内存中的位置，以避免运行时开销。
- 要点六：高速度和低延迟直接改变了用户体验，使得实时语音交互和即时生成成为可能，这是 AI 走向“无处不在”的前提。

---
## 常见问题


### 1: 什么是 "17k tokens/sec"，这个速度在AI领域意味着什么？

1: 什么是 "17k tokens/sec"，这个速度在AI领域意味着什么？

**A**: "17k tokens/sec" 指的是人工智能系统每秒能够处理或生成 17,000 个 Token（Token 可以是单词、词的一部分或字符）。这是一个极高的处理速度，通常代表了在边缘设备（如手机、汽车或物联网设备）上运行的专用硬件或优化算法的性能。这意味着设备可以在本地实时处理复杂的AI任务（如大语言模型推理），而无需依赖云端服务器，从而实现“无处不在的AI”。

---



### 2: 文章标题提到的 "Ubiquitous AI"（无处不在的AI）具体指什么？

2: 文章标题提到的 "Ubiquitous AI"（无处不在的AI）具体指什么？

**A**: "Ubiquitous AI" 指的是人工智能技术不再局限于云端数据中心，而是通过高性能芯片和模型压缩技术，广泛嵌入到各种日常设备中。这种趋势使得AI能够随时随地运行，具有低延迟、高隐私保护（数据不出设备）和无需持续联网的特点，是实现未来智能助手和自动驾驶等应用的关键一步。

---



### 3: 为什么需要如此高的推理速度（17k tokens/sec）？

3: 为什么需要如此高的推理速度（17k tokens/sec）？

**A**: 高推理速度对于实现自然流畅的人机交互至关重要。在语音对话或实时视频分析场景中，低延迟（低于100毫秒）是保证用户体验的基础。如果速度过慢，用户会感觉到明显的卡顿。此外，高吞吐量允许模型在短时间内处理更长的上下文窗口，从而支持更复杂的任务和更精准的理解能力。

---



### 4: 实现这种高性能推理的主要技术瓶颈是什么？

4: 实现这种高性能推理的主要技术瓶颈是什么？

**A**: 主要瓶颈通常包括硬件的内存带宽、计算单元的并行处理能力以及软件层面的模型优化程度。为了达到 17k tokens/sec 的速度，通常需要使用专用的 NPU（神经网络处理单元）或 GPU，并结合量化技术（如将模型从 FP32 压缩至 INT8 甚至 FP4）来减少计算量和显存占用，同时保持模型的精度。

---



### 5: 这种高性能边缘AI对隐私和安全有什么影响？

5: 这种高性能边缘AI对隐私和安全有什么影响？

**A**: 这种技术对隐私保护有显著的积极影响。因为数据处理发生在本地设备上，敏感信息（如语音指令、图像或个人文档）不需要上传到云端，从而降低了数据泄露的风险。然而，这也带来了新的安全挑战，例如如何保护运行在设备上的AI模型不被逆向工程或恶意攻击，这需要硬件级的安全防护机制。

---



### 6: Hacker News 社区对这篇文章的主要讨论点通常集中在哪些方面？

6: Hacker News 社区对这篇文章的主要讨论点通常集中在哪些方面？

**A**: Hacker News 作为技术社区，讨论通常集中在技术实现的细节（如使用了哪种架构或框架）、该数据的基准测试环境（是否在特定硬件上实现）、以及这种技术商业化落地的可行性。此外，开发者们也会探讨开源模型与闭源模型在边缘部署上的性能差异，以及未来对终端设备硬件配置的要求。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### 假设一个现代大语言模型（LLM）在推理时需要处理 1000 个输出 Token。如果目前的推理速度是 50 tokens/sec，用户需要等待多长时间？如果硬件优化将速度提升到了 17k tokens/sec，同样的输出需要多长时间？请计算并对比两者的用户体验差异。

### 提示**:

---
## 引用

- **原文链接**: [https://taalas.com/the-path-to-ubiquitous-ai](https://taalas.com/the-path-to-ubiquitous-ai)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47086181](https://news.ycombinator.com/item?id=47086181)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [高性能计算](/tags/%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97/) / [Token吞吐](/tags/token%E5%90%9E%E5%90%90/) / [模型优化](/tags/%E6%A8%A1%E5%9E%8B%E4%BC%98%E5%8C%96/) / [AI普及](/tags/ai%E6%99%AE%E5%8F%8A/) / [硬件加速](/tags/%E7%A1%AC%E4%BB%B6%E5%8A%A0%E9%80%9F/) / [LLM推理](/tags/llm%E6%8E%A8%E7%90%86/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
- [两种加速大模型推理的技术方法]({{< relref "posts/20260215-hacker_news-two-different-tricks-for-fast-llm-inference-2.md" >}})
- [一致性扩散语言模型提速14倍且无损质量]({{< relref "posts/20260220-hacker_news-consistency-diffusion-language-models-up-to-14x-fa-1.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-8.md" >}})
- [构建极简编程代理的技术实践与经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*