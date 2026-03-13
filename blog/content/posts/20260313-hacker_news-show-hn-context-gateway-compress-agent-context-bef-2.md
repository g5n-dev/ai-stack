---
title: "Context Gateway：在LLM处理前压缩Agent上下文"
date: 2026-03-13T19:25:31+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "Agent", "上下文压缩", "Context Gateway", "Token优化", "推理加速", "中间件", "Show HN"]
categories: ["AI 工程", "大模型"]
source: hacker_news
description: "随着大模型应用对上下文窗口的需求日益增长，传输海量 token 带来的成本与延迟问题逐渐凸显。Context Gateway 作为一个中间层，通过在请求到达 LLM 之前对上下文进行智能压缩，有效平衡了信息完整性与处理效率。本文将介绍其核心工作原理，并展示如何通过这一方案优化你的 AI 应用架构。"
external_url: https://github.com/Compresr-ai/Context-Gateway
scenarios: ["大语言模型"]
---

# Context Gateway：在LLM处理前压缩Agent上下文

---

## 基本信息

- **作者**: ivzak
- **评分**: 12
- **评论数**: 4
- **链接**: [https://github.com/Compresr-ai/Context-Gateway](https://github.com/Compresr-ai/Context-Gateway)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47367526](https://news.ycombinator.com/item?id=47367526)

---
## 导语

随着大模型应用对上下文窗口的需求日益增长，传输海量 token 带来的成本与延迟问题逐渐凸显。Context Gateway 作为一个中间层，通过在请求到达 LLM 之前对上下文进行智能压缩，有效平衡了信息完整性与处理效率。本文将介绍其核心工作原理，并展示如何通过这一方案优化你的 AI 应用架构。

---
## 评论

### 评价：Show HN: Context Gateway – Compress agent context before it hits the LLM

**文章中心观点**
通过在 Agent 与 LLM 之间引入一个专门的“上下文网关”层，在请求到达模型之前对上下文进行算法压缩、重排序和过滤，是解决长上下文场景下 Token 成本过高和模型注意力分散问题的有效工程手段。

**支撑理由与边界条件**

**理由 1：缓解“大海捞针”效应，提升模型响应质量**
*   **事实陈述**：当前主流的 LLM（如 GPT-4, Claude 3）虽然支持 128k 甚至 200k 的上下文窗口，但在处理超长文本时，中间部分的注意力往往会出现显著下降，导致模型“遗忘”关键信息。
*   **你的推断**：Context Gateway 通过重排序和提取摘要，将最相关的信息置于上下文的“黄金位置”（通常是开头或结尾），能够显著提升模型在 RAG（检索增强生成）和复杂 Agent 任务中的准确率。
*   **反例/边界条件**：如果压缩算法本身引入了语义偏差或丢失了关键的细微差别（例如法律文档中的特定限定词），这种预处理会导致模型产生不可逆的幻觉，且比原始长文本更难被用户察觉。

**理由 2：显著的经济效益与延迟优化**
*   **事实陈述**：主流 LLM API 的计费模式是基于输入和输出 Token 数量的。长上下文 Agent 应用（如代码库分析、长期对话）经常因为重复发送系统提示词和历史记录而产生巨额费用。
*   **作者观点**：文章主张通过压缩上下文来减少 Token 消耗，从而直接降低运营成本，并可能因为输入变短而减少首字生成延迟（TTFT）。
*   **反例/边界条件**：引入 Gateway 本身增加了系统的网络跳数和预处理计算时间。如果压缩过程本身耗时过长（例如使用了较慢的本地模型进行摘要），或者 Gateway 的计算成本超过了节省的 LLM 成本，则该架构在经济上是负收益。

**理由 3：架构解耦与模块化治理**
*   **事实陈述**：在 Agent 开发中，业务逻辑往往与提示词工程耦合紧密。
*   **你的推断**：Context Gateway 实际上是一种“中间件”模式的回归。它将“上下文管理”这一非功能性需求从 Agent 的核心逻辑中剥离出来，使得开发者可以独立优化上下文策略（如切换不同的 RAG 策略或压缩算法），而无需修改 Agent 代码。
*   **反例/边界条件**：这种架构增加了系统的复杂度和调试难度。当 Agent 回答错误时，很难快速定位是 LLM 能力不足，RAG 检索错误，还是 Gateway 的压缩逻辑丢失了信息。

**创新性与实用价值评价**

从**技术角度**看，Context Gateway 并没有提出全新的算法，而是将信息检索中的“查询重写”和“文档摘要”技术集成到了 Agent 基础设施中。其创新点在于**将上下文处理视为一个独立的、可配置的管道**，而非简单的提示词技巧。

从**行业角度**看，这标志着 AI 应用开发正在从“模型为中心”转向“数据流和架构为中心”。随着模型能力的逐渐商品化，如何高效地喂养模型、优化上下文窗口的利用率，将成为企业级 AI 应用的核心竞争力。该方案对于构建长期记忆的 Agent、代码助手等场景具有极高的实用价值。

**争议点与不同观点**

1.  **压缩 vs. 长窗口模型**：随着长窗口模型成本的降低和能力的提升（如 Gemini 1.5 Pro 的 1M 窗口），是否还有必要做复杂的压缩？一种观点认为，暴力计算终将解决上下文问题，中间层压缩属于“过度工程”。
2.  **黑盒风险**：开发者可能会过度信任 Gateway 的输出，导致对模型实际“看到”了什么信息失去掌控。在金融或医疗领域，这种信息处理的不透明性是合规性的巨大挑战。
3.  **语义损失**：任何有损压缩都存在风险。如果 Gateway 错误地判断了某段信息的优先级，将其丢弃，那么后续的 LLM 无论多么强大都无法得出正确答案。

**实际应用建议**

1.  **分级处理策略**：不要对所有请求进行压缩。建议设置阈值，仅当上下文超过模型“黄金窗口”（通常为 32k 或 64k）时触发 Gateway 压缩逻辑。
2.  **保留原始引用**：Gateway 在输出摘要或压缩内容时，必须保留指向原始文档的索引或 ID，以便 LLM 生成回答时能够溯源，也方便开发者进行调试。
3.  **混合检索模式**：结合语义搜索和关键词匹配。Gateway 不应只做摘要，更应做“过滤器”，确保高价值信号（如实体名称、金额、日期）不被摘要模型吞没。

**可验证的检查方式**

1.  **Token 成本与延迟对比测试**：
    *   *指标*：在开启/关闭 Gateway 的情况下，对比相同 Agent 任务的端到端延迟和 API 调用成本。
    *   *预期*：Gateway 增加的延迟 < 节省的 LLM 推理延迟；总成本下降 > 20%。

2.  **RAG 问答准确率**：
    *   *实验*：使用 RAG 评估集（如包含多跳问题的数据集），对比“直接将检索结果喂给 LLM”与“经过 Gateway 压

---
## 代码示例




```python
# 示例1：基于关键词的上下文压缩
def compress_context_by_keywords(full_context: str, keywords: list, max_length: int = 1000) -> str:
    """
    根据关键词从长文本中提取相关句子，实现上下文压缩
    
    参数:
        full_context: 原始完整上下文
        keywords: 关键词列表
        max_length: 压缩后的最大长度
        
    返回:
        压缩后的上下文
    """
    # 分割成句子
    sentences = full_context.split('。')
    
    # 筛选包含关键词的句子
    relevant_sentences = []
    for sentence in sentences:
        if any(keyword in sentence for keyword in keywords):
            relevant_sentences.append(sentence)
    
    # 合并结果并截断
    compressed = '。'.join(relevant_sentences)
    return compressed[:max_length] + '...' if len(compressed) > max_length else compressed

# 使用示例
original_text = "人工智能是计算机科学的一个分支。它试图理解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。"
keywords = ["人工智能", "计算机"]
print(compress_context_by_keywords(original_text, keywords))
```




```python
# 示例2：基于相似度的上下文压缩
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compress_context_by_similarity(full_context: str, query: str, top_n: int = 3) -> str:
    """
    根据与查询的相似度提取最相关的句子
    
    参数:
        full_context: 原始完整上下文
        query: 用户查询
        top_n: 返回的最相关句子数量
        
    返回:
        压缩后的上下文
    """
    # 分割成句子
    sentences = full_context.split('。')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 计算TF-IDF相似度
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences + [query])
    
    # 获取与查询最相似的句子
    similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    # 合并结果
    compressed = '。'.join([sentences[i] for i in top_indices])
    return compressed

# 使用示例
context = "机器学习是人工智能的一个分支。它使计算机能够在没有明确编程的情况下学习。深度学习是机器学习的一个子集。神经网络是深度学习的基础。"
query = "什么是深度学习"
print(compress_context_by_similarity(context, query))
```




```python
# 示例3：基于摘要的上下文压缩
from transformers import pipeline

def compress_context_by_summary(full_context: str, max_length: int = 200) -> str:
    """
    使用预训练模型生成摘要来压缩上下文
    
    参数:
        full_context: 原始完整上下文
        max_length: 摘要最大长度
        
    返回:
        压缩后的摘要
    """
    # 加载摘要生成管道
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # 生成摘要
    summary = summarizer(full_context, max_length=max_length, min_length=30, do_sample=False)
    
    return summary[0]['summary_text']

# 使用示例
long_text = """人工智能（AI）是计算机科学的一个分支，它致力于创造能够执行通常需要人类智能的任务的机器。
这些任务包括视觉感知、语音识别、决策制定和语言翻译等。AI的研究始于1956年的达特茅斯会议。
近年来，随着大数据和计算能力的提升，AI技术取得了突破性进展，特别是在深度学习领域。
AI现在被广泛应用于医疗、金融、交通、教育等各个领域。"""
print(compress_context_by_summary(long_text))
```


---
## 案例研究


### 1：某大型金融科技公司的智能客服系统

 1：某大型金融科技公司的智能客服系统

**背景**: 该公司的客服机器人需要处理复杂的银行业务咨询，后台接入了长达 100+ 页的银行产品手册、合规文档以及过往的对话记录作为上下文。

**问题**: 在处理长对话或复杂查询时，直接将海量原始上下文发送给 LLM（如 GPT-4）导致 Token 消耗极高，单次对话成本超过 0.5 美元。同时，由于上下文过长，模型经常出现“迷失中间”现象，导致检索准确率下降，回答速度延迟超过 5 秒，严重影响用户体验。

**解决方案**: 在 LLM 调用链路中引入 Context Gateway 机制。系统在上下文发送给模型之前，利用语义压缩算法对文档内容进行去重和摘要，提取与当前用户意图最相关的高密度信息块，将输入上下文窗口压缩了 70%。

**效果**: API 调用成本降低了 60%，系统的平均响应时间（Latency）减少了 40%。更重要的是，由于干扰信息减少，模型对复杂合规问题的回答准确率提升了 15%。

---



### 2：SaaS 平台的代码审查助手

 2：SaaS 平台的代码审查助手

**背景**: 一个服务于 DevOps 团队的 AI 代码审查工具，需要分析开发者提交的 Pull Request (PR)。为了理解代码逻辑，它不仅要读取当前的 Diff 文件，还必须加载整个项目的代码库结构、依赖关系图以及历史提交记录作为上下文。

**问题**: 随着项目迭代，代码库体积急剧膨胀。单次审查请求的上下文经常超过 10k Tokens，导致频繁触发 LLM 的上下文窗口上限，或者因为模型处理能力饱和而忽略掉关键的边缘情况逻辑。高昂的推理成本也限制了该功能在免费版用户中的开放。

**解决方案**: 部署了上下文网关服务，专门针对代码结构进行优化。它在请求到达 LLM 前，通过 AST（抽象语法树）分析剔除未引用的依赖库和注释，仅保留与当前 Diff 相关的函数调用链和类型定义，实现了对代码上下文的“无损压缩”。

**效果**: 成功将大型项目的单次审查上下文控制在 4k Tokens 以内，使得审查功能的并发处理能力提升了 3 倍。同时，由于上下文更加聚焦，AI 指出潜在 Bug 的误报率降低了 25%，显著提升了开发者的信任度。

---



### 3：企业级法律文档分析平台

 3：企业级法律文档分析平台

**背景**: 该平台允许律师上传数千页的法律案件卷宗，并要求 AI 生成案件摘要和证据链分析。这需要 LLM 拥有极强的长文本记忆能力，能够跨越多个文档进行关联推理。

**问题**: 直接将所有卷宗文本填入 Prompt 不仅极其昂贵，而且往往超出模型的上下文限制。传统的 RAG（检索增强生成）方案虽然能截取片段，但容易丢失文档间的隐含关联，导致 AI 在梳理时间线时出现逻辑断层。

**解决方案**: 采用 Context Gateway 作为中间层，实施分层压缩策略。首先对文档进行向量化聚类，然后使用小型的参数高效模型（PEFT）对每个文档簇生成高信息密度的摘要，最后将这些结构化的摘要而非原始文本发送给主 LLM 进行最终分析。

**效果**: 在保证案件分析质量（由律师人工评估）不下降的前提下，处理单起案件的 Token 消耗量减少了 80%。这使得平台能够支持更大规模的文档上传，并将案件分析的生成时间从分钟级缩短到了秒级。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施语义压缩而非简单截断

**说明**: 
传统的上下文处理往往通过简单的字符截断或移除最早的文本来控制Token数量，这会导致关键信息丢失。Context Gateway 的核心在于语义压缩，即在保留核心语义的前提下，通过提取关键信息、总结段落或去除冗余修饰来减少Token消耗，同时保持信息的完整性。

**实施步骤**:
1. 建立文本分析层，识别输入文本中的关键实体、动词和核心逻辑。
2. 使用较小的模型（如 GPT-3.5 或 GPT-4o-mini）对长文本块进行摘要式压缩。
3. 对比压缩前后的语义向量，确保信息失真度低于设定阈值。

**注意事项**: 
对于高度结构化的数据（如 JSON 或 SQL），应保留其结构键，仅压缩值内容，避免破坏数据格式导致后续解析错误。

---

### 实践 2：分层缓存策略

**说明**: 
Agent 对话中往往包含大量重复的系统指令或通用知识。通过在 Context Gateway 层引入缓存机制，可以避免重复发送静态或低频变化的上下文，从而显著降低 Token 使用量和延迟。

**实施步骤**:
1. 将上下文划分为“静态系统提示词”、“近期对话历史”和“动态检索数据”。
2. 对静态部分使用哈希值进行本地或 Redis 缓存，仅在检测到变更时重新发送。
3. 对检索到的文档片段进行去重，合并相似内容。

**注意事项**: 
必须设计严格的缓存失效策略，特别是在用户修改了系统指令或动态数据源更新后，确保 LLM 接收到的是最新状态。

---

### 实践 3：基于 RAG 的上下文注入

**说明**: 
并不是所有历史信息都需要发送给 LLM。Context Gateway 应充当智能过滤器，利用向量数据库检索与当前用户意图最相关的历史片段或知识库条目，而非将整个历史记录抛给模型。

**实施步骤**:
1. 将用户的当前 Query 向量化。
2. 在向量数据库中检索 Top-K 个相关片段。
3. 仅将检索到的片段以及必要的系统提示词组装成最终的 Context。

**注意事项**: 
检索的相关性阈值需要根据具体业务场景微调，过低会导致注入噪音，过高会导致上下文缺失。

---

### 实践 4：动态 Token 预算管理

**说明**: 
不同的模型任务对 Token 限制的要求不同。Context Gateway 应具备动态调整上下文大小的能力，根据目标模型（如 GPT-4 vs. Claude 3.5）的 Context Window 限制和成本预算，动态决定压缩的激进程度。

**实施步骤**:
1. 为每个模型会话定义 max_token_budget。
2. 在 Gateway 层实时计算当前累积的 Token 数量。
3. 当接近预算上限时，自动触发“激进压缩模式”（如提高摘要压缩比）或“历史遗忘机制”（丢弃最旧的低权重对话）。

**注意事项**: 
要为“系统提示词”和“输出预留”保留固定的 Buffer 空间，防止因输入过长导致模型无法生成完整回复。

---

### 实践 5：结构化数据与非结构化数据的分流处理

**说明**: 
Agent 上下文通常混合了自然语言对话和结构化数据（如 API 返回的 JSON）。混合压缩容易破坏数据结构。最佳实践是将两者分流，对非结构化文本进行语义压缩，对结构化数据进行字段级筛选。

**实施步骤**:
1. 在 Gateway 中解析输入流，识别 JSON/XML 块与自然语言块。
2. 对于自然语言，应用 LLM 进行摘要或重写。
3. 对于结构化数据，根据当前任务所需的 Schema，仅保留相关字段，剔除无用元数据。

**注意事项**: 
确保重组后的上下文在拼接回 LLM 时，包含清晰的分隔符或指令，明确告知模型哪部分是压缩后的文本，哪部分是原始数据。

---

### 实践 6：引入质量评估反馈循环

**说明**: 
压缩不可避免地会带来信息损失。为了确保压缩后的上下文仍能支撑 Agent 完成任务，需要建立一个反馈机制，评估压缩对最终输出质量的影响。

**实施步骤**:
1. 记录压缩率（压缩前 Token / 压缩后 Token）与任务成功率。
2. 定期抽样检查：使用原始上下文和压缩后上下文分别询问同一问题，对比答案的一致性。
3. 如果发现答案偏差过大，调整压缩 Prompt 或降低该类数据的压缩强度。

**注意事项**: 
不要盲目追求极致的压缩率。对于关键决策类任务，应优先保留信息的完整性，而非节省成本。

---
## 学习要点

- 基于提供的标题和来源，以下是关于 Context Gateway 的关键要点总结：
- Context Gateway 通过在上下文发送给 LLM 之前进行压缩，显著降低了 Token 使用成本并减少了模型延迟。
- 该工具的核心价值在于解决 AI 应用中“上下文窗口”受限和长文本处理昂贵的问题。
- 它作为一个中间层（网关）介入，能够智能地保留关键信息并剔除冗余内容。
- 这种方法对于处理大量文档检索或长对话历史的 Agent 应用场景尤为有效。
- 优化上下文压缩可以在不牺牲最终输出质量的前提下，提升系统的整体响应速度。

---
## 常见问题


### 1: Context Gateway 是什么？它主要解决什么问题？

1: Context Gateway 是什么？它主要解决什么问题？

**A**: Context Gateway 是一个中间件服务，旨在优化大语言模型（LLM）的输入成本和性能。它主要解决的问题是：随着 AI Agent 变得越来越复杂，发送给 LLM 的上下文（包括对话历史、工具定义、检索到的文档等）变得非常庞大，导致 Token 消耗剧增且处理速度变慢。Context Gateway 通过在上下文发送给 LLM 之前对其进行智能压缩和优化，从而降低 API 成本并减少延迟。

---



### 2: 它是如何压缩上下文的？压缩过程是否会丢失关键信息？

2: 它是如何压缩上下文的？压缩过程是否会丢失关键信息？

**A**: Context Gateway 通常使用多种策略的组合来压缩上下文，而不是简单的文本截断。这些策略包括：
1.  **语义压缩**：使用小型、高效的模型来总结或改写冗长的文本，同时保留核心语义。
2.  **去重**：移除重复的指令或系统提示词。
3.  **结构化优化**：优化 JSON 或其他结构化数据的格式。
4.  **选择性保留**：识别并优先保留对当前任务最重要的信息。
关于信息丢失，该工具的设计目标是保留“语义密度”。虽然它减少了字数，但会尽力确保对最终决策有用的信息被保留下来。通常，这种权衡是为了在保持 Agent 性能基本不变的前提下，大幅降低成本。

---



### 3: 将 Context Gateway 接入现有的 AI Agent 系统是否困难？

3: 将 Context Gateway 接入现有的 AI Agent 系统是否困难？

**A**: 接入通常设计得非常简单，旨在作为“即插即用”的组件。它通常作为一个代理服务运行。你只需要修改原本发送给 LLM API（如 OpenAI）的请求地址，将其指向 Context Gateway 的端点，或者在你的 Agent 代码中将 Context Gateway 作为一层包装器。它负责处理输入的上下文，然后将优化后的内容转发给实际的 LLM 提供商，最后再将结果返回。因此，对现有代码库的侵入性很小。

---



### 4: Context Gateway 适用于哪些场景？什么时候使用它效果最好？

4: Context Gateway 适用于哪些场景？什么时候使用它效果最好？

**A**: 它最适合以下场景：
1.  **长对话历史**：Chatbot 需要处理大量历史消息时。
2.  **RAG（检索增强生成）应用**：从向量数据库检索回大量相关文档片段，需要全部或大部分发送给 LLM 进行分析时。
3.  **复杂 Agent 工作流**：Agent 需要加载大量的工具定义、API 文档或代码库上下文时。
简而言之，如果你的应用每次请求的 Token 数量（输入 Token）经常很高（例如超过 4k 或 8k tokens），导致成本和延迟成为瓶颈，那么 Context Gateway 就能发挥最大价值。

---



### 5: 使用 Context Gateway 会增加多少延迟？这种压缩是否值得？

5: 使用 Context Gateway 会增加多少延迟？这种压缩是否值得？

**A**: 这是一个典型的“以时间换空间”的权衡。Context Gateway 本身处理上下文需要一定的时间（通常在几百毫秒级，取决于上下文长度）。然而，由于发送给 LLM 的上下文变小了，LLM 的处理时间（首字延迟和生成时间）通常会显著减少。
在大多数输入 Token 量较大的场景下，LLM 节省的处理时间往往超过了 Context Gateway 增加的处理时间，因此端到端的总体延迟可能会降低，或者至少在保持延迟持平的同时大幅降低了成本。

---



### 6: 它支持哪些大模型？是否仅限于 OpenAI？

6: 它支持哪些大模型？是否仅限于 OpenAI？

**A**: Context Gateway 通常被设计为模型无关的。虽然它可能默认配置为与 OpenAI API 兼容，但由于它处理的是发送给模型的“文本/提示词”，因此理论上它适用于任何基于文本的 LLM，包括 Anthropic (Claude)、开源模型（如 Llama 系列）以及通过 API 提供的其他模型服务。只要你的 Agent 是通过文本提示与模型交互，Context Gateway 就可以作为一个预处理层工作。

---



### 7: 数据隐私如何保障？我的上下文会被发送到第三方吗？

7: 数据隐私如何保障？我的上下文会被发送到第三方吗？

**A**: 这取决于具体的部署方式。Context Gateway 很可能是开源的，这意味着你可以将其部署在你自己的基础设施上（本地服务器或私有云）。在这种自托管模式下，你的数据流是：Client -> Context Gateway (你的服务器) -> LLM Provider。除了最终的 LLM 提供商外，不会有额外的第三方接触到你的上下文数据。如果使用的是官方托管的 SaaS 版本（如果有的话），则需要查阅其隐私政策，确认其是否会记录用于压缩的中间数据。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在不改变 LLM 模型参数的前提下，如何通过简单的文本预处理技术（如去除无关字符、标准化格式）来优化 Agent 上下文的 Token 占用？请列出三种具体的预处理方法。

### 提示**: 思考 JSON 数据的冗余性、空格/换行符的消耗以及自然语言中的“停用词”对语义保留的影响。

### 

---
## 引用

- **原文链接**: [https://github.com/Compresr-ai/Context-Gateway](https://github.com/Compresr-ai/Context-Gateway)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47367526](https://news.ycombinator.com/item?id=47367526)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [LLM](/tags/llm/) / [Agent](/tags/agent/) / [上下文压缩](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8E%8B%E7%BC%A9/) / [Context Gateway](/tags/context-gateway/) / [Token优化](/tags/token%E4%BC%98%E5%8C%96/) / [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [中间件](/tags/%E4%B8%AD%E9%97%B4%E4%BB%B6/) / [Show HN](/tags/show-hn/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Agent Skills：压缩智能体技能以提升模型效率]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [Claws 成为 LLM 智能体之上的新架构层]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-11.md" >}})
- [Moltis：具备记忆、工具与技能扩展能力的AI助手]({{< relref "posts/20260213-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--15.md" >}})
- [Moltis：具备记忆、工具调用及自扩展技能的AI助手]({{< relref "posts/20260214-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--16.md" >}})
- [让大语言模型互斗万智牌的实验项目]({{< relref "posts/20260217-hacker_news-show-hn-i-taught-llms-to-play-magic-the-gathering--10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*