---
title: "构建确定性 AI 代理安全层：利用 Amazon Bedrock AgentCore 策略"
date: 2026-03-13T19:25:32+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "AI Agent", "Cedar 策略", "访问控制", "安全防护", "自然语言处理", "运行时拦截"]
categories: ["安全", "AI 工程"]
source: blogs_podcasts
description: "本文介绍了Amazon Bedrock AgentCore中的Policy功能，旨在为AI智能体提供安全防护。核心要点如下： 1. **独立执行层**：Policy创建了一个独立于智能体自身推理之外的确定性执行层，确保安全控制不依赖于模型的不确定性输出。 2. **自然语言转策略**：用户可以将业务规则的自然语言描述转"
external_url: https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore
scenarios: ["AI/ML项目", "命令行工具"]
---

# 构建确定性 AI 代理安全层：利用 Amazon Bedrock AgentCore 策略

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:16:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)

---
## 摘要/简介

In this post, you will understand how Policy in Amazon Bedrock AgentCore creates a deterministic enforcement layer that operates independently of the agent's own reasoning. You will learn how to turn natural language descriptions of your business rules into Cedar policies, then use those policies to enforce fine-grained, identity-aware controls so that agents only access the tools and data that their users are authorized to use. You will also see how to apply Policy through AgentCore Gateway, intercepting and evaluating every agent-to-tool request at runtime.

---
## 导语

随着 AI 智能体在企业场景中的深入应用，如何确保其行为符合既定规则已成为不可忽视的安全挑战。本文将介绍 Amazon Bedrock AgentCore 中的 Policy 功能，探讨如何通过构建独立于模型推理之外的确定性执行层，将业务规则转化为 Cedar 策略。阅读本文，您将掌握实施细粒度、身份感知控制的具体方法，从而有效约束智能体的工具调用与数据访问权限。

---
## 摘要

本文介绍了Amazon Bedrock AgentCore中的Policy功能，旨在为AI智能体提供安全防护。核心要点如下：

1.  **独立执行层**：Policy创建了一个独立于智能体自身推理之外的确定性执行层，确保安全控制不依赖于模型的不确定性输出。
2.  **自然语言转策略**：用户可以将业务规则的自然语言描述转化为Cedar策略，从而实施细粒度、具有身份感知的访问控制。
3.  **运行时拦截与评估**：通过AgentCore Gateway应用这些策略，能够在运行时拦截并评估智能体对工具的每一个请求，确保智能体仅能访问用户被授权使用的工具和数据。

---
## 评论

### 中心观点
文章核心观点是：通过引入 Amazon Bedrock AgentCore 的 Policy（基于 Cedar 语言），可以在 AI Agent 的“推理层”之外构建一个独立的、确定性的“执行层”，从而在不牺牲模型自主性的前提下，解决大模型应用中的安全与合规难题。

### 支撑理由与深度评价

**1. 架构层面的“控制平面”与“数据平面”分离**
*   **事实陈述**：文章提出了一种架构范式，即 AI Agent 的 LLM（大语言模型）负责生成计划，而 AgentCore 负责执行计划，且执行过程受 Cedar 策略的硬编码约束。
*   **深度评价**：这是对当前 Agent 架构脆弱性的一次重要修正。目前的 AI Agent 普遍存在“幻觉”导致的非法操作风险（如越权访问数据库、删除文件）。将 LLM 视为“大脑”，将 Cedar Policy 视为“小脑/反射神经”，符合高可用系统的设计原则。这种**确定性覆盖层**的引入，使得 AI 系统从“概率性信任”转向了“机制性信任”。

**2. 自然语言到策略代码的转换效率**
*   **事实陈述**：文章展示了如何将业务规则（如“财务顾问不能查看非其客户的投资组合”）转化为 Cedar 策略。
*   **作者观点**：这种转化降低了安全策略的编写门槛，使得业务人员也能参与定义 Agent 的边界。
*   **深度评价**：这是 Cedar 语言相比传统 RBAC（基于角色的访问控制）的一大优势，支持 ABAC（基于属性的访问控制）。在 AI 场景下，权限往往依赖于上下文，而不仅仅是静态角色。这种灵活的表达能力是构建复杂企业级 Agent 的基石。

