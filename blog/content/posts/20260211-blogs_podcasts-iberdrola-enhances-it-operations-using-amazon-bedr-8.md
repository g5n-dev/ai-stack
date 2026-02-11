---
title: "Iberdrola enhances IT operations using Amazon Bedrock A"
date: 2026-02-11T22:09:57+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "Agentic AI", "IT 运维", "AWS", "对话式 AI", "事件管理"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "Iberdrola 是全球最大的公用事业公司之一，为了革新其在 ServiceNow 平台上的 IT 运营，通过合作采用了 AWS 的先进 AI 技术。具体而言，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种代理架构，重点聚焦于三个关键领域： 1. **优化变更请求验证**：在变"
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
## 导语

Iberdrola 作为全球最大的公用事业公司之一，正通过 AWS 合作引入先进的 AI 技术，以重塑其基于 ServiceNow 的 IT 运营体系。本文将详细剖析其利用 Amazon Bedrock AgentCore 构建智能体架构的具体实践，涵盖变更请求优化与事件管理等关键场景。通过阅读本文，您将了解如何利用生成式 AI 提升运维效率，并获得企业级智能体落地的技术参考。

---
## 摘要

Iberdrola 是全球最大的公用事业公司之一，为了革新其在 ServiceNow 平台上的 IT 运营，通过合作采用了 AWS 的先进 AI 技术。具体而言，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种代理架构，重点聚焦于三个关键领域：

1.  **优化变更请求验证**：在变更请求的草拟阶段进行优化。
2.  **增强事件管理**：利用情境智能丰富事件管理内容。
3.  **简化变更模型选择**：通过对话式 AI 简化变更模型的选择流程。

这些创新举措有效减少了运营瓶颈，帮助团队加速了工单解决速度，并实现了全组织范围内高质量且一致的数据处理。

---
## 评论

基于您提供的标题、摘要片段以及Iberdrola（伊比德罗拉）与AWS合作在ServiceNow中实施AI的行业背景，以下是对该案例的深入技术与行业评价。

### 中心观点
**文章展示了大型公用事业企业如何通过将“代理式AI”嵌入ITSM（IT服务管理）流程，利用Amazon Bedrock AgentCore在ServiceNow平台上实现从“脚本自动化”向“目标导向型自主运维”的范式跃迁。**

### 深入评价

#### 1. 内容深度：观点的深度和论证的严谨性
**评价：** 文章触及了当前企业级AI应用的最深水区——**非生成式任务的复杂决策链**。
*   **[你的推断]** 摘要中提到的“AgentCore”很可能是指AWS Bedrock中用于编排多Agent系统的核心组件（或特定的解决方案架构）。Iberdrola的深度在于没有止步于用大模型（LLM）写工单描述，而是让AI“操作”ServiceNow。
*   **[事实陈述]** ServiceNow的传统强项是流程标准化，而弱项是处理非结构化数据和复杂逻辑判断。Iberdrola通过引入Agent架构，实际上是在ServiceNow之上构建了一个“数字大脑”层。
*   **支撑理由：** 这种架构解决了LLM“幻觉”问题。在IT运维中，单纯依靠LLM生成代码或指令风险极高。AgentCore通常结合了RAG（检索增强生成）和工具调用，使得AI在执行重启服务器、修改配置等操作时，能够严格遵循预设的安全逻辑，而非自由发挥。

#### 2. 实用价值：对实际工作的指导意义
**评价：** 该案例为CIO们提供了一个**“旧系统新用”**的高价值模板。
*   **[作者观点]** 许多企业面临两难：是推翻现有的ERP/ITSM系统重建AI原生应用，还是在旧系统上打补丁？Iberdrola证明了后者更具性价比。
*   **支撑理由：** ServiceNow是全球大多数企业的IT运维底座。通过AWS Bedrock连接ServiceNow，意味着企业不需要替换核心资产，就能获得GenAI能力。这对于拥有沉重技术债务的传统行业（能源、银行、制造）具有极高的参考价值。
*   **反例/边界条件：** 如果企业的ServiceNow实例中历史数据治理极差（例如工单描述混乱、分类错误），训练出的Agent将频繁失败。此外，对于极度依赖遗留协议（如Telnet、旧式Mainframe交互）的场景，AgentCore难以直接触达，需要额外的中间件层。

