---
title: 后端面试高频考点：MCP、Skill 与 Function Call 的区别
date: 2026-02-27 08:07:36+08:00
draft: false
entry_kind: auto
tags:
- MCP
- Function Call
- Skill
- LLM
- AI面试
- 后端开发
- 模型协议
- 技术解析
categories:
- 后端
- 大模型
source: juejin
description: '**面试热点解析：MCP、Skill 与 Function Call 的区别** 随着 AI 大模型技术在各领域的深入应用，后端面试中
  AI 相关题目的重要性日益凸显。为帮助开发者应对高频考点，本文将对 **MCP、Skill、Function Call** 这三个核心概念及其区别进行总结。 **1.
  概念定义** *'
external_url: https://juejin.cn/post/7611084174967210019
scenarios:
- 大语言模型
- AI/ML项目
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **作者**: Java编程爱好者
- **链接**: [https://juejin.cn/post/7611084174967210019](https://juejin.cn/post/7611084174967210019)

---

## 导语

随着 AI 技术在后端开发中的渗透，MCP、Skill 和 Function Call 已成为高频面试考点，但许多开发者对其概念边界与应用场景仍缺乏清晰认知。厘清这三者的技术差异与适用逻辑，不仅有助于应对面试提问，更能指导我们在实际业务中做出更合理的架构设计。本文将深入剖析它们的核心区别，助你建立系统化的认知框架。

---

## 描述

最近翻后台留言，发现好多朋友都在吐槽：现在后端面试，AI 相关的题目已经成了高频必考点，没提前准备很容易被问懵。 所以我后面计划陆续更新 AI 大模型开发相关的面试题系列，帮大家提前攒好干货、做好储备

---

## 摘要

**面试热点解析：MCP、Skill 与 Function Call 的区别**

随着 AI 大模型技术在各领域的深入应用，后端面试中 AI 相关题目的重要性日益凸显。为帮助开发者应对高频考点，本文将对 **MCP、Skill、Function Call** 这三个核心概念及其区别进行总结。

**1. 概念定义**

*   **Function Calling (函数调用)**
    这是一种技术机制，允许大模型（LLM）在生成文本的同时，输出结构化的 JSON 数据。这使得模型能够“指示”外部系统执行特定的操作（如查询数据库、调用 API），从而将生成式 AI 与实际业务逻辑相结合。

*   **Skill (技能)**
    Skill 通常指封装好的、特定领域的**能力或应用**。它将一个或多个 Function Call 及其配套的提示词、逻辑打包，形成一个独立的功能单元。用户可以直接调用该技能来完成特定任务，而不需要关心底层的具体实现细节。

*   **MCP (Model Context Protocol)**
    MCP 是一种**开放标准协议**（类似 AI 界的“USB”）。它定义了 AI 应用（如客户端）与数据源（如服务器）之间连接和通信的统一规范。MCP 旨在解决不同 AI 工具与各类数据服务之间连接碎片化的问题，实现“一次连接，到处通用”。

**2. 核心区别总结**

*   **层级与维度不同：**
    *   **Function Call** 是底层的**技术交互手段**，解决的是模型“怎么发指令”的问题。
    *   **Skill** 是应用层的**能力封装**，解决的是模型“能做什么”的问题。
    *   **MCP** 是基础设施层的**连接标准**，解决的是系统间“怎么互联互通”的问题。

*   **灵活性与通用性：**
    *   Function Call 最灵活，但需要针对每个接口单独开发。
    *   Skill 复用性强，便于共享和分发。
    *   MCP 通用性最强，打破了不同应用和服务器之间的壁垒，便于生态互通。

**总结：**
这三者共同构成了 AI 应用开发的关键拼图：**Function Call** 负责打通模型与代码的执行，**Skill** 负责将能力产品化，而 **MCP** 则致力于构建统一的连接生态。

---

## 评论

**中心观点**
该文章试图在 AI 应用开发的面试语境下，通过厘清 MCP（模型上下文协议）、Skill（技能/插件化封装）与 Function Call（函数调用/工具使用）这三个核心概念的技术边界，来构建一套关于大模型“工具使用”与“系统扩展性”的知识评估框架。

**支撑理由与深度评价**

1.  **概念层级与架构视角的区分（事实陈述 / 作者观点）**
    *   **分析**：文章的核心价值在于将这三个容易混淆的术语进行了分层。
        *   **Function Call** 是**机制层**。它解决的是“如何让 LLM 输出结构化数据（如 JSON）”以便机器解析的问题。这是大模型与外部世界交互的“握手协议”。
        *   **Skill** 是**能力层**。它通常是对 Function Call 的业务封装。一个 Skill 可能由多个 Function 组成，或者是一个经过 Prompt Engineering 优化的“人设”。它解决的是“模型能做什么具体任务”的问题。
        *   **MCP (Model Context Protocol)** 是**基础设施/协议层**。它试图解决的是“异构系统如何统一连接”的问题。类比于 HTTP 协议之于互联网，MCP 旨在统一 AI 应用与数据源（如 GitHub、Slack、本地文件）之间的连接标准，避免为每个应用重复开发 Adapter。
    *   **评价**：这种区分方式非常符合现代 AI 工程架构的演进逻辑。从底层的 JSON Schema 定义，到中层的业务逻辑封装，再到顶层的互操作性协议，体现了从“点”到“面”的技术视野。

2.  **面试场景下的“造词”与“标准化”之争（事实陈述 / 你的推断）**
    *   **分析**：文章提到“后端面试 AI 题成高频必考”，这反映了行业现状：企业迫切需要能将大模型能力落地的工程人才。
    *   **评价**：然而，这里存在一个**边界条件**：**MCP 是 Anthropic 提出的协议，并非行业标准（如 OpenAI 的 Function Calling 格式已成事实标准）。** 如果面试官过度纠结 MCP 的实现细节，可能存在特定技术栈的偏见。
    *   **反例**：在许多非 Anthropic 技术栈的企业中，所谓的“Skill”可能直接对应 LangChain 中的 `Tool` 或 OpenAI 的 `GPTs`，而“MCP”的概念可能完全不存在。如果面试者死记硬背 MCP 而不理解其背后的“互操作性”设计思想，在实际工作中可能无法迁移到基于 Dify 或 OpenAI 的平台上。

3.  **技术实现的混淆风险与实际落地难点（作者观点 / 你的推断）**
    *   **分析**：文章可能倾向于将这三者作为并列概念讲解，但在实际工程中，它们往往是**嵌套关系**。
    *   **边界条件**：MCP Server 的实现，本质上往往就是定义了一组 Resources（读取数据）和 Prompts（模板），而在底层通信时，依然依赖 Function Calling 的机制来传递参数。
    *   **批判性思考**：单纯区分概念是不够的。真正的技术难点在于：**当 Function Call 变得极其复杂时（如数百个函数），如何通过 Skill 进行分组管理，以及如何利用 MCP 协议来解决客户端与 Host 之间的数据同步问题。** 如果文章仅停留在名词解释，而未触及“上下文窗口限制”或“函数路由延迟”等性能问题，其实用价值会打折扣。

**行业影响与争议点**

1.  **协议碎片化与统一**
    *   **争议点**：MCP 的出现是为了解决“每个 AI 应用都要写一遍连接器”的痛点。但行业是否会接受 Anthropic 的标准？OpenAI 和 Google 也有类似的连接方案。文章若未提及 MCP 的竞争格局（如 OpenAI 的 GPTs Actions），可能会给读者造成“MCP 是唯一解”的错觉。
2.  **Agent 与 Tool 的界限模糊**
    *   **不同观点**：在某些高级 Agent 框架（如 AutoGen 或 CrewAI）中，Skill 可能指代一个具有自主规划能力的子 Agent，而不仅仅是被动调用的函数。如果文章将 Skill 仅仅定义为“函数的集合”，可能忽略了 AI Agent 自主性的发展趋势。

**实际应用建议**

1.  **不要为了面试而面试**：理解 **Function Call** 是基石，无论面试哪家公司，这是大模型开发者的必修课。理解 JSON Schema、参数校验和错误重试机制比背诵 MCP 协议字段更重要。
2.  **关注“连接”而非“名词”**：MCP 的核心思想是“数据即服务”。在构建企业级 AI 应用时，应优先考虑如何将现有 API 转化为 LLM 可调用的工具，而不是纠结于使用哪种协议。如果 MCP 能降低开发成本，则采用；否则，直接调用 SDK 更高效。
3.  **Skill 设计的原子性原则**：在设计 Skill 时，应遵循单一职责原则。一个 Skill 不应包含过于复杂的逻辑，否则会导致 LLM 的参数解析出错。

**可验证的检查方式**

1.  **技术验证（指标）**：
    *   **Function Call 准确率**：在复杂参数场景下，LLM 生成 JSON 的成功率是多少？（可通过沙箱测试验证）
    *   **MCP 连接延迟**：使用 MCP 协议读取本地文件或调用远程 API 相比于原生 HTTP 调用，增加了多少毫秒的延迟？

2.  **行业观察（观察窗口

---

## 学习要点

- 根据您提供的内容，以下是关于 MCP、Skill 和 Function Call 区别的关键要点总结：
- Function Call 是基础能力，指大模型根据上下文自主判断并调用外部工具函数的单次执行机制。**
- Skill 是对 Function Call 的封装与组合，通过将多个函数串联形成标准化的工作流，以解决特定的复杂任务。**
- MCP (Model Context Protocol) 是统一的连接标准，旨在打破不同 AI 应用与数据源之间的壁垒，实现即插即用的系统级互操作性。**
- 三者呈现层级递进关系：MCP 是连接标准，Skill 是业务逻辑封装，而 Function Call 是底层的原子执行动作。**
- 从生态角度看，MCP 解决的是“通用连接”问题，而 Skill 和 Function Call 更多是解决“具体任务执行”问题。**

---

## 常见问题

### 什么是 Function Call (函数调用)？它的核心作用是什么？

Function Call 是大语言模型（LLM）的一种基础能力，指模型可以根据用户的语义，自主判断并生成调用外部工具或 API 的指令（通常为 JSON 格式），而不是直接生成文本回复。

其核心作用是打破 LLM 只能基于训练数据进行对话的局限，赋予模型“联网”和“执行操作”的能力。通过 Function Call，LLM 可以查询实时信息（如天气、股票）、操作私有数据库（如查询企业知识库）或执行具体任务（如发送邮件、预订会议室）。它是实现 AI Agent（智能体）从“对话者”转变为“执行者”的第一步。

### 什么是 Skill (技能)？它与 Function Call 有何不同？

Skill 通常指 AI 系统中封装好的、具有特定业务逻辑的“技能包”或“服务”。

两者的区别主要在于层级和封装度：
1.  **粒度**：Function Call 往往对应底层的、原子级的 API 接口（例如 `get_user_info(user_id)`）；而 Skill 是更高层的概念，可能由多个 Function Call 组合而成，完成一个复杂的任务（例如“预订机票”这个 Skill，可能包含查询航班、锁定座位、支付等多个 Function Call）。
2.  **标准化**：Function Call 是一种通用的技术标准（如 OpenAI 的 function calling 格式）；而 Skill 更多是应用层或平台层（如 Dify、Coze 等平台）的概念，用于方便开发者复用和编排业务逻辑。
3.  **关系**：Skill 的底层实现通常依赖 Function Call，但 Skill 提供了更友好的配置界面和更复杂的上下文管理能力。

### 什么是 MCP (Model Context Protocol)？它解决了什么问题？

MCP (Model Context Protocol) 是一个开放的标准协议，旨在解决 AI 应用与数据源/工具之间的连接问题。

它主要解决了以下痛点：
1.  **连接碎片化**：在 MCP 出现之前，每个 AI 应用（如 ChatGPT、Claude Desktop 或各类 IDE 插件）连接数据源（如 Google Drive、Slack、本地文件）都需要开发专门的插件。MCP 定义了一套统一的连接标准，使得“一次开发，处处运行”成为可能。
2.  **上下文获取的标准化**：它规范了 AI 如何向服务器请求内容、服务器如何返回内容。简单来说，MCP 让 LLM 能够通过标准化的方式“读取”和“写入”各种系统的数据，而无需为每个系统重复开发适配器。

### MCP、Skill 和 Function Call 三者在技术架构上是什么关系？

这三者通常处于 AI 交互栈的不同层级，可以理解为从底层到上层的递进关系：

1.  **Function Call (机制层)**：这是最底层的“握手协议”。它定义了 LLM 如何向外部系统发送指令（JSON），以及外部系统如何返回结果。它是实现工具调用的基础技术手段。
2.  **MCP (传输/协议层)**：这是中间层的“连接管道”。它定义了 AI 客户端如何与远端服务（提供数据或工具的服务）建立连接、传输数据。MCP 的传输内容往往就包含了 Function Call 的定义或执行结果。
3.  **Skill (应用/业务层)**：这是最上层的“功能封装”。对于最终用户或开发者而言，他们配置的是一个“Skill”（如“帮我分析 GitHub 代码”）。这个 Skill 内部可能通过 MCP 协议连接到 GitHub 数据，然后通过 Function Call 机制触发具体的查询操作。

**总结**：Function Call 是“怎么做”，MCP 是“怎么连”，Skill 是“做什么”。

### 在实际开发中，我应该优先选择哪种技术？

这取决于你的开发场景和目标：

*   **如果你是底层模型开发者或直接调用 OpenAI/Claude API**：你主要打交道的是 **Function Call**。你需要定义函数的 JSON Schema，并处理模型返回的参数。
*   **如果你在构建 AI 应用或 Agent 平台**：你会大量使用 **Skill** 的概念。你需要将业务逻辑封装成可复用的技能，并处理技能之间的编排。
*   **如果你需要让 AI 客户端连接到企业内部数据或 SaaS 软件**：**MCP** 是未来的首选。如果你的客户端支持 MCP，实现 MCP 服务端将比开发各种私有插件更高效、更具通用性。

### 为什么说 MCP 是连接 AI 与数据源的“USB 接口”？

这是一个形象的比喻。在计算机硬件中，USB 协议允许各种不同的设备（鼠标、键盘、硬盘）通过标准接口插入电脑，无需为每个设备定制主板的物理接口。

MCP 在 AI 领域扮演了同样的角色：
*   **AI 客户端**（如 Claude、IDE）相当于“电脑”。
*   **数据源/工具**（如 Jira、Git、本地文件系统）相当于“外设”。
*   **MCP

---

## 引用

- **掘金原文**: [https://juejin.cn/post/7611084174967210019](https://juejin.cn/post/7611084174967210019)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [MCP](/tags/mcp/) / [Function Call](/tags/function-call/) / [Skill](/tags/skill/) / [LLM](/tags/llm/) / [AI面试](/tags/ai%E9%9D%A2%E8%AF%95/) / [后端开发](/tags/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [模型协议](/tags/%E6%A8%A1%E5%9E%8B%E5%8D%8F%E8%AE%AE/) / [技术解析](/tags/%E6%8A%80%E6%9C%AF%E8%A7%A3%E6%9E%90/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
- [大模型API本质解析：Tools、MCP与Skills的区别]({{< relref "posts/20260215-juejin-从-0-诠释大模型-api-的本质-tools-mcp-skills-0.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [Context Graphs与Agent Traces技术解析]({{< relref "posts/20260204-blogs_podcasts-ainews-context-graphs-and-agent-traces-0.md" >}})
