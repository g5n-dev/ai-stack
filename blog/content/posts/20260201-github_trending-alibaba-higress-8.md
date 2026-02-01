---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-01T08:16:19+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "WASM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是对 **Higress** 项目的简洁总结： **项目概况** * **名称**：Higress * **开发方**：阿里巴巴 * **定位**：AI Native API Gateway（AI 原生 API 网关） * **编程语言**：Go * **社区热度**：GitHub 星标数约 7,"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "DevOps/运维"]
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在为云原生应用与大模型场景提供统一的流量管理入口。它不仅继承了传统 API 网关在微服务路由与 Kubernetes Ingress 方面的能力，更针对 LLM 应用进行了深度优化，支持 AI 网关特性及 MCP 服务器托管。本文将梳理其架构设计，并重点介绍 WASM 插件体系及其在 AI 场景下的核心功能。

---
## 摘要

基于您提供的内容，以下是对 **Higress** 项目的简洁总结：

**项目概况**
*   **名称**：Higress
*   **开发方**：阿里巴巴
*   **定位**：AI Native API Gateway（AI 原生 API 网关）
*   **编程语言**：Go
*   **社区热度**：GitHub 星标数约 7,419。

**核心定义**
Higress 是一个基于 **Istio** 和 **Envoy** 构建的云原生 API 网关。它通过引入 **WebAssembly (WASM)** 插件能力进行了扩展，将控制面（配置管理）与数据面（流量处理）分离。其架构支持配置变更通过 xDS 协议在毫秒级内生效且无连接中断，特别适用于 AI 流式响应等长连接场景。

**三大核心功能与用途**

