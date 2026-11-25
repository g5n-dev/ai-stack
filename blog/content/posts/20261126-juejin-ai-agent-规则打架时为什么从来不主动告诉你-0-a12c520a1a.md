---
title: "AI Agent 规则打架时，为什么从来不主动告诉你？"
date: 2026-11-26T06:31:51+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:cd178a0b2eac62f620a6858ef35ec0b15da13e5e43998d86f577b5a2c4be1dca"
source_payload_sha256: "sha256:1671d95dce1e3cc08c1d8f991e917239bb86d75c87a6eab48243cb6a9197445c"
source_published_at: 2026-11-25T20:11:14Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:3e7125582c8e7980b8c9d691875a28fdac773ac05e8293a843d8b0575ff45db7"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 27
description: "核心结论 来源文章的核心判断是：Agent 规则失效不一定是上下文过长，而更可能是不同来源的规则已经彼此冲突。实验显示，注入 50,000 tokens 的无关历史并重复一致的规则时，Gemini 3.8 Flash 的规则违反次数为 0；相反，面对直接矛盾的指令，模型虽然多数时候能识别异常，却不会主动告知用户。"
external_url: https://juejin.cn/post/7712014425431293979
observation_id: obs_a12c520a1ab5541202cd24009bf01a4ff6fb7ec91d7ad6fc2055398c1a40f29d
revision_id: rev_de324bf20c00f0b8d420a8312addba3e45e743b22e0367e4ce728b11eb45bd74
event_id: evt_9afd53607e66f22a18837d948ad9ddab98be2b3cce3a08088e3a3b7f4b967aa3
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-25T22:30:14.776059Z
last_seen_at: 2026-11-25T22:31:51Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 可夫小子
- **原始来源**: [https://juejin.cn/post/7712014425431293979](https://juejin.cn/post/7712014425431293979)
- **原文发布时间**: Wed, 25 Nov 2026 20:11:14 GMT

## 核心结论

来源文章的核心判断是：Agent 规则失效不一定是上下文过长，而更可能是不同来源的规则已经彼此冲突。实验显示，注入 50,000 tokens 的无关历史并重复一致的规则时，Gemini 3.8 Flash 的规则违反次数为 0；相反，面对直接矛盾的指令，模型虽然多数时候能识别异常，却不会主动告知用户。

报告将这类跨文件、跨时间形成的上下文不同步称为“上下文漂移”。在 110 次没有额外提示的运行中，模型主动指出矛盾的比例为 0%；在 73% 的运行中，其内部思考摘要已经明确意识到两个来源不一致。也就是说，识别冲突与向用户报告是两回事：模型可能自行选择一个规则继续执行。

来源还提出一项更积极的方案：提供只读 MCP 工具 `report_inconsistency`，把冲突记录为 `conflict`，把过时内容记录为 `stale`。在未额外要求聊天提示的情况下，该工具在 152 次运行中成功记录 150 次，主动记录率为 98.7%。不过，记录上报并不等同于阻断冲突。

## 能力机制

规则优先级是问题的主要触发机制。在 95% 至 100% 的匹配任务中，任务级 skill 文件会覆盖根目录 `AGENTS.md`，即使后者使用严格的 MUST 措辞也未改变结果。因此，只修改全局规则而遗漏任务级文件，容易让 Agent 持续执行旧版本。

过时文档与真实代码不一致时，Agent 也可能通过兼容处理掩盖问题。实验中，某文档引用了代码库中已改名的测试辅助函数；15 次测试里有 9 次，模型没有提示文档过期，而是在新测试文件中增加包装函数，使 `pytest` 继续通过。

当两个同级 skill 文件冲突且没有明确优先级时，模型需要反复权衡，思考 token 增加了 47%。相比之下，加入只读上报工具后，总执行轮次基本未变，思考 token 平均约下降 19%，但来源将其归为正常波动，不能据此认定性能收益。

只读 MCP 工具的价值主要是提供可审计出口，而不是替用户决定冲突规则。重复分类 `duplicate` 会增加额外轮次，因此被移除。工具启用后，模型默认将问题写入后台日志，聊天中的口头提醒概率会降至 0%；若希望两处都出现，还需在规则中同时要求聊天报告和日志记录。

## 快速开始

以下是基于来源事实整理的接入建议：

1. 盘点仓库中的 `AGENTS.md`、任务级 `SKILL.md`、记忆文件、历史规范和团队文档，重点检查退款期限、权限边界、测试入口等可能重复定义的规则。

2. 配置一个只读异常上报工具 `report_inconsistency`，只保留 `conflict` 与 `stale` 两类结果，避免让模型为无害重复内容消耗额外轮次。

3. 在初始提示词中直接列出相关文件的摘要。对于探索步数较少、未主动遍历目录的 Gemini Pro，来源报告指出，文件摘要配合预加载工具比按需搜索更稳定。

4. 如需用户立即看到问题，在 `AGENTS.md` 中要求模型同时在聊天界面报告并写入后台记录。只要求写入工具而没有聊天提示时，模型通常不会口头提醒。

5. 如果采用社区提出的静态检查路线，可在流程中使用来源明确给出的命令：

```bash
npx @reporails/cli check
```

静态检查适合在会话开始前拦截重复和矛盾；MCP 上报适合保留运行期间的异常记录。

## 适用边界

470 项任务、73%、98.7% 等结果均来自 Patrick Kelly 在自定义 Git 沙盒中的自报实验，只覆盖 Gemini 3.8 Flash 和 Gemini Pro，来源未公开完整测试数据集仓库，因而暂不能视为可独立复现的普遍结论。

该机制只能记录已经发现的问题，不能自动判断哪个规则正确，也不能替代权限审批。对于涉及权限或不可逆操作的冲突，来源引用的工程观点认为应触发硬阻断，并保存现场供人工决定，而不是仅写入后台队列。

模型是否能够遍历规则文件也受工具加载方式和探索预算影响。隐藏于按需工具搜索之后、或未在初始上下文中提供文件摘要时，模型可能根本不会发现漂移。此外，上报工具及文件摘要仍会增加首轮上下文信息，其具体开销需要结合项目环境评估。

## 核验清单

- 是否已清点 `AGENTS.md`、skill、记忆文件与历史规范之间的重复和冲突？
- 修改全局规则后，是否同步检查了任务级 `SKILL.md`？
- 规则冲突时，Agent 是执行、兼容处理，还是明确报告？
- `report_inconsistency` 是否仅使用 `conflict` 和 `stale` 两类？
- 是否在初始提示词中提供文件摘要，并让工具保持预加载？
- 是否分别验证了后台日志上报与聊天界面提醒？
- 对权限审批和不可逆操作，是否设置了确定性阻断，而不只是被动记录？
- 接入前后是否分别检查了规则违反率、上报率、轮次与思考 token？
- 使用静态检查时，是否确认命令适用于当前仓库，而不是直接照搬来源示例？
- 对实验结论是否保留了模型、任务集、沙盒环境和可复现性方面的适用范围？

## 来源与核验

- [原始文章](https://juejin.cn/post/7712014425431293979)
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