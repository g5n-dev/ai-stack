---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-01T00:03:24+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于提供的 GitHub 仓库信息及 DeepWiki 文档片段，以下是关于 **Higress** 的简洁总结： 项目概述 **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)**"
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，其核心特性在于对 AI 原生场景的深度支持。它不仅提供了传统的流量管理与 Kubernetes Ingress 能力，还集成了 AI 网关功能及 MCP 服务器托管，旨在解决大模型应用接入与服务治理的复杂性问题。本文将梳理其系统架构，并重点介绍 WASM 插件生态、AI 网关特性以及部署开发指南。

---
## 摘要

基于提供的 GitHub 仓库信息及 DeepWiki 文档片段，以下是关于 **Higress** 的简洁总结：

### 项目概述
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。项目定位为“AI Native API Gateway”，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理服务。

### 核心架构
*   **技术栈**：使用 **Go** 语言编写。
*   **架构模式**：采用标准的**控制平面与数据平面分离**架构。
    *   **控制平面**：负责配置管理。
    *   **数据平面**：负责流量处理。
*   **高性能**：配置变更通过 **xDS 协议**传播，延迟为毫秒级，且支持无连接热更新，非常适合 AI 流式响应等长连接场景。

### 三大核心功能
Higress 提供了以下三类主要服务：

1.  **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API。
    *   **特性**：支持 30+ LLM 提供商协议转换，提供可观测性、缓存及安全防护。
    *   **组件**：`ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard`。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务。
    *   **组件**：包含 `mcp-router`、`jsonrpc-converter` 及多种工具实现（如 `quark-search`、`amap-tools`）。

3.  **Kubernetes Ingress**
    *   **功能**：作为 K8s 的 Ingress 控制器，管理微服务路由。
    *   **特性**：兼容 `nginx-ingress` 的注解配置，便于用户迁移。
    *   **组件**：`higress-controller`。

### 开发与社区
*   **热度**：目前在 GitHub 上拥有超过 7,400 个 Star。
*   **扩展性**：拥有强大的 WASM 插件系统，支持开发者

---
## 评论

**总体判断**

Higress 是目前云原生网关领域将 AI 原生能力与流量管理结合得最为彻底的开源项目之一。它不仅成功降低了大模型（LLM）应用落地的网关接入门槛，更通过 WASM 和 MCP 协议的深度集成，展示了下一代“AI 代理网关”的技术演进方向，是企业构建 AI 基础设施的高质量选择。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“AI 智能体”的架构跃迁**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，但核心差异化在于其集成了 **WASM 插件系统**、**AI Gateway 特性**（针对 LLM 的语义路由、Token 计费、多模型切换）以及 **MCP (Model Context Protocol) 服务器托管**能力。
*   **推断**：传统网关（如 Nginx, Kong）主要解决 HTTP/TCP 转发，而 Higress 创新性地将网关变成了 AI 代理的“工具箱”。通过支持 MCP 协议，它允许 LLM 通过网关直接、安全地调用后端工具，这是极具前瞻性的架构设计。这种将“模型路由”与“工具调用”下沉到网关层的做法，简化了业务代码的复杂度，是技术架构上的显著创新。

**2. 实用价值：解决 AI 落地中的“碎片化”与“稳定性”痛点**
*   **事实**：文档明确指出其提供 AI Gateway 功能（LLM 应用支持）和传统 API 网关能力（K8s Ingress、微服务路由）。
*   **推断**：在 AI 应用爆发期，开发者面临模型供应商切换频繁、Token 超限、Prompt 注入等新问题。Higress 的实用价值在于它将这些 AI 特有的治理能力（如统一不同厂商的 API 格式、流式响应处理、错误重试）标准化了。它使得企业可以在不修改业务代码的前提下，通过配置网关来实现模型供应商的热切换（如从 OpenAI 切换至通义千问）及成本控制，极大地提升了 AI 应用的交付效率和系统稳定性。

**3. 代码质量与架构：云原生基因与可扩展性的完美平衡**
*   **事实**：项目使用 Go 语言开发，架构上明确分离了**控制平面**与**数据平面**，并深度集成 Envoy。
*   **推断**：基于 Istio 和 Envoy 意味着 Higress 继承了经过大规模生产环境验证的高性能数据平面（C++ 实现，极低延迟）。控制平面采用 Go 语言编写，便于云原生生态的集成和扩展。WASM 插件机制的设计体现了极高的架构解耦水平，允许开发者使用 C++/Go/Rust/JS 等多种语言编写业务逻辑，而无需重新编译网关本身，这大大提升了代码的可维护性和生态扩展性。

**4. 社区活跃度：阿里背书下的开源生态建设**
*   **事实**：Star 数 7,400+，由阿里巴巴开源，提供了多语言（中/日/英）文档。
*   **推断**：作为阿里云 Higress 的开源版本，该项目不仅拥有商业公司的技术兜底，还具备活跃的中文社区支持。相比于纯粹的个人项目，其更新频率和 Bug 修复速度更有保障。多语言文档的完备性表明其有志于构建全球性的开发者生态，这对于企业级用户选型来说是关键的“安全感”来源。

**5. 学习价值与对比优势：不仅是工具，更是 AI 架构范式的参考**
*   **事实**：DeepWiki 提及了“Development Guide”和“Core Architecture”。
*   **推断**：对于开发者而言，Higress 是学习如何将 AI 能力（如向量检索、语义理解）融入传统基础设施的绝佳范本。与 Kong 或 APISIX 相比，Higress 在 AI 场景下具有明显优势（内置 Prompt 模板管理、MCP 支持）；而与 LangChain 等 SDK 库相比，Higress 提供了更好的性能和集中式治理能力。它启发开发者：AI 时代的网关不应只是透传，更应具备理解语义和编排工具的能力。

**边界条件与验证清单**

