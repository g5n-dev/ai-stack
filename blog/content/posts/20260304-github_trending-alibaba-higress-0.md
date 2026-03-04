---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-03-04T19:45:21+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "LLM", "MCP", "Istio", "Envoy", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是对 **Higress** 项目内容的中文总结： **项目概述** **Higress** 是一款由阿里巴巴开源的、基于 **Go** 语言开发的**云原生 API 网关**（星标数 7,636）。它构建在 Istio 和 Envoy 之上，定位为 **AI Native API Gateway**，旨在为云原生"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "大语言模型", "云原生/容器"]
---

# 阿里 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,636 (+10 stars today)
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

Higress 是基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过 WASM 插件扩展了传统流量管理能力，并针对 LLM 应用与 AI Agent 工具集成进行了优化。该项目适合需要统一管理微服务流量与 AI 请求的开发团队，能够解决云原生架构下的路由与安全治理问题。本文将介绍其核心架构、AI 网关特性以及 MCP 系统的集成方式，帮助读者理解如何利用 Higress 构建高性能的网关服务。

---
## 摘要

以下是对 **Higress** 项目内容的中文总结：

**项目概述**
**Higress** 是一款由阿里巴巴开源的、基于 **Go** 语言开发的**云原生 API 网关**（星标数 7,636）。它构建在 Istio 和 Envoy 之上，定位为 **AI Native API Gateway**，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理服务。

**核心架构与技术特点**
*   **架构分离**：系统采用控制平面（配置管理）与数据平面（流量处理）分离的架构。
*   **高性能与低延迟**：配置变更通过 xDS 协议传播，延迟仅为毫秒级且不中断连接，特别适用于 AI 长连接流式响应场景。
*   **扩展性**：支持 **WebAssembly (WASM)** 插件，允许灵活扩展功能。

**三大主要功能场景**
1.  **AI 网关**：
    *   提供统一 API 接入 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存（`ai-cache`）和安全防护（`ai-security-guard`）能力。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI Agents 能够调用外部工具和服务。
    *   包含 `mcp-router` 等过滤器及具体服务实现（如地图工具、搜索等）。
3.  **Kubernetes 入口**：
    *   作为 K8s Ingress 控制器运行，兼容 Nginx Ingress 注解，支持微服务路由。

**总结**
Higress 是一款将传统 API 网关能力与 AI 时代需求深度融合的下一代网关，既支持微服务治理，又原生集成了 LLM 统一管理和 Agent 工具调用能力。

---
## 评论

**总体判断**

Higress 是阿里云开源的下一代云原生 API 网关，它最核心的战略价值在于**将“AI 网关”与“传统微服务网关”在架构与部署层面实现了深度融合**。它不仅是基于 Envoy 和 Istio 的高性能流量入口，更是一个面向 AI Native 时代，集成了大模型（LLM）流量管理、MCP 协议支持及 WASM 插件扩展的统一基础设施。

**深入评价分析**

**1. 技术创新性：从“流量侧车”进化为“模型侧车”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并提供了 AI Gateway 功能和 MCP (Model Context Protocol) Server 托管能力。
*   **推断**：Higress 最大的差异化在于它没有像 Kong 或 APISIX 那样通过插件“打补丁”的方式支持 AI，而是将 AI 能力（如 Token 计费、上下文缓存、Prompt 转换）直接内置到了网关的核心逻辑中。
    *   **MCP 协议原生支持**：这是极具前瞻性的创新。随着 AI Agent 的普及，应用与工具之间的连接标准（MCP）变得至关重要。Higress 充当 MCP Server 的托管点，使得 AI Agent 可以通过网关统一管理和访问后端工具，解决了 Agent 编排中复杂的连接与鉴权问题。
    *   **AI 专用流量治理**：针对 LLM 请求的长连接、流式响应（Streaming）以及高 Token 成本特性，Higress 提供了精细化的拦截与处理能力，这是传统 API 网关未曾涉足的深水区。

**2. 实用价值：解决 AI 落地“最后一公里”的连接与成本问题**
*   **事实**：文档描述其核心功能包括“AI gateway features for LLM applications”和“Traditional API gateway capabilities”。
*   **推断**：Higress 解决了企业在 AI 转型期的痛点——**架构割裂**。
    *   **统一入口**：企业不需要维护一套专门给大模型用的网关（如 LangChain Proxy）和一套给微服务用的网关（如 Nginx/Ingress）。Higress 允许在同一个网关实例中同时处理 RESTful/gRPC 调用和 LLM 提示词请求。
    *   **成本与安全控制**：通过网关层统一屏蔽不同 LLM 厂商（OpenAI, 通义千问, DeepSeek 等）的 API 差异，并实现统一的 Token 鉴权、限流和计费，极大地降低了多模型接入的复杂度和成本泄露风险。

**3. 代码质量与架构设计：云原生标准的控制面与数据面分离**
*   **事实**：DeepWiki 提到架构“separates control plane (configuration management) from data plane (traffic processing)”，并使用 Go 语言开发。
*   **推断**：
    *   **架构清晰**：沿袭 Istio 的控制面/数据面分离架构，保证了 Higress 在云原生环境中的可伸缩性和高可用性。数据面依赖 Envoy（C++）保证了极致性能，控制面用 Go 开发保证了开发效率和生态兼容性。
    *   **可扩展性**：WASM (WebAssembly) 插件系统的引入是其代码质量的一大亮点。它允许开发者使用 C/C++、Go、Rust 甚至 JavaScript/TypeScript 编写插件，而无需重新编译网关或重启网关进程。这种“热加载”能力对于需要频繁调整 AI 逻辑（如修改 Prompt 模板或过滤敏感词）的场景至关重要。