1.  **AI 网关**
    *   **用途**：为大语言模型（LLM）应用提供统一接口。
    *   **能力**：支持 30+ LLM 提供商，提供协议转换、可观测性、缓存及安全防护。
    *   **组件**：`ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件。

2.  **MCP 服务器托管**
    *   **用途**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务。
    *   **组件**：`mcp-router`、`jsonrpc-converter` 过滤器以及 `quark-search`、`amap-tools` 等实现。

3.  **Kubernetes Ingress**
    *   **用途**：作为 Kubernetes Ingress 控制器，兼容 nginx-ingress 注解，处理微服务路由。
    *   **组件**：`higress-controller`。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的云原生网关，它成功地将**云原生流量治理**与**AI 原生生态**融合，不仅解决了传统 API 网关的扩展性痛点，更精准地击中了 LLM（大模型）应用落地中的流量与协议管理难题。它不仅是一个技术产品，更是阿里巴巴在 AI 时代对流量基础设施这一层的关键布局，具有极高的工程落地价值。

**深入评价依据**

**1. 技术创新性：基于 WASM 的“可插拔”架构与 AI 深度集成**
*   **事实**：DeepWiki 指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。同时，它明确提出了“AI Gateway”和“MCP (Model Context Protocol) Server Hosting”的概念。
*   **推断**：Higress 的核心差异化在于其**“WASM 优先”的架构设计**。传统网关（如早期的 Nginx 或 Kong）扩展插件通常需要 C++ 编写或嵌入 Lua，开发门槛高且安全性隔离差。Higress 利用 WASM 的沙箱特性，允许开发者使用 Go/Python/JS 等高级语言编写插件，实现了**业务逻辑与网关内核的解耦**，这极大地降低了定制化开发的门槛并提升了安全性。
*   **AI 特性**：针对 AI 场景，Higress 并没有止步于简单的流量转发，而是直接集成了 LLM 的语义理解与路由能力（如 Prompt 模板管理、Token 计费、多模型切换）。特别是对 MCP 协议的支持，表明它致力于成为 AI Agent 的基础设施，而不仅仅是 HTTP 的路由器。

**2. 实用价值：填补“AI 落地”的中间层空白**
*   **事实**：文档提到它提供“Kubernetes Ingress”和“微服务路由”功能，同时强调“AI Gateway features for LLM applications”。
*   **推断**：在当前的 AI 落地阶段，企业面临一个关键痛点：**大模型的不稳定性与私有数据的隔离性**。Higress 解决了这个问题，它作为中间层，能够对上屏蔽不同模型厂商（OpenAI, 通义千问, Llama 等）的 API 差异，对下保护后端业务系统。
*   **应用场景**：它非常适合**企业级 AI 应用平台**。例如，企业可以通过 Higress 统一管理所有部门的 LLM 调用，进行统一的鉴权、限流和 Prompt 注入，而无需修改每一行业务代码。这种“非侵入式”的升级路径，使其具有极高的实用价值。

**3. 代码质量与架构：云原生标准的继承与演进**
*   **事实**：项目使用 Go 语言编写，星标数 7,419，架构上分离了控制平面和数据平面。
*   **推断**：基于 Istio 和 Envoy 意味着 Higress 继承了业界**最成熟的数据平面技术**。Envoy 的高性能 C++ 网络处理能力结合 Go 语言编写控制面的易维护性，是当前云原生基础设施的黄金组合。从 README 的多语言支持（中/日/英）和详细的文档结构来看，项目具备**企业级软件的规范度**。Go 语言的使用也保证了在处理高并发控制逻辑时的性能与开发效率的平衡。

**4. 社区活跃度与生态：阿里背书的强有力驱动**
*   **事实**：作为阿里巴巴开源的项目，拥有 7k+ 的 Star。
*   **推断**：虽然无法直接看到最近的 Commit 记录，但阿里巴巴的开源项目通常有较强的内部业务支撑（如淘宝、天猫的流量治理实践），这意味着项目不会轻易烂尾。社区方面，由于切中了“AI + 网关”的热点，吸引了大量关注 AI 基础设施的开发者。其 WASM 插件市场如果能形成规模，将构建起强大的护城河。

**5. 潜在问题与改进建议**
*   **复杂度挑战**：引入 Istio 和 Envoy 意味着运维复杂度的提升。对于小型团队或非 K8s 环境，Higress 可能显得过于厚重。
*   **建议**：虽然 WASM 性能尚可，但相比原生 C++ 模块仍有损耗。建议在文档中提供更详尽的 WASM 插件性能基准测试数据，以便开发者做出权衡。此外，MCP 协议尚在演进中，Higress 需保持对协议更新的敏锐跟进。

**对比优势**

*   **对比 Nginx/Kong**：Higress 原生支持 K8s Ingress 和 Service Mesh 架构，且 WASM 插件模型比 Lua (Nginx) 或 Go (Kong) 插件具有更好的隔离性和安全性。
*   **对比 APISIX**：两者均为高性能网关，但 Higress 在 AI 领域的集成（如 Prompt 管理、MCP 支持）更为激进和深入，更适合 AI 原生应用。

**边界条件与验证清单**

**不适用场景**：
*   极简单的流量转发需求（使用 Nginx 足矣）。
*   非 Kubernetes 环境且资源极度受限的边缘节点。
*   需要极低延迟（微秒级）的高频交易场景（WASM 和 Envoy 层级可能引入额外抖动）。

**快速验证

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文将从架构设计、功能实现、技术细节、适用场景及工程哲学等维度进行深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构采用了**控制平面与数据平面分离**的云原生模式，这是典型的 Istio/Envoy 演进架构。
*   **数据平面**：基于 **Envoy** 构建。Envoy 是高性能的 C++ 网络代理，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **控制平面**：使用 **Go** 语言开发。它向下通过 xDS 协议（包括 LDS, RDS, CDS 等）驱动 Envoy，向上通过 Kubernetes Ingress 或 Gateway API 标准接收用户配置。
*   **扩展层**：引入了 **WebAssembly (WASM)** 作为插件运行时。这使得 Higress 能够在不重启代理的情况下动态扩展功能，且插件可以使用 C++/Rust/Go/AssemblyScript 等多种语言编写。

### 核心模块与关键设计
1.  **AI 网关层**：这是 Higress 最具差异化的模块。它不仅仅是流量转发，更在网关层集成了 LLM 的处理逻辑。
2.  **MCP (Model Context Protocol) 服务器托管**：Higress 能够作为 MCP Server 的托管点，这是为了适配 AI Agent 的工具调用场景，打通了 AI 应用与外部数据/工具的连接。
3.  **配置分发系统**：基于 Istio 的 Pilot 模块进行了深度定制，优化了配置推送的延迟和稳定性。

### 技术亮点与创新点
*   **AI Native 原生集成**：传统的 API 网关（如 Nginx, Kong）主要处理 HTTP/gRPC，而 Higress 原生理解 LLM 协议（如 OpenAI 协议）。它能在网关层处理 Prompt 模板管理、Token 计费、流式响应（SSE）处理，甚至实现简单的多模型路由。
*   **WASM 插件市场**：Higress 内置了丰富的 Wasm 插件生态，利用 Wasm 的沙箱隔离性和高性能，解决了传统 Lua 插件（如 OpenResty）在并发安全和稳定性上的痛点。
*   **毫秒级配置热更新**：得益于 xDS 协议的增量推送机制，配置变更可以在不中断长连接（如 AI 对话中的 SSE 连接）的情况下生效。

### 架构优势分析
*   **低延迟**：数据平面使用 Envoy (C++)，性能损耗极低。
*   **高扩展性**：WASM 插件机制允许用户像写业务代码一样扩展网关功能，而无需修改网关内核。
*   **云原生亲和**：直接作为 Kubernetes Ingress Controller 部署，与 K8s 生态无缝融合。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **Provider 路由**：根据请求内容或元数据，将请求路由到不同的 LLM 提供商（如 OpenAI, Azure, 通义千问等）。
    *   **Token 计数与限流**：在网关层计算 Token 消耗，实现基于 Token 的精细化限流和配额管理。
    *   **结果缓存**：对相同的 Prompt 进行缓存，直接返回结果，降低后端 LLM 成本。
    *   **敏感词过滤**：在请求发送给 LLM 前或返回给用户前进行内容审核。
2.  **传统 API 网关**：支持 K8s Ingress、微服务路由、金丝雀发布、负载均衡。
3.  **MCP 协议支持**：作为 AI Agent 的工具层，将后端服务封装为 MCP 标准接口供 Agent 调用。

### 解决的关键问题
*   **LLM 接入碎片化**：企业内部可能同时使用多种模型，Higress 提供了统一的接入层，屏蔽了底层 Provider 的差异。
*   **流式响应处理**：LLM 通常返回 SSE 流，传统网关在处理流式转发时的缓冲策略可能导致首字延迟高或连接中断。Higress 针对长连接和流式传输进行了优化。
*   **AI 应用的可观测性**：自动记录 Prompt 和 Response，便于追踪和调试 AI 应用行为。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **核心语言** | Go (控制) + C++ (数据) | Go/Lua (数据) | Lua (数据) | C (数据) |
| **AI 原生支持** | **强** (内置 Provider 路由/Token 管理) | 弱 (需插件) | 弱 (需插件) | 无 |
| **扩展机制** | **WASM** (高性能/多语言) | Plugin (Lua/PJS) / WASM (Beta) | Lua / WASM | C Module / Lua |
| **配置热更新** | 是 (xDS) | 是 | 是 | 是 (Nginx Plus/Reload) |
| **K8s 集成** | 原生 Ingress | 需 KIC | 原生 Ingress | 需 Ingress Controller |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件加载**：Higress 使用 Proxy-WASM 规范。当 Go 控制平面下发配置时，会将 Wasm 插件代码推送到 Envoy。Envoy 在沙箱中执行这些代码，通过 `on_request_headers`、`on_body` 等钩子函数修改请求或响应。
*   **AI 流式处理**：在处理 SSE (Server-Sent Events) 时，Higress 的数据平面配置了流式缓冲策略。它不会等待整个响应结束才转发，而是以 Chunk 为单位实时转发，这对于 ChatGPT 类型的对话体验至关重要。

### 代码组织结构
*   **Pilot (pkg/control-plane)**：负责 xDS 协议的实现，将 K8s CRD 或控制台配置转换为 Envoy 能理解的配置格式。
*   **Router (pkg/router)**：核心路由逻辑，包括 AI 特定的路由匹配。
*   **Wasm Plugins (plugins)**：存放预置的 Wasm 插件源码。

### 性能优化与扩展性
*   **全异步 I/O**：基于 Envoy 的事件循环模型，无阻塞。
*   **零拷贝**：在数据平面尽可能减少内存拷贝。
*   **水平扩展**：控制平面与数据平面解耦，数据平面可以任意扩容 Pod 数量以应对高并发流量。

---

## 4. 适用场景分析

### 适合的项目
1.  **AI 应用开发平台**：企业内部构建类似 ChatGPT 的应用，需要统一管理对 OpenAI、阿里云等模型的调用。
2.  **微服务网关**：需要高性能、可扩展的 K8s Ingress Controller，且对云原生有强依赖。
3.  **SaaS 提供商**：需要基于 Token 计费或对 API 调用进行精细化管理的场景。

### 最有效的场景
当你的系统**高度依赖 Kubernetes**，且**大量使用 LLM 能力**时，Higress 是目前最优选。它能将 AI 流量治理与微服务流量治理合二为一，避免维护两套网关。

### 不适合的场景
1.  **非 K8s 环境**：如果你还在使用虚拟机或物理机部署，Higress 的部署复杂度会急剧上升（虽然支持，但非首选）。
2.  **极端静态配置**：如果配置几年不变，使用 Nginx 可能更简单轻量。
3.  **对资源极其敏感**：Envoy 本身比 Nginx 占用更多内存，如果是边缘设备（如嵌入式网关），可能过于重。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 协议理解**：从简单的转发发展到 Prompt 注入、RAG（检索增强生成）网关化，即网关直接连接向量数据库进行预处理。
*   **Dapr 集成**：作为服务间调用的基础设施，与 Dapr 结合实现更完善的分布式服务治理。

### 社区反馈与改进空间
*   **文档与易用性**：虽然阿里开源，但部分文档对非中文用户不够友好，控制台 UI 的交互逻辑仍有优化空间。
*   **Wasm 生态**：目前 Wasm 插件的开发门槛相对较高（相比 Python 脚本），未来可能需要更低代码的插件定义方式。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的运维/架构师。
*   对云原生网关、Service Mesh (Istio) 感兴趣的后端开发。
*   需要落地 AI 应用基础设施的技术负责人。

### 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 概念，了解 Envoy 基本原理（Listener, Filter, Cluster）。
2.  **进阶**：阅读 Higress 官方文档，尝试在本地 Kind 集群部署。
3.  **实践**：编写一个简单的 Wasm 插件（如修改请求头），并在 Higress 中加载。
4.  **深入**：研究 Higress 如何实现 AI Provider 的路由转发，阅读 `pkg/router` 相关源码。

---

## 7. 最佳实践建议

### 正确使用指南
*   **资源限制**：在 K8s 中为 Higress Gateway 设置合理的 CPU/Memory limits，因为 Wasm 插件的执行会消耗额外内存。
*   **配置隔离**：生产环境建议将 AI 流量网关与传统微服务网关分开部署（使用不同的 Gateway Class），以免 AI 流量的长连接占用过多资源影响普通业务。

### 常见问题与解决
*   **Wasm 插件导致网关 Crash**：确保插件代码中没有死循环，且内存使用在限制范围内。利用 Higress 的插件调试功能进行本地测试。
*   **长连接超时**：AI 请求可能耗时较长，需调整 Gateway 的 `streamIdleTimeout` 等超时配置，避免网关提前断开连接。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在抽象层上做了**“流量治理与业务逻辑中间态”**的尝试。
*   **传统网关**：只管网络层（L4/L7）。
*   **业务代码**：管逻辑（Prompt 拼接、模型选择）。
*   **Higress**：把“模型选择”、“Token 计算”、“简单的 Prompt 转换”提升到了网关层。
*   **复杂性转移**：它将**业务逻辑的复杂性**部分转移给了**网关配置**。这意味着，网关运维人员现在需要理解 LLM 的概念（如 Token,

---
## 代码示例




```python
# 示例1：Higress WasmPlugin 配置生成
def generate_wasm_plugin_config():
    """
    生成 Higress WasmPlugin 的 YAML 配置
    解决问题：为 Higress 网关配置 Wasm 插件
    """
    config = {
        "apiVersion": "extensions.higress.io/v1alpha1",
        "kind": "WasmPlugin",
        "metadata": {
            "name": "my-wasm-plugin",
            "namespace": "default"
        },
        "spec": {
            "url": "oci://registry.example.com/wasm/plugin:latest",
            "sha256": "abc123...",  # 插件文件的 SHA256 校验和
            "phase": "AUTHN",  # 插件执行阶段：AUTHN/AUTHZ/DEFAULT
            "priority": 100,  # 插件优先级
            "config": {  # 插件配置参数
                "log_level": "info",
                "custom_header": "X-Custom-Header"
            }
        }
    }
    return config

