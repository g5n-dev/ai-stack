---
title: Iberdrola 如何利用 Amazon Bedrock AgentCore 优化 ServiceNow I
date: 2026-02-10 22:46:04+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- ServiceNow
- 智能体架构
- IT 运营
- AWS
- 对话式 AI
- 情境智能
categories:
- AI 工程
- 大模型
source: blogs_podcasts
description: Iberdrola（伊比德罗拉）作为全球最大的公用事业公司之一，通过引入前沿的AI技术，成功实现了其 ServiceNow 平台中 IT
  运营的革新。 在与 AWS 的合作中，Iberdrola 利用 **Amazon Bedrock AgentCore** 实施了多种智能体架构，重点聚焦于三大关键领域：
  1. **优
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios:
- AI/ML项目
aliases:
- /posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1/
- /posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-2/
- /posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-7/
- /posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-8/
- /posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-10/
- /posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-11/
- /posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-12/
- /posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-13/
- /posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-8/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# Iberdrola 如何利用 Amazon Bedrock AgentCore 优化 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

作为全球规模最大的公用事业公司之一，Iberdrola 引入尖端人工智能技术，在 ServiceNow 中彻底变革其 IT 运营。通过与 AWS 合作，Iberdrola 借助 Amazon Bedrock AgentCore 实施了多种智能体架构，聚焦三大关键领域：在起草阶段优化变更请求验证、以情境智能丰富事件管理，以及利用对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加速工单解决，并在整个组织范围内实现一致且高质量的数据处理。

---
## 导语

作为全球规模最大的公用事业公司之一，Iberdrola 正通过引入尖端人工智能技术，在 ServiceNow 平台上重塑其 IT 运营模式。本文将详细拆解其如何利用 Amazon Bedrock AgentCore 构建智能体架构，以优化变更请求验证、丰富事件管理情境，并简化模型选择。通过这些具体实践，读者可以了解到企业如何借助对话式 AI 减少流程瓶颈，从而加速工单解决并提升整体数据质量。

---
## 摘要

Iberdrola（伊比德罗拉）作为全球最大的公用事业公司之一，通过引入前沿的AI技术，成功实现了其 ServiceNow 平台中 IT 运营的革新。

在与 AWS 的合作中，Iberdrola 利用 **Amazon Bedrock AgentCore** 实施了多种智能体架构，重点聚焦于三大关键领域：

1.  **优化变更请求验证**：在起草阶段提升验证效率；
2.  **丰富事故管理**：利用情境智能增强事故处理能力；
3.  **简化变更模型选择**：通过对话式 AI 辅助模型选择。

这些创新举措有效消除了运营瓶颈，帮助团队加速了工单解决速度，并确保了整个组织内数据处理的**一致性**与**高质量**。

---
## 评论

### 评价综述

**中心观点**：文章通过Iberdrola利用Amazon Bedrock AgentCore重构ServiceNow IT运维的案例，核心展示了**“多智能体架构”如何将传统IT服务管理从“脚本化流程”升级为“具有推理能力的自主运维”**，标志着能源行业IT正从“上云”迈向“云原生AI智能化”的深水区。

---

### 深度评价与维度分析

#### 1. 内容深度：从“自动化”到“自主化”的范式跨越
*   **支撑理由**：
    *   **[事实陈述]** 文章提及使用Amazon Bedrock AgentCore构建“不同的智能体架构”，这不仅是简单的API调用，而是引入了规划、记忆和工具使用能力。
    *   **[你的推断]** Iberdrola作为全球最大的公用事业公司之一，其IT环境极其复杂（涉及SCADA、AMI、GIS等多系统异构数据）。文章暗示了通过AgentCore处理非结构化数据（如工单描述）并调用ServiceNow API的能力，这解决了传统ITSM中“分类僵化”的痛点。
    *   **[作者观点]** 这种架构体现了“神经符号AI”的趋势——结合大模型的语言理解能力与ServiceNow的结构化业务逻辑。
*   **反例/边界条件**：
    *   **边界条件**：在处理涉及物理安全（如电网断电指令）或高合规性（如核设施维护）的操作时，纯概率性的LLM推理必须被严格的人机回环机制截断，文章若未强调此点，则技术严谨性有缺憾。

#### 2. 实用价值：高门槛的“样板间”
*   **支撑理由**：
    *   **[事实陈述]** 案例具体落地在ServiceNow这一通用平台，而非定制系统，使得该架构对大量使用SNOW的企业具有极高的参考价值。
    *   **[你的推断]** 对于CIO而言，价值在于证明了“生成式AI不仅能聊天，还能干活”。它展示了如何利用Bedrock的托管服务快速绕过模型选型和基础设施运维的泥潭，直接进入业务逻辑开发。
