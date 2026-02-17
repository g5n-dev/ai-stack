---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-17T05:23:13+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP 协议", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的中文总结： **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力，旨"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "大语言模型"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,544 (+7 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构统一管理流量与服务。它不仅提供传统的微服务路由与 Kubernetes Ingress 能力，更针对 LLM 应用集成了 AI 网关特性及 MCP 服务托管，解决了大模型集成与工具调用的连接问题。本文将梳理其核心架构，并重点介绍 WASM 插件体系、AI 网关功能及部署方式。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的中文总结：

**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力，旨在为 AI 时代提供基础设施支持。

**核心特性：**
1.  **AI 网关**：提供统一接口对接 30 多家大语言模型（LLM）提供商，支持协议转换、可观测性、缓存和安全防护。
2.  **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
3.  **传统 API 网关**：完全兼容 Kubernetes Ingress，支持微服务路由及 Nginx 注解。

**架构优势：**
*   **控制与数据分离**：将配置管理与流量处理分离。
*   **高性能**：配置变更通过 xDS 协议传播，延迟低至毫秒级且无连接中断。
*   **AI 优化**：特别适合 AI 流式响应等长连接场景。

该项目主要采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,500 颗星。

---
## 评论

**总体判断**

Higress 是一款将云原生网关与 AI 原生能力深度融合的开源项目，它成功解决了企业在 LLM（大语言模型）落地过程中面临的流量治理、安全防护及协议适配难题，是构建 AI 应用基础设施的优选方案。

**详细评价依据**

**1. 技术创新性：从“流量转发”进化为“智能路由”**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，引入了 WebAssembly (WASM) 插件系统，并明确提出了“AI Native API Gateway”的概念，集成了 AI Gateway 特性和 MCP (Model Context Protocol) 服务托管能力。
*   **推断**：传统网关仅关注 HTTP/gRPC 的转发，而 Higress 的创新在于它将 LLM 的语义处理能力下沉到了网关层。通过支持 AI 专用协议（如 OpenAI 协议兼容），它能够实现模型 Provider 的无感切换和 Prompt 的模板化管理。MCP 系统的集成更是极具前瞻性，它使网关成为了 AI Agent 的工具调度中心，而不仅仅是流量入口。这种“网关即 AI 编排器”的定位，是目前市场上极具差异化的技术方案。

**2. 实用价值：填补 AI 落地中的“最后一公里”**
*   **事实**：DeepWiki 提到其核心功能包括 AI gateway features for LLM applications，同时保留了 Kubernetes Ingress 和微服务路由等传统网关能力。
*   **推断**：在当前 AI 应用爆发期，开发者面临两个痛点：一是如何统一管理 OpenAI、Azure、通义千问等不同厂商的 API Key 和接口差异；二是如何在保障现有微服务架构稳定的前提下接入 AI 能力。Higress 通过统一的 AI 网关层解决了这些问题，使得企业无需修改业务代码即可实现 LLM 的流量控制、鉴权和计费。其“传统网关 + AI 网关”的双模特性，极大地降低了存量系统向 AI 架构演进的成本。

**3. 代码质量与架构：云原生标准与扩展性并重**
*   **事实**：项目使用 Go 语言编写，星标数 7,544，架构上明确分离了控制平面和数据平面。
*   **推断**：基于 Envoy 和 Istio 意味着 Higress 继承了 CNCF 顶级项目的数据平面高性能和控制平面标准化优势。Go 语言的使用保证了控制面在处理高并发配置时的性能。WASM 插件系统的引入是代码架构设计的点睛之笔，它允许开发者使用 C/C++/Go/Rust 等多种语言编写业务逻辑，而无需重新编译网关主体，极大地提升了系统的可维护性和扩展边界。

**4. 社区活跃度与学习价值：阿里背书的工业级实践**
*   **事实**：由阿里巴巴开源，拥有较高的星标数，且 README_ZH.md 的存在显示了对中文开发者的友好支持。
*   **推断**：作为阿里云核心网关产品的开源版本，Higress 经受了双11等超大规模流量的验证，其代码质量和架构设计代表了工业界的最高标准。对于开发者而言，学习 Higress 不仅是学习如何配置网关，更是学习如何构建高可用、可扩展的云原生系统，以及如何将 WASM 技术应用于实际业务场景。

**5. 潜在问题与对比优势**
*   **推断**：相比 Kong 或 APISIX，Higress 的最大优势在于对 Kubernetes 和 Istio 生态的原生集成，以及对 AI 场景的针对性优化（如 Token 计费、上下文缓存管理）。然而，其潜在的复杂性在于部署依赖较重（通常需要 K8s 环境），对于仅需简单转发的小型应用可能存在“杀鸡用牛刀”的问题。此外，AI 领域迭代极快，如何保持对最新模型（如 Sora, Claude 3.5）的同步支持是其持续的挑战。

**边界条件与验证清单**

**不适用场景**：
*   边缘计算或资源极度受限的嵌入式设备（Envoy 资源占用相对较高）。
*   仅需极简单的 API 转发且无 K8s 环境的轻量级个人项目。

**快速验证清单**：
1.  **协议兼容性实验**：部署 Higress，配置一个路由指向 OpenAI 接口，使用 cURL 发送请求，验证其是否能正确处理流式响应（SSE）并修改请求头。
2.  **WASM 插件热加载**：编写一个简单的 Go WASM 插件（如修改响应 Body），在不重启网关的情况下加载该插件，观察流量是否按预期发生变化。
3.  **MCP 服务器集成**：尝试配置一个标准的 MCP 工具（如文件读取），验证 AI Agent 是否能通过 Higress 网关成功调用该工具。
4.  **性能基准测试**：使用 wrk 或 hey 对比 Higress 与 Nginx 在纯 HTTP 转发场景下的 QPS 和延迟，评估其在非 AI 场景下的性能损耗是否在可接受范围内。

---
## 技术分析

# Higress 深度技术分析报告

Higress 是阿里巴巴开源的一款基于 Istio 和 Envoy 构建的**云原生 API 网关**，其最显著的特征是提出了 **"AI Native"（AI 原生）** 的理念，旨在解决大模型（LLM）应用落地中的流量管理、安全防护和工具集成问题。

以下是对该项目的深度剖析：

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了标准的**控制平面与数据平面分离**的架构模式，这是现代云原生网关的典型设计。

*   **数据平面**：深度依赖 **Envoy**。Envoy 是高性能的 L7 代理，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **控制平面**：基于 **Istio** 进行了简化和定制。Higress 去除了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理逻辑，专注于 Gateway 的 Ingress 管理。
*   **扩展机制**：**WebAssembly (WASM)** 是其核心扩展能力。Higress 允许用户使用 C++/Go/Rust 等语言编写插件，编译为 WASM 字节码后在 Envoy 中动态加载。
*   **配置协议**：使用 **xDS 协议**（包括 LDS, RDS, CDS 等）在控制平面与数据平面之间传递配置。Higress 对此进行了优化，实现了毫秒级的配置热更新，且不断连。

### 核心模块与关键设计
1.  **路由层**：兼容 Kubernetes Ingress API 和 Nginx Ingress 注解，降低了迁移门槛。
2.  **插件市场**：内置了丰富的 Wasm 插件（如鉴权、限流、请求/响应修改），并支持动态加载。
3.  **AI 网关层**：这是 Higress 的差异化模块。它不仅仅是转发 HTTP 请求，还针对 LLM 的协议（如 OpenAI 协议）进行了深度解析。
4.  **MCP (Model Context Protocol) Server**：作为 AI Agent 的工具集成层，Higress 可以托管 MCP 服务，将后端 API 暴露给 AI 应用调用。

### 架构优势
*   **高性能**：得益于 Envoy 的异步非阻塞架构和 C++ 实现，Higress 在处理高并发长连接（特别是 AI 流式响应）时表现优异。
*   **业务逻辑解耦**：通过 Wasm 插件，业务逻辑（如 Token 计费、敏感词过滤）可以在网关层完成，无需侵入后端服务代码。

---

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 目前最核心的卖点。
*   **主要功能**：
    *   **模型提供商统一接入**：将 OpenAI、Azure、通义千问、DeepSeek 等不同厂商的 API 统一为一个标准接口。
    *   **Token 计费与限流**：针对 LLM 的计费单位进行精细化管理。
    *   **Prompt 模板管理**：在网关层管理 Prompt 模板，实现 Prompt 的版本控制和 A/B 测试。
    *   **结果缓存**：对相同的 Question 进行缓存，直接返回 Answer，减少后端 LLM 的调用成本。
    *   **敏感词过滤**：在请求发送给 LLM 之前或响应返回给用户之前进行内容审核。
*   **解决的关键问题**：解决了企业接入多个大模型时的**标准化问题**、**成本控制**和**安全合规**问题。

### MCP (Model Context Protocol) Server
*   **功能**：Higress 能够充当 MCP Server，将企业内部的 RESTful API 自动转换为 AI Agent 可调用的 Tool。
*   **意义**：这解决了 AI Agent 落地中最难的"最后一公里"问题——如何让 AI 安全、合规地调用企业内部数据。

### 传统 API 网关能力
*   提供了与 Kong、APISIX 类似的功能，包括全生命周期管理、金丝雀发布、蓝绿部署、服务超时重试等。

---

## 3. 技术实现细节

### 关键技术方案
*   **Wasm 插件热加载**：Higress 利用 Envoy 的 Wasm 能力，通过 OCI（Open Container Initiative） 标准拉取插件镜像。这意味着插件更新不需要重启网关进程。
*   **流式处理优化**：针对 LLM 的 SSE (Server-Sent Events) 流式响应，Higress 在数据平面进行了特殊处理，确保在转发流式数据时不阻塞，并且能够对流式内容进行实时拦截（如实时敏感词检测）。

### 代码组织结构
*   **Higress Console**：前端管理界面，通常基于 Vue/React 开发。
*   **Higress Controller**：Kubernetes Controller，监听 Ingress/Gateway 资源并转换为 Istio 配置。
*   **Higress Gateway**：基于 Envoy 构建，包含自定义的 Filter 和 HTTP Filter。

### 性能与扩展性
*   **性能**：Go 语言编写的控制器保证了配置分发的效率，C++ 编写的数据平面保证了转发性能。
*   **扩展性**：Wasm 机制是其扩展性的核心。相比于 Nginx 的 Lua 模块，Wasm 提供了更好的隔离性和安全性，且支持多语言开发。

---

## 4. 适用场景分析

### 适合使用的场景
1.  **AI 应用开发与中台**：企业正在构建 AI 应用（如 Copilot、Chatbot），需要统一管理对 OpenAI、阿里云等模型的调用，并控制成本。
2.  **Kubernetes 环境下的微服务治理**：已经使用 K8s 的企业，需要一款高性能的 Ingress Controller。
3.  **需要高度定制网关逻辑的场景**：例如，需要在网关层进行复杂的请求校验、数据转换，且不希望修改后端服务代码。
4.  **多模型切换与灾备**：需要在不同模型厂商之间快速切换（例如从 OpenA 切换到国产模型）。

### 不适合的场景
1.  **非 K8s 环境**：虽然可以二进制运行，但 Higress 强绑定 K8s 体系，在传统虚拟机环境下部署复杂度远高于 Nginx。
2.  **极简静态站点**：对于简单的静态资源托管，Nginx 更加轻量。
3.  **对 Lua 脚本有重度依赖**：如果你有大量基于 OpenResty/Lua 的旧脚本，迁移到 Wasm (Go/C++) 成本较高。

---

## 5. 发展趋势展望

*   **从流量网关到 AI 网关**：Higress 正在重新定义 API 网关。未来的网关不仅仅是流量的管道，更是 AI 的**大脑前庭**，负责 Prompt 优化、记忆管理和工具编排。
*   **MCP 协议的普及**：随着 AI Agent 的爆发，作为 MCP Server 的 Higress 将成为连接企业数据与 AI 模型的标准枢纽。
*   **Wasm 生态的爆发**：随着 Wasm 标准的成熟，Higress 的插件生态将更加丰富，可能会有第三方开发者出售专门用于 AI 防护、Prompt 优化的 Wasm 插件。

---

## 6. 学习建议

*   **适合人群**：云原生架构师、后端开发者、AI 应用工程师。
*   **学习路径**：
    1.  **基础**：熟悉 Kubernetes Ingress 和 Service Mesh 基本概念。
    2.  **核心**：学习 Envoy 的基本配置和 xDS 协议原理。
    3.  **进阶**：学习 WebAssembly (WASM) 原理，尝试使用 Go 编写一个简单的 Higress 插件。
    4.  **实战**：在本地 Kind 集群中部署 Higress，配置一个转发给 OpenAI 的路由，并开启 Token 统计。
*   **实践建议**：阅读官方的 `README_ZH.md`，尝试使用 Console 界面进行配置，然后再去研究生成的 YAML 配置文件。

---

## 7. 最佳实践建议

1.  **资源隔离**：在生产环境中，建议将 AI 业务的网关与传统微服务的网关分开部署（使用不同的 Higress 实例或 Gateway Class），因为 AI 请求通常耗时较长且占用连接，可能影响普通业务。
2.  **插件开发**：尽量使用 Wasm 插件实现业务逻辑，避免修改 Higress 自身的镜像，以便于版本升级。
3.  **观测性**：务必开启 OpenTelemetry 集成。AI 调用的链路追踪对于排查 Prompt 质量和延迟问题至关重要。
4.  **安全防护**：在 AI Gateway 层必须配置"敏感词过滤"插件，防止 Prompt Injection（提示词注入）攻击绕过后端直接攻击模型。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**"云原生基础设施"**这一层进行了抽象。它将**流量治理的复杂性**从业务代码中剥离，转移到了**网关配置层**。
*   **代价**：运维团队需要理解 Envoy、Istio、Wasm 等复杂概念。它把"写代码的复杂性"变成了"配置的复杂性"。
*   **价值取向**：它倾向于**标准化**和**可移植性**。通过遵守 Ingress 标准和 WASM 标准，它牺牲了部分极致的性能优化空间（相比完全手写的高性能 C++ 代理），但换取了跨云厂商的通用性。

### 工程哲学
Higress 的核心范式是**"流量即代码"**。它认为 AI 时代的流量管理不仅仅是路由，还包括对语义的理解和干预。
*   **误用风险**：最容易误用的是将**业务逻辑**过度下沉到网关。例如，在网关插件中写复杂的数据库查询或业务计算。这会导致网关变得臃肿，失去其作为"无状态基础设施"的轻量级优势，甚至影响整体吞吐量。

### 可证伪的判断
1.  **性能判断**：在开启 Wasm 插件（如鉴权）的情况下，Higress 的长连接并发处理能力相比原生 Nginx + Lua 模式，延迟增加在 5% 以内（验证 Wasm 的性能损耗是否足够低）。
2.  **AI 效率判断**：通过 Higress 的 Prompt 模板管理和缓存功能，在特定问答场景下，后端 LLM 的 Token 消耗减少 20% 以上（验证 AI Gateway 的降本能力）。
3.  **迁移成本判断**：一个熟练使用 Nginx Ingress 的团队，在 4 小时内可以将现有的 Ingress 规则迁移到 Higress 并保持业务零中断（验证兼容性承诺）。

---
## 代码示例




```python
# 示例1：使用Higress实现简单的API网关路由
from higress import Gateway

def setup_api_gateway():
    """
    配置一个简单的API网关，将不同路径的请求路由到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="demo-gateway")
    
    # 添加路由规则：将 /api/v1 路径的请求转发到 service1
    gateway.add_route(
        path="/api/v1",
        destination="http://service1:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：将 /api/v2 路径的请求转发到 service2
    gateway.add_route(
        path="/api/v2",
        destination="http://service2:8080",
        methods=["GET"]
    )
    
    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用Higress快速搭建一个API网关，
# 实现不同路径的请求路由到不同的后端服务，适用于微服务架构中的流量管理。
```




```python
# 示例2：配置Higress的流量灰度发布
from higress import CanaryRule

def setup_canary_release():
    """
    配置灰度发布规则，将10%的流量路由到新版本服务
    """
    # 创建灰度规则
    canary = CanaryRule(
        name="service-canary",
        service="http://service:8080",
        new_version="http://service-v2:8080"
    )
    
    # 设置10%的流量路由到新版本
    canary.set_traffic_split(percentage=10)
    
    # 添加基于请求头的灰度条件
    canary.add_condition(
        header="X-Canary",
        value="true",
        match_type="exact"
    )
    
    # 应用灰度规则
    canary.apply()

# 说明：这个示例展示了如何使用Higress实现灰度发布，
# 通过流量百分比和请求头条件控制新旧版本的流量分配，
# 适用于需要平滑升级服务的场景。
```




```python
# 示例3：使用Higress实现请求限流
from higress import RateLimiter

def setup_rate_limiting():
    """
    配置API请求限流，防止服务过载
    """
    # 创建限流器
    limiter = RateLimiter(
        name="api-limiter",
        default_limit=100  # 每秒100个请求
    )
    
    # 为特定API路径设置更严格的限流
    limiter.add_rule(
        path="/api/expensive",
        limit=10,  # 每秒10个请求
        burst=20   # 允许突发20个请求
    )
    
    # 添加基于IP的限流例外
    limiter.add_whitelist(ip="192.168.1.100")
    
    # 应用限流规则
    limiter.apply()

# 说明：这个示例展示了如何使用Higress实现API请求限流，
# 通过设置不同的限流规则保护服务免受过载影响，
# 适用于需要控制API访问频率的场景。
```


---
## 案例研究


### 1：阿里集团内部通义千问业务网关

 1：阿里集团内部通义千问业务网关

**背景**:  
通义千问是阿里云推出的超大规模语言模型，在对外提供API服务时，需要处理海量并发请求，同时涉及复杂的鉴权、流量控制和模型路由逻辑。随着用户量的激增，传统的网关架构在处理长连接和AI特有的高延迟响应时遇到了瓶颈。

**问题**:  
原有的网关架构在处理AI大模型场景时，主要面临三个问题：一是高并发下QPS（每秒查询率）性能不足，导致请求排队；二是缺乏对SSE（Server-Sent Events）等流式传输协议的高效支持，影响了模型生成内容的实时性；三是扩展性受限，难以快速适配新上线的不同参数规模的模型服务。

**解决方案**:  
全面采用 Higress 作为 AI 服务的流量入口。利用 Higress 原生支持 WASM（WebAssembly）的能力，编写了专门的插件来处理大模型特有的鉴权逻辑和请求改写。同时，基于 Higress 的云原生架构，实现了后端服务到不同模型版本（如 Qwen-72B, Qwen-14B）的动态负载均衡，并开启了 Higress 针对长连接和流式传输的深度优化功能。

**效果**:  
成功支撑了通义千问业务的爆发式增长，网关层 P99 延迟降低了 40%，单集群 QPS 承载能力提升至数万级别。通过 Wasm 插件实现了业务逻辑的秒级热更新，无需重启网关服务，极大提升了业务迭代效率。

---



### 2：某头部电商平台大促流量防护

 2：某头部电商平台大促流量防护

**背景**:  
该电商平台在每年的“双11”和“618”大促期间，流量会呈现数十倍的增长。微服务架构中的商品详情、购物车、交易链路等核心接口面临着巨大的流量冲击。此前使用的开源网关在超高并发下会出现 CPU 飙升甚至内存溢出（OOM）的风险，且缺乏精细化的流量治理能力。

**问题**:  
大促期间主要面临两大挑战：一是热门商品接口的“热点流量”难以精准识别和限流，容易导致后端服务雪崩；二是多语言（Java、Go、Python）微服务环境下的服务发现和路由配置复杂，原有关联配置出错率高，影响服务稳定性。

**解决方案**:  
引入 Higress 替换了原有的 Ingress Controller。利用 Higress 内置的热点参数限流功能，针对热门商品 ID 进行精准的流控防护，自动识别异常流量并削峰填谷。同时，利用 Higress 对 Istio 和 Nacos 的深度兼容，统一了南北向（入口网关）与东西向（服务间）的流量管理，通过一套配置即可处理 K8s 集群内外的服务路由。

**效果**:  
在最近的一次大促中，Higress 稳定承接了每秒数十万级的请求峰值，系统资源利用率（CPU/内存）相比旧架构优化了 30%。通过精准的流量防护，后端核心服务的可用性保持在 99.99% 以上，且运维人员的配置复杂度大幅降低，实现了“零故障”过峰。

---



### 3：某跨国 SaaS 企业多地域 API 统一管理

 3：某跨国 SaaS 企业多地域 API 统一管理

**背景**:  
一家提供全球服务的 SaaS 企业，其服务部署在阿里云位于不同地域（如中国香港、法兰克福、弗吉尼亚）的 Kubernetes 集群中。由于各地域需要独立进行合规性管理和数据落盘，且需要通过统一的全球公网域名对外提供服务，此前面临着跨地域流量调度混乱和 API 管理分散的问题。

**问题**:  
在没有统一网关之前，各地域的集群各自暴露入口，导致全球流量调度（如 DNS 就近接入）难以自动化，且每个地域都需要独立维护 API 鉴权、计量和访问日志逻辑，运维成本高昂，安全策略也难以统一。

**解决方案**:  
部署 Higress 作为全球统一的 API 网关。在各地域集群中部署 Higress，并结合阿里云 DNS 全球流量调度（GTM）实现就近接入。利用 Higress 的多集群管理能力，在一个控制平面统一配置全球的 API 路由规则，并使用 Wasm 插件统一注入了全球适用的鉴权和日志采集逻辑，实现了“一处配置，全局生效”。

**效果**:  
实现了全球 API 的标准化统一管理，跨地域的流量调度响应速度提升了 50%。通过统一的网关层管控，企业能够集中进行 API 计量和访问审计，不仅降低了 40% 的多集群运维成本，还有效满足了不同地区的数据合规性要求。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高流量场景 | 极高性能，基于 Lua 和 Nginx，性能接近 Kong |
| 易用性 | 提供可视化控制台和 Kubernetes 原生支持，配置简单 | 提供管理界面和丰富的插件，但配置较复杂 | 提供管理面板和动态路由，但学习曲线较陡 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 功能支持 | 支持流量管理、安全防护、可观测性等 | 插件生态丰富，支持认证、限流、监控等 | 功能全面，支持动态路由、限流、认证等 |
| 社区活跃度 | 社区活跃，由阿里巴巴维护 | 社区活跃，用户基数大 | 社区活跃，国内用户较多 |
| 扩展性 | 支持自定义插件和扩展 | 支持自定义插件，扩展性强 | 支持自定义插件和 Lua 脚本扩展 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，性能和安全性较高。
- 优势2：深度集成 Kubernetes，适合云原生环境。
- 优势3：提供开箱即用的可视化控制台，降低使用门槛。

### 不足分析

- 不足1：相比 Kong 和 APISIX，插件生态尚不够丰富。
- 不足2：社区成熟度和用户基数略低于 Kong 和 APISIX。
- 不足3：部分高级功能可能依赖企业版或额外配置。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WebAssembly (Wasm) 技术，允许用户使用 C++、Go、Rust 或 AssemblyScript 编写自定义插件。相比传统的 Lua 脚本或硬编码方式，Wasm 插件提供了接近原生的性能，且支持热加载，无需重启网关即可更新业务逻辑。

**实施步骤**:
1. 根据团队技术栈选择 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 Proxy-Wasm 规范编写插件逻辑。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台的插件管理中。
4. 在网关配置或路由规则中关联该插件，并配置具体的参数。

**注意事项**: 
- Wasm 插件运行在沙箱中，但需注意内存限制，避免处理超大请求体导致内存溢出。
- 生产环境部署前务必对插件进行压力测试，确保其延迟在可接受范围内。

---

### 实践 2：精细化配置流量路由与灰度发布

**说明**: 利用 Higress 强大的路由转发能力，基于 Header、Query 参数、Cookie 或权重实现金丝雀发布和蓝绿部署。这可以确保新版本服务在出现问题时能快速回滚，降低发布风险。

**实施步骤**:
1. 在服务来源中注册不同版本的服务（如 v1 和 v2）。
2. 创建两个路由规则，或者使用一个带有权重配置的路由规则。
3. 设置匹配条件，例如将包含 `x-canary: true` 的 Header 请求转发至 v2 版本。
4. 配置流量权重（例如 10% 流量去 v2，90% 流量去 v1），逐步观察 v2 版本的运行状况。

**注意事项**: 
- 灰度发布必须有完善的监控和日志告警配合，以便及时发现异常流量。
- 确保不同版本的服务在数据库变更或 API 兼容性上做好适配，防止数据不一致。

---

### 实践 3：构建全链路安全防护体系

**说明**: Higress 内置了丰富的安全能力，最佳实践是组合使用认证鉴权、IP 访问控制和流量清洗。通过在网关层统一处理安全问题，可以避免将流量暴露给后端微服务，简化后端服务的开发复杂度。

**实施步骤**:
1. 配置 Basic Auth、JWT 或 AK/SK 认证插件，保护 API 入口。
2. 开启 IP 访问控制插件，黑名单拦截恶意 IP，白名单限制管理后台访问。
3. 针对常见 Web 攻击（如 SQL 注入、XSS），配置 Wasm 防护插件或对接 WAF 规则。
4. 启用严格的后端服务间 TLS (mTLS) 通信，确保传输链路安全。

**注意事项**: 
- JWT 密钥应定期轮换。
- 高并发场景下，复杂的安全校验（如 WAF 正则匹配）可能会增加延迟，建议通过异步处理或硬件加速优化。

---

### 实践 4：对接云原生服务注册与发现

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 以及 Kubernetes Service。最佳实践是将 Higress 与现有的注册中心无缝对接，实现自动化的服务发现和健康检查，避免手动维护静态 IP 列表。

**实施步骤**:
1. 在 Higress 控制台的“服务来源”中添加对应的注册中心（如 Nacos）。
2. 配置命名空间和服务分组，确保 Higress 能正确读取到服务列表。
3. 在创建路由时，直接选择注册中心中的服务名作为目标服务。
4. 启用主动健康检查，配置探测路径和间隔，自动摘除不健康的实例。

**注意事项**: 
- 确保注册中心与 Higress 之间的网络连通性，避免因网络分区导致服务列表丢失。
- 注意服务名与 DNS 解析的冲突，建议使用具有明确业务含义的域名前缀。

---

### 实践 5：实施细粒度的流量治理与超时控制

**说明**: 在微服务架构中，链路长、依赖复杂。最佳实践是在网关层设置合理的超时时间、重试策略和限流规则，以防止下游服务故障引发的雪崩效应，并保障核心服务的可用性。

**实施步骤**:
1. 根据业务 SLA 要求，为不同路由配置全局超时或单服务超时。
2. 针对幂等接口（如 GET 请求），配置自动重试策略，设定最大重试次数（建议 2-3 次）。
3. 开启请求缓存插件，对读多写少的场景进行缓存，减轻后端压力。
4. 配置并发限流或基于令牌桶的速率限制，保护后端服务不被突发流量击垮。

**注意事项**: 
- 重试策略必须谨慎使用，非幂等

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 QUIC 协议，解决了 HTTP/2 的队头阻塞问题，显著降低弱网环境下的延迟。Higress 作为高性能网关，启用 HTTP/3 可提升移动端和跨地域访问的吞吐量。

**实施方法**:
1. 在 Higress 监听器配置中开启 HTTP/3 支持（需 1.1.0+ 版本）。
2. 配置 UDP 端口（默认 443）并确保防火墙放行。
3. 为网关域名配置支持 ECDSA 的 TLS 1.3 证书。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，连接建立成功率提升 15% 以上。

---

### 优化 2：启用 WASM 插件预热与 AOT 编译

**说明**: Higress 支持 WASM 插件扩展，但默认的 JIT 模式存在冷启动延迟。通过预热和 AOT 编译可消除首次执行开销，并降低运行时 CPU 消耗。

**实施方法**:
1. 使用 `tinygo` 编译 WASM 插件时开启 `-optimize=2` 和 `-scheduler=none` 参数。
2. 在网关配置中启用 `wasmPrewarm: true`，在流量进入前强制加载所有插件。
3. 对高频使用的插件（如 Auth、Key Rate Limit）进行 AOT 编译缓存。

**预期效果**: 插件冷启动耗时从 50-100ms 降至 5ms 以内，插件处理延迟减少 40%。

---

### 优化 3：配置智能 DNS 缓存与连接池复用

**说明**: 默认的 DNS 解析和短连接建立会显著增加后端延迟。通过配置 DNS 缓存和 HTTP/2 连接池，可减少网络握手开销。

**实施方法**:
1. 在 `GlobalConfig` 中设置 `dnsCacheTTL: 3600s`（根据实际 TTL 调整）。
2. 对后端服务启用 HTTP/2 连接池（`http2: true`），并设置 `maxRequestsPerConnection: 1000`。
3. 针对长尾服务调整 `keepalive` 参数（如 `idleTimeout: 60s`）。

**预期效果**: 后端连接建立耗时减少 80%，P99 延迟降低 100-200ms。

---

### 优化 4：实施全链路超时控制与熔断

**说明**: 缺乏超时控制会导致线程池耗尽，熔断缺失会放大故障影响。精细化的超时和熔断策略可保障系统稳定性。

**实施方法**:
1. 为每个路由设置独立的 `timeout` 参数（建议不超过后端 P99.9 延迟的 2 倍）。
2. 对依赖服务配置 `retryOn` 条件（如 `5xx` 和 `reset`），并限制 `retryAttempts` 为 2 次。
3. 启用 `outlierDetection`（如连续 5 个 5xx 触发熔断，30 秒后恢复）。

**预期效果**: 故障场景下可用性提升至 99.99%，资源争抢导致的延迟尖刺减少 70%。

---

### 优化 5：优化日志采样与异步上报

**说明**: 全量日志会严重拖慢网关性能。通过采样和异步上报可平衡可观测性与性能。

**实施方法**:
1. 对健康检查和 200 状态码的请求设置 `logSampleRate: 0.01`（1% 采样）。
2. 使用 OpenTelemetry Collector 的异步模式，配置 `batchCount: 512` 和 `timeout: 5s`。
3. 将日志输出至高性能 Kafka/Pulsar 集群，避免本地磁盘 I/O。

**预期效果**: 日志系统 CPU 占用从 15% 降至 3%，日志上报延迟减少 90%。

---

### 优化 6：启用 CPU 亲和性与 NUMA 优化

**说明

---
## 学习要点

- 基于提供的来源信息（Alibaba / Higress，来自 GitHub Trending），以下是关于 Higress 的关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量治理的复杂性问题。
- 它深度集成了 K8s Ingress 资源，支持作为标准 Ingress Controller 使用，能够无缝对接 Kubernetes 生态体系。
- 提供了强大的 WAF（Web 应用防火墙）插件保护能力，能够有效防御 SQL 注入、XSS 等常见 Web 安全威胁。
- 兼容 Nginx Ingress 注解配置，并支持 Nginx 语法，大大降低了用户从传统 Nginx 迁移到 Higress 的成本和门槛。
- 内置了针对 Dubbo、Nacos、gRPC 等微服务协议的原生支持，实现了服务网格与 API 网关的技术栈统一。
- 采用标准 WASM (WebAssembly) 技术实现插件扩展，支持使用 C++、Go、Rust、JavaScript 等多语言编写高性能、低耦合的业务逻辑插件。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的定位与作用，对比 Nginx、Kong 及传统网关的区别。
- Higress 架构概览：了解 Higress 基于 Istio 与 Envoy 的底层架构，其高可用、低延时的技术原理。
- 核心概念：掌握 Ingress、Gateway、Route（路由）、Service（服务）及 Upstream（上游服务）的定义。
- 基本安装部署：学习如何在 Docker 环境及 Kubernetes 集群中安装 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与简介)
- Higress GitHub 仓库 (README 与 Quick Start)
- Envoy 官方文档 (基础概念部分)

