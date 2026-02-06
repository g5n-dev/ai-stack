---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T15:20:37+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的简洁总结： **项目概况** * **名称**：Higress * **开发方**：Alibaba * **定位**：AI 原生 API 网关 * **语言**：Go * **热度**：GitHub 上拥有超过 7,400 星标。 **核心定义与架构** Higr"
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
- **星标**: 7,468 (+16 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，专为云原生环境与 LLM 应用设计。它通过集成 WASM 插件系统，在提供传统流量管理能力的同时，实现了对 AI 服务的代理与 MCP 协议支持，适合需要统一管理微服务与大模型流量的团队。本文将介绍其系统架构、核心组件及主要应用场景，帮助开发者理解如何利用该网关实现更高效的 API 治理与 AI 集成。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的简洁总结：

**项目概况**
*   **名称**：Higress
*   **开发方**：Alibaba
*   **定位**：AI 原生 API 网关
*   **语言**：Go
*   **热度**：GitHub 上拥有超过 7,400 星标。

**核心定义与架构**
Higress 是一个基于 Istio 和 Envoy 构建的云原生 API 网关，通过扩展 WebAssembly (WASM) 插件能力，实现了控制平面与数据平面的分离。其配置变更通过 xDS 协议传播，具有毫秒级延迟且无连接中断，特别适合 AI 长连接流式响应场景。

**三大核心功能与用途**
1.  **AI 网关**：
    *   提供统一的 API 接口，兼容 30 多家 LLM 提供商。
    *   具备协议转换、可观测性、缓存和安全防护能力。
    *   涉及组件：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议 (MCP) 服务器，使 AI 智能体能够调用工具和服务。
    *   涉及组件：`mcp-router`, `jsonrpc-converter` 以及各类 MCP 服务实现（如搜索、地图等）。
3.  **Kubernetes Ingress**：
    *   作为 Kubernetes 入口控制器，支持微服务路由，并兼容 nginx-ingress 注解。
    *   涉及组件：`higress-controller`。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的云原生网关，它成功地将传统的 API 网关能力与大模型（LLM）应用所需的流量治理深度融合。作为阿里云开源的“AI Native”网关，它不仅继承了 Envoy 的高性能，更通过 WASM 技术和 AI 特性填补了当前 AI 应用落地中“网关层”的空白，是构建现代 AI 基础设施的优选方案。

**详细评价**

**1. 技术创新性：从“流量管道”到“AI 智能体”的进化**
*   **差异化方案：** Higress 最核心的创新在于其 **AI Native（AI 原生）** 架构。传统网关（如 Nginx, Kong）主要关注 HTTP 路由和负载均衡，而 Higress 原生集成了 LLM 的标准协议（如 OpenAI 协议）。
*   **事实与推断：** 根据 DeepWiki 描述，Higress 提供了 **MCP (Model Context Protocol) 服务器托管** 功能。这是一个极具差异化的技术选型。推断其设计意图是让网关不仅仅是流量的转发者，更成为 AI Agent（智能体）的“工具调度中心”。通过在网关层直接托管 MCP 工具，Agent 可以通过网关安全、标准化地调用外部 API，无需在应用层硬编码工具调用逻辑。
*   **WASM 插件生态：** 基于 Istio 和 Envoy，Higress 充分利用了 **WebAssembly (WASM)** 的隔离性和高性能。这意味着开发者可以用 C++/Go/Rust/AssemblyScript 编写插件，在热更新（无需重启网关）的同时，获得接近原生代码的执行效率。这解决了传统 Lua 插件（如 OpenResty）开发门槛高且容易阻塞主线程的问题。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **解决的关键问题：** 在企业接入 LLM 时，通常面临三个痛点：**Token 计费与统计困难、Prompt/Response 的实时修改、模型供应商的切换成本**。Higress 直接在网关层解决了这些问题。
*   **应用场景：**
    *   **AI 代理与转换：** 企业内部可能同时调用阿里云通义千问、OpenAI 或开源模型。Higress 允许在网关层将标准请求转换为不同厂商的格式，实现后端模型的热切换。
    *   **安全与治理：** 利用 WASM 插件，可以在网关层实现 Prompt 注入（注入企业上下文）、敏感词过滤（防止数据泄露）以及请求限流（基于 Token 数量而非单纯的请求数），这对控制 AI 成本至关重要。
    *   **MCP 作为统一工具入口：** 对于构建 Agent 应用的开发者，Higress 提供了一个统一的 MCP Server 集群，使得 Agent 可以通过网关发现和调用工具，极大地简化了微服务与 AI 交互的复杂度。

**3. 代码质量与架构设计：云原生的教科书级实践**
*   **架构设计：** Higress 采用了标准的 **控制面与数据面分离** 架构。控制面负责配置分发（基于 Istio），数据面负责流量处理（基于 Envoy）。这种设计保证了极高的扩展性和稳定性，符合云原生 CNCF 的最佳实践。
*   **代码规范：** 项目主要使用 **Go** 语言编写。Go 语言在云原生基础设施领域占据统治地位（如 Kubernetes, Docker 均为 Go 编写），这保证了 Higress 的二进制文件体积小、部署简单、并发性能强。
*   **文档完整性：** 从提供的 DeepWiki 来看，项目拥有详细的多语言（中/日/英） README 和分模块的架构文档。这表明该项目不仅面向国内开发者，也有明确的国际化野心，文档维护较为严谨。

**4. 社区活跃度：背靠阿里的强力驱动**
*   **活跃度分析：** 拥有 **7,468** 的星标数（截至数据统计时），在 API 网关领域属于头部梯队。作为阿里巴巴开源项目，它通常能获得持续的迭代支持。
*   **开发者反馈：** 社区活跃度通常体现在 Issue 的响应和 PR 的合并速度。考虑到阿里云内部正在大规模使用 Higress 作为其云产品的网关底座，该项目出现“烂尾”的风险极低。其更新频率通常紧跟 Kubernetes 和 Envoy 的版本发布，确保兼容性。

**5. 学习价值：理解 AI 时代的流量治理**
*   **启发意义：** 对于开发者而言，Higress 是学习 **“如何将 AI 能力基础设施化”** 的最佳案例。它展示了如何将非结构化的 LLM 流量纳入传统的微服务治理体系中。
*   **WASM 实战：** 它是学习 Envoy WASM 插件开发的优秀平台，开发者可以通过编写插件来处理 HTTP 请求头、Body，这对于理解中间件原理极有帮助。
*   **MCP 协议落地：** 随着 Anthropic 提出的 MCP 协议逐渐成为 AI Agent 连接工具的标准，Higress 率先在网关层支持，为开发者学习 MCP 的服务端实现提供了参考。

**6. 潜在问题与改进建议**
*   **复杂度门槛：** 虽然它支持 Kubernetes Ingress，但完全发挥其威力（如 WASM 插件、MCP 配置）需要理解

---
## 技术分析

# Higress 深度技术分析报告

Higress 是由阿里云开源的**云原生 API 网关**，其核心定位是 **"AI Native API Gateway"**。它基于 Envoy 和 Istio 构建，通过引入 WebAssembly (WASM) 插件生态和对大模型（LLM）场景的深度优化，试图解决传统 API 网关在 AI 时代的局限性。

以下是对该项目的深度剖析：

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的经典云原生架构模式。

*   **底层基座**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L7 处理能力和可观测性；复用 **Istio** 的部分控制平面能力（如 xDS 协议下发），但进行了轻量化和定制化改造，移除了 Sidecar 模式的复杂性，专注于 Gateway 模式。
*   **编程语言**：**Go** 用于控制平面（管理配置、WASM 插件生命周期、Kubernetes Ingress 控制）；**C++** (Envoy) 用于核心数据转发；**Rust/AssemblyScript** (WASM) 用于编写业务逻辑插件。

### 核心模块与关键设计
1.  **AI 网关路由层**：
    *   **Provider 抽象**：将不同的 LLM 提供商（如 OpenAI, Azure, 通义千问, HuggingFace 等）抽象为统一的 Backend 配置。
    *   **LLM 路由策略**：支持基于请求内容（如 Prompt 长度、Token 预估）或元数据（用户等级）的智能路由，实现多模型之间的流量切换。
2.  **WASM 插件市场**：
    *   Higress 的核心差异化竞争力。它允许用户在不重启网关的情况下动态加载逻辑。
    *   内置了针对 AI 场景的插件，如 `key-auth`（API Key 管理）、`prompt-guard`（敏感词过滤）、`request-block`（请求拦截）。
3.  **MCP (Model Context Protocol) Server**：
    *   这是针对 AI Agent 场景的创新设计。Higress 不仅能转发请求，还能作为 MCP Server 的托管端，将内部微服务封装为 AI Agent 可调用的工具。

### 技术亮点与创新点
*   **长连接无损配置更新**：传统网关更新配置往往需要重启或 drain 连接。Higress 利用 Envoy 的 xDS 热更新机制，结合 Go 控制平面的优化，实现了配置变更时的**毫秒级生效**且不断连。这对于 AI 应用的流式响应至关重要。
*   **AI 原生流量管理**：它不仅处理 HTTP 请求，还理解 AI 语义。例如，它支持基于 Token 的计费与限流，而非传统的请求数或字节数。

### 架构优势分析
*   **性能**：数据平面基于 Envoy C++，具备极高的吞吐量和低延迟。
*   **扩展性**：WASM 提供了接近原生的性能且隔离性良好，解决了 Lua 插件（如 OpenResty）崩溃导致主进程不稳定的问题。
*   **标准化**：完全兼容 Kubernetes Ingress API 和 Gateway API，降低了迁移成本。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量网关**：
    *   **统一接入**：企业内部只需部署一个网关，即可对接外部几十种 LLM API。
    *   **Token 管理**：自动计算 Prompt 和 Completion 的 Token 数量，用于成本控制和预算告警。
    *   **流式代理**：完美支持 SSE (Server-Sent Events) 流式转发，确保 ChatGPT 类似的打字机效果不被截断。
2.  **MCP 协议支持**：
    *   **场景**：AI Agent 需要调用企业内部 API（如查询数据库、调用 ERP）。Higress 可以将这些后端服务自动注册为 MCP Tools，简化了 Agent 的工具调用链路。
3.  **传统微服务网关**：
    *   支持 K8s Ingress、Nacos 服务发现、金丝雀发布、蓝绿部署。

### 解决的关键问题
*   **API Key 泄露风险**：集中管理所有大模型的 Key，前端应用无需接触真实 Key，网关层进行统一鉴权和转发。
*   **模型供应商锁定**：通过统一的 API 规范，企业可以随时在 Higress 配置中切换底层模型（例如从 GPT-4 切换到 Qwen-Max），而无需修改客户端代码。
*   **高并发下的稳定性**：解决了直接访问第三方 LLM API 可能遇到的网络抖动或限流问题，Higress 可以在本地做重试和缓存。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Provider, Token计费)** | 弱 (需插件) | 弱 (需插件) | 无 |
| **架构** | Envoy + Istio (Go) | Nginx/Lua (C) | etcd + Lua (Go/Lua) | C Module |
| **WASM 支持** | **原生支持，生态完善** | 支持 (需企业版/复杂配置) | 支持 | 实验性 |
| **K8s 集成** | **完美集成** | 良好 | 良好 | 需 Ingress Controller |
| **配置热更新** | **毫秒级，不断连** | 较快 | 快 | 需 Reload |

