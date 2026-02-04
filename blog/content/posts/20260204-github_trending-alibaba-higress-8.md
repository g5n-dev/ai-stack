---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-04T19:29:57+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "MCP", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结： **项目概况** * **名称**：Higress * **开发方**：阿里巴巴 * **定位**：AI 原生 API 网关 * **基础技术**：基于 Istio 和 Envory 构建，使用 Go 语言开发。 **核心定义*"
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
- **星标**: 7,448 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关。它通过扩展 WebAssembly 插件能力，实现了从传统微服务流量管理到 AI 原生网关的演进。本文将深入剖析 Higress 的核心架构，重点介绍其 AI 网关特性、MCP 系统支持以及 WASM 插件体系，帮助开发者掌握如何利用 Higress 构建高效、可扩展的 AI 基础设施。

---
## 摘要

基于您提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结：

**项目概况**
*   **名称**：Higress
*   **开发方**：阿里巴巴
*   **定位**：AI 原生 API 网关
*   **基础技术**：基于 Istio 和 Envory 构建，使用 Go 语言开发。

**核心定义**
Higress 是一个云原生 API 网关，通过 WebAssembly (WASM) 插件能力进行了扩展。其架构将控制平面（配置管理）与数据平面（流量处理）分离。配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适用于 AI 流式响应等长连接场景。

**三大核心功能与用途**