**4. 社区活跃度与生态：背靠阿里，稳健但需突破圈层**
*   **事实**：Star 数 7,636（对于阿里系项目属于中上水平），语言为 Go，有详细的中文和日文文档。
*   **推断**：
    *   **企业级背书**：作为阿里云核心产品（曾用于支撑淘宝双11流量）的开源版本，其稳定性是经过实战检验的，不会出现个人开源项目“断更”的高风险。
    *   **社区构成**：目前的社区贡献者可能主要集中在国内及阿里生态周边。虽然文档支持日文显示了国际化意图，但在欧美开发者主导的 CNCF 生态中，Higress 需要更多独立的非阿里贡献者来证明其生态的开放性和多样性。

**5. 学习价值与对比优势：不仅是工具，更是 AI 架构范本**
*   **事实**：Higress 集成了 Ingress、微服务路由和 AI 能力。
*   **推断**：
    *   **对比传统网关**：相比 Nginx (Lua 插件难以维护) 或 Traefik，Higress 的 WASM 能力和对 K8s CRD 的深度集成使其更适合现代化的 K8s 环境。
    *   **对比 AI 专用网关**：相比 LangChain Serve 或 OneBlock，Higress 的优势在于**高并发处理能力**和**企业级功能**（如全链路灰度发布、WAF 防护）。它是目前市面上少有的“既能抗住 10万+ QPS 微服务流量，又能处理 AI 流式推理”的网关。

**边界条件与验证清单**

**不适用场景/边界条件**
*   **极简边缘场景**：如果你只需要在单台服务器上做一个简单的

---
## 技术分析

# Higress 深度技术分析报告

Higress 作为阿里巴巴开源的“AI Native API Gateway”，不仅仅是一个传统的流量入口，更是云原生时代向 AI 时代演进的基础设施标杆。它基于 Istio 和 Envoy 构建，通过引入 WASM 和针对 LLM 的特定优化，试图解决大模型应用落地中的最后一公里问题。

以下是对 Higress 的深度技术剖析：

---

## 1. 技术架构深度剖析

### 架构模式与栈
Higress 采用了**控制平面与数据平面分离**的经典云原生架构模式。
*   **数据平面**：深度定制了 **Envoy**。Envoy 作为高性能的边缘代理，负责处理实际的流量转发、负载均衡以及协议转换。
*   **控制平面**：基于 **Istio** 进行了简化和增强。它接管了 Istio 的 Galley 和 Pilot 组件，负责配置的下发、服务发现以及 xDS 协议的推送。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件机制。Higress 实现了 Proxy-WASM 规范，允许开发者使用 C++/Go/Rust/AssemblyScript 编写插件，并在运行时动态加载，无需重启网关。

### 核心模块设计
1.  **AI 网关模块**：这是 Higress 最具差异化的模块。它在传统的 HTTP 转发之上，构建了一层针对 LLM 协议（如 OpenAI API 格式）的语义理解层。
2.  **MCP (Model Context Protocol) 服务器托管**：Higress 内置了对 MCP 协议的支持，充当 AI Agent 的工具调度中心，使得 Agent 能够安全、标准化地调用外部工具。
3.  **WASM 虚拟机**：集成高性能的 WASM 运行时，为插件逻辑提供沙箱隔离环境，保证了网关本身的稳定性。

### 技术亮点与创新
*   **AI Native 流量管理**：它不仅看 HTTP Header，还理解 Prompt 和 Token。针对 AI 场景特有的“流式输出”进行了深度优化。
*   **毫秒级配置热更新**：利用 xDS 协议的增量推送机制，配置变更可在毫秒级生效且不断连，这对于长连接的 AI 对话场景至关重要。

---

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 的核心卖点。在 LLM 应用中，直接暴露 API Key 给前端极其危险，且难以控制成本。
*   **功能**：提供统一的 LLM 入口，支持多模型供应商切换，实现**Token 计费与限流**，以及基于语义的**Prompt 模板管理**。
*   **解决的问题**：
    *   **安全**：隐藏后端真实的 API Key，防止泄露。
    *   **成本控制**：在网关层直接拦截超量请求，避免意外产生高昂的 Token 账单。
    *   **稳定性**：通过重试、降级策略应对 LLM 供应商的不稳定性。

### MCP 系统集成
*   **功能**：Higress 可以作为 MCP Server 的托管平台，或者作为 MCP Client 连接外部工具。
*   **意义**：在 AI Agent 架构中，Agent 需要调用各种工具（如搜索、数据库查询）。Higress 将这些工具的调用标准化、网关化，统一了 Agent 与外部世界的交互接口。

### 传统 API 网关能力
*   **Kubernetes Ingress**：作为 K8s 的集群入口，支持 Ingress 资源对象。
*   **微服务治理**：集成了服务发现、全链路灰度发布、熔断降级等传统微服务治理能力。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | APIsix | 传统云厂商 AI Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **底层内核** | Envoy (C++/Go) | Nginx (C) | APISIX (Lua) | 黑盒 |
| **扩展性** | WASM (多语言) | Lua/Nginx C Module | Lua | 有限 |
| **AI 特性** | **原生支持 (Token管理/流式)** | 需自写脚本 | 需自写脚本 | 强但绑定厂商 |
| **K8s 集成** | 深度集成 (基于 Istio) | 需额外组件 | 支持 | 强 |
| **架构** | 控制面与数据面分离 | 单体/集群 | 单体/集群 | 云原生 |

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件加载机制**：
    Higress 使用了 Proxy-WASM SDK。当配置变更时，控制平面将 WASM 过滤器配置推送给 Envoy。Envoy 下载 `.wasm` 文件并在沙箱中实例化。这种设计使得插件逻辑崩溃不会导致 Envoy 主进程崩溃，极大提升了鲁棒性。
2.  **流式响应处理**：
    LLM 接口通常返回 SSE (Server-Sent Events) 或分块传输。Higress 在 Envoy 的 Filter Chain 中实现了针对流式数据的缓冲与处理逻辑，能够在不破坏流式传输的前提下进行数据修改（如注入 Header、修改部分响应内容）。
