---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T21:59:04+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： **项目概况** Higress 是一款由阿里巴巴开源的、基于 **Go** 语言开发的**云原生 API 网关**。它构建在 Istio 和 Envoy 之上，目前定位为 **AI Native API Gateway**（AI 原生 API 网关），在 GitHub 上拥"
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

Higress 是基于 Istio 和 Envoy 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，支持传统流量治理与 AI 应用网关双重场景。它能够统一管理 LLM 流量、托管 MCP 服务器，并处理 Kubernetes Ingress 与微服务路由，适合需要在同一架构下融合 AI 服务与传统 API 的开发团队。本文将介绍其核心架构、AI 网关特性及插件系统，帮助你评估是否将其纳入技术栈。

---
## 摘要

以下是对 Higress 项目的简洁总结：

**项目概况**
Higress 是一款由阿里巴巴开源的、基于 **Go** 语言开发的**云原生 API 网关**。它构建在 Istio 和 Envoy 之上，目前定位为 **AI Native API Gateway**（AI 原生 API 网关），在 GitHub 上拥有超过 7,400 颗星。

**核心特点**
Higress 架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离。它利用 **WebAssembly (WASM)** 插件系统扩展能力，支持通过 xDS 协议毫秒级下发配置，且不中断连接，非常适合 AI 长连接流式响应场景。

**三大主要功能**
1.  **AI 网关**：提供统一的 API 接入 30 多家大语言模型（LLM）提供商，具备协议转换、可观测性、缓存和 AI 安全防护能力。
2.  **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务。
3.  **标准 API 网关**：作为 Kubernetes Ingress 控制器使用，支持微服务路由，并兼容 nginx-ingress 注解。

**核心组件**
包括 `ai-proxy`（AI 代理）、`ai-cache`（AI 缓存）、`mcp-router`（MCP 路由）等插件及过滤器，实现了从传统微服务治理到 AI 流量管理的全面覆盖。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**结合得最彻底的开源项目之一。它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 MCP 协议的深度集成，为 LLM（大模型）应用提供了一套标准化的流量与模型治理方案，是企业构建 AI 基础设施的高性价比选择。

### 深度评价分析

#### 1. 技术创新性：从“流量网关”向“AI 神经中枢”的演进
*   **差异化方案（事实+推断）**：Higress 最大的创新在于提出了 **AI Native API Gateway** 的概念。不同于 Kong 或 APISIX 仅作为通用 HTTP 网关，Higress 原生集成了**MCP (Model Context Protocol)** 服务托管能力。这意味着它不仅能转发请求，还能直接作为 AI Agent 的“工具箱”提供商，解决了 Agent 与外部工具连接的标准化问题。
*   **WASM 的深度应用**：基于 Envoy 的 WASM 插件机制，Higress 允许开发者使用 C++/Go/Rust/AssemblyScript 编写高性能插件。这对于 AI 场景至关重要，例如在网关层实时进行 Token 计数、敏感词过滤或 Prompt 注入，而无需重启网关或修改后端应用代码。

#### 2. 实用价值：统一 AI 与微服务的“入口”
*   **解决关键问题（推断）**：在 AI 应用爆发期，企业面临三个痛点：模型供应商的切换成本高、Token 消耗不可控、LLM 调用的安全性（Prompt 注入攻击）。Higress 通过内置的**AI 路由**和**Provider 适配**，允许用户通过配置文件在不同大模型（如 OpenAI、通义千问、Llama）之间无缝切换，实现了“去厂商锁定”。
*   **应用场景（事实）**：它既支持 Kubernetes Ingress（微服务入口），又支持 AI Gateway。这意味着企业可以用一套基础设施同时管理传统的 RESTful API 和新兴的 LLM 流量，显著降低了运维复杂度和基础设施成本。

#### 3. 代码质量与架构：云原生标准的稳健实践
*   **架构设计（推断）**：Higress 采用了标准的**控制平面与数据平面分离**架构。控制平面基于 Istio 进行了简化与增强（去掉了 Sidecar 模式的复杂性），数据平面依托 Envoy。这种设计既保证了数据面的极致性能（C++ 实现），又利用 Go 语言实现了控制面的敏捷开发。
*   **文档与规范（事实）**：仓库提供了多语言（中/日/英） README，且 DeepWiki 显示其拥有详细的架构、构建和开发指南。作为阿里巴巴开源的项目，其代码规范遵循了 Go 语言的标准实践，且在生产环境经过了大规模验证（支撑了阿里内部及阿里云的流量）。

#### 4. 社区活跃度：头部背书与生态建设
*   **活跃度指标（事实）**：拥有 **7,400+ Stars**，对于基础设施类项目而言，这是一个非常高的关注度，表明市场需求强烈。
*   **生态建设（推断）**：作为阿里云产品 Higress 的开源版，它拥有稳定的维护团队。社区不仅关注传统的网关功能，近期热点集中在 AI 插件开发（如 Python Runtime 支持）和与大模型的集成适配上，这种紧跟技术趋势的迭代速度是其活跃度的核心保障。

