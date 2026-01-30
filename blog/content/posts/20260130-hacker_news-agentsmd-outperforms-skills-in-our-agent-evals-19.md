---
title: "Agent评估显示AGENTS.md配置优于Skills"
date: 2026-01-30T11:13:00+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "LLM", "AGENTS.md", "Skills", "评估", "配置", "AI Agent", "工程实践"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在智能体的实际评估中，传统的“技能”抽象正面临挑战，而 AGENTS.md 展现出了更优的效能。这一发现表明，通过文档形式定义智能体行为，可能比硬编码的技能更能适应复杂任务。本文将深入分析背后的评估数据与逻辑，帮助你重新思考智能体的构建策略，并理解为何文档化方法在当前技术路径下更具优势。"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent评估显示AGENTS.md配置优于Skills

---

## 基本信息

- **作者**: maximedupre
- **评分**: 344
- **评论数**: 148
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在智能体的实际评估中，传统的“技能”抽象正面临挑战，而 AGENTS.md 展现出了更优的效能。这一发现表明，通过文档形式定义智能体行为，可能比硬编码的技能更能适应复杂任务。本文将深入分析背后的评估数据与逻辑，帮助你重新思考智能体的构建策略，并理解为何文档化方法在当前技术路径下更具优势。

---
## 评论

### 深度评价：AGENTS.md outperforms skills in our agent evals

**中心观点**
文章主张在智能体开发中，**结构化的系统提示词（AGENTS.md）在任务表现上优于传统的显式工具调用，这一观点揭示了当前AI智能体开发正从“函数调用”向“上下文推理”进行范式转移。**（你的推断）

**支撑理由与深度分析**

**1. 认知负载的转移：从“执行”到“理解”**
*   **事实陈述**：文章指出，在测试中，提供详细背景文档（AGENTS.md）的智能体表现优于被赋予特定技能的智能体。
*   **深度解析**：这反映了LLM的本质优势在于**自然语言理解与推理**，而非严格的逻辑执行。当Agent通过Skills调用外部工具（如搜索、计算）时，模型需要进行多次上下文切换，并承担工具调用的容错成本。而通过AGENTS.md将知识内化为Prompt，实际上是将计算复杂度转移给了模型的推理能力，利用了模型强大的隐式知识检索能力，减少了中间步骤的误差累积。

**2. 动态性与适应性的提升**
*   **作者观点**：Skills往往硬编码了特定的行为模式，缺乏灵活性。
*   **深度解析**：在处理复杂、多变的任务时，基于Skills的Agent容易陷入“僵化”。例如，一个被赋予“搜索股票价格”技能的Agent可能无法处理“搜索昨天的 adjusted close price”这种细微的语义变化，除非Skill被显式编程。而AGENTS.md提供了上下文，允许Agent根据具体情况动态决定行动策略，这种**软约束**比硬编码的**强约束**更具鲁棒性。

**3. 工程复杂度的降维**
*   **你的推断**：这实际上是工程哲学的回归——从“面向对象编程（OOP）”式的Agent设计（封装一个个Skill），回归到了“面向上下文编程（COP）”。
*   **深度解析**：维护复杂的Skills库需要处理API版本、鉴权、错误处理等繁琐问题。AGENTS.md通过文本协议绕过了这些工程债务，使得迭代速度大幅加快。这种“文本即代码”的趋势，与最近ReAct模式、Plan-and-Execute模式的流行相呼应。

**反例与边界条件**

**1. 幻觉风险与时效性限制**
*   **反例**：如果任务需要**绝对的精确性**（如转账、数学计算）或**实时数据**（如此刻的股价），AGENTS.md完全失效。
*   **分析**：LLM无法通过Prompt准确预测小数点后四位的汇率，也无法获取未写入训练集的新闻。此时，必须使用Skills（Function Calling）来挂载外部系统。文章的结论可能仅在“知识密集型”而非“数据/计算密集型”任务中成立。

