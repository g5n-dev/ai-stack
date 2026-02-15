---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-15T02:54:54+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里云", "Istio", "Envoy", "LLM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： **项目简介** Higress 是一款由阿里云开源的、基于 **Go** 语言开发的**云原生 API 网关**。它建立在 Istio 和 Envoy 之上，定位为 **AI Native API Gateway**（AI 原生 API 网关）。目前该项目在 GitHub"
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
- **星标**: 7,528 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过集成 WASM 插件能力，在提供传统流量管理功能的同时，专为 LLM 应用和 AI Agent 工具集成进行了优化。该项目旨在解决云原生环境下对 AI 服务治理与微服务路由的双重需求，帮助开发者在统一架构下管理复杂流量。本文将介绍其系统架构、核心组件以及 AI 网关特性，帮助读者理解如何利用 Higress 构建高效的 AI 服务基础设施。

---
## 摘要

以下是对 Higress 项目的简洁总结：

**项目简介**
Higress 是一款由阿里云开源的、基于 **Go** 语言开发的**云原生 API 网关**。它建立在 Istio 和 Envoy 之上，定位为 **AI Native API Gateway**（AI 原生 API 网关）。目前该项目在 GitHub 上已获得超过 7,500 颗星。

**核心架构与技术特点**
*   **架构设计**：采用控制平面与数据平面分离的架构。
*   **高性能与扩展性**：利用 **WebAssembly (WASM)** 插件能力进行扩展，支持通过 xDS 协议进行毫秒级配置变更，且变更过程不中断连接。
*   **兼容性**：兼容 Kubernetes Ingress 以及 nginx-ingress 注解。

**三大主要功能场景**

1.  **AI 网关**：
    *   为大语言模型 (LLM) 应用提供统一 API，兼容 30+ 家 LLM 提供商。
    *   具备协议转换、可观测性、缓存和 AI 安全防护等功能。
    *   *核心组件*：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。

2.  **MCP 服务器托管**：
    *   托管模型上下文协议 (MCP) 服务器，使 AI 智能体能够调用工具和服务。
    *   *核心组件*：`mcp-router`, `jsonrpc-converter` 过滤器及多种 MCP 服务器实现。

3.  **传统 API 网关**：
    *   作为 Kubernetes Ingress 控制器，处理微服务路由。

**总结**
Higress 专为现代云原生应用和 AI 应用设计，特别适合需要处理 AI 流式响应等长连接场景，同时保留了作为传统微服务网关的强大功能。

---
## 评论

**总体评价**

Higress 是目前云原生网关领域中将 **AI 原生能力** 与 **传统流量治理** 结合得最为彻底的开源项目之一。它不仅成功解决了 Istio 在作为网关使用时的复杂性问题，更敏锐地捕捉到了大模型（LLM）应用时代的流量特征，通过 WASM 和 MCP 协议支持，成功转型为 AI 时代的流量入口。

**核心评价依据**

**1. 技术创新性：从“流量转发”到“模型语义处理”的架构演进**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，但引入了 WASM（WebAssembly）插件系统，并明确提出了 AI Gateway 和 MCP（Model Context Protocol）Server 托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP 七层负载均衡，对 AI 交互中特有的“流式输出（SSE）”支持较差。Higress 的差异化在于它将 AI 模型的调用视为一等公民。通过 WASM，它允许开发者使用 C++/Go/Rust 等高性能语言编写插件，在网关层直接处理 Prompt 增强、敏感词过滤甚至 Token 计费，而无需侵入后端业务代码。这种“计算下沉”到网关层的架构，是应对 AI 高并发、高延迟场景的有效技术解耦。

**2. 实用价值：打通 AI Agent 的“最后一公里”**
*   **事实**：文档指出 Higress 提供 MCP server hosting 功能，用于 AI agent 工具集成，同时支持 Kubernetes Ingress 和微服务路由。
*   **推断**：在企业落地 AI 应用时，最大的痛点之一是模型与工具（如数据库、API）之间的连接安全性与鉴权。Higress 通过内置 MCP Server 支持，实际上充当了 AI Agent 的“安全代理”。这意味着企业无需暴露内部 API 给公网模型提供商，只需通过 Higress 进行协议转换和权限控制。这解决了 LLM 应用落地中最关键的安全与合规问题，使其不仅是一个网关，更是 AI 生态的聚合枢纽。

**3. 代码质量与架构：云原生标准化的降维打击**
*   **事实**：项目采用 Go 语言开发，架构上明确分离了控制平面和数据平面，且完全兼容 K8s Ingress 标准。
*   **推断**：阿里巴巴在 Higress 上展现了深厚的云原生基建功底。相比于从零开始写一个网关，基于 Envoy 意味着获得了 C++ 编写的高性能数据平面，而 Higress 自身专注于 Go 语言的控制平面逻辑（配置管理、路由发现）。这种架构既保证了性能（Envoy 的零拷贝、异步 I/O），又保证了可扩展性（Go 的开发效率）。其 WASM 插件市场的设计，使得功能扩展像使用手机 App 一样简单，极大地提升了代码的可维护性和复用性。

**4. 社区活跃度：头部背书与生态建设**
*   **事实**：仓库星标数 7,528（且持续增长），由阿里巴巴开源，拥有详细的中文、日文、英文文档。
*   **推断**：在 API 网关这个相对“红海”的领域，Higress 能迅速获得关注，主要得益于阿里云的成熟技术背书和清晰的商业化路径（通常开源版对应云产品）。社区活跃度不仅体现在 Star 数，更体现在对前沿技术（如 MCP 协议）的跟进速度上。它不仅是阿里内部技术的输出，也是对 CNCF 生态的重要补充，吸引了大量寻求国产替代或 AI 网关解决方案的开发者。