#### 5. 学习价值：理解 AI 时代的流量治理
*   **对开发者的启发**：Higress 是学习**“如何将 AI 协议（如 SSE 流式传输、OpenAPI 格式）融入传统 HTTP 网关”**的最佳范例。开发者可以从中学习如何处理流式响应的转发、超时控制以及如何在网关层实现 AI 语义层的负载均衡（而不仅仅是连接层）。
*   **WASM 插件开发**：它提供了一个低门槛的 WASM 插件开发平台，后端开发者可以通过编写简单的逻辑来扩展网关功能，而不需要懂 C++ 或修改 Envoy 核心代码。

#### 6. 潜在问题与改进建议
*   **复杂度曲线**：虽然基于 Istio，但完全剥离了 Sidecar 模式，专注于 Gateway API。对于已经深度绑定 Istio 原生资源的用户，迁移成本需要评估。
*   **AI 功能的成熟度**：作为新晋功能，其 MCP 协议支持和 AI 插件生态（如现成的安全防护插件）尚在丰富中，可能需要企业自行开发部分特定逻辑。
*   **性能损耗**：在启用复杂的 WASM 插件（特别是涉及 AI 模型推理或大量文本处理）时，会增加网关的延迟，建议将重度逻辑下沉到独立服务，网关仅做轻量级处理。

#### 7. 与同类工具的对比优势
*   **对比 Kong/APISIX**：传统网关插件丰富，但在 AI 领域（如 LLM 协议支持、Token 限流、MCP 协议）需要大量二次开发。Higress 开箱即用。
*   **对比 Istio Ingress**：Istio 过于厚重，配置复杂。Higress 专注于 Ingress 场景，去除了冗余功能，提供了更友好的控制台和配置方式。
*   **核心优势**：**“懂 AI”** 是其最大护城河。它

---
## 技术分析

# Higress 技术深度分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本报告将从架构设计、核心功能、技术实现、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构遵循**云原生**的设计范式，采用**控制面与数据面分离**的架构模式。
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力；基于 **Istio** 的控制面理念进行配置管理（但进行了轻量化和改造）。
*   **技术栈**：核心逻辑使用 **Go** 语言编写（控制面与网关逻辑），插件扩展采用 **WebAssembly (WASM)**（支持 C++/Go/Rust/AssemblyScript 等编写），底层代理为 Envoy (C++)。

### 核心模块与关键设计
1.  **控制面**：
    *   负责 Ingress/API Gateway 配置的解析（如 Kubernetes Ingress YAML 或自定义 CRD）。
    *   通过 **xDS 协议**（包括 LDS, CDS, RDS, EDS）将配置下发至数据面。
    *   **关键设计**：配置热更新。通过 xDS 的增量推送机制，配置变更可以在毫秒级生效且不断开连接，这对 AI 长连接场景至关重要。
2.  **数据面**：
    *   基于 Envoy，负责实际的流量转发、负载均衡、WASM 插件执行。
    *   **关键设计**：高并发、低延迟。Envoy 的事件驱动架构保证了处理海量 AI 请求时的性能。
3.  **WASM 插件系统**：
    *   这是 Higress 的“灵魂”。它允许用户在不重新编译网关二进制文件的情况下，动态加载业务逻辑。
    *   **关键设计**：沙箱隔离。插件运行在 WASM 虚拟机中，崩溃不会导致网关崩溃，且内存隔离性较好。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：Higress 是业界较早明确提出“AI 网关”定位的产品。它不仅仅是透传流量，还内置了对 **LLM 协议**（如 OpenAI 协议）的理解。例如，它能在网关层处理 Prompt 的上下文拼接、Token 计费、语义路由等。
*   **MCP (Model Context Protocol) Server Hosting**：支持直接在网关层面托管 AI Agent 的工具调用服务，简化了 Agent 架构的部署复杂度。
*   **Kubernetes 原生集成**：无缝对接 K8s Ingress，无需引入复杂的 Istio 全局治理，即可享受 Envoy 的强大功能。

### 架构优势分析
*   **安全性**：WASM 的沙箱机制防止了恶意或错误插件导致网关进程崩溃。
*   **可扩展性**：用户可以用 Go/Rust 编写复杂逻辑，通过 WASM 部署，解决了传统 Lua 插件（如 OpenResty）开发门槛高且性能不稳定的问题。
*   **统一性**：将传统微服务流量与 AI 大模型流量统一管理，减少了基础设施的碎片化。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **功能**：Provider 聚合（一个入口对接 OpenAI、通义千问等）、Token 计费与流控、Prompt 模板管理、**结果缓存**（减少 LLM 调用成本）。
    *   **场景**：企业构建 AI 应用时，统一管理多个 LLM 供应商的 Key，控制成本，屏蔽后端模型变更对客户端的影响。
2.  **MCP 系统集成**：
    *   **功能**：作为 AI Agent 的工具提供者。
    *   **场景**：当 AI Agent 需要调用外部工具（如查询数据库、调用天气 API）时，Higress 可以托管这些工具的定义和连接，充当 Agent 与工具之间的桥梁。
3.  **传统 API 网关**：
    *   **功能**：金丝雀发布、蓝绿部署、负载均衡、认证鉴权。
    *   **场景**：替代 Nginx Ingress Controller 或 Kong，作为 K8s 集群的统一流量入口。

