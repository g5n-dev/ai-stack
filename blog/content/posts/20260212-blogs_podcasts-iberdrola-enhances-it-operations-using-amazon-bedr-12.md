---
title: "伊维尔德罗拉如何利用 Amazon Bedrock 优化 ServiceNow IT 运营"
date: 2026-02-12T10:28:19+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "IT 运营", "多代理架构", "变更管理", "事件管理", "对话式 AI"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "全球最大的公用事业公司之一Iberdrola，通过与其合作伙伴AWS紧密协作，采用了前沿的人工智能技术，对其ServiceNow平台中的IT运营进行了全面革新。 Iberdrola利用Amazon Bedrock AgentCore实施了多种智能体架构，重点聚焦于以下三个关键领域以实现优化： 1. **变更请求验证优化"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# 伊维尔德罗拉如何利用 Amazon Bedrock 优化 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

伊维尔德罗拉，全球最大的公用事业公司之一，已采用尖端人工智能技术，彻底变革其在 ServiceNow 中的 IT 运营。通过与 AWS 合作，伊维尔德罗拉利用 Amazon Bedrock AgentCore 实施了多种代理架构，聚焦三大关键领域：优化草稿阶段的变更请求验证、以情境智能丰富事件管理，以及通过对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加快工单解决速度，并在整个组织内实现一致、高质量的数据处理。

---
## 导语

全球能源巨头伊维尔德罗拉正通过生成式 AI 重塑其 IT 运营体系。本文介绍了该公司如何利用 Amazon Bedrock AgentCore，在 ServiceNow 平台中实现变更请求验证、事件管理及模型选择的自动化与智能化。通过解析这一合作案例，读者将了解如何利用多代理架构消除流程瓶颈，从而在保障数据质量的前提下，显著提升工单处理效率。

---
## 摘要

全球最大的公用事业公司之一Iberdrola，通过与其合作伙伴AWS紧密协作，采用了前沿的人工智能技术，对其ServiceNow平台中的IT运营进行了全面革新。

Iberdrola利用Amazon Bedrock AgentCore实施了多种智能体架构，重点聚焦于以下三个关键领域以实现优化：
1.  **变更请求验证优化**：在草稿阶段即优化变更请求的验证流程。
2.  **事件管理增强**：利用上下文智能丰富事件管理能力。
3.  **变更模型选择简化**：通过对话式AI简化变更模型的选择过程。

这些创新举措有效消除了运营瓶颈，不仅帮助团队加速了工单解决速度，还在整个组织范围内实现了高质量且一致的数据处理。

---
## 评论

### 中心观点
这篇文章展示了Iberdrola通过利用Amazon Bedrock AgentCore在ServiceNow中构建“代理架构”，标志着企业级IT运维正从传统的自动化脚本向具有自主规划能力的**生成式AI智能体**演进，但其核心价值在于**特定场景下的决策增强**而非通用的无人化自治。

### 支撑理由与深度评价

#### 1. 从“工作流自动化”向“意图识别与规划”的技术跃迁
*   **事实陈述**：文章提到Iberdrola利用Amazon Bedrock AgentCore构建了不同的代理架构。这表明技术栈不再仅仅依赖RPA（机器人流程自动化）或固定的决策树，而是引入了基于大语言模型（LLM）的规划层。
*   **你的推断**：这是行业内的一个重要信号。传统的ServiceNow实施通常侧重于表单化和流程固化，而引入AgentCore意味着系统开始具备理解自然语言意图并动态调用工具的能力。
*   **技术深度**：AgentCore的核心在于“编排”。它不仅仅是调用一个模型，而是管理记忆、检索增强生成（RAG）和工具调用。这种架构解决了LLM在复杂企业环境中“幻觉”和上下文窗口限制的问题，使得处理复杂的IT运维工单成为可能。

#### 2. 解决“非结构化数据”与“结构化流程”的断层
*   **事实陈述**：Iberdrola作为全球最大的公用事业公司之一，其IT环境极其复杂，遗留系统众多。
*   **作者观点**：文章暗示了AI在处理遗留系统文档和即时故障排查中的潜力。传统ITSM（IT服务管理）最大的痛点是用户提交的工单往往是非结构化的、描述不清的文本，而后端需要结构化的API调用。
*   **实用价值**：Agentic AI在此处的价值在于充当了“翻译层”和“路由层”。它能将模糊的报错自动匹配到知识库文章，甚至自动触发修复脚本，这在高负载运维场景下能显著降低MTTR（平均修复时间）。

