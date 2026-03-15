---
title: "利用 Amazon Bedrock AgentCore Policy 构建 AI Agent 确定性执行层"
date: 2026-03-14T23:04:01+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "AI Agent", "Cedar", "访问控制", "确定性执行", "策略引擎", "运行时拦截"]
categories: ["AI 工程", "安全"]
source: blogs_podcasts
description: "本文介绍了 Amazon Bedrock AgentCore 中的 Policy（策略）功能，旨在解决 AI 智能体（AI Agents）在执行任务时的安全与控制问题。 **核心概念与原理** AgentCore 引入了一个**确定性的执行层**，该层独立于智能体自身的推理过程运行。这意味着无论 AI 模型如何生成请求"
external_url: https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore
scenarios: ["AI/ML项目", "命令行工具"]
---

# 利用 Amazon Bedrock AgentCore Policy 构建 AI Agent 确定性执行层

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:16:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)

---
## 摘要/简介

在本文中，你将了解 Amazon Bedrock AgentCore 中的 Policy 如何构建一个独立于 Agent 自身推理的确定性执行层。你将学习如何将业务规则的自然语言描述转化为 Cedar 策略，进而利用这些策略实施细粒度、具备身份感知的管控，从而确保 Agent 仅能访问其用户被授权使用的工具和数据。你还将看到如何通过 AgentCore Gateway 应用 Policy，在运行时拦截并评估每一个 Agent 对工具的请求。

---
## 导语

随着 AI Agent 深入企业核心业务，如何确保其行为符合安全规范成为关键挑战。本文介绍 Amazon Bedrock AgentCore 中的 Policy 功能，它通过构建独立于 Agent 推理的确定性执行层，实现了细粒度、具备身份感知的权限管控。阅读本文，你将掌握如何将自然语言规则转化为 Cedar 策略，并利用 Gateway 在运行时精准拦截未授权的工具调用，从而在赋予 Agent 自主能力的同时，确保数据访问的合规与安全。

---
## 摘要

本文介绍了 Amazon Bedrock AgentCore 中的 Policy（策略）功能，旨在解决 AI 智能体（AI Agents）在执行任务时的安全与控制问题。

**核心概念与原理**
AgentCore 引入了一个**确定性的执行层**，该层独立于智能体自身的推理过程运行。这意味着无论 AI 模型如何生成请求，系统都会通过预设的策略强制执行规则，从而确保智能体行为符合企业规范。

**功能与实现**
1.  **规则转换**：用户可以用**自然语言**描述业务规则，系统会自动将其转换为 **Cedar 策略**代码。
2.  **细粒度控制**：这些策略支持基于身份的细粒度控制，确保智能体仅能访问用户被授权使用的特定工具和数据。
3.  **运行时拦截**：通过 **AgentCore Gateway** 应用策略，系统会在运行时拦截并评估每一个智能体对工具的请求，防止未经授权的操作。

**总结**
简而言之，该功能通过将自然语言规则转化为强制执行的代码策略，并在请求路径上进行实时拦截，为企业级 AI 智能体提供了一套安全、可控且符合权限管理的运行机制。

---
## 技术分析

基于您提供的文章标题《Secure AI agents with Policy in Amazon Bedrock AgentCore》及其摘要，以下是对该技术方案的深度分析。

---

# 1. 核心观点深度解读

**主要观点**
文章的核心观点是：**AI 智能体的安全性不应依赖于模型自身的不确定性推理，而应通过外部的、确定性的策略层进行强制执行。** Amazon Bedrock AgentCore 引入的 Policy 功能，旨在构建一个独立的“护栏”，确保即使 Agent 产生幻觉或试图执行越权操作，系统也能依据预设规则进行拦截。

**核心思想**
作者传达了“控制与推理分离”的设计哲学。在生成式 AI（GenAI）应用中，模型的概率性本质（即每次输出可能不同）与商业合规的确定性要求之间存在天然矛盾。通过引入 Cedar 策略语言，将自然语言描述的业务规则转化为代码逻辑，形成了一个独立于 Agent 推理过程的强制执行层。

