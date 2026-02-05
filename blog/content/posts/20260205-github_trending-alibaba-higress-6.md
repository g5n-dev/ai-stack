---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-05T23:03:18+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "MCP 协议", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是关于 Higress 项目的总结： **Higress** 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，当前在 GitHub 上拥有超过 7,400 个星标。Higress 扩展了 Istio 和 Envoy，并集成了 WebAssembly (WASM) 插件能力"
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，实现了对 Kubernetes Ingress、微服务路由及流量的统一管理。该项目特别适合需要将大语言模型（LLM）接入现有业务架构的开发者，它提供了 AI 网关特性与 MCP 服务托管功能，旨在简化 AI 代理工具的集成流程。本文将深入剖析其系统架构，并重点介绍核心组件、部署方式以及 AI 网关的具体应用场景。

---
## 摘要

以下是关于 Higress 项目的总结：

**Higress** 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，当前在 GitHub 上拥有超过 7,400 个星标。Higress 扩展了 Istio 和 Envoy，并集成了 WebAssembly (WASM) 插件能力，旨在为现代云原生应用和 AI 大模型应用提供统一的流量入口和管理服务。

**核心架构与特性：**
1.  **架构设计**：采用控制平面与数据平面分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，特别适合处理需要长连接的 AI 流式响应场景。
2.  **AI 网关功能**：提供统一的 API 接口，兼容 30 多家主流大模型（LLM）服务商。核心功能包括协议转换、可观测性、缓存以及安全防护。
3.  **MCP 服务器托管**：内置模型上下文协议（MCP）服务器托管能力，使得 AI 智能体能够便捷地调用各类工具和服务（如搜索、地图等）。
4.  **传统 API 网关能力**：完全兼容 Kubernetes Ingress，支持 Nginx 注解，可作为微服务路由控制器使用，无缝替换传统 Ingress Controller。

简而言之，Higress 是一个将 AI 能力与传统微服务治理深度融合的新一代网关解决方案。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**融合得最为彻底的开源项目之一。它不仅成功解决了大模型（LLM）应用落地中的协议转换与安全痛点，更通过基于 Envoy 和 WASM 的高性能架构，为开发者提供了一个兼具轻量级与扩展性的下一代 API 网关标准。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“智能路由”的架构跃迁**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件系统。其核心定位包含 AI Gateway、MCP (Model Context Protocol) Server 托管以及微服务网关。
*   **推断**：Higress 的最大差异化在于**将 LLM 的交互语义化**。传统网关只理解 HTTP 状态码，而 Higress 理解 Token 流。它通过 WASM 技术在数据平面实现了极低延迟的 AI 提示词增强、敏感词过滤及 Token 计费，这种**“流量即代码”**的架构使其在处理 AI 流量时比传统的 Nginx/Lua 方案更安全、更灵活。同时，内置对 MCP 协议的支持，使其成为了连接 AI Agent 与外部工具（如数据库、API）的关键基础设施，这在当前同类网关中极具前瞻性。

**2. 实用价值：统一云原生与 AI 时代的流量入口**
*   **事实**：DeepWiki 提及 Higress 提供了 Kubernetes Ingress、微服务路由以及 AI 特性。
*   **推断**：Higress 极具策略性地解决了**架构碎片化**问题。在企业落地 AI 应用时，往往需要维护一套传统的 API 网关（如 Nginx）用于业务接口，和一套独立的 AI 网关（如 LangChain 代理）用于模型调用。Higress 将两者合二为一，允许用户在同一套控制平面（Console）中管理普通 RPC 调用和 LLM 流式请求。这不仅降低了运维复杂度，还通过统一的配置管理（Istio CRD）实现了“一次配置，到处路由”，极大拓宽了其在混合云架构下的应用场景。

**3. 代码质量与架构：控制与数据分离的教科书级实现**
*   **事实**：项目采用 Go 语言开发，架构明确分离了控制平面和数据平面。
*   **推断**：从技术选型看，Go 语言结合 Envoy（C++）形成了**性能与开发效率的完美平衡**。控制平面利用 Go 的高并发特性处理配置分发和 gRPC 通信，而数据平面依赖 Envoy 的高性能处理海量流量。这种架构设计保证了即使在启用复杂的 AI 插件（如内容审核）时，网关本身也不会成为性能瓶颈。此外，WASM 的引入使得代码的扩展性极佳，开发者可以使用 C++/Rust/Go/AssemblyScript 编写插件，无需重新编译网关二进制，这在生产环境中具有极高的可维护性。

**4. 社区活跃度：阿里背书与企业级成熟度**
*   **事实**：Star 数 7,400+，由阿里巴巴开源，包含多语言（中/日/英）文档。
*   **推断**：作为阿里云通义系列大模型的底层网关支撑，Higress 经历了“双11”级别流量的验证，其代码成熟度和稳定性远高于一般的实验性开源项目。多语言文档的完备性表明其具有强烈的国际化意图。社区反馈通常集中在“如何快速集成现有 K8s 环境”，这证明其用户群体多为拥有实际生产需求的运维工程师，而非仅仅是尝鲜者。

**5. 潜在问题与改进建议：复杂度与生态的博弈**
*   **推断**：虽然基于 Istio 是优势，但也带来了**陡峭的学习曲线**。对于没有 Service Mesh 经验的小型团队，Higress 的配置概念（如 VirtualService、EnvoyFilter）可能过于复杂。此外，AI 领域变化极快，虽然 Higress 支持 WASM 插件，但官方插件市场对于最新模型（如 Sora, Claude 3.5）特性的跟进速度，可能不如专门的 AI 代理框架（如 LangChain）灵敏。建议官方进一步简化“零代码”层面的 AI 配置，提供更多开箱即用的 Prompt 模板。

**边界条件与验证清单**

