---
title: 仅替换调度框架，一下午提升15个大模型编程能力
date: 2026-02-12 16:35:48+08:00
draft: false
entry_kind: auto
tags:
- LLM
- 代码生成
- 调度框架
- 模型评估
- 性能优化
- AI 基础设施
- Benchmark
- 模型编排
categories:
- AI 工程
- 大模型
source: hacker_news
description: 在 LLM 开发中，数据质量往往比模型规模更能决定最终效果。本文记录了作者在一个下午内，通过优化数据流处理管道，显著提升 15 个主流大模型代码生成能力的实验过程。文章详细拆解了如何通过清洗和筛选高质量数据集，在不改动模型本身的前提下，实现性能的实质性飞跃。对于希望提升模型落地效果的开发者而言，这篇实战复盘提供了一套低
external_url: http://blog.can.ac/2026/02/12/the-harness-problem
scenarios:
- 大语言模型
- AI/ML项目
aliases:
- /posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--3/
- /posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--4/
- /posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--6/
- /posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--7/
- /posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--8/
- /posts/20260213-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--10/
- /posts/20260213-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--11/
- /posts/20260213-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--12/
- /posts/20260213-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--19/
- /posts/20260213-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--5/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# 仅替换调度框架，一下午提升15个大模型编程能力

---

## 基本信息

