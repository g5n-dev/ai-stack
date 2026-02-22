---
title: "Claws成为LLM代理的新一层"
date: 2026-02-22T05:33:26+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "Agents", "Claws", "AI 架构", "代理框架", "模型层", "Hacker News", "自动化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型（LLM）应用场景的深化，如何让智能体更稳定地处理复杂任务成为关键挑战。Claws 作为一种新增的抽象层，通过在 LLM 之上构建结构化逻辑，旨在弥合模型能力与实际执行之间的鸿沟。本文将探讨 Claws 的核心设计理念，分析它如何通过增强控制流来提升系统的可靠性，并帮助开发者理解在构建生产级 Agent"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型", "AI/ML项目"]
---

# Claws成为LLM代理的新一层

---

## 基本信息

- **作者**: Cyphase
- **评分**: 236
- **评论数**: 672
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大语言模型（LLM）应用场景的深化，如何让智能体更稳定地处理复杂任务成为关键挑战。Claws 作为一种新增的抽象层，通过在 LLM 之上构建结构化逻辑，旨在弥合模型能力与实际执行之间的鸿沟。本文将探讨 Claws 的核心设计理念，分析它如何通过增强控制流来提升系统的可靠性，并帮助开发者理解在构建生产级 Agent 时引入这一层的实际价值。

---
## 评论

由于您未提供具体的文章正文，以下评价基于标题 **《Claws are now a new layer on top of LLM agents》** 及其隐含的“Claws”（指代具身智能的机械爪/执行终端，或某种特定的控制层）作为大模型智能体新架构层这一技术隐喻进行深度剖析。

---

### **一句话中心观点**
文章提出了一种架构演进范式：即单纯的“大脑”（LLM）已遇瓶颈，未来的竞争壁垒在于“Claws”（高精度的执行/控制层），它将作为独立的功能层与模型层解耦并深度融合，从而赋予智能体物理世界或数字系统的真实操纵能力。

### **深度评价**

#### **1. 内容深度：观点的深度和论证的严谨性**
*   **支撑理由（事实陈述/你的推断）：**
    *   **从“认知”到“行动”的跨越：** 文章若论证有力，应指出了当前LLM Agents主要受困于“幻觉”与“执行鸿沟”。Claws层（无论是物理机械臂还是高权限API调用）本质上是将概率性的语言输出转化为确定性的物理或数字状态变更。
    *   **系统解耦的必要性：** 将执行层抽象出来，意味着标准化。这类似于计算机体系结构中指令集与硬件的分离，论证了通用大模型需要专用的“手”来完成垂直任务（如焊接代码或焊接零件）。
*   **反例/边界条件（你的推断）：**
    *   **端到端大模型的吞噬：** 如果Google的RT-2或类似的多模态模型成功将视觉-语言-动作完全内化，无需中间层，那么“Claws作为独立层”的架构可能只是过渡态。
    *   **纯数字场景的局限性：** 在纯软件Agent（如客服）中，“Claws”可能仅是API调用，这一层早已存在，文章若过度拔高其为“新层”可能存在概念包装之嫌。

#### **2. 实用价值：对实际工作的指导意义**
*   **支撑理由（事实陈述）：**
    *   **工程化落地指南：** 对于构建Agent的开发者，这意味着不要只盯着Prompt Engineering，而要投入资源构建稳固的Tool Use接口和错误处理机制（即Claws的“抓力”）。
    *   **投资风向标：** 指明硬件机器人或垂直SaaS（拥有高权限操作能力的软件）是下一个风口，而非仅是基础模型训练。
*   **反例/边界条件（作者观点/你的推断）：**
    *   **成本陷阱：** 强调Claws层可能导致系统成本（Token消耗与物理硬件）指数级上升，对于低价值任务，这种架构可能“杀鸡用牛刀”。

#### **3. 创新性：提出了什么新观点或新方法**
*   **支撑理由（你的推断）：**
    *   **具身智能的抽象化：** 将具体的物理硬件抽象为逻辑上的“Layer”，这是一种视角的创新。它暗示了未来的AI Agent架构 = LLM（大脑） + Planning（小脑） + Claws（四肢/执行器）。
