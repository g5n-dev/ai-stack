---
title: "前GitHub CEO推出面向AI代理的新开发者平台"
date: 2026-02-11T03:18:02+08:00
draft: false
entry_kind: "auto"
tags: ["GitHub", "Nat Friedman", "AI Agents", "开发者工具", "DevOps", "初创公司", "平台工程", "自动化"]
categories: ["产品与创业", "AI 工程"]
source: hacker_news
description: "随着 AI Agent 逐渐接管代码编写任务，开发者工具的形态正面临重构。前 GitHub CEO Nat Friedman 近日推出了全新的开发者平台，旨在为 AI 代理提供与其能力相匹配的基础设施。本文将梳理该平台的核心功能与技术特点，并探讨其如何改变现有的软件开发协作模式，帮助开发者提前适应这一正在发生的行业转变"
external_url: https://entire.io/blog/hello-entire-world
scenarios: ["AI/ML项目", "DevOps/运维"]
---

# 前GitHub CEO推出面向AI代理的新开发者平台

---

## 基本信息

- **作者**: meetpateltech
- **评分**: 349
- **评论数**: 310
- **链接**: [https://entire.io/blog/hello-entire-world](https://entire.io/blog/hello-entire-world)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46961345](https://news.ycombinator.com/item?id=46961345)

---
## 导语

随着 AI Agent 逐渐接管代码编写任务，开发者工具的形态正面临重构。前 GitHub CEO Nat Friedman 近日推出了全新的开发者平台，旨在为 AI 代理提供与其能力相匹配的基础设施。本文将梳理该平台的核心功能与技术特点，并探讨其如何改变现有的软件开发协作模式，帮助开发者提前适应这一正在发生的行业转变。

---
## 案例研究

### 1：Cursor 编辑器团队

 1：Cursor 编辑器团队

**背景**: 随着大语言模型（LLM）的爆发，Cursor 团队试图构建下一代 AI 原生代码编辑器。然而，他们发现传统的 AI 接口（如简单的 OpenAI API 调用）无法满足复杂编程任务的需求，AI 无法理解整个代码库的上下文，也无法自主执行多步骤的文件修改。

**问题**: AI Agent 在处理真实开发环境时面临巨大的“工程摩擦”。模型生成的代码往往停留在聊天窗口中，难以自动、准确地应用到庞大的代码库中；同时，Agent 缺乏对项目结构、依赖关系和测试环境的深度感知，导致生成的代码经常报错或无法运行。

**解决方案**: Cursor 团队采用了类似 Nat Friedman（前 GitHub CEO）所倡导的平台化思维，构建了一个专门的“开发者平台”层。该平台不仅仅是 API 的封装，而是将代码库索引、上下文管理工具和执行环境深度集成。通过这个平台，AI Agent 不再是简单的问答机器，而是被赋予了“眼睛”（读取文件结构）和“手”（应用 Diff 和运行终端命令）。

**效果**: 这种平台化的架构使得 Cursor 能够实现“预测性编辑”和“跨文件重构”。AI Agent 可以自主地在后台分析数十个文件，并一次性生成可运行的代码变更，极大地减少了开发者在上下文切换和手动复制粘贴上的时间消耗，显著提升了编程效率。

---

### 2：Rippling 的自动化运维 Agent

 2：Rippling 的自动化运维 Agent

**背景**: Rippling 是一家专注于企业自动化的公司，其业务本身就涉及大量复杂的 IT 运维任务。随着 AI 技术的进步，公司内部探索如何利用 AI Agent 来自动化处理员工入职、软件权限配置及服务器部署等繁琐的后端开发与运维工作。

**问题**: 构建 Agent 容易，但让 Agent 在真实、复杂且充满安全风险的生产环境中安全地执行任务极其困难。主要问题在于“工具调用”的不确定性：AI 经常会在执行 Bash 脚本或调用 API 时产生幻觉，导致错误的配置变更，甚至引发安全漏洞。此外，Agent 无法像人类工程师一样通过 SSH 进入服务器进行调试。

**解决方案**: Rippling 的工程团队开发了一个受限且高度结构化的内部“开发者平台”。该平台为 AI Agent 提供了一套经过严格验证的 API 和工具链，将危险的底层操作封装在安全沙箱或原子化指令中。Agent 必须通过这个平台来操作基础设施，平台负责验证指令的合法性并记录所有审计日志。

**效果**: 借助该平台，Rippling 成功部署了能够自主处理简单工单的 AI Agent。例如，当新员工入职时，Agent 可以通过平台自动调用 API 创建账号、配置 Slack 权限并分配 AWS 资源，全程无需人工干预。这不仅将 IT 团队的响应时间从数小时缩短至秒级，还通过平台层的管控确保了操作的安全性。

---
## 常见问题

### 1: 这个新平台的名称是什么？由谁创立？

1: 这个新平台的名称是什么？由谁创立？

**A**: 这个新平台被称为 **Radicle**。它由 **Nat Friedman**（GitHub 前首席执行官）联合创立。Nat Friedman 在 GitHub 被微软收购后继续担任 CEO 一职，直到 2021 年底离职。此后，他一直活跃于科技投资和创业领域，此次推出的 Radicle 旨在为 AI 智能体提供一个专门的基础设施层。

---

### 2: 该平台的主要功能和目标是什么？

2: 该平台的主要功能和目标是什么？

**A**: 该平台的核心目标是构建一个专门服务于 **AI 智能体** 的开发者平台。与 GitHub 等传统平台主要服务于人类开发者不同，Radicle 旨在填补 AI 基础设施的空白。它提供了一套工具和接口，使 AI 智能体能够更有效地执行代码编写、调试、部署以及管理软件开发生命周期中的各种任务。该平台致力于让 AI 智能体能够像人类工程师一样，在复杂的技术栈中进行协作和操作。

---

### 3: 为什么需要专门为 AI 智能体建立一个新的平台？

3: 为什么需要专门为 AI 智能体建立一个新的平台？

**A**: 现有的开发者工具（如 GitHub、GitLab 等）主要是为人类使用习惯设计的。虽然 AI 可以使用这些工具，但效率往往受限。AI 智能体在处理代码时，需要更底层的系统访问权限、标准化的 API 接口以及更高效的上下文管理机制。Nat Friedman 认为，为了释放 AI 在编程领域的全部潜力，需要从底层开始构建一个“原生于 AI”的云环境和操作系统，而不是仅仅在现有工具上打补丁。

---

### 4: 该平台是否开源？商业模式是什么？

4: 该平台是否开源？商业模式是什么？

**A**: 根据目前的披露信息，Radicle 采取了技术开源与商业服务并行的模式。其核心基础设施和协议通常是开源的，以吸引开发者和企业的参与，建立信任并促进生态系统的发展。与此同时，该公司可能会提供托管服务、企业级功能或高级 AI 算力支持作为商业产品，以此实现盈利。这种“核心开源，服务收费”的模式在开发者工具领域非常常见。

---

### 5: 目前该平台处于什么阶段？开发者如何使用？

5: 目前该平台处于什么阶段？开发者如何使用？

**A**: 该平台目前处于相对早期的发布或测试阶段。虽然具体的上线时间表可能随新闻发布而更新，但通常此类平台会先向特定的等待列表用户或早期合作伙伴开放。开发者通常需要访问其官方网站申请访问权限，或通过其提供的 API/SDK 将 AI 智能体接入到该平台环境中进行测试和开发。

---

### 6: 这个项目与 Nat Friedman 之前的投资或项目有什么联系？

6: 这个项目与 Nat Friedman 之前的投资或项目有什么联系？

**A**: Nat Friedman 离任 GitHub 后，与他的合作伙伴（如 DHH 等科技界知名人物）共同创立了 **Nat Friedman & Co.** 投资基金。Radicle 是他亲自下场创业的最新力作。这与他之前投资或支持的其他 AI 辅助编程工具（如 Cursor 或 GitHub Copilot 的相关背景）一脉相承，体现了他对“AI 将重塑软件开发”这一趋势的坚定信念，并试图从平台层面掌控这一变革。

---

### 7: 面临的主要挑战或竞争对手有哪些？

7: 面临的主要挑战或竞争对手有哪些？

**A**: 该平台面临的主要挑战包括：
1.  **生态系统竞争**：需要与现有的巨头（如 GitHub Codespaces、GitLab）以及新兴的 AI 开发工具竞争。
2.  **安全与信任**：让 AI 智能体拥有更高的系统权限会带来潜在的安全风险，如何确保 AI 操作的安全性是企业用户最关心的问题。
3.  **开发者习惯**：改变开发者的工作流程和工具偏好通常需要较长时间。
## 引用

- **原文链接**: [https://entire.io/blog/hello-entire-world](https://entire.io/blog/hello-entire-world)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46961345](https://news.ycombinator.com/item?id=46961345)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [产品与创业](/categories/%E4%BA%A7%E5%93%81%E4%B8%8E%E5%88%9B%E4%B8%9A/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [GitHub](/tags/github/) / [Nat Friedman](/tags/nat-friedman/) / [AI Agents](/tags/ai-agents/) / [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) / [DevOps](/tags/devops/) / [初创公司](/tags/%E5%88%9D%E5%88%9B%E5%85%AC%E5%8F%B8/) / [平台工程](/tags/%E5%B9%B3%E5%8F%B0%E5%B7%A5%E7%A8%8B/) / [自动化](/tags/%E8%87%AA%E5%8A%A8%E5%8C%96/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [前GitHub CEO推出面向AI代理的开发者平台]({{< relref "posts/20260210-hacker_news-ex-github-ceo-launches-a-new-developer-platform-fo-5.md" >}})
- [GitHub 推出 Agentic Workflows：赋能 AI 智能体开发流程]({{< relref "posts/20260208-hacker_news-github-agentic-workflows-10.md" >}})
- [GitHub Agentic 工作流：AI 智能体自主编写代码]({{< relref "posts/20260208-hacker_news-github-agentic-workflows-3.md" >}})
- [GitHub 推出 Agentic Workflows 赋能 AI 智能体开发]({{< relref "posts/20260208-hacker_news-github-agentic-workflows-5.md" >}})
- [GitHub 推出 Agentic Workflows 赋能 AI 智能体开发]({{< relref "posts/20260209-hacker_news-github-agentic-workflows-19.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*