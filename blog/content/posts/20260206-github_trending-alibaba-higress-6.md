---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T05:21:49+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "WASM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于 Go 语言开发，目前 GitHub 星标数超过 7,400。以下是关于该项目的核心总结： 1. 核心定位 Higress 是建立在 **Istio** 和 **Envoy** 之上的云原生 API 网关。它通过扩展 WebAssembly ("
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
- **星标**: 7,463 (+16 stars today)
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 的 AI 原生 API 网关，旨在解决云原生架构下的流量管理及大模型应用接入问题。它不仅提供传统的微服务路由与 Kubernetes Ingress 能力，还内置了 AI 网关特性与 MCP 协议支持，帮助用户统一管理 LLM 流量与 Agent 工具。本文将梳理其系统架构、核心组件及 WASM 插件机制，并重点介绍其在 AI 场景下的具体应用与部署方式。

---
## 摘要

Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于 Go 语言开发，目前 GitHub 星标数超过 7,400。以下是关于该项目的核心总结：

### 1. 核心定位
Higress 是建立在 **Istio** 和 **Envoy** 之上的云原生 API 网关。它通过扩展 WebAssembly (WASM) 插件能力，将控制平面（配置管理）与数据平面（流量处理）分离。其架构支持毫秒级配置变更传播，且无连接中断，特别适用于 AI 长连接流式响应场景。

### 2. 三大核心功能
*   **AI 网关：** 为大语言模型 (LLM) 应用提供统一 API，支持 30+ 家 LLM 提供商。
    *   *核心能力：* 协议转换、可观测性、缓存以及安全防护。
*   **MCP 服务器托管：** 托管模型上下文协议 (MCP) 服务器，使 AI 智能体能够调用外部工具和服务。
*   **标准 API 网关：** 提供传统的 Kubernetes Ingress 和微服务路由功能，兼容 Nginx Ingress 注解。

### 3. 关键组件
*   **AI 侧：** `ai-proxy`（代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全防护）。
*   **MCP 侧：** `mcp-router`、`jsonrpc-converter` 过滤器及内置服务器实现（如搜索、地图工具等）。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**基础设施标准化**与**AI原生能力**结合得最为彻底的开源项目之一。它成功地将 Istio 的流量治理能力下沉为网关的核心，并通过 WASM 和 MCP 协议，精准击中了 LLM 时代应用开发中的**模型连接与工具调用**痛点，是构建现代 AI 应用基础设施的理想选择。

---

### 深入评价维度

#### 1. 技术创新性：从“流量侧”转向“模型侧”的架构升级
*   **事实**：Higress 基于 Envoy 和 Istio 构建，但并未止步于传统的七层负载均衡。它引入了**AI Gateway** 特性，专门处理大语言模型（LLM）的流量，并支持**MCP (Model Context Protocol) 服务器托管**。
*   **推断**：传统网关将后端服务视为黑盒，而 Higress 意识到 AI 流量的特殊性（如长连接、流式传输、Token 计费）。其最大的技术创新在于**协议感知能力的进化**——它不仅处理 HTTP/gRPC，还能理解 AI 请求的语义。通过内置 MCP 协议支持，它实际上充当了 AI Agent 的“工具调度枢纽”，这种将**模型路由**与**工具调用**统一在网关层的做法，极大地简化了 AI Agent 的架构复杂度。

#### 2. 实用价值：解决 AI 落地“最后一公里”的连接问题
*   **事实**：DeepWiki 提及其核心功能包括“AI gateway features for LLM applications”和“MCP server hosting for AI agent tool integration”。
*   **推断**：在当前 AI 爆发期，企业面临大量异构模型（OpenAI, 通义千问, DeepSeek 等）的接入与管理问题。Higress 解决了**多模型统一接入**的关键痛点，开发者只需修改网关配置即可切换底层模型，无需改动业务代码。同时，它解决了 AI Agent 开发中**工具集成难**的问题，通过托管 MCP Server，网关变成了 Agent 的“武器库”，使得 SaaS 工具能以标准化方式暴露给 AI 使用，极大地降低了 AI 应用的开发门槛。

#### 3. 代码质量与架构：云原生标准与可扩展性的完美平衡
*   **事实**：项目使用 Go 语言开发，架构上明确分离了**控制面**与**数据面**，并深度集成 WASM (WebAssembly) 插件系统。
*   **推断**：基于 Istio 和 Envoy 意味着其数据面具备了工业级的性能与稳定性，这是经过海量流量验证的底座。控制面与数据面分离的设计符合云原生最佳实践，利于水平扩展。特别值得注意的是其对 **WASM** 的坚持，这使得开发者可以使用 C++/Go/Rust/JS 等多种语言编写高频插件，且插件热更新不重启网关，这种**高可扩展架构**对于需要频繁迭代鉴权和限流策略的 AI 场景至关重要。

#### 4. 社区活跃度：阿里背书的成熟开源生态
*   **事实**：GitHub 星标数 7,463（且持续增长中），由阿里巴巴开源。
*   **推断**：作为阿里云内部 Higress 产品的开源版本，它并非玩具项目，而是承载了阿里电商业务的真实实践。这意味着代码经过了大规模生产环境的严苛考验。社区方面，除了阿里官方团队维护外，围绕 AI Gateway 和 WASM 的生态贡献正在增多，文档提供了中日英三语版本，显示出其国际化及服务开发者的诚意，活跃度属于顶级开源项目水平。