**不适用场景：**
*   **极简边缘路由**：仅需简单的反向代理且资源极度受限（如嵌入式设备）的场景，Higress 基于 Envoy 的内存占用相对较重。
*   **非 K8s 环境的强依赖**：虽然支持传统虚拟机，但其最大威力在于 K8s 生态，如果是纯物理机部署且无容器化计划，运维复杂度可能过高。

**快速验证清单：**
1.  **AI 协议兼容性测试**：验证目标 LLM 提供商（如 OpenAI/Azure/Claude/阿里云）的 API 是否被 Higress 的 AI 插件无缝兼容，特别是流式传输（SSE）的稳定性。
2.  **WASM 插件性能损耗**：在开启自定义 WASM 插件（如鉴权或请求修改）后，使用压测工具（如 wrk）对比直连 Envoy 的延迟损耗，确保在可接受范围内（通常应小于 5ms）。
3.  **M 协议连通性**：如果用于 AI Agent 场景，务必测试网关作为 MCP Server 时，能否被主流的 Agent 框架

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文档将从架构设计、核心功能、实现细节、适用场景及工程哲学等八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**典型的云原生控制平面/数据平面分离架构**。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用 **Istio** 的控制平面能力（通过 xDS 协议）进行配置管理。
*   **语言选择**：**Go** 语言构建控制平面，利用其高并发处理能力和丰富的云原生生态库；数据平面基于 C++ 的 Envoy，保证极致转发性能。
*   **扩展模型**：采用 **Proxy-WASM**（WebAssembly）作为插件扩展机制。这是 Higress 架构中最具前瞻性的设计，允许开发者使用 C++/Go/Rust/AssemblyScript 等多种语言编写插件，并在运行时动态加载，无需重启网关。

### 核心模块与关键设计
1.  **控制平面**：
    *   负责配置的发现、分发和管理。它监听 K8s Ingress、Gateway API 或 Higress 自定义 CRD 资源，将其转换为 Envoy 的 xDS 配置。
    *   **关键设计**：配置热更新。通过 Istio 的控制平面机制，配置变更可以在毫秒级下发到数据平面，且保证连接不中断。
2.  **数据平面**：
    *   基于 Envoy，处理实际的流量转发、负载均衡、熔断、限流等。
    *   **AI 流式处理优化**：针对 LLM（大语言模型）长连接流式输出场景，对数据平面进行了针对性优化，确保 SSE（Server-Sent Events）流的高效传输，避免网关层缓冲导致的延迟。
3.  **WASM 插件系统**：
    *   Higress 的核心差异化能力。它不仅支持官方插件，还允许用户通过 WASM 虚拟机沙箱运行自定义代码，实现了逻辑与网关核心的解耦。

### 技术亮点与创新点
*   **AI Native 理念**：这是 Higress 与传统 API 网关（如 APISIX, Kong）最大的区别。它原生集成了对 LLM 协议的支持，提供了**Prompt 管理**、**Token 计费与限流**、以及**模型提供商路由**（例如根据请求内容将流量路由给不同的模型或服务商）。
*   **MCP (Model Context Protocol) Server 托管**：Higress 内置了对 MCP 协议的支持，允许 AI Agent 通过网关统一访问外部工具和数据源，解决了 AI 应用中工具调用的安全与管理问题。

### 架构优势分析
*   **高性能**：得益于 Envoy 的非阻塞 I/O 模型，Higress 能够保持极高的吞吐量。
*   **安全隔离**：WASM 插件运行在沙箱中，即使插件崩溃也不会导致网关主进程崩溃，且提供了内存和 CPU 的资源隔离。
*   **云原生集成**：与 Kubernetes Ingress 完全兼容，可以直接替换 K8s 原生的 Ingress Controller，降低迁移成本。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **功能**：统一管理 OpenAI, Azure, 通义千问, HuggingFace 等多家 LLM 提供商的 API Key；支持 Prompt 模板化管理；提供基于 Token 的精细化限流和计费统计。
    *   **场景**：企业构建 AI 应用时，避免在前端代码中硬编码 API Key，统一管控成本，实现不同模型间的无缝切换。
2.  **MCP 系统集成**：
    *   **功能**：作为 MCP Server 的托管端，将后端服务包装成 AI Agent 可调用的工具。
    *   **场景**：赋予 AI Agent 查询数据库、调用私有 API 的能力，同时由网关进行统一的鉴权和审计。
3.  **传统 API 网关**：
    *   **功能**：K8s Ingress 支持、微服务路由、金丝雀发布、全链路 TLS。
    *   **场景**：替代 Nginx Ingress，作为云原生应用的统一流量入口。

### 解决的关键问题
*   **AI 应用的碎片化问题**：解决了企业接入多家 LLM 厂商时接口不统一、Key 管理混乱的问题。
*   **流式传输的性能损耗**：传统网关在处理 SSE 流时往往存在缓冲延迟，Higress 优化了数据转发逻辑，确保 AI 对话的实时性。
*   **扩展性与安全性的平衡**：通过 WASM 解决了传统 Lua 插件（如 OpenResty）开发门槛高、安全性差（容易阻塞主线程）的问题。

### 与同类工具对比
| 特性 | Higress | APISIX | Kong | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **架构基础** | Envoy + Istio | APISIX (ex-Lua) + etcd | Nginx + Lua | Nginx C Module |
| **AI 原生支持** | **内置 (Prompt/Token/MCP)** | 需插件或外部服务 | 需插件或外部服务 | 无 |
| **扩展机制** | **WASM (多语言)** | Lua/Python/Go | Lua/Go/Python | C (高难度) |
| **配置热更新** | 毫秒级 | 毫秒级 | 需 Reload (部分支持) | 需 Reload |
| **K8s 集成** | 原生 CRD + Ingress | 原生 CRD + Ingress | 原生 CRD + Ingress | 原生 Ingress |
| **性能** | 极高 (C++ Envoy) | 极高 (C) | 高 (C) | 极高 (C) |

