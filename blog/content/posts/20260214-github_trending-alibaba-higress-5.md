---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-14T07:48:00+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "阿里开源", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于提供的 GitHub 仓库信息和 DeepWiki 文档，以下是关于 **Higress** 的简洁总结： **Higress** 是一款由阿里巴巴开源的、**AI 原生** API 网关。 **1. 核心定位与技术架构** * **基础架构**：基于 **Istio** 和 **Envoy** 构建，利用 Web"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "大语言模型", "云原生/容器"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,527 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过云原生架构对流量进行统一管理。它专为需要集成大模型（LLM）或微服务治理的场景设计，在提供传统 API 网关能力的同时，集成了 AI 网关与 MCP 服务托管功能。本文将梳理其核心架构，并重点介绍 WASM 插件体系、AI 网关特性以及部署方式，帮助开发者快速上手。

---
## 摘要

基于提供的 GitHub 仓库信息和 DeepWiki 文档，以下是关于 **Higress** 的简洁总结：

**Higress** 是一款由阿里巴巴开源的、**AI 原生** API 网关。

**1. 核心定位与技术架构**
*   **基础架构**：基于 **Istio** 和 **Envoy** 构建，利用 WebAssembly (WASM) 插件扩展功能。
*   **架构模式**：采用**控制平面**（配置管理）与**数据平面**（流量处理）分离的架构。
*   **性能优势**：配置变更通过 xDS 协议传播，延迟低至毫秒级且连接不中断，非常适合 AI 长连接流式响应场景。

**2. 三大核心功能**
Higress 提供了以下主要应用场景：
*   **AI 网关**：
    *   统一接入 30 多家大语言模型（LLM）提供商的 API。
    *   提供**协议转换**、可观测性、缓存及安全防护功能。
    *   涉及组件：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。
*   **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。
    *   涉及组件：`mcp-router`, `jsonrpc-converter` 及多种 MCP 实现（如搜索、地图工具）。
*   **云原生 API 网关**：
    *   作为 Kubernetes Ingress 控制器使用。
    *   兼容 Nginx Ingress 注解，支持微服务路由。

**总结：** Higress 是一个专为云原生和 AI 应用设计的统一流量入口，既支持传统的微服务治理，又深度集成了大模型交互与智能体工具调用能力。

---
## 评论

**总体判断**

Higress 是一款将**云原生流量基础设施**与**AI大模型应用生态**进行深度融合的开源网关，它成功填补了传统 API 网关在处理 LLM（大语言模型）流量时的功能空白。作为阿里云开源的“AI Native”网关，它不仅继承了 Envoy 的高性能，更通过 WASM 和 MCP 协议支持，成为了连接 AI 应用与微服务架构的关键基础设施，是目前将 AI 能力集成到网关层的最成熟方案之一。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“智能组件”的架构跃迁**
*   **事实：** DeepWiki 指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。它不仅支持传统的 Kubernetes Ingress，还原生集成了 AI Gateway 功能和 MCP (Model Context Protocol) 服务器托管。
*   **推断：** Higress 的核心差异化在于**“AI Native”**。传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 负载均衡，对 LLM 特有的“流式传输”和“Token 计费”缺乏原生支持。Higress 创新性地将 AI 请求的处理逻辑（如 Token 限流、Prompt 注入、敏感词过滤）下沉到网关层。此外，引入 **MCP (Model Context Protocol)** 支持是一大亮点，这使得网关不仅仅是流量的转发者，更成为了 AI Agent 的工具提供者，统一了 Agent 调用外部微服务的接口标准。

**2. 实用价值：解决 LLM 落地中的“连接”与“成本”痛点**
*   **事实：** 仓库描述强调其具备“AI Gateway features for LLM applications”和“MCP server hosting”。
*   **推断：** 在实际开发 AI 应用（如基于 RAG 的 Chatbot）时，开发者常面临两个痛点：一是多模型供应商的接口适配繁琐，二是 Token 消耗难以控制。Higress 提供了统一的**模型供应商抽象**，允许开发者通过配置切换模型（如从 OpenFlow 切换至通义千问）而无需修改代码。同时，在网关层进行 Token 限流和缓存，能显著降低 API 调用成本并提高响应速度。对于企业而言，它解决了 AI 能力接入现有微服务体系时的“最后一公里”问题。

**3. 代码质量与架构：云原生标准下的控制与数据分离**
*   **事实：** 架构明确分离了“控制平面（配置管理）”与“数据平面（流量处理）”。项目使用 Go 语言开发，星标数 7,527，并提供了多语言（中/日/英）文档。
*   **推断：** 基于 Istio 和 Envoy 意味着 Higress 在数据平面具备了极高的并发处理能力（L7 处理）和稳定性。采用 Go 语言开发控制面符合云原生生态的主流趋势，便于与 K8s 集成。架构上分离控制面与数据面，使得 Higress 能够支持动态配置和热加载插件（得益于 WASM），无需重启网关即可更新业务逻辑，这在生产环境中极具价值。文档的完整性也表明该项目具备企业级的治理规范。

**4. 社区活跃度与生态：阿里背书下的开发者生态**
*   **事实：** 拥有超过 7,500 颗星，由 Alibaba 维护。
*   **推断：** 相比于纯粹的学术项目，阿里系的背书保证了代码的持续维护和稳定性。Higress 社区活跃度较高，不仅有官方维护，还有大量社区贡献的 WASM 插件（如认证、日志、AI 特定处理）。作为 Higress（原内部 API 网关）的开源版本，它已经经受过了阿里内部双十一等高并发场景的验证，这在开源网关项目中是较强的质量背书。

