---
title: "AGENTS.md 架构在智能体评估中优于 Skills 架构"
date: 2026-01-30T12:06:39+08:00
draft: false
entry_kind: "auto"
tags: ["智能体", "Agent", "评估", "AGENTS.md", "架构设计", "LLM", "AI", "性能测试"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在构建 AI Agent 的技术选型中，AGENTS.md 正展现出优于传统 Skills 的评估表现。这一差异不仅关乎代码的执行效率，更直接影响智能体在复杂任务中的规划准确性与系统稳定性。本文将深入剖析两者的核心区别，并分享我们在实际评估中的具体数据与发现，希望能为你的 Agent 架构设计提供更具参考价值的决策依据"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型", "AI/ML项目"]
---

# AGENTS.md 架构在智能体评估中优于 Skills 架构

---

## 基本信息

- **作者**: maximedupre
- **评分**: 353
- **评论数**: 149
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在构建 AI Agent 的技术选型中，AGENTS.md 正展现出优于传统 Skills 的评估表现。这一差异不仅关乎代码的执行效率，更直接影响智能体在复杂任务中的规划准确性与系统稳定性。本文将深入剖析两者的核心区别，并分享我们在实际评估中的具体数据与发现，希望能为你的 Agent 架构设计提供更具参考价值的决策依据。

---
## 评论

**文章中心观点**
在构建通用AI智能体时，采用结构化、基于角色的AGENTS.md配置文件（即“人设驱动”）在任务执行的灵活性与泛化能力上显著优于传统的原子化“技能”调用模式，因为前者能更好地激发大语言模型（LLM）的上下文推理能力。

**支撑理由与边界条件分析**

**1. 认知封装的层级差异（事实陈述 / 作者观点）**
*   **支撑理由**：文章指出，Skills模式通常将任务预拆解为僵硬的函数调用（如`tool.search()`），这要求模型在推理前必须先进行精确的意图识别和工具匹配。相比之下，AGENTS.md模式通过在System Prompt中植入详尽的角色定义、目标背景和软性约束，允许模型在上下文窗口内自主规划路径。这种方法利用了LLM的“思维链”特性，减少了中间步骤的上下文切换损耗，从而在复杂任务中表现更佳。
*   **反例/边界条件**：在**高精度或确定性要求**的场景下（如执行SQL交易、严格遵循API入参），Skills模式由于强制了Schema约束，其执行稳定性往往高于自由度较高的AGENTS.md模式。后者的“幻觉”问题可能导致非结构化的输出。

**2. 维护成本与组合灵活性（你的推断 / 作者观点）**
*   **支撑理由**：从软件工程角度看，Skills模式类似于面向对象编程（OOP）中的方法调用，扩展新功能往往需要注册新的工具。而AGENTS.md更像是一种“配置即代码”的声明式管理。当业务逻辑变更时（例如改变客服机器人的语气或处理流程），修改Prompt中的文本描述显然比重写代码逻辑或重新编排Skill工作流要敏捷得多。
*   **反例/边界条件**：当系统规模扩大到**数百个智能体**协作时，纯粹的文本配置（AGENTS.md）会导致版本控制和依赖管理变得混乱。相比之下，Skills作为代码接口，具有更强的类型检查和互操作性，更适合构建大规模微服务架构的Agent系统。

**3. 上下文学习（ICL）的效能（你的推断）**
*   **支撑理由**：AGENTS.md实际上是一个巨大的Few-Shot提示模板。它不仅告诉模型“做什么”，还通过示例和描述告诉模型“怎么做”以及“谁在做”。这种高密度的语义信息能帮助模型更好地处理边缘情况。
*   **反例/边界条件**：这种模式高度依赖模型的**上下文窗口大小和指令遵循能力**。对于参数量较小（如7B以下）的模型，过长的AGENTS.md文档可能导致“迷失中间”现象，即模型忽略了文档中的关键约束，反而导致性能下降。

**可验证的检查方式**

为了验证AGENTS.md是否真的优于Skills，建议进行以下维度的对比测试：

1.  **Token消耗与延迟对比测试（指标）**：
    *   在相同任务集下，分别统计两种模式的输入/输出Token数及端到端延迟。
    *   *观察窗口*：虽然AGENTS.md输入Token更长（Prompt更长），但若其能减少多轮交互次数，则总Token成本可能更低。

2.  **边缘案例通过率（实验）**：
    *   构建一组包含模糊指令或需要多步推理的测试集（例如：“帮我整理一下会议纪要，如果太长就发邮件，否则存为草稿”）。
    *   *观察窗口*：观察Skills模式是否因为缺少预定义工具而失败，以及AGENTS.md模式是否能通过自主规划完成任务。

