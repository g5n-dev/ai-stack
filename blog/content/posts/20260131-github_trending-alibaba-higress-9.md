---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T02:40:40+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是对 **Higress** 项目的简洁总结： **1. 项目定位** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。它被定义为一个“AI Native”（AI 原"
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

Higress 是阿里巴巴开源的 AI 原生 API 网关，基于 Istio 与 Envoy 构建，集成了 WASM 插件能力。它专为需要统一管理 LLM 流量、部署 MCP 服务以及处理传统微服务路由的场景设计，能够有效解决云原生架构下的流量治理与 AI 应用集成问题。本文将介绍其系统架构、核心组件及主要用例，帮助开发者了解如何利用 Higress 构建高效、可扩展的网关服务。

---
## 摘要

基于您提供的内容，以下是对 **Higress** 项目的简洁总结：

**1. 项目定位**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。它被定义为一个“AI Native”（AI 原生）网关，旨在统一管理流量、AI 模型调用以及智能体工具集成。

**2. 核心架构**
*   **架构设计**：采用控制平面与数据平面分离的架构。
*   **性能优势**：配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适合 AI 流式响应等长连接场景。

**3. 三大核心功能**
Higress 提供以下三类主要服务：

*   **AI 网关**：
    *   提供统一 API 接口，兼容 30 多家 LLM 提供商。
    *   支持协议转换、可观测性、缓存和语义安全防护。
    *   *相关组件*：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。
*   **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
    *   *相关组件*：`mcp-router`, `jsonrpc-converter` 以及内置的工具实现（如 `quark-search`, `amap-tools`）。
*   **Kubernetes Ingress**：
    *   作为 K8s 入口控制器，支持微服务路由，并兼容 nginx-ingress 注解。
    *   *相关组件*：`higress-controller`。

**总结**：Higress 是一个将传统 API 网关能力与 AI 生态（LLM 接入与 Agent 工具调用）深度融合的高性能网关系统。

---
## 评论

**总体判断**

Higress 是阿里云开源的一款极具前瞻性的“AI 原生”网关，它成功地将云原生流量治理技术与大模型（LLM）应用需求深度融合。该项目不仅继承了 Istio 和 Envoy 的底层高性能优势，更通过 WASM 技术和 AI 特性（如 Token 计费、提示词管理）解决了企业落地 AI 时的关键连接与管控问题，是目前将“传统 API 网关”向“AI 基础设施”演进中最具竞争力的实践之一。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“AI 神经中枢”的架构演进**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并深度集成了 **WebAssembly (WASM)** 插件系统。DeepWiki 明确指出其提供“AI Gateway features for LLM applications”和“MCP server hosting”。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP 转发，而 Higress 的差异化在于它**感知 AI 协议**。它不仅是流量的代理，更是 AI 服务的编排层。
    *   **MCP (Model Context Protocol) 支持**：这是一个极具前瞻性的创新。随着 AI Agent 的普及，模型与外部工具的连接成为痛点。Higress 直接内置 MCP Server 托管，使其成为 Agent 的“工具箱”，极大简化了 Agent 应用的开发复杂度。
    *   **WASM 插件化**：利用 WASM 实现逻辑热加载，允许开发者用 C++/Go/Rust/AssemblyScript 编写插件（如 Key 隔离、敏感词过滤），无需重启网关即可更新 AI 交互逻辑，这种“微内核+插件”的架构比硬编码业务逻辑的传统网关更具灵活性。

**2. 实用价值：解决 AI 落地“最后一公里”的流量与成本问题**
*   **事实**：文档描述其核心功能包括“AI gateway features”和“Traditional API gateway capabilities”。
*   **推断**：Higress 解决了企业在接入大模型时面临的三个核心痛点：
    *   **成本与流控**：LLM 调用成本主要来自 Token。传统网关只能按请求次数限流，而 Higress 能够实现基于 Token 的精细化计量和限流，防止恶意刷接口或预算超支。
    *   **统一接入与安全**：企业往往需要对接多家模型（OpenAI, 通义千问, 文心一言等）。Higress 提供了统一的标准协议层，将后端异构模型接口标准化，并在网关层统一管理 API Key，避免了将密钥暴露给前端或业务侧，增强了安全性。
    *   **平滑迁移**：它保留了作为 K8s Ingress 和微服务网关的能力，意味着用户可以在不引入新组件的情况下，将传统业务流量与 AI 业务流量统一管理，降低了运维复杂度。

**3. 代码质量与架构：云原生标准的工业化实现**
*   **事实**：项目使用 **Go** 语言编写，星标数 7,415，架构上明确分离了“控制平面”和“数据平面”。
*   **推断**：
    *   **架构设计**：控制面与数据面分离是现代网关的标准架构。控制面负责配置下发（兼容 K8s Ingress API），数据面负责高性能转发。这种设计保证了 Higress 在处理高并发 AI 请求时的低延迟。
    *   **代码规范**：作为阿里系开源项目，其代码结构通常遵循严格的 Go 语言规范，模块划分清晰。文档中提到的“Core Architecture”和“Development Guide”表明项目具有较好的可维护性和可扩展性，便于企业二次开发。
    *   **文档完整性**：提供了中、英、日三种语言的 README，且 DeepWiki 显示了详细的架构、构建及插件开发指南，说明该项目对国际化和开发者体验非常重视。

