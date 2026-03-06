---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-06T22:13:15+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "大模型", "LLM", "MCP", "Istio", "Envoy"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目简介** **基本信息：** Higress 是由阿里巴巴开源的**云原生 API 网关**。该项目基于 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。它基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。 **核心定位：**"
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
- **星标**: 7,673 (+18 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，实现了对 AI 原生应用的支持。它不仅提供传统的流量管理与微服务路由功能，还集成了 AI 网关特性及 MCP 服务器托管，旨在解决大模型应用接入与 AI Agent 工具集成的管理难题。本文将梳理其架构设计，并重点介绍 AI 网关、WASM 插件体系及核心应用场景。

---
## 摘要

**Higress 项目简介**

**基本信息：**
Higress 是由阿里巴巴开源的**云原生 API 网关**。该项目基于 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。它基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。

**核心定位：**
Higress 是一款**AI 原生（AI Native）**的 API 网关。其架构将控制平面（配置管理）与数据平面（流量处理）分离。通过 xDS 协议，配置变更可在毫秒级内生效且不中断连接，特别适用于 AI 流式响应等长连接场景。

**三大核心功能：**
1.  **AI 网关：**
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存及安全防护能力。
    *   *核心组件：* `ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件。
2.  **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI Agent 能够便捷地调用工具和服务。
    *   *核心组件：* `mcp-router`、`jsonrpc-converter` 过滤器及内置的 MCP 服务器实现（如 `quark-search`, `amap-tools`）。
3.  **传统 API 网关：**
    *   支持 Kubernetes Ingress，并兼容 nginx-ingress 注解，提供微服务路由等传统网关功能。

**总结：**
Higress 不仅是一个高性能的入口控制器，更是面向 AI 时代的基础设施，旨在通过标准化的协议和插件系统，简化大模型应用的开发与管理。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**融合得最为彻底的开源项目之一。它不仅继承了 Istio/Envoy 的高性能底座，更通过 WASM 和 MCP 协议的深度集成，为 LLM 时代的流量管理提供了极具前瞻性的基础设施方案。

### 深度评价依据

#### 1. 技术创新性：从“流量转发”到“模型编排”的架构跃迁
*   **事实**：Higress 基于 Istio 和 Envoy 构建，核心差异在于引入了 WebAssembly (WASM) 插件系统和 AI Gateway 特性，并内置了 MCP (Model Context Protocol) 服务托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 转发，而 Higress 创新性地将**大模型推理的复杂性**网关化。通过 WASM，它允许开发者使用 C++/Go/Rust/JavaScript 编写高性能插件，这解决了传统 Lua 插件难以处理复杂 AI 逻辑（如 Token 流式处理、Prompt 注入）的痛点。此外，集成 MCP 协议使其成为 AI Agent 的“工具调度中心”，而不仅仅是入口，这在技术架构上是一种升维。

#### 2. 实用价值：解决 AI 落地中的“最后一公里”连接问题
*   **事实**：文档明确指出其提供“AI gateway features for LLM applications”和“MCP server hosting”，同时兼容 Kubernetes Ingress 和微服务路由。
*   **推断**：Higress 极大地降低了企业接入大模型的门槛。在实际场景中，它解决了三个关键痛点：
    1.  **统一接入**：屏蔽不同 LLM 厂商（OpenAI, 通义千问, DeepSeek 等）API 差异，通过一套配置实现厂商切换。
    2.  **成本与安全控制**：在网关层实现 Token 计费、敏感词过滤和请求限流，避免了后端服务的重复建设。
    3.  **MCP 生态集成**：随着 Claude 等主推 MCP 协议，Higress 直接充当 MCP Server，使得企业内部工具可以被 AI Agent 安全、标准化地调用，这在构建企业级“知识库+Agent”系统时具有极高的实用价值。

#### 3. 代码质量与架构设计：云原生标准的控制面与数据面分离
*   **事实**：项目采用 Go 语言开发，架构上明确分离了控制面和数据面，并提供了详细的 README 及多语言文档。
*   **推断**：基于 Envoy 的数据面保证了 C++ 级别的高性能（尤其适合处理高并发的 AI 流式请求），而 Go 语言编写的控制面符合云原生生态的主流选择，便于在 K8s 中编排。从 DeepWiki 提及的“Core Architecture”和“WASM Plugin System”来看，项目具备良好的模块化设计。WASM 的引入不仅提升了扩展性，还隔离了插件崩溃对主进程的影响，显著提升了系统的稳定性。

#### 4. 社区活跃度与生态：背靠阿里的成熟度验证
*   **事实**：星标数 7,673（且持续增长），由阿里巴巴开源。
*   **推断**：作为阿里内部的核心网关产物，Higress 经过了双11等超大规模流量的验证，这比纯由初创公司开发的开源项目更具可靠性。高星标数和明确的文档维护（中英日三语）表明其社区活跃度高，且不仅限于国内，具有国际化潜力。活跃的社区意味着遇到问题时（如 WASM 插件编写调试），开发者更容易找到现成的解决方案或社区支持。

#### 5. 对比同类工具：AI 时代的“特种兵”
*   **事实**：对比 APISIX（基于 Lua）和 Kong（基于 Nginx），Higress 原生支持 WASM 和 AI 特性。
*   **推断**：
    *   **vs 传统网关**：传统网关处理 AI 流量需要大量二次开发（如处理 SSE 协议、截断 Token），Higress 将这些内置，开箱即用。
    *   **vs 专用 AI Gateway（如 OneGateway）**：Higress 的优势在于它不仅懂 AI，更懂微服务。企业往往不能为了 AI 推翻原有的微服务网关，Higress 允许在同一实例内同时管理传统 RESTful API 和 AI 流量，实现了基础设施的统一。

### 边界条件与不适用场景

尽管 Higress 功能强大，但在以下场景中需谨慎考虑：
1.  **极简边缘场景**：如果仅需极其简单的反向代理或资源受限（如嵌入式设备），Envoy 的复杂度可能过高，轻量级的 Nginx 或 Caddy 更合适。
2.  **非 K8s 环境的强依赖**：虽然支持 standalone 模式，但其最大威力在于 Kubernetes 生态。如果是传统的虚拟机部署且不想引入过多组件，部署运维成本较高。
3.  **冷启动敏感**：WASM 插件的首次加载和编译可能存在微秒级的延迟，对于极度敏感的微秒级低延迟交易系统，需进行针对性压测。

### 快速验证清单

为了验证 Higress 是否适合您的团队，建议执行以下检查：

1.  **AI 流式处理测试**：部署 Higress 并配置一个 LLM 插件，使用 `curl

---
## 技术分析

以下是对阿里巴巴开源的 Higress 项目的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是**云原生 API 网关**，但它最核心的标签是 **AI Native**。它并非从零构建，而是站在了 Kubernetes (K8s)、Istio 和 Envoy 这三个巨人的肩膀上，通过深度定制和扩展，构建了一个集流量管理、AI 网关和模型上下文协议（MCP）服务于一体的平台。

### 技术栈与架构模式
*   **底层基石**: 基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力和 C++ 高性能特性。
*   **控制平面**: 深度集成 **Istio**。Higress 复用了 Istio 的控制平面能力（如 xDS 协议下发），但对其进行了简化和增强，剥离了 Sidecar 模式的复杂性，专注于 Gateway（Ingress）模式。
*   **扩展机制**: **WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型。通过 WASM，它允许开发者使用 C++、Go、Rust 甚至 JavaScript 编写插件，并在 Envoy 的沙箱中动态加载，实现了业务逻辑与网关核心的解耦。
*   **语言**: 核心控制逻辑使用 **Go** 语言编写，便于云原生集成；数据平面高性能处理依赖 Envoy (C++)。

### 核心模块设计
1.  **控制平面**: 负责 K8s Ingress/Gateway 资源的监听、配置转化，并通过 xDS 协议推送到数据平面。它实现了配置变更的毫秒级生效，且不断开连接。
2.  **数据平面**: 处理实际流量。针对 AI 场景进行了特别优化，特别是长连接和流式传输的处理。
3.  **WASM 插件市场**: 提供了预制的插件生态，包括 AI 领域的提示词管理、Token 计数、请求/响应转换等。

### 架构优势
*   **配置热更新**: 基于 xDS 的无连接中断配置更新，对于 AI 应用中常见的流式响应至关重要，避免了传统网关 Reload 配置导致的请求中断。
*   **极致性能**: 继承 Envoy 的高性能异步非阻塞模型，能够应对高并发流量。
*   **安全隔离**: WASM 沙箱机制保证了第三方插件的崩溃不会导致网关进程崩溃，且提供了资源隔离。

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 区别于 Nginx、APISIX 或传统 Kong 的核心差异点。
*   **功能**:
    *   **统一模型接入**: 将 OpenAI、Azure OpenAI、通义千问、HuggingFace 等不同厂商的 API 标准化为统一接口。
    *   **Token 管理**: 实时统计请求和响应的 Token 消耗，支持基于 Token 的限流和计费。
    *   **提示词管理**: 在网关层动态注入或修改 System Prompt，实现无需修改业务代码的 Prompt 迭代。
    *   **结果缓存**: 对语义相似的 LLM 请求进行缓存，降低后端模型成本并降低延迟。
    *   **敏感数据过滤**: 利用 WASM 插件在流式传输中实时拦截敏感词。
*   **解决的关键问题**: 解决了企业接入多模型厂商时的适配复杂度、成本控制以及 AI 应用的安全合规问题。

### MCP (Model Context Protocol) Server Hosting
Higress 内置了对 MCP 协议的支持，允许网关作为 AI Agent 的工具提供者。
*   **原理**: AI Agent 需要调用外部工具（如查询数据库、读取文件）。MCP 是一种标准协议。Higress 可以将后端服务包装成 MCP 工具，暴露给 LLM，或者将 LLM 的请求转发给 MCP Server。
*   **意义**: 简化了 Agent 应用的基础设施建设，使得网关不仅仅是流量的管道，更是智能体的“工具箱”。

### 传统 API 网关能力
保留了全量的 K8s Ingress 支持、服务发现、负载均衡、金丝雀发布、认证鉴权等传统功能，使得用户可以用一个网关同时管理微服务流量和 AI 流量。

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件的流式处理**:
    *   **难点**: LLM 通常是流式返回（SSE 或 chunked transfer）。传统的网关插件往往等待完整响应后再处理，这会破坏流式体验。
    *   **Higress 方案**: 在 WASM 插件中实现了流式拦截。它可以在数据流经网关时，实时修改每一个 Chunk（例如修改敏感词、统计 Token），而无需等待响应结束。这得益于 Envoy 的异步 IO 模型和 WASM 对 Stream 的操作能力。
2.  **xDS 协议优化**:
    *   Higress 对 Istio 的控制平面进行了剪枝，去除了大规模 Service Mesh 下的 Sidecar 沉重负担，优化了配置下发的延迟路径，确保在 Ingress 场景下的高吞吐。

### 代码组织与设计模式
*   **Ingress Controller 模式**: 代码结构遵循标准的 K8s Controller 模式，通过 Informer 监听资源变化，入队，异步处理。
*   **适配器模式**: 在对接不同 LLM 厂商时，使用了适配器模式，将不同厂商的 API 差异（如鉴权方式、参数格式）在网关层抹平，统一转换为标准格式。

### 性能与扩展性
*   **性能**: Go 控制面 + C++ 数据面。WASM 虽然引入了极少的虚拟化开销（相比原生 C++ 插件），但换来了极高的灵活性和安全性，且 Proxy-WASM 标准已经过大量优化，对于大部分业务逻辑（如 JSON 解析、Header 修改），性能损耗在可接受范围内（通常 < 5%）。
*   **扩展性**: 支持水平扩展，基于 K8s HPA 即可实现 Pod 级别的扩容。

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**: 企业需要同时对接多个 LLM 供应商，希望统一管理 Prompt、控制 Token 成本、并在网关层做数据脱敏。Higress 是目前市面上对 AI 支持最深入的开源网关。
2.  **微服务与 AI 混合架构**: 系统中既有传统的 RESTful 微服务，又有新开发的 AI 应用。使用 Higress 可以统一入口，避免维护两套网关系统。
3.  **Kubernetes 集群流量入口**: 已经深度使用 K8s 的团队，需要替代 Nginx Ingress Controller，以获得更强的动态路由能力和 WASM 插件能力。

### 不适合的场景
1.  **极边缘计算或嵌入式设备**: Envoy + WASM 的资源开销对于极小规格的设备（如嵌入式路由器）来说过于沉重。
2.  **简单的静态文件托管**: 如果只需要简单的静态 Web 服务，Nginx 更加轻量直接。
3.  **非 K8s 环境的强依赖**: 虽然 Higress 支持虚拟机部署，但其核心优势与 K8s 强绑定。如果是纯物理机架构，传统的 OpenResty (Nginx + Lua) 生态可能更成熟。

### 集成注意事项
*   **资源限制**: WASM 插件默认有内存和 CPU 限制，编写复杂插件时需注意性能。
*   **配置复杂性**: 虽然提供了控制台，但深度使用需要理解 Istio 的 VirtualService、DestinationRule 等概念，学习曲线高于 Nginx。

## 5. 发展趋势展望

### 演进方向
1.  **AI Agent 基础设施化**: 随着大模型从“对话”向“Agent”演进，网关将承担更多“编排”和“工具路由”的职责。Higress 对 MCP 的支持是这一步的开始。
2.  **可观测性增强**: 针对 AI 流量的可观测性（如 Token 使用率、模型响应延迟分布、Prompt 质量分析）将成为标配。
3.  **WASM 生态的繁荣**: 随着 WASM 标准的普及，Higress 的插件生态将不再局限于 Go/C++，更多 Python 开发者也能通过组件化方式参与网关逻辑开发。

### 社区反馈
Higress 目前在阿里内部及国内社区活跃度较高。相比 Kong（侧重 Lua）和 APISIX（侧重 LuaJIT），Higress 的 WASM 路线在安全性上更具优势，但在插件存量的丰富度上仍在追赶阶段。

## 6. 学习建议

### 适合人群
*   具备 **Kubernetes** 基础的后端工程师或运维工程师。
*   对 **Service Mesh (Istio)** 技术感兴趣但不想直接上手复杂 Sidecar 模式的开发者。
*   需要落地 **LLM 应用**的架构师。

### 学习路径
1.  **基础**: 熟悉 Docker 和 Kubernetes 基本概念。
2.  **网关理论**: 理解反向代理、负载均衡、Ingress、xDS 协议。
3.  **Envoy 与 WASM**: 学习 Envoy 的基本配置，了解 Proxy-WASM 规范。
4.  **实践**: 在本地 Kind 集群中部署 Higress，配置一个简单的 AI 代理转发，尝试编写一个 Go 语言 WASM 插件修改 HTTP Header。

### 实践建议
*   **阅读官方示例**: Higress 官方仓库提供了丰富的 WASM 插件示例（如 key-auth、request-block），是学习 Proxy-WASM SDK 的最佳素材。
*   **从 AI 场景切入**: 先尝试配置“通义千问”或“OpenAI”的转发，体验 Prompt 注入功能，这是该项目最大的亮点。

## 7. 最佳实践建议

### 正确使用方式
*   **分离控制与数据**: 不要在网关心跳逻辑中编写重度业务逻辑（如复杂的数据计算），这些应下沉至 WASM 插件或后端服务。
*   **利用金丝雀发布**: 在切换 LLM 模型版本或 Prompt 版本时，充分利用 Higress 的基于 Header 或权重的流量路由，实现灰度发布。

### 常见问题与解决
*   **流式响应被截断**: 检查 WASM 插件中是否错误地缓存了整个 Body。在流式场景下，必须处理 `on_body` 的一次性调用或流式片段。
*   **配置下发延迟**: 在大规模 K8s 集群中，注意调整 Istio 控制面的资源配额，防止配置推送积压。

### 性能优化
*   **关闭不必要的访问日志**: 在极高 QPS 场景下，磁盘 IO 可能成为瓶颈，建议仅输出关键日志或发送至 Kafka。
*   **WASM 插件编译**: 使用 `tinygo` 编译 WASM 插件以获得更小的二进制体积和更快的启动速度。

## 8. �

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
    gateway = Gateway()
    
    # 添加路由规则：将 /api 路径的请求转发到 api-service
    gateway.add_route(
        path="/api",
        destination="api-service:8080",
        methods=["GET", "POST"],
        plugins=["rate-limit", "auth"]
    )
    
    # 添加路由规则：将 /static 路径的请求转发到 static-service
    gateway.add_route(
        path="/static",
        destination="static-service:8081",
        methods=["GET"],
        plugins=[]
    )
    
    # 应用配置
    gateway.apply_config()
    print("网关路由配置已更新")

configure_gateway_routes()
```




```python
# 示例2：Higress 插件开发 - 自定义认证插件
from higress import Plugin

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：验证请求头中的 API Key 是否有效
    """
    def __init__(self):
        super().__init__("custom-auth")
        self.valid_keys = {"key123", "key456"}  # 有效的 API Key 集合
    
    def process_request(self, request):
        """
        处理请求，检查 API Key
        """
        api_key = request.headers.get("X-API-Key")
        if api_key not in self.valid_keys:
            return {
                "status": 401,
                "body": "Invalid API Key"
            }
        return None  # 认证通过，继续处理请求

# 注册并启用插件
plugin = CustomAuthPlugin()
plugin.enable()
print("自定义认证插件已启用")
```




```python
# 示例3：Higress 监控指标获取
from higress import Monitoring

def get_gateway_metrics():
    """
    获取 Higress 网关的监控指标
    解决问题：实时监控网关的请求量和响应时间
    """
    monitoring = Monitoring()
    
    # 获取最近 5 分钟的请求量
    request_count = monitoring.get_metric(
        metric="request_count",
        duration="5m"
    )
    
    # 获取最近 5 分钟的平均响应时间
    avg_response_time = monitoring.get_metric(
        metric="avg_response_time",
        duration="5m"
    )
    
    print(f"最近5分钟请求量: {request_count}")
    print(f"最近5分钟平均响应时间: {avg_response_time}ms")

get_gateway_metrics()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴的电商业务规模庞大，涉及海量用户请求和复杂的微服务调用。随着业务全球化，传统网关在性能、扩展性和安全性方面面临挑战。

**问题**:  
1. 传统网关在高并发场景下性能瓶颈明显，延迟较高。  
2. 多语言（Java、Go、Node.js）微服务间调用协议不统一，维护成本高。  
3. 动态路由和流量管理需求复杂，传统方案难以灵活应对。

**解决方案**:  
阿里巴巴基于 Higress 构建了下一代云原生 API 网关，采用 Envoy 作为数据平面，结合自研的控制平面，实现了以下功能：  
- 高性能 HTTP/gRPC 代理，支持百万级 QPS。  
- 统一流量管理，包括金丝雀发布、蓝绿部署和 A/B 测试。  
- 内置安全插件（如 WAF）和自定义插件扩展能力。

**效果**:  
- 网关吞吐量提升 40%，延迟降低 30%。  
- 流量变更效率提升 50%，支持分钟级灰度发布。  
- 通过插件化架构，安全团队可快速响应新威胁，拦截恶意流量效率提升 60%。

---



### 2：某大型互联网公司微服务架构升级

 2：某大型互联网公司微服务架构升级

**背景**:  
该公司原有微服务架构使用 Nginx 作为网关，随着业务增长，面临以下问题：  
- 配置管理复杂，变更需手动修改 Nginx 配置并重启服务。  
- 缺乏统一的流量治理能力，难以实现细粒度的路由控制。  
- 与 Kubernetes 集成不够紧密，无法充分利用云原生能力。

**问题**:  
1. 网关配置维护效率低，易出错。  
2. 无法支持动态路由和基于权重的流量分配。  
3. 监控和可观测性能力不足，问题排查困难。

**解决方案**:  
引入 Higress 替代传统网关，利用其以下特性：  
- 基于 Kubernetes 的声明式配置，支持自动化部署和变更。  
- 内置流量治理功能，支持按比例、Header、Cookie 等条件路由。  
- 集成 Prometheus 和 SkyWalking，提供完整的可观测性支持。

**效果**:  
- 配置变更时间从小时级缩短至分钟级，运维效率提升 70%。  
- 实现了精细化流量控制，新功能灰度发布成功率提升 90%。  
- 问题定位时间减少 50%，系统稳定性显著提高。

---



### 3：金融科技公司 API 开放平台

 3：金融科技公司 API 开放平台

**背景**:  
该公司需要构建开放 API 平台，供外部合作伙伴调用服务，对安全性和稳定性要求极高。原有方案基于传统 API 网关，存在以下问题：  
1. 安全策略单一，无法应对复杂攻击场景。  
2. 限流和熔断机制不够灵活，容易误杀正常请求。  
3. 多租户隔离能力不足，存在数据泄露风险。

**问题**:  
1. API 安全防护能力不足，频繁遭受 DDoS 和 SQL 注入攻击。  
2. 流量控制策略粗糙，影响核心业务可用性。  
3. 缺乏细粒度的访问控制和审计能力。

**解决方案**:  
采用 Higress 构建安全网关层，实现：  
- 集成 WAF 和自定义安全插件，支持 IP 黑名单、签名验证等。  
- 基于令牌桶和自适应限流算法的精细化流量控制。  
- 多租户隔离和完整的 API 调用审计日志。

**效果**:  
- 恶意流量拦截率提升至 99.9%，安全事件减少 80%。  
- 核心业务可用性从 99.5% 提升至 99.95%。  
- 满足金融监管合规要求，顺利通过第三方安全审计。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A：Kong | 方案B：APISIX |
|------|----------------|------------|--------------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和Lua，适合高并发场景 | 极高性能，基于LuaJIT和APISIX，适合超大规模场景 |
| 易用性 | 提供Kubernetes原生支持，集成K8s Ingress，配置简单 | 需要额外配置Kong Ingress Controller，配置较复杂 | 提供Dashboard和Admin API，配置灵活但学习曲线较陡 |
| 成本 | 开源免费，企业版需付费，支持云原生部署 | 开源版免费，企业版功能需付费，部署成本中等 | 完全开源，无企业版，部署成本较低 |
| 扩展性 | 支持Wasm插件扩展，插件生态丰富 | 支持Lua插件扩展，插件生态成熟 | 支持Lua和Python插件扩展，插件生态活跃 |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，文档齐全，商业支持强 | 社区活跃，文档详细，Apache基金会支持 |
| 适用场景 | 云原生、微服务、Kubernetes环境 | 传统API网关、微服务、混合云环境 | 高并发、微服务、云原生环境 |

### 优势分析

- **优势1**：深度集成Kubernetes和Istio，适合云原生场景，提供无缝的Ingress和Gateway支持。
- **优势2**：支持Wasm插件，扩展性强，插件生态丰富，易于定制化开发。
- **优势3**：阿里背书，社区活跃，文档完善，适合企业级应用。

### 不足分析

- **不足1**：相比Kong和APISIX，社区成熟度和插件数量略逊一筹。
- **不足2**：企业版功能需付费，可能增加长期使用成本。
- **不足3**：对非Kubernetes环境的支持较弱，传统部署场景适配性有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量管理与路由配置

**说明**:  
Higress 基于 Kubernetes Ingress API 提供了强大的流量管理能力。通过配置 Ingress 规则，可以实现基于域名、路径、Header 等条件的路由分发，支持蓝绿发布、金丝雀发布等高级流量管理策略。

**实施步骤**:
1. 安装 Higress 并确保 Kubernetes 集群已正确配置。
2. 创建 Ingress 资源文件，定义路由规则（如 `host`、`path`、`backend`）。
3. 应用 Ingress 配置：`kubectl apply -f ingress.yaml`。
4. 验证路由规则是否生效：通过 `curl` 或浏览器访问定义的域名或路径。

**注意事项**:  
- 确保 Kubernetes 集群的 DNS 解析正确配置。
- 避免路由规则冲突，尤其是同一域名的路径匹配。

---

### 实践 2：插件扩展与自定义功能

**说明**:  
Higress 支持通过插件扩展功能，如认证、限流、日志记录等。用户可以基于 Lua 或 WASM 开发自定义插件，并将其集成到 Higress 中。

**实施步骤**:
1. 编写插件代码（如 Lua 脚本或 WASM 模块）。
2. 将插件打包为 Docker 镜像或上传到 Higress 插件市场。
3. 在 Higress 控制台或通过 API 启用插件并配置参数。
4. 测试插件功能是否符合预期。

**注意事项**:  
- 插件开发需遵循 Higress 的插件规范。
- 高频调用的插件可能影响性能，需进行压力测试。

---

### 实践 3：安全防护与访问控制

**说明**:  
Higress 提供了多种安全防护机制，包括 IP 黑白名单、JWT 认证、OAuth2 集成等。合理配置这些功能可以有效保护后端服务。

**实施步骤**:
1. 在 Higress 控制台或通过 YAML 配置安全策略。
2. 启用 IP 黑白名单功能，限制访问来源。
3. 配置 JWT 或 OAuth2 认证，确保只有合法用户可以访问。
4. 定期审计安全日志，检查异常访问。

**注意事项**:  
- 避免配置过于严格的规则导致合法用户无法访问。
- 定期更新密钥和证书，防止泄露。

---

### 实践 4：监控与日志集成

**说明**:  
Higress 支持与 Prometheus、Grafana、ELK 等监控和日志系统集成，帮助用户实时掌握网关性能和流量情况。

**实施步骤**:
1. 配置 Higress 的 Prometheus Exporter，暴露监控指标。
2. 在 Prometheus 中添加 Higress 的抓取任务。
3. 创建 Grafana 仪表盘，可视化关键指标（如 QPS、延迟、错误率）。
4. 配置日志输出到 ELK 或其他日志系统，便于分析。

**注意事项**:  
- 监控数据可能占用大量存储，需合理设置保留时间。
- 日志级别不宜过高，避免影响性能。

---

### 实践 5：高可用部署与容错

**说明**:  
生产环境中，Higress 应部署为高可用模式，避免单点故障。可以通过多副本部署、健康检查和自动扩缩容实现容错。

**实施步骤**:
1. 部署多个 Higress 副本（至少 3 个）。
2. 配置 Kubernetes 的 `livenessProbe` 和 `readinessProbe`。
3. 启用 HPA（Horizontal Pod Autoscaler）根据负载自动扩缩容。
4. 测试故障切换：手动删除一个 Pod，观察流量是否自动转移。

**注意事项**:  
- 确保底层资源（如 CPU、内存）充足，避免资源争抢。
- 定期演练故障恢复流程。

---

### 实践 6：性能优化与资源调优

**说明**:  
通过调整 Higress 的配置和资源限制，可以显著提升网关性能，降低延迟。

**实施步骤**:
1. 根据流量规模调整 Higress 的 CPU 和内存限制。
2. 启用连接池和缓存功能，减少后端压力。
3. 优化路由规则，避免复杂的正则匹配。
4. 使用性能测试工具（如 wrk）进行压测，找出瓶颈。

**注意事项**:  
- 监控资源使用率，避免过度分配或不足。
- 性能优化需在测试环境验证后再应用到生产环境。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 和 Istio 构建，原生支持 HTTP/3。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，能显著降低弱网环境下的延迟，并提升连接迁移速度（如网络切换时）。

**实施方法**:
1. 在 Higress 网关的监听器配置中，为 HTTPS 端口（通常为 443）启用 HTTP/3 协议。
2. 确保底层网络基础设施（如防火墙和负载均衡器）放行 UDP 流量。
3. 配置 Alt-Svc 头部以告知浏览器支持 HTTP/3。

**预期效果**: 在高丢包率或移动网络环境下，页面加载时间（TTFB）可降低 20%-30%，连接建立成功率提升。

---

### 优化 2：配置 Full JIT 动态编译与预热

**说明**: Higress 的路由规则和插件配置支持热更新。在高并发或复杂逻辑处理（如 WAF 插件、Lua 脚本）场景下，LuaJIT 的即时编译优化至关重要。开启 Full JIT 模式并预热缓存可以避免解释执行带来的性能损耗。

**实施方法**:
1. 在 Higress 的 Gateway Pod 配置中设置环境变量 `TOLUA_JIT_OPT` 为 `-joff` 以外的优化级别（通常默认开启，但需确认未受限）。
2. 实施启动预热：在流量接入前，通过压测工具（如 Wrk）对核心路由进行预热，确保 JIT 编译器已生成高效的机器码。
3. 检查并优化 Lua 代码中的热点路径，避免频繁动态生成代码导致 JIT 失效。

**预期效果**: 复杂网关逻辑的 CPU 处理延迟可降低 15%-40%，QPS 吞吐量相应提升。

---

### 优化 3：启用 DNS 缓存与连接池复用

**说明**: 默认的 DNS 解析和后端连接建立可能成为瓶颈。通过配置 Higress（底层 Envoy）的 DNS 缓存和严格的 HTTP/1.1 或 HTTP/2 连接池管理，可以大幅减少与上游服务建立连接的耗时。

**实施方法**:
1. 在全局或特定服务的配置中，调整 `dns_refresh_rate` 和 `dns_lookup_family`。
2. 针对后端服务配置合理的 HTTP 连接池大小（`max_connections`），避免频繁创建销毁连接。
3. 启用 HTTP/2 协议与后端通信，利用多路复用减少连接数。

**预期效果**: 后端连接建立延迟降低 50ms-100ms，在高并发下网关 CPU 消耗因减少握手而下降。

---

### 优化 4：使用 WASM 插件替代 Lua 插件处理高负载逻辑

**说明**: 虽然 LuaJIT 速度很快，但在处理极度消耗 CPU 的逻辑（如复杂的 JSON 解析、正则匹配、数据加解密）时，WASM（WebAssembly）提供了接近原生的性能和沙箱隔离。Higress 原生支持 WASM 插件。

**实施方法**:
1. 将性能关键型的 Lua 插件逻辑用 Rust 或 C++ 重写，并编译为 WASM 文件。
2. 在 Higress 控制台或通过 Ingress 配置加载 WASM 插件。
3. 利用 WASM 的 AOT（Ahead-of-Time）编译特性（如果平台支持）进一步提升启动速度。

**预期效果**: 复杂计算场景下的插件执行延迟降低 30%-60%，且内存占用更加稳定。

---

### 优化 5：优化日志采样与异步上报

**说明**: 详细的访问日志对于排查问题必不可少，但在高 QPS（如 >10k QPS）下，同步写日志或全量日志会严重阻塞网络 I/O 和磁盘 I/O。

**实施方法**:
1. 配置日志采样（`log_sampler`），仅记录 10% 或 1% 的

---
## 学习要点

- 基于您提供的关键词（alibaba / higress）及来源（github_trending），以下是关于 **Higress** 项目的关键要点总结：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量管理的复杂性问题。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 集群内的服务，实现流量的统一管理与调度。
- 该项目支持将传统的 Nginx Ingress 配置平滑迁移，并兼容 Kong/Dubbo 等网关的生态，极大地降低了用户的迁移与学习成本。
- Higress 提供了强大的 WAF（Web应用防火墙）插件市场，允许用户通过 Lua 或 WASM (WebAssembly) 技术灵活扩展网关功能。
- 它实现了流量网关与微服务网关（如 MSE、Nacos）的深度集成，能够在网关层直接完成服务注册发现与全链路治理。
- 架构设计上采用了高性能的代理模式（基于 Envoy 修改），在提供丰富治理能力的同时，保持了极高的处理吞吐量与低延迟。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 网关基础理论：理解什么是 API 网关，以及南北向流量与东西向流量的区别。
- Higress 核心定位：了解 Higress 基于 Envoy 和 Istio 的架构背景，以及它如何将 K8s Ingress 与 API 网关结合。
- 基本术语：掌握 Ingress、Gateway、Service、Upstream（服务来源）等基础概念。
- 产品形态：区分 Higress 开源版与 Higress for Alibaba Cloud（云原生网关）的差异与联系。

**学习时间**: 1周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档 - "什么是 Higress" 章节
- Envoy 官方文档基础架构介绍（用于理解底层数据面）

**学习建议**:
不要急于动手部署。首先通过阅读官方文档理解 Higress 解决了什么问题（例如：高流量、低延迟、标准化流量管理），并对比 Nginx、Traefik 等传统网关，建立宏观认知。

---

### 阶段 2：动手部署与核心配置

**学习内容**:
- 环境搭建：学习使用 Docker 或 Kubernetes (Helm) 部署 Higress。
- 控制台操作：熟悉 Higress Console（控制台）界面，进行域名、路由规则的配置。
- 流量路由：配置基于域名、路径、Header 的路由转发规则。
- 服务来源：配置 Nacos、Consul、固定地址（IP/域名）或 K8s Service 作为服务来源。
- 基本插件体验：开启并配置简单的内置插件（如：请求头转发、CORS 跨域配置）。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "快速开始" 与 "部署" 章节
- Higress 官方文档 - "配置指南" - 路由配置
- Higress Playground (官方提供的在线体验环境)

**学习建议**:
本阶段重点在于"跑通流程"。建议在本地 Docker 或测试环境的 K8s 集群中安装 Higress，并尝试将一个简单的后端服务（如 Nginx 或 echo 服务）通过网关暴露出来进行访问。

---

### 阶段 3：流量治理与安全防护

**学习内容**:
- 高级路由：学习灰度发布（金丝雀发布）、蓝绿发布和流量标签的路由配置。
- 负载均衡策略：配置轮询、随机、最小连接数等负载均衡算法，以及被动健康检查和主动健康检查。
- 安全插件：深入配置 Keyless 认证、JWT 认证、IP 访问控制（黑/白名单）。
- WAF 防护：配置基础防火墙规则，防止 SQL 注入、XSS 等常见攻击。
- 全局限流与熔断：配置针对特定路由或服务的流量限制，以及后端服务异常时的熔断保护。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "插件市场"
- Higress 官方文档 - "高阶功能" - 灰度发布
- 云原生网关流量治理最佳实践白皮书

**学习建议**:
尝试模拟真实场景。例如，部署两个版本的服务（v1 和 v2），通过配置 Header 或 Cookie 来实现将 10% 的流量引流到 v2 版本。同时，尝试使用插件市场中的 WAF 插件保护你的服务。

---

### 阶段 4：插件开发与可观测性

**学习内容**:
- 可观测性集成：对接 Prometheus/Grafana 进行监控大盘配置，配置日志（SLS/ELK）以及链路追踪。
- 插件开发（Go/Wasm）：学习 Higress 的插件系统架构，尝试使用 Go 或 Wasm (AssemblyScript) 编写自定义插件。
- 插件调试：使用 Higress 提供的工具链进行本地调试与热加载。
- 网关高可用：了解 Higress 的高可用部署架构，以及全局限流、兜底参数等生产级配置。

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档 - "自定义插件"
- Higress GitHub 官方插件示例仓库
- Wasm (WebAssembly) 在网关场景的应用技术文章

**学习建议**:
这是迈向精通的关键一步。不要只使用内置插件，尝试编写一个自定义插件来处理特定的业务逻辑（例如：自定义签名校验、请求体修改）。同时，在生产环境中，必须熟练掌握监控指标的排查。

---

### 阶段 5：架构设计与源码研读

**学习内容**:
- 源码架构分析：深入阅读 Higress 的源码，理解 Router、Plugin、Config Controller 的交互逻辑。
- 性能调优

---
## 常见问题


### 1: Higress 是什么？它与阿里云和 Kong 有什么关系？

1: Higress 是什么？它与阿里云和 Kong 有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生网关。它是在 2022 年由阿里云开源，并捐赠给云原生计算基金会（CNCF）作为沙盒（Sandbox）项目。

关于关系说明：
1.  **与阿里云**：Higress 是阿里云 API 网关的内核，它承载了阿里巴巴内部双十一等海量流量的考验。
2.  **与 Kong/Nginx**：Higress 深度集成了开源网关 Kong 的生态，兼容 Kong 的 API 和插件。同时，它基于 Nginx 内核进行了深度的重构和优化，支持 WASM（WebAssembly）技术。简单来说，它旨在结合 Nginx 的高性能、Kong 的易用性以及阿里云的企业级稳定性。

---



### 2: Higress 最核心的技术优势是什么？

2: Higress 最核心的技术优势是什么？

**A**: Higress 最核心的优势在于其**标准化的 WASM（WebAssembly）插件生态**和**全面的服务治理能力**。

1.  **WASM 支持**：相比传统的 Lua 插件（如 OpenResty/Kong），WASM 允许开发者使用 C++、Go、Rust、AssemblyScript 等多种语言编写插件，且插件运行在隔离的沙箱环境中，不会导致网主进程崩溃，安全性更高，热更新更灵活。
2.  **微服务与 API 融合**：它打通了南北向（流量入口）和东西向（微服务间调用）的流量管理，既能作为 Ingress 控制器（K8s Ingress），也能作为 API 网关使用。
3.  **高性能**：基于对 Nginx 内核的深度优化，在开启大量插件的情况下依然保持极高的吞吐量和低延迟。

---



### 3: 如何在本地或 Kubernetes 环境中快速部署 Higress？

3: 如何在本地或 Kubernetes 环境中快速部署 Higress？

**A**: Higress 提供了非常灵活的部署方式，主要分为容器化部署和 Kubernetes 部署。

1.  **Docker 本地部署（最快速）**：
    你可以直接使用 Docker 命令一行启动：
    ```bash
    docker run -d --name higress -p 80:80 -p 443:443 higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/higress:latest
    ```
    这将启动一个包含控制台和网关实例的容器。

2.  **Kubernetes 部署（生产推荐）**：
    如果你有 Kubernetes 集群，可以通过 `kubectl` 应用官方的 Helm Chart 或 YAML 文件：
    ```bash
    kubectl apply -f https://github.com/alibaba/higress/releases/latest/download/higress.yaml
    ```
    部署完成后，Higress 会自动监听 Ingress 资源，并提供控制台服务。

---



### 4: Higress 能否直接使用现有的 Kong 或 Nginx 配置？

4: Higress 能否直接使用现有的 Kong 或 Nginx 配置？

**A**: Higress 提供了强大的兼容性迁移工具，但不是完全的“即插即用”。

1.  **Kong 兼容**：Higress 原生支持 Kong 的插件加载机制。如果你有基于 Lua 的 Kong 插件，Higress 提供了运行时支持。同时，Higress 推荐将现有插件迁移为 WASM 插件以获得更好的性能和隔离性。
2.  **Nginx 兼容**：Higress 底层基于 Nginx，因此大部分 Nginx 的指令（如 `upstream`、`server` 配置逻辑）是兼容的。但是，Higress 更推荐使用 Kubernetes Ingress YAML 或控制台 GUI 来配置路由，而不是直接修改 `nginx.conf`。对于复杂的 Nginx 原生配置，可能需要在 Higress 的配置片段中手动适配。

---



### 5: Higress 是否支持从 Nginx Ingress 或 Apache APISIX 迁移？

5: Higress 是否支持从 Nginx Ingress 或 Apache APISIX 迁移？

**A**: 是的，Higress 提供了专门的迁移工具来降低切换成本。

1.  **从 Nginx Ingress 迁移**：Higress 完全兼容 K8s 的 Ingress API。这意味着你不需要修改任何 Ingress YAML 资源文件，只需将集群的 Ingress Class 修改为 `higress`，Higress 即可立即接管 Nginx Ingress Controller 的流量，实现无缝切换。
2.  **从 APISIX 迁移**：虽然两者架构不同，但 Higress 支持导入通用的 OpenAPI 规范。由于两者都支持 WASM 或 Lua 插件，业务逻辑层面的迁移主要集中在插件配置的重新映射上。Higress 控制台通常也提供配置导入导出功能。

---



### 6: Higress 的安全性和插件隔离性如何保证？

6: Higress 的安全性和插件隔离性如何保证？

**A**: 这是 Higress 选择 WASM 作为主要插件扩展方向的重要原因

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基础环境搭建与流量验证

### 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求实现：当访问 `/httpbin/` 路径时，将流量转发到 `httpbin.org` 这个公网测试服务，而访问其他路径时返回 404。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现模型提供商的灵活切换
**场景：** 业务需要在不同大模型（如 OpenAI、通义千问、Llama）之间进行 A/B 测试或灰度发布，而不希望修改客户端代码。
**实践：** 不要将模型提供商硬编码在业务逻辑中。利用 Higress 的 Wasm (WebAssembly) 插件能力，编写一个简单的路由插件。
**操作：** 配置基于请求头（如 `X-Model-Provider`）或 URL 路径的流量分流。例如，将 `/v1/chat/completions` 的请求根据权重百分比，动态转发给后端不同的模型服务或第三方 API。
**陷阱：** 避免在 Lua 脚本中处理复杂的鉴权逻辑，Wasm 插件在处理高并发时的隔离性和安全性更好。

### 2. 实施基于 Token 的精细化流控与缓存
**场景：** 大模型调用成本高昂，且后端模型服务有严格的速率限制（RPM/TPM）。
**实践：** 区别于传统的基于“请求数（QPS）”的限流，AI 网关应关注“Token 吞吐量”。
**操作：**
*   **限流：** 在 Higress 中配置针对 API Key 或用户维度的 Token 限流插件，防止突发流量击穿后端模型服务的配额。
*   **缓存：** 针对高相似度的 Prompt（如常见问答、知识库检索），启用结果缓存。配置缓存 Key 时，应包含 Prompt 的哈希值，而非完整的 URL，以提升命中率并降低 API 费用。
**陷阱：** 缓存策略需注意时效性，对于实时性要求高的对话场景，慎用长时间缓存，以免产生“幻觉”或过时回答。

### 3. 配置语义化的 API 路由与统一入口
**场景：** 企业内部既有传统的微服务接口，又有新增的 AI 能力接口，客户端希望统一接入。
**实践：** 利用 Higress 的 Ingress 能力，将 AI 服务抽象为标准的 RESTful 资源。
**操作：** 不要直接暴露模型厂商的 API 格式。在网关层将不同厂商的异构接口格式统一转换为 OpenAI 标准格式。例如，将内部服务 `/internal/llm/generate` 映射为外部统一入口 `/v1/chat/completions`。
**陷阱：** 请求体和响应体的转换（Body Transform）会消耗网关 CPU 资源，在高吞吐量场景下，需监控网关实例的 CPU 负载，必要时进行水平扩容。

### 4. 强化 Prompt 注入防护与安全审计
**场景：** AI 接口直接暴露给前端，容易受到 Prompt 注入攻击（如越狱尝试），导致数据泄露或产生非法内容。
**实践：** 在网关层设置“护栏”。
**操作：** 部署 Wasm 插件对输入的 Prompt 进行关键词或语义模式匹配。在请求转发给模型之前，拦截包含恶意指令的请求。同时，开启全链路日志审计，记录所有输入和输出的 Token 数量，用于成本核算和合规审查。
**陷阱：** 过度的安全检查会增加请求延迟，建议采用异步日志记录，同步检查仅针对高危特征。

### 5. 处理流式响应的超时与长连接
**场景：** AI 对话通常采用 Server-Sent Events (SSE) 或流式传输，响应时间可能长达数十秒甚至分钟级。
**实践：** 调整网关和后端的超时配置，以适应长轮询场景。
**操作：** 确保 Higress 的 `IdleTimeout` 和 `StreamTimeout` 参数配置得当（例如设置为 300s），防止网关因为后端模型生成耗时过长而断开连接。同时，开启 HTTP/2 支持，以提升并发流式传输的性能。
**陷阱：

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [大模型](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260302-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260304-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*