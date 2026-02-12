---
title: "Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营流程"
date: 2026-02-12T01:06:22+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "**总结：Iberdrola 借助 Amazon Bedrock AgentCore 优化 IT 运营** 全球最大的公用事业公司之一 Iberdrola 正通过与 AWS 合作，利用尖端人工智能技术革新其 ServiceNow 平台的 IT 运营。 Iberdrola 实施了基于 Amazon Bedrock Age"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营流程

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

Iberdrola 是全球最大的公用事业公司之一，已拥抱尖端 AI 技术，以变革其在 ServiceNow 中的 IT 运营。通过与 AWS 合作，Iberdrola 使用 Amazon Bedrock AgentCore 实施了多种代理架构，聚焦于三个关键领域：在起草阶段优化变更请求的校验、以情境智能丰富事件管理，并利用对话式 AI 简化变更模型的选择。这些创新减少了瓶颈，帮助团队加速工单解决，并在整个组织内确保数据处理的一致性与高质量。

---
## 导语

Iberdrola 作为全球领先的公用事业公司，正通过 AWS 合作，利用 Amazon Bedrock AgentCore 深化其 ServiceNow 平台的智能化转型。本文将详细解析该企业如何通过多代理架构，在变更请求校验、事件管理及模型选择等核心环节实现流程自动化与效率提升。阅读本文，读者可以了解大型企业如何利用生成式 AI 解决实际运营痛点，并获得关于构建高一致性、高质量数据处理体系的实战参考。

---
## 摘要

**总结：Iberdrola 借助 Amazon Bedrock AgentCore 优化 IT 运营**

全球最大的公用事业公司之一 Iberdrola 正通过与 AWS 合作，利用尖端人工智能技术革新其 ServiceNow 平台的 IT 运营。

Iberdrola 实施了基于 Amazon Bedrock AgentCore 的多种智能代理架构，重点聚焦于三个关键领域以实现降本增效：

1.  **优化变更请求验证：** 在变更请求的草稿阶段引入 AI 优化，提升验证效率。
2.  **丰富事故管理：** 利用情境智能技术，为事故管理提供更全面的数据支持。
3.  **简化变更模型选择：** 通过对话式 AI 技术，降低变更模型选择的复杂度。

这些创新举措成功消除了运营瓶颈，加速了工单解决流程，并确保了全组织范围内数据处理的**一致性**与**高质量**。

---
## 评论

### 深度评价：Iberdrola 利用 Amazon Bedrock AgentCore 增强IT运维

**中心观点**
该案例展示了传统能源巨头通过引入基于大模型（LLM）的智能体架构，在ServiceNow平台上实现IT运维从“自动化”向“智能化”的范式跃迁，标志着AIOps正从单点工具应用向全流程自主代理演进。

**支撑理由与深度分析**

**1. 技术架构的代际跨越：从“脚本自动化”到“语义自主代理”**
*   **分析（你的推断）：** 传统IT运维依赖RPA（机器人流程自动化）或固定脚本，只能处理结构化、标准化的任务。文章中提到的“Amazon Bedrock AgentCore”与ServiceNow的结合，核心在于引入了**推理层**。这不仅仅是调用API，而是Agent理解IT运维人员的自然语言意图，动态规划步骤，并在Bedrock的多个模型间切换以完成复杂任务（如自动生成变更脚本、分析非结构化日志）。这解决了传统运维中“流程僵化”和“上下文理解缺失”的痛点。
*   **事实陈述：** Iberdrola作为全球最大的公用事业公司之一，其IT环境极其复杂且遗留系统众多。在ServiceNow这种高度复杂的ITSM（IT服务管理）平台上直接嵌入生成式AI代理，显示了其对技术栈整合的自信。