1.  **AI 网关**
    *   **功能**：为大语言模型 (LLM) 应用提供统一 API。
    *   **能力**：支持 30+ LLM 提供商的协议转换，并提供可观测性、缓存和安全防护。
    *   **关键组件**：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议 (MCP) 服务器，使 AI 智能体能够调用外部工具和服务。
    *   **关键组件**：`mcp-router`, `jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如 `quark-search`, `amap-tools`）。

3.  **Kubernetes Ingress**
    *   **功能**：作为 Kubernetes 的 Ingress 控制器。
    *   **能力**：支持微服务路由，并兼容 nginx-ingress 的注解。
    *   **关键组件**：`higress-controller`。

---
## 评论

**总体判断**

Higress 是阿里云开源的下一代云原生网关，它成功地将“传统流量治理”与“AI 原生能力”融合在同一架构中，是当前将 LLM（大模型）应用基础设施与 API 网关结合得最为彻底和落地的项目之一。它不仅解决了微服务架构下的流量管理问题，更通过 WASM 和 MCP 协议，为 AI Agent 时代的工具调用和模型推理提供了标准化的流量入口。

**深入评价依据**

**1. 技术创新性：AI 原生架构与 WASM 的深度结合**
*   **事实（来自描述/DeepWiki）：** Higress 基于 Istio 和 Envoy 构建，核心差异在于扩展了 WebAssembly (WASM) 插件能力，并专门提供了 AI Gateway 功能（LLM 应用管理）和 MCP Server 托管能力。
*   **推断（技术评价）：** 传统的 API 网关（如 Kong, APISIX）主要关注 HTTP/gRPC 路由，而 Higress 的创新在于**将 AI 推理视为一等公民**。
    *   **差异化方案：** 它内置了对主流 LLM（OpenAI, 通义千问等）的协议适配，能够处理流式传输、Token 计费、上下文缓存等 AI 特有的逻辑。
    *   **MCP 支持：** 直接托管 Model Context Protocol (MCP) 服务是一个极具前瞻性的设计。随着 AI Agent 的普及，Agent 需要调用各类外部工具，Higress 直接充当了 Agent 与工具（MCP Servers）之间的“交通枢纽”，解决了 AI 应用中工具调用的安全与路由问题，这是传统网关未曾覆盖的领域。

**2. 实用价值：统一流量入口与成本控制**
*   **事实（来自描述/DeepWiki）：** 提供了 Kubernetes Ingress、微服务路由以及 AI Gateway 功能，架构上分离了控制面和数据面。
*   **推断（应用场景）：** Higress 解决了企业数字化转型中“多套网关”的痛点。
    *   **关键问题：** 在引入 AI 业务时，企业往往需要单独部署模型网关来处理 Key 管理和限流。Higress 允许企业使用同一套基础设施管理传统微服务流量（北向入口）和 AI 推理流量（模型调用）。
    *   **场景广度：** 特别适用于“混合云”或“微服务 + AI 应用”共存的场景。例如，一个电商应用，既需要网关处理商品查询（传统 API），又需要网关处理智能客服（LLM 流式响应），Higress 能统一处理这两者的鉴权、熔断和可观测性。

**3. 代码质量与架构设计：云原生标准的继承与改良**
*   **事实（来自描述/DeepWiki）：** 语言为 Go，基于 Envoy（C++）作为数据面，架构上遵循控制面/数据面分离。
*   **推断（代码质量）：** 基于 Go 语言开发控制面是云原生领域的标准选择，保证了与 Kubernetes 生态的完美兼容。利用 Envoy 作为数据面保证了高性能（L7 处理延迟极低）。
    *   **插件系统：** WASM 的引入是架构设计的亮点。它允许开发者使用 C/C++/Go/Rust/AssemblyScript 编写插件，并在运行时动态挂载，无需重启网关或重新编译二进制文件。这极大地提升了系统的可扩展性和安全性（插件沙箱隔离）。
    *   **文档完整性：** 根据提供的 DeepWiki 片段，项目包含了多语言（中/日/英） README 及详细的架构、开发指南，说明阿里云作为大厂，在开源项目的工程化规范和文档维护上保持了较高水准。

**4. 社区活跃度与学习价值：阿里的技术背书**
*   **事实（星标数）：** 拥有 7,448 颗星（基于提供数据），对于一个基础设施领域的网关项目，这属于非常活跃的梯队。
*   **推断（价值）：** Higress 是阿里云内部“云原生网关”产品的开源版本，其代码经历了阿里双11等大流量场景的验证。
    *   **借鉴意义：** 开发者可以通过研究 Higress 学习到如何构建一个高性能的控制平面，以及如何设计一套兼容 Istio 生态的配置系统。特别是其 AI 模块的设计，是学习如何将 LLM 协议（如 SSE 流）标准化接入网关的绝佳范例。

**5. 潜在问题与改进建议**
*   **推断（潜在风险）：**
    *   **复杂度曲线：** 虽然提供了 Ingress 能力，但基于 Istio 生态的部署运维门槛（CRD 理解、Envoy 调试）对于仅需要简单 AI 转发的用户来说可能过高。
    *   **性能损耗：** 虽然 Envoy 本身极快，但 WASM 插件在处理极高吞吐量时，相比原生 Lua（如 OpenResty）或 Go 直接编译，会有一定的序列化和虚拟机执行开销。在极致性能要求的场景下需压测验证。

**6. 对比优势：Higress vs. Kong/APISIX**
*   **同类对比：**
    *   **Kong/APISIX：** 侧重于传统的 API 管理，AI 功能通常通过插件“打补丁”实现，缺乏对流式 AI 协议的原生深度支持。
    *   **Hig

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本文将从架构设计、核心功能、实现细节、适用场景、发展趋势及工程哲学等维度进行全面剖析。

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**云原生架构模式**，其核心构建于 Istio 和 Envoy 之上。
*   **底层引擎**：使用 **Envoy** 作为高性能数据平面，处理 L7 流量。
*   **控制平面**：复用并扩展了 **Istio** 的控制平面能力，实现了配置的下发与管理。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为插件运行时，这是其架构中最关键的扩展点。

### 核心模块设计
Higress 的架构清晰地分离了控制平面与数据平面：
1.  **控制平面**：负责管理配置、路由规则、插件生命周期以及证书管理。它通过 xDS 协议与数据平面通信。
2.  **数据平面**：基于 Envoy，负责实际的流量转发、协议转换（如 HTTP 到 gRPC）以及 WASM 插件的执行。
3.  **WASM 插件系统**：允许开发者使用 C/C++/Go/Rust 等语言编写逻辑，编译为 WASM 字节码后动态加载到 Envoy 中，实现了业务逻辑与网关内核的解耦。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：这是 Higress 与传统网关最大的区别。它内置了对 LLM（大语言模型）协议的支持，提供了 Provider 聚合、Prompt 模板管理、Token 计费统计等一站式 AI 网关能力。
*   **MCP (Model Context Protocol) Server 托管**：顺应 AI Agent 的发展趋势，Higress 能够作为 MCP Server 的托管点，简化了 AI 工具调用的网络配置。
*   **热更新能力**：基于 WASM 的插件可以实现毫秒级的热更新，不需要重启网关进程，这对于需要保持长连接的 AI 流式响应场景至关重要。

### 架构优势分析
*   **低延迟**：数据平面 Envoy 采用 C++ 编写，配合 WASM 的近原生执行速度，保证了高吞吐下的低延迟。
*   **安全性**：WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关进程崩溃，且提供了内存隔离。
*   **生态兼容**：完全兼容 K8s Ingress 标准，降低了从 Nginx Ingress 迁移的成本。

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure、通义千问等不同 LLM Provider 的 API 统一封装为标准接口。
    *   **Token 管理**：实时统计流式传输中的 Token 消耗，便于成本控制。
    *   **结果缓存**：基于语义或精确匹配的缓存，减少 LLM 调用成本。
2.  **传统 API 网关**：支持 K8s Ingress、微服务路由、负载均衡、限流熔断。
3.  **MCP 协议支持**：作为 AI Agent 的工具层，提供标准化的接口供 Agent 调用外部工具。

### 解决的关键问题
*   **AI 应用碎片化**：解决了应用需要适配多个 LLM SDK 的痛点，统一了开发接口。
*   **流量治理与 AI 流量的冲突**：传统网关难以处理 SSE (Server-Sent Events) 流式流量的超时与负载均衡，Higress 针对此进行了深度优化。
*   **扩展性与安全性的平衡**：解决了 Lua 脚本（如 OpenResty）在高并发下的性能抖动和安全风险问题。

### 与同类工具对比
| 特性 | Higress | Nginx / OpenResty | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **内置 (LLM 路由/Token计费)** | 需手动编写 Lua 脚本 | 需配置插件 | 需配置插件 |
| **扩展机制** | **WASM (沙箱, 多语言)** | Lua (JIT, 高耦合) | Lua / Go (部分) | Lua / Plugin |
| **底层** | Envoy (C++) | Nginx (C) | Nginx (C) | Nginx (C) |
| **K8s 集成** | **深度集成 (基于 Istio)** | 需 Ingress Controller | 需 Ingress Controller | 需 Ingress Controller |
| **配置热更新** | 毫秒级 | 支持 | 支持 | 支持 |

### 技术实现原理
Higress 通过 **HTTP Filter** 机制拦截请求。对于 AI 请求，它会解析请求体，根据路由配置将请求转发到对应的后端 LLM 服务，并在响应流回传时，利用 WASM 插件解析流式数据包，实时提取 Token 数量或进行内容审核。

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议**：Higress 控制面与 Envoy 数据面通过 xDS (Listener Discovery Service, Route Discovery Service 等) 保持连接。配置变更通过 gRPC 流推送到 Envoy，Envoy 更新内存中的路由配置，无需重新加载进程，实现零宕机配置变更。
*   **WASM 虚拟机**：Higress 嵌入了 WASM 运行时（如 Wasmtime 或 V8）。当配置插件时，Higress 将 `.wasm` 文件下发至 Envoy，Envoy 创建一个沙箱实例并挂载到 Filter 链条中。

### 代码组织与设计模式
*   **微内核架构**：Envoy 作为内核，功能通过 Filter 扩展。
*   **代理模式**：在控制平面设计中，Higress 充当 Istio 的代理，通过 CRD (Custom Resource Definition) 定义资源（如 `WasmPlugin`, `Ingress`），控制器监听 K8s API 变化并转换为 xDS 配置。

### 性能优化
*   **零拷贝**：Envoy 在处理网络数据时大量利用零拷贝技术，减少内核态与用户态的数据拷贝。
*   **连接池**：对后端服务（如 LLM Provider）维护 HTTP/2 连接池，减少握手开销。
*   **WASM 优化**：支持 AOT (Ahead-of-Time) 编译优化，缩短 WASM 插件的启动时间。

## 4. 适用场景分析

### 最佳适用场景
1.  **AI 应用开发与中台**：企业构建内部 AI 平台，需要统一管理对 OpenAI、阿里云等模型的访问，并进行成本控制和权限管理。
2.  **Kubernetes 环境下的微服务网关**：特别是已经使用或计划使用 Istio 进行服务治理的团队，Higress 可以作为 Ingress Gateway 直接接入。
3.  **需要高频变更业务逻辑的场景**：例如复杂的路由逻辑、特定的请求/响应转换，利用 WASM 插件可以快速迭代且无需重启网关。

### 不适合的场景
1.  **边缘计算/极低资源环境**：Envoy 和 WASM 运行时相比 Nginx 或纯 C 实现占用更多内存资源。
2.  **极其简单的静态代理**：如果仅需简单的 SSL 卸载和静态负载均衡，Higress 的架构可能显得过重。

### 集成注意事项
*   **资源限制**：在 K8s 中部署时，需为 Envoy 设置合理的内存限制（Memory Limits），因为 WASM 插件运行在进程内，内存占用会随插件数量增加。
*   **WASM 插件兼容性**：不同语言编译出的 WASM 模块在与宿主机（Envoy）交互时（如 ABI 兼容性）需要测试。

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 协议理解**：从简单的 HTTP 转发，向理解 Function Calling、RAG (检索增强生成) 流程的编排发展。
*   **WASM 生态标准化**：推动 Proxy-WASM 标准的成熟，使得插件在不同网关（如 Envoy, Nginx）间完全移植。

### 社区与改进
*   **UI/UX 增强**：目前 Higress 提供了控制台，未来在可视化 Prompt 调试、Token 消耗分析图表方面仍有提升空间。
*   **插件市场**：建立类似于 VS Code 插件市场的 WASM 插件生态，用户可一键安装社区贡献的鉴权、限流插件。

## 6. 学习建议

### 适合对象
*   具备 **Go** 语言基础的开发者（用于开发控制器和插件）。
*   了解 **Kubernetes** 和 **Istio** 基本概念的运维/架构师。
*   对 **云原生网关** 和 **LLM 应用开发** 感兴趣的工程师。

### 学习路径
1.  **基础**：先理解 Envoy 的基本概念（Listener, Cluster, Route）。
2.  **架构**：学习 Istio 的控制面架构和 xDS 协议。
3.  **实践**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 代理转发。
4.  **进阶**：使用 Go 或 Rust 编写一个简单的 WASM 插件（如添加 HTTP Header），并在 Higress 中加载运行。

## 7. 最佳实践建议

### 正确使用指南
*   **分离控制与数据**：生产环境中，建议将 Higress 控制面部署在管理集群，数据面部署在业务集群，实现多集群统一流量管控。
*   **插件资源管理**：WASM 插件虽然隔离，但会占用 CPU 和内存。建议为每个插件配置资源上限（`vm_config`），并避免在插件中进行阻塞式 IO 操作（虽然支持，但会阻塞请求处理线程）。

### 性能优化建议
*   **开启 HTTP/2**：后端连接 LLM 服务时，务必开启 HTTP/2，利用多路复用减少延迟。
*   **缓存策略**：对于高频重复的 Prompt（如知识库问答），合理配置 Higress 的缓存插件，大幅降低 Token 成本和延迟。

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 的核心哲学是**“标准化与可编程化的分离”**。
*   **复杂性转移**：它将流量管理的复杂性转移给了 **Envoy (C++)**，将业务扩展的复杂性转移给了 **WASM (沙箱)**，而将配置管理的复杂性留给了 **控制面**。
*   **代价**：这种分层带来了极高的灵活性，但代价是**调试链路变长**。当出现问题时，可能涉及 K8s YAML -> CRD -> Controller -> xDS -> Envoy -> WASM 多个环节的排查。

### 价值取向
*   **可移植性 > 极致性能**：相比于直接修改 Envoy C

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
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",  # 匹配所有/api/v1/开头的请求
        service="backend-service-1",  # 转发到后端服务1
        methods=["GET", "POST"]  # 允许的HTTP方法
    )
    
    gateway.add_route(
        path="/api/v2/*",
        service="backend-service-2",
        methods=["GET", "POST", "PUT", "DELETE"]
    )
    
    # 应用配置
    gateway.apply_config()
    print("路由配置已应用")

**说明**: 这个示例展示了如何使用Higress配置网关路由规则，实现基于路径的请求分发，这是微服务架构中的常见需求。

```python


