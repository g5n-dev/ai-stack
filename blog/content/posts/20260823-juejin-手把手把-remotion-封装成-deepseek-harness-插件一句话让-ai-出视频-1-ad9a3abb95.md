---
title: "手把手：把 Remotion 封装成 DeepSeek Harness 插件，一句话让 AI 出视频"
date: 2026-08-23T01:39:05+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:03ca0cde0e81f2e2b637613094dd8de2631b1375787b9e68b10d3e837cae00fb"
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
description: "核心结论 Remotion 作为 React 视频渲染框架，提供了命令行渲染能力；DeepSeek Harness 基于 Cordis 框架，支持插件机制。两者的对接通过编写 Harness 插件实现：插件注册 工具，工具内部通过 调用 Remotion CLI 完成渲染，最终输出 MP4 文件到本地。"
external_url: https://juejin.cn/post/7676446740678459430
observation_id: obs_ad9a3abb95ccd80f8e05228cd4298a93d10920353d00cf5c7a45080be3bce256
revision_id: rev_ae6fe899ee564f4f91d19f39beda254bc88caf269bf973f5c433efe121509219
event_id: evt_2f48b24f46e6f54994ae768f718247d97dccae2084ee690d07a1573ce57aa0e6
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-22T17:35:35.060887Z
last_seen_at: 2026-08-22T17:39:05Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 小虎AI生活
- **原始来源**: [https://juejin.cn/post/7676446740678459430](https://juejin.cn/post/7676446740678459430)
- **原文发布时间**: Sat, 22 Aug 2026 14:13:00 GMT

## 核心结论

Remotion 作为 React 视频渲染框架，提供了命令行渲染能力；DeepSeek Harness 基于 Cordis 框架，支持插件机制。两者的对接通过编写 Harness 插件实现：插件注册 `render_video` 工具，工具内部通过 `execSync` 调用 Remotion CLI 完成渲染，最终输出 MP4 文件到本地。

## 能力机制

DeepSeek Harness 的定位是模型执行层，核心特性是“一切皆插件”。插件通过 `defineTool` 定义工具接口，工具注册后 AI 可在对话中调用。Remotion 的定位是 React 视频渲染框架，其渲染原理是将每一帧作为 React 组件处理，支持通过命令行执行渲染任务。

两者对接的完整链路为：编写插件文件 → 注册 `render_video` 工具 → 用户对话触发工具 → 插件内部执行 `execSync` 调用 `npx remotion render` 命令 → MP4 文件输出到本地目录。插件打包后可通过 `dsh plugin` 命令发布安装。

Remotion 官方提供了面向独立开发者的组件库，可通过一条命令引入现成的标题动画、转场、背景等效果，无需从零编写。

## 快速开始

### 环境准备

启动 Harness 工作台：

```bash
npx @deepseek-ai/dsh web
```

创建 Remotion 项目：

```bash
npx create-video@latest --yes --blank my-video
cd my-video
npm i
```

### 插件开发

插件文件 `dsh-remotion.ts` 需使用具名导出 `export const name`，通过 `ctx.tools.register` 注册 `render_video` 工具，工具参数包括 title、caption、projectDir。插件内部将参数序列化后传递给 Remotion，执行渲染命令并返回输出路径。

### 配置挂载

创建 `cordis.yml` 挂载插件：

```yaml
- insert:
  - id: dsh-remotion
    name: '/绝对路径/你的目录/dsh-remotion.ts'
```

带补丁启动 Harness：

```bash
pnpm dsh web --patch ./cordis.yml
```

## 适用边界

Harness 仍处于预发布阶段，接口可能发生变化，当前不适合直接用于生产环境。Remotion 渲染过程对 CPU 和内存资源消耗较高，硬件条件有限的设备需要谨慎使用；如需批量处理视频，建议采用 Remotion 官方提供的 Lambda 方案。

插件机制意味着可执行代码直接运行于本机，仅应安装来源可信或社区高评价的插件。开发插件需要具备 TypeScript 和 React 基础知识。

Remotion 在 Windows 环境下存在兼容性问题：PowerShell 会预解析 `${Date.now()}` 这类模板语法，可通过改用 PowerShell 语法或固定输出路径解决。

## 核验清单

开发过程中需注意以下关键点：

插件导出必须使用具名导出 `export const name`，若使用 `export default` 会导致注入声明被静默丢弃，插件看似加载实则无法工作。

对象类型输出必须设置 `additionalProperties: false`，否则工具注册时会直接报错。

`inject: ['tools']` 用于声明依赖顺序，确保等工具注册表就绪后再执行注册逻辑。

`cordis.yml` 中的插件路径必须使用绝对路径，Cordis 框架不识别相对路径。

Remotion 渲染依赖无头浏览器下载，国内网络环境下可能不稳定，建议准备代理或多次重试。

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