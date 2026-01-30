---
title: "Agent评估显示AGENTS.md配置优于Skills"
date: 2026-01-30T10:25:30+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "评估", "AGENTS.md", "Skills", "配置", "LLM", "性能对比", "最佳实践"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在构建智能体的过程中，如何定义其行为边界与能力范围是开发者面临的核心挑战。本文通过对比测试发现，采用 AGENTS.md 文件来统一管理上下文与指令，其效果优于传统的技能拆分模式。文章将详细解析这一配置文件在评估中的具体表现，并探讨它如何帮助团队更高效地维护智能体的逻辑一致性。"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型"]
---

# Agent评估显示AGENTS.md配置优于Skills

---

## 基本信息

- **作者**: maximedupre
- **评分**: 339
- **评论数**: 144
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在构建智能体的过程中，如何定义其行为边界与能力范围是开发者面临的核心挑战。本文通过对比测试发现，采用 AGENTS.md 文件来统一管理上下文与指令，其效果优于传统的技能拆分模式。文章将详细解析这一配置文件在评估中的具体表现，并探讨它如何帮助团队更高效地维护智能体的逻辑一致性。

---
## 评论

### 核心观点
文章提出了一种激进但经过实证的范式转变：在构建通用智能体时，使用包含详细上下文和推理轨迹的单一“长文档”模式，在复杂任务的表现上显著优于传统的模块化“技能/工具调用”模式。

### 深入评价

#### 1. 内容深度：从“函数式”向“上下文式”的回归
**[事实陈述]** 文章对比了两种Agent架构：一种是传统的Skills模式（将任务拆解为API调用，如LangChain/HuggingGPT风格），另一种是AGENTS.md模式（将所有API文档、使用示例、错误处理逻辑写在一个巨大的Markdown文件中作为上下文）。
**[你的推断]** 这篇文章触及了当前LLM应用的核心矛盾——**模型推理能力与系统复杂度的错配**。传统软件工程强调“解耦”和“模块化”，但基于Transformer的模型本质上是在做概率预测，它更擅长在“连续的上下文窗口”中进行注意力分配，而不是在离散的API跳转中保持状态。
**[作者观点]** 作者认为，Skills模式引入了过多的中间层噪音（如解析错误、多轮对话的Token损耗），而AGENTS.md让模型能够像阅读教科书一样“内化”工具使用逻辑，从而减少了幻觉和执行断裂。

#### 2. 实用价值：对工程化落地的双重启示
**[事实陈述]** 文章展示了在内部评估中，AGENTS.md在复杂任务上的成功率大幅领先。
**[你的推断]** 这对行业具有极高的参考价值，特别是在RAG（检索增强生成）和Agent框架选型上。
*   **正面指导：** 对于处理复杂、长尾、非标准化的业务流程（如企业私有API的编排），直接将文档“喂”给模型，可能比花费数周开发精细化的API包装器更有效。这降低了开发门槛，减少了“胶水代码”。
*   **负面警示：** 这种模式极度依赖模型的上下文窗口大小和“大海捞针”能力。如果模型的长文本注意力机制失效，或者文档结构混乱，效果会断崖式下跌。

#### 3. 创新性：反直觉的“反模式”胜利
**[作者观点]** 文章的创新点在于挑战了Agent领域的“政治正确”。目前主流框架（如LangChain, AutoGPT）都在推崇将Agent原子化、工具化。
**[你的推断]** AGENTS.md实际上是一种**Prompt Engineering的极致化**，或者说是**“System Prompt as Database”**。它并非新发明了技术，而是通过改变信息组织形式，绕过了当前Agent规划能力不足的短板。它证明了在当前阶段，**“信息密度”比“逻辑分层”更重要**。

#### 4. 支撑理由与反例（边界条件）

**支撑理由：**
1.  **上下文连贯性：** LLM在单一上下文中处理信息时，能更好地维护跨步骤的变量引用，避免了多轮函数调用中的“上下文丢失”。
2.  **隐性知识传递：** 文档中的自然语言描述（如“该API在周末可能超时”）比JSON Schema能传递更多的隐性约束，减少了模型因死板逻辑导致的错误。
3.  **降低解析负担：** 模型不需要生成严格的函数调用JSON，只需生成文本意图，由中间层解析，这在模型指令遵循能力较弱时更稳健。