**3. 防御性 AI 的具体落地**
*   **事实陈述**：文章强调了 Policy 层是独立于 Agent 推理运行的。
*   **深度评价**：这解决了“提示词注入”无法被彻底根除的痛点。即使 Agent 被 Prompt Injection 攻击，意图执行恶意 SQL 语句，只要 Policy 层判定该操作不符合 `principal.action == "ExecuteSQL"` 且 `resource.id in principal.allowed_list`，操作就会被拦截。这是**纵深防御**策略在 AI 时代的具体体现。

### 反例与边界条件

尽管文章提出了优秀的架构愿景，但在实际落地中存在以下边界和挑战：

**1. 状态同步与实时性鸿沟**
*   **边界条件**：Cedar 策略的执行依赖于传入的上下文属性。
*   **潜在问题**：如果 Agent 的 LLM 推理出了一个复杂的、多步骤的中间状态（例如：“用户刚才暗示了他是管理员，虽然数据库里不是，但我应该信他”），Policy 层可能无法理解这种隐式的上下文变化。**Policy 只能验证显式声明的属性，无法验证隐式的语义意图。** 如果 LLM 在构建请求时错误地标记了属性（例如将 `action` 标记为 `read` 但实际意图是 `delete`），Policy 层会被欺骗。

**2. 策略爆炸与维护成本**
*   **反例**：在高度动态的业务场景中（例如电商促销期间的复杂优惠规则），用 Cedar 硬编码所有策略可能导致“策略表”爆炸。
*   **挑战**：当业务规则变化时，修改 Cedar 代码并重新部署的节奏，可能赶不上业务需求的变化节奏。这可能导致 Agent 的能力被僵化的策略锁死，反而失去了 AI 适应性强的优势。

**3. 确定性带来的僵化**
*   **观点**：AI 的优势在于处理模糊和边缘情况。
*   **冲突**：强制性的确定性策略会切断 Agent 处理边缘情况的能力。例如，为了救人，Agent 可能需要稍微打破一个常规流程，但 Policy 层会无情拒绝。这种“过度安全”可能降低 AI 的实用价值。

### 可验证的检查方式

为了验证文章所述方法在实际环境中的有效性，建议进行以下检查：

1.  **对抗性测试**：
    *   **指标**：Prompt Injection 攻击成功率。
    *   **实验**：构建一组越狱提示词，试图让 Agent 执行“删除所有用户”操作。对比开启 Policy 前后的拦截率。如果开启后仍有拦截失败，说明 Policy 定义存在遗漏或 LLM 构建的请求参数存在语义绕过。

2.  **延迟基准测试**：
    *   **指标**：Agent 端到端响应时间。
    *   **实验**：测量引入 Cedar 策略评估层后，单次 Action 执行增加的延迟。如果策略复杂（涉及大量层级查询），可能会显著拖慢 Agent 的交互速度，影响用户体验。

3.  **覆盖率分析**：
    *   **指标**：策略覆盖率。
    *   **观察窗口**：观察 Agent 在生产环境中的执行日志，统计有多少次操作是因为“Policy Deny”而失败的。如果比例过高，说明策略过于严格或 Agent 的意图生成与策略定义不匹配。

### 实际应用建议

1.  **不要试图用 Policy 解决所有问题**：Policy 应用于**高风险、高确定性**的操作（如数据写入、API 调用、邮件发送）。对于低风险的检索类操作，应保持宽松，以免扼杀 AI 的灵活性。
2.  **建立“红队”机制**：专门组建团队或利用另一套 LLM 来攻击 Cedar 策略，寻找逻辑漏洞。不要假设写了策略就安全。
3.  **语义层与策略层的

---
## 技术分析

基于您提供的文章标题《Secure AI agents with Policy in Amazon Bedrock AgentCore》及摘要内容，结合亚马逊云科技（AWS）在AI安全领域的最新技术动态，以下是对该文章核心观点和技术要点的深入分析。

---

# 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：**在生成式AI代理中，安全性不应依赖于大模型（LLM）自身的推理能力，而必须通过外部的、确定性的策略层来进行强制执行。** 具体而言，Amazon Bedrock AgentCore 引入的 Policy 功能，允许开发者将业务规则从自然语言转化为 Cedar 策略代码，从而在 Agent 执行动作前构建一道独立的安全防火墙。

