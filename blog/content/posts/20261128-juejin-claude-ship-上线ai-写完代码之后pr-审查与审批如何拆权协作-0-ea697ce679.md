---
title: "Claude Ship 上线：AI 写完代码之后，PR 审查与审批如何拆权协作"
date: 2026-11-28T09:59:34+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:658f861801b3e0bf31a3496d6d518d81b1ee5a9bb05f77657c4c3438946a1a15"
source_payload_sha256: "sha256:839c3b13ec19265a721831ae07e6f4151df797530ed0f6088301c75c13967a02"
source_published_at: 2026-11-27T20:11:52Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:5f002673694cfcce4ee25653f5ef7253619ee5f67b7399c61a3e8504652a1350"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 39
description: "核心结论 Claude Ship（Beta）用于承接 PR 创建后的审查、修复与审批环节。Anthropic 将流程拆为 Code Review、PR Steward 和 Claude Approvals 三个组件，分别承担检查代码、修复分支和执行审批策略，避免同一个 Agent 同时修改并放行代码。"
external_url: https://juejin.cn/post/7712769384188051506
observation_id: obs_ea697ce67947cea74a3f517aaad53d85b71220b9d06969de2717def43ca2732d
revision_id: rev_c9556951e6a65a546e22997df7cfaed52935e7af29f0a645a9c3fb6c78016f26
event_id: evt_1f037e0de86d307b2cb2e1bb679bf46a1ce73d7ed07d0d5015ddb1b197087e54
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-28T01:58:15.506841Z
last_seen_at: 2026-11-28T01:59:34Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 可夫小子
- **原始来源**: [https://juejin.cn/post/7712769384188051506](https://juejin.cn/post/7712769384188051506)
- **原文发布时间**: Fri, 27 Nov 2026 20:11:52 GMT

## 核心结论

Claude Ship（Beta）用于承接 PR 创建后的审查、修复与审批环节。Anthropic 将流程拆为 Code Review、PR Steward 和 Claude Approvals 三个组件，分别承担检查代码、修复分支和执行审批策略，避免同一个 Agent 同时修改并放行代码。

其中，Code Review 已进入 GA；PR Steward 与 Claude Approvals 仍为 Beta。PR Steward 可以提交修复，但不能批准或合并 PR，最终合入仍受开发者权限、仓库分支保护规则和 GitHub 原有审批要求约束。

来源援引 Anthropic 内部自报数据：6 月至 9 月，Claude Code 团队的 PR 合并量翻倍以上，代码回滚比例下降超过 40%。这是团队内部口径，尚无第三方独立复现报告。

## 能力机制

Code Review 会在 PR 打开后结合整个代码库上下文，从多个视角检查潜在逻辑漏洞和边界问题，并通过对抗式验证过滤误报。检查结果按严重程度写入行内评论，仓库可选择 Quick、Standard 或 Deep 三档深度。

PR Steward 会在 CI 失败、出现合并冲突，或收到审查工具及同事的修改意见时介入。它能够修改代码、推送新 Commit，并说明修改内容及回滚方式。开发者可在评论中要求它继续调整或停止，但不能授予其批准、合并权限。

Claude Approvals 会读取默认分支中的审批策略文件，作用类似增强版的 `CODEOWNERS`。策略可区分常规改动、目录和风险等级：部分变更允许 Claude 自动批准，高风险变更必须由指定人类工程师签字，也可接入自然语言分类器辅助判断。

## 快速开始

个人使用者可在 Claude Code 命令行或桌面端执行：

```bash
/ship
```

该操作会推送本地改动、创建 PR，并继续处理后续审查与 CI 修复。它不会绕过个人权限和仓库分支规则。

PR 创建后，可在评论区使用以下指令：

```text
@claude
@claude stop
```

前者用于指挥 PR Steward 调整，后者用于停止它。

团队管理员需要先按仓库启用 Code Review 和 PR Steward，再在默认分支添加审批策略文件。官方建议 Claude Approvals 初期采用 `observe-only` 模式，观察策略判断稳定后，再将对应检查绑定到分支保护规则的 Required Check。

## 适用边界

Claude Ship 当前面向 Claude Team 和 Enterprise 计划开放，按 Token 消耗计费。PR 数量、仓库体积、审查深度和自动修复轮次都会影响消耗；自然语言分类器及其触发的 Code Review 同样计费，`observe-only` 模式也不例外。管理员可为 Code Review 和 PR Steward 设置月度消费上限。

平台方面目前仅支持 GitHub。GitLab、Bitbucket 和自托管 Git 服务不在支持范围内。启用零数据保留、HIPAA 合规配置或客户托管加密密钥（CMEK）的组织也无法使用 Claude Ship。

即使 Claude Approvals 判断可以放行，只要 GitHub 要求至少一名人类成员审批，合并仍会被阻止。因此，自动审批不是对现有仓库门禁的替代。

工程上可先选择非核心仓库，以 Code Review 配合 `observe-only` 审批策略运行一段时间，并预先设置 Token 上限。该建议来自来源的操作建议，不代表已经验证的收益结论。

## 核验清单

- 确认仓库托管于 GitHub，且组织计划属于 Claude Team 或 Enterprise。
- 检查是否启用了零数据保留、HIPAA 或 CMEK；存在这些配置时不可接入。
- 按仓库启用 Code Review、PR Steward，并确认所选审查深度。
- 在默认分支配置审批策略，先验证常规改动、高风险目录和人工签字条件。
- 在 `observe-only` 模式下检查分类判断、Code Review 评论及 Token 消耗。
- 为 Code Review 和 PR Steward 设置月度消费上限。
- 验证 PR Steward 只能提交修复，不能批准或合并 PR。
- 核对分支保护中的 Required Check 与人类审批要求，确保自动审批不会绕开门禁。
- 对来源中的内部效果数据保留归因：目前属于 Anthropic 自报，尚无独立复现。

## 来源与核验

- [原始文章](https://juejin.cn/post/7712769384188051506)
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