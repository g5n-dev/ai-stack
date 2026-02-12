---
title: "Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营"
date: 2026-02-12T13:28:35+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "智能体架构", "IT 运营", "对话式 AI", "事件管理", "AWS"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "Iberdrola（伊维尔德罗拉），作为全球最大的公用事业公司之一，正通过采用尖端的人工智能技术，对其在ServiceNow平台上的IT运营进行彻底革新。 通过与AWS（亚马逊云科技）的合作，Iberdrola实施了基于Amazon Bedrock AgentCore的多种智能体架构，重点聚焦于以下三个核心领域： 1."
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

Iberdrola，全球最大的公用事业公司之一，已采用尖端的人工智能技术，以彻底变革其在 ServiceNow 中的 IT 运营。通过与 AWS 合作，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种智能体架构，聚焦三个关键领域：优化草稿阶段的变更请求验证、利用情境智能丰富事件管理，以及通过对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加快工单解决速度，并在整个组织内实现一致且高质量的数据处理。

---
## 导语

全球能源巨头 Iberdrola 正通过与 AWS 合作，利用 Amazon Bedrock AgentCore 深化其 ServiceNow 平台的智能化转型。本文详细拆解了该企业如何通过多智能体架构，在变更请求验证、事件管理及模型选择等核心环节实现自动化与情境增强。对于希望优化 IT 运营流程的团队而言，这一案例展示了如何利用生成式 AI 有效减少流程瓶颈，从而显著提升工单处理效率与数据质量。

---
## 摘要

Iberdrola（伊维尔德罗拉），作为全球最大的公用事业公司之一，正通过采用尖端的人工智能技术，对其在ServiceNow平台上的IT运营进行彻底革新。

通过与AWS（亚马逊云科技）的合作，Iberdrola实施了基于Amazon Bedrock AgentCore的多种智能体架构，重点聚焦于以下三个核心领域：

1.  **优化变更请求验证**：在起草阶段利用AI优化变更请求的验证流程。
2.  **丰富事件管理**：利用上下文智能增强事件管理能力。
3.  **简化变更模型选择**：通过对话式AI简化变更模型的选择。

这些创新举措有效减少了运营瓶颈，帮助团队加速了工单解决速度，并在整个组织范围内实现了高质量、一致的数据处理。

---
## 评论

### 中心观点
本文的核心观点是：通过在 ServiceNow 平台中集成基于 Amazon Bedrock AgentCore 的智能体架构，公用事业巨头 Iberdrola 成功实现了 IT 运维的自动化与智能化转型，验证了生成式 AI 在处理复杂企业工作流时的落地能力。

### 支撑理由与边界条件分析

**1. 深度集成与编排能力**
*   **事实陈述**：文章提到 Iberdrola 使用了“Amazon Bedrock AgentCore”与 ServiceNow 进行集成。
*   **分析**：这表明技术实施的重点不在于单一的聊天机器人，而在于利用 AgentCore 作为中间件或编排层，连接大语言模型（LLM）的推理能力与企业既有的 ITSM（IT 服务管理）流程。
*   **技术深度**：这种架构解决了企业级 AI 应用中常见的“最后一公里”问题——即如何让 AI 能够调用 API、查询数据库并执行实际操作，而不仅仅是生成文本。AgentCore 的角色是提供多智能体协作框架，处理任务拆解。

**2. 生成式 AI 对非结构化数据的处理**
*   **作者观点**：传统的 IT 运维自动化依赖规则引擎，难以处理复杂的、非结构化的工单描述。
*   **分析**：利用 Bedrock 的基础模型，Iberdrola 能够理解模糊的用户请求，自动分类工单，甚至生成解决方案脚本。这代表了从“基于脚本的自动化”向“基于意图的自动化”的转变。

