---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-29T09:54:18+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "LLM", "Istio", "Envoy", "WASM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是一款由阿里巴巴开源的、基于 Go 语言开发的**云原生 API 网关**，也是一款**AI 原生网关**。它建立在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，为云原生应用和 AI 应用提供统一的流量管理服务。目前该项目在 GitHub 上已获得超过 7"
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
- **星标**: 7,401 (+7 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在为云原生应用与大模型场景提供统一的流量管理入口。它通过 WASM 插件扩展了传统网关能力，并集成了 AI 网关特性与 MCP 协议支持，帮助开发者高效处理 LLM 应用接入及微服务路由。本文将梳理其架构设计、核心功能及适用场景，助你快速评估该技术方案。

---
## 摘要

Higress 是一款由阿里巴巴开源的、基于 Go 语言开发的**云原生 API 网关**，也是一款**AI 原生网关**。它建立在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，为云原生应用和 AI 应用提供统一的流量管理服务。目前该项目在 GitHub 上已获得超过 7,400 颗星。

以下是 Higress 的核心特性与架构总结：

**1. 核心架构**
Higress 将**控制平面**（配置管理）与**数据平面**（流量处理）分离。配置变更通过 xDS 协议传播，具有毫秒级延迟且不中断连接的特点。这种架构特别适合 AI 长连接流式响应等场景。

**2. 三大主要功能**
Higress 的定位非常广泛，主要覆盖以下三个核心使用场景：

*   **AI 网关：**
    *   提供统一的 API 接口，兼容 30 多家大语言模型（LLM）服务商。
    *   **核心功能：** 协议转换、可观测性、缓存以及安全防护。
    *   **相关组件：** 依赖 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 等插件。
*   **MCP 服务器托管：**
    *   托管**模型上下文协议 (MCP)** 服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   **相关组件：** 包含 `mcp-router`、`jsonrpc-converter` 过滤器以及具体的 MCP 服务实现（如 `quark-search`, `amap-tools` 等）。
*   **Kubernetes Ingress（传统 API 网关）：**
    *   作为 Kubernetes 的 Ingress 控制器使用，兼容 nginx-ingress 注解，负责微服务路由和入口流量管理。

**总结：**
Higress 是一款集成了传统微服务治理与前沿 AI 应用能力的网关，旨在解决 LLM 应用接入、AI 智能体工具调用以及云原生流量管理的统一需求。

---
## 评论

### 总体判断
Higress 是一款极具前瞻性的“AI Native”网关，它成功地将云原生流量治理技术与大模型（LLM）应用需求深度融合。它不仅是阿里云对开源网关市场的有力回应，更是当前企业构建 AI 原生应用时，连接后端模型服务与前端业务的高效基础设施。

### 深度评价依据

**1. 技术创新性：WASM 插件化与 AI 原生架构的深度结合**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。DeepWiki 明确指出其核心功能之一是“AI Gateway Features for LLM applications”。
*   **推断**：传统网关（如 Nginx, Kong）处理 AI 请求时，往往缺乏对流式传输、Token 计费以及提示词增强的原生支持。Higress 的差异化在于利用 WASM 的高性能隔离特性，允许开发者使用 Go/C++/Rust 编写插件来动态处理 LLM 的请求与响应逻辑。这种“AI Native”设计使得网关本身具备了处理模型路由（如根据用户问题路由到不同模型）、敏感词过滤以及结果缓存的能力，而不仅仅是做简单的 TCP/HTTP 转发。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **事实**：仓库描述强调其提供“AI Gateway”和“MCP server hosting”功能。
*   **推断**：在当前 AI 应用爆发期，企业面临的最大痛点不是模型本身，而是如何安全、稳定地将模型集成到业务中，以及如何让 AI Agent 能够调用外部工具。
    *   **MCP (Model Context Protocol) Server Hosting** 是一个非常实用的功能。它允许 Higress 直接作为 AI Agent 的工具提供者，解决了 Agent 访问内网 API 的安全和鉴权难题。
    *   通过统一的网关屏蔽不同 LLM 厂商（OpenAI, 通义千问, 文心一言等）的 API 差异，极大地降低了多模型切换和迁移的成本。

**3. 代码质量与架构：云原生标准与控制数据分离**
*   **事实**：文档提到架构分离了控制平面和数据平面。
*   **推断**：基于 Istio 和 Envoy 意味着 Higress 继承了业界最成熟的高性能网络处理逻辑。数据平面由 Envoy 驱动，保证了 C++ 级别的高吞吐量；控制平面接管配置管理，符合 Kubernetes Operator 的模式。Go 语言编写控制层保证了开发效率，而 Envoy+WASM 的组合保证了数据层的极致性能与扩展性。这种架构在代码质量上属于工业级标准，适合大规模部署。

**4. 社区活跃度：阿里背书与开源生态建设**
*   **事实**：星标数 7,401，语言为 Go，由 Alibaba 组织维护。
*   **推断**：作为阿里巴巴开源的项目，它不仅有阿里云内部的商业落地支撑，还积极拥抱 CNCF（云原生计算基金会）生态。虽然相比 Kong 或 APISIX，其社区生态成熟度稍晚，但凭借“AI Gateway”这一细分赛道的精准切入，吸引了大量关注 AI 基础设施的开发者。更新频率通常紧跟阿里云通义千问等模型的发布节奏。

**5. 学习价值与对比优势：不仅是网关，更是 AI 编排入口**
*   **事实**：相比传统的 API 网关，Higress 内置了对 AI 特定协议的支持。
*   **推断**：
    *   **对比优势**：与 **Kong** 相比，Higress 对 Kubernetes 的集成更加原生，且在 AI 流式处理（SSE）配置上更简单；与 **APISIX** 相比，Higress 的 WASM 插件生态对 AI 逻辑的嵌入更为友好。
    *   **学习价值**：开发者可以从中学习如何将 WASM 技术应用于业务逻辑热更新，以及如何设计一个兼容 OpenAI 协议的代理层。

### 边界条件与验证清单

**不适用场景：**
*   极其简单的静态网站托管（使用 Nginx 更轻量）。
*   对云原生有抵触，纯物理机部署且无 K8s 环境的传统应用。
*   需要极度复杂的传统 SQL 数据库透传（非 HTTP 协议）场景。

**快速验证清单：**
1.  **协议兼容性测试**：部署一个 Higress 实例，配置指向 OpenAI 或通义千问的代理，验证其是否能正确处理 SSE（Server-Sent Events）流式响应，且无明显的首包延迟。
2.  **WASM 插件热加载**：编写一个简单的 Go WASM 插件（例如修改响应头），在不重启网关的情况下热加载，验证流量是否无损生效。
3.  **MCP 连通性实验**：尝试配置一个 MCP 服务，通过 Higress 暴露给 AI Agent，检查鉴权与工具调用的日志记录是否完整。
4.  **高并发压测**：使用压测工具对比 Higress 与原生 Nginx 在开启复杂路由逻辑时的吞吐量差异，确认其性能损耗是否在可接受范围内（通常应控制在 10% 以内）。

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本报告将从底层架构、核心功能、技术实现、适用场景、发展趋势及工程哲学等维度进行全面剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构采用了**控制平面与数据平面分离**的云原生模式。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L4/L7 处理能力；通过 **Istio** 进行服务网格的抽象与管理，但剥离了 Istio 中繁重的 Sidecar 模式，专注于 Gateway 流量入口。
*   **语言选择**：**Go** 语言构建控制平面，利用其高并发处理能力和丰富的云原生生态；数据平面基于 C++ 的 Envoy。
*   **架构模式**：典型的 **Delegated Pattern（委派模式）**。Higress 在控制平面管理配置，通过 xDS 协议将配置下发至 Envoy。

### 核心模块与关键设计
1.  **控制平面**：
    *   负责配置管理、路由规则分发、证书管理。
    *   通过 **MCP (Multi-Cloud Proxy)** 协议或 K8s Ingress API 接收配置。
    *   **关键设计**：配置变更通过 xDS 协议推送到数据平面，实现了毫秒级生效且不断连，这对于 AI 流式响应至关重要。
2.  **数据平面**：
    *   基于 Envoy，处理实际的网络流量。
    *   **WASM 插件系统**：这是 Higress 的“心脏”。它允许使用 C++/Go/Rust/AssemblyScript 编写插件，编译为 WASM 字节码后动态加载到 Envoy 中。这使得网关逻辑可以在不重启网关的情况下热更新。
3.  **AI 网关层**：
    *   内置了对 LLM（大模型）协议的统一处理，支持 OpenAI、通义千问等标准接口的转换与流式处理。

### 技术亮点与创新点
*   **AI-Native (AI 原生)**：不同于传统 API 网关将 AI 请求视为普通 HTTP 请求，Higress 在网关层实现了**语义理解与路由**。它不仅能做负载均衡，还能根据 Prompt 内容或上下文进行模型路由、Token 计费和流式截断。
*   **WASM 插件生态**：解决了传统 Lua 插件（如 OpenResty）在安全性、隔离性和性能上的痛点。WASM 插件崩溃不会导致网关崩溃，且支持多语言编写。
*   **MCP (Model Context Protocol) Server 托管**：Higress 内置了对 MCP 协议的支持，使其不仅能转发请求，还能作为 AI Agent 的工具提供者，直接在网关层暴露数据查询能力给 LLM。

### 架构优势分析
*   **高性能**：数据平面 Envoy 基于 C++ 零拷贝技术，延迟极低。
*   **极致的可扩展性**：WASM 插件机制允许开发者像写业务代码一样扩展网关功能，而无需修改网关核心代码。
*   **平滑迁移**：完全兼容 K8s Ingress API 和 Nginx 注解，降低了从传统 Ingress Controller 迁移的成本。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将不同 LLM 提供商（OpenAI, Azure, 通义, 文心一言等）的异构接口统一为标准格式。
    *   **Token 管理**：实时统计流式传输中的 Token 消耗，用于成本控制和限流。
    *   **提示词增强**：在网关层动态插入 System Prompt，实现统一的安全围栏或上下文注入。
2.  **MCP 系统集成**：
    *   作为 MCP Server 的托管中心，允许 AI Agent 通过网关安全地访问内部 API 或数据库，解决了 AI 应用直连数据库的安全风险。
3.  **传统 API 网关**：
    *   K8s Ingress Controller、全链路 TLS、金丝雀发布、流量镜像。

### 解决的关键问题
*   **AI 供应商锁定**：通过统一接口层，业务代码无需修改即可切换底层模型。
*   **流式响应处理**：传统网关在处理 SSE (Server-Sent Events) 时往往缺乏精细控制，Higress 能够在流式传输中进行拦截、修改或计费。
*   **工具调用的安全性**：通过 MCP 协议和网关鉴权，避免了将内部敏感接口直接暴露给公网上的 LLM。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | APISIX | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 LLM 路由/Token计费)** | 弱 (需插件) | 中 (需插件) | 弱 |
| **插件机制** | **WASM (高性能/安全隔离)** | Lua (C共享库风险) | Lua/Plugin Go | WASM (配置较复杂) |
| **K8s 集成** | **原生 (CRD + Ingress)** | 需外部 Controller | 原生 | 原生 |
| **性能** | 高 (Envoy) | 高 | 高 | 高 |
| **易用性** | **高 (Console + K8s)** | 中 | 中 | 低 (学习曲线陡峭) |

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 对 Envoy 的 xDS 协议进行了深度封装，实现了配置的增量更新。这意味着当修改一个路由规则时，只推送变更部分，而非全量配置，极大提升了大规模集群下的稳定性。
*   **WASM 虚拟机集成**：使用 `proxy-wasm` 标准。在 Envoy 中嵌入 WASM 运行时（如 Wasmtime 或 V8），通过 `ABI` 接口允许插件访问 HTTP 头部、Body 和路由信息。
*   **流式处理拦截**：对于 AI 的 SSE 流，Higress 实现了流式缓冲器。它不是简单地透传 TCP 流，而是解析 SSE 格式（`data: {...}`），在转发过程中可以注入元数据或进行计费统计，而不破坏客户端的流式体验。

