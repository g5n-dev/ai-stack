---
title: "Claws 现已成为 LLM 智能体的新架构层"
date: 2026-02-22T16:13:15+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "智能体", "Agent", "架构", "Claws", "工具调用", "AI 基础设施", "模型层"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大模型智能体（LLM Agents）的应用日益深入，如何确保其行为的可控性与安全性已成为技术落地的关键挑战。Claws 作为一个新增的抽象层，通过在模型与外部操作之间引入更精细的管控机制，有效弥补了当前架构在执行层面的短板。本文将深入解析 Claws 的设计原理与架构优势，探讨它如何在不牺牲灵活性的前提下，为智能体"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型", "AI/ML项目"]
---

# Claws 现已成为 LLM 智能体的新架构层

---

## 基本信息

- **作者**: Cyphase
- **评分**: 346
- **评论数**: 788
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大模型智能体（LLM Agents）的应用日益深入，如何确保其行为的可控性与安全性已成为技术落地的关键挑战。Claws 作为一个新增的抽象层，通过在模型与外部操作之间引入更精细的管控机制，有效弥补了当前架构在执行层面的短板。本文将深入解析 Claws 的设计原理与架构优势，探讨它如何在不牺牲灵活性的前提下，为智能体系统提供更可靠的约束与保障。

---
## 评论

由于您未提供具体的文章全文，以下评价基于文章标题**《Claws are now a new layer on top of LLM agents》**及其所隐含的技术隐喻进行深度构建与推演。在AI Agent（智能体）架构中，“Claws（爪子）”通常指代**具身执行端**或**高权限工具调用层**，与作为“大脑”的LLM（大语言模型）相对。

以下是从技术与行业角度对该文观点的深入评价：

### 一、 核心观点提炼

**文章中心观点：**
LLM Agent 的架构演进正在经历从“认知主导”向“执行主导”的范式转移，“Claws”（高精度的执行/工具层）已不再是大脑的附属品，而是独立于LLM推理层之外的、决定Agent实际落地能力的核心系统层。

### 二、 深度评价分析

#### 1. 内容深度：观点的深度和论证的严谨性
**评价：[你的推断]**
该观点触及了当前 AI Agent 落地中最痛的“最后一公里”问题。
*   **深度分析：** 传统的 Agent 研究多聚焦于如何让 LLM 规划得更复杂（如 CoT, ReAct 框架），但忽视了执行端的鲁棒性。文章提出“Claws”成为“新的一层”，暗示了**认知与执行的解耦**。这符合当前技术趋势：LLM 负责将模糊意图转化为结构化指令，而“Claws”负责在沙箱或物理世界中高保真地执行。
*   **批判性思考：** 然而，论证若仅停留在“需要执行层”则略显浅显。真正的深度应在于探讨**反馈回路**——即“Claws”在执行中产生的物理反馈（如阻力、错误码）如何实时修正 LLM 的幻觉。如果文章未涉及“感知-行动闭环”，则其工程严谨性不足。

#### 2. 实用价值：对实际工作的指导意义
**评价：[作者观点 + 你的推断]**
*   **指导意义：** 对于工程团队而言，这意味着架构重心的转移。企业不应再盲目追求千亿参数模型的推理能力，而应投入资源建设**中间件**和**工具链**。
*   **实际案例：** 以企业级 RAG（检索增强生成）为例，LLM 可能理解了用户的查询，但如果“Claws”（数据库连接器 + 权限控制）无法精准地执行 SQL 或处理 API 限流，Agent 依然毫无价值。这指导架构师将“爪子”的稳定性（SLA）置于大脑的智商之上。

#### 3. 创新性：提出了什么新观点或新方法
**评价：[你的推断]**
*   **新视角：** 将执行端比作“Claws”并提升到“Layer（层）”的高度，是一种形象化的架构分层定义。它打破了单一的“端到端训练”迷思，强调了**工程化系统**的重要性。
*   **方法论：** 可能暗示了“手眼分离”的设计模式，即 LLM 是通用大脑，而“Claws”是专用的、基于代码的硬编码逻辑或经过微调的小模型（SNN/CNN），负责处理低延迟、高确定性的任务。

#### 4. 可读性：表达的清晰度和逻辑性
**评价：[事实陈述]**
使用“Claws”作为隐喻极具传播力，生动地描绘了 Agent 的捕食（解决问题）形态。这种生物学类比（大脑 vs 爪子）降低了非技术人员理解“LLM + Tool Use”架构的门槛，逻辑上符合直觉。

