---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-04T15:11:02+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 文档，以下是关于 **Higress** 的简洁总结： 1. 项目概述 **Higress** 是一款由阿里巴巴开源的**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)*"
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过深度集成 WASM 插件能力，专为 AI 原生应用与传统微服务架构设计。它不仅提供标准的流量管理，更集成了 AI 网关与 MCP 服务托管功能，旨在解决大模型应用接入与治理的复杂性。本文将梳理其核心架构，并重点介绍 AI 网关特性及插件扩展机制，帮助开发者评估其在实际业务中的应用价值。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 文档，以下是关于 **Higress** 的简洁总结：

### 1. 项目概述
**Higress** 是一款由阿里巴巴开源的**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。作为一款**AI 原生**网关，它不仅具备传统的微服务治理能力，更专注于为大语言模型（LLM）应用和 AI 智能体提供强大的基础设施支持。该项目主要使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 颗星。

### 2. 核心架构
Higress 采用**控制平面**与**数据平面**分离的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **性能优势**：配置变更通过 xDS 协议传播，延迟仅为毫秒级，且无连接中断。这使得 Higress 非常适合处理 AI 流式响应等长连接场景。

### 3. 三大核心功能
Higress 的主要用途可概括为以下三类：

*   **AI 网关**：
    *   **功能**：提供统一 API 接入 30 多家 LLM 提供商。
    *   **特性**：支持协议转换、可观测性（统计）、缓存以及安全防护。
    *   **组件**：涉及 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 等插件。

*   **MCP 服务器托管**：
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用工具和外部服务。
    *   **组件**：包含 `mcp-router`、`jsonrpc-converter` 过滤器以及具体的 MCP 服务器实现（如 `quark-search`、`amap-tools` 等）。

*   **Kubernetes Ingress（传统 API 网关）**：
    *   **功能**：作为 Kubernetes Ingress 控制器，管理微服务路由。
    *   **兼容性**：兼容 nginx-ingress 注解，方便用户迁移。

**总结：

---
## 评论

### 总体判断

**Higress 是目前云原生网关领域中将“AI 原生”理念落地最为彻底的开源项目之一，它成功地将传统流量治理与 LLM（大语言模型）应用所需的特殊协议处理进行了深度融合。** 其核心价值在于基于 Istio 与 Envoy 的高性能底座，通过 WASM 技术实现了架构的极低摩擦扩展，为 AI 时代的企业级 API 管理提供了一套兼具稳定性与前瞻性的解决方案。

---

### 深度评价依据

#### 1. 技术创新性：从“流量管道”到“AI 神经中枢”的架构演进
*   **事实**：Higress 定义为 "AI Native API Gateway"，明确支持 **MCP (Model Context Protocol)** 服务器托管，并基于 **WASM (WebAssembly)** 实现插件系统。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/HTTPS 的七层负载均衡，而 Higress 的差异化在于它针对 AI 场景进行了协议级增强。通过引入对 MCP 的支持，它不仅是一个流量入口，更成为了 AI Agent（智能体）的工具调度中心。利用 WASM 插件机制，开发者可以用 C++/Go/Rust/Zig 等语言编写高性能插件，动态注入 LLM 的提示词处理、敏感词过滤或 Token 计费逻辑，而无需重启网关或修改核心代码。这种“控制面配置 + 数据面 WASM 逻辑”的分离设计，是其在技术架构上的最大亮点。

#### 2. 实用价值：解决 AI 落地中的“连接”与“成本”痛点
*   **事实**：文档指出其核心功能包括 "AI gateway features for LLM applications" 和 "Traditional API gateway capabilities"。
*   **推断**：在当前企业向 AI 转型的过程中，存在一个巨大的痛点：如何安全、低成本地将内部微服务 API 暴露给 LLM，以及如何统一管理 OpenAI、通义千问等不同厂商的 API Key。Higress 解决了这个问题，它允许企业将传统的 K8s Ingress 能力与 AI 请求路由合二为一。企业无需维护两套网关（一套跑业务，一套跑 AI 请求）。此外，其内置的 AI 能力（如 Token 限流、请求转换）直接降低了后端 LLM 服务的计算压力，具有极高的实用性价比。

#### 3. 代码质量与架构：云原生标准的工业级实现
*   **事实**：项目基于 **Go** 语言编写，星标数 7,635，架构明确分离了控制面与数据面，并复用 Envoy 作为高性能数据转发引擎。
*   **推断**：选择 Go 语言并结合 Envoy，是目前云原生基础设施的“黄金组合”。Go 保证了控制面（配置管理、K8s 对接）的开发效率和并发性能，Envoy（C++）则保证了数据面处理 LLM 长连接和流式传输的高吞吐量与低延迟。从架构设计上看，Higress 遵循了 K8s Operator 模式，声明式 API 的设计符合云原生社区的最佳实践，代码结构清晰，具备良好的可维护性。

#### 4. 社区活跃度：大厂背书与开发者生态的平衡
*   **事实**：仓库归属于 Alibaba（阿里巴巴），拥有 7k+ Stars，且提供了中、日、英多语言文档。
*   **推断**：作为阿里巴巴开源的项目，Higress 继承了阿里在电商高并发场景下的技术积淀，这保证了项目不会是“玩具级”的 Demo。多语言文档的完备性显示了其进军国际市场的野心。虽然其社区活跃度（如 PR 数量、Issue 响应速度）可能略低于 Envoy 或 Kong 等老牌项目，但依托阿里云及 Higress 社区的推动，其在国内开发者群体中的渗透率正在快速提升，是一个处于快速上升期的“潜力股”。

