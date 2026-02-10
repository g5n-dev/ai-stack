---
title: "New Relic NOVA：基于AWS构建企业级生成式AI生产力引擎"
date: 2026-02-10T22:46:04+08:00
draft: false
entry_kind: "auto"
tags: ["生成式AI", "AWS", "企业级", "生产力", "技术架构", "LLM", "虚拟助手", "New Relic"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文介绍了 New Relic 与 AWS 生成式 AI 创新中心合作，将其虚拟助手 NOVA 从一个单纯的知识助手，转型为全面生产力引擎的案例。 文章重点探讨了以下三个方面： 1. **技术架构**：构建企业级 AI 解决方案的技术实现细节。 2. **开发历程**：项目从概念到落地的演进"
external_url: https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws
scenarios: ["AI/ML项目", "大语言模型"]
---

# New Relic NOVA：基于AWS构建企业级生成式AI生产力引擎

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:45:16+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws)

---
## 摘要/简介

通过与生成式人工智能创新中心合作，New Relic NOVA（New Relic 全能虚拟助手）已从知识助手演进为一款全面的生产力引擎。我们探讨了在构建一款企业级 AI 解决方案过程中的技术架构、开发历程以及关键经验，该解决方案能够在大规模范围内实现可衡量的生产力提升。

---
## 摘要

以下是对该内容的中文总结：

本文介绍了 New Relic 与 AWS 生成式 AI 创新中心合作，将其虚拟助手 NOVA 从一个单纯的知识助手，转型为全面生产力引擎的案例。

文章重点探讨了以下三个方面：
1.  **技术架构**：构建企业级 AI 解决方案的技术实现细节。
2.  **开发历程**：项目从概念到落地的演进过程。
3.  **关键经验**：在大规模部署中实现可衡量的生产力提升所获得的重要经验与教训。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用生成式 AI 构建智能运维助手

**说明**:  
基于 Amazon Bedrock 等服务集成大语言模型（LLM），构建能够理解自然语言查询的智能助手。通过将 New Relic 的可观测性数据与生成式 AI 结合，允许用户使用非技术语言（如“为什么我的网站变慢了？”）来查询复杂的系统状态，从而降低数据分析的门槛，加速问题排查过程。

**实施步骤**:
1. **数据准备**：确保 New Relic 中已配置并收集了足够的日志、指标和链路追踪数据。
2. **模型选择**：在 AWS 上选择适合的基座模型（如 Amazon Titan 或通过 Bedrock 访问的第三方模型）。
3. **RAG 架构搭建**：建立检索增强生成（RAG）流程，将用户的自然语言问题转换为 New Relic 的查询语言（如 NRQL），并检索相关上下文。
4. **接口集成**：将 AI 助手集成到现有的工作流中（如 Slack 或内部门户）。

**注意事项**:  
确保 LLM 在执行查询时遵循严格的权限控制，防止通过自然语言注入导致非授权的数据访问。

---

### 实践 2：自动化异常检测与根本原因分析

**说明**:  
利用生成式 AI 分析海量的可观测性数据，自动识别偏离基线的异常行为。不同于传统的静态阈值告警，生成式 AI 可以理解复杂的上下文关系，自动生成事故摘要，并推测潜在的根本原因，从而减少运维人员在“理解事故”上花费的时间。

**实施步骤**:
1. **基线建立**：让 AI 模型学习正常流量模式下的系统行为。
2. **模式识别**：配置 AI 驱动的异常检测器，实时监控数据流中的非线性变化。
3. **自动关联**：当检测到异常时，利用 AI 自动关联同一时间窗口内的日志错误、部署变更和数据库延迟。
4. **生成报告**：自动生成包含可能原因的初步事故报告，供 SRE 团队审核。

**注意事项**:  
AI 生成的根本原因分析应作为“辅助建议”而非绝对结论，人工审核机制必不可少，以防止误导。

---

### 实践 3：优化云成本与资源效率

