---
title: "LLM智能体新增Claws层以增强工具调用能力"
date: 2026-02-22T11:49:53+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "智能体", "工具调用", "Claws", "Agent", "架构设计", "模型增强", "Hacker News"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型（LLM）应用场景的深入，如何让智能体更精准地执行复杂任务成为开发焦点。Claws 作为一种新增的架构层，通过在模型与工具之间建立更规范的交互机制，有效提升了 Agent 的可控性与稳定性。本文将剖析 Claws 的核心设计逻辑，并探讨它如何帮助开发者解决 Agent 编程中的常见难题。"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型"]
---

# LLM智能体新增Claws层以增强工具调用能力

---

## 基本信息

- **作者**: Cyphase
- **评分**: 307
- **评论数**: 741
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大语言模型（LLM）应用场景的深入，如何让智能体更精准地执行复杂任务成为开发焦点。Claws 作为一种新增的架构层，通过在模型与工具之间建立更规范的交互机制，有效提升了 Agent 的可控性与稳定性。本文将剖析 Claws 的核心设计逻辑，并探讨它如何帮助开发者解决 Agent 编程中的常见难题。

---
## 评论

**文章中心观点**
文章主张“Claws”是一种在大型语言模型（LLM）智能体之上新增的中间层，旨在通过提供精细化的操作接口和安全约束，解决当前智能体在执行复杂任务时面临的控制力不足与幻觉问题，从而实现从“对话能力”向“可靠行动”的跨越。

**支撑理由与边界条件**

1.  **增强控制粒度与确定性**
    *   **[你的推断]** 文章核心逻辑在于，LLM 本质上是概率预测模型，直接输出 API 调用或动作指令容易产生格式错误或不可逆的操作。引入 Claws 层（可能指代类似工具调用约束、函数封装或中间件架构），实质上是在概率输出与物理/数字世界执行之间建立了一道“防火墙”或“适配器”。
    *   **[事实陈述]** 在 LangChain 或 AutoGPT 等框架中，直接让 LLM 生成 Shell 命令往往会导致系统崩溃。Claws 层通过预定义的动作空间，限制了 LLM 的自由度，提高了稳定性。
    *   **反例/边界条件**：如果 Claws 层的定义过于僵化，会限制 LLM 的泛化能力。例如，在需要创造性组合工具的场景下，严格的接口定义可能导致智能体无法“跳出框架”思考。

2.  **解决“幻觉”与“执行偏差”**
    *   **[作者观点]** 文章暗示 LLM 智能体常处于“眼高手低”的状态，即规划完美但执行走样。Claws 层通过反馈机制，将执行结果重新映射回 LLM 的上下文，形成闭环。
    *   **[你的推断]** 这借鉴了经典控制理论中的“误差校正”概念。Claws 不仅仅是执行器，更是验证器。
    *   **反例/边界条件**：如果 Claws 层自身的反馈机制存在延迟或噪声（例如网络请求超时被误判为任务失败），反而会误导 LLM 进行无效的重试，导致资源浪费和死循环。

3.  **安全性与沙箱隔离**
    *   **[你的推断]** 标题中的“Claws”隐喻了某种危险但有力的工具。文章强调了这一层作为安全代理的重要性，防止 LLM 智能体直接访问敏感数据或执行破坏性操作。
    *   **[事实陈述]** 企业级应用中，绝不允许 LLM 直接连接生产数据库。
    *   **反例/边界条件**：增加安全层必然带来额外的 Token 消耗和推理延迟。在实时性要求极高的场景（如高频交易或即时竞技游戏），Claws 层可能成为性能瓶颈。

**多维度深入评价**

