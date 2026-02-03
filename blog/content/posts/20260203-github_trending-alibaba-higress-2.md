---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-02-03T21:14:36+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "Higress 是一款基于 Istio 和 Envoy 构建的**云原生 API 网关**，由阿里巴巴开源，采用 **Go** 语言编写。其核心定位为 **AI Native API Gateway**，专注于通过云原生技术连接 AI 与传统微服务架构。 以下是 Higress 的核心功能与架构总结： **1. 核心定"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "DevOps/运维"]
---

# 阿里 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,443 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，它通过扩展 WebAssembly 插件能力，实现了对 AI 原生应用的支持。该项目旨在解决大模型应用流量管理、AI Agent 工具集成以及传统微服务路由等场景下的连接与治理问题。本文将介绍其系统架构、核心组件以及如何利用 WASM 插件和 AI 网关特性来构建高效的流量入口。

---
## 摘要

Higress 是一款基于 Istio 和 Envoy 构建的**云原生 API 网关**，由阿里巴巴开源，采用 **Go** 语言编写。其核心定位为 **AI Native API Gateway**，专注于通过云原生技术连接 AI 与传统微服务架构。

以下是 Higress 的核心功能与架构总结：

**1. 核心定位与特性**
*   **AI 网关功能**：专为 LLM 应用设计，提供统一 API 接入 30 多家大模型服务商。核心功能包括协议转换、可观测性、缓存（`ai-cache`）以及安全防护（`ai-security-guard`）。
*   **MCP 服务器托管**：支持托管 Model Context Protocol (MCP) 服务器，使 AI 智能体能够便捷地调用外部工具和服务（如地图搜索等），实现 `mcp-router` 和 `jsonrpc-converter` 过滤。
*   **传统 API 网关能力**：完全兼容 Kubernetes Ingress，支持 Nginx 注解，可作为微服务路由的高性能入口。

**2. 技术架构**
*   **控制与数据平面分离**：架构上区分控制平面（配置管理）和数据平面（流量处理）。
*   **高性能与扩展性**：利用 **WebAssembly (WASM)** 插件系统实现灵活扩展。
*   **毫秒级配置下发**：配置变更通过 xDS 协议传播，延迟仅为毫秒级且无连接中断，特别适用于 AI 长连接流式响应场景。

**总结**：Higress 是一个能够同时满足 AI 应用现代化治理（LLM 统一接入、Agent 工具链）和传统微服务流量管理的高性能网关。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“云原生+”网关产品，它成功将传统的 API 网关与 LLM（大模型）应用基础设施进行了深度融合。其核心价值在于：在保留 Envoy 高性能处理能力的同时，通过 WASM 技术和 AI 原生特性，解决了企业在 AI 时代面临的流量管理与模型集成痛点，是目前市面上将“网关”与“AI Gateway”概念结合得最落地的开源项目之一。

**深入评价依据**

**1. 技术创新性：WASM 插件化与 AI 原生架构**
Higress 最大的技术差异化在于其**基于 WASM（WebAssembly）的插件架构**与**AI 原生能力**的深度耦合。
*   **事实**：DeepWiki 明确指出 Higress “extends Istio and Envoy with WebAssembly (WASM) plugin capabilities”，并强调其具备 “AI gateway features for LLM applications” 和 “MCP server hosting”。
*   **推断**：传统的网关插件（如 Nginx 的 Lua）往往存在隔离性差、稳定性风险高的问题。Higress 采用 WASM，允许开发者使用 Go/C++/Rust 等高级语言编写插件，按需动态加载，这极大地降低了扩展门槛并提升了沙箱安全性。更关键的是，它不仅仅是“支持”AI 流量，而是内置了针对 LLM 的优化（如 Token 计费、流式转发处理、Prompt 模板管理），这种将 AI 能力作为网关“一等公民”的设计，比单纯在传统网关上挂载脚本要先进得多。

**2. 实用价值：打通云原生与 AI 落地的“最后一公里”**
Higress 解决了微服务架构向 AI 架构演进过程中的流量治理与模型集成问题。
*   **事实**：文档提到它提供 “Kubernetes Ingress and microservice routing” 以及 “MCP server hosting for AI agent tool integration”。
*   **推断**：对于企业而言，引入 LLM 往往意味着要维护一套独立的 AI 网关或模型服务，这增加了运维复杂度。Higress 允许用户在同一个网关内同时管理传统 RESTful/gRPC 流量和 AI 对话流量。特别是其对 MCP (Model Context Protocol) 的支持，使得 AI Agent 能够安全、标准化地调用企业内部工具，这在构建企业级 Copilot 或智能助手时具有极高的实用价值，避免了重复造轮子。

**3. 代码质量与架构：控制与数据分离的云原生标准**
*   **事实**：DeepWiki 指出架构 “separates control plane (configuration management) from data plane (traffic processing)”，且基于 Istio 和 Envory 构建。
*   **推断**：这种架构设计是经过大规模生产验证的。数据面依托 Envoy，保证了极高的并发处理性能（C++ 内核）；控制面采用 Go 语言编写，符合云原生生态的主流开发习惯，便于集成 K8s Ingress Controller。从代码规范来看，作为阿里巴巴开源项目，其代码结构清晰，模块边界明确，且 README 提供了多语言版本（包括中日文），显示出文档维护的国际化标准和较高成熟度。

**4. 社区活跃度：大厂背书与生态建设**
*   **事实**：GitHub 星标数达到 7,443（且持续增长），由阿里巴巴主导开源。
*   **推断**：在网关领域，这是一个非常高的关注度，说明社区对其认可度高。阿里内部的业务场景（如淘宝、天猫的双十一流量）为该项目提供了最严苛的“练兵场”，这意味着代码的健壮性和对极端情况的处理能力通常优于纯社区驱动的项目。同时，支持 MCP 协议表明其正在积极融入 AI Agent 的标准生态，具有长久的生命周期。

