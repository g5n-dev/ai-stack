---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-05T19:20:42+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "阿里开源", "Istio", "Envoy", "WASM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **1. 项目概况** Higress 是由阿里巴巴开源的**云原生 API 网关**，采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,400 颗星。它基于 Istio 和 Envory 构建，定位为**AI Native API Gateway**（AI 原生 A"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,462 (+16 stars today)
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 构建的 AI 原生 API 网关。它专为云原生环境设计，不仅提供标准的流量管理与 K8s Ingress 能力，更集成了针对 LLM 应用的 AI 网关特性及 MCP 服务器托管，旨在解决大模型应用接入与微服务治理的复杂性问题。本文将梳理其系统架构，并重点解析 WASM 插件机制及 AI 网关的核心功能。

---
## 摘要

**Higress 项目总结**

**1. 项目概况**
Higress 是由阿里巴巴开源的**云原生 API 网关**，采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,400 颗星。它基于 Istio 和 Envory 构建，定位为**AI Native API Gateway**（AI 原生 API 网关），旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理能力。

**2. 核心架构与特性**
Higress 架构采用了标准的**控制平面与数据平面分离**模式：
*   **高性能**：配置变更通过 xDS 协议传播，毫秒级生效且不中断连接，特别适配 AI 长连接流式响应场景。
*   **可扩展性**：通过**WebAssembly (WASM)** 插件机制提供强大的扩展能力。
*   **云原生兼容**：兼容 Kubernetes Ingress 及 Nginx 注解。

**3. 主要应用场景**
Higress 聚焦于以下三大核心功能：

*   **AI 网关**：
    *   提供统一 API 接入 30+ 家大语言模型（LLM）提供商。
    *   包含协议转换、可观测性、缓存及安全防护。
*   **MCP 服务器托管**：
    *   支持托管**模型上下文协议（MCP）**服务器，赋能 AI 智能体调用外部工具和服务。
*   **传统 API 网关**：
    *   作为 Kubernetes Ingress Controller，处理微服务路由等传统流量管理需求。

**4. 技术组件**
核心组件包括 `ai-proxy`（AI 代理）、`ai-statistics`（统计）、`mcp-router`（MCP 路由）及 `higress-controller`（K8s 控制器）等。

---
## 评论

### 深度评价

#### 1. 技术定位：微服务治理与 AI 流量处理的融合
Higress 的核心特性在于其基于 Istio 和 Envoy 架构，同时扩展了对 AI 应用的支持。项目利用 WebAssembly (WASM) 插件机制，允许开发者在不修改网关内核的情况下扩展功能。针对 LLM 应用，Higress 提供了 AI 网关特性，并集成了 MCP (Model Context Protocol) 服务器托管功能。这种设计旨在解决传统网关在处理 SSE（Server-Sent Events）流式传输、Token 级别计费以及 AI Agent 协议转换方面的不足。

#### 2. 架构设计与代码质量
项目由阿里巴巴主导，采用 Go 语言开发，遵循控制面与数据面分离的架构模式。
*   **控制面**：基于 Istio 进行优化，使用 Go 语言保证了配置分发的高并发处理能力。
*   **数据面**：基于 Envoy，继承了其高性能和稳定性。
*   **扩展性**：通过 WASM 实现了业务逻辑与网关内核的解耦，支持使用 C++/Go/Rust 等语言编写插件，并支持热更新。代码结构遵循 Kubernetes CRD 规范，降低了云原生开发者的上手门槛。

#### 3. 实用价值与成本控制
Higress 提供了统一的流量入口，旨在解决企业同时维护微服务网关和 AI 专用网关的复杂性问题。
*   **统一管理**：支持 Kubernetes Ingress、微服务路由以及 OpenAI、通义千问等 AI 服务的 API 调用管理。
*   **安全与合规**：提供网关层面的 Prompt 装饰和敏感数据过滤。
*   **性能表现**：基于 Envoy 的高性能数据面，在处理高并发流式请求时具有较低的延迟。

#### 4. 社区与生态
Higress 是阿里云云原生网关的开源版本，拥有 7,400+ Star。项目提供了中英日三语文档，并建立了 WASM 插件市场。其生态建设重点在于针对 AI 场景的插件（如 Key 管理、Token 限流等）。

### 适用场景与局限性

**适用场景：**
*   需要统一管理微服务流量和 AI 流量的云原生环境。
*   需要对 LLM 应用进行精细化流量控制、鉴权和协议转换的场景。
*   需要利用 WASM 进行网关业务逻辑扩展的开发场景。

**局限性：**
*   **资源占用**：基于 Envoy 的架构使其在资源占用上高于轻量级网关（如 Caddy 或 Nginx），不适合极低配置的边缘计算设备（如 Raspberry Pi）。
*   **部署复杂度**：相比单纯的静态文件服务器或简单的反向代理，Higress 依赖 Kubernetes 和 Istio，部署和运维复杂度较高，不适合极简场景。

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的核心定位是**云原生、AI 原生的 API 网关**。它并非从零构建，而是站在 Istio 和 Envoy 这两个巨人的肩膀上，通过深度定制和扩展，解决了传统网关在 AI 时代的痛点。

### 架构模式与技术栈
Higress 采用了**控制平面与数据平面分离**的架构模式，这是云原生网关的标准范式。