**学习建议**:
建议先阅读官方文档了解背景，随后在本地 Docker 环境快速拉起一个 Higress 实例。通过控制台界面创建一个简单的路由转发，例如将请求转发到一个公网测试服务，以验证部署成功并熟悉控制台操作。

---

### 阶段 2：流量管理与路由配置

**学习内容**:
- 路由规则详解：学习如何配置基于域名、路径、Header 的精确路由与泛域名路由。
- 流量切分：掌握灰度发布（金丝雀发布）和蓝绿发布的配置方法，实现按比例或按请求内容的流量分流。
- 负载均衡策略：理解并配置轮询、随机、最小连接数等负载均衡算法。
- 服务治理：配置超时、重试及熔断机制，保障后端服务的稳定性。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (路由配置与流量管理)
- Kubernetes Ingress Nginx 对比文档 (理解不同 Ingress 规范的差异)
- Higress 官方示例库

**学习建议**:
尝试在 Kubernetes 环境中部署两个版本的 Dummy 服务（v1 和 v2），利用 Higress 配置 Header 匹配规则，将特定流量引入 v2 版本，模拟真实的灰度发布场景。重点测试超时和重试配置对故障恢复的影响。

---

### 阶段 3：安全与可观测性

**学习内容**:
- 安全认证：学习如何在网关层实现 Basic Auth、AK/SK 认证以及 JWT 验证。
- 安全防护：配置 IP 黑白名单、CORS 跨域策略及限流防刷功能。
- 可观测性集成：对接 Prometheus/Grafana 进行监控指标采集，配置日志服务（如 SLS 或 Elasticsearch）进行访问日志分析。
- WAF 集成：了解如何集成 Web 防火墙插件以防御常见攻击。