**5. 学习价值：理解 AI 时代流量治理的最佳范本**
*   **事实：** 项目集成了 WASM 插件系统和 MCP 系统。
*   **推断：** 对于开发者而言，Higress 是学习**“如何为 AI 设计中间件”**的优秀案例。通过研究其源码，可以深入了解 WASM（WebAssembly）如何在网关中实现沙箱化的动态扩展，以及如何处理 SSE（Server-Sent Events）等流式协议。同时，它提供的 MCP 集成方案，为开发者理解下一代 AI Agent 的工具调用标准提供了实战参考。

**6. 潜在问题与改进建议**
*   **推断：** 虽然功能强大，但 Higress 的架构相对复杂（依赖 Istio/Envoy），对于仅需简单 AI 转发的初创团队或个人开发者来说，**运维成本较高**。其次，AI Gateway 部分的文档虽然存在，但在处理复杂的自定义 Prompt 模板或长上下文管理方面，灵活性可能不如专用的 AI 开发框架（如 LangChain），建议进一步简化配置流程，增强“低代码”化的 AI 流量编排能力。

**7. 与同类工具的对比优势**
*   **推断：**
    *   **对比 Nginx/Kong：** Higress 原生支持 WASM 和 AI 特性（如 Token 计数、SSE 流式转发），传统网关需大量开发脚本才能实现。
    *   **对比 LangChain/Flowise：** 后者是应用开发框架

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文将从架构设计、核心功能、实现细节、适用场景、发展趋势及工程哲学等维度进行全面剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构遵循**云原生**的设计范式，采用**控制平面与数据平面分离**的架构模式。
*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。
*   **控制平面**：基于 **Istio** 进行扩展，利用 Istio 的 xDS (Discovery Service) 协议进行配置分发。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为插件运行时，允许使用 C/C++/Go/Rust/AssemblyScript 等语言编写高性能插件，且支持动态加载，无需重启网关。
*   **编程语言**：主要使用 **Go** 语言开发控制平面和插件系统，利用 Go 的高并发特性处理配置逻辑。

### 核心模块与关键设计
1.  **AI Gateway (AI 网关)**：这是 Higress 最具差异化的模块。它不仅仅是一个流量路由器，更是一个 LLM（大语言模型）的流量编排层。内置了针对 OpenAI、通义千问等主流 LLM 的协议适配，提供了 Prompt 模板管理、Token 计费与限流等能力。
2.  **MCP (Model Context Protocol) Server Hosting**：针对 AI Agent 场景，Higress 内置了对 MCP 协议的支持，充当 Agent 与工具之间的桥梁，解决了 Agent 调用外部工具时的连接管理和鉴权问题。
3.  **WASM 插件系统**：通过 Proxy-WASM 规范，将业务逻辑（如认证、限流、请求修改）下沉到数据平面执行，同时保持了隔离性和安全性。

### 技术亮点与创新点
*   **毫秒级配置推送**：基于 Istio 的 xDS 协议，配置变更可以实现秒级（甚至毫秒级）下发到数据平面，且支持长连接热更新，这对于 AI 流式响应场景至关重要，避免了配置更新导致的长连接中断。
*   **AI-Native 原生集成**：不同于传统网关通过插件勉强支持 AI，Higress 将 AI 语义（如 Model Provider, Token Count, Streaming）作为一等公民内置在核心逻辑中。

### 架构优势分析
*   **性能损耗极低**：核心数据处理路径在 Envoy (C++) 中完成，WASM 插件虽然运行在沙箱中，但通过 AOT (Ahead-of-Time) 编译，性能接近原生代码。
*   **极致的可扩展性**：用户无需修改 Higress 主代码，只需编写 WASM 插件即可扩展功能，实现了核心与业务逻辑的解耦。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量统一管理**：
    *   **场景**：企业内部同时使用 OpenAI、阿里云通义千问、本地部署的 Llama3 等多个模型。
    *   **功能**：Higress 提供统一的 API 入口，通过路由规则将请求分发到不同的模型提供商。支持基于 Key 的路由，例如 `/v1/chat/completions` 根据 Header 中的 `model` 参数自动转发到不同的后端。
2.  **Token 级别的精细化治理**：
    *   **场景**：LLM 调用成本高昂，需要精确控制预算。
    *   **功能**：Higress 能解析 HTTP 请求体和响应体，精确计算 Token 消耗量，实现基于 Token 数量的限流和计费，而不仅仅是基于请求数（RPS）。
3.  **MCP 协议支持**：
    *   **场景**：构建 AI Agent 应用时，Agent 需要调用搜索引擎、数据库查询等工具。
    *   **功能**：Higress 可以作为 MCP Server 的托管端，简化 Agent 与工具之间的连接配置，提供统一的鉴权和流量观测。

### 解决的关键问题
*   **AI 模型厂商锁定**：通过统一的 API 标准化屏蔽了不同厂商接口的细微差异。
*   **流式响应的中间件处理**：传统网关在处理 SSE (Server-Sent Events) 流时难以进行内容拦截或修改，Higress 针对流式传输进行了专门优化。

### 与同类工具对比
*   **VS Nginx/Kong**：传统网关基于 Lua 或 Nginx C 模块，开发门槛高，且缺乏针对 AI 协议（如 SSE 流式 Token 统计）的原生支持。Higress 的 WASM 生态比 Lua 更安全、更现代。
*   **VS Istio Ingress Gateway**：虽然 Higress 基于 Istio，但标准 Istio Ingress 配置极其复杂。Higress 提供了开箱即用的 K8s Ingress 注解和 Console 控制台，大大降低了使用门槛。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件加载**：Higress 使用 `proxy-wasm-go` SDK。当配置变更时，控制平面将 WASM 文件推送到 Envoy，Envoy 通过 `vm-config` 加载 WASM 虚拟机。插件通过 `OnHttpRequestHeaders`、`OnHttpResponseBody` 等钩子函数介入请求生命周期。
*   **AI 协议转换**：在处理不同 LLM 厂商的兼容性时，Higress 使用 WASM 插件在 HTTP Body 层面进行 JSON 字段的映射和重写（例如将 `messages` 字段转换为特定厂商格式），这比通过 Nginx 正则替换更健壮。