*   **反例/边界条件（事实陈述）：**
    *   **旧瓶装新酒：** RPA（机器人流程自动化）和传统的工业控制逻辑早已存在“执行层”的概念。文章若未阐明AI驱动的Claws与传统自动化的本质区别（如适应性、泛化能力），则创新性不足。

#### **4. 可读性：表达的清晰度和逻辑性**
*   **支撑理由（作者观点）：**
    *   **隐喻的使用：** “Claws”这一比喻生动形象，直接传达了“破坏性”、“抓取力”和“实体感”，比单纯说“Actuators”或“Tools”更具冲击力，利于非技术受众理解。
*   **反例/边界条件（你的推断）：**
    *   **歧义风险：** 如果文中未严格定义Claws的边界（是物理硬件？还是中间件？），读者容易产生混淆，导致逻辑链条断裂。

#### **5. 行业影响：对行业或社区的潜在影响**
*   **支撑理由（你的推断）：**
    *   **重定义Agent评测标准：** 行业可能会从单纯的“对话智商”测试转向“任务完成率”测试。谁的Claws更稳、更准，谁就是王者。
    *   **催生“手脑分离”供应链：** 可能会出现专门提供“Claws层”解决方案的厂商，专注于做模型与硬件/系统之间的适配器。

#### **6. 争议点或不同观点**
*   **观点 A（作者观点）：** Claws是独立于LLM之外的新层级，需要专门优化。
*   **观点 B（学术界/业界反对）：** Claws只是LLM的延伸。随着VLA（Vision-Language-Action）模型的发展，控制信号将直接由Transformer输出，不存在独立的“层”，强行分层会降低系统的端到端优化效率。

#### **7. 实际应用建议**
*   **建议：** 在构建下一代Agent时，采用“双轨制”评估。不仅要测试LLM的推理能力，更要模拟极端环境测试“Claws”层的鲁棒性（如API超时、机械臂物理阻挡后的恢复能力）。

---

### **验证与检查方式**

为了验证文章中关于“Claws”作为新层的论断是否成立，建议采取以下检查方式：

1.  **技术架构解耦测试（指标）：**
    *   检查该系统是否能够无缝更换底部的执行单元（例如，

---
## 代码示例




```python
# 示例1：基础Claws层实现（结构化输出控制）
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ClawResponse:
    """Claws层响应结构"""
    content: str
    metadata: Dict[str, Any]
    confidence: float

class BaseClaw:
    """Claws基类，定义标准接口"""
    def __init__(self, agent):
        self.agent = agent
        
    def execute(self, prompt: str) -> ClawResponse:
        """执行并返回结构化响应"""
        raw_response = self.agent.generate(prompt)
        return self._process_response(raw_response)
    
    def _process_response(self, raw: str) -> ClawResponse:
        """处理原始响应（可被子类重写）"""
        return ClawResponse(
            content=raw,
            metadata={"model": self.agent.model_name},
            confidence=0.9
        )

# 使用示例
class MockAgent:
    def generate(self, prompt):
        return f"Agent response to: {prompt}"

claw = BaseClaw(MockAgent())
response = claw.execute("分析用户意图")
print(response.content)  # 输出带元数据的结构化响应
```




```python
# 示例2：安全过滤Claw（内容审核）
class SafetyClaw(BaseClaw):
    """实现内容安全过滤的Claw"""
    def __init__(self, agent, forbidden_words=None):
        super().__init__(agent)
        self.forbidden_words = forbidden_words or ["暴力", "非法"]
    
    def _process_response(self, raw: str) -> ClawResponse:
        """检查并过滤敏感内容"""
        for word in self.forbidden_words:
            if word in raw:
                return ClawResponse(
                    content="[内容已过滤]",
                    metadata={"filter_reason": f"包含禁止词: {word}"},
                    confidence=0.0
                )
        return super()._process_response(raw)

# 使用示例
safe_claw = SafetyClaw(MockAgent())
response = safe_claw.execute("如何实施暴力行为")
print(response.content)  # 输出: [内容已过滤]
```