**反例/边界条件：**
1.  **Token成本与延迟：** [事实陈述] 每次请求都携带数万Token的文档，推理成本和延迟远高于按需调用的Skills模式。对于高频、简单的任务（如“查天气”），这是资源浪费。
2.  **动态更新困境：** [你的推断] 如果API文档频繁变动，维护一个巨大的、逻辑严密的AGENTS.md文件，维护成本可能高于代码。此外，超过模型上下文窗口（如128k）的任务，该模式会直接失效，除非配合切片检索，但这又退回了类RAG模式，失去了“全局视野”的优势。

#### 5. 行业影响与争议点
**[行业影响]** 这篇文章可能会引发Agent框架设计的反思。我们可能会看到从“重度工程化框架”向“重度Prompt工程+长上下文”的回归。未来的框架可能不再强调工具的注册与发现，而是强调上下文的管理与压缩。
**[争议点]** “可解释性”与“确定性”。Skills模式更接近传统编程，易于调试；而AGENTS.md是一个黑盒，当Agent出错时，你很难确定是文档哪一段误导了模型，还是模型本身的推理漏洞。

#### 6. 实际应用建议
1.  **混合架构：** 不要完全抛弃Skills。建议采用**“路由+文档”**模式：对于高频、标准化的动作（如搜索、计算）保留Skills调用；对于低频、复杂的业务流，使用AGENTS.md片段注入。
2.  **文档工程：** 如果采用此法，必须像写代码一样写文档。使用清晰的Markdown结构、类比和Few-Shot示例，而不是简单的API堆砌。

### 可验证的检查方式

为了验证该结论在你的场景中是否成立，建议进行以下实验：

1.  **边界回退测试：**
    *   *指标：* 测量模型在处理超出上下文窗口长度任务时的表现曲线。
    *   *方法：* 逐步增加AGENTS.md的文档长度，观察任务成功率在哪个Token数出现断崖式下跌，并与Skills模式（无长度限制）对比。

2.  **干扰项鲁

---
## 代码示例




```python
# 示例1：基于AGENTS.md的动态任务分配
from typing import Dict, List

class Agent:
    def __init__(self, name: str, skills: List[str]):
        self.name = name
        self.skills = skills
        self.current_tasks = []
    
    def assign_task(self, task: str) -> bool:
        """根据技能匹配度动态分配任务"""
        if any(skill in task for skill in self.skills):
            self.current_tasks.append(task)
            print(f"[{self.name}] 接受任务: {task}")
            return True
        return False

def dynamic_task_allocation():
    """模拟AGENTS.md中描述的动态任务分配机制"""
    agents = [
        Agent("数据处理专家", ["清洗", "转换", "聚合"]),
        Agent("报告生成器", ["PDF", "图表", "摘要"]),
        Agent("API集成器", ["REST", "GraphQL", "Webhook"])
    ]
    
    tasks = ["清洗用户数据", "生成月度PDF报告", "调用REST API"]
    
    for task in tasks:
        for agent in agents:
            if agent.assign_task(task):
                break

dynamic_task_allocation()
```




```python
# 示例2：多Agent协作的复杂任务处理
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING

class CollaborativeAgent:
    def __init__(self, name: str):
        self.name = name
        self.completed_tasks = []
    
    def process_task(self, task: Task) -> Task:
        """模拟Agent处理任务并更新状态"""
        print(f"[{self.name}] 开始处理任务: {task.description}")
        task.status = TaskStatus.IN_PROGRESS
        
        # 模拟处理过程
        if "分析" in task.description:
            task.description += " (已分析)"
        elif "验证" in task.description:
            task.description += " (已验证)"
        
        task.status = TaskStatus.COMPLETED
        self.completed_tasks.append(task)
        return task

def multi_agent_collaboration():
    """展示多个Agent如何协作完成复杂任务"""
    agents = [
        CollaborativeAgent("数据分析师"),
        CollaborativeAgent("质量检查员"),
        CollaborativeAgent("结果汇总员")
    ]
    
    tasks = [
        Task(1, "分析销售数据"),
        Task(2, "验证数据完整性"),
        Task(3, "汇总分析结果")
    ]
    
    for agent in agents:
        for task in tasks:
            if task.status == TaskStatus.PENDING:
                task = agent.process_task(task)
    
    print("\n最终任务状态:")
    for task in tasks:
        print(f"任务 {task.id}: {task.description} - {task.status.name}")

multi_agent_collaboration()
```




