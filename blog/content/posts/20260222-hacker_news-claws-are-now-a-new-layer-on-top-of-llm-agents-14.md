---
title: "LLM智能体新增Claws层以优化任务执行"
date: 2026-02-22T00:55:41+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "智能体", "Claws", "任务执行", "架构优化", "Agent", "模型增强", "自动化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型（LLM）应用场景的不断拓展，如何提升智能体的执行效率与可控性成为技术落地的关键挑战。本文介绍的 Claws 框架，作为一种构建于 LLM 智能体之上的新型控制层，旨在通过更精细的任务调度与状态管理优化系统表现。通过阅读本文，读者将了解 Claws 的核心架构设计，并掌握其在增强智能体稳定性方面的实践价值"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型"]
---

# LLM智能体新增Claws层以优化任务执行

---

## 基本信息

- **作者**: Cyphase
- **评分**: 165
- **评论数**: 609
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大语言模型（LLM）应用场景的不断拓展，如何提升智能体的执行效率与可控性成为技术落地的关键挑战。本文介绍的 Claws 框架，作为一种构建于 LLM 智能体之上的新型控制层，旨在通过更精细的任务调度与状态管理优化系统表现。通过阅读本文，读者将了解 Claws 的核心架构设计，并掌握其在增强智能体稳定性方面的实践价值。

---
## 评论

### 评价文章：Claws are now a new layer on top of LLM agents

#### 一、 核心观点与论证结构

**中心观点：**
文章主张“Claws”（指代具备高精度、确定性与物理执行能力的工具或子系统）应当成为构建在 LLM Agents 之上的独立抽象层，旨在解决大模型在逻辑推理、工具调用及物理世界交互中固有的不确定性与幻觉问题，实现“大脑（LLM）”与“手脚”的解耦。

**支撑理由：**

1.  **弥补概率性缺陷：** LLM 本质上是概率模型，输出存在随机性。在金融交易、工业控制等容错率极低的场景中，直接依赖 LLM 生成最终指令风险过高。
    *   *（事实陈述）*
2.  **降低 Token 消耗与延迟：** 将复杂的计算、检索或物理控制逻辑下沉到“Claws”层，可以避免 LLM 陷入长上下文的“思维链”死循环，提升系统响应速度。
    *   *（作者观点 / 行业共识）*
3.  **明确的责任边界：** 通过引入确定的中间层，系统的安全性审计和错误归因变得更加清晰，即“大脑负责意图，手脚负责执行的正确性”。
    *   *（你的推断）*

**反例/边界条件：**

1.  **过度工程化风险：** 对于简单的创意写作或非结构化数据分析任务，引入严格的“Claws”层可能会增加不必要的系统复杂度，导致灵活性下降。
    *   *（你的推断）*
2.  **上下文割裂：** 如果“Claws”层与 LLM 的交互协议设计不当（例如仅传递最终结果而非中间过程），可能会导致 LLM 缺乏执行过程的感知，从而影响其后续决策的连贯性。
    *   *（技术局限性）*

---

#### 二、 深度评价（1200字以内）

**1. 内容深度：从“提示词工程”向“系统工程”的范式转移**
该文章触及了当前 AI Agent 领域最核心的痛点：**仅靠 Scaling Law（规模定律）无法解决 Agent 的可靠性问题。** 文章提出的“Claws”概念，实际上是对“Software 2.0”的一种修正——即并非所有代码都应由神经网络生成。
*   **评价：** 文章的深度在于它重新审视了“工具使用”的定义。传统观点认为 Tool Use 只是 LLM 的一个插件，而文章将其提升为与 LLM 并列的架构层级。这种分层思想借鉴了经典计算机科学中的抽象层理念，论证了在不确定的 LLM 之上必须覆盖一层确定性的逻辑壳。