**创新性与深度**
该观点的创新性在于**解耦**。传统的 AI 安全往往依赖 Prompt Engineering（提示词工程），如“请不要做X”，这是一种软约束，极易被模型忽略或通过“越狱”攻击绕过。而 Bedrock AgentCore 的方案引入了硬约束，类似于操作系统的内核态权限检查。其深度在于它承认了 LLM（大语言模型）作为“逻辑引擎”的不可靠性，转而使用形式化验证的方法来处理权限和合规问题。

**重要性**
随着 AI Agent 从“聊天机器人”进化为“行动者”，能够自主调用 API、修改数据库或转账，错误的代价急剧上升。这种确定性执行层是企业级 AI 落地的“安全带”，解决了企业不敢放手让 Agent 执行关键任务的核心痛点。

# 2. 关键技术要点

**关键技术概念**
1.  **Amazon Bedrock AgentCore**：AWS 提供的构建 AI Agent 的框架核心。
2.  **Cedar**：AWS 开源的一种针对通用资源的策略描述语言，专为细粒度授权设计。
3.  **确定性执行层**：一个中间件层，它在 Agent 的行动指令到达实际服务（如 S3, DynamoDB）之前进行拦截。

**技术原理与实现**
技术实现流程通常分为三步：
1.  **规则定义**：开发者用自然语言书写业务规则（例如：“只有经理可以批准超过 $1000 的退款”）。
2.  **转化与编码**：将这些规则转化为 Cedar 策略代码。例如：
    ```cedar
    permit(principal, action, resource) when {
        resource.amount < 1000 || principal.role == "Manager"
    };
    ```
3.  **运行时拦截**：当 LLM 生成一个工具调用请求（Action）时，AgentCore 不会直接执行，而是将请求上下文传递给 Policy Evaluator（策略评估器）。如果评估结果为 `Deny`，则直接拦截并返回错误，不再调用下游 API。

**技术难点与解决方案**
*   **难点**：LLM 输出的非结构化与策略引擎的结构化输入之间的鸿沟。LLM 可能说“我想帮他退款”，而不是明确的 JSON 指令。
*   **方案**：利用 Bedrock 的 Orchestrator（编排器）强制 LLM 输出结构化的意图，并将用户上下文（如属性、角色）提取为标准化的 Token 传递给 Cedar。

**技术创新点**
将自然语言处理（NLP）与基于逻辑的访问控制（ABAC/RBAC）无缝结合。这不仅仅是 API 网关，因为它理解 Agent 的“意图”和“上下文”，能够进行基于语义的动态权限判断。

# 3. 实际应用价值

**对实际工作的指导意义**
这为 AI 工程师提供了一种**“零信任”**的架构范式。在开发 Agent 时，不需要花费大量精力去微调模型以“学会”遵守规则，而是通过配置策略来保证底线安全。这极大地降低了合规成本和模型调试的难度。

**应用场景**
1.  **金融科技**：Agent 查阅财报时，自动应用数据脱敏策略（如：Agent 不能向非授权用户展示完整的信用卡号）。
2.  **企业办公**：Copilot 类 Agent 在处理邮件和文件时，严格执行 ACL（访问控制列表），防止将机密邮件摘要发给普通员工。
3.  **电商运营**：自动化的客服 Agent 可以退款，但必须限制退款金额上限和频次，防止被恶意用户利用 Agent 进行套利。

**需要注意的问题**
策略的编写本身具有复杂性。如果 Cedar 策略写得太严格，Agent 会变得“什么都不敢做”；写得太松，则失去防御作用。此外，策略的版本管理和与业务代码的同步也是挑战。

**实施建议**
采用“最小权限原则”初始化策略。先允许 Agent 只读，随着信任建立和策略完善，再逐步开放写权限。

# 4. 行业影响分析

**对行业的启示**
这标志着 AI 安全从“模型对齐”向“系统架构对齐”的转变。行业将意识到，仅仅依靠 RLHF（基于人类反馈的强化学习）是不够的，必须回归到传统的计算机科学安全原则（如最小权限、强制访问控制）来约束 AI。