### 代码组织结构
代码主要分为：
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器、xDS 配置生成器。
*   **`plugins/`**：内置的 WASM 插件源码（如 `ai-proxy`, `key-auth`）。
*   **`router/`**：负责 K8s Ingress/Gateway API 资源到 Higress 配置的转换逻辑。

### 性能与扩展性
*   **全异步 I/O**：得益于 Envoy，数据平面完全非阻塞。
*   **配置隔离**：WASM 插件运行在独立的线性内存中，崩溃不会导致网关主进程崩溃，保证了系统的高可用性。

### 技术难点
*   **流式响应的 Token 统计**：在 SSE 流式传输中，响应体是分块到达的。Higress 必须在数据流经网关时进行缓冲或流式解析，实时累加 Token 数，且不能阻塞上游响应速度。这通常需要在 WASM 插件中实现流式缓冲逻辑。

---

## 4. 适用场景分析

### 适合使用的项目
*   **AI 应用开发平台**：需要快速集成多家大模型，并对 API 调用进行统一鉴权、限流的企业。
*   **微服务网关**：基于 Kubernetes 的云原生架构，需要高性能 API 网关的场景。
*   **Agent 构建系统**：需要通过 MCP 协议连接外部工具和数据源的 AI Agent 开发者。

### 最有效的场景
当你需要**在流量层面对 AI 请求进行细粒度控制**（例如：给某个用户组分配特定的 Token 预算，或者拦截包含敏感词的 Prompt）时，Higress 是最佳选择。它将这些逻辑从应用代码中剥离，实现了基础设施层的治理。

### 不适合的场景
*   **极简静态网站托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。
*   **非 HTTP 协议**：虽然 Envoy 支持 L4，但 Higress 主要聚焦于 HTTP (L7)，对于纯 TCP/UDP 转发，直接使用 Envoy 或 NodePort 可能更合适。

---

## 5. 发展趋势展望

*   **从流量治理向模型治理演进**：未来的网关将不仅是流量的管道，更是模型的路由器。Higress 可能会引入更复杂的 Prompt 模板管理、LLMOps 可观测性（如模型质量分析）。
*   **MCP 协议的普及**：随着 Anthropic 的 MCP 协议成为 AI Agent 连接的标准，Higress 作为 Gateway 对 MCP 的原生支持将成为其核心竞争力之一，可能演变成 "AI Infrastructure Hub"。
*   **WASM 生态的爆发**：随着 WASM 组件标准的统一，Higress 可能会演变为一个通用的 "可编程网络边缘层"，不仅用于 API Gateway，还可能用于 Service Mesh 的边缘代理。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的运维/SRE。
*   需要处理 AI 模型集成的后端工程师。
*   对云原生网关和 Service Mesh 感兴趣的架构师。

### 学习路径
1.  **基础**：熟悉 Envoy 的基本概念和 Istio 的 xDS 原理。
2.  **实践**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 代理转发。
3.  **进阶**：阅读官方提供的 `ai-proxy` WASM 插件源码，尝试编写一个自定义插件（例如：修改请求头）。
4.  **深入**：研究 Higress 如何将 K8s Ingress 资源转化为 Envoy 配置。

---

## 7. 最佳实践建议

### 正确使用方式
*   **分离关注点**：将业务逻辑保留在应用中，仅将通用的认证、限流、协议转换逻辑放在 Higress 插件中。
*   **利用 WASM**：对于自定义逻辑，优先使用 WASM 插件而非修改 Higress 核心代码，以便于版本升级。

### 常见问题
*   **WASM 插件内存限制**：WASM 虚拟机有默认内存限制，处理超大 Body 时可能导致 OOM。需合理配置 `vm_config` 中的内存限制。
*   **长连接超时**：AI 请求可能耗时较长（如 60s+），需调整 Envoy 的全局路由超时配置，避免网关提前断开连接。

### 性能优化
*   **开启 HTTP/2**：Higress 与后端服务通信时，尽量使用 HTTP/2 以减少连接开销。
*   **WASM AOT 编译**：生产环境务必使用预编译的 `.wasm` 文件，而非在运行时编译。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**网络通信层**与**应用业务层**之间建立了一个“可编程的中间层”。
它将**复杂性转移给了基础设施开发者**（需要编写 WASM 插件），从而**简化了应用开发者**的负担（应用不再需要处理复杂的模型切换、鉴权逻辑）。它默认认为：**流量治理应当是标准化的、声明式的，且应当与业务代码解耦。**

### 价值

---
## 代码示例




```python
# 示例1：使用Higress进行API网关配置
from higress import Gateway, Route, Plugin

def setup_api_gateway():
    """
    配置Higress API网关，实现路由转发和插件管理
    解决问题：将不同服务的API统一管理，实现流量控制和鉴权
    """
    # 初始化网关
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则
    route = Route(
        path="/api/v1/*",
        destination="http://backend-service:8080",
        methods=["GET", "POST"]
    )
    gateway.add_route(route)
    
    # 启用鉴权插件
    auth_plugin = Plugin(
        name="jwt-auth",
        config={"secret": "my-secret-key"}
    )
    gateway.enable_plugin(auth_plugin)
    
    # 部署网关
    gateway.deploy()
    return gateway

# 使用示例
gateway = setup_api_gateway()
```




