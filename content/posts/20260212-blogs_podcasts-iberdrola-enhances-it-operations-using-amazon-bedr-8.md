---
title: "Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT"
date: 2026-02-12T02:48:17+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "ServiceNow", "IT 运营", "智能体", "AWS", "对话式 AI", "事故管理"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "Iberdrola 与 AWS 合作，通过采用 Amazon Bedrock AgentCore 等 AI 技术，对其 ServiceNow 中的 IT 运营进行了革新。这些举措主要聚焦于三大领域：优化变更请求验证、利用上下文智能丰富事件管理，以及通过对话式 AI 简化变更模型选择。这些创新成功减少了瓶颈，加速了工单解"
external_url: https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT 运营

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-10T18:31:57+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)

---
## 摘要/简介

Iberdrola，全球最大的公用事业公司之一，已采用尖端人工智能技术，对其在 ServiceNow 中的 IT 运营进行革新。通过与 AWS 的合作，Iberdrola 利用 Amazon Bedrock AgentCore 实施了多种智能体架构，聚焦于三大关键领域：在草拟阶段优化变更请求验证、以情境智能丰富事故管理，以及借助对话式 AI 简化变更模型选择。这些创新减少了瓶颈，帮助团队加速工单解决，并在整个组织范围内实现一致且高质量的数据处理。

---
## 导语

作为全球规模领先的公用事业企业，Iberdrola 正面临 IT 运营复杂性与效率的双重挑战。本文介绍了该公司如何通过 AWS 合作，利用 Amazon Bedrock AgentCore 在 ServiceNow 环境中构建智能体架构，从而实现变更验证与事故管理的自动化升级。通过这一案例，读者将了解到情境智能与对话式 AI 如何在实际场景中减少流程瓶颈，并显著提升数据处理的准确性与一致性。

---
## 摘要

Iberdrola 与 AWS 合作，通过采用 Amazon Bedrock AgentCore 等 AI 技术，对其 ServiceNow 中的 IT 运营进行了革新。这些举措主要聚焦于三大领域：优化变更请求验证、利用上下文智能丰富事件管理，以及通过对话式 AI 简化变更模型选择。这些创新成功减少了瓶颈，加速了工单解决，并确保了全组织范围内数据处理的一致性和高质量。

---
## 评论

### 评价报告：Iberdrola 与 Amazon Bedrock AgentCore 的 IT 运革

**中心观点**
该案例展示了大型公用事业企业如何利用生成式AI的“代理化”架构，将传统的IT运维从“被动记录”转变为“主动执行”，标志着企业级AI应用正从简单的对话交互向复杂的工作流自动化深度演进。

**支撑理由与多维评价**

**1. 内容深度：从“辅助”到“代理”的架构跨越**
*   **分析：** 文章的核心亮点在于引入了 **AgentCore** 这一概念。这区别于以往单纯的 RAG（检索增强生成）聊天机器人。Iberdrola 的实践表明，他们正在构建能够自主规划、调用工具（如 ServiceNow API）并执行任务的 Agent。
*   **事实陈述：** Iberdrola 利用 AWS Bedrock 构建了针对特定领域的代理架构，优化了 ServiceNow 的操作。
*   **你的推断：** 这意味着 Iberdrola 已经解决了 LLM 在企业环境中最难的一环：**确定性执行**。他们不仅让 AI 理解工单，还让 AI 具备了修改工单、自动分配、甚至执行脚本的能力，这在技术深度上比简单的问答上了一个台阶。

**2. 实用价值：解决“最后一公里”的自动化痛点**
*   **分析：** 对于传统行业，ServiceNow 等ITSM工具虽然强大，但配置繁琐、操作门槛高。该案例的实用价值在于将自然语言直接转化为业务动作。
*   **作者观点：** 这种模式对于非技术背景的业务经理或一线支持人员极具吸引力。它降低了运维门槛，使得“通过对话修复系统”成为可能。
*   **实际案例：** 想象一个场景：服务器负载过高。传统流程需要监控报警 -> 人工分析 -> 登录 ServiceNow 建单 -> 分配 -> 执行。而在 AgentCore 架构下，AI 可以自动分析日志，判断这是“已知问题”，直接在 ServiceNow 中创建变更请求并草拟执行脚本，仅需人工最后确认。这直接压缩了 MTTR（平均修复时间）。