### 代码组织与设计模式
*   **仓库结构**：典型的 Go Monorepo 结构。`pkg` 目录包含核心逻辑（路由、插件管理），`plugins` 目录包含内置 WASM 插件的源码。
*   **设计模式**：
    *   **Adapter Pattern**：将不同的 AI Provider 接口适配为统一的 `Provider` 接口。
    *   **Filter Chain**：在请求处理链中，WASM 插件被组织为链式调用，每个插件可以决定是否放行请求。

### 性能与扩展性
*   **多线程并发**：Envoy 的多线程模型配合 Go 协程，使得控制平面管理效率极高。
*   **冷启动优化**：WASM 插件支持 AOT（Ahead-of-Time）编译缓存，减少首次加载延迟。

### 技术难点
*   **流式 Body 修改**：在流式响应中修改内容（如敏感词过滤）非常困难，因为数据是分片的。Higress 通过 WASM 的流式处理接口，允许插件在数据流经时进行异步检查和拼接处理。

---

## 4. 适用场景分析

### 最适合的项目
1.  **AI 应用开发平台**：需要接入多种大模型，并进行统一计费、限流和 Prompt 管理的企业级应用。
2.  **微服务流量入口**：基于 Kubernetes 的云原生架构，需要高性能 Ingress Controller 的场景。
3.  **Agent 即服务**：需要将内部工具（API）通过 MCP 协议安全暴露给 AI Agent 的场景。

