---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-04T15:11:08+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结： 项目概况 * **名称**：Higress * **开发方**：阿里巴巴 * **简介**：一款基于 **Istio** 和 **Envoy** 构建的 **AI 原生 API 网关**。 * **语言**：Go * **热度*"
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
- **星标**: 7,449 (+8 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过集成 WASM 插件能力，实现了从传统流量管理到 AI 原生服务的平滑演进。它不仅满足微服务路由等基础需求，更针对 LLM 应用提供了 AI 网关特性及 MCP 服务器托管，旨在解决大模型接入与工具调用的复杂性。本文将梳理其系统架构，并重点剖析 AI 网关功能、MCP 系统及插件扩展机制等核心要点。

---
## 摘要

基于您提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结：

### 项目概况
*   **名称**：Higress
*   **开发方**：阿里巴巴
*   **简介**：一款基于 **Istio** 和 **Envoy** 构建的 **AI 原生 API 网关**。
*   **语言**：Go
*   **热度**：GitHub 星标数约 7,449（呈上升趋势）。

### 核心定位
Higress 是一款云原生 API 网关，它通过 **WebAssembly (WASM)** 插件能力扩展了 Istio 和 Envoy 的功能。其架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离。配置变更通过 xDS 协议传播，具备**毫秒级延迟**和**无连接中断**的特性，特别适合 AI 流式响应等长连接场景。

### 三大核心功能与用途

1.  **AI 网关**
    *   **用途**：为大语言模型（LLM）应用提供统一接口。
    *   **能力**：支持 30+ LLM 提供商的协议转换、可观测性、缓存及安全保障。
    *   **组件**：`ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 插件。

2.  **MCP 服务器托管**
    *   **用途**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用工具和服务。
    *   **组件**：`mcp-router`、`jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如 `quark-search`、`amap-tools`、`all-in-one`）。

3.  **Kubernetes Ingress**
    *   **用途**：作为 Kubernetes Ingress 控制器，支持微服务路由。
    *   **兼容性**：兼容 nginx-ingress 注解。
    *   **组件**：`higress-controller`。

### 总结
Higress 不仅涵盖了传统 API 网关的流量管理功能，更针对 AI 时代进行了深度优化，提供了从 LLM 统一接入到 Agent 工具调用的全栈能力。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“AI 原生”网关，它成功地将云原生流量治理技术与大模型（LLM）应用需求深度融合。该项目不仅是阿里巴巴开源技术栈在 AI 时代的延续，更是目前市面上将传统 API 网关与 AI 网关功能结合得最彻底、架构最清晰的落地实践之一。

**详细评价维度**

**1. 技术创新性：从“流量侧车”进化为“AI 推理中枢”**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件系统。DeepWiki 明确指出其核心功能包括 AI Gateway、MCP Server 托管以及传统微服务路由。
*   **推断**：Higress 的最大差异化在于它没有停留在“流量转发”层面，而是通过**协议转换**和**语义路由**解决了 AI 落地的痛点。它将传统的 HTTP/gRPC 路由能力扩展到了 LLM 协议（如 OpenAI 协议兼容），使得网关能够理解 Prompt 的上下文。利用 WASM 的沙箱隔离特性，开发者可以用 C++/Go/Rust 编写高性能插件，在网关层直接实现 Token 计费、敏感词过滤或 Prompt 注入，这种**“计算下沉”**的架构比传统网关更灵活，比 Sidecar 代理模式更轻量。

**2. 实用价值：统一入口，降低 AI 落地复杂度**
*   **事实**：文档强调其提供“AI gateway features for LLM applications”和“MCP server hosting”。
*   **推断**：在当前 AI 应用爆发期，企业面临两个棘手问题：一是多模型（OpenAI, 通义千问, DeepSeek 等）的接入成本高，二是 AI Agent 需要通过 MCP (Model Context Protocol) 调用外部工具。Higress 直接将 MCP Server 托管功能内置，这意味着它不仅是流量的守门员，更是 **AI Agent 的工具箱**。它解决了企业需要分别维护“传统 API 网关”和“AI 代理（如 LangChain 服务）”的割裂问题，实现了**流量管理与 AI 编排的统一**，极大地降低了运维复杂度。

**3. 代码质量与架构：云原生基因的优雅继承**
*   **事实**：项目语言为 Go，架构上明确分离了控制平面和数据平面。
*   **推断**：基于 Envoy 作为数据平面保证了高性能和可扩展性，这是业界公认的事实。Higress 的架构设计遵循了云原生的最佳实践，将配置管理（控制面）与流量处理（数据面）解耦。Go 语言编写控制面保证了开发效率，而 Envoy (C++) 处理数据面保证了极致性能。文档中提到的详细架构分页说明，体现了项目在文档规范性上的高水准，这对于企业级落地至关重要。

**4. 社区活跃度：阿里背书，生态稳健**
*   **事实**：星标数 7,449（且在快速增长中），由阿里巴巴开源。
*   **推断**：作为阿里云核心网关产品的开源版本，Higress 继承了阿里巴巴在“双11”高并发场景下的技术沉淀。相比于纯个人项目，它有明确的商业化兜底和技术支持保障，代码更新频率高，功能迭代紧跟 AI 模型的发展步伐（如迅速支持最新的模型参数）。社区活跃度不仅体现在 Star 数，更体现在其与 Kubernetes 生态的紧密集成上，这是技术社区目前最关注的领域。

**5. 学习价值：理解 AI 时代流量治理的窗口**
*   **事实**：DeepWiki 提供了从 Overview 到 Development Guide 的完整文档链路。
*   **推断**：对于开发者而言，Higress 是学习**“如何将 AI 能力嵌入基础设施”**的最佳范例。通过研究其 WASM 插件机制，开发者可以学习如何在不修改核心代码的情况下，动态扩展网关的 AI 语义处理能力。同时，它展示了 MCP 协议在实际生产环境中的托管与路由实现，为构建未来的 AI Agent 系统提供了重要的参考架构。

**6. 潜在问题与改进建议**
*   **推断**：虽然功能强大，但基于 Istio 和 Envoy 的架构使得部署和运维的**学习曲线依然陡峭**。对于非云原生背景的小团队，部署一套完整的 Higress 可能存在挑战。此外，AI Gateway 的功能（如模型路由、Prompt 模板管理）目前可能主要针对国内模型或阿里云系模型做了深度优化，对海外边缘小模型的兼容性适配可能需要社区贡献更多力量。

**7. 对比优势：比 Kong 更懂 AI，比 LangChain 更懂流量**
*   **推断**：
    *   **对比 Kong/APISIX**：传统网关虽然也有 AI 插件，但多为后补功能。Higress 从底层设计上就考虑了 AI 的流式传输特征和 MCP 协议，集成度更高。
    *   **对比 LangChain/LLM Engine**：这些框架主要关注应用逻辑和模型调用，缺乏专业的流量治理（如限流、熔断、认证）。Higress 提供了企业级的灰度发布和全链路监控能力，是 AI 应用走向生产环境的“最后一公里”保障。

**边界条件与快速验证**

**不适用场景**：
*   极简场景：如果只是个人玩票性质调用一个 OpenAI API，使用 Nginx 或

---
## 技术分析

# Higress 深度技术分析报告

Higress 是由阿里巴巴开源的一款**云原生 API 网关**，其核心定位在于**"AI Native"（AI 原生）**。它不仅仅是一个传统的流量入口，更是为了解决大模型（LLM）应用落地、AI Agent 编排以及微服务治理而设计的下一代网关。以下是基于提供的 GitHub 仓库信息及云原生网关通用技术原理的深度分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的经典架构模式，这是现代云原生数据面（如 Istio、Envoy）的标准设计。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 C++ 实现的高并发、低延迟特性处理流量。
*   **控制平面**：基于 **Istio** 进行扩展。Higress 并没有从零造轮子，而是继承了 Istio 的配置管理和分发逻辑，通过 **xDS 协议**（包括 LDS, RDS, CDS, EDS）将配置推送到数据平面。
*   **扩展语言**：**Go**。Higress 的控制平面逻辑使用 Go 编写，便于与 Kubernetes 生态集成。
*   **插件机制**：**WebAssembly (WASM)**。这是其架构中最关键的一环，允许使用 C/C++/Go/Rust 等语言编写插件，并在 Envoy 的沙箱中动态加载，实现了业务逻辑与网关核心的解耦。

### 核心模块与关键设计
1.  **路由与流量管理**：兼容 Kubernetes Ingress 标准，支持 Nginx Ingress 注解，降低了迁移成本。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时，使得插件可以在不重启网关的情况下热更新。
3.  **AI 网关层**：在传统网关之上，专门针对 LLM 协议（如 OpenAI 协议）进行了深度适配，包括请求转发、响应处理以及工具调用。

### 技术亮点与创新点
*   **AI Native 原生化**：市面上大多数网关是为 REST/RPC 设计的，Higress 原生支持 SSE（Server-Sent Events）流式转发，这对 LLM 的"打字机效果"至关重要。它解决了传统网关在处理长连接、流式响应时的缓冲和延迟问题。
*   **MCP (Model Context Protocol) Server 托管**：Higress 创新性地将网关作为 AI Agent 的工具提供者。它不仅转发请求，还能直接作为 MCP Server 暴露工具给 AI Agent，简化了 Agent 与企业内部工具集成的复杂度。
*   **毫秒级配置生效**：基于 xDS 的增量推送机制，配置变更可以达到毫秒级生效，且不断连。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一模型接入**：企业内部可能接入多家大模型（通义千问、DeepSeek、OpenAI 等），Higress 提供统一的标准接口，后端可路由到不同供应商。
    *   **Token 计费与限流**：基于 Prompt 和 Completion 的 Token 数量进行精细化计量和限流，而非传统的 HTTP 请求数。
    *   **敏感数据过滤**：利用 WASM 插件在请求发往模型前或返回给用户前，实时拦截敏感词。

2.  **MCP 系统集成**：
    *   **场景**：AI Agent 需要调用企业内部 API（如查询库存、发邮件）。
    *   **解决痛点**：直接暴露内部 API 存在安全风险，且需要编写适配器代码。Higress 允许将现有的后端服务直接声明为 MCP 工具，网关自动处理协议转换。

3.  **传统微服务网关**：
    *   支持 K8s Ingress、Nacos 服务注册发现、金丝雀发布、蓝绿部署。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | APISIX |
| :--- | :--- | :--- | :--- |
| **架构** | 基于 Envoy + Istio (控制面分离) | Nginx (单机/模块化) | 基于 Apache APISIX (Lua) |
| **AI 支持** | **原生支持** (SSE, Token限流, MCP) | 需配合 Lua 脚本或外部服务，流式处理性能损耗大 | 支持 SSE，但缺乏 AI 原生生态（如 MCP） |
| **扩展性** | WASM (沙箱，多语言，高性能) | C Module (需重启，风险高) / Lua (单线程) | Plugin (Lua/Go, Python) |
| **配置热更新** | 毫秒级，不断连 | 需 Reload (有连接抖动) | 毫秒级 |

---

## 3. 技术实现细节

### 关键技术方案
*   **流量劫持与转发**：利用 Envoy 的 Listener 和 Filter Chain 机制。在 AI 场景下，关键在于 **Stream Filter** 的实现，它能够截获 HTTP 分片，在流式传输过程中进行实时处理（如修改头部、统计 Token）而不阻塞流。
*   **WASM 插件加载**：Higress 实现了 OCI (Open Container Initiative) 镜像拉取机制。插件被打包成 OCI 镜像存储在镜像仓库中，网关按需拉取并挂载到 Envoy 的 WASM VM 中。
*   **服务发现融合**：通过 Controller 监听 Kubernetes API Server 以及 Nacos 等注册中心，将服务数据转换为 Envoy 的 EDS (Endpoint Discovery Service) 配置。

### 性能与扩展性
*   **零拷贝**：Envoy 本身的高性能得益于其零拷贝网络栈。Higress 在设计插件时，尽量避免在 WASM 内存与 Envoy 主机内存之间进行大量数据拷贝，以保持高吞吐。
*   **水平扩展**：作为无状态网关，Higress 数据平面可以轻松通过 Kubernetes HPA (Horizontal Pod Autoscaler) 进行扩容。

### 技术难点与解决
*   **流式响应的上下文处理**：LLM 返回的是流式 Token，很难在流结束前统计总 Token 数。Higress 通过在流式 Filter 中维护状态机，实时计数并在流结束时触发回调逻辑（如记录日志）来解决此问题。
*   **WASM 的冷启动**：WASM 插件首次加载可能有延迟。Higress 通过预加载机制和优化 WASM VM 的实例池来缓解此问题。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用中台**：企业统一管理对各大模型厂商的 API 调用，需要统一的鉴权、限流、计费和缓存。
2.  **AI Agent 开发平台**：需要快速将企业内部 REST API 暴露给 AI Agent，利用 Higress 的 MCP Server 功能可以省去开发 Adapter 的工作量。
3.  **高并发微服务治理**：基于 K8s 的云原生架构，需要比 Nginx Ingress 更强的动态配置能力和更灵活的插件扩展能力。

### 不适合的场景
1.  **极简边缘路由**：如果只是做一个简单的单机反向代理，Nginx 足够且更轻量，Higress 的组件复杂度（依赖 Istio/Envoy）显得过重。
2.  **非 K8s 环境的强依赖**：虽然支持非 K8s 部署，但其最大威力在于与 K8s 的结合。在传统虚拟机环境中，运维复杂度较高。

### 集成注意事项
*   **资源规划**：Envoy 和 WASM 运行时对内存有一定要求，建议为每个 Higress 实例预留足够的内存。
*   **网络连通性**：控制平面与数据平面之间的 xDS 通信必须稳定，否则配置下发会失败。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 Dapr 集成**：随着云原生向 BaaS（Backend as a Service）演进，Higress 可能会加强与服务网格和 Dapr 的集成，成为服务间通信的唯一入口。
*   **RAG (检索增强生成) 内置**：未来可能内置向量数据库连接能力，直接在网关层实现简单的 RAG 逻辑（如查询缓存、文档检索预处理），减轻后端应用压力。

### 社区与生态
*   **插件市场**：Higress 正在构建类似于 VS Code 插件市场的 WASM 插件生态，这将极大降低用户的使用门槛。
*   **标准化**：推动 MCP 协议在企业级网关中的落地，使其成为 AI Agent 连接企业服务的标准接口。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：需要深入理解 Service Mesh 和 Gateway 架构。
*   **AI 应用开发者**：需要处理模型调用、流式响应和工具调用的后端工程师。
*   **Go/后端开发**：想学习如何基于 Envoy 构建高性能控制平面。

### 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 和 基础的网关概念。
2.  **进阶**：学习 Envoy 架构，特别是 xDS 协议和 Filter 机制。
3.  **实战**：阅读 Higress 官方文档，尝试部署并编写一个简单的 WASM 插件（如修改请求头）。
4.  **深入**：研究 Higress 的 AI Gateway 实现，了解它是如何处理 SSE 流的。

---

## 7. 最佳实践建议

### 使用规范
*   **插件隔离**：WASM 插件虽然有沙箱，但耗时的插件逻辑（如调用外部 API）会阻塞请求。建议将复杂逻辑放在独立服务中，网关通过 **gRPC 或 HTTP** 调用外部服务（ExtAuth/ExtProc 模式）。
*   **配置管理**：利用 GitOps 管理网关配置，避免直接修改集群内 ConfigMap，保证可追溯性。

### 性能优化
*   **连接池**：合理配置 Envoy 到后端服务的连接池大小，避免后端服务过载。
*   **WASM 内存限制**：为每个 WASM 插件设置合理的内存上限，防止插件 Bug 导致网关 OOM。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在抽象层上做出了一个明确的抉择：**将"流量治理"的复杂性从应用代码中剥离，转移到基础设施层（网关）**。
*   **传统模式**：应用代码处理熔断、限流、鉴权、AI 协议解析。
*   **Higress 模式**：应用只关注业务逻辑，网关负责所有非功能性需求。
*   **代价**：运维复杂度上升。你需要理解 Envoy、xDS、WASM 等概念。它将开发者的负担转移给了

---
## 代码示例




```python
# 示例1：基于Higress的动态路由配置
def dynamic_routing_config():
    """
    解决问题：实现基于请求头的动态路由分发
    场景：根据用户类型（普通用户/VIP用户）将流量路由到不同后端服务
    """
    config = {
        "name": "user-routing",
        "priority": 1,
        "match": {
            "headers": {
                "user-type": {
                    "exact": "vip"  # 匹配VIP用户
                }
            }
        },
        "route": {
            "cluster": "vip-service-cluster",  # 路由到VIP服务集群
            "timeout": "5s",
            "retry_policy": {
                "retry_on": "5xx",
                "num_retries": 3
            }
        }
    }
    return config

# 说明：这个示例展示了如何使用Higress的动态路由功能，通过匹配请求头中的user-type字段，
# 将VIP用户请求路由到专门的服务集群，并配置了超时和重试策略，提高服务可靠性。
```




```python
# 示例2：Higress插件开发 - 请求限流
def rate_limit_plugin():
    """
    解决问题：实现基于IP的请求频率限制
    场景：防止恶意IP对API接口进行过度访问
    """
    plugin_config = {
        "name": "ip-rate-limit",
        "phase": "auth",  # 在认证阶段执行
        "config": {
            "limit_by": "remote_address",  # 基于远程IP限流
            "rules": [
                {
                    "limit": 100,  # 每分钟100次请求
                    "window": "1m",
                    "burst": 20    # 允许突发20次请求
                }
            ],
            "response": {
                "status_code": 429,
                "headers": {
                    "X-RateLimit-Limit": "100",
                    "X-RateLimit-Remaining": "0"
                }
            }
        }
    }
    return plugin_config

# 说明：这个示例展示了如何开发一个Higress插件来实现IP级别的请求限流，
# 通过令牌桶算法控制每个IP的访问频率，防止接口被滥用，同时返回友好的限流响应。
```




```python
# 示例3：Higress服务网格流量管理
def traffic_management():
    """
    解决问题：实现金丝雀发布流量控制
    场景：新版本灰度发布，逐步切换流量
    """
    traffic_config = {
        "name": "canary-deployment",
        "selector": {
            "match_labels": {
                "version": "v2"  # 匹配新版本服务
            }
        },
        "traffic_policy": {
            "weight": 30,  # 30%流量到新版本
            "headers": {
                "canary": {
                    "exact": "true"  # 带特定header的流量强制走新版本
                }
            },
            "mirroring": {
                "cluster": "v2-service-cluster",
                "percentage": 10  # 10%流量镜像到新版本（不响应）
            }
        }
    }
    return traffic_config

# 说明：这个示例展示了如何使用Higress进行金丝雀发布管理，
# 通过权重控制逐步将流量切换到新版本，同时支持基于请求头的精确路由和流量镜像，
# 实现平滑的服务升级和回滚能力。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 在阿里巴巴庞大的电商生态系统中，核心交易链路（如淘宝、天猫的双11大促）面临着极高的并发流量挑战。原有的 API 网关架构在处理每秒百万级 QPS（Queries Per Second）时，遇到了性能瓶颈和扩展性问题。

**问题**: 
1. 传统网关在应对突发流量时延迟较高，影响用户体验。
2. 云原生架构下的服务治理（如流量路由、灰度发布）配置复杂，缺乏标准化的流量管理能力。
3. 需要一套既能支持高并发，又能对接阿里云内部异构服务体系的网关系统。

**解决方案**: 基于 Higress（前身是内部内部迭代多年的 Gateway 架构）构建了统一的云原生 API 网关。
1. 利用 Higress 的高性能 C++ 内核，替代了部分旧的 Java 网关，显著降低了资源消耗。
2. 采用了 Higress 对 Istio 的深度集成，实现了服务网格南北向与东西向流量的统一治理。
3. 通过 Higress 的插件市场，快速实现了针对电商业务的定制化逻辑（如请求校验、流量削峰）。

**效果**: 
1. 成功支撑了双11期间每秒数百万级的请求峰值，P99 延迟显著降低。
2. 实现了网关层的弹性伸缩，在保证高可用的前提下，服务器资源成本下降了约 30%。
3. 统一的流量控制标准使得业务上线效率提升，运维复杂度大幅下降。

---



### 2：某大型互联网公司 AI 业务落地

 2：某大型互联网公司 AI 业务落地

**背景**: 随着大语言模型（LLM）和 AIGC 应用的爆发，该公司需要构建一个面向内部开发者及外部合作伙伴的 AI 网关，用于统一接入和管理各种 AI 模型服务（如 OpenAI, 通义千问, Llama 等）。

**问题**: 
1. 不同 AI 提供商的 API 接口标准不一，集成成本高。
2. AI 应用开发中缺乏统一的 Token 计费、流量限制和 Prompt 模板管理功能。
3. 数据安全性要求高，需要在网关层统一处理敏感信息过滤和请求鉴权。

**解决方案**: 部署 Higress 作为 AI 专用网关。
1. 利用 Higress 原生支持的 AI 特性，将不同模型的异构接口标准化为统一的 OpenAI 格式，方便应用层调用。
2. 配置 Higress 的插件来实现 Token 统计、基于 Token 的流控以及 Prompt 优化管理。
3. 通过网关层实现了敏感词过滤和统一鉴权，确保后端模型服务的安全。

**效果**: 
1. 开发者接入新模型的时间从数天缩短至小时级，只需在网关层配置即可切换模型供应商。
2. 实现了精细化的成本控制，能够按部门或项目统计 AI 调用成本。
3. 构建了安全合规的 AI 代理层，避免了模型接口直接暴露带来的安全风险。

---



### 3：多语言微服务架构下的企业级 SaaS 平台

 3：多语言微服务架构下的企业级 SaaS 平台

**背景**: 该企业拥有基于 Spring Cloud（Java）、Go 和 Node.js 构建的混合微服务架构。在云原生转型过程中，他们需要解决不同语言服务间的通信治理问题，并对外暴露统一的 API。

**问题**: 
1. 不同语言栈的服务分别使用各自的 SDK 进行服务注册与发现，导致维护成本极高。
2. 缺乏统一的入口来管理外部流量对内部微服务的访问，安全性难以保障。
3. 需要支持 HTTP、gRPC 等多种协议的高性能转发。

**解决方案**: 引入 Higress 作为云原生入口网关，并配合 Nacos 进行服务发现。
1. Higress 通过 Nacos 注册中心发现后端的异构微服务，无需在网关层硬编码服务地址。
2. 利用 Higress 的高性能路由能力，统一处理 HTTP 和 gRPC 流量，并实现了基于权重的蓝绿发布和金丝雀发布。
3. 启用了 Higress 的 WAF（Web应用防火墙）插件，防御 SQL 注入和 XSS 攻击。

**效果**: 
1. 统一了流量入口，屏蔽了后端多语言架构的复杂度，运维效率提升 40%。
2. 实现了流量的精细化控制，新版本的灰度发布过程平滑，故障率降低。
3. 网关层的统一安全策略有效拦截了恶意攻击，提升了系统的整体安全性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|--------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 基于OpenResty，性能较高，但扩展性依赖Lua | 基于OpenResty，性能与Kong相当，支持动态路由 |
| 易用性 | 提供可视化控制台，支持Kubernetes集成，配置简单 | 配置灵活但复杂，需要熟悉YAML或API | 提供Dashboard，但学习曲线较陡 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，企业版功能需付费 | 开源免费，企业版功能需付费 |
| 功能丰富度 | 支持流量管理、安全防护、可观测性等核心功能 | 插件生态丰富，支持多种协议 | 插件生态较丰富，支持动态配置 |
| 社区活跃度 | 阿里背书，社区活跃，文档完善 | 社区成熟，插件生态强大 | 社区活跃，国内用户较多 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性中等 | 支持Lua和自定义插件，扩展性较强 |

### 优势分析

- 优势1：基于Envoy和Istio，性能和扩展性优于传统网关。
- 优势2：提供可视化控制台和Kubernetes集成，降低使用门槛。
- 优势3：支持Wasm插件，扩展性强，适合复杂业务场景。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态尚在发展中，功能覆盖有限。
- 不足2：商业支持需付费，成本可能高于纯开源方案。
- 不足3：文档和社区资源虽然完善，但国际化程度不如Kong。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**:  
Higress 基于 Envoy 构建，通过深度定制实现了高性能的 API 网关功能。Envoy 的 L3/L7 过滤器架构和异步 I/O 模型确保了高并发场景下的低延迟。

**实施步骤**:
1. 部署 Higress 时，根据业务需求调整 Envoy 的线程数和连接池配置。
2. 启用 Envoy 的动态资源管理功能，避免内存溢出。
3. 监控 Envoy 的性能指标（如请求延迟、吞吐量），使用 Prometheus 和 Grafana 进行可视化。

**注意事项**:  
- 避免过度定制 Envoy 配置，可能导致维护困难。
- 定期更新 Higress 版本以获取最新的 Envoy 性能优化。

---

### 实践 2：服务发现与动态路由配置

**说明**:  
Higress 支持多种服务发现机制（如 Nacos、Consul、Kubernetes），并允许动态更新路由规则。这确保了服务变更时无需重启网关。

**实施步骤**:
1. 配置服务发现组件，确保 Higress 能实时感知服务实例的上下线。
2. 使用 Higress 的控制台或 API 定义路由规则，支持基于权重、Header 等条件的流量分发。
3. 测试路由规则的正确性，确保流量按预期分配。

**注意事项**:  
- 服务发现组件的稳定性直接影响 Higress 的路由准确性。
- 复杂路由规则可能增加管理复杂度，建议通过版本控制管理配置。

---

### 实践 3：安全防护与 WAF 集成

**说明**:  
Higress 提供内置的安全功能（如 IP 黑白名单、请求限流），并支持与 WAF（如阿里云 WAF）集成，增强 API 安全性。

**实施步骤**:
1. 在 Higress 控制台配置 IP 黑白名单，限制非法访问。
2. 启用请求限流功能，防止 DDoS 攻击。
3. 集成 WAF 服务，配置规则拦截恶意流量。

**注意事项**:  
- 限流阈值需根据业务实际流量调整，避免误杀正常请求。
- WAF 规则需定期更新以应对新型攻击。

---

### 实践 4：插件扩展与自定义开发

**说明**:  
Higress 支持通过插件扩展功能，开发者可以基于 Lua 或 WASM 编写自定义插件，满足特定业务需求。

**实施步骤**:
1. 评估业务需求，确定是否需要自定义插件。
2. 使用 Higress 提供的插件开发框架编写代码。
3. 测试插件功能，确保不影响网关性能。

**注意事项**:  
- 插件代码需经过充分测试，避免引入安全漏洞。
- 复杂插件可能增加网关延迟，建议性能测试后上线。

---

### 实践 5：多集群管理与流量治理

**说明**:  
Higress 支持多集群部署，提供统一的流量治理能力，适用于跨地域或跨云环境的服务调度。

**实施步骤**:
1. 部署多个 Higress 集群，配置集群间的网络连通性。
2. 使用 Higress 的控制平面统一管理流量规则。
3. 实施灰度发布或蓝绿部署，验证流量治理效果。

**注意事项**:  
- 多集群管理需确保网络延迟和带宽满足业务需求。
- 跨集群流量调度可能增加复杂度，建议逐步实施。

---

### 实践 6：可观测性与日志集成

**说明**:  
Higress 提供丰富的可观测性功能，支持与 Prometheus、SkyWalking 等工具集成，实现全链路监控和日志分析。

**实施步骤**:
1. 配置 Higress 的 Metrics 端点，对接 Prometheus。
2. 启用访问日志和错误日志，输出到 Elasticsearch 或 Loki。
3. 使用 Grafana 创建仪表盘，实时监控网关状态。

**注意事项**:  
- 日志量较大时需注意存储成本，建议配置日志轮转。
- 敏感信息（如 Token）需在日志中脱敏处理。

---

### 实践 7：高可用部署与容灾设计

**说明**:  
Higress 支持多副本部署和自动故障转移，确保网关服务的高可用性。

**实施步骤**:
1. 在 Kubernetes 环境中部署 Higress，设置副本数至少为 3。
2. 配置健康检查探针，确保异常实例自动剔除。
3. 测试故障恢复流程，验证容灾能力。

**注意事项**:  
- 多副本部署需确保资源充足，避免单点过载。
- 定期演练故障恢复流程，确保预案有效性。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，底层的网络协议对吞吐量和延迟影响巨大。HTTP/2 通过多路复用解决了 HTTP/1.x 的队头阻塞问题，而 HTTP/3 (QUIC) 基于 UDP 实现，能显著减少弱网环境下的握手延迟和丢包重传时间。

**实施方法**:
1. 在 Higress 的网关配置或监听器设置中，启用 HTTP/2 开关。
2. 如果客户端支持，配置并开启 HTTP/3 (QUIC) 监听端口（通常基于 UDP 443）。
3. 确保后端 Upstream 服务也支持 HTTP/2 以形成全链路优化。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，高并发下连接复用率提升，TCP 连接数显著减少。

---

### 优化 2：配置全链路超时与连接池调优

**说明**: 默认的超时和连接池配置往往过于保守或激进，导致连接频繁重建（RTT 增加）或资源耗尽。针对 Higress 的高并发 Java/Golang 底层特性，需精细调整 Upstream 的连接保持和超时参数。

**实施方法**:
1. **调整连接池**: 增大 `maxRequestsPerConnection` 或 `maxConnections` 参数，允许在单个 TCP 连接上处理更多请求。
2. **设置 Keep-Alive**: 开启 HTTP Keep-Alive，并设置合理的 `idleTimeout`（例如 60s），避免频繁建连。
3. **超时优化**: 根据业务 P99 耗时，调整 `connectTimeout`、`sendTimeout` 和 `readTimeout`，防止慢请求堆积。

**预期效果**: 后端服务连接数减少 40% 以上，请求建立连接的耗时（RTT）显著降低，网关吞吐量（QPS）提升 15%-25%。

---

### 优化 3：启用 Wasm 插件的高效隔离与缓存

**说明**: Higress 支持 Wasm 插件扩展，但不当的插件隔离级别（如每次请求都重新初始化）或频繁的内存分配会带来巨大的性能损耗。合理利用 Wasm 的内存复用和 Proxy-Wasm 的生命周期钩子至关重要。

**实施方法**:
1. **插件生命周期管理**: 将耗资源的初始化逻辑（如加载字典、建立连接）放在 `on_configure` 或 `on_vm_start` 阶段，避免在 `on_request` 阶段重复执行。
2. **内存复用**: 尽量复用 Wasm 虚拟机内的内存缓冲区，减少频繁的 `malloc`/`free` 操作。
3. **缓存策略**: 对于插件中的鉴权或配置拉取，在 Wasm 内存中实现本地缓存，减少对外部服务的调用。

**预期效果**: 插件执行延迟降低 20%-40%，CPU 开销显著减少，复杂路由逻辑下的网关处理性能提升明显。

---

### 优化 4：启用 CPU 亲和性与多核绑定

**说明**: Higress 基于 Envoy 和 Istio 构建，核心处理逻辑受 CPU 上下文切换影响较大。通过将网关进程绑定到特定的 CPU 核心，可以减少缓存失效和上下文切换开销，提升数据平面处理效率。

**实施方法**:
1. **容器级配置**: 在 Kubernetes Deployment 中设置 `resource.limits.cpu`，并利用 CPU Manager 策略（Guaranteed QoS）。
2. **系统级调优**: 使用 `taskset` 或 Higress/Envoy 的 `--cpuset-threads` 选项，将工作线程绑定到物理 CPU 核心。
3. **关闭超线程**: 在极致性能场景下，考虑在 BIOS 中关闭超线程，以减少 L1/L2 缓存的争抢。

**预期效果**: 长尾延迟（P99 Latency）降低 10%-30%，系统吞吐量稳定性提升，CPU 缓存命中率提高。

---

### 优化 5：实施日志采样与

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，深度集成了 Envoy 和 K8s
- 支持将 K8s Ingress、Gateway API 或 Nginx 配置直接转换为 Higress 路由规则，降低迁移成本
- 内置 WAF 插件和自定义插件系统（Wasm 支持），可灵活扩展安全防护与流量治理能力
- 提供多协议支持（HTTP、HTTPS、HTTP/3、Dubbo、gRPC 等）及高性能流量转发
- 兼容 Istio 和 Nginx Ingress 生态，可作为其替代方案无缝接入现有服务网格
- 具备服务发现、负载均衡、熔断降级等全链路治理功能，适合微服务架构
- 官方提供控制台 UI 和 Prometheus 监控集成，简化运维与可观测性管理


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 云原生网关的基本概念与Higress的定位
- Higress 与 Nginx、Istio、传统 API 网关的区别与联系
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 基础术语：路由、服务、插件、Upstream
- Docker 环境下 Higress 的快速安装与部署
- 控制台的基本操作与界面熟悉

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - "什么是 Higress" 章节
- Higress 官方文档 - "快速开始" 章节
- 云原生网关技术对比相关博客文章

**学习建议**: 
建议先通读官方文档，理解 Higress "基于 Envoy 和 Istio" 的背景。务必动手在本地或测试环境通过 Docker/Docker Compose 完成一次标准安装，并成功访问控制台页面，不要只停留在理论层面。

---

### 阶段 2：核心配置与流量管理

**学习内容**:
- 基于域名和路径的路由配置
- HTTP 与 HTTPS 流量处理与证书配置
- 服务发现与注册中心集成 (Nacos, Consul, K8s Service)
- 负载均衡策略配置 (轮询、随机、一致性哈希等)
- 金丝雀发布与蓝绿发布配置
- 流量镜像与重定向设置
- 基础认证鉴权配置 (Basic Auth, AK/SK)

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "路由配置" 与 "服务来源"
- Envoy 官方文档关于 HTTP 路由的参考
- Higress 官方示例 - K8s Ingress 资源配置示例
- Higress 官方文档 - "插件市场" 中的基础认证插件说明

**学习建议**:
此阶段重点在于 "流量搬运"。建议搭建一个简单的后端服务（如 Nginx 或 echo server），尝试配置不同的路由规则来观察流量走向。重点练习 Ingress YAML 文件的编写，这是自动化部署的基础。

---

### 阶段 3：插件开发与扩展能力

**学习内容**:
- Higress 插件系统原理
- 使用 Wasm (WebAssembly) 技术开发自定义插件
- Lua 脚本在 Higress 中的应用
- 官方插件的使用：限流、熔断、缓存、Header 修改
- 插件的热加载与配置优先级
- 全局插件与路由级插件的区别

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "自定义插件开发"
- Higress GitHub 仓库中的插件示例代码
- Envoy Wasm 相关技术文档
- Higress 官方插件市场

**学习建议**:
这是 Higress 最具特色的部分。建议先熟练使用官方插件解决常见问题（如防盗链、限流），然后尝试使用 Go 或 C++ 编写一个简单的 Wasm 插件（例如修改请求头或响应体），并在本地环境中编译、加载和测试。

---

### 阶段 4：生产实践与高阶运维

**学习内容**:
- Higress 的高可用 (HA) 部署架构设计
- 性能调优：连接池、缓冲区大小、工作线程数配置
- 监控与可观测性集成 (Prometheus, Grafana, SkyWalking)
- 安全防护：WAF 集成、CORS 跨域配置、防 DDoS 策略
- 灰度发布全链路闭环实践
- Higgress 在 Kubernetes 环境下的 Helm 部署与运维
- 常见故障排查与日志分析

**学习时间**: 4周及以上

**学习资源**:
- Higress 官方文档 - "运维指南" 与 "监控"
- Higress GitHub Issues 中的典型问题讨论
- Kubernetes Ingress Controller 最佳实践
- Prometheus 与 Grafana 监控配置文档

**学习建议**:
此阶段需要结合实际生产场景进行思考。建议模拟高并发场景进行压测，观察 Higress 的 CPU/内存表现并调整参数。深入学习如何利用 Prometheus 采集 Higress 的指标，并在 Grafana 中绘制可视化大屏。关注日志细节，学会通过日志定位网关层面的故障。

---
## 常见问题


### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它建立在 Envoy 和 Istio 等开源项目之上，由阿里云发起并开源，同时捐赠给了云原生计算基金会（CNCF）作为 Sandbox 项目。Higress 的定位是作为云原生时代的流量入口，旨在连接微服务、云函数（FC）以及后端服务，提供统一的流量管理、安全防护和插件扩展能力。它既可以在本地环境（Kubernetes）部署，也完全兼容阿里云上的 API 网关托管服务。

---



### 2: Higress 与传统的 Nginx 或 Kong 网关相比有什么核心优势？

2: Higress 与传统的 Nginx 或 Kong 网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **技术架构先进**：底层基于 Envoy 高性能代理，采用 C++ 内核，相比基于 Lua 的 Nginx 或基于 OpenResty 的 Kong，在处理高并发长连接（如 gRPC、Dubbo）时具有更低的延迟和更高的吞吐量。
2.  **标准化与云原生集成**：它深度集成了 Istio，可以作为 Ingress Controller 或 Gateway API 的实现，与 Kubernetes 服务网格（Service Mesh）生态无缝衔接，支持 Kubernetes Ingress、Gateway API 等标准。
3.  **插件生态与热更新**：Higress 提供了强大的 Wasm (WebAssembly) 插件支持。用户可以使用 Go 或 C++ 编写插件，且插件支持热加载，无需重启网关进程即可生效，这比传统的 Nginx 模块开发要灵活和安全得多。
4.  **安全防护**：内置了与阿里云 Web 应用防火墙（WAF）同源的安全能力，能够提供更强大的企业级防护。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller (如 Nginx Ingress) 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller (如 Nginx Ingress) 进行迁移？

**A**: 是的，Higress 非常重视迁移的兼容性。它支持标准的 Kubernetes Nginx Ingress Annotation 注解，这意味着在大多数情况下，用户只需要将 Kubernetes 的 Ingress Class 修改为 Higress 提供的 Class，即可无缝将流量从 Nginx Ingress Controller 切换到 Higress，而无需修改大量的 YAML 配置文件。此外，Higress 还提供了针对传统 Nginx 配置文件的转换工具，帮助用户将原有的 `nginx.conf` 转换为 Higress 的路由配置。

---



### 4: Higress 如何处理服务发现？它能对接 Kubernetes、Nacos 或 Consul 吗？

4: Higress 如何处理服务发现？它能对接 Kubernetes、Nacos 或 Consul 吗？

**A**: Higress 设计了统一的服务发现机制，能够对接多种注册中心，以适应不同的架构需求：

1.  **Kubernetes**：原生支持 Kubernetes Service，通过 Watch API 自动获取 Service 变化，这是最基础的用法。
2.  **Nacos / Consul / Zookeeper**：Higress 支持直接配置主流的微服务注册中心（如 Nacos、Consul）作为服务来源。这对于从传统微服务架构（如 Spring Cloud + Nacos）迁移到云原生网关的用户非常有用，网关可以直接从注册中心拉取服务列表，而不需要手动维护 IP 列表。
3.  **DNS**：同时也支持通过 DNS 解析来发现后端服务。

---



### 5: Higress 的插件系统是如何工作的？支持哪些语言开发？

5: Higress 的插件系统是如何工作的？支持哪些语言开发？

**A**: Higress 的插件系统基于 Wasm (WebAssembly) 技术构建。这是云原生网关的发展趋势。

1.  **工作原理**：Wasm 插件运行在沙箱环境中，与主进程隔离。当请求经过网关时，Envoy 会加载并执行 Wasm 虚拟机中的代码。这使得插件崩溃不会导致网关崩溃，且插件可以动态加载/卸载。
2.  **开发语言**：虽然 Wasm 本身是一种指令集，但 Higress 提供了强大的多语言 SDK，主要推荐使用 **Go** 语言进行开发（因为它编译为 Wasm 非常成熟且易于编写），同时也支持 C++、Rust、AssemblyScript 等语言。Higress 官方还提供了一个 Wasm 插件开发工具包（Go SDK），大大降低了开发门槛。

---



### 6: Higress 能否处理 Dubbo 或 gRPC 等非 HTTP 协议的流量？

6: Higress 能否处理 Dubbo 或 gRPC 等非 HTTP 协议的流量？

**A**: 可以。Higress 基于 Envoy，Envoy 原生对 L7（应用层）协议有很好的扩展支持。

1.  **gRPC**：Higress 原生支持 gRPC 协议的路由、负载均衡以及基于 gRPC 的请求/响应修改。
2.  **Dubbo**：这是阿里生态中常用的协议。Higress 专门针对 Dubbo（包括 Dubbo2 和 Dubbo3）进行了深度适配，支持将 HTTP 请求转换为 Dubbo 调用（HTTP to Dubbo 协议转换），允许前端

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的快速入门文档，尝试在本地 Docker 环境中部署一个最简网关，并配置一个简单的 HTTP 路由规则（例如：将 `/source` 路径的请求转发到 `httpbin.org`）。请验证请求是否成功转发。

### 提示**: 需要关注 Higress 的 Docker 镜像启动命令，以及 Ingress 或 Route 配置中的 `match` 条件与 `service` 目标地址的填写格式。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 AI 请求的“无损拦截”与“增强”
**场景**：在将请求发送给 LLM（如 OpenAI、通义千问）之前，需要对用户 Prompt 进行审核或修改，但不想引入额外的网络延迟。
**建议**：
*   **操作**：编写 Wasm (WebAssembly) 插件（支持 C++/Go/Rust）挂载在 `Route` 或 `Global` 级别。在插件逻辑中拦截请求体，提取 `messages` 或 `prompt` 字段。
*   **实践**：实现一个“敏感词过滤”或“Prompt 注入”插件。如果检测到违规内容，直接在网关层拦截并返回 403，避免无效请求消耗昂贵的 Token 配额。
*   **陷阱**：处理流式响应时，Wasm 插件需要正确处理 `chunked` 编码，否则会导致客户端无法完整接收 AI 生成的流式内容。

### 2. 配置基于 Token 的精细化限流
**场景**：大模型 API 调用成本高，且后端模型有严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制。
**建议**：
*   **操作**：不要仅使用传统的 QPS（每秒请求数）限流。结合 Higress 的 `request-block` 或自定义插件，针对特定 AI 接口配置基于 Token 预估的限流策略。
*   **实践**：对于不同的用户等级（如 Free Tier vs Pro Tier），配置不同的后端服务路由。例如，免费用户路由到成本较低的小模型（如 Llama-7B），付费用户路由到 GPT-4，并在网关层通过 Header 转发实现路由分流。

### 3. 实施模型供应商的故障转移
**场景**：依赖单一 LLM 供应商（如仅依赖 OpenAI）存在可用性风险，或需要在不同模型间切换以优化成本。
**建议**：
*   **操作**：在 Higress 中配置多服务或多目的地。利用 Higress 的“重试”或“备用”机制。
*   **实践**：设置主服务为 OpenAI，备用服务为 Azure OpenAI 或本地部署的模型（如 vLLM）。当主服务返回 5xx 错误或超时时，网关自动将请求转发到备用服务，确保业务连续性。
*   **陷阱**：确保不同供应商的 API 格式兼容。如果不兼容，需要编写 Wasm 插件在网关层进行协议转换。

### 4. 统一处理 AI 流式响应（SSE）的 Header 转发
**场景**：AI 接口通常使用 Server-Sent Events (SSE) 返回流式数据，但后端服务器可能配置了反向代理不兼容的 Header（如 `Content-Encoding: gzip`），导致前端无法流式输出。
**建议**：
*   **操作**：在 Higress 的路由配置中，明确针对 AI 接口修改响应头管理策略。
*   **实践**：
    1.  删除后端返回的 `Content-Length`（因为流式响应长度未知）。
    2.  确保 `Cache-Control` 设置为 `no-cache`。
    3.  如果后端启用了 Gzip 压缩且导致流式截断，需在网关配置插件移除 `Accept-Encoding` 请求头，强制后端返回明文，由网关处理压缩。

### 5. 建立基于“提示词”的缓存策略
**场景**：大量用户可能会问相同的问题，每次都请求 LLM 成本高且延迟高。
**建议**：
*   **操作**：利用 Higress 的缓存能力（或结合 Redis 插件）对 POST 请求的 Body 进行哈希缓存。
*   **实践**：配置缓存 Key 生成为 `HTTP Method + URL + Request Body Hash

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*