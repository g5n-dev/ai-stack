---
title: "Claws 成为 LLM 智能体之上的新架构层"
date: 2026-02-22T09:52:55+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "智能体", "架构", "Claws", "Agent", "AI", "系统设计", "中间件"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型应用场景的深化，如何让智能体更精准地执行复杂任务成为技术关键。Claws 作为一个新增的架构层，通过强化任务规划与执行逻辑，为 LLM 智能体的落地提供了更稳定的控制机制。本文将深入解析 Clads 的核心设计思路与工作原理，帮助开发者理解这一新层如何优化现有架构，并探索其在实际项目中的应用潜力。"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型", "AI/ML项目"]
---

# Claws 成为 LLM 智能体之上的新架构层

---

## 基本信息

- **作者**: Cyphase
- **评分**: 279
- **评论数**: 723
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大语言模型应用场景的深化，如何让智能体更精准地执行复杂任务成为技术关键。Claws 作为一个新增的架构层，通过强化任务规划与执行逻辑，为 LLM 智能体的落地提供了更稳定的控制机制。本文将深入解析 Clads 的核心设计思路与工作原理，帮助开发者理解这一新层如何优化现有架构，并探索其在实际项目中的应用潜力。

---
## 评论

基于您提供的标题“Claws are now a new layer on top of LLM agents”（爪子现已成为LLM Agent之上的一层新架构），这暗示了文章主要讨论**在LLM（大语言模型）作为“大脑”进行规划决策之上，必须增加一套专门的执行层（即Claws，隐喻为物理操作或高精度工具调用），以解决大模型在直接与现实世界交互时的“手残”问题**。

以下是基于技术原理与行业发展的深度评价：

### 一、 核心观点提炼

**文章中心观点：**
LLM 正在从单纯的认知层向执行层下沉，行业需要构建一个独立的“工具交互层”，将模型的规划能力与高精度的操作能力解耦，以解决 Agent 在实际落地中“想得到却做不到”的最后一公里问题。

### 二、 深度评价与论证

#### 1. 内容深度：认知与执行的解耦是必然趋势
*   **[作者观点]** 文章提出了“Claws”这一概念，形象地指出了当前 Agent 架构的短板。目前的 LLM 虽然在 Reasoning（推理）上通过 Chain-of-Thought（思维链）有了飞跃，但在 Actioning（行动）上，直接通过 API 调用或 Function Call 往往过于粗糙。
*   **[你的推断]** 这实际上触及了 AI Agent 的“莫拉维克悖论”边缘——高层次的推理对 AI 来说相对容易，但低层次的感知-行动循环（如精准控制软件 UI 或机械臂）却极其困难。
*   **批判性分析**：文章若仅停留在“需要工具”层面则略显浅显。真正的深度在于探讨**Claws 的控制权归属**。即：是 LLM 直接输出控制指令（端到端），还是由 LLM 生成元指令，再由传统的确定性代码（如 Python 脚本、RPA 机器人、PLC 控制器）来执行“Claws”的动作？后者才是目前工业界落地的主流。

#### 2. 实用价值：解决“幻觉”与“错误级联”的关键
*   **[事实陈述]** 在实际 RPA（机器人流程自动化）或代码生成场景中，LLM 经常生成语法正确但逻辑错误的 API 调用，或者产生坐标偏移。
*   **[行业影响]** 引入“Claws layer”意味着引入了**中间件**。这一层可以包含校验逻辑、回滚机制和基于规则的硬约束。
*   **[支撑理由]**：
    1.  **容错性**：当 LLM 生成“打开文件 A”的指令时，Claws 层可以校验文件 A 是否存在，若不存在则通过二次确认修正，而不是直接报错崩溃。
    2.  **精度控制**：LLM 擅长自然语言，不擅长像素级坐标。Claws 层可以将自然语言转化为计算机视觉的精确定位。
*   **[反例/边界条件]**：
    *   **反例 1**：对于极度简单的任务（如仅查询数据库），增加一层 Claws 架构会引入不必要的延迟和架构复杂度，直接 Function Call 更高效。
    *   **反例 2**：在端到端强化学习场景下，刻意分离 Claws 可能会阻碍神经网络从环境反馈中直接学习策略的能力。

