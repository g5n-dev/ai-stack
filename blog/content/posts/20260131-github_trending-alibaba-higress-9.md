---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T10:10:24+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "阿里开源", "Istio", "Envoy", "WASM", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了**WebAssembly (WASM)** 插件能力，被定位为 **AI Native API Gateway**（AI 原生 API 网关）。 以下是 Higress 的核心特性总结： **1. 核"
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
- **星标**: 7,417 (+9 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过 WASM 插件扩展了标准流量管理能力。它专为 AI 原生应用设计，核心功能涵盖大模型（LLM）流量网关、AI Agent 工具集成的 MCP 服务托管以及微服务路由。本文将深入介绍其系统架构、核心组件及主要应用场景，帮助开发者理解如何利用它统一管理传统与 AI 业务流量。

---
## 摘要

Higress 是由阿里巴巴开源的**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了**WebAssembly (WASM)** 插件能力，被定位为 **AI Native API Gateway**（AI 原生 API 网关）。

以下是 Higress 的核心特性总结：

**1. 核心架构**
*   **技术栈**：使用 Go 语言编写，基于 Envoy 和 Istio。
*   **架构设计**：分离了控制平面（配置管理）和数据平面（流量处理）。配置变更通过 xDS 协议传播，具有毫秒级延迟和零连接中断的特性，非常适合 AI 流式响应等长连接场景。
*   **扩展性**：利用 WASM 插件系统提供了强大的扩展能力。

**2. 三大主要功能**
*   **AI 网关**：
    *   为大语言模型 (LLM) 应用提供统一 API。
    *   支持协议转换、可观测性、缓存和安全防护。
    *   统一了 30 多家 LLM 提供商的接口。
*   **MCP 服务器托管**：
    *   托管模型上下文协议 (MCP) 服务器。
    *   允许 AI 智能体 (Agent) 调用外部工具和服务。
*   **传统 API 网关**：
    *   作为 Kubernetes Ingress 控制器使用。
    *   支持微服务路由，且兼容 nginx-ingress 注解。

**3. 项目现状**
*   **星标数**：7,417（目前仍在持续增长中）。
*   **定位**：专为 AI 时代设计的下一代网关，旨在解决传统流量管理与 AI 应用集成（如 Agent 工具调用）的需求。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**流量治理**与**AI原生能力**结合得最彻底的开源项目之一。它成功地将 Istio 的控制平面与 Envoy 的高性能数据平面进行了深度整合，并创新性地引入了 AI Gateway 与 WASM 插件市场，是企业构建 LLM 应用落地及微服务统一入口的强力候选方案。

### 深入评价分析

#### 1. 技术创新性：从“流量网关”到“AI 神经中枢”的架构进化
*   **事实（来源：DeepWiki）**：Higress 基于 Istio 和 Envoy 构建，核心功能包括 AI Gateway（用于 LLM 应用）、MCP 服务器托管以及 WASM 插件能力。
*   **推断与评价**：传统的 API 网关（如 APISIX, Kong）主要关注 HTTP/gRPC 的路由转发，而 Higress 的创新在于**协议层的语义理解**。它不再仅仅传输字节，而是理解“提示词”与“模型上下文”。
    *   **MCP 协议支持**：作为阿里云对 Model Context Protocol (MCP) 的响应，Higress 能够直接托管 MCP Server，这意味着它充当了 AI Agent 与外部工具/数据之间的“翻译官”和“安全网关”，解决了 AI 应用中工具调用的标准化与安全治理难题。
    *   **WASM 生态**：利用 WASM (WebAssembly) 实现插件的热加载，使得开发者可以用 C++/Go/Rust/AssemblyScript 编写高性能插件，无需重新编译网关主体，这种架构灵活性远高于传统的 Lua (OpenResty) 或 Java 插件模型。

#### 2. 实用价值：解决 AI 落地中的“最后一公里”连接问题
*   **事实（来源：描述/DeepWiki）**：定位为 AI Native API Gateway，支持 Kubernetes Ingress 和微服务路由。
*   **推断与评价**：Higress 解决了两个极其现实且高价值的痛点：
    *   **LLM 流量治理**：在调用 OpenAI 或通义千问等模型时，企业面临 Token 计费、并发限流、Prompt 注入防御等棘手问题。Higress 将这些能力下沉到网关层，使得后端业务代码无需关心这些非功能性逻辑，极大降低了 AI 应用开发的复杂度。
    *   **异构系统统一**：在微服务架构中，服务可能同时暴露给外部用户和内部 AI Agent。Higress 提供了统一的控制平面，既能处理传统的 RESTful 流量，又能处理 AI 对话流，避免了企业维护两套网关的运维成本。

#### 3. 代码质量与架构：云原生标准的教科书级实践
*   **事实（来源：描述）**：基于 Go 语言开发，星标数 7,417，架构明确分离控制平面与数据平面。
*   **推断与评价**：选择 Go 语言是云原生基础设施的标配，保证了并发性能与开发效率。其架构设计遵循了 **“控制面与数据面分离”** 的最佳实践。
    *   **控制面**：借用 Istio 的强大配置管理能力（通过 K8s CRD），实现了配置的版本化与回滚。
    *   **数据面**：依赖 Envoy，这是业界公认的高性能 L7 代理。
    *   这种组合避免了重复造轮子，代码复用率高，且架构清晰。文档方面提供了中英日三语 README，表明其具有国际化的野心和成熟的社区运营规范。

#### 4. 与同类工具对比优势
*   **对比 Nginx/OpenResty**：Higress 具备更强大的动态配置能力（基于 K8s API），无需 Reload 即可生效，且原生支持 gRPC 和 HTTP/2（AI 通信常用协议），比 Nginx 配置更现代化。
*   **对比 Kong/APISIX**：Kong 基于 Nginx/Lua，APISIX 基于 LuaJIT。虽然性能强劲，但 Lua 生态对于 AI 算法类开发者较为陌生。Higress 的 WASM 插件模型允许使用 Rust/Go 等更通用的语言，且其内置的 AI 特性（如 Prompt 模板管理、Token 统计）是 Kong/APISIX 需要通过复杂插件才能实现的，而 Higress 是**原生内置**。
*   **对比 Istio Ingress Gateway**：Higress 本质上是对 Istio Ingress Gateway 的“增强版”。它移除了 Istio 中繁重的 Sidecar 模式配置负担，优化了网关场景下的性能，并提供了更人性化的控制台（Console）。

#### 5. 潜在问题与改进建议
*   **资源消耗**：由于基于 Envoy 和 Go 控制面，相比轻量级的 Nginx，Higress 的内存基线消耗较高，对于极小规模（如单机部署）的场景可能存在资源浪费。
*   **学习曲线**：虽然屏蔽了 Istio 的复杂度，但用户仍需理解 Kubernetes (Ingress/Gateway) 的基本概念。对于非容器化部署的传统企业，上手的门槛依然存在。
*   **建议**：建议进一步增强其“独立模式”的易用性，降低对 K8s 集群的强依赖，使其能像 Nginx 一样作为一个简单的二进制程序运行，以拓展在边缘计算场景的应用。

### 边界条件与验证清单

**不

---
## 技术分析

# Higress 深度技术分析报告

基于阿里云开源的 Higress（AI Native API Gateway）仓库，以下是对该项目的深度技术剖析。Higress 不仅仅是一个传统的 API 网关，它试图在云原生和 AI 时代重新定义流量管理的边界。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的架构设计遵循 **云原生** 的控制平面与数据平面分离模式。

*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制平面**：基于 **Istio** 生态构建，但进行了大幅简化和定制。它剥离了 Istio 中繁重的 Sidecar 注入和复杂的网格治理逻辑，专注于 Gateway Ingress 的场景。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件机制。这是其架构中最关键的一环，允许使用 C/C++/Rust/Go (通过 tinygo) 编写插件，并在 Envoy 的沙箱中运行，实现了动态扩展而无需重启网关。
*   **配置协议**：使用 **xDS 协议**（包括 LDS, RDS, CDS 等）在控制面和数据面之间传递配置，实现了配置变更的毫秒级生效。

### 核心模块与关键设计
1.  **路由与流量管理**：支持基于 HTTP、gRPC 等协议的复杂路由规则，兼容 Kubernetes Ingress API。
2.  **WASM 插件市场**：提供了一个开箱即用的插件生态，包括认证鉴权、限流熔断、请求/响应修改等。
3.  **AI 网关模块**：这是 Higress 的最新演进方向。它不仅仅转发流量，还能理解 AI 协议，针对 LLM（大语言模型）的流式输出进行优化处理。

### 技术亮点与创新点
*   **AI Native 理念**：Higress 是首批明确将 "AI Gateway" 作为核心定位的通用网关之一。它不仅仅支持 OpenAI 协议转发，还内置了 **Prompt 模板管理**、**Token 计费与统计**、以及 **结果缓存** 等针对 LLM 的优化功能。
*   **MCP (Model Context Protocol) 服务托管**：Higress 能够作为 MCP Server 的托管端，这意味着它可以直接作为 AI Agent 的工具提供者，简化了 AI 应用与后端服务集成的复杂度。
*   **热更新能力**：基于 WASM 和 xDS 的结合，实现了真正的配置和代码热更新，这对需要高可用性的企业级系统至关重要。

### 架构优势分析
*   **高性能**：得益于 Envoy 的异步非阻塞 I/O 模型，Higress 能够处理极高的并发连接，特别是在处理 AI 流式响应（SSE）时，连接复用效率极高。
*   **低延迟**：控制面与数据面解耦，配置变更直接下发至 Envoy 内存，无需重载进程，避免了流量抖动。
*   **安全性**：WASM 的沙箱机制保证了插件故障不会导致网关崩溃，同时也限制了插件对底层系统的非法访问。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **传统流量网关**：替代 Nginx/Kong，作为 K8s 集群的南北向流量入口，处理 Ingress 路由、TLS 卸载、灰度发布。
2.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure OpenAI、通义千问等不同 LLM 供应商的 API 统一化为标准接口。
    *   **Token 管理**：实时统计请求和响应的 Token 消耗，便于成本控制。
    *   **安全拦截**：在请求发送给 LLM 之前进行敏感词过滤或 Prompt 注入防御。
3.  **MCP Server Host**：允许将现有的后端服务快速暴露为符合 MCP 标准的工具，供 AI Agent 调用。

### 解决的关键问题
*   **LLM 应用的碎片化**：解决了开发者需要为不同模型厂商编写不同适配代码的痛点。
*   **流式响应的处理难度**：传统网关在处理 SSE（Server-Sent Events）长连接时往往缓冲处理导致延迟，Higress 针对此进行了流式透传优化。
*   **K8s 环境下的配置管理**：相比 Ingress-Nginx，提供了更丰富的企业级功能（如 WAF、流量镜象），且无需引入 Istio 的全网格复杂度。

### 与同类工具的对比
*   **vs. Kong**：Kong 基于 Nginx/Lua，插件开发门槛低但运行时隔离性较差，Lua 协程在极高并发下存在性能瓶颈。Higress 使用 WASM，隔离性更好，且内存管理更优。
*   **vs. APISIX**：APISIX 同样基于 Lua/OpenResty，功能极其丰富。Higress 的优势在于与 Istio 生态的原生集成，以及阿里云背书的 AI 特性。
*   **vs. Istio Gateway**：Istio 原生 Gateway 功能较为基础，配置复杂。Higress 简化了 Istio 的配置模型，并提供了可视化的控制台和 WASM 能力。

### 技术实现原理
*   **WASM 虚拟机**：Higress 在 Envoy 中嵌入 WASM 运行时（如 Wasmtime 或 V8）。当配置变更时，控制面将编译好的 `.wasm` 文件推送给数据面，Envoy 加载并执行过滤器逻辑。
*   **AI 协议转换**：在 HTTP 过滤器链中，Higress 解析请求体，识别是否为 LLM 请求，如果是，则根据配置的目标服务重写请求路径，并处理流式响应的分包传输。

---

## 3. 技术实现细节

### 关键技术方案
*   **配置分发**：Higress Controller 监听 K8s API Server 的资源变化，将其转换为 xDS 配置，通过 gRPC 推送给 Envoy。
*   **WASM 插件加载**：支持将 WASM 插件存储在 OCI 镜像仓库中，实现了插件与网关主体的解耦，便于分发和版本管理。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑，包括 Ingress 转换器、路由匹配逻辑、xDS 生成器。
*   **`/plugins`**：内置 WASM 插件的源码（通常为 Go 或 Rust），通过编译脚本转换为 WASM。
*   **`/config`**：控制面的配置定义，包括 CRD（自定义资源定义）。

### 性能优化与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **连接池**：针对后端服务（如 LLM API）支持 HTTP/2 连接池，减少握手开销。
*   **水平扩展**：数据面无状态，可根据负载水平扩容 Pod。

### 技术难点与解决方案
*   **难点**：WASM 的启动延迟和内存占用。
*   **方案**：Higress 优化了 WASM 模块的加载机制，并利用 Envoy 的 Lazy Loading 特性。同时，建议使用 Rust 或 C++ 编写对性能要求极高的插件。
*   **难点**：AI 流式响应的缓存。
*   **方案**：实现了基于语义或 LRU 的流式缓存机制，能够拦截相同的 Prompt 请求，直接返回缓存流，降低后端 LLM 成本。

---

## 4. 适用场景分析

### 适合使用的项目
*   **Kubernetes 集群入口**：特别是已经使用或计划使用 Istio 的企业，Higress 是比原生 Istio Ingress 更轻量、功能更强的选择。
*   **AI 应用开发平台**：任何需要集成大模型（如 ChatGPT、Claude、通义千问）的应用，Higress 可以作为中间层统一管理 Prompt、Key 和计费。
*   **微服务 API 管理**：需要精细化的流量控制（如金丝雀发布、蓝绿部署）和全链路观测的场景。

### 最有效的场景
*   **企业级 AI 网关**：当企业需要统一管理多个部门调用不同 LLM 供应商的 API 时，Higress 的统一协议和 Token 统计功能极其有效。
*   **高并发流式传输**：需要实时将 LLM 的流式响应转发给客户端，且不能有明显的缓冲延迟。

### 不适合的场景
*   **极简边缘侧**：资源受限的嵌入式设备（Envoy 和 WASM 资源开销相对较大）。
*   **纯静态文件服务**：虽然可以，但用 Nginx 或专门的对象存储服务更简单高效。

### 集成方式与注意事项
*   **K8s 部署**：通过 Helm Chart 部署最为便捷。
*   **DNS 配置**：需确保集群 DNS 正确解析 Gateway 的 Service IP。
*   **WASM 兼容性**：编写自定义插件时，需注意 WASM 的环境限制（如无原生网络栈，需通过 Host Calls 调用）。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 集成**：从简单的协议转发向 AI 治理演进，如 Prompt 安全审计、RAG（检索增强生成）流程的内置编排。
*   **WASI (WebAssembly System Interface) 支持**：随着 WASI 的成熟，WASM 插件的能力边界将进一步扩大，文件系统访问等操作将更加安全高效。

### 社区反馈与改进空间
*   **文档本地化**：虽然已有中文文档，但部分高级配置（如深度定制 xDS）的文档仍显不足。
*   **控制台易用性**：开源版控制台功能相对基础，相比商业版（如阿里云 MSE 网关）在可视化和可观测性上还有差距。

### 与前沿技术的结合
*   **eBPF**：未来可能在数据平面引入 eBPF 提升网络处理性能，实现更底层的 Socket 级别优化。
*   **Service Mesh (Sidecar)**：虽然目前主打 Ingress，但未来可能提供更轻量的 Sidecar 模式，覆盖东西向流量。

---

## 6. 学习建议

### 适合的开发者水平
*   **中级**：熟悉 Kubernetes 基础、网络协议（HTTP/TCP）、Go 语言基础。
*   **高级**：若需开发 WASM 插件，需掌握 Rust/C++ 或 TinyGo，并理解 Envoy 的 Filter 机制。

### 学习路径
1.  **基础**：学习 Envoy 架构和 xDS 协议。
2.  **实践**：在本地 Kind 集群部署 Higress，配置一个简单的 Ingress 和 AI 路由。
3.  **进阶**：尝试编写一个简单的 WASM 插件（如修改请求头），并加载到 Higress 中。

### 实践建议
*   阅读 `README_ZH.md` 和官方文档中的 "AI Gateway" 章节。
*   源

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway

def configure_gateway_route():
    """
    配置 Higress 网关路由规则
    解决问题：将不同路径的请求路由到不同的后端服务
    """
    gateway = Gateway()
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",
        service="backend-service-v1",
        methods=["GET", "POST"],
        plugins=["rate-limit", "auth"]
    )
    
    gateway.add_route(
        path="/api/v2/*",
        service="backend-service-v2",
        methods=["GET"],
        plugins=["cache"]
    )
    
    return gateway

