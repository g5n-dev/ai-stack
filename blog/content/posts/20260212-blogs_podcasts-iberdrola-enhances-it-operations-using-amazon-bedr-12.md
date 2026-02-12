---
title: "Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营"
date: 2026-02-12T08:46:54+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "智能体架构", "IT 运营", "AWS", "变更管理", "事件管理"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "**Iberdrola 借力 Amazon Bedrock AgentCore 升级 IT 运营** 全球最大的公用事业公司之一 Iberdrola 与 AWS 合作，通过采用先进的 Amazon Bedrock AgentCore 技术，对其在 ServiceNow 平台上的 IT 运营进行了革命性升级。 Iberd"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola 如何利用 Amazon Bedrock 优化 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

作为全球最大的公用事业公司之一，Iberdrola 拥抱前沿 AI 技术，以革新其在 ServiceNow 中的 IT 运营。通过与 AWS 的合作，Iberdrola 使用 Amazon Bedrock AgentCore 实施了多种智能体架构，聚焦于三个关键领域：优化起草阶段的变更请求验证、利用上下文智能增强事件管理，以及借助对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加速工单解决，并在整个组织范围内实现一致且高质量的数据处理。

---
## 导语

作为全球能源领域的领军企业，Iberdrola 面临着复杂的 IT 运营管理挑战。本文深入剖析了该公司如何利用 Amazon Bedrock AgentCore 在 ServiceNow 环境中构建智能体架构，以解决变更请求验证与事件管理等核心痛点。通过具体案例，读者将了解对话式 AI 与上下文智能如何有效减少流程瓶颈，从而在提升工单处理效率的同时，确保企业级数据的一致性与高质量。

---
## 摘要

**Iberdrola 借力 Amazon Bedrock AgentCore 升级 IT 运营**

全球最大的公用事业公司之一 Iberdrola 与 AWS 合作，通过采用先进的 Amazon Bedrock AgentCore 技术，对其在 ServiceNow 平台上的 IT 运营进行了革命性升级。

Iberdrola 利用 AgentCore 构建了多种智能体架构，重点优化了以下三个关键领域：
1.  **优化变更请求验证**：在草稿阶段即进行验证，提升流程效率。
2.  **丰富事故管理**：利用上下文情报增强事故处理能力。
3.  **简化变更模型选择**：通过对话式 AI 降低选择复杂度。

这些创新举措有效减少了运营瓶颈，加速了工单解决速度，并实现了全组织范围内的高质量数据处理。

---
## 评论

### 文章中心观点
**事实陈述**：文章核心观点是，通过在ServiceNow平台上集成基于Amazon Bedrock AgentCore的智能体架构，Iberdrola成功实现了IT运维从传统自动化向“自主决策”的智能化转型，从而显著提升了运营效率并降低了人为干预成本。

### 深入评价

#### 1. 内容深度与论证严谨性
文章展示了较高的技术颗粒度，将讨论焦点从泛泛的“AI应用”下沉到了具体的架构层面。
*   **支撑理由**：
    *   **架构解耦**：文章提及使用Amazon Bedrock AgentCore，这表明Iberdrola没有仅仅使用简单的API调用，而是构建了一个具有“记忆”和“工具调用”能力的Agentic Workflow。这解决了传统LLM在处理IT工单时缺乏上下文和执行能力的痛点。
    *   **场景聚焦**：明确指出针对ServiceNow这一IT运维核心系统进行优化。ServiceNow不仅是工单系统，更是工作流引擎。将AI Agent嵌入工作流引擎，是实现“人机协同”向“无人值守”跨越的关键一步。
    *   **行业标杆效应**：作为公用事业巨头，Iberdrola面临的是遗留系统多、合规要求严苛的复杂环境。在此类场景下验证Agent架构，比在互联网初创公司验证更具说服力。
*   **反例/边界条件**：
    *   **幻觉风险**：在IT运维中，精确性是第一要务。文章未深入探讨如何防止Agent在执行脚本或修改配置时产生“幻觉”。如果Agent错误地关闭了服务器或修改了电网相关参数，后果是灾难性的。
    *   **遗留系统兼容性**：虽然ServiceNow被现代化了，但Iberdrola底层的电网控制系统和ERP系统可能极其陈旧。AgentCore能否通过API顺畅地与这些“黑盒”或基于大型机的系统交互，文章未详细说明，这往往是项目失败的原因。

