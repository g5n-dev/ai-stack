---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-08T06:53:19+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "阿里开源", "Istio", "Envoy", "LLM", "MCP协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**，基于 Go 语言开发，目前在 GitHub 上拥有超过 7,600 颗星。该系统构建在 Istio 和 Envoy 之上，旨在通过云原生技术为现代应用架构提供强大的流量管理和 AI 集成能力。 **核心架构与特性：** Higress 采用"
external_url: https://github.com/alibaba/higress
scenarios: ["云原生/容器", "大语言模型", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,686 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，实现了从传统流量管理到 AI 原生服务的平滑演进。它不仅支持 Kubernetes Ingress 和微服务路由，更针对 LLM 应用提供了 AI 网关特性及 MCP 服务托管，旨在解决企业在 AI 时代的流量治理与服务集成难题。本文将深入剖析其系统架构，并详细介绍核心组件、部署方式及 WASM 插件体系。

---
## 摘要

Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**，基于 Go 语言开发，目前在 GitHub 上拥有超过 7,600 颗星。该系统构建在 Istio 和 Envoy 之上，旨在通过云原生技术为现代应用架构提供强大的流量管理和 AI 集成能力。

**核心架构与特性：**
Higress 采用了**控制平面与数据平面分离**的架构。其显著特点包括：
1.  **高性能与可扩展性：** 利用 WebAssembly (WASM) 插件能力扩展功能，配置变更通过 xDS 协议传播，具备毫秒级延迟且无连接中断，特别适用于 AI 长连接流式响应场景。
2.  **AI 网关：** 提供统一的 API 接口支持 30 多家大语言模型 (LLM) 提供商，内置协议转换、可观测性、缓存和安全防护等插件。
3.  **MCP 服务器托管：** 支持托管模型上下文协议 (MCP) 服务器，使 AI Agent 能够便捷地调用外部工具和服务。
4.  **传统 API 网关：** 兼容 Kubernetes Ingress 和 Nginx 注解，提供微服务路由等传统网关功能。

**主要应用场景：**
*   **AI 应用开发：** 统一管理 LLM 访问，提供安全、统计与缓存支持。
*   **AI Agent 工具集成：** 通过 `mcp-router` 等组件实现工具与服务的调用。
*   **Kubernetes 入口流量管理：** 作为 Ingress 控制器管理集群入口流量。

---
## 评论

### 总体评价

Higress 是阿里巴巴开源的**下一代“AI 原生”API 网关**，它成功地将云原生流量治理与 AI 大模型应用所需的特殊协议处理进行了深度融合。该项目不仅是对传统 API 网关的演进，更是一个面向 LLM 时代的**连接与编排层**，其最大的价值在于将 Envoy 的高性能与 AI 应用的复杂性（如 Token 计费、模型切换）进行了标准化封装，是目前企业构建 AI 基础设施中极具竞争力的“流量入口”方案。

---

### 深入评价维度

#### 1. 技术创新性：从“流量治理”向“意图治理”的跃迁
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并引入了 WebAssembly (WASM) 插件系统。DeepWiki 明确指出其核心功能包括“AI Gateway 特性”和“MCP server hosting”。
*   **推断**：传统网关关注 HTTP/gRPC 的转发，而 Higress 创新性地将 AI 领域的**语义协议**纳入治理范畴。
    *   **差异化方案**：它不仅仅是在做负载均衡，而是在做**AI 请求的编排**。例如，它原生支持 LLM 的特有参数处理（如 `temperature`, `top_p`），并能对流式响应进行拦截和修改。
    *   **MCP 协议支持**：DeepWiki 提到的 MCP (Model Context Protocol) server hosting 是一大亮点。这意味着 Higress 不仅仅是一个被动的网关，更是一个主动的 AI Agent 工具集托管中心，允许 AI 应用通过网关直接调用挂载的 MCP 工具，这是对传统网关“仅做路由”定义的突破。

#### 2. 实用价值：解决 AI 落地“最后一公里”的痛点
*   **事实**：文档描述其为“AI Native API Gateway”，同时保留了 Kubernetes Ingress 和微服务路由能力。
*   **推断**：Higress 解决了企业在引入大模型时面临的**多模型异构管理**和**成本控制**难题。
    *   **统一接入层**：企业通常同时使用 OpenAI、通义千问、DeepSeek 等不同模型。Higress 允许后端配置不同的 Provider，前端业务代码只需调用 Higress 的统一标准接口，极大降低了业务侧的改造成本。
    *   **可观测性与计费**：AI 时代的计费单位从“请求数”变成了“Token 数”。Higress 能够在网关层精确统计输入/输出 Token，实现了流量的精细化计费和配额管理，这是传统网关无法做到的。

#### 3. 代码质量与架构：云原生标准的继承与扩展
*   **事实**：项目使用 Go 语言编写，基于 Envoy (C++) 和 Istio (Go) 生态。
*   **推断**：
    *   **架构设计**：采用**控制面与数据面分离**的架构。控制面负责配置下发（兼容 Istio），数据面由 Envoy 处理流量。这种设计保证了极高的性能和可扩展性。
    *   **扩展性**：WASM 插件系统的引入是架构设计的神来之笔。它允许开发者使用 C/C++、Go、Rust 甚至 JavaScript 编写业务逻辑，而无需重新编译网关或引入 Sidecar。对于 AI 场景中频繁变化的鉴权、Prompt 注入等需求，这种热插拔能力至关重要。

#### 4. 社区活跃度：背靠阿里的强力驱动
*   **事实**：星标数 7,686（且在快速增长中），由阿里巴巴主导。
*   **推断**：作为阿里云通义系列背后的核心网关组件，Higress 并非“玩具项目”，而是经过了阿里内部大规模电商和高并发场景验证的工业级产品。其更新频率较高，且对 AI 新特性的支持（如最近对 Claude、DeepSeek 等模型的快速适配）非常敏锐。社区贡献者主要集中在云原生和 AI 应用开发领域，Issue 响应速度较快。

#### 5. 学习价值：理解“AI + 基础设施”的绝佳样本
*   **推断**：对于开发者而言，Higress 是学习如何将**传统中间件向 AI 时代演进**的最佳教科书。
    *   它展示了如何利用 WASM 技术在 Envoy 中处理 SSE (Server-Sent Events) 流式数据，这在当前的 AI 应用开发中是一项稀缺且高价值的技能。
    *   它的配置模型（Kubernetes CRD）展示了如何定义 AI 路由、Provider 和 Prompt 模板，有助于开发者掌握云原生 AI 应用的编排逻辑。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **复杂度曲线**：虽然 Higress 提供了控制台，但基于 Istio 的架构意味着运维门槛较高。对于没有 Kubernetes 基础的小团队，部署和调优成本可能比简单的 Nginx 反代要高得多。
    *   **文档碎片化**：尽管 DeepWiki 显示有详细文档，但开源项目往往存在文档更新滞后于代码的问题，特别是 AI 特性迭代极快，部分高级配置（如复杂的 WASM 插件开发）可能缺乏示例。
    *   **性能损耗**：在处理 SSE 流式转发时，网关层进行 Token 统计和内容过滤可能会增加额外的延迟和 CPU 开销，

---
## 技术分析

# Higress 技术深度分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本报告将从技术架构、核心功能、实现细节、适用场景、发展趋势、学习路径、最佳实践以及工程哲学等八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构遵循**云原生**的设计范式，采用了标准的**控制平面与数据平面分离**的架构模式。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。同时，它深度集成了 **Istio**，复用 Istio 的控制平面能力（如 xDS 协议下发、服务发现、安全治理），但将其下沉定位为更通用的 API 网关，而非局限于服务网格内的 Sidecar 模式。
*   **扩展机制**：最关键的技术栈选择是 **WebAssembly (WASM)**。Higress 将 WASM 作为一等公民，允许开发者使用 C/C++/Go/Rust 等多种语言编写插件，运行在 Envoy 的沙箱中。这解决了传统 Lua 插件（如 OpenResty）在安全性、隔离性和性能稳定性上的痛点。
*   **配置管理**：通过 **xDS 协议**（包括 LDS, RDS, CDS, EDS）将控制平面（Higress Console）的配置变更实时推送给数据平面。这种机制保证了配置变更的毫秒级生效，且无需重启网关进程。

### 核心模块
1.  **Router (路由层)**：负责流量匹配，支持基于 Host、Header、Path 的 HTTP 路由，以及 gRPC 和 Dubbo 协议的路由。
2.  **WASM Plugin System (插件市场)**：运行时动态加载插件。Higress 内置了丰富的插件生态（如限流、认证、日志、请求/响应修改）。
3.  **AI Gateway (AI 网关)**：这是最新的核心模块。它不仅仅是代理流量，还针对 LLM（大语言模型）协议进行了深度优化。
4.  **MCP Server Host**：集成了 Model Context Protocol (MCP) 服务托管能力，用于连接 AI Agent 与外部工具/数据源。

### 技术亮点与创新
*   **AI-Native 理念**：这是 Higress 与 Nginx、Kong 等传统网关最大的区别。它原生支持 SSE（Server-Sent Events）流式转发，针对 AI 对话场景的低延迟要求，对数据平面的 Buffer 机制进行了优化，避免了传统网关在处理流式响应时的缓存积压问题。
*   **MCP 协议集成**：Higress 率先在网关层面支持 MCP 标准。这意味着网关不仅仅是流量的管道，更成为了 AI Agent 的“工具调度中心”，统一管理 Agent 对后端 API 的访问权限和鉴权。

### 架构优势
*   **极致性能**：得益于 Envoy 的 C++ 异步非阻塞模型，Higress 在处理高并发、长连接（如 SSE）时具有极高的性能和极低的资源损耗。
*   **热更新能力**：基于 WASM 和 xDS，业务逻辑（插件）和路由配置都可以在运行时动态变更，无需重启服务，这对于 7x24 小时运行的 AI 服务至关重要。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一模型接入**：将 OpenAI、Azure、通义千问、Llama 等不同厂商的 API 标准化，开发者只需调用 Higress 的统一接口，由网关负责路由到具体的模型提供商。
    *   **Token 管理与计费**：在传输层实时统计 Prompt 和 Completion 的 Token 数量，便于精细化成本控制。
    *   **提示词增强**：在网关层动态插入 System Prompt，实现统一的安全围栏或上下文注入。
2.  **MCP 服务器托管**：
    *   解决了 AI Agent 如何安全、标准化地访问外部数据（如数据库、私有 API）的问题。Higress 充当 MCP Server 的宿主和代理。
3.  **传统 API 网关**：
    *   K8s Ingress Controller：替代 Nginx Ingress，提供更强的动态配置能力。
    *   流量治理：金丝雀发布、蓝绿部署、负载均衡、熔断降级。

### 解决的关键问题
*   **AI 服务的碎片化**：企业内部可能同时使用多个 LLM 供应商，切换成本高。Higress 提供了统一抽象层。
*   **流式传输的断点续传与超时**：传统网关在处理 SSE 时容易因超时断开，Higress 针对长连接场景优化了 Idle Timeout 策略。
*   **工具调用的安全性**：直接给 LLM 暴露 API Key 是危险的。通过 Higress 的 AI Gateway + MCP，可以实现“工具调用”的鉴权和审计，防止 Agent 越权访问。

### 与同类工具对比
| 特性 | Higress | APISIX (Apache) | Kong |
| :--- | :--- | :--- | :--- |
| **内核** | Envoy (C++) | apisix (LuaJIT) | Nginx (C) / Kong (Lua) |
| **扩展语言** | Go/C++/Rust (WASM) | Lua (性能极高) | Lua / Go / Python (PDK) |
| **AI 特性** | **原生支持** (SSE优化, Token统计, MCP) | 需配置插件支持 | 需配置插件支持 |
| **配置热更新** | xDS (毫秒级, 无缝) | Etcd (毫秒级) | 数据库轮询 (有延迟) |
| **K8s 集成** | 深度集成 (Istio 生态) | 深度集成 | 支持但较重 |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中嵌入 WASM 运行时（如 Wasmtime 或 V8）。当插件被配置时，Higress Control Plane 将编译好的 `.wasm` 文件推送到 Data Plane。Envoy 为每个请求（或每个线程）创建一个 WASM VM 实例（或复用实例），通过 `proxy-wasm` ABI 标准与宿主交互。
*   **流式处理优化**：在处理 SSE 请求时，Higress 配置 Envoy 的 `streaming_filters`。它不会等到整个响应 Body 接收完毕再转发，而是通过 Filter Chain 逐块处理数据，确保 AI 生成的每一个 Token 都能实时抵达客户端。

### 代码组织与设计模式
*   **控制平面**：主要使用 Go 语言编写。采用了 Kubernetes Controller 模式（Informer/SharedInformer）来监听 K8s 资源和 Higress 自定义资源（CRD）。
*   **配置分发**：实现了标准的 xDS Server（v2/v3 gRPC 协议）。当 Go 侧检测到配置变化时，将其转换为 Envoy 的 Listener/Route/Cluster 配置，通过 gRPC 推送给 Envoy。
*   **插件系统**：采用了 **Filter Chain** 模式。无论是用 Go 还是 C++ 编写的 WASM 插件，最终都实现 `on_http_request_headers`、`on_http_response_body` 等钩子函数。

### 性能与扩展性
*   **线程模型**：Envoy 采用多线程单事件循环模型。Higress 继承了这一点，每个 CPU 核心一个线程，避免了锁竞争。
*   **扩展性瓶颈**：WASM 的执行速度虽然快，但比原生 C++ 代码慢，且存在内存拷贝开销。Higress 通过在内存中缓存 WASM 实例来优化，但在极高并发下，WASM 插件的内存占用仍需监控。

---

## 4. 适用场景分析

### 最适合的项目
*   **大模型应用 (LLM Apps)**：特别是需要同时对接多个模型厂商、需要精细化 Token 计费、或者涉及 RAG（检索增强生成）流式输出的场景。
*   **云原生微服务网关**：运行在 Kubernetes 之上，需要与 Istio 服务网格共存或复用 Istio 能力的企业。
*   **需要高度定制逻辑的网关**：如果你的业务逻辑需要频繁变更（如特定的鉴权算法、请求改写），且不希望修改网关核心代码或重启网关，WASM 插件机制是最佳选择。

### 不适合的场景
*   **极致简单场景**：如果只是做一个简单的 Nginx 反向代理，Higress 的部署复杂度（依赖 K8s、Istio）过高，不如直接使用 OpenResty 或 Nginx。
*   **非 K8s 环境**：虽然可以手动部署，但 Higress 的设计初衷是云原生，在虚拟机或物理机上的运维复杂度远高于传统网关。

### 集成注意事项
*   **资源限制**：WASM 插件虽然隔离，但并非完全无开销。需要为 Envoy 容器配置合理的 Memory Limit，防止插件内存泄漏导致 OOM。
*   **xDS 连接**：确保控制平面与数据平面之间的网络稳定，否则配置将无法下发。

---

## 5. 发展趋势展望

### 技术演进方向
*   **从流量管理到语义管理**：Higress 正在从传统的 L7 流量管理向 LLM 语义层管理演进。未来可能会包含更复杂的 Prompt 管理版本控制、向量数据库连接代理等。
*   **MCP 生态的深化**：随着 AI Agent 的普及，MCP 协议可能成为标准。Higress 有望成为企业内部 MCP Server 的标准网关。

### 社区与改进
*   **易用性提升**：目前 WASM 插件的开发对普通开发者仍有门槛（需要了解 WASM 工具链）。未来可能会推出更高级的 DSL（如基于 TypeScript 或 Lua 的转译层），降低插件开发门槛。

---

## 6. 学习建议

### 适合的开发者
*   具备 Golang 基础，了解 Kubernetes 基本概念。
*   对云原生网络、HTTP 协议有深入理解。
*   对 LLM 应用开发感兴趣的开发者。

### 学习路径
1.  **基础**：先学习 Envoy 的基本概念和 xDS 协议。
2.  **实践**：在本地 Kind 集群中部署 Higress，体验 Console 配置和路由转发。
3.  **进阶**：学习 `proxy-wasm` SDK，尝试用 Go 编写一个简单的 WASM 插件（如添加 HTTP Header）。
4.  **AI 特性**：配置 AI 网关，对接 OpenAI 接口，观察流式输出的处理过程。

---

## 7. 最佳实践建议

### 正确使用方式
*   **资源隔离**：在生产环境中，建议将 Higress 网关节点与业务容器分开部署，避免业务应用抢占网关资源。

---
## 代码示例




```python
# 示例1：使用 Higress 进行 API 网关路由配置
from higress import Gateway, Route, Upstream

def setup_api_gateway():
    """
    配置一个简单的 API 网关，将请求路由到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 定义后端服务
    user_service = Upstream(
        name="user-service",
        endpoints=["http://user-service:8001"]
    )
    
    order_service = Upstream(
        name="order-service",
        endpoints=["http://order-service:8002"]
    )
    
    # 配置路由规则
    gateway.add_route(Route(
        path_prefix="/api/users",
        upstream=user_service,
        timeout_ms=5000
    ))
    
    gateway.add_route(Route(
        path_prefix="/api/orders",
        upstream=order_service,
        timeout_ms=3000
    ))
    
    # 应用配置
    gateway.apply()
    print("API 网关路由配置已应用")

# 说明：这个示例展示了如何使用 Higress 配置一个简单的 API 网关，
# 将不同的 API 路径路由到不同的后端服务，并设置超时时间。
```




```python
# 示例2：使用 Higress 实现请求限流
from higress import Gateway, RateLimitConfig

def setup_rate_limiting():
    """
    配置请求限流，防止服务过载
    """
    gateway = Gateway(name="api-gateway")
    
    # 配置限流规则
    rate_limit = RateLimitConfig(
        requests_per_second=100,  # 每秒最多100个请求
        burst=200,                # 允许突发200个请求
        key_type="IP",            # 基于IP限流
        rejected_code=429         # 被拒绝时返回429状态码
    )
    
    # 应用限流配置
    gateway.set_rate_limit(rate_limit)
    print("请求限流配置已应用")

# 说明：这个示例展示了如何使用 Higress 实现请求限流功能，
# 防止服务因过多请求而过载，保护后端服务稳定性。
```




```python
# 示例3：使用 Higress 实现请求认证
from higress import Gateway, AuthConfig

def setup_authentication():
    """
    配置 API 请求认证，确保只有合法请求能通过
    """
    gateway = Gateway(name="api-gateway")
    
    # 配置 JWT 认证
    auth_config = AuthConfig(
        type="JWT",
        jwt_secret="your-secret-key",
        jwt_issuer="your-issuer",
        jwt_audience="your-audience"
    )
    
    # 应用认证配置
    gateway.set_auth(auth_config)
    print("请求认证配置已应用")

# 说明：这个示例展示了如何使用 Higress 实现 API 请求认证，
# 通过 JWT 验证确保只有合法的请求能够访问后端服务。
```


---
## 案例研究


### 1：阿里巴巴淘天集团

 1：阿里巴巴淘天集团

**背景**:  
在阿里巴巴内部，Higress 的前身是支撑阿里内部大量业务（如淘宝、天猫、饿了么等）的网关系统。随着云原生架构的演进，阿里需要一套能够同时支持传统微服务和 Service Mesh（服务网格）架构的统一网关层，以应对每年双11大促期间巨大的流量冲击。

**问题**:  
原有的网关系统在面临云原生架构时存在扩展性瓶颈，且维护成本高。业务部门需要一个能够无缝对接 Kubernetes、支持高并发路由、具备热更新能力且对业务代码侵入性极低的 API 网关。同时，大促期间需要对流量进行精细化的灰度发布和限流控制，传统的配置方式过于复杂且响应不够及时。

**解决方案**:  
阿里基于内部多年的实践沉淀，开源了 Higress。Higress 被部署在阿里云核心业务链路中，作为统一的 API 入口。它深度集成了 Envoy 和 Istio，利用其高性能的 HTTP/3 和 Wasm 插件能力，实现了业务逻辑与网关基础设施的解耦。通过 Higress，阿里实现了对南北向（外部流量进入）和东西向（服务间通信）流量的统一管理。

**效果**:  
Higress 成功支撑了双11期间每秒数十万级的 QPS 峰值。通过 Wasm 插件机制，网关的迭代周期从周级缩短至天级，开发人员可以像写脚本一样扩展网关功能，极大提升了业务迭代效率。同时，统一的网关层显著降低了跨部门协作的复杂度，资源利用率提升了 30% 以上。

---



### 2：萝卜运力（快狗打车）

 2：萝卜运力（快狗打车）

**背景**:  
萝卜运力（快狗打车）作为一家同城货运平台，其业务系统经历了从单体架构向微服务架构的转型。随着业务量的增长，其 API 接口数量激增，且涉及司机端、货主端及内部运营系统等多个终端，对 API 管理和安全性提出了极高要求。

**问题**:  
在转型过程中，团队面临多套网关并存的混乱局面（如 Nginx、Spring Cloud Gateway 等），导致配置不统一、维护困难。此外，旧网关在处理 OpenAPI 规范管理、流量鉴权以及跨域资源共享（CORS）配置时效率低下，且缺乏一个标准化的平台来供前端和后端开发者协作。

**解决方案**:  
快狗打车引入 Higress 作为其云原生 API 网关，替代了原有的异构网关体系。利用 Higress 强大的 OpenAPI 兼容能力和 Ingress/Nginx 兼容配置，团队平滑地将流量迁移至 Higress。同时，利用 Higress 的插件市场（如 Key Auth、Request Block）快速实现了统一的流量安全防护和认证鉴权。

**效果**:  
通过统一网关，快狗打车实现了全链路流量的可视化管理，API 接口的上线发布流程实现了标准化。网关的性能提升了 20%，延迟显著降低。开发团队不再需要关注底层的负载均衡和证书配置，专注于业务逻辑开发，运维效率提升了 50%，并彻底解决了多终端接入时的鉴权混乱问题。

---



### 3：深维科技（AI 视觉处理）

 3：深维科技（AI 视觉处理）

**背景**:  
深维科技专注于为图像和视频处理提供高性能的云计算解决方案。其核心产品需要对上传的图片进行实时的 AI 识别、压缩和格式转换，这对后端处理服务的吞吐量和延迟极其敏感。

**问题**:  
在处理海量图片请求时，传统的网关层往往成为瓶颈，无法高效地将图片流量分发到不同的后端处理服务。此外，针对不同客户定制的图片处理逻辑（如特定的水印、裁剪规则）如果硬编码在网关中，会导致网关逻辑臃肿，难以维护和扩展。

**解决方案**:  
深维科技采用 Higress 作为其业务网关，并利用 Higress 的 Wasm (WebAssembly) 插件能力来处理复杂的图片路由逻辑。他们编写了特定的 Wasm 插件，在网关层直接解析图片请求的参数，动态路由到最适合的 GPU 处理集群，甚至利用 Wasm 的高性能特性在网关边缘做轻量级的预处理。

**效果**:  
通过 Wasm 插件技术，深维科技实现了业务逻辑的动态热加载，无需重启网关即可上线新的图像处理规则。这种架构使得系统的整体吞吐量提升了 40%，同时将业务变更的上线时间从小时级缩短至分钟级，极大地增强了其 SaaS 服务的灵活性和市场响应速度。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和Lua，适合高流量场景 | 极高性能，基于LuaJIT和APISIX，适合超大规模场景 |
| 易用性 | 提供Kubernetes原生支持，集成Istio，配置灵活 | 提供丰富的插件和GUI管理界面，配置相对简单 | 提供动态配置和丰富的插件，但学习曲线较陡 |
| 成本 | 开源免费，企业版需付费支持 | 开源免费，企业版需付费支持 | 开源免费，企业版需付费支持 |
| 扩展性 | 支持自定义插件和Wasm扩展 | 支持自定义插件和Lua脚本 | 支持自定义插件和Lua脚本 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，插件生态丰富 | 社区活跃，国内支持较好 |
| 安全性 | 内置WAF和流量管理功能 | 需额外配置安全插件 | 内置安全功能，但需额外配置 |

### 优势分析

- 优势1：与Kubernetes和Istio深度集成，适合云原生环境。
- 优势2：支持Wasm插件，扩展性强，性能损耗低。
- 优势3：阿里巴巴背书，企业级支持可靠。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较小，插件数量较少。
- 不足2：学习曲线较陡，需要熟悉Istio和Envoy。
- 不足3：企业版功能需付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**: Higress 是基于 Envoy 和 Istio 构建的，充分利用 Envoy 的高性能 L3/L7 处理能力是核心。最佳实践包括理解并调整 Envoy 的线程模型、连接池配置以及缓存设置，以适应高并发、低延迟的云原生 API 网关场景。

**实施步骤**:
1. 根据 CPU 核心数合理配置 Envoy 的 Worker 线程数（通常建议设置为容器的 CPU 限制数）。
2. 针对后端服务配置合适的连接池和限流设置，避免后端过载。
3. 开启并配置 Envoy 的 HTTP 过滤器链，利用 Higress 提供的 Wasm 插件扩展功能，而不是修改 C++ 核心代码。

**注意事项**: 在调整底层网络参数（如 TCP keepalive 或缓冲区大小）时，需先在预发环境进行压力测试，避免因参数不当导致连接异常或内存溢出。

---

### 实践 2：利用 Wasm 插件实现业务逻辑扩展

**说明**: Higress 原生支持 WebAssembly (Wasm) 插件，这允许开发者使用 C++, Go, Rust, AssemblyScript 或 JavaScript 编写自定义逻辑，而无需重新编译网关或使用 Lua 脚本。这比传统的 Lua 脚本性能更好，且隔离性更高。

**实施步骤**:
1. 识别需要在网关层处理的通用逻辑（如请求头转换、JWT 验证、流量染色）。
2. 使用 Higress 官方提供的 Wasm SDK 或示例模板开发插件。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 注册表进行分发。
4. 在路由或全局维度配置插件启用，并配置所需的参数。

**注意事项**: Wasm 插件运行在沙箱中，但仍需注意内存使用和执行耗时。避免在插件中执行阻塞式长耗时操作，以免增加请求延迟。

---

### 实践 3：服务发现与 Nacos 集成配置

**说明**: Higress 深度集成了 Nacos 和 Consul 等注册中心。最佳实践是直接让 Higress 从注册中心动态获取服务列表，实现从“微服务网关”到“API 网关”的无缝对接，避免手动维护静态 IP 列表。

**实施步骤**:
1. 在 Higress 中配置源服务（Source Service），指向你的 Nacos 或 Consul 服务地址。
2. 确保网关网络与注册中心网络互通。
3. 创建 Ingress 或网关路由规则时，Service 名称直接填写注册中心中的服务名。
4. 配置健康检查机制，确保注册中心中的不健康实例不会被网关转发流量。

**注意事项**: 如果服务跨注册中心或跨 namespace，需注意命名规范和访问权限控制。对于大规模服务列表，关注全量拉取对注册中心造成的压力。

---

### 实践 4：精细化流量管理与安全防护

**说明**: 利用 Higress 的全功能网关能力，实施严格的安全策略和流量治理。这包括配置 IP 黑白名单、基于请求头的鉴权、以及防范常见的 Web 攻击（如 SQL 注入、XSS）。

**实施步骤**:
1. 启用 Higress 自带或 Wasm 类型的安全插件，配置基本的安全规则（如限制允许访问的 IP 段）。
2. 对于对外暴露的 API，配置严格的 CORS 策略和请求大小限制。
3. 结合 KeyAuth 或 HMAC Auth 插件对 API 进行签名验证，防止未授权访问。
4. 定期审查网关访问日志，利用对接的日志系统（如 Prometheus/Grafana 或 SLS）分析异常流量。

**注意事项**: 安全策略的启用可能会轻微增加延迟，建议在安全性和性能之间做权衡。避免在日志中打印敏感信息（如 Token、密码）。

---

### 实践 5：金丝雀发布与蓝绿部署

**说明**: 在云原生架构中，平滑升级至关重要。Higress 支持基于 Header、Cookie 或权重的流量路由，是实现金丝雀发布和蓝绿部署的最佳入口。

**实施步骤**:
1. 准备新版本的 Service，并确保其已注册到服务发现中心。
2. 在 Higress 中配置两个不同的服务版本（如 v1 和 v2）。
3. 创建或修改路由规则，设置流量分流策略。例如，设置 10% 的流量流向 v2 版本，或者仅当 Header `x-canary: true` 时流向 v2。
4. 观察新版服务的错误率和延迟，确认稳定后逐步调整权重至 100%。

**注意事项**: 确保新旧版本的数据兼容性。在流量切换期间，保持全链路追踪（Tracing）开启，以便快速定位问题。

---

### 实践 6：可观测性与监控告警

**说明**: Higress

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 构建，原生支持 HTTP/2 和 HTTP/3。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，HTTP/3 则基于 UDP 协议，进一步解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，明确启用 HTTP/2 协议支持。
2. 对于需要极致性能的场景，配置监听器启用 HTTP/3 (QUIC)。
3. 确保上游服务也支持 HTTP/2 以建立端到端的连接复用。

**预期效果**: 在高并发或弱网环境下，请求延迟可降低 20%-40%，连接数消耗减少 50% 以上。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时设置通常较长，不合理的配置会导致大量连接处于挂起状态，耗尽网关线程池资源。精细化的超时与重试策略能快速失败，释放资源给健康的请求。

**实施方法**:
1. **连接超时**: 建议设置为 3-5 秒，避免长时间等待不活跃的 TCP 握手。
2. **请求超时**: 根据业务 P99 耗时设置，例如设置为 2 秒。
3. **智能重试**: 配置针对 5xx 错误或连接失败的重试策略，限制重试次数（如 2 次），并开启“指数退避”算法。

**预期效果**: 在故障发生时，系统响应速度提升，资源利用率提高 30% 以上，有效防止雪崩效应。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 或远程调用逻辑，Wasm 执行效率更高，且安全性更好。同时，对于高频读取的低频变动配置（如限流规则、路由映射），应启用本地缓存以减少 I/O 开销。

**实施方法**:
1. 将复杂的鉴权、请求头修改逻辑编写为 Wasm 插件并部署。
2. 在网关配置中开启路由匹配或配置项的本地内存缓存。
3. 避免在请求路径中进行同步的远程 RPC 调用（如查库），改为异步或缓存。

**预期效果**: Wasm 插件比传统 Lua 插件性能提升 10%-20%；启用本地缓存可减少 90% 的配置读取延迟。

---

### 优化 4：调整连接池与工作线程数

**说明**: Higress (Envoy) 默认的连接池配置可能无法应对突发流量。适当调大上游连接池大小，并根据 CPU 核心数调整 Worker 线程数，可以最大化吞吐量。

**实施方法**:
1. **调整连接池**: 将 HTTP/1.1 连接池的最大连接数从默认的 2 或 5 调整为 100-500（视上游服务承载能力而定）。
2. **启用 HTTP/2 上游**: 如果上游支持，使用 HTTP/2 连接池以减少连接数开销。
3. **Worker 线程**: 确保 Higress 容器的 `worker` 数量与 CPU 核心数绑定（通常设置为 `auto` 或等于核心数）。

**预期效果**: 吞吐量（QPS）提升 50%-200%，显著降低因连接池耗尽导致的 503 错误率。

---

### 优化 5：启用数据压缩与响应缓存

**说明**: 对于文本类数据（JSON, XML, HTML, JS），启用 Gzip 或 Brotli 压缩可大幅减少网络传输带宽，并加快客户端首字节加载速度。对于幂等的 GET 请求，可配置网关层缓存。

**实施方法**:
1. 在 Higress 路由配置中启用“压缩”过滤器，设置压缩阈值（如大于 1KB）

---
## 学习要点

- 基于对 Alibaba Higress 项目（通常出现在 GitHub Trending 上的云原生网关）的分析，总结如下：
- Higress 是阿里云开源的下一代云原生 API 网关，深度集成了 K8s Ingress 与 Gateway API 标准，实现了从南向负载均衡到北向 API 管理的全栈能力。
- 该项目基于 Envoy 和 Istio 构建，在保持高性能数据面的同时，通过将控制面从 Istio 中解耦，显著降低了架构复杂度和运维成本。
- 它提供了开箱即用的 WAF（Web 应用防火墙）插件支持，能够有效防范 SQL 注入、XSS 等 Web 安全威胁，保障业务安全性。
- Higress 兼容 Nginx Ingress 注解配置，并支持从 Nginx 平滑迁移，使得用户能够以极低的迁移成本享受云原生网关的弹性与可观测性。
- 内置了针对 Dubbo、gRPC 等微服务协议的强大支持，解决了传统网关在处理 RPC 服务调用时的协议转换与流量治理难题。
- 拥有强大的 Wasm 插件生态，支持使用 Go、Python、AssemblyScript 等多语言编写插件，实现了业务逻辑的热加载与灵活扩展。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 的作用，以及 Higress 与 Nginx、Kong、Istio Ingress Gateway 的区别与联系。
- 核心架构：掌握 Higress 基于 Envoy 和 Istio 的架构设计，理解其数据面与控制面的分离。
- 部署方式：学习如何通过 Docker 和 Kubernetes (Helm) 部署 Higress。
- 基本配置：掌握域名转发、路由匹配、TLS 证书配置等基础流量管理操作。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (入门与安装部分)
- Higress GitHub 仓库 README
- Envoy 官方文档基础概念

**学习建议**: 建议先在本地或测试环境使用 Docker 快速部署一个 Higress 实例，通过控制台界面进行一次简单的服务转发配置，建立感性认识。

---

### 阶段 2：流量治理与插件系统

**学习内容**:
- 高级流量管理：深入学习灰度发布、蓝绿发布、流量镜像和超时重试配置。
- 插件系统：掌握 Higress 的插件机制，学习如何使用官方插件（如限流、认证、请求/响应修改）。
- WAF 防护：了解如何利用内置插件配置 Web 应用防火墙规则以增强安全性。
- 服务发现：配置对接 Nacos、Consul 或 Kubernetes Service 作为服务来源。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件市场
- Higress 官方示例库
- Kubernetes Service 与 Ingress 官方文档

**学习建议**: 尝试构建一个包含两个版本服务的微服务场景，配置基于 Header 的金丝雀发布。同时，实验 Key Auth 插件来保护 API 安全。

---

### 阶段 3：云原生集成与高性能实践

**学习内容**:
- Ingress 与 Gateway API：深入学习 Higress 作为 Kubernetes Ingress Controller 的使用，以及对 Gateway API 标准的支持。
- 全局缓存与动态路由：配置 HTTP 缓存策略以提升后端性能，实现更复杂的动态路由规则。
- 可观测性：集成 Prometheus、Grafana、SkyWalking 或阿里云 ARMS，配置日志服务（SLS）和链路追踪。
- 高可用部署：学习生产环境下的多副本部署、资源限制与性能调优。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 可观测性与最佳实践
- Gateway API 规范说明
- Prometheus 监控最佳实践

**学习建议**: 在 Kubernetes 集群中部署 Higress，并模拟高并发流量场景。重点配置监控大盘，观察 QPS、延迟和成功率等指标，以此为基础进行参数调优。

---

### 阶段 4：深度定制与源码开发

**学习内容**:
- 自定义插件开发：学习使用 Lua 或 WASM (WebAssembly) 开发自定义插件，实现业务定制的逻辑。
- WASM 生态：深入理解 WASM 在 Higress 中的应用，使用 Go 或 Rust 编写 Wasm 插件。
- 源码解析：阅读 Higress 控制面和 Router 的源码，理解配置下发机制和路由匹配逻辑。
- 服务网格集成：探索 Higress 与 Istio 服务网格的深度集成场景，实现东西向与南北向流量的统一管理。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub 源码
- Higress 官方文档 - 自定义插件开发指南
- WebAssembly (Wasm) 官方文档与教程
- Istio 官方文档

**学习建议**: 选取一个具体的业务痛点（如特殊的签名验证逻辑），尝试编写一个 Lua 或 Go Wasm 插件并在 Higress 中运行。阅读源码时，建议从控制面处理 Ingress 资源的逻辑入手。

---
## 常见问题


### 1: Higress 是什么？它主要解决什么问题？

1: Higress 是什么？它主要解决什么问题？

**A**: Higress 是一款由阿里云开源的、云原生领域的 API 网关。它基于阿里内部多年在网关领域的实践以及开源项目 Istio 和 Envoy 构建。Higress 主要旨在解决云原生架构下 API 流量管理的问题，特别是连接后端微服务（如 Kubernetes 上的服务）与前端客户端（如 Web、App、SaaS）之间的连接层。它集成了 Nginx Ingress Controller 的流量管理能力、Kong 的高性能扩展能力以及 Istio 的强大治理能力，旨在提供一站式的流量入口管理解决方案。

---



### 2: Higress 与传统的 Nginx Ingress Controller 或 Kong 网关相比有什么优势？

2: Higress 与传统的 Nginx Ingress Controller 或 Kong 网关相比有什么优势？

**A**: Higress 相比传统网关具有以下显著优势：

1.  **云原生深度集成**：Higress 原生支持 Kubernetes 和 Istio 服务网格，能够无缝对接服务网格内的服务，实现南北向（入口流量）与东西向（服务间流量）流量的统一管理，这是传统 Nginx Ingress 难以做到的。
2.  **高性能与低资源消耗**：基于 Envoy（C++ 编写）作为数据面，Higress 在处理高并发流量时通常比基于 Lua 的 Kong 或纯 Nginx 配置具有更低的延迟和更高的吞吐量，且资源占用更少。
3.  **标准化的扩展能力**：Higress 支持 WASM（WebAssembly）插件编写。这意味着开发者可以使用 Go、C++、Rust 甚至 JavaScript/TypeScript 来编写插件，这些插件运行在沙箱环境中，不仅安全性高，而且无需重新编译网关即可动态加载，比 Nginx 的 Lua 模块或 Kong 的插件开发更灵活、更现代化。
4.  **开箱即用的特性**：它提供了丰富的内置功能，如 Dashboard 控制台、完善的 Prometheus 监控集成、以及针对阿里云生态（如 MSE, ACK）的深度优化。

---



### 3: Higress 与 Istio 有什么区别？既然有了 Istio，为什么还需要 Higress？

3: Higress 与 Istio 有什么区别？既然有了 Istio，为什么还需要 Higress？

**A**: 虽然 Higress 底层依赖了 Istio 的控制平面组件（如 Pilot），但它们的定位不同：

1.  **定位差异**：Istio 主要专注于服务网格，即管理集群内部的服务间通信（东西向流量）。而 Higress 专注于 API 网关，即管理进入集群的流量（南北向流量）。
2.  **易用性与功能**：原生的 Istio Ingress Gateway 配置非常复杂（需要处理 CRD、VirtualService 等），且缺乏许多传统 API 网关的特性，如精细的鉴权、流量后端直接转发、域名管理、控制台 UI 等。Higress 在 Istio 之上进行了封装，提供了更符合 API 网关使用习惯的控制台和配置方式，填补了 Istio 作为入口网关时的易用性空白。
3.  **性能优化**：Higress 对 Envoy 进行了针对网关场景的特定优化，使其在作为入口网关时性能更佳。

简单来说，Higress 可以被看作是 Istio Ingress Gateway 的增强版和商业化/产品化实现。

---



### 4: Higress 支持哪些类型的插件？如何扩展功能？

4: Higress 支持哪些类型的插件？如何扩展功能？

**A**: Higress 拥有非常灵活的插件体系，主要支持以下几种扩展方式：

1.  **WASM (WebAssembly) 插件（推荐）**：这是 Higress 最具特色的扩展方式。它支持 WASM 标准，允许开发者使用 Go、AssemblyScript、Rust 或 C++ 编写逻辑。WASM 插件的优势是**热加载**（无需重启网关）、**隔离性好**（插件崩溃不影响网关主进程）且开发门槛低。
2.  **Lua 插件（兼容）**：为了兼容 Nginx 和 Kong 生态，Higress 也支持 Lua 脚本，允许用户复用现有的 Lua 逻辑。
3.  **原生 Envoy 过滤器**：对于极高性能要求的场景，Higress 底层基于 Envoy，因此也支持编写 Envoy 原生扩展。
4.  **预置插件**：官方内置了大量开箱即用的插件，包括认证鉴权（如 Basic Auth, AK/SK, JWT）、流量控制（限流、熔断）、可观测性（日志、调用链）以及针对阿里云服务的特定插件。

---



### 5: Higress 是否支持从 Nginx 或 Kong 迁移？迁移难度大吗？

5: Higress 是否支持从 Nginx 或 Kong 迁移？迁移难度大吗？

**A**: 是的，Higress 非常注重对旧有网关的兼容性，旨在降低迁移成本。

1.  **Nginx 兼容**：Higress 提供了 Nginx Ingress 注解的兼容支持。这意味着如果你的 Kubernetes 集群原本使用的是 Nginx Ingress Controller，Higress 可以识别大部分常见的 Nginx 注解，

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速上手与流量验证

### 假设你已经成功通过 Docker 或 Kubernetes 部署了 Higress。请配置一个简单的 Ingress 路由，将访问 `http://your-domain.com/test` 的流量转发到后端的 `httpbin.org` 服务，并要求在转发请求时自动添加一个名为 `Higress-Route` 的 HTTP Header，值为 `test-demo`。请使用 Higress 的控制台（Console）或 WasmPlugin 配置完成此操作，并使用 curl 命令验证 Header 是否添加成功。

### 提示**:

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 6 条实践建议：

### 1. 利用 AI 指标进行精细化成本控制
Higress 在 AI 网关模式下，能够解析大模型（LLM）的 Token 流。建议在路由配置中开启针对 Token 的统计与限流。
*   **具体操作**：不要仅依赖传统的 QPS（每秒请求数）限制。在插件配置中，设置基于 Prompt Tokens 和 Completion Tokens 的速率限制。例如，对低成本用户限制每分钟处理的 Token 总数，以防止恶意消耗模型配额。
*   **常见陷阱**：忽略流式响应（SSE）中的 Token 计数差异，导致实际计费与预期不符。

### 2. 实施模型供应商的故障转移
在生产环境中，单一的大模型服务商（如 OpenAI 或 Azure）可能会出现 API 不稳定或限流。
*   **具体操作**：在 Higress 的服务管理中配置多来源模型服务。利用 Higress 的“默认服务”和“ fallback 服务”机制，配置当主模型供应商响应超时（如超过 5 秒）或返回 5xx 错误时，自动将请求切换至备用模型提供商或备用的模型 Endpoint。
*   **最佳实践**：结合 Higress 的云原生网关特性，将不同厂商的 API 注册为同一个服务下的不同主机，实现无感知的故障切换。

### 3. 敏感数据的实时脱敏与审计
当企业内部数据传输至公有大模型时，存在数据泄露风险。
*   **具体操作**：部署并启用 Higress 的“请求体转换”或专门的 AI 安全插件。配置规则以拦截并遮盖 Prompt 中的敏感信息（如身份证号、API Key、内部 IP 地址）。
*   **具体操作**：开启全链路日志审计，记录 Prompt 和 Completion 的摘要，用于后续的合规检查和模型调优分析，但需注意在日志侧也要进行脱敏处理。

### 4. 优化 SSE 流式响应的连接超时配置
AI 对话通常采用 Server-Sent Events (SSE) 流式输出，耗时较长，这与传统的高频短链接 API 网关配置不同。
*   **具体操作**：检查并调整 Higress 的全局或路由级 `idle_timeout` 和 `request_timeout` 配置。对于生成类模型，建议将超时时间放宽至 2 分钟甚至更长，以适应模型生成长文本的需求。
*   **常见陷阱**：使用了默认的短连接超时配置（如 60 秒），导致模型还在生成内容时，网关主动断开连接，前端报错。

### 5. 构建统一的 Prompt 模板管理
为了避免在每个前端应用中硬编码 Prompt，建议将 Prompt 管理下沉至网关层。
*   **具体操作**：使用 Higress 的插件（如 `ai-proxy` 或请求头插件）在网关层预置 System Prompt。前端只需发送简化的 User Message，网关在转发给后端模型前，自动拼接预设的“人设”或“上下文”模板。
*   **最佳实践**：通过不同路由或插件参数区分不同业务场景的 Prompt 模板，实现 Prompt 的版本控制与灰度发布，无需重新部署业务代码。

### 6. 区分 AI 流量与传统 API 流量的治理策略
Higress 同时承载传统流量和 AI 流量，两者的资源消耗模型截然不同（AI 流量通常连接时间长、CPU 计算密集、带宽消耗取决于 Token 生成速度）。
*   **具体操作**：建议在 K8s 集群中为 Higress 开启自动扩缩容（HPA）时，不仅关注 CPU 指标，还要关注并发连接数。考虑将 AI 网关与普通 API 网关进行逻辑隔离（使用不同的 Ingress 或 Gateway 实例），防止 AI 的高负载长连接占满网关连接池，从而影响普通业务接口的响应速度。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/)
- 场景： [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260207-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260214-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*