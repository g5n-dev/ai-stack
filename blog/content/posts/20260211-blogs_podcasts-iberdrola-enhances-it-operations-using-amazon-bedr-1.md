---
title: "Iberdrola enhances IT operations using Amazon Bedrock A"
date: 2026-02-11T03:18:02+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "Amazon Bedrock", "AgentCore", "ServiceNow", "IT运维", "智能体", "工单自动化", "企业级AI"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "西班牙公用事业巨头Iberdrola通过与AWS合作，利用Amazon Bedrock AgentCore革新其IT运营。该AI技术主要应用于三个方面：优化变更请求验证、丰富事件管理的情境智能以及简化变更模型选择。这些创新有效减少了运营瓶颈，加速了工单解决，并提升了数据处理的一致性与质量。"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola enhances IT operations using Amazon Bedrock AgentCore

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

Iberdrola, one of the world’s largest utility companies, has embraced cutting-edge AI technology to revolutionize its IT operations in ServiceNow. Through its partnership with AWS, Iberdrola implemented different agentic architectures using Amazon Bedrock AgentCore, targeting three key areas: optimizing change request validation in the draft phase, enriching incident management with contextual intelligence, and simplifying change model selection using conversational AI. These innovations reduce bottlenecks, help teams accelerate ticket resolution, and deliver consistent and high-quality data handling throughout the organization.

---
## 摘要

西班牙公用事业巨头Iberdrola通过与AWS合作，利用Amazon Bedrock AgentCore革新其IT运营。该AI技术主要应用于三个方面：优化变更请求验证、丰富事件管理的情境智能以及简化变更模型选择。这些创新有效减少了运营瓶颈，加速了工单解决，并提升了数据处理的一致性与质量。

---
## 评论

**文章中心观点**
Iberdrola 通过利用 Amazon Bedrock AgentCore 构建多智能体架构，成功将生成式 AI 深度集成至 ServiceNow 工作流中，实现了 IT 运维从“脚本化执行”向“自主智能体协作”的模式跃迁，证明了“大模型+编排工具”在传统重资产行业中具备极高的落地潜力。

**支撑理由与边界条件**

**1. 技术架构的演进：从单点调用到 Agent 编排**
*   **支撑理由（事实陈述）：** 文章指出 Iberdrola 采用了 Amazon Bedrock AgentCore。这标志着技术应用的深化。早期企业应用 AI 多为直接调用 API（如简单的文本生成），而 AgentCore 意味着引入了“思考-行动-观察”的循环机制。企业不再只是使用模型的“知识”，而是利用模型的“推理能力”来拆解任务、调用 API（如查询 ServiceNow 知识库、自动创建工单）并自我纠错。
*   **反例/边界条件（你的推断）：** 并非所有 IT 运维场景都需要复杂的 Agent 架构。对于确定性极高、逻辑简单的任务（如“重置密码”或“查询服务器状态”），传统的硬编码脚本或简单的 RAG（检索增强生成）可能比 Agent 更高效、延迟更低且成本更便宜。Agent 架构引入了额外的 Token 消耗和不确定性（如幻觉导致的循环调用）。

**2. 业务价值的深化：知识资产的货币化与体验重塑**
*   **支撑理由（作者观点）：** Iberdrola 的案例展示了 AI 在“隐性知识显性化”方面的巨大价值。大型公用事业公司积累了数十年的运维文档和故障排除经验，这些往往分散在不同员工的脑海中或过时的文档中。通过 Agent 架构，非结构化文档被转化为可执行的动态知识库。这不仅提升了 L1/L2 级运维人员的效率，更大幅降低了初级工程师的上手门槛，解决了“老专家退休导致知识断层”的行业痛点。
*   **反例/边界条件（事实陈述）：** 这种高度依赖知识库的 AI 效果受限于数据质量。如果 ServiceNow 中的历史工单记录混乱、充满非标准术语或过时信息，Agent 的输出质量将呈指数级下降（Garbage In, Garbage Out）。数据治理是落地的前置成本。

