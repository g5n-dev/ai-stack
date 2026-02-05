---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-05T10:24:36+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "LLM", "云原生", "Istio", "Envoy", "WASM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是针对 Higress 项目的简洁总结： **Higress** 是阿里巴巴开源的一款**云原生 AI 网关**（AI Native API Gateway）。该项目基于 **Go** 语言开发，在 GitHub 上拥有超过 7,000 颗星。它构建在 **Istio** 和 **Envoy** 之上，通过扩展 W"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "AI/ML项目", "云原生/容器"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI Gateway | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,454 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在满足云原生环境下的流量治理需求。它不仅提供标准的微服务路由与 Kubernetes Ingress 管理，还深度集成了大模型应用所需的 AI 网关特性及 MCP 服务器托管能力。本文将梳理其核心架构，重点介绍 WASM 插件系统与 AI 相关功能，帮助开发者理解如何利用该工具统一管理传统流量与 AI 服务。

---
## 摘要

以下是针对 Higress 项目的简洁总结：

**Higress** 是阿里巴巴开源的一款**云原生 AI 网关**（AI Native API Gateway）。该项目基于 **Go** 语言开发，在 GitHub 上拥有超过 7,000 颗星。它构建在 **Istio** 和 **Envoy** 之上，通过扩展 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理服务。

**核心定位与架构：**
Higress 采用**控制平面**与**数据平面**分离的架构。它利用 xDS 协议进行配置分发，具备毫秒级延迟和无缝连接切换的特性，非常适合 AI 流式响应等长连接场景。

**三大主要功能场景：**

1.  **AI 网关**：专为 LLM（大语言模型）应用设计。
    *   提供统一 API 接入，兼容 30+ 家 LLM 提供商。
    *   核心功能包括协议转换、可观测性、缓存以及安全防护。
2.  **MCP 服务器托管**：服务于 AI Agent（智能体）的工具集成。
    *   托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务（如地图、搜索等）。
3.  **Kubernetes Ingress**：作为云原生 API 网关。
    *   兼容 Nginx Ingress 注解，支持微服务路由和 Kubernetes 流量管理。

简而言之，Higress 是一个将传统 API 网关能力与 AI 时代所需的 LLM 管理、协议转换及 Agent 工具调用能力深度融合的新一代网关系统。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的云原生网关，它成功地将**云原生流量治理**与**AI大模型编排**合二为一。作为阿里云开源的产物，它不仅继承了 Istio/Envoy 的稳健底座，更通过 WASM 和 AI 原生功能填补了传统网关在 LLM 时代的功能空白，是目前企业构建 AI 应用基础设施的优选方案之一。

**详细评价维度**

**1. 技术创新性：从“流量管道”进化为“智能中枢”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。同时，它集成了 AI Gateway 功能和 MCP (Model Context Protocol) 服务器托管。
*   **推断**：Higress 的核心差异化在于其**“AI Native”**定位。传统网关（如 Nginx, Kong）主要关注 HTTP 转发，而 Higress 内置了对 LLM 协议的深度支持。
    *   **协议转换与流式处理**：它不仅仅是转发请求，还能处理 SSE（Server-Sent Events）流，这对 AI 对话的响应速度至关重要。
    *   **MCP 集成**：支持托管 MCP Server 是一个极具前瞻性的创新。这意味着网关不仅仅是流量的入口，更成为了 AI Agent（智能体）的工具箱，直接解决了 Agent 调用外部工具时的连接与鉴权难题。
    *   **WASM 插件化**：利用 WASM 实现逻辑热更新，使得开发者可以用 C++/Go/Rust/AssemblyScript 编写高频逻辑（如 Key 验证、Prompt 注入、敏感词过滤），既保证了性能，又提供了极高的扩展性。

**2. 实用价值：解决 AI 落地“最后一公里”的连接难题**
*   **事实**：文档提到其三大核心功能包括 AI Gateway、MCP server hosting 以及传统的 API 网关能力。
*   **推断**：在 AI 应用落地中，开发者面临两大痛点：**模型提供商的碎片化**（OpenAI, Azure, 通义千问等接口标准不一）和**Token 成本与安全**。
    *   **统一抽象**：Higress 允许企业通过一个网关屏蔽不同模型厂商的 API 差异，实现模型切换的零代码改动。
    *   **成本与安全控制**：它可以在网关层实现统一的 Token 计费、并发限流（防止后端模型被击穿）和敏感数据脱敏。对于企业而言，这不仅是技术组件，更是成本控制和安全合规的关隘。

**3. 代码质量与架构：云原生工业级标准的继承者**
*   **事实**：项目基于 Go 语言开发，星标数 7,454，架构明确分离了控制面和数据面。
*   **推断**：基于 Envoy (C++) 作为数据面和 Go 作为控制面是目前云原生网关的黄金组合。
    *   **架构稳健**：控制面负责配置分发，数据面负责高性能转发，这种解耦设计保证了系统在高负载下的稳定性。
    *   **代码规范**：作为阿里系开源项目，其代码结构通常遵循严格的 Go 规范，且 README 提供了多语言版本（中/日/英），表明其具备国际化的视野和维护标准。WASM 插件的引入也证明了架构具有良好的模块化设计，避免了核心代码的臃肿。

**4. 社区活跃度与生态：背靠大树，连接广泛**
*   **事实**：Star 数超过 7k，且明确提到了对 Kubernetes Ingress 的支持。
*   **推断**：Higress 并非从零起步，它汲取了 Hango 和 Nginx Ingress 的经验，并得到了阿里云云原生团队的支持。其社区活跃度较高，且因为它兼容 K8s Ingress 标准，降低了 K8s 用户的学习门槛。对于国内开发者而言，中文文档的完善度是其社区活跃度的一大加分项。

