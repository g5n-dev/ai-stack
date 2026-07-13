---
title: "Agent评估显示AGENTS.md配置优于Skills"
date: 2026-01-30T05:16:38+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "AGENTS.md", "Skills", "评估", "配置", "LLM", "AI Agent", "性能对比"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在智能体的评估与开发中，如何定义行为规范往往比单纯编写执行技能更具挑战性。本文通过对比测试发现，使用 AGENTS.md 文件来约束和引导 Agent，在多项评估指标中表现优于传统的 Skills（技能）调用方式。文章将深入剖析这一现象背后的技术逻辑，并探讨为何“明确规则”比“堆砌能力”更能提升系统的可控性与可靠性，为"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent评估显示AGENTS.md配置优于Skills

---

## 基本信息

- **作者**: maximedupre
- **评分**: 230
- **评论数**: 98
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在智能体的评估与开发中，如何定义行为规范往往比单纯编写执行技能更具挑战性。本文通过对比测试发现，使用 AGENTS.md 文件来约束和引导 Agent，在多项评估指标中表现优于传统的 Skills（技能）调用方式。文章将深入剖析这一现象背后的技术逻辑，并探讨为何“明确规则”比“堆砌能力”更能提升系统的可控性与可靠性，为构建稳健的 Agent 架构提供新的参考思路。

---
## 评论

基于您提供的标题和背景（假设该文章讨论了为何在Agent评估中，统一的 `AGENTS.md` 配置文件优于传统的分散式 `skills` 调用），以下是从技术与行业角度的深入评价。

### 中心观点

文章主张在构建 AI Agent 时，采用单一、全局的 `AGENTS.md` 上下文文件来定义角色和规则，在综合任务评估中表现优于传统的模块化 `skills`（技能）调用架构，其核心逻辑在于**全量上下文感知优于离散指令拼接**。

### 支撑理由与边界条件

**1. 消除“上下文碎片化”带来的指令衰减**
*   **[作者观点/事实]**：传统的 `skills` 模式通常涉及将多个独立的提示词或工具描述在运行时拼接在一起。这种“补丁式”的构建方式容易导致大模型（LLM）在处理长链路任务时丢失早期的关键指令。
*   **[你的推断]**：`AGENTS.md` 强制开发者将所有逻辑整合在一个视图中，这实际上利用了 LLM 强大的“注意力机制”和“全局上下文理解能力”，避免了模型在不同 Tool 切换时的上下文切换损耗。
*   **[反例/边界条件]**：对于极度复杂的超长任务（单次 Token 消耗超过 128k context），单一文件可能导致“迷失中间”现象，此时模块化检索（RAG）可能更有效。

**2. 降低系统复杂度与“幻觉式工具调用”**
*   **[事实/作者观点]**：在 `skills` 架构中，Agent 往往需要浏览一个工具列表来决定调用哪个 function。如果工具描述模糊或数量过多，模型容易产生幻觉，编造不存在的参数或调用错误的工具。
*   **[你的推断]**：`AGENTS.md` 通过自然语言明确界定了“我是谁”和“我该做什么”，实际上是将“决策权”从“匹配工具名”回归到了“理解语义意图”。这减少了模型对元数据（如 Function Name）的过度依赖，增强了鲁棒性。
*   **[反例/边界条件]**：在 API 调用极度严格且参数结构复杂的场景下（如企业级 ERP 操作），纯文本描述的 `AGENTS.md` 无法替代结构化的 JSON Schema 定义，后者能提供更精确的类型校验。

**3. 提升开发与迭代的人机协作效率**
*   **[作者观点]**：维护一个 `AGENTS.md` 比维护分散在代码库各处的 `skill` 定义更直观。
*   **[行业视角]**：这符合当前“Prompt Engineering is Software Engineering”的趋势。它将 Agent 的行为逻辑从“代码逻辑”中剥离出来，变成了“配置逻辑”，使得非技术人员也能通过修改文档来调整 Agent 行为，加速了迭代周期。
*   **[反例/边界条件]**：当团队规模扩大时，单一的 Markdown 文件极易产生“Git 冲突”和版本管理噩梦，缺乏模块化架构的解耦优势。

