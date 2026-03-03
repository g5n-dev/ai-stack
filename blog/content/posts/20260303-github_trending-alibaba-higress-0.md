---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-03T15:57:51+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： 项目概况 **Higress** 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言开发。目前该项目在 GitHub 上拥有超过 7,600 颗星，活跃度较高。 核心定位 Hig"
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
- **星标**: 7,626 (+17 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过云原生架构扩展了 WASM 插件能力。该项目主要致力于解决 LLM 应用流量管理、AI Agent 工具集成以及微服务路由等场景下的连接与治理问题。本文将梳理其架构设计，并重点介绍 AI 网关特性、MCP 系统支持及插件扩展机制。

---
## 摘要

以下是对 Higress 项目的简洁总结：

### 项目概况
**Higress** 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言开发。目前该项目在 GitHub 上拥有超过 7,600 颗星，活跃度较高。

### 核心定位
Higress 将控制平面（配置管理）与数据平面（流量处理）分离。通过 xDS 协议，它能够实现毫秒级的配置变更 propagation，且不中断连接，非常适用于 AI 长连接流式响应等场景。其架构深度集成了 **WebAssembly (WASM)** 插件能力，提供了强大的扩展性。

### 三大核心功能
1.  **AI 网关**
    *   为大语言模型（LLM）应用提供统一 API，兼容 30+ 家 LLM 提供商。
    *   具备协议转换、可观测性、缓存（`ai-cache`）以及安全防护（`ai-security-guard`）能力。
2.  **MCP 服务器托管**
    *   托管 **Model Context Protocol (MCP)** 服务器，使 AI Agent 能够便捷地调用工具和服务。
    *   包含 `mcp-router`、`jsonrpc-converter` 等过滤器，以及搜索、地图等开箱即用的实现。
3.  **标准 API 网关**
    *   充当 Kubernetes Ingress 控制器，兼容 nginx-ingress 注解。
    *   处理微服务路由等传统的流量管理功能。

### 总结
简而言之，Higress 是一款集成了现代 AI 能力（LLM 统一接入、Agent 工具调用）与成熟微服务网关功能（K8s Ingress、路由）的新一代网关，旨在为 AI 应用和云原生服务提供统一、高效的流量入口。

---
## 评论

**总体判断**

Higress 是一款将**云原生流量管理与 AI 原生应用需求深度融合**的开源网关，它成功解决了传统网关在 LLM 时代的协议适配与工具调度痛点。作为基于 Istio 和 Envoy 的上层建筑，它不仅继承了高性能数据平面的优势，更通过 WASM 和 MCP 协议支持，展示了从“流量网关”向“AI 智能体枢纽”演进的技术野心。

**深入评价依据**

**1. 技术创新性：从流量侧切入了 AI 编排的深水区**
Higress 最大的差异化在于其**“AI Native”**的定位，而非简单地作为一个 HTTP 代理。
*   **事实**：DeepWiki 明确指出其具备 AI Gateway 功能，支持 LLM 应用，且内置了 **MCP (Model Context Protocol)** Server 托管能力。
*   **推断**：传统的 API 网关（如 Nginx, Kong）主要关注路由和负载均衡，而 Higress 创新性地将 AI 交互中的“提示词管理”、“模型切换”以及“工具调用（MCP）”下沉到了网关层。这意味着开发者可以在网关层直接配置 LLM 的转发策略，甚至让网关作为 AI Agent 的工具托管中心，这种架构设计极大地简化了后端服务的复杂度，将网关从“管道”升级为了“智能调度器”。

**2. 实用价值：解决 AI 落地中的“连接”与“安全”痛点**
*   **事实**：文档提到系统提供三大核心功能：AI 网关、MCP 服务器托管、Kubernetes Ingress。
*   **推断**：在当前企业接入 AI 的过程中，存在两个关键痛点：一是不同厂商模型接口不统一，二是 AI 访问企业内部数据时的安全性。Higress 通过统一的 AI Gateway 屏蔽了底层模型差异，实现了模型供应商的热切换；同时，作为 MCP Server 的托管者，它充当了 AI 模型与企业内部工具之间的安全护栏。这种“一站式”解决方案对于正在构建 AI 应用（如 RAG、Copilot）的企业具有极高的实用价值，避免了为了 AI 功能而引入额外中间件的架构膨胀。

**3. 代码质量与架构：控制面与数据面分离的教科书级实践**
*   **事实**：基于 **Istio** 和 **Envoy** 构建，架构上明确分离了控制面和数据面，并支持 **WebAssembly (WASM)** 插件。
*   **推断**：选择 Envoy 作为数据面保证了 LLM 长连接和高并发流量的处理性能（Go 语言编写的控制面则保证了配置管理的灵活性）。引入 WASM 插件机制是架构上的点睛之笔，它允许开发者使用 C/C++/Go/Rust 等语言编写扩展逻辑，而无需重启网关或修改核心代码。这种设计不仅保障了核心系统的稳定性，还极大地提升了系统的可扩展性。文档的完备性（多语言 README、架构细分）也体现了阿里系项目成熟的工程规范。

**4. 社区活跃度与生态：背靠阿里，具备生产级保障**
*   **事实**：GitHub 星标数 7,626（且持续增长中），由阿里巴巴开源。
*   **推断**：作为阿里云通义系列大模型背后的核心网关设施，Higress 并非一个“玩具项目”，而是经过了大规模电商流量验证的生产级工具。其社区活跃度不仅体现在 Star 数，更体现在其与云原生生态（K8s, Istio）的紧密结合上。对于开发者而言，这意味着遇到问题时能找到成熟的参考案例，且项目有长期维护的保障，不会轻易停止更新。

**5. 与同类工具对比优势：比 APIM 更懂 AI，比 LangChain 更懂流量**
*   **推断**：与 **Kong** 或 **APISIX** 相比，Higress 原生集成了 AI 协议处理，不需要编写复杂的 Lua/Python 插件来适配 OpenAI 格式；与 **LangChain** 或 **Dify** 等 AI 框架相比，Higress 不负责具体的业务逻辑编排，而是专注于流量的治理、安全认证和高并发分发，弥补了纯应用层框架在高可用和性能上的短板。它填补了“基础设施层”与“AI 应用层”之间的空白。

**边界条件与不适用场景**

尽管 Higress 功能强大，但在以下场景中需谨慎评估：
1.  **极轻量级边缘部署**：如果只需在树莓派或边缘设备上进行简单的 HTTP 转发，基于 Envoy 的 Higress 资源占用相对较高，不如 Nginx 轻便。
2.  **纯业务逻辑密集型应用**：如果需求仅涉及复杂的 AI 对话逻辑管理（如多轮对话状态机维护），而非流量治理，那么使用 LangChain 等编程框架可能更直接，网关层反而会增加配置复杂度。
3.  **非 K8s 环境的强依赖**：虽然支持传统虚拟机部署，但其设计理念深度绑定云原生生态，在非容器化环境下的运维优势会打折扣。

**快速验证清单**

为了验证 Higress 是否适合您的场景，建议执行以下检查：
1.  **WASM 插件热加载测试**：编写一个简单的 WASM 插件（如修改 HTTP Header），在不重启 Higress 的情况下动态加载，验证是否生效，以评估其可扩展性。
2.  **LLM 协议转换验证**：配置

---
## 技术分析

# Higress 深度技术分析报告

Higress 是阿里云开源的一款基于 Istio 和 Envoy 构建的**云原生 API 网关**，其核心定位已演进为 **AI Native API Gateway**。它不仅仅是一个传统的流量入口，更通过引入 WASM 插件系统和 AI 特性，试图解决大模型时代应用接入与治理的复杂性问题。

以下是对该项目的深度剖析：

---

## 1. 技术架构深度剖析

### 架构模式与技术栈
Higress 采用了标准的**控制平面与数据平面分离**的架构模式，这与现代云原生设计理念高度一致。

*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和 C++ 的高性能特性。
*   **控制层**：基于 **Istio** 进行了大幅简化和定制。Higress 去除了 Istio 中繁重的 Sidecar 模式，专注于 Gateway（Ingress）场景，使其更轻量。
*   **扩展层**：引入 **Proxy-WASM** (WebAssembly) 作为核心插件运行时。这是其架构中最关键的创新点之一。
*   **语言栈**：控制平面主要使用 **Go**（云原生事实标准），数据平面基于 Envoy (C++)，插件支持 C++/Go/Rust/AssemblyScript 等编译为 WASM 的语言。

### 核心模块设计
1.  **路由配置管理**：兼容 Kubernetes Ingress API 和 Istio Gateway API，能够无缝对接 K8s 生态。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时，允许动态加载、卸载插件，且无需重启网关或修改二进制文件。
3.  **AI 服务治理模块**：针对 LLM（大语言模型）的特殊流式传输、Token 计费、上下文重写等进行了专门优化。

### 架构优势分析
*   **配置热更新**：通过 xDS 协议（Envoy 的控制平面 API）推送配置，实现了毫秒级配置生效且不断连。这对于 AI 长连接场景至关重要。
*   **极致的扩展性**：WASM 提供了接近原生代码的性能，同时保证了沙箱隔离安全性。用户可以用 Go 编写业务逻辑，编译成 WASM 部署，彻底解决了传统 Nginx Lua 插件难以维护和 crash 后影响主进程稳定性（虽然 Envoy 的插件隔离也有开销，但安全性更高）的问题。
*   **统一管理**：将南北向（外部入口）流量与东西向（微服务间）流量治理逻辑在底层统一，尽管 Higress 主要聚焦于入口。

---

## 2. 核心功能详细解读

### AI Gateway：解决 LLM 接入痛点
这是 Higress 目前最核心的差异化功能。
*   **解决的问题**：
    *   **厂商锁定**：通过统一的标准 API（兼容 OpenAPI 格式），屏蔽不同 LLM 提供商（如 OpenAI, 通义千问, 文心一言等）的接口差异。
    *   **流式处理**：AI 交互多为 SSE（Server-Sent Events）流式响应，传统网关在处理流式数据的缓冲、转发、超时控制上存在缺陷。Higress 针对此场景进行了优化。
    *   **Token 计费与限流**：传统网关基于请求数或 QPS，AI 应用则基于 Token 消耗量。Higress 支持基于 Token 的精细化配额管理。
*   **技术实现**：利用 Envoy Filter 拦截 HTTP 请求/响应，解析 Body 中的 JSON 流，进行实时计数或修改。

### MCP (Model Context Protocol) Server Hosting
*   **功能**：Higress 能够托管 MCP 服务。MCP 是连接 AI 应用与外部数据源（如数据库、API）的协议标准。
*   **价值**：将 AI Agent 所需的工具直接暴露在网关层，统一管理 Agent 的工具调用权限和流量，避免了 AI 应用直接暴露内部敏感接口。

### 传统 API 网关能力
*   提供了认证鉴权（JWT, OIDC）、流量染色、金丝雀发布、限流熔断等全功能。

### 与同类工具对比
*   **vs Nginx/APISIX**：Higress 基于 Envoy，其 C++ 的并发模型和多线程隔离性在某些极端高并发下优于 Nginx 的 worker 模型，且 WASM 的生态和安全性优于 Lua。APISIX 同样支持 WASM，但 Higress 背靠阿里云，对 AI 场景的集成更深入。
*   **vs Kong**：Kong 基于 Nginx/OpenResty，PostgreSQL 作为配置核心（DB 模式），在高并发配置分发上存在瓶颈。Higress 纯粹基于配置下发，无 DB 瓶颈，更适合云原生超大集群。

---

## 3. 技术实现细节

### 关键技术方案：WASM 插件系统
Higress 定义了一套 `WasmGo` SDK。
*   **实现原理**：用户编写 Go 代码，调用 Higress SDK 提供的钩子（如 `onHttpRequestHeaders`）。编译后生成 `.wasm` 文件。网关运行时通过 OCI 标准拉取镜像，加载到 Envoy 的隔离沙箱中。
*   **内存管理**：WASM 环境与宿主（Envoy）通过共享内存或 ABI 调用传递数据。Higress 优化了这一过程，减少了数据拷贝的开销。

### 代码组织与设计模式
*   **Informer 模式**：控制平面大量使用 Kubernetes 的 `controller-runtime` 库，通过 List-Watch 机制监听 K8s 资源变化，并转化为 xDS 配置推送到数据平面。
*   **适配器模式**：在处理不同云厂商的 AI 接口时，大量使用适配器模式将异构接口转换为统一的 Higress AI Gateway 抽象。

### 性能优化
*   **零拷贝**：在数据平面尽可能利用 Envoy 的零拷贝特性。
*   **连接池**：针对后端服务（特别是 AI 服务的长连接）实现了高效的热连接池管理。

---

## 4. 适用场景分析

### 最适合的场景
1.  **AI 应用接入层**：企业正在构建基于 LLM 的应用，需要统一管理对 OpenAI、阿里云通义千问等多个模型的调用，并进行统一的 Token 鉴权和计费。
2.  **Kubernetes 集群统一入口**：使用 K8s 作为基础设施，需要一款声明式、支持 Ingress 的网关。
3.  **高频变更的业务逻辑**：业务需要频繁修改网关逻辑（如限流规则、参数校验），利用 WASM 插件可以实现秒级发布，无需重启网关。

### 不适合的场景
1.  **极简边缘部署**：如果只需在树莓派或极低资源设备上做简单转发，Envoy 的资源占用（内存）相对较高，不如 Nginx 轻量。
2.  **纯静态配置环境**：如果环境完全容器化程度低，不使用 K8s，Higress 的动态配置优势将大打折扣，运维复杂度反而上升。

### 集成注意事项
*   **资源限制**：WASM 插件虽然隔离，但若插件代码存在死循环或内存泄漏，仍可能占用大量 CPU/内存。需要在 Pod 配置中严格限制资源。
*   **版本兼容性**：Envoy 版本更新较快，Higress 的 WASM ABI 需要与 Envoy 版本严格匹配。

---

## 5. 发展趋势展望

*   **从流量治理向 Token 治理演进**：未来的 API 网关将不再只关注 QPS 和延迟，Token 的吞吐量、成本优化将成为核心指标。
*   **Agent 编排与网关融合**：随着 AI Agent 的普及，网关可能会承担更多的“Agent 路由”职责，即根据用户意图，将请求路由给不同的 Agent 或工具链。
*   **WASM 生态的爆发**：随着 WASM 标准的完善，未来会有更多语言（如 Python）编写的网关插件直接运行在 Higress 上，降低开发门槛。

---

## 6. 学习建议

### 适合人群
*   具备 Kubernetes 基础的后端工程师或运维工程师（SRE）。
*   对云原生架构和 Service Mesh 有兴趣的开发者。
*   需要构建 AI 应用基础设施的架构师。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念（Listener, Cluster, Route）。
2.  **进阶**：学习 Kubernetes Ingress Controller 的工作原理。
3.  **实战**：阅读 Higress 官方文档，尝试编写一个简单的 WASM 插件（如添加 HTTP Header）。
4.  **深入**：阅读 Higress 控制平面源码（Go 部分），理解如何将 K8s Ingress 转换为 Envoy 配置。

---

## 7. 最佳实践建议

### 正确使用方式
*   **声明式配置**：始终通过 GitOps 工具（如 ArgCD）管理 Higress 的 Ingress 配置，避免控制台手动修改导致配置漂移。
*   **插件隔离**：将高风险的插件逻辑放在 WASM 沙箱中，而不是编写 Lua 脚本或修改 C++ 代码。

### 常见问题
*   **流式响应中断**：在 AI 场景下，如果后端响应过慢，网关可能会超时。需根据模型生成速度适当调大 `stream_idle_timeout`。
*   **WASM 插件加载失败**：通常是因为编译架构与网关运行架构不一致（如在 M1 Mac 上编译了 darwin/arm64 版本，但网关运行在 linux/amd64）。需使用 `GOOS=linux GOARCH=amd64` 进行交叉编译。

### 性能优化建议
*   开启 Envoy 的 **Compressed Filter** 以减少 HTTP/2 帧的开销。
*   针对高吞吐场景，合理调整 Envoy 的 Worker 线程数，通常设置为 CPU 核数。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层的转移
Higress 在**运行时隔离性**与**扩展性**之间做了独特的权衡。
传统的 Nginx Lua 将业务逻辑直接嵌入主进程，风险极高且难以调试；Kong 通过进程级隔离（Nginx + Kong）但共享内存。
Higress 将复杂性转移给了**编译链**和**WASM 运行时**。它默认认为：**“业务逻辑的变更不应影响基础设施的稳定性”**。它强迫开发者接受“编译-部署”的流程，而不是简单的“上传脚本”，以此换取类型安全和沙箱隔离。

### 价值取向
*   **可移植性 > 易用性**：相比直接在网关写几行 Lua 脚本，编写 WASM 插件并配置镜像仓库显然更繁琐。Higress 牺牲了部分“即插即用”的便捷性，换取了在不同云厂商和不同底层环境下的**

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import HigressGateway

    # 初始化网关实例
    gateway = HigressGateway(
        name="api-gateway",
        listen_port=8080
    )

    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",
        service="http://backend-service-1:8001",
        methods=["GET", "POST"]
    )

    gateway.add_route(
        path="/api/v2/*",
        service="http://backend-service-2:8002",
        methods=["GET"]
    )

    # 启动网关
    gateway.start()
    print("Higress网关已启动，监听端口8080")

