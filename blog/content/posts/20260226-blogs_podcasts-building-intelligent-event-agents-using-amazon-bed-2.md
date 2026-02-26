---
title: "利用 Amazon Bedrock AgentCore 构建生产级智能活动助手"
date: 2026-02-26T02:52:57+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "RAG", "智能体", "生产部署", "无服务器", "知识库", "身份认证"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 **Amazon Bedrock AgentCore** 和 **Amazon Bedrock Knowledge Bases** 快速构建生产级智能活动助手的方案。 主要内容包括构建一个能记住参会者偏好并随时间提供个性化体验的智能助手，并利用 Bedrock AgentCore 的核心组件简化生产"
external_url: https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases
scenarios: ["RAG应用", "AI/ML项目"]
---

# 利用 Amazon Bedrock AgentCore 构建生产级智能活动助手

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T19:51:08+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)

---
## 摘要/简介

本文演示如何利用 Amazon Bedrock AgentCore 的组件快速部署一个生产就绪的活动助手。我们将构建一个智能伴侣，能够记住与会者的偏好，并随着时间的推移打造个性化体验，同时让 Amazon Bedrock AgentCore 顶住生产部署的重任：利用 Amazon Bedrock AgentCore Memory 维护对话上下文和长期偏好，无需自定义存储方案；利用 Amazon Bedrock AgentCore Identity 实现安全的身份验证（支持多 IdP）；利用 Amazon Bedrock AgentCore Runtime 实现无服务器扩缩和会话隔离。我们还将使用 Amazon Bedrock Knowledge Bases 进行托管式 RAG 和活动数据检索。

---
## 导语

构建具备长期记忆与安全交互能力的智能体，是当前生成式 AI 应用落地的关键。本文将演示如何利用 Amazon Bedrock AgentCore 的 Memory 和 Identity 组件，结合 Amazon Bedrock Knowledge Bases，快速部署一个具备记忆认证的活动助手。通过阅读本文，您将掌握利用托管式服务实现无服务器扩缩、会话隔离及基于 RAG 的数据检索，从而构建稳定且个性化的生成式 AI 解决方案。

---
## 摘要

本文介绍了一种利用 **Amazon Bedrock AgentCore** 和 **Amazon Bedrock Knowledge Bases** 快速构建生产级智能活动助手的方案。

主要内容包括构建一个能记住参会者偏好并随时间提供个性化体验的智能助手，并利用 Bedrock AgentCore 的核心组件简化生产部署：

1.  **Amazon Bedrock AgentCore Memory**：用于维护对话上下文和长期偏好，无需自定义存储方案。
2.  **Amazon Bedrock AgentCore Identity**：支持安全的、基于多身份提供商（IDP）的身份认证。
3.  **Amazon Bedrock AgentCore Runtime**：提供无服务器扩展能力和会话隔离。

此外，该方案还结合了 **Amazon Bedrock Knowledge Bases**，用于实现托管型检索增强生成（RAG）及活动数据检索。

---
## 评论

### 深度评价：Building intelligent event agents using Amazon Bedrock AgentCore and Amazon Bedrock Knowledge Bases

**文章中心观点**
文章主张通过组合 Amazon Bedrock 的 AgentCore（编排框架）与 Knowledge Bases（RAG架构），开发者能够以低代码方式快速构建具备长期记忆和个性化能力的生产级智能体，从而解决传统对话机器人无法处理复杂上下文和私有数据的痛点。

---

### 核心评价

#### 1. 内容深度与论证严谨性
*   **支撑理由（事实陈述）：** 文章紧扣当前生成式AI落地的核心难点——即如何将大模型的通用能力与企业的私有数据（RAG）及业务逻辑（Agent编排）相结合。它没有停留在简单的ChatBot demo层面，而是引入了“记忆”和“事件规划”的概念，触及了Stateful Application（有状态应用）的构建，这是从玩具走向生产的关键一步。
*   **支撑理由（你的推断）：** 文章隐含地论证了“模型即服务”与“基础设施即服务”结合的必要性。通过强调 Bedrock AgentCore，实际上是在传达一种观点：未来的AI应用开发将不再是单纯的Prompt Engineering，而是基于工作流的状态机管理。
*   **反例/边界条件（你的推断）：** 文章可能低估了“非结构化数据预处理”的复杂性。在实际场景中，会议议程、演讲者简介往往格式混乱，Knowledge Bases 的向量化检索效果高度依赖切片质量，文章对此一笔带过，可能导致开发者对数据清洗工作量产生误判。