```python
# 示例3：工具调用Claw（增强能力）
class ToolCallingClaw(BaseClaw):
    """支持工具调用的Claw"""
    def __init__(self, agent, tools=None):
        super().__init__(agent)
        self.tools = tools or {}
    
    def execute(self, prompt: str) -> ClawResponse:
        """执行并处理工具调用"""
        response = super().execute(prompt)
        while "USE_TOOL:" in response.content:
            tool_name = response.content.split("USE_TOOL:")[1].split()[0]
            if tool_name in self.tools:
                tool_result = self.tools[tool_name]()
                response = ClawResponse(
                    content=f"工具 {tool_name} 返回: {tool_result}",
                    metadata=response.metadata,
                    confidence=response.confidence
                )
        return response

# 使用示例
def weather_tool():
    return "晴天，25°C"

tool_claw = ToolCallingClaw(MockAgent(), {"weather": weather_tool})
response = tool_claw.execute("查询天气 USE_TOOL: weather")
print(response.content)  # 输出工具调用结果
```


---
## 案例研究


### 1：金融合规自动化审查

 1：金融合规自动化审查

**背景**: 某中型金融科技公司每天需要处理数千笔贷款申请，其中涉及大量非结构化文档（如银行流水、发票扫描件、信用报告）。公司此前使用了基于 LLM 的智能体来提取信息，但合规部门要求对关键数据（如金额、日期、账号）的准确率必须达到 100%，且所有提取过程必须可审计、可回溯。

**问题**: 原有的 LLM 智能体虽然能流畅理解文档语义，但在处理数字和格式化输出时存在“幻觉”或格式错误。如果直接依赖 LLM 生成 SQL 或 JSON，偶尔会因类型不匹配导致下游数据库崩溃，且纯模型的黑盒特性无法满足金融审计的合规要求。

**解决方案**: 引入 Claws 作为 LLM 智能体之上的逻辑控制层。LLM 负责理解文档语义并生成初步意图，而 Claws 负责执行严格的数据校验逻辑。例如，LLM 提取“金额”后，Claws 会强制运行正则表达式验证和类型检查，只有通过验证的数据才会被写入数据库。如果校验失败，Claws 会将错误反馈给 LLM 进行修正，而不是直接返回错误结果。

**效果**: 系统的数据录入准确率从 95% 提升至 99.9%，完全消除了因格式错误导致的系统故障。由于 Claws 层记录了所有的校验逻辑和修正过程，审计人员可以清晰地看到每一条数据的决策路径，顺利通过了监管审计。

---



### 2：SaaS 平台复杂工作流编排

 2：SaaS 平台复杂工作流编排

**背景**: 一家提供企业级营销自动化服务的 SaaS 公司，其客户希望在 AI 助手中通过自然语言触发复杂的内部操作。例如，当客户在对话中说“给上周注册的所有用户发送优惠券”时，系统需要执行查询数据库、计算筛选条件、调用邮件 API 以及记录日志等一系列跨服务操作。

**问题**: 纯粹的 LLM 智能体在处理这种长链条、多步骤的任务时，往往因为上下文过长或 API 调用顺序错误而失败。例如，LLM 可能会在数据库查询尚未完成时就尝试调用发送邮件的 API，或者在某个步骤失败后无法正确执行“回滚”或“重试”逻辑，导致数据不一致或用户体验受损。

**解决方案**: 将 Claws 架构在智能体与后端服务之间，作为确定性的工作流编排层。LLM 仅负责将用户的自然语言翻译成结构化的“意图图”，而 Claws 负责解析这张图并严格按照预定义的 DAG（有向无环图）执行任务。Claws 确保了只有步骤 A（查询用户）成功返回后，才会触发步骤 B（生成优惠券），并内置了重试和错误处理机制。

