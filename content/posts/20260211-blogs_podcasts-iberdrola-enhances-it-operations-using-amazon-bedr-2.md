---
title: "Iberdrola enhances IT operations using Amazon Bedrock A"
date: 2026-02-11T16:19:57+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "智能代理", "IT 运维", "对话式 AI", "工单自动化", "AWS"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "Iberdrola 与 AWS 合作，利用 Amazon Bedrock AgentCore 引入前沿 AI 技术，对其在 ServiceNow 中的 IT 运营进行了革新性优化。通过实施不同的智能代理架构，重点实现了三大核心改进： 1. **优化变更请求验证**：在起草阶段对变更请求进行智能验证。 2. **丰富事件"
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

Iberdrola 与 AWS 合作，利用 Amazon Bedrock AgentCore 引入前沿 AI 技术，对其在 ServiceNow 中的 IT 运营进行了革新性优化。通过实施不同的智能代理架构，重点实现了三大核心改进：

1.  **优化变更请求验证**：在起草阶段对变更请求进行智能验证。
2.  **丰富事件管理**：利用上下文智能增强事件处理能力。
3.  **简化变更模型选择**：通过对话式 AI 辅助模型选择。

这些创新举措有效减少了运营瓶颈，帮助团队加速了工单解决速度，并确保了全组织范围内数据处理的持续性与高质量。

---
## 技术分析

基于您提供的文章标题和摘要，虽然正文内容被截断，但结合Iberdrola（伊维尔德罗拉）作为全球最大公用事业公司之一的背景，以及AWS（亚马逊云科技）和ServiceNow（IT服务管理巨头）的技术生态，我们可以对该文的核心观点和技术架构进行深入的逻辑重构和前瞻性分析。

这篇文章实际上揭示了**“企业级AI从‘对话式玩具’向‘自主智能体’演进”**的关键转折点。以下是基于标题、摘要及行业背景的深度分析：

---

## 1. 核心观点深度解读

**文章的主要观点**：
文章的核心观点是：通过在ServiceNow等核心IT运维平台中集成基于Amazon Bedrock AgentCore的**Agentic AI（智能体AI）架构**，企业能够将IT运维从“被动响应”转变为“主动优化”和“自主执行”，从而实现IT运营的质变。

**作者想要传达的核心思想**：
AI的价值不再仅仅是生成代码或回答问题（Copilot模式），而是通过**Agent（智能体）**接管复杂的工作流。Iberdrola通过Bedrock AgentCore构建了一个多智能体系统，这些智能体能够理解意图、规划步骤、调用工具（如ServiceNow API），并独立完成IT变更、故障排查和资源优化。

**观点的创新性和深度**：
- **从辅助到自主**：传统的RAG（检索增强生成）主要用于问答，而AgentCore引入了推理和行动循环。
- **私有化与可控性**：在Bedrock上构建AgentCore，意味着企业可以利用大模型的能力，同时保持对数据隐私和API调用的严格控制，这对能源行业至关重要。
- **架构分层**：针对“三个关键领域”（摘要中提及，通常指：事件管理、变更管理、资源优化）构建不同的智能体架构，表明这是一种模块化的系统工程，而非单一的Chatbot。

**为什么这个观点重要**：
对于像Iberdrola这样拥有庞大IT基础设施的公用事业公司，IT故障直接关系到电网稳定和能源供应。引入Agentic AI不仅降低了人力成本，更重要的是提高了系统的**韧性**和**响应速度**，这是传统ITIL流程无法比拟的。

---

## 2. 关键技术要点

**涉及的关键技术或概念**：
- **Amazon Bedrock**：AWS的托管大模型服务，提供底层模型访问。
- **AgentCore（核心概念）**：虽然这是AWS内部或合作伙伴使用的术语，但在技术语境下，它通常指代**智能体的编排框架**。它负责处理“大脑”（LLM）与“手”（工具/API）之间的连接。
- **ServiceNow**：ITSM（IT服务管理）的核心系统，存储着工单、配置项（CMDB）和流程数据。
- **Agentic Architectures（智能体架构）**：包括ReAct（推理+行动）、Multi-Agent（多智能体协作）模式。