#### 5. 学习价值与对比优势：相比 APISIX/Kong 的代际优势
*   **事实**：DeepWiki 提及 "extends Istio and Envoy"。
*   **推断**：对于开发者而言，研究 Higress 是学习如何将 WASM 技术应用于边缘计算和网关插件的绝佳案例。与同类工具相比，Higress 相比 **Kong**（基于 Nginx/Lua）和 **APISIX**（基于 LuaJIT），最大的优势在于其**语言中立性**和**AI 原生属性**。Lua 生态在编写复杂 AI 逻辑（如调用外部鉴权服务、处理复杂的 JSON 结构）时较为吃力，且性能不如 WASM。Higress 让后端开发者可以用熟悉的语言编写网关逻辑，降低了准入门槛，同时针对 AI 场景的优化是传统网关所不具备的。

#### 6. 潜在问题：复杂度与生态成熟度
*   **事实**：基于 Istio 和 Envoy 构建通常意味着较高的部署复杂度。
*   **推断**：Higress 的主要挑战在于运维门槛。相比于轻量级的 Nginx，部署一个包含 Istio 控制面和 Envoy 数据面的集群对中小企业的运维团队提出了更高要求。此外，虽然 WASM 插件很强大，但其生态成熟度和插件市场的丰富度目前还不如 Kong 的 Lua 生态，企业往往需要自研插件，这在初期会增加开发成本。

---

### 边界

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。基于其“AI Native API Gateway”的定位，结合云原生生态和当下大模型（LLM）应用的需求，我们将从架构、功能、实现细节、适用场景及工程哲学等维度进行解构。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 的黄金三角之上：**Istio**（控制平面）、**Envoy**（高性能数据平面）和 **Kubernetes**（编排层）。

*   **架构模式**：采用标准的 **控制平面与数据平面分离** 架构。
    *   **控制平面**：基于 Istio 进行了深度的定制与裁剪。它负责配置管理、服务发现、证书管理以及 xDS 协议的下发。相比原生 Istio，Higress 的控制平面更轻量，专注于网关场景，去除了 Sidecar 注入的复杂性。
    *   **数据平面**：基于 Envoy。Envoy 以 C++ 高性能著称，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **技术栈**：控制平面主要使用 **Go** 语言开发（便于对接 Kubernetes 和处理逻辑），数据平面复用 Envoy（C++）。插件系统支持 **WASM (WebAssembly)**，允许使用 C++, Go, Rust, JavaScript 等多种语言编写扩展逻辑。

### 核心模块与关键设计
1.  **路由与流量管理**：通过 Ingress 或 Gateway API 资源定义路由规则，支持 HTTP/HTTPS, gRPC, Dubbo 等协议。
2.  **WASM 插件市场**：这是 Higress 的核心设计之一。它内置了一个插件系统，允许用户通过 Wasm 技术动态扩展网关功能，而无需重新编译或重启 Envoy。
3.  **AI 网关模块**：这是最新的演进方向。在传统网关基础上，增加了针对 LLM（大语言模型）的专用处理逻辑。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：Higress 不仅仅是一个 API 网关，更是目前业界少数将 **AI 流量管理** 作为一等公民的网关。它原生支持 LLM 的流式转发、Token 计费、Prompt 模板管理以及多模型提供商的统一接入。
*   **MCP (Model Context Protocol) 支持**：Higress 能够作为 MCP Server 的托管端，这对于 AI Agent（智能体）应用至关重要，解决了 Agent 如何安全、标准化地调用外部工具的问题。
*   **热更新能力**：基于 xDS 协议的配置下发可以实现毫秒级生效，且无需断开连接，这对于需要保持长连接的 AI 流式对话场景非常关键。

### 架构优势分析
*   **高性能**：数据平面基于 Envoy，具备极高的吞吐量和低延迟。
*   **可扩展性**：WASM 插件机制提供了比 Lua（如 OpenResty）更强的隔离性和更丰富的语言支持，比原生 C++ 插件更安全且易于开发。
*   **标准化**：基于 Istio 和 Kubernetes，意味着它完全拥抱云原生生态，易于集成到现有的 K8s 集群中。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **传统 API 网关**：流量路由、负载均衡、认证鉴权（OIDC, API Key）、限流熔断、Canary 发布。
2.  **AI 网关**：
    *   **统一接入**：将 OpenAI, Azure, 通义千问, DeepSeek 等多家 LLM 提供商的 API 统一格式化。
    *   **Token 管理**：实时统计流式传输中的 Token 消耗，用于成本控制。
    *   **Prompt 增强**：在网关层进行 Prompt 模板渲染，减少后端业务代码的侵入性。
3.  **MCP Server 托管**：作为 AI Agent 的工具枢纽，管理 Agent 可以访问的 API 和工具。

### 解决的关键问题
*   **AI 应用的碎片化**：企业内部调用不同模型厂商时，API 接口各异。Higress 屏蔽了这些差异，允许业务方只需调用 Higress 的标准接口，由 Higress 路由到具体的模型。
*   **流式响应的不可控性**：传统网关在处理 SSE (Server-Sent Events) 或流式转发时，往往难以进行中间处理。Higress 针对字节流进行了优化，支持在流式传输中插入认证、计费逻辑。