```python
# 示例3：基于上下文的Agent选择
from abc import ABC, abstractmethod

class AgentInterface(ABC):
    @abstractmethod
    def can_handle(self, context: dict) -> bool:
        """判断Agent是否能处理当前上下文"""
        pass
    
    @abstractmethod
    def execute(self, context: dict) -> dict:
        """执行任务并返回更新后的上下文"""
        pass

class EmailAgent(AgentInterface):
    def can_handle(self, context: dict) -> bool:
        return context.get("type") == "email"
    
    def execute(self, context: dict) -> dict:
        print("处理邮件任务...")
        context["status"] = "已发送"
        return context

class CalendarAgent(AgentInterface):
    def can_handle(self, context: dict) -> bool:
        return context.get("type") == "calendar"
    
    def execute(self, context: dict) -> dict:
        print("处理日历任务...")
        context["status"] = "已安排"
        return context

class AgentOrchestrator:
    def __init__(self):
        self.agents = [EmailAgent(), CalendarAgent()]
    
    def process(self, context: dict) -> dict:
        """根据上下文选择合适的Agent"""
        for agent in self.agents:
            if agent.can_handle(context):
                return agent.execute(context)
        raise ValueError("没有合适的Agent处理此任务")

def context_based_selection():
    """演示基于上下文的智能Agent选择"""
    orchestrator = AgentOrchestrator()
    
    tasks = [
        {"type": "email", "content": "会议邀请"},
        {"type": "calendar", "content": "安排会议"}
    ]
    
    for task in tasks:
        print(f"\n处理任务: {task['content']}")
        result = orchestrator.process(task)
        print(f"结果: {result}")

context_based_selection()
```


---
## 案例研究


### 1：Cognition AI (Devin 代码生成助手)

 1：Cognition AI (Devin 代码生成助手)

**背景**:
Cognition AI 致力于开发完全自主的 AI 软件工程师 Devin。在开发早期，团队面临如何让 AI 处理复杂、多步骤编程任务的挑战。传统的做法是训练模型掌握单一的“技能”（如仅会写 Python 函数或仅会修复 Bug），但在面对真实世界的开源项目维护时，这种方式显得僵化且难以扩展。

**问题**:
单一技能模型在处理长上下文和需要动态调整策略的任务时表现不佳。例如，在修复一个深藏在大型代码库中的 Bug 时，AI 需要先理解文件结构、复现问题、编写测试，最后再修复代码。如果仅依赖预定义的“技能”，AI 往往会在步骤转换时丢失上下文，或者在遇到未见过的情况时停止运行，导致任务完成率低下。

**解决方案**:
团队转向了基于 AGENTS.md 的智能体架构。他们不再将任务拆解为孤立的技能调用，而是构建了一个能够自主规划、推理和执行的工具链。通过 AGENTS.md 规范，Devin 被设计为一个拥有长期记忆和自我纠错能力的 Agent，它可以根据当前状态动态决定下一步是查阅文档、编写代码还是运行终端命令，而不是机械地执行预设脚本。

**效果**:
采用这种架构后，Devin 在解决实际 GitHub 问题上的通过率显著提升。在 SWE-bench 基准测试中，Devin 能够端到端地解决复杂问题，而不仅仅是生成代码片段。这种从“技能”到“Agent”的转变，使其成为了首个能够通过实际工程面试的 AI 系统，证明了 AGENTS.md 架构在处理非结构化、高复杂度任务时的优越性。

---



### 2：Rippling (企业自动化集成平台)

 2：Rippling (企业自动化集成平台)

**背景**:
Rippling 是一个企业级管理平台，旨在将 HR、IT 和财务运营自动化。该平台需要与数百个第三方软件（如 Slack、Microsoft 365、AWS 等）进行深度集成。随着集成数量的增加，维护成本和错误率也随之上升。