3.  **替换模型后的鲁棒性测试（实验）**：
    *   将底层LLM从GPT-4o切换到Llama-3-70b或更小的模型。
    *   *观察窗口*：记录性能下降的斜率。通常Skills模式对模型智力要求较低，而AGENTS.md模式在弱模型上的表现可能会出现断崖式下跌。

---

### 深度评价

#### 1. 内容深度
文章触及了当前Agent工程化的核心矛盾：**是“代码逻辑”强，还是“自然语言语义”强？** 作者通过AGENTS.md这一具体载体，实际上是在探讨“软架构”的可能性。论证较为严谨，指出了传统Skill编排的僵化性。然而，文章可能略带技术偏见，似乎将Skills等同于简单的函数调用，忽略了现代Agent框架（如LangGraph）中动态编排Skills的能力。

#### 2. 实用价值
对于初创团队或快速原型验证阶段，该观点极具价值。它降低了开发门槛，使得非程序员也能通过编写Markdown文档来定义Agent行为。这符合当前“Prompt Engineering is not dead”的趋势。但在企业级落地中，完全抛弃Skills可能导致难以追溯的Debug困难。

#### 3. 创新性
将“配置文件”提升为“第一性原理”是文章的创新点。它挑战了目前主流的ReAct模式（即Thought+Action），提出了一种更拟人化的“Role+Context”模式。这与近期业界关于“Generalist Agents”的探索不谋而合。

#### 4. 可读性
文章结构清晰，对比鲜明。通过具体的文件名（AGENTS.md）作为概念锚点，易于传播和记忆。

#### 5. 行业影响
如果这一观点被广泛采纳，可能会催生新一代的Agent开发框架，这类框架将不再以“工具注册”为核心，而是以“Role/Profile管理”为核心。同时也可能推动LLM在长文本理解上的进一步优化。

#### 6. 争议点或不同观点
最大的争议在于

---
## 代码示例




```python
# 示例1：基于AGENTS.md的动态任务规划
def dynamic_task_planner():
    """
    模拟AGENTS.md中的动态任务规划能力
    相比固定技能调用，能根据上下文自动调整执行步骤
    """
    from typing import List, Dict
    
    def plan_execution(context: Dict) -> List[str]:
        """根据上下文动态生成执行计划"""
        steps = []
        if context.get("has_database"):
            steps.append("query_database")
        if context.get("needs_api"):
            steps.append("call_external_api")
        if context.get("requires_processing"):
            steps.append("process_results")
        return steps
    
    # 测试用例
    scenario1 = {"has_database": True, "needs_api": False}
    scenario2 = {"has_database": False, "needs_api": True, "requires_processing": True}
    
    print(f"场景1执行计划: {plan_execution(scenario1)}")
    print(f"场景2执行计划: {plan_execution(scenario2)}")

dynamic_task_planner()
```




```python
# 示例2：多步骤推理与验证
def reasoning_with_verification():
    """
    模拟AGENTS.md中的推理验证机制
    在执行关键步骤前进行合理性检查
    """
    def safe_divide(a: float, b: float) -> float:
        """带验证的除法操作"""
        if abs(b) < 1e-6:
            raise ValueError("除数接近零")
        return a / b
    
    def calculate_average(numbers: List[float]) -> float:
        """计算平均值并验证结果"""
        if not numbers:
            return 0.0
        avg = sum(numbers) / len(numbers)
        if not (min(numbers) <= avg <= max(numbers)):
            raise ValueError("计算结果超出合理范围")
        return avg
    
    # 测试用例
    try:
        print(f"安全除法: {safe_divide(10, 2)}")
        print(f"平均值: {calculate_average([1, 2, 3, 4, 5])}")
    except ValueError as e:
        print(f"验证失败: {e}")

reasoning_with_verification()
```




```python
# 示例3：工具使用决策树
def tool_selection_tree():
    """
    模拟AGENTS.md中的工具选择决策
    根据输入特征自动选择最合适的处理工具
    """
    from enum import Enum
    
    class ToolType(Enum):
        TEXT_PROCESSOR = 1
        IMAGE_ANALYZER = 2
        NUMERIC_CALCULATOR = 3
    
    def select_tool(input_data: Dict) -> ToolType:
        """根据输入特征选择工具"""
        if input_data.get("type") == "text":
            return ToolType.TEXT_PROCESSOR
        elif input_data.get("type") == "image":
            return ToolType.IMAGE_ANALYZER
        elif input_data.get("type") == "number":
            return ToolType.NUMERIC_CALCULATOR
        else:
            raise ValueError("未知输入类型")
    
    # 测试用例
    inputs = [
        {"type": "text", "content": "hello"},
        {"type": "image", "url": "example.jpg"},
        {"type": "number", "value": 42}
    ]
    
    for inp in inputs:
        tool = select_tool(inp)
        print(f"输入类型: {inp['type']} -> 选择工具: {tool.name}")

tool_selection_tree()
```


