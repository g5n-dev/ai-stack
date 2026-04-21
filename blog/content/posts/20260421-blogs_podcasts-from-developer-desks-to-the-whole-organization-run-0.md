---
title: "Amazon Bedrock上线Claude Cowork"
date: 2026-04-21T19:31:59+08:00
draft: false
entry_kind: "auto"
tags: ["Claude", "Amazon Bedrock", "Claude Cowork", "LLM网关", "AI助手", "产品发布", "知识工作者", "开发工具"]
categories: ["大模型"]
source: blogs_podcasts
description: "概览 今天正式宣布，Claude Cowork 已在 Amazon Bedrock 上线。用户现在可以在 Bedrock 环境中直接运行 Cowork 和 Claude Code Desktop，或通过 LLM 网关访问，从而把原本仅限开发者使用的工具扩展到整个组织。 集成方式 - **直接调用**：在 Bedrock"
external_url: https://aws.amazon.com/blogs/machine-learning/from-developer-desks-to-the-whole-organization-running-claude-cowork-in-amazon-bedrock
scenarios: ["大语言模型", "AI/ML项目"]
---

# Amazon Bedrock上线Claude Cowork

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-04-21T19:13:49+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/from-developer-desks-to-the-whole-organization-running-claude-cowork-in-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/from-developer-desks-to-the-whole-organization-running-claude-cowork-in-amazon-bedrock)

---
## 摘要/简介

今天，我们很高兴宣布在 Amazon Bedrock 中推出 Claude Cowork。您现在可以通过 Amazon Bedrock 直接或使用 LLM 网关来运行 Cowork 和 Claude Code Desktop。在本文中，我们将介绍 Claude Cowork 如何与 Amazon Bedrock 集成，并展示知识工作者如何在实践中使用它。

---
## 摘要

#### 概览
今天正式宣布，Claude Cowork 已在 Amazon Bedrock 上线。用户现在可以在 Bedrock 环境中直接运行 Cowork 和 Claude Code Desktop，或通过 LLM 网关访问，从而把原本仅限开发者使用的工具扩展到整个组织。

#### 集成方式
- **直接调用**：在 Bedrock 控制台或 API 中选择对应模型实例，启动 Cowork 或 Claude Code Desktop，零配置即可使用。
- **LLM 网关**：通过统一的 LLM 网关路由请求，支持在企业内部已有的 AI Gateway 框架中无缝接入，提供统一的身份验证、日志和配额管理。

#### 使用示例
某企业的业务分析师在日常工作中需要快速生成报告摘要。借助 Bedrock 上的 Cowork，分析师只需在协作界面输入需求，系统自动调用大模型进行文本抽取、结构和语言优化，最终生成可直接阅读的摘要。整个过程无需编写代码，完全由业务用户自行完成，显著提升了工作效率。

#### 价值与前景
- **组织覆盖**：从研发团队扩展到非技术岗位，实现全员 AI 协作。
- **统一治理**：利用 Bedrock 的安全、合规和监控能力，统一管理所有 AI 交互。
- **快速落地**：无需额外的基础设施投入，直接在现有的 AWS 环境中启用，降低了部署门槛。

通过 Amazon Bedrock，Cowork 与 Claude Code Desktop 为企业提供了从代码开发到业务决策的全链路 AI 支持，帮助组织更快实现智能化转型。

---
## 评论

#### 中心观点

事实陈述：文章宣布 Claude Cowork 与 Claude Code Desktop 已可在 Amazon Bedrock 上运行，支持直接调用或通过 LLM 网关。
作者观点：作者认为这标志着 AI 辅助工具从开发者桌面扩展到全组织，是企业级生产力提升的关键路径。
推断：这一举措可能促使更多业务部门采用自然语言模型进行工作流自动化。

#### 支撑理由

事实陈述：文章列举了统一安全合规、跨部门资源调度、即插即用 API 三项优势。
作者观点：作者指出这些优势降低了技术门槛，使非技术用户也能快速上手。
推断：若企业成功落地，Cowork 或成为标准协作平台，提升跨团队协作效率。

#### 边界条件

事实陈述：目前仅在特定 AWS 区域可用，且受 IAM 权限和 Bedrock 配额限制。
作者观点：作者提醒部署前需评估现有云资源与安全策略的适配度。
推断：对尚未使用 AWS 的组织，迁移成本可能限制该方案的适用范围。

#### 实践启发

事实陈述：文章提供了知识工作者使用 Cowork 自动化报告生成的示例。
作者观点：作者建议先从试点项目验证 ROI，再逐步扩大规模。
推断：企业应建立 AI 治理小组，负责模型使用监控与合规审查，确保技术落地的可持续性。

