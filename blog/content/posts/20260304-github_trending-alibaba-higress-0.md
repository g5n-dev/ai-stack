---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-04T18:13:15+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "云原生", "Istio", "Envoy", "WASM", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的、基于云原生架构的**AI 原生 API 网关**。以下是该项目的核心总结： 1. 项目定位 Higress 是建立在 **Istio** 和 **Envoy** 之上的云原生 API 网关。它通过扩展 **WebAssembly (WASM)** 插件能力，实现了控制平面（配置管理）"
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
- **星标**: 7,636 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它将云原生流量管理与大模型应用需求相结合。该项目不仅提供传统的微服务路由与 Kubernetes Ingress 管理，还针对 LLM 应用内置了 AI 网关特性及 MCP 服务器托管能力。本文将介绍其系统架构与核心组件，并重点解析 WASM 插件体系及 AI 网关的具体功能。

---
## 摘要

Higress 是由阿里巴巴开源的、基于云原生架构的**AI 原生 API 网关**。以下是该项目的核心总结：

### 1. 项目定位
Higress 是建立在 **Istio** 和 **Envoy** 之上的云原生 API 网关。它通过扩展 **WebAssembly (WASM)** 插件能力，实现了控制平面（配置管理）与数据平面（流量处理）的分离。其架构优势在于配置变更可通过 xDS 协议在毫秒级内生效，且无连接中断，特别适配 AI 长连接流式响应场景。

### 2. 核心功能
Higress 提供以下三大核心功能：
*   **AI 网关：** 为大语言模型（LLM）应用提供统一 API。它集成了 30 多个 LLM 提供商，支持协议转换、可观测性、缓存以及安全防护。
*   **MCP 服务器托管：** 托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
*   **传统 API 网关：** 兼容 Kubernetes Ingress，支持微服务路由，并兼容 nginx-ingress 注解。

### 3. 技术与生态
*   **编程语言：** Go
*   **架构特点：** 云原生、基于 Envoy/Istio、支持 WASM 插件扩展。
*   **热门程度：** 截至当前，GitHub 星标数超过 7,600。