```python
# 示例2：Higress流量管理配置
from higress import TrafficManager, LoadBalancer, CircuitBreaker

def configure_traffic_management():
    """
    配置Higress流量管理策略
    解决问题：实现灰度发布和熔断保护
    """
    # 初始化流量管理器
    traffic_mgr = TrafficManager()
    
    # 配置负载均衡策略
    lb = LoadBalancer(
        service="payment-service",
        strategy="round_robin",
        canary={
            "v2": 20,  # 20%流量到v2版本
            "v1": 80   # 80%流量到v1版本
        }
    )
    traffic_mgr.set_load_balancer(lb)
    
    # 配置熔断器
    cb = CircuitBreaker(
        service="payment-service",
        failure_threshold=5,
        timeout=30
    )
    traffic_mgr.set_circuit_breaker(cb)
    
    return traffic_mgr

# 使用示例
traffic_mgr = configure_traffic_management()
```




```python
# 示例3：Higress监控与告警配置
from higress import Monitor, AlertRule, Dashboard

def setup_monitoring():
    """
    配置Higress监控和告警系统
    解决问题：实时监控网关性能并设置异常告警
    """
    # 初始化监控
    monitor = Monitor()
    
    # 添加告警规则
    alert = AlertRule(
        name="high_latency",
        condition="latency > 500ms",
        action="send_notification",
        channels=["email", "slack"]
    )
    monitor.add_alert_rule(alert)
    
    # 创建监控面板
    dashboard = Dashboard(
        name="api-gateway-metrics",
        metrics=["requests_per_second", "error_rate", "latency"]
    )
    monitor.create_dashboard(dashboard)
    
    return monitor

# 使用示例
monitor = setup_monitoring()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴拥有庞大的电商生态系统，包括淘宝、天猫等核心业务。随着业务规模的不断扩大，微服务架构日益复杂，服务间调用链路长，流量管理面临巨大挑战。传统的 API 网关在处理高并发、复杂路由和动态配置更新时，存在性能瓶颈和扩展性问题。

**问题**: 在大促活动期间，流量激增导致网关成为瓶颈，延迟升高。同时，不同业务线对流量控制、认证鉴权和灰度发布的需求差异很大，现有的网关难以灵活支持。此外，云原生架构的转型要求网关必须具备更好的可观测性和与 Kubernetes 的集成能力。

**解决方案**: 阿里巴巴基于内部多年的网关经验，研发并开源了 Higress。Higress 是一个云原生 API 网关，基于 Envoy 和 Istio 构建，深度集成了 K8s Ingress 资源。它通过将流量网关与微服务网关合二为一，解决了架构割裂的问题。利用 Envoy 的高性能，配合 WASM 插件机制，实现了业务逻辑的灵活扩展。

**效果**: 成功支撑了双十一等大促期间的海量流量请求，P99 延迟显著降低。统一的网关层简化了运维复杂度，通过插件市场实现了安全认证、流量镜像等功能的快速复用，极大提升了研发和运维效率。

---



### 2：某大型互联网金融科技公司

 2：某大型互联网金融科技公司

**背景**: 该公司提供金融服务，业务系统部署在混合云架构中（部分自建机房，部分使用阿里云 ACK）。随着业务的快速迭代，开发团队需要频繁进行 API 接口变更和灰度发布。原有的 Nginx Ingress Controller 配置复杂，且缺乏标准化的 API 管理能力，导致多环境管理困难。

**问题**: 开发人员经常因为配置错误导致线上故障，且缺乏统一的流量控制策略，无法对特定 API 进行精细化的限流和熔断。此外，从旧架构向 K8s 迁移过程中，需要保证业务无缝切换，传统的网关难以平滑衔接微服务治理体系。

**解决方案**: 引入 Higress 作为统一的云原生网关。利用 Higress 对 Nginx Ingress 注解的兼容能力，实现了低成本的平滑迁移。通过 Higress 强大的 HTTP 到 gRPC 的协议转换能力，打通了前端 HTTP 请求与后端 gRPC 服务的链路。同时，利用其与 Istio 的集成，实现了服务级别的流量治理和安全管控。

**效果**: 实现了混合云架构下的统一流量管控，API 管理效率提升 50% 以上。通过金丝雀发布功能，成功将新版本上线导致的故障率降低了 90%。WASM 插件的使用使得定制化安全策略的部署时间从数小时缩短至分钟级。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Nginx + Lua (OpenResty) | Kong |
|------|-----------------|------------------------|------|
| 架构 | 基于Envoy和Istio的高性能云原生API网关 | 基于Nginx事件驱动的轻量级Web服务器/反向代理 | 基于Nginx/OpenResty的云原生API网关 |
| 性能 | 高性能，支持Wasm插件，低延迟 | 极高性能，低资源消耗，适合静态内容和高并发 | 高性能，但插件执行可能增加延迟 |
| 易用性 | 提供控制台和Kubernetes CRD，支持热更新，配置简单 | 需要手动配置Lua脚本，学习曲线较陡 | 提供管理UI和RESTful API，配置灵活但复杂 |
| 扩展性 | 支持Wasm插件和Lua插件，扩展性强 | 通过Lua脚本扩展，但需重启Nginx | 支持Lua和自定义插件，扩展性中等 |
| 云原生支持 | 原生支持Kubernetes和Istio，适合微服务 | 需额外配置才能适配Kubernetes | 支持Kubernetes，但需额外配置 |
| 社区与生态 | 阿里背书，社区活跃，与阿里云集成 | 成熟社区，插件丰富 | 强大社区，企业级支持 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源免费，商业支持需第三方 | 开源版免费，企业版收费 |

### 优势分析

- **高性能与低延迟**：基于Envoy和Istio，优化了网络通信和插件执行效率。
- **云原生集成**：原生支持Kubernetes和Istio，适合现代微服务架构。
- **灵活的扩展性**：支持Wasm和Lua插件，开发者和运维人员可以轻松扩展功能。
- **易用性**：提供控制台和Kubernetes CRD，简化配置和管理。
- **阿里生态支持**：与阿里云服务深度集成，适合阿里云用户。

### 不足分析

- **社区相对较小**：相比Nginx和Kong，社区规模和插件生态尚在发展中。
- **学习曲线**：对于不熟悉Envoy或Istio的用户，可能需要额外学习成本。
- **成熟度**：作为较新的项目，生产环境验证和稳定性可能不如Nginx或Kong。
- **文档和工具**：文档和周边工具可能不如成熟方案完善。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展开发

**说明**:  
Higress 基于 Envoy 构建，利用 WASM (WebAssembly) 技术可以实现高性能、跨语言、隔离安全的插件扩展。相比于原生 C++ 插件，WASM 插件支持使用 Go、Rust、JavaScript 等高级语言编写，且支持热加载，无需重启网关即可生效。

**实施步骤**:
1. 根据业务需求选择合适的 WASM 开发语言（推荐 Go 或 Rust）。
2. 使用 Higress 提供的 SDK 或工具链（如 `wasmedge` 或 `wasmtime`）编写插件逻辑。
3. 将编译好的 WASM 文件上传到 Higress 控制台或通过 OCI 镜像仓库进行分发。
4. 在网关路由或全局规则中配置并启用该插件。

**注意事项**:  
开发时需注意 WASM 运行时的内存限制和性能开销，避免在插件中进行阻塞式长耗时操作。

---

### 实践 2：精细化流量路由与灰度发布

**说明**:  
利用 Higress 强大的路由管理能力，可以实现基于 Header、Query 参数、Cookie 或权重的流量路由。这对于蓝绿部署、金丝雀发布和 A/B 测试场景至关重要，能够最大程度降低新版本上线的风险。

**实施步骤**:
1. 定义目标服务的不同版本（如 v1 和 v2）。
2. 在 Higress 中配置 Ingress 或 Gateway API 资源，定义匹配规则（例如 `x-version: canary`）。
3. 设置流量百分比权重，逐步将小部分流量引流至新版本。
4. 观察新版本监控指标，确认无误后逐步调整权重直至全量上线。

**注意事项**:  
确保灰度规则的优先级设置正确，避免普通流量意外进入灰度环境。建议配合全链路灰度环境进行隔离。

---

### 实践 3：全面对接云原生可观测性

**说明**:  
Higress 原生支持 Prometheus、OpenTelemetry 等标准，能够无缝集成到现有的云原生监控体系中。通过采集 Metrics、Traces 和 Logs，可以实时掌握网关的性能瓶颈和流量状态。

**实施步骤**:
1. 在 Higress 配置中开启 Prometheus Metrics 暴露端口。
2. 配置 OpenTelemetry Collector 收集链路追踪数据，并上报至 Jaeger 或 Zipkin。
3. 配置访问日志格式，建议使用 JSON 格式以便于解析，并对接如 Elasticsearch 或 Loki 等日志系统。
4. 在 Grafana 中导入 Higress 官方提供的 Dashboard 监控模板。

**注意事项**:  
注意高并发下日志采样率的配置，避免海量日志对网关性能或存储造成压力。

---

### 实践 4：多协议支持与服务治理整合

**说明**:  
Higress 不仅支持 HTTP/HTTPS，还原生支持 Dubbo、gRPC 等微服务协议。通过服务发现（Nacos, Consul, K8s CoreDNS）的整合，Higress 可以作为南北向流量网关，统一管理进入微服务集群的流量，实现跨协议的路由和透传。

**实施步骤**:
1. 在 Higress 中配置服务来源（Service Source），关联注册中心（如 Nacos）。
2. 配置服务路由规则，将 HTTP 请求映射至后端的 gRPC 或 Dubbo 服务。
3. 配置超时、重试及熔断策略，以增强后端服务的容错能力。
4. 利用 Higress 的服务来源管理功能，实现服务的自动发现与健康检查。

**注意事项**:  
配置协议转换时，需注意 HTTP Header 与 gRPC Metadata 之间的映射关系，以及 Dubbo 序列化格式的兼容性。

---

### 实践 5：高可用部署与资源隔离

**说明**:  
作为流量入口，Higress 的高可用性至关重要。在 Kubernetes 环境中，需要通过合理的资源请求与限制、反亲和性调度以及多副本部署来保障网关自身的稳定性，防止因网关宕机导致服务不可用。

**实施步骤**:
1. 设置 Higress Pod 的 `requests` 和 `limits`，防止资源争抢（OOM 或 CPU 节流）。
2. 配置 Pod 反亲和性，确保同一应用的多个 Higress 副本分布在不同的节点甚至可用区上。
3. 结合 HPA (Horizontal Pod Autoscaler) 根据 CPU 或自定义指标（如 QPS）自动扩缩容。
4. 配置健康检查探针，确保异常 Pod 能及时被剔除。

**注意事项**:  
生产环境中建议至少部署 3 个副本，并开启 PDB (Pod Disruption Budget) 以维护节点维护时的可用性。

---

### 实践 6：安全防护与认证鉴权

**说明**:  
Higress 提供了丰富的安全插件，用于应对 OWASP 风险、API 认证和流量控制。通过配置 JWT 鉴权、Keyless 认证或

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 构建，原生支持 HTTP/2 和 HTTP/3。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，HTTP/3 (QUIC) 则进一步解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，明确启用 HTTP/2 协议支持。
2. 如客户端支持，在 Listener 配置中开启 HTTP/3 (QUIC) 监听（通常基于 UDP 端口）。
3. 确保上游服务也支持 HTTP/2 或保持 HTTP/1.1 连接复用。

**预期效果**: 在高并发或弱网环境下，请求延迟可降低 20%-40%，连接数减少 50% 以上。

---

### 优化 2：配置全链路连接池与 Keep-Alive

**说明**: 默认的短连接建立（TCP 三次握手）开销巨大。通过配置 Higress 与上游服务之间的连接池，可以复用 TCP 连接，减少网络握手和 TLS 握手的耗时。

**实施方法**:
1. 在路由或服务配置中，启用 HTTP 连接池。
2. 调整 `maxRequestsPerConnection` 参数，平衡连接复用与长连接负载均衡（建议设置为 10^7 或保持默认，视上游服务处理能力而定）。
3. 设置合理的 `idleTimeout`，避免连接过早关闭或占用过多资源。

**预期效果**: 后端服务建立连接的 CPU 开销降低 30%，TPS（每秒事务处理量）提升 15%-25%。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 或远程调用逻辑，Wasm 执行效率极高。利用 Wasm 插件在网关层实现高频数据的本地缓存（如鉴权 token、配置信息），可以拦截大部分请求，避免回源。

**实施方法**:
1. 部署 Wasm 类型的插件，编写缓存逻辑。
2. 对于鉴权类插件，将 Token 验证结果缓存在网关内存中，设置合理的 TTL（如 60s）。
3. 避免在请求处理路径中使用同步的远程 RPC 调用（如调用远端 Redis），改用异步 Wasm HostCall 或本地缓存。

**预期效果**: 鉴权或复杂逻辑处理的延迟降低至 1ms-5ms 以内，后端负载减少 40%-60%（视缓存命中率而定）。

---

### 优化 4：启用 DNS 缓存与服务发现优化

**说明**: 如果上游域名解析频繁变动或 DNS 查询慢，会严重影响请求性能。Higress (Envoy) 的 DNS 缓存可以减少 DNS 查询频率。同时，针对 Kubernetes 服务发现，应避免不必要的全量列表更新。

**实施方法**:
1. 配置 Cluster 的 DNS 缓存时间（`dnsRefreshRate`），根据业务场景设置（如 60s）。
2. 如果在 K8s 环境，确保 Higress 使用 Endpoint Subset 或通过 `dns_lookup_family` 设置为 `V4_ONLY` 以减少查询开销。
3. 优先使用 IP 地址而非域名配置上游服务（如果环境允许）。

**预期效果**: 消除因 DNS 解析导致的偶发延迟（通常为 10ms-50ms），提高请求稳定性。

---

### 优化 5：调整 Worker 线程数与资源限制

**说明**: Higress 的处理性能与 CPU 核心数强相关。默认配置可能未充分利用宿主机的多核性能，或者因 Pod 资源限制导致 CPU 节流。

**实施方法**:
1. 将 Higress Gateway 的副本 CPU Request 与 Limit 设置为一致（避免 Burstable 策略导致的节流），建议使用 `performance` 配置文件。
2. 调整 Envoy 的 Worker �

---
## 学习要点

- 基于您提供的信息（Alibaba/Higress 在 GitHub 趋势中），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的一款基于 Istio 构建的下一代云原生 API 网关，旨在连接南北向流量与东西向流量。
- 它深度集成了 Envoy 和 K8s，能够作为 Ingress Controller 或 API Gateway 使用，提供高性能的流量管理。
- 该项目支持与 K8s Ingress、Gateway API 以及 Nginx Ingress 的高度兼容，降低了迁移和学习的成本。
- 内置了针对 Dubbo、Nacos 和 gRPC 等微服务生态的协议支持，特别适合构建 Java 微服务网关。
- 提供了开箱即用的 WAF（Web 应用防火墙）插件和安全防护能力，增强了网关的安全性。
- 具备强大的可扩展性，支持通过 WASM (WebAssembly) 或 Go/Python/Java 等语言编写自定义插件来处理业务逻辑。


---
## 学习路径

## 学习路径

### 阶段 1：基础认知与环境准备

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心特性、应用场景及架构设计
- 容器基础 与 Kubernetes 基础原理
- Ingress 与 Gateway API 的基本区别

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (https://higress.io/docs/latest/overview/what-is-higress/)
- Higress GitHub 仓库 README (https://github.com/alibaba/higress)
- Kubernetes 官方文档关于 Service 与 Ingress 的介绍

**学习建议**:
- 此阶段重点在于理解“为什么需要 Higress”以及它解决了什么问题。
- 如果不熟悉 Kubernetes，建议先补充 Pod、Service、Namespace 等基本概念。
- 阅读官方文档时，重点关注架构图，理解 Higress 如何将 Istio 的控制层与 Envoy 的高性能数据层结合。

---

### 阶段 2：核心功能实战与配置

**学习内容**:
- Higress 的安装部署（Docker/Kubernetes/Helm）
- 域名、路由、重定向/重写配置
- 服务来源的注册与发现（Nacos, Consul, K8s Service, Fixed Address 等）
- 流量管理：金丝雀发布、蓝绿发布、Header 匹配路由
- 插件系统入门：使用 WAF 插件、Key Rate Limit 插件

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 快速开始与用户指南
- Higress 控制台界面实操
- Envoy 基础概念（Listener, Route, Cluster）

**学习建议**:
- 动手搭建一套本地环境（推荐使用 Kind 或 Minikube 部署 Higress）。
- 尝试将一个简单的后端服务（如 Nginx 或 Go Echo）接入 Higress，并通过域名访问。
- 重点练习路由配置，理解不同匹配优先级对流量走向的影响。

---

### 阶段 3：插件开发与安全治理

**学习内容**:
- Higress 插件（Wasm 插件）的工作原理
- Lua 和 Go（Wasm）编写自定义插件
- 全局认证与鉴权：OIDC、JWT、Basic Auth
- 安全防护：WAF 防护配置、CORS 跨域配置
- Mock 服务与泛化调用（Dubbo/HTTP）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场与开发指南
- Envoy Wasm 官方文档
- Higress 官方插件市场案例参考

**学习建议**:
- 学习插件开发是掌握 Higress 的关键。尝试编写一个简单的 Go Wasm 插件（例如：添加自定义 Header 或简单的鉴权逻辑）。
- 深入理解 Higress 如何通过插件扩展网关能力，而不需要修改核心代码。
- 在生产环境模拟场景中配置安全策略，防止 SQL 注入或限流测试。

---

### 阶段 4：高可用架构与性能优化

**学习内容**:
- Higress 的高可用部署架构与多集群容灾
- 性能指标监控与日志采集（对接 Prometheus/Grafana/SLS）
- 热更新与配置版本管理
- 常见故障排查 与调优手段
- Higress 对接 AI 服务（如对接通义千问等大模型网关能力）

**学习时间**: 2-3周

**学习资源**:
- Higress GitHub Issues 与 Discussions
- 云原生可观测性最佳实践文档
- Higress Ingress 高级配置文档

**学习建议**:
- 关注生产环境的稳定性，学习如何进行滚动升级和回滚。
- 学习如何分析 Access Log 和 Trace 链路追踪来定位性能瓶颈。
- 了解 Higress 在 AI 网关方向的最新进展，这是其区别于传统网关的重要特性。

---

### 阶段 5：源码剖析与社区贡献

**学习内容**:
- Higress 源码结构分析（控制平面 Istio 组件、数据平面 Envoy 扩展）
- Router、Console、Wasm Go SDK 核心代码解读
- 参与社区 Issue 讨论与贡献 PR
- 定制化开发与私有化部署适配

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码 (https://github.com/alibaba/higress)
- Istio 源码与 Envoy 源码参考

**学习建议**:
- 在精通使用和配置的基础上，阅读源码有助于理解底层实现逻辑。
- 尝试修复一个简单的 Bug 或添加一个实用的功能到社区，这能极大提升技术深度。
- 关注 Higress 社区的 Roadmap，

---
## 常见问题


### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里云将内部使用的 HSF 路由网关和 Istio 网关进行融合，并开源出来的产品。

它建立在 Envoy 和 Istio 之上，旨在解决云原生架构下的流量管理问题。Higress 遵循 Open Gateway (OGC) 标准，不仅支持 Kubernetes Ingress，也支持 API 网关的各种传统功能（如鉴权、限流、流量染色）。作为阿里云云原生 API 网关的开源版本，它继承了阿里在双十一等高并发场景下的稳定性经验，同时积极拥抱云原生生态。

---



### 2: Higress 与 Nginx、APISIX 或 Traefik 等 Ingress 控制器相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Traefik 等 Ingress 控制器相比有什么优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **高性能**: 基于 C++ 编写的 Envoy 作为数据面，相比基于 Nginx Lua 的控制器（如 APISIX、Kong）或基于 Go 的控制器（如 Traefik），在处理长连接、高并发请求时通常具有更低的延迟和更高的吞吐量。
2.  **安全与隔离**: Higress 将配置管理与数据面转发分离。配置变更（通过 WASM 插件或 Lua 逻辑）不会导致网关进程重启或核心配置重载，从而避免了流量抖动，安全性更高。
3.  **标准化与扩展性**: 它原生支持 Istio，可以无缝集成服务网格（Service Mesh）。同时，它支持 WASM (WebAssembly) 插件，允许开发者使用 Go、C++、Rust、JavaScript 等多种语言编写插件，且插件热加载无需重启网关，比传统的 Lua 脚本更具现代化和安全性。
4.  **兼容性**: Higress 兼容 Kubernetes Ingress API 和 Nginx 注解，降低了从传统 Ingress Controller 迁移过来的成本。

---



### 3: Higress 支持 WASM (WebAssembly) 插件吗？这对开发者意味着什么？

3: Higress 支持 WASM (WebAssembly) 插件吗？这对开发者意味着什么？

**A**: 是的，对 WASM 的支持是 Higress 的核心亮点之一。

这意味着开发者不再受限于网关原本的语言（如 Nginx 的 Lua）。你可以使用任何编译为 WASM 的语言（例如 Go、C++、Rust、AssemblyScript 甚至 TypeScript/JavaScript）来编写自定义的业务逻辑。

**具体优势包括**：
*   **沙箱隔离**: 插件在独立的沙箱中运行，即使插件崩溃也不会导致整个网关进程崩溃，极大地提升了系统的稳定性。
*   **热更新**: 修改或发布插件时，不需要重启 Higress 进程，流量完全无损。
*   **高性能**: WASM 的执行效率接近原生代码，且内存占用低。

---



### 4: 我已经在使用 Istio，是否还需要 Higress？

4: 我已经在使用 Istio，是否还需要 Higress？

**A**: 这取决于你的具体需求。Higress 实际上可以作为 Istio 的 Ingress Gateway 替代品。

*   **如果你只需要基本的南北向流量管理**：标准的 Istio Ingress Gateway 可能已经足够。
*   **如果你需要更强大的 API 网关功能**：标准的 Istio Ingress Gateway 配置较为复杂（需要操作 CRD），且缺乏一些传统 API 网关的便捷功能（如控制台 UI、简单的流量塑形、复杂的鉴权插件等）。Higress 提供了更加人性化的控制台，内置了丰富的流量管理和安全插件，并且兼容 Istio 的 CRD。因此，Higress 可以被视为“增强版”的 Istio Ingress Gateway，它让 Istio 的使用门槛更低，功能更全面。

---



### 5: Higress 如何处理服务发现？它是否只能对接 Kubernetes 服务？

5: Higress 如何处理服务发现？它是否只能对接 Kubernetes 服务？

**A**: Higress 原生支持 Kubernetes Service，但这并不是唯一的选项。作为一个现代化的 API 网关，Higress 具备强大的**服务发现**能力，能够对接多种注册中心。

除了 Kubernetes 原生服务外，Higress 还支持：
*   **Nacos**: 阿里巴巴开源的微服务发现与配置管理中心。
*   **Consul**: HashiCorp 提供的服务网格解决方案。
*   **ZooKeeper**: 传统的 Dubbo 服务注册中心。
*   **固定地址 (DNS/IP)**: 支持手动配置上游服务列表。

这使得 Higress 非常适合处于从传统微服务架构（如 Spring Cloud + Nacos）向云原生架构过渡的混合环境。

---



### 6: Higress 是否支持 Dubbo 服务？如果我的后端是 Dubbo 接口，能否直接通过 HTTP 调用？

6: Higress 是否支持 Dubbo 服务？如果我的后端是 Dubbo 接口，能否直接通过 HTTP 调用？

**A**: 是的，Higress 对 Dubbo 框架有非常深度的支持，这是它作为阿里系产品的特色之一。

Higress 提供了 **Dubbo-to-HTTP (或者 HTTP-to-Dubbo)** 的协议转换能力。这意味着，如果你的

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础路由配置

### 假设你有一个运行在本地 8080 端口的后端服务（例如一个简单的 Python Flask 或 Node.js 应用），请编写一个 Higress 的 Ingress 配置文件，实现通过域名 `example.com` 访问该服务。

### 提示**: 关注 Higress 的 `Ingress` 资源定义，重点在于 `spec.rules` 字段中的 `host` 设置以及后端 `service` 的端口对齐。你需要先确保有一个对应的 Kubernetes Service 指向你的 Pod。

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，为您提供的 6 条实践建议：

### 1. 利用 AI 提供者路由实现成本与性能的最优解
Higress 的核心优势在于能够统一管理不同的 LLM（大语言模型）提供商。在实际使用中，不要仅仅将其作为转发代理，而应充分利用其**路由功能**。
*   **具体操作**：在配置服务来源时，同时接入 OpenAI、Azure OpenAI、通义千问以及本地部署的 Ollama 等多个模型提供商。在路由规则中，根据业务需求分发流量：例如，将简单的摘要任务路由给更便宜的小模型（如 GPT-3.5 或 Qwen-Turbo），将复杂的代码生成任务路由给高智商模型（如 GPT-4 或 Qwen-Max）。
*   **最佳实践**：配置基于权重的金丝雀发布。当新模型发布时，先通过 Higress 分流 10% 的流量进行测试，观察响应延迟和 token 消耗，确认无误后再全量切换。
*   **常见陷阱**：避免在应用代码中硬编码模型 API 地址。所有模型调用应统一经过 Higress，这样当某个厂商 API 宕机或限流时，你可以在网关层快速切换流量，而无需重新发布业务代码。

### 2. 实施细粒度的 Token 预算与速率限制
LLM 调用的成本主要基于 Token 计费，且 API 提供商通常有严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制。Higress 提供了针对 AI 特性的限流能力。
*   **具体操作**：针对不同的 API Key 或租户，配置精细的限流策略。例如，为内部测试账号设置较低的 TPM 限制，防止意外消耗高额费用；为 VIP 客户设置独立的并发队列。
*   **最佳实践**：启用 Higress 的“请求计数”插件，结合 Prometheus 监控不同应用的 Token 消耗趋势，基于真实数据优化网关层的限流阈值。
*   **常见陷阱**：仅配置传统的 QPS（每秒请求数）限流是不够的。因为一次 LLM 请求可能包含数千个 Prompt Token，且生成时间很长。必须配置 TPM 和并发数限制，以防止后端模型提供商触发 429 Too Many Requests 错误，导致服务中断。

### 3. 部署 Prompt 模板与敏感词过滤插件
为了提升开发效率和安全性，应将 Prompt 的管理收拢至网关层，利用 Higress 的 Wasm 插件生态。
*   **具体操作**：使用 Higress 的“请求体转换”或官方 AI 插件，在网关层预置 Prompt 模板。客户端只需发送简短的指令（如 `{"category": "summary"}`），网关自动拼接完整的 System Prompt。
*   **最佳实践**：部署内容安全插件（如阿里云内容安全或开源的 LLM Guard）。在请求发送给模型之前，拦截包含 PII（个人敏感信息）或违规内容的输入；在模型返回结果时，再次过滤输出，防止法律风险。
*   **常见陷阱**：不要在网关层处理过长的 Prompt 拼接逻辑。虽然 Wasm 性能很高，但复杂的文本处理会增加网关延迟。建议仅做模板替换和关键词过滤，将重计算逻辑保留在业务端或模型端。

### 4. 配置语义缓存以降低成本并提升响应速度
对于用户咨询中常见的重复问题（如“帮我写一封请假信”），每次都调用 LLM API 是一种浪费。Higress 支持基于语义的缓存。
*   **具体操作**：开启 Higress 的 AI 缓存插件。配置向量数据库（如 Redis 向量搜索或 Milvus）作为缓存后端。当用户提问时，Higress 先计算问题的语义向量，检索是否存在相似度 > 0.95 的历史问答。
*   **最佳实践**：针对“只读”类问题（如知识

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260207-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*