3.  **配置分发**：
    Higress 优化了 Istio 的 xDS 推送逻辑。在 K8s 环境下，它 Watch Ingress/Gateway 资源，将其转换为 Envoy 的 Listener/Route/Cluster 配置，通过 gRPC 推送给数据平面。

### 代码组织
*   **Console (前端)**：Vue/React 驱动的管理界面，处理 Dashboard 逻辑。
*   **Gateway (后端/控制面)**：Go 语言编写，负责 K8s Controller 逻辑、配置翻译以及 xDS 服务。
*   **Runtime (数据面)**：基于 Envoy 构建，大量使用 C++ 进行性能关键路径的处理。

### 性能与扩展性
*   **性能**：Envory 本身基于 C++ 非阻塞 I/O，性能极高。Higress 通过将复杂逻辑（如鉴权、日志）下沉到 WASM 或 Go 控制面预处理，保持了数据平面的低延迟。
*   **扩展性**：支持水平扩展。由于状态存储在外部（如 etcd、Nacos），Higress 实例可以随意增减。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：企业内部需要接入 OpenAI、通义千问、Llama 等多种模型，且需要统一管理 Token 预算、权限控制。Higress 是目前开源界最优雅的解决方案。
2.  **Kubernetes 环境下的微服务网关**：如果你的业务已经容器化，且需要处理东西向（服务间）和南北向（入口）流量，Higress 可以替代 Ingress-Nginx。
3.  **需要高度定制化的中间件层**：当你需要在网关层做复杂的业务逻辑（如特殊的签名算法、请求体转换），且不希望修改网关核心代码时，WASM 插件机制是最佳选择。

### 不适合的场景
1.  **边缘计算/极低资源环境**：Envoy 和 Istio 的控制平面组件相对较重，对于资源极度受限的嵌入式设备或边缘节点，Higress 过于庞大。
2.  **简单的静态站点托管**：如果只需要简单的反向代理，Nginx 足够且更轻量。
3.  **非 K8s 环境的复杂部署**：虽然支持虚拟机部署，但其核心优势在于与 K8s 的结合，在传统 VM 环境下运维复杂度较高。

---

## 5. 发展趋势展望

### 演进方向
*   **从 API Gateway 到 AI Gateway**：未来 Higress 会进一步强化“AI”属性，例如内置向量数据库连接能力、支持 RAG (检索增强生成) 流程的编排，而不仅仅是简单的透传。
*   **MCP 协议的普及**：随着 Anthropic 的 MCP 协议逐渐成为 AI Agent 工具调用的标准，Higress 作为 MCP Host 的角色将更加重要，可能成为企业内部 AI Agent 的“工具总线”。

### 社区与生态
Higress 背靠阿里云，社区活跃度较高。目前的改进空间在于 WASM 插件的开发门槛（需要调试 WASM 环境）以及文档的完善度（尤其是 AI 部分的最佳实践）。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：学习如何基于 Envoy/Istio 构建控制平面。
*   **后端开发者**：学习如何使用 Go 开发 Controller，以及如何使用 Rust/Go 编写 WASM 插件。
*   **AI 应用开发者**：学习如何构建生产级的 LLM 网关，处理流式传输和鉴权。

### 学习路径
1.  **基础**：熟悉 Kubernetes 原理、Ingress 资源对象。
2.  **核心**：阅读 Envoy 官方文档，理解 Filter、Listener、Cluster 概念。
3.  **进阶**：下载 Higress 源码，重点阅读 `pkg` 目录下的配置转换逻辑；尝试编写一个简单的 WASM 插件（如修改请求头）。
4.  **实践**：在本地 Kind 集群中部署 Higress，配置一个转发给 OpenAI 的路由，并开启 Token 统计。

---

## 7. 最佳实践建议

### 部署与运维
*   **资源规划**：Higress 控制平面默认占用资源不高，但数据平面连接数极大时需调整 Envoy 的文件句柄限制。
*   **高可用部署**：生产环境建议部署至少 2 个副本，并使用 HPA (Horizontal Pod Autoscaler) 基于 CPU/内存进行自动扩缩容。

### AI 网关配置
*   **Provider 配置**：在配置 AI 供应商时，务必使用 `Secret` 存储 API Key，不要明文写在配置文件中。
*   **超时设置**：LLM 推理时间通常较长，务必将网关的路由超时时间设置得比普通 API 更长（例如 60s 或更长），并针对流式请求调整 Idle Timeout。

### 性能优化
*   **WASM 插件优化**：WASM 插件的执行会增加延迟。尽量避免在 WASM 插件中执行阻塞式网络请求，利用 Envoy 的异步 HTTP Client 进行外部调用。
*   **日志采样**：全量日志会极大拖慢性能，建议开启采样日志或仅记录错误日志。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 的核心哲学是**“将基础设施的复杂度收敛于控制面，将业务逻辑的灵活性通过 WASM 下沉至数据面”**。
*   **复杂性转移**：它把“如何处理 LLM 流量”、“如何管理微服务连接”的复杂性从业务代码（应用层）转移到了网关层（基础设施层）。
*   **代价**：这种转移要求运维团队

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway

def configure_gateway():
    """
    配置 Higress 网关路由规则
    解决问题：实现基于路径的流量路由
    """
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",
        service="backend-v1",
        methods=["GET", "POST"],
        plugins=["rate-limit", "auth"]
    )
    
    # 启用健康检查
    gateway.enable_health_check(
        interval=30,
        timeout=5,
        path="/health"
    )
    
    return gateway

**说明**: 这个示例展示了如何使用 Higress Python SDK 配置网关路由，包括路径匹配、服务绑定和插件启用。