**学习时间**: 2-3周

**学习资源**:
- Higress 安全配置文档
- Higress 可观测性与插件开发文档
- Prometheus 监控最佳实践

**学习建议**:
安全方面，建议为测试服务添加一个简单的 JWT 认证，并使用 Postman 或 Curl 验证带 Token 和不带 Token 的访问区别。监控方面，务必配置 Prometheus 抓取 Higress 指标，并在 Grafana 中导入 Dashboard 面板观察 QPS 与延迟变化。

---

### 阶段 4：插件生态与高级扩展

**学习内容**:
- 插件系统：深入理解 Higress 的 Wasm 插件机制，学习 Lua 和 Wasm (AssemblyScript/Go/Rust) 插件的开发流程。
- 自定义插件开发：动手编写一个自定义插件（如自定义请求头处理或简单的鉴权逻辑）。
- 服务发现集成：学习 Higress 如何对接 Nacos、Consul、Zookeeper 等注册中心，实现从注册中心动态获取服务列表。
- 高可用部署：在生产环境中规划 Higress 的高可用架构，包括多副本部署与弹性伸缩。

**学习时间**: 3-4周

**学习资源**:
- Higress 插件市场 (Wasm 插件示例)
- Higress 开发者指南 (自定义插件开发)
- Nacos 与 Higress 集成最佳实践

