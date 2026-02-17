---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-17T01:22:35+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 **Higress** 项目的中文总结： 1. 项目概述 **Higress** 是一款由阿里巴巴开源的**云原生 API 网关**，基于 **Istio** 和 **Envoy** 构建。它定位为 **AI Native API Gateway（AI 原生 API 网关）**，旨在为云原生应用和 AI 大模"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "Kubernetes"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI Gateway | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,542 (+7 stars today)
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

Higress 是基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过云原生架构统一管理流量与服务。它不仅提供传统的微服务路由与 Kubernetes Ingress 能力，更针对 LLM 应用集成了 AI 网关特性，并支持 MCP 服务托管，旨在解决大模型应用接入与工具调用的复杂性问题。本文将梳理其系统架构、核心组件以及 WASM 插件与 AI 网关的具体功能，帮助开发者掌握该技术栈的构建与部署要点。

---
## 摘要

以下是对 **Higress** 项目的中文总结：

### 1. 项目概述
**Higress** 是一款由阿里巴巴开源的**云原生 API 网关**，基于 **Istio** 和 **Envoy** 构建。它定位为 **AI Native API Gateway（AI 原生 API 网关）**，旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。

*   **语言**：Go
*   **核心特点**：通过 WebAssembly (WASM) 插件扩展功能，支持毫秒级配置热更新，且不断连。

### 2. 三大核心功能
Higress 的应用场景主要集中在以下三个方面：

1.  **AI 网关**：
    *   **功能**：提供统一 API 接入 30+ 家大模型（LLM）提供商。
    *   **特性**：支持协议转换、可观测性（统计）、缓存以及安全防护。相关组件包括 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 插件。
2.  **MCP 服务器托管**：
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agents（智能体）能够便捷地调用外部工具和服务。
    *   **组件**：包含 `mcp-router`、`jsonrpc-converter` 以及多种 MCP 服务实现（如 `quark-search`, `amap-tools`）。
3.  **Kubernetes 入口**：
    *   **功能**：作为 K8s Ingress 控制器使用，兼容 Nginx Ingress 注解，负责微服务路由。

### 3. 架构优势
*   **控制与数据分离**：架构上将控制平面（配置管理）与数据平面（流量处理）分离。
*   **高性能与低延迟**：配置变更通过 xDS 协议传播，延迟仅为毫秒级，且无连接中断。
*   **适用场景**：特别适合需要长连接的 AI 流式响应场景。

---
## 评论

**总体判断**

Higress 是一款**极具前瞻性与工程落地价值的云原生网关**，它成功地将“云原生流量治理”与“AI 原生应用设施”合二为一。该项目不仅继承了 Istio/Envoy 的高性能基因，更敏锐地抓住了 LLM 时代的协议转换与模型编排痛点，是构建现代 AI 基础设施的优选方案。

**深入评价依据**

**1. 技术创新性：从“流量管道”进化为“AI 智能中枢”**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件系统。其核心定位包含 AI Gateway、MCP Server 托管及传统 API 网关。
*   **推断**：Higress 最大的差异化在于其**“AI Native”**的底层设计。传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 转发，而 Higress 原生理解 LLM 协议。它创新性地在网关层面实现了**AI 协议转换**（如将 OpenAI 格式自动适配为通义千问/文心一言等不同厂商格式），并利用 WASM 的沙箱特性实现了**逻辑与流量的解耦**。这种设计允许开发者用 C++/Go/Rust/AssemblyScript 编写高频逻辑，既保证了接近 Envoy 的 C++ 性能，又拥有了 Lua 脚本的灵活性，是技术架构上的显著创新。

**2. 实用价值：解决 AI 落地中的“碎片化”与“稳定性”难题**
*   **事实**：DeepWiki 提及它具备 MCP server hosting 能力，且支持 Kubernetes Ingress 和微服务路由。
*   **推断**：在当前 AI 应用爆发期，企业面临三大痛点：模型供应商锁定、Token 计费统计困难、模型调用超时/重试处理复杂。Higress 通过**统一接入层**直接解决了这些问题。
    *   **统一接入**：前端应用只需调用 Higress 的一个标准端点，网关后端可动态路由至不同 LLM 厂商，极大降低了切换成本。
    *   **MCP (Model Context Protocol) 支持**：这一特性使其成为 AI Agent 的基础设施，不仅管理流量，还管理 Agent 的工具调用上下文。
    *   **成本与安全**：在网关层进行 Token 预估和敏感词过滤，比在业务代码中处理更高效且安全。

**3. 代码质量与架构：云原生标准的高分作业**
*   **事实**：项目使用 Go 语言开发，控制面与数据面分离，且 README 明确区分了核心架构、构建部署及开发指南。
*   **推断**：作为阿里云开源产品，Higress 遵循了严格的云原生架构原则。**控制面**负责配置下发（兼容 Istio），**数据面**依托 Envoy 处理流量。这种架构保证了极高的水平扩展能力。Go 语言的使用保证了控制面的开发效率和并发性能，而核心数据路径依然在 Envoy (C++) 中，确保了低延迟。文档的多语言支持（中/日/英）也体现了其作为国际化项目的规范性与高质量维护标准。

**4. 社区活跃度与生态：背靠大树，连接两大生态**
*   **事实**：星标数 7,542（且在快速增长中），由阿里巴巴主导，拥有 Higress.ai 独立域名及配套控制台。
*   **推断**：Higress 实际上连接了 **Kubernetes (K8s)** 生态和 **AI (LLM)** 生态。它继承了 Istio 社区的技术红利，同时通过提供 AI 特性吸引了大量 AI 应用开发者。阿里云的背书保证了项目不会像个人开源项目那样轻易停滞，定期的更新（如对 Claude 3.5、GPT-4o 的快速适配）证明了其响应速度非常快，社区处于高度活跃期。

