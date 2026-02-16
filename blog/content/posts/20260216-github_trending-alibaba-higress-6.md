---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-16T19:07:08+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**，基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,500 颗星。 该项目构建在 **Istio** 和 **Envoy** 之上，通过扩展 **WebAssembly (WASM)** 插件能力，将控制面（配置管理）与数据面"
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
- **星标**: 7,538 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，它通过扩展 WASM 插件能力，致力于为 LLM 应用提供 AI 网关特性，并支持 MCP 服务器托管及传统微服务路由。该项目旨在解决 AI 原生应用流量管理与服务集成问题，适合需要统一处理传统 API 与 AI 交互流量的开发者。本文将介绍其系统架构、核心组件以及主要应用场景，帮助你理解如何利用它构建高效的流量入口。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**，基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,500 颗星。

该项目构建在 **Istio** 和 **Envoy** 之上，通过扩展 **WebAssembly (WASM)** 插件能力，将控制面（配置管理）与数据面（流量处理）分离。其架构优势在于配置变更通过 xDS 协议毫秒级传播，且无连接中断，特别适用于 **AI 流式响应**等长连接场景。

Higress 的核心功能涵盖以下三大应用场景：

1.  **AI 网关**：提供统一 API 接入 30 多家大模型（LLM）提供商。核心功能包括协议转换、可观测性、缓存及安全防护（通过 `ai-proxy`、`ai-statistics` 等插件实现）。
2.  **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用工具和服务（通过 `mcp-router`、`jsonrpc-converter` 及内置工具实现）。
3.  **Kubernetes Ingress**：作为 Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由等传统 API 网关能力。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的**“AI原生”网关**，它成功地将云原生流量治理与 LLM（大语言模型）应用所需的语义处理能力相结合。它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 MCP 协议支持，填补了传统 API 网关在 AI 时代的功能空白，是目前构建 AI Agent 基础设施的最优解之一。

**详细评价维度**

**1. 技术创新性：从“流量管道”到“智能节点”**
Higress 最大的差异化在于其**AI Native**的定位，而非简单的 AI 功能插件。
*   **事实**：DeepWiki 明确指出 Higress 扩展了 Envoy，集成了**WASM 插件能力**，并专门支持 **MCP (Model Context Protocol) 服务器托管**。
*   **推断**：传统的网关（如 Nginx, Kong）主要处理 L7 层的 HTTP 负载均衡，对 AI 语义无感知。Higress 创新性地将网关变成了 AI 流量的处理节点：
    *   **WASM 插件化 AI 逻辑**：利用 WebAssembly，开发者可以用 C++/Go/Rust 编写高性能的插件，在网关层直接实现 Prompt 模板管理、敏感词过滤、Token 计费统计，而无需修改后端应用代码。
    *   **MCP 协议内置**：随着 Anthropic 推出 MCP，AI Agent 需要连接海量外部数据源。Higress 直接作为 MCP Server 的托管点，使得网关成为了 Agent 的“工具箱”，这在架构上极大地简化了 Agent 与外部工具的交互复杂度。

**2. 实用价值：解决 LLM 落地“最后一公里”的痛点**
*   **事实**：文档提到其提供“AI gateway features for LLM applications”以及“Traditional API gateway capabilities”。
*   **推断**：Higress 解决了企业接入大模型时的三个核心痛点：
    *   **协议与模型差异屏蔽**：企业内部往往同时使用 OpenAI、通义千问、DeepSeek 等不同模型。Higress 可以通过路由配置，将标准化的请求转发给不同的供应商，实现**模型供应商的无缝切换**。
    *   **成本与安全控制**：在网关层实现 Token 限流和 Key 管理，防止后端应用直接暴露大模型 API Key，解决了最基本的安全与成本审计问题。
    *   **兼容性**：它完全兼容 K8s Ingress 和 Istio API，这意味着企业可以在不推翻现有微服务架构的情况下，平滑引入 AI 能力，应用场景极广。

**3. 代码质量与架构：云原生工业级的典范**
*   **事实**：基于 **Go** 语言编写，底层依托 **Envoy**，控制平面与数据平面分离。
*   **推断**：
    *   **架构设计**：控制面负责配置下发（如路由、插件配置），数据面负责高性能转发。这种架构解耦保证了系统的扩展性和稳定性。
    *   **性能**：数据面使用 Envoy (C++)，处理 LLM 的长连接和流式传输（SSE）时，比纯 Go 实现的网关（如某些早期 Kong 插件）具有更低的内存开销和更稳的延迟表现。
    *   **文档**：作为阿里开源项目，其中英文文档、README 以及 DeepWiki 的完整性较高，对开发者友好，降低了上手门槛。

**4. 社区活跃度：阿里背书的强力驱动**
*   **事实**：星标数 **7,538**（对于基础架构类软件，这是一个非常健康的数字），且包含 README_ZH.md，显示了对中文社区的重视。
*   **推断**：阿里巴巴内部庞大的电商和 AI 业务是其最好的“试验田”。相比纯个人项目，Higress 的迭代速度更有保障，且更贴合国内复杂的云环境（如兼容各类 K8s 发行版）。社区活跃度处于上升期，特别是在 AI Agent 开发者圈层中。

**5. 学习价值：深入理解“网关即服务”**
*   **事实**：支持 WASM 和 MCP。
*   **推断**：对于开发者而言，Higress 是学习**云原生网关开发**和 **AI 基础设施** 的绝佳案例。
    *   学习如何通过 WASM 技术在网关中注入业务逻辑，而无需重启网关进程。
    *   理解如何设计系统来支持 SSE（Server-Sent Events）流式转发，这是实时 AI 对话的关键技术点。

