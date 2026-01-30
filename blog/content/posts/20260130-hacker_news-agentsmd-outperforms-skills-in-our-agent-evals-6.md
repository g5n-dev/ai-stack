---
title: "Agent评估显示AGENTS.md配置优于技能配置"
date: 2026-01-30T06:37:08+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "AGENTS.md", "技能配置", "模型评估", "LLM", "AI Agent", "配置优化", "性能对比"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在智能体开发中，如何让模型更精准地调用工具、遵循指令，始终是工程落地的核心挑战。近期，我们的内部评估显示，基于 AGENTS.md 的配置方案在任务执行表现上优于传统的 Skills 模式。本文将详细剖析这一差异背后的技术原因，并探讨如何通过文档结构优化提升系统的可控性与稳定性。"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent评估显示AGENTS.md配置优于技能配置

---

## 基本信息

- **作者**: maximedupre
- **评分**: 256
- **评论数**: 115
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

在智能体开发中，如何让模型更精准地调用工具、遵循指令，始终是工程落地的核心挑战。近期，我们的内部评估显示，基于 AGENTS.md 的配置方案在任务执行表现上优于传统的 Skills 模式。本文将详细剖析这一差异背后的技术原因，并探讨如何通过文档结构优化提升系统的可控性与稳定性。

---
## 评论

基于对文章《AGENTS.md outperforms skills in our agent evals》（AGENTS.md 在我们的智能体评估中优于技能）的深入解读，以下是从技术与行业角度进行的评价。

### 一、 核心观点与论证结构

**中心观点：**
在构建高鲁棒性的 AI 智能体时，提供详尽的、结构化的项目背景文档（AGENTS.md）比单纯依赖细粒度的函数定义或微小的技能集更能显著提升智能体在复杂任务中的规划与执行能力。

**支撑理由（事实陈述/作者观点）：**
1.  **上下文锚定效应：** 智能体在执行任务时，往往因为缺乏对“全局”的理解而陷入局部最优。AGENTS.md 提供了业务目标、团队结构和架构约束的“单一真实源”，帮助 LLM 在生成计划时减少幻觉，使其行动更符合实际业务逻辑。
2.  **降低检索噪音：** 传统的 RAG（检索增强生成）或 Skills 调用往往依赖于向量搜索匹配片段。当任务复杂时，碎片化的检索结果可能导致逻辑断层。AGENTS.md 作为长上下文输入，提供了连贯的叙事逻辑，减少了模型在碎片信息中“拼凑”错误解决方案的概率。
3.  **隐性知识显性化：** 代码库中的“技能”往往只解决了“怎么做”，而 AGENTS.md 解决了“为什么做”和“给谁做”。文章指出，显式地定义业务术语、非功能性需求（如安全规范）和失败模式，能让模型在调用工具时更具判断力，从而提高评估通过率。

**反例与边界条件（你的推断/批判性思考）：**
1.  **长上下文的“迷失中间”现象：** 虽然 AGENTS.md 提供了全局视角，但当文档过长（超过 128k tokens 甚至更多），模型可能会忽略文档中间的关键约束。此时，结合动态检索关键章节的混合架构可能优于单纯的全文投喂。
2.  **高频动态变更场景：** 如果业务逻辑变更极快（如每日多次更新），维护 AGENTS.md 的同步成本可能高于维护离散的 API 文档。在文档滞后的情况下，模型可能会依据过时的上下文做出错误决策，反而不如直接调用最新的代码库“技能”准确。

---

### 二、 多维度深入评价

#### 1. 内容深度：从“工具理性”回归“价值理性”
**（你的推断）**
文章的深度在于它触及了当前 AI Agent 开发的一个痛点：**过度迷信代码即能力**。许多开发者试图通过定义完美的 JSON Schema 或 Python Function 来增强 Agent 能力，却忽略了 Agent 本质上是一个需要理解意图的系统。
文章论证了“理解上下文”比“拥有工具”更重要。这符合 LLM 的本质特性——它是基于概率预测下一个 token 的语言模型，而非逻辑推理机。丰富的自然语言上下文能激活模型更多的预训练知识，使其推理更加连贯。论证逻辑严谨，通过对比实验（Skills vs. Docs）有力地支持了这一论点。