**3. 行业标杆效应：能源行业的“保守式创新”**
*   **支撑理由（你的推断）：** 能源行业通常以高稳定性、低风险容忍度著称。Iberdrola 作为巨头采用此类技术，是一个强烈的信号。它表明生成式 AI 已经走出了“营销/客服”等边缘部门，开始进入核心的 IT 运维领域。这种“保守式创新”意味着 AWS Bedrock 提供的企业级安全护栏（如 Guardrails）和私有化部署能力已经足以满足严苛的合规要求。
*   **反例/边界条件（作者观点）：** 尽管是“核心 IT 运维”，但距离“核心 OT 运维”（如电网调度、发电厂控制）仍有巨大鸿沟。IT 容错率相对较高，而 OT 系统直接涉及物理安全。目前 AgentCore 主要应用于 ITSM（IT 服务管理），不应过度解读为 AI 已经接管了电网控制。

**4. 人机协作模式的转变**
*   **支撑理由（事实陈述）：** 文章暗示了角色的转变。人类运维人员从“执行者”变成了“审核者”和“训练师”。Agent 负责初步诊断和信息聚合，人类负责最终决策。
*   **反例/边界条件（你的推断）：** 这种模式存在“自动化偏见”风险。如果 Agent 过于自信且准确率极高，运维人员可能会产生依赖，导致技能退化，从而在 Agent 失效时无法进行人工干预。

**综合评价**

*   **内容深度：** 文章属于典型的“厂商成功案例”风格，虽然展示了架构图和应用场景，但往往略过了底层微调的细节、Prompt Engineering 的复杂度以及具体的 ROI（投资回报率）数据。论证严谨性在于其验证了技术路径的可行性，但缺乏对实施难度的客观剖析。
*   **实用价值：** 高。对于正在寻找 GenAI 落地场景的 CIO 或 CTO 而言，这是一个极佳的参考范式。它指出了“ServiceNow + AWS Bedrock”是一条成熟度高、风险可控的转型路径。
*   **创新性：** 中等。Agent 概念不新鲜，但在大型传统企业的核心系统中落地 Agentic Workflow（智能体工作流）具有标杆意义。
*   **可读性：** 结构清晰，技术术语（AgentCore, ServiceNow）使用准确，逻辑顺畅。
*   **行业影响：** 将加速公用事业及制造业将“运维知识库”作为 GenAI 落地的第一站。

**可验证的检查方式**

为了验证该文章描述的效果是否真实且可持续，建议关注以下指标与实验：

1.  **指标：工单解决率偏差**
    *   **观察窗口：** 实施后的 3-6 个月。
    *   **验证方式：** 对比 AI Agent 建议的解决方案与最终人工解决方案的一致性。如果 Agent 建议“重启服务器”而人工实际操作是“修补内存泄漏”，则说明 Agent 推理深度不足。
    *   **关键指标：** L1/L2 级工单的平均处理时间（MTTR）是否下降 30% 以上；自动解决率

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用生成式 AI 构建统一的知识检索平台

**说明**: Iberdrola 面临的挑战在于 IT 运营知识分散在不同文档中，导致信息检索困难。通过使用 Amazon Bedrock 和 AgentCore，他们构建了一个能够理解自然语言查询的智能系统。该系统不仅限于简单的关键词匹配，而是利用大语言模型（LLM）的推理能力，从非结构化文档中提取准确答案，将分散的数据孤岛转化为统一的、可对话的知识库。

**实施步骤**:
1. **盘点并整合数据源**：将现有的 IT 运维手册、故障排查指南、架构文档等集中存储到支持向量搜索的存储库（如 Amazon OpenSearch Serverless）中。
2. **选择基础模型**：在 Amazon Bedrock 中选择适合文本理解和摘要的模型（如 Anthropic Claude 或 Amazon Titan）。
3. **构建检索流程**：配置 AgentCore 以便在用户提问时，自动将查询转换为向量检索指令，定位相关文档片段。

**注意事项**: 确保对文档数据进行严格的权限控制，确保敏感的运维信息仅对授权人员可见。

---

### 实践 2：采用 RAG 架构确保信息的时效性与准确性

**说明**: 为了避免大语言模型产生“幻觉”或提供过时的信息，Iberdrola 采用了检索增强生成（RAG）架构。这意味着 AI 在生成回答之前，会先从 Iberdrola 自己的实时数据源中检索最新信息。这种做法确保了 IT 运营人员获得的建议是基于公司当前标准和最新架构的，而不是模型训练时的通用知识。