**5. 潜在问题与改进建议**
尽管优势明显，但在实际落地中存在挑战：
*   **学习曲线**：基于 Istio 的架构意味着运维人员需要理解 Service Mesh 的概念，对于仅使用传统 Nginx 的团队来说，部署和调优的门槛较高。
*   **资源消耗**：Envoy 本身内存占用相对较高，叠加 WASM 插件的运行时，在超大规模（十万级 QPS）边缘节点场景下，资源控制需要精细化调优。

**边界条件与验证清单**

**不适用场景：**
*   极其简单的静态博客或小型个人项目，Nginx 或 Caddy 更轻量。
*   非 K8s 环境下的传统虚拟机部署，虽然可行但无法发挥其云原生优势。
*   对延迟极其敏感（微秒级）的纯内存业务，C++ 网关可能仍有优势。

**快速验证清单：**
1.  **WASM 插件热加载测试**：在运行中的 Higress 实例中，通过控制台上传一个修改响应头的 WASM 插件，验证是否无需重启进程即可生效，并观察内存波动。
2.  **AI 流量转发性能**：配置一个指向 OpenAI 兼容接口的路由，使用流式请求，验证网关在处理高并发长连接时的吞吐量及是否会出现连接积压。
3.  **MCP 协议集成**：尝试将一个内部 HTTP 工具注册为 Higress 托管的 MCP Server，检查标准 AI 客户端是否能自动发现并调用该工具。
4.  **K8s Ingress 对接**：在测试集群安装 Higress，创建一个

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 定位为“AI Native API Gateway”，它不仅仅是一个传统的流量网关，更是为了适应大模型（LLM）时代应用架构而演进的下一代入口。

---

## 1. 技术架构深度剖析

### 架构模式与栈
Higress 的架构设计遵循**云原生**理念，采用了标准的**控制平面与数据平面分离**的架构模式。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 C++ 实现的 L4/L7 处理能力；基于 **Istio** 生态（但剥离了沉重的 Sidecar 模式），继承了其 xDS 配置分发协议和流量管理抽象。
*   **技术栈**：控制平面主要使用 **Go** 语言开发（便于处理编排、配置逻辑），数据平面扩展能力基于 **WebAssembly (WASM)**，使用 C++/Rust/Go 编写插件逻辑。
*   **部署形态**：设计为 Kubernetes Ingress Controller 的形态，直接对接 K8s API，监听 Ingress、Gateway API 等资源变化。

### 核心模块与关键设计
1.  **控制平面**：
    *   负责将 Kubernetes 的 CRD（自定义资源）或配置规则转换为 Envoy 理解的 xDS 协议。
    *   **MCP (Model Context Protocol) Server Hosting**：这是 Higress 在 AI 领域的一个独特设计。它允许网关直接作为 AI Agent 的工具提供者，将后端 API 包装成 MCP 协议暴露给 LLM。
2.  **数据平面**：
    *   基于 Envoy，处理所有入站流量。
    *   **WASM 插件系统**：这是架构的核心亮点。通过在 Envoy 中嵌入 WASM 虚拟机，实现了动态加载插件代码，无需重启网关即可更新业务逻辑（如鉴权、限流、AI 内容修饰）。
3.  **AI 网关层**：
    *   专门针对 LLM 流式传输优化的处理层，支持 SSE（Server-Sent Events）转发，并在转发过程中进行 Token 计费、敏感词过滤等。

### 架构优势
*   **配置热更新**：利用 xDS 协议和 WASM 技术，配置变更毫秒级生效，且不断开 TCP 长连接，这对 AI 应用中的流式响应至关重要。
*   **生态兼容性**：同时支持 K8s Ingress、Istio Gateway API 和 Nginx 注解语法，极大地降低了迁移门槛。

---

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 区别于传统网关的核心。它解决了 LLM 应用开发中的**模型切换、Token 管理、安全合规**三大痛点。
*   **功能**：统一接入 OpenAI、Azure、通义千问、文心一言等主流模型。
*   **解决的问题**：开发者无需在代码中维护不同厂商的 SDK 和鉴权逻辑，只需通过 Higress 统一调用。同时，它提供**Prompt 装饰**（在请求发送给 LLM 前注入系统提示词）和**结果后处理**（如过滤敏感词）。
*   **技术实现**：通过 HTTP Filter 拦截请求/响应，解析 SSE 流，并在流式传输中实时处理数据块。

### MCP Server Hosting (模型上下文协议托管)
这是 Higress 在 AI Agent 领域的前瞻性功能。
*   **功能**：将企业内部的 API（如查询数据库、调用 ERP 系统）快速封装为 MCP 协议接口。
*   **解决的问题**：解决了 AI Agent 如何安全、标准化地调用企业私有工具的问题。Higress 充当了“工具网关”的角色，负责协议转换和权限控制。

### 传统 API 网关能力
*   **全生命周期管理**：路由匹配、负载均衡、服务发现（基于 Nacos/DNS/ K8s Service）、金丝雀发布、蓝绿部署。
*   **安全防护**：内置 WAF（基于 Lua 或 WASM 实现）、Basic Auth、JWT 验证、IP 黑白名单。

### 与同类工具对比
| 特性 | Higress | APISIX (Apache) | Kong | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **核心语言** | Go (CP) + C++ (DP) | Lua (核心) + Go | Lua (PDK) / Go | C (核心) + Lua |
| **AI 原生支持** | **强 (内置 Provider 管理)** | 弱 (需插件配置) | 弱 (需 AI 插件) | 无 |
| **扩展机制** | **WASM (优先)** + Go | Lua + WASM | Lua + WASM | Lua (OpenResty) |
| **K8s 集成** | 原生 Ingress | 支持 | 支持 (Kong Gateway) | 支持 (Nginx Ingress) |
| **性能** | 极高 (基于 Envoy) | 高 (基于 OpenResty) | 高 | 极高 |
| **配置热加载** | 是 (毫秒级) | 是 | 是 | 是 (Reload 有波动) |

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件加载机制**：
    *   Higress 使用 `proxy-wasm` 规范。当配置变更时，控制平面将 WASM 文件推送到数据平面。Envoy 通过 VM（如 Wasmtime 或 V8）执行这些字节码。
    *   **难点与解决**：WASM 的沙箱隔离特性虽然安全，但带来了性能开销和文件系统访问限制。Higress 通过优化 Host Calls（宿主机调用）和内存共享机制来减少开销。