**作者想要传达的核心思想**
作者试图传达“控制权分离”的理念。AI Agent 的核心价值在于自主规划和推理，但这种自主性在涉及企业敏感数据或关键操作时带来了巨大的风险。核心思想在于：**让 AI 负责“思考”，而让明确的策略负责“放行”。** 这种机制确保了即使 AI 产生幻觉或被诱导做出有害决策，底层的策略引擎也能像传统的访问控制一样，基于逻辑阻断非法操作。

**观点的创新性和深度**
这一观点的创新性在于打破了“提示词工程”作为唯一安全防线的局限。传统的 Agent 安全主要依赖 System Prompt（如“不要做X”），这是一种软约束。而 Bedrock AgentCore 引入 Cedar 策略，将传统的身份认证与授权（IAM）模型引入了 Agent 的动态决策流中。这是一种**架构层面的深度革新**，它承认了概率性模型（LLM）在合规性上的先天不足，并引入形式化逻辑进行兜底。

**为什么这个观点重要**
随着 AI Agent 从“聊天机器人”向“办事员”转变，它们开始获得数据库查询、发送邮件、修改订单等实际操作权限。如果缺乏这种确定性策略层，Agent 的误操作将直接导致企业资产损失或数据泄露。这一观点为 AI 落地企业级核心业务提供了必须的安全底座。

# 2. 关键技术要点

**涉及的关键技术或概念**
1.  **Amazon Bedrock AgentCore**: AWS 构建生成式 AI 应用的核心框架，负责编排 Agent 的推理过程。
2.  **Cedar**: AWS 开发的一种开源策略语言，专为编写细粒度访问控制策略而设计，类似于自然语言但具备严格的逻辑结构。
3.  **Deterministic Enforcement Layer (确定性执行层)**: 与 LLM 的概率性输出不同，这一层的执行结果是 0 或 1，不存在“可能”。
4.  **Natural Language to Policy (NL2Policy)**: 利用 LLM 将业务描述自动转换为 Cedar 代码的转换过程。

**技术原理和实现方式**
*   **独立运行机制**: 策略层并不参与 Agent 的初始思维链。Agent 规划出一组动作后，在执行每一个动作之前，必须向 Policy Engine 发送请求。
*   **策略评估**: Policy Engine 接收请求，结合当前的上下文（如用户角色、当前时间、请求的资源ID）和预定义的 Cedar 策略进行逻辑比对。
*   **拦截与放行**: 如果评估结果为 Allow，Agent 调用 API；如果为 Deny，Agent 被强制中断或要求重新规划。

**技术难点和解决方案**
*   **难点**: 上下文映射。Agent 的思维链往往是抽象的（例如“帮他查一下”），而策略需要具体的参数（如 User_ID, Resource_ID）。
*   **解决方案**: 文章可能强调通过“函数调用”或“工具定义”的元数据来规范 Agent 输出的结构，确保传递给 Policy 层的参数是完整且格式化的。

**技术创新点分析**
最大的创新点在于**将 Cedar 策略语言引入 AI Agent 生命周期**。Cedar 本身是为微服务设计的，将其引入 Agent 领域，意味着 AI 安全治理可以无缝复用企业现有的 IAM 体系，实现了“同一套语言，既管人，也管 AI”。

# 3. 实际应用价值

**对实际工作的指导意义**
这一技术为架构师和 AI 开发者提供了标准化的 Agent 安全落地范式。它解决了“既要灵活，又要合规”的矛盾。开发者不再需要苦口婆心地通过 Prompt 哄骗 AI 遵守规则，而是可以像配置防火墙规则一样硬性配置 Agent 的行为边界。

**可以应用到哪些场景**
1.  **金融交易**: 限制 Agent 只能查询账户，不能执行转账，或者限制转账金额上限。
2.  **企业知识库**: Agent 可以读取文档，但不能基于文档内容生成包含敏感 PII（个人身份信息）的公开报告。
3.  **多租户 SaaS**: 确保 Agent 在处理租户 A 的请求时，即使在 Prompt 中被诱导，也无法访问租户 B 的数据。

