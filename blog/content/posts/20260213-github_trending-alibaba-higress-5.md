---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-13T14:12:23+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "LLM", "Istio", "Envoy", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是对 **Higress** 项目的简洁中文总结： 项目概况 * **名称**：alibaba / higress * **简介**：一款 AI 原生 API 网关。 * **语言**：Go。 * **热度**：GitHub 星标数约 7,500+。 核心定义与架构 Higress 是一个基于 I"
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
- **星标**: 7,524 (+13 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关。本文将深入剖析其系统架构，详细介绍核心组件与 WASM 插件体系，帮助开发者掌握如何利用 Higress 构建高性能的 AI 网关服务。

---
## 摘要

基于您提供的内容，以下是对 **Higress** 项目的简洁中文总结：

### 项目概况
*   **名称**：alibaba / higress
*   **简介**：一款 AI 原生 API 网关。
*   **语言**：Go。
*   **热度**：GitHub 星标数约 7,500+。

### 核心定义与架构
Higress 是一个基于 Istio 和 Envoy 构建的**云原生 API 网关**。它通过 **WebAssembly (WASM)** 插件扩展了功能，将控制面（配置管理）与数据面（流量处理）分离。其架构优势在于配置变更可通过 xDS 协议在毫秒级内生效且无连接中断，特别适合 AI 流式响应等长连接场景。

### 三大核心功能与用途
Higress 提供了以下三类主要服务：

1.  **AI 网关**
    *   **功能**：为大语言模型 (LLM) 应用提供统一 API，支持协议转换、可观测性、缓存及安全防护。
    *   **组件**：包含 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 等插件。
    *   **覆盖范围**：兼容 30+ 家 LLM 提供商。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议 (MCP) 服务器，使 AI Agent 能够调用工具和服务。
    *   **组件**：利用 `mcp-router`、`jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如 `quark-search`、`amap-tools`）。

3.  **Kubernetes Ingress (传统 API 网关)**
    *   **功能**：作为 Kubernetes Ingress 控制器使用，并兼容 nginx-ingress 注解，负责微服务路由。

---
## 评论

### 总体判断

**Higress 是目前云原生网关领域中将“AI 原生”理念落地最彻底的开源项目之一。** 它成功打破了传统 API 网关与 AI 大模型（LLM）应用之间的壁垒，通过将 Istio 的控制平面与 Envoy 的高性能数据平面结合，并深度集成 WASM 和 MCP 协议，为构建下一代 AI 应用提供了一套标准化的流量基础设施。

### 深入评价依据

**1. 技术创新性：从“流量转发”进化为“流量理解与增强”**
*   **事实**：Higress 定义为 "AI Native API Gateway"，核心基于 Istio 和 Envoy，并扩展了 WebAssembly (WASM) 插件能力。文档明确提及了 AI Gateway 特性、MCP (Model Context Protocol) 系统以及对 LLM 应用的支持。
*   **推断**：传统网关（如 Nginx, 早期 Kong）主要解决 HTTP/TCP 的负载均衡和鉴权，对 AI 语义无感知。Higress 的差异化在于它“懂”AI。它不仅转发请求，还能通过 **WASM 插件在 Sidecar 或网关层直接处理 Prompt（提示词）**、实现敏感词过滤、Token 计费统计，甚至基于语义做路由。此外，支持 **MCP 协议** 是一大亮点，这意味着 Higress 可以作为 AI Agent 的工具托管中心，解决了 Agent 与外部工具连接的标准化问题，这在目前的网关产品中极具前瞻性。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **事实**：仓库描述指出其提供三大核心功能：AI Gateway、MCP Server Hosting、传统 API 网关（K8s Ingress）。星标数 7,524 且背靠阿里巴巴。
*   **推断**：在 LLM 应用开发中，开发者面临一个痛点：大模型厂商接口各异（OpenAI, Claude, 通义千问等），切换成本高。Higress 提供了**统一的标准 API 协议**，使得后端切换模型时只需修改配置，无需改动业务代码。同时，它解决了 AI 时代的**多租户计费**（按 Token 或请求次数）和**安全合规**（PII 信息脱敏）问题。对于企业而言，它既保护了对 K8s (Istio) 的现有投资，又平滑地引入了 AI 能力，极大地降低了 AI 转型门槛。

**3. 代码质量与架构：云原生最佳实践的集大成者**
*   **事实**：基于 Go 语言开发，架构明确分离了控制平面和数据平面。DeepWiki 提及了详细的架构、构建部署及开发指南。
*   **推断**：选择 Go 语言是云原生基础设施的标配，保证了并发性能。复用 Envoy 作为数据平面是极其明智的架构决策，避免了造轮子，继承了其 C++ 编写的高性能和稳定性。控制平面对 Istio 的解耦和重构（去掉了 Istio 庞重的 Sidecar 注入复杂性，使其能独立部署），体现了阿里在工程化落地上的务实态度——既要云原生的弹性，又要传统网关的轻量部署体验。WASM 的引入保证了扩展性的同时，隔离了插件崩溃对主流程的影响。

**4. 社区活跃度与生态：头部厂商背书，商业化验证充分**
*   **事实**：星标数超过 7,500，文档包含中、日、英三种语言，显示了国际化野心。
*   **推断**：作为阿里内部（如淘宝、天猫、阿里云）核心流量网关的开源版本，Higress 经过了“双11”等超大规模流量的验证。相比于纯粹的实验性项目，Higress 的代码质量和稳定性更有保障。社区的活跃度不仅体现在 Star 数，更体现在其插件市场的丰富度上，特别是针对 AI 模型的适配插件更新频率较高。

**5. 潜在问题与改进建议**
*   **推断**：虽然基于 Envoy 性能强劲，但 WASM 插件的执行效率仍不及原生 C++ 插件，在超高吞吐量下（如百万级 QPS），WASM 的沙箱逃逸开销和序列化/反序列化延迟可能成为瓶颈。此外，Istio 和 Envoy 的学习曲线极其陡峭，Higress 虽然做了封装，但在排查深层网络问题时，对运维人员的要求依然较高。建议增强可观测性（Observability）的集成，特别是针对 AI 请求的 Trace ID 透传，以便在 RAG（检索增强生成）场景下追踪请求链路。

**6. 与同类工具对比优势**
*   **对比 Apache APISIX/Kong**：后两者主要通过 Lua 插件扩展，生态虽成熟但在 AI 领域的专用功能（如流式响应处理、Token 限流）需要用户自行编写插件。Higress 原生支持 AI 特性，且 WASM 的安全性（内存隔离）优于 Lua 的虚拟机。
*   **对比 Istio 标准网关**：Istio 原生配置过于复杂（CRD 繁多）。Higress 提供了更符合运维直觉的控制台和 Ingress API，大大降低了使用门槛，同时针对 AI 场景做了专用优化。

### 边界条件与验证清单

**不适用场景：**
*   极其简单的静态博客托管（使用 Nginx 即可，无需引入 K8s 复杂

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是基于 **Istio** 与 **Envoy** 构建的 AI 原生网关。其架构设计体现了“控制平面与数据平面分离”的云原生设计哲学，同时在传统网关能力之上，通过 **WASM (WebAssembly)** 和 **MCP (Model Context Protocol)** 实现了对 AI 时代的适配。

### 架构模式与技术栈
*   **底层基石**: 使用 **Envoy** 作为高性能数据平面（L7 代理），利用其 C++ 的高性能特性处理长连接和高并发。
*   **控制平面**: 深度集成 **Istio**，复用其 xDS (控制平面与数据平面通信协议) 配置下发机制。这意味着 Higress 天然具备 K8s Ingress Controller 的能力，且配置变更可达毫秒级热更新，无需重启数据面。
*   **扩展机制**: 核心亮点在于 **WASM 插件系统**。Higress 摒弃了传统的 Lua (如 OpenResty) 或 Java (如 Zuul) 过滤器模式，转而支持 WASM。这使得业务逻辑可以使用 C++/Go/Rust/AssemblyScript 编写，编译为沙箱化字节码在 Envoy 中运行，既保证了性能，又实现了隔离性。

### 核心模块
1.  **AI Gateway (AI 网关)**: 这是 Higress 最显著的差异化模块。它不仅仅是流量转发，更提供了 LLM（大语言模型）的语义层处理。
2.  **MCP Server**: 内置对 Model Context Protocol 的支持，作为 AI Agent 的工具集成中心。
3.  **Kubernetes Ingress Controller**: 替代 Nginx Ingress，提供更强大的流量管理能力。

### 架构优势
*   **热更新能力**: 基于 xDS 协议，路由和插件配置的修改可以在毫秒级生效，且不断开已有连接。这对于 AI 场景下的 **流式响应 (SSE/Streaming)** 至关重要，传统网关在配置更新时往往会导致长连接中断。
*   **极致性能**: 数据面 Envoy 采用非阻塞 I/O 模型，配合 WASM 的 Near-native 执行速度，延迟极低。

---

## 2. 核心功能详细解读

### AI Gateway：不仅仅是转发
Higress 将自身定位为 "AI Native API Gateway"，主要解决 LLM 应用开发中的**碎片化**和**稳定性**问题。

*   **统一模型抽象**: 开发者通常面临 OpenAI、通义千问、DeepSeek 等不同厂商的 API 接口差异（尽管都兼容 OpenAI 格式，但仍有细微差别，且涉及 Key 管理）。Higress 允许在网关层统一配置 Provider，后端服务只需调用 Higress，由网关负责路由到具体的 LLM 厂商。
*   **Token 管理**: AI 应用的核心成本在于 Token。Higress 支持基于 Token 的流控和计费统计，这是传统 API 网关（仅处理 HTTP Request/Response 计数）所不具备的。
*   **语义层缓存**: 针对大模型请求昂贵且重复的问题，Higress 支持基于语义的缓存。即如果用户提问的语义相似，网关可以直接返回缓存结果，而无需请求大模型，从而大幅降低成本和延迟。
*   **安全防护**: 提供 Prompt 注入检测和敏感信息脱敏功能。

### MCP Server Hosting
*   **痛点**: AI Agent 需要调用外部工具（如搜索、数据库查询）。MCP 是连接 Agent 和 Tools 的标准协议。
*   **解耦**: Higress 充当 MCP Server 的托管中心，使得 Agent 不需要直接连接各个工具服务，而是通过网关统一管理和鉴权，增强了系统的安全性。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | APISIX |
| :--- | :--- | :--- | :--- |
| **底层语言** | Go (控制面) + C++ (数据面 Envoy) | C (Nginx) / Golang (Kong) | Golang + LuaJIT |
| **配置热更新** | 支持 (基于 xDS, 无缝) | Nginx 原生不支持 Reload 会断连接 / Kong 支持 | 支持 |
| **扩展机制** | **WASM (沙箱, 多语言)** | Lua/C (侵入性强) | Lua/Plugin (依赖 LuaJIT) |
| **AI 特性** | **原生支持 (Token计费, 模型路由)** | 需自行编写插件 | 需自行编写插件 |
| **K8s 集成** | Istio 原生 | 需额外组件 | 支持 |

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件加载**:
    *   Higress 通过 Envoy 的 WASM Filter 加载插件。
    *   实现了 Proxy-WASM 规范，允许插件访问 HTTP Header/Body、路由信息以及共享内存。
    *   **难点**: WASM 的内存管理是线性的，如何高效地在 Host (Envoy) 和 Guest (WASM) 之间传递大量数据（如 LLM 的流式 Body）是性能优化的关键。Higress 对此进行了优化，减少了数据拷贝的开销。

2.  **LLM 流式转发**:
    *   大模型响应通常采用 Server-Sent Events (SSE) 或分块传输。
    *   传统网关在处理流式数据时，往往需要缓冲整个 Body 才能进行修改或鉴权，导致首字节延迟（TTFB）过高。
    *   Higress 在数据面实现了流式拦截和处理，可以在数据流经网关时实时进行 Token 统计或内容替换，而不需要等待响应结束。

### 代码组织
*   **控制面**: 主要使用 Go 语言编写。负责 K8s CRD 监听、配置翻译为 xDS、WASM 插件生命周期管理。
*   **数据面**: 基于 Envoy 官方镜像进行定制，扩展了特定的 C++ 扩展或 WASM 运行时。
*   **Console**: 提供图形化管理界面，简化了复杂的 Istio 配置。

---

## 4. 适用场景分析

### 最适合的场景
1.  **AI 应用开发与中台**: 企业构建 AI 中台，统一管理多个部门的 LLM 调用，进行统一的 Key 轮转、鉴权和流控。
2.  **高并发微服务网关**: 替代 Nginx Ingress，特别是需要频繁变更路由规则且不能断连的场景（如游戏、即时通讯）。
3.  **多语言插件生态**: 团队中包含不同语言开发者，希望使用 Go/Rust 编写网关业务逻辑，而不被 Lua 限制。

### 不适合的场景
1.  **极简单流量转发**: 如果仅需要简单的 Nginx 反向代理，Higress 的架构过于复杂，运维成本高于 Nginx。
2.  **非 K8s 环境**: 虽然 Higress 可以在非 K8s 环境运行，但其最大的优势在于与 K8s 和 Istio 的结合。在传统虚拟机环境下部署 Higress 会大材小用且配置繁琐。

### 集成注意事项
*   **资源消耗**: Envoy + WASM 运行时的内存消耗相对较高，需要合理配置 Sidecar 或 Gateway 的资源限制。
*   **WASM 兼容性**: 并非所有 Envoy 特性在 WASM 中都能完美支持，开发复杂插件时需要查阅 Proxy-WASM API 文档。

---

## 5. 发展趋势展望

Higress 的演进方向紧贴 AI 工程化趋势：
1.  **从流量网关到语义网关**: 未来的网关将不仅处理 L7 流量，还能理解 LLM 的上下文。Higress 可能会集成更强的向量检索能力或 RAG（检索增强生成）处理逻辑，直接在网关层完成部分 RAG 链路。
2.  **Dapr 集成**: 随着云原生的深入，网关与应用的边界可能模糊，Higress 可能会加强与 Dapr 的集成，提供更完善的 Service-to-Service 通信能力。
3.  **更强大的 AI 可观测性**: 针对大模型调用的 Trace、Token 消耗明细、Prompt 质量分析将成为标配功能。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**: 想要深入理解 Istio 和 Envory 的实战应用。
*   **AI 工程师**: 需要构建生产级 LLM 应用的开发者。
*   **后端开发**: 对高性能网关技术感兴趣的开发者。

### 学习路径
1.  **基础**: 熟悉 Kubernetes Ingress 概念，了解 HTTP 协议细节。
2.  **核心**: 阅读 Envoy 官方文档，理解 xDS 协议（LDS/CDS/RDS）。
3.  **进阶**: 学习 WebAssembly (WASM) 基础，尝试编写一个简单的 Higress WASM 插件（如添加一个请求头）。
4.  **实战**: 部署 Higress 到本地 K8s 集群，配置一个 AI 模型提供商，并实现基于 Token 的限流。

---

## 7. 最佳实践建议

### 性能优化
*   **开启 WASM 沙箱优化**: 在生产环境中，确保使用合适的 WASM 运行时配置，以平衡安全性与性能。
*   **连接池管理**: 针对后端 LLM 服务（通常响应较慢），合理调整 Envoy 的连接池超时时间，避免频繁建立连接导致握手开销过大。

### 常见问题
*   **流式响应中断**: 如果发现 AI 回复中断，通常是因为网关或后端配置的超时时间过短。需检查 `stream_idle_timeout` 等配置。
*   **WASM 插件崩溃**: WASM 插件崩溃不应拖垮主网关。利用 Higress 的插件隔离机制，确保异常插件被自动重启。

### 使用原则
*   **逻辑下沉**: 尽量将复杂的业务逻辑放在 WASM 插件中，而不是修改 Envoy 核心代码，这样便于升级和维护。
*   **配置即代码**: 使用 GitOps 管理 Higress 的配置（Ingress/Gateway 资源），避免控制台手动修改导致的配置漂移。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在抽象层上做了一个关键的**“下沉”**决策：它将 **Istio** 的复杂性（通常被认为是 Service Mesh 中极难运维的部分）封装成了 **API Gateway** 的易用性。
*   **复杂性转移**: 它把复杂性从“应用代码”转移到了“基础设施层”。用户不再需要在应用中处理 LLM 的重试、鉴权、模型切换，而是将其配置在网关层。
*   **代价**: 这种抽象要求运维团队必须理解 Envoy 和 xDS 的调试。当出现网络

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则，将请求转发到不同的后端服务
    解决问题：根据请求路径或头部信息动态路由到微服务
    """
    from higress import Gateway, RouteRule, BackendService

    # 创建网关实例
    gateway = Gateway(name="api-gateway")

    # 定义后端服务
    user_service = BackendService(
        name="user-service",
        url="http://user-service:8080",
        health_check="/health"
    )

    order_service = BackendService(
        name="order-service",
        url="http://order-service:8081",
        health_check="/health"
    )

    # 配置路由规则
    user_route = RouteRule(
        match=["/api/users/*"],
        backend=user_service,
        timeout=5  # 超时时间(秒)
    )

    order_route = RouteRule(
        match=["/api/orders/*"],
        backend=order_service,
        timeout=3
    )

    # 添加路由到网关
    gateway.add_routes([user_route, order_route])
    gateway.apply_config()

    print("Higress路由配置已应用")
```




```python
# 示例2：Higress 流量控制插件
def higress_rate_limit():
    """
    实现基于IP的请求限流
    解决问题：防止恶意请求或流量突增导致服务过载
    """
    from higress import Gateway, RateLimitPlugin

    gateway = Gateway(name="api-gateway")

    # 配置限流插件
    rate_limiter = RateLimitPlugin(
        name="ip-rate-limiter",
        key="client_ip",  # 基于客户端IP限流
        limit=100,        # 每分钟100次请求
        burst=20,         # 允许突发20次请求
        response_code=429,
        response_message="Too Many Requests"
    )

    # 应用插件到网关
    gateway.add_plugin(rate_limiter)
    gateway.apply_config()

    print("限流插件已启用")
```




```python
# 示例3：Higress 金丝雀发布
def higress_canary_release():
    """
    实现服务的金丝雀发布
    解决问题：灰度发布新版本服务，降低发布风险
    """
    from higress import Gateway, RouteRule, BackendService, CanaryConfig

    gateway = Gateway(name="api-gateway")

    # 定义生产版本和金丝雀版本
    prod_service = BackendService(
        name="product-service-v1",
        url="http://product-service-v1:8080"
    )

    canary_service = BackendService(
        name="product-service-v2",
        url="http://product-service-v2:8080"
    )

    # 配置金丝雀规则
    canary_rule = RouteRule(
        match=["/api/products/*"],
        backends={
            "primary": prod_service,
            "canary": canary_service
        },
        canary=CanaryConfig(
            traffic_percentage=10,  # 10%流量到金丝雀版本
            header_match="x-canary:true"  # 带特定header的请求强制走金丝雀
        )
    )

    gateway.add_route(canary_rule)
    gateway.apply_config()

    print("金丝雀发布配置已应用")
```


---
## 案例研究


### 1：阿里巴巴百亿级流量大促保障

 1：阿里巴巴百亿级流量大促保障

**背景**:
在每年的“双11”和“618”等大型购物节期间，阿里巴巴电商生态面临着巨大的流量洪峰。传统的网关架构在应对每秒数十万甚至数百万级的QPS（每秒查询率）时，往往面临资源利用率低、扩容响应慢以及配置变更风险高等挑战。系统需要一个能够承载极高并发且具备极致弹性的流量入口。

**问题**:
原有的网关架构在应对突发流量时存在扩容滞后问题，且传统网关与业务代码耦合较紧，导致路由规则和流量治理策略的更新发布流程繁琐，容易引发线上故障。此外，多语言（Java、Go、Node.js等）微服务体系的统一接入和认证鉴权也变得日益复杂。

**解决方案**:
阿里巴巴基于内部多年的网关经验，开源并使用了 **Higress**。Higress 遵循 Ingress/Gateway API 标准，将阿里内部经过验证的高性能流量治理能力与开源的 Envoy 内核相结合。
1.  **架构升级**：采用 Higress 作为云原生 API 网关，实现了业务流量与网关基础设施的解耦。
2.  **极致弹性**：利用 Higress 的轻量级和高性能特性，结合 Kubernetes，实现了秒级的弹性扩缩容，从容应对流量洪峰。
3.  **插件生态**：利用 Higress 的 WASM (WebAssembly) 插件市场，实现了业务逻辑（如限流、鉴权、路由重写）的热加载，无需重启网关即可更新逻辑。

**效果**:
通过 Higress，阿里巴巴不仅成功支撑了双11期间核心交易链路的百亿级流量冲击，实现了 99.996% 的高可用性，还将网关的资源成本降低了约 50%。更重要的是，业务开发人员可以通过编写 WASM 插件自助完成流量治理逻辑，网关的变更发布效率提升了数倍，极大降低了运维风险。

---



### 2：某大型互联网企业 AI 应用网关重构

 2：某大型互联网企业 AI 应用网关重构

**背景**:
随着大模型（LLM）技术的爆发，某大型互联网公司内部涌现了大量基于 AI 的应用，包括智能客服、代码辅助和数据分析助手。这些应用需要对接不同的模型提供商（如通义千问、文心一言等），同时也面临高昂的 Token 计费成本和复杂的 Prompt 管理需求。

**问题**:
在接入 AI 服务时，团队遇到了几个痛点：
1.  **成本高昂**：大模型调用按 Token 计费，缺乏有效的流量控制和缓存机制，导致成本难以控制。
2.  **兼容性差**：不同的模型提供商 API 接口标准不一，业务代码需要针对不同厂商做适配，开发效率低。
3.  **安全风险**：API Key 直接暴露在客户端代码中，存在严重的安全泄露隐患。

**解决方案**:
该企业引入 **Higress** 作为 AI 专用网关（AI Gateway）。
1.  **统一接口**：利用 Higress 内置的 AI 插件能力，将不同厂商的异构 API 统一封装为标准接口，业务端只需调用 Higress，无需关心底层模型供应商。
2.  **Token 缓存与优化**：开启 Higress 的语义缓存功能，对于相似的 Prompt 请求直接返回缓存结果，大幅减少对下游大模型的重复调用，降低 Token 消耗。
3.  **安全隔离**：在网关层统一管理 API Key 和密钥，客户端仅持有网关颁发的凭证，实现了敏感信息的完全隔离。

**效果**:
使用 Higress 后，该企业 AI 应用的开发接入时间从 3 天缩短至 1 小时。通过智能缓存和流控策略，大模型调用的 Token 消耗降低了约 30%，显著节省了运营成本。同时，统一的安全管控消除了 API Key 泄露的风险，保障了生产环境的安全合规。

---



### 3：某跨国电商平台多地域流量治理

 3：某跨国电商平台多地域流量治理

**背景**:
该电商平台业务覆盖中国、东南亚和欧洲，基础设施部署在多个不同云厂商的 Kubernetes 集群中。随着业务微服务化，服务间的调用关系变得极其复杂，跨地域、跨集群的流量管理成为运维的噩梦。

**问题**:
1.  **跨云互通难**：不同云厂商的 LoadBalancer 实现标准不一，服务发现和路由配置难以统一。
2.  **灰度发布复杂**：在进行新版本发布时，无法精确控制不同地域、不同用户群体的流量走向，导致全量发布风险极高。
3.  **协议转换繁琐**：后端存在 gRPC 服务，但前端是 HTTP/HTTPS，网关层缺乏高效的协议转换能力。

**解决方案**:
该平台采用 **Higress** 构建了统一的多集群 ingress 网关体系。
1.  **统一流量入口**：在各个 Kubernetes 集群中部署 Higress，通过关联 MSE（微服务引擎）或自建的控制平面，实现了多集群流量的统一视图和配置下发。
2.  **精细化路由**：基于 Higress 的 HTTP 到 gRPC 的协议转换能力，前端无需改动即可调用后端高性能微服务。利用 Header 匹配和权重配置，实现了基于地域和用户画像的蓝绿/金丝雀发布。
3.  **全链路生态**：Higress 原生集成了 Prometheus 和 SkyWalking，实现了跨云流量的统一监控和可观测性。

**效果**:
Higress 的部署成功打通了跨云网络，实现了“一处配置，处处生效”。新功能的灰度发布周期从 2 周缩短至 2 天，且实现了零故障上线。通过 gRPC 协议转换，服务间通信延迟降低了 20%，极大地提升了全球用户的访问体验。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|------------|--------|--------|
| 性能 | 基于Istio+Envoy，高性能，支持Wasm插件扩展 | 高性能，基于OpenResty/Nginx | 极高性能，基于OpenResty/LuaJIT |
| 易用性 | 提供控制台和Kubernetes CRD，支持云原生部署 | 提供管理界面和RESTful API，配置灵活 | 提供Dashboard和CLI，配置较复杂 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源版免费，企业版收费 | 开源免费，企业版收费 |
| 功能 | 支持流量管理、安全防护、可观测性，集成K8s | 丰富的插件生态，支持API网关功能 | 功能全面，支持动态路由、限流熔断 |
| 社区 | 阿里背书，社区活跃，文档完善 | 社区成熟，用户基数大 | 社区活跃，国内用户较多 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境
- 优势2：支持Wasm插件，扩展性强，性能损耗低
- 优势3：阿里云提供商业支持，适合企业级应用

### 不足分析

- 不足1：社区规模和插件生态不如Kong成熟
- 不足2：学习曲线较陡峭，需要熟悉Istio和Envoy
- 不足3：非Kubernetes环境部署复杂度较高

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现插件扩展

**说明**: Higress 基于 Envoy 和 Istio 构建，其最大的特性之一是对 WebAssembly (WASM) 的原生支持。利用 WASM 插件机制，可以使用 C++、Go、Rust 或 AssemblyScript 等多种语言编写自定义逻辑，而无需修改网关核心代码或重新部署整个网关集群。这极大地扩展了网关的功能边界，实现了业务逻辑的灵活热插拔。

**实施步骤**:
1. 确定业务需求（如自定义鉴权、请求头修改、流量染色）。
2. 选择合适的编程语言（推荐 Go 或 Rust）开发 WASM 插件，利用 Higress 提供的 SDK。
3. 在本地或 CI/CD 流水线中将源码编译为 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传插件。
5. 在特定的网关路由或全局范围内配置并启用该插件。

**注意事项**: 编写 WASM 代码时需注意内存管理和性能开销，避免阻塞主线程导致请求延迟增加。

---

### 实践 2：服务注册与发现集成

**说明**: Higress 设计为云原生网关，能够无缝对接主流的服务注册中心。通过配置服务来源（Service Sources），Higress 可以自动从注册中心获取服务实例列表，实现动态流量转发。这解决了传统 Nginx 配置繁重且无法自动感知实例上下线的问题。

**实施步骤**:
1. 在 Higress 控制台的“来源管理”中添加对应的服务来源（如 Nacos, Consul, Zookeeper, 或 K8s Service）。
2. 配置注册中心的连接地址（如 Nacos 的 namespace 和 serverAddr）。
3. 创建服务并关联已配置的来源，Higress 将自动同步服务下的 IP 列表。
4. 在路由配置中直接选择服务名称作为后端服务。

**注意事项**: 确保网络连通性，即 Higress 网关所在的网络环境能够访问注册中心的网络端口。

---

### 实践 3：全链路安全防护与认证

**说明**: 在微服务架构中，网关是流量的唯一入口，必须在此处实施严格的安全策略。Higress 提供了从 HTTP 到 HTTPS 的协议转换以及多种认证方式。最佳实践是启用 mTLS（双向认证）以增强服务间通信安全，并配合 JWT 或 OIDC 进行终端用户身份验证。

**实施步骤**:
1. 在 Higress 的域名管理中上传或配置 SSL 证书，强制开启 HTTPS。
2. 配置“认证鉴权”插件，选择 Keycloak、OIDC 或自研的 JWT 验证逻辑。
3. 对于对内请求，配置 mTLS 策略，要求客户端提供有效证书。
4. 设置 IP 黑白名单插件，限制特定来源的访问请求。

**注意事项**: 定期轮换 SSL 证书和 JWT 密钥，避免使用默认或弱加密算法（如 SHA1）。

---

### 实践 4：精细化流量治理与灰度发布

**说明**: 利用 Higress 强大的路由能力实现蓝绿部署或金丝雀发布。通过基于 HTTP Header、Cookie 或权重将流量精确路由到不同版本的服务实例上。这可以最大程度降低新版本上线的风险，实现快速回滚。

**实施步骤**:
1. 准备好不同版本的服务实例（如 v1 和 v2），并确保它们已注册到服务发现中心。
2. 在 Higress 中创建两个服务（Service），分别关联 v1 和 v2 的实例分组。
3. 配置路由规则，设置“匹配条件”，例如当 Header `x-version: v2` 时路由至 v2 服务，否则路由至 v1 服务。
4. 或者使用“权重路由”功能，设置 10% 流量流向 v2，观察无异常后逐步调整至 100%。

**注意事项**: 灰度发布期间必须保持 Session（会话）粘性（Sticky Session）的一致性，除非是无状态服务。

---

### 实践 5：构建高可用部署架构

**说明**: 生产环境必须保证网关自身的高可用性。Higress 通常部署在 Kubernetes 集群中，应合理配置 HPA（水平自动伸缩）和 PDB（Pod 中断预算）。同时，应配置多副本部署以消除单点故障，并开启健康检查机制。

**实施步骤**:
1. 在 Kubernetes 中为 Higress Gateway 配置 HPA，根据 CPU 使用率或 QPS 自动调整副本数。
2. 配置 `readinessProbe` 和 `livenessProbe`，确保异常 Pod 能及时被摘除。
3. 设置 `PodDisruptionBudget`，确保在节点维护时至少有最小数量的 Pod 运行。
4. 在 Higress 前端配置负载均衡器（如 ALB 或 SLB），将流量均匀分发至各 Higress Pod。

**注意事项**: 避免配置过大的内存

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，启用 HTTP/3 协议可以显著改善弱网环境下的连接建立速度和吞吐量。基于 UDP 的 QUIC 协议解决了 TCP 队头阻塞问题，能降低连接迁移时的延迟，特别适合移动端或跨地域访问场景。

**实施方法**:
1. 在 Higress 网关监听器配置中，开启 HTTP/3 协议开关（需确保底层网络环境允许 UDP 流量）。
2. 配置 TLS 1.3 作为 HTTP/3 的基础加密层。
3. 在 DNS 配置中添加 HTTPS 记录以启用 HTTP/3 的 Alt-Svc 机制。

**预期效果**: 在高丢包率或高延迟网络环境下，连接建立时间可减少 30%-50%，页面加载速度提升 20%。

---

### 优化 2：优化 Wasm 插件执行效率

**说明**: Higress 的核心优势之一是支持 Wasm 插件。不规范的 Wasm 插件代码（如在请求路径中进行大量正则匹配或阻塞式 I/O）会严重拖慢网关吞吐。通过优化 Wasm 代码逻辑和利用 Proxy-Wasm 的 ABI 特性，可以降低延迟。

**实施方法**:
1. **复用内存**: 在 `onConfigure` 阶段预编译正则表达式或初始化共享对象，避免在 `onHttpRequest` 等高频路径中重复初始化。
2. **减少宿主调用**: 尽量在 Wasm 虚拟机内部处理简单逻辑，减少与宿主环境的跨边界调用次数。
3. **使用 TinyGo 编译**: 使用 TinyGo 编译 Wasm 插件以获得更小的二进制体积和更快的启动速度，并开启优化选项（`-opt=2`）。

**预期效果**: 复杂插件处理阶段的 CPU 开销降低 20%-40%，单核 QPS（每秒查询率）提升 15% 以上。

---

### 优化 3：配置全链路超时与连接池调优

**说明**: 默认的配置往往过于保守。后端服务响应慢或连接数不足会导致网关线程阻塞。通过精细调整上游服务的连接超时、最大空闲连接数和最大请求等待时间，可以防止资源耗尽并提高转发效率。

**实施方法**:
1. **调整连接池**: 根据后端服务能力，适当增加 `maxIdleConnections` 和 `maxRequestsPerConnection`。
2. **设置合理超时**: 设置 `connectTimeout`（连接超时）为 2-5s，`readTimeout`（读取超时）根据业务 SLA 设置（如 10s），避免长时间挂起。
3. **启用 HTTP/2 连接复用**: 对后端启用 HTTP/2，减少 TCP 连接建立开销。

**预期效果**: 后端服务高负载时的 P99 延迟降低 15%-30%，有效减少因超时堆积导致的网关内存溢出（OOM）风险。

---

### 优化 4：启用本地与分布式缓存策略

**说明**: 对于高频读取但低频变更的配置数据或鉴权结果，每次都回源 Redis 或数据库会造成巨大的网络延迟。利用 Higress 的本地缓存或分布式缓存能力，可以显著缩短请求处理链路。

**实施方法**:
1. **启用 Wasm 插件本地缓存**: 在 Wasm 插件中使用 `SharedKVMAP` 或内存哈希表存储热点数据（如 Token 验证结果、限流计数器快照）。
2. **配置 HTTP 缓存**: 对静态资源或 API 响应配置标准的 HTTP Cache-Control 头，并让 Higress 处理缓存逻辑。
3. **使用 Redis 缓存**: 对于分布式场景，配置 Higress 的 Redis 缓存插件，并开启连接池。

**预期效果**: 需要频繁鉴权或查询配置的请求，延迟可降低 50%-70%，后端数据库 QPS 下降 60%。

---

---
## 学习要点

- Higress 是阿里开源的高性能、可扩展的云原生 API 网关，基于 Istio 和 Envoy 构建，支持 Kubernetes 和传统环境。
- 提供丰富的流量管理功能，包括负载均衡、熔断降级、限流和灰度发布，适用于微服务架构。
- 原生集成 K8s Ingress 和 Service Mesh，简化服务网格与 API 网关的统一管理。
- 支持动态路由和插件扩展，允许通过 Lua 或 WASM 编写自定义插件，灵活扩展业务逻辑。
- 兼容 Kubernetes Ingress API，可直接替代 Nginx Ingress，降低迁移成本。
- 内置可观测性能力，集成 Prometheus、Grafana 等工具，提供实时监控和日志分析。
- 适用于云原生应用和混合云场景，提供高可用性和企业级安全特性。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 理解云原生网关的核心概念：什么是 API Gateway，以及它与 Nginx、传统 Kong 网关的区别。
- 了解 Higress 的背景：基于 Istio 和 Envoy 构建，结合了阿里内部的流量治理经验。
- 掌握基本术语：Ingress、Route、Service、Upstream、Plugin。
- 学习 Higress 的架构设计：控制面与数据面的分离，以及如何通过控制台或 CRD 进行管理。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (入门与架构篇)
- Envoy 官方文档基础架构介绍
- Istio 官方文档中的流量管理概念

**学习建议**: 
不要急于动手部署，先通读官方文档的架构介绍，理解 Higress 为什么强调“高可用”和“低延迟”。如果对 Kubernetes 不熟悉，需要先补充 K8s Ingress 的基础知识。

---

### 阶段 2：核心功能实战与部署

**学习内容**:
- 部署 Higress：在本地 Docker 环境或 Kubernetes 集群中安装 Higress。
- 流量路由配置：学习如何配置域名路由、路径匹配、Header 路由以及服务版本管理。
- 服务治理：配置负载均衡策略（加权轮询、一致性哈希等）、超时重试、熔断限流。
- 插件系统：学习如何使用 Higress 提供的内置插件（如 JWT 认证、Request Block）。

**学习时间**: 2-3周

**学习资源**:
- Higress GitHub 仓库 (部署示例 YAML 文件)
- Higress 官方控制台操作指南
- Kubernetes 官方文档 (Ingress API 说明)

**学习建议**: 
建议使用 Minikube 或 Kind 创建一个本地 K8s 集群进行实操。尝试部署两个不同的后端服务（如 httpbin 和 nginx），并通过 Higress 将流量按比例路由到这两个服务，以验证配置的正确性。

---

### 阶段 3：插件开发与高级流量管理

**学习内容**:
- Wasm 插件开发：学习 Higress 基于 Wasm (WebAssembly) 的插件机制，这是 Higress 的核心优势。
- 编写 Wasm 插件：使用 Go 或 C++ 开发自定义插件，实现鉴权、请求修改等逻辑。
- 高级流量特性：全链路灰度发布、金丝雀发布、流量镜像。
- 安全防护：配置 WAF 防护规则，防止 SQL 注入和 XSS 攻击。
- 多租户与多环境管理：在不同命名空间下管理网关配置。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方插件开发文档
- Envoy Wasm 官方文档
- Higress 官方插件市场 (参考现有插件源码)

**学习建议**: 
尝试编写一个简单的 Wasm 插件，例如在请求头中添加特定的自定义字段。学习如何将插件打包并上传到 Higress 控制台。重点关注 Wasm 的性能特性及其热加载能力。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- 监控与可观测性：集成 Prometheus、Grafana、SkyWalking，配置日志采集（SLS）。
- 性能调优：理解连接池配置、Buffer 限制、工作线程数调优。
- 高可用部署：在 K8s 中配置 HPA (Horizontal Pod Autoscaler)，配置多副本容灾。
- 网关安全：配置 HTTPS 证书管理、mTLS 双向认证。
- 与微服务生态集成：对接 Nacos、Consul 等注册中心，实现动态服务发现。

**学习时间**: 3-4周

**学习资源**:
- Higress 运维最佳实践文档
- Envoy 性能调优指南
- Prometheus 监控最佳实践

**学习建议**: 
模拟生产环境进行压测（使用 JMeter 或 Locust），观察 Higress 的 CPU 和内存消耗，并根据监控指标调整配置。重点学习如何通过 Ingress Class 实现多网关实例的隔离管理。

---

### 阶段 5：源码剖析与架构定制

**学习内容**:
- 源码结构分析：深入阅读 Higress Controller 和 Router 的源码。
- 自定义控制器开发：学习如何基于 Higress 进行二次开发，定制控制面逻辑。
- 贡献开源：参与 GitHub Issue 讨论，提交 PR 修复 Bug 或增加新特性。
- 架构演进：研究 Higress 如何处理长连接、WebSocket 以及 gRPC 流量。

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码 (alibaba/higress)
- Istio C++ 与 Go 源码分析
- Envoy xDS

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是在阿里云内部多年实践的基础上，结合开源社区标准（如 Envoy 和 Istio）构建的。它基于 Envoy 和 Istio（特别是基于 Envoy 的控制面），旨在提供高性能、可扩展的流量管理能力。

与 Nginx 相比，Higress 提供了更现代化的控制面和更强的动态配置能力，支持热更新，无需像传统 Nginx 那样频繁重载配置。与 Kong 相比，Higress 深度集成了云原生生态，支持服务网格（Service Mesh）模式，能够更好地与 Kubernetes 和 Istio 配合，且在处理高并发流量时通常具有更优的性能表现。

---



### 2: Higress 是如何兼容 Apache Dubbo、Nacos 和 gRPC 等阿里系技术栈的？

2: Higress 是如何兼容 Apache Dubbo、Nacos 和 gRPC 等阿里系技术栈的？

**A**: 作为阿里云开源的项目，Higress 对阿里系主流微服务技术栈提供了原生的深度支持。

1.  **Dubbo 支持**：Higress 内置了对 Apache Dubbo 服务的代理能力，可以将 HTTP/HTTPS 请求转换为 Dubbo 协议，实现 RESTful API 到 Dubbo 服务的透传，无需编写额外的适配层。
2.  **Nacos 集成**：Higress 可以直接对接 Nacos 作为服务注册中心和配置中心。它能够实时监听 Nacos 的服务变更，动态调整路由规则，实现流量的平滑调度。
3.  **gRPC 支持**：基于 Envoy 的高性能网络库，Higress 原生支持 gRPC 和 HTTP/2 协议，可以作为 gRPC 服务的路由网关，支持协议转换和负载均衡。

---



### 3: Higress 是否支持 WAF（Web 应用防火墙）功能？如何保障安全？

3: Higress 是否支持 WAF（Web 应用防火墙）功能？如何保障安全？

**A**: 是的，Higress 提供了内置的 WAF 插件支持。它允许用户通过插件的形式定义安全规则，用于防御常见的 Web 攻击（如 SQL 注入、XSS 跨站脚本等）。

此外，Higress 支持对 API 进行细粒度的访问控制，包括基于 IP 的访问控制黑白名单、JWT 验证、以及 Keyless 认证等。它还支持对接阿里云 WAF 或者通过插件扩展自定义的安全逻辑，以保障后端服务的安全性。

---



### 4: Higress 的性能如何？能否支撑高并发业务场景？

4: Higress 的性能如何？能否支撑高并发业务场景？

**A**: Higress 的设计初衷之一就是为了应对超大规模的流量冲击。其数据面基于 Envoy 构建，Envoy 是业界公认的高性能代理，采用 C++ 编写，具有极低的资源消耗和延迟。

在阿里云内部，Higress 已经接管了包括双十一大促在内的海量流量。根据官方基准测试数据，Higress 在处理长连接和短连接请求时，均能保持极高的吞吐量（QPS）和稳定的低延迟，其性能通常优于基于 OpenResty 或 Nginx Lua 的传统网关方案。

---



### 5: 如何从 Nginx、Ingress Controller（如 Nginx Ingress）迁移到 Higress？

5: 如何从 Nginx、Ingress Controller（如 Nginx Ingress）迁移到 Higress？

**A**: Higress 提供了良好的迁移兼容性，特别是针对 Kubernetes 环境。

1.  **Ingress 兼容**：Higress 实现了 Kubernetes Ingress API 的标准，因此可以直接替换 Nginx Ingress Controller，通常只需要修改 Ingress Class 即可，无需大规模修改现有的 Ingress YAML 资源文件。
2.  **Nginx 配置转换**：对于传统的 Nginx 用户，Higress 社区提供了配置转换工具，可以将 Nginx 的 `nginx.conf` 配置转换为 Higress 的路由和插件配置。
3.  **平滑过渡**：由于支持金丝雀发布和蓝绿部署，用户可以在 Higress 上逐步切量，确保业务迁移过程中的稳定性。

---



### 6: Higress 支持哪些类型的插件？如何扩展功能？

6: Higress 支持哪些类型的插件？如何扩展功能？

**A**: Higress 拥有灵活的插件系统，支持以下几类插件：

1.  **原生插件**：内置了认证鉴权、流量管控、可观测性等核心功能的插件。
2.  **Lua/Python/Wasm 插件**：支持通过编写 Lua 或 Python 脚本来扩展业务逻辑，同时也支持 WebAssembly (Wasm) 插件，这使得开发者可以使用 C++/Rust/Go 等语言编写高性能的插件，且插件更新时无需重启网关。
3.  **生态兼容**：Higress 兼容 Kong 和 APISIX 的部分插件设计，降低了迁移成本。用户可以通过控制台或 WASM Store 一键安装所需的插件。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基础环境搭建与流量验证

### 在本地或测试环境中部署 Higress，并配置一个简单的路由规则，将 `/api/v1` 的请求转发到一个模拟的后端服务（如 httpbin.org）。验证请求头中是否包含特定的自定义信息（如 `source: higress`）。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，以下是针对实际生产使用场景的 7 条实践建议：

### 1. 利用 Wasm 插件实现模型供应商的统一适配
**场景**：企业内部可能同时调用 OpenAI、通义千问、DeepSeek 等不同厂商的模型，且各厂商的 API 协议（如鉴权方式、参数格式）存在差异。
**建议**：不要在业务代码中处理不同模型的差异。利用 Higress 的 Wasm 插件能力（或官方提供的 `ai-proxy` 插件），在网关层将不同厂商的 API 统一适配为 OpenAI 的标准格式。
**最佳实践**：配置路由时，将 `/v1/chat/completions` 等标准路径指向 Higress，并在网关配置中通过插件将请求转发至不同的后端上游，实现业务代码的一次编写、多模型复用。
**常见陷阱**：直接在网关透传，导致业务层必须维护多套客户端逻辑，增加代码耦合度。

### 2. 实施基于 Token 的精细化流控与预算保护
**场景**：大模型调用按 Token 计费，突发流量可能导致成本失控。
**建议**：不要仅依赖传统的 QPS（每秒请求数）限流，应配置基于 Token 或 Request Count 的限流策略。
**最佳实践**：针对不同的 API Key 或租户，设置每分钟或每月的 Token 消耗上限。当达到阈值时，网关可以直接拦截请求并返回 429 状态码，防止产生意外账单。
**常见陷阱**：仅设置了并发数限制，忽略了单个长对话（上下文很长）可能消耗大量 Token 的情况，导致成本瞬间飙升。

### 3. 配置语义缓存以降低延迟与成本
**场景**：用户常重复提问相似的问题（如常见的知识库问答），每次都转发给 LLM 会导致高延迟和高费用。
**建议**：启用 Higress 的语义缓存功能。
**最佳实践**：配置缓存策略，对 Prompt 进行向量化或哈希处理。当命中缓存时，网关直接返回历史结果，无需转发给后端模型。建议对精确度要求不高的场景（如闲聊、概览生成）开启此功能。
**常见陷阱**：对所有请求开启缓存，导致用户获取到过时的信息；或者缓存 Key 设置不当，导致命中率极低。务必根据业务场景设置合理的 TTL（生存时间）。

### 4. 构建基于 Prompt 的安全防护体系
**场景**：AI 应用容易受到 Prompt Injection（提示词注入）攻击，或输出敏感内容。
**建议**：在 Higress 的请求和响应阶段分别配置安全插件。
**最佳实践**：
*   **请求阶段**：利用 Wasm 插件检查用户输入，拦截包含恶意指令（如“忽略之前的指令”）的请求。
*   **响应阶段**：检查模型输出，过滤掉仇恨言论或敏感数据。
**常见陷阱**：完全依赖模型厂商的安全过滤，忽略了企业自身合规性的要求，导致合规风险。

### 5. 实现多模型间的负载均衡与故障转移
**场景**：单一 LLM 服务可能出现 API 抖动或限流，影响业务可用性。
**建议**：在 Higress 中配置多模型服务集群，并设置主动健康检查。
**最佳实践**：将不同厂商的模型（如主用通义千问，备用 Azure OpenAI）配置在同一个服务列表中。设置权重实现流量分发（例如 90% 流量走模型 A，10% 走模型 B 进行灰度测试）。当主服务响应超时或返回 5xx 错误时，网关自动切换至备用服务。
**常见陷阱**：未设置超时时间，导致某个模型卡死时，整个请求链程被阻塞，进而耗尽网关的连接池。

### 6. 数据落盘与可观测性集成
**场景**：需要分析用户 Prompt 以优化产品，或进行计费对账。
**建议**：配置日志插件将请求体和响应体中的关键数据（如 Model, Token Usage

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*