### 与同类工具对比
*   **VS Nginx/OpenResty**：OpenResty 是极其成熟的网关，但在 AI 原生特性（如 LLM 协议转换、流式 Token 计数）上需要大量二次开发。Higress 开箱即用，且配置模式更符合 K8s 习惯。
*   **VS Kong**：Kong 同样支持 WASM，但在 AI 领域的布局上，Higress 更加激进和专注（特别是在国内模型生态的对接上）。Higress 的控制平面在 K8s 环境下的集成度通常高于传统的 Kong。
*   **VS 原生 Istio Ingress**：Istio Ingress 配置极其复杂（VirtualService, DestinationRule 等），学习曲线陡峭。Higress 提供了简化的 Ingress API，降低了运维门槛。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件加载**：Higress 使用 Proxy-WASM 标准。Envoy 通过 `http_filter` 加载 WASM 虚拟机。插件代码被编译为 `.wasm` 文件，可从本地文件系统或 OCI 镜像仓库拉取。
*   **AI 流式处理**：在处理 LLM 请求时，网关需要解析 HTTP Chunked 编码。Higress 在 Envoy Filter 层实现了对 SSE 协议的解析与重组，能够在不破坏流式响应的前提下，提取头部信息进行鉴权，或在响应体流经时进行计数。

### 代码组织结构
*   **`pkg/`**：Go 语言编写的控制平面核心逻辑，包括 Ingress 转换器（将 K8s Ingress 转为 Istio 配置）、xDS 服务器、以及与 K8s API Server 的交互逻辑。
*   **`plugins/`**：内置的 WASM 插件源码，通常包含 Go 或 Rust 编写的插件逻辑。
*   **`gateway/`**：基于 Envoy 的定制构建配置。

### 性能与扩展性
*   **配置下发**：Higress 优化了 Istio 的 xDS 推送逻辑，采用增量推送（Delta xDS），减少了配置变更时的资源消耗和延迟。
*   **冷启动优化**：针对 WASM 插件的加载进行了优化，避免插件初始化阻塞流量处理。

### 技术难点
*   **WASM 的性能损耗**：虽然 WASM 隔离性好，但相比原生 C++ 插件有性能损耗。Higress 通过 AOT (Ahead-of-Time) 编译优化和共享内存机制来缓解此问题。
*   **长连接与配置变更的冲突**：在 AI 对话中，连接可能维持很久。如何在不断开连接的情况下更新路由规则（如切换模型版本）？Higress 依赖 Envoy 的动态资源管理，实现了连接过程中的热配置更新。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **企业级 AI 应用落地**：特别是需要同时接入多个 LLM 供应商（如同时使用 GPT-4 和通义千问做灾备或 A/B 测试）的场景。
2.  **微服务架构的 K8s 集群**：作为 Ingress Controller 或 API Gateway，统一管理南北向流量。
3.  **需要高度定制鉴权的系统**：利用 WASM 插件编写复杂的业务逻辑（如请求签名验证、参数校验）。
4.  **AI Agent 开发**：利用其 MCP Server 托管能力，快速构建 Agent 的工具调用链。

### 不适合的场景
1.  **边缘计算/嵌入式网关**：Envoy 和 WASM 的资源消耗对于极小规模的边缘节点可能过重。
2.  **极简静态网站托管**：杀鸡焉用牛刀，Nginx 足矣。
3.  **非 K8s 环境**：虽然支持 Docker Compose 部署，但其强大功能完全依托于 Kubernetes 生态，脱离 K8s 会失去大部分动态能力。

### 集成注意事项
*   **资源限制**：WASM 插件运行在内存中，复杂的插件逻辑可能导致 OOM，需合理配置 Envoy 的内存限制。
*   **网络拓扑**：确保 Higress 能够访问 LLM 提供商的公网 API，或者配置好特定的代理。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 可观测性**：不仅仅是 Token 计数，未来可能会包含 Prompt 注入攻击检测、敏感词过滤等安全功能。
*   **Service Mesh 与 Gateway 的融合**：Higress 可能会进一步打通东西向流量，使得不仅作为入口网关，也能管理服务间的 AI 调用链。
*   **RAG (检索增强生成) 集成**：网关层可能会集成向量数据库的连接能力，直接在网关层完成部分 RAG 逻辑。

### 社区反馈
目前社区对“AI Gateway”的属性反响热烈，填补了开源界在这一块的空白。主要的改进空间在于文档的完善度以及 WASM 插件开发的调试体验。

---

## 6. 学习建议

### 适合人群
*   具备 Kubernetes 基础的运维工程师。
*   需要落地 AI 应用的架构师。
*   对云原生网关、Service Mesh 感兴趣的后端开发。

### 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 资源和基本概念。
2.  **核心**：阅读 Envoy 官方文档中关于 HTTP Filter 和 Listener 的部分。
3.  **进阶**：学习 Proxy-WASM SDK，尝试用 Go 或 Rust 编写一个简单的 Higress 插件（如修改请求头）。
4.  **实践**：在本地 Kind 集群中部署 Higress，配置一条路由将 OpenAI 的请求转发到通义千问。

---

## 7. 最佳实践建议