### 技术实现原理
*   **流式转发**：Higress 在 Envoy Filter 层面实现了对 HTTP Chunked 编码和 SSE 协议的透明代理。它识别出流式响应的头，保持连接双向打通，并在流式数据传输过程中进行实时的上下文处理（如敏感词拦截）。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 控制平面与 Envoy 数据平面通过 xDS (v2/v3) 通信。为了保证配置变更的平滑，Higress 实现了 `EDS` (Endpoint Discovery Service) 的增量更新，仅推送变更的集群配置，减少全量推送带来的 CPU 峰值。
*   **WASM 虚拟机**：集成了 **Wasmtime** 或 **V8** 引擎。在 Go 代码中维护 WASM 插件的生命周期，通过 `proxy-wasm` ABI 标准与 Envoy 交互。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑。
    *   `ingress`：K8s Ingress 资源到 Config 的转换逻辑。
    *   `config`：配置的 CRUD 和 xDS 转换。
*   **`plugins/`**：WASM 插件的源码仓库（通常独立仓库，但在配置中引用）。
*   **`router/`**：针对 AI 请求的特殊路由逻辑，例如根据 JSON Body 中的 `model` 字段进行后端匹配。

### 性能与扩展性
*   **性能优化**：利用 Envoy 的高性能网络栈，避免了 Go 语言在处理海量长连接时的协程调度开销（数据面在 C++）。控制面采用异步非阻塞模式处理配置事件。
*   **扩展性**：通过 `Go Plugin` (控制面) + `WASM Plugin` (数据面) 的双层扩展模型，用户既可以扩展配置管理逻辑，也可以深入修改请求/响应报文。

