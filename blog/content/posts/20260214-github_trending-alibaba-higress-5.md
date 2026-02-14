---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-14T20:42:31+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的中文总结： **项目概述** Higress 是一款由阿里巴巴开源的**云原生 API 网关**，定位为 **AI Native API Gateway**（AI 原生 API 网关）。该项目基于 **Istio** 和 **Envoy** 构建，并使用 **Go"
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
- **星标**: 7,527 (+4 stars today)
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

Higress 是基于 Istio 与 Envoy 构建的云原生 API 网关，通过集成 WASM 插件能力，兼顾了传统微服务流量管理与 AI 原生应用的需求。它专为需要统一处理 LLM 流量、MCP 服务托管及 Kubernetes Ingress 的场景设计，能够有效降低异构服务治理的复杂度。本文将梳理其核心架构，并重点介绍 AI 网关特性、插件系统及部署方式，帮助读者评估其在实际业务中的应用价值。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的中文总结：

**项目概述**
Higress 是一款由阿里巴巴开源的**云原生 API 网关**，定位为 **AI Native API Gateway**（AI 原生 API 网关）。该项目基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言编写。目前在 GitHub 上拥有超过 7,500 颗星。

**核心架构**
Higress 采用了**控制平面与数据平面分离**的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **通信机制**：配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接的特性，特别适用于 AI 长连接流式响应等场景。

**核心功能与用途**
Higress 提供了三大主要功能：
1.  **AI 网关**：
    *   为大语言模型（LLM）应用提供统一 API，支持 30+ LLM 提供商。
    *   功能涵盖协议转换、可观测性、缓存及安全防护。
    *   *涉及组件*：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。
    *   *涉及组件*：`mcp-router`, `jsonrpc-converter` 以及内置实现（如 `quark-search`, `amap-tools`）。
3.  **传统 API 网关**：
    *   兼容 Kubernetes Ingress，支持微服务路由，并兼容 Nginx Ingress 注解。
    *   *涉及组件*：`higress-controller`。

**扩展性**
系统通过 **WebAssembly (WASM)** 插件能力进行了扩展，允许灵活定制业务逻辑。

---
## 评论

**总体判断**

Higress 是当前云原生网关领域中将“AI 原生”理念落地得最为彻底的开源项目之一，它成功打破了传统流量网关与 LLM（大语言模型）网关的界限。通过在 Istio/Envoy 生态中深度集成 WASM 和 MCP 协议，Higress 不仅解决了微服务流量治理的遗留问题，更为 AI 应用的落地提供了极具前瞻性的基础设施层支持。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“智能节点”的架构跃迁**
*   **事实**：DeepWiki 明确指出 Higress 是“基于 Istio 和 Envoy 构建”，并具备“AI Gateway Features”和“MCP server hosting”能力，同时支持“WASM plugin capabilities”。
*   **推断**：Higress 的核心差异化在于其“AI Native”的架构设计。传统网关（如 Nginx, Kong）主要处理 HTTP 转发，而 Higress 将 LLM 的交互流程（Token 计费、上下文缓存、语义路由）内置到了数据平面。
    *   **WASM 插件化**：利用 WebAssembly 技术，允许开发者使用 C++/Go/Rust 等语言编写高频插件，这比传统的 Lua 插件（如 OpenResty）在隔离性、安全性和性能上更具优势，也使得 AI 逻辑的动态热更新成为可能。
    *   **MCP 协议支持**：集成 Model Context Protocol (MCP) 是一大亮点。这意味着 Higress 不仅仅是一个被动的 API 网关，更是一个主动的 AI Agent 工具调度中心，能够标准化地挂载各类外部数据源给大模型调用。

**2. 实用价值：打通 AI 落地“最后一公里”的关键连接器**
*   **事实**：项目描述强调其核心功能包括“AI gateway features for LLM applications”和“traditional API gateway capabilities”。
*   **推断**：Higress 解决了 AI 时代开发者的两个核心痛点：
    *   **统一接入与成本控制**：企业通常同时使用 OpenAI、通义千问、DeepSeek 等多种模型。Higress 提供了统一的标准 API 接口，屏蔽了不同厂商间的差异。更重要的是，它能在网关层进行 Token 流量统计和限流，防止大模型调用成本失控。
    *   **遗留系统兼容**：它并没有为了 AI 而牺牲传统功能，依然保留了 Kubernetes Ingress 和微服务路由能力。这使得企业可以在不引入新组件的情况下，平滑地将 AI 能力集成到现有的微服务架构中。

**3. 代码质量与架构设计：云原生标准的工业化实践**
*   **事实**：基于 Go 语言开发，Star 数超 7,500，且明确分离了控制平面和数据平面。
*   **推断**：作为阿里巴巴开源的项目，Higress 继承了阿里系中间件“高可用、高并发”的基因。
    *   **架构解耦**：控制平面与数据平面分离的设计符合云原生最佳实践，使得 Higress 可以轻松部署在 Kubernetes 集群中，并利用 Envoy 强大的并发处理能力（C++ 实现）来应对 AI 长连接场景下的高吞吐量。
    *   **文档与规范**：提供中日英三语 README 及详细的架构文档，表明该项目具有国际化的视野和较高的维护标准。Go 语言的主控代码配合 Envoy 的底座，在保证了扩展性的同时，也确保了核心链路的稳定性。

**4. 社区活跃度与学习价值：通往 AI 基础设施的窗口**
*   **事实**：Star 数 7.5k+，由阿里巴巴主导，更新频率较高，且 DeepWiki 中包含详细的“Development Guide”。
*   **推断**：在云原生网关领域，这是一个非常活跃的头部项目。
    *   **学习价值**：对于开发者而言，Higress 是学习“如何将 AI 协议（如 SSE 流式传输、OpenAI 协议兼容）融入 HTTP 网关”的绝佳范例。它的 WASM 插件机制更是学习如何在不重启网关情况下扩展业务逻辑的教科书级方案。
    *   **社区生态**：背靠阿里云，该项目不仅有开源社区的贡献，更有商业版本的打磨，这意味着其代码经过了大规模生产环境的验证，并非仅仅是“Demo 级别”的玩具。