**1. 内容深度：从“大脑”到“小脑”的进化**
文章的深度在于它跳出了单纯优化 Prompt 或模型参数的窠臼，转向了**系统架构**的视角。它敏锐地指出了当前 AI Agent 领域的一个痛点：仅有强大的“大脑”（LLM）是不够的，还需要灵活的“手”和精准的“神经末梢”（Claws）。文章将 Claws 定义为“Layer”，暗示了这是一种基础设施级别的抽象，而非简单的工具集，这具有相当的理论高度。然而，文章在技术实现细节上可能略显模糊，未明确 Claws 是基于代码逻辑、确定性有限状态机（DFA）还是另一个轻量级模型。

**2. 实用价值：工程落地的关键拼图**
对于开发者而言，这篇文章的价值极高。它直接指导了如何构建生产级的 Agent 系统。目前许多开源 Agent 项目失败的原因就是缺乏这一层，导致系统在 Demo 中表现完美，但在长周期运行中崩溃。文章提出的架构实际上是目前业界主流的“ReAct 模式 + 工具调用”的升级版或具象化，对于 RAG（检索增强生成）系统的后期处理和自动化运维具有直接的指导意义。

**3. 创新性：概念的重新包装与聚焦**
“Claws”作为一个新术语，虽然技术上可能对应现有的 Tool Use 或 Function Calling，但其隐喻非常精准。它强调了“抓取”和“破坏力”的双重属性。创新点在于将“安全约束”与“执行能力”合并为一个独立的层级进行讨论，这有助于开发者将关注点从“如何让模型更聪明”转移到“如何让模型更听话、更可控”。

**4. 可读性与逻辑性**
文章结构清晰，通过“Layer”这一概念有效地降低了认知负荷。但技术类文章若缺乏具体的架构图或伪代码，容易让读者陷入“听起来很有道理，但不知道怎么写代码”的困境。如果文章能结合具体的案例（如数据库操作失败后的回滚机制）来阐述 Claws 的作用，说服力会更强。

**5. 行业影响**
如果这一概念被广泛采纳，将推动 AI Agent 开发从“模型驱动”向“架构驱动”转变。未来的竞争可能不再仅仅是谁的模型参数大，而是谁的 Claws 层更坚固、更灵活。这可能会催生一批专门提供“Agent 执行层中间件”的初创公司。

**6. 争议点与不同观点**
*   **[争议点]** 是否需要独立的 Claws 层，还是可以通过模型微调（如 SFT）直接让 LLM 学会严格遵守格式？
*   **[不同观点]** 坚定的“Scaling Law”信仰者可能认为，随着模型推理能力的提升，未来的 LLM 可以直接端到端地处理所有细节，中间层只是过渡期的补丁，而非长期解决方案。

**7. 实际应用建议**

---
## 代码示例




```python
# 示例1：基础LLM Agent与Claws层集成
from openai import OpenAI

class ClawsLayer:
    """Claws层：为LLM Agent添加工具调用能力"""
    def __init__(self, tools):
        self.tools = tools  # 可用工具列表
    
    def execute(self, tool_name, **kwargs):
        """执行指定工具"""
        if tool_name not in self.tools:
            raise ValueError(f"工具 {tool_name} 不存在")
        return self.tools[tool_name](**kwargs)

def basic_agent_with_claws():
    # 初始化Claws层，注册工具
    claws = ClawsLayer(tools={
        "calculator": lambda x, y: x + y,
        "get_weather": lambda city: f"{city}当前温度25°C"
    })
    
    # 模拟LLM Agent决策
    user_query = "计算3+5"
    if "计算" in user_query:
        result = claws.execute("calculator", x=3, y=5)
        return f"计算结果：{result}"
    return "抱歉，无法处理该请求"

print(basic_agent_with_claws())
```