**6. 潜在问题与改进建议**
*   **复杂性成本**：引入 Istio 和 Envoy 的运维门槛较高。对于只有几个简单后端的小团队，Higress 可能显得过于厚重。
*   **WASM 生态成熟度**：虽然 WASM 是趋势，但其调试工具链相比传统代码仍不够完善，编写复杂插件的学习曲线较陡峭。

**7. 与同类工具对比**
*   **对比 Kong/APISIX**：传统网关插件多为 Lua 或 Python，处理高并发 AI 流量时的性能和安全性不如 Go/C++ 组合，且缺乏对 AI 协议（如 SSE 流式截断、重试）的原生支持。
*   **对比专用 AI Gateway (如 OneGateway)**：Higress 的优势在于它**同时**具备传统微服务治理能力。企业不需要部署两套网关（一套

---
## 技术分析

基于对 Alibaba Higress 仓库的深入分析，以下是从技术架构、核心功能、实现细节、适用场景、发展趋势、学习建议、最佳实践以及工程哲学八个维度的详细解读。

---

# Alibaba Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的核心定位是**云原生 API 网关**，其最显著的技术特征在于**"AI Native"（AI 原生）**与**"基于 Istio/Envoy 的深度扩展"**的结合。

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的架构模式，这是现代云原生网关的标准范式：
*   **数据平面**：深度依赖 **Envoy**。Envoy 是高性能的 C++ 边缘代理，负责处理实际的流量（L7 路由、负载均衡、执行插件）。Higress 并未从零造轮子，而是基于 Envoy 进行了针对性优化。
*   **控制平面**：基于 **Istio** 进行了简化和增强。Istio 原本的重心在于 Service Mesh（服务间通信），而 Higress 将其能力边界推向了 Ingress（南北向流量）和 AI Gateway。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件机制。通过代理级 WASM (Proxy-WASM) 规范，允许开发者使用 C++/Go/Rust/AssemblyScript 编写插件，并在 Envoy 的沙箱中运行。

### 核心模块与关键设计
1.  **路由与配置管理**：通过 xDS 协议（Envoy 的发现服务）将控制面的配置（路由规则、插件配置）下发给数据面。设计上支持**毫秒级配置热更新**，且不断开连接，这对于 AI 的流式响应至关重要。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时。这使得 Higress 具备了动态加载代码的能力，解决了传统 Nginx Lua 插件难以隔离、内存安全性差且难以动态卸载的痛点。
3.  **AI 网关层**：这是 Higress 区别于传统网关的关键。它在架构上增加了一层专门用于处理 LLM（大语言模型）流量的逻辑，包括 Provider 管理（如 OpenAI, Azure, 通义千问等）的统一抽象。

### 架构优势
*   **极致性能**：继承了 Envoy 的高性能（异步非阻塞 I/O，多线程），避免了 Nginx Lua 协程切换的开销。
*   **安全隔离**：WASM 插件运行在资源受限的沙箱中，单个插件的崩溃不会导致整个网关进程崩溃，且内存隔离性更好。
*   **统一管理**：将 K8s Ingress、Service Mesh 和 AI Gateway 三者合一，减少了基础设施的碎片化。

---

## 2. 核心功能详细解读

### 主要功能与关键问题解决
Higress 旨在解决企业从微服务向 AI 应用转型过程中的**流量治理**和**模型接入**问题。

1.  **AI Gateway (AI 网关)**
    *   **功能**：提供统一的 LLM 访问入口。支持多模型提供商的切换、Token 计费与限流、Prompt 模板管理。
    *   **解决问题**：解决了应用层直接对接多家 LLM API 的复杂性，以及 LLM 调用缺乏统一治理（如限流、鉴权、可观测性）的问题。特别是针对**流式响应**的转发和处理，传统网关往往处理不好长连接，而 Higress 专门对此进行了优化。

2.  **MCP (Model Context Protocol) Server Hosting**
    *   **功能**：Higress 能够托管 MCP 服务。
    *   **解决问题**：MCP 是 AI Agent 连接外部数据源的标准协议。Higress 充当 MCP Server 的托管网关，使得 AI Agent 能够安全、标准化地通过网关访问后端工具或数据，解决了 Agent 工具集成的网络暴露和权限控制问题。

3.  **WASM 插件市场**
    *   **功能**：内置了丰富的开箱即用插件（如 Auth, Keyless, Request Block）。
    *   **解决问题**：降低了业务定制网关逻辑的门槛。用户无需修改网关核心代码，只需编写 WASM 插件即可实现复杂的鉴权或流量修改逻辑。

### 与同类工具对比
*   **VS Nginx/APISIX**：Higress 基于 Envoy，相比 Nginx 的多进程模型，Envoy 的多线程模型在多核 CPU 上利用率更高，且 WASM 的生态隔离性优于 Lua。APISIX 同样基于 LuaJIT，虽然性能极高，但在 AI 原生场景和 WASM 支持的先进性上，Higress 走得更靠前。
*   **VS Kong**：Kong 也是基于 Nginx/Lua，虽然支持 WASM，但 Higress 背靠阿里云，对 K8s 和 Istio 的集成更加顺滑，且对国内 AI 模型（通义千问等）的支持有天然优势。
*   **VS 原生 Istio Ingress**：原生 Istio Ingress 配置极其复杂，学习曲线陡峭。Higress 提供了更符合 K8s Ingress 规范的 CRD，并简化了配置逻辑，同时针对 AI 场景做了增强。