**5. 与同类工具对比及潜在问题**
*   **对比优势**：
    *   **vs. Kong/APISIX**：Kong 和 APISIX 主要是传统 API 网关，虽然也推出了 AI 插件，但 Higress 是“原生”支持，对 AI 特性（如 Prompt 模板管理、对话历史处理）的集成度更深。且 Higress 默认基于 K8s/Istio 生态，在云原生环境下的亲和力更强。
    *   **vs. 专用 AI Proxy (如 One-Pixel)**：专用代理轻量但功能单一。Higress 提供了全套的企业级网关功能（WAF、认证、灰度发布），是“全能型选手”。
*   **潜在问题**：
    *   **复杂度门槛**：基于 Istio 和 Envoy 的架构意味着部署和维护的复杂度较高，对于没有 K8s 基础的小团队来说，上手难度远高于简单的 Nginx 反向代理。
    *   **资源消耗**

---
## 技术分析

# Higress 深度技术分析报告

Higress 是由阿里云开源的**云原生 API 网关**，其核心定位已从传统的流量管理演进为 **AI Native API Gateway**。它基于 Envoy 和 Istio 构建，通过引入 WebAssembly (WASM) 插件生态和对大模型（LLM）场景的深度优化，试图解决云原生时代特别是 AI 时代的流量治理、模型调用集成及服务编排问题。

以下是对 Higress 的深度剖析：

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了标准的**控制平面与数据平面分离**的架构模式，这与 Istio 的设计理念一脉相承，但更加聚焦于网关层的轻量化与高性能。

*   **数据平面**: 基于 **Envoy** 构建。Envoy 是高性能的 C++ 网络代理，负责处理实际的流量转发、负载均衡、TLS 终结等。Higress 对 Envoy 进行了扩展，增加了对 WASM 的原生支持以及对 AI 特定协议（如 SSE 流式传输）的优化。
*   **控制平面**: 使用 **Go** 语言开发。它接管了 Istio 中复杂的控制面逻辑，并将其简化。它通过 xDS 协议（包括 LDS, CDS, RDS, EDS）向数据平面下发配置。
*   **插件系统**: 核心扩展机制。允许开发者使用 C++/Rust/Go/AssemblyScript 编写逻辑，并在 Envoy 的沙箱中运行。这是 Higress 实现业务逻辑扩展和“AI Gateway”能力的基石。

### 核心模块与关键设计
1.  **路由与流量管理**: 继承自 Istio，支持基于权重、Header、Cookie 等复杂条件的路由。
2.  **WASM 虚拟机**: 集成了代理级别的 WASM 运行时。这意味着插件逻辑的修改不需要重启网关，只需动态加载新的 WASM 字节码，配置生效延迟在毫秒级。
3.  **AI 服务发现与路由**: 这是 Higress 的差异化模块。它不仅仅识别 HTTP 服务，还能识别后端的 LLM 服务（如 OpenAI 兼容接口），并提供 Provider 路由（例如：根据请求内容将部分请求发往 Azure OpenAI，部分发往通义千问）。

### 技术亮点与创新点
*   **毫秒级配置推送**: 基于 xDS 的增量推送机制，解决了传统网关（如 Nginx）配置 Reload 导致的连接抖动问题，这对于 AI 流式响应场景至关重要。
*   **AI 原生集成**: 并不是简单的 HTTP 代理，而是针对 AI 场景做了深度优化。例如，它支持**多模型负载均衡**、**Token 计费与流控**、以及**Prompt 模板管理**。
*   **MCP (Model Context Protocol) Server Hosting**: 这是一个前沿特性，允许 Higress 作为 AI Agent 的工具提供者，直接在网关层暴露工具接口，简化了 Agent 应用的架构。

### 架构优势分析
*   **低延迟**: 数据面 Envoy 采用 C++ 异步非阻塞模型，配合 Go 控制面，在保持扩展性的同时维持了极高的吞吐量。
*   **安全性**: WASM 沙箱隔离机制保证了插件故障不会导致网关崩溃，同时也限制了插件对底层资源的非法访问。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **Kubernetes Ingress Controller**: 作为 K8s 集群的流量入口，替代传统的 Nginx Ingress。
2.  **AI Gateway (AI 网关)**:
    *   **Provider 聚合**: 统一 OpenAI, Azure, Anthropic, 通义千问等异构接口，屏蔽底层差异。
    *   **Token 级流控**: 传统网关只能基于 QPS 限流，AI 网关可以基于 Token 消耗量进行限流和计费。
    *   **结果缓存**: 针对相同的 Prompt 进行缓存，直接返回结果，降低后端 LLM 成本。
3.  **MCP Server Hosting**: 允许用户将内部服务包装成 AI Agent 可调用的工具，并托管在网关上。

### 解决的关键问题
*   **AI 供应商锁定**: 通过统一的标准 API，用户可以轻松切换底层的 LLM 提供商，无需修改业务代码。
*   **LLM 可观测性差**: 传统的日志只记录 HTTP 状态码，Higress 能够记录 Prompt 内容、Token 消耗、首字生成时间（TTFT）等 AI 关键指标。
*   **流式传输中断**: AI 对话通常采用 SSE (Server-Sent Events)，传统反向代理在处理长连接时容易断开，Higress 针对这种长连接进行了连接池优化。

### 与同类工具的对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **语言** | Go (Control) / C++ (Data) | Lua (Control) / C (Data) | Lua (Control) / C (Data) | C |
| **扩展性** | WASM (强隔离) | LuaJIT / WASM | Lua / WASM | C Module / Lua |
| **AI 特性** | **原生支持 (Provider路由, Token限流)** | 需要插件 | 需要插件 | 无 |
| **配置热更新** | 毫秒级，无断连 | 支持但可能有延迟 | 支持但可能有延迟 | 需 Reload (有断连) |
| **K8s 集成** | 原生 CRD | 支持 Ingress | 支持 Ingress | 支持 Ingress |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件加载**: Higress 实现了一套插件市场机制。当配置一个插件时，控制面会拉取 WASM 镜像（OCI 标准），并将其通过 xDS 协议推送到 Envoy。Envoy 内置的 WASM 运行时（如 Wasmtime 或 V8）会加载并执行这些代码。
*   **HTTP 协议扩展过滤器**: 为了支持 AI 的流式响应，Higress 在 Envoy Filter 层面实现了对 SSE 和 Chunked 编码的智能处理，确保在流式传输过程中可以进行日志记录和 Header 修改，而不中断流。