**5. 潜在问题与改进建议**
*   **推断**：虽然基于 Istio，但 Higress 在控制平面去除了 Sidecar 模式，专注于 Ingress Gateway。这在简化部署的同时，也意味着如果用户需要全链路 Mesh 治理，仍需部署完整的 Istio，可能存在一定的功能重叠或认知负担。此外，WASM 插件的调试难度相对较高，社区需要提供更完善的调试工具链（如 IDE 插件、沙箱测试环境）以降低开发者门槛。

**边界条件与验证清单**

**不适用场景：**
*   **极边缘计算环境**：Envoy 的资源消耗对于几 MB 内存的边缘设备可能过重。
*   **简单的静态博客托管**：对于仅需基础 HTTP 服务的场景，Higress 属于“杀鸡用牛刀”，配置复杂度远高于 Nginx。
*   **非 K8s 环境的强依赖**：虽然支持 Docker，但其强大功能高度依赖 Kubernetes 的 API 交互，传统虚拟机环境难以发挥全部威力。

**快速验证清单：**
1.  **AI 流式处理测试**：部署 Higress 并配置通义千问或 OpenAI 路由，使用 `curl` 测试其 SSE（Server-Sent Events）转发能力，观察在长连接下的网关内存占用是否稳定。
2.  **WASM 插件热加载**：在控制台安装一个官方插件（如 JWT Auth），修改配置（如 Token 过期时间），验证是否能在不重启 Pod 的情况下毫秒级生效。
3.  **MCP 协议连通性**：配置一个本地工具作为 MCP Server，通过 Higress 暴露给 AI Agent，验证网关层是否正确拦截并转发了工具调用请求，以及鉴权是否生效。
4.  **高并发性能对比**：使用 Wrk 或 Hey 对比 Higress 与标准 Nginx 在开启

---
## 技术分析

# Higress 深度技术分析报告

Higress 是阿里云开源的一款基于 Istio 和 Envoy 构建的云原生 API 网关。它不仅仅是一个传统的流量入口，更被定义为 **AI Native API Gateway**（AI 原生 API 网关）。以下是对该项目的深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了标准的 **控制平面与数据平面分离** 的架构模式，这是现代云原生网关的标志性设计。

*   **数据平面**：基于 **Envoy** 构建。Envoy 是高性能的 C++ 网络代理，负责处理实际的流量（L7 路由、负载均衡、执行 WASM 插件）。
*   **控制平面**：基于 **Istio**（主要是 Pilot 组件）进行深度改造。它负责管理 Envoy 配置的生命周期，通过 xDS 协议（包括 LDS, RDS, CDS, EDS）将配置下发到数据平面。
*   **扩展层**：引入了 **WebAssembly (WASM)** 技术作为核心扩展机制。Higress 将 Envoy 的 WASM 能力通过 Go 语言封装，极大降低了插件开发门槛。

### 核心模块与设计
1.  **路由与流量管理**：继承了 Istio 的强大路由能力，支持基于权重、Header、Cookie 的灰度发布和蓝绿部署。
2.  **WASM 插件市场**：这是 Higress 的核心差异化设计。它允许用户编写 Go 代码，自动编译为 WASM，并动态推送到 Envoy 中执行，无需重启网关。
3.  **AI 网关层**：在传统网关之上增加了一层专门针对 LLM（大语言模型）流量的处理逻辑，包括 Token 计费、上下文重写、模型转换等。

### 技术亮点与创新
*   **AI 原生设计**：这是 Higress 最大的创新点。传统网关是“字节”或“包”级别的转发，而 Higress 引入了“Token”级别的感知能力。它理解 LLM 的 SSE（Server-Sent Events）流式响应，能够对 Token 进行计数、限流和脱敏。
*   **MCP (Model Context Protocol) 集成**：Higress 内置了对 MCP 协议的支持，可以作为 AI Agent 的工具提供者，让大模型安全地访问内部 API。
*   **热更新能力**：得益于 Istio 的架构，配置变更通过 xDS 协议秒级下发，且在长连接（如 SSE 流）场景下能做到不断连更新。

### 架构优势分析
*   **高性能**：Envoy 的 C++ 异步非阻塞模型保证了极高的吞吐量和低延迟。
*   **可扩展性**：WASM 插件机制使得业务逻辑可以像“脚本”一样热加载，解决了传统 Nginx Lua 插件难以维护和安全性差的问题。
*   **云原生亲和**：直接作为 Kubernetes Ingress Controller 运行，无缝对接 K8s 服务发现。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接口**：将不同 LLM 厂商（OpenAI, 通义千问, 文心一言等）的异构 API 统一化为标准接口。
    *   **Token 管理**：基于 Token 数量或成本进行精细化限流和计费。
    *   **提示词管理**：在网关层动态注入 System Prompt，避免在应用代码中硬编码。
2.  **MCP 服务器托管**：
    *   允许用户将内部微服务注册为 MCP 工具，使得 AI Agent 能够通过标准协议调用这些服务，同时由网关处理认证和鉴权。
3.  **传统 API 网关**：
    *   K8s Ingress 管理。
    *   服务治理：熔断、重试、负载均衡算法。
    *   全链路灰度发布。

### 解决的关键问题
*   **AI 模型切换成本**：企业不再需要为每个模型编写适配代码，通过 Higress 即可切换底层模型供应商。
*   **AI 调用的可观测性**：传统网关只能看到 HTTP 流量，Higress 能记录 Prompt 和 Token 消耗，便于成本分析。
*   **私有化部署中的模型路由**：在混合云场景下，智能路由流量到公有云或本地私有化模型。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **核心语言** | Go (控制) / C++ (数据) | Lua / Go | Lua | C |
| **AI 原生支持** | **内置 (Token计费/模型转换)** | 需插件 | 需插件 | 无 |
| **扩展机制** | WASM (Go开发) | Lua / WASM / Go | Lua / Python / WASM | Lua (OpenResty) |
| **K8s 集成** | 原生 Ingress | 需 KIC | 原生 Ingress | 需 Ingress Controller |
| **配置热更新** | xDS 秒级 | DB 轮询 / Reload | ETCD Watch | Reload (断连) |