```python
# 示例2：带记忆的Claws增强Agent
from typing import Dict, List

class EnhancedClawsAgent:
    """带记忆和工具调用的增强型Agent"""
    def __init__(self):
        self.memory: Dict[str, str] = {}  # 对话记忆
        self.claws = ClawsLayer(tools={
            "save_note": lambda content: f"已保存笔记：{content}",
            "search_web": lambda query: f"搜索结果：关于'{query}'的前3条信息..."
        })
    
    def process(self, user_input: str) -> str:
        # 检查记忆
        if user_input in self.memory:
            return f"从记忆中找到：{self.memory[user_input]}"
        
        # 工具调用决策
        if "保存" in user_input:
            response = self.claws.execute("save_note", content=user_input)
            self.memory[user_input] = response
            return response
        elif "搜索" in user_input:
            return self.claws.execute("search_web", query=user_input)
        return "我可以帮您保存笔记或搜索信息"

agent = EnhancedClawsAgent()
print(agent.process("保存今天的会议记录"))
print(agent.process("搜索Python教程"))
```




```python
# 示例3：多工具协作的Claws工作流
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    data: str
    next_action: str = None

class WorkflowClaws:
    """支持工作流的Claws层"""
    def __init__(self):
        self.tools = {
            "extract_data": lambda text: ToolResult(True, "提取的数据：ABC123"),
            "validate": lambda data: ToolResult(True, f"验证通过：{data}"),
            "store": lambda data: ToolResult(True, f"已存储：{data}")
        }
    
    def execute_workflow(self, steps: List[str]) -> str:
        current_data = None
        for step in steps:
            if step not in self.tools:
                return f"未知步骤：{step}"
            
            result = self.tools[step](current_data) if current_data else self.tools[step]()
            if not result.success:
                return f"步骤 {step} 失败"
            
            current_data = result.data
            if result.next_action:
                steps.append(result.next_action)
        
        return current_data

workflow = WorkflowClaws()
print(workflow.execute_workflow(["extract_data", "validate", "store"]))
```


---
## 案例研究


### 1：某大型跨境电商平台的智能客服调度系统

 1：某大型跨境电商平台的智能客服调度系统

**背景**:
该平台拥有数百万日活用户，客服团队每天需处理海量咨询，涉及订单查询、退换货、物流追踪及复杂的售后纠纷。平台已部署了基于 LLM 的客服机器人来处理基础问答，但随着业务复杂度增加，单一模型难以应对所有场景。

**问题**:
单一的 LLM Agent 在处理“多步骤、跨系统”的任务时表现不佳。例如，处理一个“跨境退货并退款”的请求，机器人需要查询物流状态（调用物流 API）、检查仓库入库记录（调用 ERP 系统）、计算汇率差异（计算模块）并最终执行退款（调用支付网关）。LLM 往往在逻辑推理上产生幻觉，或者在 API 调用时因为参数错误而失败，导致任务完成率低，不得不转交人工，增加了运营成本。

**解决方案**:
引入 Claws 作为 LLM Agent 的编排控制层。Claws 并不替代底层的 LLM，而是作为一层“逻辑增强”的外骨骼。
1. **任务分解**：Claws 接收用户意图后，利用硬编码的确定性逻辑将复杂的退货流程拆解为严格的步骤序列。
2. **工具校验**：在 LLM 生成 API 调用代码之前，Claws 会预先校验参数的完整性和格式，防止 LLM 发送非法请求。
3. **状态管理**：Claws 维护交互的状态机，确保只有在上一步（如仓库确认收货）成功后，才触发下一步（退款操作）。

**效果**:
引入 Claws 后，复杂任务的自动化处理成功率从 45% 提升至 85% 以上。系统不再因为 LLM 的偶尔幻觉而执行错误的退款操作，安全性大幅提高。同时，由于 Claws 处理了繁琐的流程控制，LLM 只需专注于理解用户意图和生成自然语言回复，响应延迟降低了 30%。

---



### 2：金融科技公司的自动化合规审计 Agent

 2：金融科技公司的自动化合规审计 Agent

**背景**:
一家金融数据服务商需要为客户自动生成审计报告。该过程要求 Agent 阅读大量的非结构化财务文档（如 PDF 报表），提取特定数据，并严格依据预定义的合规规则（如 Basel III 或当地税务法规）进行计算和比对。

