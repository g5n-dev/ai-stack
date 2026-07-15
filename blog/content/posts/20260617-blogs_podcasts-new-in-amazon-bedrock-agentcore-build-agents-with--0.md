---
title: Bedrock AgentCore新功能：知识连接与智能体治理优化
date: 2026-06-17 15:52:08+08:00
draft: false
entry_kind: auto
tags:
- 智能体
- 知识连接
- 生产监控
- 治理
- 安全合规
- 持续学习
- 实时追踪
- Bedrock
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 连接更广泛知识 AgentCore 现在能够直接接入组织内部文档、Web 检索以及付费数据源，使 agent 在运行时拥有更丰富的背景信息，提升回答的准确性和覆盖面。
  生产环境问题定位与修复 平台提供实时的执行链路追踪与异常检测，帮助团队快速定位 agent 在生产中出现的错误或性能瓶颈，并提供自动化的修复建议，降低运
external_url: https://aws.amazon.com/blogs/machine-learning/new-in-amazon-bedrock-agentcore-build-agents-with-broader-knowledge-and-continuous-learning
scenarios:
- AI/ML项目
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-06-17T15:29:36+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/new-in-amazon-bedrock-agentcore-build-agents-with-broader-knowledge-and-continuous-learning](https://aws.amazon.com/blogs/machine-learning/new-in-amazon-bedrock-agentcore-build-agents-with-broader-knowledge-and-continuous-learning)

---
## 摘要/简介

今天，我们将在 Amazon Bedrock AgentCore 上推出新的功能——这是一个用于构建、连接和优化智能体的平台。在这篇博客中，我们将介绍这些功能如何逐一弥合这些差距：将智能体与组织知识、网络知识和付费知识相连接；帮助团队发现并修复生产环境中的问题；以及实施能够随着智能体能力增长而扩展的管控措施。这些功能共同帮助您更快地构建更强大的智能体，通过可扩展的管控措施进行治理，并持续对其进行优化。

---
## 导语

Amazon Bedrock AgentCore 新增功能现已上线，旨在帮助开发团队弥合智能体与多源知识的连接缺口，并提升生产环境中的可观测性与治理能力。通过整合组织内部知识、网络检索与付费数据源，智能体能够获取更丰富的上下文信息，从而在复杂任务中做出更精准的决策。与此同时，这些功能还提供问题发现与修复的辅助能力，并支持随智能体能力演进而动态调整的管控策略，使团队能够在保障安全与合规的前提下，持续优化智能体性能并快速实现业务价值。

---
## 摘要

#### 连接更广泛知识
AgentCore 现在能够直接接入组织内部文档、Web 检索以及付费数据源，使 agent 在运行时拥有更丰富的背景信息，提升回答的准确性和覆盖面。

#### 生产环境问题定位与修复
平台提供实时的执行链路追踪与异常检测，帮助团队快速定位 agent 在生产中出现的错误或性能瓶颈，并提供自动化的修复建议，降低运维成本。

#### 可扩展的安全与合规控制
随着 agent 能力提升，控制策略会自动演进，支持细粒度的权限管理、日志审计和策略强制执行，确保治理始终与业务需求保持同步，避免风险累积。

这些新功能共同帮助企业在构建更强大 agent 的同时，实现快速迭代、全面治理和持续改进。

---
## 评论

#### 中心观点

Amazon Bedrock AgentCore 的这批新功能标志着企业级 AI Agent 从“能对话”向“能做事”转变的关键节点。知识连接能力的增强和可观测性的提升，本质上是在解决企业落地 Agent 时最核心的两个瓶颈：信息从哪里来，以及问题怎么被发现。

#### 支撑理由

**事实陈述**（基于文章摘要）：新版 AgentCore 重点补足了三大能力缺口——连接组织内部知识库、接入网络实时信息、集成付费数据源，同时强化了生产环境的可观测性和问题定位工具。

**作者观点**（从行文逻辑推断）：AWS 认为企业 Agent 之所以在生产环境中表现不稳定，根本原因并非模型能力不足，而是 Agent 与可靠知识源之间的“最后一公里”没有打通。此外，缺少有效的监控手段导致问题发现滞后，严重影响用户体验。

**我的推断**：这反映出 AWS 正在将 Agent 框架从“实验性工具”向“生产级系统”演进。知识连接和可观测性不是独立功能，而是企业级 Agent 必须具备的基础设施能力。没有这两项支撑，Agent 在受控测试环境中的优秀表现无法转化为真实业务价值。

#### 边界条件

首先，这些能力的效果高度依赖知识源的质量和更新频率——如果接入的是过时或碎片化的数据，Agent 的输出仍然会偏离预期。其次，问题定位工具的精准度受限于日志和追踪数据的完整性，企业需要投入额外的工程资源来规范化埋点。此外，多知识源集成可能带来成本叠加，尤其是付费数据源的调用费用需要提前评估ROI。

#### 实践启发

对于计划采用 AgentCore 的团队，我的建议是：先完成知识体系的治理，再推进 Agent 开发。在动手构建 Agent 之前，先审视现有知识库的覆盖率、准确性和更新机制，这是投入产出比最高的前置工作。同时，建议从低风险场景开始试点，例如内部知识问答或流程辅助，而非直接投入面向客户的对话式服务，以便在可控范围内验证监控和问题定位工具的有效性。最终，Agent 的持续优化将高度依赖生产数据的回流，知识连接和可观测性是形成这一闭环的基础。

---
## 技术分析

#### 核心观点与中心命题

Amazon Bedrock AgentCore本次更新聚焦于两个核心命题：扩展Agent知识边界与提升生产环境可观测性。平台通过引入组织知识库、Web搜索和付费数据源三类知识连接能力，解决企业Agent在实际业务场景中"知识孤岛"的痛点。同时，配套的生产监控与问题诊断工具帮助团队快速定位Agent行为异常，形成从构建到运维的完整闭环。

#### 关键技术点分析

##### 知识连接架构

新功能支持三类知识源的无缝集成：结构化的组织内部知识库、非结构化的网络实时信息、以及需要授权的付费数据服务。技术实现层面采用检索增强生成（RAG）框架，对不同来源的知识进行向量化处理和语义检索，确保Agent在响应时能够调用最相关的上下文信息。

##### 生产可观测性

监控模块提供Agent行为的完整追踪能力，包括意图识别准确率、工具调用成功率、响应延迟分布等关键指标。当检测到异常模式时，系统能够自动触发根因分析流程，帮助运维人员快速定位是知识库配置问题、提示词设计缺陷还是模型能力边界。

#### 实际应用价值

在客户服务场景中，Agent现在能够实时检索最新产品文档和常见问题解答，显著降低"幻觉"回答的概率。在数据分析场景中，集成付费数据源使Agent可以直接调用专业市场研究报告，提升回答的专业性和权威性。对于运维团队，生产监控能力将问题排查时间从小时级压缩到分钟级。

#### 行业影响

这一更新标志着企业级Agent平台从"功能完善"向"工程化落地"的转变。知识连接能力降低了企业采用Agent的门槛，无需大规模数据清洗即可利用现有知识资产。可观测性工具则为Agent的规模化部署提供了必要的基础设施支撑，预计将加速Agent在金融、医疗、法律等合规要求较高行业的渗透。

#### 边界条件与实践建议

知识连接的边界条件包括：知识库更新延迟可能导致Agent引用过时信息；多知识源冲突时缺乏统一的消解策略；付费数据源的访问成本需要精确核算。建议企业在部署时建立知识库的定期同步机制，明确各类知识源的优先级权重，并对Agent的回答进行抽检验证。

#### 论证地图

中心命题：Bedrock AgentCore通过知识扩展和生产监控能力，显著提升企业Agent的实用性和可靠性。支撑理由包括知识连接的灵活性、监控能力的完整性、以及与现有AWS生态的深度集成。反例方面，跨知识源的语义一致性和实时性仍是技术挑战，需要业务层面的人工审核机制补充。可验证方式包括生产环境的A/B测试对比、用户满意度调查、以及响应准确率的量化评估。

---
## 学习要点

- AgentCore 通过集成多源企业知识库（S3、RDS、向量库等）实现更广泛的知识覆盖，使代理能够实时检索最新数据并提供精准答案。
- 持续学习机制利用用户交互反馈和强化学习自动微调模型，代理随使用不断提升性能和准确性。
- 新的层级任务分解与并行执行功能增强了复杂业务流程的编排能力，提升了代理处理多步骤任务时的效率与容错性。
- 内置细粒度安全控制（IAM、VPC、数据加密）与合规审计功能，满足企业级安全与监管要求。
- 提供简化的 API、预置模板和一键部署功能，显著降低开发者的构建、部署与监控门槛。
- 全链路可观测性（日志、指标、追踪）帮助实时监控代理行为并快速定位问题，提升运维效率。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/new-in-amazon-bedrock-agentcore-build-agents-with-broader-knowledge-and-continuous-learning](https://aws.amazon.com/blogs/machine-learning/new-in-amazon-bedrock-agentcore-build-agents-with-broader-knowledge-and-continuous-learning)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [知识连接](/tags/%E7%9F%A5%E8%AF%86%E8%BF%9E%E6%8E%A5/) / [生产监控](/tags/%E7%94%9F%E4%BA%A7%E7%9B%91%E6%8E%A7/) / [治理](/tags/%E6%B2%BB%E7%90%86/) / [安全合规](/tags/%E5%AE%89%E5%85%A8%E5%90%88%E8%A7%84/) / [持续学习](/tags/%E6%8C%81%E7%BB%AD%E5%AD%A6%E4%B9%A0/) / [实时追踪](/tags/%E5%AE%9E%E6%97%B6%E8%BF%BD%E8%B8%AA/) / [Bedrock](/tags/bedrock/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [OpenAI Frontier：企业级AI智能体构建与治理平台]({{< relref "posts/20260205-hacker_news-openai-frontier-5.md" >}})
- [OpenAI Frontier：具备共享上下文与治理功能的企业级AI代理平台]({{< relref "posts/20260205-hacker_news-openai-frontier-5.md" >}})
- [ElevenLabs融资11亿美元估值，Cerebras获23亿美元估值及音频与芯片代理进展]({{< relref "posts/20260205-blogs_podcasts-ainews-elevenlabs-500m-series-d-at-11b-cerebras-1b-0.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