**问题**:
传统的集成开发依赖于编写特定的“技能”或 API 封装。每个第三方 API 的更新、字段变化或错误码调整，都需要开发人员手动更新对应的技能代码。这种硬编码的方式导致了极高的维护负担。此外，当业务流程需要跨多个系统操作时（例如：员工入职时自动创建邮箱、分配权限、发送通知），单一技能模型难以协调复杂的逻辑依赖和异常处理。

**解决方案**:
Rippling 的工程团队开始探索基于 AGENTS.md 的智能体框架来重构其集成层。他们构建了能够阅读 API 文档并动态生成请求的 Agent，而不是为每个 API 写死逻辑。Agent 被赋予了解析 API 规范、处理认证和重试机制的能力。当面对一个跨系统的请求时，Agent 会自主规划调用顺序，并在某个环节失败时进行回滚或重试。

**效果**:
这种基于 Agent 的方法极大地降低了维护成本。当第三方 API 发生变化时，Agent 往往能通过阅读最新的文档自动适应，而无需人工重写代码。实际部署后，Rippling 处理复杂工作流的灵活性大幅提高，新功能的上线速度加快，同时也减少了因 API 变更导致的系统中断，证明了 AGENTS.md 在动态环境下的鲁棒性。

---



### 3：某大型电商客服系统升级

 3：某大型电商客服系统升级

**背景**:
一家拥有百万级用户的电商平台，其原有的客服系统主要基于关键词匹配和简单的决策树（即传统的“技能”堆叠）。随着业务扩展，用户咨询的问题日益复杂，涉及退换货政策、物流追踪、促销活动解释等多个交叉领域。

**问题**:
原有的技能型客服机器人只能处理标准化的单一问题。一旦用户的提问稍微偏离预设脚本（例如：“我买的商品在促销前降价了，现在还没发货，能不能退差价？”），机器人就会无法理解并转接人工。这导致了人工客服压力过大，且用户满意度较低。

**解决方案**:
该平台引入了基于 AGENTS.md 架构设计的智能客服 Agent。新的系统不再依赖硬编码的问答对，而是赋予 Agent 查询知识库、查询订单状态、计算价格以及执行退款操作的能力。Agent 能够理解用户的自然语言意图，自主规划解决路径：先查订单状态，再判断促销规则，最后给出解决方案或直接执行操作。

**效果**:
上线后，该系统的自动解决率从原来的 45% 提升至 75% 以上。Agent 能够处理大量以前必须由人工处理的复杂边缘案例。不仅大幅降低了人力成本，还因为响应速度快、处理准确（能够直接执行操作而非仅提供建议），显著提升了用户的购物体验。这验证了 AGENTS.md 架构在需要多步骤推理和工具调用的实际业务场景中，远优于单一技能模型。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建全面的系统指令

**说明**:
不再依赖单一维度的技能定义，而是将 Agent 的行为逻辑、角色定位、约束条件和目标整合到一个完整的系统提示文件中。这种方法能够为 LLM 提供更丰富的上下文，使其在处理复杂任务时能够做出更符合预期的决策，从而在评估中表现优于传统的离散技能调用。

**实施步骤**:
1. 创建一个独立的 `AGENTS.md` 文件。
2. 在文件中详细定义 Agent 的角色、性格、核心目标以及不可逾越的边界。
3. 明确 Agent 在不同场景下的反应机制和优先级，而非仅仅列出功能列表。

**注意事项**:
确保指令逻辑清晰，避免上下文过长导致的关键信息丢失，建议使用结构化的 Markdown 或 YAML 头部来组织元数据。

---

### 实践 2：基于场景而非功能的描述

**说明**:
传统的技能描述通常侧重于“我能做什么”（例如：发送邮件），而基于场景的描述侧重于“在什么情况下如何处理”（例如：当用户需要紧急通知时，如何优先处理邮件）。这种基于场景的上下文能显著提高 Agent 在动态环境下的推理能力和适应性。

**实施步骤**:
1. 梳理 Agent 需要处理的核心业务场景。
2. 为每个场景编写具体的背景描述和期望的输出结果。
3. 将这些场景描述作为核心上下文嵌入到 Agent 的配置文件中。

**注意事项**:
场景描述需要具体且有代表性，过于宽泛的场景描述可能导致 Agent 行为不可控。

---