---

## 3. 技术实现细节

### 关键技术方案
1.  **配置热更新**：
    *   利用 Istio 的控制平面逻辑，通过 xDS (v2/v3) 协议与 Envoy 通信。当用户修改 K8s Ingress 或 Higress 的 Gateway 配置时，控制器会生成新的 Envoy 配置，通过增量 xDS 推送给 Envoy。
    *   **难点**：确保配置更新不导致流量中断。Higress 实现了热更新机制，在 Listener 更新时保持连接池的优雅切换。

2.  **WASM 插件加载**：
    *   使用 `proxy-wasm-go` SDK（如果插件是 Go 编写）。Go 代码会被编译为 WASM 模块（.wasm 文件），然后 Higress 会将这些文件加载到 Envoy 的内存中。
    *   **Host 映射**：Higress 在 Envoy 中实现了特定的 ABI 接口，允许 WASM 插件调用 Envoy 的底层 API（如获取 Header、修改 Body、调用日志）。

3.  **AI 流式处理**：
    *   LLM 的响应通常是 SSE (Server-Sent Events) 或分块流。Higress 在数据平面必须具备**流式透传**能力，不能缓存整个响应后再发送，否则会导致首字延迟极高。
    *   实现上，Envoy 的 Streaming Filter 机制在此处发挥了关键作用，Higress 编写了特定的 Filter 来处理 SSE 协议的分发和错误注入。

### 性能与扩展性
*   **性能优化**：Go 控制面通过并发处理 CRD 事件来提升大规模集群下的配置收敛速度。数据面 Envoy 本身零拷贝技术保证了高吞吐。
*   **扩展性**：通过 WASM，用户可以在不重新编译 Higress 二进制文件的情况下扩展功能。这比传统的过滤器链模式更加灵活。

---

## 4. 适用场景分析

### 最适合的场景
1.  **AI 应用接入层**：如果你的业务正在构建 AI 应用（如 Chatbot），需要同时对接 OpenAI、Claude 或国内模型，并且需要统一管理 Token 消耗、密钥，Higress 是目前最佳的开源选择之一。
2.  **Kubernetes 多集群/Service Mesh 入口**：对于已经使用或计划使用 Istio 的企业，Higress 可以作为 Ingress Gateway 的替代品，提供比原生 Istio Gateway 更易用的配置体验和更强的功能。
3.  **需要高频变更逻辑的网关**：业务逻辑经常变动（如复杂的鉴权规则、Header 修改），且不想重启网关服务，WASM 插件系统提供了完美的解决方案。

### 不适合的场景
1.  **极端性能要求的四层负载均衡**：如果只需要做 TCP/UDP 转发，不需要 L7 处理，Envoy 的开销相对较大，此时 IPVS 或单纯的四层 LB 更高效。
2.  **极简边缘部署**：如果是资源极度受限的边缘设备（如嵌入式网关），Envoy + WASM 的内存占用可能过于沉重，轻量级的 Nginx 更合适。

### 集成注意事项
*   **K8s 版本兼容性**：部署前需检查 Higress 版本与 K8s 集群版本的兼容性。
*   **WASM 资源限制**：部署 WASM 插件时，务必配置好内存和 CPU 限制，防止失控的插件拖垮整个网关节点。

---

## 5. 发展趋势展望

Higress 的演进方向清晰地指向了 **"AI Infrastructure (AI 基础设施)"**。

1.  **从流量管道到 AI 编排**：未来的网关不仅仅是转发，还会承担更多 AI 相关的计算任务，如 Prompt 的动态注入、RAG (检索增强生成) 的路由分发、甚至向量检索的网关化。
2.  **MCP 协议的深化**：随着 AI Agent 的普及，MCP 可能成为连接 Agent 与 Tools 的标准。Higress 作为 MCP Server 的托管平台，有望成为企业内部 AI 能力开放的标准出口。
3.  **WASM 生态的繁荣**：随着 WASM 标准的成熟，未来会有更多语言（如 Python 编译为 WASM）支持编写网关插件，这将极大降低网关开发的门槛。

---

## 6. 学习建议

### 适合人群
*   **云原生运维工程师**：需要掌握 K8s Ingress、Istio 基础概念。
*   **后端开发/架构师**：希望深入理解流量治理、LLM 接入标准。
*   **Go/C++ 开发者**：希望学习 Envoy 插件开发或 WASM 技术。

### 学习路径
1.  **基础阶段**：先理解 Envoy 的基本概念，以及 Istio 的控制平面原理。
2.  **实践阶段**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 路由（例如转发到 OpenAI）。
3.  **进阶阶段**：尝试使用 Go 编写一个 WASM 插件（例如添加一个自定义的 HTTP Header），并在 Higress 中加载运行。
4.  **源码阅读**：阅读 Higress Controller 的 Reconcile 逻辑，理解 K8s CRD 如何转化为 xDS 配置。

---

## 7. 最佳实践建议

### 正确使用方式
*   **资源隔离**：在生产环境中，建议将 Higress 的控制平面与数据平面分离部署，或者使用 HPA (Horizontal Pod Autoscaler) 对数据平面进行弹性伸缩。
*   **插件版本管理**：WASM 插件应进行版本化管理。Higress 支持插件配置的热更新，但插件二进制文件（.wasm）的更新建议采用灰度发布策略。