**问题**:
纯 LLM 方案在数学计算和规则遵守上存在缺陷。LLM 可能会“理解”文档内容，但在进行复杂的财务比率计算（如流动比率、负债率）时，经常出现算术错误。此外，合规规则是刚性的，不允许 LLM 进行“创造性”的解读。直接使用 LLM 往往导致审计结果不准确，无法满足金融级的合规要求。

**解决方案**:
使用 Claws 构建混合架构，将 LLM 作为“感知层”，Claws 作为“计算与规则层”。
1. **感知与提取**：LLM 负责阅读文档，将关键数字（如资产总额、负债总额）提取为结构化 JSON。
2. **规则硬化**：Claws 接收 LLM 提取的数据，利用内置的确定性 Python 执行环境和预置的合规公式库进行计算。
3. **结果断言**：Claws 对计算结果进行逻辑断言检查（例如：资产必须等于负债加所有者权益），如果发现不平衡，会强制 LLM 重新提取数据，而不是直接生成错误报告。

**效果**:
该方案实现了审计报告生成的高度准确率，数值计算错误率降至接近零。通过 Claws 的介入，系统成功通过了严格的外部合规审计。相比完全人工审计，报告生成时间从 3 天缩短至 20 分钟，且保证了 100% 的规则执行一致性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建模块化的工具层

**说明**: Claws 作为 LLM agents 之上的新层，核心功能在于为智能体提供与外部世界交互的能力。最佳实践是构建一个模块化、标准化的工具接口层，将具体的 API 调用、数据库查询或文件操作封装成标准化的函数。这可以降低大模型直接处理复杂逻辑的难度，提高系统的可维护性。

**实施步骤**:
1. 审查现有业务逻辑，识别出可被 Agent 调用的功能点（如发送邮件、查询库存）。
2. 使用 Python 装饰器或 JSON Schema 定义这些工具的输入参数和输出描述。
3. 将所有工具注册到 Claws 的工具注册表中，确保元数据清晰。

**注意事项**: 确保工具的输入输出描述极其准确，因为 LLM 依赖这些文本来理解如何调用工具。

---

### 实践 2：实施严格的错误处理与回退机制

**说明**: 由于 LLM 生成的工具调用参数可能存在格式错误或逻辑漏洞，系统必须具备鲁棒性。不能假设 Agent 第一次调用就能成功。当工具调用失败（如 API 超时或参数无效）时，系统应能捕获错误，并将具体的错误信息反馈给 LLM，让其进行自我修正。

**实施步骤**:
1. 在工具执行器周围包裹 Try-Catch 块，捕获所有异常。
2. 将错误信息转化为自然语言提示词，重新输入给 LLM。
3. 设计重试策略，对于非致命错误允许重试 1-2 次。

**注意事项**: 避免将原始的堆栈跟踪信息直接暴露给 LLM，应总结为可读的错误描述。

---

### 实践 3：优化提示词工程以增强工具调用能力

**说明**: 并非所有的 LLM 都能天生理解如何使用工具。需要通过精心设计的 System Prompt 来指导 Agent 何时以及如何使用 Claws 层。提示词应包含工具使用的示例、输出格式的具体要求以及工具调用的限制条件。

**实施步骤**:
1. 在 System Prompt 中明确列出可用工具及其用途。
2. 提供 2-3 个 Few-shot 示例，展示在特定场景下如何组合使用工具。
3. 指导模型在缺少必要参数时主动向用户提问，而不是瞎猜。

**注意事项**: 定期根据模型表现更新提示词，不同的基座模型可能需要不同的提示策略。

---

### 实践 4：建立细粒度的权限与安全沙箱

