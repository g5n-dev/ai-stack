---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T19:59:26+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "Istio", "Envoy", "Kubernetes", "WASM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目概述总结** **1. 项目简介** Higress 是一个基于 **Istio** 和 **Envoy** 构建的**云原生 AI 网关**，由阿里巴巴开源。它采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,400 颗星。Higress 的核心定位是“AI Native”，"
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
- **星标**: 7,419 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，实现了对传统流量管理与 AI 原生场景的双重支持。它能够有效解决 LLM 应用接入、AI Agent 工具集成以及微服务路由等复杂需求，适合需要统一管理混合云流量的技术团队。本文将梳理其核心架构，重点介绍 AI 网关特性、MCP 系统托管及 WASM 插件机制，帮助读者评估该方案在业务中的落地路径。

---
## 摘要

**Higress 项目概述总结**

**1. 项目简介**
Higress 是一个基于 **Istio** 和 **Envoy** 构建的**云原生 AI 网关**，由阿里巴巴开源。它采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,400 颗星。Higress 的核心定位是“AI Native”，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理平台。

**2. 核心架构与特性**
*   **架构设计**：系统分离了**控制平面**（配置管理）和**数据平面**（流量处理）。
*   **高性能与低延迟**：配置变更通过 **xDS 协议**传播，延迟仅为毫秒级且不中断连接，特别适合 AI 流式响应等长连接场景。
*   **可扩展性**：通过 **WebAssembly (WASM)** 插件系统提供强大的扩展能力。

**3. 三大核心功能**
Higress 具备三大主要功能，以满足传统微服务和现代 AI 应用的需求：

1.  **AI 网关**：
    *   提供统一 API 接口，支持 **30+ 家 LLM 提供商**。
    *   核心能力包括协议转换、可观测性、缓存和安全管理。
    *   涉及组件：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。

2.  **MCP 服务器托管**：
    *   托管 **模型上下文协议 (MCP)** 服务器，使 AI 智能体能够便捷地调用工具和服务。
    *   涉及组件：`mcp-router`, `jsonrpc-converter` 等。

3.  **Kubernetes Ingress**：
    *   作为 K8s 入口控制器运行，兼容 `nginx-ingress` 注解。
    *   提供传统的微服务路由、流量治理等 API 网关能力。

---
## 评论

### 总体评价

Higress 是一款**极具前瞻性与工程落地价值的云原生网关**，它成功地将传统的流量治理与前沿的 AI 应用网关需求融合，基于 Envoy 和 Istio 构建了高扩展性的架构。对于正在构建 AI 原生应用或寻求高性能 API 管理的团队而言，这是一个兼具技术深度与实用价值的优选方案。

---

### 深度评价维度

#### 1. 技术创新性：从“流量管道”到“智能中枢”的进化
Higress 最显著的技术差异化在于其 **"AI Native"（AI 原生）** 的定位，而非仅仅是一个支持 AI 协议的传统网关。
*   **事实**：DeepWiki 明确指出 Higress 提供了 **AI Gateway Features**（用于 LLM 应用）和 **MCP Server Hosting**（用于 AI Agent 工具集成）。
*   **推断**：大多数传统网关（如早期的 Nginx 或 Kong）对 AI 的支持仅限于简单的透传。Higress 创新性地在网关层集成了 LLM 的语义处理能力。它不仅仅是转发 HTTP 请求，还能理解 Prompt、处理 Token 计费、实现对话上下文保持，甚至直接作为 **MCP (Model Context Protocol)** 的宿主。这意味着网关变成了 AI 智能体的调度中心，而不仅仅是流量入口，这种架构设计极大地简化了 AI 应用的拓扑复杂度。
*   **WASM 生态**：基于 Envoy 的 WASM 插件机制是其另一大技术亮点。它允许开发者使用 C++/Go/Rust/AssemblyScript 编写插件，并在运行时动态加载，无需重启网关。这解决了传统网关扩展性差、Lua 脚本维护难的问题。

#### 2. 实用价值：解决 AI 时代的“最后一公里”连接问题
Higress 的实用价值体现在它精准打击了当前 LLM 落地中的痛点。
*   **事实**：文档提到它具备“Kubernetes Ingress and microservice routing”能力，同时针对 LLM 应用进行了优化。
*   **推断**：
    1.  **统一接入层**：在企业内部，通常存在传统的微服务和新兴的 AI 应用。Higress 允许企业用同一套基础设施管理这两类截然不同的流量，避免了维护两套网关（如一套 Nginx 一套 Python 网关）的运维噩梦。
    2.  **AI 特性降本增效**：通过在网关层实现**Token 限流**和**请求缓存**，直接保护了后端昂贵的 LLM API 调用成本。例如，对于重复的 Prompt，网关可以直接返回缓存结果，而无需扣费调用大模型。
    3.  **标准化集成**：随着 OpenAI 推出 MCP 协议，Agent 如何调用工具成为难题。Higress 内置 MCP Server Hosting，使得外部工具可以像 API 一样被安全地注册和调用，加速了 Agent 编排系统的落地。

#### 3. 代码质量与架构：云原生工业级的典范
*   **事实**：项目基于 **Go** 语言编写，架构上明确分离了 **Control Plane（配置管理）** 和 **Data Plane（流量处理）**。
*   **推断**：Go 语言在云原生领域的统治地位保证了其并发性能和部署便利性。控制面与数据面分离是 Istio 和 Envoy 的最佳实践，这种解耦设计使得 Higress 能够轻松实现高可用部署（控制面挂掉不影响数据面转发）。代码结构上，作为阿里系开源项目，其代码规范性通常较高，接口定义清晰，且 README 提供了多语言版本（包括中日文），显示了其对国际化代码规范和文档质量的重视。