### 4. 主要应用场景与组件
| 应用场景 | 描述 | 核心组件 |
| :--- | :--- | :--- |
| **AI 网关** | 统一 30+ LLM 提供商 API，含协议转换、监控、缓存及安全 | `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 插件 |
| **MCP 服务器托管** | 允许 AI 智能体通过 MCP 协议调用工具和服务 | `mcp-router`, `jsonrpc-converter` 过滤器及相关服务器实现 |
| **Kubernetes Ingress** | 作为 Ingress 控制器，兼容 nginx 注解 | `higress-controller` |

---
## 评论

### 总体评价

Higress 是阿里云开源的**下一代“AI 原生”网关**，它不仅继承了基于 Istio 和 Envoy 的云原生流量管理基因，更通过深度集成 LLM 处理、MCP 协议支持及 WASM 插件市场，成功打破了传统 API 网关与 AI 应用基础设施之间的界限。**它是目前将云原生网关稳定性与大模型应用生态融合得最彻底的工业级项目之一。**

---

### 深入分析

#### 1. 技术创新性：从“流量管道”到“AI 智能体”
*   **事实**：DeepWiki 明确指出 Higress 扩展了 Envoy，引入了 **WebAssembly (WASM)** 插件能力，并提供了 **AI Gateway 功能**（如 LLM 应用处理）和 **MCP 服务器托管**（用于 AI Agent 工具集成）。
*   **推断**：Higress 的最大创新在于**“网关即 AI 编排层”**。传统网关只做七层负载均衡，而 Higress 直接在网关层处理 AI 的特殊性。例如，利用 WASM 的高性能沙箱，开发者可以用 C++/Go/Rust 编写插件来拦截 Prompt，实现敏感词过滤、计费统计，甚至基于语义的缓存，而无需修改后端应用代码。支持 MCP (Model Context Protocol) 协议更是极具前瞻性，这意味着 Higress 可以直接作为 LLM 与外部数据/工具（如数据库、企业 API）之间的标准化连接器，解决了 AI Agent 落地中“工具接入复杂”的痛点。

#### 2. 实用价值：统一微服务与 AI 流量入口
*   **事实**：文档描述其核心功能包括“Kubernetes Ingress”、“微服务路由”以及“AI Gateway”。
*   **推断**：在“AI 重塑应用”的当下，企业往往面临两套网关：一套管微服务（如 K8s Ingress），一套管大模型调用。Higress 提供了**统一入口**，极大地降低了运维复杂度。对于开发者而言，其价值在于**AI 请求的标准化处理**：它可以将不同 LLM 厂商（OpenAI, 通义千问, 文心一言等）的异构 API 统一转换为标准格式，使得应用层可以轻松切换模型供应商，避免 Vendor Lock-in（供应商锁定）。这对构建多模型策略的企业至关重要。

#### 3. 代码质量与架构：云原生工业级的典范
*   **事实**：项目基于 Go 语言编写，构建于 Istio 和 Envoy 之上，架构明确分离了**控制面**与**数据面**。
*   **推断**：基于 Istio/Envoy 意味着它继承了**极高的数据平面性能**和**标准化的控制面 API**。Go 语言的使用保证了控制面在处理高并发配置下发时的效率。架构上，将配置管理与流量处理分离，符合云原生设计的最佳实践，保证了系统的可扩展性和稳定性。作为阿里系开源项目，其代码规范性和工程成熟度通常较高，能够经受大规模流量的考验。

#### 4. 社区活跃度：阿里背书与生态共建
*   **事实**：星标数达到 7,636（且在持续增长），提供中、日、英多语言文档，拥有详细的开发指南和 WASM 插件系统说明。
*   **推断**：高星标数和阿里云的背书证明了该项目并非“玩具级”产品。多语言文档显示了其国际化的野心和对社区的重视。活跃的社区不仅意味着 Bug 修复快，更意味着**丰富的插件生态**。对于 WASM 插件的支持，鼓励了开发者贡献自定义逻辑，这种“平台+插件”的模式极易形成正向循环的社区生态。

#### 5. 学习价值：深入理解云原生与 AI 基础设施
*   **推断**：对于开发者，Higress 是学习**“云原生网关如何处理 AI 流量”**的最佳范例。
    *   **架构视角**：可以学习如何通过 Envoy Filter 扩展功能，以及如何设计控制面来驱动 Envoy 配置（xDS 协议）。
    *   **AI 视角**：可以研究如何在网关层实现 Token 计费、流式传输（SSE）处理以及 Prompt 模板管理。
    *   **WASM 视角**：它是学习如何使用 WASM 技术为 Go/C++ 系统实现热插拔逻辑的优秀参考。

#### 6. 潜在问题与改进建议
*   **复杂度门槛**：虽然提供了 Docker 镜像，但深度定制通常需要理解 Istio 和 Envoy 的复杂概念，对中小团队的学习曲线较陡峭。
*   **AI 功能的成熟度**：作为较新的 AI 网关，相比传统的 API 网关功能，其 AI 特性（如复杂的 RAG 编排、高级 Token 限流算法）可能仍在快速迭代中，文档的细节覆盖度有时可能滞后于代码更新。
*   **建议**：建议官方提供更多针对 AI 场景的“开箱即用”配置模板（如“给通义千问加一个简单的缓存”的完整 YAML 示例），而不仅仅是架构文档。

#### 7. 对比优势：Higress vs. Kong/APISIX vs. 专用 AI Proxy
*   **对比传统网关**：相比 Kong 或 APIS

---
## 技术分析

基于您提供的 GitHub 仓库信息（alibaba/higress）以及对该项目技术栈和背景的深入理解，以下是对 Higress 的全面技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 架构模式与技术栈
Higress 的核心定位是**云原生 API 网关**，其架构设计深刻体现了“控制平面与数据平面分离”的云原生设计理念。

*   **底层基石**：构建于 **Envoy** 之上。Envoy 是高性能的 C++ 边缘代理，负责处理底层的网络连接、流量转发、TLS 卸载等重 I/O 操作。
*   **控制平面**：深度集成 **Istio**。Higress 复用了 Istio 的控制平面能力（如 Istiod），通过 xDS 协议（包括 LDS, CDS, RDS, EDS）将配置下发到数据平面。这意味着它天然支持 Kubernetes 的服务发现和流量管理规范。
*   **扩展层**：引入 **WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型之一。通过 WASM，它允许开发者使用 C/C++、Go、Rust、JavaScript 等高级语言编写插件，这些插件会被编译成 WASM 字节码并在 Envoy 的沙箱中运行。
*   **编程语言**：**Go**。Higress 的控制平面和配套工具主要由 Go 语言编写，利用 Go 优秀的并发处理模型和丰富的云原生生态库。

### 核心模块设计
1.  **路由与流量管理**：基于 Envoy 的高性能路由匹配，支持 HTTP/gRPC/Dubbo 等多协议。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时（如 Wasmtime 或 V8），实现插件的热加载和动态执行，无需重启网关即可更新业务逻辑。
3.  **配置分发系统**：优化了 Istio 的配置下发机制，实现了毫秒级的配置推送延迟，这对于 AI 流式响应等长连接场景至关重要。

### 架构优势分析
*   **极致性能**：数据平面基于 Envoy (C++)，避免了纯 Java 网关（如 Zuul 1.x）的线程上下文切换开销，能够应对极高的并发吞吐量。
*   **安全隔离**：WASM 插件运行在资源受限的沙箱中，即使插件崩溃也不会导致网关主进程崩溃，且内存隔离性优于传统的 Lua 脚本（如 OpenResty）。
*   **云原生亲和**：作为 Ingress Controller 或 API Gateway 运行在 K8s 中，直接消费 K8s CRD 资源，运维成本低。

---

## 2. 核心功能详细解读

### AI Gateway (AI 原生网关)
这是 Higress 最具差异化的功能点。随着大语言模型（LLM）的爆发，传统的 API 网关无法处理 AI 流量的特殊需求。
*   **解决的问题**：
    *   **Token 计费与限流**：传统网关基于请求数或连接数限流，而 AI 应用基于 Token 计费。Higress 支持基于 Token 的精细化流控。
    *   **提示词管理**：在网关层进行 Prompt 的注入、转换和脱敏，避免后端服务直接暴露敏感 Prompt。
    *   **模型供应商切换**：作为统一入口，支持将请求路由到 OpenAI、通义千问、Llama 等不同供应商，实现解耦。
*   **技术实现**：通过解析 HTTP 流量（通常是 SSE 或 Chunked Transfer），在流式传输过程中进行协议转换和上下文处理。

### MCP (Model Context Protocol) Server Hosting
Higress 能够托管 MCP Server。
*   **解决的问题**：AI Agent 需要调用外部工具。MCP 是一种标准化协议。Higress 允许网关直接作为这些工具的托管点，简化了 Agent 与工具集成的复杂度，使得网关成为 AI 能力的“调度中心”。

### 传统 API 网关能力
*   **全生命周期管理**：认证鉴权（OIDC, API Key）、流量染色、灰度发布（金丝雀发布）、熔断降级。
*   **服务治理**：集成 Nacos、Consul 等注册中心，实现微服务间的自动发现。

### 与同类工具对比
*   **对比 Nginx/OpenResty**：Higress 具备更强大的动态配置能力（无需 Reload 进程）和更现代的编程模型（WASM vs Lua），且 K8s 集成度更高。
*   **对比 Kong**：Kong 基于 Nginx/OpenResty + PostgreSQL，配置依赖数据库。Higress 基于 Envoy + K8s CRD，配置下发更轻量，延迟更低，且 WASM 的安全性优于 Kong 的 Lua 插件。
*   **对比 APISIX**：两者架构类似（均基于 Envoy/Lua 或 WASM），但 Higress 背靠阿里云，对 AI 场景的支持（如 SSE 流处理、Token 统计）更为原生和深入。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件机制**：
    *   **Proxy-WASM 规范**：遵循 Proxy-WASM ABI 标准。
    *   **多语言支持**：通过 `wasm-go` 等工具链，允许开发者用 Go 编写插件，编译为 WASM。这解决了 C++ 插件开发门槛高、Lua 插件性能差且难以调试的问题。
2.  **配置热更新**：
    *   利用 Istio 的 xDS (v2/v3) 协议。控制平面监听 K8s API Server 的变化，将其转换为 Envoy 配置，通过 gRPC 推送给数据平面。
    *   **增量推送**：优化了全量推送机制，仅推送变更的路由配置，减少网关节点的 CPU 和内存抖动。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器、路由匹配逻辑、Dubbo 协议处理等。
*   **`plugins/`**：内置 WASM 插件的源码，如 `key-auth`、`request-block` 等。
*   **`installer/`**：Helm Charts 包，定义了 K8s 上的部署结构。

### 性能优化与扩展性
*   **零拷贝**：Envoy 底层处理网络包时尽量减少内存拷贝。
*   **异步 I/O**：全异步非阻塞模型。
*   **水平扩展**：数据平面无状态，可通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU/内存指标自动扩缩容。

---

## 4. 适用场景分析

### 最适合的场景
1.  **AI 应用中间层**：企业构建基于 LLM 的应用时，使用 Higress 作为统一网关，处理 Prompt 增强、Token 鉴权、多模型路由。
2.  **Kubernetes 集群入口**：作为云原生架构的 Ingress Controller，替代传统的 Nginx Ingress，获得更强的流量治理能力。
3.  **微服务 API 治理**：需要复杂的流量控制（如按 Header 灰度、全链路灰度）和 WAF 防护的场景。
4.  **多协议混合**：系统内部同时存在 HTTP (RESTful)、gRPC、Dubbo 协议，需要统一网关进行协议转换和路由。

### 不适合的场景
1.  **边缘计算/极低资源环境**：Envoy + WASM 的资源开销（内存）相对较高，不如纯 Nginx 或轻量级边缘代理适合资源受限的 IoT 设备。
2.  **简单的静态文件托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更简单直接。
3.  **非 K8s 环境的强依赖**：虽然支持 Linux 二进制部署，但其最大威力在 K8s 环境，在传统虚拟机环境中部署复杂度较高。

### 集成方式
主要通过 **Helm** 在 Kubernetes 集群中部署。配置通过 K8s CRD (如 `Ingress`, `Gateway`, `WasmPlugin`) 进行管理。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **AI Native 深化**：从简单的透传转向“理解”内容。未来可能集成向量检索、RAG (检索增强生成) 的网关层实现，直接在网关层完成部分知识库查询。
2.  **WASM 生态标准化**：随着 WASM 组件模型的成熟，Higress 可能会支持更复杂的插件间通信，甚至插件间直接共享内存（在安全沙箱内）。
3.  **服务网格融合**：虽然目前定位是网关，但与 Sidecar 模式的界限可能进一步模糊，形成“单栈”架构（即同时作为 Gateway 和 Mesh 数据平面）。

### 社区与改进
*   **插件市场**：Higress 正在构建官方插件市场，降低用户编写代码的门槛，通过 UI 配置即可使用常见功能。
*   **可观测性**：未来将更深度集成 OpenTelemetry，提供针对 AI 流量（Token 消耗、模型响应时间）的专属看板。

---

## 6. 学习建议

### 适合的开发者
*   **云原生运维工程师** (SRE)：需要掌握 K8s 和 Helm。
*   **后端开发/架构师**：希望理解流量治理和 AI 基础设施。
*   **Go 语言爱好者**：希望学习如何用 Go 构建大规模分布式控制系统。

### 学习路径
1.  **基础理论**：理解 Envoy 的 xDS 协议和 Istio 的基本原理。
2.  **动手实践**：使用 Kind (Kubernetes in Docker) 在本地搭建 Higress，部署一个示例应用，配置路由。
3.  **插件开发**：尝试使用 Go 编写一个简单的 WASM 插件（例如修改请求头），并在 Higress 中加载。
4.  **AI 场景实验**：配置 Higress 连接 OpenAI API，体验 SSE 流式转发和 Token 统计功能。

### 实践建议
*   阅读 `README_ZH.md`（中文文档）。
*   源码阅读建议从 `pkg/config` 和 `ingress` 核心包入手，理解 K8s 资源如何转化为 Envoy 配置。

---

## 7. 最佳实践建议

### 正确使用指南
1.  **资源规划**：WASM 插件运行需要内存，务必为 Higress 的 Pod 设置合理的 `limits` 和 `requests`，防止插件 OOM 导致网关重启。
2.  **插件隔离**：对于高风险或消耗资源的插件（如 AI 推理预处理），建议在独立的 Wasm VM 实例中运行，或使用 Higress 的插件优先级机制，防止阻塞主流程。
3.  **配置版本管理**：所有的网关配置应纳入 GitOps 流程（如使用 ArgoCD），避免直接在控制台手动修改导致配置漂移。

### 常见问题与解决
*   **长连接超时**

---
## 代码示例




```python
# 示例1：使用Higress实现基于路径的路由转发
from higress import Gateway, Route, Service