**5. 学习价值：理解“网关即服务”的最佳范例**
*   **推断**：对于开发者而言，研究 Higress 有三个核心价值：
    1.  **学习 Envoy 与 WASM 的结合**：如何通过 WASM 在不重启网关的情况下动态修改流量行为，是现代高性能网关的必修课。
    2.  **理解 AI 流量特征**：通过阅读其 AI Gateway 实现，可以学到如何处理超长时连接、流式传输截断与拼接等 AI 特有的网络编程问题。
    3.  **MCP 协议的工程化实践**：作为新兴协议，MCP 在 Higress 中的实现是学习如何构建 AI Agent 基础设施的绝佳案例。

**6. 潜在问题与改进建议**
*   **复杂度曲线**：虽然功能强大，但基于 Istio 和 Envoy 的架构意味着运维门槛较高。对于仅需简单转发的场景，Higress 可能显得过重。
*   **建议**：建议官方提供更轻量级的“Standalone”模式部署文档，降低非 K8s 环境下的试用成本。同时，随着 AI 协议的快速迭代，需持续跟进主流模型（如 Claude 3.5, GPT-4o）的最新特性（如 Audio 支持）。

**7. 对比优势**
*   **对比 Nginx/Kong**：Higress 原生支持 K8s

---
## 技术分析

# Higress 技术深度分析报告

基于阿里巴巴开源的 Higress 仓库（alibaba/higress），这是一款基于 Istio 和 Envoy 构建的云原生 API 网关，其最显著的特征是提出了“AI Native”的概念，将大模型（LLM）的流量治理与传统微服务网关能力深度融合。以下是从八个维度进行的深入技术分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的架构模式，这是现代云原生网关的标准范式。
*   **数据平面**：深度依赖 **Envoy** 作为高性能代理底座。Envoy 负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **控制平面**：基于 **Istio** 进行了大幅度的裁剪和扩展。它去掉了 Istio 中繁重的 Sidecar 注入模式，专注于 Gateway（Ingress）场景。控制平面负责配置的下发，通过 xDS 协议（包括 LDS, CDS, RDS 等）与数据平面通信。
*   **扩展层**：引入了 **WebAssembly (WASM)** 作为插件运行时。Higress 默认代理了 WASM 的 HTTP 接口，允许用户在运行时动态加载 Go、C++、Rust 或 AssemblyScript 编写的插件，而无需重启网关。

### 核心模块与关键设计
1.  **AI 网关层**：这是 Higress 最具差异化的模块。它在网关层直接集成了对 LLM 协议（如 OpenAI 协议）的理解，能够处理 SSE（Server-Sent Events）流式传输，并提供 Prompt 管理和 Key 管理能力。
2.  **MCP (Model Context Protocol) 服务托管**：Higress 内置了对 MCP 协议的支持，能够作为 AI Agent 的工具提供者，将后端服务暴露为标准化的 MCP 工具供 LLM 调用。
3.  **Kubernetes Ingress Controller**：完全兼容 K8s Ingress 规范，可以作为 Nginx Ingress 的直接替代品。

### 技术亮点与创新点
*   **毫秒级配置推送**：得益于 Istio 的架构，配置变更通过 xDS 协议推送到 Envoy，实现了配置热更新，且在长连接（如 AI 流式响应）场景下不断连。
*   **AI 原生流量治理**：传统网关只看 HTTP 头和 Body，Higress 能够理解 LLM 的 Token 消耗，支持基于 Token 的限流和计费，这是传统网关无法做到的。
*   **WASM 插件市场**：提供了一个类似 VS Code 插件市场的生态，用户可以在控制台一键开启 WAF、Auth、缓存等功能。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量统一入口**：
    *   **场景**：企业内部同时调用 OpenAI、通义千问、DeepSeek 等多个模型。
    *   **功能**：Higress 提供统一的 API 接口，前端只需调用 Higress，由 Higress 根据配置路由到不同的模型提供商。它支持**模型切换**、**Key 轮转**（防止单 Key 被封禁影响全站）和**Fallback 机制**。
2.  **MCP Server 托管**：
    *   **场景**：构建 AI Agent 时，需要让 LLM 调用内部 API（如查询数据库、调用 ERP）。
    *   **功能**：Higress 可以将后端微服务自动封装为 MCP 工具，简化了 Agent 的工具链接入流程。
3.  **传统微服务网关**：
    *   **功能**：金丝雀发布、蓝绿部署、负载均衡、服务鉴权。

### 解决的关键问题
*   **LLM 供应商锁定**：通过统一抽象层，业务代码无需关心底层是哪个模型，切换模型只需修改网关配置。
*   **流式响应处理**：传统网关在处理 SSE 流时往往无法进行拦截或修改，Higress 针对数据流进行了优化，支持在流式传输过程中进行日志记录和内容审核。
*   **高成本控制**：针对 AI 请求的高昂成本，提供了基于 Token 或请求次数的精细化限流。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | APISIX |
| :--- | :--- | :--- | :--- |
| **底层架构** | Envoy + Istio (Go/C++) | Nginx (C) / Kong (Lua) | etcd + APISIX (Lua) |
| **AI 原生支持** | **内置** (Prompt/Token管理) | 需编写复杂脚本 | 需编写插件 |
| **配置热更新** | 毫秒级 (xDS) | 秒级/需 Reload | 毫秒级 |
| **扩展性** | WASM (高性能, 多语言) | C Module / Lua (高性能但单线程) | Lua / Python |
| **K8s 集成** | 原生 CRD 支持 | 需独立 Controller | 原生 CRD 支持 |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 之上嵌入了一个 WASM Runtime（通常基于 Wasmtime 或 V8）。它实现了一个 Proxy-WASM 的 ABI 接口。当 Go 代码编译为 WASM 后，它运行在一个沙箱环境中，可以直接访问请求的 Header、Body 和 Log，甚至通过 Host Calls 调用网关的能力。
*   **AI 协议转换**：Higress 实现了复杂的流式数据截断与重组算法。在处理 SSE 流时，网关作为中间人，接收来自 LLM 提供商的 `data: {}` 块，并实时转发给客户端，同时计算 Token 数量用于计量。

