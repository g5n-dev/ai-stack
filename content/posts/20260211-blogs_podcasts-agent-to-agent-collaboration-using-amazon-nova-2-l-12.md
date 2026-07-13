---
title: "基于Amazon Bedrock实现多智能体协作：Nova 2 Lite规划与Nova Act交互"
date: 2026-02-11T01:40:26+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "这篇文章介绍了如何利用 **Amazon Bedrock** 上的 **Amazon Nova 2 Lite** 和 **Amazon Nova Act** 模型，构建一个**多智能体协作系统**，旨在解决单一智能体架构在处理复杂任务时的脆弱性。 **核心内容总结：** 1. **架构演进：从单智能体到多智能体** 文"
external_url: https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems
scenarios: ["AI/ML项目"]
---

# 基于Amazon Bedrock实现多智能体协作：Nova 2 Lite规划与Nova Act交互

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:00:28+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems](https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems)

---
## 摘要/简介

本文介绍如何在实践中实现 Amazon Bedrock 上的智能体与智能体协作：使用 Amazon Nova 2 Lite 进行规划，并使用 Amazon Nova Act 进行浏览器交互，从而将脆弱的单智能体设置转变为可预测的多智能体系统。

---
## 导语

在构建复杂应用时，单一智能体往往难以兼顾高层规划与底层执行的稳定性。本文深入探讨了如何在 Amazon Bedrock 上实现智能体间的协作，具体展示了利用 Amazon Nova 2 Lite 负责逻辑规划，并指挥 Amazon Nova Act 处理浏览器交互的实践方法。通过阅读此文，您将掌握如何将脆弱的单智能体架构重构为可预测的多智能体系统，从而显著提升自动化任务的可靠性。

---
## 摘要

这篇文章介绍了如何利用 **Amazon Bedrock** 上的 **Amazon Nova 2 Lite** 和 **Amazon Nova Act** 模型，构建一个**多智能体协作系统**，旨在解决单一智能体架构在处理复杂任务时的脆弱性。

**核心内容总结：**

1.  **架构演进：从单智能体到多智能体**
    文章首先指出了传统单一智能体系统的局限性。在单智能体模式下，一个模型需要同时负责推理、规划和执行具体操作（如网页浏览）。这种“全能”模式往往导致系统不稳定，容易在复杂步骤中出错。为了解决这个问题，文章提出了基于**角色分离**的多智能体架构。

2.  **模型分工与角色定义**
    该多智能体系统通过明确的分工实现高效协作，具体使用了两个 Amazon Nova 模型：
    *   **Amazon Nova 2 Lite（规划者）：** 利用其强大的推理和文本生成能力，充当“大脑”。它的主要职责是**理解用户意图**、**拆解复杂任务**，并制定详细的**行动计划**。它不直接执行操作，而是发出指令。
    *   **Amazon Nova Act（执行者）：** 专为浏览器交互设计。它的主要职责是**接收 Nova 2 Lite 的指令**，并将其转化为具体的**浏览器动作**（如点击、输入、滚动等），直接与互联网环境互动以获取信息或完成任务。

3.  **工作流程与协作机制**
    文章详细描述了两个智能体之间的协作闭环：
    *   用户提出请求。
    *   **Nova 2 Lite** 分析请求，生成一系列具体的子任务指令。
    *   **Nova Act** 接管浏览器，执行这些指令，并将执行结果（如截图、读取的网页内容）反馈给 Lite。
    *   **Nova 2 Lite** 根据反馈评估进度，判断任务是否完成。如果未完成，它会生成下一步指令，再次发送给 Nova Act 执行。
    *   这个循环持续进行，直到任务最终完成。

4.  **优势与结论**
    通过将“规划”与“执行”分离，该架构将原本脆弱的单体系统转化为一个**可预测、更可靠**的工作流。Lite 负责逻辑闭环，Act 负责精准操作，两者配合显著提升了自动化任务的成功率和稳定性。

**一句话总结：**
利用 Amazon Nova

---
## 评论

**文章中心观点**
该文章主张通过将“规划者”与“执行者”解耦，利用 Amazon Nova 2 Lite 负责逻辑编排、Amazon Nova Act 负责浏览器操作，构建多智能体协作系统，从而解决单体智能体在处理复杂工作流时稳定性不足和可观测性差的问题。

**深入评价**

**1. 内容深度：从“提示词工程”向“系统架构”的跨越**
*   **支撑理由（事实陈述）：** 文章触及了当前 AI 应用的核心痛点——长上下文任务中的“注意力分散”与“错误级联”。单体 Agent 在处理长链路任务时，往往因为一步操作失败导致整体崩溃。文章提出的 Lite（轻量级模型）+ Act（专用工具模型）的组合，实际上是一种**算法层面的职责分离（Separation of Concerns）**。Lite 专注于 Token 消耗较低的推理与规划，Act 专注于高延迟的浏览器环境交互。这种架构设计比单纯优化 Prompt 更具鲁棒性。
*   **支撑理由（作者观点）：** 文章强调了“可预测性”。在商业落地中，概率性的生成式输出往往难以通过测试。通过将规划固化在 Lite 模型中，将执行约束在 Act 模型的浏览器环境内，实际上是将不可控的黑盒变成了两个相对可控的白盒/灰盒，增加了系统的确定性边界。
*   **反例/边界条件（你的推断）：** 这种深度依赖于特定的模型分工。如果 Nova 2 Lite 的推理能力不足以生成完美的 JSON 格式指令，或者 Nova Act 对网页结构的理解出现幻觉（例如找不到 DOM 元素），整个系统会陷入“死循环”或“静默失败”，且这种多 Agent 调试比单体 Agent 更为复杂。

