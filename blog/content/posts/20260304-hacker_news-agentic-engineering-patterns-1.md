---
title: "智能体工程模式：架构设计与核心范式"
date: 2026-03-04T10:32:30+08:00
draft: false
entry_kind: "auto"
tags: ["智能体", "Agent", "架构设计", "工程模式", "LLM", "范式", "Agentic", "系统设计"]
categories: ["AI 工程", "大模型"]
source: hacker_news
description: "随着大模型应用从简单的对话机器人向具备自主规划能力的智能体演进，传统的软件开发范式已难以应对复杂的编排需求。本文系统梳理了构建 Agentic 系统的核心工程模式，深入探讨了从单一模型调用向多组件协作架构转型的技术路径。通过解析反思、工具调用及多智能体协作等关键设计模式，读者将掌握构建高鲁棒性 AI 应用的具体方法论，"
external_url: https://simonwillison.net/guides/agentic-engineering-patterns
scenarios: ["大语言模型"]
---

# 智能体工程模式：架构设计与核心范式

---

## 基本信息

- **作者**: r4um
- **评分**: 137
- **评论数**: 36
- **链接**: [https://simonwillison.net/guides/agentic-engineering-patterns](https://simonwillison.net/guides/agentic-engineering-patterns)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47243272](https://news.ycombinator.com/item?id=47243272)

---
## 导语

随着大模型应用从简单的对话机器人向具备自主规划能力的智能体演进，传统的软件开发范式已难以应对复杂的编排需求。本文系统梳理了构建 Agentic 系统的核心工程模式，深入探讨了从单一模型调用向多组件协作架构转型的技术路径。通过解析反思、工具调用及多智能体协作等关键设计模式，读者将掌握构建高鲁棒性 AI 应用的具体方法论，从而有效解决实际业务中的复杂逻辑控制问题。

---
## 评论

**文章标题评价：Agentic Engineering Patterns**

**中心观点**
该文章主张，随着 AI 从“对话式工具”向“自主智能体”演进，软件工程的核心范式正从编写确定性代码转向编排概率性工作流。开发者需要掌握一套新的“代理工程模式”来管理循环、记忆、工具和反射，以解决非结构化问题。

**支撑理由与边界分析**

1.  **从确定性逻辑向概率性控制的转变**
    *   **理由**：传统软件依赖 `if-else` 等确定性逻辑，而 Agentic 系统依赖 LLM 的推理能力。文章指出工程师不再直接控制执行路径，而是通过设计 Prompt、Context 和 Tool 规范来引导 Agent。
    *   **边界条件**：对于高频交易、嵌入式系统或核心账务逻辑，确定性仍是首要任务。在这些场景下，引入概率性 Agent 会带来不可控的抖动或幻觉风险。Agent 模式更适合作为辅助决策层，而非核心数据处理层。

2.  **“循环”作为第一性原理的工程化**
    *   **理由**：文章强调了 Agentic Patterns 与 Chain-of-Thought（CoT）的区别在于“循环”（即 `Observe -> Thought -> Act` 的迭代）。这要求工程师具备处理状态机、长期记忆和错误恢复的能力，而非仅进行单次 Prompt 优化。
    *   **边界条件**：并非所有任务都需要循环。对于简单的信息抽取或一次性问答，引入多轮循环会增加延迟和 Token 成本，且可能导致错误累积。简单任务应坚持使用线性模式。

3.  **工具编排与系统设计的解耦**
    *   **理由**：成熟的 Agentic Engineering 将 LLM 视为通用的“推理控制器”，将具体能力（如 SQL 查询、API 调用）通过标准化接口（如 Function Calling）解耦。文章提倡的模式本质上是关于如何设计鲁棒的接口来配合模型的推理能力。
    *   **边界条件**：当工具本身极其复杂或文档缺失时，Agent 难以有效使用工具。此外，如果工具调用的副作用不可逆（如删除数据库），仅靠 Prompt 层面的约束是不够的，必须在底层沙箱层面做限制。

**深度评价**

1.  **内容深度：**
    文章触及了 AI 工程化的核心难点，跳出了“如何写好 Prompt”的初级阶段，进入了“如何设计系统架构”的层面。其论证体现在对 Agent 失败模式（如死循环、目标漂移）的探讨，表明作者具有实际落地经验。若文章能更深入探讨多 Agent 协作时的“通信开销”与“一致性保证”，其深度将更完善。

2.  **实用价值：**
    对于从 Demo 转向产品的团队，文章提供了标准化的词汇表（如 Reflection Pattern, Planning Pattern），有助于团队高效沟通。例如，在构建客户支持 Agent 时，区分“单次响应”与“带反思的迭代优化”模式，能直接影响系统设计。

3.  **创新性：**
    将传统的软件设计模式思想嫁接到 AI Agent 领域是本文的特点。虽然具体技术点（RAG, Function Calling）并非原创，但将其系统化地归纳为“工程模式”有助于建立行业参考标准。

4.  **可读性与逻辑：**
    文章遵循“问题定义 -> 核心模式 -> 边界条件”的逻辑，结构清晰。这对读者的工程背景有一定要求，需具备分布式系统或异步编程的基础知识，以理解 Agent 的并发机制。

5.  **行业影响：**
    这篇文章反映了行业从“模型中心”向“工程中心”的转移。随着模型能力提升，未来的竞争点将在于谁能建立更好的 Agentic 架构来治理模型的不可控性。这将推动 MLOps 向 LLMOps 或 AgentOps 演进。

6.  **争议点：**
    *   **单一 Agent vs 多 Agent**：文章可能倾向于复杂的单 Agent 设计，但在实际工程中，多 Agent 协作在处理复杂任务时往往表现出更高的模块化程度和可维护性，尽管这会引入通信开销。

---
## 代码示例




```python
# 示例1：工具调用模式 - 智能客服系统
from typing import TypedDict, List

class CustomerQuery(TypedDict):
    """客户查询数据结构"""
    question: str
    history: List[str]

class ToolResponse(TypedDict):
    """工具响应数据结构"""
    tool_name: str
    result: str

def customer_service_agent(query: CustomerQuery) -> str:
    """
    智能客服代理 - 自动选择工具解决客户问题
    
    解决问题：根据客户问题自动选择最合适的解决方案
    """
    # 工具箱定义
    tools = {
        "check_order": lambda order_id: f"订单{order_id}状态为已发货",
        "process_return": lambda item: f"已为您处理{item}的退货申请",
        "answer_faq": lambda topic: f"关于{topic}的常见问题解答..."
    }
    
    # 简单意图识别逻辑
    if "订单" in query["question"]:
        return tools["check_order"]("12345")
    elif "退货" in query["question"]:
        return tools["process_return"]("商品A")
    else:
        return tools["answer_faq"]("会员政策")

# 测试用例
print(customer_service_agent({"question": "我的订单什么时候发货？", "history": []}))
```




```python
# 示例2：多代理协作模式 - 内容创作团队
from dataclasses import dataclass
from typing import List

@dataclass
class Article:
    """文章数据结构"""
    title: str
    content: str
    quality_score: float

class ContentAgent:
    """内容创作代理基类"""
    def __init__(self, name: str):
        self.name = name
    
    def process(self, article: Article) -> Article:
        raise NotImplementedError

class WriterAgent(ContentAgent):
    """写作代理 - 负责生成初稿"""
    def process(self, article: Article) -> Article:
        article.content = f"关于{article.title}的初稿内容..."
        return article

class EditorAgent(ContentAgent):
    """编辑代理 - 负责优化内容"""
    def process(self, article: Article) -> Article:
        article.content = article.content.replace("初稿", "优化后的内容")
        article.quality_score = 0.8
        return article

class PublisherAgent(ContentAgent):
    """发布代理 - 负责最终审核"""
    def process(self, article: Article) -> Article:
        if article.quality_score > 0.7:
            article.content = "[已发布] " + article.content
        return article

def content_pipeline(topic: str) -> Article:
    """
    内容创作流水线 - 多代理协作完成内容生产
    
    解决问题：通过专业化代理协作完成复杂任务
    """
    article = Article(title=topic, content="", quality_score=0.0)
    agents = [WriterAgent("作家"), EditorAgent("编辑"), PublisherAgent("发布者")]
    
    for agent in agents:
        article = agent.process(article)
        print(f"{agent.name}处理后的内容: {article.content[:30]}...")
    
    return article

# 测试用例
final_article = content_pipeline("人工智能的发展趋势")
```




```python
# 示例3：反思模式 - 自我修正的代码生成器
import re

class CodeGenerator:
    """具有自我修正能力的代码生成器"""
    
    def __init__(self):
        self.max_attempts = 3
    
    def generate_code(self, requirement: str) -> str:
        """
        生成代码并进行自我修正
        
        解决问题：通过反思和修正提高生成代码的质量
        """
        for attempt in range(1, self.max_attempts + 1):
            # 生成代码（模拟）
            code = self._initial_generation(requirement)
            print(f"尝试 {attempt}: 生成代码\n{code}\n")
            
            # 反思检查
            issues = self._review_code(code)
            if not issues:
                return code
            
            # 修正代码
            code = self._fix_code(code, issues)
            print(f"发现并修正问题: {issues}\n")
        
        return code
    
    def _initial_generation(self, requirement: str) -> str:
        """初始代码生成（模拟）"""
        if "排序" in requirement:
            return "def sort(arr):\n  return sorted(arr)"  # 故意缺少类型提示
        return "# 未实现"
    
    def _review_code(self, code: str) -> List[str]:
        """代码审查（反思阶段）"""
        issues = []
        if "def sort" in code and not re.search(r"List\[", code):
            issues.append("缺少类型提示")
        if "return sorted" in code and "key" not in code:
            issues.append("可能需要自定义排序规则")
        return issues
    
    def _fix_code(self, code: str, issues: List[str]) -> str:
        """代码修正"""
        if "类型提示" in issues:
            code = code.replace("def sort(arr):", "def sort(arr: List[int]) -> List[int]:")
        if "排序规则" in issues:
            code = code.replace("return sorted(arr)", "return sorted(arr, key=lambda x: x


---
## 案例研究


### 1：Cognition AI (Devin)

 1：Cognition AI (Devin)

**背景**:
Cognition AI 致力于开发完全自主的 AI 软件工程师。为了实现这一目标，他们需要构建一个能够像人类工程师一样思考、规划并执行复杂编程任务的智能体系统，而不仅仅是代码补全工具。

**问题**:
传统的 LLM（大语言模型）在处理长周期任务时容易产生“幻觉”或丢失上下文。在面对真实的 GitHub 仓库、复杂的依赖关系以及需要多步骤调试的 Bug 修复任务时，简单的提示词工程无法保证任务完成的一致性和准确性。AI 需要能够自主决定使用何种工具（如终端、浏览器、编辑器），并根据执行结果动态调整策略。

**解决方案**:
采用了 Agentic Engineering 中的 **ReAct (Reasoning + Acting)** 模式与 **Tool Use** 架构。
Devin 被设计为一个拥有独立沙箱环境的 Agent。它不仅仅生成代码，还通过一个“规划器”将高层级指令（如“构建一个贪吃蛇游戏”）分解为数百个低层级步骤。系统通过反馈循环不断验证自己的输出：运行代码 -> 捕获错误 -> 搜索文档 -> 修改代码 -> 重新运行。这种架构赋予了 Agent 长期记忆和上下文感知能力，使其能够自主处理边缘情况。

**效果**:
Devin 成功通过了实际工程面试，并在 Upwork 上完成了真实的工作任务。在 SWE-bench 基准测试中，它解决了 13.86% 的问题（远超之前模型的 1.96%），能够端到端地完成从需求分析到代码部署的全过程，展示了 Agentic System 在处理复杂、非确定性工作流时的巨大潜力。

---



### 2：Klarna (客服自动化)

 2：Klarna (客服自动化)

**背景**:
Klarna 是一家全球领先的支付金融服务商，拥有庞大的全球客户群，每天需要处理数以十万计的客服咨询，涉及退款、退货、账户管理等重复性高但逻辑复杂的问题。

**问题**:
传统的聊天机器人依赖于僵硬的决策树，无法理解复杂的用户意图，导致转人工率极高，运营成本高昂。而直接使用通用大语言模型（LLM）又面临准确性问题，且无法直接操作后端系统来实际解决问题（例如直接执行退款操作），只能回答问题而不能“办事”。

**解决方案**:
实施了基于 **Function Calling（函数调用）** 的 Agentic 架构。
Klarna 构建了一个能够连接其内部技术栈的 AI Agent。当用户提出退款请求时，Agent 首先通过 NLP 理解意图，然后通过 API 调用查询订单状态，验证是否符合退款政策，最后直接调用后端服务执行退款操作。该 Agent 被赋予了特定的权限和工具集，能够模拟人类客服的操作流程，在安全范围内执行任务。

**效果**:
该 AI Agent 在上线后处理了三分之二的客服咨询（约 230 万次对话），直接完成了相当于 700 名全职人工客服的工作量。它不仅将客户咨询的解决时间从 11 分钟缩短至 2 分钟，而且预计每年将为公司节省约 4000 万美元的运营成本，显著提升了运营效率。

---



### 3：开源项目 AutoGPT

 3：开源项目 AutoGPT

**背景**:
AutoGPT 是早期探索“自主智能体”的标志性开源项目。其目标是验证 LLM 是否可以作为一个“大脑”，在没有任何人类微调的情况下，自主完成一系列预设的目标。

**问题**:
虽然 LLM 拥有强大的知识储备，但它们本身是被动的（输入 -> 输出）。如何让 LLM 主动设定子目标、利用互联网搜索信息、编写并保存文件以积累进度，从而实现“自我驱动”的长期任务规划，是当时面临的主要挑战。

**解决方案**:
采用了 **Recursive Task Decomposition（递归任务分解）** 模式。
AutoGPT 构建了一个循环架构：
1.  **思考**: Agent 分析当前状态与目标的差距。
2.  **规划**: 生成下一步具体的行动计划。
3.  **行动**: 调用预设的工具（如 Google Search、Python REPL、文件写入）执行计划。
4.  **观察**: 获取工具执行的反馈结果。
5.  **循环**: 将观察结果作为新的输入重新进入思考阶段。
这种模式通过将 LLM 与外部工具（文件系统、互联网）深度绑定，赋予了 Agent 记忆和执行能力。

**效果**:
AutoGPT 在 GitHub 上迅速获得超过 15 万颗星，成为了 Agentic AI 领域的基石项目。虽然受限于早期 LLM 的推理能力，它在复杂任务上的成功率有限，但它成功验证了“自主智能体”的技术范式，启发了后续 LangChain、CrewAI 等主流框架的设计，确立了现代 AI Agent 的标准工程模式。

---
## 最佳实践

## 最佳实践指南

### 实践 1：从单循环到多循环架构

**说明**:
传统的单循环架构仅包含“思考-行动”的一个步骤，容易导致模型在遇到复杂问题时陷入死循环或产生幻觉。最佳实践是采用多循环架构，将推理过程分解为“观察-思考-行动”的循环，并引入“反思”循环。这意味着在执行行动后，系统应评估结果，如果未达到预期，则重新进入观察和思考阶段，而不是盲目继续执行。

**实施步骤**:
1. 设计工作流时，明确区分规划、执行和反思三个阶段。
2. 在代码中实现状态机，确保 Agent 能够根据反馈回退到之前的状态。
3. 为反思循环设置特定的提示词，要求模型批判性地评估上一步的输出。

**注意事项**:
避免无限循环，必须设置最大迭代次数或超时机制作为硬性终止条件。

---

### 实践 2：实施工具使用验证与沙箱机制

**说明**:
当 Agent 调用外部工具（如搜索引擎、数据库查询或文件操作）时，输入参数可能包含错误或恶意指令。最佳实践要求对所有工具的输入进行严格验证，并在受限的沙箱环境中执行操作，以防止意外的系统修改或数据泄露。

**实施步骤**:
1. 为每个工具函数定义严格的 Pydantic 模型或 JSON Schema，强制类型检查。
2. 在工具执行前，增加一层验证逻辑，检查参数是否在允许的范围内（如文件路径白名单）。
3. 使用 Docker 容器或受限的运行时环境来运行 Agent 代码。

**注意事项**:
不要直接将原始用户输入传递给系统命令或敏感 API，始终进行清洗和转义。

---

### 实践 3：明确的人机协同与监督回路

**说明**:
在处理高风险或关键业务决策时，完全自主的 Agent 可能不可靠。最佳实践是设计“人在回路”的机制，允许 Agent 在执行不可逆操作或关键决策之前请求人类批准。这不仅提高了安全性，还能利用人类反馈来微调模型行为。

**实施步骤**:
1. 定义敏感操作列表（如发送邮件、删除数据、部署代码），当 Agent 计划执行这些操作时触发中断。
2. 构建一个审核界面，向人类展示 Agent 的计划、理由和预期结果。
3. 根据人类的反馈（批准、修改、拒绝），调整 Agent 的执行路径。

**注意事项**:
尽量减少对人类注意力的干扰，只在真正必要时触发审核，以免造成审核疲劳。

---

### 实践 4：结构化状态管理与记忆持久化

**说明**:
Agent 不仅仅是处理当前的输入，还需要维护上下文状态。最佳实践是将对话历史、任务目标和中间结果存储在结构化的记忆系统中，而不是全部塞入 Prompt 的上下文窗口中。这有助于降低 Token 消耗并提高检索效率。

**实施步骤**:
1. 区分短期记忆（当前对话上下文）和长期记忆（向量数据库或键值存储）。
2. 实现记忆写入和检索机制，使 Agent 能够在需要时查询过往的相关信息。
3. 维护一个全局的“任务状态”对象，记录当前步骤、已完成的子目标和待办事项。

**注意事项**:
需要定期对记忆进行摘要或清理，防止无关信息积累导致模型注意力分散。

---

### 实践 5：基于计划的执行与动态修正

**说明**:
让 Agent 直接行动往往缺乏条理。最佳实践是先让 Agent 生成一个详细的计划，然后按照计划逐步执行。如果在执行过程中发现错误或环境变化，应允许 Agent 动态修正后续计划，而不是僵化地执行原定路线。

**实施步骤**:
1. 在任务开始前，专门设置一个“规划者”角色，生成步骤列表。
2. 设置一个“执行者”角色，严格按照当前步骤行动。
3. 设置一个“监控者”角色，检查每一步的输出是否与计划相符，若不符则触发重新规划。

**注意事项**:
计划不应过于详细以至于限制了灵活性，也不应过于模糊以至于无法指导行动。

---

### 实践 6：全面的可观测性与日志记录

**说明**:
Agent 系统的行为具有概率性和非确定性，调试极其困难。最佳实践是记录从 Prompt、中间推理过程、工具调用参数到最终结果的完整链路。这对于事后分析和系统优化至关重要。

**实施步骤**:
1. 集成 OpenTelemetry 或类似的追踪框架，为每个 Agent 任务分配唯一的 Trace ID。
2. 记录每次 LLM 调用的完整 Prompt 和返回的 Token 使用情况及耗时。
3. 将工具调用的输入输出结构化存储到日志系统（如 ELK 或 Loki）中。

**注意事项**:
注意保护用户隐私，确保日志中不包含敏感的 PII（个人身份信息）数据，或对敏感字段进行脱敏处理。

---
## 学习要点

- 将复杂的任务分解为可管理的子任务，并让智能体通过迭代循环（如规划、执行、验证）来提高解决复杂问题的成功率。
- 采用反思与自我修正机制，让智能体能够审查自己的输出并利用错误反馈来优化最终结果的质量。
- 实施多智能体协作模式，通过分配不同角色（如研究员、评论员、执行者）来模拟团队工作，从而突破单一模型的能力局限。
- 利用外部工具和知识库检索（RAG）增强智能体能力，使其能够获取实时信息并执行代码等非语言类操作。
- 设计清晰且结构化的提示词，明确界定智能体的角色、目标和上下文，以减少幻觉并提高输出的稳定性。
- 引入人类监督和反馈回路，在关键决策点进行人工干预，以确保系统行为的可控性和安全性。
- 建立完善的评估与测试体系，不仅检查最终答案，还要监控智能体的推理过程和中间步骤的有效性。

---
## 常见问题


### 1: 什么是 Agentic Engineering Patterns（智能体工程模式），它与传统的软件开发模式有何不同？

1: 什么是 Agentic Engineering Patterns（智能体工程模式），它与传统的软件开发模式有何不同？

**A**: Agentic Engineering Patterns 是指在构建大语言模型（LLM）驱动的智能体时所采用的一套架构设计和工程实践模式。与传统的软件开发不同，传统模式主要基于确定性的逻辑（如 `if-else`）和固定的 API 调用。而 Agentic Engineering 的核心在于处理“概率性”的输出。智能体通常具备规划、记忆、工具使用和反思的能力。工程模式关注的核心问题包括：如何将复杂的任务拆解、如何让模型自主选择工具调用、如何设计多智能体协作机制以及如何构建有效的反馈循环来修正模型的错误，从而实现从单纯的“聊天机器人”向能够解决复杂问题的“智能体”转变。

---



### 2: 在构建 Agentic 系统时，最核心的架构模式有哪些？

2: 在构建 Agentic 系统时，最核心的架构模式有哪些？

**A**: 目前业界公认的几种核心架构模式包括：

1.  **ReAct 模式**：这是最基础的模式，即推理+行动。模型生成推理过程，并据此执行外部工具调用，然后观察结果再进行下一步推理。
2.  **规划与执行**：将任务分为两个阶段，先由一个 Planner 生成详细的任务列表，再由一个 Executor 逐步执行。
3.  **反思与自我修正**：在任务完成后或阶段性节点，引入一个 Critic 角色来评估结果，如果不符合要求则返回重试。
4.  **多智能体协作**：设置多个具有不同角色（如编码员、审查员、产品经理）的智能体，通过对话或工作流协同完成复杂的单一模型难以胜任的任务。
5.  **工作流编排**：使用代码（如 LangChain 或 LangGraph）将模型的调用逻辑固化为有向无环图（DAG），以获得更高的可控性和稳定性。

---



### 3: 既然 LLM 很强大，为什么还需要“工程模式”？直接用 Prompt 解决不行吗？

3: 既然 LLM 很强大，为什么还需要“工程模式”？直接用 Prompt 解决不行吗？

**A**: 虽然 Prompt Engineering（提示工程）很重要，但它难以解决所有问题，特别是在生产环境中。主要局限性包括：

1.  **上下文限制**：复杂任务需要的指令和数据可能超过模型的上下文窗口。
2.  **可靠性问题**：仅靠 Prompt 难以保证模型 100% 按照预期格式输出或遵循复杂逻辑，容易出现“幻觉”或逻辑跳跃。
3.  **状态管理**：Prompt 是无状态的，而 Agentic 系统通常需要记忆历史交互、中间结果和长期记忆。
4.  **工具集成**：Prompt 难以处理复杂的 API 调用逻辑、错误重试机制和流式响应。
工程模式通过引入控制逻辑、记忆组件和工具接口，将模型从单纯的“文本生成器”转变为系统的“控制器”，从而解决上述问题。

---



### 4: 什么是“工具使用”在 Agentic Engineering 中的角色，如何实现它？

4: 什么是“工具使用”在 Agentic Engineering 中的角色，如何实现它？

**A**: “工具使用”是智能体连接现实世界的关键。它允许 LLM 在生成文本的过程中，输出特定的指令来调用外部函数（如搜索引擎、数据库查询、代码执行器等），而不是直接生成回复。

实现方式通常包括：
1.  **工具定义**：向模型注册可用的函数，包括函数名称、描述和参数结构（通常以 JSON Schema 格式）。
2.  **工具选择**：模型根据用户的 Query，判断是否需要使用工具，以及使用哪个工具，并生成相应的参数。
3.  **代码拦截与执行**：应用层代码拦截模型的输出，识别出工具调用请求，执行实际的函数代码，并将结果返回给模型。
4.  **结果总结**：模型根据工具返回的结果，生成最终的自然语言回复给用户。
这种机制极大地扩展了模型的能力边界，使其能够处理实时数据和私有数据。

---



### 5: 在多智能体系统中，如何避免“混乱”或“死循环”？

5: 在多智能体系统中，如何避免“混乱”或“死循环”？

**A**: 多智能体系统虽然强大，但容易陷入无休止的讨论或逻辑死循环。常见的控制策略包括：

1.  **有向图控制**：使用如 LangGraph 等框架，将智能体之间的交互定义为状态图。明确指定状态转移的条件，例如只有当“审查员”批准后，流程才能进入下一步，否则强制结束或重试。
2.  **最大步数限制**：在运行时设置最大迭代次数或 Token 消耗上限，一旦达到阈值立即终止并返回当前最佳结果或错误信息。
3.  **人类介入**：在关键决策点设置人工确认机制，由人来打破僵局或纠正方向。
4.  **角色隔离**：确保每个 Agent 的 Prompt 足够明确，限制其职责范围，防止角色边界模糊导致的指令混乱。

---



### 6: 评估 Agentic 系统的性能有哪些挑战？应该如何解决？

6: 评估 Agentic 系统的性能有哪些挑战？应该如何解决？

**A**: 评估 Agentic 系统比评估传统的 NLP 任务（如分类）要困难得多，因为输出是开放式的且涉及多步推理。

主要挑战和解决方案包括：
1.  **结果不确定性**：同样的输入可能导致不同的执行路径。解决方法是进行多次

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在设计一个简单的 Agent 工作流时，你需要在执行外部工具调用（如搜索或数据库查询）之前，先验证用户的输入参数是否符合基本要求（例如，查询字符串不能为空，日期格式必须正确）。请设计一个“输入验证与路由”的伪代码逻辑，确保只有参数合法时才调用工具，否则直接返回友好的错误提示。

### 提示**: 考虑使用“守卫”模式。不要将验证逻辑写在业务逻辑内部，而是将其作为 Agent 决策链中的一个独立节点或前置条件检查。

### 

---
## 引用

- **原文链接**: [https://simonwillison.net/guides/agentic-engineering-patterns](https://simonwillison.net/guides/agentic-engineering-patterns)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47243272](https://news.ycombinator.com/item?id=47243272)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/) / [工程模式](/tags/%E5%B7%A5%E7%A8%8B%E6%A8%A1%E5%BC%8F/) / [LLM](/tags/llm/) / [范式](/tags/%E8%8C%83%E5%BC%8F/) / [Agentic](/tags/agentic/) / [系统设计](/tags/%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [人人都在构建异步智能体 但鲜有人能定义其概念]({{< relref "posts/20260209-hacker_news-everyones-building-async-agents-but-almost-no-one--14.md" >}})
- [LLM智能体新增Claws层：强化外部工具调用与任务执行能力]({{< relref "posts/20260221-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-13.md" >}})
- [LLM智能体新增Claws层以增强功能]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-10.md" >}})
- [Claws 成为 LLM 智能体之上的新架构层]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*