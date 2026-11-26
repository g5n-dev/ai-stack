---
title: "我写的 12 个 AI Skill，三个月后 8 个在吃空饷"
date: 2026-11-26T23:13:25+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:8e162350fea7c7496ed274f22a6a5e21494a2f328fda96e5605b2bca29f5cffd"
source_payload_sha256: "sha256:5b83b672fff6bf73cf3adfab400f99f565f92ebc9a6ca792450e4875228da9dc"
source_published_at: 2026-11-26T10:57:14Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:ead7c0da8dd000cd19f55b4ec1afe17c5f3b0b1eee8b38e38d18ec1d20e34e80"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 30
description: "核心结论 **来源事实：**作者从 8 月底开始编写了 12 个自定义 Skill，并以“超过 30 天没有改动”作为停用代理指标进行盘点。最终保留缺陷闭环、像素还原、代码纪律、活动页开发 4 个；度量、复盘、发布同步、交付门禁、内网代理、Skill 发版、埋点校验、组件开发 8 个停用。"
external_url: https://juejin.cn/post/7712307777096007720
observation_id: obs_0aeb3b19b69acc8968d8e4fcd4db63a94f08b09a0586b5ef5fad291e4284a417
revision_id: rev_43196efb5628350e28a68e0823602cf0e5baf0629efee41f276009b0d7a14e15
event_id: evt_c080945919a378be0aec86e15812ed77ecddb7e6e3f90532e36c36bda949dfdc
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-26T23:50:36.644087Z
last_seen_at: 2026-11-26T15:13:25Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: kyriewen
- **原始来源**: [https://juejin.cn/post/7712307777096007720](https://juejin.cn/post/7712307777096007720)
- **原文发布时间**: Thu, 26 Nov 2026 10:57:14 GMT

## 核心结论

**来源事实：**作者从 8 月底开始编写了 12 个自定义 Skill，并以“超过 30 天没有改动”作为停用代理指标进行盘点。最终保留缺陷闭环、像素还原、代码纪律、活动页开发 4 个；度量、复盘、发布同步、交付门禁、内网代理、Skill 发版、埋点校验、组件开发 8 个停用。

停用并不等于文件被删除，而是移出常驻触发名单，退回候选池。保留的 4 个 Skill 分别具备明确触发场景、可验收交付物和清楚职责边界。作者由此将 Skill 视为需要持续维护的责任单元，而不只是新增能力。

## 能力机制

**来源事实：**这批 Skill 的使用效果呈现出四类机制。

1. **缺少外部真值，结果难以验证。**度量与复盘类任务缺少明确的验收依据，输出即使频繁生成，也难以判断质量。像素还原则可以直接对照设计稿间距，缺陷闭环可以观察缺陷状态是否完成闭环。
2. **依赖人工记忆，难以稳定触发。**代码纪律挂在编码、修改缺陷等既有动作上，不需要额外提醒；复盘、度量需要主动调用，容易因遗忘而闲置。
3. **维护成本超过复用收益。**发布同步依赖渠道、版本规则和目录结构等外部状态。来源中的粗略测算为修改一次约半小时、使用一次节省约五分钟；若一个月使用不足六次，收益不足以覆盖维护成本。
4. **职责重叠导致入口合并。**埋点校验与缺陷闭环存在包含关系，实际调用集中到覆盖范围更广的缺陷闭环，埋点校验因此失去独立入口。

存活 Skill 的说明书包含三个共同要素：使用用户自然表达描述触发条件；交付物能够被验收；明确声明不负责哪些相邻工作。

**工程建议：**设计 Skill 时，应优先寻找可客观核验的结果、挂接已有工作动作、隔离外部依赖，并检查同类 Skill 是否争夺同一触发入口。

## 快速开始

**来源事实：**新 Skill 先进入候选池试用 30 天，需要同时满足两项条件：

- 30 天内至少真正触发 3 次；
- 曾因实际踩坑而修改 Skill，说明它已经参与工作流。

两项均通过后再进入常用名单并配置触发词。未通过者退回候选池，不立即删除。

常用 Skill 可使用五项问题检查：

1. 出错时能否立即发现对错；
2. 由 Skill 自动进入，还是必须人工想起；
3. 30 天内是否因踩坑而修正；
4. 单次节省时间是否大于单次维护时间；
5. 移除后任务质量是否下降，而不只是速度变慢。

其中任意三项不通过，即停用并移出常用名单。

## 适用边界

**来源事实：**最后改动时间只是代理指标，不能替代使用日志。一个月没有修改的 Skill 仍可能正在运行；该结论依赖作者自身维护习惯和项目上下文。五个 Skill 同日停止更新，也只能说明工作方式或调用入口发生了变化，不能据此断言它们已经失去全部用途。

经济性判断同样依赖实际使用频率、修改成本和质量收益。发布同步的示例账目不能直接外推到其他团队。自定义 Skill 与他人维护的 Skill 也应分开统计：作者本机共安装 64 个 Skill，其中 12 个为自行编写，剩余 60 个由他人维护。

**工程建议：**盘点时应结合触发次数、缺陷修正记录和任务质量变化，不应仅凭提交日期直接删除。涉及本地文件或配置的维护动作，也不能据此推导为推理数据一定不会离开本机；来源只确认相关配置或文件保存在本地。

## 核验清单

**来源事实对应的核验项：**

- 列出全部自定义 Skill，记录职责、最后改动日期和提交次数；
- 判断交付物是否存在客观验收依据；
- 检查触发条件是否对应具体、自然的用户表达；
- 统计 30 天内真实触发次数及踩坑后的修改次数；
- 估算单次维护成本与单次收益；
- 对照其他 Skill 的职责范围，确认是否存在入口竞争；
- 停用时保留文件，仅调整其常用状态。

**工程建议：**每次更新流程、依赖或目录结构后重新检查相关 Skill；在转正前验证自动触发是否有效；连续观察一个完整工作周期，再决定其进入常用名单、候选池还是停用状态。

## 来源与核验

- [原始文章](https://juejin.cn/post/7712307777096007720)
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