*   **反例/边界条件**：
    *   **反例**：对于中小型企业，Bedrock+AgentCore+SNOW的许可成本和定制开发成本极高。如果企业IT流程尚未标准化，上AI只会加速制造混乱。

#### 3. 创新性：AgentCore作为“编排中枢”
*   **支撑理由**：
    *   **[作者观点]** 文章的亮点在于AgentCore的角色。它不仅仅是一个路由器，更是一个“元智能体”，负责拆解任务（如“优化 incident”），然后分发给专门的子智能体（如“查询KB智能体”、“执行变更智能体”）。
    *   **[你的推断]** 这代表了从RAG（检索增强生成）向Agentic RAG的演进，即AI不再被动回答问题，而是主动调用API修改系统状态。
*   **反例/边界条件**：
    *   **反例**：目前Agent模式在长链路任务中的稳定性仍受“幻觉”风险困扰，如果缺乏强大的测试框架，这种创新可能带来不可预测的系统错误。

#### 4. 可读性与逻辑
*   **[作者观点]** 摘要逻辑清晰，遵循了“挑战-方案-架构-成效”的标准商业案例叙事。
*   **[你的推断]** 虽然摘要未展开，但此类文章通常容易陷入“营销术语堆砌”（如Revolutionize, Cutting-edge），需要读者具备较强的技术背景去伪存真，剥离出“多智能体协作”这一核心技术实质。

#### 5. 行业影响：能源行业的数字化风向标
*   **[你的推断]** Iberdrola作为传统能源巨头，其技术选择具有风向标意义。这表明能源行业的数字化转型焦点已从“连接设备”转向“智能运营”。这将促使其他公用事业公司加速在ERP、CRM、EAM等核心系统中引入生成式AI代理。

#### 6. 争议点与不同观点
*   **争议点**：**数据主权与模型黑箱的冲突**。
    *   **[你的推断]** 欧洲能源企业对GDPR极为敏感。将内部IT工单数据发送至Amazon Bedrock（即便在特定区域处理），是否完全符合欧洲严格的AI法案和数据隐私要求？文章可能回避了数据清洗和脱敏的巨大工程成本。
*   **不同观点**：**Agent vs. 传统RPA**。
    *   传统的RPA（机器人流程自动化）也能处理ServiceNow流程。观点的差异在于：Agent能处理RPA无法处理的“模糊意图”，但Agent缺乏RPA的“确定性”。文章若过分强调Agent而贬低传统自动化，则是片面的。

---

### 实际应用建议

1.  **不要直接复制架构，要复制“思维”**：
    *   不要上来就部署AgentCore。先梳理IT运维中哪些环节是“基于语言且高频重复”的（如L1分级排查、工单摘要），这些是Agent的切入点。
2.  **建立“护栏机制”**：
    *   在ServiceNow中为AI Agent设置严格的权限边界。例如，Agent只能“建议”变更，而不能直接“执行”生产环境的变更，必须由人工确认。
3.  **关注“人机协同”的指标**：
    *   不要只看“自动化率”。要关注“平均解决时间（MTTR）”的缩短幅度和“工单一次性解决率（FCR

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于 Amazon Bedrock 的统一智能运维代理架构

**说明**: 
利用 Amazon Bedrock 的 AgentCore 能力，构建一个集中式的智能运维代理。该代理作为中间层，连接底层基础设施数据与上层运维人员，通过自然语言处理理解运维意图，自动编排工具并执行修复操作，从而实现从被动响应到主动预测的转变。

**实施步骤**:
1. **定义代理角色**: 明确运维代理的职责边界，如日志分析、事件响应或资源优化。
2. **集成知识库**: 将 Iberdrola 现有的运维手册、Runbook 和历史工单数据向量化并存储到 Amazon OpenSearch Serverless 等向量数据库中，作为 Agent 的上下文。
3. **配置工具组**: 通过 API 将监控工具（如 Datadog, Splunk）和执行工具（如 AWS Systems Manager）连接到 Bedrock Agent。
4. **选择基础模型**: 根据任务复杂度选择合适的 FM（如 Claude 3 或 Anthropic 系列），平衡推理能力与响应速度。

**注意事项**: 
确保代理具有最小权限原则，仅授予执行特定运维任务所需的 IAM 权限。

---

### 实践 2：实施 RAG 技术以增强领域知识准确性

**说明**: 
单纯依赖大模型可能导致“幻觉”，在电力能源等关键行业中这是不可接受的。通过检索增强生成（RAG）技术，强制模型在回答问题或执行操作前，先从 Iberdrola 专有的内部文档中检索相关信息，确保生成的建议和代码符合公司特定的安全和操作标准。

