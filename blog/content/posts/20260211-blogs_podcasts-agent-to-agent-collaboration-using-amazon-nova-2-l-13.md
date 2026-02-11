---
title: "Agent-to-agent collaboration: Using Amazon Nova 2 Lite"
date: 2026-02-11T07:44:29+08:00
draft: false
entry_kind: "auto"
tags: ["Multi-Agent", "Amazon Bedrock", "Agent 协作", "Amazon Nova", "Browser Use", "LLM", "系统架构", "AI Agent"]
categories: ["AI 工程", "大模型"]
source: blogs_podcasts
description: "This post walks through how agent-to-agent collaboration on Amazon Bedrock works in practice, using Amazon Nova 2 Lite for planning and Amazon Nova Act for brow"
external_url: https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent-to-agent collaboration: Using Amazon Nova 2 Lite and Amazon Nova Act for multi-agent systems

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:00:28+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems](https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems)

---
## 摘要/简介

This post walks through how agent-to-agent collaboration on Amazon Bedrock works in practice, using Amazon Nova 2 Lite for planning and Amazon Nova Act for browser interaction, to turn a fragile single-agent setup into a predictable multi-agent system.

---
## 学习要点

- Amazon Nova Act 具备直接操作用户界面（UI）的能力，能够自主完成点击、滚动和填写表单等复杂任务，无需依赖 API 集成。
- 利用 Amazon Nova 2 Lite 作为中央控制器，可以高效地将复杂工作流分解为子任务并分发给其他代理，实现多代理编排。
- 该多代理架构通过将推理与执行分离，显著降低了系统构建的复杂性，并提高了自动化流程的容错能力。
- Amazon Nova 2 Lite 能够根据上下文动态决定是直接回答用户问题还是调用 Nova Act 执行具体操作，实现了灵活的任务路由。
- 这种代理协作模式展示了如何通过结合强大的推理模型与具备行动能力的模型，来构建端到端的自动化解决方案。
- 该方案验证了在无需编写大量定制代码的情况下，利用基础模型快速构建能够操作真实软件系统的智能体的可行性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems](https://aws.amazon.com/blogs/machine-learning/agent-to-agent-collaboration-using-amazon-nova-2-lite-and-amazon-nova-act-for-multi-agent-systems)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Multi-Agent](/tags/multi-agent/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [Agent 协作](/tags/agent-%E5%8D%8F%E4%BD%9C/) / [Amazon Nova](/tags/amazon-nova/) / [Browser Use](/tags/browser-use/) / [LLM](/tags/llm/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/) / [AI Agent](/tags/ai-agent/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [迈向智能体系统规模化科学：工作原理与适用条件]({{< relref "posts/20260201-hacker_news-towards-a-science-of-scaling-agent-systems-when-an-13.md" >}})
- [Agent评估显示AGENTS.md配置优于Skills]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-4.md" >}})
- [Agent评估显示AGENTS.md配置优于技能配置]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-6.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
- [编码代理的成功对通用AI系统的启示]({{< relref "posts/20260130-hacker_news-what-the-success-of-coding-agents-teaches-us-about-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*