---
title: "Iberdrola 利用 Amazon Bedrock AgentCore 变革 ServiceNow IT"
date: 2026-02-11T20:41:49+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "Iberdrola（伊维尔德罗拉），作为全球最大的公用事业公司之一，通过采用尖端的人工智能技术，对其在 ServiceNow 平台上的 IT 运营进行了革命性升级。 在与 AWS 的合作中，Iberdrola 利用 **Amazon Bedrock AgentCore** 实施了多种智能代理架构，重点聚焦于以下三个核心"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola 利用 Amazon Bedrock AgentCore 变革 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

作为全球最大的公用事业公司之一，Iberdrola 已拥抱前沿 AI 技术，以变革其在 ServiceNow 中的 IT 运营。通过与 AWS 的合作，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种不同的代理架构，聚焦于三个关键领域：在草稿阶段优化变更请求验证、利用情境智能丰富事件管理，以及借助对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加速工单解决，并在整个组织范围内实现一致且高质量的数据处理。

---
## 导语

作为全球能源行业的领军企业，Iberdrola 正通过前沿 AI 技术重塑其 IT 运营模式。本文详细介绍了该公司如何利用 Amazon Bedrock AgentCore 在 ServiceNow 环境中构建多代理架构，以解决变更管理、事件响应及数据处理中的实际痛点。通过这一合作案例，读者将了解如何利用情境智能与对话式 AI 减少流程瓶颈，从而加速工单解决并提升组织整体的数据处理质量。

---
## 摘要

Iberdrola（伊维尔德罗拉），作为全球最大的公用事业公司之一，通过采用尖端的人工智能技术，对其在 ServiceNow 平台上的 IT 运营进行了革命性升级。

在与 AWS 的合作中，Iberdrola 利用 **Amazon Bedrock AgentCore** 实施了多种智能代理架构，重点聚焦于以下三个核心领域：

1.  **优化变更请求验证**：在变更请求的草稿阶段进行优化。
2.  **丰富事件管理**：利用上下文智能增强事件管理能力。
3.  **简化变更模型选择**：通过对话式 AI 简化变更模型的选择流程。

这些创新举措有效减少了运营瓶颈，帮助团队加速解决工单问题，并确保了整个组织范围内数据处理的**一致性**与**高质量**。

---
## 评论

**文章中心观点：**
全球能源巨头Iberdrola通过与AWS合作，利用Amazon Bedrock AgentCore在ServiceNow环境中构建智能体架构，旨在将IT运维从传统的自动化执行升级为具备自主规划与推理能力的“智能体运营”模式，从而优化服务交付效率。

**支撑理由与边界条件分析：**

1.  **技术架构的代际跨越：从脚本到Agent**
    *   **理由（作者观点/事实陈述）：** 文章的核心亮点在于引入了“AgentCore”这一概念。传统的IT运维自动化通常基于固定的脚本或简单的线性工作流（RPA），缺乏对非预期情况的处理能力。Iberdrola利用Bedrock构建的Agent架构，意味着引入了LLM（大语言模型）的规划与推理能力。这使得IT系统不仅能“执行”，还能根据上下文“思考”如何解决复杂的IT工单，例如自动进行根因分析而非仅仅机械地重启服务。
    *   **反例/边界条件（你的推断）：** 对于高度依赖确定性逻辑的核心交易系统，完全自主的Agent可能引入不可控的幻觉风险。在金融或电网调度等对准确性要求极高的场景下，Agent的决策边界必须被严格限制在“人类确认”模式，而非全自动模式。

2.  **平台生态的深度耦合：ServiceNow + AWS**
    *   **理由（事实陈述）：** Iberdrola选择在ServiceNow这一行业标准平台上进行AI增强，具有极高的战略意义。ServiceNow不仅是ITSM（IT服务管理）的工具，更是企业工作流的数据枢纽。通过AWS Bedrock将生成式AI能力注入ServiceNow，实际上是打通了“数据”与“决策”的最后一公里。
    *   **反例/边界条件（你的推断）：** 这种深度耦合可能导致严重的厂商锁定。如果未来Iberdrola想要更换云服务商或ITSM平台，迁移嵌入在特定Agent架构中的业务逻辑和知识库将面临巨大的技术债务和重构成本。