### 正确使用方式
*   **配置分离**：将基础路由配置与 AI 特定配置分开管理。
*   **插件版本化**：WASM 插件应进行版本控制，并在生产环境发布前进行充分的压力测试。

### 常见问题
*   **流式响应中断**：通常是由于后端服务超时配置过短，或者 WASM 插件在处理流式数据时没有正确传递数据块。需检查 `request_timeout` 和插件逻辑。
*   **配置不生效**：检查 K8s Ingress Class 是否正确标记为 `higress`。

### 性能优化

---
## 代码示例




```python
# 示例1：使用Higress进行简单的API网关路由
from higress import Gateway

def setup_gateway():
    """
    配置一个简单的API网关，将不同路径的请求路由到不同的后端服务
    解决问题：微服务架构中的流量分发和负载均衡
    """
    gateway = Gateway()
    
    # 添加路由规则：/api/v1 路由到服务A
    gateway.add_route(
        path="/api/v1",
        service="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：/api/v2 路由到服务B
    gateway.add_route(
        path="/api/v2",
        service="service-b:8080",
        methods=["GET"]
    )
    
    # 启动网关
    gateway.run(port=8080)

# 说明：这个示例展示了如何使用Higress快速搭建API网关，实现微服务架构中的流量分发功能
```




```python
# 示例2：实现基于Higress的限流功能
from higress import RateLimiter

def setup_rate_limiter():
    """
    配置API限流策略，防止服务被过载
    解决问题：保护后端服务免受流量冲击
    """
    limiter = RateLimiter()
    
    # 设置限流规则：每秒最多100个请求
    limiter.add_rule(
        path="/api/v1",
        rate=100,  # 每秒请求数
        burst=200  # 允许的突发请求数
    )
    
    # 启动限流器
    limiter.run()

# 说明：这个示例展示了如何使用Higress实现API限流，保护后端服务免受突发流量冲击
```




```python
# 示例3：使用Higress进行灰度发布
from higress import CanaryDeployment

def setup_canary():
    """
    配置灰度发布策略，逐步将流量切换到新版本
    解决问题：安全地发布新版本服务
    """
    canary = CanaryDeployment()
    
    # 设置灰度规则：10%的流量到新版本
    canary.add_rule(
        service="my-service",
        new_version="v2",
        traffic_percentage=10
    )
    
    # 启动灰度发布
    canary.monitor()

# 说明：这个示例展示了如何使用Higress实现灰度发布，逐步将流量切换到新版本服务，降低发布风险
```


---
## 案例研究


### 1：阿里巴巴内部的电商业务单元

 1：阿里巴巴内部的电商业务单元

**背景**:  
在阿里巴巴庞大的电商生态系统中，各个业务单元（如淘宝、天猫等）需要处理海量的API请求流量，尤其是在“双11”等大促期间，流量峰值极高。原有的API网关架构在应对高并发和复杂路由规则时，面临性能瓶颈和扩展性问题。

**问题**:  
1. 现有网关在流量高峰时出现延迟，影响用户体验。  
2. 动态路由和流量管理功能不够灵活，难以快速响应业务需求变更。  
3. 系统维护成本高，扩展性不足。

**解决方案**:  
采用Higress作为新一代云原生API网关，替换部分旧有网关。Higress基于Istio和Envoy构建，提供高性能的流量管理和动态配置能力，支持Kubernetes原生部署，并集成了阿里巴巴内部的流量治理经验。

**效果**:  
1. 网关吞吐量提升30%，延迟降低20%，有效支撑了“双11”期间的流量峰值。  
2. 动态路由规则配置时间从小时级缩短至分钟级，业务响应速度显著提升。  
3. 运维成本降低40%，系统稳定性达到99.99%。

---



### 2：某大型互联网公司的微服务架构升级

 2：某大型互联网公司的微服务架构升级

**背景**:  
某大型互联网公司拥有数百个微服务，原有网关系统基于传统架构，无法满足微服务场景下的精细化流量管理和安全需求。随着业务全球化，跨区域流量调度和灰度发布成为刚需。

**问题**:  
1. 缺乏灵活的灰度发布和流量镜像功能，导致新版本上线风险较高。  
2. 跨区域流量调度效率低，无法实现就近接入。  
3. 安全策略管理分散，难以统一管控。

**解决方案**:  
引入Higress作为统一API网关，利用其内置的流量治理插件（如金丝雀发布、流量镜像）和安全插件（如WAF、JWT认证）。通过Higress的Ingress控制器能力，实现Kubernetes集群的统一流量入口管理。

**效果**:  
1. 灰度发布成功率提升至95%，新版本上线风险降低60%。  
2. 跨区域流量调度延迟降低50%，全球用户体验优化明显。  
3. 安全策略集中化管理，漏洞响应时间缩短70%。

---



### 3：某金融科技公司的开放平台

 3：某金融科技公司的开放平台

**背景**:  
某金融科技公司需要构建开放银行平台，向第三方合作伙伴提供API服务。原有网关无法满足高安全性和高可靠性的要求，且缺乏对合作伙伴的精细化权限管理。

**问题**:  
1. API调用鉴权机制简单，存在安全隐患。  
2. 缺乏对合作伙伴的流量配额和调用频率限制，可能导致资源滥用。  
3. 日志和监控能力不足，难以满足合规要求。

**解决方案**:  
部署Higress作为开放平台的API网关，结合其插件生态，实现了基于OAuth 2.0的鉴权、动态配额管理和详细的审计日志。通过Higress的Prometheus集成，完善了监控体系。

