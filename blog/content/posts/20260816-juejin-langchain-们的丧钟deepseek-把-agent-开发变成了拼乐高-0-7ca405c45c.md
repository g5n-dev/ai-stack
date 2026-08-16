---
title: "LangChain 们的丧钟？DeepSeek 把 Agent 开发变成了拼乐高"
date: 2026-08-16T19:37:31+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:7736f2b324496e23dc3e15f07565b5a6987477c6df87010b1edf4fd534da7f06"
source_payload_sha256: "sha256:cbc52f690aa3387b61af74345830c4380f2e6b271595a680718fb8e1060dfd88"
source_published_at: 2026-08-16T11:04:10Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:b785c47632eea33667a25080edce169d7a2e78c88815fc41cce622432fd5718a"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 40
description: "核心结论 Cordis 提出的是一套协议，而非又一个框架。协议采用 MIT 许可发布，任何人可以用它定义自己的框架实现。核心组件全部可替换，不存在特权代码。框架层由 DeepSeek Harness 提供参考实现。这意味着开发者拿到的不再是“在我家装修”的受限扩展能力，而是“给你一块地，自己决定怎么盖”的完整主权。"
external_url: https://juejin.cn/post/7674145872716513280
observation_id: obs_7ca405c45c5d3c45ddd1bf7e3639daf504f7613443218e890a9d6995228b67f6
revision_id: rev_3ae886bf09e4226488d8ff1692990417568cc10ea84bba3221243714a0a005b8
event_id: evt_df453a3d95208c491a650c679b5f8ac7755e2b7a22e77b589e17f4ec65cd3734
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-16T11:34:05.085583Z
last_seen_at: 2026-08-16T11:37:31Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 一拳不是超人
- **原始来源**: [https://juejin.cn/post/7674145872716513280](https://juejin.cn/post/7674145872716513280)
- **原文发布时间**: Sun, 16 Aug 2026 11:04:10 GMT

## 核心结论

Cordis 提出的是一套协议，而非又一个框架。协议采用 MIT 许可发布，任何人可以用它定义自己的框架实现。核心组件全部可替换，不存在特权代码。框架层由 DeepSeek Harness 提供参考实现。这意味着开发者拿到的不再是“在我家装修”的受限扩展能力，而是“给你一块地，自己决定怎么盖”的完整主权。Cordis 的协议层不绑定 Agent 领域，解决的是组件如何安全地组合、拆分与替换这一通用工程问题。Agent 是其目前最耀眼的应用场景，但非唯一场景。

## 能力机制

Cordis 定义了服务注册、依赖声明、副作用回收、事件通信、组件加载与卸载五类协议。所有参与者包括框架自身核心在内均遵守同一套协议约定，无特权层级。

这一设计导致与传统框架的根本差异。LangChain 的 agent loop 是框架核心代码，修改调度逻辑必须 fork 并自行维护差异。C ordis 的 agent loop 是普通插件，替换调度逻辑只需注册同名服务即可，旧实现自动被降级，无需 fork 任何源码。

系统通过可逆效应、热模块替换与反应式依赖管理实现组件安全替换。卸载旧组件时，框架按 LIFO 顺序自动回滚该组件注册的全部副作用。加载新组件时，框架自动解析依赖并注册新副作用。整个过程对其他组件透明，它们仅感知“服务已变更”，无需了解替换细节。

该机制为自进化 Agent 提供工程基础。运行时检测到需求变化后可按序卸载旧组件、加载新组件，全程不中断服务、不丢失状态。例如发现用户频繁提及日语时可自动挂载翻译插件，发现某工具频繁失败时可卸载并切换替代实现。

## 快速开始

项目代码可从 GitHub 获取，协议为 MIT。Cordis 官方提供文档站点。首个大规模验证案例 Koishi 已在四年周期内积累超过四千个社区插件，覆盖即时通讯适配器、数据库驱动、管理控制台等功能领域。

开发流程通常为定义服务接口、实现插件逻辑、声明依赖与副作用、注册到框架。组件通过事件总线与系统通信，生命周期由框架统一管理。

## 适用边界

该方案适用于需要灵活替换核心组件、追求高度可组合性的开发团队。对于已在传统全家桶框架中受限、无法按需修改核心行为的开发者，协议优先的设计提供了新的选择。跨框架复用工具链的团队可受益于统一的接口标准。

其局限同样需要正视。目前仅有 Koishi 单一生态作为大规模验证案例，编程语言限于 TypeScript。论文坦承缺乏与其他架构的受控对比实验。自进化 Agent 的运行时框架仍为“下一步验证方向”，并非已落地的产品能力。协议层本身的开放性为生态建设奠定基础，但生态成熟度仍取决于社区参与规模。

## 核验清单

- 确认发布时间为 2026 年 8 月 13 日
- 确认协议类型为 MIT
- 确认 DeepSeek Harness 为参考框架实现
- 确认 Cordis 元框架定位为协议层
- 确认 Koishi 案例存在四年积累与四千加插件规模
- 确认自进化 Agent 描述来自论文，为验证方向而非产品功能
- 确认未出现具体性能数据或商业落地报告

## 来源与核验

- [原始文章](https://juejin.cn/post/7674145872716513280)
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