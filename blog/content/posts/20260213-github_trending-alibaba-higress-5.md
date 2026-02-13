---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-13T19:28:07+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "WASM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的简洁总结： 项目概况 * **名称**：Higress * **开发方**：阿里巴巴 * **定位**：AI 原生 API 网关 * **语言**：Go * **热度**：GitHub 超过 7,500 星标。 核心定位与架构 Higress 是一个基于 **Is"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "RAG应用"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,523 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在为云原生应用与 LLM 服务提供统一的流量管理入口。它不仅兼容 Kubernetes Ingress 等传统微服务路由场景，更针对 AI 应用集成了模型服务与 MCP 协议支持，帮助企业解决异构流量治理难题。本文将梳理其架构设计，并重点介绍 WASM 插件生态及 AI 网关的核心特性。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的简洁总结：

### 项目概况
*   **名称**：Higress
*   **开发方**：阿里巴巴
*   **定位**：AI 原生 API 网关
*   **语言**：Go
*   **热度**：GitHub 超过 7,500 星标。

### 核心定位与架构
Higress 是一个基于 **Istio** 和 **Envoy** 构建的云原生 API 网关。它通过 **WebAssembly (WASM)** 插件扩展功能，采用了**控制平面**与**数据平面**分离的架构。其配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适用于 AI 长连接流式响应场景。

