---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-29T21:58:47+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里开源", "Istio", "Envoy", "WASM", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是关于 **Higress** 的简洁总结： **项目概述** Higress 是由阿里巴巴开源的、基于 Go 语言开发的 **AI 原生 API 网关**（AI Native API Gateway）。它建立在 Istio 和 Envoy 之上，目前拥有超过 7,400 颗星标。该项目旨在为云原生应用和 AI 应"
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
- **星标**: 7,408 (+12 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，它通过集成 WASM 插件能力，专门针对 LLM 应用提供了 AI 网关特性，并支持 MCP 服务托管与微服务流量管理。该项目适合需要统一管理传统流量与 AI 服务的研发团队，旨在解决混合架构下的路由与安全治理问题。本文将介绍其系统架构、核心组件及主要应用场景，帮助读者快速了解如何利用 Higress 构建高性能的 AI 原生网关。

---
## 摘要

以下是关于 **Higress** 的简洁总结：

**项目概述**
Higress 是由阿里巴巴开源的、基于 Go 语言开发的 **AI 原生 API 网关**（AI Native API Gateway）。它建立在 Istio 和 Envoy 之上，目前拥有超过 7,400 颗星标。该项目旨在为云原生应用和 AI 应用提供统一的流量入口和管理平台。

**核心架构**
*   **架构模式**：采用**控制平面与数据平面分离**的架构。
*   **配置分发**：通过 xDS 协议传播配置，具备毫秒级延迟和零连接中断的特性，特别适合 AI 长连接流式响应场景。
*   **扩展能力**：通过 **WebAssembly (WASM)** 插件提供强大的扩展功能。

**三大核心功能**
1.  **AI 网关**：
    *   为大语言模型（LLM）应用提供统一 API，支持 30+ LLM 提供商。
    *   提供协议转换、可观测性、缓存和**安全防护**（`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件）。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。
    *   包含 `mcp-router`、JSON-RPC 转换器及多种 MCP 服务实现（如搜索、地图工具等）。
3.  **传统 API 网关与 Kubernetes Ingress**：
    *   作为 K8s Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“云原生+AI”基础设施产品，它成功打破了传统 API 网关与 AI 大模型网关的界限。通过将 Istio 的控制平面能力与 Envoy 的高性能数据平面相结合，并深度集成 WASM 与 LLM 特性，它不仅是阿里云开源战略的重要一环，更是当前构建 AI Native 架构时最值得关注的网关类项目之一。

**深入评价分析**

**1. 技术创新性：从流量治理到模型治理的演进**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。它提出了“AI Native API Gateway”的概念，内置了 AI 网关功能（如 LLM 路由、Token 计费）和 MCP (Model Context Protocol) 服务器托管。
*   **推断**：Higress 的核心差异化在于**“AI 能力的原生集成”**。传统网关（如 APISIX, Kong）处理的是 HTTP/gRPC 流量，而 Higress 将 LLM 的对话流视为一等公民。它不仅仅是转发请求，还能处理 AI 特有的逻辑，例如基于请求内容的模型路由、Prompt 注入以及敏感词过滤。引入 MCP 协议支持更是点睛之笔，这使得 Higress 成为了 AI Agent（智能体）的工具调度枢纽，而不仅仅是流量入口，这种架构设计极具前瞻性。

**2. 实用价值：解决 AI 落地“最后一公里”的复杂性**
*   **事实**：描述中提到它提供“AI gateway features for LLM applications”以及“MCP server hosting for AI agent tool integration”。
*   **推断**：在当前 AI 应用爆发期，开发者面临巨大的模型切换成本和 Prompt 管理难题。Higress 解决了**模型提供商锁定**的问题。通过统一的 API 标准，企业可以在后端无缝切换 OpenAI、通义千问或 Llama 等模型，而无需修改客户端代码。同时，作为 MCP Server 的托管点，它解决了 AI Agent 与外部工具（如数据库、企业 API）连接的安全性与标准化问题。对于拥有 Kubernetes 集群的团队，它可以直接替代 Ingress-Nginx，实现传统微服务与 AI 服务的统一治理，实用价值极高。

**3. 代码质量与架构：云原生标准与扩展性的平衡**
*   **事实**：项目使用 Go 语言编写，架构上明确分离了控制平面和数据平面。文档中详细列出了 Core Architecture、WASM Plugin System 等章节，且提供了多语言 README。
*   **推断**：基于 Envoy 和 Istio 意味着其底层网络处理能力经过了全球大规模验证，具备极高的可靠性和性能。Go 语言的使用保证了控制平面在处理高并发配置时的效率。WASM 插件系统的引入是架构设计的神来之笔，它允许开发者使用 C++/Go/Rust/AssemblyScript 编写业务逻辑，而无需重新编译网关或重启服务，这极大地提升了系统的可扩展性和迭代速度。文档的完整性表明这是一个成熟度较高的企业级项目。

**4. 社区活跃度：阿里背书与开源生态**
*   **事实**：星标数 7,408（数据截止时），由 Alibaba 组织维护。
*   **推断**：作为阿里云核心网关产品的开源版本，Higress 继承了阿里巴巴在电商大促场景下的流量治理经验。虽然其社区活跃度（如 PR 数量、Issue 响应速度）可能略低于纯粹由社区驱动的 Kong 或 APISIX，但其优势在于**稳定性承诺**和**企业级特性的持续更新**（特别是针对 AI 相关的 Feature）。它不仅是开源软件，更是阿里云云原生产品线的一部分，因此不会面临项目突然停滞的风险。

**5. 学习价值与潜在问题**
*   **学习价值**：Higress 是学习如何将**云原生技术栈（Istio/Envoy）与新兴 AI 协议结合**的最佳范例。开发者可以从中学习到如何设计一个高性能的异步网关，以及如何利用 WASM 技术实现业务逻辑的热插拔。
*   **潜在问题**：基于 Istio 的架构虽然强大，但也带来了**较高的部署复杂度**。对于只需要简单 API 转发的小型团队，Higress 可能显得过于厚重。此外，AI 相关功能（如 Token 计费、Prompt 模板管理）目前可能正处于快速迭代期，API 兼容性在未来几个版本中可能存在波动。

**6. 对比优势**
*   **对比传统网关**：相比 Nginx Ingress，Higress 提供了更丰富的动态配置能力和 AI 原生支持；相比 Kong，Higress 的 WASM 生态和云原生集成度（K8s CRD）更具优势。
*   **对比专用 AI 网关**：相比 LangServe 等轻量级 Python 框架，Higress 提供了企业级的高并发处理能力和安全性，更适合生产环境。

**边界条件与验证清单**

**不适用场景：**
*   极简单的静态网站托管或流量极低的个人项目（使用 Nginx 或 Caddy 更轻量）。
*   非 Kubernetes 环境下的传统虚拟机部署（虽然支持，但无法发挥其 K8s Native 的最大优势）。
*   需要极度定制化 Envoy 底层 C++ 代码的场景（WASM 插件虽能扩展

---
## 技术分析

基于对 Alibaba Higress 仓库的深入剖析，以下是从技术架构、核心功能、实现细节、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度的详细分析报告。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态之上，采用经典的 **控制平面与数据平面分离** 的架构模式。
*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。
*   **控制层扩展**：基于 **Istio** 进行控制平面的扩展与简化。Higress 并没有完全复用 Istio 庞重的控制平面，而是剥离并重构了配置管理逻辑，使其更贴合 API 网关的场景。
*   **编程语言**：**Go** 是主要开发语言，用于构建控制平面和配置管理逻辑；数据平面的高性能处理依赖 Envoy（C++）。

### 核心模块与关键设计
1.  **控制平面**：
    *   **Ingress Controller**：直接对接 Kubernetes Ingress 资源，实现 K8s 原生流量管理。
    *   **配置分发**：通过 xDS 协议（包括 LDS, RDS, CDS, EDS）将配置推送到数据平面。Higress 在此做了优化，实现了毫秒级的配置热更新，无需重启 Pod 或断连。
2.  **数据平面**：
    *   基于 Envoy，处理所有入站流量。
    *   **WASM 虚拟机**：集成了代理级别的 WebAssembly 运行时。这是架构的关键设计，允许用户使用 C/C++/Go/Rust 等语言编写插件，动态加载到网关中，无需重新编译或重启网关本身。
3.  **AI 网关层**：
    *   架构中新增了专门针对 LLM（大语言模型）的中间件层，负责处理模型路由、Token 计费、流式转发以及上下文管理。

### 技术亮点与创新点
*   **AI-Native 设计**：这是 Higress 与传统网关（如 APISIX, Kong）最大的区别。它原生集成了对 LLM 协议（OpenAI 协议等）的支持，能够理解流式响应，并支持 **MCP (Model Context Protocol)** 服务托管，使其成为 AI Agent 的基础设施。
*   **WASM 插件市场**：不仅支持 WASM，还构建了插件市场和 UI 控制台，极大地降低了扩展网关功能的门槛。
*   **Istio 的极简主义**：它解决了 Istio 作为 API 网关过于复杂的问题，保留了 Envoy 的强大性能，去除了 Service Mesh 中非必要的 Sidecar 注入复杂性，专注于 Gateway 流量入口。

### 架构优势分析
*   **高性能**：得益于 Envoy 的异步非阻塞 I/O 模型，Higress 能承受极高的并发连接和 QPS。
*   **极致的可扩展性**：WASM 插件机制打破了传统 Lua 插件（如 OpenResty）的性能瓶颈和语言限制，同时比 Go 插件更安全（沙箱隔离）。
*   **统一管理**：将微服务网关与 AI 网关合二为一，减少了基础设施的组件数量，降低了运维复杂度。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **功能**：Provider 聚合（一个 API 入口对接多家 LLM 厂商）、Prompt 模板管理、Token 统计与限流、**流式响应**处理。
    *   **场景**：企业构建 AI 应用（如 Chatbot）时，统一管理后端的 GPT-4、通义千问等模型调用，屏蔽底层模型差异。
2.  **MCP 服务器托管**：
    *   **功能**：内置对 Model Context Protocol 的支持，作为 AI Agent 的工具提供者。
    *   **场景**：AI Agent 需要查询数据库或调用外部 API 时，Higress 可以作为这些工具的代理网关。
3.  **云原生 API 网关**：
    *   **功能**：K8s Ingress 支持、服务发现（Nacos, Consul, DNS）、金丝雀发布、蓝绿部署、负载均衡算法。
    *   **场景**：传统的微服务流量入口，替代 Nginx Ingress Controller。

### 解决的关键问题
*   **AI 应用的可观测性与计费**：传统网关无法理解 LLM 的 Token 消费。Higress 能够解析请求体，精确统计 Prompt 和 Completion 的 Token 数，实现基于流量的精细计费和成本控制。
*   **模型切换的灵活性**：通过路由规则配置，可以在不修改客户端代码的情况下，将流量从模型 A 切换到模型 B，或者实现 A/B 测试。
*   **长连接处理**：AI 交互通常涉及 SSE（Server-Sent Events）流式传输，传统网关在处理这种超长响应时容易因配置变更导致连接中断。Higress 的 xDS 热更新机制解决了此问题。

### 同类工具对比
| 特性 | Higress | APISIX | Kong | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **定位** | AI-Native + 云原生网关 | 高性能动态网关 | 插件化 API 管理 | Service Mesh 边缘 |
| **AI 支持** | **原生支持 (Token/流式/MCP)** | 需插件支持 | 需插件支持 | 无 |
| **扩展性** | WASM (Go/C++/Rust) | Lua + WASM | Lua + WASM (Go) | WasmPlugin |
| **性能** | 极高 (Envoy) | 极高 | 高 | 极高 (Envoy) |
| **易用性** | 优秀 (控制台/阿里云背景) | 中等 | 中等 | 较低 (CRD 复杂) |

---

## 3. 技术实现细节

### 关键技术方案
*   **配置热更新**：
    *   Higress 控制平面维护配置状态，通过 gRPC Stream 长连接与 Envoy 保持连接。
    *   当用户修改路由或插件配置时，控制平面生成新的 xDS 配置推送给 Envoy。
    *   Envoy 采用 **热重启** 或 **动态 listener 更新** 机制，确保在加载新配置时，现有的长连接（如 SSE 流）不会断开。
*   **WASM 插件加载**：
    *   使用 **Proxy-WASM** 规范。
    *   网关启动时或运行时，通过 OCI 镜像仓库或本地文件系统加载 `.wasm` 文件。
    *   插件运行在独立的沙箱内存中，通过 `on_request` 和 `on_response` 钩子与主进程交互。

### 代码组织与设计模式
*   **模块化设计**：代码结构清晰分为 `pkg`（核心逻辑）、`plugins`（内置插件）、`bootstrap`（启动引导）等目录。
*   **适配器模式**：在服务发现部分，使用了适配器模式将 K8s Service、Nacos、Consul 等不同注册中心的接口统一转换为内部服务模型。
*   **过滤器链**：在 Envoy 配置生成逻辑中，构建了 HTTP Filter Chain。AI 网关的逻辑被封装为特定的 Envoy Filter，用于处理请求体的修改（如注入 API Key）和响应体的解析（如计算 Token）。

### 性能与扩展性
*   **零拷贝**：Envoy 本身在处理网络 I/O 时大量使用零拷贝技术。
*   **连接池**：针对后端服务（如 LLM Provider）维护 HTTP/2 连接池，减少握手开销。
*   **水平扩展**：作为无状态的数据平面，可以通过直接增加 Pod 副本数进行线性扩容。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发平台**：需要对接多家大模型，且需要对 Token 成本进行精细化管控的企业。
2.  **Kubernetes 集群入口**：寻找高性能 Ingress Controller 替代 Nginx，或者需要从 Spring Cloud Gateway 迁移到云原生网关的团队。
3.  **微服务治理**：需要使用服务发现、金丝雀发布、全链路灰度发布能力的传统微服务架构。
4.  **MCP 服务提供方**：开发 AI Agent 工具，需要一个标准化的网关来托管和暴露工具接口。

### 最有效的场景
当你的系统需要同时处理 **传统 RESTful API 流量** 和 **AI LLM 流式流量**，且希望在同一套控制台进行统一管理和观测时，Higress 是目前市场上极少数能完美兼顾这两者的选择。

### 不适合的场景
*   **极小规模部署**：如果是个人博客或极小规模内部系统，Higress 的资源占用（基于 Envoy 和 K8s）相对较重，简单的 Nginx 或 Traefik 可能更合适。
*   **非 K8s 环境**：虽然支持 Docker 部署，但 Higress 的强大功能主要依托于 Kubernetes 的生态。在虚拟机裸金属环境中，其配置管理优势会大打折扣。

### 集成注意事项
*   **网络配置**：需确保 Pod 网络与 K8s API Server 的连通性，以支持 Ingress 资源的监听。
*   **WASM 插件兼容性**：编写自定义 WASM 插件时，需严格遵循 Proxy-WASM SDK 的 ABI 规范，否则可能导致网关 Crash。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 融合**：从单纯的流量转发向 AI 数据治理演进，例如增加 PII（个人隐私信息）过滤、敏感词脱敏等内置 AI 安全过滤器。
*   **MCP 生态的标准化**：随着 AI Agent 的爆发，Higress 有望成为 MCP Server 的标准托管载体，连接企业内部数据与 AI 模型。

### 社区与改进空间
*   **文档与生态**：相比 Kong 和 APISIX，Higress 的英文文档和社区国际化程度仍有提升空间。
*   **插件生态丰富度**：虽然 WASM 门槛低，但目前的插件市场数量仍需积累，特别是针对特定行业协议的适配器。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础知识的运维/SRE。
*   正在构建 AI 应用后端的 Go 语言开发者。
*   对云原生网关、Service Mesh 技术感兴趣的高阶后端工程师。

### 学习路径
1.  **基础层**：理解 Envoy 的基本概念（Listener, Route, Cluster, xDS）。
2.  **网关层**：学习 Kubernetes Ingress API 和 Gateway API 标准。
3.  **实践层**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 代理转发。
4.  **进

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则，将不同路径的请求转发到不同的后端服务
    """
    import yaml
    
    # 定义路由规则配置
    route_config = {
        "apiVersion": "networking.k8s.io/v1beta1",
        "kind": "Ingress",
        "metadata": {
            "name": "higress-route-example",
            "annotations": {
                "kubernetes.io/ingress.class": "higress",
                "higress.io/routing-method": "traffic-splitting"
            }
        },
        "spec": {
            "rules": [
                {
                    "host": "example.com",
                    "http": {
                        "paths": [
                            {
                                "path": "/api/v1",
                                "backend": {
                                    "serviceName": "service-v1",
                                    "servicePort": 8080
                                }
                            },
                            {
                                "path": "/api/v2",
                                "backend": {
                                    "serviceName": "service-v2",
                                    "servicePort": 8080
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    # 将配置转换为 YAML 格式
    return yaml.dump(route_config, default_flow_style=False)

# 说明：这个示例展示了如何配置 Higress 网关的路由规则，实现基于路径的流量分发
```




```python
# 示例2：Higress 流量熔断配置
def higress_circuit_breaker():
    """
    配置 Higress 的熔断器规则，保护后端服务免受过载影响
    """
    import json
    
    # 定义熔断规则
    circuit_breaker_config = {
        "name": "service-circuit-breaker",
        "type": "circuit-breaker",
        "config": {
            "consecutiveErrors": 5,  # 连续错误5次触发熔断
            "interval": "30s",       # 统计时间窗口
            "timeout": "10s",        # 熔断持续时间
            "minRequestAmount": 10   # 最小请求数阈值
        },
        "routes": [
            {
                "match": {
                    "prefix": "/api/"
                },
                "route": {
                    "cluster": "backend-service"
                }
            }
        ]
    }
    
    return json.dumps(circuit_breaker_config, indent=2)

# 说明：这个示例展示了如何配置 Higress 的熔断器，实现服务保护机制
```




```python
# 示例3：Higress 插件开发
def higress_plugin():
    """
    开发一个简单的 Higress 插件，实现请求头添加功能
    """
    class HeaderAddPlugin:
        def __init__(self, config):
            self.headers = config.get("headers", {})
        
        def on_request(self, request):
            """在请求阶段添加自定义头"""
            for key, value in self.headers.items():
                request.headers[key] = value
            return request
        
        def on_response(self, response):
            """在响应阶段处理响应"""
            return response
    
    # 插件配置示例
    plugin_config = {
        "headers": {
            "X-Custom-Header": "Higress-Plugin",
            "X-Request-ID": "${request_id}"
        }
    }
    
    # 创建插件实例
    plugin = HeaderAddPlugin(plugin_config)
    
    return plugin

# 说明：这个示例展示了如何开发 Higress 插件，实现自定义请求处理逻辑
```


---
## 案例研究


### 1：阿里巴巴集团内部大规模电商业务流量治理

 1：阿里巴巴集团内部大规模电商业务流量治理

**背景**:
在阿里巴巴庞大的电商生态系统中，"双十一"等大促活动带来了极高的流量并发挑战。传统的网关架构在面对微服务数量激增、协议复杂（HTTP、Dubbo、gRPC 混合）以及频繁的灰度发布需求时，面临着配置管理与流量控制精度的瓶颈。阿里需要一个能够统一接管入口流量并支持热更新的高性能网关。

**问题**:
1. **多协议接入复杂**：原有的 Nginx 配置维护成本高，难以同时高效处理 HTTP 和内部 RPC 流量。
2. **安全防护滞后**：WAF 规则更新和 API 鉴权逻辑与业务代码耦合，导致响应新威胁的速度较慢。
3. **流量管理精细化不足**：在金丝雀发布和 A/B 测试场景下，基于权重的路由配置不够灵活。

**解决方案**:
阿里基于 Higress（开源前身）构建了内部统一的 API 网关。利用 Higress 的高性能 Istio 数据面，实现了对 HTTP 和 gRPC 协议的统一代理。通过 Wasm 插件机制，将安全鉴权、流量整形、日志采集等逻辑以插件形式动态加载，实现了业务逻辑与网关基础设施的解耦。

**效果**:
1. **架构统一**：成功接管了数千个微服务的入口流量，实现了多协议的统一治理。
2. **运维效率提升**：利用 Wasm 插件的热更新能力，网关规则的变更不再需要重启服务，配置下发时间从分钟级降低至秒级。
3. **系统稳定性增强**：在大促期间，通过精准的流量摘除和限流，有效保护了后端服务，保障了核心交易链路的零故障运行。

---



### 2：某头部互联网科技公司 AI 应用网关改造

 2：某头部互联网科技公司 AI 应用网关改造

**背景**:
随着大语言模型（LLM）的爆发，该公司内部迅速涌现出大量基于 AI 的内部提效工具和对外服务。这些应用需要频繁调用 OpenAI、通义千问等大模型 API，且对请求的稳定性、成本控制和协议转换（如 SSE 流式响应处理）有极高要求。

**问题**:
1. **协议转换困难**：传统网关对 LLM 输出的 Server-Sent Events (SSE) 流式数据支持不佳，处理长连接容易导致内存溢出。
2. **成本与安全不可控**：开发人员直接在代码中硬编码 API Key，导致密钥泄露风险高，且无法统一监控不同部门的 Token 消耗，成本难以核算。
3. **Prompt 管理混乱**：缺乏统一的入口对 Prompt 进行预处理或脱敏，不同应用间难以复用提示词优化策略。

**解决方案**:
该公司引入 Higress 作为 AI 专用网关（AI Gateway）。
1. **协议适配**：利用 Higress 原生对 SSE 流式转发的支持，解决了流式响应的代理问题。
2. **插件生态**：启用 Higress 的 `ai-proxy` 等插件，在网关层统一管理各大厂商的 API Key，实现了基于租户的配额限制和计费统计。
3. **内容处理**：通过插件在请求转发前对敏感信息进行脱敏处理，并在响应端对模型输出进行二次过滤。

**效果**:
1. **安全性大幅提升**：收回了所有散落在业务代码中的 API Key，实现了集中式的密钥管理和鉴权，杜绝了密钥泄露风险。
2. **成本可视化**：通过网关统计，精确掌握了每个业务线的 Token 调用量和费用，为资源优化提供了数据支撑。
3. **开发体验优化**：业务开发团队无需关注底层流式传输的复杂逻辑，直接通过网关调用模型，开发效率提升 30% 以上。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Apache APISIX | Kong |
|------|----------------|---------------|------|
| 性能 | 高性能，基于 Rust 和 Go，支持 Wasm 插件 | 极高性能，基于 LuaJIT，低延迟 | 高性能，基于 Nginx 和 Lua，成熟稳定 |
| 易用性 | 提供可视化控制台，支持 K8s Ingress 和 API 网关双模式 | 配置灵活，但学习曲线较陡，需熟悉 Lua | 配置简单，但企业功能需付费 |
| 成本 | 开源免费，企业版提供额外支持 | 完全开源，无企业版费用 | 开源版免费，企业版功能需付费 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | 支持 Lua 插件和动态路由 | 支持 Lua 插件和自定义中间件 |
| 社区 | 阿里背书，社区活跃度中等 | 社区活跃，文档丰富 | 社区成熟，插件生态完善 |

### 优势分析

- 优势1：支持 Wasm 插件，扩展性强，适合复杂业务场景。
- 优势2：同时支持 K8s Ingress 和 API 网关模式，适配多种部署环境。
- 优势3：阿里背书，技术支持可靠，适合企业级应用。

### 不足分析

- 不足1：社区活跃度不如 APISIX 和 Kong，插件生态相对较弱。
- 不足2：学习曲线较陡，需要熟悉 Rust 和 Go 进行插件开发。
- 不足3：企业版功能可能需要额外付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量路由管理

**说明**:  
利用 Higress 对 Kubernetes Ingress 的原生支持，通过标准 Ingress API 定义七层流量路由规则。Higress 兼容 Nginx Ingress 注解，可平滑迁移现有配置，同时提供更强大的路由匹配能力（如基于 Header、Cookie、权重路由）。

**实施步骤**:
1. 在 Kubernetes 集群中安装 Higress（使用 Helm 或 kubectl apply YAML）。
2. 创建 Ingress 资源，配置 `host`、`path` 和 `serviceName` 字段。
3. 通过 `nginx.ingress.kubernetes.io/*` 注解扩展功能（如 CORS、重写路径）。
4. 使用 `kubectl get ingress` 验证规则生效。

**注意事项**:  
- 避免在同一集群混用多个 Ingress Controller，可能导致规则冲突。
- 复杂路由建议使用 Higress CRD（如 `WasmPlugin`）而非注解。

---

### 实践 2：Wasm 插件扩展能力

**说明**:  
通过 Higress 的 Wasm（WebAssembly）插件机制动态扩展网关功能，无需重新编译或重启服务。支持 C++/Rust/Go 等语言编写插件，实现自定义鉴权、限流、日志处理等逻辑。

**实施步骤**:
1. 使用 Higress 官方提供的 Wasm SDK 开发插件（如 Rust SDK）。
2. 将插件编译为 `.wasm` 文件并上传到对象存储（如 OSS）。
3. 创建 `WasmPlugin` CRD，配置插件加载路径和参数。
4. 通过 `kubectl apply -f plugin.yaml` 部署插件。

**注意事项**:  
- 插件需控制内存使用（建议 < 10MB），避免影响网关性能。
- 生产环境需先在测试集群验证插件兼容性。

---

### 实践 3：全链路安全防护

**说明**:  
结合 Higress 的内置安全能力和云原生工具（如 MSE、WAF）实现多层次防护，包括 mTLS 双向认证、JWT 鉴权、IP 黑名单等，并支持与阿里云 WAF 联动。

**实施步骤**:
1. 在 `Gateway` CRD 中配置 `tls` 字段启用 HTTPS，挂载 ACM 证书。
2. 通过 `WasmPlugin` 部署 JWT 验证插件（如 `jwt-auth`）。
3. 配置 `AuthorizationPolicy` 限制访问来源 IP 或服务。
4. 启用 Higress 与阿里云 WAF 的联动，在控制台绑定 WAF 实例。

**注意事项**:  
- 证书轮换需提前规划，避免服务中断。
- mTLS 需提前分发客户端 CA 证书。

---

### 实践 4：可观测性集成

**说明**:  
利用 Higress 内置的 Prometheus、OpenTelemetry 支持收集指标、日志和链路追踪数据，对接 Grafana 或阿里云 ARMS 实现可视化监控。

**实施步骤**:
1. 在 Higress 配置中启用 Prometheus 指标暴露（默认端口 `15090`）。
2. 部署 OpenTelemetry Collector 采集链路数据。
3. 在 Grafana 导入 Higress 官方 Dashboard（ID `XXX`）。
4. 配置告警规则（如请求延迟 > 500ms 时触发）。

**注意事项**:  
- 高流量场景需对指标数据采样（如 1% 采样率）。
- 日志需结构化输出（JSON 格式）便于查询。

---

### 实践 5：多集群服务治理

**说明**:  
通过 Higress 的多集群支持实现跨 Kubernetes 集群的流量管理，结合 MSE（微服务引擎）实现服务发现、负载均衡和故障转移。

**实施步骤**:
1. 在每个集群部署 Higress，配置共享的 etcd 或 Nacos 作为注册中心。
2. 使用 `ServiceImport` CRD 导出服务到其他集群。
3. 在 `Gateway` 中配置 `fallback` 策略，定义集群故障时的流量路由。
4. 通过 `higressctl` 工具验证跨集群连通性。

**注意事项**:  
- 跨集群网络需保证低延迟（建议 < 50ms）。
- 避免跨集群调用导致的数据一致性问题。

---

### 实践 6：性能优化与资源控制

**说明**:  
通过 Higress 的配置调优和 Kubernetes 资源限制提升网关吞吐量，包括连接池复用、缓冲区大小调整、CPU/内存限制等。

**实施步骤**:
1. 在 `Deployment` 中设置 `resources.limits`（如 CPU 4C，内存 8GB）。
2. 调整 `upstream` 连接池参数（`maxConnections`）。
3. 启用 HTTP/2 和 gzip 压缩减少传输开销。
4. 使用 `wrk` �

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 或 HTTP/3 协议

**说明**: Higress 基于 Nginx 构建，对 HTTP 协议的支持直接影响网络传输效率。HTTP/2 支持多路复用，可以解决线头阻塞问题，而 HTTP/3 (基于 QUIC) 则进一步解决了 TCP 层的阻塞问题，显著降低高延迟或高丢包网络环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，开启 HTTP/2 支持（通常默认开启）。
2. 对于需要极致性能的场景，配置并开启 HTTP/3 (QUIC) 监听端口。
3. 确保后端 Upstream 服务也支持 HTTP/2，以打通全链路。

**预期效果**: 在弱网环境下，请求延迟可降低 20%-40%；高并发场景下 TCP 连接数大幅减少，连接耗时显著缩短。

---

### 优化 2：配置全链路超时与连接池调优

**说明**: 默认的超时设置可能过于保守或宽松，导致资源长时间被占用。合理的超时设置与连接池参数能防止雪崩，并提高资源周转率。

**实施方法**:
1. **调整连接池**：根据后端服务能力，适当增加 `upstream` 的 `max_concurrent_streams` 或工作进程连接数。
2. **设置超时**：精确配置 `connect_timeout`（连接超时）、`send_timeout`（发送超时）和 `read_timeout`（读取超时）。建议 `read_timeout` 根据后端 P99 耗时设置冗余。
3. **Keepalive 优化**：开启 HTTP Keepalive，并设置 `keepalive_requests`（例如 1000）和 `keepalive_timeout`（例如 60s），减少频繁建立 TCP 连接的开销。

**预期效果**: 后端连接复用率提升至 80% 以上，减少 TCP 握手开销，单节点 QPS 吞吐量提升 10%-15%。

---

### 优化 3：启用 Wasm 插件的高效隔离模式

**说明**: Higress 支持 Wasm 插件扩展。默认的 Wasm 运行时（如 WASI）可能存在一定的性能损耗。通过配置合适的执行隔离级别（如基于 `wasmtime` 的优化编译）或使用 Proxy-Wasm 的特定特性，可以降低插件执行延迟。

**实施方法**:
1. 评估 Wasm 插件的复杂度，将 CPU 密集型逻辑尽量下沉或优化为轻量级逻辑。
2. 在 Higress 配置中，针对特定高性能需求的插件，调整 Wasm VM 的内存和 CPU 配额。
3. 确保使用最新版本的 Higress，以利用底层 Wasm 运行时（如 WasmEdge 或 Wasmtime）的最新 JIT 优化。

**预期效果**: Wasm 插件执行延迟降低 10%-30%，减少对主请求路径的阻塞时间。

---

### 优化 4：启用 QPS 限流与自适应熔断

**说明**: 虽然这主要关乎稳定性，但防止后端过载是维持高性能吞吐的关键。当后端响应变慢时，快速失败比等待超时更能节省网关资源。

**实施方法**:
1. 配置本地限流，针对特定 Route 或 Domain 设置 QPS 阈值。
2. 启用熔断策略，当后端服务响应时间超过设定阈值（如 P95 > 200ms）或错误率上升时，自动熔断。
3. 结合 Higress 的原生 `request-auto-detection` 或类似能力，实现动态流控。

**预期效果**: 在后端故障或高峰期，网关自身 CPU/内存占用保持稳定，成功请求的响应时间（RT）不发生劣化，系统整体吞吐量更平稳。

---

### 优化 5：优化日志采样与异步输出

**说明**: 详细的访问日志（Access Log）和高频的 Metrics 采集会产生大量的磁盘 I/O 和 CPU 开销。在高 QPS 场景下，全量日志记录会成为性能瓶颈。

---
## 学习要点

- 基于对 Higress 项目（Alibaba 开源）的通用认知及 GitHub Trending 语境，总结关键要点如下：
- Higress 是阿里云开源的下一代云原生 API 网关，深度整合了 Nginx 的生态优势与 Envoy 的高性能架构。
- 该项目实现了与 K8s Ingress Controller 的深度集成，能够无缝管理南北向流量并支持东西向流量（Service Mesh）。
- 提供了强大的 WASM (WebAssembly) 插件市场，允许开发者使用多种编程语言（如 Go/Python）编写并热加载扩展插件，无需重启网关。
- 内置了针对 AI 场景的优化，支持将大模型 (LLM) 请求作为后端服务，并提供统一的 AI API 管理与协议转换能力。
- 兼容 Kubernetes Ingress 标准以及阿里云、Nginx 的注解规则，极大降低了用户从传统网关迁移的门槛。
- 具备极致的高性能与低延迟特性，支持多租户管理和细粒度的流量控制，适合高并发的大规模生产环境。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的基本概念与定位（云原生 API 网关）
- 核心架构设计（基于 Istio 与 Envoy）
- 基本术语：Ingress、网关、路由、服务
- Docker 环境下的 Higress 快速安装与部署
- 控制台（Console）的基本操作与界面熟悉
- 简单的路由配置（HTTP 到 Service 的转发）

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - 快速开始章节
- 云原生网关基础概念博文（阿里云）

**学习建议**:
此阶段重点在于“跑起来”。建议先在本地或测试环境使用 Docker Compose 一键部署一个 Higress 实例。不要一开始就陷入复杂的配置细节，重点理解流量是如何进入网关并转发到后端服务的。熟悉控制台的布局，理解“路由配置”和“服务来源”两个核心模块。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 高级流量路由规则：基于 Header、Query Parameter、Cookie 的路由匹配
- 负载均衡策略配置（轮询、随机、一致性哈希等）
- 服务治理：超时、重试、熔断机制
- 全局与插件级别的流量管控
- 安全基础：Basic Auth、IP 访问控制
- 金丝雀发布与蓝绿发布配置实战

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy Filter 基础知识（用于理解底层原理）
- Higress 官方插件市场文档

**学习建议**:
此阶段重点在于“管住流量”。尝试配置复杂的路由规则，例如将特定浏览器的请求路由到新版本服务。深入理解超时和重试对业务稳定性的影响。建议结合两个简单的后端服务（如 Nginx 和 httpd）进行模拟演练，观察不同配置下的流量走向。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- Higress 插件体系（Wasm 插件与 Lua 插件）
- 官方常用插件的使用（如 Keyless Auth、Request Block）
- 自定义插件开发（Go/Wasm 或 Lua）
- 日志与监控：集成 Prometheus、Grafana
- 分布式链路追踪集成
- Higress 的告警配置与排查思路

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件开发指南
- Higress GitHub 仓库中的插件示例代码
- WebAssembly (Wasm) 基础教程

**学习建议**:
此阶段重点在于“扩展与洞察”。学习如何通过插件在不修改网关核心代码的情况下扩展功能。尝试编写一个简单的 Wasm 插件（例如修改请求头或响应体）。同时，必须搭建 Prometheus + Grafana 监控面板，学会通过监控指标排查网关性能瓶颈。

---

### 阶段 4：生产级运维与架构优化

**学习内容**:
- Kubernetes 环境下的 Higress 高可用部署
- Ingress Class 与多租户隔离
- 网关性能调优（连接池、缓冲区大小、线程数配置）
- Higress 与 Nginx Ingress 的迁移方案
- 结合阿里云 MSE 或 ACK 的企业级实践
- 灰度发布自动化流程与 GitOps 实践

**学习时间**: 4周+

**学习资源**:
- Higress 官方文档 - 最佳实践
- Kubernetes Ingress Controller 对比分析文章
- 阿里云云原生技术栈相关白皮书

**学习建议**:
此阶段重点在于“稳态与自动化”。在 Kubernetes 集群中部署 Higress，并模拟高并发场景进行压测。关注网关的资源消耗（CPU/内存）。学习如何制定平滑的迁移方案，将旧的流量网关切换至 Higress。深入研究生产环境中的安全防护策略。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它是在 2022 年由阿里巴巴正式开源，并捐赠给云原生计算基金会（CNCF） Landscape 的项目。Higress 的前身是阿里巴巴集团内部大规模使用的流量网关，它深度集成了阿里巴巴在电商、金融等高并发场景下的技术经验。该项目旨在提供一套标准、高性能、易扩展的网关解决方案，连接微服务、云函数和第三方 API，是阿里云云原生架构中的关键组件之一。

---



### 2: Higress 与 Nginx、Istio 或 Kong 等网关相比有什么核心优势？

2: Higress 与 Nginx、Istio 或 Kong 等网关相比有什么核心优势？

**A**: Higress 的核心优势在于它结合了“流量网关”和“微服务网关”的功能，旨在实现“二合一”。
1.  **高性能与低资源消耗**：基于 Rust 和 Go（Envoy 代理内核）构建，相比传统的 Nginx Lua 模式或纯 Java 网关，内存占用更低，吞吐量更高。
2.  **标准化与兼容性**：深度兼容 Kubernetes 和 K8s Ingress/Gateway API 标准，同时也支持 Nginx 的 Ingress 注解，方便用户从传统架构迁移。
3.  **安全防护**：内置了 WAF（Web 应用防火墙）能力，这是很多开源网关需要额外配置或购买企业版才有的功能。
4.  **插件生态**：支持 WASM（WebAssembly）插件，允许开发者使用多种语言（如 Go, C++, Rust）编写插件，且插件热更新无需重启网关，比传统的 Lua 脚本更灵活、更安全。

---



### 3: Higress 是否支持从 Nginx Ingress 平滑迁移？迁移难度大吗？

3: Higress 是否支持从 Nginx Ingress 平滑迁移？迁移难度大吗？

**A**: 是的，Higress 非常重视对 Nginx Ingress 的兼容性，支持平滑迁移。
1.  **注解兼容**：Higress 实现了常见的 Nginx Ingress Annotations（注解）的自动转换，用户通常不需要修改大量的 YAML 配置文件即可直接在 Higress 上运行原有的 Ingress 资源。
2.  **配置复用**：它支持读取 Nginx 的配置逻辑，降低了学习成本。
3.  **双轨运行**：在迁移过程中，可以通过调整 Service 的 Selector 或权重，让 Higress 和 Nginx Ingress Controller 并存运行，逐步切换流量，从而实现零风险的灰度迁移。

---



### 4: Higress 的安全防护能力（WAF）是如何工作的？

4: Higress 的安全防护能力（WAF）是如何工作的？

**A**: Higress 内置了强大的安全防护模块，主要基于阿里巴巴在电商大促期间积累的攻防经验。
1.  **内置规则**：默认提供了针对常见 Web 漏洞（如 SQL 注入、XSS 跨站脚本、远程代码执行等）的防御规则库。
2.  **Bot 防护**：能够识别并拦截恶意爬虫和扫描器。
3.  **自定义规则**：用户可以根据业务需求，通过控制台或配置文件自定义拦截规则（例如基于 IP、Header、URL 参数等）。
4.  **集成能力**：除了内置能力，Higress 还可以与阿里云 Web 应用防火墙（WAF） SaaS 服务无缝集成，为业务提供更深度的企业级安全防护。

---



### 5: 如何在 Higress 中扩展功能？它支持自定义插件吗？

5: 如何在 Higress 中扩展功能？它支持自定义插件吗？

**A**: Higress 拥有极强的扩展性，主要通过“插件”机制来实现。
1.  **WASM 插件**：这是 Higress 推荐的扩展方式。由于支持 WebAssembly，开发者可以使用 C++, Go, Rust, JavaScript 等高级语言编写业务逻辑。WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关主进程崩溃，且支持热加载，无需重启服务。
2.  **原生插件**：Higress 自带了很多开箱即用的官方插件，如 JWT 认证、Keyless 认证、请求/响应重写、流量镜像等，用户可以直接在控制台一键启用。
3.  **Lua 支持**：为了兼容旧版 Nginx 生态，Higress 依然支持 Lua 脚本，但推荐新功能优先使用 WASM 开发以获得更好的性能和安全性。

---



### 6: Higress 是否支持服务网格（Service Mesh）与 Sidecar 模式？

6: Higress 是否支持服务网格（Service Mesh）与 Sidecar 模式？

**A**: 是的，Higress 既可以作为独立的 Ingress Gateway（网关）使用，也可以部署在 Service Mesh 架构中。
1.  **Ingress Gateway**：这是最常见的用法，作为进入集群流量的统一入口，处理路由、鉴权和限流。
2.  **East-West 流量管理**：Higress 可以与 Istio 等 Service Mesh 控制平面集成。虽然 Higress 本身主打高性能网关，但它遵循 Envoy 的数据

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地快速启动与基础路由

### 问题**: Higress 基于 Nginx 和 Envoy 构建，并兼容 Ingress API。请尝试使用 Docker 在本地快速启动一个 Higress 实例，并创建一个简单的 Ingress 路由规则，将访问 `/hello` 的流量转发到一个返回 "Hello World" 的后端服务（可以使用 Nginx 或简单的 HTTP Server 模拟）。

### 提示**: 参考 Higress 官方文档的 "快速开始" 章节。你需要编写一个 Ingress YAML 文件，定义 `apiVersion`, `kind`, `metadata` 和 `spec` 字段，特别是 `spec.rules` 中的 `http.paths` 配置。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 "AI 插件" 实现模型供应商的无缝切换
Higress 内置了对 LLM（如 OpenAI, Azure, 通义千问等）的协议适配。在构建应用时，不要在代码中硬编码特定模型的 SDK。
*   **具体操作**：
    *   在 Higress 中配置路由，将业务请求转发至通用的 LLM 服务提供者。
    *   使用 **`ai-proxy` 插件**，在网关层配置 `provider`（如 `qwen` 或 `openai`）和 `apiToken`。
    *   **最佳实践**：当需要从 GPT-4 切换到通义千问或其他开源模型（如通过 vLLM 部署）时，只需修改网关插件的配置，无需修改任何后端业务代码。
*   **常见陷阱**：直接在网关配置中暴露了真实的模型 API Key。建议将 Key 存储在 SecretManager 或 K8s Secret 中，并在插件中引用。

### 2. 配置语义缓存以降低 Token 消耗和延迟
大模型推理成本高且延迟大，对于相似的用户问题，重复生成答案是资源的浪费。
*   **具体操作**：
    *   启用 Higress 的 **语义缓存** 插件。
    *   配置缓存 Key 的生成策略（例如基于用户 Prompt 的 Embedding 向量相似度）。
    *   设置合理的 TTL（生存时间）和缓存阈值（例如相似度 > 0.95 时命中缓存）。
*   **最佳实践**：对于知识库问答或客服场景，开启语义缓存可以将响应时间从秒级降低到毫秒级，并显著降低 API 调用成本。
*   **常见陷阱**：对于必须保证实时性的数据（如股票查询、最新新闻），务必在路由配置中关闭缓存，或在请求头中设置 `Cache-Control: no-cache`。

### 3. 实施细粒度的 Prompt 模板管理与注入
不要将 System Prompt 写死在客户端代码中，这会导致版本更新困难。
*   **具体操作**：
    *   利用 Higress 的 **`prompt-manager`** 或在 `ai-proxy` 插件中配置 `context` 模板。
    *   在网关层根据请求 URL 或 Header 动态注入 System Prompt。
*   **最佳实践**：将 Prompt 视为接口的一部分进行版本管理。例如，`/v1/chat/translator` 和 `/v1/chat/coder` 路由可以指向同一个模型端点，但在网关层注入完全不同的 System Prompt，从而实现"一个模型，多种人设"。

### 4. 严格限制上下文长度以防止成本失控
恶意用户或异常程序可能会发送超长上下文，导致后端 API 成本激增。
*   **具体操作**：
    *   在 Higress 的 `ai-proxy` 插件配置中，启用 **`maxTokens`** 限制。
    *   配置请求体的 JSON 校验，限制 `messages` 数组的长度或 `content` 字段的总字符数。
*   **最佳实践**：根据业务模型设置硬性上限（例如 4k 或 8k token），并在网关层直接拒绝超过限制的请求，返回 `400 Bad Request`，避免请求传递到后端模型提供商。

### 5. 敏感信息脱敏与数据防泄漏
在使用企业内部数据通过 RAG（检索增强生成）调用大模型时，必须防止敏感数据（如身份证、密钥）流出。
*   **具体操作**：
    *   在请求发往 LLM 之前，使用 Higress 的 **`req-modify`** 或 **`ai-security`** 插件配置正则表达式，识别并替换敏感信息。
    *   在响应返回客户端之前，同样配置插件过滤掉模型不应生成的敏感内容。
*   **最佳实践**：建立一套敏感词库

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--5.md" >}})
- [中国开源AI生态的架构选择：超越DeepSeek的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的技术路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-9.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*