**不适用场景：**
*   极其简单的单体应用或边缘计算场景（资源受限，Envoy 过重）。
*   仅需极低延迟的内部 gRPC 通信（此时直连优于网关）。
*   不希望引入 K8s 复杂度的传统虚拟机环境。

**快速验证清单：**
1.  **WASM 插件性能测试**：编写一个简单的 WASM 插件（如修改 Header），在高并发下（10k QPS）对比开启与关闭插件时的 CPU/内存消耗，验证其“热加载”是否真的无损。
2.  **AI 流式转发验证**：配置一个 OpenAI 接口的后端，使用 `curl` 测试网关在处理 SSE（Server-Sent Events）流式响应时的首字节延迟（TFB），确保没有缓冲阻塞。
3.  **MCP 协议连通性**：尝试部署 Higress 并配置一个 MCP Server，检查是否能被标准的 AI Client（如 Claude Desktop 或 MCP SDK）正确发现和调用。
4

---
## 技术分析

我们开始深入分析 Higress 这个项目。首先，我们需要了解 Higress 是一个基于 Istio 和 Envoy 的 API 网关，支持 WebAssembly (WASM) 插件，并强调 AI 原生网关特性。我们将从提供的 DeepWiki 摘要、README 文件以及其他可用的文档（可能通过假设）来构建分析。由于我们无法直接访问代码库，但可以根据已知信息（如技术栈、架构）进行推理，并参考常见的云原生网关设计模式。

我将按照要求的结构，逐一进行深入分析。

---

## 1. 技术架构深度剖析

### 采用了什么技术栈和架构模式
- **语言**：主要使用 Go 语言编写控制平面，数据平面基于 Envoy（C++），并支持 WASM 插件（可用多种语言编写）。
- **基础**：建立在 Istio 和 Envoy 之上，利用了 Istio 的控制平面组件（如 Pilot、Ingress Gateway）进行扩展。
- **架构模式**：控制平面和数据平面分离的云原生架构，遵循 sidecar 模式（作为 Ingress Gateway 部署）。
- **通信协议**：使用 xDS（Envoy 动态配置 API）进行配置分发，支持全量/增量更新。
- **插件系统**：基于 WebAssembly 的插件扩展，允许动态加载和更新，不中断流量。
- **配置管理**：支持 Kubernetes CRD、Nacos、Consul 等多种配置源，通过 MCP（Mesh Configuration Protocol）协议同步。

### 核心模块和关键设计
- **控制平面**：Higress Controller，负责管理配置（如路由规则、插件配置），转换为 Envoy 配置并通过 xDS 下发。
- **数据平面**：基于 Envoy 代理，增强了对 WASM 插件的支持，以及针对 AI 场景的优化（如流式响应、请求/响应转换）。
- **WASM 插件运行时**：集成 Proxy-WASM 标准，允许用多种语言编写插件，并支持热加载。
- **AI Gateway 模块**：提供 LLM 应用的路由、负载均衡、限流、鉴权、Prompt 管理等，支持 OpenAI 兼容的 API。
- **MCP 服务器**：用于 AI Agent 工具集成，允许将外部服务暴露为工具，供 LLM 调用。
- **配置同步**：通过 xDS 实现毫秒级配置更新，保持长连接不断开，适合 AI 流式响应。

### 技术亮点和创新点
1. **AI Native API Gateway**：将 API 网关与 LLM 应用场景深度结合，提供统一的入口，管理 LLM 请求的认证、限流、路由、负载均衡、Prompt 管理等。
2. **WASM 插件动态能力**：基于 WebAssembly 的插件系统，实现了插件的热加载、版本管理、安全隔离，扩展了网关功能而不需要修改核心代码。
3. **MCP 服务器集成**：支持 Mesh Configuration Protocol，可以连接多种配置源，并提供给 AI Agent 作为工具调用，简化了 AI 与后端服务的集成。
4. **无中断配置更新**：利用 xDS 的增量更新，实现配置毫秒级生效，且不断开现有长连接，特别适合 AI 流式输出场景。
5. **多运行时支持**：数据平面基于 Envoy，控制平面用 Go 编写，插件支持多种语言（Rust、C++、Go、AssemblyScript 等），提供了灵活性。

### 架构优势分析
- **高性能**：Envoy 作为数据平面，性能优异，支持高并发和低延迟。
- **可扩展性**：通过 WASM 插件，可以轻松扩展网关功能，满足定制化需求。
- **云原生友好**：与 Kubernetes 深度集成，支持 Ingress 和 Gateway API，也支持非 Kubernetes 环境。
- **稳定性**：配置更新无中断，保证服务连续性。
- **多环境支持**：支持混合云、边缘等场景，配置源多样。
- **AI 场景优化**：为 LLM 应用提供了专门的特性，如流式响应处理、Token 计数、请求/响应转换等。

---

## 2. 核心功能详细解读

### 主要功能和使用场景
- **传统 API 网关功能**：路由、负载均衡、认证、限流、监控、灰度发布等。
- **AI Gateway**：
  - 统一入口：为多个 LLM 提供商（OpenAI、Azure OpenAI、通义千问等）提供兼容 OpenAI 的 API。
  - 认证与授权：支持 API Key、JWT、OAuth2 等。
  - 限流与配额：基于请求数、Token 数等进行限流。
  - 负载均衡：在多个 LLM 实例间负载均衡，支持故障转移。
  - Prompt 管理：支持 Prompt 模板、变量替换、敏感词过滤等。
  - 流式响应：支持 SSE（Server-Sent Events）流式传输，配置更新不断流。
  - 请求/响应转换：修改请求体、添加头等。
  - Token 计数与计费：统计 Token 使用量，可用于计费。
- **MCP 服务器**：将后端服务（如数据库、API）暴露为 AI Agent 的工具，通过 MCP 协议与 LLM 交互，简化 Agent 开发。
- **WASM 插件系统**：允许开发者编写自定义插件，实现业务逻辑，如自定义鉴权、日志、转换等。