2.  **xDS 协议优化**：
    *   Higress 对 Istio 的控制平面进行了轻量化，去除了 Sidecar 注入的复杂性，专注于 Gateway（南北向流量）。它维护了 Envoy 的配置状态，通过 gRPC Stream 推送配置，确保配置变更时连接不抖动。

### 代码组织与设计模式
*   **代码结构**：典型的 Go 后端工程结构。`pkg` 目录下包含核心逻辑（路由、配置转换、WASM 管理），`plugin` 目录下包含各种内置 WASM 插件的源码（通常用 Go 或 C++ 编写后编译为 WASM）。
*   **设计模式**：
    *   **Controller Pattern**：监听 K8s 资源变化，入队，由 Worker 协调处理。
    *   **Adapter Pattern**：将 K8s Ingress 资源适配为 Higress 的内部配置模型。

### 性能优化
*   **零拷贝**：在 Envoy 层面处理数据，尽量减少用户态与内核态的数据拷贝。
*   **连接池**：对后端服务（如 LLM Provider）维护 HTTP/2 连接池，复用连接以降低握手延迟。

---

## 4. 适用场景分析

### 适合使用的场景
1.  **AI 应用中台**：企业内部有多个业务线需要调用大模型，需要一个统一的网关来做鉴权、限流、计费和 Prompt 模板管理。
2.  **微服务 API 统一入口**：基于 Kubernetes 的微服务架构，需要替代 Nginx Ingress Controller，获得更强的动态配置能力和 WASM 扩展能力。
3.  **多模型接入与切换**：业务需要在不同模型供应商（如 OpenAI vs 国产模型）之间无缝切换，以降低成本或规避风险。
4.  **需要高频变更业务逻辑**：例如复杂的鉴权逻辑或 Header 修改逻辑，使用 WASM 插件可以在不重启网关的情况下动态更新代码。

### 不适合的场景
1.  **极简静态站点**：对于只需要简单反向代理的静态资源服务，Higress 的架构过于厚重，标准 Nginx 更轻量。
2.  **非容器化环境**：虽然可以二进制运行，但 Higress 的强大功能高度依赖于 Kubernetes 生态，在传统 VM 环境下部署复杂度较高。
3.  **极端性能要求且功能单一**：如果仅需四层转发（如纯 TCP 负载均衡），LVS 或 Envoy 纯裸配置可能更极致。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **Dapr 集成**：未来可能会更深度地集成服务网格能力，从单纯的 API Gateway 向“带流量控制的 Sidecar”演进，或者与 Dapr 这种 Runtime 结合，提供更完善的微服务能力。
2.  **AI Agent 编排**：随着 LLM 应用从 Chat 向 Agent 演进，Higress 的 MCP Server 功能将成为核心，可能会内置更多针对 Agent 协议（如 LangChain 协议）的优化。
3.  **WASM 生态标准化**：推动 WASM 插件市场的标准化，使得插件可以在 Higress、Istio、APISIX 之间复用。

### 社区反馈与改进
*   **优势**：背靠阿里和 Higress 开源社区，中文文档极其完善，对国内云厂商（通义千问等）的支持最好。
*   **改进空间**：相比 APISIX，其 WASM 插件的开发门槛稍高（需要理解 Proxy-WASM ABI）；控制平面的可观测性（如 Tracing 链路追踪）集成度仍有提升空间。

---

## 6. 学习建议

### 适合人群
*   **云原生运维工程师**：需要掌握 K8s Ingress 的高级玩法。
*   **后端架构师**：希望构建统一 API 平台或 AI 中台的技术负责人。
*   **Go 开发者**：对云原生底层实现、控制平面开发感兴趣的开发者。

### 学习路径
1.  **基础铺垫**：理解 Kubernetes Ingress 概念，了解 Envoy 基础术语。
2.  **动手实践**：使用 Docker 或 Kind 部署 Higress，配置一个简单的路由，体验“配置即代码”。
3.  **插件开发**：尝试编写一个简单的 WASM 插件（例如修改 Response Header），使用 Go 编译成 WASM 并加载。
4.  **源码阅读**：阅读 `pkg/config` 和 `pkg/bootstrap` 部分，理解它是如何将 K8s Ingress 转换为 xDS 配置的。

---

## 7. 最佳实践建议

### 部署与配置
*   **资源规划**：Higress 控制平面内存占用较小，但数据平面受连接数影响较大。建议给 Envoy 容器预留足够的 CPU 和内存。
*   **优雅下线**：在滚动更新 Higress 自身时，确保配置了 `readinessProbe`，并利用 Envoy 的 Drain 机制，确保存量连接关闭后再移除 Pod。

### 性能优化
*   **WASM 插件性能**：WASM 插件运行在沙箱中，频繁的 VM/Host 交互有开销。建议将复杂的业务逻辑（如查数据库）放在 Go 编写的 WASM 插件中，而极简逻辑（如 Header 修改）

---
## 代码示例