def setup_path_based_routing():
    # 创建Higress网关实例
    gateway = Gateway(name="api-gateway")
    
    # 定义后端服务
    user_service = Service(name="user-service", url="http://user-service:8080")
    order_service = Service(name="order-service", url="http://order-service:8080")
    
    # 配置路径路由规则
    gateway.add_route(Route(
        path="/api/users/*",
        service=user_service,
        methods=["GET", "POST"]
    ))
    
    gateway.add_route(Route(
        path="/api/orders/*",
        service=order_service,
        methods=["GET", "POST"]
    ))
    
    # 应用配置
    gateway.apply()
    print("路由配置已应用：/api/users/* -> user-service, /api/orders/* -> order-service")

setup_path_based_routing()
```




```python
# 示例2：实现请求流量控制（限流）
from higress import Gateway, RateLimitRule

def setup_rate_limiting():
    gateway = Gateway(name="api-gateway")
    
    # 配置限流规则：每分钟最多100次请求
    rate_limit = RateLimitRule(
        path="/api/v1/*",
        requests_per_minute=100,
        burst=10  # 允许短时突发10个请求
    )
    
    gateway.add_rate_limit(rate_limit)
    gateway.apply()
    print("限流规则已应用：/api/v1/* 路径每分钟最多100次请求")