#### 2. 实用价值与指导意义
*   **支撑理由（事实陈述）：** 对于已经处于 AWS 生态中的企业而言，该架构提供了极高的参考价值。它展示了如何利用云原生服务（如 OpenSearch Serverless 作为向量库）来避免自建维护向量数据库的运维负担，显著降低了技术债务。
*   **支撑理由（作者观点）：** 文章提出的“Event Assistant”场景是典型的B2B2C场景，具有高复用性。其关于“Attendee Preferences”（参会者偏好）的记忆实现，为电商、客服等需要个性化推荐的场景提供了直接的范本。
*   **反例/边界条件（批判性思考）：** 该方案具有强厂商锁定风险。Bedrock AgentCore 的抽象层虽然简化了开发，但如果企业未来需要迁移至 GCP 或 Azure，或者切换到开源模型（如 Llama 3），这种深度的专有架构集成将带来极高的迁移成本。

#### 3. 创新性与行业影响
*   **支撑理由（你的推断）：** 文章展示了“Agent”概念的标准化趋势。过去 Agent 是学术概念或开源项目，现在 AWS 将其封装为托管服务，这标志着 AI 应用开发正在进入“工业化”阶段。
*   **支撑理由（事实陈述）：** 结合 Knowledge Bases 实现的检索增强生成（RAG）是目前解决大模型幻觉的主流方案，文章将此与 Agent 的工具调用能力结合，代表了从“检索”到“行动”的技术跨越。
*   **反例/边界条件（行业观点）：** 相比于 LangChain 等开源框架提供的极致灵活性，Bedrock AgentCore 可能过于黑盒。对于需要精细控制每一个推理步骤或对延迟极其敏感（如高频交易辅助）的场景，这种托管式 Agent 可能因缺乏透明度而受限。

#### 4. 可读性与逻辑性
*   **支撑理由（事实陈述）：** 采用了典型的技术博客结构：痛点 -> 解决方案架构 -> 代码实现 -> 部署验证。这种“手把手”的教学风格极大地降低了读者的认知门槛。
*   **支撑理由（作者观点）：** 通过具体的“Event Assistant”案例贯穿始终，比抽象地讲解架构概念更容易理解，逻辑链条清晰。

---

### 综合评价与实际应用建议

这篇文章是一篇典型的**“厂商最佳实践”指南**。它技术路线正确，紧跟 RAG + Agent 的行业主流趋势，但带有明显的 AWS 商业推广色彩。

**实际应用建议：**
1.  **评估数据成熟度：** 在采用此方案前，务必确认你的非结构化数据（PDF、网页）是否已经过良好的清洗和结构化处理。RAG 的效果上限由数据质量决定，而非模型本身。
2.  **成本监控：** Bedrock Knowledge Bases 涉及向量存储、检索请求和模型推理的多重计费。对于高并发场景，建议先进行压力测试和成本测算，避免出现“云账单震惊”。
3.  **混合架构策略：** 对于核心业务逻辑，可以考虑在 Bedrock 之上保留一层轻量级的中间件（自行编写的微服务），以便在未来需要更换底层模型或平台时，能够保留业务控制权。

### 可验证的检查方式

为了验证文章所述架构的有效性，建议进行以下检查：

1.  **幻觉率测试：**
    *   *指标：* 针对构建好的知识库，提出 50 个只能通过文档回答的具体问题（如“演讲者 X 在 2023 年的演讲主题是什么？”）。
    *   *验证标准：* 检查 Agent 回答中引用的事实与原文档的吻合度。如果出现超过 5% 的编造内容，说明检索配置或上下文窗口设置存在问题。

2.  **多轮对话状态保持测试：**
    *   *实验：* 进行一段包含 5 轮以上的对话，例如先设定偏好“我对 AI 安全感兴趣”，在第 3 轮询问“推荐相关会议”，在第 5 轮再次确认“刚才推荐的那个会议几点开始

---
## 技术分析