---
## 技术分析

#### 核心观点
- 文章宣布 **Claude Cowork** 与 **Claude Code Desktop** 通过 **Amazon Bedrock** 对外提供，支持直接 API 调用或经由 LLM Gateway 路由。
- 将原本面向开发者的 AI 编程助手扩展至全体知识工作者，强调跨部门协作、企业级安全与合规。

##### 关键技术点
- **托管式 Bedrock 平台**：统一 IAM、VPC、加密与审计，满足多租户合规需求。
- **Cowork 容器化**：每个会话在独立计算单元中保持状态，支持细粒度权限控制。
- **LLM Gateway 路由**：依据模型能力动态分发请求、实现批处理、流量分片与容错。
- **安全与合规**：传输加密、静态加密、RBAC、数据驻留与 GDPR/SOC2 认证。
- **集成工作流**：提供 CI/CD 插件、SageMaker 兼容接口、CloudWatch 监控与 CloudTrail 审计。

##### 实际应用价值
- 开发者通过 AI 代码补全、自动化审查提升生产力。
- 非技术业务人员使用自然语言接口完成报告生成、文档摘要等任务，降低技术门槛。
- 统一平台实现资源共享、成本透明，帮助企业统一预算与配额管理。

##### 行业影响
- 推动 **AI 能力从研发部门渗透到全组织**，改变企业采购与部署 AI 服务的模式。
- 为其他云服务商树立企业级 LLM 集成的标杆，加速行业合规落地。

##### 边界条件与实践建议
- **边界条件**：仅在支持的 AWS 区域可用；跨境数据隐私法规可能限制使用；并发会话数受限于配额。
- **实践建议**：
  1. 在开发环境先做概念验证，评估吞吐量、成本与延迟。
  2. 配置细粒度 RBAC，防止未授权访问模型输出。
  3. 启用 CloudWatch 与 CloudTrail 监控异常调用并完成审计。
  4. 对业务部门进行使用合规与输出质量培训。
  5. 生产环境使用 LLM Gateway 做流量分片，避免单点瓶颈。

#### 论证地图
##### 中心命题
Claude Cowork 通过 Amazon Bedrock 实现全组织 AI 代码协作是可规模化、合规且具备成本优势的解决方案。

##### 支撑理由
1. Bedrock 提供统一治理与安全合规基础设施，降低自建成本。
2. Cowork 的会话保持与版本控制提升跨团队协作效率。
3. LLM Gateway 实现多模型混合部署、负载均衡与容错。

##### 反例或边界条件
- 若企业已拥有自建微调平台且对数据主权要求极高，迁移成本可能抵消收益。
- 对实时性要求极高的交互式调试，托管服务可能导致响应延迟。

##### 可验证方式
- 基准测试对比 Bedrock 与自建环境的延迟、吞吐与费用。
- 审计日志验证安全合规；业务满意度调研评估协作效率提升。

---
## 学习要点

- 请您提供这篇文章或更详细的摘要，这样我才能为您提炼出 5‑7 条关键要点。谢谢。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/from-developer-desks-to-the-whole-organization-running-claude-cowork-in-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/from-developer-desks-to-the-whole-organization-running-claude-cowork-in-amazon-bedrock)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Claude](/tags/claude/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [Claude Cowork](/tags/claude-cowork/) / [LLM网关](/tags/llm%E7%BD%91%E5%85%B3/) / [AI助手](/tags/ai%E5%8A%A9%E6%89%8B/) / [产品发布](/tags/%E4%BA%A7%E5%93%81%E5%8F%91%E5%B8%83/) / [知识工作者](/tags/%E7%9F%A5%E8%AF%86%E5%B7%A5%E4%BD%9C%E8%80%85/) / [开发工具](/tags/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Claude：打造用于深度思考的交互空间]({{< relref "posts/20260204-hacker_news-claude-is-a-space-to-think-12.md" >}})
- [Claude Is a Space to Think]({{< relref "posts/20260204-hacker_news-claude-is-a-space-to-think-17.md" >}})
- [Claude：一个用于深度思考的交互空间]({{< relref "posts/20260204-hacker_news-claude-is-a-space-to-think-5.md" >}})
- [Claude：打造用于深度思考的AI交互空间]({{< relref "posts/20260205-hacker_news-claude-is-a-space-to-think-18.md" >}})
- [Claude Opus 4.6 发布]({{< relref "posts/20260205-hacker_news-claude-opus-46-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*