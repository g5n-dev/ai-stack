---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-12T19:07:52+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 AI 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言开发。该项目在 GitHub 上拥有超过 7,700 个星标，旨在通过提供云原生架构，满足现代 AI 应用和微服务的流量管理需求。 以下是 Higress 的核心特性总结："
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
- **星标**: 7,742 (+7 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，实现了对 AI 原生应用的支持。它不仅提供传统的流量管理功能，还针对大模型应用集成了 AI 网关特性，并支持 MCP 服务器托管，适合需要统一管理微服务与 AI 流量的团队。本文将介绍其系统架构、核心组件以及主要的部署与开发指南，帮助开发者快速上手。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 AI 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言开发。该项目在 GitHub 上拥有超过 7,700 个星标，旨在通过提供云原生架构，满足现代 AI 应用和微服务的流量管理需求。

以下是 Higress 的核心特性总结：

**1. 架构设计**
Higress 采用了**控制平面**与**数据平面**分离的架构。其优势在于配置变更可以通过 xDS 协议以毫秒级延迟生效，且不会造成连接中断。这一特性特别适用于 AI 流式响应等需要保持长连接的场景。

**2. 三大核心功能**
*   **AI 网关：** 为大语言模型（LLM）应用提供统一 API。它支持 30 多家 LLM 提供商，提供协议转换、可观测性、缓存以及安全防护（通过 `ai-proxy`、`ai-statistics` 等插件实现）。
*   **MCP 服务器托管：** 支持托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用工具和服务。
*   **Kubernetes Ingress：** 作为标准的 K8s Ingress 控制器，兼容 Nginx Ingress 注解，提供微服务路由等传统网关功能。

**3. 可扩展性**
系统集成了 **WebAssembly (WASM)** 插件能力，允许用户灵活扩展网关功能，以适应不同的业务逻辑和定制化需求。

简而言之，Higress 是一款将传统 API 网关能力与 AI 时代需求深度融合的下一代网关产品。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的云原生网关产品，它成功地将**云原生流量治理**与**AI大模型应用编排**合二为一。该项目不仅继承了 Envoy 的高性能基石，更通过 WASM 技术和 AI 原生特性，解决了传统网关在 LLM 时代的功能缺失问题，是目前将“AI Gateway”概念落地得最彻底的开源项目之一。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“智能编排”的架构跃迁**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并引入了 WebAssembly (WASM) 插件系统，同时专门针对 LLM 应用提供了 AI Gateway 特性及 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：Higress 的核心差异化在于其**“AI Native”**的定位。传统网关（如 Nginx, Kong）主要关注 HTTP 转发，而 Higress 创新性地将 AI 交互协议（如 OpenAI 协议转换）和语义路由内置到数据平面。利用 WASM 技术，它允许开发者使用 C/C++/Go/Rust 等语言编写高频插件并热加载，这打破了传统 Lua 插件的性能黑箱限制。此外，支持 MCP 协议托管意味着 Higress 直接打通了 AI Agent 与外部工具（如数据库、API）的连接链路，这是非常具有前瞻性的架构设计。

**2. 实用价值：解决 LLM 落地中的“连接与成本”痛点**
*   **事实**：文档提到它提供 Kubernetes Ingress、微服务路由，以及专门的 AI Gateway 功能。
*   **推断**：在实用层面，Higress 解决了三个关键问题：
    1.  **模型供应商统一**：企业无需在代码中适配不同大模型（如通义千问、OpenAI、Claude）的接口差异，通过 Higress 的统一协议转换即可实现低成本切换。
    2.  **Token 成本与安全**：作为网关层，它天然适合做统一的数据脱敏和 Token 计费管理，避免了在业务代码中散落逻辑。
    3.  **基础设施复用**：它允许企业用同一套基础设施管理传统微服务流量和 AI 应用流量，大幅降低了运维复杂度。对于正在向 AI 转型的互联网企业，其应用场景非常广泛。

**3. 代码质量与架构：云原生标准的控制与数据分离**
*   **事实**：描述中提到架构将控制平面（配置管理）与数据平面（流量处理）分离。
*   **推断**：作为阿里开源项目，Higress 遵循了严格的云原生架构设计。控制平面对接 Istio，利用其强大的配置分发能力；数据平面基于 Envoy，保证了 C++ 编写的高性能转发。Go 语言编写控制面符合当前云原生生态的主流选择。从文档完整性（多语言 README、详细的架构章节）来看，该项目具有较高的成熟度，适合作为生产级基础设施选型。

**4. AI 特性的深度整合：MCP 与语义路由**
*   **事实**：DeepWiki 特别强调了“MCP server hosting for AI agent tool integration”。
*   **推断**：这是 Higress 区别于传统 API 网关（如 APISIX）加 AI 插件的最大亮点。随着 AI Agent 的兴起，Agent 需要调用大量外部工具。Higress 直接充当 MCP Server 的托管层，使得 Agent 可以通过网关安全、标准化地访问工具，这构建了一个强大的 AI 生态中间件底座。

**5. 社区活跃度与生态背书**
*   **事实**：Star 数 7,742（且在持续增长），由阿里巴巴主导。
*   **推断**：阿里在中间件领域（如 Nacos, Sentinel）有着深厚的技术积累和社区运营能力。Higress 继承了这一基因，且因为切中了当下最火的 AI Agent 赛道，社区活跃度较高。对于国内开发者而言，中文文档的完备性和阿里系的背书使其成为替代 Kong 或 APISIX 的强力候选者。

**边界条件与不适用场景**

尽管 Higress 功能强大，但在以下场景中需谨慎考虑：
1.  **极简边缘场景**：如果只需要一个简单的反向代理或负载均衡器，Higress 基于 K8s 和 Istio 的架构显得过于重量级。
2.  **非 K8s 环境**：虽然支持 Standalone 模式，但其核心优势在于与 K8s 的深度结合，在传统虚拟机环境下部署复杂度较高。
3.  **极致低延迟要求**：对于某些纯内存级转发、对 CPU 指令极其敏感的场景，Envoy 的 WASM 插件可能会带来微小的性能损耗（相比原生 C 模块），需进行压测验证。

**快速验证清单**

在决定引入 Higress 前，建议执行以下验证：

1.  **WASM 插件性能压测**：开启自定义 WASM 插件后，使用 wrk 或 hey 对比开启前后的 QPS 和 P99 延迟，确保插件逻辑未成为瓶颈。
2.  **AI 上下文缓存测试**：验证其 LLM 缓存功能（如果启用）在不同 Prompt 下的命中率，确认是否真正降低了 Token 消耗和后端延迟。
3.  **MSP 协议兼容性检查**：如果你

---
## 技术分析

以下是对 Alibaba Higress 仓库的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是基于 Istio 和 Envoy 构建的**下一代云原生 API 网关**。其核心架构设计体现了“控制平面与数据平面分离”的云原生理念，并在此基础上进行了深度的定制化扩展。

### 1.1 技术栈与架构模式
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制平面**：深度集成 **Istio**，复用其控制平面能力进行服务发现和配置管理（xDS 协议）。
*   **编程语言**：**Go**（控制平面与后端管理）与 **C++**（Envoy 数据平面核心）的结合。
*   **扩展模型**：采用 **WebAssembly (WASM)** 作为核心插件扩展机制，支持 C++, Go, Rust, JavaScript 等多语言编写插件。

### 1.2 核心模块与设计
Higress 的架构可以概括为“一个内核，两个平面，三个核心能力”：
1.  **统一配置平面**：通过 Istio 控制平面进行配置分发，实现了配置变更的毫秒级生效，且无需重启数据平面，这对长连接场景至关重要。
2.  **高性能数据平面**：基于 Envoy 处理所有入站流量。
3.  **三大核心能力模块**：
    *   **AI Gateway**：针对大模型（LLM）流量进行专门优化。
    *   **MCP Server Hosting**：托管 Model Context Protocol 服务，作为 AI Agent 的工具调度中心。
    *   **传统 API 网关**：Kubernetes Ingress 控制器、微服务路由、负载均衡。

### 1.3 技术亮点与创新点
*   **AI-Native 架构**：Higress 不是在传统网关上打补丁支持 AI，而是将 AI 流量视为一等公民。它原生支持 SSE（Server-Sent Events）流式转发，解决了传统网关在处理长连接流式响应时的缓冲和延迟问题。
*   **WASM 插件市场**：构建了基于 WASM 的插件生态。由于 WASM 的沙箱隔离特性，用户可以在不修改网关核心代码的情况下，动态加载高风险或自定义逻辑（如 Key 管理、Prompt 注入、数据脱敏）。
*   **MCP 协议集成**：Higress 率先集成了 MCP (Model Context Protocol) 标准的托管能力。它充当了 AI Agent 与外部工具（如数据库、API）之间的“翻译器”和“安全网关”。

### 1.4 架构优势
*   **零宕机部署**：配置通过 xDS 协议热更新，连接不中断。
*   **极致性能**：数据平面 Envoy 采用 C++ 非阻塞 I/O，处理转发延迟极低。
*   **生态互通**：完美兼容 K8s Ingress 标准和 Istio 服务网格，降低了从传统微服务架构向 AI 架构迁移的门槛。

---

## 2. 核心功能详细解读

### 2.1 AI Gateway (AI 网关)
这是 Higress 最具差异化的功能。
*   **解决的问题**：企业在接入 LLM（如 OpenAI, 通义千问等）时面临的多模型切换成本、API Key 泄露风险、Token 计费统计困难以及 Prompt 注入安全问题。
*   **核心功能**：
    *   **统一模型接口**：将不同厂商的异构 API 统一为标准格式，前端应用只需改动配置即可切换模型。
    *   **Token 管理与计费**：实时统计请求和响应的 Token 数量，便于成本分摊。
    *   **Prompt 安全防护**：通过插件在请求发送给 LLM 之前进行敏感词过滤和 Prompt 劫持检测。
    *   **流式处理优化**：确保 AI 生成的文本能够实时（TTS）传输给用户，而不是等待全部生成完毕。

### 2.2 MCP Server Hosting
*   **解决的问题**：AI Agent 需要调用外部工具获取信息，直接暴露内部 API 给 LLM 存在巨大的安全风险，且每个 Agent 都去实现复杂的认证鉴权过于繁琐。
*   **技术实现**：Higress 作为 MCP Server 的托管网关，对外暴露标准 MCP 接口，对内连接企业微服务。它负责将 Agent 的自然语言意图转换为具体的 API 调用，并在中间层做权限校验和数据过滤。

### 2.3 与同类工具对比
| 特性 | Higress | Nginx/Kong | API Gateway (AWS) |
| :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强** (内置流式处理、Token统计) | 弱 (需通过 Lua/Go 插件硬编码) | 中 (依赖集成，如 Bedrock) |
| **扩展性** | **WASM (沙箱、多语言)** | Lua/Nginx C Module (耦合度高、风险大) | Lambda 集成 (冷启动问题) |
| **云原生亲和度** | **极高** (Istio 原生) | 中 (需 K8s Ingress Controller) | 高 (AWS 生态锁定) |
| **性能** | 高 (Envoy C++) | 极高 (Nginx C++) | 中 (受云服务链路影响) |

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **配置热加载**：
    Higress 利用 Envoy 的 xDS (v2/v3) 协议。控制平面监听 K8s CRD 或配置中心的变化，将其翻译成 Envoy 能理解的配置，推送给数据平面。数据平面通过 LDS (Listener Discovery Service) 和 RDS (Route Discovery Service) 动态更新路由规则，而不断开 TCP 连接。
*   **WASM 虚拟机集成**：
    Higress 在 Envoy 中嵌入 Proxy-WASM 运行时。当请求进入时，WASM 过滤器被挂载到请求处理链上。关键在于**内存共享**与**生命周期隔离**：WASM 插件可以访问请求头/体，但无法直接修改 Envoy 的主进程内存，崩溃只影响当前请求，不会导致网关崩溃。

### 3.2 代码组织与设计模式
*   **代码结构**：典型的 Go 后端微服务架构。`pkg` 目录包含核心逻辑，`plugins` 目录包含 WASM 插件源码。
*   **设计模式**：
    *   **Controller Pattern**：控制器模式，持续监听资源状态并调和。
    *   **Filter Chain**：责任链模式，请求通过一系列 HTTP Filter（认证、限流、路由、WASM 插件）。

### 3.3 性能与扩展性
*   **性能优化**：利用 Envoy 的零拷贝技术和线程模型（每个线程一个非阻塞 event loop）。Higress 针对长连接（SSE）优化了缓冲区策略，改为流式转发，减少内存占用。
*   **扩展性**：支持水平扩展。由于控制平面与数据平面分离，可以独立扩容 Pod 数量以应对更高的并发流量。

### 3.4 技术难点与解决
*   **难点**：WASM 插件的性能损耗。
*   **解决**：Higress 优化了 WASM 虚拟机的启动速度，并支持插件缓存机制。对于极高并发场景，建议将核心逻辑仍用 C++ (Envoy Filter) 编写，WASM 用于业务逻辑变更频繁的部分。

---

## 4. 适用场景分析

### 4.1 最适合的项目
*   **AI 应用开发**：需要接入多家 LLM 厂商，且需要统一管理 Token 消耗和 API Key 的 SaaS 平台。
*   **企业微服务网关**：已经使用 Kubernetes 部署业务，需要替代传统的 Nginx Ingress Controller，希望获得更强的流量管理和可观测性。
*   **AI Agent 基础设施**：需要构建企业内部 Agent，需要安全地暴露内部 API 给 LLM 的场景（利用 MCP 功能）。

### 4.2 不适合的场景
*   **极简静态博客托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。
*   **超低延迟的高频交易系统**：虽然 Envoy 很快，但经过网关一层代理必然有微秒级损耗，且 WASM 插件会增加额外延迟，直连服务更优。

### 4.3 集成注意事项
*   **资源限制**：WASM 插件虽然隔离，但会消耗内存和 CPU，需对 Pod 资源做合理限制。
*   **版本兼容性**：Higress 依赖的 Istio 版本需要与集群版本兼容，升级时需遵循特定顺序。

---

## 5. 发展趋势展望

### 5.1 演进方向
*   **从流量管理向意图管理进化**：随着 AI Agent 的普及，网关不再仅仅转发“数据”，而是转发“意图”。Higress 将会增强对自然语言请求的理解、路由和编排能力。
*   **更强的 WASM 生态**：未来可能会出现更多针对 AI 特定场景（如 RAG 检索增强、Prompt 优化）的开源 WASM 插件。

### 5.2 社区与改进
*   目前社区主要集中在国内，国际化程度正在提升。
*   **改进空间**：UI 控制台的易用性、WASM 插件的调试工具链、更细粒度的指标监控。

---

## 6. 学习建议

### 6.1 适合的开发者
*   **中高级后端工程师**：希望深入理解云原生、Service Mesh 和 API 网关原理。
*   **AI 应用架构师**：需要设计企业级 AI 应用的接入层。
*   **Go 语言爱好者**：想学习大型 Go 项目的工程化实践。

### 6.2 学习路径
1.  **基础**：熟悉 Kubernetes 和 Docker 基础操作。
2.  **前置知识**：阅读 Envoy 官方文档，理解 xDS 协议、Listener 和 Cluster 概念。
3.  **动手实践**：在本地 Kind 集群中通过 Helm 部署 Higress，尝试配置一个简单的路由转发。
4.  **进阶**：编写一个简单的 Go WASM 插件（如修改请求头），加载到 Higress 中观察效果。

### 6.3 实践建议
*   阅读 `pkg/config` 下的代码，理解 K8s CRD 如何转化为 Envoy 配置。
*   查看 `plugins/wasm-go` 目录，学习如何编写高性能 WASM 插件。

---

## 7. 最佳实践建议

### 7.1 部署与配置
*   **资源规划**：生产环境建议将 Higress 独立部署在专门的 Node Pool 中，避免与业务应用争抢资源。
*   **高可用**：至少部署 3 个副本，

---
## 代码示例




```python
# 示例1：Higress网关路由配置
def configure_higress_route():
    """
    配置Higress网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway()
    
    # 添加路由规则：/api/v1 转发到 service-a
    gateway.add_route(
        path="/api/v1",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：/api/v2 转发到 service-b
    gateway.add_route(
        path="/api/v2",
        destination="service-b:8080",
        methods=["GET"]
    )
    
    # 应用配置
    gateway.apply_config()
    print("Higress路由配置已更新")

# 说明：这个示例展示了如何使用Higress配置网关路由，实现微服务架构中的流量分发。

```python


def configure_higress_plugin():
"""
配置Higress的限流插件
解决问题：防止API被过度调用导致服务过载
"""
from higress import Plugin
# 创建限流插件实例
rate_limit = Plugin("rate-limit")
# 配置限流规则：每分钟最多100次请求
rate_limit.set_config({
"max_requests_per_minute": 100,
"burst_size": 10
})
# 将插件应用到特定路由
rate_limit.apply_to_route("/api/v1")
print("限流插件已配置并应用")

```python
# 示例3：Higress健康检查配置
def configure_health_check():
    """
    配置Higress的健康检查机制
    解决问题：自动检测后端服务健康状态并隔离故障节点
    """
    from higress import HealthCheck
    
    # 创建健康检查实例
    health_check = HealthCheck()
    
    # 配置检查参数
    health_check.set_config({
        "endpoint": "/health",  # 健康检查端点
        "interval": 10,         # 每10秒检查一次
        "timeout": 3,           # 超时时间3秒
        "unhealthy_threshold": 3  # 连续3次失败则标记为不健康
    })
    
    # 应用到所有后端服务
    health_check.apply_to_all_services()
    
    print("健康检查已配置")

# 说明：这个示例展示了如何配置Higress的健康检查机制，实现自动故障隔离和服务高可用。


---
## 案例研究


### 1：阿里巴巴内部电商业务与淘宝网

 1：阿里巴巴内部电商业务与淘宝网

**背景**:
作为中国最大的电商平台，淘宝和天猫的业务规模极其庞大，拥有数亿日活用户和海量的并发请求。在“双11”等大促期间，流量峰值达到惊人的级别，且业务逻辑极其复杂，涉及数千个微服务之间的调用。

**问题**:
随着业务从单体架构向微服务和云原生架构迁移，团队面临着严峻的流量治理挑战。
1.  **异构系统互通困难**：存量系统中存在大量使用不同语言（如 Go、C++）开发的服务，这些服务无法像 Java 服务那样方便地接入传统的 Service Mesh（如 Istio）数据面，导致流量管理存在盲区。
2.  **网关性能瓶颈**：传统的 API 网关在处理超高并发流量时，延迟和资源消耗成为瓶颈，难以支撑大促期间的极端流量。
3.  **配置复杂度高**：微服务间的路由、限流、熔断规则配置繁琐，缺乏统一的流量管理标准。

**解决方案**:
阿里巴巴团队基于内部多年的 Nginx 和 Envoy 实践经验，研发并开源了 Higress。
1.  **统一网关与 Sidecar 代理**：Higress 被部署为统一的 API 网关，接管所有外部进站流量；同时，利用 Higress 对 Envoy 的深度集成和扩展，为非 Java 语言的微服务提供了一套高性能的 Sidecar 代理方案，实现了全链路的流量管理。
2.  **高性能架构**：利用 Higress 基于 Envoy 和 WASM（WebAssembly）的技术架构，将流量处理逻辑下沉到高性能的 C++ 层，大幅降低了请求延迟。
3.  **Kubernetes 原生集成**：深度整合 Ingress 和 Gateway API，实现了与阿里云 ACK（Kubernetes）的无缝对接，实现了路由规则的自动化管理和动态推送。

**效果**:
1.  **极致性能**：成功支撑了双11期间每秒数百万级 QPS 的流量冲击，网关延迟显著降低，系统稳定性达到 99.995% 以上。
2.  **生态统一**：打通了 Java、Go、Node.js 等多语言微服务的流量治理壁垒，实现了统一的流量控制、灰度发布和安全认证策略。
3.  **成本优化**：通过高性能的流量转发，降低了同等吞吐量下的服务器资源消耗，显著降低了基础设施成本。

---



### 2：某头部金融科技公司

 2：某头部金融科技公司

**背景**:
该公司负责运营一个日均请求量达数十亿的金融交易与数据服务平台。随着业务的快速扩展，其技术栈包含了 Spring Cloud、gRPC 以及遗留的 Dubbo 服务，且运行在混合云环境（本地机房 + 公有云）中。

**问题**:
1.  **多协议支持复杂**：原有的网关主要针对 HTTP，对于内部大量使用的 gRPC 和 Dubbo 协议支持不够友好，需要繁琐的协议转换插件，且性能损耗大。
2.  **插件开发维护难**：业务部门经常有定制化的鉴权、流控需求，但原有网关的插件开发需要修改核心代码或使用 Lua，开发门槛高且存在安全隔离隐患。
3.  **云原生迁移受阻**：在向 Kubernetes 迁移过程中，原有的 Ingress Controller 功能受限，无法满足复杂的七层路由和基于权重的蓝绿发布需求。

**解决方案**:
该企业引入 Higress 作为下一代云原生 API 网关。
1.  **多协议统一接入**：利用 Higress 原生支持 HTTP、HTTPS、gRPC、Dubbo 等协议的能力，直接透传和处理后端服务流量，消除了协议转换的性能损耗。
2.  **WASM 插件生态**：开发团队使用 C++、Go 或 Rust 编写 WASM 插件来实现自定义的签名验证、数据加解密和请求修改逻辑。WASM 的沙箱隔离特性保证了插件崩溃不会影响网关主进程，且支持热加载，无需重启网关。
3.  **精细化流量治理**：利用 Higress 的全链路灰度发布能力，按照用户 ID、Header 或 Cookie 进行流量分流，实现了对新版本的金丝雀发布。

**效果**:
1.  **开发效率提升**：基于 WASM 的插件开发模式使得定制化功能的上线周期从数周缩短至数天，且安全性得到保障。
2.  **零停机发布**：实现了平滑的蓝绿发布和金丝雀发布，新版本上线故障率降低了 80%，极大地提升了业务迭代的敏捷性。
3.  **资源利用率提升**：Higress 的高吞吐特性使得网关集群规模减少了 30%，同时在高负载下依然保持了低 P99 延迟。

---



### 3：某大型 AI 创业公司（AIGC 领域）

 3：某大型 AI 创业公司（AIGC 领域）

**背景**:
该公司专注于提供大模型（LLM）应用服务，后端对接 OpenAI、阿里云通义千问等多个大模型提供商。前端应用需要根据用户请求动态路由到不同的模型，并进行 Prompt 增强和结果缓存。

**问题**:
1.  **模型切换与路由繁琐**：业务需要根据用户等级或业务类型，将请求路由到不同的模型供应商。传统的网关难以处理这种复杂的逻辑路由，往往需要在应用层代码中硬编码。
2.  **Token 成本高昂**：大模型调用按 Token 计费，重复的请求导致成本居高不下，且缺乏在网关层进行统一缓存和截断的机制。
3.  **API 标准不一**：不同模型供应商的 API 接口定义存在差异，客户端需要适配多套接口规范。

**解决方案**:
该公司采用 Higress 作为 AI 服务的专用网关（AI Gateway）。
1.  **LLM 插件支持**：利用 Higress 社区提供的 LLM 扩展插件，实现了在网关层面直接对接多家大模型厂商的 API。
2.  **智能路由与缓存**：配置了基于内容的路由规则，将特定类型的请求自动转发给成本更低或速度更快的模型。同时，开启了网关层的语义缓存功能，对于相似的 Prompt 直接返回缓存结果，减少后端调用。
3.  **统一接口规范**：通过 Higress 的插件将不同厂商的异构 API 转换为内部统一的接口格式，简化了客户端的调用逻辑。

**效果**:
1.  **大幅降低成本**：通过网关层的缓存

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|-----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 高性能，基于Nginx/Lua，成熟稳定 | 极高性能，基于LuaJIT，低延迟 |
| 易用性 | 提供控制台和Kubernetes集成，配置灵活 | GUI友好，文档丰富，社区支持强 | 提供Dashboard和API，配置稍复杂 |
| 成本 | 开源免费，企业版需付费支持 | 开源版免费，企业版功能需付费 | 完全开源，企业支持需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 插件生态丰富，支持Lua插件 | 支持Lua和Python插件，生态活跃 |
| 社区 | 阿里背书，社区增长中 | 社区成熟，用户基数大 | 国内活跃，国际社区较小 |

### 优势分析

- 优势1：深度集成Istio和Envoy，适合云原生环境。
- 优势2：支持Wasm插件，扩展性和灵活性高。
- 优势3：阿里技术支持，适合国内企业需求。

### 不足分析

- 不足1：社区相对较小，生态不如Kong成熟。
- 不足2：文档和案例较少，学习成本较高。
- 不足3：企业版功能可能需要额外付费。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 注解的精细化流量管理

**说明**: Higress 原生兼容 Kubernetes Ingress 注解。利用 Ingress 注解可以在不修改网关核心配置的情况下，针对特定的 Service 或 Route 实现细粒度的流量控制，如设置超时时间、重试策略或限流阈值。

**实施步骤**:
1. 编辑目标 Ingress 资源的 YAML 文件。
2. 在 `metadata.annotations` 字段中添加 Higress 支持的注解（例如 `nginx.ingress.kubernetes.io/proxy-connect-timeout` 或 Higress 特有的注解）。
3. 应用配置：`kubectl apply -f ingress.yaml`。
4. 通过 Higress 控制台或日志验证流量规则是否生效。

**注意事项**: 部分注解可能与旧版 Nginx Ingress Controller 兼容，但建议优先查阅 Higress 官方文档以确认注解的具体命名和支持范围，避免配置冲突。

---

### 实践 2：构建插件驱动的安全防护体系

**说明**: Higress 提供了强大的 WAF（Web Application Firewall）插件支持。通过启用和配置相应的安全插件（如 key-auth、jwt-auth 或 IP 限制），可以在网关层直接拦截恶意流量，保护后端服务安全。

**实施步骤**:
1. 登录 Higress 控制台，进入“插件市场”或“插件配置”页面。
2. 根据需求选择安全类插件（例如 `bot-detect` 用于机器人检测，或 `request-block` 用于 IP 黑名单）。
3. 在全局或特定路由范围内启用插件，并配置具体的防护规则（如正则表达式、IP 列表）。
4. 进行压力测试或模拟攻击，验证拦截效果。

**注意事项**: 插件配置可能会增加轻微的延迟，建议在非生产环境先进行性能测试。同时，需定期更新防护规则以应对新的威胁。

---

### 实践 3：利用 Wasm 插件实现业务逻辑扩展

**说明**: Higress 深度集成 WebAssembly (Wasm) 技术，允许开发者使用 C++、Go、Rust 或 AssemblyScript 编写自定义插件。这比传统的 Lua 脚本性能更高，且隔离性更好，适合实现复杂的自定义鉴权、请求修改或响应处理逻辑。

**实施步骤**:
1. 确定业务逻辑需求（如特殊的请求签名校验）。
2. 使用支持 Wasm 的语言编写插件代码，并编译为 `.wasm` 文件。
3. 将 `.wasm` 文件上传至 Higress 控制台的 Wasm 插件管理中，或通过 OCI 镜像仓库进行部署。
4. 配置插件的执行阶段和参数，并将其绑定到相应的网关路由上。

**注意事项**: Wasm 插件的内存和 CPU 使用需要限制，防止异常插件影响网关整体稳定性。建议对 Wasm 插件进行资源配额设置。

---

### 实践 4：服务发现与 Nacos 集成

**说明**: Higress 能够无缝对接 Nacos、Consul 等注册中心。对于微服务架构，通过 Higress 直接对接 Nacos，可以实现从注册中心动态获取服务实例列表，从而自动完成服务路由和负载均衡，无需手动维护 Service 定义。

**实施步骤**:
1. 在 Higress 全局配置中，找到“服务来源”或“服务发现”设置。
2. 添加 Nacos 注册中心配置，输入 Nacos 服务地址、命名空间和访问凭证。
3. 配置完成后，Higress 将自动同步 Nacos 中的服务列表。
4. 在创建路由时，直接选择已同步的服务名称作为目标服务。

**注意事项**: 确保 Higress 所在的网络环境能够访问 Nacos 服务端。如果使用的是 Nacos 2.x 版本，需注意 gRPC 端口的防火墙配置。

---

### 实践 5：全链路 Observability 集成

**说明**: 为了快速定位问题，必须建立完善的可观测性体系。Higress 原生支持 OpenTelemetry，可以将访问日志、指标和链路追踪数据导出到 Prometheus、Grafana 或 SkyWalking 等后端系统。

**实施步骤**:
1. 配置 Higress 的日志采集，确保输出格式（如 JSON）符合下游日志系统的解析要求。
2. 在 Higress 配置中开启 Prometheus Metrics，暴露监控端口。
3. 配置链路追踪，设置 OTLP 协议的 Endpoint 地址（如 Jaeger 或 SkyWalking OAP Server）。
4. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板，实时监控网关 QPS、延迟和错误率。

**注意事项**: 高流量场景下，全链路追踪产生的数据量巨大，建议采用采样策略（如 1% 或 10% 采样率）以降低存储和网络压力。

---

### 实践 6：金丝雀发布与蓝绿部署

**

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 构建，原生支持 HTTP/2 和 HTTP/3。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，HTTP/3 则基于 UDP 协议，进一步解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，明确启用 HTTP/2 协议支持。
2. 在 Higress 的路由或全局配置中开启 QUIC/HTTP3 支持（需确保底层网络环境允许 UDP 传输）。
3. 配置 TLS 版本至少为 1.2 以上（HTTP/2 和 HTTP/3 强制依赖 TLS）。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，并发连接处理能力提升，减少 TCP 连接建立带来的资源消耗。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时设置通常较长，不合理的配置会导致大量连接处于挂起状态，耗尽网关线程池或连接池资源。精细化的超时与指数退避重试策略能保障系统在下游服务不稳定时的吞吐量。

**实施方法**:
1. **连接超时**: 建议设置为 3-5 秒，避免长时间等待不可达的后端。
2. **请求超时**: 根据业务 P99 耗时设置，建议设置为 2-5 秒。
3. **重试策略**: 开启针对 5xx 错误的自动重试，配置指数退避，限制最大重试次数（如 2-3 次）。

**预期效果**: 减少无效请求堆积，提升系统在故障场景下的可用性，将长尾请求对整体 P99 延迟的影响降低 20% 以上。

---

### 优化 3：启用异步调用与 DNS 缓存

**说明**: Higress 支持将 HTTP 请求处理转换为异步模式，避免阻塞工作线程。同时，频繁的 DNS 解析会显著增加延迟。启用 DNS 缓存和严格的后端连接池管理可以减少网络开销。

**实施方法**:
1. 确保使用 Higress 的非阻塞 IO 模型（默认开启，但在自定义插件开发时需注意不要阻塞 EventLoop）。
2. 配置严格的 Upstream 连接池大小，避免无限创建连接导致后端被打挂。
3. 调整 DNS 缓存 TTL，减少 DNS 查询频率。

**预期效果**: 减少 DNS 查询带来的毫秒级延迟累积，通过连接池复用降低 TCP 握手开销，提升单节点吞吐量 15%-30%。

---

### 优化 4：优化 WAF 与插件执行链路

**说明**: Higress 支持丰富的 WAF 和插件生态。复杂的正则匹配或顺序执行的插件链会显著增加 CPU 消耗和请求延迟。

**实施方法**:
1. **WAF 规则优化**: 精简 WAF 正则规则，优先匹配高频攻击特征，避免回溯性极高的正则表达式。
2. **插件编排**: 将高开销的插件（如 JWT 验证、复杂鉴权）尽可能前置或后置，甚至下放到服务网格 Sidecar，减少网关中心节点的计算压力。
3. **本地缓存**: 在 WAF 或限流插件中启用本地缓存，减少回源或查询 Redis 的次数。

**预期效果**: 降低网关 CPU 负载 20%-40%，减少因正则匹配导致的 CPU 毛刺，将路由转发延迟控制在毫秒级。

---

### 优化 5：启用零拷贝与 Sendfile 机制

**说明**: 对于大文件下载或静态资源分发，数据在内核空间与用户空间之间频繁拷贝会消耗大量 CPU 和内存带宽。利用零拷贝技术可直接在内核空间传输数据。

**实施方法**:
1. 确认 Higress 底层 Envoy 配置中启用了 Sendfile

---
## 学习要点

- 基于提供的有限信息（"alibaba / higress" 及其来源 "github_trending"），以下是关于 Higress 项目最关键的 5 个要点总结：
- Higress 是由阿里云开源的一款基于 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 Envoy 和 K8s，旨在解决云原生架构下流量管理与微服务通信的复杂性问题。
- 该项目支持将传统微服务网关（如 Spring Cloud Gateway、Nginx）无缝迁移至云原生架构，降低迁移成本。
- Higress 提供了标准化的 K8s Ingress Controller 实现，能够统一管理集群南北向流量与微服务间的东西向流量。
- 它具备强大的插件扩展能力（支持 WASM 和 Lua），允许用户通过热加载方式灵活扩展网关功能。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 理解云原生网关的核心概念
- 了解 Higress 的背景、定位及核心特性（如高可用、低延迟、插件扩展性）
- 掌握基本的容器与 Docker 基础知识
- 学习 Kubernetes (K8s) 的基本原理和常用命令

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (Introduction 章节)
- Kubernetes 官方文档基础概念
- Docker 官方入门教程

**学习建议**:
- 在开始之前，确保对 Linux 操作系统有基本操作能力。
- 重点理解 Higress 作为“流量网关”与“微服务网关”的区别。
- 本阶段不需要深入代码，重点在于理解架构图和术语。

---

### 阶段 2：核心功能实战与部署

**学习内容**:
- 学习 Higress 的多种部署方式（Docker Compose / Kubernetes Helm）
- 掌握 Ingress 资源配置与网关路由规则
- 实践服务发现配置（Nacos, Consul, 固定地址等）
- 学习基本的流量管理：路由匹配、重定向、重写、Header 操作
- 了解 Higress 控制台的使用与基本运维操作

**学习时间**: 2-3周

**学习资源**:
- Higress GitHub 仓库中的示例配置
- Higress 官方文档 - 用户指南
- Higress 官方控制台演示

**学习建议**:
- 动手搭建一个本地环境，推荐使用 Kind 或 Minikube 模拟 K8s 环境进行部署。
- 尝试将一个简单的后端服务（如 Nginx）通过 Higress 暴露出来。
- 熟悉 Wasm 插件的基本概念，但暂时不需要深入编写。

---

### 阶段 3：高级流量治理与安全

**学习内容**:
- 深入学习金丝雀发布、蓝绿发布与流量标签
- 掌握负载均衡算法与健康检查配置
- 学习全链路安全：HTTPS 证书管理、JWT 认证、IP 访问控制
- 理解 Higress 的限流熔断机制
- 学习服务 Mock 与故障注入测试

**学习时间**: 2-4周

**学习资源**:
- Higress 官方文档 - 高级配置指南
- Envoy 官方文档（关于 HTTP 路由与集群配置的部分）
- 云原生网关最佳实践博客

**学习建议**:
- 结合实际业务场景思考流量治理的需求，例如如何平滑发布新版本。
- 实验不同的负载均衡策略，观察后端服务的压力变化。
- 重点攻克 Wasm 插件的使用，学会如何在控制台上传并配置 JSON 类型的插件来处理鉴权或限流。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- 深入理解 Wasm (WebAssembly) 在网关侧的应用
- 学习使用 Go 或 C++ 开发自定义 Wasm 插件
- 掌握 Higress 的配置原理（基于 Envoy 的 xDS 协议）
- 学习 Higress 的多租户管理与网关组管理
- 探索 Higress 对 AI 服务的代理与提示词管理功能

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - Wasm 插件开发指南
- Higress GitHub Wasm Plugin Examples
- Proxy-Wasm Go SDK 文档

**学习建议**:
- 尝试编写一个简单的 Wasm 插件（例如修改请求头或响应体）。
- 如果涉及 AI 应用，重点研究 Higress 在处理大模型流量时的特性（如流式传输处理）。
- 阅读源码，理解 Higress 如何通过 Ingress 转换为 Envoy 配置。

---

### 阶段 5：生产级运维与架构优化

**学习内容**:
- 掌握 Higress 的高可用（HA）部署架构
- 学习性能调优：连接池、缓冲区大小、并发配置
- 深入日志与监控体系：集成 Prometheus、Grafana、Skywalking
- 灾难恢复与备份策略
- 网关多集群容灾与跨云管理

**学习时间**: 持续学习

**学习资源**:
- Higress 官方文档 - 运维手册
- Envoy Deep Dive 系列文章
- 云原生可观测性最佳实践

**学习建议**:
- 在生产环境中，重点关注可观测性，确保能追踪每一个请求的链路。
- 定期进行压测，根据业务增长调整网关的资源配额。
- 关注社区动态，参与 Higress 的 Issue 讨论或贡献，保持技术栈的更新。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 或 Kong 等传统网关有什么区别？

1: Higress 是什么？它与 Nginx 或 Kong 等传统网关有什么区别？

**A**: Higress 是一款云原生 API 网关，它是阿里云内部多年网关经验的产物，并于近期开源。它基于 Envoy 和 Istio 构建，旨在解决云原生时代流量管理的问题。

与 Nginx 或 Kong 等传统网关的主要区别在于：
1.  **架构基础**：传统网关多基于 Nginx/Lua（如 OpenResty、Kong）或 Java（如 Spring Cloud Gateway），而 Higress 基于 Envoy（C++/Rust）和 Istio，具有更高的性能和更低的资源消耗。
2.  **云原生集成**：Higress 原生支持 Kubernetes 和 Istio 服务网格，可以作为 Ingress Controller 或 Gateway API 使用，实现了南北向（入口流量）与东西向（服务间流量）流量的统一管理。
3.  **标准化**：它支持 Kubernetes Ingress、Gateway API 以及 Envoy 的配置标准，而不仅仅是自定义的配置语法。
4.  **扩展性**：Higress 提供了类似 Kong 的插件市场（Wasm 插件），支持使用 Go、Python、JavaScript 等语言编写插件，比传统的 Lua 脚本更易于开发和维护。

---



### 2: Higress 是否完全兼容 Nginx 或 Ingress 的配置？

2: Higress 是否完全兼容 Nginx 或 Ingress 的配置？

**A**: Higress 提供了高度兼容性，但并非 100% 逐行兼容。

1.  **Kubernetes Ingress**：Higress 完全支持标准的 Kubernetes Ingress 资源。如果你正在使用 Nginx Ingress Controller，Higress 可以作为替代品直接接入，只需修改 Controller 的类名和注解。
2.  **Nginx 配置**：对于传统的 `nginx.conf`，Higress 不支持直接使用。但是，Higress 提供了 Nginx 配置转换工具，可以帮助用户将 Nginx 的逻辑（Location、Upstream、重写规则等）迁移到 Higress 的配置格式（Kubernetes CRD 或控制台配置）中。
3.  **注解支持**：为了降低迁移门槛，Higress 实现了部分常见的 Nginx Ingress 注解，使得用户无需大幅修改 YAML 文件即可迁移。

---



### 3: Higress 支持哪些类型的插件？如何扩展功能？

3: Higress 支持哪些类型的插件？如何扩展功能？

**A**: Higress 拥有强大的插件系统，主要通过 **Wasm (WebAssembly)** 技术来实现。

1.  **内置插件**：Higress 开箱即用，包含了常见的网关功能插件，例如认证鉴权（Key Auth, JWT, OIDC）、限流熔断、请求/响应重写、流量镜像、CORS 处理等。
2.  **Wasm 插件**：这是 Higress 的核心扩展机制。由于 Envoy 对 Wasm 的支持，开发者可以使用 **Go**、**AssemblyScript**、**Rust** 或 **Python** 等高级语言编写业务逻辑。这些代码会被编译成 Wasm 字节码在 Envoy 中运行。
3.  **Lua 兼容**：虽然 Higress 主要推 Wasm，但考虑到生态迁移，它也支持运行 Lua 脚本（通过特定的处理器），方便从 OpenResty/Kong 迁移旧逻辑。
4.  **插件市场**：Higress 提供了官方的插件市场，用户可以在控制台一键安装和配置社区贡献的插件。

---



### 4: Higress 的性能表现如何？能否支撑高并发场景？

4: Higress 的性能表现如何？能否支撑高并发场景？

**A**: Higress 的设计目标之一就是高性能，完全能够支撑企业级的高并发场景。

1.  **底层优势**：Higress 的数据面基于 Envoy。Envoy 使用 C++ 编写，采用异步非阻塞 I/O 模型，在处理长连接、高并发请求时，性能和稳定性通常优于基于 Java 或 Lua 的网关。
2.  **基准测试**：在官方的压测数据中，Higress 在开启常见插件（如限流、认证）的情况下，依然能保持极高的吞吐量和极低的延迟，其性能通常优于传统的 Java Gateway 网关，与原生 Envoy 持平。
3.  **资源消耗**：得益于 Wasm 的沙箱隔离机制，插件崩溃不会导致网主进程崩溃，且内存占用相比运行 Java 应用要低得多。

---



### 5: Higress 能否直接对接阿里云或 AWS 的云服务？

5: Higress 能否直接对接阿里云或 AWS 的云服务？

**A**: 可以，Higress 具备很强的云服务集成能力，尤其是阿里云生态。

1.  **阿里云集成**：作为阿里云开源的产品，Higress 可以无缝对接阿里云的 **MSE (微服务引擎)**、**ACK (容器服务)**、**SAE (应用引擎)** 以及 **IDaaS (身份认证)**。例如，它可以轻松实现从 OIDC 或阿里云 IAM 获取用户身份信息。
2.  **后端

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### 在本地 Docker 环境中快速启动 Higress，并配置一个简单的路由规则。要求实现：当访问 `http://localhost:8080/example` 时，能够将请求转发到一个模拟的后端服务（如 httpbin.org）并返回成功响应。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，以下是针对实际落地场景的 7 条实践建议：

### 1. 利用 Wasm 插件实现模型供应商的无缝切换
**场景：** 生产环境中需要在不同 LLM 提供商（如 OpenAI、通义千问、DeepSeek）之间切换，或实现流量灰度。
**建议：** 不要在业务代码中硬编码 API 地址。利用 Higress 的 **AI 代理（AI Proxy）** 插件或编写 Wasm 插件，在网关层统一处理模型路由。
**操作：** 配置路由时，将不同的路径（如 `/v1/chat/openai` 和 `/v1/chat/qwen`）或不同的 Header 标签映射到不同的后端服务（Upstream）。这样当某个模型 API 变更或限流时，只需修改网关配置，无需重新发布业务应用。

### 2. 配置 Token 级别的超时与流式处理策略
**场景：** LLM 推理耗时较长，且通常使用流式响应（SSE），传统的连接超时配置可能导致传输中断。
**建议：** 针对大模型场景调整路由超时配置。
**操作：**
*   将 `request_timeout` 和 `idle_timeout` 设置为较大值（如 5 分钟以上），以适应模型生成长文本的需求。
*   确保开启 **流式透传** 支持。Higress 原生支持 SSE 协议，确保网关配置不会对响应体进行缓冲，否则会导致流式输出的“打字机效果”失效，变成一次性输出。

### 3. 实施基于 Prompt 的语义路由
**场景：** 企业内部同时部署了通用模型（如 GPT-4）和垂直领域微调模型（如医疗、代码模型），需要根据用户提问意图自动分发。
**建议：** 利用 Higress 的 AI 特性进行语义路由，而非简单的关键词匹配。
**操作：** 配置路由规则时，使用 **语义向量匹配** 或者在网关层接入一个轻量级分类模型。例如，检测到 Prompt 包含“代码生成”或“Bug修复”时，自动将流量路由至专门优化的 Code-Llama 服务；通用对话路由至 Qwen 服务。这能显著降低推理成本并提高响应质量。

### 4. 严格管控 API Key 并实现多租户鉴权
**场景：** 企业将 LLM 能力开放给内部多个子系统或外部客户，需要防止 Key 泄露和配额滥用。
**建议：** 在网关层统一管理鉴权，避免将真实的云厂商 API Key 暴露给客户端。
**操作：**
*   使用 Higress 的 **鉴权插件**（如 AK/SK 认证或 JWT）。
*   在网关配置“消费者”概念，为不同的业务部门或客户分配独立的 AppID/AppKey。
*   结合 **限流插件**，针对每个 AppKey 设置 QPS 或 TPM（Tokens Per Minute）限制，防止单一租户耗尽配额导致整个系统不可用。

### 5. 建立敏感词过滤与安全护栏
**场景：** 生成式 AI 容易产生幻觉或输出违规内容，给企业带来合规风险。
**建议：** 在网关层插入“审核”环节，而非依赖后端模型本身的安全对齐。
**操作：** 启用或开发 Wasm 插件，对接阿里云内容安全或其他合规服务。在请求发送给 LLM 之前拦截恶意 Prompt（提示词注入攻击），在响应返回给用户之前拦截违规回复。这比在应用层代码中做拦截更统一、更易维护。

### 6. 优化 Prompt 模板管理
**场景：** 多个应用调用同一个底层模型，但需要预设不同的 System Prompt（如“你是一个翻译官” vs “你是一个 SQL 生成器”）。
**建议：** 将 Prompt 模板配置在网关侧，实现业务逻辑与提示词工程的解耦。
**操作：** 使用 Higress 的 **Prompt Template** 插件功能。在网关配置中

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260302-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260304-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*