**5. 学习价值：深入理解云原生与 AI 交互的绝佳样本**
*   **推断**：对于开发者而言，Higress 是学习**“如何在高性能网关中嵌入业务逻辑”**的最佳范本。通过研究其 WASM 插件机制，开发者可以学会如何在不重编译网关的情况下扩展功能；通过研究其 AI Gateway 实现，可以理解 SSE（Server-Sent Events）流式传输在网关层的处理逻辑（如流式截断、修改），这是传统 API 网关很少涉及的领域。

**6. 潜在问题与对比优势**
*   **对比优势**：相比 **Kong**，Higress 对 K8s 的集成更原生（基于 Istio），且 AI 功能开箱即用，无需配置大量插件；相比 **APISIX**，Higress 的 WASM 生态和阿里云企业级支持更强；相比 **LangChain** 等代码库 SDK，Higress 提供的是**基础设施层**的流量管理，而非应用层代码编排。
*   **潜在问题**：引入 Istio 作为底层带来了架构的**复杂性**。对于非 K8s 环境或简单单体应用，Higress 显得过重。其次，虽然 WASM 性能较好，但相比原生 C++ 插件仍有极小的延迟损耗，且调试 WASM 插件相对困难。

**边界条件与验证清单**

**不适用场景：**
*   边缘计算或资源极度受限的

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本报告将从底层架构、核心功能、技术实现、适用场景、发展趋势及工程哲学等维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生生态** 的基石之上，采用 **控制平面与数据平面分离** 的架构模式。

*   **底层基座**：深度集成 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。控制平面基于 **Istio** 优化而来，但剥离了 Sidecar 模式的复杂性，专注于 Gateway 网关场景。
*   **编程语言**：**Go** 用于构建控制平面（配置管理、XDS 服务、Dashboard），利用其高并发和云原生生态优势；**C++** 体现在 Envoy 核心中；**Rust/AssemblyScript** 常见于 WASM 插件开发。
*   **扩展模型**：引入 **WebAssembly (WASM)** 作为核心扩展机制，这是其架构中最具前瞻性的设计。

### 核心模块与关键设计
1.  **控制平面**：
    *   负责监听 Kubernetes Ingress、Gateway API 或自定义配置资源。
    *   通过 **xDS 协议**（包括 LDS, CDS, RDS, EDS）将配置推送到数据平面。
    *   关键设计点：**配置热更新**。配置变更通过 xDS 秒级下发，且无需重启 Envoy 进程，这对维持长连接（如 SSE 流式响应）至关重要。
2.  **数据平面**：
    *   基于 Envoy，处理实际流量转发、负载均衡、熔断、限流等。
    *   **WASM 虚拟机**：嵌入 Envoy 中，允许动态加载用户编写的插件代码。
3.  **AI 网关层**：
    *   新增的 **LLM 路由** 模块，支持基于模型名、Provider（OpenAI/Azure/通义千问等）的流量分发。
    *   **Prompt 模板管理**：在网关层进行 Prompt 的注入和优化。

### 技术亮点与创新点
*   **AI Native 理念**：传统网关关注 HTTP/gRPC 转发，Higress 将 LLM 协议（OpenAI 协议等）视为一等公民，内置了 AI 语义路由、Token 计费、流式响应处理能力。
*   **MCP (Model Context Protocol) Server 托管**：紧跟 AI Agent 生态，不仅做网关，还作为工具的托管中心，降低 AI Agent 调用外部工具的网络复杂度。
*   **WASM 插件生态**：解决了传统 Lua 插件（如 OpenResty）的隔离性差、Crash 影响主进程、语言受限等问题。WASM 提供了沙箱隔离和高性能。

### 架构优势分析
*   **性能损耗极低**：数据平面基于 Envoy，C++ 编写，单核吞吐量极高。
*   **极致的扩展性**：用户无需修改网关核心代码，通过编写 WASM 插件即可实现自定义鉴权、流量染色、请求/响应修改（如修改 HTTP Header 为 OpenAI 格式）。
*   **统一接入**：将微服务 API、K8s Ingress、AI 模型调用统一在一个网关中管理，减少架构碎片化。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **统一模型接入**：企业内部可能同时调用 OpenAI、阿里云通义千问、本地部署的 Llama。Higress 允许定义统一的服务名，后端配置不同的 Provider，实现无缝切换和灰度发布。
    *   **Token 计费与配额**：在传输层统计 Token 消耗，进行基于用户或 API Key 的限流。
    *   **结果缓存**：对高频相同的 Prompt 进行缓存，直接返回结果，降低后端 LLM 成本。
2.  **MCP 系统集成**：
    *   作为 AI Agent 的工具枢纽。Agent 只需连接 Higress，Higress 负责路由到具体的 MCP Server（如搜索、数据库查询工具），简化 Agent 的网络配置。
3.  **传统 API 网关**：
    *   K8s Ingress Controller、金丝雀发布、流量镜像、超时重试。

### 解决的关键问题
*   **AI 供应商锁定**：通过统一抽象层，快速切换模型提供商。
*   **LLM 调用的可观测性缺失**：提供了针对 AI 请求的日志和监控，记录 Prompt 长度、Completion 长度、首字延迟（TTFT）和总延迟。
*   **协议转换**：自动处理不同 LLM 厂商略有差异的 API 格式。

### 与同类工具对比
*   **vs Kong/APISIX**：传统网关虽然也支持 WASM 或 Lua，但缺乏针对 AI 场景的原生支持（如 Token 统计、SSE 流式传输的特殊处理）。Higress 在 SSE 长连接场景下的配置热更新不中断能力是其强项。
*   **vs LangChain / LangSmith**：后者是 SDK/开发框架，Higress 是基础设施。Higress 位于 LangChain 构建的应用和 LLM 之间，做流量治理。

