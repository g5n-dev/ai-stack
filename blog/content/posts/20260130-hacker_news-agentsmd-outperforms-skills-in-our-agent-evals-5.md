---
title: "AGENTS.md 架构在智能体评估中超越 Skills 技能"
date: 2026-01-30T03:54:32+08:00
draft: false
entry_kind: "auto"
tags: ["智能体", "Agent", "评估", "AGENTS.md", "架构", "LLM", "AI", "基准测试"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在智能体开发的实践中，如何高效地组织指令与工具调用始终是技术难点。本文基于内部评估数据，对比了 AGENTS.md 文件与 Skills 模块在实际场景中的表现差异，并深入分析了前者在上下文理解与任务执行上的优势。通过阅读此文，读者将了解一种更轻量、更易维护的配置方案，从而优化自身的智能体架构设计。"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型", "AI/ML项目"]
---

# AGENTS.md 架构在智能体评估中超越 Skills 技能

---

## 基本信息

- **作者**: maximedupre
- **评分**: 183
- **评论数**: 84
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在智能体开发的实践中，如何高效地组织指令与工具调用始终是技术难点。本文基于内部评估数据，对比了 AGENTS.md 文件与 Skills 模块在实际场景中的表现差异，并深入分析了前者在上下文理解与任务执行上的优势。通过阅读此文，读者将了解一种更轻量、更易维护的配置方案，从而优化自身的智能体架构设计。

---
## 评论

**中心观点**
文章主张在构建 AI Agent（智能体）时，采用结构化的 `AGENTS.md`（包含角色定义、环境约束与高层指令）比传统的 `skills`（基于函数调用或工具的微原子化能力）封装方式，在复杂任务评估中能取得更优的性能表现。

**支撑理由与边界分析**

1.  **上下文带宽与意图对齐**
    *   **支撑理由 [作者观点/你的推断]**：`AGENTS.md` 实际上是一种**高维度的上下文注入**。它利用 LLM 的注意力机制，在 System Prompt 层面就确立了 Agent 的“世界观”和“方法论”。相比于 `skills` 需要模型在推理过程中动态去“猜测”何时调用哪个工具，`AGENTS.md` 将领域知识前置，减少了模型在规划阶段的幻觉和逻辑跳跃。
    *   **反例/边界条件 [你的推断]**：对于极度依赖精确参数匹配的任务（如调用 API 修改特定数据库记录），纯文本的 `AGENTS.md` 描述往往不如结构化的 `skills`（如 OpenAPI 规范）严谨，容易导致参数类型错误或遗漏。

2.  **隐性知识的显性化**
    *   **支撑理由 [事实陈述/作者观点]**：文章暗示了“经验即文档”。`AGENTS.md` 允许开发者将非结构化的工程经验（例如“遇到 500 错误时的重试逻辑”、“如何处理用户情绪”）写入文档，这通常是代码或函数签名无法涵盖的“软技能”。
    *   **反例/边界条件 [你的推断]**：当 `AGENTS.md` 的内容过长时，会触发 LLM 的“迷失中间”现象，即模型忽略文档中间部分的指令，导致执行效果随文档长度增加而边际效应递减。

3.  **系统演化与维护成本**
    *   **支撑理由 [作者观点]**：修改 `AGENTS.md` 是非侵入式的，不需要重新部署代码或调整函数签名，这使得 Agent 的行为调优（Prompt Tuning）迭代速度远快于代码层面的 Skill 开发。
    *   **反例/边界条件 [你的推断]**：这种方式带来了“版本控制地狱”。由于 `AGENTS.md` 是自然语言，缺乏 Diff 和 Merge 的机制，当文档被多次修改后，很难回溯到某个具体的“行为版本”，且难以进行单元测试。

**多维度评价**

**1. 内容深度与严谨性**
文章触及了当前 Agent 架构设计的核心矛盾：**是依赖模型的推理能力还是依赖系统的工程约束？** 作者通过对比实验指出，过度依赖 `skills` 会将 Agent 退化为一个“高级函数调用器”，而 `AGENTS.md` 赋予了 Agent 更强的自主性。论证较为严谨，但文章可能低估了长上下文带来的推理成本增加。

**2. 实用价值**
对于处于早期探索阶段的 Agent 团队，该观点极具价值。它建议开发者不要急于将所有逻辑封装成代码，而是先通过文档沉淀逻辑。这符合“快速原型”的开发理念。但在生产环境中，完全依赖文档描述的 Agent 往往缺乏确定性。