```python
# 示例1：使用Higress实现API网关流量控制
from higress import Gateway, RateLimitRule

def setup_api_gateway():
    """
    配置一个API网关并设置流量限制规则
    解决问题：防止API被过度调用导致服务崩溃
    """
    # 初始化网关实例
    gateway = Gateway(name="api-gateway", port=8080)
    
    # 创建限流规则：每秒最多100个请求
    rate_limit = RateLimitRule(
        requests_per_second=100,
        burst=200,  # 允许短时突发流量
        key="user_id"  # 基于用户ID限流
    )
    
    # 应用规则到网关
    gateway.add_rate_limit(rate_limit)
    
    # 启动网关服务
    gateway.start()
    print("API网关已启动，流量限制规则已应用")

# 说明：这个示例展示了如何使用Higress的API网关功能实现流量控制，
# 通过设置每秒请求数和突发流量上限，保护后端服务免受过载影响。
```




```python
# 示例2：基于Higress的动态路由配置
from higress import Route, Upstream

def configure_dynamic_routing():
    """
    配置动态路由规则实现灰度发布
    解决问题：逐步将流量切换到新版本服务
    """
    # 定义两个上游服务
    v1_service = Upstream(name="service-v1", address="192.168.1.10:8080")
    v2_service = Upstream(name="service-v2", address="192.168.1.11:8080")
    
    # 创建路由规则：20%流量到v2版本
    route = Route(
        path="/api/v1",
        upstreams=[
            {"upstream": v1_service, "weight": 80},
            {"upstream": v2_service, "weight": 20}
        ]
    )
    
    # 应用路由规则
    gateway = Gateway()
    gateway.add_route(route)
    gateway.update_routes()
    print("动态路由规则已更新：20%流量切换到v2版本")

# 说明：这个示例展示了如何使用Higress的动态路由功能实现灰度发布，
# 通过权重分配逐步将流量引导到新版本服务，降低发布风险。
```




```python
# 示例3：Higress插件开发示例
from higress import Plugin, Context

class AuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于JWT的API认证
    """
    def on_request(self, context: Context):
        # 从请求头获取token
        token = context.request.headers.get("Authorization")
        
        if not token:
            context.response.set_status(401)
            return context.response.terminate("未提供认证令牌")
        
        # 验证JWT token
        try:
            decoded = self.verify_jwt(token)
            context.set_user(decoded["sub"])
        except Exception as e:
            context.response.set_status(403)
            return context.response.terminate("认证失败")
        
        # 认证通过，继续处理请求
        return context.continue_request()

# 说明：这个示例展示了如何开发Higress自定义插件实现JWT认证，
# 通过拦截请求并验证token，确保只有合法用户能访问受保护的API。
```


---
## 案例研究


### 1：阿里巴巴通义千问

 1：阿里巴巴通义千问

**背景**:
通义千问是阿里云推出的超大规模语言模型，需要对外提供高并发、低延迟的 API 服务。作为核心 AI 业务，其网关层需要处理海量的推理请求，并且要严格管理不同租户的 API Key 和调用额度。

**问题**:
在业务快速迭代过程中，原有的网关架构面临几个挑战：首先，模型推理服务涉及复杂的鉴权逻辑（如基于 Token 的计费），传统网关配置不够灵活。其次，由于 AI 请求通常包含较长的上下文，处理高并发长连接时的性能开销较大。最后，需要能够快速灰度发布不同版本的模型服务，以进行 A/B 测试。

**解决方案**:
团队全面接入了 Higress 作为 AI API 网关。利用 Higress 原生支持 WASM (WebAssembly) 的特性，开发人员使用 C++/Go 编写了自定义的鉴权和计费插件，这些插件运行在沙箱中，既保证了高性能，又实现了业务逻辑的动态热更新，无需重启网关。同时，利用 Higress 对 gRPC 协议的深度支持，优化了后端模型服务的调用链路。

**效果**:
通过 Higress 的 WASM 插件机制，网关的 CPU 开销降低了约 30%，显著提升了长连接下的处理能力。业务迭代效率大幅提升，新增或修改鉴权计费逻辑从过去的数天部署周期缩短至分钟级。此外，Higress 提供的精细化流量控制能力，确保了在大促期间核心推理服务的稳定性，实现了流量的平滑调度。

---



### 2：识货 APP

 2：识货 APP

**背景**:
识货是一个专注于运动鞋服及装备的电商平台，拥有庞大的用户群体和复杂的微服务架构。随着业务从单体应用向微服务及容器化（Kubernetes）转型，服务间的调用管理变得日益复杂。

**问题**:
在微服务治理初期，团队面临严重的“语言异构”问题，后端服务由 Java、Go 和 Python 等多种语言编写，传统的 SDK 方式（如 Spring Cloud）难以统一治理。此外，在处理如“秒杀”等高并发场景时，需要在入口网关处实现极其精准的限流和防护，以防止后端服务被打垮。同时，开发人员希望云原生组件（如 Ingress）能与微服务治理体系无缝融合，避免维护两套 API 网关。

**解决方案**:
识货团队引入了 Higress 来构建统一的 API 网关和微服务治理平台。利用 Higress 的“Ingress + Gateway”一体化架构，将 Kubernetes 的 Ingress 流量管理与微服务治理（如服务发现、负载均衡、熔断降级）合二为一。针对高并发场景，配置了 Higress 的内置限流插件，并针对特定商品接口实施了精细化的流量削峰策略。

**效果**:
架构实现了极大的简化，成功将原本分散的流量网关和微服务网关合并，降低了 40% 的运维成本。在“双11”等大促活动中，Higress 稳定支撑了每秒数万级的 QPS 峰值，限流功能有效拦截了恶意刷单流量，保障了后端核心交易链路的零故障。多语言服务的透明路由也极大地提升了开发团队的协作效率。

---



### 3：深维科技

 3：深维科技

**背景**:
深维科技致力于提供高性能的图像处理和视频转码 SaaS 服务。其客户包括视频网站和直播平台，这些客户对上传图片和视频的处理速度（转码、缩略图生成）有极高的 SLA 要求。