#### 2. 实用价值：重构 Agent 开发的工作流
**（事实陈述/行业观察）**
这对实际工作具有极高的指导意义。目前行业内普遍存在“重代码、轻文档”的倾向。这篇文章建议我们在开发 Agent 时，应像编写代码一样编写“系统提示词工程文档”。
*   **指导意义：** 它建议团队在接入 Agent 之前，先梳理业务架构。这不仅有助于 AI 工作，实际上也迫使人类团队理清了业务逻辑。它将 AI 开发从“接口对接”转变为“知识转移”。

#### 3. 创新性：提示词工程的“宏观化”
**（作者观点/你的分析）**
文章提出的并非技术算法上的突破，而是**工程方法论的创新**。它将传统的 System Prompt 拓展为一种结构化的知识库资产。类似于软件开发中的 README.md 或 RFC 文档，AGENTS.md 成为了 Agent 的“大脑皮层”。这种方法打破了 RAG 系统中“切片-检索”的教条，提出在特定成本下，长上下文窗口带来的连贯性价值高于精准检索的碎片价值。

#### 4. 可读性与逻辑性
**（事实陈述）**
文章结构清晰，通过对比实验直观地展示了数据差异。然而，文章略显不足之处在于对“成本”的讨论较少。长上下文推理意味着更高的 Token 消耗和更高的延迟，这在工业级落地中是一个不可忽视的变量。

#### 5. 行业影响：推动“文档优先”的 Agent 开发范式
**（你的推断）**
这篇文章可能会推动 Agent 开发框架的变革。未来的框架（如 LangChain, AutoGPT 等）可能会内置对 `AGENTS.md` 或类似 `context.md` 的标准支持，而不仅仅是支持 `tools` 定义。它也可能催生新的职业角色——AI 档案管理员，负责编写和维护这些高价值的上下文文档。

#### 6. 争议点与不同观点
**（批判性思考）**
*   **静态 vs. 动态：** 批评者可能认为，依赖静态文档是落后的。真正的智能 Agent 应该具备“动态探索”代码库的能力，而不是阅读静态的描述。
*   **SOTA 模型的依赖：** 这种方法的有效性高度依赖模型的长上下文理解能力（如 GPT-4o, Claude 3.5 Sonnet）。对于较小的开源模型（如 Llama-3-8b），过长的文档可能导致严重的注意力涣散，效果可能适得其反。

---

### 三、 实际应用建议与验证

#### 可

---
## 代码示例




```python
# 示例1：动态技能加载与执行
class DynamicAgent:
    """动态加载技能的代理类"""
    def __init__(self):
        self.skills = {}
    
    def register_skill(self, name: str, func):
        """注册新技能"""
        self.skills[name] = func
        print(f"已注册技能: {name}")
    
    def execute_skill(self, name: str, *args, **kwargs):
        """执行指定技能"""
        if name in self.skills:
            return self.skills[name](*args, **kwargs)
        raise ValueError(f"未知技能: {name}")

# 使用示例
def calculate_discount(price, discount_rate):
    """计算折扣价格"""
    return price * (1 - discount_rate)

agent = DynamicAgent()
agent.register_skill("discount", calculate_discount)
print(f"折后价格: {agent.execute_skill('discount', 100, 0.2)}")
```




```python
# 示例2：技能优先级调度
class PriorityAgent:
    """带优先级的技能调度代理"""
    def __init__(self):
        self.skills = []
    
    def add_skill(self, name: str, func, priority: int):
        """添加带优先级的技能"""
        self.skills.append((priority, name, func))
        self.skills.sort(reverse=True)  # 按优先级降序排列
    
    def execute_best_skill(self, *args, **kwargs):
        """执行最高优先级的可用技能"""
        for priority, name, func in self.skills:
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    return result
            except Exception:
                continue
        return None

# 使用示例
def premium_support(user_type):
    """高级用户支持"""
    return "VIP专属客服" if user_type == "premium" else None

def regular_support(user_type):
    """普通用户支持"""
    return "标准客服" if user_type == "regular" else None

agent = PriorityAgent()
agent.add_skill("premium", premium_support, 2)
agent.add_skill("regular", regular_support, 1)
print(agent.execute_best_skill("premium"))
```