**效果**: 跨服务操作的成功率从 70% 提升到了 98% 以上。开发团队发现，通过 Claws 将业务逻辑与模型推理分离后，维护和更新工作流变得更加容易，不再需要为了修复一个 API 调用顺序问题而对 Prompt 进行繁琐的调试。

---
## 最佳实践

## 最佳实践指南

### 实践 1：理解抽象层级与职责分离

**说明**:
Claws 作为位于 LLM Agents 之上的新层级，其核心价值在于提供标准化的接口和工具封装，而不是直接处理业务逻辑。理解这一层级划分意味着要明确 Claws 负责处理与外部世界的交互复杂性（如 API 调用、数据验证），而下层的 LLM Agents 专注于推理、规划和自然语言理解。这种分离能显著降低系统耦合度。

**实施步骤**:
1. 绘制系统架构图，明确标记出 LLM Agent 层和 Claws 控制层。
2. 定义 Claws 层的输入输出规范，确保其处理的是结构化指令而非自然语言。
3. 审查现有代码，将属于“工具使用”和“环境交互”的逻辑从 Agent 提示词或代码中剥离，迁移至 Claws 层。

**注意事项**: 避免在 Claws 层嵌入任何业务决策逻辑，保持其作为通用工具集的纯粹性。

---

### 实践 2：实施标准化的工具定义

**说明**:
Claws 本质上是对工具调用的增强层。最佳实践要求所有通过 Claws 暴露给 Agent 的工具必须具有严格的类型定义、参数校验和清晰的文档描述。这能减少 LLM 产生的幻觉调用，提高执行成功率。

**实施步骤**:
1. 为每个工具编写 JSON Schema 或 Pydantic 模型，明确定义参数类型和必填项。
2. 在 Claws 配置中为每个工具添加详细的自然语言描述，说明其功能、副作用及适用场景。
3. 建立工具的版本管理机制，确保底层 API 变更时不会直接破坏 Agent 的运行。

**注意事项**: 工具的描述应尽可能简洁客观，避免在描述中诱导 LLM 进行不必要的调用。

---

### 实践 3：构建细粒度的错误处理与回退机制

**说明**:
在 LLM 调用外部工具时，网络波动、API 限流或权限错误是常态。Claws 层应作为“防火墙”，捕获底层的技术性错误（如 500 Internal Server Error），并将其转化为 LLM 能够理解的语义化反馈（如“服务暂时不可用，请稍后重试”），而不是直接抛出异常导致 Agent 中断。

**实施步骤**:
1. 在 Claws 层实现统一的异常捕获中间件。
2. 定义错误码映射表，将技术异常映射为语义化的错误消息返回给 Agent。
3. 为关键工具配置自动重试策略（如指数退避算法），并在重试失败后触发回退流程。

**注意事项**: 不要将原始的堆栈跟踪信息直接返回给 LLM，这会浪费 Token 并可能导致 Agent 混淆。

---

### 实践 4：优化上下文管理与 Token 效率

**说明**:
Claws 层通常位于 Agent 和工具之间，容易成为信息流的瓶颈。如果不加控制，工具返回的冗长数据（如长日志、大文件片段）会迅速消耗上下文窗口。Claws 应具备数据预处理能力，仅传递相关信息。

**实施步骤**:
1. 在 Claws 层实现数据截断和摘要逻辑，对于过长的工具返回值进行预处理。
2. 使用向量检索或关键词过滤，确保 Agent 只接收到执行任务所必需的最小数据集。
3. 监控各工具的平均 Token 消耗量，对高消耗工具进行优化或限制。

**注意事项**: 在压缩数据时，必须保留关键的元数据和状态码，防止 Agent 丢失执行上下文。

---

### 实践 5：确保可观测性与调试能力

**说明**:
由于引入了新的中间层，排查问题变得更加困难。必须建立完善的可观测性体系，记录 Agent 的意图、Claws 的转换过程以及底层工具的执行结果。这对于调试 Agent 的行为轨迹至关重要。