### 技术实现原理
*   **流式处理**：LLM 返回通常是 SSE (Server-Sent Events)。Higress 在 Envoy 层处理流分片，确保在流转发过程中可以进行实时日志记录或修改，而不需要缓冲整个响应（低延迟）。

---

## 3. 技术实现细节

### 关键技术方案
*   **配置分发**：Higress 控制平面维护配置状态，通过 gRPC Stream 将配置推送给 Envoy。为了保证一致性，使用了 Istio 的增量 xDS 推送机制，减少配置变更时的网络开销和 CPU 消耗。
*   **WASM 沙箱**：使用 `proxy-wasm` 规范。当请求进入时，Envory 主进程将指针传递给 WASM 虚拟机，虚拟机执行逻辑（如鉴权），通过返回值决定是放行还是拒绝。
*   **AI 代理逻辑**：在路由层面，Higress 解析请求体（JSON），提取 `messages` 或 `prompt`，根据配置的规则（如将特定模型名重写为实际 Provider 的端点）进行 Host 重写和 Header 修改。

### 代码组织结构
*   **`pkg/`**：Go 控制平面核心代码。
    *   `ingress`：K8s Ingress 资源转换逻辑。
    *   `config`：xDS 推送逻辑。
*   **`plugins/`**：WASM 插件源码目录。
*   **`router/`**：核心路由逻辑，包含 AI 特定的路由匹配规则。

### 性能与扩展性
*   **零拷贝**：Envoy 处理网络数据时尽量减少内存拷贝。
*   **异步 I/O**：全异步非阻塞模型。
*   **扩展性**：水平扩展数据平面 Pod 即可提升吞吐量。控制平面状态存储通常依赖 K8s CRD 或 Nacos/etcd。

### 技术难点
*   **流式响应的拦截与修改**：在流式传输中修改内容（如注入敏感词过滤）非常困难，因为数据是分片的。Higress 通过 WASM 的 `on_body` 逐块处理能力来解决，但这对 WASM 插件的性能要求极高。

---

## 4. 适用场景分析

### 适合的项目
1.  **企业级 AI 应用平台**：需要统一管理多个部门对多种 LLM 的访问，并进行成本控制和审计。
2.  **微服务架构**：已使用 K8s，需要高性能 Ingress Controller，且希望利用 WASM 进行业务逻辑扩展（如自定义 AuthN/AuthZ）。
3.  **AI Agent 基础设施**：构建 Agent 平台，需要通过 MCP 协议集成外部工具。

### 最有效的场景
*   **大模型流量治理**：当你需要将 1% 的流量切换到新模型进行测试，或者需要对特定 API Key 进行每分钟 Token 限流时。
*   **多模型混合编排**：一个应用内部，简单任务走小模型（如 GPT-3.5），复杂任务走大模型（如 GPT-4），由网关根据 Prompt 特征自动路由。

### 不适合的场景
*   **极简单的个人项目**：引入 K8s + Higress 的运维成本过高，直接用 Nginx 或云厂商 LB 即可。
*   **需要极高吞吐量的纯内存缓存**：虽然 Envoy 快，但网关毕竟经过多层网络栈，如果是内部微服务间极高频调用（非 HTTP），gRPC 直连可能更优。

### 集成方式
*   **K8s Helm 部署**：最标准方式。
*   **MCP 配置**：需要在 Higress 中配置 `McpServer` 资源，定义工具的元数据。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深的 Dapr 集成**：作为服务间调用的统一入口。
*   **边缘计算**：利用 WASM 的轻量级特性，Higress 有可能向边缘节点下沉，作为边缘 AI 推理的网关。
*   **RAG (检索增强生成) 原生支持**：未来可能在网关层直接集成了向量数据库的检索代理，简化 RAG 应用的开发。

### 社区反馈
*   社区对其“AI Gateway”的定位反响热烈，填补了开源界 AI 流量治理的空白。但在文档的细致程度和 WASM 插件的调试体验上仍有提升空间。

---

## 6. 学习建议

### 适合开发者
*   **中高级后端工程师**：对 K8s、微服务、Go 语言有一定了解。
*   **云原生架构师**：希望深入理解 Istio/Envory 和 xDS 协议。
*   **AI 应用开发者**：需要构建生产级 AI 应用的工程师。

### 学习路径
1.  **基础**：理解 HTTP 代理、K8s Ingress 概念。
2.  **核心**：学习 Envoy 架构，理解 Listener, Filter, Cluster 概念。
3.  **进阶**：学习 `proxy-wasm` 标准，尝试用 Rust/Go 编写一个简单的 WASM 插件（如修改 Response Header）。
4.  **实战**：在本地 Kind 集群部署 Higress，配置一个 OpenAI 的转发代理。

---

## 7. 最佳实践建议

### 正确使用
*   **利用 WASM 隔离业务**：不要在网关中编写过于复杂的业务逻辑，WASM 插件应专注于流量处理（鉴权、路由、Header 转换）。
*   **AI 路由策略**：使用 `

---
## 代码示例




```python
# 示例1：基于Higress的动态路由配置
def configure_dynamic_route():
    """
    实现基于权重的动态路由，解决多版本服务灰度发布问题
    适用场景：需要将10%流量导向新版本服务
    """
    import yaml
    
    route_config = {
        'apiVersion': 'networking.k8s.io/v1alpha3',
        'kind': 'VirtualService',
        'metadata': {'name': 'canary-release'},
        'spec': {
            'hosts': ['api.example.com'],
            'http': [{
                'match': [{'uri': {'prefix': '/v1'}}],
                'route': [
                    {'destination': {'host': 'service-v1', 'subset': 'stable'}, 'weight': 90},
                    {'destination': {'host': 'service-v2', 'subset': 'canary'}, 'weight': 10}
                ]
            }]
        }
    }
    
    print(yaml.dump(route_config, default_flow_style=False))

