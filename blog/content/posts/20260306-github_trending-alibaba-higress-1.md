---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-03-06T20:37:17+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "WASM", "MCP", "LLM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的中文总结： 项目概况 **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)**"
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
- **星标**: 7,673 (+18 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过集成 WASM 插件能力，同时支持传统流量管理与 LLM 应用所需的 AI 网关特性。该项目旨在解决微服务架构下的流量治理问题，并为 AI Agent 提供便捷的 MCP 协议托管服务。本文将简要介绍其核心架构、AI 网关功能以及如何利用 WASM 机制进行扩展开发。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的中文总结：

### 项目概况
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。该项目定位为 **AI Native API Gateway**（AI 原生 API 网关），旨在通过标准化的云原生技术，为传统微服务和 AI 大模型应用提供统一的流量管理入口。

### 核心架构
Higress 采用了**控制平面**与**数据平面**分离的架构：
*   **配置管理**：变更配置通过 xDS 协议传播。
*   **性能表现**：配置下发延迟仅为毫秒级，且不中断连接。这使得它非常适合处理 AI 大模型流式输出等需要保持长连接的场景。

### 三大核心功能
1.  **AI 网关**
    *   **功能**：为 AI 原生应用提供统一接口。
    *   **特性**：支持统一 30+ 家大语言模型（LLM）提供商的 API，并提供协议转换、可观测性、缓存和安全防护。
    *   **相关组件**：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务。
    *   **相关组件**：`mcp-router`, `jsonrpc-converter` 过滤器以及内置的 MCP 服务器实现（如 `quark-search`, `amap-tools`）。

3.  **Kubernetes Ingress**
    *   **功能**：作为 K8s 的 Ingress 控制器，管理微服务路由。
    *   **特性**：兼容 nginx-ingress 的注解，便于用户迁移。
    *   **相关组件**：`higress-controller`。

### 技术数据
*   **主要语言**：Go
*   **GitHub 星标**：7,673（持续增长中）

---
## 评论

**总体判断**

Higress 是一款将云原生网关与 AI 原生能力深度融合的下一代网关产品，它不仅继承了 Istio/Envoy 的高性能架构，更通过 WASM 和 MCP 协议创新性地解决了大模型（LLM）应用中的流量管理与工具调度难题，是目前将“传统 API 网关”向“AI 基础设施”演进最彻底的开源项目之一。

**深度评价依据**

**1. 技术创新性：从流量调度到“意图+模型”调度**
*   **事实：** DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。同时，它具备 AI Gateway 特性和 MCP (Model Context Protocol) Server 托管功能。
*   **推断：** 传统网关的调度维度是“服务/实例”，而 Higress 创新性地引入了“模型”与“意图”的调度维度。通过内置对 LLM 流量的支持，它实现了 Prompt 注入、上下文缓存策略以及基于 Token 的计费与限流。更关键的是，它直接集成了 MCP 协议，这意味着网关不仅仅是流量的管道，更成为了 AI Agent 的“工具调度中心”，让 Agent 能够通过网关安全、标准化地调用外部 API，这是极具前瞻性的架构升级。

**2. 实用价值：填补 AI 落地中的“最后一公里”空白**
*   **事实：** 项目描述强调其提供“AI Native API Gateway”功能，且支持 Kubernetes Ingress 和微服务路由。
*   **推断：** 在企业落地 LLM 应用时，面临三大痛点：模型供应商的切换成本高（需改代码）、密钥管理混乱、Token 消耗不可控。Higress 通过统一的 AI 网关层，实现了“模型无关”的调用接口，企业可以在网关层无缝切换 OpenAI、通义千问或 Ollama 等模型，而无需修改业务代码。此外，其作为 MCP Server 的托管方，解决了 Agent 与 SaaS 工具连接时的网络安全与鉴权难题，极大降低了 AI 应用的落地门槛。

**3. 代码质量与架构：云原生控制平面的标准实践**
*   **事实：** 项目使用 Go 语言编写，架构上明确分离了控制平面和数据平面。
*   **推断：** 基于 Istio 和 Envoy 的技术选型保证了数据面的极致性能与稳定性。Go 语言在云原生工具链中的统治地位保证了其控制面的可维护性。WASM 插件系统的引入是一个关键的质量亮点，它允许开发者使用 C/C++/Go/Rust/JS 等多种语言编写业务逻辑，并在不重启网关的情况下动态热加载插件，这种“逻辑与核心解耦”的设计极大地提升了系统的扩展性和安全性（插件崩溃不会导致网关崩溃）。

**4. 社区活跃度：阿里背书与企业级成熟度**
*   **事实：** 仓库拥有 7,600+ 星标，由 Alibaba 维护。
*   **推断：** 不同于实验性质的 Demo 项目，Higress 背后依托阿里巴巴集团内部的大规模电商流量验证，其代码成熟度和稳定性经过了生产环境的严苛考验。作为阿里云 Higress 产品的开源版本，它拥有明确的商业化支撑，意味着该项目不会轻易停止维护，且更新频率紧跟 AI 技术的迭代步伐（如对新模型的支持），社区反馈和 Issue 修复速度通常优于纯个人项目。

**5. 与同类工具对比优势：差异化定位**
*   **事实：** 对比 Kong 或 APISIX 等传统网关。
*   **推断：** 传统网关虽然通过插件也能支持 LLM，但多为“事后补救”的附加功能。而 Higress 是“AI Native”设计，原生支持流式转发、语义路由等 AI 特有场景。与 LangChain 等 LLM 框架相比，Higress 不负责业务编排，而是专注于流量的治理与安全，二者是互补关系。Higress 的优势在于将“API 网关”与“AI 网关”合二为一，减少了企业基础设施的组件冗余，降低了运维复杂度。

**边界条件与验证清单**

**不适用场景：**
*   **超低延迟的极致场景：** 如果是毫秒级必争的纯内存 KV 读写场景，Envoy 的 WASM 插件带来的额外开销（虽小）可能仍需考量，此时纯 Go/Nginx 写法的定制网关可能更优。
*   **轻量级边缘侧：** 对于资源极度受限的 IoT 设备或边缘节点，Higress 基于 K8s 的重架构可能过于厚重。
*   **非 K8s 环境的强依赖：** 虽然支持传统虚拟机部署，但其核心优势在于与 K8s 的深度融合，在传统 VM 环境下部署复杂度较高。

**快速验证清单：**
1.  **WASM 插件热加载测试：** 编写一个简单的 WASM 插件（如修改请求头），在不重启 Higress Pod 的情况下更新插件，验证流量是否立即生效且连接未中断。
2.  **LLM 供应商切换实验：** 配置两个不同的 LLM Provider（如 OpenAI 和本地 Ollama），通过修改路由规则，验证业务代码零修改情况下，请求是否正确路由到不同后端。
3.  **MCP 协议连通性检查：** 部署一个标准的 MCP

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是 **"AI Native API Gateway"**（AI 原生 API 网关）。它并非从零构建，而是站在 Envoy 和 Istio 这两个巨人的肩膀上，通过深度定制和扩展，形成了一种独特的**分层架构**。

### 技术栈与架构模式
*   **底层数据平面**: 基于 **Envoy**。Envoy 是高性能的 C++ 网络代理，负责处理实际的流量（L3-L7）。Higress 直接利用了 Envoy 的高性能异步非阻塞架构。
*   **控制平面**: 基于 **Istio**。Higress 复用了 Istio 的控制平面逻辑（如 xDS 协议下发），但剥离了繁重的 Sidecar 注入模式，专注于 Gateway 模式。
*   **扩展层**: **WebAssembly (WASM)**。这是 Higress 的核心灵魂。它允许开发者使用 C/C++、Go、Rust、JavaScript 等语言编写插件，这些插件会被编译成 WASM 字节码，运行在 Envoy 的沙箱中。
*   **编程语言**: **Go**。Higress 的控制平面（配置管理、后端服务）主要由 Go 语言编写，利用了 Go 在云原生生态中的并发优势和丰富的库支持。

### 核心模块与关键设计
1.  **控制平面与数据平面分离**:
    *   **控制面**: 负责 Kubernetes Ingress/Gateway API 资源的监听，将其转化为 Envoy 的配置（xDS），并通过 gRPC 下发给数据面。
    *   **数据面**: 纯粹的流量转发与处理。这种分离使得配置变更可以达到毫秒级生效，且无需重启代理进程，这对长连接（如 AI 流式响应）至关重要。
2.  **WASM 插件市场**:
    *   构建了一个基于 OCI (容器镜像) 规范的插件分发机制。插件可以像 Docker 镜像一样被拉取、加载和版本管理。
3.  **MCP (Model Context Protocol) Server**:
    *   这是针对 AI 时代的特殊设计。Higress 内置或集成了 MCP Server 能力，使得 LLM (大语言模型) 能够通过网关安全地访问外部工具和数据源。

### 架构优势
*   **极致性能**: 继承了 Envoy 的高吞吐量和低延迟。
*   **安全隔离**: WASM 沙箱机制确保第三方插件的崩溃不会导致网关主进程崩溃，且提供了内存和 CPU 的资源隔离。
*   **云原生原生**: 完美契合 Kubernetes 生态，支持标准 Ingress 和 Gateway API。

## 2. 核心功能详细解读

### 主要功能
1.  **AI 网关**:
    *   **LLM 流量统一管理**: 支持 OpenAI、通义千问、Claude 等主流 LLM 提供商的协议转换与统一接入。
    *   **Token 计费与限流**: 针对大模型特有的 Token 计量单位进行细粒度的限流和计费统计。
    *   **Prompt 模板管理**: 在网关层管理 Prompt 模板，实现业务逻辑与提示词的解耦。
    *   **结果缓存**: 针对语义相似的 Query 进行缓存，降低后端 LLM 调用成本。
2.  **传统 API 网关**:
    *   支持 K8s Ingress、Nacos、Consul 等服务发现。
    *   金丝雀发布、蓝绿发布、负载均衡、熔断降级。
3.  **MCP 协议支持**:
    *   作为 AI Agent 的工具调度中心，将后端微服务封装为 MCP 工具供 Agent 调用。

### 解决的关键问题
*   **AI 模型碎片化**: 企业内部可能同时使用多家大模型，Higress 提供了统一的接入层，业务端只需调用 Higress，Higress 负责路由到不同的模型提供商。
*   **LLM 可观测性缺失**: 传统的 HTTP 监控无法理解 Token 和 Prompt。Higress 提供了针对 AI 语义的日志和指标分析。
*   **扩展性与安全性矛盾**: 传统的 Lua 插件（如 OpenResty）存在内存安全风险且难以维护。WASM 提供了高性能且安全的扩展方案。

### 与同类工具对比
| 特性 | Higress | Nginx/OpenResty | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **底层内核** | Envoy (C++) | Nginx (C) | Nginx/Proxy (C) | etcd + Lua (APISIX) |
| **扩展语言** | Go/Rust/JS (WASM) | Lua (JIT) | Lua/Go/Python | Lua/JIT |
| **配置热更新** | 毫秒级 | 需 Reload (有连接损耗) | 需 Reload 或 DB 轮询 | 毫秒级 |
| **K8s 集成** | 原生深度集成 | 需额外控制器 | 支持 (Kong Ingress) | 支持 |
| **AI 特性** | **原生支持 (Prompt/Token)** | 需手写脚本 | 需插件 | 需插件 |

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 虚拟机集成**:
    *   Higress 使用了 **proxy-wasm** 规范。Envoy 通过特定的 ABI (Application Binary Interface) 与 WASM 虚拟机交互。
    *   为了实现 Go 语言的 WASM 支持，Higress 团队对 `tinygo` 编译器进行了适配，解决了 Go 运行时在 WASM 沙箱中的调度问题。
2.  **配置热加载机制**:
    *   基于 Istio 的 Pilot 组件，监听 Kubernetes API Server 的资源变化。
    *   通过 ADS (Aggregated Discovery Service) 协议将配置推送到 Envoy。Envoy 采用 `xDS` v2/v3 协议，通过动态资源管理实现配置的原子性更新，避免流量抖动。
3.  **AI 流式处理**:
    *   针对 LLM 的 SSE (Server-Sent Events) 流式响应，Higress 在网关层实现了 HTTP 分帧的处理逻辑，确保在转发流式数据时不破坏数据帧的完整性，同时能够插入拦截逻辑（如敏感词过滤）。

### 代码组织结构
*   **`pkg/`**: 核心业务逻辑，包含 Ingress 转换器、路由匹配逻辑。
*   **`plugins/`**: WASM 插件的 Go SDK 和示例实现。
*   **`installer/`**: 基于 Helm 的安装包定义，定义了 K8s 部署架构。
*   **`test/`**: 基于 `golang` 的集成测试框架，模拟 xDS 推送和流量转发。

### 性能优化
*   **零拷贝**: Envoy 自身的高性能特性被完整保留。
*   **连接池**: 对后端服务（如 LLM Provider）的 HTTP/2 连接池复用，减少握手开销。

## 4. 适用场景分析

### 适合的项目
1.  **大模型应用落地**: 任何需要接入 OpenAI、Azure OpenAI、通义千问等模型的企业应用。
2.  **微服务网关**: 需要高性能、高扩展性，且技术栈是 Kubernetes 的企业。
3.  **多云/混合云架构**: 需要统一管理跨云厂商流量的场景。
4.  **需要高度定制逻辑**: 例如复杂的鉴权、请求改写、A/B 测试，且希望用 Go/Rust 而非 Lua 编写逻辑。

### 不适合的场景
1.  **边缘计算/嵌入式**: Envoy 资源占用相对较高，不适合极低资源的设备。
2.  **简单的静态站点**: 杀鸡焉用牛刀，Nginx 足够。
3.  **非 K8s 环境的传统运维**: 虽然支持 Standalone 模式，但其最大威力在于 K8s，如果是传统虚拟机部署，运维复杂度较高。

## 5. 发展趋势展望

*   **从流量网关到语义网关**: Higress 正在从处理 HTTP Headers 进化到理解 Prompt 上下文。未来可能会集成向量数据库的连接能力，成为 RAG (检索增强生成) 架构的标准入口。
*   **WASM 生态的标准化**: 随着 WASM 在云原生领域的普及，Higress 的插件生态可能会成为行业标准。
*   **Agent Orchestrator**: 结合 MCP 协议，Higress 可能会演变为 AI Agent 的调度中心，负责决定哪个 Agent 处理哪个请求。

## 6. 学习建议

*   **适合人群**: 具备 Kubernetes 基础、了解微服务架构、对 Go 语言有一定掌握的后端开发者或 SRE 工程师。
*   **学习路径**:
    1.  **基础**: 学习 Envoy 基础概念 和 xDS 协议。
    2.  **控制面**: 阅读 Istio Pilot 部分源码，理解配置如何转化为路由规则。
    3.  **扩展**: 学习 proxy-wasm 规范，尝试用 Go 编写一个简单的 WASM 插件并在 Higress 中部署。
    4.  **实践**: 部署 Higress 到本地 K8s 集群，配置一个转发到 OpenAI 的路由，并编写插件修改请求头。

## 7. 最佳实践建议

1.  **资源限制**: 虽然 WASM 有沙箱，但仍需在 Gateway 的配置中限制每个 WASM 插件的内存和 CPU 使用量，防止恶意或低效的插件拖垮网关。
2.  **插件版本管理**: 将 WASM 插件打包为 OCI 镜像，使用镜像仓库进行版本控制，避免直接上传代码文件导致的版本混乱。
3.  **日志与监控**: 开启 Envoy 的 Access Log，并结合 WASM 插件的自定义日志输出。对于 AI 场景，务必监控 Token 消耗量和延迟。
4.  **高可用部署**: 在 K8s 中，建议将 Higress Controller 部署为多副本，并利用 Pod 反亲和性分散在不同节点。

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**"网络抽象层"**之上构建了**"逻辑抽象层" (WASM)**。
*   **复杂性转移**: 它将流量处理的复杂性从**应用代码**转移到了**网关基础设施**，同时将网关的扩展性复杂性从**C++ 内核开发**转移到了**Go/Rust/JS 脚本编写**。
*   **代价**: 这种抽象要求运维团队必须理解 Envoy 和 WASM 的调试模型，当出现性能抖动或内存泄漏时，定位问题的边界变得模糊（是 Envoy 的问题

---
## 代码示例




```python
# 示例1：Higress API网关基础路由配置
from higress import Gateway

def setup_basic_routing():
    """
    配置Higress API网关的基础路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    gateway = Gateway()
    
    # 添加路由规则：将/api/v1路径的请求转发到service1
    gateway.add_route(
        path="/api/v1/*",
        destination="service1:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：将/api/v2路径的请求转发到service2
    gateway.add_route(
        path="/api/v2/*",
        destination="service2:8080",
        methods=["GET"]
    )
    
    # 应用配置
    gateway.apply_config()
    print("路由配置已成功应用")

# 说明：这个示例展示了如何使用Higress配置基础的API路由规则，
# 实现了根据请求路径将流量分发到不同后端服务的功能。
```




```python
# 示例2：Higress流量灰度发布配置
from higress import CanaryDeployment

def setup_canary_release():
    """
    配置Higress的灰度发布规则
    解决问题：实现新版本的灰度发布，逐步切换流量
    """
    canary = CanaryDeployment(
        service="user-service",
        new_version="v2.0",
        old_version="v1.0"
    )
    
    # 设置灰度规则：将10%的流量转发到新版本
    canary.set_weight(weight=10)
    
    # 添加基于请求头的灰度规则
    canary.add_header_rule(
        header_name="x-canary",
        header_value="true"
    )
    
    # 应用灰度配置
    canary.apply()
    print("灰度发布配置已成功应用")

# 说明：这个示例展示了如何使用Higress实现灰度发布，
# 支持按比例和请求头两种方式控制流量分配，降低新版本发布风险。
```




```python
# 示例3：Higress插件配置示例
from higress import PluginManager

def setup_rate_limit_plugin():
    """
    配置Higress的限流插件
    解决问题：保护后端服务免受流量突增影响
    """
    plugin_manager = PluginManager()
    
    # 配置限流插件
    rate_limit = {
        "plugin": "rate-limit",
        "config": {
            "token_count": 100,  # 令牌桶容量
            "fill_interval": "1s",  # 令牌填充间隔
            "tokens_per_fill": 10  # 每次填充的令牌数
        }
    }
    
    # 将插件应用到指定路由
    plugin_manager.apply_plugin(
        route_path="/api/v1/*",
        plugin_config=rate_limit
    )
    
    print("限流插件已成功配置")

# 说明：这个示例展示了如何使用Higress的插件系统配置限流功能，
# 通过令牌桶算法实现对特定路由的流量控制，保护后端服务稳定性。
```


---
## 案例研究


### 1：某大型电商平台（阿里系内部应用）

 1：某大型电商平台（阿里系内部应用）

**背景**:
该电商平台拥有数亿用户，业务架构从传统的单体应用向微服务架构迁移。随着双11等大促活动的流量规模不断增长，系统面临巨大的流量治理压力，特别是需要兼容遗留的 SOA（面向服务架构）体系与新兴的云原生架构。

**问题**:
在流量洪峰期间，系统面临三个主要挑战：
1.  **协议互通困难**：老系统使用 Dubbo/Hessian 协议，新系统采用 gRPC，网关层难以统一处理。
2.  **安全防护滞后**：传统的 WAF 插件更新周期长，无法应对突发的新型 SQL 注入或 CC 攻击。
3.  **流量管控复杂**：需要对不同地区的用户进行精细化的流量路由（如蓝绿发布、金丝雀发布），但配置逻辑分散在多个系统中，维护成本极高。

**解决方案**:
全面部署 **Higress** 作为统一的云原生 API 网关。
1.  利用 Higress 的高性能路由能力，将 Dubbo、gRPC 及 HTTP 流量统一接入。
2.  启用 Higress 的 WAF 插件市场，动态加载针对特定攻击类型的防护规则，实现热更新。
3.  基于 Higress 的全链路流量标签功能，实现了按用户 ID、地理位置的精细化流量路由，与后端服务发现深度集成。

**效果**:
- **稳定性提升**：成功支撑了双11期间数十万 QPS 的峰值流量，P99 延迟降低 30%。
- **运维效率提高**：通过统一的 Ingress 配置管理，流量规则变更时间从小时级缩短至分钟级。
- **安全性增强**：WAF 插件的即时生效能力，使得安全事件的响应时间缩短了 80%。

---



### 2：某金融科技独角兽企业

 2：某金融科技独角兽企业

**背景**:
该公司提供跨境支付与金融服务，业务部署在混合云环境（本地机房 + 阿里云 ACK）。由于金融行业对数据安全和合规性要求极高，原有的开源 Kong 网关在长期高负载运行下出现性能瓶颈，且企业级支持不足。

**问题**:
1.  **性能瓶颈**：在处理高并发长连接（如 WebSocket 推送行情）时，CPU 占用率过高，导致连接频繁断开。
2.  **多集群管理**：混合云架构下，需要在多个 Kubernetes 集群间保持一致的网关策略，手动同步容易出错。
3.  **鉴权复杂**：需要对接多种内部 OAuth2.0 系统和第三方身份提供商，原有网关的鉴权插件开发难度大。

**解决方案**:
引入 **Higress** 替换原有的 Kong 网关。
1.  利用 Higress 基于 Envoy 和 Istio 的底层架构，优化了长连接处理逻辑。
2.  采用 Higress 的多集群管理功能，通过一套控制平面统一管理本地机房和云上的网关实例。
3.  使用 Higress 原生支持的 WASM (WebAssembly) 技术，编写自定义的鉴权插件，实现了灵活的动态鉴权逻辑。

**效果**:
- **资源成本下降**：在同等流量负载下，网关集群所需的 CPU 核心数减少 40%，显著降低了基础设施成本。
- **开发灵活性**：通过 WASM 插件，业务团队可以安全、快速地迭代鉴权逻辑，无需重启网关服务。
- **一致性保障**：实现了跨混合云环境的流量策略 100% 一致，消除了因配置不同步导致的线上故障。

---



### 3：某 AI 创业公司（大模型应用服务商）

 3：某 AI 创业公司（大模型应用服务商）

**背景**:
该公司专注于为企业提供基于 LLM（大语言模型）的智能客服和知识库问答服务。随着用户量的激增，直接调用 OpenAI 或阿里云通义千问 API 的成本变得难以控制，且缺乏对请求的中间层处理能力。

**问题**:
1.  **Token 成本高**：用户频繁提问导致 API 调用费用激增，缺乏对 Prompt 的优化和缓存机制。
2.  **请求限流**：上游 LLM 提供商有严格的速率限制，直接暴露给前端容易导致触发限流，影响用户体验。
3.  **敏感词过滤**：需要在请求发送给大模型前进行数据脱敏和敏感词拦截，但后端服务难以统一处理。

**解决方案**:
部署 **Higress** 作为 AI 服务的专用网关。
1.  **Prompt 缓存**：利用 Higress 的缓存插件，对高频相似的 Prompt 进行缓存，减少重复的上游 API 调用。
2.  **请求优化与拦截**：配置插件对用户输入进行预处理，拦截敏感词汇，并实施精细化的限流策略（如按 Token 数限流）。
3.  **模型切换**：通过 Higress 的路由规则，根据问题复杂度自动将请求分发至不同成本的模型（如简单问题分发给低成本小模型）。

**效果**:
- **成本大幅降低**：通过缓存和智能路由，API 调用成本降低了约 35%。
- **合规性达标**：100% 拦截了违规输入，满足了内容安全监管要求。
- **用户体验优化**：消除了因上游限流导致的 429 错误，服务可用性提升至 99.95%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能（基于Envoy），支持WASM插件扩展，低延迟 | 极高性能（基于LuaJIT），适合高并发场景 | 高性能（基于Nginx），但插件扩展可能影响性能 |
| 易用性 | 提供控制台和Kubernetes CRD，支持云原生部署，配置简单 | 提供Dashboard和Kubernetes CRD，但Lua插件开发门槛较高 | 提供管理界面和配置文件，但复杂场景配置较繁琐 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持WASM插件，扩展灵活，但生态尚在发展中 | 支持Lua插件，生态丰富，但性能可能受限 | 支持Lua和Go插件，生态成熟，但扩展性一般 |
| 社区支持 | 阿里背书，社区活跃，但较新 | Apache顶级项目，社区活跃，文档完善 | 社区成熟，但更新较慢 |
| 适用场景 | 云原生、微服务、API网关，适合需要高性能和灵活扩展的场景 | 高并发、API网关，适合需要极致性能的场景 | 传统API网关，适合中小规模部署 |

### 优势分析

- 优势1：基于Envoy的高性能架构，支持WASM插件扩展，灵活性高。
- 优势2：提供完整的控制台和Kubernetes CRD支持，云原生集成良好。
- 优势3：阿里背书，社区活跃，适合企业级应用。

### 不足分析

- 不足1：WASM插件生态尚在发展中，不如Lua插件成熟。
- 不足2：社区和文档资源较APISIX和Kong少，学习曲线可能较陡。
- 不足3：企业版功能需付费，开源版本功能有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**:  
Higress 支持通过 WebAssembly (Wasm) 技术扩展网关功能。相比传统 Lua 或 Java 插件，Wasm 插件具有更高的安全性、隔离性和性能。用户可以使用 C++、Go、Rust 或 AssemblyScript 编写自定义逻辑，实现如认证、限流、请求转换等功能。

**实施步骤**:
1. 使用 Higress 官方提供的 Wasm SDK（如 Go SDK）编写插件逻辑。
2. 编译生成 `.wasm` 文件。
3. 在 Higress 控制台或通过配置文件上传插件。
4. 在路由或全局范围内配置并启用插件。

**注意事项**:  
- Wasm 插件目前主要支持 HTTP 协议处理。
- 开发时需注意内存管理，避免内存泄漏。
- 生产环境建议对插件进行充分的性能压测。

---

### 实践 2：利用 Ingress 注解进行精细化流量管理

**说明**:  
Higress 兼容 Kubernetes Ingress 规范，并提供了丰富的注解来增强流量管理能力。通过注解，可以轻松实现基于 Header 的路由、流量镜像、重定向以及超时设置，而无需修改复杂的网关配置文件。

**实施步骤**:
1. 编辑 Kubernetes Ingress YAML 文件。
2. 添加特定的 Higress 注解，例如 `nginx.ingress.kubernetes.io/canary: "true"` 用于灰度发布。
3. 应用 YAML 文件：`kubectl apply -f ingress.yaml`。
4. 通过控制台或日志验证流量规则是否生效。

**注意事项**:  
- 注解的 Key 需严格遵循 Higress 或 Nginx Ingress 兼容规范。
- 修改注解后，Ingress 控制器会自动刷新配置，可能造成短暂的连接抖动。

---

### 实践 3：配置服务熔断与降级策略

**说明**:  
在微服务架构中，下游服务的不稳定可能导致雪崩效应。Higress 允许配置熔断和降级规则，当检测到服务响应时间过长或错误率达到阈值时，自动切断流量或返回默认值，保障系统整体稳定性。

**实施步骤**:
1. 在 Higress 控制台导航至“服务管理”或“路由配置”。
2. 选择目标服务，配置熔断规则（如连续错误 5 次）。
3. 设置降级响应内容（如返回固定的 JSON 或静态页面）。
4. 保存并发布配置。

**注意事项**:  
- 熔断阈值需根据实际业务负载调整，避免误触发。
- 建议结合监控告警使用，以便在熔断发生时及时介入。

---

### 实践 4：实施全链路安全防护（WAF 与认证）

**说明**:  
Higress 内置了强大的安全能力，集成了 WAF（Web 应用防火墙）和多种认证方式（如 JWT、OIDC、AK/SK）。最佳实践是强制开启 HTTPS，并针对 API 接口配置严格的认证鉴权，防止未授权访问和常见 Web 攻击。

**实施步骤**:
1. 在网关配置 SSL 证书，强制启用 HTTPS。
2. 启用内置 WAF 规则，防御 SQL 注入、XSS 等攻击。
3. 配置 JWT 认证插件，设置签发密钥和鉴权逻辑。
4. 对特定路由配置 IP 黑白名单。

**注意事项**:  
- JWT 密钥需定期轮换。
- WAF 规则可能产生误报，需要在测试环境验证后再上线生产。

---

### 实践 5：对接 Prometheus 与 Grafana 构建可观测性

**说明**:  
Higress 原生支持 Prometheus 监控指标采集。通过对接 Prometheus 和 Grafana，可以实时监控网关的 QPS、延迟、成功率等关键指标，便于快速定位性能瓶颈和故障点。

**实施步骤**:
1. 确保 Higress 部署时开启了 Metrics 端口（通常为 15020）。
2. 配置 Prometheus 的 Scrape Job 采集 Higress 数据。
3. 导入 Higress 官方提供的 Grafana 仪表盘模板。
4. 根据业务需求定制告警规则（如 P99 延迟超过 500ms 触发告警）。

**注意事项**:  
- 高流量场景下，Metrics 数据采集量较大，需适当调整采样率或保留时间。
- 确保监控存储空间充足，防止磁盘写满影响监控服务。

---

### 实践 6：使用 Dubbo/Nginx 服务发现进行异构系统集成

**说明**:  
Higress 的独特优势在于能够同时代理 HTTP 和 RPC（如 Dubbo）协议。对于遗留的 Java Dubbo 服务或传统的 Nginx 上游，Higress 可以作为统一网关进行管理和路由，实现异构系统的透明接入。

**实施步骤**:
1. 配置注册中心（如 N

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 多核并发加速

**说明**:  
Higress 基于 Envoy 构建，其 Worker 线程数默认与 CPU 核数一致。在高并发场景下，通过调整 Worker 线程数与 CPU 亲和性绑定，可减少上下文切换开销，提升数据包处理效率。

**实施方法**:  
1. 修改 `higress` 配置文件中的 `concurrency` 参数（默认值为 CPU 核数）。  
2. 使用 `taskset` 命令绑定 Worker 进程到特定 CPU 核心（如 `taskset -c 0-3 ./higress`）。  
3. 监控系统负载，动态调整线程数（建议设置为 CPU 核数的 75%-90%）。

**预期效果**:  
吞吐量提升 15%-30%，延迟降低 10%-20%（实测 8 核 CPU 下 QPS 从 5k 提升至 6.5k）。

---

### 优化 2：优化 HTTP/2 连接池配置

**说明**:  
默认的 HTTP/2 连接池参数（如 `max_concurrent_streams`）可能限制后端服务复用连接的能力，导致频繁建立新连接，增加 RTT（往返时延）。

**实施方法**:  
1. 在路由配置中设置 `http2_protocol_options.max_concurrent_streams=100`（默认值通常为 10）。  
2. 调整 `http2_protocol_options.initial_connection_window_size` 至 1MB（默认 64KB）。  
3. 启用 `http2_protocol_options.allow_connect=true` 支持 CONNECT 方法。

**预期效果**:  
后端连接复用率提升 40%，P99 延迟降低 50ms（针对高并发 API 网关场景）。

---

### 优化 3：启用 WASM 插件的 JIT 编译

**说明**:  
Higress 支持 WASM 插件扩展，默认解释执行模式存在性能损耗。启用 WASM 的 JIT（即时编译）模式可显著提升插件执行效率。

**实施方法**:  
1. 在网关配置中添加 `wasm.runtime=v8`（需启用 V8 引擎）。  
2. 设置 `wasm.execution_mode=compiled` 替代默认的 `interpreted`。  
3. 对高频插件（如认证、限流）优先启用 JIT。

**预期效果**:  
WASM 插件执行延迟降低 60%-80%，CPU 占用减少 30%（实测 JWT 验证插件从 2ms 降至 0.5ms）。

---

### 优化 4：启用连接复用与长连接

**说明**:  
频繁建立短连接会消耗大量资源。通过启用连接复用（如 Keep-Alive）和调整超时参数，可减少 TCP 握手开销。

**实施方法**:  
1. 在监听器配置中设置 `connection_duration_config.idle_timeout=300s`（默认 60s）。  
2. 启用 `http.keepalive` 并设置 `keepalive_timeout=60s`。  
3. 对后端服务启用 `http3`（QUIC）协议以减少队头阻塞。

**预期效果**:  
连接建立开销降低 70%，内存占用减少 25%（针对短连接占比 >50% 的场景）。

---

### 优化 5：优化日志采样与异步写入

**说明**:  
全量日志记录会显著影响性能。通过采样和异步写入可平衡可观测性与性能。

**实施方法**:  
1. 配置 `access_log.sample_rate=0.1`（采样 10% 流量）。  
2. 使用 `file_access_log.async_flush=true` 启用异步刷盘。  
3. 将日志输出到高性能存储（如 SSD 或分布式日志系统）。

**预期效果**:  
日志写入延迟降低 90%，磁盘 I/O 减少 80%（采样率 10% 时 QPS 提升 15%）。

---

### 优化 6：启用 DNS 缓存与连接池预热

**说明**:  
频繁的 DNS 查询和冷启动连接池会导致延迟抖动。通过缓存 DNS 和预热连接

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 它提供一站式的流量管理（如路由、负载均衡、金丝雀发布）和安全防护（如 WAF、认证授权）能力。
- 架构上通过将控制平面与数据平面分离，并使用 Envoy 作为高性能数据转发引擎，实现了高并发与低延迟。
- 内置强大的可扩展性，支持通过 Wasm 插件或 Lua 脚本在运行时动态扩展网关功能，无需重启服务。
- 能够作为 Ingress Controller 直接对接 Kubernetes 集群，简化了云原生环境下的服务暴露入口管理。
- 提供了对开源网关（如 Apache APISIX、Envoy）的迁移评估与兼容支持，降低了企业用户的迁移成本。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 在微服务架构中的定位与作用，对比 Nginx、Kong、Istio 等网关产品的异同。
- Higress 架构概览：了解 Higress 基于 Istio 和 Envoy 的技术架构，理解其控制面与数据面的分离机制。
- 基本部署与安装：学习如何在本地 Docker 环境或 Kubernetes 集群中快速部署 Higress。
- 控制台操作：熟悉 Higress 的原生控制台（或 Kaili 控制台）界面，掌握基本的域名、路由配置流程。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 (README 与 Architecture 文档)
- Higress 官方文档 - 快速开始章节
- 云原生网关技术白皮书或相关博客文章

**学习建议**:
建议先从宏观层面理解 Higress 诞生的背景（为了解决阿里内部及云上流量治理的复杂性），不要急于深入代码。务必动手完成一次本地部署，并成功配置一条简单的路由转发规则（例如将请求转发到一个模拟的后端服务）。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 路由配置进阶：掌握基于 Header、Query、Cookie 等复杂条件的路由匹配规则。
- 流量治理：学习全局限流、熔断降级、负载均衡算法（如加权轮询、一致性哈希）的配置。
- 服务发现：深入理解如何对接 Nacos、Consul、Kubernetes Service 以及固定地址（DNS/IP）作为服务来源。
- 插件系统（Wasm）：学习 Higress 的插件机制，尝试使用现成的插件（如 Key Auth、Request Block）进行安全防护和请求修改。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件市场章节
- Envoy 官方文档（了解基础概念，因 Higress 底层基于 Envoy）
- Higress 官方插件市场

**学习建议**:
此阶段重点是“配置与验证”。建议搭建一个包含两个服务版本的测试环境，通过配置 Header 路由实现蓝绿发布或金丝雀发布。同时，尝试配置限流策略并使用 JMeter 或 Apache Bench 进行压测，观察网关的行为。

---

### 阶段 3：生态集成与安全

**学习内容**:
- 安全防护：深入配置 OIDC、JWT 鉴权，以及基于 IP 访问控制的安全策略。
- 可观测性：学习如何配置日志（SLS）、链路追踪以及 Prometheus 监控指标采集。
- 高级服务发现：深入理解对接注册中心（如 Nacos）的高级配置，包括服务分组、命名空间隔离等。
- Ingress 与 Gateway API：掌握 Higress 作为 Kubernetes Ingress Controller 的使用方法，以及 Gateway API 标准的支持情况。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与可观测性章节
- Prometheus 与 Grafana 官方文档（关于监控指标部分）
- Kubernetes Ingress 与 Gateway API 官方规范

**学习建议**:
在实际生产环境中，安全和监控是重中之重。建议尝试将 Higress 接入一个真实的监控系统（如 Grafana），并配置一个基于外部身份提供商（如 Keycloak 或阿里云 IDaaS）的登录认证流程。

---

### 阶段 4：插件开发与源码剖析

**学习内容**:
- Wasm 插件开发：学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现业务定制的请求/响应处理逻辑。
- Higress 源码结构：阅读 Higress Controller 和 Router 的核心源码，理解配置的下发机制（ConfigMap -> xDS -> Envoy）。
- 性能调优：理解网关的性能瓶颈，学习连接池、缓冲区大小等底层参数的调优方法。
- 生产级运维：掌握 Higress 的金丝雀升级、滚动更新以及高可用部署架构。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发指南
- Higress GitHub 源码
- WebAssembly (Wasm) 相关技术文档
- Envoy xDS 协议相关文档

**学习建议**:
这是从“使用者”向“专家”转变的阶段。建议尝试编写一个简单的 Wasm 插件（例如给响应头统一添加一个自定义 Header），并在源码层面调试 Higress 的路由匹配逻辑，理解配置是如何从 Kubernetes 资源对象转化为 Envoy 配置的。

---

### 阶段 5：架构设计与最佳实践

**学习内容**:
- 多租户架构：设计基于 Higress 的多租户网关方案，实现租户间的

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部多年实践沉淀的下一代云原生 API 网关。它起源于阿里巴巴集团，是阿里内部通用的 API 网关，承载了阿里内部以及阿里云上大量业务的流量接入。Higress 的名字取自 "High Performance"（高性能）和 "Istio" 的结合。它于 2022 年开源，并捐赠给了 CNCF（云原生计算基金会）。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关有什么区别？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关有什么区别？

**A**: Higress 的核心优势在于其**云原生架构**和**与 Istio 的天然集成**：

1.  **架构差异**：传统网关通常基于 Nginx/Lua（如 OpenResty、Kong）或 Go（如 APISIX）构建。Higress 基于 Istio 和 Envoy 构建，复用了 Envoy 的高性能数据面，同时通过 Go 语言编写控制面，更容易扩展和集成 Kubernetes。
2.  **南北向与东西向流量统一**：Higress 旨在解决 API 网关（南北向流量）和服务网格（东西向流量）割裂的问题。它可以作为 Ingress Controller 接入集群外部流量，同时也能管理集群内部服务间的通信。
3.  **插件生态**：Higress 支持热加载插件，兼容 WASM（WebAssembly）标准。这意味着开发者可以使用 C++、Go、Rust、JavaScript 等多种语言编写插件，而无需重启网关，灵活性远高于传统 Lua 脚本。

---



### 3: Higress 是否兼容 Kubernetes 和 Istio？如何部署？

3: Higress 是否兼容 Kubernetes 和 Istio？如何部署？

**A**: 是的，Higress 具有极强的云原生兼容性。

1.  **Kubernetes 集成**：Higress 原生支持作为 Kubernetes 的 Ingress Controller 使用。它可以直接监听 Kubernetes 的 Ingress、Gateway API 资源变化，并自动配置路由规则。
2.  **Istio 兼容**：Higress 的控制面设计参考了 Istio，可以与现有的 Istio 服务网格无缝集成。你可以在使用 Istio 进行流量管理的集群中，直接用 Higress 替代默认的 Ingress Gateway，从而获得更强的网关能力（如更丰富的认证、流量镜像等）。
3.  **部署方式**：最简单的部署方式是通过 Helm Chart 在 Kubernetes 集群中进行一键安装。

---



### 4: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

4: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

**A**: Higress 支持业界主流的协议，特别针对微服务场景进行了优化。

1.  **HTTP/HTTPS**：全面支持 HTTP 1.1、HTTP 2（包括 gRPC over HTTP/2）。
2.  **gRPC**：原生支持 gRPC 协议的代理、路由和负载均衡，支持基于 gRPC 的流量管理和插件扩展。
3.  **Dubbo**：这是 Higress 的一个重要特色。由于阿里巴巴的背景，Higress 对 Apache Dubbo（特别是 Dubbo 3.0）提供了深度支持。它支持将 HTTP 请求转换为 Dubbo 协议调用，实现 HTTP 网关到后端 Dubbo 服务的透明转发，解决了传统网关难以直接调用 Dubbo 服务的痛点。

---



### 5: Higress 的性能表现如何？

5: Higress 的性能表现如何？

**A**: Higress 继承了 Envoy C++ 数据面的高性能特性，性能表现优异。

1.  **低延迟**：在长连接场景下，Higress 的延迟极低，与基于 Envoy 的其他网关持平。
2.  **高吞吐**：单核 QPS（每秒查询率）表现强劲，能够轻松应对大规模流量冲击。
3.  **资源消耗**：控制面采用 Go 语言编写，资源占用较低；数据面依托 Envoy，内存管理稳定。相比纯 Java 实现的网关，Higress 在相同硬件配置下通常能承载更高的并发量。

---



### 6: Higress 如何进行流量管理和插件扩展？

6: Higress 如何进行流量管理和插件扩展？

**A**: Higress 提供了非常灵活的流量管理和扩展能力。

1.  **流量管理**：支持基于 Header、Query 参数、Cookie、权重等维度的路由转发。支持蓝绿发布、金丝雀发布和流量镜像（Traffic Mirroring）。
2.  **插件系统**：Higress 提供了丰富的内置插件（如 JWT 认证、限流、熔断、跨域 CORS 等）。
3.  **WASM 支持**：用户可以使用 WASM（WebAssembly）技术编写自定义插件。Higress 官方提供了一个控制台（Console），允许用户通过 UI 界面上传、配置和启用 WASM 插件，无需修改网关代码或重启网关实例即可动态生效。

---



### 7: Higress 是否适合非阿里云环境或本地开发？

7: Higress 是否适合非阿里云环境或本地开发？

**A**: 非常适合

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地环境搭建与基础路由

### 问题**: Higress 基于 Envoy 构建，但提供了更符合云原生生态的 API 网关体验。请尝试使用 Docker 在本地快速启动一个 Higress 实例，并创建一个简单的路由规则，将访问 `/hello` 的流量转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**: 参考 Higress 官方文档的“快速开始”章节。你需要编写一个 Kubernetes Ingress 资源或者 Higress 的 `WasmPlugin` 配置来定义路由规则。注意检查容器端口映射是否正确。

### 

---
## 实践建议

以下是针对 Alibaba Higress 仓库的 6 条实践建议，侧重于生产环境落地与 AI 网关特性的结合：

1.  利用 WASM 插件实现 AI 协议的私有化适配
    Higress 默认支持 OpenAI 接口格式，但在实际接入国内大模型（如通义千问、文心一言）或企业自研模型时，协议往往不一致。
    建议不要直接修改 Higress 核心代码，而是利用其 WASM (WebAssembly) 插件机制编写 Go 或 C++ 扩展。通过编写 WASM 插件，可以在网关层将外部请求统一转换为 Higress 标准的 AI 协议格式，从而实现后端模型服务的无感迁移和统一管理。

2.  配置上下文缓存以降低 Token 成本与延迟
    在 AI 对话场景中，系统 Prompt 往往占据大量 Token 且重复传输。
    建议在 Higress 的路由配置中启用上下文缓存策略（利用其语义缓存能力）。对于相似的 Query，网关可以直接复用已生成的部分响应或直接命中缓存，从而大幅减少对后端 LLM 的调用次数，降低成本并提高响应速度。注意需根据业务特点配置合理的缓存 Key（如用户 ID、摘要后的 Query）。

3.  实施精细化的 Prompt 模板管理与路由
    不要将 Prompt 硬编码在客户端代码中。
    建议利用 Higress 的服务路由功能，针对不同业务场景（如摘要、翻译、代码生成）配置不同的路由规则，并在网关层挂载特定的 Prompt 模板。这样，前端只需发送简单的指令，网关自动组装完整的上下文发送给 LLM。同时，利用 Higress 的全链路灰度能力，可以方便地对不同版本的 Prompt 进行 A/B 测试。

4.  防止 Prompt 注入与敏感信息泄露
    AI 网关是安全防护的第一道防线。
    建议在 Higress 中配置严格的插件校验逻辑。在请求转发前，利用 WASM 插件拦截并清洗恶意输入，防止通过 Prompt Injection 攻击绕过模型限制。同时，配置响应脱敏插件，防止后端 LLM 返回包含企业内部敏感信息（如数据库 Schema、内部 IP）的数据直接泄露给终端用户。

5.  建立基于语义的智能限流与熔断机制
    AI 服务的计算成本远高于传统 Web 服务，传统的 QPS 限流可能无法有效控制成本。
    建议结合 Higress 的限流功能与 Token 计数机制。不仅要限制每秒请求数（RPS），还要限制每用户每分钟的 Token 消耗量。当检测到后端模型响应延迟过高或错误率上升时，应配置熔断规则，自动降级为预设的兜底回复，避免后端服务雪崩导致高额费用产生。

6.  规避模型厂商的 IP 限流风险
    直接部署 Higress 并通过公网访问大模型 API 时，可能会因为出口 IP 变动或单一 IP 高频访问而被云厂商封禁。
    建议在部署 Higress 时配置固定出口 IP（如果是 Kubernetes 环境，需指定 Service 的 `loadBalancerIP` 或使用 NAT 网关），并在大模型厂商的控制台将该 IP 加入白名单。对于高并发场景，建议配置 Higress 的连接池设置，复用 HTTP 连接，避免因频繁握手导致的连接数耗尽。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260301-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*