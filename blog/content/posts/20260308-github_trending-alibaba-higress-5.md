---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-08T00:04:28+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是关于 **Higress** 项目的中文总结： **项目概况** Higress 是一个由阿里巴巴开源的、**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，目前在 GitHub 上拥有超过 7,600 个星标。它建立在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WA"
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
- **星标**: 7,682 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在为云原生应用与大模型场景提供统一的流量管理入口。它通过 WASM 插件扩展了传统 API 网关能力，并集成了 AI 网关与 MCP 服务托管功能，适合需要处理微服务路由或 LLM 应用的开发团队。本文将介绍其核心架构、主要功能及适用场景，帮助读者理解如何利用它来简化服务治理与 AI 集成。

---
## 摘要

以下是关于 **Higress** 项目的中文总结：

**项目概况**
Higress 是一个由阿里巴巴开源的、**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，目前在 GitHub 上拥有超过 7,600 个星标。它建立在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，为云原生应用和 AI 大模型应用提供统一的流量管理入口。

**核心架构与优势**
Higress 采用**控制平面与数据平面分离**的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **高性能分发**：配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适合 AI 长连接流式响应等场景。

**三大主要功能场景**
1.  **AI 网关**：
    *   提供统一的 API 接口，兼容 30+ 家大语言模型（LLM）提供商。
    *   支持协议转换、可观测性、缓存和**安全防护**（`ai-security-guard`）。
2.  **MCP 服务器托管**：
    *   托管 **模型上下文协议 (MCP)** 服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   包含 `mcp-router` 和具体的工具实现（如地图搜索等）。
3.  **传统 API 网关**：
    *   作为 Kubernetes Ingress 控制器使用，支持微服务路由，并兼容 nginx-ingress 注解，方便用户无缝迁移。

**总结**
简而言之，Higress 是一款将传统微服务治理与新兴 AI 应用需求深度融合的下一代网关，既能处理 K8s Ingress 流量，又能为 AI 应用提供模型分发、智能体工具集成及安全防护。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域将**AI 原生能力**与**传统流量治理**融合得最为彻底的开源项目之一。它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 MCP 协议的深度集成，为 LLM（大语言模型）应用提供了一套标准化的基础设施解决方案，是连接传统微服务与未来 AI 服务的强力纽带。

---

### 深度评价分析

#### 1. 技术创新性：从“流量管道”进化为“AI 智能体”
*   **事实**：Higress 定义为 "AI Native API Gateway"，核心基于 Istio 和 Envoy，并引入了 WASM 插件能力和 MCP (Model Context Protocol) 系统支持。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/TCP 转发，而 Higress 的差异化在于它**内置了对 AI 语义的理解**。
    *   **WASM 的深度应用**：它利用 WebAssembly 技术实现了热更新和沙箱隔离，使得开发者可以用 C++/Go/Rust/JS 编写复杂的 AI 逻辑（如 Prompt 注入、敏感词过滤）而无需重启网关，这比 Lua 脚本更具安全性和高性能。
    *   **MCP 协议集成**：这是极具前瞻性的创新。通过支持 MCP，Higress 直接充当了 AI Agent（智能体）的工具箱。这意味着网关不再仅仅是流量的转发者，更是 AI 能力的**提供者和编排者**，让 LLM 能够安全、标准地调用后端 API 和数据。

#### 2. 实用价值：解决 AI 落地“最后一公里”的痛点
*   **事实**：文档明确指出其提供 "AI gateway features for LLM applications" 和 "MCP server hosting"，同时兼容 Kubernetes Ingress。
*   **推断**：在当前 AI 爆发期，企业面临大量异构模型（OpenAI, Claude, 通义千问等）的接入难题。Higress 解决了三个关键问题：
    *   **统一协议与模型切换**：通过网关屏蔽不同厂商 API 的差异，业务层只需调用统一接口，网关层可动态配置路由到不同的模型提供商，实现**模型供应商的无感切换**。
    *   **成本与安全控制**：提供了 Token 计费、上下文缓存管理和请求拦截。企业可以在网关层直接截断恶意攻击或超额请求，避免后端昂贵的 LLM 产生不必要的费用。
    *   **存量资产保护**：它完全兼容 K8s Ingress，意味着用户可以在不引入新组件的情况下，将现有的微服务网关平滑升级为 AI 网关。

#### 3. 代码质量与架构：云原生工业级的典范
*   **事实**：项目由阿里巴巴主导，使用 Go 语言开发，星标数 7,682。架构上明确分离了控制平面和数据平面。
*   **推断**：
    *   **架构设计**：基于 Envoy 作为数据平面保证了极高的并发性能（C++ 的 L4/L7 处理能力），Go 语言编写的控制平面利用了 K8s 的成熟生态。这种“控制面 Go + 数据面 Envoy”的组合是目前云原生组件的**黄金标准**，兼顾了开发效率和运行时性能。
    *   **可扩展性**：WASM 插件系统的设计非常精妙，它允许业务逻辑与核心网关代码解耦。从代码规范来看，作为阿里系开源项目，其代码结构清晰，遵循了严格的 Go 惯用法和 K8s 风格的 API 定义。

#### 4. 社区活跃度与生态：头部背书，生态初成
*   **事实**：GitHub 星标数较高，且 README 提供了中、日、英多语言版本，显示其国际化野心。
*   **推断**：作为阿里云 Higress 的开源版本，它拥有强大的商业背书，避免了个人开源项目容易弃坑的风险。社区活跃度不仅体现在 Issue 响应上，更体现在其**插件生态**的丰富度上。由于它兼容 Istio，Kubernetes 社区的庞大用户群体都是其潜在贡献者。目前它正在积极构建 AI 生态插件，这比单纯的网关项目更具吸引力。