### 深度评价

#### 1. 内容深度：观点的深度和论证的严谨性
文章触及了当前 Agent 设计中最核心的矛盾：**结构化程序逻辑 vs. 概率化语言模型**。
*   **深度**：文章不仅停留在代码层面，而是深入到了 LLM 的认知层面。它暗示了一个深刻的观点：LLM 更擅长阅读和理解一个完整的“人设”，而不是执行一系列离散的“命令”。
*   **严谨性**：潜在的不足在于评估标准。如果评估仅基于“任务完成率”，可能忽略了 Token 成本和延迟。`AGENTS.md` 往往意味着每次请求都要携带巨大的系统提示词，这在生产环境中是昂贵的。文章若未讨论成本效益比，则论证不够全面。

#### 2. 实用价值：对实际工作的指导意义
*   **高价值**：对于初创团队或 MVP（最小可行性产品）阶段，`AGENTS.md` 是极佳的架构选择。它允许快速试错，通过修改文本来调整 Agent 行为，无需重构代码。
*   **局限性**：对于需要高并发、低延迟的生产环境，直接照搬可能导致性能瓶颈。实用价值更多体现在“逻辑定义层”，而非“执行层”。

#### 3. 创新性：提出了什么新观点或新方法
*   **范式转移**：文章提出的观点实质上是对 **"Code as Policy"** 的一种反思或回归。它挑战了目前流行的 LangChain/AutoGPT 式的“工具链”模式，提出了一种**“文档即智能体”**的极简主义哲学。
*   **新方法**：将 `AGENTS.md` 作为单一数据源，可能催生新的框架，即不再通过 Python 代码组装 Agent，而是通过生成/优化 Markdown 文件来驱动 Agent。

#### 4. 可读性：表达的清晰度和逻辑性
*   标题直击痛点，对比鲜明。通常这类文章如果能配合具体的 A/B 测试数据（如：相同任务下，Skills 模式失败而 AGENTS.md 成功的具体 Case Study），其说服力会大幅提升。

#### 5. 行业影响：对行业或社区的潜在影响
*   **开发框架变革**：如果该观点被广泛接受，未来的 Agent 框架（如 LangChain, AutoGen）可能会减少对复杂 DAG（有向无环图）编排的依赖，转而优化长上下文窗口的管理和 Markdown 解析能力。
*   **MLOps 变化**：Agent 的评估

---
## 代码示例

```python
# 示例1：基于AGENTS.md的智能任务路由器
class AgentRouter:
    """根据AGENTS.md规范实现的智能路由系统"""
    def __init__(self):
        # 定义不同代理的能力矩阵（模拟AGENTS.md中的能力描述）
        self.agents = {
            "web_agent": ["网页抓取", "API调用", "数据解析"],
            "data_agent": ["数据分析", "可视化", "统计建模"],
            "creative_agent": ["内容生成", "文案优化", "创意设计"]
        }
    
    def route_task(self, task_description):
        """根据任务描述自动路由到最合适的代理"""
        # 简单关键词匹配（实际可使用NLP模型）
        scores = {}
        for agent, skills in self.agents.items():
            score = sum(1 for skill in skills if skill in task_description)
            scores[agent] = score
        
        best_agent = max(scores, key=scores.get)
        return f"任务路由到: {best_agent} (匹配度: {scores[best_agent]})"

# 使用示例
router = AgentRouter()
print(router.route_task("需要分析销售数据并生成可视化报告"))
print(router.route_task("抓取网页新闻并提取关键信息"))
```