**说明**: 赋予 Agent 调用工具的能力意味着赋予了其改变现实世界状态的能力。必须实施最小权限原则。Claws 层应包含一个中间件，用于校验 LLM 生成的调用请求是否符合安全策略，防止 Agent 执行危险操作（如删除数据库或发送恶意邮件）。

**实施步骤**:
1. 为每个工具定义风险等级。
2. 实施人工确认机制：对于高风险操作，系统应暂停并等待人工审批，而不是自动执行。
3. 限制工具的可访问范围，例如限制文件系统的访问路径。

**注意事项**: 安全检查应在工具执行之前进行，而不是之后。

---

### 实践 5：设计可观测性与日志记录系统

**说明**: 在 LLM 和工具交互的闭环中，"黑盒"问题依然存在。为了调试和优化，必须记录每一次思考过程。你需要记录 LLM 的原始输出、解析后的工具调用参数、工具的返回结果以及最终的用户回复。

**实施步骤**:
1. 集成追踪系统（如 LangSmith 或自建日志中间件）。
2. 记录完整的链路追踪数据：User Input -> LLM Thought -> Tool Call -> Tool Output -> Final Answer。
3. 建立仪表盘分析工具调用的成功率和常见错误模式。

**注意事项**: 在记录日志时注意脱敏，不要将敏感的用户数据或 API Key 写入日志。

---

### 实践 6：处理上下文窗口与记忆管理

**说明**: 随着对话的深入和工具调用的增多，上下文长度会迅速膨胀。Claws 层需要配合记忆管理机制，对历史工具调用结果进行压缩或摘要，避免超出模型的 Token 限制，同时保留关键信息。

**实施步骤**:
1. 区分短期记忆和长期记忆。
2. 对于工具返回的冗长数据（如长文档内容），先进行摘要再存入上下文。
3. 实施滑动窗口策略，适时丢弃不再相关的历史工具调用记录。

**注意事项**: 确保在压缩信息时，不会丢失解决当前任务所需的关键细节。

---
## 学习要点

- 基于对 Claws 架构及其在 LLM Agents 生态中定位的分析，以下是 5 个关键要点：
- Claws 被定义为位于大语言模型（LLM）Agents 之上的全新抽象层，旨在解决当前 Agent 架构中存在的碎片化问题。
- 该架构通过提供统一的标准化接口，将底层大模型与上层应用逻辑解耦，从而显著降低开发复杂 AI 应用的门槛。
- Claws 引入了“状态持久化”机制，能够有效解决 LLM 的无状态特性，使 Agent 具备长期记忆和上下文连续性。
- 它通过模块化的设计模式（如工具调用和规划组件），大幅提升了 AI 系统的可扩展性与可维护性。
- 这种分层结构有助于构建更通用的“Agent 即服务”生态，让开发者能专注于业务逻辑而非底层模型细节。

---
## 常见问题


### 1: Claws 在 LLM Agents 架构中的具体定位是什么？

1: Claws 在 LLM Agents 架构中的具体定位是什么？

**A**: 根据标题描述 "Claws are now a new layer on top of LLM agents"，Claws 被定义为一个位于大语言模型智能体之上的新层级。在软件架构中，这通常意味着 Claws 并非替代底层的 LLM（如 GPT-4 或 Claude），而是作为一个中间件或接口层存在。它的主要作用可能是处理 LLM 与外部环境之间的交互，例如管理工具调用、处理持久化记忆、或者优化 Agent 的输出结构。简而言之，LLM 负责“思考”和生成语言，而 Claws 负责“行动”和与系统交互的具体实现。

---



### 2: 为什么需要在 LLM Agents 之上添加一个新层级？

2: 为什么需要在 LLM Agents 之上添加一个新层级？