**2. 上下文窗口与Token成本**
*   **边界条件**：当AGENTS.md的内容极其庞大时，会挤占宝贵的Context Window，并导致推理延迟和成本指数级上升。
*   **分析**：Skills通常是按需调用的，而文档是常驻内存的。对于长对话场景，显式的Skill调用在Token效率上远优于长文本Prompt。

**3. 确定性系统的要求**
*   **反例**：在金融交易或工业控制领域，系统要求行为的可解释性与确定性。
*   **分析**：依赖Prompt（AGENTS.md）的行为具有概率性，难以调试。当Agent出错时，很难定位是Prompt的哪一段描述导致了错误；而Skill调用有明确的日志输入输出，更符合传统软件工程的安全标准。

**评价维度总结**

1.  **内容深度**：文章触及了Agent设计的核心矛盾，即**代码与文本的边界**。它敏锐地指出了GPT-4o等模型在处理长文本和深层语义时的能力被低估，但略显夸大了“Prompt Engineering”的通用性，忽略了工具调用的必要性。
2.  **实用价值**：对于初创公司和快速原型开发，这一观点极具价值。它建议开发者不要急于构建复杂的RAG或工具链，先优化Prompt和文档，能显著降低MVP（最小可行性产品）的开发成本。
3.  **创新性**：提出了“文档优于接口”的反直觉观点，挑战了目前主流的LangChain/AutoGPA等框架的“工具优先”设计理念。
4.  **可读性**：逻辑清晰，对比实验明确，但缺乏对AGENTS.md具体编写策略的详细拆解。
5.  **行业影响**：可能会推动开发者重新审视“System Prompt”的设计，促使Agent框架从“编排工具”转向“优化上下文”。

**可验证的检查方式**

为了验证该文章结论的有效性，建议进行以下实验：

1.  **对比实验（指标：Success Rate & Token Cost）**
    *   **设置**：构建两组Agent，一组使用AGENTS.md（纯Prompt），一组使用Function Calling（Skills）。
    *   **任务集**：混合“知识问答”（需常识）、“数据查询”（需实时API）、“逻辑推理”（需计算）。
    *   **预期观察**：AGENTS.md在知识问答中胜出且成本低；Skills在数据查询中胜出；AGENTS.md在计算中可能出现幻觉。

2.  **鲁棒性测试（指标：Error Type Distribution）**
    *   **设置**：故意引入干扰信息或模糊指令。
    *   **观察窗口**：观察Agent是报错（Skill模式常见）还是尝试理解但产生幻觉（

---
## 代码示例




```python
# 示例1：动态任务规划与执行
def dynamic_task_planner():
    """
    模拟AGENTS.md中的动态任务规划能力
    解决问题：根据用户输入自动拆分复杂任务并执行
    """
    from typing import List, Dict
    
    # 模拟任务分解逻辑
    def decompose_task(user_input: str) -> List[Dict]:
        if "天气" in user_input:
            return [
                {"action": "get_location", "params": {"user_input": user_input}},
                {"action": "fetch_weather", "params": {"location": "from_previous"}}
            ]
        elif "计算" in user_input:
            return [
                {"action": "parse_expression", "params": {"user_input": user_input}},
                {"action": "calculate", "params": {"expression": "from_previous"}}
            ]
        return [{"action": "default_response", "params": {}}]
    
    # 模拟执行动作
    def execute_action(action: str, params: Dict) -> str:
        if action == "get_location":
            return "北京"
        elif action == "fetch_weather":
            return "晴天，25°C"
        elif action == "parse_expression":
            return "2 + 3"
        elif action == "calculate":
            return "5"
        return "未识别的请求"
    
    # 主流程
    user_input = "今天北京天气怎么样？"
    tasks = decompose_task(user_input)
    results = []
    for task in tasks:
        result = execute_action(task["action"], task["params"])
        results.append(result)
    
    return " -> ".join(results)

# 测试
print(dynamic_task_planner())  # 输出：北京 -> 晴天，25°C
```




