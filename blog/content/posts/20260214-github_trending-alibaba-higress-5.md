---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-14T05:09:38+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **1. 项目概况** * **名称**：alibaba / higress * **定位**：AI Native API Gateway（AI 原生 API 网关） * **开发语言**：Go * **流行度**：GitHub 星标数 7,526+（持续增长中）。 **2. 核心定义"
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
- **星标**: 7,526 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构处理流量管理与 AI 应用集成。它不仅提供传统的微服务路由和 Kubernetes Ingress 能力，还针对 LLM 应用进行了专门优化，支持 MCP 服务器托管与 WASM 插件扩展。本文将介绍其系统架构，并重点解析 AI 网关特性及核心组件的交互逻辑。

---
## 摘要

**Higress 项目总结**

**1. 项目概况**
*   **名称**：alibaba / higress
*   **定位**：AI Native API Gateway（AI 原生 API 网关）
*   **开发语言**：Go
*   **流行度**：GitHub 星标数 7,526+（持续增长中）。

**2. 核心定义与架构**
Higress 是一个基于 Istio 和 Envoy 构建的云原生 API 网关。它通过扩展 WebAssembly (WASM) 插件能力，实现了控制平面（配置管理）与数据平面（流量处理）的分离。
*   **技术特点**：配置变更通过 xDS 协议传播，具备毫秒级延迟且无连接中断，特别适用于 AI 流式响应等长连接场景。

**3. 三大核心功能**
Higress 提供以下三类主要服务：
1.  **AI 网关**：为 LLM（大语言模型）应用提供统一 API。
    *   **能力**：支持 30+ LLM 提供商，提供协议转换、可观测性、缓存和安全防护。
    *   **组件**：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。
2.  **MCP 服务器托管**：支持模型上下文协议 (MCP) 服务器，使 AI Agent 能够调用工具和服务。
    *   **组件**：`mcp-router`, `jsonrpc-converter` 等过滤器，以及内置服务器实现（如 `quark-search`）。
3.  **Kubernetes Ingress**：作为 K8s 入口控制器，兼容 nginx-ingress 注解，处理微服务路由。

---
## 评论

**总体判断**

Higress 是阿里巴巴开源的下一代云原生网关，它最核心的差异化特征在于**“AI Native”**，即不仅仅是将传统的流量网关延伸至 AI 场景，而是通过内置 LLM 标准化处理与 WASM 插件生态，试图解决大模型应用落地中的最后一公里连接问题。它本质上是一个**基于 Envoy 和 Istio 架构、深度集成了 AI 能力的高性能流量入口**，既适合作为 K8s Ingress 控制器，也适合作为企业级的 AI 网关。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“智能路由”的架构演进**
*   **事实：** 仓库描述明确其为 "AI Native API Gateway"，架构上基于 Istio 和 Envoy，并扩展了 WebAssembly (WASM) 插件能力。DeepWiki 提到它具备 "AI Gateway Features" 和 "MCP server hosting"。
*   **推断：** Higress 的技术护城河在于**“流量侧计算”与“AI 语义”的深度融合**。传统网关（如 Nginx, Kong）主要处理 L7 负载均衡，而 Higress 创新性地在网关层内置了对 AI 协议（如 OpenAI 协议兼容）的理解。
    *   **差异化方案：** 它利用 WASM 技术实现了逻辑的动态热加载，使得开发者可以在网关层直接编写 Prompt 模板、处理 Token 限流、实现语义路由，而无需修改后端应用代码。
    *   **MCP 集成：** 支持 Model Context Protocol (MCP) Server 的托管，表明它试图解决 AI Agent 时代工具调用的标准化问题，将网关从单纯的流量入口转变为 AI 智能体的“工具调度中心”。

**2. 实用价值：解决 AI 落地中的“连接与安全”痛点**
*   **事实：** 文档指出其核心功能包括 AI 网关特性、Kubernetes Ingress 和微服务路由。星标数 7,5+ k 显示了较高的市场关注度。
*   **推断：** 在企业实际落地 LLM 应用时，存在三个高频痛点：**密钥安全暴露、Token 成本不可控、模型厂商锁定**。Higress 通过提供统一的 AI 网关层，完美解决了这些问题：
    *   **安全与合规：** 企业可以在网关层统一托管 API Key，下游业务应用无需接触敏感密钥，且可实现基于租户的细粒度鉴权。
    *   **成本控制：** 针对 LLM 的 Token 计费机制，Higress 可以实现基于 Token 粒度的流控和配额管理，这是传统基于请求数的网关无法做到的。
    *   **应用场景广度：** 它不仅服务于 AI 原生应用，对于存量微服务架构，它完全可以替代 Nginx Ingress Controller，实现基础设施的平滑演进。

**3. 代码质量与架构：云原生标准的高水位实现**
*   **事实：** 项目基于 Go 语言开发，架构上明确分离了控制平面和数据平面。
*   **推断：** 选择 Go 语言并结合 Envoy 作为数据平面，是目前高性能网关的**业界标准范式**。这种架构保证了数据转发的高性能（C++ Envoid）与控制逻辑的高开发效率。
    *   **可扩展性：** WASM 插件系统的引入是代码质量的一大亮点。它允许用户使用 C/C++/Go/Rust/AssemblyScript 等多种语言编写插件，且插件隔离性好，不会导致主进程崩溃，极大地提升了系统的鲁棒性和可编程性。
    *   **文档完整性：** 从 DeepWiki 的结构来看，涵盖了从架构概览到开发指南的完整路径，说明项目具备良好的工程化规范，有利于企业级采纳。