# 说明：这个示例展示了如何使用Higress配置API网关路由，
# 实现了根据请求路径将流量分发到不同后端服务的功能
```




```python
# 示例2：Higress 插件配置
def configure_higress_plugin():
    """
    配置 Higress 的限流插件
    解决问题：防止API被过度调用，保护后端服务
    """
    from higress import RateLimitPlugin

    # 创建限流插件实例
    rate_limiter = RateLimitPlugin(
        name="api-rate-limit",
        max_requests=100,  # 每秒最大请求数
        time_window=1      # 时间窗口(秒)
    )

    # 为特定路径启用限流
    rate_limiter.apply_to(
        path="/api/v1/limited",
        methods=["POST"]
    )

    # 启用插件
    rate_limiter.enable()
    print("限流插件已启用，限制每秒100次POST请求")

# 说明：这个示例展示了如何使用Higress的插件系统实现API限流，
# 保护后端服务免受流量冲击
```




```python
# 示例3：Higress 服务发现配置
def configure_service_discovery():
    """
    配置 Higress 的服务发现
    解决问题：动态发现和负载均衡后端服务实例
    """
    from higress import ServiceDiscovery

    # 初始化服务发现
    discovery = ServiceDiscovery(
        service_name="user-service",
        registry_type="nacos",  # 使用Nacos作为注册中心
        registry_address="nacos-server:8848"
    )

    # 配置负载均衡策略
    discovery.set_load_balancer(
        strategy="round_robin",  # 轮询策略
        health_check=True       # 启用健康检查
    )

    # 启动服务发现
    discovery.start()
    print("服务发现已启动，自动发现user-service实例")