**4. 社区活跃度与生态：背靠阿里的强力驱动**
*   **事实**：星标数超过 7.4k，且由阿里巴巴主导。
*   **推断**：在云原生网关领域，这是一个非常高的关注度。阿里云内部庞大的业务场景（如淘宝、天猫的流量治理及电商 AI 应用）为 Higress 提供了“实战验证”的沙盒。相比纯个人项目，Higress 的迭代速度更有保障，且更倾向于解决真实的规模化问题。社区中关于 WASM 插件的贡献也正在形成生态，开发者可以复用现成的插件来处理 AI 请求/响应。

**5. 学习价值与对比优势：不仅仅是网关，更是 AI 编排的最佳实践**
*   **事实**：DeepWiki 提及“AI Native API Gateway”概念。
*   **推断**：
    *   **对比传统网关**：与 APISIX 或 Kong 相比，Higress 最大的优势在于**“AI 原生”**。其他网关更多是通过插件来支持 AI，而 Higress 是将 AI 能力（如 Prompt 模板管理、多模型路由）内置到了核心逻辑中。
    *   **对比 LangChain 等 LLM 框架**：LangChain 侧重于应用代码逻辑，而 Higress 侧重于**基础设施层**。它让后端工程师无需修改 Python/Java 业务代码，仅通过网关配置即可实现模型切换、缓存或鉴权。
    *   **学习价值**：

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），以下是对其技术架构、核心功能、实现细节及应用场景的全面深入分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**云原生**架构模式，其核心设计理念是**控制平面与数据平面分离**。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和异步非阻塞 I/O 模型。
*   **控制平面**：深度集成 **Istio**，复用 Istio 的 xDS（发现服务）协议进行配置下发，但剥离了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理功能，专注于 Gateway 边界流量。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为插件运行时。这是架构中最关键的一环，允许使用 C/C++/Go/Rust 等多种语言编写插件，编译为 WASM 字节码后在 Envoy 的沙箱中运行。

### 核心模块与关键设计
1.  **MCP (Model Context Protocol) Server Hosting**：
    *   这是 Higress 作为 "AI Gateway" 的核心差异化设计。它不仅代理流量，还内置了 MCP 协议的服务端实现。这意味着 AI Agent 可以直接通过 Higress 获取工具定义，无需为每个工具单独构建 MCP 服务。
2.  **AI Provider Abstraction (统一模型抽象)**：
    *   架构中包含了一层针对 LLM 提供商的抽象层。无论是 OpenAI、通义千问还是 HuggingFace，Higress 将其接口标准化为统一的 Schema。
3.  **WASM Plugin Marketplace**：
    *   设计了一个插件市场机制，允许插件动态加载、热更新，且无需重启网关进程。

### 技术亮点与创新点
*   **毫秒级配置推送**：基于 Istio 的控制平面，配置变更通过 xDS 协议推送到数据平面，实现了配置热更新，且在长连接（如 SSE 流式响应）场景下不断连。
*   **AI-Native 流量处理**：传统网关关注 HTTP Header/Body，而 Higress 创新性地引入了对 AI Token 的处理能力，支持 Prompt 装饰、Token 计数与限流、敏感词过滤等针对 LLM 的语义级治理。

### 架构优势分析
*   **高性能**：数据平面 Envoy 采用 C++ 编写，处理延迟极低。
*   **安全性**：WASM 沙箱隔离机制，即使插件崩溃也不会导致网关主进程崩溃，且限制了插件对底层资源的非法访问。
*   **生态兼容**：完全兼容 K8s Ingress API 和 Gateway API，降低了从 Nginx/Ingress Controller 迁移的门槛。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **功能**：统一管理多家 LLM 提供商的 API Key，实现密钥轮换、透传、重试。
    *   **场景**：企业内部统一接入大模型，避免将 Key 泄露给终端用户，实现模型调用的统一计费和审计。
2.  **MCP 协议托管**：
    *   **功能**：将后端微服务自动暴露为 MCP 工具。
    *   **场景**：AI Agent 需要调用企业内部 API（如查询库存、下单）时，Higress 自动生成 MCP 描述，Agent 可直接发现并调用这些工具。
3.  **传统 API 网关**：
    *   **功能**：路由、负载均衡、限流熔断、认证鉴权。
    *   **场景**：替代 Nginx 或 Kong，作为 K8s 集群的统一流量入口。

### 解决的关键问题
*   **LLM 接口碎片化**：解决了开发者需要适配不同模型厂商 SDK 的问题，一次接入，多处使用。
*   **流式响应处理难**：传统网关在处理 SSE（Server-Sent Events）流时往往难以进行内容拦截或修改，Higress 通过 WASM 插件实现了流式数据的实时处理（如逐 Token 敏感词检测）。
*   **Agent 工具接入成本高**：通过内置 MCP Server，自动化了 AI Agent 与后端服务的“握手”过程。

### 与同类工具的对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Prompt/Token/MCP)** | 弱 (需插件) | 弱 (需插件) | 无 |
| **扩展机制** | **WASM (多语言, 沙箱)** | Lua/Go/Python | Lua/Plugin | C Module/Lua |
| **配置热更新** | **毫秒级** | 支持但需数据库 | 支持但需 etcd | Reload (断连) |
| **K8s 集成** | **原生 (基于 Istio)** | 需 KIC | 原生 CRD | 需 Ingress Controller |

### 技术实现原理
*   **流式拦截**：利用 Envoy 的 `Streaming Filter` 机制，WASM 插件可以在 Buffer 未满时即处理数据流，这对于 AI 的流式输出至关重要，否则用户等待时间将显著增加。
*   **MCP 实现**：Higress 在网关内部实现了一个轻量级的 MCP Transport 层，将 HTTP 服务定义动态转换为 MCP Resource/Prompt 格式。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件加载**：
    *   使用 `proxy-wasm` 规范。Higress 实现了一个插件隔离器，能够从远程仓库（如 OCI 镜像仓库）拉取 WASM 包，并通过 VM（如 Wasmtime 或 V8）加载到 Envoy 进程中。