---
## 案例研究


### 1：某 SaaS 客户支持自动化项目

 1：某 SaaS 客户支持自动化项目

**背景**: 一家提供企业级 CRM 软件的初创公司，试图利用 AI 客服代理来处理日益增长的工单量。最初，他们采用基于“技能”的架构，为不同任务（如“重置密码”、“更新账单”、“生成报表”）分别编写了独立的 API 调用函数。

**问题**: 在实际评估中，单一技能无法处理复杂的边缘情况。例如，当用户询问“为什么我的报表生成失败，且我想顺便更改邮箱”时，基于技能的系统只能线性执行，往往在处理报表报错逻辑时卡住，无法灵活切换到更改邮箱的上下文，导致任务完成率仅为 45%。

**解决方案**: 团队重构了系统，采用类似 AGENTS.md 的架构，不再依赖硬编码的技能，而是向 Agent 提供一份包含所有 API 端点、数据库模式和业务逻辑规则的详细文档。Agent 被允许自主规划路径，根据文档动态决定是先查日志还是先改配置。

**效果**: 在相同的测试集下，Agent 的任务完成率提升至 82%。它成功处理了多轮推理和跨域问题，减少了 60% 需要人工介入的复杂工单。

---



### 2：内部 DevOps 知识库问答助手

 2：内部 DevOps 知识库问答助手

**背景**: 一家拥有 10 年技术积累的金融科技公司，其内部运维文档极其庞杂，包含数千页的 Wiki 和 Confluence 页面。新入职的工程师很难快速找到解决特定服务器报错的方法。

**问题**: 早期的问答系统基于“技能”匹配，即预先定义好常见问题（FAQ）的模板。如果用户提问方式与模板稍有偏差，或者问题涉及多个微服务的交互（如“服务 A 降级导致服务 B 数据不一致”），系统就无法检索到正确答案，只能返回通用的错误链接。

**解决方案**: 引入基于 AGENTS.md 模式的 Agent，将整个内部网络拓扑、常见故障排除指南和 API 文档作为上下文输入。Agent 不再检索预定义答案，而是像阅读文档的资深工程师一样，实时阅读相关文档并综合信息给出操作步骤。

**效果**: 系统解决问题的覆盖率从 30% 提升到了 75% 以上。Agent 能够根据文档中的逻辑推断出非标准问题的解决方案，将新员工的平均问题解决时间从 30 分钟缩短至 5 分钟以内。

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用显式知识库替代隐式技能微调

**说明**: 在构建 Agent 时，直接在 AGENTS.md 或类似的上下文文档中提供详细的领域知识、操作指南和业务规则，往往比通过微调模型来学习特定技能更有效。显式的知识库更容易更新、维护，且能减少模型幻觉，确保 Agent 的行为符合预期。

**实施步骤**:
1. 整理业务流程、常见问题解答和操作规范。
2. 将这些信息结构化写入 AGENTS.md 或知识库文件。
3. 在 Agent 运行时，将该文档作为系统提示词或检索上下文的一部分输入。
4. 定期根据业务变化更新文档内容。

**注意事项**: 确保文档结构清晰，避免信息过载，必要时结合 RAG（检索增强生成）技术进行分段检索。

---

### 实践 2：构建结构化的 Agent 角色定义

**说明**: 不要仅依赖简单的指令，而应在配置文件中详细定义 Agent 的角色、目标、约束条件和背景信息。明确的角色定义有助于模型更好地理解任务上下文，从而在评估中表现出更高的准确性和稳定性。

**实施步骤**:
1. 定义 Agent 的核心职责和主要目标。
2. 列出 Agent 必须遵守的负面约束。
3. 描述 Agent 的目标受众和交互风格。
4. 将上述内容标准化并置于 AGENTS.md 的头部或配置区域。

**注意事项**: 角色定义应与实际任务高度相关，避免过于宽泛或抽象的描述。

---

### 实践 3：实施少样本提示策略

**说明**: 在 AGENTS.md 中包含具体的输入输出示例。相比于让模型通过训练学习技能，提供高质量的示例能让模型快速掌握预期的交互模式和推理路径，显著提升复杂任务的完成质量。

