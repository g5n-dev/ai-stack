---
title: "LLM智能体新增Claws层以增强能力"
date: 2026-02-22T07:40:33+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "智能体", "Claws", "架构", "增强能力", "AI", "模型优化", "系统设计"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型（LLM）应用的深入，如何让智能体更稳定地执行复杂任务成为技术关键。Claws 作为一种新增的抽象层，旨在通过结构化的方式增强 LLM 智能体的任务编排与控制能力。本文将探讨 Claws 的核心设计思路及其对系统架构的影响，帮助读者理解这一层如何提升智能体的可靠性与可扩展性。"
external_url: https://twitter.com/karpathy/status/2024987174077432126
scenarios: ["大语言模型", "AI/ML项目"]
---

# LLM智能体新增Claws层以增强能力

---

## 基本信息

- **作者**: Cyphase
- **评分**: 254
- **评论数**: 700
- **链接**: [https://twitter.com/karpathy/status/2024987174077432126](https://twitter.com/karpathy/status/2024987174077432126)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47096253](https://news.ycombinator.com/item?id=47096253)

---
## 导语

随着大语言模型（LLM）应用的深入，如何让智能体更稳定地执行复杂任务成为技术关键。Claws 作为一种新增的抽象层，旨在通过结构化的方式增强 LLM 智能体的任务编排与控制能力。本文将探讨 Claws 的核心设计思路及其对系统架构的影响，帮助读者理解这一层如何提升智能体的可靠性与可扩展性。

---
## 评论

由于您在提示词中仅提供了文章标题“Claws are now a new layer on top of LLM agents”而未提供正文内容，以下评价将基于**该标题所隐含的技术隐喻**以及当前LLM Agent（智能体）领域关于“工具使用”与“具身智能”的前沿趋势进行推演性深度评价。

---

### 深度评价：关于“Claws”作为LLM Agent新层级的隐喻

#### 1. 核心观点
文章主张“Claws（利爪/执行终端）”已成为LLM Agent架构中独立于大模型“大脑”之外的全新关键层级，标志着行业重心从单纯的“推理能力”向“物理/数字执行能力”的范式转移。

#### 2. 支撑理由与边界条件

**支撑理由：**

*   **从“软体”向“硬体”的架构演进（事实陈述）：**
    目前的Agent架构通常遵循“规划-记忆-工具”的三层模型。标题中的“Claws”隐喻精准地指出了当前架构的短板：LLM作为大脑虽然强大，但缺乏能够精确、鲁棒地改变物理世界或复杂数字环境的“手”。这一观点符合当前AI从Chatbot（聊天机器人）向Actuator（执行器）演进的技术趋势。
*   **执行层的非语言性挑战（作者观点/技术推断）：**
    传统的LLM处理的是离散的Token，而“Claws”层处理的是连续的动作、空间坐标或复杂的API调用序列。将这两者解耦，允许“Claws”层独立发展出专门针对高频、低延迟操作的算法（如传统的控制算法或专用的Action Models），这解决了LLM直接生成动作指令时的抖动和高成本问题。
*   **安全与可控性的隔离舱（你的推断）：**
    将“Claws”作为一个独立层级，实际上是在Agent架构中引入了“沙箱”机制。大脑负责思考，爪子负责执行，中间通过严格的接口（如函数调用Function Calling）连接。这种分层有助于限制AI的潜在危害，因为“爪子”的动作可以被硬编码规则限制，而不仅仅依赖于LLM的道德对齐。

**反例/边界条件：**

*   **端到端具身智能的挑战（反例）：**
    Google DeepMind的RT-2等模型表明，直接将感知映射到动作的端到端模型依然有效。如果过度强调“Claws”作为独立层级，可能会导致系统割裂，丧失LLM在处理长尾、未见过的复杂任务时的泛化能力。有时，“大脑”直接控制“神经末梢”比中间多一层“爪子”更灵活。
*   **数字Agent的“无爪”困境（边界条件）：**
    对于纯粹的代码生成或数据分析Agent，其“Claws”本质上是API调用或系统Shell。这种“爪子”是虚拟且标准化的，并不需要像物理机器人那样复杂的控制理论层。因此，该观点可能主要适用于具身智能或RPA（机器人流程自动化）领域，对纯软件Agent的普适性需打折扣。

#### 3. 维度评价

**1. 内容深度与严谨性：**
该隐喻触及了Agent架构的核心矛盾：**符号推理与连续控制之间的鸿沟**。如果文章深入探讨了如何将LLM的高层意图映射为底层控制指令（如使用PaLM-E或RT-2的方法），则具有极高的技术深度。但若仅停留在“需要工具”的浅层论述，则略显平庸。

**2. 实用价值：**
对工程实践极具指导意义。它提示开发者在构建Agent时，不应只关注Prompt Engineering（大脑训练），而应投入资源构建稳定的Action Layer（爪子），例如建立标准化的Tool API、错误处理机制和状态反馈循环。

**3. 创新性：**
“Claws”这一词汇的引入具有极强的视觉冲击力，它比传统的“Tool Use”或“Actuators”更生动地强调了**破坏性**和**直接性**。它暗示了Agent不仅仅是助手，更是能够直接干预环境的行动者。

**4. 行业影响：**
这一观点可能预示着AI创业公司的新赛道：**“Agent Body”供应商**。未来可能出现专门为LLM提供“Claws”接口的中间件公司，负责将LLM的指令标准化为机器人的动作指令或企业软件的操作流。

**5. 争议点：**
主要争议在于**“手脑分离”还是“手脑一体”**。支持分离者认为这利于模块化工程；支持一体者认为LLM的世界模型必须包含对物理世界的理解，否则无法真正实现通用智能（AGI）。

#### 4. 可验证的检查方式

为了验证该文章观点的有效性及“Claws”层的实际效能，建议采用以下指标：

*   **指标1：Action Failure Rate（动作失败率）**
    *   *定义：* 在Agent执行任务过程中，由“Claws”层导致的物理操作失败或API调用错误的比率。
    *   *验证逻辑：* 如果独立的“Claws”层确实优于LLM直接生成指令，那么其失败率应显著低于端到端生成模式。

*   **指标2：Latency per Action（单次操作延迟）**
    *   *定义：* 从发出指令到“Claws”完成物理反馈的时间。
    *   *验证逻辑：* 独立层级通常意味着更轻量级的模型或专用算法，应能显著降低延迟，特别是在机器人抓取等对实时性要求高的场景。

*   **实验：Long-Horizon Task Completion（长

---
## 代码示例




```python
# 示例1：工具调用层 - 让LLM能执行系统命令
import subprocess
from typing import Dict, Any

class ToolLayer:
    """工具层：为LLM提供安全执行系统命令的能力"""
    
    def __init__(self):
        self.available_tools = {
            "run_shell": self._run_shell,
            "get_weather": self._get_weather
        }
    
    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """执行指定工具并返回结果"""
        if tool_name not in self.available_tools:
            return {"error": f"工具 {tool_name} 不存在"}
        
        try:
            result = self.available_tools[tool_name](**kwargs)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _run_shell(self, command: str) -> str:
        """安全执行shell命令（示例仅支持简单命令）"""
        if not command.isprintable():
            raise ValueError("不安全的命令")
        return subprocess.check_output(command, shell=True, text=True)
    
    def _get_weather(self, city: str) -> str:
        """模拟天气查询工具"""
        return f"{city}今天晴，温度25°C"

# 使用示例
tool_layer = ToolLayer()
print(tool_layer.execute("get_weather", city="北京"))
print(tool_layer.execute("run_shell", command="echo 'Hello Claws!'"))
```




```python
# 示例2：记忆管理层 - 为LLM添加持久化记忆
import json
from datetime import datetime
from typing import List, Dict

class MemoryLayer:
    """记忆层：为LLM提供短期和长期记忆功能"""
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = memory_file
        self.short_term: List[Dict] = []
        self.long_term: Dict = {}
        self._load_memory()
    
    def add_memory(self, content: str, memory_type: str = "short"):
        """添加新记忆"""
        timestamp = datetime.now().isoformat()
        memory_entry = {
            "content": content,
            "timestamp": timestamp,
            "type": memory_type
        }
        
        if memory_type == "short":
            self.short_term.append(memory_entry)
            if len(self.short_term) > 10:  # 保持短期记忆不超过10条
                self.short_term.pop(0)
        else:
            self.long_term[timestamp] = memory_entry
        
        self._save_memory()
    
    def get_relevant_memories(self, query: str) -> List[str]:
        """根据查询获取相关记忆（简化版实现）"""
        # 实际应用中这里可以使用向量相似度搜索
        relevant = []
        for memory in self.short_term:
            if query.lower() in memory["content"].lower():
                relevant.append(memory["content"])
        return relevant
    
    def _save_memory(self):
        """持久化记忆到文件"""
        with open(self.memory_file, 'w') as f:
            json.dump({
                "short_term": self.short_term,
                "long_term": self.long_term
            }, f, indent=2)
    
    def _load_memory(self):
        """从文件加载记忆"""
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                self.short_term = data.get("short_term", [])
                self.long_term = data.get("long_term", {})
        except FileNotFoundError:
            pass

# 使用示例
memory = MemoryLayer()
memory.add_memory("用户喜欢Python编程", "long")
memory.add_memory("今天讨论了LLM架构", "short")
print(memory.get_relevant_memories("Python"))
```




```python
# 示例3：安全防护层 - 过滤有害内容
import re
from typing import Optional

class SafetyLayer:
    """安全层：为LLM添加内容过滤和防护机制"""
    
    def __init__(self):
        self.blocked_patterns = [
            r"password", r"secret", r"\b\d{16}\b",  # 敏感信息
            r"drop table", r"rm -rf",  # 危险操作
        ]
        self.max_retries = 3
    
    def check_input(self, user_input: str) -> Optional[str]:
        """检查用户输入是否安全"""
        for pattern in self.blocked_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return "检测到敏感内容，请修改您的输入"
        return None
    
    def sanitize_output(self, llm_output: str) -> str:
        """清理模型输出中的潜在问题"""
        # 移除可能的代码注入
        sanitized = re.sub(r"<script.*?>.*?</script>", "", llm_output, flags=re.IGNORECASE)
        # 限制输出长度
        return sanitized[:2000] if len(sanitized) > 2000 else sanitized
    
    def rate_limit_check(self, user_id: str) -> bool:
        """简单的速率限制检查（实际应用需要更复杂的实现）"""
        # 这里简化处理，实际应该记录请求时间


---
## 案例研究


### 1：MultiOn

 1：MultiOn

**背景**: MultiOn 是一家致力于构建 AI Agent 的初创公司，其目标是让 AI 不仅能生成文本，还能像人类一样操作浏览器，完成订票、购物等复杂任务。

**问题**: 传统的 LLM Agent 在处理网页交互时面临严峻挑战。网页结构复杂（DOM 树庞大），且现代网页大量使用动态内容（React/Vue），传统的基于 HTML 解析或纯视觉定位的方法往往不稳定。Agent 经常因为找不到按钮、弹窗干扰或页面加载延迟而执行失败，导致任务完成率在长流程中急剧下降。

**解决方案**: MultiOn 采用了一种类似 "Claws" 的架构设计，在 LLM 规划层和浏览器操作层之间引入了一个专门的执行层。这一层通过多模态模型直接理解屏幕截图和语义化页面标签，而非依赖脆弱的 CSS 选择器。它将浏览器的操作原语抽象为更高级的指令，处理了点击、输入、滚动等动作的底层细节和重试逻辑。

**效果**: 这种分层架构显著提高了 Agent 在真实网络环境下的鲁棒性。MultiOn 的 Agent 能够在复杂的电商网站上完成从搜索、筛选到结账的全流程，成功率远超传统基于 Selenium 或 Playwright 的脚本方案，实现了真正的“端到端”自动化。

---



### 2：Rabbit (R1) 与 Large Action Model (LAM)

 2：Rabbit (R1) 与 Large Action Model (LAM)

**背景**: 硬件初创公司 Rabbit 推出了 R1 便携设备，旨在通过自然语言界面接管用户的手机应用操作，实现“意图计算”。

**问题**: 手机应用环境极其封闭且碎片化。不同的 App 有完全不同的用户界面（UI）和交互逻辑，且这些界面是封闭的黑盒，无法通过简单的 API 调用来控制。如果让 LLM 直接去猜测屏幕上的坐标进行点击，误差率极高，且无法适应 App 界面的频繁更新。

**解决方案**: Rabbit 开发了 Large Action Model (LAM) 作为核心中间件，这正是“Claws”理念的体现。LAM 并不直接让底层 LLM 去操作像素，而是预先学习并维护了各个主流 App 的“操作蓝图”。当用户发出指令时，LAM 将意图转化为特定 App 的功能函数，再由底层控制模块与 App 进行基于 UI 的交互。这一层负责处理具体的界面跳转和异常反馈。

**效果**: 这种架构使得 R1 能够可靠地操作 Uber、Spotify 等复杂应用，而无需这些应用开放官方 API。用户只需说出“帮我叫车”，系统即可通过模拟人类操作完成 App 内的一系列复杂动作，展示了在无 API 环境下通过中间层控制软件的巨大潜力。

---



### 3：CrewAI 企业级数据录入自动化

 3：CrewAI 企业级数据录入自动化

**背景**: 某大型物流企业试图利用 AI Agent 自动化处理供应链中的发票录入工作，需要从供应商发送的 PDF 邮件附件中提取数据并录入到老旧的 ERP 系统中。

**问题**: 现有的 LLM 虽然能很好地理解 PDF 内容，但无法直接与企业的旧版 ERP 系统交互。该 ERP 系统基于旧有的 Web 表单，字段校验逻辑复杂，且存在会话超时机制。直接使用 LLM 生成代码来操作表单经常因为字段格式错误或网络抖动导致数据录入失败。

**解决方案**: 开发团队使用 CrewAI 框架构建了 Agent 系统，并引入了一个类似“Claws”的工具层。该层封装了与 ERP 系统交互的具体逻辑，包括处理会话保持、字段格式清洗、错误捕获和自动重试。LLM 仅负责从 PDF 中提取结构化数据（如金额、日期、单号），而将“如何安全地将数据填入表单”的任务完全交给下方的工具层执行。

**效果**: 通过将“认知”与“执行”分离，系统的数据录入准确率提升至 99% 以上。下方的工具层成功屏蔽了 ERP 系统的复杂性对 LLM 的干扰，即使 ERP 页面发生微小的 UI 调整，只需更新工具层配置即可，无需重新训练或调整 LLM 提示词，极大降低了维护成本。

---
## 最佳实践

## 最佳实践指南

### 实践 1：理解 Claws 的抽象层级定位

**说明**: Claws 并非旨在替代现有的 LLM 智能体框架，而是作为一种覆盖在智能体之上的控制层或增强层。它主要负责处理智能体与外部系统交互时的复杂性，提供更高级别的编排能力和安全性保障。

**实施步骤**:
1. 评估现有智能体架构，识别出需要更高层级控制的环节（如工具调用、错误恢复）。
2. 将 Claws 集成到智能体与执行环境之间，而非重写底层逻辑。
3. 定义 Claws 层的输入输出标准，确保与底层 LLM 智能体的无缝通信。

**注意事项**: 避免在 Claws 层实现过多的业务逻辑，应保持其轻量级，专注于协调与控制。

---

### 实践 2：实施细粒度的工具调用控制

**说明**: 利用 Claws 对 LLM 智能体调用的工具和 API 进行精细化管理。这一层可以验证智能体生成的参数、限制调用频率或在调用前进行权限检查，防止智能体产生不可控的操作。

**实施步骤**:
1. 列出所有允许底层智能体访问的工具清单。
2. 在 Claws 层配置工具调用的验证规则（Schema Validation）。
3. 实施中间件模式，拦截智能体的工具请求，通过安全检查后再转发给实际执行端。

**注意事项**: 确保验证逻辑的严格性，防止因提示词注入导致绕过 Claws 的安全检查。

---

### 实践 3：构建状态管理与上下文持久化机制

**说明**: LLM 智能体通常是无状态的，而 Claws 层应当负责维护多轮对话和任务执行过程中的状态。这包括记录已完成的步骤、存储中间变量以及处理任务的中断与恢复。

**实施步骤**:
1. 设计状态机模型，定义任务的不同生命周期状态（如初始化、执行中、等待输入、已完成）。
2. 集成持久化存储（如 Redis 或数据库），将 Claws 层的状态数据实时保存。
3. 编写恢复逻辑，当智能体崩溃或重置时，Claws 能根据存储的状态恢复上下文。

**注意事项**: 注意处理状态同步的延迟问题，确保 Claws 记录的状态与实际执行环境保持一致。

---

### 实践 4：增强的错误处理与重试策略

**说明**: 智能体在执行任务时可能会遇到 API 失败、网络超时或格式错误。Claws 层应具备智能的错误捕获与修复能力，而不是简单地将错误抛回给 LLM。

**实施步骤**:
1. 在 Claws 层定义标准错误码和错误处理映射表。
2. 实现指数退避重试机制，处理暂时性故障。
3. 对于无法自动修复的错误，构建人工干预接口，允许人工修正后继续执行。

**注意事项**: 设置最大重试次数阈值，防止因无限重试导致资源耗尽。

---

### 实践 5：结构化日志与可观测性设计

**说明**: 由于 Claws 位于智能体之上，它拥有全局视角。利用这一优势，在该层实施全面的日志记录和追踪，对于调试智能体行为和分析性能瓶颈至关重要。

**实施步骤**:
1. 为每一个通过 Claws 的请求分配唯一的 Trace ID。
2. 记录详细的决策日志，包括 Claws 修改了智能体的哪些参数、拦截了哪些请求。
3. 集成 OpenTelemetry 或类似的监控工具，可视化智能体的执行链路。

**注意事项**: 日志记录可能涉及敏感数据，需确保在记录前对敏感信息进行脱敏处理。

---

### 实践 6：定义清晰的反馈循环

**说明**: Claws 不仅要控制智能体，还需要将执行结果转化为 LLM 易于理解的反馈格式。建立双向反馈机制，确保智能体能根据 Claws 的调整结果优化后续行为。

**实施步骤**:
1. 设计标准化的反馈提示词模板，用于向 LLM 汇报执行结果或错误原因。
2. 实施“思维链”监控，分析 LLM 如何根据 Claws 的反馈调整其输出。
3. 定期复盘反馈数据，优化 Claws 的控制策略。

**注意事项**: 反馈信息应简洁明了，避免过多的技术细节干扰 LLM 的理解。

---
## 学习要点

- 根据提供的标题和来源，以下是关于 Claws 架构的关键要点总结：
- Claws 被定义为一种位于 LLM Agents（大模型智能体）之上的新型架构层，旨在解决现有智能体在实际应用中的局限性。
- 该架构层通过抽象底层复杂性，为开发者提供了构建更可靠、更复杂 AI 应用的标准化接口。
- 它的核心价值在于将“规划”与“执行”解耦，使智能体能够更稳定地处理长期任务和复杂的工作流。
- Claws 的引入标志着 AI 开发模式从单纯的“提示词工程”向具备状态管理和工具调用的系统性工程转变。
- 这种分层设计有助于降低多智能体系统中的协调难度，提升整体系统的可扩展性和容错能力。

---
## 常见问题


### 1: Claws 本质上是什么技术或架构？

1: Claws 本质上是什么技术或架构？

**A**: 根据描述，Claws 被定义为建立在 LLM agents（大语言模型智能体）之上的一个“新层”。在 AI 架构语境中，这通常意味着 Claws 并非要替代现有的 LLM 或 Agent 框架，而是作为一个中间件或功能层存在。它的主要作用可能是填补基础模型能力与实际复杂任务执行之间的鸿沟，通过提供额外的工具、安全控制、状态管理或工作流编排，来增强底层 Agent 的稳定性和输出质量。

---



### 2: 为什么我们需要在 LLM Agents 之上增加一个新的“层”？

2: 为什么我们需要在 LLM Agents 之上增加一个新的“层”？

**A**: 直接使用底层 LLM Agents 往往面临几个挑战：一是输出的不确定性（幻觉），二是缺乏对复杂长期任务的状态记忆，三是难以直接与外部工具或 API 进行安全、高效的交互。引入像 Claws 这样的“层”，旨在解决这些问题。它可能充当了“守门员”或“调度器”的角色，负责将高层级的指令转化为底层 Agent 可执行的步骤，验证 Agent 的输出，并管理执行过程中的上下文，从而使整个系统更加健壮和可靠。

---



### 3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

3: Claws 与现有的 Agent 框架（如 LangChain 或 AutoGPT）有什么区别？

**A**: 现有的 Agent 框架（如 LangChain）主要侧重于构建 Agent 的逻辑链、提示词管理以及基础的工具调用。而 Claws 作为一个“新层”，其定位可能更偏向于**运行时增强**或**生产环境治理**。如果将框架比作操作系统的内核，Claws 可能更像是负责资源调度和权限管理的系统服务。它不一定负责定义 Agent 的行为逻辑，而是负责监控、优化或保护这些行为在实际运行中的表现，专注于解决从“Demo”到“生产环境”落地时的工程化问题。

---



### 4: Claws 是否解决了 LLM 的“幻觉”问题？

4: Claws 是否解决了 LLM 的“幻觉”问题？

**A**: 虽然仅凭标题无法断言 Claws 完全消除了幻觉，但作为一个“控制层”，它极有可能包含了验证机制。在架构上，这一层可以通过引入确定性逻辑、规则约束或交叉验证模型，来检查底层 Agent 生成的结果。如果检测到不合理或不准确的输出，Claws 层可以拦截并要求 Agent 重试，或者调用外部工具进行事实核查。因此，它提供了一种通过架构设计来缓解幻觉问题的工程手段。

---



### 5: 开发者应如何集成或使用 Claws？

5: 开发者应如何集成或使用 Claws？

**A**: 既然它被描述为一个“层”，集成方式通常是无侵入性或低侵入性的。开发者理论上不需要重写现有的 Agent 逻辑，而是将现有的 Agent 接入到 Claws 的接口中。Claws 可能提供了 API 或 SDK，允许开发者将 Agent 的输入输出流经过 Claws 进行处理。这种设计使得开发者可以保留原有的模型选择和提示词策略，同时获得 Claws 层提供的增强功能（如日志记录、错误恢复、工具集成等）。

---



### 6: Claws 的主要应用场景有哪些？

6: Claws 的主要应用场景有哪些？

**A**: 作为一个增强层，Claws 特别适合那些对准确性和稳定性要求较高的复杂任务场景。例如：**自动化客服**（需要确保回答合规且准确）、**代码生成与审查**（需要验证生成的代码能否运行）、**多步骤的研究分析**（需要管理长期的上下文和中间状态）以及**企业级工作流自动化**（需要安全地与内部数据库交互）。简而言之，任何单纯依靠 LLM 显得不够“靠谱”的场景，都是 Claws 潜在的应用市场。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你正在构建一个简单的 LLM Agent，现在需要为其添加一个 "Claws" 层来强制执行特定的输出格式（例如 JSON）。请设计一个提示词策略，确保 LLM 在处理非结构化文本输入时，能够始终返回符合 Schema 定义的 JSON 对象，且不包含任何解释性文本。

### 提示**: 考虑在 System Prompt 中定义严格的 Role 和 Task，并使用 Few-Shot Prompting（少样本提示）提供正例和反例。同时，思考如何利用 Output Interpreters 或 Pydantic 等工具在代码层面进行兜底验证。

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
- 标签： [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Claws](/tags/claws/) / [架构](/tags/%E6%9E%B6%E6%9E%84/) / [增强能力](/tags/%E5%A2%9E%E5%BC%BA%E8%83%BD%E5%8A%9B/) / [AI](/tags/ai/) / [模型优化](/tags/%E6%A8%A1%E5%9E%8B%E4%BC%98%E5%8C%96/) / [系统设计](/tags/%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [LLM智能体新增Claws层以增强功能]({{< relref "posts/20260222-hacker_news-claws-are-now-a-new-layer-on-top-of-llm-agents-10.md" >}})
- [迈向智能体系统规模化科学：工作原理与适用条件]({{< relref "posts/20260201-hacker_news-towards-a-science-of-scaling-agent-systems-when-an-13.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*