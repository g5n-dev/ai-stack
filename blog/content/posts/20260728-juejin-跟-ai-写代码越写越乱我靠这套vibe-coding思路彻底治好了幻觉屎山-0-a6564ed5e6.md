---
title: "跟 AI 写代码越写越乱？我靠这套「Vibe Coding」思路彻底治好了幻觉屎山"
date: 2026-07-28T07:33:49+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:5992a12b29f2002be2b01bcd636caee8a785b9d314d5da6265e55141eeae7d35"
source_payload_sha256: "sha256:7e9817fdaaa8b8584f65a3253c8f3d9a60fae2898de25995b5b4bfceb16229d3"
source_published_at: 2026-07-27T15:40:30Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:7a1e9563b679985e43f844ae122dbe9bf0115a098843bf15b85494a6127bf463"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
description: "核心结论 Vibe Coding 是一套与 AI 协作编写代码的方法论，核心理念是：在让 AI 动手之前，先建立完整的规划约束；使用 AI 时优先充当“胶水”角色而非从零构建。具体包括三个关键环节——先规划后写代码、用成熟组件替代手写核心逻辑、建立并迭代个人规范文件。"
external_url: https://juejin.cn/post/7667093548291178496
observation_id: obs_a6564ed5e6f4ff0d5589f30d9beebdac705a6912d102c234e1b2df5b23089bbf
revision_id: rev_37446af1f5aaefe0e2b92dc7585c310caa5daf5c73c404b91ab95878d2a34c6e
event_id: evt_e68039e498e0d577f7f54ad251310e302d4fbfb2a380d4774949f274e704732b
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-07-27T23:32:28.378096Z
last_seen_at: 2026-07-27T23:33:49Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: To\_OC
- **原始来源**: [https://juejin.cn/post/7667093548291178496](https://juejin.cn/post/7667093548291178496)
- **原文发布时间**: Mon, 27 Jul 2026 15:40:30 GMT

## 核心结论

Vibe Coding 是一套与 AI 协作编写代码的方法论，核心理念是：在让 AI 动手之前，先建立完整的规划约束；使用 AI 时优先充当“胶水”角色而非从零构建。具体包括三个关键环节——先规划后写代码、用成熟组件替代手写核心逻辑、建立并迭代个人规范文件。这套方法能够有效降低 AI 生成代码的幻觉风险，减少后期维护成本。

## 能力机制

**规划约束机制**
规划阶段明确技术栈版本、功能边界、模块拆分和数据结构定义。功能边界中明确标注“不做什么”，防止 AI 擅自添加额外功能。数据结构定死后，字段名称在整个项目中保持一致，从源头消除字段名混乱问题。模块拆分在规划阶段完成，约束 AI 按组件粒度输出代码，避免出现面条式代码。

**胶水编程机制**
胶水编程将开发过程类比为拼乐高：成熟开源组件视为工厂生产的零件，经过广泛验证；AI 的角色是编写少量衔接代码将这些零件组合起来。AI 输出的代码量减少，出错概率随之降低。核心逻辑交由社区维护的开源库处理，AI 只负责数据流转和组件适配。即使出现问题，代码量少也便于定位和修复。

**规范迭代机制**
个人规范文件记录技术栈偏好、代码风格和踩过的坑。开新项目时先将规范文件喂给 AI，实现“岗前培训”。每次 AI 完成代码后让其复盘不符合规范之处，将结论更新至规范文件。规范文件持续迭代，AI 对开发者习惯的理解逐步加深，输出质量随之提升。

## 快速开始

**建立个人规范文件**
创建一个 markdown 文件，记录技术栈偏好（如 React + Tailwind）、代码风格要求、禁止的行为模式。每次开新项目前将此文件内容作为上下文输入给 AI。

**单次任务的标准流程**
第一步，发送规划请求，明确技术栈版本、列出功能边界（包含明确的不做事项）、拆分模块结构、定义数据结构。第二步，等待 AI 输出完整规划，确认无误后再进入下一阶段。第三步，分模块请求代码实现，每个模块完成后核对是否符合规划，不符合立即修正。第四步，代码完成后让 AI 复盘并输出优化建议。

**胶水编程请求模板**
给待办列表增加拖拽排序，选用 react-beautiful-dnd 实现，不手写拖拽底层逻辑，只做组件衔接和数据流转，基于现有 TodoList 组件做适配。

## 适用边界

**适合的场景**
日常业务页面开发、演示项目搭建、需要快速迭代的中小型功能、使用主流技术栈的标准组件组合。

**不适合的场景**
完全没有现成方案的核心业务逻辑需要人工编写，复杂自定义交互逻辑如虚拟列表、复杂动画、手写拖拽底层等场景 AI 手写十个有八个存在 bug，此时应选择成熟开源库并让 AI 做胶水衔接。

**效果依赖因素**
技术栈越主流、社区生态越完善，胶水编程效果越好。个人规范文件积累越充分，AI 输出越贴合习惯。功能边界划分越清晰，幻觉概率越低。

## 核验清单

- 规划阶段是否明确标注了“不做什么”
- 数据结构是否明确定义且各字段名称统一
- 模块拆分是否覆盖所有组件并各自独立
- 是否禁止 AI 在规划确认前输出代码
- 胶水编程场景是否优先选用了成熟开源组件
- AI 输出的代码量是否控制在最小必要范围
- 是否每个模块完成后立即核对而非攒到最后
- 个人规范文件是否包含踩过的坑和对应的禁止规则
- 是否定期让 AI 复盘并更新规范文件
- 边界情况如快速拖拽、边缘元素处理是否由开源库保障

## 来源与核验

- [原始文章](https://juejin.cn/post/7667093548291178496)
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