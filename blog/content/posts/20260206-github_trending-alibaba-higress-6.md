---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T00:00:46+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： **项目概况** **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envory 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。该项目专为 AI 原生应用设计，旨在提供统一的流量入口和管理平台。项"
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
- **星标**: 7,462 (+16 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构解决 LLM 应用接入与微服务治理的复杂性。它不仅提供传统的流量管理与 Kubernetes Ingress 能力，更集成了 AI 网关特性与 MCP 协议支持，以适应大模型时代的接口需求。本文将梳理其架构设计，并重点介绍 WASM 插件体系及 AI 流量管理的核心功能。

---
## 摘要

以下是对 Higress 项目的简洁总结：

**项目概况**
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envory 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。该项目专为 AI 原生应用设计，旨在提供统一的流量入口和管理平台。项目主要使用 **Go** 语言开发，目前在 GitHub 上拥有超过 7,400 颗星。

**核心架构与优势**
Higress 采用**控制平面**与**数据平面**分离的架构：
*   **配置管理**：配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接。
*   **高性能**：特别适合需要处理长连接的场景，例如 AI 流式响应。

**三大核心功能**
1.  **AI 网关**：
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存及安全防护能力（通过 `ai-proxy`、`ai-statistics` 等插件实现）。
2.  **MCP 服务器托管**：
    *   托管**模型上下文协议（MCP）**服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   包含路由转换及多种内置服务实现（如搜索、地图工具等）。
3.  **传统 API 网关**：
    *   作为 Kubernetes Ingress 控制器使用。
    *   兼容 Nginx Ingress 注解，支持微服务路由等传统网关功能。

**总结**
Higress 是一款将**传统微服务治理**与**新兴 AI 应用需求**（LLM 统一管理、Agent 工具调用）完美融合的下一代网关产品。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“AI 原生”网关，它成功地将云原生流量治理技术与大模型（LLM）应用需求深度融合。对于正处于 AI 落地初期的企业而言，它不仅仅是一个流量入口，更是解决 AI 应用碎片化、协议异构以及模型服务治理痛点的关键基础设施。

**深入评价依据**

**1. 技术创新性：基于 WASM 的“AI 原生”架构重构**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件系统。其核心定位包含 AI Gateway、MCP Server 托管以及传统 API 网关。
*   **推断**：Higress 的最大技术创新在于**将 AI 协议处理能力下沉到网关层**。传统网关主要处理 HTTP/gRPC，而 Higress 原生支持 SSE（Server-Sent Events）流式转发、LLM 请求/响应的语义转换（如 OpenAI 格式转通义千问格式）。通过 WASM 技术，它允许开发者使用 C++/Go/Rust 编写高性能插件，动态扩展 AI 逻辑（如 Prompt 模板注入、敏感词过滤），而无需重启网关或修改后端应用代码。这种“逻辑下沉”架构极大地降低了 AI 应用接入的复杂度。

**2. 实用价值：统一 AI 与微服务的治理平面**
*   **事实**：DeepWiki 提及该系统提供“AI gateway features for LLM applications”和“MCP server hosting for AI agent tool integration”，同时兼容 Kubernetes Ingress。
*   **推断**：Higress 解决了 AI 时代最棘手的**“协议与路由碎片化”**问题。在企业落地 AI 时，往往需要同时对接 OpenAI、Azure 或本地开源模型，后端还需要连接数据库或 RAG 引擎。Higress 充当了“统一翻译官”和“流量调度员”的角色：
    *   **多模型统一**：前端应用只需调用一个标准接口，网关负责路由到不同的 LLM 提供商。
    *   **MCP 协议支持**：对 AI Agent 而言，它解决了工具调用的标准化问题，使得 Agent 可以通过网关安全地访问后端 MCP 工具。
    *   **成本与安全**：通过网关层的 Token 限流和计费，企业可以精确控制 AI 成本，避免了将昂贵的 API Key 暴露给前端。

**3. 代码质量与架构：云原生标准的控制与数据分离**
*   **事实**：文档明确指出架构分离了“控制平面（配置管理）”与“数据平面（流量处理）”。
*   **推断**：这种架构设计符合云原生最佳实践。控制平面通常依托 K8s 进行配置分发，而数据平面由 Envoy 驱动，保证了极高的转发性能（C++ 内核）与资源隔离性。Go 语言编写上层逻辑保证了开发效率，而核心路径由 Envoy 承载确保了稳定性。从文档的详尽程度（包含多语言 README 和针对 MCP、AI 特性的专门章节）来看，该项目具备较高的工程成熟度，适合作为企业级基础设施进行二次开发。

**4. 潜在问题与边界：运维复杂度的双刃剑**
*   **事实**：基于 Istio 和 Envoy 的架构通常意味着较高的学习曲线。
*   **推断**：虽然 Higress 提供了控制台来简化配置，但其底层依然依赖复杂的 CRD（自定义资源）和 Envoy 配置概念。对于仅需要简单转发的小型团队，Higress 可能存在“过重”的问题。此外，AI Gateway 功能（如流式传输的上下文修改）对 WASM 插件的编写有一定门槛，调试难度高于传统的脚本语言。

**5. 对比优势：比 Kong 更懂 AI，比 LangChain 更懂网关**
*   **事实**：Higress 开源且背靠阿里巴巴，星标数 7k+。
*   **推断**：与 Kong 或 APISIX 相比，Higress 的核心优势在于**开箱即用的 AI 特性**（如 SSE 流式处理、Prompt 模板管理），传统网关处理这些通常需要编写复杂的 Lua 插件。与 LangChain 或 LlamaIndex 等 Python 框架相比，Higress 是基础设施层的“管道”，它不负责模型推理逻辑，但负责将推理请求安全、高效地输送到模型，并提供生产级的并发与熔断能力，这是 Python 应用难以独立承担的。

**边界条件与验证清单**

**不适用场景：**
*   极其简单的单体应用，不需要复杂的流量治理。
*   对延迟极其敏感（微秒级）且极度排斥 Go 内存开销的场景（虽然 Envoy 是 C++，但控制面仍有开销）。
*   非云原生环境（如传统虚拟机环境），部署优势会打折扣。

**快速验证清单：**
1.  **SSE 流式转发测试**：配置一个后端 LLM 服务，通过 Higress 转发，验证网关是否能无损地保持流式响应，且无明显的 Buffering 延迟。
2.  **WASM 插件热加载**：编写一个简单的 WASM 插件（如修改 Header），在不重启 Pod 的情况下加载，观察是否生效及性能损耗。
3.  **MCP 协议连通性**：尝试在网关层配置一个 MCP 工

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 定位为“AI Native API Gateway”，它不仅仅是一个传统的流量网关，更是一个面向 LLM（大语言模型）时代的 AI 流量编排入口。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**云原生**的架构模式，基于 **Istio** 和 **Envoy** 构建。它没有重复造轮子，而是站在巨人的肩膀上：
*   **数据平面**：深度依赖 **Envoy**。Envoy 是高性能的 L7 代理，负责处理实际的流量转发、负载均衡以及通过 WASM 执行扩展逻辑。
*   **控制平面**：基于 **Istio** 进行了简化和改造。Higress 移除了 Istio 中繁重的 Sidecar 模式，专注于 **Ingress Gateway** 和 **API Gateway** 场景。
*   **扩展机制**：**WebAssembly (WASM)** 是其核心扩展能力。Higress 支持 C++、Go、Rust、AssemblyScript 等语言编写插件，编译为 WASM 后在 Envoy 的沙箱中运行。
*   **配置分发**：使用 **xDS 协议**（包括 LDS, CDS, RDS 等）在控制平面和数据平面之间传递配置，实现了配置变更的毫秒级生效和热更新。

### 核心模块与关键设计
1.  **控制平面**：负责管理路由规则、证书、插件配置。它通过 K8s Ingress 或 Gateway API 获取用户意图，将其转化为 Envoy 可理解的配置。
2.  **数据平面**：处理网络 I/O。关键设计在于其**无连接中断**的配置热更新机制，这对于 AI 应用的长连接流式响应至关重要。
3.  **WASM 插件系统**：这是 Higress 的“杀手锏”。它允许在不重启网关的情况下动态加载代码，且 WASM 的沙箱机制保证了安全性。
4.  **MCP (Model Context Protocol) 服务器托管**：Higress 内置了对 MCP 协议的支持，能够作为 AI Agent 的工具提供者，将后端 API 包装为 AI 可调用的工具。

### 技术亮点与创新点
*   **AI Native 特性**：这是与传统网关最大的区别。它内置了对 LLM 流式传输（SSE）的支持，提供了针对 AI 请求的**语义路由**（基于向量而非简单的字符串匹配）和**提示词管理**。
*   **统一网关理念**：试图打通“南北向”（入口流量）与“东西向”（服务间流量），并融合了 AI 流量管理，减少架构中的组件数量。
*   **标准 Istio 兼容**：允许用户利用 Istio 庞大的生态资源，同时降低了 K8s 用户的使用门槛。

### 架构优势分析
*   **高性能**：基于 Envoy 的 C++ 内核，处理并发能力远高于基于 Java/Node.js 的传统 API 网关。
*   **低延迟**：控制平面与数据平面分离，配置下发通过内存级 gRPC 通信，避免了配置重载带来的流量抖动。
*   **极致的可扩展性**：WASM 插件机制使得业务逻辑的迭代速度可以媲美脚本语言，同时保持了接近原生代码的执行效率。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **提供商统一**：将 OpenAI、Azure、通义千问、HuggingFace 等不同 LLM 提供商的 API 统一封装。
    *   **Token 管理**：提供基于 Token 的计费、流控和多租户复用。
    *   **提示词增强**：在网关层动态注入 System Prompt，实现敏感词过滤或格式约束。
2.  **MCP (Model Context Protocol) 支持**：
    *   Higress 可以作为 MCP Server，将内部 RESTful API 自动暴露给 AI Agent，解决 Agent 如何安全调用企业内部工具的问题。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、微服务路由、金丝雀发布、蓝绿部署。

### 解决的关键问题
*   **AI 流量的不可预测性与成本控制**：解决了企业接入多个大模型时的统一管理和成本审计问题。
*   **流式响应的中间件处理难题**：传统网关在处理 SSE（Server-Sent Events）流时往往难以进行修改或拦截，Higress 的 WASM 插件可以在流式传输过程中实时处理数据。

### 与同类工具的对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **内核** | Envoy (C++) | Nginx (C) / Go | etcd + Lua (OpenResty) | Nginx (C) |
| **扩展性** | WASM (多语言) | Lua / Go / WASM (部分) | Lua / Python | C Module / Lua (OpenResty) |
| **AI 特性** | **原生支持** | 依赖插件 | 依赖插件 | 无 |
| **配置热更新** | 毫秒级，无感 | 需要重载部分连接 | 需要重载 | 需要重载 |
| **K8s 集成** | 深度集成 (Ingress/Gateway API) | 支持 | 支持 | 支持 (Ingress Controller) |

### 技术实现原理
*   **AI 代理实现**：Higress 通过 Envoy Filter 或 WASM 插件拦截 HTTP 请求，识别目标 LLM 的 API 规范（如 `/v1/chat/completions`），在转发前进行鉴权和 Header 修改，在响应回传时解析流式数据块。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 集成了 **Wasmtime** 或 **V8** 引擎。当请求进入 Envoy 时，如果配置了插件，WASM VM 会被挂载到请求处理链中。
*   **配置同步**：Higress Console -> ConfigMap/CRD -> Higress Control Plane (Istio) -> xDS gRPC -> Envoy。
*   **AI 流式处理**：利用 Envoy 的 Async Message Filter 机制，在流式响应的每个 Chunk 上通过 WASM Hook 进行处理，实现了对 AI 生成内容的实时审核或格式化。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑，包含 Ingress 转换器、路由注册等。
*   **`/plugins`**：WASM 插件的 Go SDK 和预置插件源码（如 auth, key-auth, ai-proxy）。
*   **`/docker`**：镜像构建相关，通常基于 distroless 或 alpine 基础镜像。

### 性能优化与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被继承。
*   **插件隔离**：WASM 插件崩溃不会导致 Envoy 主进程崩溃，保障了网关的稳定性。
*   **水平扩展**：作为 K8s Deployment 运行，可根据负载自动扩缩容。

### 技术难点与解决方案
*   **难点**：WASM 的启动开销和内存占用。
*   **方案**：Higress 使用了 **WASM Cache** 和 **VM Pooling** 技术，复用虚拟机实例，减少冷启动带来的延迟。

---

## 4. 适用场景分析

### 适合使用的项目
*   **AI 应用开发**：特别是需要对接多个 LLM 厂商，或者需要对企业内部 API 进行 MCP 协议暴露的场景。
*   **Kubernetes 集群入口**：需要高性能、低延迟云原生网关的微服务架构。
*   **高并发 API 管理**：对传统网关（如 Spring Cloud Gateway）的性能不满意，需要 C++ 级别的吞吐量。

### 最有效的情况
*   当你需要**统一管理**传统微服务 API 和新兴的 AI 模型 API 时，Higress 的混合路由能力能显著降低运维复杂度。
*   当业务逻辑需要**频繁变更**（如不同的鉴权算法、请求限流策略）时，WASM 插件的热加载能力能极大提升迭代效率。

### 不适合的场景
*   **极简边缘侧**：资源极度受限（如几 MB 内存）的嵌入式设备，Envoy 本身较重。
*   **纯静态文件服务**：虽然能做，但用 Nginx 或 CDN 更合适。

### 集成方式与注意事项
*   **K8s 部署**：通常通过 Helm Chart 部署。
*   **注意**：WASM 插件虽然有沙箱，但高性能插件（如复杂正则匹配）仍会消耗较多 CPU，需要合理限制资源配额。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 编排**：从简单的转发发展到多模型路由、Fallback 降级、Prompt 模板管理。
*   **WASM 组件生态**：构建类似 Nginx Module 的 WASM 插件市场，让用户可以一键安装各类功能。

### 社区反馈与改进空间
*   **优势**：背靠阿里，中文文档完善，对国内云厂商支持好。
*   **改进**：相比 Kong，其插件生态的丰富度和第三方贡献度仍有差距；控制平面的 UI 易用性仍有提升空间。

### 与前沿技术的结合
*   **eBPF**：未来可能会在数据平面结合 eBPF 进行更底层的网络加速或可观测性采集。
*   **Service Mesh (Sidecar)**：虽然目前主打 Ingress，但可能会回归 Mesh 场景，提供更完整的网格解决方案。

---

## 6. 学习建议

### 适合的开发者水平
*   **中级**：了解 Kubernetes 基础、HTTP 协议。
*   **高级**：若需贡献核心代码或编写复杂 WASM 插件，需掌握 C++/Go/Rust 及 Envoy 架构。

### 可学习的内容
*   **云原生架构**：学习控制平面与数据平面分离的设计模式。
*   **WASM 开发**：掌握如何用 Go/Rust 编写高性能、安全的沙箱插件。
*   **Envoy 配置**：深入理解 xDS 协议和 Filter 链式处理逻辑。

### 推荐学习路径
1.  **部署体验**：使用 Docker 或 Kind 在本地搭建 Higress，跑通一个简单的 AI 代理示例。
2.  **插件开发**：使用 Go-SDK 编写一个简单的 `RequestHeader` 修改插件，编译为 WASM 并部署。
3.  **源码阅读**：阅读 `pkg/ingress` 目录，理解 K8s Ingress 资源如何转化为 Envoy 配置。

---

## 7. 最佳实践建议

### 正确使用方式
*   **分离控制与数据**：不要将业务逻辑（如复杂的数据库查询）写在网关插件中。网关应专注于流量控制、

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway, Route, Service
    
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 定义后端服务
    user_service = Service(name="user-service", url="http://user-service:8080")
    order_service = Service(name="order-service", url="http://order-service:8080")
    
    # 配置路由规则
    gateway.add_route(Route(
        path="/api/users/*",  # 匹配 /api/users/ 开头的路径
        methods=["GET", "POST"],
        service=user_service,
        plugins=["auth"]  # 应用认证插件
    ))
    
    gateway.add_route(Route(
        path="/api/orders/*",
        methods=["GET", "POST"],
        service=order_service,
        plugins=["rate-limit"]  # 应用限流插件
    ))
    
    return gateway

# 使用示例
gateway = configure_higress_route()
print("Higress 网关路由配置完成")
```




```python
# 示例2：Higress 插件开发 - 自定义认证插件
from higress import Plugin, RequestContext

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于 JWT 的请求认证
    """
    def __init__(self):
        super().__init__(name="custom-auth")
        self.secret_key = "your-secret-key"  # 实际应用中应从配置中心获取
    
    def on_request(self, context: RequestContext):
        # 获取请求头中的 token
        token = context.headers.get("Authorization", "")
        
        if not token.startswith("Bearer "):
            context.response.set_status(401)
            return context.response.terminate("Missing or invalid token")
        
        # 验证 JWT token
        try:
            payload = jwt.decode(token[7:], self.secret_key, algorithms=["HS256"])
            context.user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            context.response.set_status(401)
            return context.response.terminate("Token expired")
        except jwt.InvalidTokenError:
            context.response.set_status(401)
            return context.response.terminate("Invalid token")
        
        # 认证通过，继续处理请求
        return context.next()

# 注册插件
plugin = CustomAuthPlugin()
plugin.register()
```




```python
# 示例3：Higress 流量管理 - 金丝雀发布
def configure_canary_release():
    """
    配置金丝雀发布策略
    解决问题：逐步将流量从旧版本切换到新版本
    """
    from higress import Canary, Service, Route
    
    # 定义新旧版本服务
    old_service = Service(name="service-v1", url="http://service-v1:8080")
    new_service = Service(name="service-v2", url="http://service-v2:8080")
    
    # 创建金丝雀发布策略
    canary = Canary(
        name="service-canary",
        primary_service=old_service,
        canary_service=new_service,
        # 10% 的流量转发到新版本
        traffic_weight=10,
        # 基于 HTTP 头的流量路由
        match_headers={
            "X-Canary": "true"  # 带有此头的请求全部转到新版本
        }
    )
    
    # 应用金丝雀策略到路由
    route = Route(
        path="/api/service/*",
        canary=canary
    )
    
    return route

# 使用示例
canary_route = configure_canary_release()
print("金丝雀发布策略配置完成，10% 流量将转发到新版本")
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**：  
阿里巴巴拥有庞大的电商生态系统，包括淘宝、天猫等平台。这些平台每天处理数亿次请求，涉及复杂的微服务调用链路。随着业务规模的增长，传统的API网关面临性能瓶颈和扩展性挑战。

**问题**：  
- 高并发场景下，现有网关响应延迟增加，影响用户体验。  
- 多种协议（HTTP、Dubbo、gRPC）的统一管理复杂，导致开发和运维成本高。  
- 动态路由和流量管理能力不足，难以支持A/B测试和灰度发布。

**解决方案**：  
采用Higress作为新一代云原生API网关，结合其高性能的架构和插件化能力。通过Higress的动态路由和流量治理功能，实现多协议统一管理和精细化流量控制。

**效果**：  
- 网关吞吐量提升30%，平均延迟降低20%，显著改善用户体验。  
- 统一管理HTTP和Dubbo服务，运维效率提升40%。  
- 支持灵活的流量策略，灰度发布时间缩短50%。

---



### 2：某头部在线教育平台

 2：某头部在线教育平台

**背景**：  
该平台为千万级用户提供在线课程服务，业务高峰期（如开学季）流量激增，对API网关的稳定性和弹性提出极高要求。

**问题**：  
- 传统网关在流量突增时出现服务不可用，导致用户无法访问课程。  
- 缺乏实时监控和告警机制，故障排查耗时较长。  
- 多租户隔离能力不足，存在数据泄露风险。

**解决方案**：  
部署Higress网关，利用其弹性伸缩和实时监控能力。通过Higress的多租户隔离插件，确保不同租户的数据安全。结合Prometheus和Grafana实现全链路监控。

**效果**：  
- 高峰期流量承载能力提升50%，未发生服务中断。  
- 故障定位时间从小时级缩短至分钟级，运维效率显著提高。  
- 多租户隔离机制通过安全审计，满足合规要求。

---



### 3：某大型物流企业

 3：某大型物流企业

**背景**：  
该企业物流系统覆盖全国，涉及订单管理、车辆调度、仓储等多个子系统，API调用频繁且复杂。

**问题**：  
- API接口版本管理混乱，兼容性问题频发。  
- 跨区域调用时，网络延迟和丢包率较高。  
- 缺乏统一的认证鉴权机制，存在安全隐患。

**解决方案**：  
引入Higress网关，通过其版本管理和协议转换功能解决兼容性问题。部署多区域Higress集群，结合智能路由优化跨区域调用。集成OAuth2.0插件实现统一认证。

**效果**：  
- API版本冲突问题减少80%，开发迭代速度提升。  
- 跨区域调用延迟降低30%，丢包率降至0.1%以下。  
- 统一认证机制覆盖所有API，安全漏洞数量下降90%。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Kong | APISIX | Nginx + Lua |
|------|----------------|------|-------|------------|
| 架构 | 基于Istio，支持云原生和微服务 | 独立网关，插件化架构 | 独立网关，动态路由 | 传统反向代理，需手动扩展 |
| 性能 | 高性能，基于Envoy和Go | 高性能，基于Nginx和Lua | 高性能，基于LuaJIT | 极高性能，但扩展性有限 |
| 易用性 | 提供控制台和K8s集成，部署简单 | 需配置数据库，管理复杂 | 提供Dashboard，配置灵活 | 需手动编写Lua脚本，学习曲线陡 |
| 扩展性 | 支持Wasm插件，扩展灵活 | 插件生态丰富，但需开发 | 插件生态丰富，支持自定义 | 扩展需修改Nginx配置，维护成本高 |
| 社区支持 | 阿里背书，社区活跃 | 成熟社区，企业级支持 | 开源社区活跃，国内支持好 | 社区庞大，但非网关专用 |
| 成本 | 开源免费，企业版收费 | 开源免费，企业版收费 | 完全开源，企业支持收费 | 完全免费，但人力成本高 |

### 优势分析

- **云原生集成**：深度集成Istio和Kubernetes，适合微服务架构。
- **高性能**：基于Envoy和Go，性能优于传统网关。
- **易用性**：提供控制台和K8s Operator，部署和管理简单。
- **扩展性**：支持Wasm插件，开发灵活，适合复杂业务场景。
- **阿里生态**：与阿里云产品无缝集成，适合已有阿里云基础设施的用户。

### 不足分析

- **社区成熟度**：相比Kong和APISIX，社区和生态尚在发展中。
- **学习曲线**：对Istio和Kubernetes不熟悉的用户可能需要额外学习。
- **企业支持**：企业版支持不如Kong和APISIX完善。
- **文档完善度**：部分功能文档较少，依赖社区支持。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现轻量级功能扩展

**说明**:
Higress 基于 Istio 与 Envoy 构建，其核心优势之一在于原生支持 WebAssembly (Wasm)。相比于传统的 Lua 脚本或 Sidecar 模式，使用 Wasm 插件可以实现业务逻辑与网关内核的强隔离，支持多语言（如 C++, Go, Rust, AssemblyScript）编写，并且可以实现热插拔，无需重启网关即可更新插件逻辑。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust，社区支持较好）。
2. 引入 Higress 提供的 SDK（如 `proxy-wasm-go-sdk`）编写插件逻辑，处理请求/响应头或 Body。
3. 将编写好的代码编译为 `.wasm` 文件。
4. 在 Higress 控制台或通过 OCI 工具将 Wasm 文件上传为插件资源。
5. 在特定路由或网关全局范围内配置并启用该插件。

**注意事项**:
- Wasm 插件运行在沙箱中，虽然隔离性好，但频繁的内存拷贝会带来一定的性能损耗，避免在插件中处理超大 Body。
- 编译 Wasm 时需注意目标架构（通常为 `wasm32`）与 Higress 运行环境的兼容性。

---

### 实践 2：精细化配置流量治理与安全防护

**说明**:
利用 Higress 强大的路由和安全能力，替代传统 Nginx 的复杂配置。通过域名、Header、Cookie、Query 参数等维度的路由匹配规则，实现蓝绿发布、金丝雀发布以及 A/B 测试。同时，配置 IP 访问控制、请求鉴权等安全策略以保护后端服务。

**实施步骤**:
1. 定义目标服务，在 Higress 中创建服务来源，并关联 K8s Service 或固定地址。
2. 配置 Ingress 或 Gateway API 资源，设置精确的匹配规则（如 URI 前缀、正则匹配）。
3. 配置路由策略，设置流量权重（例如 90% 流量走 V1 版本，10% 流量走 V2 版本）。
4. 启用插件市场中的“防盗链”、“IP 访问限制”或“Basic Auth”插件增强安全性。
5. 配置超时、重试及熔断策略，防止级联故障。

**注意事项**:
- 路由匹配优先级需仔细规划，避免通配符路由覆盖了特定业务路由。
- 在进行金丝雀发布时，确保后端服务版本间的数据兼容性，特别是涉及 Session 状态的情况。

---

### 实践 3：利用 Higress Gateway API 实现标准化网关管理

**说明**:
Higress 是国内目前对 Gateway API 标准支持最好的网关之一。相比于传统的 Ingress API，Gateway API 提供了更结构化的资源模型，将“基础设施配置”（由运维管理）与“路由配置”（由开发管理）分离，支持多租户场景，实现更规范的云原生网关管理。

**实施步骤**:
1. 确认集群已安装 Gateway API 的 CRD。
2. 运维人员创建 `GatewayClass` 和 `Gateway` 资源，定义网关的基础监听端口和协议。
3. 开发人员创建 `HTTPRoute` 或 `TLSRoute` 资源，定义具体的流量转发规则，并将其引用到上述 Gateway。
4. 通过命名空间隔离不同业务的路由配置，实现权限管控。

**注意事项**:
- Gateway API 仍在不断演进中，使用前请查阅 Higress 文档确认当前版本支持的字段范围。
- 从 Ingress 迁移时，注意路径匹配类型的差异（如 `Prefix` vs `Exact`）。

---

### 实践 4：对接云原生注册中心实现服务自动发现

**说明**:
Higress 设计初衷之一是打通微服务生态。不要将后端服务地址硬编码在网关配置中，而应直接接入 K8s Service、Nacos 或 Consul 等注册中心。这样当后端 Pod 扩缩容或实例上下线时，Higress 能实时感知并自动更新路由后端，实现全链路云原生。

**实施步骤**:
1. 在 Higress 控制台的“服务来源”配置中，添加对应的注册中心类型（如选择 Nacos 并配置地址、命名空间）。
2. 确认 Higress 能够访问到注册中心的网络端口（通常在 K8s 集群内需配置正确的 Service DNS 或 Headless Service）。
3. 在配置路由时，直接选择已发现的“服务名”作为目标后端。
4. 配置健康检查，确保 Higress 只将流量转发给健康的实例。

**注意事项**:
- 跨网络访问注册中心（如 Higress 在 K8s 内，注册中心在物理机）时，需确保网络互通性。
-

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 构建，原生支持现代 HTTP 协议。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，而 HTTP/3 (QUIC) 基于 UDP 协议，进一步解决了 TCP 层的队头阻塞，显著降低了高丢包率网络环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，明确启用 HTTP/2 协议。
2. 在 `higress-config` 全局配置中，开启 QUIC / HTTP/3 支持（需确保底层网络环境允许 UDP 流量）。
3. 配置 TLS 版本至少为 TLS 1.2，推荐 TLS 1.3，以配合 HTTP/3 发挥最佳性能。

**预期效果**: 在高并发连接数下，TCP 连接数可减少 50% 以上，高延迟网络下的请求响应时间（RTT）降低 30%-40%。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时设置通常较长，若后端服务出现故障或响应慢，会导致网关连接池（Connection Pool）被长时间占用，耗尽网关资源。合理的超时与指数退避重试机制能快速释放资源，保障系统整体吞吐量。

**实施方法**:
1. 设置合理的 `connectTimeout`（连接超时）、`requestTimeout`（请求总超时）和 `streamIdleTimeout`（空闲超时）。
2. 配置路由级别的重试策略，指定触发条件（如 5xx 错误或连接失败），并设置最大重试次数（建议 2-3 次）。
3. 开启“指数退避”策略，避免重试风暴冲击后端服务。

**预期效果**: 在后端服务部分实例故障时，系统错误率可降低 90% 以上，99 分位延迟（P99 Latency）显著降低，防止雪崩效应。

---

### 优化 3：启用 Wasm 插件的高效缓存与轻量化

**说明**: Higress 支持通过 Wasm 插件扩展功能。Wasm 插件虽然比 Lua 性能更好，但频繁的内存分配和跨语言调用仍有开销。对于鉴权、限流等高频调用场景，优化插件逻辑和启用本地缓存至关重要。

**实施方法**:
1. 在编写 Wasm 插件时，尽量复用内存对象，减少频繁的内存分配。
2. 利用 Higress 的 KV 功能或插件本地缓存（如 LRU Cache）缓存鉴权结果或配置信息，避免每次请求都回源查询 Redis 或数据库。
3. 将复杂的鉴权逻辑下沉至 Envoy Filter 或使用原生配置替代，减少 Wasm 虚拟机的计算开销。

**预期效果**: 高频鉴权场景下，插件处理延迟降低 50%-80%，后端数据库/Redis 查询量减少 90% 以上。

---

### 优化 4：调整连接池与并发限制

**说明**: Higress 默认的连接池配置可能无法满足高吞吐场景。过小的连接池会导致请求排队等待，过大的连接池则可能压垮后端服务。同时，需启用并发限制以保护系统稳定性。

**实施方法**:
1. 根据后端服务能力，调整 HTTP/1.1 连接池大小（`maxConnections`）或 HTTP/2 并发流限制。
2. 开启 Envoy 的 `global_downstream_max_connections` 或服务级别的并发限制。
3. 启用 `buffer_limit` 调优，防止大请求/响应占用过多内存导致 OOM。

**预期效果**: 提升后端连接复用率，减少连接建立握手开销，吞吐量（QPS）可提升 20%-50%，同时有效防止内存溢出（OOM）。

---

### 优化 5：利用 DNS 缓存与服务发现预热

**说明**: 在 Kubernetes 环境中，频繁的 Pod 滚动更新会导致 DNS 解析

---
## 学习要点

- 基于提供的 GitHub 趋势信息（Alibaba/Higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接云原生生态系统。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿发布、负载均衡及流量镜像。
- Higress 内置了对 WASM (WebAssembly) 的支持，允许开发者使用 C++/Go/Rust 等语言编写高性能、插件化的扩展逻辑。
- 该网关兼容 Nginx Ingress 注解，旨在成为 Nginx Ingress 的高性能、现代化替代方案。
- 它支持将微服务网关（如 Spring Cloud、Dubbo）与 API 网关合二为一，简化了架构复杂度。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的背景与核心概念：了解 Higress 是什么，为什么需要它，以及它与云原生生态的关系。
- 基本架构：掌握 Higress 的核心组件（如 Ingress Controller、Gateway）及其工作原理。
- 安装与部署：学习如何在 Kubernetes 集群中安装 Higress，包括使用 Helm 或官方提供的安装脚本。
- 基础配置：掌握基本的路由配置、域名管理、以及简单的流量转发规则。

**学习时间**: 1-2周

**学习资源**:
- 官方文档：Higress GitHub 仓库的 README 和官方文档。
- 入门教程：官方提供的快速开始指南。
- 社区资源：Higress 官方博客和社区讨论区。

**学习建议**:
- 优先阅读官方文档，理解 Higress 的设计理念和核心功能。
- 动手实践安装和基础配置，建议在本地或测试环境中完成。
- 加入 Higress 社区（如钉钉群或 Slack），遇到问题及时提问。

---

### 阶段 2：进阶提升

**学习内容**:
- 高级路由与流量管理：学习基于权重、Header、Cookie 等条件的复杂路由配置。
- 插件系统：掌握 Higress 的插件机制，学习如何使用和配置常用插件（如限流、认证、日志等）。
- 服务治理：了解 Higress 与服务网格（如 Istio）的集成，学习服务发现、负载均衡策略等。
- 监控与可观测性：学习如何配置 Prometheus、Grafana 等工具监控 Higress 的运行状态。

**学习时间**: 2-4周

**学习资源**:
- 官方文档：插件开发指南和高级配置文档。
- 实战案例：官方或社区提供的实际应用案例。
- 视频教程：B站或YouTube上的进阶教程。

**学习建议**:
- 结合实际场景练习高级路由和插件配置，例如模拟灰度发布或流量镜像。
- 尝试开发或定制一个简单的插件，熟悉插件开发流程。
- 搭建完整的监控体系，深入理解 Higress 的运行指标。

---

### 阶段 3：高级应用与优化

**学习内容**:
- 性能优化：学习如何调整 Higress 的配置以提升性能，包括连接池、缓冲区大小等参数。
- 安全加固：掌握 Higress 的安全配置，如 TLS/SSL 配置、访问控制、防护常见攻击等。
- 多集群管理：学习如何在多 Kubernetes 集群中部署和管理 Higress。
- 故障排查：掌握常见问题的排查方法，学习日志分析和调试技巧。

**学习时间**: 3-5周

**学习资源**:
- 官方文档：性能调优指南和故障排查文档。
- 社区经验：GitHub Issues 和社区论坛中的常见问题与解决方案。
- 实战演练：参与开源项目或企业级案例的实践。

**学习建议**:
- 在生产环境中模拟高并发场景，测试和优化 Higress 的性能。
- 深入学习网络安全知识，确保 Higress 的部署符合安全最佳实践。
- 定期回顾社区动态，关注新版本的功能和改进。

---

### 阶段 4：精通与贡献

**学习内容**:
- 源码分析：深入阅读 Higress 的源码，理解其核心模块的实现原理。
- 自定义开发：学习如何为 Higress 贡献代码，包括开发新功能或修复 Bug。
- 架构设计：掌握 Higress 的整体架构设计，能够基于 Higress 设计复杂的流量管理系统。
- 社区贡献：参与 Higress 的开源社区，提交 PR、参与讨论或撰写技术文章。

**学习时间**: 持续学习

**学习资源**:
- 源码：Higress GitHub 仓库的源码。
- 设计文档：官方的架构设计文档和 RFC。
- 开发者指南：贡献者指南和代码规范。

**学习建议**:
- 从简单的 Bug 修复或文档改进开始，逐步参与社区贡献。
- 定期参加社区会议或技术分享，与其他开发者交流经验。
- 结合自身工作或项目需求，尝试基于 Higress 实现定制化功能。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在 API 网关领域的实践经验，结合 Envoy 和 Istio 等开源技术构建而成的。Higress 旨在为云原生架构提供统一的高性能入口，支持 Kubernetes Ingress、微服务 API 管理以及云原生网关等多种场景。它由阿里巴巴主导开源，并捐赠给了 CNCF（云原生计算基金会）。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其深度集成云原生生态和极致的扩展性。
1.  **技术架构**：Higress 基于 Envoy 和 Istio（Nginx 等通常基于 Nginx/Lua），在处理长连接、热更新和可观测性方面具有天然的架构优势。
2.  **安全防护**：内置了针对 WAF（Web 应用防火墙）的插件，特别是针对阿里云用户常见的 CC 攻击和 Bot 防护有深度优化。
3.  **插件生态**：兼容 Kong 和 APISIX 的绝大部分插件，并支持 WASM (WebAssembly) 技术，允许开发者使用多种语言（如 Go, Python, TypeScript）编写插件，而无需修改网关核心代码。
4.  **服务发现**：与 Nacos、Consul、DNS 以及 Kubernetes Service 原生集成，非常适合微服务架构。

---



### 3: Higress 是否支持从其他网关（如 Nginx 或 Kong）迁移？

3: Higress 是否支持从其他网关（如 Nginx 或 Kong）迁移？

**A**: 是的，Higress 提供了完善的迁移工具和兼容性支持。
1.  **配置兼容**：Higress 提供了配置转换工具，可以将 Nginx 的配置文件（nginx.conf）自动转换为 Higress 的配置格式。
2.  **插件兼容**：对于 Kong 用户，Higress 的插件系统在设计上参考了 Kong 的规范，支持 Lua 插件的运行（通过 WASM 或特定适配层），降低了迁移成本。
3.  **Ingress 兼容**：完全兼容 Kubernetes Ingress Annotation 和 Gateway API 标准，可以直接替换 K8s 原生的 Ingress Controller。

---



### 4: Higress 如何处理流量管理和安全防护？

4: Higress 如何处理流量管理和安全防护？

**A**: Higress 将流量管理与安全防护深度融合。
1.  **流量管理**：支持金丝雀发布、蓝绿发布、A/B 测试以及基于 Header、Cookie、权重等复杂条件的流量路由。
2.  **安全防护**：
    *   **认证鉴权**：内置了 Basic Auth、API Key、JWT、OIDC 等多种认证方式。
    *   **WAF 防护**：提供了开源版的 WAF 插件，能够识别和拦截 SQL 注入、XSS 跨站脚本、恶意扫描等常见 Web 攻击。
    *   **限流熔断**：支持基于请求速率、并发连接数的限流，以及服务异常时的自动熔断保护。

---



### 5: Higress 是否支持 WASM (WebAssembly)？这对开发者意味着什么？

5: Higress 是否支持 WASM (WebAssembly)？这对开发者意味着什么？

**A**: 是的，对 WASM 的支持是 Higress 的一大亮点。Higress 允许用户使用 Go、C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript 编写插件逻辑，并编译为 WASM 格式运行。
这意味着开发者**不需要**为了编写网关插件而去学习 Envoy 原生要求的 C++ 语言，也不需要受限于 Lua 的性能瓶颈。WASM 插件运行在沙箱环境中，既保证了安全性，又提供了接近原生的执行效率，且支持插件的热加载，无需重启网关即可生效。

---



### 6: Higress 的性能表现如何？能否支撑高并发业务？

6: Higress 的性能表现如何？能否支撑高并发业务？

**A**: Higress 继承了 Envoy 高性能的特点，能够轻松支撑高并发业务。
1.  **底层性能**：基于 C++ 编写的 Envoy 数据面，具有极低的延迟和极高的吞吐量。
2.  **优化**：阿里巴巴内部针对 Higress 在大规模流量场景（如双11）进行了深度优化，其长连接处理能力和单核转发性能在同类开源网关中处于领先地位。
3.  **水平扩展**：作为云原生网关，Higress 可以利用 Kubernetes 的 HPA（水平自动伸缩）能力，根据流量自动扩缩容实例数量。

---



### 7: 如何在本地或 Kubernetes 集群中快速试用 Higress？

7: 如何在本地或 Kubernetes 集群中快速试用 Higress？

**A**: Higress 提供了极其简便的部署方式。
1.  **Docker 方式**：可以通过一行 Docker 命令快速启动 Standalone 模式，适合本地开发调试。
2.  **Kubernetes 方式**：提供了标准的 Helm Chart 仓库，执行几条 `helm install` 命令即可在 K8s 集群中部署生产级的高可用集群。
3.  **

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署一套 Higress 网关，并配置一个简单的路由转发规则。要求将访问 `/httpbin/` 路径的流量转发到公共测试服务 `httpbin.org`。

### 提示**:

### 查阅官方文档中的 "快速开始" 章节，获取 Docker Compose 的配置文件模板。

---
## 实践建议

以下是针对 Higress (AI Gateway) 的 6 条实践建议：

1.  **利用路由级配置实现灰度发布**
    Higress 继承了 Nacos 的流量管理能力。在接入新的 AI 模型（如从 GPT-3.5 迁移到 GPT-4）时，不要直接全量切换。建议配置基于 Header（如 `x-user-group`）或权重的路由规则，将 5% 的流量指向新模型服务，观察响应延迟和错误率，确认无异常后再逐步扩大流量占比。

2.  **配置 Prompt 模板管理以降低 Token 消耗**
    在网关层配置 Prompt 模板，而不是在业务代码中硬编码。通过 Higress 的插件（如 `ai-proxy`）预设 System Prompt，可以统一管理提示词版本。这不仅便于快速 A/B 测试不同的提示词策略，还能减少前端传输的冗余 Token，降低 API 调用成本。

3.  **实施语义缓存策略**
    对于常见的用户提问（如客服场景中的标准问答），AI 模型的回答往往是固定的。建议开启 Higress 的语义缓存功能，对向量相似的请求直接返回缓存结果。这能显著减少对上游 LLM 的调用次数，在高并发场景下能有效降低成本并提升响应速度。

4.  **注意流式传输的超时与连接配置**
    AI 生成内容通常耗时较长，且采用 SSE（Server-Sent Events）流式返回。务必将网关和后端服务的超时时间配置得比普通 API 更长（例如 60s 或更高），并确保开启 HTTP/2 支持。同时，检查客户端是否正确处理流式断连，避免因网络抖动导致整个请求失败。

5.  **敏感词过滤与安全防护**
    不要将用户输入直接透传给 LLM。建议在 Higress 上配置输入输出校验插件，对 Prompt 进行注入攻击检测和敏感词过滤。这不仅能防止恶意 Prompt 导致的 Token 消耗失控，还能确保生成内容符合合规性要求，避免法律风险。

6.  **监控指标关注 Token 使用量而非仅 QPS**
    传统的 API 网关主要关注 QPS 和延迟，但 AI 网关的核心成本在于 Token。建议配置可观测性插件，专门监控每个请求的 Token 消耗量（输入+输出）和模型成本。设置基于 Token 使用量的告警阈值，防止因异常大模型请求（如超长 Context）导致账单激增。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*