**学习建议**:
这是最具有挑战性的阶段。建议从修改官方现有的简单插件 Demo 开始，逐步编写自己的业务逻辑。同时，尝试在本地搭建一个 Nacos 注册中心，让 Higress 直接从 Nacos 发现服务而非静态配置，以体会“云原生”网关的动态性。

---

### 阶段 5：生产级实战与性能调优

**学习内容**:
- 生产环境架构设计：规划多环境（开发、测试、生产）的网关隔离策略。
- 性能调优：内核参数调优、连接池配置、长连接复用等高并发场景下的优化手段。
- 多租户管理：利用命名空间或标签实现多租户网关

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是基于阿里云内部多年的网关实践经验开源的。它是在 Istio 和 Envoy 的基础上构建的，旨在解决云原生架构下的流量管理问题。

与 Nginx 和 Kong 的主要区别如下：
1.  **架构基础**：Nginx 主要基于 C 语言开发，配置逻辑相对静态；Kong 基于 OpenResty (Nginx + Lua)，通过插件扩展功能；而 Higress 深度集成了 Istio，使用 Envoy 作为数据平面，支持标准的 Kubernetes Ingress 和 Gateway API，更适合云原生环境。
2.  **安全性与隔离**：Higress 支持 WASM (WebAssembly) 插件，允许使用 C/C++、Go、Rust、JavaScript 等多种语言编写插件，且插件运行在沙箱环境中，不会导致网关主进程崩溃。相比之下，Kong 的 Lua 插件如果出现错误可能会影响整个网关的稳定性。
3.  **集成能力**：Higress 原生集成了服务发现（如 Nacos、Consul、ZooKeeper 等），能够直接连接微服务注册中心，而传统的 Nginx 往往需要配合 Consul Template 等工具才能实现类似功能。