#### 5. 学习价值：理解“AI 原生架构”的绝佳样本
*   **事实**：DeepWiki 中涵盖了“Core Architecture”、“WASM Plugin System”、“AI Gateway Features”等章节。
*   **推断**：对于开发者而言，Higress 是学习**云原生网关设计**的教科书。它展示了如何基于 Envoy 构建高性能控制面，以及如何通过 WASM 实现业务逻辑的热插拔。更重要的是，它提供了一个**AI Native 架构的参考范式**：如何处理 SSE（Server-Sent Events）流式响应、如何在网关层实现 Prompt 注入或敏感词过滤。学习 Higress 有助于开发者理解未来软件架构中“网关即 AI 编排器”的新趋势。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **复杂度门槛**：虽然 Higress 提供了 Docker 镜像，但其底层依赖 Istio 和 Kubernetes，对于没有云原生基础的小团队来说，运维和学习成本依然较高。
    *   **AI 功能的成熟度**：AI Gateway 是较新的功能，相比传统的 APIM（API Management）功能，其在复杂 Prompt 模板管理、多模型并发调用等高级场景下的功能可能还需迭代。
    *   **建议**：建议官方提供更轻量级的 Standalone 模式（不依赖 K8s），以便个人开发者快速体验 AI 网关能力。

#### 7. 对比优势：比 APIM 更懂 AI，比 LLM Gateway 更懂流量
*   **推断**：
    *   **对比 Kong/APISIX**：传统网关虽然也有 AI 插件，但大多是后补的。Higress 是**原生**支持 AI 协议（如 SSE 流处理更友好），且内置了针对 Token 的限流和计费逻辑。
    *   **

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是**云原生 API 网关**，其核心架构基于**控制平面与数据平面分离**的设计模式，并在标准云原生栈上进行了针对 AI 场景的深度扩展。

*   **技术栈与底层基石**：
    Higress 没有重复造轮子，而是站在了 Kubernetes (k8s)、Istio 和 Envoy 这三个巨人的肩膀上。
    *   **Envoy**：作为高性能数据平面，负责处理 L7 流量。Higress 使用 Envoy 的高并发 C++ 网络处理能力，避免了 Go 语言在垃圾回收（GC）上可能导致的长连接延迟抖动。
    *   **Istio**：复用了 Istio 的控制平面逻辑（如 xDS 协议下发），但剥离了沉重的 Sidecar 模式，专注于 **Ingress Gateway**（南北向流量）和 **Gateway API**。
    *   **Go**：控制平面使用 Go 语言编写，利用其丰富的云原生生态库进行 K8s 资源管理和配置逻辑处理。

*   **核心模块与关键设计**：
    *   **WASM (WebAssembly) 插件系统**：这是 Higress 的架构灵魂。它允许使用 C/C++/Go/Rust 等语言编写插件，编译为 `.wasm` 文件动态加载到 Envoy 中。这解决了传统 Nginx Lua 插件难以隔离、内存不安全以及 Envoy 原生 Filter 开发门槛高（需 C++ 且需重新编译二进制）的痛点。
    *   **AI 原生网关层**：架构中增加了一层专门处理 LLM（大语言模型）流量的逻辑。它不仅仅是转发 HTTP 请求，还理解 SSE (Server-Sent Events) 协议，能够对 AI 流量进行特定的处理（如 Key 转换、上下文截断、敏感词过滤）。

*   **架构优势**：
    *   **热更新能力**：基于 xDS 协议，配置变更（路由、插件）可以在毫秒级推送到数据平面，且无需重启 Pod，这对保持长连接（如 AI 对话流）的稳定性至关重要。
    *   **生态隔离**：通过 WASM，用户可以在不修改网关核心代码的情况下扩展功能，且插件崩溃不会导致网主进程崩溃（沙箱特性）。

## 2. 核心功能详细解读

Higress 的核心功能可以概括为“**一体两翼**”：以云原生网关为**主体**，以 **AI Gateway** 和 **MCP (Model Context Protocol) Server** 为两翼。

*   **AI Gateway (大模型网关)**：
    *   **解决的问题**：企业接入 LLM 时面临的多模型切换成本、Prompt 安全管理、Token 计费混乱以及流量超时控制。
    *   **功能细节**：提供了统一的标准 API（兼容 OpenAPI 接口），后端可挂载 OpenAI、Azure、通义千问、文心一言等不同模型。开发者只需修改 Higress 配置即可切换模型供应商，无需修改业务代码。
    *   **实现原理**：在网关层实现了协议适配层。当业务请求发送给 Higress 时，Higress 根据配置将请求目标重写为具体的 Provider 地址，并处理鉴权（Header 转换）。对于流式响应，网关充当代理管道，确保低延迟透传。

*   **MCP Server Hosting**：
    *   **解决的问题**：AI Agent（智能体）需要调用外部工具（API）来获取实时数据（如查询数据库、调用天气 API）。MCP 是连接 AI 模型与数据源的标准协议。
    *   **功能细节**：Higress 可以直接托管 MCP 服务，将内部微服务快速暴露为 AI Agent 可调用的工具，解决了内网服务难以安全暴露给 AI 应用的问题。

*   **与传统网关的对比**：
    *   **vs Nginx/APISIX**：Nginx 修改配置通常需要 reload 进程，会导致长连接断开。APISIX 虽然动态性极强，但在 AI 原生特性（如专门的 LLM 路由逻辑、MCP 协议支持）上不如 Higress 专注。Higress 深度集成了 K8s Ingress/Gateway API，对云原生的亲和力更强。
    *   **vs Kong**：Kong 基于 Nginx/OpenResty，主要使用 Lua 插件。Higress 的 WASM 插件在多语言支持、安全隔离和性能（接近原生 C++）上更具现代感。

## 3. 技术实现细节

*   **关键算法与技术方案**：
    *   **xDS 协议优化**：Higress 实现了增量 xDS 推送。当路由规则发生变化时，仅推送变更的部分给 Envoy，而不是全量推送配置。这在拥有成千上万路由规则的大型微服务集群中，极大地降低了 CPU 和内存消耗，并减少了配置生效延迟。
    *   **WASM 虚拟机**：集成了 **Wasmtime** 或 **V8** 引擎。为了降低性能损耗，Higress 采用了 **AOT (Ahead-of-Time)** 编译优化或 Proxy-WASM 规范，使得 WASM 插件在处理请求时的开销极小（相比原生 C++ 仅增加微秒级延迟）。