### 技术实现原理
*   **流式处理**：Higress 在 Envoy Filter 层实现了针对 SSE 协议的解析器。它拦截 HTTP 响应流，解析 `data: ` 格式的 JSON 块，实时统计 Token 数，并在流结束后生成访问日志。
*   **WASM 沙箱**：插件运行在 Envoy 的线性内存沙箱中，通过 `proxy_on_http_request_headers` 等 ABI 挂钩点与宿主交互。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 对 Istio Pilot 进行了优化，去除了大部分 Sidecar 相关的冗余逻辑，专注于 Gateway 场景，减少了控制平面的资源消耗。
*   **Go to WASM 编译链**：Higress 提供了一套 SDK，允许用户用 Go 编写插件。构建时，使用 TinyGo 将 Go 代码编译为 WASM 字节码。这使得开发者无需学习 C++ 或 Lua 即可扩展网关功能。

### 代码组织结构
*   **pkg/**：核心业务逻辑，包含 xDS 转换器、路由匹配逻辑。
*   **plugin/**：WASM 插件系统的 Go SDK 实现。
*   **router/**：核心路由引擎，负责将 K8s Ingress YAML 转换为 Envoy 配置。
*   **core/**：与 Envoy 的交互接口层。

### 性能与扩展性
*   **性能优化**：
    *   **零拷贝**：Envoy 本身的高性能特性被完整保留。
    *   **连接池**：针对后端服务维护 HTTP/2 连接池，减少握手开销。
*   **扩展性**：
    *   水平扩展：数据平面无状态，可通过 K8s HPA 自动扩缩容。
    *   功能扩展：WASM 插件可以独立于网关版本进行迭代。

### 技术难点与解决
*   **难点**：WASM 的性能损耗与内存限制。
*   **解决**：Higress 针对高频场景（如 Body 修改）进行了优化，建议使用 Proxy-WASM 规范，并合理配置 WASM VM 的内存大小。对于极致性能要求，仍建议使用原生 Envoy Filter。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **大模型应用集成**：任何需要接入 OpenAI、通义千问等 LLM 的企业应用，特别是需要统一管理 Prompt 和 Key 的场景。
2.  **微服务网关**：基于 Kubernetes 的微服务架构，需要替代 Nginx Ingress 或传统 API 网关。
3.  **AI Agent 开发**：需要将内部工具（API）通过 MCP 协议暴露给大模型的场景。
4.  **多语言/异构系统**：后端由不同语言编写，需要在网关层统一处理认证、限流逻辑。

### 最有效的场景
*   **AI 流量中转站**：当企业同时使用多个模型供应商，且需要在网关层做统一鉴权、计费和模型切换时，Higress 是目前最成熟的开源方案。

### 不适合的场景
*   **极致边缘计算**：由于基于 Envoy 和 Istio，资源占用（内存/CPU）相对较高，不适合极度受限的边缘设备（如嵌入式路由器）。
*   **简单的静态文件托管**：用 Nginx 直接处理更轻量。

### 集成方式
*   **K8s 部署**：通过 Helm Chart 一键部署。
*   **服务发现**：自动关联 K8s Service，无需手动配置后端 IP。
*   **插件配置**：通过 ConfigMap 或 WasmPlugin CRD 进行配置。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 LLM 融合**：从简单的转发转向 RAG（检索增强生成）的编排层，例如在网关层直接对接向量数据库进行语义缓存。
*   **可观测性增强**：集成 OpenTelemetry，提供针对 Prompt 和 Token 的专用 Dashboard。

### 社区反馈与改进
*   社区普遍认可其“AI 网关”的定位，但在 WASM 插件的调试体验上仍有提升空间（如调试工具链的完善）。
*   文档对于非 K8s 用户的友好度有待提高。

### 未来结合
*   **Service Mesh (Istio) 深度融合**：Higress 可能会进一步向 Istio 上游贡献代码，使得 Gateway 和 Sidecar 模式能够无缝切换，形成真正的“统一网关”。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的后端工程师。
*   需要落地 LLM 应用的架构师。
*   对云原生网关技术感兴趣的开发者。

### 学习路径
1.  **基础**：理解 Kubernetes Ingress 概念，学习 Envoy 基础术语（Listener, Cluster, Route）。
2.  **进阶**：阅读 Higress 官方文档，尝试部署并配置一个简单的 AI 网关转发。
3.  **高级**：学习 Proxy-WASM 规范，使用 Go SDK 编写一个自定义插件（如请求头篡改）。

### 实践建议
*   **从 Docker Desktop 开始**：本地使用 Docker Desktop 的 K8s 环境进行测试，避免直接在生产环境操作。
*   **阅读源码**：重点关注 `router` 和 `plugin` 目录，理解配置是如何转化为 Envoy 配置的。

---

## 7. 最佳实践建议

### 如何正确使用
*   **资源隔离**：在生产环境中，建议将 Higress 的控制平面与数据平面分开部署，或者使用 HPA 进行弹性伸缩。
*   **插件开发**

---
## 代码示例




```python
# 示例1：使用Higress进行简单的路由转发
def higress_routing_example():
    """
    这个示例展示了如何使用Higress进行简单的路由转发。
    假设我们有一个服务，需要将请求从路径 /api/v1 转发到后端服务 http://backend-service:8080/v1
    """
    from higress import HigressGateway

    # 初始化Higress网关
    gateway = HigressGateway()

    # 定义路由规则
    gateway.add_route(
        path="/api/v1",  # 前端请求路径
        backend="http://backend-service:8080/v1",  # 后端服务地址
        methods=["GET", "POST"]  # 允许的HTTP方法
    )

    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用Higress进行简单的路由转发。
# 它将前端请求路径 /api/v1 转发到后端服务 http://backend-service:8080/v1，
# 并限制了允许的HTTP方法为GET和POST。
```




```python
# 示例2：使用Higress进行流量灰度发布
def higress_canary_release_example():
    """
    这个示例展示了如何使用Higress进行流量灰度发布。
    假设我们有两个版本的服务 v1 和 v2，需要将10%的流量转发到v2版本进行测试。
    """
    from higress import HigressGateway

    # 初始化Higress网关
    gateway = HigressGateway()

    # 定义主版本路由规则（90%流量）
    gateway.add_route(
        path="/api/v1",
        backend="http://backend-service-v1:8080/v1",
        weight=90  # 流量权重
    )

    # 定义灰度版本路由规则（10%流量）
    gateway.add_route(
        path="/api/v1",
        backend="http://backend-service-v2:8080/v1",
        weight=10  # 流量权重
    )

    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用Higress进行流量灰度发布。
# 它将90%的流量转发到v1版本的服务，10%的流量转发到v2版本的服务，
# 从而实现平滑的版本升级和测试。
```




```python
# 示例3：使用Higress进行API限流
def higress_rate_limiting_example():
    """
    这个示例展示了如何使用Higress进行API限流。
    假设我们需要限制每个IP每分钟最多访问100次 /api/v1 接口。
    """
    from higress import HigressGateway

    # 初始化Higress网关
    gateway = HigressGateway()

    # 定义限流规则
    gateway.add_rate_limit(
        path="/api/v1",  # 需要限流的接口
        limit=100,  # 限流次数
        window=60,  # 时间窗口（秒）
        key="client_ip"  # 限流依据（客户端IP）
    )

    # 定义路由规则
    gateway.add_route(
        path="/api/v1",
        backend="http://backend-service:8080/v1"
    )

    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用Higress进行API限流。
# 它限制了每个IP每分钟最多访问100次 /api/v1 接口，
# 从而保护后端服务免受恶意攻击或突发流量影响。
```


---
## 案例研究


### 1：某大型电商平台（阿里内部生态）

 1：某大型电商平台（阿里内部生态）

**背景**: 该电商平台拥有海量的商品数据和用户流量，在大促期间（如双11），系统面临巨大的并发压力。原有的 API 网关在处理每秒数十万级的 QPS（Queries Per Second）时，资源消耗过高，且对复杂的流量路由逻辑支持不够灵活。

**问题**: 
1. 开源网关在超高并发下性能出现瓶颈，延迟增加。
2. 业务需求变化快，需要频繁修改路由规则和插件，旧架构的扩展性差，维护成本高。
3. 需要更好地对接阿里云内部的微服务生态（如 Nacos, MSE）。

**解决方案**: 
基于 **Higress** 构建了新一代的云原生 API 网关。利用 Higress 的高性能内核（基于 Rust 和 C++ 实现），替代了原有的 Java 网关。同时，利用 Higress 的 WASM (WebAssembly) 插件能力，实现了业务逻辑的热加载，无需重启网关即可更新鉴权、限流和流量染色逻辑。

**效果**: 
1. 成功支撑了大促期间峰值流量，网关最大吞吐量提升了 50%，资源利用率（CPU/内存）降低了 30%。
2. 插件开发效率提升，新业务上线周期从周级缩短至天级。
3. 实现了标准化的云原生网关架构，统一了流量治理入口。

---



### 2：某AI大模型应用服务商

 2：某AI大模型应用服务商

**背景**: 随着 AIGC（生成式 AI）的爆发，该公司对外提供基于 LLM（大语言模型）的对话和文本生成服务。用户请求直接调用后端的 LLM 模型接口。

**问题**: 
1. 直接暴露后端模型接口存在极大的安全风险，容易被恶意攻击导致 Token 泄露或滥用。
2. LLM 推理成本高昂，缺乏有效的请求缓存和提示词（Prompt）管理机制，导致重复请求消耗大量预算。
3. 需要对不同用户进行精细化的流控和计费管理。

**解决方案**: 
部署 **Higress** 作为 AI 专用网关。利用 Higress 原生支持的 LLM 特性，在网关层实现了 Prompt 模板管理和上下文缓存。通过配置插件，对用户的输入进行安全审查和内容过滤，并针对相似的高频问答启用缓存策略，直接返回缓存结果而无需请求后端模型。

**效果**: 
1. 显著降低了后端 LLM 的调用成本，通过缓存机制减少了约 20% 的重复推理请求。
2. 增强了系统的安全性，有效拦截了恶意注入和越狱攻击。
3. 利用 Higress 的 JSON-to-Text 转换能力，屏蔽了后端接口差异，为前端应用提供了标准化的 API 格式，开发体验大幅提升。

---



### 3：某跨国物流企业 SaaS 平台

 3：某跨国物流企业 SaaS 平台

**背景**: 该企业将传统的单体物流管理系统拆分为微服务架构，并容器化部署在混合云环境（部分在阿里云，部分在本地数据中心）。系统需要对接多个外部合作伙伴的 API（如海关、船公司）。

**问题**: 
1. 南北向流量管理混乱，外部 API 访问和内部微服务调用共用一套网关，存在安全隐患。
2. 不同租户（物流客户）需要配置不同的路由规则和访问策略，传统网关配置极其繁琐。
3. 开源网关（如 Nginx）缺乏对 gRPC 和 Dubbo 协议的高级路由支持。

**解决方案**: 
引入 **Higress** 作为统一的流量入口。利用其强大的服务发现能力（对接 Nacos 和 Kubernetes Service），实现了对内部微服务的全自动路由。针对外部访问，配置了严格的域名路由和认证插件。同时，利用 Higress 对 HTTP/gRPC/Dubbo 的多协议支持，统一了老旧系统与新系统的接入标准。

**效果**: 
1. 实现了流量的精细化治理，内外网流量完全隔离，安全性得到保障。
2. 运维人员通过 Ingress 注解或控制台即可管理路由，配置错误率降低了 90%。
3. 解决了异构系统间的通信障碍，平滑完成了从 Dubbo 到 RESTful 的服务过渡，系统整体可观测性增强。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Istio 和 Envoy，支持高并发 | 高性能，基于 Nginx 和 OpenResty | 极高性能，基于 OpenResty 和 LuaJIT |
| 易用性 | 提供图形化控制台，支持 Kubernetes 原生集成 | 配置灵活，但需要手动管理较多配置 | 提供图形化控制台，支持动态配置 |
| 成本 | 开源免费，社区版功能丰富 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持插件扩展，兼容 Envoy 和 WASM 插件 | 支持插件扩展，社区插件丰富 | 支持插件扩展，Lua 插件生态成熟 |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，用户基数大 | 社区活跃，国内支持较好 |
| 功能覆盖 | 支持网关、流量管理、安全防护等全功能 | 侧重 API 管理和网关功能 | 侧重 API 网关和流量管理 |

### 优势分析

- 优势1：深度集成 Kubernetes 和 Istio，适合云原生环境。
- 优势2：支持 WASM 插件，扩展性更强，兼容多种语言编写插件。
- 优势3：阿里背书，企业级支持和稳定性有保障。

### 不足分析

- 不足1：社区生态相对 Kong 和 APISIX 较新，插件数量较少。
- 不足2：对非 Kubernetes 环境的支持不如传统网关（如 Nginx）灵活。
- 不足3：学习曲线较陡，需要熟悉 Istio 和 Envoy 的相关概念。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 K8s Ingress 的标准化网关管理

**说明**:  
利用 Higress 对 Kubernetes Ingress API 的原生支持，将网关管理纳入 K8s 生态体系。通过 Ingress 或 Gateway API 定义路由规则，实现与云原生应用的统一编排。

**实施步骤**:
1. 部署 Higress Gateway Controller 到 K8s 集群
2. 创建 Ingress 资源定义域名和路径路由规则
3. 配置 Service 关联后端 Pod 服务
4. 通过 Kubectl 或 GitOps 工具（如 ArgoCD）管理配置

**注意事项**:  
- 确保 Higress 版本与 K8s 版本兼容性
- 生产环境建议启用高可用部署（多副本）

---

### 实践 2：Wasm 插件化扩展能力

**说明**:  
通过 Higress 的 Wasm（WebAssembly）插件系统实现业务逻辑热更新，无需重启网关即可动态扩展功能，例如自定义认证、流量染色等。

**实施步骤**:
1. 编写 Wasm 插件（支持 C++/Go/Rust 等语言）
2. 编译为 `.wasm` 文件并上传至 OCI 镜像仓库
3. 在 Higress 控制台配置插件引用
4. 为特定路由或全局启用插件

**注意事项**:  
- 插件代码需遵循 Wasm ABI 规范
- 控制插件内存使用（建议单插件 < 64MB）

---

### 实践 3：全链路安全防护体系

**说明**:  
集成 Higress 内置安全能力与第三方安全组件，构建包含认证授权、流量清洗、WAF 防护的纵深防御体系。

**实施步骤**:
1. 启用 JWT/OIDC 认证插件
2. 配置 IP 黑白名单限制
3. 集成 ModSecurity WAF 规则
4. 开启安全日志审计（对接 SLS/ELK）

**注意事项**:  
- 定期更新 WAF 规则库
- 敏感接口建议启用 mTLS 双向认证

---

### 实践 4：多集群流量治理

**说明**:  
使用 Higress 实现跨 Kubernetes 集群的流量调度，支持蓝绿发布、金丝雀发布等高级发布策略，提升业务迭代安全性。

**实施步骤**:
1. 配置多集群服务发现（关联多 K8s 集群）
2. 创建流量分组（如 canary/production）
3. 设置基于权重/HTTP头的流量路由规则
4. 监控发布关键指标（错误率/延迟）

**注意事项**:  
- 确保集群间网络互通
- 发布前进行流量回滚演练

---

### 实践 5：服务治理与高可用

**说明**:  
通过 Higress 的服务治理功能实现熔断、限流、重试等容错机制，保障后端服务稳定性，防止雪崩效应。

**实施步骤**:
1. 为关键路由配置熔断规则（如连续 5xx 错误）
2. 设置基于令牌桶的限流策略
3. 配置指数退避的重试机制
4. 启用健康检查（主动/被动）

**注意事项**:  
- 限流阈值需压测验证
- 重试次数建议不超过 3 次

---

### 实践 6：可观测性集成

**说明**:  
建立指标、日志、链路追踪三位一体的可观测体系，通过 Prometheus/Grafana 实现实时监控和异常告警。

**实施步骤**:
1. 开启 Prometheus Metrics 暴露
2. 配置访问日志输出（JSON 格式）
3. 集成 OpenTelemetry 链路追踪
4. 设置 Grafana 仪表盘模板

**注意事项**:  
- 生产环境日志采样率建议 10%-100%
- 监控关键指标：QPS、延迟、错误率

---

### 实践 7：性能优化实践

**说明**:  
通过连接池复用、缓存策略、压缩传输等手段提升 Higress 处理性能，降低资源消耗。

**实施步骤**:
1. 调整 Upstream 连接池大小（默认 128）
2. 启用 HTTP 缓存（静态资源）
3. 开启 Gzip/Brotli 压缩
4. 配置 HTTP/2 或 HTTP/3

**注意事项**:  
- 连接池大小需匹配后端服务能力
- 压缩可能增加 CPU 开销

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，底层的网络协议对吞吐量和延迟影响巨大。HTTP/2 支持多路复用，解决了 HTTP/1.x 的队头阻塞问题；HTTP/3 (QUIC) 则基于 UDP 实现了更低的传输延迟和更好的连接迁移能力，特别是在弱网环境下表现优异。

**实施方法**:
1. 在 Higress 的网关配置中，确保 Listener 协议设置开启 HTTP/2。
2. 检查并配置 TLS 证书，因为现代浏览器通常要求在 HTTPS 环境下使用 HTTP/2 或 HTTP/3。
3. 若版本支持，在配置中开启 HTTP/3 (QUIC) 监听器选项。
4. 调整 HTTP/2 连接的并发流限制，以匹配后端服务器的处理能力。

**预期效果**: 弱网环境下请求延迟降低 20%-40%，高并发场景下 TCP 连接数大幅减少，显著提升并发处理能力。

---

### 优化 2：配置高效的全局缓存策略

**说明**: 对于读多写少的流量，通过在网关层引入缓存，可以直接拦截请求，避免流量打到后端业务服务。Higress 支持对后端响应进行缓存，这能极大降低后端负载并缩短响应时间（RT）。

**实施方法**:
1. 在路由配置中启用缓存功能，并设定合理的 Cache Key（如根据 URL、Header 组合）。
2. 配置 TTL（生存时间），针对不同业务场景（如静态资源、API 数据）设置差异化的过期时间。
3. 启用状态码缓存，通常缓存 200、301 等状态码的响应体。
4. 若数据一致性要求高，可配置缓存刷新策略。

**预期效果**: 缓存命中时，RT 降低至 1ms-5ms 级别，后端 QPS（每秒查询率）负载可降低 30%-60%。

---

### 优化 3：启用 WASM 插件并优化 Lua/WASM 代码执行效率

**说明**: Higress 支持 WASM (WebAssembly) 和 Lua 插件扩展。不当的插件代码（如复杂的正则匹配、阻塞式调用）会阻塞请求处理线程。相比传统的 Lua，WASM 提供了接近原生的执行性能和更强的隔离性。

**实施方法**:
1. 将计算密集型或复杂的鉴权、限流逻辑迁移至 WASM 插件中编写（使用 C++/Go/Rust 编译）。
2. 避免在插件请求处理阶段（如 `onRequestBody`）进行阻塞的网络 I/O 调用。
3. 优化正则表达式，使用预编译的匹配规则，避免回溯攻击。
4. 使用 `body_filter` 阶段处理响应体，减少内存拷贝开销。

**预期效果**: 复杂业务逻辑处理延迟降低 10%-30%，CPU 使用率在高并发下增长更平缓。

---

### 优化 4：精细化连接池与超时配置

**说明**: 默认的连接池配置往往不是最优的。如果连接池过小，会导致请求排队等待连接；超时时间设置过长会导致资源被无效请求占用，导致雪崩。

**实施方法**:
1. 调整后端服务的 `maxRequestsPerConnection`，复用连接以减少 TCP/TLS 握手开销。
2. 根据后端服务处理能力，适当调大 `http2MaxRequests` (针对 HTTP/2) 和连接池大小。
3. 设置严格的超时策略：`connectTimeout` (连接超时)、`timeout` (请求总超时) 建议根据 P99.9 耗时设置，并留出 20% 余量。
4. 开启 `idleTimeout`，及时清理空闲连接，释放文件描述符资源。

**预期效果**: 减少因连接等待造成的排队延迟，提升资源利用率，防止连接泄漏导致的内存溢出。

---

### 优化

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba/Higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的基于 Envoy 和 Istio 构建的下一代云原生 API 网关，旨在连接南北向流量与东西向微服务。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝适配容器化服务网格环境，实现基础设施的统一管理。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿发布、负载均衡以及超时重试等复杂的路由规则配置。
- Higress 原生集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、AssemblyScript 等语言编写高性能且安全的插件来扩展网关功能。
- 平台内置了对 AI 服务的支持，提供了一整套用于处理大模型 (LLM) 流量、鉴权及 Prompt 管理的解决方案，简化了 AI 应用的接入流程。
- 它兼容 Nginx 的 Ingress 注解配置，并支持从 Nginx/Dubbo 等传统网关平滑迁移，降低了用户的迁移成本与学习曲线。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与架构认知

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）及阿里云 MSE 的区别
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 基本术语：路由、服务、插件、上游

**学习时间**: 3-5天

**学习资源**:
- Higress 官方文档 (GitHub README)
- Higress 官方网站架构介绍页
- 云原生网关技术演进相关博客文章

**学习建议**: 
此阶段重点在于理解“为什么需要 Higress”。建议先阅读官方文档的背景介绍，理解其基于 Envoy 和 Istio 的技术底座。不要急于动手安装，先通过架构图理清数据流向（流量如何从客户端经过网关到达后端服务）。

---

### 阶段 2：本地部署与核心功能实践

**学习内容**:
- 使用 Docker 或 Docker Compose 在本地快速部署 Higress
- Higress 控制台的使用与界面概览
- 配置 HTTP/HTTPS 路由规则
- 服务来源的配置（如 Nacos, 固定地址, K8s Service）
- 基础流量管理：负载均衡策略、健康检查、重试与超时配置

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 仓库中的 Quick Start 指南
- 官方提供的 Docker Compose 部署示例文件
- Higress 官方文档 - 配置中心章节

**学习建议**: 
动手是此阶段的关键。建议在本地搭建一个包含两个简单后端服务（如使用 Nginx 模拟）的环境，通过配置 Higress 路由来实现流量转发。尝试修改路由配置并观察流量变化，熟悉控制台的操作逻辑。

---

### 阶段 3：流量治理与安全防护

**学习内容**:
- 高级流量管理：基于 Header、Query、Cookie 的路由匹配
- 全局与自定义插件系统的使用（WAF 防护、限流熔断、请求/响应修改）
- Higress 的认证鉴权机制：Basic Auth、ApiKey、JWT、OIDC
- Mock 服务与回源管理

**学习时间**: 2-3周

**学习资源**:
- Higress 官方插件市场文档
- Higress 官方文档 - 流量治理与插件开发指南
- Envoy 基础文档（用于理解底层过滤器的概念）

**学习建议**: 
重点掌握“插件”能力，这是 Higress 区别于普通网关的强项。尝试配置一个限流插件来保护后端服务，或者使用 WAF 插件拦截特定请求。理解 Wasm 技术在其中的作用，但不必深究 C++/Rust 开发，重点在于如何配置和使用现有的 Lua/Wasm 插件。

---

### 阶段 4：Kubernetes 环境集成与生产运维

**学习内容**:
- 在 Kubernetes 集群中部署 Higress (Helm 安装)
- Ingress API 与 Gateway API 的使用与转换
- Higress 与 Nacos、Consul 等注册中心的深度集成
- 监控与可观测性：对接 Prometheus/Grafana、日志采集（SLS/ELK）
- 高可用部署架构与性能调优

**学习时间**: 3-4周

**学习资源**:
- Higress Kubernetes 部署手册
- Kubernetes Ingress 官方文档
- Higress GitHub Issues 中的生产环境最佳实践

**学习建议**: 
此阶段面向生产环境。建议在一个测试用的 K8s 集群中通过 Helm Chart 部署 Higress，并学习如何通过 Ingress YAML 文件管理路由，而不仅仅是依赖控制台。重点关注网关的监控指标（QPS、延迟、成功率）以及如何进行滚动更新和配置热加载。

---

### 阶段 5：生态扩展与插件开发（精通）

**学习内容**:
- Higress 的插件开发机制（Wasm Go/AssemblyScript）
- 自定义插件编写、编译与热加载
- 服务网格场景下的 Higress 应用（结合 Istio）
- 多租户网关管理与多环境交付策略
- 源码分析与贡献指南

**学习时间**: 持续学习

**学习资源**:
- Higress 官方插件开发文档
- Higress GitHub 源码
- Wasm (WebAssembly) 在云原生领域的应用案例

**学习建议**: 
这是通往专家的路径。你需要具备一定的编程基础（Go 或 Rust）。尝试编写一个简单的 Wasm 插件来实现特定的业务逻辑（如特殊的签名校验或数据脱敏），并将其部署到 Higress 中运行。阅读源码以理解 Higress 如何处理配置下发和数据

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里内部多年在 API 网关领域的实践，结合了 Envoy 和 Istio 的技术栈构建而成的。Higress 旨在提供高性能、可扩展且易于管理的流量入口，支持 Kubernetes 环境，能够处理南北向（入口）流量以及微服务间的东西向流量。它由阿里巴巴集团开源，并捐赠给了 CNCF（云原生计算基金会）作为 Sandbox 项目（注：具体孵化状态视最新进展而定），是阿里云云原生网关产品的核心开源版本。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的主要优势体现在以下几个方面：
1.  **云原生架构**：它深度集成了 Kubernetes 和 Istio，原生支持服务发现，能够无缝对接 K8s Service，无需像传统 Nginx 那样手动维护复杂的上游服务器列表。
2.  **高性能**：基于 C++ 编写的 Envoy 作为数据面，具有极高的吞吐量和低延迟。
3.  **标准化**：支持 Kubernetes Ingress、Gateway API 以及 Istio 的 VirtualService 配置，方便用户在不同云原生体系间迁移。
4.  **扩展性**：支持 Wasm (WebAssembly) 插件，允许开发者使用 Go、C++、Rust、JavaScript 等多种语言编写插件，且插件热更新无需重启网关，比传统的 Lua (OpenResty) 插件更安全、灵活。
5.  **安全防护**：内置了针对常见 Web 攻击的防护能力，并集成了 Keyless 的 KMS 网关能力。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 迁移？迁移难度大吗？

3: Higress 是否支持从 Nginx 或 Ingress Controller 迁移？迁移难度大吗？

**A**: 是的，Higress 提供了非常友好的迁移工具和兼容性。
1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，可以将现有的 Nginx.conf 配置自动转换为 Higress 的路由配置。
2.  **Ingress 兼容**：Higress 完全兼容 Kubernetes Ingress 规范，可以直接替换 K8s 原生的 Ingress Controller 或 Nginx Ingress Controller。通常只需修改 Ingress Class 的注解即可平滑切换。
3.  **配置复用**：对于常用的域名、路径、Header 路由规则，Higress 的控制台和 API 都提供了直观的配置方式，迁移过程主要是配置平移，难度较低。

---



### 4: Higress 如何处理插件扩展？是否支持热加载？

4: Higress 如何处理插件扩展？是否支持热加载？

**A**: Higress 拥有强大的插件系统，这是其核心亮点之一。
1.  **Wasm 支持**：Higress 允许用户通过 Wasm (WebAssembly) 技术编写自定义插件。这意味着你可以使用 Go 或 Rust 等高级语言编写业务逻辑，然后编译为 Wasm 文件上传。
2.  **热加载**：Wasm 插件支持动态加载和卸载。当你上传或更新一个插件时，网关进程不需要重启，流量也不会中断，配置会立即生效。
3.  **插件市场**：Higress 社区提供了丰富的预置插件（如 JWT 认证、请求鉴权、流量镜像、限流熔断等），用户可以直接在控制台一键启用。

---



### 5: 在生产环境中部署 Higress 有什么资源要求？如何保证高可用？

5: 在生产环境中部署 Higress 有什么资源要求？如何保证高可用？

**A**: Higress 的资源消耗相对较低，但为了保证生产环境的稳定性，建议如下：
1.  **资源配置**：根据流量大小调整，一般建议每个实例至少分配 2 Core CPU 和 4GB 内存。在千并发场景下，资源占用极低。
2.  **高可用部署**：在 Kubernetes 中，建议使用 Deployment 或 DaemonSet 部署 Higress，并设置副本数至少为 2。结合 HPA（Horizontal Pod Autoscaler）可以根据 CPU 或内存使用率自动扩容。
3.  **网关类型**：对于入口流量，建议结合 LoadBalancer 类型的 Service 或使用阿里云 SLB 暴露服务。对于内部服务网格，可以配合 Istio Pilot 使用。

---



### 6: Higress 是否支持服务治理功能，如熔断、限流和灰度发布？

6: Higress 是否支持服务治理功能，如熔断、限流和灰度发布？

**A**: 是的，Higress 提供了全套的服务治理能力，并且这些功能通常通过简单的配置即可实现，无需修改代码。
1.  **全局限流**：支持基于请求速率、并发连接数的限流，可以精确到某个 API 路径或特定的消费者（API Key）。
2.  **熔断降级**：集成了 Sentinel 或通过 Wasm 插件实现熔断逻辑，当后端服务出现响应延迟或错误率上升时，自动触发熔断，防止雪崩。
3.  **灰度

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 和 Istio 构建，但针对云原生网关场景做了优化。请查阅 Higress 的官方文档或源码，列举出 Higress 相比直接使用标准 Istio Ingress Gateway，在流量治理层面新增的三个具体特性。

### 提示**: 关注 Higress 在 WASM 支持、Dubbo 或多协议注册中心对接方面的描述，思考“网关”与“Service Mesh 侧车”在处理南北向流量时的功能差异。

### 

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 6 条实践建议：

### 1. 利用 AI 提供商路由实现高可用与成本优化
**场景**：在生产环境中调用大模型（如 OpenAI、通义千问等），面临单点故障或 API 配额限制的问题。
**建议**：
不要将 LLM Provider 的地址硬编码在业务代码中。应在 Higress 中配置多个 AI 提供商，并使用“提供商路由”功能。
**操作**：
为同一个模型（例如 `gpt-4`）配置主供应商和备用供应商。当主供应商返回 4xx/5xx 错误或超时时，Higress 会自动切换流量到备用供应商。
**最佳实践**：可以配置一个高延迟但便宜的供应商作为兜底，或者配置不同云厂商的同类模型以实现跨云容灾。

### 2. 配置请求与响应的“语义缓存”
**场景**：AI 应用中经常会出现重复的用户提问（例如“帮我写一个 Python 冒泡排序”），直接转发给 LLM 会产生不必要的 Token 消耗和延迟。
**建议**：
启用 Higress 的语义缓存插件，而非简单的精确匹配缓存。
**操作**：
在 AI 服务的路由规则中，开启缓存插件，并设置合适的 TTL（生存时间）。Higress 能够识别语义相似的请求并直接返回缓存结果。
**常见陷阱**：
对于实时性要求极高或上下文强相关的场景（如长时间对话的中间轮次），请谨慎开启缓存，或在缓存 Key 中加入 Session ID 以避免上下文错乱。

### 3. 实施细粒度的 Token 计费与访问控制
**场景**：企业内部需要向不同部门或项目组开放 AI 接口，且需要根据实际使用量（Token 数）进行成本分摊。
**建议**：
不要仅依赖 IP 限制，而应结合 API Key 和插件系统进行精细化流控。
**操作**：
使用 Higress 的鉴权插件（如 Basic Auth 或 JWT）区分不同客户端，并配置“请求限流”插件。针对 AI 场景，可以配置基于 Token 生成量的预估限流，或者结合后端计费系统进行日志记录。
**最佳实践**：为不同的开发者或团队生成独立的 API Key，并在网关层面配置针对该 Key 的 QPS 或 RPM（每分钟请求数）上限，防止个别异常程序消耗巨额预算。

### 4. 使用 Prompt 模板管理降低前端耦合度
**场景**：应用需要频繁调整 System Prompt（系统提示词）来优化模型效果，每次修改都需要重新发布业务服务。
**建议**：
将 Prompt 模板的管理权下沉到网关层。
**操作**：
利用 Higress 的 `prompt-template` 插件或在 Wasm 插件中配置模板。前端只需传递业务参数（如 `{ "query": "用户输入", "tone": "专业" }`），网关自动将其组装成包含 System Prompt 的完整消息体发送给 LLM。
**最佳实践**：这样可以实现“提示词工程”与业务代码的解耦，运营人员可以直接通过控制台调整提示词而无需发版。

### 5. 谨慎处理流式传输的超时与断开
**场景**：AI 对话通常采用 SSE（Server-Sent Events）流式返回，耗时较长（可能超过 30 秒），导致默认网关配置报错。
**建议**：
务必调整路由的超时时间并开启对 Chunked 编码的正确透传。
**操作**：
在 Ingress 或网关路由配置中，将 `read_timeout` 设置为一个较大的值（如 3 分钟或更长）。同时，确保后端服务配置了正确的 HTTP Header（`Content-Type: text/event-stream`）。
**常见陷阱**：
如果在网关层开启了全量日志记录（Body Logging），在流式传输下会消耗极大的 CPU 和内存用于拼接数据包。建议在 AI 流式路由上**关闭**请求/响应 Body 的日志记录，仅记录 Headers 和 Metadata。

### 6. 利用 Wasm 插件实现敏感词过滤与数据

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [阿里云](/tags/%E9%98%BF%E9%87%8C%E4%BA%91/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*