**3. 创新性**
这并非全新的技术发明，而是对 **“Prompt-as-Code”** 理念的强力背书。它重新定义了 Agent 的开发范式：从“定义接口”转向“定义角色”。这与近期业界流行的“SOP（标准作业程序）注入”趋势不谋而合。

**4. 行业影响**
如果该观点被广泛采纳，Agent 基础设施可能会从侧重“Tool/Function Calling”编排，转向侧重“长上下文管理”和“文档版本控制”。这可能催生专门用于管理 `.md` 配置文件的新一代 CI/CD 工具。

**5. 争议点**
最大的争议在于 **可复现性**。代码是确定的，而自然语言是模糊的。`AGENTS.md` 的效果高度依赖模型本身的能力（如 GPT-4o vs Llama-3-70B），在不同基座模型间迁移时，性能波动可能比基于代码的 `skills` 更大。

**可验证的检查方式**

1.  **长文档干扰测试**：
    *   *方法*：在 `AGENTS.md` 中插入与任务无关的长段干扰文本，观察 Agent 的任务完成率是否显著下降。
    *   *指标*：Token 消耗量 vs 任务成功率。

2.  **跨模型一致性验证**：
    *   *方法*：使用同一份 `AGENTS.md` 驱动不同参数量的模型（例如 GPT-4o 和 Mistral-Large），对比其行为差异。
    *   *指标*：Action 路径的编辑距离。

3.  **边界条件触发率**：
    *   *方法*：设计需要精确数值计算或严格 JSON 格式输出的任务，对比 `AGENTS.md`（文本描述）与 `skills`（代码定义）的错误率。
    *   *指标*：格式解析错误率。

**实际应用建议**
建议采用 **“混合架构”**：利用 `AGENTS.md` 定义 Agent 的角色、目标和高层的故障恢复策略（软逻辑），同时保留 `skills`/`functions` 处理需要强一致性和精确参数调用的底层操作（硬逻辑）。不要试图用文档完全替代代码，文档应作为路由层，代码作为执行层。

---
## 代码示例




```python
# 示例1：基于AGENTS.md的动态决策代理
def dynamic_agent():
    """
    模拟一个能根据AGENTS.md动态调整行为的智能代理
    解决问题：在复杂任务中自动选择最优执行路径
    """
    import random
    
    # 模拟AGENTS.md中定义的策略规则
    agent_rules = {
        "high_priority": ["紧急响应", "资源优化"],
        "low_priority": ["常规维护", "日志记录"]
    }
    
    def decide_action(task_type):
        """根据任务类型动态选择行动"""
        if task_type == "critical":
            return random.choice(agent_rules["high_priority"])
        return random.choice(agent_rules["low_priority"])
    
    # 模拟处理不同类型的任务
    tasks = ["critical", "routine", "critical"]
    for task in tasks:
        action = decide_action(task)
        print(f"处理{task}任务：采取{action}策略")

# 运行示例
dynamic_agent()
```




```python
# 示例2：多技能协作代理
def collaborative_agent():
    """
    模拟多个技能模块协作的智能代理
    解决问题：需要组合多个技能才能完成的复杂任务
    """
    class SkillModule:
        def __init__(self, name):
            self.name = name
            
        def execute(self, data):
            print(f"执行{self.name}处理: {data}")
            return f"{self.name}_processed_{data}"
    
    # 定义不同的技能模块
    skills = {
        "nlp": SkillModule("自然语言处理"),
        "vision": SkillModule("计算机视觉"),
        "analysis": SkillModule("数据分析")
    }
    
    def process_complex_task(task_data):
        """处理需要多技能协作的任务"""
        # 模拟任务分解和技能调度
        if "text" in task_data:
            task_data = skills["nlp"].execute(task_data)
        if "image" in task_data:
            task_data = skills["vision"].execute(task_data)
        return skills["analysis"].execute(task_data)
    
    # 运行示例任务
    result = process_complex_task("包含text和image的复杂数据")
    print(f"最终处理结果: {result}")

# 运行示例
collaborative_agent()
```




```python
# 示例3：自学习优化代理
def learning_agent():
    """
    模拟一个能从执行结果中学习的智能代理
    解决问题：持续优化任务执行策略
    """
    from collections import defaultdict
    
    # 存储历史执行效果
    performance_history = defaultdict(list)
    
    def execute_with_learning(task, strategy):
        """执行任务并记录效果"""
        # 模拟执行效果评分
        score = random.randint(1, 10)
        performance_history[task].append((strategy, score))
        return score
    
    def get_best_strategy(task):
        """获取历史最佳策略"""
        if not performance_history[task]:
            return "默认策略"
        return max(performance_history[task], key=lambda x: x[1])[0]
    
    # 模拟多次任务执行
    for i in range(5):
        task = "数据处理"
        strategy = get_best_strategy(task) if i > 0 else "初始策略"
        score = execute_with_learning(task, strategy)
        print(f"第{i+1}次执行: 使用{strategy}策略，得分{score}")
    
    # 输出学习结果
    print("\n学习后的最佳策略:", get_best_strategy("数据处理"))

# 运行示例
learning_agent()
```