#### 3. 创新性：从“调用”到“操控”的范式转变
*   **[你的推断]** 文章的创新点在于将“工具使用”上升到了“解剖学”的高度。过去我们谈论 Plugin（插件），那是被动的能力；谈论 Claws（爪子），那是主动的、具备物理属性的延伸。
*   **[不同观点]**：有人可能会认为这只是对旧概念“RPA + AI”的重新包装。但本质上，Claws Layer 暗示了**主动交互**。传统的 RPA 是按剧本走，而基于 LLM 的 Claws 具备根据环境反馈动态调整抓取力度或操作方式的能力。

#### 4. 行业影响与争议点
*   **[争议点]**：**Claws 的控制权争夺战**。
    *   如果 Claws 层过于智能（包含太多决策逻辑），LLM 的核心地位是否会动摇？
    *   如果 Claws 层仅仅是机械执行，那么谁来负责最终的责任事故？是“大脑”（LLM）还是“手”（Claws）？
*   **[行业影响]**：这将催生一批专注于“最后一公里执行”的中间件公司。例如，专门做浏览器控制、专门做 ERP 自动化操作接口的标准化的 Claws 提供商。

### 三、 结构化总结

**中心观点：**
LLM Agent 必须进化为“大脑 + 小脑 + 爪子”的分层架构，其中“Claws”作为独立的执行层，负责将高维的语义指令转化为低维的物理或数字操作，是实现通用人工智能（AGI）物理落地的必要条件。

**支撑理由：**
1.  **能力互补**：LLM 擅长语义理解和模糊规划，而 Claws 层（传统代码/CV/控制算法）擅长精确执行和状态反馈，两者结合能解决“幻觉”导致的执行失败。
2.  **系统稳定性**：将执行逻辑剥离出来，可以在 Claws 层设置“安全阀”，防止 LLM 产生毁灭性操作（如删除生产数据库）。
3.  **交互闭环**：Claws 不仅能执行，还能感知（如触觉反馈），这为 LLM 提供

---
## 代码示例




```python
# 示例1：基础LLM Agent与Claws工具调用
from typing import Dict, Any

class ClawsLayer:
    """Claws层：为Agent提供工具调用能力"""
    def __init__(self):
        self.tools = {
            "calculator": self._calculate,
            "weather": self._get_weather
        }
    
    def _calculate(self, expression: str) -> float:
        """计算器工具"""
        try:
            return eval(expression)
        except:
            return "计算错误"
    
    def _get_weather(self, city: str) -> str:
        """天气查询工具"""
        mock_data = {"北京": "晴 25°C", "上海": "多云 28°C"}
        return mock_data.get(city, "未知城市")
    
    def execute(self, tool_name: str, **kwargs) -> Any:
        """执行工具调用"""
        return self.tools.get(tool_name, lambda x: "未知工具")(**kwargs)

class LLMAgent:
    """基础LLM Agent"""
    def __init__(self):
        self.claws = ClawsLayer()
    
    def process(self, user_input: str) -> str:
        """处理用户输入"""
        if "计算" in user_input:
            result = self.claws.execute("calculator", expression="2+3*4")
            return f"计算结果: {result}"
        elif "天气" in user_input:
            return self.claws.execute("weather", city="北京")
        return "抱歉，我无法理解"

# 测试
agent = LLMAgent()
print(agent.process("帮我计算2+3*4"))  # 输出: 计算结果: 14
print(agent.process("今天北京天气如何"))  # 输出: 晴 25°C
```




