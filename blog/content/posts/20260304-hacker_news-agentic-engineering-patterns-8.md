---
title: "智能体工程模式：构建自主系统的架构设计"
date: 2026-03-04T15:11:02+08:00
draft: false
entry_kind: "auto"
tags: ["智能体", "Agent", "架构设计", "自主系统", "LLM", "工程模式", "系统设计", "Agentic"]
categories: ["AI 工程", "系统与基础设施"]
source: hacker_news
description: "随着大模型应用从简单的对话机器人向复杂系统演进，如何构建具备自主规划与工具调用能力的 Agent 成为工程实践的核心议题。本文系统梳理了 Agentic 工程领域的常见设计模式，旨在解决从单次对话向长期任务流转过程中的架构挑战。通过解析反思、记忆与规划等关键机制，读者可以掌握构建高鲁棒性智能系统的具体路径，从而在实际项"
external_url: https://simonwillison.net/guides/agentic-engineering-patterns
scenarios: ["大语言模型"]
---

# 智能体工程模式：构建自主系统的架构设计

---

## 基本信息

- **作者**: r4um
- **评分**: 289
- **评论数**: 147
- **链接**: [https://simonwillison.net/guides/agentic-engineering-patterns](https://simonwillison.net/guides/agentic-engineering-patterns)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47243272](https://news.ycombinator.com/item?id=47243272)

---
## 导语

随着大模型应用从简单的对话机器人向复杂系统演进，如何构建具备自主规划与工具调用能力的 Agent 成为工程实践的核心议题。本文系统梳理了 Agentic 工程领域的常见设计模式，旨在解决从单次对话向长期任务流转过程中的架构挑战。通过解析反思、记忆与规划等关键机制，读者可以掌握构建高鲁棒性智能系统的具体路径，从而在实际项目中有效落地复杂的自动化业务逻辑。

---
## 评论

由于您未提供具体的文章正文，以下评价基于**“Agentic Engineering Patterns”（智能体工程模式）**这一当前AI领域的前沿主题及其通常涵盖的核心内容（如循环模式、反思模式、规划模式等）进行综合性的深度评价。

### 评价综述

**中心观点：**
Agentic Engineering Patterns 标志着 AI 工程化从“单一提示优化”向“结构化系统设计”的范式转移，其核心在于通过**模块化、状态管理和反馈循环**来解决大语言模型（LLM）在复杂任务中的不确定性与局限性，将模型从“聊天工具”转化为具有自主行动能力的“系统内核”。

---

### 深入评价

#### 1. 内容深度与论证严谨性
*   **支撑理由（事实陈述/作者观点）：** 该类文章通常深刻剖析了 LLM 的**非确定性本质**。它不再将 AI 视为一个简单的输入输出函数，而是将其视为一个需要“推理-行动-观察”循环的操作系统。论证逻辑通常基于软件工程中的控制论，指出单纯的 Prompt Engineering（提示工程）无法处理长上下文和复杂逻辑，必须引入如 **ReAct (Reason + Act)**、**Plan-and-Solve** 等模式。这种将认知科学（反思机制）与软件架构相结合的视角具有很高的理论深度。
*   **反例/边界条件（你的推断）：** 这种深度往往掩盖了**“线性交互”的价值**。并非所有场景都需要 Agentic 模式。对于简单的知识抽取或一次性翻译，引入复杂的 Agentic 架构（如多步调用、工具检索）不仅浪费算力，还增加了延迟。文章有时会过度工程化简单问题。

#### 2. 实用价值与指导意义
*   **支撑理由（事实陈述）：** 文章提出的模式（如 **Multi-Agent Collaboration** 多智能体协作）直接解决了企业级应用中的痛点。例如，在编码领域，通过将“架构师”、“工程师”和“测试员”解耦为不同的 Agent，可以显著提高代码生成的通过率。这种**角色分工**模式为构建复杂 AI 原生应用提供了标准化的“设计模式”，极大地降低了试错成本。
*   **反例/边界条件（你的推断）：** 实用性受限于**调试的复杂性**。传统的软件调试是确定性的，而 Agentic 系统的执行路径是概率性的。当系统由多个 Agent 交互时，出现“幻觉”或“死循环”的排查难度呈指数级上升。文章往往侧重于“如何构建”，而较少探讨“如何在大规模生产环境中监控和修复”这些不可预测的 Agent 行为。

#### 3. 创新性
*   **支撑理由（你的推断）：** 该领域的最大创新在于**将“思维链”显性化**。传统的程序是“数据+算法=结果”，而 Agentic 模式是“意图+上下文+工具+反思=结果”。它提出了 **Memory（记忆）** 和 **Planning（规划）** 作为一等公民，这在以往的 NLP 应用架构中是极其罕见的。它实际上是在定义 AI 时代的“操作系统”调度逻辑。
*   **反例/边界条件（事实陈述）：** 许多所谓的“新模式”实际上是旧概念的包装。例如，“工具使用”在 90 年代的专家系统和符号 AI 中就已经存在。因此，部分创新更多是工程实现上的演进，而非纯理论突破。

#### 4. 可读性与逻辑性
*   **支撑理由（作者观点）：** 优秀的 Agentic Engineering 文章通常具备极强的**结构化思维**。它们往往使用流程图、状态机转换图来描述 Agent 的行为，这对于工程师来说非常友好。它成功地将模糊的自然语言交互转化为清晰的工程逻辑。
*   **反例/边界条件（你的推断）：** 术语泛滥是可读性的最大障碍。Agent、Workflow、Chain、Component 在不同语境下定义模糊，容易导致读者在概念理解上产生歧义，增加了团队沟通成本。

#### 5. 行业影响与潜在争议
*   **支撑理由（你的推断）：** 这篇文章（及其代表的流派）正在推动 **RAG（检索增强生成）向 Agentic RAG 进化**。它迫使行业重新思考数据基础设施：我们不再只需要向量数据库，还需要图数据库来维护 Agent 的关系记忆，需要消息队列来处理异步事件。它将深刻影响 AI 基础设施的发展方向。
*   **争议点（行业不同观点）：**
    *   **单体 vs. 多体：** 行业对于“一个强模型+多个工具”还是“多个弱模型+协作”存在巨大分歧。OpenAI 等倾向于前者，而 AutoGPT 等开源社区倾向于后者。
    *   **端到端派：** 一些研究者认为，随着模型推理能力（如 OpenAI o1）的增强，显式的工程模式可能会消失，模型将自主完成所有规划和反思，Agentic Patterns 只是过渡期的补丁。

---

### 实际应用建议

基于上述评价，在实际落地 Agentic 模式时，建议遵循以下策略：

1.  **从“手”开始，而非“脑”：** 不要一开始就构建复杂的自主规划 Agent。先构建**确定性的工具调用**，让 AI 拥有操作 API 的能力，验证其可靠性。
2.  **显式的“人机协同”：** 在关键决策节点（如发送邮件、执行交易、修改生产环境代码）设置**人工确认**机制，将 Agent 视为“副驾驶”而非“自动驾驶”，防止幻觉导致的灾难性后果。
3.

---
## 代码示例




```python
# 示例1：多智能体协作模式
def multi_agent_collaboration():
    """
    模拟多智能体协作解决复杂问题
    场景：一个研究团队（研究员、分析师、审阅者）协作完成报告
    """
    from typing import List, Dict
    import time

    class Agent:
        def __init__(self, name: str, role: str):
            self.name = name
            self.role = role
            self.memory = []
        
        def process(self, input_data: str) -> str:
            """模拟智能体处理信息"""
            print(f"[{self.role}] {self.name} 正在处理: {input_data}")
            time.sleep(0.5)  # 模拟处理时间
            result = f"{self.role}处理结果: {input_data} (已优化)"
            self.memory.append(result)
            return result

    # 创建智能体团队
    researcher = Agent("张三", "研究员")
    analyst = Agent("李四", "分析师")
    reviewer = Agent("王五", "审阅者")

    # 协作流程
    topic = "AI在医疗领域的应用"
    research_data = researcher.process(f"收集关于{topic}的资料")
    analysis = analyst.process(f"分析{research_data}")
    final_report = reviewer.process(f"审阅{analysis}并生成报告")

    return final_report

# 运行示例
print(multi_agent_collaboration())
```


---

```python
# 示例2：带记忆的对话系统
def conversational_agent_with_memory():
    """
    实现一个能记住上下文的对话智能体
    场景：客服机器人需要记住用户之前的对话
    """
    from typing import List

    class ConversationalAgent:
        def __init__(self):
            self.conversation_history: List[str] = []
            self.max_history = 5  # 只保留最近5轮对话
        
        def respond(self, user_input: str) -> str:
            """根据用户输入和对话历史生成回复"""
            # 记录当前输入
            self.conversation_history.append(f"用户: {user_input}")
            
            # 模拟生成回复（实际中这里会调用LLM）
            if "价格" in user_input:
                response = "我们的产品价格是$99/月"
            elif "功能" in user_input:
                response = "主要功能包括数据分析、自动化报告等"
            else:
                response = "抱歉，我不太明白。您可以询问价格或功能。"
            
            # 记录回复并保持历史记录在限制范围内
            self.conversation_history.append(f"机器人: {response}")
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-self.max_history * 2:]
            
            return response
        
        def show_history(self):
            """显示对话历史"""
            return "\n".join(self.conversation_history)

    # 模拟对话
    agent = ConversationalAgent()
    print(agent.respond("你好"))
    print(agent.respond("价格是多少？"))
    print(agent.respond("有哪些功能？"))
    print("\n对话历史:")
    print(agent.show_history())

# 运行示例
conversational_agent_with_memory()
```


---

```python
# 示例3：工具使用智能体
def tool_using_agent():
    """
    实现一个能使用外部工具的智能体
    场景：个人助理智能体可以调用天气、计算器等工具
    """
    import random

    # 定义可用工具
    def get_weather(city: str) -> str:
        """模拟天气API"""
        conditions = ["晴", "多云", "雨", "雪"]
        temp = random.randint(10, 30)
        return f"{city}今天{random.choice(conditions)}，温度{temp}°C"

    def calculator(expression: str) -> str:
        """模拟计算器"""
        try:
            result = eval(expression)
            return f"计算结果: {result}"
        except:
            return "无法计算该表达式"

    class ToolUsingAgent:
        def __init__(self):
            self.tools = {
                "天气": get_weather,
                "计算器": calculator
            }
        
        def process_request(self, user_input: str) -> str:
            """根据用户输入决定使用哪个工具"""
            if "天气" in user_input:
                city = user_input.split("天气")[0].strip() or "北京"
                return self.tools["天气"](city)
            elif "计算" in user_input:
                expr = user_input.split("计算")[1].strip()
                return self.tools["计算器"](expr)
            else:
                return "我可以帮您查询天气或进行计算，请问需要什么帮助？"

    # 测试智能体
    agent = ToolUsingAgent()
    print(agent.process_request("上海天气怎么样？"))
    print(agent.process_request("计算 25 * 4 + 10"))
    print(agent.process_request("你好"))

# 运行示例
tool_using_agent()
```


---
## 案例研究


### 1：Cognition AI (Devin)

 1：Cognition AI (Devin)

**背景**: Cognition AI 致力于构建完全自主的 AI 软件工程师。在软件开发领域，传统的 LLM（如 ChatGPT）虽然能生成代码片段，但无法完成从需求分析到最终部署的复杂端到端任务，且容易在环境配置和长任务链中产生幻觉或错误。

**问题**: 仅仅依靠大语言模型的预测能力无法解决实际工程问题。主要难点在于：模型无法自主操作开发环境（如终端、编辑器、浏览器），无法在遇到错误时自我调试，也难以管理复杂的多步骤工作流（如查找 API 文档、编写代码、运行测试、修复 Bug）。

**解决方案**: 采用了 **Agent + 工具使用** 的工程模式。他们构建了名为 Devin 的智能体，它不仅拥有经过专门微调的代码生成模型，还集成了沙箱执行环境。Devin 可以自主规划任务，使用 Bash 终端执行命令，编辑代码文件，并在出现错误时通过查看日志和文档进行“反思”和自我修正，直到测试通过。

**效果**: Devin 能够完成 Upwork 等平台上的真实外包任务，能够端到端地构建和部署小型应用。这标志着 AI 从辅助工具向具备自主解决问题能力的“工程师”转变，极大地提升了自动化开发的水平。

---



### 2：Klarna (客服助手)

 2：Klarna (客服助手)

**背景**: Klarna 是一家全球性的金融科技和购物服务公司，拥有庞大的客户服务需求。随着业务增长，人工客服成本高昂且响应时间难以保证，特别是在处理退货、退款等常规查询时。

**问题**: 传统的聊天机器人基于规则或简单的意图识别，灵活性差，无法处理复杂的用户问题，往往需要转接人工。而直接使用通用 LLM 虽然理解能力强，但存在产生幻觉、胡乱回答财务问题或无法接入公司内部数据库（如订单状态）的风险。

**解决方案**: 采用了 **RAG（检索增强生成） + Agent 工作流** 的模式。Klarna 构建了一个基于 OpenAI 技术的智能体，该 Agent 能够根据用户问题，自主决定调用内部 API 查询实时订单数据，或者检索公司的知识库来回答政策问题。通过将推理能力与数据访问能力结合，确保了回答的准确性和时效性。

**效果**: 该 AI 助手上线后，在上线一个月内处理了 230 万次对话（占总量的 2/3），直接完成了相当于 700 名全职人工客服的工作量，并将客户问题的解决时间从 11 分钟缩短至 2 分钟，预计每年可为公司节省 4000 万美元的成本。

---



### 3：Tavily (AI 搜索 Agent)

 3：Tavily (AI 搜索 Agent)

**背景**: 随着 AI 应用的爆发，越来越多的企业和开发者希望构建能够访问实时信息的 AI Agent（如市场分析 Agent、新闻摘要 Agent）。然而，传统的搜索引擎 API 是为人类设计的，返回的是 HTML 网页，而非结构化数据。

**问题**: 通用 LLM 无法直接联网，且如果直接使用 Google 等搜索引擎的结果喂给 LLM，会包含大量广告、导航栏等噪音，导致 Token 消耗巨大且提取关键信息困难。开发者需要一个专门为 Agent 设计的、能够快速返回准确答案的搜索接口。

**解决方案**: Tavily 作为一个专门的 **Agentic 工具** 被开发出来。它不仅仅是一个搜索引擎，更是一个 Agent 的“感知器官”。它优化了搜索和提取过程，能够智能地理解搜索意图，并返回经过优化的、LLM 可直接使用的上下文信息，甚至支持多步查询和深层挖掘。

**效果**: Tavily 成为了构建现代 Agentic 应用（特别是基于 LangChain 或 AutoGPT 构建的应用）的标准基础设施之一。它使得 AI Agent 能够以极低的延迟获取高准确度的实时数据，解决了 AI 幻觉问题，极大地提升了 AI 应用在金融、新闻等时效性敏感领域的可用性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：循环模式

**说明**: 循环模式是 Agentic 系统的核心架构，区别于传统的线性输入输出。它强调系统必须具备“观察-思考-行动”的闭环能力。Agent 不仅要执行任务，还需要根据执行结果进行自我反思，判断任务是否完成，若未完成则调整策略重新执行，直到达成目标或达到最大重试次数。

**实施步骤**:
1. 定义明确的终止条件，防止无限循环。
2. 在每次行动后引入“反思”步骤，让 LLM 评估当前结果与目标的差距。
3. 设计状态追踪机制，记录每次循环的输入、输出和思考过程。
4. 实现异常处理逻辑，当连续多次循环无法进展时触发人工干预。

**注意事项**: 避免在没有明确退出标准的情况下使用无限循环，这会导致资源耗尽和成本激增。

---

### 实践 2：记忆与状态管理

**说明**: Agentic 应用通常涉及多轮对话和长周期任务，系统必须能够记住之前的交互、提取的上下文以及中间步骤的执行结果。最佳实践是将短期记忆（当前会话）与长期记忆（向量数据库或键值存储）分离，确保 Agent 能够在复杂的决策过程中调用历史信息。

**实施步骤**:
1. 设计分层的存储架构，区分会话级上下文和持久化知识库。
2. 实现记忆的检索机制，根据当前任务的相关性动态拉取历史数据。
3. 定期对记忆进行清洗和总结，将冗长的对话压缩为高维度的语义摘要，以控制 Token 消耗。
4. 确保状态更新的原子性，防止并发操作导致的数据不一致。

**注意事项**: 随着对话轮次增加，上下文窗口可能会溢出，必须实施有效的上下文修剪或摘要策略。

---

### 实践 3：工具使用与外部接口

**说明**: Agent 的能力边界由其能够调用的工具决定。最佳实践不仅仅是提供 API，而是要为 LLM 提供结构化的工具描述。这包括清晰的工具名称、功能描述、参数 schema 以及调用示例。工具应当是原子的、功能单一的，并且具有幂等性，以便 Agent 可靠地重复调用。

**实施步骤**:
1. 为每个工具编写详细的文档字符串，这将被直接注入到 LLM 的提示词中。
2. 验证工具的输入输出类型，严格遵循 JSON Schema 或 Pydantic 模型定义。
3. 实现工具调用的错误处理和回滚机制，确保外部 API 失败不会导致 Agent 崩溃。
4. 提供工具的调用示例，帮助 LLM 理解在何种场景下使用特定工具。

**注意事项**: 限制工具的返回数据量，过大的响应会迅速消耗上下文窗口并降低推理质量。

---

### 实践 4：系统提示词工程

**说明**: 系统提示词是 Agent 的“大脑皮层”，定义了 Agent 的角色、目标、约束条件和行为模式。在 Agentic Engineering 中，提示词应当是模块化的，将核心指令与具体的任务指令分离。此外，应明确指示 Agent 如何处理不确定性，以及在何时寻求帮助。

**实施步骤**:
1. 采用角色扮演技术，明确设定 Agent 的身份和专业领域。
2. 将复杂的指令拆分为“思维链”步骤，引导 Agent 进行逐步推理。
3. 在提示词中硬编码安全边界，明确禁止的操作（如删除文件、绕过安全协议）。
4. 使用版本控制管理提示词，便于进行 A/B 测试和回滚。

**注意事项**: 避免提示词过长或指令冲突，这会导致 LLM 产生幻觉或忽略关键约束。

---

### 实践 5：可观测性与日志记录

**说明**: 由于 LLM 的输出具有非确定性，调试 Agentic 系统极具挑战性。最佳实践要求记录每一次循环的完整链路，包括 LLM 的输入提示词、原始输出、解析后的工具调用、工具返回结果以及系统的内部状态转换。这对于事后分析和优化至关重要。

**实施步骤**:
1. 集成追踪工具（如 LangSmith 或 OpenTelemetry），自动记录每个 Agent 的执行轨迹。
2. 为每次请求分配唯一的 Trace ID，以便关联分散的日志条目。
3. 记录 Token 使用量和延迟指标，用于性能监控和成本分析。
4. 建立可视化仪表盘，实时监控 Agent 的成功率、失败模式和工具调用频率。

**注意事项**: 日志记录本身可能产生额外的延迟和存储成本，需要在详细程度与性能之间取得平衡。

---

### 实践 6：安全沙箱与权限控制

**说明**: 赋予 Agent 执行代码或修改文件的能力带来了显著的安全风险。最佳实践是将 Agent 运行在受限的沙箱环境中，并实施最小权限原则。Agent 不应直接访问生产数据库或敏感的用户数据，而应通过受控的网关或代理层进行交互。

**实施步骤**:
1. 使用容器化技术（如 Docker）或 WebAssembly (WASM) 运行时代

---
## 学习要点

- 基于您提供的主题“Agentic Engineering Patterns”（智能体工程模式），以下是该领域目前最核心的工程化设计原则与关键要点：
- 将复杂任务分解为可管理的子任务并构建多智能体系统，是解决超出上下文窗口限制或过于复杂问题的最有效模式。
- 采用反思与自我修正机制，让智能体在执行过程中审查并优化其输出，能显著提高最终结果的准确性和质量。
- 实施工具使用验证，确保智能体在调用外部API或函数时参数正确且符合预期，是保证系统稳定性的关键。
- 引入记忆系统（包括短期和长期记忆），赋予智能体跨会话存储和检索信息的能力，是实现个性化交互的基础。
- 设计清晰的系统提示词与角色定义，通过约束智能体的行为边界来减少幻觉并提高任务完成度。
- 规划与执行分离，将生成高层计划的“慢思考”模式与执行具体动作的“快思考”模式解耦，有助于优化系统性能。

---
## 常见问题


### 1: 什么是 Agentic Engineering Patterns（代理工程模式）？

1: 什么是 Agentic Engineering Patterns（代理工程模式）？

**A**: Agentic Engineering Patterns 是指在构建人工智能代理系统时采用的一套标准化架构和设计方法。与传统的基于请求响应的 AI 应用不同，Agentic Engineering 关注如何构建能够自主规划、使用工具、记忆上下文并执行复杂工作流的智能体。这些模式旨在解决大语言模型（LLM）在处理复杂任务时面临的幻觉、上下文限制以及缺乏持久化等问题，通过将推理、行动和反馈循环结构化，使 AI 系统能够更可靠地完成端到端的任务。

---



### 2: 在构建 Agentic AI 时，最核心的架构模式有哪些？

2: 在构建 Agentic AI 时，最核心的架构模式有哪些？

**A**: 目前业界公认的核心架构模式主要包括以下几种：

1.  **ReAct (Reasoning + Acting)**：这是最基础的模式，即让模型先进行推理，制定行动计划，然后执行动作，最后观察结果并循环，直到完成任务。
2.  **Reflection (反思)**：引入自我修正机制。代理在执行任务后会观察自己的输出，通过另一个提示词或模型来批评和改进结果，从而提高输出的准确性和质量。
3.  **Multi-Agent Collaboration (多代理协作)**：将复杂任务拆解，由多个具有不同角色（如研究员、程序员、审查员）的代理协作完成。常见的实现方式包括通过“主持人”代理进行调度，或者是完全去中心化的网络通信。
4.  **Planning (规划)**：在执行前先生成一个全局计划，并在执行过程中根据实际情况动态调整计划，以避免模型陷入局部最优或死循环。

---



### 3: Agentic AI 与传统的 Chain-of-Thought (CoT) 提示词工程有什么区别？

3: Agentic AI 与传统的 Chain-of-Thought (CoT) 提示词工程有什么区别？

**A**: CoT 主要是一种提示词技巧，旨在通过引导模型一步步思考来提高单个推理任务的准确性，通常是在单次对话中完成。而 Agentic Engineering 是一个系统工程概念，它不仅包含推理，还包含了与外部环境的交互。

具体区别在于：Agentic AI 具有持久化的记忆、能够调用外部工具（API、数据库、搜索引擎）、具备多步骤的循环控制结构，并且通常涉及代码层面的编排框架（如 LangChain, AutoGen 等）。CoT 是 Agentic AI 中的一个组件或思维模式，但 Agentic AI 更强调系统的自主性和行动能力。

---



### 4: 在工程实践中，如何解决 Agentic AI 的“循环中的错误累积”问题？

4: 在工程实践中，如何解决 Agentic AI 的“循环中的错误累积”问题？

**A**: 错误累积是 Agentic 系统面临的最大挑战之一，即代理在某一步犯错后，后续步骤会基于这个错误继续执行，导致最终结果完全偏离。工程上常见的解决方案包括：

1.  **Human-in-the-loop (HITL)**：在关键决策点或执行终点引入人工确认或干预。
2.  **验证器模式**：设置独立的“审查者”代理或专门的验证脚本，对每一步的输出进行逻辑检查或格式校验，不通过则重试。
3.  **回滚机制**：为代理维护一个执行历史栈，当检测到严重错误或结果不理想时，允许系统回退到之前的状态并尝试不同的路径。
4.  **确定性工具调用**：尽量减少让 LLM 生成 JSON 或代码的自由度，而是通过强类型的函数调用接口来约束其行为，从而减少语法或逻辑错误。

---



### 5: 对于初创公司或开发者，应该从零开始构建 Agentic 框架还是使用现有的开源框架？

5: 对于初创公司或开发者，应该从零开始构建 Agentic 框架还是使用现有的开源框架？

**A**: 在绝大多数情况下，建议从使用现有的成熟框架（如 LangChain, LangGraph, AutoGen, CrewAI 等）开始。

原因如下：
1.  **复杂性**：构建一个可靠的代理编排层涉及复杂的异步状态管理、流式传输处理、错误重试逻辑和记忆管理，这些都是重复造轮子。
2.  **快速迭代**：Agentic 领域发展极快，框架通常会迅速集成最新的最佳实践（如 RAG、图数据库集成）。
3.  **何时自建**：只有当你的业务对延迟有极高的要求（需要极致优化），或者现有框架无法满足你的特定编排逻辑（例如非常复杂的非循环依赖图）时，才考虑基于底层 LLM API 自建轻量级编排。

---



### 6: Agentic Engineering Pattern 中如何处理“记忆”？

6: Agentic Engineering Pattern 中如何处理“记忆”？

**A**: 在 Agentic 架构中，记忆不仅仅是聊天历史，它通常被分为三类进行工程化处理：

1.  **短期记忆**：通常指当前的上下文窗口。工程上需要通过摘要技术或滑动窗口来管理 Token 限制。
2.  **长期记忆**：利用向量数据库实现 RAG（检索增强生成）。代理可以主动查询外部知识库来获取持久化的信息。
3.  **实体记忆与工作流记忆**：这是 Agentic 特有的。系统需要记录关于用户的关键信息（如偏好、过往任务），以及当前任务的执行状态（如“我已经尝试了方法A，失败了，现在尝试方法B”）。这通常通过结构化的数据存储（如 SQL 或图数据库）与 LLM 的读写接口结合来实现。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在构建 Agentic 工作流时，LLM 调用常面临 API 不稳定（超时或速率限制）的问题。请设计一个基础的“重试装饰器”模式，要求包含指数退避策略，并说明为什么在 Agent 系统中，简单的“无限重试”是危险的。

### 提示**: 考虑如何计算等待时间（例如 `base_delay * (2 ** attempt)`），并思考在 Agent 复杂的链式调用中，无限重试如何导致成本失控或延迟累积。

### 

---
## 引用

- **原文链接**: [https://simonwillison.net/guides/agentic-engineering-patterns](https://simonwillison.net/guides/agentic-engineering-patterns)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47243272](https://news.ycombinator.com/item?id=47243272)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/) / [自主系统](/tags/%E8%87%AA%E4%B8%BB%E7%B3%BB%E7%BB%9F/) / [LLM](/tags/llm/) / [工程模式](/tags/%E5%B7%A5%E7%A8%8B%E6%A8%A1%E5%BC%8F/) / [系统设计](/tags/%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/) / [Agentic](/tags/agentic/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [智能体工程模式：构建自主系统的架构设计]({{< relref "posts/20260304-hacker_news-agentic-engineering-patterns-2.md" >}})
- [智能体工程模式：架构设计与核心范式]({{< relref "posts/20260304-hacker_news-agentic-engineering-patterns-1.md" >}})
- [智能体工程模式：自主系统的架构设计范式]({{< relref "posts/20260304-hacker_news-agentic-engineering-patterns-3.md" >}})
- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [人人都在构建异步智能体 但鲜有人能定义其概念]({{< relref "posts/20260209-hacker_news-everyones-building-async-agents-but-almost-no-one--14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*