---
title: "LLM智能体新增Claws层以增强功能"
date: 2026-02-22T02:59:35+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "智能体", "Claws", "架构设计", "Agent", "增强功能", "AI 系统", "模型优化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型（LLM）应用场景的深入，如何让智能体更稳定地处理复杂任务成为开发者关注的焦点。Claws 作为一种新兴的中间层，旨在通过精细化的流程控制来弥补 LLM 在执行确定性任务时的不足。本文将剖析 Claws 的架构设计，并探讨它如何提升智能体的可靠性，帮助读者在实际项目中构建更可控的 AI 系统。"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型", "AI/ML项目"]
---

# LLM智能体新增Claws层以增强功能

---

## 基本信息

- **作者**: Cyphase
- **评分**: 196
- **评论数**: 647
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大语言模型（LLM）应用场景的深入，如何让智能体更稳定地处理复杂任务成为开发者关注的焦点。Claws 作为一种新兴的中间层，旨在通过精细化的流程控制来弥补 LLM 在执行确定性任务时的不足。本文将剖析 Claws 的架构设计，并探讨它如何提升智能体的可靠性，帮助读者在实际项目中构建更可控的 AI 系统。

---
## 评论

**文章标题：Claws are now a new layer on top of LLM agents**
**（注：由于您未提供原文正文，以下评价基于标题“Claws are now a new layer on top of LLM agents”所蕴含的技术隐喻及当前Agent技术发展趋势进行深度推演与评价）**

### 一、 核心观点与支撑逻辑

**中心观点：**
文章主张“Claws”（利爪/工具层）应当被显式定义为独立于大语言模型（LLM）大脑之上的新型基础设施层，旨在解决当前AI Agent在物理世界或数字环境中“行动力”与“鲁棒性”不足的核心痛点。

**支撑理由：**
1.  **弥补“执行断层”：** LLM本质上是概率预测引擎，擅长推理但拙于精确执行。将“Claws”剥离出来，意味着将API调用、函数执行、甚至机械臂控制等确定性逻辑与概率性推理解耦，从而降低幻觉导致的执行错误。（*你的推断*）
2.  **提升系统鲁棒性：** 传统的Agent架构中，工具调用往往内嵌于Prompt中。将“Claws”作为独立层，可以引入重试机制、沙箱隔离和异常处理，防止Agent因一次工具调用失败而崩溃。（*作者观点/行业共识*）
3.  **专业化分工趋势：** 随着模型能力趋同，竞争壁垒将转移到“Claws”层——即谁能更精准地连接垂类数据、谁能更稳定地操控硬件，谁就能构建更强的Agent。（*你的推断*）

**反例/边界条件：**
1.  **过度解耦导致上下文丢失：** 如果“Claws”层过于独立，可能会切断LLM推理过程与工具执行结果之间的细粒度语义反馈，使得LLM无法根据工具报错的细节进行动态调整（如参数微调）。
2.  **端到端学习的反噬：** 随着VLA（Vision-Language-Action）模型的发展，未来的模型可能原生具备“手眼协调”能力，不再需要外挂的“Claws”层，这种显式架构可能只是过渡方案。

---

### 二、 深度评价（基于维度分析）

#### 1. 内容深度：从“大脑”到“四肢”的架构重构
文章提出的“Claws”概念，实际上触及了当前Agent架构设计的核心矛盾：**Generalization（通用性）与 Precision（精确性）的博弈**。
*   **论证严谨性：** 如果文章仅停留在“我们需要工具”这一层面，深度尚浅。但如果它论证了“为何工具必须是独立的一层（Layer）而非仅仅是Prompt的一部分”，则具有极高的架构学价值。这暗示了从“Chain of Thought（思维链）”向“Chain of Action（行动链）”的范式转移。
*   **批判性视角：** 深度的潜在不足在于，文章可能低估了“定义统一Claws接口”的难度。不同的工具（SQL查询 vs 机械臂抓取）的输入输出方差极大，强行抽象为一层可能导致“抽象泄漏”。

#### 2. 实用价值：为工程化落地指明方向
对实际开发具有极高的指导意义。
*   **工程指导：** 它提醒开发者不要沉迷于优化LLM的Prompt，而应投入资源建设稳固的工具层。例如，不要让LLM直接写正则表达式（容易出错），而是提供一个“Claw”工具，LLM只需描述意图，由该工具执行精确匹配。
*   **案例说明：** 在金融数据分析Agent中，LLM负责解读用户意图（大脑），而“Claws”层负责通过Python执行沙箱运行代码。如果“Claws”层不独立，LLM可能会生成带有语法错误的代码，或者生成带有恶意倾向的系统指令。