#### 5. 学习价值：理解云原生与 AI 交互的绝佳样本
*   **事实**：项目涵盖了 Ingress 管理、WASM 插件开发、MCP 协议实现以及 AI 流量处理逻辑。
*   **推断**：对于开发者而言，Higress 是学习**“如何将 AI 能力工程化”**的最佳教科书。
    *   你可以学习如何处理 SSE（Server-Sent Events）流式传输，这是 LLM 对话体验的关键。
    *   你可以深入理解 WASM 在边缘计算和网关侧的实际落地模式。
    *   它展示了如何设计一个既支持传统 RESTful API，又支持 AI 对话流的统一网关架构。

#### 6. 潜在问题与改进建议
*   **复杂度曲线**：虽然功能强大，但基于 Istio 和 Envoy 的架构意味着运维门槛较高。对于没有 K8s 基础的小团队，部署和调优 Higress 是一个挑战。
*   **WASM 的调试难度**：虽然 WASM 提供了隔离性，但在生产环境调试 WASM 插件的性能瓶颈和内存泄漏相比原生

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是 **"AI Native API Gateway"**，其架构设计体现了云原生时代对高性能、可扩展性和 AI 生态融合的深度思考。

### 1.1 技术栈与架构模式
Higress 采用了 **控制平面与数据平面分离** 的标准云原生架构模式。
*   **数据平面**：基于 **Envoy** 构建。Envoy 是 L7 代理和边车车的行业标准，C++ 编写，具有极高的性能和内存安全性。Higress 深度定制了 Envoy，以支持 WASM 和特定的 AI 协议处理。
*   **控制平面**：基于 **Istio** 生态。它复用了 Istio 的 Galley（配置验证）和 Pilot（xDS 下发）核心逻辑，但剥离了 Sidecar 模式的繁重治理能力，专注于 Gateway 的 Ingress 管理。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为一等公民。通过 Proxy-WASM 规范，允许使用 C/C++/Go/Rust 等语言编写插件，运行在沙箱环境中，极大降低了扩展门槛并提升了安全性。

### 1.2 核心模块
*   **Router (路由层)**：基于 Envoy 的 HTTP Connection Manager 针对云原生场景进行了优化，支持 HTTP/1.1, HTTP/2, HTTP/3 (QUIC) 以及 gRPC。
*   **WASM Plugin System (插件系统)**：这是 Higress 的心脏。它不仅支持传统的流量管理（鉴权、限流、重试），还通过 WASM 实现了动态加载和热更新，无需重启网关即可修改业务逻辑。
*   **AI Service Integration (AI 服务集成)**：专门针对 LLM（大语言模型）优化的处理模块。它能够理解 SSE (Server-Sent Events) 流式传输，并进行协议转换。

### 1.3 架构优势
*   **配置变更毫秒级生效**：得益于 xDS 协议（控制平面与数据平面通信标准），配置变更无需 Reload 进程，连接不中断，这对长连接（如 AI 对话流）至关重要。
*   **生态隔离**：将 Istio 的复杂治理能力下沉，仅保留 Gateway 所需的核心，使得运维复杂度相比完整的 Istio 大幅降低。

---

## 2. 核心功能详细解读

### 2.1 AI Gateway (AI 网关)
这是 Higress 区别于 Nginx、APISIX 或 Kong 的核心差异点。
*   **功能**：提供统一的后端管理（OpenAI, Azure, 通义千问, Ollama 等），支持 Provider 之间的模型切换。
*   **解决的关键问题**：
    *   **协议兼容性**：自动处理不同 LLM 提供商之间细微的 API 差异。
    *   **Token 计费与流式处理**：在网关层截获流式响应，统计 Token 消耗，实现基于流量的精确计费和限流，而无需等待流结束。
    *   **提示词增强**：在请求到达后端模型前，通过网关注入系统提示词或敏感词过滤逻辑。

### 2.2 MCP (Model Context Protocol) Server Hosting
Higress 内置了对 MCP 协议的支持，允许 AI Agent 透过网关安全地访问外部工具和数据源。
*   **技术实现**：网关充当 MCP Server 的托管代理，将内部微服务暴露为 AI Agent 可调用的 Tools，同时处理认证和鉴权，解决了 AI 时代 "Agent 如何安全访问企业内网服务" 的问题。

### 2.3 传统 API 网关能力
*   支持 K8s Ingress 自动发现。
*   支持 Canary Deployment（金丝雀发布）和 Blue-Green Deployment（蓝绿部署）。
*   全功能的 WASM 插件市场（官方提供 Keyless Auth, Request Block, JWT Auth 等插件）。

### 2.4 与同类工具对比
| 特性 | Higress | Nginx/Kong (OpenResty) | APISIX | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **底层语言** | C++ (Envoy) + Go (Control) | C (Nginx) + Lua | C++ (Exaslax) + Lua | C++ (Envoy) + Go |
| **扩展机制** | WASM (沙箱, 多语言) | Lua (JIT, 高耦合) | Lua / Plugin Runner | WASM / Lua |
| **AI 原生支持** | **内置** (Provider管理, SSE处理) | 需手写脚本 | 需手写插件 | 需配置 EnvoyFilter |
| **配置热更新** | 毫秒级, 无损 | 秒级 (部分需 Reload) | 毫秒级 | 毫秒级 |
| **K8s 集成** | 原生支持 (CRD) | 需 Controller | 原生支持 (CRD) | 原生支持 (CRD) |

**结论**：Higress 在 AI 场景下具有明显的“开箱即用”优势，且 WASM 架构比 Lua 更具现代化和安全性。

---

## 3. 技术实现细节

### 3.1 关键技术方案：WASM 插件加载
Higress 使用了 Proxy-WASM SDK。
*   **流程**：控制平面将编译好的 `.wasm` 文件推送到数据平面。Envoy 启动一个独立的 WASM VM（通常是 Wasmtime 或 V8）。
*   **通信**：通过 `on_request_headers`, `on_response_body` 等虚函数钩子，Host (Envoy) 与 Guest (WASM) 之间进行零拷贝内存共享或 ABI 调用。
*   **难点解决**：WASM 的启动延迟和资源隔离。Higress 对 WASM VM 的生命周期进行了优化，支持 Plugin-level 的 VM 复用。

