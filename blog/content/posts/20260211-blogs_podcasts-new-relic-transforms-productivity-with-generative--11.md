---
title: "New Relic transforms productivity with generative AI on"
date: 2026-02-11T12:07:35+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "AWS", "企业级", "生产力", "技术架构", "智能助手", "NOVA", "落地实践"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "**总结：New Relic 借助 AWS 生成式 AI 实现生产力变革** New Relic 与 **AWS 生成式 AI 创新中心** 深度合作，成功将其智能助手 **New Relic NOVA**（New Relic Omnipresence Virtual Assistant）从一个单纯的知识助手升级为一套"
external_url: https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws
scenarios: ["AI/ML项目"]
---

# New Relic transforms productivity with generative AI on AWS

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:45:16+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws)

---
## 摘要/简介

Working with the Generative AI Innovation Center, New Relic NOVA (New Relic Omnipresence Virtual Assistant) evolved from a knowledge assistant into a comprehensive productivity engine. We explore the technical architecture, development journey, and key lessons learned in building an enterprise-grade AI solution that delivers measurable productivity gains at scale.

---
## 摘要

**总结：New Relic 借助 AWS 生成式 AI 实现生产力变革**

New Relic 与 **AWS 生成式 AI 创新中心** 深度合作，成功将其智能助手 **New Relic NOVA**（New Relic Omnipresence Virtual Assistant）从一个单纯的知识助手升级为一套全面的生产力引擎。

该内容重点探讨了构建这一企业级 AI 解决方案的过程，涵盖了以下核心方面：

1.  **技术架构与演进**：详细介绍了支撑 NOVA 的技术架构及其从简单功能向复杂生产力工具演变的开发历程。
2.  **企业级落地经验**：分享了在构建可扩展、高可靠性的企业级 AI 系统时解决的关键挑战。
3.  **显著成效**：该方案成功实现了大规模的可衡量生产力提升，为企业数字化转型提供了强有力的支持。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用生成式 AI 加速代码生成与开发流程

**说明**:
通过集成 Amazon Bedrock 等生成式 AI 服务，开发团队可以自动化编写样板代码、生成单元测试，并根据自然语言需求创建代码片段。New Relic 的实践表明，这能显著减少开发人员在重复性编码任务上的时间消耗，从而将更多精力投入到核心业务逻辑和创新中。

**实施步骤**:
1. 评估现有的开发工作流，识别可以通过自动化节省时间的环节（如 API 文档生成、测试用例编写）。
2. 利用 AWS 的 AI 服务（如 CodeWhisperer 或 Bedrock）集成到 IDE 或 CI/CD 流水线中。
3. 建立代码审查机制，确保 AI 生成的代码符合安全标准和性能要求。

**注意事项**:
生成式 AI 产生的代码必须经过严格的安全扫描和人工审查，以防止引入漏洞或技术债务。

---

### 实践 2：构建智能化的可观测性助手

**说明**:
传统的可观测性工具数据量大且复杂，查询门槛高。利用大语言模型（LLM）将自然语言查询转换为数据库查询语言（如 NRQL），可以让非技术背景的业务人员或运维人员也能快速获取系统洞察。New Relic 通过这种方式降低了数据查询的门槛，提升了全员生产力。

**实施步骤**:
1. 定义用户常用的查询场景和意图。
2. 选择合适的 LLM 模型并进行微调，使其能准确理解自然语言并转换为特定的查询语法。
3. 在现有仪表盘或操作界面中嵌入自然语言处理（NLP）接口。

**注意事项**:
需严格限制 AI 助手的数据访问权限，确保其只能回答用户权限范围内的数据问题，防止数据泄露。

---

### 实践 3：自动化数据摘要与异常根因分析

**说明**:
面对海量的监控日志和警报，人工分析效率低下。利用生成式 AI 对日志数据进行智能总结、自动检测异常模式并分析根本原因（RCA），可以大幅缩短平均修复时间（MTTR）。AI 能快速关联分散的事件，给出简洁的事故报告。

