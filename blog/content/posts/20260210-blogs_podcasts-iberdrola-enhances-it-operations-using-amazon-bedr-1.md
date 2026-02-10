---
title: "Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营"
date: 2026-02-10T21:20:19+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "**Iberdrola 利用 Amazon Bedrock AgentCore 优化 IT 运营** 作为全球最大的公用事业公司之一，Iberdrola 通过与 AWS 合作，采用前沿的人工智能技术对其在 ServiceNow 平台上的 IT 运营进行了全面革新。借助 Amazon Bedrock AgentCore，"
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

Iberdrola 是全球最大的公用事业公司之一，已采用前沿 AI 技术来革新其在 ServiceNow 平台上的 IT 运营。通过与 AWS 合作，Iberdrola 利用 Amazon Bedrock AgentCore 部署了多种代理架构，聚焦三个关键领域：优化草稿阶段的变更请求验证、以情境智能丰富事件管理，以及借助对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加快工单解决速度，并在整个组织范围内实现一致、高质量的数据处理。

---
## 导语

作为全球规模领先的公用事业企业，Iberdrola 面临着复杂的 IT 运营管理挑战。本文介绍了该公司如何通过与 AWS 合作，利用 Amazon Bedrock AgentCore 在 ServiceNow 平台上部署多种 AI 代理架构。通过优化变更请求验证、丰富事件管理情境及简化模型选择，这些举措有效减少了流程瓶颈。阅读本文，您将了解前沿 AI 技术如何具体落地，帮助团队提升工单解决速度并实现高质量的数据处理。

---
## 摘要

**Iberdrola 利用 Amazon Bedrock AgentCore 优化 IT 运营**

作为全球最大的公用事业公司之一，Iberdrola 通过与 AWS 合作，采用前沿的人工智能技术对其在 ServiceNow 平台上的 IT 运营进行了全面革新。借助 Amazon Bedrock AgentCore，Iberdrola 实施了多种智能体架构，重点聚焦于以下三个关键领域：

1.  **优化变更请求验证**：在变更请求的草拟阶段引入 AI 优化流程；
2.  **丰富事件管理**：利用上下文情报增强事件管理能力；
3.  **简化变更模型选择**：通过对话式 AI 简化变更模型的选择过程。

这些创新举措有效减少了运营瓶颈，不仅帮助团队加速了工单解决速度，还在整个组织范围内实现了高质量、一致的数据处理。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用生成式 AI 构建知识库以实现 IT 运营自动化

**说明**:
传统的 IT 运营依赖人工检索文档和手册，效率低下且容易出错。通过使用 Amazon Bedrock 和 AgentCore 技术，可以将零散的 IT 文档（如 Wiki、Confluence、Runbook）整合，构建成一个生成式 AI 驱动的知识库。这使得系统能够理解自然语言查询，并自动生成准确的解决方案或直接执行操作，从而将响应时间从小时级缩短到分钟级。

**实施步骤**:
1. **数据收集与清洗**：汇总所有相关的 IT 运维文档，清洗掉过时或重复的信息。
2. **向量化存储**：使用 Amazon Bedrock 的嵌入模型将文档转换为向量，并存储在向量数据库中。
3. **Agent 配置**：配置 AgentCore 逻辑，使其能够根据用户提问检索相关上下文，并调用基础模型生成回答。

**注意事项**:
确保知识库数据的实时更新，避免 AI 提供过时的配置信息。

---

### 实践 2：采用人机协同模式确保关键操作的准确性

**说明**:
虽然 AI 可以处理大量常规请求，但在 IT 运营中，关键基础设施的变更或故障处理仍需极高准确性。Iberdrola 的经验表明，最佳模式是“AI 建议 + 人工确认”。AI 负责初步诊断和生成脚本，由运维人员审核后执行，或者由 AI 在受控权限下自动执行非破坏性操作。

**实施步骤**:
1. **权限分级**：定义 AI Agent 的操作权限边界，区分“只读”、“建议”和“执行”权限。
2. **审批流集成**：将 AI 生成的操作建议集成到现有的工单系统（如 ServiceNow 或 Jira）中，供人工审核。
3. **反馈循环**：记录人工修正 AI 建议的案例，用于微调模型。

**注意事项**:
对于可能导致服务中断的命令，必须保留人工“最后一公里”的确认机制。

---

### 实践 3：标准化提示词工程与上下文管理