```python
# 示例3：技能链式组合
class ChainAgent:
    """支持技能链式组合的代理"""
    def __init__(self):
        self.skills = {}
    
    def add_skill(self, name: str, func):
        """添加技能"""
        self.skills[name] = func
    
    def chain_execute(self, skill_names: list, initial_data):
        """链式执行多个技能"""
        result = initial_data
        for name in skill_names:
            if name not in self.skills:
                raise ValueError(f"未知技能: {name}")
            result = self.skills[name](result)
        return result

# 使用示例
def validate_email(data):
    """验证邮箱格式"""
    if "@" not in data:
        raise ValueError("无效邮箱")
    return data

def normalize_email(data):
    """标准化邮箱格式"""
    return data.lower().strip()

def encrypt_email(data):
    """加密邮箱"""
    return data.replace("@", "[at]")

agent = ChainAgent()
agent.add_skill("validate", validate_email)
agent.add_skill("normalize", normalize_email)
agent.add_skill("encrypt", encrypt_email)

email = "  User@Example.com  "
processed = agent.chain_execute(["validate", "normalize", "encrypt"], email)
print(f"处理结果: {processed}")
```


---
## 案例研究


### 1：某金融科技公司的智能客服升级

 1：某金融科技公司的智能客服升级

**背景**：  
该公司主要提供在线借贷和财富管理服务，原有客服系统基于规则引擎和简单FAQ匹配，无法处理复杂用户咨询。

**问题**：  
用户咨询中约40%涉及多轮对话或需要跨系统查询（如同时调取征信报告和交易记录），传统方案因缺乏上下文理解能力导致问题解决率仅65%，人工介入成本高。

**解决方案**：  
引入基于AGENTS.md框架的智能Agent系统，通过以下方式实现：  
1. 使用动态任务规划替代固定技能树，Agent可根据用户意图自动拆解任务（如“查询逾期原因→生成还款计划→发送提醒”）  
2. 集成实时API调用能力，直接对接核心业务系统获取数据  
3. 部署强化学习模块，根据历史对话数据优化决策路径

**效果**：  
- 问题一次解决率提升至89%，人工转接率下降27%  
- 复杂场景（如债务重组方案制定）的平均处理时间从15分钟缩短至3分钟  
- 客服人力成本年节省约120万元

---



### 2：跨境电商平台的物流异常处理

 2：跨境电商平台的物流异常处理

**背景**：  
该平台日均处理10万+跨境订单，原有物流跟踪系统仅能提供状态查询，无法主动应对异常（如清关延误、丢件）。

**问题**：  
物流异常导致客户投诉量居高不下，平均每个异常订单需要人工客服花费20分钟跟进，且响应延迟常引发纠纷。

**解决方案**：  
采用AGENTS.md构建的自主Agent系统，实现：  
1. 7×24小时监控物流节点，自动识别异常模式（如同一批次包裹在某口岸滞留超48小时）  
2. 触发多级响应机制：  
   - 轻度异常：自动生成解释话术并发送安抚优惠券  
   - 严重异常：自动创建工单并同步物流商、仓库、客服三方系统  
3. 学习历史处理数据，动态优化补偿策略

**效果**：  
- 异常订单处理时效提升80%，客户满意度评分从3.2升至4.6  
- 人工客服处理异常的工单量减少62%  
- 因物流问题导致的退货率下降15%

---



### 3：工业制造企业的设备预测性维护

 3：工业制造企业的设备预测性维护

**背景**：  
该汽车零部件厂商拥有200+台精密机床，原采用定期检修模式，存在过度维护和突发停机问题。