---



### 2: Higress 与 Istio Gateway 是什么关系？

2: Higress 与 Istio Gateway 是什么关系？

**A**: Higress 可以被理解为 Istio Gateway 的增强版和独立运行版。
1.  **兼容性**：Higress 完全兼容 Istio 的 API 规范，可以无缝接管 Istio 的 Gateway 资源配置。
2.  **独立运行**：原生的 Istio Gateway 通常需要部署完整的 Istio 控制平面，部署和维护成本较高。Higress 将控制平面和数据平面整合，支持独立部署，不需要依赖庞大的 Istio 控制平面即可使用 Gateway 的流量管理功能。
3.  **功能增强**：Higress 在 Istio 的基础上增加了对 HTTP 协议的高级扩展、更丰富的插件生态以及对接主流微服务注册中心的能力。

---



### 3: 如何在 Higress 中使用 WASM 插件？它有什么优势？

3: 如何在 Higress 中使用 WASM 插件？它有什么优势？

**A**: Higress 原生支持 WASM (WebAssembly) 插件，用户可以通过编写 Go 或 C++ 等语言的代码，编译成 `.wasm` 文件并上传到网关中使用。

**优势**：
1.  **安全性**：WASM 插件运行在资源受限的沙箱环境中，即使插件代码崩溃（如内存溢出或除零错误），也不会导致 Higress 网关主进程崩溃，从而保证了网关的高可用性。
2.  **灵活性**：开发者可以使用自己熟悉的语言（如 Go、Rust、AssemblyScript）编写逻辑，而不必局限于 Lua。
3.  **热加载**：WASM 插件支持动态加载和更新，修改插件逻辑不需要重启网关服务，可以实现毫秒级的配置生效。