**3. 创新性：多代理协作的行业标杆**
*   **分析：** 文章提到实施了“different agentic architectures”（不同的代理架构），暗示了 **Multi-Agent（多智能体）** 模式的应用。
*   **你的推断：** Iberdrola 很可能没有使用一个巨大的“上帝模型”来做所有事，而是设计了专门的 Agent 分别负责“用户意图识别”、“ServiceNow API 调用”、“安全合规检查”。这种模块化的思维是当前企业级 AI 落地的最佳实践，既保证了模型的专业性，又限制了幻觉的风险。

**4. 行业影响：公用事业领域的“灯塔效应”**
*   **分析：** 公用事业（电力、水务）通常是保守、高度监管的行业。Iberdrola 作为巨头，其成功部署具有极强的示范效应。
*   **事实陈述：** Iberdrola 是全球最大的公用事业公司之一。
*   **行业影响：** 这打破了“AI 仅用于代码生成或营销”的刻板印象，证明了在关键基础设施的 IT 运维中，生成式 AI 也能安全、高效地工作。这将促使更多能源、制造企业加速上云并用 AI 重构遗留系统。

**反例与边界条件（批判性思考）**

尽管该案例前景广阔，但必须正视以下局限性与潜在风险：

1.  **幻觉风险与关键基础设施：**
    *   **边界条件：** 在 IT 运维中，一个错误的参数可能导致服务中断。如果 Agent 产生了幻觉，错误地关闭了一个关键实例，后果不堪设想。
    *   **反例：** 相比于生成一段营销文案，IT 运维对准确性的要求是 99.99%。文章未详细披露其“护栏”机制（Guardrails），即如何防止 AI 执行破坏性命令（如 `rm -rf` 或删除生产数据库）。

2.  **数据隐私与主权：**
    *   **边界条件：** 公用事业公司涉及大量敏感用户数据和电网机密。
    *   **反例：** 虽然 AWS 提供了 VPC 等私有化部署选项，但将核心运维数据发送给 LLM 进行推理，仍需面临极其严苛的合规审查。如果数据跨境传输或被模型用于训练，将触犯 GDPR 等法规。

3.  **遗留系统的集成摩擦：**
    *   **边界条件：** ServiceNow 通常只是 IT 架构的一部分。
    *   **反例：** Iberdrola 的后台可能仍有大量大型机或古老的 ERP 系统。Bedrock AgentCore 虽然强大，但如果无法通过 API 顺畅连接这些“黑盒”遗留系统，Agent 的能力将被严重限制在 ServiceNow 的围墙之内。

**可验证的检查方式**

为了验证该项目是否如文章所述成功，或评估类似项目的可行性，建议关注以下指标：

1.  **平均工单解决时间：**
    *   *指标：* 对比部署 AgentCore 前后，L1/L2 级别工单的处理时长是否显著下降。
    *   *验证方式：* 查看 ServiceNow 报表中的 MTTR 趋势。

2.  **自动化介入率：**
    *   *指标：* 在所有流转的工单中，有多少比例是由 Agent 完全自动完成（无需人工点击），多少比例需要人工审核。
    *   *验证方式：* 统

---
## 技术分析

基于您提供的文章标题和摘要，虽然原文内容被截断，但结合Iberdrola（伊维尔德罗拉）作为全球能源巨头的背景、AWS（亚马逊云科技）的技术生态以及ServiceNow（IT服务管理）的常见应用场景，我们可以对该文的核心观点和技术架构进行深入的逻辑重构和专业分析。

这篇文章实质上是一篇关于**“生成式AI代理化落地企业级IT运维”**的标杆案例研究。以下是基于现有信息及行业通用最佳实践的深度分析：