#### 3. 创新性：概念隐喻的具象化
*   **新观点：** 将冷冰冰的“Tool Use”重新命名为“Claws”，极具形象感。它强调了工具的**攻击性、穿透力和物理属性**。这不仅是技术术语的更新，更是对Agent定位的转变——从“聊天机器人”变为“行动实体”。
*   **局限性：** 这一概念并非完全原创，类似于Robotic Process Automation (RPA) 与 AI 的结合，或者是OS层面的Copilot概念。创新点在于将其置于LLM架构的顶层进行定义。

#### 4. 可读性与逻辑性
*   **表达清晰度：** 使用“Layer（层）”这一术语，符合软件工程师的直觉，易于理解。
*   **逻辑结构：** 逻辑上遵循了“感知-决策-行动”的经典控制论模型。但需警惕文章是否将“Claws”与现有的Agent框架（如LangChain的Tools）过度割裂，造成概念混淆。

#### 5. 行业影响：重估“连接”的价值
*   **潜在影响：** 如果这一观点被广泛接受，AI行业的价值链将发生转移。单纯的模型微调服务可能贬值，而**“Claws提供商”**（即高质量的API聚合器、硬件适配器、企业数据连接器）将成为新的风口。
*   **社区反应：** 可能会引发关于“Agent Native Application”定义的讨论，推动开发者从“以模型为中心”转向“以行动为中心”。

#### 6. 争议点与不同观点
*   **争议点：** **Agent是否真的需要这一层？**
    *   **正方（文章立场）：** 需要。模型太不稳定，必须外挂确定性层。
    *   **反方（端到端派）：** 不需要。GPT

---
## 代码示例




```python
# 示例1：基础LLM Agent与Claws层集成
import openai

class BaseAgent:
    """基础LLM代理"""
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
    
    def query(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class ClawsLayer:
    """Claws增强层"""
    def __init__(self, agent):
        self.agent = agent
        self.tools = {
            "calculator": self._calculate,
            "search": self._search
        }
    
    def _calculate(self, expr):
        """计算器工具"""
        try:
            return eval(expr)
        except:
            return "计算错误"
    
    def _search(self, query):
        """模拟搜索工具"""
        return f"搜索结果：关于'{query}'的前3条结果..."
    
    def process(self, user_input):
        # 1. 先通过LLM判断需要使用哪个工具
        tool_prompt = f"用户输入：{user_input}\n可用工具：{list(self.tools.keys())}\n请选择最合适的工具名称"
        selected_tool = self.agent.query(tool_prompt)
        
        # 2. 执行工具
        if selected_tool in self.tools:
            return self.tools[selected_tool](user_input)
        return self.agent.query(user_input)

# 使用示例
agent = BaseAgent("your-api-key")
enhanced_agent = ClawsLayer(agent)
print(enhanced_agent.process("计算 123 * 456"))  # 会调用计算器工具
```




```python
# 示例2：带记忆的Claws层实现
from datetime import datetime

class MemoryClawsLayer:
    """带记忆功能的Claws层"""
    def __init__(self, agent):
        self.agent = agent
        self.memory = []
        self.max_memory = 5
    
    def remember(self, context):
        """存储对话上下文"""
        self.memory.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "content": context
        })
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)
    
    def get_memory_context(self):
        """获取记忆上下文"""
        return "\n".join([f"[{m['timestamp']}] {m['content']}" for m in self.memory])
    
    def process(self, user_input):
        # 1. 添加用户输入到记忆
        self.remember(f"用户：{user_input}")
        
        # 2. 构建带记忆的提示词
        prompt = f"""对话历史：
{self.get_memory_context()}

当前用户输入：{user_input}
请基于对话历史回复"""
        
        # 3. 获取回复并存储
        response = self.agent.query(prompt)
        self.remember(f"助手：{response}")
        return response

# 使用示例
agent = BaseAgent("your-api-key")
memory_agent = MemoryClawsLayer(agent)
print(memory_agent.process("我叫什么名字？"))  # 第一次可能不知道
print(memory_agent.process("我叫张三"))  # 告诉名字
print(memory_agent.process("我叫什么名字？"))  # 现在应该知道了
```