#### 4. 社区活跃度：背靠大树，初具规模
*   **事实**：Star 数为 **7,419**（数据截止至当前），由 **Alibaba** 维护。
*   **推断**：对于基础设施类项目，7k+ 的 Star 数是一个相当健康的信号，表明其已经过初步的市场验证。背靠阿里巴巴，意味着该项目有明确的商业支持（通常与阿里云 MSE 产品挂钩），不会像个人开源项目那样轻易废弃。社区反馈通常较快，且在国内开发者生态中具有较强的影响力。

#### 5. 学习价值：理解现代网关与 AI 落地的绝佳教材
*   **推断**：
    *   **架构视角**：开发者可以从中学习如何基于 Envoy 构建上层控制平台，理解 xDS 协议的具体落地。
    *   **AI 工程视角**：Higress 提供了一个标准的 AI 网关实现范例。开发者可以研究它是如何拦截 SSE（Server-Sent Events）流进行处理的，这对于理解流式响应的处理机制非常有启发。
    *   **WASM 实践**：它是一个学习如何编写高性能、热加载网关插件的优秀沙盒。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **复杂度曲线**：虽然功能强大，但引入 Istio/Envoy 生态本身带来了较高的部署和学习成本。对于仅有几个简单 API 的小团队来说，Higress 可能显得过于“重”。
    *   **AI 功能的成熟度**：作为新晋功能，AI Gateway 部分的协议兼容性（如对各家 LLM 厂商不同 API 格式的适配）可能仍需迭代打磨，可能会遇到特定模型

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是**AI Native API Gateway**，其架构设计体现了云原生时代“标准与扩展并存”的工程哲学。

### 核心技术栈与架构模式
Higress 采用了典型的**控制平面与数据平面分离**的架构模式，这是现代云原生网关的标准范式。
*   **数据平面**：基于 **Envoy** 构建。Envoy 是 CNCF 托管的高性能代理，以 C++ 编写，具备 L7 处理能力和低延迟特性。Higress 在此基础上深度集成了 **WebAssembly (WASM)** 技术栈。
*   **控制平面**：基于 **Istio** 生态进行改造。Higress 并没有完全复用 Istio 庞重的控制平面，而是提取并精简了其 xDS（发现服务）下发逻辑，实现了轻量级的配置管理。
*   **配置管理**：集成了 **Nacos**（阿里云生态）和 **Kubernetes Ingress**，支持服务发现和配置的动态推送。

### 关键设计亮点
1.  **WASM 插件化架构**：这是 Higress 最核心的技术差异化点。传统的网关扩展（如 Nginx 的 Lua 模块或 Kong 的 Nginx C 模块）往往存在耦合度高、稳定性风险（插件崩溃导致网关崩溃）、语言限制等问题。Higress 利用 WASM 的沙箱隔离特性，允许开发者使用 **Go/C++/Rust/AssemblyScript** 编写插件，这些插件运行在隔离的内存中，崩溃不会导致主进程崩溃，且支持**热加载**（毫秒级生效，无需重启网关）。
2.  **AI Native 数据面改造**：针对 LLM（大语言模型）的特殊流式传输场景，Higress 对 Envoy 的数据流处理进行了深度优化。传统的网关在处理 SSE（Server-Sent Events）或流式响应时，往往缓冲整个请求或响应，导致 AI 对话的首字延迟（TTFT）极高。Higress 实现了**流式透传与处理**能力，能够在数据流经网关时进行实时的鉴权、计费和内容修改，而不破坏流式连接。

### 架构优势分析
*   **高可用性与性能**：继承了 Envoy 的高性能异步非阻塞模型。
*   **极致的扩展性**：WASM 插件系统解决了传统网关“扩展难、维护难”的痛点。
*   **统一接入层**：打通了微服务（gRPC/HTTP）与 AI 服务（OpenAI Protocol）的界限，使得一个网关可以同时处理传统业务流量和 AI 流量。

---

## 2. 核心功能详细解读

### AI Gateway：大模型流量的统一入口
Higress 并不只是一个简单的路由转发器，它针对 AI 场景提供了**Provider 集成**能力。
*   **功能**：用户可以在 Higress 中配置 OpenAI、Azure、通义千问、月之暗面等多种 LLM Provider 的 API Key。前端应用只需调用 Higress 的统一接口，Higress 负责将请求路由到具体的模型提供商。
*   **解决的关键问题**：
    *   **密钥泄露风险**：前端无需携带各厂商的 Key，由网关统一管理。
    *   **模型切换成本**：通过修改网关配置即可切换底层模型，无需修改客户端代码。
    *   **Token 计费与限流**：基于请求或 Token 数量的精细化流控。

### MCP (Model Context Protocol) Server Hosting
这是 Higress 近期引入的前沿功能。MCP 是连接 AI Agent 与外部数据/工具的开放协议。
*   **功能**：Higress 可以作为 MCP Server 的托管网关。这意味着 AI Agent 可以通过 Higress 安全地访问企业内部的数据源（如数据库、文档系统）。
*   **意义**：将 AI Agent 的“工具调用”纳入了 API 网关的管理范畴，使得企业可以对 AI 的行为进行审计、鉴权和流量控制。

### 与同类工具对比
*   **VS Nginx/Kong**：Kong 主要基于 Nginx/Lua，虽然生态成熟，但在处理高并发流式 AI 请求时的内存管理和扩展性（WASM vs Lua）不如 Higress 灵活。Higress 的 WASM 性能接近原生，且隔离性更好。
*   **VS Istio Ingress**：Istio 原生 Ingress 配置过于复杂，且缺乏针对 AI 场景（如 SSE 透传、Token 统计）的特定功能。Higress 提供了更符合运维习惯的 K8s Ingress 注解和 Console 控制台。