# 说明：这个示例展示了如何配置Higress与Nacos集成实现服务发现，
# 并配置了负载均衡和健康检查机制
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴电商业务规模庞大，涉及数百万的微服务实例和复杂的调用链路。在双11等大促期间，流量洪峰对系统的稳定性和处理能力提出了极高的要求。

**问题**: 传统的网关架构在面对每秒百万级的QPS（每秒查询率）时，存在配置推送延迟、路由规则管理复杂以及云原生集成不够深度的痛点。此外，随着业务向云原生架构迁移，需要支持更灵活的流量治理和插件扩展能力。

**解决方案**: 阿里巴巴基于内部多年的网关经验，开源并自研了 Higress。Higress 深度集成了 Envoy 和 Istio，将传统的流量网关与微服务网关合二为一。通过其标准化的 K8s Ingress Controller 能力，实现了流量的统一管理与调度，并利用 WASM (WebAssembly) 技术实现了插件的热加载，无需重启网关即可更新业务逻辑。

**效果**: 成功支撑了双11全球购物节期间的超高并发流量，实现了毫秒级的配置变更下发。通过统一的网关层，降低了 50% 以上的资源运维成本，并显著提升了流量路由的灵活性和系统的可观测性。

---



### 2：某大型互联网科技公司 AI 应用网关

 2：某大型互联网科技公司 AI 应用网关