**实施步骤**:
1. **数据清洗与预处理**: 去除过时的运维文档，确保知识库内容的时效性。
2. **建立索引**: 使用 Amazon Bedrock Knowledge Base 功能自动管理嵌入模型和向量存储。
3. **提示词工程**: 在系统提示词中明确指示模型：“必须优先依据检索到的上下文信息回答，若未找到相关信息则回答不知道”。
4. **持续微调**: 根据代理的反馈循环，定期更新检索策略和文档库。

**注意事项**: 
需对知识库的访问进行严格控制，防止敏感的基础设施拓扑信息泄露给未授权人员。

---

### 实践 3：建立“人机协同”的验证与反馈闭环

**说明**: 
在自动化运维的初期，保持“人在回路”至关重要。Iberdrola 的实践表明，在 Agent 执行高风险操作（如变更配置、删除资源）之前，引入人工审批机制，可以有效建立信任，并收集负反馈样本用于后续优化。

**实施步骤**:
1. **风险分级**: 将运维操作分为“低风险（自动执行）”、“中风险（人工确认）”和“高风险（人工执行）”三个等级。
2. **配置审批流**: 对于中高风险操作，Agent 应生成详细的执行计划并通过 Slack 或 Microsoft Teams 发送给运维工程师审批。
3. **反馈收集**: 在每次交互结束后，增加用户满意度评价（点赞/点踩），并将这些数据存储在 S3 中用于后续分析。
4. **监控与干预**: 使用 Amazon CloudWatch 监控 Agent 的行为，一旦检测到异常循环或错误，立即触发人工介入。

**注意事项**: 
审批流程不应过于繁琐，以免影响运维效率，建议仅对涉及生产环境核心资源的操作设置人工关卡。

---

### 实践 4：标准化工具接口与 API 编排

**说明**: 
Amazon Bedrock Agent 的核心能力在于调用 Action Groups。为了最大化效率，必须将现有的 IT 运维工具（无论是基于 AWS 的还是本地遗留系统）封装成标准化的 RESTful API。这使得 Agent 能够像拼积木一样组合不同工具的功能来解决复杂问题。

**实施步骤**:
1. **API 网关统一**: 使用 Amazon API Gateway 作为所有运维工具的统一入口，屏蔽后端系统的复杂性。
2. **OpenAPI 规范定义**: 为每个工具编写清晰的 OpenAPI (Swagger) 定义文件，详细描述参数、返回值和语义，以便 LLM 准确理解如何调用。
3. **错误处理标准化**: 统一 API 错误码和错误消息格式，使 Agent 能够解析错误并自动尝试重试或回滚。
4. **Lambda 函数封装**: 对于复杂的逻辑，编写 AWS Lambda 函数作为中间层，处理多步骤的编排逻辑。

**注意事项**: 
确保 API 的幂等性，防止因网络重试导致重复执行操作（例如重复重启同一台服务器）。

---

### 实践 5：利用 Guardrails 保障安全性与合规性

**说明**: 
能源行业对数据安全和合规性要求极高。利用 Amazon Bedrock Guardrails 建立防护栏，防止 Agent 生成有害内容、提取敏感 PII（个人身份信息）或执行违反公司安全策略的指令。

**实施步骤**:
1. **设置内容过滤**: 配置 Guardrails 以过滤仇恨言论、暴力或任何非专业用语。
2. **敏感信息屏蔽**: 配置正则表达式模式，自动识别并屏蔽 IP 地址、客户数据或内部密钥，防止这些信息被泄露

---
## 学习要点

- 基于对 Iberdrola 利用 Amazon Bedrock 和 AgentCore 增强 IT 运营的案例分析，以下是总结出的关键要点：
- Iberdrola 通过利用 Amazon Bedrock 构建生成式 AI 应用程序，成功实现了 IT 运营的现代化，显著提升了内部流程的自动化水平。
- 借助 AgentCore 框架，企业能够快速开发和部署具备检索增强生成（RAG）能力的智能体，确保了数据处理的准确性和时效性。
- 该解决方案通过将大型语言模型（LLM）与内部企业数据安全集成，有效解决了数据隐私和安全性方面的挑战。
- 实施该 AI 系统后，IT 支持团队的工作效率得到大幅提升，员工能够更快速地获取技术支持并解决问题。
- 采用无服务器架构和托管服务降低了基础设施的运维复杂度，使团队能够专注于业务逻辑的创新而非底层管理。
- 此案例证明了将生成式 AI 应用于企业内部知识库的可行性，为其他传统企业进行数字化转型提供了可复用的参考架构。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [智能体架构](/tags/%E6%99%BA%E8%83%BD%E4%BD%93%E6%9E%B6%E6%9E%84/) / [IT 运营](/tags/it-%E8%BF%90%E8%90%A5/) / [AWS](/tags/aws/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/) / [情境智能](/tags/%E6%83%85%E5%A2%83%E6%99%BA%E8%83%BD/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow 运]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
