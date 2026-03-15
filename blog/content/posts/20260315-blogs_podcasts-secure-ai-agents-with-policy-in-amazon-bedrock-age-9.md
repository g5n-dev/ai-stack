---
title: "利用 Amazon Bedrock AgentCore Policy 为 AI 代理实施确定性访问控制"
date: 2026-03-15T21:05:00+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "访问控制", "Cedar", "AI 代理", "身份认证", "运行时安全", "策略引擎"]
categories: ["安全", "AI 工程"]
source: blogs_podcasts
description: "本文介绍了 **Amazon Bedrock AgentCore** 中的 **Policy（策略）** 功能，旨在为 AI 智能体（Agent）提供安全、确定性的执行层。其核心在于将策略执行与智能体自身的推理过程解耦，确保系统严格遵循预设的业务规则。 **主要功能与实现方式：** 1. **从自然语言到 Cedar"
external_url: https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore
scenarios: ["AI/ML项目", "命令行工具"]
---

# 利用 Amazon Bedrock AgentCore Policy 为 AI 代理实施确定性访问控制

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:16:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)

---
## 摘要/简介

本文将带你了解 Amazon Bedrock AgentCore 中的 Policy 如何创建一个确定性的执行层，该层独立于 Agent 自身的推理能力运行。你将学习如何将业务规则的自然语言描述转换为 Cedar 策略，随后利用这些策略来实施细粒度且具备身份感知的访问控制，从而确保 Agent 仅访问其用户被授权使用的工具与数据。你还将看到如何通过 AgentCore Gateway 应用 Policy，在运行时拦截并评估每一份 Agent 发向工具的请求。

---
## 导语

构建具备自主决策能力的 AI Agent 往往伴随着权限失控的风险。本文将深入探讨 Amazon Bedrock AgentCore 中的 Policy 机制，解析如何通过构建一个独立于 Agent 推理能力的确定性执行层来解决这一安全隐患。你将学习如何将自然语言业务规则转换为 Cedar 策略，并利用 AgentCore Gateway 在运行时实施细粒度且具备身份感知的访问控制，从而确保 Agent 仅调用用户授权范围内的工具与数据。

---
## 摘要

本文介绍了 **Amazon Bedrock AgentCore** 中的 **Policy（策略）** 功能，旨在为 AI 智能体（Agent）提供安全、确定性的执行层。其核心在于将策略执行与智能体自身的推理过程解耦，确保系统严格遵循预设的业务规则。

**主要功能与实现方式：**

1.  **从自然语言到 Cedar 策略：**
    用户可以将自然语言描述的业务规则自动转换为 **Cedar 策略**。Cedar 是一种开源的语言，专为细粒度的权限控制而设计。

2.  **细粒度与身份感知控制：**
    通过这些策略，系统能够实施精细化的访问控制。这意味着 AI 智能体只能调用那些当前用户经过授权的工具和数据，从而有效防止越权访问。

3.  **运行时拦截与评估：**
    Policy 功能通过 **AgentCore Gateway** 进行应用。它会在运行时拦截智能体发出的每一个工具调用请求，并根据预设策略进行实时评估和裁决。

**总结：**
Amazon Bedrock AgentCore 的 Policy 功能通过独立的确定性执行层，将业务规则转化为代码，并在运行时强制执行身份感知的访问控制，确保了 AI 智能体在操作工具和数据时的安全性与合规性。

---
## 技术分析

基于您提供的文章标题《Secure AI agents with Policy in Amazon Bedrock AgentCore》及其摘要，以下是对该技术方案的深度全面分析。

---

# 深度分析：基于 Amazon Bedrock AgentCore Policy 的 AI 代理安全架构

## 1. 核心观点深度解读

**主要观点**
文章的核心观点在于：**AI 智能体的安全性不能仅依赖于模型本身的对齐或推理能力，必须在架构层面引入一个独立的、确定性的强制执行层。** Amazon Bedrock AgentCore 引入的 Policy 机制，本质上是在概率性的 LLM（大语言模型）推理层之外，包裹了一层基于逻辑的硬约束。

**核心思想**
作者试图传达“控制平面与数据平面分离”的思想在 AI 时代的演进。传统的 AI Agent 是“自主思考+自主行动”的闭环，这带来了不可控的风险。Bedrock AgentCore 的 Policy 功能主张将“业务规则”从“提示词”中剥离出来，利用 Cedar 策略语言构建一个独立运行的“守门人”。即使 Agent 被诱导产生了有害意图，Policy 层也能作为最后一道防线，基于确定性逻辑拦截违规操作。

