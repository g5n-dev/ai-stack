---
title: 利用 Amazon Bedrock AgentCore Policy 精细化管控 AI Agent 工具访问
date: 2026-03-16 16:46:26+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- AI Agent
- Cedar 策略
- 访问控制
- 工具调用
- 运行时拦截
- 身份感知
categories:
- 安全
- AI 工程
source: blogs_podcasts
description: 本文介绍了如何利用 Amazon Bedrock AgentCore 中的 Policy 功能，为 AI 代理构建安全且确定性的执行层。核心要点如下：
  1. **构建独立执行层**：Policy 创建了一个独立于 Agent 自身推理逻辑之外的确定性强制执行层，确保无论 Agent 如何决策，安全规则始终被优先执行。
external_url: https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore
scenarios:
- AI/ML项目
- 命令行工具
---

# 利用 Amazon Bedrock AgentCore Policy 精细化管控 AI Agent 工具访问

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:16:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)

---

## 摘要/简介

在本文中，你将了解 Amazon Bedrock AgentCore 中的 Policy 如何创建一个确定性的执行层，该层独立于 Agent 自身的推理能力运行。你将学习如何将业务规则的自然语言描述转化为 Cedar 策略，并利用这些策略实施细粒度、具备身份感知的管控，确保 Agent 仅访问其用户有权使用的工具与数据。你还将看到如何通过 AgentCore Gateway 应用 Policy，在运行时拦截并评估每一个 Agent 针对工具的请求。

---

## 导语

随着 Amazon Bedrock Agent 的应用场景不断拓展，如何确保其行为严格遵循业务规范与权限边界，已成为构建安全系统的关键挑战。本文将深入解析 Amazon Bedrock AgentCore 的 Policy 机制，探讨如何利用 Cedar 策略语言构建独立于 Agent 推理能力的确定性执行层。我们将介绍如何将自然语言规则转化为细粒度的管控策略，并通过 AgentCore Gateway 在运行时精准拦截并评估请求，从而确保 Agent 仅访问用户授权范围内的工具与数据，实现安全可控的智能体应用。

---

## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 中的 Policy 功能，为 AI 代理构建安全且确定性的执行层。核心要点如下：

1.  **构建独立执行层**：Policy 创建了一个独立于 Agent 自身推理逻辑之外的确定性强制执行层，确保无论 Agent 如何决策，安全规则始终被优先执行。
2.  **从自然语言到代码**：支持将业务规则的自然语言描述自动转化为 Cedar 策略代码，从而实施细粒度、具有身份感知的访问控制，确保 Agent 仅能访问用户授权的工具与数据。
3.  **运行时实时拦截**：通过 AgentCore Gateway 应用这些策略，在运行时拦截并评估每一次 Agent 发起的工具请求，确保合规性。

---

## 评论

**中心观点**
该文章提出了一种将自然语言业务规则转化为确定性代码策略的范式，主张在 Amazon Bedrock 的 AgentCore 架构中引入 Cedar 策略引擎，作为独立于大模型推理之外的“确定性执行层”，以解决生成式 AI 在企业级应用中面临的安全与合规不可控难题。

**支撑理由与深度评价**

**1. 确定性边界对抗概率性幻觉（事实陈述 + 你的推断）**
*   **理由：** 文章的核心技术逻辑在于解耦。大模型本质上是概率性的，无法保证 100% 遵守指令。文章通过引入 Cedar 策略层，构建了一个“硬约束”。这意味着无论 Agent 产生何种创意或不可预测的输出，底层的策略引擎都能像防火墙一样进行拦截。
*   **深度分析：** 这是目前 AI 安全领域最务实的路径之一。单纯依赖 Prompt Engineering（提示词工程）来限制模型行为（如“不要做X”）极易受到越狱攻击。将策略代码化，使得安全审计具备了可执行性，而非依赖对自然语言的理解。

**2. 策略即代码的自然语言化落地（作者观点）**
*   **理由：** 文章强调了从自然语言描述到 Cedar 策略的转换流程。这降低了安全策略的编写门槛，使得业务专家（可能不懂代码）也能参与定义规则。
*   **深度分析：** 这是一个极具商业价值的卖点。传统的 RBAC（基于角色的访问控制）或 ABAC（基于属性的访问控制）往往需要开发人员介入。如果 Bedrock 能准确地将“只有销售总监可以查看超过百万美元的合同”转化为精确的 Cedar 策略，将极大缩短 AI 应用的上市时间。

