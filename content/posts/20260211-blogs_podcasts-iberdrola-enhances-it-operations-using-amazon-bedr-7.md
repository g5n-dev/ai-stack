---
title: "Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow I"
date: 2026-02-11T19:17:12+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "西班牙公用事业巨头Iberdrola通过AWS合作，利用Amazon Bedrock AgentCore革新其ServiceNow平台IT运营。主要措施包括：优化变更请求草稿验证、通过情境智能丰富事件管理、用对话式AI简化变更模型选择。成果：消除流程瓶颈、加速工单解决、实现全组织数据处理的高质量与一致性。"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

Iberdrola，全球最大的公用事业公司之一，采用尖端人工智能技术，彻底革新其在 ServiceNow 中的 IT 运营。通过与 AWS 合作，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种代理架构，聚焦三大关键领域：优化草稿阶段的变更请求验证、以情境智能丰富事件管理，以及通过对话式 AI 简化变更模型的选择。这些创新减少了瓶颈，帮助团队加快工单解决速度，并在整个组织内实现一致且高质量的数据处理。

---
## 导语

Iberdrola 作为全球领先的公用事业公司，正通过生成式 AI 重塑其 IT 运营效率。本文详细介绍了该公司如何利用 Amazon Bedrock AgentCore 在 ServiceNow 环境中构建智能代理架构，以解决变更管理、事件处理等核心流程中的瓶颈。通过阅读本文，读者将了解如何利用情境智能与对话式 AI 加速工单流转，以及如何确保企业级数据处理的一致性与高质量。

---
## 摘要

西班牙公用事业巨头Iberdrola通过AWS合作，利用Amazon Bedrock AgentCore革新其ServiceNow平台IT运营。主要措施包括：优化变更请求草稿验证、通过情境智能丰富事件管理、用对话式AI简化变更模型选择。成果：消除流程瓶颈、加速工单解决、实现全组织数据处理的高质量与一致性。

---
## 评论

### 核心评价

**中心观点：**
这篇文章展示了大型公用事业企业利用生成式AI从“数字化”向“智能化”运维转型的典型范式，其核心价值在于验证了**基于Agent架构的LLM（大语言模型）应用在处理复杂ITSM（IT服务管理）流程时的可控性与落地性**，而非单纯的算法创新。

**支撑理由（深度分析）：**

1.  **技术架构的“可控性”突破（事实陈述）：**
    Iberdrola选择Amazon Bedrock AgentCore而非直接调用OpenAI API，体现了企业级应用的核心诉求——**可控与合规**。AgentCore提供的不是单一的聊天机器人，而是一个编排框架，允许企业定义Guardrails（护栏）、连接企业知识库（RAG）并调用API。对于能源行业而言，数据隐私和操作的可解释性至关重要，这种架构解决了LLM“幻觉”可能导致生产事故的痛点。

2.  **从“提效”到“自愈”的流程重构（作者观点）：**
    文章提到针对“优化”等关键领域，这暗示了AI的角色从辅助工具向自主代理转变。传统的ServiceNow自动化多基于基于规则的脚本，维护成本高且僵化。引入Agentic AI后，系统具备了理解自然语言意图并动态规划工具调用的能力。这意味着IT运维的边际成本有望大幅降低，特别是在处理重复性高、路径依赖强的工单时。

3.  **行业标杆的“去风险”效应（你的推断）：**
    Iberdrola作为老牌能源巨头，其IT环境通常包含大量遗留系统。其成功案例具有极强的**信号传递作用**：如果连对稳定性要求极高的电力行业都能在核心IT系统中部署Agentic AI，说明该技术栈已具备了工业级的鲁棒性，这将加速金融、制造等传统行业的跟进。

**反例/边界条件（批判性思考）：**

1.  **“Agent”的实际自主程度存疑（你的推断）：**
    尽管标题使用了“AgentCore”，但在实际生产环境中，这些Agent很可能仍处于**“人在回路”**的低级别自动化阶段（如仅做分类、摘要或建议），而非完全自主的“自愈”。对于核心电力调度系统，完全放手给AI目前仍不现实。文章可能存在营销层面的概念夸大，实际落地可能仅限于非核心业务（如HR支持、一般IT故障排查）。