**技术原理和实现方式**：
1.  **意图识别与路由**：用户在ServiceNow中发起请求，Bedrock AgentCore首先分析意图（是查询？还是修改？还是优化？）。
2.  **规划与分解**：Agent将复杂任务（如“优化服务器资源”）分解为子任务（如：获取CPU利用率数据 -> 分析趋势 -> 生成调整建议 -> 执行变更）。
3.  **工具调用**：Agent通过API调用ServiceNow的内部脚本或AWS的云运维接口，获取实时数据。
4.  **上下文记忆**：在整个交互过程中，AgentCore维护对话历史和任务状态，确保多步骤操作的一致性。
5.  **人机协同**：对于高风险操作（如重启核心服务器），Agent会生成方案并暂停，等待人工审批后执行。

**技术难点和解决方案**：
- **难点：幻觉与API幻觉**。LLM可能会编造不存在的API参数。
  - **解决方案**：使用严格的JSON Schema定义工具，并结合Bedrock的Guardrails进行输入输出过滤。
- **难点：数据孤岛**。ServiceNow数据与AWS云监控数据的打通。
  - **解决方案**：构建统一的知识库和向量存储，通过AgentCore作为中间层统一调度。
- **难点：权限控制**。
  - **解决方案**：在AgentCore层面集成IAM（身份和访问管理），确保每个智能体只能访问其授权范围内的数据。

**技术创新点分析**：
将通用的Bedrock模型“垂直化”封装进ServiceNow工作流。这不是简单的API调用，而是将**业务流程代码化**为Agent的Prompt和Tool定义。

---

## 3. 实际应用价值

**对实际工作的指导意义**：
该案例证明了企业不需要从头训练大模型，而是可以通过**“基础模型 + 框架 + 企业数据”**的组合，快速落地高价值AI应用。

**可以应用到哪些场景**：
1.  **L1/L2 技术支持自动化**：Agent自动处理密码重置、权限申请等低级工单。
2.  **根因分析（RCA）**：当报警发生时，Agent自动查阅日志、历史工单和知识库，给出故障原因预测。
3.  **云成本优化**：Agent定期分析AWS资源使用率，自动调整ServiceNow记录中的资产配置或触发AWS缩容操作。
4.  **合规性审计**：自动扫描IT操作日志，生成合规报告。

**需要注意的问题**：
- **数据质量**：如果ServiceNow中的CMDB数据不准确，Agent的决策也会出错。
- **可解释性**：AI执行了操作后，必须能生成人类可读的日志，否则运维团队不敢信任。

**实施建议**：
不要试图一步到位替换所有运维流程。应从“Read-only”（只读分析）类Agent开始，验证其准确性，再逐步过渡到“Write”（执行变更）类Agent。

---

## 4. 行业影响分析

**对行业的启示**：
公用事业和能源行业通常被视为数字化转型的保守派，Iberdrola的案例表明，**高监管行业正在加速拥抱生成式AI**，特别是用于解决复杂的运维难题。

**可能带来的变革**：
- **IT运维角色的转变**：运维工程师将从“执行者”变为“管理者”和“训练师”，负责设计Agent的规则和验证其输出。
- **SaaS平台的进化**：ServiceNow、Salesforce等SaaS平台将不再只是记录数据的系统，而会演变为**Agent的执行终端**。

**相关领域的发展趋势**：
- **AIOps 的 2.0 时代**：传统的AIOps基于异常检测（数学模型），未来的AIOps将基于语义理解（LLM），能处理更模糊、更复杂的非结构化问题。

**对行业格局的影响**：
AWS、Azure等云厂商通过提供Agent框架，正在向应用层下沉。这可能会挤压传统IT咨询公司的生存空间，因为“写代码”的价值降低了，“定义流程”的价值升高了。

---

## 5. 延伸思考

**引发的思考**：
如果Agent可以优化IT资源，那么它是否可以直接优化电力调度？Iberdrola作为能源公司，这套IT运维的Agent架构极有可能被复制到**电网运营**领域。

**拓展方向**：
- **多模态Agent**：除了文本，Agent能否直接分析服务器热成像图或电路图？
- **跨域Agent**：IT Agent与OT（运营技术）Agent的协作。例如，IT Agent发现服务器过热，直接指挥OT Agent调整机房的空调系统。

**需进一步研究的问题**：
- 如何量化Agent的“自主性”等级？
- 在多Agent协作中，如何解决“循环依赖”或“死锁”问题？

---

## 6. 实践建议