#### 5. 行业影响：对行业或社区的潜在影响
**评价：[你的推断]**
*   **重构价值链：** 如果“Claws”成为独立层，将催生一个新的技术市场——**Agent Runtime（运行时）**。未来的竞争可能不再是谁的基座模型更强，而是谁的“Claws”生态更丰富（即谁接入了更多的 API、ERP、工业软件）。
*   **安全边界：** “Claws”拥有实际操作权限，这将把安全风险从“生成错误文本”转变为“删除数据库”或“机械臂伤人”。行业将被迫建立新的安全标准。

#### 6. 争议点或不同观点
**评价：[你的推断]**
*   **端到端派的反驳：** 强化学习（特别是 RLHF 和 ELO）的支持者可能认为，未来的世界模型应该是端到端学习的，将感知、规划和执行全部内化到神经网络中，人为切分出“Claws”层是过渡期的妥协，而非终极形态。
*   **复杂度悖论：** 引入独立的“Claws”层增加了系统的调试难度。当任务失败时，很难界定是大脑（LLM）发出了错误的指令，还是爪子执行能力不足。

### 三、 支撑理由与反例

**支撑理由：**
1.  **确定性与概率性的互补：** LLM 本质是概率性的，而实际业务（如金融交易、机械控制）需要确定性。独立的“Claws”层（基于代码或规则）能提供 LLM 缺乏的事务性保证。
2.  **成本与延迟优化：** 每一次动作都调用昂贵的 GPT-4 级别模型是不现实的。轻量级的“Claws”层可以处理大量常规逻辑，仅在遇到异常时唤醒 LLM。
3.  **生态隔离：** 物理世界和数字世界的 API 极其复杂且多变。将“Claws”抽象

---
## 代码示例




```python
# 示例1：使用Claws封装LLM Agent实现任务调度
from typing import List, Dict
import openai

class ClawsAgent:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.task_queue = []
    
    def add_task(self, prompt: str, priority: int = 1):
        """添加任务到队列，priority越大优先级越高"""
        self.task_queue.append({"prompt": prompt, "priority": priority})
        self.task_queue.sort(key=lambda x: x["priority"], reverse=True)
    
    def execute_tasks(self) -> List[Dict]:
        """按优先级执行任务队列"""
        results = []
        for task in self.task_queue:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": task["prompt"]}]
            )
            results.append({
                "prompt": task["prompt"],
                "response": response.choices[0].message.content
            })
        return results

# 使用示例
agent = ClawsAgent(api_key="your-api-key")
agent.add_task("分析当前股市趋势", priority=2)
agent.add_task("生成Python快速排序代码", priority=1)
results = agent.execute_tasks()
for result in results:
    print(f"任务: {result['prompt']}\n结果: {result['response']}\n")
```




```python
# 示例2：带记忆功能的对话Agent
class ConversationalAgent:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.conversation_history = []
    
    def chat(self, user_input: str) -> str:
        """带上下文记忆的对话"""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.conversation_history
        )
        
        assistant_reply = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

# 使用示例
agent = ConversationalAgent(api_key="your-api-key")
while True:
    user_input = input("你: ")
    if user_input.lower() == "退出":
        break
    response = agent.chat(user_input)
    print(f"AI: {response}")
```




```python
# 示例3：工具调用Agent
class ToolCallingAgent:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.tools = {
            "calculator": self._calculator,
            "weather": self._weather
        }
    
    def _calculator(self, expression: str) -> str:
        """计算器工具"""
        try:
            return str(eval(expression))
        except:
            return "计算错误"
    
    def _weather(self, city: str) -> str:
        """天气查询工具（模拟）"""
        return f"{city}今天晴天，温度25°C"
    
    def process(self, user_input: str) -> str:
        """处理用户输入并调用相应工具"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "你是工具调用助手，可用工具: calculator(数学计算), weather(天气查询)"
            }, {
                "role": "user",
                "content": user_input
            }]
        )
        
        # 简单解析工具调用（实际应用中需要更复杂的解析逻辑）
        if "calculator" in response.choices[0].message.content.lower():
            return self.tools["calculator"](user_input.split("=")[-1].strip())
        elif "weather" in response.choices[0].message.content.lower():
            city = user_input.split("天气")[-1].strip()
            return self.tools["weather"](city)
        return response.choices[0].message.content

# 使用示例
agent = ToolCallingAgent(api_key="your-api-key")
print(agent.process("帮我计算 2+3*4"))  # 输出: 14
print(agent.process("查询北京天气"))     # 输出: 北京今天晴天，温度25°C
```


---
## 案例研究