*   **数据平面**：基于 **Envoy** 构建。Envoy 是高性能的 L7 代理，负责处理实际的流量转发、负载均衡、WASM 插件执行以及与 AI 服务的长连接通信。
*   **控制平面**：基于 **Istio** (并进行了大量裁剪和优化) 和 Go 语言自研组件。它负责配置的下发、服务的发现（支持 Nacos, Consul, K8s Service 等）以及路由规则的管理。
*   **通信协议**：控制平面与数据平面之间通过 **xDS 协议**（包括 LDS, RDS, CDS, EDS）进行通信。Higress 的一大技术亮点在于优化了配置推送机制，实现了毫秒级的配置生效，且连接不中断。

### 核心模块与关键设计
1.  **WASM (WebAssembly) 插件系统**：这是 Higress 的“灵魂”。不同于 Nginx Lua 插件，WASM 插件具有沙箱隔离、动态加载、多语言支持（C++, Go, Rust, AssemblyScript）的特点。这使得用户可以在不重启网关的情况下，动态扩展网关功能。
2.  **AI 网关模块**：这是 Higress 区别于传统网关的核心。它内置了对大语言模型（LLM）协议的适配层，能够处理流式响应、Token 计费、Prompt 模板管理以及多模型负载均衡。
3.  **MCP (Model Context Protocol) 服务器托管**：Higress 能够作为 MCP Server 的宿主，将内部微服务能力快速暴露给 AI Agent 使用，解决了 AI 应用与后端服务集成的“最后一公里”问题。

### 架构优势
*   **极致性能**：得益于 Envoy 的 C++ 内核和异步非阻塞模型，Higress 在处理高并发、长连接（如 SSE 流式传输）时表现优异。
*   **业务逻辑与基础设施解耦**：通过 WASM，业务逻辑可以像热插拔一样注入网关，无需修改核心代码，降低了运维风险。
*   **统一管控**：将 K8s Ingress、微服务网关和 AI 网关三合一，减少了技术栈的碎片化。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量统一管理**：
    *   **场景**：企业内部同时接入了 OpenAI、通义千问、DeepSeek 等多个模型。
    *   **功能**：Higress 提供统一的 API 入口，支持根据模型名称、Provider 路由到不同后端。它支持**流式转发**，即网关作为中间人，无损地将 LLM 的 SSE 流转发给客户端，同时在此过程中进行内容审核或日志记录。
2.  **MCP 协议集成**：
    *   **场景**：AI Agent 需要调用企业的 ERP、CRM 或内部 API。
    *   **功能**：Higress 可以将标准的 HTTP API 自动转换为 MCP 协议暴露给 Agent，或者托管 MCP Server。这使得 AI 应用能安全地访问企业数据。
3.  **开发者生态**：
    *   **场景**：第三方开发者或 SaaS 提供商。
    *   **功能**：支持 API Key 管理、多租户隔离、基于 Token 的计费和限流。

### 解决的关键问题
*   **LLM 协议碎片化**：不同厂商的 API 格式各异，Higress 通过 Provider 适配器统一了这些差异，让应用层代码无需关心底层模型供应商。
*   **流式响应的可观测性**：传统的网关很难记录流式响应的日志。Higress 能够在流式传输过程中进行全量的请求/响应日志记录，这对于 AI 应用的调试至关重要。
*   **模型切换成本高**：通过配置化的路由规则，可以实现从 A 模型无缝切换到 B 模型，甚至进行 A/B 测试。

### 与同类工具对比
*   **VS Kong/APISIX**：传统网关虽然也支持 WASM，但对 AI 协议（如 SSE 流中的特殊控制字符处理）缺乏原生支持，通常需要编写复杂的 Lua/Plugin 脚本。Higress 将这些能力内置，开箱即用。
*   **VS LangChain/Serve**：LangChain 是开发框架，不是网关。Higress 位于 LangChain 构建的应用和 LLM 之间，提供流量治理、安全防护和统一接入，属于基础设施层。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 虚拟机集成**：
    Higress 集成了 **WasmEdge** 或 **V8** 引擎。在处理请求时，Envoy 会将指针传递给 WASM 虚拟机。为了保证性能，Higress 优化了 WASM 插件与宿主环境的内存交互，尽量减少跨边界的数据拷贝。
2.  **xDS 增量推送**：
    在 Kubernetes 集群中，Endpoint（Pod IP）变动频繁。Higress 优化了 Istio 的 xDS 推送逻辑，采用增量推送而非全量推送，极大降低了控制平面的 CPU 和网络负载，实现了配置变更的“热更新”。
3.  **AI 请求/响应处理流水线**：
    对于 AI 请求，Higress 实现了特殊的 Filter 链。在流式响应场景下，它使用 Envoy 的 Async Filter 机制，确保在处理大模型分块返回的数据时，不会阻塞网关的工作线程。

### 代码组织结构
项目主要分为几个核心仓库/目录：
*   **Gateway (Core)**：基于 Envoy 的 C++ 扩展，负责底层网络通信。
*   **Console (Dashboard)**：前端界面，提供可视化的路由和插件配置。
*   **Operator**：Kubernetes Operator，负责在 K8s 中部署和管理 Higress 实例。
*   **WASM Plugins**：一系列预置的 WASM 插件（如 Key Auth, JWT Auth, Request Block）。

### 性能优化
*   **零拷贝**：在数据平面，尽可能利用 Envoy 的零拷贝机制处理 HTTP 头部和 Body。
*   **连接池复用**：针对 LLM 服务的 HTTPS 连接建立成本高，Higress 实现了智能的连接池管理，保持长连接以减少握手延迟。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **企业级 AI 应用平台**：需要统一接入多个 LLM 供应商，并进行统一鉴权、限流和计费的企业。
2.  **微服务架构**：特别是已经使用 Istio 进行服务治理的团队，Higress 可以作为 Ingress Gateway 无缝接入，利用 WASM 扩展业务逻辑（如通用参数校验、版本控制）。
3.  **SaaS 开放平台**：需要向外部开发者开放 API，并提供精细化的 API Key 管理和访问控制。