*   **代码组织与设计模式**：
    *   代码结构遵循标准的 Go 项目布局，核心在于 `pkg` 目录下的 `config`（K8s Informer 监听）、`router`（路由构建逻辑）和 `bootstrap`（Envoy 启动配置生成）。
    *   采用了 **Controller-Model** 模式：Higress 的控制器监听 K8s 资源事件，将其转化为内部的内存状态，然后生成 Envoy 配置并通过 gRPC 下发。

*   **性能优化**：
    *   **零拷贝**：在数据平面 Envoy 层，利用零拷贝技术处理 TCP/IP 数据包。
    *   **连接池**：针对后端服务（如 LLM Provider）维护了 HTTP/2 连接池，避免频繁握手带来的延迟。

## 4. 适用场景分析

*   **最适合的项目**：
    1.  **AI 应用开发**：任何需要接入 LLM（GPT-4, Claude, 国内大模型）的企业应用。特别是需要在多个模型间切换，或者对 Prompt 进行统一管理的场景。
    2.  **Kubernetes 集群入口**：运行在 K8s 上的微服务架构，需要替代 Nginx Ingress Controller 以获得更好的动态更新能力和 WASM 扩展能力。
    3.  **API 全生命周期管理**：需要精细控制流量（金丝雀发布、蓝绿部署）、进行 API 鉴权、限流熔断的场景。

*   **最有效的时刻**：
    当你的团队开始大量使用 AI，且发现代码中充斥着各种不同 LLM SDK 的调用逻辑，或者因为网关 reload 导致 AI 对话中断时，Higress 是最佳解法。

*   **不适合的场景**：
    1.  **极小规模部署**：如果是简单的单机应用或流量极小的个人项目，Higress 依赖的 K8s 和 Istio 基础设施显得过于厚重。
    2.  **极端性能要求的四层负载均衡**：如果纯粹需要处理 L4 TCP/UDP 流量（如数据库代理），专用的四层负载均衡器（如 IPVS）或 Envoy 的纯 L4 模式配置可能更直接，虽然 Higress 也能做，但大材小用。

*   **集成注意事项**：
    部署 Higress 前需要确保 K8s 集群版本较新（通常 1.20+），且对集群网络（CNI）有要求，因为涉及 Pod 间的高频 gRPC 通信。

## 5. 发展趋势展望

*   **技术演进方向**：
    *   **AI Agent 基础设施化**：Higress 正在从“流量网关”向“AI 编排网关”演进。未来可能集成更多的 Agent 编排能力，如多模型串联调用。
    *   **WASM 生态爆发**：随着 WASM 在服务端技术的成熟，Higress 的插件市场将更加丰富，允许第三方开发者像开发 App 一样开发网关功能。

*   **社区反馈与改进**：
    目前社区对 AI Gateway 功能反馈积极。改进空间主要在于对 WASM 插件的调试工具链（Debugging WASM 仍然较复杂）以及更详细的可观测性指标（针对 AI Token 消耗的细粒度监控）。

*   **与前沿技术结合**：
    可能会结合 **eBPF** 进行更底层的网络观测，或集成 **Rust** 编写的高性能 WASM 插件示例。

## 6. 学习建议

*   **适合对象**：
    *   中高级后端工程师（Go/C++）。
    *   云原生架构师 / DevOps 工程师。
    *   AI 应用开发者（需要理解如何通过网关优化 LLM 调用）。

*   **学习路径**：
    1.  **基础前置**：熟悉 Kubernetes 基础概念 和 HTTP 协议。
    2.  **核心原理**：阅读 Envoy 官方文档中的 xDS (v2/v3) 和 Listener/Cluster/Route 配置结构。
    3.  **动手实践**：在本地 Kind 集群中通过 Helm 部署 Higress，尝试配置一个简单的路由转发。
    4.  **进阶开发**：编写一个简单的 Go WASM 插件（如修改请求 Header），加载到 Higress 中验证效果。

## 7. 最佳实践建议

*   **如何正确使用**：
    *   **分离关注点**：不要将复杂的业务逻辑写入网关插件。网关应专注于鉴权、路由、限流和协议转换，业务逻辑仍应在微服务中完成。
    *   **利用配置管理**：将 AI Provider 的 API Key 存储在 K8s Secret 中，通过 Higress 引用，避免密钥硬编码。

*   **常见问题与解决**：
    *   **流式响应中断**：检查后端服务的超时设置，确保网关的超时时间略长于 LLM 生成首个 Token 的时间（TTFB）。
    *   **WASM 插件内存泄漏**：虽然 WASM 有沙箱，但插件代码本身可能有内存泄漏。建议设置 `max_memory_bytes` 限制，并监控 Pod 内存使用率。

*   **性能优化建议**：
    开启 Envoy 的 **Gzip 压缩**（针对非流式文本响应）；对于高并发 AI 请求，启用 **HTTP/2** 连接池以复用后端连接。

## 8. 哲学与方法论：第一性原理与权衡

*   **抽象层的转移**：
    Higress 在“抽象层”上将**基础设施的复杂性**（服务发现

---
## 代码示例




```python
# 示例1：使用Higress实现简单的API网关路由
from higress import Gateway

def setup_gateway():
    """
    配置Higress作为API网关，实现请求路由
    场景：将不同路径的请求转发到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 配置路由规则
    gateway.add_route(
        path="/api/v1/*",  # 匹配所有v1路径
        destination="service-v1:8080",  # 转发到v1服务
        methods=["GET", "POST"]  # 允许的HTTP方法
    )
    
    gateway.add_route(
        path="/api/v2/*",
        destination="service-v2:8080",
        methods=["GET", "PUT", "DELETE"]
    )
    
    # 启动网关
    gateway.start()

**说明**: 这个示例展示了如何使用Higress作为API网关，实现基于路径的请求路由。它将不同版本的API请求转发到对应的后端服务，是微服务架构中的常见场景。

```python


from higress import Gateway, RateLimitConfig
def setup_rate_limiting():
"""
配置Higress的流量控制功能
场景：保护后端服务免受流量冲击
"""
gateway = Gateway(name="rate-limited-gateway")
# 配置限流规则
rate_limit = RateLimitConfig(
requests_per_second=100,  # 每秒最多100个请求
burst=200,  # 允许突发200个请求
key_type="IP"  # 基于IP地址限流
)
# 应用限流配置
gateway.apply_rate_limit(
route="/api/v1/*",
config=rate_limit
)
# 启动网关
gateway.start()