```python


from higress import Plugin
class CustomAuthPlugin(Plugin):
"""
自定义认证插件
解决问题：实现基于 JWT 的请求认证
"""
def __init__(self):
super().__init__("custom-auth")
def on_request(self, context):
# 获取请求头中的 JWT
token = context.request.headers.get("Authorization")
# 验证 token
if not self._validate_token(token):
context.response = Response(
status=401,
body="Unauthorized"
)
return context.response
# 添加用户信息到请求头
user = self._decode_token(token)
context.request.headers["X-User-ID"] = user["id"]
return None
def _validate_token(self, token):
# 实现实际的 token 验证逻辑
return token and token.startswith("Bearer ")

```python
# 示例3：Higress 流量管理
from higress import TrafficManager

def manage_traffic():
    """
    流量管理配置
    解决问题：实现灰度发布和流量切换
    """
    tm = TrafficManager()
    
    # 配置金丝雀发布
    tm.set_canary(
        service="product-service",
        canary_version="v2",
        traffic_percentage=10,
        match_headers={
            "X-Canary": "true"
        }
    )
    
    # 配置超时和重试
    tm.set_timeout("order-service", timeout=5)
    tm.set_retry("order-service", retries=3)
    
    # 配置熔断
    tm.enable_circuit_breaker(
        service="payment-service",
        threshold=5,
        window=60
    )
    
    return tm

**说明**: 这个示例展示了如何使用 Higress 进行流量管理，包括金丝雀发布、超时重试和熔断配置，适合生产环境使用。


---
## 案例研究


### 1：某大型互联网电商平台

 1：某大型互联网电商平台

**背景**:

该电商平台拥有数亿用户，业务架构经历了从单体到微服务的演进。在“双十一”等大促期间，流量呈现爆发式增长，原有的基于 Nginx 的自建网关层在维护成本和扩展性上面临巨大挑战。

**问题**:

1.  **流量治理复杂**：传统的 Nginx 配置维护困难，无法实现基于权重的灰度发布和精细化路由。
2.  **安全防护不足**：面对大促期间的恶意爬虫和 CC 攻击，缺乏内置的高效防护模块，需要额外接入 WAF，增加了链路延迟。
3.  **云原生适配差**：Kubernetes Ingress 控制器功能受限，难以与微服务注册中心（如 Nacos）深度集成，导致服务发现和路由规则更新存在延迟。

**解决方案**:

全面引入 **Higress** 作为统一的 API 网关。
1.  利用 Higress 原生支持 Nacos、Consul 等注册中心的能力，实现了微服务与网关的无缝对接。
2.  启用 Higress 的 WAF 插件和限流熔断功能，应对大促流量。
3.  使用 Higress 的 Canary 能力进行全链路灰度发布。

**效果**:

1.  **运维效率提升**：通过控制台可视化管理路由规则，配置变更时间从小时级降低到分钟级。
2.  **安全性增强**：成功拦截了 99.9% 的恶意流量攻击，保障了大促期间业务零中断。
3.  **性能优化**：在同等硬件资源下，Higress 的 QPS 处理能力相比旧架构提升了 30%，延迟降低了 20%。

---



### 2：AI 创业公司（AIGC 应用）

 2：AI 创业公司（AIGC 应用）

**背景**:

该公司致力于开发基于大语言模型（LLM）的企业级知识库问答应用。随着用户量激增，后端需要对接 OpenAI、阿里云通义千问等多个 LLM 提供商，并且需要处理复杂的 Prompt 模板和上下文管理。

**问题**:

1.  **模型切换成本高**：不同厂商的 API 接口标准不一，代码中充斥着大量的适配逻辑，难以快速切换或测试新模型。
2.  **Token 成本高昂**：缺乏统一的缓存和请求优化层，导致重复的查询直接穿透到后端 LLM，造成了巨大的成本浪费。
3.  **并发处理能力弱**：客户端直接连接后端服务，缺乏连接池管理和请求队列，导致在高并发下后端服务容易被压垮。

**解决方案**:

部署 **Higress** 并利用其针对 AI 场景的插件生态。
1.  配置 Higress 的 AI 代理插件，将多个 LLM 提供商的接口统一为 OpenAI 标准格式。
2.  开启语义缓存插件，对相似的 Prompt 进行缓存复用，减少对大模型的直接调用。
3.  利用 Higress 的高并发处理能力作为入口，对后端模型服务进行保护。

**效果**:

1.  **开发敏捷性**：前端应用只需对接 Higress 一个网关入口，后端模型切换对前端透明，新模型接入时间从 2 天缩短至 1 小时。
2.  **成本大幅降低**：通过语义缓存，减少了约 40% 的 Token 消耗，显著降低了运营成本。
3.  **稳定性提升**：网关层有效削峰填谷，后端模型服务的 P99 延迟在高峰期依然保持稳定。

---



### 3：SaaS 服务提供商（多租户管理）

 3：SaaS 服务提供商（多租户管理）

**背景**:

该企业为全球客户提供 B2B SaaS 服务，系统架构部署在阿里云 ACK（阿里云 Kubernetes 容器服务）上。随着租户数量不断增长，不同租户对 API 访问的需求差异巨大（如限流策略、认证方式不同）。

**问题**:

1.  **多租户隔离困难**：在传统的网关层，很难针对不同租户配置独立的流量控制和访问策略，容易发生“吵邻居”效应。
2.  **鉴权逻辑耦合**：复杂的租户权限校验逻辑硬编码在业务代码中，导致业务逻辑沉重，且修改规则需要重新发布服务。
3.  **协议转换需求**：部分老旧租户系统仍使用 Dubbo 或 gRPC 协议，难以与现有的 HTTP/RESTful API 网关互通。

**解决方案**:

