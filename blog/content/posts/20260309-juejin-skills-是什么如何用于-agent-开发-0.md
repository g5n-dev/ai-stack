---
title: Agent Skills 概念解析及其在 Agent 开发中的应用
date: 2026-03-09 01:01:37+08:00
draft: false
entry_kind: auto
tags:
- Agent
- LLM
- AI Agent
- Agent Skills
- 智能体开发
- Prompt Engineering
- AI 应用架构
- 技术解析
categories:
- 大模型
- AI 工程
source: juejin
description: 随着 AI Agent 技术的演进，如何让模型更精准地调用外部工具已成为开发的关键。本文由资深工程师双越撰写，将深入解析 Agent Skills
  的技术概念，并探讨其与其他 AI 技术的关联。通过阅读本文，读者不仅能厘清 Skills 的核心逻辑，还能掌握将其应用于实际 Agent 开发的具体方法，从而提升系统的可控
external_url: https://juejin.cn/post/7614331029458026531
scenarios:
- 大语言模型
- AI/ML项目
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# Agent Skills 概念解析及其在 Agent 开发中的应用

---

## 基本信息

- **作者**: 前端双越老师
- **链接**: [https://juejin.cn/post/7614331029458026531](https://juejin.cn/post/7614331029458026531)

---

## 导语

随着 AI Agent 技术的演进，如何让模型更精准地调用外部工具已成为开发的关键。本文由资深工程师双越撰写，将深入解析 Agent Skills 的技术概念，并探讨其与其他 AI 技术的关联。通过阅读本文，读者不仅能厘清 Skills 的核心逻辑，还能掌握将其应用于实际 Agent 开发的具体方法，从而提升系统的可控性与执行效率。

---

## 描述

大家好，我是双越，wangEditor 作者，前百度、滴滴资深软件工程师。本文将讲解 Agent SKILLS 技术的概念与应用，以及它与其他 AI Agent 技术之间的关联。欢迎点赞收藏～

---

## 评论

**文章中心观点**
文章主张将“Skills（技能）”作为 AI Agent 开发的核心抽象单元，通过封装 Prompt、工程逻辑和工具调用，实现 Agent 能力的模块化、标准化和可复用性，以解决当前大模型应用开发中代码耦合度高、难以维护的痛点。

**深入评价与分析**

**1. 内容深度：工程化视角的降维打击**
*   **支撑理由（事实陈述/作者观点）：** 文章并未停留在理论层面的 Agent 架构探讨（如仅讨论反思或规划模式），而是直接切入“工程落地”的痛点。作者作为 wangEditor 的创造者，具备丰富的前端和工程化经验，因此文章敏锐地指出了当前 Agent 开发中的“泥球代码”问题。将“Skill”定义为“Prompt + Function Calling + 业务逻辑”的集合，这是一个非常务实的深度观点，它揭示了 Agent 开发本质上是软件工程的延续，而非纯粹的 Prompt Engineering。
*   **反例/边界条件（你的推断）：** 这种定义存在边界模糊的问题。当“Skill”变得过于复杂（例如包含了一个完整的 RAG 流程或多步推理链），它就不再是一个“技能”，而是一个“子 Agent”或“微服务”。如果强行将复杂逻辑封装为 Skill，可能会导致内部参数（如 Temperature、Top-P）的调优变得极其困难，因为上下文被封装壳隔离了。

**2. 实用价值：中台化思维的体现**
*   **支撑理由（事实陈述）：** 对于企业级应用开发，文章提出的思路具有极高的参考价值。它实际上是在提倡建立 AI 能力的“中台”。通过标准化 Skill 的输入输出，团队可以实现能力的复用，避免重复造轮子。例如，一个“查天气”的 Skill 可以被客服 Agent 和导购 Agent 同时调用。
*   **反例/边界条件（你的推断）：** 对于初创公司或 MVP（最小可行性产品）阶段，强行抽象 Skill 层属于“过度设计”。在需求尚未明确时，构建复杂的 Skill 管理系统会拖慢迭代速度。此外，目前的 Skill 标准尚未统一（如 LangChain 的 Tool 与 Semantic Kernel 的 Skill 互不兼容），采纳该方案可能面临未来的迁移成本。

**3. 创新性：旧瓶装新酒的必要性**
*   **支撑理由（作者观点）：** 文章的创新点不在于发明了新概念，而在于**重新定义了开发者的心智模型**。它将开发者从“写 Prompt 的人”转变为“编排能力的工程师”。它强调了 Skill 的“可组合性”，这与前端组件化思想（如 React/Vue）一脉相承，将 UI 组件化的经验迁移到了 AI 逻辑层。
*   **反例/边界条件（你的推断）：** 这种观点并非没有先例，微软的 Semantic Kernel 和 LangChain 的 Chain 早已涉及类似概念。文章的创新性更多体现在对中文开发者社区的普及和具体落地节奏的把握上，而非理论突破。

**4. 行业影响与争议点**
*   **争议点（你的推断）：** **Agent 的“原子性”之争。** 行业内目前存在争议：Agent 的最小颗粒度应该是“Skill”还是“Action”？如果 Skill 内部包含了自主决策逻辑，那么多个 Skill 组合时可能会出现意图冲突。例如，一个“闲聊 Skill”和一个“销售 Skill”同时被激活，Agent 该听谁的？文章未深入探讨 Skill 之间的冲突解决机制（如路由层或仲裁器的设计）。
*   **行业影响（你的推断）：** 这类文章的普及有助于推动 AI 开发从“手工作坊”向“工业化”迈进。如果“Skill”成为一种行业标准协议，未来可能会出现类似 npm 或 Docker Hub 的“Skill 市场”，彻底改变软件的分发模式。

**实际应用建议**
1.  **不要过早抽象：** 在只有 3-5 个 Prompt 时，直接写在代码里。当发现重复代码出现时，再抽取为 Skill。
2.  **定义严格契约：** Skill 的输入输出必须是强类型（如 TypeScript Interface），避免 LLM 生成非结构化数据导致解析失败。
3.  **监控与隔离：** 每个 Skill 应该有独立的调用日志和成功率监控，以便排查是 Skill 本身的问题，还是 Agent 规划层的问题。

**可验证的检查方式**

1.  **复用率指标（可观测性）：**
    *   *检查方式：* 在引入 Skill 架构后，统计代码库中 Prompt 逻辑的复用率。如果一个新的 Agent 开发，80% 的能力是通过调用现有 Skill 完成的，而非重写 Prompt，则证明该架构有效。
2.  **上下文窗口压缩测试（实验）：**
    *   *检查方式：* 对比“将所有逻辑写在一个超长 Prompt 中”与“拆分为多个 Skill 调用”的 Token 消耗。如果 Skill 化后的总 Token 消耗反而大幅增加（因为重复传输 System Context），则说明封装粒度有问题。
3.  **并行调用能力（观察窗口）：**
    *   *检查方式：* 观察在一个复杂的 Agent 任务中，互不依赖的 Skill（如“查天气”和“计算汇率”）是否能够真正并行执行。如果架构导致必须串行调用，则未发挥出 Skill 独立性的优势。

---

## 学习要点

- Skills 是将大模型能力具象化为可执行、可验证、可组合的标准化功能单元，是 Agent 实现复杂任务拆解与专业处理的核心机制。
- 开发 Skills 应遵循单一职责原则，通过精心设计的 Prompt 模板和上下文注入来约束模型行为，确保输出格式的稳定性。
- 通过定义清晰的输入输出 Schema（如 JSON 或 Pydantic 模型），实现 Skills 与 Agent 主控程序及工具链之间的可靠数据交互。
- Skills 的编排模式决定了 Agent 的能力上限，包括串行调用、并行分支以及基于结果反馈的动态路由策略。
- 高质量 Skills 的构建依赖于结构化数据的注入（如知识库 RAG）而非仅依赖模型本身的通用知识，以解决幻觉问题。
- 对 Skills 进行独立的单元测试与性能评估是保障 Agent 整体鲁棒性的必要手段，需关注其成功率与延迟。
- 将通用能力（如搜索、计算）封装为标准化 Skills 并沉淀为资产，能大幅提升后续 Agent 开发的效率与复用性。

---

## 常见问题

### Skills 在 Agent 开发中具体指什么？

在 Agent 开发（特别是基于 Dify、AutoGPT 或 LangChain 等框架）的语境下，Skills（技能）是指封装了特定功能或逻辑的代码模块。它们是 Agent 实现特定任务的最小可执行单元。可以将 Skills 理解为 Agent 的“工具箱”中的具体工具，例如“搜索网页”、“解析 PDF 文件”、“查询天气”或“调用 API”。通过组合不同的 Skills，Agent 才能具备解决复杂问题的能力。

### 如何将一个外部 API 封装为 Agent 的 Skill？

将外部 API 封装为 Skill 通常需要以下步骤：
1.  **定义接口**：明确 API 的输入参数（如查询关键词、时间范围）和输出结构（如 JSON 格式）。
2.  **编写处理逻辑**：在开发平台（如 Dify）中创建新的 Skill，编写代码调用该外部 API。这通常涉及使用 Python 的 `requests` 库发送 HTTP 请求。
3.  **处理认证**：如果 API 需要 API Key 或 OAuth，需要在 Skill 代码中安全地处理这些密钥。
4.  **数据清洗与映射**：将 API 返回的原始数据转换为 Agent 容易理解的文本或结构化数据，以便大模型（LLM）进行后续处理。

### Agent 是如何知道何时调用哪个 Skill 的？

这依赖于大模型（LLM）的推理能力和框架的编排机制。开发者需要为每个 Skill 配置清晰的**描述**和**参数说明**。当用户向 Agent 发送指令时，系统会将用户的意图、可用的 Skills 列表及其描述一起发送给 LLM。LLM 会根据上下文分析，判断需要调用哪个工具来完成任务，并生成相应的参数。这个过程被称为“函数调用”或“工具使用”。

### 在开发 Skills 时，如何处理复杂的业务逻辑？

对于复杂的业务逻辑，不应将所有代码堆砌在一个 Skill 中。建议采用**模块化**的设计思路：
1.  **拆分任务**：将复杂流程拆解为多个独立的子任务，例如“数据获取”、“数据清洗”、“格式化输出”。
2.  **多 Skill 协作**：为每个子任务创建独立的 Skill。
3.  **工作流编排**：利用 Agent 平台的工作流功能，将多个 Skill 串联起来。前一个 Skill 的输出作为后一个 Skill 的输入，从而实现复杂的业务流自动化。

### 开发 Skills 时有哪些常见的错误需要避免？

常见的错误包括：
1.  **描述模糊**：Skill 的描述写得不清楚，导致 LLM 无法准确理解何时调用该 Skill，或者调用时参数填错。
2.  **缺少错误处理**：没有处理 API 调用失败、超时或返回错误码的情况，导致 Agent 直接崩溃或向用户输出报错信息。
3.  **输出格式不统一**：Skill 返回的数据格式不规范（例如有时返回 JSON，有时返回纯文本），这会增加 LLM 解析信息的难度。
4.  **过度依赖 LLM 进行计算**：将本应由代码精确完成的数学计算或逻辑判断交给 LLM 处理，导致结果不准确。

### Skills 与 Agent 的“记忆”有什么区别？

Skills 和记忆是 Agent 架构中两个不同的组件：
*   **Skills（行动力）**：代表 Agent **能做什么**。它是动态的代码逻辑，用于与外部环境交互（读取文件、联网、操作数据库）。
*   **记忆（存储力）**：代表 Agent **记得什么**。它用于存储对话历史、用户偏好或长期知识库。
简单来说，Skills 是“手和脚”，负责执行任务；记忆是“大脑皮层”，负责存储信息。在开发中，Skills 可以读取记忆中的内容来辅助决策。

### 如何调试一个运行不正常的 Skill？

调试 Skills 通常建议按以下顺序进行：
1.  **日志检查**：在代码关键节点（如 API 请求前、接收后）添加打印日志，确认输入参数是否正确传递。
2.  **独立测试**：将 Skill 代码剥离出来，使用模拟参数进行单独运行，排除逻辑错误。
3.  **检查 LLM 输入**：观察发送给 LLM 的 System Prompt 和 Tool Schema，确认描述是否具有误导性。
4.  **查看执行轨迹**：在 Agent 平台的运行日志中，查看 LLM 生成的具体调用参数，确认是否因为参数格式不匹配（例如传了字符串给数字型参数）导致调用失败。

---

## 引用

- **掘金原文**: [https://juejin.cn/post/7614331029458026531](https://juejin.cn/post/7614331029458026531)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [LLM](/tags/llm/) / [AI Agent](/tags/ai-agent/) / [Agent Skills](/tags/agent-skills/) / [智能体开发](/tags/%E6%99%BA%E8%83%BD%E4%BD%93%E5%BC%80%E5%8F%91/) / [Prompt Engineering](/tags/prompt-engineering/) / [AI 应用架构](/tags/ai-%E5%BA%94%E7%94%A8%E6%9E%B6%E6%9E%84/) / [技术解析](/tags/%E6%8A%80%E6%9C%AF%E8%A7%A3%E6%9E%90/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [Agent Skills：智能体技能框架与能力评估]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [Agent Skills：智能体技能评估与开源框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