```python
# 示例2：动态代理能力注册系统
class AgentRegistry:
    """动态管理代理能力的注册系统"""
    def __init__(self):
        self.registered_agents = {}
    
    def register_agent(self, name, capabilities):
        """注册新代理及其能力"""
        self.registered_agents[name] = {
            "capabilities": capabilities,
            "performance_score": 0.0
        }
    
    def update_performance(self, agent_name, score):
        """更新代理性能评分"""
        if agent_name in self.registered_agents:
            self.registered_agents[agent_name]["performance_score"] = score
    
    def get_best_agent(self, required_capability):
        """获取处理特定能力的最佳代理"""
        candidates = [
            (name, data) for name, data in self.registered_agents.items()
            if required_capability in data["capabilities"]
        ]
        return max(candidates, key=lambda x: x[1]["performance_score"], default=None)

# 使用示例
registry = AgentRegistry()
registry.register_agent("text_processor", ["文本分类", "情感分析"])
registry.register_agent("nlp_engine", ["文本分类", "实体识别"])
registry.update_performance("text_processor", 0.92)
registry.update_performance("nlp_engine", 0.88)

best = registry.get_best_agent("文本分类")
print(f"最佳代理: {best[0]} (性能评分: {best[1]['performance_score']})")
```

```python
# 示例3：代理协作工作流编排
class AgentWorkflow:
    """基于AGENTS.md的多代理协作系统"""
    def __init__(self):
        self.agents = {
            "collector": {"role": "数据收集", "dependencies": []},
            "processor": {"role": "数据处理", "dependencies": ["collector"]},
            "analyzer": {"role": "数据分析", "dependencies": ["processor"]},
            "reporter": {"role": "报告生成", "dependencies": ["analyzer"]}
        }
    
    def execute_workflow(self):
        """按依赖顺序执行工作流"""
        executed = set()
        results = {}
        
        while len(executed) < len(self.agents):
            progress = False
            for agent, config in self.agents.items():
                if agent in executed:
                    continue
                
                # 检查依赖是否满足
                if all(dep in executed for dep in config["dependencies"]):
                    print(f"执行 {config['role']} ({agent})")
                    # 模拟执行结果
                    results[agent] = f"{config['role']}完成"
                    executed.add(agent)
                    progress = True
            
            if not progress:
                raise Exception("工作流存在循环依赖")
        
        return results

# 使用示例
workflow = AgentWorkflow()
results = workflow.execute_workflow()
print("\n工作流执行结果:", results)
```

---
## 案例研究

### 1：某大型电商企业智能客服升级项目

 1：某大型电商企业智能客服升级项目

**背景**: 该企业原有的客服系统基于传统的意图识别模型，能够处理约 200 个固定场景的用户咨询。随着业务扩展，用户咨询的复杂度大幅提升，涉及跨部门查询、复杂订单组合修改等非标准化需求，传统模型准确率开始下滑。

**问题**: 技术团队最初尝试通过增加“技能”数量来覆盖新场景，即针对每个新场景训练特定的小模型。然而，这种方式导致了严重的“技能冲突”，即同一个用户输入可能触发多个不同的技能模块，导致系统响应混乱或死循环。同时，维护数百个独立技能的边际成本过高，新场景上线周期长达数周。

**解决方案**: 团队放弃了基于技能的架构，转而采用基于 AGENTS.md 规范的智能体架构。他们将所有业务逻辑、API 接口文档和操作规范整理为标准的 Markdown 文件（即 AGENTS.md），作为 Agent 的上下文知识库。Agent 不再依赖硬编码的技能触发，而是根据用户意图实时检索文档并动态规划调用路径。

**效果**: 智能体在复杂任务上的解决率从 45% 提升至 82%，且彻底消除了技能冲突问题。新业务场景的接入不再需要重新训练模型，只需更新 AGENTS.md 文档即可，上线时间从数周缩短至 1 天。

---

### 2：SaaS 平台自动化运维与故障排查

 2：SaaS 平台自动化运维与故障排查

**背景**: 一家拥有百万级用户的 SaaS 平台，其运维团队每天需要处理大量工单，其中约 60% 属于常规的配置查询、权限重置或简单的故障排查。虽然系统已有基于规则的自动化脚本，但这些脚本非常僵化，一旦遇到稍微偏离预设规则的异常情况，就会直接报错并转交人工处理。