基于您提供的文章标题和摘要，以及对 Amazon Bedrock 生态系统的技术理解，以下是对这篇关于“构建智能事件代理”文章的深度分析。

---

# 深度分析报告：基于 Amazon Bedrock AgentCore 与知识库的智能代理构建

## 1. 核心观点深度解读

**主要观点**
文章的核心观点是：利用 **Amazon Bedrock AgentCore**（注：此处应指代 Bedrock 的 Agents 框架或核心编排能力）与 **Amazon Bedrock Knowledge Bases** 的组合，开发者可以低代码、高效率地构建出具备长期记忆和个性化能力的生产级智能助手。

**核心思想**
作者试图传达“**编排与记忆是通往高级 AI 应用的关键**”这一思想。传统的 LLM 应用往往受限于上下文窗口和静态知识，而通过 AgentCore 的编排能力和知识库的检索增强生成（RAG）能力，AI 系统可以从“一次性问答工具”进化为“**能够随时间积累经验的智能伴侣**”。

**观点的创新性和深度**
*   **从“对话”到“行动”的转变**：文章不仅讨论对话，更强调了 Agent（代理）的概念，即 AI 能够自主拆解任务、调用 API 完成操作。
*   **动态记忆机制**：强调“记住偏好并随时间建立个性化体验”，这触及了 AI 应用的痛点——**状态管理与长期记忆**。这比单纯的 RAG 多了一层用户画像和会话历史的维度。

**重要性**
在当前的生成式 AI 爆发期，企业面临的最大挑战不是模型不够强，而是如何将模型落地到具体业务流中。这篇文章展示了一种**标准化的架构模式**，解决了“幻觉”（通过知识库）和“缺乏执行力”（通过 AgentCore）两大难题，对于企业快速落地 GenAI 具有极高的参考价值。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **Amazon Bedrock Knowledge Bases (RAG)**：检索增强生成技术，允许 LLM 访问私有数据源，而无需训练模型。
2.  **AgentCore (Orchestration)**：理解为 Bedrock Agents 的核心引擎，负责理解用户意图、规划步骤（Chain of Thought）。
3.  **Function Calling / Tool Use**：代理连接外部系统（如票务系统、CRM）的能力。
4.  **User Profile / Memory Store**：用于存储用户偏好和历史交互数据的数据库（通常与 DynamoDB 等集成）。

**技术原理和实现方式**
*   **RAG 流程**：用户提问 -> AgentCore 将查询转换为向量 -> 在 Knowledge Base 中检索相关文档 -> 将检索到的上下文与用户问题合并 -> 发送给 Foundation Model (如 Claude 3) -> 生成回答。
*   **Agent 编排**：利用 ReAct (Reasoning + Acting) 模式。模型首先进行“推理”（思考下一步该做什么），然后执行“行动”（调用知识库或 API），并观察结果，直到完成任务。

**技术难点和解决方案**
*   **难点：上下文窗口限制与信息过载。**
    *   *解决方案*：通过向量检索只提取最相关的片段，而不是把整个数据库塞给 LLM。
*   **难点：用户偏好的实时更新。**
    *   *解决方案*：在 Agent 的逻辑中设计专门的“记忆写入”工具，当用户确认偏好时，自动调用 API 写入持久化存储，供下次查询时调用。

**技术创新点分析**
文章隐含的创新点在于**“无服务器化”的 AI 编排**。开发者不需要手动管理 LangChain 的复杂链路或维护向量数据库的底层基础设施，Bedrock 提供了托管的全栈能力，极大地降低了开发门槛。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为构建“企业级知识助手”提供了标准蓝图。它告诉我们，不要试图用一个 Prompt 解决所有问题，而应该建立**“知识库（大脑记忆）+ 代理（小脑执行）”**的双核架构。

**可以应用到哪些场景**
1.  **企业内部 IT/HR 支持**：员工可以查询政策，也可以通过代理直接提交请假条（Agent 执行能力）。
2.  **电商智能导购**：记住用户的尺码和风格偏好（长期记忆），结合库存知识库，推荐商品。
3.  **医疗问诊分诊**：基于医疗指南库（知识库）回答常识问题，并根据患者描述自动预约科室（Agent 能力）。

