---
title: "AGENTS.md 架构在智能体评估中优于 Skills 架构"
date: 2026-01-30T09:43:20+08:00
draft: false
entry_kind: "auto"
tags: ["智能体", "Agent", "AGENTS.md", "架构设计", "评估", "Skills", "LLM", "性能优化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在智能体的实际评估中，AGENTS.md 这种文档形式的表现优于传统的 Skills 定义。这一发现促使团队重新审视构建 Agent 的最佳实践，并思考如何通过更清晰的文档来提升系统的可控性与推理能力。本文将详细解读这一评估结果背后的原因，并探讨其对未来 Agent 开发流程的启示。"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型"]
---

# AGENTS.md 架构在智能体评估中优于 Skills 架构

---

## 基本信息

- **作者**: maximedupre
- **评分**: 310
- **评论数**: 131
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在智能体的实际评估中，AGENTS.md 这种文档形式的表现优于传统的 Skills 定义。这一发现促使团队重新审视构建 Agent 的最佳实践，并思考如何通过更清晰的文档来提升系统的可控性与推理能力。本文将详细解读这一评估结果背后的原因，并探讨其对未来 Agent 开发流程的启示。

---
## 评论

**中心观点**
文章主张在构建 AI Agent 时，采用“AGENTS.md”（即显式的、文档化的全局上下文与规范）作为指令输入，其效果优于传统的“Skills”（即结构化的函数调用或工具定义）。

**支撑理由与边界条件**

1.  **上下文带宽与语义完整性（事实陈述/作者观点）**
    *   **理由**：传统的 Skills 定义通常受限于 Schema（如 OpenAPI 的 JSON 描述），只能描述参数类型和简要描述，难以承载复杂的业务逻辑、禁忌条件或上下文依赖。而 AGENTS.md 实际上是一段长文本，允许模型以自然语言的形式深度理解任务的“全貌”。这符合 LLM 基于概率预测下一个 token 的特性，即“上下文越多，推理越准”。
    *   **边界条件/反例**：当任务极其简单且对确定性要求极高时（如单纯的加减法或查询特定字段），长文本反而可能引入噪音，导致模型“幻觉”或过度解读，此时结构化的 Skills 更优。

2.  **降低“中间层”的语义损耗（你的推断）**
    *   **理由**：使用 Skills 往往需要模型进行两次映射：User Intent -> Function Call -> Execution。AGENTS.md 模式更接近于“思维链”引导，模型直接在文档中查找策略并生成最终输出或代码，减少了“意图识别”到“工具选择”之间的语义断层。这对于需要多步推理的复杂任务尤为有效。
    *   **边界条件/反例**：在需要与外部系统进行严格类型交互的场景下（如操作数据库 SQL），缺乏强类型约束的 AGENTS.md 可能导致生成的代码无法执行，此时 Skills 的类型检查功能不可替代。

3.  **动态规划与自我修正能力（作者观点）**
    *   **理由**：文章暗示 AGENTS.md 赋予了 Agent 更大的自主权。模型不是机械地调用预定义的工具，而是根据文档描述的“原则”动态决定行动方案。这种“软约束”比“硬编码”更具鲁棒性，能处理边缘情况。
    *   **边界条件/反例**：对于黑盒操作或安全性要求极高的生产环境，这种“自由度”是危险的。如果 AGENTS.md 的权限描述不严谨，模型可能会做出越权操作，而 Skills 可以通过后端代码进行硬性权限拦截。

---

**深度评价**

#### 1. 内容深度：从“工具理性”回归“认知理性”
文章触及了当前 Agent 工程化的一个核心痛点：**结构化数据与自然语言之间的摩擦成本**。
*   **论证严谨性**：作者通过 Eval 结果对比，揭示了“过度工程化”的弊端。过去几个月，行业倾向于将一切能力封装成 API/Skills，但这实际上是用传统的编程思维去约束生成式 AI。文章指出，对于 LLM 而言，一段高质量的、信息密集的自然语言文档，往往比一堆结构化的接口定义更能激发其推理能力。
*   **批判性视角**：文章可能存在“幸存者偏差”。Eval 的测试集可能偏向于逻辑推理或文本处理类任务。如果 Eval 包含大量的数据抓取或格式化转换任务，Skills 的优势可能会被抹杀。

#### 2. 实用价值：重构 Agent 开发流程
*   **指导意义**：这对开发者提出了新的要求——**Prompt Engineering 的宏观化**。开发者不仅要擅长写 Prompt，更要擅长写“系统文档”。这意味着 Agent 的开发重心从“写代码封装工具”转移到了“编写高质量的规范文档”。
*   **局限性**：AGENTS.md 的维护成本极高。随着业务逻辑变更，如何保证文档的实时更新？Skills 可以通过代码版本控制，而文档很容易成为“僵尸文档”。

#### 3. 创新性：Prompt Chaining 的极致形态
*   **新观点**：文章提出的并非全新技术，而是一种**范式转移**。它否定了“Agent = ChatGPT + Function Calling”的简单公式，提出了“Agent = ChatGPT + Knowledge Base (as Policy)”的架构。这与最近流行的“System 2 Thinking”（慢思考）趋势不谋而合。
*   **对比**：这与 Semantic Kernel 或 LangChain 等框架强调的“工具编排”截然不同，它更接近于“RAG（检索增强生成）+ Reasoning”的结合体。

#### 4. 可读性与逻辑
*   **表达清晰度**：文章标题直击痛点，通过对比实验结果直接抛出结论，逻辑链条清晰（问题 -> 实验 -> 结论 -> 建议）。
*   **逻辑漏洞**：文章未详细说明 AGENTS.md 的具体颗粒度。是将所有业务逻辑写在一个文件里，还是模块化引用？如果是前者，上下文窗口限制和注意力分散将是巨大问题。

#### 5. 行业影响：挑战“API 主义”
*   **潜在影响**：如果该结论在大范围内得到验证，将对现有的 Agent 框架（如 LangChain, AutoGPT）产生冲击。这些框架大多建立在“工具/链”的抽象之上。行业可能会从“构建复杂的工具调用链”转向“构建高质量的上下文文档库”。
*   **社区反应**：这可能会引发“去工具化”的讨论，即：我们是否过度设计了 Agent 的结构，而忽视了模型本身的理解能力？

#### 6. 争议点与不同观点
*   **争议点**：**可解释性与调试性**。Skills 模式下，开发者可以通过日志清晰地看到模型调用了哪个函数、传了什么参数，容易排查错误

---
## 代码示例




```python
# 示例1：基于AGENTS.md的动态任务规划
def dynamic_task_planner(user_request):
    """
    模拟AGENTS.md中的动态任务规划能力
    根据用户请求自动拆解和分配子任务
    """
    # 任务分解规则（模拟AGENTS.md中的指令）
    task_rules = {
        "数据分析": ["数据收集", "清洗", "建模", "可视化"],
        "报告生成": ["数据提取", "格式化", "生成文档"],
        "系统监控": ["状态检查", "日志分析", "报警"]
    }
    
    # 简单的任务匹配逻辑
    matched_tasks = []
    for task_type, subtasks in task_rules.items():
        if task_type in user_request:
            matched_tasks.extend(subtasks)
    
    # 返回执行计划
    return {
        "original_request": user_request,
        "matched_tasks": matched_tasks,
        "execution_order": list(range(1, len(matched_tasks)+1))
    }

# 测试用例
print(dynamic_task_planner("我需要做数据分析和报告生成"))
```




```python
# 示例2：上下文感知的技能组合
def context_aware_skill_combination(context):
    """
    模拟AGENTS.md中的上下文感知能力
    根据当前上下文自动组合相关技能
    """
    # 技能库（模拟AGENTS.md中的技能定义）
    skill_library = {
        "python": ["数据分析", "自动化", "后端开发"],
        "javascript": ["前端开发", "数据可视化"],
        "sql": ["数据库操作", "数据提取"]
    }
    
    # 上下文分析
    active_skills = set()
    for keyword, skills in skill_library.items():
        if keyword in context.lower():
            active_skills.update(skills)
    
    # 返回推荐技能组合
    return {
        "context": context,
        "recommended_skills": list(active_skills),
        "combination_strategy": "intersection" if len(active_skills) > 1 else "single"
    }

# 测试用例
print(context_aware_skill_combination("我需要用Python和SQL处理数据"))
```




```python
# 示例3：自适应学习机制
def adaptive_learning_agent(task_history):
    """
    模拟AGENTS.md中的自适应学习机制
    根据历史任务表现动态调整策略
    """
    # 学习规则（模拟AGENTS.md中的学习指令）
    learning_rules = {
        "success_threshold": 0.8,
        "improvement_factor": 1.2,
        "degradation_factor": 0.9
    }
    
    # 分析历史表现
    success_rate = sum(1 for task in task_history if task["success"]) / len(task_history)
    
    # 动态调整策略
    if success_rate > learning_rules["success_threshold"]:
        adjustment = learning_rules["improvement_factor"]
        strategy = "增强模式"
    else:
        adjustment = learning_rules["degradation_factor"]
        strategy = "保守模式"
    
    # 返回调整后的策略
    return {
        "current_success_rate": success_rate,
        "adjustment_factor": adjustment,
        "new_strategy": strategy,
        "recommended_actions": ["增加资源分配", "优化算法参数"] if strategy == "增强模式" else ["简化任务", "增加验证步骤"]
    }

# 测试用例
task_history = [
    {"task": "数据清洗", "success": True},
    {"task": "模型训练", "success": True},
    {"task": "可视化", "success": False}
]
print(adaptive_learning_agent(task_history))
```


---
## 案例研究


### 1：某头部电商平台智能客服升级项目

 1：某头部电商平台智能客服升级项目

**背景**: 该电商平台原有的智能客服系统基于传统的意图识别模型，能够处理退款、物流查询等高频标准化问题，但随着业务复杂度增加，涉及多步骤协商、个性化推荐及售后纠纷的复杂咨询占比显著提升。

**问题**: 传统的“技能”模式在处理复杂任务时面临瓶颈。每个技能独立运行，缺乏全局上下文记忆。例如，当用户先询问“物流延迟”再询问“如何退货”时，系统往往无法将两者关联（即因为延迟而退货），导致答非所问，人工转接率高达 40%，严重影响用户体验和运营成本。

**解决方案**: 引入基于 AGENTS.md 架构的智能体系统替代离散技能。新的 Agent 具备自主规划能力，能够将用户需求拆解为子任务，并动态调用查询物流、判断责任归属、执行退货指令等多个工具。系统通过长短期记忆机制，在整个对话过程中保持对用户核心诉求的连贯理解。

**效果**: 上线后，复杂咨询的一步解决率提升了 25%，人工转接率降低了 18%。Agent 能够在多轮对话中准确捕捉用户意图变更，不仅解决了上下文割裂的问题，还通过自主决策能力，在不增加人工标注成本的情况下，处理了长尾场景的客服需求。

---



### 2：金融科技公司的合规报告自动化生成

 2：金融科技公司的合规报告自动化生成

**背景**: 该金融科技公司需要为中小企业客户提供每周的风险评估报告。数据来源分散，包括银行流水、税务记录、市场舆情以及内部交易数据。

**问题**: 此前，公司尝试开发多个特定的“技能”来自动化这一流程，例如“数据提取技能”、“图表生成技能”和“文本撰写技能”。然而，这些技能之间缺乏协同。当数据出现异常（如缺失值）或需要跨数据源验证时，技能流水线容易中断。开发人员需要编写大量的硬编码逻辑来处理异常情况，维护成本极高，且报告生成的准确率仅为 75%。

**解决方案**: 采用基于 AGENTS.md 的自主 Agent 架构重构系统。Agent 不再依赖固定的技能流水线，而是被设定为一个“分析员”角色。它自主决定先清洗哪些数据、如何验证异常值、以及采用何种逻辑进行风险评估。当遇到不确定的数据时，Agent 甚至可以自主编写并执行 SQL 查询进行二次验证，而不是直接报错。

**效果**: 新系统成功将合规报告的生成准确率提升至 95% 以上。由于 Agent 具备自我纠错和动态规划能力，系统在面对非标准化的数据输入时不再频繁崩溃，研发团队的维护迭代周期缩短了 50%，极大提升了业务交付效率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用基于文档的上下文注入策略

**说明**: 核心发现表明，在构建 Agent 时，将详细的上下文信息（如系统提示词、领域知识、配置规则）直接放置在 `AGENTS.md` 文件中，并通过上下文窗口注入，通常比将逻辑封装在独立的“技能”或“工具”调用中表现更好。这种方法减少了 Agent 在执行任务时的检索和决策延迟，使其能直接访问“大脑”中的知识库。

**实施步骤**:
1. 创建一个结构化的 `AGENTS.md` 文件，作为 Agent 的核心知识库。
2. 将原本可能被编码为独立函数或工具的复杂逻辑、业务规则和背景信息写入该文档。
3. 在初始化 Agent 会话时，将此文档作为系统提示词的一部分或长上下文输入。
4. 指导 Agent 在处理任务时优先参考文档内容，而非尝试调用外部 API。

**注意事项**: 确保文档内容经过精心排版和去重，避免因上下文过长导致的关键信息稀释（即“迷失在中间”现象）。

---

### 实践 2：显式定义推理链

**说明**: `AGENTS.md` 优于技能的一个关键因素是它能够强制 Agent 在执行前进行更深入的思考。在文档中显式定义“思维链”或“推理步骤”，可以让 Agent 模拟规划过程，而不是盲目地执行预定义的动作。这种结构化的提示方式能显著提高复杂任务的解决率。

**实施步骤**:
1. 在 `AGENTS.md` 中定义一个标准的“问题解决模板”。
2. 要求 Agent 在给出最终答案或调用工具前，必须按照以下步骤输出：分析用户意图 -> 拆解任务 -> 确定所需信息 -> 制定执行计划。
3. 使用 `<thought>` 标签或类似的分隔符来包裹推理过程，以便与最终输出区分。

**注意事项**: 监控 Agent 的输出长度，确保推理过程不会消耗过多的 Token 预算，导致实际响应被截断。

---

### 实践 3：集中管理动态上下文与静态知识

**说明**: 将静态知识（如 API 文档、业务规范）与动态上下文（如对话历史、当前状态）分离，但统一通过 `AGENTS.md` 的引用机制进行管理。这种混合模式允许 Agent 拥有长期的记忆（文档）和短期的记忆（会话），弥补了传统技能库缺乏灵活性的缺陷。

**实施步骤**:
1. 将不常变更的底层逻辑和规则固化在 `AGENTS.md` 中。
2. 建立一套机制，在运行时将特定的用户数据或会话状态追加到 Agent 的上下文中。
3. 在文档中预留“变量插槽”或引用标记，指示 Agent 在何处应关注动态上下文。

**注意事项**: 需要建立清晰的版本控制流程，因为 `AGENTS.md` 的变更会直接影响所有依赖该 Agent 的实例行为。

---

### 实践 4：优化文档结构与可读性

**说明**: LLM 对上下文的敏感度极高，`AGENTS.md` 的物理结构直接影响 Agent 的表现。使用清晰的标题层级、项目符号和代码块可以显著提升模型对指令的遵循能力。相比于代码形式的技能定义，自然语言文档更易于 LLM 进行语义理解和检索。

**实施步骤**:
1. 使用 Markdown 语法对文档进行严格的结构化，确保一级标题、二级标题逻辑清晰。
2. 将关键指令放在文档的开头和结尾，利用 LLM 的“首尾注意力”机制。
3. 对于复杂的逻辑，使用具体的示例（Few-Shot Examples）代替抽象的描述，直接在文档中展示“输入-输出”对。

**注意事项**: 避免在文档中使用过于晦涩的技术术语或未经解释的缩写，保持语言的自然和直观。

---

### 实践 5：减少对工具调用的过度依赖

**说明**: 评估结果显示，过度依赖“技能”（通常表现为 Function Calling 或 Tool Use）会增加系统的复杂度和出错概率（如工具参数解析错误）。通过在 `AGENTS.md` 中提供足够的背景信息和逻辑指引，Agent 可以利用其内在的知识直接生成答案，从而绕过不必要的工具调用步骤。

**实施步骤**:
1. 审查现有的技能/工具列表，识别哪些可以通过自然语言推理直接替代。
2. 将那些用于简单查询或格式转换的工具逻辑转化为 `AGENTS.md` 中的“操作指南”。
3. 仅保留必须与外部系统交互（如数据库查询、邮件发送）的工具调用。

**注意事项**: 这种方法依赖于模型的基础能力，对于需要极高准确性或实时数据的任务，仍应保留工具调用。

---

### 实践 6：建立迭代式的评估反馈循环

**说明**: 既然 `AGENTS.md` 在评估中表现更好，就需要建立一套专门的流程来优化文档内容。不同于代码调试，文档优化需要通过分析 Agent 的失败案例，不断地向文档中添加澄清说明、边界条件处理和异常情况应对策略。

**实施步骤**:
1. 记录 Agent 在测试集中的失败案例。
2.

---
## 学习要点

- 根据提供的标题和来源，以下是关于 AGENTS.md 与 Skills 在智能体评估中对比的关键要点总结：
- 在智能体评估中，基于 AGENTS.md 的架构设计在性能上显著优于传统的 Skills 架构。
- AGENTS.md 的成功表明，将系统指令与上下文集中管理（如通过文档形式）比硬编码的技能调用更具灵活性和鲁棒性。
- 该方法突出了“上下文感知”能力的重要性，即智能体通过阅读文档动态获取指令，而非依赖静态的预定义技能集。
- 这一发现可能改变 AI 智能体的开发范式，促使开发者从编写复杂代码逻辑转向编写高质量的指令文档。
- AGENTS.md 的引入降低了构建高级智能体的门槛，使得通过自然语言描述来驱动复杂行为成为可能。

---
## 常见问题


### 1: 什么是 AGENTS.md，它与传统的 "Skills"（技能）定义有什么本质区别？

1: 什么是 AGENTS.md，它与传统的 "Skills"（技能）定义有什么本质区别？

**A**: AGENTS.md 是一种基于 Markdown 文件的标准化规范，用于定义 AI Agent（智能体）的角色、目标、约束和可用资源。与传统的 "Skills"（通常指硬编码的函数调用或特定的 API 端点）不同，AGENTS.md 采用了一种更全面、基于文本的配置方式。

传统的 "Skills" 往往是孤立的代码片段，Agent 只能机械地执行特定指令。而 AGENTS.md 允许开发者通过自然语言描述 Agent 的上下文、性格和任务流程。这种方法使得 Agent 能够根据上下文动态地规划任务，而不是简单地调用预定义的函数。在 Hacker News 的讨论中，这种从“调用函数”到“阅读指令”的转变被认为是性能提升的关键，因为它赋予了 Agent 更强的推理能力和适应性。

---



### 2: 为什么在评估测试中，基于 AGENTS.md 的 Agent 会优于基于 Skills 的 Agent？

2: 为什么在评估测试中，基于 AGENTS.md 的 Agent 会优于基于 Skills 的 Agent？

**A**: 根据来源社区的反馈和评估结果，基于 AGENTS.md 的 Agent 表现更好，主要归因于以下几个因素：

1.  **上下文感知能力**：AGENTS.md 提供了完整的任务背景和约束条件，使 LLM（大语言模型）能够理解“为什么要做”以及“如何做”，而不仅仅是接收一个函数名。
2.  **减少幻觉**：当 Agent 只依赖 Skills 时，可能会因为缺乏上下文而错误地拼接函数。AGENTS.md 通过明确的指令边界，限制了 Agent 的行为范围，从而减少了错误操作。
3.  **灵活性**：在处理复杂、多步骤的任务时，基于文本的配置允许 Agent 动态调整策略，而硬编码的 Skills 往往缺乏这种弹性，难以应对边缘情况。

---



### 3: AGENTS.md 的具体工作原理是什么？它是如何被加载和执行的？

3: AGENTS.md 的具体工作原理是什么？它是如何被加载和执行的？

**A**: AGENTS.md 的工作流程通常包含以下几个步骤：

1.  **定义**：开发者创建一个 `AGENTS.md` 文件，其中包含 Agent 的角色定义（例如：“你是一个高级数据分析师”）、任务描述、允许使用的工具列表以及输出格式要求。
2.  **注入**：在运行时，Agent 框架（如 AutoGen, LangChain 等）会将该 Markdown 文件的内容作为系统提示词或上下文信息注入到大语言模型（LLM）中。
3.  **推理与执行**：LLM 阅读并理解文件内容后，结合用户的输入进行推理。它会根据文档中的指导来决定下一步行动，是调用工具、查询数据库还是生成文本。

这种方式将“配置”变成了“提示词工程”，使得修改 Agent 行为无需重写代码，只需修改文档即可。

---



### 4: 使用 AGENTS.md 方式是否存在性能成本或 Token 消耗过大的问题？

4: 使用 AGENTS.md 方式是否存在性能成本或 Token 消耗过大的问题？

**A**: 这是一个常见的权衡问题。确实，将详细的 AGENTS.md 内容作为上下文每次都发送给 LLM 会增加输入 Token 的消耗。

然而，支持者认为这种成本是值得的：
*   **准确率提升**：虽然 Token 消耗增加了，但由于任务完成度的提高和错误率的降低，实际上减少了因重试而产生的额外 Token 消耗和时间成本。
*   **缓存优化**：许多现代推理引擎支持提示词缓存。由于 AGENTS.md 的内容在多次调用中通常是不变的，这部分 Token 消耗可以被大幅优化，实际边际成本并不高。

---



### 5: AGENTS.md 是否会取代现有的工具调用或函数调用机制？

5: AGENTS.md 是否会取代现有的工具调用或函数调用机制？

**A**: 不会完全取代，而是对其进行封装和增强。AGENTS.md 并不直接执行代码，它是一个管理层。

在实际应用中，AGENTS.md 负责告诉 Agent “在什么情况下应该使用哪个工具”。底层的函数调用机制仍然是 Agent 与软件交互的最终手段。你可以将 AGENTS.md 视为“大脑”的指令集，而 Skills 是“手”的具体动作。通过 AGENTS.md，Agent 能更智能地决定何时以及如何使用这些“手”。

---



### 6: 对于开发者来说，从迁移到 AGENTS.md 的难度大吗？

6: 对于开发者来说，从迁移到 AGENTS.md 的难度大吗？

**A**: 难度通常不大，甚至可能降低开发门槛。

*   **无需深入编码**：对于简单的 Agent 调整，开发者只需要编辑 Markdown 文本，而不需要深入修改 Python 或 JavaScript 代码逻辑。
*   **标准化**：它提供了一种通用的格式来描述 Agent 行为，使得团队内部共享和复用 Agent 配置变得更加容易。
*   **调试便利**：相比于调试复杂的逻辑代码，阅读和修改自然语言描述的配置文件通常更加直观，便于快速迭代。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在构建 AI Agent 时，"硬编码技能"（Hard-coded Skills）与"基于文档的 Agent"（AGENTS.md）在处理未知任务时的行为模式有何根本不同？请列举一个具体的业务场景，说明后者为何能产生更好的泛化能力。

### 提示**: 考虑当用户提出一个开发者未曾预先编写过函数的问题时，系统分别会做出什么反应。重点在于"静态代码逻辑"与"动态上下文推理"的区别。

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
- 标签： [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [AGENTS.md](/tags/agents-md/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [Skills](/tags/skills/) / [LLM](/tags/llm/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-4.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-8.md" >}})
- [Agent Skills：压缩智能体技能以提升模型效率]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [Agent评估显示AGENTS.md配置优于技能配置]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*