**需要注意的问题**
*   **策略覆盖度**: 策略必须覆盖所有可能的工具和 API 组合，否则 Agent 可能绕过检查。
*   **性能延迟**: 每一步动作都需要额外的策略检查，会增加 Agent 的响应延迟。

**实施建议**
建议从“高权限、严监控”转向“最小权限、显式授权”。在开发初期，就将 Cedar 策略作为代码的一部分纳入 CI/CD 流程，而不是事后补丁。

# 4. 行业影响分析

**对行业的启示**
这一动向表明，AI 安全治理正在从“软约束”时代迈向“硬编码”时代。行业将意识到，仅靠对齐训练是不够的，必须要有运行时的强制干预机制。

**可能带来的变革**
这可能会催生**“AI 防火墙”**这一新品类的成熟。未来的企业架构中，LLM 将被视作不可信的内部网络，所有的出口都必须经过 Policy 网关。

**相关领域的发展趋势**
*   **Verifiable AI**: 结合形式化验证，确保 Agent 行为符合数学证明的安全规范。
*   **Governance as Code**: 策略即代码，AI 的合规性将通过代码审计来保障。

**对行业格局的影响**
AWS 通过推广 Cedar 语言，正在试图建立 AI 安全领域的标准。如果 Cedar 成为 Agent 策略的事实标准，将极大地增强 AWS 在企业级 AI 市场的护城河。

# 5. 延伸思考

**引发的其他思考**
*   **动态策略**: 未来的策略能否根据 Agent 的“信心分数”动态调整？例如，Agent 信心低时，策略自动收紧，要求人工介入。
*   **策略冲突**: 当多个 Agent 协作时，不同 Agent 的策略集发生冲突该如何解决？

**可以拓展的方向**
*   **Human-in-the-loop**: 结合 Policy，当 Deny 发生时，自动触发人工审批流程。
*   **策略解释性**: 当 Agent 被拦截时，如何用自然语言向用户解释违反了哪条 Cedar 策略。

**未来发展趋势**
AI Agent 将逐渐具备“自我修正”能力。当被 Policy 拦截后，Agent 不应直接报错，而应理解拦截原因，自动调整行动计划以符合策略要求。

# 6. 实践建议

**如何应用到自己的项目**
1.  **盘点工具**: 列出 Agent 能够调用的所有 API 和工具。
2.  **定义边界**: 明确哪些操作是绝对禁止的，哪些是有条件的（如特定角色、特定时间）。
3.  **编写 Cedar 策略**: 使用 AWS 提供的模板或生成式工具，将边界条件转化为 Cedar 代码。
4.  **测试与红队**: 专门设计 Prompt 试图诱导 Agent 越界，验证 Policy 层的有效性。

**具体的行动建议**
*   学习 Cedar 语法（非常类似 Python/JSON）。
*   在 Bedrock 配置中启用 `orchestration` 类型的 Agent，并关联 Policy 模板。
*   建立策略的版本控制。

**需要补充的知识**
*   了解 ABAC（基于属性的访问控制）模型。
*   熟悉 Amazon Bedrock 的 Agent 框架结构。

**实践中的注意事项**
不要试图用 Policy 去限制 Agent 的“思考内容”（例如限制它想什么），只能限制它的“行动”（例如限制它调用什么 API）。试图审查思维链会导致 Agent 性能急剧下降。

# 7. 案例分析

**成功案例分析**
*   **场景**: 某银行部署了 AI 客服助理协助理财经理查询客户信息。
*   **配置**: 设置 Cedar 策略 `permit(principal, action, resource) when { resource.owner == principal.department }`。
*   **效果**: 即使黑客通过 Prompt 注入攻击，让 Agent 试图查询 CEO 的薪资，Policy 层检测到资源所有者与当前操作者部门不匹配，直接拦截，成功防御了数据泄露。

**失败案例反思**
*   **场景**: 电商 Agent。
*   **问题**: 开发者只设置了策略限制“购买”动作，却忘了限制“查看订单详情”动作。
*   **后果**: 攻击者诱导 Agent 拼凑了订单详情中的敏感信息（如地址、电话），虽然没有直接购买，但造成了隐私泄露。
*   **教训**: 策略覆盖必须全面，所有涉及敏感数据的读写操作都必须纳入 Policy 管控，不仅仅是写操作。