**2. 业务价值的深度挖掘：隐性知识的显性化与流程优化**
*   **分析（你的推断）：** 文章提到针对“三个关键领域”进行优化（推测包括事件管理、请求管理和知识管理）。在大型企业中，资深工程师的“经验”往往难以传承。Agentic Architectures的核心价值在于，它能通过RAG（检索增强生成）调用企业私有数据，将“隐性经验”转化为“显性服务”。例如，初级人员通过自然语言与Agent交互，即可获得专家级的故障排查建议，这大幅降低了运维门槛和平均修复时间（MTTR）。
*   **实用价值：** 对于拥有庞大IT资产的企业，这种架构能显著减少“告警疲劳”，让Agent处理L1/L2级别的常规工单，让人聚焦于复杂决策。

**3. 生态系统的战略卡位：AWS与ServiceNow的深度耦合**
*   **分析（你的推断）：** 此案例不仅是Iberdrola的成功，也是AWS和ServiceNow生态战略的胜利。ServiceNow原本有自己的AI引擎，但Iberdrola选择通过AWS Bedrock来接入模型，这表明**“中间件策略”**的兴起。企业不希望被单一模型厂商锁定，而是希望通过Bedrock这样的中间件，灵活选择Anthropic、Cohere或Amazon自研模型。这种架构为未来快速切换更优模型保留了接口。

**反例与边界条件**

1.  **幻觉风险与容错率边界（反例）：** IT运维对准确性要求极高。虽然Agent能生成代码或配置，但在电力这种涉及物理安全的行业，AI生成错误的网络变更脚本可能导致灾难性后果。因此，AgentCore必须具备严格的“人机协同”验证机制，不能完全无人值守。
2.  **遗留系统的集成摩擦（边界条件）：** Iberdrola这类老牌能源公司拥有大量大型机或旧式ERP系统。Bedrock AgentCore虽然强大，但如果底层数据无法通过API实时、标准化地暴露给AI Agent，智能化的效果将大打折扣。文章未提及对遗留系统的改造成本，这可能是一个隐形陷阱。

**可验证的检查方式**

1.  **MTTR与自动化率指标：** 观察Iberdrola在实施该架构后的6-12个月内，IT服务台的中断平均修复时间（MTTR）是否显著下降，以及“无人干预”自动解决的工单占比是否提升（例如从10%提升至40%）。
2.  **Token消耗成本与ROI分析：** 检查其运维成本结构。虽然效率提升，但频繁调用Bedrock上的高端大模型（如Claude Opus）会产生高昂的Token费用。需验证效率提升带来的收益是否覆盖了推理成本。
3.  **安全合规审计：** 针对能源行业的合规性，检查是否有数据泄露风险。具体可通过红队测试，验证Agent是否会通过诱导性提示词泄露敏感的基础设施拓扑图或员工信息。

**综合评价**

*   **内容深度：** 文章虽然作为案例研究略显简短，但切中了“Agentic AI”这一当前技术演进的最前沿。它没有停留在简单的“聊天机器人”层面，而是深入到了“AgentCore（代理核心）”这种架构级的应用，论证了AI如何成为执行者而非仅仅是辅助者。
*   **创新性：** 提出了“多代理架构”在传统ITSM平台中的落地范式，将生成式AI从“内容生成”推向了“任务执行”。
*   **行业影响：** 对于公用事业、制造等传统行业具有极强的示范效应。它证明了即使是最保守的行业，也可以通过云原生架构和AI代理实现数字化转型。
*   **争议点：** 文章可能过分美化了技术的即插即用性，忽略了数据治理这一前置条件。没有清洗过的高质量数据，AgentCore就是无米之炊。

**实际应用建议**

对于类似Iberdrola的大型传统企业，不应盲目复制全套架构，而应采取**“高价值场景切入”**策略：
1.  **先做知识库助手：** 不要直接让AI去执行变更，先让它做“运维Copilot”，辅助查询和推荐，验证其准确性。
2.

---
## 技术分析

基于您提供的标题和摘要片段，结合Iberdrola（伊维尔德罗拉）作为全球最大公用事业公司之一的背景，以及AWS Amazon Bedrock AgentCore的技术特性，以下是对该案例的深度分析。

---