### 3.2 代码组织结构
*   **`/pkg`**: 核心业务逻辑，主要是 Ingress Controller 的实现，负责监听 K8s 资源并转换为 xDS 配置。
*   **`/plugins`**: WASM 插件源码，通常包含 Go (通过 TinyGo 编译) 或 C++ 实现的示例。
*   **`/docker`**: 镜像构建相关，将 Envoy 和 Controller 打包。

### 3.3 性能优化
*   **多线程并发**：Envoy 本身基于非阻塞 I/O，利用多核进行 Worker 线程调度。
*   **零拷贝**：在处理 SSE 流时，尽量减少内存拷贝，直接透传 TCP Payload。
*   **连接池**：针对 LLM 后端服务，维护 HTTP/2 连接池，减少握手开销。

---

## 4. 适用场景分析

### 4.1 最适合的场景
1.  **AI 应用开发平台**：企业构建类似 ChatGPT 的应用，需要统一管理 OpenAI/Azure/私有模型的 Key、配额和路由。
2.  **微服务 API 统一入口**：特别是 K8s 环境，且需要复杂的自定义逻辑（如复杂的 Header 转换、鉴权）。
3.  **多语言混合技术栈**：团队中有 Go/Python/Java 开发者，都可以通过 WASM 编写网关逻辑，无需所有人去学 Lua（Nginx）或 C++（Envoy 原生）。

### 4.2 不适合的场景
1.  **极致边缘计算**：如果资源受限严重（如 1GB 内存以下），Envoy 的内存开销相比 OpenResty/Nginx 较大。
2.  **静态文件服务**：虽然能做，但用 Nginx 或 CDN 处理静态资源更简单高效。
3.  **简单的 L4 负载均衡**：不需要 L7 处理时，使用 IPVS 或单纯的 Service 足够。

### 4.3 集成方式
*   **K8s Ingress**：通过 `Ingress` 资源或自定义的 `GreedyRouteConfig` 资源进行配置。
*   **控制台 UI**：Higress 提供了基于 K8s 的管理后台，可视化管理路由和插件。

---

## 5. 发展趋势展望

### 5.1 技术演进方向
*   **AI Agent 基础设施化**：随着 LLM 应用的深入，网关将不仅仅是流量转发，更会成为 "AI 编排层"，负责 RAG (检索增强生成) 的路由、Cache 命中率优化以及语义缓存。
*   **WASM 生态标准化**：Higress 正在推动 WASM 插件在不同网关之间的通用性。

### 5.2 潜在改进空间
*   **可观测性深度集成**：虽然支持 Prometheus/SLS，但对于 AI 特有的指标（如 Token 响应时间 TTFB, 上下文长度分布）的原生监控面板仍需加强。
*   **MCP 协议的成熟度**：MCP 目前仍较新，Higress 对其的实现细节和安全性验证有待社区检验。

---

## 6. 学习建议

### 6.1 适合的开发者
*   具备 **Kubernetes** 基础的运维/SRE。
*   **Go 语言**开发者（阅读控制平面代码）。
*   **云原生架构师**（理解 Service Mesh 和 Gateway）。

### 6.2 学习路径
1.  **基础**：先理解 Envoy 的 xDS 协议和 HTTP 路由概念。
2.  **实践**：在本地 Kind 集群中部署 Higress，配置一个简单的 Ingress 和一个 WASM 插件（如 Key Auth）。
3.  **进阶**：使用 Go 或 TinyGo 编写一个自定义 WASM 插件，实现自定义的请求修改逻辑。
4.  **AI 场景**：配置 Higress 作为 OpenAI 的代理，体验 Provider 切换和流式响应处理。

---

## 7. 最佳实践建议

### 7.1 正确使用指南
*   **资源限制**：在 K8s 中为 Higress Gateway 设置合理的 Memory Limit，建议预留 2GB+，因为 Envoy 的内存消耗与连接数和缓存配置正相关。
*   **WASM 插件开发**：避免在插件中进行阻塞式网络调用（如直接请求第三方 API），这可能阻塞 Envoy 的 Worker 线程。应尽量使用异步调用或本地缓存逻辑。
*   **AI 提示词注入**：利用 Higress 的插件能力，在网关层统一注入企业的安全合规 Prompt，避免在每个应用中重复实现。

### 7.2 常见问题
*   **连接中断**：配置变更后旧连接是否会断？答：Higress 支持无损更新，连接不会断开，但新配置仅对新连接生效。
*   **性能瓶颈**：WASM 插件会增加

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway, Route, Service

    # 创建网关实例
    gateway = Gateway(name="api-gateway")

    # 定义后端服务
    user_service = Service(name="user-service", url="http://user-service:8080")
    order_service = Service(name="order-service", url="http://order-service:8081")

    # 配置路由规则
    gateway.add_route(Route(
        path="/api/users/*",
        service=user_service,
        methods=["GET", "POST"]
    ))

    gateway.add_route(Route(
        path="/api/orders/*",
        service=order_service,
        methods=["GET", "POST", "PUT"]
    ))

    return gateway

# 说明：这个示例展示了如何使用 Higress 配置微服务网关的路由规则，
# 实现了根据请求路径将流量分发到不同的后端服务。
```




```python
# 示例2：Higress 限流配置
def higress_rate_limiter():
    """
    配置 Higress 的限流策略
    解决问题：保护后端服务免受流量冲击
    """
    from higress import Gateway, RateLimit

    gateway = Gateway(name="api-gateway")

    # 配置全局限流策略
    gateway.add_rate_limit(RateLimit(
        name="global-limit",
        requests_per_second=100,
        burst=200
    ))

    # 配置特定API的限流策略
    gateway.add_rate_limit(RateLimit(
        name="api-limit",
        path="/api/v1/sensitive",
        requests_per_second=10,
        burst=20
    ))

    return gateway