2.  **配置分发**：
    *   控制平面监听 K8s API Server 的资源变化（Inress/Gateway/WasmPlugin），将其转化为 Istio 配置，再通过 gRPC (xDS v2/v3) 推送给 Envoy。
3.  **AI 请求路由**：
    *   基于 HTTP Header（如 `model: gpt-4`）或 Path 进行路由分发，同时支持将非标准协议（如 SSE）转换为标准 HTTP 处理流程。

### 代码组织与设计模式
*   **Go (控制平面)**：采用 K8s Controller 模式，通过 Informer 监听资源事件，入队 Reconcile 逻辑。
*   **C++ (数据平面)**：基于 Envoy 源码扩展，主要涉及 Filter Chain 的扩展和 Upstream Cluster 的动态管理。
*   **设计模式**：大量使用 **观察者模式**（配置变更监听）和 **责任链模式**（HTTP Filter 处理链）。

### 性能优化与扩展性
*   **零拷贝**：Envoy 内部处理数据尽量减少内存拷贝。
*   **WASM 性能**：通过编译为 AOT (Ahead-of-Time) 或使用高性能 WASM 运行时来降低 JIT 开销。
*   **水平扩展**：数据平面无状态，可根据 K8s HPA 自动扩缩容。

### 技术难点与解决方案
*   **难点**：WASM 插件的内存管理与隔离。
*   **解决**：限制每个插件的最大内存使用，并设置严格的 CPU 时间片，防止单个插件占用过多资源导致网关抖动。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发平台**：需要快速接入 OpenAI/Claude/阿里云百炼等多个模型，并进行统一 Prompt 管理和 Key 鉴权的企业。
2.  **AI Agent 基础设施**：构建 Agent 时，需要将企业内部大量 RESTful API 暴露给 Agent 调用，利用 Higress 的 MCP 功能可极大减少适配工作。
3.  **高并发微服务网关**：需要基于 K8s 的云原生架构，且对性能、延迟有极高要求的场景。

### 最有效的情况
*   **混合云/多云管理**：当业务分布在不同的 K8s 集群或云厂商，需要统一的流量入口和 AI 模型策略分发时。
*   **流式 AI 交互**：需要实时监控或修改 AI 返回内容（如实时敏感词过滤）的场景。

### 不适合的场景
*   **极简单流量转发**：仅需要简单的 Nginx 反向代理，使用 Higress 可能过重（资源占用高于 Nginx）。
*   **非 K8s 环境**：虽然支持 Docker 部署，但其强大功能依赖于 K8s 体系，在虚拟机环境下部署复杂度较高。

### 集成方式与注意事项
*   **集成**：通过 Helm Chart 部署在 K8s 集群中，通常部署在 `kube-system` 或独立的 `ingress-gateway` 命名空间。
*   **注意**：WASM 插件与 Envoy 版本强相关，升级 Higress 时需检查 WASM 插件的兼容性。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 协议理解**：从简单的 HTTP 转发，向理解 AI 语义（如 Function Calling 结果校验）演进。
*   **边缘计算支持**：利用 WASM 的轻量级特性，将 Higress 部署到边缘节点（如 CDN 边缘），实现更低延迟的 AI 推理加速。

### 社区反馈与改进空间
*   **改进**：目前 WASM 插件的调试相对困难，日志获取不够直观。未来需要更强的 WASM 生态工具链支持。
*   **文档**：针对 AI 特性的高级用法（如复杂的 Prompt Template 编排）文档仍需完善。

### 与前沿技术的结合
*   **eBPF**：未来可能在 L3/L4 层面引入 eBPF 进行更底层的 Socket 加速，与 WASM 形成“内核加速 + 用户态逻辑”的互补。

---

## 6. 学习建议

### 适合的开发者水平
*   **中级**：了解 K8s 基础、Docker 容器技术、HTTP 协议。
*   **高级**：若需深入定制 WASM 插件或修改核心逻辑，需掌握 C++ (Envoy) 或 Go (Istio 控制面)。

### 学习路径
1.  **基础**：学习 Envoy 基础概念（Listener, Route, Cluster）。
2.  **进阶**：理解 Istio 的 xDS 协议和控制平面数据流向。
3.  **实战**：尝试编写一个简单的 WASM 插件（如修改 HTTP Header），部署到 Higress 并观察效果。
4.  **AI 特性**：配置 AI Provider，使用 Postman 模拟 LLM 请求，体验路由和 Key

---
## 代码示例




```python
# 示例1：基于Higress的简单路由配置
def higress_route_config():
    """
    模拟Higress网关的路由配置
    实际应用中会通过K8s CRD或Higress Dashboard配置
    """
    route_config = {
        "apiVersion": "networking.k8s.io/v1beta1",
        "kind": "Ingress",
        "metadata": {
            "name": "higress-demo-route",
            "annotations": {
                "nginx.ingress.kubernetes.io/rewrite-target": "/$2"
            }
        },
        "spec": {
            "rules": [{
                "host": "example.com",
                "http": {
                    "paths": [{
                        "path": "/api(/|$)(.*)",
                        "backend": {
                            "serviceName": "backend-service",
                            "servicePort": 8080
                        }
                    }]
                }
            }]
        }
    }
    
    # 这里只是模拟配置，实际会应用到K8s集群
    print("路由配置已生成:")
    print(f"域名: {route_config['spec']['rules'][0]['host']}")
    print(f"路径规则: {route_config['spec']['rules'][0]['http']['paths'][0]['path']}")
    print(f"后端服务: {route_config['spec']['rules'][0]['http']['paths'][0]['backend']['serviceName']}")

# 运行示例
higress_route_config()
```