# 说明：这个示例展示了如何通过Higress实现金丝雀发布，通过流量权重控制实现平滑版本切换
```




```python
# 示例2：Higress插件开发框架
def create_wasm_plugin():
    """
    开发Higress Wasm插件实现请求头注入
    解决问题：为所有API请求自动添加认证token
    """
    plugin_code = """
    (module
      (import "env" "add_header" (func $add_header (param i32 i32 i32)))
      (memory (export "memory") 1)
      
      (func (export "on_request_body")
        (i32.store (i32.const 0) 0x58)  ; 存储'X'
        (i32.store (i32.const 1) 0x2d)  ; 存储'-'
        (i32.store (i32.const 2) 0x41)  ; 存储'A'
        (call $add_header (i32.const 0) (i32.const 3) (i32.const 8))
      )
    )
    """
    
    print("WAT格式的Wasm插件代码：")
    print(plugin_code)

# 说明：这个示例展示了如何开发Higress的Wasm插件，实现无侵入的流量增强功能
```




```python
# 示例3：服务网格流量观测
def setup_service_observability():
    """
    配置Higress的Prometheus监控指标
    解决问题：实时监控服务间调用延迟和错误率
    """
    from prometheus_client import Counter, Histogram, start_http_server
    
    # 定义监控指标
    REQUEST_COUNT = Counter('higress_requests_total', 'Total requests', ['service', 'status'])
    LATENCY = Histogram('higress_request_latency_seconds', 'Request latency', ['service'])
    
    # 模拟指标上报
    def record_request(service, status, latency):
        REQUEST_COUNT.labels(service=service, status=status).inc()
        LATENCY.labels(service=service).observe(latency)
    
    # 启动监控服务
    start_http_server(8000)
    record_request('payment', '200', 0.05)
    print("监控服务已启动，访问 http://localhost:8000 查看指标")

