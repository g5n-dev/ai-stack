---
title: Spring AI 多模型对话实战：统一接口与 Redis 记忆
date: 2026-02-17 15:40:46+08:00
draft: false
entry_kind: auto
tags:
- Spring AI
- LLM
- OpenAI
- Ollama
- Redis
- SSE
- AOP
- 流式输出
categories:
- 后端
- AI 工程
source: juejin
description: 这是一份关于 **Spring AI 多模型对话实战 Demo** 的简洁总结： **1. 核心功能：多模型统一适配** 该 Demo 实现了一套
  API 接口同时兼容 **OpenAI** 和 **Ollama** 两种大模型服务。系统通过 参数进行智能路由，支持在运行时动态覆盖模型名称，开发者无需为不同模型编写重复
external_url: https://juejin.cn/post/7606793134375534655
scenarios:
- AI/ML项目
- 大语言模型
- 后端开发
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **作者**: 求知摆渡
- **链接**: [https://juejin.cn/post/7606793134375534655](https://juejin.cn/post/7606793134375534655)

---
## 导语

Spring AI 为 Java 生态接入大模型提供了标准化的解决方案，但在实际业务中，往往需要同时兼容云端与本地模型，并处理会话记忆与流式响应等细节。本文通过一套可复用的实战 Demo，演示了如何用统一接口适配 OpenAI 与 Ollama，并利用 Redis 实现上下文管理。阅读后，你将掌握多模型路由、SSE 流式输出及 AOP 日志打点的具体实现，从而快速构建稳定的企业级 AI 应用。

---
## 描述

这是一套可直接复用的 Spring AI 示例：同一套 API 同时兼容 OpenAI 与 Ollama，根据 provider 路由模型，并支持运行时覆盖 model；会话上下文通过 Redis 实现。

---
## 摘要

这是一份关于 **Spring AI 多模型对话实战 Demo** 的简洁总结：

**1. 核心功能：多模型统一适配**
该 Demo 实现了一套 API 接口同时兼容 **OpenAI** 和 **Ollama** 两种大模型服务。系统通过 `provider` 参数进行智能路由，支持在运行时动态覆盖模型名称，开发者无需为不同模型编写重复代码，实现了灵活的模型切换与调用。

**2. 会话记忆：Redis 存储**
为了解决大模型无状态的问题，项目引入了 **Redis** 来存储和管理会话上下文（Chat Memory）。这使得应用能够具备多轮对话能力，让 AI 记住之前的交流内容，从而提供更连贯的交互体验。

**3. 交互体验：SSE 流式输出**
在响应性能方面，Demo 采用了 **SSE (Server-Sent Events)** 技术。这意味着 AI 的生成内容是逐字推送到前端的，而非等待全部生成完毕后一次性返回，极大地提升了用户在对话时的实时感官体验。

**4. 运维与监控：AOP 日志打点**
代码中运用了 **AOP（面向切面编程）** 技术，实现了非侵入式的日志采集。通过切面统一记录关键节点信息，便于后续进行问题排查、数据统计及系统监控，保持了业务代码的整洁性。

**总结：**
这是一个高可复用的 Spring AI 脚手架，涵盖了从模型层适配、状态管理、流式交互到系统监控的完整闭环，适合作为企业级 AI 应用的基础框架进行二次开发。

---
## 评论

**文章中心观点**
本文旨在构建一套基于 Spring AI 的企业级对话脚手架。核心方案通过抽象层屏蔽异构大模型（OpenAI/Ollama）的 API 差异，并利用 Redis 结合 SSE 技术处理有状态会话管理与流式响应，旨在解决 AI 应用集成中的工程化痛点。

**支撑理由与多维评价**

**1. 架构设计与工程严谨性**
文章展示了“防腐层”架构思想在 AI 集成中的应用。通过实现 ChatClient 的动态路由，有效隔离了底层模型厂商的 API 变动，符合依赖倒置原则（DIP）。
*   **论证分析**：利用 Redis 存储 ChatHistory 是解决 LLM 无状态特性的标准方案。但文章若仅停留在基础配置，在生产级实践中仍面临挑战。例如，Token 序列化策略（String vs. Hash）、TTL 设置策略以及超出 Context Window 时的截断逻辑（如滑动窗口），均是必须考虑的工程细节。
*   **局限与边界**：在长上下文场景下，单纯依赖 Redis 存储全量历史会导致 Prompt 膨胀，增加 Token 成本并可能引发模型焦点迷失。生产环境通常需引入 RAG（检索增强生成）或摘要记忆机制作为补充。

**2. 实用价值与落地场景**
对于企业级开发者，该方案提供了具备参考价值的脚手架。
*   **论证分析**：针对网络环境与算力限制，文章提出的混合部署方案具有实际意义。开发者可在开发测试阶段使用 Ollama（本地、私有），在生产环境切换至 OpenAI 或 Azure OpenAI，保证了环境的一致性。此外，AOP 切面日志解决了 AI 调用链路追踪的“黑盒”问题，有助于审计与调试。
*   **局限与边界**：Spring AI 目前处于快速迭代期（如 1.0.0 M1 前后 API 变动较大），依赖快照版本存在兼容性风险。同时，Ollama 受限于本地算力，其并发处理能力与推理延迟不及云端 GPU 集群，该架构更适合内部工具或低并发场景，而非高并发 ToC 产品。

**3. 技术实现与性能考量**
文章的技术亮点在于 SSE 与 Redis 的结合使用，这是实现类 ChatGPT 流式交互的标准实践。
*   **论证分析**：相比 WebSocket，SSE 在服务端向客户端单向推送文本流的场景下更轻量，且易于与 Spring WebFlux/MVC 整合。
*   **局限与边界**：在微服务架构中，AOP 切面若处理不当（如完整打印 Request/Response Body），会带来显著的性能开销与存储成本。对于流式输出，如何在不阻塞流传输的前提下进行结构化日志记录是一个技术难点，粗暴的 AOP 实现可能导致内存溢出或响应阻塞。

**4. 行业趋势与生态定位**
本文反映了 LLMOps 从“提示词工程”向“应用工程化”演进的趋势。
*   **论证分析**：Spring AI 的出现标志着 Java 企业级生态正在接入 AI 能力。该案例验证了利用 Java 成熟组件（如 Redis、AOP）构建稳健后端服务的可行性，弥补了 Python 生态在并发与分布式治理上的短板。
*   **局限与边界**：当前 LangChain（Python/JS）仍占据市场主导，Spring AI 的社区生态与插件丰富度尚有差距。企业在选型时，可能会因缺乏特定向量数据库或第三方工具的现成集成支持而受限。

**可验证的检查方式**

1.  **并发压力测试**：
    *   *指标*：在 Redis 开启持久化（AOF/RDB）时，模拟 500 并发用户进行流式对话。
    *   *验证点*：观察 SSE 连接稳定性及 Redis CPU/内存开销，以评估架构在高负载下的表现。

2.  **模型兼容性测试**：
    *   *指标*：构造包含 Function Calling（函数调用）的请求，分别路由至 OpenAI GPT-4 与 Ollama 支持的模型（如 Llama 3）。
    *   *验证点*：验证抽象层是否能正确处理不同模型间的参数差异与响应格式。

---
## 学习要点

- Spring AI 实现了 OpenAI 与 Ollama 等本地模型的无缝切换，通过统一接口屏蔽了不同大模型厂商的底层差异
- 利用 Redis ChatMemory 组件解决了大模型无状态问题，实现了跨请求的上下文记忆与多轮对话管理
- 基于 Spring WebFlux 的 StreamingChatModel 原生支持 SSE 流式输出，有效降低了大模型首字生成延迟
- 通过 AOP 切面技术实现了对模型调用耗时、Token 消耗及提示词内容的无侵入式监控与日志打点
- 引入 Prompt Template（提示词模版）进行动态参数管理，实现了业务逻辑与提示词构建的解耦
- 使用 Spring Boot Configuration 封装了模型参数配置，支持灵活切换 Ollama 等本地私有化部署模型

---
## 常见问题


### 1: Spring AI 如何实现 OpenAI 和 Ollama 等不同模型的统一调用？

1: Spring AI 如何实现 OpenAI 和 Ollama 等不同模型的统一调用？

**A**: Spring AI 提供了统一的 API 抽象层，通过 `ChatClient` 或 `ChatModel` 接口屏蔽了不同厂商（如 OpenAI、Ollama、Azure OpenAI）的差异。开发者只需在配置文件（如 `application.yml`）中定义不同的 `ChatModel` Bean（例如 `openAiChatModel` 和 `ollamaChatModel`），然后在代码中通过构造器注入或 `@Qualifier` 注解指定使用哪个模型实现。这样，业务代码不需要修改，只需切换注入的 Bean 即可在云端大模型和本地模型之间灵活切换。

---



### 2: 在 SSE 流式输出场景下，如何确保 Redis 会话记忆的准确性？

2: 在 SSE 流式输出场景下，如何确保 Redis 会话记忆的准确性？

**A**: 在流式输出（SSE）场景下，AI 的回复是分片返回的。为了确保 Redis 存储完整的对话历史，不能在接收到每一个 Token 时就更新 Redis，这样会造成巨大的网络开销和存储浪费。最佳实践是利用响应式编程（如 Reactor 的 `Flux`），在流式传输结束后（使用 `.collectList()` 或 `doOnComplete()`），将完整的回复内容拼接后，再通过 `ChatMemory` 接口写入 Redis。这样可以保证 Redis 中存储的是完整的上下文，便于下一次对话时准确提取。

---



### 3: 如何利用 Spring AOP 实现 AI 对话的全链路日志打点？

3: 如何利用 Spring AOP 实现 AI 对话的全链路日志打点？

**A**: 可以定义一个切面（Aspect），切入点（Pointcut）设置为 Controller 层的处理对话方法。在 `@Around` 环绕通知中，可以记录方法入参（Prompt、模型配置）、开始时间。在方法执行过程中或结束后，记录返回结果、Token 消耗情况以及结束时间。通过计算时间差统计耗时，并将请求 ID、用户 ID、模型名称等关键信息记录到日志文件或数据库中，从而实现非侵入式的全链路监控和后续的问题排查。

---



### 4: 使用 Ollama 作为本地模型时，Spring AI 连接超时或响应慢怎么解决？

4: 使用 Ollama 作为本地模型时，Spring AI 连接超时或响应慢怎么解决？

**A**: Ollama 默认运行在本地 11434 端口。如果遇到连接超时，首先检查 Ollama 服务是否正常启动。其次，由于本地模型推理依赖 CPU/GPU 性能，首字生成时间（TTFT）可能较长，建议在 Spring AI 的配置中适当调大连接超时时间（`connect-timeout`）和读取超时时间（`read-timeout`）。此外，如果使用的是较新的模型版本或量化模型，确保 Ollama 版本已更新，并检查本地资源（内存/显存）是否被占满。

---



### 5: 如何处理多用户场景下的 Redis 会话隔离问题？

5: 如何处理多用户场景下的 Redis 会话隔离问题？

**A**: 为了防止不同用户的对话历史混淆，必须在存取 Redis 时使用唯一的会话 ID。通常的做法是在前端请求时携带一个 `sessionId`（或 `conversationId`），后端在构建 `ChatMemory` 配置时，将该 ID 作为 Redis Key 的一部分（例如 Key 格式设计为 `chat:memory:{userId}:{sessionId}`）。Spring AI 的 `RedisChatMemory` 配置类通常支持自定义 Key 生成策略，通过动态传入会话 ID，确保每个用户的对话上下文独立存储和检索。

---



### 6: SSE 流式输出在前端断开连接后，后端服务是否会继续执行？

6: SSE 流式输出在前端断开连接后，后端服务是否会继续执行？

**A**: 在标准的 Spring WebFlux 或 MVC + SSE 实现中，如果客户端（浏览器）断开连接，底层的 HTTP 连接会关闭。Spring 的响应式流（Reactor）会检测到连接终止信号，通常会触发 `onCancel` 或 `onError` 事件，从而中断数据流的发射。这意味着后端的 AI 推理请求可能会被中断（取决于具体的流式处理实现），从而节省服务器资源。但在日志打点时，建议监听这一事件，将“客户端断开”的状态记录下来，以便区分是正常结束还是异常中断。

---
## 引用

- **掘金原文**: [https://juejin.cn/post/7606793134375534655](https://juejin.cn/post/7606793134375534655)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Spring AI](/tags/spring-ai/) / [LLM](/tags/llm/) / [OpenAI](/tags/openai/) / [Ollama](/tags/ollama/) / [Redis](/tags/redis/) / [SSE](/tags/sse/) / [AOP](/tags/aop/) / [流式输出](/tags/%E6%B5%81%E5%BC%8F%E8%BE%93%E5%87%BA/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [Kirara-ai：支持多平台接入的多模态AI聊天机器人]({{< relref "posts/20260127-github_trending-lss233-kirara-ai-2.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人框架]({{< relref "posts/20260127-github_trending-lss233-kirara-ai-2.md" >}})
- [发现逾17.5万个Ollama AI实例公网暴露]({{< relref "posts/20260131-hacker_news-175k-publicly-exposed-ollama-ai-instances-discover-19.md" >}})
- [多模态 AI 聊天机器人 Kirara AI：支持多平台接入与主流模型]({{< relref "posts/20260127-github_trending-lss233-kirara-ai-2.md" >}})
- [Codex 应用：基于 GPT-3 的代码生成工具]({{< relref "posts/20260202-hacker_news-the-codex-app-1.md" >}})
*本文由 AI Stack 自动生成，提供深度内容分析。*
