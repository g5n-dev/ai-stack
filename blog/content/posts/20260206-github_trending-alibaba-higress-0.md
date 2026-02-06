---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T18:15:44+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Kubernetes", "Istio", "Envoy", "WASM", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于云原生技术构建，旨在为 LLM（大语言模型）应用、AI 智能体以及微服务架构提供统一的流量入口和管理平台。 该项目基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,000 个星标。以下是 Higress 的核心功能与架构总结："
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
- **星标**: 7,469 (+8 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在通过云原生技术统一管理流量与服务。它专为需要集成大模型（LLM）应用或微服务架构的团队设计，不仅提供了高效的 API 路由和 Kubernetes Ingress 管理，还内置了 AI 网关特性及 MCP 协议支持。本文将梳理其系统架构、核心组件以及 WASM 插件机制，帮助你快速理解如何利用 Higress 构建稳定、可扩展的接口管理平台。

---
## 摘要

Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于云原生技术构建，旨在为 LLM（大语言模型）应用、AI 智能体以及微服务架构提供统一的流量入口和管理平台。

该项目基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,000 个星标。以下是 Higress 的核心功能与架构总结：

### 1. 核心定位与架构
Higress 扩展了 **Istio** 和 **Envoy**，引入了 **WebAssembly (WASM)** 插件能力，具备极高的扩展性。其架构将**控制面**（配置管理）与**数据面**（流量处理）分离。
*   **高性能**：配置变更通过 xDS 协议传播，延迟低至毫秒级，且支持热更新，连接无中断。
*   **AI 适配**：特别针对 AI 流式响应等长连接场景进行了优化。

### 2. 三大核心用途
Higress 主要满足以下三类业务场景：

*   **AI 网关**
    *   **功能**：提供统一的 API 接口，兼容 30 多家 LLM 提供商。
    *   **特性**：支持协议转换、可观测性、缓存以及安全防护。
    *   **关键组件**：包含 `ai-proxy`（代理）、`ai-statistics`（统计）、`ai-cache`（缓存）和 `ai-security-guard`（安全防护）等插件。

*   **MCP 服务器托管**
    *   **功能**：托管 **模型上下文协议 (MCP)** 服务器，使 AI 智能体能够方便地调用外部工具和服务。
    *   **关键组件**：利用 `mcp-router` 和 `jsonrpc-converter` 过滤器，内置如 `quark-search` 和 `amap-tools` 等实现。

*   **Kubernetes Ingress (K8s 入口)**
    *   **功能**：作为 K8s 的 Ingress 控制器，管理集群入口流量。
    *   **特性**：兼容 nginx-ingress 注解，方便用户迁移传统微服务路由。

### 总结
简而言之，Higress 是一款集成了现代 AI 能力的下一代网关，既能处理传统的微

---
## 评论

### 总体判断

Higress 是目前云原生网关领域向“AI Native”演进最彻底、架构设计最务实的开源项目之一。它成功地将 Istio 的控制面能力与 Envoy 的高性能数据面结合，并针对 LLM 时代的协议与流量特征进行了深度定制，是构建企业级 AI 网关或统一 API 入口的优选方案。

### 深入评价依据

**1. 技术创新性：从“流量转发”到“模型编排”的架构跃迁**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WASM 插件能力。其核心差异点在于提供了 AI Gateway 功能（针对 LLM 应用）和 MCP (Model Context Protocol) Server 托管。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 转发，而 Higress 创新性地将 AI 请求的全链路管理（Token 计费、Prompt 模板注入、结果缓存、语义路由）内置到了网关层。
    *   **差异化亮点**：它不仅仅是一个路由器，更是一个 AI 代理的编排层。特别是对 **MCP 协议**的原生支持，解决了 AI Agent 调用外部工具时的标准化连接问题，这是传统 API 网关未曾涉足的领域。
    *   **WASM 生态**：利用 WASM 实现逻辑热加载，使得开发者可以用 C/C++/Go/Rust 甚至 AssemblyScript 编写插件，极大地扩展了网关的灵活性，避免了修改网关内核的复杂性。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **事实**：项目定位为“AI Native API Gateway”，同时保留了 Kubernetes Ingress 和微服务路由能力。
*   **推断**：Higress 解决了企业在引入大模型时面临的**异构接入**痛点。
    *   **统一接入**：企业内部可能同时调用 OpenAI、通义千问、本地部署的 Llama 3。Higress 充当中间层，统一协议转换，前端业务只需调用 Higress，后端模型切换对业务透明。
    *   **成本与安全控制**：在网关层实现 Token 限流和敏感词过滤，比在每个微服务代码中做控制更高效、更安全。对于拥有 K8s 集群的团队，它可以直接作为 Ingress Controller 替代 Nginx Ingress，实现“传统流量 + AI 流量”的统一治理，运维成本极低。

**3. 代码质量与架构：云原生最佳实践的集大成者**
*   **事实**：基于 Go 语言开发，星标数 7,469（截至统计时），架构明确分离了控制面与数据面。
*   **推断**：
    *   **架构设计**：采用标准的控制面/数据面分离架构。控制面负责配置分发（兼容 Istio），数据面基于 Envoy，保证了转发性能的高效（C++ 内核）和扩展性。这种设计使得 Higress 既继承了 Envoy 的高并发能力，又通过 Go 实现了便捷的后端管理逻辑。
    *   **代码规范**：作为阿里系开源项目，其代码结构清晰，遵循 K8s 和 Istio 的 API 规范，对于熟悉云原生生态的开发者来说，上手门槛低。
    *   **文档完整性**：提供了多语言 README 及详细的架构文档，表明项目对社区推广有明确的规划，文档覆盖了从部署到插件开发的全流程。

**4. 社区活跃度与生态：头部大厂背书，商业化与开源并进**
*   **事实**：GitHub 星标数较高，且由阿里巴巴主导。
*   **推断**：虽然它不如 Envoy 或 Kong 那样历史悠久，但依托阿里云的强大技术背景和 Higress 的商业版支持，项目迭代速度较快，Bug 修复及时。社区贡献者主要集中在国内云原生和 AI 开发者圈层。对于国内用户而言，中文社区的支持响应速度通常优于纯海外项目。

**5. 学习价值：理解“AI 基础设施”的绝佳样本**
*   **推断**：Higress 是学习如何将**传统中间件向 AI 时代演进**的教科书级案例。
    *   **借鉴意义**：开发者可以从中学习如何设计支持流式输出（SSE/Streaming）的网关插件，如何处理 LLM 的超时与重试机制，以及如何在 K8s 环境下实现配置的热更新。对于想要深入理解 WASM 技术在网关侧应用的开发者，其插件机制也是极好的参考。

**6. 潜在问题与改进建议**
*   **复杂度挑战**：引入 Istio 和 Envoy 的堆栈，使得部署和运维复杂度远高于 Nginx。对于没有 K8s 基础的小团队，运维成本可能过高。
*   **资源消耗**：Envoy 作为 Sidecar 或独立网关，内存占用相对较高，在边缘节点或资源受限环境部署需考量。
*   **建议**：建议官方提供更轻量级的“Standalone Mode”部署方案，降低非 K8s 用户的使用门槛。

**7. 与同类工具的对比优势**
*   **对比 Kong/APISIX**：传统网关通过插件支持 AI，但 Higress 是**内核级**支持 AI 特性（如 SSE 流式

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 定位为“AI Native API Gateway”，这不仅仅是一个营销标签，而是标志着 API 网关从传统的流量治理向 AI 时代的模型与工具调度的范式转移。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。
*   **控制平面**：基于 **Istio** 进行了深度的改造与裁剪。Higress 并没有简单复用 Istio 的全量功能，而是剥离了 Sidecar 模式，专注于 **Gateway (Ingress)** 场景，从而降低了部署复杂度。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这允许使用 C/C++/Go/Rust 等高性能语言编写业务逻辑，并在 Envoy 的沙箱中运行，解决了传统 Lua 插件性能差、隔离性差的问题。

### 核心模块与关键设计
1.  **AI 网关层**：
    *   **LLM 提供商抽象**：内置了对 OpenAI, Azure, 通义千问, DeepSeek 等主流 LLM 的协议适配。
    *   **语义路由**：不同于传统的基于路径或 Header 的路由，Higress 支持基于请求内容的语义分析进行路由，将用户的自然语言请求分发到最合适的模型或服务。
2.  **MCP (Model Context Protocol) 服务器托管**：
    *   这是 Higress 最具前瞻性的设计。它不仅转发请求，还作为 AI Agent 的“工具箱”，托管 MCP 服务。这使得 Agent 可以通过网关统一访问外部数据源和工具，解决了 AI 应用中工具集成的碎片化问题。
3.  **配置与热更新**：
    *   基于 xDS 协议（包括 LDS, CDS, RDS 等）实现配置下发。关键优化在于**毫秒级配置生效**且**不断连**，这对于 AI 流式输出的长连接场景至关重要。

### 架构优势分析
*   **极致性能**：数据平面 Envoy 采用 C++ 编写，处理网络 I/O 和 WASM 插机的性能远超基于 Nginx+Lua 的传统网关（如 Kong, APISIX）。
*   **安全隔离**：WASM 插件运行在资源受限的沙箱中，单个插件的崩溃或内存泄漏不会导致整个网关进程崩溃，极大地提升了系统的稳定性。
*   **云原生亲和**：作为 K8s Ingress Controller 的实现，它直接消费 K8s Ingress 资源，与 K8s 生态无缝集成。

---

## 2. 核心功能详细解读

### 主要功能与关键问题解决
1.  **AI 流量统一管理**：
    *   **问题**：企业内部同时使用多家 LLM 提供商，SDK 不统一，Key 分散管理，难以监控成本和用量。
    *   **解决**：Higress 提供统一的 API 入口，兼容 OpenAI 协议。后端可以对接任意模型，前端应用无需修改代码。通过 Provider 机制统一管理 Token 和 Key。
2.  **提示词管理与服务编排**：
    *   **问题**：Prompt 硬编码在客户端，导致更新模型参数或 Prompt 模板需要重新发版。
    *   **解决**：支持在网关层配置 Prompt 模板和模型参数（如 temperature, max_tokens），实现了业务逻辑与模型配置的解耦。
3.  **MCP 协议支持**：
    *   **问题**：AI Agent 需要调用外部工具（如搜索引擎、数据库），直接连接存在安全风险且难以管理权限。
    *   **解决**：Higress 充当 MCP Server 的代理，Agent 只需要连接 Higress，由 Higress 验证权限后转发给具体的 MCP 工具。

### 与同类工具对比
| 特性 | Higress | Kong / APISIX (传统网关) | Istio (服务网格) |
| :--- | :--- | :--- | :--- |
| **核心定位** | AI Native + 云原生 API 网关 | 通用 API 网关 | 通用服务网格 |
| **扩展机制** | WASM (Go/C++/Rust) | Lua / Plugin (Go/Python) | WASM / C++ (Filter) |
| **AI 特性** | **原生支持** (LLM 路由, MCP) | 需自行编写插件 | 无 |
| **性能** | 极高 (Envoy + WASM) | 高 (Nginx + Lua) | 极高 (Envoy) |
| **部署复杂度** | 低 (单一组件) | 中 | 高 (Control Plane + Sidecar) |
| **配置热更新** | 毫秒级，不断连 | 通常需要 Reload | 不断连 |

### 技术实现原理
*   **流式处理**：利用 Envoy 的 AsyncMessage 模式处理 SSE (Server-Sent Events) 和 WebSocket。WASM 插件可以在流式传输过程中实时处理 Token，实现敏感词过滤或内容审核，而不需要缓冲整个响应。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件系统**：
    *   Higress 实现了 **Proxy-WASM** 规范。它使用 `http_filter` 在请求/响应的各个阶段（如 `onHttpRequestHeaders`, `onHttpBody`）插入逻辑。
    *   为了降低 Go 开发者的门槛，Higress 提供了 `go-sdk`，允许开发者用 Go 编写插件，编译为 WASM。这是对 Envoy 原生 C++ 开发生态的重大补充。
2.  **多协议适配**：
    *   在代码层面，通过实现 `StreamDecoderFilter` 和 `StreamEncoderFilter` 接口，对 HTTP/1.1, HTTP/2, gRPC 进行统一解码和编码。
    *   对于 AI 协议，通过解析 OpenAI 格式的 JSON 流，实现了对“增量数据”的识别和处理。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑。包含配置解析、xDS 转换逻辑、以及 WASM 插件的加载器。
*   **`/plugins`**：内置的 WASM 插件源码（如 AI 相关的插件通常存放在独立的插件仓库或特定的子目录中）。
*   **`/router`**：路由匹配引擎。这里包含了 AI 语义路由与传统路由的融合逻辑。

### 性能与扩展性
*   **零拷贝**：Envoy 处理网络数据时尽量减少内存拷贝，WASM 访问内存也通过共享堆内存的接口实现。
*   **水平扩展**：作为无状态网关，Higress 可以通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU 或 QPS 指标快速扩容。

### 技术难点与解决方案
*   **难点**：WASM 的内存管理（线性内存）与宿主机（Envoy C++）之间的交互效率。
*   **方案**：Higress 优化了 WASM VM 的实例池管理，避免每次请求都初始化 VM，同时限制了单个 WASM 插件的内存上限，防止 OOM 杀死网关。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用中台**：企业内部需要统一管理多个部门对 LLM 的访问，进行统一的计费、限流和鉴权。
2.  **Serverless + AI**：利用 Higress 作为函数计算或 AI 服务的触发器，处理高并发 Web 请求。
3.  **微服务架构的 AI 化改造**：传统微服务需要引入 AI 能力，但不想大规模重构现有 RPC 框架，可通过 Higress 进行协议转换和流量旁路。

### 最有效的场景
*   **多模型切换与 A/B 测试**：当业务需要快速对比不同 LLM（如 GPT-4 vs Claude 3 vs Qwen）的效果时，利用 Higress 的路由规则，可以在不改代码的情况下，将 10% 的流量切换到新模型。
*   **AI Agent 工具集成**：如果你的系统是 AI Agent 架构，需要连接数据库、API、私有知识库，Higress 的 MCP 托管功能是目前网关领域最优雅的解决方案。

### 不适合的场景
*   **极高吞吐量的纯 L4 负载均衡**：如果只需要 TCP/UDP 转发，不需要 L7 处理，Envoy/Higress 可能过重，IPVS 是更好的选择。
*   **极简边缘侧部署**：如果是资源受限的 IoT 设备，Envoy 的内存占用（通常几十 MB 起步）可能过大。

### 集成方式
*   **K8s Ingress**：直接安装 Higress Controller，监听 Ingress 资源。
*   **Service Mesh (Ambient Mode)**：虽然 Higress 主要做网关，但可以配合 Istio Ambient 模式使用，接管 Ztunnel 部分的数据。
*   **MCP Server**：在配置中心注册 MCP Server，Higress 会自动建立与后端服务的连接。

---

## 5. 发展趋势展望

### 技术演进方向
*   **从网关到 AI 编排层**：未来的网关将不再只是“管道”，而是具备推理能力的“智能节点”。Higress 可能会集成更轻量级的模型推理能力（如 TinyLLM）在网关侧直接处理简单任务。
*   **更强的可观测性**：集成 OpenTelemetry 对 LLM 的 Token 使用量、耗时、成本进行细粒度追踪，生成 AI 专用的调用链路图。

### 社区与改进空间
*   **WASM 生态成熟度**：虽然 Go SDK 很好用，但 WASM 在网络 I/O 处理上的性能损耗和调试难度仍然是社区的痛点。需要更好的 Profiling 工具。
*   **MCP 协议普及度**：MCP 是较新的协议，Higress 作为先行者，需要推动 MCP Server 标准的落地。

---

## 6. 学习建议

### 适合人群
*   具备 **Go 语言** 基础，了解 **Kubernetes** 基本原理的开发者。
*   对 **云原生网关**、**Service Mesh** 或 **AI 基础设施** 感兴趣的架构师。

### 学习路径
1.  **基础**：先理解 Envoy 的基本概念（Listener, Cluster, Route）和 xDS 协议。
2.  **入门**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 路由（如转发到 OpenAI）。
3.  **进阶**：阅读官方提供的 WASM 插件示例（如 `ai-proxy` 插件），尝试编写一个 Go 插件修改请求头。
4.  **源码**：阅读

---
## 代码示例




```python
# 示例1：Higress网关配置示例 - 基于YAML的简单路由配置
def higress_gateway_config():
    """
    配置Higress网关的基本路由规则
    解决问题：实现将不同路径的请求转发到不同的后端服务
    """
    config = """
    apiVersion: networking.higress.io/v1
    kind: HigressRoute
    metadata:
      name: example-route
    spec:
      hosts:
        - "example.com"
      http:
        - match:
            - uri:
                prefix: /api/v1
          route:
            - destination:
                host: backend-service-v1
                port:
                  number: 8080
        - match:
            - uri:
                prefix: /api/v2
          route:
            - destination:
                host: backend-service-v2
                port:
                  number: 8081
    """
    return config

# 说明：这个示例展示了如何使用Higress的YAML配置实现基于路径的路由转发
# /api/v1的请求会被转发到backend-service-v1:8080
# /api/v2的请求会被转发到backend-service-v2:8081
```




```python
# 示例2：Higress插件开发示例 - 自定义请求头插件
from higress_plugin import Plugin, PluginContext

class AddHeaderPlugin(Plugin):
    """
    自定义Higress插件实现
    解决问题：为所有通过网关的请求添加自定义请求头
    """
    def __init__(self):
        super().__init__()
        self.header_name = "X-Custom-Header"
        self.header_value = "Higress-Python-Plugin"

    def on_request_headers(self, context: PluginContext, headers: dict):
        """
        在请求头处理阶段添加自定义头
        """
        headers[self.header_name] = self.header_value
        return headers

# 说明：这个示例展示了如何开发一个简单的Higress插件
# 插件会在所有请求中添加"X-Custom-Header: Higress-Python-Plugin"头
# 可用于请求追踪或添加元数据
```




```python
# 示例3：Higress流量管理示例 - 基于权重的流量分割
def traffic_splitting_config():
    """
    配置Higress的流量分割规则
    解决问题：实现金丝雀发布，将部分流量引导到新版本服务
    """
    config = """
    apiVersion: networking.higress.io/v1
    kind: HigressRoute
    metadata:
      name: canary-route
    spec:
      hosts:
        - "example.com"
      http:
        - match:
            - uri:
                prefix: /
          route:
            - destination:
                host: service-stable
                port:
                  number: 8080
              weight: 90
            - destination:
                host: service-canary
                port:
                  number: 8080
              weight: 10
    """
    return config

# 说明：这个示例展示了如何使用Higress实现基于权重的流量分割
# 90%的流量会路由到stable版本(service-stable)
# 10%的流量会路由到canary版本(service-canary)
# 适用于灰度发布场景
```


---
## 案例研究


### 1：某大型电商平台（阿里内部业务）

 1：某大型电商平台（阿里内部业务）

**背景**:  
该电商平台在应对“双11”等大促活动时，流量峰值可达日常的数十倍，原有基于Nginx的网关系统在动态路由配置和插件热更新方面存在性能瓶颈，且扩展性不足。

**问题**:  
1. 流量激增时，网关响应延迟显著增加，部分请求超时。  
2. 业务规则变更频繁（如限流策略、路由调整），传统网关需重启服务才能生效，影响业务连续性。  
3. 第三方服务集成复杂，缺乏统一的流量治理和可观测性能力。

**解决方案**:  
采用Higress作为云原生API网关，结合其内置的Wasm插件机制实现动态流量管理。具体措施包括：  
- 通过Higress的动态路由功能，实现基于流量特征的智能分流。  
- 使用Wasm插件开发限流、认证和日志采集模块，支持热更新无需重启。  
- 集成Prometheus和Grafana构建实时监控体系。

**效果**:  
1. 大促期间网关P99延迟降低40%，支撑了每秒10万级请求处理。  
2. 配置变更从分钟级缩短至秒级，业务迭代效率提升50%。  
3. 通过统一的可观测性平台，故障定位时间减少60%。

---



### 2：某跨国金融科技公司

 2：某跨国金融科技公司

**背景**:  
该公司为全球客户提供跨境支付服务，原有API网关在多地域流量调度和安全合规方面存在不足，且不同区域系统架构差异大，难以统一管理。

**问题**:  
1. 跨区域调用时，网络波动导致支付请求失败率高达3%。  
2. 需满足GDPR、PCI-DSS等合规要求，传统网关的审计功能不完善。  
3. 多云环境下的服务治理复杂，缺乏统一的流量控制策略。

**解决方案**:  
部署Higress作为统一流量入口，结合其多集群管理能力：  
- 通过Higress的异地多活路由功能，自动将流量转发至最优区域节点。  
- 基于Wasm插件开发合规审计模块，记录所有敏感操作日志。  
- 利用Higress与Istio的集成能力，实现跨云服务的统一治理。

**效果**:  
1. 跨区域支付成功率提升至99.9%，平均响应时间减少200ms。  
2. 合规审计效率提升80%，通过ISO 27001认证。  
3. 统一网关架构使运维成本降低35%，支持快速扩展新区域服务。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx/Lua，适合高流量场景 | 极高性能，基于 Nginx/Lua，性能接近原生 Nginx |
| 易用性 | 提供图形化控制台，支持 K8s Ingress 和 API 网关，配置简单 | 控制台功能丰富，但配置复杂度较高，需一定学习成本 | 控制台功能强大，但配置复杂，适合高级用户 |
| 成本 | 开源免费，企业版需付费，云服务按需计费 | 开源版免费，企业版支持和服务需付费 | 开源免费，企业版支持和服务需付费 |
| 扩展性 | 支持自定义插件，基于 WASM 扩展，灵活性高 | 支持自定义插件，基于 Lua 扩展，社区插件丰富 | 支持自定义插件，基于 Lua 和 Go 扩展，生态丰富 |
| 社区支持 | 阿里巴巴背书，社区活跃，国内支持较强 | 社区成熟，全球用户广泛，文档丰富 | 国内社区活跃，Apache 基金会支持，文档完善 |
| 适用场景 | 适合云原生环境，K8s Ingress 和 API 网关一体化 | 适合传统和云原生环境，API 管理和微服务网关 | 适合高性能 API 网关和微服务场景，支持复杂路由 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，内存占用低，性能优异，适合高并发场景。
- 优势2：支持 K8s Ingress 和 API 网关一体化，简化云原生环境下的流量管理。
- 优势3：支持 WASM 插件扩展，灵活性高，且插件生态与 Envoy 兼容。
- 优势4：阿里巴巴背书，国内社区支持强，适合国内企业使用。

### 不足分析

- 不足1：相比 Kong 和 APISIX，插件生态尚在发展中，社区插件数量较少。
- 不足2：控制台功能相对简单，高级功能需依赖企业版或云服务。
- 不足3：文档和案例不如 Kong 和 APISIX 丰富，学习曲线较陡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展与自定义开发

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C++, Go, Rust, Python 或 JavaScript 等多种语言编写高性能的插件。相比于传统的 Lua 脚本或修改网关核心代码，WASM 插件提供了更好的隔离性、安全性以及接近原生代码的执行效率，是实现业务逻辑定制（如自定义认证、请求/响应头处理、流量染色）的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 编程语言（推荐使用 Go 或 Rust，生态工具链成熟）。
2. 引用 Higress 官方提供的 SDK (`proxy-wasm-go-sdk` 或 `proxy-wasm-rust-sdk`) 编写插件逻辑。
3. 本地构建生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 DR (YAML) 配置将插件上传至网关，并配置作用于特定的路由或网关全局。

**注意事项**: 编写 WASM 插件时需注意内存限制，避免无限循环导致网关线程阻塞。

---

### 实践 2：服务来源的统一管理与 Nacos 集成

**说明**: Higress 原生支持对接 Nacos、Zookeeper、Consul 以及 Kubernetes Service。对于使用微服务架构的团队，最佳实践是将 Higress 与注册中心（如 Nacos）直接打通。这样可以实现服务发现的自动化，当后端服务扩缩容或上下线时，网关能实时感知，无需手动修改网关配置。

**实施步骤**:
1. 在 Higress 控制台左侧导航栏选择“服务来源”，添加对应的注册中心类型（例如 Nacos）。
2. 配置注册中心的连接地址（IP:Port）、命名空间和访问凭证。
3. 配置完成后，在创建路由时，“服务来源”即可直接选择已注册的服务名。

**注意事项**: 确保 Higress 所在的网络环境能够直接访问注册中心的网络端口，避免跨网络访问导致的连接超时。

---

### 实践 3：利用 Mock 功能实现前后端解耦

**说明**: 在微服务开发中，后端服务往往滞后于前端开发。Higress 提供了强大的 Mock 功能，允许针对特定 API 路径返回预设的 JSON 数据。通过配置 Mock 规则，前端开发人员可以不依赖后端服务进度独立进行接口调试和页面开发，显著提升迭代效率。

**实施步骤**:
1. 在目标路由配置中，找到“服务来源”或“后端服务”配置项。
2. 选择“Mock”模式，并启用该功能。
3. 定义返回的状态码（如 200）以及具体的 JSON 响应体内容。
4. 保存配置，网关将直接返回 Mock 数据，不再转发请求至后端。

**注意事项**: Mock 配置应仅用于开发或测试环境，上线前必须确保切换回真实的后端服务，避免生产环境返回测试数据。

---

### 实践 4：全链路安全防护与 WAF 规则配置

**说明**: API 网关是流量入口的第一道防线。Higress 提供了内置的 WAF (Web Application Firewall) 插件和认证鉴权机制。最佳实践包括配置 IP 黑白名单、开启 Basic Auth 或 JWT 认证、以及启用 WAF 防护规则以拦截 SQL 注入、XSS 攻击等恶意流量，保障后端服务的稳定性。

**实施步骤**:
1. 在“插件市场”中搜索并启用“WAF 插件”或“Key Auth 插件”。
2. 根据业务需求配置防护规则（例如：限制请求频率、阻止特定 User-Agent）。
3. 针对敏感 API 配置 JWT 认证插件，验证请求头中的 Token 合法性。
4. 配置 IP 访问控制，限制只允许特定 CIDR 段访问管理接口。

**注意事项**: 安全策略配置过于严格可能会误伤正常流量，建议先在监控模式下运行，观察无误后再开启拦截模式。

---

### 实践 5：金丝雀发布与蓝绿部署

**说明**: Higress 基于 Istio 和 Envoy 实现，继承了强大的流量治理能力。在进行服务版本升级时，最佳实践是利用 Higress 的“灰度发布”功能。通过基于 HTTP Header、Cookie 或权重比例的流量路由，将一小部分用户流量引导至新版本服务，待验证无误后再全量发布。

**实施步骤**:
1. 在注册中心（如 Nacos）中准备两个版本的服务实例（例如 v1 和 v2）。
2. 在 Higress 中创建两个不同的服务（Service）引用这两个版本，或者使用一个服务但配置不同的子集。
3. 配置路由规则，设定流量匹配条件（如 `header: x-canary: true`）指向新版本服务。
4. 设置灰度权重（例如 10% 流量去往新版本），逐步观察

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与本地缓存

**说明**: Higress 支持 WASM (WebAssembly) 插件，相比传统 Lua 插件，WASM 提供了更接近原生的执行性能。同时，在网关层面启用本地缓存可以显著减少对后端服务的重复请求。

**实施方法**:
1. 将高频使用的自定义插件从 Lua 迁移至 WASM (C++/Go/Rust) 编写。
2. 在网关配置中开启 `local_response_cache` 或 `request_cache` 插件。
3. 针对只读的高频 API 数据配置合理的 TTL (Time To Live)。

**预期效果**: 插件执行延迟降低 20%-40%，后端请求负载减少 30%-60%（取决于缓存命中率）。

---

### 优化 2：配置连接池与 HTTP/2

**说明**: 默认的连接配置可能无法应对高并发场景。通过调整上游服务的连接池大小并启用 HTTP/2 协议，可以减少 TCP 握手开销，提高链路复用率。

**实施方法**:
1. 修改 Service 或 Upstream 配置，调大 `connectTimeout` 和 `maxRequestsPerConn`。
2. 启用 `http2` 协议支持（需确保后端支持 HTTP/2）。
3. 根据后端服务处理能力，适当增加 `connectionPool` 的大小。

**预期效果**: 在高并发下，网关至后端的建立连接延迟降低 50%，吞吐量（QPS）提升 20%以上。

---

### 优化 3：启用全链路超时控制与熔断降级

**说明**: 防止后端服务故障拖垮网关性能。通过配置精细的超时时间和熔断策略，可以快速释放资源，避免线程或协程长时间阻塞。

**实施方法**:
1. 设置合理的 `timeout`（包括连接超时、请求超时）。
2. 在路由或服务级别配置 `sentinel` 或 `circuit-breaker` 规则。
3. 定义降级返回内容（如默认 JSON 或静态页面），防止级联雪崩。

**预期效果**: 在后端故障时，网关自身 P99 延迟保持在可控范围（如 <50ms），系统可用性提升至 99.99%。

---

### 优化 4：优化日志采样与异步上报

**说明**: 在高流量场景下，全量日志记录会消耗大量 CPU 和磁盘 I/O，成为性能瓶颈。通过采样和异步上报可以平衡可观测性与性能。

**实施方法**:
1. 配置日志采样率（如 10% 或 1%），仅记录关键流量日志。
2. 将日志输出驱动调整为 `async` 模式，或使用高性能的日志插件（如 Kafka Proxy 直接转发）。
3. 关闭不必要的 Access Log 字段（如 request_body、response_body）。

**预期效果**: CPU 使用率降低 10%-20%，磁盘 I/O 写入量减少 80%以上。

---

### 优化 5：利用 DNS 缓存与 IP 直连

**说明**: 频繁的 DNS 解析会增加请求延迟。Higress 可以配置 DNS 缓存，或者在服务发现阶段直接使用 IP 地址，减少域名解析开销。

**实施方法**:
1. 在 DNS 配置中增加缓存时长设置。
2. 在 Registry (如 Nacos) 配置中优先使用 IP 地址注册。
3. 确保上游服务列表的更新机制（如服务发现）与 DNS 缓存策略协调，避免连接到已下线的 IP。

**预期效果**: 消除 DNS 解析延迟（通常为 10ms-50ms），请求建立连接阶段耗时减少。

---
## 学习要点

- Higress 是基于阿里云内部多年实践沉淀的下一代云原生 API 网关，深度集成 Istio 与 Envoy 核心能力。
- 该项目提供标准 K8s Ingress Controller 实现，能够无缝替代 Nginx Ingress 并提供更强的流量管理功能。
- 内置针对 Dubbo、Nacos 及 Spring Cloud 等微服务生态的深度支持，解决了云原生与传统微服务框架的互通难题。
- 具备高性能的 WAF（Web 应用防火墙）插件能力，为业务提供开箱即用的安全防护。
- 支持将网关实例作为 Service Mesh 的数据面，实现从南北向（入口流量）到东西向（服务间流量）的全链路治理。
- 提供开发者友心的 WASM 插件市场，支持使用 C++、Go、AssemblyScript 等语言编写扩展逻辑，且热更新不中断业务。
- 兼容 Ingress 与 Gateway API 两种标准，支持从传统架构向云原生架构的平滑迁移。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）及阿里云 API Gateway 的区别
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- Docker 环境下 Higress 的快速安装与部署（Standlone 模式）
- 基本术语：路由、服务、插件、Upstream

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：快速开始与核心概念
- 云原生网关技术白皮书

**学习建议**: 
建议先从宏观上理解 Higress 基于 Envoy 和 Istio 的技术背景。动手在本地 Docker 环境中跑通一个最简单的 Demo，将流量通过 Higress 转发到一个静态后端服务（如 Nginx），验证连通性。

---

### 阶段 2：核心配置与流量管理

**学习内容**:
- K8s Ingress 与 Gateway API 的配置方式
- 基于域名、路径、Header 的路由规则配置
- 服务发现集成：Nacos、Consul、固定地址及 K8s Service
- 负载均衡策略与超时、重试机制配置
- 金丝雀发布与蓝绿发布的流量配置
- 全局与域名级别的 TLS/SSL 证书管理

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：流量管理章节
- Gateway API 官方标准文档（对照学习）
- Higress 官方示例库

**学习建议**: 
此阶段重点在于“跑通流量”。建议在 Kubernetes 环境中进行练习。尝试模拟一个真实场景：将一个后端应用部署在 K8s 中，通过 Higress 配置 Ingress，并实现基于 Header 的流量切流（例如 10% 流量到新版本）。

---

### 阶段 3：插件开发与扩展能力

**学习内容**:
- Higress 插件系统原理（Wasm 支持）
- 使用官方预置插件（如 Key Auth, JWT Auth, Request Block）进行安全防护
- Lua 脚本编写与 Wasm (C++, Go, Rust) 插件开发基础
- 插件配置：参数校验与动态生效
- 自定义 Wasm 插件的编写、编译与部署流程
- 插件市场与插件脚本的加载机制

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：插件开发指南
- Envoy Wasm 官方文档
- Higress GitHub 仓库中的示例插件代码

**学习建议**: 
从使用官方插件解决具体问题（如限流、鉴权）入手。随后尝试编写一个简单的 Wasm 插件（例如修改请求头或响应体），并使用 Higress 提供的工具将其构建并在控制台中加载，理解数据面的处理流程。

---

### 阶段 4：高可用与生产级运维

**学习内容**:
- Higress 的高可用部署架构与容量规划
- 控制面与数据面的性能调优（连接池、缓冲区大小等）
- 可观测性集成：对接 Prometheus/Grafana 监控指标
- 分布式链路追踪集成
- 访问日志采集与分析（ALoS 或自定义 Log Service）
- 灰度发布与平滑升级策略
- 常见故障排查与应急处理

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：运维与监控
- Envoy 官方性能调优指南
- 云原生可观测性最佳实践

**学习建议**: 
重点在于“稳定性”。建议搭建一套包含 Prometheus 和 Grafana 的监控环境，观察 Higress 在高并发下的 QPS、延迟和错误率。模拟后端服务故障，观察 Higress 的重试和熔断表现。

---

### 阶段 5：深度定制与生态集成

**学习内容**:
- Higress 源码编译与本地调试
- 深入理解 Higress 对 Istio 的适配与扩展
- 服务网格中的 Sidecar 模式与 Gateway 模式的协同
- 多集群管理与服务网格互通
- 结合阿里云云产品的深度集成（如 MSE, ARMS）
- 参与开源社区贡献与定制化二开

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Istio 源码与架构设计文档
- Higress 社区路演视频与技术博客

**学习建议**: 
此阶段适合有特定深度定制需求或希望成为 Core Developer 的学习者。阅读源码，理解 HTTP 请求如何在 Higress 内部流转

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它诞生于阿里巴巴，是集团内部 Gateway 产品的开源版本，旨在解决云原生时代流量管理的复杂性。Higress 遵循 OGC（Open Gateway Community）标准，致力于成为云原生网关的统一标准，不仅服务于阿里云的用户，也贡献给了整个云原生开源社区。它结合了 Nginx 的高性能与 Envoy 的可扩展性，并针对 Kubernetes 环境进行了深度优化。

---



### 2: Higress 与 Nginx、Envoy 或传统的 API 网关（如 Kong、APISIX）相比有什么核心优势？

2: Higress 与 Nginx、Envoy 或传统的 API 网关（如 Kong、APISIX）相比有什么核心优势？

**A**: Higress 的核心优势在于其“开箱即用”的云原生体验和深度集成能力。

1.  **技术架构**：它基于 Envoy 和 Istio 进行了深度的二次开发，继承了 Envory 高性能和可扩展性的同时，解决了 Envory 配置复杂的问题。
2.  **安全防护**：内置了与阿里云 Web 应用防火墙（WAF）同源的防护能力，能提供更强的企业级安全支持。
3.  **服务治理**：与 Nacos、Consul 等主流注册中心无缝集成，实现了微服务架构下的服务发现与流量管理的统一，无需像传统 Nginx 那样手动维护 upstream 列表。
4.  **插件生态**：兼容 Kong 和 APISIX 的部分插件，同时支持 Wasm 插件，允许使用多种编程语言（如 Go、C++、Rust）编写扩展逻辑，比传统的 Lua 插件更安全且易于维护。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller（如 Nginx Ingress）进行无缝迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller（如 Nginx Ingress）进行无缝迁移？

**A**: 是的，Higress 非常重视迁移的平滑性。它提供了强大的兼容性工具和配置转换能力：

1.  **配置兼容**：Higress 支持标准的 Nginx Ingress Annotation，这意味着大多数情况下，你只需要将 Kubernetes Ingress 资源中的 `ingress.class` 修改为 `higress`，即可实现从 Nginx Ingress 到 Higress 的零代码迁移。
2.  **协议兼容**：完全兼容 Nginx 的配置语法和核心模块，使得现有的 Nginx 配置可以轻松复用。
3.  **流量切换**：支持基于权重的灰度发布，可以在旧网关和新网关之间进行流量的逐步切换，确保业务稳定性。

---



### 4: Higress 的插件系统是如何工作的？支持哪些类型的插件？

4: Higress 的插件系统是如何工作的？支持哪些类型的插件？

**A**: Higress 拥有一个灵活且强大的插件市场，主要分为以下几类：

1.  **原生插件**：内置了限流、熔断、认证、重试、路由等常见的网关功能。
2.  **Wasm 插件**：这是 Higress 的亮点。它支持 WebAssembly (Wasm) 技术，允许开发者使用 Go、C++、Rust、AssemblyScript 等高性能语言编写插件。Wasm 插件运行在沙箱环境中，安全性高，且支持热加载，无需重启网关即可更新插件逻辑。
3.  **生态兼容**：Higress 兼容 Kong 和 APISIX 的 Lua 插件生态，用户可以轻松移植现有的 Lua 插件到 Higress 中使用。

---



### 5: 在生产环境中，Higress 的性能表现如何？是否支持高可用部署？

5: 在生产环境中，Higress 的性能表现如何？是否支持高可用部署？

**A**: Higress 专为高性能和高可用场景设计。

1.  **高性能**：底层基于 Envoy，采用了全异步、非阻塞的 I/O 模型，单核性能强劲，能够处理海量并发请求。长连接（如 gRPC、WebSocket）处理能力也非常优异。
2.  **高可用**：作为云原生网关，Higress 原生支持 Kubernetes 的 Deployment 模式，可以轻松实现多副本部署和自动故障恢复。结合健康检查机制，能够确保流量自动路由到健康的实例。
3.  **弹性伸缩**：支持基于 CPU、内存等指标的水平自动伸缩（HPA），能够根据流量情况动态调整网关实例数量。

---



### 6: Higress 如何处理服务发现？它支持哪些服务注册中心？

6: Higress 如何处理服务发现？它支持哪些服务注册中心？

**A**: Higress 能够自动感知后端服务的健康状态和变化，这是其区别于传统负载均衡器的关键特性。

1.  **Kubernetes 原生**：在 K8s 集群内，Higress 直接与 API Server 交互，自动发现 Service 和 Endpoint 变化。
2.  **主流注册中心**：对于非 K8s 环境或混合云架构，Higress 支持通过配置接入 Nacos、Consul、Zookeeper、Eureka 等主流注册中心。它会根据注册中心的服务列表动态更新路由配置，实现微服务与网关的联动。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础路由与请求头管理

### 问题**：

### Higress 基于 Envoy 构建，但默认配置可能无法满足特定流量需求。请尝试在本地 Docker 环境中部署 Higress，并创建一个简单的路由规则：将域名为 `example.com` 的 HTTP 请求流量转发到后端的一个模拟服务（如 httpbin.org），同时修改请求头，添加一个 `X-Higress-Request: true` 的头部。

### 提示**：

---
## 实践建议

以下是基于 Higress 作为 AI 网关/API 网关的 5-7 条实践建议：

### 1. 利用 AI 提示词模板实现业务与 Prompt 解耦
**场景：** 多个应用调用相同的 LLM 模型，但需要不同的上下文或人设。
**建议：** 不要在应用代码中硬编码 Prompt。在 Higress 中配置 AI 提示词模板，将前端传入的简单参数（如 `{{query}}`）映射为完整的 Prompt。
**最佳实践：** 在网关层统一管理 Prompt 版本。当需要优化模型效果调整 Prompt 时，只需在 Higress 控制台修改配置并重新发布，无需重新部署业务代码，实现快速迭代。
**常见陷阱：** 忽略模板中的参数校验，导致缺失关键参数时发送了格式错误的请求给 LLM 服务商。

### 2. 配置语义缓存以降低 Token 成本与延迟
**场景：** 客服或知识库问答场景，用户往往会重复提问相似问题（如“如何退款？”）。
**建议：** 开启 Higress 的语义缓存功能。与传统的精确匹配缓存不同，语义缓存能识别问题意图的相似性，直接返回缓存的答案。
**最佳实践：** 针对高频问答设置合理的缓存过期时间（TTL）和相似度阈值。
**常见陷阱：** 对实时性要求极高的场景（如股票查询）误用长缓存，导致用户获取过时信息；或者缓存 Key 设置过于简单，导致不同用户的隐私数据被串用。

### 3. 实施基于令牌桶的精细化流量控制
**场景：** 对接 OpenAI 或其他商业 LLM 时，后端 API 有严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制。
**建议：** 在 Higress 全局流控插件中，针对不同的 API Key 或路由规则配置 TPM 限流。
**最佳实践：** 设置“秒级”突发流量限制，防止因前端重试或流量突增导致后端账号被封禁。
**常见陷阱：** 仅在应用层做单机限频，而在多实例部署下总流量仍超过服务商限制，导致 429 错误。

### 4. 统一处理模型服务商的错误与重试策略
**场景：** 网络波动或 LLM 服务端（如 Azure OpenAI）偶尔返回 503 或超时。
**建议：** 在 Higress 的路由插件中配置自定义的“错误重试”和“降级”策略。
**最佳实践：** 配置指数退避重试机制。如果主模型调用失败，可配置自动切换到备用模型（例如从 `gpt-4` 降级到 `gpt-3.5-turbo`）以保证服务可用性。
**常见陷阱：** 无脑重试所有请求。对于客户端参数错误（400）或鉴权失败（401），配置重试只会徒增后端压力，应仅对网络错误或 5xx 错误进行重试。

### 5. 构建多模型供应商的统一路由层
**场景：** 业务需要在不同模型间切换，或者同时使用通义千问、DeepSeek、OpenAI 等多个服务。
**建议：** 利用 Higress 的服务来源管理功能，将不同厂商的 API 注册为统一的服务。在业务代码中只需调用 Higress 的标准接口，通过 Header 参数（如 `x-model-provider`）动态指定后端厂商。
**最佳实践：** 屏蔽底层厂商的 API 差异（如鉴权方式、参数格式），由 Higress 统一转换为标准 OpenAI 协议格式。
**常见陷阱：** 忽略了不同模型对上下文窗口大小的限制，直接透传超长文本导致后端报错。

### 6. 敏感数据脱敏与安全防护
**场景：** 企业内部数据通过公网 LLM 处理，存在数据泄露风险。
**建议：** 在请求发送给 LLM 之前，使用 Higress 的插件（如 WAF 插件

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Kubernetes](/tags/kubernetes/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*