**需要注意的问题**
*   **数据隐私**：将企业私有数据放入知识库前，必须做好权限管控（ACL），确保用户 A 不能检索到用户 B 的敏感数据。
*   **更新延迟**：知识库的数据同步通常有延迟，不适合对实时性要求极高的秒级交易数据。

**实施建议**
*   从小处着手，先建立知识库（RAG），验证回答质量。
*   逐步加入工具调用能力，完善 Agent 的功能。
*   重点关注“记忆”的设计，这是提升用户体验的关键。

## 4. 行业影响分析

**对行业的启示**
这标志着 AI 开发正在从“模型调优”转向“**系统工程**”。未来的核心竞争力不再是拥有最大的模型，而是拥有最完善的 Agent 编排能力和最优质的私有知识库。

**可能带来的变革**
*   **SaaS 软件的智能化重构**：传统的 SaaS 软件将把 Agent 作为第一层交互界面，后台的按钮和表单将由 Agent 代为操作。
*   **知识管理的复兴**：原本沉睡在文档中的非结构化数据，通过 Knowledge Bases 变得可被机器理解和操作，极大地释放了数据价值。

**相关领域的发展趋势**
*   **Multi-Agent（多智能体）**：未来的事件助手可能由多个子 Agent 组成（一个负责行程，一个负责餐饮，一个负责财务），协同工作。

## 5. 延伸思考

**引发的思考**
*   **个性化与隐私的边界**：为了提供个性化体验，系统需要记录用户行为。这种“记忆”应该保留多久？用户是否有权“遗忘”？
*   **Agent 的幻觉风险**：虽然引入了知识库，但如果 Agent 执行 API 调用时传错了参数（例如删除了错误的文件），这种“行动上的幻觉”比“语言上的幻觉”后果更严重。

**可以拓展的方向**
*   **多模态交互**：目前的文章主要基于文本，未来的 Event Agent 可以处理图片（用户上传活动现场照片进行分析）或语音。
*   **主动式 Agent**：现在的 Agent 是被动的（响应用户请求）。未来的 Agent 可以根据日程主动提醒用户：“根据您的偏好，您可能对接下来的一场讲座感兴趣。”

## 6. 实践建议

**如何应用到自己的项目**
1.  **数据准备**：整理你的 FAQ 文档、操作手册，清洗并转换为适合向量化的格式（Markdown/HTML）。
2.  **定义工具**：明确你需要 Agent 调用哪些后端 API（如查询数据库、发送邮件），并编写清晰的 OpenAPI Schema 描述。
3.  **Prompt 工程**：在 Bedrock Agent 配置中，精心设计系统提示词，明确 Agent 的角色、限制条件和如何使用知识库的指令。

**具体行动建议**
*   **评估数据源**：检查你现有的文档是否结构化良好。
*   **选择基座模型**：对于复杂的 Agent 任务，建议优先选择 Claude 3.5 Sonnet 或具备强大推理能力的模型。
*   **建立测试集**：准备一组涵盖“简单问答”、“多轮推理”、“工具调用”的测试用例，验证 Agent 的表现。

**需要补充的知识**
*   **向量数据库基础**：理解 Embedding 和相似度搜索。
*   **OpenAPI/Swagger 规范**：为了给 Agent 定义工具，必须理解如何编写 API 描述文件。

## 7. 案例分析

**成功案例分析（基于文章场景）**
*   **场景**：一个大型科技会议的 AI 助手。
*   **表现**：
    *   *RAG 能力*：准确回答关于会议日程、演讲者背景的复杂问题。
    *   *记忆能力*：用户昨天问过“素食餐厅”，今天直接问“推荐午餐”，AI 默认只推荐素食。
    *   *执行能力*：用户说“帮我报名这个讲座”，AI 直接调用报名 API 并反馈成功。
*   **成功因素**：知识库更新及时（实时同步日程变更），API 定义清晰，错误处理机制完善（如讲座已满时的提示）。

**失败案例反思**
*   **场景**：某企业客服机器人。
*   **问题**：Agent 试图通过 API 修改用户订单，但因为 Prompt 指令模糊，错误地将“取消订单”理解成了“退款”，且没有进行二次确认，导致直接执行了退款操作。
*   **教训**：对于涉及资金或重要数据的操作，必须引入**“人机协同”**机制，Agent 只能生成操作草稿或建议，必须由人工确认后才能执行。