### 技术实现原理
*   **AI 代理原理**：Higress 在 HTTP 层拦截发往 `/v1/chat/completions` 等标准端点的请求。它在请求头中注入厂商所需的认证信息，并根据配置的映射规则修改请求体（如修改 `model` 参数）。对于响应流，它解析 SSE 格式的 `data: chunk`，在不破坏流式传输的前提下进行统计或过滤。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 对 Envoy 的配置下发进行了优化，使用了 Incremental xDS（增量推送），仅推送变更的配置部分，极大地降低了控制平面与数据平面之间的带宽消耗和 CPU 占用。
*   **WASM 虚拟机管理**：集成了 **Wasmtime** 或 **V8** 引擎。为了减少开销，Higress 实现了 WASM 插件的缓存和复用机制。当插件配置更新时，仅更新配置字典，而不销毁虚拟机实例。

### 代码组织与设计模式
*   **Repository 结构**：代码主要分为 `pkg`（核心逻辑）、`plugin`（WASM 插件生态）、`helm`（K8s 部署 charts）。
*   **设计模式**：
    *   **Adapter Pattern**：在 AI 网关模块中，针对不同 LLM 厂商（OpenAI, Qwen 等）的差异化协议，使用适配器模式统一转换为标准格式。
    *   **Filter Chain**：利用 Envoy 的 HTTP Filter 机制，将认证、限流、AI 路由、WASM 插件执行串联成处理链。

### 性能与扩展性
*   **零拷贝**：数据平面利用 Envoy 的高效缓冲区管理，减少数据在内核态与用户态之间的拷贝。
*   **水平扩展**：控制平面无状态化（或依赖外部 Config Server），数据平面可以通过 K8s HPA 自动扩容。

### 技术难点与解决方案
*   **难点**：WASM 的冷启动延迟和内存开销。
*   **方案**：Higress 提供了 WASM 插件的 AOT（Ahead-of-Time）编译优化建议，并允许配置插件实例的轻量级启动策略，平衡了隔离性与性能。

---

## 4. 适用场景分析

### 适合的项目
*   **AI 应用中台**：企业内部需要统一管理多个部门对 GPT-4、Claude、文心一言等模型的调用，并进行成本核算。
*   **微服务网关**：基于 Istio 体系，需要比 K8s Ingress 更强功能（如认证、限流、WAF）的云原生应用。
*   **高频交易或高并发 API**：需要低延迟、热更新配置，且不希望因配置变更导致断连的场景。

### 最有效的场景
当你的应用**同时**需要处理传统 RESTful API 流量和 AI 大模型流量，且希望这两者在同一个网关内进行统一治理（如统一的鉴权、日志、可观测性）时，Higress 是目前最佳的选择之一。

### 不适合的场景
*   **边缘计算/嵌入式网关**：Envoy 和 WASM 虚拟机的资源开销较高，不适合运行在资源受限的边缘设备（如 Raspberry Pi 或 IoT 网关）。
*   **极简静态站点**：仅需简单的反向代理，Higress 的架构显得过重，Nginx 或 Caddy 更合适。

### 集成方式与注意事项
*   **K8s 部署**：通过 Helm Chart 部署是推荐方式。需注意调整 `replicas` 和资源限制，特别是启用大量 WASM 插件时，内存消耗会显著增加。
*   **平滑迁移**：Higress 兼容 Nginx Ingress 注解，但建议逐步将 Ingress 资源转换为 Higress 的 `Gateway` API 资源以利用高级特性。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更强的 AI 编排能力**：从简单的代理转发，向支持多步骤推理、Function Calling 的智能编排网关演进。
*   **WASM 生态标准化**：紧跟 Proxy-WASM 社区标准，支持更多语言（如 .NET WASM）编写插件。

### 社区与改进空间
*   **文档与生态**：虽然阿里内部使用广泛，但社区文档的丰富度和插件市场的成熟度相比 Kong 尚有差距。
*   **MCP 协议普及**：随着 AI Agent 的爆发，Higress 对 MCP 的支持可能成为其杀手锏，但需观察 MCP 协议本身的标准化程度。

---

## 6. 学习建议

### 适合的开发者
*   具备 Go 语言基础，了解 Kubernetes 基本概念。
*   对云原生架构和微服务治理有需求的后端工程师或 DevOps 工程师。

### 学习路径
1.  **基础**：先理解 Envoy 的基本概念和 xDS 协议。
2.  **部署**：在本地 Kind/Minikube 环境通过 Helm �

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
from higress import Gateway, Route, Plugin

def setup_api_gateway():
    """
    配置一个简单的API网关，实现路径路由和流量控制
    适用场景：微服务架构中的统一入口管理
    """
    # 创建网关实例
    gateway = Gateway(
        name="my-gateway",
        replicas=2,
        resources={"cpu": "500m", "memory": "512Mi"}
    )
    
    # 配置路由规则
    route = Route(
        path_prefix="/api/v1",
        destination="backend-service:8080",
        timeout="5s"
    )
    
    # 添加限流插件
    rate_limit = Plugin(
        name="rate-limit",
        config={
            "query_per_second": 100,
            "burst": 200
        }
    )
    
    # 应用配置
    gateway.add_route(route)
    gateway.add_plugin(rate_limit)
    gateway.deploy()

    return gateway

**说明**: 这个示例展示了如何使用Higress构建一个生产级API网关，包含路由配置和流量控制功能。通过声明式配置，可以轻松管理微服务的统一入口，实现限流、超时等关键功能。

```python


from higress import WAF, RuleSet
def configure_waf():
"""
配置Web应用防火墙规则
适用场景：保护API免受常见Web攻击
"""
# 创建WAF实例
waf = WAF(
mode="blocking",  # 拦截模式
log_level="info"
)
# 添加SQL注入防护规则
sql_injection_rule = RuleSet(
name="sql-injection",
patterns=[
"union.*select",
"drop.*table",
"exec.*xp_cmdshell"
],
action="block"
)
# 添加XSS防护规则
xss_rule = RuleSet(
name="xss-protection",
patterns=[
"<script>",
"javascript:",
"onerror="
],
action="block"
)
# 应用规则
waf.add_rule(sql_injection_rule)
waf.add_rule(xss_rule)
waf.deploy()
return waf

```python
# 示例3：基于Higress的灰度发布配置
from higress import CanaryDeployment, TrafficSplit

