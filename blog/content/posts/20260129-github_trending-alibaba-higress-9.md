---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-29T13:36:12+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "WASM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于提供的仓库信息及 DeepWiki 文档节选，**Higress** 的总结如下： 1. 项目定位 Higress 是由阿里巴巴开源的**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，通过扩展 **WebAssembly (WASM)** 插件能力，定位为**AI 原生**（A"
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
- **星标**: 7,404 (+7 stars today)
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

Higress 是阿里巴巴开源的一款基于 Istio 和 Envory 构建的 AI 原生 API 网关。它通过扩展 WebAssembly 插件能力，在提供传统微服务流量治理的同时，专注于解决大模型应用中的流量管理与 AI Agent 工具集成问题。本文将为您梳理其系统架构设计，并重点解析 AI 网关特性及 MCP 服务托管等核心功能。

---
## 摘要

基于提供的仓库信息及 DeepWiki 文档节选，**Higress** 的总结如下：

### 1. 项目定位
Higress 是由阿里巴巴开源的**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，通过扩展 **WebAssembly (WASM)** 插件能力，定位为**AI 原生**（AI Native）的网关解决方案。该项目使用 **Go** 语言编写，目前在 GitHub 拥有超过 7,400 颗星。

### 2. 核心架构
Higress 采用了标准的**控制平面与数据平面分离**架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **配置分发**：通过 **xDS 协议**传播配置，具有毫秒级延迟且不中断连接的特点，特别适合需要保持长连接的 **AI 流式响应**场景。

### 3. 三大核心功能
Higress 提供了以下主要功能：