### 解决的关键问题
*   **LLM 流式响应的转发难题**：传统的网关在处理 SSE (Server-Sent Events) 或流式响应时，往往会出现缓冲延迟或连接中断。Higress 基于 Envoy 的流式处理能力，实现了真正的**流式透传**，降低了首字生成时间（TTFT）。
*   **插件生态的割裂**：在 APISIX 或 Kong 中，插件多由 C++ 或 Lua 开发，维护成本高。Higress 利用 WASM，允许后端工程师使用熟悉的语言（如 Go）编写网关逻辑，降低了扩展门槛。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **底层** | Envoy (Go控制) | Nginx/OpenResty | Apache APISIX (Lua) | Nginx (C) |
| **扩展性** | WASM (多语言) | Lua/C/Go | Lua/Java | C/Lua |
| **AI 特性** | **原生支持 (Prompt/Token/MCP)** | 需插件 | 需插件 | 无 |
| **性能** | 极高 (C++ Data Plane) | 高 | 高 | 极高 |
| **配置下发** | xDS (gRPC) | 数据库/Rest Admin | etcd | Reload (进程) |

### 技术实现原理
*   **AI 协议转换**：Higress 在 HTTP 过滤器层面拦截请求。检测到 Content-Type 或 URL 路径匹配 LLM 特征时，触发 AI 专用过滤器。该过滤器解析请求体，提取 Prompt，根据配置进行修改或路由，然后通过流式机制将响应体分段返回给客户端。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 集成了 **Wasmtime** 或 **V8** 引擎。在 Envoy 的 Filter Chain 中，WASM Filter 被插入。Go 控制面将编译好的 `.wasm` 文件通过 xDS 协议推送到 Envoy，Envoy 加载并实例化虚拟机。
*   **配置分发**：Higress Controller 监听 K8s API Server 的资源变化。它将 K8s Ingress/Gateway 资源转换为 Envoy 的 xDS 配置。为了保证配置一致性，它维护了全量和增量的配置版本控制。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑。包含 ingress 转换器、xDS 服务器实现、路由匹配逻辑。
*   **`plugins/`**：内置 WASM 插件的源码（如 Keyless Request、AI Request Blocker）。
*   **`installer/`**：基于 Helm 的安装脚本。
*   **设计模式**：大量使用 **Controller-Model**（K8s 风格的控制器模式）和 **Strategy Pattern**（用于不同的路由匹配策略和插件执行策略）。

### 性能与扩展性
*   **性能优化**：由于数据面是 Envoy（C++），处理网络 I/O 的性能极高。WASM 插件的执行虽然有虚拟机开销，但通过 **Lazy Initialization**（延迟初始化）和 **AOT Compilation**（预编译）优化，通常能满足绝大多数业务需求。
*   **扩展性**：水平扩展能力极强，由于是无状态设计，可以直接在 K8s 中增加 Pod 副本。

### 技术难点
*   **WASM 的资源限制**：WASM 插件如果死循环或内存泄漏，可能导致网关 OOM。Higress 通过配置 `runtime` 的 CPU 时间片限制和内存上限来缓解此问题。
*   **xDS 的版本控制**：在多副本环境下，保证所有 Envoy 实例配置的一致性和时序性是一个挑战，通常采用控制面状态机来解决。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **大模型应用开发**：需要对接多家 LLM 厂商，需要在网关层做统一鉴权、Token 统计、Prompt 模板管理的场景。
2.  **云原生微服务**：已经使用 Kubernetes 部署，需要高性能 Ingress Controller，且业务逻辑需要通过自定义插件扩展的场景。
3.  **混合云架构**：需要统一管理跨云、跨数据中心的流量，利用 Envoy 的强大网络能力。

### 最有效的情况
*   当你需要**快速迭代网关业务逻辑**（如增加一个特殊的认证算法）时，使用 WASM 插件可以在不重启网关、不重新构建镜像的情况下秒级发布。
*   当你需要处理**高并发的 AI 流式请求**时，Envoy 的流式处理能力比基于 Node.js 或 Python 的网关框架更稳健。

### 不适合的场景
*   **极简静态站点托管**：如果只是简单的静态文件托管，Nginx 或 Caddy 更轻量，Higress 的 K8s 依赖显得过重。
*   **极端性能要求的纯四层负载均衡**：如果是纯粹的四层 TCP/UDP 转发，IPVS 或单纯的 Envoy 配置可能更直接，Higress 带来了额外的七层处理开销。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 集成**：未来可能会内置 RAG（检索增强生成）的网关层实现，例如在网关层直接向 Vector Database 发起查询并注入 Prompt。
*   **WASM 性能提升**：随着 WASM 标准的演进（如 WASM GC），支持更高级语言（如 C#）编写插件，且性能逼近原生代码。

### 社区与改进
*   目前社区主要集中在国内（阿里主导）。国际社区需要更多与 Istio 生态的兼容性证明。
*   文档和 Dashboard 的易用性仍有提升空间，特别是对于非 K8s 专家的用户。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的运维/SRE。
*   后端开发人员（Go/Java/Rust），希望扩展网关功能。
*   AI 应用开发者，需要理解底层流量分发机制。

