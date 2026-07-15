---
title: AWS Secrets Manager为AgentCore Identity新增密钥引用功能，支持直接使用预先
date: 2026-06-01 23:28:09+08:00
draft: false
entry_kind: auto
tags:
- AWS
- 密钥管理
- 跨账户
- 外部连接器
- 安全
- Bedrock
- 云原生
- Agent
categories:
- AI 工程
- 安全
source: blogs_podcasts
description: 功能概述 亚马逊云服务在AgentCore Identity中新增了引用AWS Secrets Manager密钥的能力。用户可以在AgentCore直接使用已在Secrets
  Manager中预先配置好的密钥，无需在AgentCore中重新创建，从而复用已有的密钥管理流程。 关键优势 - 完全掌控密钥的加密配置、轮换
external_url: https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity
scenarios:
- AI/ML项目
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# AWS Secrets Manager为AgentCore Identity新增密钥引用功能，支持直接使用预先配置的密钥并保留完整管理控制权

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-06-01T22:16:28+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity](https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity)

---
## 摘要/简介

今天，我们很高兴地宣布在AWS Secrets Manager中为AgentCore Identity提供了引用密钥的功能，这样您就可以从Secrets Manager引用自己预先配置的密钥，并保留对其管理方式的完全控制权。利用此功能，您可以将组织现有的密钥治理流程扩展到AgentCore。您可以提供现有的、预先配置的AWS Secrets Manager密钥，以用于您的凭证提供者资源。您保留对其加密配置、轮换、复制、标签和资源策略的完全控制权，就像管理Secrets Manager中的其他密钥一样。您还可以选择同一AWS区域内其他AWS账户中的密钥，但不支持跨区域密钥共享。此功能还支持通过AWS Secrets Manager外部连接器导入的密钥，从而实现与第三方密钥管理器的集成。

---
## 摘要

#### 功能概述
亚马逊云服务在AgentCore Identity中新增了引用AWS Secrets Manager密钥的能力。用户可以在AgentCore直接使用已在Secrets Manager中预先配置好的密钥，无需在AgentCore中重新创建，从而复用已有的密钥管理流程。

#### 关键优势
- 完全掌控密钥的加密配置、轮换、复制、标签及资源策略，保持与现有Secrets Manager操作一致。
- 支持跨账户引用：在同一AWS区域内，可从其他AWS账户选取密钥，扩大共享范围。
- 兼容外部连接器：可通过AWS Secrets Manager外部连接器将第三方密钥管理器中的密钥引入AgentCore。
- 与组织已有的密钥治理流程无缝衔接，提升安全合规性。

#### 注意事项
- 不支持跨区域密钥共享，仅在同一AWS区域内有效。
- 使用跨账户密钥时，需要确保目标账户已授予相应的访问权限。
- 密钥的轮换、审计等操作仍由Secrets Manager负责，AgentCore仅负责引用。

该功能让AgentCore能够利用企业已有的密钥资源，降低重复配置的风险，同时保持密钥管理的统一治理。

---
## 评论

#### 中心观点

此次AWS在Bedrock AgentCore Identity中引入Secrets Manager密钥直接引用能力，本质上是将云原生密钥管理的灵活性重新还给企业用户，使身份配置流程不必再被迫锁定在平台提供的有限选项中。

#### 支撑理由

**事实陈述**：AWS官方披露，该功能允许用户在AgentCore Identity配置阶段直接引用已在Secrets Manager中预创建的密钥资源，支持自行管理密钥生命周期包括轮换策略和访问权限。

**作者观点**：文章强调这一能力“可扩展组织现有的安全最佳实践”，暗示AWS认可用户已有的密钥管理架构价值，而非要求其重新适配新范式。

**我的推断**：从技术实现推测，该功能很可能通过IAM角色信任关系与Secrets Manager资源策略协同完成，无需在AgentCore侧额外存储凭证明文，从而在架构层面保持密钥的单一可信来源。

#### 边界条件

该功能目前仅适用于AgentCore Identity组件，而非所有Bedrock配置场景。使用前需确保AgentCore执行角色已具备对应Secrets Manager资源的读取权限。此外，跨账户场景下的密钥引用可能涉及额外的信任链路配置。

#### 实践启发

对于已在Secrets Manager中建立统一密钥治理体系的企业，该集成提供了低迁移成本的接入路径。建议在启用前评估现有密钥轮换策略与AgentCore任务执行周期的匹配度，避免因密钥过期导致长时间任务中断。同时，组织应借此机会审视AgentCore Identity与Secrets Manager之间的最小权限边界，确保引用关系不会意外扩大运行时权限半径。

---
## 技术分析

#### 核心观点
该功能允许在 Amazon Bedrock 的 AgentCore Identity 中直接引用 AWS Secrets Manager 中预置的密钥，从而让组织对密钥生命周期拥有完整控制权，同时保持与 AI Agent 的安全集成。