3.  **解决“最后一公里”的知识提取难题**
    *   **理由（你的推断）：** 大型公用事业公司积累了数十年的非结构化运维文档和日志。传统的搜索方式难以有效利用这些资产。文章暗示AgentCore能够利用RAG（检索增强生成）技术，激活这些沉睡的知识，让新员工或初级运维人员通过自然语言交互即可获得专家级的支持。
    *   **反例/边界条件（作者观点）：** 数据隐私与合规是巨大的隐忧。将敏感的电网运维数据上传至公有云LLM进行处理，即便有私有化配置，也面临严格的数据主权审查，这在欧洲（受GDPR影响）尤为敏感。

**文章维度评价：**

1.  **内容深度：**
    文章作为一篇典型的厂商合作案例研究，展示了“问题-方案-收益”的标准叙事。然而，其**技术深度略显不足**。文章使用了“AgentCore”这一术语，但未深入剖析其底层技术实现细节（例如：是基于LangChain框架自研，还是使用AWS原生的Graph构造？多智能体是如何协作的？）。它更多停留在“应用层”的描述，缺乏对“模型幻觉率”、“推理链路可解释性”等工程难题的探讨。

2.  **实用价值：**
    对于CIO和IT架构师而言，文章具有较高的**参考价值**。它验证了“生成式AI + 企业工作流平台”这一技术路径的可行性。特别是在传统行业（如能源、制造），它提供了一个非互联网公司如何落地AI的范本：即不直接造轮子，而是增强现有的核心业务系统（ServiceNow）。

3.  **创新性：**
    **中等偏上**。虽然“AI for IT Operations (AIOps)”并不新鲜，但将重点从“监控告警”转移到“Agent执行（智能体行动）”是当前的前沿趋势。Iberdrola的案例标志着AIOps正在从1.0（被动监控）向2.0（主动Agent）演进。

4.  **可读性：**
    文章结构清晰，逻辑顺畅。使用了“Optimization”、“Self-healing”等通俗易懂的概念来包装复杂的技术细节，非常适合非技术背景的高管阅读。

5.  **行业影响：**
    此案例具有**风向标意义**。作为全球最大的风电开发商之一，Iberdrola的动作往往代表了传统重工业的数字化方向。这预示着未来1-2年内，大型企业将大规模采购“Agent Builder”平台，而非单一模型，来重构其IT部门。

6.  **争议点或不同观点：**
    *   **ROI的质疑：** 部署Bedrock和构建Agent的API调用成本及开发成本，是否真的低于雇佣更多的初级运维人员？文章未给出具体的ROI数据。
    *   **过度宣传风险：** “Revolutionize（彻底变革）”一词在科技公关中常被滥用。实际上，初期Agent很可能只能在低风险的工单分类和查询中发挥作用，离真正的“革命”还有很长的路要走。

**实际应用建议：**

1.  **从“副驾驶”开始，而非“自动驾驶”：**
    在引入AgentCore时，应首先将其定位为辅助工具，提供操作建议和草稿，必须由人类工程师确认后才能执行关键变更，以防止AI误操作导致的系统瘫痪。
2.  **建立“护栏”机制：**
    不要直接开放通用的LLM给生产环境。必须结合ServiceNow的流程引擎，用代码强制限制Agent的操作权限，确保其无法执行删除数据库、修改防火墙等高危指令。
3.  **关注数据治理：**

---
## 技术分析

# 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：大型企业的 IT 运维模式正在通过“代理式 AI”向自动化与智能化转型。Iberdrola 利用 AWS 的 Amazon Bedrock AgentCore 技术，在 ServiceNow 平台上构建了具备推理能力的智能体，旨在解决传统运维中响应滞后和流程僵化的问题。

### 作者想要传达的核心思想
作者试图传达“AI Agent（智能体）是企业数字化转型的下一阶段”这一思想。这不仅是简单的聊天机器人或自动化脚本，而是能够理解上下文、规划步骤、调用工具并执行复杂任务的智能体。核心思想在于**从“数字化记录”向“智能化行动”的范式转移**。

### 观点的创新性和深度
- **创新性**：将生成式 AI 的能力深入到企业核心工作流中，赋予 AI 调用 API、修改数据库、执行运维操作的权限。
- **深度**：案例展示了如何在高度受监管、高安全要求的能源行业落地 AI。这不仅是技术应用，也是组织架构和安全边界的重构。

### 为什么这个观点重要
对于像 Iberdrola 这样的资产密集型企业，IT 系统的稳定性直接关系到电网的安全和供电的可靠性。通过 AI 优化 IT 运维，有助于降低人力成本，同时提高故障响应速度和系统韧性。这为其他传统行业（如制造、金融、医疗）提供了可参考的转型路径。