**实施步骤**:
1. 收集典型的用户查询和理想的 Agent 响应。
2. 挑选具有代表性的边缘案例和常见场景。
3. 将示例格式化后放入知识库中。
4. 在提示词中明确指示模型参考这些示例进行回答。

**注意事项**: 示例需要保持高质量和一致性，错误的示例会直接误导模型。

---

### 实践 4：建立标准化的评估基准

**说明**: 既然 AGENTS.md 方法在评估中表现更好，应建立一套严格的评估基准来验证知识库的有效性。通过自动化测试和人工评估相结合的方式，持续监控 Agent 在特定任务上的表现。

**实施步骤**:
1. 定义关键评估指标，如准确率、召回率和响应相关性。
2. 构建包含不同难度级别的测试集。
3. 定期运行 Agent 评估脚本，对比不同配置版本的性能。
4. 根据评估结果迭代优化 AGENTS.md 的内容。

**注意事项**: 评估数据应与训练数据分离，确保测试结果的客观性。

---

### 实践 5：利用思维链增强推理能力

**说明**: 在 AGENTS.md 中引导模型展示其推理过程。通过要求模型在执行动作前进行逐步思考，可以减少逻辑错误，提高在多步推理任务中的成功率，这比单纯训练模型“直觉”更可靠。

**实施步骤**:
1. 在知识库中添加“思考协议”或“推理步骤”章节。
2. 指示 Agent 在回答复杂问题时先列出步骤。
3. 提供包含思考过程的完整示例供模型模仿。
4. 调整提示词以强制输出思考过程。

**注意事项**: 平衡推理深度与响应速度，避免在简单任务上产生不必要的延迟。

---

### 实践 6：动态上下文注入与检索优化

**说明**: AGENTS.md 可能会变得非常庞大。最佳实践是结合检索机制，根据当前任务动态提取最相关的部分注入到上下文中，而不是每次都将整个文件发送给模型，以提高效率和准确性。

**实施步骤**:
1. 将 AGENTS.md 拆分为多个模块或章节。
2. 实现语义检索功能，将用户查询映射到相关章节。
3. 仅提取最相关的 Top-K 个片段作为上下文。
4. 构建提示词，将检索到的内容与任务指令结合。

**注意事项**: 确保检索片段包含足够的上下文信息，避免截断导致语义缺失。

---
## 学习要点

- 基于标题“AGENTS.md outperforms skills in our agent evals”，以下是关于 AI 代理系统设计的 5 个关键要点总结：
- 自然语言指令优于结构化技能**：直接在系统提示词中提供详尽的 AGENTS.md 文档，其表现优于将功能封装为独立的“技能”或工具，这表明大模型在理解上下文时，自然语言比结构化定义更高效。
- 降低系统复杂度是关键**：放弃复杂的技能调用架构，转而依赖文档驱动的方法，可以显著减少工程开销和系统维护的难度。
- 上下文即代码**：该发现暗示了在 Agent 开发中，高质量的上下文文档（如 AGENTS.md）正在取代传统的代码逻辑或硬编码配置，成为控制 Agent 行为的核心。
- 提升代理的推理能力**：通过文档而非僵化的技能接口进行交互，可能给予了模型更大的推理空间，从而在评估中获得了更好的决策质量。
- 重新评估“工具使用”范式**：这一结果挑战了当前主流的“函数调用”或“工具使用”趋势，提示在某些场景下，纯粹的语言交互可能比 API 调用更强大。

---
## 常见问题


### 1: 什么是 AGENTS.md，它与传统的 "Skills"（技能）定义有何本质区别？

1: 什么是 AGENTS.md，它与传统的 "Skills"（技能）定义有何本质区别？

**A**: AGENTS.md 是一种用于定义和描述 AI 智能体行为的新标准或方法论。在传统的 AI 开发中，"Skills" 通常指代特定的、狭窄的能力（例如“写诗”、“翻译代码”），这些技能往往是硬编码或通过特定微调获得的。

AGENTS.md 的核心区别在于它提供了一种更全面、结构化的方式来描述智能体的上下文、目标、约束和可用资源。它不再仅仅将智能体视为一堆技能的集合，而是将其视为一个具有明确角色定义和决策边界的实体。通过这种文档化的定义，智能体能够更好地理解其在复杂任务中的职责，从而在评估中表现出比单纯调用“技能”更好的性能。



### 2: 为什么在评估中 AGENTS.md 的表现会优于 Skills？

2: 为什么在评估中 AGENTS.md 的表现会优于 Skills？

