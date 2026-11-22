---
title: "workbuddy可以操控电脑！真的太省心了，AI博主利器啊"
date: 2026-11-23T03:37:34+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:15f267b271e0d864af82789c85a836643d8ca1ec74e6e8da6e0c2d3abe099d35"
source_payload_sha256: "sha256:506f3602ebc793bed61f68b89ca0ca6cf5384cf254dd832ba051e48693ad8936"
source_published_at: 2026-11-22T14:26:01Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:2dda47e33063c256645422cdf3a6e4a55e501b110e9aa14a1003d72705cd3db1"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 30
description: "核心结论 WorkBuddy 的「电脑操控」可在独立虚拟桌面中执行鼠标、键盘等 GUI 操作。来源实测覆盖了浏览器、画图和文件管理器三类任务，场景包括处理弹窗并访问网址、按描述修正未闭合图形、归整素材。 首次启用后，系统能够创建独立桌面，但 WorkBuddy 执行任务时提示 操作被拒绝。"
external_url: https://juejin.cn/post/7710647322555760691
observation_id: obs_935896c5be364d7f8e106796d5ddcfaec0cf0bffdf6e72c1fcc0577c0bc3925a
revision_id: rev_24bda69ac038d3a57ab883c84982c753228a78622e8c5164f5fcd993a9e16177
event_id: evt_657e5661254f7c9c1491d622a1265e8be7266c9b7a180c6a15616aa93336f609
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-22T19:36:12.861312Z
last_seen_at: 2026-11-22T19:37:34Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 小虎AI生活
- **原始来源**: [https://juejin.cn/post/7710647322555760691](https://juejin.cn/post/7710647322555760691)
- **原文发布时间**: Sun, 22 Nov 2026 14:26:01 GMT

## 核心结论

WorkBuddy 的「电脑操控」可在独立虚拟桌面中执行鼠标、键盘等 GUI 操作。来源实测覆盖了浏览器、画图和文件管理器三类任务，场景包括处理弹窗并访问网址、按描述修正未闭合图形、归整素材。

首次启用后，系统能够创建独立桌面，但 WorkBuddy 执行任务时提示 `schtasks.exe` 操作被拒绝。来源将问题定位到「安全中心 → 命令安全」中的命令白名单：删除其中的 `schtasks.exe` 条目并重启 WorkBuddy 后，独立桌面恢复可操作。

该功能仍受单例架构限制。即使任务运行在独立桌面中，进程也会唤起主桌面的 WorkBuddy 实例，无法在两个桌面分别启动实例并同时执行不同任务。因此，现有实测更接近单个桌面内依次接活，而不是并行分流。

## 能力机制

功能入口位于 WorkBuddy 的「设置 → 智能体 → 电脑操控」，其中包含「电脑应用操控」与「浏览器操控」。首次开启时，界面状态由未启用变为「已安装」。

实际执行时，WorkBuddy 会创建与主桌面并列显示的独立桌面，并在其中打开应用、输入内容和操作界面。来源记录了三组实测：

- 浏览器任务：打开浏览器后处理出现的弹窗，继续输入目标网址并确认访问。
- 画图任务：首次生成的框线没有闭合；用户指出四边需要连通后，WorkBuddy 重新绘制并得到闭合结果。
- 文件管理任务：打开文件管理器，将查到的资料和截图归整到指定位置。

任务执行依赖桌面环境中的 GUI 应用，而不是仅有文字输出。来源未给出任务调度、模型调用、文件隔离或底层控制实现，因此不能据此推断其内部架构或数据流向。

## 快速开始

1. 打开 WorkBuddy，进入右下角头像菜单中的「设置」。
2. 在左侧选择「智能体」，向下找到「电脑操控」。
3. 分别检查「电脑应用操控」和「浏览器操控」，按需启用；来源首次操作后显示为「已安装」。
4. 请求 WorkBuddy 创建独立桌面，确认桌面已经出现。
5. 若执行时报错提示 `schtasks.exe` 操作被拒绝，进入「安全中心 → 命令安全」。
6. 在相关白名单中找到 `schtasks.exe`，删除该条目，然后重启 WorkBuddy。
7. 重启后重新发送 `继续`，可在独立桌面中打开记事本并输入文字，以验证 GUI 控制是否恢复。
8. 验证通过后，再依次测试浏览器、画图和文件管理器操作。

来源同时提醒电脑操控存在风险。这里的操作顺序仅复现已记录路径；删除安全规则前，应由操作者结合自身系统策略决定是否接受相关风险。

## 适用边界

该功能适合能够通过可见界面完成的短流程任务，例如网页操作、简单绘图和素材整理。来源未提供长任务稳定性、复杂应用兼容性、异常恢复速度或执行准确率数据，不能扩展出相关性能结论。

单例限制是当前明确边界。独立桌面只是任务运行位置不同，并不能产生两个可同时工作的 WorkBuddy 实例。即使两边分别运行不同任务，执行时仍会唤起主桌面实例。

图形任务也可能需要人工纠偏。来源中的首次框线未闭合，追加描述后才完成重绘，说明“已打开应用”不等于“结果已经符合要求”，关键输出仍需检查。

命令安全配置是启用后的直接卡点。开关正常、桌面可创建，并不能证明任务可执行；遇到 `schtasks.exe` 拒绝提示时，应检查命令安全规则。来源只记录了删除该白名单条目这一条已验证解法，没有给出其他修复命令。

## 核验清单

- 确认「设置 → 智能体 → 电脑操控」中的两个子项已启用，并显示「已安装」。
- 确认能够创建独立桌面，且主桌面与独立桌面可同时显示。
- 在独立桌面中打开记事本并输入文字，验证不只是能建桌面，而是能执行 GUI 操作。
- 若出现 `schtasks.exe` 操作被拒绝，检查「安全中心 → 命令安全」中的对应白名单条目。
- 删除对应条目后确认已重启 WorkBuddy，再使用 `继续` 复测。
- 浏览器测试需覆盖弹窗处理、网址输入和确认访问三个环节。
- 画图测试需检查线条是否闭合，不能只以应用启动成功作为通过标准。
- 文件管理测试需确认资料和截图是否已按要求归整。
- 多开测试应记录是否仍唤起主桌面实例；在来源所测版本中，这一限制尚未解决。

## 来源与核验

- [原始文章](https://juejin.cn/post/7710647322555760691)
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