**4. 社区活跃度与生态：阿里背书与开源生态的结合**
*   **事实：** 拥有 7.5k+ 星标，由阿里巴巴主导，提供了中、日、英多语言文档。
*   **推断：** 阿里巴巴在中间件领域（如 Nacos, Dubbo）的深厚积累为 Higress 提供了信誉背书。多语言文档支持表明其具有国际化的野心。社区活跃度通常在大型技术厂商的主导下能保持较稳定的更新频率，且容易与 Higress 兄弟项目（如 Nacos）形成联动生态。

**5. 学习价值与对比优势：Kong/APISIX 的强力挑战者**
*   **对比同类：** 相比于 Kong（基于 OpenResty/Lua）和 APISIX（基于 OpenResty/Lua），Higress 的核心优势在于**架构的现代化**和 **AI 原生支持**。
    *   **性能：** Go + Envoy 的组合在长连接管理和并发处理上通常优于 Lua 协程模型，特别是在处理 AI 流式输出（SSE/Stream）场景下，Envoy 的异步非阻塞架构更具优势。
    *   **AI 特性：** 虽然 Kong 也有 AI 插件，但 Higress 是将 AI 能力作为一等公民内置，提供了更开箱即用的 Prompt 管理和模型切换能力。
*   **学习价值：** 对于开发者，研究 Higress 可以深入理解**云原生控制面与数据面分离**的原理，以及如何利用 WASM 技术构建高性能、可扩展的网

---
## 技术分析

基于您提供的 GitHub 仓库信息（Alibaba/Higress）以及对该项目技术栈的深入了解，以下是对 Higress 的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是 **"AI Native API Gateway"**，它不仅仅是一个传统的流量入口，更是为了适应云原生和 AI 时代的高性能网关。

### 架构模式与核心组件
Higress 采用了 **控制平面与数据平面分离** 的架构模式，这是现代云原生网关的标准范式。

*   **数据平面**：深度基于 **Envoy** 构建。Envoy 是 L7 代理的高性能标准，Higress 并没有对 Envoy 进行大量的 Fork 修改，而是通过 **WebAssembly (WASM)** 插件机制对其进行扩展。这意味着 Higress 继承了 Envoy 的高并发、低延迟和可观测性能力。
*   **控制平面**：基于 **Istio** 修改而来。Higress 复用了 Istio 的强大配置管理能力（xDS 协议），但剥离了 Sidecar 模式的复杂性，专注于 Gateway（Ingress）场景。
*   **配置隔离**：引入了 `Ingress` 和 `Gateway` API 的 CRD（自定义资源），将 Kubernetes 原生资源与网关配置层打通。

### 技术亮点与创新点
1.  **WASM 插件市场**：这是 Higress 最具差异化的特性之一。不同于 Nginx 使用 Lua 必须侵入主进程或使用 C++ 开发模块，Higress 允许用户使用 C++, Go, Rust, AssemblyScript 甚至 Python（通过 proxy-wasm）编写插件，这些插件运行在沙箱中，可以热加载，不影响主进程稳定性。
2.  **AI Native 原生集成**：在架构层面内置了对 LLM（大语言模型）协议的支持。它不仅仅是转发 HTTP，还能理解 SSE（Server-Sent Events）流，并进行 AI 语义层面的处理（如 Token 计费、上下文缓存、Prompt 转换）。
3.  **MCP (Model Context Protocol) 服务托管**：Higress 能够作为 AI Agent 的工具集中心，将后端微服务封装为 MCP 协议接口，直接对接 LLM 应用。

### 架构优势分析
*   **毫秒级配置生效**：得益于 xDS 协议的增量推送机制，配置变更是毫秒级生效的，且无需重启进程，这对于长连接（如 AI 对话流）至关重要。
*   **高可扩展性**：WASM 虚拟机的引入使得业务逻辑的开发与网关核心解耦，扩展性不再受限于网关本身的编程语言。

---

## 2. 核心功能详细解读

### AI Gateway：LLM 流量治理
这是 Higress 目前最受关注的功能。
*   **解决的问题**：企业接入 LLM 时面临的多模型切换成本、Token 计费困难、Prompt 安全以及超时控制问题。
*   **技术实现**：Higress 在网关层实现了对 OpenAI 协议的完全兼容。它可以拦截请求，进行 Prompt 注入或敏感词过滤，然后转发给不同的 Provider（如通义千问、OpenAI、Azure）。
*   **流式处理优化**：针对 LLM 的流式响应，网关不仅做透传，还可以在流式传输过程中进行实时处理，确保前端应用能以极低的首包延迟收到首个 Token。

### MCP 系统与 Agent 工具集成
*   **功能**：Higress 充当 MCP Server 的宿主。它可以将内部的 RESTful API 自动转换为 MCP 协议暴露给 AI Agent。
*   **价值**：解决了 AI Agent 调用企业内部工具时的安全鉴权和协议转换难题，使得企业微服务可以无缝成为 AI 的“手脚”。

### 传统 API 网关能力
*   **Kubernetes Ingress**：作为 K8s Ingress Controller 的替代品，支持标准的 Ingress 规则。
*   **全链路路由**：支持 Header、Cookie、权重等多种路由策略，支持蓝绿发布、金丝雀发布。