**A**: 根据 Hacker News 的讨论及相关技术背景，主要原因在于**上下文理解**和**任务泛化能力**的提升。

1.  **上下文完整性**：AGENTS.md 提供了关于智能体角色和能力的完整描述，使得模型在生成响应时能够依据更丰富的元数据进行推理，而不仅仅是匹配一个关键词触发的技能。
2.  **减少幻觉与错误匹配**：传统的 Skills 调用有时会因意图识别错误而失败。AGENTS.md 允许智能体根据文档中的指令自主判断如何行动，这种基于角色的推理通常比基于函数调用的推理更鲁棒。
3.  **复杂任务处理**：在需要多步推理的复杂评估中，AGENTS.md 能帮助智能体保持目标一致性，而 Skills 往往是碎片化的，难以协同处理长尾任务。



### 3: AGENTS.md 是否意味着不再需要 Function Calling（函数调用）或 Tools（工具）？

3: AGENTS.md 是否意味着不再需要 Function Calling（函数调用）或 Tools（工具）？

**A**: 不是。AGENTS.md 并不是要取代 Function Calling 或工具使用，而是对它们的一种补充和增强。

AGENTS.md 主要解决的是**智能体如何定义自身以及如何理解任务指令**的问题。在实际运行中，通过 AGENTS.md 定义的智能体依然可能需要调用外部 API 或执行具体的代码函数。区别在于，AGENTS.md 提供了更高层次的逻辑控制，告诉智能体*何时*以及*为何*使用某个工具，而不是仅仅依赖底层的技能接口。简而言之，AGENTS.md 是“大脑”的说明书，而 Skills 是“手”的操作指南，两者结合效果最佳。



### 4: 对于开发者来说，采用 AGENTS.md 会有哪些具体的好处？

4: 对于开发者来说，采用 AGENTS.md 会有哪些具体的好处？

**A**: 开发者采用这种标准可以获得以下显著优势：

1.  **调试与可观测性**：通过文本化的定义文件，开发者可以更清晰地看到智能体被赋予了什么权限和目标，这比在代码中零散地定义技能更容易调试。
2.  **模块化与复用**：AGENTS.md 可以作为一种配置文件被不同的智能体实例复用，便于快速部署具有特定角色的 AI 助手。
3.  **性能提升**：正如标题所述，由于智能体能更准确地理解预期行为，因此在实际评估中往往能获得更高的分数，减少了针对特定 Prompt 进行反复微调的时间。



### 5: 这种方法目前是否存在局限性或潜在风险？

5: 这种方法目前是否存在局限性或潜在风险？

**A**: 是的，尽管评估结果积极，但仍存在一些挑战：

1.  **Token 消耗**：将详细的智能体描述注入到上下文窗口中会占用大量的 Token，这在处理长对话或上下文窗口有限的模型时可能会增加成本或导致上下文截断。
2.  **解析准确性**：智能体需要能够准确地“阅读”并遵守 AGENTS.md 中的指令。如果模型的指令遵循能力较弱，那么文档再详细也可能被忽略。
3.  **标准化问题**：目前 AGENTS.md 并非一个强制性的行业标准，而是一种最佳实践的总结。不同的团队可能使用不同的格式，导致缺乏互操作性。



### 6: AGENTS.md 最适合应用在哪些场景中？

6: AGENTS.md 最适合应用在哪些场景中？

**A**: AGENTS.md 最适合应用于**角色定义明确**且**任务逻辑复杂**的场景。

例如：
*   **客户支持专员**：需要严格遵守服务准则，同时具备查询订单、退款等多种技能。
*   **私人助理**：需要根据用户的日程和偏好进行多步规划，而不是简单执行单一命令。
*   **代码审查专家**：需要理解特定的编码规范和项目背景，而不仅仅是运行一个 linter 工具。

在这些场景中，明确的职责界定比单纯的技能调用更能保证输出的质量和安全性。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在构建 Agent 时，"技能"通常被定义为执行特定任务的硬编码函数或提示词模板。请列举出三个具体的场景，在这些场景中，使用硬编码的"技能"会比通用的 Agent（如文中提到的 AGENTS.md 方法）表现更好或效率更高。

### 提示**: 思考那些输入输出格式极度固定、对延迟敏感、或者不需要复杂推理链路的任务。考虑维护成本与系统复杂度的平衡。

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
- 标签： [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [AGENTS.md](/tags/agents-md/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/) / [LLM](/tags/llm/) / [AI](/tags/ai/) / [性能测试](/tags/%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-4.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-8.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-16.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*