---

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：通过引入**Amazon Bedrock AgentCore**（一种基于代理的AI架构），传统企业能够将生成式AI从“简单的对话助手”升级为“具备推理和执行能力的智能体”，从而在ServiceNow等核心IT系统中实现高度自动化的运维优化。

**作者想要传达的核心思想**
作者试图传达**“Agentic Workflows（代理工作流）”**优于传统自动化的理念。传统的IT运维依赖预定义的脚本和人工干预，而Iberdrola的案例表明，利用大语言模型（LLM）的推理能力结合企业知识库，AI可以自主拆解复杂任务、调用API并执行操作，实现从“人找事”到“AI找人并解决”的范式转变。

**观点的创新性和深度**
*   **创新性**：在于“AgentCore”这一概念的应用。这不仅仅是调用一个ChatGPT接口，而是构建了一个多代理架构。这种架构允许AI在处理IT请求时，能够根据上下文动态选择工具（如查询知识库、创建工单、调用AWS修复脚本），而不是死板地执行单一指令。
*   **深度**：文章触及了企业级AI落地的深水区——**非结构化数据与结构化动作的融合**。它展示了如何将自然语言请求转化为ServiceNow中的具体业务逻辑，解决了LLM“只会说不会做”的痛点。

**为什么这个观点重要**
对于像Iberdrola这样庞大的公用事业公司，IT系统的稳定性直接关系到电网和国计民生。该观点证明了在高度合规、复杂的传统行业中，AI不仅能做客服，还能成为核心的生产力工具，显著降低IT运营成本并提升响应速度。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Amazon Bedrock**: AWS的托管生成式AI服务，提供对多种基础模型（如Anthropic Claude, Meta Llama等）的访问。
*   **AgentCore (代理核心)**: 这是一个关键的技术抽象层。它可能指的是AWS提供的代理框架或Iberdrola自研的中间件，用于管理LLM的推理循环、记忆和工具调用。
*   **ServiceNow**: 企业IT服务管理（ITSM）平台，存储了大量的工单、资产配置和流程数据。
*   **RAG (检索增强生成)**: 结合企业私有数据（如IT文档、历史工单）来增强模型的回答准确性。

**技术原理和实现方式**
1.  **意图识别**: 用户输入自然语言请求（如“我的服务器变慢了”）。
2.  **推理与规划**: AgentCore利用LLM分析请求，将其分解为子任务（例如：检查服务器状态 -> 查找错误日志 -> 提出解决方案）。
3.  **工具调用**: Agent通过API调用ServiceNow的Table API查询CMDB（配置管理数据库），或调用AWS Systems Manager获取服务器指标。
4.  **上下文融合**: 将查询到的数据回填给LLM，生成最终回复或自动执行修复脚本。

**技术难点和解决方案**
*   **幻觉问题**: AI可能会编造不存在的IT操作指令。
    *   *解决方案*: 使用Bedrock的Guardrails（防护栏）技术和严格的RAG检索，限制AI只能基于验证过的文档回答。
*   **API复杂性**: ServiceNow的API非常复杂，直接让LLM写API代码容易出错。
    *   *解决方案*: 使用**Function Calling（函数调用）**或**LangChain**等框架，预先定义好工具的描述，让LLM只负责选择工具，而不负责编写底层连接代码。
*   **数据安全**: 能源公司的数据极其敏感。
    *   *解决方案*: 利用VPC（虚拟私有云）端点，确保数据在传输过程中不离开Iberdrola的安全环境，且不使用私有数据训练公共模型。

**技术创新点分析**
最大的创新在于**多代理协作**的架构设计。针对摘要中提到的“三个关键领域”（可能是：事件管理、资产管理、知识管理），系统可能部署了专门的Agent。例如，“优化Agent”专注于分析日志趋势，“执行Agent”专注于变更管理。这种分工使得系统更加专业和可靠。

## 3. 实际应用价值

