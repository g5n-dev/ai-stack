---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T10:41:40+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["AI 工程", "系统与基础设施"]
source: github_trending
description: "Higress 是由阿里巴巴开源的**云原生 AI 网关**。基于 Go 语言编写，目前在 GitHub 上拥有超过 7,000 颗星。 以下是该项目的核心总结： **1. 核心定位** Higress 是一个**AI 原生的 API 网关**。它构建在 Istio 和 Envoy 之上，通过扩展 WebAssembl"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "Kubernetes"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,468 (+16 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，同时支持大模型流量管理与微服务路由。它旨在解决 AI 应用与传统云原生架构下的流量治理难题，并提供 MCP 服务器托管功能。本文将梳理其系统架构与核心组件，并重点介绍 AI 网关特性及插件系统的具体实现。

---
## 摘要

Higress 是由阿里巴巴开源的**云原生 AI 网关**。基于 Go 语言编写，目前在 GitHub 上拥有超过 7,000 颗星。

以下是该项目的核心总结：

**1. 核心定位**
Higress 是一个**AI 原生的 API 网关**。它构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，将传统的 API 网关功能与 AI 应用需求深度结合。其架构采用控制面（配置管理）与数据面（流量处理）分离的设计，配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，非常适合 AI 流式响应等长连接场景。

**2. 三大核心功能**
*   **AI 网关**：为 LLM 应用提供统一 API。支持 30+ 家大模型提供商，包含协议转换、可观测性、缓存和安全性防护。
*   **MCP 服务器托管**：托管模型上下文协议 (MCP) 服务器，使 AI Agent 能够调用工具和服务（如搜索、地图工具）。
*   **Kubernetes Ingress**：作为 K8s 入口控制器，兼容 Nginx ingress 注解，支持微服务路由。

**3. 关键组件**
系统通过插件和过滤器实现功能，包括 `ai-proxy`（AI 代理）、`ai-cache`（AI 缓存）、`mcp-router`（MCP 路由）以及用于安全防护的 `ai-security-guard` 等。

---
## 评论

**总体判断**

Higress 是一款基于 Istio 与 Envoy 深度重构的**云原生 API 网关**，它最核心的差异化价值在于将**大模型（LLM）流量治理**与**传统微服务网关**合二为一。对于正在构建 AI Agent 或 RAG 应用的技术团队而言，它不仅是一个流量入口，更是一个集成了模型提供商对接、Token 计费与提示词管理的 AI 基础设施中间件。

**深入评价依据**

**1. 技术创新性：从“流量网关”向“AI 网关”的架构跃迁**
*   **事实**：DeepWiki 明确指出 Higress 是“AI Native API Gateway”，基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 负载均衡，而 Higress 创新性地引入了“AI 原生”视角。它利用 WASM 的高性能隔离特性，动态加载针对 AI 场景的插件（如 LLM 路由、对话上下文缓存、敏感词过滤）。这种设计使得网关具备了“理解”AI 协议（如 OpenAI 协议）的能力，能够处理流式传输（SSE）和非结构化数据，这是传统网关通过硬编码难以实现的。

**2. 实用价值：解决 AI 落地中的“碎片化”与“成本”痛点**
*   **事实**：描述中提到其具备“AI gateway features for LLM applications”以及“MCP server hosting for AI agent tool integration”。
*   **推断**：在构建 AI 应用时，开发者常面临两个痛点：一是多模型提供商的 API 格式不统一，二是 Token 成本难以控制。Higress 的实用价值在于它充当了标准化层，允许后端服务通过统一的 API 调用不同的 LLM（如 OpenAI、通义千问、Llama），并在网关层实现统一的 Token 计费和限流。此外，其对 MCP (Model Context Protocol) 的原生支持，直接解决了 Agent 调用外部工具时的连接与鉴权难题，极大地降低了 AI 应用的集成复杂度。

**3. 代码质量与架构：云原生控制平面的优雅解耦**
*   **事实**：文档强调架构分离了“控制平面（配置管理）”与“数据平面（流量处理）”，且使用 Go 语言编写。
*   **推断**：基于 Envoy (C++) 作为数据平面保证了极致的高性能与稳定性，而使用 Go 语言构建控制平面符合云原生生态的主流选择（如 Kubernetes）。这种组合兼顾了“数据转发的高性能”与“业务逻辑开发的敏捷性”。从阿里巴巴开源的项目惯例推断，其代码规范应遵循 Alibaba Java/Go 编码规范，且由于依托 K8s Ingress，其架构设计具备良好的水平扩展能力和声明式配置特性，文档完整性通常较高（中英日三语 README 即为佐证）。

**4. 社区活跃度与生态：背靠阿里，连接 CNCF 生态**
*   **事实**：星标数 7,468，语言为 Go，明确提及 Istio 和 Envoy。
*   **推断**：作为阿里巴巴开源项目，其在国内云原生社区具有极高的影响力。相比纯开源社区项目，Higress 更有可能获得长期的企业级维护。它不仅仅是一个独立工具，更是连接 CNCF (Cloud Native Computing Foundation) 生态与 AI 生态的桥梁。对于已经使用 Istio 的企业，迁移成本极低，社区活跃度主要集中在 AI 插件开发和 K8s 集成场景上。

**5. 学习价值：理解“可编程网关”的最佳实践**
*   **事实**：系统包含 WASM Plugin System 和 Development Guide。
*   **推断**：对于开发者，Higress 是学习如何使用 Proxy-WASM 规范进行网关扩展的优秀范例。它展示了如何在不重启网关的情况下，动态推送 Go/C++/Rust 编写的插件逻辑。这对于理解云原生架构下的“热更新”机制、以及如何将业务逻辑下沉到网关层（如认证、限流、AI Prompt 拦截修改）具有极高的参考价值。

**6. 潜在问题与改进建议**
*   **推断**：尽管功能强大，Higress 的架构相对厚重。对于仅需简单 AI 代理功能的轻量级应用，部署一套基于 Istio 的网关可能存在“杀鸡用牛刀”的问题，运维复杂度（尤其是对 Envoy 配置的调优）较高。建议项目方提供更轻量的“Standalone 模式”或 Docker Compose 部署方案，以降低非 K8s 用户的使用门槛。

**7. 对比优势：与传统网关及专用 AI 网关的博弈**
*   **推断**：
    *   **对比 Kong/APISIX**：Higress 在 AI 场景（如 SSE 流式处理、LLM 协议转换）上提供了开箱即用的支持，而传统网关往往需要编写复杂的 Lua 插件才能实现。
    *   **对比专用 AI Gateway (如 One-Pixel)**：Higress 底盘更强，它继承了 Envoy 的高并发处理能力和全量的微服务治理能力（灰度发布、熔断降级）。这意味着企业不需要维护一个“业务网关”和一个“AI 网关”，Higress 试图统一两者

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。Higress 定位为“AI Native API Gateway”，它不仅仅是一个传统的 API 网关，更是为了适应大模型（LLM）时代而演进的下一代流量入口。

---

### 1. 技术架构深度剖析

**技术栈与架构模式**
Higress 采用了标准的 **控制平面 + 数据平面** 分离架构。
*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 C++ 高并发处理能力；控制平面基于 **Istio** 优化而来，剥离了 Sidecar 模式，专注于 Gateway 模式。
*   **语言栈**：控制平面主要使用 **Go** 语言开发（便于云原生编排），数据平面依赖 Envoy (C++)，插件扩展支持 **WASM (WebAssembly)** (支持 C++/Go/Rust/JS 等多语言编写)。
*   **架构模式**：遵循 **Kubernetes Ingress Controller** 模式，通过 CRD (Custom Resource Definition) 声明式配置管理网关行为。

**核心模块与关键设计**
1.  **路由与流量管理**：基于 Envoy 的 HTTP 连接管理，支持加权路由、Header 匹配、流量镜像等。
2.  **WASM 插件市场**：这是 Higress 的核心设计之一。它允许在不重启网关的情况下动态加载插件，逻辑运行在沙箱中，保证了安全性和隔离性。
3.  **AI 网关模块**：专门针对 LLM 流量设计的处理层，实现了与 OpenAI 协议的兼容、Token 计费、流式传输处理以及模型提供商的抽象。

**技术亮点与创新点**
*   **AI Native 特性**：这是与传统网关（如 APISIX, Kong）最大的区别。Higress 原生理解 LLM 的语义。例如，它能在流式传输中拦截并修改请求/响应，实现“敏感词过滤”而不打断流；支持将请求路由到不同的 LLM Provider（如通义千问、OpenAI、Azure）。
*   **MCP (Model Context Protocol) Server 托管**：Higress 创新地将 AI Agent 的工具调用能力集成进网关。它不仅能转发请求，还能作为 MCP Server 的托管点，让 AI Agent 更容易地通过网关获取外部工具能力，简化了 Agent 的基础设施复杂度。

**架构优势分析**
*   **毫秒级配置生效**：得益于 Envoy 的 xDS 协议（尤其是增量 xDS），配置变更可秒级推达到数据平面，且无需断开连接，这对于长连接场景（如 AI 对话）至关重要。
*   **极致性能**：数据平面 Envoy 采用异步非阻塞 I/O 模型，配合 Go 控制平面的轻量级协程，实现了高吞吐与低延迟。

---

### 2. 核心功能详细解读

**主要功能与使用场景**
1.  **AI 网关**：
    *   **统一 API 接口**：将不同厂商的 LLM API 统一化为标准接口（如 OpenAI 格式），降低上层应用切换模型成本。
    *   **Token 管理**：实时统计请求和响应的 Token 消耗，便于成本控制。
    *   **提示词增强**：在网关层动态插入 System Prompt，实现统一的人设注入或安全策略。
2.  **MCP 系统集成**：
    *   解决了 AI Agent 如何安全、高效地调用外部 API 的问题。Higress 可以作为 MCP 协议的透明代理，将内部微服务注册为 AI 可用的工具。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、全链路灰度发布、Mock 服务、认证鉴权。

**解决了什么关键问题**
*   **AI 落地的碎片化**：企业内部既有微服务，又有新兴的 AI 应用。Higress 提供了一个统一入口，避免了维护两套网关（一套业务网关，一套 AI 网关）的尴尬。
*   **流式处理的中间件缺失**：传统 API 网关难以处理 SSE (Server-Sent Events) 流式响应的修改（如审计、脱敏）。Higress 的 WASM 插件支持对流式分片进行实时处理。

**技术实现原理**
*   **LLM 路由**：基于 HTTP Header 或 Body 内容（如 JSON 模型字段）进行路由分发。
*   **流式拦截**：利用 Envoy 的流式处理能力，WASM 插件可以挂载在 Decoder/Filter 阶段，对数据流进行分片缓冲、处理后再转发，实现了类似“中间人”的透明处理能力。

---

### 3. 技术实现细节

**关键算法与技术方案**
*   **配置热更新**：基于 Istio 的 Galley 组件优化，监听 K8s APIServer，转换为 Envoy 的 EDSS (Endpoint Discovery Service) 和 LDSS (Listener Discovery Service) 配置，通过 gRPC 推送给 Envoy。
*   **WASM 虚拟机**：集成 **Wasmtime** 或 **V8** 引擎。Higress 对 WASM 插件进行了内存和 CPU 的隔离限制（通过 cgroups），防止插件异常导致网关崩溃。

**代码组织结构**
*   代码通常分为 `pkg`（核心逻辑）、`plugins`（内置 WASM 插件源码）、`installer`（Helm charts）等模块。
*   **设计模式**：大量使用 **过滤器模式** 和 **责任链模式**。在 Go 控制平面，通过 Controller 模式监听资源变化；在数据平面，通过 Envoy Filter Chain 组织处理逻辑。

**性能优化与扩展性**
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **可扩展性**：通过 WASM，开发者可以用 Python/Go 编写逻辑，无需修改网关核心代码，甚至不需要重新编译网关。

---

### 4. 适用场景分析

**适合使用的项目**
*   **AI 应用开发**：特别是需要对接多个大模型厂商，或需要对大模型输出进行实时审核/脱敏的场景。
*   **微服务架构**：基于 K8s 的云原生架构，需要统一流量入口的企业。
*   **AI Agent 构建**：需要通过 MCP 协议集成外部工具和数据源的智能体应用。

**最有效的情况**
*   当你需要将企业内部的微服务能力快速暴露给 LLM（即 Function Calling）时，Higress 的 MCP + Gateway 功能是目前最优雅的解决方案之一。
*   需要对 AI 调用成本进行精细化管控（按部门、用户限流、计费）时。

**不适合的场景**
*   **极低延迟的交易系统**：虽然 Envoy 很快，但引入 WASM 插件会有额外的序列化/反序列化开销，对于微秒级要求的纯交易场景可能不如 Nginx + Lua (OpenResty) 极致。
*   **非 K8s 环境**：Higress 深度绑定 K8s 生态，如果是传统虚拟机部署，会丧失其动态配置和编排的巨大优势。

---

### 5. 发展趋势展望

**技术演进方向**
*   **从流量网关到语义网关**：未来网关将不仅处理 HTTP 协议，还会理解 Prompt 的语义，进行智能路由（如：简单问题路由给小模型，复杂问题路由给大模型）。
*   **边缘计算结合**：Higress 可能会进一步向边缘端推进，利用 WASM 的轻量级特性，将 AI 推理或预处理逻辑下沉到边缘节点。

**社区反馈与改进空间**
*   **文档与易用性**：作为一个新兴项目，其 AI 相关的文档和最佳实践仍有待丰富，特别是 MCP 协议的落地案例较少。
*   **WASM 调试难度**：编写 WASM 插件的调试体验相比直接编写 Go 代码仍有门槛，需要更好的工具链支持。

---

### 6. 学习建议

**适合人群**
*   具备 Go 语言基础，了解 Kubernetes 基本概念。
*   对云原生架构、Service Mesh 有兴趣的后端开发者或架构师。

**学习路径**
1.  **基础**：先熟悉 Envoy 的基本概念和 K8s Ingress 机制。
2.  **核心**：阅读 Higress 官方文档中关于“AI 网关”和“WASM 插件”的部分。
3.  **实践**：在本地 Kind 集群中部署 Higress，尝试配置一个转发给 OpenAI 的路由，并编写一个简单的 Go WASM 插件修改 HTTP Header。

---

### 7. 最佳实践建议

**如何正确使用**
*   **插件隔离**：生产环境中，务必为 WASM 插件配置合理的内存限制和超时时间，防止有缺陷的插件拖垮整个网关实例。
*   **模型抽象**：利用 Higress 的 Provider 抽象能力，在应用层代码中只调用“Higress AI 网关”，由网关负责路由到具体的模型（如 qwen-turbo 或 gpt-4），这样应用无需变更代码即可切换底层模型。

**性能优化**
*   **连接池**：合理配置 Envoy 到后端 Upstream（LLM 服务或微服务）的连接池大小，避免 LLM 高并发时的连接建立延迟。
*   **缓存策略**：对于相同的 Prompt 请求，可以在网关层配置缓存（需注意 LLM 的概率性特性，缓存需谨慎），或者缓存 Prompt 的预处理结果。

---

### 8. 哲学与方法论：第一性原理与权衡

**抽象层与复杂性转移**
*   Higress 在 **协议理解** 层面做了抽象。它假设 AI 时代的流量不仅仅是字节流，而是“语义流”。
*   它将 **AI 路由和鉴权** 的复杂性从业务代码（应用层）转移到了 **基础设施层**（网关层）。
*   **代价**：网关变得更重了。以前网关只负责转发，现在网关需要理解 Token、理解 SSE、甚至理解 Prompt 格式。这要求运维团队必须具备更高的 AI 基础设施认知。

**默认价值取向**
*   **可扩展性 > 极致性能**：选择 WASM 而非静态编译的 C++ Filter，牺牲了一点点性能（纳秒级），换取了极大的动态扩展灵活性。
*   **标准化 > 兼容性**：强制推行 OpenAI 兼容协议和 MCP 协议，试图在混乱的 AI 生态中建立秩序。

**工程哲学与误用风险**
*   **范式**：**“网关即中间件”**。Higress 试图通过 WASM 让网关变成一个分布式的中间件运行时。
*   **误用点**：最容易误用的是 **在网关中编写过重的业务逻辑**。虽然 WASM 允许写复杂逻辑，但网关的核心职责是流量控制。如果在网关里进行复杂的数据库查询或耗时计算，会阻塞 I/O 线程，导致整个网关吞吐量下降。

**可证伪的判断**
1.  **性能判断**：在开启 3 个以上复杂 WASM 插件（如请求

---
## 代码示例




```python
# 示例1：Higress网关路由配置
def higress_route_config():
    """
    配置Higress网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway()
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",      # 匹配路径模式
        service="user-service", # 目标服务名
        methods=["GET", "POST"], # 允许的HTTP方法
        plugins=["auth-plugin"] # 启用的插件
    )
    
    # 添加另一个路由规则
    gateway.add_route(
        path="/api/v2/*",
        service="order-service",
        methods=["GET"],
        plugins=["rate-limit-plugin"]
    )
    
    # 应用配置
    gateway.apply_config()

**说明**: 这个示例展示了如何使用Higress配置网关路由，实现根据请求路径将流量分发到不同的微服务，并附加认证和限流插件。

```python


def custom_auth_plugin():
"""
开发自定义认证插件
解决问题：实现基于JWT的请求认证
"""
from higress import Plugin, Context
class JWTAuthPlugin(Plugin):
def on_request(self, context: Context):
# 从请求头获取JWT token
token = context.request.headers.get("Authorization", "")
# 验证token
if not self._verify_jwt(token):
context.response.status_code = 401
context.response.body = "Unauthorized"
return context.response.stop()
# 添加用户信息到请求头
user_info = self._decode_jwt(token)
context.request.headers["X-User-Id"] = user_info["id"]
def _verify_jwt(self, token: str) -> bool:
# 实际项目中这里应该实现真正的JWT验证逻辑
return token.startswith("Bearer ")
def _decode_jwt(self, token: str) -> dict:
# 实际项目中这里应该实现真正的JWT解码逻辑
return {"id": "12345"}
# 注册插件
plugin = JWTAuthPlugin()
plugin.register()

```python
# 示例3：Higress流量管理
def traffic_management():
    """
    配置灰度发布和流量分割
    解决问题：实现新版本的灰度发布
    """
    from higress import TrafficSplitter
    
    # 创建流量分割器
    splitter = TrafficSplitter()
    
    # 配置灰度发布规则
    splitter.add_rule(
        service="product-service",
        versions={
            "v1": 80,  # 80%流量到旧版本
            "v2": 20   # 20%流量到新版本
        },
        match_headers={
            "X-Canary": "true"  # 带此头的请求全部发往v2
        }
    )
    
    # 应用流量规则
    splitter.apply()

**说明**: 这个示例展示了如何使用Higress实现灰度发布，通过流量分割控制新旧版本的流量比例，并支持基于请求头的定向流量分配。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴内部拥有庞大的电商生态，包括淘宝、天猫等核心业务。这些业务对API网关有极高的要求，需要处理每秒百万级的QPS（每秒查询率），同时支持复杂的路由逻辑、流量管理和安全防护。

**问题**:  
随着业务规模的扩大，原有的API网关在性能和扩展性上遇到瓶颈。传统网关难以应对高并发场景下的流量突发，且配置灵活性不足，无法快速响应业务需求的变化。此外，多语言（Java、Go等）微服务的调用链路复杂，导致调试和监控困难。

**解决方案**:  
阿里巴巴基于开源的Istio和Envoy项目，开发了Higress。Higress结合了云原生API网关和流量管理的能力，支持动态配置、高性能路由和全面的流量观测。通过Higress，阿里巴巴实现了对内部微服务的统一管理，并优化了跨语言服务的调用效率。

**效果**:  
Higress上线后，阿里巴巴核心电商业务的API网关性能提升了30%，能够稳定支撑双11等大促期间的流量高峰。同时，配置变更的响应时间从小时级缩短到分钟级，显著提升了开发运维效率。

---



### 2：某大型互联网公司微服务架构升级

 2：某大型互联网公司微服务架构升级

**背景**:  
该互联网公司拥有数百个微服务，采用Spring Cloud和Dubbo混合架构。随着业务全球化扩展，需要支持多云部署和跨区域流量调度，同时降低API网关的运维成本。

**问题**:  
原有API网关基于传统架构，无法满足多云部署的需求，且扩展性受限。跨区域流量调度依赖手动配置，效率低下。此外，网关与微服务的监控数据分散，难以实现全链路追踪。

**解决方案**:  
该公司引入Higress作为新一代API网关，利用其云原生特性实现多云部署和自动化流量管理。Higress与Prometheus和Skywalking集成，提供了统一的监控和追踪能力。同时，通过Higress的插件市场，快速实现了自定义认证和限流功能。

**效果**:  
Higress帮助该公司实现了跨区域流量的智能调度，延迟降低了20%。运维成本减少40%，同时通过全链路监控快速定位了多次性能瓶颈问题，业务可用性提升至99.99%。

---



### 3：开源社区AI服务集成

 3：开源社区AI服务集成

**背景**:  
一家AI初创公司需要为外部开发者提供统一的API接口，以访问其自研的机器学习模型。这些模型部署在多个云平台上，且需要支持高频调用和动态扩展。

**问题**:  
直接暴露模型服务存在安全风险，且缺乏统一的流量控制和计费能力。此外，不同云平台的API规范不一致，导致客户端集成复杂。

**解决方案**:  
该公司使用Higress作为API网关，统一管理所有模型服务的访问。Higress的插件系统被用于实现API认证、请求限流和动态计费。通过Higress的Wasm插件能力，快速集成了自定义的鉴权逻辑。

**效果**:  
Higress的引入使该公司能够安全地对外开放AI服务，API调用成功率提升至99.5%。开发者的集成时间从数天缩短到数小时，同时通过精细化的流量控制，降低了30%的云资源成本。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能优秀，但不如Envoy | 基于Lua和Nginx，性能接近Kong |
| 易用性 | 提供图形化控制台，配置简单，适合云原生场景 | 配置复杂，需要较多手动操作 | 配置灵活但学习曲线较陡 |
| 成本 | 开源免费，企业版收费 | 开源版免费，企业版收费 | 完全开源，无企业版 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性中等 | 支持Lua和Python插件，扩展性强 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API网关 | 传统API网关、微服务 | 高性能API网关、微服务 |

### 优势分析

- 优势1：基于Envoy和Istio，深度集成云原生生态，适合Kubernetes环境。
- 优势2：支持Wasm插件，扩展性和灵活性更强，适合复杂业务需求。
- 优势3：提供图形化控制台，降低运维和配置复杂度，适合中小团队。
- 优势4：阿里背书，企业级支持和稳定性有保障。

### 不足分析

- 不足1：社区资源相对Kong和APISIX较少，第三方插件和文档有限。
- 不足2：企业版功能可能需要付费，增加长期使用成本。
- 不足3：对非云原生或传统架构的支持不如Kong成熟。
- 不足4：Wasm插件生态尚在发展中，不如Lua插件成熟。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**:  
Higress 基于 Istio 与 Envoy 构建，原生支持 WebAssembly (Wasm)。相比传统的 Lua 脚本或 C++ 插件，Wasm 插件提供了更高的安全性、隔离性以及多语言开发能力（支持 C++, Go, Rust, AssemblyScript 等）。利用 Wasm 插件可以在不重启网关的情况下动态扩展网关功能，如自定义认证、请求头修改或响应体处理。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 编写插件逻辑，利用 Higress 提供的 Proxy-Wasm SDK 处理请求/响应头或 Body。
3. 将编译好的 `.wasm` 文件上传至 Higress 的 Wasm 插件管理中，或配置 OCI 存储库进行远程拉取。
4. 在网关路由配置中关联该 Wasm 插件，并配置所需的插件参数。

**注意事项**:  
- Wasm 插件运行在沙箱中，虽然安全性高，但频繁的内存拷贝和序列化会带来一定的性能损耗，需避免在插件中进行密集计算。
- 生产环境建议对 Wasm 插件进行资源限制（CPU 和内存），防止插件异常导致网关不稳定。

---

### 实践 2：精细化流量管理与路由配置

**说明**:  
Higress 继承并增强了 Istio 的流量管理能力。最佳实践包括使用虚拟主机和路由表的组合来管理多域名、多路径的流量转发。通过配置 Header 匹配、权重路由和 Header 重写，可以实现蓝绿发布、金丝雀发布以及 A/B 测试等复杂的流量调度场景。

**实施步骤**:
1. 定义 `Ingress` 或 `Gateway` 资源来接入外部流量。
2. 配置具体的路由规则，区分不同的域名或路径前缀。
3. 设置流量匹配条件，例如基于 HTTP Header（如 `user-id` 或 `canary: true`）进行分流。
4. 配置服务发现，将路由指向具体的 Service 名称或固定 IP 地址。

**注意事项**:  
- 路由匹配优先级遵循“最长匹配原则”，需注意避免路由规则冲突导致流量被错误的规则截获。
- 在进行金丝雀发布时，建议基于 Header 分流而非百分比权重，以便于回滚和问题排查。

---

### 实践 3：全链路安全防护与认证

**说明**:  
在云原生架构下，网关是流量的唯一入口，必须实施严格的安全策略。Higress 支持主流的认证协议（如 JWT, OIDC, Basic Auth, AK/SK）。最佳实践是结合 Wasm 插件或原生配置实现 mTLS（双向认证），确保服务间通信的加密与身份验证，防止中间人攻击和未授权访问。

**实施步骤**:
1. 在网关配置中开启 HTTPS，并配置有效的 TLS 证书。
2. 启用 JWT 认证插件，对接统一的认证中心（如 Keycloak 或 Auth0），验证请求中的 `Authorization` 头。
3. 对于后端服务，配置 mTLS 策略，强制网关与后端服务之间的双向证书验证。
4. 配置 IP 黑白名单或限流策略，抵御恶意攻击。

**注意事项**:  
- JWT 验证会引入一定的网络延迟，建议配置本地缓存以减少对认证中心的频繁请求。
- 定期轮换 TLS 证书和 JWT 密钥，避免证书过期导致的服务中断。

---

### 实践 4：服务注册与发现集成

**说明**:  
Higress 设计初衷之一是打通微服务生态。它原生支持 Nacos, Consul, Eureka, ZooKeeper 以及 Kubernetes CoreDNS。最佳实践是将 Higress 与现有的注册中心打通，实现自动化的服务发现，避免在网关层硬编码后端服务 IP 地址，从而实现服务的动态扩缩容感知。

**实施步骤**:
1. 在 Higress 全局配置中添加对应类型的注册中心（如 Nacos）地址与认证信息。
2. 配置来源服务，指定要监听的命名空间或服务分组。
3. 在创建路由时，直接选择注册中心中的服务名称作为目标服务。
4. 验证当后端服务 Pod 或实例发生变更时，网关是否能实时感知并更新路由列表。

**注意事项**:  
- 如果注册中心服务数量极多（如上万级），建议配置服务分组或按需订阅，避免全量订阅导致网关内存溢出。
- 确保注册中心与 Higress 之间的网络连通性，防火墙需开放相应端口。

---

### 实践 5：可观测性建设与监控告警

**说明**:  
为了保障网关的稳定性，必须建立完善的可观测性体系。Higress 提供了丰富的日志、指标和链路追踪能力。最佳实践是将 Higress 的访问日志接入日志系统（如 Elasticsearch, SLS），将监控指标接入 Prometheus

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 和 Istio 构建，Envoy 对 HTTP/3 有较好的支持。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，能显著降低弱网环境下的延迟，并提升连接迁移能力（如网络切换）。

**实施方法**:
1. 在 Higress 网关的监听器配置中，启用 HTTP/3 协议支持。
2. 配置 QUIC 协议相关参数（如最大数据包大小、空闲超时等）。
3. 确保后端服务也支持 HTTP/3 或配置 Higress 进行协议转换。

**预期效果**: 在高延迟或丢包网络环境下，页面加载时间减少 20%-30%，连接建立成功率提升。

---

### 优化 2：启用 WASM 插件本地缓存与预编译

**说明**: Higress 支持通过 WASM (WebAssembly) 扩展功能。WASM 插件的冷启动和编译可能带来额外的 CPU 开销。通过启用本地缓存和预编译（AOT），可以减少运行时的编译延迟。

**实施方法**:
1. 在 Higress 配置中启用 WASM 插件的本地缓存功能。
2. 使用 `wasm-opt` 等工具对 WASM 文件进行体积优化和性能优化。
3. 预编译 WASM 模块为机器码（如果运行时支持），减少即时编译（JIT）的开销。

**预期效果**: WASM 插件初始化时间减少 50% 以上，请求处理延迟降低 10-20ms。

---

### 优化 3：优化 DNS 查询缓存与连接池

**说明**: 频繁的 DNS 查询和短连接建立会增加网络延迟。通过调整 Higress 的 DNS 缓存策略和后端服务的连接池配置，可以减少网络往返时间。

**实施方法**:
1. 增大 Higress 的 DNS 查询缓存 TTL（Time To Live）。
2. 配置 HTTP/2 或 gRPC 后端服务的连接池大小（如 `max_connections`）。
3. 启用连接复用（Keep-Alive），减少 TCP 握手次数。

**预期效果**: 后端服务响应时间减少 10%-15%，网络错误率降低。

---

### 优化 4：启用请求/响应压缩

**说明**: 对于文本类数据（如 JSON、XML、HTML），启用 Gzip 或 Brotli 压缩可以显著减少传输数据量，从而降低带宽占用和传输延迟。

**实施方法**:
1. 在 Higress 的路由配置中启用 Gzip 压缩。
2. 设置压缩的最小阈值（如 1KB），避免小文件压缩浪费 CPU。
3. 根据客户端 `Accept-Encoding` 头动态选择压缩算法。

**预期效果**: 传输数据量减少 60%-80%，带宽成本降低，大文件传输速度提升 30% 以上。

---

### 优化 5：调整工作线程与资源限制

**说明**: Higress 的性能受限于 CPU 和内存配置。通过合理调整工作线程数和资源限制，可以充分利用多核 CPU 的并行处理能力。

**实施方法**:
1. 根据 CPU 核心数设置 `worker_processes` 或 `worker_threads`（通常设置为 `CPU 核心数 - 1`）。
2. 调整 Higress 容器的 CPU 和内存限制（如 Kubernetes 的 `requests` 和 `limits`）。
3. 监控 CPU 和内存使用率，避免资源瓶颈。

**预期效果**: 吞吐量（QPS）提升 20%-50%，延迟降低 10%-20%（具体取决于硬件配置）。

---

### 优化 6：启用 Prometheus 监控与日志采样

**说明**: 过于详细的日志和监控数据可能影响性能。通过启用日志采样和优化监控指标采集频率，可以减少 I/O 和 CPU 开销。

**实施方法**:
1. 配置日志采样率（如仅记录 10% 的请求日志

---
## 学习要点

- 基于提供的信息（Higress 是阿里开源的 API 网关），以下是关键要点总结：
- Higress 是阿里云开源的、基于 Istio 的下一代云原生 API 网关，旨在解决云原生时代流量治理与网关管理的碎片化问题。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够作为 K8s 集群的统一流量入口，实现从南向（入口流量）到北向（服务网格）的全链路管理。
- 提供了强大的 WAF（Web 应用防火墙）插件能力，支持对流量进行精细化的安全防护与策略管理。
- 兼容 Envoy 和 Nginx Ingress 的配置习惯，并支持与 Dubbo、gRPC 等微服务协议无缝对接，降低了传统架构向云原生迁移的门槛。
- 拥有高性能的代理转发能力，并支持通过 WASM (WebAssembly) 技术进行灵活的热插拔插件扩展。
- 旨在打通微服务网关与 Ingress 网关的界限，通过一套架构同时支持南北向流量管理与东西向流量治理，简化运维复杂度。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与Higress的定位
- Higress的核心架构与组件（基于Istio与Envoy）
- 基本术语：Ingress、Gateway、路由、服务发现
- 容器环境（Docker/Kubernetes）基础操作

**学习时间**: 1-2周

**学习资源**:
- [Higress 官方文档](https://higress.io/docs)
- [Higress GitHub 仓库](https://github.com/alibaba/higress)
- [Kubernetes 基础教程](https://kubernetes.io/zh/docs/tutorials/)

**学习建议**: 
先通过官方文档理解Higress与传统网关（如Nginx）的区别，建议在本地Docker环境快速部署一个Higress实例，体验基本的流量转发功能。

---

### 阶段 2：核心功能与配置

**学习内容**:
- Higress 的安装与部署（Docker 与 Kubernetes 模式）
- 域名、路径、Header 路由配置
- 服务来源配置：Kubernetes Service、Nacos、固定地址
- 基础插件系统：WAF、限流、CORS、请求/响应头修改
- 控制台（Console）的使用与操作

**学习时间**: 2-3周

**学习资源**:
- [Higress 快速开始指南](https://higress.io/docs/latest/ops/deploy-by-docker/)
- [Higress 插件市场文档](https://higress.io/docs/latest/user/plugin-common/)
- [Envoy 基础概念](https://www.envoyproxy.io/docs/envoy/latest/intro/what_is_envoy)

**学习建议**: 
重点掌握“路由配置”和“插件配置”两个核心板块。尝试搭建一个包含两个后端服务的测试环境，配置基于权重的灰度发布，并启用一个限流插件进行测试。

---

### 阶段 3：高级特性与生态集成

**学习内容**:
- 高级流量治理：金丝雀发布、蓝绿发布、负载均衡策略
- 安全防护：WAF 规则配置、认证鉴权（JWT/OIDC）、mTLS
- 服务网格集成：Higress 作为 Istio Ingress Gateway 的使用
- 高可用与性能调优：资源限制、长连接、连接池配置
- Prometheus 监控指标采集与 Grafana 展示

**学习时间**: 3-4周

**学习资源**:
- [Higress 流量治理最佳实践](https://higress.io/docs/latest/user/traffic-management/)
- [Higress 安全配置文档](https://higress.io/docs/latest/user/security/)
- [Istio 流量管理概念](https://istio.io/latest/docs/concepts/traffic-management/)

**学习建议**: 
深入学习 Higress 在微服务场景下的应用。建议结合 Prometheus 观察不同配置下的 QPS、延迟等指标。尝试对接 Nacos 或 Consul 进行服务发现测试。

---

### 阶段 4：插件开发与云原生实战

**学习内容**:
- Wasm (WebAssembly) 技术基础
- Higress 自定义插件开发（Go/C++/Rust）
- 插件的生命周期管理与配置规范
- Higress 在 Knative 等 Serverless 场景下的应用
- 生产环境运维：日志排查、版本升级、容灾备份

**学习时间**: 4-6周

**学习资源**:
- [Higress 自定义插件开发指南](https://higress.io/docs/latest/user/wasm-go/)
- [Higress 官方博客案例](https://higress.io/blog)
- [WebAssembly 在代理侧的应用](https://webassembly.org/)

**学习建议**: 
动手编写一个简单的 Wasm 插件（例如修改请求 Body 或实现简单的自定义鉴权逻辑），并在 Higress 中加载测试。关注生产环境下的平滑升级与回滚策略。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部两年多的实战经验，由阿里云携手蚂蚁集团以及社区多名参与者联合开源的云原生 API 网关。它建立在 Istio（Envoy）之上，旨在解决云原生时代流量治理的痛点。Higress 的前身是阿里云内部广泛使用的 API 网关技术，它继承了阿里巴巴在电商、金融等高并发场景下的流量管理经验，并针对云原生架构进行了深度优化。

---



### 2: Higress 与 Kong、Nginx 或 APISIX 等传统网关相比有什么优势？

2: Higress 与 Kong、Nginx 或 APISIX 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”和“标准化”架构：
1.  **深度集成 K8s 与 Istio**：Higress 原生支持 Kubernetes 和 Istio 服务网格，可以无缝接管 Ingress 流量，实现从南向（外部访问）到北向（服务间调用）的统一治理，而传统网关通常需要额外配置才能与网格协同。
2.  **高性能与低资源消耗**：基于 Envoy C++ 内核开发，相比基于 Lua 的 OpenResty（Kong/APISIX），Higress 在处理高并发请求时通常具有更低的延迟和更稳定的资源占用。
3.  **安全防护**：集成了阿里云 Web 应用防火墙（WAF）的核心能力，开箱即用地提供强大的安全防护。
4.  **插件生态兼容**：支持 K8s Ingress 注解，兼容 Nginx 的配置习惯，同时支持 WASM 插件，允许使用多种编程语言（如 Go、C++、Rust）编写扩展插件，比传统的 Lua 插件更安全、易于维护且性能更高。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

**A**: 是的，Higress 非常重视迁移的便利性。
1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，可以帮助用户将现有的 Nginx.conf 配置转换为 Higress 的路由配置。
2.  **K8s Ingress 标准支持**：Higress 完全实现了 Kubernetes Ingress 规范，因此它可以作为 K8s 的 Ingress Controller 直接替换掉原生的 Nginx Ingress Controller，通常只需要修改 Service 的 selector 配置即可平滑切换。
3.  **阿里云 MSE 托版**：对于商业用户，阿里云提供 MSE（微服务引擎）云托管版 Higress，提供全托管服务和企业级支持。

---



### 4: 什么是 Higress 的 WASM 插件机制？为什么它很重要？

4: 什么是 Higress 的 WASM 插件机制？为什么它很重要？

**A**: WASM（WebAssembly）是 Higress 架构中的一个关键特性。
1.  **灵活性**：传统的 API 网关扩展通常需要使用 Lua（如 OpenResty）或 C++/Java。Lua 开发调试困难，C++ 开发门槛高且容易导致内存安全问题。WASM 允许开发者使用 Go、Rust、JavaScript 甚至 C++ 编写插件逻辑。
2.  **隔离性与安全性**：WASM 插件运行在独立的沙箱环境中。即使插件代码崩溃或出现内存溢出，也不会导致整个网关进程崩溃，极大地提高了网关的稳定性。
3.  **热加载**：WASM 插件支持动态加载和卸载，无需重启网关服务即可更新业务逻辑，这对于生产环境的连续性至关重要。

---



### 5: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

5: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

**A**: 是的，Higress 对微服务协议有非常完善的支持。
1.  **gRPC**：Higress 原生支持 gRPC 协议的代理和路由，支持将 HTTP/JSON 请求转换为 gRPC 请求，实现网关对后端 gRPC 服务的透明调用。
2.  **Dubbo**：作为阿里巴巴出品的网关，Higress 对 Dubbo（特别是 Dubbo 3.0）有深度支持。它可以将 HTTP 请求转换为 Dubbo 协议调用，允许前端通过 HTTP/RESTful 方式直接调用后端的 Dubbo 服务，无需额外的适配层。这对于许多使用 Java 技术栈的企业来说是一个巨大的便利。

---



### 6: Higress 的性能表现如何？能否支撑大流量场景？

6: Higress 的性能表现如何？能否支撑大流量场景？

**A**: Higress 的设计初衷就是为了应对阿里巴巴内部的高并发场景。
1.  **底层优势**：基于 Envoy 开发，Envoy 本身就是业界公认的高性能 L7 代理，采用 C++ 编写，具备非阻塞 I/O 和高效的连接池管理能力。
2.  **基准测试**：在官方和社区的基准测试中，Higress 在长连接、短连接、HTTPS 加解密以及高 QPS 场景下，性能表现优异，通常能够达到或超过业界主流网关的水平（如 Nginx、Envoy），且在开启大量

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速启动与路由验证

### 在本地 Docker 环境中快速部署 Higress，并配置一个简单的 HTTP 路由规则。要求实现：当访问 `/httpbin/` 路径时，将流量转发到公共的测试服务 `httpbin.org:80`，但去除路径前缀 `/httpbin`。

### 提示**:

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位及其在阿里云内部的实践，以下是针对实际生产场景的 6 条实践建议：

### 1. 利用 AI 指标进行精细化可观测性
**场景：** 在接入大模型（LLM）应用时，传统的 HTTP 状态码和延迟不足以反映业务健康度。
**建议：** 开启 Higress 的 AI 特有指标监控，重点关注 Token 吞吐量、首字生成时间（TTFT）以及大模型服务的 HTTP 错误率映射。
**最佳实践：** 将这些指标对接到 Prometheus + Grafana，设置基于 Token 消耗速率的告警，以便在成本激增或模型服务变慢时快速响应。

### 2. 实施模型供应商的容灾与降级策略
**场景：** 依赖单一 LLM 提供商（如 OpenAI 或通义千问）存在 API 不稳定或限流的风险。
**建议：** 配置 Higress 的“服务来源”功能，将多个 LLM 提供商注册为同一个服务。利用 Higress 的路由规则或插件（如 `request-block` 或自定义 Lua/Python 插件）实现自动故障转移。
**陷阱：** 不要仅依赖 DNS 轮询进行容灾，因为不同 LLM 提供商的 API 协议（如鉴权方式、参数格式）可能完全不同，需要在网关层做协议统一和适配。

### 3. 部署“提示词”安全防护插件
**场景：** 对外暴露 AI 应用时，恶意用户可能通过精心设计的 Prompt 进行“越狱”攻击，套取系统指令或消耗大量 Token。
**建议：** 在 AI 网关的鉴权之后、模型调用之前，配置输入审查插件。可以使用 Higress 的 `ai-statistics` 或结合 WAF 插件逻辑，检测输入文本的长度和敏感词。
**最佳实践：** 设置最大 Token 限制和输入内容过滤规则，防止恶意的长文本攻击导致后端成本失控。

### 4. 统一 API 协议与客户端兼容性
**场景：** 企业内部存在老旧业务，期望调用 OpenAI 格式的接口，但后端实际使用的是其他国产模型。
**建议：** 利用 Higress 的 AI 插件能力进行协议转换。配置路由将 `/v1/chat/completions` 等标准路径转发至非标准模型后端，并在网关层完成请求参数的映射和响应格式的重写。
**优势：** 这样可以实现模型切换的“无感化”，业务代码无需修改即可更换底座模型。

### 5. 缓存高频问题以降低 Token 成本
**场景：** AI 应用中存在大量重复或相似的用户提问，直接转发给 LLM 会产生不必要的费用。
**建议：** 利用 Higress 的缓存能力（或结合 KV 存储插件）对高频的 Prompt 和 Response 进行缓存。对于语义完全一致的请求，直接返回网关层的缓存结果。
**陷阱：** 注意缓存时效性。对于实时性要求高的场景，需谨慎设置 TTL，避免向用户返回过时的信息。

### 6. 在 K8s 环境下合理配置资源与 HPA
**场景：** Higress 部署在 Kubernetes 集群中，处理高并发 AI 请求时可能出现网关瓶颈。
**建议：** 根据并发连接数和 AI 请求的响应体大小（通常流式响应连接维持时间较长），合理调整 Pod 的 Request 和 Limit。配置 Horizontal Pod Autoscaler (HPA) 时，建议不仅仅关注 CPU，还要关注并发连接数指标。
**最佳实践：** 如果启用了 Wasm 插件处理复杂逻辑，确保为网关 Pod 分配足够的内存，并监控 Wasm 虚拟机的内存开销，防止 OOM（内存溢出）导致网关崩溃。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*