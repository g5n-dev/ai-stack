---
title: "「AI学习笔记」Loop Engineering 和 Graph Engineering"
date: 2026-08-09T22:55:24+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:0172945e9254be9fed21e176fa420937b622af0052edc7a7a4eff47574f36002"
source_payload_sha256: "sha256:37dbee71052c6da5136d0e8210682c1a83cbdac6185d0902197c5acd898c4887"
source_published_at: 2026-08-09T14:28:45Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:5a761a09883416afc3f889a9d51269be0a1659e77e26e3339c13b6ad5c1f5856"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "核心结论 Loop Engineering 与 Graph Engineering 并非竞争关系，而是同一工程思路在不同颗粒度上的体现。前者解决单个 Agent 节点如何自动完成任务，后者解决多个节点之间的拓扑编排与状态流转。"
external_url: https://juejin.cn/post/7671698607829811240
observation_id: obs_f3c0a5eedec23750a7ed5540e7472ced81aaa72daf89cc4a697882509d9c027a
revision_id: rev_8f95d12c9da6e8b48a697fafa464bf0ce85b19bc1dbd28f268767e7870ee5519
event_id: evt_c713dbfd14844e84b6b39409e7048a096a9b93fdb79cefc5b9fb598e61f363e4
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-09T14:52:37.990373Z
last_seen_at: 2026-08-09T14:55:24Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 山间小僧
- **原始来源**: [https://juejin.cn/post/7671698607829811240](https://juejin.cn/post/7671698607829811240)
- **原文发布时间**: Sun, 09 Aug 2026 14:28:45 GMT

## 核心结论

Loop Engineering 与 Graph Engineering 并非竞争关系，而是同一工程思路在不同颗粒度上的体现。前者解决单个 Agent 节点如何自动完成任务，后者解决多个节点之间的拓扑编排与状态流转。LangChain 指出，这两种范式都服务于同一个目标：把模型的推理能力放在真正需要判断的地方，其余交给确定性代码。

## 能力机制

### Loop Engineering 的核心构件

Loop Engineering 强调用系统替代人工逐轮 Prompt，其基础构件包括四个要素：Agent 本身、Verifier（验证器）、反馈路径以及停止条件。缺少 Verifier 会导致 Agent 自行判断“看起来做完了”而停止执行；缺少停止条件则可能产生无限循环。Addy Osmani 等人将这一概念系统化，定义为核心动作是“把手动给 Agent 发 Prompt 的人替换成一套自动化系统”。

### Graph Engineering 的拓扑模型

Graph Engineering 将 Agent 之间的协作关系从隐式（依赖 LLM 自己判断下一步）转变为显式（通过图结构规定合法路径）。图中节点可以是确定性代码、单次 LLM 调用、完整 Agent，也可以是路由器、汇聚点或人工审批检查点。边分为确定性边和条件边（根据节点结果或外部信号动态决定）。整体可视为状态机，状态在图中流动。LangChain 特别指出，生产环境的 Agent 图通常是带环的有向图，而非 DAG，因为需要支持重试、信息补全、用户交互等场景。

## 快速开始

### Loop Engineering 的最小闭环

实现 Loop Engineering 的最小可运行单元需要四个组件协同工作。以伪代码结构为例，实际项目中可参考 Kiro 的 goal 功能或 Claude Code 的 Autopilot 模式，这些工具已内置上述四要素的编排逻辑。核心思路是定义任务目标后，由系统自动驱动 Agent 执行、验证、反馈迭代，直到满足停止条件。

### Graph Engineering 的框架选型

目前 LangGraph 是该领域的代表性框架，已稳定运行三年。对于需要显式工作流控制的场景，可优先考虑支持有向有环图的框架，而非强制使用 DAG 结构。LangChain 自身在 Deep Research 功能开发中也经历了从预定义 LangGraph 工作流到自由 Agent 循环的调整，表明图与循环的选择应依据任务动态性决定。

## 适用边界

### 适合使用 Loop Engineering 的场景

具备以下特征的任务适合 Loop Engineering：有明确、机器可判定的完成标准（如修 lint 报错、批量升级依赖）；可以在沙箱或隔离环境中完全验证的任务（Agent 犯错代价可控）；任务时长本身较长、值得无人值守运行的场景；任务执行者与验证者可以分离的场景（由独立 Evaluator 或 Sub-agent 检查，而非 Agent 自我评分）。

### 适合使用 Graph Engineering 的场景

业务流程具有可预测结构时适合使用图：将固定路径直接编码进拓扑，模型仅在需要判断的节点发挥作用。典型场景包括客服流程（先分类再回答或升级）、编码流程（先读仓库再提改动）、合规流程（审批后才能执行）。

### 不适合使用图工程的场景

任务本身高度自主、步骤难以预定义时（如 Deep Research 类任务：规划、检索、阅读、综合均需动态展开），硬塞进确定性路径反而是错误方向。这类场景更适合直接使用 Agent Harness，让规划和上下文管理在框架内部涌现。

## 核验清单

评估是否需要引入 Loop Engineering 或 Graph Engineering 时，可按以下维度自检：

任务颗粒度判断：若聚焦单个 Agent 的自动驱动，优先考虑 Loop Engineering；若涉及多 Agent 或异构节点的协作编排，引入 Graph Engineering。

停止条件明确性：确认任务存在可判定的完成标准，且该标准可由系统自动验证。

验证器独立性：确保验证逻辑独立于被测 Agent，避免 Agent 自行判断完成状态。

图的环需求评估：若业务流程需要重试、信息补全、用户交互等回环操作，确认所选框架支持有向有环图。

动态性判断：任务步骤是否高度可预测。若是，选择 Graph；若否，考虑 Agent Harness 配合自由循环。

现有框架兼容性：当前项目是否已使用 LangChain/LangGraph、Kiro、Claude Code 等已内置相关能力的框架。

## 来源与核验

- [原始文章](https://juejin.cn/post/7671698607829811240)
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