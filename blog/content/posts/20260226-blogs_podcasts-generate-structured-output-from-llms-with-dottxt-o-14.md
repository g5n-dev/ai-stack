---
title: "在 AWS SageMaker 上利用 Dottxt Outlines 实现 LLM 结构化输出"
date: 2026-02-26T07:42:03+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "结构化输出", "AWS", "SageMaker", "Outlines", "Dottxt", "JSON Schema", "生成式 AI"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "以下是对该内容的简洁总结： **主题：在 AWS 上利用 Dottxt Outlines 实现大模型结构化输出** 本文主要探讨了如何通过 AWS Marketplace 在 Amazon SageMaker 中部署并使用 **Dottxt 的 Outlines 框架**，以解决大语言模型（LLM）生成非结构化文本的问"
external_url: https://aws.amazon.com/blogs/machine-learning/generate-structured-output-from-llms-with-dottxt-outlines-in-aws
scenarios: ["大语言模型", "AI/ML项目", "Web应用开发"]
---

# 在 AWS SageMaker 上利用 Dottxt Outlines 实现 LLM 结构化输出

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-24T15:42:34+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/generate-structured-output-from-llms-with-dottxt-outlines-in-aws](https://aws.amazon.com/blogs/machine-learning/generate-structured-output-from-llms-with-dottxt-outlines-in-aws)

---
## 摘要/简介

本文探讨了如何通过 Dottxt 的 Outlines 框架，借助 AWS Marketplace 在 Amazon SageMaker 中实现结构化输出，作为一种切实可行的实践方案。

---
## 导语

随着大语言模型（LLM）在企业级应用中的深入，确保输出符合特定格式已成为开发者的核心挑战。本文聚焦于 Dottxt 的 Outlines 框架，详细解析如何借助 AWS Marketplace 在 Amazon SageMaker 内部实现高可靠性的结构化输出。通过阅读此文，您将掌握一套切实可行的部署方案，从而有效解决模型输出不稳定的问题，并将其平滑集成至现有的生产环境。

---
## 摘要

以下是对该内容的简洁总结：

**主题：在 AWS 上利用 Dottxt Outlines 实现大模型结构化输出**

本文主要探讨了如何通过 AWS Marketplace 在 Amazon SageMaker 中部署并使用 **Dottxt 的 Outlines 框架**，以解决大语言模型（LLM）生成非结构化文本的问题，实现可靠的结构化数据输出。

**核心要点如下：**

1.  **背景与挑战**：
    LLM 原生输出通常为非结构化的自然语言。但在生产环境中，开发者往往需要模型输出符合特定格式（如 JSON）的数据以便下游系统调用。传统的提示词约束往往不够稳定，因此需要更技术性的框架来保证输出格式的严谨性。

2.  **解决方案：Dottxt Outlines**：
    Outlines 是一个专门用于生成结构化输出的 Python 库。它能够强制 LLM 的输出符合预定义的结构（例如正则表达式或 JSON Schema），从而确保模型生成的是可以直接被代码解析的合法数据，而不是伪装成 JSON 的文本片段。

3.  **AWS 实施路径**：
    文章介绍了具体的落地步骤，即在 **Amazon SageMaker**（AWS 的机器学习平台）内通过 **AWS Marketplace** 获取 Dottxt 的模型或容器。这意味着企业可以在 AWS 的云基础设施中，直接利用 Outlines 的能力来构建安全、合规的生成式 AI 应用，而无需自行搭建复杂的底层约束逻辑。

**总结：**
这篇文章为开发者提供了一份实践指南，展示了如何在 AWS 生态系统中集成 Outlines 框架，将 LLM 从单纯的文本生成器转变为能够提供稳定、结构化接口的数据服务，适用于需要高可靠性的企业级应用场景。

---
## 评论

**文章中心观点**
该文章主张通过在 AWS SageMaker 上集成 Dottxt 的 Outlines 框架，利用结构化生成技术来解决大语言模型（LLM）在实际生产环境中输出格式不稳定的问题，从而实现企业级应用的高可靠性与自动化集成。

**深入评价与分析**

**1. 内容深度与论证严谨性**
*   **支撑理由：** 文章触及了 LLM 工程化落地的核心痛点——非结构化文本与结构化数据（如 JSON、函数调用参数）之间的转换鸿沟。Outlines 框架的核心价值在于将生成过程约束在正则语言或上下文无关文法（CFG）定义的集合内。文章若深入探讨了如何通过修改模型的 Logits（对数几率）在采样阶段屏蔽非法 Token，则具备较高的技术深度。
*   **事实陈述：** 传统的 JSON Schema 验证是“事后补救”，而 Outlines 采用的是“事前约束”，这从根本上杜绝了格式错误，降低了 Token 消耗和重试率。
*   **反例/边界条件：** 对于极度复杂的嵌套 Schema 或需要极高创造性发散的文本生成任务，强制结构化约束可能会抑制模型的生成能力，导致输出变得生硬或出现语义截断。此外，该技术对推理服务器的底层推理引擎（如 vLLM, TensorRT-LLM）有较强的依赖性，并非所有老旧的 SageMaker 镜像都能无缝集成。

**2. 实用价值与行业影响**
*   **支撑理由：** 在 AWS Marketplace 上提供现成的解决方案极大地降低了企业的试错成本。对于正在构建 Agent（智能体）工作流或 RAG（检索增强生成）应用的开发者而言，能够保证模型输出 100% 符合 API 定义是至关重要的。
*   **你的推断：** 这篇文章实际上预示了 LLM 应用开发从“Prompt Engineering（提示工程）”向“Grammar Engineering（文法工程）”的范式转移。它强调了基础设施层面的控制，而非仅通过 Prompt 来祈求模型格式正确。
*   **反例/边界条件：** 如果企业已经深度绑定了 OpenAI 的 GPT-4 等闭源模型服务（这些服务已原生支持 Structured Outputs 或 Function Calling），在 SageMaker 上自建 Outlines 方案在运维成本和延迟上可能并不具备优势。该方案更适合对数据隐私敏感、必须使用私有化部署模型的企业。

**3. 创新性与可读性**
*   **支撑理由：** 文章的创新点在于将开源社区的高效框架与 AWS 的云基础设施进行了商业化的结合。它将复杂的数学原理（有限状态机与 Token 空间的映射）封装为可部署的产品。
*   **反例/边界条件：** 这种“缝合”并非技术原理的创新。Outlines 本身并非唯一选择，微软的 Guidance、Llama.cpp 的 Grammar Sampling 等技术路径同样存在，文章若未进行横向对比，则显得视野略显局限。

**争议点与不同观点**
*   **性能损耗争议：** 虽然约束采样减少了重试，但在推理端施加 Logits Mask 会增加计算负担。有观点认为，随着模型越来越大，通过微调让模型学会输出格式比在推理时强行约束更高效。文章可能低估了在大规模并发请求下，动态生成掩码矩阵对 GPU 显存带宽的压力。

**实际应用建议**
1.  **适用场景：** 强烈推荐用于需要将 LLM 接入传统数据库、API 调用链或自动化流水线的场景，特别是金融、医疗数据提取等对格式零容忍的领域。
2.  **技术选型：** 在采用前，务必评估你的基础模型是否支持 Logits Processor 接口。如果使用的是高度优化的量化模型（如 AWQ 4bit），需验证 Outlines 是否能正确加载并修改推理层。
3.  **混合策略：** 不要对所有任务都使用强约束。对于需要创意的文本生成，仍应使用自然语言 Prompt；仅在数据提取和工具调用阶段启用 Outlines。

**可验证的检查方式**
1.  **格式严格性测试：** 针对特定的 JSON Schema，连续生成 10,000 次，统计格式解析失败率。指标要求：Error Rate = 0。
2.  **延迟对比实验：** 在同等并发量下，对比使用 Outlines 约束生成与使用 Re-prompt（如果格式错误则要求重试）策略的平均首字延迟（TTFT）和总延迟。观察窗口：高并发场景（如 100 QPS）。
3.  **幻觉率评估：** 在结构化字段中（如日期、ID），检查模型是否为了满足格式约束而编造虚假信息。观察点：结构化正确但语义错误的样本比例。

---
## 技术分析

以下是对文章《Generate structured output from LLMs with Dottxt Outlines in AWS》核心观点与技术要点的深度分析。

---

# 深度分析报告：基于 Dottxt Outlines 与 AWS 的 LLM 结构化输出方案

## 1. 核心观点深度解读

**主要观点：**
文章的核心主张是，利用 **Dottxt 的 Outlines 框架** 结合 **AWS SageMaker**，是解决大语言模型（LLM）“幻觉”和格式不稳定问题的最佳工程实践之一。它主张通过**结构化生成**技术，将LLM从自由文本生成器转变为可靠的数据处理组件，从而使其能够安全地接入企业级生产工作流。

**核心思想：**
作者传达的核心思想是**“约束即自由”**。通过正则表达式或JSON Schema对模型的解码过程进行数学上的严格约束，可以在不改变模型权重（无需重新训练）的情况下，强制模型输出符合预定义的结构。这使得LLM不再仅仅是一个聊天机器人，而是一个可信赖的、确定性的API接口。

**创新性与深度：**
该观点的创新性在于将**生成式AI的不确定性**与**传统软件工程的确定性**进行了桥接。传统的Prompt Engineering（提示工程）依赖于概率性的“希望”模型输出正确格式，而Outlines通过修改推理过程中的采样逻辑，从数学上保证了输出格式的100%符合率。这是一种从“软约束”向“硬约束”的思维转变。

**重要性：**
这个观点至关重要，因为它是LLM落地企业级应用的最大瓶颈之一。企业无法容忍一个下游系统因为上游LLM少输出了一个逗号而崩溃。结构化输出是LLM从“玩具”走向“工具”，从“内容生成”走向“业务逻辑处理”的关键基础设施。

## 2. 关键技术要点

**涉及的关键技术：**
*   **Dottxt Outlines:** 一个轻量级Python库，用于强制模型输出遵循JSON Schema、正则表达式或Pydantic模型。
*   **AWS SageMaker & AWS Marketplace:** 用于托管和部署模型的基础设施。
*   **结构化生成:** 区别于传统的“生成后校验”方法。
*   **状态机/掩码:** 在Transformer推理过程中，动态限制下一个token的词汇表。

**技术原理：**
Outlines 的核心原理在于**推理时的词汇表干扰**。
1.  **传统LLM推理：** 在每一步生成时，模型计算整个词汇表中每个Token的概率，并选择概率最高的。
2.  **Outlines推理：** 在生成之前，Outlines根据用户提供的JSON Schema或Regex构建一个**有限状态机（FSM）**。在每一步生成时，FSM会计算出哪些Token是合法的（例如，在JSON键值对中，冒号后面合法的Token只能是引号或数字开头）。
3.  **逻辑门控：** Outlines将非法Token的概率强行置为负无穷（或零），只保留合法Token。因此，模型**不可能**生成格式错误的文本。

**技术难点与解决方案：**
*   **难点：** 如何在不重训练模型的情况下干预其生成逻辑？
*   **解决方案：** 利用了Transformer架构的特性，输出仅依赖于当前的Logits。通过在Logits层面应用掩码，无需接触模型内部参数即可控制输出。
*   **难点：** 性能损耗。
*   **解决方案：** 这种方法实际上减少了模型需要考虑的Token数量，在某些情况下甚至能略微加速推理过程。

**技术创新点：**
*   **零样本结构化：** 不需要微调模型即可遵循复杂的JSON结构。
*   **类型安全：** 直接与Python的类型系统（如Pydantic）集成，实现了从模型到代码对象的无缝转换。

## 3. 实际应用价值

**指导意义：**
对于AI工程师而言，这篇文章提供了一条将LLM能力集成到传统后端服务的标准路径。它标志着开发范式的转变：从“写Prompt -> 解析字符串 -> Try/Catch异常”转变为“定义数据结构 -> 获取对象 -> 业务逻辑”。

**应用场景：**
1.  **数据提取与非结构化转结构化：** 从发票、合同或医疗报告中提取特定字段，直接存入数据库。
2.  **Agent工具调用：** Function Calling的基础。Agent需要生成特定的函数参数（如JSON格式）来执行工具，Outlines保证了参数的准确性。
3.  **知识图谱构建：** 实体和关系的抽取必须严格符合Schema。
4.  **API编排：** LLM作为不同微服务之间的中间件，负责将请求转换为特定格式的JSON。

**需要注意的问题：**
*   **模型能力上限：** 约束只能保证格式正确，不能保证内容正确。模型仍可能生成符合格式但语义错误的“幻觉”。
*   **长上下文限制：** 极其复杂的JSON Schema可能会消耗大量上下文窗口。

**实施建议：**
建议在所有需要将LLM输出传递给程序代码（而非直接展示给人类）的场景中，默认采用结构化输出方案。

## 4. 行业影响分析

**对行业的启示：**
行业正在从“模型中心论”转向“工程中心论”。单纯拥有强大的基座模型已不再足够，如何通过工程化手段（如Outlines）驯化模型，使其适应工业级标准，成为竞争的关键。

**可能带来的变革：**
*   **RAG架构的进化：** 未来的RAG系统将不再返回文本块，而是直接返回结构化的对象，使得检索更加精准。
*   **LLM Ops标准化：** 结构化输出将成为LLM Ops中的必选项，而非可选项。

**发展趋势：**
*   **原生支持：** 像OpenAI的GPT-4o、Google的Gemini等前沿模型已经开始在API层面原生支持结构化输出（Function Calling），Outlines代表了开源社区对这一能力的平权化（让开源Llama/Qwen也能做到）。
*   **端侧部署：** 由于Outlines不需要额外的模型或服务器，它非常适合在边缘设备上运行的结构化数据提取任务。

## 5. 延伸思考

**引发的思考：**
*   **推理速度与准确率的权衡：** 严格的Token掩码是否会影响模型的创造力？在创意写作任务中应避免使用，但在逻辑任务中必须使用。
*   **多模态结构化：** 这种技术能否扩展到图像生成？例如强制生成符合特定布局的UI设计图？

**拓展方向：**
*   **流式结构化输出：** 目前Outlines主要处理完整生成，如何在流式传输中保证部分JSON的有效性是一个技术难点。
*   **反馈闭环：** 将结构化输出的验证结果反馈给RLHF（基于人类反馈的强化学习）流程，以训练出天生更懂格式的模型。

## 6. 实践建议

**如何应用到项目中：**
1.  **环境搭建：** 在AWS SageMaker中使用Deep Learning AMI，通过pip安装`outlines`库。
2.  **模型部署：** 从AWS Marketplace订阅并部署兼容的模型（如Llama-3-8b-Instruct）到SageMaker端点。
3.  **Schema定义：** 使用Pydantic定义你的输出数据模型。
4.  **代码集成：** 使用`outlines`库调用SageMaker端点，传入Schema。

**行动建议：**
*   **第一步：** 不要试图重构整个系统。先从一个简单的“文本分类”或“实体提取”微服务开始尝试。
*   **第二步：** 建立严格的单元测试，测试模型在极端输入下是否仍能输出符合Schema的JSON（即使内容是乱码，格式也不能错）。

**注意事项：**
*   确保使用的模型分词器与Outlines的兼容性。
*   注意AWS SageMaker的冷启动时间，对于高频实时调用可能需要预热。

## 7. 案例分析

**成功案例（模拟）：**
*   **场景：** 一家金融科技公司需要从数以万计的PDF财报中提取“净利润”、“同比增长率”等关键指标。
*   **传统做法：** 使用正则表达式硬匹配，维护成本极高，遇到格式变化就失效。
*   **Outlines做法：** 定义一个Pydantic模型包含`net_profit: float`和`growth_rate: float`。将财报文本输入Llama-3-70b（通过SageMaker部署），使用Outlines强制输出JSON。
*   **结果：** 提取成功率达到95%以上，且输出直接入库，无需复杂的清洗代码。

**失败反思：**
*   **场景：** 要求模型生成一段极具创意的营销文案，并强制其结构为`{"intro": "...", "body": "...", "call_to_action": "..."}`。
*   **问题：** 虽然格式正确，但模型为了符合字段长度限制或结构逻辑，可能牺牲了文案的流畅度和感染力。
*   **教训：** 结构化输出是逻辑的枷锁，不要用在需要高度艺术自由度的生成任务中。

## 8. 哲学与逻辑：论证地图

**中心命题:**
**在生产环境中部署大语言模型时，采用基于推理约束的结构化生成技术（如 Dottxt Outlines）是确保系统可靠性与可维护性的必要条件。**

**支撑理由:**
1.  **确定性需求:** 软件工程依赖于确定性的接口，LLM的概率性输出本质与现有系统不兼容。
    *   *依据:* 传统软件崩溃的主要原因之一是空指针或类型错误，非结构化的LLM输出引入了这种风险。
2.  **成本效益:** 基于推理约束的方法比微调模型更高效、更灵活。
    *   *依据:* 微调需要大量数据和算力，且难以适应Schema的频繁变更；Outlines只需修改一行代码即可改变输出结构。
3.  **原生能力局限:** 即使是最先进的模型（如GPT-4），在没有约束的情况下也无法保证100%的JSON格式有效性（特别是复杂的嵌套结构）。
    *   *依据:* OpenAI官方文档也指出，对于极复杂的Schema，必须使用Function Calling或Strict Mode来保证格式。

**反例 / 边界条件:**
1.  **创意生成任务:** 在写诗、写故事等任务中，结构化约束会显著降低模型的创造性和语言的流畅度。
2.  **极低延迟场景:** 如果应用对延迟极其敏感（毫秒级），复杂的FSM计算可能会引入不可接受的延迟（尽管通常很小，但在边缘设备上可能明显）。

**命题性质分析:**
*   **事实判断:** Outlines确实能通过数学约束保证格式正确。
*   **价值判断:** “必要条件”是一种价值判断，意味着如果不这样做，系统在工程上是“不合格”的。
*   **可检验预测:** 随着Agent系统复杂度的增加，不使用结构化输出的系统维护成本将呈指数级上升，最终导致系统不可用。

**立场与验证:**
*   **立场:** 强力支持。在所有涉及数据流转的后端逻辑中，必须使用结构化输出。
*   **验证方式:**
    *   **指标:** 统计生产环境中“后处理解析失败”的次数。使用Outlines后，该指标应降为0。
    *   **实验:** 对比Prompt Engineering（要求模型输出JSON）与Outlines在1000次随机请求下的格式合规率。前者通常在95%-98%，后者应为100%。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Pydantic 模型定义严格的数据结构

**说明**: 使用 Python 的 Pydantic 库定义强类型的输出模型。Outlines 库能够直接读取 Pydantic 模型的类定义，并将其转换为 JSON Schema，从而强制 LLM 仅输出符合该结构的 JSON 数据。这确保了从 AWS 环境中返回的数据是可预测且易于代码集成的。

**实施步骤**:
1. 安装 `outlines` 和 `pydantic` 库。
2. 定义一个继承自 `pydantic.BaseModel` 的类，明确字段名称和类型（如 `str`, `int`, `float`）。
3. 在调用 Outlines 的生成函数时，使用 `schema=` 参数传入该 Pydantic 模型。

**注意事项**: 确保模型中的字段名称和描述非常清晰，因为 LLM 会依据这些元数据来填充内容。

---

### 实践 2：在 AWS Lambda 中优化冷启动性能

**说明**: 在 AWS Lambda 等无服务器环境中使用 Outlines 时，库的加载和模型初始化可能会影响冷启动时间。为了优化性能，应尽量减少每次调用的初始化开销。

**实施步骤**:
1. 将 Outlines 的客户端初始化代码放在 Lambda 处理程序函数之外，利用全局变量进行复用。
2. 确保 Lambda 层包含所有必要的依赖项，以避免运行时下载。
3. 如果可能，预编译正则表达式或 Schema 结构。

**注意事项**: 监控 Lambda 的初始化时间和执行时间，以平衡内存分配与冷启动速度。

---

### 实践 3：使用正则表达式约束特定格式

**说明**: 除了 JSON 结构外，有时需要 LLM 输出特定格式的字符串（如电子邮件、电话号码或特定 ID）。Outlines 支持将正则表达式作为结构化约束传递给 LLM，确保输出完全匹配模式。

**实施步骤**:
1. 定义所需的正则表达式模式。
2. 使用 `outlines.generate.regex()` 方法（或对应函数）将正则模式应用于生成过程。
3. 将提示词与正则约束结合，发送给托管在 AWS 上的模型（如 Bedrock 或 SageMaker）。

**注意事项**: 复杂的正则表达式可能会增加推理时的计算负担，导致延迟增加，应保持正则表达式的简洁性。

---

### 实践 4：实施重试机制处理格式错误

**说明**: 尽管使用了结构化生成，但在极端情况下模型仍可能偶尔返回不完整或格式略有偏差的数据。在 AWS 分布式环境中，网络抖动或模型端点超时也可能导致问题。

**实施步骤**:
1. 在调用 Outlines 生成函数的外层包裹重试逻辑（如使用 Python 的 `tenacity` 库）。
2. 设置最大重试次数（例如 3 次）。
3. 捕获特定的异常（如 `json.JSONDecodeError` 或 Outlines 特定的验证错误）。

**注意事项**: 指数退避策略应与 AWS 服务的速率限制保持一致，避免在重试时触发限流。

---

### 实践 5：结合 Amazon Bedrock Guardrails 进行安全过滤

**说明**: 结构化生成保证了格式，但不能保证内容的安全性。结合 AWS Bedrock Guardrails 可以在生成过程中过滤敏感信息、仇恨言论或有害内容。

**实施步骤**:
1. 在 AWS Bedrock 中配置 Guardrail，定义拒绝主题和敏感信息过滤器。
2. 在通过 Outlines 调用 Bedrock 模型时，关联创建的 Guardrail ID。
3. 验证输出结构的同时，确认内容未触发屏蔽机制。

**注意事项**: Guardrails 可能会拦截某些提示词，导致输出为空或错误，需要在代码中妥善处理此类阻断响应。

---

### 实践 6：构建高效的提示词模板

**说明**: 为了提高结构化输出的准确性，提示词必须明确指示模型遵循特定的模式。Outlines 负责强制执行结构，但提示词负责引导内容的语义正确性。

**实施步骤**:
1. 在系统提示词中明确说明“必须返回符合以下 JSON Schema 的数据”。
2. 在提示词中提供少量示例，展示输入与期望的 JSON 输出之间的关系。
3. 使用 Jinja2 或类似模板引擎管理复杂的提示词结构，便于维护。

**注意事项**: 提示词中的指令不要与 Outlines 强制的 Schema 产生逻辑冲突，例如要求输出自由文本却强制一个严格的对象结构。

---

### 实践 7：监控与日志记录

**说明**: 在生产环境中，必须记录结构化生成的成功率、延迟和输出质量。利用 AWS CloudWatch 可以监控 Outlines 集成的健康状况。

**实施步骤**:
1. 记录每次生成的输入 Token 数、输出 Token 数和总延迟时间。
2. 记录结构化验证失败的日志，以便分析 Schema 是否过于复杂或提示词是否模糊。
3. 设置 CloudWatch 告警，用于检测异常高的错误率或延迟。

**注意事项**: 在记录日志时，注意过滤敏感数据（PII

---
## 学习要点

- Dottxt Outlines 库通过结构化约束机制，能够确保 LLM 严格遵循预定义的 JSON、XML 或 Pydantic 模型输出，从而有效消除生成格式错误的风险。
- 在 AWS 环境中集成 Outlines 可实现端到端的类型安全，将非结构化的模型输出直接转化为 AWS Lambda 或 API Gateway 可直接使用的代码对象，无需编写繁琐的解析或验证代码。
- 该方案通过强制模型输出符合特定模式（如正则表达式或 JSON Schema），显著降低了 LLM 产生幻觉或生成无效数据的概率，提高了生产环境的可靠性。
- 利用 Outlines 的结构化生成能力，开发者可以构建更确定性的 LLM 工作流，使模型输出能够无缝对接传统的确定性软件逻辑和数据库系统。
- 在 AWS 上部署时，该工具通过减少对模型输出进行后处理和重试的需求，优化了 token 使用效率并降低了推理成本。
- 此方法支持流式处理结构化数据，允许在生成过程中逐步验证输出格式，提升了实时应用的响应速度和用户体验。
- 通过将输出模式定义作为提示词的一部分，Outlines 实现了从自然语言请求到结构化数据的直接转换，简化了基于 RAG 或函数调用的应用开发流程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/generate-structured-output-from-llms-with-dottxt-outlines-in-aws](https://aws.amazon.com/blogs/machine-learning/generate-structured-output-from-llms-with-dottxt-outlines-in-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [LLM](/tags/llm/) / [结构化输出](/tags/%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA/) / [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Outlines](/tags/outlines/) / [Dottxt](/tags/dottxt/) / [JSON Schema](/tags/json-schema/) / [生成式 AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8F-ai/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [AWS SageMaker集成Dottxt Outlines实现LLM结构化输出]({{< relref "posts/20260225-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-4.md" >}})
- [AWS SageMaker集成Dottxt Outlines：实现LLM结构化输出]({{< relref "posts/20260224-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-1.md" >}})
- [AWS SageMaker集成Dottxt Outlines实现LLM结构化输出]({{< relref "posts/20260224-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-2.md" >}})
- [AWS SageMaker实战：用Dottxt Outlines实现LLM结构化输出]({{< relref "posts/20260225-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-12.md" >}})
- [在 Amazon SageMaker 上利用 Dottxt Outlines 实现 LLM 结构化输出]({{< relref "posts/20260225-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*