setup_rate_limiting()
```




```python
# 示例3：配置JWT认证中间件
from higress import Gateway, JwtAuth

def setup_jwt_auth():
    gateway = Gateway(name="api-gateway")
    
    # 配置JWT认证
    jwt_auth = JwtAuth(
        path="/api/secure/*",
        secret_key="your-secret-key",  # 实际使用中应从安全配置中获取
        algorithm="HS256",
        token_header="Authorization",
        token_prefix="Bearer "
    )
    
    gateway.add_auth_middleware(jwt_auth)
    gateway.apply()
    print("JWT认证已配置：/api/secure/* 路径需要有效JWT令牌")

setup_jwt_auth()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴的电商业务（如淘宝、天猫）拥有极高的并发流量，尤其是在“双11”等大促期间，流量峰值可达每秒百万级请求。原有的 API 网关架构在应对大规模微服务调用时，面临配置管理复杂和性能瓶颈的挑战。

**问题**: 随着微服务数量爆炸式增长，基于传统网关的架构出现了以下痛点：1. 路由规则管理复杂，难以支持动态变更；2. 网关与 K8s Ingress 控制器功能割裂，导致维护成本高；3. 在处理高并发流量时，延迟和资源消耗难以优化。

**解决方案**: 阿里巴巴基于内部多年的网关经验，开源了 Higress。Higress 是一个云原生 API 网关，深度集成了 Envoy 和 Istio，实现了 Ingress 与网关的合一。它通过标准化的 WASM 插件机制，允许业务方灵活扩展功能，同时利用 Envoy 的高性能数据处理能力应对高并发。

**效果**: 1. 成功支撑了阿里巴巴内部核心电商链路的高并发流量，P99 延迟显著降低；2. 统一了流量入口管理，将网关与 K8s Ingress 控制器合并，大幅降低了运维复杂度；3. 通过开源生态，让外部企业也能复用阿里经过实战验证的网关技术。

---



### 2：某互联网科技公司微服务治理

 2：某互联网科技公司微服务治理

**背景**: 该公司业务全面云原生化，运行在 Kubernetes 集群之上。随着业务发展，微服务拆分粒度越来越细，服务间调用关系错综复杂。此前使用的是传统的 Nginx Ingress Controller，主要用于简单的南北向流量管理。

**问题**: 随着业务需求升级，团队面临以下问题：1. 传统的 Nginx 配置缺乏动态性，修改路由规则需要 Reload，影响业务连续性；2. 缺乏对 gRPC、Dubbo 等多协议的统一支持；3. 需要更精细化的流量治理（如金丝雀发布、全链路灰度），但现有方案实现成本极高。

**解决方案**: 团队将流量入口迁移至 Higress。利用 Higress 对 Istio 的集成能力，实现了东西向（服务间）和南北向（入口）流量的统一治理。通过 Higress 提供的控制台，运维人员可以直观地配置服务路由、权重分流和流量镜像，无需手动修改复杂的配置文件。

**效果**: 1. 实现了配置热更新，业务变更无需重启网关，服务稳定性提升；2. 统一支持了 HTTP、gRPC 和 Dubbo 协议，简化了技术栈；3. 极大地简化了全链路灰度发布的流程，新版本上线效率提升 50% 以上，且故障回滚更加迅速安全。

---



### 3：AI 应用服务的高并发接入

 3：AI 应用服务的高并发接入

**背景**: 一家专注于 AI 大模型应用开发的创业公司，需要将其部署在 K8s 上的 LLM（大语言模型）服务通过 API 暴露给外部用户。AI 应用通常对请求的上下文管理和 Token 计费有强依赖，且推理服务响应时间较长，容易导致连接拥塞。

**问题**: 使用通用的 API 网关无法满足 AI 领域的特殊需求：1. 无法识别语义层面的 Token 统计，难以实现基于 Token 的精确限流和计费；2. 在处理流式输出（SSE）时，通用网关性能不佳，容易造成内存堆积；3. 需要针对不同模型版本进行 A/B 测试，但传统网关对复杂负载均衡支持有限。

**解决方案**: 该公司采用了 Higress，并利用其 WASM (WebAssembly) 插件市场中的 AI 扩展能力。通过编写轻量级的 WASM 插件，在网关层实现了对请求体的解析，提取 Prompt 并进行 Token 预估和计费。同时，利用 Higress 对 SSE 协议的高性能转发能力，优化了流式响应体验。

