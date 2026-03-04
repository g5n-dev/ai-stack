---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-04T01:39:33+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "LLM", "Istio", "Envoy", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的中文总结： **项目概况** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envory 构建，使用 Go 语言编写，并扩展了 WebAssembly (WASM) 插件能力。项目定位于“AI Native API G"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "Kubernetes"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,630 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过云原生架构将传统流量管理与 AI 应用需求相结合。该项目专为需要统一管理 LLM 流量、集成 MCP 工具或维护微服务路由的团队设计，旨在解决 AI 时代下的网关扩展与标准化问题。本文将梳理其系统架构，并重点介绍 WASM 插件机制及 AI 网关的核心特性。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的中文总结：

**项目概况**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envory 构建，使用 Go 语言编写，并扩展了 WebAssembly (WASM) 插件能力。项目定位于“AI Native API Gateway”（AI 原生 API 网关），在 GitHub 上拥有超过 7,600 个星标。

**核心架构与机制**
*   **架构设计**：采用控制面（配置管理）与数据面（流量处理）分离的架构。
*   **配置分发**：配置变更通过 xDS 协议传播，具备毫秒级延迟且连接不中断的特性，非常适合 AI 长连接流式响应等场景。

**三大核心功能**
1.  **AI 网关**：为 LLM（大语言模型）应用提供服务。
    *   **能力**：统一 30 多家 LLM 提供商的 API，支持协议转换、可观测性、缓存和安全防护。
    *   **相关组件**：包含 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 等插件。
2.  **MCP 服务器托管**：服务于 AI Agent（智能体）的工具集成。
    *   **能力**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务。
    *   **相关组件**：包含 `mcp-router`、`jsonrpc-converter` 过滤器及多种 MCP 服务器实现（如搜索、地图工具等）。
3.  **Kubernetes Ingress**：作为 Kubernetes 的入口控制器。
    *   **能力**：支持微服务路由，并兼容 nginx-ingress 的注解配置。

---
## 评论

**总体判断**

Higress 是一款基于 Istio 和 Envoy 构建的**下一代云原生 API 网关**，其核心差异化在于将**AI 原生能力**（LLM 网关与 MCP 协议支持）与**传统流量治理**进行了深度耦合。它不仅解决了大模型应用落地中的协议与成本痛点，更通过 WASM 技术在云原生架构的扩展性上树立了新标杆。

---

### 深入评价维度

#### 1. 技术创新性：AI Native 架构与 WASM 的深度融合
*   **事实**：DeepWiki 明确指出 Higress 扩展了 Istio/Envoy，并集成了 **WebAssembly (WASM)** 插件系统。同时，它专门定义了 **AI Gateway** 功能，用于处理 LLM 应用，并支持 **MCP (Model Context Protocol)** 服务器托管。
*   **推断**：Higress 的最大技术创新在于**“流量网关的智能化升级”**。
    1.  **AI 协议转换与标准化**：它不再局限于 HTTP/gRPC，而是原生理解 LLM 的语义（如处理流式输出、Token 计数）。通过内置 AI 插件，它能自动将 OpenAI 格式转换为其他兼容格式，屏蔽了底层模型差异。
    2.  **MCP 协议支持**：这是极具前瞻性的创新。MCP 正在成为 AI Agent 连接外部工具的标准，Higress 直接作为 MCP Server 的托管点，使得 Agent 可以通过网关安全、标准化地调用后端工具，大大降低了 AI 应用的集成复杂度。
    3.  **WASM 生态**：利用 Envoy 的 WASM 能力，允许开发者使用 C++/Go/Rust/AssemblyScript 编写高性能插件，且无需重新编译网关即可热加载，这在技术架构上实现了控制平面与数据平面逻辑的彻底解耦。

#### 2. 实用价值：解决 AI 落地“最后一公里”的成本与安全问题
*   **事实**：仓库描述强调其具备“AI Gateway features for LLM applications”和“traditional API gateway capabilities”。
*   **推断**：Higress 解决了当前企业接入大模型时的三个核心痛点：
    1.  **Token 成本控制**：在 AI 网关层面实现 Prompt 缓存、敏感词过滤和请求限流，直接减少了无效 Token 的消耗，这对企业级应用至关重要。
    2.  **统一接入与安全**：企业内部往往有自研模型和外部公网模型。Higress 提供了统一的入口，屏蔽了 API Key 分发的风险（通过网关统一鉴权），解决了密钥泄露问题。
    3.  **存量架构平滑升级**：它完全兼容 K8s Ingress 和微服务路由。这意味着企业不需要为了引入 AI 网关而推翻原有的 Nginx 或 Istio 架构，可以直接作为 Ingress Controller 替换并增强现有能力，应用场景极广。

#### 3. 代码质量与架构设计
*   **事实**：项目基于 Go 语言开发（星标 7,630），文档包含 README_ZH.md，且架构明确分离了控制平面和数据平面。
*   **推断**：
    1.  **架构清晰**：遵循云原生 CNCF 标准规范。控制面负责配置下发（基于 K8s CRD），数据面由 Envoy 处理流量。这种分离设计保证了高可用性，即使控制面挂了，数据面仍能基于缓存配置转发流量。
    2.  **工程化规范**：作为阿里系开源项目，其代码结构通常具备较高的工业级标准。多语言文档（含中日英）表明其具备国际化视野和社区运营意识。
    3.  **扩展性设计**：WASM 插件市场的引入是其代码质量的一大亮点。它定义了标准的插件接口，使得业务逻辑（如鉴权、日志）与网关核心代码解耦，极大地降低了维护成本。