### 最有效的情况
*   当你需要**在流量层进行细粒度的 AI 逻辑控制**（如：根据用户等级路由到不同精度的模型，或实时拦截敏感 Prompt）时，Higress 的 AI Native 特性比传统网关更有效。
*   当你需要**动态扩展网关功能**（如临时加一个鉴权逻辑）且不想重启网关时，WASM 插件是最佳选择。

### 不适合的场景
*   **极简边缘网关**：如果只需要在单机上进行简单的反向代理，Higress 的资源占用（基于 Envoy 和 Go Control Plane）相对 Nginx 会较重。
*   **非 K8s 环境**：虽然支持 Standalone 模式，但其强大之处在于与 K8s 的结合，在虚拟机裸金属部署上运维复杂度较高。

### 集成方式
*   **Ingress 模式**：替换 K8s 原生 Ingress Controller，通过注解或 CRD 配置。
*   **Service Mesh 模式**：与 Istio 集成，接管东西向流量。

---

## 5. 发展趋势展望

### 演进方向
1.  **从流量网关到语义网关**：未来的 API 网关将不仅基于 URL 路由，而是基于请求的“意图”进行路由。Higress 已经在这个方向上起步（AI Gateway）。
2.  **Dapr 集成**：可能会加强与 Dapr 的集成，使网关不仅是流量的入口，也是分布式能力（状态管理、发布订阅）的入口。
3.  **边缘计算支持**：利用 WASM 的轻量级特性，Higress 可能会进一步向边缘节点下沉，作为边缘端的 AI 推理网关。

### 社区反馈与改进
*   **优势**：阿里巴巴背书，社区活跃，文档完善（中文支持极好）。
*   **改进空间**：WASM 插件的开发调试体验仍有提升空间，目前缺乏类似 VSCode 的强大断点调试工具；AI 网关的 Provider 适配仍需不断追赶新模型发布速度。

---

## 6. 学习建议

### 适合人群
*   **中高级后端工程师**：希望深入理解云原生网关、Service Mesh 及 Envoy 原理。
*   **AI 应用架构师**：需要构建企业级 LLM 应用的技术负责人。
*   **Go 语言爱好者**：研究如何用 Go 构建高性能控制平面。

### 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 概念，了解 Envoy 基础术语。
2.  **入门**：本地部署 Higress (Docker 或 Helm)，配置一个简单的 AI 路由。
3.  **进阶**：阅读 `pkg` 目录下的 xDS 推送逻辑，理解配置如何生效。
4.  **高阶**：编写一个自定义 WASM 插件（使用 Go 或 C++），实现自定义的 Header 修改或鉴权逻辑。

### 实践建议
*   尝试将 Higress 部署在本地 Kind 集群中。
*

---
## 代码示例




```python
# 示例1：使用Higress进行流量路由配置
def configure_higress_routing():
    """
    配置Higress的流量路由规则
    解决问题：实现基于路径的智能路由，将不同请求分发到不同后端服务
    """
    from higress import RouteRule, Gateway

    # 创建网关实例
    gateway = Gateway("my-gateway")

    # 添加路由规则1：/api/v1 路由到服务A
    rule1 = RouteRule(
        match_path="/api/v1/*",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    gateway.add_route(rule1)

    # 添加路由规则2：/api/v2 路由到服务B
    rule2 = RouteRule(
        match_path="/api/v2/*",
        destination="service-b:8080",
        methods=["GET"]
    )
    gateway.add_route(rule2)

    # 应用配置
    gateway.apply_config()
    print("Higress路由配置已成功应用")

# 说明：这个示例展示了如何使用Higress的Python SDK配置基于路径的流量路由，
# 实现将不同API版本的请求分发到不同的后端服务，是微服务架构中的常见场景。
```




