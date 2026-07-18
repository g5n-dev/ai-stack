---
title: "Open Interpreter Rust 版：Harness、ACP 与 Codex 兼容实践"
date: 2026-07-17T23:42:15+08:00
lastmod: 2026-07-18T10:12:00+08:00
draft: false
entry_kind: "curated"
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "curated_sources"
source_completeness: "verified"
source_is_truncated: false
source_author: "冬奇Lab"
source_published_at: 2026-07-17T21:50:00+08:00
fact_checked_at: 2026-07-18
tags: ["Open Interpreter", "AI Agent", "Rust", "Codex", "Harness", "ACP", "Kimi K3", "工程实践"]
categories: ["AI 工程", "开发工具"]
scenarios: ["AI/ML项目", "命令行工具", "自动化脚本"]
description: "从 Harness 模型适配、ACP 编辑器接入、Codex SDK 兼容到沙箱权限，给出 Open Interpreter Rust 版的可核验工程解读与落地检查表。"
external_url: https://juejin.cn/post/7663304647513718799
editorial_sources:
  - https://juejin.cn/post/7663304647513718799
  - https://github.com/openinterpreter/openinterpreter
  - https://www.openinterpreter.com/docs/terminal/harness
  - https://www.openinterpreter.com/docs/terminal/acp
  - https://www.openinterpreter.com/docs/terminal/sdk
  - https://www.openinterpreter.com/docs/terminal/sandbox
---

## 转写说明

> 本文基于公开资料转写与事实核验，非原文转载。