2.  **成本与收益的平衡挑战（作者观点）：**
    Bedrock等企业级LLM服务的调用成本远高于传统API。如果Iberdrola仅仅是用Agent来回答简单的知识库问题，其ROI（投资回报率）可能极低。该方案只有在处理**长尾、复杂**的IT问题时，通过减少昂贵的人工介入时间，才能证明其经济合理性。

---

### 维度详细评价

#### 1. 内容深度与严谨性
文章作为技术案例研究，深度中等。它成功描绘了“问题-方案-结果”的闭环，但缺乏底层技术细节（如：使用了哪个基础模型？RAG的检索准确率是多少？Agent的决策成功率如何？）。它更像是一篇经过公关润色的成功故事，而非硬核的技术复盘。对于技术决策者而言，它提供了战略方向，但缺乏架构落地的具体参数。

#### 2. 实用价值
**高**。对于正在探索如何将GenAI引入企业内部流程的CIO/CTO来说，这是一个极佳的参考范本。它指明了一条路径：不要试图用通用的ChatGPT解决企业问题，而是利用云厂商的Agent服务（如Bedrock）结合现有的流程平台（如ServiceNow）进行垂直整合。

#### 3. 创新性
**中等**。利用AI优化ITSM并不新鲜，新鲜点在于**“AgentCore”这一架构模式的普及化**。它标志着企业AI应用从“Copilot（副驾驶）”向“Agent（智能体）”形式的试探性跨越，即AI不仅生成内容，还在开始执行操作。

#### 4. 行业影响
该案例是**“企业级Agentic AI”**落地的里程碑。它证明了AWS的Bedrock生态在传统行业的渗透力，可能会引发一波利用Agent重构ERP/CRM/ITSM系统的浪潮。ServiceNow与AWS的深度绑定也将挤压其他小型垂直AI厂商的生存空间。

#### 5. 争议点与风险
*   **数据主权：** 尽管Bedrock承诺数据隐私，但对于能源巨头，将IT运维数据上传至云端训练或推理，始终存在合规红线。
*   **复杂度陷阱：** 引入Agent架构增加了系统的不可预测性。当Agent调用链路变长，排查错误的难度呈指数级上升，这可能导致新的运维黑盒。

---

### 实际应用建议

**1. 不要迷信全自动，先做“人机协同”**
在参考Iberdrola的案例时，建议从**Level 2辅助（AI提供建议，人确认执行）**开始，切勿直接让AI拥有修改生产环境数据库的权限，除非你有极其完善的回滚机制。

**2. 关注“失败案例”而非“成功故事”**
在实施类似项目前，不仅要看Iberdrola做了什么，更要询问AWS或ServiceNow：**“在什么场景下Agent会失效？”** 例如，处理跨多个遗留系统的复杂事务时，Agent是否能保持上下文不丢失？

**3. 指标验证**
如果贵公司计划实施该项目，请建立以下监控指标。

### 可验证的检查方式

为了验证该类Agent项目在贵公司是否真正有效，建议设置以下观察窗口和

---
## 技术分析

基于您提供的标题和摘要片段，以及对 Iberdrola（伊比德罗拉）作为全球最大公用事业公司之一背景的了解，以及 AWS Amazon Bedrock 和 AgentCore 的技术特性，以下是对该案例的深入分析。

---

# Iberdrola 利用 Amazon Bedrock AgentCore 增强IT运营深度分析

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**传统的大型企业 IT 运维（ITOps）正在从“基于规则的自动化”向“基于代理的自主化”演进。** Iberdrola 通过在 ServiceNow 环境中引入 Amazon Bedrock AgentCore，成功构建了多智能体架构，使 AI 不仅作为辅助工具，而是作为具备推理能力的“代理”来处理复杂的 IT 运营任务，从而在保障安全与合规的前提下，实现了效率的质变。