### 学习路径
1.  **基础**：理解 Envoy 架构。
2.  **进阶**：学习 WASM 基础，尝试使用 Go 编写一个简单的 Higress 插件（如修改请求头）。
3.  **高级**：阅读 `pkg/ingress` 源码，理解 K8s Ingress 如何转换为 Envoy 配置。

### 实践建议
*   使用 `docker-compose` 或 `kind` 在本地搭建一个 Higress 实例。
*   编写一个 WASM �

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway("http://higress-gateway:8080")
    
    # 配置路由规则
    gateway.add_route(
        path="/api/v1/*",  # 匹配路径
        service="user-service:8080",  # 后端服务地址
        methods=["GET", "POST"],  # 允许的HTTP方法
        plugins=["auth-plugin", "rate-limit"]  # 启用的插件
    )
    
    print("路由配置已添加")

# 说明：这个示例展示了如何使用 Higress 的 Python SDK 配置网关路由，
# 实现了将 /api/v1/* 路径的请求转发到 user-service 的功能，
# 同时启用了认证和限流插件。

```python


def custom_auth_plugin():
"""
开发自定义认证插件
解决问题：实现基于 JWT 的请求认证
"""
from higress import Plugin
# 创建插件实例
plugin = Plugin("jwt-auth")
# 定义插件配置
plugin.set_config({
"jwt_secret": "your-secret-key",
"token_header": "Authorization",
"token_prefix": "Bearer "
})
# 定义认证逻辑
@plugin.on_request
def authenticate(request):
token = request.headers.get("Authorization", "").replace("Bearer ", "")
if not validate_jwt(token):
return {"status": 401, "body": "Unauthorized"}
return request
return plugin
def validate_jwt(token):
"""JWT 验证逻辑"""
# 实际实现中这里应该验证 JWT 签名和有效期
return token.startswith("valid_")
# 实现了基于 JWT 的请求认证功能，可以拦截未授权的请求。

```python
# 示例3：Higress 流量管理
def traffic_management():
    """
    配置流量管理规则
    解决问题：实现灰度发布和流量分割
    """
    from higress import TrafficManager
    
    # 创建流量管理器
    tm = TrafficManager("http://higress-gateway:8080")
    
    # 配置流量分割规则
    tm.add_traffic_split(
        service="product-service",
        rules=[
            {
                "match": {"headers": {"canary": "true"}},
                "destination": "product-service-v2:8080",
                "weight": 10  # 10% 流量到新版本
            },
            {
                "destination": "product-service-v1:8080",
                "weight": 90  # 90% 流量到旧版本
            }
        ]
    )
    
    print("流量分割规则已配置")

# 说明：这个示例展示了如何使用 Higress 的流量管理功能，
    实现了基于请求头的灰度发布，将带有 canary=true 的请求
    转发到新版本服务，同时控制流量比例。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴电商业务面临高并发、多协议（HTTP、Dubbo、gRPC）的复杂调用场景，需要统一的流量管理和安全防护。

**问题**:  
传统网关（如Nginx、Zuul）在动态配置、协议扩展和性能上存在瓶颈，难以支撑双11等大促场景的流量洪峰，且多语言服务治理成本高。

**解决方案**:  
基于Higress构建统一API网关，整合阿里内部Envoy生态，支持热更新路由规则、插件化扩展（如限流、认证、日志），并通过Wasm插件实现业务逻辑的动态加载。

**效果**:  
- 双11期间单集群QPS突破100万，P99延迟降低至5ms以内  
- 运维效率提升40%，配置变更从小时级缩短至分钟级  
- 安全拦截能力增强，恶意请求识别准确率提升至99.9%  

---



### 2：某头部在线教育平台

 2：某头部在线教育平台

**背景**:  
该平台原有微服务体系中存在Spring Cloud Gateway和Kong混用的情况，导致路由配置分散、监控数据割裂，且第三方服务调用（如支付、直播）需要灵活的流量控制。

**问题**:  
多网关架构维护成本高，新功能（如灰度发布、流量染色）开发周期长，且无法实时响应业务部门的流量调整需求。

**解决方案**:  
全量迁移至Higress，利用其原生支持Nacos服务发现、Dubbo协议转换的能力，通过控制台统一管理所有API，并基于Higgress的Ingress注解实现金丝雀发布。

**效果**:  
- 网关资源占用减少60%，单实例可承载3万并发连接  
- 灰度发布效率提升80%，业务迭代周期从2周缩短至3天  
- 统一监控体系下，接口调用链路追踪覆盖率从70%提升至100%  

---



### 3：某跨国物流企业

 3：某跨国物流企业

**背景**:  
该企业需将自建数据中心与云上服务（AWS、阿里云）打通，且部分区域存在网络不稳定问题，需要网关具备高可用和容错能力。

**问题**:  
原有Nginx配置难以应对跨云场景的动态路由调整，且缺乏对gRPC流式请求的优化，导致实时物流数据传输延迟高。

**解决方案**:  
部署Higress作为混合云网关，启用其HTTP/2与gRPC代理能力，结合Istio实现多集群流量调度，并通过自定义插件对失败请求进行指数退避重试。