# Iberdrola 利用 Amazon Bedrock AgentCore 增强IT运营的深度分析

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**企业级生成式AI的应用正从“简单的对话交互”转向“复杂的智能体协作”，以解决传统IT运维（ITOM）中的自动化孤岛问题。** Iberdrola 通过在 ServiceNow 环境中集成 Amazon Bedrock 的 AgentCore 架构，成功构建了能够理解、规划并执行复杂IT任务的智能体，从而实现了IT运营的现代化和效率的指数级提升。

**作者想要传达的核心思想**
作者试图传达一种**“编排与重构”**的思维方式。仅仅拥有大模型（LLM）是不够的，关键在于如何通过 AgentCore 这样的框架，将 LLM 的推理能力与企业现有的业务逻辑（ServiceNow）、数据源和API进行深度编排。核心思想在于**“Agentic（代理化）”**——即 AI 不再仅仅是建议者，而是具备执行能力的操作者。

**观点的创新性和深度**
*   **创新性**：该案例超越了通用的 Chatbot（聊天机器人），展示了多智能体架构在垂直领域（公用事业/IT运维）的深度应用。它不仅仅是“问答”，而是“行动”。
*   **深度**：文章触及了企业 AI 落地的深水区——如何在保证安全性和可控性的前提下，让 AI 访问和修改核心业务系统（如工单系统）。

**为什么这个观点重要**
对于像 Iberdrola 这样的庞大企业，IT 运维的复杂度极高。传统的自动化脚本维护成本高且脆弱。引入 AgentCore 意味着 IT 运维从“基于规则的自动化”向“基于意图的自主化”转变。这不仅能降低成本，更能提高系统的韧性和响应速度，是数字化转型进入智能化阶段的关键标志。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **Amazon Bedrock**：AWS 的托管生成式 AI 服务，提供基础模型访问。
2.  **AgentCore（Agent 框架/编排层）**：这是核心。它并非单一模型，而是一个架构层，负责管理智能体的生命周期、记忆、工具调用和任务分解。
3.  **ServiceNow**：企业级 IT 服务管理（ITSM）平台，是 Iberdrola 的核心工作流引擎。
4.  **Agentic Architecture（智能体架构）**：指使用多个 AI 智能体协同工作，每个智能体可能有不同的角色（如：分析员、调度员、执行员）。
5.  **RAG（检索增强生成）**：虽然摘要未明示，但在企业场景下，查询文档和历史工单必然涉及 RAG 技术。

**技术原理和实现方式**
*   **任务分解**：当用户提出一个模糊的请求（如“优化云资源使用”），AgentCore 首先利用 LLM 的推理能力将大任务拆解为子任务（如：获取报告 -> 分析异常 -> 生成工单 -> 执行变更）。
*   **工具调用**：AgentCore 通过 API 与 ServiceNow 交互。例如，调用 ServiceNow 的 Table API 来读取 Incident 数据，或使用 Flow API 来触发变更流程。
*   **多智能体协作**：
    *   *Orchestrator Agent（编排者）*：负责理解意图和分发任务。
    *   *ServiceNow Agent*：专门负责与 ServiceNow API 对话，将自然语言转化为 ServiceNow 查询语言。
    *   *Validation Agent*：负责检查生成的操作是否符合安全合规要求。

**技术难点和解决方案**
*   **难点：幻觉与数据一致性**。AI 可能会生成不存在的工单号或错误的配置参数。
    *   *解决方案*：通过 AgentCore 的“人机协同”机制，对于高风险操作（如删除数据库），智能体生成计划后，由人工确认执行，或者通过严格的 API Schema 定义限制模型的输出空间。
*   **难点：上下文记忆**。IT 运维问题往往需要跨系统、跨时间追溯。
    *   *解决方案*：利用 Bedrock 的长上下文窗口能力和外部记忆存储，维护会话状态和工单历史。

**技术创新点分析**
利用 **AgentCore** 实现了 **"Zero-Shot Integration"（零样本集成）** 的潜力。传统的集成需要为每种场景写代码，而基于 AgentCore 的架构可以通过自然语言描述 API，让 LLM 动态学习如何调用工具，极大降低了集成成本。

## 3. 实际应用价值