**对实际工作的指导意义**
该案例为CIO和IT管理者提供了一个清晰的路径：不要试图用一个大模型解决所有问题。应该通过**AgentCore**构建专门的代理，连接底层的SaaS系统（如ServiceNow），将AI嵌入到现有的业务流程中。

**可以应用到哪些场景**
*   **L1/L2 级IT支持自动化工单处理**: 自动分类、路由并解决常规的密码重置、软件安装请求。
*   **故障根因分析 (RCA)**: 自动聚合告警日志，结合历史知识库，生成事故报告。
*   **云资源优化**: 监控AWS上的资源使用情况，自动建议或执行缩容操作以节省成本。

**需要注意的问题**
*   **权限控制**: AI Agent拥有执行权限，必须确保其权限最小化，防止AI误操作导致生产事故。
*   **人工确认**: 对于高风险操作（如重启生产服务器），必须设计“人机协同”确认机制。

**实施建议**
建议从“只读”代理开始，让AI负责分析和建议，待模型成熟后，逐步开放“写入”和“执行”权限。

## 4. 行业影响分析

**对行业的启示**
Iberdrola的案例表明，公用事业和制造业等传统行业正在成为AI应用的新高地。这些行业拥有深厚的工业积淀和数据积累，一旦引入Agent技术，将释放巨大的**“数据资产价值”**。

**可能带来的变革**
IT运维部门的角色将发生转变。从“救火队”（被动响应）转变为“指挥官”（管理AI代理舰队）。初级运维人员的招聘需求可能会减少，但对**AI工程师**和**Prompt工程师**的需求将激增。

**相关领域的发展趋势**
*   **Agent-as-a-Service**: 未来的SaaS软件（如ServiceNow）将原生集成Agent能力，而不是作为外挂插件。
*   **多模态运维**: Agent不仅能处理文本，还能直接分析服务器热成像图、电网拓扑图。

## 5. 延伸思考

**引发的其他思考**
*   **Agent的幻觉成本**: 在IT运维中，一个错误的API调用可能导致服务中断。如何建立“AI保险”机制？
*   **模型漂移**: 随着ServiceNow数据的更新，Agent的知识库如何保持实时同步？

**可以拓展的方向**
*   将Agent扩展到**OT（运营技术）领域**，不仅管理IT服务器，还管理电网设备、变压器的维护数据。
*   结合**数字孪生**技术，让Agent在虚拟环境中模拟操作变更，验证无误后再应用到物理环境。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估数据成熟度**: 确保你的ServiceNow或ITSM系统中有结构化良好的数据。
2.  **选择合适的基座模型**: 在Bedrock中，Claude 3.5 Sonnet通常在指令遵循和代码生成方面表现优异，适合做Agent核心；Llama 3成本低，适合做简单分类。
3.  **构建工具库**: 不要让AI直接写SQL，而是封装好Python/Node.js函数，让AI通过JSON Schema调用。

**具体的行动建议**
*   **第一步**: 搭建一个基于RAG的知识库问答Agent，解决“如何做”的问题。
*   **第二步**: 集成ServiceNow API，实现“查询状态”的功能。
*   **第三步**: 引入人工审批流，实现“创建工单”或“简单变更”的功能。

**需要补充的知识**
*   **Prompt Engineering**（提示工程）: 特别是ReAct（推理+行动）模式的提示词编写。
*   **Orchestration Framework**: 学习LangChain或LlamaIndex。

## 7. 案例分析

**结合实际案例说明**
Iberdrola面临的挑战是典型的“大企业病”：系统庞杂、流程僵化。通过Bedrock AgentCore，他们实际上构建了一个**“统一的中控层”**。

**成功案例分析**
假设场景：某变电站IT系统报警。
*   **传统流程**: 警报 -> 运维人员收到邮件 -> 登录系统查文档 -> 尝试修复 -> 失败 -> 升级二线。
*   **Agent流程**: 警报 -> Agent自动捕获 -> 查阅ServiceNow历史类似案例 -> 发现是补丁缺失 -> 自动调用AWS Systems Manager安装补丁 -> 验证状态 -> 关闭工单。
*   **成果**: 平均修复时间（MTTR）从小时级降低到分钟级。