**效果**: 1. 实现了毫秒级的 Token 统计和基于业务逻辑的精准限流，保护了后端昂贵的 GPU 资源；2. 流式响应的转发效率大幅提升，端到端延迟降低，用户体验更加流畅；3. 利用 Higress 的路由标签功能，轻松实现了不同模型版本之间的流量切换，加速了模型迭代验证过程。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|--------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和OpenResty | 极高性能，基于Lua和OpenResty |
| 易用性 | 提供可视化控制台，支持Kubernetes集成 | 配置灵活但需手动管理较多 | 提供Dashboard，配置相对简单 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 完全开源免费 |
| 扩展性 | 支持插件扩展，兼容Istio生态 | 支持插件扩展，社区丰富 | 支持Lua插件扩展，灵活性强 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 国产开源，社区活跃 |
| 功能特性 | 支持流量管理、安全防护、可观测性 | 功能全面，支持API网关和微服务 | 功能全面，支持动态路由和限流熔断 |

### 优势分析

- 优势1：基于Envoy和Istio，天然支持云原生和微服务架构。
- 优势2：提供可视化控制台，降低运维复杂度。
- 优势3：阿里背书，企业级支持和稳定性有保障。

### 不足分析

- 不足1：相比Kong和APISIX，社区生态和插件数量较少。
- 不足2：企业版功能需付费，成本较高。
- 不足3：对非Kubernetes环境的支持相对较弱。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 架构的高性能网关部署

**说明**: Higress 基于 Envoy 和 Istio 构建，利用其高性能的数据平面处理能力。在生产环境中，应充分利用其非阻塞 I/O 和多线程架构来处理高并发流量，避免传统阻塞式网关的性能瓶颈。

**实施步骤**:
1. 确保部署环境满足资源要求（CPU、内存），建议使用 Kubernetes 部署以获得弹性伸缩能力。
2. 配置合适的 Envoy 线程数，通常设置为与 CPU 核心数相等，以最大化资源利用率。
3. 启用 HTTP/2 或 HTTP/3 (QUIC) 协议支持，提升客户端与服务端之间的通信效率。

**注意事项**: 监控 Envoy 的 Worker 线程状态，避免因单线程过载导致的延迟增加。

---

### 实践 2：精细化流量管理与路由规则配置

**说明**: 利用 Higress 强大的路由能力实现灰度发布、蓝绿部署或 A/B 测试。通过 Header、Cookie 或 URL 参数进行流量分流，确保新版本上线的平滑过渡。

**实施步骤**:
1. 在控制台或通过 Ingress 配置定义路由规则，设置匹配条件（如 `x-canary: true`）。
2. 配置多版本服务权重，逐步将流量从旧版本切换到新版本。
3. 设置超时和重试策略，防止部分实例故障导致整体请求失败。

**注意事项**: 在生产环境发布前，务必在测试环境验证路由规则的匹配优先级，避免流量路由错误。

---

### 实践 3：全面的安全防护与插件体系应用

**说明**: Higress 提供了丰富的 WAF 能力和插件市场。应启用基本的安全防护措施，如 IP 黑白名单、请求限流以及 JWT 认证，以保护后端服务免受恶意攻击。

**实施步骤**:
1. 安装并启用 `key-auth` 或 `jwt-auth` 插件，对 API 接口进行身份验证。
2. 配置 `request-block` 或 `request-limit` 插件，限制单个 IP 的请求频率（QPS）。
3. 开启 CORS（跨域资源共享）配置，严格控制允许访问的来源。

**注意事项**: 限流阈值应根据实际业务容量进行压测后设定，防止误杀正常流量。

---

### 实践 4：服务注册与发现的动态集成

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 等注册中心。实现网关与服务注册中心的深度集成，可以实现自动的服务发现和健康检查，减少手动配置维护成本。

**实施步骤**:
1. 在 Higress 配置中添加对应类型的注册中心（如 Nacos）地址和命名空间。
2. 配置服务来源，将微服务应用接入 Higress。
3. 验证服务列表是否自动同步，并测试服务下线时网关是否自动摘除故障节点。

**注意事项**: 确保网关与注册中心之间的网络连通性，避免因网络抖动导致服务列表不一致。

---

### 实践 5：可观测性与监控告警建设

**说明**: 建立全面的监控体系，对接 Prometheus、Grafana 或阿里云 ARMS。通过监控黄金指标（延迟、流量、错误率、饱和度）来快速定位系统瓶颈和异常。

**实施步骤**:
1. 开启 Higress 的 Prometheus 访问入口，配置 ServiceMonitor 或抓取规则。
2. 导入官方提供的 Grafana Dashboard 模板，可视化网关性能数据。
3. 配置告警规则（如 P99 延迟超过 500ms 或 5xx 错误率超过 1%），并接入钉钉或企业微信通知。

**注意事项**: 日志采集（Access Log）会产生较大的性能开销和存储成本，建议在生产环境按需开启或采样记录。

---

### 实践 6：使用 WASM 技术扩展网关功能

**说明**: Higress 支持 WebAssembly (WASM) 插件，允许使用 C++、Go、Rust 或 AssemblyScript 编写高性能的自定义扩展逻辑，而无需修改网关核心代码或重启网关。

**实施步骤**:
1. 根据业务需求编写 WASM 插件逻辑（例如自定义请求头修改、复杂鉴权逻辑）。
2. 将编译好的 `.wasm` 文件上传至 Higress 或配置 OCI 远程加载。
3. 在网关控制台启用该插件，并配置相应的路由作用域。