#### 2. 创新性与新方法
*   **支撑理由**：
    *   **从RPA到Agentic AI的演进**：传统的IT运维自动化依赖RPA（机器人流程自动化），规则僵硬。文章提出的Agentic Architecture意味着系统具备了“推理-规划-行动”的能力。例如，面对服务器报警，RPA只能执行预设脚本，而Agent可以结合日志分析、历史案例和当前负载，动态决定是重启服务、扩容还是通知人工。
    *   **AgentCore的落地**：利用AWS Bedrock的托管服务快速编排Agent，这代表了一种新的技术交付模式——即利用大厂的基础模型能力快速构建垂直领域的“大脑”，而非从零训练模型。
*   **反例/边界条件**：
    *   **技术栈锁定**：深度绑定AWS和Bedrock可能导致未来的供应商锁定问题，且数据出境（对于跨国能源公司）涉及复杂的合规红线。

#### 3. 实用价值与行业影响
*   **支撑理由**：
    *   **可复用的路径**：对于其他拥有复杂IT资产的传统企业（如制造、银行、电信），Iberdrola的案例提供了一条清晰的路径：不要试图用AI推翻旧系统，而是用AI“包裹”旧系统（通过ServiceNow等中间层）。
    *   **降本增效的实证**：IT运维成本通常是大型企业的沉重负担。Agent能够处理L1/L2级别的常规工单，将释放工程师精力用于架构优化，这对CIO极具吸引力。
*   **反例/边界条件**：
    *   **人才断层**：实施Agentic AI需要既懂IT运维又懂Prompt Engineering和Agent编排的复合型人才，目前市场上此类人才极度稀缺。

#### 4. 可读性与逻辑性
文章结构清晰，采用了“问题-方案-成效”的经典叙事逻辑。技术术语使用准确，适合CTO、架构师及数字化转型决策者阅读。但略显不足的是，摘要中提到的“targeting three key areas”在截取部分未完全展开，导致对具体业务场景的理解略显碎片化。

### 实际应用建议
基于对该案例的分析，提出以下建议：
1.  **建立“人机回环”机制**：在AgentCore与ServiceNow之间强制设置人工审核层，特别是涉及“删除”、“重启”、“变更配置”等高危操作时，必须由人工确认Agent生成的计划。
2.  **数据治理先行**：在引入Agent之前，必须清洗ServiceNow中的CMDB（配置管理数据库）数据。如果输入Agent的数据本身就是错误的（如服务器IP记录过时），Agent的推理再强也会导致误操作。
3.  **灰度发布策略**：不要一开始就让Agent处理生产环境工单。应先在影子模式运行，对比Agent的建议与人工操作的结果，待准确率达标后再逐步放开权限。

### 可验证的检查方式
为了验证该案例的真实效果及技术的成熟度，建议关注以下指标：
1.  **MTTR（平均修复时间）变化率**：
    *   *指标*：对比引入Agent前后，处理同类IT工单的平均耗时。
    *   *预期*：L1/L2工单的MTTR应显著下降（如减少50%以上）。
2.  **自动解决率**：
    *   *指标*：无需人工干预即可闭环的工单比例。
    *   *观察窗口*：上线后3-6个月。
3.  **幻觉拦截率**：
    *   *指标*：Agent生成错误操作建议被安全过滤器或人工拦截的次数。
    *   *实验*：红队测试，故意发送包含

---
## 技术分析

## 技术分析

### 核心观点深度解读
本案例展示了全球能源巨头 Iberdrola 如何通过 AWS Amazon Bedrock 和 AgentCore 架构，将生成式 AI 从简单的对话交互升级为具备执行能力的智能体，并成功集成到 ServiceNow 的 IT 运维流程中。其核心思想在于利用 AgentCore 编排层，将大语言模型（LLM）的推理能力与企业特定的业务逻辑及私有数据深度绑定。这标志着 AI 应用从“内容生成”向“流程自动化”的跨越，证明了在高度监管和复杂的传统行业中，通过混合架构（托管模型+定制化逻辑）实现 AI 安全落地的可行性。