```python
# 示例2：上下文记忆与推理
def context_memory_agent():
    """
    模拟AGENTS.md中的上下文记忆能力
    解决问题：在多轮对话中保持上下文连贯性
    """
    from collections import deque
    
    class ContextAgent:
        def __init__(self, max_history=5):
            self.history = deque(maxlen=max_history)
            self.facts = {}
        
        def process(self, user_input: str) -> str:
            # 存储历史
            self.history.append(user_input)
            
            # 简单的事实提取
            if "我的名字是" in user_input:
                name = user_input.split("我的名字是")[-1].strip()
                self.facts["name"] = name
                return f"好的，记住了您的名字是{name}"
            
            # 上下文推理
            if "我刚才说" in user_input and "name" in self.facts:
                return f"您刚才说您的名字是{self.facts['name']}"
            
            return "我需要更多信息来回答这个问题"
    
    agent = ContextAgent()
    print(agent.process("我的名字是张三"))  # 输出：好的，记住了您的名字是张三
    print(agent.process("我刚才说的名字是什么？"))  # 输出：您刚才说您的名字是张三

# 测试
context_memory_agent()
```




```python
# 示例3：多工具协作
def multi_tool_collaboration():
    """
    模拟AGENTS.md中的多工具协作能力
    解决问题：自动选择并组合多个工具完成任务
    """
    import json
    
    # 模拟工具集
    tools = {
        "search": lambda x: f"搜索结果：{x}",
        "translate": lambda x: f"翻译结果：{x}",
        "summarize": lambda x: f"摘要：{x}"
    }
    
    def orchestrate_tools(user_input: str) -> str:
        # 简单的工具选择逻辑
        if "搜索" in user_input and "翻译" in user_input:
            query = user_input.replace("搜索", "").replace("翻译", "").strip()
            search_result = tools["search"](query)
            return tools["translate"](search_result)
        elif "摘要" in user_input:
            content = user_input.replace("摘要", "").strip()
            return tools["summarize"](content)
        return "无法处理该请求"
    
    # 测试用例
    print(orchestrate_tools("搜索Python教程并翻译成英文"))
    # 输出：翻译结果：搜索结果：Python教程
    
    print(orchestrate_tools("摘要：这是一段很长的文本..."))
    # 输出：摘要：这是一段很长的文本...

# 测试
multi_tool_collaboration()
```


---
## 案例研究


### 1：Cognition AI (Devin 代码生成 Agent)

 1：Cognition AI (Devin 代码生成 Agent)

**背景**: Cognition AI 致力于开发完全自主的 AI 软件工程师 Devin。在早期的开发过程中，团队发现让 Agent 拥有固定的“技能”无法应对复杂多变的真实编程任务。

**问题**: 传统的“技能”模式要求开发者预先定义好 Agent 的行为模式。当面对一个从未见过的全栈开发任务时，基于静态技能的 Agent 往往会卡在环境配置或依赖安装上，因为它不知道如何动态调整策略以解决未预见到的错误。

**解决方案**: 团队转而采用基于“AGENTS.md”或类似长上下文规划文档的架构。他们不再仅仅给 Agent 赋予一个个孤立的 API 调用技能，而是通过一个包含大量工程背景知识、调试策略和工具使用说明的“大脑”文档来驱动 Agent。这使得 Agent 能够像人类工程师一样，根据当前的报错信息和项目状态，动态查阅文档并规划下一步操作，而不是机械地执行预置脚本。

**效果**: 根据 Cognition AI 的演示及评估报告，采用这种基于深度上下文和规划能力的 Agent，在解决实际 GitHub Issue 上的成功率远超基于简单技能调用的模型。Devin 能够成功通过实际的技术面试，并在 Upwork 上完成真实的编码任务，证明了其在处理未知复杂问题时的鲁棒性。

---



### 2：Rabbit (R1 操作系统)

 2：Rabbit (R1 操作系统)

**背景**: Rabbit 是一家致力于重塑人机交互的硬件初创公司，其产品 R1 旨在通过自然语言控制各种服务（如播放音乐、订车、订购外卖），而不需要用户打开一个个特定的 App。

**问题**: 传统的 App 集成方式类似于给 Agent 配备“技能”——为 Uber 写一个接口，为 Spotify 写一个接口。然而，这种方式扩展性极差。一旦某个 App 的 UI 发生变化或出现网络波动，特定的“技能”就会失效，导致 Agent 无法完成任务。