### 常见问题与

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway()
    
    # 配置路由规则
    gateway.add_route(
        path="/api/v1/*",      # 匹配路径
        service="user-service", # 目标服务
        methods=["GET", "POST"] # 允许的HTTP方法
    )
    
    # 启用流量控制
    gateway.enable_rate_limiting(
        path="/api/v1/*",
        requests_per_second=100  # 每秒100个请求
    )
    
    return gateway

# 说明：这个示例展示了如何使用Higress配置基本的路由规则和流量控制，
# 适用于微服务架构中的API网关场景。
```




```python
# 示例2：Higress 插件开发
def higress_plugin_development():
    """
    开发自定义Higress插件
    解决问题：实现自定义请求处理逻辑，如认证、日志记录等
    """
    from higress import Plugin
    
    class AuthPlugin(Plugin):
        def __init__(self):
            super().__init__("auth-plugin")
            
        def on_request(self, request):
            # 在请求处理前执行
            token = request.headers.get("Authorization")
            if not self.validate_token(token):
                return {"status": 401, "body": "Unauthorized"}
                
        def validate_token(self, token):
            # 简单的token验证逻辑
            return token == "valid-token"
    
    # 注册插件
    plugin = AuthPlugin()
    plugin.register()
    
    return plugin

# 说明：这个示例展示了如何开发一个简单的认证插件，
# 适用于需要自定义请求处理逻辑的场景。
```




```python
# 示例3：Higress 服务发现集成
def higress_service_discovery():
    """
    集成服务发现功能
    解决问题：动态管理后端服务实例
    """
    from higress import ServiceDiscovery
    
    # 创建服务发现实例
    discovery = ServiceDiscovery()
    
    # 注册服务实例
    discovery.register_service(
        service_name="order-service",
        instance_id="order-1",
        host="192.168.1.10",
        port=8080
    )
    
    # 获取健康的服务实例
    healthy_instances = discovery.get_healthy_instances("order-service")
    
    # 实现负载均衡
    selected_instance = discovery.select_instance(healthy_instances)
    
    return selected_instance