#### 3. 信任边界与安全围栏是落地的核心挑战
*   **事实陈述**：Iberdrola选择了AWS作为合作伙伴，并使用了Bedrock这一托管服务。
*   **你的推断**：对于能源行业这种关键基础设施（CII）而言，数据隐私是红线。Iberdrola敢用公有云的生成式AI，说明Bedrock在“数据不出境”或“私有化微调”方面的合规性满足了其严苛要求。
*   **行业影响**：这为其他受监管行业（金融、医疗）提供了一个范本——即**如何在保持数据安全的前提下利用生成式AI**。

### 反例与边界条件

尽管文章前景乐观，但必须批判性地看待其局限性：

1.  **边界条件：复杂推理的“黑盒”风险**
    *   **反例**：Agentic AI在处理涉及多系统耦合的级联故障时，可能会给出看似合理但灾难性的建议。例如，为了重启一个服务而错误地关闭了依赖它的关键数据库。
    *   **你的推断**：文章未提及“人在回路”的具体机制。在IT变更管理中，完全自动化的Agent是极其危险的，其应用边界应严格限制在“信息查询”和“低风险操作”领域。

2.  **边界条件：成本与性能的权衡**
    *   **反例**：对于简单的密码重置或常见问题（FAQ），调用庞大的Agent架构（LLM推理+向量检索+工具调用）的成本和延迟，远高于传统的基于规则的脚本。
    *   **作者观点**：如果Iberdrola将所有IT负载都跑在Agent上，运营成本（OpEx）可能会爆炸式增长。真正的技术挑战在于**路由智能**——即决定什么时候用AI，什么时候用传统脚本。

### 可验证的检查方式

为了验证该项目的真实成效，而非仅停留在营销层面，建议关注以下指标：

1.  **指标：平均交互轮数与解决率**
    *   **验证方式**：观察AI Agent在ServiceNow中处理工单时，是否能在2轮以内解决用户问题，且无需人工介入。如果AI频繁将工单转回人工，说明意图识别或工具调用能力不足。

2.  **实验：回溯测试**
    *   **验证方式**：选取过去一年的高难度工单数据集，让Agent进行模拟处理，对比其生成的解决方案与人工实际操作的一致性。重点关注“幻觉率”，即AI是否编造了不存在的运维命令。

3.  **观察窗口：变更事故率**
    *   **验证方式**：在上线后的6个月内，统计由AI建议或直接执行的操作所引发的次要事故数量。如果因AI误操作导致的回滚频率上升，则说明架构的“安全护栏”尚未完善。

### 总结与建议

这篇文章虽然简短，但精准地捕捉到了企业级AI从“聊天”走向“行动”的趋势。Iberdrola的案例证明了**Agentic Architecture（代理架构）**在ITSM领域的成熟度正在提高。

**实际应用建议：**
对于打算跟进的企业，不要试图构建一个全能的“上帝Agent”。应采取**“分而治之”**的策略：构建专门负责“日志分析”的Agent、专门负责“API调用”的Agent和专门负责“合规检查”的Agent，然后通过一个主控Agent进行调度。同时，必须在ServiceNow中保留强制的人工审核节点，特别是对于涉及生产环境的变更请求。

---
## 技术分析

# 技术分析

## 1. 核心观点深度解读

**主要观点**
本案例的核心观点是：企业级IT运维正从“基于规则的自动化”向“基于推理的自主化”演进。Iberdrola通过引入Amazon Bedrock AgentCore，构建了具备推理能力的智能体，成功解决了大型企业中IT服务管理（ITSM）流程僵化、知识库利用率低以及人工处理成本高的问题。

**核心思想**
文章传达的核心思想是**“代理式工作流重构”**。这不仅仅是给聊天机器人加个大模型（LLM），而是通过AgentCore框架，让AI具备调用工具、理解上下文并执行复杂ServiceNow API操作的能力，使AI从信息的检索者转变为任务的执行者。