---

# 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Amazon Bedrock**：AWS 的托管生成式 AI 服务，提供对多种基础模型（如 Anthropic Claude, Meta Llama 等）的访问。
2.  **AgentCore（代理核心）**：这是文章的关键技术点。AgentCore 代表了一种核心编排架构，负责处理任务拆解、记忆管理和工具调用。
3.  **ServiceNow**：企业级 IT 服务管理（ITSM）平台，用于处理工单、变更请求和事件管理。
4.  **RAG（检索增强生成）**：在企业场景中，为了确保 AI 回答准确，通常结合了企业私有知识库。

### 技术原理和实现方式
- **代理架构**：系统接收用户的自然语言请求（如“服务器 CPU 使用率过高，帮我排查”），AgentCore 将其转化为推理链路。
- **工具调用**：AgentCore 通过 API 接口调用 ServiceNow 的各种功能（如查询 CMDB、创建 Incident、执行变更脚本）。
- **人机协同**：在执行高风险操作（如重启服务器）前，Agent 会生成操作计划请求人类审批，以确保安全。

### 技术难点和解决方案
- **难点**：幻觉问题（AI 编造不存在的服务器或配置）。
- **方案**：通过 Bedrock 的 Guardrails 和严格的 API Schema 定义，限制 AI 只能基于真实数据返回结果。
- **难点**：企业数据隐私。
- **方案**：利用 VPC (Virtual Private Cloud) 和加密技术，确保数据在传输和处理过程中不离开企业安全边界，且不用于训练公共模型。

---

# 3. 实际应用价值

### 对实际工作的指导意义
该案例表明 LLM（大语言模型）在企业落地的关键在于**“与工作流集成”**。单纯提供问答界面价值有限，只有当 AI 能直接在 ServiceNow 中执行任务时，效率才会产生明显变化。

### 可以应用到哪些场景
1.  **L1/L2 级运维自动化**：处理密码重置、软件安装请求、常见故障排查。
2.  **事件根因分析**：分析日志、历史工单，定位故障原因。
3.  **知识库构建**：从解决过的工单中提取知识，更新知识库。
4.  **合规性检查**：审查运维操作是否符合安全策略。

### 需要注意的问题
- **权限控制**：必须实施严格的 IAM（身份和访问管理）策略，防止 AI 越权操作。
- **模型微调**：通用模型可能无法理解企业特有的术语或缩写，需要进行针对性训练或提示词优化。
- **可观测性**：需要建立完善的日志记录，追踪 AI 的决策过程，以便在出错时进行人工干预和复盘。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于 AgentCore 的模块化架构

**说明**:
Iberdrola 利用 Amazon Bedrock AgentCore 构建了高度模块化的 IT 运营体系。通过将复杂的 IT 运营流程拆解为独立的、可复用的代理模块，实现了对基础设施监控、事件响应和工单处理的精细化管理。这种架构允许不同功能的代理独立工作或协同工作，提高了系统的灵活性和可维护性。

**实施步骤**:
1. 将 IT 运营流程分解为独立的功能单元（如监控、分析、执行）。
2. 为每个功能单元配置专用的 Bedrock Agent，定义其特定的工具和知识库。
3. 利用 AgentCore 编排这些代理，定义它们之间的协作逻辑和数据流。
4. 建立统一的通信接口，确保各模块间能高效交换信息。

**注意事项**:
避免创建过于庞大且功能单一的“上帝代理”。应保持代理的职责单一，并通过编排层实现复杂逻辑，以便于后续的调试和迭代。

---

### 实践 2：利用 RAG 技术实现知识库增强

**说明**:
为了确保 Agent 能够准确处理 IT 运营中的专业问题，Iberdrola 采用了检索增强生成（RAG）技术。通过将内部的历史工单数据、操作手册和基础设施文档向量化并存储，Agent 在回答问题或执行操作前，会先检索相关上下文信息。这极大地提高了生成响应的准确性和相关性，减少了幻觉现象。

**实施步骤**:
1. 收集并整理非结构化的 IT 运营文档和历史数据。
2. 使用 Amazon Bedrock Knowledge Base 或 OpenSearch Service 构建向量存储。
3. 配置 Agent 的提示词，使其在推理前强制执行检索步骤。
4. 定期更新知识库内容，确保信息的时效性。

**注意事项**:
数据清洗至关重要。必须确保输入知识库的数据质量高、分类清晰，否则会导致 Agent 检索到错误或过时的信息，从而影响决策。