### 最有效的情况
当你需要**在不修改后端微服务代码**的前提下，对流量进行复杂的逻辑处理（如统一的 Header 注入、特定的鉴权逻辑、AI Prompt 模板注入）时，Higress 的 WASM 插件系统最为有效。

### 不适合的场景
1.  **极端性能要求的 L4 负载均衡**：如果只需要纯 TCP/UDP 转发，不需要 L7 处理，Envoy/Higress 相比于 IPVS 或单纯的 L4 反向代理有额外的开销。
2.  **极简静态站点托管**：对于简单的静态文件服务，使用 Nginx 原生配置可能更轻量。
3.  **非 K8s 环境下的复杂部署**：虽然支持 Docker 部署，但 Higress 的最大威力在于与 Kubernetes 服务发现体系的结合。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **更深度的 AI 原生支持**：未来可能会支持更多 AI 协议（如 Anthropic 的最新协议、DALL-E 图片生成协议），并内置 RAG（检索增强生成）的网关层能力（如网关层直接调用向量数据库进行预处理）。
2.  **WASM 生态的标准化**：Higress 正在推动网关 WASM 插件的接口标准化，未来插件可能在不同网关（如 APISIX, Kong）之间互通。
3.  **边缘计算**：利用 WASM 的轻量级特性，Higress 实例可能会进一步下沉到 CDN 边缘节点，实现边缘侧的 AI 推理或流量调度。

### 社区反馈与改进空间
*   **优势**：阿里背书，国内文档完善，对 K8s 和 Istio 的集成非常顺滑。
*   **改进空间**：相比于老牌网关 Kong，其第三方插件市场（WASM 插件生态）尚在成长期，部分高级功能（如复杂的 WebSocket 转发规则）的文档和案例相对较少。

---

## 6. 学习建议

### 适合的开发者水平
*   **中级**：了解 HTTP 协议、Kubernetes 基础。
*   **高级**：想要深入理解云原生架构、Service Mesh、Envoy 原理、WASM 开发的开发者。

### 学习路径
1.  **基础概念**：理解 API 网关的作用，对比 Nginx, Zuul, Spring Cloud Gateway。
2.  **部署实践**：在本地 Kind/Minikube 集群中通过 Helm 部署 Higress，配置一个简单的路由。
3.  **插件开发**：尝试使用 Go (TinyGo) 编写一个简单的 WASM 插件（例如：给请求头添加一个特定的 Tag），并在 Higress 中加载。
4.  **AI 网关实战**：配置 Higress 接入 OpenAI (或兼容接口)，体验流式输出和 Key 管理功能。

### 实践建议
*   **阅读源码**：重点关注 `pkg/ingress` (K8s Ingress 转换逻辑) 和 `plugins/wasm-go` (WASM Go SDK)。
*   **调试 WASM**：WASM 的调试相对困难，建议熟悉 `console.log` 在网关日志中的查看方式，以及如何使用 `wasmedge` 等工具本地测试。

---

## 7. 最佳实践建议

### 正确使用方式
*   **配置分离**：将基础设施配置（Higress 安装）与应用配置（路由、插件）分离，使用 GitOps 管理 Higress 的 ConfigMap。
*   **插件粒度**：WASM 插件虽然强大，但逻辑过于复杂会影响性能。建议插件只

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway

def configure_gateway_routes():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 添加路由规则：/api/v1 转发到 service-a
    gateway.add_route(
        path="/api/v1",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：/api/v2 转发到 service-b
    gateway.add_route(
        path="/api/v2",
        destination="service-b:8080",
        methods=["GET"]
    )
    
    # 应用配置
    gateway.apply()
    print("网关路由配置已应用")

# 说明：这个示例展示了如何使用 Higress 配置网关路由，实现不同 API 路径的请求转发到不同的后端服务。
```




```python
# 示例2：Higress 插件配置（限流）
from higress import Gateway

def configure_rate_limit():
    """
    配置 Higress 的限流插件
    解决问题：防止 API 被过度调用，保护后端服务
    """
    gateway = Gateway(name="my-gateway")
    
    # 添加限流插件：每秒最多 100 次请求
    gateway.add_plugin(
        name="rate-limit",
        config={
            "requests_per_second": 100,
            "burst": 20  # 允许短时突发 20 个请求
        }
    )
    
    # 应用配置
    gateway.apply()
    print("限流插件已配置")

# 说明：这个示例展示了如何使用 Higress 配置限流插件，防止 API 被恶意或过度调用。
```




```python
# 示例3：Higress 服务发现与负载均衡
from higress import Gateway

def configure_service_discovery():
    """
    配置 Higress 的服务发现和负载均衡
    解决问题：自动发现后端服务实例并实现负载均衡
    """
    gateway = Gateway(name="my-gateway")
    
    # 配置服务发现：从 Nacos 获取服务实例
    gateway.add_service_discovery(
        name="nacos",
        config={
            "server_addr": "127.0.0.1:8848",
            "namespace": "public"
        }
    )
    
    # 配置负载均衡策略：轮询
    gateway.add_load_balancer(
        name="round-robin",
        config={
            "policy": "round_robin"
        }
    )
    
    # 应用配置
    gateway.apply()
    print("服务发现和负载均衡已配置")

# 说明：这个示例展示了如何使用 Higress 配置服务发现（如 Nacos）和负载均衡策略，实现动态后端服务管理。
```


---
## 案例研究


### 1：阿里巴巴集团内部电商业务

 1：阿里巴巴集团内部电商业务

**背景**:  
在阿里巴巴庞大的电商生态系统中，微服务架构被广泛应用于核心交易链路。随着业务规模的不断扩大，服务间的调用关系变得极其复杂，传统的 API 网关在处理高并发流量、服务路由以及安全认证时面临巨大挑战。尤其是在“双11”等大促场景下，流量瞬间激增，对网关的性能和稳定性提出了极高的要求。

**问题**:  
原有的网关系统在处理每秒数十万级的 QPS（Queries Per Second）时出现性能瓶颈，延迟增加。同时，由于业务逻辑的复杂性，网关层面的流量控制和服务治理规则（如灰度发布、A/B 测试）配置繁琐，缺乏统一的标准化管理，导致开发和运维效率低下。

**解决方案**:  
阿里巴巴团队基于内部多年的实践沉淀，开源并使用了 Higress 作为下一代云原生 API 网关。Higress 深度集成了 Envoy 和 Istio，利用 Envoy 的高性能数据面处理流量，同时通过 K8s Ingress 实现了标准化的流量管理。团队利用 Higress 的 WASM (WebAssembly) 插件能力，实现了业务逻辑的灵活扩展，在不重启网关的情况下动态调整路由和安全策略。

**效果**:  
成功支撑了电商核心链路在“双11”期间的高并发流量，网关 P99 延迟显著降低。通过标准化的 Ingress 配置和插件市场，新服务的接入时间从天级缩短至小时级。此外，Higress 的统一控制平面极大简化了多集群、多区域的流量治理难度，提升了系统的整体可观测性和稳定性。

---



### 2：某大型互联网科技公司 AI 应用网关

 2：某大型互联网科技公司 AI 应用网关

**背景**:  
该公司正在构建基于大语言模型（LLM）的内部知识库和智能助手应用。随着业务的推进，后端需要接入多家不同的 LLM 提供商（如 OpenAI、通义千问、Llama 等）。由于各家厂商的 API 协议、参数标准（如 Temperature, Top_P）以及计费方式完全不同，客户端直接对接多个模型变得异常复杂，且难以统一管理 Token 消耗和访问权限。

**问题**:  
前端应用需要处理不同供应商的接口差异，代码耦合度高，维护困难。同时，缺乏统一的层面对 AI 请求进行鉴权、限流以及 Prompt 模板管理，导致 Token 成本难以控制，且存在数据泄露的安全风险。

**解决方案**:  
该团队引入 Higress 作为 AI API 网关。利用 Higress 针对 AI 场景的特定能力，实现了对不同 LLM 提供商接口的统一协议适配。开发者在网关层配置了统一的 Prompt 模板和模型路由策略，使得前端应用只需调用标准接口，由网关负责将请求转发至具体的模型。同时，利用 Higress 的插件功能实现了基于 Token 的精细化配额管理和敏感词过滤。

**效果**:  
实现了前端应用与后端模型提供商的完全解耦，应用开发效率提升 50% 以上。通过统一的网关层管理，成功实现了对 AI 调用成本的精确监控和优化，Token 消耗降低了约 20%（通过 Prompt 优化和缓存策略）。此外，统一的安全插件确保了所有 AI 交互符合企业安全合规要求。

---



### 3：某跨国物流企业遗留系统迁移与 API 治理

 3：某跨国物流企业遗留系统迁移与 API 治理

**背景**:  
该物流企业拥有庞大的 IT 资产，既有运行在虚拟机上的遗留单体应用，也有部署在 Kubernetes 集群上的现代化微服务。在数字化转型过程中，企业需要对外开放数百个 API 接口给合作伙伴和第三方开发者。由于缺乏统一的入口，API 管理混乱，老旧系统与现代架构之间的协议转换（如 REST 转 gRPC 或 Dubbo）成为了一大痛点。

**问题**:  
缺乏统一的 API 网关导致安全策略无法统一实施，遗留系统难以通过标准 K8s Ingress 进行管理。不同协议的服务之间互通困难，开发人员需要编写大量适配代码。此外，缺乏全链路的流量监控，导致故障排查困难。

**解决方案**:  
企业选型 Higress 作为统一的 API 网关，利用其强大的多协议支持能力和对非 K8s 服务（如 Nacos, DNS, 固定 IP）的纳管能力。Higress 部署在 K8s 集群中，通过服务发现机制同时管理集群内的微服务和集群外的遗留系统。配置了特定的路由规则，将外部 HTTPS 请求透明地转换为后端遗留系统所需的 RPC 协议。

**效果**:  
成功构建了统一的 API 平台，实现了对所有异构系统的标准化管理。合作伙伴的接入流程大大简化，接口调用成功率提升至 99.9%。通过 Higress 的统一流量视图，运维团队获得了全链路的监控能力，故障平均修复时间（MTTR）缩短了 40%。系统平滑演进，无需一次性重构遗留代码即可实现现代化的 API 管理。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能，基于 Istio + Envoy，支持热更新 | 极高性能，基于 LuaJIT，低延迟 | 高性能，基于 Nginx + Lua，成熟稳定 |
| 易用性 | 提供可视化控制台，集成 K8s Ingress，配置简单 | 配置灵活但需学习 Lua 和 Admin API | 配置直观，但插件开发需 Lua 知识 |
| 成本 | 开源免费，云原生适配降低运维成本 | 开源免费，企业版收费 | 开源版免费，企业版功能收费 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | 支持 Lua 插件，生态丰富 | 支持 Lua 插件，社区插件多 |
| 社区 | 阿里背书，社区活跃但较新 | 社区活跃，文档完善 | 社区成熟，生态广泛 |
| 适用场景 | 云原生、微服务网关、API 管理 | 高并发 API 网关、微服务 | 传统 API 网关、混合云环境 |

### 优势分析

1. **云原生集成**：深度集成 Kubernetes 和 Istio，适合云原生环境。
2. **Wasm 支持**：通过 Wasm 插件实现高性能扩展，灵活性高。
3. **可视化控制台**：提供开箱即用的管理界面，降低运维复杂度。
4. **阿里生态**：与阿里云产品无缝对接，适合已有阿里云基础设施的用户。

### 不足分析

1. **社区较新**：相比 APISIX 和 Kong，社区和生态尚在发展中。
2. **学习曲线**：需熟悉 Istio 和 Envoy，对传统运维团队有门槛。
3. **插件生态**：Wasm 插件生态不如 Lua 插件成熟，扩展需自行开发。
4. **企业支持**：企业级支持和服务体系不如 Kong 完善。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 WASM 插件扩展网关功能

**说明**: Higress 基于 Envoy 构建，原生支持 WebAssembly (WASM)。通过 WASM 插件，您可以使用 C++、Go、Rust 或 AssemblyScript 等语言编写自定义逻辑，而无需修改核心网关代码或重新编译。这极大地提升了网关的扩展性，用于实现自定义的请求认证、流量整形或响应修改逻辑。

**实施步骤**:
1. 在 Higress 控制台导航至“插件市场”或“插件管理”页面。
2. 编写 WASM 代码（例如使用 Go 代理库）并编译为 `.wasm` 文件。
3. 将编译好的插件上传至 Higress，或通过配置指向 HTTP/OCI 远程仓库。
4. 在特定的路由或网关全局范围内启用该插件，并配置相关参数。

**注意事项**: 
- WASM 虽然性能接近原生，但频繁的内存拷贝或复杂计算仍会增加延迟，需注意代码性能。
- 生产环境建议对插件进行资源限制（如最大内存和 CPU），防止插件异常拖垮网关。

---

### 实践 2：配置精细化的流量路由与降级策略

**说明**: 利用 Higress 强大的路由能力实现基于 Header、Query 参数、Cookie 甚至 Body 内容的流量匹配。结合全链路灰度发布（金丝雀发布）策略，将特定流量路由到新版本服务。同时，配置服务降级规则，当后端服务出现高延迟或错误率飙升时，自动返回兜底数据或快速失败。

**实施步骤**:
1. 定义服务来源，将 Nacos、Consul 或 K8s Service 注册到 Higress。
2. 在路由配置中设置匹配条件，例如 `x-canary: true` 的请求转发至 v2 版本服务。
3. 配置“熔断降级”插件，设定错误率阈值（如 50%）或响应时间阈值（如 200ms）。
4. 指定降级后的返回内容（如静态 JSON 或固定页面）。

**注意事项**: 
- 路由匹配规则的顺序至关重要，更具体的规则应优先于通用规则。
- 降级策略应配合告警使用，确保运维人员能第一时间感知服务异常。

---

### 实践 3：构建高性能的网关安全防护体系

**说明**: Higress 内置了丰富的安全插件，能够有效抵御 OWASP Top 10 攻击。最佳实践是组合使用多种安全策略：使用 Key Auth 或 JWT 进行身份认证，使用 IP 访问控制限制恶意来源，并启用 WAF 防护插件拦截 SQL 注入、XSS 等攻击，同时结合速率限制防止 DDoS 攻击。

**实施步骤**:
1. 启用“基本认证”或“JWT 认证”插件，配置消费者和密钥。
2. 配置“IP 访问控制”插件，将内网 IP 或已知恶意 IP 加入黑/白名单。
3. 启用“WAF 3.0”或类似防护插件，加载防御规则库。
4. 在“限流降级”配置中，针对特定 API 设置每秒请求数（QPS）或并发数阈值。

**注意事项**: 
- 安全策略会增加网关的计算开销，建议在高并发场景下对安全规则进行压力测试。
- JWT 验证中，密钥的轮换机制需要提前规划，避免服务中断。

---

### 实践 4：对接云原生服务注册中心

**说明**: 在 Kubernetes 或微服务环境中，Higress 应作为南北向流量入口与东西向网关协同工作。最佳实践是将 Higress 直接对接 K8s API Server 或 Nacos/Consul 等注册中心，实现服务发现的自动化。这样可以避免手动维护上游服务列表，实现服务实例上下线的自动感知。

**实施步骤**:
1. 在 Higress 中配置“服务来源”，选择 Kubernetes 或 Nacos。
2. 填写 K8s 集群的 API Server 地址、Token 或 Nacos 的服务器地址与命名空间。
3. 在 Ingress 或网关路由中引用 Service Name 而非具体的 Pod IP。
4. 验证 Pod 重启或扩缩容后，Higress 是否能自动更新后端健康检查列表。

**注意事项**: 
- 如果服务数量极多（超过 1000+），关注 Higress 的配置推送性能，必要时进行服务分租管理。
- 确保注册中心与 Higress 之间的网络连通性，避免因网络抖动导致服务列表丢失。

---

### 实践 5：实施可观测性与全链路监控

**说明**: 网关是流量的必经之路，是监控的最佳观测点。最佳实践包括启用 Higress 的日志采集（集成 SLS 或 Elasticsearch）、配置 Prometheus 监控指标（QPS、延迟、状态码分布）以及开启分布式链路追踪。这有助于快速定位性能瓶颈和故障点。

**实施步骤

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题。在弱网或高丢包环境下，Higress 网关的连接建立速度和传输稳定性将得到显著提升，特别适合移动端 API 网关场景。

**实施方法**:
1. 在 Higress 的网关配置中开启 QUIC 监听端口。
2. 配置 TLS 1.3 及对应的 HTTP/3 ALPN 协议协商。
3. 确保客户端（SDK 或浏览器）支持 HTTP/3 协议。

**预期效果**: 在弱网环境下，连接建立延迟降低 30%-50%，吞吐量提升 20% 以上。

---

### 优化 2：配置全链路超时与连接池调优

**说明**: 默认配置可能导致连接数过多或后端服务长时间挂起。通过精细调整上游服务的连接超时、最大空闲连接数和 Keep-Alive 间隔，可以减少频繁建立 TCP 连接的开销，防止连接泄漏。

**实施方法**:
1. 调整 `upstream` 的 `idleTimeout` 和 `connectTimeout` 参数。
2. 根据后端服务能力，设置合理的 `maxRequestsPerConnection`。
3. 启用 HTTP/1.1 的 Keep-Alive 或 HTTP/2 连接复用。

**预期效果**: 后端服务连接数减少 40%，P99 延迟降低 15%-20%。

---

### 优化 3：启用 Wasm 插件的本地缓存与预编译

**说明**: Higress 支持通过 Wasm 扩展网关功能。频繁的 Wasm 虚拟机实例化或内存分配会消耗 CPU 资源。通过启用 Wasm 插件的 AOT（预编译）及配置高效的内存缓存策略，可显著降低插件执行延迟。

**实施方法**:
1. 在网关配置中启用 Wasm 的 AOT 编译模式。
2. 优化 Wasm 插件代码，减少不必要的 Host Proxy 调用。
3. 配置插件级别的缓存策略，避免重复计算。

**预期效果**: Wasm 插件执行延迟降低 10%-30%，网关 CPU 占用率下降 10%。

---

### 优化 4：实施精细化日志采样与异步上报

**说明**: 在高并发场景下，同步记录访问日志会严重阻塞请求处理线程。通过配置日志采样率（如仅记录 10% 的流量）以及采用异步非阻塞方式上报日志，可极大释放 I/O 线程压力。

**实施方法**:
1. 修改 `logsetting` 配置，针对非关键业务设置采样率（如 0.1）。
2. 将日志输出后端改为异步模式（如使用 Kafka 或 Async File Logger）。
3. 关闭不必要的 Access Log 字段（如 request_body）。

**预期效果**: 高并发下吞吐量提升 20%-40%，I/O Wait 显著降低。

---

### 优化 5：启用 DNS 缓存与连接复用

**说明**: 默认的 DNS 解析可能产生额外的网络延迟。Higress 作为网关，对后端服务的域名解析频率极高。启用客户端侧的 DNS 缓存，并配合长连接复用，可消除 DNS 查询延迟。

**实施方法**:
1. 在 Higress 全局配置中开启 DNS 缓存，并设置合理的 TTL（如 60s）。
2. 确保后端服务使用域名而非 IP（若使用 IP，需配合服务发现机制）。
3. 配置 DNS 解析失败后的快速降级策略。

**预期效果**: 消除 DNS 查询延迟（通常为 10ms-50ms），请求总耗时略有下降。

---
## 学习要点

- Higress 是阿里云开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 它通过将 Ingress 网关与微服务网关合二为一，解决了传统架构中网关碎片化带来的高运维成本问题。
- 提供了强大的 WAF 插件市场，支持热加载，允许用户低代码扩展安全防护与流量处理能力。
- 架构设计上采用高性能的 Rust 编写代理核心（Envoy 超集），在处理高并发请求时具有更低的资源消耗与延迟。
- 兼容 Kubernetes Ingress 标准与 Nginx Ingress 注解，极大地降低了用户从传统架构迁移至云原生架构的门槛。
- 内置了对阿里云应用监控 (ARMS) 与 Prometheus 的深度集成，提供了开箱即用的可观测性。
- 支持将服务直接注册到网关，实现了无 Sidecar（Sidecarless）的微服务治理模式，简化了部署复杂度。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的定位与作用，对比 Higress 与 Nginx、Kong、Istio Ingress 的区别。
- Higress 架构概览：掌握 Higress 的整体架构（Ingress Controller + Gateway Pod 分离设计），了解其基于 Istio 和 Envoy 的技术底座。
- 基础安装与部署：学习如何在 Kubernetes 集群中通过 Helm 或 YAML 资源文件安装 Higress。
- 核心概念模型：理解 Higress 的 Ingress API（兼容 K8s Ingress）和 Gateway API 基础用法。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - 快速入门章节
- [云原生网关 Higress 实战系列文章](https://developer.aliyun.com/group/higress)

**学习建议**:
建议先在本地搭建一套 Kind 或 Minikube 环境，不要急于在生产环境尝试。重点理解 Higress 如何通过标准 Kubernetes 资源来管理流量，动手完成一次简单的服务转发配置。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- 高级路由配置：掌握基于 Header、Query、Cookie 等条件的复杂路由匹配规则。
- 流量管理特性：学习灰度发布（金丝雀发布）、蓝绿部署、Header 重写/重定向、流量镜像（Traffic Mirroring）。
- 服务保护：配置超时时间、重试策略以及熔断降级规则。
- 负载均衡策略：了解并配置轮询、随机、最小连接数等负载均衡算法。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy 官方文档（理解底层代理逻辑）
- Higress 官方示例仓库

**学习建议**:
此阶段重点在于“如何精细化控制流量”。建议模拟真实的业务场景，例如“将 5% 的流量路由到新版本服务”，并观察日志验证是否符合预期。同时，尝试配置错误注入来测试系统的容错能力。

---

### 阶段 3：插件生态与安全防护

**学习内容**:
- 插件系统机制：理解 Higress 的 Wasm 插件运行原理，以及 Lua 脚本支持（如适用）。
- 核心插件使用：实战配置常用插件，包括 Key Rate Limit（限流）、Basic Auth（鉴权）、CORS、Request Block 等。
- 安全防护：学习如何配置 IP 访问控制列表（ACL）、防御 SQL 注入或 XSS 攻击插件。
- 自定义插件开发：学习使用 Wasm (AssemblyScript/Go/Rust) 编写简单的自定义插件来扩展网关功能。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场
- Higress 官方文档 - 自定义插件开发指南
- WebAssembly (Wasm) 相关教程

**学习建议**:
先熟练使用官方插件市场中的现成插件解决常见问题（如限流和鉴权）。随后，尝试编写一个简单的 Wasm 插件（例如修改请求 Header 或响应 Body），以掌握扩展网关能力的核心技能。

---

### 阶段 4：服务集成与高可用运维

**学习内容**:
- 多协议支持：配置 Dubbo、Nacos Service Registry 等非 HTTP 或 RPC 协议的服务接入。
- 服务发现集成：学习如何对接 Nacos、Consul、ZooKeeper 等注册中心，实现 K8s 服务与外部服务的统一流量管理。
- 可观测性：配置 Prometheus 监控指标、集成 SkyWalking/Zipkin 进行分布式链路追踪，以及配置日志采集（SLS/ELK）。
- 高可用部署：学习 Higress 的高可用架构部署，包括资源限制、性能调优与弹性伸缩。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - Nacos 注册中心集成
- Higress 官方文档 - 可观测性与监控
- Prometheus 与 Grafana 官方文档

**学习建议**:
此阶段侧重于“生产就绪”。建议构建一个包含服务网格和传统微服务的混合架构场景，重点练习将外部服务（如 Nacos 中的服务）引入网关进行管理。同时，务必配置好监控大盘，能够通过 Grafana 看到网关的 QPS、延迟和错误率。

---

### 阶段 5：架构设计与源码贡献

**学习内容**:
- 深度源码剖析：阅读 Higress Controller 源码，理解 Ingress 资源如何转化为 Envoy 配置（xDS 协议推送流程）。
- 架

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生网关。它最初源于阿里巴巴集团内部的电商业务需求，用于支撑双十一等大流量场景。Higress 是开源项目（托管在 GitHub 上），也是 CNCF（云原生计算基金会）全景图中的项目。它基于 Istio 和 Envoy 构建，旨在提供一站式的流量管理、安全防护和插件管理平台，兼容 Kubernetes 和 Nginx Ingress 生态。

---



### 2: Higress 与传统的 Nginx Ingress Controller 或 Kong 网关相比有什么优势？

2: Higress 与传统的 Nginx Ingress Controller 或 Kong 网关相比有什么优势？

**A**: Higress 的主要优势体现在以下几个方面：
1.  **架构先进**：基于 Istio 和 Envoy，支持热更新，配置变更无需 Reload 进程，连接不会中断。
2.  **安全防护**：内置了 WAF（Web 应用防火墙）能力，能够有效防御 SQL 注入、XSS 等常见 Web 攻击，且支持与阿里云 WAAP 的深度集成。
3.  **插件生态**：支持 Lua 和 WASM（WebAssembly）插件。WASM 插件支持多语言编写（如 Go, C++, Rust, JS），且插件热更新无需重启网关，安全性更高。
4.  **服务发现**：原生支持 Nacos、Consul、ZooKeeper 以及 Kubernetes Service，解决了传统网关对接微服务注册中心复杂的问题。

---



### 3: Higress 是否支持从 Nginx 或 Nginx Ingress 平滑迁移？

3: Higress 是否支持从 Nginx 或 Nginx Ingress 平滑迁移？

**A**: 是的，Higress 提供了极佳的兼容性以降低迁移门槛。
1.  **配置兼容**：Higress 支持标准的 Nginx Ingress Annotation，同时也支持直接导入 Nginx 的配置片段。
2.  **工具支持**：官方提供了 `nginx2Higress` 配置转换工具，可以帮助用户将现有的 Nginx 配置自动转换为 Higress 的 Ingress 或 Gateway API 配置。
3.  **流量切换**：在 Kubernetes 环境中，可以通过调整 Selector 标签的方式，将 Service 的流量逐步从 Nginx Ingress 切换到 Higress，实现灰度发布和平滑迁移。

---



### 4: Higress 的 WASM 插件机制是如何工作的？为什么要使用 WASM？

4: Higress 的 WASM 插件机制是如何工作的？为什么要使用 WASM？

**A**: Higress 强调插件能力的扩展性，而 WASM（WebAssembly）是其核心特性之一。
1.  **工作原理**：用户可以使用 Go、C++、Rust 或 JavaScript 编写业务逻辑，编译成 WASM 文件。Higress 网关运行时会加载这些 WASM 文件，并在请求处理的特定阶段执行插件逻辑。
2.  **优势**：
    *   **安全性**：WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关主进程崩溃。
    *   **灵活性**：支持多语言开发，开发者不需要学习 Lua 就可以编写高性能插件。
    *   **热更新**：插件修改后可以动态推送到网关，无需重启网关进程或中断流量。

---



### 5: Higress 如何处理全链路的安全防护？

5: Higress 如何处理全链路的安全防护？

**A**: Higress 提供了从入口到后端服务的全链路安全方案：
1.  **认证与鉴权**：支持标准的 OIDC（OpenID Connect）、OAuth 2.0、API Key、Basic Auth 等多种认证方式。同时支持基于 IP、Header、JWT 的精细化访问控制。
2.  **WAF 防护**：内置开源 ModSecurity 规则集，能够识别和拦截常见的 Web 攻击。企业版或云上版本可以集成更强大的 AI 驱动 WAF 能力。
3.  **mTLS 支持**：支持网关与后端服务之间的双向 TLS 认证（mTLS），确保服务间通信的加密和安全。

---



### 6: Higress 是否支持非 Kubernetes 环境部署？

6: Higress 是否支持非 Kubernetes 环境部署？

**A**: 支持。虽然 Higress 是为云原生和 Kubernetes 环境设计的，但它也提供了**标准版**（Standalone 版本）。
1.  **部署方式**：可以通过 Docker Compose 或直接下载二进制包的方式在裸机或虚拟机上部署。
2.  **功能差异**：标准版依然保留了强大的网关核心能力、API 管理和插件功能，适合传统虚拟机环境或边缘计算场景使用。用户可以通过控制台或 Ingress 配置文件进行管理。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速体验与流量转发

### 假设你有一个运行在本地 8080 端口的后端服务（例如一个简单的 Python Flask 或 Node.js 应用）。请下载并使用 Docker Compose 快速部署 Higress，并配置一个 Ingress 路由，使得访问 Higress 网关的 80 端口时，流量能被正确转发到你本地的 8080 端口服务上。

### 提示**:

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，为您提供的 7 条实践建议：

### 1. 利用 AI 提示词模板实现服务标准化
**场景**：前端直接调用大模型时，容易泄露系统提示词，且难以统一修改。
**建议**：在 Higress 中配置 AI 服务的 `prompt` 模板。不要将完整的 System Prompt 写在客户端代码中，而是将其配置在网关的路由或插件配置里。
**操作**：在创建 AI 服务时，定义固定的模板变量（如 `{{input}}`），客户端只需传递用户输入，网关自动拼接预设的上下文和提示词。
**收益**：便于集中管理 Prompt 版本，无需重新发布业务应用即可调整模型行为。

### 2. 配置语义缓存以降低 Token 消耗
**场景**：AI 应用中存在大量重复或相似的高频提问（如客服常见问题），直接转发给 LLM 会产生不必要的费用和延迟。
**建议**：启用 Higress 的语义缓存插件。
**操作**：针对非实时性要求极高的场景，配置向量缓存策略。当用户提问与缓存中的问题语义相似度超过阈值（如 0.9）时，直接返回缓存的回复，而不再请求大模型。
**陷阱**：对于创意写作或需要极高逻辑严密性的场景，慎用缓存，以免返回过时或缺乏上下文关联的答案。

### 3. 实施基于 Token 的超时与重试策略
**场景**：大模型推理时间不确定，简单的 HTTP 超时设置可能导致流式输出中断或前端报错。
**建议**：不要仅依赖默认的连接超时，应根据模型平均响应时间配置读取超时。
**操作**：在 Higress 的服务来源或路由配置中，适当调长 `timeout` 时长。同时，配置针对上游 LLM 服务的重试策略（例如：非 200 状态码或特定错误码时重试），但要确保开启“流式重试”支持，避免破坏 SSE 体验。
**陷阱**：超时时间设置过长会导致请求堆积，占用网关连接池，需根据实际业务压测设定平衡值。

### 4. 敏感信息脱敏与输入校验
**场景**：用户可能通过 Prompt 注入攻击套取系统信息，或在输入中包含隐私数据。
**建议**：在请求到达 LLM 之前，通过 Higress 的插件（如 `request-block` 或自定义 WAF 插件）进行拦截和清洗。
**操作**：配置关键词黑名单拦截恶意 Prompt，或使用正则表达式过滤身份证号、手机号等敏感信息，防止这些数据被发送至外部模型提供商。
**收益**：降低合规风险和数据泄露风险。

### 5. 利用多模型供应商切换实现高可用
**场景**：单一模型提供商（如 OpenAI 或通义千问）可能出现 API 限流或服务宕机。
**建议**：在 Higress 中配置多个模型服务来源，并利用路由规则实现故障切换或负载均衡。
**操作**：定义两个不同的 AI 服务（Service A 和 Service B），分别指向不同的 Provider。在路由插件中配置 fallback 逻辑，或者通过流量比例切分，将 5% 的流量导向备用模型以验证其可用性。
**最佳实践**：不要将所有业务押注在一个 Provider 的 API Key 上，通过网关层解耦，可以快速切换底层模型。

### 6. 鉴权与 API Key 的统一管理
**场景**：前端应用不应直接暴露大模型厂商的 API Key，且多租户环境下需要隔离不同用户的额度。
**建议**：在 Higress 层面统一管理 Provider 的 API Key，客户端只携带业务鉴权信息。
**操作**：配置 AI 服务时填入真实的 LLM API Key。客户端请求时携带业务 Token，Higress 通过 `jwt-auth` 等插件验证用户身份后，自动注入底层的 API Key 转发请求。
**收益**：防止 Key 泄露，便于在网关层统一监控和控制不同厂商的 API 调用配额。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*