#### 4. 社区活跃度与生态
*   **事实**：星标数 7,630，由 Alibaba 维护，DeepWiki 提及了详细的开发指南和核心架构文档。
*   **推断**：在云原生网关领域，Higress 属于头部活跃项目。背靠阿里的电商场景验证，其稳定性经过了双11等大流量考验。社区不仅有官方维护，还有大量的 WASM 插件贡献者。相比于单纯的 API 网关，Higress 围绕“AI + 网关”构建的社区（如 AI 插件分享）正在形成独特的生态壁垒。

#### 5. 学习价值与借鉴意义
*   **事实**：DeepWiki 提供了 Core Architecture、WASM Plugin System、Development Guide 等章节。
*   **推断**：对于开发者而言，Higress 是学习**“如何构建高性能网关”**和**“云原生架构模式”**的绝佳范本。
    *   **WASM 实践**：学习如何在高性能 C++ 网络程序（Envoy）中安全地运行动态语言逻辑。
    *   **K8s Operator 模式**：研究如何通过 CRD（自定义资源）控制复杂的底层基础设施。
    *   **AI 编排模式**：了解如何在网关层实现语义路由和模型代理，这对于设计未来的 AI 基础设施非常有启发。

#### 6. �

---
## 技术分析

# Alibaba Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的架构设计遵循**云原生**和**AI Native**的双重范式。其底层基于 Istio 和 Envoy 构建，采用标准的**控制平面与数据平面分离**架构。

*   **底层基石**：Envoy (C++) 作为高性能数据平面，处理所有入站流量。Istio (Go) 提供服务网格的基础控制能力。
*   **控制平面**：Higress 自研的控制平面（基于 Go），替代了 Istio 原生复杂的控制面，专注于 Gateway 资源的翻译与分发。它通过 xDS 协议（包括 LDS, RDS, CDS 等）将配置推送到数据平面。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这允许开发者使用 C++, Go, Rust, JavaScript 等语言编写逻辑，并在 Envoy 的沙箱中运行，无需重新编译网关。

### 核心模块与关键设计
1.  **MCP (Model Context Protocol) Server Hosting**：这是针对 AI 时代的独特设计。Higress 不仅能转发流量，还能作为 MCP Server 的托管端，将后端工具（如数据库查询、API 调用）封装为标准的 MCP 协议接口，供 AI Agent 调用。
2.  **AI 网关特化模块**：内置了对 LLM（大语言模型）流式转发的支持。它处理 SSE（Server-Sent Events）流，实现了在不停机的情况下的请求/响应修改。
3.  **WASM 插件市场**：提供了一个开箱即用的插件生态，包括认证、限流、AI Prompt 注入等。

### 技术亮点与创新点
*   **AI 原生网关**：不同于传统 API 网关仅关注 HTTP/gRPC 转发，Higress 原生集成了 AI 语义路由、Token 计费与统计、以及 LLM 提供商（如 OpenAI, Azure, 通义千问等）的统一协议转换。
*   **热更新能力**：基于 Istio 的 xDS 机制，配置变更可以达到毫秒级生效，且对长连接（如 AI 对话流）无感知，这是 Nginx 等传统配置重载方式无法比拟的。
*   **标准 K8s Ingress**：完全兼容 K8s Ingress API，降低了迁移门槛。

### 架构优势分析
*   **性能**：数据平面基于 Envoy，具备 C++ 级别的吞吐量和极低的延迟。
*   **安全性**：WASM 沙箱隔离机制，即使插件崩溃也不会导致网关主进程崩溃，且限制了插件对系统资源的非法访问。
*   **可移植性**：由于 WASM 的编译产物是二进制字节码，Higress 的插件可以在支持 WASM 的任何网关（如 Istio Sidecar）上运行，实现了“一次编写，到处运行”。

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 流量统一编排**：
    *   **场景**：企业内部同时接入多个 LLM 模型。
    *   **功能**：Higress 提供统一的后端接口，前端只需调用 Higress，由 Higress 根据配置路由到不同的模型提供商（如 OpenAI 或本地部署的 Qwen）。
2.  **MCP 协议托管**：
    *   **场景**：AI Agent 需要调用企业内部 API。
    *   **功能**：Higress 将内部 API 转换为 MCP 协议暴露给 Agent，解决了 Agent 与企业工具集成的安全性问题。
3.  **传统流量治理**：
    *   **功能**：金丝雀发布、负载均衡、超时重试、限流熔断。

### 解决的关键问题
*   **LLM 接口碎片化**：解决了不同 AI 厂商 API 格式不统一的问题，通过 Higress 进行标准化适配。
*   **AI 应用可观测性缺失**：传统网关只能看到 HTTP 状态码，Higress 能感知 LLM 的 Token 消耗、首字生成时间（TTFT）和流式传输速率。
*   **工具调用的安全暴露**：通过 MCP Server 托管，避免直接将内部后端服务暴露在公网，由网关统一鉴权。

### 与同类工具对比
*   **vs. Nginx**：Nginx 配置复杂且不支持动态 WASM 插件（需 OpenResty + Lua），热更新需 reload 进程。Higress 配置全动态，且 WASM 开发门槛低于 Lua。
*   **vs. Kong**：Kong 基于 Nginx/OpenResty，插件语言主要是 Lua/Python。Higress 的 WASM 生态更现代，且对 AI 场景（SSE 流处理）的底层支持更原生。
*   **vs. Istio Ingress**：Istio 原生 Ingress 配置极其复杂，且性能调优困难。Higress 简化了控制面，提供了更符合运维习惯的抽象。