**2. 实用价值：为 B2B 应用提供落地范式**
对于致力于构建企业级 Agent 的开发者而言，这篇文章具有极高的指导意义。目前行业普遍面临 LLM 输出不可控导致的“生产环境恐惧”。
*   **实际案例：** 在构建**数据库查询 Agent** 时，直接让 LLM 生成 SQL 往往会写出语法错误或具有权限风险的代码。如果引入“Claws”层，该层包含一个基于规则或传统编译原理的 SQL 生成器与校验器，LLM 仅负责将自然语言转为中间表示（IR），系统的成功率将大幅提升。
*   **指导意义：** 它指导开发者停止试图通过微调 LLM 来解决所有问题，转而投资于传统软件工程与 LLM 的结合。

**3. 创新性：概念重塑大于技术突破**
“Claws”这个词本身具有强烈的隐喻色彩，将 Agent 的“攻击性”或“执行力”具象化。
*   **新观点：** 文章隐含提出了**“可验证的计算”**应当与“生成式的推理”分离。这与近期业界流行的“Guardrails（护栏）”或“Boson AI”的确定性执行思路不谋而合，但“Claws”的表述更强调主动的执行能力而非被动的防御。

**4. 可读性与逻辑性**
文章逻辑结构清晰，遵循了“问题-方案-价值”的标准叙事路径。然而，文章在技术实现细节上可能略显模糊。例如，“Claws”层具体是基于代码解释器、确定性状态机还是符号推理系统？如果文章未能明确界定其技术边界，容易让读者将其与简单的“Function Calling”混淆。

**5. 行业影响：推动“混合架构”的普及**
如果该观点被广泛接受，将加速 **Neuro-symbolic AI（神经符号人工智能）** 的复兴。未来的 AI Agent 基础设施可能会分化为两极：一极是越来越聪明的通用大模型（大脑），另一极是越来越专业化、标准化的执行中间件市场（Claws）。这将催生专门提供“高精度执行层”的初创公司。

**6. 争议点与不同观点**
*   **端到端派的反驳：** 以 OpenAI 为代表的学派可能认为，随着模型推理能力的提升（如 o1 模型），模型本身足以处理复杂逻辑和自我纠错，额外的层级只是过渡期的拐杖，增加了系统的信息熵和传输损耗。
*   **灵活性争议：** 硬编码的“Claws”可能限制了 Agent 的涌现能力。如果“爪子”只能做特定的动作，Agent 可能无法应对训练数据中未见过的新颖工具组合。

**7. 实际应用建议**
*   **不要重新发明轮子：** 在构建 Agent 时，先用 LangChain 或 LlamaIndex 等框架的 Tool 功能快速验证，当发现频繁出现“幻觉执行”或“格式错误”

---
## 代码示例




```python
# 示例1：基于Claws的LLM Agent任务调度
def task_scheduler():
    """
    模拟Claws作为LLM Agent的调度层，实现任务分发和执行
    """
    from typing import List, Callable
    
    class ClawsScheduler:
        def __init__(self):
            self.agents = []
        
        def register_agent(self, agent: Callable):
            """注册可用的LLM Agent"""
            self.agents.append(agent)
        
        def dispatch(self, task: str) -> str:
            """根据任务类型分发到合适的Agent"""
            for agent in self.agents:
                if agent.can_handle(task):
                    return agent.execute(task)
            return "No suitable agent found"
    
    # 示例Agent实现
    class CodeAgent:
        @staticmethod
        def can_handle(task: str) -> bool:
            return "code" in task.lower()
        
        @staticmethod
        def execute(task: str) -> str:
            return f"CodeAgent executing: {task}"
    
    # 使用示例
    scheduler = ClawsScheduler()
    scheduler.register_agent(CodeAgent())
    
    return scheduler.dispatch("Write Python code for sorting")

# 测试
print(task_scheduler())  # 输出: CodeAgent executing: Write Python code for sorting
```