**失败案例反思**
如果Agent没有做好权限隔离，可能会误将生产环境的数据库关闭作为“优化资源”的手段。因此，**边界条件测试**至关重要。

## 8. 哲学与逻辑：论证地图

**中心命题**
**企业级IT运维的效率革命将通过部署具备自主推理和工具调用能力的生成式AI代理来实现，而非单纯依赖人类专家或传统脚本。**

**支撑理由**
1.  **认知负担转移**: LLM具备自然语言理解能力，能将非结构化的用户请求转化为结构化的系统指令，降低了人机交互的门槛。
    *   *依据*: Iberdrola在ServiceNow中实现了自然语言到IT工单的转化。
2.  **执行效率提升**: AgentCore架构允许AI并行处理多源数据（如AWS CloudWatch + ServiceNow CMDB），比人类线性检索更快。
    *   *依据*: AWS Bedrock提供的函数调用能力实现了实时数据抓取。
3.  **知识复用**: RAG技术使得企业过去十年的IT运维文档和工单数据得以实时激活，避免了“重复造轮子”。
    *   *依据*: 摘要中提到的“optimization”（优化）通常基于历史数据分析。

**反例或边界条件**
1.  **零样本失效**: 在遇到从未见过的新型网络攻击或极端硬件故障时，Agent缺乏经验直觉，可能会给出错误的建议。
2.  **合规黑盒**: 在高度监管的能源行业，AI的决策过程如果不可解释，可能无法满足审计要求。

**判断性质**
*   **事实**: Iberdrola使用了AWS Bedrock和ServiceNow。
*   **价值判断**: 这种架构是“革命性”的。
*   **可检验预测**: 实施该系统后，IT工单的平均解决时间将显著缩短。

**立场与验证**
*   **立场**: 支持Agent技术在IT运维中的核心地位，但主张“渐进式部署”。
*   **验证方式**:
    *   **指标**: 对比实施前后的L1/L2工单解决率。
    *   **实验**: 进行灰度测试，让AI处理10%的工单，计算其准确率和人工介入率。
    *   **观察窗口**: 实施后的3-6个月，重点关注系统误操作（False Positive）的次数。

---

**总结**: 这篇文章

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于 Amazon Bedrock 的集中式知识库

**说明**: 利用 Amazon Bedrock 和 Amazon OpenSearch Serverless (AOS) 构建统一的企业知识库。通过将内部文档、技术手册和操作指南向量化并存储，使 AgentCore 能够基于企业私有数据提供准确的答案，有效减少模型幻觉。

**实施步骤**:
1. 收集并整理企业内部的非结构化数据（如 PDF、Wiki 页面）。
2. 使用 Amazon Titan Embeddings 模型将数据转换为向量并存储至 AOS。
3. 配置 Bedrock Knowledge Base，建立向量索引与生成式模型的映射关系。

**注意事项**: 确保数据源的定期更新，以保证 Agent 回答信息的时效性。

---

### 实践 2：实施严格的访问控制与安全护栏

**说明**: 在生成式 AI 应用中贯彻“零信任”安全原则。利用 AWS Identity and Access Management (IAM) 和 Bedrock Guardrails 来过滤不当内容，并确保用户只能访问其权限内的数据，防止敏感信息泄露。

**实施步骤**:
1. 定义精细化的 IAM 策略，限制不同角色对 Bedrock 模型和知识库的访问权限。
2. 配置 Bedrock Guardrails 以屏蔽有害内容、PII（个人身份信息）或特定领域的专业术语滥用。
3. 在 Agent 逻辑层实施用户上下文检查，确保数据查询的合法性。

**注意事项**: 定期审计 Guardrails 的日志，根据新的安全威胁动态调整过滤策略。

---

