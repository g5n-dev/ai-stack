---
title: "AI 写代码总跑偏？用 spec-superflow 把规划引擎和执行纪律焊成一条流水线"
date: 2026-08-09T12:38:05+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:99f80fb8c11688076f838ff7d31da61862f284cf0d8a9d83d8f0bff0dfd90483"
source_payload_sha256: "sha256:49350aacce5237ad509a9d62d5ec76f977a1c4cd6d7c5f700e54ccd6eb131736"
source_published_at: 2026-08-09T04:00:39Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:a6623130010e57a3b2bdcbbe793c992767f6adf3091549aa14515c3d6ff8b6a7"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "核心结论 spec-superflow 将 OpenSpec 规划引擎与 Superpowers 执行纪律在源码层面融合为一个工作流插件。该工具通过 9 个 Skill 串联 8 个显式状态，并在两者之间建立 execution-contract.md 作为强制交接层，从机制上解决 AI 编程中「规划与执行脱节」的核…"
external_url: https://juejin.cn/post/7671508846049607722
observation_id: obs_df97b332175cf95c71ae2506f9b89bd544bece3e451123391b1e74dce1353d14
revision_id: rev_70a8cb4bd708bfd2a65f7edfe6284c542da963ce4b3fd325dc6dffcf53726f3f
event_id: evt_84f67d43d957da328de00c71378dbc6e64bf3ad9596c4242e7370dcb4304daf2
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-09T07:15:56.575765Z
last_seen_at: 2026-08-09T04:38:05Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 码哥字节
- **原始来源**: [https://juejin.cn/post/7671508846049607722](https://juejin.cn/post/7671508846049607722)
- **原文发布时间**: Sun, 09 Aug 2026 04:00:39 GMT

## 核心结论

spec-superflow 将 OpenSpec 规划引擎与 Superpowers 执行纪律在源码层面融合为一个工作流插件。该工具通过 9 个 Skill 串联 8 个显式状态，并在两者之间建立 execution-contract.md 作为强制交接层，从机制上解决 AI 编程中「规划与执行脱节」的核心问题。当前版本 v0.9.0，支持 17 个 AI 编程平台。

## 能力机制

### 九阶段 Skill 架构

工具将变更生命周期划分为 9 个技能域，每个 Skill 职责单一。入口 Skill `workflow-start` 负责状态路由；`need-explorer` 执行一问一答式探索并提供方案对比；`spec-writer` 按 proposal、specs、design、tasks 顺序产出规划工件；`contract-builder` 将四类工件压缩为执行契约；`build-executor` 驱动 TDD/SDD 模式执行；`bug-investigator` 执行四阶段根因分析；`code-reviewer` 输出结构化审查；`release-archivist` 验证并归档；`spec-merger` 将增量规范合并回主分支。

### 契约桥接机制

`contract-builder` 的核心作用是消除规划与执行之间的断层。它将 proposal 提取为意图锁和范围栅栏，从 specs 提取已批准需求与测试义务，从 design 提取架构约束，从 tasks 提取执行批次与审查时机。这份契约在执行阶段具有唯一约束力，AI 不再自由引用聊天记录。契约内置内容级过期检测，当 proposal 范围溢出、specs 需求变更或 design 约束漂移时，系统自动回退至 contract-builder 重建契约。

### 三重执行纪律

`build-executor` 内置三重硬约束。TDD 铁律要求 RED→GREEN→REFACTOR 循环，未见失败测试不得写生产代码。SDD 子代理驱动模式要求先在 `.superpowers/sdd/execution-plan.json` 保存带依赖和策略的执行计划，再按 wave 派发子代理。Review Gate 要求每个 wave 必须产出非空 review report 并记录 pass receipt，否则阻断后续流程。

### 模式自动降级

系统根据文件数量和变更类型自动降级工作流。full 模式执行完整流程；hotfix 模式（≤2 文件）可跳过规划工件但仍需最小契约并经 DP-3 批准；tweak 模式（≤4 文件、纯配置或文档）无需契约和执行计划，可直接从 exploring 跳转至 approved-for-build。

## 快速开始

安装方式因平台而异。Claude Code 用户执行 `/plugin marketplace add MageByte-Zero/spec-superflow` 后安装插件。Cursor 用户运行 `npx spec-superflow@latest install-cursor`。全局 CLI 通过 `npm install -g spec-superflow` 安装。

安装完成后可通过三个命令进行基本操作：`ssf list` 列出所有变更及状态；`ssf doctor` 执行健康检查；`ssf validate .` 验证工件完整性。恢复会话时使用「继续上次的工作流」，查询状态时使用「帮我看看现在该干什么」，系统会进行内容级判断并路由至正确 Skill。

## 适用边界

该工具适用于大型功能开发、多人协作项目、长期维护的代码库、需要 TDD 与 Review Gate 约束的棕地改造。在这些场景下，规范文档与执行契约能够有效防止 AI 大规模修改文件时偏离原始意图。

不适用场景包括一次性脚本编写与纯咨询问答。这类场景的变更范围极小，引入完整工作流反而增加不必要的开销。

工具的核心价值在于将「人的确认」精确安插在 8 个决策点（DP-0 至 DP-7），而非在所有环节均依赖人工干预。DP-3 契约批准是唯一的硬门禁，其余决策点多为信息确认，成本低但护栏实。

## 核验清单

检查点一：确认 execution-contract.md 已生成且经 DP-3 批准，未批准状态 build-executor 不得启动。

检查点二：TDD 模式下每个 wave 必须先有失败测试用例，再有生产代码实现，测试套件全程保持绿色。

检查点三：每个 wave 完成后必须有 code-reviewer 出具的 review report 并记录 pass receipt，下一 wave 或 closing 阶段才可放行。

检查点四：需求变更时必须回退至 specifying 或 bridging 状态重建契约，不允许在契约外直接修改代码。

检查点五：调试阶段遇到 3 次以上修复失败应触发架构质疑流程，而非继续试错。

## 来源与核验

- [原始文章](https://juejin.cn/post/7671508846049607722)
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