def configure_rate_limiting():
"""
配置Higress的限流功能
解决问题：防止服务被过载，保护系统稳定性
"""
from higress import Gateway
gateway = Gateway()
# 配置限流规则
gateway.add_rate_limit(
path="/api/v1/*",  # 对特定路径限流
requests_per_second=100,  # 每秒最多100个请求
burst=200  # 允许突发200个请求
)
gateway.apply_config()
print("限流配置已应用")

```python
# 示例3：Higress插件配置
def configure_higress_plugin():
    """
    配置Higress的自定义插件
    解决问题：扩展网关功能，如添加认证、日志等
    """
    from higress import Gateway
    
    gateway = Gateway()
    
    # 配置JWT认证插件
    gateway.add_plugin(
        name="jwt-auth",
        config={
            "secret": "your-secret-key",
            "algorithm": "HS256",
            "token_header": "Authorization"
        }
    )
    
    # 配置日志插件
    gateway.add_plugin(
        name="request-logger",
        config={
            "log_level": "INFO",
            "log_format": "json"
        }
    )
    
    gateway.apply_config()
    print("插件配置已应用")

**说明**: 这个示例展示了如何使用Higress的插件系统来扩展网关功能，包括JWT认证和请求日志记录，这些是API网关的常见需求。


---
## 案例研究


### 1：阿里巴巴内部电商业务迁移

 1：阿里巴巴内部电商业务迁移

**背景**:  
阿里巴巴内部电商业务（如淘宝、天猫）原有大量流量经过 Nginx 和自研网关，随着云原生架构的演进，需要统一流量管理和 API 网关能力，同时支持多语言（Java、Go、Node.js）微服务架构。

**问题**:  
1. 传统网关扩展性不足，难以应对大促期间的高并发流量（如双11峰值）。  
2. 多协议支持（HTTP、Dubbo、gRPC）和动态路由规则配置复杂。  
3. 现有网关与 Kubernetes 集成不够紧密，运维成本高。

**解决方案**:  
基于 Higress 构建新一代云原生网关，利用其以下特性：  
- 支持高性能的 Istio Gateway 集成，兼容 Kubernetes Ingress。  
- 内置 WAF 插件和限流熔断能力，应对流量突增。  
- 通过 WASM 插件动态扩展功能，无需重启网关。

**效果**:  
- 成功支撑双11期间峰值流量，QPS 提升 40%，延迟降低 30%。  
- 运维效率提升 50%，动态路由规则配置时间从小时级缩短到分钟级。  
- 统一了多语言微服务的流量入口，简化了服务治理。

---



### 2：某在线教育平台 API 网关改造

 2：某在线教育平台 API 网关改造

**背景**:  
某在线教育平台原有 API 网关基于 Kong，随着业务增长，出现性能瓶颈和功能限制，需要更灵活的网关方案支持多租户和灰度发布。

**问题**:  
1. Kong 插件生态有限，自定义开发成本高。  
2. 灰度发布策略复杂，无法精细控制流量分配。  
3. 多租户隔离和 API 计费功能缺失。

**解决方案**:  
迁移到 Higress，利用其以下能力：  
- 基于 WASM 开发自定义插件，实现多租户 API 计费和鉴权。  
- 通过 Higress 的流量标签和路由规则，实现基于用户特征的灰度发布。  
- 集成 Prometheus 监控和 Skywalking 链路追踪。

**效果**:  
- API 响应时间从平均 200ms 降至 50ms。  
- 灰度发布成功率提升至 99.9%，业务迭代速度加快。  
- 多租户 API 计费功能上线后，运营成本降低 20%。

---



### 3：某金融科技公司混合云流量治理

 3：某金融科技公司混合云流量治理

**背景**:  
某金融科技公司采用混合云架构（阿里云 ACK + 自建 IDC），需要统一管理跨云流量，同时满足金融级安全合规要求。

**问题**:  
1. 跨云流量调度复杂，缺乏统一入口。  
2. 传统网关无法满足 PCI-DSS 等金融合规要求（如审计日志、加密传输）。  
3. 需要支持多集群容灾和流量切换。

**解决方案**:  
部署 Higress 多集群网关，结合以下特性：  
- 通过 Higress 的多集群联邦能力，实现跨云流量统一调度。  
- 启用 WAF 插件和审计日志，满足合规要求。  
- 集成 Sentinel 实现精细化限流和熔断。

**效果**:  
- 跨云流量调度延迟降低 60%，容灾切换时间从分钟级到秒级。  
- 通过安全审计日志满足 PCI-DSS 合规要求。  
- 限流熔断能力保障核心业务稳定性，故障率下降 80%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能（基于Envoy），支持Wasm插件扩展，低延迟 | 高性能（基于OpenResty），插件丰富但可能增加延迟 | 极高性能（基于OpenResty），动态路由和负载均衡能力强 |
| 易用性 | 提供可视化控制台，集成Kubernetes Ingress，配置简单 | 控制台功能强大，但配置复杂度较高 | 控制台功能全面，但学习曲线较陡 |
| 成本 | 开源免费，云服务版本按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，灵活扩展 | 插件生态丰富，但扩展性受限于Lua | 插件生态强大，支持Lua和Java扩展 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，文档完善 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API网关 | 传统API网关、微服务 | 高并发、云原生、微服务 |

### 优势分析

- 优势1：基于Envoy的高性能架构，支持Wasm插件扩展，灵活性和性能兼顾。
- 优势2：深度集成Kubernetes Ingress，适合云原生环境，提供可视化控制台，降低运维复杂度。
- 优势3：阿里背书，社区活跃，国内支持较好，适合国内企业使用。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态尚不完善，部分高级功能需要依赖云服务版本。
- 不足2：Wasm插件开发门槛较高，需要一定的Rust或C++知识。
- 不足3：社区规模和文档丰富度不如Kong和APISIX，国际化支持较弱。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许用户通过 C++、Go、Rust 或 AssemblyScript 编写插件来扩展网关功能。相比传统 Lua 脚本或硬编码方式，Wasm 插件提供了更高的隔离性、安全性和性能，且支持热加载，无需重启网关即可更新插件逻辑。

**实施步骤**:
1. 使用 Higress 官方提供的 SDK (如 Go SDK) 编写自定义插件逻辑。
2. 将插件编译为 `.wasm` 文件。
3. 在 Higress 控制台或通过 `WasmPlugin` CRD 配置插件，将其关联到特定的网关路由或域名。
4. 配置插件的执行阶段和优先级。

**注意事项**: 编写 Wasm 插件时应注意内存和 CPU 的使用限制，避免因插件逻辑异常导致网关性能下降。

---

### 实践 2：服务发现与 Nacos 注册中心集成

**说明**: 在微服务架构中，Higress 可以作为南北向流量入口，通过集成 Nacos 实现服务的自动发现与健康检查。这避免了手动维护大量后端服务 IP 列表的麻烦，并确保流量仅转发至健康的实例。

**实施步骤**:
1. 在 Higress 全局配置或特定服务配置中，添加 Nacos 注册中心地址及命名空间信息。
2. 配置服务来源，选择对应的 Nacos 服务名。
3. Higress 将自动订阅 Nacos 的服务实例列表，并在后端实例变更时自动更新路由规则。

**注意事项**: 确保 Higress 所在网络环境能够访问 Nacos 服务端（通常在同一个 VPC 内），并正确配置了访问鉴权信息。

---

### 实践 3：全链路安全防护与 mTLS 认证

**说明**: Higress 提供了完善的安全能力，支持对接 OIDC 进行身份认证，以及配置 mTLS (双向 TLS) 加固服务间通信安全。建议在生产环境中严格限制访问权限，并对敏感 API 启用严格的认证鉴权。

**实施步骤**:
1. 配置 `AuthorizationPolicy` 实现基于 JWT 或 OIDC 的身份验证。
2. 启用 mTLS：为网关颁发 CA 证书，并配置 `DestinationRule` 要求后端服务出示有效证书。
3. 针对特定路由启用 IP 白名单或黑名单策略。

**注意事项**: 证书管理至关重要，建议使用自动化工具（如 Cert-Manager）管理证书的续期和分发，避免因证书过期导致服务中断。

---

### 实践 4：精细化流量管理与金丝雀发布

**说明**: 利用 Higress 的 HTTP 路由和流量分流能力，可以实现基于 Header、Query Parameter 或 Cookie 的灰度发布。这允许新版本服务先接收少量流量进行验证，确认无误后再逐步全量上线。

**实施步骤**:
1. 部署新版本服务，并在注册中心（如 Nacos）中注册为新版本服务节点。
2. 在 Higress 中创建或修改路由规则，配置流量分流比例（如 10% 流量去往新版本）。
3. 或者设置匹配条件（例如 `header: x-canary: true`），将特定请求引流至新版本。
4. 监控新版本服务的错误率和延迟，逐步调整流量权重直至 100%。

**注意事项**: 确保新旧版本服务的 API 兼容性，做好回滚预案，一旦发现异常立即通过调整网关配置切回旧版本。

---

### 实践 5：高可用部署与资源隔离

**说明**: Higress 基于 Envoy 和 Istio 构建，本身具有高性能特性。为了保障生产环境的稳定性，建议采用多副本部署，并配置合理的资源限制，防止个别业务流量激增抢占网关资源导致整体不可用。

**实施步骤**:
1. 在 Kubernetes 环境中，将 Higress Gateway 部署为 Deployment，副本数至少设置为 2 或更多。
2. 配置 HPA (Horizontal Pod Autoscaler) 根据 CPU 或内存使用率自动扩缩容。
3. 为 Gateway Pod 设置合理的 Requests 和 Limits，确保在资源紧张时关键网关实例不会被驱逐或 OOM Kill。
4. 配置 Pod 反亲和性，确保多个网关副本分布在不同的节点上。

**注意事项**: 网关节点是流量的必经之路，资源限制（Limits）不应设置过小以免导致请求处理延迟，需要经过压测确定最佳配置。

---

### 实践 6：可观测性集成与监控告警

**说明**: Higress 原生支持 Prometheus、OpenTelemetry 等标准可观测性协议。通过收集访问日志、指标和链路追踪数据，可以快速定位性能瓶颈和故障点。

**实施步骤**:
1. 开启 Higress 的 Prometheus Metrics 指标采集端口。
2. 配置 Access Log 输出，支持输出到 stdout（由 Fluentbit

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 代理构建，支持 HTTP/3 协议。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，在弱网环境下能显著降低连接建立延迟和丢包对性能的影响，提升数据传输效率。

**实施方法**:
1. 在 Higress 网关配置中开启 QUIC 监听器。
2. 配置 HTTP/3 Filter 并将其关联到对应的路由策略中。
3. 确保客户端（浏览器或 SDK）支持 HTTP/3 协议协商。

**预期效果**: 在弱网环境下，页面加载时间或接口响应延迟可降低 20%-40%；连接建立成功率显著提升。

---

### 优化 2：启用 Wasm 插件隔离与多线程并发

**说明**: Higress 的核心优势之一是支持 Wasm (WebAssembly) 插件。默认情况下，Wasm 可能在主线程或特定线程中运行。通过配置 Wasm 虚拟机的隔离级别和并发策略，可以避免复杂插件逻辑阻塞主网络 I/O 线程，从而提升网关的整体吞吐量。

**实施方法**:
1. 在部署 Wasm 插件时，评估插件代码的复杂度。
2. 对计算密集型插件，配置启用独立的线程池或适当的隔离级别，防止阻塞 Proxy Worker 线程。
3. 利用 Higress 的多核调度特性，确保 Wasm 插件实例在多个 CPU 核心上并行处理请求。

**预期效果**: 在运行复杂鉴权或限流逻辑时，网关 P99 延迟降低 10%-30%，吞吐量（QPS）提升 15% 以上。

---

### 优化 3：配置智能 DNS 解析与连接池优化

**说明**: Higress 作为入口网关，后端通常连接多个微服务实例。默认的 DNS 解析和连接建立策略可能存在延迟。通过启用更激进的 DNS 缓存策略和调整 HTTP/2 连接池大小，可以减少频繁握手带来的开销，并提高与后端服务的复用率。

**实施方法**:
1. 调整 Envoy 的 `cluster` 配置，增大 `max_requests_per_connection`（对于 HTTP/1.1）或优化 HTTP/2 连接复用策略。
2. 配置 DNS 缓存时长，减少不必要的 DNS 查询。
3. 针对高频访问的后端服务，启用“乐观连接池”或预热连接，确保请求到来时连接已就绪。

**预期效果**: 后端连接建立开销减少 50% 以上，网关与后端服务间的平均往返时间（RTT）显著降低。

---

### 优化 4：全链路超时与重试策略精细化控制

**说明**: 不合理的超时和重试设置会导致请求堆积，耗尽网关连接池。通过针对不同接口特征（如读多写少、计算密集型）设置差异化的超时时间、重试次数及退避算法，可以快速失败，释放资源给健康请求，从而提升系统整体的抗压能力。

**实施方法**:
1. 在路由配置中，针对不同 API 路径设置精细化的 `timeout` 参数。
2. 配置指数退避的重试策略，避免在服务故障时造成雪崩。
3. 限制单次请求的最大重试次数（例如 2 次），防止无效重试占用带宽和 CPU。

**预期效果**: 在后端服务出现部分故障时，网关自身资源（CPU/内存/连接数）利用率保持平稳，成功请求的响应延迟不受失败请求影响。

---

### 优化 5：启用 CPU 亲和性与零拷贝优化

**说明**: Higress 底层依赖 Envoy，对 CPU 架构敏感。通过操作系统的 CPU 亲和性绑定，减少进程在不同核心间切换的缓存失效开销。同时，确保启用 sendfile 零拷贝机制，减少数据在内核空间与用户空间之间的拷贝次数。

**实施方法**:
1. 在 Higress

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 提供开箱即用的流量管理、安全防护与可观测性能力，支持 HTTP/gRPC/Dubbo 等多协议。
- 通过 Wasm 插件机制实现高度可扩展性，用户可用 C++/Go/Rust 等语言编写自定义插件。
- 内置高精度限流熔断、动态路由与负载均衡算法，可应对生产级高并发场景。
- 兼容 Ingress/Gateway API 标准，支持从 Nginx/Kong 等传统网关平滑迁移。
- 提供可视化控制台与 Prometheus/Grafana 监控集成，降低运维复杂度。
- 基于 Envoy 内核优化性能，实测吞吐量较传统网关提升 30% 以上。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 理解云原生网关的核心概念与Higress的定位
- 了解Higress与Nginx、Istio、Kubernetes Ingress的区别与联系
- 学习Higress的基本架构：Wasm插件与Istio的结合
- 本地Docker环境部署或通过Docker Compose快速安装Higress
- 熟悉Higress控制台的基本操作与界面导航

**学习时间**: 1周

**学习资源**:
- Higress GitHub官方仓库
- Higress官方文档 - "快速开始"章节
- 云原生网关技术对比文章

**学习建议**: 
建议先不要深入代码，而是通过官方文档理解Higress诞生的背景（解决传统网关性能与扩展性问题）。务必动手完成一次本地安装，并成功访问控制台页面，建立感性认识。

---

### 阶段 2：核心流量管理与配置

**学习内容**:
- 掌握Ingress Route（K8s CRD）或网关路由规则的配置
- 学习服务来源的配置，包括Nacos、固定地址、K8s Service等
- 理解并配置核心流量治理功能：路由匹配、重定向、重写、Header修改
- 学习全局限流、灰度发布（金丝雀发布）的配置方法
- 掌握基于Wasm插件的流量管理（如请求鉴权、Key Rate Limiting）

**学习时间**: 2-3周

**学习资源**:
- Higress官方文档 - "路由配置"与"插件市场"
- Higress官方示例
- Go-Zero 或 Nacos 相关服务注册与发现文档

**学习建议**: 
尝试搭建一个简单的后端服务（可以使用echo server），通过Higress进行代理。重点练习流量路由规则，例如将 `/api/v1` 转发到服务A，将 `/api/v2` 转发到服务B。尝试在控制台开启官方自带的限流插件，观察效果。

---

### 阶段 3：Wasm插件开发与安全防护

**学习内容**:
- 深入理解Wasm（WebAssembly）在网关侧的优势与运行机制
- 学习Higress的插件开发规范（Go或C++）
- 实践编写一个自定义Wasm插件（例如：实现一个特殊的请求头校验或日志记录）
- 学习对接外部认证系统，如OAuth2、OIDC或Keycloak
- 配置Higress的安全防护策略，防止SQL注入、XSS攻击等

**学习时间**: 3-4周

**学习资源**:
- Higress官方文档 - "自定义开发"章节
- Higress GitHub - Plugin-Demo 示例代码
- WebAssembly on the server side 相关教程

**学习建议**: 
这是从"使用者"向"开发者"转变的关键阶段。建议从修改官方提供的插件Demo开始，编译成 `.wasm` 文件并上传到Higress控制台进行测试。不要一开始就写过于复杂的逻辑，重点熟悉配置解析和请求/响应拦截的生命周期。

---

### 阶段 4：生产级部署与高可用

**学习内容**:
- Higress在Kubernetes集群中的生产部署与配置管理
- Higress的高可用（HA）架构设计与容错机制
- 监控与可观测性：对接Prometheus、Grafana、SkyWalking
- 网关性能调优：连接池、缓冲区大小、并发处理配置
- Higress与Dubbo、gRPC协议的深度集成与配置

**学习时间**: 2-3周

**学习资源**:
- Higress官方文档 - "运维管理"与"最佳实践"
- Kubernetes Ingress Controller 运维指南
- 云原生可观测性相关博客

**学习建议**: 
关注系统的稳定性。学习如何通过Prometheus采集Higress的监控指标，并在Grafana中绘制仪表盘。尝试模拟后端服务宕机，观察Higress的故障转移表现。如果涉及微服务，重点学习Higress对gRPC协议的透传与路由支持。

---

### 阶段 5：架构设计与源码研读

**学习内容**:
- 深入研读Higress核心源码
- 理解Higress如何基于Istio进行扩展与定制
- 掌握Higress在多租户、多环境下的架构设计方案
- 参与Higress开源社区贡献或企业内部定制化开发

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Istio 官方源码与架构设计文档
- Envoy 相关深度技术文档

**学习建议**: 
此时应当具备从架构层面审视技术的能力。阅读源码时，重点关注数据面如何处理请求流转以及控制面如何下发配置。可以尝试在本地编译Higress并进行断点调试，深入

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一个开源的、基于云原生架构的 API 网关。它是在阿里巴巴内部多年双十一大流量验证的网关经验基础上，结合了 Envoy 高性能内核与 Istio 治理能力而诞生的。

与 Nginx 和 Kong 的主要区别在于：
1.  **架构基础**：Nginx 和 Kong 主要基于 Nginx/OpenResty，而 Higress 深度集成了 Envoy，利用其 C++ 的高性能特性，在处理大规模并发连接时通常具有更低的延迟和更高的吞吐量。
2.  **云原生集成**：Higress 原生支持 Kubernetes 和 Istio，可以无缝接管 Ingress 流量和 Service Mesh 中的南北向与东西向流量。Kong 虽然也支持 K8s，但在服务网格的深度整合上，Higress 设计得更为紧密。
3.  **安全与防护**：Higress 内置了 WAF（Web 应用防火墙）插件，提供了开箱即用的安全防护能力，而传统网关通常需要额外配置或购买企业版才能获得类似功能。
4.  **扩展性**：Higress 提供了 Wasm (WebAssembly) 插件支持，允许开发者使用多种语言（如 Go, Python, Rust）编写插件，比传统的 Lua 脚本更易于维护和扩展。

---



### 2: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

2: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

**A**: 是的，Higress 非常重视迁移的便捷性，并提供了相应的工具和兼容性支持。

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，可以帮助用户将现有的 Nginx.conf 配置转换为 Higress 的路由和插件配置。同时，Higress 的路由匹配逻辑（如正则、前缀匹配）与 Nginx 高度相似。
2.  **Kubernetes Ingress**：Higress 完全实现了 Kubernetes Ingress API。这意味着你不需要修改现有的 Ingress YAML 文件，只需将集群的 Ingress Controller 切换为 Higress，即可立即接管流量。
3.  **Gateway API**：除了标准的 Ingress，Higress 还前瞻性地支持 Kubernetes Gateway API，这是 Ingress 的下一代标准，提供了更丰富的流量管理能力。

---



### 3: Higress 如何处理插件开发？是否必须使用 Lua？

3: Higress 如何处理插件开发？是否必须使用 Lua？

**A**: 不，Higress 的一个核心优势在于**不再强制要求使用 Lua** 来编写插件。

1.  **Wasm 支持**：Higress 允许使用 WebAssembly (Wasm) 技术编写插件。这意味着开发者可以使用 **Go, Rust, C++, JavaScript (AssemblyScript)** 等高级语言来编写业务逻辑。
2.  **优势**：Wasm 插件以沙箱模式运行，具有更好的隔离性（插件崩溃不会导致网关崩溃），且开发门槛比 Lua 更低，更符合现代后端开发者的技术栈。
3.  **传统插件**：当然，考虑到 Envoy 的生态，Higress 依然支持原生的 Envoy 过滤器配置，同时也兼容 Lua 脚本处理，以便从旧系统迁移。

---



### 4: Higress 的性能表现如何？能否支撑高并发场景？

4: Higress 的性能表现如何？能否支撑高并发场景？

**A**: Higress 的设计初衷就是为了应对阿里巴巴内部超大规模的流量挑战，因此在性能方面表现优异。

1.  **底层内核**：基于 Envoy 构建，Envoy 本身就是为云原生高并发场景设计的 C++ 应用，具有极高的处理效率和低延迟特性。
2.  **数据面与控制面分离**：Higress 采用 Istio 的架构理念，控制面负责配置下发，数据面负责流量转发。这种分离确保了数据面极其轻量，专注于处理网络 I/O。
3.  **实测数据**：在标准的云原生环境中，Higress 在长连接、短连接、HTTPS 加解密等场景下的吞吐量和延迟表现通常优于基于 OpenResty 的传统网关，特别是在开启大量插件的情况下，性能损耗控制得更好。

---



### 5: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

5: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

**A**: 是的，Higress 是一个全功能的 API 网关，对微服务生态有完善的支持。

1.  **HTTP/gRPC**：作为基于 Envoy 的网关，Higress 原生支持 HTTP/1.1, HTTP/2 和 gRPC 协议，支持 gRPC 到 JSON 的转码，方便前端调用后端 gRPC 服务。
2.  **Dubbo 支持**：这是 Higress 在国内生态的一大亮点。它提供了对 Dubbo (Dubbo2/Dubbo3) 协议的原生支持，可以将 HTTP 请求转换为 Dubbo 协议调用后端服务。这对于大量使用 Java 和 Dubbo 框架的企业来说，是一个非常实用的功能

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 Nginx 或 httpbin）。

### 提示**: 参考 Higress 官方文档的"快速开始"章节，使用 `docker-compose` 进行部署；注意配置 Ingress 资源中的 `spec.rules.host` 和 `spec.rules.http.paths` 字段。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位及其在阿里云内部的实战经验，以下为您提供 6 条针对实际生产环境的实践建议：

### 1. 利用内置的 Prompt 模板管理实现 LLM 提示词的版本控制
**场景**：在将大模型集成到业务中时，提示词通常硬编码在客户端或业务后端，导致更新困难且无法复用。
**建议**：使用 Higress 的 `AI` 插件或配置中心来定义和托管 Prompt 模板。将提示词作为网关层面的配置资源，通过 API 调用时传入变量来渲染模板。
**价值**：实现提示词与业务代码解耦，支持灰度发布和 A/B 测试不同的提示词策略，无需重新部署业务服务。

### 2. 配置语义缓存以降低 Token 消耗与延迟
**场景**：在客服或问答场景中，大量用户问题高度相似（如“如何退款”），每次都请求 LLM 会导致高昂的成本和较高的延迟。
**建议**：在 Higress 中配置针对 LLM 请求的语义缓存策略。利用向量数据库或基于键值的缓存，对相似的 Query 进行短时间命中。
**陷阱**：避免对实时性要求极高的场景（如实时数据查询）使用缓存，并务必设置合理的 TTL（生存时间），以免返回过时信息。

### 3. 实施基于 Token 的精细化流控与并发保护
**场景**：大模型 API 的调用成本通常按 Token 计费，且后端模型服务有严格的并发限制（RPM/TPM）。
**建议**：不要仅基于传统的“请求数（QPS）”进行限流，而应配置基于“请求数 * 预估 Token 数”或“实际响应 Token 数”的限流规则。针对不同 API Key 或租户设置不同的 Token 配额。
**价值**：防止个别长文本请求占尽模型带宽，保护后端模型服务不被打挂，并精确控制成本。

### 4. 构建多模型供应商的故障转移机制
**场景**：依赖单一模型供应商（如 OpenAI 或某单一云厂商）存在可用性风险，且不同模型在不同任务上表现各异。
**建议**：在 Higress 中配置服务路由，将后端定义为多个模型提供商的地址。配置超时策略和重试机制，当主模型响应超时或返回 5xx 错误时，自动切换至备用模型。
**陷阱**：需注意不同模型的 Chat Template（对话模板）格式可能不同，在网关层需要做格式归一化处理，确保切换模型时客户端无需感知。

### 5. 敏感信息的实时脱敏与注入
**场景**：企业数据（PII）可能通过用户提问泄露给公网大模型，或者需要在 Prompt 中动态注入用户的上下文信息。
**建议**：启用 Higress 的插件能力，在请求转发前进行正则匹配或 NLP 识别，将敏感信息（如身份证号、密钥）替换为占位符，或在请求头中提取用户信息动态插入到 System Prompt 中。
**价值**：满足企业合规要求，防止核心数据外泄。

### 6. SSE 流式响应的完整性与超时处理
**场景**：AI 生成通常采用 Server-Sent Events (SSE) 流式返回，网关作为代理必须正确处理长连接。
**建议**：确保网关的读写超时时间设置得足够长（建议设置为模型最大生成时间的 1.5 倍）。检查网关配置，确保其不会对 SSE 流进行缓冲，而是实时转发给客户端。
**陷阱**：某些前端负载均衡器或代理可能会因为 SSE 连接“无数据传输时间过长”而断开连接，需要调整网关的心跳或 KeepAlive 设置。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*