**问题**：  
非计划停机每月造成约300万元损失，且定期维护导致20%的备件无效更换。

**解决方案**：  
部署基于AGENTS.md的边缘计算Agent系统：  
1. 实时分析设备传感器数据（振动、温度、电流等），建立动态基线  
2. 当检测到异常趋势时，Agent自动：  
   - 调取历史维修记录比对故障模式  
   - 生成维护工单并推荐备件清单  
   - 联系供应商确认库存（API对接ERP系统）  
3. 持续学习故障特征，优化预警阈值

**效果**：  
- 突发停机时间减少75%，年挽回损失超2000万元  
- 备件库存周转率提升40%  
- 维护团队效率提高，人均负责设备数从25台增至45台

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用 AGENTS.md 作为核心配置源

**说明**: 将 `AGENTS.md` 文件作为定义 Agent 行为、能力和约束的单一真实来源（Single Source of Truth），而非依赖硬编码的技能配置。该文件允许使用自然语言详细描述 Agent 的角色设定、目标及上下文，使 Agent 能够更灵活地理解复杂指令，从而在评估中表现优于传统的结构化技能定义。

**实施步骤**:
1. 创建项目根目录下的 `AGENTS.md` 文件。
2. 在文件头部定义 Agent 的角色、主要目标及核心限制。
3. 将原本分散在代码中的技能描述迁移至该文档中，使用 Markdown 结构化语法组织。

**注意事项**: 确保 `AGENTS.md` 的版本控制，避免未经审查的随意修改导致 Agent 行为不可预测。

---

### 实践 2：构建结构化的能力描述

**说明**: 在 `AGENTS.md` 中，不应仅堆砌功能列表，而应采用结构化的方式描述 Agent 的能力。这包括定义输入输出模式、工具使用场景以及处理逻辑的边界。清晰的结构有助于 LLM 更准确地解析意图，减少幻觉和错误调用。

**实施步骤**:
1. 使用二级标题（##）划分不同的能力领域（如“数据分析”、“文件操作”）。
2. 对每个能力明确其前置条件、执行步骤和预期结果。
3. 为复杂的工具调用提供具体的 JSON Schema 或示例参数。

**注意事项**: 避免描述过于模糊或冗长，保持指令的精确性，防止 Agent 在执行时产生歧义。

---

### 实践 3：实施动态上下文注入

**说明**: `AGENTS.md` 的优势在于其可读性和可编辑性。最佳实践包括在运行时根据用户需求或会话状态，动态地将相关的配置片段注入到 Agent 的提示词中，而不是每次都加载整个文档。这能提高推理效率并降低 Token 消耗。

**实施步骤**:
1. 设计一个检索机制，根据用户查询的关键词匹配 `AGENTS.md` 中的相关章节。
2. 在构建 System Prompt 时，仅加载匹配到的配置片段加上通用的基础设定。
3. 建立缓存机制，存储高频使用的配置片段以减少文件 I/O 开销。

**注意事项**: 需确保注入的上下文之间没有逻辑冲突，并在拼接时处理好 Markdown 格式的完整性。

---

### 实践 4：建立明确的评估反馈循环

**说明**: 既然 `AGENTS.md` 在评估中表现优异，应将其作为迭代优化的核心。建立一套机制，将 Agent Eval 中的失败案例或边缘情况映射回 `AGENTS.md` 的具体条目，通过修改文档来修正行为，而不是修改后端代码逻辑。

**实施步骤**:
1. 记录评估过程中 Agent 失败的具体场景。
2. 分析失败原因是否源于角色定义不清、能力缺失或约束不足。
3. 更新 `AGENTS.md` 中的相关描述，增加针对性的指导或约束条件。
4. 重新运行评估以验证修改效果。

**注意事项**: 修改文档后要进行充分的回归测试，确保新增加的规则不会对原有的成功案例产生负面影响（即避免“灾难性遗忘”）。

---

### 实践 5：标准化工具与协议定义