**说明**:  
利用 AI 分析 New Relic 中的基础设施性能数据与 AWS 成本数据，识别资源浪费和性能瓶颈。生成式 AI 可以提供具体的优化建议（例如：“将非生产环境的数据库实例在夜间缩小规格以节省 30% 成本”），并自动生成优化脚本的代码片段。

**实施步骤**:
1. **数据集成**：将 AWS CloudWatch Billing Metrics 与 New Relic 的基础设施监控数据打通。
2. **成本模式训练**：训练模型识别高成本低回报的资源使用模式（如闲置的 EC2 实例或过度配置的容器）。
3. **建议生成**：设置定期任务，让 AI 生成包含具体 ROI 分析的优化建议书。
4. **自动化执行**：对于低风险的优化建议，通过 AWS Lambda 实现自动化修复。

**注意事项**:  
在实施自动缩容或资源释放策略前，务必设置资源锁定机制，防止关键业务组件被误操作。

---

### 实践 4：利用 AI 辅助编写与维护代码

**说明**:  
结合 Amazon CodeWhisperer 等工具，利用生成式 AI 帮助开发人员编写用于监控的应用代码（如自定义插件、API 集成脚本）。AI 可以根据 New Relic 的最佳实践自动生成样板代码，确保监控代码的规范性和覆盖率，减少技术债务。

**实施步骤**:
1. **IDE 集成**：在开发环境中集成 AI 编码助手。
2. **上下文注入**：在编写代码时，提供 New Relic API 文档作为上下文参考，让 AI 生成符合规范的调用代码。
3. **代码审查**：利用 AI 审查现有的监控代码，指出未处理的异常或性能不佳的查询语句。
4. **单元测试生成**：自动生成针对监控逻辑的测试用例，确保数据采集的稳定性。

**注意事项**:  
AI 生成的代码必须经过安全扫描，确保没有硬编码的密钥或敏感信息（如 AWS API Key）泄露。

---

### 实践 5：构建生成式 AI 应用的可观测性

**说明**:  
当企业基于 AWS 构建自己的生成式 AI 应用时，New Relic 可以作为专门的监控层。最佳实践包括监控 LLM 的延迟、Token 使用量（成本）、提示词有效性以及模型的幻觉率。这确保了 AI 应用本身的可靠性、安全性和成本效益。

**实施步骤**:
1. **定义指标**：确立关键 AI 指标，如每次交互的平均 Token 数、模型响应时间及用户满意度评分。
2. **追踪链路**：利用分布式追踪记录从用户提示到模型响应再到后端数据库调用的完整链路。
3. **数据质量监控**：监控输入和输出数据，检测是否存在提示词注入攻击或不当内容生成。
4. **成本看板**：

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/new-relic-transforms-productivity-with-generative-ai-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [生成式AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8Fai/) / [AWS](/tags/aws/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/) / [生产力](/tags/%E7%94%9F%E4%BA%A7%E5%8A%9B/) / [技术架构](/tags/%E6%8A%80%E6%9C%AF%E6%9E%B6%E6%9E%84/) / [LLM](/tags/llm/) / [虚拟助手](/tags/%E8%99%9A%E6%8B%9F%E5%8A%A9%E6%89%8B/) / [New Relic](/tags/new-relic/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [利用 Hugging Face 与 SageMaker 扩展企业级 LLM 微调]({{< relref "posts/20260210-blogs_podcasts-scale-llm-fine-tuning-with-hugging-face-and-amazon-9.md" >}})
- [AI对工程类岗位的影响或与预期不同]({{< relref "posts/20260129-hacker_news-ais-impact-on-engineering-jobs-may-be-different-th-5.md" >}})
- [Codex 应用：基于 GPT-3 的代码生成工具]({{< relref "posts/20260202-hacker_news-the-codex-app-1.md" >}})
- [Codex 应用：基于 OpenAI 模型的代码生成工具]({{< relref "posts/20260203-hacker_news-the-codex-app-12.md" >}})
- [我的 AI 技术应用实践与经验总结]({{< relref "posts/20260205-hacker_news-my-ai-adoption-journey-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*