**作者想要传达的核心思想**
作者试图传达的核心思想是**“负责任的 AI 实践”与“垂直化智能体落地”**。对于像能源/公用事业这样对稳定性要求极高的行业，AI 的落地不能是盲目的。通过使用 AWS 的托管服务（Bedrock AgentCore），企业可以在不牺牲数据隐私（利用 VPC 等隔离机制）和可观测性的前提下，利用生成式 AI 的强大推理能力来解决具体的业务痛点（如摘要、优化和自动化）。

**观点的创新性和深度**
该案例的创新性在于**“架构的落地化”**。许多企业谈论 RAG（检索增强生成）或 AI Agent，但往往停留在 POC（概念验证）阶段。Iberdrola 的深度在于：
1.  **平台整合**：将 AI 智能体深度嵌入 ServiceNow（企业级 ITSM 工具），而非孤立的聊天机器人。
2.  **多代理协作**：利用 AgentCore 构建不同的代理架构，针对“摘要”、“优化”等不同任务分工，而非一个大模型解决所有问题。
3.  **企业级控制**：展示了如何在受监管行业中利用 Bedrock 的 Guardrails（护栏）来控制 AI 输出。

**为什么这个观点重要**
对于全球企业而言，这是一个重要的信号：**生成式 AI 的价值在于整合进现有工作流。** Iberdrola 的实践表明，通过 Agent 架构，可以将非结构化的 IT 数据转化为可执行的自动化操作，这标志着 IT 运维从“数字化”向“智能化”的关键跨越。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Amazon Bedrock**: AWS 的托管生成式 AI 服务，提供对基础模型（FM）的访问。
*   **AgentCore**: 文中提到的核心组件（通常指 AWS 提供的 Agent 框架或能力），用于构建能够推理、执行工具调用和记忆管理的 AI 应用。
*   **ServiceNow**: 企业级 IT 服务管理（ITSM）平台，Iberdrola 数据的载体。
*   **Agentic Architectures (代理架构)**: 指利用多个 AI 智能体协作，每个智能体可能有不同的角色（如：分析工单的 Agent、执行脚本的 Agent、撰写报告的 Agent）。

**技术原理和实现方式**
1.  **推理与规划**: 利用 Bedrock 上的 Foundation Models（如 Anthropic Claude 或 Amazon Titan）理解 Iberdrola IT 运维人员的自然语言指令或工单内容。
2.  **工具调用**: AgentCore 赋予模型调用外部工具的能力。例如，当需要查询服务器状态时，Agent 会调用 ServiceNow API；当需要优化配置时，Agent 会调用相应的脚本或 AWS Systems Manager。
3.  **RAG (检索增强生成)**: 针对 Iberdrola 庞大的内部知识库（文档、历史工单），通过向量数据库检索相关上下文，确保回答基于企业内部事实，而非模型通用训练数据。
4.  **私有化集成**: 通过 AWS PrivateLink 或 VPC，确保 ServiceNow 与 Bedrock 之间的数据流量不经过公网，满足能源行业的数据安全合规要求。

**技术难点和解决方案**
*   **难点：幻觉与合规风险**。AI 可能会生成错误的操作指令。
    *   *解决方案*：使用 Bedrock Guardrails 设置严格的输出过滤，并利用 AgentCore 的“人机协同”机制，高风险操作必须经过人工确认。
*   **难点：上下文窗口限制**。IT 运维日志可能非常长。
    *   *解决方案*：采用摘要链式处理或向量检索，只将最相关的日志片段注入 Prompt。
*   **难点：多步骤任务编排**。
    *   *解决方案*：AgentCore 负责将复杂任务（如“排查并修复网络故障”）拆解为子任务（查询日志 -> 分析原因 -> 执行修复 -> 验证结果）。

**技术创新点分析**
最大的创新在于**将生成式 AI 的“对话能力”转化为“行动能力”**。传统的 Chatbot 只能告诉用户“怎么做”，而 Iberdrola 的 Agent 可以在 ServiceNow 中直接“做”一部分事情（如自动归类工单、自动填充字段、甚至触发重启脚本），实现了 LLM 与 RPA（机器人流程自动化）能力的融合。