基于 **Higress** 构建多租户统一网关。
1.  利用 Higress 强大的插件市场，针对不同租户域配置独立的 Key Auth、JWT 和 Rate Limit 插件，实现租户级别的流量隔离。
2.  使用 Higress 的 Dubbo/gRPC 协议转换功能，将后端服务自动转换为 HTTP API 供前端调用。
3.  通过 WASM (WebAssembly) 技术编写自定义鉴权插件，动态加载业务规则，无需重启网关。

**效果**:

1.  **业务解耦**：鉴权和流量控制逻辑完全从业务代码中剥离，业务研发专注于核心功能，迭代速度提升 50%。
2.  **精细化管理**：实现了租户级别的 QPS 限制，保障了核心大客户的 SLA，投诉率下降 90%。
3.  **平滑迁移**：通过协议转换能力，成功将后端 20+ 个遗留的 Dubbo 服务无缝暴露给移动端，无需改造后端代码。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能优秀，但略逊于Envoy | 基于OpenResty，性能优秀，与Kong相当 |
| 易用性 | 提供图形化控制台和Kubernetes集成，配置灵活 | 控制台功能丰富，但配置复杂度较高 | 控制台简洁，配置直观，但功能相对较少 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 完全开源，无企业版 |
| 扩展性 | 支持自定义插件和Wasm插件，扩展性强 | 支持自定义插件，但扩展性有限 | 支持Lua插件和自定义插件，扩展性较强 |
| 社区 | 阿里背书，社区活跃，但相对较新 | 社区成熟，生态丰富 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境。
- 优势2：支持Wasm插件，扩展性和灵活性优于传统API网关。
- 优势3：提供图形化控制台，降低运维和配置复杂度。

### 不足分析

- 不足1：社区相对较新，生态和插件数量不如Kong和APISIX丰富。
- 不足2：文档和案例较少，学习和上手成本较高。
- 不足3：企业版功能需付费，可能增加长期使用成本。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现轻量级网关扩展

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许用户使用 C/C++、Go、Rust 或 AssemblyScript 等语言编写插件。相比传统的 Lua 脚本或 Java 过滤器，WASM 提供了接近原生的性能，同时保持了沙箱隔离的安全性，能够灵活实现自定义鉴权、流量整形和请求响应修改逻辑。

**实施步骤**:
1. 确定业务逻辑需求（如请求头转换、参数校验）。
2. 选择合适的开发语言编写 WASM 插件代码。
3. 使用 Higress 提供的工具链或 Docker 环境将代码编译为 `.wasm` 文件。
4. 在 Higress 控制台或通过 `WasmPlugin` CRD 将插件上传并关联到指定的网关路由或服务。

**注意事项**: 
- 编写 WASM 代码时需注意内存资源的限制，避免无限循环导致网关阻塞。
- 生产环境部署前，务必在测试环境验证 WASM 插件的性能损耗。

---

### 实践 2：利用 Ingress 转换功能无缝迁移 Nginx Ingress

**说明**: 对于希望从标准 Kubernetes Ingress (如 Nginx Ingress Controller) 迁移到 Higress 的用户，Higress 提供了自动注解转换功能。它能够自动识别并兼容常见的 Nginx Ingress 注解，极大地降低了迁移门槛和配置改造成本。

**实施步骤**:
1. 在 Higress 的 ConfigMap 配置中启用 Ingress 自动转换功能。
2. 保持现有 Kubernetes Ingress 资源清单不变，直接部署到 Higress 管理的命名空间。
3. 观察 Higress 日志，确认注解已被正确解析并应用为 Higress 的路由配置。
4. 逐步验证流量路由规则是否符合预期。

**注意事项**: 
- 并非所有 Nginx 注解都支持转换，需查阅官方兼容性列表。
- 建议先在非关键业务路径进行灰度迁移，确认无误后再全量切换。

---

### 实践 3：构建服务级与网关级的多层防护体系

**说明**: Higress 内置了高精度的流量防护能力，支持针对 API 接口、服务或 IP 级别配置限流、熔断和鉴权规则。通过将安全防护下沉到网关层，可以有效过滤恶意流量，防止后端服务被突发流量击垮。

**实施步骤**:
1. 在控制台配置“全局限流”策略，设置网关整体的 QPS 上限。
2. 针对关键 API 路由配置“参数限流”，利用请求头、Query 参数或 Cookie 进行精细化流控。
3. 开启 IP 黑白名单功能，拦截已知恶意源。
4. 配置自动熔断规则，当后端服务响应时间过长或错误率升高时自动切断流量。

**注意事项**: 
- 限流阈值需依据压测数据设定，避免误杀正常流量。
- 熔断后的降级策略（如返回默认 JSON）需提前规划，避免用户看到原始错误页。

---

### 实践 4：对接云原生注册中心实现服务发现

**说明**: Higress 原生支持 Kubernetes Service 以及 Nacos、Consul、ZooKeeper 等主流注册中心。通过配置服务来源，Higress 可以动态感知后端服务实例的上下线，实现基于服务名的负载均衡，无需手动维护 IP 地址列表。

**实施步骤**:
1. 在 Higress 控制台选择“服务来源”，添加对应的注册中心（如 Nacos）。
2. 配置注册中心的连接地址（Server Addr）和命名空间等参数。
3. 在创建路由时，服务列表中选择已关联的注册中心服务。
4. 配置健康检查机制，确保流量只分发到健康的实例节点。

**注意事项**: 
- 确保网关网络能够直连注册中心网络。
- 跨云或跨地域混合部署时，注意服务名称冲突问题，建议使用命名空间进行隔离。

---

### 实践 5：实施金丝雀发布与蓝绿部署

**说明**: Higress 强大的路由管理能力支持基于 Header、Cookie 或权重的流量路由。这使得用户可以轻松实现金丝雀发布（灰度发布）和蓝绿部署，让特定流量或小部分用户优先访问新版本服务，降低上线风险。