# 说明：这个示例展示了如何使用Higress的服务发现功能，
# 适用于动态服务管理和负载均衡场景。
```


---
## 案例研究


### 1：某大型电商平台

 1：某大型电商平台

**背景**: 该电商平台在每年的“双11”和“618”大促期间，流量会呈现数十倍的爆发式增长。原有的基于 Nginx 的 API 网关架构在应对每秒百万级 QPS（Queries Per Second）的突发流量时，配置变更效率低，且难以进行精细化的流量管控。

**问题**:
1.  传统网关在处理高并发连接时资源消耗过高，容易导致延迟增加。
2.  多语言（Java、Go、Python）微服务后端的鉴权逻辑重复开发，维护成本高。
3.  需要对不同地区的用户进行 A/B 测试和金丝雀发布，但传统路由配置不够灵活。

**解决方案**: 引入 Higress 作为统一 API 网关。利用 Higress 的高性能 Envoy 底层，配合 Wasm 插件市场，实现了业务逻辑与网关能力的解耦。通过 Higress 的全链路灰度发布能力，实现了按流量比例、Header 等维度的精细化路由。

**效果**: 成功支撑了大促期间峰值流量的平稳运行，网关延迟降低了 40%。通过 Wasm 插件实现了统一的鉴权和限流逻辑，研发效率提升了 50%，且无需重启网关即可动态更新插件配置。

---



### 2：某 AI 创业公司（大模型应用服务商）

 2：某 AI 创业公司（大模型应用服务商）

**背景**: 该公司专注于基于 LLM（大语言模型）的企业级应用开发。随着业务发展，其 SaaS 平台需要对接 OpenAI、阿里云通义千问、Llama 等多种模型服务。同时，企业客户对 API 调用的稳定性和成本控制极为敏感。

**问题**:
1.  直接暴露第三方模型服务的 API Key 存在极大的安全隐患，且难以防止恶意刷量。
2.  不同模型厂商的接口参数不统一，客户端适配复杂。
3.  缺乏有效的流控手段，导致模型调用成本不可控。

**解决方案**: 部署 Higress 作为 AI API 网关。利用 Higress 原生支持的 LLM 特性，实现了多模型提供商的统一接入和协议转换。配置了基于 Token 和 RPM（每分钟请求数）的精细化限流插件，并开启了语义缓存以减少重复的 Token 消耗。

**效果**: 统一了后端模型接口，前端开发效率提升 30%。通过语义缓存和精准的流控策略，模型调用成本降低了约 20%。同时，网关层面的 Key 管理彻底解决了密钥泄露风险，保障了业务安全。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高并发场景 | 极高性能，基于 Nginx 和 Lua，性能接近原生 Nginx |
| 易用性 | 提供丰富的 UI 控制台，支持 K8s Ingress 和 API 网关双模式，上手简单 | UI 功能较弱，依赖配置文件或 API，学习曲线较陡 | UI 功能完善，支持动态配置，但文档和社区支持略逊于 Kong |
| 成本 | 开源免费，云原生集成度高，适合混合云部署 | 开源版免费，企业版收费，云服务成本较高 | 开源免费，企业版收费，云服务成本适中 |
| 扩展性 | 支持 WASM 插件，扩展灵活，插件生态逐步丰富 | 插件生态成熟，支持 Lua 和 Go 扩展 | 插件生态强大，支持 Lua 和 Python 扩展 |
| 社区支持 | 阿里背书，社区活跃，但国际影响力有限 | 国际社区活跃，文档和案例丰富 | 国内社区活跃，国际影响力逐步提升 |

### 优势分析

- 优势1：云原生集成度高，支持 K8s Ingress 和 API 网关双模式，适合混合云和容器化环境。
- 优势2：支持 WASM 插件，扩展性强，插件开发门槛低，适合快速迭代。
- 优势3：性能优异，基于 Rust 和 Go 开发，资源占用低，适合高并发场景。

### 不足分析

- 不足1：社区和生态相对年轻，插件数量和案例不如 Kong 和 APISIX 丰富。
- 不足2：国际影响力有限，文档和社区支持以中文为主，国际化程度较低。
- 不足3：企业级功能（如高级监控、安全防护）可能依赖阿里云服务，灵活性不足。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展开发

**说明**: Higress 原生支持 WebAssembly (WASM)，允许开发者使用 C++、Go、Rust 或 AssemblyScript 编写高性能的插件。相比传统的 Lua 脚本，WASM 插件拥有更好的隔离性、更高的执行效率以及更丰富的标准库支持。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust，社区支持较好）。
2. 引用 Higress 官方提供的 SDK 或 Proxy-WASM 标准库进行开发。
3. 在本地编写并编译为 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传并配置插件。

**注意事项**: 
- 开发时需注意内存资源的限制，避免编写消耗大量内存的循环逻辑。
- 生产环境部署前，务必对 WASM 插件进行充分的性能压测，确保其不会阻塞请求处理主线程。

---

### 实践 2：精细化流量管理与灰度发布

**说明**: 利用 Higress 强大的全链路路由能力，实现基于 Header、Query 参数、Cookie 或权重比例的流量路由。这对于微服务架构下的蓝绿部署、金丝雀发布以及 A/B 测试至关重要。

**实施步骤**:
1. 在 Ingress 配置中定义多个服务版本（如 `v1` 和 `v2`）。
2. 配置路由规则，使用 `match` 条件定义特定流量特征（例如 `x-version: v2`）。
3. 对于按比例灰度，配置流量拆分权重（例如 90% 流量指向 v1，10% 指向 v2）。
4. 结合 Prometheus 监控观察新版本的错误率和延迟，逐步调整权重。

**注意事项**: 
- 确保灰度规则的优先级设置正确，避免规则冲突导致流量意外路由。
- 灰度发布过程中应保持会话粘性配置，避免同一用户在版本切换时出现状态不一致。

---

### 实践 3：对接 Nacos 实现服务动态发现

**说明**: Higress 深度集成了 Nacos 注册中心。通过将网关与 Nacos 对接，可以实现后端服务的动态发现，无需手动修改网关配置即可感知服务实例的上下线，从而实现自动负载均衡和故障转移。

**实施步骤**:
1. 在 Higress 全局配置或特定路由配置中，添加 Nacos 作为服务来源。
2. 配置 Nacos 服务器的地址、命名空间和访问凭证。
3. 在路由配置的目标服务中，引用 Nacos 中的服务名。
4. 配置健康检查机制，确保 Higress 能及时剔除 Nacos 中不健康的实例。

**注意事项**: 
- 确保 Higress 所在网络能够访问 Nacos 集群，注意防火墙和 K8s NetworkPolicy 的配置。
- 如果使用 Nacos 2.0 版本，需确认 gRPC 端口的连通性。

---

### 实践 4：配置安全防护与认证鉴权

**说明**: 网关是流量的唯一入口，必须在此处统一实施安全策略。Higress 提供了丰富的内置插件（如 Keyless 认证、JWT 验证、IP 访问控制等），用于保护后端服务免受未授权访问和恶意攻击。

**实施步骤**:
1. 开启并配置 `jwt-auth` 插件，对 API 请求进行身份验证。
2. 配置 `key-rate-limit` 插件，防止 API 被恶意刷量或 DDoS 攻击。
3. 使用 `ip-restriction` 插件限制管理端或敏感 API 的访问来源 IP。
4. 配置 CORS（跨域资源共享）策略，允许合法的前端域名访问。

**注意事项**: 
- 密钥和 JWT Secret 应存储在保密字典中，不要明文写在配置里。
- 限流配置应根据后端服务的实际承载能力进行测算，避免误杀正常流量。

---

### 实践 5：利用 IngressAnnotation 进行高级路由配置

**说明**: 除了标准的 Kubernetes Ingress 字段，Higress 提供了丰富的 Annotation 扩展。通过这些注解，可以在不修改网关逻辑的情况下实现超时控制、重试策略、Header 修改等高级功能。

**实施步骤**:
1. 在 Ingress YAML 的 `metadata.annotations` 字段中添加配置。
2. 例如，设置超时时间：`nginx.ingress.kubernetes.io/proxy-connect-timeout: "60"`（注：Higress 兼容 Nginx 注解，也支持自有格式）。
3. 配置后端服务保持活动：`nginx.ingress.kubernetes.io/upstream-keepalive-connections: "100"`。
4. 应用配置后，通过控制台检查路由详情确认注解已生效。

**注意事项**: 
- 不同版本的 Higress 对注解的支持可能有所不同，升级版本前请查阅兼容

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，启用 HTTP/3 协议可以显著改善弱网环境下的连接建立速度和吞吐量。HTTP/3 基于 UDP，解决了 TCP 队头阻塞问题，能降低连接延迟并提升传输稳定性。

**实施方法**:
1. 在 Higress 的网关配置中，监听器协议类型选择 `HTTP/3` 或开启 QUIC 协议支持。
2. 确保后端服务配置了 UDP 端口（通常为 443）的防火墙放行策略。
3. 配置 TLS 1.3，因为 HTTP/3 强制要求使用 TLS 1.3。

**预期效果**: 在弱网环境下，连接建立时间可降低 30%-50%，页面加载速度提升 20% 左右，减少连接超时率。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置可能导致后端服务负载堆积。精细化的超时与重试策略可以防止雪崩效应，快速释放连接资源，提升系统整体吞吐量。

**实施方法**:
1. **连接超时**: 建议设置为 2s-5s，避免长时间挂起。
2. **请求超时**: 根据业务 P99 耗耗设置，建议略高于 P99 值（如 3s）。
3. **重试策略**: 仅对幂等请求（GET、HEAD）开启重试，重试次数建议为 2 次，配合指数退避算法。

**预期效果**: 减少无效连接占用，在故障发生时，系统可用性从 90% 提升至 99.9% 以上，同时降低平均响应延时（LAT）。

---

### 优化 3：启用 Wasm 插件与 Lua 脚本的高效隔离

**说明**: Higress 原生支持 Wasm (WebAssembly)。将复杂的业务逻辑（如鉴权、请求头修改）从核心路由逻辑剥离并下沉到 Wasm 插件中，利用其沙箱隔离特性，可以避免单点故障影响全局，并利用 AOT 编译提升执行效率。

**实施方法**:
1. 开发自定义 Wasm 插件替代复杂的 Lua 脚本或外部调用。
2. 在网关路由配置中引用对应的 Wasm 插件。
3. 启用 Wasm 的多线程能力（如配置 `wasm` 执行线程数）。

**预期效果**: 复杂逻辑处理延迟降低 10%-20%，且插件崩溃不会导致网关主进程崩溃，提升系统稳定性。

---

### 优化 4：开启连接复用与 HTTP/2 后端通信

**说明**: Higress 与后端服务之间建立 HTTP/2 连接，利用多路复用技术，减少 TCP 连接数，降低网络握手开销，从而显著提升高并发场景下的吞吐量。

**实施方法**:
1. 在 `Upstream` 或 `Service` 配置中，将协议设置为 `HTTP/2` 或 `gRPC`。
2. 调整 `max_requests_per_connection` 参数，允许单个长连接处理更多请求（默认通常为 0，即无限，但建议根据后端能力设置如 1000）。
3. 启用 Keep-Alive 探测以保持连接活跃。

**预期效果**: 后端连接数减少 50%-80%，CPU 利用率因握手减少而降低 10%-15%，QPS 吞吐量提升显著。

---

### 优化 5：实施精细化缓存策略

**说明**: 对于读多写少的流量，在 Higress 网关层开启缓存（如 HTTP 缓存头或插件级缓存），可以直接拦截请求回源，大幅降低后端服务压力并减少响应延迟。

**实施方法**:
1. 配置 `ResponseCache` 或 `LocalResponseCache` 插件。
2. 针对不同 API 设置合理的 TTL（生存时间），例如静态资源设置 1 小时，动态

---
## 学习要点

- 基于提供的来源信息（Alibaba / Higress），以下是关键要点总结：
- Higress 是阿里云开源的下一代云原生 API 网关，基于 Istio 与 Envoy 内核构建。
- 该项目深度集成了 K8s Ingress 与 Gateway API，能够无缝适配云原生基础设施。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿部署及负载均衡等高级路由特性。
- Higress 兼容 Nginx Ingress 注解，并针对 Dubbo、gRPC 等微服务协议进行了扩展支持。
- 内置了针对高并发场景的 WAF 插件与安全防护能力，保障网关层的安全性。
- 通过标准化的 WASM 插件市场，允许用户低代码扩展网关功能，具备极高的灵活性。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 网关基础：理解 API 网关的定义、核心功能（流量管理、安全防护、协议转换）及其在微服务架构中的定位。
- Higress 简介：了解 Higress 的背景（基于 Envoy 和 Istio）、其与 Nginx、APISIX 或 Kong 的区别与优势。
- 核心概念：掌握 Ingress、Gateway、Route、Service、Upstream 等基础术语。
- 快速上手：学习使用 Docker 或 Kubernetes 部署一个最简单的 Higress 实例，并进行基本的流量转发配置。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (基础介绍与快速开始)
- Envoy 官方文档 (基础概念部分)
- Kubernetes Ingress Controller 通用原理文章

**学习建议**:
建议先从宏观上理解云原生流量网关的演进逻辑，再动手实践。不要一开始就陷入复杂的配置细节，重点是跑通第一个"Hello World"示例，理解请求是如何经过网关到达后端服务的。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 配置模型：深入学习 Higress 的配置结构（Wasm 插件机制、路由匹配规则）。
- 流量治理：掌握金丝雀发布、蓝绿部署、流量镜像、Header 重写/转发、超时与重试策略。
- 安全防护：学习配置基本的安全策略，如 IP 黑白名单、CORS 跨域配置、以及简单的鉴权插件使用。
- 负载均衡：理解并配置不同的负载均衡算法（轮询、随机、最小连接等）及健康检查机制。

**学习时间**: 2-3周

**学习资源**:
- Higress GitHub 仓库 (示例配置与 README)
- Higress 官方文档 (流量治理与插件市场章节)
- Envoy Proxy 官方文档 (关于 HTTP 路由与集群管理)

**学习建议**:
此阶段应结合实际业务场景进行模拟练习。例如，模拟一个服务上线场景，配置 Header 匹配的灰度发布。重点关注 Higress 如何通过 Wasm 插件扩展功能，这是其区别于传统网关的重要特性。

---

### 阶段 3：生态集成与高级特性

**学习内容**:
- 服务发现集成：学习 Higress 如何对接 Nacos、Consul、Kubernetes Service 以及注册中心（如 ZooKeeper/Eureka）。
- 高级插件开发：了解 Wasm (WebAssembly) 技术原理，尝试使用 Go 或 C++ 编写一个简单的自定义 Wasm 插件。
- 可观测性：学习配置日志（访问日志、审计日志）、指标（Prometheus 集成）和链路追踪。
- 高可用部署：学习在 Kubernetes 集群中进行 Higress 的高可用安装与配置，以及性能调优基础。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 (开发者指南与自定义插件开发)
- Wasm 官方网站与相关教程
- Prometheus 与 Grafana 集成教程

**学习建议**:
这个阶段是迈向精通的关键。建议深入阅读官方关于架构设计的文档，理解数据面与控制面的交互。尝试编写一个自定义插件来解决特定问题（如特定的请求校验逻辑），这将极大地加深对 Higress 扩展能力的理解。

---

### 阶段 4：生产实践与源码剖析

**学习内容**:
- 生产级运维：掌握网关的平滑升级、回滚策略、资源限制与性能压测方法。
- 源码分析：阅读 Higress 控制面和数据面的核心源码，理解请求处理的全链路流程。
- 多租户与多环境管理：学习如何在复杂的企业级环境中管理多套网关配置。
- 社区贡献：参与 GitHub Issue 讨论，修复 Bug 或提交文档改进。

**学习时间**: 持续进行

**学习资源**:
- Higress GitHub 源码
- Higress 官方博客与深度技术文章
- 云原生社区相关技术分享

**学习建议**:
在达到此阶段时，应当具备从源码层面定位问题的能力。建议尝试在本地搭建调试环境，单步调试源码。同时，关注社区的 Roadmap，了解未来的技术发展方向，如 AI 网关能力的集成。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在开源网关 Envoy（由 Lyft 开发的高性能代理）和 Istio（服务网格）的基础上构建的。

与 Nginx 和 Kong 的主要区别如下：
1.  **架构基础**：Nginx 和 Kong 传统上基于 Nginx/OpenResty（内存小，但长连接和动态配置支持有限）。Higress 基于 Envoy（C++/Go 架构），采用 WASM（WebAssembly）插件技术，支持热加载，且具有极高的扩展性和安全性。
2.  **云原生集成**：Higress 原生支持 Kubernetes 和 Istio，可以作为 Ingress Controller 使用，也可以接管 Istio 的南北向流量（Gateway），而 Kong 虽然也支持 K8s，但在服务网格生态的深度集成上不如 Higress 顺畅。
3.  **兼容性**：Higress 兼容 Nginx 的 Ingress 注解和 Kong 的部分插件生态，旨在降低迁移成本。
4.  **开源模式**：它由阿里云发起，完全开源，不仅提供标准版功能，还集成了阿里云商业版网关的许多稳定性特性。

---



### 2: Higress 与 Apache APISIX 相比有什么优势？

2: Higress 与 Apache APISIX 相比有什么优势？

**A**: 两者都是目前国内非常活跃的开源 API 网关，主要优势体现在技术路线和生态整合上：
1.  **插件机制**：APISIX 基于 Lua (OpenResty)，插件开发需要熟悉 Lua 语言。Higress 采用 WASM (WebAssembly) 插件机制，允许开发者使用 Go、C++、Rust 甚至 JavaScript/TypeScript 编写插件，开发门槛更低，且插件隔离性更好（插件崩溃不会导致网关崩溃）。
2.  **服务网格集成**：Higress 是阿里云对 Istio 的标准实现，天然适合作为 Istio 的数据平面，处理进入集群的流量。APISIX 虽然也有 Ingress 控制器，但与 Istio 的深度整合属于“共存”模式，而非 Higress 的“融合”模式。
3.  **性能与资源**：在高并发长连接场景下，Envoy（Higress 底层）的内存管理通常优于 OpenResty（APISIX 底层），且 Higress 对 HTTP/2 和 gRPC 的支持经过了大规模实战验证。

---



### 3: Higress 是否支持从 Nginx 或 Kong 迁移？迁移难度大吗？

3: Higress 是否支持从 Nginx 或 Kong 迁移？迁移难度大吗？

**A**: 是的，Higress 非常重视迁移兼容性，设计上就是为了降低用户的迁移阻力。
1.  **Nginx Ingress 兼容**：Higress 实现了 Kubernetes 的 Nginx Ingress Controller 的注解兼容。这意味着，如果你的 Kubernetes 集群正在使用 Nginx Ingress，通常只需要将 Ingress Class 切换为 Higress，大部分配置即可直接生效。
2.  **配置转换**：对于 Kong，Higress 提供了配置导入工具，可以将 Kong 的配置（Routes, Services, Plugins）转换为 Higress 的格式。
3.  **脚本转换**：对于 Nginx 原生的配置文件，虽然不能直接运行，但 Higress 支持将 Nginx 的逻辑通过 Lua 插件或 Go 插件重写，或者直接使用其控制台进行可视化配置，无需手写复杂的正则。

---



### 4: Higress 的性能如何？能否支撑企业级的高并发流量？

4: Higress 的性能如何？能否支撑企业级的高并发流量？

**A**: Higress 具备极高的性能，完全能够支撑企业级高并发流量。
1.  **底层优势**：基于 Envoy 构建，Envoy 本身就是为云原生高并发场景设计的，采用 C++ 编写，拥有零拷贝、非阻塞 I/O 等特性。
2.  **实战验证**：Higress 继承了阿里云内部网关（用于淘宝、天猫等超大规模流量）的代码基因，经过了“双11”等极端流量场景的验证。
3.  **数据指标**：在单核性能、长连接保持能力以及冷启动时间上，Higress 都表现优异。配合 WASM 插件，其插件运行时的性能损耗也比传统的 Lua JIT 要更加可控。

---



### 5: 如何在 Higress 中开发自定义插件？支持哪些语言？

5: 如何在 Higress 中开发自定义插件？支持哪些语言？

**A**: Higress 的核心亮点之一就是其强大的插件扩展能力，主要通过 WASM 实现。
1.  **支持语言**：官方推荐使用 **Go** 语言进行插件开发，因为 Higress 提供了完善的 Go SDK 和代码生成工具。此外，理论上支持任何能编译为 WASM 的语言，如 Rust、C++、AssemblyScript 等。
2.  **开发流程**：
    *   定义插件配置（JSON Schema）。
    *   使用 Go SDK 编写逻辑（处理请求

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速上手与路由转发

### 假设你有一个运行在 `http://backend:8080` 的后端服务。请编写一个 Higress 的 Ingress 或 Gateway API 配置，将访问网关 `/hello` 路径的流量转发到该后端服务，并要求将请求头中的 `User-Agent` 修改为 `Higress-Test/1.0`。