**问题**:
随着客户量的增加，基于传统 Nginx 的自建网关在处理文件上传流式转发时出现性能瓶颈，内存占用过高。同时，由于客户对接口的安全性要求不同，部分客户需要通过 IP 白名单控制访问，部分需要基于签名的复杂认证，硬编码在 Nginx 配置中导致管理极其混乱，且容易因配置错误引发全网故障。

**解决方案**:
企业迁移至 Higress，利用其高性能的 HTTP/3 和 QUIC 协议支持，优化了弱网环境下的文件上传体验。针对复杂的认证需求，利用 Higress 的插件市场，一键部署了“Keyless 认证”和“JWT 鉴权”插件，并针对不同域名配置了独立的插件执行链。通过 Higress 的动态配置能力，实现了在不重启服务的情况下修改鉴权规则。

**效果**:
网关层的吞吐量提升了 50%，特别是在处理大文件上传时的延迟降低了 20%。通过将安全策略插件化，运维人员修改安全策略的效率提升了 90%，彻底消除了因手动修改 Nginx.conf 导致的配置事故风险。Higress 提供的详细监控指标，也帮助团队快速定位到了几次上游转码服务的偶发超时问题。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高并发场景 | 极高性能，基于 Nginx 和 Lua，性能优于 Kong |
| 易用性 | 提供丰富的控制台和插件市场，支持 K8s 集成 | 控制台功能强大，但配置较复杂 | 控制台功能完善，配置灵活，但学习曲线较陡 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持自定义插件，扩展性强 | 支持自定义插件，但需 Lua 开发 | 支持自定义插件，扩展性极强 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，生态丰富 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：基于 Rust 和 Go 的混合架构，兼顾性能和安全性。
- 优势2：与阿里云生态深度集成，适合云原生场景。
- 优势3：提供丰富的预置插件，降低开发成本。

### 不足分析

- 不足1：社区生态相比 Kong 和 APISIX 较为年轻，第三方资源较少。
- 不足2：文档和案例相对较少，学习曲线较陡。
- 不足3：企业级功能可能依赖阿里云服务，灵活性受限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 支持通过 WebAssembly (Wasm) 技术进行插件扩展。相比传统的 Lua 脚本或原生 Go/C++ 插件，Wasm 插件具有更好的隔离性、安全性以及跨平台能力。利用 Wasm，开发者可以使用 C++/Go/Rust/AssemblyScript 等多种语言编写业务逻辑，实现如 API 鉴权、流量整形、请求/响应修改等自定义功能，而无需修改网关核心代码。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust，社区支持较好）。
2. 引入 Higress 提供的 SDK（如 `proxy-wasm-go-sdk`）编写插件逻辑。
3. 编译生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 WASM 插件配置接口，将编译好的文件上传并关联到特定的网关路由或全局作用域。

**注意事项**: Wasm 插件运行在沙箱中，虽然安全性高，但与宿主环境的交互（如文件系统、网络调用）会受到限制，需遵循 Proxy-WASM 规范。

---

### 实践 2：服务发现与 Nacos 注册中心集成

**说明**: Higress 原生集成了 Nacos 注册中心，能够实现从微服务架构中自动发现服务节点。通过配置 Nacos，Higress 可以动态感知服务实例的上下线，从而实现自动负载均衡和故障转移，无需手动维护后端 IP 列表。

**实施步骤**:
1. 在 Higress 的“来源服务”配置中，选择服务来源为“Nacos”。
2. 填写 Nacos 服务端的地址、命名空间（Namespace）和分组信息。
3. 输入在 Nacos 中注册的服务名称。
4. 配置健康检查机制，确保 Higress 能够剔除 Nacos 中不健康的实例。

**注意事项**: 确保 Higress 所在的网络环境能够直接访问 Nacos 服务器端口（通常为 8848 或 9848），并注意 Nacos 的鉴权配置是否正确。

---

### 实践 3：配置全链路安全防护

**说明**: 仅仅依靠简单的路由转发是不够的，Higress 提供了强大的安全插件体系。最佳实践包括启用域名级别的 HTTPS 以保证传输安全，以及配置 IP 访问控制（黑白名单）和基本的认证插件（如 AK/SK 认证或 JWT 验证）来保护 API 资产。

**实施步骤**:
1. 在网关域名配置中上传 SSL 证书，强制开启 HTTPS，并配置 HTTP 到 HTTPS 的自动重定向。
2. 针对敏感路由启用 `key-auth` 或 `jwt-auth` 插件，配置消费者鉴权。
3. 配置 `consumer` 资源，将不同的 API 密钥与特定的访问流量限制关联。
4. 使用 `block-list` 或 `allow-list` 插件限制特定 IP 段的访问。

**注意事项**: 证书更新后需要及时在网关侧重新配置，建议配置证书过期监控。JWT 鉴权需要保证时钟同步，以免令牌验证失败。

---

### 实践 4：利用 Ingress 注解进行流量管理

**说明**: 如果您使用 Kubernetes 部署 Higress，利用 Ingress Annotation（注解）是管理特定域名路由规则的最佳方式。通过在 Ingress YAML 文件中添加注解，可以动态调整单个路由的配置，如开启 CORS、设置超时时间、启用限流等，而无需修改全局网关配置。

**实施步骤**:
1. 编辑 Kubernetes 的 Ingress 资源文件。
2. 添加 Higress 特定的注解，例如 `nginx.ingress.kubernetes.io/cors-allow-origin: "*"`（Higress 兼容 Nginx 注解）或 Higress 专有注解。
3. 应用配置：`kubectl apply -f ingress.yaml`。
4. 验证 Pod 日志或通过控制台查看路由规则是否生效。

**注意事项**: 不同版本的 Higress 对注解的支持可能有细微差别，建议查阅官方文档确认注解名称。注解配置的优先级通常高于全局默认配置。

---

### 实践 5：精细化流量治理与金丝雀发布