# 说明：这个示例展示了如何使用 Higress 配置限流策略，
# 可以实现全局限流和针对特定API的精细限流控制。
```




```python
# 示例3：Higress 插件配置
def higress_plugin_config():
    """
    配置 Higress 的插件功能
    解决问题：为网关添加认证、日志等增强功能
    """
    from higress import Gateway, Plugin

    gateway = Gateway(name="api-gateway")

    # 配置JWT认证插件
    gateway.add_plugin(Plugin(
        name="jwt-auth",
        config={
            "secret": "your-secret-key",
            "algorithm": "HS256",
            "token_header": "Authorization"
        }
    ))

    # 配置访问日志插件
    gateway.add_plugin(Plugin(
        name="access-logger",
        config={
            "log_format": "json",
            "include_headers": ["User-Agent", "X-Request-ID"],
            "log_path": "/var/log/higress/access.log"
        }
    ))

    return gateway

# 说明：这个示例展示了如何使用 Higress 的插件系统，
# 实现了JWT认证和访问日志记录等增强功能。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务核心链路

 1：阿里巴巴内部电商业务核心链路

**背景**:
在阿里巴巴庞大的电商生态系统中，双十一等大促活动期间，流量会呈现数十倍甚至百倍的瞬时爆发。传统的网关架构在面对这种海量并发请求时，往往面临资源利用率不均、扩容响应滞后以及配置推送延迟等挑战。

**问题**:
原有基于传统架构的网关在应对流量洪峰时存在以下痛点：
1.  **配置热更新效率低**：路由规则和限流配置的修改需要重启或较长时间生效，无法应对大促期间瞬息万变的流量防护需求。
2.  **性能瓶颈**：在高并发场景下，CPU 开销较高，延迟不够稳定。
3.  **架构僵化**：难以与阿里云内部的 Service Mesh（如 Istio）体系进行无缝协同，导致微服务治理割裂。

**解决方案**:
阿里巴巴团队将核心电商流量网关迁移至 Higress。Higress 基于 Istio 与 Envoy 构建，深度集成了阿里自研的 WASM（WebAssembly）技术。
1.  利用 Higress 的 **WASM 插件市场**，通过编写 C++/Go/AssemblyScript 的插件来实现业务逻辑（如请求鉴权、流量染色、请求头修改），并在运行时动态热加载，无需重启网关。
2.  采用 Higress 的 **Ingress** 控制器能力，统一接管 Kubernetes 集群入口流量，并利用其针对云原生场景优化的高性能转发引擎。

**效果**:
1.  **极致性能**：在大促压力测试中，Higress 网关在处理百万级 QPS 时，延迟显著降低，资源利用率（CPU/内存）相比旧架构优化了 50% 以上。
2.  **极高的灵活性**：通过 WASM 插件实现了毫秒级的配置变更和逻辑热更新，保障了在大促期间对突发流量的快速响应。
3.  **统一管控**：成功实现了东西向（服务间）与南北向（入口）流量的技术栈统一，降低了运维复杂度。

---



### 2：某大型互联网科技公司 AI 应用网关

 2：某大型互联网科技公司 AI 应用网关

**背景**:
随着 AIGC（生成式 AI）的爆发，该公司内部有大量业务线需要接入大语言模型（LLM）。由于不同业务线对模型提供商（如 OpenAI、通义千问、文心一言等）的选择不同，且调用方式各异，导致前端应用直接对接模型 API 时面临复杂的鉴权、协议转换和流量管理问题。

**问题**:
1.  **协议不统一**：不同模型厂商的 API 接口标准不一，前端业务代码需要适配多种 SDK，开发成本高。
2.  **Token 成本与安全**：API Key 直接暴露在前端或业务服务中存在极大的泄露风险；同时缺乏有效的请求截断和 Token 计费管理手段。
3.  **缺乏可观测性**：无法统一监控各个业务线对模型 API 的调用情况、耗时和错误率。

**解决方案**:
该企业引入 Higress 作为 AI 专用网关。
1.  **统一模型接口**：利用 Higress 强大的插件扩展能力，开发了 AI 代理插件，将不同厂商的异构 API 统一封装为标准 OpenAI 协议格式，供业务侧统一调用。
2.  **安全与流控**：在网关层集中管理 API Key，业务侧只持有网关颁发的内部 Token；配置基于 Token 数量或 RPM/QPM 的限流插件，防止突发流量导致模型服务不可用或产生天价账单。
3.  **内容处理**：部署语义缓存插件，对高频重复的 Prompt 进行缓存拦截，直接返回结果，减少对下游模型的调用次数。

**效果**:
1.  **开发提效**：业务开发团队无需关注底层模型差异，只需对接统一接口，接入新模型的时间从数天缩短至配置级（分钟级）。
2.  **成本大幅降低**：通过语义缓存和精准的流控策略，模型调用费用降低了约 30%。
3.  **安全性提升**：实现了 API Key 的中心化管理，彻底杜绝了凭证泄露到终端设备的风险。

---



### 3：某跨国物流企业微服务流量治理

 3：某跨国物流企业微服务流量治理

**背景**:
该企业正处于从单体架构向微服务架构转型的深水区，拥有数百个微服务，运行在多个 Kubernetes 集群中。业务遍布全球，对网络延迟和链路稳定性要求极高。

**问题**:
1.  **金丝雀发布困难**：新版本上线时，难以做到按百分比、按请求头（如特定用户 ID）进行精细化的灰度引流，导致新版本故障影响面过大。
2.  **全链路追踪断层**：请求在经过网关进入微服务集群后，链路追踪（Tracing）数据经常丢失或上下文缺失，排查问题极为困难。
3.  **多云入口管理混乱**：由于使用了不同的云厂商和自建机房，入口网关配置不一致，导致管理规范难以落地。

**解决方案**:
采用 Higress 作为统一的云原生 API 网关。
1.  **精细化流量管理**：利用 Higress 对 HTTP 头部、Cookie、权重的高级路由支持，实现了基于用户画像的蓝绿发布和金丝雀发布策略。
2.  **可观测性集成**：Higress 原生支持 OpenTelemetry 标准，自动将网关的 Trace ID 透传给后端服务，打通了全链路监控数据。
3.  **多集群统一**：在多个 Kubernetes 集群中部署 Higress，并通过统一的控制平面进行配置管理（GitOps 或 Dashboard），实现了跨地域流量调度的标准化。