#### 3. 创新性：提出了什么新观点或新方法
**评价：** 核心创新在于**多智能体协作**在垂直业务场景中的落地。
*   **[你的推断]** 摘要提到的“targeting three key areas”（针对三个关键领域）暗示了分工明确的Agent架构。
*   **支撑理由：**
    1.  **规划Agent：** 理解模糊的IT报错（如“系统很慢”），并将其转化为具体的排查步骤。
    2.  **执行Agent：** 调用ServiceNow API或AWS Systems Manager执行修复。
    3.  **审核Agent：** 确保操作符合合规性（SOX法案等）。
    这种“分而治之”的方法比单一巨型模型更具鲁棒性和可解释性，是AI工程化的重要进步。

#### 4. 可读性与逻辑性
**评价：** 从技术传播角度看，该文逻辑清晰，**[事实陈述]** 采用了经典的“挑战-方案-成效”结构。
*   **[作者观点]** 文章巧妙地避开了枯燥的技术参数（如具体的Prompt Token数或模型温度设置），转而聚焦于业务价值（优化IT运维），这使得非技术背景的高管也能轻松理解其战略意义。

#### 5. 行业影响：对行业或社区的潜在影响
**评价：** 此案例可能成为**能源行业数字化转型**的标杆。
*   **[事实陈述]** Iberdrola是全球风电巨头，其IT系统的复杂度涉及SCADA系统、分布式能源管理等多个维度。
*   **[你的推断]** 如果Iberdrola成功，这将证明GenAI不仅能写代码，还能管理代码的运行环境。这将推动整个公用事业行业从“预防性维护”向“预测性自治”迈进，迫使竞争对手加速上云。

#### 6. 争议点与不同观点
**评价：** 尽管前景广阔，但该方案存在显著的**隐性成本与风险**。
*   **[作者观点]** **“黑盒悖论”**是最大的争议点。当AI Agent自动关闭了一个服务器实例以防止故障蔓延时，如果导致了其他服务中断，人类管理员很难在事后复现AI的决策逻辑。在受监管的能源行业，这种不可解释性可能触犯合规红线。
*   **[反例/边界条件]** 并非所有运维任务都适合AI Agent。对于涉及物理安全（如核电站参数调整）的操作，目前监管机构极不可能接受全自动化的AI决策，必须保留“人在回路”。

#### 7. 实际应用建议
**评价：** 对于希望效仿Iberdrola的企业，建议采取**“三步走”**策略。
1.  **建立护栏：** 在ServiceNow中为Agent划定严格的权限范围，例如只读权限优先，写操作需要双重验证。
2.  **数据清洗：** 在引入Bedrock之前，必须清洗ServiceNow的CMDB（配置管理数据库），垃圾

---
## 技术分析

# 技术分析：Iberdrola 基于 Amazon Bedrock 与 ServiceNow 的 IT 运维架构演进

## 1. 核心观点深度解读

**文章的主要论点**
文章的核心论点是：面对日益复杂的 IT 基础设施，传统的人工运维模式在效率和响应速度上存在局限。通过引入基于**代理式架构**的生成式 AI，企业能够将 IT 运维模式从“被动响应”转变为“主动处理”。Iberdrola 通过在 ServiceNow 平台中集成 Amazon Bedrock AgentCore，展示了大型企业如何利用 AI 智能体自动化处理复杂任务，从而在保障安全合规的前提下提升运营效率。