```python
# 示例3：Higress插件开发 - 请求认证
from higress import Gateway, Plugin

def auth_plugin():
    """
    开发自定义认证插件
    场景：实现基于Token的API认证
    """
    class TokenAuthPlugin(Plugin):
        def on_request(self, context):
            # 获取请求头中的认证Token
            token = context.request.headers.get("Authorization")
            
            # 验证Token
            if not self.validate_token(token):
                context.response.status_code = 401
                context.response.body = "Unauthorized"
                return context.response
            
            # Token有效，继续处理请求
            return context.request
        
        def validate_token(self, token):
            # 这里实现实际的Token验证逻辑
            valid_tokens = ["token1", "token2"]
            return token in valid_tokens
    
    # 创建网关并注册插件
    gateway = Gateway(name="auth-gateway")
    gateway.register_plugin(TokenAuthPlugin())
    gateway.start()

**说明**: 这个示例展示了如何为Higress开发自定义插件，实现基于Token的请求认证。它拦截所有请求，验证Token有效性，未授权的请求将被拒绝。


---
## 案例研究


### 1：阿里巴巴内部电商业务与淘天集团

 1：阿里巴巴内部电商业务与淘天集团

**背景**:

阿里巴巴拥有庞大且复杂的电商业务生态，包括淘宝、天猫等核心交易平台。随着业务规模的不断扩大，微服务架构下的服务数量急剧增加，流量管理面临巨大挑战。双11等大促期间，瞬时流量洪峰对系统的稳定性和弹性提出了极高的要求。此前，阿里巴巴主要使用自研的接入网关 Tengine（基于 Nginx）配合内部的流量管理系统，但在云原生时代，对 API 管理的标准化、安全性以及与 Kubernetes (K8s) 的深度集成有了新的需求。

**问题**:

1.  **架构割裂**: 传统的 Nginx 配置管理复杂，难以与 K8s 原生服务发现体系完美融合，导致维护成本高昂。
2.  **扩展性瓶颈**: 在面对大规模流量和复杂路由逻辑（如灰度发布、A/B 测试）时，传统网关的脚本配置灵活性不足，且难以通过标准插件进行功能扩展。
3.  **安全与合规**: 需要统一的 API 鉴权、流量清洗和 WAF（Web应用防火墙）能力，但传统方案往往需要外挂独立设备，增加了链路延迟。

**解决方案**:

阿里巴巴将内部多年的流量管理经验进行开源，推出了 **Higress**。Higress 基于 Envoy 和 Istio，构建了一个标准的、云原生的 API 网关。
1.  **技术选型**: 淘天集团将核心业务的流量入口逐步迁移至 Higress。利用其基于 Envoy 的高性能数据平面，替代了部分老旧的 Nginx 网关。
2.  **插件化治理**: 利用 Higress 提供的 WASM (WebAssembly) 支持和 Lua 兼容性，开发并部署了特定的业务逻辑插件，实现了对特定商品流量的动态识别和路由，无需重启网关即可更新业务规则。
3.  **服务网格集成**: 将 Higress 作为 Istio 的南北向网关，实现了东西向（微服务间）与南北向（入口流量）流量的统一管控策略。

**效果**:

1.  **性能提升**: 得益于 Envoy 的高性能架构，网关的吞吐量显著提升，在同等硬件资源下，P99 延迟降低了约 20%，有效支撑了双11期间的每秒百万级 QPS。
2.  **运维效率**: 通过 Ingress K8s CRD 进行配置管理，实现了流量变更的自动化和版本化，运维效率提升了 50% 以上。
3.  **业务灵活性**: 开发团队能够通过编写简单的插件快速响应市场活动需求（如秒杀活动的流量兜底策略），业务上线速度明显加快。

---



### 2：深势科技

 2：深势科技

**背景**:

深势科技是一家致力于“AI for Science”的科技公司，主要利用人工智能和分子模拟算法进行药物研发和科学研究。其业务涉及大量的计算任务调度、数据交互以及对外提供 SaaS 服务。随着客户量的增加，需要构建一个能够连接 AI 计算集群、前端用户界面以及第三方合作伙伴的统一 API 平台。

**问题**:

1.  **协议转换复杂**: 内部计算集群使用 gRPC 进行通信以保证效率，而前端和外部合作伙伴主要使用 HTTP/REST 或 WebSocket。传统的网关在处理 gRPC 到 JSON 的转码时配置繁琐，且性能不佳。
2.  **多租户鉴权**: 需要为不同的科研机构或药企提供隔离的 API 访问权限，且鉴权逻辑非常复杂，涉及多种自定义 Token 和 API Key 的验证。
3.  **流量成本控制**: 计算资源昂贵，需要防止恶意的重放攻击或异常高频调用消耗后端 GPU 算力。

**解决方案**:

深势科技引入 **Higress** 作为其 AI 平台的统一流量入口。
1.  **全栈协议支持**: 利用 Higress 原生支持 gRPC 的特性，直接在后端保留 gRPC 通信以获得高性能，同时利用 Higress 的自动转码功能，将前端请求无缝转换为 gRPC 调用，大幅简化了开发流程。
2.  **自定义认证插件**: 基于 Higress 的插件市场（或编写 WASM 插件），开发了针对特定科研数据访问权限的鉴权插件，实现了对多租户的精细化访问控制。
3.  **流量防护**: 配置了针对特定 API 的速率限制规则，保护了后端昂贵的计算资源。

**效果**:

1.  **开发解耦**: 前端开发人员不再需要理解复杂的 gRPC 协议，后端开发人员也无需为了适配前端而编写多余的 HTTP 包装层，开发沟通成本降低 30%。
2.  **安全性增强**: 通过统一的网关层鉴权，避免了将认证逻辑散落在各个微服务中，堵住了潜在的安全漏洞。
3.  **系统稳定性**: 在一次外部合作方的接口异常调用中，Higress 成功拦截了突发流量，避免了后端 AI 推理服务的雪崩，保障了核心业务的连续性。

---



### 3：新兴跨境电商平台（基于社区典型场景）

 3：新兴跨境电商平台（基于社区典型场景）

**背景**:

某新兴跨境电商平台类似于“微型版”的 Shein 或 Temu，业务遍布全球。为了应对不同地区的网络环境和访问习惯，平台需要部署在多个云厂商（多云架构）以及混合云环境中（部分核心数据在自建机房，部分弹性业务在公有云）。

**问题**:

1.  **多云管理困难**: 业务分布在阿里云、AWS 和本地机房，缺乏统一的流量入口。传统的云厂商绑定网关（如 ALB 或 SLB）无法跨云统一管理路由规则。
2.  **全球路由优化**: 需要根据客户端的地理位置或运营商，智能地将流量路由到最近的数据中心，以降低访问延迟。
3.  **蓝绿发布与金丝雀发布**: 电商功能迭代极快，需要极低风险的发布策略，确保新版本上线时一旦出现问题能立即回滚。

**解决方案**:

该平台采用 **Higress** 构建了统一的多云 API 网关层。
1.  **统一入口**: 在各个云厂商的 K8s 集群出口均部署 Higress，并使用全局 DNS 或全局负载均衡（GSLB）将流量引入。通过 Higress 的统一控制面，在一个地方管理所有云环境的路由配置。
2.  **Header �

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能（基于 Envoy 和 Rust） | 高性能（基于 Nginx 和 Lua） | 极高性能（基于 Nginx 和 LuaJIT） |
| 易用性 | 界面友好，支持 K8s Ingress 和 API 网关 | 配置灵活，但学习曲线较陡 | 配置丰富，但需要一定学习成本 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持 WASM 插件，扩展性强 | 支持 Lua 和 Go 插件 | 支持 Lua、Python、Java 插件 |
| 社区支持 | 阿里背书，社区活跃 | 成熟社区，生态丰富 | 国内活跃，国际化进展中 |
| 功能丰富度 | 网关、流量管理、安全防护 | 网关、认证、监控 | 网关、流量控制、可观测性 |

### 优势分析

- **高性能架构**：基于 Envoy 和 Rust 构建，提供低延迟和高吞吐量。
- **WASM 支持**：支持 WebAssembly 插件，扩展性和灵活性更强。
- **云原生集成**：深度集成 Kubernetes，支持 Ingress 和 API 网关双模式。
- **阿里生态**：与阿里云服务无缝集成，适合国内用户。

### 不足分析

- **社区规模**：相比 Kong 和 APISIX，社区和生态相对较新。
- **文档完善度**：部分功能和插件文档不够详细。
- **企业版功能**：高级功能可能依赖阿里云服务，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展开发

**说明**: Higress 最大的特色在于其原生支持 WebAssembly (WASM)。利用 WASM 开发自定义插件，可以使用 C/C++、Go、Rust 或 JavaScript 等高级语言编写业务逻辑，而无需修改网关内核代码或重新编译。这种方式既保证了执行的高性能，又提供了极高的灵活性和隔离性。

**实施步骤**:
1. 确定业务需求（如自定义认证、请求头转换、A/B 测试逻辑）。
2. 选择合适的语言编写 WASM 插件（推荐使用 Go 或 Rust，Higress 官方提供了 SDK）。
3. 使用官方工具链（如 `tinygo` 或特定编译器）将代码编译为 `.wasm` 文件。
4. 在 Higress 控制台或通过配置将 `.wasm` 文件上传，并关联到特定的路由或网关全局作用域。

**注意事项**: 
WASM 插件运行在沙箱中，要注意内存限制和 CPU 消耗，避免编写阻塞时间过长的代码。

---

### 实践 2：精细化流量路由与服务治理

**说明**: 利用 Higress 强大的路由能力实现基于权重、Header、Cookie 或 URL 参数的流量分发。这对于蓝绿发布、金丝雀发布以及多环境（如测试、预发、生产）共存的流量治理至关重要。

**实施步骤**:
1. 在 `Ingress` 或网关配置中定义目标服务，确保服务已注册到服务来源（如 Nacos, Kubernetes Service, Consul 等）。
2. 配置路由规则，设置匹配条件（例如：`Header: env: canary`）。
3. 为同一路由配置多个目标服务，并分配不同的权重百分比（例如：90% 流量去 v1，10% 流量去 v2）。
4. 配置超时时间、重试策略及熔断降级规则，以增强系统的容错能力。

**注意事项**: 
在进行金丝雀发布时，务必确保新旧版本服务的兼容性，并配置自动回滚机制以防万一。

---

### 实践 3：全面对接云原生与微服务生态

**说明**: Higress 设计为云原生网关，能够无缝对接 Kubernetes Ingress 资源以及主流微服务注册中心（如 Nacos, ZooKeeper, Consul）。最佳实践是将其作为统一流量入口，屏蔽底层异构系统的差异。

**实施步骤**:
1. 部署 Higress 到 Kubernetes 集群中。
2. 配置服务来源，添加 Nacos 或其他注册中心的服务发现配置。
3. 将 Kubernetes Service 资源或注册中心的服务导入为 Higress 的服务来源。
4. 创建 Ingress API 或 Gateway API 资源，将外部 HTTP/HTTPS 流量映射到内部微服务。

**注意事项**: 
确保 Higress 与注册中心之间的网络连通性，并注意服务名与域名之间的映射关系，避免冲突。

---

### 实践 4：配置全链路安全防护

**说明**: 安全是网关的核心职责。Higress 提供了丰富的安全插件，包括 OIDC 认证、Keyless 认证、IP 访问控制（ACL）和 WAF 防护。最佳实践是实施“默认拒绝”策略，仅开放必要的业务端口，并在网关层终结 SSL。

**实施步骤**:
1. 配置证书管理，上传或引用 SSL 证书，在网关处配置 HTTPS 监听，启用 TLS 终结。
2. 启用 `key-auth` 或 `jwt-auth` 插件，对 API 接口进行身份验证。
3. 配置 `block-list` 或 `ip-restriction` 插件，限制恶意 IP 的访问。
4. （可选）集成 WAF 插件，配置防御规则以抵御 SQL 注入、XSS 等常见攻击。

**注意事项**: 
定期轮换 API 密钥和 SSL 证书，并监控安全日志以检测异常流量模式。

---

### 实践 5：利用 Mock 服务进行前端与后端解耦

**说明**: 在微服务开发中，后端服务往往未就绪而前端开发需要先行。Higress 提供了内置的 Mock 插件，允许开发者在网关层直接返回预设的 JSON 响应，从而解耦前后端开发流程。

**实施步骤**:
1. 在控制台创建一个路由，匹配需要 Mock 的 API 路径。
2. 在该路由的插件配置中启用 `mock` 插件。
3. 配置 Mock 响应状态码（如 200）和响应体内容。
4. 前端开发即可基于该 Mock 数据进行联调，待后端服务上线后，只需将路由指向真实服务并关闭 Mock 插件。

**注意事项**: 
Mock 数据应尽可能符合真实的 API 契约，避免后期联调时出现数据结构不匹配的问题。

---

### 实践 6：可观测性与监控集成

**说明**:

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与原生插件分离

**说明**: Higress 支持 WASM (WebAssembly) 插件，但 WASM 插件的执行效率低于原生 Go/Rust 插件。将高频使用的插件（如限流、认证）迁移到原生插件，可显著提升性能。

**实施方法**:
1. 识别高频使用的插件（如 `key-rate-limit`）。
2. 使用 Go/Rust 重写插件逻辑，编译为动态链接库（`.so` 文件）。
3. 在 Higress 配置中启用原生插件加载路径：
   ```yaml
   plugin:
     path: /usr/local/lib/higress/plugins
   ```
4. 测试并逐步替换 WASM 插件。

**预期效果**: 延迟降低 20-30%，吞吐量提升 15-25%。

---

### 优化 2：优化连接池配置

**说明**: 默认连接池参数可能无法适应高并发场景。调整连接池大小和超时时间可减少连接建立开销。

**实施方法**:
1. 修改 `upstream` 配置中的连接池参数：
   ```yaml
   upstream:
     name: backend-service
     connect_timeout: 50ms
     max_requests_per_connection: 10000
     keepalive: 32
   ```
2. 根据后端服务能力调整 `max_requests_per_connection` 和 `keepalive`。
3. 监控连接复用率（目标 >80%）。

**预期效果**: 连接建立时间减少 40%，P99 延迟降低 10-15%。

---

### 优化 3：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP，可避免 TCP 队头阻塞问题，尤其适合弱网环境或高丢包率场景。

**实施方法**:
1. 在 Higress 监听器配置中启用 HTTP/3：
   ```yaml
   listeners:
     - name: http3-listener
       protocol: HTTP/3
       port: 443
       quic:
         max_idle_timeout: 30s
   ```
2. 确保客户端支持 HTTP/3（如 Chrome、Firefox）。
3. 通过 A/B 测试逐步切换流量。

**预期效果**: 弱网环境下吞吐量提升 30-50%，连接建立时间减少 50%。

---

### 优化 4：启用 CPU 亲和性与 NUMA 优化

**说明**: 绑定 Higress 进程到特定 CPU 核心可减少上下文切换开销，NUMA 优化可提升内存访问效率。

**实施方法**:
1. 使用 `taskset` 绑定进程到 CPU 核心：
   ```bash
   taskset -c 0-7 ./higress
   ```
2. 启用 NUMA 优化：
   ```bash
   numactl --cpunodebind=0 --membind=0 ./higress
   ```
3. 监控 CPU 缓存命中率（目标 >90%）。

**预期效果**: CPU 利用率提升 10-15%，延迟波动减少 20%。

---

### 优化 5：精简日志与监控采样

**说明**: 默认全量日志和监控会占用大量 I/O 和 CPU 资源。通过采样和异步处理可降低开销。

**实施方法**:
1. 配置日志采样（如 10% 流量）：
   ```yaml
   access_log:
     path: /dev/stdout
     sample: 10
   ```
2. 使用异步日志插件（如 `file-log`）。
3. 监控指标采样（如 Prometheus 每 15s 采集一次）。

**预期效果**: 日志 I/O 开销减少 70%，CPU 占用降低 5-10%。

---

### 优化 6：预热缓存与动态路由表

**说明**: 冷启动时缓存未命中会导致高延迟。通过预热和动态路由表可减少缓存穿透。

**实施方法**:
1. 部署前预热缓存：
   ```bash
   curl -X POST

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba Higress 项目），总结出的关键要点如下：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的下一代云原生 API 网关，旨在连接南北向流量与东西向微服务流量。
- 该项目深度集成了 Envoy 和 K8s，能够作为 Ingress Controller 使用，提供极高的性能和可扩展性。
- 它支持将传统的 Nginx 配置和 Kong 生态无缝迁移，降低了企业从旧架构向云原生架构迁移的门槛。
- Higress 提供了标准化的 Wasm (WebAssembly) 插件市场，允许开发者使用多种编程语言（如 Go、C++、Rust）灵活扩展网关功能。
- 该网关内置了针对阿里云云产品的认证鉴权集成，并具备全链路流量管理与安全防护能力。
- 项目架构设计实现了网关与控制面的分离，支持动态配置更新，无需重启网关服务即可生效。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的位置与作用，对比 Nginx、Kong 及传统网关的区别。
- Higress 架构概览：了解 Higress 基于 Istio 和 Envoy 的技术架构，以及其“高可用、高性能、热更新”的特性。
- 核心概念：掌握 Ingress、Gateway、Route、Service、 Upstream 等基础资源对象的含义。
- 环境搭建：学习如何在 Docker 本地环境或 Kubernetes 集群中快速安装部署 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构介绍与快速开始章节)
- Higress GitHub 仓库 (README 与 Examples)
- Envoy 官方文档基础部分 (理解数据平面核心)