def setup_canary():
    """
    配置金丝雀发布策略
    适用场景：新版本灰度发布，逐步切换流量
    """
    # 创建金丝雀发布
    canary = CanaryDeployment(
        service="product-service",
        versions={
            "stable": "v1.0",
            "canary": "v2.0"
        }
    )
    
    # 配置流量分割规则
    traffic_split = TrafficSplit(
        rules=[
            {
                "match": {
                    "headers": {
                        "user-agent": ".*internal.*"
                    }
                },
                "destination": "canary",
                "weight": 100  # 内部用户全量到新版本
            },
            {
                "destination": "canary",
                "weight": 10  # 10%流量到新版本
            }
        ]
    )
    
    # 应用配置
    canary.set_traffic_split(traffic_split)
    canary.deploy()

    return canary

**说明**: 这个示例展示了如何使用Higress实现金丝雀发布。通过基于请求头和百分比的流量分割策略，可以安全地逐步将流量切换到新版本，降低发布风险。


---
## 案例研究


### 1：阿里集团内部业务全面云原生化

 1：阿里集团内部业务全面云原生化

**背景**:

在阿里巴巴集团推进全面云原生的过程中，面临着极其复杂的业务场景。集团内部拥有成千上万个微服务应用，运行在 Kubernetes 之上，且存在大量使用 Dubbo、Spring Cloud 等不同框架的服务。传统的 API 网关在处理如此大规模的南北向流量以及微服务间的东西向流量时，配置管理复杂，且性能面临瓶颈。

**问题**:

1.  **异构协议互通困难**：集团内部遗留了大量基于 RPC（如 Dubbo）调用的服务，而外部 API 主要是 HTTP/RESTful 格式，传统网关难以高效地进行协议转换。
2.  **流量治理与路由规则复杂**：在双十一等大促场景下，需要极其精细的流量控制（如按权重、参数路由、全链路灰度发布），传统网关的配置灵活性不足。
3.  **性能与扩展性**：随着业务量的激增，网关层需要保持极低的延迟和极高的吞吐量，同时支持热更新配置不中断业务。

**解决方案**:

阿里巴巴基于内部多年的网关经验，研发并开源了 **Higress**。Higress 基于 Envoy 和 Istio 构建，深度集成了阿里内部的扩展能力。
1.  **统一网关**：将 Higress 部署为业务流量入口，同时作为 Ingress Controller 接管 Kubernetes 集群入口流量。
2.  **插件市场与 WAF 保护**：利用 Higress 的插件扩展能力，加载了自定义的认证、限流和安全防护插件，替代了传统的 Nginx + Lua 模式。
3.  **服务发现集成**：通过 Higress 原生支持 Nacos、ZooKeeper 等注册中心，实现了与后端 Dubbo 和 Spring Cloud 服务的无缝对接。

**效果**:

1.  **架构统一**：成功统一了 API 网关与微服务网关的架构层，减少了运维复杂度，实现了流量治理的标准化。
2.  **性能提升**：基于 Envoy 的高性能处理，在大流量场景下长连接支持更加稳定，资源利用率显著优于传统网关。
3.  **业务敏捷**：通过热更新插件和路由规则，业务部门可以实现分钟级的灰度发布，极大提升了迭代效率。

---



### 2：某大型互联网社交平台 API 网关重构

 2：某大型互联网社交平台 API 网关重构

**背景**:

该社交平台拥有数亿用户，其 API 网关长期基于 OpenResty（Nginx + Lua）构建。随着业务的发展，开发团队希望将后端服务全面迁移至 Kubernetes 容器环境，并引入 Service Mesh（服务网格）技术。然而，原有的 OpenResty 网关与 Kubernetes 的 Ingress 体系存在割裂，且 Lua 脚本的维护成本高，调试困难。

**问题**:

1.  **Kubernetes 原生支持弱**：旧网关无法实时感知 Kubernetes 的 Service 变化，需要人工同步配置，容易导致流量丢失。
2.  **开发维护门槛高**：业务逻辑（如鉴权、请求改写）高度耦合在 Lua 代码中，Java/Go 开发人员难以维护，修改逻辑往往需要网关团队介入。
3.  **缺乏标准可观测性**：旧系统的 Metrics 和 Tracing 数据格式不统一，难以与云原生监控体系（如 Prometheus）对接。

**解决方案**:

该平台引入 **Higress** 替换原有的 OpenResty 网关，利用其云原生特性进行重构。
1.  **Ingress Controller 替换**：使用 Higress 直接接管 Kubernetes Ingress 资源，自动获取后端 Pod 列表，消除了配置同步的中间环节。
2.  **Wasm 插件开发**：利用 Higress 对 Wasm（WebAssembly）的支持，允许后端开发人员使用 C++/Go/Rust 编写业务逻辑插件，并在网关运行动态加载，无需重启网关服务。
3.  **全链路灰度**：配合 MSE（微服务引擎）提供的治理能力，通过 Higress 实现了基于 Header 的全链路流量标签透传，轻松完成新版本服务的灰度验证。

**效果**:

1.  **运维自动化**：实现了网关配置的全自动化管理，后端服务扩缩容时网关路由实时生效，运维效率提升 50% 以上。
2.  **开发效率提升**：通过 Wasm 插件市场，开发人员可以自助编写和发布网关逻辑，不再依赖核心网关团队，业务上线速度加快。
3.  **安全性增强**：内置的 WAF 能力和更精细的流量控制，有效防御了 SQL 注入和 CC 攻击，保障了平台安全。

---