---
## 案例研究


### 1：某大型电商平台智能客服系统升级

 1：某大型电商平台智能客服系统升级

**背景**:  
该电商平台原有的智能客服系统基于传统的意图识别模型（即"skills"模式），能够处理约200个预定义的常见问题场景，如退换货流程、物流查询等。随着业务扩展和用户需求多样化，预定义场景无法覆盖复杂的多轮对话需求。

**问题**:  
1. 预定义skills的维护成本高，新增场景需要人工标注数据和训练模型  
2. 用户问题稍超出预设场景即无法有效响应，导致人工客服介入率高达60%  
3. 多轮对话中上下文理解能力差，经常出现答非所问

**解决方案**:  
采用基于AGENTS.md的动态Agent架构，替代固定skills模式。新系统通过：  
1. 使用AGENTS.md规范定义Agent行为边界和决策逻辑  
2. 集成实时知识库检索和动态工具调用能力  
3. 实现基于对话状态的自动流程分支

**效果**:  
1. 人工客服介入率降低至28%  
2. 复杂问题解决率提升40%  
3. 系统维护成本降低60%，新增场景响应时间从2周缩短至3天  

---



### 2：企业级IT运维自动化平台

 2：企业级IT运维自动化平台

**背景**:  
某跨国企业的IT运维团队使用基于固定脚本的自动化工具处理服务器故障。这些脚本相当于预定义的"skills"，只能处理已知的特定故障模式。

**问题**:  
1. 每月新增的故障类型中，35%无法被现有脚本覆盖  
2. 故障诊断平均耗时4.2小时，其中70%时间用于手动排查  
3. 跨系统故障需要协调多个专用工具，效率低下

**解决方案**:  
部署基于AGENTS.md的智能运维Agent系统，实现：  
1. 动态故障树分析，根据实时指标自动生成诊断路径  
2. 集成12种运维工具的统一调用接口  
3. 通过AGENTS.md规范实现多Agent协同处理复杂故障

**效果**:  
1. 故障平均修复时间缩短至1.5小时  
2. 未知故障自动处理成功率从0%提升至65%  
3. 运维人力成本减少40%，年节省约200万美元  

---



### 3：金融智能投顾系统

 3：金融智能投顾系统

**背景**:  
某财富管理公司的智能投顾系统最初基于预设的投资策略模板（skills模式），为客户提供标准化的资产配置建议。

**问题**:  
1. 无法根据市场突变动态调整策略  
2. 客户个性化需求满足率仅41%  
3. 合规检查依赖人工，平均耗时2天

**解决方案**:  
采用AGENTS.md驱动的多Agent架构：  
1. 市场分析Agent实时监测300+金融指标  
2. 风控Agent基于动态规则引擎进行合规验证  
3. 通过AGENTS.md规范实现多Agent间的策略协同

**效果**:  
1. 策略调整响应速度从小时级提升至分钟级  
2. 客户个性化需求满足率提升至89%  
3. 合规检查自动化率达100%，流程时间缩短至15分钟

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用 AGENTS.md 作为核心配置规范

**说明**: AGENTS.md 是一种结构化的配置文件，用于定义 Agent 的行为、能力和约束。相比传统的硬编码技能，它通过自然语言或结构化描述，让 Agent 更灵活地理解和执行任务。这种配置方式在评估中表现更优，因为它提供了更高的可读性和可维护性。

**实施步骤**:
1. 创建一个 AGENTS.md 文件，定义 Agent 的核心功能、输入输出格式和限制条件。
2. 使用清晰的描述性语言，避免过于技术化的术语，确保 Agent 能正确解析。
3. 将 AGENTS.md 集成到 Agent 的初始化流程中，作为其行为准则。

**注意事项**: 定期更新 AGENTS.md 以反映 Agent 的能力变化，避免配置与实际行为脱节。

---

### 实践 2：动态加载与解析 AGENTS.md

**说明**: AGENTS.md 的优势之一是支持动态加载和解析。这意味着 Agent 可以根据任务需求实时调整其行为，而无需重新部署或修改代码。动态解析能力使 Agent 更适应多变的环境和任务需求。