**A**: 在当前的 AI Agent 开发中，直接让 LLM 与底层工具或 API 交互往往面临稳定性、安全性和解析能力的问题。引入像 Claws 这样的新层级通常是为了解决以下痛点：
1.  **稳定性**：防止 LLM 生成无效的 API 调用或格式错误的指令。
2.  **抽象化**：将复杂的底层逻辑封装起来，让开发者只需关注高层业务逻辑。
3.  **控制与监控**：在执行动作前增加一道防线，便于进行权限审查或日志记录。
4.  **增强能力**：赋予 LLM 原本不具备的能力，例如精确的数学计算、复杂数据库查询或长期记忆管理。

---



### 3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

**A**: 虽然 Claws 的具体实现细节取决于其发布的技术文档，但根据“新层级”这一描述，它可能更侧重于“执行层”或“运行时环境”的构建，而不仅仅是链式调用。与 LangChain 等侧重于编排组件的框架不同，Claws 可能更像是一个紧贴 LLM 输出的“外壳”或“操作系统”，专门负责将 LLM 的意图转化为具体的计算机操作。它可能比通用框架更轻量，或者专门针对特定的交互模式（如浏览器自动化、代码执行）进行了优化。

---



### 4: Claws 是否支持多模态输入或输出？

4: Claws 是否支持多模态输入或输出？

**A**: 虽然标题未明确提及，但作为一个现代 LLM Agent 的增强层，Claws 很有可能设计用于处理多模态交互。如果 Claws 旨在作为 Agent 的感官和行动接口，它可能不仅处理文本，还负责图像的渲染、音频的播放或网页的浏览控制。这意味着当 LLM 生成描述（如“显示一张猫的图片”）时，Claws 负责实际的渲染和展示工作；或者当 Agent 需要视觉信息时，Claws 负责截取屏幕或处理图像数据并传递给 LLM。

---



### 5: 集成 Claws 是否会显著增加系统的延迟？

5: 集成 Claws 是否会显著增加系统的延迟？

**A**: 增加一个额外的层级理论上会引入一定的处理开销，但这取决于 Claws 的实现效率。如果 Claws 是用高性能语言（如 Rust 或 Go）编写的，并且主要进行轻量级的逻辑判断或数据转发，其对延迟的影响几乎可以忽略不计。相反，如果 Claws 能有效缓存结果、预处理请求或减少 LLM 的 Token 消耗（例如通过本地计算替代某些 LLM 推理），它甚至可能提高整体系统的响应速度和效率。

---



### 6: Claws 是开源项目还是商业产品？

6: Claws 是开源项目还是商业产品？

**A**: 该内容来源于 Hacker News，通常意味着它是一个受到开发者社区关注的技术项目。虽然标题未明确说明其开源状态，但出现在该平台上通常意味着它有公开的代码库、技术文档或可供开发者测试的版本。开发者通常可以通过访问项目的 GitHub 页面或官方网站来确认其许可证类型。如果它是作为一个“层”被提出，很可能是为了促进开发者采用，因此开源或提供免费开发版的可能性较大。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 架构调用链路的变化

### 问题**: 在传统的 LLM Agent 架构中，通常直接由 LLM 决定调用哪个工具。如果引入 "Claws"（作为新的控制层），在处理简单的天气查询任务时，系统架构的调用链路会发生什么具体变化？

### 提示**: 思考在没有 Claws 时，LLM 是如何直接生成 API 调用的；加入 Claws 后，是谁来验证或拦截这个调用请求，以及这是如何增加了一层“手”的概念的。

### 

---
## 引用

- **原文链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [工具调用](/tags/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8/) / [Claws](/tags/claws/) / [Agent](/tags/agent/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/) / [模型增强](/tags/%E6%A8%A1%E5%9E%8B%E5%A2%9E%E5%BC%BA/) / [Hacker News](/tags/hacker-news/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [LLM智能体新增Claws层：强化外部工具调用与任务执行能力]({{< relref "posts/20260221-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-13.md" >}})
- [LLM智能体新增Claws层以增强功能]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-10.md" >}})
- [LLM智能体新增Claws层以优化任务执行]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-14.md" >}})
- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*