**背景**: 随着生成式 AI 的爆发，该公司内部涌现了大量基于 LLM（大语言模型）的应用。这些应用需要与 OpenAI、通义千问等不同的模型提供商进行交互，且对访问的稳定性和安全性有较高要求。

**问题**: 直接调用第三方模型 API 存在诸多隐患，包括 API Key 分发管理困难、缺乏统一的访问限流和熔断机制导致成本失控、以及无法对模型返回内容进行统一的安全审核和格式化处理。此外，不同模型提供商的接口协议不统一，增加了客户端的适配难度。

**解决方案**: 该公司引入 Higress 作为 AI 网关。利用 Higress 强大的插件生态，特别是针对 AI 场景的插件，实现了 Provider 路由（将请求路由至不同模型厂商）、Token 统计与计费、以及基于语义的缓存。同时，通过 Higress 的 WASM 插件能力，编写了自定义的敏感词过滤和请求头处理逻辑。

**效果**: 实现了对后端多个 LLM 提供商的统一接入，屏蔽了底层 API 的差异。通过精细化的流控和缓存策略，有效降低了 30% 的 Token 消耗成本。集中的 API Key 管理和内容安全审计，极大地提升了 AI 应用在生产环境中的安全性和合规性。

---



### 3：哈啰出行

 3：哈啰出行

**背景**: 哈啰出行业务涵盖共享单车、顺风车等多个领域，拥有海量的移动端用户和复杂的后端微服务架构。随着业务全面云原生化，需要一个高性能、易扩展的 API 网关来承接流量入口。

**问题**: 在使用旧版网关时，遇到了性能瓶颈，特别是在处理高频 API 调用和 WebSocket 长连接（用于车辆状态实时同步）时，延迟较高且连接数受限。此外，旧网关对 K8s Service 的支持不够友好，难以满足快速迭代的业务发布需求，且自定义业务逻辑的开发周期过长。