### 代码组织结构
*   **Pilot (Control Plane)**：主要用 Go 编写。负责监听 K8s API Server 和 Higress CRD，将其转换为 Envoy 的 xDS 配置。
*   **Gateway (Data Plane)**：基于 Envoy 构建。C++ 编写核心，但通过 WASM 桥接器允许 Go 代码介入业务逻辑。
*   **Console**：前端管理界面，提供可视化的流量管理和插件配置。

### 性能与扩展性
*   **性能**：Envoy 本身基于 C++，具有极高的 L7 处理性能。Higress 通过优化配置下发路径，减少了配置延迟。
*   **扩展性**：WASM 插件机制是核心。虽然 WASM 有一定的性能损耗（相比原生 C++），但其隔离性和多语言支持（开发者可以用 Go 写插件）极大地降低了开发门槛，且安全性远高于 Lua 脚本。

---

## 4. 适用场景分析

### 适合使用的项目
*   **AI 应用开发**：特别是那些需要集成多个 LLM 模型、需要统一管理 API Key、或需要构建 AI Agent 的企业。
*   **云原生微服务**：已经使用 Kubernetes 的用户，Higress 可以无缝替换 Ingress-Nginx，并提供更强大的流量管理。
*   **需要高度定制网关逻辑的场景**：利用 WASM 插件，企业可以开发极其私有的鉴权、加密或数据混淆逻辑，而不需要修改网关核心代码。

### 最有效的情况
当你的系统**既有传统的微服务 API 流量，又有新兴的 AI LLM 流量**，且希望用一套基础设施统一治理时，Higress 是目前最优的选择。

### 不适合的场景
*   **极边缘计算**：Envoy 和 WASM 的资源消耗相对较高（MB 级别），对于资源极度受限的 IoT 设备（KB 级别）可能过于重。
*   **简单的静态文件托管**：如果是纯粹的静态 CDN 场景，使用 Nginx 或 Caddy 更轻量。

### 集成方式
通常作为 K8s DaemonSet 或 Deployment 部署，通过 Service (LoadBalancer/NodePort) 暴露，并配置 IngressClass 来接管特定域名的流量。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 LLM 可观测性**：未来将不仅仅转发流量，还会对 Prompt 和 Response 进行深度分析，提供如“Prompt 注入检测”、“敏感词过滤”等内生安全能力。
*   **Dapr 集成**：Higress 可能会进一步与 Dapr (Distributed Application Runtime) 融合，成为服务网格与 Sidecar 模式下的统一入口。

### 社区反馈与改进空间
*   **文档与易用性**：虽然功能强大，但 WASM 插件的开发调试流程对于初学者仍有门槛（需要本地编译 WASM 并上传）。
*   **控制面性能**：在大规模集群（数千个 Service）下，Istio 控制面的资源消耗依然是挑战，Higress 需要持续优化配置同步机制。

---

## 6. 学习建议

### 适合的开发者
*   **中高级后端工程师**：特别是对云原生、微服务治理有了解的开发者。
*   **AI 应用架构师**：需要设计 AI 基础设施的技术负责人。

### 学习路径
1.  **基础理论**：理解 Envoy Proxy 的基本概念（Listener, Filter, Cluster）。
2.  **云原生标准**：学习 Kubernetes Ingress 和 Gateway API 规范。
3.  **WASM 编程**：学习如何使用 Go 或 TinyGo 编写 Proxy-WASM 插件。
4.  **实践**：在本地 Kind 集群中部署 Higress，尝试配置一个转发到 OpenAI 的路由，并编写一个简单的 Wasm 插件修改 Request Header。

---

## 7. 最佳实践建议

### 正确使用指南
*   **插件隔离**：生产环境中，对性能敏感的插件（如限流、认证）尽量使用原生 Filter 或高度优化的 WASM 插件，避免在插件中进行阻塞式 HTTP 调用。
*   **资源限制**：WASM 虚拟机需要内存，务必为 Higress 的 Pod 设置合理的 Memory Limit，防止 OOM。
*   **配置管理**：利用 GitOps 管理 Higress 的 Config，避免在控制台手动修改导致配置漂移。

### 性能优化建议
*   **开启连接复用**：在后端服务（如 LLM Provider）支持的情况下，开启 HTTP/2 或 gRPC 连接池，减少握手开销。
*   **WASM 缓存**：确保 WASM 插件被预编译和缓存，避免每次请求重新加载 VM。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**“流量治理的标准化”**这一抽象层上做了大量工作。
*   **复杂性转移**：它将**业务代码的复杂性**（如何调用不同模型、如何重试、如何鉴权）转移到了**网关基础设施层**。同时，它将

---
## 代码示例


展示如何通过Higress实现基于路径的流量路由，实际部署时只需在Higress控制台配置路由规则即可实现服务发现和负载均衡。

```python
# 示例1：基于Higress的API网关流量路由
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    模拟用户查询接口
    实际生产中会连接数据库或调用下游服务
    """
    # 模拟用户数据
    users = {
        1: {"name": "张三", "role": "admin"},
        2: {"name": "李四", "role": "user"}
    }
    
    user = users.get(user_id, {"error": "用户不存在"})
    return jsonify(user)

if __name__ == '__main__':
    # 在Higress中配置路由规则：
    # /api/v1/user/* -> 转发到本服务:5000
    app.run(host='0.0.0.0', port=5000)
```


演示如何通过Higress实现金丝雀发布，通过流量控制逐步验证新版本功能，降低发布风险。