# 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级生成式 AI Agent 时，**必须**在 LLM 推理层之外部署独立的确定性策略执行层（如 Cedar Policy），以确保系统的安全性与合规性。

**支撑理由与依据**
1.  **LLM 的本质缺陷**: LLM 是概率性模型，存在幻觉和对抗性攻击风险，无法保证 100% 遵守指令。
    *   *依据*: 研究表明，Prompt Injection 攻击能绕过 System Prompt 的限制。
2.  **企业合规的刚性需求**: 企业安全标准（如 SOC2, HIPAA）要求访问控制必须是强制性的、可审计的，不能依赖“黑盒”模型的自觉。
    *   *依据*: 传统 IAM 模型的成功实践。
3.  **责任分离原则**: 将“规划”与“执行/校验”分离，符合软件工程的高内聚低耦合原则，便于维护和调试。
    *   *依据*: 架构设计的最佳实践。

**反例或边界条件**
1.  **纯创意/低风险场景**: 如果 Agent 仅用于生成诗歌或头脑风暴，不涉及任何外部 API 调用或敏感数据，引入复杂的 Cedar 策略可能是过度设计。
2.  **极低延迟要求**: 在毫秒级响应的实时交易中，额外的策略评估步骤如果优化不当，可能成为性能瓶颈。

**命题性质分析**
*   **事实**: LLM 存在不确定性；Cedar 语言具备确定性验证能力。
*   **价值判断**: 安全性优于 Agent 的响应速度；可解释性优于黑盒推理。
*   **可检验预测**: 采用此架构的 AI 系统，在红队测试中的防御成功率将显著高于仅依赖 Prompt 的系统。

**立场与验证方式**
*   **立场**: 支持在所有涉及数据操作或工具调用的 Agent 系统中引入 Bedrock AgentCore Policy。
*   **可证伪验证**:
    *   *实验*: 构建两组 Agent，A 组仅使用 Prompt 限制，B 组使用 Cedar Policy 限制。进行 100 次 Prompt Injection 攻击。
    *   *指标*: 记录

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施最小权限访问控制

**说明**: 为 Amazon Bedrock 中的 AI 代理分配执行任务所需的最小权限集。通过限制代理对特定 AWS 资源（如 Lambda 函数、OpenSearch Serverless 集合或 S3 存储桶）的访问权限，可以降低潜在安全漏洞的影响范围，并防止代理被诱导访问未经授权的数据。

**实施步骤**:
1. 为每个代理创建专用的 IAM 角色。
2. 在 IAM 策略中明确定义允许调用的特定操作和资源 ARN。
3. 避免使用 `*` 通配符，而是精确限定资源路径。
4. 定期审计 IAM 策略，移除不再需要的权限。

**注意事项**: 确保代理角色没有创建或修改 IAM 策略的权限，以防止权限升级攻击。

---

### 实践 2：配置防护轨道策略以防止敏感操作

**说明**: 利用 Amazon Bedrock 的 Guardrails 功能定义严格的策略边界。通过配置敏感信息过滤、拒绝关键词和主题限制，确保代理不会生成有害内容、泄露 PII（个人身份信息）或执行禁止的操作，从而在应用层实现合规与安全。

**实施步骤**:
1. 在 Bedrock 控制台中创建 Guardrail。
2. 配置“拒绝的主题”以阻止代理参与受限领域的对话。
3. 设置“敏感信息过滤”以屏蔽 PII 或正则表达式匹配的特定数据模式。
4. 将创建的 Guardrail 关联到特定的 Agent 别名或版本。

**注意事项**: Guardrail 是应用层的防线，应与 IAM 权限控制结合使用，不能替代底层资源的访问控制。

---

### 实践 3：强化提示词注入防御

**说明**: 设计系统提示词和上下文以减轻提示词注入攻击的风险。攻击者可能试图通过精心设计的输入来覆盖代理的原始指令。通过使用清晰的分隔符和指令性防御，可以确保代理遵循预期的业务逻辑。

