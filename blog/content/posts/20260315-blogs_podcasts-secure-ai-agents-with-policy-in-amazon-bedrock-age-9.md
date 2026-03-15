---
title: "利用 Amazon Bedrock AgentCore Policy 实施细粒度访问控制"
date: 2026-03-15T07:34:53+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "访问控制", "Cedar策略", "AI安全", "智能体", "运行时拦截", "身份感知"]
categories: ["安全", "AI 工程"]
source: blogs_podcasts
description: "本文介绍了 Amazon Bedrock AgentCore 中的 Policy 功能，旨在为 AI 智能体构建一个确定性的安全执行层。主要内容包括： 1. **独立执行机制**：Policy 作为一个独立于智能体自身推理之外的强制层，确保业务规则被严格遵守，不受 AI 模型自主决策的影响。 2. **自然语言转策略*"
external_url: https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore
scenarios: ["AI/ML项目", "命令行工具"]
---

# 利用 Amazon Bedrock AgentCore Policy 实施细粒度访问控制

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:16:50+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)

---
## 摘要/简介

在本文中，您将了解 Amazon Bedrock AgentCore 中的 Policy 如何创建一个确定性的执行层，该层独立于 Agent 自身的推理逻辑运行。您将学习如何将业务规则的自然语言描述转化为 Cedar 策略，然后利用这些策略实施细粒度、具备身份感知能力的控制，从而确保 Agent 仅能访问其用户被授权使用的工具和数据。您还将看到如何通过 AgentCore Gateway 应用 Policy，在运行时拦截并评估每一个 Agent 发向工具的请求。

---
## 导语

随着生成式 AI 应用从原型走向生产，如何确保 Agent 在执行任务时严格遵守业务规则与权限边界，成为技术团队面临的关键挑战。本文将深入探讨 Amazon Bedrock AgentCore 中的 Policy 机制，解析其如何通过独立的确定性执行层，将自然语言描述转化为 Cedar 策略。通过本文，您将掌握构建细粒度、具备身份感知能力的控制体系的方法，从而在运行时精准拦截并评估请求，确保 Agent 仅能访问其用户被授权的工具与数据。

---
## 摘要

本文介绍了 Amazon Bedrock AgentCore 中的 Policy 功能，旨在为 AI 智能体构建一个确定性的安全执行层。主要内容包括：

1.  **独立执行机制**：Policy 作为一个独立于智能体自身推理之外的强制层，确保业务规则被严格遵守，不受 AI 模型自主决策的影响。
2.  **自然语言转策略**：支持将业务规则的自然语言描述转换为 Cedar 策略语言。
3.  **细粒度权限控制**：利用这些策略实施基于身份的精细控制，确保智能体仅能访问其用户被授权使用的工具和数据。
4.  **运行时拦截与评估**：通过 AgentCore Gateway 应用策略，在运行时拦截并评估每一个智能体对工具的请求，从而保障操作的安全性。

---
## 评论

**中心观点**
文章主张在构建自主 AI Agent 时，应通过 Amazon Bedrock AgentCore 引入基于 Cedar 语言的独立策略层，将“业务规则判定”从大模型的概率性推理中剥离，以实现可验证、可审计且确定性的安全管控。

**支撑理由与深度评价**

**1. 架构层面的“控制平面”与“数据平面”分离（事实陈述 + 你的推断）**
*   **支撑理由**：文章的核心价值在于指出了当前 AI Agent 落地中的最大痛点：不可预测性。传统的 Agent 通过 Prompt（如 System Prompt）来约束行为，这本质上是一种“软约束”，依赖于模型的推理能力和对齐程度。Bedrock AgentCore 提出的方案是引入一个外挂的、确定性的鉴权引擎（基于 Cedar）。这相当于在 LLM 这个“概率性引擎”之上，覆盖了一个“规则引擎”。
*   **深度分析**：这是对 AI 安全架构的重要修正。它承认了 LLM 不适合作为安全守门员的事实。将“能不能做”的权限检查从 Agent 的“思考过程”中解耦，符合计算机科学中关注点分离的原则。这不仅能防止 Prompt Injection（提示注入）绕过系统指令，还能让合规部门直接审查代码级策略，而不是晦涩的模型权重。

**2. 自然语言到代码的转换降低了策略编写门槛（事实陈述）**
*   **支撑理由**：文章强调了将自然语言业务描述转化为 Cedar 策略的能力。这使得非开发人员（如安全合规官）也能参与定义 Agent 的行为边界。
*   **深度分析**：这一点的实用性极高。在金融或医疗等强监管行业，业务规则极其复杂。如果要求安全专家精通 Rust 或 Cedar 语法，推广成本极高。通过 LLM 辅助生成策略代码，实际上是构建了一个“翻译层”，打通了业务需求与技术实现之间的鸿沟。

**3. 确定性执行是构建可信赖生产级 Agent 的前提（作者观点）**
*   **支撑理由**：文章暗示了只有通过确定性执行，企业才敢将 Agent 接入核心业务系统（如数据库、ERP）。
*   **深度分析**：这是行业从“玩具级 Demo”转向“企业级应用”的关键一步。在 ToC 场景，模型胡说八道可能只是体验问题；但在 ToB 场景，Agent 越权访问数据可能导致法律事故。AgentCore 的这种设计模式，实际上是将 API Gateway 或微服务网关中的传统鉴权逻辑，无缝集成到了 AI 编排层。

