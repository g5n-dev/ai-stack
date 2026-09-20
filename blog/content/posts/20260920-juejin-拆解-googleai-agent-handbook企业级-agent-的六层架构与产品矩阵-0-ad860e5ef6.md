---
title: "拆解 Google《AI Agent Handbook》：企业级 Agent 的六层架构与产品矩阵"
date: 2026-09-20T09:09:50+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:e8d9d452b6a9ca78d9faa113083b9c175b9aa8216c1a1772b5ceb2707acebfa9"
source_payload_sha256: "sha256:94919cb451d6fee76501af6edee58ecd7e1a6332bed47dda007b88de40b953c5"
source_published_at: 2026-09-20T00:57:59Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:9777704dd45fc892993cab7d62c0608432e2def6a16bce1ae548bbb5048a8a86"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
description: "核心结论 该手册将Google企业Agent产品矩阵划分为数据访问层、知识加工层、决策协作层、业务流程层、开发协作层和平台能力层六个层级。用户卷入度和模型能力要求随层级递增：底层仅需RAG加多模态检索，上层需要No-code编排、工具调用和跨Agent通信。"
external_url: https://juejin.cn/post/7687151813254021154
observation_id: obs_ad860e5ef6f3195e1425e4b29711657ecef048afb06f69fec12a21bd7ecbb02f
revision_id: rev_2e5456910d9dab5262cf8bf4c071accbff28b7936e1c33b2bb6e01eca94bc2e0
event_id: evt_06d7b8c132931595f4a0e89805f1dafcfcaa9e6b03538f8e88d9a28fdee8762b
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-20T01:08:05.153250Z
last_seen_at: 2026-09-20T01:09:50Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 怕浪猫
- **原始来源**: [https://juejin.cn/post/7687151813254021154](https://juejin.cn/post/7687151813254021154)
- **原文发布时间**: Sun, 20 Sep 2026 00:57:59 GMT

## 核心结论

该手册将Google企业Agent产品矩阵划分为数据访问层、知识加工层、决策协作层、业务流程层、开发协作层和平台能力层六个层级。用户卷入度和模型能力要求随层级递增：底层仅需RAG加多模态检索，上层需要No-code编排、工具调用和跨Agent通信。

企业搜索被明确定位为Agent系统的“地基”，而非Agent本身。手册原文指出企业搜索虽然技术上不算严格意义上的AI Agent，但它是Agent式AI的基础层。Agent能力链起点是找信息，若此步缺失，后续推理与决策无从实现。

Multi-agent已成为实际产品形态。Customer Engagement Suite明确采用三Agent架构，分别面向客户、客服和管理者。Idea Generation Agent使用数百个Agent生成创意并通过多角度评估实现自评分，这是Agent-as-Judge范式的规模化应用。

Agent2Agent协议被纳入产品支持范围，意味着Google的Agent可与外部平台构建的Agent互通。手册列举的客户案例涉及医疗、教育、咨询、通信、企业软件等多个行业，落地场景包括临床信息检索、市场调研分析、客服通话优化、销售准备、软件开发加速和HR政策查询。

## 能力机制

数据访问层依赖统一入口与预置连接器。Google的解法是Gemini Enterprise作为统一入口，配合预置连接器接入Drive、邮箱、CRM、IT工单、HRIS等散落数据源，并通过Chrome搜索栏实现天然入口覆盖。手册强调没有统一访问层，Agent只能在已接入的单一系统中运行。

知识加工层采用Audio Overviews机制。NotebookLM可将文档转换为播客形式，实现从文本检索到音频输出的知识消费形态转变。

决策协作层通过多Agent分工实现专业聚焦。Customer Engagement Suite的三个Agent分别承担多语言自动响应与路由、实时辅导与推荐、全量交互分析等职责。Idea Generation Agent则采用“生成群加评审群”架构，由一组Agent负责产出创意，另一组Agent负责互评打分和排序输出。

业务流程层通过连接器与现有系统集成。营销场景使用营销连接器，销售场景使用CRM连接器，HR场景集成HR系统，实现Agent能力向现有业务流程的嵌入。

开发协作层提供从现成到自建的分级能力。Agent Gallery提供预置Agent商店，Agent Designer提供No-code聊天式编排界面，Vertex AI Agent Builder面向开发者提供专业构建能力。

平台能力层支持自建Agent的全生命周期管理。Vertex AI Agent Builder提供Agent设计和部署能力，支持No-code编排、工具调用和跨Agent通信需求。

## 快速开始

手册未提供可执行的命令或代码示例。若需评估企业搜索能力，可验证Gemini Enterprise对内部Drive文档、邮件内容和数据库的覆盖范围。若需验证多Agent协作能力，可测试Customer Engagement Suite中三个Agent的分工响应和状态同步。若需验证No-code编排能力，可在Agent Designer中尝试用聊天界面拼接一个简单的信息查询Agent。

## 适用边界

手册定位为企业落地指南，而非技术原理文档。手册有意回避了Agent可解释性、跨系统权限治理、多Agent故障定位和长时任务成本控制等工程级痛点。手册未涉及ReAct、tool use、function calling等底层机制的技术细节。

手册的结论适用于企业级Agent产品规划与定位。对国内做企业Agent的团队，手册提供的分层框架可作为产品坐标参考。手册强调场景必须落到具体工作流，不建议做“通用助手”。手册建议优先构建数据底座，再提升模型能力。

A2A协议值得关注但需跟踪发展。手册提及该协议的支持，但未提供技术规格或实现路径。Agent平台开发者可考虑参与协议制定或保持跟进。

## 核验清单

若计划参考该手册做企业Agent产品规划，建议按以下维度进行核验：

数据底座完整性方面，需要确认已接入的企业系统覆盖范围、跨系统权限模型是否建立、增量更新与定时同步的策略是否明确。

产品定位方面，需要确认产品在六层架构中的目标层级、该层级的竞品分布情况、上下游依赖卡点。

Multi-agent设计方面，需要确认是否需要多Agent分工而非单Agent方案、Agent之间是否需要互评或裁判机制。

分发策略方面，需要确认目标用户是否具备技术背景、是否需要No-code能力支撑业务人员自助使用。

协议兼容性方面，需要确认是否需要与其他平台Agent互通、A2A协议的发展状态是否值得投入跟进。

## 来源与核验

- [原始文章](https://juejin.cn/post/7687151813254021154)
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