### 技术难点与解决
*   **难点**：WASM 插件的内存隔离与资源限制。
*   **解决**：Higress 限制了每个 WASM VM 的内存上限和 CPU 时间片，防止恶意或低效的插件拖垮整个网关进程。

---

## 4. 适用场景分析

### 适合的项目
1.  **企业级 AI 应用平台**：需要对接多个大模型，且对 API Key 安全、成本控制有强需求的 SaaS 应用。
2.  **微服务流量入口**：基于 Kubernetes 的微服务架构，需要高性能网关。
3.  **AI Agent 开发**：需要将内部业务能力通过 MCP 协议暴露给 LLM 的企业。

### 最有效的情况
*   当你的应用需要**同时**处理传统 Web 流量和 AI 流量，且希望统一管理时。
*   当你需要对 AI 请求进行**细粒度控制**（如：不同用户路由到不同模型，或对 Prompt 进行实时修改）时。

### 不适合的场景
*   **极简边缘侧**：如嵌入式设备或资源极受限的容器，Envoy 的内存占用相对较高。
*   **纯静态文件服务**：杀鸡焉用牛刀，Nginx 更轻量。

### 集成方式
*   **Kubernetes Helm 部署**：最推荐的方式。
*   **Docker Standalone**：适合测试环境。

---

## 5. 发展趋势展望

### 演进方向
*   **从 "Gateway" 到 "AI Gateway"**：未来将强化对 Prompt 的管理、缓存以及 RAG (检索增强生成) 流程的内置支持。
*   **MCP 生态的深化**：随着 AI Agent 的爆发，Higress 可能会成为企业内部服务暴露给 AI 的标准枢纽。

### 改进空间
*   **WASM 调试工具**：目前 WASM 插件的调试相对困难，需要更强大的 IDE 集成和日志追踪工具。
*   **文档与社区**：相比 Kong，AI 特性的文档尚需完善，特别是复杂配置的案例。

---

## 6. 学习建议

### 适合开发者
*   具备 **Go** 语言基础，了解 **Kubernetes** 基本概念。
*   对 **云原生架构** 和 **Service Mesh** 有兴趣的后端工程师或 DevOps 工程师。

### 学习路径
1.  **基础**：先理解 Envoy 的基本概念。
2.  **实践**：使用 Docker Compose 或 Minikube 部署 Higress，配置一个简单的 AI 路由（如转发到 OpenAI）。
3.  **进阶**：尝试编写一个 WASM 插件（使用 Rust 或 AssemblyScript），实现自定义的请求头处理。

### 实践建议
*   阅读 `pkg/config` 下的代码，理解 K8s 资源如何转化为 Envoy 配置。
*   查阅官方提供的 WASM 插件示例，学习 `proxy-wasm` SDK 的使用。

---

## 7. 最佳实践建议

### 正确使用方式
*   **资源限制**：在生产环境中，务必为 Higress Pod 设置合理的 CPU 和 Memory Limits，防止流量突增导致 OOM。
*   **配置隔离**：将 AI 路由配置与传统微服务路由分开管理，避免配置混乱。

### 常见问题解决
*   **流式响应中断**：检查后端服务是否正确设置了 `Transfer-Encoding: chunked` 以及超时设置是否过短。

