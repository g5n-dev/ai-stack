---
title: 'Agent-to-agent collaboration: Using Amazon Nova 2 Lite and Amazon Nova Act
  for multi-agent systems'
date: 2026-02-11 01:40:26+08:00
draft: false
entry_kind: auto
tags:
- Multi-Agent
- Amazon Bedrock
- Agent 协作
- Amazon Nova
- 系统架构
- LLM
- 自动化
- 模型部署
categories:
- 大模型
- AI 工程
source: blogs_podcasts
description: 以下是对该内容的中文简洁总结： 本文主要介绍了如何利用 Amazon Bedrock 平台上的 Amazon Nova 2 Lite 和
  Amazon Nova Act 模型，构建稳健的多智能体协作系统，以解决单一智能体架构的脆弱性问题。 **核心内容要点：** 1. **架构转型（从单智能体到多智能体）：**
  文章指
external_url: https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems
scenarios:
- 大语言模型
- AI/ML项目
aliases:
- /posts/20260211-blogs_podcasts-agent-to-agent-collaboration-using-amazon-nova-2-l-13/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:00:28+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems](https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems)

---
## 摘要/简介

本文介绍了如何在实践中实现 Amazon Bedrock 上的代理间协作，利用 Amazon Nova 2 Lite 进行规划、利用 Amazon Nova Act 进行浏览器交互，将脆弱的单代理架构转变为可预测的多代理系统。

---
## 导语

构建稳健的多智能体系统往往面临单点脆弱性与任务复杂度的双重挑战。本文深入探讨了如何在 Amazon Bedrock 环境中实现智能体间的高效协作，通过利用 Amazon Nova 2 Lite 进行任务规划并调用 Amazon Nova Act 处理浏览器交互，从而将不稳定的单代理架构转变为可预测的多代理系统。阅读本文，您将掌握构建这种分层协作机制的具体实践方法，以提升自动化流程的可靠性。

---
## 摘要

以下是对该内容的中文简洁总结：

本文主要介绍了如何利用 Amazon Bedrock 平台上的 Amazon Nova 2 Lite 和 Amazon Nova Act 模型，构建稳健的多智能体协作系统，以解决单一智能体架构的脆弱性问题。

**核心内容要点：**

1.  **架构转型（从单智能体到多智能体）：**
    文章指出，仅依靠单一智能体处理复杂任务往往缺乏稳定性和可预测性。通过引入“智能体对智能体”的协作机制，可以将复杂的任务流程拆解，从而提高系统的整体可靠性。

2.  **角色分工与模型应用：**
    *   **Amazon Nova 2 Lite（规划者）：** 负责制定计划。该模型利用其强大的推理能力，对用户请求进行分析，并将任务拆解为可执行的步骤。
    *   **Amazon Nova Act（执行者）：** 负责浏览器交互。该模型专门用于执行具体的 Web 操作，能够接管浏览器环境，完成导航、点击和数据提取等任务。

3.  **实际工作流程：**
    文章演示了这两个模型如何协同工作。Nova 2 Lite 首先接收高层指令并生成具体的行动方案，随后指挥 Nova Act 执行浏览器层面的操作。这种“规划”与“行动”分离的模式，使得原本脆弱的单点系统转变为一个可预测、可回溯且高效的多智能体系统。

---

## 最佳实践指南

### 实践 1：基于能力差异的智能体角色分配

**说明**:
在多智能体系统中，应根据不同 Amazon 模型的特性进行角色分配。Amazon Nova 2 Lite 具备强大的多模态理解能力和极低的延迟，非常适合作为“规划者”或“协调者”，负责解析复杂指令、拆解任务以及分发工作流。而 Amazon Nova Act 专为行动设计，擅长模拟人类操作计算机（如点击、输入），应将其定位为“执行者”，负责完成具体的网页交互或系统操作。

**实施步骤**:
1.  构建一个主控 Agent（基于 Nova 2 Lite），负责接收用户 Prompt 并生成结构化的执行计划。
2.  定义子 Agent（基于 Nova Act）的角色，明确其仅负责接收原子化的操作指令（如“打开网站”、“点击按钮”）。
3.  设计中间件层，将主控 Agent 的意图转化为 Nova Act 可执行的计算机指令。

**注意事项**:
避免让 Nova Act 执行需要复杂逻辑推理的任务，这可能会导致操作成本增加或错误率上升。应保持逻辑层与执行层的解耦。

---

### 实践 2：建立标准化的通信协议

**说明**:
为了确保 Agent 之间的高效协作，必须定义严格的通信标准。由于 Nova 2 Lite 处理自然语言，而 Nova Act 处理计算机控制信号，两者之间需要一种标准化的消息格式（如 JSON）来传递上下文、指令和状态更新。这可以防止信息在传递过程中丢失或被误解。