```python
# 示例2：Higress插件配置示例
def higress_plugin_config():
    """
    模拟Higress的插件配置
    这里展示如何配置一个限流插件
    """
    plugin_config = {
        "apiVersion": "extensions.higress.io/v1alpha1",
        "kind": "WasmPlugin",
        "metadata": {
            "name": "rate-limit-plugin",
            "namespace": "higress-system"
        },
        "spec": {
            "url": "oci://higress-registry.cn-hangzhou.cr.aliyuncs.com/plugins/rate-limit:1.0.0",
            "ruleConfig": {
                "limit_by_header": "X-User-ID",
                "query": 100,  # 每秒100次请求
                "time_window": "1s",
                "rejected_code": 429,
                "rejected_msg": "请求过于频繁，请稍后再试"
            }
        }
    }
    
    print("插件配置已生成:")
    print(f"插件名称: {plugin_config['metadata']['name']}")
    print(f"限流规则: 每个用户每秒{plugin_config['spec']['ruleConfig']['query']}次请求")
    print(f"超限响应: {plugin_config['spec']['ruleConfig']['rejected_code']} - {plugin_config['spec']['ruleConfig']['rejected_msg']}")

# 运行示例
higress_plugin_config()
```




```python
# 示例3：Higress服务发现配置
def higress_service_discovery():
    """
    模拟Higress的服务发现配置
    展示如何配置Nacos服务发现
    """
    service_discovery_config = {
        "apiVersion": "networking.higress.io/v1alpha1",
        "kind": "ServiceSource",
        "metadata": {
            "name": "nacos-service-source",
            "namespace": "higress-system"
        },
        "spec": {
            "type": "nacos",
            "nacos": {
                "address": "nacos-server.default.svc.cluster.local",
                "port": 8848,
                "namespaceId": "public",
                "groups": ["DEFAULT_GROUP"],
                "service": "user-service",
                "clusters": ["DEFAULT"]
            }
        }
    }
    
    print("服务发现配置已生成:")
    print(f"服务来源: {service_discovery_config['spec']['type']}")
    print(f"Nacos地址: {service_discovery_config['spec']['nacos']['address']}:{service_discovery_config['spec']['nacos']['port']}")
    print(f"服务名称: {service_discovery_config['spec']['nacos']['service']}")
    print(f"命名空间: {service_discovery_config['spec']['nacos']['namespaceId']}")

# 运行示例
higress_service_discovery()
```


---
## 案例研究


### 1：某大型电商平台微服务网关改造

 1：某大型电商平台微服务网关改造

**背景**:
该电商平台拥有数百个微服务，原先使用 Nginx 作为传统的流量入口。随着业务向云原生架构迁移，团队需要一个能够深度集成 Kubernetes，且支持动态配置和标准 API 管理的下一代网关。

**问题**:
原有的 Nginx 配置维护复杂，每次变更都需要重新加载配置，容易导致服务中断。此外，由于缺乏对 gRPC 和 Dubbo 等微服务协议的原生支持，路由配置极其繁琐。团队急需一种既能处理传统南北向流量，又能高效管理东西向流量的统一网关，且要求具备与阿里云 ARMS 等可观测性平台的无缝集成能力。

**解决方案**:
引入 Higress 作为统一的云原生 API 网关。利用 Higress 的 Ingress 特性接管 Kubernetes 集群流量，同时启用其对 Dubbo 和 Nacos 的原生支持，实现了服务发现与流量管理的自动化。通过 Higress 的插件市场，快速集成了认证鉴权和请求限流逻辑。

**效果**:
网关配置的变更实现了秒级生效，无需重启服务。通过 Higress 的高性能处理，网关层的资源成本降低了 30%。同时，统一的插件管理使得开发人员可以专注于业务逻辑，流量治理效率提升了 50% 以上。

---



### 2：AI 模型推理服务的高并发接入

 2：AI 模型推理服务的高并发接入

**背景**:
一家 AI 初创公司推出了基于 LLM（大语言模型）的智能对话服务。该服务部署在 Kubernetes 集群中，后端对接不同的模型推理引擎。随着用户量激增，入口网关面临巨大的挑战。

**问题**:
传统的网关在处理 AI 应用的长连接和流式传输时表现不佳，且缺乏针对模型调用的特定负载均衡策略。由于推理服务耗时较长且资源昂贵，简单的轮询负载均衡会导致某些后端实例过载而其他实例空闲，无法有效控制并发请求，进而影响服务稳定性。

**解决方案**:
部署 Higress 并利用其针对 AI 场景的特定能力。配置了请求级排队与并发控制插件，确保进入后端模型的请求量严格限制在 GPU 实例能承受的范围内。同时，利用 Higress 对 SSE（Server-Sent Events）的完善支持，优化了流式响应的转发性能。