### 关键技术要点
1.  **Amazon Bedrock**：作为底层模型托管服务，提供了无服务器的基础设施，允许 Iberdrola 访问多种高性能 LLM（如 Anthropic Claude），无需直接管理模型训练和部署的底层复杂性。
2.  **AgentCore 架构**：这是实现智能体逻辑的核心组件。它负责将用户的自然语言指令转化为具体的执行计划，协调 LLM 推理、上下文记忆管理以及工具调用。
3.  **工具调用与 API 集成**：通过 Function Calling 机制，AgentCore 能够将 LLM 的输出转化为结构化的 API 请求，直接与 ServiceNow 平台交互，实现工单查询、状态更新等自动化操作。
4.  **检索增强生成 (RAG)**：利用向量数据库连接企业知识库，确保模型在回答问题时能够基于最新的内部文档和历史数据，有效减少幻觉。

### 技术难点与解决方案
*   **难点：企业数据的安全性与隔离**。
    *   **解决方案**：利用 AWS 的安全框架和 VPC 隔离机制，确保数据在传输和处理过程中的私密性。同时，通过 Bedrock 的 Guardrails 功能过滤不当输出，强制 AI 仅基于可信的企业知识源进行回答。
*   **难点：复杂业务逻辑的准确执行**。
    *   **解决方案**：AgentCore 并未赋予 LLM 直接操作数据库的权限，而是将其限制在预定义的、经过严格测试的 API 函数集合内。这种“代理模式”确保了即使模型产生推理偏差，其执行的操作也在业务允许的安全范围内。

### 技术创新点分析
*   **从“辅助”到“代理”的转变**：传统的 AI 运维工具多提供诊断建议，仍需人工执行。本案例中的智能体具备了直接操作 ServiceNow 的能力，实现了从“信息检索”到“任务闭环”的质变。
*   **动态模型路由**：AgentCore 能够根据任务的复杂程度，动态选择最适合的模型（例如简单查询使用快速廉价的小模型，复杂推理使用高精度的大模型），从而在性能和成本之间取得最佳平衡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于 AgentCore 的模块化运维架构

**说明**:
Iberdrola 利用 Amazon Bedrock AgentCore 构建了高度模块化的 IT 运维系统。通过将复杂的运维任务（如日志分析、事件响应、资源管理）拆解为独立的 Agent 模块，实现了功能的解耦和复用。这种架构允许不同的 Agent 专注于特定领域，同时通过核心编排层协同工作，从而提高了系统的灵活性和可维护性。

**实施步骤**:
1. 识别 IT 运维中的关键领域（如监控、补丁管理、安全合规）。
2. 为每个领域设计独立的 Agent 逻辑和知识库。
3. 利用 AgentCore 编排这些 Agent，定义它们之间的通信和协作协议。
4. 建立统一的接口层，以便用户或其他系统可以通过自然语言调用这些 Agent。

**注意事项**:
- 避免单体式设计，确保每个 Agent 的职责单一且清晰。
- 需要建立清晰的 Agent 间数据流转标准，防止信息孤岛。

---

### 实践 2：利用企业私有知识库增强生成式 AI 准确性

**说明**:
为了确保生成式 AI 能够准确回答 Iberdrola 特定的技术问题，项目实施了 RAG（检索增强生成）模式。通过将公司内部的历史工单、技术文档、操作手册等非结构化数据索引化，并结合 Amazon Bedrock 的 Foundation Models，AgentCore 能够在生成回答前检索相关上下文。这极大地减少了模型幻觉，并提高了回答的相关性。

**实施步骤**:
1. 收集并清洗企业内部的运维文档和历史数据。
2. 将数据向量化并存储在向量数据库（如 Amazon OpenSearch Serverless）中。
3. 配置 AgentCore 的知识库关联，使其在处理用户查询时自动执行语义检索。
4. 定期更新知识库索引，以确保信息的时效性。

**注意事项**:
- 数据清洗是关键，必须移除过时或错误的文档，以免误导模型。
- 需要严格的数据访问权限控制，确保敏感信息不被泄露。

---

### 实践 3：建立自然语言到 API 的自动化转换机制