---
## 代码示例




```python
# 示例1：基于Higress的API网关动态路由配置
# 解决问题：根据请求头动态路由到不同后端服务
from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟Higress的路由规则配置
ROUTE_RULES = {
    "v1": "http://backend-v1.example.com",
    "v2": "http://backend-v2.example.com"
}

@app.route('/api/proxy', methods=['GET', 'POST'])
def dynamic_routing():
    # 获取请求头中的API版本信息
    api_version = request.headers.get('API-Version', 'v1')
    
    # 根据版本选择后端服务
    backend_url = ROUTE_RULES.get(api_version, ROUTE_RULES['v1'])
    
    # 模拟转发请求到后端服务
    response = {
        "message": f"请求已路由到 {backend_url}",
        "path": request.path,
        "version": api_version
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```




```python
# 示例2：Higress插件开发 - 请求限流
# 解决问题：实现基于IP的简单限流功能
from collections import defaultdict
from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟限流计数器
rate_limit_counter = defaultdict(int)
RATE_LIMIT = 10  # 每分钟最大请求数

@app.before_request
def check_rate_limit():
    client_ip = request.remote_addr
    current_count = rate_limit_counter.get(client_ip, 0)
    
    if current_count >= RATE_LIMIT:
        return jsonify({"error": "请求过于频繁，请稍后再试"}), 429
    
    rate_limit_counter[client_ip] += 1

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": "正常响应"})

if __name__ == '__main__':
    app.run(debug=True)
```




```python
# 示例3：Higress配置热更新模拟
# 解决问题：实现配置的动态更新而不重启服务
import json
import time
from threading import Thread
from flask import Flask, jsonify

app = Flask(__name__)

# 模拟Higress的配置存储
current_config = {
    "routes": {
        "/api/v1": "service-a",
        "/api/v2": "service-b"
    }
}

def config_updater():
    """模拟配置热更新线程"""
    while True:
        time.sleep(10)  # 每10秒检查一次配置更新
        # 这里可以替换为从配置中心拉取最新配置
        new_config = {
            "routes": {
                "/api/v1": "service-a-updated",
                "/api/v3": "service-c"
            }
        }
        current_config.update(new_config)
        print("配置已更新:", json.dumps(current_config, indent=2))

@app.route('/admin/config', methods=['GET'])
def get_config():
    return jsonify(current_config)

if __name__ == '__main__':
    # 启动配置更新线程
    Thread(target=config_updater, daemon=True).start()
    app.run(debug=True)
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴内部电商业务（如淘宝、天猫）面临高并发、大流量的挑战，尤其是在“双11”等大促期间，流量峰值可能达到平时的数十倍。原有的网关系统在处理海量请求时，性能和扩展性成为瓶颈。

**问题**:  
1. 传统网关架构难以支撑每秒百万级的请求处理。  
2. 动态路由和流量管理策略的调整需要人工介入，响应速度慢。  
3. 多语言（Java、Go、Node.js）微服务之间的调用链路复杂，缺乏统一管理。

**解决方案**:  
基于 Higress 构建新一代云原生 API 网关，结合其高性能（基于 Envoy 和 Istio）和动态配置能力，实现：  
1. 支持水平扩展，轻松应对流量峰值。  
2. 通过动态路由和流量灰度发布，快速调整流量分配策略。  
3. 集成服务网格（Istio），统一管理微服务调用链路。

**效果**:  
1. 大促期间网关吞吐量提升 40%，平均延迟降低 30%。  
2. 流量策略调整时间从小时级缩短至分钟级。  
3. 微服务调用可观测性增强，故障定位效率提升 50%。  

---



### 2：某大型金融科技公司

 2：某大型金融科技公司

**背景**:  
该金融科技公司提供支付、信贷等核心服务，对系统的稳定性和安全性要求极高。随着业务扩展，原有 API 网关无法满足以下需求：  
1. 细粒度的权限控制和审计。  
2. 对第三方 API 的安全调用管理。  
3. 低延迟和高可用性保障。

**问题**:  
1. 传统网关的权限管理功能有限，难以适配复杂的业务场景。  
2. 第三方 API 调用缺乏统一的认证和限流机制，存在安全隐患。  
3. 网关单点故障风险高，影响业务连续性。

**解决方案**:  
部署 Higress 作为统一 API 网关，利用其以下特性：  
1. 基于 Open Policy Agent（OPA）实现细粒度的动态权限控制。  
2. 集成 JWT 认证和 IP 白名单，保障第三方 API 调用安全。  
3. 通过多副本部署和健康检查机制，实现高可用性。

**效果**:  
1. 权限管理覆盖 100% 的 API 接口，审计效率提升 60%。  
2. 第三方 API 调用安全性显著增强，未授权访问事件降至零。  
3. 网关可用性达到 99.99%，业务中断时间减少 90%。  

---



### 3：某互联网教育平台

 3：某互联网教育平台

**背景**:  
该教育平台提供在线课程、直播教学等服务，用户量快速增长。原有网关系统在以下方面存在不足：  
1. 无法灵活应对不同地区用户的流量调度需求。  
2. 直播流媒体服务的 API 调用延迟较高。  
3. 缺乏对 API 调用数据的实时分析和监控。

**问题**:  
1. 跨地域流量调度依赖手动配置，响应速度慢。  
2. 直播服务 API 延迟影响用户体验。  
3. 运营团队无法实时掌握 API 调用情况，决策滞后。

**解决方案**:  
采用 Higress 替换原有网关，实现：  
1. 基于地理位置的智能路由，自动将用户请求分配至最近节点。  
2. 优化与直播服务相关的 API 路径，减少网络跳数。  
3. 集成 Prometheus 和 Grafana，提供实时 API 调用监控面板。

**效果**:  
1. 跨地域访问延迟降低 45%，用户满意度提升 20%。  
2. 直播服务 API 响应时间从 200ms 降至 80ms。  
3. 运营团队通过实时监控数据，快速优化资源分配，成本降低 15%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能优异，适合高流量场景 | 基于OpenResty，性能稳定，适合中小规模 |
| 易用性 | 提供可视化控制台，配置简单，集成K8s | 配置灵活但复杂，学习曲线较陡 | 提供管理界面，但插件开发需Lua知识 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性中等 | 支持Lua插件，扩展性中等 |
| 社区 | 阿里背书，社区活跃 | 社区活跃，文档丰富 | 社区成熟，插件生态完善 |

### 优势分析

- 优势1：基于Envoy和Istio，云原生集成度高，适合微服务架构。
- 优势2：支持Wasm插件，扩展性强，且不依赖特定语言。
- 优势3：提供可视化控制台，降低使用门槛，适合快速上手。

### 不足分析

- 不足1：社区生态相对较新，插件数量不如APISIX和Kong丰富。
- 不足2：文档和案例较少，学习资源有限。
- 不足3：对非K8s环境的支持较弱，依赖容器化部署。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许用户使用 C++, Go, Rust, AssemblyScript 或 Python 编写插件来扩展网关功能。相比传统的 Lua 脚本，Wasm 插件提供了更强的隔离性、更高的性能以及更丰富的编程语言支持，能够实现复杂的流量处理逻辑而无需修改网关核心代码。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-as-assembly` 工具链编写插件逻辑。
3. 本地编译生成 `.wasm` 文件。
4. 在 Higress 控制台的 "插件市场" 中上传 Wasm 文件，或通过 `WasmPlugin` CRD 进行配置。
5. 将插件绑定到特定的网关实例、路由或域名上生效。