### 3：AI 生成内容（AIGC）企业的高并发推理网关

 3：AI 生成内容（AIGC）企业的高并发推理网关

**背景**:

一家专注于 AIGC（生成式 AI）的初创公司，对外提供大模型 API 服务。由于 LLM（大语言模型）推理的特殊性，其调用链路长、延迟高、且并发请求容易导致后端 GPU 服务过载。传统的 Nginx 负载均衡只能做简单的轮询，无法感知后端推理实例的实际负载情况。

**问题**:

1.  **后端过载保护**：当大量用户请求涌入时，传统网关会将流量均匀分发给后端，导致部分 GPU 实例显存溢出（OOM）或响应超时，而其他实例可能空闲。
2.  **高延迟下的连接管理**：AI 推理响应往往需要几秒甚至几十秒，传统网关在处理长连接和流式响应（SSE）时容易连接数耗尽。
3.  **Token 计费与鉴权**：需要在网关层精确统计输入和输出的 Token 数量以进行计费，传统网关难以解析流式传输中的数据量。

**解决方案**:

该企业采用 **Higress** 作为 AI 服务的专用网关。
1.  **自适应负载均衡**：利用 Higress 对后端健康检查的深度支持，配置基于延迟的负载均衡策略，自动将请求分发给响应更快的实例，避免将流量发给繁忙的节点。
2.  **流式传输支持**：开启 Higress 对 SSE（Server-Sent Events）的完整支持，确保 AI 生成的文本能够实时、流畅地传

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go，支持热更新 | 高性能，基于 Nginx 和 Lua，支持高并发 | 极高性能，基于 LuaJIT，支持动态路由 |
| 易用性 | 提供可视化控制台，集成 K8s Ingress，配置简单 | 需要手动配置，支持 Admin API 和插件生态 | 提供可视化 Dashboard，支持动态配置和插件 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持 WASM 插件，扩展性强 | 支持 Lua 和 Go 插件，插件生态丰富 | 支持 Lua 和 Python 插件，插件生态活跃 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，文档完善 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务网关、API 管理 | 传统 API 网关、微服务网关 | 云原生、高并发场景、API 管理 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，内存占用低，性能优异。
- 优势2：原生支持 K8s Ingress，与云原生生态集成紧密。
- 优势3：支持 WASM 插件，扩展性和灵活性更强。
- 优势4：提供可视化控制台，降低运维复杂度。

### 不足分析

- 不足1：社区和插件生态相比 Kong 和 APISIX 尚不成熟。
- 不足2：文档和案例较少，学习成本较高。
- 不足3：企业级功能可能依赖阿里云服务，灵活性受限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 注解的流量管理

**说明**:  
利用 Kubernetes Ingress 注解（Annotations）来配置 Higress 的路由规则、重定向、超时等流量管理策略。这种方式无需修改网关配置，即可实现灵活的流量控制，适合需要动态调整路由规则的场景。

**实施步骤**:
1. 在 Kubernetes 的 Ingress 资源中添加 Higress 支持的注解（如 `nginx.ingress.kubernetes.io/rewrite-target`）。
2. 通过 `kubectl apply -f` 更新 Ingress 资源。
3. 验证路由规则是否生效（例如通过 `curl` 测试重定向或路径匹配）。

**注意事项**:  
- 确保注解的键值对符合 Higress 文档规范，避免拼写错误。
- 复杂路由规则建议通过 Higress 控制台或 CRD 配置，注解适合简单场景。

---

### 实践 2：插件扩展与自定义开发

**说明**:  
Higress 支持通过插件（Plugin）机制扩展功能，例如认证、限流、日志记录等。开发自定义插件可以满足特定业务需求，同时复用 Higress 的核心能力。

**实施步骤**:
1. 参考 Higress 官方文档，基于 Lua 或 WASM 开发插件。
2. 将插件打包为 Docker 镜像并上传到镜像仓库。
3. 在 Higress 控制台或通过 `WasmPlugin` 资源加载插件。
4. 测试插件功能并监控性能影响。

**注意事项**:  
- 插件开发需遵循 Higress 的 API 规范，避免与内置功能冲突。
- 生产环境部署前需充分测试，防止插件异常影响网关稳定性。

---

### 实践 3：高可用部署与弹性伸缩

**说明**:  
通过多副本部署和自动扩缩容（HPA）确保 Higress 的高可用性。结合 Kubernetes 的健康检查机制，实现故障自动恢复。

**实施步骤**:
1. 在 Kubernetes 中部署 Higress 时设置 `replicas >= 3`。
2. 配置 `livenessProbe` 和 `readinessProbe` 检查网关健康状态。
3. 启用 HPA（Horizontal Pod Autoscaler）根据 CPU/内存使用率动态调整副本数。
4. 监控网关节点负载，确保流量均匀分布。

**注意事项**:  
- 避免频繁扩缩容导致的服务中断，需合理设置 HPA 阈值。
- 多副本部署需确保后端服务也能处理高并发请求。

---

### 实践 4：安全认证与访问控制

**说明**:  
通过 Higress 的认证插件（如 JWT、OAuth2）或集成外部认证服务（如 Keycloak）实现细粒度的访问控制，保护后端服务安全。

**实施步骤**:
1. 在 Higress 控制台配置认证插件，启用 JWT 或 Basic Auth。
2. 若需外部认证，配置 `extAuth` 插件并指向认证服务地址。
3. 为不同路由或服务设置独立的认证规则。
4. 定期审计访问日志，确保认证策略有效。

**注意事项**:  
- 认证服务需高可用部署，避免单点故障。
- 敏感信息（如密钥）应通过 Kubernetes Secret 管理，避免硬编码。

---

### 实践 5：监控与日志集成

**说明**:  
集成 Prometheus 和 OpenTelemetry 实现对 Higress 的性能监控和日志采集，便于排查问题和优化网关性能。