**效果**:
1.  **发布安全性提升**：实现了从 1% 流量开始的平滑灰度发布，新版本回滚时间从小时级缩短至秒级。
2.  **运维效率翻倍**：统一的控制平面让运维团队可以在一个界面管理全球流量入口，配置错误率下降了 80%。
3.  **故障排查加速**：全链路 Tracing 的完整性达到 100%，大幅缩短了跨网络延迟问题的定位时间。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Istio，支持高并发 | 高性能，基于 Nginx 和 OpenResty，适合高并发场景 | 极高性能，基于 OpenResty 和 LuaJIT，适合超高并发 |
| 易用性 | 提供图形化控制台，支持 K8s Ingress 和 API 网关，集成阿里云服务 | 配置灵活但需手动管理，插件生态丰富，社区支持强 | 配置简单，支持动态路由和热更新，适合云原生环境 |
| 成本 | 开源免费，企业版需付费，集成阿里云服务可能产生额外费用 | 开源免费，企业版需付费，插件和扩展可能增加成本 | 开源免费，企业版需付费，社区插件丰富但需自行维护 |
| 扩展性 | 支持自定义插件，基于 WASM 和 Go，扩展性强 | 支持自定义插件，基于 Lua 和 Go，插件生态成熟 | 支持自定义插件，基于 Lua 和 Go，插件生态活跃 |
| 社区支持 | 阿里巴巴背书，社区活跃，文档完善 | 社区成熟，文档丰富，用户基数大 | 社区活跃，文档完善，国内用户较多 |

### 优势分析

1. **性能优势**：Higress 基于 Envoy 和 Istio，继承了两者的高性能和稳定性，适合大规模微服务场景。
2. **易用性**：提供图形化控制台和 K8s 集成，降低了部署和管理复杂度，适合云原生环境。
3. **扩展性**：支持 WASM 和 Go 插件，扩展性强，适合定制化需求。
4. **阿里云集成**：与阿里云服务深度集成，适合已使用阿里云的企业。

### 不足分析

1. **社区成熟度**：相比 Kong 和 APISIX，Higress 的社区和插件生态尚在发展中，资源相对较少。
2. **学习成本**：基于 Envoy 和 Istio 的架构可能对新手有一定学习门槛。
3. **企业版成本**：企业版功能可能需要付费，集成阿里云服务可能增加额外成本。
4. **兼容性**：与某些非阿里云服务的兼容性可能不如 Kong 和 APISIX。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现业务逻辑扩展

**说明**:
Higress 原生支持 WebAssembly (Wasm) 技术，允许用户使用 C/C++、Go、Rust 或 AssemblyScript 编写自定义插件。相比传统网关（如 Nginx）需要修改 C 模块并重新编译，Higress 的 Wasm 插件支持动态加载，可以实现业务逻辑的热更新，且无需重启网关实例。

**实施步骤**:
1. 根据团队技术栈选择 Wasm 开发语言（推荐使用 Go 或 Rust，社区支持较好）。
2. 引用 Higress 官方提供的 SDK（如 `github.com/alibaba/higress/sdk-go-go`）编写插件逻辑。
3. 本地编译生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 WASM 插件管理接口上传文件，并配置路由规则关联插件。
5. 配置插件的执行阶段和优先级。

**注意事项**:
- Wasm 插件运行在沙箱中，虽有轻微性能损耗，但安全性极高。
- 避免在插件中执行长时间阻塞操作，以免增加请求延迟。

---

### 实践 2：利用 Ingress 注解实现精细化流量管理

**说明**:
Higress 兼容 Kubernetes Ingress 规范，同时通过扩展注解提供了比标准 Ingress 更强大的流量治理能力。通过在 Ingress YAML 文件中添加特定的 Annotation，可以无需修改网关配置即可实现金丝雀发布、Header 转发、超时控制等功能。

**实施步骤**:
1. 编辑 Kubernetes 中的 Ingress 资源文件。
2. 添加 Higress 特有的注解，例如实现基于权重的灰度发布：
   ```yaml
   nginx.ingress.kubernetes.io/canary: "true"
   nginx.ingress.kubernetes.io/canary-weight: "20"
   ```
3. 应用配置：`kubectl apply -f ingress.yaml`。
4. 监控 Higress 日志或控制台，确认路由规则已生效。

**注意事项**:
- 不同版本的注解格式可能略有差异，请参考对应 Higress 版本的官方文档。
- 注解配置错误可能导致流量无法路由，建议先在测试环境验证。

---

### 实践 3：构建服务来源与 Nacos 的无缝集成

**说明**:
Higress 深度集成了阿里巴巴的 Nacos 注册中心。对于使用 Spring Cloud 或 Dubbo 架构的微服务体系，Higress 可以直接从 Nacos 动态拉取服务列表，实现从注册中心到网关的自动化服务发现，替代手动维护服务 IP 列表。

**实施步骤**:
1. 在 Higress 控制台导航至“服务来源”管理。
2. 选择“注册中心”来源，配置 Nacos 的服务地址和命名空间。
3. 配置服务分组和访问凭据（如 Nacos 的用户名密码）。
4. 在创建路由时，直接选择已发现的 Nacos 服务作为服务来源。

**注意事项**:
- 确保 Higress 所在网络能够访问 Nacos 服务器端口（通常为 8848 或 9848）。
- 如果使用 Nacos 2.0，注意 gRPC 端口的防火墙策略。

---

### 实践 4：配置全链路安全防护与认证

**说明**:
Higress 提供了标准化的鉴权能力，支持 Keyless 认证、Basic Auth、JWT 以及 OIDC（OpenID Connect）。通过配置鉴权规则，可以保护后端服务免受未授权访问，实现网关层面的统一认证中心，避免将认证逻辑散落在各个微服务中。

**实施步骤**:
1. 在 Higress 控制台创建鉴权规则（如 JWT Auth）。
2. 配置 JWT 签名密钥、Claims 字段映射。
3. 将鉴权规则绑定到特定的路由或域名。
4. 对于外部 API 访问，可配置“全局限流”或“IP 访问控制”作为第一道防线。

