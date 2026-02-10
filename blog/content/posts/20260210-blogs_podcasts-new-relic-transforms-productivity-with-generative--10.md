---
title: "New Relic联手AWS构建生成式AI生产力引擎"
date: 2026-02-10T21:20:19+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文详细介绍了 New Relic 如何通过与 AWS 生成式 AI 创新中心合作，将其虚拟助手 NOVA 从单纯的知识助手升级为全面的生成引擎，从而显著提升生产力。 **核心内容概要：** 1. **项目背景与目标** * **挑战：** 随着 New Relic 平台功能的快速增长，用户"
external_url: https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws
scenarios: ["Web应用开发"]
---

# New Relic联手AWS构建生成式AI生产力引擎

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:45:16+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws)

---
## 摘要/简介

Working with the Generative AI Innovation Center, New Relic NOVA (New Relic Omnipresence Virtual Assistant) evolved from a knowledge assistant into a comprehensive productivity engine. We explore the technical architecture, development journey, and key lessons learned in building an enterprise-grade AI solution that delivers measurable productivity gains at scale.

---
## 导语

New Relic 与 AWS Generative AI Innovation Center 合作，将 NOVA 从基础的知识助手升级为全面的生产力引擎。本文深入剖析了该企业级 AI 解决方案的技术架构与开发历程，探讨了如何通过生成式 AI 实现可衡量的效率提升。无论您关注系统设计还是工程实践，都能从中获得构建大规模生产级 AI 应用的宝贵经验。

---
## 摘要

以下是对该内容的中文总结：

本文详细介绍了 New Relic 如何通过与 AWS 生成式 AI 创新中心合作，将其虚拟助手 NOVA 从单纯的知识助手升级为全面的生成引擎，从而显著提升生产力。

**核心内容概要：**

1.  **项目背景与目标**
    *   **挑战：** 随着 New Relic 平台功能的快速增长，用户（包括开发者和客户）面临信息过载，难以快速找到所需文档或操作指引，导致效率低下。
    *   **解决方案：** 开发 New Relic NOVA，利用生成式 AI 技术，帮助用户快速解答问题、执行任务并提供可操作的洞察。

2.  **技术架构与实现**
    *   **基础架构：** 系统构建于 AWS 之上，利用 **Amazon Bedrock** 作为底层模型接入层，提供了灵活性和安全性。
    *   **模型选择：** 经过评估，选择了 **Anthropic 的 Claude 3** 模型。该模型在处理长上下文、遵循复杂指令以及减少幻觉方面表现优异。
    *   **技术栈：** 结合了 **LangChain** 进行编排，使用 **Amazon OpenSearch Service** 进行语义检索（RAG 架构），并采用 **AWS Step Functions** 编排工作流。

3.  **关键功能与应用场景**
    *   **知识检索：** NOVA 能基于 New Relic 庞大的文档库，精准回答技术问题。
    *   **任务自动化：** 它不仅能回答问题，还能生成并运行代码（如 NRQL 查询），甚至直接调用 API 执行操作，充当“代理”角色。
    *   **可观测性：** NOVA 自身也具备完整的可观测性，开发者可以追踪其思维链和执行步骤。

4.  **开发经验与教训**
    *   **迭代开发：** 项目采用了快速原型与迭代的方法，从简单的“问答”逐步扩展到复杂的“任务执行”。
    *   **评估与优化：** 建立了严格的评估机制，利用合成数据生成和“黄金数据集”来持续测试模型性能，确保回答的准确性和相关性。
    *   **上下文管理：** 优化了提示词工程和上下文窗口的使用，以处理复杂的技术文档。

5.  **成果与展望**
    *   NOVA 已成为企业级 AI 解决方案的

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Amazon Bedrock 构建可扩展的生成式 AI 基础

**说明**:
通过使用 Amazon Bedrock 服务，企业可以无需管理底层基础设施即可访问高性能的基础模型（如 Claude 3 等）。New Relic 的实践表明，直接调用 Bedrock API 能够快速集成大语言模型能力，同时利用 AWS 的云原生架构保障系统的可扩展性和安全性。

**实施步骤**:
1. 在 AWS 控制台中启用 Amazon Bedrock 服务，并请求访问所需的基础模型。
2. 配置 IAM 角色，确保应用程序拥有调用 Bedrock `InvokeModel` API 的最小权限。
3. 在应用代码中通过 AWS SDK (如 Boto3) 建立与 Bedrock 的连接，处理推理请求和响应流。

**注意事项**:
- 严格控制 API 密钥和 IAM 权限，遵循最小权限原则。
- 监控 Token 使用量和 API 调用延迟，以便优化成本和性能。