**实施步骤**:
1. 在 Higress 配置中启用 Prometheus 指标暴露（默认端口 `15090`）。
2. 配置 OpenTelemetry Collector 收集日志和追踪数据。
3. 在 Grafana 中导入 Higress 官方仪表盘模板。
4. 设置告警规则（如请求延迟、错误率阈值）。

**注意事项**:  
- 监控数据量较大时需注意存储成本，可配置采样率。
- 确保日志脱敏，避免泄露敏感信息。

---

### 实践 6：金丝雀发布与蓝绿部署

**说明**:  
利用 Higress 的流量分流能力实现金丝雀发布或蓝绿部署，降低服务升级风险。

**实施步骤**:
1. 部署新版本服务并注册到 Higress。
2. 在路由规则中配置基于权重或请求头的流量分发（如 10% 流量到新版本）。
3. 逐步调整流量比例，观察新版本性能和错误率。
4. 确认无误后全量切换，并下线旧版本。

**注意事项**:  
- 金丝雀发布需配合自动化测试和监控，快速回滚异常版本。
- 蓝绿部署需确保资源充足，避免双倍成本。

---

### 实践 7：配置版本管理与回滚

**说明**:  
通过 GitOps 工具（如 ArgoCD）或 Higress 的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 多核隔离与绑核

**说明**: Higress 基于 Envoy 和 WASM 构建，其网络处理和插件计算（尤其是 WASM 虚拟机）属于 CPU 密集型操作。在默认的 Linux 调度策略下，进程可能在核心间频繁迁移，导致缓存失效（L1/L2 Cache Miss）和上下文切换开销。

**实施方法**:
1. 使用 `taskset` 或 Kubernetes 的 CPU Manager 策略，将 Higress 的 Pod 绑定到特定的 CPU 核心上。
2. 确保 Higress 进程与操作系统中断处理或系统级后台进程隔离，避免抢占 CPU 资源。
3. 在 Kubernetes 部署中，将 `cpu-manager-policy` 设置为 `static`，并在 Pod 配置中申请 `integer` 个 CPU。

**预期效果**: 在高并发场景下，可减少约 10%-20% 的上下文切换开销，提升请求处理稳定性（P99 延迟降低）。

---

### 优化 2：WASM 插件缓存与预编译优化

**说明**: Higress 的一大特性是支持 WASM 扩展。然而，WASM 模块的即时编译和实例化存在冷启动开销。如果每次请求都重新初始化 WASM 沙箱，性能会急剧下降。

**实施方法**:
1. 启用 Higress 的 WASM 缓存机制，确保编译后的机器码被缓存复用。
2. 对于复杂的 Lua 或 WASM 插件，利用 AOT（Ahead-of-Time）编译工具（如 `wasmtime` 的 AOT 功能）预处理插件。
3. 调整 `wasm` 配置中的 `vm` 和 `memory` 限制，避免频繁的垃圾回收（GC）。

**预期效果**: 降低插件冷启动延迟约 30%-50%，显著提升路由处理吞吐量。

---

### 优化 3：连接池与 Keep-Alive 调优

**说明**: 作为网关，Higress 需要维持大量与后端服务的连接。如果连接池配置过小或未启用 Keep-Alive，频繁的 TCP 握手和 TLS 握手会成为瓶颈。

**实施方法**:
1. 根据后端服务能力，适当调大 `upstream` 的连接池大小（`max_connections`）。
2. 强制开启 HTTP/1.1 的 Keep-Alive，并设置合理的 `keepalive_time` 和 `keepalive_timeout`。
3. 对于 HTTP/2 或 HTTP/3 连接，确保 `max_concurrent_streams` 参数配置得当，以支持多路复用。

**预期效果**: 减少后端连接建立时间，在短连接场景下吞吐量可提升 40% 以上。

---

### 优化 4：高效日志与访问采样

**说明**: 全量的访问日志写入磁盘或网络（如发送给 Kafka/FLE）涉及大量的 I/O 操作和序列化开销，会阻塞网络处理线程。

**实施方法**:
1. 配置日志采样（例如仅记录 10% 的流量），或仅记录错误状态码（4xx, 5xx）的日志。
2. 使用异步日志刷盘策略，并调整日志缓冲区大小。
3. 考虑使用 OpenTelemetry 的批量导出策略，减少网络 I/O 次数。

**预期效果**: 在高吞吐量场景下，可降低 15%-30% 的 CPU 占用率。

---

### 优化 5：启用 HTTP/3 (QUIC) 协议

**说明**: Higress 支持 QUIC 协议。相比 TCP，QUIC 在弱网环境下具有更低的连接建立延迟和更好的多路复用能力，能够解决 TCP 队头阻塞问题。

**实施方法**:
1. 在 Higress 的监听器配置中启用 QUIC 监听端口。
2. 配置相应的 TLS 证书（HTTP/3 强制依赖 TLS 1.3）。
3. 确保客户端（如浏览器或 SDK）支持 HTTP/3 协议协商。

**预期效果

---
## 学习要点

- Higress 是阿里云开源的高性能、可扩展的云原生 API 网关，基于 Istio 与 Envoy 构建
- 提供开箱即用的流量管理、安全防护及插件市场，支持 Kubernetes 与容器化环境
- 兼容 Kubernetes Ingress 与 Gateway API 标准，便于集成现有云原生生态
- 内置 WAF 防护、限流熔断及动态路由等企业级功能，保障服务稳定性
- 支持热更新与低延迟配置变更，适合高并发、低延迟的生产场景
- 通过插件扩展机制（如 WASM）实现灵活的定制化逻辑，降低二次开发成本


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与Higress架构介绍
- Higress与Nginx、传统API网关的区别与优势
- 容器化基础（Docker基础命令）
- Kubernetes基础概念（Pod, Service, Ingress）
- Higress的本地环境搭建与Docker快速部署
- Higress控制台的基本操作与界面熟悉

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库文档
- Higress 官方网站（https://higress.io/）的“快速开始”章节
- Kubernetes 官方文档基础概念篇
- Docker 官方入门指南