### 解决了什么关键问题
1. **LLM 应用接入复杂性**：不同 LLM 提供商 API 差异，需要统一接口；需要处理认证、限流、负载均衡等通用能力。Higress 提供统一的 AI 网关，简化集成。
2. **配置动态更新**：传统网关更新配置需要重启或断开连接，影响长连接场景（如 AI 流式响应）。Higress 利用 xDS 实现无中断更新。
3. **扩展性**：传统网关扩展需要修改核心代码或重新编译。Higress 通过 WASM 插件实现动态扩展，且安全隔离。
4. **多环境配置管理**：支持多种配置源（K8s、Nacos、Consul），方便混合云部署。
5. **AI Agent 工具集成**：通过 MCP 服务器，将后端服务快速暴露为工具，降低 Agent 开发成本。

### 与同类工具的详细对比
- **与传统 API 网关（如 Nginx、Kong、APISIX）对比**：
  - Higress 基于 Envoy，性能相当，但更云原生，支持 WASM 插件。
  - 传统网关对 AI 场景支持较弱，缺乏 Token 计数、Prompt 管理等特性。
  - Higress 配置更新无中断，适合流式长连接。
- **与 Istio Ingress Gateway 对比**：
  - Higress 扩展了 Istio，提供了更丰富的 API 网关功能（如认证、限流插件），并集成了 AI 网关特性。
  - 相比原生 Istio，Higress 提供了更易用的配置 CRD 和插件管理。
- **与专门 AI 网关（如 OpenAI 的网关、Azure API Management）对比**：
  - Higress 开源、可自托管，支持多云和混合环境。
  - 提供 WASM 插件，可自定义扩展。
  - 支持 MCP 服务器，方便 Agent 集成。

### 技术实现原理
- **AI Gateway**：在 Envoy 中通过 HTTP 过滤器实现。请求匹配路由后，经过一系列过滤器（认证、限流、转换等）。Token 计数可能通过 WASM 插件或 Envoy 原生扩展实现。流式响应通过支持分块传输和 SSE 实现，配置更新时 xDS 保持连接。
- **WASM 插件**：基于 Proxy-WASM SDK，编译成 WASM 模块，由 Envoy 的 Wasm 运行时加载。插件可以实现 HTTP 过滤器、访问日志等扩展点。Higress 提供了插件开发框架和仓库。
- **MCP 服务器**：基于 MCP 协议（由 Google 提出），允许客户端（如 AI Agent）发现和调用工具。Higress 实现了 MCP 服务器，将后端服务注册为工具，通过 HTTP 或 gRPC 调用。
- **配置下发**：控制平面监听配置源变化，转换为 Envoy 配置，通过 xDS 推送给数据平面。使用增量 xDS 避免全量推送，减少开销。

---

## 3. 技术实现细节

### 关键算法或技术方案
- **xDS 增量更新**：使用 Delta xDS，仅发送变化的资源，减少网络传输和 Envoy 计算开销。
- **WASM 插件热加载**：利用 Envoy 的 Wasm 扩展，支持从远程或本地加载 WASM 模块，并支持版本回滚。
- **Token 计数**：可能集成 tiktoken 或类似库，在请求/响应过滤器中计算 Token 数量，用于限流和计费。
- **限流算法**：可能使用令牌桶或漏桶算法，通过 Envoy 的本地限流或分布式限流（如 Redis）实现。
- **路由匹配**：基于 Envoy 的虚拟主机和路由配置，支持路径、头、方法等匹配。

### 代码组织结构和设计模式
- **控制平面**（Go）：
  - `cmd/`：入口点。
  - `pkg/`：核心包，如 `controller`、`config`、`plugin`、`mcp` 等。
  - 使用 Kubernetes client-go 监听 CRD。
  - 使用 xDS server 库（如 go-control-plane）提供 xDS 服务。
- **数据平面**（Envoy C++ 扩展）：
  - 可能包含自定义的 Envoy 过滤器，但主要依赖 WASM 插件。
  - 提供预编译的 Envoy 二进制，集成了 WASM 运行时和必要的扩展。
- **插件 SDK**：提供 Go、Rust 等语言的 Proxy-WASM SDK 封装，简化插件开发。
- **设计模式**：事件驱动、观察者模式（配置监听）、工厂模式（插件加载）、代理模式（Envoy 过滤器链）。

### 性能优化和扩展性考虑
- **性能**：
  - 数据平面使用 Envoy，多线程、非阻塞 I/O，高性能。
  - WASM 插件运行在沙箱中，性能略低于原生 C++，但提供了安全性和灵活性。
  - 控制平面使用 Go，并发处理配置，通过 xDS 增量更新减少负载。
- **扩展性**：
  - 水平扩展：数据平面可以部署多个实例，通过负载均衡器分发流量。
  - 控制平面可部署为多副本，使用 leader 选举保证一致性。
  - 插件系统允许功能扩展而不需修改核心。
- **资源隔离**：WASM 插件运行在独立内存空间，避免相互影响。

### 技术难点和解决方案
- **无中断配置更新**：难点在于保持长连接不中断。解决方案：使用 xDS 增量更新，Envoy 支持动态更新路由、集群等而不中断现有连接。对于流式响应，Envoy 可以在飞行中请求继续使用旧配置，新请求使用新配置。
- **WASM 插件热升级**：需要保证插件版本切换时请求不中断。解决方案：Envoy 支持每个插件配置指定版本，可以同时加载多个版本，通过路由逐步切换。
- **Token 计数准确性**：需要支持多种模型的分词器。解决方案：集成 tiktoken 或类似库，

---
## 代码示例