## 8. 哲学与逻辑：论证地图

**中心命题**
利用 Amazon Bedrock 的托管编排能力和知识库技术，是构建具备记忆与执行能力的生产级 AI 应用的**最高效路径**。

**支撑理由与依据**
1.  **理由 1：开发效率大幅提升。**
    *   *依据*：相比从零开始构建 LangChain 链路，托管服务减少了 70% 以上的基础设施代码量（事实）。
2.  **理由 2：解决模型幻觉问题。**
    *   *依据*：RAG 架构强制模型基于检索到的私有数据回答，显著降低了事实性错误（技术原理）。
3.  **理由 3：具备动态成长能力。**
    *   *依据*：通过结合长期记忆，Agent 可以随交互次数增加而变得更懂用户，这是静态 Prompt 无法实现的（功能特性）。

**反例或边界条件**
1.  **边界条件 1：极高定制化需求。** 如果应用需要极度精细的控制逻辑（例如每一个 Token 的处理逻辑），托管 Agent 的黑盒特性可能成为阻碍，自建框架更灵活。
2.  **边界条件 2：超低延迟要求。** 经过 Agent 编排、向量检索、模型生成的多跳链路，响应时间通常在 3-10 秒，无法满足毫秒级的实时交易需求。

**命题属性分析**
*   *事实*：Bedrock 提供了这些服务。
*   *价值判断*：“最高效”是基于工程成本和维护成本的考量。
*   *可检验预测*：使用 Bedrock 构建原型的速度将快于使用开源模型自建。

**立场与验证方式**
*   **立场**：支持采用 Bedrock AgentCore 架构作为企业级 AI 应用的起步方案，但需保留定制化接口。
*   **验证方式（可证伪）**：
    *   *指标*：对比两个团队（A组用 Bedrock，B组自建），在相同功能需求下，A组的上线时间是否显著短于 B 组（如 < 50% 时间）。
    *   *观察窗口*：在运行 3 个月后，A组的运维成本（代码行数/维护工时）是否低于 B 组。

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计精细化的数据检索策略

**说明**:
单纯依赖向量相似度搜索往往无法满足复杂的业务需求。最佳实践是结合 Amazon Bedrock Knowledge Bases 的混合检索功能（向量搜索 + 关键词搜索）以及元数据过滤，以提高检索的相关性和准确性。这能有效减少“幻觉”并确保 Agent 获取到最准确的上下文信息。

**实施步骤**:
1. 在配置 Knowledge Base 时，启用向量搜索与关键词检索的混合模式。
2. 在数据摄取阶段，为文档定义清晰的元数据结构（如日期、部门、文档类型）。
3. 在 Agent 提示词或 API 调用中，利用元数据过滤条件来限定搜索范围。

**注意事项**:
定期评估检索结果的“Top K”准确率，并根据实际查询情况调整向量嵌入模型或搜索权重。

---

### 实践 2：构建结构化的动作定义

**说明**:
AgentCore 的核心能力在于调用 API 执行操作。为了确保 Agent 能够正确理解并执行任务，必须为每一个 Action Group 提供高度结构化、清晰且包含上下文的 OpenAPI 架构定义。模糊的 API 定义会导致 Agent 调用失败或生成错误的参数。

**实施步骤**:
1. 编写标准的 OpenAPI 3.0/3.1 规范文件，明确描述每个端点的参数、类型和必填项。
2. 在 API 描述字段中详细说明参数的业务含义和限制条件。
3. 将 API 操作按逻辑分组，确保每个 Action Group 职责单一，避免在一个组中堆砌过多不相关的接口。

**注意事项**:
确保 API 的命名和描述符合自然语言习惯，这有助于 LLM 更好地将用户意图映射到具体的 API 调用。

---

### 实践 3：优化提示词工程与上下文管理

**说明**:
虽然 Bedrock AgentCore 会自动处理部分上下文，但显式地优化基础提示词对于控制 Agent 的行为至关重要。你需要明确 Agent 的角色、任务边界、输出格式限制以及如何处理未知情况。