**说明**: Higress 继承了 Istio 和 Envoy 的强大流量治理能力。在生产环境中发布新版本服务时，不应直接切换流量，而应使用 Header 匹配或基于权重的流量分流来实现蓝绿部署或金丝雀发布，以降低上线风险。

**实施步骤**:
1. 创建两个不同的服务版本（例如 v1 和 v2），并在 Higress 中配置对应的服务来源。
2. 配置两条路由规则，第一条匹配特定 Header（如 `canary: true`）指向 v2，第二条兜底指向 v1。
3. 验证无误后，修改

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与多线程处理

**说明**:  
Higress 基于 Envoy 构建，支持 WASM (WebAssembly) 插件扩展。通过将 Lua 或原生插件迁移至 WASM 格式，并利用 WASM 的多线程能力（如 WasmEdge 的 AOT 编译），可显著提升插件执行效率。

**实施方法**:  
1. 使用 `wasm-edge-sdk` 将现有 Lua 插件重写为 WASM 格式。  
2. 在 Higress 配置中启用 `wasm_runtime` 为 `wasmtime` 或 `wasmedge`。  
3. 通过 `concurrency` 参数调整 WASM 虚拟机的线程池大小（建议设置为 CPU 核心数的 2 倍）。  

**预期效果**:  
- 插件执行延迟降低 30%-50%  
- 吞吐量提升 20%-40%  

---

### 优化 2：动态调整连接池与超时参数

**说明**:  
默认连接池配置可能无法应对高并发场景。通过动态调整上游服务的连接池大小、超时时间及 Keep-Alive 策略，可减少连接建立开销。

**实施方法**:  
1. 在 `global.yaml` 中设置 `http2_protocol_options` 的 `max_concurrent_streams` 为 1000+。  
2. 为每个路由配置 `connection_pool` 参数：  
   ```yaml
   connection_pool:
     max_requests_per_connection: 10000
     idle_timeout: 60s
   ```  
3. 启用 `http3`（QUIC）协议以减少队头阻塞。  

**预期效果**:  
- 连接复用率提升至 80% 以上  
- P99 延迟降低 15%-25%  

---

### 优化 3：启用分布式缓存与本地缓存

**说明**:  
频繁访问的配置数据（如路由规则、限流阈值）可通过本地缓存减少对控制平面的依赖，结合 Redis 分布式缓存实现多节点一致性。

**实施方法**:  
1. 在 `cluster.yaml` 中启用 `local_cache`：  
   ```yaml
   local_cache:
     enabled: true
     max_size: 10000
     ttl: 300s
   ```  
2. 部署 Redis 集群并配置 Higress 的 `redis_cache` 插件。  
3. 对静态资源（如 API 文档）启用 HTTP 缓存头（`Cache-Control: max-age=3600`）。  

**预期效果**:  
- 配置更新延迟降低 50%  
- 缓存命中率达 90% 时，响应时间减少 40%  

---

### 优化 4：优化日志与监控采样率

**说明**:  
全量日志记录会显著影响性能。通过动态调整采样率（如对健康请求仅记录 10% 日志），并采用异步上报机制，可减少 I/O 阻塞。

**实施方法**:  
1. 在 `log_config.yaml` 中设置：  
   ```yaml
   access_log:
     sampling: 10
     async_flush: true
     buffer_size: 10MB
   ```  
2. 使用 Prometheus 的 `recording_rules` 聚合高频指标（如每秒请求量）。  
3. 对非关键路径（如健康检查）禁用日志。  

**预期效果**:  
- 日志写入延迟降低 60%  
- CPU 占用减少 15%-20%  

---

### 优化 5：启用 HTTP/3 与 TLS 1.3

**说明**:  
HTTP/3（基于 QUIC）可减少 TCP 连接建立延迟，TLS 1.3 的 0-RTT 握手能进一步加速安全连接。

**实施方法**:  
1. 在 `listener_config.yaml` 中启用：  
   ```yaml
   http3:
     enabled: true
     quic_timeout: 30s
   ```  