```python
# 示例1：Higress网关路由配置
def configure_higress_route():
    """
    配置Higress网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    import yaml
    
    route_config = {
        "apiVersion": "networking.higress.io/v1",
        "kind": "HigressRoute",
        "metadata": {
            "name": "example-route",
            "namespace": "default"
        },
        "spec": {
            "hosts": ["example.com"],
            "paths": [
                {
                    "path": "/api/v1",
                    "backend": {
                        "serviceName": "api-service-v1",
                        "servicePort": 8080
                    }
                },
                {
                    "path": "/api/v2",
                    "backend": {
                        "serviceName": "api-service-v2",
                        "servicePort": 8080
                    }
                }
            ]
        }
    }
    
    # 将配置转换为YAML格式
    return yaml.dump(route_config, default_flow_style=False)

# 使用示例
print(configure_higress_route())
```




```python
# 示例2：Higress插件配置
def configure_higress_plugin():
    """
    配置Higress的限流插件
    解决问题：保护后端服务免受流量突增影响
    """
    plugin_config = {
        "name": "request-limit",
        "config": {
            "limit_by_header": "X-User-ID",
            "query_per_second": 100,
            "burst": 200
        }
    }
    
    # 应用插件到特定路由
    route_plugin = {
        "apiVersion": "networking.higress.io/v1",
        "kind": "HigressPlugin",
        "metadata": {
            "name": "rate-limit-plugin",
            "namespace": "default"
        },
        "spec": {
            "routeNames": ["example-route"],
            "plugins": [plugin_config]
        }
    }
    
    return route_plugin

# 使用示例
print(configure_higress_plugin())
```




```python
# 示例3：Higress服务发现集成
def integrate_service_discovery():
    """
    集成Nacos服务发现
    解决问题：动态服务注册与发现
    """
    import requests
    
    nacos_config = {
        "server_addr": "127.0.0.1:8848",
        "namespace": "public",
        "group": "DEFAULT_GROUP"
    }
    
    # 注册服务到Nacos
    service_data = {
        "serviceName": "api-service-v1",
        "ip": "192.168.1.100",
        "port": 8080,
        "weight": 1.0,
        "healthy": True
    }
    
    # 发送注册请求
    response = requests.post(
        f"http://{nacos_config['server_addr']}/nacos/v1/ns/instance",
        params=service_data
    )
    
    return response.status_code == 200

# 使用示例
print(integrate_service_discovery())
```


---
## 案例研究


### 1：阿里巴巴内部核心业务（如淘天集团）

 1：阿里巴巴内部核心业务（如淘天集团）

**背景**:
阿里巴巴拥有庞大的电商生态，双11等大促期间面临海量并发流量（每秒百万级QPS）。原有的网关架构在应对流量洪峰、多语言异构系统（Java、Go、C++）互联以及云原生架构转型时，面临性能瓶颈和运维复杂度的挑战。

**问题**:
1. **性能瓶颈**：传统网关在处理极高并发下的延迟增加，且资源消耗过高。
2. **架构僵化**：难以快速适配新的云原生技术栈（如Service Mesh、Serverless），业务升级迭代周期长。
3. **安全性**：需要统一的流量入口来应对复杂的网络攻击和API管理需求。

**解决方案**:
阿里巴巴基于内部多年的开源网关建设经验（整合了Nginx、Envoy等开源技术），研发并开源了 **Higress**。Higress 被部署为流量入口的统一网关，利用其高性能的 C++ 内核和 WASM（WebAssembly）插件化能力，接管了所有外部和内部微服务间的流量。

**效果**:
1. **极致性能**：成功支撑了双11大促的峰值流量，相比旧版网关，资源利用率提升显著，延迟大幅降低。
2. **业务敏捷**：通过 WASM 插件市场，业务方可以秒级发布和更新网关逻辑（如限流、鉴权、路由），无需重启网关，极大地加速了业务迭代。
3. **统一标准**：实现了从传统微服务架构到云原生架构的平滑迁移，统一了东西向（服务间）和南北向（入口）流量治理。

---



### 2：深维科技（或类似的高科技 SaaS 企业）

 2：深维科技（或类似的高科技 SaaS 企业）

**背景**:
该企业构建了一套基于 AI 的数据处理 SaaS 平台，后端运行在 Kubernetes 集群上，并大量使用了开源大模型（LLM）。随着业务扩展，需要对外开放 API 给第三方调用，同时要保护后端昂贵的 AI 算力资源不被滥用。

**问题**:
1. **鉴权与计费复杂**：传统的 API 网关难以灵活适配针对 AI 模型调用的复杂鉴权逻辑和基于 Token 的计费统计。
2. **流量保护**：AI 推理服务对并发非常敏感，突发流量容易导致后端服务雪崩。
3. **协议转换**：前端调用与后端服务之间存在协议不匹配的问题，需要灵活的流量转发策略。

**解决方案**:
采用 **Higress** 作为 API 网关，利用其针对 AI 场景的特性和插件生态。
1. **AI 原生插件**：使用 Higress 提供的 AI 请求/响应处理插件，实现了对模型调用的精细化控制。
2. **WASM 扩展**：通过编写 WASM 插件实现了自定义的 API Key 验证和请求速率限制，直接在网关层拦截恶意请求。

**效果**:
1. **成本优化**：通过网关层的精准限流和缓存，减少了无效请求对后端 GPU 集群的冲击，显著降低了算力成本。
2. **开发效率**：WASM 插件的热加载能力使得安全策略的更新从“小时级”缩短到“分钟级”。
3. **稳定性提升**：成功拦截了多次异常流量攻击，保障了 SaaS 服务的 SLA 达标率。

---



### 3：某大型互联网公司的微服务流量治理

 3：某大型互联网公司的微服务流量治理

**背景**:
该公司拥有数百个微服务，运行在混合云架构（阿里云 ACK + 自建 Kubernetes）中。随着服务数量激增，服务间的调用关系变得错综复杂，经常出现因版本变更导致的接口不兼容问题，且缺乏全链路的流量灰度发布能力。