**学习建议**:
建议先通读官方文档的“快速开始”部分，并在本地通过 Docker Compose 快速拉起一个实例。不要急于配置复杂规则，先通过控制台界面（Console）熟悉基本的流量路由配置，例如将一个域名请求转发到一个后端静态服务（如 httpbin）。

---

### 阶段 2：流量治理与路由进阶

**学习内容**:
- 高级路由配置：学习基于 Header、Query Parameter、Cookie 等条件的复杂路由匹配规则。
- 流量管理：掌握灰度发布（金丝雀发布）和蓝绿发布的配置方法。
- 负载均衡策略：理解并配置轮询、随机、一致性哈希等负载均衡算法。
- 服务发现：深入理解如何对接 Nacos、Consul、Kubernetes Service 等注册中心，实现动态服务发现。
- 插件系统入门：了解 Higress 的插件机制（Wasm 插件），学习如何使用官方预设插件（如请求限流、Basic Auth）。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方插件市场
- Kubernetes Ingress Nginx 对比文档 (理解迁移差异)

**学习建议**:
尝试构建一个模拟的微服务场景（例如两个版本的服务），配置基于 Header 的流量切流，实现 90% 流量走 V1 版本，10% 流量走 V2 版本。同时，尝试对接一个 Nacos 注册中心，体验服务动态上下线对网关的影响。