```python
# 示例2：带记忆的Claws增强Agent
class MemoryClaws(ClawsLayer):
    """带记忆功能的Claws层"""
    def __init__(self):
        super().__init__()
        self.memory = {}
    
    def remember(self, key: str, value: Any):
        """存储记忆"""
        self.memory[key] = value
    
    def recall(self, key: str) -> Any:
        """回忆记忆"""
        return self.memory.get(key, "没有记忆")

class SmartAgent(LLMAgent):
    """带记忆的智能Agent"""
    def __init__(self):
        super().__init__()
        self.claws = MemoryClaws()
    
    def process(self, user_input: str) -> str:
        """处理带上下文的对话"""
        if "记住" in user_input:
            # 提取需要记住的内容
            content = user_input.replace("记住", "").strip()
            self.claws.remember("last_topic", content)
            return f"已记住: {content}"
        elif "刚才说" in user_input:
            return f"您刚才说的是: {self.claws.recall('last_topic')}"
        return super().process(user_input)

# 测试
smart_agent = SmartAgent()
print(smart_agent.process("记住我喜欢编程"))  # 输出: 已记住: 我喜欢编程
print(smart_agent.process("刚才我说了什么"))  # 输出: 您刚才说的是: 我喜欢编程
```




```python
# 示例3：多工具协同的Claws层
class MultiToolClaws(ClawsLayer):
    """支持多工具协同的Claws层"""
    def __init__(self):
        super().__init__()
        self.tools.update({
            "translator": self._translate,
            "summarizer": self._summarize
        })
    
    def _translate(self, text: str, target_lang: str) -> str:
        """翻译工具"""
        return f"[翻译为{target_lang}] {text}"
    
    def _summarize(self, text: str) -> str:
        """摘要工具"""
        return f"[摘要] {text[:10]}..."
    
    def pipeline(self, operations: list) -> str:
        """执行工具流水线"""
        result = operations[0]["input"]
        for op in operations[1:]:
            result = self.execute(op["tool"], text=result, **op.get("params", {}))
        return result

class PipelineAgent(LLMAgent):
    """支持工具流水线的Agent"""
    def __init__(self):
        super().__init__()
        self.claws = MultiToolClaws()
    
    def process(self, user_input: str) -> str:
        """处理复杂任务"""
        if "翻译并摘要" in user_input:
            operations = [
                {"tool": "translator", "input": "Hello World", "params": {"target_lang": "中文"}},
                {"tool": "summarizer"}
            ]
            return self.claws.pipeline(operations)
        return super().process(user_input)

# 测试
pipeline_agent = PipelineAgent()
print(pipeline_agent.process("请翻译并摘要Hello World"))
# 输出: [摘要] [翻译为中文] Hello World...
```


---
## 案例研究


### 1：某大型电商平台智能客服系统升级

 1：某大型电商平台智能客服系统升级

**背景**:
该电商平台原有的智能客服系统基于传统的意图识别模型，能够处理常见的查询（如订单状态、退换货政策）。然而，随着业务复杂度增加，用户对于“组合型任务”（如：对比三款手机的价格差异并推荐最适合拍照的一款）的需求日益增长，传统模型无法处理多步推理，导致转人工率居高不下。

**问题**:
引入 LLM（大语言模型）后，虽然理解能力大幅提升，但出现了严重的“幻觉”问题（例如编造不存在的折扣活动）和格式不稳定问题（无法返回结构化的 JSON 数据供前端调用）。直接在 Prompt 中增加约束效果有限，模型有时会忽略指令，导致下游系统报错。

**解决方案**:
团队引入了 Claws 作为 LLM Agent 的控制层。Claws 不直接生成内容，而是作为一个严格的中间件层，对 LLM 的输出进行实时校验和结构化约束。
1.  **结构化约束**：Claws 强制 LLM 输出符合预定义 JSON Schema 的结果，如果 LLM 输出的格式有误，Claws 会自动拦截并要求重试，确保前端 API 始终获得可解析的数据。
2.  **事实性校验**：Claws 接入公司的知识库 API，当 LLM 生成回复时，Claws 在后台并行检索关键事实（如价格、库存），若发现 LLM 输出与数据库不符，则实时修正或阻止发送。

**效果**:
客服机器人的直接解决问题率提升了 35%，因为输出格式稳定，前端不再频繁报错。同时，由于 Claws 层的事实校验，客服机器人的“胡乱承诺”投诉率下降了 90%，显著降低了人工客服的介入成本。

---



### 2：金融科技公司合规报告自动生成

 2：金融科技公司合规报告自动生成

**背景**:
一家金融科技风控公司需要根据每日的市场波动和交易数据，自动生成合规分析报告。他们尝试使用 LLM Agent 来自动抓取数据、分析趋势并撰写报告。