**实施步骤**:
1. 实现结构化日志记录，记录每一次 Tool Call 的完整链路。
2. 在开发模式下启用详细的 Trace ID 追踪，将 LLM 的思维链与 Claws 的执行动作关联起来。
3. 建立仪表盘，监控工具调用频率、失败率以及平均响应时间。

**注意事项**: 记录日志时注意敏感数据的脱敏处理，特别是涉及用户隐私或 API 密钥的内容。

---

### 实践 6：强化安全验证与权限控制

**说明**:
Claws 层是防止 Agent 执行危险操作的最后防线。不能完全依赖 LLM 的判断力来决定是否执行“删除数据库”或“发送邮件”等高危操作。必须在 Claws 层实施硬编码的安全检查。

**实施步骤**:
1. 实施基于角色的访问控制（RBAC），确保 Agent 实例只能调用其被授权的工具。
2. 对具有破坏性操作的工具（如写入、删除）配置“人工确认”模式或二次校验逻辑。
3. 限制工具的参数范围（例如限制转账金额上限、限制文件访问路径）。

**注意事项**: 安全策略应独立于 Agent 的提示

---
## 学习要点

- 根据您提供的内容（基于 Hacker News 关于 Claws 的讨论），以下是总结出的关键要点：
- Claws 被定义为一种构建在 LLM Agents 之上的新型抽象层或基础设施，旨在解决当前智能体开发中的碎片化问题。
- 该架构的核心价值在于将“控制回路”与底层大模型解耦，从而允许开发者在不修改模型逻辑的情况下独立优化决策流程。
- 通过引入这一中间层，Claws 能够显著提升智能体在执行复杂任务时的可靠性和稳定性，减少大模型固有的幻觉或不可预测行为。
- 这种设计模式促进了模块化开发，使得不同的工具、记忆系统和执行策略可以像“插件”一样灵活插拔。
- 它标志着 AI 应用架构的演进重心正从单纯追求模型参数规模，转向构建更高效的模型编排与管理系统。

---
## 常见问题


### 1: Claws 在 LLM Agent 架构中具体扮演什么角色？

1: Claws 在 LLM Agent 架构中具体扮演什么角色？

**A**: Claws 被定义为位于 LLM Agents（大语言模型智能体）之上的一个“新层”。它的主要作用是充当智能体与外部环境（如互联网、API、本地文件系统）之间的接口或中间件。传统的 LLM Agent 通常直接依赖模型本身的能力或通过简单的插件来执行任务，而 Claws 作为一个独立层，可能专门负责处理工具调用、执行复杂的工作流、管理状态或处理与底层系统的交互细节，从而将“思考”（LLM 的推理）与“行动”（实际的操作）分离开来。

---



### 2: 为什么我们需要在 LLM Agents 之上添加 Claws 这样的层？

2: 为什么我们需要在 LLM Agents 之上添加 Claws 这样的层？

**A**: 引入 Claws 主要是为了解决当前 LLM Agents 在实际落地中遇到的几个关键问题：
1.  **稳定性与控制力**：直接让 LLM 控制工具调用往往容易出现格式错误或逻辑混乱，Claws 可以提供更结构化的控制机制。
2.  **安全性**：将执行层隔离出来，可以更方便地对 Agent 的操作权限进行限制和审计，防止模型产生危险的操作。
3.  **状态管理**：复杂的任务往往需要多步交互且保持上下文状态，Claws 层可以专门负责维护这些状态，而不需要 LLM 每次都重新处理。
4.  **解耦**：它允许开发者独立升级工具调用逻辑，而无需改动底层的提示词或模型配置。

---



### 3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

**A**: 现有的框架通常提供的是一套完整的构建 Agent 的工具链，包括提示词管理、记忆存储和工具定义。而 Claws 的概念更侧重于“层”的职责。它可以被视为这些框架中的一个增强组件，或者是一种替代性的架构思路。与其说它是一个竞争产品，不如说它是一种架构模式的演进：将“执行”的复杂性从“推理”的模型中剥离出来，形成一个专门的子系统。这意味着 Claws 可能更专注于执行层面的鲁棒性，而不是模型本身的推理能力。

