---
title: "Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow I"
date: 2026-02-11T23:34:28+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "西班牙公用事业巨头伊贝德罗拉（Iberdrola）通过与 AWS 合作，利用 Amazon Bedrock AgentCore 在其 ServiceNow 平台上革新了 IT 运营。主要举措包括： 1. **优化变更请求验证**：在起草阶段提升效率； 2. **增强事件管理**：利用上下文智能丰富数据处理； 3. **"
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

Iberdrola 作为全球最大的公用事业公司之一，拥抱尖端人工智能技术，在 ServiceNow 中彻底变革其 IT 运营。通过与 AWS 合作，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种智能体架构，聚焦三个关键领域：优化草稿阶段的变更请求验证、以情境智能丰富事件管理，以及借助对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加快工单解决速度，并在全组织范围内实现一致且高质量的数据处理。

---
## 导语

Iberdrola 作为全球能源领域的领军企业，正通过生成式 AI 重塑其 IT 运营体系。本文深入剖析该公司如何利用 Amazon Bedrock AgentCore 在 ServiceNow 环境中构建智能体架构，从而优化变更请求验证并提升事件管理效率。通过展示这一合作案例，读者将了解对话式 AI 如何消除流程瓶颈，以及如何实现全组织范围内的高质量数据处理。

---
## 摘要

西班牙公用事业巨头伊贝德罗拉（Iberdrola）通过与 AWS 合作，利用 Amazon Bedrock AgentCore 在其 ServiceNow 平台上革新了 IT 运营。主要举措包括：

1. **优化变更请求验证**：在起草阶段提升效率；
2. **增强事件管理**：利用上下文智能丰富数据处理；
3. **简化变更模型选择**：通过对话式 AI 降低操作门槛。

这些创新减少了瓶颈，加速了工单解决，并确保了全组织数据的高质量与一致性。

---
## 评论

**中心观点**
本文的核心观点是：大型公用事业企业可以通过在ServiceNow平台中部署基于Amazon Bedrock的AgentCore智能体架构，实现IT运维从“响应式”向“预测式”的转型，从而在保障安全合规的前提下显著提升运营效率。

**支撑理由与边界条件**

1.  **多智能体架构的协同效应（支撑理由）**
    *   **事实陈述**：Iberdrola并非简单地使用单一聊天机器人，而是构建了针对不同场景的专用Agent架构。
    *   **深度分析**：这种“分而治之”的策略解决了通用大模型在专业领域“幻觉”较多的问题。通过将Agent能力限定在特定流程（如事件管理、变更请求）中，利用ServiceNow的结构化数据作为上下文，有效降低了LLM的不可控性。例如，一个Agent专门负责从日志中提取特征，另一个负责在知识库中检索解决方案，这种模块化设计符合软件工程的高内聚原则。
    *   **作者观点**：这是企业级AI落地最务实的路径，即“大模型+工作流”，而非仅依赖“大模型+提示词”。

2.  **生成式AI与ITSM（IT服务管理）的深度融合（支撑理由）**
    *   **事实陈述**：文章提到利用Amazon Bedrock的模型能力来处理ServiceNow中的工单。
    *   **深度分析**：传统的ITSM自动化（基于RPA或脚本）缺乏灵活性，无法处理非结构化的自然语言描述。引入Bedrock AgentCore后，系统具备了语义理解能力，能够自动分类工单、填充字段甚至起草解决方案。这意味着L1（一级支持）的人力成本将被大幅削减，运维人员可以从重复性劳动中释放出来，专注于复杂问题的解决。

3.  **受控环境下的模型治理（支撑理由）**
    *   **事实陈述**：作为能源巨头，Iberdrola必须在AWS的安全框架内操作。
    *   **深度分析**：文章强调了“安全合规”的背景。在电力行业，IT系统的稳定性直接关系到电网安全。通过使用Bedrock，企业可以利用Guardrails等机制过滤有害信息，并确保数据不离域（如果使用VPC接口）。这回应了行业对公有云大模型最大的顾虑——数据隐私与泄露风险。

**反例/边界条件**