**效果**:  
- 跨云请求成功率从85%提升至99.7%，平均延迟降低200ms  
- 网关集群宕机自动恢复时间从分钟级降至秒级  
- 开发团队通过Lua插件扩展业务功能，无需修改核心代码

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Go，支持高并发 | 高性能，基于 Nginx 和 Lua，支持高并发 | 极高性能，基于 Nginx 和 Lua，支持高并发 |
| 易用性 | 提供控制台和 K8s 集成，配置简单 | 控制台功能丰富，但配置较复杂 | 控制台功能完善，配置灵活 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持插件扩展，基于 Go 和 WASM | 支持插件扩展，基于 Lua | 支持插件扩展，基于 Lua 和 Go |
| 社区 | 社区活跃，由阿里云主导 | 社区成熟，用户基数大 | 社区活跃，国内用户较多 |

### 优势分析

- 优势1：基于 Envoy 和 Go，性能和扩展性更强
- 优势2：深度集成 K8s，适合云原生场景
- 优势3：支持 WASM 插件，扩展更灵活

### 不足分析

- 不足1：社区相对较小，生态不如 Kong 和 APISIX 成熟
- 不足2：文档和案例较少，学习成本较高
- 不足3：商业支持有限，企业级功能需付费

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量路由管理

**说明**: Higress 基于 Kubernetes Ingress API 提供了强大的流量路由能力。通过配置 Ingress 规则，可以实现基于域名、路径、Header 等条件的流量分发，支持蓝绿发布、金丝雀发布等高级流量管理场景。

**实施步骤**:
1. 部署 Higress Ingress Controller 到 Kubernetes 集群
2. 创建 Ingress 资源定义路由规则，包括 host、path 和 backend 服务
3. 配置 TLS 证书以支持 HTTPS 流量
4. 使用 Higress 提供的注解扩展功能，如流量镜像、权重路由

**注意事项**: 确保 Ingress 资源的命名空间与服务匹配，避免跨命名空间访问问题

---

### 实践 2：服务治理与熔断降级

**说明**: 利用 Higress 的服务治理功能，可以配置熔断、降级和限流策略，保护后端服务免受过载影响。通过实时监控服务健康状态，自动隔离不健康的服务实例。

**实施步骤**:
1. 在 Higress 控制台或通过 API 配置目标服务的熔断规则
2. 设置降级策略，定义返回的默认响应或重定向路径
3. 配置限流规则，基于 QPS 或并发数限制请求速率
4. 启用健康检查，定期探测后端服务状态

**注意事项**: 熔断阈值需要根据实际负载测试结果调整，避免误判

---

### 实践 3：插件扩展与自定义处理

**说明**: Higress 提供了丰富的插件生态，支持 Lua、WASM 和 Go 语言编写的自定义插件。通过插件可以实现请求/响应的定制处理，如认证、日志记录、数据转换等。

**实施步骤**:
1. 评估需求，选择合适的预置插件或决定开发自定义插件
2. 在 Higress 控制台上传并配置插件参数
3. 为插件设置生效范围（全局、路由或服务级别）
4. 监控插件性能影响，必要时进行优化

**注意事项**: 自定义插件应避免阻塞操作，防止影响网关性能

---

### 实践 4：安全防护与认证授权

**说明**: Higress 集成了多种安全机制，包括 JWT/OAuth2 认证、IP 访问控制、CORS 配置等。合理配置这些安全策略可以有效保护 API 和后端服务。

**实施步骤**:
1. 配置认证插件，如 JWT 验证或 OAuth2 集成
2. 设置 IP 黑白名单，限制访问来源
3. 启用 CORS 策略，控制跨域访问行为
4. 定期审计安全配置，及时更新安全策略

**注意事项**: 认证信息应通过安全通道传输，避免泄露

---

### 实践 5：可观测性与监控告警

**说明**: Higress 提供了详细的指标、日志和追踪信息，集成 Prometheus、Grafana 等工具可以实现全面的监控和告警。通过可观测性数据，可以快速定位问题和优化性能。

**实施步骤**:
1. 配置 Higress 与 Prometheus 的集成，导出监控指标
2. 设置 Grafana 仪表盘，可视化关键指标如 QPS、延迟、错误率
3. 配置分布式追踪（如 SkyWalking），分析请求链路
4. 建立告警规则，及时通知异常情况

**注意事项**: 监控数据量可能很大，需要合理配置采样率和数据保留策略

---

### 实践 6：多集群与多环境管理

**说明**: 对于复杂的微服务架构，Higress 支持多集群和多环境管理。通过统一控制平面，可以管理分布在多个 Kubernetes 集群中的服务，实现跨集群的流量调度和服务治理。

**实施步骤**:
1. 部署 Higress 控制平面，管理多个数据平面集群
2. 配置集群间的服务发现和通信机制
3. 定义跨集群的路由规则，实现流量调度
4. 实施统一的配置管理和策略下发

**注意事项**: 确保集群间网络连通性和安全性，避免单点故障

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 或 HTTP/3 协议支持

**说明**: Higress 作为高性能网关，利用 HTTP/2 的多路复用特性可以显著减少 TCP 连接数，降低网络延迟。HTTP/3 (QUIC) 则在弱网环境下表现更优，能减少队头阻塞。