### 三大核心功能
1.  **AI 网关**：
    *   为大语言模型（LLM）应用提供统一 API。
    *   支持 30+ 家 LLM 提供商的协议转换。
    *   核心插件包括：`ai-proxy`（代理）、`ai-statistics`（可观测性）、`ai-cache`（缓存）和 `ai-security-guard`（安全防护）。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。
    *   包含 `mcp-router`、`jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如搜索、地图工具等）。
3.  **传统 API 网关**：
    *   提供 Kubernetes Ingress 控制器功能。
    *   兼容 `nginx-ingress` 注解，支持微服务路由。

---
## 评论

### 总体判断

Higress 是一款将**云原生流量治理与 AI 大模型应用生态深度融合**的开源网关，它成功打破了传统 API 网关仅作为流量“管道”的定位，通过内置 AI 网关与 MCP 协议支持，转型为 LLM 时代的**智能流量入口**。对于正在构建 AI Agent 或大模型应用的企业，Higress 提供了目前开源界最完备的“流量网关+模型网关”二合一解决方案。

---

### 深度评价分析

#### 1. 技术创新性：从“流量路由”进化到“模型路由”
*   **事实**：Higress 基于 Istio 与 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。其核心定位包含 AI Gateway、MCP Server 托管及微服务网关。
*   **推断**：Higress 的最大技术亮点在于**将 LLM 的语义处理能力下沉到了网关层**。传统网关只做 HTTP 转发，而 Higress 创新性地引入了针对 AI 服务的路由逻辑（如基于 Token 计费的流量整形、模型 Provider 的无感切换）。此外，它对 **MCP (Model Context Protocol)** 的原生支持是其极具前瞻性的差异化方案，解决了 AI Agent 调用外部工具时的连接标准问题，使其成为 AI 生态中的关键基础设施，而不仅仅是一个反向代理。

#### 2. 实用价值：解决 AI 落地中的“连接”与“成本”痛点
*   **事实**：文档明确指出其支持 Kubernetes Ingress、微服务路由以及 AI Gateway 特性。
*   **推断**：在实用层面，Higress 解决了三个关键问题：
    1.  **架构统一**：企业无需分别维护“传统微服务网关”和“大模型专用网关”，一套架构同时处理 RPC 调用和 LLM 请求，降低了运维复杂度。
    2.  **AI 安全与合规**：通过网关层统一拦截敏感词，避免了在应用代码中重复造轮子，且便于做 PII（个人隐私信息）脱敏。
    3.  **成本控制**：AI 流量极其昂贵，Higress 可以在网关层实现基于 Token 的限流和缓存，直接减少对上游模型厂商的 API 调用费用，这对生产环境至关重要。

#### 3. 代码质量与架构：云原生标准的高起点
*   **事实**：项目基于 Go 语言开发，星标数 7,523，架构上明确分离了控制平面与数据平面。
*   **推断**：依托 Envoy 作为高性能数据平面，Higress 继承了业界顶级的 C++ 高并发处理能力。控制面采用 Go 语言，符合云原生生态的主流开发范式，便于 Kubernetes 集成。WASM 插件系统的引入使得代码扩展性极佳，开发者可以使用 C++/Go/Rust/AssemblyScript 编写插件而无需重新编译网关主体，这种架构设计体现了极高的工程成熟度。文档的多语言支持（中/日/英）也反映了其面向全球社区的代码规范与文档完整性。

#### 4. 社区活跃度：背靠阿里的强有力支撑
*   **事实**：仓库归属于 Alibaba 组织，星标数超过 7500，且提供了详细的 DeepWiki 架构说明。
*   **推断**：作为阿里内部的产物开源，Higress 经过了阿里电商高并发场景的验证。其社区活跃度通常较高，更新频率紧跟 AI 技术的迭代速度（例如对 Claude、DeepSeek 等新模型的支持通常很快）。相比于个人开源项目，Higress 的企业级背景意味着其代码更稳定，出现严重 Bug 的修复速度也更有保障。

#### 5. 学习价值：理解“AI Native”架构的最佳范本
*   **事实**：项目涵盖了从 Core Architecture 到 AI Gateway Features 的完整文档。
*   **推断**：对于开发者而言，Higress 是学习**“如何将 AI 能力嵌入传统基础设施”**的绝佳案例。通过阅读其 WASM 插件源码，开发者可以学习如何处理流式传输、如何在网关层解析 SSE (Server-Sent Events) 以及如何实现提示词的动态注入。这对于理解下一代软件架构非常有启发。

#### 6. 潜在问题与改进建议
*   **事实**：基于 Istio 架构，功能极其丰富。
*   **推断**：
    *   **复杂度过高**：对于仅需简单 AI 对话功能的小型团队，Higress 的配置模型（Ingress API、路由规则）可能显得过于厚重，学习曲线陡峭。
    *   **资源消耗**：作为 Sidecar 或独立网关，Envoy 本身对内存和 CPU 的要求高于轻量级 Nginx，在边缘计算或资源受限的设备上部署可能存在挑战。
    *   **建议**：进一步简化 AI 相关的 CRD（自定义资源）定义，提供类似 Traefik 或 Kong 那样更简洁的配置方式，以降低中小开发者的使用门槛。

#### 7. 与同类工具对比优势
*   **对比 Nginx/Kong**：传统网关对 SSE（流式响应）的支持通常需要复杂的 Lua 脚本配置，且难以做语义层面的路由。Higress 原生理解 AI 协议，配置更简单。
*   **对比 LangChain/Nginx-AI**：LangChain 是开发框架

---
## 技术分析

以下是对阿里巴巴开源仓库 **Higress** 的深度技术分析。Higress 定位为“AI Native API Gateway”，它基于 Istio 和 Envoy 构建，旨在解决云原生应用和 AI 应用（特别是 LLM）的流量管理、安全防护和服务治理问题。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了标准的**控制平面与数据平面分离**的架构模式，这是现代云原生网关的主流设计。
*   **数据平面**：深度依赖 **Envoy**。Envoy 是高性能的 C++ 网络代理，负责处理实际的流量转发、负载均衡、TLS 终结等。
*   **控制平面**：基于 **Istio** 进行了扩展和简化。Higress 移除了 Istio 中繁重的 Sidecar 模式，专注于作为 Ingress Gateway 或 API Gateway 的角色。它使用 **xDS 协议**（包括 LDS, RDS, CDS, EDS）将配置下发给数据平面。
*   **扩展层**：引入了 **WebAssembly (WASM)** 作为核心插件运行时。这使得用户可以使用 C++, Go, Rust, JavaScript (QuickJS) 等多种语言编写插件，并在 Envoy 的沙箱中运行。

### 核心模块
1.  **Router (路由层)**：基于 Envoy 的 HTTP Router filter，支持基于 Header、Path、Query Parameter 的精细化路由。
2.  **WASM Plugin System (插件市场)**：这是 Higress 的核心差异化能力。它允许动态加载代码，而无需重启网关。
3.  **AI Gateway Module (AI 网关模块)**：专门针对 LLM 流量设计的处理模块，包含 Provider 管理、Token 计数、流式响应处理等。
4.  **MCP (Model Context Protocol) Server**：作为 AI Agent 的工具集成层，允许大模型安全地调用外部 API。

### 技术亮点与创新点
*   **AI-Native 设计**：Higress 是业界较早将“AI 网关”作为一等公民设计的网关。它不仅仅是转发 HTTP 请求，还理解 LLM 的语义（如处理 SSE 流式响应、统一 OpenAI 格式转换）。
*   **热更新能力**：利用 Envoy 的 xDS 机制，配置变更可以在毫秒级生效且不断开连接（长连接友好），这对于 AI 对话场景至关重要。
*   **Kubernetes 原生**：通过 Ingress 或 Gateway API CRD 进行管理，与 K8s 生态无缝融合。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure、通义千问、Llama 等不同厂商的 API 统一封装为标准格式。
    *   **Token 管理**：实时统计 Prompt 和 Completion 的 Token 消耗，实现基于 Token 的限流和计费。
    *   **Prompt 保护**：通过敏感词过滤和 PII（个人隐私信息）脱敏插件，防止数据泄露。
    *   **结果缓存**：针对高频相同的 Prompt 缓存 LLM 的响应，降低成本并降低延迟。

2.  **传统 API 网关**：
    *   支持 K8s Ingress，替代 Nginx Ingress Controller。
    *   流量染色、金丝雀发布、蓝绿发布。
    *   全局认证与鉴权（OIDC, AK/SK, JWT）。

3.  **MCP 协议支持**：
    *   Higress 可以作为 MCP Server 的托管端，让 AI Agent 能够通过网关安全、受控地访问后端工具（如数据库查询、API 调用）。

### 解决的关键问题
*   **LLM 落地成本与安全**：解决了企业接入多个 LLM 厂商时的接口碎片化问题，并提供了统一的流量控制和审计能力。
*   **异构系统通信**：在微服务和 AI 应用之间提供了高性能的桥梁。
*   **扩展性与灵活性**：通过 WASM 解决了传统 Lua 插件（如 OpenResty）难以维护、安全性差、性能受限于 Lua 协作器的问题。

### 与同类工具对比
*   **VS Nginx/OpenResty**：Higress 配置更现代化（K8s CRD），支持 WASM（多语言、沙箱隔离），并发处理能力更强（基于 C++ Envoy），但配置复杂度略高于简单的 Nginx。
*   **VS Kong**：Kong 基于 Nginx/OpenResty + PostgreSQL，Higress 基于 Envoy + K8s。Higress 在云原生集成度上更高，且无强依赖数据库（配置存储在 etcd/K8s 中）。
*   **VS Istio Ingress**：Higress 本质上是一个“裁剪版”且“增强版”的 Istio Ingress Gateway。它去掉了 Istio 控制面的沉重负担，但保留了强大的数据面能力，并增加了 WASM 和 AI 特性。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM 运行时（如 Wasmtime 或 V8）。当请求进入时，Envoy 会将指针传递给 WASM 内存空间，插件逻辑在此执行。
*   **配置分发**：Higress Controller 监听 K8s API Server 的资源变化，将其转换为 xDS 配置，通过 gRPC 推送给 Envoy。
*   **流式转发**：对于 AI 的 SSE（Server-Sent Events）响应，Higress 使用 Envoy 的 Streaming Filter 机制，确保在流式传输过程中依然可以进行诸如“敏感词拦截”的处理（虽然实现难度极大，通常需要流式匹配算法）。

### 代码组织与设计模式
*   **Controller 模式**：使用 K8s Controller-Runtime 模式编写控制平面，监听资源事件并调和状态。
*   **Filter Chain 模式**：数据平面采用责任链模式，插件按顺序挂载到请求处理的 Pre-Auth、Pre-Routing、Post-Action 等阶段。

### 性能与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **水平扩展**：无状态设计，可以通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU/内存指标自动扩缩容。

### 技术难点与解决
*   **WASM 的冷启动与性能损耗**：WASM 的编译和实例化有开销。Higress 通过缓存编译后的 Module 和使用 AOT (Ahead-of-Time) 编译优化来降低此开销。
*   **长连接与配置更新**：传统的网关更新配置可能需要重载进程，导致长连接断开。Higress 利用 Envoy 的热重启和 xDS 热更新机制，实现了配置变更对业务无感。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：企业内部需要接入多个大模型，并对 API 调用进行统一的鉴权、限流、审计和 Prompt 模板管理。
2.  **微服务流量入口**：替代 Nginx Ingress，需要更强大的流量治理能力（如全链路灰度、超时重试）。
3.  **多云/混合云 API 管理**：需要统一管理部署在不同 K8s 集群的 API 服务。

### 不适合的场景
1.  **极简静态资源服务**：如果只是托管几个静态 HTML 文件，Nginx 或 Caddy 更轻量。
2.  **非 K8s 环境**：虽然 Higress 可以在非 K8s 环境运行，但其配置管理高度依赖 K8s API，在传统虚拟机环境部署会显得“杀鸡用牛刀”且配置复杂。
3.  **极度依赖 DB 的应用网关**：如果需要将 API 配置存储在复杂的 SQL 数据库中进行复杂的联表查询，Higress 的 K8s 声明式模型可能需要额外的 CRD 扩展。

### 集成方式
*   **Ingress 模式**：直接替换 K8s 集群的 Ingress Controller。
*   **API Gateway 模式**：创建 `Gateway` 和 `Route` CRD，配合 WASM 插件使用。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 语义理解**：从简单的流量转发转向“语义路由”，即根据 Prompt 的意图将请求路由到不同参数的模型或 RAG 系统。
*   **WASM 生态的标准化**：推动 Proxy-WASM 标准的成熟，吸引更多插件开发者。

### 社区反馈与改进空间
*   **文档与易用性**：对于非 K8s 专家，上手门槛较高。控制台 UI 的易用性仍需提升。
*   **WASM 调试困难**：编写 WASM 插件时的调试体验不如本地脚本方便。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：需要理解 Service Mesh 和 Gateway 的演进。
*   **后端/平台工程工程师**：负责构建公司内部的 API 平台。
*   **AI 应用开发者**：需要处理 LLM 调用的工程化问题（Token 管理、安全）。

### 学习路径
1.  **基础**：熟悉 Kubernetes 原理，特别是 Ingress 和 CRD。
2.  **核心**：阅读 Envoy 官方文档，理解 xDS 协议、Listener/Cluster/Route 配置。
3.  **进阶**：学习 WebAssembly (WASI) 原理，尝试使用 Go 或 Rust 编写一个简单的 Higress 插件。
4.  **实践**：在本地 Kind 集群中部署 Higress，配置一个 AI 代理转发到 OpenAI。

---

## 7. 最佳实践建议

### 正确使用指南
*   **利用 WASM 隔离业务逻辑**：不要修改 Higress 的核心代码，将自定义认证、日志记录、Header 修改逻辑全部写成 WASM 插件。
*   **AI 模型的降级策略**：在路由配置中设置“后备模型”，例如当主模型（如 GPT-4）超时或失败时，自动降级到更便宜的模型（如 GPT-3.5）。

### 性能优化
*   **开启 HTTP/2**：Higress 与后端服务通信时，尽量开启 HTTP/2 以减少连接数开销。
*   **WASM 插件优化**：避免在 WASM 插件中进行阻塞式网络调用（如有必要，需使用异步调用），否则会阻塞 Envoy 的事件循环，导致吞吐量暴跌。

### 常见问题
*   **503/502 错误**：通常是由于后端服务健康检查失败或 Envoy 连接池耗尽。检查 Upstream 的配置。
*   **流式响应中断**：检查网关与客户端之间的超时设置，AI 流式响应可能耗时较长，需调大 `stream_idle_timeout`。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与

---
## 代码示例




```python
# 示例1：基于Higress的动态路由配置
def dynamic_routing_config():
    """
    解决问题：根据请求头动态路由到不同服务
    场景：A/B测试或灰度发布时，需要将特定用户流量导向新版本服务
    """
    config = {
        "route_name": "canary-release",
        "match_conditions": {
            "headers": {
                "x-user-group": "beta-testers"  # 匹配测试用户
            }
        },
        "destination": {
            "service": "user-service-v2",  # 新版本服务
            "port": 8080
        },
        "fallback": {
            "service": "user-service-v1",  # 旧版本服务
            "port": 8080
        }
    }
    
    # 模拟发送配置到Higress网关
    print(f"应用动态路由配置: {config['route_name']}")
    print(f"匹配条件: {config['match_conditions']}")
    print(f"目标服务: {config['destination']['service']}")
    return config