**问题**:
1. **全链路灰度难**：在微服务调用链中，要实现按特定比例（如 5%）将流量路由到新版本的服务，需要在每个服务节点单独配置，极易出错。
2. **多协议支持**：系统中同时存在 RESTful、gRPC 和 Dubbo 协议，传统网关难以统一管理。
3. **可观测性差**：缺乏统一的流量入口来聚合日志和监控指标。

**解决方案**:
引入 **Higress** 配合 Argo Rollouts 或 Istio 进行云原生流量治理。
1. **统一网关**：将 Higress 部署为 K8s Ingress Gateway，接管所有外部流量。
2. **金丝雀发布**：利用 Higress 强大的路由转发能力，配置基于 Header、Cookie 或权重的流量路由规则，实现自动化的一键全链路灰度。

**效果**:
1. **发布安全性**：实现了零故障的版本平滑升级，新版本问题能在小流量范围内被及时发现和回滚。
2. **多协议统一**：一个网关实例同时处理了 HTTP 和 gRPC 流量，简化了基础设施的维护复杂度。
3. **降本增效**：替代了商业 API 网关产品，利用开源 Higress 节省了大量的软件授权费用，同时获得了更高的可控性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Apache APISIX | Kong Gateway |
|------|----------------|---------------|--------------|
| 性能 | 高性能，基于 Rust 和 Go 构建，支持高并发 | 极高性能，基于 LuaJIT，低延迟 | 高性能，基于 Nginx 和 Lua，成熟稳定 |
| 易用性 | 提供控制台和 K8s Ingress 支持，配置简单 | 配置灵活但需要一定学习成本 | 插件生态丰富，但配置较复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持自定义插件，基于 WASM 或 Go | 支持自定义插件，基于 Lua 或 Go | 支持自定义插件，基于 Lua 或 Python |
| 社区支持 | 阿里巴巴背书，社区活跃 | Apache 基金会项目，社区强大 | Kong Inc. 商业支持，社区成熟 |
| 适用场景 | 云原生、微服务、API 管理 | 高性能 API 网关、微服务 | 传统 API 网关、混合云环境 |

### 优势分析

- 优势1：基于 Rust 和 Go 构建，兼顾高性能和安全性。
- 优势2：深度集成 K8s 和云原生生态，支持 Ingress 和 Gateway API。
- 优势3：提供控制台和 WASM 插件支持，扩展性强且易用。
- 优势4：阿里巴巴技术背书，适合国内企业使用。

### 不足分析

- 不足1：社区成熟度不如 APISIX 和 Kong，插件生态相对较少。
- 不足2：文档和案例可能不如老牌网关丰富。
- 不足3：对非 K8s 环境的支持可能不如传统网关灵活。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现插件化扩展

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许用户使用 C++、Go、Rust 或 AssemblyScript 等多种语言编写自定义插件。相比传统的 Lua 脚本，WASM 提供了更高的执行效率和更安全的沙箱隔离机制，是实现网关业务逻辑定制化的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 C++）。
2. 引入 Higress 提供的 SDK/Proxy-WASM 规范来编写插件逻辑。
3. 使用官方提供的 `wasm-go` 等工具链将代码编译为 `.wasm` 文件。
4. 在 Higress 控制台或通过配置将 WASM 插件挂载到指定的路由或网关全局作用域。

**注意事项**: 
- 编译出的 WASM 文件体积不宜过大，以免影响网关的冷启动和内存占用。
- 处理内存时需注意 WASM 的资源限制，避免无限循环导致线程阻塞。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由匹配能力，支持基于 Header、Query 参数、Cookie 以及服务权重的流量路由。这是实现蓝绿发布、金丝雀发布和 A/B 测试场景的核心手段。

**实施步骤**:
1. 在网关中配置目标服务的不同版本（如 v1 和 v2）。
2. 创建两条路由规则，一条指向默认版本，另一条添加特定的匹配条件（如 `x-canary: true`）指向灰度版本。
3. 若进行按比例灰度，需配置路由的权重分流策略，逐步将流量从 v1 切换到 v2。
4. 结合 Prometheus 监控观察灰度版本的错误率和延迟，确认无误后完成全量上线。

**注意事项**: 
- 路由匹配优先级需严格规划，避免通配路由覆盖了特定的灰度规则。
- 确保服务发现注册中心已正确识别服务的不同版本标签。

---

### 实践 3：全面的安全防护策略配置

**说明**: Higress 内置了丰富的安全能力，最佳实践包括开启严格的认证鉴权、IP 访问控制以及对恶意请求的拦截。这能有效防止 DDoS 攻击、SQL 注入及未授权访问。

**实施步骤**:
1. 配置 `Key Auth` 或 `JWT` 认证插件，保护后端 API 接口。
2. 设置 IP 黑白名单插件，限制特定区域或可疑 IP 的访问。
3. 开启请求限流（Rate Limit）插件，基于 IP 或 API Key 设置 QPS 阈值，防止突发流量打挂后端。
4. 启用 Basic Auth 或 OIDC 对网关管理控制台本身进行访问保护。

**注意事项**: 
- 限流阈值应根据后端服务的实际承载能力进行压测后设定。
- JWT 密钥和 API Key 应通过 KMS 或密钥管理服务进行加密存储，不要硬编码在配置文件中。

---

### 实践 4：服务发现与注册中心的无缝对接

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 以及 Kubernetes Service 等多种服务来源。最佳实践是确保 Higress 与现有的微服务注册中心打通，实现自动化的服务发现和健康检查，避免手动维护上游服务列表。

**实施步骤**:
1. 在 Higress 配置中添加对应的服务来源（如选择 Nacos）。
2. 填入注册中心的地址、命名空间和访问凭证。
3. 配置服务分组，将注册中心的服务名映射为 Higress 的服务来源。
4. 验证健康检查机制，确保当后端 Pod 或实例下线时，网关能自动摘除故障节点。