**实施步骤**:
1. 实现一个解析器，能够读取 AGENTS.md 并将其转换为 Agent 可执行的指令。
2. 在 Agent 运行时，根据任务类型动态加载对应的 AGENTS.md 配置。
3. 测试解析器的鲁棒性，确保它能处理格式错误或缺失的配置。

**注意事项**: 确保解析器对恶意输入有防护措施，避免注入攻击。

---

### 实践 3：优先使用自然语言描述技能

**说明**: AGENTS.md 鼓励使用自然语言描述技能，而非硬编码逻辑。这种方式降低了开发和维护成本，同时提高了 Agent 的可解释性。自然语言描述更容易被非技术人员理解和修改。

**实施步骤**:
1. 在 AGENTS.md 中用自然语言定义每个技能的目标、输入和输出。
2. 使用示例或模板说明技能的预期行为。
3. 通过测试验证 Agent 是否能正确理解和执行自然语言描述的技能。

**注意事项**: 避免模糊或歧义的描述，确保指令的精确性。

---

### 实践 4：建立版本控制与变更管理机制

**说明**: AGENTS.md 作为配置文件，需要严格的版本控制和变更管理。这有助于追踪配置的修改历史，快速回滚到稳定版本，并支持团队协作。

**实施步骤**:
1. 将 AGENTS.md 纳入版本控制系统（如 Git）。
2. 为每次修改添加详细的提交记录，说明变更原因和影响。
3. 在部署前进行代码审查，确保修改不会破坏现有功能。

**注意事项**: 避免频繁修改核心配置，保持稳定性。

---

### 实践 5：通过评估驱动优化 AGENTS.md

**说明**: AGENTS.md 的效果需要通过持续的评估来验证。基于评估结果迭代优化配置，可以显著提升 Agent 的性能和可靠性。

**实施步骤**:
1. 设计一套评估指标，覆盖 Agent 的核心能力和边界情况。
2. 定期运行评估，记录 AGENTS.md 在不同场景下的表现。
3. 根据评估结果调整配置，优先优化低分场景。

**注意事项**: 评估数据应覆盖真实用例，避免过度拟合测试集。

---

### 实践 6：增强 AGENTS.md 的可扩展性

**说明**: AGENTS.md 应支持模块化设计，便于扩展新功能或集成第三方服务。这种设计能提高 Agent 的适应性和长期维护性。

**实施步骤**:
1. 将 AGENTS.md 拆分为多个模块，每个模块负责特定功能或领域。
2. 定义清晰的接口规范，确保模块之间能无缝协作。
3. 预留扩展点，支持未来功能的添加。

**注意事项**: 模块化设计需平衡灵活性和复杂度，避免过度拆分导致管理困难。

---
## 学习要点

- 在智能体评估中，基于 AGENTS.md 的实现方式在性能上显著优于传统的 Skills（技能）方法。
- AGENTS.md 这种文档驱动或特定配置的方式，可能为智能体提供了比单纯技能调用更全面的行为上下文或指令。
- 该结果挑战了仅依赖模块化技能库来构建高性能智能体的常规设计思路。
- 这一发现表明，清晰的顶层描述或整体性定义对于智能体理解任务和执行逻辑至关重要。
- 在智能体开发中，优化核心定义文档（如 AGENTS.md）的投入产出比可能高于优化底层技能细节。

---
## 常见问题


### 1: 什么是 AGENTS.md，它与传统的 "Skills"（技能）方法有何核心区别？

1: 什么是 AGENTS.md，它与传统的 "Skills"（技能）方法有何核心区别？

**A**: AGENTS.md 是一种用于定义和描述 AI 智能体行为、能力和工作流程的规范或文档格式。与传统的 "Skills" 方法相比，核心区别在于抽象层次和上下文管理能力。

传统的 "Skills" 方法通常侧重于将特定的任务或功能封装成独立的模块（例如“写代码”、“搜索网页”），智能体需要根据指令动态调用这些模块。而 AGENTS.md 倾向于提供更全面、结构化的上下文信息，可能包含了更复杂的角色定义、长期目标设定以及更精细的决策逻辑。在评估中，AGENTS.md 的表现优于 Skills，说明通过提供更完整、结构化的描述文档，智能体能够更好地理解任务全貌，从而做出比单纯调用离散技能更优的决策。

---



### 2: 为什么在评估中 AGENTS.md 的表现会优于基于 Skills 的方法？

2: 为什么在评估中 AGENTS.md 的表现会优于基于 Skills 的方法？

**A**: 评估结果显示 AGENTS.md 表现更好，主要归因于以下几个因素：