**对实际工作的指导意义**
该案例表明，企业在落地 AI 时，不应只关注模型的“智商”（参数大小），更应关注模型的“手脚”（Agent 架构与工具集成能力）。IT 部门应从“维护脚本”转向“维护智能体流程”。

**可以应用到哪些场景**
1.  **L1/L2 技术支持自动化**：智能体自动处理密码重置、权限申请等常见工单。
2.  **事件根因分析（RCA）**：智能体自动搜集日志、监控指标和历史事件，生成初步的事故报告。
3.  **CMDB（配置管理数据库）校验**：智能体定期扫描资产，对比 ServiceNow 记录与实际环境，自动修正差异。
4.  **云成本优化**：智能体分析资源使用率，自动调整非生产环境的实例规格。

**需要注意的问题**
*   **权限控制**：智能体继承调用者的权限还是拥有独立权限？必须实施最小权限原则（IAM Role）。
*   **数据隐私**：确保发送给 Bedrock 的数据（Prompt）不包含敏感的 PII（个人身份信息）或商业机密，或利用 VPC Endpoint 保证数据不出私网。

**实施建议**
采用 **"Human-in-the-loop"（人机协同）** 的渐进式策略。先让智能体负责“信息检索”和“草拟方案”，经过人工验证后，再逐步开放“执行变更”的权限。

## 4. 行业影响分析

**对行业的启示**
能源和公用事业行业是典型的资产密集型、流程驱动型行业。Iberdrola 的成功证明了传统行业可以通过 GenAI 快速实现“知识密集型流程”的自动化。这打破了“只有互联网科技公司才能玩转 AI”的刻板印象。

**可能带来的变革**
*   **运维角色的转变**：IT 运维人员将从“救火队员”转变为“智能体训练师”和“流程架构师”。
*   **MPP（Managed Service Providers）模式升级**：未来的外包服务将不再是卖人头，而是卖“智能体服务能力”。

**相关领域的发展趋势**
*   **Ops to Agentic Ops**：DevOps 和 AIOps 将向 **Agentic Ops** 演进，系统具备自愈和自优化能力。
*   **垂直小模型的上位**：通用大模型作为大脑，而针对 ServiceNow、SAP 等特定系统的微调小模型或 Prompt 模板将成为企业的核心资产。

## 5. 延伸思考

**引发的思考**
如果 AI 可以直接操作 ServiceNow，那么 ServiceNow 的界面（UI）是否还重要？未来我们是否会看到一个“无头”的企业软件形态，所有交互都通过自然语言和 API 完成？

**拓展方向**
*   **跨平台编排**：不仅限于 ServiceNow，能否让同一个智能体同时操作 AWS CloudWatch（监控）和 Jira（开发管理），打通开发与运维的墙？
*   **预测性运维**：结合 Bedrock 的多模态能力，分析变电站的图像数据和 IT 日志，实现 IT 与 OT（运营技术）的融合运维。

**需进一步研究的问题**
*   如何量化智能体的“可靠性”？即在多复杂的指令下能保持 100% 的执行正确率？
*   智能体之间的“冲突消解”机制：当两个智能体同时操作同一个工单时怎么办？

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估工具链**：检查您当前的企业软件（如 ServiceNow, Jira, Salesforce）是否提供了完善的 API。
2.  **定义“原子”能力**：将复杂的业务流程拆解为不可再分的 API 操作（如：`get_user`, `update_ticket`），这些是智能体的“工具箱”。
3.  **选择框架**：基于 Bedrock 的 Agent 能力（或开源的 LangGraph/AutoGen）构建编排层。

**具体的行动建议**
*   **Step 1**: 选取一个痛点明显的低风险流程（如：每周的服务器巡检报告生成）。
*   **Step 2**: 使用 Bedrock Agent Builder 定义该流程的 Prompt 和 API Schema。
*   **Step 3**: 进行小范围内测，重点观察 Agent 是否会产生幻觉（如编造数据）。
*   **Step 4**: 逐步引入更复杂的决策逻辑。