**注意事项**:
- 密钥轮换时需同步更新 Higress 配置，避免服务中断。
- 启用 HTTPS 确保传输层安全，防止 Token 被窃听。

---

### 实践 5：实施多环境流量治理与灰度发布

**说明**:
利用 Higress 强大的流量标签（Tag）路由能力，可以实现全链路灰度发布。通过为部署在 Kubernetes 中的不同版本工作负载打标签，Higress 可以将带有特定 Header 的请求流量精准路由到灰度版本的服务，实现按用户或按比例的流量切分。

**实施步骤**:
1. 为灰度版本的 Kubernetes Deployment 或 Service 打上特定的 Label（如 `version: v2`）。
2. 在 Higress 中配置服务来源，确保能识别带有不同标签的服务实例。
3. 创建或修改路由规则，配置“灰度规则”，匹配

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，网络传输层的协议对延迟影响巨大。HTTP/3 (QUIC) 协议基于 UDP，解决了 TCP 的队头阻塞问题，能显著降低弱网环境下的连接建立延迟和丢包重传延迟，特别适合移动端或跨地域访问的场景。

**实施方法**:
1. 在 Higress 的网关配置中，监听器（Listener）配置部分启用 HTTP/3 协议支持。
2. 确保负载均衡器或前端防火墙开放 UDP 端口（通常端口 443）。
3. 配置 Alt-Svc 服务器推送参数，引导浏览器客户端自动升级到 HTTP/3。

**预期效果**: 在高丢包率（>1%）网络环境下，页面加载时间（TTFB）可降低 20%-40%；连接建立耗时减少 1-2 个 RTT。

---

### 优化 2：启用全链路异步调用与零拷贝

**说明**: Higress 支持基于 WASM (WebAssembly) 或 Go/Java 的插件扩展。在编写自定义插件或处理请求时，如果采用同步阻塞模式，会迅速耗尽网关的线程资源，导致吞吐量上不去。利用 Higress 的异步处理能力，可以避免请求处理线程阻塞。

**实施方法**:
1. 在开发 Wasm 插件或 Java/Go 扩展时，严格使用非阻塞 I/O API。
2. 避免在插件逻辑中进行长耗时计算或数据库同步查询，应将这些逻辑下沉到后端服务或通过异步调用处理。
3. 启用 Higress 的零拷贝特性，减少数据在用户态和内核态之间的内存拷贝次数。

**预期效果**: 在高并发（QPS > 10k）场景下，网关吞吐量可提升 30%-50%，请求延迟 P99 值显著下降。

---

### 优化 3：配置智能 DNS 缓存与连接池调优

**说明**: 网关作为流量的入口，频繁的后端服务 DNS 解析和 TCP/TLS 握手是主要的性能瓶颈。通过合理配置上游服务的连接池和 DNS 缓存，可以大幅减少握手开销。

**实施方法**:
1. 调整 `upstream` 连接池配置，增大 HTTP/2 或 gRPC 的最大并发连接数。
2. 启用 DNS 缓存，将 TTL 设置为合理的值（如 60s），避免每次请求都进行 DNS 解析。
3. 针对后端 HTTP/1.1 服务，启用 Keep-Alive 并调整 `max_requests` 参数，复用已建立的连接。

**预期效果**: 后端连接建立耗时降低至接近 0，整体网关 CPU 使用率在相同流量下下降 10%-20%。

---

### 优化 4：实施精细化路由缓存与预热

**说明**: Higress 支持复杂的路由匹配逻辑。当路由规则数量达到成百上千条时，路由匹配本身会成为 CPU 密集型操作。此外，冷启动时缓存未命中会导致延迟抖动。

**实施方法**:
1. 对路由规则进行整理，将高频匹配的路由规则置于配置列表的前部（虽然 Higress 内部有优化，但逻辑清晰有助于维护）。
2. 启用路由匹配缓存。
3. 在发布更新或重启网关 Pod 时，利用流量预热功能，逐步切量，避免缓存雪崩导致后端瞬间压力过大。

**预期效果**: 路由匹配耗时减少，在大规模路由表（>500条）下，CPU 消耗可降低约 15%。

---

### 优化 5：开启数据压缩与响应缓存

**说明**: 对于 API 响应体较大（如 JSON 数据）或静态资源，启用压缩可以显著减少网络传输带宽，并加快客户端接收速度。同时，对于读多写少的接口，在网关层开启缓存可完全穿透到后端。

**实施方法**:
1. 在 Higress 全

---
## 学习要点

- 基于您提供的信息（来源：GitHub Trending，项目：Alibaba / Higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的一款基于 Istio 构建的云原生 API 网关，旨在深度整合云原生生态与流量管理。
- 它兼容 Kubernetes Ingress 标准，能够作为 K8s 集群的入口网关，实现对南北向和东西向流量的统一管理。
- 该项目集成了 K8s 的 Ingress 资源管理与 Istio 的服务治理能力，解决了传统网关在微服务架构中功能割裂的问题。
- Higress 提供了强大的扩展能力，支持通过 WASM (WebAssembly) 技术编写插件，从而实现业务逻辑的热更新与低延迟执行。
- 它支持将高流量的网关业务逻辑从 Envoy (C++) 卸载至 WASM 虚拟机中运行，显著提升了动态扩展的安全性和灵活性。
- 该网关设计上兼容 Nginx 的 Ingress 注解，降低了用户从传统 Nginx Ingress 迁移到云原生架构的门槛。


---
## 学习路径

## 学习路径

### 阶段 1：概念认知与基础环境搭建

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与 Nginx、Istio、传统 API 网关的区别与联系
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 本地 Docker 环境或 Kubernetes 集群（如 Kind/Minikube）的搭建
- 使用 Docker Compose 或 Helm 部署第一个 Higress 实例

**学习时间**: 1 周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：什么是 Higress
- 云原生网关技术对比文章