**3. 防御深度与最小权限原则（行业观点）**
*   **理由：** 该架构符合纵深防御的理念。即使 LLM 被攻破或生成了恶意指令，Agent 执行层也会因为缺乏相应的 Policy 授权而拒绝执行。
*   **深度分析：** 这解决了 Agent 最大的痛点——Tool Use（工具使用）的安全性。Agent 往往拥有调用数据库、API 的权限，如果完全由模型自主决定何时调用，风险极大。Policy 层充当了最后的守门员。

**反例与边界条件**

**1. 静态策略与动态上下文的冲突（你的推断）**
*   **边界条件：** Cedar 策略本质上是静态代码或基于预定义属性的。然而，AI Agent 的交互往往是高度动态和依赖上下文的。
*   **挑战：** 如果业务规则涉及复杂的语义判断（例如：“如果用户情绪激动，则不要拒绝退款”），这种基于逻辑和属性的 Cedar 策略极难表达。策略层可能过于死板，扼杀了 AI 应有的灵活性和个性化服务能力。

**2. 性能延迟与系统复杂度（事实陈述）**
*   **边界条件：** 引入独立的策略引擎意味着在 LLM 生成响应和最终执行动作之间增加了一步验证过程。
*   **挑战：** 在高频交易或实时对话场景中，额外的网络跳转和策略计算会增加延迟。同时，维护两套逻辑（LLM 的 Prompt 指令 + Cedar 的代码指令）可能会导致“策略漂移”，即开发者修改了 Prompt 却忘了更新 Cedar，导致系统行为不一致。

**可验证的检查方式**

为了验证该文章所述方法的有效性，建议进行以下检查：

1.  **越狱抵抗测试：**
    *   **指标：** 构建一组“越狱 Prompt”试图诱导 Agent 执行被禁止的操作（如删除数据、发送钓鱼邮件）。
    *   **验证方式：** 对比仅使用 System Prompt 和使用 Bedrock AgentCore Policy 两种情况下的拦截率。Policy 层应展现出接近 100% 的拦截率，且不产生误判。

2.  **语义与逻辑的对齐度测试：**
    *   **指标：** 策略转换准确率。
    *   **验证方式：** 输入 50 条复杂的自然语言业务规则，由系统自动转换为 Cedar 策略。由安全专家审查生成的 Cedar 代码是否完全覆盖了自然语言的意图，是否存在逻辑漏洞。

3.  **端到端延迟监控：**
    *   **指标：** 策略评估耗时。
    *   **验证方式：** 在生产环境中观察 Agent 请求的总耗时，计算 Policy 验证阶段所占的比例。如果策略评估平均耗时超过 200ms，可能会影响用户体验。

**总结**

这篇文章从技术架构上提出了解决 AI 落地“最后一公里”安全问题的可行方案。它并没有试图让模型变得更“聪明”或更“守规矩”，而是承认模型的不完美，通过外挂的确定性系统来兜底。这种“控制平面与数据平面分离”的思路是云原生的精髓，也是 AI Agent 走向企业级核心业务的必经之路。然而，其挑战在于如何处理复杂的语义边界规则，以及避免引入过高的系统复杂度。

---

## 技术分析

基于您提供的文章标题《Secure AI agents with Policy in Amazon Bedrock AgentCore》及摘要，我将结合Amazon Bedrock、AgentCore架构以及Cedar策略引擎的通用技术原理，为您进行深入的分析与解读。

---

### 深度分析：基于 Amazon Bedrock AgentCore 的策略安全机制

### 1. 核心观点深度解读

### 文章的主要观点
文章的核心主张是：**在生成式AI代理的架构中，必须将“安全与合规控制层”与“代理的自主推理层”进行物理与逻辑上的解耦。** 通过引入 Amazon Bedrock AgentCore 的 Policy 功能，利用 Cedar 策略语言构建一个确定性的执行层，能够独立于 Agent 的 LLM（大语言模型）推理过程之外，强制执行业务规则。

### 作者想要传达的核心思想
作者试图纠正当前构建 AI Agent 时的一个常见误区：即过度依赖 LLM 的“对齐”或 Prompt Engineering（提示词工程）来保证安全性。核心思想在于“确定性胜过概率性”——LLM 的推理是概率性的，容易产生幻觉或被越狱，而基于代码的策略（如 Cedar）是确定性的。只有通过这种外部强制力，才能在企业级生产环境中放心地赋予 Agent 操作真实业务系统的权限。

### 观点的创新性和深度
这一观点的深度在于它承认了 LLM 本质的不可控性，并提出了**“分层防御”**的架构模式。
*   **创新性**：将自然语言直接转化为可执行的代码策略，降低了策略编写门槛，同时保留了代码执行的严谨性。这不仅仅是简单的 API 调用过滤，而是基于 RBAC（基于角色的访问控制）和 ABAC（基于属性的访问控制）的深度集成。
*   **深度**：它触及了 AI 治理的根本问题——如何在不限制 AI 创造力的前提下，划定其行为的不可逾越的红线。