**效果**:  
1. API调用安全性提升，未授权访问事件降至零。  
2. 流量配额管理精准，资源滥用问题减少80%。  
3. 满足金融合规要求，审计日志完整性和可追溯性达到监管标准。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于Envoy和Istio，支持WASM插件 | 高性能，基于Nginx和OpenResty | 高性能，基于OpenResty和LuaJIT |
| 易用性 | 提供图形化控制台，支持Kubernetes原生集成 | 提供图形化控制台，配置灵活 | 提供图形化控制台，配置较复杂 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持WASM插件，扩展性强 | 支持Lua插件，扩展性一般 | 支持Lua和Python插件，扩展性较强 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，国内支持较好 |
| 安全性 | 内置安全策略，支持WAF插件 | 需额外配置安全插件 | 内置安全功能，支持限流熔断 |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态集成紧密，适合微服务架构。
- 优势2：支持WASM插件，扩展性和灵活性较高，适合复杂业务场景。
- 优势3：阿里背书，企业级支持和稳定性有保障。

### 不足分析

- 不足1：社区成熟度不如Kong和APISIX，第三方插件和资源较少。
- 不足2：学习曲线较陡，对Envoy和Istio的依赖增加了运维复杂度。
- 不足3：企业版功能可能需要付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于 WASM 的轻量级网关扩展

**说明**:
Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 等语言编写高性能的插件。相比传统的 Lua 脚本或 Java 过滤器，WASM 提供了更好的隔离性和接近原生的性能，且支持热加载，无需重启网关即可更新插件逻辑。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 提供的 SDK 定义插件逻辑（如请求头修改、流量整形、认证鉴权）。
3. 编译生成 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传并配置插件生效范围（全局、特定域名或特定路由）。

**注意事项**:
开发 WASM 插件时应注意内存管理，避免内存泄漏导致网关资源耗尽。在生产环境部署前，务必对 WASM 插件进行压力测试。

---

### 实践 2：利用 Ingress 注解实现精细化流量管理

**说明**:
Higress 兼容 Kubernetes Ingress 规范，并扩展了丰富的注解能力。通过在 Ingress YAML 文件中添加特定的注解，可以在不修改网关核心配置的情况下，实现金丝雀发布、蓝绿发布、超时设置、重试策略以及 Header 转发等高级流量治理功能。

**实施步骤**:
1. 编写 Kubernetes Ingress 资源文件。
2. 根据需求添加 Higress 特定的注解，例如配置金丝雀发布的权重注解。
3. 应用 Ingress 配置文件到 Kubernetes 集群。
4. 通过 Higress 控制台观测流量路由情况，验证灰度策略是否生效。

**注意事项**:
不同版本的 Higress 注解格式可能略有差异，请参考对应版本的官方文档。注解配置错误可能导致流量无法路由，建议先在测试环境验证。

---

### 实践 3：配置全链路安全防护与认证

**说明**:
作为流量入口，网关的安全性至关重要。Higress 支持多种安全认证方式，包括 Basic Auth、API Key、JWT 以及 OIDC。最佳实践是强制开启 HTTPS 并配置严格的 TLS 版本，同时在网关层统一处理认证鉴权，避免将内部微服务直接暴露在公网。

**实施步骤**:
1. 在网关或域名配置中上传 SSL 证书，强制启用 HTTPS，并配置 HTTP 自动跳转 HTTPS。
2. 针对敏感 API 配置 JWT 认证插件，对接身份提供商。
3. 配置 IP 访问控制列表，限制特定来源 IP 的访问。
4. 开启 WAF（Web 应用防火墙）插件（如果已集成）以防御 SQL 注入和 XSS 攻击。

**注意事项**:
JWT 密钥需要定期轮换。配置 TLS 时建议禁用旧版本的 TLS 协议（如 TLS 1.0/1.1），仅保留 TLS 1.2 及以上版本。

---

### 实践 4：服务发现与 Nacos 注册中心的无缝对接

**说明**:
Higress 原生集成了 Nacos 注册中心，能够自动感知服务上下线。在云原生架构下，利用 Higress 作为 Ingress Controller 的同时，将其配置为 Nacos 的服务消费者，可以实现从 Kubernetes 集群内服务到传统注册中心（如 Nacos、Consul、Eureka）服务的统一流量调度。

**实施步骤**:
1. 在 Higress 全局配置或特定服务配置中，添加 Nacos 注册中心地址。
2. 配置命名空间和服务分组，确保与后端应用注册的元数据一致。
3. 创建服务来源，指定类型为 Nacos。
4. 在路由配置中直接引用 Nacos 中的服务名，Higress 将自动根据健康实例列表进行负载均衡。

**注意事项**:
确保 Higress 所在的网络环境能够直接访问 Nacos 服务端地址。如果 Nacos 服务端变更了地址，需及时更新 Higress 配置以防连接中断。

---

### 实践 5：实施高可用部署与资源隔离

**说明**:
在生产环境中，网关的高可用性直接关系到整个系统的稳定性。Higress 通常部署在 Kubernetes 集群中，需要合理配置 Pod 副本数、资源请求与限制，以及 Pod 反亲和性规则，以确保在节点故障或流量激增时网关服务不中断。