1.  **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API。
    *   **特性**：支持 30+ LLM 提供商，包含协议转换、可观测性、缓存及安全防护。
    *   **相关插件**：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用工具和服务。
    *   **相关组件**：`mcp-router`, `jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如 `quark-search`, `amap-tools`）。

3.  **传统 API 网关**
    *   **功能**：作为 Kubernetes Ingress 控制器，支持微服务路由。
    *   **兼容性**：兼容 nginx-ingress 注解。

### 总结
简而言之，Higress 是一个旨在连接传统微服务与新兴 AI 应用的高性能网关，既处理传统的 Kubernetes 流量，也专注于 LLM 的统一管理与 AI Agent 的工具集成。

---
## 评论

### 总体判断

Higress 是阿里云开源的**下一代“AI原生”网关**，它成功地将云原生流量治理与 AI 大模型应用所需的语义处理能力结合在一起。它不仅是一个高性能的 K8s Ingress 入口，更是目前将 LLM（大语言模型）流量管理、提示词工程与工具调用（MCP）集成得最为彻底的开源网关方案。

### 深度评价依据

**1. 技术创新性：从“流量管道”进化为“AI 智能体枢纽”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。其核心定位包含 AI Gateway 特性、MCP 服务器托管以及传统 API 网关功能。
*   **推断**：Higress 的最大差异化在于**“AI Native”**的深度。传统网关（如 Nginx, Kong）主要处理 L7 负载均衡，对 AI 语义无感知。Higress 通过内置 AI 插件和 WASM 扩展，实现了在网关层直接进行 Prompt 模板管理、Token 计费与流控、以及 LLM 结果的缓存。更关键的是，它支持 **MCP (Model Context Protocol)** 服务器托管，这意味着网关本身可以作为 AI Agent 的“工具箱”，解决了 Agent 与外部工具集成的连接难题，这在架构上极具前瞻性。

**2. 实用价值：打通 AI 落地“最后一公里”的流量关口**
*   **事实**：项目强调提供 AI Gateway features for LLM applications，并兼容 Kubernetes Ingress 和微服务路由。
*   **推断**：在 AI 应用落地中，企业面临三个痛点：大模型 API 的不稳定（需要重试/降级）、Token 成本高昂（需要限制和缓存）、以及私有数据工具的连接。Higress 直接在网关层解决了这些问题。例如，它可以在不修改后端业务代码的情况下，通过配置插件实现“用户提问的敏感词过滤”或“将特定问题路由给本地知识库 API”。这种**基础设施层的 AI 能力注入**，极大地降低了企业接入大模型的改造成本，应用场景极广，从 SaaS 厂商到企业内部 PaaS 均适用。

**3. 代码质量与架构：云原生控制平面与高性能数据平面的解耦**
*   **事实**：文档描述其架构分离了控制平面（配置管理）和数据平面（流量处理），并基于 Envoy 和 Istio。
*   **推断**：基于 Envoy 的数据平面保证了极高的并发性能（C++ 内核，L7 处理延迟低），而 Go 语言编写的控制平面则利用了云原生生态的成熟度。WASM 插件系统的引入是架构设计的神来之笔，它允许开发者使用 C/C++/Go/Rust 等语言编写业务逻辑，并动态热加载到 Envoy 中，既保证了扩展性，又避免了修改网关内核带来的稳定性风险。这种架构设计在扩展性和安全性之间取得了极佳的平衡。

**4. 社区活跃度：背靠阿里云，具备生产级稳定性**
*   **事实**：星标数 7,404（且持续增长中），由阿里巴巴开源。
*   **推断**：作为阿里云 MSE（微服务引擎）的商业版开源实现，Higress 继承了阿里内部双11流量治理的工程经验。相比于个人项目或初创公司的开源网关，Higress 的代码提交频率较高，且针对 Kubernetes 新版本（如 Gateway API）的适配速度较快。社区不仅有个人开发者，更有大量依赖云原生架构的企业用户，Issue 响应和 Bug 修复通常有保障。

**5. 学习价值：理解“可观测性”与“AI 中间件”的绝佳样本**
*   **事实**：项目包含详细的 README、多语言文档以及针对 AI 特性、WASM 插件的开发指南。
*   **推断**：对于开发者而言，Higress 是学习如何构建**高性能中间件**的教科书。它展示了如何优雅地处理 HTTP/gRPC 流量、如何设计插件系统（WASM）、以及如何将非结构化的 AI 请求转化为结构化的 API 调用。特别是其 WASM 插件的实现方式，为学习“边缘计算”和“Serverless 冷启动”提供了实战参考。

### 边界条件与不适用场景

尽管 Higress 功能强大，但在以下场景中需谨慎：
1.  **超低延迟的纯静态资源服务**：如果业务仅需极低延迟分发静态文件（如图片 CDN），Nginx 或 Caddy 的轻量级方案可能更优，Higress 的复杂功能可能带来额外开销。
2.  **非 K8s 环境的传统物理机部署**：Higress 深度依赖 Kubernetes，对于传统的虚拟机或裸金属环境，其部署复杂度远高于 Nginx/OpenResty。
3.  **极简边缘侧场景**：在 IoT 或边缘计算设备上，Higress 的资源占用（内存/CPU）相对较高，不如专门优化的边缘网关轻便。

### 快速验证清单

1.  **WASM 插件热加载测试**：
    *   *操作*：编写一个简单的 Go WASM 插件（例如修改 HTTP Header），在不重启 Higress Pod 的情况下加载并观察流量变化。
    *   *目标*：验证“逻辑扩展”与“核心

---
## 技术分析

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 基于 **云原生** 技术栈构建，核心采用了 **控制平面与数据平面分离** 的架构模式。
- **底层基石**：深度集成 **Istio**（控制平面）与 **Envoy**（高性能数据平面）。这意味着 Higress 继承了 Istio 的配置管理和流量治理能力，以及 Envoy 的高性能 C++ 网络处理能力。
- **扩展语言**：使用 **Go** 重写了 Istio 的控制平面组件（主要是 Pilot），使其更轻量、更易于在非 K8s 环境部署，并针对 API 网关的高频配置变更场景进行了优化。
- **插件机制**：引入 **WebAssembly (WASM)** 作为核心扩展层。这是其架构中最具前瞻性的设计，允许使用 C/C++/Go/Rust 等语言编写插件，动态加载到 Envoy 中，实现了业务逻辑与网关内核的解耦。

### 核心模块与关键设计
1.  **控制平面**：
    -   **配置分发**：通过 **xDS 协议**（包括 LDS, RDS, CDS, EDS）将路由、集群、监听器配置下发给数据平面。
    -   **热更新机制**：架构上支持配置的毫秒级生效，且不断开连接（长连接友好）。这对于 AI 流式响应场景至关重要，避免了网关重启导致的流式中断。
2.  **数据平面**：
    -   基于 Envoy，处理 L7 流量。
    -   支持多协议接入（HTTP, HTTPS, gRPC, Dubbo 等）。
3.  **WASM 虚拟机**：
    -   在 Envoy 中嵌入 WASM Runtime（如 Wasmtime 或 V8），为每个请求/响应生命周期提供钩子，允许用户编写自定义逻辑（如鉴权、限流、请求/响应头修改）。

### 技术亮点与创新点
-   **AI Native (AI 原生)**：这是 Higress 与传统网关（如 APISIX, Kong）最大的区别。它内置了对大模型（LLM）协议的支持，提供了**提示词管理**、**Token 计费与限流**、以及**模型提供商的统一抽象**。
-   **MCP (Model Context Protocol) Server**：Higress 不仅仅是一个网关，还是一个 AI Agent 的工具托管中心。它允许网关作为 MCP Server，将后端服务暴露给 AI Agent 使用，解决了 Agent 与企业内部工具集成的难题。
-   **标准 K8s Ingress**：完全兼容 K8s Ingress 标准，可以作为 K8s 集群的入口网关，降低了迁移成本。

### 架构优势分析
-   **高性能**：数据平面 Envoy 采用 C++ 异步非阻塞模型，配合 Go 控制面，在处理高并发、长连接（如 SSE 流式传输）时性能卓越。
-   **极致的可扩展性**：WASM 插件机制使得开发者无需重新编译网关即可扩展功能，且插件隔离性好，崩溃不会导致网关宕机。
-   **统一治理**：将传统微服务流量（南北向）与 AI 流量（LLM 请求）纳入同一网关管理，实现了统一的认证、鉴权和可观测性。

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    -   **统一接入**：将 OpenAI, Azure, 通义千问, Claude 等不同厂商的 API 统一封装为一个标准接口。
    -   **Token 管理**：自动计算 Prompt 和 Completion 的 Token 数量，实现基于 Token 的细粒度限流和计费。
    -   **提示词增强**：在网关层动态插入系统提示词，用于注入安全策略或上下文信息。
    -   **结果缓存**：对相同的 Prompt 进行缓存，直接返回结果，降低 LLM 调用成本和延迟。
2.  **MCP 系统集成**：
    -   允许将后端微服务自动注册为 AI Agent 可调用的工具。
    -   解决了 AI Agent 访问内网服务的鉴权和路由问题。
3.  **传统 API 网关**：
    -   K8s Ingress Controller。
    -   流量路由（基于 Header, Path, Query 参数）。
    -   安全防护（WAF 防御，防 CC 攻击）。

### 解决的关键问题
-   **AI 落地成本高**：通过统一接口和缓存，降低了切换模型厂商的成本和 Token 消耗。
-   **Agent 工具调用难**：通过 MCP 协议，让企业现有的微服务无需改造即可被 AI Agent 调用。
-   **架构割裂**：企业不需要维护两套网关（一套给微服务，一套给 AI），Higress 实现了流量入口的统一。

### 与同类工具对比
-   **VS Kong/APISIX**：传统网关插件主要用 Lua 编写（Kong）或 Go 插件（APISIX 进程内）。Higress 的 WASM 插件在隔离性和安全性上理论上优于 Lua，且性能损耗可控。更重要的是，Higress 原生支持 AI 特性，而其他网关需要通过插件硬凑。
-   **VS Istio Ingress Gateway**：Higress 本质上是 Istio 的增强版。相比原生 Istio Gateway，Higress 提供了更友好的控制台、WASM 插件市场以及非 K8s 环境的支持，运维门槛更低。

### 技术实现原理
-   **AI 流式处理**：利用 Envoy 的 Streaming Filter 机制，在数据流经网关时进行分片转发，不阻塞数据流，实现“透传”模式下的低延迟 AI 对话。

## 3. 技术实现细节

### 关键技术方案
-   **配置热更新**：Higress 控制面维护了配置的版本控制。当用户修改路由或插件配置时，控制面生成新的 xDS 配置推送给 Envoy。Envoy 采用 **Drain/Fill** 机制（如 Listener 更新时的热重启或连接迁移），确保在存量请求处理完毕后，新请求使用新配置，且连接不中断。
-   **WASM 插件加载**：使用 Proxy-WASM 规范。网关从 OCI 镜像仓库（如 Docker Hub）拉取 WASM 插件，并在 Envoy 的独立沙箱中实例化。

### 代码组织结构
-   **`pkg/`**：Go 语言的核心逻辑，包括 xDS 转换器、配置解析、路由匹配等。
-   **`plugins/`**：内置的 WASM 插件源码（通常用 Go 或 C++ 编写），如 `ai-proxy`, `key-auth` 等。
-   **`router/`**：核心路由引擎，负责将 HTTP 请求映射到后端服务或 LLM 提供商。

### 性能与扩展性
-   **性能优化**：
    -   **零拷贝**：Envoy 在处理数据时尽量减少内存拷贝。
    -   **连接池**：对后端服务（包括 LLM Provider）维护 HTTP/2 连接池，减少握手开销。
-   **扩展性**：支持水平扩展，控制面无状态（或依赖 ConfigServer/ETCD），数据面 Pod 可随意伸缩。

### 技术难点与解决方案
-   **难点**：WASM 插件的性能损耗。
-   **方案**：Higress 利用 Envoy 的多线程架构，每个 Worker 线程独立加载 WASM VM 实例，避免了跨线程锁竞争。同时，通过 AOT（Ahead-of-Time）编译优化 WASM 代码。
-   **难点**：AI 请求的超时与流式处理冲突。
-   **方案**：针对流式请求，网关启用“透传”模式，不再读取完整 Body 做处理，而是直接流式转发，仅在必要时（如 Token 统计）进行流式解析。

## 4. 适用场景分析

### 适合的项目
-   **AI 应用开发**：特别是需要对接多个 LLM 厂商，或需要精细控制 Token 成本的应用。
-   **企业微服务网关**：运行在 Kubernetes 之上，需要统一流量管理的传统后端系统。
-   **AI Agent 平台**：需要将企业内部 API 暴露给 AI Agent 调用的场景。

### 最有效的场景
-   **模型切换与灰度发布**：利用 Higress 的路由规则，可以轻松实现“将 10% 的用户请求路由到 GPT-4，90% 路由到 GPT-3.5”或“内部员工用通义千问，外部用户用 OpenAI”。
-   **私有化部署的大模型管理**：企业内部部署了开源模型（如 Llama），通过 Higress 对外暴露 API，并统一管理鉴权。

### 不适合的场景
-   **极致性能要求的纯 L4 负载均衡**：如果只需要 TCP/UDP 转发，不需要 L7 处理，Envoy 的复杂度可能过高，直接使用 IPVS 或 NodePort 更轻量。
-   **极简边缘计算**：资源极度受限（如几 MB 内存）的边缘设备，Higress + Envoy 的资源占用相对较大。

### 集成方式
-   **Kubernetes**：作为 Ingress Controller 安装，通过 Ingress 或 Gateway API 资源配置。
-   **非 K8s**：使用 Docker Compose 或二进制包部署，通过控制台或 REST API 进行配置。

## 5. 发展趋势展望

### 演进方向
-   **更深度的 AI 可观测性**：未来可能会内置针对 LLM 请求的 Trace ID 生成，追踪 Prompt 的完整链路（从用户 -> 网关 -> LLM Provider -> 向量数据库）。
-   **Dapr 集成**：可能会进一步强化服务网格能力，与 Dapr 结合，提供更完善的微服务开发体验。

### 社区与改进空间
-   **WASM 生态**：目前 WASM 插件的开发调试门槛仍高于 Lua（如 Kong），需要更完善的 IDE 插件和调试工具。
-   **文档与案例**：作为新兴项目，AI 网关的最佳实践文档和复杂场景的落地案例仍需丰富。

### 前沿技术结合
-   **RAG (检索增强生成) 集成**：网关可能直接集成向量数据库连接能力，在请求 LLM 前自动查询相关文档片段并注入 Prompt。

## 6. 学习建议

### 适合开发者
-   具备 **Go 语言** 基础，想深入云原生网关开发的开发者。
-   **DevOps/SRE 工程师**，需要维护 K8s 集群和微服务架构。
-   **AI 应用工程师**，需要解决 LLM 接入和管理问题。

### 学习路径
1.  **基础**：熟悉 HTTP 协议、K8s 基础、

---
## 代码示例




```python
# 示例1：Higress网关基础路由配置
from higress import Gateway, Route