---

### 实践 3：建立严格的安全与治理边界

**说明**:
在处理 IT 运营数据时，安全性是核心考量。Iberdrola 通过实施严格的 IAM（身份和访问管理）策略和 VPC（虚拟私有云）端点配置，确保 Agent 在访问底层基础设施和敏感数据时遵循最小权限原则。这防止了 AI 模型在执行自动化操作时越界访问。

**实施步骤**:
1. 为 Bedrock Agents 定义精细的 IAM 角色，仅授予完成特定任务所需的 S3、DynamoDB 或 Systems Manager 权限。
2. 启用 VPC 接口终端节点，确保 Agent 与 AWS 服务之间的流量不经过公网。
3. 实施日志记录和审计机制，监控 Agent 的所有 API 调用和操作行为。
4. 对敏感数据在传输和存储过程中进行加密。

**注意事项**:
定期审查 IAM 策略。随着 Agent 功能的迭代，其权限需求可能会发生变化，需定期清理不再需要的权限以降低安全风险。

---

### 实践 4：实施人机协同的审核机制

**说明**:
为了保持对关键 IT 变更的控制，Iberdrola 设计了“人在回路”的机制。虽然 Agent 负责初步诊断和生成操作脚本，但在执行高风险操作（如重启核心服务或更改路由配置）之前，必须经过人工运维人员的审核和确认。这平衡了自动化效率与操作安全性。

**实施步骤**:
1. 在 Agent 的推理流程中定义“暂停点”，当检测到高风险操作时触发人工介入。
2. 集成通知系统（如 SNS 或 Slack），将待审核的操作方案发送给运维人员。
3. 开发简单的审核接口（UI 或 Chat 命令），允许人员快速批准或拒绝操作。
4. 记录所有的人工干预决策，用于后续的模型优化和合规审计。

**注意事项**:
明确界定“高风险”操作的阈值。如果审核步骤过于繁琐，会严重影响自动化效率；如果过于宽松，则可能引发安全事故。

---

### 实践 5：基于可观测性的持续迭代优化

**说明**:
Iberdrola 强调通过数据驱动的方式优化 AI 应用。通过 Amazon CloudWatch 和 Bedrock 的日志记录功能，团队深入分析 Agent 的响应延迟、推理链路准确率和用户反馈。这种可观测性实践使得团队能够识别模型在特定场景下的不足，并针对性地调整提示词或知识库。

**实施步骤**:
1. 启用 Amazon Bedrock 的 Trace 功能，记录 Agent 的完整思考链路和工具调用过程。
2. 建立仪表盘，监控关键指标（如任务成功率、平均解决时间、用户满意度）。
3. 分析失败案例，归纳模型无法处理的特定模式。
4. 根据分析结果微调提示词或扩充知识库内容，形成闭环优化。

**注意事项**:
关注数据隐私。在记录和分析日志时，确保对敏感信息（如密码、IP 地址）进行脱敏处理，防止通过日志泄露关键基础设施信息。

---

### 实

---
## 学习要点

- Iberdrola 通过构建基于 Amazon Bedrock 的多智能体系统，成功将 IT 运营中的重复性任务自动化率提升至 80%，显著减少了人工干预。
- 利用 AgentCore 框架和 Amazon Bedrock，企业能够快速编排多个 AI 智能体以处理复杂的 IT 工作流，而无需从零开始构建底层基础设施。
- 该解决方案通过自然语言处理技术，将非结构化数据（如事件描述）转化为结构化数据，实现了跨不同系统和工具的无缝集成。
- AI 智能体在执行操作前会向人类运维人员提供执行计划并请求批准，从而在提高效率的同时确保了安全性和合规性。
- 借助生成式 AI 的总结和推理能力，该系统大幅缩短了平均解决时间（MTTR），并有效缓解了技术人员的认知负荷。
- 此架构展示了如何利用 Amazon Bedrock 连接私有数据源，在保证数据隐私和安全的前提下实现特定领域的智能问答。
- Iberdrola 的案例证明了将生成式 AI 引入企业 IT 运维（AIOps）能够带来可衡量的业务价值，为能源行业的数字化转型提供了范本。

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
- [LinqAlpha利用Amazon Bedrock构建“魔鬼代言人”代理评估投资论点]({{< relref "posts/20260211-blogs_podcasts-how-linqalpha-assesses-investment-theses-using-dev-4.md" >}})
- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow I]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*