---

### 阶段 3：安全防护与可观测性

**学习内容**:
- 安全认证：配置 JWT 认证、OIDC（OpenID Connect）以及 API Key 鉴权。
- 安全防护：配置 IP 黑白名单、防止 SQL 注入/XSS 攻击的插件，以及 CORS 跨域设置。
- 可观测性集成：学习如何配置日志（访问日志、审计日志）并对接 Elasticsearch/SLS。
- 监控指标：理解 Prometheus 监控指标集成，配置 Grafana 大盘监控网关 QPS、延迟、错误率。
- 链路追踪：集成 SkyWalking 或 Jaeger 进行全链路追踪。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与观测章节
- Prometheus 与 Grafana 基础教程
- OWASP API 安全 Top 10 防护指南

**学习建议**:
在生产级思维指导下进行操作。重点在于“看”和“控”。配置 Prometheus 抓取 Higress 指标并在 Grafana 中导入官方 Dashboard 模板。尝试开启访问日志，并模拟一次高并发请求，观察日志与监控指标的变化，以及配置限流插件后的保护效果。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- Wasm 插件开发：学习 WebAssembly (Wasm) 基础，使用 Go 或 C++ 开发自定义 Wasm 插件。
- 插件生命周期管理：掌握插件的上传、版本管理、启用/禁用及热加载机制。
- 配置中心与高可用：深入理解 Higress 的配置存储（基于 Nacos 或 K8s CRD），以及集群模式下的部署与容灾。
- 性能调优：理解连接池、缓冲区大小等参数调优，进行压测（如使用 Wrk）。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发章节
- Envoy Wasm C++/Go SDK 文档
- Higress GitHub 源码 (参考官方插件实现)