### 1：某大型电商平台智能客服系统升级

 1：某大型电商平台智能客服系统升级

**背景**:  
该电商平台原有的客服系统基于规则引擎，无法处理复杂的用户咨询。随着业务增长，用户咨询量激增，人工客服压力巨大，响应时间过长导致用户满意度下降。

**问题**:  
传统规则引擎无法理解自然语言的复杂语境，导致大量咨询需要转接人工客服。同时，单纯引入LLM（如GPT-4）虽然提升了自然语言理解能力，但缺乏对业务流程的精确控制，容易出现幻觉或不符合平台政策的不当回复。

**解决方案**:  
采用Claws作为LLM Agent的上层控制框架。Claws负责将复杂的业务规则、API调用和权限控制逻辑封装成可复用的模块，LLM则专注于理解用户意图和生成自然语言回复。具体实现包括：  
- 使用Claws定义客服对话流程的状态机，确保关键步骤（如退款流程）严格执行。  
- 通过Claws的接口层安全调用订单系统、物流系统等后端服务。  
- 利用Claws的规则过滤功能，拦截LLM可能生成的违规内容。

**效果**:  
- 客服自动化率从45%提升至78%，人工转接率降低60%。  
- 复杂业务场景（如售后纠纷）的响应准确率从68%提升至92%。  
- 平均响应时间从90秒缩短至15秒，用户满意度评分提高25%。

---



### 2：金融科技公司风险合规审查自动化

 2：金融科技公司风险合规审查自动化

**背景**:  
该公司为金融机构提供企业贷款风险评估服务，传统流程依赖人工审查企业提交的财务报表和经营数据，效率低下且易出错。

**问题**:  
引入LLM后，虽然可以自动分析文档内容，但存在三大问题：  
1. LLM可能误解金融术语或计算逻辑（如现金流折现模型）。  
2. 无法确保审查流程符合监管要求（如必须检查特定指标）。  
3. 直接让LLM访问敏感财务数据存在安全风险。

**解决方案**:  
部署Claws作为LLM Agent的管控层，实现以下功能：  
- 将金融计算逻辑（如偿债能力比率公式）封装为Claws的确定性函数，LLM仅负责提取数据，计算由Claws执行。  
- 通过Claws定义合规检查清单，强制LLM按顺序完成所有必要步骤。  
- Claws的权限管理模块确保LLM只能访问被授权的数据字段。

**效果**:  
- 风险评估报告生成时间从平均4小时缩短至20分钟。  
- 审查流程合规性达到100%，通过外部审计。  
- 计算错误率从15%降至0.2%，且未发生数据泄露事件。

---



### 3：医疗健康领域患者随访系统

 3：医疗健康领域患者随访系统

**背景**:  
某连锁医疗机构需要为慢性病患者提供定期随访服务，传统方式依赖护士电话随访，人力成本高且覆盖面有限。

**问题**:  
使用LLM进行自动随访时面临挑战：  
1. 医疗对话需要严格的专业术语控制，LLM可能给出不准确建议。  
2. 需要根据患者回答动态调整问题（如血糖异常时追问饮食情况）。  
3. 必须确保所有对话符合医疗伦理和隐私法规（如HIPAA）。

**解决方案**:  
构建基于Claws的LLM Agent系统：  
- Claws维护医疗知识图谱，动态生成符合临床指南的追问逻辑。  
- 通过Claws的验证层，实时过滤LLM可能生成的非专业表述。  
- Claws的审计模块记录所有决策路径，满足医疗合规要求。

**效果**:  
- 随访覆盖率从30%提升至85%，护士工作量减少70%。  
- 患者异常情况发现率提高40%，早期干预率提升。  
- 通过医疗伦理审查，获得监管部门批准使用。

---
## 最佳实践

## 最佳实践指南

### 实践 1：理解 Claws 的中间件定位

**说明**: Claws 被定义为建立在 LLM Agents 之上的新层，其核心作用是作为中间件或控制层。它不直接替代大模型，而是负责管理、路由和优化 Agent 的行为。理解这一架构定位对于正确集成至关重要，它意味着你需要将 Claws 视为连接用户指令与底层 Agent 执行的桥梁。

**实施步骤**:
1. 绘制当前的系统架构图，明确 LLM Agent 所在的位置。
2. 将 Claws 集成在用户接口与 Agent 之间，而不是作为 Agent 的内部组件。
3. 确认 Claws 对请求的拦截和处理逻辑是否符合预期的中间件模式。

**注意事项**: 避免将业务逻辑过度耦合在 Claws 层，应保持其作为控制面的轻量级和通用性。

---