**注意事项**: WASM 插件虽然隔离性好，但频繁的内存分配或复杂计算仍会增加请求延迟，需优化插件代码性能。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，支持 HTTP/3 可以显著减少连接建立延迟，特别是在高丢包率的弱网环境下。通过在 Higress 网关层面开启 QUIC 协议，可以利用 UDP 的多路复用能力，解决 TCP 队头阻塞问题，从而提升首包加载速度和并发处理能力。

**实施方法**:
1. 在 Higress 的网关配置中，找到监听器协议设置。
2. 启用 HTTP/3 或 QUIC 协议支持（需确保底层网络环境允许 UDP 流量）。
3. 配置证书以支持 QUIC 的 TLS 握手（通常复用 HTTPS 证书）。
4. 开启 0-RTT (Zero Round Trip Time) 恢复功能以进一步减少握手延迟。

**预期效果**: 在弱网环境下，首字节延迟（TTFB）降低约 30%-50%，连接建立成功率显著提升。

---

### 优化 2：配置全局限流与熔断策略

**说明**: 防止后端服务因突发流量导致雪崩效应。Higress 继承了 Istio 的流量管理能力，通过精细化的限流配置，可以保护后端服务不被压垮。同时，配置熔断器可以在检测到后端服务响应时间过长或错误率过高时，快速失败，避免请求堆积在网关层消耗线程资源。

**实施方法**:
1. 使用 Higress 的 `RequestLimit` 或 `GlobalRateLimit` 插件，基于 IP、API Key 或 Header 设置 QPS 阈值。
2. 在 `VirtualService` 或 `Gateway` 配置中定义 `OutlierDetection`（异常值检测），设置连续 5xx 错误的数量阈值。
3. 配置 `CircuitBreaker`（熔断器），限制并发连接数和最大请求数。
4. 针对关键接口配置“排队”策略，在限流时允许一定数量的请求排队等待而非直接拒绝。

**预期效果**: 将后端服务的 P99 延迟波动降低 20% 以上，系统在高负载下的可用性提升至 99.9% 以上。

---

### 优化 3：利用本地缓存减少回源请求

**说明**: 对于读多写少或对实时性要求不极高的 API（如商品详情、配置信息），在 Higress 网关层启用本地缓存可以大幅减少对后端服务的请求压力。Higress 支持基于内存的本地缓存，能够以极低的延迟响应请求。

**实施方法**:
1. 启用 Higress 的 `local-response-cache` 或类似功能的插件。
2. 配置缓存 Key 的生成规则（通常基于 URL Path 或指定的 Header）。
3. 设置合理的 TTL（生存时间）和最大缓存体大小。
4. 对于需要鉴权的接口，配置缓存 Key 包含用户标识，防止数据泄露。

**预期效果**: 缓存命中时，API 响应延迟降低至 1ms-5ms 级别，后端服务负载降低 30%-60%（视业务读多写少程度而定）。

---

### 优化 4：优化 WAF 规则与安全插件执行顺序

**说明**: Higress 内置了 WAF（Web 应用防火墙）功能。如果安全规则过于复杂或执行顺序不当，会显著增加请求处理的 CPU 消耗和延迟。通过优化正则表达式、减少不必要的检查项以及调整插件执行链，可以在保持安全性的同时提升吞吐量。

**实施方法**:
1. 审计当前的 WAF 规则，移除冗余或过时的规则。
2. 优化正则表达式，避免使用回溯风险极高的复杂正则。
3. 调整插件执行顺序：将“快速失败”的插件（如 IP 黑名单、静态限流）放在前面，将消耗资源较多的插件（如深度包检测）放在后面。
4. 在生产环境压测中，逐步开启严格模式以平衡安全与性能。

**

---
## 学习要点

- Higress 是阿里云开源的基于 Istio 的下一代云原生 API 网关，深度集成 Envoy 和 K8s，提供高性能流量管理能力。
- 它支持将 Ingress 与 Gateway API 统一管理，实现从传统微服务到云原生架构的无缝迁移。
- 内置 WAF 插件与安全防护机制，能够有效抵御常见的 Web 攻击并保障 API 通信安全。
- 提供标准化的 Wasm 插件扩展机制，支持使用 Go 或 C++ 编写自定义逻辑，业务处理灵活度极高。
- 兼容 Kubernetes Ingress 与 Nginx 注解配置，大幅降低了用户从传统网关迁移的技术门槛。
- 具备完善的流量治理与服务编排功能，支持金丝雀发布、蓝绿部署及负载均衡策略。
- 提供开箱即用的 Prometheus 监控集成与 Grafana 仪表盘，便于实时观测网关运行状态与性能指标。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）以及阿里云 API 网关的区别
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 基础环境搭建：Docker/Docker Compose 本地部署或 Kubernetes 集群部署
- 控制台（Console）的基本操作与界面熟悉

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 (README.md)
- Higress 官方文档 - "快速开始" 章节
- 云原生网关技术白皮书或相关架构设计博客

**学习建议**: 
建议先阅读官方文档了解背景，然后务必动手使用 Docker Compose 在本地启动一个 Higress 实例。通过控制台创建一个简单的路由转发（例如将请求转发到 httpbin.org），以验证环境是否正常。

---

### 阶段 2：核心流量管理与配置

**学习内容**:
- 路由配置：基于域名、路径、Header 的流量匹配规则
- 服务来源管理：注册中心（Nacos, Consul, ZooKeeper, DNS, 固定地址）的配置与对接
- 负载均衡策略：轮询、随机、一致性哈希等算法的应用
- 插件系统入门：使用官方预设插件（如 Key Auth, Request Block）进行流量控制
- 全局配置与 TLS/HTTPS 证书管理

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "流量管理" 与 "服务来源" 板块
- Higress 官方插件市场文档
- Kubernetes Ingress (Nginx) 迁移至 Higress 的迁移指南/案例