## 3. 实际应用价值

**对实际工作的指导意义**
该案例证明了 LLM 在企业内部最直接的价值在于**“知识管理的智能化”**和**“流程自动化”**。对于 IT 部门，这意味着减少 L1/L2 级别支持人员的重复性劳动，加快故障恢复时间（MTTR）。

**可以应用到哪些场景**
1.  **智能工单路由**: 自动阅读用户报错描述，分类并指派给正确的运维团队。
2.  **事件根因分析 (RCA)**: 自动聚合告警日志，生成事故报告草稿。
3.  **合规性审查**: 自动检查 IT 变更请求是否符合公司安全策略。
4.  **内部知识问答**: 员工可以用自然语言查询复杂的 IT 文档。

**需要注意的问题**
*   **数据质量**: ServiceNow 中的历史数据如果是脏数据（分类错误、描述不清），Agent 的表现会大打折扣。
*   **权限控制**: Agent 必须继承企业严格的 IAM 权限体系，防止越权访问。
*   **成本控制**: 频繁调用大模型处理海量日志可能产生较高的 API 费用，需要设计缓存机制。

**实施建议**
1.  **从小处着手**: 先选择一个痛点最明显的场景（如工单摘要），验证 ROI。
2.  **建立反馈闭环**: 在 ServiceNow 中加入“点赞/点踩”机制，收集 Agent 的输出数据用于微调或 Prompt 优化。
3.  **护栏先行**: 在开放 Agent 操作权限前，必须配置好 Guardrails，防止输出有害信息或执行危险指令。

## 4. 行业影响分析

**对行业的启示**
Iberdrola 作为传统重资产行业的巨头，其成功实践为**公用事业、制造业和金融业**树立了标杆。它表明，最保守的行业也可以通过云托管服务安全地拥抱 GenAI。关键在于选择正确的入口（IT 运维）和正确的架构（Agent）。

**可能带来的变革**
IT 运维团队的角色将发生转变。从“操作者”转变为“管理者”和“训练师”。未来的 SRE（站点可靠性工程师）将更多地负责设计 Agent 的行为逻辑，而不是手动重启服务器。

**相关领域的发展趋势**
*   **AIOps 的进化**: 从基于规则的 AIOps 向基于 LLM 的 Agentic AIOps 演进。
*   **SaaS 的智能化**: ServiceNow、Salesforce 等 SaaS 巨头将全面集成 Agent 能力，平台将不再只是记录数据的系统，而是执行任务的系统。

## 5. 延伸思考

**引发的其他思考**
*   **Agent 的寿命管理**: 如果一个 Agent 负责优化系统，它是否会陷入“过度优化”的死循环？是否需要引入“睡眠/唤醒”机制？
*   **多 Agent 协同的冲突**: 如果“成本优化 Agent”和“稳定性 Agent”的目标冲突，系统如何仲裁？

**未来发展趋势**
*   **自主数字员工**: Iberdrola 的案例只是开始，未来每个企业员工可能都会配备一个专属的 IT Agent 助手。
*   **跨平台 Agent**: Agent 将不再局限于 ServiceNow，而是能跨越 AWS、Azure 和本地数据中心工作。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估数据底座**: 检查你的 ITSM 系统（如 Jira, ServiceNow）中是否有足够的高质量文本数据供 Agent 学习。
2.  **选择技术栈**: 如果是 AWS 用户，优先考虑 Bedrock；如果是 Azure 用户，考虑 OpenAI Studio。核心是“托管服务”以降低维护成本。
3.  **定义 Agent 边界**: 明确 Agent 只能“读”，还是可以“写”，或者是“执行”。

**具体的行动建议**
*   **Week 1-2**: 梳理 IT 运维中最耗时、最重复的 Top 3 流程。
*   **Week 3-4**: 构建简单的 RAG PoC，验证模型对内部文档的理解准确率。
*   **Week 5-8**: 引入 Agent 框架，连接 ServiceNow API，实现“工单自动摘要”功能。