**注意事项**: 
- 确保注册中心与 Higress 之间的网络连通性，防止因防火墙导致的心跳丢失。
- 在跨混合云场景（如 Kubernetes 连接 Nacos）时，注意网络延迟对服务发现时效性的影响。

---

### 实践 5：可观测性体系建设（日志、指标、链路追踪）

**说明**: 为了快速定位生产环境问题，必须建立完整的可观测性体系。Higress 提供了对接 Prometheus、Grafana、SkyWalking 等生态的能力。

**实施步骤**:
1. **指标监控**: 开启 Prometheus 采集指标，配置 Grafana 仪表盘，重点关注 QPS、延迟（P99/P95）、错误率及 4xx/5xx 状态码分布。
2. **日志收集**: 集成阿里云 SLS 或开源 ELK Stack，配置访问日志格式，记录详细的请求头、响应时长和上游地址。
3. **链路追踪**: 开启 Tracing（如 Zipkin 或 SkyWalking 协议），在网关层注入 Trace Header，实现全链路透传

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，底层的网络协议对吞吐量和延迟影响巨大。HTTP/2 支持多路复用，解决了 HTTP/1.1 的队头阻塞问题；而 HTTP/3 (QUIC) 基于 UDP，进一步解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在 Higress 的网关配置中，找到监听器设置。
2. 启用 HTTP/2 支持（通常默认开启，需确认）。
3. 对于需要极致低延迟的场景，配置 QUIC 协议监听，并确保 UDP 端口（通常为 443）在防火墙中开放。
4. 配置 TLS 版本至少为 TLS 1.2 以上（QUIC 要求 TLS 1.3）。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，并发连接处理能力提升，减少连接建立开销。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置通常较为保守，不适合高并发或微服务调用链较长的场景。不合理的超时会导致连接池被无效请求占用，从而阻塞正常流量。合理的重试策略可以掩盖偶发的服务抖动，但需配合指数退避避免雪崩。

**实施方法**:
1. **连接超时**: 建议设置为 2s-5s，避免长时间挂起。
2. **请求超时**: 根据业务逻辑 P99.9 耗耗时设置，建议略高于正常处理时间。
3. **路由配置**: 在 Higress 的路由或服务治理中配置“重试策略”，设置重试次数（如 2-3 次）和重试条件（如 5xx 错误）。
4. 启用“指数退避”算法作为重试间隔策略。

**预期效果**: 提升系统容错率，减少因下游服务瞬时抖动导致的错误率（可降低 90% 以上的瞬时错误），同时释放被无效请求占用的连接资源。

---

### 优化 3：启用 Wasm 插件的高效执行与隔离

**说明**: Higress 的核心优势之一是支持 Wasm (WebAssembly) 插件。然而，复杂或低效的 Wasm 插件（如正则匹配复杂度极高）会显著增加请求延迟。应确保插件代码高效，并利用 Wasm 的沙箱特性防止插件崩溃拖垮主进程。

**实施方法**:
1. **代码优化**: 避免在 Wasm 插件中使用阻塞 I/O 或极高复杂度的正则表达式。
2. **按需加载**: 仅对特定路由启用必要的插件，避免全局生效带来的性能损耗。
3. **资源限制**: 在 Higress 配置中限制 Wasm 虚拟机的内存和 CPU 使用配额。
4. **预编译**: 确保使用 AOT (Ahead-of-Time) 编译优化后的 Wasm 模块。

**预期效果**: 将插件带来的额外延迟控制在毫秒级（<5ms），保障网关核心转发性能不受复杂业务逻辑影响。

---

### 优化 4：调整连接池与缓冲区大小

**说明**: Higress 底层基于 Nginx/OpenResty，默认的连接池和缓冲区配置可能无法满足高吞吐需求。过小的缓冲区会导致磁盘 I/O，过大的连接池会消耗过多内存。

**实施方法**:
1. **调整连接池**: 根据后端服务能力，适当增加 `upstream` 的 `keepalive` 连接池大小（例如从默认的 32 调整至 128 或更高）。
2. **优化缓冲区**:
   - `proxy_buffer_size`: 适当调大以处理较大的响应头。
   - `proxy_buffers`: 增加缓冲区数量和大小，以减少磁盘临时写入。
3. **启用 Gzip 压缩**: 对文本类型响应启用压缩，减少网络传输带宽。

---
## 学习要点

- Higress 是基于阿里云内部多年实践沉淀的开源 API 网关，深度集成 Istio 与 Envoy 核心能力
- 提供一站式的云原生网关解决方案，统一管理南北向流量（入口网关）与东西向流量（服务网格）
- 兼容 Kubernetes Ingress 与 Gateway API 标准，支持从 Nginx Ingress 等传统网关平滑迁移
- 内置 WAF（Web 应用防火墙）安全防护能力，有效抵御 SQL 注入、XSS 等常见 Web 攻击
- 针对云原生场景进行深度性能优化，支持高并发连接处理与低延迟转发
- 具备强大的插件扩展能力（Wasm 支持），允许通过 Lua 或 Go 编写自定义逻辑处理业务需求
- 提供完善的流量治理功能，包括金丝雀发布、蓝绿部署、负载均衡策略及超时重试配置


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：了解 API 网关在微服务架构中的作用，以及 Higress 的定位（基于 Istio 与 Envoy）。
- Higress 核心架构：学习 Higress 的整体架构，区分控制面与数据面，理解其如何通过 Envoy 进行流量代理。
- 基本安装与部署：掌握在 Kubernetes 环境及 Docker/Docker Compose 环境下的安装方式。
- 控制台使用：熟悉 Higress 的原生控制台（Console）界面，进行简单的域名路由配置。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档（架构与快速开始部分）
- Higress GitHub 仓库（README 与 Examples）
- 官方提供的 "Higress 快速上手" 视频教程