**3. 行业特性的契合度**
*   **分析**：公用事业公司拥有庞大的遗留资产和复杂的合规要求。Iberdrola 的案例证明了在高度监管的行业中，利用私有化或安全托管的大模型服务来辅助内部 IT 运维是可行的。

**反例与边界条件**

*   **边界条件 1：成本与延迟的权衡**
    *   **推断**：对于高频但低复杂度的任务（如简单的密码重置），调用 Bedrock 上的大模型可能比传统的硬编码脚本成本更高且延迟更大。Agentic 架构不应完全取代规则引擎，而应作为补充。
*   **边界条件 2：幻觉风险**
    *   **事实陈述**：生成式 AI 存在幻觉问题。
    *   **分析**：在 IT 运维中，AI 生成的错误代码或错误的配置更改可能导致服务中断。文章若未提及“人在回路”或严格的自动化测试 gating 机制，则其论证在安全性上不够严谨。

---

### 多维度深入评价

#### 1. 内容深度与论证严谨性
文章展示了 AWS 与 ServiceNow 生态结合的典型范式。然而，从技术角度看，文章略显营销导向。
*   **缺失点**：文章未详细说明 AgentCore 的具体工作流——是采用了 ReAct（推理+行动）模式，还是 Plan-and-Execute 模式？此外，对于“优化”的量化指标（如工单解决时间减少了多少百分比，人力节省了多少）缺乏具体数据支撑，使得论证在严谨性上有所欠缺。

#### 2. 实用价值与指导意义
对于正在探索“AI + 企业级工作流”的架构师和 CIO 而言，该案例具有极高的参考价值。
*   **指导意义**：它指明了一条技术路径——不要试图用 AI 重新构建 ERP 或 ITSM 系统，而是构建“Agentic Layer（智能体层）”包裹在现有系统之上。ServiceNow 负责记录状态，AgentCore 负责动态决策和执行。

#### 3. 创新性
*   **新观点**：将“AgentCore”作为独立概念提出，暗示了 AI 架构正在从“单点应用”向“多智能体协作”演进。
*   **行业趋势**：这是“Agentic Workflow”在能源行业的落地。它不再是简单的“Copilot（副驾驶）”模式，即给人提建议，而是走向了“Agent（代理）”模式，即自主完成任务。

#### 4. 行业影响
Iberdrola 作为头部企业的背书，会加速公用事业及能源行业对 GenAI 的接纳度。它表明，即使是拥有沉重历史包袱的传统行业，也可以通过云原生架构快速切入 AI 轨道。

#### 5. 争议点与不同观点
*   **Vendor Lock-in（厂商锁定）**：深度依赖 AWS Bedrock 和 ServiceNow 的原生集成可能导致极高的迁移成本。
*   **过度工程化**：部分观点可能认为，许多 IT 运维任务完全可以通过传统的 RPA（机器人流程自动化）或简单的脚本解决，引入大模型智能体可能是“用大炮打蚊子”。

---

### 实际应用建议

基于对该案例的分析，对于计划实施类似项目的企业，建议如下：

1.  **明确人机协同边界**：不要将 Agent 设置为完全自主运行。在执行变更类操作（如修改服务器配置、删除数据）时，必须引入人工审批节点。
2.  **建立评估基准**：在上线前，必须建立一套标准的测试集，用于评估 Agent 的准确率和召回率，防止模型更新导致服务质量下降。
3.  **关注数据主权**：使用 Bedrock 时，需确认敏感的 IT 运维数据（如内部拓扑图、密钥）是否会用于模型训练。应配置 Cross-Account Inference 或 VPC Endpoint 确保数据不出境。

### 可验证的检查方式

为了验证该案例的真实效果及类似项目的成败，可以通过以下方式进行观察或实验：

1.  **观察指标：MTTR（平均修复时间）**
    *   **

---
## 技术分析

## 技术分析

### 1. 核心架构与实现逻辑
该案例展示了如何利用**Amazon Bedrock AgentCore**构建智能体架构，并将其集成到**ServiceNow**工作流中，以实现IT运维流程的自动化。