**实施步骤**:
1. 将应用性能监控（APM）和日志数据流式传输至支持向量搜索或 AI 分析的服务。
2. 配置 AI 模型以识别正常行为模式与异常偏离。
3. 设置自动化工作流，在检测到异常时自动生成包含上下文和可能原因的摘要报告。

**注意事项**:
AI 的分析结果应作为辅助决策，关键操作仍需人工确认，以避免误判导致的服务中断。

---

### 实践 4：利用 AWS 基础设施实现安全与可扩展的 AI 部署

**说明**:
在 AWS 上部署生成式 AI 应用（如利用 Amazon SageMaker 或 Bedrock）可以无缝利用 AWS 的安全合规框架和弹性计算能力。这确保了在处理敏感数据时的安全性，同时能够根据业务需求自动扩展资源，优化成本结构。

**实施步骤**:
1. 采用 AWS Lambda 或 ECS 进行无服务器容器化部署，以应对 AI 推理的弹性需求。
2. 配置 AWS IAM Identity Center，实施细粒度的访问控制和数据加密。
3. 使用 AWS Cost Explorer 监控 AI 模型运行带来的额外成本，并设置预算警报。

**注意事项**:
生成式 AI 模型的推理成本可能较高，建议实施智能缓存策略，对常见问题进行缓存以减少 API 调用次数。

---

### 实践 5：建立负责任的 AI 使用规范与护栏

**说明**:
随着 AI 工具的普及，确保其输出内容的准确性、公正性和安全性至关重要。企业需要建立明确的 AI 使用政策，防止员工将敏感代码或数据输入到公共 AI 模型中，同时要验证 AI 输出的事实准确性，防止“幻觉”误导决策。

**实施步骤**:
1. 制定企业内部的 AI 使用指南，明确哪些数据可以用于 AI 训练或提示，哪些禁止。
2. 在 AI 应用层实施内容过滤机制，屏蔽有害或有偏见的内容。
3. 定期对 AI 模型的输出进行抽样评估，确保其持续符合业务预期。

**注意事项**:
保护知识产权（IP）和客户隐私是首要任务，优先使用企业级、私有化的 AI 模型而非公共模型来处理敏感数据。

---

### 实践 6：持续监控与优化 AI 模型性能

**说明**:
AI 模型本身也是软件系统的一部分，需要对其进行可观测性监控。通过跟踪 AI 的响应延迟、Token 使用量、查询成功率以及用户满意度，可以持续优化提示词工程和模型选择，确保 AI 投资的回报率。

**实施步骤**:
1. 为 AI 服务端点配置专门的监控仪表盘，关注延迟和错误率。
2. 收集用户对 AI 生成结果的反馈（如点赞/点踩），用于未来的模型微调。
3. 定期进行 A/B 测试，比较不同模型或提示词策略的效果。

**注意事项**:
AI 模型可能会随时间出现性能漂移，必须建立持续评估循环，及时更新模型版本或提示词

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [生成式 AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8F-ai/) / [AWS](/tags/aws/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/) / [生产力](/tags/%E7%94%9F%E4%BA%A7%E5%8A%9B/) / [技术架构](/tags/%E6%8A%80%E6%9C%AF%E6%9E%B6%E6%9E%84/) / [智能助手](/tags/%E6%99%BA%E8%83%BD%E5%8A%A9%E6%89%8B/) / [NOVA](/tags/nova/) / [落地实践](/tags/%E8%90%BD%E5%9C%B0%E5%AE%9E%E8%B7%B5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [New Relic NOVA：基于AWS构建企业级生成式AI生产力引擎]({{< relref "posts/20260210-blogs_podcasts-new-relic-transforms-productivity-with-generative--10.md" >}})
- [Scale LLM fine-tuning with Hugging Face and Amazon Sage]({{< relref "posts/20260211-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [利用 Hugging Face 与 SageMaker 扩展企业级 LLM 微调]({{< relref "posts/20260210-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*