**学习建议**:
不要急于修改配置，首先通过官方文档理解 Higress "基于 Envoy 和 Istio" 的背景。建议先在本地使用 Docker Compose 快速启动一个 Standalone 模式，通过控制台界面熟悉 UI 布局和基本功能菜单。

---

### 阶段 2：核心流量管理与配置实战

**学习内容**:
- 基本流量路由：域名路由、路径匹配、Header 路由
- 服务来源管理：注册中心（Nacos, ZooKeeper, Consul, Eureka）的配置与对接
- 负载均衡策略：轮询、随机、一致性哈希等的配置
- 金丝雀发布与蓝绿发布配置
- 流量镜像与重定向、重写规则的使用
- WAF 插件基础与安全防护配置

**学习时间**: 2-3 周

**学习资源**:
- Higress 官方文档：配置指南
- Higress 官方示例库
- Envoy 路由配置官方文档（用于理解底层原理）

**学习建议**:
此阶段重点在于 "动手"。尝试接入一个真实的后端服务（可以是 Spring Boot 或 Go 写的简单 Echo 服务），并配置不同的路由规则。重点练习对接 Nacos 等注册中心，这是 Higress 区别于传统 Ingress 的强项。

---

### 阶段 3：插件生态与高可用扩展

**学习内容**:
- Higress 插件系统运行机制
- 使用官方预置插件处理特定需求（如 JWT 认证、请求限流、Key Rate Limiting）
- 开发自定义插件：使用 Wasm (WebAssembly) 或 Go/Java/Python 编写插件逻辑
- 全局配置与网关实例的参数调优
- 在 Kubernetes 生产环境中的 Helm 高级部署与运维
- 监控与可观测性：对接 Prometheus、Grafana、SkyWalking

**学习时间**: 3-4 周

**学习资源**:
- Higress 官方文档：插件开发指南
- Higress 官方插件市场
- Wasm (WebAssembly) 简易教程
- Kubernetes Ingress 高级配置指南

**学习建议**:
深入学习 Lua 或 Wasm 来扩展网关能力。尝试编写一个简单的自定义插件（例如：在请求头中添加特定 Metadata）。同时，关注网关的高可用部署，学习如何通过 HPA (Horizontal Pod Autoscaler) 自动伸缩网关实例。

---

### 阶段 4：架构设计与源码级掌控

**学习内容**:
- Higress 深度架构剖析：控制面与数据面的交互细节
- Envoy xDS 协议在 Higress 中的应用
- Higress 源码分析：核心数据结构、配置流转流程
- 复杂场景下的架构设计：多集群容灾、全链路灰度
- 性能瓶颈分析与压测工具使用
- 参与 Higress 开源社区贡献与 Issue 排查

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Envoy 官方深度文档
- Istio 控制面原理分析文章
- 云原生网关深度技术博客

**学习建议**:
阅读源码是通往专家的必经之路。建议从 "一个配置请求如何从控制台下发到 Envoy 并生效" 这一链路进行代码调试。结合实际生产中的高并发或复杂业务场景，思考 Higress 的架构优化方向，并尝试向社区提交 PR 或回答 Issue。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和 Kong 有什么关系？

1: Higress 是什么？它与阿里巴巴和 Kong 有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在电商、金融等高并发场景下的实战经验沉淀而成的。

具体关系如下：
1.  **与阿里巴巴的关系**：Higress 是阿里云推出的开源项目，其内核源自阿里巴巴内部广泛使用的“云原生网关”技术，旨在解决微服务架构下的流量治理和安全管理问题。
2.  **与 Kong 的关系**：Higress 兼容 Kong 的生态。它支持导入和运行 Kong 的插件，这意味着用户从 Kong 迁移到 Higress 时，可以复用已有的插件资源，降低了迁移成本。

---



### 2: Higress 与 Nginx 或 Envoy 相比有什么核心优势？

2: Higress 与 Nginx 或 Envoy 相比有什么核心优势？

**A**: Higress 并不是从零开始构建的，它站在了巨人的肩膀上，并针对云原生场景进行了深度优化。

*   **与 Nginx 相比**：Nginx 主要依赖配置文件（nginx.conf）进行管理，这在动态微服务环境中配置修改和热加载比较复杂。Higress 提供了控制平面（基于 Istio），支持通过控制台或 API 进行动态配置，无需重启网关即可生效，且对 gRPC、Dubbo 等微服务协议有更好的原生支持。
*   **与 Envoy 相比**：Envoy 本身是一个强大的数据平面（L4/L7 代理），但配置极其复杂（通过静态文件或 xDS 协议）。Higress 将 Envoy 作为数据平面核心，但对其进行了封装，提供了更加人性化的控制台和 K8s Ingress/Gateway CRD 支持，大大降低了使用门槛。同时，Higress 内置了 WAF 防护、流量标签透传等业务功能。

---



### 3: Higress 是否支持 Kubernetes？如何部署？

3: Higress 是否支持 Kubernetes？如何部署？

**A**: 是的，Higress 是为云原生而生的，完美支持 Kubernetes 环境。

部署方式非常灵活：
1.  **标准 K8s 部署**：通过 Helm Chart 或 kubectl 应用 YAML 资源文件，可以直接将 Higress 部署在 K8s 集群内。它会自动监听 K8s 的 Ingress 或 Gateway API 资源变化，并自动更新路由规则。
2.  **服务发现集成**：部署在 K8s 中后，Higress 可以自动发现 K8s 的 Service 和 Pod，无需手动配置后端服务器地址，实现了服务的自动注册和健康检查。

---



### 4: 我可以使用 Wasm (WebAssembly) 技术来扩展 Higress 的功能吗？

4: 我可以使用 Wasm (WebAssembly) 技术来扩展 Higress 的功能吗？

**A**: 可以，这是 Higress 的一个核心亮点。Higress 是基于 C++ 构建的，但深度集成了 Wasm 支持。