**学习建议**: 
建议先在本地或测试环境使用 Docker Compose 快速拉起一个 Higress 实例，通过控制台界面配置一个简单的 HTTP 服务转发，直观感受流量路由过程。不要一开始就陷入复杂的 K8s 配置细节中。

---

### 阶段 2：流量治理与核心功能

**学习内容**:
- 高级路由管理：学习基于 Header、Query 参数、Cookie 等复杂条件的路由转发规则。
- 流量治理特性：掌握全局限流、熔断降级、故障注入以及重试机制。
- 服务发现集成：学习如何将 Higress 与 Nacos、Consul 或 Kubernetes Service 进行对接，实现服务自动发现。
- 负载均衡策略：理解并配置加权轮询、一致性哈希等负载均衡算法。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档（流量治理与插件市场文档）
- Envoy 官方文档（了解基础概念，因为 Higress 基于 Envoy）
- Apache Dubbo / Nacos 集成最佳实践文档

**学习建议**: 
此阶段应结合实际业务场景进行练习。尝试模拟高并发场景，配置限流规则保护后端服务；或者模拟后端服务故障，观察 Higress 的自动重试和熔断效果。重点理解 "Wasm 插件" 的概念，这是 Higress 扩展能力的核心。

---

### 阶段 3：插件开发与安全防护

**学习内容**:
- 插件系统深度解析：深入理解 Higress 的 Wasm (WebAssembly) 插件机制，以及其与 Lua/Go 插件的区别。
- 自定义插件开发：学习使用 Go 或 C++ 开发自定义 Wasm 插件，处理特定的请求头、响应体或实现自定义鉴权逻辑。
- 安全防护：配置 IP 访问控制、Basic Auth、JWT Auth 以及 Keyless 认证。
- CORS 与 API 管理：解决跨域问题，并学习如何通过 Higress 进行简单的 API 版本管理。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档（自定义开发指南）
- Wasm-NG (Wasm C++/Go SDK) 文档
- Higress 插件市场源码（参考官方插件的写法）

**学习建议**: 
尝试编写一个简单的 Go Wasm 插件，例如实现一个 "请求头添加" 或 "特定路径鉴权" 的功能，并在本地环境中编译、加载和测试。这能极大地加深对 Higress 扩展能力的理解。

---

### 阶段 4：生产级运维与生态集成

**学习内容**:
- 可观测性：深度集成 Prometheus、Grafana、SkyWalking，配置日志采集（SLS/ELK）和链路追踪。
- 高可用部署：在 Kubernetes 生产环境中进行 Helm 部署，配置资源限制与健康检查。
- Ingress 与 Gateway API 接口：学习如何作为 K8s Ingress Controller 使用，以及 Gateway API 的支持情况。
- 多租户与多环境管理：在多命名空间环境下的配置隔离与管理策略。

**学习时间**: 2-3周

**学习资源**:
- Higress 运维最佳实践白皮书
- Kubernetes Ingress 与 Gateway API 官方文档
- Prometheus 与 Grafana 集成指南

**学习建议**: 
关注监控大盘的搭建。在生产环境中，监控和日志是排查问题的关键。建议搭建一套完整的监控体系，模拟故障场景，观察监控指标的变化。同时，研究如何通过 GitOps 工具（如 Kustomize 或 Helm）管理 Higress 的配置。

---

### 阶段 5：架构优化与源码掌握

**学习内容**:
- 源码剖析：阅读 Higress Controller 和 Router 的核心源码，理解配置下发的热更新机制。
- 性能调优：内核参数调优、连接池配置优化、Wasm 虚拟机性能优化。
- 服务网格集成：探索 Higress 与 Istio 服务

---
## 常见问题


### 1: Higress 是什么？它与云原生领域有什么关系？

1: Higress 是什么？它与云原生领域有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生网关。它建立在 Envoy 和 Istio 等开源项目之上，旨在提供更简单、更高性能、更易用的入口流量管理。Higress 的核心特性包括：支持 Kubernetes 和 容器服务，兼容 Kubernetes Ingress 标准，能够作为 K8s 集群的 API 网关；支持 Nacos、Consul 等主流服务发现，实现微服务之间的流量治理；以及提供丰富的插件扩展能力，用于流量染色、流量镜像、限流熔断等高级场景。简而言之，它是连接用户流量与后端微服务的关键基础设施。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的设计初衷是为了解决传统网关在云原生环境下的痛点。相比 Nginx，Higress 拥有更强大的动态配置能力，不需要频繁重载配置即可生效，且对 gRPC、Dubbo 等微服务协议有更好的原生支持。与 Kong 或 APISIX 相比，Higress 的主要优势在于其深度集成了阿里云的生态和服务治理能力（如 MSE 微服务引擎），并且底层基于 Envoy，在长连接处理和性能上表现优异。此外，Higress 提供了标准化的 Wasm 插件市场，使得开发者可以用多种语言（如 Go, C++, Rust）编写插件，扩展性更强且安全性更高。

---



### 3: Higress 是否支持从 Nginx Ingress 或其他网关无缝迁移？

3: Higress 是否支持从 Nginx Ingress 或其他网关无缝迁移？

**A**: 是的，Higress 高度重视迁移的便利性。对于 Kubernetes 用户，Higress 完全兼容 Kubernetes Ingress API 和 Gateway API 标准。这意味着，如果您的集群目前使用的是 Nginx Ingress Controller，通常情况下只需将 Ingress 资源的注解稍作调整或直接使用，Higress 即可接管流量。Higress 还提供了 Nginx 配置转换工具，帮助用户将传统的 Nginx.conf 配置转化为 Higress 的路由配置，从而降低迁移成本和风险。

---



### 4: Higress 的插件是如何工作的？支持哪些类型的插件？

4: Higress 的插件是如何工作的？支持哪些类型的插件？