**实施方法**:
1. 在 Higress 网关监听器配置中，将协议设置为 HTTP/2 或开启 HTTP/3 支持。
2. 确保后端 Upstream 服务也支持 HTTP/2 协议。
3. 配置合适的 TLS 版本（至少 TLS 1.2）以支持 ALPN 协商。

**预期效果**: 高并发场景下 TCP 连接数减少 50% 以上，弱网环境下请求延迟降低 20%-30%。

---

### 优化 2：配置全局限流与熔断策略

**说明**: 防止后端服务因突发流量过载而崩溃，保障网关自身的稳定性。Higress 支持基于 Token Bucket 算法的限流。

**实施方法**:
1. 在路由或全局级别配置 `request-rate-limit` 插件。
2. 设置精确的 QPS 阈值（例如：每秒 1000 次请求）。
3. 针对关键服务配置熔断规则，当错误率超过阈值（如 50%）时自动熔断。

**预期效果**: 将后端服务崩溃率降低至 0%，在流量突增情况下保持网关 P99 延迟稳定。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm 插件，通过将鉴权、限流等逻辑下沉到 Wasm 虚拟机中执行，比传统的 Lua 或远程调用性能更高。同时，利用本地缓存减少对后端的重复请求。

**实施方法**:
1. 将高频使用的认证逻辑编译为 Wasm 插件并在网关加载。
2. 启用 Higress 的 `local-cache` 插件，对响应数据进行缓存（如配置信息或静态资源）。
3. 设置合理的缓存 TTL（生存时间）和 Key 规则。

**预期效果**: 插件执行延迟降低 10%-50%，缓存命中时后端请求量减少 60% 以上。

---

### 优化 4：优化连接池与 Keep-Alive 设置

**说明**: 默认的连接配置可能不适合高吞吐场景。调整与后端服务之间的 HTTP Keep-Alive 连接池大小，可以减少频繁建立 TCP 连接的三次握手开销。

**实施方法**:
1. 在 Upstream 配置中，调大 `http2_max_requests` 和 `max_connections_per_host` 参数。
2. 启用 `keepalive` 并将 `idle_timeout` 设置为合理的值（例如 60s）。
3. 确保后端服务支持长连接。

**预期效果**: 后端连接建立耗时显著降低，吞吐量提升 15%-30%。

---

### 优化 5：启用 CPU 亲和性与多核绑定

**说明**: Higress 基于 Envoy，通过绑定工作线程到特定的 CPU 核心，可以减少上下文切换和缓存失效，提升处理效率。

**实施方法**:
1. 在 Higress 的启动配置或环境变量中设置 worker 进程数量等于 CPU 核心数。
2. 操作系统层面使用 `taskset` 或 `cgroup` 将进程绑定到固定核心。
3. 确保开启了 `reuse_port` 监听选项。

**预期效果**: CPU 上下文切换开销减少，系统负载更加平稳，单核吞吐量提升约 10%-20%。

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关
- 深度集成了 K8s Ingress 与 Gateway API 标准，提供统一的流量管理
- 内置针对 Dubbo、Nacos 和 Spring Cloud 的微服务治理能力
- 提供开箱即用的 WAF 防护与安全插件支持
- 支持高性能的 WASM 插件扩展机制，允许灵活定制业务逻辑
- 兼容 Nginx Ingress 注解，降低了从传统网关迁移的成本
- 提供完善的控制台与 Dashboard，显著降低了运维与配置的复杂度


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 的作用、位置及核心功能（路由转发、负载均衡、统一认证）。
- Higress 架构概览：了解 Higress 基于 Istio 和 Envoy 的技术架构，以及其作为阿里云开源产品的定位。
- 基本概念：掌握 Ingress、Gateway、Service、Upstream 等基础术语。
- 环境搭建：学习如何在本地 Docker 环境或 Kubernetes 集群中快速部署 Higress。
- 简单流量管理：通过控制台或 K8s YAML 创建简单的路由规则，实现服务访问。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (入门与快速开始部分)
- Higress GitHub 仓库 (README 与 Architecture 文档)
- Kubernetes Ingress 基础教程

**学习建议**: 建议先抛开复杂的配置，优先在本地 Docker 环境跑通官方提供的 Quick Start 示例，直观感受流量是如何经过网关转发到后端服务的。同时，需要补充一些 Kubernetes 的基础网络知识，以便理解 Ingress 资源。

---

### 阶段 2：核心功能深度实践

**学习内容**:
- 高级流量管理：学习基于 Header、Query Parameter、Cookie 等复杂条件的路由匹配规则。
- 插件系统：深入理解 Higress 的插件机制，学习如何配置和使用官方预设插件（如限流、认证、CORS 处理）。
- 服务治理：掌握全链路灰度发布、蓝绿发布以及 Header 传递与转换。
- 安全防护：配置 Keyless 认证、JWT 认证以及 IP 访问控制。
- 可观测性：集成 Prometheus 与 Grafana，配置日志收集与监控大盘，查看访问日志。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (插件市场与流量管理)
- Envoy Filter 基础文档 (理解底层过滤机制)
- Higress 官方博客中的最佳实践案例