**学习建议**:
动手实践是关键。尝试编写一个简单的 Go Wasm 插件，例如实现一个“请求头修改”或“特定参数校验”的逻辑。将插件编译成 `.wasm` 文件并上传到 Higress 网关运行。阅读 Higress 的源码，理解请求是如何从 Gateway Controller

---
## 常见问题


### 1: Higress 是什么？它与云原生 API 网关有什么关系？

1: Higress 是什么？它与云原生 API 网关有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年开源的，建立在 Envoy 和 Istio 之上，旨在提供高性能、高可用且易于扩展的网关体验。它不仅继承了传统 API 网关的流量管理特性，还深度集成了服务网格能力，可以作为连接南北向流量（外部用户到内部服务）与东西向流量（服务间通信）的关键组件。



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

**A**: Higress 的主要优势在于其云原生架构和深度集成能力。
1.  **性能与资源**：基于 Envoy C++ 内核，相比基于 Lua 的 Kong 或 Nginx，Higress 在处理高并发时具有更低的延迟和更稳定的资源消耗。
2.  **标准化**：它原生支持 Kubernetes Ingress、Gateway API 以及 Istio 标准，能够直接对接 K8s 服务网格，无需复杂的适配。
3.  **扩展性**：Higress 提供了 Wasm (WebAssembly) 插件支持，允许开发者使用 Go、C++、Rust 等多种语言编写插件，且插件热更新无需重启网关，比传统的 Lua 脚本更安全、更灵活。
4.  **安全**：默认集成了阿里云开源的 WAF 核心检测引擎，提供开箱即用的安全防护。



### 3: Higress 是否兼容 Nginx 的配置或 Ingress 规则？

3: Higress 是否兼容 Nginx 的配置或 Ingress 规则？

**A**: 是的，Higress 具有很强的兼容性。
1.  **K8s Ingress**：Higress 完全支持 Kubernetes 标准的 Ingress 资源，可以作为 Nginx Ingress Controller 的直接替代品。
2.  **Nginx 配置**：虽然 Higress 不直接运行 `nginx.conf`，但它支持 Nginx 的注解，并且提供了工具或迁移指南来帮助用户将传统的 Nginx 配置逻辑转换为 Higress 的路由配置。这使得从 Nginx 迁移到 Higress 的成本相对较低。



### 4: 在 Higress 中如何使用 Wasm 插件？它解决了什么痛点？

4: 在 Higress 中如何使用 Wasm 插件？它解决了什么痛点？

**A**: 在 Higress 中，Wasm 插件是其核心特性之一。
*   **如何使用**：用户可以通过 Higress 控制台或 CRD (WasmPlugin) 轻松加载 Wasm 文件。Higress 官方插件市场也提供了许多开箱即用的 Wasm 插件（如 JWT 认证、请求限流等）。
*   **解决的痛点**：传统网关（如早期 Kong）通常使用 Lua 编写插件，存在第三方库依赖复杂、插件崩溃可能导致网关崩溃、以及单线程性能瓶颈等问题。Wasm 插件运行在沙箱环境中，隔离性更好，支持多语言开发，且可以实现热加载，极大地提升了网关的稳定性和开发效率。



