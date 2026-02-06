---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T19:27:16+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "阿里开源", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于提供的文档内容，以下是关于 **Higress** 的中文总结： **Higress** 是一个由阿里巴巴开源的、**云原生 AI 原生 API 网关**。它基于 **Go** 语言构建，核心架构建立在 **Istio** 和 **Envoy** 之上，并通过扩展 **WebAssembly (WASM)** 插件"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI Gateway | AI 原生 API 网关
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在通过云原生技术连接大模型与应用。它不仅提供传统的流量管理能力，还针对 LLM 应用提供了 AI 网关特性及 MCP 服务器托管，适合需要在微服务架构中集成 AI 能力的开发者。本文将介绍其核心架构、WASM 插件系统以及如何利用 AI 网关功能提升应用交付效率。

---
## 摘要

基于提供的文档内容，以下是关于 **Higress** 的中文总结：

**Higress** 是一个由阿里巴巴开源的、**云原生 AI 原生 API 网关**。它基于 **Go** 语言构建，核心架构建立在 **Istio** 和 **Envoy** 之上，并通过扩展 **WebAssembly (WASM)** 插件能力来实现高度的可扩展性。

**核心功能与架构特点：**

1.  **架构设计：** 采用控制平面（配置管理）与数据平面（流量处理）分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，特别适用于 AI 长连接流式响应场景。
2.  **三大核心用途：**
    *   **AI 网关：** 提供统一的 API 接入，支持 30 多家大语言模型（LLM）提供商。核心功能包括协议转换、可观测性、缓存和安全防护（涉及 `ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件）。
    *   **MCP 服务器托管：** 托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务（涉及 `mcp-router`、`jsonrpc-converter` 及具体实现）。
    *   **Kubernetes Ingress：** 作为 Ingress 控制器运行，兼容 nginx-ingress 注解，处理微服务路由。

**总结：** Higress 是一个专为 AI 应用和传统微服务设计的统一入口，旨在通过标准化的协议和强大的插件生态，简化 AI 应用的集成与管理。

---
## 评论

**总体判断**

Higress 是阿里云开源的、目前市场上最具前瞻性的“AI原生”网关之一。它成功地将云原生流量治理与 AI 大模型所需的语义处理、协议转换及工具调用能力融合，不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 MCP 协议解决了 AI 落地中的具体工程痛点，是企业构建 LLM 应用的理想基础设施。

**深度评价依据**

**1. 技术创新性：从“流量网关”向“语义网关”的范式转移**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并引入了 WebAssembly (WASM) 插件系统和 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 L7 层的 HTTP 负载均衡，对 AI 语义无感知。Higress 的差异化在于它不仅转发流量，还能理解流量。它内置了对 LLM 协议的兼容处理（如将 OpenAI 协议转为 Huggingface 或通义千问格式），并利用 WASM 技术实现了业务逻辑与网关内核的热解耦。这种设计允许开发者用 C++/Go/Rust/JS 编写高性能插件，在网关层直接实现 Prompt 注入、敏感词过滤或 Token 计费，无需修改后端应用代码。

**2. 实用价值：解决 AI 落地中的“碎片化”与“异构”难题**
*   **事实**：DeepWiki 提及其核心功能包括“AI Gateway Features for LLM applications”和“MCP server hosting for AI agent tool integration”。
*   **推断**：在构建 AI Agent 时，开发者面临两大痛点：一是大模型供应商的 API 标准不一（切换模型需改代码），二是 Agent 调用外部工具时的鉴权与路由管理复杂。Higress 直接解决了这些问题。它充当了“模型适配器”，屏蔽了底层模型差异；同时作为 MCP Host，它让网关变成了 Agent 的工具调度中心，统一管理 SaaS 工具的 API 调用。这使得企业可以在不暴露后端微服务细节的情况下，安全、高效地对外暴露 AI 能力。

**3. 代码质量与架构：云原生控制与数据平面的标准解耦**
*   **事实**：仓库采用 Go 语言编写，架构明确分离了控制平面和数据平面，且文档覆盖了从核心架构到开发指南的完整链路。
*   **推断**：基于 Envoy 的数据平面保证了极高的并发处理能力（C++ 内核级性能），而 Go 语言编写的控制平面利用了 Kubernetes 的 Operator 模式，符合云原生社区的最佳实践。这种架构不仅保证了网关本身的稳定性（高可用），还确保了配置变更的实时性。文档的多语言支持（中/日/英）也体现了阿里云对开源国际化的重视，降低了上手门槛。

**4. 社区与生态：背靠阿里，连接 AI 生态的枢纽**
*   **事实**：星标数 7,469（且持续增长中），由阿里巴巴维护，且深度集成了 WASM 和 MCP 等新兴技术标准。
*   **推断**：相比于单纯的社区项目，Higress 有阿里云内部大规模生产环境的背书，避免了“玩具项目”的常见陷阱。它积极拥抱 WASM 云原生生态和 OpenAI/MCP 协议标准，使其不仅仅是一个网关，更是一个连接 Kubernetes 世界与 AI 模型世界的“路由器”。社区活跃度较高，对于国内开发者而言，中文文档和响应速度是巨大的加分项。

**5. 学习价值与对比优势**
*   **对比优势**：与 **Kong** 或 **APISIX** 相比，Higress 最大的优势在于“开箱即用”的 AI 特性。传统网关处理 AI 流流需要编写复杂的 Lua 或 Python 插件来处理 SSE 流或 Token 统计，而 Higress 将这些能力原生集成。与 **LangChain** 等 Python 框架相比，Higress 提供了基础设施层的治理能力，而非应用层的逻辑编排。
*   **学习价值**：开发者可以通过研究 Higress 学习到如何将 Envoy 的 Filter 机制应用于 AI 流处理，以及如何设计一个兼容 Kubernetes Ingress 的云原生控制器。

**边界条件与验证清单**

**不适用场景**
*   **极致轻量级边缘部署**：如果仅需在边缘端（如 IoT 设备）进行简单的 HTTP 转发，Envoy 的资源占用可能过重，轻量级 Nginx 或 Caddy 更合适。
*   **纯业务逻辑处理**：网关应专注于流量和协议治理，不应将复杂的业务计算（如长时间的视频转码、大规模数据处理）放入网关插件中，否则会阻塞网络 I/O。

**快速验证清单**
1.  **协议转换测试**：部署 Higress，配置一个后端服务（如通义千问），通过 Postman 发送标准的 OpenAI 格式请求，验证网关是否能自动转换并成功返回结果。
2.  **WASM 插件热加载**：编写一个简单的 WASM 插件（如修改 HTTP Header），在不重启网关的情况下加载插件，观察流量是否立即受影响，验证其动态性。
3.  **MCP 代理能力**：尝试配置一个 MCP Server，检查网关是否能正确处理 AI Agent 对该工具的调用请求，并验证鉴权是否生效。

---
## 技术分析

基于对 Alibaba Higress 仓库（特别是 v1.3+ 版本引入 AI Gateway 特性后）的深入分析，以下是关于该项目的全面技术评估。

---

# 1. 技术架构深度剖析

Higress 的架构设计体现了**"深度继承云原生生态，差异化创新 AI 能力"**的策略。

*   **技术栈与架构模式**：
    *   **底层基座**：基于 **Istio**（控制平面）和 **Envoy**（数据平面）。这意味着 Higress 天然继承了云原生生态的黄金标准，利用 Envoy 的高性能 C++ 网络处理能力和 Istio 的成熟控制面逻辑。
    *   **架构模式**：采用标准的控制面与数据面分离架构。
        *   **控制面**：负责配置管理（通过 K8s CRD 或控制台 UI）、路由规则下发、WASM 插件管理。它将 Istio 的控制面进行了"裁剪"和"增强"，移除了 Sidecar 模式的复杂性，专注于 Gateway 模式。
        *   **数据面**：基于 Envoy，处理实际的流量转发、负载均衡、协议转换。
    *   **扩展机制**：核心亮点在于 **WASM (WebAssembly)** 插件系统。Higress 支持在 C++/Go/Rust 中编写插件，编译为 WASM 字节码后动态挂载到 Envoy 中。这打破了传统 Nginx Lua 插件的性能瓶颈和语言限制。

*   **核心模块**：
    *   **Router (路由)**：支持 HTTP、HTTPS、gRPC，以及基于 AI 语义的路由。
    *   **WASM Plugin System (插件市场)**：提供了开箱即用的插件（如鉴权、限流、请求/响应修改）。
    *   **AI Native Layer (AI 原生层)**：这是最新的核心模块，专门用于处理 LLM（大语言模型）流量，支持 Provider 转换、Prompt 模板管理和结果处理。

*   **架构优势**：
    *   **热更新能力**：基于 xDS 协议，配置变更毫秒级生效，且无需重启数据面进程，这对于长连接（如 SSE 流式响应）至关重要。
    *   **生态隔离**：WASM 插件运行在沙箱中，插件崩溃不会导致网关崩溃，且支持多语言开发。

# 2. 核心功能详细解读

Higress 正在从一个传统的 API 网关向 **AI Native Gateway** 演进。

*   **主要功能与场景**：
    1.  **AI 网关（核心差异化功能）**：
        *   **统一协议转换**：将不同 LLM 厂商（OpenAI, Anthropic, 通义千问等）的异构 API 统一化为标准接口（如 OpenAI 格式）。业务方只需对接一个网关，即可灵活切换后端模型。
        *   **Token 计费与流控**：针对 LLM 的 Token 计数进行精细化限流，而非传统的 HTTP 请求数限流。
        *   **提示词管理**：在网关层进行 Prompt 模板注入和变量替换，减轻业务代码负担。
    2.  **MCP (Model Context Protocol) 服务器托管**：
        *   Higress 能够托管 MCP Server，充当 AI Agent 与外部数据/工具之间的桥梁。它解决了 Agent 如何安全、标准化地调用外部工具的问题。
    3.  **传统微服务网关**：
        *   K8s Ingress 支持、服务发现（Nacos, Consul, DNS）、全链路灰度发布、金丝雀发布。

*   **解决的关键问题**：
    *   **AI 供应商锁定**：通过统一适配层，企业可以在不同模型间无缝切换，无需修改业务代码。
    *   **AI 流量的不可观测性**：提供针对 AI 请求的日志、指标和追踪，记录 Token 消耗和模型响应时间。
    *   **长连接处理**：针对 LLM 流式输出的 SSE（Server-Sent Events）场景进行了深度优化，确保在流式传输中的网关转发性能。

*   **与同类工具对比**：
    *   **VS Nginx/APISIX**：Higress 基于 Envoy，C++ 事件驱动模型在处理高并发长连接时比 Nginx/OpenResty 的 Lua 协程模型在某些极端场景下更稳定，且 WASM 的隔离性优于 Lua。
    *   **VS Kong**：Kong 基于 Nginx/OpenResty，生态成熟但架构较重。Higress 更轻量，且深度绑定 K8s/Istio 生态，对云原生应用更友好。
    *   **VS 专用 AI Gateway (如 OneGateway)**：Higress 的优势在于它**同时**具备传统流量管理和 AI 流量管理能力，企业无需部署两套网关。

# 3. 技术实现细节

*   **关键技术方案**：
    *   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM 运行时。这允许开发者用 Go 编写插件，编译为 `.wasm` 文件。Higress 实现了插件配置的动态热加载，利用 `xDS` 协议将配置推送到 Envoy，Envoy 加载 WASM 模块并执行。
    *   **配置分发**：Higress Controller 监听 K8s API Server 的资源变化，将其转换为 Istio 的 Gateway/VirtualService 配置，并最终转化为 Envoy 的 xDS 配置下发。
    *   **AI 流量处理**：在数据面实现了针对 HTTP Body 的流式处理逻辑。对于 LLM 的 SSE 流，网关不仅是透传，还能进行分片缓冲、语义分析（如提取 Token 数）和实时拦截。

*   **代码组织**：
    *   仓库主要分为 `pkg`（核心逻辑）、`plugins`（WASM 插件源码）、`docker`（镜像构建）、`test`（E2E 测试）。
    *   **设计模式**：大量采用 **CRD (Custom Resource Definition)** 模式。用户通过 YAML 定义路由和插件，Controller 通过 Informer 模式监听并处理。

*   **性能优化**：
    *   利用 Envoy 的高性能网络栈。
    *   WASM 插件虽然比原生 C++ 慢，但比 Lua 快，且通过 AOT (Ahead-of-Time) 编译优化启动速度。
    *   针对流式传输，优化了内存缓冲策略，避免大 Body 回传导致网关内存 OOM。

# 4. 适用场景分析

*   **最适合的项目**：
    *   **云原生微服务架构**：特别是已经使用 Istio 或 K8s 的企业，Higress 可以无缝融入。
    *   **集成大模型能力的应用**：需要同时调用多个 LLM 厂商 API，或需要对 AI 接口进行统一鉴权、限流、缓存的企业应用。
    *   **需要高度定制扩展的网关**：业务逻辑复杂，需要在网关层通过代码（WASM）实现特定逻辑（如特殊的签名算法、请求体改造）。

*   **最有效的情况**：
    *   当你需要将 AI 能力集成到现有微服务，且希望**零代码改造**现有业务逻辑，仅通过网关配置实现模型切换和 Prompt 管理。
    *   当你需要处理**高并发流式 AI 请求**，且要求网关转发延迟极低。

*   **不适合的场景**：
    *   **非 K8s 环境**：虽然支持 Docker 部署，但 Higress 强依赖 K8s 的 CRD 体系，在虚拟机或裸金属环境下的管理复杂度高于 Nginx。
    *   **极简静态站点托管**：对于简单的静态资源服务，Higress 过于重量级。
    *   **极端依赖 Lua 生态**：如果你有大量基于 OpenResty 的 Lua 脚本，迁移到 Higress (WASM) 需要重写插件，成本较高。

*   **集成注意事项**：
    *   部署前需规划好 Service Mesh 的边界，避免控制面冲突。
    *   WASM 插件编写需注意内存限制，避免无限循环阻塞 Envoy 线程。

# 5. 发展趋势展望

*   **技术演进**：
    *   **AI Gateway 的标准化**：Higress 正在推动 AI 网关的标准化（如支持 OpenAI SDK 兼容协议），未来可能成为 LLM 流量管理的标准 Sidecar/Gateway。
    *   **MCP 协议的深度整合**：随着 AI Agent 的爆发，作为 MCP Server 的托管层将成为核心增长点。
    *   **WASM 生态的组件化**：未来可能出现更多官方维护的 WASM 插件市场，用户像搭积木一样配置网关功能。

*   **社区反馈**：
    *   阿里内部大规模使用验证了其稳定性。
    *   社区主要关注点在于 AI 功能的丰富度（如 RAG 支持）以及与传统监控系统的集成。

# 6. 学习建议

*   **适合人群**：
    *   **中高级后端工程师/运维/SRE**：需要具备 K8s、Docker 基础，理解网络协议（HTTP/TCP）。
    *   **AI 应用开发者**：希望掌握生产环境 LLM 落地基础设施的开发者。

*   **学习路径**：
    1.  **基础**：熟悉 Istio 和 Envoy 的基本概念（Sidecar, xDS, Listener, Cluster）。
    2.  **实践**：在本地 Kind/Minikube 环境部署 Higress，配置一个简单的 Ingress 路由。
    3.  **进阶**：尝试编写一个 Go WASM 插件（如添加一个 HTTP Header），并体验热更新。
    4.  **AI 特性**：配置 AI Provider，使用 `curl` 模拟 OpenAI Client 请求 Higress，观察其如何转发至通义千问或其他模型。

# 7. 最佳实践建议

*   **正确使用方式**：
    *   **资源隔离**：在生产环境中，建议将 Higress 的控制面与数据面分开部署，或使用 HPA (Horizontal Pod Autoscaler) 应对流量突发。
    *   **插件开发**：优先使用官方预置插件。自定义 WASM 插件时，务必设置 CPU 和内存限制，防止插件异常拖垮网关。
    *   **AI 缓存**：对于相同的 Prompt 请求，开启网关层的缓存功能（如果业务允许），以降低 LLM API 调用成本。

*   **常见问题**：
    *   **流式响应中断**：检查后端服务的超时设置，确保网关的超时时间大于 LLM 生成时间。
    *   **WASM 插件加载失败**：通常是架构不匹配（amd64/arm64）或导入包路径问题，需在构建时严格指定 `GOOS=js GOARCH=wasm`。

*   **性能优化**：
    *   调整 Envoy 的 Worker 线程数与 CPU 核心数一致。
    *   在高吞吐场景下，开启访问日志的

---
## 代码示例




```python
# 示例1：使用Higress实现简单的API网关路由
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """模拟用户API端点"""
    users = [
        {"id": 1, "name": "张三"},
        {"id": 2, "name": "李四"}
    ]
    return jsonify(users)

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    """模拟产品API端点"""
    products = [
        {"id": 101, "name": "笔记本电脑"},
        {"id": 102, "name": "无线鼠标"}
    ]
    return jsonify(products)