```python
# 示例2：使用Higress进行金丝雀发布
import random

@app.route('/api/v2/feature', methods=['GET'])
def new_feature():
    """
    新版本功能接口
    通过Higress配置实现灰度发布
    """
    # 模拟新功能逻辑
    if random.random() > 0.5:  # 50%流量使用新逻辑
        return jsonify({"version": "v2", "feature": "新功能"})
    return jsonify({"version": "v1", "feature": "旧功能"})

# 在Higress中配置金丝雀规则：
# 50%流量 -> v2版本服务
# 50%流量 -> v1版本服务
```


展示如何开发Higress自定义插件实现认证功能，实际使用时需要实现Higress的插件接口规范，并在控制台进行配置。

```python
# 示例3：Higress插件开发示例
class AuthPlugin:
    """
    自定义认证插件示例
    实际使用时需要实现Higress的插件接口
    """
    def __init__(self, config):
        self.config = config
    
    def on_request(self, request):
        """
        请求拦截处理
        """
        # 检查请求头中的认证信息
        auth_header = request.headers.get('Authorization')
        if not auth_header or not self._validate_token(auth_header):
            return {"status": 401, "message": "未授权访问"}
        
        # 添加认证通过的标记
        request.headers['X-Auth-Status'] = 'success'
        return None  # 继续处理请求
    
    def _validate_token(self, token):
        """
        简单的token验证逻辑
        实际应该连接认证服务验证
        """
        return token.startswith("Bearer ") and len(token) > 10

# 在Higress中配置插件：
# 1. 将插件打包上传
# 2. 在路由规则中启用该插件
# 3. 配置插件参数（如token验证规则）
```


---
## 案例研究


### 1：阿里巴巴淘天集团

 1：阿里巴巴淘天集团

**背景**:  
在阿里巴巴内部，Higress 是基于内部两年多的 Envoy 网关实践沉淀而出的开源标准。在淘天集团（淘宝、天猫等核心电商业务）的云原生架构转型过程中，面临着极其复杂的流量管理挑战。每年双11大促期间，流量峰值巨大，且业务逻辑极其复杂，涉及成千上万的微服务之间的调用。

**问题**:  
传统的 API 网关在处理海量并发连接时存在性能瓶颈，且对于不同协议（如 HTTP、Dubbo、gRPC）的统一管理和路由配置较为繁琐。此外，随着业务微服务化，需要网关具备更强的扩展性来支持自定义的流量治理逻辑（如灰度发布、流量标签路由），同时需要降低与内部 Service Mesh（如 Istio）集成的复杂度。

**解决方案**:  
淘天集团全面采用 Higress 作为其统一的云原生 API 网关。利用 Higress 基于 Envoy 和 Istio 的底层架构，实现了与底层服务网格的无缝对接。通过 Higress 的 Wasm 插件市场，开发团队能够用 C++、Go 或 Rust 编写高性能的自定义插件，实现了精细化的流量控制和安全防护，替代了传统网关中低效的 Lua 脚本。

**效果**:  
成功支撑了双11期间每秒数十万级的 QPS（每秒查询率），显著降低了网关层的资源消耗和延迟。通过标准化的 Ingress 配置，实现了多集群流量的统一调度，提升了系统的稳定性。同时，Wasm 插件的沙箱隔离机制保证了网关内核的安全性，使得新业务逻辑的上线效率提升了 50% 以上。

---



### 2：某大型互联网公司 AI 应用网关

 2：某大型互联网公司 AI 应用网关

**背景**:  
随着 AIGC（生成式人工智能）浪潮的兴起，一家专注于智能客服领域的科技公司需要构建一个能够处理大量并发请求的 AI 网关。该公司的后端接入了多个大语言模型（LLM）提供商（如 OpenAI、通义千问、Llama 等），前端则面向企业客户提供 SaaS 服务。

**问题**:  
直接对接不同的 LLM 服务商存在 API 标准不统一的问题（如参数格式差异、鉴权方式不同）。此外，AI 请求通常耗时较长（Token 流式输出），容易导致连接超时或资源占用过高。传统的网关难以处理这种长连接和流式数据的转发，且缺乏针对 AI 语义层面的缓存和流控能力，导致 API 调用成本高昂。

**解决方案**:  
该公司引入 Higress 作为 AI 网关。利用 Higress 对 AI 生态的原生支持，统一了不同模型提供商的 API 接口规范。通过配置 Higress 的流式转发能力，确保了大模型生成的 Token 能够实时、低延迟地传输给终端用户。同时，利用 Higress 的插件能力实现了基于语义的缓存和请求限流，避免了对大模型的重复无效调用。

**效果**:  
实现了对后端多种 AI 模型的统一管理，屏蔽了厂商差异，开发效率提升 30%。通过智能缓存和连接复用技术，成功将 API 调用成本降低了 40%，并在高并发场景下避免了网关层的资源耗尽，保证了用户交互的实时性和流畅性。

---



### 3：萝卜快跑

 3：萝卜快跑

**背景**:  
萝卜快跑是百度旗下的自动驾驶出行服务平台。其业务系统架构复杂，涉及车载终端、云端调度中心、地图服务以及高精定位等多个子系统。系统需要处理海量的实时车辆位置数据、订单请求以及视频流数据，对网络通信的实时性和安全性要求极高。

**问题**:  
在业务快速扩张期，原有的网关系统在处理 WebSocket 长连接（用于车辆实时状态推送）时出现性能瓶颈，且难以对海量物联网设备的接入进行有效鉴权。此外，不同业务线（如运力调度、乘客端 App、司机端 App）的接口协议各异，缺乏统一的流量治理和安全防护标准，导致运维成本高企。

**解决方案**:  
百度 Apollo 团队采用 Higress 作为其边缘网关和内部 API 网关的核心组件。利用 Higress 对 HTTP、gRPC 及 WebSocket 协议的高性能支持，统一接管了所有南北向流量。通过 Higress 的细粒度权限控制插件，实现了针对不同车型和终端设备的严格鉴权。同时，借助其与 Kubernetes 的深度集成，实现了网关实例的弹性伸缩，以应对早晚高峰的流量波动。