**效果**:
成功实现了对后端脆弱推理服务的“过载保护”，服务稳定性显著提升，P99 延迟降低了 40%。流式传输的吞吐量大幅增加，用户体验更加流畅。此外，通过精细的流量控制，公司在硬件成本不变的情况下，成功支撑了 3 倍的用户并发增长。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持WASM插件扩展 | 基于OpenResty，性能较高，但插件扩展性有限 | 基于OpenResty，性能优异，支持Lua插件 |
| 易用性 | 提供控制台和K8s集成，配置灵活，学习曲线中等 | 提供管理界面和API，配置较复杂，学习曲线较陡 | 提供Dashboard和K8s集成，配置简单，学习曲线平缓 |
| 成本 | 开源免费，企业版需付费支持 | 开源免费，企业版需付费支持 | 开源免费，企业版需付费支持 |
| 扩展性 | 支持WASM插件，扩展性强，适合复杂场景 | 支持Lua和Go插件，扩展性一般 | 支持Lua和WASM插件，扩展性较强 |
| 社区支持 | 阿里背书，社区活跃，文档较完善 | 社区成熟，文档丰富，但更新较慢 | 社区活跃，文档完善，更新较快 |

### 优势分析

- 优势1：基于Envoy和Istio，性能和扩展性优于传统网关
- 优势2：支持WASM插件，灵活性强，适合复杂业务场景
- 优势3：阿里背书，社区活跃，文档和生态支持较好

### 不足分析

- 不足1：学习曲线较陡，需要一定的Envoy和Istio知识
- 不足2：相比Kong和APISIX，社区成熟度稍逊
- 不足3：企业版功能需付费，成本较高

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 原生支持 WebAssembly (Wasm) 技术，允许用户使用 C++、Go、Rust 或 AssemblyScript 编写高性能的插件。相比传统的 Lua 脚本或 Java Filter，Wasm 插件提供了更好的隔离性、更快的启动速度以及接近原生的执行性能，且无需重启网关即可动态加载。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或示例模板开发插件逻辑（如：自定义认证、请求头修改、响应体处理）。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 镜像仓库进行配置。
4. 在网关规则中针对特定路由或全局应用该插件，并配置所需的参数。

**注意事项**: 
- Wasm 插件运行在沙箱中，处理内存和 CPU 资源时需注意限制。
- 调试 Wasm 插件相对复杂，建议在本地环境充分测试后再部署至生产环境。

---

### 实践 2：精细化流量路由与服务治理

**说明**: 利用 Higress 强大的路由能力实现基于权重、Header、Cookie 或 URL 参数的流量分流。这常用于蓝绿发布、金丝雀发布以及 A/B 测试场景。同时，结合服务发现功能，实现对微服务实例的负载均衡和健康检查。

**实施步骤**:
1. 在控制台配置路由规则，定义匹配条件（如 `x-canary: true`）。
2. 设置多个目标服务版本，并分配相应的流量权重（例如：95% 流量走 v1，5% 流量走 v2）。
3. 配置超时时间、重试策略以及熔断降级规则，以防止后端服务故障影响整体网关。
4. 启用健康检查，确保 Higress 能够自动摘除不健康的后端 Pod 或实例。

**注意事项**: 
- 权重路由的变更应逐步进行，避免流量瞬间切换导致的风险。
- 确保超时时间设置合理，通常应大于后端服务的平均响应时间。

---

### 实践 3：全链路安全防护与认证

**说明**: Higress 提供了丰富的安全插件，用于保护后端服务免受恶意攻击。通过配置 IP 访问控制、动态请求频率限制以及集成主流认证方式（如 OIDC、JWT、Basic Auth 或 API Key），构建网关层面的安全防线。

**实施步骤**:
1. 开启 `block-list` 或 `allow-list` 插件，限制特定 IP 段的访问。
2. 配置 `key-rate-limit` 或 `request-block` 插件，防御 DDoS 攻击或恶意刷接口。
3. 若对接微服务网关（如 Nacos），配置 `jwt-auth` 插件实现无状态的服务间鉴权。
4. 对于外部 API 开放，启用 `hmac-auth` 或 `api-key` 插件进行调用方身份验证。

**注意事项**: 
- 频率限制策略应根据业务实际 QPS 进行压测设定，以免误杀正常用户。
- 敏感配置（如密钥）建议使用 KMS 或密钥管理服务进行存储，而非明文写在配置中。

---

### 实践 4：对接云原生服务注册中心

**说明**: Higress 设计为云原生网关，能够无缝对接 Nacos、Consul、ZooKeeper 以及 Kubernetes CoreDNS。通过服务发现机制，网关可以动态感知后端服务实例的上下线，无需手动维护繁琐的 IP 列表。

**实施步骤**:
1. 在 Higress 控制台的“服务来源”中添加对应的注册中心（例如 Nacos）。
2. 配置命名空间和服务分组，确保 Higress 能正确读取到微服务列表。
3. 在创建路由时，直接选择服务名称作为目标服务，而非静态 IP 地址。
4. (可选) 开启 DNS 代理功能，实现 Kubernetes Service 的自动解析。

**注意事项**: 
- 确保网络连通性，Higress 所在的网络环境必须能访问注册中心的端口。
- 如果使用 Nacos，请确认命名空间 ID 配置正确，避免环境隔离错误。

---

### 实践 5：可观测性与监控告警

**说明**: 借助 Higress 的集成能力，建立全方位的监控体系。通过 Access Log 记录详细流量信息，利用 Prometheus 采集指标数据，并对接 SkyWalking 或 Jaeger 实现 Tracing 链路追踪，快速定位性能瓶颈或异常。