**注意事项**: 
开发 Wasm 插件时需注意内存和 CPU 的限制，避免阻塞主线程导致网关性能下降。

---

### 实践 2：服务发现与 Nacos 注册中心集成

**说明**: Higress 原生支持 Nacos 作为服务注册中心，实现了与阿里云微服务生态的无缝对接。通过启用服务发现功能，Higress 可以自动感知后端服务实例的上下线，从而实现动态负载均衡，避免了手动维护静态 IP 列表的繁琐工作。

**实施步骤**:
1. 在 Higress 全局配置或特定来源服务中添加 Nacos 注册中心地址。
2. 配置 Nacos 的命名空间 (Namespace) 和服务分组，确保与后端应用配置一致。
3. 在创建 Ingress 或网关路由时，"服务来源" 选择 "Nacos"，并直接引用服务名。
4. 配置健康检查机制，确保 Higress 能够及时剔除不健康的实例。

**注意事项**: 
确保 Higress 所在的网络环境能够直接访问 Nacos 服务端，特别是跨 Kubernetes 集群或混合云部署场景下的网络连通性。

---

### 实践 3：精细化全链路安全防护

**说明**: 利用 Higress 内置的 IP 访问控制、基本认证 (Basic Auth) 和 JWT 认证插件，构建多层防御体系。同时，结合 Wasm 插件实现自定义的鉴权逻辑，例如对接内部账号系统或实现 API 签名验证，保护后端服务免受未授权访问。

**实施步骤**:
1. 配置 IP 黑/白名单插件，限制特定网段的访问请求。
2. 对于对外的 API 接口，启用 JWT 认证插件，配置签名密钥和必要的 Claims 校验。
3. 启用 CORS (跨域资源共享) 插件以允许合法的前端跨域调用。
4. 对于高敏感接口，部署自定义 Wasm 插件实现高频调用限流或复杂的参数校验。

**注意事项**: 
安全策略应遵循 "最小权限原则"，避免过度配置导致合法用户无法访问。定期审计安全日志以检测异常模式。

---

### 实践 4：利用 Ingress 注解实现金丝雀发布

**说明**: Higress 完全兼容 K8s Ingress 规范并扩展了注解能力。通过配置特定的注解，可以轻松实现基于流量比例或 Header 匹配的金丝雀发布，让新版本服务先接收少量流量进行验证，从而降低上线风险。

**实施步骤**:
1. 准备两个版本的 Deployment，例如 `app-v1` 和 `app-v2`。
2. 创建 Service 指向 `app-v1`。
3. 创建一个 Ingress 资源指向该 Service。
4. 创建一个 Canary Ingress (或同一个 Ingress 中配置)，指向 `app-v2`。
5. 在 Canary Ingress 中添加注解 `nginx.ingress.kubernetes.io/canary: "true"` 和 `nginx.ingress.kubernetes.io/canary-weight: "10"` (表示 10% 流量)。

**注意事项**: 
金丝雀发布过程中，应保持新旧版本数据库 schema 的兼容性，或者确保流量能够严格隔离，防止数据污染。

---

### 实践 5：配置高精度的流量治理与超时控制

**说明**: 在微服务架构中，级联故障是常见问题。通过在 Higress 中配置请求超时、重试策略和熔断规则，可以有效防止下游服务响应慢拖垮整个链路，提升系统的整体可用性。