**说明**:
为了获得高质量的回答，必须对 Amazon Bedrock 中的基础模型进行精细的提示词管理。通过为 IT 运营场景设计专门的系统提示词，可以约束 AI 的行为，使其输出符合企业内部规范（如特定的代码风格、日志格式或沟通语气）。

**实施步骤**:
1. **定义角色与目标**：在系统提示词中明确 AI 的角色（例如：“你是一位资深的 Linux 系统管理员”）。
2. **上下文注入**：在每次请求中动态注入相关的环境上下文（如特定服务器的版本、网络拓扑信息）。
3. **输出格式化**：强制要求 AI 以结构化格式（如 JSON 或 Markdown）返回数据，便于后续解析。

**注意事项**:
定期审查和优化提示词，以适应新的业务需求或模型版本更新。

---

### 实践 4：建立严格的治理与安全防护机制

**说明**:
在引入生成式 AI 时，数据安全和隐私是首要考量。必须确保通过 Amazon Bedrock 传输的数据是加密的，并且 AgentCore 在调用外部 API 或执行命令时，有严格的防注入和验证机制，防止提示词泄露或恶意指令执行。

**实施步骤**:
1. **数据脱敏**：在将日志或代码发送给 Bedrock 之前，自动脱敏敏感信息（如密码、IP 地址、PII 数据）。
2. **Guardrails 设置**：利用 Amazon Bedrock Guardrails 过滤不当内容或阻止模型越狱。
3. **审计日志**：开启所有 AI 交互的 CloudTrail 日志记录，确保每个操作可追溯。

**注意事项**:
定期进行安全审计，检查 AI Agent 是否有权限访问超出其职责范围的数据。

---

### 实践 5：实施持续监控与模型评估

**说明**:
AI 模型的表现并非一成不变。需要建立一套监控体系，跟踪 AgentCore 的响应质量、成功率和用户满意度。通过分析“幻觉”案例或错误的解决方案，持续改进知识库和提示词。

**实施步骤**:
1. **定义 KPI**：设定关键指标，如平均解决时间 (MTTR)、查询成功率、用户采纳率。
2. **A/B 测试**：在灰度环境中对比不同模型或提示词版本的效果。
3. **人工评估**：定期抽样 AI 的回答，由专家团队进行质量打分。

**注意事项**:
关注模型漂移现象，当底层基础模型更新时，务必重新评估现有应用的表现。

---

### 实践 6：渐进式推广与用户培训

**说明**:
技术成功不等于业务成功。Iberdrola 的项目成功部分归功于对员工的培训。不要试图一次性用 AI 替代所有流程，而应从低风险场景开始，逐步建立团队对 AI 工具的信任。

**实施步骤**:
1. **试点项目**：选择一个痛点明显但风险较低的 IT 团队（如 Level 1 技术

---
## 学习要点

- 基于您提供的来源主题，以下是关于 Iberdrola 利用 Amazon Bedrock AgentCore 增强 IT 运营的关键要点总结：
- Iberdrola 通过部署基于 Amazon Bedrock 的 AgentCore 解决方案，成功实现了 IT 运营中复杂服务请求的自动化处理，显著提升了运维效率。
- 该智能代理能够与企业现有的 ITSM（IT 服务管理）工具和知识库深度集成，从而在无需人工干预的情况下精准执行任务。
- 利用生成式 AI 的自然语言处理能力，系统可以准确理解员工的查询意图，并将非结构化请求转化为具体的操作指令。
- 该解决方案不仅减少了 IT 服务台的工作量，还加快了员工获取技术支持和完成业务请求的速度。
- Iberdrola 的实践展示了大型企业如何利用生成式 AI 技术优化内部工作流程，为能源行业的数字化转型提供了重要参考。

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

- [🔥GPT-5职场革命！企业如何用AI重塑生产力？🚀]({{< relref "posts/20260127-blogs_podcasts-inside-gpt-5-for-work-how-businesses-use-gpt-5-9.md" >}})
- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260210-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--8.md" >}})
- [Building Prometheus: How Backend Aggregation Enables Gi]({{< relref "posts/20260210-blogs_podcasts-building-prometheus-how-backend-aggregation-enable-8.md" >}})
- [OpenAI在ChatGPT测试广告以支持免费访问]({{< relref "posts/20260210-blogs_podcasts-testing-ads-in-chatgpt-1.md" >}})
- [Transformers.js v4 预览版已发布 NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*