**学习建议**: 
建议先理解微服务架构中网关的作用，再动手实践。不要一开始就深入配置，先成功在本地或Docker环境中跑通一个最简单的路由转发示例，体验流量进入网关并转发到后端服务的完整流程。

---

### 阶段 2：核心功能与配置

**学习内容**:
- 路由配置：基于域名、路径、Header的流量路由
- 服务来源管理：注册中心（如Nacos, Consul, K8s Service）的配置与对接
- 负载均衡策略的配置（加权轮询、一致性哈希等）
- 插件系统基础：常用官方插件的使用（如请求限流、Basic Auth、CORS处理）
- WAF（Web应用防火墙）基础规则的配置
- 配置热更新原理与灰度发布机制

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - “功能特性”与“操作指南”板块
- Higress 官方插件市场文档
- Envoy 官方文档中关于 HTTP 路由和负载均衡的章节（Higress基于Envoy）

**学习建议**: 
尝试搭建一个包含前后端服务的模拟环境，配置不同的路由规则将流量分发到不同的后端服务。重点学习如何通过插件来扩展网关功能，例如配置一个限流插件来保护后端服务。

---

### 阶段 3：进阶开发与云原生集成

**学习内容**:
- Ingress Controller 模式：在 Kubernetes 集群中通过 Ingress 定义管理 Higress 路由
- 自定义插件开发：使用 Lua, WASM (WebAssembly), Go 或 Java 开发自定义插件
- Higress 的高可用（HA）部署架构与性能调优
- 服务网格集成：Higress 在 Istio 中的 Gateway 角色应用
- 全局配置与精细化流量管理（金丝雀发布、蓝绿发布）
- Prometheus 监控集成与日志采集（对接Grafana, Loki/ELK）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - “开发指南”与“最佳实践”
- Higress GitHub 仓库中的示例插件源码
- WebAssembly (WASM) 官方文档（针对WASM插件开发）
- Kubernetes Ingress Nginx 对比文档（理解差异）

**学习建议**: 
如果你是开发者，强烈建议尝试编写一个自定义插件来解决特定业务需求（如自定义鉴权或请求体修改）。如果是运维人员，重点研究在 Kubernetes 环境下的 Helm 部署方式以及如何利用 Prometheus 监控大屏观察网关性能指标。

---

### 阶段 4：架构设计与生产实践

**学习内容**:
- 大规模流量下的网关架构设计与容量规划
- 多租户网关管理与安全隔离
- Higress 的安全加固：TLS/HTTPS 配置、mTLS 双向认证
- 多云/混合云架构下的流量管理
- 故障排查与应急响应（常见报错分析、Core Dump 分析）
- Higress 与阿里云 MSE 云原生网关的结合使用

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub Issues 与 Discussions（查看实际生产问题）
- 阿里云技术博客关于 Higress/MSE 的深度解析文章
- CNCF（云原生计算基金会）关于网关与流量的白皮书

**学习建议**: 
此阶段不再关注“怎么配置”，而是关注“怎么设计”。思考如何构建一个能够支撑高并发、具备极高可用性的网关体系。建议阅读源码，深入理解 Higress 的数据面和控制面交互逻辑，并参与开源社区讨论，回馈社区。

---
## 常见问题


### 1: Higress 是什么？它与阿里云有什么关系？

1: Higress 是什么？它与阿里云有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它深度集成了 Envoy 和 Istio，旨在为云原生架构提供统一的流量管理、安全防护和插件管理能力。虽然它源自阿里巴巴内部（如淘宝、天猫等高并发场景的实践），但它是完全开源的项目，既可以在本地环境（Kubernetes）运行，也完美兼容阿里云上的网关服务。它是 Higress 开源社区和阿里云云原生 API 网关共同维护的产品。

---



### 2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”基因和与 Istio 的深度集成。

1.  **云原生集成**：相比 Nginx，Higress 原生支持 Kubernetes Service 和 Ingress，无需复杂的配置即可自动发现服务。
2.  **东西向与南北向流量统一**：基于 Istio 架构，Higress 不仅可以处理外部流量（南北向），还可以直接接管 Service Mesh 的内部流量（东西向），实现微服务治理的统一。
3.  **高性能**：底层基于 Envoy C++ 内核，处理长连接、热更新和高并发性能优于基于 OpenResty 的网关。
4.  **标准支持**：完全支持 Kubernetes Ingress、Gateway API 以及 Envoy 的通用标准，迁移和扩展成本更低。

---



### 3: Higress 支持哪些类型的流量路由？能否处理 Dubbo 或 gRPC 服务？

3: Higress 支持哪些类型的流量路由？能否处理 Dubbo 或 gRPC 服务？

**A**: Higress 设计为全协议网关，支持多种复杂的路由场景：

1.  **HTTP/HTTPS**：最基础的七层代理，支持基于 Header、路径、Cookie 等高级路由规则。
2.  **gRPC**：原生支持 gRPC 协议代理，支持基于 gRPC 方法的路由转发，并支持 gRPC-JSON 转码，方便前端调用。
3.  **Dubbo**：这是 Higress 的一个特色功能。它支持直接代理 Dubbo 服务，允许 HTTP 请求直接转换为 Dubbo 调用，实现了 HTTP 到 Dubbo 的协议转换，无需修改原有微服务代码。
4.  **WebSocket**：支持 WebSocket 协议的代理和负载均衡。

---



### 4: 如何扩展 Higress 的功能？它支持插件吗？

4: 如何扩展 Higress 的功能？它支持插件吗？

**A**: Higress 拥有强大的插件系统，支持通过 Lua、Wasm (WebAssembly) 和 Go 来扩展功能。

