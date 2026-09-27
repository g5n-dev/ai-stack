---
title: "从 LangChain 到 LangGraph：多 Agent 不是玄学，是 token 账本和干扰问题"
date: 2026-09-27T16:11:58+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:69ad291c93fe317cacdcdbad3047b6ea3ab702a6703cc6e9b2dad40d2e86bbbd"
source_payload_sha256: "sha256:b5316837de07b232a7dfe22312c74f10aefeb732141c1f3cb60fe0730d47f4d1"
source_published_at: 2026-09-27T07:11:36Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:d2971b6e9c729345687620abda7b2a97f2c6378dae1196fed5cefe5b9cab9922"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
description: "核心结论 多 Agent 拆分本质是 token 开销与信息干扰的工程权衡。LangChain 负责线性工作流编排和基础模块，LangGraph 专注于网状工作流编排，处理多 Agent 协作中的分支、循环、状态持久化和人工中断场景。两者的关系是配合而非替代。"
external_url: https://juejin.cn/post/7689415591787266074
observation_id: obs_7862cbf2567f3049cabb793df7783e8abbac4761d3899f1695d089416a5ad01c
revision_id: rev_290281318a9c7533454bddc2a6db2d935e981174e26b5c6f7a31bfa61b619ab1
event_id: evt_a6b91f56b8a045debc96067e0091d856419512376230dcc9f44a3dbf91642eac
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-27T08:08:41.746576Z
last_seen_at: 2026-09-27T08:11:58Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: BreezeJiang
- **原始来源**: [https://juejin.cn/post/7689415591787266074](https://juejin.cn/post/7689415591787266074)
- **原文发布时间**: Sun, 27 Sep 2026 07:11:36 GMT

## 核心结论

多 Agent 拆分本质是 token 开销与信息干扰的工程权衡。LangChain 负责线性工作流编排和基础模块，LangGraph 专注于网状工作流编排，处理多 Agent 协作中的分支、循环、状态持久化和人工中断场景。两者的关系是配合而非替代。

LangGraph 的核心架构由 State、节点、边三要素构成：State 声明状态 schema 并定义 reducer 规则，节点是返回部分状态更新的普通函数，边负责连接节点并控制流转方向。

## 能力机制

**State 声明**：通过 `Annotation.Root` 定义状态结构，字段级 reducer 决定状态合并方式，default 提供初始值。新值覆盖旧值是常见的 reducer 实现模式。

**分支路由**：在节点内完成条件判断并将结果写入 state，条件边根据 state 中的路由标识将执行流导向对应节点。关注点分离使判断逻辑与业务逻辑解耦。

**循环实现**：没有专门的循环 API，条件边指向自身即形成自环。需要配合计数器和终止条件避免死循环，三要素为自环、计数、终止条件。

**状态持久化**：通过 `compile` 时挂载 checkpointer 实现，invoke 时传入 thread_id 标识会话。同一个 thread_id 连续调用会累加状态，换 thread_id 则从初始值重新开始。MemorySaver 存储在内存中，失败后可恢复；生产环境可替换为 sqlite、redis 等持久化方案。

**人工中断**：节点内调用 `interrupt()` 暂停执行并抛出 payload，调用方从返回结果的 `__interrupt__` 字段读取中断信息，使用 `Command({resume})` 配合同一 thread_id 恢复执行。interrupt 依赖 checkpointer 保存暂停状态。

## 快速开始

最小图的构建流程：

```javascript
import { Annotation, StateGraph, START, END } from '@langchain/langgraph'

const StateAnnotation = Annotation.Root({
  text: Annotation({
    reducer: (_prev, next) => next,
    default: () => "",
  }),
})

const step1 = (state) => ({ text: `${state.text} -> step1` })
const step2 = (state) => ({ text: `${state.text} -> step2` })

const graph = new StateGraph(StateAnnotation)
  .addNode("step1", step1)
  .addNode("step2", step2)
  .addEdge(START, "step1")
  .addEdge("step1", "step2")
  .addEdge("step2", END)
  .compile()

// 可视化导出
const drawable = await graph.getGraphAsync()
console.log(drawable.drawMermaid({ withStyles: true }))

// 执行
const result = await graph.invoke({ text: "hello" })
```

持久化需要挂载 checkpointer：

```javascript
import { MemorySaver } from '@langchain/langgraph'

const checkpointer = new MemorySaver()
const graph = new StateGraph(StateAnnotation)
  .addNode("visit", visit)
  .addEdge(START, "visit")
  .addEdge("visit", END)
  .compile({ checkpointer })

const config = { configurable: { thread_id: "用户_小张" } }
await graph.invoke({}, config)
```

中断恢复示例：

```javascript
const waitConfirm = (state) => {
  const text = interrupt({
    hint: "输入确认或备注后回车",
    actionSummary: state.actionSummary,
  })
  return { useInput: String(text) }
}

const paused = await graph.invoke({}, config)
const line = await readLine() // 人工确认
const done = await graph.invoke(new Command({ resume: line }), config)
```

## 适用边界

LangGraph 适用于需要多 Agent 协作的工作流，每个 Agent 可携带精简 prompt 减少 token 消耗并降低干扰。网状编排能力适合包含分支判断、重试逻辑、长期状态维护和人工审批节点的应用场景。

不适合纯线性任务，LangChain 的链式结构已能覆盖的场景无需引入 LangGraph 的额外复杂度。

interrupt 机制要求调用方具备接收暂停、读取状态、等待人工输入、恢复执行的能力，纯粹的自动化流程无法直接使用该特性。

状态持久化依赖 checkpointer，缺少该配置时中断后无法恢复。MemorySaver 仅存储在内存中，服务重启会丢失状态。

所有示例代码均为静态整理，未经过运行验证。实际使用需要根据 LangGraph 版本调整 API 调用方式。

## 核验清单

- State 的每个字段都定义了 reducer 和 default
- 节点返回值是部分状态更新，而非完整 state
- 条件函数返回值与映射表 key 一一对应
- 自环包含终止条件，不会形成死循环
- 需要持久化的图已挂载 checkpointer，invoke 时携带 thread_id
- interrupt 恢复使用同一 thread_id 配合 `new Command({resume})`
- `drawMermaid` 输出可导入 mermaid 渲染器验证图结构

## 来源与核验

- [原始文章](https://juejin.cn/post/7689415591787266074)
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