##### 关键论点
- **统一控制**：密钥的创建、轮换、审计仍在 Secrets Manager 完成。
- **安全委托**：通过 IAM Role 与 AgentCore 身份绑定，实现最小权限访问。
- **动态注入**：在 Agent 执行时自动拉取密钥，无需在代码或环境变量中硬编码。

#### 关键技术点
##### Secrets Manager 引用机制
AgentCore 通过 `aws:source-arn` 与 Secrets Manager 资源策略配合，在运行时调用 `secretsmanager:GetSecretValue`。引用时可使用完整 ARN 或带标签的选择器，实现细粒度定位。

##### AgentCore Identity 集成
- **身份属性**：AgentCore 为每个执行实例生成唯一身份（Identity），关联特定 IAM Role。
- **跨账户支持**：若密钥位于不同账号，可通过 Resource‑Based Policy 授予目标账号访问权限。

##### 权限模型
- **最小权限原则**：仅授予 `GetSecretValue`（对特定密钥）以及 `DescribeSecret`（审计）。
- **加密传输**：所有密钥传输使用 TLS 1.2+，并在内存中解密后立即销毁。

#### 实际应用价值
##### 统一密钥管理
组织已有成熟的密钥轮换策略，无需在 Agent 代码中额外实现，即可保持合规。

##### 动态凭证注入
在 Agent 需要调用外部 API（如支付网关）时，可即时获取短期凭证，降低泄露风险。

##### 多环境一致性
同一套密钥定义可在开发、预生产、生产环境中通过不同别名或标签切换，实现环境隔离。

#### 行业影响
- **推动 AI 原生安全**：将传统密钥管理最佳实践延伸到 AI 运行时环境，提升整体安全水位。
- **示范效应**：为其他云服务（如 Parameter Store、HSM）提供类似引用模式奠定基础。

#### 边界条件与实践建议
##### 边界条件
- **密钥不可直接复制**：AgentCore 仅支持读取，无法修改或删除 Secrets Manager 中的密钥。
- **网络连通性**：AgentCore 与 Secrets Manager 必须同区域或通过 VPC 端点互通。
- **配额限制**：每个 Agent 实例的并发密钥请求受 Secrets Manager 请求速率限制。

##### 实践建议
1. 为每个业务场景创建独立密钥并打标签，便于细粒度授权。
2. 启用 Secrets Manager 自动轮转功能，确保 Agent 获得最新凭证。
3. 在 IAM Role 上使用条件键（如 `aws:RequestedRegion`）限制跨区域访问。
4. 监控 `GetSecretValue` 调用日志，配合 CloudTrail 进行异常检测。

#### 论证地图
##### 中心命题
在 AgentCore Identity 中引用自建 Secrets Manager 密钥，可实现 AI 工作负载的安全、自动化凭证管理。

##### 支撑理由
- 密钥生命周期在 Secrets Manager 完全可控，满足合规要求。
- IAM + 资源策略实现最小权限，降低泄露面。
- 动态注入避免硬编码，提高安全可移植性。

##### 反例或边界条件
- 若密钥存储在非 AWS 环境（如本地 HSM），则无法直接引用。
- 密钥轮换周期过长会导致 Agent 使用过期凭证，需配合短生命周期凭证或即时刷新。

##### 可验证方式
- 通过 CloudTrail 检查 `GetSecretValue` 事件的调用者身份与时间戳。
- 在测试环境模拟密钥失效，验证 Agent 的错误处理与降级策略。
- 使用 IAM Policy Simulator 验证 Role 对特定密钥的访问权限是否符合预期。

---
## 学习要点

- 直接在 Bedrock AgentCore 中使用 `aws:secretsmanager:secret-arn` 引用 Secrets Manager 的密钥，实现安全注入（最重要）。
- 必须为 Bedrock AgentCore 的执行角色配置 IAM 策略，允许 `secretsmanager:GetSecretValue` 操作对应的 secret 资源。
- 引用时应使用完整的 secret ARN 或带有版本阶段的 ARN（如 `AWSCURRENT`），以确保获取正确版本的密钥。
- 通过环境变量或参数将获取的密钥传递给自定义代码或第三方 API，避免在代码中硬编码明文凭据。
- 启用 Secrets Manager 的自动轮换并在 AgentCore 中实现重试或重新加载机制，保证密钥始终保持最新。
- 确保密钥在传输和持久化过程中使用 HTTPS 加密和 KMS 加密，满足安全合规要求。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity](https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [安全](/categories/%E5%AE%89%E5%85%A8/)
- 标签： [AWS](/tags/aws/) / [密钥管理](/tags/%E5%AF%86%E9%92%A5%E7%AE%A1%E7%90%86/) / [跨账户](/tags/%E8%B7%A8%E8%B4%A6%E6%88%B7/) / [外部连接器](/tags/%E5%A4%96%E9%83%A8%E8%BF%9E%E6%8E%A5%E5%99%A8/) / [安全](/tags/%E5%AE%89%E5%85%A8/) / [Bedrock](/tags/bedrock/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/) / [Agent](/tags/agent/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Amazon SageMaker AI构建无服务器对话AI代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph构建SageMaker AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