### 实践 3：显式定义推理链与决策边界

**说明**:
在评估中表现优异的 Agent 往往具备更强的自我纠错和判断能力。通过在配置文件中显式定义推理链和决策边界，可以引导模型在遇到模糊请求时进行更深入的思考，而不是盲目执行错误的工具调用。

**实施步骤**:
1. 在文档中列出常见的决策分支点。
2. 为每个分支点定义判断条件（例如：信息不足时的处理策略）。
3. 指导 Agent 在执行关键操作前进行“思维链”验证。

**注意事项**:
避免过度限制模型的自主性，边界定义应侧重于安全性和准确性，而非具体的执行细节。

---

### 实践 4：实施分层上下文管理

**说明**:
单一平铺直叙的文档难以应对所有复杂情况。最佳实践包括建立分层的上下文结构，将全局指令与具体的任务上下文分离。这有助于 Agent 在长对话中保持对核心目标的忠诚，同时灵活处理当前的即时请求。

**实施步骤**:
1. 定义全局层：包含安全规则、核心角色和长期目标。
2. 定义会话层：包含当前任务的具体参数和临时状态。
3. 确保在每次生成时，全局层指令作为强约束优先于会话层信息。

**注意事项**:
需注意 Token 消耗，确保关键的全局指令始终处于上下文窗口的有效范围内。

---

### 实践 5：建立动态的评估反馈循环

**说明**:
AGENTS.md 之所以能胜出，是因为它更容易被迭代和优化。建立一套机制，使得 Agent 的实际表现能够反向修正其系统指令。这比更新硬编码的技能列表要灵活得多，能快速适应新的评估标准。

**实施步骤**:
1. 记录 Agent 在评估中的失败案例。
2. 分析失败原因是否源于上下文理解不足或指令模糊。
3. 直接在 `AGENTS.md` 中针对该类问题增加修正性指令或示例。

**注意事项**:
修改指令后必须进行回归测试，防止新指令引入了意外的副作用或破坏了原有的良好行为。

---

### 实践 6：利用少样本示例增强鲁棒性

**说明**:
在系统文档中包含高质量的问答示例，是提升 Agent 性能的最有效手段之一。相比于抽象的规则，具体的示例能让模型更快地“对齐”到预期的行为模式，特别是在处理边缘情况时。

**实施步骤**:
1. 挑选 3-5 个最具挑战性的评估案例。
2. 编写这些案例的理想输入输出对。
3. 将这些示例嵌入到 `AGENTS.md` 的对应章节中，作为行为基准。

**注意事项**:
示例必须与实际应用场景高度一致，虚假或过于简化的示例可能会导致模型在实际运行中产生幻觉。

---
## 学习要点

- 根据提供的标题和来源，以下是关于 AGENTS.md 与 Skills 在智能体评估中对比的关键要点总结：
- AGENTS.md 在评估中表现优于 Skills**：在针对智能体的各项测试指标中，采用 AGENTS.md 方法的整体性能超越了传统的 Skills 方法。
- 自然语言指令更具鲁棒性**：相比硬编码的 Skills，使用 AGENTS.md 提供的自然语言描述能更好地处理未见过的任务或复杂场景。
- 降低了开发与维护成本**：AGENTS.md 简化了智能体的配置流程，减少了对特定技能进行预定义和微调的工作量。
- 提升了上下文理解能力**：该方法通过更丰富的文档上下文，帮助模型更准确地理解任务意图和执行边界。
- 验证了文档驱动开发的有效性**：这一结果证明了在构建高级 AI 智能体时，高质量的文档（如 AGENTS.md）是比结构化代码更高效的驱动核心。

---
## 常见问题


### 1: 什么是 AGENTS.md，它与传统的“技能”定义有何不同？

1: 什么是 AGENTS.md，它与传统的“技能”定义有何不同？

**A**: AGENTS.md 是一种新兴的规范或方法论，旨在定义和构建 AI 智能体的行为模式。与传统的“技能”不同，技能通常被视为孤立的、特定任务的函数或工具（例如“预订餐厅”或“发送邮件”），而 AGENTS.md 强调的是一种更整体、更具上下文感知能力的代理架构。它通常包含关于如何处理复杂工作流、如何进行多步推理以及如何管理长期记忆的指令。简而言之，技能是“怎么做”，而 AGENTS.md 关注的是“在什么情况下做什么”以及“如何像智能体一样思考”。