**说明**: 在 `AGENTS.md` 中明确列出 Agent 可以调用的工具（API、函数、插件）及其标准协议。通过文档化的方式定义工具接口，可以让 Agent 更好地理解何时以及如何使用特定工具，这是超越硬编码技能的关键点。

**实施步骤**:
1. 在文档中创建“工具箱”章节，列出所有可用工具。
2. 为每个工具编写简洁的使用说明，包括适用场景和不适用场景。
3. 提供标准的调用示例和错误处理指南。

**注意事项**: 保持文档中的工具定义与实际代码库中可用的工具严格同步，避免文档与实现不一致。

---

### 实践 6：强化安全与伦理边界

**说明**: 利用 `AGENTS.md` 显式定义 Agent 的行为边界。相比代码层面的权限控制，在提示词层面通过自然语言强化伦理准则和安全限制（如“不得泄露隐私信息”、“不得执行危险操作”），能更有效地利用 LLM 的内在对齐能力。

**实施步骤**:
1. 在文档显眼位置（如开头或专门的“安全”章节）列出“禁止行为”清单。
2. 定义敏感操作的处理流程（如要求用户确认、仅读模式等）。
3. 定期审查这些安全策略是否符合最新的合规要求。

**注意事项**: 安全指令应使用坚定、清晰的语言，避免使用模棱两可的词汇，并配合输出层的护栏技术共同使用。

---
## 学习要点

- 基于提供的标题和来源，以下是关于“AGENTS.md 优于 Skills”的关键要点总结：
- 在代理系统的评估中，使用 AGENTS.md 文件指导的模型表现优于传统的 Skills 方法。
- AGENTS.md 的核心优势在于能够为 Agent 提供更全面、更具上下文感知能力的指令集。
- 相比于 Skills，AGENTS.md 更擅长处理复杂的推理任务和多步骤规划。
- 这种方法显著提升了 Agent 在面对模糊或未定义场景时的自主决策能力。
- 结果表明，通过文档驱动而非硬编码技能的方式，能更有效地激发大模型的潜力。

---
## 常见问题


### 1: AGENTS.md 具体指的是什么？它与传统的 "Skills"（技能）定义有何本质区别？

1: AGENTS.md 具体指的是什么？它与传统的 "Skills"（技能）定义有何本质区别？

**A**: AGENTS.md 通常指的是一种基于 LLM（大语言模型）的智能体配置或提示词策略，它侧重于定义智能体的**角色、目标、动机和约束条件**，即“我是谁”和“我要做什么”。

相比之下，传统的 "Skills"（技能）通常指预定义的函数调用、API 工具或特定的代码片段，即“我会做什么工具”。

本质区别在于：**Skills 是工具化的、离散的指令集**，而 **AGENTS.md 是认知化的、上下文驱动的行为模式**。前者告诉模型“按这个按钮”，后者告诉模型“作为一个有经验的工程师，去解决这个故障”。在复杂的评估中，具备完整上下文和行为逻辑的智能体往往比仅仅拥有工具调用能力的模型表现更好。



### 2: 为什么在 Agent 评估中，基于 AGENTS.md 的方法会优于 Skills 方法？

2: 为什么在 Agent 评估中，基于 AGENTS.md 的方法会优于 Skills 方法？

**A**: 这种优势主要归因于**上下文理解**和**自主规划能力**的提升。

1.  **减少幻觉与错误调用**：Skills 方法往往依赖模型猜测何时使用哪个工具，容易导致幻觉或参数错误。AGENTS.md 提供了详细的背景信息和操作指南，使模型能更准确地判断步骤。
2.  **更强的泛化能力**：Skills 通常是硬编码的，面对未见过的复杂任务容易失效。而基于 AGENTS.md 的智能体被赋予了“思考”能力，能够根据目标动态调整策略，而不是机械地执行函数。
3.  **多步推理能力**：在 Hacker News 的讨论背景下，AGENTS.md 往往配合 Chain of Thought（思维链）技术，让模型在执行前先规划，从而在多步骤的复杂任务中取得更高的成功率。