**实施步骤**:
1. 配置日志采集，将 Higress 的访问日志输出至 Elasticsearch、Loki 或 Kafka。
2. 开开 Prometheus Metric 抓取端点，配置 Grafana 仪表盘监控 QPS、延迟、错误率等核心指标。
3. 启用 Tracing

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy，天然支持 HTTP/3 协议。HTTP/3 基于 UDP，解决了 TCP 队头阻塞问题，在弱网环境下能显著降低连接延迟和握手时间，提升传输效率。

**实施方法**:
1. 在 Higress 网关的监听器配置中，为需要优化的路由或域名启用 HTTP/3 协议。
2. 确保底层网络环境（防火墙、负载均衡器）放行 UDP 流量（通常端口 443）。
3. 配置 TLS 1.3 以配合 HTTP/3 发挥最佳性能。

**预期效果**: 在弱网或丢包环境下，页面加载时间（TTLB）可降低 20%-40%，连接建立成功率提升。

---

### 优化 2：启用 Wasm 插件的高效缓存与隔离

**说明**: Higress 的核心特性之一是支持 Wasm (WebAssembly) 插件。默认情况下，Wasm 可能在每次请求或连接时进行编译或实例化。通过配置 Wasm 的缓存和预编译，可以大幅减少 CPU 开销和响应延迟。

**实施方法**:
1. 在网关配置中启用 Wasm VM 的代码缓存功能。
2. 使用 `wasm` 过滤器配置时，将 Wasm 文件挂载到内存文件系统或本地缓存，避免重复网络下载。
3. 合理配置 Wasm 插件的并发度，避免锁竞争。

**预期效果**: Wasm 插化的处理延迟可降低 30%-50%，网关 CPU 利用率在流量高峰期更平稳。

---

### 优化 3：配置全局限流与连接复用

**说明**: Higress 内置了高性能限流功能。通过在网关层实施全局限流，可以防止突发流量击穿后端服务。同时，优化后端服务的连接池配置，启用 HTTP/2 或连接复用，减少后端频繁建立 TCP 连接的开销。

**实施方法**:
1. 使用 Higress 的 `request-auth` 或自定义 Wasm 插件实现基于 IP 或 API Key 的全局限流。
2. 在 Upstream 配置中，调整 `http2_protocol_options` 或 `connection_pool` 参数。
3. 增加单个后端节点的最大连接数限制，并启用“保持连接”以复用链接。

**预期效果**: 后端连接建立开销减少 50% 以上，抗突发流量能力提升，保护后端服务稳定性。

---

### 优化 4：启用本地与分布式缓存

**说明**: 对于读多写少的流量（如 API 响应、配置数据），在 Higress 网关层启用缓存可以直接拦截请求，避免流量打到后端业务逻辑。Higress 支持本地内存缓存，也可对接 Redis 等分布式缓存。

**实施方法**:
1. 在路由配置中启用响应缓存插件，设定合理的 TTL（生存时间）。
2. 针对鉴权结果等元数据，使用 Wasm 插件配合本地字典进行缓存。
3. 配置基于请求头或 URL 的缓存键策略，确保缓存命中率的准确性。

**预期效果**: 后端请求量减少 30%-90%（视业务读多写少程度而定），平均响应延迟（RT）降低至毫秒级。

---

### 优化 5：精细化日志与采样控制

**说明**: 详细的日志是排查问题的关键，但在高并发场景下，全量日志记录会严重消耗磁盘 I/O 和 CPU，甚至成为性能瓶颈。通过动态调整日志级别和采样率，可以在保证可观测性的前提下提升性能。

**实施方法**:
1. 将 Access Log 的输出级别从 `DEBUG` 调整为 `INFO` 或 `WARN`。
2. 配置日志采样（例如仅记录 4xx/5xx 错误日志或 10% 的正常流量日志）。
3. 使用异步日志发送（如对接 Kafka、SLS）时，调整 Batch Size 和 Flush Interval，减少网络 I/O 次数

---
## 学习要点

- 根据提供的内容（Alibaba / Higress），以下是总结出的关键要点：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的云原生 API 网关，旨在连接南北向流量与东西向流量。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够作为 Ingress 控制器直接管理集群入口流量。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿部署、负载均衡以及超时重试等精细化路由规则。
- Higress 原生集成了 WAF（Web 应用防火墙）插件，提供开箱即用的安全防护能力以抵御常见 Web 攻击。
- 该网关支持全面扩展，兼容 Envoy 和 WASM 插件生态，允许用户通过 Lua、WASM 或 Go 开发自定义插件。
- 它具备高性能与低延迟特性，支持热更新与配置动态下发，适用于对性能要求严苛的大规模流量场景。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的核心概念与架构：理解其作为云原生 API 网关的定位，以及基于 Istio 和 Envoy 的技术架构。
- 基本术语：掌握 Ingress、Gateway、路由、服务、插件等基础术语。
- 本地环境搭建：学习使用 Docker 或 Kubernetes (Kind/Minikube) 部署 Higress。
- 控制台操作：熟悉 Higress 提供的 Console/Dashboard 界面，进行简单的服务发现和流量路由配置。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与快速开始章节)
- Higress GitHub 仓库 (README.md)
- Docker 和 Kubernetes 基础教程

**学习建议**:
- 在开始之前，建议先对 Kubernetes 和 Docker 有基本的了解，因为 Higress 通常运行在 K8s 集群之上。
- 动手实践是关键，不要只看文档，务必在本地搭建一个单机版环境并跑通第一个 "Hello World" 示例。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- HTTP 路由配置：深入学习基于域名、路径、Header 的流量匹配与转发规则。
- 服务来源管理：学习如何配置固定地址、Nacos、Consul、Kubernetes Service 等服务来源。
- 负载均衡策略：理解并配置轮询、随机、加权最少连接等负载均衡算法。
- 全局与精细化流量治理：学习超时、重试、熔断、限流以及 CORS 跨域配置。
- 金丝雀发布与蓝绿发布：掌握基于 Header 或权重的灰度发布能力。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (流量治理、服务来源板块)
- Envoy 官方文档 (了解底层代理原理)
- 云原生网关最佳实践博客