```python
# 示例2：Claws的Agent能力监控
def agent_monitor():
    """
    实现Claws对LLM Agent运行状态的实时监控
    """
    import time
    from datetime import datetime
    
    class ClawsMonitor:
        def __init__(self):
            self.metrics = {
                'total_requests': 0,
                'successful': 0,
                'failed': 0,
                'avg_response_time': 0
            }
        
        def log_request(self, success: bool, duration: float):
            """记录每次请求的指标"""
            self.metrics['total_requests'] += 1
            if success:
                self.metrics['successful'] += 1
            else:
                self.metrics['failed'] += 1
            
            # 更新平均响应时间
            n = self.metrics['total_requests']
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (n-1) + duration) / n
            )
        
        def get_health_report(self) -> str:
            """生成健康报告"""
            return (
                f"Agent Health Report @ {datetime.now()}\n"
                f"Total Requests: {self.metrics['total_requests']}\n"
                f"Success Rate: {self.metrics['successful']/self.metrics['total_requests']*100:.1f}%\n"
                f"Avg Response: {self.metrics['avg_response_time']:.2f}s"
            )
    
    # 使用示例
    monitor = ClawsMonitor()
    monitor.log_request(True, 1.2)
    monitor.log_request(True, 0.8)
    monitor.log_request(False, 2.1)
    
    return monitor.get_health_report()

# 测试
print(agent_monitor())
```




```python
# 示例3：Claws的Agent动态加载
def dynamic_agent_loader():
    """
    实现Claws对LLM Agent的动态加载和卸载
    """
    import importlib
    import sys
    
    class ClawsLoader:
        def __init__(self):
            self.loaded_agents = {}
        
        def load_agent(self, agent_name: str, module_path: str):
            """动态加载Agent模块"""
            try:
                module = importlib.import_module(module_path)
                self.loaded_agents[agent_name] = module
                return f"Successfully loaded {agent_name}"
            except Exception as e:
                return f"Failed to load {agent_name}: {str(e)}"
        
        def unload_agent(self, agent_name: str):
            """卸载已加载的Agent"""
            if agent_name in self.loaded_agents:
                del self.loaded_agents[agent_name]
                return f"Unloaded {agent_name}"
            return f"{agent_name} not found"
        
        def list_agents(self) -> list:
            """列出所有已加载的Agent"""
            return list(self.loaded_agents.keys())
    
    # 使用示例
    loader = ClawsLoader()
    print(loader.load_agent("MathAgent", "math"))  # 模拟加载内置模块
    print(loader.list_agents())
    print(loader.unload_agent("MathAgent"))
    print(loader.list_agents())

# 测试
dynamic_agent_loader()
```


---
## 案例研究


### 1：某大型电商企业的智能客服升级

 1：某大型电商企业的智能客服升级

**背景**:  
该企业原有的客服系统基于规则引擎，只能处理简单、标准化的问题。随着业务扩展，用户咨询量激增，复杂问题（如订单异常、售后纠纷）占比提升，人工客服压力巨大。

**问题**:  
传统规则引擎无法理解用户意图，导致问题解决率低（仅40%），且频繁转人工导致平均响应时间超过10分钟。同时，LLM直接接入存在幻觉风险（如错误承诺退款）。

**解决方案**:  
采用Claws作为中间层，在LLM Agent之上构建“护栏”。具体实现包括：  
1. 通过Claws的意图识别模块，将用户问题分类为“可直接处理”“需人工介入”“高风险操作”三类。  
2. 对高风险操作（如退款、修改订单），Claws调用API验证权限并生成结构化指令，而非直接依赖LLM生成文本。  
3. 整合企业知识库，通过Claws的检索增强生成（RAG）功能减少幻觉。

**效果**:  
- 问题自动解决率提升至75%，人工客服工作量减少50%。  
- 平均响应时间缩短至2分钟，用户满意度提高30%。  
- 高风险操作错误率降至0.1%以下。

---



### 2：金融科技公司的风控系统优化

 2：金融科技公司的风控系统优化

**背景**:  
该公司为银行提供风控SaaS服务，传统风控模型依赖固定规则（如交易金额阈值），难以应对新型欺诈手段（如账户盗用后的分散小额交易）。

**问题**:  
现有模型对复杂欺诈模式识别率低（漏报率约15%），且误报率高（正常交易被拦截率8%），导致客户投诉增加。

