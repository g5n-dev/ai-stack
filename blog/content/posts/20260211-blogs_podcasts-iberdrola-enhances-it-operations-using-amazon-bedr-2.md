---
title: "Iberdrola enhances IT operations using Amazon Bedrock A"
date: 2026-02-11T09:27:49+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "智能体", "IT 运营", "事件管理", "对话式 AI", "AWS"]
categories: ["AI 工程", "大模型"]
source: blogs_podcasts
description: "Iberdrola 作为全球最大的公用事业公司之一，正通过采用尖端的人工智能技术，对其 ServiceNow 平台中的 IT 运营进行彻底变革。 在与 AWS 的合作下，Iberdrola 利用 **Amazon Bedrock AgentCore** 实施了多种智能代理架构，重点聚焦于以下三个核心领域以实现优化： 1"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola enhances IT operations using Amazon Bedrock AgentCore

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

Iberdrola 是全球最大的公用事业公司之一，已采用前沿的人工智能技术，在 ServiceNow 中对其 IT 运营进行变革。通过与 AWS 合作，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种代理架构，重点聚焦三个领域：在草稿阶段优化变更请求的校验，为事件管理注入上下文智能，以及借助对话式 AI 简化变更模型的选择。这些创新举措消除了瓶颈，帮助团队加快工单解决速度，并在整个组织范围内确保数据处理的一致性与高质量。

---
## 摘要

Iberdrola 作为全球最大的公用事业公司之一，正通过采用尖端的人工智能技术，对其 ServiceNow 平台中的 IT 运营进行彻底变革。

在与 AWS 的合作下，Iberdrola 利用 **Amazon Bedrock AgentCore** 实施了多种智能代理架构，重点聚焦于以下三个核心领域以实现优化：

1.  **优化变更请求验证：** 在草案阶段即介入，提升验证效率。
2.  **丰富事件管理：** 利用上下文情报增强事件处理能力。
3.  **简化变更模型选择：** 通过对话式 AI 让模型选择过程更加便捷。

这些创新举措成功消除了运营瓶颈，不仅帮助团队加速了工单解决速度，还在整个组织范围内实现了高质量且一致的数据处理。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于角色的访问控制与审计机制

**说明**：在利用 Amazon Bedrock AgentCore 等 AI 工具增强 IT 运营时，必须确保所有自动化操作都遵循最小权限原则。Iberdrola 的经验表明，为不同的 IT 运营角色（如网络管理员、系统运维人员、安全分析师）定义精细的 IAM 权限至关重要，防止 AI 代理执行越权操作。同时，必须对所有 AI 生成的操作指令和执行结果进行完整的日志记录，以满足能源行业严格的合规与审计要求。

**实施步骤**：
1. 定义 IT 运维中不同角色的职责边界，梳理出允许 AI 代理执行的操作清单。
2. 在 Amazon Bedrock 和 AWS IAM 中配置精细的策略，确保 AgentCore 只能调用被授权的特定 API。
3. 启用 AWS CloudTrail 以监控所有 API 调用，并建立集中式日志分析（如 Amazon OpenSearch Service）来审查 AI 的决策路径。

**注意事项**：定期审查权限策略，特别是在更新模型或添加新的 IT 运维工具时，确保权限范围未无意扩大。

---

### 实践 2：实施 RAG 模式以利用私有领域知识

**说明**：通用的基础大模型往往缺乏企业内部特定的 IT 架构、历史故障处理手册和专有协议的知识。通过检索增强生成（RAG）架构，将 Iberdrola 内部的 IT 文档库、历史工单系统和基础设施配置文件与 Amazon Bedrock AgentCore 连接，可以显著提高故障诊断的准确率和响应速度，确保生成的建议符合企业实际环境。

**实施步骤**：
1. 将非结构化的 IT 文档和知识库文章存储到 Amazon OpenSearch Service 或 Amazon Aurora PostgreSQL 等向量数据库中。
2. 配置 AgentCore 的知识库功能，将其与向量存储关联。
3. 在提示词工程中明确指示模型优先检索内部知识库，而非仅依赖预训练数据。

**注意事项**：定期更新知识库内容，剔除过时的文档，防止 AI 依据错误的旧信息生成操作建议。

---