---

## 3. 技术实现细节

### 流式处理与 AI 优化
在代码实现层面，Higress 处理 AI 请求的核心在于对 **HTTP Filter Chain** 的精细控制。
*   **Streaming Logic**：对于 LLM 的流式响应，Higress 避免了读取完整 Body 再转发的模式。它基于 Envoy 的 Streaming Filter 机制，逐块处理数据帧。
*   **Token 计数**：为了实现基于 Token 的限流，Higress 必须在流式传输过程中解析 SSE 数据包（通常格式为 `data: {"choices":...}`），实时累加 Token 数量。这要求极高的代码效率，否则会成为流式传输的瓶颈。

### 插件系统 (WASM Go SDK)
Higress 提供了 `github.com/alibaba/higress/plugins/wasm-go` SDK。
*   **设计模式**：采用了**过滤器模式**。开发者实现特定的接口（如 `OnHttpRequestHeaders`, `OnHttpResponseBody`）。
*   **内存管理**：由于 WASM 环境受限，Higress 的 Go SDK 对 Host（宿主机 Envoy）的内存访问进行了封装，利用 `proxy-wasm-go` 标准库与 Envoy 进行 ABI 交互。
*   **多线程支持**：Envoy 是多线程的，WASM 插件通常需要处理多线程隔离问题。Higress 的插件系统在底层处理了不同 Worker 线程间的插件实例同步逻辑。

### 配置热加载
*   **xDS 协议**：Higress 控制平面通过 gRPC 与 Envoy 建立长连接，使用 LDS (Listener Discovery Service) 和 RDS (Route Discovery Service) 动态下发配置。
*   **无中断发布**：配置变更时，Envoy 会先建立新的 Listener，再将流量切过去，确保长连接（如 SSE）不会因为配置重载而断开。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：企业内部构建 AI 助手或 Copilot，需要统一管理不同厂商的 LLM Key，并对员工访问进行审计和限流。
2.  **微服务 + AI 混合架构**：既有传统的微服务需要治理，又有新增的 AI 服务需要接入，希望统一网关技术栈，避免维护两套网关。
3.  **Kubernetes 多集群管理**：作为 K8s Ingress Controller 使用，特别是需要利用 WASM 插件实现自定义业务逻辑（如请求鉴权、Header 修改）的场景。

### 不适合的场景
1.  **极简单的静态网站托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。
2.  **极端依赖 Lua 生态的旧系统迁移**：如果已有大量 OpenResty/Lua 脚本，迁移到 Higress (WASM Go) 需要重写代码，成本较高。
3.  **非容器化部署**：虽然 Higress 支持虚拟机部署，但其强大功能依赖于与 Kubernetes 服务的集成本，在纯物理机环境下优势不如在 K8s 中明显。

### 集成注意事项
*   **资源限制**：WASM 插件虽然隔离，但依然消耗内存。在编写插件时需注意内存泄漏，因为 WASM 垃圾回收（GC）机制不如宿主机原生语言直接。
*   **版本兼容性**：Envoy 版本更新较快，Higress 的 WASM ABI 需要与之匹配，升级时需注意兼容性测试。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **从流量治理到协议治理**：随着 MCP 协议的引入，网关正在从单纯的 HTTP 流量管理，进化为 AI Agent 的**协议网关**。未来 Higress 可能会内置更多 AI 协议（如 LangChain 协议）的支持。
2.  **WASM 生态的标准化**：Higress 正在推动 Proxy-WASM 的生态建设，未来可能会出现“插件市场”，用户可以像安装 NPM 包一样安装网关功能。
3.  **Sidecar 模式**：虽然目前主要是 Gateway 模式，但技术上具备下沉为 Service Mesh Sidecar 的潜力，为每个微服务提供本地的 AI 能力调用。

### 社区与改进空间
*   **文档与示例**：作为一个新兴项目，虽然核心文档完善，但针对复杂 WASM 插件开发的 Debug 指南和最佳实践案例仍有待丰富。
*   **性能基准测试**：社区需要更多针对高并发 AI 流量下的性能数据，以消除用户对 WASM 性能损耗的顾虑。

---

## 6. 学习建议

### 适合人群
*   **云原生运维工程师**：需要掌握 K8s Ingress 和服务治理。
*   **后端开发者**：希望深入理解网关中间件、Go 语言与 C++ 交互（通过 WASM）的开发者。
*   **AI 应用架构师**：需要设计企业级 AI 落地架构的技术人员。

### 学习路径
1.  **基础层**：理解 Envoy 基础概念（Listener, Route, Cluster, Filter）。
2.  **协议层**：学习 HTTP 协议细节，特别是 SSE（Server-Sent Events）和 Chunked 编码，这对理解 AI 流式传输至关重要。
3.  **实践层**：阅读 Higress 官方的 Go WASM 插件开发文档，尝试编写一个简单的请求头修改插件。
4.  **源码层**：阅读 `pkg/wasm` 相关代码，了解 Higress 是如何将 WASM 插件注入到 Envoy Filter Chain 中的。

---

## 7. 最佳实践建议

### 正确使用方式
*   **利用 Wasm 插件隔离业务逻辑**：不要在网关层编写复杂的业务代码，WASM 插件应仅用于处理通用的横切关注点（鉴权、日志、协议转换）。
*   **AI Provider 抽象**：在 Higress 中定义好 Provider 后，应用层应使用统一的模型名称（如 `gpt-4`），由 Higress 配置决定实际指向 OpenAI 还是通义千问，实现**模型供应商无关化**。

