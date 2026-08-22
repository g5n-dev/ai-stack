---
title: "手把手：把 Remotion 封装成 DeepSeek Harness 插件，一句话让 AI 出视频"
date: 2026-08-23T03:39:16+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:41b00a0fd763d41b179285415a3c5b878f43ef64f9a4903187d6da180b45edeb"
source_payload_sha256: "sha256:caaa3246812f857d1fe23ea326676089e03cc0ed16f6df8ec9e6d336d303739f"
source_published_at: 2026-08-22T14:13:00Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:5952c8ded0b40f0ba323cfdc19a4cd47b6614c6287d94326fc9c3927f73afc33"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 50
description: "核心结论 DeepSeek Harness 通过插件机制扩展工具能力，可将 Remotion 视频渲染框架封装为 工具。封装后的插件允许 AI 在对话中接收标题和文案参数，自动调用 Remotion 命令行完成 MP4 视频生成。"
external_url: https://juejin.cn/post/7676446740678459430
observation_id: obs_ad9a3abb95ccd80f8e05228cd4298a93d10920353d00cf5c7a45080be3bce256
revision_id: rev_ae6fe899ee564f4f91d19f39beda254bc88caf269bf973f5c433efe121509219
event_id: evt_2f48b24f46e6f54994ae768f718247d97dccae2084ee690d07a1573ce57aa0e6
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-22T19:34:35.146432Z
last_seen_at: 2026-08-22T19:39:16Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 小虎AI生活
- **原始来源**: [https://juejin.cn/post/7676446740678459430](https://juejin.cn/post/7676446740678459430)
- **原文发布时间**: Sat, 22 Aug 2026 14:13:00 GMT

## 核心结论

DeepSeek Harness 通过插件机制扩展工具能力，可将 Remotion 视频渲染框架封装为 `render_video` 工具。封装后的插件允许 AI 在对话中接收标题和文案参数，自动调用 Remotion 命令行完成 MP4 视频生成。核心链路为：Harness 插件注册 `render_video` 工具 → 工具内部通过 `execSync` 执行 Remotion CLI → 输出视频文件到指定目录。该方案基于 DeepSeek Harness 的 Cordis 框架实现，目前处于 0.1.0 预发布阶段。

## 能力机制

Harness 采用插件化架构，所有扩展功能以插件形式加载。插件需导出 `name` 变量并在 `apply` 函数中注册工具。Remotion 封装插件通过 `defineTool` 定义 `render_video` 工具，接收三个必填参数：视频标题、文案内容、Remotion 项目绝对路径。工具执行时将参数序列化为 JSON，通过 `--props` 传递给 Remotion CLI，最终输出 MP4 文件。

插件与主系统的对接依赖 Cordis 配置系统。需要在项目根目录创建 `cordis.yml` 文件，通过 `insert` 指令挂载插件路径。插件加载顺序由 `inject` 数组控制，`inject: ['tools']` 确保工具注册表就绪后再执行插件逻辑。输出 schema 必须声明 `additionalProperties: false`，否则注册失败。

## 快速开始

环境准备需完成两步：启动 Harness 工作台，执行 `npx @deepseek-ai/dsh web` 后访问本地端口；创建 Remotion 项目，执行 `npx create-video@latest --yes --blank my-video` 并进入目录安装依赖。Remotion 渲染依赖无头浏览器，国内网络环境下可能需要多次尝试或配置代理。

插件代码保存在项目根目录，文件命名如 `dsh-remotion.ts`，导出 `name` 和 `apply` 函数。插件注册后需在 `cordis.yml` 中配置绝对路径，挂载命令为 `pnpm dsh web --patch ./cordis.yml`。对话中可直接通过自然语言触发视频生成，例如描述标题和文案内容。

视频质量提升可通过引入 Remocn 组件库实现，该库提供标题动画、转场、背景等预置组件，安装命令为 `npx shadcn@latest add @remocn/blur-reveal`。插件打包发布需在 `package.json` 中声明插件配置，通过 `dsh plugin --profile web add github:仓库地址` 完成安装。

## 适用边界

版本层面，Harness 0.1.0 为预发布版本，接口稳定性无法保证，不建议直接用于生产环境。性能层面，Remotion 渲染属于 CPU 和内存密集型操作，老旧硬件上需谨慎使用；大规模批量渲染建议使用 Remotion 官方 Lambda 方案。

安全层面，插件在本机以可执行代码形式运行，应仅安装官方或高星级的插件来源。技术门槛层面，该方案需要 TypeScript 和 React 基础知识，相比传统视频编辑软件学习曲线较低。Windows 环境下存在路径解析差异，PowerShell 会预解析 `${Date.now()}` 语法，建议改用 PowerShell 原生命令或固定输出路径规避。

## 核验清单

插件开发需确认以下要点：代码中必须使用具名导出 `export const name`，而非默认导出；输出 schema 的对象类型必须包含 `additionalProperties: false` 约束；`inject` 数组需正确声明依赖顺序；`cordis.yml` 中插件路径必须为绝对路径；Remotion 项目目录必须预先初始化并包含 `src/index.ts` 入口文件。

功能触发前需验证：Harness 工作台正常启动并监听本地端口；Remotion CLI 可通过 `npx remotion` 命令正常调用；项目目录结构符合 Remotion 规范且包含视频组件定义。网络环境需支持无头浏览器下载，否则渲染过程可能中断。

## 来源与核验

- [原始文章](https://juejin.cn/post/7676446740678459430)
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