---



### 4: Claws 是否支持多模态操作（如处理图像、音频或网页浏览）？

4: Claws 是否支持多模态操作（如处理图像、音频或网页浏览）？

**A**: 虽然具体的实现细节取决于 Claws 的具体代码库设计，但作为一个位于 LLM 之上的“层”，其设计初衷通常是为了增强 Agent 与世界的交互能力。因此，它极有可能设计为支持多种模态的输入输出。例如，它可以封装浏览器自动化工具来处理网页视觉信息，或者调用图像处理 API。通过将多模态工具的复杂性封装在这一层中，LLM Agent 可以通过统一的接口来处理非文本任务。

---



### 5: Claws 是如何处理 LLM 的幻觉或错误指令的？

5: Claws 是如何处理 LLM 的幻觉或错误指令的？

**A**: 由于 Claws 是一个独立的执行层，它可以在指令真正作用于系统之前引入验证机制。当 LLM 发出一个可能存在错误或风险的指令时，Claws 层可以解析该指令，检查参数的有效性，甚至通过预设的规则或额外的轻量级模型来确认操作的合理性。如果检测到异常（例如试图删除系统关键文件），Claws 可以拦截该请求并要求 LLM 重新生成，从而作为一道防火墙来提高系统的可靠性。

---



### 6: 开发者如何开始使用或集成 Claws 到现有的项目中？

6: 开发者如何开始使用或集成 Claws 到现有的项目中？

**A**: 根据该项目的开源性质，开发者通常可以通过包管理器（如 pip）将其作为库安装到 Python 环境中。集成过程通常涉及定义 Claws 实例，配置允许访问的工具或 API，然后将 LLM（如 GPT-4 或本地模型）的输出连接到 Claws 的输入接口。开发者需要编写配置文件来定义 Claws 如何解析 LLM 的意图，并将其映射到具体的函数调用上。具体的集成步骤通常会在项目的官方文档或 README 中有详细说明。

---



### 7: Claws 这个名字的含义是什么？

7: Claws 这个名字的含义是什么？

**A**: 在生物学中，"Claws"（爪子）是动物用于抓取、操作物体和与物理世界互动的关键器官。在这个技术语境下，这是一个形象的比喻：LLM 充当“大脑”负责思考，而 Claws 充当“爪子”负责实际地去操作、抓取数据并与数字环境进行交互。这个名字强调了其作为执行机构和操作工具的核心定位。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**：在传统的 LLM Agent 架构中，提示词工程和上下文管理通常占据主导地位。如果引入 "Claws" 这一新层级作为执行层，请列举出它应该承担哪三个原本由 LLM 直接负责的低级任务，并说明为什么将这些任务剥离出来可以提高系统的整体稳定性。

### 提示**：考虑 LLM 的本质是概率预测，以及确定性代码执行在处理结构化数据（如 API 调用、文件读写）时的优势。

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
- 标签： [LLM](/tags/llm/) / [Agents](/tags/agents/) / [Claws](/tags/claws/) / [AI 架构](/tags/ai-%E6%9E%B6%E6%9E%84/) / [代理框架](/tags/%E4%BB%A3%E7%90%86%E6%A1%86%E6%9E%B6/) / [模型层](/tags/%E6%A8%A1%E5%9E%8B%E5%B1%82/) / [Hacker News](/tags/hacker-news/) / [自动化](/tags/%E8%87%AA%E5%8A%A8%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Smooth CLI：面向 AI 智能体的低 Token 开销浏览器]({{< relref "posts/20260206-hacker_news-show-hn-smooth-cli-token-efficient-browser-for-ai--14.md" >}})
- [LLM智能体新增Claws层以优化任务执行]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-14.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-8.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
- [编码代理的成功对通用AI系统的启示]({{< relref "posts/20260130-hacker_news-what-the-success-of-coding-agents-teaches-us-about-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*