**学习建议**: 
尝试模拟真实的微服务场景，例如在本地启动两个不同的后端服务，配置 Higress 将不同路径的流量路由到不同的服务上。重点练习如何对接 Nacos 作为服务来源，这是 Higress 在国内场景下的核心优势。

---

### 阶段 3：插件开发与 WAF 防护

**学习内容**:
- 高级插件使用：WAF 防护、限流降级、流量镜像
- Higress 插件开发规范：Wasm (WebAssembly) 技术基础（Go/C++/Rust）
- 编写自定义 Wasm 插件：处理请求头/响应头、修改请求体
- 插件的冷启动与性能优化
- 安全防护策略：针对 SQL 注入、XSS 等攻击的防御配置

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "插件市场" 与 "自定义插件" 开发指南
- Envoy Wasm 官方文档
- Higress GitHub 仓库中的示例插件代码

**学习建议**: 
此阶段是 Higress 进阶的关键。建议学习 Go 语言编写 Wasm 插件。先从官方提供的 Demo 插件入手，修改逻辑并编译测试，理解如何在 Wasm 虚拟机中拦截和处理 HTTP 请求。同时，配置 WAF 防护规则模拟拦截恶意请求。

---

### 阶段 4：生产级运维与高可用

**学习内容**:
- 在 Kubernetes 中的生产级部署配置（HPA, 资源限制）
- 可观测性集成：对接 Prometheus/Grafana 监控指标、链路追踪
- 日志服务集成：访问日志采集到 Elasticsearch/SLS 等日志系统
- 灰度发布与蓝绿发布实战
- 网关的高可用（HA）部署与灾备演练
- 常见问题排查与性能调优（连接池、缓冲区大小等参数）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "运维指南" 与 "可观测性"
- Kubernetes 官方文档关于 Ingress Controller 的最佳实践
- Higress GitHub Issues 中的常见问题排查记录

**学习建议**: 
重点关注监控和告警。部署 Prometheus 并配置 Higress 的 ServiceMonitor，观察 QPS、延迟、成功率等核心指标。尝试进行一次全链路灰度发布，验证流量按比例切换的正确性。学习如何通过日志定位 502/504 错误。

---

### 阶段 5：架构设计与源码研读

**学习内容**:
- Higress 深度架构剖析：Istio 与 Envoy 的集成原理
- 源码结构分析：控制面与数据面的交互流程
- 高级扩展：自定义 Ingress Class、多集群管理
- 服务网格结合：Higress 作为 Istio 的入口网关
- 参与开源社区：提交 Issue、PR 或贡献插件

**学习时间**: 持续

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部多年实践沉淀的下一代云原生网关。它是阿里云面向开源社区贡献的核心产品，旨在解决云原生时代流量治理和 API 管理的痛点。

Higress 的前身是阿里云内部的 Gateway 网关产品，它继承了阿里巴巴在双11等高并发场景下的流量管理经验。它建立在 Istio（Envoy） 之上，深度集成了 K8s Ingress 以及 API 网关的能力。简单来说，Higress 是一个集成了**流量网关**（K8s Ingress）和**微服务网关**（如 Spring Cloud Gateway）功能的统一入口层产品，旨在提供高性能、高扩展性和标准化的云原生 API 网关体验。

---



### 2: Higress 与 Nginx、Istio 或传统的 API 网关（如 Kong/APISIX）相比有什么优势？

2: Higress 与 Nginx、Istio 或传统的 API 网关（如 Kong/APISIX）相比有什么优势？

**A**: Higress 的设计理念是“合一”，即通过一个网关解决多种问题，其核心优势如下：

1.  **架构融合**：传统的 Nginx 主要作为静态配置的反向代理，缺乏动态服务发现能力；传统的微服务网关（如 Zuul/Gateway）缺乏 K8s 体系支持；而 Service Mesh（Istio）的 Sidecar 模式运维复杂。Higress 将 Ingress（入口网关）和 Gateway（API 网关）合二为一，既支持 K8s Ingress 资源，也支持更复杂的 API 管理和插件扩展。
2.  **高性能**：基于 C++ 编写的 Envoy 作为数据面，相比基于 Java 的传统网关（如 Spring Cloud Gateway），Higress 拥有更低的资源消耗和更高的吞吐量，更适合高并发场景。
3.  **强安全性**：支持 WAF（Web 应用防火墙）插件，能够提供更细粒度的安全防护，这是很多轻量级 Ingress Controller 所不具备的。
4.  **标准兼容与扩展性**：完全兼容 K8s Ingress 标准，同时支持 WASM（WebAssembly）插件，允许开发者使用多种语言（如 Go, C++, Rust, JS）编写插件，扩展性极强。

---



### 3: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

3: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

**A**: Higress 原生支持 HTTP、HTTPS 和 HTTP/2 协议。对于 gRPC 和 Dubbo 等微服务协议，Higress 也提供了强大的支持：

1.  **gRPC**：Higress 原生支持 gRPC 代理和路由，可以对 gRPC 服务进行流量管理、负载均衡以及通过插件修改请求或响应头。
2.  **Dubbo**：作为阿里巴巴出品的网关，Higress 对 Dubbo 有着深度的原生支持。它可以将 HTTP/JSON 请求转换为 Dubbo 协议，从而实现 HTTP 客户端调用后端 Dubbo 服务的跨协议互通。这对于许多使用 Java 技术栈的传统企业进行云原生改造非常有价值。

---



### 4: Higress 的插件系统是如何工作的？支持热加载吗？