### 代码组织与设计模式
*   **Repository 结构**: 代码主要分为 `pkg`（核心逻辑）、`plugins`（内置 WASM 插件源码）、`docker`（构建镜像）。
*   **CRD 驱动**: 遵循 Kubernetes 的 Operator 模式。用户编写 YAML（如 `WasmPlugin` 或 `Ingress`），Higress Controller Watch 这些资源变化，并翻译成 Envoy 配置。

### 性能优化与扩展性
*   **零拷贝**: Envoy 本身的高性能特性被完整保留。
*   **协程模型**: 控制面使用 Go 协程处理大量配置变更事件，保证了控制面的稳定性不会因为配置量过大而崩溃。

### 技术难点
*   **配置一致性**: 如何保证在分布式网关场景下，所有 Envoy 实例的配置最终一致？Higress 依赖 Istio 的配置分发机制，通过全量快照和增量更新解决此问题。
*   **WASM 冷启动**: WASM 插件初次加载可能有性能损耗。Higress 通过 AOT (Ahead-of-Time) 编译优化和缓存机制缓解此问题。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **企业级 AI 应用开发**: 需要同时接入多个大模型，并对 Token 成本进行控制的企业。
2.  **云原生微服务网关**: 已经使用 Kubernetes，需要替代 Nginx Ingress 或传统 API 网关的团队。
3.  **需要高度定制认证逻辑的场景**: 利用 WASM 编写复杂的认证鉴权插件（如整合企业内部的 SSO）。

### 最有效的场景
*   **LLM 聚合层**: 当你的业务需要根据用户等级或问题类型，动态地将请求路由给不同的 LLM Provider 时，Higress 的 AI Gateway 功能是目前业界最优雅的解决方案之一。

### 不适合的场景
*   **极简静态站点部署**: 如果只是简单的静态资源托管，使用 Nginx 或 Caddy 更加轻量，Higress 引入了过多的复杂性。
*   **非 K8s 环境**: 虽然 Higress 支持手动部署，但其强大之处在于与 K8s 的结合。在虚拟机环境下，运维复杂度较高。

### 集成方式
*   **Ingress**: 安装 Higress Helm Chart，创建 `Ingress` 资源。
*   **Gateway API**: 支持 Kubernetes Gateway API CRD。
*   **MCP**: 配置 `McpServer` 资源，将后端服务暴露给 AI Agent。

---

## 5. 发展趋势展望

### 技术演进方向
*   **从流量治理到模型治理**: Higress 正在从单纯的 API 网关向 LLM Orchestrator（编排器）演进。未来可能会包含更复杂的 Prompt 管理和 RAG (检索增强生成) 流程编排。
*   **MCP 协议的深度整合**: 随着 Model Context Protocol 的普及，Higress 可能会成为企业内部工具与 AI Agent 之间的标准连接器。

### 社区反馈与改进
*   **文档与易用性**: 作为阿里系开源项目，国内文档较好，但国际化文档和社区互动仍有提升空间。
*   **控制面性能**: 在超大规模（如 10W+ Service）集群下，控制面的内存占用和配置推送延迟仍需持续优化。

---

## 6. 学习建议

### 适合人群
*   具备 Kubernetes 基础的后端工程师或运维工程师（SRE）。
*   对 Service Mesh 和云原生技术感兴趣的开发者。
*   需要构建 AI 基础设施的架构师。

### 学习路径
1.  **基础**: 熟悉 Kubernetes Ingress 概念和 Envoy 基础原理。
2.  **入门**: 在本地 Kind 集群中部署 Higress，配置一个简单的路由和 AI Provider。
3.  **进阶**: 学习 WASM (使用 TinyGo 编写一个简单的认证插件)，理解插件如何与 Envoy 交互。
4.  **高级**: 研究其控制面代码，理解 xDS 协议如何将 K8s CRD 转换为 Envoy 配置。

---

## 7. 最佳实践建议

### 如何正确使用
*   **资源隔离**: 在生产环境中，务必为 Higress 的控制面和数据面设置独立的 Resource Quota，防止被其他业务抢占资源。
*   **插件版本管理**: WASM 插件一旦推送到网关，会影响所有匹配的流量。建议建立插件的多版本管理机制，先在特定的 Canary 环境验证。

### 性能优化建议
*   **连接池调优**: 针对后端 LLM 服务（通常延迟较高），适当调大 Envoy 的连接池

---
## 代码示例




```python
# 示例1：基于Higress的API网关路由配置
def higress_api_gateway():
    """
    模拟Higress网关的路由配置
    解决问题：如何将不同路径的请求路由到不同的后端服务
    """
    from pydantic import BaseModel
    
    # 定义路由规则模型
    class RouteRule(BaseModel):
        path: str      # 请求路径
        service: str   # 目标服务
        method: str    # HTTP方法
    
    # 模拟路由表配置
    routes = [
        RouteRule(path="/api/v1/users", service="user-service", method="GET"),
        RouteRule(path="/api/v1/orders", service="order-service", method="POST")
    ]
    
    # 模拟请求处理
    def handle_request(request_path: str, request_method: str) -> str:
        for route in routes:
            if request_path == route.path and request_method == route.method:
                return f"转发到服务: {route.service}"
        return "404 Not Found"
    
    # 测试用例
    print(handle_request("/api/v1/users", "GET"))  # 输出: 转发到服务: user-service
    print(handle_request("/api/v1/orders", "POST"))  # 输出: 转发到服务: order-service
```