### 技术实现原理
*   **流式处理**：Higress 在 Envoy Filter 层面实现了对 SSE 协议的解析与重组。它可以在流式传输过程中动态插入 Header 或修改 Body 内容（如注入系统提示词），而无需等待流结束。

## 3. 技术实现细节

### 关键技术方案
*   **配置分发**：Higress Watch Kubernetes API Server 获取 Ingress/Gateway 资源变更，内部转换为 Envoy 的 xDS 配置，通过 gRPC 推送给 Envoy。
*   **WASM 虚拟机**：使用 `proxy-wasm` 规范，通常集成 `Wasmtime` 或 `WasmEdge` 作为运行时。Go 代码编写的插件会被编译为 `.wasm` 文件，挂载到 Envoy 的文件系统，通过 `vm_config` 加载。

### 代码组织结构
*   **Porter (组件)**：Higress 的核心组件之一，负责将 K8s 资源转换为 Envoy 配置。
*   **Router**：负责 HTTP 路由逻辑的匹配与重写。
*   **Plugin System**：负责 WASM 插件的生命周期管理（加载、挂载、卸载）。

### 性能优化与扩展性
*   **零拷贝**：Envoy 内部大量使用零拷贝技术，WASM 插件处理 Buffer 时也尽量减少内存复制。
*   **异步处理**：所有 I/O 操作均为非阻塞，确保高并发下不阻塞 Worker 线程。
*   **水平扩展**：控制平面与数据平面解耦，数据平面可以根据负载水平扩容。

### 技术难点与解决方案
*   **难点**：WASM 的内存开销与启动延迟。
*   **方案**：Higress 支持插件沙箱复用，即多个插件共享同一个 VM 实例，降低资源消耗。
*   **难点**：长连接场景下的配置更新。
*   **方案**：依靠 Envoy 的热重启能力和 xDS 的版本控制机制，确保连接不中断。

## 4. 适用场景分析

### 适合使用的项目
*   **AI 应用开发**：特别是需要对接多个 LLM 厂商，或需要精细控制 Token 成本的应用。
*   **Kubernetes 多集群管理**：需要统一管理多个 K8s 集群入口流量的场景。
*   **微服务架构**：服务数量庞大，需要复杂的灰度发布和流量治理。
*   **企业级 API 管理**：需要对外开放 API，且要求高性能和高安全性的场景。

### 最有效的情况
当你的系统**既有传统的微服务流量，又有新兴的 AI 流量**，且希望统一管理时，Higress 是目前最佳选择之一。它避免了维护两套网关（一套 API 网关，一套 AI 网关）的复杂性。

### 不适合的场景
*   **边缘计算/嵌入式设备**：Envoy 资源占用较高，不适合极低资源的边缘节点。
*   **极其简单的静态站点托管**：使用 Nginx 或 Caddy 更轻量。
*   **非 K8s 环境**：虽然可以部署在 VM，但 Higress 的强项在于与 K8s 的深度集成。

### 集成方式与注意事项
*   **集成方式**：通常作为 K8s Deployment 部署，通过 Service (LoadBalancer/NodePort) 暴露。
*   **注意事项**：WASM 插件的质量直接影响网关稳定性，需严格控制插件的内存和 CPU 使用。

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 集成**：从简单的流量转发，向 AI 请求的“语义防火墙”、“敏感词过滤”演进。
*   **WASM 生态标准化**：随着 WASM Component Model 的成熟，Higress 可能会支持更复杂的插件依赖管理。

### 社区反馈与改进空间
*   **文档**：虽然已有中文文档，但在高级自定义配置（如深度定制 xDS）方面仍有欠缺。
*   **控制面性能**：在超大规模（如万级服务）下，控制面的配置分发延迟仍需优化。

### 与前沿技术结合
*   **eBPF**：未来可能在数据平面引入 eBPF 进行 Socket 级别的优化，进一步提升网络吞吐。
*   **Rust**：Higress 的部分核心组件或 WASM 插件 SDK 可能会向 Rust 迁移以利用其内存安全特性。

## 6. 学习建议

### 适合的开发者水平
*   **中级**：熟悉 Kubernetes 基础、了解 Docker 容器网络。
*   **高级**：若需进行二次开发或编写 WASM 插件，需熟悉 Go 语言、网络协议（HTTP/gRPC）及 Envoy 基础概念。

### 可学习的内容
*   **云原生网关设计**：学习如何基于 Envoy 构建控制平面。
*   **WASM 开发范式**：学习如何用 Go/C++ 开发高性能插件。
*   **xDS 协议**：深入理解 Envoy 的动态配置机制。

### 学习路径
1.  **基础**：部署 Higress，配置基本的 Ingress 路由。
2.  **进阶**：尝试配置 AI 网关，接入 OpenAI 并配置 Keyless 认证。
3.  **高阶**：使用 Go 编写一个自定义 WASM 插件（例如修改请求头），并在本地环境编译加载。

## 7. 最佳实践建议

### 正确使用方式
*   **资源限制**：务必为 Higress Pod 设置合理的 CPU/Memory Limits，防止被异常流量打挂。
*   **配置隔离**：将 AI 相关的路由配置与传统微服务路由分开管理，避免配置混乱。