**观点的创新性与重要性**
*   **创新性**：将自然语言策略直接转化为可执行的代码策略，降低了安全治理的门槛。这不仅仅是简单的 API 过滤，而是引入了细粒度的属性基访问控制（ABAC）逻辑到 Agent 的决策链中。
*   **重要性**：随着 Agent 从“聊天机器人”进化为“行动机器人”，其拥有调用 API、修改数据库的权限。一旦失控，后果不仅是“乱说话”，而是“乱操作”。这种确定性层是企业级应用 AI 的必要安全前提。

## 2. 关键技术要点

**涉及的关键技术**
*   **Amazon Bedrock AgentCore**：AWS 提供的构建和管理 AI Agent 的核心框架。
*   **Cedar**：AWS 开源的一种用于编写权限策略的语言，专为表达资源、主体和动作之间的关系而设计。
*   **Deterministic Enforcement Layer（确定性执行层）**：与 LLM 的概率性生成不同，该层基于布尔逻辑执行，结果是确定的（Yes/No）。
*   **Natural Language to Policy (NL2Policy)**：利用 LLM 将人类可读的业务规则转换为 Cedar 代码的转换过程。

**技术原理与实现方式**
1.  **定义边界**：开发者首先定义 Agent 可以访问的资源（如数据库、API）和操作。
2.  **规则转化**：用户用自然语言描述规则（例如：“只有经理级别的员工可以查看工资单”）。系统利用 LLM 生成对应的 Cedar Policy 代码。
3.  **运行时拦截**：当 Agent 推理出需要执行某个工具（Tool）时，请求不会直接发送给后端服务，而是先经过 AgentCore 的 Policy 评估器。
4.  **属性校验**：评估器检查当前上下文（用户角色、环境、资源属性）是否满足 Cedar 策略。如果满足，请求通过；否则，直接拒绝并返回错误，无需 LLM 再次介入。

**技术难点与解决方案**
*   **难点**：LLM 生成的 Cedar 代码可能存在逻辑漏洞或语法错误。
*   **解决方案**：通常采用“生成-验证-修正”的闭环，或者提供经过严格测试的模板库，确保生成的策略是安全且符合预期的。
*   **难点**：上下文属性的实时提取。
*   **解决方案**：AgentCore 需要与企业的身份认证系统（如 IAM、LDAP）深度集成，以便在运行时获取用户的实时属性。

## 3. 实际应用价值

**对实际工作的指导意义**
这标志着 AI 治理从“软约束”（Prompt Engineering）转向“硬约束”（Code Enforcement）。对于企业架构师而言，这意味着可以像管理传统 API 权限一样管理 AI Agent 的权限，无需担心 Prompt 注入导致的数据泄露。

**可应用场景**
*   **金融交易 Agent**：限制 Agent 只能查询股票信息，严禁执行超过一定金额的转账操作，除非满足多重签名策略。
*   **企业知识库助手**：基于文档的机密级别（如“绝密”、“机密”）和用户的部门权限，动态过滤 Agent 检索的内容。
*   **医疗诊断辅助**：确保 Agent 只能“建议”而不能“开具处方”，且必须遵守 HIPAA 等数据隐私法规。

**实施建议**
*   **最小权限原则**：默认拒绝所有访问，仅根据业务需求开启必要的最小权限。
*   **策略版本控制**：将生成的 Cedar 策略纳入 Git 版本管理，进行 Code Review。

## 4. 行业影响分析

**对行业的启示**
Bedrock AgentCore 的这一举措可能成为行业标配。未来，AI Agent 编排框架（如 LangChain, AutoGen 等）若想进入企业级市场，必须内置类似 RBAC/ABAC 的强制策略执行层。

**可能带来的变革**
*   **DevSecAI 的兴起**：安全团队将直接参与 AI Agent 的开发流程，编写安全策略将成为核心工作流。
*   **合规性自动化**：通过将法律条文转化为 Cedar 策略，企业能够更直观地向审计机构证明其 AI 系统符合合规要求（如 GDPR 的“被遗忘权”可通过策略立即生效）。

## 5. 延伸思考

**引发的思考**
*   **策略冲突**：当自然语言描述模糊，导致生成的 Cedar 策略之间存在冲突时，系统如何解决？
*   **对抗性鲁棒性**：如果攻击者通过精心构造的上下文欺骗了“NL2Policy”的生成过程，生成了恶意策略怎么办？
*   **性能开销**：在每一次 Agent 动作前增加策略评估，会增加系统的延迟。对于高频交易等场景，这毫秒级的延迟是否可接受？

**未来趋势**
未来可能会看到“策略即代码”市场的繁荣，第三方公司可能会出售针对特定行业（如医疗、金融）预打包的 Cedar 策略库。