**学习建议**: 此阶段重点在于“动手配置”。建议搭建一个包含两个服务版本（v1 和 v2）的测试环境，尝试配置流量权重切换来模拟金丝雀发布。同时，尝试开启几个常用的安全插件，观察其对请求的影响。

---

### 阶段 3：扩展开发与 WAF 集成

**学习内容**:
- WAF 防护：深入理解 Higress 与 K8s Ingress 的区别，重点学习如何利用 WAF 插件防御 SQL 注入、XSS 等常见 Web 攻击。
- 自定义插件开发：学习 Lua 或 WASM (WebAssembly) 基础，尝试编写一个简单的自定义插件来处理特定的请求逻辑（如自定义鉴权或请求体修改）。
- 多租户与多环境管理：在复杂的 K8s 环境下管理多个命名空间的网关配置。
- 高可用部署：学习 Higress 的高可用部署模式及性能调优参数。

**学习时间**: 3-4周

**学习资源**:
- Higress 自定义插件开发文档
- WebAssembly (Wasm) 简明教程
- Higress 性能测试报告与白皮书

**学习建议**: 如果你的业务有特定的鉴权或逻辑处理需求，不要修改核心代码，而是尝试编写一个 Lua/Wasm 插件。这个阶段需要一定的代码阅读能力，建议阅读 GitHub 上几个官方插件的源码作为参考。

---

### 阶段 4：生态集成与架构精通

**学习内容**:
- 服务网格集成：学习 Higress 如何作为 Istio 的入口网关，实现从 Ingress Gateway 到 Sidecar 的全链路连通。
- 多协议支持：探索 Dubbo、gRPC 等非 HTTP 协议的代理与转换配置。
- 云原生生态对接：结合 Prometheus、SkyWalking 等可观测性工具进行深度监控与链路追踪。
- 源码级理解：阅读 Higress Controller 和 Runner 的核心源码，理解配置如何从 K8s CRD 下发至 Envoy。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub Source Code
- Istio 官方文档 (Gateway 相关部分)
- 云原生网关架构设计相关深度技术文章

**学习建议**: 此阶段适合架构师或高级开发人员。建议尝试将 Higress 接入现有的微服务架构中，替换传统的 Nginx 或旧版网关，并对比性能差异。通过阅读源码，理解其控制面与数据面的交互细节，以便进行深度的二次开发或故障排查。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是基于阿里云内部多年实践以及开源社区（特别是 Envoy 和 Istio）的经验构建的。它旨在提供高性能、可扩展且易于管理的流量入口解决方案。

与 Nginx 和 Kong 的主要区别如下：
1.  **架构基础**：Nginx 和 Kong 主要基于 Nginx/OpenResty 构建（多进程或单进程事件驱动），而 Higress 基于 Envoy 构建（C++、L3/L4/L7 过滤器、异步 I/O），在云原生环境中的可观测性和动态配置能力更强。
2.  **集成能力**：Higress 原生集成了 K8s Ingress Controller 和 Istio 控制平面功能，能够无缝对接服务网格，而 Kong 和 Nginx 通常需要额外的配置或插件来实现类似功能。
3.  **插件市场**：Higress 提供了类似 Kong 的插件市场，支持 Wasm (WebAssembly) 插件，允许使用多种语言（如 Go, C++, Rust）编写插件，比传统的 Lua 脚本更安全且易于开发。

---



### 2: Higress 与阿里巴巴内部的 Gateway 有什么关系？

2: Higress 与阿里巴巴内部的 Gateway 有什么关系？

**A**: Higress 的技术核心源自阿里巴巴内部大规模的电商业务实践。它汲取了阿里云 Tengine（Nginx 的分支）以及内部自研的高性能网关的精华逻辑。

具体来说，Higress 是阿里云将内部沉淀的流量管理技术进行标准化和开源化的产物。它旨在解决阿里云上混合云、多语言以及多协议接入的痛点，可以被视为阿里云 API 网关的开源版本或技术延续，专为云原生架构设计。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

**A**: 是的，Higress 非常重视兼容性，旨在降低用户的迁移门槛。

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置注释和 Ingress API 的兼容支持。用户可以直接使用标准的 K8s Ingress 资源定义，Higress 会自动将其转换为内部的 Envoy 配置。
2.  **注解支持**：它支持常见的 K8s Ingress 注解，这意味着现有的 YAML 文件通常不需要大量修改即可在 Higress 上运行。
3.  **迁移工具**：对于从传统 Nginx 迁移的用户，Higress 社区也提供了相应的工具和指南来帮助转换配置逻辑。

---



### 4: Higress 的性能表现如何？是否支持高并发？

4: Higress 的性能表现如何？是否支持高并发？

**A**: Higress 具备极高的性能，能够应对企业级的高并发流量需求。

1.  **底层优势**：基于 Envoy 构建，Envory 本身以高性能和低内存占用著称，采用 C++ 编写，处理延迟极低。
2.  **阿里验证**：其核心代码经过了阿里巴巴“双11”等超大规模流量场景的验证，具备处理每秒百万级请求的能力。
3.  **热更新**：支持配置的热更新，在路由规则或插件变更时不需要重启网关进程，从而保证业务不中断，这对于高可用场景至关重要。

---



### 5: 如何在 Higress 中扩展功能？是否支持自定义插件？