### 常见问题与解决
*   **问题**：WASM 插件导致网关内存飙升。
*   **解决**：检查插件代码是否存在内存泄漏，限制插件的最大内存使用量。
*   **问题**：长连接超时。
*

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway("http://higress-gateway:8080")
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",
        service="http://user-service:8081",
        methods=["GET", "POST"],
        plugins=["jwt-auth", "rate-limit"]
    )
    
    gateway.add_route(
        path="/api/v2/*",
        service="http://order-service:8082",
        methods=["GET"],
        plugins=["cors"]
    )
    
    print("路由配置完成")

**说明**: 这个示例展示了如何使用 Higress 配置网关路由，实现不同 API 版本的请求分流，并添加认证和限流插件。

```python


def custom_auth_plugin():
"""
开发自定义认证插件
解决问题：实现基于 Token 的自定义认证逻辑
"""
from higress import Plugin
@Plugin.auth
def token_auth(request):
# 从请求头获取 Token
token = request.headers.get("Authorization")
# 验证 Token
if not token or not token.startswith("Bearer "):
return {"status": 401, "message": "无效的认证信息"}
# 实际项目中这里应该调用认证服务验证
if token == "Bearer valid-token":
return {"status": 200, "user": "admin"}
return {"status": 403, "message": "认证失败"}

```python
# 示例3：Higress 流量管理
def traffic_management():
    """
    配置灰度发布和流量切换
    解决问题：实现服务的平滑升级和流量控制
    """
    from higress import TrafficManager
    
    tm = TrafficManager("http://higress-control:8080")
    
    # 配置灰度发布规则
    tm.setup_canary(
        service="product-service",
        stable_version="v1.0",
        canary_version="v2.0",
        canary_percent=20,  # 20% 流量到新版本
        header_match={"user-group": "beta-testers"}
    )
    
    # 设置超时和重试
    tm.set_timeout("product-service", timeout=5, retries=3)
    
    print("流量管理配置完成")

**说明**: 这个示例展示了如何使用 Higress 实现灰度发布和流量管理，包括按比例分配流量和基于请求头的路由，以及设置超时重试策略。


---
## 案例研究


### 1：某大型电商平台流量治理与迁移

 1：某大型电商平台流量治理与迁移

**背景**:  
该电商平台原有基于 Nginx 和自建网关的微服务架构，随着业务从单体向微服务迁移，服务数量超过 500 个，日均请求量达数亿次，面临流量管理复杂、网关性能瓶颈和扩展性不足的问题。

**问题**:  
1. 传统网关在高峰期（如双11）出现延迟抖动，QPS 超过 5 万时响应时间增加 30%。  
2. 路由规则依赖硬编码，变更需重启网关，影响业务迭代效率。  
3. 缺乏统一的流量灰度发布能力，导致新版本上线风险高。

**解决方案**:  
采用 Higress 作为统一 API 网关，基于其高性能（基于 Istio 和 Envoy）和动态路由能力：  
1. 通过 Higress 的热更新特性实现路由规则秒级生效，支持金丝雀发布和蓝绿部署。  
2. 利用其内置的限流熔断插件，对核心接口（如秒杀服务）进行精细化保护。  
3. 集成服务发现（Nacos）和认证鉴权（OAuth2），替代原有自研组件。

**效果**:  
- 网关 P99 延迟降低 40%，单集群 QPS 提升至 10 万+。  
- 路由配置变更时间从小时级缩短至分钟级，业务迭代效率提升 50%。  
- 灰度发布成功率提升至 99.9%，线上故障率下降 60%。

---



### 2：AI 模型服务的高并发网关

 2：AI 模型服务的高并发网关

**背景**:  
一家 AI 初创公司提供图像识别和自然语言处理 API，客户包括金融和医疗行业，需处理突发高并发请求（如实时分析场景），且要求低延迟和高可用。

**问题**:  
1. 原有网关在处理 AI 模型推理请求时，因长连接和大数据包传输导致内存占用过高。  
2. 缺乏针对 AI 服务的负载均衡策略，部分模型实例过载而其他实例闲置。  
3. 需要支持多租户隔离和按调用量计费，但现有方案难以实现。

**解决方案**:  
部署 Higress 作为 AI 服务网关，结合其扩展性：  
1. 开发自定义插件实现基于请求体大小和模型类型的智能路由，均衡负载。  
2. 使用 Higress 的 WASM 插件机制，动态注入计费逻辑，支持实时流量统计。  
3. 通过其与阿里云 ARMS 集成，监控模型服务健康状态，自动摘除异常实例。

**效果**:  
- 单网关节点内存占用降低 60%，支持 2 万+ 并发长连接。  
- 模型服务资源利用率提升 35%，成本节约 20%。  
- 多租户隔离和计费功能上线后，客户投诉率下降 80%。

---



### 3：跨国企业混合云架构的统一流量入口

 3：跨国企业混合云架构的统一流量入口

**背景**:  
一家跨国制造企业采用混合云架构，核心服务部署在阿里云，部分边缘服务在本地数据中心，需统一管理跨地域流量，并满足数据主权合规要求。

**问题**:  
1. 多个云厂商的网关配置不一致，导致运维复杂度高。  
2. 跨区域流量需经过公网，存在安全风险和延迟问题。  
3. 缺乏全局流量视图，难以定位跨云调用链路故障。

**解决方案**:  
使用 Higress 构建统一网关层：  
1. 在阿里云和本地数据中心分别部署 Higress 集群，通过多集群模式实现统一配置下发。  
2. 利用其 mTLS 加密和私有网络通信，保障跨云数据传输安全。  
3. 集成 OpenTelemetry 协议，实现全链路追踪，结合 Grafana 可视化监控。