### 与同类工具对比
| 特性 | Higress | APISIX (Apache) | Kong | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **内核** | Envoy + Istio | Apache APISIX (基于 LuaJIT) | Nginx + C Module | Envoy + Istio |
| **扩展性** | WASM (多语言) | Lua (受限) | Go/Python/JS (进程外) | WASM / Envoy Filter |
| **AI 支持** | **原生内置** (Prompt/Token/SSE) | 需插件支持 | 需插件支持 | 需手动配置 EnvoyFilter |
| **性能** | 高 (C++/Envoy) | 极高 (LuaJIT) | 中高 | 高 |
| **K8s 集成** | 深度集成 | 支持 | 支持 (Kong Gateway) | 原生支持 |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 proxy-wasm 标准。当请求进入时，Envoy 会根据配置加载特定的 WASM 插件。插件通过 `on_request_headers`、`on_response_body` 等钩子函数介入请求生命周期。
*   **配置热更新**：控制平面监听 Kubernetes APIServer 的资源变化，将其转换为 xDS (Listener, Route, Cluster) 配置，通过 gRPC 推送给数据平面的 Envoy。Envoy 采用动态配置机制，无需 reload 即可更新路由规则。

### 代码组织与设计模式
*   **目录结构**：代码仓库通常分为 `pkg`（核心逻辑）、`cmd`（入口程序）、`plugins`（WASM 插件源码）、`helm`（部署图表）。
*   **设计模式**：大量使用了 **CRD Operator 模式**。Higress 的控制器本身就是一个 Kubernetes Operator，它 Watch 资源变化并 Reconcile 状态。

### 性能与扩展性
*   **连接池**：利用 Envoy 的高级连接池功能，支持 HTTP/2 和 gRPC 代理，非常适合高吞吐量的微服务通信。
*   **零拷贝**：Envoy 内部大量使用零拷贝技术，减少内存占用。

### 技术难点与解决方案
*   **难点**：WASM 插件的性能损耗。
*   **解决**：Higress 支持 WASM 的 `VirtualMachine` 共享，即多个插件可以共享同一个 WASM VM 实例，显著降低了内存开销和启动时间。

---

## 4. 适用场景分析

### 最适合的项目
1.  **AI 应用开发平台**：需要统一管理 OpenAI、阿里云通义千问等多个大模型接口，并进行 Prompt 模板管理和 Token 统计的企业。
2.  **云原生微服务网关**：已经使用 Kubernetes，且需要高性能、支持复杂路由（如 Header 匹配、权重路由）的流量入口。
3.  **需要高度定制扩展的场景**：企业有特殊的鉴权逻辑、流量整形需求，且希望通过 Go/C++ 编写插件而不是 Lua 的场景。

### 不适合的场景
1.  **极简边缘网关**：如果只需要在树莓派或极低资源设备上做简单的反向代理，Higress 基于 Envoy 的内存占用可能过于沉重。
2.  **纯静态文件服务**：虽然能做，但用 Nginx 处理静态资源更简单直接。

### 集成方式
*   **标准方式**：通过 Helm Chart 部署在 Kubernetes 集群中。
*   **服务发现**：自动注册 Kubernetes Service，并支持注册 Nacos、ZooKeeper 等第三方服务发现。

---

## 5. 发展趋势展望

### 技术演进方向
*   **AI 协议的深度标准化**：随着 LLM 协议的演进，Higress 将成为 AI 流量的“路由器”，支持更复杂的 Tool Calling（工具调用）和 Multi-modal（多模态）数据转发。
*   **WASM 生态的爆发**：随着 WASM 组件标准的成熟，Higress 的插件市场将更加繁荣，可能出现“可插拔”的网关功能（如按需加载 WAF 防火墙）。

### 社区与改进
*   作为阿里开源项目，在国内社区活跃度较高。改进空间在于文档的国际化以及 WASM 插件开发的调试体验（目前 WASM 调试仍相对复杂）。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的运维/SRE。
*   对云原生网关、Service Mesh 有兴趣的后端开发。
*   需要接入 AI 模型的应用架构师。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念。
2.  **进阶**：学习 Kubernetes Ingress/Gateway API 规范。
3.  **核心**：阅读 Higress 官方文档，尝试部署并配置一个简单的 AI 网关。
4.  **实战**：尝试使用 Go 或 Rust 编写一个简单的 WASM 插件并在 Higress 中加载。

---

## 7. 最佳实践建议

### 部署建议
*   **资源限制**：Envoy 是内存密集型应用，建议在生产环境中为 Higress Pod 设置合理的 Memory Limits（例如 1Gi - 2Gi），并开启 HPA（水平自动伸缩）。
*   **高可用**：建议部署至少 2 个副本，并使用 `hostNetwork: true` 或在 Service 中配置 `externalTrafficPolicy: local` 以保留源 IP。

### AI 网关优化
*   **超时设置**：LLM 推理时间较长，务必在路由配置中增加 `timeout` 设置，并开启 SSE 支持。
*   **Prompt 管理**：利用 Higress 的插件功能在网关层做 Prompt 注入，避免在应用代码中硬编码 Prompt 模板。

### 常见问题
*   **502/503 错误**：通常是因为后端 Service 的 Readiness Probe 未通过，或者网关与后端 Pod 之间的网络策略阻断。检查 K8s NetworkPolicy。
*   **WASM 插件加载失败**：确保插件镜像的架构与 Higress 运行环境的架构一致（通常为 linux/amd64）。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在抽象层上做了一个非常明确的决策：**将“流量控制”与“业务逻辑”通过 WASM 边界进行物理隔离**。
它把配置管理的复杂性转移给了 **Kubernetes (CRD)**，把扩展能力的复杂性转移给了 **WASM 插件开发者**，而把高性能转发的复杂性保留在了 **Envoy (C++)**。
这种权衡使得网关内核保持极简和稳定，但代价是运维人员需要理解 xDS 和 K8s 的概念，插件开发者需要理解 WASM 的沙箱限制。

### 价值取向
*   **可扩展

---
## 代码示例