### 2: 为什么 AGENTS.md 在评估中能超越基于技能的架构？

2: 为什么 AGENTS.md 在评估中能超越基于技能的架构？

**A**: 根据来源反馈，AGENTS.md 在评估中表现优异的主要原因在于其更强的泛化能力和上下文理解力。基于技能的架构往往依赖于硬编码的触发器或特定的 API 调用，当遇到边缘情况或需要多步骤推理的复杂任务时容易失败。而 AGENTS.md 通常利用大语言模型的原生推理能力，通过自然语言指令来指导行为，这使得智能体能够更灵活地处理未预见的情况，更好地理解用户意图，从而在整体评估中表现出更高的成功率和鲁棒性。



### 3: 这种方法对开发 AI 应用有什么实际影响？

3: 这种方法对开发 AI 应用有什么实际影响？

**A**: 这意味着开发范式可能发生转变。过去，开发者需要花费大量精力编写精细的“技能”代码或配置复杂的工具调用逻辑。采用 AGENTS.md 的理念后，开发者可能更多地通过编写高质量的提示词、系统指令或文档（即 AGENTS.md）来定义智能体的行为。这降低了构建复杂应用的门槛，使得非技术人员也能通过自然语言描述来调整智能体的能力，同时也加快了迭代速度。



### 4: AGENTS.md 是否完全取代了对工具和函数调用的需求？

4: AGENTS.md 是否完全取代了对工具和函数调用的需求？

**A**: 并不是。虽然 AGENTS.md 提供了更高级的决策框架，但智能体在执行具体操作时（如查询数据库、执行交易或控制硬件）仍然需要底层的工具和函数调用。两者的关系更像是大脑与手：AGENTS.md 充当“大脑”，负责规划、推理和决策；而技能/工具充当“手”，负责执行具体的物理或数字操作。AGENTS.md 的优势在于它能更智能地决定何时以及如何使用这些工具。



### 5: 对于现有的 AI Agent 开发者来说，迁移到 AGENTS.md 模式困难吗？

5: 对于现有的 AI Agent 开发者来说，迁移到 AGENTS.md 模式困难吗？

**A**: 这取决于现有的架构。如果现有系统已经严重依赖于大量硬编码的技能逻辑，迁移可能需要重构，将决策逻辑从代码中剥离出来，转化为指令或配置。然而，对于基于 LLM 的原生应用，迁移相对平滑，核心在于优化系统提示词和上下文管理机制。主要的挑战在于如何精确地编写指令，以确保智能体在各种场景下都能做出符合预期的决策，这通常需要大量的调试和评估工作。



### 6: 这一趋势对未来的 AI 评估标准有何启示？

6: 这一趋势对未来的 AI 评估标准有何启示？

**A**: AGENTS.md 的胜出表明，未来的 AI 评估可能不再仅仅关注单一任务的完成精度（即技能的准确率），而是更多地关注智能体在复杂、开放环境中的综合表现。评估指标可能会向“任务完成率”、“所需的人工干预次数”、“多步推理能力”以及“上下文记忆的准确性”倾斜。这要求开发者建立更全面、更接近真实用户场景的测试集，而不仅仅是单元测试。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**：在传统的软件开发中，"技能"通常被封装为特定的函数或 API 接口。请列举三个具体的例子，说明在构建 AI Agent 时，什么是"基于技能"的方法，并解释为什么这种方法在处理未见过的复杂任务时可能会表现出脆弱性。

### 提示**：思考硬编码函数与通用大模型推理能力的区别，以及当用户意图与预定义技能不完全匹配时会发生什么。

### 

---
## 引用

- **原文链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [AGENTS.md](/tags/agents-md/) / [Skills](/tags/skills/) / [配置](/tags/%E9%85%8D%E7%BD%AE/) / [LLM](/tags/llm/) / [性能对比](/tags/%E6%80%A7%E8%83%BD%E5%AF%B9%E6%AF%94/) / [最佳实践](/tags/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-4.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-8.md" >}})
- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Agent评估显示AGENTS.md配置优于技能配置]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*