# 使用示例
plugin_config = generate_wasm_plugin_config()
print("生成的 WasmPlugin 配置：")
print(plugin_config)
```




```python
# 示例2：Higress 路由规则配置
def create_higress_route():
    """
    创建 Higress 路由规则
    解决问题：定义 HTTP 路由规则，将请求转发到不同服务
    """
    route = {
        "apiVersion": "networking.higress.io/v1",
        "kind": "HttpRoute",
        "metadata": {
            "name": "example-route",
            "namespace": "default"
        },
        "spec": {
            "hosts": ["example.com"],  # 匹配的域名
            "paths": ["/api/*"],  # 匹配的路径
            "methods": ["GET", "POST"],  # 匹配的 HTTP 方法
            "destination": {  # 目标服务配置
                "service": {
                    "name": "backend-service",
                    "namespace": "default",
                    "port": 8080
                },
                "weight": 100  # 流量权重（用于灰度发布）
            },
            "timeout": "10s",  # 请求超时时间
            "retries": 3  # 重试次数
        }
    }
    return route

# 使用示例
route_config = create_higress_route()
print("创建的路由规则：")
print(route_config)
```




```python
# 示例3：Higress 流量镜像配置
def configure_traffic_mirror():
    """
    配置 Higress 流量镜像
    解决问题：将生产流量复制到测试环境，用于测试和监控
    """
    mirror_config = {
        "apiVersion": "networking.higress.io/v1",
        "kind": "TrafficMirror",
        "metadata": {
            "name": "prod-mirror",
            "namespace": "default"
        },
        "spec": {
            "source": {  # 源服务配置
                "service": "production-service",
                "namespace": "prod",
                "port": 80
            },
            "mirror": {  # 镜像目标配置
                "service": "test-service",
                "namespace": "test",
                "port": 80,
                "percentage": 10  # 镜像 10% 的流量
            },
            "headers": {  # 添加的请求头
                "X-Mirror-Source": "production"
            }
        }
    }
    return mirror_config