### 为什么这个观点重要
随着 AI Agent 从“聊天机器人”向“自主任务执行者”演进，其风险等级呈指数级上升。一个不受控的 Agent 可能会误删数据库、发送错误邮件或泄露敏感数据。该观点提供了一条通往 **Agent 安全治理** 的标准化路径，是 AI 从玩具走向生产环境的关键基础设施。

### 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Amazon Bedrock AgentCore**：Bedrock 中负责编排 Agent 行为的核心引擎，处理任务分解、工具调用和记忆管理。
2.  **Cedar**：Amazon 开源的一种专为构建细粒度权限控制而设计的策略语言。它类似于 Rego（OPA），但语法更接近自然语言，专为定义“谁在什么条件下可以对什么资源执行什么操作”而优化。
3.  **Deterministic Enforcement Layer（确定性执行层）**：独立于 LLM 推理链路的代码层，即使 LLM 发出错误指令，该层也能拦截。
4.  **Natural Language to Policy（自然语言转策略）**：利用 LLM 将业务人员描述的规则（如“经理只能查看本部门预算”）转换为 Cedar 代码。

### 技术原理和实现方式
*   **拦截机制**：在 AgentCore 调用工具或 API 之前，系统会暂停请求，将当前的请求上下文（用户信息、动作、目标资源）传递给 Policy Evaluation Engine（策略评估引擎）。
*   **评估流程**：
    1.  Agent 决定调用 `TransferFunds` 工具。
    2.  系统提取上下文：`User: Alice`, `Action: Transfer`, `Resource: Account_B`, `Amount: $10,000`。
    3.  加载对应的 Cedar 策略。
    4.  引擎进行逻辑运算，返回 `Permit` 或 `Deny`。
    5.  只有 `Permit` 才会真正执行 API 调用；如果是 `Deny`，系统会将错误信息反馈给 LLM，要求 LLM 重新规划或向用户解释。

### 技术难点和解决方案
*   **难点：上下文映射**。LLM 的思维链是非结构化的，而策略引擎需要结构化的属性。
*   **解决方案**：通过严格的 Schema 定义，强制 Agent 在调用工具时提供结构化的元数据，或者通过中间件层将非结构化的请求转化为结构化的属性查询。
*   **难点：策略冲突**。当多条策略规则冲突时（例如全局规则允许，但特定资源规则禁止）。
*   **解决方案**：Cedar 内置了优先级和组合逻辑，遵循“拒绝优先”或“最匹配优先”的原则。

### 技术创新点分析
最大的创新点在于**“治理左移”**（Shifting Governance Left）。传统的安全往往在网络层或应用层，而这里将安全策略直接嵌入到了 Agent 的决策循环中，并且利用 LLM 自身来辅助生成安全策略，形成了一种“用 AI 保护 AI”的闭环。

### 3. 实际应用价值

### 对实际工作的指导意义
对于架构师和 AI 工程师而言，这意味着在设计 Agent 时，不再需要通过极其复杂的 Prompt 来限制 Agent 的行为（例如：“千万不要做X，除非Y”），而是可以将这些规则代码化。这大大提高了系统的可维护性和可靠性。

### 可以应用到哪些场景
1.  **金融交易**：限制 AI Agent 只能执行特定额度内的转账，且必须符合风控规则。
2.  **企业数据访问**：确保 HR Agent 只能访问员工权限范围内的数据，防止越权查看薪资。
3.  **客户服务**：允许 Agent 查看订单，但禁止其直接退款超过特定金额，必须转交人工。
4.  **代码操作**：允许 DevOps Agent 读取日志，但禁止其执行 `rm -rf` 等高危命令。

### 需要注意的问题
*   **策略覆盖率的完整性**：如果策略定义不严谨，Agent 可能会找到漏洞。
*   **性能延迟**：每次工具调用都增加了一次策略评估，可能影响响应速度。
*   **误报率**：过于严格的策略可能导致 Agent 无法完成有效任务，降低用户体验。

### 实施建议
*   **最小权限原则**：初始策略应设为最严格模式，然后逐步放开。
*   **人机结合**：对于高风险操作，即使策略允许，也应引入“人类确认”环节。
*   **审计日志**：记录所有策略评估的 Deny 日志，用于分析 Agent 的行为模式并优化策略。

### 4. 行业影响分析