**效果**:  
网关系统成功承载了数万辆自动驾驶车辆的实时并发连接，消息转发延迟降低至毫秒级，极大地提升了车辆调度的响应速度。统一的流量治理策略使得接口安全性得到显著增强，有效抵御了恶意攻击。通过云原生架构的落地，运维效率提升了 40%，资源利用率优化了 25%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持WASM插件扩展 | 高性能，基于OpenResty/Nginx，支持Lua插件 | 极高性能，基于OpenResty/Nginx，支持Lua和WASM插件 |
| 易用性 | 提供控制台和K8s集成，适合云原生环境 | 控制台功能丰富，社区支持强 | 控制台简洁，配置灵活，社区活跃 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源版免费，企业版收费 | 开源免费，商业支持可选 |
| 扩展性 | 支持WASM和自定义插件，扩展性强 | 支持Lua插件和自定义扩展 | 支持Lua和WASM插件，扩展性极强 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API管理 | 传统API网关、混合云 | 高并发、云原生、API管理 |

### 优势分析

- 优势1：深度集成Istio和Envoy，适合云原生和微服务架构。
- 优势2：支持WASM插件，扩展性强且性能损耗低。
- 优势3：阿里云提供商业支持，适合企业级应用。

### 不足分析

- 不足1：社区资源相比Kong和APISIX较少，生态尚在发展中。
- 不足2：控制台功能可能不如Kong丰富。
- 不足3：对非K8s环境的支持可能不如传统网关（如Nginx）。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 注解的精细化流量管理

**说明**: Higress 深度集成了 Kubernetes Ingress 资源，通过在 Ingress YAML 中添加特定的注解，可以实现无需修改网关配置的流量控制。这包括基于 Header 的路由、金丝雀发布以及流量镜像等高级功能，充分利用 Higress 对 Nginx Ingress 注解的兼容性来降低迁移成本。

**实施步骤**:
1. 在 Kubernetes 的 Ingress 资源 metadata 中添加 `nginx.ingress.kubernetes.io` 前缀的注解，或 Higress 原生注解。
2. 配置灰度发布注解（如 `canary-by-header`）将特定流量引入新版本服务。
3. 应用配置后，通过 Higress 控制台或日志观测流量分发是否符合预期。

**注意事项**: 虽然兼容 Nginx 注解，但建议优先查阅 Higress 官方文档确认特定注解的支持情况，对于复杂逻辑，建议使用 Higress 的 `WasmPlugin` 或原生路由规则替代，以获得更好的性能。

---

### 实践 2：利用 Wasm 插件扩展网关业务逻辑

**说明**: Higress 的核心优势之一是其对 WebAssembly (Wasm) 的原生支持。相比于传统的 Lua 脚本或硬编码网关逻辑，Wasm 插件允许使用 C++、Go、Rust 或 AssemblyScript 编写业务逻辑（如 JWT 验证、请求阻断、响应转换），并支持动态加载，无需重启网关即可生效。

**实施步骤**:
1. 访问 Higress 官方插件市场或使用 `wasm-assembler` 工具将业务代码编译为 `.wasm` 文件。
2. 将 `.wasm` 文件上传至 OCI 兼容的镜像仓库（如 Docker Hub 或阿里云容器镜像服务）。
3. 在 Higress 控制台配置 `WasmPlugin` 资源，指定 Wasm 文件的镜像地址，并将其绑定到特定的网关路由或域名上。

**注意事项**: Wasm 插件的执行会增加少量的网络延迟，应避免在插件中编写阻塞式或长耗时的 I/O 操作。生产环境部署前应对插件进行性能压测。

---

### 实践 3：服务发现与 Nacos/Sentinel 无缝集成

**说明**: Higress 设计初衷是为了打通微服务网关与入口网关的边界。通过配置 Nacos 注册中心，Higress 可以直接将后端微服务动态解析为服务来源，并结合 Sentinel 实现自适应限流保护，从而构建从流量入口到微服务调用的全链路高可用体系。

**实施步骤**:
1. 在 Higress 全局配置或特定服务来源中，添加 Nacos 注册中心地址及命名空间信息。
2. 配置服务来源，选择 "Nacos" 并建立服务连接。
3. 在路由配置中直接选择 Nacos 中的服务名作为后端服务，无需手动配置具体的 Pod IP。
4. 关联 Sentinel 限流规则，配置 QPS 阈值或并发线程数。

**注意事项**: 确保 Higress 所在的网络环境能够直接访问 Nacos 服务器地址和端口。若使用云上托管的 Nacos，需配置好相应的鉴权信息（AccessKey）。

---

### 实践 4：全链路安全防护与 mTLS 认证

**说明**: 在处理敏感数据或金融级业务时，仅依靠 HTTP 基础认证是不够的。Higress 支持配置 mTLS (双向认证) 来加密网关与后端服务之间的通信流量，并支持集成 OIDC (OpenID Connect) 进行单点登录和身份认证，确保只有经过验证的客户端和服务才能交互。

**实施步骤**:
1. 在 Higress 控制台或通过 ConfigMap 配置 mTLS 策略，上传 CA 证书、服务端证书和私钥。
2. 配置 `DestinationRule`，强制要求特定命名空间的服务启用 mTLS 通信模式。
3. 若需客户端认证，配置 OIDC 插件，填入 IdP (身份提供商) 的 Client ID、Secret 和 Discovery URL。

**注意事项**: 证书管理至关重要，务必监控证书的过期时间并建立自动轮换机制，避免因证书过期导致服务中断。

---

### 实践 5：高可用部署与资源隔离

**说明**: 在生产环境中，网关作为流量的咽喉，必须具备高可用性。Higress 基于 Envoy 构建，本身是无状态的，建议使用 Deployment 或 DaemonSet 部署，并结合 Kubernetes 的 Pod 反亲和性策略，确保网关实例分散在不同的节点上，防止单点故障。