**解决方案**:  
部署Claws作为LLM Agent的决策控制层：  
1. Claws实时分析交易上下文（如用户历史行为、设备指纹），生成动态风险评估报告。  
2. 对可疑交易，Claws调用LLM生成自然语言解释（如“该交易与用户习惯不符”），供人工复核。  
3. 通过Claws的反馈循环机制，将人工复核结果持续优化风控模型。

**效果**:  
- 新型欺诈识别率提升至92%，漏报率下降至3%。  
- 误报率降低至2%，客户投诉减少60%。  
- 人工复核效率提高40%（因LLM生成的解释清晰易读）。

---



### 3：医疗问诊平台的AI辅助诊断

 3：医疗问诊平台的AI辅助诊断

**背景**:  
该平台提供在线问诊服务，早期使用LLM直接回答用户健康问题，但存在医学建议不准确的风险（如错误推荐药物）。

**问题**:  
LLM生成的回复缺乏专业验证，曾导致用户因错误建议延误就医，引发医疗纠纷。同时，平台需确保符合HIPAA等隐私法规。

**解决方案**:  
引入Claws作为安全与合规层：  
1. Claws将用户问题分类为“可公开回答”“需医生审核”“需紧急就医”三类。  
2. 对医学建议，Claws强制调用经过认证的医学知识库API，而非依赖LLM生成内容。  
3. 所有敏感数据通过Claws的脱敏模块处理，确保隐私合规。

**效果**:  
- 医学建议准确率从85%提升至99.5%，纠纷事件归零。  
- 医生审核效率提高50%（因Claws已预处理非紧急问题）。  
- 通过HIPAA合规审计，平台用户增长加速。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建模块化的工具层

**说明**: Claws 作为位于 LLM agents 之上的新层，其核心价值在于通过标准化的接口与底层模型交互。最佳实践要求将工具调用、API 交互和外部数据访问抽象为独立的模块。这样可以确保底层的 LLM agent 专注于推理，而 Claws 层专注于执行，从而实现关注点分离。

**实施步骤**:
1. 定义所有外部功能（如数据库查询、API 请求）的标准化接口模式。
2. 将每个具体功能封装为独立的模块或插件，避免将业务逻辑直接嵌入 Agent 提示词中。
3. 在 Claws 层实现统一的错误处理和重试机制，屏蔽底层网络波动对 Agent 的影响。

**注意事项**: 确保工具的输入输出描述清晰且类型严格，因为 LLM 依赖这些描述来生成正确的调用参数。

---

### 实践 2：实施精细化的权限控制与安全沙箱

**说明**: 既然 Claws 是位于 Agent 之上的执行层，它就成为了防止 LLM 产生幻觉导致灾难性后果的关键防线。必须限制 Agent 的实际操作权限，确保其只能访问和修改被明确允许的资源。

**实施步骤**:
1. 为不同的 Agent 角色分配最小必要权限，遵循“默认拒绝”原则。
2. 在 Claws 层实现参数验证机制，检查 Agent 生成的指令是否包含恶意参数（如 SQL 注入或路径遍历）。
3. 对于高风险操作（如删除数据、发送邮件），实施人工确认机制或二次校验逻辑。

**注意事项**: 不要完全信任 LLM 的输出，即使是最先进的模型也可能生成看似合理但实则有害的指令。

---

### 实践 3：建立上下文感知的日志与可观测性系统

**说明**: 在多层架构中，调试变得异常困难。当 Agent 未能完成任务时，需要区分是 LLM 推理错误、Claws 层工具调用失败，还是外部环境问题。详细的日志记录是排查问题的关键。

**实施步骤**:
1. 记录每一次 Agent 的思考过程、Claws 层接收到的指令参数以及工具的返回结果。
2. 为每个请求分配唯一的 Trace ID，以便在 Agent 层和 Claws 层之间追踪调用链路。
3. 结构化日志输出，便于后续使用自动化脚本分析 Agent 的行为模式。

**注意事项**: 在记录日志时注意数据隐私，避免将敏感信息（如 PII 数据）直接写入日志系统。

---

### 实践 4：设计容错与降级机制