1.  **长尾场景的失效风险（反例）**
    *   **推断**：虽然Agent在处理常见故障（如密码重置、服务器重启）时效率极高，但在面对从未见过的“零日漏洞”或极其复杂的跨系统耦合故障时，基于历史数据训练的Agent可能会给出错误的建议，导致“灾难性遗忘”或盲目自信。
    *   **边界条件**：Agent架构必须设计“人机协同”的熔断机制，当AI的置信度低于阈值时，必须强制转交人工处理，而不能全自动闭环。

2.  **遗留系统的集成摩擦（反例）**
    *   **推断**：ServiceNow通常是现代企业的IT中枢，但Iberdrola作为百年老店，其底层必然存在大量遗留系统。
    *   **边界条件**：如果Agent需要调用的API接口文档缺失，或者老旧系统不支持API调用，Agent的“工具使用”能力将大打折扣。文章未提及如何解决RPA与LLM结合的脏活累活，实际落地中这往往是最大的瓶颈。

**可验证的检查方式**

1.  **MTTR（平均修复时间）对比实验**
    *   **指标**：选取实施AgentCore前后的两组同类IT工单（如服务器宕机、网络延迟），对比其从“开单”到“解决”的平均时长。
    *   **验证点**：观察L1级工单的自动解决率是否显著提升。

2.  **幻觉率与人工介入率监测**
    *   **实验**：在Agent运行初期，设置“影子模式”，即AI给出建议但不自动执行，由人工审核。
    *   **指标**：统计AI建议被人工驳回的比例。如果驳回率超过5%，说明Agent的准确度尚未达到生产级标准。

3.  **Token消耗与ROI分析**
    *   **观察窗口**：运行3个月后，分析Bedrock的API调用成本与节省的人力成本。
    *   **验证点**：验证使用昂贵的Foundation Model（如Claude 3或通过Bedrock调用的其他模型）处理简单IT任务是否经济，是否需要切换到更小型的模型以降低边际成本。

**综合评价**

*   **内容深度**：文章属于典型的“厂商+标杆客户”案例推广，技术细节适中。虽然未公开具体的Prompt Engineering技巧或架构图，但准确抓住了“Agent + Workflow”这一当前企业级AI的核心痛点。
*   **实用价值**：对于同样面临数字化转型的传统企业（如制造、金融、能源）具有极高的参考价值。它展示了一条清晰的路径：不必自研模型，只需利用现有SaaS平台与云厂商的PaaS能力结合。
*   **创新性**：观点不算激进，属于“稳健创新”。它没有追求完全自主的AGI，而是将AI作为现有流程的加速器。
*   **争议点**：文章可能过度美化了实施过程。实际上，将非结构化的运维日志清洗成Agent可理解的数据，往往占据了80%的工作量，而文章对此轻描淡写。

**实际应用建议**
建议IT决策者在效仿此案例时，不要直接追求全量自动化。应先从“知识库检索增强（RAG）”入手，让AI先做运维人员的Cop

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建领域专用的知识库

**说明**: 
Iberdrola 的成功关键在于没有直接使用通用大模型，而是利用 Amazon Bedrock 将其内部特定的 IT 运维文档、历史工单和操作手册转化为向量数据库。通过检索增强生成（RAG）技术，确保 AgentCore 生成的回答基于企业内部的真实数据，而非模型的通用训练数据，从而保证了回答的准确性和合规性。

**实施步骤**:
1. 收集并整理企业内部非结构化数据（如 PDF、Wiki、日志）。
2. 将数据清洗并分块，上传至 Amazon OpenSearch Service 或其他向量存储。
3. 在 Bedrock Agent 配置中，将该知识库定义为主要的“知识源”。

**注意事项**: 
定期更新知识库内容，确保模型不会回答过时信息。

---

### 实践 2：明确代理的角色定位与边界

**说明**: 
在设计 AgentCore 时，Iberdrola 并没有试图创建一个“全能”的 AI，而是将其严格限定在“IT 运营助手”的角色范围内。通过精心设计的系统提示词，明确告知 Agent 它的职责是辅助查询、日志分析和故障排查，并严格禁止其执行未经授权的变更操作。

**实施步骤**:
1. 在 Bedrock Agent 的 Instructions 中清晰定义 Agent 的职责范围。
2. 编写负向约束，明确列出 Agent 不能做的事情（如“不能直接修改生产环境配置”）。
3. 设定特定的对话风格，要求回复必须专业、简洁。

**注意事项**: 
角色定义越清晰，模型产生幻觉或越界操作的风险就越低。

