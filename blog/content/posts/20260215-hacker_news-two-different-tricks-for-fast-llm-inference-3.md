---
title: "两种提升大模型推理速度的技术方法"
date: 2026-02-15T14:30:08+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "推理加速", "KV Cache", "量化", "Flash Attention", "PagedAttention", "vLLM", "性能优化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "大语言模型在实际应用中常面临推理延迟高、吞吐量低的挑战，这直接影响了用户体验与部署成本。本文介绍了两种不同的技术技巧，旨在通过优化计算流程来加速模型推理。通过阅读本文，读者可以了解这些方法的具体实现原理，以及如何在不显著牺牲模型性能的前提下，有效提升生成速度。"
external_url: https://www.seangoedecke.com/fast-llm-inference
scenarios: ["大语言模型"]
---

# 两种提升大模型推理速度的技术方法

---

## 基本信息

- **作者**: swah
- **评分**: 58
- **评论数**: 29
- **链接**: [https://www.seangoedecke.com/fast-llm-inference](https://www.seangoedecke.com/fast-llm-inference)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47022329](https://news.ycombinator.com/item?id=47022329)

---
## 导语

大语言模型在实际应用中常面临推理延迟高、吞吐量低的挑战，这直接影响了用户体验与部署成本。本文介绍了两种不同的技术技巧，旨在通过优化计算流程来加速模型推理。通过阅读本文，读者可以了解这些方法的具体实现原理，以及如何在不显著牺牲模型性能的前提下，有效提升生成速度。

---
## 评论

### 一、 核心观点与逻辑架构

**文章中心观点：**
LLM 推理加速正从依赖硬件堆叠转向算法架构层面的结构性突破，特别是通过打破“逐 Token 生成”的串行依赖或利用“小模型猜大模型”的并行策略，能在不显著牺牲生成质量的前提下实现数量级的延迟降低。

**支撑理由（基于该类文章通常涵盖的技术路径）：**

1.  **投机采样：**
    *   **[事实陈述]** 利用一个小型 Draft Model 快速预测多个 Token，然后由大型 Target Model 并行验证。如果验证通过，则一次性生成多个 Token，从而将大模型的串行推理转化为小模型的多步推理加一次并行验证。
    *   **[你的推断]** 这种方法的核心优势在于“零显式成本”的质量保证，因为最终输出完全由大模型把关，理论上不会引入额外的幻觉风险。

2.  **非自回归/并行解码：**
    *   **[事实陈述]** 通过 Mask 机制或 Jacobi 解码迭代，强制模型一次性输出 N 个 Token，并在内部通过去耦依赖关系进行并行修正。
    *   **[作者观点]** 这种方法直接挑战了 Transformer 的自回归本性，将解码复杂度从 $O(N)$ 降至 $O(1)$（常数次迭代），是长文本生成的终极解决方案。

3.  **KV Cache 优化：**
    *   **[事实陈述]** 如 Multi-Query Attention (MQA) 或 Grouped-Query Attention (GQA)，通过减少 KV Cache 的显存占用和读写带宽，间接提升了推理吞吐量。
    *   **[你的推断]** 虽然不如前两者“性感”，但这往往是工程落地中性价比最高的手段，因为它不改变模型架构，仅需推理框架支持。

**反例与边界条件：**

1.  **投机采样的失效场景（反例）：**
    *   **[事实陈述]** 当 Draft Model 的准确率低于 50%-60% 时，验证开销超过收益，推理速度反而变慢。
    *   **[你的推断]** 在创意性极强或逻辑跳跃极大的文本生成中，小模型很难猜中大模型的下一个词，导致“投机失败”。

2.  **非自回归的质量塌陷（反例）：**
    *   **[事实陈述]** 并行解码在处理长尾依赖时容易出现“复读机”现象或逻辑断裂。
    *   **[边界条件]** 这种方法通常需要数轮迭代 refining，如果迭代次数过多，延迟可能高于原始的自回归解码。

---

### 二、 多维深度评价

#### 1. 内容深度：观点的深度和论证的严谨性
该类文章通常触及了 LLM 推理的“阿喀琉斯之踵”——显存墙与带宽墙。
*   **深度分析：** 文章若仅停留在“速度快”是浅层的。真正的深度在于探讨**“计算-通信比”**。投机采样本质上是用 Draft Model 的计算量换取 Target Model 的通信带宽（因为验证阶段是并行矩阵乘法）。文章如果能深入分析在显存受限（如消费者显卡）与计算受限（如 H100 集群）下的不同表现，则具备极高的技术深度。
*   **严谨性：** 需警惕幸存者偏差。许多文章仅展示 Draft Model 表现良好的案例，而忽略了在数学推理或代码生成等高难度任务中，投机采样可能带来的性能抖动。

#### 2. 实用价值：对实际工作的指导意义
*   **极高。** 对于工程团队而言，投机采样是目前最容易落地的“银弹”。
*   **案例说明：** Medusa 算法（一种不使用独立 Draft Model，而是在大模型头上加多个解码头的方法）证明了不需要训练两个模型就能实现 2x-3x 的加速。这直接降低了部署成本，使得在单张 4090 上运行 70B 模型成为可能。

#### 3. 创新性：提出了什么新观点或新方法
*   **范式转移：** 传统的优化集中在 FlashAttention、PagedAttention 等算子层面。而该文章探讨的“Trick”代表了**架构层面的创新**。
*   **新观点：** 提出了“推理不一定非要由大模型全程主导”。这是一种模型协作的新思路，类似于 MoE（混合专家）在推理阶段的应用——让小模型处理简单模式，大模型仅负责纠错和生成复杂模式。

#### 4. 可读性：表达的清晰度和逻辑性
此类技术文章通常面临“数学门槛”。
*   **清晰度：** 优秀的文章应避免堆砌公式，转而使用“并行验证”、“一次生成多词”等直观概念。
*   **逻辑性：** 建议采用“问题-方案-验证-局限”的闭环结构。特别是在解释 Jacobi 迭代或 Tree Mask 时，应辅以图表说明 Token 依赖关系的解耦过程，否则读者极易在并行逻辑中迷失。

---

### 三、 总结与建议

**总体评价：**
这篇文章（或该技术方向）揭示了 LLM 推理优化的新边疆。它不再局限于 squeezing the hardware（压榨硬件），而是开始 rethinking the generation process（重塑生成过程）。

**改进建议：**
1.  **补充量化数据：** 建议增加在不同 Batch Size 和不同上下文长度下的延迟对比曲线。
2.  **讨论工程开销：** 投机采样需要维护两个模型实例，这对显存容量的要求是否反而抵消了速度优势？这是一个值得深入探讨的 Trade

---
## 代码示例




```python
# 示例1：KV Cache优化
def kv_cache_example():
    import torch
    import torch.nn as nn
    
    class SimpleLLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.key_cache = []
            self.value_cache = []
            
        def forward(self, x):
            # 模拟计算key和value
            k, v = torch.randn(x.size(0), 10), torch.randn(x.size(0), 10)
            
            # 缓存key和value
            self.key_cache.append(k)
            self.value_cache.append(v)
            
            # 使用缓存的key和value计算注意力
            cached_k = torch.cat(self.key_cache, dim=0)
            cached_v = torch.cat(self.value_cache, dim=0)
            return cached_k, cached_v
    
    model = SimpleLLM()
    input_tensor = torch.randn(5, 10)
    output = model(input_tensor)
    print(f"缓存的Key形状: {output[0].shape}, Value形状: {output[1].shape}")
```




```python
# 示例2：动态批处理
def dynamic_batching_example():
    import time
    from collections import defaultdict
    
    class RequestBatcher:
        def __init__(self, max_batch_size=4, wait_time=0.1):
            self.max_batch_size = max_batch_size
            self.wait_time = wait_time
            self.requests = []
            
        def add_request(self, request):
            self.requests.append(request)
            if len(self.requests) >= self.max_batch_size:
                return self.process_batch()
            return None
            
        def process_batch(self):
            batch = self.requests[:self.max_batch_size]
            self.requests = self.requests[self.max_batch_size:]
            # 模拟批处理
            time.sleep(self.wait_time)
            return f"处理批次: {len(batch)}个请求"
    
    batcher = RequestBatcher()
    for i in range(10):
        result = batcher.add_request(f"请求{i+1}")
        if result:
            print(result)
```




```python
# 示例3：量化加速
def quantization_example():
    import torch
    import torch.nn as nn
    
    class QuantizedLinear(nn.Module):
        def __init__(self, in_features, out_features):
            super().__init__()
            self.weight = nn.Parameter(torch.randn(out_features, in_features))
            self.scale = nn.Parameter(torch.randn(out_features, 1))
            
        def forward(self, x):
            # 模拟8位量化计算
            quantized_weight = torch.round(self.weight / self.scale).to(torch.int8)
            return torch.matmul(x, quantized_weight.float() * self.scale)
    
    # 比较原始层和量化层
    original_layer = nn.Linear(10, 5)
    quantized_layer = QuantizedLinear(10, 5)
    quantized_layer.weight.data = original_layer.weight.data.clone()
    
    input_tensor = torch.randn(2, 10)
    print(f"原始输出: {original_layer(input_tensor).shape}")
    print(f"量化输出: {quantized_layer(input_tensor).shape}")
```


---
## 案例研究


### 1：Character.AI - 大规模实时对话系统

 1：Character.AI - 大规模实时对话系统

**背景**: Character.AI 是一个允许用户与 AI 角色进行实时互动的平台，每天处理数十亿次对话请求。随着用户量激增，其基于大语言模型（LLM）的对话系统面临巨大的算力成本和延迟挑战。

**问题**: 在标准 GPU 上运行大模型推理速度较慢，无法满足实时聊天的低延迟要求（通常需要低于 100ms）。同时，为了维持模型的创造性和多样性，无法简单地通过减小模型尺寸来解决。

**解决方案**: Character.AI 采用了激进的多项采样策略结合 TensorRT-LLM 等高效推理引擎。他们通过优化 Transformer 架构的 KV Cache 机制，并实施连续批处理以最大化 GPU 利用率。此外，他们还采用了多 GPU 推理并行化技术，将单个大模型的计算负载分散到多个 GPU 上，从而显著降低单个请求的延迟。

**效果**: 通过这些优化，Character.AI 成功地将推理延迟降低到了用户几乎无法感知的程度，实现了流畅的实时对话体验。这不仅提升了用户留存率，还大幅降低了每次对话的算力成本，使得在消费级硬件上运行复杂模型成为可能。

---



### 2：LMSYS Org - Vicuna 模型与 Chatbot Arena

 2：LMSYS Org - Vicuna 模型与 Chatbot Arena

**背景**: LMSYS Org 是一个由加州大学伯克利分校师生发起的研究组织，致力于开发开放的 LLM 评估工具和模型。他们维护的 Chatbot Arena 需要为全球用户提供与不同开源模型（如 Vicuna、Llama）进行实时对比测试的能力。

**问题**: 运行 Chatbot Arena 需要同时服务大量并发用户，且资源有限。开源模型通常未经高度优化，直接部署会导致显存占用过高（OOM）和吞吐量低下，无法应对高峰期的访问流量。

**解决方案**: LMSYS 开发了 FastChat 服务平台，集成了 vLLM 作为核心推理引擎。vLLM 引入了 PagedAttention 算法，这是一种受操作系统虚拟内存启发的注意力机制优化。它有效地解决了显存碎片化问题，允许系统在不牺牲生成速度的情况下，将批处理大小提高了数倍。

**效果**: 使用 vLLM 后，Chatbot Arena 的吞吐量提升了约 10-20 倍，显存利用率显著提高。这使得 LMSYS 能够在有限的 GPU 资源下，为数百万用户提供稳定的模型评估服务，极大地加速了开源 LLM 的研究和迭代进程。

---
## 最佳实践

## 最佳实践指南

### 实践 1：KV Cache 优化

**说明**:  
KV Cache 是一种缓存机制，用于存储模型在生成过程中的键值对，避免重复计算。通过缓存这些中间结果，可以显著减少推理延迟，特别是在长文本生成场景中效果明显。

**实施步骤**:
1. 在模型推理框架中启用 KV Cache 功能（如 Hugging Face Transformers 的 `use_cache=True`）。
2. 根据硬件资源调整缓存大小，避免内存溢出。
3. 对生成的文本进行分批处理时，确保缓存正确共享。

**注意事项**:  
- KV Cache 会占用额外内存，需在速度和内存之间权衡。
- 对于动态长度的输入，需动态调整缓存策略。

---

### 实践 2：模型量化

**说明**:  
模型量化是通过降低模型参数的精度（如从 32 位浮点数降至 8 位整数）来减少计算量和内存占用。量化后的模型推理速度更快，且对精度影响较小。

**实施步骤**:
1. 使用量化工具（如 TensorFlow Lite、ONNX Runtime 或 PyTorch 的量化模块）。
2. 选择适合的量化方法（如动态量化或静态量化）。
3. 在验证集上评估量化后的模型性能，确保精度损失在可接受范围内。

**注意事项**:  
- 静态量化需要校准数据集，动态量化无需校准但可能性能稍差。
- 某些硬件（如 GPU）对低精度计算支持更好，量化效果更佳。

---

### 实践 3：批处理推理

**说明**:  
批处理推理是将多个输入请求合并为一个批次进行处理，充分利用硬件并行计算能力。这种方法可以显著提高吞吐量，尤其适用于高并发场景。

**实施步骤**:
1. 根据硬件资源（如 GPU 内存）确定合适的批次大小。
2. 使用支持批处理的推理框架（如 NVIDIA Triton Inference Server）。
3. 对输入数据进行预处理（如填充或截断），确保批次内数据长度一致。

**注意事项**:  
- 批次大小过大会导致内存不足或延迟增加。
- 动态批处理（Dynamic Batching）可以根据请求负载自动调整批次大小。

---

### 实践 4：稀疏注意力机制

**说明**:  
稀疏注意力机制通过减少注意力计算中的非零元素数量来降低计算复杂度。这种方法特别适合长序列处理，可以显著加速推理。

**实施步骤**:
1. 选择支持稀疏注意力的模型架构（如 Longformer 或 BigBird）。
2. 在训练或微调阶段引入稀疏注意力模式。
3. 在推理时，根据输入长度动态调整稀疏模式。

**注意事项**:  
- 稀疏注意力可能影响模型精度，需在任务中验证。
- 某些硬件对稀疏计算优化不足，需测试实际性能。

---

### 实践 5：模型蒸馏

**说明**:  
模型蒸馏是通过训练一个较小的“学生模型”来模仿大型“教师模型”的行为。蒸馏后的模型体积更小、推理更快，同时保留大部分性能。

**实施步骤**:
1. 选择一个大型预训练模型作为教师模型。
2. 设计一个较小的学生模型架构。
3. 使用教师模型的输出作为软标签训练学生模型。

**注意事项**:  
- 蒸馏过程需要额外的计算资源和时间。
- 学生模型的表现可能无法完全达到教师模型水平。

---

### 实践 6：硬件加速

**说明**:  
利用专用硬件（如 GPU、TPU 或 AI 加速卡）可以显著提升 LLM 推理速度。硬件加速结合优化软件栈（如 CUDA、TensorRT）效果更佳。

**实施步骤**:
1. 根据需求选择合适的硬件（如 NVIDIA GPU 或 Google TPU）。
2. 安装对应的优化库（如 CUDA、cuDNN 或 TensorRT）。
3. 将模型转换为硬件支持的格式（如 ONNX 或 TensorRT 引擎）。

**注意事项**:  
- 硬件成本较高，需评估性价比。
- 某些硬件对特定模型格式或精度支持有限。

---

### 实践 7：动态计算图优化

**说明**:  
动态计算图优化通过减少不必要的计算节点或融合操作来提升推理效率。这种方法适合框架原生支持动态图的模型（如 PyTorch）。

**实施步骤**:
1. 使用工具（如 TorchScript 或 ONNX）将动态图转换为静态图。
2. 启用图优化选项（如操作融合或常量折叠）。
3. 在推理时使用优化后的静态图。

**注意事项**:  
- 静态图可能限制模型的灵活性，需权衡。
- 某些优化可能导致数值不稳定，需验证结果。

---
## 学习要点

- KV Cache 通过缓存每个 token 的历史键值对，避免在生成长序列时重复计算，将计算复杂度从平方级降低至线性级。
- Speculative Decoding 利用一个小型模型快速草拟多个 token，然后由大型模型并行验证，显著减少了生成延迟。
- Continuous Batching 允许在同一个批次中动态插入和移除请求，解决了因单个长序列导致整体 GPU 利用率低下的问题。
- Flash Attention 通过优化内存访问模式（将注意力计算分块至 SRAM），大幅减少了注意力机制在 HBM 读写上的瓶颈。
- 量化技术（如 INT8/FP4）通过降低模型权重和激活值的精度，在几乎不损失精度的前提下减少了显存占用并提升了计算速度。
- Multi-Query Attention (MQA) 或 Grouped-Query Attention (GQA) 通过减少注意力头中 Key 和 Value 矩阵的存储量，大幅降低了推理时的显存带宽压力。

---
## 常见问题


### 1: 什么是 LLM 推理中的 KV Cache（键值缓存），为什么它对加速至关重要？

1: 什么是 LLM 推理中的 KV Cache（键值缓存），为什么它对加速至关重要？

**A**: KV Cache 是 Transformer 架构中一种标准的内存优化技术，也是实现快速推理的基础。在生成文本时，模型采用自回归方式，即每生成一个新词，都需要基于之前所有的上下文进行计算。如果不使用缓存，每生成一个新 token，模型都需要重新计算之前所有 token 的 Key 和 Value 矩阵，导致计算量随生成长度呈二次方增长。

KV Cache 的作用是在第一轮计算时存储每一层的 Key 和 Value 向量。在后续生成新 token 时，只需将新 token 的 Key/Value 与缓存中的历史数据拼接，从而避免重复计算。这虽然增加了显存占用，但将计算复杂度从 $O(N^2)$ 降低到了 $O(N)$，极大提升了生成速度。

---



### 2: 什么是 Multi-Query Attention (MQA) 和 Grouped-Query Attention (GQA)，它们如何加速推理？

2: 什么是 Multi-Query Attention (MQA) 和 Grouped-Query Attention (GQA)，它们如何加速推理？

**A**: 这两种技术主要通过改变 Attention 头的数量来减少显存访问带宽（即内存墙）的瓶颈，从而加速推理。

在标准的 Multi-Head Attention (MHA) 中，每个 Attention 头都有自己独立的 Key 和 Value 矩阵。这意味着随着头数增加，KV Cache 的大小也会成倍增加，导致显存读写速度成为瓶颈。

Multi-Query Attention (MQA) 让所有的 Attention 头共享同一组 Key 和 Value 矩阵。这样 KV Cache 的大小被大幅压缩，显存读写量大幅减少，从而显著提高推理吞吐量。Grouped-Query Attention (GQA) 则是 MHA 和 MQA 的折中方案，它将 Query 头分组，每组内的头共享一组 Key 和 Value 矩阵。GQA 在保持 MQA 的速度优势的同时，比 MQA 保留了更多的模型表达能力，推理质量通常比单纯的 MQA 更好。

---



### 3: 什么是 Continuous Batching（连续批处理）或 Dynamic Batching（动态批处理）？

3: 什么是 Continuous Batching（连续批处理）或 Dynamic Batching（动态批处理）？

**A**: 传统的 LLM 服务通常使用 Static Batching（静态批处理），即必须凑齐一批请求或等待所有请求都处理完同一时间步后，才能一起进入下一步计算。这种方式在处理长短不一的请求时效率极低，因为短的请求必须等待长的请求完成后才能释放资源。

Continuous Batching（在 vLLM 等框架中也称为 Iteration-Level Scheduling）允许在批次内的某些序列生成结束后，立即插入新的序列进入批次。系统不再等待整个批次完成，而是在每个迭代步骤（生成一个 token）后动态调整批次中的请求。这种技术极大提高了 GPU 的利用率，特别是在高并发、请求长度差异大的在线服务场景中，能将吞吐量提升数倍。

---



### 4: 什么是 Speculative Decoding（推测解码）？

4: 什么是 Speculative Decoding（推测解码）？

**A**: Speculative Decoding 是一种利用小模型来辅助大模型进行快速生成的“以小博大”技术。

其核心思想是使用一个参数量较小、速度极快的“草稿模型”提前生成多个 token，然后并行地将这些 token 交给“大模型”进行验证。大模型只需一次性运行就能确认草稿模型生成的多个 token 是否正确。如果验证通过，就直接采用这些 token，从而实现了在一个大模型推理步骤中生成多个 token 的效果。如果验证失败，则回退到正确的 token 并重新生成。这种方法在保持大模型生成质量不变的前提下，能显著提升生成速度。

---



### 5: 什么是 Flash Attention，它与普通 Attention 有何不同？

5: 什么是 Flash Attention，它与普通 Attention 有何不同？

**A**: Flash Attention 是一种针对 Attention 机制的底层算子优化，主要解决 GPU 显存（HBM）与片上缓存（SRAM）之间读写速度不匹配的问题。

标准的 Attention 实现通常需要将巨大的 Attention 矩阵（$N \times N$）写入显存（HBM），这非常耗时。Flash Attention 通过对计算步骤进行平铺和重计算，利用 GPU 的片上 SRAM 来处理 Attention 矩阵的分块，极大地减少了 HBM 的读写次数。这不仅显著提升了推理速度，还因为减少了中间结果的显存占用，使得系统能够支持更长的上下文长度。

---



### 6: 什么是量化，常见的 4-bit 量化是如何工作的？

6: 什么是量化，常见的 4-bit 量化是如何工作的？

**A**: 量化是指降低模型参数的数值精度，例如将标准的 16-bit 浮点数（FP16）或 32-bit 浮点数（FP32）参数转换为 4-bit 整数（INT4）。

4-bit 量化通过将参数的数值范围映射到仅有的 16 个离散级别（$2^4$）来工作。虽然这会损失一定的数值精度，从而可能导致模型输出质量轻微下降，但它能将模型显存占用减少约 75%。显存占用的减少意味着更大的批次可以放入 GPU，或者显存带宽压力降低，从而直接转化为推理速度的提升。现代量化技术（如 GPTQ、AWQ）还能最小化这种精度损失，使得 4-bit 模型在保持近乎原版性能的同时，实现极快的推理速度。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在 LLM 推理中，KV Cache（键值缓存）是优化生成速度的核心技术。请解释 KV Cache 具体缓存了哪些数据，以及它是如何避免在生成每一个新 token 时进行重复计算的。

### 提示**: 关注 Transformer 架构中的自注意力机制。思考在解码阶段，当序列长度增加 1 时，哪些矩阵乘法的结果是可以被复用的，而不需要重新对整个历史序列进行计算。

### 

---
## 引用

- **原文链接**: [https://www.seangoedecke.com/fast-llm-inference](https://www.seangoedecke.com/fast-llm-inference)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47022329](https://news.ycombinator.com/item?id=47022329)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [LLM](/tags/llm/) / [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [KV Cache](/tags/kv-cache/) / [量化](/tags/%E9%87%8F%E5%8C%96/) / [Flash Attention](/tags/flash-attention/) / [PagedAttention](/tags/pagedattention/) / [vLLM](/tags/vllm/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Nano-vLLM 技术解析：vLLM 风格推理引擎的运行机制]({{< relref "posts/20260203-hacker_news-nano-vllm-how-a-vllm-style-inference-engine-works-13.md" >}})
- [Nano-vLLM 原理：解析 vLLM 风格推理引擎机制]({{< relref "posts/20260202-hacker_news-nano-vllm-how-a-vllm-style-inference-engine-works-0.md" >}})
- [Nano-vLLM 原理剖析：vLLM 风格推理引擎的实现机制]({{< relref "posts/20260202-hacker_news-nano-vllm-how-a-vllm-style-inference-engine-works-3.md" >}})
- [Nano-vLLM 原理：vLLM 风格推理引擎的实现机制]({{< relref "posts/20260203-hacker_news-nano-vllm-how-a-vllm-style-inference-engine-works-9.md" >}})
- [两种加速大模型推理的技术方法]({{< relref "posts/20260215-hacker_news-two-different-tricks-for-fast-llm-inference-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*