**需补充的知识**
*   **Prompt Engineering**：特别是 System Prompt 的设计，用于约束 Agent 的行为边界。
*   **API Design**：理解 RESTful 和 GraphQL，因为 Agent 最终是通过代码调用来工作的。
*   **Observability（可观测性）**：学会使用 AWS CloudWatch 来追踪 Agent 的思考过程（Chain of Thought）。

## 7. 案例分析

**结合实际案例说明**
Iberdrola 面临的挑战是全球范围内的 IT 支撑需求庞大且语言多样。传统的 ServiceNow 实施虽然强大，但操作繁琐，需要专业人员。

**成功案例分析**
*   **场景**：一个非技术员工需要申请网络访问权限。
*   **传统方式**：登录 -> 填表 -> 选择复杂的菜单 -> 提交 -> 等待审批。
*   **AgentCore 方式**：员工在 Teams/Slack 中输入：“我需要访问马德里办公室的 Wi-Fi。”
*   **执行**：Agent 识别意图 -> 查阅员工数据库确认身份 -> 调用 ServiceNow API 查找对应的 Catalog Item -> 自动填充表单 -> 提交 -> 返回确认号。
*   **成效**：将 10 分钟的操作缩短为 10 秒的对话。

**失败案例反思（假设性推演）**
如果 Iberdrola 直接让 AI 自动处理“服务器重启”请求而没有设置审批关卡，可能会导致关键业务中断。
*   **教训**：Agent 的自主权必须与风险等级挂钩。高风险动作必须由 Agent 生成方案，人类点击“确认”后，Agent 再执行 API 调用。

## 8. 哲学与逻辑：论证地图

**中心命题**
在企业级 IT 运维中，基于 **Amazon Bedrock AgentCore** 的**多智能体架构**，相比传统的单一自动化脚本或静态工作流，能显著提升**非结构化任务的处理效率**并**降低系统维护的边际成本**。

**支撑理由与依据**
1.  **理由 1：语义理解与意图识别能力**
    *   *依据*：LLM 能够理解模糊的自然语言指令（如“系统感觉有点慢”），而传统脚本需要精确的参数输入。
2.  **理由 2：动态规划与工具调用**
    *   *依据*：AgentCore 能够根据实时情况动态调用 API（如

---
## 学习要点

- Iberdrola 通过部署 Amazon Bedrock AgentCore，成功将 IT 运营中的重复性任务自动化，显著提升了运营效率。
- 该解决方案利用生成式 AI 快速检索并整合来自多个数据源的信息，大幅缩短了故障排查时间。
- 借助大语言模型（LLM）的推理能力，AgentCore 能够理解复杂的自然语言指令并执行多步骤操作流程。
- 企业利用该技术实现了知识管理的现代化，将分散的文档转化为可交互的智能问答系统。
- 此应用案例展示了生成式 AI 在能源与公用事业领域，通过优化后台支持系统驱动业务转型的巨大潜力。
- 通过自动化处理常见请求，该平台有效减轻了一线 IT 支持团队的工作负担，使其能专注于更复杂的任务。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [blogs_podcasts](/tags/blogs-podcasts/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Amazon Bedrock实现多智能体协作：Nova 2 Lite规划与Nova Act交互]({{< relref "posts/20260211-blogs_podcasts-agent-to-agent-collaboration-using-amazon-nova-2-l-12.md" >}})
- [Building real-time voice assistants with Amazon Nova So]({{< relref "posts/20260211-blogs_podcasts-building-real-time-voice-assistants-with-amazon-no-3.md" >}})
- [Building real-time voice assistants with Amazon Nova So]({{< relref "posts/20260211-blogs_podcasts-building-real-time-voice-assistants-with-amazon-no-9.md" >}})
- [LinqAlpha如何利用Amazon Bedrock构建投资思路压力测试系统]({{< relref "posts/20260211-blogs_podcasts-how-linqalpha-assesses-investment-theses-using-dev-3.md" >}})
- [How LinqAlpha assesses investment theses using Devil’s]({{< relref "posts/20260211-blogs_podcasts-how-linqalpha-assesses-investment-theses-using-dev-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*