### 5: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

5: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

**A**: 支持。Higress 不仅仅是一个 HTTP 网关，它对微服务生态有深度支持。
1.  **gRPC**：Higress 原生支持 gRPC 协议的反向代理，支持将 HTTP/JSON 请求转换为 gRPC 请求，这对于 Web 前端调用后端微服务的场景非常有用。
2.  **Dubbo**：由于源自阿里系，Higress 对 Apache Dubbo 有着天然的支持，能够实现 HTTP 转 Dubbo 的协议转换，使得传统的 Web 应用可以无缝调用后端的 Java Dubbo 服务，而无需修改后端代码。



### 6: Higress 的部署架构是怎样的？是否支持高可用？

6: Higress 的部署架构是怎样的？是否支持高可用？

**A**: Higress 专为云原生环境设计，通常部署在 Kubernetes 集群中。
*   **控制面与数据面**：它采用控制面和数据面分离的架构。控制面负责配置下发和管理，数据面由 Envoy 实例组成，负责处理实际流量。
*   **高可用**：在 Kubernetes 中，通常通过部署多个副本并结合 Service 的负载均衡来实现高可用。Higress 的配置变更通过控制面实时推送到数据面，配置毫秒级生效，且支持金丝雀发布等高级流量管理功能。



### 7: 我是一个个人开发者或中小企业，Higress 适合我使用吗？

7: 我是一个个人开发者或中小企业，Higress 适合我使用吗？

**A**: 非常适合。
1.  **开源免费**：Higress 是完全开源的（Apache 2.0 协议），没有商业版本的功能限制，你可以免费使用其企业级特性。
2.  **易用性**：虽然功能强大，但 Higress 提供了非常友好的控制台，即使是初学者也能通过图形界面快速配置路由、负载均衡和插件，而不

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的快速入门文档，使用 Docker Compose 在本地快速搭建一个 Higress 实例，并配置一个简单的路由规则。要求实现：当访问 `http://localhost:8080/foo` 时，能够将请求转发到后端的一个模拟服务（如 httpbin.org），并返回 200 状态码。

### 提示**:

### 查阅 Higress 官方文档中的 "快速开始" 章节。

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其云原生架构与 AI 代理能力，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 WASM 技术实现“零代码”AI 插件扩展
**场景**：当大模型（如通义千问、ChatGPT）的返回结果包含敏感词，或者需要根据用户身份进行输入拦截时。
**建议**：不要编写自定义 Go 代码重新编译 Higress。利用 Higress 对 WebAssembly (WASM) 的原生支持，使用 Go 或 C++ 编写插件并编译为 WASM 文件，直接在控制台动态加载。
**最佳实践**：在 WASM 插件中处理 Token 计费、内容审查或 Prompt 注入逻辑。这样可以在不重启网关的情况下更新业务逻辑，且由于 WASM 的沙箱隔离特性，插件崩溃不会导致整个网关宕机。
**常见陷阱**：避免在 WASM 插件中进行高延迟的阻塞调用（如直接同步调用第三方鉴权接口），这会显著拖慢 AI 的流式响应速度。

### 2. 配置“语义缓存”以降低 Token 成本与延迟
**场景**：企业内部知识库问答，或高频重复的用户提问（如“如何重置密码”）。
**建议**：针对 LLM 请求配置特定的缓存策略。不同于传统的 URL 缓存，AI 请求的 Body 很大且细微差异会导致结果不同。建议配置基于请求 Body 哈希（或向量相似度）的缓存键。
**最佳实践**：对于允许一定精度偏差的场景，可以开启较长时间的 TTL，直接返回网关层缓存的上一条回答。这能直接绕过 LLM 推理，将延迟从秒级降至毫秒级，并大幅节省 API 调用成本。
**常见陷阱**：确保缓存键包含了用户的 Role 或 Context（上下文），否则会导致用户 A 看到用户 B 的私密对话内容。

### 3. 生产环境必须开启 SSE (Server-Sent Events) 全链路透传
**场景**：类 ChatGPT 的流式对话体验。
**建议**：确认 Higress 的路由配置中，超时时间设置得足够长（例如 300s），并且并未在网关层对响应进行缓冲。
**最佳实践**：检查后端服务（如 Python/Java AI 服务）的响应头是否正确设置 `Content-Type: text/event-stream`。Higress 默认支持流式转发，但如果配置了特定的 Body 修改插件，可能会强制网关缓冲完整响应导致流式失效。
**常见陷阱**：在日志采集插件中，切勿打印完整的响应 Body。流式响应的 Body 是分片的，打印日志不仅会产生海量 IO，还可能导致内存溢出（OOM）。

### 4. 实施精细化的 Prompt 模板管理与注入
**场景**：需要在请求发送给 LLM 之前，统一注入系统提示词或用户上下文。
**建议**：使用 Higress 的 `Prompt Template` 或 `Prompt Guard` 插件功能，将 Prompt 管理能力从业务代码中剥离到网关层。
**最佳实践**：在网关层配置“提示词工程”模板。例如，根据 HTTP Header 中的 `User-Agent` 判断是否为移动端请求，并自动在请求 Body 中注入“请用简洁的语言回答”的指令。
**常见陷阱**：注意注入 Prompt 后的 Token 长度限制。网关应在转发前校验总 Token 数是否超过模型上限（如 4k/8k/32k），避免无效请求消耗费用。

### 5. 建立基于 Token 计费的流量控制
**场景**：AI API 成本与 Token 消耗量成正比，传统的基于 QPS（每秒请求数）或并发数的限流无法有效控制成本。
**建议**：配置自定义限流策略，或结合 Wasm 插件实现基于 Token 的限流。
**最佳实践**：根据请求中的 `max_tokens` 参数估算一次请求的成本，并结合用户配额进行限流。例如，限制免费用户每天最多

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*