**实施步骤**:
1. 设置 Higress 的副本数至少为 3 个，以保证集群冗余。
2. 配置 Pod Anti-Affinity (反亲和性)，确保每个节点最多运行一个 Higress 副本（或根据资源情况调整）。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 构建，天然支持现代网络协议。HTTP/2 通过多路复用解决了线头阻塞问题，而 HTTP/3 (QUIC) 基于 UDP 实现，进一步解决了 TCP 层的队头阻塞，显著降低了高丢包率网络环境下的延迟。

**实施方法**:
1. 在网关监听器配置中，明确启用 HTTP/2 协议支持。
2. 对于客户端连接，在 Higress 的路由配置或全局配置中开启 HTTP/3 (QUIC) 支持。
3. 确保后端 Upstream 服务也配置为 HTTP/2 或 gRPC 协议，以利用长连接减少握手开销。

**预期效果**: 在弱网环境下，请求延迟可降低 30%-50%；高并发场景下 TCP 连接数大幅减少，连接池利用率提升。

---

### 优化 2：配置全链路连接池与 Keep-Alive

**说明**: 默认配置下，如果未调优连接参数，频繁的 TCP 三次握手和四次挥手会消耗大量 CPU 和网络带宽。保持客户端与 Higress、Higress 与后端服务之间的长连接至关重要。

**实施方法**:
1. **客户端侧**: 调整 `idleTimeout` 参数，适当延长空闲超时时间（例如设置为 60s 或更长），避免频繁断连。
2. **后端侧**: 在 `Upstream` 配置中，合理设置连接池大小。根据后端服务器的处理能力调整 `maxRequestsPerConnection`。
3. 启用 `http2_protocol_options` 中的 `keepalive` 时间，确保 HTTP/2 连接不断开。

**预期效果**: 后端服务连接建立开销减少 90% 以上，网关 P99 延迟显著降低，吞吐量（QPS）提升 20%-40%。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持通过 Wasm (WebAssembly) 扩展功能。相比于 Lua 或远程调用，Wasm 提供了接近原生的执行速度。此外，对于鉴权、配置下发等高频调用场景，利用 Higress 的本地缓存能力可以极大减少对后端的请求。

**实施方法**:
1. 将高频使用的鉴权、限流或请求头处理逻辑通过 Wasm 插件实现，而非调用外部 HTTP API。
2. 在网关配置中启用 `cache` 功能，对后端响应进行缓存（针对 GET 请求）。
3. 在插件代码内部实现内存缓存（如缓存 JWT 签名验证结果或配置元数据），减少重复计算。

**预期效果**: 插件执行延迟降低至微秒级；对于可缓存内容的请求，后端负载减少 60%-80%，响应时间降低 90% 以上。

---

### 优化 4：启用 CPU 亲和性与零拷贝优化

**说明**: Envoy (Higress 核心) 在 Linux 环境下可以通过 `SO_REUSEPORT` 和 CPU 亲和性优化来减少上下文切换和锁竞争。开启零拷贝技术可以减少数据在内核空间与用户空间之间的拷贝次数。

**实施方法**:
1. **启动参数**: 确保 Higress 启动时配置了 `--enable-atomic-tx` 或相关的 Envoy 优化参数。
2. **系统配置**: 在宿主机或 Pod 配置中启用 `SO_REUSEPORT`，允许多个工作线程监听同一端口。
3. 调整 Worker 线程数，通常建议设置为 CPU 核心数，并绑定 CPU 核心以避免线程在不同核心间迁移。

**预期效果**: 网关 CPU 利用率更加平滑，在超高 QPS 场景下，长尾延迟（P999）可降低 15%-30%。

---

### 优化 5：启用 DNS 缓存与 IP 地址自动发现

**说明**: 默认情况下，网关可能会频繁请求 DNS 解析后端服务域名，这不仅增加了延迟，DNS 服务器也可能成为

---
## 学习要点

- Higress 是阿里巴巴开源的基于 Istio 的云原生 API 网关，旨在提供高性能、可扩展的流量管理和服务治理能力。
- 它深度集成了 K8s Ingress 和 Gateway API，支持声明式配置，能无缝对接云原生生态。
- 内置了对 Dubbo、Nacos 和 gRPC 等微服务协议的扩展支持，解决了传统网关对微服务协议兼容性差的问题。
- 提供了强大的 WAF（Web 应用防火墙）插件和安全防护能力，保障服务接口的安全性。
- 支持热更新和动态路由配置，可以在不重启服务的情况下实时调整流量规则，降低运维风险。
- 兼容 Envoy 和 Kong 的插件生态，允许用户低成本迁移现有插件或进行二次开发。
- 提供了完善的控制台和可观测性支持（对接 Prometheus、SkyWalking 等），便于监控和排查链路问题。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 在现代微服务架构中的定位与作用。
- Higress 项目背景：了解 Higress 的开源背景、基于 Istio 和 Envoy 的技术架构。
- 基本概念：掌握 Ingress、Gateway、路由、服务发现等核心术语。
- 环境搭建：学习如何在 Kubernetes 集群中通过 Helm 或 YAML 快速部署 Higress。
- 控制台使用：熟悉 Higress Dashboard 的界面布局与基础操作。

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 仓库 README
- Higress 官方文档 - 快速开始章节
- Kubernetes 官方文档 - Ingress 概念