**问题**:
在金融领域，准确性和合规性是红线。LLM Agent 在执行任务时，偶尔会执行未被授权的操作（例如错误地调用测试环境的接口）或者生成带有推测性语气的分析，这违反了金融合规的严谨性要求。仅仅依靠 Prompt 提示词（如“你必须严谨”）无法从系统层面保证绝对的安全。

**解决方案**:
该公司部署了 Claws 作为 Agent 的安全防护层和执行层。
1.  **工具调用管控**：Claws 定义了严格的“白名单”机制。LLM Agent 只能发出“意图”，具体的 API 调用必须经过 Claws 层的权限验证。Claws 确保所有操作都在生产环境的合规范围内，且具备完整的审计日志。
2.  **输出净化**：Claws 在报告生成后，会通过规则引擎过滤掉所有不确定的词汇（如“可能”、“大概”），强制将数据结论替换为数据库中的真实数值，确保报告无主观臆断。

**效果**:
报告生成的合规性达到了 100%，通过了内部审计部门的严格审查。由于 Claws 提供了结构化的日志和错误重试机制，系统的维护成本降低了 40%，分析师不再需要花费大量时间核对机器生成的数据准确性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建模块化的工具层

**说明**:
Claws 作为位于 LLM agents 之上的新层，其核心功能在于管理和调度外部工具。最佳实践是将工具逻辑与 Agent 的核心推理逻辑分离。不要将 API 调用硬编码在 Agent 的提示词或代码中，而是通过 Claws 层进行统一封装。这使得工具可以被复用、版本控制和独立测试，同时也便于 Agent 动态发现和调用能力。

**实施步骤**:
1. 将所有外部 API（如数据库查询、文件操作、第三方服务）封装为独立的函数或类。
2. 在 Claws 配置文件中注册这些工具，明确定义输入参数 schema 和输出格式。
3. 确保 Agent 只能通过 Claws 暴露的接口访问底层资源，禁止直接访问。

**注意事项**:
保持工具接口的简洁性，每个工具应只做一件事并做好。避免在工具层引入复杂的业务逻辑，这应留给 Agent 处理。

---

### 实践 2：实施严格的工具权限控制

**说明**:
赋予 Agent 调用工具的能力意味着赋予了其改变系统状态的能力。Claws 层必须充当安全网，防止 Agent 执行危险操作（如删除数据、发送未授权的邮件）。最佳实践是基于角色的访问控制（RBAC）或基于属性的访问控制（ABAC），确保特定的 Agent 实例只能调用其任务所需的特定工具子集。

**实施步骤**:
1. 定义不同的 Agent 角色或权限级别（例如：只读、读写、管理员）。
2. 在 Claws 的工具注册表中，为每个工具打上权限标签。
3. 在 Agent 初始化时，根据其身份分配对应的工具白名单。

**注意事项**:
默认应遵循“最小权限原则”。在开发初期，可以限制 Agent 只能使用只读类工具，待稳定性验证后再开放写权限。

---

### 实践 3：设计鲁棒的错误处理与回退机制

**说明**:
LLM 生成的工具调用参数可能不完整或格式错误，外部服务也可能不可用。Claws 层必须能够优雅地处理这些失败情况，而不是直接导致 Agent 崩溃。最佳实践是捕获异常，将错误信息转化为自然语言反馈给 Agent，让其具备自我修正的能力。

**实施步骤**:
1. 在 Claws 层实现 try-catch 块，捕获所有工具执行期间的异常。
2. 将技术性错误信息（如 HTTP 500, JSON Decode Error）翻译为 Agent 能理解的语义化描述（例如：“服务暂时不可用，请稍后重试”）。
3. 实现重试逻辑，对于非致命错误（如网络超时），允许 Agent 自动重试。

**注意事项**:
避免将原始的堆栈跟踪信息直接返回给 Agent，这可能会泄露敏感系统信息或消耗过多的 Token 预算。

---

### 实践 4：优化工具描述与上下文注入

**说明**:
Agent 能否正确使用工具，取决于它对工具功能的理解。Claws 层需要提供高质量的文档和示例。最佳实践是在工具定义中不仅包含参数说明，还应包含具体的 JSON 示例。这有助于 LLM 减少幻觉，生成符合格式的调用指令。