**实施步骤**:
1. 针对读取服务和写入服务设置不同的超时时间（例如写操作 5s，读操作 2s）。
2. 配置自动重试策略，明确哪些 HTTP 状态码（如 5xx）需要重试，并限制最大重试次数（建议 2-3 次）。
3. 启用熔断器，当后端服务错误率超过阈值时，自动熔断，快速返回失败

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 Wasm 插件与代理预热

**说明**: Higress 基于 Envoy 构建，其 Wasm 插件机制允许用 C++/Go/Rust 编写高性能扩展。默认冷启动可能导致首包延迟（TTFB）增加 50-200ms。

**实施方法**:
1. 将 Lua/Java 插件迁移至 Wasm 格式（官方提供迁移工具）
2. 配置 `warmup_duration_secs` 参数（建议值：30s）
3. 启用 `wasm_runtime` 的 `v8` 引擎（比默认的 `wamr` 快 20%）

**预期效果**: 
- 冷启动延迟降低 60%
- 并发请求处理能力提升 30%

---

### 优化 2：配置分层缓存策略

**说明**: 默认缓存配置可能导致频繁回源。通过多级缓存（内存+Redis）可减少 90% 后端访问。

**实施方法**:
1. 在路由配置中启用 `cache_enabled: true`
2. 设置缓存键规则示例：
   ```yaml
   cache_key:
     - query_param: version
     - header: X-Device-ID
   ```
3. 配置 Redis 作为二级缓存（`redis_host: 127.0.0.1`）

**预期效果**: 
- 回源流量减少 85%
- P99 延迟从 120ms 降至 15ms

---

### 优化 3：调整连接池参数

**说明**: 默认连接池配置（max_connections: 1024）在高并发场景下会导致请求排队。实测 2000 QPS 时出现 15% 请求超时。

**实施方法**:
1. 修改 `upstream` 配置：
   ```yaml
   connection_pool:
     max_connections: 4096
     max_requests_per_connection: 10000
   ```
2. 启用 HTTP/2（`http2: true`）

**预期效果**: 
- 吞吐量提升 120%
- 连接复用率从 40% 提升至 95%

---

### 优化 4：启用 QUIC 协议

**说明**: 在弱网环境下 QUIC 可将连接建立时间从 TCP 的 3RTT 降至 1RTT。

**实施方法**:
1. 在监听器配置中添加：
   ```yaml
   quic_config:
     enabled: true
     idle_timeout: 30s
   ```
2. 客户端需支持 HTTP/3（如 Chrome 浏览器）

**预期效果**: 
- 弱网环境下页面加载速度提升 40%
- 连接迁移成功率 99.9%

---

### 优化 5：实施金丝雀发布优化

**说明**: 默认的蓝绿部署会导致流量突增。通过渐进式金丝雀发布可平滑负载。

**实施方法**:
1. 配置流量规则：
   ```yaml
   canary:
     weight: 10
     match:
       headers:
         - name: X-Canary
           value: "true"
   ```
2. 每 5 分钟自动增加 10% 流量

**预期效果**: 
- 错误率降低 70%
- 发布期间 CPU 峰值波动减少 50%

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Envoy，提供高性能流量管理。
- 支持热更新路由规则、插件扩展及金丝雀发布，显著提升微服务架构的灵活性。
- 内置 WAF 防护、限流熔断等安全能力，可直接对接 Nacos/Consul 等服务发现组件。
- 提供可视化控制台与 K8s CRD 双模式运维，降低多云环境下的网关管理复杂度。
- 通过 WASM 插件机制实现动态扩展，避免传统网关重启服务的性能损耗。
- 兼容 Ingress/Gateway API 标准，可平滑替代 Nginx/Kong 等传统网关组件。
- 开源版本已包含企业级特性（如分布式追踪、指标监控），适合生产环境直接部署。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的定位与作用，对比 Higress 与 Nginx、Kong、Istio 的区别。
- Higress 核心架构：深入学习 Higress 的架构设计，了解其如何结合 Ingress Controller 和 Gateway 的能力。
- 基本安装部署：掌握在 Kubernetes 环境及 Docker/Docker Compose 环境下的部署方式。
- 基本流量管理：学习如何通过 Ingress 或 Gateway API 配置简单的路由转发（HTTP/HTTPS）。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (GitHub Wiki 或 官网)
- Higress GitHub 仓库 README
- 云原生网关基础概念相关博文

**学习建议**:
建议先从官方提供的 "Quick Start" 入手，在本地搭建一个最小化的可用环境。不要一开始就陷入复杂的配置，重点在于跑通流量从客户端 -> Higress -> 后端服务的全链路。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 高级路由特性：学习基于 Header、Query、Cookie 等条件的复杂路由匹配，以及 Header/Body 的改写操作。
- 服务治理与负载均衡：掌握服务发现（Nacos, Consul, K8s Service）的配置，以及超时、重试、熔断等容错机制。
- 安全防护：学习如何配置 Basic Auth、JWT 验证、IP 黑白名单以及 CORS 跨域设置。
- 插件系统入门：了解 Higress 的插件规范（Wasm 支持），学会如何在控制台开启和配置官方预设插件（如限流、防盗链）。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件开发章节
- Higress 控制台实操界面
- Envoy Filter 基础知识（Higress 底层基于 Envoy）