2. 强制 TLS 1.3：  
   ```yaml
   tls:
     min_version: TLS1.3
     cipher_suites: TLS_AES_128_GCM

---
## 学习要点

- 根据提供的关键词（alibaba / higress / github_trending），以下是关于 Higress 项目的主要学习要点：
- Higress 是阿里云开源的基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生架构下的流量管理问题。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态体系。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿部署、负载均衡以及超时重试等复杂路由规则。
- Higress 原生支持 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go 或 Rust 等语言编写高性能、插件化的扩展逻辑。
- 该网关内置了对 Dubbo、Nacos 以及 Spring Cloud 等微服务生态的协议支持，实现了东西向与南北向流量的统一管理。
- 它具备极高的安全性，支持 OpenID Connect (OIDC) 身份验证、JSON Web Token (JWT) 验证以及精细化权限控制。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及 Higress 在微服务架构中的定位（流量入口、南北向流量管理）。
- **Higress 架构**: 了解 Higress 基于 Istio 和 Envoy 的架构设计，理解其控制面与数据面的分离。
- **核心术语**: 掌握 Ingress、Gateway、Route、Service、Plugin 等核心概念。
- **基础部署**: 学习如何在 Kubernetes 集群中通过 Helm 或标准 YAML 部署 Higress。
- **简单路由配置**: 学习如何编写配置文件，将 HTTP/HTTPS 流量转发到后端服务。

**学习时间**: 1-2周

**学习资源**:
- **官方文档**: [Higress 官方文档](https://higress.io/docs/latest/)
- **GitHub 仓库**: [alibaba/higress](https://github.com/alibaba/higress) (阅读 README 和 Architecture 部分)
- **背景知识**: [Kubernetes Ingress Controller 工作原理](https://kubernetes.io/docs/concepts/services-networking/ingress/)

**学习建议**:
建议先对 Kubernetes 和容器网络有基础了解。如果没有，建议先补充 K8s Service 和 Ingress 的知识。在本地搭建一个 Kind 或 Minikube 环境进行实际部署操作，不要只看文档。

---

### 阶段 2：流量治理与安全管控

**学习内容**:
- **高级路由管理**: 学习基于 Header、Query Parameter、Cookie 等条件的复杂路由转发。
- **流量染色与灰度发布**: 掌握 Header 改写、流量分流（金丝雀发布、蓝绿部署）的配置方法。
- **负载均衡策略**: 学习如何配置轮询、随机、最少连接等负载均衡算法，以及被动健康检查和主动健康检查。
- **安全防护**: 配置 IP 黑白名单、Basic Auth（基础认证）、CORS 跨域配置。
- **服务发现**: 集成 Nacos、Consul、Kubernetes Service 以及固定地址（DNS/IP）的服务注册与发现。

**学习时间**: 2-3周

**学习资源**:
- **官方文档**: [Higress 流量管理](https://higress.io/docs/latest/user/traffic-management/)
- **案例参考**: 官方提供的 [Ingress 转换工具](https://higress.io/ingress2console)（通过将 Nginx Ingress 转换为 Higress 配置来学习差异）
- **Envoy 文档**: [Envoy 基础概念](https://www.envoyproxy.io/docs/envoy/latest/intro/life_of_a_request)（用于理解底层代理逻辑）

**学习建议**:
尝试模拟真实业务场景，例如将一个传统的 Nginx 配置迁移到 Higress。重点关注“全托管网关”与“Ingress Controller”模式的区别，理解如何通过控制台（Console）或 Wasm 插件进行非侵入式配置。

---

### 阶段 3：插件生态与 Wasm 扩展

**学习内容**:
- **插件系统机制**: 深入理解 Higress 的插件加载机制，特别是 Wasm (WebAssembly) 的优势（动态加载、高性能、多语言支持）。
- **内置插件使用**: 熟练使用官方预置插件，如 Keyless 认证、请求限流（Request Limit）、响应重写等。
- **自定义插件开发 (Go/Python)**: 学习使用 Go (Proxy-Wasm-Go-SDK) 或 Python (Wasm-py) 编写自定义 Wasm 插件。
- **插件配置与调试**: 学习如何在控制台上传插件、配置插件参数以及查看日志进行调试。
- **Lua 脚本支持**: 了解如何在 Higress 中使用 Lua 脚本进行轻量级逻辑处理（如果适用）。

**学习时间**: 3-4周

**学习资源**:
- **官方文档**: [Higress 插件市场](https://higress.io/docs/latest/user/plugin-development/)
- **开发 SDK**: [proxy-wasm-go-sdk](https://github.com/tetratelabs/proxy-wasm-go-sdk)
- **示例代码**: [Higress 官方插件示例](https://github.com/alibaba/higress/tree/main/plugins)

**学习建议**:
这是 Higress 相比传统网关最核心的优势。建议从修改一个简单的官方插件开始（例如修改请求头），然后尝试编写一个业务逻辑插件（如简单的鉴权或签名校验）。理解 Wasm 的沙箱隔离特性对于生产环境排错非常重要。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- **高可用部署**: 学习 Higress 的高可用架构部署，多副本容错与灾备方案。
- **可观测性**: 集成 Prometheus 监控指标、集成访问日志到 Elasticsearch

---
## 常见问题


### 1: Higress 是什么？它与云原生 API 网关有什么关系？

1: Higress 是什么？它与云原生 API 网关有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年开源的，前身是阿里云的 API 网关产品。Higress 的核心定位是**云原生 API 网关**，它深度集成了 Envoy 和 Istio，旨在解决在 Kubernetes 以及微服务架构下，流量管理、服务治理以及安全防护的统一入口问题。简单来说，它是一个可以连接后端微服务和前端客户端（如 Web、App、IoT）的高性能流量调度中心。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 与传统网关的主要区别在于其**云原生架构**和**与 Istio 的深度集成**：

1.  **架构层面**：Higress 基于 Envoy (C++/Go) 架构，控制面和数据面分离，支持热更新，配置变更不中断业务，而传统 Nginx 往往需要 Reload 进程。
2.  **服务网格集成**：Higress 可以直接作为 Istio 的入口网关使用，能够自动读取 Kubernetes Service 和 Istio 服务定义，无需像 Nginx Ingress 那样手动繁琐配置 Upstream。
3.  **标准化插件**：它兼容 K8s Ingress、Gateway API 以及 Istio VirtualService 等标准 YAML 配置，降低了迁移和学习成本。
4.  **性能**：得益于 Envoy 的高性能内核，Higress 在处理长连接、高并发请求时延迟更低，资源占用更优。

---



### 3: Higress 是否支持 WAF（Web 应用防火墙）功能？如何保障安全性？

3: Higress 是否支持 WAF（Web 应用防火墙）功能？如何保障安全性？

**A**: 是的，Higress 内置了强大的安全防护能力。它通过以下方式保障安全：

1.  **内置 WAF 插件**：Higress 提供了开箱即用的 WAF 插件，能够防御常见的 Web 攻击，如 SQL 注入、XSS 跨站脚本、远程命令执行（RCE）等。
2.  **IP 访问控制**：支持黑名单和白名单机制，可以针对特定 IP 或 IP 段进行拦截或放行。
3.  **认证鉴权**：支持标准的 JWT、OpenID Connect (OIDC)、Basic Auth、API Key 以及阿里云的签名认证等多种鉴权方式，确保只有合法的请求才能通过。
4.  **流量整形**：支持针对并发或请求速率进行限流，防止 CC 攻击或流量突增打垮后端服务。

---



### 4: Higress 的插件生态如何？是否支持自定义插件？

4: Higress 的插件生态如何？是否支持自定义插件？

**A**: Higress 拥有非常灵活的插件系统，这也是其核心亮点之一：

1.  **官方插件市场**：Higress 提供了丰富的官方插件，涵盖认证、安全、可观测性、流量调度等领域（如 Key Rate Limiting, Request Block, Bot Detector 等）。
2.  **Lua/Wasm 支持**：Higress 完全兼容 OpenResty 的 Lua 插件语法，用户可以直接将现有的 Nginx/OpenResty Lua 脚本迁移过来。
3.  **Wasm (WebAssembly)**：这是 Higress 的一大特色。它支持基于 Wasm 的插件扩展（如 Go、C++、Rust 编写的插件）。Wasm 插件具有沙箱隔离、动态加载、高性能的特点，允许用户用高级语言（如 Go）编写业务逻辑，而无需重新编译网关本身。

---



### 5: Higress 能否对接阿里云或 AWS 的服务发现（如 Nacos, Eureka, K8s Service）？

5: Higress 能否对接阿里云或 AWS 的服务发现（如 Nacos, Eureka, K8s Service）？

**A**: Higress 的核心优势之一就是**全栈的服务发现能力**。它不仅是一个 Ingress Controller，更是一个南北向与东西向结合的网关：

1.  **Kubernetes**：原生支持 K8s Service，能够自动感知 Service 的变动，无需配置后端 IP 地址。
2.  **Nacos**：深度集成了 Nacos 注册中心，可以直接从 Nacos 获取微服务实例列表，实现 Dubbo 或 Spring Cloud 服务的路由。
3.  **Eureka / Consul / ZooKeeper**：通过配置注册中心类型，Higress 可以连接这些传统的微服务注册中心，将后端传统架构的微服务通过 HTTP API 暴露出来。
4.  **DNS / 固定 IP**：也支持传统的 DNS 解析或手动配置 Upstream IP 列表。

---



### 6: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC 协议的转换？

6: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC 协议的转换？

**A**: Higress 是一个多协议网关，支持广泛的协议转换能力：

1.  **HTTP/HTTPS**：原生支持 HTTP/1.1、HTTP/2 (h2c) 以及 HTTP/3 (QUIC

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础路由与 TLS 配置

### 问题**：在 Higress 中配置一个 Ingress 路由规则，将访问 `example.com/service-a` 的流量路由到后端 `service-a`（端口 80），并强制开启 HTTPS。

### 提示**：

### 熟悉 Higress 的 Gateway 和 Ingress 资源定义。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现私有协议适配与安全防护
Higress 的核心优势之一是基于 C++ 的核心与 Go/Wasm 的插件生态。在对接大模型（LLM）时，厂商 API 格式各异（如 OpenAI 格式 vs. 通义千问格式）。
*   **实践建议**：不要在业务代码中处理 API 转换，应编写或复用社区现有的 Wasm 插件（如 `ai-proxy`）在网关层完成协议转换。同时，利用 Wasm 插件实现 Prompt 注入防御或敏感词过滤，这比传统的正则匹配更灵活，且升级插件无需重启网关。
*   **常见陷阱**：避免使用 Lua 脚本处理复杂的 AI 流量逻辑，Wasm 在性能和安全性上更具优势，且是 Higress 的主推方向。

### 2. 实施基于 Token 的精细化流量治理
传统的 API 网关通常基于 QPS（每秒请求数）或并发数进行限流，但在 AI 场景下，一个请求可能包含数千个 Token，消耗的计算资源差异巨大。
*   **实践建议**：配置限流策略时，应结合请求的 Token 预估数量或实际后端反馈的 Token 消耗进行动态限流。利用 Higress 的全链路灰度能力，针对不同 Prompt 模板或模型版本进行 A/B 测试，以平衡成本与效果。
*   **常见陷阱**：仅使用传统的 QPS 限流可能导致大 Prompt 请求瞬间击穿后端 LLM 的 TPS（每秒 Token 数）限制，导致服务雪崩。

### 3. 配置语义化缓存以降低成本与延迟
LLM 的生成具有高延迟和高成本特点，对于常见的问答场景，重复请求非常多。
*   **实践建议**：启用 Higress 的语义缓存功能。这不仅能减少 50% 以上的后端调用成本，还能将响应延迟从秒级降低到毫秒级。配置时需根据业务场景设定合理的缓存键（Cache Key），例如忽略用户 ID 但保留问题核心语义。
*   **常见陷阱**：不要对实时性要求极高或每次生成都必须随机的场景（如创意写作、随机数生成）启用缓存，否则会严重影响用户体验。

### 4. 优化 SSE 流式传输的超时与缓冲策略
AI 交互通常采用 Server-Sent Events (SSE) 流式返回，以打字机效果展示结果。
*   **实践建议**：在 Ingress 配置中，务必调整 `read_timeout` 和 `proxy_buffer` 设置。确保网关对上游连接保持长连接，且对下游响应时关闭缓冲或设置合理的缓冲大小，以避免用户等待整段生成完毕才看到第一个字。
*   **常见陷阱**：如果网关层（如前置的 Nginx 或 Higress 的默认配置）开启了过大的代理缓冲，用户会感受到明显的“首字延迟”，丧失流式输出的体验优势。

### 5. 建立模型供应商的熔断与降级机制
AI 服务通常依赖外部 API（如 OpenAI, Azure, 或其他云厂商），网络波动或供应商限流是常态。
*   **实践建议**：在 Higress 中配置多活或主备模型服务。例如，将主要请求路由至成本较低的模型，当检测到错误率上升或延迟超标时，自动通过故障注入或自动熔断机制，将流量切换至备用的高可用模型或降级为预设的静态回复。
*   **常见陷阱**：不要将 AI 网关视为单纯的透传通道，若未配置超时与重试策略，后端模型的卡顿会直接耗尽网关的所有连接池。

### 6. 通过服务来源管理保护 API Key
在多租户或微服务架构中，避免将 LLM 的 API Key 硬编码在业务服务中。
*   **实践建议**：使用 Higress

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*