---

### 实践 2：实施全面的可观测性策略

**说明**:
构建生成式 AI 应用不仅仅是调用模型，还需要监控整个请求链路，包括向量数据库检索、上下文构建以及模型推理的耗时。New Relic 通过监控 AWS Lambda 函数和 Bedrock 的调用情况，确保了 AI 助手的响应速度和准确性。

**实施步骤**:
1. 部署 New Relic Lambda 扩展层，自动捕获函数的冷启动和内存使用情况。
2. 利用 OpenTelemetry 标准协议，将 Bedrock 的调用指标（如延迟、Token 消耗）发送至 New Relic 平台。
3. 配置自定义仪表盘，可视化展示用户查询的端到端延迟和模型推理成功率。

**注意事项**:
- 确保在日志中脱敏处理 PII（个人身份信息），避免敏感数据传入可观测性平台。
- 设置针对高延迟或高错误率的告警阈值。

---

### 实践 3：优化提示词工程与上下文管理

**说明**:
生成式 AI 的质量高度依赖于 Prompt 的设计。最佳实践包括建立动态的 Prompt 模板，并根据用户意图注入相关的上下文信息（如文档片段），以提高回答的相关性并减少幻觉。

**实施步骤**:
1. 建立版本控制的 Prompt 模板库，针对不同任务（如总结、提取、问答）设计专用模板。
2. 实施检索增强生成（RAG）模式，先通过语义搜索获取相关文档，再将其作为上下文填入 Prompt。
3. 迭代测试不同的 Prompt 变体，基于用户反馈闭环优化模板。

**注意事项**:
- 注意上下文窗口的 Token 限制，避免超出模型最大处理长度。
- 在 Prompt 中明确设定输出格式（如 JSON 或 Markdown），便于后续处理。

---

### 实践 4：采用无服务器架构以实现弹性与成本效益

**说明**:
利用 AWS Lambda 等 Serverless 服务运行 AI 应用逻辑，可以根据请求量自动伸缩，仅在代码执行时付费。这种架构特别适合处理突发流量，避免了为闲置资源付费。

**实施步骤**:
1. 将 AI 应用的后端逻辑封装为 AWS Lambda 函数。
2. 配置 API Gateway 或 Application Load Balancer 作为触发器。
3. 调整 Lambda 的内存和超时设置，以适应不同 LLM 的推理时间需求。

**注意事项**:
- 注意 Lambda 的默认超时限制，对于耗时较长的模型推理任务，可能需要异步调用模式。
- 优化 Lambda 层的大小，加快冷启动速度。

---

### 实践 5：建立严格的数据治理与安全合规机制

**说明**:
在使用生成式 AI 时，数据隐私和安全至关重要。必须确保传输到 AWS Bedrock 的数据符合企业合规要求，并防止数据泄露给未授权的模型或第三方。

**实施步骤**:
1. 启用 AWS KMS（Key Management Service）对静态数据进行加密。
2. 在数据发送至 LLM 之前，通过中间件层进行敏感数据扫描和过滤。
3. 定期审计 AWS CloudTrail 日志，追踪所有对 Bedrock API 的访问记录。

**注意事项**:
- 了解所选基础模型的数据保留政策（例如 AWS 不使用客户数据训练模型）。
- 建立数据使用审批流程，区分公开数据与内部机密数据的处理路径。

---

### 实践 6：构建基于反馈的持续改进闭环

**说明**:
AI 模型的效果需要持续验证。通过收集用户对 AI 回复的点赞/点踩反馈，可以将人工反馈转化为模型微调或 Prompt 优化的依据，从而持续提升系统效能。

**实施步骤**:
1. 在用户界面集成简单的反馈机制（如“有用/无用”按钮）。
2. 将反馈数据连同原始 Query、上下文和模型响应存储在数据湖（如 Amazon S3）中。
3. 定期分析低分案例，针对性地调整 Prompt 或补充知识库内容。

**注意事项**:
- 确保反馈数据的收集符合隐私法规。
- 建立自动化流程，定期评估模型在特定测试

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [blogs_podcasts](/tags/blogs-podcasts/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260210-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--8.md" >}})
- [Building Prometheus: How Backend Aggregation Enables Gi]({{< relref "posts/20260210-blogs_podcasts-building-prometheus-how-backend-aggregation-enable-8.md" >}})
- [结合Hugging Face与SageMaker实现企业级LLM高效微调]({{< relref "posts/20260210-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [OpenAI在ChatGPT测试广告以支持免费访问]({{< relref "posts/20260210-blogs_podcasts-testing-ads-in-chatgpt-1.md" >}})
- [Transformers.js v4 预览版已发布 NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*