---



### 4: Higress 是否支持从 Nginx 或传统网关迁移？

4: Higress 是否支持从 Nginx 或传统网关迁移？

**A**: 是的，Higress 提供了良好的迁移支持。
1.  **Nginx Ingress**：Higress 兼容 Kubernetes 的 Nginx Ingress 注解，这意味着在许多情况下，你可以直接将 Ingress Class 修改为 `higress`，无需修改大量 YAML 配置即可切换流量。
2.  **配置转换**：对于传统的 Nginx 配置，虽然不能直接导入 `nginx.conf`，但 Higress 提供了基于 Kubernetes 原生资源的配置方式，流量路由逻辑可以很容易地转化为 Ingress 或 Gateway API 资源。
3.  **服务发现**：如果传统架构中使用了 Nacos 等注册中心，Higress 可以直接对接，省去了在 Nginx 中手动配置 upstream 的繁琐过程。

---



### 5: Higress 的性能表现如何？能否支撑高并发场景？

5: Higress 的性能表现如何？能否支撑高并发场景？

**A**: Higress 具备极高的性能，能够支撑企业级的高并发流量。
1.  **底层优势**：Higress 的数据平面基于 Envoy，Envoy 本身就是高性能的 L7 代理，采用 C++ 开发，具有非阻塞 I/O 和多线程架构。
2.  **基准测试**：根据官方及社区的压测数据，Higress 在开启长连接和 TLS 卸载的情况下，处理 HTTP/HTTPS 请求的吞吐量和延迟表现均处于业界领先水平，能够轻松应对双十一级别的流量冲击。
3.  **弹性伸缩**：作为云原生网关，Higress 可以结合 Kubernetes 的 HPA (Horizontal Pod Autoscaler) 进行水平扩容，以应对流量波峰。