**实施步骤**:
1. 在系统提示词中明确界定用户输入与系统指令的边界（例如使用 `###` 或 XML 标签）。
2. 包含“指令层级”指示，要求代理优先处理系统指令而非用户输入。
3. 对用户输入进行预处理，过滤掉试图操控模型行为的特定字符序列。

**注意事项**: 不要在上下文中直接展示未经清洗的用户输入，特别是当这些输入将被传递给下游工具时。

---

### 实践 4：对工具调用进行严格验证

**说明**: 代理通常通过调用外部 API（工具）来执行操作。必须在代码层面或配置层面验证代理生成的输入参数，防止注入攻击或恶意参数传递给后端系统。

**实施步骤**:
1. 在 Lambda 函数（作为代理的后端）中实施严格的输入验证模式。
2. 检查参数类型、长度和允许的值范围。
3. 对于涉及文件系统或数据库的操作，确保参数化查询，避免拼接字符串。

**注意事项**: 即使 IAM 权限配置正确，如果工具实现代码存在漏洞，代理仍可能被利用执行非预期操作。

---

### 实践 5：启用详细的日志记录与监控

**说明**: 为了检测异常行为和安全事件，必须启用 CloudTrail 数据事件记录和 Bedrock 的调用日志。这允许安全团队审计代理调用的模型、使用的工具以及返回的响应，从而在发生安全事件时进行取证分析。

**实施步骤**:
1. 在 Bedrock 中配置模型调用日志，将其发送到 CloudWatch Logs 或 S3。
2. 确保为代理使用的 IAM 角色启用 CloudTrail 记录。
3. 设置 CloudWatch 告警，用于监控异常的 API 调用频率或错误率。

**注意事项**: 日志中可能包含敏感数据，请确保日志存储桶（S3）和日志组已启用加密并配置了适当的访问策略。

---

### 实践 6：实施上下文感知的访问控制

**说明**: 确保代理在处理数据时，能够根据用户身份动态应用访问控制策略。这不仅是关于代理能否访问工具，还在于代理代表用户检索数据时，不应跨越用户权限边界。

**实施步骤**:
1. 在将上下文传递给代理之前，在应用层验证用户身份。
2. 在代理的工具定义中，设计能够接收用户上下文作为参数的接口。
3. 确保后端逻辑（如 RAG 检索或数据库查询）根据传递的用户 ID 过滤数据。

**注意事项**: 不要依赖代理本身来“理解”或“遵守”数据访问权限，必须在数据检索层面强制执行权限检查。

---
## 学习要点

- Amazon Bedrock AgentCore 引入了一种基于策略的权限控制机制，允许开发者通过精细化的策略定义来严格限制 AI 智能体的操作边界和 API 访问权限。
- 该框架通过将安全策略与核心业务逻辑解耦，实现了在不修改代理代码的情况下灵活地管理和更新安全规则。
- 系统支持在策略中定义上下文感知的防护措施，能够根据用户身份或环境动态调整智能体对敏感数据的访问级别。
- 借助自动化的策略执行引擎，Bedrock AgentCore 能够在运行时实时拦截并阻断任何违反预定义安全策略的指令或工具调用。
- 这种基于策略的安全模型显著降低了在复杂 AI 应用中实施治理与合规要求的难度，提升了企业级部署的安全性与可控性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [AI Agent](/tags/ai-agent/) / [Cedar 策略](/tags/cedar-%E7%AD%96%E7%95%A5/) / [访问控制](/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/) / [安全防护](/tags/%E5%AE%89%E5%85%A8%E9%98%B2%E6%8A%A4/) / [自然语言处理](/tags/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/) / [运行时拦截](/tags/%E8%BF%90%E8%A1%8C%E6%97%B6%E6%8B%A6%E6%88%AA/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [利用 Amazon Bedrock AgentCore Policy 实现安全访问]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-3.md" >}})
- [构建安全的 Amazon Bedrock 代理：利用 AgentCore Policy 实现细粒度访问控制]({{< relref "posts/20260312-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-2.md" >}})
- [基于 Bedrock AgentCore 策略构建确定性执行层以管控 AI 智能体]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-4.md" >}})
- [构建安全的 Amazon Bedrock 智能体：利用 AgentCore Policy 实现工具调用合规]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-5.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*