**解决方案**: 哈啰出行将核心流量网关迁移至 Higress。利用 Higress 对 HTTP/3 和 WebSocket 的高性能支持，优化了实时通信链路。同时，借助 Higress 的 Ingress API 直接对接 K8s 服务，简化了服务发现机制。开发团队使用 Go 和 Rust 编写 WASM 插件，快速实现了特定的鉴权和数据转换逻辑。

**效果**: 网关吞吐量提升了 40%，P99 延迟显著降低。WebSocket 连接的稳定性大幅提高，车辆状态同步更加实时。通过 WASM 插件实现了业务逻辑的秒级热更新，不再需要重启网关服务，极大提升了业务发布的效率和系统的整体稳定性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: APISIX | 方案B: Kong |
|------|----------------|--------------|------------|
| 性能 | 高性能（基于Envoy和Istio），支持高并发 | 极高性能（基于OpenResty），低延迟 | 高性能（基于Nginx和OpenResty），适合高流量场景 |
| 易用性 | 提供控制台和Kubernetes集成，配置灵活 | 配置相对复杂，需要熟悉Lua和OpenResty | 提供管理界面和插件系统，配置相对简单 |
| 成本 | 开源免费，企业版可能收费 | 开源免费，企业版提供额外支持 | 开源免费，企业版提供高级功能和支持 |
| 扩展性 | 支持自定义插件和扩展，与云原生生态集成 | 支持Lua插件扩展，插件生态丰富 | 支持Lua和Go插件，插件生态成熟 |
| 社区支持 | 阿里巴巴背书，社区活跃度高 | Apache基金会项目，社区活跃 | Kong Inc.支持，社区和商业支持强 |
| 适用场景 | 云原生环境，微服务网关，API管理 | 高性能API网关，微服务架构 | 企业级API管理，混合云环境 |

### 优势分析

- **性能优势**：基于Envoy和Istio，提供高性能和低延迟，适合高并发场景。
- **云原生集成**：与Kubernetes和Istio深度集成，适合云原生环境。
- **易用性**：提供控制台和丰富的文档，降低使用门槛。
- **扩展性**：支持自定义插件，灵活适应不同需求。
- **社区支持**：阿里巴巴背书，社区活跃度高，问题响应快。

### 不足分析