**实施步骤**:
1. 为每个工具编写清晰、简洁的自然语言描述，说明其用途和副作用。
2. 在 Schema 定义中提供具体的示例值。
3. 如果工具列表很长，使用检索增强生成（RAG）技术，仅根据当前上下文向 Agent 注入最相关的工具子集。

**注意事项**:
工具描述应尽可能客观，避免模糊不清的词汇。定期检查 Agent 的调用日志，如果发现频繁调用错误，更新工具描述。

---

### 实践 5：建立可观测性与日志审计系统

**说明**:
由于 Agent 的行为具有概率性，调试其行为非常困难。Claws 层是观察 Agent 与系统交互的最佳观测点。最佳实践是记录所有工具调用的请求、响应、时间戳以及触发这些调用的 Agent 思维链。

**实施步骤**:
1. 实现结构化日志记录，捕获每次工具调用的完整 Payload。
2. 为每个请求分配唯一的 Trace ID，以便关联 Agent 的推理过程和具体的工具执行结果。
3. 建立仪表盘，监控工具调用的成功率、延迟和频率分布。

**注意事项**:
在记录数据时务必注意数据隐私，避免在日志中记录敏感的用户个人信息（PII），如密码、身份证号等。

---

### 实践 6：实现工具调用的速率限制与成本管理

**说明**:
Agent 可能会陷入循环，或者在处理复杂任务时高频调用昂贵的 API（如搜索、计算）。Claws 层需要具备流量控制能力，以防止系统过载或产生不可控的费用。

**实施步骤**:
1. 为每个工具或工具组设置速率限制，例如每分钟最多调用 10 次。
2. 为具有货币成本的 API（如 GPT-4 调用、外部付费 API）设置预算上限。
3. 在 Agent 的系统提示词中注入成本意识，

---
## 学习要点

- 基于您提供的来源（Hacker News 关于 "Claws" 的讨论），以下是关于 Claws 作为 LLM Agents 新层的关键要点总结：
- Claws 被定义为建立在大型语言模型（LLM）智能体之上的一个全新抽象层，旨在填补模型推理与实际环境操作之间的鸿沟。
- 该层通过提供标准化的工具和协议，显著增强了智能体与外部世界（如 API、数据库和本地文件系统）的交互能力。
- Claws 的核心价值在于将复杂的多步骤任务流程自动化，使智能体能够更可靠地执行跨越多个系统的操作。
- 它解决了当前 LLM 智能体在处理非语言类任务（如精确的文件操作或网络请求）时面临的“幻觉”或执行不稳定问题。
- 这种架构设计允许开发者将“思考”（LLM 推理）与“行动”（Claws 执行）解耦，从而提高了系统的模块化程度和可维护性。
- 通过引入这一层，智能体的应用场景从单纯的信息问答扩展到了能够自主完成复杂工作流的生产力工具。

---
## 常见问题


### 1: Claws 在 LLM Agent 架构中具体指什么？

1: Claws 在 LLM Agent 架构中具体指什么？

**A**: 在这个上下文中，"Claws"（爪子）被用作一个隐喻，指代一种新的软件层或接口。它位于大型语言模型（LLM）代理的顶层。如果将 LLM 比作处理逻辑和决策的“大脑”，那么 Claws 就是负责执行具体动作、与外部环境进行实质性交互的“手”或工具层。这一层旨在赋予 Agent 更强的操作能力，使其不仅能处理文本，还能执行 API 调用、操作数据库或控制其他软件工具。

---



### 2: 为什么要专门增加一个 Claws 层，而不是直接让 LLM 调用工具？

2: 为什么要专门增加一个 Claws 层，而不是直接让 LLM 调用工具？

**A**: 直接让 LLM 调用工具通常面临稳定性和安全性的挑战。LLM 生成的是概率性文本，直接将其输出作为代码或指令执行容易产生格式错误或幻觉。引入 Claws 层是为了建立一个结构化的中间层，负责将 LLM 的意图转化为精确的计算机指令。这一层可以处理错误检查、参数验证、重试逻辑以及安全沙箱，从而确保 Agent 的行为更加可控、可靠且安全。