**实施步骤**:
1. **建立向量化索引**：将企业的非结构化数据进行分块、向量化并建立索引。
2. **配置提示词工程**：设计 System Prompt，明确指示模型必须“仅依据提供的上下文信息回答问题”，如果上下文中没有答案，则回答不知道。
3. **持续更新知识库**：建立自动化流程，确保当 IT 文档更新时，向量数据库也能同步更新。

**注意事项**: 定期评估检索准确率，优化文档切分的策略，以确保检索到的片段既包含上下文又足够精准。

---

### 实践 3：通过抽象层实现模型无关性与灵活性

**说明**: 使用 Amazon Bedrock 的核心优势之一是其“模型无关”的特性。Iberdrola 通过 Bedrock 的 API 调用模型，而不是将应用与特定模型硬编码绑定。这使得他们可以根据不同的任务场景（如代码生成、文本摘要、数据分析）灵活切换最适合的模型，或者在出现更优模型时快速迭代，而无需重写底层代码。

**实施步骤**:
1. **标准化接口调用**：在应用程序代码中调用 Bedrock 的标准 API，而非特定模型的 SDK。
2. **性能评估**：针对不同任务测试不同模型的性能（延迟、成本、准确性）。
3. **动态配置**：在配置文件中设置模型 ID，以便在需要更换模型时只需修改配置而无需部署新版本。

**注意事项**: 关注不同模型的 Token 定价差异，根据任务复杂度选择性价比最高的模型以控制成本。

---

### 实践 4：自动化工作流以减少人工干预

**说明**: Iberdrola 的目标不仅是回答问题，而是解决问题。利用 Amazon Bedrock AgentCore，他们能够将 AI 的能力与自动化运维工具链集成。当 AI 识别出用户意图（例如“重启服务”或“查看日志”）时，它可以调用 API 函数直接执行操作，或自动编排工作流，从而大幅缩短 IT 运营人员的平均修复时间（MTTR）。

**实施步骤**:
1. **定义可执行动作**：梳理 IT 运维中可自动化的高频操作，并将其封装为 API 接口。
2. **配置 Agent 动作组**：在 Bedrock Agents 中定义这些 API 的架构，让模型理解何时以及如何调用它们。
3. **设置人工审核环节**：对于高风险操作（如删除资源），配置 Agent 在执行前必须获得人工确认。

**注意事项**: 严格限制自动化操作的权限范围，遵循最小权限原则，防止 AI 误操作导致系统故障。

---

### 实践 5：建立严格的负责任 AI 与数据安全标准

**说明**: 在能源等高度受监管的行业，数据隐私和安全至关重要。Iberdrola 利用 Amazon Bedrock 的合规性功能（如数据不用于训练模型、加密传输）来确保数据安全。同时，他们在实施过程中建立了明确的“护栏”，防止 AI 生成有害内容或泄露敏感信息，确保 AI 行为符合企业道德和法律规范。

**实施步骤**:
1. **启用数据隐私保护**：确认 Bedrock 设置中关闭了“将数据用于模型改进”的选项。
2. **应用 Guardrails**：配置 Amazon Bedrock Guardrails 来过滤特定词汇、阻止越狱尝试并过滤 PII（个人身份信息）。
3. **审计与日志记录**：开启 CloudTrail 记录所有 API 调用，定期审计 AI 的输入和输出数据。

**注意事项**: 定期进行红

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS](/tags/aws/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [IT运维](/tags/it%E8%BF%90%E7%BB%B4/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [工单自动化](/tags/%E5%B7%A5%E5%8D%95%E8%87%AA%E5%8A%A8%E5%8C%96/) / [企业级AI](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7ai/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Snowflake与OpenAI达成2亿美元协议引入企业级AI智能体]({{< relref "posts/20260204-blogs_podcasts-snowflake-and-openai-partner-to-bring-frontier-int-8.md" >}})
- [ElevenLabs融资11亿美元估值，Cerebras获23亿美元估值及音频与芯片代理进展]({{< relref "posts/20260206-blogs_podcasts-ainews-elevenlabs-500m-series-d-at-11b-cerebras-1b-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*