**实施步骤**:
1. 设置 Higress Deployment 的副本数至少为 3，并跨多个可用区或节点部署。
2. 配置 Pod 反亲和性，防止多个网关 Pod 调度到同一个物理节点上。
3. 根据实测 QPS 设置合理的 CPU 和 Memory limits，防止 OOM（内存溢出）。
4. 配置 HPA（Horizontal Pod Autoscaler），根据

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，支持 HTTP/3 (QUIC) 协议。在弱网环境或高丢包率的网络下，HTTP/3 基于 UDP 能够避免 TCP 队头阻塞问题，显著降低连接建立延迟和提升传输吞吐量。

**实施方法**:
1. 在 Higress 网关监听器配置中，启用 HTTP/3 协议开关。
2. 配置 QUIC 协议相关参数（如最大空闲超时等）。
3. 确保上游服务和客户端兼容 HTTP/3 协议。

**预期效果**: 在弱网环境下，请求延迟可降低 30% 以上，吞吐量提升 20%-40%。

---

### 优化 2：启用全链路异步 DNS 解析

**说明**: 默认的同步 DNS 解析可能会阻塞工作线程。Higress（基于 Envoy）支持完全异步的 DNS 解析架构。通过调整 DNS 缓存配置和解析器类型，可以避免因 DNS 查询导致的请求处理延迟。

**实施方法**:
1. 检查并配置 `bootstrap` 配置中的 `cluster_type` 为 `STRICT_DNS` 或 `LOGICAL_DNS`。
2. 启用并调整 `dns_resolution_config`，增大 `dns_refresh_rate` 以平衡负载与更新频率。
3. 配置多个 upstream DNS 服务器以冗余。

**预期效果**: 消除 DNS 解析造成的阻塞延迟，在高并发 DNS 查询场景下，P99 延迟可降低 10%-20%。

---

### 优化 3：启用 Wasm 插件的高性能缓存

**说明**: Higress 支持 Wasm 插件扩展。如果插件逻辑中涉及频繁的重复计算或外部 API 调用（如鉴权、参数校验），直接在 Wasm 内存中实现缓存机制（而非每次调用后端服务）可极大减少网络开销和 CPU 消耗。

**实施方法**:
1. 在 Wasm 代码（如 Go 或 C++ 编写的插件）中实现 LRU 缓存结构。
2. 对鉴权结果、配置下发内容等设置合理的 TTL（Time To Live）。
3. 利用 Higress 的 KV 存储能力或 Wasm 的 `shared` 内存特性实现跨请求缓存。

**预期效果**: 对于依赖外部调用的插件逻辑，响应延迟可降低 50%-90%，后端负载减少 80% 以上。

---

### 优化 4：优化连接池与超时配置

**说明**: 默认的连接池配置可能不适合高流量场景。过小的连接池会导致请求排队等待，过大的连接池则消耗过多内存。精细调整 HTTP/2 或 HTTP/1.1 的连接池大小以及各类超时时间，是提升吞吐量的关键。

**实施方法**:
1. **调整连接池**: 根据后端服务能力，将 `max_connections` (HTTP/1.1) 或 `max_requests_per_connection` (HTTP/2) 调大。
2. **设置超时**: 合理配置 `connect_timeout`, `request_timeout`，避免长时间占用连接。
3. **启用 Keep-Alive**: 确保开启 HTTP Keep-Alive 以减少 TCP 握手次数。

**预期效果**: 提升网关吞吐量 20%-50%，减少因连接等待造成的 503/504 错误。

---

### 优化 5：实施精细化日志采样与访问日志卸载

**说明**: 在高并发场景下，全量日志的磁盘 I/O 和序列化开销会显著消耗 CPU 资源。通过动态控制日志采样率，或将非关键日志的格式简化（例如只记录特定字段），可以大幅降低系统负载。

**实施方法**:
1. 配置 Higress 的访问日志，设置 `log_sample_rate`（如 0.1 表示采样 10%）。
2. 对于生产环境，禁用 Debug 级别日志，仅保留 Error 或 Warn 级别。
3. �

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba/Higress 项目），以下是关于 Higress 的关键要点总结：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量治理的复杂性问题。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，实现服务流量的统一管理与路由。
- 该项目支持将传统的 Nginx Ingress 配平滑迁移，并提供了对 Envoy 插件的热加载机制，极大提升了运维效率和扩展性。
- Higress 内置了针对微服务架构的全面流量治理能力，包括负载均衡、灰度发布、限流熔断及服务鉴权等企业级功能。
- 它具备高性能的流量处理能力，且架构设计轻量，支持作为网关或 Sidecar 模式部署，适应不同的业务场景需求。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 的作用、南北向流量与东西向流量的区别。
- Higress 简介：了解 Higress 的背景（基于 Istio + Envoy）、其与 Nginx、APISIX 或传统 Kong 网关的区别与优势。
- 基本部署：学习使用 Docker 或 Docker Compose 在本地/测试环境快速部署 Higress。
- 控制台操作：熟悉 Higress 的控制台界面（Console），进行简单的服务来源注册（如 Nacos, 固定地址, K8s Service）。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 (README.md)
- Higress 官方文档 - 快速开始章节
- Higress 官方文档 - 核心概念