if __name__ == '__main__':
    # 在实际Higress部署中，这些路由会被配置为网关规则
    app.run(host='0.0.0.0', port=8080)
```




```python
# 示例2：模拟Higress的限流功能
from time import time
from collections import deque

class RateLimiter:
    def __init__(self, rate, per):
        """
        限流器类
        :param rate: 限流数量
        :param per: 时间窗口(秒)
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time()
        self.requests = deque()

    def allow(self):
        """检查是否允许请求"""
        current = time()
        time_passed = current - self.last_check
        self.last_check = current
        
        # 令牌桶算法
        self.allowance += time_passed * (self.rate / self.per)
        if self.allowance > self.rate:
            self.allowance = self.rate
        
        if self.allowance < 1:
            return False
        else:
            self.allowance -= 1
            return True

# 使用示例
limiter = RateLimiter(rate=10, per=60)  # 每分钟10次请求
for i in range(15):
    if limiter.allow():
        print(f"请求 {i+1}: 允许通过")
    else:
        print(f"请求 {i+1}: 被限流")
```




```python
# 示例3：模拟Higress的负载均衡策略
import random

class ServiceInstance:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.current_requests = 0

class LoadBalancer:
    def __init__(self):
        self.instances = []
    
    def add_instance(self, instance):
        self.instances.append(instance)
    
    def weighted_round_robin(self):
        """加权轮询负载均衡算法"""
        if not self.instances:
            return None
            
        total_weight = sum(inst.weight for inst in self.instances)
        rand = random.uniform(0, total_weight)
        cumulative = 0
        
        for instance in self.instances:
            cumulative += instance.weight
            if rand <= cumulative:
                instance.current_requests += 1
                return instance.name
        
        return self.instances[-1].name

# 使用示例
lb = LoadBalancer()
lb.add_instance(ServiceInstance("服务A", 3))
lb.add_instance(ServiceInstance("服务B", 2))
lb.add_instance(ServiceInstance("服务C", 1))

# 模拟10次请求分发
for _ in range(10):
    selected = lb.weighted_round_robin()
    print(f"请求被分发到: {selected}")
```


---
## 案例研究


### 1：某大型电商平台双11大促

 1：某大型电商平台双11大促

**背景**: 
该电商平台拥有数百万日活用户，业务架构基于微服务模式，包含数百个后端服务。每逢大促（如双11），流量会呈现数十倍的瞬时爆发。

**问题**: 
原有的开源 Kong 网关在处理每秒数十万级 QPS 请求时，延迟显著升高，且出现 CPU 负载不均的情况。此外，多语言（Java、Go、Python）服务的鉴权逻辑重复开发，维护成本极高。由于传统网关配置修改需要重启，导致在大促期间无法灵活应对突发流量调整。

**解决方案**: 
全面迁移至 Higress 作为云原生 API 网关。利用 Higress 的高性能 Istio 数据面代理，结合其内置的 Wasm 插件市场，实现了通过 Lua 或 Wasm 编写一次鉴权逻辑即可在所有服务间生效。同时，利用 Higress 对 Nacos 和 Consul 的原生支持，实现了服务发现的无缝对接。

**效果**: 
网关吞吐量提升了 50%，P99 延迟降低了 30%。通过 Wasm 插件实现了业务逻辑与网关的解耦，热加载功能使得配置变更无需重启，保障了大促期间 100% 的服务可用性。

---



### 2：某跨国 AI 创业公司

 2：某跨国 AI 创业公司

**背景**: 
该公司主要业务是向全球用户提供基于 LLM（大语言模型）的对话生成服务。其后端同时接入了 OpenAI、Azure OpenAI 以及自研的模型服务，需要统一对外暴露 API。

**问题**: 
直接调用第三方模型 API 成本高昂，且缺乏统一的流量控制。在处理高并发请求时，不同模型提供商的接口参数差异巨大，导致客户端 SDK 集成困难。同时，缺乏有效的 Prompt 模板管理和缓存机制，导致 Token 消耗过大。

**解决方案**: 
部署 Higress 作为 AI 服务的统一网关。利用 Higress 的 AI 插件特性，实现了多模型提供商的统一协议转换。配置了提示词缓存和语义缓存插件，对相似的用户提问进行短时间缓存，减少对后端模型的直接调用。同时，通过 Higress 实现了基于 Token 的精细化流控，防止个别用户恶意刷量。

**效果**: 
后端模型调用成本降低了 40%，统一了客户端调用接口，开发效率提升。通过精准的流控策略，成功拦截了恶意爬虫流量，保障了付费用户的体验稳定性。

---



### 3：某互联网金融科技公司

 3：某互联网金融科技公司

**背景**: 
该公司提供支付、借贷等核心金融服务，对系统的一致性和安全性要求极高。随着业务从单体架构向云原生容器化架构迁移，原有的 Nginx Ingress 配置管理变得日益复杂，且难以与微服务治理体系打通。

**问题**: 
运维团队面临严重的配置漂移问题，手动修改 Nginx 配置容易导致误操作。同时，需要在网关层面实现更复杂的灰度发布（金丝雀发布）策略，而传统的 Ingress Controller 对基于 Header、Cookie 或权重的流量路由支持不够灵活。此外，需要对接内部的 OAuth2.0 认证系统。

**解决方案**: 
引入 Higress 替换原有的 Nginx Ingress。利用 Higress 与 K8s Ingress API 的完美兼容性，平滑迁移现有配置。通过 Higress 的全链路灰度发布功能，实现了按用户画像的精细化流量路由。集成 OIDC 认证插件，统一接管了所有流量的安全认证。

**效果**: 
实现了配置的版本化管理，消除了配置漂移风险。灰度发布的效率提升，新版本上线回滚时间从分钟级降低到秒级。统一的安全认证拦截了 99.9% 的非法请求，显著提升了系统的安全性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和LuaJIT | 极高性能，基于LuaJIT和Nginx |
| 易用性 | 提供控制台和Kubernetes集成，配置较简单 | 提供管理界面和丰富的插件，配置灵活 | 提供Dashboard和API，配置较复杂 |
| 成本 | 开源免费，企业版收费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持自定义插件和Wasm扩展 | 支持Lua插件和自定义扩展 | 支持Lua插件和自定义扩展 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，插件丰富 | 社区活跃，国内支持较好 |
| 安全性 | 内置WAF和限流功能 | 需要额外配置安全插件 | 内置安全功能，需额外配置 |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态集成更好，适合Kubernetes环境。
- 优势2：阿里巴巴背书，技术支持可靠，适合企业级应用。
- 优势3：内置WAF和流量管理功能，开箱即用，减少额外配置。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态和社区资源较少。
- 不足2：学习曲线较陡峭，对Envoy和Istio的依赖可能增加复杂度。
- 不足3：企业版功能可能需要付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WebAssembly (Wasm) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写自定义插件。相比传统网关插件，Wasm 插件具有沙箱隔离、高性能、动态加载和热更新的优势，且无需重新编译或重启网关即可生效。

**实施步骤**:
1. 确定业务逻辑需求（如自定义认证、请求头转换、流量染色）。
2. 选择合适的语言开发 Wasm 插件，并利用 Higress 提供的 Proxy-Wasm SDK。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或配置为 OCI 镜像仓库地址。
4. 在网关规则中针对特定路由或全局作用域启用该插件，并配置相关参数。

**注意事项**: Wasm 插件虽然执行效率高，但在处理极高并发时仍需注意内存消耗；建议在插件中实现超时控制，避免阻塞网关主线程。

---

### 实践 2：利用 Ingress API 实现服务自动化接入

**说明**: Higress 原生兼容 Kubernetes Ingress API 和 Gateway API。通过标准的 Kubernetes 资源配置（YAML），即可实现从容器服务到网关路由的自动化同步，无需在 Higress 控制台手动配置，适合云原生应用的全自动化部署流程。

**实施步骤**:
1. 在 Kubernetes 集群中部署 Higress Gateway。
2. 编写 Ingress 或 Gateway API 资源定义，指定 Host、Path 以及后端 Service。
3. 应用配置文件，Higress Controller 会自动监听集群变更并更新路由规则。
4. 验证流量是否正确转发至对应的 Pod。

**注意事项**: 在大规模微服务场景下，建议使用 Gateway API 以获得更丰富的路由匹配能力和协议支持；同时需关注 Ingress 控制器的同步延迟。

---

### 实践 3：配置精细化的流量治理与金丝雀发布

**说明**: Higress 提供了强大的全链路流量管理能力。通过配置 Header 匹配、权重百分比或 Cookie 参数，可以轻松实现蓝绿部署、金丝雀发布和 A/B 测试，确保新版本上线的平滑过渡。

**实施步骤**:
1. 准备两个不同版本的 Service（例如 v1 和 v2）。
2. 在 Higress 中创建路由规则，配置默认指向 v1 版本。
3. 添加一条带匹配条件（如特定 Header 或基于权重的分流）的规则，将部分流量导向 v2 版本。
4. 逐步增加 v2 版本的流量权重，观察监控指标，直至全量切换。

**注意事项**: 金丝雀发布期间必须保持全链路 Tracing 的透传，确保流量标记在服务调用链中不丢失；同时准备好快速回滚机制。

---

### 实践 4：对接服务注册中心实现服务发现

**说明**: Higress 能够无缝对接 Nacos、Consul、ZooKeeper 以及 Kubernetes Core DNS。通过引入服务注册中心，网关可以动态感知服务实例的上下线，实现基于服务名的负载均衡，避免了硬编码 IP 地址带来的维护难题。

**实施步骤**:
1. 在 Higress 全局配置中添加对应类型的注册中心源（如 Nacos 地址）。
2. 配置服务来源的命名空间和访问凭证。
3. 在创建路由时，服务类型选择“服务发现”，并输入注册的服务名称。
4. 配置健康检查机制，确保网关只转发流量至健康的实例节点。

**注意事项**: 确保网关网络与注册中心网络互通；对于非 K8s 服务，需注意处理服务名过长或包含特殊字符的兼容性问题。

---

### 实践 5：实施全方位的安全防护策略

**说明**: Higress 内置了多种安全防护机制，包括 IP 黑白名单、严格的路由匹配规则以及对接 WAF（Web Application Firewall）。通过配置这些策略，可以有效防御 SQL 注入、XSS 攻击以及恶意流量刷单。

**实施步骤**:
1. 在全局或特定路由下配置 IP 访问控制，限制只允许特定网段访问。
2. 启用 Higress 内置的防护插件或对接开源 WAF（如 Lua-resty-waf）。
3. 开启 CORS（跨域资源共享）配置，防止非法跨域请求。
4. 对于后端 API，配置 JWT 或 OAuth2.0 认证插件，保护接口安全。

**注意事项**: 安全策略配置过于严格可能会误拦截正常流量，建议先在“监控模式”或“拦截并记录”模式下运行一段时间，观察无误后再开启严格拦截。

---

### 实践 6：构建基于 Prometheus 的可观测性体系

**说明**: Higress 默认暴露 Prometheus 兼容的 Metrics 接口。通过采集这些指标，可以实时监控网关的 QPS、响应延迟、错误率以及后端服务的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 绑定

**说明**: Higress 的数据面基于 Envoy，通过将 Envoy 进程绑定到固定的 CPU 核心，可以减少上下文切换带来的开销，并最大化利用 CPU 的 L1/L2/L3 缓存，从而显著提升数据面的转发效率。

**实施方法**:
1. 在容器启动配置中设置资源限制，确保 CPU 核心数与 Envoy 工作线程数一致。
2. 修改 Higress Gateway 的部署 YAML，添加 `istio-proxy` 容器的环境变量 `CPU_LIMIT` 和 `CPU_PIN`。
3. 在 Kubernetes 中使用 `CPU Manager` 策略为 `Guaranteed` QoS 的 Pod 分配独占 CPU 资源。

**预期效果**: 在高并发场景下，长尾延迟可降低 10%-20%，吞吐量提升 5%-15%。

---

### 优化 2：调整连接池与缓冲区大小

**说明**: 默认的 Envoy 配置较为保守，对于高吞吐量的内部服务（如微服务间调用或对接 K8s Service），适当增加上游和下游连接池的大小以及缓冲区上限，可以减少频繁建立连接的开销。

**实施方法**:
1. 修改 EnvoyFilter 或全局配置，调整 `http.connect_timeout` 和 `http.max_requests_per_connection`。
2. 针对特定服务增加 `cluster` 级别的连接池配置，例如将 `max_connections` 从默认值提升至 512 或更高。
3. 调整 `per_connection_buffer_limit_bytes` 以适应大包传输场景（如大文件上传或 gRPC 流）。

**预期效果**: 在高 QPS 场景下，连接建立失败率降低至 0，请求响应延迟（P99）减少 10%-30%。

---

### 优化 3：启用 HTTP/2 与 HTTP/3 (QUIC)

**说明**: Higress 支持 HTTP/2 和 HTTP/3。HTTP/2 通过多路复用减少 TCP 连接数，HTTP/3 (QUIC) 则基于 UDP 解决了 TCP 队头阻塞问题。对于客户端到网关的链路，启用新协议可显著提升弱网环境下的性能。

**实施方法**:
1. 在网关监听器配置中，启用 `HTTP2` 协议支持。
2. 如需使用 QUIC，需在 Listener 配置中开启 `QUIC` 选项，并确保 UDP 端口（通常为 443）在防火墙和 LoadBalancer 层开放。
3. 确保后端服务也支持 HTTP/2 以实现端到端的协议升级。

**预期效果**: 弱网环境下请求成功率提升 20% 以上，页面加载总时间（TLCP）减少 15%-40%。

---

### 优化 4：优化日志采样与异步上报

**说明**: 在高流量下，同步打印访问日志或全量日志会严重消耗 CPU 和磁盘 I/O，成为性能瓶颈。通过异步日志上报和采样策略，可以在保留关键可观测性数据的同时降低系统负载。

**实施方法**:
1. 配置 Higress 将访问日志输出到 stdout，由 Fluentd/Fluent Bit 侧车容器异步采集，而非 Higress 进程直接写盘。
2. 开启 Envoy 的 Access Log Sampling 功能，仅记录特定比例（如 10%）或特定条件的日志。
3. 使用 OpenTelemetry 协议导出遥测数据，并配置合理的批处理间隔。

**预期效果**: CPU 使用率降低 10%-25%，磁盘 I/O 写入量减少 50%-90%。

---

### 优化 5：启用本地与分布式缓存

**说明**: Higress 内置了强大的缓存能力。对于响应变化不频繁的 GET 请求，启用网关层缓存可以直接命中返回，避免流量穿透到后端业务逻辑，减轻后端压力并降低端到端延迟。

**实施方法**:
1. 在路由配置中启用缓存策略，配置基于 HTTP Header（如 `Cache-Control`）的缓存规则。
2. 对于需要更高性能

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态
- 提供了 WAF 插件支持，能够有效防范 SQL 注入、XSS 等 Web 安全威胁
- 兼容 Ingress 与 Gateway API 标准，支持从 Nginx Ingress 等传统网关平滑迁移
- 具备高性能流量处理能力，支持热更新与动态配置，可实现秒级服务扩容
- 内置丰富的流量管理插件，支持金丝雀发布、蓝绿部署及负载均衡策略
- 提供标准化的 Wasm 插件市场，支持使用 Go/Python/JavaScript 等语言编写扩展逻辑
- 拥有可视化的控制台，极大降低了服务治理、安全配置和路由规则的管理门槛


---
## 学习路径

## 学习路径

### 阶段 1：概念认知与基础环境搭建

**学习内容**:
- 理解云原生网关的核心概念：API网关、流量入口、南北向流量与东西向流量
- 了解 Higress 的定位：基于 Envoy 和 Istio 的下一代网关
- 掌握 Docker 基础知识，因为 Higress 通常以容器化方式部署
- 学习基本的网络协议知识：HTTP/HTTPS、HTTP/2、gRPC、WebSocket
- Higress 的本地部署与安装（Docker Desktop 或 Kubernetes 环境）

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：快速入门章节
- Envoy 官方文档基础介绍（了解数据平面概念）
- Docker 官方入门教程

**学习建议**:
不要急于一开始就深入配置。首先在本地成功运行一个 Higress 实例，并访问控制台（Console）。理解 Higress 是如何作为“流量大门”存在的，对比 Nginx 或传统硬件负载均衡器的区别。

---

### 阶段 2：核心功能实操与流量管理

**学习内容**:
- 掌握 Higress 控制台的使用界面
- 配置域名与路由：实现基于域名的转发、路径匹配、Header 匹配
- 服务来源管理：如何注册 Nacos、Consul、固定地址或 K8s Service 的服务
- 流量治理插件：了解插件市场，使用 CORS、重定向、请求头修改等常用插件
- 负载均衡策略：轮询、随机、一致性哈希等配置
- 全局与精细化限流配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：路由配置、服务来源、插件市场
- Higress 官方示例：Github 中的 examples 目录
- Kubernetes Service 基础知识（如果在 K8s 中部署）

**学习建议**:
动手搭建一个简单的微服务场景（例如两个后端服务），通过 Higress 将流量路由到这两个服务。尝试配置不同规则，观察流量走向。重点体验“插件”功能，这是 Higress 区别于传统网关的一大特色（Wasm 支持）。

---

### 阶段 3：高级安全、可观测性与 Wasm 插件开发

**学习内容**:
- 安全认证：配置 Basic Auth、Jwt Auth、ApiKey 认证
- 金丝雀发布与蓝绿发布：实现流量的灰度切换
- 可观测性：对接 Prometheus/Grafana 监控指标，配置日志服务（SLS/ELK），链路追踪
- Wasm (WebAssembly) 插件开发：使用 Go 或 C++ 编写自定义插件
- 高可用部署：在 Kubernetes 集群中的生产级配置

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：高阶流量治理、安全鉴权、自定义 Wasm 插件开发
- WebAssembly (Wasm) 基础教程
- Prometheus 监控最佳实践白皮书

**学习建议**:
这是从“使用者”向“专家”转变的关键阶段。建议尝试编写一个简单的 Wasm 插件（例如修改请求响应体或实现特定的鉴权逻辑），并部署到 Higress 中。同时，重点关注生产环境必备的监控和日志链路，学会如何排查网关层面的性能瓶颈。

---

### 阶段 4：生态集成与架构优化

**学习内容**:
- Higress 与阿里云云原生产品的集成（MSE、ACK、ARMS）
- 服务网格集成：Higress 作为 Istio 的 Ingress Gateway 使用
- 多集群 ingress 管理与多租户隔离
- 性能调优：连接池配置、缓冲区调整、并发处理优化
- Higress 的源码分析与架构设计原理（基于 Envoy 的动态配置机制）

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Istio 官方文档（Ingress Gateway 章节）
- Envoy 深度解析技术博客
- 阿里云云原生 API 网关白皮书

**学习建议**:
结合实际业务架构思考 Higress 的位置。如果是阿里云用户，深入研究 MSE 网关托管版的优势。阅读源码，理解 Higress 如何通过配置翻译将控制台的配置转化为 Envoy 的 xDS 协议下发，这有助于在遇到深层 Bug 时进行排查。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在开源网关 Envoy 和 Istio 的基础上进行构建和优化的。

与 Nginx 和 Kong 的主要区别如下：
1.  **架构基础**：Nginx 主要基于 C/S 架构和内存管理，Kong 基于 Nginx 和 OpenResty（Lua），而 Higress 深度集成了 Envoy（C++/L4/L7 高性能代理）和 Istio（服务网格控制平面）。Higress 的数据层使用 Envoy，具有极高的性能和可扩展性。
2.  **云原生集成**：Higress 原生支持 Kubernetes 和 Istio，可以作为 Ingress Controller 或 API 网关使用，能够直接纳管 Istio 下的服务，实现从“南向”（入口流量）到“西向”（服务间流量）的统一管理。
3.  **扩展性**：Higress 提供了 Wasm (WebAssembly) 插件市场，支持使用 Go、C++、Rust 等多种语言编写插件，比传统的 Nginx C 模块或 Kong 的 Lua 脚本更安全、更灵活且易于热加载。

---



### 2: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

2: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

**A**: 是的，Higress 非常重视迁移的便利性，提供了多种工具和兼容性支持：

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，可以帮助用户将现有的 Nginx 配置转换为 Higress 的路由配置。
2.  **Kubernetes Ingress 注解支持**：作为 Ingress Controller 运行时，Higress 兼容主流的 Kubernetes Ingress 注解，这意味着如果你正在使用 Nginx Ingress Controller，通常只需要修改少量的注解或直接使用标准 Ingress 资源即可切换到 Higress。
3.  **网关资源迁移**：对于阿里云 API 网关的用户，Higress 提供了专门的迁移工具，可以一键导入现有的 API 分组和配置。

---



### 3: Higress 的性能表现如何？能否应对高并发场景？

3: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 的性能表现非常优异，设计之初就是为了应对阿里云超大规模的流量冲击。

1.  **底层优势**：得益于 Envoy 的高性能异步非阻塞 I/O 模型，Higress 在处理长连接、高并发请求时延迟极低，资源占用（CPU/内存）相比传统的基于 Lua 的网关（如 Kong）通常更低。
2.  **弹性伸缩**：作为云原生网关，Higress 可以结合 K8s 的 HPA（水平自动伸缩）进行快速扩容，以应对流量洪峰。
3.  **冷启动优化**：Higress 对配置加载和路由分发进行了深度优化，能够在极短的时间内完成大量路由规则的加载，适合微服务架构下路由数量庞大的场景。

---



### 4: 如何在 Higress 中扩展功能？是否必须修改代码重新编译？

4: 如何在 Higress 中扩展功能？是否必须修改代码重新编译？

**A**: 不需要重新编译网关程序。Higress 采用了现代化的插件系统，极大地降低了扩展门槛：

1.  **Wasm 插件**：这是 Higress 推荐的扩展方式。用户可以使用 Go、AssemblyScript、Rust 或 C++ 编写业务逻辑，编译成 `.wasm` 文件后，直接通过控制台或 API 上传即可动态加载。
2.  **热加载**：Wasm 插件支持热加载，上传后无需重启网关进程即可生效，这保证了业务的高可用性。
3.  **插件市场**：Higress 社区维护了官方插件市场，内置了 JWT 鉴权、请求鉴权、流量镜像、Keyless 认证等常用插件，用户可以直接开箱即用。

---



### 5: Higress 和 Istio 的关系是什么？我是否需要先安装 Istio？

5: Higress 和 Istio 的关系是什么？我是否需要先安装 Istio？

**A**: Higress 与 Istio 关系紧密，但**不需要**必须先安装 Istio 才能使用 Higress。

1.  **独立使用**：Higress 可以作为一个独立的 API 网关或 Ingress Controller 部署在 Kubernetes 集群中，接管集群的南北向流量。
2.  **集成使用**：如果你的集群中已经安装了 Istio，Higress 可以作为 Istio 的入口网关。它能够自动发现 Istio 注册的服务，实现流量从 API 网关到 Sidecar 的无缝透传。
3.  **架构定位**：你可以把 Higress 看作是 Istio Ingress Gateway 的增强版，它解决了原生 Istio Ingress 配置复杂、缺乏标准网关管理界面（如控制台、鉴权、插件市场）等问题。

---



### 6: Higress 对 Dub

6: Higress 对 Dub

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 快速上手与环境验证

### 问题**:

### 在本地 Docker 环境中快速部署 Higress 最小化集群，并配置一个简单的 HTTP 路由规则。要求实现当访问 `http://localhost/test` 时，能够将流量转发到 `httpbin.org` 这个公网测试服务，并返回 200 状态码。

### 提示**:

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 5-7 条针对实际使用场景的实践建议：

### 1. 利用 AI 代理插件实现统一协议转换
**场景：** 将内部基于 OpenAI 协议的大模型服务暴露给外部调用，或者将第三方模型（如 Claude、通义千问）统一转换为 OpenAI 格式以兼容现有客户端。
**建议：** 在 Higress 中配置 `ai-proxy` 插件。
**具体操作：**
*   在路由配置中启用 `ai-proxy`，将后端服务指向实际的 LLM API 地址。
*   设置 `serviceType` 为 `ai`，并配置 `serviceName` 为对应的模型提供商（如 `qwen` 或 `openai`）。
*   利用 `context` 参数在网关层统一注入 API Key，避免将密钥分发给每一个客户端应用，实现集中化的鉴权管理。

### 2. 实施基于 Token 的精细化限流
**场景：** 大模型 API 调用成本高昂，且后端处理能力（TPS/QPS）有限，需要防止恶意刷接口或异常流量导致账单爆炸。
**建议：** 不要仅使用传统的 QPS（每秒请求数）限流，应配置针对 Token 或字符数的限流策略。
**具体操作：**
*   使用 `request-block` 或 `key-rate-limit` 插件时，关注 AI 特有的计费维度。
*   如果后端支持 Token 计数，在网关层配置全局限流，例如：每用户每分钟最大消耗 100,000 Tokens。
*   对于流式输出接口，注意流式连接会长时间占用连接数，需配置合理的并发连接数限制，防止连接池耗尽。

### 3. 配置提示词模板与敏感信息过滤
**场景：** 希望在网关层统一控制 System Prompt，或者拦截包含敏感词的请求，减轻后端模型压力。
**建议：** 使用 `ai-proxy` 插件的高级配置功能，在请求到达后端前进行改写。
**具体操作：**
*   在 `ai-proxy` 配置中利用 `prompt` 模板功能，固定 System Prompt，确保所有请求都携带预设的上下文或安全指令。
*   结合 WAF（Web Application Firewall）插件或自定义脚本，在请求发往 LLM 之前拦截包含 PII（个人敏感信息）或违禁词的 Prompt，实现合规性“防火墙”。

### 4. 优化流式传输的缓存策略
**场景：** 相同的用户问题（如“请总结今天的热点新闻”）会被反复请求，直接转发给 LLM 会造成不必要的 Token 消耗和延迟。
**建议：** 谨慎开启缓存，针对非实时性对话场景配置语义缓存或精确匹配缓存。
**具体操作：**
*   对于非流式请求，开启标准的 HTTP 缓存以减少后端压力。
*   **注意：** 对于流式请求，标准的 HTTP 缓存通常不适用。建议通过业务层设计，对高频的通用 Prompt 进行预计算和存储，或者在网关层针对特定的 `prompt_text` 进行哈希匹配缓存，直接返回网关存储的历史完整回复，而非建立新的 LLM 连接。

### 5. 观测与可观测性：提取模型响应头
**场景：** 需要统计不同模型的实际 Token 消耗量以进行成本分析，或者监控模型的响应时间。
**建议：** 确保网关正确透传并记录 LLM 返回的 HTTP Headers。
**具体操作：**
*   Higress 默认会记录请求延迟。在日志采集配置中，确保开启对上游响应头的日志收集。
*   重点记录 `X-LLM-Usage-Token-Input`、`X-LLM-Usage-Token-Output` 等类似字段（具体字段名取决于后端 LLM 返回的头信息）。
*   将这些指标接入 Prometheus/Grafana，建立基于 Token 消耗的监控看板，而非仅仅关注 HTTP 状态码。

###

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*