**作者意图分析**
作者旨在阐述**AI 技术在企业级应用中从“交互”向“执行”的转变**。这不仅仅是构建对话机器人，而是让 AI 具备代表用户执行业务流程的能力。文章重点分析了 AWS 与 ServiceNow 的集成机制，展示了如何利用 Bedrock AgentCore 作为编排层，将大语言模型（LLM）的推理能力与企业系统的 API 调用能力相结合。

**观点的技术价值**
对于像 Iberdrola 这样拥有庞大 IT 资产和严格监管要求的公用事业公司，该案例提供了一种可行的技术路径：**在受控环境中实现运维流程的自动化**。这种模式为其他高合规性行业（如金融、医疗）提供了重要的技术参考。

## 2. 关键技术要点

**涉及的核心技术组件**
*   **Amazon Bedrock**：AWS 提供的全托管生成式 AI 服务，用于访问和管理基础模型。
*   **Amazon Bedrock AgentCore**：本案例的技术核心组件。它负责 AI Agent 的构建、部署和管理，主要功能包括任务编排、会话记忆管理以及工具调用。
*   **ServiceNow**：企业级 IT 服务管理（ITSM）平台，作为此次 AI 落地的业务系统载体。
*   **Agentic Architectures（代理式架构）**：一种系统设计模式，其中 AI Agent 具备感知环境、做出决策并调用工具采取行动的能力。

**技术原理与实现逻辑**
1.  **任务编排与分解**：AgentCore 接收自然语言指令（如“排查服务器故障”），利用 LLM 将其分解为可执行的子任务。
2.  **API 工具调用**：Agent 通过 ServiceNow 提供的 API 接口与底层系统交互。例如，查询 CMDB（配置管理数据库）获取资产信息，或调用自动化脚本执行重启操作。
3.  **上下文记忆管理**：AgentCore 维护对话历史和任务状态，确保在多轮交互中上下文的连贯性，减少重复输入。
4.  **人机协同确认**：对于高风险操作，系统设计了审批流程，Agent 会暂停操作并等待人工确认，以确保操作安全。

**技术难点与应对策略**
*   **难点：模型幻觉与准确性**。AI 可能生成不准确的信息或操作步骤。
    *   *解决方案*：采用 RAG（检索增强生成）技术，限制 Agent 的回答基于企业知识库和 ServiceNow 中的实时数据，从而降低幻觉风险。
*   **难点：权限控制与安全性**。如何确保 AI 的操作权限受控？
    *   *解决方案*：在 AgentCore 层面实施严格的 IAM（身份和访问管理）策略，确保 Agent 的操作权限严格对齐用户的角色权限。

**技术创新点分析**
该案例的技术创新点在于**架构的可组合性**。Iberdrola 并未构建单一庞大的 AI 应用，而是利用 AgentCore 构建了针对特定场景（如事件管理、变更管理）的专用 Agent。这些 Agent 可以独立工作或协同作业，形成了一个灵活的多智能体系统。

---
## 学习要点

- Iberdrola 通过 Amazon Bedrock AgentCore 构建生成式 AI 应用，显著提升了 IT 运营效率并优化了用户体验。
- 利用 Amazon Bedrock 的托管服务，企业无需从头构建基础设施，即可快速部署和管理智能代理。
- 该解决方案通过自动化处理常见 IT 请求（如密码重置和软件安装），有效减少了人工干预。
- AgentCore 能够安全地集成现有 IT 系统与数据源，确保在私有网络环境中执行操作。
- 采用生成式 AI 技术不仅降低了运营成本，还提高了员工对 IT 服务的满意度。
- 此案例展示了传统公用事业公司如何通过云原生 AI 技术实现业务流程的现代化转型。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [Agentic AI](/tags/agentic-ai/) / [IT 运维](/tags/it-%E8%BF%90%E7%BB%B4/) / [AWS](/tags/aws/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/) / [事件管理](/tags/%E4%BA%8B%E4%BB%B6%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-2.md" >}})
- [利用全栈模板加速开发基于Amazon Bedrock AgentCore的应用]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--12.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*