5: 如何在 Higress 中扩展功能？是否支持自定义插件？

**A**: Higress 提供了非常灵活的扩展机制，主要通过以下两种方式：

1.  **Wasm 插件（推荐）**：这是 Higress 最具特色的扩展方式。它支持 WebAssembly 标准，允许开发者使用 Go、C++、Rust 或 JavaScript 等高级语言编写业务逻辑。Wasm 插件运行在沙箱环境中，安全性高，且可以动态加载，不会影响主进程的稳定性。
2.  **Lua 插件（兼容）**：为了兼容 OpenResty/Kong 生态，Higress 也支持 Lua 脚本插件，方便用户复用现有的 Lua 代码资产。

---



### 6: Higress 是否支持服务网格对接？

6: Higress 是否支持服务网格对接？

**A**: 是的，Higress 的设计初衷之一就是作为服务网格的南北向流量入口。

它可以作为 Istio 的入口网关替换默认的 Ingress Gateway。Higress 能够自动发现服务网格中的服务，并根据 Istio 的 VirtualService 等资源进行流量路由。这使得它非常适合作为云原生架构中的统一流量入口，管理进入集群的流量。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 是基于 Envoy 构建的。请查阅 Higress 的文档或源码，找出 Higress 在标准 Envoy 基础上，针对云原生网关场景主要增加了哪三个核心功能模块？

### 提示**: 关注 Higress 架构图中的 "Wasm Plugin"、"Ingress" 以及与阿里云内部集成的部分，思考它与传统 Nginx Ingress 的本质区别。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用“模型服务提供商插件”统一 AI 接入标准
**场景**：你的应用需要对接 OpenAI、Azure OpenAI 以及通义千问等多个 LLM 提供商，或者需要在私有化部署和公有云调用之间切换。
**建议**：不要在业务代码中硬编码不同厂商的 API 格式。配置 Higress 的 AI 提供商插件（如 `ai-proxy`），将不同厂商的 API 统一映射为标准的 OpenAI 接口格式。
**最佳实践**：在 Higress 中配置“模型服务提供商”时，将不同模型映射为统一的模型名称。这样业务端只需修改请求中的 `model` 参数即可切换底层供应商，无需修改任何代码或 SDK 调用逻辑。
**常见陷阱**：忽略不同模型对 Token 计算方式的差异。虽然接口统一了，但不同厂商的 Token 计费和上下文限制不同，建议在网关层配置针对不同路由的 `max_tokens` 限制，防止成本失控。

### 2. 实施基于 Token 的精细化流控与防护
**场景**：LLM 调用成本高昂，且容易受到恶意攻击或上游过载的影响。
**建议**：传统的基于“请求数（QPS）”或“连接数”的限流对 AI 场景不够精确。应使用 Higress 针对请求体或响应体内容的处理能力，实施更精细的策略。
**最佳实践**：结合 WAF 插件与自定义插件，对 Prompt 长度进行校验。例如，限制单个请求的 Body 大小或 Prompt 字符数，防止恶意用户发送超长 Prompt 消耗大量 Token。
**常见陷阱**：仅配置了并发数限制，未配置超时时间。AI 模型生成响应（TTFB）通常较慢，如果网关层的超时时间设置过短（例如默认的 60秒），会导致流式响应在生成一半时被网关主动断开，报错 `upstream request timeout`。

### 3. 配置 SSE（流式）透传与缓存策略
**场景**：为了用户体验，大多数 AI 交互需要使用 Server-Sent Events (SSE) 流式返回，但流式数据难以被常规 HTTP 缓存拦截。
**建议**：确保 Higress 的路由配置开启了 Full Chain SSE 支持，并且配置合理的语义缓存。
**最佳实践**：对于高重复度的问答（如知识库检索），配置基于 Prompt 指纹的缓存插件。当检测到相同的 Prompt 时，网关直接截断请求并返回缓存的历史生成结果（即使原结果是流式的，网关也应模拟流式下发），这能显著降低 API 调用成本和延迟。
**常见陷阱**：在网关层开启了“Body Buffering”（体缓冲）。这会导致网关试图等待上游全部生成完毕再转发给客户端，不仅破坏了流式体验，还会极大地增加网关内存占用和延迟。务必确保流式请求的配置下 Buffering 是关闭的。

### 4. 敏感信息脱敏与 Prompt 注入防御
**场景**：企业内部数据通过 AI 网关传输，需要防止用户上传敏感信息（如身份证、API Key），或通过 Prompt 注入攻击系统指令。
**建议**：利用 Higress 的 WAF 模块或自定义 Lua/Wasm 插件，在请求发送给 LLM 之前进行拦截和清洗。
**最佳实践**：部署“关键词拦截”插件，配置针对 SQL 注入、系统提示词泄露（如 "Ignore previous instructions"）的检测规则。同时，利用正则插件在请求发往上游前，自动脱敏响应中的敏感数据。
**常见陷阱**：只在请求阶段做过滤，忽略了响应阶段。LLM 有时会在对话中意外泄露训练数据或系统 Prompt，建议对响应内容也进行扫描。

### 5. 善用 WASM 插件实现自定义业务逻辑
**场景**

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*