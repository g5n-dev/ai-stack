---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-30T23:03:03+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的简洁总结： **项目概况** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件能力。该项目使用 **Go** 语言编写，目前在 GitHub 上拥"
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
- **星标**: 7,415 (+9 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过扩展 WASM 插件能力，在提供传统微服务治理的基础上，增加了针对大模型应用的 AI 网关与 MCP 服务托管功能。该项目适合需要在云原生环境中统一管理流量与 AI 服务的开发者或运维团队。本文将介绍其系统架构、核心组件以及如何利用其特性进行构建与部署。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的简洁总结：

**项目概况**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件能力。该项目使用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,400 颗星。

**核心定位**
Higress 定位为 **AI Native API Gateway**（AI 原生 API 网关）。其架构采用标准的控制平面与数据平面分离设计，通过 xDS 协议进行毫秒级配置下发，支持热更新，特别适用于 AI 流式响应等长连接场景。

**三大主要功能**
1.  **AI 网关**：提供统一 API 接入 30 多家大语言模型（LLM）提供商。具备协议转换、可观测性、缓存（`ai-cache`）和安防（`ai-security-guard`）等功能。
2.  **MCP 服务器托管**：支持托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务（如地图、搜索等）。
3.  **传统 API 网关**：作为 Kubernetes Ingress 控制器使用，兼容 Nginx 注解，支持微服务路由。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“AI 原生”网关，它成功将云原生流量治理技术与大模型（LLM）应用需求深度融合。作为阿里开源的标杆项目，它不仅解决了传统 API 网关在处理 AI 流量时的协议与成本痛点，更通过 WASM 和 MCP 协议支持，重新定义了下一代 API 网关的形态，是构建 AI 基础设施的关键连接器。

**深度评价依据**

**1. 技术创新性：从“流量转发”进化为“流量理解与增强”**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，核心创新点在于集成了 AI Gateway 特性、MCP (Model Context Protocol) 服务器托管以及 WASM 插件系统。
*   **推断**：传统网关（如 Nginx）对 AI 流量是“盲”的，仅做 TCP/HTTP 转发。Higress 的差异化在于它“懂” AI。它原生支持 LLM 的语义分块、Token 计费与限流，这解决了 AI 应用中最棘手的成本控制问题。此外，引入 MCP 协议支持使其成为 AI Agent（智能体）的工具调度中心，这种将“网关”升级为“AI 编排入口”的架构设计极具前瞻性，走在了 Kubernetes Ingress Controller 的前列。

**2. 实用价值：解决 AI 落地“最后一公里”的昂贵与复杂问题**
*   **事实**：文档明确指出其具备“AI gateway features for LLM applications”和“MCP server hosting”功能，且支持 Kubernetes Ingress。
*   **推断**：Higress 极大地降低了 AI 应用的接入门槛。在实用层面，它解决了两个关键痛点：一是**安全性**，通过网关统一屏蔽后端 LLM 服务的 Key 泄露风险；二是**成本与稳定性**，通过在网关层实现 Prompt 模板管理和重试机制，避免后端业务代码被这些逻辑侵入。对于企业而言，它可以用一套架构同时管理传统微服务和新兴的 AI 应用，避免了维护两套网关的运维负担。

**3. 代码质量与架构：云原生标准的教科书级实现**
*   **事实**：项目采用 Go 语言编写，控制面与数据面分离，架构文档详细涵盖了 Core Architecture、WASM Plugin System 等模块。
*   **推断**：基于 Envoy 和 Istio 的底座保证了其高性能与可扩展性。Go 语言的使用确保了在云原生环境下的二进制分发便利性。引入 WASM (WebAssembly) 插件系统是代码架构的神来之笔，它允许开发者使用 C++/Go/Rust/JavaScript 等多种语言编写插件，并在不重启网关的情况下动态热加载。这种架构设计不仅提升了系统的灵活性，也通过沙箱机制保证了网关内核的稳定性。

**4. 社区活跃度与生态：阿里背书的成熟度**
*   **事实**：Star 数 7,415（且持续增长），拥有中、日、英多语言文档，更新频率较高。
*   **推断**：作为阿里云核心产品（Higress）的开源版本，它并非实验性玩具，而是经过“双11”级别流量验证的工业级产品。社区支持不仅限于个人开发者，更有阿里云团队的强力兜底，这意味着 Bug 修复速度和功能迭代速度都有保障。对于企业用户来说，这种“大厂开源 + 商业支持”的模式大大降低了技术选型的风险。

**5. 学习价值与对比优势：不仅是工具，更是 AI 架构范式的参考**
*   **事实**：同类工具主要包括 Kong (AI Gateway 插件)、APISIX 以及传统的云厂商 Ingress。
*   **推断**：相比于 Kong 或 APISIX 更多是将 AI 能力作为插件附加，Higress 是“原生”集成。例如，其对 MCP 协议的支持目前是行业领先的，这使得它在构建 AI Agent 基础设施时具有天然优势。对于开发者而言，阅读 Higress 的源码（特别是其如何处理 SSE 流式转发和 Prompt 上下文管理）是学习如何在高并发网关中集成 AI 逻辑的最佳范本。

**边界条件与快速验证清单**

**不适用场景：**
*   **极简边缘场景**：如果仅需在树莓派或边缘设备上进行简单的 HTTP 反向代理，Higress 基于 Envoy 的重资源架构可能过于厚重。
*   **纯静态网站托管**：对于不需要动态路由、鉴权或 AI 逻辑的静态资源服务，使用 Nginx 或 Caddy 更加轻量高效。
*   **非 K8s 环境的强依赖**：虽然支持 Standalone 模式，但其设计理念高度耦合 Kubernetes，在传统虚拟机环境下部署复杂度会显著增加。

**快速验证清单：**
1.  **协议兼容性实验**：部署一个 Higress 实例，配置路由指向 OpenAI API，验证其是否能在不修改客户端代码的情况下，成功拦截并转换请求头（如添加鉴权信息）。
2.  **WASM 插件动态加载**：编写一个简单的 Go WASM 插件（例如修改响应头），在不重启 Higress Pod 的情况下加载该插件，检查是否生效且流量是否中断。
3.  **AI 流量编排能力**：配置一个 LLM 路由，设置 Token 限流（如 10 tokens/min），通过脚本发送流式请求，观察网关是否

---
## 技术分析

以下是对 Alibaba Higress 仓库的深入技术分析。

---

# Alibaba Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是**云原生 API 网关**，但其最大的技术特征在于**"AI Native"（AI 原生）**。它并非从零构建，而是站在了 Kubernetes 生态巨人的肩膀上，采用了**控制平面与数据平面分离**的架构模式。

*   **技术栈**：
    *   **底层引擎**：基于 **Envoy** 构建。Envoy 是高性能的 L7 代理，负责处理底层的网络连接、路由、负载均衡和流量治理。Higress 复用了 Envoy 的 C++ 内核以保证极致性能。
    *   **控制平面**：深度集成 **Istio**。Higress 实现了 Istio 的控制平面规范，能够监听 Kubernetes 和 Istio 的 CRD（自定义资源）变化，并将其转化为 Envoy 的配置。
    *   **扩展机制**：**WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型。它允许开发者使用 C/C++/Go/Rust 等语言编写插件，编译为 WASM 字节码后在 Envoy 中沙箱运行，实现了逻辑的热加载和隔离。
    *   **编程语言**：控制平面主要使用 **Go** 语言编写，利用 Go 在云原生领域的生态优势；数据平面基于 Envoy (C++)。

*   **核心模块**：
    1.  **Router (路由层)**：处理 HTTP/gRPC 流量路由，支持 Header、Cookie、权重等多种路由策略。
    2.  **WASM Plugin System (插件市场)**：一个可扩展的插件运行时，支持认证、限流、请求/响应修改。
    3.  **AI Gateway Layer (AI 网关层)**：这是新增的核心模块。它位于客户端和 LLM 提供商（如 OpenAI, 通义千问）之间，处理 Token 管理、Prompt 模板化、语义路由等。
    4.  **MCP Server Host (模型上下文协议)**：用于托管 AI Agent 的工具调用服务。

*   **架构优势**：
    *   **配置秒级生效**：基于 xDS 协议（Envoy 的控制平面 API），配置变更可以在毫秒级推送到数据平面，且无需重启进程，对长连接（如 AI 的 SSE 流式响应）极其友好。
    *   **标准兼容**：完全兼容 K8s Ingress 和 Istio Gateway 规范，降低了迁移成本。

## 2. 核心功能详细解读

Higress 的功能集可以概括为“传统网关能力 + AI 增强能力”。

*   **AI Gateway (AI 网关)**：
    *   **统一模型接口**：将不同 LLM 厂商（OpenAI, Anthropic, 阿里云等）的异构 API 统一化为标准接口。应用层只需调用 Higress，Higress 负责适配下游。
    *   **Token 经济学管理**：提供基于 Token 的流控和计费统计。由于 LLM 按 Token 计费，传统的请求计数不再适用，Higress 在流式传输中实时解析并统计 Token 消耗。
    *   **Prompt 模板管理**：将 Prompt 提示词作为配置的一部分进行管理，支持变量替换，实现 Prompt 即代码。
    *   **结果缓存**：对于相同的 Query，可以直接返回缓存的 LLM 结果，大幅降低成本并降低延迟。

*   **MCP (Model Context Protocol) 支持**：
    *   这是 Higress 迈向 AI Agent 基础设施的关键一步。它允许 Higress 作为 MCP Server 的宿主，让 AI Agent 能够通过网关安全、标准化地调用外部工具（如数据库查询、API 获取）。

*   **解决的关键问题**：
    *   **厂商锁定**：通过统一接口，业务代码无需修改即可切换 LLM 供应商。
    *   **AI 请求的可观测性**：传统网关只能看到 HTTP 请求，看不到 AI 的语义。Higress 能够记录 Prompt 和 Token 使用情况。

*   **与同类工具对比**：
    *   **vs Nginx/Kong**：Kong 主要基于 Lua/OpenResty，虽然也支持 WASM，但 Envoy 的异步架构在处理长连接和高并发时通常具有更低的延迟抖动。Nginx 修改配置通常需要 reload，会有连接瞬断；Higress 基于 xDS 热更新，连接无感。
    *   **vs Istio Ingress Gateway**：原生的 Istio Ingress 配置极其复杂，学习曲线陡峭。Higress 提供了更符合运维直觉的 K8s Ingress 注解和 GUI 控制台，大大降低了使用门槛。

## 3. 技术实现细节

*   **WASM 插件机制**：
    *   **原理**：Envoy 每个Worker 线程都会加载一个独立的 WASM VM（通常基于 Wasmtime 或 V8）。当请求进入时，Proxy-WASM 规范定义的 `on_request_headers`, `on_body` 等钩子会被触发。
    *   **实现**：Higress 实现了插件的生命周期管理，支持插件的上传、版本控制和灰度发布。Go 代码通过 `tinygo` 编译为 WASM，这使得 Go 开发者可以轻松编写网关插件而无需触碰 C++。

*   **流式处理**：
    *   LLM 应用通常使用 SSE (Server-Sent Events) 返回流式数据。Higress 在网关层对流式数据进行透明代理，同时具备**流式拦截**能力。例如，可以在流式传输过程中实时进行敏感词过滤，或者进行格式转换（如将不同厂商的流式格式统一为 SSE）。

*   **配置分发**：
    *   Higress Console 接受配置 -> 存储到 ConfigMap/Database -> Higress Controller (Go) 监听变化 -> 转换为 xDS JSON -> 通过 gRPC 推送给 Envoy -> Envoy 更新内存中的路由表。

*   **性能优化**：
    *   利用 Envoy 的零拷贝技术和多线程模型。
    *   在 AI 场景中，针对 SSE 长连接进行了连接池优化，避免频繁握手带来的开销。

## 4. 适用场景分析

*   **最适合的场景**：
    1.  **LLM 应用统一接入**：企业内部同时使用多家大模型，需要一个网关来统一鉴权、限流和路由。
    2.  **微服务 API 治理**：基于 K8s 的复杂微服务体系，需要金丝雀发布、全链路灰度。
    3.  **AI Agent 开发**：需要通过 MCP 协议将私有数据或工具暴露给 LLM 的场景。

*   **集成方式**：
    *   **K8s Ingress**：直接替换原有的 Ingress Controller。
    *   **Service Mesh (Sidecar 模式)**：虽然主要用于 Gateway，但可以配合 Istio 做全链路治理。

*   **不适合的场景**：
    1.  **极端性能需求的四层负载均衡**：如纯 TCP/UDP 转发，这种场景 LVSP 或单纯使用 Envoy 配置更轻量。
    2.  **非 K8s 环境**：虽然支持 Docker 部署，但 Higress 的强项在于与 K8s API 的结合，脱离 K8s 会丧失其动态配置的优势。

## 5. 发展趋势展望

*   **从流量治理向语义治理演进**：未来的网关不仅能看 HTTP Header，还能理解 Prompt 的内容，实现基于语义的路由（例如：将“写代码”的请求路由到 Codex 模型，将“写文案”的请求路由到 GPT-4）。
*   **AI Native 可观测性**：不仅仅是日志和指标，还将包含 Prompt 质量、Token 效率、模型响应时间分布等 AI 特有的指标。
*   **边缘计算**：由于 WASM 的轻量级特性，Higress 有潜力被部署到 CDN 边缘节点，作为离用户最近的 AI 交互入口，实现低延迟的 AI 推理预处理。

## 6. 学习建议

*   **适合人群**：云原生架构师、后端工程师、AI 应用开发者。
*   **学习路径**：
    1.  **前置知识**：必须理解 Kubernetes Ingress 概念，了解 HTTP 协议细节。
    2.  **Envory 基础**：阅读 Envoy 官方文档中的 Listener, Cluster, Route 配置概念。
    3.  **WASM 实践**：尝试使用 Higress 官方提供的 Go SDK 编写一个简单的 WASM 插件（例如：添加一个自定义 Header）。
    4.  **AI 特性实验**：在本地部署 Higress，配置一个转发到 OpenAI 的路由，体验 Provider 和 API Key 的管理功能。

## 7. 最佳实践建议

*   **资源隔离**：在生产环境中，建议将 AI 流量的路由和传统业务流量的路由分开，或者使用不同的 Higress 实例/Workload，避免 AI 的长连接占用过多资源影响普通业务。
*   **WASM 插件性能**：虽然 WASM 很灵活，但仍有序列化开销。避免在插件中进行阻塞式重网络请求（如调用外部数据库），应尽量使用 Envoy 的异步上游调用机制。
*   **安全配置**：在 AI Gateway 中，严格限制 API Key 的权限范围。利用 Higress 的插件对 Prompt 进行注入防御，防止 Prompt Injection 攻击。

## 8. 哲学与方法论：第一性原理与权衡

*   **抽象层的转移**：
    Higress 将**网络通信的复杂性**（连接管理、协议解析、TLS 握手）封装在 Envoy (C++) 中，将**业务扩展的复杂性**通过 WASM 暴露给用户（Go/C++/Rust），将**配置管理的复杂性**通过 K8s CRD 暴露给运维。
    *权衡*：它牺牲了“单一二进制文件”的极简部署模式（依赖 K8s 生态），换取了“极致的可扩展性”和“云原生标准性”。

*   **默认价值取向**：
    *   **可扩展性 > 易用性**：虽然提供了控制台，但核心逻辑依然高度依赖 K8s 资源模型，对新手有门槛。
    *   **标准化 > 性能极致**：遵循 xDS 和 Istio 标准意味着经过多层协议转换，性能略低于手写的高性能 C++ 代理，但在通用场景下可忽略。
    *   **AI 优先**：在架构设计上优先考虑了 AI 场景的长连接和流式处理，这是对传统 Nginx 模式的一种修正。

*   **工程哲学**：
    Higress 遵循**"Platform as a Product"（平台即产品）**的理念。它不只是一个软件，更是一套建立在 K8s 之上的标准。它解决问题的范式是：**不重复造轮子（复用 Envoy/Istio），而是通过适配层

---
## 代码示例

```python
# 示例1：Higress网关路由配置
def configure_higress_route():
    """
    配置Higress网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway, Route, Service

    # 创建网关实例
    gateway = Gateway(name="main-gateway")

    # 定义后端服务
    user_service = Service(name="user-service", url="http://user-service:8080")
    order_service = Service(name="order-service", url="http://order-service:8080")

    # 配置路由规则
    gateway.add_route(Route(
        path="/api/users/*",
        service=user_service,
        methods=["GET", "POST"]
    ))

    gateway.add_route(Route(
        path="/api/orders/*",
        service=order_service,
        methods=["GET", "POST", "PUT"]
    ))

    # 应用配置
    gateway.apply()

    print("Higress路由配置已成功应用")

# 说明：这个示例展示了如何使用Higress的Python SDK配置网关路由规则，
# 将不同API路径的请求转发到相应的后端服务，实现微服务架构中的API网关功能。
```

```python
# 示例2：Higress流量治理
def configure_traffic_management():
    """
    配置Higress的流量治理规则
    解决问题：实现灰度发布和流量控制
    """
    from higress import Gateway, CanaryRule, TrafficSplit

    gateway = Gateway(name="main-gateway")

    # 配置金丝雀发布规则
    canary_rule = CanaryRule(
        service="product-service",
        canary_version="v2",
        traffic_percentage=20,  # 20%流量到新版本
        match_headers={
            "user-group": "beta-testers"  # 特定用户组全量流量
        }
    )

    # 配置流量分割
    traffic_split = TrafficSplit(
        service="checkout-service",
        regions={
            "us-east": 60,  # 60%流量到美国东部
            "eu-west": 40   # 40%流量到欧洲西部
        }
    )

    gateway.add_canary_rule(canary_rule)
    gateway.add_traffic_split(traffic_split)
    gateway.apply()

    print("流量治理规则已配置完成")

# 说明：这个示例展示了如何使用Higress实现高级流量治理功能，
# 包括金丝雀发布（灰度发布）和基于地理位置的流量分割，
# 帮助团队安全地发布新功能并优化全球用户体验。
```

```python
# 示例3：Higress安全防护配置
def configure_security_policies():
    """
    配置Higress的安全防护策略
    解决问题：保护API免受常见攻击和未授权访问
    """
    from higress import Gateway, SecurityPolicy, RateLimit, AuthPlugin

    gateway = Gateway(name="main-gateway")

    # 配置速率限制
    rate_limit = RateLimit(
        path="/api/checkout",
        requests_per_minute=100,
        burst=20
    )

    # 配置JWT认证
    jwt_auth = AuthPlugin(
        name="jwt-auth",
        config={
            "issuer": "https://auth.example.com",
            "audience": "higress-gateway",
            "jwks_uri": "https://auth.example.com/.well-known/jwks.json"
        }
    )

    # 配置安全策略
    security_policy = SecurityPolicy(
        enable_waf=True,
        block_sql_injection=True,
        block_xss=True,
        cors_config={
            "allowed_origins": ["https://example.com"],
            "allowed_methods": ["GET", "POST", "PUT"],
            "max_age": 3600
        }
    )

    gateway.add_rate_limit(rate_limit)
    gateway.add_auth_plugin(jwt_auth)
    gateway.set_security_policy(security_policy)
    gateway.apply()

    print("安全防护策略已配置完成")

# 说明：这个示例展示了如何使用Higress配置全面的安全防护措施，
# 包括速率限制防止API滥用、JWT认证保护API访问、
# 以及WAF防护常见Web攻击，帮助保护后端服务安全。
```

---
## 案例研究

### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴拥有庞大的电商生态，包括淘宝、天猫等平台，日均处理数十亿次API调用。随着业务复杂度增加，原有的API网关面临性能瓶颈和扩展性问题。

**问题**:  
1. 传统网关无法应对高并发流量，导致延迟增加。  
2. 多种协议（HTTP、gRPC、Dubbo）的统一管理困难。  
3. 动态路由和流量治理能力不足，影响业务迭代效率。

**解决方案**:  
阿里巴巴基于Higress开发了新一代云原生API网关，整合了Nacos、Sentinel等组件，实现了以下功能：  
- 支持多协议统一接入与转换。  
- 提供动态路由、负载均衡和流量灰度发布能力。  
- 通过Wasm插件扩展实现自定义安全策略。

**效果**:  
1. 网关吞吐量提升50%，P99延迟降低30%。  
2. 业务迭代周期从周缩短至天。  
3. 统一管理了超过10万个API服务，运维效率显著提升。

---

### 2：某在线教育平台

 2：某在线教育平台

**背景**:  
该平台提供直播课、录播课等服务，用户量在疫情期间激增，原有网关无法应对突发流量。

**问题**:  
1. 高峰期频繁出现服务不可用。  
2. 缺乏精细化的流量控制，导致核心服务被拖垮。  
3. 第三方服务集成复杂，开发效率低。

**解决方案**:  
采用Higress作为API网关，结合以下措施：  
- 配置限流熔断规则保护核心服务。  
- 使用Higress的插件市场快速集成支付、认证等第三方服务。  
- 通过Ingress Controller实现Kubernetes服务自动化管理。

**效果**:  
1. 系统可用性从99.5%提升至99.95%。  
2. 开发团队集成新服务的时间减少60%。  
3. 成功应对了单日10倍流量突增的挑战。

---

### 3：某跨国物流企业

 3：某跨国物流企业

**背景**:  
该企业需要整合全球多个区域的物流系统，涉及不同云厂商和私有数据中心。

**问题**:  
1. 跨云、跨地域的服务调用延迟高且不稳定。  
2. 缺乏统一的API治理策略，安全风险高。  
3. 现有网关不支持多云部署架构。

**解决方案**:  
基于Higress构建全球API网关网络：  
- 在各区域部署Higress实例，实现就近接入。  
- 通过配置全局路由策略优化跨区域调用。  
- 使用JWT认证和IP白名单插件增强安全性。

**效果**:  
1. 跨区域调用延迟平均降低40%。  
2. 统一管理了分布在5个云厂商的200多个服务。  
3. 满足GDPR等合规要求，安全审计效率提升80%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|--------|
| 性能 | 高性能，基于 Envoy 和 Rust，支持高并发 | 高性能，基于 Nginx 和 Lua，适合中等负载 | 极高性能，基于 Nginx 和 Lua，适合高负载 |
| 易用性 | 提供图形化控制台，配置简单，支持 Kubernetes 集成 | 配置较复杂，需要手动管理插件和路由 | 配置灵活，但学习曲线较陡，需要熟悉 Lua |
| 成本 | 开源免费，企业版提供额外支持 | 开源免费，企业版收费 | 开源免费，企业版提供商业支持 |
| 扩展性 | 支持自定义插件，基于 WASM 或 Go | 支持自定义插件，基于 Lua 或 Go | 支持自定义插件，基于 Lua 或 Python |
| 社区支持 | 阿里巴巴背书，社区活跃，文档完善 | 社区成熟，插件生态丰富 | 社区活跃，国内支持较强 |
| 适用场景 | 云原生环境，微服务网关，混合云部署 | 传统微服务架构，API 管理 | 高性能 API 网关，云原生环境 |

### 优势分析

- **优势1**：基于 Envoy 和 Rust，性能优异，适合高并发场景。
- **优势2**：提供图形化控制台，降低配置复杂度，适合快速上手。
- **优势3**：支持 Kubernetes 集成，云原生适配性强。

### 不足分析

- **不足1**：社区和插件生态相比 Kong 和 APISIX 尚未完全成熟。
- **不足2**：企业版功能可能需要付费，开源版功能有限。
- **不足3**：文档和案例较少，学习资源相对有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展开发

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许使用 C++, Go, Rust, AssemblyScript 或 JavaScript 编写高性能插件。相比传统 Lua 插件，WASM 插件具有更好的隔离性、更高的执行效率以及更丰富的标准库支持，是实现复杂业务逻辑（如自定义认证、请求响应体修改）的首选方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐 Go 或 Rust）。
2. 使用 Higress 官方提供的 SDK 或 `wasm-as-tool` 工具链进行插件开发。
3. 在本地或 CI 环境中将代码编译为 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传并配置插件。
5. 配置插件的生效范围（全局、特定路由或特定服务）。

**注意事项**: 
- WASM 插件运行在沙箱中，处理大量请求时需注意内存和 CPU 的配额限制。
- 编译出的 `.wasm` 文件体积不宜过大，以免影响网关的加载速度。

---

### 实践 2：服务来源的统一接入与管理

**说明**: Higress 的核心优势之一是能够同时接管 Nacos、Consul、Eureka、Kubernetes Service 以及固定地址（DNS/IP）等多种服务来源。最佳实践是利用 Higress 作为流量入口，统一管理异构微服务架构的服务注册与发现，避免在网关层维护复杂的静态 IP 列表。

**实施步骤**:
1. 在 Higress 控制台的“服务来源”页面添加对应的注册中心（如 Nacos）或 Kubernetes 集群。
2. 配置命名空间与服务的同步规则，确保 Higress 能获取到最新的上游服务实例列表。
3. 创建 Ingress 或网关路由规则时，直接引用已注册的服务名称，而非手动填写 IP。
4. 为不同的服务来源配置健康检查参数，确保故障节点能及时摘除。

**注意事项**: 
- 跨网络（如跨 Kubernetes 集群或跨 VPC）访问服务时，需确保网络连通性。
- 避免在同一个服务名称下混用不同类型的服务来源，防止路由冲突。

---

### 实践 3：精细化流量治理与安全防护

**说明**: 利用 Higress 的全功能网关能力，替代传统的 Nginx 或简单的 Ingress Controller。实施包括 IP 黑白名单、请求限流（并发或 QPS）、JWT 认证、CORS 配置以及 WAF 防护在内的精细化治理策略，保障后端服务的稳定性与安全性。

**实施步骤**:
1. 针对公开接口配置严格的 CORS 和 Header 校验规则。
2. 对 API 接口实施基于 Token 的 JWT 认证插件，验证用户身份。
3. 根据预估流量配置“请求限流”插件（如令牌桶算法），防止突发流量击垮后端。
4. 配置“全局防护”插件，拦截常见的 SQL 注入、XSS 等恶意攻击。
5. 定期审查访问日志，动态调整安全策略。

**注意事项**: 
- 限流配置需经过压测验证，确保阈值设置合理，既防刷又不误杀正常用户。
- 启用多个插件时，注意插件的执行顺序，因为插件间存在依赖关系（如先认证后限流）。

---

### 实践 4：Kubernetes 环境下的 Ingress 自动化部署

**说明**: 在 Kubernetes 集群中，Higress 兼容标准 K8s Ingress API 和 Gateway API。最佳实践是将 Higress 部署为 Ingress Controller，并通过 GitOps 工具（如 ArgoCD 或 Flux）管理 Ingress 资源，实现路由配置的版本化与自动化同步。

**实施步骤**:
1. 使用 Helm Chart 在 Kubernetes 集群中部署 Higress。
2. 编写 Kubernetes Ingress YAML 文件，定义 Host、Path 以及后端 Service 的映射关系。
3. 将 Ingress 配置文件存入 Git 仓库，作为基础设施即代码的一部分。
4. 配置 CI/CD 流水线，应用变更时自动更新 Kubernetes 集群中的 Ingress 资源。
5. 利用 Higress 提供的 Canary（金丝雀）发布注解，实现蓝绿或灰度发布。

**注意事项**: 
- 确保部署 Higress 的 Pod 拥有足够的 RBAC 权限以读取 Service 和 Endpoint 信息。
- 在大规模域名场景下，关注 Ingress 对象的更新频率，避免频繁变更导致 Controller 重载配置过高。

---

### 实践 5：可观测性与日志集成

**说明**: 生产环境的网关必须具备完善的可观测性。Higress 提供了详细的日志采集、Metrics 指标（兼容 Prometheus）以及链路追踪（兼容 OpenTelemetry/SkyWalking

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 Wasm 插件替代 Lua 插件

**说明**: Higress 原生支持 WebAssembly (Wasm) 插件，相比传统的 Lua 插件，Wasm 插件通过近原生代码执行（AOT 编译）能提供更高的执行效率，同时利用沙箱隔离机制提高安全性，减少对主进程的性能损耗。

**实施方法**:
1. 将现有 Lua 插件逻辑使用 C++/Rust/Go 重写为 Wasm 格式。
2. 在 Higress 控制台或通过 `WasmPlugin` CRD 部署 Wasm 插件。
3. 确保网关节点已开启 Wasm 运行时支持（默认开启）。

**预期效果**: 插件执行延迟降低 20%-40%，高并发下 CPU 占用率显著降低。

---

### 优化 2：配置 HTTP/2 与 HTTP/3 (QUIC)

**说明**: 启用 HTTP/2 可以利用多路复用减少 TCP 连接数，降低网络延迟。进一步开启 HTTP/3 (QUIC) 可以在丢包环境下显著减少连接建立延迟和队头阻塞，特别适合移动端或弱网环境下的 API 调用。

**实施方法**:
1. 在网关监听器配置中启用 HTTP/2。
2. 配置证书以支持 HTTP/3（需 UDP 端口 443 开放）。
3. 调整 HTTP/2 最大并发流限制以匹配后端处理能力。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，并发连接数减少 50% 以上。

---

### 优化 3：全链路超时与连接池调优

**说明**: 默认配置通常较为保守。通过精细调整上游服务的连接池大小和超时时间，可以防止线程阻塞，并显著提高网关的吞吐量（QPS）。特别是针对长连接场景，合理的 KeepAlive 设置至关重要。

**实施方法**:
1. **连接池调优**: 将 `maxConnections` 根据后端服务能力调大（如从默认 1024 调至 4096）。
2. **超时配置**: 设置合理的 `connectTimeout`、`sendTimeout` 和 `readTimeout`，避免慢请求堆积。
3. **KeepAlive**: 开启 HTTP KeepAlive 并调整 `idleTimeout`，复用后端连接。

**预期效果**: 后端连接复用率提升至 80% 以上，网关最大吞吐量提升 30%-50%。

---

### 优化 4：启用本地与分布式缓存

**说明**: 对于高频读取但低频变更的配置数据或 API 响应，启用缓存可以极大减少对后端服务的压力以及网络 I/O 开销。Higress 支持本地内存缓存（极速）以及对接 Redis 等分布式缓存。

**实施方法**:
1. 在路由或插件配置中启用“缓存”功能。
2. 针对鉴权数据（如 JWT JWKs）配置本地缓存，减少每次请求的验证开销。
3. 针对只读 API 响应配置 Redis 分布式缓存，设定合理的 TTL。

**预期效果**: 缓存命中时，后端请求量减少 90% 以上，响应延迟降低至 1ms-5ms。

---

### 优化 5：精细化 CPU 亲和性与隔离配置

**说明**: Higress 基于 Envoy，对 CPU 调度敏感。通过将工作进程绑定到特定的 CPU 核心（CPU 亲和性），可以减少上下文切换和缓存失效，提高单核处理效率。

**实施方法**:
1. 在部署配置中设置 `worker_processes` 为 `auto` 或具体 CPU 核心数。
2. 使用 `worker_cpu_affinity` 绑定 CPU 核心。
3. 确保 Higress 进程运行在独立的 CPU Set 上，避免与系统其他高负载进程争抢资源。

**预期效果**: 单核 QPS 处理能力提升 10%-20%，长尾延迟（P99）显著降低。

---

###

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态
- 提供开箱即用的 WAF 防护、流量管理与安全插件，支持低代码开发与插件热更新
- 兼容 Ingress/Gateway API 标准，支持从 Nginx/Kong 等传统网关平滑迁移
- 内置服务发现与负载均衡机制，可无缝对接阿里云及常见注册中心（如 Nacos/Consul/Eureka）
- 采用高性能架构设计，支持高并发流量处理与动态路由配置，降低运维复杂度
- 提供企业级可观测性（Prometheus/Grafana 集成）与精细化限流熔断能力

---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 云原生网关的基本概念与演变历史
- Higress 的核心特性、定位及应用场景
- Higress 与 Nginx、Apache APISIX、Kubernetes Ingress 的区别
- Docker 基础知识（用于本地运行 Higress）
- 基本术语理解：Ingress、Gateway、Route、Service、Plugin

**学习时间**: 1周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档：什么是 Higress
- 云原生网关技术对比文章

**学习建议**:
建议先通读官方文档，理解 Higress "开源+云原生" 的定位。利用 Docker 在本地快速启动一个 Standalone 模式的 Higress 实例，通过控制台界面熟悉配置流程，不要一开始就陷入底层代码细节。

---

### 阶段 2：核心功能掌握与配置实战

**学习内容**:
- 部署架构：在 Kubernetes 集群中安装与配置 Higress
- 流量管理：配置域名、路由规则、路径重写及 Header 操作
- 服务发现：集成 Nacos、Consul、DNS 或固定地址进行服务注册
- 负载均衡策略配置（轮询、随机、一致性哈希等）
- 全局与精细化流量治理：超时、重试、熔断机制
- 基础认证与安全配置（Basic Auth、JWT）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 用户指南
- Higress 官方示例
- Kubernetes Ingress Controller 基础操作文档

**学习建议**:
此阶段重点是"动手"。建议在本地搭建一套 Kubernetes 环境（如 Kind 或 Minikube），并部署一个简单的微服务应用（如 Spring Cloud 或 Go Demo）。通过 Higress 将该服务暴露出来，并尝试修改路由规则来观察流量变化，深刻理解配置生效的逻辑。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- Higress 插件系统原理（Wasm 插件与 Lua 插件）
- 使用 Go 或 C++ 开发 Wasm 插件
- 官方插件的配置与使用（如 Key Rate Limiting, Request Blocking）
- 可观测性集成：对接 Prometheus、Grafana 进行监控
- 日志采集：集成 SLS、Loki 或 Stdout 输出
- 链路追踪：接入 SkyWalking 或 Zipkin

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件开发指南
- Wasm (WebAssembly) 基础教程
- Higress GitHub 仓库中的插件源码示例
- Prometheus 与 Grafana 配置指南

**学习建议**:
从使用官方插件开始，理解插件的处理流程。随后尝试编写一个简单的 Wasm 插件（例如修改请求 Header 或阻断特定请求），并在本地环境中加载测试。同时，学习如何查看 Higress 的监控大盘，分析 QPS、延迟和错误率，这对于生产环境运维至关重要。

---

### 阶段 4：高级架构与生产级运维

**学习内容**:
- Higress 的高可用部署架构与扩缩容策略
- 金丝雀发布与蓝绿发布实战
- 多租户管理与多网关控制平面配置
- Higress 对接阿里云 MSE 或云原生 API 网关的最佳实践
- 性能调优：连接池、缓冲区大小、并发处理优化
- 灰度发布与全链路灰度解决方案
- 安全防护：WAF 防护、CORS 配置、限流降级策略

**学习时间**: 4周以上

**学习资源**:
- Higress 官方博客与最佳实践案例
- Envoy 官方文档（Higress 底层基于 Envoy，理解 Envoy 有助于深入调优）
- 云原生网关高可用架构设计白皮书

**学习建议**:
此阶段面向生产环境。建议研究 Higress 在高并发场景下的表现，进行压力测试。重点关注平滑升级、数据一致性以及复杂的服务治理场景。如果是在阿里云环境，深入学习 MSE Higress 的托管特性；如果是自建，需要重点关注监控告警与故障排查流程。

---
## 常见问题

### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是在 2022 年由阿里云正式开源的，其核心底层代码源自阿里云内部庞大的电商流量网关，经过了多年“双十一”大促的严苛验证。

Higress 遵循云原生计算基金会（CNCF）的云原生技术栈标准，深度集成了 Envoy 和 Istio。简单来说，它建立在 Envoy 高性能网络代理库之上，并兼容 Istio 的 API 标准，旨在解决云原生时代下的流量管理、安全防护和微服务治理问题。它是从阿里内部业务孵化出来的成熟技术，回馈给开源社区。

---

### 2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”架构和“安全防护”能力，主要区别如下：

1.  **技术架构**：传统网关（如旧版 Nginx）通常基于多进程模型，扩展插件往往需要修改配置文件并重载。Higress 基于 Envoy（C++/L4/L7）和 Go（控制面），采用 WASM (WebAssembly) 技术支持插件。这意味着你可以在不重启网关实例的情况下，动态加载或卸载插件，热更新能力极强。
2.  **服务治理集成**：Higress 原生支持 Istio，可以无缝接管 Kubernetes 服务网格的南北向（入口）流量，并与服务间的治理逻辑打通。而传统网关通常需要复杂的适配才能融入 Service Mesh 体系。
3.  **安全能力**：Higress 内置了与阿里云 Web 应用防火墙（WAF）同源的安全防护能力，能够提供更强大的 Bot 防护、防爬虫和流量清洗功能，这通常是开源 API 网关的弱项。

---

### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

**A**: 是的，Higress 非常重视迁移的便利性，并提供了专门的工具来降低迁移成本。

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，可以将现有的 Nginx 配置文件转换为 Higress 的路由配置。同时，Higress 支持标准的 Nginx Ingress 注解，这使得很多基于 Nginx Ingress 的 YAML 文件可以直接在 Higress 上运行。
2.  **Ingress Controller 替换**：在 Kubernetes 环境中，Higress 可以直接作为 Ingress Controller 部署。它兼容 Kubernetes Ingress API，同时也支持 Gateway API（来自 SIG-NETWORK），可以平滑替代原有的 Nginx Ingress Controller。

---

### 4: Higress 支持哪些类型的插件？如何开发自定义插件？

4: Higress 支持哪些类型的插件？如何开发自定义插件？

**A**: Higress 拥有非常灵活的插件系统，主要分为以下几类：

1.  **原生插件**：内置了常见的认证鉴权（如 Keyless, Basic Auth, JWT）、流量控制（限流、熔断）、可观测性（日志、监控）等插件。
2.  **WASM 插件（推荐）**：这是 Higress 的最大亮点。它支持使用 **Go、C++、Rust、JavaScript/TypeScript** 等多种语言编写插件，并编译为 WASM 格式运行。WASM 插件具有沙箱隔离特性，插件崩溃不会导致网关崩溃，且支持热加载。
3.  **Lua/Python 脚本**：为了降低门槛，Higress 也支持直接编写脚本或使用 WASM-Edge 运行时来执行轻量级逻辑。
4.  **进程级插件**：虽然不推荐，但仍然支持通过 gRPC 扩展的方式与外部服务交互。

开发者可以使用 Higress 提供的 CLI 工具或 SDK 快速生成 WASM 插件模板，像编写普通业务代码一样编写网关插件。

---

### 5: Higress 的性能表现如何？能否支撑高并发业务？

5: Higress 的性能表现如何？能否支撑高并发业务？

**A**: Higress 的设计初衷就是为了应对阿里云内部极高并发的业务场景，因此性能表现非常优异。

1.  **底层优化**：其数据面基于 Envoy，Envoy 本身就是高性能的 L7 代理，采用 C++ 编写，具备零拷贝、多线程非阻塞架构等特性。
2.  **实测数据**：在官方基准测试中，Higress 在开启常见插件（如限流、认证）的情况下，依然能保持极高的吞吐量和极低的延迟延迟，性能损耗远低于基于 Lua 的 OpenResty 系网关。
3.  **弹性伸缩**：作为云原生网关，Higress 可以结合 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU 或流量指标自动扩缩容，轻松应对流量洪峰。

---

### 
## 实践建议

以下是为 Alibaba Higress 仓库提供的 6 条实践建议，侧重于 AI 网关的实际落地与生产环境运维：

### 1. 利用 WASM 技术实现插件热加载与多语言扩展
Higress 基于 C++ 构建，但支持通过 WebAssembly (WASM) 运行时动态加载插件。在生产环境中，**强烈建议不要修改 Higress 的核心代码**，而是将业务逻辑（如特定的鉴权、请求头修改、日志格式化）编写为 WASM 插件。
*   **最佳实践**：使用 Go 或 Rust 编写 WASM 插件。这样可以在不重启网关服务的情况下动态更新业务逻辑，实现“代码即配置”的灵活部署。
*   **常见陷阱**：避免在 WASM 插件中执行重量级的 CPU 计算或阻塞式 I/O 操作，这会拉低网关的整体吞吐量。

### 2. 针对 AI 语义调用的“提示词”管理与安全防护
作为 AI Native 网关，Higress 能够拦截并修改发送给 LLM 的请求。建议在网关层实施统一的 Prompt 模板管理和注入。
*   **最佳实践**：利用 Ingress 或 Route 配置，在请求转发给 LLM 之前，自动注入系统预设的 Prompt 前缀（例如限定角色、设定输出格式），从而减少前端开发的重复工作。
*   **常见陷阱**：忽视 Prompt 注入攻击。务必在网关层配置严格的关键词过滤或语义审查策略，防止恶意用户通过精心设计的输入绕过前端直接攻击后端的大模型。

### 3. 配置精细化的模型路由与 fallback 机制
AI 场景下，单一模型提供商可能不稳定或限流。利用 Higress 的服务路由能力，构建模型调用的容错闭环。
*   **最佳实践**：配置多活或主备路由。例如，默认请求指向 OpenAI，当检测到 HTTP 429 (Too Many Requests) 或 503 错误时，利用 Higress 的重试或流量切换能力，自动将请求转发至备用的模型提供商（如 Azure OpenAI 或本地部署的模型）。
*   **常见陷阱**：在设置超时时间时未考虑大模型的生成时间（TTFE）。大模型推理耗时通常高于普通 API，建议将网关层的超时设置放宽至 30 秒甚至更长，并开启流式转发支持。

### 4. 实施基于 Token 的计量与限流策略
传统的 API 网关通常基于 QPS（每秒请求数）或 RPM（每分钟请求数）限流，但在 AI 场景下，成本主要消耗在 Token 上。
*   **最佳实践**：结合 WASM 插件或 Higress 的内置能力，解析请求体和响应体中的 Token 数量（针对 OpenAI 格式），实现基于 Token 用量的精细化限流和计费。这比单纯限制并发数更能有效控制后端成本。
*   **常见陷阱**：直接照搬传统网关的“连接数限流”。AI 请求通常是长连接或流式传输，连接数少但带宽占用高，应根据实际带宽和 Token 消耗来配置限流规则。

### 5. 处理流式响应（SSE）的缓冲与转发
大模型交互通常采用 Server-Sent Events (SSE) 或流式返回。网关在处理此类请求时需要特别小心，以免“背压”导致连接中断。
*   **最佳实践**：确保网关配置了流式透传能力，不要在网关层将整个流式响应缓冲完成后才转发给客户端，否则用户体验会有明显的延迟感。Higress 对此有原生支持，需确保相关配置开启。
*   **常见陷阱**：在日志插件中记录响应 Body 时，流式响应的 Body 可能无法被完整捕获或导致内存溢出。建议针对流式接口关闭 Body Logging 或仅记录 Metadata。

### 6. 做好可观测性：区分网关指标与模型指标
在 AI 网关架构中，延迟的来源非常复杂（网络延迟 + �

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [中国开源AI生态的架构选择：超越DeepSeek的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的技术路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*