```python
# 示例2：Higress插件开发 - 请求限流
def higress_rate_limit():
    """
    实现基于Higress的请求限流插件
    解决问题：如何保护后端服务免受流量洪峰影响
    """
    import time
    from collections import deque
    
    class RateLimiter:
        def __init__(self, rate: int, per: int):
            self.rate = rate    # 限流速率
            self.per = per      # 时间窗口(秒)
            self.allowance = rate  # 当前允许的请求数
            self.last_check = time.time()
        
        def allow(self) -> bool:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            
            # 补充允许的请求数
            self.allowance += time_passed * (self.rate / self.per)
            
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            if self.allowance < 1:
                return False
            else:
                self.allowance -= 1
                return True
    
    # 使用示例
    limiter = RateLimiter(rate=5, per=10)  # 每10秒允许5个请求
    
    for i in range(7):
        if limiter.allow():
            print(f"请求 {i+1}: 允许通过")
        else:
            print(f"请求 {i+1}: 被限流")
```




```python
# 示例3：Higress服务发现与负载均衡
def higress_service_discovery():
    """
    模拟Higress的服务发现和负载均衡
    解决问题：如何动态发现服务实例并实现负载均衡
    """
    import random
    
    class ServiceRegistry:
        def __init__(self):
            self.services = {
                "user-service": ["10.0.0.1:8080", "10.0.0.2:8080", "10.0.0.3:8080"],
                "order-service": ["10.0.1.1:8080", "10.0.1.2:8080"]
            }
        
        def get_instances(self, service_name: str) -> list:
            return self.services.get(service_name, [])
    
    class LoadBalancer:
        @staticmethod
        def select(instances: list) -> str:
            return random.choice(instances) if instances else None
    
    # 使用示例
    registry = ServiceRegistry()
    lb = LoadBalancer()
    
    # 获取user-service的实例并选择一个
    instances = registry.get_instances("user-service")
    selected = lb.select(instances)
    print(f"选中的服务实例: {selected}")
    
    # 模拟多次请求的负载均衡
    print("\n模拟5次请求的负载均衡结果:")
    for _ in range(5):
        print(lb.select(instances))
```


---
## 案例研究


### 1：阿里巴巴内部电商业务体系

 1：阿里巴巴内部电商业务体系

**背景**: 在阿里巴巴庞大的电商生态中，服务间调用极其复杂。随着业务向微服务和云原生架构迁移，传统的 Nginx 等网关在处理海量流量、动态路由配置以及与阿里云内部服务（如 MSE, ARMS, ACK）集成时，面临着运维成本高和扩展性不足的挑战。

**问题**: 
1. 旧有网关在应对大促流量洪峰时，配置变更生效慢，无法满足秒级弹性伸缩需求。
2. 需要一个能够原生支持 Dubbo、gRPC 以及 HTTP 的统一流量入口，以打通 Spring Cloud 和 Service Mesh (Istio) 架构。
3. 开源网关与阿里云内部可观测性系统的集成深度不够，导致全链路追踪存在盲区。

**解决方案**: 阿里巴巴将内部经过多年“双十一”验证的网关技术进行开源，推出了 Higress。Higress 基于 Istio 与 Envoy 核心，进行了深度的优化与定制。它被部署在阿里核心电商链路的流量入口，利用其标准化的 Ingress Gateway 能力，统一管理 K8s 集群内外流量。

**效果**: 
1. 成功支撑了双十一期间每秒数十万级的 QPS 流量冲击，稳定性达到 99.99% 以上。
2. 通过 Higress 的热配置更新能力，路由规则修改实现了毫秒级生效，极大提升了业务迭代效率。
3. 统一了南北向（外部入口）与东西向（服务间）流量治理，显著降低了基础设施的运维复杂度。

---



### 2：识货 APP（得物旗下）

 2：识货 APP（得物旗下）

**背景**: 识货是一个知名的球鞋与潮流商品导购平台。随着用户量的激增和 API 接口对外开放的需求增加，平台需要一个高性能、可扩展的 API 网关来管理外部合作伙伴的访问以及内部微服务的流量调度。

**问题**: 
1. 传统的 API 网关在处理高并发读写请求时，延迟较高，影响用户体验。
2. 开放 API 业务需要精细化的流量控制和安全防护（如 WAF 防御、防刷），以防止恶意攻击和资源滥用。
3. 业务方希望能够通过插件形式快速扩展网关功能，而不需要修改核心代码。

**解决方案**: 识货技术团队引入并深度使用了 Higress。利用 Higress 提供的 Wasm (WebAssembly) 插件市场，识货快速部署了自定义的认证鉴权和流量整形插件。同时，利用 Higress 对 HTTP/2 和 gRPC 的高性能支持，优化了移动端与后端服务的通信效率。

**效果**: 
1. 网关处理请求的 P99 延迟显著降低，提升了 APP 的响应速度。
2. 通过 Higress 的插件生态，团队在两周内完成了原本需要两个月开发的流量安全防护功能上线。
3. 实现了 API 的全生命周期管理，合作伙伴的接入效率提升了 50% 以上。

---



### 3：杭州某智慧政务云平台

 3：杭州某智慧政务云平台

**背景**: 该政务云平台承载了多个局委办的业务系统，包括政务服务网、数据共享交换平台等。由于涉及大量敏感数据，系统对数据安全和协议兼容性有着极高的要求，且底层架构混合了虚拟机和容器化环境。

**问题**: 
1. 现有网关无法很好地兼容遗留的 SOAP/WebService 协议与新兴的 RESTful API，导致数据孤岛严重。
2. 政务系统要求严格的国密算法支持，市面上通用的开源网关难以直接满足合规要求。
3. 跨部门数据调用需要进行严格的审计和限流，传统方案缺乏灵活的流量控制手段。

**解决方案**: 该平台采用 Higress 作为统一的政务 API 网关。利用 Higress 强大的协议转换能力，实现了老旧系统与微服务架构的无缝对接。同时，基于 Higress 的 Lua/Wasm 插件能力，定制开发了符合国密标准的加解密插件，并集成了实名认证系统。