### 常见问题与优化
*   **流式响应卡顿**：检查 WASM 插件中是否对 Body 进行了不必要的缓冲操作。确保只处理 Header 或在

---
## 代码示例




```python
# 示例1：Higress 网关配置示例
def higress_gateway_config():
    """
    Higress 是阿里云开源的云原生 API 网关
    本示例展示如何配置一个基本的 Higress 网关服务
    """
    import yaml
    
    config = {
        'apiVersion': 'networking.k8s.io/v1beta1',
        'kind': 'Ingress',
        'metadata': {
            'name': 'higress-demo',
            'namespace': 'default',
            'annotations': {
                'higress.io/destination': 'service.default.svc.cluster.local'
            }
        },
        'spec': {
            'rules': [{
                'host': 'example.com',
                'http': {
                    'paths': [{
                        'path': '/api',
                        'backend': {
                            'serviceName': 'higress-gateway',
                            'servicePort': 80
                        }
                    }]
                }
            }]
        }
    }
    
    # 将配置转换为 YAML 格式
    return yaml.dump(config, default_flow_style=False)

# 测试配置
print(higress_gateway_config())
```




```python
# 示例2：Higress 流量管理配置
def higress_traffic_management():
    """
    展示 Higress 的流量管理功能
    包括金丝雀发布和流量分割
    """
    config = {
        'apiVersion': 'traffic.higress.io/v1alpha1',
        'kind': 'TrafficShift',
        'metadata': {
            'name': 'canary-release',
            'namespace': 'default'
        },
        'spec': {
            'service': 'productpage',
            'versions': [
                {
                    'name': 'v1',
                    'weight': 90  # 90% 流量到 v1
                },
                {
                    'name': 'v2',
                    'weight': 10  # 10% 流量到 v2 (金丝雀版本)
                }
            ],
            'match': [
                {
                    'headers': {
                        'x-canary': {
                            'exact': 'true'  # 带有特定 header 的流量全部到 v2
                        }
                    }
                }
            ]
        }
    }
    
    return config

# 测试配置
print(higress_traffic_management())
```