**实施步骤**:
1.  定义包含 `task_id`（任务ID）、`action_type`（操作类型）、`parameters`（参数）和 `status`（状态）的 JSON Schema。
2.  在 Nova 2 Lite 的输出层强制要求其输出符合上述 Schema 的结构化数据。
3.  确保 Nova Act 能够解析该结构，并能返回包含执行结果（如截图文本、错误码）的标准反馈。

**注意事项**:
通信协议应包含错误处理机制。如果 Nova Act 返回执行失败，协议应支持重试或将控制权交还给 Nova 2 Lite 进行重新规划。

---

### 实践 3：实施基于上下文感知的动态反馈循环

**说明**:
多智能体系统不应是单向的线性流水线，而应具备动态调整能力。当 Nova Act 执行完操作后，系统应将结果（例如网页更新的内容或弹窗信息）实时反馈给 Nova 2 Lite。Nova 2 Lite 需要根据这些最新的视觉或文本信息，判断任务是否完成，或者是否需要调整下一步策略。

**实施步骤**:
1.  配置 Nova Act 在执行关键操作后自动截取界面快照或提取 DOM 文本。
2.  将这些反馈数据注入回 Nova 2 Lite 的上下文窗口中。
3.  设置 Nova 2 Lite 的推理循环，使其基于“观察-思考-行动”的模式不断修正指令，直到达成目标。

**注意事项**:
注意上下文窗口的 Token 限制。在反馈循环中，应对截图或冗长文本进行压缩或摘要处理，只保留关键状态信息，以避免超出模型限制。

---

### 实践 4：设计精细化的工具调用接口

**说明**:
虽然 Nova Act 具备操作计算机的能力，但在多智能体协作中，应通过 Function Calling（工具调用）机制来约束其行为。不要直接给予 Nova Act 无限制的系统访问权限，而是通过预定义的 API 接口（如 `search_web`、`fill_form`、`retrieve_data`）来规范其操作范围，提高安全性和可控性。

**实施步骤**:
1.  在 Nova 2 Lite 的系统提示词中注册一系列可用的工具函数。
2.  当 Nova 2 Lite 决定使用某个工具时，触发对应的 Nova Act 工作流。
3.  Nova Act 仅执行该特定工具对应的计算机操作序列，完成后返回结果。

**注意事项**:
工具定义必须清晰明确。模糊的工具描述会导致 Agent 选择错误的执行路径。定期审查工具调用的日志，优化工具的描述和参数设置。

---

### 实践 5：强化执行过程的可观测性与日志记录

**说明**:
在 Agent 协作过程中，尤其是涉及自动化操作时，必须具备完整的可观测性。你需要追踪 Nova 2 Lite 的决策过程以及 Nova Act 的每一步操作。这对于调试协作逻辑错误、回溯失败原因以及优化系统性能至关重要。

**实施步骤**:
1.  实现全链路日志系统，记录从用户输入、Lite 规划、Act 执行到最终输出的所有数据。
2.  为每个 Agent 的思维链（Chain of Thought）和操作步骤打上时间戳。
3.  构建可视化仪表盘，实时展示 Agent 的工作流状态和中间结果。

**注意事项**:
在记录日志时，注意过滤敏感信息（如 PII 数据、密码、API Key），确保符合数据安全和隐私保护规范。

---

### 实践 6：设定明确的边界条件与异常处理策略

**说明**:
Agent 协作可能会遇到不可预见的情况

---
## 学习要点

- Amazon Nova Act 具备自主操作浏览器的能力，能够直接执行复杂的工作流程而无需人工干预。
- 多智能体系统通过将推理任务与执行任务分离，利用 Nova 2 Lite 负责逻辑规划、Nova Act 负责具体操作，从而实现高效的智能体间协作。
- Nova Act 能够像人类一样与网页界面进行交互，不仅能点击和输入，还能根据视觉反馈自我纠正错误。
- 该架构显著降低了构建自动化应用的门槛，开发者无需编写底层的集成代码即可实现端到端的业务流程自动化。
- Nova 2 Lite 模型在处理复杂逻辑推理任务时表现出色，能够为执行类智能体提供精确、可执行的分步指令。
- 这种协作模式展示了将“思考”与“行动”解耦的设计优势，使多智能体系统在处理现实世界任务时更加灵活且具备容错性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems](https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Multi-Agent](/tags/multi-agent/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [Agent 协作](/tags/agent-%E5%8D%8F%E4%BD%9C/) / [Amazon Nova](/tags/amazon-nova/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/) / [LLM](/tags/llm/) / [自动化](/tags/%E8%87%AA%E5%8A%A8%E5%8C%96/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [编码代理的成功对通用AI系统的启示]({{< relref "posts/20260130-hacker_news-what-the-success-of-coding-agents-teaches-us-about-11.md" >}})
- [迈向智能体系统规模化科学：工作原理与适用条件]({{< relref "posts/20260201-hacker_news-towards-a-science-of-scaling-agent-systems-when-an-11.md" >}})
- [构建极简且具倾向性的编程代理的经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-1.md" >}})
- [构建极简且具倾向性的编程代理的经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-1.md" >}})
- [构建极简编程代理的技术实践与经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