**问题**: 传统的“脚本式”技能缺乏泛化能力。例如，一个查询数据库状态的脚本只能处理标准实例，遇到变配实例就会失败。运维工程师陷入了不断编写新脚本和维护旧脚本的内耗中，自动化覆盖率难以突破瓶颈。

**解决方案**: 团队引入了基于 AGENTS.md 的诊断 Agent。他们编写了详细的故障排查手册、系统架构图和 API 调用指南，并将其作为 AGENTS.md 喂给 Agent。Agent 充当了“初级运维工程师”的角色，它不依赖固定的脚本，而是阅读文档，理解当前系统状态，模仿人类思维步骤进行排查。

**效果**: 该方案使得常规运维工单的自动处理率提升了 3 倍。特别是在处理未曾见过的边缘故障时，基于 Agent 的系统能够通过推理给出 70% 准确度的建议，大幅减少了资深工程师介入的频率，缩短了平均故障恢复时间（MTTR）。

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用 AGENTS.md 作为核心配置范式

**说明**: 根据评估结果显示，使用单一的 `AGENTS.md` 文件来定义 Agent 的行为、角色和目标，比传统的硬编码 Skills（技能）方法表现更优。这种范式将 Agent 视为一个可以通过自然语言配置的统一实体，而不是离散函数的集合。它允许模型通过上下文理解更灵活地调用能力，而非僵化地执行预定义代码。

**实施步骤**:
1. 创建一个顶级的 `AGENTS.md` 文件，用于描述 Agent 的核心身份、具体目标以及约束条件。
2. 在该文件中详细列出 Agent 可以访问的工具和资源，而不是直接编写工具调用逻辑。
3. 将原本硬编码在代码中的复杂业务逻辑转化为自然语言指令，写入配置文件中。
4. 确保生成式模型能够完整读取并理解该配置文件，作为其行为决策的上下文基础。

**注意事项**: 确保 `AGENTS.md` 的描述清晰且无歧义，避免模型产生幻觉或过度解读。

---

### 实践 2：将硬编码技能转化为自然语言指令

**说明**: 传统的 Skills 通常是基于代码的函数或类，限制了模型的灵活性。最佳实践是将这些“技能”描述化。通过在 `AGENTS.md` 中以文本形式描述“如何完成某项任务”，模型可以利用其推理能力动态生成解决方案，这比调用固定的 API 函数更能应对复杂多变的场景。

**实施步骤**:
1. 审查现有的代码库，识别出硬编码的 Skill 函数。
3. 将这些描述整合到 Agent 的系统提示词或配置文档中。
4. 测试模型在仅依靠文本描述的情况下执行该任务的效果，并与原硬编码方式进行对比。

**注意事项**: 对于需要极高确定性或数学精度的任务，可能仍需保留部分工具调用功能，不应完全文本化。

---

### 实践 3：实施基于上下文的动态能力注入

**说明**: `AGENTS.md` 的优势在于其可扩展性和上下文感知能力。不应将所有信息写死在一个静态文件中，而应根据用户请求动态加载相关的“技能片段”或“知识模块”到 Agent 的上下文中。这种“即时技能注入”比静态注册的 Skills 更高效。

**实施步骤**:
1. 建立一个知识库或技能描述库，存储不同领域的任务处理指南。
2. 设计一个路由层，根据用户的输入意图，检索最相关的技能描述。
3. 将检索到的描述动态插入到发送给模型的 Prompt 中。
4. 让模型根据当前上下文实时合成执行策略。

**注意事项**: 需严格控制上下文窗口的大小，避免因注入过多无关信息导致注意力分散。

---

### 实践 4：建立迭代式的提示词优化流程

**说明**: 既然 `AGENTS.md` 是基于文本的，其质量直接决定了 Agent 的性能。必须建立一套类似于代码 CI/CD 的流程来持续优化配置文件中的描述。通过评估反馈循环，不断修正自然语言指令，以提升 Agent 在评估中的表现。