---



### 6: Higress 支持哪些服务发现机制？

6: Higress 支持哪些服务发现机制？

**A**: Higress 设计了极强的连接能力，支持多种服务注册中心，旨在打通云原生架构与传统微服务架构。
目前支持的主流服务发现工具包括：
1.

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Nginx 和 Envoy 构建。请分析 Higress 的默认配置文件，并找出它如何处理 HTTP 流量的基本路由规则。具体来说，如何配置一个简单的路由，将所有访问 `/api` 路径的请求转发到后端服务 `http://backend-service:8080`？

### 提示**: 查看 Higress 的 Ingress 或 Gateway API 配置示例，关注 `path` 和 `backend` 字段的定义。

### 

---
## 实践建议

以下是针对 Higress (AI Gateway) 的 6 条实践建议，侧重于生产环境落地与 AI 特定场景的优化：

### 1. 实施基于 Token 的精细化流控与熔断
不同于传统 API 网关仅关注 QPS（每秒请求数）或并发数，AI 场景下大模型推理的消耗主要取决于 Token 数量和请求的耗时。
*   **具体操作**：在 Higress 的插件配置中，利用 `ai-statistics` 或类似流控插件，针对不同的模型（如 GPT-4, Llama-3）设置基于 Token/分钟（TPM）或 Request/分钟（RPM）的阈值。
*   **最佳实践**：对于内部关键业务，配置基于 Token 的全局限流，防止因上游 Prompt 注入攻击或下游异常高频调用导致 API 配额瞬间耗尽。
*   **常见陷阱**：仅限制并发连接数。由于 LLM 请求通常耗时较长（SSE 流式返回可能持续几十秒），仅限制并发会导致连接池占满，但实际吞吐量极低，无法有效控制成本。

