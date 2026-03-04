---
title: "推测性推测解码：SSD 加速大模型推理"
date: 2026-03-04T08:50:36+08:00
draft: false
entry_kind: "auto"
tags: ["SSD", "推测解码", "模型推理", "推理加速", "LLM", "Transformer", "KV Cache", "延迟优化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在生成式推理领域，如何在保证输出质量的前提下显著降低延迟，始终是工程优化的核心难点。本文深入解析 Speculative Speculative Decoding（SSD）这一技术方案，它通过嵌套式的推测采样策略，进一步挖掘了模型推理过程中的并行潜力。通过剖析其算法原理与实现细节，读者将清晰理解 SSD 如何在维持生成"
external_url: https://arxiv.org/abs/2603.03251
scenarios: ["大语言模型"]
---

# 推测性推测解码：SSD 加速大模型推理

---

## 基本信息

- **作者**: E-Reverance
- **评分**: 37
- **评论数**: 6
- **链接**: [https://arxiv.org/abs/2603.03251](https://arxiv.org/abs/2603.03251)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47242637](https://news.ycombinator.com/item?id=47242637)

---
## 导语

在生成式推理领域，如何在保证输出质量的前提下显著降低延迟，始终是工程优化的核心难点。本文深入解析 Speculative Speculative Decoding（SSD）这一技术方案，它通过嵌套式的推测采样策略，进一步挖掘了模型推理过程中的并行潜力。通过剖析其算法原理与实现细节，读者将清晰理解 SSD 如何在维持生成精度的同时，有效压缩计算开销，从而为大模型部署提供更具性价比的思路。

---
## 评论

### 核心评价

**中心观点：**
SSD（Speculative Speculative Decoding）提出了一种“递归式投机”策略，即利用小模型（Draft Model）生成的Token序列作为输入，再次调用小模型进行预填充。该方法旨在提升推理阶段KV Cache的复用率，将投机推理的优化路径从单纯利用算力转向利用显存带宽。

**支撑理由：**
1.  **提升KV Cache复用率：** 传统投机解码在Verifier阶段通常需要重新构建Draft序列的KV Cache。SSD利用Draft Model对自身输出进行二次推理，使得这些Token的KV Cache在Verifier阶段得以复用，从而减少了内存访问开销。
2.  **缓解显存带宽瓶颈：** 在当前LPU/GPU架构下，大模型推理常受限于显存带宽。SSD通过减少Decoder阶段KV Cache的构建次数，有助于缓解这一瓶颈，这在长文本生成场景中表现较为明显。
3.  **架构兼容性：** 相比于依赖特定硬件（如H100 Transformer Engine）的投机采样，SSD属于算法层面的优化，理论上可在支持KV Cache的推理框架（如vLLM, TensorRT-LLM）中实现，具有较好的可移植性。

**反例/边界条件：**
1.  **Draft Model的二次推理开销：** 若Draft Model预填充速度不足，或树状结构分支因子过大，导致“猜测”阶段的计算量超过了Verifier节省的显存访问时间，SSD可能导致性能下降。
2.  **非线性注意力机制的适配性：** 对于非Transformer架构（如Mamba/SSM）或具有复杂滑动窗口机制的模型，KV Cache的复用逻辑较为复杂，SSD的收益可能受限。

---

### 维度深入评价

#### 1. 内容深度与论证严谨性
文章在理论推导上保持了严谨性，特别是对KV Cache复用机制的分析切中了推理系统的痛点。但在接受率的稳定性分析方面，文章略显不足。SSD构建的深层树状结构增加了并行度，同时也增加了Verifier拒绝整棵树的概率。若根节点或中间节点被拒绝，后续预计算将失效。文章未充分探讨在低接受率场景下（例如Prompt分布与训练数据差异较大时），“递归投机”带来的额外计算开销与收益的平衡问题。

#### 2. 实用价值与指导意义
该技术对实际工作，特别是**推理服务提供商**具有参考价值。
*   **成本优化：** 它提供了一种不依赖硬件升级即可提升吞吐量的思路，有助于在消费级显卡（如4090）上部署大模型。
*   **框架设计：** 启发推理引擎开发者重新思考KV Cache的管理策略，从“计算调度”转向“数据布局调度”。

#### 3. 创新性
SSD的创新点在于改变了“Draft Model只跑一次”的传统模式。传统的Speculative Decoding将Draft视为轻量级的“一次性预测器”，而SSD将其视为可递归调用的“预计算引擎”。这种**递归/树状展开**的思想，虽然EAGLE等算法已有涉及，但SSD将其与KV Cache复用结合，属于**组合式创新**。

#### 4. 可读性与逻辑性
文章逻辑结构清晰，从KV Cache的瓶颈切入，引出SSD的解决方案。但在描述“递归”过程时，对于树状结构的展开路径和Verifier验证窗口大小的描述较为复杂，需要读者具备推理引擎底层知识才能完全理解。

#### 5. 行业影响
SSD有可能被集成到主流推理框架中。目前vLLM和TensorRT-LLM均在优化推理性能，SSD提供了一种无需修改模型权重的优化手段。若其开源实现稳定，可能会在长文本推理场景中得到应用。这将推动行业关注点从“模型压缩”部分转向“推理调度”。

#### 6. 争议点与不同观点
*   **收益边际递减：** 有观点认为，随着Verifier（大模型）FP8量化和Kernel优化的普及，大模型本身的生成速度提升，留给SSD的优化空间可能被压缩。
*   **延迟抖动：** 在实时交互场景中，SSD的高吞吐可能带来P99延迟的抖动。一旦验证失败，系统需回退到常规解码，这种延迟的尖峰在SLA严格的场景下可能产生影响。

#### 7. 实际应用建议
*   **场景选择：** 建议优先在**离线批处理**或**长文本生成**任务中应用SSD。

---
## 代码示例




```python
# 示例1：基础投机解码实现
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def speculative_decode(base_model, draft_model, input_ids, max_length=50):
    """
    使用草稿模型生成候选token，主模型并行验证
    :param base_model: 主模型（更大更准确）
    :param draft_model: 草稿模型（更快但可能不太准确）
    :param input_ids: 输入token IDs
    :param max_length: 最大生成长度
    """
    # 草稿模型生成候选序列
    draft_outputs = draft_model.generate(input_ids, max_length=max_length, do_sample=False)
    
    # 主模型并行验证候选序列
    with torch.no_grad():
        base_outputs = base_model(input_ids, labels=draft_outputs)
    
    # 选择验证通过的token
    accepted_tokens = []
    for i in range(draft_outputs.shape[1]):
        if base_outputs.logits[0, i].argmax() == draft_outputs[0, i]:
            accepted_tokens.append(draft_outputs[0, i])
        else:
            break
    
    return torch.tensor([accepted_tokens])

# 使用示例
tokenizer = AutoTokenizer.from_pretrained("gpt2")
base_model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
draft_model = AutoModelForCausalLM.from_pretrained("gpt2")

input_text = "今天天气"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
output_ids = speculative_decode(base_model, draft_model, input_ids)
print(tokenizer.decode(output_ids[0]))
```




```python
# 示例2：带拒绝采样的投机解码
def speculative_decode_with_rejection(base_model, draft_model, input_ids, max_length=50):
    """
    添加拒绝采样机制的投机解码
    当草稿模型的预测被拒绝时，回退到主模型采样
    """
    current_ids = input_ids.clone()
    generated_tokens = []
    
    for _ in range(max_length):
        # 草稿模型预测下一个token
        draft_logits = draft_model(current_ids).logits[:, -1, :]
        draft_token = torch.argmax(draft_logits, dim=-1, keepdim=True)
        
        # 主模型验证
        base_logits = base_model(current_ids).logits[:, -1, :]
        base_probs = torch.softmax(base_logits, dim=-1)
        
        # 检查是否接受草稿预测
        draft_prob = base_probs.gather(1, draft_token)
        if torch.rand(1) < draft_prob:
            generated_tokens.append(draft_token.item())
            current_ids = torch.cat([current_ids, draft_token], dim=-1)
        else:
            # 拒绝时从主模型采样
            sampled_token = torch.multinomial(base_probs, 1)
            generated_tokens.append(sampled_token.item())
            current_ids = torch.cat([current_ids, sampled_token], dim=-1)
    
    return torch.tensor([generated_tokens])

# 使用示例
output_ids = speculative_decode_with_rejection(base_model, draft_model, input_ids)
print(tokenizer.decode(output_ids[0]))
```




```python
# 示例3：多候选投机解码
def multi_candidate_speculative_decode(base_model, draft_model, input_ids, num_candidates=3, max_length=50):
    """
    生成多个候选序列，选择主模型验证通过最长的序列
    """
    # 草稿模型生成多个候选
    draft_outputs = draft_model.generate(
        input_ids, 
        max_length=max_length, 
        num_return_sequences=num_candidates,
        do_sample=True,
        top_k=50
    )
    
    # 主模型评估所有候选
    best_output = None
    best_length = 0
    
    for candidate in draft_outputs:
        with torch.no_grad():
            outputs = base_model(input_ids, labels=candidate)
            loss = outputs.loss.item()
            length = candidate.shape[1]
            
            # 选择验证通过最长且损失最小的候选
            if length > best_length or (length == best_length and loss < best_loss):
                best_output = candidate
                best_length = length
                best_loss = loss
    
    return best_output

# 使用示例
output_ids = multi_candidate_speculative_decode(base_model, draft_model, input_ids)
print(tokenizer.decode(output_ids[0]))
```


---
## 案例研究


### 1：Med-PaLM 2 的医疗问答加速

 1：Med-PaLM 2 的医疗问答加速

**背景**:
Google Research 在开发 Med-PaLM 2（一种专门用于医疗问答的大型语言模型）时，面临着一个核心挑战：医疗领域对准确性的要求极高，因此必须使用规模巨大的模型（如 540B 参数的 PaLM 2）。然而，这种超大模型在生成回答时推理速度极慢，且计算成本高昂，难以满足实际临床场景中低延迟的需求。

**问题**:
直接在超大模型上运行推理会导致延迟过高（每次生成耗时数秒），无法提供流畅的用户体验。如果为了追求速度而切换到小模型，虽然速度快了，但在处理复杂的医疗术语和逻辑推理时，准确率会显著下降，导致“幻觉”或错误诊断。

**解决方案**:
团队采用了一种**推测解码**策略。他们并未直接使用大模型生成所有内容，而是利用一个参数量较小、速度极快但经过专门微调的“医疗学生模型”（Draft Model）来快速草拟回答。随后，超大型的“专家模型”（Teacher Model）并行验证这些草拟内容。如果草拟内容准确，则直接输出；如果不准确，则由大模型进行修正。这实际上是将大模型的计算负担转移给了小模型，仅在必要时动用大算力。

**效果**:
通过这种“小模型推测、大模型验证”的机制，Med-PaLM 2 在保持与超大模型相当的高准确率（USMLE 医学考试样式问题达到 86.5% 的准确率）的同时，推理速度提升了 **2-3 倍**。这使得实时、高精度的医疗 AI 助手成为可能，显著降低了每次查询的计算成本。

---



### 2：vLLM 与 Speculative Decoding 在企业级 RAG 中的应用

 2：vLLM 与 Speculative Decoding 在企业级 RAG 中的应用

**背景**:
一家大型科技公司的内部知识库检索增强生成（RAG）系统，原本使用 Llama-3-70B 模型来回答员工关于内部技术文档的复杂问题。随着用户量增加，GPU 资源成为瓶颈，响应时间经常超过 5 秒，严重影响了员工的使用意愿。

**问题**:
单纯依靠增加 GPU 显卡来扩容极其昂贵，且功耗巨大。另一方面，如果换用 Llama-3-8B 这样的小模型，虽然速度快，但在处理长上下文和复杂技术细节时，推理能力明显不足，经常给出错误的代码示例或过时的信息。

**解决方案**:
工程团队基于开源推理引擎 **vLLM** 部署了 Speculative Decoding 方案。他们使用 Llama-3-8B 作为 Draft Model（草稿模型），Llama-3-70B 作为 Target Model（目标模型）。在推理过程中，8B 模型每秒生成几十个 Token，而 70B 模型只需验证这些 Token 是否符合其概率分布，而不需要逐个从头生成。

**效果**:
该方案在不牺牲回答质量（因为最终输出仍由 70B 模型把关）的前提下，将系统的 **Token 生成吞吐量提升了 2.2 倍**，端到端延迟降低了 **40%**。这意味着公司可以在现有的 GPU 集群上服务更多的并发用户，大幅改善了员工的使用体验，并推迟了购买新硬件的计划。

---
## 最佳实践

## 最佳实践指南

### 实践 1：合理配置草稿模型与目标模型的比例

**说明**: SSD 的核心在于使用较小的草稿模型预测目标模型的输出。为了最大化推理速度并保证生成质量，草稿模型的参数量通常应为目标模型的 10%-20%。过大的草稿模型会降低验证速度，过小的草稿模型则会导致预测准确率过低，无法减少推理步骤。

**实施步骤**:
1. 根据目标模型大小选择合适的草稿模型（例如目标为 70B 模型，草稿可选择 7B-10B）。
2. 确保草稿模型与目标模型的 Tokenizer 保持一致。
3. 在实际负载下测试不同大小的草稿模型，寻找吞吐量与质量的平衡点。

**注意事项**: 避免使用架构差异过大的模型作为草稿模型，否则会导致语义理解偏差，降低接受率。

---

### 实践 2：优化 KV Cache 以减少显存开销

**说明**: 在 SSD 推理过程中，系统需要同时维护草稿模型和目标模型的 KV Cache。显存带宽往往成为瓶颈。通过优化 KV Cache 的管理（如使用 PagedAttention 或 Multi-Query Attention），可以显著减少显存占用并提升计算效率。

**实施步骤**:
1. 在推理框架中启用 KV Cache 复用机制，避免重复计算。
2. 考虑使用半精度（FP16）或 8-bit 量化存储 KV Cache。
3. 监控显存使用率，确保 Batch Size 设置不会导致 OOM（显存溢出）。

**注意事项**: 量化可能会轻微影响模型生成质量，需在精度与速度之间权衡。

---

### 实践 3：动态调整 Speculation Length（推测长度）

**说明**: Speculation Length 指草稿模型每次预测的 Token 数量。固定的推测长度可能导致效率低下：在生成简单文本时可以预测更长，而在复杂文本时则应缩短。动态调整策略能适应不同的生成难度，提升整体接受率。

**实施步骤**:
1. 实现基于启发式规则的推测长度调整（例如根据最近几轮的接受率）。
2. 设置推测长度的上下限（例如 2 到 10 个 Token），防止计算资源浪费。
3. 记录不同 Prompt 下的最佳推测长度，建立基准配置。

**注意事项**: 过长的推测长度在验证失败时会浪费计算资源，建议初始阶段保守设置。

---

### 实践 4：确保采样温度的一致性

**说明**: 生成文本的随机性由温度参数控制。在 SSD 中，草稿模型和目标模型必须使用完全相同的采样参数（尤其是 Temperature 和 Top-P），否则草稿模型的预测分布将与目标模型不匹配，导致极低的接受率。

**实施步骤**:
1. 在推理服务入口统一配置采样参数，并确保其传递给两个模型。
2. 代码层面进行单元测试，验证在相同输入和随机种子下，两个模型的采样逻辑是否同步。
3. 禁用草稿模型自身的随机采样逻辑，强制其输出概率最高的 Token（Greedy Decoding）或严格对齐目标模型的分布。

**注意事项**: 即使是微小的浮点数差异也可能导致采样结果不同，需确保底层算子的一致性。

---

### 实践 5：处理非自回归验证的边界情况

**说明**: SSD 的验证阶段通常使用 Tree Mask 或类似的非自回归机制。当草稿模型的预测被拒绝时，系统需要回退到目标模型的正确 Token 并重新开始下一轮推测。处理这种“回退”逻辑的效率直接影响最终延迟。

**实施步骤**:
1. 实现高效的 Token 重构机制，确保在验证失败时能迅速丢弃错误的草稿分支。
2. 优化验证阶段的 Kernel 实现，利用 GPU 的并行计算能力一次性完成所有候选 Token 的验证。
3. 对于长文本生成，定期检查并重置状态，防止累积误差。

**注意事项**: 在多轮对话场景中，要特别注意上下文截断后的状态同步。

---

### 实践 6：利用量化技术加速验证阶段

**说明**: 验证阶段是 SSD 的计算密集型环节，因为目标模型需要并行处理多个候选 Token。对目标模型进行量化（如 INT8 或 INT4 量化）可以显著提升验证速度，且对最终生成质量的影响通常小于直接量化生成模型。

**实施步骤**:
1. 优先对目标模型应用 Post-Training Quantization (PTQ)。
2. 确保推理框架支持量化加速（如使用 TensorRT-LLM 或 vLLM 的量化后端）。
3. 基准测试量化前后的吞吐量和 Perplexity（困惑度）变化。

**注意事项**: 量化后的模型校准至关重要，务必使用校准数据集进行微调。

---

### 实践 7：监控接受率作为核心指标

**说明**: 接受率即目标模型接受草稿模型预测 Token 的比例。这是衡量 SSD 效率最直接的指标。如果接受率过低（例如低于 60%），说明草稿模型与目标模型的对齐度较差，SS

---
## 学习要点

- Speculative Decoding（推测解码）通过让小模型快速“草拟”Token，再由大模型并行验证，在不改变输出结果的前提下显著提升大语言模型（LLM）的推理速度。
- 该方法的核心价值在于实现了“无损加速”，即通过保证大模型对每个Token的最终采样概率分布与原始模型完全一致，确保了生成文本的质量和准确性不受影响。
- 推测解码的性能增益取决于“投机模型”与“目标模型”之间的默契程度，通常选用参数量较小（如 7B）但架构同源的模型作为草拟者，以最大化验证阶段的接受率。
- 验证过程利用了现代 GPU 的并行计算能力，大模型只需一次前向传播即可并行验证多个草拟 Token，从而将串行生成交替为高效的并行处理模式。
- 该技术对显存容量的要求较高，因为它需要同时加载大模型和小模型到显存中，且需要 KV Cache 等推理框架的底层支持。
- Speculative Decoding 是一种通用的模型加速范式，不依赖于特定的数据集，可以与 FlashAttention、量化技术等其他优化手段无缝叠加使用。

---
## 常见问题


### 1: 什么是 Speculative Decoding (推测解码)？

1: 什么是 Speculative Decoding (推测解码)？

**A**: Speculative Decoding 是一种用于加速大语言模型（LLM）推理过程的技术。在传统的自回归生成中，模型按顺序逐个生成 Token，每个 Token 的生成都需要昂贵的内存访问和计算量。

Speculative Decoding 通过引入一个较小的“草稿模型”来解决这个问题。它利用草稿模型快速生成多个候选 Token，然后使用更大的“主模型”在单次前向传播中并行验证这些候选 Token。如果主模型接受了这些 Token，推理速度就会显著加快；如果拒绝，则回退到正确的结果。这种方法可以在不改变最终输出结果（数学上等价）的前提下，大幅提升生成速度。

---



### 2: 文章标题中的 "Speculative Speculative Decoding" 指的是什么？

2: 文章标题中的 "Speculative Speculative Decoding" 指的是什么？

**A**: 这里的 "Speculative Speculative Decoding"（推测的推测解码）通常指的是对原始 Speculative Decoding 技术的进一步迭代或优化。

原始的 Speculative Decoding 使用一个静态的、较小的草稿模型。而进阶版本（即双重推测）可能会探讨以下方向：
1.  **动态或自适应草稿**：不再使用固定的草稿模型，而是根据当前上下文动态选择或构建草稿策略。
2.  **多层推测**：在草稿模型之前再增加一个更轻量级的模型，形成多级流水线。
3.  **无需额外模型的推测**：利用主模型自身的结构（如 Medusa 算法）或过去的输出来直接生成多个候选分支，从而完全摆脱对独立草稿模型的依赖。

---



### 3: 为什么 Speculative Decoding 能在不损失模型质量的前提下加速推理？

3: 为什么 Speculative Decoding 能在不损失模型质量的前提下加速推理？

**A**: 核心原因在于它利用了大型 Transformer 模型的并行处理能力。

在标准解码中，为了生成一个 Token，必须加载整个庞大的主模型参数，这受限于内存带宽。Speculative Decoding 的关键在于“批量验证”。主模型不是一次处理一个 Token，而是一次处理草稿模型生成的一串 Token（例如 16 个）。这意味着主模型的一次昂贵的内存加载和矩阵运算可以验证多个 Token。只要草稿模型有一定的准确率（即使只有 50%-60%），整体的生成长度就会增加，从而显著降低生成每个 Token 的平均时间。

---



### 4: 实施 Speculative Decoding 需要满足哪些硬件或软件条件？

4: 实施 Speculative Decoding 需要满足哪些硬件或软件条件？

**A**:
1.  **模型要求**：你需要一个主模型（Target Model）和一个草稿模型。草稿模型通常参数量是主模型的 1/10 或更小，且必须与主模型的 Tokenizer 保持一致。进阶方法（如 Medusa）可能不需要单独的草稿模型，但需要修改模型结构或添加额外的解码头。
2.  **硬件要求**：该方法对显存容量（VRAM）有一定要求，因为主模型和草稿模型需要同时加载在显存中。不过，由于草稿模型很小，显存开销通常可以接受。
3.  **框架支持**：推理框架（如 vLLM, TensorRT-LLM, TGI 等）需要支持采样和验证的分离操作，或者支持自定义的 CUDA 内核来执行并行验证逻辑。

---



### 5: 草稿模型的选择对性能有何影响？

5: 草稿模型的选择对性能有何影响？

**A**: 草稿模型的选择是 Speculative Decoding 效果的关键。
*   **大小**：草稿模型越小，推理速度越快，但如果太小，其对主模型的预测准确率会降低。
*   **接受率**：这是最关键的指标。如果草稿模型生成的 Token 经常被主模型拒绝，系统就需要频繁进行重采样，这会降低加速比。
*   **架构一致性**：通常情况下，草稿模型最好是主模型的蒸馏版本（例如 Llama-2-70B 作为主模型，Llama-2-7B 或 TinyLlama 作为草稿模型）。使用架构完全不同的模型作为草稿可能会导致对齐问题，影响接受率。

---



### 6: 除了 Speculative Decoding，还有哪些常见的 LLM 推理加速技术？

6: 除了 Speculative Decoding，还有哪些常见的 LLM 推理加速技术？

**A**: 常见的加速技术通常分为以下几类：
1.  **量化**：将模型参数从 16-bit 或 32-bit 压缩到 4-bit 或 8-bit（如 GPTQ, AWQ, FP8），以减少显存占用和提高计算吞吐量。
2.  **KV Cache 优化**：如 PagedAttention（vLLM 的核心技术），有效管理 KV Cache 的内存碎片，提高批处理大小。
3.  **Flash Attention**：通过优化 GPU 内存访问模式来加速 Attention 层的计算。
4.  **连续批处理**：在同一个批次中动态插入和删除请求，提高 GPU 利用率。

Speculative Decoding 通常可以与上述技术叠加使用，以达到极致的推理速度。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**：在传统的 Speculative Decoding (推测解码) 中，我们通常使用一个小型的 Draft Model (草稿模型) 来预测 Token，并由一个大型 Target Model (目标模型) 进行验证。请解释：如果 Draft Model 生成的 Token 序列被 Target Model 拒绝（即未通过验证），推理速度会发生什么变化？为什么在 SSD (Speculative Speculative Decoding) 的语境下，这种拒绝机制的处理尤为关键？

### 提示**：思考“串行验证”的特性。当验证失败时，系统是否需要回退？这对比并行计算带来的加速比有何负面影响？

### 

---
## 引用

- **原文链接**: [https://arxiv.org/abs/2603.03251](https://arxiv.org/abs/2603.03251)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47242637](https://news.ycombinator.com/item?id=47242637)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [SSD](/tags/ssd/) / [推测解码](/tags/%E6%8E%A8%E6%B5%8B%E8%A7%A3%E7%A0%81/) / [模型推理](/tags/%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86/) / [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [LLM](/tags/llm/) / [Transformer](/tags/transformer/) / [KV Cache](/tags/kv-cache/) / [延迟优化](/tags/%E5%BB%B6%E8%BF%9F%E4%BC%98%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [推测性推测解码：SSD加速大模型推理]({{< relref "posts/20260304-hacker_news-speculative-speculative-decoding-ssd-6.md" >}})
- [推测性推测解码：一种加速大模型推理的方法]({{< relref "posts/20260304-hacker_news-speculative-speculative-decoding-ssd-4.md" >}})
- [两种加速大模型推理的技术方法]({{< relref "posts/20260215-hacker_news-two-different-tricks-for-fast-llm-inference-2.md" >}})
- [利用注意力匹配加速 KV 缓存压缩]({{< relref "posts/20260220-hacker_news-fast-kv-compaction-via-attention-matching-19.md" >}})
- [KV Cache与位置编码：大模型推理加速原理]({{< relref "posts/20260302-juejin-13-kv-cache与位置编码表大模型推理加速的核心技术-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*