### 对行业的启示
这一动向标志着 **AI 治理从“软约束”走向“硬约束”**。行业将意识到，仅靠 RLHF（基于人类反馈的强化学习）是不够的，必须引入类似 Cedar 这样的确定性逻辑层作为“安全护栏”。

### 可能带来的变革
*   **RAG（检索增强生成）的安全升级**：未来的 RAG 不仅是检索文档，还会在检索后应用文档级别的安全策略，防止 LLM 读取了它不该读的片段。
*   **Agent 编排标准的重构**：未来的 Agent 框架（如 LangChain, AutoGPT）可能会内置标准的策略接口，而不仅仅是 Bedrock。

### 相关领域的发展趋势
*   **Policy-as-Code（策略即代码）** 的普及。
*   **可解释性安全**：当 Agent 被拒绝时，系统能准确告知是因为违反了哪条具体策略，而不是模糊的“安全原因”。

### 5. 延伸思考

### 引发的其他思考
*   **动态策略调整**：策略能否根据实时风险评分动态变化？例如，检测到异常登录地点时，自动收紧 Agent 的操作权限。
*   **多 Agent 协作中的权限传递**：当 Agent A 调用 Agent B 时，权限是如何传递的？是否需要降权？

### 可以拓展的方向
*   **联邦学习与隐私计算**：在保护用户隐私数据的前提下进行策略评估。
*   **对抗性防御**：利用 Policy 层防御 Prompt Injection（提示词注入）攻击。如果 Agent 被注入了“忽略所有规则”的指令，Policy 层因为独立于推理之外，将成为最后一道防线。

### 未来发展趋势
未来可能会出现 **“策略市场”**，企业可以购买通用的业务策略模板（如“SOX合规策略包”），直接导入到 AgentCore 中使用。

### 7. 案例分析

### 结合实际案例说明
**场景**：一个企业内部的“IT 助手” Agent，具有重置密码和访问 AWS S3 存储桶的权限。

**成功案例分析**：
*   **配置**：设置了 Cedar 策略，规定“重置密码”仅限于非管理员账户，且必须验证用户邮箱；“S3 访问”仅限于 `logs/` 目录。
*   **结果**：黑客试图通过 Prompt Injection 让 Agent 删除 S3 上的根目录文件。Agent 的 LLM 理解了指令并试图调用 `DeleteObject` API，但 AgentCore 拦截了请求，因为策略中只允许访问 `logs/` 前缀。攻击被阻断。

**失败案例反思**：
*   **配置**：策略编写过于宽泛，允许 Agent 访问所有 S3 资源，只要用户标签是 `IT_Staff`。
*   **结果**：一名刚离职的员工（账号未及时注销，仍有 `IT_Staff` 标签）出于报复心理，让 Agent 列出了所有敏感文件。
*   **教训**：静态属性（如标签）必须与动态上下文（如员工状态）结合验证，策略粒度不能过粗。

---

## 学习要点

- Amazon Bedrock AgentCore 引入了“策略”概念，允许开发者通过定义可验证的规则来限制 AI 智能体的行为边界，从而确保其操作符合安全规范。
- 该框架支持将自然语言安全策略直接转换为可执行的代码，使得非技术人员也能通过简单的描述来实施复杂的访问控制和安全约束。
- 通过在运行时强制执行策略，系统能够自动拦截并阻止任何违反预定义规则的指令或工具调用，有效防止了数据泄露和未授权操作。
- 这种机制提供了细粒度的权限控制，能够根据上下文动态限制智能体对敏感 API 或特定数据源的访问，而非仅仅依赖静态的 API 密钥管理。
- 策略即代码的实现方式使得安全规则具备可审计性和版本管理能力，便于企业在合规性审查中追踪和验证 AI 智能体的行为逻辑。
- 该解决方案简化了企业级生成式 AI 应用的安全部署流程，使开发者无需构建繁琐的自定义基础设施即可获得企业级的安全保障。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [AI Agent](/tags/ai-agent/) / [Cedar 策略](/tags/cedar-%E7%AD%96%E7%95%A5/) / [访问控制](/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/) / [工具调用](/tags/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8/) / [运行时拦截](/tags/%E8%BF%90%E8%A1%8C%E6%97%B6%E6%8B%A6%E6%88%AA/) / [身份感知](/tags/%E8%BA%AB%E4%BB%BD%E6%84%9F%E7%9F%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [构建确定性 AI 代理安全层：利用 Amazon Bedrock AgentCore 策略]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-6.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore Policy 管控 AI Agent]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-8.md" >}})
- [利用 Amazon Bedrock AgentCore Policy 构建 AI Agent 确定性执行层]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-9.md" >}})