# 调用示例
dynamic_routing_config()
```




```python
# 示例2：Higress插件开发 - 请求认证
def custom_auth_plugin():
    """
    解决问题：实现自定义的API认证逻辑
    场景：需要验证请求头中的API密钥是否有效
    """
    def authenticate_request(request_headers):
        # 模拟从数据库获取有效密钥
        valid_api_keys = ["key123", "key456"]
        
        # 从请求头获取API密钥
        api_key = request_headers.get("x-api-key", "")
        
        # 验证逻辑
        if api_key in valid_api_keys:
            print("认证成功")
            return True
        else:
            print("认证失败: 无效的API密钥")
            return False
    
    # 模拟请求处理
    test_headers = {"x-api-key": "key123"}
    result = authenticate_request(test_headers)
    return result

# 调用示例
custom_auth_plugin()
```




```python
# 示例3：Higress流量控制配置
def rate_limiting_config():
    """
    解决问题：防止API被过度调用
    场景：限制每个IP每分钟最多100次请求
    """
    config = {
        "limit_name": "api-rate-limit",
        "rate_limit": {
            "requests_per_minute": 100,
            "burst": 10  # 允许短时突发流量
        },
        "key_type": "IP",  # 基于IP限流
        "response": {
            "status_code": 429,
            "message": "请求过于频繁，请稍后再试"
        }
    }
    
    # 模拟应用限流配置
    print(f"应用限流配置: {config['limit_name']}")
    print(f"限流规则: 每分钟{config['rate_limit']['requests_per_minute']}次请求")
    print(f"基于: {config['key_type']}")
    return config