## 6. 实践建议

**如何应用到自己的项目**
1.  **审计现有 Agent**：检查现有项目中的 Agent 是否拥有不受限制的 API 访问权限。
2.  **引入中间件思维**：即使不使用 Bedrock，也可以在 LangChain 等框架中自行实现一个“Pre-Handler”钩子，在工具调用前执行简单的逻辑判断。
3.  **学习 Cedar 语言**：团队中需要有人掌握 Cedar 的语法，以便审核 LLM 生成的策略。

**注意事项**
*   不要完全信任 LLM 生成的策略代码，必须进行人工审核。
*   策略的粒度不能太粗，否则会限制 Agent 的能力；也不能太细，否则维护成本过高。

## 7. 案例分析

**成功案例设想：银行客服 Agent**
*   **场景**：用户询问转账。
*   **无 Policy**：Agent 可能被社会工程学攻击，直接转账给黑客账户。
*   **有 Policy**：Agent 生成转账意图 -> AgentCore 拦截 -> 检查 Cedar 策略（规则：收款账户必须不在黑名单 AND 金额 < 单日限额）。如果违规，Policy 直接拒绝，Agent 收到拒绝信号，转而告知用户原因。

**失败案例反思**
*   **过度依赖**：如果开发者认为有了 Policy 就可以放松对 Prompt 的安全设计，可能会遇到“拒绝服务”的情况。例如，策略过于严格，导致合法的用户请求也被频繁拦截，严重影响用户体验。

## 8. 哲学与逻辑：论证地图

**中心命题**
在生成式 AI 架构中，**必须**在模型推理层之外部署独立的确定性策略执行层，以保障系统安全。

**支撑理由与依据**
1.  **LLM 的本质缺陷**：大语言模型是基于概率预测的， inherently 存在幻觉和不可控性。
    *   *依据*：无数的研究表明，Prompt Injection 攻击可以绕过系统提示词。
2.  **责任归属**：企业应用需要符合合规性要求，合规性是基于逻辑规则（如 GDPR），而非基于“模型的善意”。
    *   *依据*：金融和医疗行业的法律条文。
3.  **纵深防御**：单一的安全防线（Prompt）是不够的，需要多层防御。
    *   *依据*：网络安全领域的标准最佳实践。

**反例与边界条件**
1.  **边界条件**：对于完全离线、无高危操作（仅限文本生成）的个人玩具 Agent，引入复杂的 Cedar 策略可能属于过度设计。
2.  **反例风险**：如果策略编写不当（例如逻辑死锁），可能会导致 Agent 在处理边缘情况时彻底瘫痪，即使模型本身知道如何处理。

**命题性质分类**
*   **事实**：LLM 是概率性的，非确定性的。
*   **价值判断**：企业应用的安全性比 Agent 的执行效率或自主性更重要。
*   **可检验预测**：采用独立策略层的 AI 系统，在对抗性攻击测试中的通过率将显著高于仅依赖 Prompt 的系统。

**立场与验证**
*   **立场**：坚决支持引入独立策略层。这是 AI 从“玩具”走向“工具”的关键一步。
*   **验证方式（可证伪）**：
    *   *实验*：构建两个相同的 Agent，A 仅用 Prompt 限制，B 使用 Bedrock Policy 限制。使用红队测试集进行攻击。
    *   *指标*：记录违规操作的成功率。如果在 100 次 SQL 注入尝试中，A 成功 30 次，而 B 成功 0 次，则命题成立。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的输入输出边界

**说明**: 利用 Amazon Bedrock Guardrails 作为 Agent 的第一道防线。通过配置敏感信息过滤、有害内容检测和主题拒绝策略，确保 Agent 不会处理或生成违反安全策略的内容。这是防止提示词注入和恶意输入的基础。

**实施步骤**:
1. 在 Amazon Bedrock 控制台中创建 Guardrail。
2. 配置拒绝主题，定义 Agent 不应讨论的领域。
3. 设置敏感信息过滤器（如 PII、凭证等）以防止数据泄露。
4. 将创建的 Guardrail 关联到 Agent 的 Alias 或特定版本上。

**注意事项**: Guardrail 的配置应在模型推理之前生效，确保即使模型被诱导，也能在输出阶段被拦截。

---

### 实践 2：定义精细化的作用域和上下文限制

**说明**: 明确 Agent 的职责边界，防止其执行超出预定范围的行动。通过在系统提示词或 Agent 配置中严格限制其可访问的工具和知识库范围，减少“越狱”风险。