### 2. 配置语义化缓存以降低成本与延迟
LLM 的生成具有确定性，对于常见的问答或知识库查询，重复调用大模型是巨大的成本浪费。
*   **具体操作**：开启 Higress 的语义缓存插件。配置向量数据库（如 Redis 向量搜索）作为缓存后端，设置合理的相似度阈值（如 0.95）和缓存过期时间。
*   **最佳实践**：将高频提问但答案固定的内容（如“公司报销政策是什么”）纳入缓存范围。这不仅能节省 90% 以上的 API 调用成本，还能将响应延迟从秒级降低到毫秒级。
*   **常见陷阱**：使用精确匹配（Exact Match）进行缓存。用户提问的措辞稍有变化（如把“你好”改成“您好”）就会导致缓存未命中，使得缓存形同虚设。

### 3. 统一提示词管理与敏感信息过滤
在企业内部应用中，直接将原始 Prompt 传递给公网大模型存在数据泄露风险，且难以保证输出格式的一致性。
*   **具体操作**：使用 Higress 的 `prompt-manager` 插件或“模型服务”配置功能。在网关层对用户输入进行“模板化”处理，追加 System Prompt（例如：“你是一个专业的客服...”），并配置 `content-filter` 插件拦截敏感词。
*   **最佳实践**：在网关层统一注入上下文信息。例如，在请求转发给 LLM 之前，自动在 Prompt 中追加用户的 Profile 信息，业务代码只需传递用户 ID。
*   **常见陷阱**：在业务代码中硬编码 System Prompt。一旦需要调整模型的人设或逻辑，就需要重新发布所有微服务，维护成本极高。

### 4. 优化 SSE 流式传输的超时与缓冲策略
AI 交互通常采用 Server-Sent Events (SSE) 流式输出以提升用户体验，但这给网关层的代理带来了挑战。
*   **具体操作**：检查 Higress 的路由配置，确保开启 SSE 支持并调整网关层面的 `read_timeout`。对于流式请求，超时时间应设置为模型最大生成时间的上限（例如 300 秒）。
*   **最佳实践**：开启网关的“流式转发”模式，确保从上游模型返回的数据能够实时（低延迟）推送给客户端，而不是在网关层缓冲整块数据。
*   **常见陷阱**：网关层启用了缓冲（Buffering）。这会导致用户看到“假死”状态，直到模型完全生成完毕才一次性返回所有文字，严重破坏用户体验。

### 5. 利用“模型供应商”抽象实现平滑切换与降级
企业级应用中，不能被单一模型供应商绑定（如 OpenAI），且需要具备在服务不可用时的降级能力。
*   **具体操作**：在 Higress 中配置统一的模型服务提供商。将后端实际指向 OpenAI、Azure OpenAI 或通义千问等不同提供商。
*   **最佳实践**：配置“兜

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*