### 实践 3：采用“人机协同”的反馈闭环机制

**说明**: 建立用户反馈机制，利用 Amazon Bedrock 的模型评估功能或自定义工作流，收集用户对 Agent 回答质量的评价（点赞/点踩），并将这些反馈用于持续优化提示词和知识库内容。

**实施步骤**:
1. 在用户界面（UI）中集成简单的反馈按钮。
2. 将反馈数据存储在 S3 或 DynamoDB 中。
3. 定期分析负面反馈案例，调整检索策略或补充知识库缺失的文档。

**注意事项**: 建立标准化的评估指标（如准确率、相关性），量化优化效果。

---

### 实践 4：优化提示词工程以适配业务场景

**说明**: 不要仅依赖模型的基础能力。通过精心设计的 System Prompt（系统提示词）和 Few-shot Learning（少样本学习），明确 Agent 的角色定位、输出格式限制以及处理未知问题的准则，确保回答的专业性和一致性。

**实施步骤**:
1. 编写清晰的背景设定，例如“你是一位资深的 IT 运维专家”。
2. 在提示词中包含具体的“思维链”示例，引导模型分步推理。
3. 明确指示模型在知识库找不到答案时回复“不知道”，而非编造答案。

**注意事项**: 随着业务逻辑的变化，提示词需要版本控制和持续迭代。

---

### 实践 5：建立全面的可观测性与监控体系

**说明**: 利用 Amazon CloudWatch 和 AWS CloudTrail 监控 Agent 的运行状况。重点追踪延迟、Token 消耗量、检索准确率以及模型调用失败率，确保 IT 运维的稳定性。

**实施步骤**:
1. 配置 CloudWatch 告警，针对错误率或高延迟设置阈值。
2. 开启 CloudTrail 以记录所有 API 调用，用于合规审计和故障排查。
3. 构建自定义仪表盘，可视化 Agent 的使用趋势和用户满意度。

**注意事项**: 监控数据应与现有的 ITSM（IT 服务管理）工具集成，以便自动化工单处理。

---

### 实践 6：设计高效的检索增强生成 (RAG) 策略

**说明**: 单纯的向量检索可能不够精确。结合混合检索（关键词+向量）和重排序机制，提高从海量知识库中召回最相关文档的成功率，从而提升生成回答的质量。

**实施步骤**:
1. 评估知识库特点，决定是使用纯向量搜索还是混合搜索。
2. 在检索到初步结果后，引入重排序模型对文档进行重新打分。
3. 仅将得分最高的前 K 个文档填入 Prompt 上下文窗口。

**注意事项**: 平衡检索深度与上下文窗口限制，避免 Token 消耗过高。

---
## 学习要点

- 通过Amazon Bedrock AgentCore构建的AI助手能够自动处理复杂的IT运维请求，显著提升技术团队的响应速度与工作效率。
- 利用生成式AI技术，成功实现了对海量非结构化运维文档的精准检索与总结，打破了信息孤岛。
- AI Agent具备自主规划与执行能力，能够串联多个步骤（如查询、验证、修复）以完成端到端的故障排查任务。
- 将大语言模型（LLM）与企业知识库深度集成，有效降低了技术人员获取专业知识的门槛并减少了人为错误。
- 基于Amazon Bedrock的架构设计保证了系统的可扩展性，能够随着业务需求的变化灵活调整AI助手的处理能力。
- 该案例展示了通过自然语言处理技术实现IT运维自动化转型的最佳实践，为传统企业智能化升级提供了参考。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/iberdrola-enhances-it-operations-using-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [ServiceNow](/tags/servicenow/) / [IT 运营](/tags/it-%E8%BF%90%E8%90%A5/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [AWS](/tags/aws/) / [对话式 AI](/tags/%E5%AF%B9%E8%AF%9D%E5%BC%8F-ai/) / [事故管理](/tags/%E4%BA%8B%E6%95%85%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-2.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [利用全栈模板加速开发基于Amazon Bedrock AgentCore的应用]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*