**可能带来的变革**
未来，AI Agent 的开发栈将标配“策略层”。类似于 Web 开发必须有防火墙和 WAF，AI Agent 开发也将标配 Policy Engine。这将催生“AI 策略工程师”这一新角色，他们不需要懂模型训练，但需要精通业务逻辑和安全策略语言。

**相关领域发展趋势**
*   **Governance as Code（治理即代码）**：业务合规规则将像软件代码一样被版本控制、审查和测试。
*   **可解释性安全**：当 Agent 拒绝执行操作时，系统可以明确指出是违反了哪一条 Cedar 策略，比黑盒模型的拒绝更具可解释性。

# 5. 延伸思考

**引发的思考**
如果 Policy 层足够强，我们是否还需要在 Prompt 中加入大量的安全提示词？这可能导致 Prompt 极大简化，让 Token 消耗更高效。

**拓展方向**
*   **动态策略**：策略能否根据 Agent 的“置信度”动态调整？例如，如果 LLM 对某个操作的置信度很低，Policy 层自动提升验证等级（如要求二次验证）。
*   **跨 Agent 策略**：当多个 Agent 协作时，如何防止 Agent A 利用 Agent B 绕过自己的权限限制（类似于提权攻击）？

**未来研究问题**
如何利用 LLM 自动生成 Cedar 策略？即实现从“员工手册”直接到“可执行安全代码”的自动化转换。

# 6. 实践建议

**如何应用到项目中**
1.  **审计现有 Agent**：检查当前你的 AI 应用中，哪些操作涉及敏感数据或写入权限。
2.  **定义边界**：明确列出 Agent 绝对不能做的事（如：删除数据、发送邮件给外部人员）。
3.  **引入 Cedar**：在 AWS Lambda 或 Bedrock 的逻辑流中，先构建策略验证逻辑，再连接模型输出。

**具体行动建议**
*   学习 Cedar 语法（它与 Python/Ruby 类似，上手快）。
*   在 Bedrock 控制台中开启 Agent 的“Guardrail”或“Policy”配置选项。
*   编写单元测试，模拟 Agent 发出恶意指令，验证策略层是否成功拦截。

**补充知识**
需要了解 ABAC（基于属性的访问控制）模型，因为 Cedar 主要基于此模型（Principal, Action, Resource, Context）。

# 7. 案例分析

**成功案例设想：某银行智能贷款助手**
*   **场景**：Agent 协助员工查看客户贷款状态。
*   **策略**：`permit(principal, action, resource) when { principal.branch == resource.branch }`。
*   **效果**：即使 LLM 理解错误，或者用户诱导 Agent 说“帮我看看隔壁分行的机密数据”，AgentCore 在执行 API 查询前，会检查当前员工的分支机构属性与目标数据的分支机构属性，不匹配则直接拒绝。这成功防止了内部数据泄露。

**失败案例反思**
*   **情况**：策略定义过于依赖 LLM 提取的 `Context`。
*   **问题**：如果 LLM 误将用户身份识别为“Admin”（例如解析错误），且策略层完全信任 LLM 传入的上下文，那么策略层就会形同虚设。
*   **教训**：**永远不要信任 Agent 传来的身份声明**。策略层必须从可信的 IAM 系统中获取 Principal 信息，而不是从 LLM 的生成文本中获取。

# 8. 哲学与逻辑：论证地图

**中心命题**
**在生成式 AI 架构中，必须引入独立于模型推理之外的确定性策略执行层（如 Cedar Policy），才能实现企业级的安全与合规。**

**支撑理由与依据**
1.  **理由 1：模型本质的不可靠性**
    *   依据：LLM 是概率模型，存在幻觉和“越狱”风险，Prompt Engineering 无法提供 100% 的安全保证。
2.  **理由 2：业务合规的确定性要求**
    *   依据：金融、医疗等行业的法规（如 SOX, HIPAA）要求逻辑必须是可验证、可审计且确定性的，这是概率模型无法直接满足的。
3.  **理由 3：责任归属的清晰化**
    *   依据：当违规操作发生时，通过代码策略（Cedar）可以精确定位是哪条规则被绕过或缺失，比分析黑盒模型的神经元更符合工程审计要求。