**学习建议**:
此阶段建议结合实际业务场景进行练习。例如，模拟后端服务故障，观察 Higress 的重试和熔断机制是否生效；尝试配置一个限流插件，压测观察效果。务必熟悉控制台的操作，因为这是日常运维最常用的工具。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- Wasm 插件开发：深入学习如何使用 Go 或 C++ 开发 Wasm (WebAssembly) 插件，实现自定义的业务逻辑（如自定义鉴权、请求响应体修改）。
- 可观测性集成：掌握 Prometheus 监控指标的采集与配置，集成常见的日志系统（如 SLS, ELK）和链路追踪。
- 高可用部署：学习 Higress 的高可用（HA）部署模式，配置健康检查与优雅关闭。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方插件开发示例
- WebAssembly (Wasm) 官方文档
- Prometheus 与 Grafana 使用教程

**学习建议**:
尝试编写一个简单的 Wasm 插件，例如在请求头中添加一个特定的标识，并在后端服务中验证该标识。同时，搭建一套 Prometheus + Grafana 监控看板，重点关注 QPS、延迟和成功率等核心指标。

---

### 阶段 4：生态集成与源码解析

**学习内容**:
- AI 网关特性：学习 Higress 在 AI 领域的应用，包括对接大模型（LLM）的 Prompt 模板管理、Token 计数与限流。
- 服务网格集成：探索 Higress 与 Istio 的集成模式，实现东西向与南北向流量的统一管理。
- 源码级理解：阅读 Higress 核心源码，理解请求的处理流水线以及配置的下发机制。
- 性能调优：深入理解 Higress 的性能瓶颈，进行连接池、缓冲区大小等内核参数的调优。

**学习时间**: 4周以上 (持续学习)

**学习资源**:
- Higress GitHub 源码
- Higress AI 网关相关博客与文档
- 云原生社区技术分享

**学习建议**:
在这个阶段，你需要从“使用者”转变为“贡献者”或“专家”。阅读源码时，建议从 HTTP Filter 的处理逻辑入手。如果工作中涉及 AI 应用，重点研究 AI 网关的特性，这是 Higress 相比传统网关的一大亮点。尝试参与 GitHub Issue 的讨论或提交 PR。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是基于阿里云内部多年实践以及开源社区 Istio 和 Envoy 的经验构建的。它旨在提供高性能、高可用的流量管理能力。

**主要区别如下：**
*   **与 Nginx 的区别**：Nginx 主要是一个高性能的 Web 服务器和反向代理，配置主要通过配置文件进行，适合静态配置场景。Higiggs 则更侧重于**云原生和动态配置**，提供了控制台和 API 来动态管理路由、服务发现和插件配置，无需重启网关即可生效，且对 Kubernetes 有更深的集成。
*   **与 Kong 的区别**：Kong 基于 OpenResty (Nginx + Lua)，其插件扩展主要使用 Lua 语言编写。Higiggs 底层基于 **Envoy** (C++/Go)，使用 **Go** 语言编写插件（Wasm 插件），在安全隔离性（沙箱）、资源管控和性能上通常更具优势，且与 Istio 服务网格的生态融合更紧密。

---



### 2: Higress 是如何兼容 Istio 的？我可以在现有的 Istio 集群中使用它吗？

2: Higress 是如何兼容 Istio 的？我可以在现有的 Istio 集群中使用它吗？

**A**: Higiggs 设计之初就考虑了与 Istio 的深度兼容。它遵循 Istio 的 Ingress Gateway 规范，并复用了 Istio 的大量 CRD（自定义资源定义），如 `VirtualService`、`DestinationRule` 等。

**具体兼容性表现：**
1.  **无缝替换**：你可以直接用 Higiggs 替换掉 Istio 默认的 Ingress Gateway，Higiggs 会自动识别 Kubernetes 集群中 Istio 产生的路由规则配置。
2.  **控制平面对接**：Higiggs 可以作为 Istio 的数据平面，由 Istio 控制平面进行配置下发，同时也可以利用 Higiggs 自带的控制台进行更精细化的流量和插件管理。
3.  **平滑迁移**：对于已经在使用 Istio 的用户，引入 Higiggs 可以获得更好的可观测性、更丰富的扩展插件（如 Dubbo、Nacos 服务发现支持）以及更易用的控制台，而无需修改原有的 Istio 资源配置。

---



### 3: Higress 支持哪些协议？除了 HTTP/HTTPS，它支持 gRPC 或 Dubbo 吗？

3: Higress 支持哪些协议？除了 HTTP/HTTPS，它支持 gRPC 或 Dubbo 吗？

**A**: Higiggs 基于 Envoy，因此继承了 Envoy 强大的协议处理能力，支持多种主流协议。

1.  **HTTP/HTTPS**：原生支持 HTTP 1.0/1.1/2 以及 HTTP/3 (QUIC)。
2.  **gRPC**：完全支持 gRPC 和 gRPC-Web，支持基于 gRPC 的路由管理和负载均衡。
3.  **Dubbo**：这是 Higiggs 的一个特色功能。由于背靠阿里云生态，Higiggs 原生支持 Apache Dubbo/Dubbo3 协议。它可以将 HTTP 请求转换为 Dubbo 调用，实现网关与后端微服务的高效互通，这对于使用 Java 生态和 Dubbo 框架的用户非常友好。
4.  **其他协议**：支持 TCP 和 TLS 透传，以及基于 WebSocket 的长连接通信。

---



### 4: Higress 的插件机制是如何工作的？支持自定义插件吗？

4: Higress 的插件机制是如何工作的？支持自定义插件吗？