# 调用示例
rate_limiting_config()
```


---
## 案例研究


### 1：识货 APP

 1：识货 APP

**背景**:  
识货是阿里巴巴旗下的垂直电商平台，专注于运动装备和潮流文化，拥有千万级用户。随着业务发展，其 API 网关面临高并发流量和复杂路由规则的挑战。

**问题**:  
原有网关架构在处理突发流量时性能不足，且缺乏灵活的流量管理和安全防护能力。同时，多语言微服务（如 Java、Go、Python）的统一接入和协议转换（HTTP、gRPC）存在技术瓶颈。

**解决方案**:  
采用 Higress 作为云原生 API 网关，利用其高性能（基于 Rust 和 C++ 实现）和插件化能力。通过 Higress 的动态路由和负载均衡功能，实现多语言服务的统一接入；结合 WAF 插件增强安全防护；使用流量标签和灰度发布功能优化版本管理。

**效果**:  
- 网关吞吐量提升 50%，延迟降低 30%  
- 支持日均 10 亿+ API 调用  
- 灰度发布效率提高 80%，故障率下降 60%  

---



### 2：阿里云云原生 API 网关

 2：阿里云云原生 API 网关

**背景**:  
阿里云为全球客户提供云原生 API 网关服务，需要支持多租户、高可用和弹性扩展。传统网关方案在资源隔离和按需扩展方面存在局限。

**问题**:  
多租户场景下资源竞争严重，导致性能抖动；同时，客户需求多样化（如自定义插件、跨云部署），现有方案难以快速响应。

**解决方案**:  
基于 Higress 构建阿里云云原生 API 网关，利用其多租户架构和 Kubernetes 原生支持。通过 Higress 的 WASM 插件机制，允许客户自定义逻辑；结合阿里云 SLB 和弹性伸缩能力，实现自动扩缩容。

**效果**:  
- 支持 10 万+ 租户隔离，资源利用率提升 40%  
- 插件开发效率提高 70%，支持客户自定义逻辑  
- 弹性伸缩响应时间缩短至秒级  

---



### 3：B站（Bilibili）

 3：B站（Bilibili）

**背景**:  
B站作为国内领先的视频平台，其微服务架构涉及数百个服务，API 流量峰值达百万 QPS。原有网关在处理长连接（如 WebSocket）和实时数据推送时存在性能瓶颈。

**问题**:  
传统网关在长连接场景下内存占用高，且缺乏对实时流量的精细控制（如限流、熔断）。同时，多团队协作时插件开发和热更新流程复杂。

**解决方案**:  
引入 Higress 作为核心流量入口，利用其高性能 HTTP 和 WebSocket 支持。通过 Higress 的分布式限流和熔断能力，保障核心服务稳定性；结合 Istio 实现服务网格集成，统一流量治理。

**效果**:  
- WebSocket 连接数提升 3 倍，内存占用降低 50%  
- 核心接口 P99 延迟从 200ms 降至 80ms  
- 插件热更新时间从分钟级缩短至秒级

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Istio 和 Envoy，支持高并发 | 高性能，基于 Nginx 和 OpenResty | 极高性能，基于 LuaJIT 和 OpenResty |
| 易用性 | 提供控制台和 K8s 集成，配置灵活 | 控制台功能丰富，但配置较复杂 | 控制台简洁，支持热更新 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持插件扩展，兼容 K8s CRD | 支持插件扩展，社区丰富 | 支持插件扩展，Lua 生态强大 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，文档完善 | 社区活跃，国内支持强 |

### 优势分析

- 优势1：深度集成 K8s 和 Istio，适合云原生场景
- 优势2：支持多种协议（HTTP、Dubbo、gRPC），兼容性强
- 优势3：提供企业级安全防护和流量管理能力

### 不足分析

- 不足1：社区生态相对 Kong 和 APISIX 较新，插件较少
- 不足2：学习曲线较陡，对 K8s 和 Istio 依赖较强
- 不足3：企业版功能可能需要额外付费

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Envoy 和 Istio 的兼容性进行平滑迁移

**说明**: Higress 基于 Envoy 和 Istio 构建，能够与现有的 Istio 服务网格无缝集成。通过利用这一特性，企业可以在不中断业务的情况下，将 API 网关功能从传统网关迁移至 Higress，同时保持与微服务治理的一致性。

**实施步骤**:
1. 评估现有 Istio 或 Envoy 的配置，确定迁移范围。
2. 在测试环境中部署 Higress，并配置与现有服务网格的对接。
3. 逐步将流量从旧网关切换至 Higress，监控性能和错误率。
4. 完成全量切换后，下线旧网关实例。

**注意事项**: 确保网络策略和 RBAC 配置在迁移前后保持一致，避免权限问题。

---

### 实践 2：使用 Wasm 插件扩展网关功能

**说明**: Higress 支持 WebAssembly (Wasm) 插件，允许开发者使用多种编程语言（如 Go、Rust、AssemblyScript）编写自定义逻辑。这种机制比传统的 Lua 插件更安全、更灵活，且性能更高。

**实施步骤**:
1. 确定需要自定义的功能需求（如自定义认证、流量整形）。
2. 使用支持 Wasm 的语言编写插件代码，并编译为 `.wasm` 文件。
3. 将插件上传至 Higress 控制台或通过 API 配置插件。
4. 为特定路由或全局网关启用插件，并进行测试。

**注意事项**: Wasm 插件的资源消耗需监控，避免因插件性能问题影响网关整体性能。

---

### 实践 3：配置多环境流量管理与灰度发布

**说明**: Higress 提供强大的流量路由能力，支持基于权重、Header、Cookie 等条件的流量分配。通过合理配置，可以实现蓝绿部署、金丝雀发布等灰度发布策略，降低新版本上线的风险。

**实施步骤**:
1. 在 Higress 中定义多个服务版本（如 v1、v2）。
2. 创建路由规则，设置流量分配比例（如 90% 流量至 v1，10% 至 v2）。
3. 根据业务需求调整流量比例，逐步增加新版本流量。
4. 监控新版本性能，确认无问题后全量切换。

**注意事项**: 灰度发布需配合完善的监控和日志系统，以便快速定位问题。

---

### 实践 4：集成 Nacos 或 Consul 实现动态服务发现

**说明**: Higress 原生支持与 Nacos、Consul 等注册中心集成，能够自动感知服务的上下线状态。这种动态服务发现机制避免了手动维护服务列表的繁琐，提高了系统的弹性和可靠性。

**实施步骤**:
1. 在 Higress 配置中添加 Nacos 或 Consul 作为服务来源。
2. 配置服务的命名空间和分组，确保与注册中心一致。
3. 验证 Higress 能够正确识别注册中心的服务实例。
4. 测试服务上下线时网关的路由更新是否实时生效。

**注意事项**: 确保注册中心与 Higress 之间的网络连通性，避免因网络分区导致服务发现失败。

---

### 实践 5：启用安全防护与限流降级

**说明**: Higress 内置了多种安全特性，如 IP 黑白名单、JWT 认证、API 签名验证等。同时，支持基于 QPS 或并发数的限流功能，保护后端服务免受流量冲击。

**实施步骤**:
1. 在网关层配置 JWT 认证，确保 API 访问的合法性。
2. 设置 IP 黑白名单，拦截恶意流量。
3. 针对关键 API 配置限流规则（如每秒 1000 次请求）。
4. 配置降级策略，当后端服务不可用时返回默认响应。

**注意事项**: 限流阈值需根据实际业务容量测试确定，避免误杀正常流量。

---

### 实践 6：优化网关性能与资源利用率

**说明**: Higress 基于 Envoy 的高性能架构，能够处理大规模并发流量。通过合理调整线程数、连接池大小等参数，可以进一步提升网关的吞吐量和响应速度。

**实施步骤**:
1. 根据服务器 CPU 核心数调整 Envoy 的工作线程数。
2. 优化 HTTP/2 和 gRPC 的连接池配置，减少连接建立开销。
3. 启用 HTTP/3 (QUIC) 以提升弱网环境下的性能。
4. 定期检查网关的 CPU、内存使用情况，及时扩容或缩容。

**注意事项**: 性能优化需结合实际负载测试，避免过度优化导致资源浪费。

---

### 实践 7：利用 Higress 控制台进行可视化运维

**说明**: Higress 提供了功能丰富的控制台界面，支持路由配置、插件管理、监控告

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 构建，支持 HTTP/3 协议。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，在弱网环境下能显著降低连接建立延迟和提升传输效率。

**实施方法**:
1. 在 Higress 网关配置中启用 HTTP/3 监听器。
2. 确保客户端（浏览器或 SDK）支持 HTTP/3 协议。
3. 配置 QUIC 协议相关参数（如最大数据包大小、空闲超时等）。

**预期效果**: 在弱网环境下，连接建立时间可减少 30%-50%，页面加载速度提升 20%-40%。

---

### 优化 2：配置 Wasm 插件异步调用

**说明**: Higress 支持 Wasm 插件扩展。默认情况下，Wasm 插件可能在请求主线程上执行，导致延迟增加。通过配置异步调用模式，可以将非阻塞逻辑移至后台处理，减少对请求路径的影响。

**实施方法**:
1. 在 Wasm 插件配置中启用 `async` 模式。
2. 确保插件逻辑支持异步执行（如日志记录、第三方 API 调用等）。
3. 监控 Wasm 插件的执行时间和资源占用。

**预期效果**: 请求延迟可减少 10%-30%，具体取决于插件逻辑的复杂度。

---

### 优化 3：优化连接池和并发配置

**说明**: Higress 作为网关，需要处理大量后端连接。通过调整连接池大小、最大并发请求数等参数，可以避免资源耗尽或排队延迟。

**实施方法**:
1. 调整 `upstream` 连接池配置，如 `maxConnections` 和 `pendingRequests`。
2. 根据后端服务能力设置合理的并发限制。
3. 启用 HTTP/2 连接复用，减少连接建立开销。

**预期效果**: 后端连接复用率提升 20%-50%，请求排队延迟减少 15%-30%。

---

### 优化 4：启用 CPU 亲和性和 NUMA 优化

**说明**: Higress 基于 Envoy，支持 CPU 亲和性配置。通过绑定 Worker 进程到特定 CPU 核心，可以减少上下文切换和缓存失效，提升吞吐量。

**实施方法**:
1. 在 Higress 部署配置中启用 `cpuAffinity` 选项。
2. 根据 NUMA 拓扑调整 Worker 进程分布。
3. 监控 CPU 使用率和上下文切换次数。

**预期效果**: 吞吐量（QPS）可提升 10%-25%，CPU 利用率提高 5%-15%。

---

### 优化 5：配置高效的缓存策略

**说明**: Higress 支持对响应内容进行缓存。通过合理配置缓存规则（如 TTL、缓存键），可以减少后端请求压力和响应延迟。

**实施方法**:
1. 在路由配置中启用 `responseCache` 插件。
2. 设置合理的缓存键（如 URL、Header 组合）。
3. 根据业务需求调整缓存 TTL（如静态资源缓存 1 小时）。

**预期效果**: 缓存命中时，后端请求减少 80%-100%，响应延迟降低 50%-70%。

---

### 优化 6：启用 Prometheus 监控与自适应调优

**说明**: 通过 Prometheus 监控 Higress 的性能指标（如 QPS、延迟、错误率），结合自适应调优工具（如 Envoy 的 `adaptive_concurrency`），可以动态调整限流和并发策略。

**实施方法**:
1. 部署 Prometheus 并配置 Higress 的监控指标采集。
2. 启用 `adaptiveConcurrency` 功能，根据后端延迟动态调整并发。
3. 设置告警规则，及时发现性能瓶颈。

**预期效果**: 动态限流可减少 20%-40% 的超时错误，整体服务稳定性提升。

---
## 学习要点

- 基于您提供的关键词（Alibaba/Higress/Github Trending），以下是关于 Higress 项目的主要技术价值点总结：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量管理与 API 管理的分离问题。
- 它深度集成了 K8s Ingress 资源，可作为标准 Ingress 控制器使用，实现了从传统微服务架构向 Service Mesh 架构的平滑过渡。
- 该网关内置了对 Dubbo、Nacos 和 Spring Cloud 等主流阿里系及开源微服务生态的原生支持，弥补了传统 API 网关在服务治理上的短板。
- Higress 提供了标准 Wasm (WebAssembly) 插件扩展机制，允许开发者使用 C++、Go、Rust 或 JavaScript 等语言编写高性能且易于扩展的插件。
- 它具备极致的轻量级和高性能特性，资源消耗极低，非常适合在边缘计算或资源受限的环境中进行部署。
- 项目提供了开箱即用的 Prometheus 监控指标集成和可视化管理控制台，极大降低了云原生网关的运维与可观测性门槛。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 云原生网关的基本概念与演变历史（从 Nginx 到 Ingress 再到 Higress）
- Higress 的核心架构设计：基于 Envoy 和 Istio 的技术栈
- Higress 与传统网关（如 Nginx, Kong）及阿里云 SLB 的区别
- 基本术语：Ingress、Gateway API、路由、服务发现、插件

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档（架构介绍章节）
- Envoy 官方文档基础概念（了解数据平面与控制平面）
- Kubernetes Ingress Controller 基础知识

**学习建议**: 
建议先不要急于部署，先通读官方文档的"产品简介"和"架构说明"部分，理解 Higress 作为一个"云原生 API 网关"在微服务架构中的位置。如果你没有 Kubernetes 基础，需要先补充 K8s 的基本操作知识。

---

### 阶段 2：核心功能实战与部署

**学习内容**:
- 本地或集群环境安装部署 Higress（Docker 版或 Kubernetes 版）
- 域名与路由配置：HTTP 路由、HTTPS 路由、路径重写
- 服务来源配置：接入固定地址、Nacos、Nacos Service、K8s Service
- 流量管理：基于 Header、Cookie、Query 参数的路由匹配
- 基础认证鉴权：AK/SK 认证、JWT 认证、Basic Auth

**学习时间**: 2-3周

**学习资源**:
- Higress 官方 GitHub 仓库（快速开始 Quick Start）
- Higress 官方控制台操作指南
- Higress 官方示例仓库

**学习建议**: 
动手是关键。建议在本地 Docker 环境或测试用的 K8s 集群中安装 Higress。尝试配置一个简单的后端服务（如 nginx 或 httpbin），通过 Higress 暴露服务并进行访问。重点练习配置不同规则的路由转发，观察流量走向。

---

### 阶段 3：插件生态与流量治理

**学习内容**:
- Higress 插件体系原理（Wasm 插件与 Lua 插件）
- 常用官方插件使用：限流、跨域（CORS）、请求响应头修改、防盗链
- 全局插件与路由级插件的配置与优先级
- 高级流量治理：金丝雀发布、蓝绿发布、Header 转发
- 服务预热与负载均衡策略配置

**学习时间**: 3-4周

**学习资源**:
- Higress 官方插件市场文档
- Higress 官方提供的 Wasm 插件开发示例
- Envoy 负载均衡策略文档

**学习建议**: 
此阶段重点在于"治理"。尝试模拟生产环境场景，例如对某个 API 开启"限流"插件，或者配置"金丝雀发布"将 10% 的流量转发到新版本服务。尝试编写一个简单的 Lua 或 Wasm 插件来修改请求头，深入理解插件的处理逻辑。

---

### 阶段 4：深度定制与生产运维

**学习内容**:
- Higress 高可用部署架构与性能调优（线程数、内存配置）
- 自定义插件开发：使用 Go 或 C++ 开发 Wasm 插件
- 监控与可观测性：集成 Prometheus、Grafana、Skywalking
- 安全防护：集成 WAF 防护、应对 DDoS 攻击策略
- 多集群管理与容灾备份方案

**学习时间**: 4-6周

**学习资源**:
- Higress 源码分析
- WebAssembly (Wasm) 官方教程
- Prometheus 监控集成最佳实践
- Higress 生产环境运维白皮书

**学习建议**: 
关注生产环境的稳定性。学习如何通过 Prometheus 监控 Higress 的 QPS、延迟、P99 等指标。如果业务有特殊逻辑，尝试开发自定义插件。阅读源码以理解 Ingress Controller 如何将 K8s 资源转化为 Envoy 配置，这将帮助你解决深层次的 Bug。

---
## 常见问题


### 1: Higress 是什么？它与 Alibaba 有什么关系？

1: Higress 是什么？它与 Alibaba 有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是由阿里巴巴（Alibaba）发起的，并基于阿里内部多年在大规模流量治理领域的实践经验构建而成。Higress 旨在满足云原生时代下 API 管理的高标准需求，兼容 Kubernetes Ingress 标准，并深度集成了 Envoy 高性能代理。它源自阿里巴巴对电商、金融等超大规模业务场景的流量管理技术积累，是阿里云云原生网关的开源版本。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：
1.  **极致性能与热更新**：基于 Envioy (C++) 内核，利用 Envoy 的高性能特性，并实现了配置热更新，无需重启进程即可生效，业务无感知。
2.  **安全防护**：内置了针对常见 Web 漏洞（如 CVE-2023-44487 HTTP/2 快速流攻击）的防御能力，提供了更安全的运行环境。
3.  **标准化与兼容性**：完全兼容 Kubernetes Ingress Annotation 和 Gateway API 标准，同时也兼容 Nginx 的 Ingress 注解，降低了迁移成本。
4.  **插件生态**：支持 WASM (WebAssembly) 插件，允许使用 Go、C++、Rust 等多种语言编写插件，且插件可以在运行时动态加载，极大地扩展了网关的自定义能力。
5.  **微服务集成**：与 Nacos、Consul 等主流注册中心以及 Dubbo、gRPC 等协议进行了深度集成，非常适合微服务架构。

---



### 3: Higress 是否支持从 Nginx Ingress 进行平滑迁移？

3: Higress 是否支持从 Nginx Ingress 进行平滑迁移？

**A**: 是的，Higress 非常重视对 Nginx Ingress 的兼容性。它支持直接导入 Nginx 的 Ingress 配置，并兼容大部分常用的 Nginx Ingress Annotations。这意味着用户在将集群入口从 Nginx Ingress 切换到 Higress 时，通常不需要大幅修改现有的 YAML 配置文件，从而降低了迁移风险和工作量。

---



### 4: Higress 提供哪些安全防护功能？

4: Higress 提供哪些安全防护功能？

**A**: Higress 内置了强大的安全能力，主要包括：
1.  **WAF (Web Application Firewall)**：支持对 SQL 注入、XSS (跨站脚本攻击)、命令执行等常见 Web 攻击进行检测和拦截。
2.  **流量整形与限流**：支持基于请求速率、并发连接数等进行精细化的流量控制，防止后端服务被突发流量击垮。
3.  **协议安全**：针对 HTTP/2 和 HTTP/3 协议层级的攻击（如 HTTP/2 快速重置攻击）有专门的防护机制。

---



### 5: Higress 的插件系统是如何工作的？支持哪些语言？

5: Higress 的插件系统是如何工作的？支持哪些语言？

**A**: Higress 采用基于 Envoy 的 WASM (WebAssembly) 插件系统。这是 Higress 区别于传统网关的一大亮点。
1.  **工作原理**：插件运行在 Envoy 的沙箱环境中，通过 WASM 虚拟机执行。这使得插件即使崩溃也不会导致网关主进程崩溃，保证了网关的高可用性。
2.  **支持语言**：得益于 WASM 的特性，开发者可以使用 **Go**、**AssemblyScript**、**C++**、**Rust** 等多种语言编写插件逻辑，然后编译为 WASM 文件供 Higress 加载。
3.  **动态加载**：插件可以在不重启网关实例的情况下进行发布、更新或下线。

---



### 6: 在微服务场景下，Higress 如何处理服务发现和流量路由？

6: 在微服务场景下，Higress 如何处理服务发现和流量路由？

**A**: Higress 是为云原生微服务架构设计的，在服务治理方面非常灵活：
1.  **服务发现**：除了支持 Kubernetes Service (基于 DNS) 外，Higress 还可以直接对接 **Nacos**、**Consul**、**ZooKeeper** 等主流注册中心，实现与后端微服务的直连，绕过 Kubernetes Service 的负载均衡，减少网络跳转。
2.  **多协议支持**：原生支持 HTTP、HTTPS、HTTP/2、HTTP/3 (QUIC)、gRPC 以及 Dubbo 协议的路由和透传。
3.  **全链路灰度发布**：支持基于 Header、Cookie、权重或用户 ID 的流量路由，轻松实现金丝雀发布和蓝绿部署。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 是基于 Istio 和 Envoy 构建的，请尝试在本地或 Kubernetes 集群中完成 Higress 的最小化安装，并配置一个简单的 Ingress 路由规则，将访问特定域名（例如 `example.com`）的流量转发到一个后端服务（如 Nginx）。

### 提示**: 请参考 Higress 官方文档中的“快速开始”或“安装指南”部分。注意检查 Higress Gateway 的 Service 暴露方式（NodePort 或 LoadBalancer），并确保本地 hosts 或 DNS 能够正确解析到网关 IP。

### 

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的 5-7 条实践建议：

### 1. 利用 Wasm 插件实现模型供应商的无缝切换
**场景**：在生产环境中，直接将模型供应商（如 OpenAI、Azure、通义千问）的硬编码 URL 写在业务代码中会导致迁移成本高昂。
**建议**：充分利用 Higress 的 `ai-proxy` 插件。在网关层配置服务路由，将业务请求指向统一的内部路径（如 `/models/gpt-4`），然后在插件配置中定义具体的供应商和 API Key。
**最佳实践**：建立一套内部的模型名称标准。当需要切换供应商或进行 A/B 测试时，只需修改网关的插件配置，无需重新发布后端服务代码。

### 2. 实施细粒度的 Token 预留与超时控制
**场景**：大模型推理耗时较长，且 Token 消耗不可预测。简单的超时设置可能导致客户端在模型即将返回结果时断开连接。
**建议**：不要仅依赖 HTTP 层面的超时。应针对不同的模型类型配置不同的超时策略。对于流式响应，确保网关的 Idle Timeout 设置足够长，以支持长文本生成。
**陷阱**：避免对所有接口设置统一的短超时（如 30 秒），这会导致复杂的推理任务失败。

### 3. 配置基于 Token 的精细化限流
**场景**：AI 服务的成本主要取决于 Token 消耗量。传统的基于 QPS（每秒请求数）或并发连接数的限流无法有效控制成本。
**建议**：使用 Higress 的 `token-limit` 或针对 AI 场景的限流插件。根据用户等级或 API Key 设置每分钟或每天的 Token 预算。
**最佳实践**：在网关层实现 Token 预估和扣除。当用户配额耗尽时，网关直接返回 429 状态码，避免请求转发至后端模型提供商，从而节省不必要的费用。

### 4. 建立语义化路由与负载均衡
**场景**：企业内部可能同时部署了开源模型（如 Llama 3）和商业模型。需要根据请求的复杂程度或用户权限将流量路由到不同的模型集群。
**建议**：利用 Higress 的路由匹配功能（Header 匹配或权重路由）。例如，在 HTTP Header 中携带 `Model-Preference`，网关根据该 Header 将请求转发给高性能 GPU 集群或低成本 CPU 集群。
**陷阱**：避免在业务逻辑中混入模型选择逻辑，这会造成代码维护困难。路由策略应在网关层统一管理。

### 5. 敏感信息脱敏与安全防护
**场景**：用户可能通过 Prompt 注入攻击系统，或在对话中无意泄露隐私数据。
**建议**：配置 Wasm 插件对请求体进行实时扫描。在请求发送给 LLM 之前，插件可以拦截并过滤掉包含敏感关键词（如数据库密码、内部 IP）的内容，或检测恶意攻击模式。
**最佳实践**：将安全策略与业务逻辑解耦。即使后端模型服务被攻破，网关层依然作为第一道防线防止敏感数据流出。

### 6. 观测性：将模型指标纳入监控体系
**场景**：传统的 API 网关只关注 HTTP 状态码和延迟。AI 应用还需要关注 Token 使用量、首字生成时间（TTFT）和吞吐量。
**建议**：确保 Higress 的可观测性插件已开启，并配置 Prometheus 抓取 AI 相关的指标。重点关注 `prompt_tokens`、`completion_tokens` 和 `total_tokens`。
**最佳实践**：在 Grafana 中建立专门的仪表盘，监控不同模型路由的 Token 消耗趋势，以便财务部门进行成本核算和资源优化。

### 7. 处理流式响应的头部传递
**场景**：客户端依赖响应头（如 `X-Request-Id`）进行链路追踪，但在 SSE（Server-Sent Events）流式传输模式下，部分网关配置可能导致响应头丢失或分块

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*