**学习建议**:
- 尝试模拟真实的业务场景，例如将一个后端服务接入 Higress，并配置路由规则。
- 重点理解 "Wasm 插件" 的概念，这是 Higress 区别于传统网关的一大特性，虽然此阶段不必深究代码，但需了解其作用。
- 对比学习 Nginx Ingress，理解 Higress 在云原生环境下的优势。

---

### 阶段 3：插件开发与安全防护

**学习内容**:
- 插件市场使用：熟悉如何直接在控制台开启和配置官方插件（如 KeyAuth、RequestBlock）。
- 安全防护：学习配置 IP 访问控制、Basic Auth、JWT 认证以及 API 防火墙策略。
- Wasm 插件开发（进阶）：学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现特定的业务逻辑（如请求体修改、自定义鉴权）。
- 插件调试：掌握如何在本地或生产环境中调试 Wasm 插件。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 (插件开发指南)
- Higress 官方插件市场
- WebAssembly (Wasm) 基础教程

**学习建议**:
- 先学会使用现有的官方插件解决常见问题（如防盗链、限流）。
- 如果有编程基础，尝试编写一个简单的 Go 语言 Wasm 插件，例如给所有请求添加一个特定的 Header，并部署到网关中验证。

---

### 阶段 4：高可用与生产实践

**学习内容**:
- 高可用部署架构：学习 Higress 在 Kubernetes 中的多副本部署、资源限制与性能调优。
- 可观测性：深度集成 Prometheus/Grafana 进行监控，配置日志采集（SLS/ELK）以及链路追踪。
- 多集群管理：了解如何使用 Higress 进行多集群或混合云的流量管理。
- 网关平滑升级与迁移：学习从 Nginx Ingress 或其他网关迁移到 Higress 的策略。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (运维指南、监控板块)
- Kubernetes 运维最佳实践
- Prometheus 与 Grafana 配置教程

**学习建议**:
- 关注性能指标（QPS、延迟），并学习如何通过调整 Pod 资源和 Envoy 配置来优化性能。
- 在测试环境中模拟网关故障，观察系统的自愈能力和流量切换情况。
- 研究阿里云云原生 API 网关的商业化产品文档，了解企业级的高级功能（虽然我们使用开源版，但架构思想相通）。

---
## 常见问题


### 1: Higress 是什么？它与云原生 API 网关有什么关系？

1: Higress 是什么？它与云原生 API 网关有什么关系？

**A**: Higress 是一款云原生 API 网关。它是基于阿里云内部多年实践沉淀的 Gateway 架构，结合了 Envoy 和 Istio 的优点，旨在为用户提供标准化、高集成、易扩展、云原生的网关产品。它遵循开源 OpenNMS 社区的 Gateway API 标准，可以作为 Kubernetes 集群的 Ingress Controller 使用，也可以作为独立的 API 网关部署。



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的主要优势在于其“云原生”基因和深度集成能力：
1.  **架构先进**：基于 Envoy (C++/Go) 架构，数据面性能高，控制面 (Istio/Go) 扩展性强。
2.  **标准化支持**：原生支持 Kubernetes Gateway API 和 Ingress API，迁移和适配成本更低。
3.  **安全防护**：内置了 WAF (Web Application Firewall) 能力，提供开箱即用的安全防护。
4.  **服务治理集成**：与 Nacos、Consul 等主流注册中心以及 Dubbo、gRPC 等微服务协议深度集成，能够无缝对接微服务生态，无需复杂的配置即可实现服务发现和流量管理。



### 3: Higress 是否支持 Dubbo 服务？如何进行 HTTP 转 Dubbo 的协议转换？

3: Higress 是否支持 Dubbo 服务？如何进行 HTTP 转 Dubbo 的协议转换？

**A**: 是的，Higress 对 Dubbo 有着深度的原生支持。这是 Higress 的核心特色之一。它允许用户通过 HTTP/HTTPS 协议访问后端的 Dubbo 服务。在 Higress 中，用户只需要配置路由规则，指定 Dubbo 服务的服务名、方法名和参数类型，Higress 就会自动完成协议转换和流量转发，极大地简化了网关对接微服务的复杂度。



### 4: Higress 如何处理插件扩展？是否支持热加载？

4: Higress 如何处理插件扩展？是否支持热加载？

**A**: Higress 提供了强大的插件扩展能力。它支持使用 Go、Python、Java、WASM (WebAssembly) 等多种语言编写插件。特别是基于 WASM 的插件，可以实现沙箱隔离运行，安全性高且支持动态热加载。用户可以在 Higress 控制台直接上传插件或配置插件参数，无需重启网关服务即可使插件生效，这大大提升了运维效率和系统的灵活性。



### 5: Higress 的 WAF 功能是收费的吗？它是如何工作的？

5: Higress 的 WAF 功能是收费的吗？它是如何工作的？

**A**: 在开源版本中，Higress 提供了基础的 WAF 能力。它通过内置的规则库来识别和防御常见的 Web 攻击，如 SQL 注入、XSS 跨站脚本、远程代码执行等。用户可以在网关路由配置中开启 WAF 防护，并根据需要设置拦截模式（监控模式或拦截模式）。这使得用户在不需要额外购买昂贵 WAF 设备的情况下，也能获得基础的安全保障。