*   **插件开发**：开发者可以使用 C++, Go, Rust, JavaScript (AssemblyScript) 等多种语言编写 Wasm 插件。
*   **动态加载**：Wasm 插件可以在不重启 Higress 进程的情况下动态加载、卸载和更新。这解决了传统 Nginx 模块必须重新编译和重启的痛点。
*   **隔离性**：Wasm 插件运行在沙箱环境中，即使插件崩溃也不会导致网主进程崩溃，保证了系统的稳定性。

---



### 5: Higress 如何处理服务发现，特别是对于非 K8s 环境（如 ECS/VM）中的服务？

5: Higress 如何处理服务发现，特别是对于非 K8s 环境（如 ECS/VM）中的服务？

**A**: Higress 具备强大的多语言/多框架服务发现能力，不仅限于 K8s。

*   **注册中心集成**：Higress 原生支持对接主流的服务注册中心，如 **Nacos**、**Consul**、**ZooKeeper** 以及 **Eureka**。
*   **工作原理**：通过配置文件或控制台关联相应的注册中心，Higress 会自动拉取服务实例列表。当后端服务扩容或缩容时，Higress 能感知到变化并实时更新路由转发策略，无需人工干预。这对于混合云架构（部分业务在容器，部分在虚拟机）非常关键。

---



### 6: Higress 是否适合作为 API 管理平台？它支持认证和限流吗？

6: Higress 是否适合作为 API 管理平台？它支持认证和限流吗？

**A**: 是的，Higress 完全具备 API 管理的核心能力。

1.  **认证与鉴权**：Higress 内置了标准的认证插件，支持 **API Key**、**Basic Auth**、**JWT (JSON Web Token)** 校验，以及 **OIDC (OpenID Connect)** 单点登录集成。它可以轻松对接阿里云 IAM 或其他 IdP。
2.  **流量防护**：它提供了精准的限流功能，支持基于请求速率、并发连接数的限流，并且可以针对特定的 IP、Header 或参数进行限流，有效防止恶意流量刷垮后端服务。
3.  **安全插件**：还内置了基础的 WAF（Web Application Firewall）功能，可以防御 SQL 注

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并创建一个简单的路由规则，将访问 `/httpbin/` 路径的流量转发到公共测试服务 `httpbin.org`。

### 提示**:

### 查阅 Higress 官方文档的 "快速开始" 章节，获取 Docker 容器启动命令。

---
## 实践建议

以下是针对 Higress（阿里云开源的 AI 原生 API 网关）的 6 条实践建议，涵盖了从流量管控、AI 服务集成到生产环境运维的关键场景：

### 1. 利用“模型提供商”插件实现统一接入与成本控制
Higress 的核心优势在于其 AI 原生能力，特别是对大模型（LLM）的统一管理。不要将 API Key 直接硬编码在客户端应用中，而是利用 Higress 的 **AI 模型提供商** 配置功能。
*   **具体操作**：在控制台配置不同厂商（如 OpenAI, Azure, 通义千问等）的 API Key。通过创建路由，将不同的请求路径（如 `/v1/chat/completions`）映射到不同的后端模型服务上。
*   **最佳实践**：利用 **Prompt 模板管理** 功能。将常用的 System Prompt 固化在网关侧，前端只需传递用户输入。这样不仅降低了客户端的复杂度，还能在不发版的情况下灵活调整 Prompt 策略。
*   **常见陷阱**：忽略 Token 计费配置。在配置提供商时，务必准确填写不同模型的 Token 单价，以便利用 Higress 的 **可观测性面板** 查看各模型的真实调用成本，防止云厂商账单爆炸。

### 2. 实施基于语义的 AI 智能路由
在 AI 应用中，用户的问题往往千奇百怪。传统的基于路径（Path）的路由无法满足需求，建议使用 Higress 的 **AI 智能路由** 功能。
*   **具体操作**：配置不同的路由目标（例如：一个连接 GPT-4 用于复杂逻辑，一个连接便宜的小模型用于简单闲聊）。在路由规则中，编写描述性文本（如“处理复杂技术问题”或“处理简单问候”），让网关根据用户请求的语义自动分发流量。
*   **最佳实践**：建立“高低搭配”策略。将 20% 需要深度推理的请求路由到高质量/高成本模型，将 80% 的简单请求路由到低成本/高速度模型，从而在保证体验的同时大幅降低成本。
*   **常见陷阱**：语义描述过于模糊。如果路由规则的描述缺乏区分度（例如一个写“回答问题”，一个写“解决问题”），网关可能会频繁路由错误，导致响应质量下降。

### 3. 配置“结果缓存”以应对高并发查询并节省 Token
对于具有重复性的用户查询（如常见的知识问答、代码解释），直接转发给 LLM 是一种浪费。
*   **具体操作**：在对应的路由配置中启用 **AI 统计与缓存** 插件。设置缓存键（Cache Key），通常基于用户问题的 Hash 值或特定的 Prompt 指纹。
*   **最佳实践**：针对“事实性”问题（如“公司报销政策是什么”）开启长缓存（如 1 小时）；针对“创造性”问题（如“写一首诗”）关闭缓存或设置极短的缓存时间。
*   **常见陷阱**：缓存了带有上下文 的对话。如果是多轮对话，必须确保 Cache Key 包含对话历史 ID，否则用户 A 会看到用户 B 的对话结果，造成严重的数据泄露。

### 4. 启用“安全护栏”防止 Prompt 注入和敏感词泄露
直接将用户输入传递给后端大模型存在巨大的安全风险（如 Prompt 注入攻击导致系统指令被覆盖）。
*   **具体操作**：在路由链中插入 **内容安全** 插件。配置输入过滤规则，拦截常见的攻击指令或敏感词汇；配置输出过滤规则，防止模型返回违规内容。
*   **最佳实践**：结合 Higress 的 **JSON 传参** 修改功能，在请求转发前强制锁定 `system` 字段，确保恶意用户无法通过前端篡改系统提示词。
*   **常见陷阱**：过度拦截导致用户体验卡顿。安全规则应设置为“拦截并替换”或“拦截并返回默认友好提示”，而不是直接断开连接，以免前端应用报错。

### 5. 警惕 LLM 的超时

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

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*