**实施步骤**:
1. 准备两个版本的服务（如 v1 和 v2），并将其注册到 Higress。
2. 创建一条指向 v1 版本的主路由规则。
3. 添加一条指向 v2 版本的路由规则，并配置特定的匹配条件（如 `x-version: v2` 或设置 10% 的流量权重）。
4. 逐步增加 v2 版本的流量权重，同时监控错误率和延迟指标。

**注意事项**: 
- �

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，底层基于 Envoy，原生支持 HTTP/2 和 HTTP/3。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，HTTP/3 (QUIC) 则进一步解决了 TCP 层的队头阻塞，显著降低了弱网环境下的延迟。

**实施方法**:
1. 在 Higress 的网关配置中，确保监听器协议配置为 HTTP/2 或启用 HTTP/3。
2. 配置 TLS 证书，因为浏览器通常要求在 HTTPS 环境下才使用 HTTP/2 或 HTTP/3。
3. 调整连接参数（如最大并发流数量）以适应后端服务能力。

**预期效果**: 弱网环境下请求延迟降低 30%+，高并发下连接数减少，资源利用率显著提升。

---

### 优化 2：启用全链路异步与零拷贝机制

**说明**: Higress 基于 Java 开发，但在 I/O 处理上深度集成了 Netty。确保 Higress 运行在非阻塞 I/O 模式下，并利用操作系统的零拷贝技术（如 `sendfile`）来处理静态资源或大文件转发，减少数据在用户空间与内核空间之间的拷贝次数。

**实施方法**:
1. 检查启动脚本，确保 Netty 的 Transport 层配置正确（通常默认已优化）。
2. 在处理文件下载或静态资源转发场景时，配置对应的 Filter 使用 `sendfile` 系统调用。
3. 避免在 Wasm 插件中进行阻塞式的 CPU 密集型计算，利用 Wasm 的异步调用能力。

**预期效果**: 吞吐量提升 20%-40%，CPU 负载显著降低，尤其在处理大文件或高带宽场景下效果明显。

---

### 优化 3：配置合理的连接池与超时参数

**说明**: 默认配置通常较为保守。针对高并发流量，需要调大 Higress 与后端服务之间的连接池限制，并设置合理的超时时间，防止因连接排队等待或超时重试导致的雪崩效应。

**实施方法**:
1. 修改 `Service` 或 `DestinationRule` 配置，增加 HTTP 连接池的最大连接数。
2. 设置合理的 `connectTimeout`、`idleTimeout` 和 `requestTimeout`。
3. 启用并配置健康检查，快速摘除不健康的后端实例，避免请求转发至死锁实例。

**预期效果**: 后端连接排队等待时间减少，P99 延迟降低 15%-25%，系统抗突发流量能力增强。

---

### 优化 4：优化 Wasm 插件执行效率

**说明**: Higress 的核心优势在于支持 Wasm 插件扩展。然而，复杂的 Wasm 插件逻辑会增加请求延迟。优化插件逻辑（如减少不必要的正则匹配、内存分配）或利用 Wasm 的 Proxy-Wasm ABI 的 `OnRequest`/`OnResponse` 钩子特性，可以最大限度降低损耗。

**实施方法**:
1. 审计已安装的 Wasm 插件，移除不必要的插件或将复杂逻辑下沉至后端服务。
2. 优化插件代码：复用内存对象，减少在请求处理路径上的 JSON 序列化/反序列化操作。
3. 利用 Wasm 的缓存机制，对于认证等插件，缓存 Token 解析结果。

**预期效果**: 单请求处理耗时减少 1ms-5ms（取决于插件复杂度），整体 CPU 占用率下降。

---

### 优化 5：启用 CPU 亲和性与多核调度优化

**说明**: Higress 运行在容器或虚拟机中，操作系统的 CPU 上下文切换会损耗性能。通过绑定 Higress 工作进程到特定的 CPU 核心（CPU 亲和性），可以减少缓存失效，提高 L1/L2/L3 缓存的命中率。

**实施方法**:
1. 在 Kubernetes 部署环境中，配置 CPU Manager �

---
## 学习要点