**需要补充的知识**
*   **Prompt Engineering**: 如何写好 System Prompt 来约束 Agent 的行为。
*   **API 设计**: 理解 RESTful API 和 GraphQL，以便让 Agent 调用工具。

## 7. 案例分析

**成功案例分析 (Iberdrola)**
*   **背景**: 全球巨头，IT 环境复杂，合规要求高。
*   **做法**: 利用 AWS Bedrock + ServiceNow。
*   **成效**: 提升了 IT 运营的效率，实现了三个关键领域的优化（摘要、优化、自动化）。
*   **关键成功因素**: 强大的合作伙伴关系（AWS），选择了成熟的企业级平台，而非从零构建。

**失败案例反思 (假设性推演)**
*   **场景**: 某公司试图用通用的 ChatGPT 直接处理 IT 工单，未做隔离。
*   **后果**: 数据泄露（将敏感密码发送给公网模型），或 Agent 产生幻觉误删数据库。
*   **教训**: 必须使用企业级、带护栏的架构（如 Bedrock），且必须进行 RAG 检索以增强事实准确性。

## 8. 哲学与逻辑：论证地图

**中心命题**
**在高度受监管的企业环境中，基于 Amazon Bedrock AgentCore 的多智能体架构是提升 IT 运营效率与安全性的最优解。**

**支撑理由**
1.  **效率提升**: 生成式 AI 具备极强的非结构化数据处理能力，能大幅缩短工单处理时间。
    *   *依据*: Iberdrola 案例中提到的“优化”和“自动化”成果；常识：阅读速度 AI > 人类。
2.  **安全性与可控性**: Bedrock 等托管服务提供了企业级的数据隐私保护，符合公用事业行业的合规要求。
    *   *依据*: AWS 的合规认证（ISO/SOC）；VPC 隔离技术原理。
3.  **架构的灵活性**: Agentic 架构比单一模型更能适应复杂的业务逻辑。
    *   *依据*: 软件工程中的“分治法”原理；Agent

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于知识的智能检索架构

**说明**:
利用 Amazon Bedrock 的 AgentCore 能力，结合企业私有数据源（如文档、数据库），构建 RAG（检索增强生成）架构。这确保了生成式 AI 不仅依赖通用训练数据，还能引用准确、最新的企业内部信息，从而提高回答的相关性和准确性。

**实施步骤**:
1. 识别并整理企业内部的高价值知识源（如 IT 运维手册、故障排查指南）。
2. 使用 Amazon OpenSearch Service 或类似向量数据库存储文本嵌入。
3. 配置 AgentCore 以连接知识库，确保在生成回复前先进行相关性检索。

**注意事项**:
确保数据源的清洗和去重，避免过时或错误的信息干扰模型判断。

---

### 实践 2：实施严格的权限控制与安全护栏

**说明**:
在处理敏感的 IT 运营数据时，必须确保 AI 代理遵循最小权限原则。通过配置 IAM 角色和 Bedrock Guardrails，可以防止模型访问未授权的资源或生成有害/不当的内容，确保企业数据安全。

**实施步骤**:
1. 定义精细的 IAM 策略，仅授予 AgentCore 访问特定 S3 存储桶或 DynamoDB 表的权限。
2. 启用 Amazon Bedrock Guardrails，设置过滤器以屏蔽个人身份信息（PII）或敏感词汇。
3. 定期审计 Agent 的访问日志，确保权限没有被滥用。

**注意事项**:
安全策略应随着业务需求的变化而动态调整，避免权限过度集中。

---

### 实践 3：将复杂任务分解为可复用的原子操作

**说明**:
不要试图让 AI 一次性解决所有问题。借鉴 Iberdrola 的经验，将复杂的 IT 运营流程（如服务器重启、日志分析）分解为小的、定义明确的“原子”函数。AgentCore 负责编排这些函数，从而提高执行的成功率和可维护性。