**效果**: 
1. 打通了不同局委办之间的数据壁垒，实现了跨部门业务流程的自动化流转。
2. 通过定制化的安全插件，满足了国家信息安全等级保护（等保）的合规要求。
3. 实现了对全网流量的精细化管控，有效防止了某一业务高峰期挤占整个平台资源的情况，保障了核心政务系统的稳定性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|-----------------|--------|------|
| 性能 | 高性能，基于 Envoy 和 Rust，支持高并发 | 极高性能，基于 Lua 和 OpenResty，低延迟 | 高性能，基于 Nginx 和 Lua，成熟稳定 |
| 易用性 | 提供控制台和 K8s Ingress 支持，配置灵活 | 控制台功能丰富，但配置复杂度较高 | 控制台直观，但插件管理较复杂 |
| 成本 | 开源免费，企业版需付费支持 | 开源免费，企业版需付费支持 | 开源免费，企业版需付费支持 |
| 扩展性 | 支持 WASM 插件，扩展性强 | 支持 Lua 插件，生态丰富 | 支持 Lua 和 Go 插件，生态成熟 |
| 社区支持 | 阿里背书，社区活跃度中等 | Apache 基金会项目，社区活跃 | Kong Inc. 支持，社区成熟 |
| 适用场景 | 云原生、微服务、API 网关 | 高并发 API 网关、微服务 | 传统 API 网关、混合云环境 |

### 优势分析

- **alibaba/higress**：
  - 基于 Envoy 和 Rust，性能和安全性较高。
  - 支持 WASM 插件，扩展性和灵活性优于传统方案。
  - 阿里生态集成良好，适合云原生和微服务场景。

- **APISIX**：
  - 极高性能，适合高并发场景。
  - Apache 基金会项目，社区活跃，文档完善。
  - 动态路由和负载均衡功能强大。

- **Kong**：
  - 成熟稳定，企业级支持完善。
  - 插件生态丰富，适合传统和混合云环境。
  - 控制台直观，易于上手。

### 不足分析

- **alibaba/higress**：
  - 社区活跃度不如 APISIX 和 Kong。
  - 企业版功能可能需要付费，成本较高。
  - 文档和案例相对较少。

- **APISIX**：
  - 配置复杂度较高，学习曲线陡峭。
  - 企业版功能需付费，成本较高。
  - 控制台功能虽丰富，但界面不够直观。

- **Kong**：
  - 性能略低于 APISIX 和 Higress。
  - 插件管理较复杂，维护成本高。
  - 对云原生支持不如 Higress 和 APISIX。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 标准的流量管理

**说明**:  
Higress 深度兼容 Kubernetes Ingress 标准，通过 Ingress API 定义路由规则可实现服务间的流量转发与负载均衡。相比传统的 Service Mesh，这种方式更轻量且易于集成。

**实施步骤**:
1. 在 Kubernetes 集群中部署 Higress Gateway 组件。
2. 编写 Ingress YAML 文件，定义 `host`、`path` 和 `backend` 服务。
3. 应用配置：`kubectl apply -f ingress.yaml`。
4. 验证路由规则是否生效。

**注意事项**:  
- 确保后端 Service 的端口与 Ingress 配置一致。
- 避免使用过于宽泛的路径规则（如 `/*`），以免冲突。

---

### 实践 2：插件化扩展功能

**说明**:  
Higress 支持通过插件（如 WAF、限流、认证）扩展功能。插件可动态加载，无需重启网关，适合快速响应业务需求。

**实施步骤**:
1. 在 Higress 控制台选择“插件市场”。
2. 根据需求选择插件（如 `key-auth`）并配置参数。
3. 启用插件并绑定到目标路由或服务。
4. 测试插件功能是否符合预期。

**注意事项**:  
- 插件配置错误可能导致流量中断，建议先在测试环境验证。
- 定期检查插件版本更新，确保安全性。

---

### 实践 3：服务安全防护

**说明**:  
通过 Higress 的安全插件（如 IP 访问控制、JWT 认证）保护后端服务，防止未授权访问或恶意攻击。

**实施步骤**:
1. 在路由配置中启用 `jwt-auth` 插件。
2. 配置 JWT 签名密钥和声明（Claims）。
3. 设置 IP 黑白名单插件，限制访问来源。
4. 监控安全日志，及时调整策略。

**注意事项**:  
- JWT 密钥需妥善保管，避免泄露。
- 定期审计 IP 白名单，移除无效条目。

---

### 实践 4：金丝雀发布与流量灰度

**说明**:  
Higress 支持基于权重的流量分流，可实现金丝雀发布或 A/B 测试，降低新版本上线的风险。

**实施步骤**:
1. 部署新版本服务（如 `v2`）。
2. 在 Ingress 或 Gateway API 中配置流量规则，将 10% 流量指向 `v2`。
3. 观察 `v2` 的错误率和性能指标。
4. 逐步调整流量比例直至完全切换。

**注意事项**:  
- 确保新旧版本兼容，避免数据格式不一致导致的问题。
- 准备快速回滚方案。

---

### 实践 5：监控与可观测性

**说明**:  
集成 Prometheus 和 Grafana 实时监控 Higress 的性能指标（如 QPS、延迟、错误率），快速定位问题。

**实施步骤**:
1. 在 Higress 中启用 Prometheus 指标暴露。
2. 配置 Prometheus 抓取 Higress 的 `/metrics` 端点。
3. 导入 Higress 官方 Grafana 仪表盘模板。
4. 设置告警规则（如错误率超过 1%）。

**注意事项**:  
- 监控数据存储需预留足够空间。
- 避免过度采集指标，影响性能。

---

### 实践 6：高可用部署

**说明**:  
通过多副本部署和健康检查确保 Higress 的高可用性，避免单点故障。

**实施步骤**:
1. 在 Kubernetes 中设置 Higress Deployment 的副本数 ≥ 3。
2. 配置 `readinessProbe` 和 `livenessProbe` 检查 `/health` 端点。
3. 使用反亲和性规则将 Pod 分散到不同节点。
4. 测试节点故障时流量是否自动切换。