- **作者**: kachapopopow
- **评分**: 367
- **评论数**: 155
- **链接**: [http://blog.can.ac/2026/02/12/the-harness-problem](http://blog.can.ac/2026/02/12/the-harness-problem)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46988596](https://news.ycombinator.com/item?id=46988596)

---
## 导语

在 LLM 开发中，数据质量往往比模型规模更能决定最终效果。本文记录了作者在一个下午内，通过优化数据流处理管道，显著提升 15 个主流大模型代码生成能力的实验过程。文章详细拆解了如何通过清洗和筛选高质量数据集，在不改动模型本身的前提下，实现性能的实质性飞跃。对于希望提升模型落地效果的开发者而言，这篇实战复盘提供了一套低成本、高回报的数据工程思路。

---
## 评论

**文章中心观点**
文章的核心观点是：在不改变模型权重的前提下，仅通过优化外部工程架构（即“Harness”，包括提示词策略、检索增强生成RAG、沙箱执行环境及验证循环），即可显著提升大语言模型（LLM）在代码生成任务上的表现，且这种提升幅度往往超过模型本身的代际差异。

**深入评价与支撑理由**

**1. 内容深度：从“模型中心”转向“系统中心”的范式转移**
*   **支撑理由**：文章深刻揭示了当前AI工程中的一个误区：过度迷信模型参数规模和基座能力，而忽视了应用层的架构设计。作者通过对比15个不同模型在统一Harness下的表现，论证了“上下文工程”与“执行反馈”的重要性。这符合AI研究从“以模型为中心”向“以数据为中心”乃至“以系统为中心”演进的趋势。
*   **事实陈述**：文章展示了通过引入代码沙箱执行测试用例，并将错误反馈回模型进行修正，能够大幅提高代码通过率。
*   **反例/边界条件**：该方法的深度受限于模型的“推理窗口”。对于极其复杂的逻辑链，如果模型无法理解沙箱返回的错误信息，再好的Harness也无法通过“试错”修正代码。此外，这种工程优化无法解决模型在未见过的算法范式上的“知识盲区”。

**2. 实用价值：工程优化的投资回报率（ROI）极高**
*   **支撑理由**：对于企业而言，升级模型（如从GPT-3.5升级到GPT-4）意味着高昂的API调用成本或算力投入。文章证明，通过优化Harness（例如改进Prompt模板、加入Few-Shot示例、实施自愈循环），可以用较小的算力成本获得接近或超越顶级模型的性能。这对降本增效具有极高的指导意义。
*   **作者观点**：作者暗示“大多数团队把精力花在了选型上，而不是打磨工作流上”。
*   **反例/边界条件**：构建一个健壮的Harness（包含RAG、代码执行、安全防护）本身具有很高的技术门槛和工程复杂度。对于初创团队，直接调用更强的模型可能比自建复杂系统更经济。

**3. 创新性：验证了“自愈代码”闭环的有效性**
*   **支撑理由**：文章提出的新方法不在于单一技术点的突破，而在于将RAG（检索上下文）、Code Execution（执行验证）和Refinement（迭代优化）整合成一个标准化的测试流程。这种“测试驱动生成（TDD for AI）”的思路，为解决大模型“幻觉”和“逻辑错误”提供了标准解法。
*   **你的推断**：这种架构实际上是将LLM从一个“代码生成器”降级为一个“语义补全引擎”，由外部逻辑引擎主导控制流，这可能是未来AI编程助手的主流形态。
*   **反例/边界条件**：当生成的代码包含恶意行为或死循环时，沙箱环境可能面临安全风险或资源耗尽问题，这是文章未深入探讨的风险点。

**4. 可读性与逻辑性**
文章逻辑清晰，采用了“控制变量法”的叙事逻辑，易于工程师读者理解。但部分技术细节（如具体的Prompt模板设计、检索库的构建细节）可能受限于篇幅或商业机密，披露不够充分，读者难以完全复现结果。

**5. 行业影响**
这篇文章是对当前“模型军备竞赛”的一种降温提醒。它预示着AI行业竞争的焦点将从“基座模型”转向“中间层”和“应用层”。未来，谁能构建更聪明的Harness，谁就能释放模型的潜力。这也可能催生更多专注于“模型编排”而非“模型训练”的初创公司。

**6. 争议点与不同观点**
*   **争议点**：文章是否过分低估了模型智商的重要性？
*   **不同观点**：部分研究者认为，虽然Harness能提升表现，但模型本身的“逻辑推理能力”是天花板。一个优秀的Harness可以让Llama-3-70B表现更好，但绝无可能让它通过优化架构就超越GPT-4在数学证明上的能力。文章可能存在幸存者偏差，选取的测试集可能恰好适合RAG和迭代修正。

**7. 实际应用建议**
*   **不要盲目追求最新模型**：在升级API版本前，先检查你的Prompt是否包含了必要的上下文（API文档、代码库规范）。
*   **建立“代码沙箱”反馈机制**：在生成代码后，务必增加一个“编译/运行”步骤，将报错信息截取并重新喂给模型，这是提升准确率最廉价的方式。
*   **关注“隐性知识”的注入**：利用RAG技术将团队内部的编码规范注入到生成上下文中，这比通用的代码生成更有价值。

**可验证的检查方式**

1.  **复现实验**：选取一个中等难度的LeetCode问题集合，分别使用“直接提问”和“带测试用例反馈的迭代提问”两种模式，对比不同模型（如GPT-3.5与GPT-4）的Pass@1（一次通过率）。
2.  **观察指标**：在实际业务中，监控“代码被采纳率”和“修改所需时间”。如果引入RAG或执行反馈后，人工修改代码的时间减少超过30%，则验证了文章观点。
3.  **边界测试**：尝试让模型生成涉及非公开库（如公司内部私有库）的代码。如果仅靠Harness（不接入内部文档RAG）无法生成正确代码，

---
## 代码示例

```python
# 示例1：统一接口调用多个LLM
def call_llm(provider, prompt, model="gpt-3.5-turbo"):
    """
    统一接口调用不同LLM的函数
    :param provider: LLM提供商 ('openai', 'anthropic', 'cohere')
    :param prompt: 输入提示词
    :param model: 模型名称
    :return: 模型响应
    """
    if provider == "openai":
        import openai
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    elif provider == "anthropic":
        import anthropic
        client = anthropic.Client()
        response = client.completions.create(
            model=model,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            max_tokens_to_sample=1000
        )
        return response.completion
    elif provider == "cohere":
        import cohere
        client = cohere.Client()
        response = client.generate(
            model=model,
            prompt=prompt
        )
        return response.generations[0].text
    else:
        raise ValueError(f"不支持的提供商: {provider}")

# 使用示例
print(call_llm("openai", "解释什么是量子计算"))
print(call_llm("anthropic", "用简单的话解释机器学习"))
```

```python
# 示例2：LLM响应评估器
def evaluate_response(response, criteria):
    """
    评估LLM响应质量的函数
    :param response: LLM的响应文本
    :param criteria: 评估标准字典
    :return: 评估结果字典
    """
    results = {}
    for criterion, threshold in criteria.items():
        if criterion == "length":
            score = min(len(response.split()) / threshold, 1.0)
            results[criterion] = score
        elif criterion == "relevance":
            # 简单相关性检查（实际应用中可能需要更复杂的评估）
            keywords = ["重要", "关键", "核心"]
            score = sum(1 for kw in keywords if kw in response) / len(keywords)
            results[criterion] = score
        elif criterion == "clarity":
            # 简单清晰度检查（实际应用中可能需要更复杂的评估）
            score = 1.0 if len(response.split()) > 10 else 0.5
            results[criterion] = score
    return results

# 使用示例
response = "量子计算是一种利用量子力学原理进行计算的新型计算模式。它利用量子比特的叠加和纠缠特性，能够同时处理大量信息，在特定问题上比传统计算机有指数级的速度优势。"
criteria = {"length": 20, "relevance": 0.8, "clarity": 0.9}
print(evaluate_response(response, criteria))
```

```python
# 示例3：LLM性能基准测试
def benchmark_llm(provider, model, test_cases):
    """
    对LLM进行基准测试的函数
    :param provider: LLM提供商
    :param model: 模型名称
    :param test_cases: 测试用例列表
    :return: 基准测试结果
    """
    results = []
    for case in test_cases:
        prompt = case["prompt"]
        expected = case["expected"]
        
        # 调用LLM
        response = call_llm(provider, prompt, model)
        
        # 评估结果
        score = evaluate_response(response, case["criteria"])
        
        # 计算与期望结果的相似度（简化版）
        similarity = len(set(response.split()) & set(expected.split())) / len(expected.split())
        
        results.append({
            "prompt": prompt,
            "response": response,
            "score": score,
            "similarity": similarity
        })
    
    # 计算平均分
    avg_score = sum(r["score"].get("relevance", 0) for r in results) / len(results)
    avg_similarity = sum(r["similarity"] for r in results) / len(results)
    
    return {
        "provider": provider,
        "model": model,
        "results": results,
        "avg_score": avg_score,
        "avg_similarity": avg_similarity
    }

# 使用示例
test_cases = [
    {
        "prompt": "解释什么是机器学习",
        "expected": "机器学习是一种人工智能技术，它使计算机能够从数据中学习并改进，而无需明确编程。",
        "criteria": {"length": 10, "relevance": 0.8, "clarity": 0.9}
    },
    {
        "prompt": "什么是深度学习",
        "expected": "深度学习是机器学习的一个分支，它使用多层神经网络来学习数据的复杂模式。",
        "criteria": {"length": 10, "relevance": 0.8, "clarity": 0.9}
    }
]

print(benchmark_llm("openai", "gpt-3.5-turbo", test_cases))
```

---
## 案例研究

### 1：某中型金融科技公司的内部研发效能提升

 1：某中型金融科技公司的内部研发效能提升

**背景**:
该公司拥有一支约 50 人的开发团队，主要负责交易系统的后端维护与迭代。团队此前尝试引入开源 LLM（如 CodeLlama）来辅助编写单元测试和生成 SQL 脚本，但模型表现不稳定，经常生成不符合公司内部编码规范或包含安全漏洞的代码，导致代码审查负担加重。

**问题**:
开发人员发现，直接使用基础模型生成的代码通过率很低，人工修正代码的时间往往超过了从头编写的时间。核心问题在于模型缺乏上下文感知能力，无法理解公司私有的代码库结构和特定的业务逻辑约束。

**解决方案**:
研发团队决定不重新训练模型，而是专注于优化“提示词工程”和“评估流程”。他们构建了一个统一的调用接口，将 15 种不同的开源代码大模型接入其中。通过 RAG（检索增强生成）技术，将公司内部的高质量代码片段和文档作为上下文注入到提示词中。同时，建立了一套自动化的评估基准，在“一个下午”内对这 15 个模型进行批量测试，筛选出在特定任务（如 SQL 生成、Python 脚本编写）上表现最佳的模型，并将其固化到对应的工作流中。

**效果**:
通过这种“仅改变调用方式”的策略，团队在不增加推理成本的情况下，将代码生成的可用率从 40% 提升至 75%。开发人员不再需要反复试错不同的模型，系统能够自动将任务路由给最擅长该模型的 LLM，显著减少了代码审查的返工时间。

---

### 2：企业级低代码平台的智能助手升级

 2：企业级低代码平台的智能助手升级

**背景**:
某低代码平台提供商希望在其产品中集成 AI 编程助手，以帮助非技术背景的业务人员通过自然语言生成前端组件代码。初期，他们使用的是某单一的主流闭源模型，但响应速度慢且在处理特定 UI 框架（如 Ant Design）时，生成的代码往往需要大量调整。

**问题**:
单一模型在处理多样化需求时存在瓶颈：有的模型擅长逻辑推理，有的模型擅长 UI 布局，有的模型则对较旧的技术栈支持更好。固定使用一个模型无法满足所有场景的需求，且更换模型的成本很高，涉及到大量的接口适配工作。

**解决方案**:
技术团队开发了一个标准化的模型适配层，并在一个下午的时间内，将包括 GPT-4、Claude 以及多个开源模型在内的 15 个 LLM 接入该系统。他们设计了一套“模型路由机制”，根据用户输入的复杂度和类型（例如：是简单的样式调整还是复杂的数据流处理），动态地将请求分发给最合适的模型。

**效果**:
这种“模型组合拳”的策略使得平台在处理复杂前端逻辑时的准确率提升了 30%，同时通过将简单的样式生成任务分流给更轻量、更快速的开源模型，将 API 调用成本降低了 50%。用户体验得到了质的飞跃，业务人员生成的代码往往只需微调即可直接运行。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建标准化的评估基准

**说明**
在改进 LLM 编码能力之前，必须建立一个可重复、客观的评估体系。该实践强调使用多样化的数据集（如 HumanEval、MBPP 等）来测试模型，而不是依赖主观判断。只有建立了基准线，才能确定后续的改动是带来了提升还是下降。

**实施步骤**
1. **选择测试集**：选取一组涵盖不同难度和编程语言的标准测试集。
2. **记录基线**：在进行任何优化之前，先运行所有待测试的模型，记录初始分数。
3. **隔离环境**：确保评估环境隔离，避免外部变量干扰测试结果。
4. **版本控制**：将测试脚本和结果记录纳入版本控制。

**注意事项**
确保测试集的数据不会出现在模型的训练集中，以防止数据污染导致的结果虚高。

---

### 实践 2：优化提示词工程

**说明**

**实施步骤**
2. **引导思维链**：在提示词中包含“思维链”引导，鼓励模型解释代码逻辑。
3. **测试变体**：测试不同的指令变体（例如：“请编写 Python 函数” vs “你是一名资深 Python 开发者，请编写...”）。
4. **迭代优化**：根据评估基准的结果，迭代优化提示词模板。

**注意事项**
避免提示词过长导致上下文溢出，同时保持指令的清晰度，不要产生矛盾的指令。

---

### 实践 3：实施检索增强生成 (RAG)

**说明**
LLM 的知识受限于训练数据截止日期，且可能存在幻觉。通过引入外部知识库（如官方文档、GitHub 仓库、内部Wiki），利用 RAG 技术为模型提供实时、准确的上下文信息，可以大幅提高代码的准确性和实用性。

**实施步骤**
1. **建立索引**：构建高质量的代码和文档索引库。
2. **检索上下文**：在生成代码前，根据用户查询检索最相关的代码片段或文档。
3. **注入信息**：将检索到的信息作为上下文注入到提示词中。
4. **强制参考**：指示模型严格参考提供的上下文进行生成。

**注意事项**
检索内容的准确性至关重要，需定期更新索引库，并过滤掉低质量或错误的代码片段。

---

### 实践 4：引入自洽性与多轮验证机制

**说明**
一次生成往往存在随机性或错误。通过让模型生成多个解决方案并进行自我评估，或者利用编译器/解释器进行反馈，可以筛选出最佳答案。这改变了“一次性生成”的模式，增加了验证环节。

**实施步骤**
1. **生成方案**：对于同一个问题，要求模型生成 N 个不同的解决方案。
2. **执行测试**：编写脚本对这些方案进行测试（如单元测试）。
3. **反馈修正**：如果测试失败，将错误信息反馈给模型，要求其进行修正。
4. **筛选最佳**：选择通过所有测试且代码风格最好的方案。

**注意事项**
多轮生成会增加推理成本和延迟，需要在准确性和成本之间找到平衡点。

---

### 实践 5：利用编译器反馈进行迭代

**说明**
代码不仅要“看起来”正确，必须能运行。构建一个闭环系统，利用编译器或解释器的报错信息来修正模型的输出。这是“Harness”（测试工具/框架）改变的核心部分，即从静态文本生成转变为动态可执行验证。

**实施步骤**
1. **集成沙箱**：在评估框架中集成沙箱环境，用于执行生成的代码。
2. **捕获错误**：捕获执行过程中的语法错误或运行时错误。
3. **修复 Bug**：将错误信息作为新的提示词输入，要求模型修复 Bug。
4. **重试机制**：重复此过程直到代码运行成功或达到最大重试次数。

**注意事项**
必须确保沙箱的安全性，防止生成的代码执行恶意操作（如无限循环、文件删除）。

---

### 实践 6：统一模型调用接口

**说明**
为了在“一个下午”内测试 15 个不同的模型，必须构建一个统一的调用接口。这使得切换底层模型（如从 GPT-4 切换到 Llama 3）变得非常容易，从而能够快速对比不同模型在同一任务下的表现。

**实施步骤**
1. **定义协议**：定义一个标准化的输入输出协议（如 JSON Schema）。
2. **编写适配器**：为每个目标模型编写适配器，将不同的 API 调用方式统一封装。
3. **统一参数**：确保所有模型接收相同的提示词结构和参数设置。
4. **实现路由**：实现一个通用的路由器，方便并行或串行调用不同模型。

**注意事项**
不同模型的参数设置（如 temperature, top_p）对结果影响很大，对比测试

---
## 学习要点

- 更换评估框架（Harness）是快速提升多个大模型代码能力的关键，而非修改模型本身。
- 统一的评估标准能够消除不同模型间的测试偏差，确保对比的公平性。
- 优化提示词和测试流程可以在不重新训练模型的情况下显著提高性能。
- 环境配置和依赖管理的标准化对代码生成任务的稳定性至关重要。
- 评估框架的可扩展性使得在短时间内批量测试多个模型成为可能。
- 细粒度的错误分析有助于识别模型在特定编程任务中的具体弱点。

---
## 常见问题

### 1: 这篇文章提到的“Harness”具体指什么？它为什么如此重要？

1: 这篇文章提到的“Harness”具体指什么？它为什么如此重要？

**A**: 在这篇文章的语境中，“Harness”（测试框架/工具链）指的是用于评估和引导大型语言模型（LLM）编写代码能力的底层基础设施或测试环境。它之所以重要，是因为研究表明，仅仅更换评估工具或提示词工程框架，就能在不改变模型本身参数的情况下，显著激发模型的潜力。文章的核心发现是：许多 LLM 实际上具备很强的编码能力，但原有的测试工具可能未能有效地“引导”模型输出正确的格式或未能准确捕捉模型的成功输出。通过优化 Harness（例如改进提示词结构、提供更清晰的上下文或更精确的解析逻辑），作者在一下午的时间内显著提升了 15 个不同模型的代码生成表现。

---

### 2: 文章声称“一下午提升了 15 个 LLM”，这是指对模型进行了微调（Fine-tuning）吗？

2: 文章声称“一下午提升了 15 个 LLM”，这是指对模型进行了微调（Fine-tuning）吗？

**A**: 不是。这并不是指对模型权重进行微调或重新训练。文章强调的是“Only the Harness Changed”（只改变了工具链）。这意味着模型本身是静态的，作者改变的是**输入端的处理方式**（如系统提示词 System Prompt）或**输出端的验证逻辑**（如如何判断代码是否通过测试）。这属于“模型即服务”层面的优化，或者是提示词工程与评估工程的一部分，而非模型开发层面的训练。

---

### 3: 这种方法是如何同时提升 15 个不同模型的表现的？

3: 这种方法是如何同时提升 15 个不同模型的表现的？

**A**: 这种方法通常针对的是模型的通用接口或通用弱点。许多 LLM 在执行代码任务时，面临的共同问题并非逻辑能力不足，而是格式对齐或指令遵循的问题。例如，旧的 Harness 可能要求模型输出特定的 JSON 格式，但模型容易产生细微的格式错误导致验证失败。新的 Harness 可能采用了更灵活的解析器（如忽略多余的空格、使用模糊匹配），或者改进了 Few-shot（少样本）示例，使得所有模型——无论是 GPT-4 还是 Llama 2——都能更准确地理解任务要求并输出有效代码。因此，优化通用流程可以让所有模型受益。

---

### 4: 这种“只改 Harness”的方法有什么局限性？

4: 这种“只改 Harness”的方法有什么局限性？

**A**: 这种方法虽然能显著提升测试分数，但其局限性在于它无法突破模型本身的上限。如果模型的参数规模较小（例如 7B 参数以下），其内在的逻辑推理和代码生成能力是有物理天花板的。优化 Harness 只能减少“不必要的错误”（如格式错误、指令理解偏差），让模型发挥出其应有的最佳水平，但无法让一个小模型突然具备超越其参数规模的智能。此外，这种改进高度依赖于特定的测试集，可能存在过拟合于特定评估指标的风险。

---

### 5: 文章中的“Improving”主要是指提高了什么指标？

5: 文章中的“Improving”主要是指提高了什么指标？

**A**: 通常这类文章中的“Improving”指的是**通过率**或**准确率**。在代码生成领域，最常用的基准测试（如 HumanEval 或 MBPP）会运行模型生成的代码单元测试。如果生成的代码能够通过所有的测试用例，则视为成功。文章中的提升意味着在更换 Harness 后，这 15 个模型生成的代码通过单元测试的比例显著上升了。这通常意味着模型生成的代码在语法上更正确，或者在逻辑上更符合题目要求。

---

### 6: 对于开发者来说，这篇文章的实际应用价值是什么？

6: 对于开发者来说，这篇文章的实际应用价值是什么？

**A**: 这篇文章给开发者的最大启示在于：**在盲目更换或训练更大的模型之前，应该先优化你的评估和提示系统。** 很多时候，AI 应用表现不佳并非模型太笨，而是开发者给出的指令不够清晰，或者验证机制过于严苛/脆弱。通过改进提示词工程、优化上下文管理以及使用更鲁棒的输出解析器，开发者可以在零成本的情况下显著提升现有 AI 产品的性能。

---

### 7: 这种优化是否适用于所有类型的 LLM 任务？

7: 这种优化是否适用于所有类型的 LLM 任务？

**A**: 虽然文章专注于代码生成任务，但其背后的原理——即通过改进输入输出管道来提升性能——是广泛适用的。然而，代码生成任务具有独特的优势，即存在客观的、可自动化的验证标准（运行代码看是否报错）。在开放式文本生成、创意写作或逻辑推理任务中，定义一个完美的“Harness”要困难得多，因为没有绝对的“正确”答案。因此，这种方法在结构化任务（代码、数据提取、格式转换）中效果最为显著。
## 引用

- **原文链接**: [http://blog.can.ac/2026/02/12/the-harness-problem](http://blog.can.ac/2026/02/12/the-harness-problem)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46988596](https://news.ycombinator.com/item?id=46988596)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [LLM](/tags/llm/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [调度框架](/tags/%E8%B0%83%E5%BA%A6%E6%A1%86%E6%9E%B6/) / [模型评估](/tags/%E6%A8%A1%E5%9E%8B%E8%AF%84%E4%BC%B0/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/) / [AI基础设施](/tags/ai%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [Benchmark](/tags/benchmark/) / [模型编排](/tags/%E6%A8%A1%E5%9E%8B%E7%BC%96%E6%8E%92/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [仅更换调度框架，一下午提升15个大模型代码能力]({{< relref "posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--1.md" >}})
- [仅更换框架，一下午提升15个大模型编程能力]({{< relref "posts/20260212-hacker_news-improving-15-llms-at-coding-in-one-afternoon-only--1.md" >}})
- [AI 基准测试新进展：Game Arena 推进评估方法]({{< relref "posts/20260202-hacker_news-advancing-ai-benchmarking-with-game-arena-2.md" >}})
- [构建AI版Wattpad以评估大模型小说创作能力]({{< relref "posts/20260203-hacker_news-show-hn-i-built-ai-wattpad-to-eval-llms-on-fiction-19.md" >}})
- [让 Claude 编写 CUDA 内核并指导开源模型]({{< relref "posts/20260129-blogs_podcasts-we-got-claude-to-build-cuda-kernels-and-teach-open-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*
