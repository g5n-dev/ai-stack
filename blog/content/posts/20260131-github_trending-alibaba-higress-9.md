---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T08:01:57+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "Istio", "Envoy", "WASM", "MCP", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力，旨在为现代云原生应用和 AI 应用提供统一的流量管理入口。 以下是关于 Higress 的核心总结： **1. 架构与技术特点** * **"
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
- **星标**: 7,415 (+9 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过集成 WebAssembly 插件能力，实现了对 Kubernetes Ingress、微服务路由及 LLM 应用的统一管理。本文将深入剖析其核心架构，重点介绍 MCP 系统支持及 AI 网关的关键特性，帮助开发者理解如何利用 Higress 构建高效、可扩展的入口管理服务。

---
## 摘要

Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力，旨在为现代云原生应用和 AI 应用提供统一的流量管理入口。

以下是关于 Higress 的核心总结：

**1. 架构与技术特点**
*   **底层基础：** 构建于 Istio 和 Envoy 之上，利用 Envoy 处理高频流量，利用 Istio 进行服务网格管理。
*   **控制与数据分离：** 采用控制平面（配置管理）与数据平面（流量处理）分离的架构。
*   **高性能配置：** 配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适用于 AI 长连接流式响应场景。
*   **可扩展性：** 通过 WASM 插件机制提供强大的扩展能力，支持 Go、C++、Rust 等多种语言编写插件。

**2. 三大核心功能与用途**

Higress 目前主要定位在以下三个核心使用场景：

*   **AI 网关：**
    *   **功能：** 为大语言模型 (LLM) 应用提供统一 API，支持对接 30+ 家 LLM 服务商。
    *   **特性：** 提供协议转换、可观测性、智能缓存以及安全防护。
    *   **核心组件：** `ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件。

*   **MCP 服务器托管：**
    *   **功能：** 托管模型上下文协议 (MCP) 服务器，使 AI Agent 能够方便地调用外部工具和服务。
    *   **核心组件：** 包含 `mcp-router`、`jsonrpc-converter` 以及多种内置实现（如 `quark-search`、`amap-tools`）。

*   **云原生 API 网关：**
    *   **功能：** 提供传统的 API 网关能力，支持 Kubernetes Ingress 和微服务路由。
    *   **兼容性：** 兼容 Nginx Ingress 注解，可作为 Kubernetes 的 Ingress Controller 使用。

**3. 开源状态**
*   **开发语言：

---
## 评论

**总体判断**

Higress 是阿里云开源的下一代云原生网关，它最核心的战略价值在于**将“AI 网关”与“传统 API 网关”在架构与生态上进行了深度融合**。它不仅仅是基于 Envoy 的高性能流量入口，更通过 WASM 和 MCP 协议，成为了连接大模型（LLM）与应用程序的关键基础设施，是目前云原生网关领域向 AI Native 方向演进中极具竞争力的标杆产品。

**详细评价依据**

**1. 技术创新性：AI Native 架构与 WASM 插件生态**
*   **事实（来源）：** Higress 基于 Istio 和 Envoy 构建，核心特性包括 WebAssembly (WASM) 插件能力、AI Gateway 功能以及 MCP (Model Context Protocol) Server 托管。
*   **推断（分析）：** 传统网关（如 Nginx, Kong）主要处理 HTTP 转发，而 Higress 的差异化在于它**原生内置了 AI 全生命周期管理能力**。
    *   **AI 提示词管理：** 它不仅仅做路由，还能在网关层做 Prompt 模板化和版本管理，这对降低后端服务改动成本至关重要。
    *   **MCP 协议支持：** 支持 MCP Server 托管是一个极具前瞻性的技术选型。随着 AI Agent 的普及，模型需要通过 MCP 协议调用外部工具，Higress 直接充当了 Agent 的工具箱，这比让每个应用单独实现 MCP 客户端要高效得多。
    *   **WASM 插件化：** 使用 WASM (C++/Go/Rust) 编写业务逻辑，既保持了 Envoy 的高性能，又打破了 Lua 脚本的性能瓶颈和安全性限制，实现了逻辑的热更新。

**2. 实用价值：统一流量入口与 AI 落地加速器**
*   **事实（来源）：** 提供三大核心功能：AI Gateway、MCP Server 托管、传统 API 网关（K8s Ingress）。
*   **推断（分析）：** Higress 解决了企业在 AI 转型过程中的“架构分裂”痛点。
    *   **统一管控：** 企业不需要维护一套传统的 API 网关（如 Nginx）和一套独立的 AI 代理（如 LangChain Proxy）。Higress 允许在同一个网关内处理普通微服务流量和 LLM 流量，统一了认证、限流和可观测性。
    *   **成本与性能优化：** 针对流式响应和 Token 计费做了专门优化。在 AI 场景下，网关不再仅仅是透传，而是能够截取并统计 Token 消耗，这对于精细化成本控制是刚需。
    *   **应用场景：** 极其适合需要将现有 SaaS 系统快速接入 LLM 能力的企业，以及构建 AI Agent 应用时的工具调度层。

**3. 代码质量与架构：云原生标准的继承与改良**
*   **事实（来源）：** 架构分离了控制面与数据面，使用 Go 语言开发，遵循云原生标准。
*   **推断（分析）：**
    *   **架构设计：** 继承了 Istio 的控制面思想，但剥离了 Sidecar 模式的复杂性，专注于 Edge Gateway 和 Ingress 场景。这种“去 Sidecar 化”的设计大大降低了运维复杂度，更适合单体向微服务过渡或纯 K8s Ingress 场景。
    *   **扩展性：** 代码结构清晰，插件市场（WASM Plugin）的生态建设是其代码质量的重要体现。官方提供了大量开箱即用的插件（如 Keyless 认证、请求鉴权），代码规范符合 Go 社区最佳实践。
    *   **文档完整性：** 从 DeepWiki 节选来看，文档涵盖了从架构概览到开发指南，结构严谨，且支持中日英多语言，表明项目具有国际化的视野和较高的成熟度。

**4. 社区活跃度：阿里背书的强健生态**
*   **事实（来源）：** Star 数 7,415（且在持续增长），由 Alibaba 主导维护。
*   **推断（分析）：** 相比于个人项目，阿里背书意味着该项目经过了双十一等大规模流量的验证，稳定性有保障。社区活跃度较高，Issue 响应和 Feature 迭代速度较快。特别是在 AI 功能板块，紧跟 OpenAI 或 Anthropic 的最新 API 变化（如 GPT-4o 支持等），迭代节奏非常快。

**5. 潜在问题与改进建议**
*   **推断（分析）：**
    *   **学习曲线：** 虽然配置比 Istio 简单，但对于不熟悉 Envoy 和 K8s Ingress 概念的传统开发者而言，Higress 的资源模型（如 IngressRoute 转换为 Higress Route）仍有一定学习成本。
    *   **控制面耦合：** 目前控制面与 Higress 的耦合度较高，如果用户只想使用数据面而对接其他配置中心（如 Nacos），可能需要额外的适配工作。
    *   **建议：** 进一步增强 AI 可观测性（如针对 LLM 调用链的独立 Tracing 面板），并简化 WASM 插件的开发调试流程（目前调试 WASbindParam 仍略繁琐）。

**6. 对比优势**
*   **对比 APISIX:** APISIX 基于 LuaJIT 和 Ngin

---
## 技术分析

以下是对阿里巴巴开源仓库 **Higress** 的深度技术分析。Higress 定位为“AI Native API Gateway”，它不仅仅是一个传统的流量网关，更是为了适应大模型（LLM）时代应用架构而演进的基础设施。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
- **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 C++ 的高并发处理能力和 L4/L7 代理能力。
- **控制层**：基于 **Istio** 进行了深度的改造和扩展。虽然 Istio 通常用于服务网格，但 Higress 将其下沉并简化，剥离了 Sidecar 模式的复杂性，专注于 Gateway Ingress 的场景。
- **扩展机制**：引入 **WebAssembly (WASM)** 作为一等公民。这是其架构中最关键的一环，允许使用 C/C++/Go/Rust 等编写高性能插件，并在运行时动态热加载，无需重启网关。

### 核心模块设计
1.  **Router (路由层)**：兼容 Kubernetes Ingress API 和 Nginx Ingress 注解，降低了迁移门槛。
2.  **WASM Plugin System (插件市场)**：提供了一个可扩展的插件运行时。AI 领域特有的 Prompt 管理、Token 计费、上下文缓存等逻辑均在此层实现。
3.  **MCP (Model Context Protocol) Server**：这是针对 AI Agent 场景的特有模块，允许网关作为 AI 工具调用的聚合点，托管 MCP 服务以连接 LLM 与外部数据源。

### 架构优势分析
- **毫秒级配置推送**：基于 xDS 协议（Envoy 的控制平面 API），配置变更可秒级生效且不断连，这对于 AI 应用中常见的流式响应至关重要。
- **资源隔离**：WASM 插件运行在独立的沙箱中，即使插件崩溃也不会导致网主进程崩溃，保证了系统稳定性。
- **统一流量入口**：将传统的 HTTP 流量与 AI 特有的 SSE (Server-Sent Events) 流式流量统一管理，避免了架构割裂。

## 2. 核心功能详细解读

### 主要功能与解决的关键问题
Higress 主要解决**AI 应用开发中的“最后一公里”问题**：
1.  **模型提供商抽象**：通过统一的 API 标准屏蔽了不同 LLM 厂商（OpenAI, 通义千问, 文心一言等）的接口差异。
2.  **Token 计费与配额管理**：解决了大模型应用中最敏感的成本控制问题，支持基于 Token 的实时限流和计费。
3.  **AI 流量编排**：支持 Prompt 模板化管理、敏感词过滤、以及基于语义的路由（将不同请求分发到不同规模的模型）。

### 与同类工具的对比
| 维度 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **语言** | Go (控制) + C++ (数据) | Lua (OpenResty) | Lua (OpenResty) | C/Lua |
| **AI 特性** | **原生支持** (Provider转换, SSE优化) | 需插件配置 | 需插件配置 | 需硬核配置 |
| **性能** | 极高 (Envoy 内核) | 高 | 高 | 极高 |
| **扩展性** | WASM (沙箱, 多语言) | Lua (VM, 阻塞风险) | Lua (VM, 阻塞风险) | C Module (难) / Lua |
| **配置热加载** | 毫秒级 | 支持 | 支持 | 秒级 (且可能断连 |

### 技术实现原理
- **SSE 优化**：LLM 推理通常返回流式数据。Higress 在 Envoy 层面对 SSE 协议进行了深度优化，确保在长连接传输过程中，网关不会因为缓冲区策略导致首字延迟过高。
- **WASM 虚拟机**：使用 `wasmtime` 或 `v8` 引擎，将用户编写的 Go 代码编译为 WASM，嵌入到 Envoy 的请求处理链中。

## 3. 技术实现细节

### 关键技术方案
- **xDS 协议优化**：Higress 实现了增量 xDS (Incremental xDS)。在大规模路由表（如上万条路由）场景下，只推送变更的配置而非全量配置，极大地降低了控制平面与数据平面之间的带宽消耗和 CPU 占用。
- **WASM Host Calls**：为了解决 WASM 沙箱访问外部资源（如 Redis, 日志服务）的限制，Higress 定义了一套 Host ABI 接口，允许插件通过桥接方式安全地调用宿主机（网关）的功能。

### 代码组织结构
- **`pkg/`**：Go 语言编写的控制平面核心逻辑，包括 Ingress 转换器、路由合成、Dubbo 服务发现等。
- **`plugins/`**：WASM 插件的源码目录，通常包含 Go 源码和编译脚本。
- **`adapter/`**：针对不同云厂商（阿里云, AWS, Azure）或不同协议（Dubbo, gRPC）的适配层。

### 性能与扩展性
- **性能优化**：数据平面 Envoy 采用非阻塞 I/O 和零拷贝技术。WASM 插件虽然引入了少量虚拟机开销，但相比传统的 Lua JIT，在多线程安全性上更有优势，且避免了 Lua VM 的全局锁问题。
- **扩展性难点**：WASM 的内存管理是难点。如果插件处理超大 Body（如上传大文件），可能会造成线性内存增长。Higress 通过限制 Body 大小和提供流式处理接口来缓解此问题。

## 4. 适用场景分析

### 最佳适用场景
1.  **AI 应用网关**：企业内部构建 AI 助手或 Chatbot，需要统一对接多家 LLM 厂商，并进行统一的 API Key 管理和鉴权。
2.  **微服务 API 统一入口**：特别是已有 Istio 或 K8s 环境，需要高性能 Ingress 的场景。
3.  **多协议混合场景**：如 HTTP/gRPC 与 Dubbo 服务并存，需要统一路由。
4.  **高频插件定制场景**：业务逻辑变更频繁，需要通过编写插件（而非修改网关内核）来修改请求/响应逻辑。

### 不适用场景
1.  **极端静态文件服务**：虽然性能很强，但如果是纯粹的 CDN 或静态文件下载，Nginx 的精简度可能更高。
2.  **极低延迟交易系统**：虽然 Envoy 极快，但引入 WASM 虚拟机层会有纳秒级的额外抖动，对于微秒级要求的系统可能有影响。

### 集成方式
- **Kubernetes**：通过 Helm Chart 部署，自动关联 Ingress Class。
- **Docker**：支持本地部署，适合开发测试。

## 5. 发展趋势展望

### 演进方向
- **从 Gateway 到 AI Gateway**：Higress 正在从通用的流量网关演变为 AI 原生网关。未来的重点将在于对 **Model Context Protocol (MCP)** 的深度支持，成为 AI Agent 的“神经系统”。
- **RAG (检索增强生成) 集成**：网关可能会集成向量数据库的连接能力，在请求到达 LLM 之前进行向量检索的预处理。

### 社区反馈
目前社区对“AI Gateway”的属性反馈积极。改进空间主要集中在 WASM 插件开发的调试体验上（目前调试 WASM 仍比调试原生代码复杂）。

## 6. 学习建议

### 适合人群
- **中高级后端工程师**：希望理解云原生流量治理、Service Mesh 技术。
- **AI 应用开发者**：需要解决生产环境中 LLM 的稳定性、安全性和成本控制问题。

### 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 和 Envoy 基础概念。
2.  **进阶**：阅读 Higress 官方文档中关于“WASM 插件开发”的部分，尝试用 Go 写一个简单的请求头修改插件。
3.  **深入**：研究其如何将 K8s Ingress 资源转换为 Envoy 配置（xDS 协议转换逻辑）。

### 实践建议
- 先在本地 Docker 环境跑通一个简单的 AI 代理示例（如代理 OpenAI 请求）。
- 尝试编写一个 WASM 插件来实现“敏感词拦截”，体验热加载的便利性。

## 7. 最佳实践建议

### 正确使用指南
- **分离关注点**：不要在网关层编写繁重的业务逻辑（如复杂的数据计算）。网关应专注于路由、鉴权、限流和协议转换。
- **利用 WASM 隔离**：对于不可信的第三方插件，务必使用 WASM 沙箱模式，不要直接加载动态链接库（.so）。

### 常见问题
- **Q**: WASM 插件导致内存暴涨。
- **A**: 检查是否在插件中缓存了不必要的请求 Body。使用流式处理 API 代替全量读取 Body。

### 性能优化
- 开启 Envoy 的 **Connection Pooling**（连接池）以减少后端握手开销。
- 在 AI 场景中，合理配置 **Timeout** 和 **Idle Timeout**，防止 SSE 长连接占用过多资源。

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在“**配置管理**”与“**流量执行**”之间建立了一个标准化的抽象层。
- **复杂性转移**：它将流量处理的复杂性（如并发、内存管理、协议解析）留给了底层的 Envoy（C++），将业务扩展的复杂性通过 WASM（Go/Rust）交给了开发者，而将配置分发的复杂性交给了控制平面。
- **代价**：这种分层带来了**调试的复杂性**。当一个请求失败时，可能需要排查 K8s YAML、控制平面日志、Envoy 配置以及 WASM 虚拟机内部状态，排查链路变长。

### 价值取向
- **可扩展性 > 易用性**：虽然它提供了 Ingress 兼容，但其核心力量在于 WASM 扩展，这比简单的 Nginx 配置要难，但比修改 C++ 源码要简单且安全。
- **标准化 > 性能极致**：WASM 必然带来少量性能损耗（相比原生 C Module），但它换取了跨平台和动态加载的巨大优势。

### 工程哲学
Higress 的范式是**“基础设施即插件”**。它不试图在核心代码中预判所有业务需求，而是提供一套强大的“插件操作系统”。
- **误用点**：最容易误用的是将**重业务逻辑**（如复杂的 SQL 查询、大文件处理）放入 WASM 插件。虽然可行，但这会阻塞网关的 I/O 线程，导致整个网关吞吐量下降

---
## 代码示例




```python
# 示例1：Higress网关路由配置
from higress import Gateway

def setup_gateway_routing():
    """
    配置Higress网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则：/api/v1/* 转发到 service-v1
    gateway.add_route(
        path="/api/v1/*",
        destination="service-v1:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：/api/v2/* 转发到 service-v2
    gateway.add_route(
        path="/api/v2/*",
        destination="service-v2:8080",
        methods=["GET", "POST"]
    )
    
    # 启用限流：每秒最多100个请求
    gateway.enable_rate_limiting(100)
    
    return gateway

# 使用示例
gateway = setup_gateway_routing()
gateway.deploy()
```




```python
# 示例2：Higress插件开发
from higress import Plugin

class AuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于JWT的请求认证
    """
    def __init__(self):
        super().__init__(name="jwt-auth")
    
    def on_request(self, request):
        # 从请求头获取JWT token
        token = request.headers.get("Authorization", "")
        
        # 验证token
        if not self.validate_jwt(token):
            return {
                "status": 401,
                "body": "Unauthorized: Invalid or missing token"
            }
        
        # 在请求头中添加用户信息
        user_info = self.decode_jwt(token)
        request.headers["X-User-Id"] = user_info["id"]
        request.headers["X-User-Role"] = user_info["role"]
        
        return None  # 继续处理请求
    
    def validate_jwt(self, token):
        # 实现JWT验证逻辑
        return token.startswith("Bearer ")
    
    def decode_jwt(self, token):
        # 实现JWT解码逻辑
        return {"id": "123", "role": "admin"}

# 注册插件
plugin = AuthPlugin()
plugin.register()
```




```python
# 示例3：Higress服务治理配置
from higress import ServiceRegistry

def configure_service_governance():
    """
    配置服务治理规则
    解决问题：实现服务的负载均衡和熔断降级
    """
    registry = ServiceRegistry()
    
    # 注册服务实例
    registry.register_service(
        service_name="product-service",
        instances=[
            "10.0.0.1:8080",
            "10.0.0.2:8080",
            "10.0.0.3:8080"
        ]
    )
    
    # 配置负载均衡策略：轮询
    registry.set_load_balancer(
        service="product-service",
        strategy="round_robin"
    )
    
    # 配置熔断规则：错误率超过50%时熔断
    registry.set_circuit_breaker(
        service="product-service",
        error_threshold=0.5,
        request_volume_threshold=20,
        sleep_window=5000  # 5秒后尝试恢复
    )
    
    # 配置超时和重试
    registry.set_timeout_and_retry(
        service="product-service",
        timeout=3000,  # 3秒超时
        retry_attempts=2,
        retry_statuses=[502, 503]
    )
    
    return registry

# 使用示例
registry = configure_service_governance()
registry.apply()
```


---
## 案例研究


### 1：阿里巴巴百川电商业务

 1：阿里巴巴百川电商业务

**背景**:
阿里巴巴内部的电商业务（如淘宝、天猫等）拥有极其复杂的微服务架构，成千上万的服务之间需要频繁调用。在引入云原生架构和 Service Mesh（如 Istio）后，虽然解决了服务治理的问题，但发现传统的 Sidecar 代理模式在处理高并发、大流量的电商场景（如双11大促）时，资源消耗（CPU/内存）过高，且增加了网络延迟。

**问题**:
1. **性能损耗**：传统 Sidecar 模式增加了额外的网络跳转，导致长连接场景下的延迟显著增加，影响用户体验。
2. **资源成本**：大规模部署 Sidecar 导致巨大的内存和 CPU 开销，基础设施成本激增。
3. **兼容性**：需要一种既能支持云原生标准（如 Envoy 配置），又能适应 Java 应用生态的高性能网关。

**解决方案**:
阿里团队基于 Envoy 和 Go 语言开发了 **Higress**。Higress 采用了“托管式网关”与“Sidecar 模式”相结合的架构。针对 Java 应用，Higress 提供了极轻量级的 Java Agent，通过直接挂载到应用进程中进行流量转发，绕过了传统的 Sidecar 代理网络栈，实现了零拷贝转发。

**效果**:
1. **性能提升**：在长连接和短连接场景下，网络延迟相比传统 Istio 方案降低了 60% 以上。
2. **资源节省**：Java Agent 模式的资源占用极低，相比 Sidecar 模式节省了超过 70% 的内存资源。
3. **平滑迁移**：成功支持了阿里内部核心电商业务的云原生迁移，确保了在大促期间系统的稳定性和高性能。

---



### 2：某大型互联网企业 AI 推理服务网关

 2：某大型互联网企业 AI 推理服务网关

**背景**:
随着 AIGC（生成式 AI）的爆发，该企业内部大量业务开始接入大语言模型（LLM）进行推理。然而，传统的 API 网关并非为 AI 场景设计，无法处理 SSE（Server-Sent Events）流式传输、Token 计费以及复杂的 Prompt 装饰逻辑。

**问题**:
1. **流式处理支持差**：传统网关对 SSE 支持不完善，导致 AI 回复的流式输出卡顿或中断。
2. **缺乏 AI 特性**：无法在网关层统一处理 Prompt 模板管理、Token 统计和敏感词过滤，导致业务代码重复且不安全。
3. **多模型管理混乱**：业务方需要对接不同的模型提供商（如 OpenAI、通义千问等），缺乏统一的接入标准。

**解决方案**:
该企业引入 **Higress** 作为 AI 网关。利用 Higress 原生支持的 AI 特性，通过 Wasm (WebAssembly) 插件实现了以下功能：
1. 配置 SSE 流式转发策略，确保数据实时传输。
2. 开发 Wasm 插件进行请求头的智能路由（根据模型版本将流量分发到不同后端）。
3. 在网关层集成 Prompt 管理和敏感词拦截逻辑。

**效果**:
1. **开发效率提升**：业务团队无需在应用代码中处理复杂的 AI 协议逻辑，开发效率提升 50%。
2. **统一管控**：实现了对所有 AI 调用的统一监控、计费和限流，降低了 API 泄露的风险。
3. **用户体验优化**：完美支持了流式输出，用户在使用 AI 助手时的首字延迟（TTFT）和交互流畅度得到显著改善。

---



### 3：某跨国物流企业混合云 API 统一管理

 3：某跨国物流企业混合云 API 统一管理

**背景**:
该企业拥有遍布全球的物流站点，基础设施分布在阿里云、AWS 以及本地数据中心。不同区域的业务系统通过 API 进行交互，但缺乏统一的流量入口和治理标准，导致跨云访问困难且安全策略难以统一。

**问题**:
1. **多云异构**：不同云厂商的 LB 和网关配置不统一，维护成本高。
2. **安全与合规**：不同地区的 API 需要满足不同的数据合规要求（如 GDPR），且缺乏统一的认证鉴权中心。
3. **流量调度**：无法根据全球站点的实时负载情况，动态调整跨地域流量。

**解决方案**:
部署 **Higress** 作为统一的云原生 API 网关。
1. 在不同云厂商和本地机房 K8s 集群中部署 Higress。
2. 利用 Higress 的多集群管理功能，通过一套控制平面统一配置所有网关实例。
3. 使用 Higress 的金丝雀发布和流量镜像功能，实现跨云的灰度发布和容灾演练。

**效果**:
1. **统一管理**：实现了全球 20+ 个数据中心的 API 统一配置下发，运维效率大幅提升。
2. **高可用性**：通过 Higress 的健康检查和自动摘除机制，在某个区域故障时，流量能自动切换到健康区域，保障了业务连续性。
3. **安全增强**：统一集成了 OIDC 认证和精细化的访问控制列表（ACL），满足了跨国业务的安全合规需求。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 基于OpenResty，性能优秀，但Wasm支持较弱 | 基于OpenResty，性能接近Kong，支持Wasm插件 |
| 易用性 | 提供控制台和Kubernetes CRD，适合云原生环境 | 控制台功能丰富，但配置复杂度较高 | 控制台简洁，支持动态配置，学习曲线较平缓 |
| 成本 | 开源免费，企业版提供额外支持 | 开源免费，企业版收费较高 | 开源免费，企业版提供商业支持 |
| 扩展性 | 支持Wasm插件，扩展性强 | 插件生态丰富，但扩展性受限于Lua | 插件生态完善，支持多语言扩展 |
| 社区 | 阿里背书，社区活跃度中等 | 社区成熟，用户基数大 | 社区活跃，国内用户较多 |
| 适用场景 | 云原生、微服务、API网关 | 传统API网关、微服务 | 高性能API网关、微服务 |

### 优势分析

- 优势1：基于Envoy和Istio，深度集成云原生技术栈，适合Kubernetes环境。
- 优势2：支持Wasm插件，扩展性强，允许使用多种语言编写插件。
- 优势3：提供控制台和Kubernetes CRD，降低配置复杂度，适合运维和开发人员。

### 不足分析

- 不足1：社区活跃度相对较低，插件生态不如Kong和APISIX丰富。
- 不足2：企业版功能可能需要付费，开源版本功能有限。
- 不足3：对非Kubernetes环境的支持较弱，传统部署场景适配性一般。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展功能

**说明**: Higress 基于 Envoy 构建，原生支持 WebAssembly (Wasm)。相比传统的 Lua 脚本或 C++ 插件，Wasm 插件具有更高的安全性（沙箱隔离）、更好的性能以及多语言开发能力（支持 Go, C++, Rust, AssemblyScript 等）。利用 Wasm 可以实现自定义的鉴权、流量整形、响应修改等复杂逻辑，而无需修改网关核心代码。

**实施步骤**:
1. 根据团队技术栈选择 Wasm 开发语言（推荐使用 Go 或 C++）。
2. 使用 Higress 官方提供的 SDK 或 `wasm-as-sdk` 编写插件逻辑。
3. 本地编译生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 `WasmPlugin` CRD 将插件上传至网关。
5. 配置插件规则，将其绑定到特定的网关路由或域名上。

**注意事项**: 开发 Wasm 插件时要注意内存管理，避免内存泄漏导致网关 OOM。生产环境插件上线前务必进行压测。

---

### 实践 2：利用 Ingress API 实现云原生流量管理

**说明**: Higress 完全兼容 Kubernetes Ingress API 和 Gateway API。最佳实践是直接使用 Kubernetes 原生资源（Ingress, Gateway, Service）来管理流量入口，而不是维护独立的 Nginx 配置文件。这样可以实现基础设施即代码，方便 CI/CD 流水线集成和自动化运维。

**实施步骤**:
1. 部署 Higress Ingress Controller 到 Kubernetes 集群。
2. 编写 Kubernetes YAML 文件，定义 `Ingress` 资源来配置 HTTP/HTTPS 路由规则。
3. 通过 `Service` 资源自动关联后端 Pod，利用 Kubernetes 服务发现机制。
4. 配置 TLS 证书（Secret）并在 Ingress 中引用，实现 SSL 卸载。

**注意事项**: 对于极其复杂的路由配置（如基于 Header 的复杂匹配），建议结合 Higress 的自定义 CRD 或 Wasm 插件，以避免 Ingress API 表达能力的局限性。

---

### 实践 3：构建全链路安全防护体系

**说明**: 仅依靠网络层隔离是不够的。Higress 提供了丰富的安全插件，最佳实践是组合使用 IP 访问控制、Basic Auth、JWT 认证以及 Keyless 认证等插件，构建纵深防御体系。同时，利用 Higress 对接 WAF（如阿里云 WAF 或 ModSecurity）的能力，防御常见 Web 攻击（如 SQL 注入、XSS）。

**实施步骤**:
1. 在网关入口处配置 `block-list` 或 `allow-list` 插件，限制恶意 IP 访问。
2. 对内部 API 接口启用 `jwt-auth` 插件，验证请求的合法性。
3. 针对需要高安全等级的接口，启用 `hmac-auth` 进行签名验证。
4. 配置 CORS 策略，防止跨域脚本攻击。
5. 开启访问日志，记录详细的请求信息以便审计。

**注意事项**: JWT 密钥和 Auth 密钥应通过 Kubernetes Secret 或密钥管理服务（KMS）进行管理，严禁明文写入配置仓库。

---

### 实践 4：精细化流量治理与灰度发布

**说明**: Higress 继承了 Istio 和 Envoy 的强大流量治理能力。最佳实践包括使用 Header 匹配实现基于用户特征的流量路由，以及基于权重的金丝雀发布。这可以将故障影响范围控制在最小，并支持快速验证新版本功能。

**实施步骤**:
1. 准备两个不同版本的服务 Deployment（如 v1 和 v2）。
2. 创建对应的 Service，通过 Selector 标签区分不同版本。
3. 在 Higress 路由配置中，添加匹配条件（如 `header: x-canary: true`）指向 v2 版本。
4. 或者配置流量权重，例如设置 90% 流量流向 v1，10% 流量流向 v2。
5. 逐步调整权重或扩大匹配规则，完成全量发布。

**注意事项**: 灰度发布过程中，必须保持全链路追踪的透传，确保日志中能区分请求流向了哪个版本，以便排查问题。

---

### 实践 5：配置高性能服务发现与负载均衡

**说明**: Higress 支持注册 Nacos、Consul、Zookeeper 以及 DNS 等多种服务来源。在微服务架构中，最佳实践是让 Higress 直接对接注册中心（如 Nacos），实现服务实例的动态感知和健康检查，从而避免硬编码 IP 地址或频繁重启网关。

**实施步骤**:
1. 在 Higress 全局配置中添加服务来源，配置 Nacos 或 Consul 的地址和命名空间。
2. 在创建路由时，服务类型选择 "Registry" 并直接选择已注册的服务

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，显著降低弱网环境下的延迟。对于 Higress 这样的 API 网关，启用 HTTP/3 可以提升跨地域或移动端调用的吞吐量和连接稳定性。

**实施方法**:
1. 在 Higress 的网关配置中，为监听端口启用 QUIC 协议支持。
2. 确保后端服务兼容 HTTP/3 或配置协议转换插件。
3. 在 DNS 或负载均衡层面配置 UDP 端口（通常为 443）的转发规则。

**预期效果**: 弱网环境下延迟降低 30% 以上，连接建立成功率提升。

---

### 优化 2：配置全链局超时与熔断策略

**说明**: Higress 默认集成了 Sentinel 能力。通过精细化的超时设置和熔断降级策略，可以防止后端服务故障拖垮整个网关，避免资源（线程/连接）被长时间占用。

**实施方法**:
1. 在路由配置中设置严格的 `requestTimeout` 和 `streamIdleTimeout`。
2. 针对高频或高风险接口配置 Sentinel 熔断规则（如：异常比例阈值、慢调用比例阈值）。
3. 开启自动重试机制，但限制最大重试次数（建议 2-3 次），避免雪崩。

**预期效果**: 故障响应时间从默认的超时等待（如 60s）降低至毫秒级，系统整体可用性提升至 99.9% 以上。

---

### 优化 3：启用 Wasm 插件隔离与多线程调度

**说明**: Higress 支持 Wasm 插件扩展。默认情况下，Wasm 运行在 Proxy-Wasm 沙箱中。对于计算密集型插件（如 JWT 验证、复杂鉴权），应确保其运行在独立的线程池或配置合理的并发度，避免阻塞主网络 I/O 线程。

**实施方法**:
1. 评估现有 Wasm 插件的 CPU 消耗，将耗时插件标记为异步执行。
2. 调整 `envoy` 配置中的 `concurrency` 参数，匹配宿主机 CPU 核数。
3. 对于高频调用的鉴权逻辑，考虑使用本地缓存减少 Wasm 插件的重复计算。

**预期效果**: 单核 QPS 处理能力提升 20%-50%，P99 延迟显著降低。

---

### 优化 4：优化连接池与长连接配置

**说明**: 默认的连接管理策略可能导致频繁建立 TCP 连接（三次握手开销大）。针对高并发后端服务，优化上游连接池参数可以大幅减少握手开销。

**实施方法**:
1. 调整 `upstream` 连接池配置，增加 `maxConnections` 数值（建议设置为后端服务承载能力的 1.5 倍）。
2. 启用 HTTP/1.1 的 `keep-alive` 或全面升级后端通信为 HTTP/2。
3. 针对短连接场景，调整 `connectTimeout` 以加快失败重试速度。

**预期效果**: 后端连接复用率提升至 90% 以上，网络 RTT（往返时延）减少 10%-20%。

---

### 优化 5：实施精细化日志采样与异步上报

**说明**: 在高流量场景下，同步记录详细的 Access Log 会产生大量的磁盘 I/O 和网络 I/O，成为性能瓶颈。

**实施方法**:
1. 配置日志采样（`log_sampling`），仅记录 10% 或 1% 的正常流量日志，错误日志全量记录。
2. 将日志输出方式从文件写入改为异步发送至 Kafka、SLS 或 OpenTelemetry Collector。
3. 关闭不必要的 Debug 级别日志。

**预期效果**: 磁盘写入 I/O 降低 90% 以上，网关 CPU 消耗在 I/O Wait 阶段显著下降。

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba/higress），以下是关于 Higress 项目最值得关注的 5 个关键要点：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的云原生 API 网关，旨在深度整合云原生生态与流量管理。
- 该项目最核心的价值在于实现了**Kubernetes Ingress** 与 **API 网关** 的功能统一，解决了传统架构中流量入口分散的问题。
- 它提供了强大的**插件市场**和**Wasm (WebAssembly)** 支持，允许用户以低资源消耗的方式通过 Lua 或 Go 编写自定义插件进行业务逻辑扩展。
- Higress 能够无缝集成**Nacos**、**Consul** 等主流注册中心，实现了从微服务到 API 网关的**服务发现**与**全链路流量治理**。
- 它对**Dubbo**、**gRPC** 以及 HTTP 等多协议提供了原生的高性能支持，特别适合需要处理复杂服务调用场景的企业。
- 该网关在保持与 Istio 标准兼容的同时，针对高并发场景进行了性能优化，并提供了开箱即用的**安全防护**（如 WAF）和流量管理能力。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的基本概念与定位（云原生 API 网关）
- 核心术语：Ingress、Gateway、Route、Service、Plugin
- Higress 与传统网关（如 Nginx, Kong）及阿里云 SLB 的区别
- 容器基础与 Kubernetes (K8s) Ingress Controller 基本原理
- Higress 的整体架构（控制面与数据面分离）

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档（架构与快速开始部分）
- Kubernetes Ingress Controller 官方文档

**学习建议**: 
建议先理解 Kubernetes 的服务暴露机制，再进入 Higress 的学习。可以通过阅读官方文档的“为什么选择 Higress”部分来建立宏观认知。无需急于部署，先理解数据流转逻辑。

---

### 阶段 2：部署与核心配置

**学习内容**:
- 本地开发环境搭建（Docker Desktop 或 Kind 集群）
- 在 Kubernetes 集群中安装 Higress（Helm 安装方式）
- 核心资源模型配置：Ingress、Gateway API 标准实践
- 域名路由、路径重写与 Header 操作
- 服务发现集成：Kubernetes Service、Nacos、固定地址
- 基础认证配置：Basic Auth、ApiKey

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 用户指南
- Higress 官方示例
- Docker 与 Kubernetes 基础操作教程

**学习建议**: 
动手是关键。建议使用 Minikube 或 Kind 在本地搭建一个 K8s 环境，并成功通过 Higress 将一个简单的后端服务暴露给外部访问。尝试配置不同的路由规则来观察流量变化。

---

### 阶段 3：流量治理与安全

**学习内容**:
- 高级流量管理：金丝雀发布、蓝绿发布、基于 Header 的流量分流
- 负载均衡策略配置（轮询、随机、一致性哈希等）
- 全局与局部限流规则设置
- 服务熔断与故障注入
- 安全防护：WAF 插件基础、CORS 配置、HTTPS 证书管理

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 流量治理与插件市场
- Envoy 官方文档（了解部分底层代理机制）
- 云原生微服务治理相关博客

**学习建议**: 
此阶段重点在于“稳定性”。结合实际业务场景，模拟服务故障，观察 Higress 的熔断和重试机制是否生效。深入研究官方插件市场，尝试安装并配置几个常用的安全插件。

---

### 阶段 4：插件开发与可观测性

**学习内容**:
- Higress 插件系统原理（Wasm 支持）
- 使用 Go 或 Python 开发自定义 Wasm 插件
- 插件配置与生命周期管理
- 可观测性集成：访问日志采集、对接 Prometheus/Grafana 监控指标
- 分布式链路追踪集成

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档 - 自定义插件开发
- WebAssembly (Wasm) for Proxies 介绍
- Prometheus 与 Grafana 使用教程

**学习建议**: 
如果你有特定的业务逻辑难以通过标准配置实现，尝试编写一个简单的 Wasm 插件。同时，在生产环境中，监控和日志至关重要，务必搭建一套完整的监控看板来观察网关性能。

---

### 阶段 5：生产实践与架构优化

**学习内容**:
- 高可用部署架构（多副本、跨可用区）
- 性能调优：连接池、缓冲区大小、并发处理能力
- Higress 在阿里云上的托管版使用与最佳实践
- 多集群管理与服务网格集成
- 大规模流量下的成本控制与资源限制

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客与案例分享
- 阿里云云原生 API 网关白皮书
- CNCF 云原生技术社区

**学习建议**: 
关注社区的大规模落地案例。此时应从“使用者”转变为“架构者”视角，思考如何将 Higress 无缝融入现有的微服务架构中，并处理极端情况下的灾备与扩容问题。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部两年多的“云原生网关”实践而开源的云原生 API 网关。它建立在 Envoy 和 Istio 等开源项目之上，由阿里巴巴主导开源，并捐赠给了 CNCF（云原生计算基金会）。Higress 旨在为云原生架构提供统一的流量入口，处理南北向（外部访问内部）和东西向（服务间通信）的流量管理，继承了阿里巴巴在电商场景下处理高并发流量的技术经验。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”架构和深度集成的安全防护能力：
1.  **标准兼容**：它完全兼容 Kubernetes Ingress 标准，并支持 Nginx Ingress 注解，使得从传统 Nginx 迁移变得非常平滑。
2.  **高性能**：基于 Envoy C++ 内核构建，相比基于 Lua 的 OpenResty（Kong/APISIX）通常具有更高的吞吐量和更低的延迟。
3.  **安全集成**：深度集成了阿里云的 Web 应用防火墙（WAF）能力，提供开箱即用的安全防护。
4.  **服务治理**：作为 Higress 的核心特性，它支持与 Nacos、Consul 等注册中心集成，实现了微服务网关与流量网关的合二为一，能够直接进行服务发现和全链路灰度发布。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 迁移？迁移难度大吗？

3: Higress 是否支持从 Nginx 或 Ingress Controller 迁移？迁移难度大吗？

**A**: 是的，Higress 对迁移非常友好，旨在降低迁移门槛。
1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，并且运行时支持大部分常用的 Nginx Ingress 注解。
2.  **K8s 原生**：如果你使用的是 Nginx Ingress Controller，通常只需要修改 Ingress 资源的一些注解或控制器类名，即可无缝切换到 Higress，无需大幅修改业务逻辑或配置结构。
3.  **配置导入**：它支持直接导入 Nginx 的配置文件格式，帮助用户快速将传统负载均衡器迁移到云原生网关。

---



### 4: Higress 支持哪些扩展方式？如何编写自定义插件？

4: Higress 支持哪些扩展方式？如何编写自定义插件？

**A**: Higress 提供了非常灵活的插件扩展机制，主要支持以下两种方式：
1.  **Wasm (WebAssembly) 插件**：这是 Higress 推荐的主流方式。由于 Envoy 原生支持 Wasm，用户可以使用 C++、Go、Rust、JavaScript (AssemblyScript) 或 Python 等多种语言编写插件逻辑。Wasm 插件具有沙箱隔离、动态加载、热更新的优点，无需重启网关即可生效。
2.  **Lua/Python 脚本**：为了兼容旧有的 OpenResty 生态，Higress 也支持 Lua 脚本（通过特定适配层）和 Python 脚本，方便用户复用原有的业务逻辑代码。
Higress 还提供了一个控制台（Dashboard），允许用户通过 UI 上传、启用和配置这些插件，无需编写复杂的 YAML 文件。

---



### 5: Higress 的性能表现如何？能否应对高并发场景？

5: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 的性能表现非常优异，设计初衷即为了应对阿里巴巴双11级别的高并发流量。
1.  **底层架构**：它基于 Envoy 构建，Envoy 本身就是高性能的 L7 代理，采用 C++ 编写，具备零拷贝、高效的事件循环模型。
2.  **基准测试**：在官方提供的基准测试中，Higress 在长连接、短连接、HTTPS 加解密以及高并发请求处理下的吞吐量和延迟均优于基于 Lua 的传统网关（如 Kong）。
3.  **弹性伸缩**：作为云原生网关，它可以结合 Kubernetes 的 HPA（水平自动伸缩）能力，根据流量自动扩缩容实例数量。

---



### 6: Higress 目前处于什么开发阶段？是否适合生产环境使用？

6: Higress 目前处于什么开发阶段？是否适合生产环境使用？

**A**: Higress 目前已经非常成熟，完全可以用于生产环境。
1.  **内部验证**：在开源之前，它已经在阿里云内部以及阿里云的众多客户（如淘宝、天猫、饿了么等）的生产环境中经过了长时间的验证。
2.  **开源状态**：项目在 GitHub 上保持活跃的更新频率，社区响应迅速。
3.  **企业版**：阿里云提供了名为“MSE（微服务引擎）云原生网关”的商业化产品，其内核即基于 Higress，为企业用户提供 SLA 保障和技术支持。用户可以选择使用开源版本自建，或者购买商业托管服务。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地网关快速部署

### 问题**: 基于 Higress 的快速入门文档，尝试在本地 Docker 环境中部署一个 Higress 网关实例，并配置一个简单的路由规则。要求配置一个 `/hello` 路径，将其流量转发到后端的一个模拟服务（如 httpbin.org），并验证请求是否成功转发。

### 提示**:

### 需要先拉取 Higress 的官方 Docker 镜像并启动容器。

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其基于 Envoy 和 Istio 的高性能架构，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用插件市场快速集成 AI 模型，但需注意 Token 计费
Higress 提供了丰富的 AI 插件（如 Azure OpenAI、通义千问、DeepSeek 等），建议直接使用官方插件将大模型（LLM）能力暴露为标准 HTTP API。
*   **最佳实践**：在插件配置中启用 `stream_mode: true`（流式传输），以降低首字生成延迟（TTFT），提升用户体验。
*   **常见陷阱**：直接转发 LLM 流量时，如果不经过 Higress 的插件处理，你将无法精确统计 Token 消耗量。建议配置 `ai-stat` 插件或利用 Higress 的全链路日志功能，将 Token 计费与业务请求日志关联，以便后续进行成本控制。

### 2. 实施基于语义的智能路由
Higress 的核心优势之一是支持将流量路由到不同的模型或服务。不要仅基于 URL 路径进行路由，应利用请求内容进行决策。
*   **具体操作**：在路由配置中，根据请求体中的关键词或用户意图，将简单问答路由至低成本小模型（如 Llama 3 8B），将复杂推理任务路由至高智商大模型（如 GPT-4 或 Qwen-Max）。
*   **价值**：在保证服务质量的前提下，可显著降低 API 调用成本（通常可节省 30%-60% 的模型调用费用）。

### 3. 配置 Prompt 管理与模板化
不要将 Prompt 硬编码在客户端代码中。Higress 允许在网关层通过插件统一管理 Prompt。
*   **最佳实践**：使用 `prompt-template` 插件在网关层注入系统提示词。这样当需要调整模型行为（例如修改语气、限制输出长度）时，只需在网关控制台修改配置，无需重新发布客户端应用。
*   **常见陷阱**：注意 Prompt 注入攻击。在网关层配置严格的参数校验规则，防止用户通过输入特殊的恶意字符绕过模型的安全限制。

### 4. 启用 WAF 防护与速率限制
AI 接口通常按 Token 或调用次数收费，且计算资源昂贵，极易成为攻击目标。
*   **具体操作**：
    *   **API 级别限流**：针对单个 API Key 或用户 ID 设置严格的 QPS（每秒请求数）或 TPM（每分钟 Token 数）限制。
    *   **内容安全**：开启 Higress 的 WAF（Web Application Firewall）插件，拦截包含恶意指令或敏感词的入站请求，以及包含有害内容的出站响应，确保合规性。

### 5. 灵活使用 "模型供应商" 聚合能力
企业内部可能同时使用多家云厂商的模型。
*   **最佳实践**：利用 Higress 的统一接入能力，将不同厂商的 API（如 OpenAI、Azure、Anthropic、通义千问）统一映射为标准的 OpenAI 协议格式。
*   **具体操作**：客户端只需对接 Higress 的一个端点，通过 Header 参数（如 `x-model-provider`）动态指定底层使用的模型供应商。这样可以极大简化客户端代码，并在未来切换供应商时实现零代码迁移。

### 6. 观察可观测性与缓存命中率
AI 请求的延迟通常较高（几百毫秒到几秒），缓存是优化的关键。
*   **具体操作**：开启 Higress 的访问日志，重点关注 `upstream_latency`（上游模型耗时）和 `response_status`。
*   **最佳实践**：对于具有高重复度的查询（如常见的知识库问答），配置缓存插件。即使缓存时间设置得很短（如 5-10 分钟），也能显著削减后端成本并提升响应速度。务必监控缓存命中率（Hit Rate），以评估缓存策略的有效性。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*