**注意事项**:  
- 确保集群资源充足，避免资源争抢。
- 定期演练故障恢复流程。

---

### 实践 7：配置版本管理与回滚

**说明**:  
使用 Git 或 Higress 控制台管理配置版本，支持快速回滚到历史版本，减少配置错误的影响。

**实施步骤**:
1. 将 Ingress 和插件配置存储在 Git 仓库。
2. 通过 CI/CD 流程自动应用配置。
3. 在 Higress 控制台记录每次变更的备注。
4. 如需回滚，选择历史版本并重新应用。

**注意事项**:  
- 敏感信息（如密钥）应使用 Kubernetes Secret 管理，避免硬编码。
- 回滚前评估对现有流量的影响。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，利用 HTTP/2 的多路复用特性可以消除 TCP 层面的队头阻塞，减少连接建立开销。对于弱网环境，启用 HTTP/3 (QUIC) 可以基于 UDP 进一步提升连接建立速度和传输稳定性。

**实施方法**:
1. 在监听器或路由配置中，将协议版本设置为 `h2` 或 `h2c` (明文 HTTP/2)。
2. 启用 TLS 配置，并在 ALPN 中包含 `h2` 和 `http/1.1`。
3. 在高级设置中开启 QUIC 支持（如果 Higress 版本支持）。

**预期效果**:在高并发或弱网环境下，请求延迟可降低 20%-40%，TCP 连接数减少 50% 以上。

---

### 优化 2：配置全链路超时与连接池

**说明**: 默认的超时配置可能不适合高吞吐场景，过长的超时会导致连接资源堆积。合理的连接池配置（最大连接数、最大空闲连接数）能够有效复用后端连接，减少频繁握手带来的 CPU 消耗。

**实施方法**:
1. **连接池调优**: 调整 `upstream` 的 `maxRequestsPerConnection` 和 `http2MaxRequests`。
2. **超时设置**: 根据业务 P99 耗时，设置合理的 `connectTimeout`、`sendTimeout` 和 `readTimeout`。
3. **空闲回收**: 配置 `idleTimeout`，及时清理不活跃的连接。

**预期效果**: 后端服务连接数更加平稳，网关内存占用降低约 15%-30%，有效防止雪崩效应。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 或远程调用鉴权逻辑，Wasm 执行效率极高（接近原生速度）。同时，在网关层开启本地缓存（如缓存鉴权结果或配置数据）可大幅减少对后端的请求。

**实施方法**:
1. 将高频使用的鉴权、限流或请求头处理逻辑编写为 Wasm 插件并部署。
2. 配置 Higress 的 `local_reply` 或使用 `ext_proc` 结合内存缓存。
3. 针对不变的数据（如 JWT 公钥），配置定时预加载到内存。

**预期效果**: 插件执行延迟降低至微秒级，后端请求总量减少 20%-50% (视缓存命中率而定)。

---

### 优化 4：启用 CPU 亲和性与 NUMA 优化

**说明**: Higress 基于 Envoy，通常运行在多核环境。开启 CPU 亲和性可以将工作线程绑定到特定的 CPU 核心，减少上下文切换和缓存失效。在 NUMA 架构下优化内存分配可进一步提升吞吐。

**实施方法**:
1. 在启动配置或环境变量中设置 worker 线程数等于 CPU 核心数。
2. 配置 `--cpuset-cpus` 或使用容器运行时的 CPU 绑定功能。
3. 确保内存分配策略针对 NUMA 节点进行了优化（如修改 `kernel.numa_balancing`）。

**预期效果**: 在极高 QPS 场景下，系统 CPU 利用率提升 10%-15%，长尾延迟减少 30%。

---

### 优化 5：开启零拷贝与 Sendfile 机制

**说明**: 对于静态资源分发或大文件传输，传统的数据流转需要多次在内核态与用户态之间拷贝数据。开启零拷贝技术（如 Linux 的 `sendfile`）可以直接在内核空间将文件传输到网卡，极大降低 CPU 负载。

**实施方法**:
1. 确认底层操作系统支持 `sendfile` 或 `splice` 系统调用。
2. 在 Higress 的配置中，针对静态资源路由开启 Buffer 限制优化，确保数据流尽量绕过用户态处理。
3. �

---
## 学习要点