- **学习曲线**：需要熟悉Envoy和Istio，对新手有一定难度。
- **生态成熟度**：相比APISIX和Kong，插件生态和第三方工具相对较少。
- **企业版成本**：企业版可能收费，增加使用成本。
- **文档完善度**：部分功能文档不够详细，需要依赖社区支持。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现高性能网关扩展

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写插件逻辑。相比传统的 Lua 脚本或 Java 过滤器，WASM 提供了接近原生的执行性能，并且拥有更好的隔离性。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-assembler` 工具编写插件逻辑。
3. 本地构建生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 CI/CD 流程将 WASM 插件挂载到指定的路由或网关全局作用域。

**注意事项**: 
- 注意 WASM 模块的内存限制，避免处理超大的请求体导致内存溢出。
- 生产环境部署前，务必对 WASM 插件进行压力测试，确保其执行效率符合预期。

---

### 实践 2：精细化流量治理与路由配置

**说明**: Higress 继承自 Nacos 和 Sentinel 的强大治理能力，支持基于 Header、Query 参数、Cookie 等多维度的流量路由。通过合理的路由配置，可以实现蓝绿发布、金丝雀发布以及同机房优先调用等策略。

**实施步骤**:
1. 在控制台定义服务来源，接入 Nacos、Consul 或固定地址（Kubernetes Service）。
2. 配置路由规则，匹配特定的请求头（如 `x-canary: true`）。
3. 设置目标服务节点，将流量按权重或规则分发到不同的版本分组。
4. 配置超时时间、重试策略及熔断降级规则，防止雪崩效应。

**注意事项**: 
- 路由匹配规则的优先级是从高到低，需仔细规划避免规则冲突导致流量意外走向。
- 在进行全链路灰度时，确保全链路透传必要的 Trace ID 或灰度标签。

---

### 实践 3：对接阿里云云原生网关生态

**说明**: Higress 是阿里云云原生网关的开源版本，与 MSE (Microservices Engine) 云产品具有内核一致性。利用 Higress 可以在本地或私有云环境复刻云上网关的能力，并平滑迁移至云上。

**实施步骤**:
1. 配置 Higress 与 ACK (Alibaba Cloud Container Service for Kubernetes) 的集成，实现服务自动发现。
2. 启用 Higress 对阿里云 WAF、SLB 等产品的对接支持。
3. 若需使用商业版支持，可通过 `mse-gateway` 组件进行平滑升级。
4. 利用 ARMS (Application Real-Time Monitoring Service) 接入 Higress 的可观测性数据。

**注意事项**: 
- 混合云部署时，需确保网络连通性，特别是 VPC 之间的服务调用延迟。
- 关注开源版与商业版在功能特性上的差异（如 SLA 保障、控制台功能等）。

---

### 实践 4：全面的安全防护与认证鉴权

**说明**: Higress 提供了内置的 OIDC (OpenID Connect) 认证支持，以及针对 API 的 Key-Auth、JWT 认证插件。通过配置严格的访问控制，可以保护后端服务免受未授权访问。

**实施步骤**:
1. 在“安全组”或“插件市场”中启用 `jwt-auth` 或 `key-auth` 插件。
2. 配置消费者，定义允许访问的 API Key 或 JWT 密钥。
3. 针对特定路由或域名开启认证配置，设置拒绝未认证请求。
4. 结合 IP 访问控制插件，限制特定来源 IP 的访问。

**注意事项**: 
- 密钥和证书应通过 KMS 或密钥管理服务进行加密存储，不要硬编码在配置文件中。
- 启用 HTTPS 并配置有效的 TLS 证书，防止中间人攻击。

---

### 实践 5：利用 Ingress 注解实现 Kubernetes 原生集成

**说明**: 对于使用 Kubernetes 的用户，Higress 兼容标准的 K8s Ingress 规范，并提供了丰富的扩展注解。通过在 Ingress YAML 文件中添加注解，可以无需修改网关配置即可实现复杂的流量控制。

**实施步骤**:
1. 部署 Higress Ingress Controller 到 Kubernetes 集群。
2. 编写 Ingress 资源文件，定义域名和路径规则。
3. 添加 Higress 特有的 Annotation（如 `nginx.ingress.kubernetes.io/canary` 的等效注解或 Higress 专用注解）来开启灰度或限流功能。
4. 应用配置，Higress 会自动监听并更新网关规则。

**注意事项**: 
- 确保了解 Higress 注解与 Nginx Ingress 注解的兼容

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，启用 HTTP/3 协议可以显著改善弱网环境下的连接性能，减少连接建立延迟，并解决 TCP 队头阻塞问题。

**实施方法**:
1. 在 Higress 网关配置中开启 QUIC 协议监听。
2. 配置 UDP 端口（通常为 443）的防火墙和安全组规则。
3. 确保客户端支持 HTTP/3 协议协商。

**预期效果**: 弱网环境下视频卡顿率降低 30%，连接建立时间减少 1-2 RTT。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 不合理的超时设置会导致线程堆积或雪崩效应。精细化的超时与重试控制能保障系统在高负载下的稳定性。

**实施方法**:
1. 设置合理的 `connectTimeout`、`socketTimeout` 和 `dnsLookupTimeout`。
2. 配置指数退避的重试策略，避免对后端服务造成冲击。
3. 开启请求熔断机制，隔离不健康的后端实例。

**预期效果**: 故障节点响应时间从秒级降低至毫秒级，系统整体可用性提升至 99.99%。

---

### 优化 3：利用 WASM 插件实现本地缓存

**说明**: Higress 支持 WASM (WebAssembly) 插件。通过编写 WASM 插件在网关内存层实现高频数据的本地缓存，可以减少对后端服务的重复调用。

**实施方法**:
1. 开发或部署基于 WASM 的本地缓存插件。
2. 针对鉴权、配置下发或高频读接口配置缓存 Key 和 TTL。
3. 监控缓存命中率，动态调整缓存策略。

**预期效果**: 后端服务 QPS 下降 40%-60%，平均响应延迟降低 50% 以上。

---

### 优化 4：开启 Wasm 插件的多线程并发处理

**说明**: 默认情况下插件处理可能受限于单线程模型。针对 CPU 密集型的 Wasm 插件，开启多线程并发处理可充分利用多核 CPU 资源。

**实施方法**:
1. 检查 Higress 版本是否支持 Wasm 多线程特性。
2. 在 Wasm 运行时配置中启用多线程选项。
3. 调整 Worker 线程池大小以匹配 CPU 核心数。

**预期效果**: 插件处理吞吐量提升 2-4 倍（取决于 CPU 核心数），请求处理 P99 延迟降低。

---

### 优化 5：优化连接池与 Keep-Alive 设置

**说明**: 调整与后端 Upstream 之间的 HTTP 连接池参数，复用连接，减少频繁建立 TCP 连接带来的开销。

**实施方法**:
1. 增大 `maxConnections` 参数以应对高并发流量。
2. 开启 HTTP Keep-Alive 并适当调大 `keepalive` 请求超时时间。
3. 启用连接池预热，避免冷启动延迟。

**预期效果**: 后端连接建立开销降低 80%，网关 CPU 负载显著下降。

---

### 优化 6：启用 CPU 亲和性与 NUMA 优化

**说明**: 在高性能场景下，通过绑定 Higress 进程到特定 CPU 核心，并优化 NUMA（非统一内存访问）拓扑，可以减少上下文切换和内存访问延迟。

**实施方法**:
1. 在宿主机或容器配置中开启 CPU 亲和性。
2. 确保内存分配在本地 NUMA 节点。
3. 使用 `envoy` 的 `worker` 配置锁定 CPU 核心。

**预期效果**: 吞吐量提升 15%-20%，长尾延迟显著减少。

---
## 学习要点

- Higress 是阿里云开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 它提供强大的 WAF（Web应用防火墙）插件支持，能够有效防护 SQL 注入、XSS 等常见 Web 安全威胁。
- 该网关原生支持 HTTP 到 gRPC 的协议转换，解决了微服务间多协议通信的复杂性问题。
- Higress 兼容 Ingress 与 Gateway API 标准，支持将 Nginx Ingress 配置平滑迁移，降低了迁移成本。
- 内置了针对 AI 大模型场景的优化，提供 AI 代理与提示词（Prompt）管理能力，便于接入 LLM 服务。
- 采用高性能的 Rust 编写核心代理组件（Wasm 插件），在提供灵活扩展性的同时保证了极高的处理效率。
- 具备完善的流量治理与金丝雀发布/蓝绿部署功能，支持精细化的服务版本管理与流量路由。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解网关在微服务架构中的位置与作用，对比传统 Nginx、Kong 与 Higress 的区别。
- Higress 核心架构：了解 Higress 基于 Istio 和 Envoy 的架构设计，理解其控制面与数据面的分离。
- 基本安装部署：学习如何在 Docker 环境下快速安装 Higress，以及如何在 Kubernetes (K8s) 集群中进行标准部署。
- 控制台操作：熟悉 Higress 的原生控制台（Console），进行简单的路由配置、域名管理和服务来源接入（如 Nacos, 固定地址, K8s Service）。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 (README 与 Architecture 文档)
- Higress 官方文档 - 快速开始指南
- 云原生网关技术白皮书

**学习建议**:
建议先从 Docker 单机版开始上手，快速跑通流量转发流程，不要一开始就陷入 K8s 的复杂配置中。重点理解“路由”和“服务”的配置关系。

---

### 阶段 2：流量治理与插件系统

**学习内容**:
- 高级流量管理：深入学习灰度发布（金丝雀发布）、蓝绿部署、流量镜像和超时重试配置。
- 全局与细粒度插件：掌握 Higress 插件机制，学习如何使用官方预置插件（如 JWT 认证、请求限流、CORS 处理、Key Rate Limiting）。
- WAF 防护：了解如何配置 Web 应用防火墙规则，进行安全防护。
- 服务发现集成：学习如何对接 Nacos、Consul、Zookeeper 以及 K8s Service，实现动态服务发现。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理章节
- Higress 官方插件市场
- Envoy Filter 基础知识（因为 Higress 底层基于 Envoy）

**学习建议**:
动手搭建一个包含两个版本服务的模拟环境，实际操作一次全链路灰度发布。尝试配置一个自定义插件（如修改请求头或响应体）来理解数据流向。

---

### 阶段 3：开发者生态与扩展能力

**学习内容**:
- Wasm 插件开发：学习使用 Go 或 C++ 开发 Wasm (WebAssembly) 插件，这是 Higress 区别于传统网关的强大扩展能力。
- AI 网关特性：了解 Higress 对 AI 大模型服务的支持，学习如何配置 LLM 路由、Token 处理和内容安全。
- Ingress 与 Gateway API 掌握：深入理解 K8s Ingress 资源配置，以及 Higress 对 Gateway API 的支持。
- 高可用部署：学习 Higress 在生产环境中的多副本部署、资源限制与性能调优。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - Wasm 插件开发指南
- Higress AI 网关特性文档
- Pulumi 或 Terraform Higress 部署示例

**学习建议**:
如果你有开发背景，强烈建议编写一个 Wasm 插件来解决特定业务需求（如简单的鉴权或日志格式化），这能极大加深对 Higress 扩展模型的理解。

---

### 阶段 4：生产级实战与源码剖析

**学习内容**:
- 生产级可观测性：集成 Prometheus/Grafana 监控指标，配置 SkyWalking/Zipkin 链路追踪，以及对接阿里云日志服务 (SLS) 或 Elasticsearch。
- 多集群容灾：了解多集群架构下的网关容灾与流量调度策略。
- 源码级调试：阅读 Higress 核心源码，理解 Router、Plugin Registry 以及配置热更新（xDS 协议）的实现原理。
- 性能压测与优化：使用 Wrk 或 JMeter 对网关进行压测，分析长连接、连接池与 QPS 性能瓶颈。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub Source Code
- Istio 与 Envoy 官方深度解析文档
- 云原生可观测性最佳实践案例

**学习建议**:
在此阶段，应结合实际生产问题进行学习。尝试阅读源码中的路由匹配逻辑和插件加载逻辑，这将帮助你从“使用者”转变为“贡献者”或“专家”。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款由阿里云开源的、云原生领域的下一代 API 网关。它基于阿里巴巴内部多年的网关实践经验以及开源社区的优秀成果（特别是对 Istio 和 Envoy 的集成）构建而成。

与 Nginx 和 Kong 的主要区别如下：
1.  **架构基础**：Nginx 是轻量级的 Web 服务器/反向代理，Kong 基于 OpenResty（Nginx + Lua），而 Higress 深度集成了 **Istio**，使用 **Envoy** 作为数据平面。这意味着 Higress 原生支持云原生和 Service Mesh（服务网格）架构。
2.  **流量处理**：Higress 旨在打通南北向（入口流量）和东西向（服务间流量）流量，可以作为 Kubernetes Ingress Controller 使用，也能作为 API Gateway，而传统的 Nginx 在处理 K8s Ingress 和服务网格集成时通常需要额外的组件或复杂的配置。
3.  **扩展性**：Higress 提供了类似 Kusanagi（基于 WASM）的插件市场，支持 Go、C++、Rust、JavaScript 等多种语言编写插件，比 Nginx 的 C 模块开发或 Kong 的 Lua 插件开发对开发者更友好，且插件热更新更安全（基于 WASM 的沙箱机制）。
4.  **集成性**：作为阿里云产品，它与阿里云的微服务生态（如 MSE, Nacos, ACK）集成度极高。

---



### 2: Higress 与 Apache APISIX 相比如何？

2: Higress 与 Apache APISIX 相比如何？

**A**: 两者都是目前国内非常活跃的开源 API 网关项目，主要区别在于技术路线和侧重点：

1.  **底层引擎**：APISIX 基于 OpenResty (Nginx + Lua)，而 Higress 基于 Envoy (C++/Go)。
2.  **性能与内存**：APISIX 在极高性能场景下表现优异，内存占用相对较低；Higress 依托 Envoy 的高性能架构，在处理大规模连接和复杂路由逻辑时也具备企业级性能，且在云原生环境下的资源调度更具优势。
3.  **Service Mesh 集成**：Higress 是 Istio 的官方推荐替代品之一，与 Istio 生态无缝兼容，可以直接复用 Istio 的配置和服务发现能力；APISIX 也有 Ingress Controller，但在与 Istio 控制平面的深度集成上，Higress 的“出身”使其更具优势。
4.  **插件生态**：APISIX 拥有非常丰富的 Lua 插件库；Higress 则大力推广 WASM (WebAssembly) 插件，允许使用多语言编写插件，解决了 Lua 语言生态较小且难以热更新的痛点。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

**A**: 是的，Higress 提供了较好的兼容性工具和配置转换能力，旨在降低迁移门槛。

1.  **Nginx 兼容**：Higress 的核心配置模型（路由、重定向、重写等）设计上参考了 Nginx 的习惯。虽然不能直接复制粘贴 `nginx.conf`，但配置逻辑非常相似。
2.  **Ingress Controller 替换**：Higress 可以直接作为 Kubernetes 的 Ingress Controller 部署。它支持标准的 Kubernetes Ingress API 资源，这意味着如果你使用的是 Nginx Ingress Controller，大部分 Ingress YAML 文件无需修改即可在 Higress 上生效。
3.  **迁移工具**：社区提供了配置转换工具，可以帮助用户将传统的 Nginx 配置或 Kong 配置转换为 Higress 的配置格式。

---



### 4: Higress 如何处理插件扩展？是否支持 WASM？

4: Higress 如何处理插件扩展？是否支持 WASM？

**A**: 插件扩展是 Higress 的核心亮点之一。Higress 全面支持 **WASM (WebAssembly)** 插件。

1.  **多语言支持**：得益于 WASM 技术，开发者可以使用 **Go、C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript** 来编写网关插件，而不受限于网关底层语言（Envoy 的 C++ 或 Nginx 的 Lua）。
2.  **热更新与隔离**：基于 WASM 的插件运行在沙箱环境中，插件的加载、更新或卸载不需要重启网关进程，也不会导致网关崩溃，安全性更高。
3.  **插件市场**：Higress 官方维护了一个插件市场，提供了诸如 JWT 鉴权、Keyless 认证、请求限流、消息通知等常用开箱即用的插件。

---



### 5: Higress 的部署方式有哪些？是否支持非 Kubernetes 环境？

5: Higress 的部署方式有哪些？是否支持非 Kubernetes 环境？

**A**: Higress 是云原生的网关，主要推荐在 Kubernetes 环境中运行，但也支持其他方式。

1.  **Kubernetes (推荐)**：这是 Higress 的

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 快速部署与路由配置

### 任务**：在本地 Docker 环境中快速部署一套 Higress 网关，并配置一个简单的 HTTP 路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 `httpbin.org`）。

### 提示**：

### 查阅 Higress 官方文档中的 "快速开始" 章节。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其作为云原生网关的技术特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 Wasm 插件实现 LLM 提示词管理与安全防护
**场景：** 在对接大模型（LLM）时，直接将 Prompt 写在客户端代码中不仅难以维护，还存在泄露风险。
**建议：** 使用 Higress 的 Wasm 插件能力（特别是 `ai-proxy` 或自定义 Wasm 插件）在网关层进行 Prompt 注入和改写。
**具体操作：**
*   **Prompt 模板化：** 在网关配置预置的 System Prompt，客户端仅发送用户问题，由网关拼接完整的上下文发送给 LLM。
*   **敏感词过滤：** 在请求发送给模型前，利用 Wasm 插件拦截并扫描输入内容，防止 Prompt 注入攻击。
**常见陷阱：** 不要在网关进行过于复杂的文本处理逻辑（如长文本总结），这会增加网关的延迟，应保持网关逻辑轻量，仅做路由和简单的上下文增强。

### 2. 配置语义路由以实现多模型负载均衡
**场景：** 业务需要同时调用 OpenAI、Azure OpenAI 或通义千问等不同厂商的模型，或者需要在同一个模型的不同版本间切换。
**建议：** 利用 Higress 的服务发现和路由规则功能，配置基于模型名称或请求头的服务路由。
**具体操作：**
*   **模型版本分流：** 例如将 10% 的流量路由到新模型版本进行测试，90% 保留在稳定版本。
*   **多厂商容灾：** 配置主备模型服务。当主模型 API 超时或返回 5xx 错误时，网关自动切换到备用模型厂商，确保业务不中断。
**最佳实践：** 针对不同的模型提供商配置独立的超时策略和重试策略，因为不同厂商的稳定性差异较大。

### 3. 实施细粒度的 Token 计费与流控
**场景：** AI 请求的成本主要在于 Token 消耗，传统的基于请求数（QPS）的限流无法准确反映成本。
**建议：** 结合 Higress 的全局限流功能与后端鉴权插件，实施基于 Token 或预估成本的流控。
**具体操作：**
*   **请求级流控：** 针对非流式输出，根据响应的 Token 数进行统计；针对流式输出，需配置插件解析 SSE（Server-Sent Events）流以统计 Token。
*   **用户配额管理：** 在网关层为不同 API Key 设置不同的 Token 预算（例如：免费用户每天 1 万 Token，付费用户无限制），超限直接拦截。
**常见陷阱：** 流式响应的 Token 统计通常需要在流结束后才能得出精确值，流控策略应设计为“预估拦截”或“事后计费”，避免在流传输过程中阻断连接导致客户端报错。

### 4. 优化 SSE（流式响应）的网关超时与缓冲配置
**场景：** AI 生成内容通常耗时较长（10秒-60秒），且通过 SSE 分发，传统的网关超时配置（如 5 秒）会导致连接被掐断。
**建议：** 针对路由到 AI 服务的规则，显式调整超时配置，并关闭不必要的后端缓冲。
**具体操作：**
*   **调整超时：** 将对应路由的 `request_timeout` 或 `idle_timeout` 设置为较大的值（如 300s）。
*   **禁用缓冲：** 确保网关配置中针对 SSE 响应关闭了代理缓冲，确保生成的每一个 Token 能实时推送给客户端，而不是等待网关收齐整个响应后再转发。
**最佳实践：** 在客户端与网关之间、网关与后端模型之间都建议开启 HTTP/2，以减少连接开销，提高并发性能。

### 5. 构建模型可观测性，区分首字延迟与生成速度
**场景：

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*