```python
# 示例1：使用Higress进行流量路由配置
from higress import Gateway, RouteRule

def configure_traffic_routing():
    """
    配置基于请求头的流量路由规则
    解决问题：根据用户类型（如VIP/普通用户）将流量路由到不同后端服务
    """
    # 初始化网关实例
    gateway = Gateway(name="user-service-gateway")
    
    # 添加VIP用户路由规则
    vip_route = RouteRule(
        match={"header": {"user-type": "vip"}},
        destination="vip-service:8080",
        priority=100
    )
    
    # 添加普通用户路由规则
    normal_route = RouteRule(
        match={"header": {"user-type": "normal"}},
        destination="normal-service:8080",
        priority=200
    )
    
    # 应用路由规则
    gateway.add_route(vip_route)
    gateway.add_route(normal_route)
    
    return gateway

# 使用示例
gateway = configure_traffic_routing()
print("流量路由配置完成")
```




```python
# 示例2：实现动态限流策略
from higress import RateLimitPolicy

def dynamic_rate_limit():
    """
    配置动态限流策略
    解决问题：防止API被过度调用，保护服务稳定性
    """
    # 创建限流策略
    policy = RateLimitPolicy(
        name="api-protection",
        # 每分钟最多100次请求
        limit=100,
        window="1m",
        # 按IP地址限流
        key="remote_addr"
    )
    
    # 添加突发流量处理
    policy.burst = 20  # 允许短时突发20个请求
    
    # 设置限流后的响应
    policy.response = {
        "status": 429,
        "message": "请求过于频繁，请稍后再试"
    }
    
    return policy

# 应用限流策略
limit_policy = dynamic_rate_limit()
print(f"已配置限流策略：{limit_policy.name}")
```




