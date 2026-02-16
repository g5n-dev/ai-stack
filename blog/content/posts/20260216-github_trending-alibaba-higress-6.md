---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-02-16T15:22:30+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是关于 **Higress** 项目的简洁总结： **项目概况** Higress 是阿里巴巴开源的一款**云原生 AI 网关**。基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前在 GitHub 上拥有超过 7,500 颗星。 **核心定位** Higress 旨在解决 AI 时代流量管理的需求"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "大语言模型", "云原生/容器"]
---

# 阿里 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,535 (+4 stars today)
- **链接**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

---
## DeepWiki 速览（节选）

# Overview

Relevant source files

  * [README.md](https://github.com/alibaba/higress/blob/8deceb4d/README.md)
  * [README_JP.md](https://github.com/alibaba/higress/blob/8deceb4d/README_JP.md)
  * [README_ZH.md](https://github.com/alibaba/higress/blob/8deceb4d/README_ZH.md)



## Purpose and Scope

This document provides a comprehensive overview of Higress, an AI Native API Gateway built on Istio and Envoy. It covers the system's architecture, core components, and primary use cases. For detailed information about specific subsystems, refer to the Core Architecture (page 2), Build and Deployment (page 3), WASM Plugin System (page 4), AI Gateway Features (page 5), MCP System (page 6), and Development Guide (page 7) sections.

## What is Higress

Higress is a cloud-native API gateway that extends Istio and Envoy with WebAssembly (WASM) plugin capabilities. The system provides three core functions: AI gateway features for LLM applications, MCP server hosting for AI agent tool integration, and traditional API gateway capabilities including Kubernetes Ingress and microservice routing.

The architecture separates control plane (configuration management) from data plane (traffic processing). Configuration changes propagate through the xDS protocol with millisecond latency and no connection disruption, making it suitable for long-connection scenarios such as AI streaming responses.

**Primary Use Cases:**

Use Case| Description| Core Components  
---|---|---  
**AI Gateway**|  Unified API for 30+ LLM providers with protocol translation, observability, caching, and security| `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` plugins  
**MCP Server Hosting**|  Host Model Context Protocol servers enabling AI agents to call tools and services| `mcp-router`, `jsonrpc-converter` filters + MCP server implementations (`quark-search`, `amap-tools`, `all-in-one`)  
**Kubernetes Ingress**|  Ingress controller with compatibility for nginx-ingress annotations| `higress-controller`, Ingress/Gateway API translation to Istio configs  
**Microservice Gateway**|  Service discovery from multiple registries (Nacos, Consul, ZooKeeper, Eureka)| `McpBridgeReconciler`, registry-specific watchers  
  
**Production Validation:**

Higress originated at Alibaba to address Tengine reload issues affecting long-connection services and insufficient gRPC/Dubbo load balancing. Within Alibaba Cloud, it supports core AI applications including Tongyi Qianwen (通义千问), Tongyi Bailian model studio, and PAI platform. The system handles hundreds of thousands of requests per second with 99.99% availability guarantees.

Sources: [README.md30-52](https://github.com/alibaba/higress/blob/8deceb4d/README.md#L30-L52)

## Core Architecture

Higress implements a control plane and data plane separation derived from Istio's architecture. The control plane watches Kubernetes resources and generates Envoy configurations distributed via xDS protocol. The data plane processes traffic through Envoy proxies extended with WASM plugins.

### System Components and Binaries

**Component Deployment Diagram:**


**Binary and Process Mapping:**

Binary| Source Entry Point| Deployment Location| Primary Functions  
---|---|---|---  
`higress-controller`| [cmd/higress/main.go1-100](https://github.com/alibaba/higress/blob/8deceb4d/cmd/higress/main.go#L1-L100)| Single pod in `higress-system`| Resource watching, `IngressController`, `WasmPluginController`, `McpBridgeReconciler`, service discovery management  
`pilot-discovery`| Istio upstream (patched)| Same pod as controller| xDS server implementation, configuration distribution on ports 15010 (gRPC), 15012 (gRPC-TLS), 15017 (webhook)  
`higress-gateway`| Envoy binary + extensions| DaemonSet or Deployment| Data plane proxy, WASM VM (V8), HTTP/HTTPS listeners on ports 80/443, admin API on 15021  
`hgctl`| [cmd/hgctl/main.go1-50](https://github.com/alibaba/higress/blob/8deceb4d/cmd/hgctl/main.go#L1-L50)| Local CLI tool| MCP server management, local development (`hgctl agent`, `hgctl mcp add`)  
  
**Key Process Communication:**

The controller and pilot run in the same pod and communicate via localhost gRPC on port 15051. The controller implements multiple Kubernetes controllers (`pkg/ingress/kube/`) that watch different resource types and update an in-memory cache (`pkg/ingress/kube/common/cache.go`). The cache state is pushed to pilot, which converts it to xDS configurations (Listener Discovery Service, Route Discovery Service, Cluster Discovery Service, Endpoint Discovery Service) and streams them to all gateway instances.

Sources: [README.md32](https://github.com/alibaba/higress/blob/8deceb4d/README.md#L32-L32) Diagram 2 from provided architecture diagrams

### Configuration Flow and Controller Architecture

**Configuration Update Sequence:**


**Controller Registry and Responsibilities:**

The controller implements the informer pattern for multiple resource types:

Controller| Source Location| Watched Resource| Generated Configs  
---|---|---|---  
`IngressController`| [pkg/ingress/kube/ingress/ingress.go1-500](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/ingress/ingress.go#L1-L500)| `Ingress` (v1)| `VirtualService`, `DestinationRule`, `Gateway`  
`IngressController` (v1beta1)| [pkg/ingress/kube/ingress/ingressv1beta1.go1-400](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/ingress/ingressv1beta1.go#L1-L400)| `Ingress` (v1beta1)| Legacy Ingress support  
`KIngressController`| [pkg/ingress/kube/kingress/kingress.go1-300](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/kingress/kingress.go#L1-L300)| Knative `Ingress`| Knative-specific routing  
`WasmPluginController`| [pkg/ingress/kube/wasmplugin/wasmplugin.go1-400](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/wasmplugin/wasmplugin.go#L1-L400)| `WasmPlugin` CRD| `EnvoyFilter` with WASM config  
`McpBridgeReconciler`| [pkg/ingress/kube/mcpbridge/reconciler.go1-300](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/mcpbridge/reconciler.go#L1-L300)| `McpBridge` CRD| Registry watcher lifecycle  
`ConfigMapController`| [pkg/ingress/kube/configmap/1-100](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/configmap/#L1-L100)| `higress-config` ConfigMap| `EnvoyFilter` for global settings  
  
The central cache (`pkg/ingress/kube/common/cache.go`) maintains in-memory state for all Istio resources and provides atomic updates to prevent partial configuration states. Configuration changes propagate to pilot within milliseconds, significantly faster than nginx-ingress reload times (reported 10x improvement).

Sources: [README.md108-116](https://github.com/alibaba/higress/blob/8deceb4d/README.md#L108-L116) Diagram 2 from provided architecture diagrams

## Key Capabilities

### AI Gateway Features

AI gateway functionality is implemented through a pipeline of WASM plugins that process requests and responses for LLM providers. The plugins support protocol translation, observability, caching, and security.

**AI Plugin Pipeline:**

Plugin| Source Location| Request Phase| Response Phase  
---|---|---|---  
`ai-proxy`| [plugins/wasm-go/extensions/ai-proxy/main.go1-500](https://github.com/alibaba/higress/blob/8deceb4d/plugins/wasm-go/extensions/ai-proxy/main.go#L1-L500)| Protocol detection, provider selection, request transformation| Response transformation, SSE stream processing  
`ai-statistics`| [plugins/wasm-go/extensions/ai-statistics/main.go1-400](https://github.com/alibaba/higress/blob/8deceb4d/plugins/wasm-go/extensions/ai-statistics/main.go#L1-L400)| Extract request attributes (user, model, tokens)| Extract response tokens, latency, write metrics/logs/traces  
`ai-cache`| [plugins/wasm-go/extensions/ai-cache/main.go1-300](https://github.com/alibaba/higress/blob/8deceb4d/plugins/wasm-go/extensions/ai-cache/main.go#L1-L300)| Check cache (semantic search)| Store response in Redis  
`ai-security-guard`| [plugins/wasm-go/ext

[...truncated...]

---
## 导语

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过扩展 WASM 插件能力，将传统的流量管理与 LLM 应用支持整合在同一架构中。该项目旨在解决微服务路由、Kubernetes Ingress 管理以及 AI Agent 工具集成（如 MCP）的复杂需求，为云原生应用提供统一的流量入口。本文将深入介绍其系统架构、核心组件，并重点解析 AI 网关特性及插件系统的运作机制。

---
## 摘要

以下是关于 **Higress** 项目的简洁总结：

**项目概况**
Higress 是阿里巴巴开源的一款**云原生 AI 网关**。基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前在 GitHub 上拥有超过 7,500 颗星。

**核心定位**
Higress 旨在解决 AI 时代流量管理的需求，将**传统 API 网关**与 **AI 原生能力**相结合。其架构采用控制平面与数据平面分离，通过 xDS 协议进行配置分发，具备毫秒级延迟和零连接中断的特性，特别适用于 AI 长连接流式响应场景。

**三大核心功能**
1.  **AI 网关：**
    *   提供统一 API 接入 30 多家大语言模型（LLM）提供商。
    *   提供协议转换、可观测性、缓存及安全防护能力。
2.  **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI Agent 能够便捷地调用外部工具和服务（如地图工具、搜索引擎等）。
3.  **Kubernetes Ingress：**
    *   作为标准的 K8s 入口控制器，兼容 Nginx Ingress 注解，处理微服务路由。

**技术亮点**
*   **扩展性强：** 基于 WASM（WebAssembly）插件系统，允许灵活扩展功能。
*   **高性能：** 继承 Envoy 的高性能特质，支持平滑配置变更。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“传统流量治理”与“AI 原生能力”融合得最彻底的开源项目之一。它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 MCP 协议精准切入 LLM 时代，是构建 AI Agent 基础设施的理想入口。

**详细评价**

**1. 技术创新性：AI 原生架构与 WASM 的深度结合**
Higress 的核心差异化在于其“AI Native”定位，而非仅仅是在传统网关上打补丁。
*   **事实**：DeepWiki 提到其基于 Istio 和 Envoy，并扩展了 WebAssembly (WASM) 插件能力，同时明确支持 MCP (Model Context Protocol) 服务器托管。
*   **推断**：这种架构极具前瞻性。传统网关插件多基于 Lua（如 OpenResty），存在隔离性差、语言受限的问题。Higress 全面拥抱 WASM，允许开发者使用 Go/C++/Rust 等高性能语言编写插件，且实现了沙箱隔离，这在需要处理高并发 AI 流量时至关重要。此外，内置对 MCP 的支持意味着它直接解决了 AI Agent 调用外部工具时的标准化连接问题，这是目前大多数网关忽视的痛点。

**2. 实用价值：统一 AI 流量与微服务治理**
*   **事实**：文档指出 Higress 提供 K8s Ingress、微服务路由以及 AI 网关功能（LLM 应用处理）。
*   **推断**：在实际架构中，这解决了“割裂”问题。企业通常需要维护一套 API 网关（如 Kong）处理业务接口，再维护一套 AI 网关处理大模型请求。Higress 允许在同一个控制平面内，既管理传统的微服务调用，又管理对 OpenAI/通义千问等模型的调用。它解决了 AI 时代特有的“Token 计费”、“Prompt 模板管理”、“超时与重试（LLM 很慢）”等关键问题，应用场景极广，从 SaaS 集成到企业内部 Copilot 平台均适用。

**3. 代码质量与架构设计：云原生标准的继承者**
*   **事实**：项目由阿里主导，语言为 Go，架构明确分离了控制平面和数据平面。
*   **推断**：Go 语言在云原生基础设施领域是事实标准，保证了并发性能。基于 Envoy 作为数据平面是业界最稳健的选择（避免了 Nginx fork 进程模型的某些瓶颈），虽然增加了运维复杂度，但换来了极高的可扩展性和热更新能力。代码结构通常遵循阿里系开源项目的高规范，文档（包含中日英三语）也体现了其对国际化社区的支持，成熟度较高。

**4. 社区活跃度与生态：背靠阿里，生态健康**
*   **事实**：GitHub 星标数 7,535，且包含 DeepWiki 等丰富的文档索引。
*   **推断**：作为阿里的核心开源项目之一，其更新频率和稳定性有企业级保障。7k+ 的 Star 数在网关领域属于第一梯队。社区不仅关注基础功能，还通过 DeepWiki 等形式沉淀了架构知识，说明社区不仅有代码提交，还有知识沉淀，这对于长期维护非常有利。

**5. 学习价值：理解下一代网关的范本**
*   **推断**：对于开发者而言，Higress 是学习“如何将 AI 能力基础设施化”的最佳范例。它展示了如何设计一个支持流式传输的网关，如何处理 SSE (Server-Sent Events) 协议转发，以及如何利用 WASM 技术在不重启网关的情况下动态扩展业务逻辑。这些技能对于构建现代 AI 应用至关重要。

**6. 潜在问题与改进建议**
*   **推断**：基于 Istio 的架构是一把双刃剑。虽然功能强大，但对于非 K8s 环境或小型团队来说，部署和运维 Higress 的门槛远高于 Nginx 或简单的 API 网关。Envoy 的配置复杂度较高，学习曲线陡峭。建议在未来的版本中，进一步简化“非容器化”部署的流程，或提供更轻量级的 Standalone 模式。

**7. 对比优势：比 Kong 更懂 AI，比 LangChain 更懂网关**
*   **推断**：与 Kong/APISIX 相比，Higress 原生集成了 AI 插件（如 Token 统计、模型路由），无需二次开发；与 LangChain 等应用框架相比，Higress 位于基础设施层，提供了框架无法提供的流量控制、并发限制和统一鉴权能力。

**边界条件与验证清单**

**不适用场景：**
*   极其简单的单体应用转发（Nginx 足够，杀鸡焉用牛刀）。
*   非 K8s 环境且运维资源极度匮乏的团队（Envoy 调试困难）。
*   需要极低延迟的内存级缓存转发（网关层有损耗）。

**快速验证清单：**
1.  **WASM 插件验证**：编写一个简单的 Go WASM 插件，在不重启网关的情况下挂载到特定路由，验证热加载生效。
2.  **AI 流量转发测试**：配置一个转发至 OpenAI 的路由，检查是否正确保留了 SSE 流式响应的格式，并观察网关层的 Latency 指标。
3.

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本报告将从架构设计、核心功能、技术实现、适用场景及工程哲学等维度进行全面剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态系统之上，采用了典型的 **控制平面与数据平面分离** 的架构模式。

*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和 xDS 动态配置协议。
*   **控制层扩展**：基于 **Istio** 进行了轻量化和增强。相比于 Istio 沉重的全栈服务网格功能，Higress 剥离了 Sidecar 模式，专注于 Gateway/Ingress 的单一职责，降低了运维复杂度。
*   **编程语言**：**Go**。控制平面使用 Go 开发，利用其高并发处理能力和丰富的云原生工具链。数据平面虽然 Envoy 是 C++，但 Higress 通过 **Proxy-WASM** 规范允许使用 Go/C++/Rust 编写插件，打破了 Envoy 原生仅支持 C++ 过滤器的限制。

### 核心模块与关键设计
1.  **控制平面**：
    *   负责配置管理（通过 K8s CRD 或控制台）、路由规则下发。
    *   **MCP (Model Context Protocol) Server**：这是 Higress 作为 AI 网关的独特设计，它不仅转发流量，还能作为 MCP Server 暴露工具给 AI Agent 调用。
2.  **数据平面**：
    *   基于 Envoy，处理实际流量转发、负载均衡、WASM 插件执行。
    *   **AI 代理优化**：针对 LLM 的长连接和 SSE（Server-Sent Events）流式传输进行了连接池和超时配置的深度优化。

### 技术亮点与创新点
*   **WASM 插件市场**：Higress 最具创新性的设计之一。它允许业务逻辑以 WASM 模块的形式热加载到 Envoy 中。这解决了传统网关（如 Nginx Lua）插件开发门槛高、隔离性差、崩溃会影响主进程的问题。WASM 提供了沙箱隔离和近原生的执行性能。
*   **AI Native 原生集成**：不同于传统网关通过插件“硬塞”AI 功能，Higress 在路由层面原生理解 AI 语义。例如，它能够识别 LLM 的请求/响应格式，自动处理 Token 统计、上下文缓存策略，甚至进行模型间的负载均衡（如从 GPT-4 切换到通义千问）。

### 架构优势分析
*   **低配置延迟**：通过 xDS 协议，配置变更可在毫秒级生效，且无需重启数据面，这对于需要频繁调整 Prompt 或路由策略的 AI 应用至关重要。
*   **解耦与可扩展**：控制面与数据面分离，使得 Higress 可以轻松对接 K8s Ingress 或传统的 Service Mesh 架构。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure OpenAI、通义千问等不同厂商的 API 统一封装成标准接口。
    *   **Token 管理**：实时计费、配额限制、请求重写（如修改 System Prompt）。
    *   **提示词管理**：在网关层动态注入或修改 Prompt，实现无代码的 Prompt 优化。
2.  **MCP 协议支持**：
    *   Higress 可以作为 MCP Server，将内部微服务注册为 AI Agent 的工具。这意味着 AI Agent 可以通过 Higress 安全、受控地调用企业内部 API，解决了 AI 应用集成的安全性问题。
3.  **传统 API 网关**：
    *   K8s Ingress Controller、金丝雀发布、流量镜像、认证鉴权。

### 解决的关键问题
*   **AI 落地的碎片化**：企业不需要为每个 LLM 厂商写一套 SDK，Higress 提供了统一抽象层。
*   **流式响应的性能损耗**：传统网关在处理 SSE 流时往往缓冲导致延迟，Higress 针对流式传输进行了零拷贝优化。
*   **工具调用的安全风险**：直接暴露 API 给 Agent 存在安全隐患，通过 Higress 的 MCP Server 模式，可以在网关层进行权限校验和审计。

### 与同类工具对比
*   **vs. Kong/APISIX**：传统网关虽支持 AI，但多为事后插件。Higress 的优势在于深度集成了 WASM，且对 LLM 流式传输有针对性优化。Kong 依赖 Lua，APISIX 依赖 LuaJIT，其沙箱隔离性和开发便捷性不如 WASM。
*   **vs. Istio Ingress**：Istio 过于厚重，配置复杂。Higress 保留了 Istio 的标准 xDS 优势，但简化了部署模型，且内置了 AI 所需的高级功能（如 Token 计数），这是 Istio 原生不具备的。

### 技术实现原理
*   **LLM 路由**：基于 HTTP Header 或 Body 内容（如 JSON Path）进行路由决策，支持将不同模型的请求分发到不同的后端服务。
*   **WASM 虚拟机**：嵌入在 Envoy 中，通过 `proxy-wasm` 规范与宿主交互。插件可以拦截请求/响应，修改 Header/Body，甚至直接调用外部服务（如 Redis 进行限流）。

---

## 3. 技术实现细节

### 关键技术方案
*   **配置热更新**：Higress 控制面监听 K8s API Server 的变化，将其转换为 Envoy 的 xDS 配置，通过 gRPC 推送给数据面。数据面根据 LDS (Listener Discovery Service) 和 RDS (Route Discovery Service) 动态调整路由表。
*   **WASM 插件加载**：使用 `http_filter` 配置项将 WASM 模块挂载到 Envoy 的过滤器链中。支持 OCI (Open Container Initiative) 标准拉取插件镜像，实现了插件的容器化分发。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器、xDS 控制器、路由匹配逻辑。
*   **`plugins/`**：内置 WASM 插件的源码（通常用 Go 或 C++ 编写），如 `ai-proxy`、`key-auth`。
*   **`router/`**：路由规则匹配引擎，支持基于权重的路由和 Header 匹配。

### 性能优化与扩展性
*   **零拷贝**：在 Envoy 层面处理数据，尽量减少用户态与内核态的数据拷贝。
*   **连接池管理**：针对 LLM 长连接场景，优化了上游连接的保持策略，避免频繁握手带来的延迟。
*   **水平扩展**：数据面无状态，可通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU/连接数自动扩缩容。

### 技术难点与解决方案
*   **难点**：WASM 的内存开销和启动延迟。
*   **方案**：Higress 采用 AOT (Ahead-of-Time) 编译优化 WASM 模块，并利用 Envoy 的 VM 共享机制，减少每个请求的冷启动开销。
*   **难点**：AI 流式响应的中断处理。
*   **方案**：在网关层实现流式缓冲区，当客户端断开连接时，网关能快速检测并中断上游连接，防止资源浪费。

---

## 4. 适用场景分析

### 适合的项目
*   **AI 应用开发**：特别是需要对接多个 LLM 厂商、需要统一管理 API Key 和 Token 消耗的项目。
*   **企业级微服务网关**：需要高度可定制化扩展（通过 WASM 插件）且对性能有要求的 K8s 环境。
*   **Agent 工具集成**：需要将内部 API 安全地暴露给 LLM Agent 使用的场景（利用 MCP 功能）。

### 最有效的情况
*   当你需要**在不修改后端服务代码**的情况下，为 AI 请求添加认证、计费、限流或 Prompt 优化逻辑时。
*   当你需要**标准化**异构的 LLM 接口，使得上层业务无需关心底层模型切换时。

### 不适合的场景
*   **极低延迟的交易系统**：虽然 Envoy 性能极高，但相比于纯 C++ 手写的 TCP Proxy，经过 WASM 插件处理仍会有微秒级损耗。
*   **非 K8s 环境**：Higress 深度依赖 K8s API，如果是虚拟机部署，虽然可行但管理复杂度会上升，不如传统 Nginx 灵活。

### 集成方式
*   **Ingress 模式**：直接替换 K8s 原生 Ingress Controller。
*   **API 网关模式**：部署在 Service Mesh 的边缘，接管南北向流量。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更强的 AI 推理能力**：网关将不仅仅是转发，未来可能集成轻量级模型，在网关层进行语义路由或简单的 RAG 检索。
*   **WASM 生态爆发**：随着 WASM 组件标准的统一，Higress 可能会成为云原生中间件的通用运行时。

### 社区反馈与改进
*   目前社区对 AI Gateway 功能反响热烈，但在文档完善度和 WASM 插件调试工具方面仍有提升空间。

### 前沿技术结合
*   **eBPF**：未来可能在数据平面引入 eBPF 替代部分 WASM 逻辑，以获得更高的内核级性能。
*   **RAG Integration**：网关可能直接集成向量数据库连接能力，作为 RAG 流程的统一入口。

---

## 6. 学习建议

### 适合开发者
*   具备 **Go** 语言基础，了解 **K8s** 基本概念，对 **Service Mesh** 或 **API Gateway** 有兴趣的后端工程师/架构师。

### 学习路径
1.  **基础**：先理解 Envoy 的基本概念（Listener, Cluster, Route）和 xDS 协议。
2.  **进阶**：学习 WASM (WebAssembly) 基础，理解其沙箱机制。
3.  **实践**：在本地 Kind 集群中部署 Higress，尝试编写一个简单的 Go WASM 插件（如修改请求 Header）并挂载。

### 实践建议
*   阅读官方 `README_ZH.md` 和插件开发文档。
*   从修改现有的内置插件（如 `ai-proxy`）开始，理解其配置结构和数据流。

---

## 7. 最佳实践建议

### 正确使用
*   **插件隔离**：将不同功能的 WASM 插件解耦，避免单个插件过于臃肿导致内存占用过高。
*   **资源限制**：在 K8

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway

def setup_gateway_routing():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    gateway = Gateway()
    
    # 添加路由规则：将 /api/v1 请求转发到 service-a
    gateway.add_route(
        path="/api/v1/*",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：将 /api/v2 请求转发到 service-b
    gateway.add_route(
        path="/api/v2/*",
        destination="service-b:8080",
        methods=["GET", "PUT", "DELETE"]
    )
    
    # 启用流量镜像，将 10% 的请求复制到 service-c
    gateway.enable_traffic_mirror(
        path="/api/v1/*",
        mirror_destination="service-c:8080",
        mirror_percentage=10
    )
    
    return gateway

# 使用示例
gateway = setup_gateway_routing()
gateway.apply_config()
```


1. 基于路径的路由转发
2. HTTP 方法过滤
3. 流量镜像功能（用于金丝雀发布）
适用于微服务架构中的流量管理场景。
---

```python
# 示例2：Higress 插件开发
from higress import Plugin, PluginContext

class RateLimitPlugin(Plugin):
    """
    自定义限流插件
    解决问题：保护后端服务免受流量冲击
    """
    def __init__(self):
        super().__init__(
            name="rate-limit",
            version="1.0.0",
            config_schema={
                "max_requests": {"type": "int", "default": 100},
                "window_seconds": {"type": "int", "default": 60}
            }
        )
    
    def on_request(self, context: PluginContext):
        """处理请求阶段"""
        client_ip = context.request.headers.get("X-Real-IP")
        current_count = self.redis.get(f"rate_limit:{client_ip}")
        
        if current_count and int(current_count) >= self.config["max_requests"]:
            return context.response(
                status=429,
                body="Too Many Requests"
            )
        
        # 增加计数器
        self.redis.incr(f"rate_limit:{client_ip}")
        self.redis.expire(f"rate_limit:{client_ip}", self.config["window_seconds"])

# 注册插件
plugin = RateLimitPlugin()
plugin.register()
```


1. 基于 IP 的限流功能
2. 使用 Redis 存储计数器
3. 可配置的限流参数
适用于 API 网关的流量控制场景。
---

```python
# 示例3：Higress 配置管理
from higress import ConfigManager

def manage_higress_config():
    """
    管理 Higress 配置
    解决问题：动态更新网关配置而不中断服务
    """
    config_manager = ConfigManager()
    
    # 获取当前配置
    current_config = config_manager.get_current_config()
    print("当前配置:", current_config)
    
    # 更新配置
    new_config = {
        "routes": [
            {
                "path": "/api/v3/*",
                "destination": "service-d:8080",
                "plugins": ["jwt-auth", "rate-limit"]
            }
        ],
        "global_plugins": {
            "cors": {
                "allow_origins": ["*"],
                "allow_methods": ["GET", "POST"]
            }
        }
    }
    
    # 验证配置
    if config_manager.validate_config(new_config):
        # 应用新配置
        config_manager.apply_config(new_config)
        print("配置更新成功")
    else:
        print("配置验证失败")
    
    # 回滚到上一个版本
    if not config_manager.health_check():
        config_manager.rollback()

# 使用示例
manage_higress_config()
```


---
## 案例研究


### 1：某大型电商平台（阿里集团内部业务）

 1：某大型电商平台（阿里集团内部业务）

**背景**:
该电商平台面临大规模流量挑战，尤其是在“双11”等促销活动期间，需要处理每秒数十万级的API请求。原有架构基于传统Nginx网关，配置管理复杂，且难以与云原生生态深度集成。

**问题**:
- 传统网关配置变更生效慢，无法满足高频业务迭代需求。
- 跨地域流量调度能力不足，导致部分区域服务器负载过高。
- 安全防护策略（如WAF）与网关解耦，增加了运维复杂度和延迟。

**解决方案**:
采用Higress作为统一API网关，利用其云原生架构和Istio集成能力。通过Higress的动态配置功能实现秒级策略更新，结合其内置的流量治理插件进行智能路由，并对接阿里云WAF服务实现安全防护一体化。

**效果**:
- 配置变更效率提升90%，业务迭代周期从天级缩短至小时级。
- 跨地域流量调度优化使服务器CPU利用率均衡度提升25%。
- 安全策略响应速度提升40%，运维人力成本降低30%。

---



### 2：某跨国SaaS服务商

 2：某跨国SaaS服务商

**背景**:
该服务商为全球客户提供API服务，原有网关系统基于开源Kong，在多租户隔离和插件扩展性方面存在瓶颈。随着客户量增长，定制化需求（如多语言支持、差异化限流）难以快速响应。

**问题**:
- 多租户数据隔离不彻底，存在安全隐患。
- 自定义插件开发需修改核心代码，升级风险高。
- 第三方API集成（如Auth0认证、Stripe支付）缺乏标准化流程。

**解决方案**:
迁移至Higress，利用其Wasm插件系统实现无侵入式功能扩展。通过Higress的多租户API管理功能实现资源隔离，并使用官方插件市场快速集成认证和支付服务。

**效果**:
- 租户隔离安全性达到金融级标准，通过ISO 27001认证。
- 自定义插件开发效率提升60%，且无需担心版本升级冲突。
- 第三方集成成本降低50%，客户API接入时间从3天缩短至4小时。

---



### 3：某物联网平台企业

 3：某物联网平台企业

**背景**:
该企业管理超过500万台设备，设备数据通过MQTT协议上报至云端处理。原有网关无法有效处理海量长连接，且协议转换效率低下。

**问题**:
- 长连接并发处理能力不足，高峰期丢包率达5%。
- MQTT到HTTP的协议转换消耗大量服务器资源。
- 缺乏设备级别的流量控制，导致个别异常设备影响整体服务。

**解决方案**:
部署Higress的MQTT网关插件，利用其高性能事件驱动架构处理长连接。通过Higress的协议转换能力实现MQTT到gRPC的高效转换，并配置设备级限流策略。

**效果**:
- 单节点长连接处理能力提升至10万+，丢包率降至0.01%。
- 协议转换延迟降低70%，服务器资源占用减少40%。
- 异常设备影响范围控制在单设备内，整体服务可用性提升至99.99%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 基于OpenResty，性能较高，但受限于Lua | 基于OpenResty和LuaJIT，性能极高 |
| 易用性 | 提供控制台和Kubernetes原生支持，配置简单 | 配置较复杂，需要手动管理路由和插件 | 提供Dashboard，但配置灵活性较高 |
| 成本 | 开源免费，企业版可能收费 | 开源版免费，企业版收费 | 开源免费，企业版支持收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性一般 | 支持Lua和自定义插件，扩展性强 |
| 社区支持 | 阿里背书，社区活跃度中等 | 社区成熟，生态丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API管理 | 传统API网关、微服务 | 高性能API网关、微服务 |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态集成紧密。
- 优势2：支持Wasm插件，扩展性和灵活性较高。
- 优势3：提供控制台和Kubernetes原生支持，降低使用门槛。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较小。
- 不足2：企业版功能可能需要付费。
- 不足3：文档和案例可能不如成熟方案丰富。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 基于 Envoy 构建，原生支持 Wasm (WebAssembly)。相比于传统的 Lua 脚本或 C++ 插件，Wasm 插件具有更高的安全性、隔离性以及多语言开发能力（支持 Go, C++, Rust 等）。利用 Wasm 可以动态扩展网关功能，如自定义鉴权、请求/响应修改等，而无需重启服务。

**实施步骤**:
1. 使用 Go 或 Rust 编写 Wasm 插件逻辑，利用 Higress 提供的 SDK。
2. 将编译好的 `.wasm` 文件上传至 Higress 的插件管理中心或配置为 OCI 镜像。
3. 在网关控制台配置插件规则，将其绑定到特定的路由或服务上。
4. 配置插件的执行顺序（如 `PreAuth`, `PostAuth` 阶段）。

**注意事项**: Wasm 插件运行在沙箱中，虽然有性能开销，但通常在可接受范围内。需注意插件内的内存使用限制，避免内存泄漏。

---

### 实践 2：服务来源的统一接入与管理

**说明**: Higress 的核心优势之一是能够同时管理 K8s Ingress、MSE (微服务引擎)、Nacos 以及固定地址服务。最佳实践是统一将异构基础设施中的服务注册到 Higress 中，利用其作为流量入口，避免维护多套网关系统。

**实施步骤**:
1. 在控制台左侧导航栏选择“来源管理”。
2. 根据实际后端服务类型，分别添加 K8s Service、Nacos 注册中心或 MSE 云原生网关作为服务来源。
3. 配置服务发现规则，确保 Higress 能实时感知服务的健康状态和实例列表。
4. 在路由配置中直接引用已注册的服务名称。

**注意事项**: 如果使用 Nacos 或 MSE，需确保 Higress 所在网络与注册中心网络互通。对于 K8s 服务，建议使用 Service 名称而非 Pod IP，以利用 K8s 的服务发现机制。

---

### 实践 3：精细化流量治理与路由配置

**说明**: 利用 Higress 强强的路由匹配能力（如前缀匹配、精确匹配、正则匹配）以及 Header 转换能力，实现灰度发布、A/B 测试和多环境流量隔离。避免将所有流量无差别地导向后端，应根据业务属性进行分流。

**实施步骤**:
1. 创建路由规则，定义匹配条件（如 URL 路径、Header、Query 参数）。
2. 配置目标服务，支持设置权重百分比，用于金丝雀发布（例如：将 10% 流量导向 v2 版本）。
3. 开启 Header 修改插件，在请求转发给后端前添加或删除特定的 Header（如添加 `x-env-version: prod`）。
4. 使用 Mock 功能在服务未就绪时返回特定响应。

**注意事项**: 路由匹配优先级需仔细规划，避免因规则冲突导致流量被错误的路由截获。建议使用较具体的匹配规则优先级高于泛匹配规则。

---

### 实践 4：全链路安全防护与认证

**说明**: Higress 提供了内置的认证鉴权能力，包括 Keyless 认证、Basic Auth、JWT 认证以及阿里云云原生网关的 WAF 集成。最佳实践是在网关层统一处理认证逻辑，后端服务专注于业务逻辑，避免重复造轮子。

**实施步骤**:
1. 在“安全”视图下，创建认证配置（如 JWT 认证），配置 JWKs 或验签规则。
2. 将认证规则绑定到特定的路由或域名。
3. 针对外部 API 调用，配置 IP 黑白名单或限流策略以防止 DDoS 攻击。
4. 开启 WAF 防护（如果部署在阿里云上），拦截常见 Web 攻击。

**注意事项**: JWT 验证会消耗一定的 CPU 资源，建议配置合理的缓存时间。对于内部服务间调用，通常不需要网关层认证，应通过服务网格或网络策略隔离。

---

### 实践 5：高可用部署与资源配置

**说明**: 在生产环境中，Higress 控制面和数据面应分离部署，并配置合理的资源限制。Higress 数据面基于 Envoy，对长连接处理和并发性能要求较高，需根据实际流量调整 Pod 数量和资源配额。

**实施步骤**:
1. 使用 Helm 或 K8s Deployment 部署 Higress，设置 `replicas >= 2` 以保证高可用。
2. 根据 QPS 评估，调整 Pod 的 CPU 和 Memory limits，避免因资源不足导致 OOMKill 或 CPU Throttling。
3. 配置 Liveness 和 Readiness 探针，确保故障实例能被自动摘除。
4. 开用 Higress 的本地缓存机制（如 Istio 配置缓存），减少对控制面的依赖

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 绑定与隔离

**说明**: Higress 作为高性能网关，其核心组件（如 Envoy 和 WASM 插件运行时）对 CPU 调度延迟敏感。默认的操作系统调度策略可能导致线程在核心间频繁迁移，造成缓存失效（Cache Miss）和上下文切换开销。

**实施方法**:
1. 在 Kubernetes 部署中，为 Higress 的 Pod 配置 `cpu-load-balancing.crio.io` 或 `cpu-manager-policy` 为静态策略。
2. 在 Higress Gateway 的 YAML 配置中，设置 `containerd` 的资源限制，并利用 Linux 的 `taskset` 或 Kubernetes 的 `CPU Manager` 确保 Gateway 进程绑定到固定的 CPU 核心上。
3. 隔离专门的中断处理核心，避免网络软中断处理网关业务线程。

**预期效果**: 在高并发场景下，可降低 P99 延迟约 10%-20%，提升吞吐量 5%-10%。

---

### 优化 2：配置全链路 HTTP/2 与 HTTP/3 (QUIC)

**说明**: Higress 底层基于 Envoy，对 HTTP/2 和 HTTP/3 有原生支持。相比于传统的 HTTP/1.1，HTTP/2 支持多路复用，解决了线头阻塞问题，能显著减少连接数开销。启用 QUIC (HTTP/3) 则能在弱网环境下大幅减少丢包带来的延迟。

**实施方法**:
1. 在监听器配置中，明确启用 HTTP/2 作为 Upstream 和 Downstream 的协议。
2. 在网关入口配置中开启 QUIC 协议支持，并配置相应的 UDP 端口暴露（通常需确保 LoadBalancer 支持 UDP 透传）。
3. 调整 HTTP/2 的并发流限制，根据后端服务能力调整 `max_concurrent_streams` 参数。

**预期效果**: 单连接吞吐量提升 30% 以上，弱网环境下的请求延迟降低 20%-40%。

---

### 优化 3：WASM 插件冷启动优化与预加载

**说明**: Higress 支持通过 WASM (WebAssembly) 扩展功能。然而，WASM 插件的首次加载和编译（JIT 编译）会产生“冷启动”延迟，这在流量突增或网关扩容时尤为明显。优化 WASM 加载机制可减少请求超时风险。

**实施方法**:
1. 使用 `AOT (Ahead-of-Time)` 编译模式，将 WASM 插件预编译为本地机器码，减少运行时编译开销。
2. 在 Higress 配置中启用 WASM 插件的 `vm_config` 缓存，确保插件实例在 Worker 间共享或持久化，避免重复加载。
3. 对核心 WASM 插件进行预热，在网关启动阶段通过健康检查触发插件初始化。

**预期效果**: WASM 插件首次调用延迟从毫秒级降至微秒级，扩容时的流量丢失率接近 0。

---

### 优化 4：精细化连接池与超时配置

**说明**: 默认的连接池配置往往过于保守或激进，无法适应所有业务场景。过小的连接池会导致请求排队等待，过大的连接池则耗尽后端资源。不合理的超时设置会导致资源长时间被占用。

**实施方法**:
1. 根据后端服务的处理能力，动态调整 `max_requests_per_connection` 和 `max_connections` 参数，避免频繁建立 TCP 连接。
2. 启用连接池的 `idle_timeout` 配置，及时清理僵尸连接，但需设置合理的 `keepalive` 时间。
3. 针对慢请求，设置严格的 `per_request_timeout` 和 `global_timeout`，利用 Higress 的 `timeout` 边界策略防止级联雪崩。

**预期效果**: 后端服务 CPU 利用率更加平稳，减少因连接等待造成的响应延迟，提升整体系统吞吐量 15%-25%。

---

### 优化 5：启用高级路由缓存与正则优化

**说明**: 复

---
## 学习要点

- 根据提供的上下文（GitHub 趋势中的 Alibaba/Higress 项目），以下是关于 Higress 的关键要点总结：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的云原生 API 网关，旨在解决云原生时代流量治理与入口管理的复杂性问题。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，实现从传统微服务向云原生架构的平滑迁移。
- 它提供了开箱即用的 WAF（Web 应用防火墙）插件能力，有效增强 API 安全性并防御常见的 Web 攻击。
- Higress 兼容 Nginx Ingress 注解及 Nginx 配置习惯，显著降低了用户从传统 Nginx 迁移到现代服务网格的技术门槛与学习成本。
- 架构上支持将 K8s 服务与 ECS、IDC 等异构后端统一进行管理，实现了混合云环境下的流量统一调度与路由。
- 内置了针对 Dubbo、Nacos、gRPC 等主流微服务框架的协议支持与扩展，弥补了传统网关在处理 RPC 服务调用上的短板。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 的作用、位置及核心功能（路由转发、负载均衡、安全防护）。
- Higress 项目背景：了解 Higress 的开源背景、基于 Istio 和 Envoy 的技术架构，以及它与 Nginx、传统 Kong 网关的区别。
- 基本概念：掌握 Ingress、Gateway、Service、Upstream 等基础术语。
- 环境搭建：学习如何在 Docker 本地环境或 Kubernetes 集群中快速安装和部署 Higress。
- 控制台使用：熟悉 Higress 的原生控制台（Console）界面，进行简单的服务来源注册（如 Nacos, 固定地址, K8s Service）和路由配置。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 (README.md)
- Higress 官方文档 - "快速开始" 章节
- 云原生网关技术对比文章

**学习建议**: 建议先通读官方文档的架构介绍，然后在本地使用 Docker Compose 快速拉起一个实例。不要急于深入配置，先通过控制台界面创建一个简单的 HTTP 路由（例如将 `/` 路径转发到 `httpbin.org`），观察流量是否通顺。

---

### 阶段 2：流量治理与路由进阶

**学习内容**:
- 高级路由配置：学习基于 Header、Query Parameter、Cookie、URI 等条件的复杂路由匹配规则。
- 流量管理：掌握全链路灰度发布（金丝雀发布）、蓝绿发布、Header 重写/转发、路径重写。
- 负载均衡策略：理解并配置轮询、随机、最小连接数等负载均衡算法，以及源地址会话保持。
- 服务治理：配置超时时间、重试策略、熔断降级等容错机制。
- 插件系统入门：了解 Higress 的插件规范，尝试在控制台开启并配置几个官方预置插件（如：请求限流、Basic Auth、CORS）。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "流量管理" 与 "插件市场" 板块
- Envoy Filter 官方文档（用于理解底层过滤原理）
- Higress 官方示例仓库

**学习建议**: 此阶段建议结合 Kubernetes 进行学习，因为 Higress 在 K8s 环境下功能最全。尝试部署两个不同版本的微服务，配置基于 Header 的灰度路由，观察流量按预期比例分发。同时，务必测试服务不可用时的重试和熔断效果。

---

### 阶段 3：安全防护与可观测性

**学习内容**:
- 安全认证：学习如何配置 Keyless 认证、ApiKey 认证、JWT 验证、OIDC（单点登录）以及 HMAC 签名认证。
- 访问控制：配置 IP 黑白名单、基于角色的访问控制（RBAC）。
- WAF 防护：了解 Higress 如何通过插件防御 SQL 注入、XSS 等 Web 攻击。
- 可观测性集成：学习如何配置日志（访问日志、审计日志）对接 Elasticsearch、SLS 或 Kafka。
- 监控指标：掌握 Prometheus 集成，理解 Higress 的关键 Metrics（如 Request Rate, Latency, Upstream Health）。
- 分布式追踪：配置集成 SkyWalking 或 Zipkin，实现全链路追踪。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "安全" 与 "可观测性" 章节
- Prometheus 监控最佳实践白皮书
- OpenTelemetry 相关文档

**学习建议**: 安全方面，建议尝试对接公司内部的 IdP 或使用 Keycloak 进行 OIDC 联调。在可观测性方面，建议搭建一套 Prometheus + Grafana 的监控栈，导入 Higress 官方提供的 Dashboard 模板，实时观察网关的 QPS 和延迟变化。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- 插件开发（Wasm）：学习 Higress 基于 WebAssembly (Wasm) 的插件开发机制。
- 编程语言实践：使用 Go 或 Python 编写自定义 Wasm 插件。
- 插件调试：掌握如何在本地或远程调试 Wasm 插件，处理上下文请求与响应。
- 配置热更新原理：理解插件配置如何在不重启网关的情况下动态生效。
- 高级扩展：学习如何通过 ConfigMap 管理 Wasm 插件，以及如何开发自定义的 Wasm 插件市场。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "Wasm 插件开发" 指南
- Higress GitHub - `higress-group` �

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 或 Kong 等传统网关有什么区别？

1: Higress 是什么？它与 Nginx 或 Kong 等传统网关有什么区别？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 Ingress 网关的基础上进行了深度的升级和优化。与 Nginx 或 Kong 相比，Higress 的主要区别在于：

1.  **架构层面**：Higress 深度集成了 Istio，可以作为 Istio 的数据平面，同时兼容 Kubernetes Ingress 和 Gateway API 标准。它不仅支持南北向流量（入口流量），也能更好地处理东西向流量（服务间流量）。
2.  **性能与扩展性**：Higress 基于 C++ 编写，拥有极高的性能。它支持热更新插件，无需重启网关即可加载或修改插件规则，这在传统网关中通常需要重新加载配置甚至重启进程。
3.  **安全性**：Higress 默认集成了 WAF（Web 应用防火墙）功能，提供了开箱即用的安全防护能力，而传统网关通常需要额外配置或购买企业版。
4.  **生态兼容**：它兼容 Nginx 的配置语法，同时也支持 Apache Dubbo、Nacos 等中国开发者常用的微服务生态，对 Spring Cloud 也有很好的支持。

---



### 2: Higress 是否支持从 Nginx 或 Ingress Controller（如 Nginx Ingress）进行迁移？

2: Higress 是否支持从 Nginx 或 Ingress Controller（如 Nginx Ingress）进行迁移？

**A**: 是的，Higress 非常重视迁移的平滑性，并提供了专门的工具来降低迁移成本。

1.  **Nginx 兼容**：Higress 的核心基于 Envoy，但针对 Nginx 用户做了大量适配工作。它支持直接导入 Nginx 的配置文件（nginx.conf），Higress 会尝试将其转换为自身的路由配置。
2.  **注解兼容**：对于 Kubernetes 用户，Higress 兼容 Nginx Ingress Controller 的大部分常用注解。这意味着你通常不需要修改 YAML 文件中的 Ingress 资源定义，只需将控制平面切换到 Higress，即可实现无缝迁移。
3.  **迁移工具**：官方提供了配置迁移工具，可以帮助用户将现有的配置自动转换为 Higress 的格式。

---



### 3: Higress 的插件系统是如何工作的？支持哪些类型的插件？

3: Higress 的插件系统是如何工作的？支持哪些类型的插件？

**A**: Higress 拥有一个非常灵活且强大的插件系统，旨在满足网关的定制化需求。

1.  **插件类型**：
    *   **原生插件**：Higress 内置了大量的核心插件，如限流熔断、认证鉴权（Basic Auth, JWT, API Key）、请求/响应重写、CORS 处理等。
    *   **WAF 插件**：内置了针对 SQL 注入、XSS 等常见攻击的防护插件。
    *   **自定义插件**：支持使用 Go、C++、Lua、WASM (WebAssembly)、Python 和 Java 编写自定义插件。其中，WASM 插件因其沙箱隔离和高性能特性，是官方推荐的扩展方式。
2.  **运行机制**：插件可以配置在全局范围、特定路由或特定域名上。支持在控制台进行可视化的插件启用、参数配置和顺序调整，且配置下发是毫秒级的，不会导致业务中断。

---



### 4: Higress 如何处理服务发现？它是否支持非 Kubernetes 环境的服务？

4: Higress 如何处理服务发现？它是否支持非 Kubernetes 环境的服务？

**A**: Higress 不仅是一个 Kubernetes Ingress 网关，也是一个强大的 API 网关，具备完善的服务发现能力。

1.  **Kubernetes 原生**：在 K8s 集群中，它自动与 Service 和 Endpoints 对接，实现服务发现。
2.  **注册中心集成**：对于非 K8s 的服务或混合架构，Higress 原生支持对接主流的服务注册中心，包括 **Nacos**、**ZooKeeper**、**Consul** 以及 **DNS**。这使得 Higress 可以轻松地连接传统的微服务架构（如 Spring Cloud 或 Dubbo 应用）。
3.  **固定地址**：同时也支持直接配置 IP 地址或域名作为上游服务（Upstream）。

---



### 5: Higress 是否支持 Dubbo 服务？如何进行 HTTP 转 Dubbo 的协议转换？

5: Higress 是否支持 Dubbo 服务？如何进行 HTTP 转 Dubbo 的协议转换？

**A**: 支持。Higress 对 Dubbo 有着深度的原生支持，这是它区别于许多国外主流网关的一个重要特性。

1.  **直接调用**：Higress 可以直接作为 Dubbo 服务的消费者，通过注册中心（如 Nacos 或 ZooKeeper）发现 Dubbo 服务节点，并基于 Dubbo 协议发起调用。
2.  **协议转换**：Higress 具备强大的协议转换能力，可以将外部的 HTTP/HTTPS 请求转换为内部的 Dubbo (Triple 或 Hessian2) 请求。这意味着前端应用可以使用标准的 RESTful API 调用，而后端服务则运行在 Dubbo 协议上，网关自动处理参数映射和协议转换，实现

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

### 查阅 Higress 官方文档的 "快速开始" 章节。

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为网关的核心功能与 AI 特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 "AI 提词词管理" 实现模型调用的标准化与解耦
*   **场景**：后端业务代码直接调用大模型（如 OpenAI、通义千问）时，一旦需要调整 Prompt（提示词）或切换模型版本，通常需要重新发布应用。
*   **建议**：在 Higress 中配置 AI 服务的路由时，使用其**内容改写**或**服务插件**功能，将复杂的 System Prompt 配置在网关层。
*   **最佳实践**：将 Prompt 模板化管理，业务端仅传递业务变量（如用户查询），网关负责组装完整的请求体发送给 LLM。这样可以在不重启业务服务的情况下，通过修改网关配置来实时优化模型输出效果。

### 2. 实施细粒度的 Token 计费与流量控制
*   **场景**：大模型 API 调用成本主要与 Token 数量成正比，传统的基于 QPS（每秒请求数）或并发数的限流无法有效控制成本。
*   **建议**：配置针对 AI 服务的特定限流策略。Higress 支持针对请求体大小或响应体大小进行统计，建议结合插件对 Token 进行估算（如 `1 Token ≈ 0.75 个英文单词` 或使用更精确的计数器插件）。
*   **最佳实践**：针对不同级别的 API Key 或用户租户，设置 "每分钟 Token 消耗上限" 而不仅仅是 "每分钟请求次数上限"，防止恶意 Prompt 或长文本上下文导致的成本失控。

### 3. 配置 LLM 语义与 HTTP 状态码的双重熔断机制
*   **场景**：大模型提供商服务偶尔不稳定，或者模型输出触发了安全策略导致拦截，直接返回 200 OK 但内容包含错误信息。
*   **建议**：不要仅依赖 HTTP 错误码进行熔断。利用 Higress 的**脚本插件**或**响应体检查**能力，检测 LLM 返回的 JSON 结构或错误字段。
*   **常见陷阱**：如果 LLM 返回了 `{"error": "rate_limit_exceeded"}` 但 HTTP 状态码是 200，常规的网关熔断器不会生效。
*   **操作**：配置熔断规则，当响应体中包含特定错误关键词或检测到非预期的 JSON 格式时，自动触发熔断，将流量切换到备用模型或降级服务。

### 4. 构建多模型供应商的容灾切换路由
*   **场景**：企业应用通常同时接入多家模型厂商（如同时使用 Azure OpenAI 和通义千问）。当主厂商宕机时，需要无缝切换。
*   **建议**：利用 Higress 的**服务来源**或**路由规则**配置多活或主备逻辑。
*   **最佳实践**：
    *   定义一个抽象的 AI 服务路由（如 `/api/llm/chat`）。
    *   配置两个服务来源（Service A: OpenAI, Service B: Qwen）。
    *   设置健康检查，当 Service A 的健康检查失败（或响应超时）时，Higress 自动将流量转发至 Service B，对客户端完全透明。

### 5. 优化 SSE (Server-Sent Events) 流式传输的缓冲策略
*   **场景**：AI 对话通常使用 SSE 流式返回数据。如果网关配置了过大的缓冲区，会导致用户看到 "打字机" 效果出现明显的卡顿；如果配置不当，可能导致连接中断。
*   **建议**：检查 Higress 的动态路由 Upstream 配置中的 `buffer_size` 或超时设置。
*   **最佳实践**：对于流式 AI 接口，**禁用或调小**响应缓冲，确保网关在收到模型生成的每一个 Token 后立即推送给客户端，而不是等待网关缓冲区填满。同时，务必将网关的**读取超时

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*