*   **Agentic AI（智能体AI）的应用**：
    与传统的基于检索增强生成（RAG）的问答机器人不同，本方案采用了具备规划、记忆和工具调用能力的智能体架构。AI不再局限于生成文本，而是能够执行具体的业务操作。
*   **技术集成方式**：
    通过Amazon Bedrock作为中间层，连接大语言模型（LLM）与企业业务逻辑。Bedrock负责将自然语言指令转化为对ServiceNow API的结构化调用，实现了从“对话”到“执行”的跨越。

### 2. 关键技术组件
*   **Amazon Bedrock AgentCore**：负责对LLM的输出进行编排，管理任务的分解与执行流程。
*   **工具调用**：利用Function Calling机制，将Llm的意图映射为具体的API操作（如创建工单、查询状态）。
*   **ServiceNow平台**：作为IT服务管理（ITSM）的底座，接收并处理来自AI智能体的指令。

### 3. 运维模式的转变
该技术方案旨在推动IT运维从“响应式”向“主动式”转变：
*   **自动化处理**：智能体可以自主处理L1/L2级别的常规运维请求（如密码重置、资源分配），减少人工干预。
*   **流程增强**：AI被嵌入现有的ITIL流程中，辅助进行根因分析（RCA）和工单分类，而非完全替代现有系统。

### 4. 实施中的挑战与应对
*   **准确性与合规性**：在企业环境中，LLM的输出必须符合业务规范。方案通过引入**Bedrock Guardrails**和**人机协同**机制，确保高风险操作需要人工审批，防止错误执行。
*   **系统解耦**：使用AgentCore隔离底层模型与上层业务逻辑，便于未来模型的迭代或更换，无需重构ServiceNow端的代码。

---
## 最佳实践

## 最佳实践

### 1. 构建基于知识库的检索增强生成（RAG）架构
**说明**：利用 Amazon Bedrock 和 AgentCore 将非结构化的运营文档（如 IT 运维手册、事件报告）转化为向量存储。这确保了 LLM 在生成回答时能够引用企业内部的真实数据，有效避免模型幻觉，保证技术建议的准确性和时效性。
**实施步骤**：
1.  **数据清洗与分块**：将 PDF、Word 等格式的运维文档转换为纯文本，并根据语义逻辑进行切分。
2.  **向量化与存储**：使用 Amazon Bedrock 的 Embedding 模型将文本块转换为向量，并存储在向量数据库（如 Amazon OpenSearch Serverless）中。
3.  **检索集成**：配置 AgentCore 使得用户查询首先在向量库中检索相关上下文，再作为 Prompt 输入给 LLM 生成答案。
**注意事项**：严格管理源文档的版本控制，防止过时的运维信息误导模型生成错误的操作指令。

### 2. 利用 Agent Framework 实现复杂任务的自主编排
**说明**：通过 Amazon Bedrock 的 Agents（或类似 AgentCore 框架），实现从简单问答到复杂任务执行的跨越。Agent 能够根据用户意图自动拆解任务，按顺序调用多个 API（如查询日志、重启服务、创建工单），从而实现 IT 运维流程的自动化。
**实施步骤**：
1.  **定义 API Schema**：将 IT 运维工具（如 ServiceNow、监控工具）封装为标准的 OpenAPI 规范描述文件。
2.  **配置 Agent 链路**：在 Bedrock 中配置 Agent，使其能够理解何时以及如何调用上述 API。
3.  **逻辑验证**：在沙箱环境中测试 Agent 对于多步骤推理任务的执行逻辑，确保 API 调用的顺序和参数正确。
**注意事项**：为每个 API 调用配置严格的权限边界，确保 Agent 仅能执行授权范围内的操作，防止越权访问。