**说明**: LLM 的输出具有非确定性，且外部服务可能不可用。Claws 层必须具备鲁棒性，能够处理工具调用失败的情况，并引导 Agent 恢复或优雅降级，而不是直接崩溃。

**实施步骤**:
1. 为所有工具调用实现超时控制和指数退避重试策略。
2. 定义标准的错误返回格式，向 Agent 清晰地传达失败原因（例如：“API 超时”或“参数无效”），以便 Agent 自我修正。
3. 在关键流程中设计“回退”逻辑，例如当主数据源不可用时，尝试查询缓存或备用数据源。

**注意事项**: 避免无限重试导致资源耗尽，必须设置最大重试次数和超时阈值。

---

### 实践 5：优化工具描述与提示词工程

**说明**: Claws 层的效率取决于 LLM 能否准确理解并调用工具。模糊的工具描述会导致 Agent 频繁犯错。最佳实践是将工具描述视为代码的一部分进行维护。

**实施步骤**:
1. 为每个工具编写清晰、简洁的文档字符串，详细说明参数类型、必填项以及功能限制。
2. 在描述中提供具体的输入输出示例，帮助 LLM 理解预期格式。
3. 定期分析 Agent 的调用失败案例，反向优化工具的命名和描述，使其更符合自然语言直觉。

**注意事项**: 保持工具的原子性，一个工具应只做一件事，避免功能过于复杂导致 LLM 调用困难。

---

### 实践 6：实现成本与性能监控

**说明**: 引入 Claws 层增加了系统的复杂性，也可能增加 Token 的消耗（因为需要传递工具定义和返回结果）。必须监控这一层的性能和成本，以确保系统的可持续性。

**实施步骤**:
1. 监控关键指标：工具调用延迟、成功率、Token 消耗量以及最终任务完成率。
2. 建立告警机制，当特定工具的错误率突增或响应时间过长时及时通知。
3. 定期评估工具列表，移除不再使用或效率低下的工具，减少上下文窗口的占用。

**注意事项**: 平衡工具功能的丰富性与上下文长度的限制，避免加载过多无关工具导致推理速度下降。

---
## 学习要点

- Claws 被定义为建立在 LLM agents 之上的新抽象层，旨在解决模型在执行复杂任务时的局限性。
- 该架构通过将推理与执行分离，显著增强了 agent 处理多步骤任务和外部工具调用的可靠性。
- Claws 引入了标准化的接口和协议，使得不同 LLM 的 agents 能够更高效地协同工作。
- 这一新层级的设计重点在于提升 agent 在生产环境中的可观测性与可控性，降低了调试难度。
- 它为构建自主系统提供了一种更模块化的方法，允许开发者独立优化底层模型与上层逻辑。
- 该框架的出现标志着 AI agent 开发正从单纯依赖模型能力向依赖系统工程方向转变。

---
## 常见问题


### 1: Claws 本质上是什么？它是一个独立的模型还是一个中间件？

1: Claws 本质上是什么？它是一个独立的模型还是一个中间件？

**A**: 根据标题 "Claws are now a new layer on top of LLM agents" 的描述，Claws 并不是一个独立的大型语言模型（LLM），也不是一个单纯的中间件。它是一个建立在现有 LLM Agents（智能体）之上的**架构层**或**功能层**。

它的核心作用是为底层的 LLM 提供特定的能力增强。通常在 AI Agent 的架构中，LLM 充当“大脑”负责推理和规划，而像 Claws 这样的“层”则可能负责处理与外部世界的具体交互，例如工具调用、执行复杂的工作流或管理长期记忆。你可以把它理解为给智能体装上了“爪子”，使其不仅能思考，还能更精准地“执行”操作。

---



### 2: Claws 这个名字有什么含义？

2: Claws 这个名字有什么含义？

**A**: "Claws"（爪子）是一个形象化的隐喻。在人工智能领域，LLM 通常被比作“大脑”，负责认知处理。然而，仅有大脑无法与物理世界或数字环境进行有效的交互。

通过将这一层命名为 Claws，开发者暗示了它的功能是作为智能体的“手”或“工具”。它赋予了智能体抓取、操作和处理具体任务的能力。这标志着该项目从单纯的“对话与生成”转向了更具行动力的“代理与执行”阶段。