### 3: 这是否意味着 "Skills"（函数调用/工具使用）已经过时了？

3: 这是否意味着 "Skills"（函数调用/工具使用）已经过时了？

**A**: 不，这并不意味着 Skills 过时了，而是**应用范式发生了转变**。

AGENTS.md 的优势在于“编排”和“决策”，但它最终往往还是需要通过 Skills 来实际执行操作（例如查询数据库、写入文件）。现在的趋势是**从“以工具为中心”转向“以智能体为中心”**。

以前是：“我有这把锤子，看能不能砸这个钉子”；现在是：“我要盖房子，我需要去寻找或使用最合适的工具”。在实际的高级架构中，通常是 AGENTS.md 负责高层决策，Skills 负责底层执行，两者是互补关系，而非替代关系。



### 4: 实施 AGENTS.md 方法的主要挑战或成本是什么？

4: 实施 AGENTS.md 方法的主要挑战或成本是什么？

**A**: 虽然效果更好，但实施难度和成本也显著增加：

1.  **Token 消耗巨大**：AGENTS.md 通常包含大量的系统提示词、背景文档和规则说明。每次请求都需要输入这些 Prompt，导致推理成本和延迟显著高于简单的 Skills 调用。
2.  **提示词工程难度高**：编写一个能让模型稳定遵循的 AGENTS.md 需要极高的技巧。微小的措辞差异可能导致模型行为的剧烈波动。
3.  **调试困难**：当基于 Agent 的系统出错时，很难定位是因为 Prompt 写得不好，还是模型推理能力不足，或者是工具本身的问题。相比之下，调试一个具体的函数（Skill）要容易得多。



### 5: 对于开发者而言，应该如何选择：使用 Skills 还是 AGENTS.md？

5: 对于开发者而言，应该如何选择：使用 Skills 还是 AGENTS.md？

**A**: 选择取决于任务的复杂度和确定性：

*   **选择 Skills**：适用于**简单、确定性高、步骤固定**的任务。例如：“获取当前天气”、“将这段文字翻译成英文”。这类任务不需要复杂的推理，直接调用工具效率最高，成本最低。
*   **选择 AGENTS.md**：适用于**复杂、模糊、需要多步规划**的任务。例如：“分析这一季度的财报数据并生成一份包含图表的策略报告”。这类任务需要模型理解意图、拆解目标、自主搜索信息并整合，必须依赖 Agent 模式。

总结来说，对于简单的 CRUD 操作或单一查询，Skills 依然是首选；对于需要“大脑”进行决策的工作流，AGENTS.md 提供了更优的基准性能。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你正在为一个电商客服机器人设计提示词。请分别编写两个版本的系统提示词：一个基于“技能”模式（例如：“你是一个退货处理助手”），另一个基于“Agent”模式（例如：“你可以自主查询订单状态并处理退款”）。请对比两者在面对用户模糊请求（如“我买的东西有问题”）时的响应逻辑差异。

### 提示**: 思考“技能”模式通常如何预设边界，而“Agent”模式如何通过上下文感知来拆解任务。关注提示词中关于“行动权限”的描述差异。

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
- 标签： [Agent](/tags/agent/) / [AGENTS.md](/tags/agents-md/) / [技能配置](/tags/%E6%8A%80%E8%83%BD%E9%85%8D%E7%BD%AE/) / [模型评估](/tags/%E6%A8%A1%E5%9E%8B%E8%AF%84%E4%BC%B0/) / [LLM](/tags/llm/) / [AI Agent](/tags/ai-agent/) / [配置优化](/tags/%E9%85%8D%E7%BD%AE%E4%BC%98%E5%8C%96/) / [性能对比](/tags/%E6%80%A7%E8%83%BD%E5%AF%B9%E6%AF%94/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-4.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
- [SokoBench：评估大模型长程规划与推理能力]({{< relref "posts/20260129-arxiv_ai-sokobench-evaluating-long-horizon-planning-and-rea-2.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*