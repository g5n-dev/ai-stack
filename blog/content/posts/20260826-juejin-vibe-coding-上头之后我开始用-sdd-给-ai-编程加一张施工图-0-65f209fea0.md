---
title: "Vibe Coding 上头之后，我开始用 SDD 给 AI 编程加一张“施工图”"
date: 2026-08-26T00:02:56+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:da5d06e10cf7a3304133f36e05f4415244e2447020c6e7c7e036e116909ddf02"
source_payload_sha256: "sha256:54c877f30ca245f5e5ba8763e1fdad7e9a4c5329b943f32cc6485bdfe8ff5034"
source_published_at: 2026-08-25T15:41:17Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:a302010f2f02d786075a7cff0bc74079890b8f821fc0f24c242501fa2efdd779"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
description: "核心结论 SDD（Spec-Driven Development，规范驱动开发）是一套将项目意图显式化的开发方法论。其核心主张是“先把意图写成规范，再让代码成为规范的实现”。"
external_url: https://juejin.cn/post/7677878351721431050
observation_id: obs_65f209fea0b0f9895f18f232aa8dc3e1cdac00634bcbf50c267cf6f3ed3eb4ac
revision_id: rev_ed10f099163808c797f808e6f541d2ec990580c8e91fe807249df0b3d0a2542d
event_id: evt_bcf2d1956c41b4946f4e2246c0d206f17962b5408ac12024b0345ea046e3b57c
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-25T19:47:14.366425Z
last_seen_at: 2026-08-25T16:02:56Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 东风破\_
- **原始来源**: [https://juejin.cn/post/7677878351721431050](https://juejin.cn/post/7677878351721431050)
- **原文发布时间**: Tue, 25 Aug 2026 15:41:17 GMT

## 核心结论

SDD（Spec-Driven Development，规范驱动开发）是一套将项目意图显式化的开发方法论。其核心主张是“先把意图写成规范，再让代码成为规范的实现”。在 AI Coding Agent 场景下，这套方法旨在解决 Vibe Coding 容易出现的上下文丢失问题：模型只知道“做什么”，却缺乏清晰、持久、可验证的项目上下文，导致架构约定在换会话后消失、需求边界模糊时不断返工。

SDD 将规范确立为需求、设计、任务、测试与实现的共同依赖源头，形成“Spec → Plan → Tasks → Implement”的闭环流程。GitHub 的 Spec Kit 将这一流程概括为：先定义做什么，再决定怎么做，接着拆解按什么顺序做，最后才进入实现。这种反转使得规范不再是写完就丢的脚手架，而是贯穿开发全周期的持续参考。

## 能力机制

SDD 的文档体系围绕四个核心问题展开：

proposal.md 回答“为什么做”和“做什么”，包含目标用户、核心场景、MVP 范围、暂不实现的功能以及明确的验收标准。design.md 回答“怎么做”，涵盖技术选型、模块划分、数据流、接口设计以及异常与安全约束。tasks.md 回答“按什么顺序做”，将需求拆解为可执行的任务单元，标注依赖关系和可并行项。代码与测试则回答“是否真的做到了”，通过自动化测试和人工验收确认实现与规范的一致性。

有效规范必须满足三个条件：可执行，即 AI 读完后知道下一步要修改哪些模块；可验证，每个需求都有明确的成功或失败标准；可追踪，需求变化时能够定位受影响的设计、任务、代码和测试。模糊描述如“界面要好看”“接口要稳定”不算合格规范，因为它们无法验收。

## 快速开始

SDD 的启动不要求一次性完成所有文档，而是按顺序推进，每个阶段只聚焦当前目标。

**第一阶段：写 Proposal，明确 MVP 边界**

定义目标用户、核心功能范围和暂不实现的内容。验收标准必须是可观察的行为，而非模糊的质量描述。例如“正文提取失败时，不调用模型，并给出明确提示”“密钥未配置时，不发起网络请求”。主动说清“不做什么”是这份文档的核心价值，因为边界模糊时 AI 最容易过度实现。

**第二阶段：写 Design，提前解决技术风险**

基于 proposal 调研技术方案。Chrome 扩展可使用 Side Panel 替代自定义浮层；正文提取可借助 Mozilla Readability 库；模型接入应面向 OpenAI 兼容接口抽象配置层，而非将某厂商写死在业务代码中。设计文档还需回答异常场景：页面无正文怎么办、文档超长如何分片、请求超时如何处理、密钥如何安全存储。

**第三阶段：拆解 Tasks，让 AI 一次完成一个可验收单元**

每个任务应产生可检查的结果，格式如“T01 初始化 Manifest V3 扩展骨架，验证可以本地加载”。这样做有三个好处：AI 单次上下文更聚焦、问题更容易定位到具体步骤、每完成一步即可提交版本降低回退成本。没有依赖的任务可以并行推进，但“接入真实模型”应排在基础数据流跑通之后。

## 适用边界

SDD 不是多写文档，而是减少 AI 的猜测。文档数量不是重点，能否消除关键歧义才是重点。一个改按钮文案的需求不需要完整 PRD，但开发认证、支付、权限系统则不能只留一句提示词。复杂度越高、影响面越大、不可逆成本越高，规范就应该越严谨。

SDD 适用于需要 AI Coding Agent 持续开发的项目，尤其是功能边界复杂、可能跨越多个会话的中型需求。对于一次性脚本或完全确定的简单任务，Vibe Coding 的快速探索方式仍然适用。SDD 的价值在于让探索出的方向能够被稳定地建造、维护和迭代，而非取代探索本身。

变更管理是 SDD 的重要场景。当需求变化时，应先调研平台能力、更新需求范围与验收标准，再更新技术设计，标记受影响任务，最后修改代码和测试。需求变更不是聊天记录中的一句补充，而是一个可追踪的规范变更。文档和代码应该一起进入版本控制。

## 核验清单

**文档有效性**：proposal 中是否包含明确的验收标准，且每条标准可观察、可验证；design 中是否记录了最终选择方案、放弃其他方案的原因以及依赖的版本约束；tasks 中每个任务是否足够小且包含完成条件。

**规范执行**：文档规模是否与项目风险匹配；是否先写验收标准再写实现方式；是否明确列出非目标。

**变更同步**：代码变更后是否同步更新规范；文档漂移是否被视为缺陷而非“以后再补”；版本控制中是否包含文档与代码的一致性检查。

**AI 协作节奏**：是否按“需求讨论、技术调研、任务拆解、逐项实现”的顺序分工；单次对话是否只承担一种工作；出现问题时是否能定位到具体任务步骤。

## 来源与核验

- [原始文章](https://juejin.cn/post/7677878351721431050)
- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。
- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [掘金](/tags/%E6%8E%98%E9%87%91/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/) / [来源转写](/tags/%E6%9D%A5%E6%BA%90%E8%BD%AC%E5%86%99/)

### 相关文章

- [6.结构化输出](/posts/20260718-juejin-6%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA-0-80d50ad8af/)
- [GitHub Copilot for JetBrains 架构拆解：Provider / Endpoint / Skills / Sandbox / Polic](/posts/20260718-juejin-github-copilot-for-jetbrains-%E6%9E%B6%E6%9E%84%E6%8B%86%E8%A7%A3provider-endpoint-0-2a917f4cdc/)
- [从 Token 到 RAG：我这一周搭起的大模型基础认知地图](/posts/20260718-juejin-%E4%BB%8E-token-%E5%88%B0-rag%E6%88%91%E8%BF%99%E4%B8%80%E5%91%A8%E6%90%AD%E8%B5%B7%E7%9A%84%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80%E8%AE%A4%E7%9F%A5%E5%9C%B0%E5%9B%BE-0-cd9514ced7/)
- [从零到一手撸 Agent 系列 — 第 1 篇：一个 Coding Agent 是什么？](/posts/20260718-juejin-%E4%BB%8E%E9%9B%B6%E5%88%B0%E4%B8%80%E6%89%8B%E6%92%B8-agent-%E7%B3%BB%E5%88%97-%E7%AC%AC-1-%E7%AF%87%E4%B8%80%E4%B8%AA-coding-agent-%E6%98%AF%E4%BB%80%E4%B9%88-0-b0628f7a64/)
- [从BFF到SSE：我在Vue项目里藏了个“AI翻译官”](/posts/20260719-juejin-%E4%BB%8Ebff%E5%88%B0sse%E6%88%91%E5%9C%A8vue%E9%A1%B9%E7%9B%AE%E9%87%8C%E8%97%8F%E4%BA%86%E4%B8%AAai%E7%BF%BB%E8%AF%91%E5%AE%98-0-9ec70466e8/)