---

### 实践 3：将复杂任务拆解为原子化动作

**说明**: 
为了提高处理效率，Iberdrola 将复杂的 IT 运营流程（如服务器重启、日志查询）拆解为一系列小的、可复用的 API 操作。Bedrock Agent 负责根据用户意图，动态编排这些原子化的 Action Groups，而不是由模型直接生成复杂的代码来执行。

**实施步骤**:
1. 梳理 IT 运维中的高频操作，将其封装为 API 接口（Lambda 函数）。
2. 在 Bedrock 中定义 Action Groups 架构，明确每个 API 的输入参数和返回结构。
3. 配置 Agent 的推理逻辑，使其能够根据用户请求自动选择并调用正确的 API 组合。

**注意事项**: 
API 接口必须具备完善的错误处理机制，以防止单点失败导致整个 Agent 流程中断。

---

### 实践 4：实施严格的人工审核闭环机制

**说明**: 
尽管 AI 可以处理大量请求，Iberdrola 在关键操作上保留了“人机回环”。在 AgentCore 建议执行高风险操作或提供关键解决方案时，系统会要求人工运维专家进行确认。这不仅确保了安全性，还利用人工反馈数据不断微调模型的表现。

**实施步骤**:
1. 识别高风险操作类别（如删除数据、重启核心服务）。
2. 在工作流中配置确认节点，当 Agent 触发此类操作时，暂停并通知人工审核。
3. 建立反馈渠道，允许人工专家对 Agent 的建议进行评分或修正。

**注意事项**: 
审核机制不应过于繁琐，以免影响低风险任务的自动化效率。

---

### 实践 5：利用 Guardrails 建立安全护栏

**说明**: 
为了防止模型输出有害信息或敏感数据泄露，Iberdrola 利用 Amazon Bedrock 的 Guardrails 功能。这层安全网可以实时过滤掉不当的词汇、阻止提示词注入攻击，并屏蔽特定的敏感实体信息（如内部密钥或个人身份信息 PII）。

**实施步骤**:
1. 配置 Bedrock Guardrails，定义敏感词过滤规则。
2. 设置 PII（个人身份信息）屏蔽策略，防止 Agent 在对话中泄露员工或客户隐私。
3. 开启上下文-grounding 检查，强制 Agent 的回答必须基于检索到的上下文，拒绝“胡编乱造”。

**注意事项**: 
安全策略需要随着业务变化和合规要求动态调整。

---

### 实践 6：建立基于 Trace 的可观测性体系

**说明**: 
在 IT 运维中，可解释性至关重要。Iberdrola 利用 Amazon Bedrock 的 CloudWatch 集成功能，对 AgentCore 的每一次调用进行全链路追踪。这允许运维团队清楚地看到 Agent 是如何理解意图、检索了哪些文档、调用了哪个 API 以及最终是如何生成答案的。

**实施步骤**:
1. 启用 Bedrock 的模型调用日志记录，并将其关联到 CloudWatch Logs。
2. 创建自定义仪表盘，监控 Agent 的响应延迟、调用成功率和检索准确率。
3. 定期分析 Trace 数据，定位 Agent 在哪些场景下出现了推理偏差。

**注意事项**: 
日志存储需符合企业数据保留策略，并注意日志中可能包含的敏感信息需脱敏处理。

---
## 学习要点

- Iberdrola 利用 Amazon Bedrock 和 AgentCore 构建生成式 AI 智能体，成功将 IT 运维中的重复性任务自动化，显著提升了运营效率。
- 通过检索增强生成（RAG）技术整合企业内部知识库，该方案确保了技术故障排查的准确性和响应速度，同时有效降低了幻觉风险。
- 采用“人机协同”的工作流设计，在保持 AI 全天候服务能力的同时，引入人工审核机制以确保关键操作的安全性与合规性。
- 借助无代码/低代码平台，业务专家能够直接参与智能体的开发与迭代，大幅降低了技术门槛并加快了创新步伐。
- 该架构具备高度的通用性与可扩展性，不仅适用于 IT 部门，未来还能轻松复制到人力资源、客户服务及法务等其他业务领域。
- 通过将传统 IT 支持模式转变为主动式、对话式的交互体验，该方案显著改善了员工体验并释放了技术团队的人力资源。

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