---
title: "从零到一手撸 Agent 系列 — 第 1 篇：一个 Coding Agent 是什么？"
date: 2026-07-18T11:34:31+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:f0950d9b1090e7b2e2bb56681030c236ddef97646a9d9bb47bb3a56152f5869d"
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:15592ca159e4a2b765e95489acda0dc00228ce66f6afb3505212a825e23f4198"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "核心结论 Coding Agent 是一种以对话驱动的 AI 编码工具，能够自主决定读取哪些文件、运行哪些命令、怎么修改代码。与代码补全工具（如 GitHub Copilot）和 AI 编辑器（如 Cursor）不同，Coding Agent 的核心特征是主动调用工具、多轮迭代、最终产出结果，而非仅仅根据上下文续写代…"
external_url: https://juejin.cn/post/7663075794352685083
observation_id: obs_b0628f7a6433afe933cf43b80a563dec7f5d76c623df1a99436e4d00d84297e3
revision_id: rev_5b8d153befb2ccddd85561fd16c7c5cb91dd4f518cf412409232e037b1280ecc
event_id: evt_633a9bab4984fc44208346dcb489d271c6f9ba77c53cc383b8e33afbf8a16a59
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-18T03:34:31Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 我要割麦子
- **原始来源**: [https://juejin.cn/post/7663075794352685083](https://juejin.cn/post/7663075794352685083)
- **原文发布时间**: Fri, 17 Jul 2026 02:40:32 GMT

## 核心结论

Coding Agent 是一种以对话驱动的 AI 编码工具，能够自主决定读取哪些文件、运行哪些命令、怎么修改代码。与代码补全工具（如 GitHub Copilot）和 AI 编辑器（如 Cursor）不同，Coding Agent 的核心特征是主动调用工具、多轮迭代、最终产出结果，而非仅仅根据上下文续写代码。

该项目采用 Go 语言实现名为 coding-agent 的终端 AI 编码助手，计划通过 14 篇文章逐步构建完整功能。本篇为系列第一篇，目标是搭建项目骨架，定义模块边界和目录结构。

## 能力机制

项目整体架构包含多个模块，本篇仅涉及 CLI 层，后续文章逐步填充其余模块。模块职责划分如下：

CLI 模块承担命令行入口和子命令分发职能。本篇定义了三个子命令：once 执行一次性对话后退出；chat 提供交互式 REPL 模式；tui 提供 Bubble Tea 全屏终端界面。

Provider 模块封装 LLM API 调用，支持 OpenAI 和 Anthropic 两个提供商，留待第 2 篇实现。

Agent 核心模块负责主循环、消息管理和 System Prompt，由第 3 篇完成。

工具系统模块提供文件读写、Shell 执行、搜索等 23 个工具，计划在第 4 至 5 篇实现。

权限管线模块实现三级安全检查机制，包括黑名单、确认、目录边界三种检查手段，在第 6 篇登场。

JSON-RPC 模块作为自研 RPC 传输层，可供 LSP 和 MCP 共享。

其他模块涵盖 LSP 客户端、子代理、记忆系统、上下文压缩、TUI、MCP 集成、Skill 与 Hook 等功能，分别在后续文章中实现。

Go 语言选型的考量因素包括：单二进制分发能力使 `go build` 可直接产出可执行文件，用户无需安装 Python 解释器；goroutine 与 channel 的并发模型适合同时处理流式 LLM 响应、后台工具执行、UI 渲染等任务；编译后启动速度快、内存占用低；交叉编译仅需一行命令即可指定目标操作系统和架构。

## 快速开始

项目初始化步骤：

创建项目目录后，使用 `go mod init` 初始化模块。安装依赖包 `github.com/spf13/cobra` 和 `github.com/joho/godotenv`，前者用于 CLI 框架，后者用于加载 .env 文件中的环境变量。

目录结构约定采用 `cmd/` 和 `internal/` 分层。cmd 目录作为入口层，负责加载配置和组装各模块；internal 目录放置所有核心业务逻辑，后续文章逐步填充。cli 子目录包含 main.go（程序入口）、root.go（根命令定义）、once.go、chat.go、tui.go 四个文件，分别对应根命令和三个子命令。

运行和编译命令：

使用 `go build -o coding-agent ./cmd` 编译项目。执行 `./coding-agent once -m "hello world"` 可运行一次性对话模式（当前仅为占位输出）。`./coding-agent --help` 和 `./coding-agent once --help` 分别查看全局和子命令帮助信息。

环境变量配置方面，API Key 通过 .env 文件或系统环境变量提供，需在 .env 文件中设置对应变量名。项目支持通过 `--env` 参数指定 .env 文件路径，若设置为 `-` 则禁用 .env 加载。没有 .env 文件时不会报错，允许仅使用系统环境变量。

## 适用边界

本篇构建的仅为 CLI 骨架，不包含实际的 LLM 调用能力。项目当前状态是一个能编译运行、有三个子命令的占位实现，各子命令目前仅打印日志或提示信息。真正接入 LLM 的功能将在第 2 篇实现 Provider 抽象层时登场。

该方案适用于希望在终端环境中使用 AI 辅助编码的开发者。Go 语言实现使其具备良好的跨平台能力，单二进制分发便于部署。由于采用模块化设计，可以根据需要选择实现的功能模块，无需一次性引入全部功能。

安全机制方面，项目设计了权限管线和三级安全检查，但本篇仅搭建框架，具体检查逻辑在第 6 篇实现。使用时需注意权限配置，尤其是开启自动批准所有权限请求的信任模式时。

## 核验清单

项目结构核验：确认目录包含 cmd/ 目录（含 main.go 和 cli/ 子目录）、internal/ 目录（后续填充）、go.mod 和 go.sum 文件。目录结构应符合 Go 项目惯用的 cmd/internal 分层约定。

依赖可用性核验：确认 cobra 和 godotenv 两个依赖包可正常下载。go mod tidy 应能成功解析依赖且无冲突。

编译通过核验：`go build -o coding-agent ./cmd` 应成功编译，不报语法错误或导入错误。

CLI 基本功能核验：执行 `./coding-agent --help` 应输出根命令帮助信息，显示 once、chat、tui 三个子命令。执行 `./coding-agent once -m "test"` 应正常运行，输出参数确认信息而非报错。

环境变量加载核验：创建 .env 文件设置环境变量后，执行命令应能读取到配置值。不创建 .env 文件时，程序应正常运行而非报错退出。

子命令继承核验：全局 flag（如 `--provider`、`--model`、`--workdir`）在 once、chat、tui 三个子命令中均应可用，通过 `./coding-agent once --help` 可查看继承的 flag 列表。

全局 flag 配置核验：确认可通过 `--provider/-P`、`--model/-M`、`--base-url/-u`、`--workdir/-w`、`--max-turns/-t`、`--trust/-Y` 等参数配置提供商、模型、API 地址、工作目录、最大对话轮数、信任模式等选项。

## 来源与核验

- [原始文章](https://juejin.cn/post/7663075794352685083)
- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。
- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [掘金](/tags/%E6%8E%98%E9%87%91/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/) / [来源转写](/tags/%E6%9D%A5%E6%BA%90%E8%BD%AC%E5%86%99/)

### 相关文章

- [一只猫如何调试Stable Diffusion](/posts/20260213-hacker_news-how-a-cat-debugged-stable-diffusion-2023-8/)
- [AGENTS.md 概览与工具链：提升 AI Coding 仓库上下文理解](/posts/20260222-juejin-agentsmd-%E7%9C%9F%E7%9A%84%E5%AF%B9-ai-coding-%E6%9C%89%E7%94%A8%E5%90%97%E6%88%96%E8%AE%B8%E5%9C%A8%E6%AD%A4%E4%B9%8B%E5%89%8D%E4%BD%A0%E6%B2%A1%E7%94%A8%E5%AF%B9-0/)
- [从ChatGPT到OpenClaw：梳理模型、工程与框架的AI进化脉络](/posts/20260302-juejin-%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E8%BE%9E%E8%81%8C%E4%BB%8Echatgpt%E5%88%B0openclaw%E8%B7%9F%E4%B8%8A%E6%99%BA%E8%83%BD%E6%97%B6%E4%BB%A3%E7%9A%84%E8%BF%9B%E5%8C%96-2/)
- [利用 AI 辅助代码重写实现许可证变更](/posts/20260305-hacker_news-relicensing-with-ai-assisted-rewrite-2/)
- [英伟达工程师探讨行星级智能体推理与光速计算](/posts/20260310-blogs_podcasts-nvidias-ai-engineers-agent-inference-at-planetary--0/)