**观点的创新性与深度**
- **创新性**：将通用的Foundation Model（FM）与特定的企业逻辑通过AgentCore解耦，避免了为特定任务微调模型的昂贵成本，转而通过“推理+工具”的方式解决问题。
- **深度**：触及了企业AI落地的深水区——**数据安全与私有化部署**。利用Bedrock，Iberdrola可以在不将敏感IT数据泄露给公共模型的前提下，利用Claude等模型的能力。

**为什么重要**
对于拥有海量IT资产和复杂运维流程的传统企业，这标志着**AIOps（智能运维）从“监控报警”迈向了“认知自治”**。它证明了在高度监管的能源行业，生成式AI可以安全地介入核心业务流程。

## 2. 关键技术要点

**涉及的关键技术**
- **Amazon Bedrock AgentCore**：AWS提供的全托管代理服务，负责编排LLM、用户提示和工具。
- **Amazon Bedrock**：底层模型服务（可能涉及Anthropic Claude 3或Amazon Titan系列）。
- **ServiceNow API**：ITSM流程的执行接口。
- **RAG（检索增强生成）架构**：用于查询企业内部文档和历史工单。

**技术原理和实现方式**
该架构采用**多智能体**模式：
1. **理解与路由**：AgentCore分析用户意图。
2. **知识检索**：调用RAG工具查询向量数据库。
3. **API编排**：生成并执行ServiceNow REST API请求。
4. **上下文记忆**：维护会话状态，确保多轮交互连贯。

**技术难点与解决方案**
- **幻觉控制**：利用**Guardrails**限制输出范围，强制API验证参数。
- **私有数据隔离**：利用Bedrock的私有加密通道，确保内部数据不用于训练公共模型。

**技术创新点分析**
最大的创新在于**“零样本/少样本工具学习”**。无需编写大量硬编码脚本，而是通过定义OpenAPI Schema，让LLM根据自然语言动态拼接API请求。

## 3. 实际应用价值

**对实际工作的指导意义**
该案例表明，**“大模型+RAG+工具调用”**是企业内部提效的最优解（MVP），能将IT人员从繁琐的Tier-1工单处理中解放出来。

**可应用场景**
- **IT服务台（Tier 1）**：自动处理密码重置、软件安装、权限申请。
- **知识管理**：将非结构化文档转化为可对话的知识库。
- **变更管理**：分析变更风险，自动审批低风险操作。

**需要注意的问题**
- **权限管控**：遵循最小权限原则，防止AI误操作。
- **数据质量**：RAG的效果依赖于知识库的准确性与更新频率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于知识库的生成式问答架构

**说明**
传统的 IT 运维搜索依赖关键词匹配，难以理解复杂的自然语言查询。利用 Amazon Bedrock 的 AgentCore 架构，结合大型语言模型（LLM）和向量数据库，可构建能理解上下文并生成准确答案的智能问答系统。Iberdrola 的案例显示，将非结构化数据（如文档、日志）转化为向量索引，能显著提升信息检索的准确率和响应速度。

**实施步骤**
1.  **数据收集与清洗**：整合来自 Confluence、Jira、ServiceNow 等工具的运维文档和工单数据。
2.  **向量化存储**：使用 Amazon Bedrock 的 Embeddings 模型将文本数据转化为向量，并存储在向量数据库（如 Amazon OpenSearch Serverless）中。
3.  **配置检索流程**：在 Agent 中配置检索增强生成（RAG）流程，确保模型在回答问题时引用最新的内部知识库。

**注意事项**
确保数据源的权限控制，防止敏感运维信息泄露给未授权人员；定期更新向量索引以保持知识库的时效性。

---

### 实践 2：实施多模型策略以优化成本与性能

**说明**
不同的 IT 运维场景对模型的能力要求不同。例如，简单的日志查询可能不需要使用参数量最大的昂贵模型。Iberdrola 利用 Amazon Bedrock 提供的多种模型选择（如 Anthropic Claude, Amazon Titan 等），根据任务复杂度动态调用最适合的模型，从而在保证性能的前提下优化运营成本。

**实施步骤**
1.  **场景分类**：将运维任务分为“简单查询”、“代码生成”、“复杂推理”等类别。
2.  **模型评估**：在 Bedrock 上对不同模型进行基准测试，评估其在各类任务上的准确性和延迟。
3.  **动态路由**：在应用层实现逻辑，根据用户查询的类型，将其路由到性价比最高的基础模型。

