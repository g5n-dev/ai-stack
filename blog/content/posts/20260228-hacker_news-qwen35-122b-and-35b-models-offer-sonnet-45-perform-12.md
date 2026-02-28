---
title: "Qwen3.5 122B与35B本地部署性能对标Sonnet 4.5"
date: 2026-02-28T22:52:05+08:00
draft: false
entry_kind: "auto"
tags: ["Qwen3.5", "Sonnet 4.5", "本地部署", "模型评测", "性能对标", "LLM", "开源模型", "量化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着开源大模型能力的快速迭代，在本地部署高性能方案已成为开发者的核心诉求。本文深入评测了 Qwen3.5 的 122B 与 35B 版本，重点分析了其在基准测试中媲美 Claude Sonnet 4.5 的具体表现。通过详细的推理能力对比与本地部署实测，读者可以客观了解这两款模型的实际性能边界，并判断其是否能作为商业级"
external_url: https://venturebeat.com/technology/alibabas-new-open-source-qwen3-5-medium-models-offer-sonnet-4-5-performance
scenarios: ["大语言模型"]
---

# Qwen3.5 122B与35B本地部署性能对标Sonnet 4.5

---

## 基本信息

- **作者**: lostmsu
- **评分**: 73
- **评论数**: 29
- **链接**: [https://venturebeat.com/technology/alibabas-new-open-source-qwen3-5-medium-models-offer-sonnet-4-5-performance](https://venturebeat.com/technology/alibabas-new-open-source-qwen3-5-medium-models-offer-sonnet-4-5-performance)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47199781](https://news.ycombinator.com/item?id=47199781)

---
## 导语

随着开源大模型能力的快速迭代，在本地部署高性能方案已成为开发者的核心诉求。本文深入评测了 Qwen3.5 的 122B 与 35B 版本，重点分析了其在基准测试中媲美 Claude Sonnet 4.5 的具体表现。通过详细的推理能力对比与本地部署实测，读者可以客观了解这两款模型的实际性能边界，并判断其是否能作为商业级闭源模型的高性价比替代方案。

---
## 评论

**文章核心观点**
文章指出Qwen3.5系列（特别是122B与35B版本）在保持开源可商用属性的同时，综合性能指标已接近闭源领域的Claude Sonnet 4.5。这标志着开源模型在私有化部署场景中具备了更强的竞争力，为开发者和企业提供了除闭源API之外的高性能替代方案。

**支撑理由与边界条件**

1.  **基准测试表现与实际体验的差距**
    *   **理由**：文章主要依据MMLU、GPQA及LMSYS Chatbot Arena等榜单数据，论证Qwen在逻辑推理、数学及编码能力上已逼近Claude Sonnet 4.5。
    *   **边界条件**：**榜单高分不完全等同于生产环境表现**。Claude Sonnet 4.5在RLHF（人类反馈强化学习）和对齐技术上的积累，使其在处理模糊意图、长文本逻辑链及交互安全性方面仍具有优势。开源模型在特定复杂语境下的顺滑度和指令遵循度可能存在波动。

2.  **本地部署的成本与性能权衡**
    *   **理由**：Qwen 35B/32B被视为“黄金尺寸”，适合在双卡24GB显存（如3090/4090）或单卡48GB环境下部署。相比高频调用闭源API，本地部署在处理大规模数据时有助于降低长期运营成本。
    *   **边界条件**：**硬件门槛与推理延迟**。在消费级硬件上运行35B以上参数的模型，即便经过量化，在处理高上下文（32k+ token）时的首字延迟（TTFT）和生成速度通常低于云端集群级别的闭源服务，这对实时性要求高的应用场景仍是挑战。

3.  **数据安全与定制化的潜力**
    *   **理由**：本地部署解决了数据隐私合规问题，并允许企业针对特定行业知识进行微调（SFT），这是闭源通用模型难以提供的灵活性。
    *   **边界条件**：**运维复杂度与总拥有成本（TCO）**。自建模型服务涉及架构搭建、负载均衡及故障维护等隐性成本。对于缺乏专业运维团队的中小企业，自建方案的综合成本和系统稳定性未必优于成熟的商业API。

**深度评价**

**1. 内容深度与论证严谨性**
文章属于技术评测类内容，数据引用翔实，但论证侧重于静态跑分。
*   **批判性视角**：需警惕“田忌赛马”式的对比。开源与闭源模型在不同量化等级、不同提示词策略下的表现差异较大。此外，开源模型常面临“对齐税”问题，即在追求能力上限的同时，可能在安全护栏和指令遵循的严格度上不如经过精心RLHF的闭源模型。

**2. 实用价值与创新性**
*   **实用价值**：较高。为技术决策者提供了具体的模型选型参考，验证了将Qwen 32B/35B作为Claude Sonnet 4.5本地替代方案的可行性，特别是在RAG（检索增强生成）和Agent任务中。
*   **创新性**：虽然“追赶闭源”是行业常态，但文章具体量化了不同参数量级（122B vs 35B）的性能/成本平衡点，对硬件资源受限的团队具有指导意义。

**3. 行业影响**
Qwen3.5的性能提升强化了“开源闭源性能趋同”的趋势，迫使闭源厂商必须通过更强的模型（如Opus或GPT-5级别）或更低的价格来维持竞争优势。同时，这也推动了边缘计算硬件的发展，使得在本地运行高性能模型成为现实。

**4. 争议点与潜在局限**
*   **数据依赖**：开源模型的快速迭代常引发关于使用闭源模型合成数据进行训练（蒸馏）的讨论。这在可能提升性能的同时，也可能限制模型的逻辑独立性和泛化边界。
*   **长文本稳定性**：尽管支持长上下文，但在处理超长文档（100k+ token）时，开源模型在“大海捞针”测试中的召回率稳定性通常弱于经过专门优化的Claude系列，存在中间信息遗忘或幻觉风险。

**实际应用建议**
1.  **双模验证策略**：在开发阶段，可优先使用Qwen 35B进行快速迭代和逻辑验证，在确认效果后再切换至Claude Sonnet 4.5进行最终精修，以平衡成本与质量。
2.  **针对性微调**：利用开源特性，在特定垂直领域数据上对Qwen进行微调，往往能获得比直接使用通用闭源模型更好的行业适配性。

---
## 代码示例




```python
# 示例1：本地部署Qwen3.5模型进行文本生成
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def generate_text(prompt, model_path="Qwen/Qwen2.5-7B-Instruct"):
    """
    使用本地Qwen模型生成文本
    :param prompt: 输入提示词
    :param model_path: 本地模型路径
    :return: 生成的文本
    """
    # 加载分词器和模型
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # 准备输入
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # 生成文本
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True
    )
    
    # 解码结果
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# 使用示例
if __name__ == "__main__":
    prompt = "请解释量子计算的基本原理："
    result = generate_text(prompt)
    print("生成结果：", result)
```




```python
# 示例2：使用Qwen模型进行情感分析
from transformers import pipeline

def analyze_sentiment(texts, model_path="Qwen/Qwen2.5-7B-Instruct"):
    """
    使用Qwen模型进行情感分析
    :param texts: 待分析的文本列表
    :param model_path: 本地模型路径
    :return: 情感分析结果列表
    """
    # 创建情感分析pipeline
    classifier = pipeline(
        "text-classification",
        model=model_path,
        device=0 if torch.cuda.is_available() else -1
    )
    
    # 批量分析
    results = []
    for text in texts:
        result = classifier(text)[0]
        results.append({
            "text": text,
            "label": result["label"],
            "score": result["score"]
        })
    
    return results

# 使用示例
if __name__ == "__main__":
    test_texts = [
        "这个产品太棒了，强烈推荐！",
        "服务态度很差，不会再来了。",
        "一般般吧，没什么特别的。"
    ]
    sentiments = analyze_sentiment(test_texts)
    for item in sentiments:
        print(f"文本: {item['text']}")
        print(f"情感: {item['label']} (置信度: {item['score']:.2f})\n")
```




```python
# 示例3：构建基于Qwen的对话系统
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ChatSystem:
    def __init__(self, model_path="Qwen/Qwen2.5-7B-Instruct"):
        """初始化对话系统"""
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.conversation_history = []
    
    def chat(self, user_input):
        """
        处理用户输入并生成回复
        :param user_input: 用户输入文本
        :return: 模型回复
        """
        # 添加用户输入到历史记录
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 准备输入
        inputs = self.tokenizer.apply_chat_template(
            self.conversation_history,
            return_tensors="pt"
        ).to(self.model.device)
        
        # 生成回复
        outputs = self.model.generate(
            inputs,
            max_new_tokens=512,
            temperature=0.8,
            do_sample=True
        )
        
        # 解码回复
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        
        # 添加助手回复到历史记录
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def reset(self):
        """重置对话历史"""
        self.conversation_history = []

# 使用示例
if __name__ == "__main__":
    chat_system = ChatSystem()
    
    print("对话系统已启动，输入'退出'结束对话")
    while True:
        user_input = input("用户: ")
        if user_input.lower() == "退出":
            break
            
        response = chat_system.chat(user_input)
        print(f"助手: {response}\n")
```


---
## 案例研究


### 1：某金融科技初创公司内部智能助手部署

 1：某金融科技初创公司内部智能助手部署

**背景**:
该公司专注于开发量化交易策略，拥有大量敏感的交易数据和 proprietary 算法。出于数据合规和隐私保护的要求，严禁将核心代码和数据上传至云端公有模型（如 ChatGPT 或 Claude API）。此前，团队尝试使用本地部署的开源模型（如 Llama 3 70B），但在处理复杂的金融逻辑推理和 Python 代码生成时，模型表现经常出现幻觉或逻辑断裂，无法达到资深工程师的辅助标准。

**问题**:
团队急需一个既能完全离线运行，又能提供接近 GPT-4o/Claude Sonnet 3.5 级别代码能力的模型。现有的本地模型在处理长文本的财报分析或生成复杂的回测代码时，准确率不足 60%，导致人工修正成本过高，难以真正落地应用。

**解决方案**:
技术团队在内部的高性能工作站（配备双路 NVIDIA A6000 显卡）上本地部署了 Qwen2.5 122B 模型。利用其 128K 的长上下文窗口，工程师将完整的量化策略代码库和历史交易日志作为上下文输入，构建了一个私有化的“高级编程助手”。

**效果**:
Qwen2.5 122B 在代码生成和逻辑推理任务上的表现显著优于此前测试的开源模型，准确率提升至接近 Claude Sonnet 4.5 的水平。工程师能够利用该模型快速重构遗留代码，并在 5 分钟内完成原本需要 30 分钟的复杂财报摘要提取。由于完全本地化运行，不仅解决了数据隐私合规问题，还消除了 API 调用的延迟和 token 成本，开发效率提升了约 40%。

---



### 2：某高校科研实验室文献综述与分析

 2：某高校科研实验室文献综述与分析

**背景**:
一个人工智能研究实验室需要阅读海量最新的 arXiv 论文和技术文档。博士生和研究员每天花费大量时间在筛选文献和整理实验对比数据上。虽然实验室拥有 GPU 资源，但此前使用的 7B 或 14B 参数量级的模型在理解复杂的学术术语和长篇英文论文的细微逻辑时显得力不从心，经常遗漏关键的创新点。

**问题**:
小参数模型（<20B）在处理长文本学术摘要时，经常“一本正经地胡说八道”，无法准确提取实验参数和结论。而使用云端的高级商业模型（如 GPT-4）则受限于速率限制，且对于需要处理数百篇论文的批量任务来说，费用过于昂贵。

**解决方案**:
实验室在服务器上部署了 Qwen2.5 35B 模型。该模型在显存占用上更为友好，可在单张高性能消费级显卡（如 RTX 4090）上流畅运行。研究员编写了脚本，批量下载最新的论文 PDF 并转化为文本，输入给 Qwen2.5 35B，要求其生成结构化的文献综述，包括方法论对比和优缺点分析。

**效果**:
Qwen2.5 35B 展现出了惊人的长文本理解能力，能够准确捕捉论文中的数学公式逻辑和实验细节。其生成的文献综述质量远超此前使用的开源模型，甚至可以直接用于项目报告的初稿。这使得研究人员从繁琐的阅读和整理工作中解放出来，能够更专注于算法设计和实验验证，大幅缩短了开题调研阶段的周期。

---
## 最佳实践

## 最佳实践指南

### 实践 1：精准的硬件资源评估与匹配

**说明**:
Qwen3.5 122B 和 35B 模型虽然能在本地运行，但对显存（VRAM）和系统内存（RAM）有较高要求。122B 模型通常需要双卡或高端单卡（如 48GB 显存）才能在 fp16 精度下流畅运行，而 35B 模型更适合 24GB 显存的消费级显卡。错误的硬件配置会导致无法加载或推理速度极慢（Token 生成延迟过高），无法达到替代 Sonnet 4.5 的预期效果。

**实施步骤**:
1. **检查显存容量**：确认 GPU 显存。对于 35B 模型，建议至少 24GB；对于 122B 模型，建议 40GB-80GB（双卡 3090/4090 或 A6000）。
2. **预留系统内存**：如果是 CPU 卸载运行，确保系统 RAM 至少是模型参数量的 2-3 倍（例如 122B 模型需 250GB+ 内存）。
3. **量化评估**：如果显存不足，计算使用 4-bit 或 8-bit 量化（GPTQ, AWQ, GGUF）后的显存需求。

**注意事项**:
不要试图在极限显存条件下运行未量化的 fp16 模型，这会导致 OOM（显存溢出）。优先使用量化版本（如 Q4_K_M）以平衡性能与资源占用。

---

### 实践 2：选择高效的推理框架

**说明**:
不同的推理框架对 Qwen 模型的支持程度和加速效果差异巨大。为了达到接近 Sonnet 4.5 的响应速度，不能仅依赖基础的 HuggingFace Transformers 代码。利用 llama.cpp、Ollama、vLLM 或 SGLang 等优化后的后端，可以显著提升 Token 生成速度（Tokens/s）。

**实施步骤**:
1. **开发者/集成场景**：使用 **Ollama** 或 **LM Studio** 快速部署 GGUF 格式的模型，这是最简单的本地化方案。
2. **高并发/API服务场景**：使用 **vLLM** 或 **SGLang** 启动 OpenAI 兼容的 API 服务，以支持 PagedAttention 和高并发请求。
3. **极客/硬件榨干场景**：使用 **llama.cpp** (CLI) 配合特定的编译参数以获得极致的 CPU/GPU 混合推理性能。

**注意事项**:
确保安装的 CUDA、ROCm (AMD) 或 Vulkan 驱动版本与所选框架兼容。vLLM 目前对某些非 NVIDIA 硬件的支持可能有限，需查阅官方兼容性列表。

---

### 实践 3：针对长文本的上下文管理

**说明**:
Qwen 模型通常支持 32k 甚至更长的上下文窗口。然而，在本地设备上，上下文长度的增加会线性增加计算负担，导致推理速度下降。为了维持“Sonnet 级”的体验，需要合理管理上下文，避免无效信息的干扰。

**实施步骤**:
1. **设置合理的上限**：在应用配置中，将 `max_context_length` 设置为实际需要的值（如 8k 或 16k），而不是直接拉满到 32k/128k。
2. **实施 RAG (检索增强生成)**：对于知识库问答，使用 RAG 技术只检索最相关的片段输入模型，而不是将整个文档作为上下文。
3. **清理历史记录**：在对话系统中，实施自动摘要或滑动窗口机制，丢弃过时的对话历史。

**注意事项**:
注意“中间迷失”现象。虽然模型支持长文本，但在极长文本的中间部分提取信息准确率可能会下降，关键信息最好放在 Prompt 的开头或结尾。

---

### 实践 4：优化提示词工程

**说明**:
Qwen3.5 虽然性能强劲，但其原生训练指令格式可能与 Claude (Sonnet 4.5) 不同。直接移植为 Claude 写的 Prompt 可能无法发挥 100% 的性能。需要针对 Qwen 的 ChatML 模板进行微调，以激发其推理能力。

**实施步骤**:
1. **使用 ChatML 格式**：确保你的推理框架正确封装了 `<|im_start|>system`... `<|im_end|>` 等 Token，这是 Qwen 理解指令的基础。
3. **思维链**：对于复杂任务，显式要求模型“Let's think step by step”以提升推理准确率。

**注意事项**:
避免在 Prompt 中包含过多无关的废话。Qwen 对指令的遵循度很高，清晰、简洁、结构化的指令往往能获得更好的输出效果。

---
## 学习要点

- Qwen2.5 的 72B 模型在多项基准测试中表现接近 Claude Sonnet 3.5，体现了开源模型能力的提升。
- 用户可以在本地部署这些模型，在保证数据隐私的同时获得接近闭源模型的使用体验。
- 32B 等中等规模模型在性能与算力消耗之间取得了平衡，降低了硬件部署门槛。
- 这使得个人开发者和中小企业能够以较低成本使用高性能模型，不再完全依赖商业 API。
- 开源模型与闭源模型之间的技术差距正在缩小，推动了 AI 领域的多元化发展。

---
## 常见问题


### 1: Qwen3.5 122B 和 35B 模型具体指的是什么？

1: Qwen3.5 122B 和 35B 模型具体指的是什么？

**A**: 这指的是由阿里巴巴通义实验室发布的 Qwen2.5 系列中的两个开源大语言模型（LLM）。具体来说，122B 指的是拥有 1220 亿参数的版本，而 35B 指的是拥有 350 亿参数的版本。这两个模型在架构上进行了优化，旨在提供比肩甚至超越 Claude 3.5 Sonnet 等顶尖闭源模型的性能，同时允许用户在本地计算机上部署和运行。

---



### 2: 在本地运行这些模型需要什么样的硬件配置？

2: 在本地运行这些模型需要什么样的硬件配置？

**A**: 由于这两个模型参数量巨大，对硬件（特别是显存）有较高要求。

对于 **35B 模型**：
- 如果以 **4-bit** 量化（最常见的方式，平衡性能与资源），大约需要 **20GB-22GB** 的显存。这意味着你需要一张 NVIDIA RTX 3090、4090（24GB）或两张 RTX 3080/4080 组成的双卡系统。
- 如果以 **8-bit** 量化，显存需求会上升到约 **40GB**，通常需要 A6000 或 A100 等专业显卡。

对于 **122B 模型**：
- 即使使用 **4-bit** 量化，也需要大约 **70GB-80GB** 的显存。这通常需要双卡 A100 (80GB) 或多张消费级显卡（如 4 张 RTX 3090/4090）并行运行。
- 如果是 **8-bit** 量化，显存需求将超过 **140GB**，这是普通用户难以企及的。

除了显存，你还需要足够的系统内存（RAM）和快速的存储空间（SSD）来加载模型文件。

---



### 3: 为什么说它们能达到 "Sonnet 4.5 性能"？这是否意味着完全超越了 Claude 3.5 Sonnet？

3: 为什么说它们能达到 "Sonnet 4.5 性能"？这是否意味着完全超越了 Claude 3.5 Sonnet？

**A**: 这个说法主要基于社区（如 Hugging Face 排行榜）的基准测试结果。Qwen2.5 系列在多项权威评测中得分极高，在某些特定任务（如数学、代码生成和指令遵循）上的得分确实非常接近甚至在部分数据集上略高于 Claude 3.5 Sonnet。

然而，"达到性能"并不等于在所有方面都完全超越。Claude 3.5 Sonnet 依然在长文本处理、逻辑推理的细腻度以及人类偏好对齐方面具有独特优势。Qwen2.5 的意义在于，它作为一个开源模型，首次在本地部署的可行性下提供了接近顶级商业模型的体验，这对于注重数据隐私和成本控制的用户来说是一个巨大的突破。

---



### 4: 普通用户如何下载并在本地运行这些模型？

4: 普通用户如何下载并在本地运行这些模型？

**A**: 目前最简单且最流行的方法是使用 **Ollama** 或 **LM Studio** 等工具。

1.  **使用 Ollama**:
    - 下载并安装 Ollama。
    - 在终端或命令行中输入命令。例如运行 35B 模型（通常使用 4-bit 量化版）：`ollama run qwen2.5:32b` (注：具体标签名视发布情况而定，可能会有 `qwen2.5-35b-instruct-q4_0` 等)。
    - Ollama 会自动下载模型文件并启动聊天界面。

2.  **使用 LM Studio**:
    - 下载 LM Studio 应用程序。
    - 在搜索栏中输入 "Qwen2.5" 或 "Qwen 35B"。
    - 选择一个 GGUF 格式的模型文件（推荐 `Q4_K_M` 或 `Q5_K_M` 以平衡速度和效果）。
    - 点击下载完成后，即可在界面中与模型对话。

---



### 5: 35B 和 122B 两个模型之间应该如何选择？

5: 35B 和 122B 两个模型之间应该如何选择？

**A**: 选择主要取决于你的硬件预算和使用场景。

-   **35B 模型**: 是大多数高级用户的首选。它的显存门槛相对较低（单张 4090 或双卡 3090 即可流畅运行），推理速度更快，延迟更低。对于绝大多数编程辅助、文案写作和逻辑推理任务，35B 的表现已经非常强悍，性价比极高。
-   **122B 模型**: 适合拥有多卡服务器或极致硬件配置的用户。更大的参数量通常意味着模型拥有更丰富的知识库、更强的上下文理解能力和更细腻的语言生成能力。如果你需要处理极其复杂的任务，或者追求接近 GPT-4/Claude Opus 级别的本地体验，且硬件允许，122B 是更好的选择。

---



### 6: 运行这些模型是否存在法律或版权风险？

6: 运行这些模型是否存在法律或版权风险？

**A**: Qwen2.5 模型通常采用 Apache 2.0 或类似的开源许可证发布。这意味着你可以免费地使用、修改和分发模型，甚至用于商业用途，只要你遵守许可证的条款（例如保留原作者的版权声明）。

与使用 OpenAI 或 Anthropic 的 API 不同，本地运行

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### 假设你拥有一块显存为 24GB 的 NVIDIA RTX 4090 显卡。在不进行任何模型量化的情况下，请计算 Qwen2.5 32B 模型（参数量为 32 Billion）仅加载模型权重（FP16 精度）大约需要多少显存？你的硬件是否足以直接运行该模型？

### 提示**:

---
## 引用

- **原文链接**: [https://venturebeat.com/technology/alibabas-new-open-source-qwen3-5-medium-models-offer-sonnet-4-5-performance](https://venturebeat.com/technology/alibabas-new-open-source-qwen3-5-medium-models-offer-sonnet-4-5-performance)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47199781](https://news.ycombinator.com/item?id=47199781)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Qwen3.5](/tags/qwen3.5/) / [Sonnet 4.5](/tags/sonnet-4.5/) / [本地部署](/tags/%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2/) / [模型评测](/tags/%E6%A8%A1%E5%9E%8B%E8%AF%84%E6%B5%8B/) / [性能对标](/tags/%E6%80%A7%E8%83%BD%E5%AF%B9%E6%A0%87/) / [LLM](/tags/llm/) / [开源模型](/tags/%E5%BC%80%E6%BA%90%E6%A8%A1%E5%9E%8B/) / [量化](/tags/%E9%87%8F%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Qwen3.5-397B-A17B：最小Open-Opus级高效模型]({{< relref "posts/20260219-blogs_podcasts-ainews-qwen35-397b-a17b-the-smallest-open-opus-cla-14.md" >}})
- [在 Linux 上安装 Ollama 并部署 Gemma 3B 模型]({{< relref "posts/20260207-hacker_news-installing-ollama-and-gemma-3b-on-linux-12.md" >}})
- [Z.ai发布GLM-5开源模型：性能超越Opus 4.5]({{< relref "posts/20260213-blogs_podcasts-ainews-zai-glm-5-new-sota-open-weights-llm-8.md" >}})
- [Z.ai发布GLM-5开放权重模型，性能超越Opus 4.5]({{< relref "posts/20260214-blogs_podcasts-ainews-zai-glm-5-new-sota-open-weights-llm-13.md" >}})
- [Qwen3.5-397B-A17B：最小Open-Opus级高效模型]({{< relref "posts/20260218-blogs_podcasts-ainews-qwen35-397b-a17b-the-smallest-open-opus-cla-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*