### 实践 3：建立“人机协同”的确认与验证流程

**说明**：为了防止 AI 幻觉或逻辑错误导致关键 IT 基础设施（如电网控制系统）发生意外中断，不能允许 AI 完全自动执行高风险操作。最佳实践是设计一个分级响应机制：对于信息查询和低风险操作允许 AI 自主完成，而对于变更类、高风险操作（如修改防火墙规则、重启服务器），必须引入人工审批环节。

**实施步骤**：
1. 对 IT 运维任务进行风险分级（低、中、高）。
2. 在 AgentCore 的工作流中配置逻辑：高风险操作仅生成执行脚本或方案，并暂停等待人工确认。
3. 通过 Slack 或 Microsoft Teams 集成，将待确认的操作推送给运维专家。

**注意事项**：确保人工确认界面的信息展示清晰，包含 AI 的推理依据和潜在影响评估，以便专家快速决策。

---

### 实践 4：统一 API 接口与工具链集成

**说明**：Iberdrola 的 IT 环境复杂，涉及多种遗留系统和现代云服务。Amazon Bedrock AgentCore 的核心价值在于能够作为“大脑”协调不同的“手脚”。最佳实践是构建标准化的 API 层，将各种 IT 运维工具（如 ServiceNow、监控工具、自动化脚本）封装为统一的 Lambda 函数或 API 接口，供 AgentCore 调用，从而消除工具孤岛。

**实施步骤**：
1. 审计现有的 IT 运维工具，识别出可被自动化的关键功能。
2. 将这些功能封装为 AWS Lambda 函数或通过 Amazon API Gateway 暴露。
3. 在 Bedrock Agents 的 Action Group 中定义这些 API 的 OpenAPI 规范，使模型能够理解并正确调用。

**注意事项**：确保 API 的幂等性，防止因网络重试等原因导致重复执行同一操作。

---

### 实践 5：设计针对 IT 运维场景的提示词工程

**说明**：通用的提示词可能无法满足 IT 运营对精确性和格式的要求。需要专门为 IT 运维场景设计 System Prompt，明确 AI 的角色定位、输出格式（如 JSON、特定的命令行代码）以及安全边界。这能确保 AgentCore 输出的内容不仅易于阅读，而且可以直接被机器执行或导入工单系统。

**实施步骤**：
1. 在模型配置中设定严格的 System Prompt，例如“你是一位资深的 IT 运维专家，请基于提供的知识库回答问题，输出必须符合 JSON 格式”。
2. 定义 Few-shot（少样本）示例，在提示词中包含标准的故障排查案例，引导模型模仿。
3. 强制要求模型在执行任何变更类操作前，必须先列出潜在风险和回滚方案。

**注意事项**：提示词需要随着业务逻辑的变化而持续迭代，避免模型产生过时或刻板的回答。

---
## 学习要点

- Iberdrola 通过利用 Amazon Bedrock 的 AgentCore 框架，成功构建了生成式 AI 智能体，从而实现了 IT 运维流程的自动化与现代化。
- 该解决方案通过整合专有数据与大语言模型（LLM），有效解决了模型幻觉问题，确保了技术文档查询和故障排查的准确性。
- 利用 Amazon Bedrock 的托管服务，企业无需管理底层基础设施即可快速构建和扩展 AI 应用，显著降低了技术门槛和运维成本。
- 智能体能够自动执行复杂任务并调用 Amazon Systems Manager 等工具，大幅缩短了 IT 问题的解决时间，提升了运营效率。
- 该实施案例展示了如何在保证数据安全和隐私的前提下，将生成式 AI 安全地集成到企业现有的 IT 环境中。
- 通过自然语言处理技术，该系统将复杂的 IT 运维知识转化为直观的对话界面，降低了技术人员的使用门槛并改善了用户体验。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [IT 运营](/tags/it-%E8%BF%90%E8%90%A5/) / [事件管理](/tags/%E4%BA%8B%E4%BB%B6%E7%AE%A1%E7%90%86/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/) / [AWS](/tags/aws/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [亚马逊利用Nova模型自动化新履约中心运营就绪测试]({{< relref "posts/20260211-blogs_podcasts-how-amazon-uses-amazon-nova-models-to-automate-ope-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*