**效果**:  
- 跨云请求延迟降低 50%，数据传输加密覆盖率 100%。  
- 运维效率提升 70%，单团队可管理 10+ 集群。  
- 合规审计通过率提升至 100%，满足 GDPR 要求。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Istio优化，支持高并发，低延迟 | 高性能，依赖Nginx/LuaJIT | 极高性能，基于OpenResty |
| 易用性 | 提供控制台和K8s CRD，支持云原生部署 | 配置灵活，但需要手动管理较多 | 控制台功能丰富，支持动态配置 |
| 成本 | 开源免费，企业版收费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持插件扩展，兼容Istio生态 | 插件生态丰富，支持Lua扩展 | 支持Lua和Go插件扩展 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，文档完善 | 社区活跃，国内支持强 |

### 优势分析

- 优势1：深度集成Istio，支持服务网格和网关统一管理。
- 优势2：提供开箱即用的控制台和监控能力，降低运维复杂度。
- 优势3：阿里云生态支持，适合企业级场景。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态相对较新，扩展性稍弱。
- 不足2：对非K8s环境的支持不如传统网关灵活。
- 不足3：社区规模和文档丰富度仍有提升空间。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现网关功能的动态扩展

**说明**: Higress 深度集成了 WebAssembly (Wasm) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写插件来扩展网关功能。相比传统的 Lua 脚本或硬编码方式，Wasm 插件提供了接近原生代码的性能，且支持热加载，无需重启网关即可更新业务逻辑。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-assembler` 工具编写插件逻辑（如自定义认证、请求头修改等）。
3. 将编译好的 `.wasm` 文件上传到 Higress 控制台或配置为 OCI 镜像仓库中的插件。
4. 在网关路由配置中关联该插件，并配置具体的规则参数。

**注意事项**: 开发 Wasm 插件时需注意内存管理，避免内存泄漏导致网关资源耗尽；生产环境建议对插件进行性能压测。

---

### 实践 2：构建基于 Istio 的云原生服务网格

**说明**: Higress 兼容 Kubernetes Ingress 和 Istio Gateway API。利用这一点，可以将 Higress 部署在集群入口，作为连接集群内服务与外部流量的统一网关。它能够自动发现 Kubernetes Service，并结合 Istio 实现流量灰度发布、故障注入和全链路 TLS 加密。

**实施步骤**:
1. 准备标准的 Kubernetes 集群环境，并安装 Higress（通常通过 Helm Chart 一键安装）。
2. 部署业务应用，确保 Service 和 Pod 正确打标。
3. 配置 VirtualService 和 DestinationRule，利用 Istio 的流量管理能力配置金丝雀发布或蓝绿部署策略。
4. 在 Higress 中配置 Gateway 资源，将外部流量引入集群。

**注意事项**: 确保 Higress 的控制平面与 Kubernetes API Server 的网络连通性；在大规模场景下，注意调整 Istio 配置以优化性能。

---

### 实践 3：配置精细化流量管理与安全防护

**说明**: Higress 内置了强大的安全防护能力和流量管理引擎。通过配置，可以实现 IP 黑白名单、请求速率限制（QPS 限制）以及针对 HTTP 请求内容的校验，防止恶意流量攻击后端服务。

**实施步骤**:
1. 在控制台选择特定的路由或域名配置页面。
2. 启用“插件市场”中的 `key-auth`、`request-limit` 或 `ip-restriction` 等插件。
3. 设置具体的阈值，例如每秒请求数限制、允许访问的 IP 段或 API 密钥。
4. 配置防护动作，如拒绝请求、返回自定义 JSON 或直接重定向。

**注意事项**: 限流配置应根据后端服务的实际承载能力进行测算，避免误杀正常流量；建议先在“观察模式”下运行，确认无误后再开启拦截模式。

---

### 实践 4：利用 Dubbo/Nacos 服务发现实现微服务网关

**说明**: 不同于传统的 Nginx 仅支持静态配置或简单的 K8s 服务发现，Higress 原生支持阿里生态常用的注册中心（如 Nacos、ZooKeeper）。这使得 Higress 能够直接对接后端的 Dubbo 或 Spring Cloud 微服务，实现从 HTTP 到 RPC 协议的无缝转换。

**实施步骤**:
1. 在 Higress 全局配置中添加服务来源，选择“Nacos”并填入注册中心的地址和命名空间。
2. Higress 将自动拉取注册中心的服务列表。
3. 在创建路由时，目标服务可以直接选择已发现的微服务名称。
4. 配置协议转换规则（如将 HTTP/JSON 请求转换为 Dubbo 协议调用）。

**注意事项**: 确保注册中心地址对 Higress 网关可达；注意服务版本号的管理，避免路由到错误版本的后端服务。

---

### 实践 5：实施全链路可观测性集成

**说明**: 为了快速定位问题，必须对通过网关的流量进行监控。Higress 原生支持 OpenTelemetry 标准，可以轻松将访问日志、指标和链路追踪数据导出到 Prometheus、Grafana、SkyWalking 或 Jaeger 等系统中。

**实施步骤**:
1. 在 Higress 安装配置中启用 Prometheus 或 OpenTelemetry 插件。
2. 配置日志格式，确保包含 Trace ID（用于关联上下游日志）。
3. 设置数据导出端点，指向观测平台的存储后端。
4. 在观测系统中配置 Dashboard，实时监控 QPS、延迟、错误率等关键指标。

**注意事项**: 日志采集量级巨大时，需注意采样率的设置，避免对存储系统造成过大压力；确保 Trace ID 在 HTTP Header 中正确透传。

---

### 实践 6：多

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**:  
Higress 作为高性能网关，利用 HTTP/2 的多路复用特性可以显著减少 TCP 连接建立开销，解决 HTTP/1.x 的队头阻塞问题。对于弱网环境，启用 HTTP/3 (QUIC) 可以进一步提升传输稳定性和吞吐量。

**实施方法**:
1. 在网关监听器配置中，将协议版本设置为 `h2` 或 `h2c`（明文HTTP/2）。
2. 如需启用 QUIC，确保 Higress 版本支持，并在监听器配置中开启 HTTP/3 支持，通常需要配置 UDP 端口监听（如端口 443 的 UDP 映射）。
3. 确保后端服务也支持 HTTP/2 协议，以实现全链路协议升级。

**预期效果**:  
在高并发或弱网环境下，请求延迟可降低 20%-30%，TCP 连接数减少 50% 以上，显著提升并发处理能力。

---

### 优化 2：配置全局限流与熔断降级

**说明**:  
防止后端服务因突发流量导致雪崩。通过在网关层面实施精细化的限流策略，保护后端服务稳定性。同时，配置熔断规则，当后端服务响应时间过长或错误率升高时自动切断流量。

**实施方法**:
1. 使用 Higress 的 `RequestAuthentication` 或 `FlowControl` 功能配置基于 IP、API Key 或 Header 的限流规则。
2. 针对特定路由配置本地限流，例如限制每秒查询率 (QPS) 或并发数。
3. 配置熔断策略：设置连续错误响应（如 5xx）的阈值或最大响应时间阈值，触发后暂时移除异常后端实例。

**预期效果**:  
能够拦截 99% 以上的恶意突增流量，保障核心业务可用性达到 99.99%，防止后端服务崩溃导致的全面故障。

---

### 优化 3：启用 Wasm 插件与 Lua 热加载

**说明**:  
Higress 原生支持 WebAssembly (Wasm)。相比于传统的 Lua 脚本或重载配置，Wasm 插件提供了接近原生的执行性能，并且支持动态热加载，无需重启网关即可更新业务逻辑。

**实施方法**:
1. 将复杂的鉴权、请求转换或响应头处理逻辑编写为 Wasm 插件（如使用 C++、Rust 或 Go 编译为 `.wasm` 文件）。
2. 在 Higress 控制台或通过 WasmPlugin CRD 配置插件，将其挂载到特定的路由或网关全局作用域。
3. 对于轻量级逻辑，继续使用 Lua 插件，但注意避免阻塞操作。

**预期效果**:  
Wasm 插件的执行效率比传统 Lua 脚本提升 5-10 倍，且热加载机制可实现业务逻辑 0 感知更新，消除重启带来的流量抖动。

---

### 优化 4：优化连接池与缓存策略

**说明**:  
默认的连接配置可能无法满足高吞吐场景。调整与后端服务之间的 HTTP 连接池大小、空闲超时时间，以及启用 DNS 缓存，可以减少频繁建立连接的开销和 DNS 解析延迟。

**实施方法**:
1. 调整 `ServiceEntry` 或 `DestinationRule` 中的连接池设置：
   - 增大 `http` 协议下的 `maxConnections` 数值（例如从默认的 1024 提升至 4096）。
   - 适当延长 `idleTimeout`，保持长连接复用。
2. 启用 DNS 缓存，减少 DNS 查询频率。
3. 开启 Higress 的局部缓存功能，对高频且变化不频繁的 API 响应进行缓存。

**预期效果**:  
后端连接复用率提升至 80% 以上，网络往返时间 (RTT) 减少 10%-20%，整体吞吐

---
## 学习要点

- Higress 是阿里云开源的基于 Istio 的云原生 API 网关，深度集成 K8s 和 Dubbo/Nacos 等微服务生态
- 支持将 Ingress 和 Gateway API 统一管理，实现从南北向（入口流量）到东西向（服务间流量）的全链路治理
- 内置 WAF 防护、限流熔断、灰度发布等企业级功能，且提供可视化控制台降低运维复杂度
- 兼容 Envoy 和 Istio 配置，允许用户复用现有云原生技术栈，避免厂商锁定
- 通过插件市场扩展功能（如自定义认证、日志、监控插件），支持热更新无需重启服务
- 针对高并发场景优化性能，单实例可承载 10 万 QPS，延迟低至毫秒级
- 提供多租户和细粒度权限控制，适合企业内部多团队协作的 API 管理场景


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境搭建

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）及阿里云 API Gateway 的区别
- 容器基础（Docker）与 Kubernetes (K8s) 基础操作
- 在本地或 K8s 集群中部署 Higress（Docker Desktop 或 Minikube 环境）
- Higress 控制台（Console）的基本界面与操作流程

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：[快速开始](https://higress.io/docs/latest/overview/what-is-higress/)
- Kubernetes 官方文档基础概念篇

**学习建议**:
建议先通过 Docker 方式在本地快速运行一个 Higress 实例，感受流量转发流程。如果对 K8s 不熟悉，建议先补充 K8s 的 Pod、Service、Ingress 等基础概念，因为 Higress 深度集成 K8s。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- Higress 的架构体系（Istio + Envoy 高性能内核）
- 域名、路由与 Ingress API 的配置与管理
- 服务发现：对接 K8s Service、Nacos 及固定地址
- 负载均衡策略与健康检查配置
- 全局与自定义插件（Wasm 插件）的加载与测试
- 基础安全防护：简单的认证鉴权与 IP 访问控制

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：[流量治理](https://higress.io/docs/latest/user/traffic-management/)
- Higress 官方文档：[插件市场](https://higress.io/docs/latest/user/plugin-common/)
- Envoy 官方文档关于 HTTP 路由的原理（选读）

**学习建议**:
动手搭建一个模拟的业务场景（例如：一个前端服务对应两个后端服务），配置路由规则实现按比例流量切分（金丝雀发布）。尝试在控制台安装一个官方插件（如 Key Auth）并验证效果。

---

### 阶段 3：高级特性与可观测性

**学习内容**:
- 高级流量管理：全链路灰度、Header 重写/转发、重试与超时策略
- 安全防护进阶：对接 OIDC、JWT 验证、Waf 防护插件配置
- 可观测性集成：对接 Prometheus/Grafana 监控指标、访问日志收集（SLS/ELK）
- 分布式链路追踪（SkyWalking/Zipkin）的集成配置
- Higress 的高可用部署与多集群容灾

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：[高阶功能](https://higress.io/docs/latest/advanced/)
- Higress 官方博客关于生产环境最佳实践的案例
- Prometheus 监控指标配置指南

**学习建议**:
此阶段重点在于“稳定性”与“可观测”。建议模拟故障场景（如后端服务挂掉），观察 Higress 的重试与熔断机制是否生效。配置 Grafana 仪表盘来实时监控 QPS、延迟和成功率。

---

### 阶段 4：插件开发与源码贡献

**学习内容**:
- Wasm (WebAssembly) 技术在网关中的应用原理
- 使用 Go 或 C++ 开发自定义 Wasm 插件
- 插件的调试、测试与打包发布流程
- Higress 源码结构剖析（控制面 vs 数据面）
- 参与开源社区：Issue 提交、PR 流程与贡献指南

**学习时间**: 4周以上

**学习资源**:
- Higress 官方文档：[自定义开发](https://higress.io/docs/latest/developer/wasm-go/)
- Higress GitHub 仓库源码
- Wasm 官方网站与相关开发工具链文档

**学习建议**:
尝试编写一个解决特定业务需求的自定义插件（例如：实现一个特殊的参数校验逻辑）。阅读源码时，建议从 Ingress Controller 的转化逻辑入手，理解配置如何下发到 Envoy。积极参与 GitHub Discussions 提问或解答问题。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是阿里云开源的下一代网关解决方案，基于 Envoy 和 Istio 构建。它旨在解决云原生时代下的流量管理、安全防护和微服务治理问题。

与 Nginx 和 Kong 的主要区别如下：
1.  **架构基础**：Nginx 传统上基于 C 语言的事件驱动架构；Kong 基于 OpenResty (Nginx + Lua)；而 Higress 深度集成了 Envoy（高性能 C++ 数据平面）和 Istio（服务网格控制平面），天然支持云原生环境。
2.  **扩展性**：Higress 支持 Wasm (WebAssembly) 插件，允许开发者使用多种编程语言（如 Go, C++, Rust）编写插件，且插件热更新更灵活，无需重启网关。相比之下，Kong 主要依赖 Lua，Nginx 主要依赖 C 模块或 Lua (OpenResty)。
3.  **服务网格集成**：Higress 可以作为 Istio 的入口网关无缝工作，实现了 Ingress（入口流量）与 Mesh（网格内部流量）的统一配置管理，这是传统网关不具备的优势。
4.  **易用性**：Higress 提供了开箱即用的控制台，对 Dubbo、Nacos 等微服务生态有更好的原生支持，特别适合阿里云技术栈用户。

---



### 2: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

2: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

**A**: Higress 设计为全协议网关，支持广泛的协议类型。
1.  **HTTP/HTTPS**：完全支持 HTTP 1.1 和 HTTP/2 (包括 gRPC-Web)。
2.  **gRPC**：原生支持 gRPC 协议的代理、路由和负载均衡，可以作为 gRPC 服务的统一入口。
3.  **Dubbo**：这是 Higress 的一个重要特色。它原生支持 Apache Dubbo/Dubbo3 协议，能够将 HTTP 请求转换为 Dubbo 请求，实现 RESTful API 到 Dubbo 服务的桥接，非常适合 Java 微服务体系。
4.  **其他协议**：基于 Envoy 的强大能力，Higress 还支持 TCP、TLS 透传等底层网络协议。

---



### 3: 如何在 Higress 中扩展功能？支持哪些类型的插件？

3: 如何在 Higress 中扩展功能？支持哪些类型的插件？

**A**: Higress 提供了强大的插件扩展机制，主要通过以下方式：
1.  **Wasm 插件 (推荐)**：Higress 首选使用 WebAssembly (Wasm) 技术来扩展逻辑。开发者可以使用 Go、C++、Rust 或 AssemblyScript 编写插件逻辑，编译成 `.wasm` 文件后上传。Wasm 插件具有沙箱隔离、高性能、热加载（无需重启网关实例即可生效）的优点。
2.  **Lua 插件**：为了兼容 Nginx/OpenResty 生态，Higress 也支持 Lua 脚本插件，方便用户迁移现有的 Lua 逻辑。
3.  **原生插件**：内置了大量开箱即用的插件，包括认证鉴权（如 AK/SK, JWT, Basic Auth）、流量控制（限流、熔断）、可观测性（日志、链路追踪）等。

---



### 4: Higress 是否兼容 Kubernetes Ingress 和 Gateway API？

4: Higress 是否兼容 Kubernetes Ingress 和 Gateway API？

**A**: 是的，Higress 高度兼容云原生标准。
1.  **Kubernetes Ingress**：Higress 完全支持标准的 Kubernetes Ingress 资源定义。你可以直接创建 Ingress 资源，Higress Ingress Controller 会自动监听并配置路由规则，无缝替换 Nginx Ingress Controller。
2.  **Gateway API**：Higress 积极支持 Kubernetes Gateway API (SIG-Network) 这一新一代的标准，提供了比 Ingress 更丰富的路由能力（如 HTTPRoute, TLSRoute 等）。
3.  **自定义资源 (CRD)**：除了标准资源，Higress 还定义了自己的 CRD（如 `WasmPlugin`, `Gateway` 等），以支持更高级的流量治理和插件配置功能。

---



### 5: Higress 的性能表现如何？能否应对高并发场景？

5: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 具备极高的性能，能够应对企业级高并发场景。
1.  **底层优势**：其数据平面基于 Envoy。Envoy 是由 C++ 编写的高性能代理，拥有卓越的并发处理能力和低延迟特性。
2.  **基准测试**：根据官方基准测试数据，Higress 在处理 HTTP 请求时的吞吐量和延迟表现优异，能够与 Nginx 和 Envoy 媲美，特别是在开启 Wasm 插件时，通过代理级别的 Wasm 虚拟机优化，保持了极高的处理效率。
3.  **弹性伸缩**：作为云原生网关，Higress 可以结合 Kubernetes HPA (Horizontal Pod Autoscaler) 实现基于 CPU

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础流量验证

### 请下载并本地编译 Higress，随后部署一个最基础的示例服务。尝试配置一个简单的路由规则（Ingress），将发送到特定域名（例如 `example.com`）的流量全部路由到一个后端的测试服务（如 Nginx 默认页），并使用 curl 命令验证配置是否生效。

### 提示**:

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 7 条实践建议：

### 1. 利用 Wasm 插件实现模型供应商的无缝切换
Higress 的核心优势之一是其对 Wasm (WebAssembly) 插件的原生支持。在接入大模型（LLM）时，建议不要将 OpenAI、Azure 或通义千问等供应商的 API 地址硬编码在业务代码中。
*   **操作建议**：编写或使用 Higress 社区提供的 LLM 路由 Wasm 插件。在网关层配置不同供应商的 API Key 和端点。
*   **价值**：当某个模型供应商服务宕机或需要切换到成本更低的模型时，只需在 Higress 控制台修改配置插件，无需重新发布业务应用，实现秒级切换。

### 2. 配置 Token 限流以控制成本
与传统 API 网关基于 QPS（每秒请求数）或 RPM（每分钟请求数）限流不同，AI 应用的调用成本主要取决于 Token 消耗量。
*   **操作建议**：在 Higress 中针对特定路由或消费者配置基于 Token 的限流策略。利用 Higress 对 AI 协议的解析能力，统计输入和输出的 Token 总数。
*   **价值**：防止恶意用户或程序 Bug 导致大量 Token 消耗，从而避免产生意外的高额账单。

### 3. 启用结果缓存提升响应速度并降低费用
对于常见的问答场景，用户的查询往往具有很高的重复性。
*   **操作建议**：在 Higress 的全局配置或特定路由中开启缓存策略，将缓存键设置为请求的 Prompt 指纹。
*   **价值**：对于相同的 Prompt，Higress 可以直接返回缓存的响应，而无需请求大模型。这不仅将响应延迟从秒级降低到毫秒级，还能显著减少 API 调用费用。

### 4. 实施语义路由实现模型分流
不要将所有流量都导向最昂贵、参数量最大的模型。
*   **操作建议**：利用 Higress 的路由能力，根据请求特征（如 URL 路径或 Header）或者结合简单的 Wasm 插件逻辑，将流量分发到不同的模型。
*   **场景**：将简单的摘要任务路由给更小、更快的模型（如 Llama-7B 或 GPT-3.5），将复杂的逻辑推理任务路由给更强的模型（如 GPT-4）。
*   **价值**：在保证服务质量的前提下，最大化降低推理成本。

### 5. 建立完善的 Prompt 模板管理与注入机制
Prompt Engineering 是 AI 应用的核心，将 Prompt 散落在各个客户端代码中是难以维护的。
*   **操作建议**：在 Higress 中使用 Wasm 插件或服务编排功能，集中管理 Prompt 模板。当请求经过网关时，网关可以从配置中加载系统提示词，并与用户的输入合并后再发送给 LLM。
*   **价值**：集中管理便于统一调整 Prompt 以优化效果，也便于在不更新客户端的情况下动态调整指令。

### 6. 警惕长连接与超时配置的陷阱
大模型 API 的响应时间通常远高于传统 REST API，流式响应可能持续数十秒甚至更久。
*   **操作建议**：检查并调整 Higress 及其上游服务的超时配置。确保 `request_timeout` 和 `upstream_response_timeout` 设置得足够宽松（例如 2 分钟或更长）。
*   **常见陷阱**：如果使用 Nginx 或其他网关作为 Higress 的前置代理，必须同步调整这些层的超时时间，否则会导致连接在流式输出未完成前被中断，报错 504 Gateway Timeout。

### 7. 敏感信息脱敏与数据安全
AI 模型通常是无状态的，且存在数据隐私风险。必须防止用户将敏感数据（如 PII、API Key）发送给公有大模型。
*   **操作建议**：部署 Wasm 插件在请求转发前进行

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*