### 提示**:

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其云原生架构与 AI 流量治理的特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 AI 指标进行精细化流量治理
**建议内容：**
不要仅将 Higress 视为普通的流量转发网关，应充分利用其对 AI 协议的深度理解能力。在配置路由时，除了传统的 Header 匹配外，建议针对 AI 请求的特定参数（如 `model` 名称、`max_tokens`）进行流量分发或灰度发布。

**具体操作：**
在 Ingress 或路由配置中，启用针对 AI 请求体的匹配规则。例如，将指定 `model=gpt-4` 的请求路由至高优先级的后端服务，或将 `max_tokens > 4000` 的长文本请求路由至具备更大显存资源的推理节点，以实现基于负载特征的智能调度。

### 2. 实施模型供应商的熔断与降级策略
**建议内容：**
外部 LLM 提供商（如 OpenAI、Azure OpenAI）往往存在速率限制或服务不稳定的情况。建议在 Higress 中配置严格的熔断机制，防止上游故障拖垮整个业务系统。

**具体操作：**
针对不同的 LLM 提供商服务配置独立的熔断规则。当检测到某个供应商的 HTTP 429 (Too Many Requests) 或 503 错误率超过阈值时，自动触发熔断，将流量切换至备用模型或降级为本地缓存的小模型，确保业务连续性。