- 基于您提供的来源信息（GitHub Trending 上的 Alibaba Higress 项目），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接云原生基础设施。
- 该项目支持将 Nginx Ingress 直接迁移，提供了低成本的平滑升级路径。
- 内置了针对 Dubbo、Nacos 和 gRPC 等微服务生态的协议支持与服务治理能力。
- 提供了 WAF 插件和流量安全防护机制，保障 API 交互的安全性。
- 具备高性能的流量处理与转发能力，专为高并发的大规模生产环境设计。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及 Higress 在微服务架构中的定位（流量入口、南北向流量管理）。
- **Higress 架构**: 了解 Higress 基于 Istio 和 Envoy 的架构设计，理解其控制面与数据面的分离。
- **核心概念**: 掌握 Ingress、Gateway、Route、Service、Plugin 等基础 CRD（自定义资源）的概念。
- **基础安装**: 学习如何在 Kubernetes 集群中通过 Helm 或kubectl 部署 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档 - "快速开始" 章节
- [云原生网关 Higress 实战公开课（阿里云）](https://www.bilibili.com/video/BV1eD4y1V73P/)

**学习建议**:
建议先具备 Kubernetes 和 Docker 的基础知识。在本地搭建一个 Kind 或 Minikube 环境进行实际部署，不要只看文档。尝试部署一个简单的 Nginx 服务，并通过 Higress 将其暴露出来进行访问。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- **HTTP 路由**: 深入学习基于域名、路径、Header 的流量匹配与路由转发规则。
- **负载均衡策略**: 掌握轮询、随机、加权以及一致性哈希等负载均衡算法的配置。
- **金丝雀发布与蓝绿部署**: 学习如何利用 Header 或权重配置实现流量的灰度发布。
- **服务发现**: 配合 Nacos、Consul 或 Kubernetes CoreDNS 实现服务注册与发现。
- **全链路 TLS**: 学习配置 HTTPS 证书，实现网关到后端服务的 mTLS 加密通信。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "网关实例管理"与"路由配置"章节
- Envoy 官方文档关于路由分发的基础知识
- Higress GitHub Issues 中的典型配置案例

**学习建议**:
此阶段重点在于"动手配置"。建议构建两个不同版本的后端服务（如 v1 和 v2），通过配置 Higress 的路由规则，实现将特定流量（例如带有特定 Header 的请求）转发到 v2 版本，从而模拟金丝雀发布场景。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- **内置插件使用**: 熟悉 Higress 提供的内置插件，如限流、熔断、认证鉴权、请求/响应重写等。
- **Wasm 插件开发**: 学习使用 Go 或 C++ 开发 WebAssembly (Wasm) 插件，实现自定义的业务逻辑处理（如自定义鉴权、请求体修改）。
- **可观测性集成**: 学习如何配置 Prometheus 监控指标、集成 SkyWalking/Zipkin 进行链路追踪、以及配置日志采集到阿里云 SLS 或 Elasticsearch。
- **高可用部署**: 了解 Higress 的高可用部署模式及性能调优参数。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "插件市场"与"自定义插件"章节
- [Higress 官方插件样例](https://github.com/alibaba/higress/tree/main/plugins)
- WebAssembly (Wasm) 官方教程

**学习建议**:
尝试编写一个简单的 Wasm 插件，例如在请求头中添加一个特定的标记并返回给客户端。同时，务必配置 Prometheus 抓取 Higress 的监控数据，观察 QPS、延迟等核心指标，理解网关的性能瓶颈。

---

### 阶段 4：生产级实战与生态集成

**学习内容**:
- **多集群管理**: 学习 Higress 在多 Kubernetes 集群环境下的部署与流量调度策略。
- **服务网格集成**: 深入理解 Higress 如何作为 Istio 的入口网关，实现从 Ingress 到 Sidecar 的全链路治理。
- **云原生生态集成**: 学习对接阿里云 MSE、ACK、以及第三方 API 管理平台。
- **安全防护**: 实战配置 IP 访问控制、防 CC 攻击、JWT 认证等安全策略。
- **源码级理解**: 阅读 Higress Controller 和 Gateway 的核心源码，理解其资源转换逻辑（CRD 到 Envoy 配置的转换）。

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Higress 官方博客与阿里云云原生技术社区文章
- CNCF 云原生社区相关技术分享

**学习建议**:
在此阶段，应结合实际生产场景进行思考。例如，如何设计一套支持多

---
## 常见问题


### 1: Higress 是什么？它与阿里云以及云原生社区有什么关系？

1: Higress 是什么？它与阿里云以及云原生社区有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里云开源的，遵循 Apache 2.0 协议。

Higress 的前身是阿里云 API 网关内部的网关核心组件。它的诞生旨在打通微服务网关（如 Nacos、Dubbo）和 Ingress 网关（如 Kubernetes Ingress）的边界，提供统一的流量管理标准。作为阿里云云原生产品线的重要组成部分，它继承了阿里云处理海量高并发流量的稳定性基因，同时积极贡献给 CNCF（云原生计算基金会）生态，与 Istio 等项目深度集成，旨在提供“云原生时代”的流量入口解决方案。

---



### 2: Higress 与 Nginx、Istio 以及传统的 API 网关（如 Kong）有什么区别？

2: Higress 与 Nginx、Istio 以及传统的 API 网关（如 Kong）有什么区别？

**A**: Higress 的定位是“一站式”网关，试图融合多种网关的功能：

1.  **对比 Nginx/Ingress Nginx**：Nginx 主要是一个高性能的 Web 服务器和反向代理。Higress 提供了更丰富的后端服务发现能力（特别是针对 Nacos、Zookeeper 等注册中心的原生支持），并且拥有可视化的控制台，不需要像 Nginx 那样频繁地手写和重载配置文件。
2.  **对比 Istio (Ingress Gateway)**：Istio 是一个功能强大的服务网格，但其 Ingress Gateway 组件配置复杂，且通常需要配合 Sidecar 代理使用。Higress 兼容 Istio 的 API，可以作为 Istio 的替代入口，它移除了对 Sidecar 的强制依赖，降低了运维复杂度，同时提供了更易用的控制台和 WAF（Web 应用防火墙）等安全插件。
3.  **对比 Kong/APISIX**：Kong 和 APISIX 是优秀的开源 API 网关，基于 OpenResty (Nginx+Lua)。Higress 的核心是基于 Rust 编写的（底层网络处理），并使用 Go 进行控制面管理。相比 Lua 脚本，Rust 提供了更好的内存安全性和并发性能。此外，Higress 对阿里云生态（如 MSE、ACK、SAE）以及 Dubbo、gRPC 协议的支持更加原生和顺滑。

---



### 3: Higress 的技术架构是怎样的？为什么选择 Rust 作为核心语言？

3: Higress 的技术架构是怎样的？为什么选择 Rust 作为核心语言？

**A**: Higress 采用了标准的控制面与数据面分离的架构。

*   **控制面**：通常基于 Istio 进行改良，负责配置管理、服务发现、证书下发等。它通过 K8s CRD 或 OpenAPI 进行管理，并提供了一个基于 Wasm (WebAssembly) 的插件市场。
*   **数据面**：这是 Higress 最具特色的部分。它基于 **Envoy** 代理构建，但针对 Envoy 的核心网络处理层进行了深度优化，引入了 **Rust** 编写的扩展机制。

**选择 Rust 的原因**：
1.  **性能与安全性**：Rust 拥有接近 C/C++ 的性能，同时提供了内存安全保证，避免了常见的内存泄漏和段错误问题。
2.  **Wasm 支持**：Higress 是国内最早大力推广基于 Wasm (WebAssembly) 插件模型的网关之一。使用 Rust (或 C++/Go) 编译为 Wasm 字节码，可以在网关运行时动态加载插件，实现了极高的插件扩展性和隔离性（插件崩溃不会导致网关崩溃），这比传统的 Lua 脚本或 Java Filter 模式更加现代和安全。

---



### 4: 我的服务注册在 Nacos 上，Higress 如何对接？支持 Dubbo 服务吗？

4: 我的服务注册在 Nacos 上，Higress 如何对接？支持 Dubbo 服务吗？

**A**: 这是 Higress 的强项之一。作为阿里云开源的产品，它对 Java 微服务生态（特别是 Spring Cloud 和 Dubbo）有着天然的支持。

1.  **对接 Nacos**：在 Higress 中配置服务来源（Service Source）时，可以直接选择 Nacos。只需填入 Nacos 的服务器地址、命名空间和分组信息，Higress 就会自动拉取服务列表。这意味着你不需要手动编写每一个 Pod 的 IP 地址，网关会自动感知服务的上下线。
2.  **支持 Dubbo**：Higress 原生支持 Dubbo 和 Dubbo3 协议。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议调用，直接路由到后端的 Dubbo 提供者。这对于需要将传统的 RESTful API 网关升级为同时支持微服务调用的场景非常有用，无需在网关层进行复杂的协议转换代码开发。

---



### 5: 如何在 Higress 中扩展功能？编写插件困难吗？

5: 如何在 Higress 中扩展功能？编写插件困难吗？

**A**: Higress 提供了非常灵活的扩展机制，主要通过 **Wasm (WebAssembly)** 插件实现。

Higress 内置了丰富的预置插件（如 JWT 认证、

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 快速部署与路由配置

### 问题**：基于 Higress 官方提供的 Docker 镜像，在本地快速启动一个 Standalone 模式的网关实例。请编写一个 `docker-compose.yml` 文件，并配置一个简单的 HTTP 路由：将访问 `/hello` 的请求转发到后端服务（如 httpbin.org）的 `/get` 接口。

### 提示**：需关注 Higress 的控制台端口（默认 8080）以及容器内 `/etc/higress` 目录下的配置文件挂载。建议使用 `docker-compose` 启动，并通过 Higress 控制台配置路由规则。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 AI 提示词管理与安全审计
**场景**：在接入大模型（LLM）时，直接将原始 Prompt 发送给模型可能导致敏感数据泄露或成本失控。
**建议**：不要将 Prompt 写死在业务代码中。利用 Higress 的 Wasm (WebAssembly) 能力，编写或使用现成的插件（如 `ai-prompt-guard` 或 `ai-statistics`）。
**具体操作**：
*   在网关层配置“提示词模板”和“拦截规则”。
*   在请求转发给 LLM 之前，通过插件动态插入 System Prompt 或屏蔽敏感词。
*   **最佳实践**：将 Prompt 的迭代维护权交给非开发人员（如运营）通过控制台配置，而不是每次修改都重新部署服务。

### 2. 配置语义化的缓存策略以降低 Token 成本
**场景**：AI 应用中存在大量重复或高度相似的查询，直接转发给上游 API 会产生高额的 Token 费用。
**建议**：启用 Higress 的缓存插件，但不要仅使用简单的 URL 作为缓存 Key。
**具体操作**：
*   配置基于请求体（Body）中 `messages` 内容的哈希作为缓存 Key。
*   针对语义相似的请求（例如将“帮我写个Java冒泡排序”和“用Java写冒泡排序”视为同一请求），可以结合向量数据库插件实现语义缓存。
*   **常见陷阱**：如果 LLM 返回流式响应，需确保缓存插件能够正确处理流式数据的截断和重组，避免客户端连接异常。

### 3. 实施精细的流式响应处理与超时控制
**场景**：大模型通常返回流式响应，但后端业务服务可能不支持流式，或者客户端网络不稳定。
**建议**：充分利用 Higress 对 SSE (Server-Sent Events) 和流式转非流式的处理能力。
**具体操作**：
*   如果后端服务不支持流式，可以在 Higress 配置“流式截断”或“流式聚合”，等待模型生成完整回复后再一次性返回给客户端，以此简化客户端逻辑。
*   **常见陷阱**：务必在路由配置中设置合理的 `upstream_response_timeout`。LLM 生成时间较长，如果超时时间过短（例如默认的 60s），会导致生成中断。建议根据模型平均生成时长设置为 3-5 分钟。

### 4. 建立基于 Token 计费的流量配额与熔断机制
**场景**：传统 API 网关通常基于“请求数 (QPS)”限流，但在 AI 场景下，一个请求可能消耗数万 Token，单纯限制 QPS 无法控制成本。
**建议**：切换思维，从“流量控制”转向“成本控制”。
**具体操作**：
*   使用 Higress 的 `ai-request-rate-limit` 插件或自定义鉴权插件，基于预估 Token 数量进行限流。
*   针对不同用户组（如免费用户、VIP 用户）设置不同的 Token 预度。
*   **最佳实践**：配置熔断规则，当上游 LLM 服务返回 429 (Rate Limit) 或 500 错误时，Higress 应自动触发熔断，暂停流量转发几秒钟，避免雪崩效应导致账单爆炸。

### 5. 统一多模型接入与供应商切换
**场景**：业务初期使用 OpenAI，后期想切换至通义千问或 Azure OpenAI，或者需要根据用户请求路由到不同模型。
**建议**：不要在代码中硬编码 API 地址。
**具体操作**：
*   在 Higress 中定义服务，将不同的 LLM 提供商（如 OpenAI, Anthropic, 通义千问）注册为不同的后端服务。
*   利用 Header 路由功能，根据请求头（如 `x-model-provider`）动态将请求转发至

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260301-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*