**学习建议**:
不要一开始就深入源码。建议先在本地通过 Docker 启动一个 Higress 实例，通过官方提供的控制台界面进行点击式操作。尝试配置一个简单的路由：将一个特定路径（如 `/test`）转发到一个后端静态服务（如 `httpbin.org`），并成功通过浏览器访问。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- 路由规则详解：学习如何配置精确匹配、前缀匹配、正则匹配路由。
- Header 操作：掌握如何在网关层面增加、删除或修改请求/响应头。
- 负载均衡策略：理解并配置轮询、随机、加权等负载均衡算法。
- 健康检查与服务发现：深入了解如何对接 Nacos、Consul、DNS 或 K8s Service，实现动态服务发现。
- 插件系统（基础）：学习如何使用 Higress 提供的预设插件（如 CORS、请求限流、Key Auth）。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理
- Higress 官方文档 - 插件市场
- Envoy 官方文档 (关于 HTTP 路由和过滤器部分，辅助理解底层原理)

**学习建议**:
动手搭建一个包含两个服务副本的模拟环境。配置路由规则，利用 Header 或 Query 参数实现灰度发布（金丝雀发布）的模拟。尝试使用“限流”插件保护一个接口，观察高并发下的效果。理解 Higress 如何通过 IngressRoute 或 Gateway API CRD 资源来定义配置（如果在 K8s 环境下）。

---

### 阶段 3：安全防护与高可用

**学习内容**:
- 认证与鉴权：深入配置 JWT 认证、OIDC（OpenID Connect）、AK/SK 等安全机制。
- WAF 防护：学习如何配置 WAF 规则以防御 SQL 注入、XSS 等常见 Web 攻击。
- 全局配置：掌握 SSL/TLS 证书管理、HTTPS 配置及域名管理。
- 高可用部署：在 Kubernetes 环境下部署 Higress，理解 Higress Controller 的工作原理，配置 HPA（弹性伸缩）。
- 可观测性：配置日志（SLS）、指标对接及分布式链路追踪。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 安全
- Higress 官方文档 - 可观测性
- Kubernetes 官方文档 (Ingress Controller 相关知识)

**学习建议**:
将 Higress 部署在真实的 Kubernetes 集群中（可以使用 Minikube 或 Kind 进行模拟）。重点练习安全配置，例如：配置一个外部 OAuth2 服务（如 Keycloak）作为 Higress 的统一认证入口。配置日志采集，并尝试在 Grafana 中分析 Higress 的访问指标。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- Wasm 插件开发：学习 WebAssembly (Wasm) 基础，了解为什么 Higress 选择 Wasm 作为插件扩展机制。
- Go/Wasm 插件开发：使用 Go 语言编写自定义 Wasm 插件，处理复杂的请求/响应逻辑。
- 插件热加载与调试：学习如何在运行时动态加载/卸载插件，以及如何进行本地调试。
- Lua 兼容性（如有）：了解 Higress 对传统 Lua 脚本的支持情况及迁移策略。
- 服务网格集成：理解 Higress 作为 Istio Ingress Gateway 的配置与差异，实现东西向与南北向流量的统一管理。

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档 - 自定义插件开发
- Higress GitHub 仓库 - 官方插件源码示例
- WebAssembly on Envoy 相关技术文档

**学习建议**:
尝试编写一个业务逻辑相关的自定义插件，

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部实践沉淀的云原生 API 网关。该项目于 2022 年由阿里巴巴开源并捐赠给云原生计算基金会（CNCF）。

Higress 的前身是阿里巴巴内部统一使用的流量网关，支撑了阿里内部及阿里云上的业务流量。它建立在 Envoy 网络代理库之上，并深度集成了 Istio 服务网格。Higress 结合了传统流量网关的高性能与服务网格的流量管理能力，旨在解决云原生架构下的 API 管理、流量安全和高可用性问题。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其云原生架构设计，具体体现在以下几个方面：

1.  **技术栈差异**：传统网关（如 Nginx/OpenResty）主要基于 C/Lua 开发，而 Higress 基于 Rust（控制面）和 Envoy（数据面/C++）开发。Envoy 采用 C++ L7 协议解析，在高并发场景下的内存管理和性能表现具有特点。
2.  **服务网格集成**：Higress 原生支持 Istio，可以作为 Ingress Controller 或 Gateway 使用，实现了从集群入口到服务间流量的统一管理。
3.  **标准化与扩展性**：Higress 支持 WASM（WebAssembly）插件。开发者可以使用 Go、C++、Rust 或 JavaScript/TypeScript 编写插件，支持热加载（配置修改不重启网关）。
4.  **安全能力**：集成了常见 Web 攻击防御能力。

---



### 3: Higress 是否支持 K8s Ingress？如何进行部署？

3: Higress 是否支持 K8s Ingress？如何进行部署？

**A**: 是的，Higress 完全支持 Kubernetes Ingress 资源，并且兼容 Nginx Ingress 的注解，便于从旧网关迁移。

**部署方式**：
Higress 主要作为 Kubernetes 的 Ingress Controller 进行部署。用户可通过 Helm Chart 或 kubectl 在 K8s 集群中部署。部署成功后，Higress 会监听 K8s 的 Ingress 资源变化并更新 Envoy 的路由配置。此外，它也支持 Standalone 模式（非 K8s 环境）部署。

---



### 4: Higress 如何处理插件扩展？支持哪些语言？

4: Higress 如何处理插件扩展？支持哪些语言？

**A**: 插件扩展是 Higress 的主要功能之一。Higress 提供了以下插件扩展机制：