**实施步骤**:
1. 在 Agent 配置阶段，仅启用完成任务所必需的最小工具集。
2. 在系统提示词中明确指出 Agent 的限制和禁止执行的操作。
3. 限制 Agent 访问的 Lambda 函数或 API 的权限（遵循最小权限原则）。

**注意事项**: 定期审查 Agent 的工具列表，移除不再需要或高风险的工具调用权限。

---

### 实践 3：强化工具调用的授权与验证

**说明**: Agent 执行动作（如调用 Lambda 函数或 API）是风险最高的环节。必须确保每次工具调用都经过严格的身份验证和授权检查，防止 Agent 被利用来攻击下游系统。

**实施步骤**:
1. 为 Agent 分配具有最小权限的 IAM 角色。
2. 在被调用的 Lambda 函数或 API 内部实施额外的逻辑验证（如参数校验、业务权限检查）。
3. 确保工具的输入模式定义严格，不接受任意格式的参数。

**注意事项**: 不要仅仅依赖 Agent 的判断，后端服务必须具备独立的防御能力，假设 Agent 的请求可能已被篡改。

---

### 实践 4：配置上下文感知的会话策略

**说明**: 利用会话控制机制限制 Agent 的记忆长度和上下文窗口。防止攻击者通过长对话历史将恶意指令“注入”到 Agent 的上下文中，或者通过消耗大量 Token 导致服务拒绝。

**实施步骤**:
1. 设置合理的会话超时时间。
2. 限制传递给模型的上下文窗口大小，仅保留最近几轮的关键对话。
3. 对用户上传的文档或检索到的知识库片段进行预处理，过滤掉其中的潜在恶意脚本。

**注意事项**: 在多轮对话中，要警惕“渐进式提示词注入”，即攻击者逐步引导 Agent 放弃安全限制。

---

### 实践 5：建立全面的监控与审计日志

**说明**: 安全是一个持续的过程，必须对所有 Agent 交互进行记录。通过 CloudTrail 和 CloudWatch 监控异常行为，以便在发生安全事件时进行溯源和快速响应。

**实施步骤**:
1. 启用 Amazon Bedrock 的数据日志记录功能，记录模型输入和输出。
2. 配置 CloudWatch 告警，监控诸如高频拒绝率、异常敏感词触发或异常 API 调用模式。
3. 定期审查日志，寻找潜在的安全漏洞或提示词攻击尝试。

**注意事项**: 确保日志数据的存储和访问本身也是安全的，防止日志泄露导致二次敏感信息泄露。

---

### 实践 6：执行红队测试与持续验证

**说明**: 部署前必须对 Agent 进行对抗性测试。模拟攻击者的行为，尝试绕过 Guardrail 和策略限制，以发现防御体系的盲点。

**实施步骤**:
1. 构建包含提示词注入、角色扮演和越狱尝试的测试数据集。
2. 在预生产环境中运行这些测试用例，观察 Agent 的响应。
3. 根据测试结果调整 Guardrail 阈值和系统提示词。
4. 在模型更新或 Agent 配置变更后重复此过程。

**注意事项**: 安全威胁不断演变，应将红队测试纳入 CI/CD 流程，而不仅仅是一次性的检查。

---
## 学习要点

- Amazon Bedrock AgentCore 引入了一种基于策略的机制，允许通过可自定义的“护栏”来限制 AI 智能体的行为，确保其操作符合企业安全和合规标准。
- 该架构将核心推理逻辑与安全策略执行分离，使得开发者能够在不修改底层代码的情况下，灵活地更新或调整安全规则。
- 策略引擎能够对智能体的工具调用和最终输出进行实时拦截与过滤，有效防止敏感数据泄露或生成有害内容。
- 平台支持对特定工具或 API 端点实施精细化的访问控制，确保智能体仅被授权执行预定义范围内的操作。
- 企业可利用此功能建立统一的治理框架，在加速 AI 应用部署的同时，将安全风险降至最低并满足监管要求。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [访问控制](/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/) / [Cedar](/tags/cedar/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/) / [运行时安全](/tags/%E8%BF%90%E8%A1%8C%E6%97%B6%E5%AE%89%E5%85%A8/) / [策略引擎](/tags/%E7%AD%96%E7%95%A5%E5%BC%95%E6%93%8E/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [构建安全的 Amazon Bedrock 代理：利用 AgentCore Policy 实现细粒度访问控制]({{< relref "posts/20260312-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-2.md" >}})
- [利用 Amazon Bedrock AgentCore Policy 实现安全访问]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-3.md" >}})
- [构建安全的 Amazon Bedrock 智能体：利用 AgentCore Policy 实现工具调用合规]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-5.md" >}})
- [利用 Amazon Bedrock AgentCore Policy 构建 AI Agent 确定性执行层]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-9.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*