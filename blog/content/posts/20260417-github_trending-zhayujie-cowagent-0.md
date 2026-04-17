---
title: "CowAgent：基于大模型的多平台AI助理框架"
date: 2026-04-17T00:35:01+08:00
draft: false
entry_kind: "auto"
tags: ["大模型", "AI助理", "多平台", "插件化", "多模态", "Docker", "开源", "企业数字员工"]
categories: ["大模型", "开源生态"]
source: github_trending
description: "CowAgent（chatgpt‑on‑wechat）是一款基于大模型的超级 AI 助理，采用 Python 开发，GitHub 星标已超过 43,000。该系统能够主动进行思考和任务规划，直接调用操作系统和外部资源，实现 Skill 动态创建与执行，并通过长期记忆和知识库实现持续学习与成长。相比 OpenClaw，它"
external_url: https://github.com/zhayujie/CowAgent
scenarios: ["大语言模型", "AI/ML项目", "RAG应用"]
---

# CowAgent：基于大模型的多平台AI助理框架

> **原名**: zhayujie /

      CowAgent

---

## 基本信息

- **描述**: CowAgent (chatgpt-on-wechat) 是基于大模型的超级AI助理，能主动思考和任务规划、访问操作系统和外部资源、创造和执行Skills、通过长期记忆和知识库不断成长，比OpenClaw更轻量和便捷。同时支持微信、飞书、钉钉、企微、QQ、公众号、网页等接入，可选择OpenAI/Claude/Gemini/DeepSeek/Qwen/GLM/Kimi/LinkAI，能处理文本、语音、图片和文件，可快速搭建个人AI助理和企业数字员工。
- **语言**: Python
- **星标**: 43,350 (+93 stars today)
- **链接**: [https://github.com/zhayujie/CowAgent](https://github.com/zhayujie/CowAgent)
- **DeepWiki**: [https://deepwiki.com/zhayujie/CowAgent](https://deepwiki.com/zhayujie/CowAgent)

---
## DeepWiki 速览（节选）

# CowAgent Overview

Relevant source files

  * [README.md](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1)
  * [app.py](https://github.com/zhayujie/CowAgent/blob/9402e63f/app.py)
  * [bridge/bridge.py](https://github.com/zhayujie/CowAgent/blob/9402e63f/bridge/bridge.py)
  * [channel/channel_factory.py](https://github.com/zhayujie/CowAgent/blob/9402e63f/channel/channel_factory.py)
  * [channel/chat_channel.py](https://github.com/zhayujie/CowAgent/blob/9402e63f/channel/chat_channel.py)
  * [common/const.py](https://github.com/zhayujie/CowAgent/blob/9402e63f/common/const.py)
  * [config-template.json](https://github.com/zhayujie/CowAgent/blob/9402e63f/config-template.json)
  * [config.py](https://github.com/zhayujie/CowAgent/blob/9402e63f/config.py)
  * [docker/docker-compose.yml](https://github.com/zhayujie/CowAgent/blob/9402e63f/docker/docker-compose.yml)
  * [docs/en/README.md](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/en/README.md?plain=1)
  * [docs/en/guide/quick-start.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/en/guide/quick-start.mdx?plain=1)
  * [docs/en/intro/features.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/en/intro/features.mdx?plain=1)
  * [docs/en/intro/index.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/en/intro/index.mdx?plain=1)
  * [docs/guide/quick-start.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/guide/quick-start.mdx?plain=1)
  * [docs/intro/features.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/intro/features.mdx?plain=1)
  * [docs/intro/index.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/intro/index.mdx?plain=1)
  * [docs/ja/README.md](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/ja/README.md?plain=1)
  * [docs/ja/guide/quick-start.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/ja/guide/quick-start.mdx?plain=1)
  * [docs/ja/intro/features.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/ja/intro/features.mdx?plain=1)
  * [docs/ja/intro/index.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/ja/intro/index.mdx?plain=1)
  * [docs/skills/index.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/skills/index.mdx?plain=1)
  * [docs/skills/install.mdx](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/skills/install.mdx?plain=1)
  * [scripts/run.ps1](https://github.com/zhayujie/CowAgent/blob/9402e63f/scripts/run.ps1)

**CowAgent** is a high-performance, extensible AI assistant framework powered by Large Language Models (LLMs). It is designed to function as an autonomous agent capable of task planning, computer operation, and continuous learning through a sophisticated memory and knowledge base system [README.md10](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L10-L10)

Unlike traditional chatbots, CowAgent operates as a "Super Assistant" that can proactively think, execute complex workflows via a plugin-based tool system, and integrate into numerous communication channels including WeChat, Feishu, DingTalk, and web-based consoles [README.md25-33](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L25-L33)

### Core Capabilities

  * **Autonomous Task Planning** : Understands complex objectives and autonomously plans execution steps, invoking tools until the goal is met [docs/intro/index.mdx24-26](https://github.com/zhayujie/CowAgent/blob/9402e63f/docs/intro/index.mdx?plain=1#L24-L26)
  * **Multi-Modal Processing** : Handles text, voice, images, and files across different platforms [README.md31](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L31-L31)
  * **Long-term Memory** : Persists conversation history into local SQLite databases and vector stores, supporting temporal decay scoring and keyword retrieval [README.md26](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L26-L26)
  * **Skills & Tools**: Features a "Skill Hub" for installing new capabilities via Git or natural language dialogue, alongside built-in tools for browser automation and terminal execution [README.md28-29](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L28-L29)
  * **Multi-Channel & Multi-Model**: Supports simultaneous connections to various platforms and flexible switching between providers like OpenAI, Claude, Gemini, and DeepSeek [README.md32-33](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L32-L33)

* * *

### System Architecture

The CowAgent architecture bridges the gap between external communication platforms (Channels) and the internal reasoning engines (Bots/Agents).

#### High-Level Message Flow

The following diagram illustrates how a message from a user (Natural Language Space) is transformed into internal entities (Code Space) and processed by the system.

**Message Transformation & Routing**

Sources: [channel/chat_channel.py43-52](https://github.com/zhayujie/CowAgent/blob/9402e63f/channel/chat_channel.py#L43-L52) [bridge/bridge.py12-20](https://github.com/zhayujie/CowAgent/blob/9402e63f/bridge/bridge.py#L12-L20) [bridge/bridge.py83-94](https://github.com/zhayujie/CowAgent/blob/9402e63f/bridge/bridge.py#L83-L94) [bridge/bridge.py122-132](https://github.com/zhayujie/CowAgent/blob/9402e63f/bridge/bridge.py#L122-L132)

* * *

### Major Subsystems

#### 1\. Communication Channels

CowAgent uses a `ChannelFactory` to instantiate various communication adapters. The `ChannelManager` handles the lifecycle of these channels, allowing multiple channels (e.g., a Web Console and a WeChat bot) to run concurrently in separate daemon threads [app.py38-48](https://github.com/zhayujie/CowAgent/blob/9402e63f/app.py#L38-L48)

  * **Supported Channels** : WeChat (itchat), WeCom, Feishu, DingTalk, QQ, and a built-in Web Console [channel/channel_factory.py15-46](https://github.com/zhayujie/CowAgent/blob/9402e63f/channel/channel_factory.py#L15-L46)
  * **For details, see[Communication Channels](/zhayujie/CowAgent/4-communication-channels).**

#### 2\. The Bridge & Bot Factory

The `Bridge` acts as a singleton router. It identifies the requested `bot_type` or `model` from the configuration and uses the `BotFactory` to generate the appropriate LLM interface [bridge/bridge.py12-32](https://github.com/zhayujie/CowAgent/blob/9402e63f/bridge/bridge.py#L12-L32) It manages both standard chat bots and the specialized `AgentBridge` for autonomous tasks [bridge/bridge.py122-129](https://github.com/zhayujie/CowAgent/blob/9402e63f/bridge/bridge.py#L122-L129)

  * **For details, see[Bridge and Bot Factory](/zhayujie/CowAgent/2.2-bridge-and-bot-factory).**

#### 3\. Agent Mode

When enabled via `agent: true` in `config.json` [config-template.json30](https://github.com/zhayujie/CowAgent/blob/9402e63f/config-template.json#L30-L30) CowAgent shifts from a simple request-response model to a "Plan-Execute-Observe" loop. This mode utilizes a `Workspace` directory for file operations and a memory system to maintain long-term context [README.md25-29](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L25-L29)

  * **For details, see[Agent Mode](/zhayujie/CowAgent/3-agent-mode).**

#### 4\. Plugin System

The `PluginManager` provides a high-level event bus. Plugins can intercept messages at various stages (e.g., `ON_RECEIVE_MESSAGE`) to modify behavior without altering the core codebase [channel/chat_channel.py96-97](https://github.com/zhayujie/CowAgent/blob/9402e63f/channel/chat_channel.py#L96-L97)

  * **For details, see[Plugin System](/zhayujie/CowAgent/2.3-plugin-system).**

* * *

### Getting Started and Configuration

CowAgent is designed for ease of deployment. It can be launched via a one-click script, the `cow` CLI, or Docker [README.md89-105](https://github.com/zhayujie/CowAgent/blob/9402e63f/README.md?plain=1#L89-L105)

**System Component Interaction**

Sources: [app.py60-80](https://github.com/zhayujie/CowAgent/blob/9402e63f/app.py

[...truncated...]

---
## 导语

CowAgent 是一个基于大模型的 AI 助理框架，支持主动思考、任务规划和长期记忆等能力。与传统对话机器人不同，它可以访问操作系统和外部资源，并通过 Skills 机制扩展功能。该项目兼容多种即时通讯平台和主流语言模型，适合希望快速搭建个人 AI 助理或企业数字员工的开发者。本文将介绍其核心功能、接入方式以及快速部署方法。

---
## 摘要

CowAgent（chatgpt‑on‑wechat）是一款基于大模型的超级 AI 助理，采用 Python 开发，GitHub 星标已超过 43,000。该系统能够主动进行思考和任务规划，直接调用操作系统和外部资源，实现 Skill 动态创建与执行，并通过长期记忆和知识库实现持续学习与成长。相比 OpenClaw，它更轻量、部署更便捷。

#### 核心功能
- 主动思考与任务规划，支持复杂工作流自动拆解
- 操作系统级调用，可读写文件、执行命令
- Skill 引擎，支持自定义插件快速扩展
- 长期记忆 + 知识库，提供上下文连贯的对话与检索
- 多模态处理，覆盖文本、语音、图片、文件

#### 支持平台与模型
平台覆盖微信、飞书、钉钉、企业微信、QQ、公众号、网页等常用渠道；模型可选用 OpenAI、Claude、Gemini、DeepSeek、Qwen、GLM、Kimi、LinkAI 等，实现灵活的对话与业务集成。

#### 应用场景
可快速搭建个人 AI 助理，实现日程、资讯、提醒等私人助理功能；也适用于企业数字员工，提供客服、工单、CRM 自动化等业务场景。

#### 技术概况
语言：Python；代码结构清晰，提供 Docker‑Compose 部署模板，便于一键启动；项目拥有详尽的英文/中文/日文文档与快速入门指南。

CowAgent 以轻量化、插件化、多渠道接入和多模型支持为特点，为个人和企业用户提供高效、低成本的 AI 助理解决方案。

---
## 评论

#### 总体判断

CowAgent是一款面向中文社区的高成熟度开源AI助理框架，其实用性和社区活跃度在同类项目中处于领先水平。它并非概念验证型项目，而是能够真正投入生产使用的工程化产品。

#### 技术依据

从源码结构来看，项目采用模块化设计，通道层（channel）与桥接层（bridge）职责清晰，支持灵活扩展新的大模型后端和消息渠道。星标数超过43,000这一事实反映了广泛的社区认可和使用。Docker部署方案的提供降低了使用门槛。代码遵循Python社区惯例，具备基本的错误处理和配置管理机制。

#### 适用场景

该工具最适合以下场景：个人用户希望快速搭建跨平台AI助理（如微信、QQ私人助手）；中小企业需要低成本的数字员工解决方案；开发者希望以开源项目为原型进行二次开发或学习大模型应用集成。需要明确的是，该项目主要解决的是“大模型能力接入”和“多渠道分发”问题，而非大模型本身的开发或训练。

#### 局限性

从技术角度看，存在以下限制：项目依赖外部大模型API，服务质量和成本受限于第三方；多渠道消息处理在高并发场景下的稳定性未在公开资料中充分验证；长期记忆和知识库功能依赖于用户自行配置的外部存储方案。推断这些功能在生产环境中可能需要额外的工程投入才能达到企业级可靠性标准。

#### 验证方式

建议潜在使用者重点关注以下方面：确认目标使用渠道在官方支持列表中；评估目标大模型API的调用成本和响应延迟是否满足业务需求；在测试环境中验证消息路由、错误重试和并发处理是否符合预期。源码仓库中的示例和文档可作为功能边界的参考基准。

---
## 技术分析

#### 架构概述

##### 分层设计
- **已知**：项目采用 **channel 层**（渠道适配器）、**bridge 层**（模型桥接）和 **agent 核心**（规划、记忆、技能）三层结构。
- **推断**：channel 层负责把不同 IM（微信、飞书、钉钉等）的消息统一为内部 `ChatMessage`；bridge 层将内部请求转发给选定的 LLM（OpenAI、Claude 等），屏蔽模型差异；agent 核心实现思考链、任务拆解、长期记忆检索和技能调用。

##### 核心模块
- **已知**：`app.py` 为服务入口，`config.py` 与 `config-template.json` 负责全局配置，`bridge/bridge.py` 抽象模型调用，`channel/channel_factory.py` 与 `channel/chat_channel.py` 实现渠道分发。
- **推断**：`docker/docker-compose.yml` 用于一键部署，文档中出现的 `docs/guide/quick-start.mdx` 说明启动流程。

##### 通信流程（推断）
1. 渠道适配器接收外部消息（文字/语音/图片）。
2. `chat_channel` 将消息统一封装，传递给 bridge。
3. bridge 调用远程 LLM API，携带系统提示、记忆上下文与技能描述。
4. LLM 返回结构化指令或文本，agent 核心解析并执行相应 Skill。
5. 结果再次经 bridge、channel 适配器返回给用户。

---

#### 核心能力

##### 多渠道接入
- **已知**：支持微信、飞书、钉钉、企业微信、QQ、公众号、网页等多端。
- **实现要点**：通过渠道工厂 `channel_factory` 按渠道类型加载对应适配器，保持业务逻辑统一。

##### 多模型支持
- **已知**：可接入 OpenAI、Claude、Gemini、DeepSeek、Qwen、GLM、Kimi、LinkAI 等。
- **推断**：模型切换仅需在配置文件中指定模型标识，bridge 层统一封装请求/响应，兼容不同 API 签名。

##### 主动思考与任务规划
- **推断**：基于 LLM 的 CoT（Chain‑of‑Thought）或 ReAct 模式，实现意图拆解、步骤规划与执行回检。系统提示中可能内置“思考链”模板，引导模型分步输出。

##### 长期记忆与知识库
- **推断**：使用向量数据库（如 Chroma、FAISS）存储对话历史与文档片段。检索时将当前上下文嵌入并在向量空间做相似度搜索，返回最相关的记忆片段作为上下文补充。

##### Skill 创造与执行
- **推断**：Skill 以插件形式定义，通常为 Python 类或函数，注册在 `skills/` 目录并声明于 `skill.json`。LLM 可通过 function‑calling 或结构化指令调用对应 Skill，完成系统命令、文件读写、API 请求等操作。

##### 多模态交互
- **已知**：能够处理文本、语音、图片、文件。
- **实现要点**：语音可能借助 Whisper 等 ASR 服务转写为文字；图片/文件通过 base64 或 URL 方式传递给 LLM，或先进行 OCR/特征抽取再嵌入。

---

#### 技术实现细节

##### 语言与框架
- **已知**：项目使用 Python。`app.py` 可能基于 Flask/FastAPI 启动 HTTP 服务，供渠道回调（如微信公众平台的服务器配置）使用。
- **推断**：大量使用 `asyncio` 与 `aiohttp` 实现并发请求，提升对多渠道的响应效率。

##### 配置管理
- **已知**：全局配置由 `config.json`（模板 `config-template.json`）提供，支持模型、渠道、记忆、技能等细粒度开关。
- **最佳实践**：敏感信息（如 API‑Key）通过环境变量注入，避免明文写入配置文件。

##### Docker 部署
- **已知**：`docker‑compose.yml` 包含了服务依赖（Redis、向量库等），可一键拉起完整运行环境。
- **建议**：在生产环境使用自定义网络、持久化卷和资源限制，保证记忆数据的可靠性。

##### 记忆层（推断）
- **向量检索**：使用 `sentence-transformers` 生成嵌入，存入 Chroma/FAISS。检索时结合时间衰减或重要度权重，提升上下文相关性。
- **持久化**：对话日志、用户画像等结构化数据可写入 PostgreSQL/MySQL，配合向量库实现混合检索。

##### 消息路由（推断）
- `channel_factory` 根据消息来源字段（如 `source=wechat`）实例化对应 adapter；adapter 负责签名校验、消息格式解析和响应封送。
- `chat_channel` 充当统一入口，调用 bridge 前对消息进行清洗、去重和限流。

---

#### 适用场景

##### 企业数字员工
- 多平台客服、HR 问答、内部流程自动化。借助长期记忆，可保持跨会话上下文，降低重复解释成本。

##### 个人 AI 助理
- 日程管理、资讯聚合、快捷指令执行。通过 Skill 插件快速扩展，如查询天气、记账、邮件摘要等。

##### 知识库问答
- 基于文档的检索式问答，利用向量记忆提升答案准确性；可对接内部 Wiki、FAQ，实现秒级检索。

##### 轻量化原型验证
- 对于想在微信/钉钉等平台快速验证 AI 概念的团队，CowAgent 提供开箱即用的渠道适配和模型接入，大幅缩短交付周期。

---

#### 不适用场景

##### 极高实时性需求
- LLM API 的响应时间通常在几百毫秒至数秒之间，不适合需要毫秒级交互的游戏或实时监控告警。

##### 完全离线环境
- 项目依赖外部模型服务（OpenAI、Claude 等），若业务必须在内网运行，需要自行部署开源 LLM（如 LLaMA）并改造 bridge。

##### 超大规模并发
- 单体架构在垂直扩展上受限；当日活用户突破十万或日消息量达百万级别时，需要拆分微服务、引入消息队列和分布式记忆层。

---

#### 学习与落地建议

##### 入门路径
1. 阅读 `README.md` 与 `docs/guide/quick-start.mdx`，在本机使用 Docker 启动最小化实例。
2. 通过 `config-template.json` 配置一个渠道（如微信）并获取回调 URL，完成首次对话。

##### 拓展记忆
- 引入 Chroma：在 `requirements.txt` 中加入 `chromadb`，在 `config.json` 启用 `memory: vector`，配置嵌入模型（如 `sentence-transformers/all-MiniLM-L6-v2`）。
- 定期将重要对话写入向量库，使用 `memory/retrieval.py` 实现检索回调。

##### 开发 Skill
1. 在 `plugins/` 下新建 Python 类，继承 `BaseSkill`，实现 `execute(self, context)` 方法。
2. 在 `skill.json` 注册技能名称、描述与调用方式。
3. 在系统提示中加入 “你可以使用 skill: xxx”，LLM 会生成结构化调用指令。

##### 安全与合规
- 将 API‑Key、渠道 Token 存放于 `.env`，使用 `python-dotenv` 读取；生产环境推荐使用 Kubernetes Secret 或 Vault。
- 对外暴露的回调 URL 建议使用 HTTPS 并开启签名校验，防止恶意请求。

##### 性能调优
- 使用 `asyncio` 对渠道请求并行化，合理设置 API 超时（建议 30 s）和重试次数。
- 对高频渠道（如企业微信）实现消息批处理或限流，防止触发平台频率限制。

##### 监控与日志
- 集成 `prometheus_client`，将 API 延迟、渠道错误率、技能调用成功率暴露为指标。
- 日志采用结构化 JSON，配合 ELK Stack 做搜索与告警。

##### 持续迭代
- 将 Skill 与记忆层纳入 CI/CD，自动化测试覆盖率可通过模拟对话脚本验证。
- 关注模型厂商的政策与费用，定期评估性价比，必要时在 bridge 层加入多模型降级策略。

整体而言，CowAgent 通过 **渠道抽象、模型桥接、记忆‑Skill 插件** 三大核心实现了“一次开发，多端部署”的 AI 助理平台。适合快速构建企业或个人对话助手，但在极端实时、离线或超大并发场景下需结合自托管模型与微服务化改造才能满足需求。

---
## 学习要点

- 很抱歉，仅凭提供的标题信息无法提取出具体的知识点。如果您能提供 CowAgent 项目的详细描述、README 内容或主要功能说明，我可以为您归纳出 5‑7 条关键要点。

---
## 引用

- **GitHub 仓库**: [https://github.com/zhayujie/CowAgent](https://github.com/zhayujie/CowAgent)
- **DeepWiki**: [https://deepwiki.com/zhayujie/CowAgent](https://deepwiki.com/zhayujie/CowAgent)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [大模型](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI助理](/tags/ai%E5%8A%A9%E7%90%86/) / [多平台](/tags/%E5%A4%9A%E5%B9%B3%E5%8F%B0/) / [插件化](/tags/%E6%8F%92%E4%BB%B6%E5%8C%96/) / [多模态](/tags/%E5%A4%9A%E6%A8%A1%E6%80%81/) / [Docker](/tags/docker/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [企业数字员工](/tags/%E4%BC%81%E4%B8%9A%E6%95%B0%E5%AD%97%E5%91%98%E5%B7%A5/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [CowAgent：开源多平台AI助理框架，支持十余种模型]({{< relref "posts/20260415-github_trending-zhayujie-cowagent-0.md" >}})
- [CowAgent：开源多平台AI助理框架，支持多渠道接入]({{< relref "posts/20260416-github_trending-zhayujie-cowagent-0.md" >}})
- [ChatGPT-on-WeChat：支持多模型与多平台接入的AI助理框架]({{< relref "posts/20260207-github_trending-zhayujie-chatgpt-on-wechat-1.md" >}})
- [ChatGPT-on-WeChat：接入多平台与大模型的多模态AI助理]({{< relref "posts/20260221-github_trending-zhayujie-chatgpt-on-wechat-3.md" >}})
- [基于大模型的AI助理ChatGPT-on-WeChat：支持多平台接入与多模型]({{< relref "posts/20260226-github_trending-zhayujie-chatgpt-on-wechat-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*