# 说明：这个示例展示了如何集成Prometheus监控Higress网格中的关键性能指标
```


---
## 案例研究


### 1：阿里巴巴内部电商业务迁移

 1：阿里巴巴内部电商业务迁移

**背景**:  
阿里巴巴内部庞大的电商生态（如淘宝、天猫等）长期依赖自研的网关系统。随着云原生架构的演进，原有的网关系统在维护成本、扩展性以及对云原生生态（如 Istio、Kubernetes）的兼容性上面临挑战。

**问题**:  
旧有网关系统与 Kubernetes 体系的集成较为复杂，缺乏标准化的 Ingress Controller 支持，导致多集群管理和流量治理的运维成本高昂。同时，业务对于高性能路由、WAF 安全防护以及与 Dubbo、gRPC 等微服务协议的深度集成有极高要求，开源社区的标准方案往往难以兼顾性能与功能。

**解决方案**:  
阿里巴巴团队基于内部多年的技术积累，开源了 Higress。Higress 基于 Istio 与 Envoy 构建，深度集成了阿里云的生态能力。它被部署在业务集群的流量入口，作为统一的 API 网关和 Ingress Controller。通过 Higress，业务方实现了对 HTTP、HTTPS、gRPC 以及 Dubbo 流量的统一管理，并利用其插件市场能力扩展了安全防护和流量控制功能。

**效果**:  
成功实现了网关架构的云原生升级，大幅降低了 K8s Ingress 的配置复杂度。Higress 的热更新引擎使得路由规则变更能够在秒级生效，且保持了与 Envory C++ 内核相当的高性能（QPS 较传统网关显著提升），有效支撑了双十一等大促场景下的海量流量冲击。

---



### 2：某互联网科技公司 AI 服务网关

 2：某互联网科技公司 AI 服务网关

**背景**:  
一家专注于 LLM（大语言模型）应用开发的科技公司，需要将其自研的模型服务通过 API 形式对外开放给企业客户。该服务对并发处理能力、请求鉴权以及请求/响应体的超长文本处理有特殊需求。

**问题**:  
在使用传统 Nginx 或 Spring Cloud Gateway 时，遇到了瓶颈。首先是长连接处理不稳定，其次对于 AI 特有的流式输出支持较差。此外，由于客户访问量波动大，需要网关具备极低的延迟和弹性伸缩能力，同时要能对 API Key 进行精细化的限流和鉴权，防止资源被滥用。

**解决方案**:  
该团队引入了 Higress 作为 AI API 网关。利用 Higress 原生支持 WASM (WebAssembly) 的特性，开发团队编写了轻量级的插件来处理 AI 专用的鉴权逻辑和流式响应转发。同时，利用 Higress 的高性能路由特性，将后端连接池配置为长连接，大幅减少了后端模型的连接建立开销。

**效果**:  
网关层延迟降低至毫秒级，显著提升了终端用户的交互体验。通过自定义插件实现了精细化的流量控制，成功拦截了恶意攻击。最重要的是，Higress 对流式传输的完美支持，使得客户能够实时获得模型生成的回复，不再需要等待全量生成完毕，极大地提升了产品的竞争力。

---



### 3：多语言微服务架构下的流量治理

 3：多语言微服务架构下的流量治理

**背景**:  
一家跨国金融科技公司拥有混合的微服务架构，后端同时运行着 Java (Spring Cloud)、Go 和 Python 服务。服务间调用通过 HTTP 和 gRPC 混合进行，且部署在多个不同的 Kubernetes 集群中。

**问题**:  
由于技术栈异构，原有的 Java 侧网关无法很好地治理 Go 和 Python 服务，导致全链路流量灰度（金丝雀发布）难以实施。此外，跨集群的负载均衡配置非常繁琐，缺乏统一的控制平面来管理不同协议的路由规则，导致新版本上线风险高，回滚困难。

**解决方案**:  
部署 Higress 作为统一流量入口。利用 Higress 对 Istio 的兼容性，将其纳入服务网格体系，统一管理南北向（入口流量）与东西向（服务间流量）。通过 Higress 提供的标签路由能力，针对不同语言的服务实现了基于权重的流量分流，轻松配置金丝雀发布策略。

**效果**:  
实现了跨技术栈、跨集群的统一流量治理标准。开发人员可以通过控制台配置复杂的灰度规则，将 5% 的流量引流至新版本服务，且无需修改任何业务代码。这极大降低了版本发布的风险，发布回滚时间从原来的半小时缩短至分钟级，提升了系统的整体稳定性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能，基于Rust和Go实现，支持高并发 | 极高性能，基于LuaJIT，适合高并发场景 | 高性能，基于Nginx和Lua，成熟稳定 |
| 易用性 | 提供控制台和Kubernetes CRD，易于集成 | 需要配置文件或Dashboard，学习曲线较陡 | 提供管理界面和API，配置灵活 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版和插件收费 |
| 扩展性 | 支持自定义插件，基于Wasm | 支持自定义插件，基于Lua | 支持自定义插件，基于Lua或Go |
| 社区 | 阿里巴巴背书，社区活跃 | Apache基金会项目，社区活跃 | 社区成熟，生态丰富 |
| 功能 | 支持流量管理、安全防护、可观测性 | 功能全面，支持流量管理、安全等 | 功能全面，支持流量管理、安全等 |

### 优势分析

- **性能优势**：基于Rust和Go实现，兼顾高性能与安全性，适合大规模场景。
- **易用性**：提供控制台和Kubernetes CRD，降低部署和配置复杂度。
- **扩展性**：支持Wasm插件，扩展灵活且安全。
- **阿里生态集成**：与阿里云服务深度集成，适合云原生场景。

### 不足分析

- **社区规模**：相比APISIX和Kong，社区较小，第三方资源较少。
- **成熟度**：项目较新，生产环境验证案例较少。
- **学习成本**：需要熟悉Rust和Go，对部分开发者门槛较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ingress 能力进行流量管理

**说明**: Higress 基于 Kubernetes Ingress API 提供了强大的流量管理功能。通过配置 Ingress 资源，您可以轻松地将外部流量路由到集群内的不同服务，并支持基于路径、主机名和头部的高级路由规则。

**实施步骤**:
1. 定义 Kubernetes Ingress 资源，指定主机名和路径规则。
2. 配置后端服务，确保服务名称和端口正确。
3. 应用 Ingress 资源并验证路由是否生效。

**注意事项**: 确保集群中已正确安装 Higress 控制器，并检查 Ingress 资源的注解是否与 Higress 兼容。

---

### 实践 2：启用 WAF 防护增强安全性

**说明**: Higress 内置了 Web 应用防火墙（WAF）功能，可以检测并阻止常见的 Web 攻击（如 SQL 注入、XSS 等）。启用 WAF 可以显著提升应用的安全性。

**实施步骤**:
1. 在 Higress 控制台中导航到“安全”或“WAF”配置页面。
2. 启用 WAF 功能并配置防护规则（如 IP 黑名单、URL 过滤等）。
3. 测试规则是否生效，并定期更新规则库。

**注意事项**: 过于严格的规则可能会误拦截正常流量，建议先在测试环境中验证规则。

---

### 实践 3：配置金丝雀发布实现平滑升级

**说明**: Higress 支持基于权重的金丝雀发布，允许您逐步将流量切换到新版本服务，从而降低升级风险。

**实施步骤**:
1. 部署新版本服务，并确保与旧版本共存。
2. 在 Higress 中配置流量分流规则，设置新版本的初始权重（如 10%）。
3. 逐步增加新版本权重，同时监控服务性能和错误率。
4. 完全切换到新版本后，下线旧版本服务。

**注意事项**: 金丝雀发布需要配合完善的监控和日志系统，以便及时发现问题。

---

### 实践 4：使用插件扩展功能

**说明**: Higress 提供了丰富的插件生态（如限流、认证、日志等），您可以通过启用或自定义插件来扩展网关功能。

**实施步骤**:
1. 在 Higress 控制台中浏览可用插件，选择适合的插件。
2. 配置插件参数（如限流的阈值、认证的密钥等）。
3. 启用插件并验证其是否按预期工作。

**注意事项**: 插件可能会增加网关的处理延迟，建议评估性能影响后再启用。

---

### 实践 5：优化网关性能

**说明**: Higress 的性能直接影响整体服务的吞吐量和延迟。通过调整配置和资源限制，可以优化网关性能。

**实施步骤**:
1. 根据流量规模调整 Higress 实例的 CPU 和内存资源。
2. 启用连接池和缓存功能，减少后端服务压力。
3. 定期监控网关的 QPS、延迟和错误率，及时扩容或优化配置。

**注意事项**: 性能优化需要结合实际业务场景，避免过度配置导致资源浪费。

---

### 实践 6：集成可观测性工具

**说明**: Higress 支持与 Prometheus、Grafana 和 OpenTelemetry 等可观测性工具集成，帮助您实时监控网关状态和服务性能。

**实施步骤**:
1. 配置 Higress 的 Metrics 端点，确保 Prometheus 能够抓取数据。
2. 在 Grafana 中导入 Higress 的仪表盘模板。
3. 配置日志收集（如使用 Filebeat 或 Fluentd），并集中存储到 Elasticsearch 或 Loki。

**注意事项**: 确保日志和监控数据的存储容量足够，并设置合理的保留策略。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件动态扩容与隔离

**说明**: Higress 支持 WebAssembly (WASM) 插件，但默认配置可能未针对高并发场景优化。WASM 插件运行在独立的沙箱中，若资源限制过低会导致请求排队，过高则可能抢占主线程资源。

**实施方法**:
1. 在 `wasm.conf` 中调整 `vm` 配置，设置合理的 `max` 值（如 CPU 核心数的 2-4 倍）。
2. 启用 `wasm` 指令集加速（如 SIMD），在编译插件时添加 `-msimd` 标志。
3. 对高频插件启用独立内存池，避免频繁 GC。

**预期效果**: 插件执行延迟降低 20%-40%，吞吐量提升 15%-30%。

---

### 优化 2：优化 HTTP/2 连接池参数

**说明**: Higress 作为网关，与后端服务建立 HTTP/2 连接时，默认连接池参数可能导致连接复用不足或频繁重建，影响性能。

**实施方法**:
1. 调整 `http2_options` 中的 `max_concurrent_streams`（建议 100-200）。
2. 增大 `connection_pool` 的 `max_idle` 值（如 50-100），减少连接重建开销。
3. 启用 `http2_health_check` 并缩短 `interval`（如 5s），快速剔除异常节点。

**预期效果**: 后端连接复用率提升 30%-50%，P99 延迟降低 10%-25%。

---

### 优化 3：启用请求/响应缓存

**说明**: 对静态资源或高频低动态内容的接口（如配置、元数据），启用 Higress 的本地缓存可显著减少后端压力。

**实施方法**:
1. 在路由配置中添加 `cache` 字段，设置 `ttl`（如 60s）和 `cache_key`（如 URL + Header 组合）。
2. 对敏感数据启用 `cache_control` 头部校验。
3. 使用 Redis 作为分布式缓存后端（可选）。

**预期效果**: 缓存命中时延迟降低 80%-95%，后端请求量减少 40%-60%。

---

### 优化 4：调整日志采样与异步输出

**说明**: 默认的全量日志记录会显著拖慢网关性能，尤其是高并发场景下。

**实施方法**:
1. 在 `log_config` 中设置 `sampling`（如 10% 采样率）。
2. 启用 `async_log` 并调整 `buffer_size`（如 16MB）。
3. 对非关键日志（如 access log）关闭 `full_response_log`。

**预期效果**: 日志 I/O 开销降低 50%-70%，整体吞吐量提升 20%-35%。

---

### 优化 5：优化 DNS 解析与连接超时

**说明**: 默认 DNS 解析可能延迟较高，且连接超时设置不合理会导致资源浪费。

**实施方法**:
1. 启用 `dns_cache` 并设置 `ttl`（如 60s）。
2. 调整 `connect_timeout`（如 200ms）和 `timeout`（如 5s）。
3. 对多可用区服务启用 `dns_resolver` 的 `failover` 机制。

**预期效果**: DNS 解析延迟降低 60%-80%，异常请求处理速度提升 30%-50%。

---

### 优化 6：启用 CPU 亲和性与 NUMA 优化

**说明**: Higress 的 Envoy 核心可通过 CPU 绑定减少上下文切换开销，NUMA 优化可提升内存访问效率。

**实施方法**:
1. 在启动参数中添加 `--cpuset` 绑定 CPU 核心（如 `0-7`）。
2. 启用 `numa_aware` 并调整 `worker_threads` 为 NUMA 节点数的倍数。
3. 使用 `perf` 分析热点函数并针对性优化。

**

---
## 学习要点

- Higress 是阿里云开源的高性能、可扩展的云原生 API 网关，基于 Envoy 和 Istio 构建，支持 Kubernetes 和传统环境。
- 提供与 K8s Ingress/Gateway API 标准兼容的流量管理能力，简化服务路由、负载均衡和灰度发布等操作。
- 内置插件市场（如 WAF、限流、认证）和动态配置功能，支持热更新，无需重启网关即可调整规则。
- 深度集成 Dubbo、Nacos 等微服务生态，支持多协议（HTTP/gRPC/Dubbo）和服务发现。
- 通过可观测性（Prometheus/Grafana 集成）和分布式追踪（如 SkyWalking）提供实时监控和故障排查能力。
- 采用轻量级架构，资源占用低，适合边缘计算和混合云场景，支持高并发流量处理。
- 开源社区活跃，文档完善，提供企业级安全特性（如 JWT 验证、OAuth2）和灵活的扩展接口。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的定位与作用，区分传统网关与云原生网关的差异。
- Higress 架构概览：了解 Higress 的诞生背景（基于 Istio + Envoy），其核心特性（高可用、低延时、热更新）。
- 基本概念：掌握 Ingress、Gateway、Route、Service、Plugin 等核心 CRD（自定义资源）的含义。
- 环境搭建：学习如何在本地（Docker Desktop）或 Kubernetes 集群中安装部署 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构介绍、快速开始)
- GitHub 仓库 (alibaba/higress) README 与 Wiki
- Kubernetes Ingress Nginx 对比文档 (用于理解差异)

**学习建议**: 
先不要急于深入配置，先通读官方文档的“背景与简介”部分。建议使用 Minikube 或 Kind 创建一个简单的 K8s 集群，并成功部署一个 Higress 实例，通过控制台界面熟悉操作流程。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- 基本路由管理：学习如何配置基于域名、路径、Header 的路由转发规则。
- 高级流量管理：掌握灰度发布（金丝雀发布）、蓝绿部署、流量镜像与流量复制。
- 负载均衡策略：理解并配置轮询、随机、加权最少连接等负载均衡算法。
- 服务发现集成：学习如何将 Higress 与 Nacos、Consul、Kubernetes Service 等注册中心对接，实现自动服务发现。
- 健康检查：配置主动与被动健康检查，实现故障摘除与自动恢复。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy 官方文档 (关于 HTTP 路由与负载均衡的底层原理)
- Higress 控制台实操演示视频

**学习建议**: 
动手实践是关键。建议部署两个不同版本的后端服务（例如 v1 和 v2），通过配置 Header 匹配或权重比例来实现灰度发布，并观察流量走向。尝试模拟后端 Pod 宕机，观察 Higress 的摘除效果。

---

### 阶段 3：安全防护与可观测性

**学习内容**:
- 安全认证：配置 Basic Auth、JWT、ApiKey、OIDC 等多种认证鉴权方式。
- 访问控制：学习如何配置 IP 黑白名单、基于角色的访问控制 (RBAC)。
- 安全防护插件：了解并启用 WAF（Web应用防火墙）插件，防范 SQL 注入、XSS 等攻击。
- 可观测性集成：对接 Prometheus + Grafana 进行监控指标采集，配置日志服务（如 SLS、Loki）收集 Access Log。
- 链路追踪：集成 SkyWalking 或 Zipkin，实现全链路 Tracing。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与可观测性章节
- Prometheus 与 Grafana 基础教程
- OpenTelemetry 标准规范文档

**学习建议**: 
安全方面，重点测试不同鉴权方式的组合使用。可观测性方面，建议在本地搭建一套 Prometheus + Grafana，重点关注 Higress 提供的 Dashboard 模板，理解 QPS、延迟、成功率等关键指标的含义。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- 插件系统原理：深入理解 Higress 的插件加载机制与 Wasm (WebAssembly) 运行时。
- 插件开发：学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现特定业务逻辑（如请求改写、自定义限流、数据转换）。
- 插件调试与热更新：掌握插件的调试流程，体验在不重启网关的情况下动态加载插件。
- Lua 脚本支持（如有）：了解如何在 Higress 中使用 Lua 进行轻量级脚本扩展。
- 全局配置与网关组管理：学习如何在不同网关实例间共享配置，以及多租户隔离。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件开发指南
- Wasm (WebAssembly) 官方网站
- Higress 官方 Plugin Hub (参考社区插件源码)
- Go 语言基础教程 (如果基础薄弱)

**学习建议**: 
从修改一个现有的简单插件开始（例如修改请求 Header），然后尝试编写一个全新的插件。重点关注 Wasm 的性能特性以及与宿主环境的交互接口。阅读 GitHub 上社区贡献的插件源码是提高水平的捷径。

---

### 阶段 5：生产级

---
## 常见问题


### 1: Higress 是什么？它与 Alibaba 有什么关系？

1: Higress 是什么？它与 Alibaba 有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里云开源，并捐赠给云原生计算基金会（CNCF）作为沙箱（Sandbox）项目的项目。

Higress 的前身是阿里巴巴内部广泛使用的 API 网关 Tengine（基于 Nginx 深度定制）和云原生网关。它的设计初衷是结合传统的流量网关（如 Nginx）和微服务网关（如 Spring Cloud Gateway）的能力，提供一站式的流量管理、安全防护和插件扩展能力。它深度集成了 Envoy 和 Istio，旨在解决 Kubernetes 环境下的东西向（服务间）和南北向（入口）流量管理问题。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

**A**: Higress 与传统网关（如 Nginx、Kong、APISIX）相比，主要优势体现在以下几个方面：

1.  **云原生架构**：Higress 原生支持 Kubernetes 和 Istio，采用了控制面与数据面分离的架构。数据面默认使用 Envoy，其性能和可扩展性优于传统的 Nginx 模式。
2.  **标准兼容性**：它完全兼容 Kubernetes Ingress 和 Gateway API 标准，同时也兼容 Nginx 的 Ingress 注解，使得从 Nginx Ingress 迁移变得非常平滑。
3.  **安全与高可用**：继承了阿里双十一的高可用经验，支持 WAF（Web 应用防火墙）插件集成，且控制面与数据面分离，网关节点无状态，支持弹性伸缩。
4.  **插件生态**：支持 Wasm（WebAssembly）插件，允许开发者使用多种语言（如 Go、C++、Rust）编写插件，且插件热更新不需要重启网关，比传统的 Lua 插件更安全、灵活。

---



### 3: Higress 是否支持从 Nginx Ingress Controller 迁移？迁移难度大吗？

3: Higress 是否支持从 Nginx Ingress Controller 迁移？迁移难度大吗？

**A**: 是的，Higress 非常重视从 Nginx Ingress 的迁移体验，并设计为高度兼容。

1.  **注解兼容**：Higress 内置了对常用 Nginx Ingress Annotations（注解）的适配器。这意味着大部分情况下，你不需要修改 Kubernetes 的 Ingress YAML 文件中的注解，Higress 就能识别并生效。
2.  **配置迁移工具**：官方提供了配置迁移工具，可以帮助用户将现有的 Nginx 配置自动转换为 Higress 的路由配置。
3.  **零停机切换**：由于 Higress 支持标准的 Kubernetes Ingress 资源，你可以通过调整 Ingress Class 的选择器，逐步将流量从旧的 Nginx Ingress Controller 切换到 Higress，实现平滑过渡。

---



### 4: Higress 支持哪些类型的插件？如何开发自定义插件？

4: Higress 支持哪些类型的插件？如何开发自定义插件？

**A**: Higress 拥有非常灵活的插件系统，主要分为以下几类：

1.  **原生插件**：内置了常见的网关功能，如跨域处理、请求重写、 redirects、认证鉴权等。
2.  **Wasm 插件**：这是 Higress 推荐的扩展方式。它基于 Proxy-Wasm 规范，允许开发者使用 Go、AssemblyScript、Rust 或 C++ 等高性能语言编写业务逻辑。Wasm 插件运行在沙箱环境中，即使插件崩溃也不会导致网关崩溃，且支持热加载。
3.  **Lua 插件**：为了兼容 Kong 和 APISIX 的生态，Higress 也支持 Lua 脚本插件，方便旧代码的迁移。
4.  **原生 WASM 生态**：Higress 兼容 Istio 的 WasmPlugin API，这意味着很多为 Istio 开发的插件可以直接在 Higress 上运行。

开发者可以通过 Higress 提供的 CLI 工具或直接编写代码来创建自定义插件，并将其打包上传到 Higress 控制台进行配置。

---



### 5: Higress 的性能表现如何？能否支撑高并发流量？

5: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 的性能表现非常优异，完全能够支撑企业级的高并发流量。

1.  **底层引擎**：数据面基于 Envoy 构建。Envoy 是云原生领域公认的高性能 L7 代理，使用 C++ 编写，具备极高的处理效率和低延迟。
2.  **内部实践**：Higress 的核心代码源自阿里云内部承载双十一流量的网关系统，经过了数年每秒百万级 QPS 的考验。
3.  **基准测试**：在官方的基准测试中，Higress 在长连接、短连接、HTTPS 加解密等场景下的吞吐量和延迟表现均优于传统的 Nginx Ingress Controller。
4.  **弹性伸缩**：作为云原生网关，

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础服务路由配置

### 问题**: 在 Higress 的标准网关部署场景中，如何通过配置 YAML 文件，将一个特定的后端服务（例如运行在 Docker 容器中的 HTTP 服务）注册到 Higress 中，并配置一个简单的路由规则（例如 `/api/v1`）将流量转发至该服务？

### 提示**: 关注 Higress 的 `Ingress` 或 `Gateway` API 配置。你需要定义一个服务（Service）指向你的后端服务地址，然后创建一个 HTTPRoute 规则，匹配特定的路径前缀并将其指向该服务。检查 Higress 控制台或文档中关于“快速开始”或“路由配置”的基础示例。

### 

---
## 实践建议

### 实践建议

基于 Higress 对 AI 协议的原生支持及其云原生架构特性，以下是 6 条针对生产环境的实践建议：

#### 1. 利用 AI 插件统一模型接入
Higress 内置了对主流 AI 协议的支持，建议利用其 AI 代理能力进行协议转换。
*   **操作方式**：配置路由将标准的 OpenAI 协议请求转发至其他兼容或非兼容模型（如通义千问、Llama 3）。这使得业务端仅需维护一套 OpenAI SDK 调用逻辑，底层模型切换对代码透明。
*   **配置建议**：在网关层统一管理不同厂商的 API Key，避免在业务代码中硬编码密钥，便于集中管控和定期轮换。

#### 2. 配置上下文缓存以降低 Token 消耗
LLM 推理成本与 Token 消耗正相关，重复的 System Prompt 和历史上下文会带来额外开销。
*   **操作方式**：启用针对 AI 请求的缓存策略，配置基于请求体（Prompt）哈希的缓存。对于相同的输入，网关直接返回缓存结果，减少后端调用。
*   **注意事项**：需根据业务场景设置合理的 TTL（生存时间）。对于实时性要求高的场景（如数据查询），TTL 宜短；对于知识库问答，可适当延长 TTL 以节省成本。

#### 3. 实施基于 Token 的精细化限流
AI 请求的计算成本差异较大，传统的 QPS（每秒请求数）限流难以准确反映资源消耗。
*   **操作方式**：配置基于 TPM（每分钟 Token 数）或 RPM（每分钟请求数）的限流策略。例如，为不同级别的用户设置差异化的 Token 消耗额度。
*   **配置建议**：针对不同成本的模型路由设置独立的限流阈值。低成本模型（如 GPT-3.5）的阈值可相对宽松，而高成本模型（如 GPT-4）应实施更严格的限制。

#### 4. 使用 Wasm 插件进行 Prompt 处理与审计
利用 Wasm (WebAssembly) 的隔离性和扩展性，在网关层处理数据安全与合规。
*   **操作方式**：编写或加载 Wasm 插件，在请求转发前拦截并检查 Prompt 内容，自动过滤敏感信息（如 PII）或注入预设的安全指令。
*   **安全建议**：在响应阶段利用插件检查模型输出，拦截包含违规信息的回复，确保出网内容符合安全规范。

#### 5. 部署模式：Kubernetes Ingress 与独立部署
根据业务基础设施选择合适的部署形态。
*   **操作方式**：在容器化环境中，可将 Higress 部署为 Ingress Controller，通过 Kubernetes Ingress 或 Gateway API 资源管理路由规则，实现服务发现与网关配置的自动同步。
*   **注意事项**：在混合云或多集群环境下，建议将 Higress 接入服务注册中心（如 Nacos），使其能够发现并路由部署在 ECS 或非 K8s 环境中的本地推理服务。

#### 6. 可观测性：监控首字延迟与流式传输
AI 请求通常耗时较长，传统的 HTTP 总延迟监控无法完全反映用户体验。
*   **操作方式**：重点监控 **首字延迟（Time to First Token, TTFT）**，即请求发送到收到第一个 Token 的时间，这反映了模型的首包响应速度。同时，监控流式输出的吞吐量和生成速度，以评估端到端的性能表现。

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*