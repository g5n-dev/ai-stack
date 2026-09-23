---
title: "AgentKit MCP 网关上手指南｜让企业存量服务快速接入 AI"
date: 2026-09-24T04:23:48+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:db1b9c097e6a5e33ccf5686d32966ed1f6373bb6344835bb955ce3c1e9534b82"
source_payload_sha256: "sha256:0eb52fa9a20f307b04cde5e86e85e99ed34947a5772d67e6c61db26b2f7db2ea"
source_published_at: 2026-09-23T16:00:02Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:28c0dfa2dc29e5cfc8283d13709c253ecdd5d79a3d52e5ec019f7848ff47d43f"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 34
description: "核心结论 AgentKit MCP 网关提供 HTTP 转 MCP 和导入已有 MCP 服务两种接入方式，支持将存量系统 API 零改造转为标准 MCP 服务，并通过 MCP 工具集实现多服务编排与语义检索调用。"
external_url: https://juejin.cn/post/7688621328560799794
observation_id: obs_4ae01b3b55d7fa9390738ce3c1479a06763f94a029ce92466f36b892cf740deb
revision_id: rev_69c2aadc0b7f754fa5d087c3f247011276ad91f946854a8bb14180af90d7a90e
event_id: evt_131e69ec1737c6ede02b63a392edb42238e82b471a1759d1bc50652793fef352
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-23T20:21:17.694262Z
last_seen_at: 2026-09-23T20:23:48Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 火山引擎Agent社区
- **原始来源**: [https://juejin.cn/post/7688621328560799794](https://juejin.cn/post/7688621328560799794)
- **原文发布时间**: Wed, 23 Sep 2026 16:00:02 GMT

## 核心结论

AgentKit MCP 网关提供 HTTP 转 MCP 和导入已有 MCP 服务两种接入方式，支持将存量系统 API 零改造转为标准 MCP 服务，并通过 MCP 工具集实现多服务编排与语义检索调用。

## 能力机制

AgentKit 是火山引擎面向企业提供的 AI Agent 基础设施平台，涵盖运行时、身份权限、工具、记忆、知识和观测等能力模块。

MCP 网关作为其中核心组件，具备以下接入方式：

HTTP 转 MCP：将存量系统 API 转换为标准 MCP 服务，支持上传 Swagger 或 OpenAPI Schema JSON 文件完成自动转换。存量 API 文件可借助 AI 工具进行格式转化。

导入 MCP 服务：支持纳管已有的 MCP 服务，可通过固定域名、容器服务、云服务器、函数服务等方式接入。来源中以 GitHub MCP 为例演示了导入流程。

部署 MCP 服务：支持部署自研或公开的 MCP 服务，同时可将 Local MCP 转换为 Remote MCP。

MCP 工具集支持将多个 MCP 服务进行编排组合，提供三种调用模式：全量返回直接输出所有工具；语义检索基于工具描述与调用意图进行语义匹配；标签检索通过工具标签进行精准筛选。

认证方面支持 API Key 和 OAuth JWT 两种入站身份认证方式。

## 快速开始

**前期准备**

在 AgentKit 控制台开通服务；准备存量系统的 OpenAPI Schema JSON 文件和后端服务域名；导入场景需准备目标 MCP 服务的域名和 API Key。

**HTTP 转 MCP 操作流程**

在 AgentKit 控制台进入【网关 - MCP】页面，点击【创建 MCP】服务，选择共享网关或专属网关（生产环境需提前创建专属网关实例）。基本信息配置选择接入方式为“HTTP 转 MCP”，上传 OpenAPI Schema JSON 文件。认证信息配置选择 API Key 或 OAuth JWT 方式。OAuth 方式需提前创建用户池和客户端。配置存量服务的后端域名，支持函数服务、云服务器、固定域名等类型。完成后获取调用代码进行验证。

**导入已有 MCP 服务流程**

创建 MCP 服务时选择“导入 MCP 服务”，访问路径填“/mcp”。后端配置选择固定域名并输入目标服务地址。出站凭据配置选择 API Key 认证方式，设置参数位置为 Header、参数名称为 Authorization、Prefix 为 Bearer。创建完成后获取调用代码。

**创建 MCP 工具集**

在【网关 - MCP - MCP 工具集】点击【创建 MCP 工具集】，选择共享模式。在工具管理中配置调用模式，可选择全量返回、语义检索或标签检索。从已创建的 MCP 服务中选择需要纳入工具集的工具，确认后完成创建。通过【调用示例】可将工具集配置到 Trae 等工具中使用。工具集支持在线调试功能，可在控制台验证语义检索效果。

## 适用边界

共享网关适用于 POC 或低流量验证场景，专属网关适用于生产环境并需提前创建网关实例。

首次选择共享网关模式创建 MCP 服务时，系统会自动下单共享网关。

工具集语义检索模式下，实际效果受大模型能力、网络状况等因素影响可能存在波动，需以实际运行结果为准。

该方案适用于存量系统数量较多、接口改造成本高的企业场景，可快速实现存量能力的标准化接入与统一纳管。

## 核验清单

服务开通：确认 AgentKit 服务已开通并可访问控制台

接入方式：根据存量系统情况选择 HTTP 转 MCP 或导入已有 MCP 服务

文件准备：HTTP 转 MCP 场景需准备符合规范的 OpenAPI Schema JSON 文件

认证配置：确认入站认证方式（API Key 或 OAuth JWT），OAuth 场景需提前完成用户池和客户端创建

后端配置：确认存量服务域名或目标 MCP 服务地址可正常访问

工具集编排：根据业务需求选择合适的调用模式（建议生产环境评估语义检索模式）

调用验证：使用控制台提供的监控和调试功能验证服务可用性

配置同步：按调用示例将服务配置到实际使用的 Agent 工具中

## 来源与核验

- [原始文章](https://juejin.cn/post/7688621328560799794)
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