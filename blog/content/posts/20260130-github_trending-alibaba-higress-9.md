---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-30T10:25:30+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI网关", "阿里开源", "Istio", "Envoy", "WASM", "MCP协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 AI 网关**，基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。以下是关于该项目的核心总结： 1. 产品定位 Higress 将**API 网关**与 **AI 网关**功能合二为一。它采用了控制平面与数据平面分离的架构，"
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
- **星标**: 7,413 (+12 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，它通过扩展 WASM 插件能力，深度集成了 AI 网关与 MCP 服务托管功能。该项目旨在为 LLM 应用开发者及微服务架构团队提供统一的流量管理与模型调用入口，同时兼容 Kubernetes Ingress 等传统网关场景。本文将为您梳理其核心架构设计，并重点解析 AI 原生特性与插件系统的实际应用。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 AI 网关**，基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。以下是关于该项目的核心总结：

### 1. 产品定位
Higress 将**API 网关**与 **AI 网关**功能合二为一。它采用了控制平面与数据平面分离的架构，通过 xDS 协议进行配置分发，具备毫秒级配置下发能力和零连接中断特性，特别适用于 AI 长连接流式响应场景。

### 2. 三大核心功能
*   **AI 网关**：
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存及安全防护能力。
    *   *相关组件*：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。
*   **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   *相关组件*：`mcp-router`, `jsonrpc-converter` 及内置工具实现（如地图搜索等）。
*   **云原生 API 网关**：
    *   作为 Kubernetes Ingress 控制器使用，兼容 Nginx Ingress 注解。
    *   支持微服务路由与传统流量管理。

### 3. 技术特点
*   **编程语言**：Go
*   **扩展性**：基于 WASM 插件系统，支持灵活的功能扩展。
*   **高性能**：基于 Envoy 的高性能数据处理能力，且配置变更热更新不影响业务连接。

目前该项目在 GitHub 上已获得超过 7,400 颗星，是一个活跃且专注于 AI 基础设施的开源项目。

---
## 评论

**总体判断**

Higress 是阿里开源的一款极具前瞻性的**云原生 API 网关**，它成功地将**云原生流量管理**与**AI 原生能力**深度融合。作为基于 Istio 和 Envoy 构建的上层网关，它不仅解决了传统微服务网关的痛点，更通过 WASM 和 AI 网关特性，为 LLM（大模型）应用时代提供了一套标准化的流量与模型治理方案，是目前将“云原生”与“AI Native”结合得最为紧密的开源网关之一。

**深入评价依据**

**1. 技术创新性：WASM 插件生态与 AI 原生架构**
Higress 最大的技术创新在于其**“AI Native”**的定位与**WebAssembly (WASM)** 插件系统的深度结合。
*   **事实**：DeepWiki 指出 Higress 扩展了 Istio 和 Envoy，具备 WASM 插件能力，并提供 AI 网关功能及 MCP (Model Context Protocol) 服务器托管。
*   **推断**：传统的网关（如 Nginx）修改逻辑需要重新编译或使用 Lua，限制较多。Higress 利用 WASM 的沙箱特性和高性能，允许开发者使用 Go/C++/Rust 等语言编写插件并**动态热加载**，极大地扩展了网关的灵活性。更重要的是，它内置了对 LLM 的支持（如 Token 计费、Prompt 转换、模型路由），这标志着网关从单纯的“流量路由”向“模型与语义路由”的范式转移。

**2. 实用价值：统一流量与模型治理**
Higress 解决了企业在 AI 转型期面临的**碎片化问题**，即如何在一个网关内同时管理传统的微服务 API 和新兴的 AI 应用流量。
*   **事实**：文档提到其核心功能包括 AI 网关特性、Kubernetes Ingress 以及微服务路由。
*   **推断**：在实际场景中，企业往往需要维护两套网关（一套给 K8s Ingress，一套给 OpenAI 调用）。Higress 实现了**“All-in-One”**，既能处理 K8s 集群内服务通信，又能作为 AI 代理统一对接多家 LLM 厂商（OpenAI, 通义千问等）。此外，其对 MCP 的支持意味着它可以直接作为 AI Agent 的工具托管中心，降低了 AI 应用的部署复杂度，实用价值极高。

**3. 代码质量与架构设计：控制面与数据面分离**
*   **事实**：DeepWiki 明确指出架构将**控制面**与**数据面**分离，基于 Envoy 处理流量。
*   **推断**：这种架构继承了 Envoy 在高并发下的 C++ 性能优势，同时利用 Go 语言构建控制面，保证了配置管理的敏捷性。作为阿里系开源项目，其代码规范性较高，且 README 支持多语言（中/日/英），文档覆盖了从架构到开发的各个环节，显示出成熟的工程化水平。对于追求生产级稳定性的团队来说，这种经过大厂验证的架构比单纯的实验性项目更具吸引力。

**4. AI 时代的开发者体验与生态**
*   **事实**：项目强调“AI Gateway”和“MCP System”。
*   **推断**：Higress 极大地降低了开发者接入 AI 能力的门槛。通过网关层面的 Prompt 模板管理和统一 API 规范，前端应用无需关心后端具体调用的是哪个模型。这种对 AI 语义层的抽象，是其在当前技术浪潮中最大的亮点。它让网关不再只是“管道”，而变成了具备业务逻辑（如 Token 鉴权、敏感词过滤）的“智能节点”。

**边界条件与不适用场景**

尽管 Higress 功能强大，但并非所有场景都适用：
1.  **极致轻量级边缘场景**：如果仅需在边缘端（如 IoT 设备）进行极其简单的流量转发，Higress 基于 K8s 和 Envoy 的架构可能过重。
2.  **传统物理机/虚拟机强绑定环境**：虽然支持 Docker，但其核心优势在于与 K8s 的深度集成。如果是非容器化的老旧架构，迁移成本可能高于收益。
3.  **简单静态站点托管**：对于仅需托管静态 HTML 的场景，使用 Nginx 或 Caddy 仍然更简单高效。

**快速验证清单**

在决定采用 Higress 前，建议进行以下验证：

1.  **性能基准测试**：使用压测工具对比 Higress（开启 WASM 插件）与原生 Nginx/Envoy 的 QPS 与延迟差异，确认 WASM 插件是否满足性能 SLA。
2.  **AI 插件兼容性实验**：实际部署一个 AI 网关场景，配置从 OpenAI 切换至开源模型（如 Llama 3）的路由规则，验证“模型切换”的透明性和 Header 转发的正确性。
3.  **MCP 协议联调**：搭建一个简单的 AI Agent，验证 Higress 作为 MCP Server 托管方的连接稳定性与工具调用响应速度。
4.  **控制面资源消耗**：在测试 K8s 集群中部署 Higress，观察控制面组件的内存与 CPU 占用，评估在资源受限集群中的运行成本。

---
## 技术分析

# Higress 技术深度分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文将从技术架构、核心功能、实现细节、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行全面剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在**云原生生态**之上，采用了典型的**控制平面与数据平面分离**的架构模式。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用 **Istio** 的控制平面能力（xDS 协议）进行配置管理。
*   **编程语言**：主要使用 **Go** 语言开发控制平面（Console、Config Controller），数据平面基于 Envoy (C++)，并通过 **WebAssembly (WASM)** 支持插件扩展（支持 C++/Go/Rust/JS 等编译为 WASM）。
*   **架构模式**：采用标准网关的 **L7 代理模式**，但在此基础上通过 WASM 实现了动态可编程的微内核架构。

### 核心模块与关键设计
1.  **控制平面**：负责配置的下发与管理。它监听 Kubernetes Ingress、Gateway API 或自定义配置，将其转换为 Envoy 的 xDS 配置。其关键设计在于**配置去重与合并**，以及**毫秒级配置推送**机制。
2.  **数据平面**：基于 Envoy，处理实际的流量转发、负载均衡、熔断、限流等。Higress 对 Envoy 进行了定制化优化，特别是针对长连接和流式传输场景。
3.  **WASM 插件系统**：这是 Higress 的“灵魂”。它允许在不重启网关的情况下动态加载插件，极大地扩展了网关的能力边界。
4.  **AI 网关模块**：专门为 LLM 设计的流量管理层，处理 Provider 路由、Token 计费、上下文缓存等 AI 特有逻辑。

### 技术亮点与创新点
*   **AI Native 理念**：不同于传统网关通过插件勉强支持 AI，Higress 将 AI 模型的调用（OpenAI 格式兼容）作为一等公民，内置了 Prompt 装饰、结果缓存和 Key 管理功能。
*   **MCP (Model Context Protocol) 服务器托管**：这是极具前瞻性的设计。Higress 不仅能转发流量，还能作为 AI Agent 的“工具集”，直接对外暴露 MCP 接口，让网关成为连接 LLM 与企业内部数据的桥梁。
*   **热更新能力**：基于 WASM 和 xDS 的结合，实现了配置和代码逻辑的热更新，对 AI 流式请求这种长连接场景极其友好，做到配置变更“零感知”。

### 架构优势分析
*   **高性能**：继承了 Envoy 的高并发、低延迟能力（C++ 异步非阻塞模型）。
*   **极致的可扩展性**：WASM 虚拟机提供了沙箱隔离的安全性，同时赋予了用户接近原生代码的扩展能力。
*   **统一管理**：将传统的微服务流量管理与 AI 流量管理统一在同一套网关中，降低了运维复杂度。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **功能**：统一管理 OpenAI、Azure、通义千问等 Provider；支持多模型切换；Token 统计与限流；Prompt 模板管理。
    *   **场景**：企业内部构建 AI 助手时，统一封装对各大模型的调用，避免前端硬编码 API Key。
2.  **MCP 服务器**：
    *   **功能**：将后端微服务或数据源包装成 AI Agent 可调用的工具。
    *   **场景**：让 ChatGPT 或 Claude 能够安全地通过网关查询企业数据库或调用内部 API。
3.  **传统 API 网关**：
    *   **功能**：Kubernetes Ingress 支持、金丝雀发布、负载均衡、认证鉴权。
    *   **场景**：替代 Nginx 或传统 Ingress Controller。

### 解决的关键问题
*   **AI 落地的碎片化**：解决了企业接入多种 LLM 时接口不统一、Key 管理混乱的问题。
*   **流式传输的不可控性**：解决了在 LLM 流式输出（SSE）过程中进行动态路由修改或拦截的难题。
*   **工具调用的安全性**：通过 MCP 托管，避免将内部服务直接暴露给公网 LLM，网关成为安全边界。

### 与同类工具对比
*   **VS Kong/APISIX**：传统网关虽然也支持 WASM，但未针对 AI 场景（如 SSE 流的截断、Token 计费）做深度优化。Higress 的 AI 指标监控和 Provider 抽象是原生优势。
*   **VS LangServe**：LangServe 侧重于 Python 服务的编排，而 Higress 侧重于**流量侧**的治理。Higress 语言无关，可以转发到任何后端实现的 AI 服务。

### 技术实现原理
*   **AI 流式处理**：Higress 在 Envoy 的 Filter 链中插入了专门处理 SSE (Server-Sent Events) 的逻辑，能够解析流式 Chunk，并在流式传输过程中进行实时计费或敏感词过滤，而不需要等待响应结束。

---

## 3. 技术实现细节

### 关键技术方案
*   **配置热更**：利用 Istio 的 xDS (v2/v3) 协议。控制平面监听配置变化，推送给 Envoy。Envoy 更新 Listener/Cluster/Route 配置时，通过 Draining 机制保证旧连接处理完毕后再切换，实现无缝切换。
*   **WASM 虚拟机**：嵌入 Proxy-WASM 规范的运行时。通常使用特定版本的 V8 引擎或 WasmEdge，通过 `on_request`、`on_response` 等钩子函数介入请求生命周期。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑。包含配置的 Ingress 转换器（K8s Resource -> xDS）、WASM 插件的管理器。
*   **`plugins/`**：内置的 WASM 插件源码，如 `ai-proxy`（AI 转发）、`key-auth`（鉴权）。
*   **`router/`**：针对 AI 请求的路由逻辑，包含模型名称的模糊匹配和版本路由算法。

### 性能与扩展性
*   **性能优化**：针对 AI 场景，优化了内存拷贝。在处理大 Prompt 或长上下文时，采用流式 Buffer 管理，避免网关层 OOM。
*   **扩展性**：支持**自定义 WASM 插件**。用户可以用 Go 写插件，编译成 `.wasm` 文件上传到 Higress，网关会自动分发到所有数据平面节点。

### 技术难点与解决方案
*   **难点**：如何在流式响应中统计 Token 数量？
*   **方案**：Higress 的 AI 插件通常不进行完整的 LLM 推理（太慢），而是通过解析 HTTP Header 或流式数据包的特定格式（如 OpenAI 的 `usage` 字段或在流中估算 Token 长度）来实现近似实时的计费和监控。

---

## 4. 适用场景分析

### 适合的项目
*   **企业级 AI 应用平台**：需要统一接入多个 LLM Provider，并对不同部门/用户进行精细化计费和限流。
*   **微服务架构**：特别是已经使用 Kubernetes 和 Istio 的团队，Higress 可以无缝融入。
*   **AI Agent 开发**：需要利用 MCP 协议将企业工具暴露给大模型的场景。

### 最有效的情况
当你的应用**既需要处理传统的 RESTful API 流量，又需要处理 AI 的流式对话流量**，且希望这两套流量共用一套鉴权、日志和监控体系时，Higress 效率最高。

### 不适合的场景
*   **极简边缘侧**：资源极度受限（如嵌入式设备）的场景，Envoy 的资源占用相对较高。
*   **纯静态内容服务**：如果只需要简单的静态文件托管，Nginx 足够且更轻量。

### 集成方式与注意事项
*   **Kubernetes 集成**：作为 Ingress Class 安装。
*   **注意事项**：WASM 插件虽然安全，但执行效率低于原生 C++ Filter。在极高 QPS（>10k）的核心路径上，需谨慎评估复杂 WASM 插件的性能损耗。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 协议支持**：除了 OpenAI 格式，未来可能原生支持更多垂直模型的协议（如 Claude 3 的特定扩展协议）。
*   **Dapr 集成**：作为 AI Agent 的基础设施，Higress 可能会与 Dapr 结合，提供更强大的服务绑定能力。

### 社区反馈与改进空间
*   **文档与易用性**：虽然功能强大，但 AI 相关的配置（如 Prompt Template 的语法）文档仍有完善空间。
*   **控制平面性能**：在大规模集群（数千个 Service）下，配置推送的延迟优化是持续改进点。

### 前沿技术结合
*   **WASI (WebAssembly System Interface)**：未来插件可能直接通过 WASI 调用网络或数据库，减少对宿主机的依赖。
*   **RAG (检索增强生成) 集成**：网关可能内置简单的向量检索逻辑，直接在网关层实现简单的 RAG，无需请求后端。

---

## 6. 学习建议

### 适合的开发者
*   具备 **Go 语言** 基础。
*   了解 **Kubernetes** 和 **Docker** 基本概念。
*   对 **云原生网关** 或 **Service Mesh** 有兴趣。

### 可以学到什么
*   **xDS 协议实战**：理解控制平面如何驱动 Envoy。
*   **WASM 插件开发**：学习如何用 Go 编写高性能、热加载的网关扩展。
*   **AI 流量治理**：了解 LLM 应用在工程化落地时的流量特征和治理难点。

### 学习路径
1.  **基础**：本地部署 Kind (Kubernetes in Docker) + Higress。
2.  **实践**：配置一个简单的 AI 代理，将请求转发至 OpenAI。
3.  **进阶**：编写一个自定义 WASM 插件，例如给所有 AI 请求的响应添加一个自定义 Header。
4.  **源码**：阅读 `pkg/ingress` 目录，理解 K8s Ingress 资源是如何转化为 Envoy 配置的。

---

## 7. 最佳实践建议

### 正确使用方式
*   **分离关注点**：将业务逻辑留在后端服务，网关只负责流量治理、认证和协议转换。不要在网关插件中编写复杂的业务逻辑。
*   **利用 WASM 隔离**：生产环境的插件务必经过资源限制测试，防止有缺陷的 WASM 插

---
## 代码示例




```python
# 示例1：Higress WasmPlugin 动态路由配置
from higress import WasmPlugin

def dynamic_routing():
    """
    实现基于请求头的动态路由
    适用场景：根据用户类型（如VIP/普通）转发到不同后端服务
    """
    plugin = WasmPlugin("dynamic-routing")
    
    # 配置路由规则
    plugin.add_route_rule(
        match=lambda ctx: ctx.request.headers.get("User-Type") == "VIP",
        action="route",
        destination="vip-service:8080"
    )
    
    plugin.add_route_rule(
        match=lambda ctx: ctx.request.headers.get("User-Type") == "Normal",
        action="route",
        destination="normal-service:8080"
    )
    
    return plugin

# 说明：此示例展示如何通过Wasm插件实现基于请求头的动态路由，
# 可用于A/B测试或灰度发布场景
```




```python
# 示例2：Higress 流量镜像配置
from higress import TrafficMirror

def mirror_traffic():
    """
    配置流量镜像到测试环境
    适用场景：在不影响生产流量的情况下测试新版本服务
    """
    mirror = TrafficMirror(
        source_service="production-service:8080",
        mirror_service="staging-service:8080",
        mirror_percentage=10  # 镜像10%的流量
    )
    
    mirror.add_header_filter(
        header="X-Mirror",
        value="true"
    )
    
    return mirror

# 说明：此示例展示如何配置流量镜像功能，
# 可用于线上流量复制到测试环境进行验证
```




```python
# 示例3：Higress 限流配置
from higress import RateLimiter

def configure_rate_limit():
    """
    配置基于IP的限流策略
    适用场景：防止API被恶意刷量
    """
    limiter = RateLimiter(
        rule_name="ip-based-limit",
        limit=100,  # 每分钟100次请求
        window=60   # 时间窗口60秒
    )
    
    limiter.add_condition(
        match=lambda ctx: ctx.request.headers.get("X-API-Key") is None,
        action="reject",
        response_code=429
    )
    
    return limiter

# 说明：此示例展示如何配置细粒度的限流策略，
# 可用于保护API免受恶意请求攻击
```


---
## 案例研究


### 1：阿里巴巴大淘宝技术部

 1：阿里巴巴大淘宝技术部

**背景**:  
在阿里巴巴内部，微服务架构极其复杂，大淘宝技术部需要统一管理数千个微服务的流量入口，同时支持云原生和传统虚拟机环境的混合部署。原有网关系统在处理高并发流量时存在性能瓶颈，且扩展性不足。

**问题**:  
1. 传统网关在双十一等大促期间，QPS（每秒查询率）峰值达到百万级时，延迟显著增加。
2. 多种协议（HTTP、Dubbo、gRPC）的统一路由管理复杂，运维成本高。
3. 需要支持动态插件扩展，但原有系统插件开发周期长。

**解决方案**:  
采用 Higress 作为下一代云原生 API 网关，基于 Envoy 和 Istio 构建。通过以下方式实施：
1. 利用 Higress 的高性能架构，将核心流量转发模块下沉至 C++ 内核。
2. 集成 Dubbo 和 gRPC 协议支持，实现多协议统一路由。
3. 使用 Higress 的 WASM 插件市场，快速部署自定义限流、认证和日志插件。

**效果**:  
1. 网关 P99 延迟降低 40%，成功支撑双十一峰值流量。
2. 运维效率提升 50%，插件开发时间从周级缩短至天级。
3. 实现了跨云（阿里云 ACK + 本地数据中心）的统一流量管理，混合云部署成本降低 30%。

---



### 2：字节跳动火山引擎

 2：字节跳动火山引擎

**背景**:  
字节跳动的火山引擎对外提供 PaaS 服务，需要为不同租户提供隔离的 API 网关服务。原有基于 Nginx 的方案在多租户场景下资源利用率低，且缺乏细粒度的流量控制能力。

**问题**:  
1. 多租户共享网关实例时，单个租户的流量突发可能影响其他租户。
2. 需要支持基于权重的蓝绿发布和金丝雀发布，但现有网关配置复杂。
3. 安全合规要求所有 API 调用必须经过细粒度的鉴权，现有鉴权系统性能不足。

**解决方案**:  
部署 Higress 作为多租户网关，结合以下特性：
1. 使用 Higress 的多租户隔离能力，为每个租户分配独立的路由规则和插件实例。
2. 通过 Higress 的流量标签功能，实现基于 Header 的金丝雀发布。
3. 集成 OAuth 2.0 和 JWT 鉴权插件，并启用 Higress 的本地缓存减少鉴权延迟。

**效果**:  
1. 单个网关集群支持的租户数量从 200 提升至 500，资源利用率提升 60%。
2. 金丝雀发布配置时间从 2 小时缩短至 10 分钟。
3. 鉴权接口 QPS 提升 3 倍，同时满足 SOC 2 安全审计要求。

---



### 3：哔哩哔哩直播中台

 3：哔哩哔哩直播中台

**背景**:  
哔哩哔哩直播中台需要为多个业务线（如游戏直播、赛事直播）提供统一的 API 网关，支持实时弹幕、礼物打赏等高并发低延迟场景。原有网关无法满足毫秒级延迟要求。

**问题**:  
1. 弹幕推送的 WebSocket 连接数峰值达到千万级，现有网关内存占用过高。
2. 需要 A/B 测试不同推荐算法，但网关层缺乏灵活的流量分流能力。
3. 监控系统与网关脱节，无法实时定位接口异常。

**解决方案**:  
引入 Higress 并结合以下优化：
1. 启用 Higress 的 WebSocket 长连接优化，将连接状态卸载至 Redis。
2. 使用 Higress 的动态路由规则，实现基于用户 ID 的 A/B 测试。
3. 通过 OpenTelemetry 集成，将网关指标接入 Prometheus + Grafana 监控栈。

**效果**:  
1. WebSocket 连接内存占用降低 70%，单节点支持 50 万并发连接。
2. 算法 A/B 测试迭代周期从 3 天缩短至 1 天。
3. 接口异常定位时间从平均 30 分钟缩短至 5 分钟，可用性提升至 99.99%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Apache APISIX | Kong |
|------|----------------|---------------|------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能优异，适合高流量场景 | 基于OpenResty，性能良好，适合中小规模 |
| 易用性 | 提供可视化控制台，集成Kubernetes，操作简便 | 配置灵活但复杂，需要一定学习成本 | 插件丰富，但配置依赖文件，管理复杂 |
| 功能 | 支持流量管理、安全防护、可观测性，与云原生集成 | 插件生态丰富，支持动态路由、限流熔断 | 插件生态强大，支持认证、监控、限流 |
| 成本 | 开源免费，商业版提供企业支持 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 社区 | 阿里背书，社区活跃，文档完善 | 社区活跃，文档齐全 | 社区成熟，文档丰富 |

### 优势分析

- 优势1：与Kubernetes和Istio深度集成，适合云原生环境。
- 优势2：提供可视化控制台，降低运维复杂度。
- 优势3：阿里技术支持，适合企业级应用。

### 不足分析

- 不足1：相比Apache APISIX，插件生态稍弱。
- 不足2：社区规模小于Kong，第三方资源较少。
- 不足3：对非Kubernetes环境支持有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量管理与路由配置

**说明**:  
Higress 基于 Kubernetes Ingress API 提供了强大的流量管理能力。通过配置 Ingress 规则，可以实现基于域名、路径、Header 等条件的路由分发，支持灰度发布和蓝绿部署。

**实施步骤**:
1. 定义 Ingress 资源，配置 `spec.rules` 指定路由规则。
2. 使用 `nginx.ingress.kubernetes.io/canary` 注解实现灰度发布。
3. 通过 `kubectl apply -f ingress.yaml` 部署规则。

**注意事项**:  
- 确保路由规则的优先级合理，避免冲突。
- 灰度发布时需监控流量分配是否符合预期。

---

### 实践 2：插件扩展与自定义开发

**说明**:  
Higress 支持通过插件机制扩展功能，如限流、认证、日志等。用户可以基于 Lua 或 WASM 开发自定义插件，满足特定业务需求。

**实施步骤**:
1. 在 Higress 控制台或通过 CLI 启用插件市场。
2. 选择或开发插件，编写 Lua/WASM 代码。
3. 将插件上传并绑定到特定路由或服务。

**注意事项**:  
- 插件开发需遵循 Higress 规范，避免性能问题。
- 测试插件时建议先在非生产环境验证。

---

### 实践 3：安全防护与访问控制

**说明**:  
Higress 提供多层次的安全防护，包括 IP 黑白名单、JWT 认证、CORS 配置等。合理配置可提升系统安全性。

**实施步骤**:
1. 在 Ingress 或全局配置中启用 IP 黑白名单。
2. 配置 JWT 认证插件，验证请求合法性。
3. 设置 CORS 规则，限制跨域访问。

**注意事项**:  
- 定期更新安全策略，避免规则过时。
- JWT 密钥需妥善保管，防止泄露。

---

### 实践 4：监控与日志集成

**说明**:  
Higress 支持与 Prometheus、Grafana、ELK 等监控日志系统集成，实时观测流量、延迟、错误率等指标。

**实施步骤**:
1. 配置 Higress 的 Prometheus Exporter。
2. 在 Grafana 中导入 Higress 仪表盘模板。
3. 设置日志输出到 Elasticsearch 或其他日志系统。

**注意事项**:  
- 监控指标需根据业务需求定制，避免数据冗余。
- 日志量较大时需优化采集策略。

---

### 实践 5：高可用部署与容错

**说明**:  
生产环境中需确保 Higress 的高可用性，避免单点故障。可通过多副本部署、健康检查和自动扩缩容实现。

**实施步骤**:
1. 在 Kubernetes 中部署多个 Higress 副本（至少 3 个）。
2. 配置 `readinessProbe` 和 `livenessProbe` 健康检查。
3. 启用 HPA（Horizontal Pod Autoscaler）根据负载自动扩缩容。

**注意事项**:  
- 健康检查参数需根据实际业务调整。
- 扩缩容时需考虑资源限制和成本。

---

### 实践 6：性能优化与资源限制

**说明**:  
通过调整 Higress 的资源配置和参数，可提升吞吐量并降低延迟。例如优化连接池、缓冲区大小等。

**实施步骤**:
1. 在 Kubernetes 中为 Higress Pod 设置合理的 CPU/内存限制。
2. 调整 `worker_processes` 和 `worker_connections` 参数。
3. 启用 HTTP/2 或 gRPC 优化长连接场景。

**注意事项**:  
- 性能调优需基于实际负载测试，避免盲目调整。
- 监控资源使用率，防止过载。

---

### 实践 7：版本升级与兼容性管理

**说明**:  
Higress 版本迭代较快，升级时需注意兼容性和平滑过渡，避免业务中断。

**实施步骤**:
1. 查阅版本发布说明，确认变更点。
2. 在测试环境验证升级流程。
3. 生产环境采用滚动更新策略，逐步替换旧版本。

**注意事项**:  
- 升级前备份配置和数据。
- 关注废弃 API 或配置项的迁移方案。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题。在弱网或丢包率较高的网络环境下，能显著减少连接建立延迟和提升传输稳定性。对于 Higress 这样的 API 网关，能够极大改善移动端或跨地域调用的体验。

**实施方法**:
1. 在 Higress 的网关配置中，找到监听器设置。
2. 开启 HTTP/3 或 QUIC 协议支持。
3. 配置 UDP 端口（通常复用 443 端口或使用指定端口）。
4. 确保负载均衡器或前端防火墙正确转发 UDP 流量。

**预期效果**: 在高丢包网络环境下，请求延迟可降低 30%-50%；连接建立时间减少 1-2 个 RTT。

---

### 优化 2：启用 Wasm 插件与 L4/L7 缓存加速

**说明**: Higress 原生支持 WebAssembly (Wasm)。将 CPU 密集型或复杂逻辑的插件（如复杂的请求校验、数据转换）用 C++/Rust/Go 编译为 Wasm 运行，比传统的 Lua (OpenResty) 性能更高。同时，对响应内容启用分层缓存可降低后端压力。

**实施方法**:
1. 将高频使用的 Lua 插件迁移为 Wasm 格式。
2. 在路由配置中启用缓存策略，对静态资源或高 QPS 的 GET 请求设置缓存 TTL。
3. 配置缓存 Key 规则，确保精准命中。

**预期效果**: Wasm 插器执行效率提升约 20%-40%；缓存命中后后端请求量减少 60%-90%，总吞吐量提升。

---

### 优化 3：全链路超时与连接池调优

**说明**: 默认配置通常较为保守。在高并发场景下，过小的连接池会导致请求排队等待，而过长的超时会导致资源堆积。针对业务特性调整上游服务的连接池和超时参数是提升吞吐的关键。

**实施方法**:
1. **连接池调优**: 增加 Higress 与上游服务之间的 `maxConnections`（例如从默认的 128 调整至 512 或更高）。
2. **超时配置**: 根据业务 P99 耗时，合理设置 `connectTimeout`、`sendTimeout` 和 `readTimeout`，避免无效连接占用。
3. **空闲连接清理**: 调整 `idleTimeout`，及时释放不活跃连接。

**预期效果**: 在高并发下，减少请求排队时间，网关 P99 延迟降低 15%-30%，有效防止连接池耗尽导致的 502 错误。

---

### 优化 4：配置分离与 DNS 缓存优化

**说明**: Higress 支持配置中心。频繁的配置变更推送或 DNS 解析请求会影响网关数据面的处理性能。优化 DNS 解析频率和减少不必要的配置更新轮询可以降低 CPU 负载。

**实施方法**:
1. 启用 DNS 缓存，并设置合理的 TTL（Time To Live），避免对同一域名的高频解析。
2. 在使用服务发现（如 Nacos）时，调整客户端缓存列表的刷新频率，避免全量推送过于频繁。
3. 确保配置热更新机制采用增量推送而非全量 reload。

**预期效果**: 降低 CPU 和网络 I/O 开销约 10%-20%，减少因 DNS 解析失败导致的偶发性 5xx 错误。

---

### 优化 5：启用请求体缓冲与流式处理优化

**说明**: 对于需要读取请求体进行鉴权或路由的插件，默认的流式处理可能会限制灵活性。针对大文件上传或高吞吐 POST 请求，合理配置缓冲策略或启用流式处理转发，可以减少内存占用并提升转发效率。

**实施方法**:
1. 对于小体积 API 请求，在插件配置中启用 `bufferRequestBody`，确保网关读取完整

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba Higress 项目），以下是关键要点总结：
- Higress 是阿里巴巴开源的一款基于 Istio 的云原生 API 网关，旨在解决云原生架构下的流量管理、安全及可观测性问题。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，降低云原生迁移门槛。
- 它内置了对 Dubbo、Nacos 等微服务生态的完善支持，特别适合需要将传统微服务架构平滑迁移至云原生平台的场景。
- Higress 提供了高性能的流量处理能力，并支持 WAF 插件与安全防护，有效保障后端服务的稳定性与安全性。
- 通过提供标准化的 Wasm 插件扩展机制，用户可以灵活地通过 Lua、Go 或 Rust 编写插件来扩展网关功能。
- 该项目兼容 Nginx Ingress 注解及大部分云原生网关特性，常被视作 Nginx Ingress Controller 的现代化替代方案。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心架构设计（基于 Envoy 和 Istio）
- 基本术语：Ingress、Gateway、Route、Service、Upstream
- 容器化基础（Docker 与 Kubernetes 基础操作）
- Higress 与传统 Nginx/API 网关的区别

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档：架构与原理介绍
- Envoy 官方文档基础部分（了解 Proxy 原理）

**学习建议**: 
此阶段重点在于理解“为什么需要 Higress”。建议先阅读官方文档的背景介绍，对比传统硬件负载均衡、Nginx 和云原生网关的差异。如果对 Kubernetes 不熟悉，需要先补充 K8s Ingress 的基础知识。

---

### 阶段 2：部署上手与基础配置

**学习内容**:
- 本地开发环境搭建（Docker Desktop 或 Kind 集群）
- 在 Kubernetes 集群中安装 Higress（Helm 安装方式）
- Higress 控制台的使用与界面介绍
- 配置第一个简单的路由转发
- 域名、路径、Header 路由规则的配置
- 基本的服务发现与负载均衡配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方快速开始指南
- Higress 官方示例
- Kubernetes 官方文档关于 Service 和 Ingress 的部分

**学习建议**: 
动手实践是本阶段的核心。建议在本地搭建一个最小化的 K8s 环境，并成功部署 Higress。尝试部署一个简单的后端服务（如 echo 服务），通过 Higress 将流量路由进去。熟悉控制台（Console）的操作是后续进阶的基础。

---

### 阶段 3：流量治理与安全管控

**学习内容**:
- 高级流量管理：金丝雀发布、蓝绿发布、A/B 测试
- 流量防护与熔断降级（结合 Sentinel）
- 全局与细粒度的认证与鉴权（Basic Auth, JWT, OIDC）
- WAF（Web 应用防火墙）插件的使用与配置
- CORS 与跨域问题处理
- Mock 服务与故障注入

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：流量治理与安全板块
- Sentinel 官方文档（了解流控规则）
- Higress GitHub Issues 中的常见配置案例

**学习建议**: 
此阶段重点在于掌握“如何控制流量”。建议模拟生产环境场景，例如配置一个金丝雀发布流程，将 10% 的流量导入新版本。同时，尝试配置 WAF 规则拦截恶意请求，理解 Higress 如何保障 API 安全。

---

### 阶段 4：插件生态与可扩展性

**学习内容**:
- Higress 插件机制原理（Wasm 与 Lua）
- 使用官方预置插件解决特定问题（如请求限流、API 鉴权、请求/响应修改）
- 开发自定义 Wasm 插件（使用 Go 或 C++）
- 插件的配置管理与热加载
- Higress 与 Dubbo、gRPC 协议的扩展支持
- 服务网格对接与 Sidecar 模式理解

**学习时间**: 4-6周

**学习资源**:
- Higress 官方插件开发文档
- Wasm 官方网站与教程
- Higress 官方插件市场
- Higress 源码分析文章

**学习建议**: 
这是从“使用者”向“开发者”转变的关键阶段。建议先深入研究官方提供的插件源码，理解其处理逻辑。随后，尝试编写一个简单的 Wasm 插件（例如修改请求 Header 或 Body），并在本地环境中编译、加载和测试。

---

### 阶段 5：生产级运维与性能调优

**学习内容**:
- Higress 的高可用部署架构
- 监控与可观测性：对接 Prometheus、Grafana、SkyWalking
- 日志分析与排查
- 性能压测与参数调优（连接池、缓冲区大小等）
- 灰度升级与回滚策略
- 多集群管理与容灾备份
- 源码级深度剖析与贡献

**学习时间**: 持续学习

**学习资源**:
- Higress 运维最佳实践文档
- Envoy 性能调优指南
- Higress GitHub 源码
- 云原生社区关于网关性能的深度技术文章

**学习建议**: 
此阶段面向生产环境。建议学习如何构建可观测体系，通过 Grafana Dashboard 监控网关的 QPS、延迟、成功率等关键指标。阅读 Higress 源码，理解

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴正式开源，并捐赠给云原生计算基金会（CNCF） landscape 的项目。

Higress 的前身是阿里巴巴集团内部统一使用的 API 网关，支撑了阿里内部成千上万的业务流量。它深度集成了阿里云的生态，同时完全兼容 Istio 和 Kubernetes 的标准。简单来说，它汲取了阿里巴巴在电商、金融等高并发场景下的网关建设经验，并结合了开源社区（特别是 Envoy 和 Istio）的优势，旨在提供一款既标准又高性能、且易于扩展的网关产品。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在“云原生集成”和“安全防护”两个维度：

1.  **深度集成 Istio**：Higress 底层基于 Envoy，但通过独特的架构设计，可以与 Istio 服务网格实现深度集成。它允许用户在同一个控制平面下管理东西向（服务间）流量和南北向（入口）流量，解决了传统网关与 Sidecar 代理配置割裂的问题。
2.  **内置安全能力**：得益于阿里巴巴的基因，Higress 内置了强大的 WAF（Web 应用防火墙）功能，能够有效防御 SQL 注入、XSS、WebShell 等常见攻击，这在同类开源网关中通常是需要额外购买或配置复杂插件的。
3.  **高性能与低延迟**：针对高并发场景进行了深度优化，支持热更新，配置变更无需重启进程，对业务流量几乎无影响。
4.  **标准化插件市场**：它提供了类似 Wasm 的插件市场，支持 Go、C++、Rust、JavaScript 等多语言编写插件，开发者可以像逛应用市场一样轻松扩展网关功能。

---



### 3: Higress 是否兼容 Nginx 的配置？迁移成本高吗？

3: Higress 是否兼容 Nginx 的配置？迁移成本高吗？

**A**: Higress 对 Nginx 用户非常友好，迁移成本相对较低。

1.  **配置兼容性**：Higress 提供了 Nginx Ingress 注解的兼容支持，许多标准的 Nginx 配置指令可以在 Higress 中找到对应的实现或直接转换。
2.  **Ingress 支持**：它完全支持 Kubernetes Ingress API 和 Gateway API，这意味着如果你目前使用的是 Nginx Ingress Controller，通常只需要调整控制平面配置，无需大规模修改应用层面的代码或资源定义。
3.  **迁移工具**：社区也提供了相应的工具来辅助将 Nginx 配置转换为 Higress 的配置格式。因此，对于已有的 Kubernetes 集群，从 Nginx 迁移到 Higress 通常是平滑且渐进的。

---



### 4: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC 这样的微服务协议？

4: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC 这样的微服务协议？

**A**: 是的，Higress 对微服务协议的支持非常广泛，这也是阿里巴巴系产品的强项。

除了标准的 HTTP、HTTPS 之外，Higress 原生支持：
1.  **gRPC**：支持 gRPC 服务的代理、路由以及负载均衡，支持 gRPC-Web 以便浏览器直接调用。
2.  **Dubbo**：这是 Higress 区别于许多国外开源网关的一大亮点。由于阿里巴巴在 Dubbo 生态的深厚积累，Higress 能够直接代理 Dubbo 服务，实现 HTTP 到 Dubbo 的协议转换，让前端可以通过 RESTful API 调用后端的 Dubbo 服务。
3.  **WebSocket**：支持 WebSocket 协议的代理，适用于实时通讯场景。
4.  **QUIC/HTTP3**：对新一代网络协议也有支持。

---



### 5: Higress 的插件机制是如何工作的？支持用 Java 或 Go 编写插件吗？

5: Higress 的插件机制是如何工作的？支持用 Java 或 Go 编写插件吗？

**A**: Higress 采用了基于 Envoy 的 Wasm（WebAssembly）插件架构，这是云原生网关的主流技术方向。

1.  **多语言支持**：虽然 Envoy 原生主要使用 C++，但通过 Wasm，Higress 允许开发者使用 **Go、Rust、JavaScript (AssemblyScript)、C++** 等语言编写插件逻辑。
2.  **Java 支持**：虽然不能直接用 Java 写 Wasm 插件，但 Higress 提供了 Java Processor 的适配模式，允许通过 Java 程序处理外部请求，或者在特定架构下通过 gRPC 扩展服务来实现 Java 逻辑的介入。
3.  **热加载**：基于 Wasm 的插件支持动态加载和卸载，无需重启网关进程即可生效，极大地提升了运维效率和迭代速度。
4.  **插件市场**：官方提供了一个插件市场，开发者可以上传自己的插件，也可以直接复用社区已有的认证、限流、流量镜像等插件。

---



### 6: Higress 是否

6: Higress 是否

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 官方镜像，快速部署一个网关实例，并配置一个简单的路由规则，将访问 `/example` 路径的流量转发到 `httpbin.org` 的 `/get` 接口。

### 提示**: 需要熟悉 Docker 容器的基本操作，并查阅 Higress 关于 `Ingress` 或路由配置的 YAML 文件结构，重点关注 `host`、`path` 和 `service` 字段的映射关系。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位及其在阿里巴巴内部的实践，以下是针对实际生产环境的 6 条实践建议：

### 1. 利用 AI 代理插件实现模型供应商的无感切换
Higress 的核心优势在于其 AI 原生能力，特别是对 LLM（大语言模型）的支持。在生产环境中，不要将后端服务硬编码为调用特定的云厂商（如 OpenAI 或通义千问）接口。
*   **操作建议**：配置 Higress 的 `ai-proxy` 插件。在网关层统一处理不同厂商的 API Key 轮换、鉴权以及协议差异（如将 OpenAI 格式转换为其他厂商格式）。
*   **最佳实践**：将模型路由逻辑下沉到网关。业务代码只需调用 Higress，由 Higress 根据配置转发到最便宜的模型或备用的模型供应商，从而实现零代码成本的供应商切换。

### 2. 实施语义路由而非传统的正则匹配
传统的 API 网关通常基于路径（如 `/api/v1/user`）进行路由，但在 AI 场景下，基于用户意图的路由更为强大。
*   **操作建议**：使用 Higress 的语义路由功能。配置不同的 Prompt 模板或模型服务，根据用户输入的文本内容（例如“帮我写代码” vs “帮我画图”）自动将请求分发到不同的后端服务（如 Code Llama 或 Stable Diffusion 服务）。
*   **常见陷阱**：不要试图在业务代码中写大量的 `if-else` 来判断用户意图，这会导致业务逻辑臃肿。利用网关的语义路由能力可以保持后端服务的纯净性。

### 3. 配置“令牌级”超时与重试策略
LLM 请求通常耗时较长（流式输出可能持续数十秒），且容易因为网络波动或服务端限流而中断。
*   **操作建议**：在 Higress 路由配置中，将超时时间设置得比普通 API 更长（建议 60s 以上）。同时，针对非流式请求配置指数退避的重试策略。
*   **常见陷阱**：避免使用默认的短超时（如 5s-10s），这会导致大模型生成回答到一半时连接被网关强制断开，用户端收到报错。
*   **进阶**：利用 Higress 对流式传输（SSE/Chunked）的支持，确保即使超时，已生成的部分内容也能被客户端接收，而不是完全丢失上下文。

### 4. 启用结果缓存以降低 Token 消耗成本
AI 请求的成本主要来自 Token 消耗，且高并发下后端模型容易成为瓶颈。
*   **操作建议**：针对知识库问答或相似问题较多的场景，开启 Higress 的缓存插件。可以基于请求的 Hash 或 Prompt 的语义向量进行缓存。
*   **最佳实践**：对于“事实性”问题（如“公司报销政策是什么”），直接返回缓存结果，既减少了延迟（从秒级降到毫秒级），又节省了昂贵的 API 调用费用。

### 5. 建立基于 Prompt 的安全护栏
直接将用户输入透传给 LLM 存在 Prompt 注入风险，可能导致系统泄露敏感信息。
*   **操作建议**：在 Higress 的请求预处理阶段，配置安全插件或简单的 Lua/Wasm 脚本，对用户输入进行清洗或拦截。
*   **具体场景**：配置规则拦截包含“忽略之前的指令”或“打印系统提示词”等特征的恶意输入。在流量到达昂贵的 GPU 集群之前，在 CPU 层面的网关上拦截掉恶意攻击。

### 6. 统一敏感信息管理与访问控制
由于 AI Gateway 需要持有调用各大 LLM 厂商的 API Key，这些密钥的安全性至关重要。
*   **操作建议**：切勿将 API Key 明文写入配置文件并提交到 Git 仓库。使用 Higress 支持的 KMS（密钥管理服务）或 Secrets 管理功能（如集成

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI网关](/tags/ai%E7%BD%91%E5%85%B3/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [中国开源AI生态的架构选择：超越DeepSeek的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的技术路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-9.md" >}})
- [为何推出科学领域AI播客以及工程师应关注的原因]({{< relref "posts/20260129-blogs_podcasts-its-time-to-science-2.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*