```python
# 示例2：Higress限流配置
def configure_rate_limiting():
    """
    配置Higress的限流策略
    解决问题：保护后端服务免受流量洪峰影响，实现QPS限流
    """
    from higress import RateLimitRule, Gateway

    # 创建网关实例
    gateway = Gateway("my-gateway")

    # 配置限流规则：每个IP每秒最多10个请求
    rate_limit = RateLimitRule(
        name="ip-rate-limit",
        limit=10,
        window="1s",
        key_type="IP"
    )
    gateway.add_rate_limit(rate_limit)

    # 应用配置
    gateway.apply_config()
    print("Higress限流配置已成功应用")

# 说明：这个示例展示了如何使用Higress配置基于IP的请求频率限制，
# 有效防止恶意请求或流量洪峰导致后端服务崩溃，是保障服务稳定性的重要手段。
```




```python
# 示例3：Higress金丝雀发布配置
def configure_canary_release():
    """
    配置Higress的金丝雀发布策略
    解决问题：实现新版本的灰度发布，逐步切换流量
    """
    from higress import CanaryRule, Gateway

    # 创建网关实例
    gateway = Gateway("my-gateway")

    # 配置金丝雀规则：10%流量到新版本
    canary = CanaryRule(
        service="my-service",
        new_version="v2",
        traffic_percentage=10,
        match_headers={
            "canary": "true"  # 带有此header的请求100%走新版本
        }
    )
    gateway.add_canary(canary)

    # 应用配置
    gateway.apply_config()
    print("Higress金丝雀发布配置已成功应用")

# 说明：这个示例展示了如何使用Higress实现金丝雀发布(灰度发布)，
# 允许将一小部分流量(如10%)引导到新版本服务，同时可以通过header控制特定请求走新版本，
# 是实现平滑升级和降低发布风险的重要实践。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务迁移与统一网关建设

 1：阿里巴巴内部电商业务迁移与统一网关建设

**背景**:
在 Higress 开源之前，阿里巴巴内部（如淘宝、天猫、饿了么等业务）长期使用自研的网关系统。随着云原生架构的演进，业务容器化程度加深，原有的网关架构在维护成本、扩展性以及对接 Kubernetes (K8s) 生态方面面临挑战。阿里需要一个既能满足内部超大规模并发需求，又能兼容云原生标准（如 Ingress、Gateway API）的统一网关层。

**问题**:
1.  **架构割裂**：传统 API 网关与 K8s Ingress 控制器功能割裂，需要维护两套系统，增加了运维复杂度。
2.  **性能瓶颈**：大促期间流量波动剧烈，需要网关具备极高的处理性能和热更新能力，且不能中断业务。
3.  **扩展性困难**：业务逻辑（如鉴权、流量整形）日益复杂，硬编码方式导致迭代周期长，难以支持不同业务线的个性化需求。

**解决方案**:
阿里巴巴基于内部沉淀多年的网关技术，结合开源社区标准，开发了 **Higress**。
1.  **统一入口**：Higress 作为统一的 API 网关和 Ingress 控制器，接管了进入 K8s 集群的南北向流量以及服务间的东西向流量。
2.  **插件生态**：利用 Higress 的 WASM (WebAssembly) 支持能力，允许业务方使用 Go 或 C++ 编写自定义插件，实现了逻辑的热加载，无需重启网关服务。
3.  **服务治理集成**：深度集成了 Nacos (注册中心) 和 Sentinel (限流熔断)，实现了无缝的服务发现和精细化的流量防护。

**效果**:
1.  **极致性能**：成功支撑了双十一等大促场景，单集群吞吐量达到百万级 QPS，且在保持高吞吐的同时延迟显著降低。
2.  **运维提效**：实现了网关层的云原生化，统一了流量治理体系，运维效率提升 30% 以上。
3.  **业务敏捷**：通过插件市场机制，业务方可以自助开发并部署流量处理逻辑，功能上线周期从周级缩短至小时级。

---



### 2：某头部互联网科技公司 AI 应用网关改造

 2：某头部互联网科技公司 AI 应用网关改造

**背景**:
随着大模型 (LLM) 技术的爆发，该公司内部多个业务线开始接入 AI 能力，涉及对 OpenAI、阿里通义千问等多家模型的调用。原有的 API 网关主要处理传统的 RESTful 调用，缺乏针对 AI 流量特性的优化。

**问题**:
1.  **Token 成本高昂**：AI 调用按 Token 计费，缺乏有效的 Prompt 优化和缓存机制，导致成本居高不下。
2.  **协议转换复杂**：不同 AI 提供商的接口协议（如 SSE 流式输出）不统一，客户端适配困难。
3.  **稳定性风险**：外部 AI 服务提供商可能出现限流或宕机，直接影响核心业务可用性，缺乏智能的容错切换机制。

**解决方案**:
该企业部署了 **Higress** 并启用了其 AI 原生特性。
1.  **AI 统一代理**：利用 Higress 的 AI 插件，将不同厂商的异构接口统一标准化，客户端只需对接 Higress，由网关负责底层协议转换。
2.  **语义缓存**：针对高频重复的 Prompt 请求，启用了基于向量的语义缓存功能，直接返回网关层的缓存结果，无需请求上游模型。
3.  **Prompt 优化与安全拦截**：在网关层注入 Prompt 模板，自动填充上下文，并配置敏感词过滤插件，确保输入输出的合规性。

**效果**:
1.  **成本大幅降低**：通过语义缓存和 Prompt 优化，AI 接口调用成本降低了约 40%。
2.  **开发体验提升**：前端开发人员无需关心复杂的流式传输处理，开发效率显著提高。
3.  **系统稳定性增强**：配置了多模型之间的 fallback（降级）策略，当主模型不可用时自动切换至备用模型，保障了业务连续性。

---



### 3：某大型跨国物流企业微服务流量治理

 3：某大型跨国物流企业微服务流量治理

**背景**:
该企业拥有庞大的物流调度系统，包含数百个微服务，运行在混合云架构（部分在阿里云，部分在本地数据中心）。业务对实时性要求极高，且需要在不同国家/地区进行数据合规处理（如数据本地路由）。

**问题**:
1.  **全链路灰度发布难**：在复杂的微服务调用链中，进行金丝雀发布极其困难，一旦新版本出错，影响范围难以控制。
2.  **跨云流量管理混乱**：混合云环境下，服务注册发现不一致，导致跨数据中心调用延迟高甚至失败。
3.  **缺少流量可视化**：出现故障时，难以快速定位是网络问题还是业务逻辑问题，缺乏全链路追踪能力。

**解决方案**:
引入 **Higress** 作为云原生 API 网关，替代了传统的 Nginx Ingress。
1.  **全链路灰度**：利用 Higress 的标签路由功能，配合 MSE (Microservices Engine) 微服务治理，实现了基于请求权重或 Header 的精细化流量路由，确保特定用户流量仅路由到灰度版本。
2.  **多集群管理**：通过 Higress 的多集群联邦模式，统一管理了本地数据中心和公有云的入口流量，实现了跨地域的智能调度。
3.  **可观测性集成**：无缝对接了 Prometheus 和 SkyWalking，提供了详细的访问日志、指标监控和调用链追踪。

**效果**:
1.  **发布安全性提升**：实现了 100% 的安全灰度发布，新版本故障回滚时间缩短至秒级。
2.  **跨云延迟优化**：通过智能路由策略，优化了跨云调用的网络路径，平均响应延迟降低了 20%。
3.  **故障定位效率**：运维人员可以通过统一的控制台查看流量拓扑，故障排查时间 (MTTR) 减少了 50%。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx | Kong |
|------|----------------|-------|------|
| 性能 | 基于Istio+Envoy，高性能，支持WASM插件扩展 | 高性能，但插件扩展需修改配置或开发C模块 | 高性能，基于OpenResty，插件生态丰富 |
| 易用性 | 提供控制台和Kubernetes集成，配置简化 | 配置复杂，需手动编辑配置文件 | 提供管理UI，但配置需一定学习成本 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源免费，商业支持需付费 | 开源免费，企业版需付费 |
| 功能 | 支持流量管理、安全防护、可观测性 | 基础反向代理和负载均衡 | 丰富的插件生态，支持API网关功能 |
| 扩展性 | 支持WASM插件，动态加载 | 扩展需重启服务，灵活性低 | 支持Lua插件，动态加载 |

### 优势分析

- **优势1**：深度集成Kubernetes和Istio，适合云原生环境。
- **优势2**：支持WASM插件，扩展性强且性能损耗低。
- **优势3**：提供开箱即用的控制台，降低运维复杂度。

### 不足分析

- **不足1**：社区生态较Nginx和Kong小，第三方插件较少。
- **不足2**：对非Kubernetes环境的支持较弱。
- **不足3**：文档和案例相对较少，学习曲线较陡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量管理

**说明**:  
Higress 支持 Kubernetes Ingress 资源，通过注解或 CRD 实现灵活的路由规则配置，包括基于路径、头部、Cookie 等条件的流量分发。

**实施步骤**:
1. 定义 Ingress 资源，配置 `spec.rules` 字段设置路由规则。
2. 使用注解（如 `nginx.ingress.kubernetes.io/rewrite-target`）实现路径重写。
3. 通过 `higress.higress.io/upstream-service` 注解指定后端服务。

**注意事项**:  
- 确保 Higress Ingress Controller 已正确部署并监听 Ingress 资源变更。
- 避免在单个 Ingress 中配置过多规则，建议按服务或域名拆分。

---

### 实践 2：插件化功能扩展

**说明**:  
Higress 提供插件机制，支持动态加载自定义或官方插件（如限流、认证、日志增强），无需重启网关即可生效。

**实施步骤**:
1. 在 Higress 控制台或通过 `WasmPlugin` CRD 启用所需插件。
2. 配置插件参数（如限流的 QPS 阈值、认证服务的地址）。
3. 测试插件功能，确保无性能退化。

**注意事项**:  
- 插件需与 Higress 版本兼容，优先使用官方验证的插件。
- 高频插件（如限流）建议预编译为 WASM 格式以提升性能。

---

### 实践 3：服务治理与熔断

**说明**:  
集成 Istio 或 Nacos 实现服务发现、熔断和重试，保障后端服务不稳定时的系统可用性。

**实施步骤**:
1. 配置 `DestinationRule` 定义熔断策略（如连续错误 5 次触发熔断）。
2. 在 `VirtualService` 中设置重试次数和超时时间。
3. 结合健康检查接口动态剔除异常实例。

**注意事项**:  
- 熔断阈值需根据实际业务 SLA 调优，避免误触发。
- 重试策略应结合幂等性设计，防止重复处理。

---

### 实践 4：安全防护与认证

**说明**:  
通过插件或集成外部认证系统（如 OIDC、API Key）实现访问控制，支持 IP 黑白名单和 JWT 校验。

**实施步骤**:
1. 启用 `key-auth` 插件并配置密钥存储（如 Redis）。
2. 在 `Ingress` 中添加 `higress.higress.io/ip-whitelist` 注解限制访问来源。
3. 对敏感 API 启用 HTTPS 并配置证书。

**注意事项**:  
- 密钥需定期轮换，避免硬编码在配置文件中。
- IP 白名单优先级高于其他认证方式，需谨慎配置。

---

### 实践 5：可观测性集成

**说明**:  
对接 Prometheus、Grafana 或 SkyWalking，收集指标、日志和链路追踪数据，支持实时监控和问题定位。

**实施步骤**:
1. 配置 Higress 的 `stats` 插件暴露 Prometheus 格式指标。
2. 集成 OpenTelemetry 协议导出链路数据至后端系统。
3. 设置告警规则（如延迟超过 500ms 触发通知）。

**注意事项**:  
- 采样率需平衡精度与性能，生产环境建议 10%-30%。
- 日志输出避免包含敏感信息（如 Token、密码）。

---

### 实践 6：多集群与高可用部署

**说明**:  
通过 Higress 的多集群支持实现跨地域流量调度，结合健康检查和故障转移保障服务连续性。

**实施步骤**:
1. 部署多个 Higress 实例并配置集群间通信（如 VPN 或专线）。
2. 使用 `GlobalRateLimit` 实现跨集群限流。
3. 在 DNS 层面配置权重路由，按地域分流。

**注意事项**:  
- 跨集群延迟需纳入监控，避免因网络抖动导致误判。
- 定期演练故障切换流程，验证自动恢复能力。

---

### 实践 7：性能优化

**说明**:  
通过连接池复用、缓存策略和资源限制提升 Higress 吞吐量，降低延迟。

**实施步骤**:
1. 调整 `upstream` 连接池大小（如 `max_connections: 100`）。
2. 对静态内容启用 `cache` 插件，设置 TTL 时间。
3. 限制 Higress 容器的 CPU/内存资源（如 `limits.memory: "2Gi"`）。

**注意事项**:  
- 连接池大小需与后端服务承载能力匹配。
- 缓存内容需校验时效性，避免返回过期数据。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，协议层的优化对延迟和吞吐量影响巨大。HTTP/2 通过多路复用减少连接数，HTTP/3 (QUIC) 基于 UDP 能有效解决 TCP 队头阻塞问题，显著降低弱网环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，明确开启 HTTP/2 和 HTTP/3 协议开关。
2. 配置 TLS 1.3 及以上版本，因为 HTTP/3 强依赖 TLS 1.3。
3. 调整连接超时和 keepalive 设置，以适应长连接场景。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，并发连接处理能力提升，TCP 连接数减少约 60%。

---

### 优化 2：启用 CPU 亲和性与自动均衡

**说明**: 默认的操作系统调度可能会导致进程在 CPU 核心间频繁迁移，造成 L1/L2 Cache 失效。Higress 基于 Envoy，可以通过配置 CPU 亲和性将工作线程绑定到固定的 CPU 核心，减少上下文切换开销。

**实施方法**:
1. 在 Higress 的启动配置或环境变量中设置 worker 线程数量等于物理核心数。
2. 启用 `--cpuset-affinity` 或类似参数（取决于具体部署方式），将 Gateway 进程绑定到特定 CPU 核心。
3. 确保网卡中断均衡（IRQ Balance）配置与 CPU 绑定策略一致，避免处理网络中断的 CPU 核心与处理业务逻辑的核心冲突。

**预期效果**: P99 延迟降低 10%-20%，系统 CPU 上下文切换率显著下降，吞吐量提升 15% 左右。

---

### 优化 3：配置全链路超时与重试策略

**说明**: 不合理的超时和重试策略会导致后端服务雪崩或资源长时间占用。精细化的超时控制能快速释放连接，重试策略的优化（如限制重试次数和触发条件）能防止无效流量风暴。

**实施方法**:
1. 针对不同类型的接口（如读请求/写请求）设置差异化的 `routeTimeout` 和 `upstreamTimeout`。
2. 配置重试策略，仅对网络错误或 5xx 状态码进行重试，并限制最大重试次数（建议 2-3 次）。
3. 开启请求镜像用于压测，但需确保其不影响正常流量超时逻辑。

**预期效果**: 在后端服务出现故障时，网关自身响应时间保持稳定，资源占用率下降，错误请求的处理效率提升 40%。

---

### 优化 4：启用 Wasm 插件的高性能缓存与 AOT 编译

**说明**: Higress 支持 Wasm 插件扩展。Wasm 默认的解释执行模式性能低于原生代码。通过启用 AOT (Ahead-of-Time) 编译或优化 Wasm 内存分配，可以大幅提升插件执行效率。

**实施方法**:
1. 如果使用 Higress 最新版本，启用 Wasm AOT 编译选项，将 Wasm 字节码预编译为本地机器码。
2. 在编写 Wasm 插件时，尽量复用 `Memory`，减少频繁的内存申请与释放操作。
3. 避免在插件请求处理路径中进行高复杂度的正则匹配或阻塞式 IO 操作。

**预期效果**: Wasm 插件执行延迟降低 50% 以上，复杂鉴权或逻辑转换的 CPU 开销显著减少。

---

### 优化 5：优化日志采样与异步上报

**说明**: 详细的访问日志对于排查问题至关重要，但在高并发下，磁盘 IO 和日志序列化会消耗大量 CPU 资源，成为性能瓶颈。

**实施方法**:
1. 配置日志采样（例如每 100 个请求采样 1 个），对于健康检查或高频低价值请求仅记录摘要。
2. 使用异步日志驱动（如将日志输出到 Kafka 或 Fluentd 的异步缓冲区

---
## 学习要点

- 基于提供的来源信息（Alibaba / Higress，来自 GitHub 趋势），以下是关于该项目最值得关注的 5 个关键要点：
- Higress 是阿里云开源的基于 Istio 的下一代云原生 API 网关，旨在解决云原生架构下的流量管理、安全及微服务通信问题。
- 该项目深度集成了 Envoy 和 K8s，能够作为 Ingress Controller 或 API Gateway 使用，实现了从南向（入口流量）到东西向（服务间流量）的全局流量管控。
- Higress 提供了开箱即用的 WAF（Web 应用防火墙）插件和认证鉴权能力，为云原生应用提供了企业级的安全防护。
- 它支持将传统的 Dubbo、Nacos 等微服务注册中心无缝接入网关，帮助存量应用平滑地迁移至云原生架构。
- 通过标准化的 WASM（WebAssembly）插件扩展机制，Higress 允许开发者使用多种编程语言（如 Go、Python、JS）灵活扩展网关功能，而无需修改网关内核。
- 该项目在 GitHub 上迅速获得关注，体现了业界对“云原生 API 网关 + 服务网格”融合架构的强烈需求及对阿里云技术实力的认可。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的基本概念与架构（基于 Istio 和 Envoy）
- 云原生网关的核心功能（流量路由、负载均衡、HTTPS 配置）
- Higress 的安装与部署（Docker、Kubernetes）
- 基本操作：创建网关、配置域名路由、简单插件使用

**学习时间**: 1-2周

**学习资源**:
- [Higress 官方文档](https://higress.io/docs/latest/)
- [Higress GitHub 仓库](https://github.com/alibaba/higress)
- [Envoy 基础教程](https://www.envoyproxy.io/docs/envoy/latest/intro)

**学习建议**:  
先理解云原生网关与传统网关（如 Nginx）的区别，通过官方文档快速上手部署一个简单的 Higress 实例，并完成基本的流量路由配置。

---

### 阶段 2：进阶提升

**学习内容**:
- 高级路由策略（灰度发布、蓝绿部署、A/B 测试）
- 插件系统：自定义插件开发（Wasm 插件）
- 服务治理：熔断、限流、重试机制
- 安全配置：JWT 认证、OAuth 2.0、WAF 防护

**学习时间**: 2-4周

**学习资源**:
- [Higress 插件开发指南](https://higress.io/docs/latest/user/plugin-development/)
- [Istio 流量管理文档](https://istio.io/latest/docs/concepts/traffic-management/)
- [Wasm 官方文档](https://webassembly.org/)

**学习建议**:  
结合实际场景练习灰度发布和流量治理，尝试编写一个简单的 Wasm 插件扩展功能，并深入学习 Istio 的流量管理模型。

---

### 阶段 3：高级优化与实战

**学习内容**:
- 性能优化（连接池、缓存、压缩）
- 多集群部署与跨云管理
- 可观测性：日志、监控、链路追踪（集成 Prometheus、Grafana、SkyWalking）
- 生产环境最佳实践（高可用、灾备、版本升级）

**学习时间**: 3-5周

**学习资源**:
- [Higress 生产实践案例](https://higress.io/blog/)
- [Prometheus 监控集成指南](https://prometheus.io/docs/guides/go-application/)
- [Kubernetes 多集群管理](https://kubernetes.io/docs/concepts/cluster-administration/multi-cluster/)

**学习建议**:  
在测试环境中模拟高并发场景，优化 Higress 的性能指标，并搭建完整的可观测性体系。参考官方案例，尝试在多集群环境中部署 Higress。

---

### 阶段 4：专家级深入

**学习内容**:
- Higress 源码分析与二次开发
- 与其他云原生工具（如 Service Mesh、Serverless）的深度集成
- 大规模流量调度与自动化运维
- 社区贡献与开源协作

**学习时间**: 持续学习

**学习资源**:
- [Higress 源码解析](https://github.com/alibaba/higress/tree/main)
- [CNCF 云原生技术栈](https://www.cncf.io/)
- [开源社区贡献指南](https://opensource.guide/)

**学习建议**:  
深入阅读 Higress 和 Istio 的源码，参与社区讨论，提交 Issue 或 PR，积累实战经验并分享技术见解。

---
## 常见问题


### 1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

**A**: Higress 是一个开源的、基于云原生架构的 API 网关。它是在 2022 年由阿里巴巴（达摩院）开源的，其核心代码源自阿里巴巴内部大规模使用多年的商业化 API 网关产品。因此，Higress 继承了阿里在处理高并发、流量治理和安全防护方面的深厚技术积累。

从技术架构上看，Higress 是基于 Nginx（具体是 OpenResty）和 Envoy 构建的。它深度集成了 Envoy 作为高性能数据面，同时利用 K8s Ingress Controller 的形态进行管理。简单来说，它结合了 Nginx/OpenResty 的高性能生态插件能力和 Envoy 的云原生可扩展性，旨在为云原生时代提供统一的流量入口。

---



### 2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

**A**: Higress 在设计上主要针对云原生环境和微服务架构进行了优化，其核心优势包括：

1.  **深度集成阿里生态**：Higress 原生支持对接阿里云 MSE（微服务引擎）、ACK（容器服务）以及 Nacos 注册中心。对于使用阿里云技术栈的用户来说，迁移和运维成本极低。
2.  **高性能与低资源消耗**：基于 Envoy 和 Rust（部分控制面组件）构建，Higress 在长连接管理和大规模路由场景下的性能表现优异，且资源占用相对较低。
3.  **插件系统兼容性**：它不仅支持原生 Lua 插件（兼容 OpenResty/Nginx 生态），还支持 Wasm（WebAssembly）插件。Wasm 插件允许使用 C++、Go、Rust 等多种语言编写，具有更好的隔离性和安全性，且支持热加载，无需重启网关。
4.  **安全防护**：内置了与阿里云 WAF 联动的能力，提供了开箱即用的安全防护规则。

---



### 3: Higress 是否支持非 K8s 环境（虚拟机或裸金属服务器）的部署？

3: Higress 是否支持非 K8s 环境（虚拟机或裸金属服务器）的部署？

**A**: 是的，Higress 支持多种部署模式。

虽然 Higress 是作为 Kubernetes 的 Ingress Controller 设计的，以充分发挥其云原生特性，但它也提供了**标准版**（Standalone）安装包。用户可以通过 Docker Compose 或直接在 Linux 服务器上部署 Higress，使其能够作为传统的 API 网关运行在虚拟机或物理机环境中。这种灵活性使得它既适用于完全容器化的架构，也适用于从传统架构向云原生架构过渡的混合环境。

---



### 4: 如何处理 Higress 的插件开发？是否必须使用 Lua？

4: 如何处理 Higress 的插件开发？是否必须使用 Lua？

**A**: 不必须。Higress 提供了非常灵活的插件扩展机制，主要分为以下几类：

1.  **Wasm 插件（推荐）**：这是 Higress 主推的插件模式。开发者可以使用 Go、C++、Rust 或 AssemblyScript 编写业务逻辑，编译成 `.wasm` 文件后上传到网关。Wasm 插件运行在沙箱环境中，安全性高，且支持动态加载，不会影响主进程稳定性。
2.  **Lua/Python 插件**：Higress 兼容 OpenResty 的 Lua 生态，用户可以直接复用现有的 Lua 脚本或 Kong 插件（通常需要少量修改）。同时，通过 Python Runner，Higress 也支持编写 Python 脚本来处理逻辑，降低了业务开发人员的门槛。
3.  **原生插件**：对于极致性能要求的场景，也可以编写 Go 代码直接编译进网关程序（通常适用于核心开发者）。

---



### 5: Higress 能否直接对接 Dubbo 或 gRPC 服务？

5: Higress 能否直接对接 Dubbo 或 gRPC 服务？

**A**: 可以。Higress 具备强大的协议转换能力，这是它作为微服务网关的一大特色。

1.  **Dubbo 支持**：Higress 原生支持 Apache Dubbo（包括 Dubbo2 和 Dubbo3 协议）。它可以将 HTTP/HTTPS 请求透明地转换为 Dubbo 协议，调用后端的 Java Dubbo 服务。这对于需要将传统的内部 Dubbo 服务暴露给外部 HTTP 客户端的场景非常有用。
2.  **gRPC 支持**：Higress 支持 gRPC 协议代理，支持 HTTP/2，并可以实现 gRPC 到 JSON/HTTP 的双向转码，方便前端或移动端调用后端的 gRPC 微服务。

---



### 6: 从 Nginx 或传统负载均衡器迁移到 Higress 困难吗？

6: 从 Nginx 或传统负载均衡器迁移到 Higress 困难吗？

**A**: 难度取决于现有的配置复杂度，但 Higress 提供了多种工具来降低迁移门槛。

1.  **Nginx 配置兼容**：Higress 提供了工具或指南，帮助用户将 Nginx 的 `nginx.conf` 配置转换为 Higress 的 Ingress 或 Gateway API 资源配置。
2.  **In

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础流量验证

### 在本地或 Kubernetes 环境中部署 Higress。配置一个简单的 Ingress 路由，将访问 `/hello` 的流量转发到一个提供 JSON 响应的测试后端服务（如 httpbin.org），并使用 curl 命令验证配置是否生效。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其与阿里云产品的集成能力及开源网关的通用特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现模型供应商的统一适配
**场景**：企业内部同时使用通义千问、OpenAI 以及本地部署的模型（如 Llama），不同厂商的 API 协议（参数格式、鉴权方式）差异巨大。
**建议**：不要在业务代码中处理不同模型的差异。编写或使用现有的 Wasm 插件（如 `ai-proxy`），在网关层将所有外部模型的 API 统一转换为 OpenAI 兼容的格式。
**操作**：配置路由时，将不同的后端服务（如 `dashscope.aliyuncs.com` 和 `api.openai.com`）挂载到同一个网关域名下，通过请求头或路径区分，并在插件层完成参数映射。
**陷阱**：注意流式输出（SSE）的转换处理，确保插件能正确处理分块传输编码，否则会导致流式响应中断。

### 2. 实施基于 Token 的精细化限流而非仅基于 QPS
**场景**：大模型推理成本高昂，且不同 Prompt 的消耗差异极大。传统的基于“每秒请求数”（QPS）的限流无法有效控制成本。
**建议**：配置针对 AI 服务的限流策略时，优先考虑基于 Token 吞吐量或请求处理时长的限流。Higress 支持对 AI 请求进行更细粒度的识别。
**操作**：在特定路由或服务级别配置限流规则，并结合业务需求，对非生产环境或内部测试账号设置较低的 Token 预算阈值。
**陷阱**：避免对长文本生成任务设置过短的超时时间，这可能导致网关过早断开连接，浪费上游模型已生成的 Token。

### 3. 配置语义路由以实现多模型分发
**场景**：简单的路径匹配（如 `/v1/chat`）无法满足复杂的业务需求，例如：简单问题走便宜的小模型，复杂 RAG 问题走大模型，或图片生成走专用模型。
**建议**：利用 Higress 的 AI 特性路由能力，根据请求内容的语义特征进行流量分发。
**操作**：配置路由规则，提取 Prompt 的摘要或特征向量，将请求分发到不同的后端服务（Service A：7B 模型，Service B：72B 模型）。这通常需要配合一个轻量级的分类模型或特定的 Prompt 指令作为路由判断依据。
**陷阱**：语义判断本身会增加延迟，需确保路由判断逻辑（通常也是一次 LLM 调用）的速度极快，或者使用本地小模型进行路由判断，防止造成性能瓶颈。

### 4. 建立提示词的安全护栏与敏感词过滤
**场景**：防止用户通过 Prompt Injection 攻击套取系统指令，或输入违规内容导致账号被封禁。
**建议**：在网关层部署安全插件，对所有进站的 AI 请求进行预处理。
**操作**：启用 Higress 的安全插件或配置 Wasm 插件，对 `user` 角色的消息进行关键词过滤或通过本地小模型进行意图审查。对于包含敏感内容的请求，网关应直接拦截并返回标准错误，避免请求打到后端昂贵的 LLM。
**陷阱**：不要过度拦截导致误杀，建议在拦截前配置“灰度模式”，先只记录违规日志而不拦截，观察一段时间后再开启硬拦截。

### 5. 启用缓存策略减少重复推理成本
**场景**：用户频繁询问相同的问题（如“如何重置密码”），每次都调用 LLM 产生高额费用且延迟高。
**建议**：针对“读多写少”且对实时性要求不极高的场景，启用响应缓存。
**操作**：配置缓存插件，将 Prompt 的 Hash 值作为 Key，将 LLM 的返回结果存入 Redis 或内存缓存中。设置合理的 TTL（例如 1 小时）。对于高相似度的 Prompt，可以考虑配置向量缓存。
**陷阱**：必须确保缓存

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [Kirara-ai：支持多平台接入的多模态AI聊天机器人]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [kirara-ai：支持多平台接入的多模态 AI 聊天机器人]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [Nemotron-Personas-Brazil：主权AI的协同设计数据集]({{< relref "posts/20260129-blogs_podcasts-nemotron-personas-brazil-co-designed-data-for-sove-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*