**学习建议**:
建议先阅读官方文档了解架构图，随后在本地或测试环境的 Kubernetes 集群（如 Kind 或 Minikube）中完成一次标准安装，并尝试通过控制台创建一个简单的路由转发。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- HTTP 路由配置：学习如何配置域名、路径匹配、Header 重写等基础路由规则。
- 负载均衡策略：掌握轮询、随机、一致性哈希等负载均衡算法的配置。
- 金丝雀发布与蓝绿发布：学习基于 Header 或权重进行流量切分，实现灰度发布。
- 服务发现集成：了解如何对接 Nacos、Consul、Kubernetes Service 等注册中心。
- 全局与插件配置：学习 CORS、重定向、限流基础等通用流控能力的配置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理章节
- Envoy 官方文档 - HTTP 路由
- Nacos 注册中心对接文档

**学习建议**:
此阶段重点在于实践。建议部署两个版本的后端服务（如 v1 和 v2），通过配置 Higress 的路由规则，实现将特定流量（如包含特定 Header）导向 v2 版本，从而验证灰度发布能力。

---

### 阶段 3：安全防护与可观测性

**学习内容**:
- 认证与鉴权：学习如何配置 Basic Auth、JWT 验证、ApiKey 认证以及 OIDC。
- 安全插件：了解 WAF 防护、IP 访问控制、请求防重放等安全策略。
- 可观测性集成：学习如何配置 Prometheus 监控、访问日志采集以及分布式链路追踪。
- 自定义插件开发：了解 Wasm (WebAssembly) 技术在 Higress 中的应用，尝试编写简单的 Go 或 Rust 插件。

**学习时间**: 2-4周

**学习资源**:
- Higress 官方文档 - 安全与可观测性章节
- Higress 官方文档 - Wasm 插件开发
- Prometheus 与 Grafana 基础教程

**学习建议**:
安全方面，建议尝试对接外部 OIDC 提供商（如 Keycloak）进行身份验证。可观测性方面，重点在于配置日志格式并导出到 Elasticsearch 或 Loki，并在 Grafana 中导入 Higress 的仪表盘模板进行监控分析。

---

### 阶段 4：高阶应用与性能调优

**学习内容**:
- 高可用部署：学习 Higress 的高可用架构设计，包括多副本部署与灾备切换。
- 性能调优：掌握连接池配置、缓冲区大小调整、超时时间优化等参数。
- 多集群管理：了解在多 Kubernetes 集群环境下使用 Higress 进行流量统一管理。
- 服务网格集成：深入理解 Higress 与 Istio 的协同工作模式，实现东西向与南北向流量的统一治理。
- 生产级运维：掌握版本升级策略、回滚机制及常见故障排查。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方博客 - 最佳实践
- Istio 官方文档 - 网格与网关集成
- Linux 内核网络参数调优指南

**学习建议**:
此阶段适合有生产环境需求的用户。建议进行压测（使用 JMeter 或 Hey），根据压测结果调整 Higress 的 Pod 资源限制与 Envoy 配置参数，同时阅读源码或社区案例以解决复杂的网络路由问题。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是基于阿里内部多年实践及开源项目 Istio 和 Envoy 演进而来的。它旨在为云原生架构提供统一的流量管理入口。

与 Nginx 相比，Higress 具备更强大的动态路由、服务发现以及流量治理能力（如金丝雀发布、全链路灰度），且配置支持热更新，不需要 Reload 进程。与 Kong 相比，Higress 深度集成了 Istio，可以更好地实现 Ingress（南北向流量）与 Mesh（东西向流量）的统一管理，且底层基于 Envoy，性能在高并发场景下表现优异，同时支持 WASM 插件进行功能扩展。

---



### 2: Higress 与 K8s Ingress、Istio Gateway 是什么关系？

2: Higress 与 K8s Ingress、Istio Gateway 是什么关系？

**A**: Higress 兼容 Kubernetes Ingress 规范，可以作为 K8s 的标准 Ingress Controller 使用。同时，Higress 也是 Istio Gateway 的一个高性能实现。

在架构上，Higress 将控制面和数据面进行了更轻量级的集成。它允许用户通过 K8s Ingress、Gateway API 或 Istio VirtualService 等多种方式配置路由规则。对于已经使用 Istio 的用户，Higress 可以作为集群入口网关，与集群内部的 Sidecar 无缝协同工作，简化了网关的运维复杂度。

---



### 3: 如何在 Higress 中扩展功能？它支持哪些插件？

3: 如何在 Higress 中扩展功能？它支持哪些插件？

**A**: Higress 提供了强大的插件扩展机制，主要支持以下两类插件：

1.  **原生插件**: Higress 内置了大量开箱即用的插件，包括认证鉴权（如 Basic Auth、API Key、JWT）、流量管控（如限流、熔断）、可观测性（如日志、链路追踪）以及请求/响应修改等。
2.  **WASM 插件**: 这是 Higress 的一大亮点。它支持 WebAssembly (WASM) 标准，允许开发者使用 C++、Go、Rust、JavaScript 或 TypeScript 编写自定义插件逻辑。WASM 插件具有动态加载、隔离性好和多语言支持的特点，无需重启网关即可生效。

---



### 4: Higress 的性能表现如何？能否支持高并发场景？

4: Higress 的性能表现如何？能否支持高并发场景？

**A**: Higress 的底层基于 Envoy，这是一个用 C++ 编写的高性能代理。经过阿里内部双十一等大流量场景的验证，Higress 在处理长连接、高并发请求和低延迟转发方面表现优异。

在标准硬件配置下，Higress 能够轻松支撑每秒数十万级别的请求处理（RPS）。其异步非阻塞的架构设计使得在开启大量插件（如 WAF、限流）的情况下，依然能保持较低的请求延迟损耗。

---



### 5: Higress 是否支持从 Nginx 或 Apache APISIX 迁移？

5: Higress 是否支持从 Nginx 或 Apache APISIX 迁移？

**A**: 是的，Higress 提供了完善的迁移工具和兼容性支持。