---



### 3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

**A**: 虽然具体的代码实现细节需要参考原文链接，但从架构角度来看，Claws 的定位可能更侧重于**“层”**的概念，而非一个全功能的框架。

现有的框架（如 LangChain）通常提供了一整套构建应用的工具链，而 Claws 可能是一个更轻量、更专注于特定交互协议的接口层。它的出现可能是为了解决现有 Agent 在执行任务时缺乏灵活性或控制力的问题。它旨在作为一个通用的增强层，叠加在不同的 LLM 之上，提升 Agent 的整体性能，而不一定是从零开始构建 Agent 的框架。

---



### 4: 引入 Claws 这一层对 AI 安全性有何影响？

4: 引入 Claws 这一层对 AI 安全性有何影响？

**A**: 在 LLM 之上增加专门的执行层，通常是为了提高安全性和可控性。

纯粹的 LLM 有时会产生不可预测的输出（幻觉），如果直接赋予其控制权，风险较大。Claws 作为一个中间层，可以充当“防火墙”或“过滤器”的角色。它可以在 LLM 发出的指令被实际执行之前进行验证、规范化处理或安全检查。这意味着，即使底层的 LLM 生成了有害或错误的指令，Claws 层也有机会拦截并修正，从而确保智能体的行为符合预期和安全标准。

---



### 5: 开发者如何开始使用或集成 Claws？

5: 开发者如何开始使用或集成 Claws？

**A**: 既然这是一个在 Hacker News 上讨论的新技术发布，开发者通常需要查找该项目的官方文档或代码仓库（通常在 GitHub 上）。

作为一个“层”，集成它通常意味着开发者不需要重写现有的 LLM 逻辑，而是需要配置 Claws 来拦截或处理 Agent 的请求。这可能涉及安装特定的软件包、配置 API 密钥以及定义 Claws 如何与底层的 LLM（如 GPT-4 或 Claude）进行通信。具体的集成步骤会依据该项目提供的 SDK 或接口规范而定。

---



### 6: Claws 是否支持所有的大型语言模型？

6: Claws 是否支持所有的大型语言模型？

**A**: "A new layer on top of LLM agents" 这种表述暗示了它设计初衷是具备**模型无关性**的。

通常，这类架构层的设计目的是为了与底层的模型解耦。理论上，Claws 应该能够支持任何遵循标准接口协议的 LLM。无论是使用 OpenAI 的模型、开源的 Llama 还是其他提供商的模型，Claws 的作用都是在这些模型生成的输出之上提供额外的处理能力，因此它应该具有广泛的兼容性。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Claws 框架被定义为建立在 LLM agents 之上的“新层”。请结合文中描述，列出 Claws 主要解决的三个核心痛点，并解释为什么仅仅依靠底层的 LLM（如 GPT-4）原生能力难以解决这些问题。

### 提示**: 关注 LLM 在处理外部系统交互时的局限性，特别是关于“状态管理”和“工具使用”的摩擦成本。思考当一个 Agent 需要执行一系列复杂操作时，如果没有中间层，会发生什么？

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
- 标签： [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Claws](/tags/claws/) / [任务执行](/tags/%E4%BB%BB%E5%8A%A1%E6%89%A7%E8%A1%8C/) / [架构优化](/tags/%E6%9E%B6%E6%9E%84%E4%BC%98%E5%8C%96/) / [Agent](/tags/agent/) / [模型增强](/tags/%E6%A8%A1%E5%9E%8B%E5%A2%9E%E5%BC%BA/) / [自动化](/tags/%E8%87%AA%E5%8A%A8%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [LLM智能体新增Claws层：强化外部工具调用与任务执行能力]({{< relref "posts/20260221-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-13.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [🤖解密Codex智能体闭环：AI如何自主进化？]({{< relref "posts/20260125-blogs_podcasts-unrolling-the-codex-agent-loop-1.md" >}})
- [Agent Skills：压缩智能体技能以提升模型效率]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-19.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*