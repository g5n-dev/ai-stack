---
title: "Workflow vs Agent：别再被“调包侠”忽悠了，一张图看懂AI工程的“骨架”与“大脑”"
date: 2026-07-23T04:25:53+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:74a7062f254782c1196cf6aa0ba1dc82b1e354454dee8966393eeebe033870dd"
source_payload_sha256: "sha256:5cb8710637da243cbda89dd562493e70052fba360a1b42a0aa6a58448bccf300"
source_published_at: 2026-07-22T15:17:27Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:0a5a8ee3fdbb0071b6671a00580ad99f6a929467b20a33d72bb3280637035d81"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
description: "核心结论 Workflow与Agent的本质区别在于控制权归属。Workflow的控制权掌握在开发者手中，路径通过硬编码的图结构预先定义，工具调用按预设规则触发，其核心价值在于提供确定性，消除意外状况。"
external_url: https://juejin.cn/post/7664862232594661402
observation_id: obs_5db02ad9c4fb03a448d510db8fa148db661ef139b8a64e98ef820cc67b884c22
revision_id: rev_4932492b57265a62efa25f4f49fd7bda838404f8186471ac02c2f811c7bbc573
event_id: evt_0fa99fa336cfb57fce8cfbcbd31292b6f48081a02059e06e77fba7ec54c8be9e
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-07-23T00:18:01.981073Z
last_seen_at: 2026-07-23T00:00:00Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 陳陈陳
- **原始来源**: [https://juejin.cn/post/7664862232594661402](https://juejin.cn/post/7664862232594661402)
- **原文发布时间**: Wed, 22 Jul 2026 15:17:27 GMT

## 核心结论

Workflow与Agent的本质区别在于控制权归属。Workflow的控制权掌握在开发者手中，路径通过硬编码的图结构预先定义，工具调用按预设规则触发，其核心价值在于提供确定性，消除意外状况。Agent则将控制权交给模型在运行时进行决策，路径由模型实时生成的思维链决定，工具由模型按需自主选择，核心价值在于适应性，能够拥抱变化。

来源指出，2026年一项arXiv研究显示，企业多智能体LLM系统生产部署失败率在41%至86.7%之间，其中约79%的失败根源并非模型能力不足，而是团队本身没有明确区分所构建的系统究竟属于Workflow还是Agent。

判断标准为：当出现意外情况时，由代码中的条件判断逻辑处理还是由大模型临场发挥。Workflow是预设的有向无环图，LLM在其中充当高级计算器角色。真正的Agent必须具备三大核心组件：感知器负责理解当前文本、图像和上下文环境；规划器动态生成任务链而非读取预设清单；执行器调用工具并根据结果反思修正下一步。

## 能力机制

Agent最核心的底层架构是ReAct，全称Reasoning plus Acting。该架构不采用一次性输出结果的方式，而是进入“思考-行动-观察”的循环。这一设计源于现实世界信息不完整的特性，Agent通过逐步探索来完成任务，而非一次性猜测答案。

从LangChain v1.0版本起，Agent的底层实现从AgentExecutor迁移至LangGraph。LangGraph是基于状态机的编排框架，其核心作用是解决Agent的可观测性和可恢复性问题，允许对Agent的每一步进行暂停、回滚和审查。但需明确的是，使用状态机作为底层并不等同于Workflow，关键差异在于：状态机中的下一步由LLM的推理结果驱动，而非由代码预定义。

工程实践中，不应为Agent编写具体步骤剧本，而应提供工具集和系统提示词作为约束，让模型自主决定行动顺序。来源提出“三明治架构”用于设计可控Agent：上层Workflow定义Agent的行动边界；中层Agent在边界内自由规划路径；下层Workflow落地执行具体API调用，保证原子操作的稳定性。

## 快速开始

Workflow开发聚焦于预定义流程图的构建，将人类专家经验固化为状态机逻辑。节点包括输入、LLM调用、条件判断、图像生成、输出等类型，通过管道串联成流水线。适合使用轻量级小模型运行固定分支，Token成本相对较低，延迟可控制在毫秒级。

Agent开发需准备工具集和系统提示词。工具集提供模型可调用的能力接口，系统提示词定义行为约束和目标。开发阶段建议引入Human-in-the-loop机制，在关键决策点设置人工确认环节。部署后可对Agent的思考-行动-观察循环进行监控和回溯。

来源提供的伪代码展示了两种思维的核心差异：Workflow采用线性步骤固定执行，当出现异常输入时流程无感知；Agent使用while循环持续检查目标达成状态，发现铜价波动超过阈值时调用历史数据对比和突发事件搜索工具，重写分析逻辑并加入风险预警，同时具备自我校验能力，信息不足时会主动补充搜索。

## 适用边界

以下场景优先选择Workflow：金融风控、合同审批、合规审计等需要留痕和可解释性的领域，出了问题需能追溯至具体步骤；重复性高、大批量、容错率极低的批处理任务；延迟敏感型业务，毫秒级响应要求；以及成本敏感型场景，Workflow的Token消耗显著低于Agent的推理循环。

以下场景适合引入Agent：输入形态多变、无法穷举所有分支的交互式任务；需要模型自主判断下一步行动的场景；以及分支过于复杂、导致Workflow结构变成“意大利面条式代码”的场景。当前主流架构模式是将两者结合的“Agentic Workflow”，即用Workflow的骨架约束Agent的野性，同时用Agent的智慧弥补Workflow的死板。

来源提醒市面上约80%的所谓“Agent”属于伪需求。鉴别方法包括：若将中间的LLM替换为简单规则引擎系统仍能运行，则为假Agent；若用户输入流程图未覆盖的需求时直接报错而非尝试解决，则为假Agent。

## 核验清单

开发前需确认团队对系统类型的定义是否清晰，是确定性优先还是适应性优先。需明确系统属于Workflow、Agent还是Agentic Workflow，避免概念混淆。

开发中需检查是否为Agent提供了清晰的工具集和系统提示词，而非预写详细步骤剧本。需确认是否设置了Human-in-the-loop机制用于关键决策点。需验证状态机或流程图的逻辑覆盖度，对边界情况有预判或兜底方案。

部署后需监控异常处理的实际表现，确认意外输入不会导致死循环或系统崩溃。Agentic Workflow需同时监控上层边界是否被遵守、下层执行是否稳定。来源指出Agent适合用满意度而非准确率进行KPI考核，且需防止Agent为达成量化指标而产生不当行为。

## 来源与核验

- [原始文章](https://juejin.cn/post/7664862232594661402)
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