1.  **Nginx Ingress**: Higress 兼容 K8s Ingress 规范，因此可以直接替换 Nginx Ingress Controller，通常只需调整少量注解配置。
2.  **Nginx 配置**: 对于传统的 Nginx 配置，Higress 提供了 Nginx 配置转换工具，可以帮助用户将 Nginx 的 `location` 和 `upstream` 配置转换为 Higress 的路由配置。
3.  **Apache APISIX**: 虽然底层架构不同，但两者概念相似（路由、插件、Upstream）。迁移主要涉及配置层面的转换，Higress 支持类似的动态路由和插件加载逻辑。

---



### 6: Higress 如何保障安全性？

6: Higress 如何保障安全性？

**A**: Higress 在多个层面提供了安全防护能力：

1.  **认证与鉴权**: 支持多种身份验证方式，包括 Keyless 认证、JWT 验证、OIDC、Basic Auth 等，并能对接外部 OAuth 服务。
2.  **IP 访问控制**: 支持黑名单和白名单机制，允许或拒绝特定 IP 或 IP 段的访问。
3.  **流量防护**: 内置限流熔断功能，可以防止下游服务被突发流量击垮。
4.  **安全插件**: 提供类似 WAF（Web Application Firewall）的安全插件，用于防御 SQL 注入、XSS 等常见 Web 攻击。

---



### 7: Higress 是开源项目吗？在哪里可以获取支持？

7: Higress 是开源项目吗？在哪里可以获取支持？

**A**: 是的，Higress 是完全开源的。该项目由阿里云发起，并捐赠给了云原生计算基金会（CNCF）作为沙盒项目进行孵化。

源代码托管在 GitHub 上（通常在 `alibaba/higress` 仓库）。用户可以通过 GitHub Issues 提交 Bug 或功能请求，也可以加入官方的 Discord 或钉钉群获取社区支持。阿里云同时也提供了商业版本 Higress（在云产品中

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 环境搭建与基础路由配置

### 难度**: 简单

### 问题描述**:

### 假设你需要在本地快速体验 Higress。请描述如何使用 Docker Compose 一键部署一个包含 Higress 控制台和默认网关节点的环境。部署成功后，请配置一个简单的路由规则：当访问 `http://localhost/test` 时，能够将流量转发到一个公网可访问的测试网站（例如 httpbin.org）。

---
## 实践建议

以下是针对 Higress（AI Native API Gateway）的 5-7 条实践建议，侧重于生产环境落地与 AI 场景优化：

### 1. 利用 Wasm 插件实现模型供应商的统一适配
Higress 的核心优势在于其 AI 原生能力，特别是对不同大模型供应商（如 OpenAI, Azure, 通义千问, DeepSeek 等）的兼容性。
*   **建议**：不要在业务代码中硬编码不同厂商的 API 调用逻辑。在 Higress 中配置**全局路由或服务**，将不同的模型供应商统一映射为标准的 OpenAI API 格式。
*   **操作**：通过 Higress 的 `ai-proxy` 插件，将后端不同的 LLM 服务地址配置为不同的服务，并在路由中通过 Header（如 `x-model-provider`）进行流量分发。这样业务端只需对接一套接口标准，即可灵活切换底层模型。
*   **价值**：降低供应商锁定风险，便于后续进行 A/B 测试或模型降级切换。

### 2. 配置精准的 Token 限流与计费
大模型 API 的成本主要与 Token 消耗量成正比，传统的基于 QPS（每秒请求数）或并发连接数的限流策略无法准确反映成本。
*   **建议**：启用基于 Token 或请求计数的细粒度限流策略。
*   **操作**：在 Higress 的 `key-rate-limit` 插件或针对 AI 的高级限流配置中，针对不同的 API Key 或用户维度设置 Token 预算。例如，限制某个测试用户每天最多消耗 100万 Tokens。
*   **陷阱**：如果仅配置 QPS 限流，可能会被恶意用户通过发送超长 Prompt 的方式绕过，导致单次请求消耗巨额 Token。

### 3. 实施语义缓存以降低延迟与成本
对于知识库问答或高频重复问题，每次都请求大模型会造成不必要的成本和延迟。
*   **建议**：开启 Higress 的语义缓存功能。
*   **操作**：配置缓存插件，设定基于向量相似度的匹配阈值。当用户提问与缓存中的问题语义高度一致时，直接网关层返回缓存结果，无需转发给 LLM。
*   **最佳实践**：建议对“事实性”问题（如“公司报销政策是什么”）开启缓存，而对“创作性”问题（如“写一首诗”）关闭缓存，以平衡准确性与成本。

### 4. 妥善处理 SSE 流式传输的超时与断连
AI 对话通常采用 Server-Sent Events (SSE) 流式返回，这比普通 HTTP 请求更复杂。
*   **建议**：检查并调整网关及后端服务的超时配置，确保长连接不被意外切断。
*   **操作**：
    *   在 Higress 路由配置中，将 `request_timeout` 或 `idle_timeout` 设置为较大的值（例如 5 分钟），以支持长文本生成。
    *   确保后端服务正确返回 `Content-Type: text/event-stream`。
*   **常见陷阱**：如果在网关层开启了过多的 Body 修改插件或全量缓存插件，可能会导致流式响应被缓冲，从而破坏流式输出的体验，导致前端“卡顿”直到全部生成完毕才显示。

### 5. 建立模型熔断与降级机制
大模型 API 可能会出现波动（如限流 429 错误或服务不可用）。
*   **建议**：在 Higress 中配置自动化的容错策略。
*   **操作**：利用 Higress 的离群实例检测功能。当某个模型提供商的接口出现连续超时或 5xx 错误时，自动将其暂时摘除，将流量切换到备用模型（例如从 GPT-4 切换到 GPT-3.5 或其他国产模型）。
*   **价值**：保证 AI 服务的可用性（SLA），避免因单一厂商故障导致业务瘫痪。

### 6. 敏感数据脱敏与安全审计
企业内部使用 AI 时，极易发生将代码

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [LLM](/tags/llm/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*