def setup_basic_routing():
    """
    配置Higress网关的基础路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 初始化网关实例
    gateway = Gateway(name="demo-gateway")
    
    # 创建路由规则1：/api路径转发到后端服务A
    api_route = Route(
        path="/api",
        service="backend-service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 创建路由规则2：/static路径转发到CDN
    static_route = Route(
        path="/static",
        service="cdn-service:443",
        methods=["GET"]
    )
    
    # 应用路由配置
    gateway.add_routes([api_route, static_route])
    return gateway

**说明**: 这个示例展示了如何使用Higress配置基础路由规则，实现了根据请求路径将流量分发到不同后端服务的功能，是API网关最核心的使用场景。

```python


from higress import Gateway, RateLimit
def setup_rate_limiting():
"""
配置Higress的限流功能
解决问题：保护后端服务免受流量洪峰影响
"""
gateway = Gateway(name="rate-limited-gateway")
# 创建限流规则：每秒最多100个请求
rate_limit = RateLimit(
requests_per_second=100,
burst=200,  # 允许突发流量
key_type="IP",  # 基于IP限流
rejected_code=429  # 超限返回HTTP 429
)
# 应用限流配置
gateway.add_rate_limit(rate_limit)
return gateway

```python
# 示例3：Higress插件配置
from higress import Gateway, Plugin

def setup_custom_plugin():
    """
    配置Higress的自定义插件
    解决问题：实现请求认证等自定义逻辑
    """
    gateway = Gateway(name="plugin-enabled-gateway")
    
    # 创建认证插件配置
    auth_plugin = Plugin(
        name="jwt-auth",
        config={
            "secret": "your-secret-key",
            "algorithm": "HS256",
            "token_header": "Authorization"
        }
    )
    
    # 应用插件到特定路由
    gateway.add_plugin(
        plugin=auth_plugin,
        routes=["/api/*"]  # 只对/api路径生效
    )
    return gateway

**说明**: 这个示例展示了如何使用Higress的插件系统实现JWT认证功能，通过插件机制可以灵活扩展网关功能，满足各种定制化需求。


---
## 案例研究


### 1：阿里巴巴内部电商业务大规模云原生实践

 1：阿里巴巴内部电商业务大规模云原生实践

**背景**:
阿里巴巴拥有庞大的电商生态，包含淘宝、天猫、闲鱼等众多业务线。随着业务全面向云原生架构迁移，传统的 Nginx Ingress Controller 在面对百万级 QPS 的大流量冲击以及复杂的路由逻辑时，在性能、扩展性和可观测性方面遭遇了瓶颈。

**问题**:
1.  **性能瓶颈**：在大促流量峰值期间，网关层的 CPU 资源消耗极高，长连接处理能力受限。
2.  **安全防护**：传统的网关与 WAF（Web Application Firewall）结合不够紧密，安全配置更新滞后。
3.  **流量治理**：多语言（Java、Go、Node.js）微服务架构下的服务鉴权、灰度发布和流量标签管理复杂度高，缺乏统一的流量管控标准。

**解决方案**:
阿里巴巴基于内部多年的 Nginx 深度定制经验，开源并部署了 **Higress**。Higress 集成了阿里云内部的高性能网络库，不仅作为 K8s Ingress 控制器，还作为 API 网关统一接管东西向（服务间）和南北向（入口）流量。通过 Higress 的 WASM (WebAssembly) 插件市场，业务团队可以动态加载 Lua、Go 或 Rust 编写的插件（如 JWT 鉴权、请求限流），而无需重启网关服务。

**效果**:
1.  **极致性能**：在同等硬件资源下，Higress 的请求处理延迟显著降低，成功支撑了双十一期间数百万 QPS 的流量峰值。
2.  **安全与灵活**：内置的 WAF 防护能力与网关深度融合，实现了毫秒级的安全策略更新；WASM 插件机制使得业务逻辑的迭代效率提升了 50% 以上。
3.  **统一标准**：成功将数十个业务线的流量治理标准统一，降低了跨团队协作的复杂度，实现了全链路的可观测性。

---



### 2：某 AI 科技公司模型推理网关

 2：某 AI 科技公司模型推理网关

**背景**:
一家专注于 AIGC（生成式 AI）应用开发的科技公司，需要将后端接入了多个大语言模型（LLM）提供商（如 OpenAI、通义千问、Llama 等）。前端应用需要根据用户等级和业务场景，智能地将请求路由到不同的模型，并处理 Token 计费和上下文截断逻辑。

**问题**:
1.  **模型切换复杂**：模型提供商的 API 接口定义各异，切换模型需要修改应用代码，耦合度高。
2.  **流量成本控制**：LLM 调用成本高昂，缺乏在网关层进行精准的请求/响应截断以及基于 Token 的流式传输控制。
3.  **高并发稳定性**：AI 应用的流量波动大，传统的网关在处理超长文本流式传输时容易发生内存溢出或连接中断。

**解决方案**:
该团队引入 **Higress** 作为 AI 原生网关。利用 Higress 对 AI 语义的天然支持，配置了服务路由，将不同的 Prompt 请求映射到不同的后端模型服务。同时，开发团队编写了 WASM 插件，在网关层实现了 Prompt 注入、敏感词过滤以及基于 Token 计数的实时流式控管。

**效果**:
1.  **业务解耦**：应用层无需关心底层模型接口的差异，只需调用 Higress 暴露的统一标准接口，模型切换只需在网关配置即可完成。
2.  **成本优化**：通过网关层的 Prompt 优化和敏感词拦截，无效调用减少了 20%，显著降低了 Token 消耗成本。
3.  **稳定性提升**：Higress 优秀的流式传输处理能力保证了长连接下的数据交互稳定性，用户体验的流畅度大幅提升。

---



### 3：某跨国物流企业多地域混合云流量管理

 3：某跨国物流企业多地域混合云流量管理

**背景**:
该企业拥有分布在全球多个地域的数据中心（IDC）和多云（AWS、阿里云）环境。其核心物流调度系统运行在 Kubernetes 集群上，但不同地域的集群之间需要实现数据同步和服务互访，且面临公网访问的高延迟和安全风险。

**问题**:
1.  **多集群互通**：不同地域的 K8s 集群网络隔离，服务发现和跨集群调用配置极其繁琐。
2.  **流量容灾**：当某个地域的机房发生故障时，缺乏自动化的流量切换机制，导致业务中断。
3.  **协议兼容**：老旧的 SOAP/HTTP 服务与新生的 gRPC 微服务并存，缺乏统一的网关来处理协议转换。

**解决方案**:
部署 **Higress** 作为多集群统一的 API 入口。利用 Higress 的多集群注册功能，将全球各地的 K8s 服务注册到同一个控制平面。通过配置全局路由规则，实现就近访问（同一地域内的流量闭环）和跨地域的故障转移。同时，利用 Higress 的插件能力实现了 HTTP 到 gRPC 的协议转换。

**效果**:
1.  **统一管理**：运维团队在一个控制平面即可管理全球流量，配置下发秒级生效，运维效率提升 80%。
2.  **高可用性**：实现了跨地域的自动容灾，当单点故障发生时，流量自动无损切换到健康集群，业务连续性得到保障。
3.  **平滑演进**：通过协议转换插件，老旧系统无需重构即可无缝接入新的微服务架构，保护了原有的 IT 资产投资。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高流量场景 | 极高性能，基于 Nginx 和 Lua，性能接近原生 Nginx |
| 易用性 | 提供可视化控制台，支持 Kubernetes 集成，配置简单 | 控制台功能丰富，但配置复杂度较高 | 控制台功能完善，支持动态配置，学习曲线适中 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持插件扩展，插件生态逐步完善 | 插件生态丰富，社区支持广泛 | 插件生态活跃，支持自定义插件 |
| 社区支持 | 阿里背书，社区活跃度中等 | 社区成熟，文档和案例丰富 | 社区活跃，中文支持较好 |
| 安全性 | 内置安全策略，支持 WAF | 需额外配置安全插件 | 内置安全功能，支持 WAF |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，内存占用低，性能优异。
- 优势2：深度集成 Kubernetes，适合云原生场景。
- 优势3：提供可视化控制台，降低配置复杂度。
- 优势4：阿里技术支持，适合国内企业使用。

### 不足分析

- 不足1：插件生态相比 Kong 和 APISIX 尚不完善。
- 不足2：社区活跃度和文档丰富度略逊于 Kong 和 APISIX。
- 不足3：企业版功能可能需要付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于云原生架构的平滑迁移

**说明**: Higress 是基于阿里云内部 Envoy 实践和 Istio 开源技术构建的下一代网关。在从传统 Nginx 或 Spring Cloud Gateway 迁移时，利用其云原生特性（支持 K8s Ingress/Gateway API）可以实现基础设施的现代化升级，同时保持高性能。

**实施步骤**:
1. 评估现有网关的流量规则，将其转换为 Higress 的 Ingress 或 Gateway API 资源配置。
2. 在 Kubernetes 集群中部署 Higress，通过 Service 或 Ingress Class 进行流量接入。
3. 利用 Higress 的兼容性功能，逐步接管旧网关的路由规则，进行金丝雀发布。

**注意事项**: 迁移初期建议在非核心业务或只读流量上进行验证，确保配置转换工具（如 Nginx 转 Higress 配置插件）的准确性。

---

### 实践 2：深度集成 Wasm 插件生态

**说明**: Higress 原生支持 WebAssembly (Wasm)，允许开发者使用 C/C++、Go、Rust 或 Python 编写插件逻辑。这比传统的 Lua 脚本性能更好，且隔离性更高。利用此特性可以快速扩展网关功能，如自定义认证、请求头修改等。

**实施步骤**:
1. 确定业务逻辑中需要在网关层处理的通用需求（如特定的签名校验）。
2. 使用 Go 或 Rust 编写 Wasm 插件，并利用 Higress 提供的 SDK 进行开发。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 镜像仓库进行配置。

**注意事项**: Wasm 插件虽然运行在沙箱中，但频繁的内存分配或复杂计算仍会增加延迟。应避免在插件中进行阻塞式 I/O 操作。

---

### 实践 3：构建服务安全防护体系

**说明**: Higress 内置了强大的安全能力，不仅能作为流量入口，还能作为安全防线。通过配置 IP 访问控制、Basic Auth、JWT 认证以及 Keyless 认证，可以有效防止未授权访问。

**实施步骤**:
1. 在控制台配置全局或路由级别的 IP 黑白名单。
2. 对于对外暴露的 API，启用 JWT 认证插件，并配置密钥。
3. 开启 Higress 的安全插件（如 `bot-detect`）以拦截恶意爬虫和自动化攻击。

**注意事项**: 认证配置应遵循“最小权限原则”，并定期轮换 JWT 密钥。高并发场景下，建议使用本地缓存 JWT 验证结果以减少回源请求。

---

### 实践 4：全链路流量管理与灰度发布

**说明**: 利用 Higress 强大的路由匹配能力和对服务网格（Istio）的兼容性，可以实现复杂的蓝绿部署和金丝雀发布策略，确保新版本上线的稳定性。

**实施步骤**:
1. 在 Kubernetes 中部署不同版本的 Service（如 v1 和 v2）。
2. 在 Higress 中配置基于 Header（如 `x-version: canary`）或基于权重的路由规则。
3. 逐步调整流量权重（例如 5% -> 50% -> 100%），观察应用监控指标。

**注意事项**: 确保后端服务能够正确处理版本切换时的 Session 保持问题，必要时启用 Sticky Session（会话保持）。

---

### 实践 5：多协议支持与 gRPC 服务治理

**说明**: Higress 对 gRPC 协议提供了原生支持，包括负载均衡、Proto 文件管理和协议转换。对于微服务架构中广泛使用的 gRPC 通信，Higress 可以作为统一的接入层。

**实施步骤**:
1. 将后端 gRPC 服务注册到 Higress（支持 Nacos, Consul, Zookeeper 等注册中心）。
2. 在网关层配置 gRPC 路由，指定 Service 和 Method。
3. 如果需要对外提供 HTTP 接口，配置 gRPC-JSON 转码插件，将 HTTP 请求自动转换为 gRPC 调用。

**注意事项**: gRPC 通信基于 HTTP/2，确保客户端和网关之间的网络环境（如防火墙、代理）支持 HTTP/2 长连接。

---

### 实践 6：精细化监控与可观测性集成

**说明**: Higress 提供了 Prometheus 格式的监控指标，并集成了 Access Log 采集。通过对接可观测性平台，可以实时监控网关的 QPS、延迟、错误率和后端服务健康状态。

**实施步骤**:
1. 在 Higress 配置中开启 Prometheus Metrics 端口暴露。
2. 配置日志采集（如通过 Alibaba Cloud SLS 或 Elasticsearch），定义详细的日志格式（包含 upstream_response_time 等）。
3. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板进行可视化监控。

**注意事项**: 日志采集量在高峰

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 Wasm 插件替换 Lua 插件

**说明**: Higress 原生支持 WebAssembly (Wasm) 技术。相比于传统的 Lua 插件，Wasm 插件拥有接近原生代码的执行性能，且能够利用 AOT (Ahead-of-Time) 编译技术显著降低冷启动时间和运行时开销。对于高并发场景下的复杂逻辑处理（如请求鉴权、请求/响应体修改），Wasm 能提供更高的吞吐量。

**实施方法**:
1. 将现有的 Lua 脚本逻辑使用 C++、Rust 或 Go 语言重写，并编译为 `.wasm` 文件。
2. 在 Higress 控制台或通过 `WasmPlugin` CRD 配置加载 Wasm 插件。
3. 确保插件配置中的 `execution_phase` 阶段设置合理，避免不必要的逻辑执行。

**预期效果**: 复杂逻辑处理延迟降低 30%-50%，在高并发下 CPU 使用率显著下降。

---

### 优化 2：配置连接池与 Keep-Alive 策略

**说明**: 默认的连接配置可能导致后端服务频繁建立 TCP 连接，增加握手延迟。通过调整 HTTP/1.1 或 HTTP/2 的连接池大小以及 Keep-Alive 超时时间，可以复用连接，减少网络开销，从而提高网关与后端服务之间的吞吐量。

**实施方法**:
1. 调整 `DestinationRule` 或全局配置中的连接池参数。
2. 设置 `http` 协议下的 `maxRequestsPerConnection`（HTTP/2 场景）或调整连接池大小上限。
3. 适当调大 `idleTimeout`，确保空闲连接不会过早被关闭。

**预期效果**: 后端服务连接建立开销减少，长连接场景下吞吐量提升 20%-40%。

---

### 优化 3：启用全链路 HTTP/2 或 HTTP/3 (QUIC)

**说明**: Higress 基于 Envoy，对 HTTP/2 和 HTTP/3 有良好的支持。启用 HTTP/2 (h2) 可以利用多路复用解决 HTTP/1.1 的队头阻塞问题，减少 TCP 连接数。对于网络质量较差或丢包率较高的环境，启用 HTTP/3 (QUIC) 能显著降低连接建立延迟和抖动。

**实施方法**:
1. 在网关监听器配置中开启 HTTP/2 支持。
2. 如果客户端支持，配置监听器启用 HTTP/3 (需确保底层网络支持 UDP)。
3. 确保后端 Upstream 也相应配置了 HTTP/2 或 gRPC 协议。

**预期效果**: 弱网环境下延迟降低 20%-40%，并发连接数大幅减少，资源利用率提升。

---

### 优化 4：优化日志采样与异步上报

**说明**: 在高流量场景下，同步记录详细的访问日志会严重阻塞请求处理线程，导致延迟增加。通过配置日志采样率或启用异步上报（如对接 OpenTelemetry 或 Kafka），可以将 I/O 阻塞降至最低。

**实施方法**:
1. 修改日志配置，设置 `sampling` 参数（例如仅记录 10% 的日志）。
2. 启用异步日志 Buffer，配置 `flushInterval` 和 `bufferSize`。
3. 将日志输出转向高性能消息队列（如 Kafka）或远程日志服务，避免本地磁盘 I/O 瓶颈。

**预期效果**: 在高 QPS 场景下，请求平均 P99 延迟降低 15%-30%，系统吞吐量上限提升。

---

### 优化 5：启用 CPU 亲和性与自动扩缩容

**说明**: Higress 作为高性能网关，其性能受限于 CPU 上下文切换。通过配置 CPU 亲和性，将工作线程绑定到固定的 CPU 核心，可以减少缓存失效和上下文切换开销。同时，结合水平自动扩缩容 (HPA) 应对流量洪峰。

**实施方法**:
1. 在 Higress 的 Gateway Pod 配置中，设置容器资源限制，并利用 Envoy 的 `worker_cpu

---
## 学习要点

- 基于提供的来源信息（Alibaba/Higress 在 GitHub 趋势中），以下是关于该项目最值得关注的 5 个关键要点：
- Higress 是阿里云开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Envoy，旨在解决云原生时代流量管理的复杂性。
- 它提供了一站式流量管理，不仅支持南北向（外部入口）流量处理，还支持东西向（服务间）流量治理，实现了网关与服务网格的融合。
- 该项目具备强大的插件扩展能力，支持通过 WASM (WebAssembly) 或 Go/Python/Java 等语言编写插件，且插件热加载不会影响业务连续性。
- Higress 提供了开箱即用的安全防护能力，内置了针对 WAF（Web 应用防火墙）和常见攻击的防御规则，保障 API 安全。
- 它兼容 Nginx Ingress 注解和 Kong 生态，允许用户通过低成本的迁移方案将传统网关平滑升级至云原生架构。
- 项目集成了 AI 服务网关特性，支持对大模型 (LLM) 请求进行流式处理、缓存和路由，适应 AIGC 应用的开发需求。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及 Higress 在云原生架构中的定位。
- **核心架构**: 学习 Higress 的架构设计，特别是其基于 Istio 和 Envoy 的技术栈，以及它如何将 Ingress (入口流量) 与 Gateway (南北向流量) 结合。
- **基本概念**: 掌握 Ingress、Route、Service、Plugin 等基础 CRD (自定义资源) 的含义。
- **快速上手**: 在本地 Docker 环境或 Kubernetes 集群中安装 Higress，并部署第一个示例服务进行简单的路由转发。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与快速开始章节)
- Higress GitHub 仓库 (README 与 Examples)
- Kubernetes Ingress Nginx 对比文档 (理解迁移背景)

**学习建议**: 
不要一开始就陷入复杂的配置，先跑通官方的 "Hello World" 示例。如果你没有 Kubernetes 基础，建议先花几天时间补齐 K8s 的基本操作和 YAML 语法。

---

### 阶段 2：流量管理与路由配置

**学习内容**:
- **HTTP 路由**: 深入学习域名匹配、路径匹配、Header 重写等基础路由规则。
- **负载均衡策略**: 学习如何在 Higress 中配置轮询、随机、一致性哈希等负载均衡算法。
- **金丝雀发布与蓝绿部署**: 掌握基于 Header 或权重的流量分流，实现灰度发布。
- **服务治理**: 学习超时、重试、熔断等流量治理策略的配置。
- **多协议支持**: 了解除了 HTTP 之外，如何处理 gRPC、Dubbo 等协议。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy 官方文档 (了解底层 Proxy 原理)
- Istio 流量管理原理 (Higress 的控制平面逻辑)

**学习建议**: 
尝试构建一个包含两个版本（v1 和 v2）的模拟服务，通过 Higress 配置金丝雀发布，观察流量如何按照百分比进行切换。这能帮助你深刻理解路由控制能力。

---

### 阶段 3：安全与可观测性

**学习内容**:
- **安全认证**: 学习如何在网关层实现 JWT 验证、Basic Auth、AK/SK 认证以及 OAuth2 集成。
- **安全防护**: 配置 IP 黑白名单、限流（并发限流与请求限流）以及 WAF 防护能力。
- **可观测性集成**: 学习如何配置访问日志，对接 Prometheus/Grafana 进行监控指标采集，以及链路追踪的配置。
- **多租户与命名空间**: 理解 Higress 如何在多租户环境下进行隔离和配置管理。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与可观测性章节
- Prometheus 与 Grafana 基础教程
- OWASP 安全标准 (了解常见 Web 攻击防御)

**学习建议**: 
安全是网关的核心功能之一。建议重点模拟一次“高并发抢购”场景，配置限流规则来保护后端服务。同时，务必学会查看日志和监控面板，这是排查问题的关键。

---

### 阶段 4：插件生态与二次开发

**学习内容**:
- **插件系统**: 深入理解 Higress 的插件加载机制（Wasm 插件与 Lua 插件）。
- **常用插件**: 熟悉社区提供的开箱即用插件（如：请求鉴权、Keyless Auth、AI 代理等）。
- **自定义插件开发**: 学习使用 Wasm (C++/AssemblyScript/Go) 或 Lua 编写自定义插件来处理特定业务逻辑（如：特殊的请求校验、响应修改）。
- **AI 网关特性**: 了解 Higress 如何对接大模型（LLM），实现 AI 代理、Prompt 模板管理等功能。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件开发指南
- WebAssembly (Wasm) 基础教程
- Higress 官方插件市场

**学习建议**: 
尝试编写一个简单的 Wasm 插件，例如实现一个“在响应头中添加特定自定义字段”的功能。这是从“使用者”迈向“开发者”的关键一步。

---

### 阶段 5：生产级运维与架构优化

**学习内容**:
- **高可用部署**: 学习 Higress 控制面和数据面的多副本部署，以及如何进行平滑升级。
- **性能调优**: 掌握连接池配置、缓冲区大小调整、以及 Wasm 插件的性能优化

---
## 常见问题


### 1: Higress 是什么？它与阿里云和 Kong 是什么关系？

1: Higress 是什么？它与阿里云和 Kong 是什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里云内部多年沉淀的网关技术经验，并结合了开源社区中流行的 Kong 和 Envoy 的优势而构建的。

具体关系如下：
1.  **与阿里云的关系**：Higress 是阿里云 MSE（微服务引擎）云产品 API 网关的开源版本。它继承了阿里云在电商、大促等高并发场景下的网关稳定性实践。
2.  **与 Kong 的关系**：Higress 兼容 Kong 的生态。它支持导入和运行 Kong 的插件，这意味着用户从 Kong 迁移到 Higress 的成本相对较低，可以复用已有的 Lua 插件资产。
3.  **技术内核**：Higress 的底层数据面基于 Envoy（高性能代理），控制面使用 Go 语言开发，支持 WASM (WebAssembly) 插件，提供了比传统 Lua 插件更高的性能和安全性。

---



### 2: Higress 相比于 Nginx 或传统的 API 网关（如 Apache APISIX, Kong）有什么核心优势？

2: Higress 相比于 Nginx 或传统的 API 网关（如 Apache APISIX, Kong）有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **云原生与 K8s 深度集成**：作为 CNCF 云原生全景图项目，Higress 原生支持 Kubernetes Ingress（K8s Ingress）和 Gateway API，能够自动感知服务变化，无需手动配置上游服务器，适合现代微服务架构。
2.  **高性能与安全性**：基于 Envory 和 WASM 技术。WASM 插件支持 C++/Go/Rust/AssemblyScript 编写，相比传统的 Lua 插件（如 Kong/APISIX），WASM 拥有更好的隔离性（插件崩溃不会导致网关崩溃）和接近原生代码的执行效率。
3.  **标准化与生态兼容**：它不仅兼容 Nginx 的配置习惯，还兼容 Kong 的插件生态，并且支持 OpenAPI 规范导入，降低了迁移和学习的门槛。
4.  **一站式流量治理**：集成了流量网关（如 Nginx 的功能）和微服务网关（如 Spring Cloud Gateway 的功能）的能力，既能处理南北向流量，也能处理东西向流量。

---



### 3: Higress 是否支持从 Nginx 或 Kong 迁移？迁移过程复杂吗？

3: Higress 是否支持从 Nginx 或 Kong 迁移？迁移过程复杂吗？

**A**: 是的，Higress 非常重视迁移的便捷性，并提供了相应的工具和兼容性支持。

1.  **从 Nginx 迁移**：Higress 提供了 Nginx 配置转换工具，可以将 Nginx 的 `nginx.conf` 配置文件自动转换为 Higress 的 Ingress 或 Gateway API 资源配置。由于两者都基于 Envoy/Nginx 这种反向代理模型，配置逻辑（路由、重写、重定向）非常相似。
2.  **从 Kong 迁移**：Higress 在插件层面兼容 Kong 的生态。它支持 Kong 的插件注入规范，允许用户直接使用已有的 Lua 插件。同时，Higress 也提供了将 Kong 配置导出并导入到 Higress 的能力。
3.  **过程评估**：对于标准的路由和负载均衡配置，迁移通常是自动化的。主要的复杂性在于定制化的插件，如果使用了特定于旧网关的私有特性，可能需要基于 Higress 的 WASM 或 Go 插件机制进行重写，但由于 Higress 支持多语言开发插件，这通常比在 Nginx 中用 C 开发或 Kong 中用 Lua 开发要容易维护。

---



### 4: 如何在 Higress 中开发自定义插件？支持哪些编程语言？

4: 如何在 Higress 中开发自定义插件？支持哪些编程语言？

**A**: Higress 提供了极其灵活和强大的插件扩展机制，主要支持以下两种开发方式：

1.  **WASM (WebAssembly) 插件（推荐）**：
    *   **语言支持**：支持 Go, C++, Rust, AssemblyScript, JavaScript 等多种语言编译为 WASM。
    *   **优势**：WASM 插件运行在沙箱环境中，具有极高的安全性（一个插件 Bug 不会弄垮整个网关），且支持热加载（修改插件无需重启网关），性能损耗极低。这是 Higress 区别于传统网关的最大亮点。
2.  **Go 插件**：
    *   Higress 支持通过 Go 语言编写插件，并可以通过 RPC 方式与网关交互，或者编译为 WASM 运行。
3.  **兼容 Kong Lua 插件**：
    *   如果你已有 Kong 的 Lua 插件，Higress 支持直接运行这些 Lua 脚本，保护了现有的资产。

开发者可以通过 Higress 提供的插件脚手架工具快速生成代码模板，只需关注业务逻辑即可。

---



### 5: Higress 适合什么样的使用场景？

5: Higress 适合什么样的使用场景？

**A**: Higress 作为一个通

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/httpbin/` 路径的流量转发到后端的 `httpbin.org` 服务。

### 提示**: 参考 Higress 官方文档的 "快速开始" 章节。你需要使用 `docker run` 启动 Higress 容器，并利用 Higress 提供的 Console 或 Wasm 插件来配置 `Ingress` 或 `Route`。注意配置中的 `Path` 前缀匹配和改写规则。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 `ai-proxy` 插件实现多模型统一接入与无感切换
**场景：** 企业内部同时接入了多家大模型厂商（如 OpenAI, 通义千问, DeepSeek 等），业务端不想维护复杂的适配逻辑，且希望具备随时切换供应商的能力。
**建议：** 核心配置 Higress 的 **`ai-proxy`** 插件。
*   **具体操作：** 在路由配置中，将不同的模型提供商（Provider）配置为不同的服务，并在 `ai-proxy` 插件中映射统一的模型名称。例如，将客户端请求的 `gpt-4` 在上游映射为通义千问的 `qwen-max`。
*   **最佳实践：** 建立一套内部的“标准模型名称”规范。当需要从 A 模型切换到 B 模型时，只需修改网关的插件配置，无需修改任何客户端代码，实现供应商解耦。

### 2. 实施基于 Token 的精细化流量治理
**场景：** AI 请求的计费模式与传统 API 不同（基于输入/输出 Token 计费），且不同 Prompt 的消耗差异巨大。
**建议：** 开启并配置 Higress 的 **Token 统计与限流** 功能。
*   **具体操作：** 在 `ai-proxy` 插件配置中，确保开启了上下文统计功能。在限流规则中，不仅仅基于“请求数（QPS）”进行限制，更要尝试基于“Token 消耗速率”或“请求上下文长度”进行熔断配置。
*   **常见陷阱：** 仅限制 QPS 可能无法防止成本失控。一个包含超长上下文的请求即使 QPS 很低，也可能瞬间产生巨额 API 费用。务必针对长文本请求设置单独的超时或截断策略。

### 3. 构建语义化路由以支持多模态请求分发
**场景：** 随着多模态模型的发展，同一网关可能需要处理文本、图片、音频等不同类型的请求，或者需要根据用户意图将文本请求路由到不同的处理逻辑（如简单的 RAG 检索 vs 复杂的 Agent 推理）。
**建议：** 利用 Higress 的**内容路由**或结合 WAF 插件进行请求体分析。
*   **具体操作：** 配置路由规则，检查请求体中的特定字段（如 `model` 参数或 `messages` 内容特征）。例如，当检测到请求包含图片 URL 时，自动路由至支持视觉模型（LVLM）的后端服务；当检测到特定关键词时，路由至成本更低的微调模型。
*   **最佳实践：** 避免在网关层进行过重的 Prompt 处理逻辑，网关应仅作为“特征识别”和“流量调度”，具体的 Prompt 工程应由后端应用或独立的服务层处理。

### 4. 配置 SSE 流式响应的超时与缓冲策略
**场景：** AI 对话通常采用 Server-Sent Events (SSE) 流式返回，响应时间可能长达数十秒甚至分钟级，且中间可能因网络波动中断。
**建议：** 针对流式请求调整全局或路由级别的超时配置。
*   **具体操作：** 将路由的 `timeout` 设置为较大的值（或留空以无限等待）。同时，关注网关与后端 AI 服务之间的连接保活设置。
*   **常见陷阱：** 如果网关层启用了过大的响应缓冲，会导致流式输出的“打字机效果”失效，用户会等到很久才一次性看到所有回复。确保 Higress 配置中流式响应是直接透传而非全量缓冲。

### 5. 建立模型服务的“兜底”与“降级”熔断机制
**场景：** 第三方 AI 接口不稳定，或者由于敏感词触发导致 API 返回 4xx/5xx 错误，直接影响最终用户体验。
**建议：

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [Kirara-AI：支持多平台接入的多模态聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [Kirara-AI：支持多平台接入的多模态聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [SokoBench：评估大模型长跨度规划与推理能力]({{< relref "posts/20260129-arxiv_ai-sokobench-evaluating-long-horizon-planning-and-rea-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*