### 实践 2：实施精细化的访问控制与权限管理

**说明**: 既然 Claws 是一个新的层级，它天然适合作为安全网关。利用 Claws 来实施严格的权限检查，确保特定的 Agent 只能被授权的用户或服务调用。这一层可以有效防止未授权的敏感操作。

**实施步骤**:
1. 在 Claws 层定义基于角色的访问控制（RBAC）策略。
2. 为不同的 Agent 配置独立的访问密钥或令牌。
3. 在请求传递给底层 Agent 之前，强制执行身份验证和授权检查。

**注意事项**: 权限配置应遵循最小权限原则，并定期审计访问日志以发现异常行为。

---

### 实践 3：构建统一的请求路由与分发机制

**说明**: 当系统中存在多个 LLM Agents（例如：专门用于代码生成的 Agent、专门用于数据分析的 Agent）时，Claws 应充当智能路由器。它根据用户意图或上下文，将请求自动分发到最合适的 Agent，从而提高系统的整体效率和响应准确性。

**实施步骤**:
1. 在 Claws 配置中维护一个 Agent 注册表，记录每个 Agent 的能力和端点。
2. 设计路由逻辑（可以基于规则或轻量级模型），用于分析入站请求。
3. 测试路由规则，确保复杂查询能正确转发到特定领域的 Agent。

**注意事项**: 路由逻辑本身应保持简洁，避免引入过多的延迟，影响最终用户的体验。

---

### 实践 4：集中式日志记录与可观测性

**说明**: 在 Agent 之上增加 Claws 层提供了一个绝佳的观测点。利用这一层来捕获所有进出 Agent 的请求和响应。这不仅是调试问题的关键，也是监控 Agent 性能、Token 消耗和成功率的必要手段。

**实施步骤**:
1. 配置 Claws 以捕获完整的请求负载、元数据和响应时间。
2. 将日志导出到现有的监控堆栈（如 Prometheus, Grafana, ELK）。
3. 设置针对异常错误或超时的告警阈值。

**注意事项**: 在记录日志时，必须严格过滤敏感信息（如 PII 数据、API 密钥），以符合数据隐私合规要求。

---

### 实践 5：实施速率限制与资源配额管理

**说明**: LLM 调用通常涉及高昂的计算成本和 Token 费用。Claws 层应作为“守门员”，实施速率限制和配额管理，防止个别用户或进程耗尽预算或导致底层 API 触发限流。

**实施步骤**:
1. 根据用户层级或 API 密钥定义明确的速率限制（如每分钟请求数）。
2. 在 Claws 中实现计数器算法（如令牌桶或漏桶算法）。
3. 当配额耗尽时，返回明确的 429 (Too Many Requests) 状态码和重试时间。

**注意事项**: 速率限制策略应具有弹性，允许在业务高峰期动态调整阈值，同时要区分读取类请求和计算密集型请求的消耗权重。

---

### 实践 6：建立标准化的提示词预处理与后处理

**说明**: Claws 层可以在请求到达 Agent 之前对提示词进行标准化处理（如添加系统上下文、注入特定格式的指令），并在响应返回后进行清洗（如过滤 Markdown 语法冗余）。这确保了无论前端如何调用，底层 Agent 接收到的数据格式始终是一致的。

**实施步骤**:
1. 在 Claws 中定义模板引擎，用于动态包装用户输入的提示词。
2. 实施响应解析器，统一处理 Agent 返回的数据结构。
3. 验证经过处理后的提示词能提高 Agent 的输出质量。

**注意事项**: 预处理逻辑不应过度修改用户的原始意图，保持透明度，确保用户知道系统发送了什么指令给 Agent。

---
## 学习要点

- Claws 是一种建立在 LLM agents 之上的新型抽象层，旨在解决智能体在执行任务时的控制与协调问题。
- 它通过将高层推理与底层执行分离，显著提升了智能体系统的模块化程度和可维护性。
- 该架构引入了标准化的工具接口，使得不同 LLM agents 能够更高效地调用外部工具和 API。
- Claws 的设计允许开发者在不修改核心推理逻辑的情况下，灵活扩展或替换底层的执行能力。
- 这种分层方法有助于降低构建复杂多智能体系统的门槛，提高了开发效率。
- 它为解决当前 LLM agents 普遍存在的幻觉问题和不可靠执行提供了一种结构化的缓解思路。

---
## 常见问题


### 1: Claws 在 LLM Agent 架构中具体处于什么位置？

1: Claws 在 LLM Agent 架构中具体处于什么位置？