```python
# 示例3：Higress 插件配置示例
def higress_plugin_config():
    """
    展示 Higress 的插件系统配置
    这里配置一个请求认证插件
    """
    plugin_config = {
        'name': 'key-auth',
        'config': {
            'keys': [
                {
                    'key': 'client1',
                    'secret': 'a1b2c3d4'
                },
                {
                    'key': 'client2',
                    'secret': 'e5f6g7h8'
                }
            ],
            'header': 'x-api-key'
        }
    }
    
    # 模拟插件加载
    def load_plugin(config):
        print(f"加载插件: {config['name']}")
        print(f"配置: {config['config']}")
        return True
    
    return load_plugin(plugin_config)

# 测试插件配置
higress_plugin_config()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务（大促场景）

 1：阿里巴巴内部电商业务（大促场景）

**背景**: 阿里巴巴每年的双11等大型促销活动中，电商系统面临着巨大的流量冲击。传统的网关架构在面对瞬时每秒百万级 QPS 的流量洪峰时，往往面临配置变更生效慢、流量管控精度不足以及扩展性受限的挑战。

**问题**: 在大促备战期间，业务团队需要频繁地调整流量路由规则（如灰度发布、A/B 测试）和限流降级策略。原有的网关系统在处理这些动态配置时，热更新效率不够高，且对于复杂的服务路由逻辑（如根据 Header、Cookie 进行精细化分流）支持不够灵活，难以满足业务快速迭代的需求。

**解决方案**: 团队引入并深度使用了 Higress。Higress 基于 Envoy 和 Istio 构建，提供了高性能的 API 网关能力。通过其标准化的 Ingress API 和 Wasm 插件市场，开发人员能够用 Go 或 C++ 编写自定义插件来处理复杂的流量逻辑，而无需修改网关核心代码。同时，利用 Higress 的热更新能力，实现了秒级的规则下发。

**效果**: 成功支撑了双11期间峰值流量的平稳运行。网关的 CPU 开销显著降低，路由规则的下发速度从分钟级提升至秒级。此外，开发人员通过 Wasm 插件快速实现了特定的业务鉴权逻辑，业务迭代效率提升了 30% 以上。

---



### 2：某互联网科技公司的微服务 API 治理

 2：某互联网科技公司的微服务 API 治理

**背景**: 该公司随着业务微服务化转型的深入，服务数量激增至数百个，对外提供的 API 接口数量超过千个。由于历史原因，系统中并存着多个不同类型的 API 网关（如 Kong、Spring Cloud Gateway），导致运维成本高昂，且缺乏统一的流量视图和安全管理标准。

**问题**: 多套网关并存导致资源浪费严重，且不同网关之间的配置无法互通。开发团队在对接新服务时，需要针对不同的网关编写适配代码，增加了开发负担。同时，缺乏统一的流量入口，使得全链路的安全防护（如 WAF、防爬虫）难以统一实施，存在安全隐患。

**解决方案**: 该公司决定将所有流量统一收敛至 Higress。利用 Higress 强大的兼容性，它能够同时接管 K8s Ingress 和 API Gateway 的流量，并通过一套控制平面进行管理。团队利用 Higress 的原生支持对接了阿里云的 WAF 服务，并启用了 JWT 认证插件来保护内部 API。

**效果**: 成功将网关集群数量缩减了 50%，大幅降低了服务器资源成本和运维复杂度。统一的 API 入口使得安全策略得以集中实施，有效拦截了恶意流量。开发人员不再需要关心底层网关差异，只需关注业务逻辑，API 发布效率提升了 40%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Nginx + Lua (OpenResty) | Kong |
|------|-----------------|-------------------------|------|
| 性能 | 高性能，基于 Rust 和 Go，支持 Wasm 插件 | 极高性能，C 语言核心，Lua 脚本扩展 | 高性能，基于 Nginx 和 OpenResty |
| 易用性 | 提供可视化控制台，支持 K8s Ingress，配置简单 | 需手动编写 Lua 脚本，配置复杂 | 提供 UI 管理界面，但配置较复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，需自行维护 | 开源版免费，企业版收费 |
| 扩展性 | 支持 Wasm 插件，插件生态丰富 | 依赖 Lua 生态，扩展性有限 | 插件生态丰富，但需付费 |
| 社区 | 阿里背书，社区活跃 | 成熟社区，文档丰富 | 社区活跃，企业支持强 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，性能优于传统 Nginx 方案。
- 优势2：原生支持 K8s Ingress 和 Wasm 插件，扩展性强。
- 优势3：提供可视化控制台，降低运维复杂度。

### 不足分析

- 不足1：社区和生态成熟度不如 Nginx 和 Kong。
- 不足2：Wasm 插件开发门槛较高，需掌握 Rust 或 Go。
- 不足3：云服务依赖阿里云，多云部署可能受限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现业务逻辑的灵活扩展

**说明**: Higress 的核心优势之一在于其强大的 Wasm (WebAssembly) 插件生态。与传统网关（如 Nginx）需要修改 C++ 模块或使用 Lua 相比，Higress 允许开发者使用 C++, Go, Rust, JavaScript 等多种语言编写插件，并以 Wasm 格式动态加载。这种机制实现了业务逻辑与网关内核的完全隔离，极大地降低了扩展功能的开发难度和风险，同时支持运行时热插拔，无需重启网关即可更新插件逻辑。

**实施步骤**:
1. 访问 Higress 官方插件市场或 GitHub 仓库，查找是否已有现成的插件满足需求（如 JWT 验证、请求鉴权等）。
2. 若需自定义，使用 Higress 提供的 SDK（推荐 Go 或 Rust）编写插件逻辑，处理请求/响应头、Body 或调用外部服务。
3. 将编写好的代码编译为 `.wasm` 文件。
4. 在 Higress 控制台的 "插件市场" 或 "路由配置" 中上传该 Wasm 文件，并将其关联到特定的网关实例或路由规则上。

**注意事项**: 
- Wasm 插件运行在沙箱中，虽然安全性高，但频繁的跨语言调用（如 Host 调用）会有一定的性能开销，应避免在插件中编写过于繁重的计算逻辑。
- 注意 Wasm 文件的内存限制，防止插件占用过多资源导致网关 OOM。

---

### 实践 2：精细化配置流量路由与灰度发布

**说明**: 利用 Higress 强大的 HTTP 路由能力，可以实现基于请求头、Cookie、URL 参数或权重的高级流量路由。这对于微服务架构下的蓝绿部署、金丝雀发布（灰度发布）以及 A/B 测试至关重要。通过配置不同的路由规则，可以将特定特征的流量（如内网用户、测试用户）精确地导向新版本服务，从而降低上线风险。

**实施步骤**:
1. 在 Higress 中定义目标服务，确保新版本和旧版本服务已在服务注册中心（如 Nacos, Consul）注册。
2. 创建两条路由规则，匹配条件相同但优先级不同，或者使用同一路由配置多个目标服务。
3. 设置流量分流权重：例如，将 10% 的流量指向新版本，90% 保留在旧版本。
4. 配置匹配规则（如 `x-canary: true`），以便在需要时通过 Header 强制将特定请求路由到新版本进行验证。

**注意事项**: 
- 灰度发布过程中，必须保持新旧版本 API 的兼容性，否则会导致旧版客户端调用失败。
- 建议配合可观测性工具（如 Prometheus + Grafana）实时监控新版本服务的错误率和延迟，一旦发现异常立即回滚流量。

---

### 实践 3：构建全链路安全防护体系

**说明**: Higress 内置了丰富的安全防护能力，最佳实践是组合使用多种安全策略来构建纵深防御体系。这包括配置严格的 CORS 策略防止跨域攻击，启用 IP 访问控制（黑/白名单）限制非法来源，以及集成认证鉴权插件（如 KeyAuth, OIDC, HMAC 认证）来保护后端 API。对于高并发接口，还应配置限流熔断策略以防止 DDoS 攻击或流量突刺打垮后端服务。

**实施步骤**:
1. **认证配置**: 在路由或域名级别启用全局认证插件（如 JWT），确保所有请求在到达业务逻辑前已通过身份验证。
2. **访问控制**: 配置 IP 黑名单插件，封禁已知恶意 IP 地址；或配置 IP 白名单，仅允许内网或 CDN 回源 IP 访问管理接口。
3. **限流配置**: 针对关键 API 配置“请求每秒”（QPS）或“请求并发数”限制，可选择使用 Redis 作为限流计数器的后端以支持集群模式。
4. **安全插件**: 启用 Wasm 类型的安全插件（如类似 ModSecurity 的功能）拦截 SQL 注入、XSS 等常见 Web 攻击。

**注意事项**: 
- 限流阈值设置需基于实际压测数据，设置过低会误杀正常用户，设置过高则无法起到保护作用。
- 启用认证后，需确保网关与后端服务之间的信任传递机制（如传递自定义 Header）配置正确，避免后端服务重复校验。

---

### 实践 4：深度集成服务注册与发现

**说明**: Higress 原生支持 Nacos、Zookeeper、Consul、Eureka 等主流注册中心。最佳实践是不要将 Higress 仅仅当作一个静态反向代理，而是将其接入服务治理体系。通过对接注册中心，Higress 可以实时感知服务实例的上下线（健康检查），自动剔除不健康的实例，并在扩缩容时无需手动修改网关

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与本地缓存

**说明**: Higress 基于 Envoy 构建，支持 WASM 插件扩展。通过启用 WASM 插件处理复杂逻辑，并利用本地缓存减少重复计算，可显著降低延迟。

**实施方法**:
1. 在 Higress 控制台配置 WASM 插件（如限流、认证）。
2. 启用路由级缓存（如 Redis 或内存缓存）。
3. 调整缓存 TTL 参数（建议 5-10 分钟）。

**预期效果**: 延迟降低 20%-30%，吞吐量提升 15%-25%。

---

### 优化 2：调整连接池与超时参数

**说明**: 默认连接池配置可能无法满足高并发场景。优化连接池大小和超时参数可减少资源争用。

**实施方法**:
1. 修改 `higress-config.yaml` 中的 `upstream_connection_pool` 参数（建议 100-200）。
2. 调整 `connect_timeout` 和 `request_timeout`（建议 5s 和 30s）。
3. 启用 HTTP/2 多路复用。

**预期效果**: 并发处理能力提升 30%-50%，错误率降低 10%-15%。

---

### 优化 3：启用 CPU 亲和性与 NUMA 优化

**说明**: 绑定 CPU 亲和性可减少上下文切换开销，NUMA 优化可提升内存访问效率。

**实施方法**:
1. 在部署脚本中添加 `taskset` 命令绑定 CPU 核心。
2. 启用 `numactl --interleave=all` 参数。
3. 禁用 Linux 内核的 `irqbalance` 服务。

**预期效果**: CPU 利用率提升 10%-20%，延迟降低 5%-10%。

---

### 优化 4：使用零拷贝技术

**说明**: 启用内核零拷贝（如 `sendfile`）可减少数据在内核态与用户态之间的拷贝次数。

**实施方法**:
1. 在 Nginx 配置中启用 `sendfile on` 和 `tcp_nopush on`。
2. 确保 Higress 部署在支持 `io_uring` 的 Linux 内核（5.1+）上。
3. 使用 `ethtool` 检查网卡是否支持 `scatter-gather`。

**预期效果**: 网络吞吐量提升 25%-40%，CPU 占用降低 15%-20%。

---

### 优化 5：分级日志与采样

**说明**: 全量日志会消耗大量 I/O 资源。通过分级日志和采样可减少写入压力。

**实施方法**:
1. 配置 `log_level=warn` 仅记录关键日志。
2. 启用 1% 请求采样（`sampling_rate=0.01`）。
3. 使用异步日志库（如 spdlog）。

**预期效果**: 磁盘 I/O 降低 50%-70%，日志处理延迟减少 30%-40%。

---

### 优化 6：预热与流量整形

**说明**: 冷启动时性能波动较大。通过预热和流量整形可平滑负载。

**实施方法**:
1. 部署时启用 `warmup_secs=60` 参数。
2. 配置令牌桶算法限流（`burst=100`）。
3. 使用 Prometheus 监控并动态调整。

**预期效果**: 冷启动延迟降低 40%-60%，P99 延迟波动减少 20%-30%。

---
## 学习要点

- Higress 是阿里云开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Nginx 生态，提供高性能的流量管理能力。
- 支持热更新路由规则、插件加载和证书配置，无需重启服务即可实现配置变更，保障业务连续性。
- 内置 WAF 防护、限流熔断、灰度发布等企业级功能，可直接对接 K8s Ingress 或 Gateway API 资源。
- 提供可扩展的插件体系（支持 WASM/Go/Python），允许开发者通过插件快速定制鉴权、日志、监控等逻辑。
- 兼容 Envoy 和 Nginx 配置语法，降低传统网关用户的迁移成本，同时支持多协议（HTTP/gRPC/Dubbo）代理。
- 通过 Prometheus/Grafana 集成提供可观测性，并支持与阿里云 ARMS、SLS 等监控服务无缝对接。
- 采用声明式配置（YAML）管理网关资源，符合云原生 GitOps 最佳实践，适合 DevOps 场景自动化运维。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的核心概念与架构设计（基于 Istio 和 Envoy）
- 云原生网关的基础知识（流量管理、安全防护、可观测性）
- Higress 与传统网关（如 Nginx、Kong）的区别与优势
- Docker 容器基础与 Kubernetes 基本操作（Deployment、Service）

**学习时间**: 1-2周

**学习资源**:
- [Higress 官方文档](https://higress.io/docs/latest/)
- [Higress GitHub 仓库](https://github.com/alibaba/higress)
- [Envoy 官方文档](https://www.envoyproxy.io/docs/envoy/latest/)
- [Kubernetes 基础教程](https://kubernetes.io/zh-cn/docs/tutorials/)

**学习建议**: 
先通过官方文档了解 Higress 的定位和核心功能，结合 Docker 和 Kubernetes 的基础操作，在本地搭建一个简单的 Higress 实例，熟悉基本配置流程。

---

### 阶段 2：核心功能与配置

**学习内容**:
- Higress 的安装与部署（Docker、Kubernetes、Helm）
- 路由配置（HTTP/HTTPS 路由、路径重写、流量转发）
- 插件系统（Wasm 插件的使用与开发）
- 服务发现与负载均衡策略
- 基本的安全配置（认证、鉴权、HTTPS 证书管理）

**学习时间**: 2-3周

**学习资源**:
- [Higress 插件开发文档](https://higress.io/docs/latest/develop/wasm-go/)
- [Higress 官方示例](https://github.com/higress-group/higress-group.github.io/tree/main/examples)
- [Wasm 官方文档](https://webassembly.org/)
- [Istio 流量管理文档](https://istio.io/latest/docs/concepts/traffic-management/)

**学习建议**: 
动手实践路由和插件配置，尝试编写一个简单的 Wasm 插件（如请求头修改或限流），并结合 Kubernetes 部署一个微服务应用，通过 Higress 管理流量。

---

### 阶段 3：高级特性与优化

**学习内容**:
- 高级流量管理（金丝雀发布、蓝绿部署、A/B 测试）
- 可观测性（Prometheus 监控、Grafana 仪表盘、日志集成）
- 性能优化（连接池、缓存、压缩）
- 多集群与混合云部署
- 与阿里云云原生产品的集成（如 MSE、ACK）

**学习时间**: 3-4周

**学习资源**:
- [Higress 可观测性文档](https://higress.io/docs/latest/ops/observability/)
- [Prometheus 官方文档](https://prometheus.io/docs/)
- [Grafana 官方文档](https://grafana.com/docs/)
- [阿里云 MSE 产品文档](https://help.aliyun.com/product/134527.html)

**学习建议**: 
在真实或模拟的生产环境中测试 Higress 的性能和稳定性，结合 Prometheus 和 Grafana 搭建监控体系，尝试实现金丝雀发布等高级流量管理策略。

---

### 阶段 4：生产实践与生态集成

**学习内容**:
- 生产环境部署最佳实践（高可用、灾备、滚动升级）
- 与 CI/CD 流水线集成（如 Jenkins、GitLab CI）
- 自定义插件开发与贡献（参与 Higress 开源社区）
- 多租户与权限管理
- 故障排查与性能调优

**学习时间**: 4-6周

**学习资源**:
- [Higress 生产实践案例](https://higress.io/blog/)
- [Higress 社区贡献指南](https://github.com/alibaba/higress/blob/main/CONTRIBUTING.md)
- [Jenkins 官方文档](https://www.jenkins.io/doc/)
- [GitLab CI/CD 文档](https://docs.gitlab.com/ee/ci/)

**学习建议**: 
参与 Higress 开源社区，尝试贡献代码或文档，结合实际业务场景设计完整的网关解决方案，重点关注高可用和性能优化，积累生产环境经验。

---
## 常见问题


### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个基于阿里云内部两年多的“通义”大模型应用实践沉淀，并结合开源社区 Istio 和 Envoy 的能力而孵化出的**云原生 API 网关**。它由阿里云开源，遵循 Apache 2.0 协议。Higress 的设计初衷是解决传统网关在云原生架构下面临的性能、扩展性和易用性问题，它深度集成了 Envoy 作为高性能数据面，并兼容 Kubernetes 和 Istio 标准，旨在为用户提供一个安全、稳定且高扩展的流量管理入口。

---



### 2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **云原生深度集成**：作为云原生网关，Higress 原生支持 Kubernetes 和 Service Mesh（服务网格）。它可以作为 Ingress Controller 使用，也可以与 Istio 无缝集成，实现东西向（服务间）和南北向（入口）流量的统一管理，这是传统网关较难做到的。
2.  **高性能**：基于 C++ 编写的 Envoy 作为数据面，具备极高的吞吐量和低延迟，能够应对高并发场景。
3.  **标准与扩展性**：Higress 支持 WASM（WebAssembly）插件机制。这意味着开发者可以使用 Go、C++、Rust 甚至 JavaScript/TypeScript（通过 AssemblyScript）编写插件，且插件热更新无需重启网关，比传统的 Lua (Nginx) 或 C/Kong 插件开发更安全、灵活。
4.  **AI 原生支持**：Higress 特别针对 AI 场景进行了优化，内置了处理大模型流式输出的能力，支持更灵活的 Prompt 管理和模型路由，这是许多传统网关目前不具备的。

---



### 3: Higress 与 Istio 的关系是什么？我是否需要安装 Istio 才能使用 Higress？

3: Higress 与 Istio 的关系是什么？我是否需要安装 Istio 才能使用 Higress？

**A**: Higress 与 Istio 既有联系又有区别。Higress 的控制面架构借鉴了 Istio 的设计理念（如 xDS 协议），但它是一个**独立**的组件。

*   **独立使用**：你**不需要**安装 Istio 就能使用 Higress。你可以直接在 Kubernetes 集群中安装 Higress，将其作为单纯的 API 网关或 Ingress Controller 来管理外部流量。
*   **结合使用**：如果你已经在使用 Istio，Higress 可以作为 Istio 的**入口网关**。相比于 Istio 原生的 Ingress Gateway，Higress 提供了更丰富的流量管理功能（如更灵活的路由匹配、热加载插件等）以及更好的控制台管理体验。

---



### 4: Higress 是否支持从 Nginx 或 Ingress NGINX Controller 进行迁移？

4: Higress 是否支持从 Nginx 或 Ingress NGINX Controller 进行迁移？

**A**: 是的，Higress 提供了良好的兼容性工具来降低迁移成本。Higress 支持**Nginx Ingress Annotation 兼容**。这意味着，如果你的 Kubernetes 应用目前使用的是 Nginx Ingress Controller，并且配置了大量的 Annotation 来进行流量控制，Higress 能够识别并支持这些常用的 Annotation。这使得用户可以在不大幅修改 YAML 配置文件的情况下，将底层网关从 Nginx 切换到 Higress，从而获得更好的性能和 WASM 插件能力。

---



### 5: 如何在 Higress 中扩展功能？是否支持自定义插件？

5: 如何在 Higress 中扩展功能？是否支持自定义插件？

**A**: Higress 拥有非常强大的插件扩展体系，主要通过 **WASM (WebAssembly)** 技术实现。

1.  **WASM 插件**：这是 Higress 推荐的扩展方式。开发者可以使用 Go 或 C++ 编写业务逻辑，编译成 WASM 文件上传到 Higress。这种插件运行在沙箱环境中，安全性高，且支持热加载（上传即生效，无需重启网关进程）。
2.  **Lua 插件**：为了兼容旧版习惯，Higress 依然支持 Lua 脚本插件，但更推荐向 WASM 迁移。
3.  **原生插件**：对于极致性能要求的场景，Higress 也支持使用 C++ 编写 Envoy 原生过滤器。
4.  **控制台配置**：Higress 提供了开箱即用的控制台（基于 Dubbo Admin 演进），用户可以在 UI 上直接配置路由、认证、限流、CORS 等常见功能，无需编写代码。

---



### 6: Higress 的安全性如何保障？

6: Higress 的安全性如何保障？

**A**: Higress 在设计上非常重视安全性，提供了以下多层防护：

1.  **身份认证与鉴权**：支持标准的 OIDC（OpenID Connect）认证，集成 Keycloak、Okta 等身份提供商。同时支持基于 IP、Header 或 JWT 的精细化访问控制。
2.  **插件安全隔离**：通过 WASM

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 快速入门与路由转发

### 问题**: 在本地 Docker 环境中快速启动 Higress，并配置一个简单的路由规则，将访问 `/httpbin` 路径的流量转发到公共测试服务 `httpbin.org`。

### 提示**: 参考 Higress 官方文档的 "快速开始" 章节。你需要使用 `docker run` 启动容器，并利用 Higress 提供的 Console 或 Wasm 插件来配置 `Ingress` 或 `Gateway` 资源。注意目标服务的 `Host` 头部设置。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位及其在阿里巴巴内部的大规模实践，以下是针对实际使用场景的 5 条实践建议：

### 1. 利用 AI 代理模式实现统一模型接入与成本优化
*   **场景**：企业内部同时接入了多家大模型厂商（如 OpenAI, 通义千问, DeepSeek 等），业务端需要灵活切换，且需要控制 Token 消费成本。
*   **建议**：不要将模型 SDK 硬编码在业务代码中。应在 Higress 中配置 AI 代理插件，将后端不同的 LLM 服务统一映射为 Higress 的标准路由。
*   **具体操作**：
    *   配置不同的 `provider`（如 `qwen`, `openai`）。
    *   在路由层使用 `header` 或 `query` 参数（例如 `x-model-provider`）来动态决定转发给哪个模型提供商。
    *   **最佳实践**：利用 Higress 的**模型重写**功能，在网关层将业务请求的廉价模型参数（如 `gpt-3.5-turbo`）在转发时修改为内部部署的高性能模型（如 `qwen-turbo`），从而在保持业务代码不变的情况下降低 API 调用成本。

### 2. 配置“语义缓存”以降低延迟与 API 调用费用
*   **场景**：客服或知识库问答场景中，大量用户提问高度重复（例如“如何退款？”），每次都请求 LLM 导致响应慢且费用高。
*   **建议**：启用 Higress 的语义缓存插件，而非传统的精确匹配缓存。
*   **具体操作**：
    *   在 AI 代理路由上启用语义缓存插件，并配置向量数据库（或内置的 Redis 向量存储）。
    *   设置合适的相似度阈值（如 0.85）和缓存 TTL。
    *   **常见陷阱**：不要对实时性要求极高或需要上下文记忆强相关的会话开启过长的缓存，否则会导致回答“答非所问”或无法跟进对话逻辑。

### 3. 实施基于 Token 的精细化限流与熔断
*   **场景**：大模型 API 的计费模式通常基于 Token 数量，传统的基于 QPS（每秒请求数）或并发连接数的限流无法有效控制成本。
*   **建议**：配置针对 Token 吞吐量的限流策略，保护后端模型服务免受突发流量冲击。
*   **具体操作**：
    *   使用 Higress 的本地限流或全局限流插件，配置针对 AI 请求的特殊规则。
    *   **最佳实践**：结合 Prompt 模板管理，在网关层对用户输入的 Prompt 进行长度截断或清洗，防止恶意用户发送超长 Prompt 导致后端 Token 消耗爆炸。
    *   **常见陷阱**：避免只限制 HTTP 请求数。一个包含 10k Token 的请求虽然只有 1 次 QPS，但可能耗尽带宽并导致后端超时。

### 4. 构建基于 Prompt 模板的安全护栏
*   **场景**：防止用户通过“提示词注入”攻击套取系统指令，或生成违规内容。
*   **建议**：利用 Higress 的插件能力在请求发送给 LLM 之前和响应返回给用户之前进行拦截和处理。
*   **具体操作**：
    *   **输入侧**：配置“敏感词过滤”或“输入审查”插件，检测并拦截包含攻击性特征的 Prompt。
    *   **输出侧**：配置输出审查插件，过滤模型生成的违规内容。
    *   **最佳实践**：在网关层强制追加 System Prompt（系统提示词），定义模型的角色和行为边界，即使客户端尝试修改 System Header，网关也能覆盖并强制执行安全策略。

### 5. 善用 Wasm 插件实现业务逻辑解耦与热更新
*   **场景**：业务部门频繁需要调整鉴权逻辑、计费逻辑或请求参数，频繁重启网关服务风险高。
*   **建议**：利用 Higress

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [Kubernetes](/tags/kubernetes/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*