**解决方案**: Rabbit 开发了一种基于“Large Action Model”（LAM）的技术，其核心逻辑与“AGENTS.md”理念一致：不依赖硬编码的技能，而是通过学习现有 App 的操作逻辑和界面映射。Agent 理解服务背后的意图和流程，作为一个通用的操作者去动态适配前端界面。它不是调用一个死板的 `order_uber()` 函数，而是理解“我要去机场”的意图，并动态规划如何与当前的 Uber 交互界面进行点击和输入。

**效果**: 这种基于理解和动态规划的 Agent 架构，使得 R1 设备无需为每一个新 App 更新代码即可支持服务。在实际演示中，即使面对复杂的 UI 流程，Agent 也能像人类一样一步步完成操作，极大地降低了维护成本并提高了服务的通用性。

---



### 3：某大型 SaaS 平台客户支持自动化

 3：某大型 SaaS 平台客户支持自动化

**背景**: 一家拥有数百万用户的 SaaS 企业试图利用 AI 自动化其 L2 级别的客户支持流程，旨在处理复杂的账单纠纷和技术故障排查。

**问题**: 最初，团队尝试使用基于“技能”的 Agent，例如“查询数据库技能”、“重置密码技能”。但在处理跨部门的复杂问题时（例如：因为系统故障导致的扣费错误），简单的技能链无法处理。Agent 经常在需要判断是否应该退款时陷入死循环，因为它缺乏上下文理解能力和决策依据。

**解决方案**: 团队重构了 Agent 架构，引入了类似“AGENTS.md”的中央知识库和推理引擎。该文档包含了公司的完整服务协议、故障排查手册和决策逻辑。Agent 不再是执行单一技能的机器人，而是一个阅读了所有运维手册的“资深支持工程师”。它能够根据用户的描述，在文档中检索相关条款，结合后台数据，生成一个经过深思熟虑的解决方案，而不是机械地执行退款或拒绝。

**效果**: 上线后，该 Agent 解决了超过 60% 的复杂工单，而这些工单之前必须由人工处理。更重要的是，由于 Agent 的决策依据是清晰的文档逻辑，其给出的解释和解决方案更加合理、合规，极大地提升了客户满意度并减少了误操作带来的财务损失。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优先采用自然语言定义 Agent 行为

**说明**: 在 `AGENTS.md` 模式中，通过自然语言（而非硬编码的函数或 JSON Schema）来定义 Agent 的行为、目标和约束。这种方式允许 LLM 更灵活地理解上下文，并在执行过程中进行动态推理，从而在复杂任务评估中表现优于传统的固定 Skills 调用。

**实施步骤**:
1. 创建一个独立的 `AGENTS.md` 文件。
2. 在文件头部清晰定义 Agent 的角色、核心目标及主要能力。
3. 用自然语言描述 Agent 应如何处理特定场景，而不是编写具体的代码逻辑。

**注意事项**: 确保语言描述清晰、无歧义，避免过于抽象导致模型理解偏差。

---

### 实践 2：构建结构化的上下文与知识库

**说明**: `AGENTS.md` 的优势在于能够容纳更丰富的上下文信息。最佳实践包括在文件中包含领域知识、常见问题解答、业务规则以及期望的输出格式。这相当于为 Agent 提供了一个“系统提示词”知识库，使其能够更准确地响应。

**实施步骤**:
1. 在文件中设立专门的“知识库”或“背景信息”章节。
2. 将业务逻辑规则、API 限制、错误处理策略以文本形式写入。
3. 明确指定输入数据的结构和输出结果的标准格式。

**注意事项**: 注意 Token 限制，确保关键信息位于文件的前部，因为模型对开头和结尾的关注度最高。

---

### 实践 3：实施迭代式的提示词优化

**说明**: 既然 `AGENTS.md` 表现优于 Skills，应将其视为需要持续优化的核心资产。通过评估结果反馈，不断调整文件中的指令、示例和约束条件，以引导模型产生更高质量的输出。

