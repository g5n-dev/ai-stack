---
title: "从BFF到SSE：我在Vue项目里藏了个“AI翻译官”"
date: 2026-07-19T01:17:21+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:67881b8e474e6a3ab3396e1dc08af51aad3674662370cb2fcb6d1fc7fd523393"
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:ce3d386283191e57dd44489c28796ef87025bd59bb7d0a002032e30975924e11"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 27
description: "核心结论 BFF（Backend For Frontend）作为前端与LLM之间的中间层，能够将API Key隔离在服务端，并承担流式数据的转发与格式化工作。前端只需发起普通fetch请求，即可获得处理好的流式文本，无需关注二进制流解码、SSE格式解析等底层细节。"
external_url: https://juejin.cn/post/7663405360652795947
observation_id: obs_9ec70466e813e1967719ed911fa8875b610e20ba937c7b48942a665b519fd37c
revision_id: rev_78aab8dc6c08dc537edb8123370ebf72ca8353b5537a1c8bc94178d9c5e8d85b
event_id: evt_1190dc97ecaadfedb14823022984a875054fbf8b0d97d0b0172162181482ec25
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-18T17:17:21Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 小林ixn
- **原始来源**: [https://juejin.cn/post/7663405360652795947](https://juejin.cn/post/7663405360652795947)
- **原文发布时间**: Sat, 18 Jul 2026 12:40:05 GMT

## 核心结论

BFF（Backend For Frontend）作为前端与LLM之间的中间层，能够将API Key隔离在服务端，并承担流式数据的转发与格式化工作。前端只需发起普通fetch请求，即可获得处理好的流式文本，无需关注二进制流解码、SSE格式解析等底层细节。该方案将复杂性保留在服务端，从而简化前端代码、提升可维护性。

## 能力机制

BFF层位于前端与后端服务之间，架构表现为前端至Node运行时再至后端或LLM的链路。BFF由前端团队维护，按需提供适配的数据格式，而非依赖通用后端接口。

流式输出场景中存在几个前端痛点：二进制流对象需要解码、SSE格式需要解析为可读文本、错误处理逻辑复杂、连接状态管理繁琐。将这些逻辑集中到BFF后，前端仅需处理最终文本的渲染。

服务端通过环境变量文件存储API Key，运行时由dotenv模块加载，确保密钥不暴露于前端代码。流式请求通过设置stream参数为true实现，响应体为ReadableStream对象，需逐块读取并透传给前端。

Vite开发服务器内置HTTP代理功能，配置规则后将匹配路径的请求转发至目标服务器。由于代理发生在服务端之间，不受浏览器同源策略限制，前端请求同源地址即可触发转发。

## 快速开始

项目初始化使用Vite创建Vue项目后，在根目录创建server.mjs作为BFF服务。

BFF服务依赖express和dotenv。服务监听独立端口（如3000），与前端开发服务器（默认5173）分离运行。

环境变量存储在.env或.env.local文件中，通过dotenv.config()加载。API Key写入环境变量名称（如VITE_DEEPSEEK_API_KEY），代码中通过process.env读取。

BFF核心路由接收prompt参数构造请求，携带Authorization头向LLM发送流式请求。响应流通过ReadableStream处理。

Vite代理配置位于vite.config.js的server.proxy字段。匹配规则target指向BFF服务地址，changeOrigin选项确保目标服务器正确识别请求来源。

启动方式为终端分别运行node server.mjs和npm run dev。

生产环境中Nginx配置反向代理时，需设置proxy_buffering off以保证流式数据的实时透传。

## 适用边界

BFF适用于需要对接多个第三方API、需要处理SSE或WebSocket等特殊协议、需要隐藏API Key等敏感信息、前端需要定制化数据格式的场景。

该方案增加了部署成本与维护复杂度，若项目仅为简单Demo或无需对接外部服务，直接调用API可能更为合适。

## 核验清单

环境变量文件已创建且包含API Key的环境变量名称。

BFF服务能够正常启动，健康检查路由返回预期响应。

Vite代理配置已生效，前端请求/api前缀的路径可正确转发至BFF。

流式路由已完整实现，包括参数解析、请求构造、流数据透传、错误捕获与响应。

生产环境Nginx配置已设置proxy_buffering off。

前端代码中无硬编码的密钥值，所有敏感信息通过环境变量读取。

## 来源与核验

- [原始文章](https://juejin.cn/post/7663405360652795947)
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
- [AI 视觉连载3：RGB与通道](/posts/20260211-juejin-ai-%E8%A7%86%E8%A7%89%E8%BF%9E%E8%BD%BD3rgb%E4%B8%8E%E9%80%9A%E9%81%93-0/)