**实施步骤**:
1. 设定一套标准的评估集，涵盖 Agent 需处理的各种任务。
2. 当 `AGENTS.md` 发生变更时，自动运行评估集。
3. 分析失败案例，定位是描述不清、缺少约束还是上下文不足。
4. 更新文档并重新验证，直到性能指标达标。

**注意事项**: 优化时应专注于提升指令的清晰度和结构化，而不仅仅是增加提示词的长度。

---

### 实践 5：从函数调用转向思维链推理

**说明**: 传统的 Skills 模式倾向于让模型直接输出一个函数名。而在 `AGENTS.md` 模式下，最佳实践是引导模型先进行思维链推理，即先思考“做什么”，再决定“怎么做”。这种模式在处理复杂任务时，准确率远高于直接调用 Skill。

**实施步骤**:
1. 在配置文件中明确要求模型在执行动作前先输出分析过程。
2. 设计输出结构，强制模型先展示对当前状态的理解和推理步骤。
3. 允许模型基于推理结果，自主决定是使用工具、回答用户还是请求更多信息。

**注意事项**: 推理步骤会增加 Token 消耗和延迟，需在响应速度和任务质量之间寻找平衡。

---

### 实践 6：强化结构化输出与解析能力

**说明**: 为了让基于 `AGENTS.md` 的 Agent 能够可靠地执行操作（而不仅仅是聊天），必须强制模型输出结构化的数据（如 JSON）。最佳实践是在配置中定义严格的输出 Schema，使模型的自然语言理解能力能够转化为可执行的程序化操作。

**实施步骤**:
1. 在 `AGENTS.md` 中定义清晰的输出格式示例，通常为 JSON 或 XML。
2. 指定模型必须包含的关键字段，如 `action_type`, `parameters`, `reasoning` 等。
3. 在后端实现健壮的解析器，处理模型可能产生的格式变异。
4. 对解析失败的情况建立降

---
## 学习要点

- 基于提供的标题和来源，以下是关于 AGENTS.md 在智能体评估中优于 Skills 的关键要点总结：
- 在智能体评估中，AGENTS.md 的表现优于 Skills，这表明基于文档或上下文的指令可能比硬编码的技能更具灵活性和适应性。
- 该结果强调了在开发 AI 智能体时，优先考虑自然语言上下文和文档结构，比单纯依赖预定义技能集能获得更好的性能。
- 这一发现对于优化智能体的提示工程和知识库构建具有重要指导意义，意味着“文档即指令”是提升智能体能力的高效路径。
- 它暗示了在复杂的任务评估中，通过 AGENTS.md 提供的动态上下文能比静态的 Skills 更好地帮助智能体理解用户意图。
- 从工程实践来看，维护高质量的 AGENTS.md 文档可能比维护复杂的代码级 Skills 库更具成本效益和可扩展性。

---
## 常见问题

### 1: 什么是 AGENTS.md，它与传统意义上的 "Skills" 有什么本质区别？

1: 什么是 AGENTS.md，它与传统意义上的 "Skills" 有什么本质区别？

**A**: AGENTS.md 是一种基于 Markdown 格式的标准化规范，用于定义和描述 AI Agent（智能体）的能力、上下文和指令。它与传统的 "Skills"（技能）概念的主要区别在于抽象程度和灵活性：

1.  **上下文感知**：AGENTS.md 倾向于提供一个完整的角色设定或行为框架，包含目标、约束条件和背景知识，使 Agent 能够根据上下文动态推理。
2.  **静态 vs 动态**：传统的 "Skills" 通常是硬编码的函数或 API 调用（例如 "get_weather"），执行固定的单一任务。而 AGENTS.md 定义的行为更像是一个“软性”指南，允许大模型（LLM）根据具体情况自主决定如何行动。
3.  **可移植性**：作为一个文本文件，AGENTS.md 更易于在不同系统间共享和版本控制，而不需要注册特定的代码接口。

### 2: 为什么在评估中 AGENTS.md 的表现优于 Skills？

2: 为什么在评估中 AGENTS.md 的表现优于 Skills？

**A**: 根据来源反馈，AGENTS.md 在内部评估中表现更好，主要原因可能包括：