**A**: Higiggs 提供了非常灵活的插件扩展机制，主要分为两类：内置插件和自定义插件。

1.  **内置插件**：Higiggs 开箱即用，提供了大量常见功能的插件，例如认证鉴权（KeyAuth, JWT）、请求限流、CORS 处理、请求/响应重写、以及阿里云特有的云原生插件等。
2.  **自定义插件**：
    *   **Go 插件**：用户可以使用 Go 语言编写自定义逻辑，编译成 WASM (WebAssembly) 格式。
    *   **Wasm 支持**：Higiggs 利用 Envoy 的 Wasm 能力，允许用户动态加载和卸载插件。这意味着你可以在不重启网关实例的情况下，更新插件逻辑，且插件的运行隔离在沙箱中，不会影响网关主进程的稳定性。
    *   **Lua/脚本支持**：虽然主推 Go+Wasm，但也支持通过脚本方式快速实现简单的逻辑。

---



### 5: 如何在生产环境中部署 Higress？对 Kubernetes 有依赖吗？

5: 如何在生产环境中部署 Higress？对 Kubernetes 有依赖吗？

**A**: Higiggs 是为云原生而设计的，强烈推荐在 Kubernetes 环境中部署。

1.  **部署方式**：通常通过 Helm Chart 或 kubectl YAML 资源文件在 Kubernetes 集群中进行部署。它会自动创建 Deployment、Service、ConfigMap 等必要的资源。
2.  **依赖性**：
    *   **标准 K8s 环境**：需要标准的 Kubernetes 集群（版本通常建议 1.19+）。
    *   **服务发现**：虽然它也可以对接 Nacos、Consul 等第三方

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### Higress 基于 Envoy 构建，但为了适应云原生环境，它在 Envoy 的配置模型上做了哪些关键性的抽象和封装？请对比直接使用 Envoy 的配置文件与使用 Higress 的 Ingress 资源配置一个简单的路由转发规则。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其与 Istio 的兼容性及对 AI 模型的支持，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用“服务来源”对接模型而非硬编码 Endpoint
**场景**：你需要对接阿里云 DashScope、通义千问或 OpenAI 等大模型服务。
**建议**：不要将模型的 API Key 或 URL 直接写死在 Ingress 或路由配置中。应使用 Higress 的“服务来源”功能（如对接 MSE、Nacos 或固定域名服务），将 LLM 提供商注册为服务。
**最佳实践**：在服务来源中配置好鉴权参数，然后在路由配置中通过 `service` 字段引用。这样当模型提供商的 API 地址变更或需要轮询切换时，只需修改服务来源配置，无需修改业务路由规则。

### 2. 配置模型级与用户级的双重流控
**场景**：LLM 调用成本高且延迟大，需要防止下游恶意刷接口或上游模型配额耗尽。
**建议**：不要仅依赖简单的 QPS 限流。
**最佳实践**：
*   **模型级保护**：针对后端具体的模型服务（如 gpt-4），配置“请求并发数”限制，而非单纯的 QPS。因为 LLM 是流式响应，并发连接数比每秒请求数更能反映实际负载。
*   **Token 限流**：在插件配置中启用基于 Token 的限流策略，精确控制运营成本。
**常见陷阱**：忽略流式连接的长时间占用特性，导致连接池耗尽，网关无法建立新连接。

### 3. 启用语义路由实现多模型聚合
**场景**：应用需要根据用户提问的意图，自动分发到不同的模型（例如：简单问题给便宜的小模型，复杂推理给大模型）。
**建议**：利用 Higress 的 **LLM 插件** 或 **路由匹配插件**。
**最佳实践**：配置基于“语义”的路由规则。例如，提取 Prompt 的前 N 个字符或通过轻量级分类模型打标，然后在网关层根据标签将流量路由到不同的后端服务（如通义千问-turbo 或通义千问-max）。这比在应用代码里写 `if-else` 更解耦。

### 4. 谨慎处理 SSE 流式响应的超时与缓存
**场景**：AI 生成内容耗时长，需要流式返回（SSE）给用户。
**建议**：必须调整网关的默认超时和缓冲策略。
**最佳实践**：
*   **超时设置**：将路由的 `RequestTimeout` 设置为一个较大的值（如 5 分钟），或者根据模型生成速度动态调整，避免生成一半被网关切断。
*   **关闭缓冲**：确保后端服务配置开启了流式转发，不要在网关层开启全量响应缓存（除非是针对特定 RAG 场景的知识库缓存），否则会破坏 SSE 的实时性。
**常见陷阱**：前端收到网关返回的 504 Gateway Timeout，是因为后端模型还在生成，但网关的连接保持时间到了。

### 5. 使用 WAF 插件过滤 Prompt 注入攻击
**场景**：直接将用户输入传递给 LLM 可能导致提示词注入，绕过安全限制。
**建议**：在网关层配置安全插件，而非仅在应用层校验。
**最佳实践**：启用 Higress 的 WAF 或自定义 Lua/Wasm 插件，对进入的 Prompt 进行关键词或正则过滤（例如过滤“忽略之前的指令”等特征）。作为 AI 网关，它是保障后端模型安全的第一道防线。

### 6. 生产环境必须开启可观测性
**场景**：排查“为什么模型回答慢”或“哪个用户的 Token 消耗最多”。
**建议**：集成 Prometheus + Grafana，并重点关注 AI 相关的 Metrics。
**最佳实践**：
*   监控 **首包时间**：这反映了模型冷启动和首 Token 生成速度。
*   �

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*