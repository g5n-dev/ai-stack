---
title: "从 Prompt 到 Graph：AI 工程的进化史"
date: 2026-08-10T12:56:59+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:b2a7c8fd2c73f94a05552b2a44a1c0fa366df5800427abda1339ce4e1f53596f"
source_payload_sha256: "sha256:c59feff8ae34abf98b8997801262d430053b6775323dadff9a16e4275fb9260c"
source_published_at: 2026-08-10T04:40:01Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:4e364cc0ddd376359c1c28915a7d249dd594beefd4da72d385691e82003c04b4"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 26
description: "核心结论 AI工程方法论在过去几年间经历了五层演进：Prompt、Context、Harness、Loop、Graph。这五层并非相互替代，而是将问题的杠杆逐步上移的过程。早期关注单次交互的提问技巧，后期转向整个工作流程的组织方式。"
external_url: https://juejin.cn/post/7671708220172582947
observation_id: obs_1141ab86a66564d4b6f77e4eb0a16378ec95db9adc5691cadb3c9addd8a8b96d
revision_id: rev_c73ee68025caeef0d4750b38dfe8af12c5bc5ac5b1bb0bae323f1e852cf15298
event_id: evt_b5265f7a1acb1bb55f9b7f4ccb6c04bd71ae1deb4496295ee6e7645577f14255
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-10T04:53:41.598985Z
last_seen_at: 2026-08-10T04:56:59Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 朱涛的自习室
- **原始来源**: [https://juejin.cn/post/7671708220172582947](https://juejin.cn/post/7671708220172582947)
- **原文发布时间**: Mon, 10 Aug 2026 04:40:01 GMT

## 核心结论

AI工程方法论在过去几年间经历了五层演进：Prompt、Context、Harness、Loop、Graph。这五层并非相互替代，而是将问题的杠杆逐步上移的过程。早期关注单次交互的提问技巧，后期转向整个工作流程的组织方式。

文章指出，当前许多自动化流程的问题不在于模型能力不足，而在于验证环节的缺失——代码通过单测不代表产品在真机上可用。有效的做法是将验收锚点放置在系统外部，确保单测绿、真机验证通过、人工批准交付这些条件不被绕过。

## 能力机制

Prompt层解决的是单次交互的提问方式。2020年GPT-3证明了few-shot示例的有效性，2022年Chain-of-Thought引导模型输出中间推理步骤。这些技巧在当前仍发挥作用，但只管单轮对话的质量。

Context层管理模型在特定时刻能看到什么。2024年Anthropic开源的MCP协议将工具调用、数据查询统一为标准化接口。注意力预算有限意味着需要主动选择进入上下文的token，而非简单塞满。

Harness层构建单个Agent的运行环境。Anthropic提出的长任务范式将规划、生成、评估分离，使用文件交接、必要时清空上下文再续。这层补足了模型本身做不到的能力，如工具权限控制、沙箱隔离、会话重置等。

Loop层用系统调度替代人工操作员。设计Automations、Worktrees、Skills、Connectors等组件，配合落在磁盘上的State实现自动化调度。核心价值在于把人从反复的Prompt操作中解放出来。

Graph层处理多条Loop或多个Agent之间的组织关系。包括依赖顺序、并行汇合、失败回退路径、检查点设置等。LangGraph在2024年已提供有状态图的实现框架。

文章介绍的Munk AI将上述能力落地为具体实现：Work对应单条需求的闭环执行，WorkSet对应多条需求的图结构编排，Device MCP提供真机验证能力。

## 快速开始

当前版本支持MacOS和Android端。桌面端下载地址为munk.sh/zh/install，可访问官网获取安装包。

运行时的外部依赖通过环境变量配置，具体变量名称参考官方文档说明。应用启动后可创建Work处理单条需求，或创建WorkSet编排多条Work的依赖关系。

## 适用边界

这套方法论主要面向需要持续运行的自动化工作场景，尤其是跨越编码、检查、部署、验证、交付多个环节的完整流程。个人和小团队可将默认工作单元从单次对话转变为可自动迭代的Loop。

对于简单的单次问答场景，基础Prompt技巧已足够，无需引入完整的Harness或Loop机制。当工作涉及多角色协作、多步骤依赖、或需要跨真机验证时，Graph层的组织能力和Device MCP的验证能力才真正发挥价值。

文章特别指出，Graph层适合的场景是“需要把流程画清楚”的情况。一旦画出来，许多以前靠聊天隐含过去的步骤就会暴露问题。如果流程本身尚未理清，强行上Graph可能反而增加复杂度。

## 核验清单

检查当前任务是否真的需要Loop机制。如果每次只需一条Prompt就能完成，Prompt层已足够，不必过度工程化。

确认验收标准是否明确定义且外部化。单测通过不等于产品可用，需要明确哪些步骤必须在真机或真实环境中验证通过。

评估Harness层的组件是否与当前模型能力匹配。Anthropic的建议是模型变强后，过时的脚手架应当拆除，而非保留所有历史配置。

验证多Agent或多条Work的依赖关系是否已梳理清楚。使用Graph结构前，确保每个节点的输入输出、失败回退路径、人工介入点都已明确。

确认Device MCP的验证结果能够回传到执行侧。真机验证的截图和界面结构数据需要成为闭环的一部分，而非仅作为人工参考。

## 来源与核验

- [原始文章](https://juejin.cn/post/7671708220172582947)
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