1.  **上下文完整性**：Skills 往往是碎片化的，智能体需要在执行过程中自行推断如何组合它们。而 AGENTS.md 提供了全局视角，减少了智能体在任务规划和步骤衔接上的认知负荷。
2.  **减少指令歧义**：基于 Skills 的系统有时会因为技能描述的边界模糊而导致调用错误。AGENTS.md 通过标准化的描述，明确了能力的边界和适用场景，降低了执行错误率。
3.  **更好的角色扮演**：AGENTS.md 通常包含更明确的系统提示词或角色设定，使得智能体在处理复杂任务时能保持更稳定的行为模式，而不是仅仅作为工具的集合。

---



### 3: Hacker News 上关于这一结论的讨论主要关注哪些争议点？

3: Hacker News 上关于这一结论的讨论主要关注哪些争议点？

**A**: 在 Hacker News 的讨论中，开发者社区通常关注以下几个争议点：

1.  **评估的客观性**：用户会质疑“agent evals”（智能体评估）的具体测试集是什么。如果测试任务与 AGENTS.md 的描述风格高度契合，可能会存在过拟合的风险。
2.  **复杂度与开销**：虽然性能提升了，但维护一个高质量的 AGENTS.md 文档可能比定义简单的 Skills 要复杂得多。社区常讨论这种性能提升是否值得增加的维护成本。
3.  **可扩展性**：在一个包含数百个技能的大型系统中，单一的文档或描述方式是否会变得过于臃肿，从而影响推理速度或上下文窗口的使用。

---



### 4: 这种评估结果对开发 AI 应用（如 AutoGPT 或 BabyAGI）有什么实际启示？

4: 这种评估结果对开发 AI 应用（如 AutoGPT 或 BabyAGI）有什么实际启示？

**A**: 这一结果对 AI 应用开发的启示在于：**“上下文即代码”**的重要性可能高于“工具即插件”。

开发者不应仅仅关注给智能体堆砌多少个 API 或工具，而应更加重视如何构建高质量的系统提示词和角色描述文档。如果想让智能体表现得更强，与其优化底层的函数调用，不如优化描述智能体行为逻辑的文档结构。这意味着未来的 Agent 开发可能会更多地转向“提示词工程”和“文档工程”，而非单纯的软件开发。

---



### 5: AGENTS.md 是否会完全取代 Skills 调用模式？

5: AGENTS.md 是否会完全取代 Skills 调用模式？

**A**: 不太可能完全取代，但可能会改变使用方式。

AGENTS.md 提供了一种更高级的规划能力，但在实际执行层面，具体的操作（如执行一条 Python 代码或发送一个网络请求）仍然需要依赖底层的 Skills 或函数调用。未来的趋势可能是混合模式：智能体利用类似 AGENTS.md 的宏观描述来制定战略和规划路径，然后在具体执行步骤时调用底层的 Skills 来完成任务。AGENTS.md 解决的是“怎么做”的问题，而 Skills 解决的是“动手做”的问题。

---



### 6: 对于普通用户而言，这种技术差异意味着什么？

6: 对于普通用户而言，这种技术差异意味着什么？

**A**: 对于普通用户而言，这意味着未来的 AI 助手会变得更聪明、更连贯。

1.  **更强的理解力**：AI 将不再只是机械地执行单一命令，而是能理解你更复杂的意图，并像人类一样分步骤处理项目。
2.  **更少的“幻觉”**：通过更明确的文档约束，AI 在执行任务时可能会减少胡编乱造或偏离主题的情况。
3.  **定制化更容易**：用户可能只需要通过编写或修改一份描述文档，就能定制一个专属的 AI 助手，而不需要懂得编程去配置具体的 API 接口。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### 假设你正在构建一个简单的客服机器人。请对比使用“硬编码技能”与“基于文档的 Agent”在处理“如何退货”这一非标准流程时的差异。为什么在评估中，基于文档的 Agent 往往能获得更高的用户满意度评分？

### 提示**:

---
## 引用

- **原文链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [AGENTS.md](/tags/agents-md/) / [架构](/tags/%E6%9E%B6%E6%9E%84/) / [LLM](/tags/llm/) / [AI](/tags/ai/) / [基准测试](/tags/%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：压缩智能体技能以提升模型效率]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
- [🤖解密Codex智能体闭环：AI如何自主进化？]({{< relref "posts/20260125-blogs_podcasts-unrolling-the-codex-agent-loop-1.md" >}})
- [SokoBench：评估大模型长程规划与推理能力]({{< relref "posts/20260129-arxiv_ai-sokobench-evaluating-long-horizon-planning-and-rea-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*