**反例或边界条件**
1.  **反例：非关键创意场景**
    *   在生成图片、写诗等非执行类、非敏感场景下，引入复杂的策略层可能过度设计，增加延迟且无必要。
2.  **边界条件：策略本身的漏洞**
    *   如果策略编写本身存在逻辑漏洞（如死循环或权限过大），那么“确定性执行”只会“确定地”执行错误操作。策略层不能解决逻辑设计错误的问题。

**命题性质分析**
*   **事实**：LLM 输出具有随机性；Cedar 语言具有确定性。
*   **价值判断**：确定性优于概率性（在安全领域）。
*   **可检验预测**：采用此架构的 AI 系统，其越权操作的成功率将显著低于仅依赖 Prompt 的系统。

**立场与验证**
*   **立场**：支持将 Policy 作为 AI Agent 的标准安全组件。
*   **验证方式（可证伪）**：
    *   **红队测试**：构建一组诱导 Agent 执行越权操作的 Prompt。对比“仅用 Prompt”和“Prompt + Policy”两种架构，统计违规拦截率。如果 Policy 架构的拦截率没有显著高于对照组，则该命题失效。
    *   **观察窗口**：观察未来 1-2 年主流企业级 AI 平台（如 Azure, Google）是否跟进类似的“外部策略层”设计。如果行业未跟进，说明该观点可能存在工程上的过度复杂性问题。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的输入输出边界防护

**说明**: 利用 Guardrails for Amazon Bedrock 在 AI 代理的数据输入和输出阶段建立多层防御。这不仅能防止恶意提示词注入，还能过滤包含个人身份信息 (PII)、仇恨言论或有害内容的响应，确保代理始终在安全边界内运行。

**实施步骤**:
1. 在 Amazon Bedrock 控制台中创建一个新的 Guardrail。
2. 配置“拒绝过滤器”，定义敏感主题、关键词和正则表达式模式。
3. 启用 PII 编辑功能，自动屏蔽输出中的敏感数据。
4. 将该 Guardrail 关联到 Agent 的 Alias 配置中。

**注意事项**: 定期审查并更新拒绝主题和关键词列表，以适应新的安全威胁和业务需求变化。

---

### 实践 2：应用细粒度的访问控制策略

**说明**: 确保 AI 代理仅拥有执行任务所需的最小权限。通过精细的 IAM (Identity and Access Management) 策略，限制代理只能访问特定的 S3 存储桶、DynamoDB 表或特定的 API 端点，防止权限被滥用。

**实施步骤**:
1. 为每个 Agent 创建专用的 IAM 角色。
2. 在 IAM 策略中明确指定允许调用的 Action 和 Resource（例如 `arn:aws:s3:::specific-bucket/*`）。
3. 避免使用 `*` 通配符授予广泛的管理员权限。
4. 利用 IAM Conditions Condition Keys 进一步限制请求来源（如 VPC 端点）。

**注意事项**: 遵循“最小权限原则”，并在代理部署前使用 IAM Access Analyzer 验证权限设置。

---

### 实践 3：建立上下文感知的会话策略

**说明**: 针对涉及敏感数据的场景，实施基于会话上下文的动态策略。通过分析对话的意图和上下文，实时调整安全策略。例如，当检测到用户试图绕过安全机制或进行异常操作时，动态触发更严格的验证流程。

**实施步骤**:
1. 在 Agent 的 Lambda 函数中集成上下文分析逻辑。
2. 利用 Amazon Bedrock 的 Orchestrator trace 数据监控对话流。
3. 配置基于上下文的阻断规则，例如当连续出现多次敏感词查询时自动终止会话。
4. 记录所有上下文切换和策略触发事件到 CloudTrail。

**注意事项**: 确保上下文分析逻辑不会导致过多的误报，影响正常用户体验。

---

### 实践 4：强化工具调用的安全验证

**说明**: AI 代理通常通过调用外部工具（API、Lambda 函数）来执行操作。必须在代码层面严格验证传递给这些工具的参数，防止通过提示词注入导致的数据泄露或未授权操作（如删除文件、发送邮件）。