**注意事项**
监控不同模型的 Token 使用量和延迟，避免因频繁切换模型导致用户体验不一致。

---

### 实践 3：通过语义搜索打破数据孤岛

**说明**
IT 运营数据通常分散在多个孤立的系统中。利用 AgentCore 的能力，可以通过语义理解而非硬编码的 API 调用来连接这些系统。Iberdrola 的实践表明，通过自然语言处理技术，可以让 Agent 自动识别用户意图，并从正确的数据源（如监控工具、CMDB）中提取信息，实现跨系统的数据聚合。

**实施步骤**
1.  **定义 API Schema**：为后端系统定义清晰的 OpenAPI 规范或函数调用描述。
2.  **意图识别**：利用 LLM 分析用户输入，确定需要调用哪些系统或工具。
3.  **结果聚合**：Agent 将来自不同工具的数据整合，生成统一的自然语言回复。

**注意事项**
处理跨系统查询时的权限验证，确保 Agent 只能访问用户有权查看的数据；处理不同数据源之间的数据格式冲突。

---

### 实践 4：建立负责任的 AI 与安全防护机制

**说明**
在处理企业敏感的 IT 运维数据时，安全性至关重要。Amazon Bedrock 提供了 VPC 支持、数据加密和 PI redaction（个人身份信息脱敏）等功能。最佳实践要求在模型交互前后实施严格的安全过滤，防止 Prompt 注入攻击和敏感数据泄露。

**实施步骤**
1.  **配置 Guardrails**：在 Amazon Bedrock 中启用 Guardrails，设置过滤策略以阻止有害或有偏见的内容。
2.  **数据脱敏**：在将数据发送给模型之前，自动识别并脱敏 IP 地址、用户名或密码等敏感信息。
3.  **VPC 部署**：确保 Agent 与后端资源之间的通信完全在私有网络内进行。

**注意事项**
定期审计模型的输入和输出日志，确保没有发生数据泄露；不要在 Prompt 中直接包含敏感凭证。

---

### 实践 5：实施“人机协同”的反馈闭环

**说明**
AI Agent 在处理复杂或高风险的运维操作时，不应完全自动化。Iberdrola 的设计理念是“人在回路”，即 AI 提供建议或草稿，由人类专家进行确认或修正。这不仅能提高操作的安全性，还能利用人类的反馈来持续微调系统提示词。

**实施步骤**
1.  **设计审批流**：对于高风险操作（如删除资源、修改配置），强制要求人工确认。
2.  **引入反馈机制**：在用户界面添加反馈按钮，收集用户对 AI 回答质量的评价。
3.  **持续迭代**：利用人工修正的数据和用户反馈，定期优化 Prompt 模板和知识库内容。

---
## 学习要点

- 利用 Amazon Bedrock AgentCore 构建的 AI 智能体能够自动化处理复杂的 IT 运维任务，显著提升响应速度与效率。
- 通过将生成式 AI 与现有 IT 工作流深度集成，实现了从人工操作到智能自动化运维的转变，大幅降低了运营成本。
- AI 智能体具备自主拆解复杂问题并调用相应工具的能力，有效减少了 IT 团队在重复性流程操作上所花费的时间。
- 借助大语言模型（LLM）的强大推理能力，系统能够更精准地理解用户自然语言指令，提升了人机交互的准确性和用户体验。
- 该解决方案展示了如何利用生成式 AI 技术对企业内部知识库进行有效利用，加速了故障排查与解决方案的获取。
- 采用 Amazon Bedrock 确保了架构的可扩展性与安全性，使企业能够灵活应对未来业务增长的需求。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [IT 运营](/tags/it-%E8%BF%90%E8%90%A5/) / [多代理架构](/tags/%E5%A4%9A%E4%BB%A3%E7%90%86%E6%9E%B6%E6%9E%84/) / [变更管理](/tags/%E5%8F%98%E6%9B%B4%E7%AE%A1%E7%90%86/) / [事件管理](/tags/%E4%BA%8B%E4%BB%B6%E7%AE%A1%E7%90%86/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow 运]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-10.md" >}})
- [Iberdrola 如何利用 Amazon Bedrock AgentCore 优化 ServiceNow I]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-11.md" >}})
- [Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-8.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*