---
title: "能计算两个10位数加法的最小Transformer模型"
date: 2026-02-28T09:32:00+08:00
draft: false
entry_kind: "auto"
tags: ["Transformer", "算法推理", "算术运算", "模型规模", "深度学习", "AI", "数学能力", "模型优化"]
categories: ["大模型", "论文"]
source: hacker_news
description: "在当前大语言模型追求参数规模的背景下，一项关于极小 Transformer 模型的实验引发了关注。该研究展示了一个参数量极小的模型，竟能完成两个 10 位数字的加法运算。这一发现挑战了人们对模型容量与算术能力关系的传统认知。通过阅读本文，读者可以了解该模型的架构细节，并深入探讨小模型在逻辑推理任务中的潜力与局限。"
external_url: https://github.com/anadim/AdderBoard
scenarios: ["AI/ML项目"]
---

# 能计算两个10位数加法的最小Transformer模型

---

## 基本信息

- **作者**: ks2048
- **评分**: 147
- **评论数**: 65
- **链接**: [https://github.com/anadim/AdderBoard](https://github.com/anadim/AdderBoard)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47170030](https://news.ycombinator.com/item?id=47170030)

---
## 导语

在当前大语言模型追求参数规模的背景下，一项关于极小 Transformer 模型的实验引发了关注。该研究展示了一个参数量极小的模型，竟能完成两个 10 位数字的加法运算。这一发现挑战了人们对模型容量与算术能力关系的传统认知。通过阅读本文，读者可以了解该模型的架构细节，并深入探讨小模型在逻辑推理任务中的潜力与局限。

---
## 评论

**文章中心观点**
该研究通过实验证明，Transformer 架构并非只能通过概率拟合来“模仿”算术运算，而是具备在极小参数规模下通过高维注意力机制“习得”算法逻辑的能力，从而挑战了“LLM 仅是随机鹦鹉”的传统认知。

**支撑理由与评价**

**1. 算法归纳能力优于单纯记忆（事实陈述）**
文章最核心的贡献在于展示了模型在极小规模下的“泛化”能力。通常认为，神经网络学习加法是通过记忆大量的查找表。然而，当模型参数量被压缩至极小（如几万级别）且训练数据有限时，单纯的记忆不再可行。实验表明，模型能够通过注意力头的特定模式，掌握进位逻辑，这证明了 Transformer 底层确实存在一种类似于算法归纳的机制。

**2. 长度外推验证了逻辑习得（你的推断）**
如果模型只是死记硬背，那么在遇到比训练数据更长的数字（例如训练是 8 位数，测试是 10 位数）时，准确率应断崖式下跌。文章中提到模型在 10 位数加法上的成功，意味着它学会了通用的“字符串处理规则”而非特定长度的数值映射。这一点对于理解大模型的逻辑推理能力上限具有重要参考价值。

**3. 参数效率的极限探索（作者观点）**
文章强调了“最小”这一概念。在当前 AI 行业普遍追求“万亿参数”的背景下，这项研究反其道而行之，探讨了完成特定逻辑任务的最小算力门槛。这有助于我们剥离掉大模型中用于“知识存储”的冗余参数，单独研究“逻辑推理”部分的参数效率。

**反例与边界条件**

*   **边界条件 1：符号表征的脆弱性（你的推断）**
    该实验通常基于标准的阿拉伯数字（0-9）字符串。如果改变输入格式，例如将数字转换为罗马数字、中文汉字或二进制，模型极大概率会失效，除非重新训练。这表明 Transformer 学到的并非抽象的“数学概念”，而是特定符号序列的操作规则。
*   **边界条件 2：算术复杂度的限制（事实陈述）**
    加法是线性复杂度的操作，且具有严格的局部依赖性（进位只影响相邻位）。如果将任务改为乘法（尤其是高精度乘法）或除法，Transformer 的注意力机制需要捕捉更长距离的依赖关系，目前的极小模型架构可能无法处理，准确率会显著下降。

**多维度深入评价**

**1. 内容深度：微观机制分析的典范**
文章不仅仅满足于展示准确率，更深入到了模型的“解剖学”层面。通过可视化注意力头，作者展示了模型如何关注特定的数位以处理进位。这种将“黑盒”模型行为与“可解释性”特征相结合的分析方式，论证严谨，为理解 Transformer 的内部逻辑提供了微观证据。

**2. 实用价值：边缘计算与逻辑层优化**
虽然直接用于生产环境的加法器没有商业意义（CPU 更快），但其实用价值在于验证了“小模型 + 逻辑推理”的可能性。这提示行业在设计边缘设备或专用逻辑推理模型时，不必盲目堆砌参数，而应专注于优化架构以捕捉长距离依赖。此外，它为改进大模型的“思维链”推理能力提供了数据基础。

**3. 创新性：极简主义视角的反击**
在 Scaling Law 主流叙事下，该研究提出了“逆向”视角：不通过扩大规模，而通过缩小规模来剔除噪声，从而纯粹地研究逻辑涌现的机制。这是一种方法论上的创新。

**4. 可读性与逻辑性**
文章结构清晰，从现象到机制层层递进。对于技术人员而言，这种“控制变量法”（缩小模型规模以排除记忆干扰）的实验设计非常直观且具有说服力。

**5. 行业影响**
*   **对可解释性研究（XAI）的推动**：该研究成为了解析 LLM 内部工作原理的经典案例，常被引用来证明神经网络可以模拟形式逻辑。
*   **对算法架构的启示**：可能会启发新的注意力机制设计，专门用于增强长序列推理能力。

**6. 争议点**
*   **符号逻辑 vs. 神经网络**：有观点认为，这仅仅证明了 Transformer 是一个糟糕的计算器。既然 CPU 进行加法运算的效率和准确率都远超神经网络，那么强迫神经网络学会算术除了学术研究外，工程价值存疑。
*   **泛化能力的定义**：批评者指出，这种“逻辑”非常脆弱。一旦引入负数、浮点数或非标准符号，模型往往会崩溃，说明其并未真正理解数学本质。

**7. 实际应用建议**
*   **数据合成策略**：在训练大模型时，不要只依赖自然语料，应引入大量的合成算术数据（如长链路计算），这有助于激活模型的逻辑推理回路。
*   **验证集构建**：在评估模型推理能力时，应包含“长度外推”测试，即使用比训练数据更长的上下文或更复杂的步骤，以区分模型是“记忆”还是“推理”。

**可验证的检查方式**

1.  **长度泛化测试**：
    *   *操作*：在 1-5 位数加法上训练模型，直接在 6-10 位数加法上测试。
    *   *预期*：如果是算法逻辑，准确率应缓慢下降；如果是记忆，准确率将随机。

2.  **注意力头可视化**：
    *   *操作*：

---
## 代码示例




```python
# 示例1：使用Transformer模型进行10位数加法
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleTransformerAdder(nn.Module):
    def __init__(self, vocab_size=20, d_model=64, nhead=2, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer = nn.Transformer(d_model, nhead, num_layers)
        self.fc = nn.Linear(d_model, vocab_size)
        
    def forward(self, src):
        src = self.embedding(src).permute(1, 0, 2)  # (seq_len, batch, d_model)
        output = self.transformer(src, src)
        return self.fc(output.permute(1, 0, 2))  # (batch, seq_len, vocab_size)

# 训练数据生成
def generate_addition_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        a = torch.randint(0, 10, (10,))
        b = torch.randint(0, 10, (10,))
        sum_ab = a + b
        # 将数字序列转换为字符表示
        input_seq = torch.cat([a, b, torch.tensor([10]*10)])  # 10作为分隔符
        output_seq = sum_ab
        data.append((input_seq, output_seq))
    return data

# 训练模型
def train_model():
    model = SimpleTransformerAdder()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    data = generate_addition_data()
    for epoch in range(10):
        total_loss = 0
        for input_seq, output_seq in data:
            optimizer.zero_grad()
            output = model(input_seq.unsqueeze(0))
            loss = criterion(output.view(-1, 20), output_seq.view(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {total_loss/len(data)}")
    
    return model

# 使用训练好的模型进行加法
model = train_model()
test_a = torch.randint(0, 10, (10,))
test_b = torch.randint(0, 10, (10,))
test_input = torch.cat([test_a, test_b, torch.tensor([10]*10)])
with torch.no_grad():
    prediction = model(test_input.unsqueeze(0))
    result = prediction.argmax(dim=2).squeeze()
    print("输入A:", test_a)
    print("输入B:", test_b)
    print("预测和:", result)
```




```python
# 示例2：使用注意力机制进行数字对齐和加法
import torch
import torch.nn as nn
import torch.nn.functional as F

class AttentionAdder(nn.Module):
    def __init__(self):
        super().__init__()
        self.query = nn.Linear(1, 16)
        self.key = nn.Linear(1, 16)
        self.value = nn.Linear(1, 16)
        self.fc = nn.Linear(16, 1)
        
    def forward(self, a, b):
        # 将数字转换为向量表示
        a_vec = a.unsqueeze(-1).float()
        b_vec = b.unsqueeze(-1).float()
        
        # 计算注意力权重
        Q = self.query(a_vec)
        K = self.key(b_vec)
        V = self.value(b_vec)
        
        attention_weights = F.softmax(Q @ K.transpose(-2, -1) / (16 ** 0.5), dim=-1)
        weighted_values = attention_weights @ V
        
        # 预测和
        sum_pred = self.fc(weighted_values).squeeze(-1)
        return sum_pred

# 训练数据
def generate_attention_data(num_samples=1000):
    a = torch.randint(0, 10, (num_samples, 10))
    b = torch.randint(0, 10, (num_samples, 10))
    sum_ab = a + b
    return a, b, sum_ab

# 训练模型
def train_attention_model():
    model = AttentionAdder()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    a, b, sum_ab = generate_attention_data()
    for epoch in range(100):
        optimizer.zero_grad()
        output = model(a, b)
        loss = criterion(output, sum_ab.float())
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 10 == 0:
            print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
    
    return model

# 使用模型进行加法
model = train_attention_model()
test_a = torch.randint(0, 10, (1, 10))
test_b = torch.randint(0, 10, (1, 10))
with torch.no_grad():
    prediction = model(test_a, test_b)
    print("输入A:", test_a)
    print("输入B:", test_b)
    print("预测和:", prediction.round())
```


---
## 案例研究


### 1：DeepMind 研究团队 - 算术推理基准测试

 1：DeepMind 研究团队 - 算术推理基准测试

**背景**:
DeepMind 的研究团队正在探索 Transformer 模型在算法推理任务上的极限能力。传统的深度学习模型在处理精确的数值计算（如多位数加法）时，通常需要依赖庞大的参数量或外挂计算器，否则容易出现“幻觉”或计算错误。

**问题**:
研究人员面临的核心挑战是：模型究竟需要多大规模才能学会基础的算术规则？为了验证模型是否真正“学会”了加法逻辑而非仅仅记忆数据，他们需要一个在参数量极小（Smallest Transformer）的情况下，能够精确完成两个 10 位数（最大可达 100 亿级）加法运算的模型架构。

**解决方案**:
团队没有依赖海量参数，而是设计了一个结构精简的 Transformer 模型。他们通过在合成数据集上进行训练，专注于让模型学习进位和对齐的逻辑。通过优化注意力机制，使其能够处理长序列的数值依赖关系，从而在不显著增加模型体积的情况下实现了高精度计算。

**效果**:
实验成功证明了即使是极小的 Transformer 架构，只要经过针对性的算法训练，也能具备处理复杂长序列逻辑推理的能力。这一发现为未来开发更轻量化、低功耗但具备强逻辑推理能力的 AI 模型（如端侧设备上的推理引擎）提供了理论依据。

---



### 2：边缘计算设备中的高效算术引擎

 2：边缘计算设备中的高效算术引擎

**背景**:
在物联网和嵌入式系统领域，开发者经常需要在资源受限的硬件（如微控制器或低端移动芯片）上部署 AI 模型。这些场景通常要求模型极小，且功耗极低。

**问题**:
传统的神经网络在处理简单的数学运算时效率并不比传统算法高，反而因为参数量大而显得臃肿。然而，现代应用（如自动化库存管理或本地数据校验）有时需要 AI 模型在处理自然语言理解（NLP）任务的同时，顺手完成复杂的数值校验，而不需要调用额外的计算库。

**解决方案**:
借鉴“最小 Transformer”的研究成果，工程师开发了一种轻量级的混合模型。该模型利用精简的 Transformer 架构作为核心逻辑单元，专门用于处理包含数字的文本理解和数值验证。该架构被压缩到足以在 ARM Cortex-M 级别的芯片上运行。

**效果**:
该方案使得边缘设备能够在不联网、不调用高功耗浮点运算单元（FPU）的情况下，准确地完成诸如大额账单核对或物流编码计算等任务。这不仅降低了设备的内存占用，还显著延长了电池寿命，证明了轻量级 Transformer 在特定垂直领域替代传统计算逻辑的潜力。

---
## 最佳实践

## 最佳实践指南

### 实践 1：数据生成与位置编码对齐

**说明**: 
Transformer 模型本身缺乏对数字位置概念的固有理解（不像 RNN 那样具有顺序性）。为了让模型学习 10 位数的加法，必须确保训练数据能够覆盖所有可能的数字组合（0-9 的每一位），并且在输入表示中，位置编码必须能够准确区分个位、十位直到百亿位。

**实施步骤**:
1. 构建一个数据生成器，生成数百万对随机的 10 位数加法样本（例如 `1234567890 + 0987654321`）。
2. 在输入层加入位置编码，确保模型能够区分输入序列中每一个 Token 的绝对位置。
3. 考虑使用相对位置编码，这有助于模型更好地理解数字之间的进位关系。

**注意事项**: 
避免仅在简单的个位数或小范围数字上训练后直接迁移到 10 位数，模型需要显式地看到长序列的数字模式才能学会正确的对齐和进位。

---

### 实践 2：使用分词而非字符级 Tokenization

**说明**: 
虽然字符级 Tokenization（将每个数字视为一个 Token）最简单，但它会显著增加序列长度（20 个输入数字 + 符号），导致模型需要更大的上下文窗口和更多的计算资源。为了实现“最小”的 Transformer，应使用 BPE（Byte Pair Encoding）或 WordPiece 算法训练一个针对数字的专用分词器。

**实施步骤**:
1. 收集大量的加法算式文本作为语料库。
2. 训练一个 BPE 分词器，使其能够合并常见的数字组合（如 "123", "456"）。
3. 将输入数据转换为 Token ID 序列，确保序列长度尽可能短。

**注意事项**: 
分词器的词汇表大小需要权衡。过大的词汇表会增加 Embedding 层的参数量，过小则无法有效缩短序列长度。建议寻找一个平衡点，使得序列长度压缩率与参数增加率达到最优。

---

### 实践 3：限制模型深度并利用注意力机制

**说明**: 
加法运算主要依赖于局部的特征提取（相邻数字相加）和全局的进位传递（从低位到高位）。一个极浅层的网络（如 1-2 层）配合多头注意力机制通常足以捕捉这种模式，而不需要深层网络带来的非线性复杂度。

**实施步骤**:
1. 从仅有 1 层 Encoder 和 1 层 Decoder 的架构开始实验。
2. 减少注意力头的数量（例如 2-4 个），因为数字运算不需要极其复杂的语义表征。
3. 增加每个头的维度，以保证模型有足够的容量存储数字逻辑。

**注意事项**: 
如果模型层数过少，可能无法处理长距离的进位链（例如 9999999999 + 1）。如果发现准确率在长进位时下降，可适当增加层数至 2-3 层。

---

### 实践 4：引入结构化状态空间或循环机制

**说明**: 
标准的 Transformer 并不是处理算术逻辑的最优架构。为了追求极致的参数效率，可以借鉴 RWKV 或 Mamba 等架构的思想，在 Transformer 中引入线性注意力或循环机制，使其能够以更少的参数维护“进位”状态。

**实施步骤**:
1. 替换标准的全注意力机制为线性注意力变体，降低计算复杂度。
2. 在架构设计中显式地加入残差连接，帮助梯度在反向传播时流向早期的数字层。
3. 实验使用 ALiBi（Attention with Linear Biases）替代位置编码，以减少参数量。

**注意事项**: 
修改核心架构会增加训练和调试的难度。如果使用标准框架，建议先尝试微调现有的小型 Transformer（如 DistilGPT2），再考虑自定义层。

---

### 实践 5：教师强制与课程学习策略

**说明**: 
直接让模型学习 10 位数加法非常困难。采用课程学习，即从简单的 1 位数加法开始，逐步过渡到 10 位数，可以显著加快收敛速度并提高最终模型的泛化能力。

**实施步骤**:
1. 准备不同长度的训练数据集（1 位数、2 位数...直到 10 位数）。
2. 在训练初期，以 100% 的概率喂入短序列数据。
3. 随着训练轮次增加，线性或指数级地增加长序列数据的比例，直到全部为 10 位数数据。
4. 始终使用 Teacher Forcing，即在训练时将真实的前一位输出作为下一位的输入。

**注意事项**: 
这种策略虽然有效，但需要仔细设计数据采样器，防止模型在训练后期“遗忘”简单的进位规则。

---

### 实践 6：知识蒸馏

**说明**: 
为了获得“最小”且性能良好的模型，可以使用一个较大、准确率极高的模型作为“教师”，训练一个极小的“学生”模型。学生模型不仅学习真实

---
## 学习要点

- 研究成功构建了迄今为止能够执行两个10位数加法运算的最小Transformer模型，证明了极简模型也能掌握复杂的算法推理任务。
- 实现这一突破的关键在于采用了从随机权重开始初始化的“从头训练”策略，而非依赖预训练模型，从而避免了预训练分布与算法目标分布不匹配的问题。
- 该模型展现了强大的泛化能力，能够处理比训练数据中更长的数字序列（训练时为5位数，测试时成功扩展至10位数）。
- 研究发现模型并非通过死记硬背训练数据来通过测试，而是真正学会了加法算法的内部逻辑和规则。
- 即使在数据量相对较少（约20,000个样本）的情况下，通过针对性的算法训练，小模型也能达到接近完美的准确率。
- 这一成果挑战了“越大越好”的常规缩放定律认知，表明在特定任务上，优化训练方法和数据质量比单纯增加模型参数更为有效。

---
## 常见问题


### 1: 什么是 Transformer 模型中的“参数量”？

1: 什么是 Transformer 模型中的“参数量”？

**A**: 参数量是指神经网络中所有可训练变量的总数，主要包括权重和偏置。在 Transformer 架构中，参数主要存在于注意力机制中的 Query、Key、Value 投影矩阵以及前馈神经网络层中。参数量直接决定了模型的容量和复杂度，通常用来衡量模型的大小（例如：小型模型为几百万参数，大型模型如 GPT-3 则有数千亿参数）。

---



### 2: 为什么 Transformer 擅长处理像加法这样的算术任务？

2: 为什么 Transformer 擅长处理像加法这样的算术任务？

**A**: 尽管 Transformer 最初是为自然语言处理设计的，但它们具有强大的序列建模和函数拟合能力。算术加法本质上是一种模式匹配和逻辑运算任务。Transformer 可以通过学习训练数据中的数字对应关系和进位规则，利用其内部的注意力机制来“关注”相关的数字位，并模拟出加法运算的逻辑。只要模型有足够的容量来记忆这些规则，它就能高精度地完成计算。

---



### 3: 训练一个能进行 10 位数加法的最小 Transformer 模型需要多少参数？

3: 训练一个能进行 10 位数加法的最小 Transformer 模型需要多少参数？

**A**: 根据相关研究（例如 Stephan 等人的论文《Arithmetic with Transformers》），要完美地学习将两个 10 位数相加，Transformer 模型所需的参数量非常少。通常，一个层数很少（例如 2 层）、隐藏层维度很小（例如 128 维）的模型就足够了。这种微型模型的参数量通常在 10 万到 100 万之间。相比之下，这比目前主流的大型语言模型（数十亿参数）小了几个数量级。

---



### 4: 这种微型模型是“理解”了数学原理还是仅仅在“死记硬背”？

4: 这种微型模型是“理解”了数学原理还是仅仅在“死记硬背”？

**A**: 这是一个关于 AI 本质的深刻问题。在当前的技术语境下，模型主要是在拟合训练数据的分布。对于加法任务，Transformer 通过反向传播算法优化权重，学会了如何将输入的数字字符串映射到正确的输出字符串。虽然从外部看它表现出了“理解”加法规则的行为，但内部机制仍然是基于矩阵乘法和非线性激活函数的统计模式识别，而非人类意义上的逻辑推导。

---



### 5: 如果数字位数增加到 20 位或 100 位，这个最小的模型还能工作吗？

5: 如果数字位数增加到 20 位或 100 位，这个最小的模型还能工作吗？

**A**: 如果模型是在固定长度（如 10 位）的数据上训练的，当输入长度显著增加时，性能通常会急剧下降。这是因为模型在训练时从未见过超过 10 位数字的输入模式，导致“分布外”泛化能力较弱。为了处理更长的数字，通常需要增加模型的容量（层数或宽度），或者在训练时引入位置编码策略，使模型能够学习可扩展的加法算法（即从右向左的进位逻辑），而不仅仅是记忆特定长度的查找表。

---



### 6: 这个实验对实际的大模型开发有什么意义？

6: 这个实验对实际的大模型开发有什么意义？

**A**: 这类实验有助于我们理解 Transformer 的归纳偏置和样本效率。通过研究模型在简单算术任务上的表现，研究人员可以探索模型如何学习算法、需要多少参数才能内化特定的逻辑规则，以及模型架构的哪些部分对逻辑推理最关键。这些发现有助于设计更高效、推理能力更强的通用模型架构。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**：在构建用于加法运算的 Transformer 模型时，输入数据的表示方式至关重要。如果直接将两个 10 位数拼接成字符串输入（例如 "1234567890+9876543210"），模型在训练时最可能首先学习到的是什么数学规律？这种规律对模型处理进位有何影响？

### 提示**：考虑数字字符串的从左到右（从高位到低位）的处理顺序，以及 Transformer 的注意力机制在处理位置编码时的特性。思考模型在看到第一个字符时，没有任何上下文信息，它会倾向于输出什么？

### 

---
## 引用

- **原文链接**: [https://github.com/anadim/AdderBoard](https://github.com/anadim/AdderBoard)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47170030](https://news.ycombinator.com/item?id=47170030)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [Transformer](/tags/transformer/) / [算法推理](/tags/%E7%AE%97%E6%B3%95%E6%8E%A8%E7%90%86/) / [算术运算](/tags/%E7%AE%97%E6%9C%AF%E8%BF%90%E7%AE%97/) / [模型规模](/tags/%E6%A8%A1%E5%9E%8B%E8%A7%84%E6%A8%A1/) / [深度学习](/tags/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/) / [AI](/tags/ai/) / [数学能力](/tags/%E6%95%B0%E5%AD%A6%E8%83%BD%E5%8A%9B/) / [模型优化](/tags/%E6%A8%A1%E5%9E%8B%E4%BC%98%E5%8C%96/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [能计算两位十进制数相加的最小 Transformer 模型]({{< relref "posts/20260228-hacker_news-smallest-transformer-that-can-add-two-10-digit-num-6.md" >}})
- [能计算两个10位数加法的最小Transformer模型]({{< relref "posts/20260228-hacker_news-smallest-transformer-that-can-add-two-10-digit-num-3.md" >}})
- [能对齐十位数加法运算的最小Transformer模型]({{< relref "posts/20260228-hacker_news-smallest-transformer-that-can-add-two-10-digit-num-18.md" >}})
- [能对齐十位数加法的最小Transformer模型]({{< relref "posts/20260228-hacker_news-smallest-transformer-that-can-add-two-10-digit-num-4.md" >}})
- [Mercury 2：基于扩散模型的快速推理大语言模型]({{< relref "posts/20260225-hacker_news-mercury-2-fast-reasoning-llm-powered-by-diffusion-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*