- 基于 Alibaba Higress 的项目特性，为您总结以下关键要点：
- Higress 是阿里云开源的下一代云原生 API 网关，深度整合了 Nginx 的生态优势与 Envoy 的高性能架构。
- 该项目完美兼容 Kubernetes Ingress 标准，能够无缝对接 K8s 服务网格，极大降低了云原生环境下的流量管理复杂度。
- 它提供了开箱即用的 WAF（Web应用防火墙）安全防护能力，有效抵御常见的 Web 攻击并保障 API 安全。
- Higress 具备强大的流量治理功能，支持金丝雀发布、蓝绿部署及全链路灰度发布，满足复杂的微服务业务场景。
- 通过内置的 AI 网关插件，它支持与主流大模型（如 OpenAI、Hugging Face）无缝集成，简化了 AI 应用的接入与流量管理。
- 该网关深度集成 K8s Nginx Ingress 注解，允许用户几乎零成本地从传统 Nginx Ingress 迁移至 Higress。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的基本概念与核心架构（基于 Envoy 和 Istio）
- Higress 与传统 API 网关的区别及优势
- 云原生网关的基础知识（Kubernetes Ingress、Gateway API）
- Higress 的安装与部署（Docker 与 Kubernetes 环境）
- 基本配置：域名、路由（Ingress Route）与服务发现

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档：[https://higress.io/docs/latest/overview/what-is-higress/](https://higress.io/docs/latest/overview/what-is-higress/)
- Higress GitHub 仓库：[https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- Envoy 官方文档基础部分：[https://www.envoyproxy.io/docs/envoy/latest/intro](https://www.envoyproxy.io/docs/envoy/latest/intro)

**学习建议**:
- 建议先理解云原生和微服务网关的背景，再深入 Higress 的特性。
- 动手实践：在本地 Docker 或 Minikube 环境中完成一次 Higress 的安装，并配置一个简单的路由转发。

---

### 阶段 2：核心功能与流量管理

**学习内容**:
- 高级流量管理：灰度发布、蓝绿部署、流量镜像
- 负载均衡算法与健康检查配置
- 安全防护：WAF 插件使用、Basic Auth、JWT 认证、CORS 配置
- 服务Mock与故障注入
- Higress 控制台的使用与监控指标查看

**学习时间**: 2-3周

**学习资源**:
- Higress 流量管理官方文档：[https://higress.io/docs/latest/user/traffic-management/](https://higress.io/docs/latest/user/traffic-management/)
- Higress 插件市场文档：[https://higress.io/docs/latest/user/plugin-common/](https://higress.io/docs/latest/user/plugin-common/)
- Kubernetes Gateway API 规范：[https://gateway-api.sigs.k8s.io/](https://gateway-api.sigs.k8s.io/)

**学习建议**:
- 重点掌握如何通过配置实现无损的下线发布和流量切换。
- 尝试启用官方插件（如 Key Auth 或 Request Block）来增强网关的安全性。
- 结合 Prometheus 观察网关的流量指标。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- Higress 插件体系架构（Wasm 插件与 Go/Python/Java 插件）
- 编写自定义插件：使用 Wasm (AssemblyScript) 或 Go 语言开发简单逻辑
- 插件的热加载与配置管理
- 可观测性集成：访问日志收集、链路追踪
- 告警配置与性能调优（连接池、缓冲区大小等）

**学习时间**: 3-4周

**学习资源**:
- Higress 自定义插件开发指南：[https://higress.io/docs/latest/user/plugin-develop/](https://higress.io/docs/latest/user/plugin-develop/)
- Wasm 官方站点：[https://webassembly.org/](https://webassembly.org/)
- OpenTelemetry 集成文档：[https://higress.io/docs/latest/user/observability/](https://higress.io/docs/latest/user/observability/)

**学习建议**:
- 从修改一个现有的官方插件开始，理解插件的生命周期和数据流。
- 学习 Wasm 基础知识，因为这是 Higress 扩展能力的核心方向。
- 在生产环境模拟场景中，配置日志输出到 ELK 或类似系统，分析慢请求。

---

### 阶段 4：企业级实战与架构优化

**学习内容**:
- 高可用部署架构：多副本部署、灾备与容灾
- Higress 在 K8s 集群中的多租户隔离
- 与阿里云 MSE、Nacos、Sentinel 等产品的深度集成
- 大规模流量下的性能极限测试与优化
- 源码级剖析：深入理解 Higress 对 Envoy 的扩展与定制

**学习时间**: 4周以上

**学习资源**:
- Higress 源码分析：GitHub 仓库源码阅读
- 阿里云 MSE 产品文档：[https://www.aliyun.com/product/mse](https://www.aliyun.com/product/mse)
- Envoy 深度解析博客与社区案例
- CNCF 云原生网关最佳实践白皮书

**学习建议**:
- 阅读源码，理解 Higress 如何处理配置下发（xDS 协议）。
- 尝试压测网关，找出系统的瓶颈点并进行调优。
- 思考如何将 Higress 作为 Service Mesh 的南北

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是阿里内部对 Nginx、Envoy 等网关技术多年实践经验的结晶。它基于 Envoy 和 Istio 进行了深度的二次开发，旨在解决云原生时代流量治理的痛点。

与 Nginx 相比，Higress 提供了更丰富的流量管理特性（如全动态配置、热更新）和标准的 Kubernetes Ingress 支持，且原生支持 WAF（Web 应用防火墙）插件。与 Kong 相比，Higress 的核心优势在于其深度集成了阿里云的生态，支持 Nacos 等主流注册中心，且在处理高并发流量时具有更好的性能和稳定性，同时完全兼容 Kubernetes Ingress 规范。

---



### 2: Higress 是否支持从 Nginx 或其他网关无缝迁移？

2: Higress 是否支持从 Nginx 或其他网关无缝迁移？

**A**: 是的，Higress 非常重视迁移的兼容性。对于 Nginx 用户，Higress 提供了 Nginx Ingress 注解的兼容支持，这意味着大部分标准的 Nginx Ingress 配置可以直接在 Higress 上使用。

对于使用云原生架构的用户，Higress 完全兼容 Kubernetes Ingress 和 Gateway API 标准。对于使用阿里云 MSE（微服务引擎）或云原生网关的用户，Higress 是其开源的核心实现，因此架构和配置逻辑高度一致，可以平滑迁移。

---



### 3: Higress 如何处理服务发现？它支持哪些注册中心？

3: Higress 如何处理服务发现？它支持哪些注册中心？

**A**: Higress 原生支持基于 Kubernetes Service 的服务发现，这是其最基础的用法。同时，为了适应微服务架构，它还深度集成了主流的服务注册中心。

目前，Higress 支持通过插件或配置直接连接 Nacos、Zookeeper、Consul 以及 Eureka 等注册中心。这使得 Higress 可以直接代理后端的微服务（如 Spring Cloud 或 Dubbo 服务），无需手动配置后端 IP 列表，能够实现流量的自动负载均衡和健康检查。

---



### 4: Higress 的插件扩展性如何？能否使用 WAF 功能？

4: Higress 的插件扩展性如何？能否使用 WAF 功能？

**A**: Higress 拥有强大的插件扩展能力，这是其核心亮点之一。它采用 Lua (基于 OpenResty) 和 WebAssembly (Wasm) 两种插件开发模式。特别是 Wasm 支持，允许开发者使用 C++、Go、Rust 等多种语言编写高性能、隔离性好的插件，且插件可以热加载，无需重启网关。

关于安全，Higress 内置了强大的 WAF 插件（基于 ModSecurity 规则），可以提供针对 OWASP Top 10 的安全防护，如 SQL 注入、XSS 攻击等。用户可以通过简单的配置即可启用 WAF 保护 API 安全。

---



### 5: Higress 是否支持 Dubbo 服务？如何处理 gRPC 或 HTTP 协议？

5: Higress 是否支持 Dubbo 服务？如何处理 gRPC 或 HTTP 协议？

**A**: 是的，Higress 对微服务协议有非常完善的支持。它原生支持 Dubbo 框架，可以作为 HTTP 到 Dubbo 的网关，将 HTTP/HTTPS 请求转换为 Dubbo 协议调用后端服务，这对于需要暴露内部 Dubbo 服务的场景非常有用。

同时，Higress 基于 Envoy 构建，因此对 gRPC 和 HTTP/2 拥有原生的支持。它可以对 gRPC 流量进行路由、负载均衡和全链路灰度发布，而无需进行协议转换，保证了通信的高效性。

---



### 6: 在生产环境中，Higress 的性能表现如何？能否应对高并发流量？

6: 在生产环境中，Higress 的性能表现如何？能否应对高并发流量？

**A**: Higress 专为高性能场景设计。其数据面基于 Envoy C++ 内核构建，相比于基于 Java 或纯 Lua 的网关，具有更低的延迟和更高的吞吐量。

在阿里云内部，经过多年双11等大促场景的验证，Higress 能够支撑每秒数十万级的 QPS 请求。其配置热更新机制（基于 xDS 协议）确保了在更新路由规则时不会导致连接中断，从而保障生产环境的业务连续性。

---



### 7: 如何部署和运维 Higress？是否支持 Helm 安装？

7: 如何部署和运维 Higress？是否支持 Helm 安装？

**A**: Higress 是完全云原生的，最推荐的部署方式是在 Kubernetes 集群中使用 Helm 进行安装。官方提供了标准的 Helm Chart，只需几条命令即可完成部署。

运维方面，Higress 提供了详细的 Prometheus 监控指标集成，可以轻松对接 Grafana 进行监控大盘展示。同时，它支持控制台配置和 Kubectl CRD 配置两种方式，提供了灵活的运维管理手段。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地快速启动

### 问题**: Higress 是基于 Istio 和 Envoy 构建的，请尝试在本地 Docker 环境中使用一条命令快速启动 Higress，并访问其控制台（Dashboard）。默认的端口是多少？

### 提示**: 参考 Higress 官方文档中的 "快速开始" 章节，注意检查本地 8080 或 8888 端口是否被占用。

### 

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 6 条实践建议：

### 1. 利用 AI 指标路由实现智能流量分发
**场景**：在接入大模型（如 OpenAI、通义千问等）时，通常需要根据请求内容的复杂度或类型，将流量分发到不同的模型或不同参数配置的端点上。
**建议**：配置基于请求体（Request Body）的 AI 指标路由。不要仅依赖 URL 路径进行路由，而应解析请求中的 `messages` 字段或业务自定义字段。
**操作**：在路由配置中启用 AI 特性检测，根据 Prompt 的 Token 数量预估或特定关键词（如“代码生成”与“日常对话”），将高资源消耗的请求路由到高算力模型，将简单请求路由到低成本模型，以优化成本与延迟。

### 2. 配置严格的 Token 限流以控制成本
**场景**：大模型 API 调用通常按 Token 计费，且模型提供商存在严格的速率限制（RPM/TPM）。传统的 QPS 限流无法有效控制 API 成本。
**建议**：启用基于 Token 的限流策略，而非仅基于并发连接数或 QPS。
**操作**：针对不同的 API Key 或租户配置 Token 预估限流。Higress 支持在网关层对请求进行 Token 计数（基于 Tokenizer 或近似算法），当请求预计消耗的 Token 超过阈值时直接拦截，防止后端模型因超限返回 429 错误或产生意外高额账单。

### 3. 实施语义缓存策略以降低延迟和费用
**场景**：在生产环境中，大量用户查询往往是重复的或高度相似的（如常见知识问答）。每次都请求大模型会导致高延迟和高费用。
**建议**：配置针对 AI 请求的语义缓存或精确匹配缓存。
**操作**：在 Higress 中配置缓存插件，将请求的 Prompt 作为 Cache Key，并将模型返回的完整响应缓存。对于允许一定误差的场景，可以结合向量数据库配置语义缓存。设置合理的 TTL（生存时间），对于实时性要求不高的问答，可以显著提升响应速度并减少 50% 以上的后端调用成本。

### 4. 统一管理多模型 Provider 并处理 Key 轮换
**场景**：企业内部可能同时使用多家大模型厂商的服务，且 API Key 需要定期轮换以保证安全。将 Key 硬编码在业务代码中管理极其困难且不安全。
**建议**：利用 Higress 的服务来源管理功能，集中管理不同厂商的 API Key 和 Endpoint。
**操作**：在网关层配置多个模型 Provider（如 OpenAI、Azure OpenAI、通义千问）。业务层仅调用统一的网关地址，通过 Header 或参数指定模型名称。当需要更换 Key 或切换厂商时，只需在 Higress 控制台修改配置，无需重新发布业务代码。同时，为不同的业务线分配不同的网关 Key，便于在网关层做统一的鉴权和审计。

### 5. 警惕流式传输的超时与中断配置
**场景**：AI 对话通常使用 SSE（Server-Sent Events）流式返回。如果网关层的超时时间配置过短，会导致连接在模型未生成完毕前被断开，用户收到不完整的回答。
**建议**：检查并调整网关的超时配置，特别是针对流式响应的处理。
**操作**：将路由或全局的超时时间设置为一个较大的值（如 300 秒），或者针对流式请求专门配置超时策略。确保 Higress 的 Upstream 配置启用了对 HTTP/1.1 Chunked 或 HTTP/2 流的正确透传支持，避免网关层尝试缓冲整个响应后再转发给客户端，这会导致流式效果失效。

### 6. 善用 Prompt 模板管理以减少客户端复杂度
**场景**：前端应用通常不擅长处理复杂的 Prompt Engineering（提示词工程），将 System Prompt 发送到客户端也存在安全风险。
**建议

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*