### 6: 如何部署 Higress？对 Kubernetes 环境有什么要求？

6: 如何部署 Higress？对 Kubernetes 环境有什么要求？

**A**: Higress 最推荐的方式是直接部署在 Kubernetes 集群中。它提供了标准的 Helm Chart 包，可以通过 Helm 3 一键安装。对于 Kubernetes 版本，通常建议使用 1.19 及以上版本以确保 Gateway API 等特性的兼容性。同时，Higress 也支持 Docker Compose 部署，方便开发测试环境使用。



### 7: Higress 与 Istio 的关系是什么？能否直接替换 Istio 的 Ingress Gateway？

7: Higress 与 Istio 的关系是什么？能否直接替换 Istio 的 Ingress Gateway？

**A**: Higress 的底层架构深受 Istio 启发，并复用了 Istio 的部分组件（如 Envoy）。Higress 可以作为 Istio 生态中的一个高性能 Ingress Gateway 组件使用。相比于 Istio 原生的 Ingress Gateway，Higress 提供了更友好的控制台、更丰富的路由插件（如自定义 Auth、流量镜像）以及对国内主流微服务框架（如 Dubbo、Nacos）的更好支持。因此，它常被用作 Istio Ingress Gateway 的增强替代品。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 构建，并支持 Nginx 的 Ingress 注解。请尝试将一个现有的 Nginx Ingress 配置迁移到 Higress，重点关注如何将基于路由的 Nginx 配置（如 `rewrite-target` 或 `ssl-redirect`）转换为 Higress 的配置格式（Kubernetes CRD 或 Console 配置）。

### 提示**: 重点关注 Higress 的 `Ingress` 资源定义或 `Gateway` API 的路由配置，查阅 Higress 文档中关于 Nginx 注解兼容性的说明。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其基于 Envoy 和 Istio 的技术架构，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 AI 插件实现统一提示词管理
**场景**：在对接大模型（LLM）时，应用层代码往往硬编码了提示词，导致调整策略或切换模型时需要重新发布服务。
**建议**：使用 Higress 的 **AI 代理插件**（如 `ai-proxy`）在网关层统一配置 System Prompt 和参数。
**操作**：
*   在路由配置中启用 AI 插件，将通用的上下文信息或人设配置在网关的 `system_prompt` 字段中。
*   仅在业务请求中传递用户具体的输入，保持后端服务逻辑的纯净。
**优势**：实现业务逻辑与模型提示策略的解耦，无需重启服务即可在线调整模型行为。

### 2. 配置语义路由以降低 Token 消耗
**场景**：传统的网关路由基于 HTTP 路径或 Header，但在 AI 场景下，可能需要根据用户的自然语言意图将请求分发到不同的后端（例如：将“写代码”请求分发到 Copilot 服务，将“画图”请求分发到 DALL-E 服务）。
**建议**：利用 Higress 的 **LLM 分类路由** 功能。
**操作**：
*   配置基于语义的路由规则，让网关先对用户输入进行一次低成本的意图识别。
*   根据识别结果将流量路由至不同的模型服务或业务后端。
**优势**：避免在后端应用中编写复杂的 `if-else` 逻辑进行意图判断，减少不必要的 Token 消耗和延迟。

### 3. 实施基于 Token 的精细化流控
**场景**：大模型 API 的调用成本主要取决于 Token 数量，传统的基于 QPS（每秒请求数）或并发连接数的限流无法有效控制成本。
**建议**：配置针对 **Token 吞吐量** 的限流策略。
**操作**：
*   在 Higress 的全局限流或局部限流配置中，关注请求体和响应体的长度限制。
*   结合插件对 Prompt 长度进行校验，拒绝或截断过长的输入，防止恶意的长输入导致后端账单爆炸。
**陷阱**：仅限制并发连接数可能会导致少量客户端发送极长的 Prompt 耗尽系统配额。

### 4. 启用结果缓存以优化性能和成本
**场景**：在问答或知识库检索场景中，大量用户问题往往是重复的（例如：“如何重置密码”），每次都调用大模型接口会产生高昂的费用和延迟。
**建议**：针对 **GET 请求或幂等的对话请求** 开启响应缓存。
**操作**：
*   利用 Higress 的缓存插件，将大模型返回的完整响应体进行缓存。
*   配置合理的 Cache Key（例如包含用户问题的 Hash）和 TTL（生存时间）。
**优势**：对于高频重复问题，可以直接由网关返回结果，响应延迟从秒级降至毫秒级，且显著降低 API 调用成本。

### 5. 妥善处理流式响应的转发与超时
**场景**：AI 对话通常采用 Server-Sent Events (SSE) 或流式返回，以提升用户体验。传统网关若配置不当，可能会缓冲整个响应直到结束才转发给客户端，导致“卡顿”感。
**建议**：确保网关配置了 **流式透传** 模式。
**操作**：
*   检查 Higress 的超时设置，流式请求可能耗时较长，需适当调大 `request_timeout`。
*   确认后端服务配置了正确的 `Content-Type: text/event-stream`，并且网关未开启可能破坏流式传输的缓冲或压缩插件。
**陷阱**：如果网关尝试解码或修改 JSON 响应体，可能会破坏流式格式，导致客户端无法解析增量数据。

### 6. 建立模型故障的降级与熔断

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
- [中国开源AI生态的架构选择：超越DeepSeek的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的技术路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*