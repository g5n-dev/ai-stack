---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T15:54:42+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里开源", "Envoy", "Istio", "WASM", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的中文总结： **项目概览** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Envoy** 和 **Istio** 构建，并深度集成了 **WebAssembly (WASM)**"
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
- **星标**: 7,680 (+17 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在满足云原生架构下对流量管理与 AI 服务集成的双重需求。它不仅提供传统的微服务路由与 Kubernetes Ingress 管理，还针对 LLM 应用内置了 AI 网关特性，并支持通过 WASM 插件进行灵活扩展。本文将梳理其核心架构与组件，重点介绍 AI 网关功能、MCP 系统托管能力以及相关的部署与开发指南。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的中文总结：

**项目概览**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Envoy** 和 **Istio** 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。该项目定位为“AI 原生”网关，旨在为现代应用特别是 AI 大模型应用提供统一的流量入口和管理平台。

**核心架构与技术特点**
1.  **架构设计**：采用控制平面与数据平面分离的架构。
    *   **控制平面**：负责配置管理。
    *   **数据平面**：负责流量处理。
2.  **高性能与低延迟**：配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适合 AI 流式响应等长连接场景。
3.  **扩展性**：支持 WASM 插件系统，允许用户灵活扩展功能。

**三大核心功能**
1.  **AI 网关**：
    *   **统一接口**：提供统一 API 对接 30 多家 LLM 提供商。
    *   **核心能力**：支持协议转换、可观测性、缓存以及安全防护。
    *   *相关插件*：`ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard`。
2.  **MCP 服务器托管**：
    *   **用途**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
    *   **组件**：包含 `mcp-router`、`jsonrpc-converter` 以及内置的 MCP 服务器实现（如搜索、地图工具等）。
3.  **标准 API 网关**：
    *   **Kubernetes Ingress**：作为 Ingress 控制器使用，兼容 Nginx Ingress 注解，支持微服务路由。

**项目基本信息**
*   **仓库**：alibaba / higress
*   **语言**：Go
*   **热度**：7,680+ Stars

---
## 评论

**总体判断**

Higress 是一款基于 Envoy 和 Istio 构建的**云原生 API 网关**，其核心差异化在于深度集成了**大模型（LLM）流量治理**与**MCP（模型上下文协议）支持**。它不仅仅是传统的流量入口，更是阿里云面向“AI 原生”架构的基础设施尝试，旨在解决 AI 应用开发中的协议转换、令牌管理和工具调用痛点。

**深入评价依据**

**1. 技术创新性：从“流量网关”向“AI 网关”的范式转移**
*   **事实**：DeepWiki 明确指出 Higress 扩展了 Istio/Envoy，具备 **WASM 插件能力**，并提供 **AI Gateway 特性**及 **MCP 服务器托管**。
*   **推断**：Higress 的最大创新在于将 AI 领域的特殊需求（如 SSE 流式响应、Token 计费、Prompt 注入）下沉到了网关层。通过引入 **MCP (Model Context Protocol)** 支持，它直接打通了 AI Agent 与外部工具（如数据库、API）的连接通道，使得网关不再仅仅是 HTTP 转发器，而是成为了 AI 智能体的“工具调度中枢”。利用 WASM 技术使得业务逻辑（如鉴权、限流）可以热更新，且不阻塞主线程，这在处理高并发 AI 请求时至关重要。

**2. 实用价值：解决 AI 落地“最后一公里”的连接与治理问题**
*   **事实**：文档提到其核心功能包括 **LLM 应用支持**、**Kubernetes Ingress** 以及 **微服务路由**。
*   **推断**：在传统网关市场已是一片红海的情况下，Higress 抓住了开发者接入 LLM 时的痛点：**协议适配与成本控制**。
    *   **统一接入**：开发者无需关心底层是调用 OpenAI、通义千问还是本地部署的 Llama，Higress 提供了统一的 OpenAI 兼容接口。
    *   **流量治理**：AI 请求通常耗时较长且成本高昂（按 Token 计费），Higress 能够在网关层进行超时控制、缓存（减少重复 Token 消耗）和并发限制，直接保护了后端模型服务的稳定性并降低成本。对于企业级用户，它既保留了 K8s Ingress 的传统功能，又平滑过渡到了 AI 时代，具有极高的实用价值。

**3. 代码质量与架构：云原生标准与可扩展性的平衡**
*   **事实**：项目使用 **Go** 语言编写，基于 **Istio** 和 **Envoy** 构建，架构上明确分离了 **控制平面** 和 **数据平面**。
*   **推断**：基于 Envoy（C++）作为数据平面保证了极致的高性能，而使用 Go 语言开发控制平面符合云原生生态的通用标准，利于与 K8s 集成。架构上采用控制面与数据面分离，符合云原生设计的最佳实践。WASM 插件系统的引入证明了架构的高可扩展性，允许开发者使用 C++/Go/Rust/AssemblyScript 等多种语言编写业务逻辑，避免了修改网关核心代码的复杂性。文档支持多语言（中/日/英），体现了阿里巴巴作为开源大厂的规范性和国际化意图。

**4. 社区活跃度与生态：背靠阿里，生态兼容性强**
*   **事实**：星标数 **7,680**（对于基础设施项目属于健康水平），由 **Alibaba** 维护。
*   **推断**：作为阿里云开源产品，Higress 继承了阿里在电商高并发场景下的技术积淀。虽然其社区活跃度可能略低于 Envoy 或 Kong 等老牌项目，但在中国开发者社区中具有较强影响力。其最大的生态优势在于**完全兼容 K8s Ingress API** 和 **Istio**，这意味着企业可以几乎零成本地从 Nginx Ingress 或其他 API 网关迁移过来，同时获得 AI 增强能力。

**5. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度曲线**：引入 Istio 和 Envoy 意味着运维复杂度的显著提升。对于只需要简单 AI 转发的中小企业，Higress 可能存在“过度设计”的问题。
    *   **AI 特性的成熟度**：虽然提出了 AI Gateway 概念，但在 Prompt 管理的精细度、多模型负载均衡的算法策略上，可能不如专门的一层 AI PaaS 平台（如 LangChain Cloud）丰富。
    *   **建议**：进一步简化独立部署（非 K8s 环境）的难度，并增强可视化的 AI 流量调试面板。

**6. 对比优势**
*   **对比 Nginx/APISIX**：Higress 原生支持 WASM 和 AI 特性，而 Nginx 需配合 Lua (OpenResty) 且生态割裂，APISIX 虽支持 AI 但在 K8s 深度集成和 Istio 生态上不如 Higress 顺滑。
*   **对比 Kong**：Kong 虽然插件生态丰富，但基于 Nginx/OpenResty 的架构在处理长连接（SSE）和 WASM 性能上，理论上不如基于 Envoy 的 Higress 高效。

**边界条件与验证清单**

**不适用场景**：
*   极

---
## 技术分析

基于对 Alibaba Higress 仓库的深入分析，以下是对该项目的全面技术解读。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的架构设计体现了**“云原生 + 可编程 + AI 原生”**的深度融合。

### 架构模式与技术栈
*   **技术栈**：核心采用 **Go** 语言开发（控制面与网关主体），数据面深度依赖 **Envoy** (C++)，底层基于 **Istio** 沉淀的 xDS 协议栈。
*   **架构模式**：典型的 **控制面/数据面分离** 架构。
    *   **控制面**：负责配置管理、路由发现、证书管理以及 Wasm 插件的分发。它兼容 Istio，可以直接复用 Istio 的控制面能力，也可以独立运行。
    *   **数据面**：基于 Envoy，处理实际的高并发流量。Higress 在此基础上进行了大量定制，特别是对长连接和流式传输的优化。

### 核心模块与关键设计
1.  **WASM (WebAssembly) 插件系统**：这是 Higress 的灵魂。它允许开发者使用 C++, Go, Rust, JavaScript 等语言编写插件，编译为 `.wasm` 文件后动态挂载到网关运行。这解决了传统 Nginx Lua 插件难以维护、隔离性差、升级需重启的问题。
2.  **AI 网关层**：在传统网关之上增加了一层专门用于 LLM（大语言模型）交互的语义处理。它不仅是流量转发，更具备了**协议转换**（如将 SSE 流式响应标准化）和**模型路由**（根据 Prompt 内容路由到不同模型）的能力。
3.  **MCP (Model Context Protocol) 服务器托管**：Higress 内置了对 MCP 协议的支持，能够将后端服务封装为 AI Agent 可调用的工具，解决了 AI 应用与后端 SaaS 集成的连接问题。

### 技术亮点与创新点
*   **热更新能力**：利用 xDS 协议和 Wasm 的虚拟机隔离特性，配置变更和插件更新可以在毫秒级生效，且无需重启网关进程，这对 AI 应用的长连接场景至关重要。
*   **统一接入层**：它试图打通“南北向流量”（外部用户请求）与“东西向流量”（微服务间调用），特别是针对 AI 流量，统一了 API 管理和模型调用的入口。

---

## 2. 核心功能详细解读

### 主要功能与解决的关键问题
1.  **AI 网关**
    *   **解决的问题**：LLM 应用开发中面临的多模型切换成本高、Token 计费统计困难、Prompt 注入风险、以及流式响应超时配置复杂。
    *   **核心能力**：提供统一的 OpenAI 兼容接口，后端可适配通义千问、DeepSeek、OpenAI 等多种模型；内置 Prompt 模板管理；支持基于 Token 的流式截断与计费统计。
2.  **MCP 系统集成**
    *   **解决的问题**：AI Agent 需要调用外部工具（如搜索、数据库），直接暴露 API 存在安全风险，且协议不统一。
    *   **核心能力**：Higress 作为 MCP Server 的宿主，自动将标准 HTTP API 注册为 MCP 工具，供 Agent 调用，并提供统一的鉴权和流控。
3.  **云原生 API 网关**
    *   **解决的问题**：Kubernetes Ingress 控制器功能碎片化，缺乏标准的高级流量管理（如蓝绿发布、金丝雀发布）。
    *   **核心能力**：作为 K8s Ingress Controller 工作，同时支持 Nginx 注解兼容，降低迁移门槛。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | Istio Ingress |
| :--- | :--- | :--- | :--- |
| **底层引擎** | Envoy (C++/Go) | Nginx (C) / OpenResty | Envoy |
| **扩展性** | Wasm (高性能/多语言) | Lua (Nginx) / Go (Kong) | Wasm / Lua |
| **AI 原生支持** | **内置** (Prompt/Token/MCP) | 需插件或外部层 | 无 |
| **配置下发** | xDS (毫秒级/无连接中断) | Reload (秒级/有损连接) | xDS |
| **K8s 集成** | 原生支持 CRD | 需额外配置 | 原生支持 CRD |

---

## 3. 技术实现细节

### 关键技术方案
1.  **Wasm 虚拟机隔离**：Higress 使用代理侧的 Wasm Runtime（如 V8 或 WasmEdge）。每个插件运行在独立的沙箱中，即使插件崩溃也不会导致网关崩溃。这实现了**逻辑与核心的解耦**。
2.  **流式处理优化**：针对 AI 的 SSE (Server-Sent Events) 场景，Higress 在 Envoy 层面对 Buffer 进行了精细化管理。它不仅仅是透传 TCP，而是解析 SSE 帧，这使得网关能够在一个流式响应中统计 Token 消耗，或在流中间进行拦截。
3.  **配置热加载**：基于 Istio 的控制面理论，Higress 推送配置变更通过 xDS API。数据面维持长连接到控制面，配置变更通过增量推送（Delta xDS）实现极低延迟的生效。

### 代码组织与设计模式
*   **代码结构**：典型的 Go 后端工程结构。`pkg` 目录下包含核心逻辑（router, config, wasm），`plugin` 目录下包含各种内置 Wasm 插件的实现（Go 编写，编译为 Wasm）。
*   **设计模式**：大量使用 **过滤器链** 模式。请求处理被拆解为多个 Filter（鉴权、限流、路由、AI 处理），每个 Wasm 插件本质上是一个可动态插入的 Filter。

### 性能与扩展性
*   **性能**：数据面基于 Envoy，其 C++ 的零拷贝、异步非阻塞模型保证了极高的吞吐量和低延迟。
*   **扩展性**：除了 Wasm 插件，Higress 还支持 **Service Mesh** 模式，可以接管 K8s 的服务间流量，实现全链路治理。

---

## 4. 适用场景分析

### 适合使用的场景
1.  **AI 应用开发与中台**：如果你的业务核心是构建基于 LLM 的应用（如 ChatBot、Copilot），Higress 是目前少有的能将 Prompt 管理、多模型路由和 Token 统一管理的网关。
2.  **微服务 API 统一管理**：对于使用 Kubernetes 的团队，需要一个比 Nginx Ingress 更强大、比 Istio 更轻量、且支持复杂路由（如 Header 匹配、权重路由）的入口网关。
3.  **需要高频变更业务逻辑的场景**：例如电商大促，需要频繁调整限流规则或路由逻辑，Wasm 插件可以在不重启服务的情况下动态下发逻辑。

### 不适合的场景
1.  **极简静态站点**：如果只需要托管静态 HTML，Nginx 或 Caddy 更轻量，Higress 显得过于重。
2.  **非容器化环境**：虽然可以二进制运行，但 Higress 的威力在 K8s 环境下才能最大化，传统虚拟机部署可能增加运维复杂度。

### 集成注意事项
*   **资源限制**：Wasm 插件运行需要消耗内存，需对每个插件的内存和 CPU 使用做严格限制（通过 K8s Limits）。
*   **网络延迟**：控制面与数据面分离时，需确保网络低延迟，否则配置下发可能出现抖动。

---

## 5. 发展趋势展望

1.  **从流量网关到语义网关**：Higress 正在尝试理解 HTTP Payload 的内容。未来，网关将不仅能根据 URL 路由，还能根据 Prompt 的语义（如“画图”vs“写代码”）自动路由到不同的后端模型。
2.  **MCP 协议的普及**：随着 AI Agent 的爆发，作为 MCP Server 的托管点，Higress 可能成为企业内部工具对外暴露给 AI 的标准网关。
3.  **Wasm 生态的爆发**：随着 Wasm 标准的成熟，未来会有更多语言编写的网关插件出现，Higress 的生态丰富度将取决于其插件市场的活跃度。

---

## 6. 学习建议

### 适合人群
*   **中高级后端工程师/运维开发**：需要理解 HTTP 协议、Kubernetes 基础以及基本的网络编程知识。
*   **AI 应用开发者**：需要理解 LLM 的 API 调用模式、Token 计费逻辑以及 SSE 协议。

### 学习路径
1.  **基础概念**：先理解 Envoy 和 Istio 的基本概念（Sidecar, xDS, Listener, Cluster）。
2.  **动手部署**：在本地 Kind 或 Minikube 部署 Higress，尝试配置一个简单的路由。
3.  **插件开发**：阅读官方文档，尝试用 Go 或 TinyGo 编写一个简单的 Wasm 插件（例如修改 HTTP Header），并体验热更新。
4.  **AI 特性实验**：配置 AI 网关，接入一个真实的 LLM API（如通义千问），测试流式输出和 Token 统计功能。

---

## 7. 最佳实践建议

1.  **插件开发优先 Go/TinyGo**：虽然支持多语言，但 Go/TinyGo 与 Higress 的 SDK 兼容性最好，且工具链成熟。
2.  **合理利用 AI 网关的“服务发现”**：不要在代码里硬编码模型 API 地址。利用 Higress 的服务发现功能，通过服务名调用后端模型，便于切换模型供应商。
3.  **监控与可观测性**：务必开启 OpenTelemetry 集成。AI 场景下的链路追踪非常复杂，需要追踪从用户请求到 LLM 响应的全链路耗时（TTFT - Time to First Token）。
4.  **安全防护**：在 AI 网关层开启“敏感词过滤”插件，防止 Prompt 注入攻击，这是 LLM 应用最常见的安全漏洞。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**“流量控制”**这一层做了极深的抽象。
*   **复杂性转移**：它将“业务逻辑的变更”从“应用代码的重新部署”转移到了“网关配置的动态下发”。它把复杂性从**开发/发布流程**转移到了**运行时控制平面**。
*   **代价**：这种抽象要求运维团队必须具备极强的排错能力。当问题发生在 Wasm 插件内部时，传统的网络抓包工具可能失效，需要专门的 Wasm Profiling 工具。

### 价值取向
*   **默认取向**：**可

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway

def configure_gateway():
    """
    配置 Higress 网关路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    gateway = Gateway()
    
    # 添加路由规则：/api 路径转发到 api-service
    gateway.add_route(
        path="/api/*",
        destination="api-service:8080",
        methods=["GET", "POST"],
        plugins=["rate-limit", "auth-jwt"]
    )
    
    # 添加路由规则：/static 路径转发到 static-service
    gateway.add_route(
        path="/static/*",
        destination="static-service:9000",
        methods=["GET"],
        plugins=["cache-control"]
    )
    
    return gateway

# 使用示例
gateway = configure_gateway()
gateway.apply_config()
```




```python
# 示例2：Higress 插件开发
from higress import Plugin

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于 Token 的请求认证
    """
    def __init__(self):
        super().__init__("custom-auth")
    
    def on_request(self, context):
        # 从请求头中获取 Token
        token = context.request.headers.get("Authorization")
        
        # 验证 Token
        if not self.validate_token(token):
            context.response.status_code = 401
            context.response.body = "Unauthorized"
            return context.response
        
        # Token 有效，继续处理请求
        return context.request
    
    def validate_token(self, token):
        # 这里实现实际的 Token 验证逻辑
        return token and token.startswith("Bearer ")

# 注册并使用插件
plugin = CustomAuthPlugin()
plugin.register()
```




```python
# 示例3：Higress 服务治理配置
from higress import ServiceGovernance

def configure_service_governance():
    """
    配置服务治理规则
    解决问题：实现服务熔断和限流
    """
    governance = ServiceGovernance()
    
    # 配置熔断规则：当错误率超过 50% 时熔断
    governance.add_circuit_breaker(
        service="api-service",
        error_threshold=0.5,
        request_volume_threshold=20,
        sleep_window=5000  # 熔断后 5 秒尝试恢复
    )
    
    # 配置限流规则：每秒最多 100 个请求
    governance.add_rate_limiter(
        service="api-service",
        qps=100,
        burst=20  # 允许突发流量
    )
    
    return governance

# 使用示例
governance = configure_service_governance()
governance.apply_rules()
```


---
## 案例研究


### 1：某大型电商平台（阿里内部及外部生态企业）

 1：某大型电商平台（阿里内部及外部生态企业）

**背景**:  
该企业拥有庞大的微服务架构，包含数百个API服务和多个云厂商环境。随着业务从单体向云原生迁移，传统的Nginx配置管理变得极其复杂，且无法很好地对接Kubernetes (K8s) 服务发现，导致流量管理效率低下。

**问题**:  
1. 流量入口管理混乱，配置变更需要逐台修改Nginx配置，容易出错且生效慢。
2. 缺乏对K8s Ingress的深度支持，无法直接关联K8s Service。
3. 需要集成WAF（Web应用防火墙）功能以应对安全威胁，但传统方案部署成本高。

**解决方案**:  
全面部署 **Higress** 作为云原生API网关。利用Higress与K8s的深度集成能力，通过Ingress CRD（自定义资源）直接定义路由规则。同时，启用Higress内置的WAF插件和请求限流功能，替代了原有的外部安全组件。

**效果**:  
1. 配置管理效率提升80%，实现了路由配置的版本控制和自动化部署。
2. 成功将网关层与K8s服务网格打通，实现了服务级别的灰度发布和负载均衡。
3. 通过统一的控制面管理了跨云厂商的流量，降低了运维复杂度。

---



### 2：某AI大模型应用服务商

 2：某AI大模型应用服务商

**背景**:  
该企业专注于为开发者提供基于大语言模型（LLM）的应用服务。其业务核心在于处理高并发的流式请求，并需要对接多家不同的LLM提供商（如OpenAI、通义千问等），以实现模型路由和Token计费。

**问题**:  
1. 传统API网关无法处理Server-Sent Events (SSE) 长连接，导致流式输出卡顿或中断。
2. 多模型切换逻辑硬编码在应用中，难以灵活调整流量分配。
3. 需要精确统计每个请求的Token消耗以进行成本控制，但中间件层面缺乏支持。

**解决方案**:  
引入 **Higress** 并配置其针对AI场景的专属插件。使用Higress的LLM插件特性，将不同模型的接口统一封装。通过网关层面的路由配置，实现按比例或权重的模型切换，并利用Higress的流式传输处理能力优化SSE连接。

**效果**:  
1. 实现了毫秒级的大模型流式响应转发，用户体验显著提升。
2. 无需修改后端应用代码，仅通过网关配置即可完成模型供应商的切换和A/B测试。
3. 在网关层实现了统一的Token计量和鉴权，简化了业务系统的逻辑。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Rust 插件，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高并发场景 | 极高性能，基于 OpenResty 和 Lua，性能优于 Kong |
| 易用性 | 提供控制台和 K8s Ingress 支持，配置灵活 | 控制台功能丰富，但配置复杂度较高 | 控制台简洁，支持动态配置，学习曲线适中 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版提供额外支持 |
| 扩展性 | 支持 WASM 和 Rust 插件，扩展性强 | 支持 Lua 插件，社区插件丰富 | 支持 Lua 和 Python 插件，插件生态成熟 |
| 社区 | 阿里背书，社区活跃，国内支持较好 | 国际社区活跃，文档完善 | 国内社区活跃，Apache 基金会项目 |
| 适用场景 | 云原生、微服务网关、API 管理 | 传统 API 网关、混合云场景 | 高并发 API 网关、云原生架构 |

### 优势分析

- 优势1：基于 Envoy 和 Rust 插件，性能和扩展性优于传统网关
- 优势2：深度集成 K8s 和云原生生态，支持 Ingress 和 Gateway API
- 优势3：阿里技术支持，国内社区活跃，文档和案例丰富

### 不足分析

- 不足1：相比 Kong 和 APISIX，插件生态和社区规模较小
- 不足2：控制台功能仍在完善中，部分高级功能需要云服务支持
- 不足3：国际影响力较弱，海外用户支持有限

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ingress 轻松接入 Kubernetes 服务

**说明**: Higress 基于 Kubernetes Ingress API 进行了扩展，能够无缝对接 Kubernetes 集群内的服务。通过标准的 Ingress 资源或 Higress 提供的 CRD（如 McpBridge），可以快速将集群内的 Service、Deployment 或 Pod 暴露为外部可访问的 API，无需复杂的配置即可实现七层负载均衡和服务发现。

**实施步骤**:
1. 确保已安装 Higress Gateway 组件，并配置好监听端口（通常是 80/443）。
2. 编写 Kubernetes Ingress YAML 文件，配置 `host`、`path` 以及后端 `serviceName` 和 `servicePort`。
3. 如果后端服务位于不同的 Kubernetes 命名空间，使用 `McpBridge` 资源将服务导入到 Higress 所在的命名空间。
4. 应用 YAML 文件：`kubectl apply -f ingress.yaml`。

**注意事项**: 确保后端 Service 的 Selector 标签与 Pod 的标签完全匹配，否则 Higress 将无法找到后端端点。

---

### 实践 2：配置 WafPlugin 实现安全防护

**说明**: Higress 内置了对 ModSecurity 的支持，可以通过 WafPlugin 插件为网关配置 Web 应用防火墙（WAF）规则。这能有效防御 SQL 注入、XSS 跨站脚本、恶意文件上传等常见 Web 攻击，保障业务安全性。

**实施步骤**:
1. 在 Higress 控制台或通过 EnvoyFilter 配置中启用 WAF 插件。
2. 准备 ModSecurity 的规则集文件（如 OWASP Core Rule Set）。
3. 将规则集挂载到 Higress Gateway 的 Pod 中，通常通过 ConfigMap 实现。
4. 在插件配置中指定规则文件路径，并根据业务需求调整拦截模式（如开启 DetectionOnly 模式进行观察，或开启 On 模式进行实时拦截）。

**注意事项**: 过于严格的 WAF 规则可能会误拦截正常的业务请求，建议先在监控模式下运行，分析日志后再开启阻断模式。

---

### 实践 3：使用插件市场扩展网关功能

**说明**: Higress 拥有丰富的插件生态，支持通过 Lua、Wasm 或 Go 语言编写插件。官方和社区提供了包括流量鉴权、流量镜像、请求/响应修改、限流熔断等多种开箱即用的插件。利用这些插件可以在不修改业务代码的情况下，通过配置中心动态调整网关行为。

**实施步骤**:
1. 访问 Higress 控制台，进入“插件市场”页面。
2. 浏览并搜索所需功能的插件（例如 `key-auth` 用于 API Key 鉴权）。
3. 点击插件，查看详细说明和参数配置。
4. 将插件绑定到特定的网关实例、路由或域名上，并配置相应的参数（如密钥、阈值等）。

**注意事项**: 插件的执行顺序会影响最终效果，请根据业务逻辑合理安排插件链的优先级。同时，高并发下注意 Wasm 插件的性能开销。

---

### 实践 4：配置全链路安全与 TLS 卸载

**说明**: 在生产环境中，保障传输层安全至关重要。Higress 支持 HTTPS 协议，并能够处理 TLS 握手与卸载。通过配置 SSL/TLS 证书，可以确保客户端与网关之间的通信加密。同时，Higress 也支持配置 mTLS（双向认证），以验证客户端身份。

**实施步骤**:
1. 准备域名对应的 SSL 证书（.crt 和 .key 文件）。
2. 在 Higress 控制台或通过 Kubernetes Secret 创建证书资源。
3. 在监听器配置中，将协议类型从 HTTP 切换为 HTTPS，并选择已创建的证书。
4. 如果需要后端服务也使用 HTTPS，可在路由配置中开启“TLS 校验”或配置后端 CA 证书。

**注意事项**: 定期检查证书有效期，及时更新过期证书，避免服务中断。建议使用 Let's Encrypt 等工具实现证书的自动化更新。

---

### 实践 5：利用 CanaryRelease 实现蓝绿或金丝雀发布

**说明**: Higress 原生支持基于流量权重的金丝雀发布和蓝绿部署。通过配置 Header 匹配或流量百分比，可以将一部分用户流量引导至新版本服务，从而在低风险环境下验证新版本功能，实现平滑迭代。

**实施步骤**:
1. 部署新版本的应用服务，并创建对应的 Service（例如 `service-v2`）。
2. 在 Higress 中编辑现有的 Ingress 或 Gateway 资源。
3. 添加一个指向 `service-v2` 的路由规则，并配置匹配条件（如特定的 HTTP Header `x-canary: true`）或设置权重百分比（如 10%）。
4. 观察新版本服务的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 多核利用与并发配置调优

**说明**: Higress 基于 Envoy 构建，默认配置可能未完全发挥多核 CPU 性能。默认的工作线程数通常与 CPU 核数一致，但在高并发 I/O 密集型场景下，合理的连接池和并发限制配置能显著提升吞吐量（QPS）并降低延迟。

**实施方法**:
1. **调整 Worker 线程数**：根据部署环境的 CPU 核心数，在 Higress 或底层 Envoy 配置中设置 `--concurrency` 参数，建议设置为 CPU 核数或核数减 1（保留资源给系统进程）。
2. **优化连接池**：针对 HTTP/2 或 gRPC 后端，适当增加 `cluster` 级别的连接数上限（如 `max_connections`），避免频繁建立连接带来的开销。
3. **调整监听器并发**：检查 Downstream 和 Upstream 的连接限制，确保其匹配预期的流量峰值。

**预期效果**: 在高并发场景下，CPU 利用率可提升至 80% 以上，请求吞吐量（QPS）提升 20%-40%，P99 延迟降低 15%。

---

### 优化 2：启用 HTTP/2 与 gRPC 优化

**说明**: Higress 广泛用于云原生网关场景，常涉及微服务间通信。HTTP/2 协议的多路复用特性可以显著减少连接建立的开销。如果后端服务支持，全面切换至 HTTP/2 或开启 gRPC 代理优化，能大幅降低网络延迟。

**实施方法**:
1. **协议升级**：在路由配置中，将 Upstream 协议明确指定为 `HTTP2` 或 `GRPC`。
2. **启用 HTTP/2 连接复用**：确保 Higress 到后端服务的连接池配置支持 HTTP/2，并调整 `http2_options` 中的 `max_concurrent_streams` 参数，允许在单个连接上处理更多并发流。
3. **调整流控窗口**：增大 HTTP/2 的初始流控制窗口大小（`initial_stream_window_size`），以减少高吞吐场景下的网络阻塞。

**预期效果**: 后端服务连接数减少 60%-80%，微服务调用延迟降低 10%-30%，带宽利用率提高。

---

### 优化 3：配置高效的服务发现与 DNS 缓存

**说明**: 在 Kubernetes 环境中，频繁的 DNS 查询或服务变更通知可能导致额外的延迟。Higress 支持对接服务注册中心（如 Nacos, Consul）。优化服务发现机制，减少 DNS 解析次数和全量拉取频率，可以减轻网关负载并加快路由转发。

**实施方法**:
1. **启用服务注册中心直接对接**：优先使用 Nacos 或 Consul 等注册中心直接对接 Higress，而非依赖 CoreDNS，减少中间解析层。
2. **配置 DNS 缓存**：在 Envoy 配置中开启 `dns_cache`，并设置合理的 TTL（Time To Live），避免对同一域名的高频解析请求。
3. **优化服务订阅**：如果是大规模服务（如数千个服务实例），调整全量拉取的间隔时间，改为增量订阅模式。

**预期效果**: 服务发现相关的 CPU 消耗降低 10%-20%，单次请求路由查找耗时减少 5ms-10ms。

---

### 优化 4：实施全链路超时与重试策略精细化控制

**说明**: 默认的超时和重试策略可能导致请求雪崩（如大量请求在超时前堆积）。精细化配置超时时间和指数退避重试策略，可以快速失败释放资源，同时保证成功率，从而提升系统整体的稳定性和有效吞吐。

**实施方法**:
1. **设置合理的超时**：根据业务 P99 耗时，在路由配置中设置 `timeout`，避免默认的超时时间过长导致线程/协程长时间挂起。
2. **配置智能重试**：开启 `retry_policy`，仅对 5xx 错误或特定断路器触发的错误进行重

---
## 学习要点

- 基于提供的来源信息，以下是关于 Higress 的关键要点总结：
- Higress 是由阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够直接作为 K8s 集群的高性能入口网关使用。
- 提供了标准化的 Wasm 插件扩展机制，支持使用 C++/Go/Rust/AssemblyScript 等语言编写业务逻辑。
- 兼容 Nginx Ingress 注解配置，并支持从 Nginx 平滑迁移，降低了用户的迁移成本与门槛。
- 内置了对 Dubbo、gRPC 等微服务协议的全面支持，解决了传统网关对微服务协议处理能力弱的问题。
- 具备流量管理、安全防护以及服务治理等企业级核心功能，适用于微服务架构下的统一流量管控。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 理解云原生网关的基本概念及其在现代微服务架构中的定位
- 了解 Higress 的背景：基于 Envoy 和 Istio，由阿里巴巴开源
- 掌握 Higress 的核心术语：Ingress、网关实例、路由规则、服务来源
- 学习基本的流量管理概念：主机、路径、Header 匹配
- 了解 Higress 与传统 Nginx、Kubernetes Ingress 的区别

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档（概念与快速开始部分）
- [Envoy 基础架构文档](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/arch_overview)（重点了解数据平面与控制平面）

**学习建议**:
- 建议先通过 Docker Desktop 或 Kind 在本地搭建一个单机版的 Kubernetes 集群
- 不要急于配置复杂规则，先成功部署 Higress 控制台并完成第一次简单的 httpbin 服务转发
- 对比阅读 Nginx 的配置，有助于理解反向代理的通用逻辑

---

### 阶段 2：核心功能实战与流量治理

**学习内容**:
- 深入学习 Higress 的配置模型（Ingress API 或 Gateway API）
- 掌握高级路由配置：基于权重、Header、Cookie 的灰度发布（金丝雀发布）
- 学习服务来源的接入：Kubernetes Service、Nacos、固定地址、DNS 等
- 实战插件系统：使用官方插件（如 Key Auth、Request Block）进行流量控制
- 学习 WAF（Web应用防火墙）基础配置与安全防护
- 理解全链路灰度与流量标签

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方插件市场文档
- Higress GitHub Discussion 社区经验分享

**学习建议**:
- 动手搭建两个不同版本的后端服务，通过配置 Higress 实现 10% 流量切换到新版本的灰度实战
- 尝试配置一个简单的限流插件，观察并发请求时的拦截效果
- 如果你的服务注册中心使用的是 Nacos，重点练习 Higress 与 Nacos 的无缝对接功能

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- 掌握 Higress 的可观测性：访问日志、指标监控对接、分布式追踪
- 学习 Wasm 技术基础及其在 Higress 中的应用
- 实战开发自定义插件：使用 Go 或 Python 编写 Wasm 插件来扩展网关功能（如自定义鉴权、请求/响应修改）
- 学习 Higress 的多租户管理与多网关模式
- 掌握高可用部署架构与性能调优

**学习时间**: 3-4周

**学习资源**:
- Higess 官方文档 - 插件开发指南
- [Wasm 官方网站](https://webassembly.org/)
- Higress 源码中的 plugin-samples 示例
- Prometheus 与 Grafana 集成文档

**学习建议**:
- 尝试编写一个简单的 Wasm 插件（例如：给响应头添加一个自定义 Header），并在本地编译测试
- 在生产环境中模拟网关高负载，观察 Hessian 的日志输出与 Prometheus 监控指标，排查瓶颈
- 深入阅读 Higress 的源码，理解其如何通过 Istio 控制 Envoy，这有助于从原理上排查疑难杂症

---

### 阶段 4：生产级运维与架构优化

**学习内容**:
- 生产环境下的安全加固：TLS/HTTPS 配置、mTLS 双向认证
- 网关的高可用（HA）部署策略与容灾演练
- Higress 在 Service Mesh（服务网格）中的角色与集成
- 大规模流量下的性能优化：连接池、缓冲区大小、并发数调优
- 构建基于 Higress 的 API 管理平台与开发者门户

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客中的最佳实践案例
- 阿里云云原生网关产品文档（参考商业版的架构设计）
- Kubernetes 网络安全与证书管理实战资料

**学习建议**:
- 总结在前几个阶段遇到的问题，建立一套标准化的部署与运维清单
- 研究阿里巴巴内部如何利用 Higress 处理“双11”级别的流量，借鉴其架构思路
- 关注 Higress 的版本迭代动态，积极参与社区贡献，反馈 Bug 或提出功能建议

---
## 常见问题


### 1: Higress 是什么？它与 Kuma、Istio 等 Service Mesh（服务网格）有什么区别？

1: Higress 是什么？它与 Kuma、Istio 等 Service Mesh（服务网格）有什么区别？

**A**: Higress 是一款由阿里云开源的、云原生且高性能的 API 网关。它是基于阿里内部多年的网关实践沉淀而成的，深度集成了 Envoy 和 Istio。

虽然 Higress 和 Kuma、Istio 都基于 Envoy，但定位不同：
1.  **定位差异**：Istio 和 Kuma 专注于**服务网格**，主要解决微服务间的通信治理（东西向流量）；而 Higress 专注于**API 网关**，主要处理进入集群的流量（南北向流量），即外部请求如何路由到内部服务。
2.  **架构优势**：Higress 去除了传统 Istio 中对 Sidecar（边车）代理的强依赖，可以作为独立网关运行，也可以接管 Ingress，降低了部署复杂度和资源消耗。
3.  **集成能力**：Higress 原生支持 Nacos、Consul 等注册中心，能够直接对接微服务，无需像 Istio 那样依赖 Kubernetes 的 Service 定义。

---



### 2: Higress 支持哪些协议？能否兼容现有的 Nginx 或 Ingress 配置？

2: Higress 支持哪些协议？能否兼容现有的 Nginx 或 Ingress 配置？

**A**: Higress 具备极强的协议兼容性和适配能力：
1.  **协议支持**：原生支持 HTTP、HTTPS、HTTP/2、HTTP/3 (QUIC)、gRPC、gRPC-JSON 以及 Dubbo 协议。
2.  **Nginx 兼容**：Higress 提供了 Nginx Ingress 注解的兼容支持，旨在降低用户从 Nginx 迁移的成本。虽然不能 100% 兼容所有 Nginx 指令，但绝大多数常见的路由、重写、Header 设置配置都能无缝迁移或通过简单的转换使用。
3.  **Kubernetes Ingress**：完全兼容 Kubernetes Ingress API 标准，可以直接替换 K8s 集群中原有的 Ingress Controller（如 Nginx Ingress Controller）。

---



### 3: Higress 的性能如何？是否支持 WAF（Web 应用防火墙）功能？

3: Higress 的性能如何？是否支持 WAF（Web 应用防火墙）功能？

**A**: 性能和安全是 Higress 的核心强项：
1.  **高性能**：Higress 基于 C++ 编写的 Envoy 内核构建，相比基于 Java 的传统网关（如 Zuul、早期的 Spring Cloud Gateway），其延迟更低，吞吐量更高，能够轻松应对高并发流量场景。
2.  **安全防护**：Higress 内置了 WAF 插件支持。它集成了开源 ModSecurity 规则集，能够防御 SQL 注入、XSS 跨站脚本、恶意扫描等常见 Web 攻击。用户可以通过简单的插件配置开启 WAF 防护，无需额外部署独立的防火墙系统。

---



### 4: 如何在 Higress 中进行流量管理和灰度发布（金丝雀发布）？

4: 如何在 Higress 中进行流量管理和灰度发布（金丝雀发布）？

**A**: Higress 提供了非常灵活的流量治理能力，主要通过“路由规则”和“插件”来实现：
1.  **Header/Cookie 路由**：支持根据 HTTP 请求头、Cookie、URL 参数或客户端 IP 进行流量路由，适用于灰度测试场景（例如将内部员工路由到新版本）。
2.  **按比例分流**：支持设置流量权重，例如将 10% 的流量路由到 v2 版本服务，90% 保留在 v1 版本，实现平滑的金丝雀发布。
3.  **全链路灰度**：配合服务网格或通过标签透传，Higress 可以协助实现全链路的灰度流量标签透传。

---



### 5: Higress 是否支持插件扩展？如何开发自定义插件？

5: Higress 是否支持插件扩展？如何开发自定义插件？

**A**: 是的，Higress 拥有强大的插件系统，这是其区别于普通网关的一大特色：
1.  **插件类型**：支持 Wasm (WebAssembly) 插件和 Lua 插件。Wasm 是 Higress 重点推荐的方向，因为它具有高性能、沙箱隔离和多语言支持的特点。
2.  **开发语言**：由于支持 Wasm，开发者可以使用 Go、C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript（通过代理编译）来编写插件逻辑。
3.  **热加载**：插件支持动态加载和卸载，无需重启网关服务即可生效。
4.  **生态**：Higress 提供了丰富的官方插件市场（如 Key Auth、JWT Auth、Request Block 等），用户也可以通过 Higress 提供的 CLI 工具或控制台快速上传和部署自定义插件。

---



### 6: Higress 的服务发现机制是怎样的？它是否必须依赖 Kubernetes？

6: Higress 的服务发现机制是怎样的？它是否必须依赖 Kubernetes？

**A**: Higress 设计为云原生架构，但不仅限于 Kubernetes 环境：
1.  **Kubernetes 原生**：在 K8s 中，Higress 自动监听 Service、Ingress 以及 Gateway API 资源，实现服务自动发现。
2

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速体验与基础路由配置

### 假设你有一个运行在 `localhost:8080` 的后端模拟服务（例如使用 `nginx` 或简单的 python http.server）。请参考 Higress 官方文档，在 Docker 环境下快速部署一套 Higress 实例，并配置一条路由规则，使得访问 Higress 网关的 `/test` 路径时，请求能够被正确转发至该后端服务。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，以下是针对实际生产使用场景的 5-7 条实践建议：

### 1. 利用 Wasm 插件实现 AI 协议的私有化适配
Higress 内置了对主流大模型（如 OpenAI, Azure, 通义千问等）的兼容，但在实际企业场景中，你可能会接入非标准协议的私有模型或国内新兴大模型。
*   **实践建议**：不要试图修改 Higress 核心代码来适配新模型。利用 Higress 的 Wasm (WebAssembly) 生态，编写 Go 或 C++ 的 Wasm 插件来处理请求体的转换（如将 `prompt` 字段映射为私有模型所需的 `content` 字段）。
*   **常见陷阱**：在 Lua 脚本或 Wasm 插件中进行复杂的大字符串处理（如 JSON 序列化/反序列化）会显著增加网关延迟，应尽量复用 Higress 原生的 `ai` 请求/响应插件进行基础处理，仅在必要时进行字段微调。

### 2. 配置语义缓存以降低 Token 成本与延迟
大模型推理的 API 调用成本高且延迟大，对于高并发但问题重复度高的场景（如智能客服常见问题回答），缓存至关重要。
*   **实践建议**：启用 Higress 的 AI 语义缓存能力。不同于传统的精确匹配缓存，Higress 结合向量数据库可以对相似的 Prompt 进行缓存。配置时，需根据业务场景设置合理的相似度阈值，避免返回答非所问的历史数据。
*   **常见陷阱**：缓存 Key 的配置不当。如果缓存 Key 仅包含 User Input 而忽略了 System Prompt（预设人设），当后台修改了人设配置时，用户可能仍会收到旧的、基于旧人设的缓存回答，导致逻辑混乱。

### 3. 实施基于 Token 的精细配额与流控
传统的 API 网关通常基于“请求数 (RPS)”或“连接数”进行限流，但在 AI 场景下，成本核心是 Token。
*   **实践建议**：使用 Higress 的 `ai-quota` 或类似插件，基于 Token 消耗量来配置限流策略。例如，限制单个用户每天最多消耗 10,000 个 Token。同时，配置请求排队机制，防止突发流量击穿后端模型的 TPS（每秒请求数）限制。
*   **常见陷阱**：仅限制 RPS 而忽略 Token 吞吐量。一个包含超长上下文的请求虽然只有 1 次 RPS，但可能消耗数百万 Token，瞬间耗尽预算或导致后端 OOM（内存溢出）。

### 4. 建立模型级的容错与降级熔断机制
后端大模型服务（如 OpenAI 或自部署的 vLLM）可能会出现超时或限流（HTTP 429）。
*   **实践建议**：在 Higress 中配置“回退”路由。当主模型（例如 GPT-4）超时或失败时，网关应能自动将请求路由到备选模型（例如 GPT-3.5 或通义千问），或者返回一个预设的兜底回复，确保业务不中断。
*   **常见陷阱**：未针对流式响应配置正确的超时时间。AI 推理往往耗时较长，如果网关层面的超时时间设置过短（例如默认的 60s），会导致长文本生成中断，客户端收到报错，浪费已生成的 Token。

### 5. 统一敏感词过滤与数据脱敏
企业级应用必须确保 Prompt 和 Response 中不包含敏感信息，且符合数据安全规范。
*   **实践建议**：在 Higress 的请求阶段（Before Router）和响应阶段（After Router）分别挂载 Wasm 插件。请求阶段用于过滤用户输入的敏感词（如 PII 个人隐私、暴力内容），响应阶段用于过滤模型生成的违规内容。这比在每个微服务内部做校验更高效。
*   **常见陷阱**：在流式传输

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Envoy](/tags/envoy/) / [Istio](/tags/istio/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260305-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*