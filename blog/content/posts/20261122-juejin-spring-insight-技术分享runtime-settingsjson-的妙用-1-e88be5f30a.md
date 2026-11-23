---
title: "【Spring Insight 技术分享】runtime-settings.json 的妙用"
date: 2026-11-22T19:21:00+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:b55062d6e7bf89648a0cf2552d23dfe208dfe7c87b6a2fd10b386d8b31c33499"
source_payload_sha256: "sha256:2bc489f134f19b1a5385716f5c2bb2caecc0bca3c8196aec7afcc9959ee249c0"
source_published_at: 2026-11-22T09:33:38Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:18d231ee1fb9692f24dc1da4197f34fb6f74a7d88b8448ac9acd504676bd4953"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
description: "核心结论 Spring Insight 将运行时设置从 中拆出，采用“启动默认值 + 本地 JSON 覆盖 + 内存当前值”的方式实现热更新。 和 仍负责从 或环境变量读取启动配置。服务启动时若存在 ，优先加载该文件；文件不存在或读取失败时，才使用启动配置。"
external_url: https://juejin.cn/post/7710449704619147300
observation_id: obs_e88be5f30a6b6da5f023feb2365b6e338c61d3be77f1625d696f31ffa61e41d5
revision_id: rev_8e90dff038bb53c463115ddddf37e92c8006c61e1a1cf1003ef2de38352f104f
event_id: evt_c0ce94a68724af85381fdf65d77f09a2bb6a359abfe97563d1a2c2f8d49d7362
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-23T00:50:37.381819Z
last_seen_at: 2026-11-23T00:00:00Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 苏渡苇
- **原始来源**: [https://juejin.cn/post/7710449704619147300](https://juejin.cn/post/7710449704619147300)
- **原文发布时间**: Sun, 22 Nov 2026 09:33:38 GMT

## 核心结论

Spring Insight 将运行时设置从 `application.yml` 中拆出，采用“启动默认值 + 本地 JSON 覆盖 + 内存当前值”的方式实现热更新。

`InsightServerAlertProperties` 和 `InsightServerAiProperties` 仍负责从 `application.yml` 或环境变量读取启动配置。服务启动时若存在 `runtime-settings.json`，优先加载该文件；文件不存在或读取失败时，才使用启动配置。告警扫描与 AI 解释随后统一读取 `InsightRuntimeSettingsService` 提供的生效配置，因此修改 webhook、SMTP、模型地址或密钥后，相关调用可以获取新值，无需重启 Server。

这里的“本地保存”仅指配置文件存放在本机数据目录，不能据此推断业务数据、Span 或模型请求一定不离开本机。

## 能力机制

运行时配置由 `InsightRuntimeSettingsService`、`InsightRuntimeSettingsStore` 和 `InsightSettingsController` 协同管理。Service 在 `@PostConstruct` 阶段完成初始化：先尝试读取磁盘文件，成功后设置 `AtomicReference`；否则把启动时的 Properties 复制为当前配置。

配置对象通过 `current` 引用发布。更新时先对当前对象执行 `deepCopy`，完成合并后再整体 `set` 一次，避免扫描线程或 HTTP 线程观察到修改到一半的对象。调用方不自行缓存 Properties，而是在每次使用时调用 `effectiveAlert()` 或 `effectiveAi()`。设置页保存完成后，下一次 AI 解释即可读取新的 API Key；告警调度约每 60 秒扫描一轮，并在每轮 `scan()` 开始时重新获取告警配置。

磁盘文件固定名为 `runtime-settings.json`。其目录随存储模式变化：SQLite 模式使用数据库文件父目录，文件模式使用 Span 文件父目录，内存模式使用 `./data`。这样备份同一数据目录时，配置可与链路数据一同迁移。

写入采用临时文件替换：先写同目录的 `runtime-settings.json.tmp`，再通过 `Files.move` 和 `ATOMIC_MOVE` 替换目标文件。来源说明，在同一文件系统内，目标应保持旧文件或完整新文件，避免留下半截 JSON。若文件损坏或加载失败，`loadOrNull` 返回空值，服务退回 YAML 启动配置。

## 快速开始

1. 使用 `spring-insight-agent-starter` 为业务服务接入上报，并运行独立的 `insight-server`。
2. 服务首次启动时，可通过 `application.yml` 或环境变量提供告警与 AI 的初始配置；即使告警配置为 `enabled: false`，Server 也可先启动。
3. 在控制台设置页填写 webhook、SMTP、模型地址及相应凭据。配置保存到 `runtime-settings.json`。
4. 通过 `GET /api/v1/ui/settings` 获取脱敏后的当前设置，通过 `PUT /api/v1/ui/settings` 调用 `updateAndApply` 更新配置。
5. 保存后直接发起下一次 AI 解释验证新配置；告警相关改动则在后续扫描轮次中生效。

设置页再次打开时，密码框和 API Key 输入框不会回显明文，只会展示 `passwordConfigured` 与 `apiKeyConfigured` 状态。webhook URL 和模型名可以正常回显。

## 适用边界

该机制面向单个 `insight-server` 进程中的告警与 AI 两类可修改配置，目标是减少配置中心依赖并支持保存后立即应用。它没有提供多实例之间的配置同步、版本回滚或并发 CAS 重试机制。

配置更新采用 merge 语义。提交内容中的密码或 API Key 为空时，会保留磁盘上的既有值；因此修改阈值、模型名等非敏感字段不会意外清空密钥。普通字段则会按提交内容更新。

来源只确认配置文件位于本地数据目录，未说明本地保存是否影响 AI 推理位置、模型网络请求路径或链路数据存储位置，不能将“配置不出本机”等同于“推理数据不出本机”。

## 核验清单

- 确认 `runtime-settings.json` 位于当前存储模式对应的数据目录。
- 检查文件写入后是否生成完整的 JSON，而非残留 `.tmp` 文件。
- 验证 `GET /api/v1/ui/settings` 仅返回密钥是否已配置的布尔状态。
- 更新其他设置时保持密钥输入为空，确认原密钥没有被覆盖。
- 保存后检查 `current` 是否通过完整副本替换，而非原地修改共享对象。
- 调用 `effectiveAlert()`、`effectiveAi()` 的位置应位于实际使用配置时，不能在业务组件字段中长期缓存旧 Properties。
- 删除或损坏 JSON 后重启，确认服务能够回退到 YAML 或环境变量中的启动配置。
- 区分即时验证与周期生效：AI 解释在下一次调用时读取生效配置，告警配置约在下一轮扫描时重新读取。

## 来源与核验

- [原始文章](https://juejin.cn/post/7710449704619147300)
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