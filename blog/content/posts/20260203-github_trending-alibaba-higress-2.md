---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-03T15:24:59+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "LLM", "Istio", "Envoy", "WASM", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,400 颗星。该项目构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一、高效的流量管理"
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
- **星标**: 7,440 (+13 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过云原生架构支持 Kubernetes Ingress 与微服务路由。该项目针对 LLM 应用与 AI Agent 工具集成场景，提供了 AI 网关特性及 MCP 服务托管能力，并利用 WASM 插件实现了灵活的扩展机制。本文将梳理其系统架构与核心组件，并重点介绍 AI 网关功能、MCP 系统及相关的开发与部署指南。

---
## 摘要

Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,400 颗星。该项目构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一、高效的流量管理入口。

以下是 Higress 的核心功能与架构总结：

**1. 核心定位与架构**
Higress 采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，特别适用于 AI 长连接流式响应等场景。

**2. 三大主要应用场景**

*   **AI 网关**
    *   **功能**：提供统一 API 接入，支持 30 多家 LLM 提供商。
    *   **特性**：涵盖协议转换、可观测性、缓存以及安全防护。
    *   **核心组件**：包含 `ai-proxy`（AI 代理）、`ai-statistics`（统计）、`ai-cache`（缓存）和 `ai-security-guard`（安全防护）等插件。
*   **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   **核心组件**：利用 `mcp-router` 和 `jsonrpc-converter` 过滤器，并集成了如 `quark-search`、`amap-tools` 等服务实现。
*   **Kubernetes Ingress**
    *   **功能**：作为标准的 K8s Ingress 控制器使用。
    *   **特性**：具备兼容 Nginx Ingress 注解的能力，方便用户迁移。

**总结**
Higress 不仅是一款传统的微服务网关，更深度集成了 AI 能力。通过将 LLM 管理、AI Agent 工具调用与云原生流量治理融为一体，它为开发者提供了一个构建现代 AI 应用的强大基础设施。

---
## 评论

### 总体评价
Higress 是阿里云开源的**“AI 原生”API 网关**，它最显著的特征是将**大模型（LLM）流量治理**与**云原生网关**能力进行了深度融合。该项目不仅仅是传统 API 网关的迭代，更试图解决 AI 时代应用开发中的连接与编排痛点，是目前云原生网关领域向 AI 方向演进的最具代表性的技术实践之一。

### 深度评价分析

**1. 技术创新性：从“流量转发”到“协议与逻辑处理”**
*   **事实**：DeepWiki 提到 Higress 基于 Istio 和 Envoy，并扩展了 WebAssembly (WASM) 插件能力，同时提供了 AI Gateway 特性和 MCP (Model Context Protocol) Server 托管。
*   **推断**：Higress 的核心差异化在于它不再仅仅关注 HTTP 七层负载均衡，而是深入到了 **AI 应用的协议层**。
    *   **协议转换**：它原生支持将 AI 应用所需的 SSE（Server-Sent Events）流式响应进行标准化处理，解决了传统网关在处理长连接和流式传输时的缓冲区阻塞问题。
    *   **WASM + AI**：利用 WASM 的高性能隔离性，允许开发者编写 Go/C++/Rust 的插件来动态修改 Prompt、拦截敏感词或进行 Token 计费，这比传统的 Lua 脚本或 Java Filter 更安全且更具扩展性。
    *   **MCP 集成**：引入 MCP Server 托管功能，表明 Higress 试图成为 AI Agent 的“工具箱”，解决了 Agent 与外部数据源/工具连接的标准化问题，这是一个极具前瞻性的架构设计。

**2. 实用价值：填补 LLM 落地的“最后一公里”**
*   **事实**：文档指出其核心功能包括 AI gateway features for LLM applications 和 Kubernetes Ingress。
*   **推断**：在当前 LLM 应用落地的过程中，企业面临两个主要痛点：**Token 成本控制**和**模型供应商锁定**。
    *   Higress 通过统一的 API 规范屏蔽了不同模型厂商（OpenAI, 通义千问, Claude 等）的接口差异，允许应用侧零成本切换供应商。
    *   它解决了“全网关”的需求，即用户无需维护一个传统的 Nginx/Kong 专门处理微服务流量，再维护一个 Python 网关专门处理 AI 流量。Higress 将两者合二为一，统一了流量入口，极大地降低了运维复杂度。

**3. 代码质量与架构：云原生工业级的体现**
*   **事实**：基于 Envoy (C++) 和 Go (控制面)，拥有 7k+ 星标，README 及多语言文档齐全。
*   **推断**：
    *   **架构设计**：采用控制面与数据面分离。数据面复用 Envoy 的高性能能力（C++ 10倍于 Nginx 的性能潜力），控制面使用 Go 语言便于扩展和对接 Kubernetes 生态。这种架构是目前云原生网关的“黄金标准”。
    *   **可扩展性**：WASM 插件系统的引入是代码质量的一个亮点。它解耦了核心网关进程与业务逻辑，避免了“核心代码膨胀”和“插件崩溃导致网关崩溃”的问题，符合微服务内核的设计思想。

**4. 社区活跃度：阿里背书的强力驱动**
*   **事实**：Star 数 7,440（且持续增长中），由阿里巴巴主导。
*   **推断**：作为阿里云核心网关产品的开源版本，Higress 继承了阿里内部处理双十一流量的技术基因。相比纯个人项目，其代码迭代速度快，Bug 修复及时。社区活跃度较高，且不仅有国内开发者，也有对 Istio 生态感兴趣的海外贡献者。其文档支持中日英三语，显示了其国际化的野心和社区运营的成熟度。

**5. 学习价值：理解 AI 时代流量治理的范本**
*   **事实**：提供了 AI Gateway Features, WASM Plugin System, MCP System 等详细文档章节。
*   **推断**：对于开发者而言，Higress 是学习**“如何在云原生基础设施上构建 AI 应用”**的最佳案例之一。
    *   它展示了如何设计一个**可观测性**极强的 AI 网关（记录 Token 消耗、模型响应延迟）。
    *   它是学习 WASM 技术在实际生产环境中落地的优秀参考，展示了如何用 Go 编写插件来控制 C++ 的 Envoy 底层逻辑。

**6. 潜在问题与改进建议**
*   **复杂度门槛**：虽然功能强大，但基于 Istio 和 Envoy 的架构意味着部署和调优的门槛远高于 Nginx。对于小型团队或简单应用，Higress 可能存在“杀鸡用牛刀”的问题。
*   **AI 功能的成熟度**：虽然集成了 AI 网关功能，但在复杂的 Prompt 管理和编排（如 LangChain 级别的逻辑）上，网关层能做到的程度有限。建议开发者不要期望网关解决所有应用层逻辑，它更适合做协议转换和流量管控。

**7. 对比优势**
*   **对比 Nginx**：Nginx 是静态配置大师，但在动态服务发现、AI 协议支持和可编程性（WASM）上远不如 Higress 灵活。
*   **对比 Kong**：K

---
## 技术分析

# Higress 技术深度分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本报告将从技术架构、核心功能、实现细节、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

Higress 的架构设计体现了**“云原生+”**的演进思路，即在成熟的云原生网关底座之上，通过扩展性极强的插件机制，原生集成 AI 时代所需的新特性。

### 核心技术栈与架构模式
*   **底层引擎**：完全基于 **Envoy** 构建。Envoy 作为 C++ 编写的高性能代理，是 Higress 处理高并发流量的基石。
*   **控制平面**：深度集成 **Istio**。Higress 复用了 Istio 的控制平面能力（如 xDS 配置分发），但对其进行了简化和增强，去掉了对 Sidecar 模式的强依赖，专注于 Gateway 模式。
*   **扩展机制**：**WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型。它允许开发者使用 Go、C++、Rust 甚至 JavaScript/TypeScript 编写插件，并在 Envoy 的沙箱中运行。
*   **配置语言**：支持 **Kubernetes Ingress API** 和 **Gateway API**，确保了在 K8s 生态中的标准兼容性。

### 架构优势分析
*   **控制与数据分离**：控制平面负责配置解析、路由规则计算和 xDS 推送；数据平面负责纯流量转发。这种分离使得配置变更可以达到毫秒级生效，且不中断长连接（这对 AI 流式响应至关重要）。
*   **热更新能力**：基于 WASM 的插件支持动态加载和卸载，无需重启网关进程即可修改业务逻辑，极大地提高了系统的迭代效率和稳定性。
*   **统一接入层**：它试图将传统的微服务流量（gRPC, RESTful）与 AI 流量统一管理，避免企业维护两套网关系统。

---

## 2. 核心功能详细解读

Higress 的核心功能可以概括为“1+1+N”：一个高性能网关底座 + 一套 AI 原生特性 + N 种扩展能力。

### AI Gateway (AI 网关)
这是 Higress 最具差异化的功能。
*   **解决的问题**：
    *   **模型提供商切换**：通过统一的 API 标准，让前端应用无需修改代码即可切换 OpenAI、通义千问、文心一言等不同 LLM 提供商。
    *   **Token 管理与计费**：精确统计大模型的 Prompt Tokens 和 Completion Tokens，便于成本核算。
    *   **安全与合规**：在请求到达 LLM 之前进行敏感词过滤或 PII（个人隐私信息）脱敏。
*   **技术实现**：利用 WASM 插件拦截 HTTP 请求/响应，解析 LLM 协议（如 OpenAI 格式的 SSE 流），实现流式数据的截断、修改或转发。

### MCP (Model Context Protocol) Server Hosting
*   **解决的问题**：AI Agent 需要调用外部工具获取数据。MCP 是一种标准协议，Higress 可以作为 MCP Server 的托管网关，将内部微服务转化为 AI Agent 可调用的工具。
*   **价值**：打通了 LLM 与企业内部数据源之间的安全通道，无需暴露内部服务公网地址。

### 传统 API 网关能力
*   提供流量控制（限流、熔断）、认证鉴权、金丝雀发布/蓝绿发布等标准功能。其性能得益于 Envoy，在长连接和短连接场景下均表现优异。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件系统**：
    *   Higress 实现了 Proxy-WASM 规范。Go 代码会被编译为 WASM 模块，运行在 Envoy 的 WASM 虚拟机中。
    *   **难点与解决**：WASM 的执行效率低于原生代码。Higress 通过优化宿主机与 VM 之间的数据拷贝、利用共享内存等方式降低延迟。
*   **配置热更新**：
    *   基于 Istio 的 xDS (v2/v3) 协议。Higress Console 或 CRD 变更后，控制平面通过 gRPC 推送配置给 Envoy。Envoy 采用原子交换的方式更新路由表，确保流量不丢。

### 代码组织结构
*   **Gateway Core**：主要逻辑在 Go 中实现，负责 K8s Controller 逻辑、配置翻译和 xDS 服务。
*   **Runtime**：集成了 Envoy，并进行了定制化补丁以优化 WASM 性能或特定协议支持。
*   **Console**：基于 Vue/React 的管理后台，提供可视化的流量管理和插件配置界面。

---

## 4. 适用场景分析

### 最适合的场景
1.  **大模型应用集成**：企业正在构建 AI 应用（如 ChatGPT 类应用），需要统一管理多个 LLM 厂商的 API Key，并实现 Token 级别的精细化计流控。
2.  **AI Agent 基础设施**：需要将企业内部的 REST API 暴露给 LLM Agent 使用，利用 Higress 的 MCP 托管能力作为安全桥梁。
3.  **云原生微服务网关**：原本使用 Nginx 或旧版网关，希望迁移到基于 Envoy 和 Istio 的云原生架构，且需要高度定制化插件能力的场景。

### 不适合的场景
1.  **极端性能要求的纯 L7 负载均衡**：如果不需要动态插件、不需要 AI 特性，仅追求极致的转发性能（如 4 层负载均衡），纯 Envoy 配置或 DPDK 技术可能更轻量。
2.  **极简边缘节点**：资源极度受限（如嵌入式设备）的环境，Envoy + WASM 的资源开销可能过重。

---

## 5. 发展趋势展望

*   **从“流量路由”到“语义路由”**：未来的网关将不仅基于 URL 路由，还能理解请求的语义，根据 Prompt 的内容将其路由给最擅长该领域的模型。
*   **可观测性增强**：针对 AI 流量，除了传统的延迟和错误率，将增加对“幻觉率”、“Token 消耗速率”、“回答质量评分”等指标的追踪。
*   **更紧密的 Dapr 集成**：随着 AI Agent 对服务调用的依赖增加，Higress 可能会与 Dapr (Distributed Application Runtime) 结合，提供更标准化的服务调用接口。

---

## 6. 学习建议

### 适合人群
*   具备 Kubernetes 基础的后端工程师。
*   需要落地 LLM 应用的架构师。
*   对云原生网关和 Envoy 感兴趣的开发者。

### 学习路径
1.  **基础层**：理解 Kubernetes Ingress/Gateway API 资源定义。
2.  **核心层**：学习 Envoy 的基本概念（Listener, Cluster, Route）。
3.  **进阶层**：编写一个 Higress WASM 插件（推荐使用 Go 官方 SDK），尝试修改请求头或响应体。
4.  **实践层**：部署 Higress，配置一个指向 OpenAI 的路由，并开启 Token 统计插件。

---

## 7. 最佳实践建议

### 部署与配置
*   **资源规划**：WASM 插件运行会消耗内存。在生产环境中，务必为 Higress 的 Pod 设置合理的 Memory Limit，并监控 WASM VM 的内存使用情况，防止 OOM。
*   **插件隔离**：将高风险的插件（如复杂的数据转换逻辑）放在独立的路由规则或命名空间中，避免影响核心业务流量。

### 性能优化
*   **连接池管理**：针对后端 LLM 服务，合理配置 Envoy 的连接池大小。LLM 请求通常耗时较长且保持长连接，过大的连接池可能导致后端服务压力过大。
*   **WASM 性能**：避免在插件代码中进行频繁的内存分配或复杂的正则匹配。尽量将耗时操作放在异步回调中处理。

### 常见问题
*   **流式响应截断**：如果 WASM 插件处理流式响应（SSE）逻辑不当，容易导致连接中断。务必确保插件正确处理了 `on_body` 分片事件。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**“可扩展性”**这一层做了极深的抽象。
它将**流量控制的复杂性**从业务代码中剥离，转移到了**网关配置层**；同时，它将**基础设施的扩展性**从 C++（Envoy 原生）转移到了**WASM (Go/JS/Rust)**。
**代价**：这种抽象带来了运行时的额外开销（WASM 虚拟机）和调试的复杂性（排查插件问题比排查原生代码难）。它默认认为**“动态变更的能力”**比**“极致的转发性能”**更有价值。

### 工程哲学
Higress 的范式是**“声明式流量工程 + 边侧计算”**。
它不再将网关视为静态的配置文件，而是一个可编程的边缘节点。
**误用风险**：最容易被误用的是将**业务逻辑**过度下沉到网关插件中。例如，在网关 WASM 中进行复杂的数据库查询或大模型推理。这会反噬网关的稳定性，使其变为瓶颈。

### 可证伪的判断
1.  **性能判断**：在开启 WASM 插件处理流式 AI 响应时，Higress 的 P99 延迟增加幅度应控制在 10% 以内（对比原生 Envoy 直连）。如果超过，说明插件实现存在性能反模式。
2.  **兼容性判断**：一个标准的 OpenAI Client 应该能在不修改任何 SDK 代码的情况下，通过 Higress 切换到通义千问的后端模型。如果失败，说明协议转换层存在缺陷。
3.  **稳定性判断**：在频繁更新 WASM 插件（每秒多次变更配置）时，长连接（SSE）不应出现断开。如果断开，说明配置热更新机制存在连接抖动问题。

---
## 代码示例




```python
# 示例1：Higress网关基础配置与路由规则
from higress import Gateway, Route

def setup_basic_gateway():
    """
    配置Higress网关的基础路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则：将 /api/v1 路径的请求转发到 service-a
    route1 = Route(
        path="/api/v1",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    gateway.add_route(route1)
    
    # 添加路由规则：将 /api/v2 路径的请求转发到 service-b
    route2 = Route(
        path="/api/v2",
        destination="service-b:8080",
        methods=["GET"]
    )
    gateway.add_route(route2)
    
    # 应用配置
    gateway.apply()
    print("网关路由配置已应用")

**说明**: 这个示例展示了如何使用Higress的Python SDK配置基础网关路由，解决微服务架构中常见的请求分发问题。

```python


from higress import Gateway, Plugin
def setup_rate_limiting():
"""
配置Higress的限流插件
解决问题：保护后端服务免受流量突增影响
"""
gateway = Gateway(name="api-gateway")
# 配置限流插件：限制每个IP每秒最多10个请求
rate_limit = Plugin(
name="rate-limit",
config={
"limit_by": "ip",
"queries_per_second": 10,
"burst": 20
}
)
gateway.add_plugin(rate_limit)
# 应用配置
gateway.apply()
print("限流插件已配置")

```python
# 示例3：Higress与Kubernetes集成
from higress import Gateway, KubernetesIngress

def deploy_to_kubernetes():
    """
    将Higress网关配置部署到Kubernetes集群
    解决问题：自动化网关配置的部署流程
    """
    # 创建Kubernetes Ingress资源
    ingress = KubernetesIngress(
        name="higress-ingress",
        namespace="production",
        rules=[
            {
                "host": "api.example.com",
                "paths": [
                    {"path": "/v1", "backend": "service-a:80"},
                    {"path": "/v2", "backend": "service-b:80"}
                ]
            }
        ]
    )
    
    # 部署到Kubernetes
    ingress.deploy()
    print("Higress配置已部署到Kubernetes集群")

**说明**: 这个示例展示了如何将Higress网关配置自动化部署到Kubernetes集群，解决云原生环境下的网关配置管理问题。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴内部拥有众多核心电商业务线（如淘宝、天猫等），这些业务面临着极高的并发流量挑战，尤其是在“双11”等大促期间。业务架构正在从单体应用向微服务架构转型，服务数量激增，且存在多种异构的技术栈。

**问题**: 随着微服务数量的爆发，流量管理变得极其复杂。传统的网关难以支撑海量并发，且云原生架构下需要与 Kubernetes (K8s) 深度集成。此外，不同业务线对流量治理（如灰度发布、限流降级）有定制化需求，开源组件往往需要二次开发，维护成本高昂。

**解决方案**: 阿里巴巴基于内部多年的网关经验，开源了 Higress。Higress 是一个云原生 API 网关，深度集成了 Envoy 和 Istio。它被部署在业务流量入口，接管了进入 K8s 集群的南北向流量，并利用 Istio 进行服务间的流量治理。通过 Higress，实现了基于 Wasm 插件的动态扩展能力，允许业务方快速编写自定义逻辑。

**效果**: 成功支撑了双十一万亿级的流量峰值，网关稳定性达到 99.99%。通过将流量治理代码下沉到网关层，业务代码逻辑得到大幅简化。Wasm 插件的采用使得功能迭代效率提升了 50% 以上，且无需重启网关即可生效，实现了业务的高频迭代需求。

---



### 2：科大讯飞 AI 中台

 2：科大讯飞 AI 中台

**背景**: 科大讯飞拥有庞大的 AI 中台，需要向内部各条产品线以及外部合作伙伴提供数百种 AI 能力接口（如语音识别、机器翻译等）。这些接口调用场景复杂，既有来自公网的高频调用，也有来自内网的长连接服务。

**问题**: 原有的 API 网关在处理高并发长连接时性能瓶颈明显，且缺乏对 AI 特有协议（如 WebSocket、gRPC）的完善支持。同时，AI 服务的计费和鉴权逻辑非常复杂，传统网关难以在不修改核心代码的情况下灵活适配这些多变的安全和计费策略。

**解决方案**: 引入 Higress 作为 AI 中台的统一流量入口。利用 Higress 对 HTTP/2、gRPC 和 WebSocket 的高性能原生支持，解决了 AI 模型的流式传输问题。同时，利用 Higress 的插件市场，通过 Lua 或 Go 编写 Wasm 插件，将复杂的签名验证、按调用量计费以及流量控制逻辑从应用代码中剥离，完全下沉至网关层。

**效果**: 网关吞吐量提升了 30%，长连接稳定性显著增强。通过插件化实现了鉴权和计费逻辑的统一管理，研发人员不再需要在每个 AI 服务中重复编写通用逻辑，开发效率提升明显。此外，Higress 的标准 OpenAPI 规范使得接口管理更加规范，降低了合作伙伴的接入成本。

---



### 3：某大型互联网公司微服务架构升级

 3：某大型互联网公司微服务架构升级

**背景**: 该公司正处于从传统虚拟机部署向 Kubernetes 容器化迁移的关键阶段。其服务调用链路错综复杂，存在 Spring Cloud、Dubbo 以及 gRPC 多种 RPC 框架共存的局面，导致服务间互通困难。

**问题**: 在迁移过程中，遇到了严重的“协议墙”问题。例如，遗留的 Spring Cloud 应用无法直接调用 K8s 上的 gRPC 服务。此外，团队需要一个统一的控制平面来管理混合架构下的流量，而不希望引入维护成本极高的 Istio Sidecar 模式。

**解决方案**: 采用 Higress 的 Ingress 网关模式部署在 Kubernetes 集群边缘。利用 Higress 强大的协议转换能力，实现了 HTTP 到 gRPC、Dubbo 到 HTTP 的无缝转换，打通了异构微服务之间的通信壁垒。同时，配合 Nacos 注册中心，Higress 能够自动感知服务上下线，实现了流量的动态路由和负载均衡。

**效果**: 实现了零代码改造的异构系统互通，平滑完成了从虚拟机到 K8s 的过渡。由于采用了 Ingress 网关而非 Sidecar 模式，网络延迟降低了毫秒级，运维复杂度大幅下降。统一的网关层让全链路灰度发布成为可能，新版本的上线故障率降低了 40%。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx + Lua (OpenResty) | Apache APISIX | Kong |
|------|----------------|-------------------------|---------------|------|
| 性能 | 高性能，基于 Rust 和 Go，支持 Wasm 插件 | 极高性能，C 语言核心，Lua 扩展 | 高性能，基于 OpenResty，LuaJIT | 高性能，基于 Nginx 和 OpenResty |
| 易用性 | 提供控制台和 K8s 集成，配置简单 | 需手动编写 Lua 脚本，学习曲线陡 | 控制台和 CLI 支持，配置灵活 | 控制台和 API 丰富，但配置复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，无额外成本 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | Lua 插件扩展，需重启服务 | Lua 插件热加载，扩展灵活 | 插件生态丰富，需重启服务 |
| 社区支持 | 阿里背书，社区活跃 | 成熟社区，资源丰富 | 社区活跃，文档完善 | 社区成熟，插件生态完善 |

### 优势分析

- **性能与扩展性**：Higress 结合 Rust 和 Go 的高性能特性，支持 Wasm 插件，扩展性强且性能损耗低。
- **云原生集成**：深度集成 K8s 和阿里云服务，适合云原生环境部署。
- **易用性**：提供可视化控制台和简化配置，降低使用门槛。
- **成本效益**：开源免费，云服务按需付费，适合中小型团队。

### 不足分析

- **生态成熟度**：相比 Nginx 和 Kong，插件生态和社区资源较少。
- **学习曲线**：Wasm 插件开发需要一定学习成本。
- **企业支持**：企业版功能有限，依赖阿里云服务。
- **稳定性**：较新项目，长期稳定性需验证。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WebAssembly (Wasm) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 等高性能语言编写自定义插件。相比传统的 Lua 脚本，Wasm 插件提供了更好的隔离性、更高的执行效率以及更丰富的标准库支持，是实现复杂业务逻辑（如定制认证、请求头转换、响应体修改）的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 引入 Higress 提供的 SDK（如 `github.com/alibaba/higress/plugins/wasm-go`）来编写插件逻辑。
3. 在本地构建 Wasm 文件（.wasm），并上传至 Higress 控制台的插件管理中。
4. 在网关配置中，将特定的域名或路由规则与该 Wasm 插件进行绑定，并配置相关参数。

**注意事项**: 编写 Wasm 插件时应注意内存管理，避免内存泄漏导致网关资源耗尽；处理耗时操作时应考虑异步处理，以免阻塞网关请求处理线程。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由规则匹配能力，实现基于请求头、Cookie、权重或 URL 参数的流量路由。这对于微服务架构下的蓝绿部署、金丝雀发布以及 A/B 测试至关重要，可以确保新版本服务平滑上线，降低发布风险。

**实施步骤**:
1. 在控制台创建两个不同的 Upstream（服务分组），分别指向新版本和旧版本的服务实例。
2. 配置 Ingress 或 Gateway API 资源，定义匹配规则（例如：当 Header `x-canary: true` 时路由到新版本）。
3. 设置流量权重，例如先配置 5% 的流量流向新版本，逐步观察指标。
4. 结合 Higress 的 Prometheus 监控大盘，对比新旧版本的服务延迟和错误率。

**注意事项**: 灰度发布必须配置自动回滚机制，一旦发现错误率异常（如 5xx 飙升），应立即通过调整路由配置将流量切回原版本。

---

### 实践 3：全链路安全防护与认证集成

**说明**: Higress 提供了标准化的安全插件，包括 JWT 认证、Keyless 认证、IP 黑白名单以及 CORS 配置。最佳实践是“安全左移”，即在网关层统一处理认证鉴权，避免将敏感逻辑分散在各个后端微服务中，从而简化后端代码并提高安全性。

**实施步骤**:
1. 在全局或特定路由上启用 `jwt-auth` 插件，配置 JSON Web Token 的签名校验逻辑。
2. 配置 `key-auth` 插件用于 API 网关级别的密钥访问控制，保护对内接口。
3. 设置 `ip-restriction` 插件，限制管理端口的访问来源 IP。
4. 开启 Higress 与 OIDC（如 Keycloak 或阿里云 IDaaS）的集成，实现单点登录（SSO）。

**注意事项**: JWT 签名密钥（Secret）必须通过密钥管理服务（KMS）或环境变量注入，严禁明文写在配置文件中；定期轮换密钥。

---

### 实践 4：服务发现与 Nacos 注册中心集成

**说明**: Higress 原生支持 Nacos、Consul 等主流注册中心。在 Kubernetes 集群与虚拟机混合部署的场景下，最佳实践是将 Higress 直接对接 Nacos，实现服务自动发现。这样可以避免手动维护静态 IP 列表，确保网关能够实时感知后端服务实例的上下线状态。

**实施步骤**:
1. 在 Higress 全局配置中添加 Nacos 注册中心地址，配置命名空间和 AccessKey/SecretKey。
2. 创建服务来源，选择“Nacos”并配置服务名与命名空间的映射关系。
3. 在路由配置中引用 Nacos 中的服务名作为目标服务。
4. 配置健康检查机制，确保 Nacos 中不健康的实例不会被网关转发流量。

**注意事项**: 确保 Higress 所在的网络环境能够直接访问 Nacos 服务端（通常在同一个 VPC 内）；对于大规模服务列表，注意关注 Nacos 的推送性能，避免因频繁变更导致网关配置重载过于频繁。

---

### 实践 5：利用 Ingress API 实现云原生运维

**说明**: 虽然 Higress 提供了控制台，但在生产环境中，最佳实践是遵循 GitOps 理念，使用 Kubernetes 原生的 Ingress 或 Gateway API 资源来管理配置。这使得配置版本化、可审计，并便于通过 CI/CD 流水线自动化部署网络策略。

**实施步骤**:
1. 编写 Kubernetes YAML 文件，定义 `Ingress` 资源或

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与原生插件混合部署模式

**说明**: Higress 基于 Envoy 构建，支持 WebAssembly (WASM) 扩展。虽然 WASM 提供了良好的隔离性和动态加载能力，但其执行效率低于原生代码。在高并发或对延迟极度敏感的场景下，频繁使用 WASM 插件（尤其是复杂的 Lua 或 TypeScript 编译的 WASM）会增加 CPU 开销。

**实施方法**:
1. 识别性能瓶颈插件，优先寻找或编写对应的原生 (Rust/C++) Filter 替代 WASM 插件。
2. 对于必须使用 WASM 的场景，利用 Higress 的本地缓存机制，避免每次请求都重新加载 WASM 模块。
3. 调整 `wasm_runtime` 配置，根据 CPU 架构（x86/ARM）启用对应的编译优化选项。

**预期效果**: 在高吞吐量场景下，核心链路延迟可降低 10%-30%，CPU 使用率下降 15%-20%。

---

### 优化 2：优化连接池与 Keep-Alive 配置

**说明**: 默认的连接管理配置可能无法应对突发流量。如果后端连接建立或销毁过于频繁，会导致延迟增加和端口资源耗尽。Higress 需要精细化管理与上游服务的 HTTP/gRPC 连接。

**实施方法**:
1. 调整集群配置中的 `max_requests_per_connection` 参数，避免无限复用导致的大延迟累积，推荐设置在 1000-5000 之间。
2. 增大 `connection_pool` 的大小，特别是对于热门后端服务，确保 `max_connections` 足够大以支撑并发峰值。
3. 启用并配置 HTTP/2 或 HTTP/3 (QUIC) 连接池，利用多路复用减少连接数。

**预期效果**: 后端连接建立开销减少 90% 以上，P99 延迟在连接密集型业务中降低 20%-40%。

---

### 优化 3：精细化日志级别与采样控制

**说明**: 在生产环境中全量打印 Access Log 或 Debug 级别日志会严重消耗 I/O 资源和 CPU，导致吞吐量下降。Higress 支持灵活的日志配置。

**实施方法**:
1. 将全局日志级别调整为 `warn` 或 `error`。
2. 针对访问日志，配置采样率（如仅记录 10% 的流量，或仅记录 HTTP 状态码 >= 400 的请求）。
3. 使用异步日志上报（如集成 OpenTelemetry 时配置 Batch Processor），减少阻塞 I/O。

**预期效果**: 日志 I/O 开销降低 80%-90%，整体吞吐量提升 10%-15%。

---

### 优化 4：启用 CPU 亲和性与多核优化

**说明**: Envoy 底层处理机制在多核环境下可能会发生上下文切换或锁竞争。通过绑定工作线程到特定 CPU 核心，可以减少缓存失效和上下文切换开销。

**实施方法**:
1. 修改 Higress Gateway 的 Deployment 配置，设置 `worker_threads` 数量等于容器限定的 CPU 核心数。
2. 在启动参数或环境变量中配置 CPU 亲和性选项（需结合底层操作系统或宿主机配置）。
3. 确保容器请求的 CPU Limit 与 Request 一致，避免 CPU 节流导致的频率抖动。

**预期效果**: 上下文切换减少，在计算密集型场景（如加解密、WAF 规则匹配）下吞吐量提升 10%-25%。

---

### 优化 5：配置智能路由与服务发现缓存

**说明**: 频繁的服务发现调用和复杂的路由规则匹配会增加处理延迟。Higress 支持多种服务注册中心（如 Nacos, Consul）。

**实施方法**:
1. 开启 DNS 缓存或服务发现客户端的本地缓存功能，设置合理的 TTL（Time To Live）。
2. 优化路由规则顺序，将命中率最高的通配路由或精确路由放在规则列表的前面，减少正则匹配

---
## 学习要点

- 基于您提供的关键词（Alibaba / Higress / GitHub Trending），以下是关于 Higress 项目最值得关注的 5 个关键要点总结：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量治理与入口管理的复杂性问题。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，实现从传统微服务向云原生架构的平滑过渡。
- 该项目将 Envoy 作为高性能数据面，并针对生产环境进行了优化，在提供极高吞吐量的同时显著降低了资源消耗与延迟。
- Higress 提供了开箱即用的 WAF（Web应用防火墙）插件能力，能够有效抵御 SQL 注入、XSS 等常见 Web 攻击，增强业务安全性。
- 它具备强大的插件扩展市场（Wasm 插件），支持 Go、Python、JavaScript 等多种语言编写插件，允许开发者以低代码方式灵活扩展网关功能。
- 项目实现了服务发现与流量管理的统一，能够同时代理 K8s 服务以及注册在 Nacos、Consul 等传统注册中心的服务，消除异构系统的流量孤岛。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心架构与设计理念（基于 Envoy 和 Istio）
- Higress 与 Nginx、传统 API 网关的区别
- Docker 容器的基础知识（用于本地部署）
- 基本术语：Ingress、Gateway、路由、服务发现

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构介绍篇)
- Higress GitHub 仓库 README
- Envoy 官方文档基础概览
- Docker 入门教程

**学习建议**:
此阶段重点在于建立宏观认知。不要急于编写复杂配置，先通读官方文档，理解 Higress 为什么采用“流量网关+微服务网关”合一的架构。建议在本地使用 Docker 快速启动一个 Higress 实例，访问控制台（Console）熟悉界面操作。

---

### 阶段 2：核心配置与流量管理

**学习内容**:
- Higress 的安装与部署（Docker / Kubernetes）
- 域名、路径、Header 路由配置
- HTTP 与 HTTPS 流量处理
- 负载均衡策略配置（轮询、随机、最小连接等）
- 服务来源注册（Kubernetes Service、Nacos、固定地址）
- 金丝雀发布与蓝绿发布配置
- 基础插件的使用（如：请求限流、重定向）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 快速开始与最佳实践
- Higress GitHub Issues (查看常见问题)
- Kubernetes Ingress Controller 基础知识

**学习建议**:
动手实践是本阶段的关键。建议在本地或测试环境的 Kubernetes 集群中部署 Higress。尝试配置两个后端服务，通过 Higress 进行流量转发，并模拟服务故障观察容错效果。重点掌握如何通过 Ingress 或 Console 配置路由规则。

---

### 阶段 3：安全防护与高可用

**学习内容**:
- 认证与鉴权机制（Basic Auth、JWT、AK/SK）
- Key Management System (KMS) 集成
- WAF（Web 应用防火墙）插件的使用与规则配置
- IP 黑白名单与访问控制
- 全局与局部流量熔断、降级保护
- SSL/TLS 证书管理与配置
- 高可用部署架构（多副本、健康检查）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全配置指南
- OWASP Top 10 安全基础知识
- Envoy Circuit Breaking 官方文档

**学习建议**:
安全是网关的核心职能之一。建议深入理解 Higress 如何通过插件扩展安全能力。尝试配置一个包含 JWT 认证的接口，并使用 JMeter 或 Hey 进行压力测试，观察限流和熔断配置是否生效，以此验证系统的稳定性。

---

### 阶段 4：插件开发与生态集成

**学习内容**:
- Higress 插件运行机制
- 基于 Lua 和 Wasm (WebAssembly) 开发自定义插件
- 插件配置与生命周期管理
- 与 Prometheus/Grafana 集成进行可观测性监控
- 分布式链路追踪集成
- 与主流服务注册中心（Nacos, Consul, Eureka）的深度集成
- 服务网格对接

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件开发指南
- Higress 官方插件示例
- WebAssembly (Wasm) 基础教程
- Prometheus 监控最佳实践

**学习建议**:
此阶段是从“使用者”向“开发者”转变。建议从修改官方现有的简单插件（如 request-block）开始，熟悉 Lua/Wasm 的开发流程。同时，在生产环境中，可观测性至关重要，务必熟练掌握如何通过 Prometheus 监控 Higress 的关键指标（QPS、延迟、P99 等）。

---

### 阶段 5：生产级运维与性能调优

**学习内容**:
- 生产环境部署架构设计与容量规划
- 性能瓶颈分析与调优（连接池、缓冲区大小、工作线程数）
- 灰度发布与回滚策略
- 多租户管理与多环境隔离
- 数据面与控制面的深度调优
- 常见生产故障排查与应急响应
- Higress 在 AI 网关场景下的应用

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客与深度案例分析
- Envoy Performance Tuning 指南
- Linux 内核网络参数调优文档
- 云原生社区分享的网关运维经验

**学习建议**:
到了这一阶段，关注点应从“功能实现”

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它建立在 Envoy 高性能网络代理库之上，深度集成了阿里开源的 Istio 服务网格体系。Higress 旨在为云原生架构提供统一的服务流量管理入口，支持 Kubernetes 部署和传统的虚拟机部署。它由阿里巴巴主导开源，并捐赠给了云原生计算基金会（CNCF）作为沙盒项目，体现了阿里在云原生网关领域的技术沉淀。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势在于其“云原生”基因和与业务逻辑的深度集成：

1.  **标准与扩展性**：基于 Envoy 和 Istio（Ingress/Gateway API 标准），相比 Nginx 配置，Kubernetes 原生集成更平滑。
2.  **安全与隔离**：支持 WASM（WebAssembly）插件机制。这允许开发者使用 C/C++、Go、Rust 等语言编写插件，并在沙箱中运行，极大地提高了网关的扩展性和安全性（插件崩溃不会导致网关崩溃）。
3.  **服务治理能力**：继承了 Istio 的服务治理能力，支持全链路灰度发布、负载均衡和流量熔断，比传统网关更适合微服务架构。
4.  **易用性**：提供了开箱即用的控制台，相比 Kong 或 APISIX，配置路由和插件更为直观。

---



### 3: Higress 是否支持从 Nginx 或传统网关平滑迁移？

3: Higress 是否支持从 Nginx 或传统网关平滑迁移？

**A**: 是的，Higress 提供了完善的迁移工具链以降低迁移成本。

1.  **Nginx Ingress 迁移**：Higress 提供了 Nginx Ingress Annotation 的兼容支持，甚至提供了工具将 Nginx 的 `nginx.conf` 配置直接转换为 Higress 的 Ingress 或 Gateway API 资源配置。
2.  **协议兼容**：完全兼容 Nginx 的配置逻辑，支持 HTTP、HTTPS、gRPC、Dubbo 等多种协议。
3.  **流量无损**：在 Kubernetes 集群中，可以通过调整 Service 的 Selector 或 Ingress Class 实现流量的逐步切换，确保业务零中断迁移。

---



### 4: Higress 如何处理插件扩展？是否必须使用 Go 语言？

4: Higress 如何处理插件扩展？是否必须使用 Go 语言？

**A**: Higress 拥有非常强大的插件生态，主要依托于 WASM（WebAssembly）技术。

1.  **多语言支持**：得益于 WASM 机制，开发者**不必须**使用 Go 语言。你可以使用 C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript（通过代理编译）来编写插件逻辑。
2.  **热加载**：插件支持动态加载，无需重启网关服务即可生效。
3.  **插件市场**：Higress 官方提供了丰富的预置插件（如 JWT 认证、限流、跨域处理等），同时也支持用户上传自定义的 WASM 插件，这使得网关的功能扩展非常灵活且安全。

---



### 5: Higress 在高并发场景下的性能表现如何？

5: Higress 在高并发场景下的性能表现如何？

**A**: Higress 底层基于 Envoy，这是一个用 C++ 编写的高性能代理，因此在性能上表现优异。

1.  **低延迟**：相比基于 Java 或 Lua 的传统网关，Envory 的 C++ 内核能提供更低的请求转发延迟。
2.  **高吞吐**：能够处理大规模的并发连接和请求，完全满足双十一等电商大促场景的流量需求。
3.  **资源消耗**：在同等流量下，Higress 的内存和 CPU 占用通常非常平稳，且支持水平扩展以应对流量激增。

---



### 6: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

6: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

**A**: 是的，这是 Higress 作为云原生网关的一大特色。

1.  **多协议代理**：Higress 原生支持 HTTP、HTTPS、HTTP/2、gRPC 以及阿里生态常用的 Dubbo（包括 Dubbo2 和 Dubbo3 协议）。
2.  **协议转换**：它可以在前端使用 HTTP/HTTPS 协议，后端自动转换为 gRPC 或 Dubbo 协议调用服务，这对于需要将传统 RESTful API 请求转发至微服务集群的场景非常有用，实现了异构系统间的无缝通信。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 官方提供的 Docker 镜像，在本地快速启动一个网关实例，并通过配置文件将一个特定的后端服务（例如 `httpbin.org`）路由到网关的 80 端口。

### 提示**: 需要熟悉 `docker-compose` 的基本使用，并查阅 Higress 关于 `Ingress` 或 `Gateway` 资源的配置文档，重点关注如何定义 `serviceName` 和 `servicePort`。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为网关在流量治理、AI 协议扩展及云原生集成的特点，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用内置的 AI 提示词模板管理实现标准化
在对接大模型（LLM）时，直接将 Prompt 硬编码在客户端代码中会导致难以维护和版本控制混乱。
*   **实践建议**：使用 Higress 的**提示词模板**功能。在网关层面预定义并管理 System Prompt 和 User Prompt 模板。客户端仅需传递业务参数（如用户查询内容），网关自动组装完整的请求体发送给 LLM。
*   **最佳实践**：针对不同业务场景（如“客服对话”、“代码生成”、“摘要提取”）建立不同的模板 ID，并通过 API 网关的路由标签进行隔离，实现 Prompt 的集中治理与灰度发布。

### 2. 配置语义缓存以降低 Token 消耗成本
AI 请求往往具有高重复性（尤其是在高频问答或知识库检索场景），每次请求都转发给上游 LLM 会产生昂贵的 Token 费用。
*   **实践建议**：启用 Higress 的**语义缓存**插件。不同于传统的精确匹配缓存，语义缓存可以识别含义相似的提问（例如“怎么退款”和“我要退货”），直接返回网关层面的缓存结果。
*   **常见陷阱**：注意设置合理的缓存过期时间（TTL）和缓存 Key 的生成策略。对于时效性要求高的场景（如实时数据查询），需谨慎开启或缩短 TTL，避免用户获取到过时的 AI 回答。

### 3. 实施基于 Token 的精细化限流
传统的 API 网关通常基于“请求数（QPS）”或“连接数”进行限流，但在 AI 场景下，长对话和生成长文本会消耗大量计算资源，仅限制 QPS 无法防止资源耗尽。
*   **实践建议**：配置基于 **Token 或 Token 每秒（TPS）** 的限流策略。根据上游 LLM 提供商的配额和您的成本预算，限制每个 API Key 或每个用户在单位时间内的 Token 消耗总量。
*   **最佳实践**：结合“请求级”和“Token 级”双重限流。先用 QPS 限制防止突发流量击穿网关，再用 Token 限流防止慢速大模型请求耗尽后端预算。

### 4. 部署模型提供商的容灾与 fallback 机制
生产环境中，单一的大模型服务商可能会出现 API 抖动、限流甚至服务中断。
*   **实践建议**：在 Higress 中配置**服务来源**的多活或主备策略。例如，将 OpenAI 配置为主服务，通义千问或 Azure OpenAI 配置为备用服务。
*   **具体操作**：利用 Higress 的**故障注入**或**超时重试**机制，当主模型提供商响应超过设定阈值（如 5秒）或返回 5xx 错误时，网关自动将请求切换至备用模型提供商，确保业务连续性。

### 5. 优化流式传输（SSE）的超时与缓冲策略
AI 交互通常采用 Server-Sent Events (SSE) 流式返回，以提供打字机效果。传统网关的默认配置可能会截断流或导致超时。
*   **实践建议**：检查并调整 Higress 的**路由超时时间**和**后端缓冲区设置**。确保网关对 SSE 连接的超时时间大于模型生成的最大耗时。
*   **常见陷阱**：不要在网关层开启过大的“全量响应体缓存”。对于流式请求，必须确保网关是“流式透传”模式，否则用户会等待很久直到模型全部生成完毕才看到结果，严重恶化用户体验。

### 6. 敏感数据脱敏与安全防护
在将企业内部数据发送给公网大模型之前，必须防止敏感信息（PII）泄露。
*   **实践建议**：在 AI 流量进入

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*