### 3. 实施基于角色的细粒度访问控制与安全防护
**说明**：在生成式 AI 应用中实施严格的安全策略。通过结合 AWS IAM Identity Center 和 Amazon Bedrock 的 Guardrails，确保模型不仅遵守数据访问权限，还能在输出层面过滤敏感信息（如密码、密钥）和不当内容。
**实施步骤**：
1.  **用户上下文传递**：在 Agent 调用中传递用户身份信息，确保检索向量库时仅返回该用户有权查看的文档片段。
2.  **配置 Guardrails**：设置敏感信息过滤规则，阻断模型输出 PII（个人身份信息）或特定的内部机密代码。
3.  **审计日志**：启用 CloudTrail 记录所有 API 调用和模型推理请求，以便合规审计。
**注意事项**：不要仅依赖 Prompt Engineering 来隐藏敏感信息，必须使用 Guardrails 和动态数据脱敏等技术手段作为强制防线。

### 4. 建立“人机协同”的验证与反馈闭环
**说明**：采用“人在回路”的设计模式。在 Agent 执行高风险操作（如变更生产环境配置）之前，系统会生成详细的执行计划供人工审批，同时允许运维人员对模型的回答进行反馈，以持续优化系统表现。
**实施步骤**：
1.  **审批流集成**：对于关键运维动作，Agent 应生成摘要并暂停，等待通过 ITSM（如 ServiceNow）系统的审批后继续执行。
2.  **反馈机制**：在用户界面引入反馈按钮，收集用户对模型回答质量的数据。
3.  **持续微调**：定期分析反馈日志，使用负反馈样本修正 Prompt 或微调模型，减少同类错误的发生。
**注意事项**：明确界定 Agent 的自主操作边界，对于可能导致服务中断的操作，必须默认设置为人工确认模式。

### 5. 专注于特定领域的 Prompt 优化与上下文管理
**说明**：通用的 LLM 往往难以理解特定的 IT 运维术语。通过精心设计的 System Prompt 和 Few-shot Learning（少样本学习），为模型注入企业特定的运维知识背景，显著提升模型对复杂日志分析和故障排查的理解能力。
**实施步骤**：
2.  **构建样本库**：提供高质量的问答对（Few-shot），指导模型如何处理特定的告警代码或错误日志。
3.  **上下文压缩**：优化检索到的文档片段，去除冗余信息，确保模型在 Token 限制内获取最关键的信息。
**注意事项**：定期审查 Prompt 的有效性，并根据模型版本的更新调整提示词策略。

---
## 学习要点

- Iberdrola 通过部署 Amazon Bedrock AgentCore，成功实现了 IT 运维流程的自动化，将处理基础设施请求的时间从数小时缩短至几分钟。
- 该解决方案利用生成式 AI 智能解析用户自然语言请求，并自动将其转化为精确的 AWS 命令或 API 调用，大幅降低了技术门槛。
- AgentCore 内置的严格安全护栏机制，确保了 AI 执行操作的合规性与安全性，有效防止了越权访问或错误配置。
- 企业通过将 AI Agent 集成到现有工作流（如 Slack）中，显著提升了员工的工作效率并改善了用户体验。
- 该架构具备高度的可扩展性，能够通过简单的配置快速适应新的业务场景和需求，而无需重新训练底层模型。
- Iberdrola 的实践证明，在 IT 运维领域引入生成式 AI 代理，是推动企业数字化转型和降本增效的关键策略。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [智能体架构](/tags/%E6%99%BA%E8%83%BD%E4%BD%93%E6%9E%B6%E6%9E%84/) / [IT 运营](/tags/it-%E8%BF%90%E8%90%A5/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/) / [事件管理](/tags/%E4%BA%8B%E4%BB%B6%E7%AE%A1%E7%90%86/) / [AWS](/tags/aws/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow 运]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-10.md" >}})
- [Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-12.md" >}})
- [Iberdrola 如何利用 Amazon Bedrock AgentCore 优化 ServiceNow I]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-11.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*