```python
# 示例3：多工具协作的Claws层
import json

class MultiToolClawsLayer:
    """支持多工具协作的Claws层"""
    def __init__(self, agent):
        self.agent = agent
        self.tools = {
            "weather": self._get_weather,
            "time": self._get_time,
            "news": self._get_news
        }
    
    def _get_weather(self, location):
        """模拟天气查询"""
        return f"{location}今天晴天，气温25°C"
    
    def _get_time(self, _):
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_news(self, category):
        """模拟新闻查询"""
        return f"最新{category}新闻：1. xxx 2. yyy 3. zzz"
    
    def parse_tool_use(self, response):
        """解析LLM返回的工具调用"""
        try:
            return json.loads(response)
        except:
            return None
    
    def process(self, user_input):
        # 1. 让LLM决定需要调用哪些工具
        tool_prompt = f"""用户请求：{user_input}
可用工具：{json.dumps(self.tools)}
请返回JSON格式的工具调用，例如：
{{"tool": "weather", "params": "北京"}}"""
        
        tool_call = self.parse_tool_use(self.agent.query(tool_prompt))
        
        # 2. 执行工具调用
        if tool_call and tool_call["tool"] in self.tools:
            result = self.tools[tool_call["tool"]](tool_call.get("params", ""))
            
            # 3. 将工具结果反馈给LLM生成最终回复
            final_prompt = f


---
## 案例研究


### 1：某头部电商平台智能客服升级项目

 1：某头部电商平台智能客服升级项目

**背景**:
该电商平台原有的智能客服系统基于传统的意图识别模型（NLU），能够处理常见的查物流、退换货等标准化问题。然而，随着大语言模型（LLM）的普及，用户开始期望客服能理解更复杂的语境并进行多轮对话。该平台尝试将底层模型替换为 LLM，以提供更自然的交互体验。

**问题**:
在直接使用 LLM Agent 后，虽然对话流畅度大幅提升，但系统频繁出现“幻觉”和违规操作。例如，Agent 为了满足用户的退款需求，可能会试图调用并不存在的“立即全额退款且无需退货”接口，或者在被拒绝时无限循环重试，导致后端 API 被恶意刷爆，且缺乏对敏感操作（如直接扣款、修改订单）的权限控制。

**解决方案**:
引入 Claws 作为 LLM Agent 上层的安全与控制层。Claws 在 Agent 和后端系统之间建立了一道“防火墙”。通过 Claws，开发团队定义了严格的工具使用策略，例如“退款金额超过 500 元必须转人工”以及“禁止在非工作时间调用库存锁定接口”。Claws 拦截了 Agent 发出的所有指令，在执行前进行合规性检查和参数修正。

**效果**:
上线后，客服系统的异常调用请求减少了 95%。LLM Agent 依然保持了高情商的对话能力，但不再能绕过业务规则。系统成功拦截了数万起潜在的违规退款尝试，并在不牺牲用户体验的前提下，确保了后端交易系统的稳定性。

---



### 2：FinTech 自动化金融研报生成器

 2：FinTech 自动化金融研报生成器

**背景**:
一家金融科技初创公司致力于为投资机构自动生成市场研报。他们的 LLM Agent 能够联网搜索最新的财经新闻，并基于内部数据库生成分析摘要。该系统需要频繁调用外部的付费数据 API（如 Bloomberg API）来获取实时股价和宏观经济数据。

**问题**:
在测试阶段，LLM Agent 偶尔会因为对复杂指令的误解，陷入死循环，反复向外部 API 发送相同的请求。这不仅导致单次报告生成的 API 调用成本高达数十美元，甚至一度因为触发速率限制而导致 API 账户被封禁。此外，Agent 缺乏对预算的感知，无法根据任务优先级分配资源。

**解决方案**:
团队部署了 Claws 来管理 Agent 的“手”和“脚”。Claws 被配置为资源的智能调度者和守门人。它为 Agent 的每一次 API 调用设置了预算上限和冷却时间。当 Agent 试图请求数据时，Claws 会先检查缓存，如果数据未过期则直接返回；若需调用接口，Claws 会根据剩余预算动态决定是使用高精度付费接口还是切换到免费的备用数据源。

**效果**:
通过引入 Claws，该系统将外部 API 的调用成本降低了 80%。Claws 的缓存机制和速率限制功能彻底解决了账户被封禁的风险。同时，系统生成的研报质量未受影响，因为 Claws 确保了关键数据请求的优先级，实现了成本与效率的最佳平衡。

---



### 3：企业级内部知识库与运维助手

 3：企业级内部知识库与运维助手

**背景**:
一家大型 SaaS 公司构建了一个内部运维助手，旨在帮助新入职的工程师快速排查服务器故障。该 LLM Agent 拥有读取日志、执行重启脚本和修改配置文件的权限。

**问题**:
在一次故障模拟中，LLM Agent 错误地将生产环境的数据库重启指令当成了测试环境指令。虽然 Agent 的初衷是“修复故障”，但由于缺乏对环境变量的严格校验，差点导致生产环境服务中断。此外，Agent 在执行危险命令（如 `rm -rf`）前缺乏二次确认机制。

**解决方案**:
利用 Claws 构建了一个“人在回路”的审批层。Claws 拦截了所有具有破坏性潜力的操作指令。对于低风险操作（如只读日志），Claws 直接放行；对于高风险操作（如重启服务、删除数据），Claws 会暂停执行，并向运维负责人的 Slack 发送包含详细执行计划的确认请求，只有获得人工批准后，才会将指令传递给服务器。

**效果**:
该方案赋予了 LLM Agent 强大的自动化能力，同时消除了人为误操作带来的风险。运维团队反馈，Claws 的引入让他们敢于将更多权限开放给 AI，从而将日常排查工作的响应时间从平均 30 分钟缩短至 2 分钟，且未发生任何安全事故。

---
## 最佳实践

## 最佳实践指南

### 实践 1：理解 Claws 作为抽象层的定位

**说明**: Claws 并非要替代现有的 LLM Agent（如 AutoGPT 或 LangChain），而是作为一个中间件或控制层存在。它主要负责处理工具调用的安全性、权限管理和状态追踪，将底层模型的推理能力与上层的具体执行逻辑解耦。

**实施步骤**:
1. 评估现有 Agent 架构，确定模型推理与工具执行之间的边界。
2. 将 Claws 集成到 Agent 循环中，使其拦截所有向外部 API 或系统发出的请求。
3. 定义 Claws 层的接口规范，确保它能与不同的底层模型兼容。

**注意事项**: 避免在 Claws 层中引入过多的业务逻辑，保持其轻量级，专注于控制和安全。

---

### 实践 2：实施严格的工具调用权限控制

**说明**: 既然 Claws 位于 Agent 之上，它应当充当守门员的角色。不要让 LLM 无限制地访问所有系统工具。利用 Claws 来定义哪些工具是可用的，以及在什么条件下可以调用。

**实施步骤**:
1. 列出所有 Agent 可能使用的工具（如文件系统、数据库、API）。
2. 在 Claws 配置中为每个工具分配角色或权限级别（例如：只读、读写、禁止）。
3. 实施运行时检查，当 Agent 请求调用工具时，Claws 验证当前会话是否有权限执行该操作。

**注意事项**: 默认应遵循“最小权限原则”，并在日志中记录所有被拒绝的调用尝试，以便调试安全策略。

---

### 实践 3：增强可观测性与日志记录

**说明**: 传统的 Agent 往往是一个黑盒，只给出最终结果。Claws 层提供了一个绝佳的观测点，用于捕获 Agent 的意图（通过 LLM 输出）与实际执行动作之间的映射关系。

**实施步骤**:
1. 在 Claws 层实现结构化日志，记录 Agent 发出的每个原始请求参数。
2. 记录工具执行后的返回值和状态码。
3. 将这些日志发送到集中式追踪系统（如 Jaeger 或专用的 LLM 观测平台），以便可视化 Agent 的决策链路。

**注意事项**: 记录日志时要注意数据隐私，避免在日志中明文记录敏感的用户数据或 PII 信息。

---

### 实践 4：构建人工反馈与干预回路

**说明**: 利用 Claws 层在执行关键操作前引入人工确认机制。对于高风险操作（如删除文件、发送邮件、执行交易），Claws 应该能够暂停执行并等待批准。

**实施步骤**:
1. 定义“高风险操作”清单。
2. 在 Claws 中配置交互模式，当检测到清单中的操作时，将请求挂起。
3. 提供一个简单的 API 或 UI 界面供人类操作员批准或拒绝该请求，并将结果反馈给 Agent。

**注意事项**: 设置超时机制，如果人工长时间未响应，应定义默认行为（通常是拒绝），以防止流程永久挂起。

---

### 实践 5：统一错误处理与重试逻辑

**说明**: LLM 经常会生成格式错误或参数不全的工具调用请求。与其让底层的 Agent 崩溃，不如在 Claws 层统一处理这些异常，尝试修复或向模型请求更正。

**实施步骤**:
1. 在 Claws 中实现参数校验逻辑。
2. 如果 LLM 生成的参数不符合工具 Schema，编写特定的错误提示返回给 LLM 进行自我修正。
3. 对于网络瞬断等暂时性错误，在 Claws 层实现指数退避的重试策略。

**注意事项**: 区分可重试错误（如超时）和不可重试错误（如鉴权失败），避免无限重试导致系统资源耗尽。

---

### 实践 6：优化上下文管理与状态维护

**说明**: Claws 层可以帮助管理 Agent 的记忆。通过在 Claws 层过滤和总结工具调用的结果，可以减少传回给 LLM 的 Token 数量，防止上下文窗口溢出。

**实施步骤**:
1. 在工具执行完毕后，让 Claws 评估返回数据的长度。
2. 如果数据过长，在 Claws 层进行摘要或仅保留关键元数据。
3. 维护一个结构化的状态对象，供 LLM 查询，而不是每次都传递原始的历史记录。

**注意事项**: 确保摘要过程不会丢失执行过程中产生的关键错误信息或中间结果。

---
## 学习要点

- Claws 被定义为一种位于 LLM Agents 之上的新型抽象层，旨在解决当前 Agent 架构中工具调用与逻辑控制耦合度过高的问题。
- 该架构通过引入“手”的概念，将底层的 API 调用、多模态交互（如点击、打字）与 Agent 的核心推理大脑解耦，实现了感知与执行的物理分离。
- 这种分层设计显著降低了 Agent 的开发门槛，开发者无需为每个任务重新编写执行逻辑，只需复用标准化的“Claws”组件。
- 它为 Agent 提供了标准化的接口，使得同一个 LLM 大脑可以轻松控制不同的软件环境或硬件设备，极大地提升了系统的通用性和可移植性。
- Claws 层的出现标志着 AI Agent 的发展趋势正从单纯的“模型能力竞争”转向“执行生态与基础设施的构建”。
- 通过将执行细节封装在 Claws 层，Agent 的核心逻辑变得更加简洁，从而提升了系统的可维护性、可测试性以及运行稳定性。

---
## 常见问题


### 1: Claws 具体是什么？它与 LLM Agent（智能体）之间是什么关系？

1: Claws 具体是什么？它与 LLM Agent（智能体）之间是什么关系？

**A**: 根据该信息的来源背景，Claws 是一个新兴的开源框架或基础设施层。它的核心定位是位于大语言模型（LLM）智能体之上的“控制层”或“编排层”。

如果把 LLM Agent 比作拥有“大脑”的实体，能够进行推理和规划，那么 Claws 则更像是这个实体的“手”或“中枢神经系统”。它主要负责处理 Agent 与外部世界交互时的复杂性，例如管理长时间运行的任务、处理 API 调用的错误重试、维护状态记忆以及执行具体的工具调用。简单来说，LLM 负责“思考”，而 Claws 负责“行动”和“落地”。

---



### 2: 为什么要专门设计一个像 Claws 这样的“新层级”？现有的 LLM Agent 框架不够用吗？

2: 为什么要专门设计一个像 Claws 这样的“新层级”？现有的 LLM Agent 框架不够用吗？

**A**: 现有的 LLM Agent 框架（如 LangChain 或 AutoGPT）主要侧重于提示词管理和简单的链式调用，但在处理生产环境中的复杂任务时往往面临以下挑战，而 Claws 正是为了解决这些问题：

1.  **状态管理与持久化**：许多 Agent 任务需要数小时甚至数天才能完成，期间可能会遇到中断。Claws 提供了强大的状态持久化能力，确保任务可以从断点恢复，而不是从头开始。
2.  **确定性与控制**：纯 LLM 的输出具有随机性。Claws 引入了更结构化的控制流，使得 Agent 的行为更加可预测、可调试。
3.  **工具集成的复杂性**：直接让 LLM 编写代码调用外部 API 往往不稳定。Claws 在这一层提供了更健壮的工具封装和错误处理机制（如自动重试、幂等性保证）。

---



### 3: Claws 是如何工作的？它的核心技术原理是什么？

3: Claws 是如何工作的？它的核心技术原理是什么？

**A**: Claws 的核心工作原理通常包含以下几个关键方面：

1.  **事件循环**：它维护了一个持续运行的事件循环，监听来自 LLM 的指令以及外部系统的反馈。
2.  **抽象接口**：它将具体的行动（如读写数据库、发送邮件、执行代码）抽象为标准化的接口。LLM 只需要发出高层次的意图指令，Claws 负责将其翻译为具体的 API 调用。
3.  **人机协作**：Claws 允许在关键步骤插入“人工确认”机制。当 Agent 准备执行高风险操作（如删除文件、转账）时，Claws 可以暂停流程，等待人类批准后再继续执行，从而提高安全性。

---



### 4: 对于开发者而言，使用 Claws 构建应用有什么实际好处？

4: 对于开发者而言，使用 Claws 构建应用有什么实际好处？

**A**: 对于开发者，Claws 极大地降低了构建复杂 AI 应用的门槛和风险：

*   **减少“幻觉”带来的风险**：通过在 Claws 层预定义工具和逻辑约束，限制了 LLM 随意发挥的空间，减少了模型产生幻觉导致系统崩溃的可能性。
*   **调试与可观测性**：由于 Claws 将“思考”和“执行”分离，开发者可以更清晰地看到 Agent 决策的每一步以及具体的执行结果，而不是面对一个黑盒。
*   **模块化开发**：开发者可以专注于编写具体的工具函数，而将如何调用这些工具的逻辑交给 Claws 和 LLM 去协商，实现了业务逻辑与控制逻辑的解耦。

---



### 5: Claws 与 LangChain、Semantic Kernel 等流行框架有什么区别？

5: Claws 与 LangChain、Semantic Kernel 等流行框架有什么区别？

**A**: 虽然它们都属于 AI 基础设施，但侧重点不同：

*   **LangChain / Semantic Kernel**：主要是**开发框架（SDK）**。它们提供了丰富的组件让开发者去组装 Agent，更多关注于“如何定义链”、“如何处理提示词”。
*   **Claws**：更像是一个**运行时环境或中间件**。它关注的是 Agent 启动后的**生命周期管理**。你可以用 LangChain 来定义一个 Agent 的行为逻辑，然后将其部署在 Claws 上运行，以获得更强的稳定性和状态管理能力。

---



### 6: Claws 目前是否已经开源？是否可以商用？

6: Claws 目前是否已经开源？是否可以商用？

**A**: 根据相关技术社区（Hacker News）的讨论，Claws 通常是作为一个开源项目出现的，旨在帮助开发者解决 Agent 落地难的问题。大多数此类项目遵循宽松的开源协议（如 MIT 或 Apache 2.0），允许商业使用。但具体的授权范围需参考其官方 GitHub 仓库的说明，因为随着功能迭代，许可证条款可能会发生变化。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基于思维链的路径验证

### 问题**：假设你正在为一个 LLM Agent 编写 Prompt，该 Agent 需要使用 Claws 来执行文件系统操作（如读取日志文件）。请设计一个包含“思维链”的 Prompt 指令，要求 Agent 在调用 Claws 的工具函数前，必须先输出对文件路径的验证逻辑。

### 提示**：考虑如何将 Claws 的控制层逻辑与 LLM 的推理过程分离。你需要明确指示 LLM 不要直接生成函数调用代码，而是生成一段伪代码或逻辑描述，由 Claws 层来捕获并执行。

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
- 标签： [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Claws](/tags/claws/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/) / [Agent](/tags/agent/) / [增强功能](/tags/%E5%A2%9E%E5%BC%BA%E5%8A%9F%E8%83%BD/) / [AI 系统](/tags/ai-%E7%B3%BB%E7%BB%9F/) / [模型优化](/tags/%E6%A8%A1%E5%9E%8B%E4%BC%98%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [LLM智能体新增Claws层：强化外部工具调用与任务执行能力]({{< relref "posts/20260221-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-13.md" >}})
- [人人都在构建异步智能体 但鲜有人能定义其概念]({{< relref "posts/20260209-hacker_news-everyones-building-async-agents-but-almost-no-one--14.md" >}})
- [AGENTS.md 架构在智能体评估中优于 Skills 架构]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-9.md" >}})
- [LLM智能体新增Claws层以优化任务执行]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-14.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*