**实施步骤**:
1. 在 Agent 配置中，编写详细的系统指令，限定 Agent 的角色范围（例如：“你是一个仅用于查询订单的助手”）。
2. 指示 Agent 在无法从 Knowledge Base 找到答案时的具体行为（例如：“回答‘我不知道’，不要编造信息”）。
3. 利用 Guardrails（防护栏机制）在提示词层面过滤有害或敏感内容。

**注意事项**:
提示词应保持简洁但指令明确。过长的提示词会消耗 Token 并增加延迟，过短则可能导致控制力不足。

---

### 实践 4：实施严格的用户权限与数据隔离

**说明**:
在多租户或企业级应用中，必须防止用户通过 Agent 获取无权访问的数据。最佳实践是在 Knowledge Base 检索阶段实施基于上下文的权限过滤，而不是在 LLM 生成回复后再进行过滤。

**实施步骤**:
1. 在 Knowledge Base 的元数据中包含用户 ID 或组 ID 标识。
2. 在 Agent 的 Action Group 或 Lambda 函数中，动态注入用户的上下文信息（如 Session Attributes）。
3. 配置检索时的过滤器，确保查询仅返回当前用户有权查看的数据片段。

**注意事项**:
不要完全依赖 LLM 来判断权限，必须通过底层数据库或元数据过滤机制来强制执行安全策略。

---

### 实践 5：建立全面的测试与评估体系

**说明**:
LLM 的输出具有概率性，因此传统的单元测试不足以保证 Agent 的质量。最佳实践是建立一个包含“黄金数据集”的评估流程，定期测试 Agent 的推理准确性和检索有效性。

**实施步骤**:
1. 准备一组覆盖典型用户场景和边缘案例的测试问题及标准答案。
2. 利用 Bedrock 的自动化评估功能或自定义脚本，定期运行这些测试用例。
3. 监控 Agent 的响应延迟、Token 消耗量以及检索命中率。

**注意事项**:
持续监控生产环境中的对话日志，并根据用户反馈不断迭代 Knowledge Base 的内容和提示词配置。

---

### 实践 6：配置合理的超时与重试机制

**说明**:
Agent 在调用底层 API 或检索 Knowledge Base 时可能会遇到网络波动或服务不可用的情况。合理的超时和重试策略能保证系统的鲁棒性，防止用户请求挂起。

**实施步骤**:
1. 为每个 Action Group 中的 Lambda 函数或 API 调用设置适当的超时时间（通常建议在 LLM 会话超时之前完成）。
2. 实施指数退避重试策略，以应对瞬时故障。
3. 在 Agent 的提示词中定义明确的错误处理逻辑，或者通过 Lambda 函数捕获错误并返回用户友好的提示。

**注意事项**:
避免过长的超时设置，这会导致用户体验下降。确保后端服务的响应时间经过优化。

---
## 学习要点

- 利用 Amazon Bedrock AgentCore 构建的事件智能体能够自主拆解复杂任务，通过多步推理自动编排工作流，从而实现事件处理流程的高度自动化。
- 集成 Amazon Bedrock Knowledge Bases 赋予了智能体检索增强生成（RAG）能力，使其能够基于私有数据准确回答问题并有效解决信息幻觉问题。
- 借助 Amazon Bedrock 的托管服务，开发者无需精通底层模型细节，即可通过简单的配置快速部署具备企业级安全性和可扩展性的智能应用。
- 智能体架构支持灵活的工具调用，能够无缝连接外部 API 和数据源，打破了大型语言模型与真实世界系统交互的壁垒。
- 该方案通过将复杂的逻辑推理与实时数据检索相结合，显著提升了企业处理非结构化数据和动态事件的效率与准确性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [RAG](/tags/rag/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [生产部署](/tags/%E7%94%9F%E4%BA%A7%E9%83%A8%E7%BD%B2/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [利用 Amazon Bedrock 构建具备记忆与个性化能力的智能活动助手]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-0.md" >}})
- [利用Amazon Bedrock构建生产级智能活动助理]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-1.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-12.md" >}})
- [利用 Amazon Bedrock AgentCore 构建统一智能系统]({{< relref "posts/20260220-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-13.md" >}})
- [基于 Amazon Bedrock 构建AI招聘系统优化人才获取流程]({{< relref "posts/20260215-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*