**反例与边界条件（批判性思考）**

**1. 边界条件：上下文感知的局限性（你的推断）**
*   **反例**：Cedar 策略虽然是确定性的，但它依赖于传入的上下文属性。如果 Agent 在构建请求时，对“用户意图”或“当前环境状态”的理解出现偏差（例如，将“删除模拟账户”误判为“删除真实账户”并传给 Cedar），那么策略层虽然执行了正确的逻辑（允许删除），但导致了错误的业务结果。
*   **结论**：Policy 层只能解决“权限滥用”，无法解决“意图理解错误”。它假设 Agent 能够准确地将自然语言意图映射为结构化的策略查询参数。

**2. 边界条件：动态性与灵活性的博弈（你的推断）**
*   **反例**：在某些需要高度灵活性的创意生成或探索性任务中，过于严格的确定性策略可能会扼杀 Agent 的“创造力”或导致频繁的任务失败。例如，一个策略规定“只能读取公开数据”，但 Agent 为了回答用户问题，需要综合公开数据和极少量的内部推断，这种模糊地带如果被硬性策略拦截，用户体验会大幅下降。

**可验证的检查方式**

为了验证该技术方案的有效性，建议进行以下检查：

1.  **对抗性测试指标**：
    *   构建一组包含“越狱尝试”和“提示注入”的测试数据集。
    *   **对比实验**：对比仅使用 System Prompt 约束的 Agent 与 使用 Bedrock AgentCore Policy 约束的 Agent。
    *   **验证指标**：统计防御成功率。AgentCore 应能展示出接近 100% 的硬阻断率，而 Prompt 约束通常存在明显的长尾失败案例。

2.  **策略覆盖率与性能测试**：
    *   **检查方式**：观察 Cedar 策略的复杂度与 Agent 响应延迟之间的相关性。
    *   **验证指标**：策略评估的延迟应在毫秒级（<50ms），且不应随策略数量线性增长。如果策略层成为瓶颈，则说明架构设计存在性能缺陷。

3.  **“幻觉-策略”错位观察**：
    *   **检查方式**：在日志中监控 Agent 传递给 Policy 层的 JSON 结构化数据。
    *   **验证指标**：检查是否存在 Agent 提取的参数与用户真实意图不符，但策略层仍予以放行的情况。这能验证“确定性策略”是否掩盖了“非确定性理解”带来的风险。

**总结**

这篇文章从技术与行业角度揭示了 AI Agent 进化的必经之路：**从“依赖模型自觉”转向“强制系统干预”**。它提出的 AgentCore 方案，实际上是在构建 AI 时代的“访问控制基础设施”。虽然它无法完全消除 LLM 本身的理解误差，但通过引入 Cedar 这一确定性层，为 AI 的企业级应用划定了一条不可逾越的安全红线，极具实战价值。

---
## 学习要点

- Amazon Bedrock AgentCore 引入了一种基于策略的机制，允许开发者通过精细化的权限控制来管理 AI 智能体对工具和 API 的访问，从而在实现复杂功能的同时有效防止未授权操作。
- 该框架通过将安全策略与核心代理逻辑解耦，使得安全团队能够独立定义和更新护栏，而无需中断或重新部署整个智能体的应用代码。
- AgentCore 支持动态策略评估，这意味着系统可以根据上下文属性（如用户角色或敏感度）实时决定是否允许特定的工具调用，显著增强了自适应安全能力。
- 这一解决方案解决了构建生成式 AI 应用时常见的安全性与功能性之间的矛盾，使企业能够在不牺牲创新速度的前提下，对自动化智能体的行为实施严格的治理。
- 通过利用 Bedrock 原生集成的这一安全层，企业能够更轻松地满足合规性要求并建立用户信任，因为智能体的行为被限制在预定义的安全边界之内。
- 该架构强调了“纵深防御”的重要性，确保即使智能体被诱导产生恶意意图，底层的策略引擎也能作为最后一道防线拦截危险指令。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-in-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [访问控制](/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/) / [Cedar策略](/tags/cedar%E7%AD%96%E7%95%A5/) / [AI安全](/tags/ai%E5%AE%89%E5%85%A8/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [运行时拦截](/tags/%E8%BF%90%E8%A1%8C%E6%97%B6%E6%8B%A6%E6%88%AA/) / [身份感知](/tags/%E8%BA%AB%E4%BB%BD%E6%84%9F%E7%9F%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [构建确定性 AI 代理安全层：利用 Amazon Bedrock AgentCore 策略]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-6.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore Policy 管控 AI Agent]({{< relref "posts/20260313-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-7.md" >}})
- [构建确定性执行层：利用 Amazon Bedrock AgentCore 策略管控 AI Agent]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-8.md" >}})
- [利用 Amazon Bedrock AgentCore Policy 构建 AI Agent 确定性执行层]({{< relref "posts/20260314-blogs_podcasts-secure-ai-agents-with-policy-in-amazon-bedrock-age-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*