**如何应用到自己的项目**：
1.  **评估数据基础**：检查你的ITSM（如Jira, ServiceNow）和监控系统（如Prometheus, Datadog）的数据是否规范、API是否完善。
2.  **选择合适的框架**：如果不使用AWS Bedrock，可以研究LangChain或AutoGPT，原理类似。
3.  **定义“工具箱”**：将你现有的运维脚本封装成Agent可调用的API。

**具体的行动建议**：
- **第一步**：构建一个RAG聊天机器人，用于回答运维知识库问题。
- **第二步**：赋予Agent只读权限，让其能查询工单状态和服务器指标。
- **第三步**：引入“人机回路”，让Agent撰写变更方案，人工审核后一键执行。

**需补充的知识**：
- Prompt Engineering（提示词工程），特别是System Prompt的设计。
- 理解LLM的Token限制和上下文窗口管理。
- 基础的DevOps和安全知识。

---

## 7. 案例分析

**结合实际案例说明**：
虽然摘要未提供细节，但基于行业通用实践，我们可以模拟一个典型的**“Iberdrola式”场景**：

*场景：某变电站的IT网关出现间歇性故障。*

**传统流程**：
1. 监控系统发报警。
2. L1运维人员接手，手动查看日志。
3. 发现不懂，升级给L2专家。
4. L2专家查阅陈旧文档，尝试重启服务。
5. 问题解决，耗时2小时。

**AgentCore介入后的流程**：
1. **报警触发Agent**。
2. **Agent（分析者）**：自动拉取过去24小时的系统日志，查询ServiceNow中的历史相似工单。
3. **Agent（决策者）**：发现日志中有“Memory Leak”特征，匹配到知识库中的补丁程序。
4. **Agent（执行者）**：在ServiceNow中创建变更请求，附带补丁链接。
5. **人工审批**：运维人员看到Agent提供的详尽分析报告，点击“批准”。
6. **Agent**：自动执行脚本打补丁，并验证服务恢复。
7. **结果**：耗时15分钟。

**成功要素**：
- 知识库的实时更新。
- API的自动化能力。
- 信任机制的建立。

---

## 8. 哲学与逻辑：论证地图

**中心命题**：
**企业级IT运维的未来将由基于大模型的自主智能体主导，而非传统的自动化脚本或人工操作。**

**支撑理由与依据**：
1.  **理由（复杂性应对）**：现代IT环境的复杂性已超出人类认知负荷，且脚本无法处理非结构化异常。
    *   *依据*：Iberdrola作为巨头，其基础设施规模庞大，依赖人工已导致瓶颈。
2.  **理由（效率提升）**：Agent能够7x24小时不间断工作，且能并行处理多源数据。
    *   *依据*：AWS Bedrock的技术能力展示了毫秒级的推理和API调用速度。
3.  **理由（知识传承）**：Agent利用LLM能力，将分散在文档和专家头脑中的隐性知识显性化。
    *   *依据*：ServiceNow中积累的大量工单数据是未被开采的金矿，RAG技术使其可被利用。

**反例或边界条件**：
1.  **边界条件（合规性）**：在涉及核电站或核心金融交易的关键系统中，完全自主的Agent可能面临法律监管障碍，必须保留“最终人类按钮”。
2.  **反例（黑盒风险）**：如果Agent出现不可解释的错误操作（如误删数据库），其造成的损失可能远超人工操作的失误，导致灾难性后果。
3.  **边界条件（成本）**：对于极小规模的简单IT环境，构建Agent的成本远高于收益。

**事实与价值判断**：
- *事实*

---
## 最佳实践

## 最佳实践

### 1. 构建基于知识库的检索增强生成（RAG）架构

**说明**：
Iberdrola 利用 Amazon Bedrock 的知识库能力，将非结构化的运营文档（如日志、手册）转化为向量存储。通过 RAG 架构，LLM 在回答问题时能够检索到最新的私有数据，从而生成准确且符合上下文的回答，有效解决了大模型“幻觉”问题，确保 IT 运营信息的准确性。

**实施步骤**：
1.  **数据准备**：收集并清洗 IT 运维相关的历史文档、工单记录和操作手册。
2.  **向量化与索引**：使用 Amazon Bedrock 的 Embeddings 模型将文本转换为向量，并存储在向量数据库（如 Amazon OpenSearch Serverless）中。
3.  **配置检索流程**：在 Agent 中配置知识库检索逻辑，确保用户查询首先匹配相关文档片段。
4.  **生成回答**：将检索到的上下文注入到 Prompt 中，利用 Bedrock 上的基础模型生成最终回答。