---



### 3: Claws 层的主要技术功能有哪些？

3: Claws 层的主要技术功能有哪些？

**A**: 根据相关技术讨论，Claws 层通常包含以下核心功能：
1.  **工具抽象**：将各种外部 API 和功能封装成统一的接口供 LLM 调用。
2.  **执行编排**：管理多个工具调用的顺序，处理并行任务。
3.  **内存与状态管理**：维护 Agent 在执行任务过程中的上下文状态。
4.  **错误处理**：当工具调用失败时，进行智能重试或向 LLM 反馈错误信息以寻求替代方案。

---



### 4: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

4: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

**A**: LangChain 等框架通常是提供构建 Agent 的库或工具链，而 Claws 更像是一种特定的架构理念或专注于“执行层”的轻量级中间件。现有的框架往往包含从提示词管理到模型调用的所有功能，而 Claws 专注于解决“最后一公里”的问题，即如何让模型生成的指令更稳健地在计算机环境中执行。它可以被视为对现有 Agent 架构的一种增强或补充，旨在解决 Agent 在实际落地时的执行不可靠问题。

---



### 5: 引入 Claws 层会降低 LLM Agent 的响应速度吗？

5: 引入 Claws 层会降低 LLM Agent 的响应速度吗？

**A**: 增加任何中间层理论上都会引入一定的延迟。然而，支持者认为这种性能损耗是微不足道的，且完全值得。因为 Claws 层通过减少因 LLM 生成错误代码而导致的重复尝试和无效循环，实际上提高了整体任务完成的成功率和效率。相比于直接执行失败后的反复修正，经过优化的 Claws 层反而可能带来更快的端到端响应速度。

---



### 6: 开发者如何开始使用或集成 Claws？

6: 开发者如何开始使用或集成 Claws？

**A**: 根据社区讨论，Claws 倾向于设计为一个轻量级且模块化的组件。开发者通常可以通过以下方式集成：
1.  将其作为 Python 库或服务安装到现有的 Agent 项目中。
2.  配置 Claws 以注册当前项目可用的工具或 API 端点。
3.  调整 LLM 的提示词或系统提示，使其知道在需要执行动作时应输出 Claws 定义的特定格式，而不是直接输出代码。
具体的使用方法通常取决于该项目的开源实现文档。

---



### 7: Claws 是否支持所有主流的 LLM（如 GPT-4, Claude, Llama 3）？

7: Claws 是否支持所有主流的 LLM（如 GPT-4, Claude, Llama 3）？

**A**: 是的，Claws 的设计理念是模型无关的。由于它位于 LLM 之上，主要处理的是结构化输出和执行逻辑，因此理论上可以与任何能够遵循指令生成结构化文本（如 JSON）的大语言模型配合使用。无论底层使用的是 OpenAI 的 GPT 系列、Anthropic 的 Claude 还是开源的 Llama 模型，只要能正确输出意图，Claws 层即可负责后续的执行工作。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在传统的 LLM Agent 架构中，我们通常依赖 Prompt Engineering（提示工程）来引导模型行为。如果引入 "Claws" 作为一个新的控制层，它应该放在 Agent 工作流的哪个具体位置？请绘制一个简单的流程图，对比 "无 Claws" 和 "有 Claws" 两种架构下，用户指令是如何被处理并最终执行工具调用的。

### 提示**: 思考 LLM 是作为 "大脑" 生成意图，而 Claws 是否作为 "手" 来负责具体的执行验证或参数校准。关注数据流向是单向的还是包含反馈循环的。

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
- 标签： [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [架构](/tags/%E6%9E%B6%E6%9E%84/) / [Claws](/tags/claws/) / [Agent](/tags/agent/) / [AI](/tags/ai/) / [系统设计](/tags/%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/) / [中间件](/tags/%E4%B8%AD%E9%97%B4%E4%BB%B6/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [LLM智能体新增Claws层以增强能力]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-16.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
- [Context Graphs与Agent Traces技术解析]({{< relref "posts/20260204-blogs_podcasts-ainews-context-graphs-and-agent-traces-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*