# 使用示例
mirror = configure_traffic_mirror()
print("配置的流量镜像规则：")
print(mirror)
```


---
## 案例研究


### 1：阿里巴巴集团内部核心业务（如淘天集团）

 1：阿里巴巴集团内部核心业务（如淘天集团）

**背景**:
在阿里巴巴内部，微服务架构极其复杂，数千个服务之间存在大量的 RPC 调用和 HTTP 流量。随着业务向云原生架构演进，传统的 Nginx+Lua 网关在维护性、扩展性和云原生集成方面面临挑战。集团需要一个能够统一管理流量、支持 K8s Ingress、并且能够与内部服务治理体系（如 Dubbo、Nacos）深度融合的网关系统。

**问题**:
1. **技术栈割裂**：旧网关难以同时处理传统的微服务调用（如 HTTP/Dubbo）和现代化的云原生 Ingress 流量。
2. **性能瓶颈**：在大促场景下，配置热更新和路由匹配的效率需要极致优化。
3. **扩展性困难**：业务逻辑（如鉴权、限流）通过硬编码方式实现，迭代周期长，难以支持业务方的快速自定义需求。

**解决方案**:
阿里巴巴基于内部多年沉淀的网关经验，开源并自研了 **Higress**。
1. **统一接入层**：Higress 被部署为云原生网关，替代了部分传统的 Ingress Controller 和 API 网关，实现了南北向（外部流量进入）与东西向（服务间调用）流量的统一治理。
2. **Wasm 插件生态**：利用 Higress 对 WebAssembly (Wasm) 的原生支持，将业务逻辑（如请求验证、流量镜像）编写为 Wasm 插件。这使得业务团队可以使用 C/C++/Go/Rust 等语言编写逻辑，而无需修改网关核心代码，且插件支持热加载，无需重启网关。
3. **服务发现集成**：深度集成了 Nacos 和 Zookeeper，实现了从注册中心动态获取服务实例，配合 K8s Service 实现了混合云环境下的服务路由。

**效果**:
1. **性能提升**：在阿里内部大促场景中，Higress 展现出了极高的吞吐量和低延迟，相比传统网关，资源利用率显著提高。
2. **研发效率**：通过 Wasm 插件市场，业务方实现了逻辑的模块化复用，新功能的上线时间从“周”级缩短至“小时”级。
3. **架构统一**：成功打通了容器云与非容器云的流量治理壁垒，简化了基础设施的运维复杂度。

---



### 2：某大型互联网科技公司 AI 业务网关

 2：某大型互联网科技公司 AI 业务网关

**背景**:
随着 AIGC（生成式 AI）的爆发，该公司的 AI 平台需要对外提供大模型服务。客户端包括 Web 端、移动端以及内部 SaaS 应用，调用协议涉及标准的 OpenAI 格式以及自研协议。

**问题**:
1. **协议转换繁琐**：后端模型服务通常使用 gRPC 或自定义协议，而前端期望使用标准的 HTTP/JSON，网关层需要处理复杂的协议转换逻辑。
2. **鉴权与计费复杂**：AI 调用成本高昂，需要基于 Token（Tokenization）进行精确的计费和限流，而传统的 API 网关通常仅基于请求数或 QPS 限流，无法感知 AI 语义层面的 Token 消耗。
3. **内容安全**：需要在网关层拦截 Prompt 注入攻击或不合规的输出内容。

**解决方案**:
引入 **Higress** 作为 AI 专用网关（AI Gateway）。
1. **AI 协议转换**：使用 Higress 内置的 AI 特性，将标准的 HTTP OpenAPI 请求无缝转换为后端模型服务的 gRPC 调用，并对返回结果进行 HTTP 封装。
2. **Token 级别流控**：利用 Higress 的 Wasm 插件能力，在网关层解析请求体和响应体，统计实际消耗的 Token 数量，并基于 Token 进行精细化限流和配额管理，防止资源滥用。
3. **安全拦截**：部署轻量级 Wasm 插件，在请求转发前分析 Prompt 敏感词，在响应返回前过滤模型输出的违规内容。

**效果**:
1. **业务敏捷性**：前端开发团队无需关心后端模型的协议差异，直接调用标准接口，大大降低了接入门槛。
2. **成本控制**：实现了基于真实使用量（Token 数）的后付费计费模式，有效拦截了恶意刷接口和异常流量，节省了昂贵的 GPU 算力成本。
3. **合规性保障**：通过网关层统一的内容过滤，确保了对外服务的合规性，降低了业务侧的法律风险。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx + Lua (OpenResty) | Kong |
|------|----------------|------------------------|------|
| 性能 | 高性能，基于 Rust 和 Go 构建，支持高并发 | 极高性能，C 语言核心，轻量级 | 高性能，基于 OpenResty，但受 Lua 限制 |
| 易用性 | 提供可视化控制台，支持 K8s Ingress，配置简单 | 需手动编写 Lua 脚本，学习曲线陡峭 | 提供管理界面，但配置复杂，需熟悉插件机制 |
| 成本 | 开源免费，云服务按需付费 | 完全开源免费，无额外成本 | 开源版免费，企业版收费 |
| 扩展性 | 支持 WASM 插件，扩展灵活 | 需编写 Lua 模块，扩展性有限 | 支持插件扩展，但需 Lua 开发 |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，资源丰富 | 社区活跃，插件生态完善 |

### 优势分析

- 优势1：基于 Rust 和 Go 构建，性能优于传统 Lua 方案。
- 优势2：提供可视化控制台和 K8s 集成，降低运维复杂度。
- 优势3：支持 WASM 插件，扩展性更强，适合云原生场景。

### 不足分析

- 不足1：社区生态不如 Nginx 和 Kong 成熟，插件数量较少。
- 不足2：Rust 和 Go 的学习曲线可能对部分开发者有门槛。
- 不足3：云服务依赖阿里云生态，多云部署可能受限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ingress 转换实现平滑迁移

**说明**: Higress 提供了强大的 Ingress 注解转换能力，可以将 Kubernetes 原生的 Ingress 资源自动转换为 Higress 的网关路由配置。这对于希望从 Nginx Ingress Controller 或其他标准 Ingress 控制器迁移到 Higress 的用户至关重要，能够最大程度复用现有的 CI/CD 流程和 YAML 配置，降低迁移门槛。

**实施步骤**:
1. 在 Higress 控制台或通过 Helm 安装时，确保开启了 Ingress API 的监听支持。
2. 保持现有 Kubernetes Ingress YAML 文件不变，直接部署到 Higress 所在的集群。
3. 使用 Higress 提供的注解（如 `higress.io/override`）对特定路由进行微调，以利用 Higress 的高级特性（如更精确的 Header 匹配）。
4. 逐步验证流量路由是否符合预期，确认无误后下线旧的网关组件。

**注意事项**: 确保 Higress 版本与 Kubernetes API 版本兼容，注意 Ingress Class 的配置，避免与集群内原有的 Ingress Controller 冲突。

---

### 实践 2：配置 WAF 插件防护安全漏洞

**说明**: Higress 原生支持 WAF（Web Application Firewall）插件，能够有效防御 SQL 注入、XSS、恶意扫描等常见 Web 攻击。作为网关层面的安全防线，配置 WAF 比在应用层修复漏洞更高效，是保障生产环境安全的必要手段。

**实施步骤**:
1. 登录 Higress 控制台，进入“插件市场”。
2. 搜索并启用“WAF 插件”。
3. 根据业务类型选择防护规则集（例如，启用 SQL 注入防御和 XSS 防御）。
4. 配置拦截模式（监控模式或阻断模式），建议先开启监控模式观察误报率，确认无误后切换为阻断模式。

**注意事项**: WAF 规则的更新可能滞后于新出现的漏洞，建议定期检查插件更新。开启阻断模式前务必进行充分的回归测试，防止误拦截正常业务流量。

---

### 实践 3：使用 WASM 插件扩展业务逻辑

**说明**: Higress 基于 C++ 构建，但通过 Proxy-WASM 标准支持高性能的扩展能力。开发者可以使用 Go、C++、Rust 或 JavaScript 编写插件来处理认证、限流、请求修改等逻辑，而无需修改网关核心代码或重新部署网关服务。

**实施步骤**:
1. 确定业务需求（如：实现一个基于特定 Header 的请求路由）。
2. 使用 Go 或 Rust 编写 WASM 插件代码，利用 Higress 提供的 SDK。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台的插件管理中，或配置 OCI 远程加载。
4. 在指定路由或全局范围内启用该插件，并配置相关参数。

**注意事项**: WASM 插件虽然隔离性好，但高计算复杂度的逻辑仍会增加延迟。避免在插件中进行阻塞式网络调用，尽量使用异步非阻塞处理。

---

### 实践 4：配置全局限流与服务熔断

**说明**: 在流量突增或下游服务不稳定时，网关层面的限流和熔断是保护后端服务的最后一道屏障。Higress 支持基于请求速率、并发连接数的限流，以及对异常实例的自动摘除（熔断），防止雪崩效应。

**实施步骤**:
1. **限流配置**: 在需要保护的路由配置中，启用“限流”插件，设置每秒请求数（QPS）或突发令牌桶阈值。
2. **熔断配置**: 配置服务来源（Service Entry）或目标服务的健康检查策略，设定连续失败次数阈值。
3. 结合 Higress 的原生支持，配置自动降级策略，当服务响应时间超过设定阈值时触发熔断。

**注意事项**: 限流阈值应根据压测结果设定，而非随意估算。熔断后的恢复策略（如半开状态）需妥善配置，避免恢复瞬间流量击垮恢复中的服务。

---

### 实践 5：对接云原生观测体系

**说明**: Higress 原生支持 Prometheus 监控指标和 OpenTelemetry 链路追踪。为了全面掌握网关的运行状态（如 QPS、延迟、错误率）并进行故障排查，必须将其接入现有的可观测性平台（如 Grafana + Prometheus 或 Jaeger）。

**实施步骤**:
1. 在部署 Higress 时，通过环境变量或 Helm Values 开启 Prometheus Metrics 端口（通常为 15020）和 Access Log 输出。
2. 配置 Prometheus 抓取 Higress 的 Pod 指标。
3. 导入 Higress 官方提供的 Grafana 仪表盘模板，可视化监控数据。
4. 若需链

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 Wasm 插件替代 Lua 插件

**说明**: Higress 支持 Wasm (WebAssembly) 和 Lua 两种插件扩展方式。Wasm 插件运行在独立的沙箱内存池中，具有接近原生代码的执行效率，且具备更好的隔离性，不会阻塞主线程。相比之下，Lua 插件由于受限于 Lua VM 的协程调度和 GC 机制，在高并发下更容易成为性能瓶颈。

**实施方法**:
1. 将现有的 Lua 插件逻辑使用 C++/Rust/Go (TinyGo) 重写为 Wasm 格式。
2. 在 Higress 控制台或通过 WasmPlugin 资源对象加载 `.wasm` 文件。
3. 配置插件生效阶段（如 `HTTP_FILTER` 阶段）。

**预期效果**: 插件执行延迟降低 30%-50%，在高并发场景下 P99 延迟提升明显。

---

### 优化 2：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，在弱网环境下连接建立速度更快，吞吐量更高。对于 Higress 作为网关接入移动端或跨地域流量的场景，启用 HTTP/3 能显著提升连接成功率和传输速度。

**实施方法**:
1. 在 Higress 的网关监听器配置中，为端口 443 开启 HTTP/3 支持。
2. 确保证书配置正确，HTTP/3 依赖 TLS 1.3。
3. 配置 Alt-Svc 请求头，引导浏览器自动升级协议。

**预期效果**: 弱网环境下页面加载速度提升 20%-40%，连接建立时间减少 1 个 RTT。

---

### 优化 3：配置全链局 DNS 缓存与连接池复用

**说明**: 默认的 DNS 解析和连接建立开销较大。通过配置 Higress 的 Upstream 连接池参数和 DNS 缓存，可以减少频繁的 TCP 握手和 DNS 查询带来的延迟。

**实施方法**:
1. 在 `Ingress` 或 `Gateway` 资源中调整 Upstream 的 `idleTimeout` 和 `max` 连接数，保持长连接。
2. 开启 Higress 的 DNS 缓存功能，设置合理的 TTL（如 60s）。
3. 确保后端服务开启了 HTTP Keep-Alive。

**预期效果**: 后端服务响应延迟减少 10%-20ms，CPU 上下文切换开销降低。

---

### 优化 4：调整 Worker 进程数与 CPU 亲和性

**说明**: Higress 基于 Envoy，采用多线程架构。默认配置可能未完全匹配宿主机的 CPU 核心数，导致上下文切换频繁或负载不均。通过精确配置 Worker 数量并绑定 CPU 核心，可以最大化利用硬件资源。

**实施方法**:
1. 将 Higress 的 `concurrency` (Worker 线程数) 设置为与宿主机 CPU 核心数一致（或设置为 `auto`）。
2. 在容器启动参数中配置 `cpuset`，将 Higress Pod 绑定到特定的 CPU 核心上，避免与系统其他进程争抢资源。

**预期效果**: 吞吐量（QPS）提升 15%-25%，系统负载更加平稳。

---

### 优化 5：启用日志采样与异步上报

**说明**: 在高流量场景下，全量日志访问会带来巨大的磁盘 I/O 压力和网络带宽消耗，甚至阻塞业务处理。通过采样和异步上报，可以在保留关键链路追踪信息的同时，大幅降低系统开销。

**实施方法**:
1. 配置 Higress 的 Access Log 采样率（如设置为 10% 或根据流量动态调整）。
2. 使用 OpenTelemetry 或类似协议将日志发送至 Kafka/SLS 时，采用批量发送和异步 Buffer 机制。
3. 对于 Trace 采样，仅在请求出错或延迟超过阈值时记录详细日志。

**预期效果**: 磁盘 I/O

---
## 学习要点

- 根据提供的信息（GitHub 趋势中的阿里 Higress 项目），总结关键要点如下：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接云原生基础设施。
- 该项目将高流量场景的治理能力与开源生态相结合，提供了企业级的流量管理与安全防护。
- Higress 支持将传统的 Nginx Ingress 配置无损迁移，降低了用户的迁移门槛。
- 它具备强大的插件扩展能力（Wasm 插件），允许开发者通过 Lua 或 Go 灵活扩展网关功能。
- 项目旨在打通微服务网关与 API 网关的界限，实现南北向与东西向流量的统一治理。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关的基本概念
- Higress 的核心架构与设计理念（基于 Envoy 和 Istio）
- 基本术语：Ingress、Gateway、路由、服务发现
- Higress 与传统 API 网关（如 Nginx, Kong）的区别
- Docker 环境下 Higress 的快速安装与部署

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：快速开始与核心概念
- Envoy 官方文档基础部分（理解数据平面）

**学习建议**:
- 建议先理解微服务架构中流量管理的痛点，再学习 Higress 的解决方案。
- 动手实践：在本地 Docker 环境中搭建 Higress，并配置一个最简单的 HTTP 路由转发。

---

### 阶段 2：流量治理与配置管理

**学习内容**:
- 详细的流量路由配置（基于路径、头部、参数的转发）
- 负载均衡策略配置（轮询、随机、最小连接等）
- 服务注册与发现集成（Nacos, Consul, Kubernetes Service）
- 金丝雀发布与蓝绿发布实战
- 全局与局部流量控制（限流、熔断、重试）
- Waf 防火墙基础插件的使用

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：流量路由与插件市场
- Kubernetes Ingress 资源配置规范
- Higress 控制台操作指南

**学习建议**:
- 熟悉控制台（Console）和 Kubernetes YAML 两种配置方式。
- 尝试将一个后端服务接入 Higress，并配置超时、重试和限流策略，观察效果。
- 深入理解“插件”机制，这是 Higress 扩展能力的核心。

---

### 阶段 3：插件开发与生态集成

**学习内容**:
- Higress 插件体系（Wasm 插件与 Go/C++ 插件）
- 使用 Lua 或 Go (Wasm) 开发自定义插件
- 插件的热加载与配置管理
- Higress 与 Istio 生态的集成（MCP 协议对接）
- OpenAPI 管理与多协议支持（Dubbo, gRPC）
- 安全认证（OIDC, API Key, JWT）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：开发者指南与 Wasm 插件开发
- Higress GitHub 仓库中的示例插件代码
- WebAssembly (Wasm) 基础教程

**学习建议**:
- 从修改官方现成的插件开始，逐步尝试编写简单的自定义逻辑（如请求头修改、简单的鉴权）。
- 学习如何将自定义插件打包并在 Higress 中加载。
- 如果有 Kubernetes 基础，尝试在 K8s 集群中通过 Ingress 注解或 ConfigMap 管理插件配置。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- Higress 的高可用（HA）部署架构
- 性能调优（连接池、缓冲区大小、工作线程数）
- 可观测性：对接 Prometheus/Grafana 监控、链路追踪
- 网关的安全加固（TLS 配置、防 DDoS）
- 灰度发布与回滚策略在生产环境的最佳实践
- 大规模流量场景下的网关容量规划

**学习时间**: 2-3周

**学习资源**:
- Higress 官方博客与运维案例
- Envoy 性能调优指南
- 云原生可观测性最佳实践

**学习建议**:
- 模拟生产环境进行压力测试，分析瓶颈。
- 重点学习日志与监控指标的解读，具备快速排查线上故障的能力。
- 关注 Higress 的版本更新日志，了解新特性与 Bug 修复。

---
## 常见问题


### 1: Higress 是什么？它与 Alibaba 有什么关系？

1: Higress 是什么？它与 Alibaba 有什么关系？

**A**: Higress 是一个基于阿里内部两年多的实战经验，由阿里巴巴开源的云原生 API 网关。它建立在 Envoy 和 Istio 之上，旨在提供标准化、高集成、易扩展、热更新的云原生网关。作为 Alibaba Cloud (阿里云) 旗下的开源项目，它继承了阿里巴巴在电商和双十一大促中积累的流量治理经验，旨在解决 Kubernetes 时代微服务架构下的流量管理问题。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：
1.  **云原生原生集成**：它深度集成了 Kubernetes (K8s) 和 Istio，可以作为 Ingress Controller 使用，也能接管服务网格中的南北向与东西向流量，比传统网关更容易融入 K8s 生态。
2.  **高扩展性**：支持通过 WASM (WebAssembly) 技术编写插件，支持 Go、C++、Rust、JavaScript 等多语言编写业务逻辑，插件可以热更新，无需重启网关，这比传统的 Lua (Nginx) 或 C++ (Kong) 插件开发更安全、灵活。
3.  **标准化与安全**：遵循 OpenAPI 规范，支持 K8s Ingress、Gateway API 等标准，配置迁移成本低。
4.  **高性能**：基于 Envoy 内核，具备极高的性能和资源利用率。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller (如 Nginx Ingress) 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller (如 Nginx Ingress) 进行迁移？

**A**: 是的，Higress 非常重视迁移的便利性。它提供了专门的工具（如 Nginx 配置转换工具）来帮助用户将现有的 Nginx 配置转换为 Higress 的 K8s YAML 配置。同时，Higress 兼容 Kubernetes 的 Ingress API 资源，这意味着对于简单的路由规则，你通常不需要修改配置即可直接使用。对于复杂的流量治理需求，Higress 提供了更丰富的 CRD (自定义资源) 来替代 Nginx 的复杂配置。

---



### 4: 在 Higress 中如何进行插件开发？支持哪些语言？

4: 在 Higress 中如何进行插件开发？支持哪些语言？

**A**: Higress 提供了非常强大的插件扩展能力，主要通过以下方式：
1.  **WASM 插件 (推荐)**：这是 Higress 的特色。由于 Envoy 对 WASM 的支持，开发者可以使用 **Go、TypeScript/JavaScript、Rust、C++** 等语言编写插件逻辑。这些代码会被编译成 WASM 格式，由 Higress 运行时加载。这种方式隔离性好，插件崩溃不会导致网关崩溃，且支持动态加载和卸载。
2.  **Lua 插件**：为了兼容传统 Nginx 生态，Higress 也支持 Lua 脚本，但更推荐使用 WASM 以获得更好的性能和多语言支持。
3.  **原生插件**：对于性能要求极高的场景，也可以直接编写 C++ Envoy Filter，但这通常需要重新编译网关镜像，不如 WASM 灵活。

---



### 5: Higress 能否同时处理外部流量 (南北向) 和内部服务间通信 (东西向)？

5: Higress 能否同时处理外部流量 (南北向) 和内部服务间通信 (东西向)？

**A**: 是的，这是 Higress 的设计初衷之一。它既可以作为 Kubernetes 的 **Ingress Gateway** 处理进入集群的外部流量，也可以作为服务网格中的 **East-West Gateway** 处理服务之间的内部通信。通过与 Istio 的集成，Higress 能够统一管理这两种流量，简化了架构中网关组件的数量，降低了运维复杂度。

---



### 6: Higress 对 Dubbo 和 gRPC 等协议的支持情况如何？

6: Higress 对 Dubbo 和 gRPC 等协议的支持情况如何？

**A**: Higress 对微服务协议有非常深入的支持，特别是针对阿里巴巴生态常用的协议：
1.  **Dubbo**：Higress 原生支持 Dubbo 和 Dubbo3 (Triple) 协议。它能够将 HTTP/JSON 请求转换为 Dubbo 协议调用后端服务，实现网关与后端 Java 服务的无缝对接，支持服务发现、超时、重试等全链路治理。
2.  **gRPC**：完全支持 gRPC 协议，支持 gRPC 到 HTTP/1.1 的协议转换，以及 gRPC Web 的支持，方便浏览器端调用后端 gRPC 服务。
3.  **其他协议**：基于 Envoy 的底层能力，Higress 也支持 TCP、UDP 等四层协议的代理。

---



### 7: Higress 是否有可视化的控制台？如何进行配置管理？

7: Higress 是否有可视化的控制台？如何进行配置管理？

**A**: 是的，Higress 提供了开箱即用的 **K8s Ingress Controller 控制台**。这个控制台不仅支持基本的路由配置，还提供了以下高级功能：
1.  **图形化界面**：可以直观地管理域名、路由规则、服务来源

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础流量管理

### 问题**：Higress 基于 Envoy 构建，但默认配置可能不满足特定需求。请尝试修改 Higress Gateway 的 Pod 副本数，并配置一个简单的路由规则，将所有发往 `/test` 路径的 HTTP 请求流量路由到一个名为 `echo-service` 的后端服务（服务已在集群内运行）。

### 提示**：这涉及 Kubernetes 的基础资源管理（如 Deployment 或 Helm 的 values.yaml）以及 Higress（或 Istio）标准的 VirtualService 配置。关注 `spec.http.match.uri.prefix` 和 `spec.http.route.destination.host` 字段。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 Wasm 插件实现 AI 协议转换与鉴权
Higress 的一大核心优势是基于 C++ Go 的 Wasm 插件生态。在对接大模型（LLM）时，不同厂商的 API 协议（如 OpenAI 格式与通义千问格式）往往存在差异。
*   **实践建议**：不要在业务代码中处理不同模型厂商的接口差异。直接使用 Higress 官方或社区提供的 **AI 代理/路由插件**（如 `ai-proxy`），在网关层完成协议统一、API Key 的轮转与隐藏以及请求头的改写。
*   **常见陷阱**：在网关层处理复杂的 Prompt 模板。虽然可以通过插件实现，但建议仅做简单的路由和鉴权，复杂的 Prompt 工程应保留在业务服务或专门的 Prompt 管理层，以免网关插件逻辑过重影响性能。

### 2. 配置语义缓存以降低 Token 成本与延迟
AI 应用最显著的成本在于 Token 消耗和模型推理延迟。对于高并发或重复性高的问答场景，网关层的缓存至关重要。
*   **实践建议**：启用 Higress 的 **AI 特性缓存**。不同于传统的 HTTP 缓存（仅基于 URL），AI 缓存应基于请求的语义。配置针对 POST 请求的缓存策略，基于请求体中的 Hash 值进行缓存，对于相同的用户问题直接返回网关层的缓存结果，从而大幅减少后端 LLM 的调用次数。
*   **常见陷阱**：缓存时间设置过长导致信息时效性滞后。针对新闻类或时效性强的 RAG（检索增强生成）场景，需谨慎设置 TTL，或者在业务逻辑中允许通过特定 Header 绕过缓存。

### 3. 实施精细化的流量治理与模型熔断
大模型服务通常有严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制，且服务偶现不稳定。
*   **实践建议**：利用 Higress 的 **服务治理能力**，为不同的 LLM 提供者配置细粒度的并发限制和超时设置。结合 **降级规则**，当主模型（如 GPT-4）响应超时或报错时，网关可以自动将请求切换至备用模型（如 GPT-3.5 或开源模型），保证业务的高可用性。
*   **常见陷阱**：忽略了 LLM 流式输出的超时配置。LLM 响应通常较慢，且是流式返回，如果全局超时时间设置过短（如默认的 60s），会导致长回答被中断，需针对 AI 接口单独调整超时策略。

### 4. 敏感数据脱敏与安全防护
在将企业内部数据发送至公有大模型之前，防止数据泄露是重中之重。
*   **实践建议**：部署 Wasm 插件在请求发送至 LLM 之前进行 **PII（个人身份信息）扫描与脱敏**。例如，自动识别并替换用户名、邮箱、身份证号等敏感信息，待模型响应返回后再进行还原（或仅保留脱敏后状态）。
*   **常见陷阱**：仅依赖 IP 白名单作为安全手段。在 AI 场景下，API Key 一旦泄露，攻击者可以轻易盗刷额度。必须结合 Higress 的 JWT 验证或 IDaaS 集成，确保调用网关的每个用户都是经过认证的。

### 5. 观测性：提取并记录 Token 使用量
传统的 API 网关日志通常只记录 HTTP 状态码和延迟，但在 AI 场景下，成本核算需要更精细的数据。
*   **实践建议**：配置 Higress 的日志插件，解析 LLM 响应头中的 Usage 信息（如 `x-completion-tokens`, `x-prompt-tokens`），将其提取出来作为独立的访问日志字段。这将帮助你精确统计每个业务线、每个用户的

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*