**实施步骤**:
1. 在 Lambda 函数或 API 网关层实施严格的参数模式验证。
2. 对所有输入参数进行清洗，移除潜在的命令注入代码。
3. 为关键操作（如写入数据库、调用外部 API）添加额外的确认步骤或二次验证机制。
4. 限制工具调用的频率，防止暴力扫描或拒绝服务攻击。

**注意事项**: 不要仅依赖 Agent 的提示工程来保证安全，后端代码必须假设输入是不可信的。

---

### 实践 5：启用全面的审计与可观测性

**说明**: 利用 Amazon CloudWatch 和 AWS CloudTrail 记录代理的所有活动。这不仅有助于故障排查，还能用于安全审计，确保代理的行为符合合规性要求，并能快速发现异常模式。

**实施步骤**:
1. 确保 Bedrock Agent 的日志记录已启用，并将日志发送到 Amazon CloudWatch Logs。
2. 配置 CloudTrail 以捕获所有管理事件和数据事件。
3. 创建 CloudWatch 告警，用于监控异常指标，如错误率激增、敏感词频繁出现或异常的 API 调用模式。
4. 定期导出日志到 S3 进行长期归档和合规性审计。

**注意事项**: 确保日志存储本身的安全，防止日志被篡改，并在日志中屏蔽敏感的用户数据。

---

### 实践 6：实施提示词注入检测与防御

**说明**: 针对大语言模型特有的提示词注入攻击，利用模型自身的推理能力或外部检测机制来识别恶意指令。确保代理不会因为精心设计的恶意输入而泄露系统指令或执行有害操作。

**实施步骤**:
1. 在系统提示词中明确指令边界，禁止代理执行超出定义范围的任务。
2. 利用 Bedrock Guardrails 中的“上下文接地”检查，确保回答基于提供的可信参考资料。
3. 对于高风险操作，引入“人机协作”模式，要求人工审批关键操作。
4. 定期进行红队测试，模拟攻击者的提示词注入尝试。

**注意事项**: 提示词工程是动态的，需要随着模型能力的提升和攻击手段的演变不断调整防御策略。

---
## 学习要点

- Amazon Bedrock AgentCore 引入了基于策略的访问控制机制，允许开发者通过精细化的权限管理来规范 AI 智能体对工具和 API 的调用，从而有效防止未经授权的操作。
- 该框架支持在策略中定义严格的输入输出限制（例如拒绝处理包含敏感个人身份信息 PII 的数据），确保 AI 智能体在处理敏感数据时符合合规性要求。
- 通过在策略中嵌入“拒绝模式”或“允许模式”，开发者可以明确限制智能体只能执行特定的业务逻辑，显著降低了 AI 产生幻觉或执行意外指令带来的安全风险。
- 新的架构将安全策略与核心业务逻辑解耦，使得安全团队可以独立于应用开发流程来更新和审计安全规则，提高了治理效率。
- 借助 Bedrock 原生的可观测性工具，管理员可以实时监控智能体的行为是否符合预设策略，并能够追溯具体的决策路径以满足审计需求。
- 此安全模型支持跨多个智能体应用复用通用的安全策略，简化了在大规模部署 AI 智能体时的安全管理复杂度。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [安全](/categories/%E5%AE%89%E5%85%A8/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [AI Agent](/tags/ai-agent/) / [Cedar](/tags/cedar/) / [访问控制](/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/) / [确定性执行](/tags/%E7%A1%AE%E5%AE%9A%E6%80%A7%E6%89%A7%E8%A1%8C/) / [策略引擎](/tags/%E7%AD%96%E7%95%A5%E5%BC%95%E6%93%8E/) / [运行时拦截](/tags/%E8%BF%90%E8%A1%8C%E6%97%B6%E6%8B%A6%E6%88%AA/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-8.md" >}})
- [利用 Amazon Bedrock AgentCore Policy 实现安全访问]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-3.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore Policy 管控 AI Agent]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
- [构建安全的 Amazon Bedrock 代理：利用 AgentCore Policy 实现细粒度访问控制]({{< relref "posts/20260312-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*