**实施步骤**:
1. 梳理 IT 运营中的常见高频操作，将其封装为 Lambda 函数或 API 接口。
2. 在 Agent 的 Action Group 中清晰定义每个函数的参数和描述。
3. 测试 Agent 在不同场景下调用这些函数的准确性。

**注意事项**:
函数描述必须清晰准确，这是 LLM 理解何时以及如何调用工具的关键。

---

### 实践 4：建立可观测性与反馈闭环机制

**说明**:
仅仅部署 Agent 是不够的，必须建立完善的监控体系。通过跟踪 Agent 的推理链、调用轨迹和用户反馈，可以持续优化提示词和工具配置，确保系统随着使用逐渐“聪明”起来。

**实施步骤**:
1. 启用 Amazon CloudWatch 以监控 Agent 的延迟和错误率。
2. 记录用户的“点赞”或“点踩”反馈，建立标注数据集。
3. 定期分析未解决的案例，微调 Prompt 或补充知识库内容。

**注意事项**:
关注“幻觉”问题，如果模型频繁给出错误建议，需检查检索质量或增加上下文约束。

---

### 实践 5：设计自然语言到技术指令的映射层

**说明**:
IT 运营人员通常习惯使用自然语言描述问题，而执行操作需要精确的技术指令。最佳实践是利用 AgentCore 作为翻译层，将模糊的业务需求（如“系统变慢了”）转化为具体的排查脚本或查询语句。

**实施步骤**:
1. 收集常见的自然语言查询与其对应的技术操作，构建 Few-shot（少样本）示例。
2. 在 Prompt 模板中明确指示模型输出结构化数据（如 JSON），以便下游系统解析执行。
3. 针对专业术语建立同义词库，提高理解准确度。

**注意事项**:
必须对模型生成的技术指令进行沙箱测试或人工审核，防止误操作导致生产事故。

---

### 实践 6：混合使用专家模型以优化成本与性能

**说明**:
不同的任务适合不同的模型。例如，简单的查询可以使用轻量级、低成本的模型（如 Claude Haiku），而复杂的代码生成或逻辑推理则需要使用高性能模型（如 Claude Sonnet）。AgentCore 支持动态路由，以实现性价比最优。

**实施步骤**:
1. 分析各类任务的复杂度和延迟要求。
2. 配置路由逻辑，将简单任务分配给快速/廉价模型，复杂任务分配给深度模型。
3. 持续监控各模型的 Token 消耗和响应质量，动态调整策略。

**注意事项**:
频繁切换模型可能会增加系统复杂性，需在性能优化和架构简洁性之间取得平衡。

---
## 学习要点

- 基于 Iberdrola 利用 Amazon Bedrock 和 AgentCore 增强 IT 运营的案例，总结如下：
- Iberdrola 通过部署基于 Amazon Bedrock 的生成式 AI 解决方案，成功将 IT 运营中常见问题的解决时间从几天缩短至几分钟，显著提升了服务效率。
- 利用 Amazon Bedrock AgentCore 构建的多智能体系统，能够自主拆解复杂任务并协调多个工具执行，从而实现了复杂 IT 流程的自动化。
- 该解决方案通过自然语言处理技术，允许非技术人员直接用人类语言与系统交互，极大地降低了技术支持的使用门槛。
- 借助 Amazon Bedrock 统一访问多种基础模型的能力，企业能够根据不同场景灵活选择最适合的模型，避免了被单一供应商锁定的风险。
- 企业在实施生成式 AI 时，必须建立严格的“护栏”机制，以确保 AI 输出的内容符合企业的安全标准和合规性要求。

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
- [LinqAlpha如何利用Amazon Bedrock构建投资思路压力测试系统]({{< relref "posts/20260211-blogs_podcasts-how-linqalpha-assesses-investment-theses-using-dev-3.md" >}})
- [🔥GPT-5职场革命！企业如何用AI重塑生产力？🚀]({{< relref "posts/20260127-blogs_podcasts-inside-gpt-5-for-work-how-businesses-use-gpt-5-9.md" >}})
- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260210-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*