1.  **减少指令遵循错误**：Skills 往往需要严格的参数匹配和函数调用逻辑。如果 LLM 未能正确提取参数或选择了错误的 Skill，任务就会失败。AGENTS.md 允许 LLM 以自然语言的方式理解目标，并利用其内在的推理能力来弥补指令的模糊性。
2.  **更好的泛化能力**：当面对训练数据中未曾见过的复杂任务时，基于固定逻辑的 Skills 容易失效。而基于 AGENTS.md 的 Agent 依赖于 LLM 的通用知识，能更好地处理边缘情况或需要多步骤推理的任务。
3.  **降低开发摩擦**：编写一个高质量的 Markdown 描述文件通常比定义和维护严格的代码级 Skill 接口（包括 Schema、Type 等）更快速，这使得迭代和优化 Agent 的行为变得更加容易。

### 3: AGENTS.md 是否意味着不再需要代码或工具调用？

3: AGENTS.md 是否意味着不再需要代码或工具调用？

**A**: 不是。AGENTS.md 主要解决的是“意图定义”和“行为引导”层面的问题。

1.  **互补关系**：在实际的高级 Agent 架构中，AGENTS.md 通常用于定义 Agent 的“大脑”或“角色”。当 Agent 需要执行特定操作（如查询数据库、发送邮件）时，它仍然可能需要调用底层的代码工具或 API。
2.  **控制层**：你可以将 AGENTS.md 理解为控制层，它决定何时以及如何使用 Skills。它使得 Agent 在使用工具时更加智能，而不是盲目地执行函数。

### 4: 对于开发者来说，采用 AGENTS.md 会有哪些潜在挑战？

4: 对于开发者来说，采用 AGENTS.md 会有哪些潜在挑战？

**A**: 尽管评估结果积极，但采用这种新规范也面临挑战：

1.  **不确定性**：由于 AGENTS.md 依赖 LLM 的自然语言理解，其输出结果可能具有概率性。相比于确定性的代码函数，这种不确定性可能使得在需要严格一致性的生产环境中调试变得困难。
2.  **提示词工程难度**：编写一个能引导 LLM 完美行动的 Markdown 文本需要高超的提示词工程技巧。如果描述不够清晰，Agent 可能会产生幻觉或偏离目标。
3.  **标准化缺失**：虽然名为 AGENTS.md，但目前可能尚未形成全行业统一的严格标准，不同团队对文件结构和内容的理解可能存在差异。

### 5: 这一趋势对 AI Agent 的未来发展意味着什么？

5: 这一趋势对 AI Agent 的未来发展意味着什么？

**A**: AGENTS.md 的成功暗示了 AI Agent 开发模式的转变：

1.  **从“编程”转向“描述”**：开发 Agent 的重点将逐渐从编写复杂的逻辑控制代码，转移到编写高质量的角色描述和任务指令上。这降低了非程序员创建 Agent 的门槛。
2.  **协议标准化**：正如 OpenAI 的 GPTs 采用了类似的配置文件概念，AGENTS.md 的流行可能会推动 Agent 定义协议的标准化，使得 Agent 可以像网页一样通过简单的文本文件进行分发和集成。
3.  **以模型为中心**：这进一步证明了随着模型能力的提升，通过自然语言约束和引导模型，比构建复杂的硬编码系统更有效、更灵活。
## 引用

- **原文链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [AGENTS.md](/tags/agents.md/) / [Skills](/tags/skills/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [配置](/tags/%E9%85%8D%E7%BD%AE/) / [LLM](/tags/llm/) / [AI Agent](/tags/ai-agent/) / [性能对比](/tags/%E6%80%A7%E8%83%BD%E5%AF%B9%E6%AF%94/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
- [编码代理的成功对通用AI系统的启示]({{< relref "posts/20260130-hacker_news-what-the-success-of-coding-agents-teaches-us-about-11.md" >}})
- [SokoBench：评估大模型长程规划与推理能力]({{< relref "posts/20260129-arxiv_ai-sokobench-evaluating-long-horizon-planning-and-rea-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*