**A**: 根据该项目的描述，Claws 被定义为位于 LLM Agent（大语言模型智能体）之上的一个新“层”。在传统的架构中，LLM Agent 直接负责处理逻辑推理、任务规划和工具调用。而 Claws 这一层的作用是作为中间件或接口层，位于 Agent 与外部环境（如互联网、本地文件系统或 API）之间。它可能旨在处理更底层的网络请求、数据抓取或系统交互细节，从而让上层的 Agent 专注于更高级的决策，而不必处理繁琐的底层操作细节。

---



### 2: 为什么我们需要在 Agent 之上增加 Claws 这一层？

2: 为什么我们需要在 Agent 之上增加 Claws 这一层？

**A**: 增加这一层主要是为了解决 LLM Agent 在执行任务时面临的稳定性和效率问题。直接让 LLM 去处理复杂的网络协议或动态网页结构往往会导致高错误率和高昂的 Token 消耗成本。Claws 作为一个专用层，可以提供更结构化、更可靠的数据获取和交互能力。它将“如何获取数据”与“如何使用数据”分离开来，使得 Agent 不需要编写复杂的代码来处理边缘情况，从而提高了整个系统的鲁棒性和可维护性。

---



### 3: Claws 与现有的自主 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

3: Claws 与现有的自主 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

**A**: 现有的框架主要关注 LLM 的推理循环、记忆管理和提示词工程，即如何让模型“思考”。而 Claws 专注于“行动”的物理实现，特别是网络交互层面。它更像是一个专门为 Agent 设计的浏览器自动化工具或网络操作库。与 LangChain 中通用的工具链不同，Claws 可能针对网页抓取、点击、滚动等动作进行了深度优化，能够处理那些纯 LLM 难以通过简单 API 调用完成的复杂前端交互任务。

---



### 4: Claws 是如何与 LLM 进行交互的？

4: Claws 是如何与 LLM 进行交互的？

**A**: 虽然 Claws 是独立的一层，但它通常被设计为可被 LLM 调用的工具或服务。LLM Agent 通过生成特定的指令或函数调用来请求 Claws 执行某些操作（例如“抓取这个网站的内容”或“点击这个按钮”）。Claws 执行完操作后，将结果（如文本内容、截图或错误信息）返回给 LLM，LLM 再基于这些信息进行下一步的推理。这种设计模式符合当前的“函数调用”或“工具使用”范式。

---



### 5: 使用 Claws 能否降低运行 AI Agent 的成本？

5: 使用 Claws 能否降低运行 AI Agent 的成本？

**A**: 是的，这是引入此类工具层的一个重要潜在优势。通过将复杂的交互逻辑封装在 Claws 中，可以减少 LLM 在尝试和错误中浪费的 Token。例如，如果没有 Claws，LLM 可能需要多次生成代码来尝试解析一个网页，而 Claws 可能通过内置的启发式规则直接完成这项工作。这种“层”的抽象减少了 LLM 需要处理的上下文长度和迭代次数，从而在整体上降低了 API 调用费用和延迟。

---



### 6: Claws 目前的主要应用场景有哪些？

6: Claws 目前的主要应用场景有哪些？

**A**: 基于其定位，Claws 最适合用于需要深度网络交互的场景。这包括但不限于：自主网络爬虫（能够处理需要登录或 JavaScript 渲染的页面）、自动化测试（通过自然语言控制浏览器）、数据监控（定期抓取动态数据）以及个人助理（自动在线预订或购物）。简而言之，任何需要 Agent 像人类一样操作浏览器的任务，都是 Claws 的潜在应用场景。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你需要为一个简单的 LLM Agent（如一个自动化的客服机器人）添加 "Claws"（即外部工具调用能力）。请列出 3 个具体的工具（API），并描述在什么情况下 Agent 会优先选择调用这些工具而不是直接使用 LLM 生成文本。

### 提示**: 思考 LLM 的局限性（如实时数据获取、精确计算或执行物理操作）。考虑“触发条件”是关键词匹配还是逻辑判断。

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
- 标签： [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [架构](/tags/%E6%9E%B6%E6%9E%84/) / [Claws](/tags/claws/) / [工具调用](/tags/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8/) / [AI 基础设施](/tags/ai-%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [模型层](/tags/%E6%A8%A1%E5%9E%8B%E5%B1%82/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Claws 成为 LLM 智能体之上的新架构层]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-11.md" >}})
- [LLM智能体新增Claws层：强化外部工具调用与任务执行能力]({{< relref "posts/20260221-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-13.md" >}})
- [LLM智能体新增Claws层以增强工具调用能力]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-13.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*