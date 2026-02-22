---
title: "Spring AI MCP 结合 WebFlux SSE 构建 AI 天气助手"
date: 2026-02-22T07:40:33+08:00
draft: false
entry_kind: "auto"
tags: ["Spring AI", "MCP", "WebFlux", "SSE", "LLM", "流式响应", "实战教程", "天气助手"]
categories: ["后端", "AI 工程"]
source: juejin
description: "在 AI 应用开发中，如何让大语言模型（LLM）与外部工具无缝集成一直是个难题。MCP（Model Context Protocol，模型上下文协议）为此提供了一个标准化的解决方案。本文将带你一步步实现一个基于 Spring WebFlux 的 Server-Sent Events（SSE）流式响应的 AI 天气助手，"
external_url: https://juejin.cn/post/7608212715346690054
scenarios: ["AI/ML项目", "Web应用开发", "大语言模型"]
---

# Spring AI MCP 结合 WebFlux SSE 构建 AI 天气助手

---

## 基本信息

- **作者**: 玹外之音
- **链接**: [https://juejin.cn/post/7608212715346690054](https://juejin.cn/post/7608212715346690054)

---
## 导语

在 AI 应用开发中，如何让大语言模型（LLM）与外部工具无缝集成一直是个难题。MCP（Model Context Protocol，模型上下文协议）为此提供了一个标准化的解决方案。本文将带你一步步实现一个基于 Spring WebFlux 的 Server-Sent Events（SSE）流式响应的 AI 天气助手，展示如何通过 MCP 将实时天气查询能力赋予 LLM。

---
## 描述

Spring AI MCP 之 SSE WebFlux 实战：从零构建 AI 天气助手
引言
在 AI 应用开发中，如何让大语言模型（LLM）与外部工具无缝集成一直是个难题。MCP（Model Context Protocol，模型上下文协议）为此提供了一个标准化的解决方案。本文将带你一步步实现一个基于 Spring WebFlux 的 Server-Sent Events（SSE）流式响应的 AI 天气助手，展示如何通过 MCP 将实时天气查询能力赋予 LLM。

---
## 评论

### 中心观点
该文章通过演示 Spring AI 与 MCP 协议的集成，提出了一种基于响应式编程（WebFlux）和 SSE（服务端推送）的技术架构，旨在解决 LLM 与外部工具集成的实时性与流式输出问题，但其“从零构建”的叙事掩盖了生产环境中的复杂性。

### 深入评价

#### 1. 内容深度：架构演示有余，工程严谨性不足
*   **支撑理由（事实陈述）：** 文章准确捕捉了当前 AI 应用开发的痛点——即 LLM 无法直接获取实时数据（如天气），需要通过 MCP（Model Context Protocol）这一新兴协议进行桥接。同时，选择 WebFlux 和 SSE 是处理流式 AI 响应的正确技术选型，能够有效避免传统阻塞式 I/O 在高并发下的资源耗尽问题。
*   **反例/边界条件（你的推断）：** 文章可能仅展示了“快乐路径”。在实际生产中，MCP 协议的握手、鉴权以及异常处理（如天气 API 超时）远比 Demo 复杂。如果文章未涉及 SSE 连接中断后的重连机制或 WebFlux 的背压处理策略，则其工程深度仅停留在“Hello World”级别。

#### 2. 实用价值：入门指南优秀，但缺乏生产级指导
*   **支撑理由（作者观点）：** 对于想要快速了解 Spring AI 生态和 MCP 协议的开发者，这篇文章提供了一个清晰的脚手架。代码片段展示了如何声明工具、如何处理流式响应，这对于降低 AI 开发门槛具有直接的指导意义。
*   **反例/边界条件（事实陈述）：** 实际工作中，构建 AI 助手不仅仅是调用 API。文章可能未涉及 Prompt Engineering（提示词工程）的细节，例如如何防止 LLM 产生幻觉，或者如何处理 MCP 工具调用时的参数解析错误。如果开发者直接照搬代码到生产环境，可能会遇到严重的稳定性问题。

#### 3. 创新性：技术栈组合新颖，但概念复用为主
*   **支撑理由（你的推断）：** 将 MCP 协议与 Spring Boot 3.x 的响应式栈结合是文章的主要创新点。目前业界关于 OpenAI API 调用的教程多基于阻塞式 Feign 或 RestTemplate，文章采用的 WebFlux + SSE 模式更符合 AI 交互“流式”的本质，具有一定的前瞻性。
*   **反例/边界条件（作者观点）：** MCP 本身并非革命性技术，它本质上是 RPC 协议的一种变体。文章并未提出新的算法或架构范式，更多是现有技术（Spring, WebFlux, SSE）在 AI 爆发背景下的新组合应用。

#### 4. 可读性：逻辑清晰，但需警惕“教程陷阱”
*   **支撑理由（事实陈述）：** 标题直击痛点，摘要部分明确了技术栈，结构符合技术类文章的标准范式。通常这类文章会按照“问题引入 -> 方案设计 -> 代码实现 -> 效果演示”的逻辑展开，易于读者跟随。
*   **反例/边界条件（你的推断）：** 如果文章充斥着大量的配置文件粘贴而缺乏核心逻辑的流程图解析，或者对 SSE 的原理仅做蜻蜓点水式的介绍，则其可读性仅限于“复制粘贴工程师”，无法帮助读者建立深层认知。

#### 5. 行业影响：顺应趋势，但受限于生态成熟度
*   **支撑理由（作者观点）：** MCP 协议由 Anthropic 提出，旨在统一 AI 与本地数据的交互标准。文章对 Spring AI MCP 的实战探索，有助于推动 Java 企业级开发社区（通常较为保守）接纳 AI 原生开发理念。
*   **反例/边界条件（事实陈述）：** 目前 MCP 生态尚未完全成熟，Spring AI 也处于快速迭代期（版本更新极快）。文章中的代码可能在 3 个月后就因 API 变更而失效，这种不稳定性是行业影响的一大制约因素。

#### 6. 争议点与不同观点
*   **争议点（你的推断）：** **“是否应该在业务层直接暴露 MCP 协议细节？”**
    *   文章可能主张直接集成，认为这样更轻量。
    *   另一种观点认为，MCP 应该作为基础设施层，业务层应通过更抽象的 Gateway 或 Agent 框架（如 LangChain4j）来调用，以解耦协议与业务逻辑。直接在 Controller 中处理 MCP 工具调用可能会导致业务代码臃肿。
*   **争议点（作者观点）：** **“WebFlux 是否是 AI 应用的最佳选择？”**
    *   虽然 WebFlux 适合 I/O 密集型，但其调试难度和响应式编程的学习曲线极陡。对于简单的 AI 助手，使用虚拟线程配合传统的 Servlet 容器可能开发效率更高，性能差异在低并发下并不明显。

#### 7. 实际应用建议
1.  **不要直接用于生产：** 将文中的代码作为 POC（概念验证），在投入生产前，必须增加熔断机制、超时控制和日志监控。
2.  **关注 Prompt 设计：** 代码只是骨架，Prompt 是灵魂。建议在实际应用中，结合业务场景对 LLM 的 System Prompt 进行深度调优，确保 MCP 工具被正确调用。
3.  **安全性考量：** MCP 允许 LLM 调用本地工具，这带来了巨大的安全风险。务必在 MCP Server 端实施严格的权限校

---
## 学习要点

- 掌握基于 Spring WebFlux 的 SSE (Server-Sent Events) 流式输出实现，解决 AI 响应的打字机效果与实时交互问题。
- 深度整合 Spring AI 与 MCP (Model Context Protocol) 协议，实现大模型与外部工具（如天气 API）的高效函数调用。
- 利用 Reactor 响应式编程模型（Flux/Mono），构建非阻塞、高并发的后端异步处理链路。
- 通过 Function Callback 机制，精准设计 Prompt 提示词与参数映射，确保 AI 能够准确理解并调用业务接口。
- 实现前后端流式数据的完整闭环，包括后端 Flux 流的生成与前端 EventSource 的标准消费处理。
- 验证了 Spring AI 在处理复杂工具调用场景下的稳定性，为构建企业级 AI Agent 应用提供标准化的架构参考。

---
## 常见问题


### 1: Spring AI MCP 中的 SSE 和传统的 HTTP 轮询有什么区别？

1: Spring AI MCP 中的 SSE 和传统的 HTTP 轮询有什么区别？

**A**: SSE（Server-Sent Events）与 HTTP 轮询在实现 AI 流式响应时有本质区别。

1.  **连接机制**：HTTP 轮询需要客户端反复向服务器发起请求（例如每秒一次），即使没有新数据也会产生大量无效请求和 HTTP 开销。而 SSE 是基于 HTTP 的单向持久连接，客户端发起一次请求后，服务器可以保持连接打开，并在有数据生成时主动推送。
2.  **实时性与资源消耗**：SSE 的延迟更低，因为数据生成后立即推送，无需等待下一次轮询周期。同时，SSE 显著减少了服务器处理无效请求的负担。
3.  **格式标准**：SSE 有标准的文本格式（以 `data:` 开头的消息），浏览器端有标准的 `EventSource` API 支持，而轮询通常需要自定义协议解析。

在 Spring WebFlux 中，SSE 的实现非常简单，只需返回 `Flux<ServerSentEvent>` 类型，Spring 会自动处理 `Content-Type: text/event-stream` 和 Keep-Alive 机制。

---



### 2: 为什么在构建 AI 天气助手时选择 Spring WebFlux 而不是 Spring MVC？

2: 为什么在构建 AI 天气助手时选择 Spring WebFlux 而不是 Spring MVC？

**A**: 选择 WebFlux 主要是为了适配 AI 大模型流式输出的特性以及高并发场景。

1.  **背压与流式处理**：AI 模型（如 OpenAI）的返回是 Token by Token 的流式数据。Spring WebFlux 基于 Reactor（`Flux` 和 `Mono`），天然支持非阻塞的响应式流。这意味着我们可以逐个 Token 处理数据，并立即通过 SSE 推送给前端，而不需要等待整个响应生成完毕。
2.  **线程模型**：在 Spring MVC（Servlet 模型）中，每个请求会占用一个线程直到响应结束。对于长连接的 AI 对话，这容易导致线程池耗尽。WebFlux 使用少量的 EventLoop 线程即可处理大量并发连接，资源利用率极高。
3.  **统一的数据流**：从调用第三方 AI API（通常是流式 HTTP 客户端）到前端 SSE 推送，全程可以使用响应式管道无缝衔接，代码更加简洁。

---



### 3: 在实战代码中，`ServerSentEvent` 和直接返回 `Flux<String>` 有什么区别？

3: 在实战代码中，`ServerSentEvent` 和直接返回 `Flux<String>` 有什么区别？

**A**: 两者都可以实现流式传输，但 `ServerSentEvent` 提供了更丰富的语义控制。

1.  **直接返回 `Flux<String>`**：Spring WebFlux 会将字符串片段直接写入响应体。这种方式简单直接，适合纯文本流。
2.  **使用 `ServerSentEvent`**：它允许你构建结构化的 SSE 消息。你可以设置：
    *   `data()`：实际的数据负载。
    *   `event()`：事件类型（前端可以通过 `addEventListener` 监听特定类型）。
    *   `id()`：用于断线重连的 Last-Event-ID。
    *   `retry()`：重连间隔。
    *   `comment()`：注释。

在构建 AI 助手时，通常推荐使用 `Flux<String>` 配合 `produces = MediaType.TEXT_EVENT_STREAM_VALUE` 即可满足需求，因为 AI 流主要关注数据本身。但如果需要区分“开始”、“中间 Token”、“结束”等事件类型，使用 `ServerSentEvent` 会更加规范。

---



### 4: 如何处理 AI 流式输出中的异常断开或超时问题？

4: 如何处理 AI 流式输出中的异常断开或超时问题？

**A**: 在长连接或网络不稳定的环境下，流式传输可能会中断。在 Spring WebFlux 中可以通过以下机制增强健壮性：

1.  **超时设置**：使用 Reactor 的 `.timeout()` 操作符限制单次请求的最大等待时间，防止客户端无限期挂起。
2.  **重试机制**：利用 `.retryWhen()` 操作符配置重试策略。但需要注意 AI 接口的幂等性，通常流式输出一旦中断，重试是重新发起请求，而不是从断点继续。
3.  **错误信号处理**：在 Flux 管道末端使用 `.doOnError()` 或 `.onErrorResume()`。当发生错误（如 AI 服务 502 错误）时，可以发送一个特殊的 SSE 事件（例如 `data: [ERROR] ...`）给前端，让前端知道流已异常终止，而不是让连接静默断开。
4.  **前端配合**：前端 `EventSource` 自带自动重连机制，但需要后端在最后发送一个结束标记（如 `data: [DONE]`），以便前端主动关闭连接，避免不必要的重连尝试。

---



### 5: MCP (Model Context Protocol) 在此架构中扮演什么角色？

5: MCP (Model Context Protocol) 在此架构中扮演什么角色？

**A**: MCP 是连接 AI 模型与外部数据源（如天气 API）的标准化桥梁。

1.  **解决上下文局限**：大模型本身无法获取实时天气数据。MCP 定义了一种标准协议，允许 AI 应用通过“工具调用”的方式与外部系统交互。

---
## 引用

- **掘金原文**: [https://juejin.cn/post/7608212715346690054](https://juejin.cn/post/7608212715346690054)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Spring AI](/tags/spring-ai/) / [MCP](/tags/mcp/) / [WebFlux](/tags/webflux/) / [SSE](/tags/sse/) / [LLM](/tags/llm/) / [流式响应](/tags/%E6%B5%81%E5%BC%8F%E5%93%8D%E5%BA%94/) / [实战教程](/tags/%E5%AE%9E%E6%88%98%E6%95%99%E7%A8%8B/) / [天气助手](/tags/%E5%A4%A9%E6%B0%94%E5%8A%A9%E6%89%8B/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Spring AI 多模型对话实战：统一接口与 Redis 记忆]({{< relref "posts/20260217-juejin-spring-ai-多模型对话-demo-实战openaiollama-一套接口redis-会话记忆-3.md" >}})
- [Spring AI 多模态实战：构建图像理解应用]({{< relref "posts/20260219-juejin-spring-ai-多模态实战手把手教你构建图像理解应用-3.md" >}})
- [Spring AI 多模态实战：构建图像理解应用]({{< relref "posts/20260219-juejin-spring-ai-多模态实战手把手教你构建图像理解应用-0.md" >}})
- [Flutter SSE 流式响应：基于 Dio 实现 OpenAI 逐 Token 输出]({{< relref "posts/20260221-juejin-flutter-sse-流式响用-dio-实现-openai-兼容接口的逐-token-输出-0.md" >}})
- [Spring AI 结构化输出转换器实战：告别字符串解析，拥抱类型安全]({{< relref "posts/20260218-juejin-spring-ai-结构化输出转换器实战告别字符串解析拥抱类型安全-4.md" >}})
*本文由 AI Stack 自动生成，提供深度内容分析。*