**2. 实用价值：企业级落地的参考范式**
*   **支撑理由（事实陈述）：** 对于正在构建 AI 员工或 RPA（机器人流程自动化）系统的企业，文章提供了一个极具性价比的架构参考。利用轻量级模型做规划可以显著降低 API 调用成本，而专用模型做浏览器操作能绕过传统 RPA 需要针对特定网站写脚本的繁琐，提升了系统的泛化能力。
*   **支撑理由（作者观点）：** 文章展示了如何利用 Amazon Bedrock 的原生编排能力，减少了开发者自己构建 Agent 通信协议的工作量。这对于云原生的开发团队具有直接的指导意义，降低了多 Agent 系统的准入门槛。
*   **反例/边界条件（你的推断）：** 实用性受限于“浏览器操作”这一单一维度。如果任务涉及复杂的文件系统操作、数据库直连或需要极高频率的实时计算，仅依赖浏览器交互的 Agent 会成为性能瓶颈。

**3. 创新性：对“工具调用”模式的深化**
*   **支撑理由（你的推断）：** 行业内普遍讨论的是“大模型 + 插件”模式。本文的创新点在于将“执行者”提升到了与“规划者”对等的 Agent 地位，而非仅仅是一个 Function Call。Nova Act 不仅仅是一个工具，它本身就是一个具备感知和行动能力的 Agent。这种 **Agent-as-a-Tool** 的视角，为解决复杂任务提供了新的思路。
*   **反例/边界条件（事实陈述）：** 这种多 Agent 协作模式并非 AWS 独创，微软的 AutoGen、LangGraph 等开源框架早已提出类似概念。文章的创新更多在于**工程化落地**而非理论突破。

**4. 行业影响与争议：锁定效应与黑盒风险**
*   **行业影响（你的推断）：** 此类文章的发布标志着云厂商开始从“卖模型”转向“卖架构”。它可能推动行业从单一模型竞争转向“模型组合”的竞争，促使开发者更关注模型间的协作能力而非单点智商。
*   **争议点（作者观点）：** 最大的争议在于**厂商锁定**。该架构高度依赖 Bedrock 的特定 API 和 Nova 系列模型的特定能力（如 Act 的浏览器控制）。一旦业务逻辑深入耦合这种 Agent 通信机制，未来迁移到本地部署或其他云服务商的成本将极高。
*   **争议点（事实陈述）：** 多 Agent 系统必然带来**延迟的叠加**。Lite 规划需要时间，Act 执行浏览器操作需要更长时间。在对实时性要求极高的场景（如在线客服、高频交易），这种架构的响应延迟可能是不可接受的。

**实际应用建议**
1.  **引入人类反馈环（HITL）：** 在 Lite 规划后、Act 执行前，增加一个人工确认步骤，防止 Agent 执行不可逆的破坏性操作（如删除数据、下单）。
2.  **监控中间态：** 不要只看最终结果。必须分别监控 Lite 生成的 Plan 质量评分和 Act 的执行成功率，以便快速定位是“脑子想错了”还是“手操作错了”。
3.  **混合架构：** 对于非浏览器类的确定性任务（如 SQL 查询），仍建议使用传统的代码函数，而非强行使用 Act 模型，以平衡准确性与成本。

**可验证的检查方式**

1.  **规划准确率指标：**
    *   *定义：* 在 100 个测试任务中，Amazon Nova 2 Lite 生成的计划步骤是否逻辑通顺且包含了所有必要的前置条件。
    *   *验证方式：* 人工标注或使用更强的模型（如 GPT-4）作为裁判，对 Lite 输出的 JSON 计划进行打分。

2.  **执行端到端成功率：

---
## 学习要点

- Amazon Nova Act 具备突破性的“计算机使用”能力，能够直接操控浏览器界面执行复杂操作，使智能体不仅能处理信息，还能真正完成工作任务。
- Amazon Nova 2 Lite 在多智能体协作中扮演高效的“规划者”角色，能以极低成本将复杂指令拆解为可执行的步骤并分配给其他模型。
- 通过组合使用 Amazon Nova 2 Lite（负责逻辑规划）和 Amazon Nova Act（负责实际执行），开发者可以构建出成本效益极高的“轻量级”智能体系统。
- 这种多智能体协作模式成功解决了单一模型难以同时兼顾深度逻辑推理和高精度操作执行的局限性。
- 借助 Amazon Bedrock 的统一 API，不同模型（如 Lite 和 Act）之间的编排与数据交换变得无缝且易于管理，极大简化了开发流程。
- 该架构展示了未来 AI 应用的趋势，即利用专用模型的分工协作（而非单一超大模型）来获得更优的性能与性价比。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems](https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [blogs_podcasts](/tags/blogs-podcasts/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [🔥GPT-5职场革命！企业如何用AI重塑生产力？🚀]({{< relref "posts/20260127-blogs_podcasts-inside-gpt-5-for-work-how-businesses-use-gpt-5-9.md" >}})
- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260210-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--8.md" >}})
- [亚马逊利用 Nova 模型自动化新履约中心运营就绪测试]({{< relref "posts/20260210-blogs_podcasts-how-amazon-uses-amazon-nova-models-to-automate-ope-0.md" >}})
- [OpenAI在ChatGPT测试广告以支持免费访问]({{< relref "posts/20260210-blogs_podcasts-testing-ads-in-chatgpt-1.md" >}})
- [Transformers.js v4 预览版已发布 NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*