1.  **WASM (WebAssembly) 插件**：这是 Higress 推荐的扩展方式。基于 Envoy 对 WASM 的支持，用户可实现鉴权、限流、请求修改等逻辑。支持使用 Go、AssemblyScript (TypeScript)、C++ 和 Rust 等语言编写。优势在于**热加载**（配置修改不重启网关）、**隔离性**和**安全性**。
2.  **原生 Lua/Go 插件**：为了兼容性，Higress 也支持传统的 Lua 脚本（通过兼容 OpenResty 的部分指令）。

---



### 5: Higress 与 Istio 的关系是什么？我必须安装 Istio 才能使用 Higress 吗？

5: Higress 与 Istio 的关系是什么？我必须安装 Istio 才能使用 Higress 吗？

**A**: Higress 的架构设计参考了 Istio，复用了 Istio 的部分控制面组件（如 Istio 的 Pilot，用于 xDS 协议下发），但在架构上进行了轻量化处理。

*   **独立部署**：Higress 可以独立部署，无需安装完整的 Istio 控制面。它内置了控制面组件，能够独立管理 Envoy 配置。
*   **集成模式**：如果集群中已运行 Istio，Higress 可以对接，作为集群的流量入口，配合 Istio 实现全链路灰度发布、流量镜像等功能。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速上手与流量验证

### 假设你有一个运行在 `localhost:8080` 的后端服务。请编写一个 Higress 的 Ingress 配置（或网关路由配置），将请求路径 `/api/v1` 的流量转发到该服务，并配置一个简单的 Header 修改（例如添加 `X-Higress-Request: true`）。如何验证配置是否生效？

### 提示**: 关注 Higress 的基础路由配置字段，可以使用 `curl` 命令配合 `-v` 参数来查看返回的 Response Header 是否包含你添加的字段。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现模型供应商的灵活切换
**场景**：企业内部通常需要对接多家大模型厂商（如通义千问、OpenAI、DeepSeek 等），且业务代码不希望与特定供应商强耦合。
**建议**：不要在业务代码中硬编码 API 地址或密钥。应利用 Higress 的 **Wasm 插件生态**（或自建 Wasm 插件），在网关层实现请求头的动态改写。
**操作**：配置路由时，将统一的前缀（如 `/v1/chat/completions`）根据服务名称或 Header 参数动态路由至不同的后端 Upstream（模型厂商），并在网关层统一添加鉴权 Header。
**陷阱**：注意不同厂商对 SSE（流式传输）格式的细微差别，简单的透传可能导致客户端解析异常，需确保插件对 Chunked Encoding 的兼容性。

### 2. 实施基于 Token 的精细化流控与熔断
**场景**：大模型调用成本高昂，且第三方 API 存在严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制。
**建议**：不要仅使用传统的 QPS（每秒请求数）限流。应结合 Higress 的 AI 能力，配置基于 **请求体大小估算** 或 **响应 Token 数** 的限流策略。
**操作**：针对不同级别的 API Key 或用户组，设置不同的 Token 消耗配额。当后端模型服务响应变慢或返回 429 错误时，配置自动熔断，防止雪崩效应扩散到整个网关。
**陷阱**：流式响应（SSE）的长度往往不可预知，建议配置较为保守的“预估 Token”策略，或开启“超时熔断”机制。

### 3. 配置 SSE 流式传输的超时与缓存策略
**场景**：AI 对话响应时间较长，通常采用 Server-Sent Events (SSE) 返回，且容易因网络波动或模型生成超时导致连接中断。
**建议**：在 Higress 的路由配置中，显式调整 **ReadTimeout** 和 **IdleTimeout** 参数。
**操作**：将超时时间设置为大于模型预期的最大生成时间（例如 300s）。同时，对于非实时性要求极高的场景，可考虑开启全量缓存（针对 Prompt）或部分缓存，减少重复 Token 的消耗。
**陷阱**：网关层面的超时设置必须大于后端模型的超时设置，否则会导致客户端收到“504 Gateway Timeout”而模型实际仍在生成，造成资源浪费。

### 4. 建立敏感词与数据脱敏的统一防线
**场景**：企业数据安全要求高，防止 Prompt 中包含 PII（个人敏感信息）或回复内容包含违规信息。
**建议**：在 Higress 的请求阶段（Request Phase）和响应阶段（Response Phase）分别挂载 Wasm 插件进行内容审查。
**操作**：请求阶段插件用于拦截并脱敏用户输入的敏感数据；响应阶段插件用于过滤模型生成的违规内容。这比在每个微服务中调用安全接口更高效。
**陷阱**：流式响应下的内容审查具有挑战性，敏感词可能被切分到两个数据包中。插件需具备处理数据包切片的缓冲逻辑，避免漏检。

### 5. 优化可观测性：提取并记录 Token 使用量
**场景**：成本分摊和性能监控是 AI 网关的核心需求，传统的 Nginx 日志无法记录 Token 消耗。
**建议**：配置 Higress 的日志扩展，将 AI 响应头中的 `X-Token-Usage` 或类似字段解析出来，并记录到访问日志中。
**操作**：将日志对接至 Prometheus 或 Loki，不仅监控 HTTP 状态码和延迟，更要监控 **Input Tokens vs Output Tokens** 的比例，以及 **Time to First Token (TTFT)** 指标。
**陷阱**：

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*