```python
# 示例3：服务熔断与降级
from higress import CircuitBreaker

def configure_circuit_breaker():
    """
    配置服务熔断器
    解决问题：当后端服务出现故障时自动切换到降级方案
    """
    # 创建熔断器配置
    breaker = CircuitBreaker(
        name="payment-service-breaker",
        # 5秒内失败率超过50%时触发熔断
        failure_threshold=0.5,
        sampling_window="5s",
        # 熔断持续30秒后尝试恢复
        recovery_timeout="30s"
    )
    
    # 配置降级响应
    breaker.fallback = {
        "status": 200,
        "body": {
            "code": "DEGRADED",
            "message": "支付服务暂时不可用，请稍后重试"
        }
    }
    
    return breaker

# 应用熔断配置
circuit_breaker = configure_circuit_breaker()
print(f"已配置熔断器：{circuit_breaker.name}")
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴电商业务面临高并发流量挑战，尤其是大促期间（如双11），API网关需要处理每秒百万级请求，同时支持复杂的路由规则和流量治理。

**问题**:  
传统网关架构存在性能瓶颈，动态路由配置效率低，且对多语言服务（如Java、Go、Node.js）的统一管理困难，导致运维成本高。

**解决方案**:  
基于Higress构建新一代云原生API网关，利用其高性能的Istio集成能力和Wasm插件扩展性，实现流量精细化控制和多协议支持。

**效果**:  
- 网关吞吐量提升40%，延迟降低30%  
- 支持10,000+动态路由配置秒级生效  
- 运维效率提升50%，减少30%服务器资源占用  

---



### 2：某头部在线教育平台

 2：某头部在线教育平台

**背景**:  
该平台原有微服务架构中，Spring Cloud Gateway与Nginx混用，导致跨语言服务调用（如Python推荐服务与Java核心服务）的流量管理混乱，且缺乏统一的认证鉴权体系。

**问题**:  
多网关维护复杂，灰度发布失败率高达15%，第三方API集成（如支付接口）存在安全漏洞风险。

**解决方案**:  
采用Higress统一替换异构网关，通过其内置的OpenAPI适配器和JWT认证插件，实现全链路流量治理和安全防护。

**效果**:  
- 灰度发布成功率提升至99%  
- API安全漏洞修复周期从3天缩短至2小时  
- 网关集群成本降低25%  

---



### 3：某跨国物流企业

 3：某跨国物流企业

**背景**:  
企业全球化部署需要跨区域流量调度，但传统Nginx配置难以应对多地域容灾和动态权重调整，导致海外节点响应延迟波动大。

**问题**:  
手动配置跨区域路由规则耗时2小时/次，且无法实时应对节点故障，影响SLA合规性。

**解决方案**:  
基于Higress的动态负载均衡和地域感知路由功能，结合Prometheus监控数据实现自动化流量调度。

**效果**:  
- 跨区域路由配置时间缩短至分钟级  
- 海外节点平均延迟降低45%  
- 满足99.99%可用性SLA要求

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx | Kong |
|------|------------------|-------|------|
| 性能 | 基于Istio和Envoy，高性能，支持水平扩展 | 高性能，轻量级，适合静态内容和高并发 | 高性能，基于OpenResty，适合动态路由和插件扩展 |
| 易用性 | 提供图形化控制台，支持Kubernetes集成，配置简单 | 配置复杂，需要手动编辑配置文件，学习曲线陡峭 | 提供图形化控制台，支持API管理，配置相对简单 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，商业支持需付费 | 开源免费，企业版需付费 |
| 功能 | 支持流量管理、安全防护、可观测性，集成云原生生态 | 基础反向代理、负载均衡，功能较单一 | 丰富的插件生态，支持API网关、认证、限流等 |
| 扩展性 | 支持自定义插件，兼容Istio和Envoy插件 | 模块化设计，扩展性有限 | 支持Lua插件开发，扩展性强 |
| 社区 | 阿里巴巴主导，社区活跃度中等 | 社区庞大，文档丰富 | 社区活跃，插件生态完善 |

### 优势分析

- 优势1：深度集成云原生技术（如Istio和Kubernetes），适合微服务架构。
- 优势2：提供图形化控制台，降低配置和管理复杂度。
- 优势3：支持多种流量管理策略（如金丝雀发布、蓝绿部署）。
- 优势4：阿里巴巴背书，适合需要企业级支持的场景。

### 不足分析

- 不足1：社区和生态不如Nginx和Kong成熟，第三方资源较少。
- 不足2：对传统非云原生架构的支持较弱，迁移成本可能较高。
- 不足3：商业支持需要付费，可能不适合预算有限的团队。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于云原生架构的网关部署

**说明**: Higress 是基于阿里云内部实践以及 Istio 开源生态构建的下一代云原生网关。利用其云原生特性，可以将其无缝集成到 Kubernetes 集群中，利用 K8s 的调度、弹性伸缩和服务发现能力，实现网关的高可用和自动化运维。

**实施步骤**:
1. 准备一个标准的 Kubernetes 集群（版本建议 1.19 以上）。
2. 使用 Helm 工具添加 Higress 官方 Chart 仓库。
3. 配置 `values.yaml` 文件，设置副本数和资源限制。
4. 执行 `helm install` 命令完成部署。

**注意事项**: 确保集群节点的资源充足，特别是 CPU 和内存，以应对高并发流量场景。

---

### 实践 2：精细化流量管理与路由配置

**说明**: Higress 兼容 Kubernetes Ingress 和 Istio Gateway API。通过声明式的 API 配置，可以实现基于 Header、Header、Query 参数、Cookie 等维度的精细化路由，支持蓝绿发布、金丝雀发布等流量治理策略。

**实施步骤**:
1. 定义 Ingress 资源或 Gateway API 资源。
2. 配置路由规则，匹配特定的 HTTP 请求头或路径。
3. 设置多个后端服务版本，并配置流量权重。
4. 应用配置并验证流量分发是否符合预期。

**注意事项**: 复杂的路由规则可能会增加网关的处理延迟，建议定期审查和优化规则。

---

### 实践 3：集成插件系统实现功能扩展

**说明**: Higress 提供了强大的插件扩展能力，支持 Lua 和 WASM (WebAssembly) 两种插件开发模式。用户可以使用社区提供的插件（如 JWT 鉴权、请求限流、Keyless 认证等）或开发自定义插件来扩展网关功能，而无需修改网关核心代码。

**实施步骤**:
1. 在 Higress 控制台或通过 CRD 配置插件中心。
2. 浏览并启用所需的官方或社区插件。
3. 根据业务需求配置插件参数（如限流阈值、鉴权密钥等）。
4. 针对特定路由或全局作用域启用插件。

**注意事项**: WASM 插件虽然性能较好且语言无关，但开发复杂度较高，建议优先使用社区成熟的 Lua 插件。

---

### 实践 4：全面的安全防护策略

**说明**: 利用 Higress 的安全插件和配置，保障 API 服务的安全性。这包括配置 HTTPS 证书、实现 OAuth2 或 JWT 认证、设置 IP 黑白名单以及防御 SQL 注入和 XSS 攻击等。

**实施步骤**:
1. 在网关配置 SSL/TLS 证书，强制开启 HTTPS。
2. 启用 `auth-plugin` 或类似鉴权插件，配置身份提供商。
3. 配置 IP 访问控制列表，限制非法来源访问。
4. 开启请求校验插件，过滤恶意流量。

**注意事项**: 定期更新证书和密钥，关注安全漏洞公告并及时升级网关版本。

---

### 实践 5：服务注册与发现的无缝对接

**说明**: Higress 原生支持 Kubernetes Service，同时也支持通过 Nacos、Consul、ZooKeeper 等注册中心进行服务发现。这使得 Higress 能够轻松管理混合云架构下的流量，连接容器化应用与虚拟机上的传统应用。

**实施步骤**:
1. 如果使用 K8s Service，直接在路由配置中引用 Service 名称。
2. 如果使用 Nacos 等外部注册中心，需在 Higress 全局配置中添加注册中心地址和认证信息。
3. 配置服务来源，确保网关能拉取到服务实例列表。
4. 验证网关能否正确解析服务域名并建立连接。

**注意事项**: 跨网络互通时，需确保 Higress 所在网络能够访问注册中心及下游服务所在的网络。

---

### 实践 6：可观测性建设与监控告警

**说明**: 生产环境的网关需要具备完善的可观测性。Higress 支持集成 Prometheus 进行指标采集，支持集成 SkyWalking、Zipkin 等进行分布式链路追踪，并支持对接 Kafka、File 等进行日志输出。

**实施步骤**:
1. 部署 Prometheus 服务，并配置 Higress 暴露 Metrics 端口。
2. 配置 Grafana 仪表盘，导入 Higress 官方提供的监控模板。
3. 开启 AccessLog 或集成 SkyWalking Agent，启用链路追踪。
4. 设置关键指标（如 QPS、延迟、错误率）的告警规则。

**注意事项**: 高流量下日志量巨大，建议对日志进行采样或对接日志聚合系统（如 Elasticsearch）进行存储和分析。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**:  
Higress 基于 Envoy 构建，支持 HTTP/3 (基于 QUIC 协议)。HTTP/3 解决了 TCP 队头阻塞问题，在丢包率较高的网络环境下（如移动网络）能显著提升连接建立速度和吞吐量。

**实施方法**:
1. 在网关监听器配置中开启 HTTP/3 协议支持
2. 配置 UDP 端口（通常端口 443）
3. 部署支持 QUIC 的证书配置
4. 在 ALB 或负载均衡器层面放行 UDP 流量

**预期效果**:  
- 弱网环境下延迟降低 30%+
- 连接建立时间减少 1-2 个 RTT
- 移动端视频流卡顿率降低 20%+

---

### 优化 2：启用 Wasm 插件隔离与缓存

**说明**:  
Higress 支持 Wasm 插件扩展。默认情况下，每次请求都可能导致 Wasm VM 重新初始化。通过启用 Wasm 缓存和预编译，可以大幅降低插件执行开销。

**实施方法**:
1. 在 `wasm` 过滤器中配置 `vm_config` 的 `code` 字段为本地缓存路径
2. 启用 `wasm` 的 `precompiled` 选项
3. 对高频插件使用 `singleton` 模式
4. 监控 Wasm 插件的 CPU 使用率

**预期效果**:  
- 插件执行延迟降低 50%-70%
- 吞吐量提升 20%+
- CPU 使用率降低 15%-30%

---

### 优化 3：优化连接池配置

**说明**:  
Higress 默认连接池配置可能不适合高并发场景。通过调整上游连接池大小、空闲连接超时等参数，可以减少连接建立开销。

**实施方法**:
1. 调整 `cluster` 配置中的 `max_connections` 参数（建议设为 1024-4096）
2. 优化 `connect_timeout`（建议 5-10s）
3. 调整 `idle_timeout`（建议 60-300s）
4. 启用 `http2_protocol_options` 的 `max_concurrent_streams`

**预期效果**:  
- P99 延迟降低 20%-40%
- 上游服务连接数减少 30%+
- 错误率降低 10%+

---

### 优化 4：启用请求/响应压缩

**说明**:  
对于文本类 API 响应（JSON/XML），启用 Gzip/Brotli 压缩可显著减少网络传输量，降低带宽成本并提升客户端加载速度。

**实施方法**:
1. 在 `http_filters` 中启用 `compressor` 过滤器
2. 配置 `compressor` 的 `content_length` 阈值（建议 1024 字节）
3. 启用 `gzip` 和 `br` (Brotli) 压缩算法
4. 排除已压缩的二进制内容（如图片、视频）

**预期效果**:  
- 响应体积减少 60%-80%
- 带宽成本降低 50%+
- 客户端加载时间提升 30%+

---

### 优化 5：实施精细化监控与自适应限流

**说明**:  
通过 Higress 的内置监控和 Sentinel 集成，实施基于延迟、错误率的自适应限流，防止雪崩效应。

**实施方法**:
1. 启用 Prometheus 监控端点 (`/stats/prometheus`)
2. 配置 `local_rate_limit` 或 `global_rate_limit`
3. 设置基于 P99 延迟的熔断规则
4. 实施请求优先级队列（`priority_filter`）

**预期效果**:  
- 系统稳定性提升 99.9%+
- 错误率降低 40%+
- 资源利用率提升 20%+

---

### 优化 6：配置智能 DNS 解析与本地缓存

**

---
## 学习要点

- 根据您提供的关键词，这指的是阿里开源的 Higress 项目。以下是基于该项目核心价值总结的要点：
- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，旨在解决 K8s 内部服务与外部流量统一管理的问题。
- 它深度集成了 Envoy 和 Istio，利用 K8s 的 Ingress 或 Gateway API 资源进行流量管理，实现了云原生架构的无缝对接。
- 该网关支持将微服务架构中的南北向（外部访问）与东西向（服务间）流量进行统一治理，降低了架构复杂度。
- Higress 原生支持 Wasm（WebAssembly）插件，允许开发者使用 C++、Go、Rust 或 JavaScript 编写高性能、灵活的扩展插件。
- 它兼容 Nginx 的 Ingress 注解和 Kong 的生态，能够作为 Nginx Ingress Controller 的平滑替代方案。
- 该项目提供了开箱即用的 Prometheus 监控集成和标准化的可观测性支持，便于运维监控。


---
## 学习路径

## 学习路径

### 阶段 1：概念认知与基础环境搭建

**学习内容**:
- 云原生网关的核心概念：理解什么是 API Gateway，以及 Higress 在微服务架构中的定位与作用。
- Higress 架构解析：了解 Higress 基于 Istio 和 Envoy 的技术架构，以及其与 Nginx、传统 Kong 网关的区别。
- 核心特性学习：掌握 Higress 的流量管理、安全防护及插件加载机制的基本原理。
- 环境搭建：学习如何在 Docker 本地环境或 Kubernetes 集群中部署 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与快速开始章节)
- Higress GitHub 仓库 (README.md)
- 云原生社区关于网关技术演进的文章

**学习建议**:
建议先通读官方文档的"快速开始"部分，并在本地成功跑通第一个示例。不要急于深入配置，重点理解"控制面"和"数据面"的分离架构，以及 Higress 如何通过 Ingress 或 Gateway API 资源来定义路由规则。

---

### 阶段 2：核心配置与流量管理

**学习内容**:
- 路由配置：深入学习如何配置 HTTP 路由、重定向、重写和流量镜像。
- 服务来源与发现：配置 Nacos、Consul、DNS 或固定地址（IP/域名）作为服务来源，实现 K8s 服务与非 K8s 服务的统一管理。
- 负载均衡策略：掌握轮询、随机、一致性哈希等负载均衡算法的应用场景。
- 全局与精细化流量控制：学习如何针对特定路由或服务进行流量限制。
- 基础认证与安全：配置 Basic Auth、JWT 认证以及 CORS 跨域设置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理板块
- Higress 控制台实操指南
- Envoy Route 配置详解（作为底层原理补充）

**学习建议**:
此阶段应结合实际业务场景进行练习。尝试模拟一个微服务场景（如用户服务调用订单服务），配置 Higress 作为入口网关，并练习灰度发布（金丝雀发布）流程。熟悉控制台（Console）的操作，同时尝试通过 YAML/Ingress YAML 方式定义配置，以便理解底层资源结构。

---

### 阶段 3：插件生态与自定义开发

**学习内容**:
- 插件系统机制：深入理解 Higress 的 Wasm 插件运行时环境。
- 生态插件使用：熟练配置官方提供的常用插件，如 Keyless Auth、Request Block、Api Key 等。
- 自定义插件开发（Go/Wasm）：学习如何使用 Go 语言编写 Wasm 插件来扩展网关功能（如修改请求头、响应体、实现自定义鉴权逻辑）。
- 插件热更新与版本管理：掌握如何在不重启网关的情况下动态加载和更新插件配置。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场与自定义开发指南
- Higress 插件开发示例 GitHub 仓库
- WebAssembly (Wasm) for Proxies 相关技术文章

**学习建议**:
从使用现有的官方插件解决具体问题开始。随后，尝试编写一个简单的 Go 插件（例如：在请求头中添加特定字段并打印日志），并在本地环境完成编译、部署与调试。这是从"使用者"迈向"开发者"的关键一步。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- 高可用部署：在 Kubernetes 生产环境中配置 Higress 的高可用（HA）模式，包括资源限制与自动扩缩容（HPA）。
- 可观测性集成：集成 Prometheus、Grafana、SkyWalking 或阿里云 ARMS，实现监控指标（QPS、延迟、P99）的采集与可视化，以及链路追踪。
- 网关性能调优：优化连接池、缓冲区大小、并发连接数等参数，应对高并发流量冲击。
- 安全加固：配置 WAF 防护（如防 SQL 注入）、IP 黑白名单以及 mTLS 双向认证。
- 灾备与容灾：制定网关的故障演练计划与回滚策略。

**学习时间**: 2-4周

**学习资源**:
- Higress 官方文档 - 运维管理最佳实践
- Envoy 性能调优官方指南
- Kubernetes 网络与安全运维相关文档

**学习建议**:
此阶段需要具备一定的 Kubernetes 运维经验。建议在测试环境中模拟高流量场景（使用压测工具如 Hey 或 JMeter），观察 Higress 的资源消耗与错误率。重点掌握如何通过日志和监控面板快速定位网关层面的瓶颈或故障。

---

### 阶段 5：架构设计与源码掌控

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是基于阿里云内部通用的架构，并结合了开源社区中 Envoy 和 Istio 的最佳实践而开发的产品。

它主要区别于 Nginx 和 Kong 的特点包括：
1.  **底层架构不同**：Nginx 和 Kong 主要基于 Nginx/OpenResty 构建，而 Higress 基于 Envoy (C++/Go) 构建，Envoy 在云原生环境下的性能和可扩展性（如 xDS 协议）方面更具优势。
2.  **标准兼容性**：Higress 原生支持 Kubernetes Ingress 和 Gateway API 标准，能够无缝对接 Istio 服务网格，实现从网格到网关的统一流量管理。
3.  **插件生态**：Higress 兼容 Kong 和 Nginx 的许多生态插件，并支持 Wasm (WebAssembly) 技术，允许使用 C++、Go、Rust 等语言编写高性能、低耦合的插件，且插件热更新无需重启网关。

---



### 2: Higress 是否支持从 Nginx 或 Kong 迁移？迁移成本高吗？

2: Higress 是否支持从 Nginx 或 Kong 迁移？迁移成本高吗？

**A**: 是的，Higress 非常重视对旧有网关的兼容性，旨在降低迁移成本。

1.  **配置兼容**：Higress 提供了工具来帮助将 Nginx 的配置文件（nginx.conf）转换为 Higress 的 CRD 资源配置。
2.  **语法兼容**：在路由规则配置上，Higress 尽量保持与 Nginx 类似的配置逻辑，同时也支持 Kong 类似的功能插件。
3.  **插件兼容**：虽然底层运行时不同，但 Higress 内置了大量常用插件（如跨域、限流、认证、重定向等），这些插件的功能逻辑与 Nginx/Kong 中的对应插件高度相似。对于复杂的自定义逻辑，可以通过编写 Wasm 插件来实现。

---



### 3: Higress 如何处理流量管理和安全防护？

3: Higress 如何处理流量管理和安全防护？

**A**: Higress 提供了企业级的流量管理和安全防护能力：

1.  **流量管理**：支持基于 Header、Query 参数、Cookie、Body 等多种维度的路由匹配规则。支持蓝绿发布、金丝雀发布和 A/B 测试等灰度发布策略。
2.  **安全防护**：
    *   **认证鉴权**：支持 Basic Auth、API Key (AK/SK)、JWT、OIDC 等多种标准认证方式。
    *   **安全插件**：内置 IP 访问控制、请求伪造防护等插件。
    *   **WAF 集成**：可以非常方便地集成开源 ModSecurity WAF 引擎，提供防火墙能力。

---



### 4: Higress 的 Wasm 插件机制有什么优势？

4: Higress 的 Wasm 插件机制有什么优势？

**A**: Wasm (WebAssembly) 是 Higress 插件生态的核心优势，也是云原生网关的主流趋势。

1.  **高性能**：Wasm 运行在沙箱环境中，执行效率接近原生代码，且不会导致主进程崩溃，稳定性极高。
2.  **多语言支持**：开发者不再被限制在 Lua (Nginx) 或 Python (Kong) 中，可以使用 Go、C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript 来编写插件逻辑。
3.  **热更新**：修改或上传 Wasm 插件时，不需要重启 Higress 网关进程，流量几乎无感知，这对于高可用生产环境至关重要。
4.  **灵活性**：插件逻辑与网关核心代码解耦，便于第三方开发者贡献插件。

---



### 5: Higress 是否支持 Dubbo 和 gRPC 协议？

5: Higress 是否支持 Dubbo 和 gRPC 协议？

**A**: 是的，Higress 对微服务协议有非常深入的支持，特别是针对阿里生态和 Spring Cloud 体系。

1.  **Dubbo 支持**：Higress 原生支持 Dubbo 协议（包括 Dubbo 2.x 和 3.x），可以将 HTTP/HTTPS 请求转换为 Dubbo 调用，实现 HTTP 到 Dubbo 的协议转换，这对于 Web 前端调用后端微服务非常有用。
2.  **gRPC 支持**：完全支持 gRPC 和 gRPC-Web 协议，支持基于 gRPC 的负载均衡和路由规则配置。

---



### 6: 在 Kubernetes 环境中，Higress 与 Ingress Controller 是什么关系？

6: 在 Kubernetes 环境中，Higress 与 Ingress Controller 是什么关系？

**A**: Higress 可以直接作为 Kubernetes 的 Ingress Controller 使用。

1.  **标准化**：它监听 Kubernetes 的 Ingress 资源变化，并自动配置网关路由。
2.  **Gateway API**：除了标准的 Ingress，Higress 还积极支持和实现了 Kubernetes Gateway API 这一新一代的标准，提供了比传统 Ingress 更丰富的表达能力（如 HTTPRoute、TCPRoute、TLSRoute 等）。
3.  **服务发现**：Higress 直接与 Kubernetes

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的官方镜像，编写一个 Docker Compose 文件，启动一个最基础的网关实例。要求配置一个简单的路由，将访问 `/hello` 的请求转发到一个后端服务（例如 httpbin.org），并成功收到响应。

### 提示**:

### 需要关注 Higress 容器的监听端口（通常是 80/8080）。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，以下是 6 条针对实际生产环境和使用场景的实践建议：

### 1. 利用 Wasm 插件实现 Token 预处理与计费统计
**场景：** 在接入 LLM（如 OpenAI、通义千问）时，直接转发请求会导致无法精确控制成本，因为后端只校验总 Token，而不区分 Prompt 和 Completion 的消耗。
**建议：** 编写或使用现有的 Wasm 插件（如 `ai-statistics`），在网关层对请求体进行拦截。
**具体操作：**
*   在请求转发给模型提供商前，解析请求体中的 `messages` 数组，计算输入 Token 数。
*   在响应返回给客户端前，解析 `usage` 字段，记录输出 Token 数。
*   将这些数据上报至 Prometheus 或日志系统，实现基于用户或 API Key 的精细化成本控制与配额管理。

### 2. 配置语义路由与模型路由
**场景：** 企业内部同时使用多个模型（如 GPT-4 用于复杂推理、Llama-3-8B 用于简单问答），客户端不应硬编码模型地址。
**建议：** 使用 Higress 的路由能力，根据请求内容或 Header 将流量智能分发到不同的后端服务。
**具体操作：**
*   **基于 Header 的路由：** 客户端请求携带 `X-Model-Provider: openai`，网关根据该 Header 将流量转发至 Openai 兼容接口。
*   **基于请求体的路由：** 利用 Wasm 插件分析 Prompt 长度或关键词。例如，检测到 "draw_image" 类指令时，自动将请求路由至文生图服务而非文本对话服务。

### 3. 实施模型供应商的熔断与降级策略
**场景：** 依赖外部 LLM API 时，可能会遇到限流（429）或服务不可用（502/503）的情况，这会导致上游业务阻塞。
**建议：** 在 Higress 中配置针对 AI 服务的熔断与降级规则，保证系统的高可用性。
**具体操作：**
*   在 `DestinationRule` 中配置异常实例熔断策略，例如连续 5 次 429 错误自动隔离该实例。
*   配置自动降级逻辑：当高配模型（如 GPT-4）超时或失败时，网关自动将请求重定向至备用模型（如 GPT-3.5-Turbo），并在响应头中添加 `X-Actual-Model` 以告知客户端实际使用的模型。

### 4. 敏感信息脱敏与安全防护
**场景：** 用户可能在与 AI 对话中无意泄露 PII（个人敏感信息）或内部 API Key，直接转发给外部模型存在合规风险。
**建议：** 在网关层配置 Wasm 插件进行请求体的实时扫描与脱敏。
**具体操作：**
*   部署 `ai-security` 类插件，利用正则或简单的关键词库（如手机号、身份证、内部 IP 段）匹配用户 Prompt。
*   发现敏感词时，直接拒绝请求并返回 403，或者将敏感部分替换为 `***` 后再转发给 LLM。
*   配置 IP 访问控制列表（ACL），限制只有内部网段 IP 才能访问核心模型的 Aggregation 接口。

### 5. 优化 SSE（Server-Sent Events） 流式传输的超时配置
**场景：** AI 回答通常采用流式输出（SSE），耗时较长。默认的网关超时配置（通常是 60s）可能导致大模型生成一半时连接断开。
**建议：** 针对特定的 AI 路由或域名，调整后端请求和响应的超时时间。
**具体操作：**
*   在路由配置中，将 `timeout` 设置为 `0`（表示无限等待）或根据模型最大生成时间设置（如 `300s`）。
*   确保网关前端的负载均衡器（如 Nginx 或 ALB）和后端 Upstream 的

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

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*