4: Higress 的插件系统是如何工作的？支持热加载吗？

**A**: Higress 采用了一种灵活且高性能的插件架构，主要基于 Envoy 的过滤器机制和 WASM（WebAssembly）技术。

1.  **Lua/WASM 插件**：Higress 支持通过 Lua 或 WASM 编写插件。WASM 是其推荐的扩展方式，因为它具有沙箱隔离特性（插件崩溃不会导致网关崩溃）以及接近原生的执行效率。
2.  **热加载**：是的，Higress 支持插件的动态热加载。你可以在不重启网关实例的情况下，通过控制台或 API 动态地加载、卸载或修改插件配置。这使得流量治理策略的调整可以实时生效，极大地提高了运维效率。
3.  **插件市场**：Higress 社区通常会提供一系列预置的常用插件（如 JWT 认证、限流熔断、请求重写等），用户可以直接配置使用，也可以编写自定义插件。

---



### 5: 在生产环境中，Higress 的部署架构是怎样的？是否支持高可用？

5: 在生产环境中，Higress 的部署架构是怎样的？是否支持高可用？

**A**: Higress 是专为云原生生产环境设计的，支持多种高可用部署架构：

1.  **Kubernetes 部署**：这是最推荐的部署方式。通常以 Deployment 的形式部署在 K8s 集群中，配合 Service（LoadBalancer 或 NodePort）对外暴露服务。通过 K8s 的 HPA（Horizontal Pod Autoscaler）可以根据 CPU/内存使用率自动扩缩容网关实例。
2.  **多副本容灾**：在生产环境中，通常部署多个副本（Pod），以确保单个网关实例故障时流量能自动切换到健康实例。
3.  **全链路灰度**：Higress 支持流量标签，配合 MSE（微服务引擎）或 Istio，可以实现从网关到后端微服务的全

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速上手与流量验证

### 假设你已经成功在本地通过 Docker 启动了 Higress。请配置一个简单的路由规则，将访问 `http://localhost/test` 的流量转发到一个公开的测试 API（例如 `http://httpbin.org/get`），并通过浏览器或 Curl 验证配置是否生效。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 7 条针对实际使用场景的实践建议：

### 1. 利用 Wasm 插件实现 AI 请求的“无损”处理
**场景：** 在调用大模型（如 GPT, 文心一言）时，通常需要处理复杂的 Prompt 模板或敏感词过滤，直接修改后端服务代码成本高且不灵活。
**建议：** 充分利用 Higress 的 Wasm (WebAssembly) 生态。不要将 Prompt 工程逻辑写在业务代码中，而是编写或复用社区现有的 Wasm 插件（如 `ai-prompt-template` 或 `ai-reply-modify`）。
**操作：** 在网关层配置 Prompt 模板变量，将业务传入的简单参数通过网关转化为复杂的 Prompt。这样在切换模型或调整 Prompt 时，只需在网关配置热更新，无需重新发布业务服务。
**陷阱：** 避免使用 Lua 脚本处理高并发 AI 流量，Wasm 的隔离性和性能在 AI 长连接场景下更具优势。

### 2. 配置语义化的缓存策略降低 Token 成本
**场景：** AI 应用的 Token 消耗是主要成本，大量重复的用户问题会重复消耗后端模型的配额。
**建议：** 针对对实时性要求不高的 AI 查询场景，开启 Higress 的缓存插件。不同于传统的 URL 缓存，AI 网关应配置为基于请求 Body（Prompt 内容）的哈希缓存。
**操作：** 设置合理的 TTL（如 1 小时），并对相似的问题进行缓存命中。对于“获取知识库文档”等确定性输出的场景，可以开启较长时间的缓存。
**陷阱：** 注意缓存 Key 的设置，必须包含完整的 Prompt 内容，否则会导致错误的 A/B 测试结果或答非所问。

### 3. 实施基于 Key 的精细化限流与熔断
**场景：** 后端大模型 API 通常有严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制，且后端服务不稳定可能导致级联故障。
**建议：** 不要仅依赖 HTTP 状态码进行熔断。在 Higress 中配置针对特定 API Key 或租户的限流规则。
**操作：** 针对不同的开发者或应用分发不同的 API Key，在 Higress 层面为每个 Key 设置独立的 Quota。如果某个 Key 超过了后端模型的限制，网关应直接拦截并返回 429，避免冲击后端。
**陷阱：** AI 流量通常是长连接（SSE）或流式响应，传统的连接数限制可能失效，应优先配置请求级别的限流。

### 4. 统一多模型接口，屏蔽供应商差异
**场景：** 业务需要在不同的大模型供应商（如 OpenAI vs 通义千问 vs Claude）之间切换，或者需要根据成本路由到不同的模型。
**建议：** 使用 Higress 的服务路由功能，将标准化的 OpenAI 协议作为统一入口。
**操作：** 配置路由规则，将 `/v1/chat/completions` 根据请求头或参数动态转发到不同的后端服务。例如，将请求头 `x-model-provider: qwen` 的流量路由至阿里云百炼，将 `default` 流量路由至 OpenAI。
**最佳实践：** 在网关层抹平不同厂商 API 参数的细微差异（如 `temperature` 范围不同），让后端业务代码无需感知底层供应商的变化。

### 5. 妥善处理 SSE 流式传输的超时与异常
**场景：** 大模型回复通常采用 Server-Sent Events (SSE) 流式返回，耗时较长（可能几十秒），容易触发网关或负载均衡器的默认超时。
**建议：** 调整网关及上游服务的超时配置，并配置流式传输的缓冲策略。
**操作：** 将 Higress 的 `idle_timeout` 和上游服务的 `read_timeout` 设置为较大的值（如 300s）。确保

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260302-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*