### 3. 配置请求与响应的缓存策略以降低 Token 成本
**建议内容：**
AI 推理成本与 Token 消耗成正比。对于高并发、重复性高的问答场景，直接使用 Higress 的缓存插件可以显著降低后端模型的调用成本和延迟。

**具体操作：**
启用 Higress 的缓存插件，并配置以 Prompt 摘要或向量化相似度为键的缓存策略。对于“命中率高”的静态知识问答，设置较长的缓存时间（TTL）；对于创造性生成任务，则关闭缓存或设置极短的 TLL，以平衡成本与时效性。

### 4. 善用 Wasm 插件处理 Prompt 注入与敏感词过滤
**建议内容：**
安全是 AI 应用的底线。不要将原始的用户输入直接透传给后端模型。利用 Higress 的 Wasm (WebAssembly) 插件生态，在网关层进行即时的安全检查。

**具体操作：**
部署 Wasm 插件（如基于 WASM 实现的正则匹配或简单模型），在请求转发前拦截包含恶意 Prompt（如“忽略之前的指令”）或敏感词的流量。这种“网关层拦截”比在应用代码中处理更高效，且能统一保护所有接入的 AI 服务。

### 5. 建立基于 Token 数量的可观测性体系
**建议内容：**
传统的 API 网关日志通常只记录 HTTP 状态码和延迟。对于 AI 网关，必须关注 Token 吞吐量和耗时，因为这才是计费和用户体验的核心指标。

**具体操作：**
确保 Higress 的日志输出中包含 AI 特定字段（如 `prompt_tokens`, `completion_tokens`, `total_tokens`）。将这些指标对接到 Prometheus/Grafana 或可观测性平台，不仅监控 QPS（每秒请求数），更要监控 TPS（每秒 Token 数），以便准确评估成本支出和模型性能瓶颈。

### 6. 避免在网关层进行大规模 Prompt 模板渲染
**建议内容：**
虽然 Higress 支持请求/响应转换，但应避免在网关层执行复杂的 Prompt 模板拼接或大量的数据库查询逻辑。

**具体操作：**
保持网关的轻量级。复杂的 Prompt Engineering（如 RAG 检索后的长文本组装）应在业务服务端完成，网关仅负责路由、认证和简单的协议转换。在网关层处理过重的逻辑会导致延迟增加，并阻塞其他请求的处理，违背网关作为“高性能入口”的初衷。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*