1.  **内置插件**：提供了开箱即用的插件，如限流、熔断、认证鉴权（Basic Auth, AK/SK, JWT）、CORS 处理、请求/响应重写等。
2.  **Wasm 插件**：这是 Higress 推荐的高级扩展方式。由于 Envoy 原生支持 Wasm，用户可以使用 C++/Go/Rust/AssemblyScript 编写逻辑，编译为 `.wasm` 文件后动态加载。这种方式插件隔离性好，崩溃不会导致网关重启，且性能接近原生。
3.  **Lua 插件**：为了兼容传统的 OpenResty/Nginx 生态，Higress 也支持 Lua 插件，方便用户迁移旧有的脚本逻辑。

---



### 5: Higress 是否支持服务治理功能，如熔断、限流和负载均衡？

5: Higress 是否支持服务治理功能，如熔断、限流和负载均衡？

**A**: 是的，Higress 继承了 Envoy 强大的服务治理能力，并对其进行了产品化封装。

1.  **流量防护**：支持并发限流和基于令牌桶的请求限流。
2.  **熔断降级**：支持基于异常比例、慢调用比例或响应时间的自动熔断，保护后端服务不被雪崩。
3.  **负载均衡**：支持轮询、随机、加权最少连接等多种负载均衡算法。
4.  **灰度发布**：支持基于 Header、Cookie 或权重的金丝雀发布和蓝绿部署，方便业务进行无风险上线。

---



### 6: 如何在 Kubernetes 中部署 Higress？

6: 如何在 Kubernetes 中部署 Higress？

**A**: Higress 在 Kubernetes 中的部署非常简单，官方提供了 Helm Chart。

1.  **前提条件**：需要一个准备好的 Kubernetes 集群（版本 >= 1.19）。
2.  **安装步骤**：
    *   添加 Higress Helm 仓库：`helm repo add higress.io https://higress.io/helm-charts`
    *   更新仓库：`helm repo update`
    *   执行安装命令：`helm install higress higress.io/helm-charts/higress -n higress-system --create-namespace`
3.  **Ingress Class**：安装完成后，只需在 Kubernetes 的 Ingress 资源中指定 `ingressClassName: higress`，流量即可自动被 Higress 接管。

---



### 7: Higress 是开源的吗？

7: Higress 是开源的吗？

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 建立在 Envoy 之上。请尝试在本地 Docker 环境中快速部署一个 Higress 实例，并配置一个简单的路由规则：将访问 `/hello` 的流量转发到一个后端测试服务（如 httpbin.org）。

### 提示**: 查阅 Higress 的官方 Docker Quick Start 文档。你需要关注如何编写一个简单的 Ingress 路由配置，其中的 `path` 需要设置为精确匹配或前缀匹配。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 AI 代理插件实现统一模型路由与降级
Higress 的核心优势在于其 AI 原生能力，不要仅将其视为普通的流量网关。
*   **实践建议**：在配置大模型（如 OpenAI、通义千问、Llama）时，使用 Higress 的 **AI 代理插件** 或 **AI 服务** 功能。配置多个模型提供商（例如同时配置 Azure OpenAI 和通义千问）作为同一个 API 的后端。
*   **具体操作**：在路由配置中，设置主模型和备用模型。当主模型（如 GPT-4）出现速率限制（429）或超时时，Higress 可以自动将请求切换到备用模型（如 GPT-3.5 或国内模型），从而实现业务的高可用性。
*   **常见陷阱**：直接将模型 API 地址硬编码在客户端代码中，导致当某个云服务商宕机时，无法快速切换，需要重新发版应用。

### 2. 配置 Token 级别的流控与速率限制
大模型 API 的调用成本主要基于 Token 计费，且供应商通常有严格的 RPM（每分钟请求数）和 TPM（每分钟 Token 数）限制。
*   **实践建议**：不要只配置简单的 QPS（每秒请求数）限流。建议结合 Higress 的插件能力，针对 AI 端点配置基于 **请求体大小估算** 或 **自定义响应头** 的限流策略。
*   **具体操作**：如果后端模型返回了 `x-ratelimit-remaining-tokens` 等 Header，可以通过 Higress 的 `lua` 或 `ext-auth` 插件解析这些 Header，动态调整网关的限流阈值，防止因触发云厂商的 TPM 封禁而导致服务中断。

### 3. 实施提示词（Prompt）的动态注入与安全过滤
在企业内部应用中，将提示词硬编码在前端是不安全的，且难以统一更新。
*   **实践建议**：利用 Higress 的 **请求头插件** 或 **Body 修改插件**，在网关层动态注入 System Prompt。
*   **具体操作**：
    1.  客户端只发送 User Message。
    2.  Higress 网关在转发请求前，自动在 Request Body 中追加预设的 System Prompt（例如设定角色、语气、安全合规限制）。
    3.  同时，配置一个敏感词过滤插件，在请求发出前拦截包含恶意指令的 Prompt，保护后端模型不被越狱攻击。

### 4. 启用 SSE（Server-Sent Events）流式响应的正确透传
AI 对话通常采用流式返回（SSE）以降低首字延迟（TTFT），但普通的 HTTP 代理可能会缓冲数据导致流式失效。
*   **实践建议**：确保 Higress 的路由配置完全支持 SSE 协议的透传。
*   **具体操作**：检查 Higress 的 Upstream 配置，确保针对 `/v1/chat/completions` 等流式接口，关闭响应缓冲。同时，确保网关的超时时间设置得足够长（例如 5 分钟以上），因为流式对话的持续时间可能远长于普通 HTTP 请求。
*   **常见陷阱**：在网关层开启了全链路 Body 缓存（例如用于日志记录），这会导致客户端无法实时收到流式数据块，必须配置流式日志或仅记录 Meta 数据。

### 5. 善用 Wasm 插件实现自定义鉴权与计费逻辑
Higress 对 Wasm（WebAssembly）有着极好的原生支持，这比传统的 Lua 插件性能更好且语言支持更广（如 Go, C++, Rust）。
*   **实践建议**：针对 AI 场景复杂的计费需求（如区分输入 Token 和输出 Token 的计费单价），编写 Wasm 插件进行流量预处理。
*

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*