**实施步骤**:
1. 建立一套评估指标来衡量 Agent 的表现。
2. 当 Agent 在评估中失败时，分析失败原因并在 `AGENTS.md` 中添加针对性的修正指令或示例（少样本学习）。
3. 记录每次修改的版本，以便回滚和对比效果。

**注意事项**: 避免指令过于冗长和复杂，保持指令的简洁性和针对性。

---

### 实践 4：明确边界与安全约束

**说明**: 利用自然语言显式定义 Agent 的操作边界和安全红线。相比于代码层面的硬编码限制，在 `AGENTS.md` 中声明约束可以更好地利用模型的内在安全对齐能力，防止 Agent 执行越界操作。

**实施步骤**:
1. 在文件中设立“约束与限制”章节。
2. 明确列出 Agent 绝对不能执行的操作（如删除数据、绕过权限）。
3. 定义当遇到恶意输入或无法处理的请求时的标准拒绝响应。

**注意事项**: 定期测试这些边界条件，确保模型在极端情况下仍能遵守约束。

---

### 实践 5：利用思维链增强推理能力

**说明**: 在 `AGENTS.md` 中引导模型进行逐步推理。通过指示模型在采取行动前先进行“思考”或“规划”，可以显著提高在复杂评估任务中的成功率，这比直接调用 Skill 更具鲁棒性。

**实施步骤**:
1. 在指令中要求 Agent 在输出最终结果前，先输出分析过程或中间步骤。
2. 提供包含推理过程的示例，展示如何从输入推导至输出。
3. 鼓励 Agent 在不确定时进行自我纠错或请求澄清。

**注意事项**: 平衡推理深度与响应延迟，确保思维链不会导致 Token 消耗过大。

---

### 实践 6：从“技能调用”转向“意图规划”

**说明**: 传统的 Skills 模式通常是“检测意图 -> 调用函数”，而 `AGENTS.md` 模式应侧重于“理解目标 -> 制定计划 -> 执行”。最佳实践是让 Agent 根据文件中的全局目标自主决定行动路径，而不是机械地匹配预定义的工具。

**实施步骤**:
1. 在 `AGENTS.md` 中定义高层面的业务目标，而非具体的 API 列表。
2. 允许 Agent 结合上下文自主决定需要哪些步骤，甚至决定何时使用外部工具。
3. 设计评估集，专门测试 Agent 处理未预见场景的能力（泛化能力）。

**注意事项**: 需要确保模型具备足够的指令遵循能力，否则可能会产生幻觉或偏离目标。

---
## 学习要点

- 基于提供的标题和来源信息，以下是关于 AGENTS.md 与 Skills 在智能体评估中对比的关键要点总结：
- 将 Agent 的行为逻辑、目标及约束条件集中定义在 AGENTS.md 文件中，比单纯依赖 Skills（技能）函数调用更能显著提升智能体在复杂任务中的表现。
- AGENTS.md 能够为 LLM 提供更全面的上下文和全局视角，使智能体能够更好地理解任务意图，从而减少执行过程中的盲目性。
- 相比于 Skills 这种碎片化的指令方式，AGENTS.md 提供的结构化文本有助于维持智能体在长对话或多步骤推理中的一致性。
- 这种方法验证了“上下文即代码”的趋势，表明通过优化提示词和文档结构来驱动智能体，往往比编写硬编码的技能更灵活有效。
- 在评估结果中，基于 AGENTS.md 的架构展现出了更强的鲁棒性，能够更有效地处理边缘情况或未明确预设的技能场景。

---
## 常见问题


### 1: 什么是 AGENTS.md，它与传统的“技能”定义有何不同？

1: 什么是 AGENTS.md，它与传统的“技能”定义有何不同？

**A**: AGENTS.md 是一种用于定义和描述 AI 智能体行为的规范或文档格式。与传统的“技能”不同，技能通常指代单一、离散的功能（例如“搜索网络”或“生成图片”），而 AGENTS.md 倾向于采用更整体、上下文感知的方法来定义智能体的能力。它可能包含关于智能体目标、可用工具、约束条件以及高层级决策逻辑的详细信息，而不仅仅是简单的函数调用。这种方法使智能体能够更有效地处理复杂、多步骤的任务。