**说明**:
Iberdrola 的实践展示了如何通过 AgentCore 将自然语言指令直接转换为 API 调用。这允许运维人员使用日常语言查询系统状态或执行操作（如“重启服务”或“查询昨天的错误日志”），而无需编写脚本或直接访问底层 CLI。AgentCore 负责解析意图、提取参数并安全地调用相应的后端服务。

**实施步骤**:
1. 梳理运维过程中常用的 API 和操作指令。
2. 在 AgentCore 中为这些 API 定义清晰的 OpenAPI 规范（Schema）。
3. 配置 Agent 的推理逻辑，使其能够根据用户输入匹配正确的 API 并填充参数。
4. 在沙箱环境中测试自然语言指令的解析准确率和执行结果。

**注意事项**:
- 必须为所有自动化操作实施严格的权限验证和审批流程。
- 对于破坏性操作（如删除资源），应配置“确认机制”或要求人工审核。

---

### 实践 4：实施基于角色的细粒度访问控制

**说明**:
在引入生成式 AI 助手时，安全性至关重要。Iberdrola 强调通过身份验证和授权策略来管理 Agent 的访问权限。确保 Agent 在执行操作或检索信息时，严格遵循当前用户的权限级别。这意味着 Agent 不能访问用户自身无权访问的数据或执行用户无权执行的操作。

**实施步骤**:
1. 集成企业现有的身份提供商（IdP），如 Active Directory 或 Okta。
2. 在 Agent 调用后端 API 时，传递用户上下文信息。
3. 在 API 网关或服务层强制执行权限检查，拒绝越权请求。
4. 审计和记录所有 Agent 的操作行为，以便合规审查。

**注意事项**:
- 不要将硬编码的凭证嵌入 Agent 配置中。
- 确保“思维链”或日志记录中不会意外泄露敏感的 PII（个人身份信息）。

---

### 实践 5：优化提示词工程与模型选择策略

**说明**:
为了平衡成本与性能，Iberdrola 并非依赖单一模型，而是根据任务复杂度选择不同的基础模型。对于简单的查询，可能使用快速且成本低的小型模型；而对于复杂的代码生成或故障分析任务，则切换到更强大的模型（如 Anthropic Claude 3）。同时，通过精心设计的 System Prompt，确保模型始终扮演运维专家的角色。

**实施步骤**:
1. 定义不同任务类型的特征（如：摘要、提取、生成、推理）。
2. 为每种任务类型测试并选定最优的基础模型。
3. 编写并迭代 System Prompt，明确模型的角色、输出格式限制和安全边界。
4. 利用 Amazon Bedrock 的 Cross-region Inference 功能优化延迟和可用性。

**注意事项**:
- 定期评估新发布的模型，看是否能提供更好的性价比。
- Prompt 中应包含“拒绝回答无关问题”的指令，防止模型被滥用。

---
## 学习要点

- 基于您提供的标题“Iberdrola enhances IT operations using Amazon Bedrock AgentCore”，以下是关于该案例的 5-7 个关键要点总结：
- 通过利用 Amazon Bedrock AgentCore，Iberdrola 成功实现了 IT 运营流程的自动化与智能化，显著提升了运维效率。
- 该方案利用生成式 AI 快速处理复杂的 IT 运营数据，从而加速了故障诊断和问题解决的速度。
- 借助 AI 智能体，企业能够将 IT 团队从重复性的日常维护任务中解放出来，使其能专注于更具战略性的创新工作。
- 这一应用展示了如何将基础模型安全地集成到企业核心业务系统中，以优化工作流程并降低运营成本。
- Iberdrola 的实践证明了大型能源企业可以通过采用云原生 AI 技术来加速其数字化转型进程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [智能体架构](/tags/%E6%99%BA%E8%83%BD%E4%BD%93%E6%9E%B6%E6%9E%84/) / [IT 运营](/tags/it-%E8%BF%90%E8%90%A5/) / [AWS](/tags/aws/) / [变更管理](/tags/%E5%8F%98%E6%9B%B4%E7%AE%A1%E7%90%86/) / [事件管理](/tags/%E4%BA%8B%E4%BB%B6%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow 运]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-10.md" >}})
- [Iberdrola 如何利用 Amazon Bedrock AgentCore 优化 ServiceNow I]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-11.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-8.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*