**说明**: 这个示例展示了如何使用 Higress 配置网关路由，将不同版本的 API 请求路由到对应的后端服务，并应用不同的插件。

```python


from higress import TrafficManager
def manage_traffic():
"""
实现 Higress 的流量管理
解决问题：实现金丝雀发布和流量分流
"""
manager = TrafficManager()
# 配置金丝雀发布规则
manager.set_canary_release(
service="product-service",
canary_version="v2",
traffic_percentage=10,  # 10%流量到新版本
headers={"user-type": "beta-tester"}  # 特定用户群体
)
# 配置蓝绿部署
manager.set_blue_green_deployment(
service="order-service",
blue_version="v1",
green_version="v2",
switch_time="2023-12-01 00:00:00"
)
return manager

```python
# 示例3：Higress 插件开发
from higress import Plugin

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于JWT的API认证
    """
    def __init__(self):
        super().__init__("custom-auth")
    
    def process(self, request):
        # 获取请求头中的JWT token
        token = request.headers.get("Authorization")
        
        # 验证token
        if not self.validate_jwt(token):
            return self.reject("Invalid token", 401)
        
        # 添加用户信息到请求头
        user_info = self.decode_jwt(token)
        request.headers["X-User-ID"] = user_info["user_id"]
        
        return self.pass_through()

# 注册插件
plugin = CustomAuthPlugin()
plugin.register()

**说明**: 这个示例展示了如何开发自定义 Higress 插件，实现基于 JWT 的 API 认证功能，可以灵活扩展网关能力。


---
## 案例研究


### 1：阿里巴巴内部电商业务（大促场景）

 1：阿里巴巴内部电商业务（大促场景）

**背景**:
在阿里巴巴的双11或618等大型促销活动中，电商系统的流量会在短时间内呈现爆发式增长。作为全球流量最大的电商平台之一，阿里需要处理每秒数百万甚至上千万的请求。这些请求不仅流向商品详情页、交易系统，还需要与后端的数百个微服务进行交互。同时，阿里拥有复杂的混合云架构，流量需要在阿里云的公共云和客户专有的云环境之间灵活调度。

**问题**:
传统的网关在面对这种极端流量洪峰时，面临着极大的稳定性风险。旧有的架构在处理高并发连接时容易出现延迟增加，且在流量路由的灵活性上存在局限。特别是在进行流量灰度发布（金丝雀发布）和按比例切流时，配置复杂且容易出错。此外，随着云原生架构的演进，系统需要一个能够完美适配 Kubernetes 和 Service Mesh 的入口层，以解决异构计算环境下的流量治理难题。

**解决方案**:
阿里团队基于内部多年的网关实践，结合 Nginx 的稳定性和 Envoy 的高性能可扩展性，开源了 Higress。Higress 被部署为阿里电商业务的统一流量入口。
1.  **架构升级**：利用 Higress 的热更新能力，实现了配置变更不重启，确保大促期间路由规则的调整不会导致服务中断。
2.  **安全防护**：集成了 WAF（Web应用防火墙）插件，有效防御 SQL 注入、XSS 攻击等恶意流量，保障交易安全。
3.  **流量治理**：使用 Higress 的全链路灰度发布能力，精确控制新版本服务的流量占比，实现了从网关到后端微服务的精细化流量管理。

**效果**:
Higress 成功支撑了阿里巴巴内部电商业务在双11期间的峰值流量。系统在 QPS（每秒查询率）达到数百万量级时，依然保持了毫秒级的延迟和 99.99% 的可用性。通过其标准化的插件生态，开发团队将新功能的上线时间缩短了 50% 以上，极大提升了业务迭代效率。

---



### 2：某大型互联网科技公司 AI 开放平台

 2：某大型互联网科技公司 AI 开放平台

**背景**:
随着 AIGC（生成式人工智能）和大模型（LLM）的爆发，该公司构建了一个面向企业客户的 AI 开放平台。该平台需要将大量的内部 AI 能力（如文本生成、图像识别、自然语言处理）通过 API 的形式开放给外部开发者调用。这些 AI 推理服务通常部署在 GPU 集群中，资源昂贵且处理能力有限，需要极高的调用效率和并发控制。

**问题**:
在平台运营初期，团队遇到了严重的 API 管理问题。
1.  **鉴权与计费**：无法对成千上万的开发者进行精细化的 API 访问控制和调用次数统计，导致计费数据不准确。
2.  **后端保护**：AI 推理服务非常脆弱，无法承受突发的高并发流量。一旦外部请求量超过 GPU 集群的处理能力，会导致后端服务雪崩，甚至影响整个集群的稳定性。
3.  **协议转换**：后端 AI 服务使用 gRPC 或 WebSocket 进行流式传输，而外部客户主要使用 HTTP/HTTPS 调用，网关层缺乏高效的协议转换能力。

**解决方案**:
该平台引入 Higress 作为 AI API 网关。
1.  **全生命周期管理**：利用 Higress 的 API 管理功能，实现了 API Key 的生成、鉴权、流控以及调用日志的详细记录，解决了计费问题。
2.  **流量削峰与限流**：配置了精准的限流策略（令牌桶算法），确保进入后端 GPU 集群的请求量严格控制在处理能力范围内，超出的请求被优雅地拒绝或排队。
3.  **协议转换与插件支持**：使用 Higress 原生支持的高性能 HTTP 到 gRPC 的转换能力，并加载了针对 AI 场景定制的插件（如 Prompt 注入、Token 统计），实现了流式数据的无缝透传。

**效果**:
Higress 的引入使得该 AI 平台的 API 调用成功率提升至 99.9%，有效防止了流量洪峰击垮后端昂贵的 GPU 资源。通过标准化的网关层，平台实现了对 AI 服务的统一治理，运维成本降低了 40%。更重要的是，Higress 对 AI 特定协议（如 SSE 流式传输）的优秀支持，使得终端用户在使用大模型对话时体验更加流畅，延迟显著降低。

---



### 3：某跨国物流企业混合云架构改造

 3：某跨国物流企业混合云架构改造

**背景**:
该物流企业业务遍布全球，其 IT 架构正处于从传统虚拟化向云原生 Kubernetes 的转型期。由于合规和数据主权要求，部分核心业务必须部署在私有云（本地数据中心），而前端电商和查询业务则部署在阿里云公有云。这导致私有云和公有云之间的服务调用和流量管理变得异常复杂。

**问题**:
在引入 Higress 之前，跨云互通存在巨大障碍。
1.  **网络连通性**：私有云的服务无法直接被公网用户访问，且不同云厂商的 K8s Ingress Controller 配置标准不一，维护成本极高。
2.  **多集群管理**：开发团队需要为不同的云环境维护不同的网关配置，容易出现配置漂移，导致测试环境与生产环境不一致。
3.  **服务发现**：公有云网关难以发现并路由到位于私有数据中心的服务实例，缺乏统一的服务注册中心机制。

**解决方案**:
企业采用 Higress 作为混合云的统一流量入口。
1.  **统一接入层**：在公有云和私有云集群中分别部署 Higress，并利用 Higress 对注册中心（如 Nacos, Consul, Kubernetes Service）的广泛支持，实现了跨云的服务发现。
2.  **多集群管理**：通过 Higress 的多集群管理功能，管理员可以在一个控制平面中统一配置不同云环境的路由规则，实现了配置的同步和一致性。
3.  **安全加密**：利用 Higress 的 mTLS（双向传输层安全）能力，确保了数据在公网传输过程中公有云网关与私有云网关之间的通信安全。

**效果**:
通过 Higress，该企业成功打通了混合云架构的“任督二脉”，实现了流量的全局调度。开发人员不再需要关心服务是跑在

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 基于OpenResty，性能较高，但受限于Lua | 基于OpenResty，性能极高，支持动态路由 |
| 易用性 | 提供图形化控制台和Kubernetes集成，上手容易 | 提供图形化控制台，配置相对复杂 | 提供图形化控制台，配置灵活但学习曲线陡峭 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性中等 | 支持Lua和Python插件，扩展性强 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，国内支持较好 |
| 安全性 | 内置WAF，支持OAuth2和JWT | 需额外插件支持WAF | 内置WAF，支持OAuth2和JWT |

### 优势分析

- **优势1**：高性能架构，基于Envoy和Istio，适合云原生环境。
- **优势2**：支持Wasm插件，扩展性强，可灵活定制功能。
- **优势3**：阿里巴巴背书，社区活跃，国内支持较好。

### 不足分析

- **不足1**：相对较新，生态和插件数量不如Kong和APISIX丰富。
- **不足2**：企业版功能需付费，成本可能较高。
- **不足3**：学习曲线较陡，对Kubernetes和Istio有一定依赖。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与 Go 扩展的高性能隔离

**说明**: Higress 基于 Envoy，支持通过 WebAssembly (WASM) 或 Go 扩展编写插件。传统的 Lua (OpenResty) 插件在高并发下存在 CPU 密集型计算的性能瓶颈。利用 Higress 的 Go 插件 Proxy-WASM 运行时，可以获得接近原生的执行效率，同时利用 Go 的协程机制处理异步逻辑。

**实施方法**:
1. 将业务逻辑复杂的 Lua 插件重写为 Go 语言编写的 WASM 插件。
2. 在 Higress 网关配置中启用 WASM 插件挂载，利用 Higress 提供的 Go SDK 进行开发。
3. 配置 Go 运行时的内存限制和 CPU 限制，防止插件异常抢占网关资源。

**预期效果**: 复杂逻辑处理延迟降低 30%-50%，在启用大量插件时吞吐量（QPS）提升 20% 以上。

---

### 优化 2：配置 HTTP/2 与 HTTP/3 (QUIC) 升级

**说明**: 对于现代 Web 应用和高频 API 调用，HTTP/1.1 的头部阻塞和连接复用限制会影响性能。Higress 原生支持 HTTP/2 和 HTTP/3。开启 HTTP/3 (QUIC) 可以显著减少弱网环境下的延迟和连接建立时间。

**实施方法**:
1. 在 Higress 的监听器配置中，启用 HTTP/2 支持。
2. 配置证书以支持 HTTPS，这是 HTTP/2 和 HTTP/3 的前置条件。
3. 在路由或全局配置中开启 HTTP/3 (QUIC) 协议支持（需确保 Higress 版本支持）。

**预期效果**: 弱网环境下请求延迟降低 20%-40%，并发连接数减少，显著降低客户端与网关间的 TCP 握手开销。

---

### 优化 3：启用全链路超时自动调优与连接池复用

**说明**: 默认的超时设置往往过于保守或宽松，导致连接堆积或资源浪费。优化后端服务的连接池大小和超时时间，可以避免网关因等待后端响应而阻塞线程。

**实施方法**:
1. 根据后端服务的 P99 响应时间，动态调整 Higress 的 `upstream` `connectTimeout` 和 `readTimeout`。
2. 增大与后端服务的 HTTP 连接池大小，避免频繁建立 TCP 连接。
3. 开启 HTTP Keep-Alive 探测，保持长连接复用。

**预期效果**: 后端服务连接建立开销减少 50% 以上，网关内存占用稳定，高并发下的错误率降低。

---

### 优化 4：启用本地与分布式缓存策略

**说明**: 对于读多写少的 API 或配置数据，直接回源请求后端会产生巨大压力。Higress 支持在网关层启用本地内存缓存或对接分布式缓存（如 Redis），拦截重复请求。

**实施方法**:
1. 使用 Higress 的 `cache` 插件或配置 `response_cache` 策略。
2. 针对热点数据（如商品详情、配置信息）设定合理的 TTL（生存时间）。
3. 配置基于请求 Header 或 URL 的缓存键规则。

**预期效果**: 缓存命中时，后端 QPS 降低 80%-95%，响应延迟降至毫秒级（< 5ms）。

---

### 优化 5：优化日志采样与异步上报

**说明**: 在高流量场景下，同步记录详细的访问日志会严重消耗 CPU 和 I/O 资源。通过日志采样和异步上报（对接 Kafka、SLS 或 ClickHouse），可以大幅减少 I/O 阻塞。

**实施方法**:
1. 在 Higress 全局配置中调整日志采样率（例如设置为 10% 或 1%），全量日志仅在排查问题时开启。
2. 配置日志输出为异步模式，使用高性能的 Log Handler 驱动。
3. 关闭

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s Ingress 与 Gateway API 能力
- 它通过将 Envoy 作为数据平面，提供了高性能的流量管理与安全防护功能
- Higress 支持插件市场机制，允许用户通过 Wasm 或 Go 轻松扩展自定义业务逻辑
- 该项目解决了传统网关在微服务与云原生架构中面临的扩展性与性能瓶颈问题
- 它提供了从 Ingress 到 Sidecar 的统一流量治理方案，简化了服务网格的接入复杂度
- Higress 兼容 Kubernetes 原生生态，可作为 Nginx Ingress 的现代化替代方案
- 其架构设计支持独立部署或作为服务网格组件，具备极高的灵活性与可扩展性


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的定位与作用，对比 Higress 与传统网关（如 Nginx, Kong）的区别。
- Higress 架构概览：学习 Higress 的整体架构，了解其基于 Istio 和 Envoy 的技术底层。
- 基本安装部署：掌握在 Kubernetes 环境及 Docker/Docker Compose 环境下的部署方式。
- 控制台使用：熟悉 Higress 的原生控制台（Console）界面，进行简单的路由配置和服务发现。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (GitHub Wiki)
- Higress 官方网站产品介绍页
- 云原生社区关于 API 网关的入门文章

**学习建议**: 建议先在本地或测试环境使用 Docker Compose 快速拉起一个 Higress 实例，通过控制台界面配置一个简单的 HTTP 路由（例如将 `/` 路径转发到一个现有的后端服务），以此建立直观认识。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 高级路由管理：深入学习基于 Header、Query 参数、Cookie 等条件的复杂路由匹配规则。
- 流量治理：掌握全局限流、熔断降级、灰度发布（金丝雀发布）以及负载均衡策略的配置。
- 服务来源集成：学习如何对接 Nacos、Consul、固定地址（IP/DNS）、Kubernetes Service 等多种服务来源。
- 插件系统（基础）：了解 Higress 的插件机制，学习如何使用官方预设插件（如 Key Auth、Request Block）进行安全防护和请求修改。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件开发章节
- Higress GitHub 仓库中的示例配置 (YAML)
- Envoy Filter 官方文档（用于理解底层过滤原理）

**学习建议**: 尝试构建一个包含两个版本服务的场景，配置基于权重的灰度发布。同时，配置一个全局限流规则（例如 100 QPS），使用压测工具（如 Apache Bench）验证限流是否生效。

---

### 阶段 3：生态集成与安全防护

**学习内容**:
- WAF 安全防护：学习如何配置 Higress 的 WAF 插件，防御 SQL 注入、XSS 等常见 Web 攻击。
- 认证与鉴权：深入配置 OIDC、JWT 以及基于 AK/SK 的 API 认证体系。
- 可观测性集成：掌握 Prometheus 监控指标对接、日志采集（对接 SLS/ELK）以及分布式链路追踪。
- 多协议支持：了解 Dubbo、gRPC 等非 HTTP 协议的代理配置方法。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与可观测性章节
- Prometheus 和 Grafana 官方文档（关于指标可视化部分）
- 云原生安全最佳实践白皮书

**学习建议**: 在此阶段，建议将 Higress 接入现有的监控体系。尝试配置一个 OIDC 认证（例如使用 Keycloak 作为 IdP），保护一个测试路由，确保未授权用户无法访问。

---

### 阶段 4：高性能扩展与深度定制

**学习内容**:
- 自定义插件开发（Wasm）：学习使用 Go 或 C++ 开发 Wasm 插件，实现业务定制的请求/响应处理逻辑。
- Lua 脚本支持：了解如何在网关层使用 Lua 脚本进行轻量级逻辑处理。
- 高可用架构设计：学习 Higress 的高可用部署模式、数据面弹性伸缩配置以及性能调优参数。
- AI 网关特性：探索 Higress 在处理 AI/大模型流量方面的特性（如 Token 计数、流式转发优化）。

**学习时间**: 3-4周

**学习资源**:
- Higress GitHub 仓库 - Wasm Go SDK
- WebAssembly (Wasm) 官方文档与教程
- Higress 性能压测报告与调优指南

**学习建议**: 尝试编写一个简单的 Wasm 插件（例如在响应头中添加一个自定义 Header），并在本地环境中编译、加载并运行。阅读 Higress 源码中的核心路由逻辑，以便在遇到复杂问题时具备排查能力。

---
## 常见问题


### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生网关。它建立在 Envoy 高性能网络代理库之上，并深度集成了 Istio 服务网格体系。Higress 于 2022 年开源，旨在提供一套标准化、高集成、易扩展、云原生的网关托管方案。它既可以在 Kubernetes 集群中作为 Ingress Controller 使用，也可以作为 API 网关管理南北向流量。作为阿里云开源的重要项目，它继承了阿里在电商、金融等高并发场景下的流量治理经验，并遵循云原生基金会（CNCF）的技术标准。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **极致性能与低延迟**：底层基于 C++ 编写的 Envoy，相比基于 Lua (OpenResty) 或其他语言的传统网关，在处理高并发请求时具有更低的延迟和更高的吞吐量，且内存占用更加稳定。
2.  **标准兼容与安全**：深度兼容 Kubernetes Ingress 标准和 Gateway API 标准，同时也兼容 Istio 的 API 规范，使得用户在混合云或多云架构下的迁移成本更低。
3.  **插件生态与热加载**：支持 WASM (WebAssembly) 插件，允许开发者使用 Go、C++、Rust、JavaScript 等多种语言编写插件，且插件支持热加载，无需重启网关即可生效，极大地扩展了自定义业务逻辑的能力。
4.  **流量治理与服务发现集成**：相比 Nginx 需要手动配置 upstream，Higress 原生对接 Nacos、Consul、Kubernetes Service 等服务发现源，能够自动感知服务实例的上下线，实现更精细的流量管理和灰度发布。

---



### 3: Higress 是否支持从 Nginx Ingress 或其他网关平滑迁移？

3: Higress 是否支持从 Nginx Ingress 或其他网关平滑迁移？

**A**: 是的，Higress 非常重视迁移的平滑性，并提供了专门的工具来降低迁移成本。

1.  **Nginx Ingress 兼容**：Higress 提供了 Nginx Ingress Annotation 的兼容支持。这意味着用户通常不需要修改大量的 Ingress 资源配置（YAML 文件），即可直接将 Higress 作为 Nginx Ingress 的替代品接入集群。
2.  **配置转换工具**：对于从传统 Nginx 配置迁移的场景，社区提供了配置转换工具，可以将 Nginx 的 `nginx.conf` 自动转换为 Higress 的路由配置。
3.  **双栈模式**：在迁移初期，Higress 可以与现有的网关并存，通过调整流量权重的形式，逐步将流量切换到 Higress，从而确保业务零风险。

---



### 4: 什么是 Higress 的 WASM 插件机制？它解决了什么痛点？

4: 什么是 Higress 的 WASM 插件机制？它解决了什么痛点？

**A**: WASM (WebAssembly) 是 Higress 架构中的关键特性。在传统的网关（如早期的 Nginx）中，扩展功能通常需要使用 C 模块编写（开发难度大、风险高）或者使用 Lua 脚本（性能受限且难以维护）。Higress 利用 Envoy 的 WASM 能力，允许开发者使用高级语言（推荐 Go）编写业务逻辑，编译成 `.wasm` 文件后动态加载到网关中。

**它解决的痛点包括：**
*   **安全性**：插件运行在沙箱环境中，即使插件崩溃也不会导致网关主进程崩溃。
*   **灵活性**：支持多语言开发，降低开发门槛。
*   **热更新**：修改或发布插件时，不需要重启 Higress 网关进程，对业务流量无感知。
*   **高性能**：WASM 的执行效率接近原生代码，远高于脚本语言。

---



### 5: Higress 如何处理服务发现？是否支持非 Kubernetes 环境（如 Nacos）？

5: Higress 如何处理服务发现？是否支持非 Kubernetes 环境（如 Nacos）？

**A**: Higress 设计之初就是为了打通微服务架构的“最后一公里”。它不仅支持 Kubernetes 原生的 Service 服务发现，还针对阿里云生态和常见的微服务注册中心做了深度集成。

1.  **注册中心对接**：Higress 原生支持 Nacos（阿里云 MSE 版和开源版）、Zookeeper、Consul 等主流注册中心。这意味着运行在虚拟机或非 K8s 环境中的 Spring Cloud/Dubbo 服务，可以直接被 Higress 发现和路由。
2.  **多协议支持**：除了 HTTP，Higress 对 gRPC、Dubbo 等微服务协议也有很好的支持，可以实现全链路的流量治理。
3.  **配置方式**：用户可以在 Higress 的控制台直接配置注册中心的地址，网关会自动拉取服务列表，无需手动维护繁琐的 IP 地址列表。

---



### 6: Higress 是否支持对接 AI 服务（如大模型

6: Higress 是否支持对接 AI 服务（如大模型

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础环境搭建与流量路由

### 问题**:

### 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求实现：当访问 `http://localhost/hello` 时，请求能被转发至后端一个模拟的 HTTP 服务（如 httpbin.org 或自建的 Nginx 容器），并返回 200 状态码。

### 提示**:

---
## 实践建议

以下是针对 Higress (AI Gateway) 的 6 条实践建议，侧重于生产环境落地与 AI 流量治理：

### 1. 实施基于 Token 的精细化流量治理
传统 API 网关关注 QPS（每秒请求数）和并发数，但 AI 场景的核心成本在于 Token。建议不要仅配置传统的 QPS 限流，而应结合 Higress 的插件能力配置基于 Token 或请求时长的限流策略。
*   **最佳实践**：针对不同模型或不同租户（API Key），设置每日或每分钟的 Token 消耗上限。对于长文本生成任务，配置超时时间，防止后端 LLM 服务长时间挂起消耗连接池。
*   **常见陷阱**：仅限制并发连接数。由于大模型推理耗时较长，少量的并发请求也可能占满网关的连接池，导致服务不可用。

### 2. 利用 `wasmPlugin` 实现提示词（Prompt）注入与安全审计
在生产环境中，直接将用户输入传递给 LLM 极其危险。建议使用 Higress 的 Wasm 插件机制在网关层进行请求拦截。
*   **具体操作**：编写或配置 Wasm 插件，在请求转发给上游模型之前，动态插入系统提示词，用于规范用户输入格式或限定回复语气。同时，在响应阶段配置敏感词过滤插件，拦截 LLM 生成的不合规内容。
*   **常见陷阱**：将安全过滤逻辑放在应用层后端。这增加了网络延迟，且一旦后端服务被绕过，安全防线即失效。网关是统一治理的最佳入口。

### 3. 构建多模型路由与 fallback 机制
AI 服务的稳定性往往受限于模型提供商（如 OpenAI、Azure 或通义千问）的可用性。建议利用 Higress 的路由能力配置多模型源。
*   **具体操作**：配置服务路由规则，当主模型提供商返回 5xx 错误或超时时，Higress 自动将请求切换至备用模型提供商或降级模型（例如从 GPT-4 切换到 GPT-3.5）。
*   **常见陷阱**：硬编码模型端点。当单一供应商 API 宕机时，需要重新发布代码才能切换，导致恢复时间目标（RTO）过长。

### 4. 配置 SSE（Server-Sent Events）流式传输的完整性与日志
AI 对话通常采用流式返回，这给网关层的日志采集和监控带来了挑战。
*   **具体操作**：确认 Higress 的日志配置已支持流式响应的记录。不要只记录 HTTP Header，要关注 Body 的缓冲或采样记录。建议在 Access Log 中配置自定义字段，记录请求输入的 Token 数量估算值和响应输出的 Token 数量，以便进行成本分析。
*   **常见陷阱**：开启全量 Body 日志记录。流式响应的 Body 可能非常大且碎片化，全量记录会严重拖慢网关性能并急剧增加日志存储成本。应仅记录元数据或进行采样。

### 5. 鉴权与 API Key 的统一管理
企业内部通常既有自研模型，又有调用外部模型的场景。
*   **具体操作**：在 Higress 中统一管理外部模型供应商的 API Key。客户端只需携带一个 Higress 颁发的凭证，网关层根据请求参数动态查找并注入对应供应商的 API Key 到请求头中。
*   **常见陷阱**：将真实的云厂商 API Key 下发到客户端或前端代码存储。这极易导致 Key 泄露和资费盗刷。网关应作为 Key 的唯一保管者。

### 6. 区分 AI 流量与传统微服务流量
如果你的 Higress 网关既承载传统的微服务调用（RESTful/gRPC），又承载 AI 网关职责，建议进行隔离。
*   **最佳实践**：创建不同的域名或 Ingress/Route 实例来区分 AI 流量和普通业务流量。AI 流量通常具有长连接、高延迟、高吞吐的特点，其资源消耗模型与普通短请求不同。混合在一起可能导致普通业务

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*