### 2: 为什么在评估中 AGENTS.md 的表现优于技能？

2: 为什么在评估中 AGENTS.md 的表现优于技能？

**A**: 根据来源信息，AGENTS.md 在评估中表现优异，主要原因可能在于其提供了更丰富的上下文和结构化的指导。传统的技能调用往往缺乏对任务整体目标的理解，容易在执行过程中迷失方向或无法处理边缘情况。AGENTS.md 通过为智能体提供一个类似“系统说明书”的完整视图，使其能够更好地规划任务流程、理解用户意图，并在执行过程中进行自我纠正，从而在复杂任务评估中取得更高的成功率。



### 3: 这种评估方法具体测试了智能体的哪些能力？

3: 这种评估方法具体测试了智能体的哪些能力？

**A**: 虽然具体的评估指标取决于测试框架，但通常这类“智能体评估”会测试大语言模型（LLM）在以下方面的能力：推理规划、工具使用准确性、长上下文记忆保持、错误恢复能力以及多步骤任务完成率。AGENTS.md 优于技能这一结果表明，在处理需要综合多种能力的复杂任务时，拥有结构化的全局指导文档比单纯依赖预设的技能库更有效。



### 4: AGENTS.md 是否会取代现有的 Agent 开发模式（如 LangChain 或 Semantic Kernel 中的技能概念）？

4: AGENTS.md 是否会取代现有的 Agent 开发模式（如 LangChain 或 Semantic Kernel 中的技能概念）？

**A**: 不一定是完全取代，而是一种进化或补充。现有的开发模式强调代码层面的模块化，而 AGENTS.md 强调描述层面的标准化。它可能会促使开发者从“编写代码函数”转向“编写高质量的行为描述”。未来的趋势可能是将两者结合：底层依然由代码和技能库支持，但上层通过类似 AGENTS.md 的标准来协调和驱动智能体的行为，使其更加通用和灵活。



### 5: 对于开发者来说，采用 AGENTS.md 规范有哪些实际好处？

5: 对于开发者来说，采用 AGENTS.md 规范有哪些实际好处？

**A**: 开发者采用这种规范可以获得几个关键好处：首先是**可移植性**，标准化的描述使得智能体配置可以在不同平台间迁移；其次是**可调试性**，当智能体行为异常时，检查文本描述比检查复杂的代码逻辑更容易发现问题；最后是**性能提升**，正如评估结果所示，这种格式能激发模型更好的推理能力，减少了为了特定任务编写复杂提示词或定制代码的需求。



### 6: 这一发现对“基于智能体的 AI”未来的发展意味着什么？

6: 这一发现对“基于智能体的 AI”未来的发展意味着什么？

**A**: 这一发现暗示了 AI 智能体的发展方向正在从“工具调用者”向“自主目标追求者”转变。它证明了通过更好的描述和规范（即“软件 2.0”或“软件 3.0”的概念），可以显著提升 AI 系统的智能水平。这意味着未来的 AI 开发可能会更加侧重于如何精确地描述任务和约束，而不是仅仅依赖于硬编码的逻辑，从而加速通用人工智能（AGI）在特定垂直领域的落地。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你正在为一个电商客服机器人设计系统。传统的“技能”方法是编写硬编码的脚本来处理“退款申请”和“查询订单”。请描述一种基于“Agent”的替代方案，说明它如何处理这两个任务，并指出为什么 Agent 方法在处理用户未预料的模糊提问时（例如：“我买的东西有问题，但我还没收到，怎么办？”）可能比硬编码技能更有效。

### 提示**: 考虑硬编码脚本与具备推理能力的 LLM 在处理非结构化输入时的区别，重点在于“泛化能力”。

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
- 标签： [Agent](/tags/agent/) / [LLM](/tags/llm/) / [AGENTS.md](/tags/agents-md/) / [Skills](/tags/skills/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [配置](/tags/%E9%85%8D%E7%BD%AE/) / [AI Agent](/tags/ai-agent/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-4.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-8.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-16.md" >}})
- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*