选题线索来自冬奇Lab 在掘金发布的 [Open Interpreter 项目介绍](https://juejin.cn/post/7663304647513718799)。AI Stack 以 [官方仓库](https://github.com/openinterpreter/openinterpreter)和官方文档为主要事实源，重新组织了架构、接入路径、安全边界和工程检查项。下文不复制原文段落，也不把项目的产品定位扩写成未经验证的性能结论。

## 30 秒结论

Open Interpreter 的 Rust 版不只是“换一种语言重写 CLI”。它基于 Codex 运行时，把工程重心放在一个更具体的问题上：同一套本地 Agent 运行时，如何针对不同模型的请求协议、工具 schema、系统提示和响应格式做适配。

这层适配被称为 **Harness**。Harness 改变模型“看到什么、怎样调工具、返回内容怎样被解析”，但工具执行、沙箱、权限、会话与审批仍由 Open Interpreter 的本地运行时负责。因此，选型时不能只问“支持哪些模型”，还要核对三件事：

- provider 实际暴露的 wire API 是 `responses`、`chat` 还是 `messages`；
- 选中的 Harness 是否支持该传输协议；
- Agent 获得了哪些文件、命令、网络和图形界面权限。

## 项目快照：哪些是可核验事实

截至 2026-07-18，官方仓库显示项目主体为 Rust，使用 Apache-2.0 许可证，并已累计约 6.6 万个 Star。官方 README 还明确说明：新 Rust 版基于 Codex；原 Python 版由 [`endolith/open-interpreter`](https://github.com/endolith/open-interpreter) 以社区分支方式继续维护。

版本号、Star 数和内置 Harness 都会快速变化。原始介绍中的版本快照在本次核验时已经更新，因此上线时应使用 [Releases 页](https://github.com/openinterpreter/openinterpreter/releases) 而不是二次文章中的固定数字做版本判断。

| 维度 | 当前可确认内容 | 工程含义 |
| --- | --- | --- |
| 运行时 | Rust 版基于 Codex | 可复用 Codex 协议面和工具执行模型 |
| 模型适配 | 多种 Harness 可切换 | 模型适配不再只是替换 API 地址 |
| 编辑器接入 | 支持 ACP | 编辑器作为客户端，Agent 以标准进程协议工作 |
| SDK 接入 | 兼容 Codex exec/app-server 协议 | 既有 Codex SDK 可通过替换执行文件接入 |
| UI 测试 | QA skill 结合 `agent-browser` 与 `trycua` | 涉及浏览器或桌面操作时，权限面会显著扩大 |

## Harness 到底改变什么

根据 [Harness 官方文档](https://www.openinterpreter.com/docs/terminal/harness)，Harness 会调整四类模型侧行为：

1. **提示结构**：系统指令、项目上下文和任务约束如何组装。
2. **工具定义**：读文件、执行 shell、编辑、搜索、待办项和子 Agent 等工具以何种 schema 暴露给模型。
3. **消息转换**：本地会话记录如何映射到 Responses、Chat Completions 或 Messages 请求。
4. **响应处理**：思考内容、工具调用、错误和上下文压缩如何被解析回统一运行时。

这也解释了为什么“模型 API 兼容 OpenAI”不等于“Agent 效果必然相同”。底层语言模型可能相同，但如果系统提示、工具名称、参数格式和错误恢复方式不同，整个 Agent 轨迹也会不同。但这是架构上的因果链，不是对任何模型性能提升幅度的保证。

### Harness 与传输协议不能乱配

官方文档将 provider 传输分为 `responses`、`chat` 和 `messages` 三类。例如，`kimi-code`、`qwen-code`、`deepseek-tui` 和 `minimal` 属于 chat 路由；`zcode` 使用 Messages 路由；`claude-code` 和 `claude-code-bare` 可根据 provider 覆盖多种传输面。

官方还提供了自动默认映射：Kimi/Moonshot 倾向 `kimi-code`，Qwen 倾向 `qwen-code`，Anthropic/Claude 倾向 `claude-code`。需要注意，“存在 `deepseek-tui` Harness”与“DeepSeek 默认一定使用它”是两个命题；当前文档中 DeepSeek 的自动默认为 `claude-code-bare`，显式配置则始终优先。

## 三种接入路径

### 1. 终端交互：先验证 Harness 与权限

官方安装方式为：

```bash
# macOS / Linux
curl -fsSL https://www.openinterpreter.com/install | sh

# 安装后启动
interpreter
```

进入 TUI 后可以用 `/model` 切换模型，用 `/harness` 查看或切换 Harness。首次试运行不建议直接放开文件写入和网络访问，应先在一个临时仓库中检查三个环节：模型能否正确调用工具、工具输出能否回到会话、危险操作是否触发审批。

如需一次性固定 Harness，官方文档给出了类似下面的调用方式：

```bash
interpreter -c harness='"kimi-code"' "review this repository"
```

这里只固定了 Harness，并没有声称任何 provider 密钥已被配置。密钥应通过 provider 文档指定的环境变量或本地密钥管理器注入，不要写进仓库、截图或文章示例。

### 2. ACP：让编辑器管 UI，Agent 管运行时

[ACP 文档](https://www.openinterpreter.com/docs/terminal/acp) 将边界划分得很清楚：编辑器或其他客户端启动 Open Interpreter 进程，通过标准输入输出创建会话、发送提示、接收流式消息、显示工具进度并处理权限请求。启动命令是：

```bash
interpreter acp
```

ACP 不是“再包一层终端爬屏”。客户端负责 UI，Open Interpreter 负责 provider、模型、工具、审批、沙箱和会话状态。这使得工具进度和审批可以以结构化事件展示，比解析终端 ANSI 输出更适合 IDE 集成。

### 3. Codex SDK：保留上层集成，替换启动进程

[SDK 文档](https://www.openinterpreter.com/docs/terminal/sdk) 说明 Open Interpreter 并不另造一套完全独立的 SDK，而是兼容 Codex 的 exec/app-server 协议。TypeScript 集成的核心变化是将启动的二进制指向 `interpreter`：

```ts
import { Codex } from "@openai/codex-sdk";

const codex = new Codex({
  codexPathOverride: "interpreter",
  config: {
    model_provider: "moonshotai",
    harness: "kimi-code",
  },
});
```

这种方式适合已经处理好线程生命周期、流式事件和审批回调的 Codex SDK 项目。如果 CI 只需要运行一个任务并取得最终结果，官方更建议使用 `interpreter exec`，不必为一次性工作引入长会话 SDK。

## Computer Use 与安全边界

Open Interpreter 的 QA skill 可通过 `agent-browser` 操作真实浏览器，也可通过 `trycua` 操作原生界面。这对端到端验证很有价值，但它也会把风险从“修改代码”扩展到“点击真实按钮、输入内容和触发外部状态”。

应将 [Sandbox & Approvals](https://www.openinterpreter.com/docs/terminal/sandbox) 视为运行时的核心配置，而不是上线前的最后一个开关。一个可操作的最小原则集如下：

- 日常分析使用只读沙箱，只在任务明确需要写入时扩权。
- 将仓库目录与用户主目录、SSH 目录、云凭证目录分离。
- 网络访问、安装依赖、启动浏览器和修改外部系统需要单独审批。
- 在自动化环境中保留任务输入、工具调用、审批和文件 diff，便于回溯。
- 任何可能提交代码、发布包、发送消息或修改线上数据的动作，都不能由“任务要求完成”自动推导出授权。

还有一个容易被忽略的边界：官方 README 确认配置和会话状态保存在 `~/.openinterpreter`，但这不等于“数据必然不离开本机”。如果 provider 是 Kimi、Anthropic、OpenAI 或其他托管服务，提示、上下文和工具结果仍可能发送给该服务商。只有当模型推理端也本地化，并且网络策略实际阻止外发时，才能对更强的本地数据边界做出承诺。

## 工程落地检查表

### 第一阶段：做协议冒烟测试

- 固定 Open Interpreter 版本，记录 provider、model、wire API 和 Harness。
- 让 Agent 执行一次只读仓库审查，检查文件读取、搜索、命令输出和最终答复。
- 主动制造一次工具失败，观察 Harness 是否能正确返回错误并继续对话。
- 检查模型是否会在不需要时反复调用工具，以及长上下文是否超出预期成本。

### 第二阶段：测试权限和恢复

- 验证文件写入、删除、网络请求和 UI 操作的审批点。
- 中断任务后恢复会话，检查未完成的工具调用会不会被重复执行。
- 在工作区外放置哨兵文件，确认 Agent 无法读写越界路径。
- 对输出做秘密扫描，确保日志、补丁和终端回显不包含凭证。

### 第三阶段：再谈性能

只有在任务成功条件和安全边界稳定后，性能对比才有意义。建议至少记录：成功率、平均工具调用次数、重试次数、人工审批次数、总 token 和总耗时。比较 Harness 时应保持模型、仓库快照、权限与任务集合一致，否则无法将差异归因到 Harness。

## 适用与不适用场景

**更适合：**

- 需要在同一个 Agent 运行时中评估 Kimi、Qwen、DeepSeek、Claude 等多个 provider。
- 已有 Codex SDK 或 ACP 客户端，希望替换底层 Agent 进程而不重写上层 UI。
- 需要统一管理 shell、文件、MCP、skills、hooks、子 Agent 和审批的工程团队。
- 希望把浏览器或桌面 QA 与代码修改放在同一条可审计轨迹中。

**需要谨慎或暂不适合：**

- 合规要求禁止任何上下文外发，但又计划使用托管模型。
- 团队尚未建立命令审批、工作区隔离、凭证注入和操作日志策略。
- 任务需要严格可重放，但外部系统的写入操作没有幂等键和补偿流程。
- 只需要单次文本问答，并不需要工具、会话或审批；这时候完整 Agent 运行时可能是不必要的复杂度。

## 事实核验与动态信息

本次转写对几个容易被放大的表述做了降级处理：

- “Harness 会让某模型接近顶级闭源模型”不是一个无条件成立的事实；它需要明确的任务集、基线、版本和测量数据。
- “Rust 重写是因为 Python 性能不足”不应当作官方已证实的单一原因；可确认的是当前官方主推基于 Codex 的 Rust 版。
- “完全本地、数据不出机”必须取决于模型 provider 和网络策略，不能从本地 CLI 和本地会话目录直接推导。
- 不同 Agent 产品的优劣需要在相同任务、模型、权限和成本预算下测量，不使用“只能”或“一定更强”等非对称表述。

## 参考资料

- [原始选题线索：每日一个开源项目（第 161 篇）](https://juejin.cn/post/7663304647513718799)
- [Open Interpreter 官方仓库](https://github.com/openinterpreter/openinterpreter)
- [Harness 官方文档](https://www.openinterpreter.com/docs/terminal/harness)
- [Agent Client Protocol 接入文档](https://www.openinterpreter.com/docs/terminal/acp)
- [Codex SDK 兼容文档](https://www.openinterpreter.com/docs/terminal/sdk)
- [Sandbox & Approvals 文档](https://www.openinterpreter.com/docs/terminal/sandbox)

> 核验日期：2026-07-18。版本、模型默认值与仓库统计属于动态信息，使用前请重新查阅官方资料。