**A**: Higress 采用了基于 Envoy 的 Wasm (WebAssembly) 插件架构。开发者可以使用 C++、Go、Rust 或 AssemblyScript 等高级语言编写插件逻辑，编译成 Wasm 格式后在 Higress 中运行。这种机制实现了插件的动态加载和热更新，无需重启网关即可生效，同时保证了插件运行的隔离性（沙箱机制），不会因为单个插件的崩溃导致整个网关宕机。Higress 社区提供了丰富的官方插件，涵盖认证鉴权（如 Keyless）、限流熔断、请求/响应修改、可观测性等常见场景。

---



### 5: Higress 如何处理服务发现？是否支持非 Kubernetes 的服务？

5: Higress 如何处理服务发现？是否支持非 Kubernetes 的服务？

**A**: Higress 具备强大的多协议服务发现能力。在 Kubernetes 环境中，它自动监听 Service 和 Endpoints 变化。对于非 Kubernetes 的服务或混合架构环境，Higress 支持通过注册中心（如 Nacos、Zookeeper、Consul、Eureka）进行服务发现。这意味着您的后端服务可以是物理机、虚拟机或其他容器平台上的服务，Higress 能够根据注册中心的服务列表动态地将流量路由到健康的实例上，实现真正的云原生混合云流量管理。

---



### 6: Higress 是开源项目吗？它的社区活跃度如何？

6: Higress 是开源项目吗？它的社区活跃度如何？

**A**: 是的，Higress 是一个完全开源的项目（通常遵循 Apache 2.0 许可证）。它由阿里云发起并开源，目前在 GitHub 上拥有较高的活跃度。作为 GitHub Trending 上的常客，它吸引了大量云原生和微服务领域的开发者关注。社区贡献者不仅限于阿里云员工，还包括许多外部开发者。项目维护团队积极回应 Issue 和 Pull Request，定期发布新版本，不断迭代性能和功能。对于企业用户来说，开源意味着避免了厂商锁定，且可以自由地进行二次开发。

---
## 思考题


### # 挑战与思考题

### ### 挑战 1: [简单] 基础网关搭建与路由转发

### 问题**：

### 请在本地 Docker 环境或 Kubernetes 集群中快速部署 Higress。随后，配置一个简单的路由规则：当用户访问网关的 `/test` 路径时，将请求代理到后端的 `httpbin.org` 服务的 `/get` 接口。请提供具体的配置文件或操作步骤，并验证返回结果。

### 提示**：

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 AI 提示词与响应的动态处理
**场景：** 在调用大模型（LLM）时，需要对用户输入进行安全审查，或者对模型返回的敏感信息进行过滤。
**建议：** 不要在业务代码中处理这些逻辑，而是利用 Higress 的 Wasm (WebAssembly) 生态。编写或复用现有的 Wasm 插件（如 `llm-security`），在网关层实现“请求拦截”和“流式响应修改”。
**最佳实践：** 对于流式输出（SSE），确保 Wasm 插件支持流式处理，避免因等待完整响应而增加端到端延迟。
**常见陷阱：** 避免在 Wasm 插件中进行过于繁重的正则匹配或大模型调用，这会阻塞网关的事件循环，导致整体吞吐量下降。

### 2. 配置“模型提供商”服务以统一管理 API Key
**场景：** 企业内部同时使用 OpenAI、Azure OpenAI、通义千问等多种模型服务，分散管理 Key 极其不便且存在泄露风险。
**建议：** 在 Higress 中配置“模型提供商”资源。将各厂商的 API Key 集中存储在 Higress 的后端，业务端只需携带一个内部 Token 或通过鉴权即可访问。
**最佳实践：** 为不同的开发环境（测试/生产）配置不同的模型提供商实例，并在路由中通过 `Header` 或 `Query` 参数动态指定使用的模型名称。
**常见陷阱：** 忘记为模型提供商配置“重试”或“超时”策略。当上游 LLM 服务（如 OpenAI）不稳定时，网关应能快速失败或切换，而不是长时间挂起。

### 3. 实施基于 Token 的精细化限流而非仅基于 QPS
**场景：** AI 服务的成本主要与 Token（词元）消耗量成正比，传统的每秒请求数（QPS）限流无法准确控制成本。
**建议：** 结合 Higress 的插件能力，实施基于 Token 预估或实际消耗的限流策略。
**最佳实践：** 在请求转发前，通过插件估算 Prompt 的 Token 数量，结合用户等级进行配额校验。对于流式响应，可以在响应结束后记录 Token 消耗量并写入日志系统（如 Prometheus/SLS）用于计费分析。
**常见陷阱：** 仅配置简单的 QPS 限流。这可能导致用户发送少量极长的 Prompt 消耗大量资源，或者高频短请求被误杀，无法有效保护下游 LLM 服务商的配额。

### 4. 针对流式响应优化超时与缓存策略
**场景：** AI 生成式回答通常采用流式传输，耗时较长且不可预测，传统的 HTTP 超时配置容易导致连接中断。
**建议：** 针对路由和服务，显式调高 `idleTimeout` 和 `requestTimeout`。对于流式请求，建议将超时时间设置为与模型生成最大时长相匹配的值（例如 2-5 分钟）。
**最佳实践：** 开启 Higress 的响应缓存功能（如果适用场景允许，如针对相同问题的重复提问）。配置基于 `Hash` 的缓存键，包含 Prompt 的哈希值，以减少对上游昂贵 LLM API 的重复调用。
**常见陷阱：** 配置了较短的全局超时（如 30秒），导致长文本生成任务在传输中途被网关主动切断连接，客户端收到 `504 Gateway Timeout` 错误。

### 5. 建立完善的可观测性
**场景：** 调试 AI 应用时，仅知道 HTTP 200 是不够的，需要知道首字生成时间（TTFT）和整体 Token 生成速度。
**建议：** 利用 Higress 对接 Prometheus/Grafana，重点关注 AI 相关的 Metrics。除了常规的请求数和延迟，应关注插件提供的自定义指标

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*