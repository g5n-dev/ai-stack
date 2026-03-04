---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-04T13:43:44+08:00
draft: false
entry_kind: "auto"
tags: ["API网关", "Higress", "阿里开源", "AI原生", "Istio", "Envoy", "LLM", "MCP协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress：阿里巴巴开源的 AI 原生 API 网关** **1. 项目概况** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。该项目基于 Istio 和 Envory 构建，并扩展了 WebAssembly (WASM) 插件能力。它目前是一个** AI 原生** 的 API 网关，编程"
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
- **星标**: 7,635 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过深度集成 WASM 插件能力，实现了对云原生流量管理与大模型应用场景的统一支持。它既保留了传统微服务路由与 Kubernetes Ingress 的核心功能，又针对 LLM 服务提供了 AI 网关特性及 MCP 服务器托管，旨在解决混合架构下的流量治理与工具集成难题。本文将梳理其架构设计，并重点解析 AI 网关特性、MCP 系统及插件扩展机制。

---
## 摘要

**Higress：阿里巴巴开源的 AI 原生 API 网关**

**1. 项目概况**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。该项目基于 Istio 和 Envory 构建，并扩展了 WebAssembly (WASM) 插件能力。它目前是一个** AI 原生** 的 API 网关，编程语言为 Go，在 GitHub 上拥有超过 7,600 颗星。

**2. 核心架构**
Higress 采用**控制平面与数据平面分离**的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **配置分发**：通过 xDS 协议传播配置，具备毫秒级延迟且不中断连接，非常适合 AI 长连接流式响应场景。

**3. 三大核心功能**
Higress 提供了三大主要功能，覆盖了传统微服务与新兴 AI 应用场景：

*   **AI 网关**：
    *   为 LLM（大语言模型）应用提供统一 API。
    *   支持 30+ 家 LLM 提供商的协议转换。
    *   具备可观测性、缓存和安全防护能力（核心插件：`ai-proxy`, `ai-cache`, `ai-security-guard` 等）。
*   **MCP 服务器托管**：
    *   托管模型上下文协议 (MCP) 服务器。
    *   使 AI Agent 能够调用工具和服务（核心组件：`mcp-router`, `jsonrpc-converter`）。
*   **Kubernetes Ingress**：
    *   作为 Kubernetes 入口控制器。
    *   兼容 nginx-ingress 注解，支持微服务路由。

---
## 评论

**深度技术评论**

**总体定位**

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关。其核心特征在于将传统的微服务流量治理能力与大模型（LLM）应用所需的协议处理、路由及安全功能进行了整合。该项目旨在解决企业在混合架构下，同时处理传统业务流量与 AI 应用流量的治理需求。

**技术维度分析**

**1. 架构演进：集成 AI 原生处理能力**
*   **核心特性**：Higress 在标准网关功能基础上，增加了对 AI 协议的深度支持。这包括对 SSE（Server-Sent Events）流式传输的原生处理，以及对 LLM 上下文的管理。
*   **MCP 协议支持**：项目支持托管 MCP (Model Context Protocol) 服务器。这一特性使网关能够作为 AI Agent 与外部数据源交互的中间层，扩展了网关在 AI 生态中的应用边界。
*   **WASM 插件生态**：通过 WebAssembly 技术，Higress 支持使用 Go、Rust 或 C++ 编写插件。这种机制实现了业务逻辑的热更新，降低了扩展功能的开发门槛，特别是在处理 AI 鉴权、提示词注入等动态逻辑时提供了灵活性。

**2. 工程实践：统一流量治理入口**
*   **混合流量管理**：Higress 提供了统一的控制平面，用于管理 Kubernetes Ingress 流量和 AI Gateway 流量。这种设计避免了企业为了引入 AI 应用而部署独立代理服务带来的架构碎片化问题。
*   **资源保护与优化**：网关层支持针对 Token 的计费、限流以及 Prompt 缓存策略。这使得系统可以在流量进入昂贵的后端 LLM 之前进行预处理和管控，有助于优化后端服务的资源消耗。

**3. 代码与架构规范**
*   **底层架构**：项目遵循控制面与数据面分离的架构模式，符合云原生设计原则。这种设计有利于保障系统的高可用性和水平扩展能力。
*   **开发规范**：项目基于 Go 语言开发，文档覆盖了架构设计、构建流程及二次开发指南。多语言支持（EN/JP/ZH）及详细的模块划分表明其具备标准化的工程结构。

**4. 社区与生态**
*   **活跃度**：项目由阿里巴巴主导开源，在 GitHub 上拥有较高的关注度（Star 数 7.6k+）。这表明该项目不仅有商业公司的技术支持，也具备一定的社区基础。
*   **应用场景**：社区讨论和技术迭代主要集中在 WASM 插件开发、AI 模型对接以及云原生集成方面，反映了其在实际业务场景中的持续演进。

**5. 学习与参考价值**
*   **技术融合参考**：对于开发者而言，Higress 提供了一个研究如何将云原生网关技术与 AI 基础设施相结合的实例。其代码库和架构设计对于理解 WASM 在网关中的应用、LLM 流量控制逻辑具有参考意义。

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 不仅仅是一个传统的 API 网关，它被明确定义为 **AI Native API Gateway**（AI 原生网关），这标志着云原生网关技术向 AI 基础设施领域的关键演进。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的架构设计体现了“深度集成”与“标准扩展”并重的哲学。

### 1.1 技术栈与架构模式
Higress 采用了 **控制平面与数据平面分离** 的标准云原生架构模式。
*   **数据平面**：深度定制了 **Envoy**。Envoy 以高性能 C++ 网络库著称，擅长处理长连接、高并发和低延迟流量。Higress 在此基础上针对 AI 场景（如 SSE 流式传输）进行了专门优化。
*   **控制平面**：基于 **Istio** 生态构建，使用 Go 语言开发。它负责配置的下发、服务的发现以及网关的全局管理。
*   **扩展机制**：核心亮点在于 **WebAssembly (WASM)** 插件系统。通过代理级 WASM (Proxy-WASM) 标准，Higress 允许用户使用 C++, Go, Rust, AssemblyScript 等语言编写插件，并在运行时动态加载，无需重启网关或重新编译二进制文件。

### 1.2 核心模块与关键设计
*   **AI 网关层**：这是 Higress 区别于 Nginx 或传统 Kong 的核心。它在网关层直接集成了大模型（LLM）的语义理解、提示词管理、Token 计费与流式处理能力。
*   **MCP (Model Context Protocol) 服务器**：Higress 内置了对 MCP 协议的支持，使其不仅能转发流量，还能作为 AI Agent 的工具托管中心，将后端 API 转化为 AI 可调用的工具。
*   **Kubernetes Ingress**：完全兼容 K8s Ingress API，可以作为 K8s 集群的统一流量入口。

### 1.3 架构优势分析
*   **毫秒级配置推送**：基于 xDS 协议（Istio/Envoy 的配置协议），配置变更可秒级生效且不中断 TCP 连接。这对于 AI 应用的长连接（SSE 流式响应）至关重要，避免了传统网关重载配置导致的连接断开和响应截断。
*   **异构系统统一**：通过将 AI 流量、微服务 RPC 流量和外部 API 流量在同一网关处理，简化了基础设施的拓扑结构。

---

## 2. 核心功能详细解读

### 2.1 AI 网关特性
Higress 将 AI 时代的特殊需求“网关化”：
*   **LLM 提供商抽象**：通过统一的 OpenAI 兼容 API 接口，屏蔽了不同模型厂商（通义千问、OpenAI、Claude 等）的差异。用户只需修改网关配置即可切换模型，无需修改业务代码。
*   **Prompt 模板管理**：支持在网关层预定义 Prompt 模板，实现提示词的版本控制和动态注入。
*   **Token 统计与限流**：传统网关基于 QPS（每秒请求数）限流，而 AI 网关基于 Token 或字符数计费和限流，这直接关联到成本控制。
*   **结果缓存**：针对 LLM 请求成本高、延迟大的特点，支持语义缓存或精确匹配缓存，减少重复计算。

### 2.2 MCP 系统与工具调用
MCP 是连接 AI 应用与数据源的标准协议。Higress 充当 MCP Server 或 Host，允许 AI Agent 通过网关安全地访问企业内部 API。这意味着网关从单纯的“流量管道”变成了“智能代理的执行层”。

### 2.3 与同类工具对比
| 特性 | Higress | Nginx / OpenResty | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **内核语言** | C++ (Envoy) + Go (Control) | C (Nginx) + Lua | C / Pongo | Lua / C |
| **AI 原生支持** | **内置 (Provider 路由, Token 限流)** | 需自行编写脚本 | 依赖插件，生态较弱 | 依赖插件，生态较弱 |
| **热更新** | **不丢连接 (xDS)** | reload 会丢失连接 | 支持 | 支持 |
| **扩展性** | **WASM (多语言, 高性能, 隔离性)** | Lua/LuaJIT (单语言, 阻塞风险) | Python/Go/JS | Lua/Java/Go |
| **云原生集成** | **深度集成 Istio** | 需额外组件 (如 Ingress Controller) | KIC (Kong Ingress Controller) | KIC |

**解决的关键问题**：解决了企业接入 LLM 时面临的**厂商锁定**、**成本不可控**（Token 消耗）、**开发效率低**（需自行处理流式传输和协议差异）以及**安全风险**（直接暴露 API Key）问题。

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **WASM 虚拟机集成**：Higress 使用 `wasmtime` 或类似的运行时嵌入 Envoy。当请求进入时，Envoy 会将请求/响应头和 Body 传递给 WASM 虚拟机。插件逻辑在沙箱中执行，处理完成后将控制权交还给 Envoy。这保证了插件崩溃不会导致网关崩溃。
*   **流式处理优化**：在 AI 对话场景中，响应是流式的（SSE）。Higress 在数据平面实现了流式数据的透传与拦截能力。例如，它可以在流式传输过程中实时计算 Token 数量，或者在流结束后进行日志记录，而不需要缓冲整个响应。

### 3.2 代码组织
项目主要分为两个大模块：
1.  **`/pkg`**：Go 语言编写的控制平面逻辑。包含配置解析、Kubernetes Controller、以及与 Istio 的交互逻辑。
2.  **`/plugins`**：WASM 插件的源码目录。通常包含 Go 或 C++ 编写的插件示例和核心实现（如 AI 请求的转发、鉴权逻辑）。

### 3.3 性能与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **异步 I/O**：非阻塞架构使得单节点能支撑极高的并发连接数，这对于维持大量并发的 AI 会话至关重要。

---

## 4. 适用场景分析

### 4.1 最佳适用场景
*   **AI 应用开发平台**：企业构建类似 ChatGPT 的内部应用，需要统一管理不同供应商的 API Key，并对员工使用进行计费或限额。
*   **微服务 + AI 混合架构**：传统业务已迁移至 Kubernetes，现在需要引入 AI 能力。使用 Higress 可以避免引入新的 AI 专用网关，统一技术栈。
*   **SaaS 企业**：需要向客户暴露 AI 能力，利用 Higress 的鉴权、限流和多模型切换能力，实现灵活的 API 策略。

### 4.2 不适合的场景
*   **极简静态站点**：对于只需要简单的反向代理，Nginx 足够且更轻量。
*   **极端低延迟交易系统**：虽然 Envoy 极快，但引入 WASM 插件层会引入微秒级至毫秒级的额外开销，对于纳秒级敏感的金融高频交易可能不适用（但绝大多数业务场景无需担心此问题）。

### 4.3 集成方式
通常作为 Kubernetes 的 **Ingress Controller** 或 **Gateway API** 的实现部署。通过 CRD (Custom Resource Definition) 定义路由规则和插件配置。

---

## 5. 发展趋势展望

### 5.1 AI 基础设施标准化
Higress 正在推动 AI 网关的标准化。未来，类似“LLM 路由”、“Prompt 管理”、“Token 统计”将成为 API 网关的标配功能，就像现在的“限流”和“熔断”一样。

### 5.2 Dapr 与 Sidecar 演进
虽然目前 Higress 主要作为边缘网关，但其 Istio 血统使其具备向 Service Mesh 数据平面下沉的潜力。未来可能会看到 Higress 的能力直接嵌入到业务 Pod 的 Sidecar 中，实现微服务间的 AI 通信治理。

### 5.3 可观测性与 AIOps
随着 AI 流量的增加，如何追踪 Prompt 的质量、模型的响应延迟将成为新的可观测性维度。Higress 未来可能会深度集成 OpenTelemetry，专门针对 AI 语义层进行监控。

---

## 6. 学习建议

### 6.1 适合人群
*   **云原生架构师**：希望深入理解 Istio/Envoy 架构及 WASM 技术。
*   **AI 应用开发者**：需要构建生产级 AI 后端服务，关注稳定性、成本和安全。
*   **Go/C++ 开发者**：希望参与高性能基础中间件开发。

### 6.2 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 和 Service Mesh 基本概念。
2.  **核心**：阅读 Envoy 官方文档，理解 xDS 协议和 Filter 机制。
3.  **扩展**：学习 Proxy-WASM 标准，尝试用 Go 或 Rust 编写一个简单的 Higress 插件（如修改 HTTP Header）。
4.  **实践**：在本地 Kind 集群中部署 Higress，配置一个转发到 OpenAI 的路由，并开启 Token 统计。

---

## 7. 最佳实践建议

### 7.1 部署与配置
*   **资源隔离**：在生产环境中，建议将 AI 网关与传统业务网关分开部署（使用不同的 Higress 实例或 Deployment），因为 AI 请求通常长连接多、耗时长，可能占用大量连接池，影响普通短连接业务。
*   **WASM 插件性能**：虽然 WASM 性能优于 Lua，但仍应避免在插件中进行密集的 CPU 计算或阻塞式 I/O 操作。插件应专注于“逻辑判断”，而非“数据处理”。

### 7.2 安全性
*   **敏感信息保护**：切勿将 API Key 明文写入配置仓库。利用 Higress 的 Secret 管理或集成 Kubernetes Secrets / Vault。
*   **Prompt 注入防护**：在网关层配置插件，对用户输入进行清洗，防止 Prompt Injection 攻击。

### 7.3 优化建议
*   **开启缓存**：对于高频重复的问题，务必开启 Higress 的结果缓存，可大幅降低 Token 成本。
*   **连接池调优**：AI 后端服务通常有严格的并发限制（TPM/RPM），需在 Higress 上游配置中精确调优连接池大小，避免网关将后端打垮。

---

## 8. 哲学与方法论：第一性原理与权衡

### 8.1 �

---
## 代码示例




```python
# 示例1：使用Higress进行流量路由
def example_traffic_routing():
    """
    场景：根据请求头将流量路由到不同版本的服务（如灰度发布）
    实现方式：通过Higress的Ingress配置定义路由规则
    """
    # 以下是Kubernetes Ingress的YAML配置示例
    ingress_config = """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: canary-ingress
  annotations:
    # Higress特定注解：启用基于请求头的路由
    higress.io/route-based: "header"
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: service-v1  # 默认服务版本
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: service-v2  # 灰度版本服务
            port:
              number: 80
        # 当请求头x-canary: true时路由到v2
        higress.io/headers: "x-canary:true"
"""
    print("流量路由配置已生成：\n" + ingress_config)

**说明**: 这个示例展示了如何使用Higress实现基于请求头的流量路由，常用于灰度发布场景。当请求头包含`x-canary:true`时，流量会导向新版本服务(v2)，否则使用默认版本(v1)。

```python


def example_jwt_auth():
"""
场景：保护API接口，要求客户端提供有效的JWT令牌
实现方式：通过Higress的Plugin配置JWT认证
"""
plugin_config = """
apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
name: jwt-auth
spec:
# 使用官方JWT认证插件
url: oci://higress-registry.cn-hangzhou.cr.aliyuncs.com/plugins/jwt-auth:1.0.0
# 插件配置参数
config:
# 签名密钥（生产环境应从安全存储获取）
secret: "your-256-bit-secret"
# 令牌位置
from:
- header: "Authorization"
prefix: "Bearer "
# 不需要认证的路径
skip_paths:
- "/api/public"
"""
print("JWT认证插件配置已生成：\n" + plugin_config)

```python
# 示例3：Higress限流配置
def example_rate_limiting():
    """
    场景：防止API被过度调用，保护后端服务
    实现方式：通过Higress的Annotation配置限流规则
    """
    ingress_config = """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rate-limited-ingress
  annotations:
    # 每秒最多10个请求
    higress.io/rate-limit: "10"
    # 突发流量允许20个请求
    higress.io/rate-limit-burst: "20"
    # 基于客户端IP限流
    higress.io/rate-limit-key: "client_ip"
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
"""
    print("限流配置已生成：\n" + ingress_config)

**说明**: 这个示例展示了如何通过Higress的Ingress注解实现API限流。配置限制每个客户端IP每秒最多10个请求（突发允许20个），有效防止后端服务被过载调用。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴内部拥有众多的大型电商业务系统，这些系统在“双十一”等大促期间面临着巨大的流量压力。原有的 API 网关架构在应对每秒百万级 QPS 的流量洪峰时，资源消耗巨大且扩展性面临瓶颈。

**问题**: 
1. 传统网关在处理海量 HTTP 请求时，内存占用过高，导致服务器成本急剧上升。
2. 业务迭代速度加快，需要网关支持更灵活的流量管理和插件扩展机制，但旧架构修改配置往往需要重启服务，影响业务稳定性。
3. 云原生架构转型过程中，需要统一 Kubernetes 集群与虚拟机环境的流量入口管理。

**解决方案**: 
团队基于 Higress 构建了下一代云原生 API 网关。利用 Higress 的高性能 Istio 数据面能力，将业务流量从旧网关平滑迁移至 Higress。通过 Higress 的热更新机制实现了路由规则和插件的动态加载，并利用其标准 WASM (WebAssembly) 接口开发了定制化的限流、鉴权及流量染色插件。

**效果**: 
1. 成本优化：在大流量场景下，Higress 的内存占用相比原网关降低了 50% 以上，显著节省了服务器资源成本。
2. 运维效率：实现了配置的毫秒级动态生效，消除了因配置变更导致的重启风险，保障了电商业务的 99.99% 高可用性。
3. 统一管控：成功打通了容器环境与遗留微服务架构的流量治理，实现了统一的流量视图和管理策略。

---



### 2：AIGC 应用开发者（AI 代理场景）

 2：AIGC 应用开发者（AI 代理场景）

**背景**: 
随着大语言模型（LLM）的爆发，一家初创 AI 应用公司需要构建一个面向 C 端用户的智能对话助手。该应用后端接入了 OpenAI 的 GPT-4 模型，同时也接入了国内外的其他开源模型，旨在根据用户提问的复杂度智能路由至不同的模型以平衡效果与成本。

**问题**: 
1. 直接将 API Key 暴露在前端存在极大的泄露风险，需要一层安全代理。
2. LLM 接口调用按 Token 计费，成本高昂，且单个用户的请求容易触发速率限制。
3. 需要实现“提示词缓存”和“请求拦截”等逻辑，但开发独立的中转服务耗时较长。

**解决方案**: 
该团队采用 Higress 作为 AI 服务的网关。利用 Higress 原生支持的 AI 代理插件（AI Proxy），在后端配置多个 LLM 提供商。通过编写简单的 Lua 脚本或使用内置插件，实现了基于请求特征的智能路由（简单问题路由至便宜模型，复杂问题路由至 GPT-4）。同时，利用 Higress 的全链路缓存能力减少了重复 Token 的消耗。

**效果**: 
1. 安全增强：隐藏了后端真实的 API Key，通过网关统一进行身份认证和鉴权。
2. 成本降低：通过智能路由策略，在保证用户体验的前提下，将模型调用成本降低了约 40%。
3. 快速上线：利用 Higress 的 AI 特性，无需编写额外的后端代码即可在 1 天内完成了多模型接入、流式输出处理及错误重试机制的搭建。

---



### 3：某大型互联网企业微服务治理

 3：某大型互联网企业微服务治理

**背景**: 
该企业拥有数百个微服务，技术栈涉及 Java、Go 和 Python。在从微服务架构向 Service Mesh (服务网格) 演进的过程中，团队发现完全的 Sidecar 模式带来了过高的网络延迟和运维复杂度，特别是在对延迟极其敏感的支付和交易链路上。

**问题**: 
1. Sidecar 代理模式在多跳调用中累积了不可忽视的网络延迟，影响了交易链路的性能。
2. 运维团队难以独立于业务开发团队去管理复杂的流量规则，导致跨部门沟通成本高。
3. 需要一套既能支持 K8s Ingress 流量，又能处理服务间内部流量的统一网关。

**解决方案**: 
企业引入 Higress，采用了“Ingress 网关 + 服务间透明代理”的混合部署模式。对于南北向流量（外部进入集群的流量）使用 Higress 作为入口网关；对于东西向流量（服务间调用），在关键链路上利用 Higress 的强大路由能力替代部分 Sidecar 功能。通过 Higress 提供的控制台，运维人员可以直接配置基于权重、Header 的金丝雀发布和蓝绿发布策略。

**效果**: 
1. 性能提升：在关键交易链路上，通过优化网络调用路径，将平均延迟降低了 20%-30%。
2. 业务敏捷性：开发人员通过自助式配置 Higress 规则，实现了分钟级的业务灰度发布，不再需要依赖运维修改复杂的配置文件。
3. 统一标准：建立了统一的流量管理标准，解决了多种网关并存的混乱局面，简化了服务治理的复杂度。

---
## 对比分析

## 与同类方案对比

| 维度 | Higress | Kong | APISIX | Nginx + Lua |
|------|---------|------|-------|-------------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和OpenResty | 极高性能，基于OpenResty和LuaJIT | 高性能，依赖Nginx核心 |
| 易用性 | 提供可视化控制台，配置简单，支持Kubernetes集成 | 配置复杂，需手动管理路由和插件 | 配置灵活，但学习曲线较陡 | 需手动编写Lua脚本，门槛高 |
| 扩展性 | 支持插件扩展，兼容Istio和Kubernetes | 丰富的插件生态，支持自定义插件 | 强大的插件系统，支持动态加载 | 依赖Lua模块，扩展性有限 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 完全开源免费 | 完全开源免费 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，文档丰富 | 社区活跃，国内支持较好 | 社区较小，依赖Nginx生态 |

### 优势分析

- 优势1：基于Envoy和Istio，天然支持云原生和微服务架构。
- 优势2：提供开箱即用的可视化控制台，降低运维复杂度。
- 优势3：与阿里云生态深度集成，适合已有阿里云服务的用户。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态尚不够丰富。
- 不足2：社区规模和文档完善度不如Kong和Nginx。
- 不足3：对非Kubernetes环境的支持较弱。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**: Higress 基于 Envoy 构建，针对云原生和高并发场景进行了深度优化。充分利用 Envoy 的高性能 L3/L7 处理能力，并结合 Higress 自研的配置热更新机制，可以实现毫秒级的配置下发与路由变更，同时保持极低的资源消耗。

**实施步骤**:
1. 在部署时根据业务规模调整 `envoy` 的资源限制（Request/Limit），建议初始值设置为 2C4G。
2. 开启 Envoy 的访问日志（Access Log）并配置 JSON 格式输出，以便对接日志系统。
3. 利用 Higress 的 Wasm 插件能力扩展 Envoy 功能，而不是修改核心代码。

**注意事项**: 避免在 Envoy 原生配置中直接修改 Higress 管理的字段，应通过 Higress 控制台或 API 进行配置，以免配置冲突。

---

### 实践 2：标准 K8s Ingress 与 Gateway API 的灵活运用

**说明**: Higress 兼容标准的 Kubernetes Ingress 规范，并积极支持 Gateway API。通过声明式的方式管理路由规则，可以实现业务与基础设施的解耦，降低迁移成本，提升多集群管理的效率。

**实施步骤**:
1. 定义 IngressClass 或 GatewayClass 来明确指定 Higress 作为流量入口控制器。
2. 使用标准的 Ingress YAML 定义域名和路径转发规则。
3. 对于复杂路由（如基于 Header、权重路由），优先使用 Higress 提供的 CRD（如 `IngressRoute`）或 Gateway API 资源。

**注意事项**: 当同时使用 Ingress 和 Gateway API 时，需注意路由匹配优先级，避免规则冲突导致流量被意外截断。

---

### 实践 3：Wasm 插件实现业务逻辑热加载

**说明**: 利用 Higress 的 Wasm (WebAssembly) 插件生态，可以在不重启网关的情况下动态加载和更新业务逻辑（如鉴权、限流、请求修改）。这比传统的 Lua 脚本性能更好，且安全性更高（沙箱隔离）。

**实施步骤**:
1. 访问 Higress 官方插件市场，预置常用的鉴权、Key Rate Limiting 等插件。
2. 编写自定义 Wasm 插件（支持 C++, Go, AssemblyScript 等语言），并构建为 `.wasm` 文件。
3. 通过 Higress 控制台或 `WasmPlugin` CRD 将插件挂载到特定的网关路由或全局作用域。

**注意事项**: Wasm 插件运行在沙箱中，虽然隔离性好，但频繁的内存分配或复杂计算仍会增加延迟，需控制插件复杂度。

---

### 实践 4：服务注册中心的平滑对接与迁移

**说明**: Higress 原生支持 Nacos、ZooKeeper、Consul、DNS 以及 K8s Service。在微服务迁移场景下，Higress 能够同时从多个注册中心获取服务列表，实现从传统架构向云原生架构的平滑过渡。

**实施步骤**:
1. 在 Higress 全局配置中添加源服务注册中心（如 Nacos）的地址和认证信息。
2. 配置服务来源（ServiceSource），将外部注册中心的服务映射到 Higress 的服务来源中。
3. 在路由配置中直接引用注册中心的服务名，Higress 会自动进行服务发现和健康检查。

**注意事项**: 确保网络连通性，Higress 所在 Pod 需能直接访问注册中心的 Server 端口；注意不同注册中心之间的服务名冲突问题。

---

### 实践 5：全链路安全防护与精细化管理

**说明**: 依托 Higress 内置的高性能防护能力，结合 OIDC 认证和插件市场，构建从流量入口到微服务的安全防线。支持 IP 黑白名单、并发限流以及 JWT 验证，保障后端服务稳定性。

**实施步骤**:
1. 配置 `Ingress` 或 `Gateway` 资源，开启 HTTPS 并配置证书和 TLS 协议版本。
2. 启用 `key-rate-limit` 插件，针对特定 API 或客户端 IP 设置精确的 QPS 限制。
3. 集成 `jwt-auth` 插件或 OIDC 认证，实现统一的身份验证和透传。

**注意事项**: 限流配置应根据后端服务的实际承载能力进行压测后设定，防止网关限流阈值远大于后端承载阈值导致雪崩。

---

### 实践 6：可观测性与金丝雀发布

**说明**: Higress 深度集成了 Prometheus、SkyWalking 和 OpenTelemetry。利用 Higress 的路由权重管理功能，可以轻松实现蓝绿发布和金丝雀发布，配合监控指标实现精细化流量治理。

**实施步骤**:
1. 开启 Prometheus Metrics 采集端口（默认 15020），配置 ServiceMonitor �

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 绑定与隔离

**说明**: Higress 基于 Envoy 构建，其高性能严重依赖多线程上下文切换的效率。在 Kubernetes 宿主机上，若 Higress 的 Pod 与其他高负载服务（如数据库或 Java 应用）共享 CPU 核心，会导致频繁的上下文切换和 L1/L2 缓存失效，显著降低网络吞吐量。

**实施方法**:
1. **CPU 限制**: 确保将 Higress 网关的 CPU `limits` 设置为整数（如 4C, 6C），避免小数导致的时间片争抢。
2. **Guaranteed QoS**: 配置 `requests` 等于 `limits`，使 Pod 进入 Guaranteed QoS 状态。
3. **独占绑定**: 在 Pod YAML 中添加 `resources.limits.cpu` 并配合 Kubernetes CPU Manager 策略（设置为 `static`），实现物理核心独占。

**预期效果**: 在高并发场景下，可减少约 15%-30% 的长尾延迟，P99 延迟显著降低。

---

### 优化 2：配置连接池与 Keep-Alive 优化

**说明**: 默认的 HTTP 连接管理策略可能导致频繁建立 TCP 连接（三次握手开销大）或后端服务连接数过多。通过精细化管理上游和下游的连接池，可以复用连接，降低网络握手开销。

**实施方法**:
1. **上游连接池**: 在 Higress 路由配置中，针对特定服务调整 `maxRequestsPerConnection`。对于高吞吐内部服务，该值可设为 10-100（复用连接发送多个请求）；对于长尾服务，保持为 1。
2. **Keep-Alive**: 确保与后端服务的 Keep-Alive 探针间隔小于后端的超时时间，防止连接被误杀。
3. **HTTP/2**: 如果后端支持，优先启用 HTTP/2 协议，利用多路复用减少连接数。

**预期效果**: 后端服务的连接数可降低 50% 以上，同时提升请求响应速度 10%-20%。

---

### 优化 3：启用 WASM 插件的缓存与预编译

**说明**: Higress 支持 WASM 插件扩展功能。WASM 默认可能采用即时编译或解释执行，且每次加载可能涉及网络传输代码。未优化的 WASM 加载会显著增加冷启动延迟或单个请求的首包延迟。

**实施方法**:
1. **本地缓存**: 确保 Higress 配置了 WASM 代码的本地缓存策略，避免每次请求都从控制平面或 OCI 仓库拉取代码。
2. **AOT 编译**: 尽可能使用预编译的 WASM 二进制文件，利用 Higress 对 WASM 的优化特性，减少运行时编译开销。
3. **插件精简**: 移除 WASM 插件中非必要的日志打印和复杂逻辑运算，减少 CPU 指令数。

**预期效果**: WASM 插件执行延迟可降低 20%-50ms，对于鉴权等高频插件效果明显。

---

### 优化 4：优化日志采样与输出级别

**说明**: 在高流量（QPS > 10k）场景下，全量日志打印会带来巨大的磁盘 I/O 压力和 CPU 序列化开销，甚至阻塞网络处理线程。

**实施方法**:
1. **访问日志采样**: 在 Higress 全局配置中启用 `logSampler`，例如设置为 10%（仅记录 10% 的流量日志）。
2. **异步输出**: 确保日志输出配置为异步模式（默认通常开启，但需检查配置），避免阻塞主线程。
3. **字段裁剪**: 自定义日志格式，移除不必要且体积大的字段（如完整的 Request Body、全量的 Headers），仅保留 Trace ID、URL、状态码和耗时。

**预期效果**: 在高负载下可释放 5%-10% 的 CPU 资源，并显著降低磁盘写入压力。

---

### 优化 5：启用 DNS 缓

---
## 学习要点

- 基于提供的 GitHub 趋势来源信息（Alibaba/Higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接云原生基础设施。
- 该项目将高流量场景下的最佳实践进行了产品化，提供企业级的流量管理与安全防护能力。
- 它支持将传统的 Nginx Ingress 配置直接通过控制台进行导入和迁移，降低了迁移成本。
- Higress 提供了强大的 WAF（Web 应用防火墙）插件市场，允许用户通过插件灵活扩展网关功能。
- 该架构设计旨在解决微服务及 Serverless 场景下的流量治理难题，兼具高性能与易用性。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的核心概念：了解什么是 Higress，它基于 Envoy 和 Istio，以及它在 API 网关和云原生流量管理中的定位。
- 基本架构：理解 Higress 的控制面和数据面分离架构，以及与 K8s Ingress 的区别。
- 快速上手：学习如何通过 Docker 或 Kubernetes (Helm) 部署 Higress。
- 控制台操作：熟悉 Higress 的控制台界面，进行简单的域名路由配置（如将 /path 路由到后端服务）。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (入门与快速开始部分)
- Higress GitHub 仓库 README
- 官方提供的 Docker 部署示例

**学习建议**:
建议先阅读官方文档了解背景，然后直接在本地或测试环境使用 Docker 部署一个 Higress 实例。通过控制台配置一个简单的路由规则，通过浏览器访问验证流量是否通过网关，建立感性认识。

---

### 阶段 2：核心功能与配置

**学习内容**:
- 路由与流量管理：深入学习 HTTP 路由、重定向、重写、流量镜像（Traffic Mirroring）和灰度发布（金丝雀发布）。
- 插件市场与插件开发：了解 Higress 的插件机制，学习如何使用官方预置插件（如限流、认证、Key Rate Limiting）。
- 服务来源：学习如何配置 Nacos、Consul、固定地址（DNS/IP）以及 K8s Service 作为服务来源。
- 安全与鉴权：配置 Basic Auth、JWT 认证以及 CORS 跨域设置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方文档 - 插件市场文档
- Higress 官方示例库

**学习建议**:
此阶段重点在于配置练习。尝试模拟一个真实场景，例如配置一个带有鉴权的 API 服务，并开启限流插件。尝试配置基于 Header 的灰度发布策略，观察流量分配是否符合预期。

---

### 阶段 3：云原生与生产实践

**学习内容**:
- Kubernetes 集成：学习如何在 K8s 集群中通过 Ingress 或 Gateway API 资源配置 Higress。
- 可观测性：学习 Higress 的日志、指标（Metrics）和链路追踪集成，配置 Prometheus 和 Grafana 监控大盘。
- 高可用部署：理解 Higress 的高可用架构，学习网关的热更新与配置回滚机制。
- WAF 防护：了解如何配置 WAF 插件以防范 SQL 注入、XSS 等常见攻击。

**学习时间**: 3-4周

**学习资源**:
- Higgress GitHub Discussions (生产实践相关讨论)
- Higress 官方文档 - 观测性与部署指南
- Envoy 官方文档 (用于深入理解数据面原理)

**学习建议**:
在 Kubernetes 环境中进行部署练习。重点关注配置的生效速度和资源消耗。尝试对接 Prometheus 查看监控数据，模拟高并发场景测试网关的吞吐量及限流效果。

---

### 阶段 4：深度定制与源码剖析

**学习内容**:
- Wasm 插件开发：深入学习使用 Go 或 C++ 开发 Wasm (WebAssembly) 插件，实现自定义的业务逻辑处理。
- Lua 脚本支持：学习如何编写 Lua 脚本来扩展网关功能（如果当前版本支持）。
- 性能调优：深入理解 Envoy 配置调优，学习如何针对长连接、连接池等参数进行优化。
- 源码架构：阅读 Higress 控制面源码，理解配置如何从控制面下发到数据面。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub Source Code
- Higress 官方文档 - 自定义开发指南
- WebAssembly on Envoy 相关教程

**学习建议**:
如果你有特定的业务逻辑无法通过现有插件满足，可以尝试编写一个自定义 Wasm 插件。阅读源码时，建议从控制面启动流程和配置同步机制入手，理解其与 Istio 的异同。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里巴巴内部多年的电商业务沉淀和 Envoy 内核构建的。Higress 旨在提供高性能、高可用的流量管理能力，支持 Kubernetes 和微服务架构。它源自阿里巴巴对 API 网关的极致需求，并作为云原生技术栈的一部分，捐赠给了开源社区（通常与 CNCF 生态紧密相关）。简单来说，它是阿里通用的 API 网关技术对外开源的版本。

---



### 2: Higress 与 Nginx、Istio 或 APISIX 相比有什么区别？

2: Higress 与 Nginx、Istio 或 APISIX 相比有什么区别？

**A**: 
*   **与 Nginx 相比**：Higress 原生支持服务发现和 Kubernetes Ingress，配置更加动态化，不需要像 Nginx 那样频繁 reload 配置文件即可生效。
*   **与 Istio 相比**：Higress 专注于**南北向流量**（入口流量）管理，虽然也基于 Envoy，但它提供了更符合传统网关使用习惯的控制台和配置方式，比 Istio 的 Ingress Gateway 更易于运维和上手，同时集成了更多网关级别的插件（如认证、限流、WAF）。
*   **与 APISIX 相比**：两者都是高性能网关，但 Higress 深度集成了阿里云的商业产品插件（如 AI 服务问答），并且对 Envoy 的原生能力利用更为彻底，架构上更倾向于云原生环境下的标准化部署。

---



### 3: Higress 支持 Wasm（WebAssembly）插件吗？如何扩展功能？

3: Higress 支持 Wasm（WebAssembly）插件吗？如何扩展功能？

**A**: 是的，对 Wasm 的支持是 Higress 的核心特性之一。Higress 允许用户使用 C++、Go、Rust 或 AssemblyScript 等语言编写 Wasm 插件。这意味着用户可以在不修改网关核心代码或不需要重新编译网关二进制文件的情况下，动态地扩展网关的功能（例如自定义鉴权、流量染色、请求修改等）。这种机制极大地提高了网关的灵活性和扩展性，同时保持了与 Envoy 内核的高性能交互。

---



### 4: Higress 是否兼容 Kubernetes Ingress 和 Nginx Ingress 注解？

4: Higress 是否兼容 Kubernetes Ingress 和 Nginx Ingress 注解？

**A**: 是的，Higress 高度兼容 Kubernetes Ingress API 标准。它可以作为 Kubernetes 集群的 Ingress Controller 接管流量。此外，为了降低用户的迁移门槛，Higress 还兼容部分常用的 Nginx Ingress 注解。这使得用户从 Nginx Ingress 迁移到 Higress 时，配置文件的改造成本大大降低。

---



### 5: Higress 如何处理 AI 和大模型（LLM）相关的流量？

5: Higress 如何处理 AI 和大模型（LLM）相关的流量？

**A**: 这是 Higress 近期的一个热门特性。Higress 提供了专门针对 AI 服务的插件和路由能力，可以作为大模型（LLM）的统一网关。它支持对请求进行参数校验、Token 计费、结果缓存以及基于内容的路由。通过 Higress，企业可以更方便地将内部微服务与外部 AI 服务（如 OpenAI 或通义千问等）进行整合，统一管理 API 调用和鉴权。

---



### 6: Higress 的性能表现如何？是否支持高并发？

6: Higress 的性能表现如何？是否支持高并发？

**A**: Higress 基于 Envoy 构建，Envoy 本身就是业界公认的高性能 L7 代理。得益于 Envoy 的异步非阻塞架构和 C++ 的高效实现，Higress 能够处理极高的并发流量和吞吐量，延迟极低。阿里巴巴内部的双十一大促场景也验证了其底层技术栈的稳定性。在标准硬件下，Higress 的性能表现通常优于基于 OpenResty 或 Java 的网关实现。

---



### 7: 如何快速上手或部署 Higress？

7: 如何快速上手或部署 Higress？

**A**: 最快的上手方式是使用 Docker 或 Kubernetes 进行部署。
1.  **Docker 方式**：可以直接使用 Higress 提供的 Docker 镜像运行，适合本地快速测试。
2.  **Kubernetes 方式**：通过 Helm Chart 或 kubectl 应用 YAML 文件将其部署在 K8s 集群中。
部署成功后，Higress 提供了一个内置的**控制台**，用户可以通过 Web UI 直接配置路由、服务来源和插件，无需手动编写复杂的配置文件，大大降低了使用门槛。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的快速上手特性，尝试部署一个简单的 HTTP 服务，并配置 Higress 作为网关将其暴露。如何验证流量是否正确通过 Higress 转发？

### 提示**: 可参考官方文档的“快速开始”部分，重点检查路由配置和目标服务的健康状态。

### 

---
## 实践建议

以下是基于 Higress（阿里云开源的 AI 原生 API 网关）的 6 条实践建议，侧重于生产环境落地与 AI 流量治理：

### 1. 利用 AI 代理插件进行协议转换而非直接透传
Higress 的核心价值在于将 OpenAI 协议转换为标准 HTTP/gRPC 协议。
*   **实践建议**：不要仅仅将 Higress 作为简单的 TCP 透传。在路由配置中启用 `ai-proxy` 插件，将后端兼容 OpenAI 格式的模型服务（如 DeepSeek、Qwen 等）统一映射为标准的 API 接口。
*   **最佳实践**：通过配置 `service` 字段指向后端模型服务，并在插件中指定 `model` 指令，这样可以在网关层统一屏蔽不同模型厂商的 API 差异，便于后续切换供应商而无需修改客户端代码。

### 2. 配置基于 Token 的精细化流控
AI 服务的成本主要与 Token 消耗量成正比，传统的 QPS（每秒请求数）限流无法准确控制成本。
*   **实践建议**：在 `ai-proxy` 插件配置中，启用 `context` 下的 `rpm`（每分钟请求数）或 `tpm`（每分钟 Token 数）限制。
*   **常见陷阱**：如果只配置了全局 QPS 限流，可能会出现少量用户发送超长 Prompt 耗尽预算，导致高频但短请求的正常用户被限流的情况。务必针对 API Key 或用户 ID 设置 TPM 限制。

### 3. 实施语义缓存以降低推理成本和延迟
对于常见的问答场景，重复调用大模型会产生不必要的费用。
*   **实践建议**：开启 Higress 的缓存插件（或利用 `ai-proxy` 的缓存能力），将向量相似度匹配与 HTTP 缓存结合。
*   **具体操作**：配置缓存策略时，设定 `semantic_cache` 为 true，并设置合理的相似度阈值（如 0.85）。这意味着当用户的问题语义相似度达到 85% 以上时，网关将直接返回缓存的答案，而不再请求后端 LLM。

### 4. 敏感信息脱敏与提示词注入防护
AI 网关是数据安全的最后一道防线，防止用户将敏感数据发送给公网模型至关重要。
*   **实践建议**：在 `ai-proxy` 插件之前，串联一个 `prompt-decorator` 或自定义 WAF 插件。
*   **具体操作**：配置正则表达式或关键词列表，拦截包含身份证号、密码等特征的请求。同时，利用插件在系统层面追加“提示词”，强制模型拒绝回答违反安全策略的问题，防止 Prompt 注入攻击。

### 5. 构建兜底模型机制以应对限流
生产环境中，单一模型服务商可能会出现 API 报错或限流（HTTP 429）。
*   **实践建议**：不要将路由死绑在某一个模型服务商上。利用 Higress 的服务发现或多服务配置能力。
*   **最佳实践**：配置Fallback（降级）策略。例如，主路由指向通义千问，当检测到错误码 429 或 500 超过重试次数时，利用 Higress 的脚本插件动态将请求转发至备用的模型服务（如 Ollama 本地部署的模型或 Azure OpenAI），确保业务连续性。

### 6. 区分流式与非流式响应的超时策略
大模型推理通常耗时较长，且流式响应的首字延迟（TTFT）与生成速度不同。
*   **实践建议**：在路由配置中，针对涉及 AI 的路径，显式调大 `upstream.response_timeout` 参数（例如设置为 60s 或 120s）。
*   **常见陷阱**：如果使用 Nginx 或默认网关配置（通常超时为 60s），在处理长文本生成时极易导致网关层提前断开连接，而客户端却收到了部分 JSON 报错。务必确保网关的超时时间大于模型的最大生成时间。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [Higress](/tags/higress/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260207-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260214-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*