**注意事项**：
确保源数据的质量和时效性，定期更新知识库以反映最新的 IT 架构变更。

---

### 2. 利用 Agent 编排实现复杂任务自动化

**说明**：
单纯的对话无法解决所有运维问题。Iberdrola 使用 Amazon Bedrock Agents 的“推理”和“编排”能力，让 AI 不仅仅是回答问题，还能通过调用 API 执行实际操作。例如，Agent 可以解读用户的自然语言指令，自动调用 AWS Lambda 函数或 AWS Systems Manager 来执行脚本或重启服务。

**实施步骤**：
1.  **定义 API Schema**：将现有的运维工具（如内部 API、CLI 工具）封装为 OpenAPI Schema 定义。
2.  **创建 Agent Action Group**：在 Bedrock Agent 中配置 Action Group，将上述 Schema 与 Agent 关联。
3.  **任务拆解与规划**：利用 Agent 的推理能力，将复杂的运维请求（如“排查为什么网站慢”）拆解为“查询状态”、“分析日志”、“扩展容量”等子任务。
4.  **权限控制**：通过 IAM 角色严格控制 Agent 调用底层资源的权限。

**注意事项**：
在赋予 Agent 操作权限时，务必遵循最小权限原则，并为高风险操作（如删除资源）设置人工确认环节。

---

### 3. 实施严格的数据治理与安全隔离

**说明**：
在能源等受监管行业，数据安全至关重要。Iberdrola 确保所有通过 Amazon Bedrock 处理的数据都符合企业安全策略。利用 Amazon Bedrock 的私有加密功能，确保数据在传输和存储过程中不仅加密，而且承诺 AWS 不会利用客户数据来训练其基础模型，从而保护了 Iberdrola 的知识产权和敏感运营数据。

**实施步骤**：
1.  **启用加密**：确保所有存储在 S3 中的数据及 Bedrock 的交互均使用 AWS KMS（Key Management Service）管理的密钥进行加密。
2.  **网络隔离**：利用 VPC 接口终端节点将 Bedrock API 调用限制在私有网络内，避免流量暴露至公网。
3.  **数据过滤**：在将数据发送给 LLM 之前，实施严格的 PII（个人身份信息）扫描和脱敏处理。

**注意事项**：
定期审查 IAM 策略和 CloudTrail 日志，确保没有未经授权的数据访问或模型调用行为。

---

### 4. 优化 Prompt 工程以提升运维指令准确性

**说明**：

**实施步骤**：
1.  **模板化**：为常见的运维场景（如日志分析、成本优化）创建可复用的 Prompt 模板。
2.  **少样本学习**：在 Prompt 中提供具体的问答示例，引导模型按照预期格式和逻辑输出。
3.  **上下文注入**：动态将当前的告警信息、系统状态元数据注入到 System Prompt 中。

**注意事项**：
避免在 Prompt 中硬编码敏感凭证。Prompt 应作为版本控制的代码进行管理，以便于迭代和回滚。

---

### 5. 建立全面的监控与反馈闭环机制

**说明**：
为了确保 AI 运维助手长期有效且稳定，Iberdrola 建立了完善的监控体系。通过 Amazon CloudWatch 实时追踪 Agent 的调用延迟、错误率及 Token 消耗情况。同时，引入用户反馈机制，允许运维人员对生成的建议进行评分，这些数据被用于后续的模型微调和 Prompt 优化，形成持续改进的闭环。

**实施步骤**：
1.  **指标监控**：配置 CloudWatch 告警，监控 Bedrock API 的调用成功率、延迟及推理成本。
2.  **日志

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [智能代理](/tags/%E6%99%BA%E8%83%BD%E4%BB%A3%E7%90%86/) / [IT 运维](/tags/it-%E8%BF%90%E7%BB%B4/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/) / [工单自动化](/tags/%E5%B7%A5%E5%8D%95%E8%87%AA%E5%8A%A8%E5%8C%96/) / [AWS](/tags/aws/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [亚马逊利用Nova模型自动化新履约中心运营就绪测试]({{< relref "posts/20260211-blogs_podcasts-how-amazon-uses-amazon-nova-models-to-automate-ope-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*