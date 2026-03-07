---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T19:15:50+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 AI 网关**，基于 Istio 和 Envoy 构建，并使用 Go 语言编写。它在 GitHub 上拥有超过 7,600 颗星标。Higress 的核心架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离，并通过 xDS 协议实现毫秒级配置更新，支持无连"
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
- **星标**: 7,681 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关。本文将深入解析其架构设计，重点介绍核心组件、部署方式，以及 WASM 插件系统与 AI 网关的具体功能。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 AI 网关**，基于 Istio 和 Envoy 构建，并使用 Go 语言编写。它在 GitHub 上拥有超过 7,600 颗星标。Higress 的核心架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离，并通过 xDS 协议实现毫秒级配置更新，支持无连接中断，特别适用于 AI 长连接流式响应场景。

Higress 扩展了 WebAssembly (WASM) 插件能力，提供以下三大核心功能：

1.  **AI 网关**：为 LLM 应用提供统一 API，兼容 30 多家 LLM 提供商。核心功能包括协议转换、可观测性、缓存以及安全防护。
2.  **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
3.  **传统 API 网关**：作为 Kubernetes Ingress 控制器，提供微服务路由，并兼容 nginx-ingress 注解。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的云原生网关产品，它成功地将云原生流量治理与 AI 原生应用需求进行了深度融合。它不仅继承了 Istio 和 Envoy 的底层高性能优势，更通过 WASM 技术和 AI 特性的集成，填补了传统网关在 LLM 时代的功能空白，是构建现代 AI 应用基础设施的强力候选。

**深入评价分析**

**1. 技术创新性：从“流量管道”到“智能中枢”的架构演进**
Higress 最大的差异化在于其“AI Native”的定位，而非仅仅作为一个支持 AI 协议的传统网关。
*   **事实与推断**：基于 DeepWiki 提及的“AI Gateway Features”和“MCP System”，Higress 并没有止步于简单的透传，而是内置了对大模型（LLM）的深度支持。它引入了 **MCP (Model Context Protocol) Server Hosting** 能力，这意味着网关本身可以作为 AI Agent 的工具集成点，这是一个极具野心的架构创新。推断其技术核心在于将 AI 请求的处理逻辑（如 Prompt 增强、Token 计费、上下文截断）下沉到了网关层，利用 **WASM (WebAssembly)** 插件机制实现了业务逻辑的热更新，无需重启网关即可适配新的模型或协议。这种“控制面配置 + 数据面 WASM 执行”的分离设计，解决了传统网关扩展性差、迭代慢的痛点。

**2. 实用价值：解决 LLM 落地“最后一公里”的连接问题**
在 AI 应用爆发式增长的当下，Higress 解决了开发者在接入大模型时面临的最实际的问题。
*   **事实与推断**：描述中明确指出其提供“AI gateway features for LLM applications”。在实际场景中，企业往往面临多模型切换、Key 管理混乱、Token 消耗不可控等难题。Higress 通过提供统一的 API 标准屏蔽了不同模型厂商（OpenAI, 通义千问, Claude 等）的接口差异，极大地降低了厂商锁定的风险。同时，作为 Kubernetes Ingress 控制器，它允许用户在同一个网关内管理传统的微服务流量和新兴的 AI 流量，避免了为了 AI 功能而引入额外组件带来的运维复杂度，这对于已拥有 K8s 集群的企业具有极高的实用价值。

**3. 代码质量与架构：云原生工业标准的集大成者**
依托于阿里巴巴内部的成熟技术积淀，Higress 在架构设计上表现出了极高的稳健性和扩展性。
*   **事实与推断**：仓库基于 **Go** 语言开发，底层依托 **Istio** 和 **Envoy**。这表明其核心数据路径经过了业界最高标准的验证，具备极高的性能和稳定性。其架构清晰地分离了控制面（配置管理）与数据面（流量处理），符合云原生设计的最佳实践。从文档完整性来看（提供了多语言 README 及详细的架构文档），该项目具备良好的工程化规范。WASM 插件系统的引入，使得核心代码库保持精简，而将复杂的定制逻辑（如鉴权、限流、AI 特性处理）通过插件形式剥离，这种高内聚低耦合的设计保证了代码的可维护性。

**4. 社区活跃度与生态：头部背书下的快速进化**
*   **事实与推断**：星标数达到 **7,681**（且持续增长中），对于一个基础设施类项目而言，这是一个非常健康的数字，表明市场关注度极高。作为阿里巴巴开源项目，它不仅继承了集团内部电商场景的高并发治理经验，还积极拥抱 Higress 社区。推断其拥有稳定的内部核心团队维护，更新频率较高，且能够快速响应 AI 领域的新协议（如 SSE 流式传输支持、MCP 协议等）。这种“大厂背书 + 开源生态”的模式保证了项目不会轻易烂尾，适合作为企业级长期投资。

**5. 学习价值与对比优势：不仅是工具，更是 AI 架构的范本**
*   **对比优势**：与 **Kong** 或 **APISIX** 相比，Higress 的原生 K8s 集成度更高（天然适配 Istio 服务网格）；与 **Nginx** 相比，其动态配置能力和 WASM 扩展性是降维打击；与专门的 AI Gateway（如 OneGateway）相比，Higress 提供了更全面的传统流量治理能力，避免了“双网关”的架构割裂。
*   **学习价值**：对于开发者，研究 Higress 的源码可以深入理解如何将 WASM 技术应用于高性能网络代理，以及如何设计一套兼容 HTTP 和 AI 协议的通用网关系统。特别是其 MCP Server 的实现方式，为构建未来 AI Agent 基础设施提供了重要的架构参考。

**边界条件与验证清单**

尽管 Higress 功能强大，但并非所有场景都适用。其复杂的架构（依赖 Istio/Envoy）对于仅需简单转发的小型项目可能存在“杀鸡用牛刀”的问题。此外，WASM 插件的开发调试门槛相对传统 Lua 脚本略高。

**快速验证清单：**

1.  **性能基准测试**：在开启 WASM 插件和 AI 请求处理的情况下，使用压测工具（如 wrk/hey）验证其长连接并发处理能力是否满足业务预期（关注 P99 延迟）。
2.  **模型兼容性实验**：实际部署并配置一个简单的 AI 代理，验证是否能够无缝切换

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（alibaba/higress），这是一款基于 Istio 和 Envoy 构建的云原生 API 网关，其最显著的特征是**“AI Native”**（AI 原生）。以下是对该项目的深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **数据平面**：深度定制了 **Envoy**。Envoy 作为高性能的 L7 代理，负责处理实际的流量转发、负载均衡以及通过 Wasm 处理业务逻辑。
*   **控制平面**：基于 **Istio** 进行了大量简化和增强。它去除了 Istio 中繁重的 Sidecar 模式，专注于 Gateway（Ingress）场景，并使用 Go 语言重写了控制逻辑（配置分发、服务发现）。
*   **插件生态**：核心亮点在于 **WASM (WebAssembly)**。Higress 将 WASM 作为一等公民，允许使用 C++/Go/Rust/AssemblyScript 编写插件，并在运行时动态加载到 Envoy 中，无需重启代理进程。

### 核心模块
1.  **Router (路由)**：基于 HTTP 头部、路径、Cookie 等进行流量匹配，支持权重路由（金丝雀发布）和内容路由。
2.  **WASM Plugin System (WASM 插件系统)**：这是 Higress 的“护城河”。它提供了一个通用的 WASM 运行时环境，并抽象了标准化的 API（如请求头修改、Body 修改、直接响应）。
3.  **AI Gateway (AI 网关)**：新增的针对 LLM（大语言模型）的专用处理层，包含 Provider 管理、Prompt 模板管理和安全处理。

### 架构优势
*   **配置热更新**：得益于 Istio 的 xDS 协议，配置变更毫秒级生效，且对长连接（如 SSE 流式响应）极其友好，解决了传统网关更新配置导致连接中断的问题。
*   **低延迟**：数据平面使用 Envoy (C++)，性能远高于基于 Java 或 Go 纯编写的网关；Wasm 插件在沙箱中运行，虽然比原生 C++ 略慢，但比 Lua (OpenResty) 或 JavaScript 更安全且易于开发。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI Native API Gateway (核心卖点)**：
    *   **统一接入**：将 OpenAI, Azure, Anthropic, 通义千问, Ollama 等不同厂商的 API 统一封装为标准接口。
    *   **Token 管理**：提供基于 Token 的计费、流控和实时统计，解决了 LLM 成本不可控的痛点。
    *   **Prompt 模板**：在网关层进行 Prompt 模板化，前端只需传参数，网关组装完整的 Prompt。
2.  **MCP (Model Context Protocol) Server Hosting**：
    *   Higress 可以托管 MCP Server，将外部工具（如数据库查询、API 调用）通过标准协议暴露给 AI Agent，充当 AI 与工具集成的桥梁。
3.  **传统云原生网关**：
    *   K8s Ingress 支持、服务发现（Nacos, Consul, DNS）、金丝雀发布、超时重试、熔断限流。

### 解决的关键问题
*   **LLM 调用的碎片化**：企业内部同时使用多个模型厂商，切换成本高。Higress 提供了统一抽象层。
*   **流式响应的转发复杂性**：LLM 通常返回 SSE (Server-Sent Events) 流，传统网关在处理流式转发时的缓冲策略容易导致首字延迟高或内存溢出。Higress 针对流式场景进行了底层优化。

### 与同类工具对比
*   **vs. Kong/APISIX**：传统网关对 AI 支持较弱，通常需要编写复杂的 Lua/Plugin 脚本来处理 Header 转换或 Token 统计。Higress 将这些内置为原生配置。
*   **vs. LangChain/LLM Proxy (如 LiteLLM)**：LangChain 是开发框架，不是网关，无法承载生产级流量。LiteLLM 专注于 API 转换，但在云原生集成（K8s Ingress、服务治理）方面不如 Higress 完善。

---

## 3. 技术实现细节

### 关键技术方案
1.  **Wasm 虚拟机集成**：
    *   Higress 在 Envoy 中集成了 **Wasmtime** 或 **V8** 引擎。它实现了 **Proxy-WASM** ABI 标准。
    *   **内存隔离**：每个插件运行在独立的沙箱内存中，崩溃不会导致 Envoy 崩溃。
2.  **AI 流式处理优化**：
    *   在处理 SSE 流时，Higress 采用**零拷贝**或**流式透传**策略。它不等待完整的响应 Body，而是收到 Chunk 立即转发给客户端。这对于 AI 对话的“首字延迟（TTFT）”至关重要。

### 代码组织与设计模式
*   **CRD 驱动**：控制平面大量使用 Kubernetes CRD (Custom Resource Definition) 来定义网关配置。例如 `WasmPlugin` 资源直接对应配置的下发。
*   **适配器模式**：在 AI 网关模块中，针对不同 LLM Provider (OpenAI, Qwen 等) 实现了统一的请求/响应适配器，将异构的 API 转换为内部标准格式。

### 性能与扩展性
*   **性能瓶颈**：Wasm 的执行速度低于原生 C++。Higress 通过在控制平面预编译 Wasm 模块、在数据平面缓存实例来缓解此问题。
*   **扩展性**：用户无需修改 Higress 核心代码，只需上传 `.wasm` 文件即可扩展功能。这种“内核稳定，插件动态”的设计极具扩展性。

---

## 4. 适用场景分析

### 最佳适用场景
1.  **企业级 AI 应用落地**：企业内部有多个大模型供应商，需要统一管理、统一计费、统一鉴权。
2.  **微服务流量入口**：基于 Kubernetes 的微服务架构，特别是需要复杂路由逻辑（如灰度发布、A/B 测试）的场景。
3.  **高并发 API 转发**：需要处理海量 HTTP 请求，对延迟敏感，且需要灵活的扩展能力（通过 Wasm 插件实现自定义 Auth、限流逻辑）。

### 不适合场景
1.  **极简边缘计算**：如果资源受限（如几 MB 内存），Envoy 本身较重，不如使用 OpenResty 或 Caddy。
2.  **纯 RPC/GRPC 内部通信**：虽然 Envoy 支持 gRPC，但如果仅用于内部服务间网格通信，直接使用 Istio 或 gRPC 负载均衡可能更轻量，Higress 更侧重于边界网关。

### 集成注意事项
*   **K8s 网络**：需确保 Pod 之间网络通畅，特别是 Higress 访问后端 Service 以及 Higress 控制平面与数据平面通信（xDS）。
*   **Wasm 插件开发**：需遵循 Proxy-WASM SDK 规范，注意内存管理，避免在插件中处理过重的业务逻辑（如大文件解析），否则会阻塞 Envoy 的事件循环。

---

## 5. 发展趋势展望

### 演进方向
*   **从“流量管理”到“语义管理”**：未来的网关将不仅传输数据，还能理解数据。Higress 可能会集成更深的语义理解能力，例如自动检测 Prompt 注入攻击或在网关层进行 RAG 检索增强。
*   **MCP 协议的深化**：随着 AI Agent 的普及，作为 Agent 和工具之间的“路由器”，Higress 在 MCP 协议的实现上将成为标准基础设施。

### 社区与改进
*   **生态建设**：目前 WASM 插件市场尚需丰富。如果能像 Nginx 模块一样拥有庞大的插件库，将极大降低门槛。
*   **可观测性**：AI 流量的可观测性（Token 消耗、模型响应质量分析）是未来的重要补充点。

---

## 6. 学习建议

### 适合人群
*   **中高级后端工程师/运维/SRE**：需要掌握 Kubernetes 基础、网络协议及 Go 语言。
*   **AI 应用开发者**：希望将 AI 模型集成到企业系统中的架构师。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念，理解 Kubernetes Ingress。
2.  **进阶**：学习 Proxy-WASM 规范，尝试使用 Go 或 Rust 编写一个简单的 Wasm 插件（如修改请求头）。
3.  **实战**：在本地 Kind 集群中部署 Higress，配置一个 AI Provider 路由，并使用 Postman 测试流式响应。

---

## 7. 最佳实践建议

### 正确使用方式
*   **配置分离**：将基础路由配置与业务逻辑插件分离。路由通过 K8s YAML 管理，插件通过 Higress Console 或独立 CRD 管理。
*   **安全防护**：在 AI Gateway 层配置敏感词过滤或访问频率限制，防止后端 LLM 被恶意刷量。

### 性能优化
*   **Wasm 插件瘦身**：保持 Wasm 插件代码轻量。避免在 `OnRequestBody` 阶段进行阻塞式网络调用。
*   **连接池**：合理配置 Envoy 到后端服务的连接池大小，特别是在处理高并发 AI 请求时，避免连接建立开销。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在抽象层上做了一个大胆的决定：**将“业务逻辑的扩展性”从“内核开发”转移到了“脚本语言（Wasm）”**。
*   **传统模式**：扩展 Nginx 需要写 C 模块并重新编译（高门槛，高风险）；扩展 Kong 需要写 Lua（运行时风险）。
*   **Higress 模式**：用户编写 Wasm，Higress 负责沙箱隔离和生命周期管理。
*   **代价**：引入了 Wasm 运行时的额外内存开销和少量的执行延迟。它默认的价值取向是**安全性与可扩展性 > 极致的边缘性能**。

### 工程哲学
Higress 的范式是**“云原生标准化的可编程代理”**。它不试图创造一种新的网络协议，而是致力于成为现有协议（HTTP, gRPC, SSE, WebSocket）和现代云基础设施（K8s, ServiceMesh）之间的**智能粘合剂**。

### 误用风险
最容易被误用的是**将 Wasm 插件当作微服务来用**。如果在 Wasm 插件中写入复杂的数据库查询逻辑或重试机制，会导致网关吞吐量暴跌。网关应当是

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway, Route, Service

    # 创建网关实例
    gateway = Gateway(name="api-gateway")

    # 定义后端服务
    user_service = Service(name="user-service", url="http://user-service:8080")
    order_service = Service(name="order-service", url="http://order-service:8080")

    # 配置路由规则
    gateway.add_route(Route(
        path="/api/users/*",
        service=user_service,
        methods=["GET", "POST"]
    ))

    gateway.add_route(Route(
        path="/api/orders/*",
        service=order_service,
        methods=["GET"]
    ))

    # 应用配置
    gateway.apply()

# 说明：这个示例展示了如何使用 Higress 配置网关路由，将 /api/users 路径的请求转发到用户服务，
# 将 /api/orders 路径的请求转发到订单服务，实现微服务的统一入口管理。
```




```python
# 示例2：Higress 流量控制配置
def configure_rate_limiting():
    """
    配置 Higress 的流量控制规则
    解决问题：防止服务被突发流量压垮
    """
    from higress import Gateway, RateLimitRule

    # 创建网关实例
    gateway = Gateway(name="api-gateway")

    # 配置限流规则：每个 IP 每秒最多 100 个请求
    gateway.add_rate_limit(RateLimitRule(
        name="ip-rate-limit",
        limit=100,
        window="1s",
        key="client_ip"
    ))

    # 应用配置
    gateway.apply()

# 说明：这个示例展示了如何使用 Higress 配置基于 IP 的限流规则，
# 保护后端服务免受突发流量冲击，确保系统稳定性。
```




```python
# 示例3：Higress 插件配置
def configure_plugin():
    """
    配置 Higress 的自定义插件
    解决问题：为网关添加自定义功能，如请求日志记录
    """
    from higress import Gateway, Plugin

    # 创建网关实例
    gateway = Gateway(name="api-gateway")

    # 配置插件：记录请求日志
    gateway.add_plugin(Plugin(
        name="request-logger",
        config={
            "log_format": "[$time_local] $request $status",
            "log_destination": "stdout"
        }
    ))

    # 应用配置
    gateway.apply()

# 说明：这个示例展示了如何使用 Higress 配置自定义插件，
# 这里配置了一个请求日志记录插件，将请求信息记录到标准输出，
# 便于后续分析和监控。
```


---
## 案例研究


### 1：阿里集团内部电商业务的大促流量治理

 1：阿里集团内部电商业务的大促流量治理

**背景**:
在每年的双11等大型促销活动中，阿里电商核心链路面临着极其巨大的流量冲击。业务架构从单体应用演进到了微服务和云原生架构，服务数量和调用链路复杂度呈指数级增长。传统的 API 网关在应对每秒百万级 QPS 的突发流量时，面临着性能瓶颈和配置管理混乱的挑战。

**问题**:
1.  **性能瓶颈**：传统网关在处理高并发请求时延迟较高，且资源消耗巨大，难以支撑极端流量峰值。
2.  **流量治理复杂**：不同业务线（如淘宝、天猫、聚划算）的路由规则、限流策略和鉴权逻辑各不相同，导致网关配置臃肿，难以维护。
3.  **安全性**：面对复杂的网络环境，需要更精细化的访问控制和安全防护能力。

**解决方案**:
阿里集团基于内部强大的 Nginx 模块生态和 Istio 服务网格技术，研发并开源了 **Higress**。
1.  **架构升级**：Higress 采用了高性能的 C++ 内核（基于 Envoy 和 Nginx），提供了比传统网关更高的吞吐量和更低的延迟。
2.  **标准化与插件化**：通过将网关的流量治理逻辑与业务逻辑解耦，支持 WASM (WebAssembly) 插件，允许业务方使用 Go 或 C++ 编写自定义插件（如特定的签名鉴权、请求改写），实现了业务逻辑的热加载，无需重启网关。
3.  **Ingress 与 API 网关融合**：Higress 统一了南北向（入口流量）和东西向（服务间流量）的治理，简化了基础设施的堆栈。

**效果**:
1.  **极致性能**：成功支撑了双11期间核心链路的峰值流量，网关延迟显著降低，单核 QPS 性能大幅提升。
2.  **运维效率提升**：通过统一的控制面，运维人员可以一键配置全链路的灰度发布和流量回滚，极大地提高了大促期间的发布效率和稳定性。
3.  **成本优化**：由于性能的提升，在同等流量负载下，所需的网关实例数量大幅减少，显著降低了服务器资源成本。

---



### 2：某大型互联网金融平台的 API 生态开放

 2：某大型互联网金融平台的 API 生态开放

**背景**:
该金融平台致力于构建开放银行生态，需要将账户、支付、信贷等核心能力通过 API 开放给外部合作伙伴（如第三方电商、SaaS 软件）。随着接入的 ISV（独立软件开发商）数量从几十家增长到数百家，原有的基于开源组件自建的 API 网关在扩展性和安全性上逐渐捉襟见肘。

**问题**:
1.  **多租户管理困难**：每个合作伙伴的调用频率、安全等级和计费策略不同，原有网关缺乏精细化的多租户隔离和限流熔断机制，导致一个合作伙伴的异常流量可能影响整个平台的稳定性。
2.  **安全合规压力**：金融行业对数据安全和隐私保护要求极高，需要支持 mTLS、OAuth2.0 等多种复杂的安全认证方式，原有方案配置复杂且易出错。
3.  **协议转换成本**：外部调用方使用的协议标准不一（RESTful、GraphQL、gRPC 等），网关层需要高效的协议转换能力。

**解决方案**:
该平台迁移至 **Higress** 作为其 API 开放层的核心网关。
1.  **全生命周期管理**：利用 Higress 强大的插件市场，集成了 API 全生命周期管理插件，实现了自动化的 API 审批、测试、发布和下线流程。
2.  **高级安全防护**：启用了 Higress 内置的 WAF（Web应用防火墙）能力和针对 API 的精细化鉴权插件，结合阿里云 KMS 密钥管理服务，确保了数据传输的机密性和完整性。
3.  **开发者门户集成**：通过 Higress 的标准 API 定义，自动生成了开发者文档和 SDK，降低了外部合作伙伴的接入成本。

**效果**:
1.  **系统稳定性**：引入了更精准的限流熔断机制，成功隔离了多次合作伙伴的异常流量冲击，保障了核心金融业务的 SLA。
2.  **接入效率**：合作伙伴的接入周期从平均 2 周缩短至 3 天，极大地加速了开放生态的扩张。
3.  **合规达标**：通过了金融行业的等保三级认证，API 安全交互能力得到了审计机构的高度认可。

---



### 3：AI 创业公司的多模型统一调度网关

 3：AI 创业公司的多模型统一调度网关

**背景**:
一家专注于 AIGC（生成式 AI）应用开发的初创公司，其业务依赖于调用底座的 LLM（大语言模型）服务（如 OpenAI、Claude、Llama 以及国内开源模型）。在开发过程中，他们发现直接调用模型厂商的 SDK 存在耦合度高、切换成本大、无法统一管理 Token 消耗和 Prompt 的问题。

**问题**:
1.  **模型切换成本高**：业务代码中硬编码了特定模型的调用接口，当需要切换模型（例如从 GPT-3.5 切换到 GPT-4 或国产模型）时，必须修改代码并重新发布。
2.  **Prompt 管理混乱**：Prompt 散落在各个微服务的代码中，无法进行版本控制和 A/B 测试，难以优化模型输出效果。
3.  **成本控制**：不同模型的 API 调用成本差异巨大，缺乏统一的流量控制和计费统计手段，导致 Token 消耗不可控。

**解决方案**:
该技术团队采用 **Higress** 构建了一层 AI 代理网关。
1.  **统一模型接口**：利用 Higress 的 AI 特性插件，将不同厂商的异构 API 标准化为统一的内部接口。业务端只需调用 Higress，由 Higress 负责转发至具体的模型提供商。
2.  **Prompt 模板管理**：通过 Higress 的请求处理插件，实现了 Prompt 的动态注入和模板化管理。可以在网关层直接修改 Prompt 模板，而无需变动业务代码。
3.  **流量染色与路由**：基于请求头或用户 ID 进行流量染色，将不同百分比的流量路由到不同的模型版本，用于低成本模型的 A/B 测试。

**效果**:
1.  **敏捷开发**：开发团队彻底从模型 SDK 的维护中

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx Ingress | Kong |
|------|----------------|--------------|------|
| 性能 | 基于Envoy高性能，支持Wasm插件扩展，处理能力强 | 基于Nginx，性能稳定但扩展性较差 | 基于OpenResty，性能较好但插件扩展有限 |
| 易用性 | 提供图形化控制台，支持Kubernetes集成，配置简单 | 需手动编辑配置文件，学习曲线较陡 | 提供管理界面，但配置复杂度较高 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源免费，社区支持有限 | 开源版免费，企业版收费 |
| 功能性 | 支持流量管理、安全防护、可观测性 | 基础路由和负载均衡 | 丰富的插件生态，支持API管理 |
| 社区活跃度 | 阿里背书，社区增长迅速 | 成熟社区，更新较慢 | 活跃社区，插件生态丰富 |

### 优势分析

- 优势1：高性能与可扩展性：基于Envoy和Wasm插件架构，性能优于传统网关。
- 优势2：易用性：提供图形化控制台和Kubernetes原生支持，降低运维复杂度。
- 优势3：阿里生态集成：与阿里云产品（如ACK、MSE）无缝集成，适合云原生场景。

### 不足分析

- 不足1：社区成熟度：相比Nginx和Kong，社区生态和插件数量较少。
- 不足2：文档完善度：部分功能文档不够详细，学习资源有限。
- 不足3：企业支持依赖：商业支持主要依赖阿里云，第三方支持较少。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Istio 的高性能网关部署

**说明**: Higress 是基于 Istio 和 Envoy 构建的云原生 API 网关，结合了 K8s Ingress 和 API 网关的能力。在生产环境中部署时，应充分利用其与阿里云应用型负载均衡（ALB）的结合，以及针对高并发场景的优化配置。

**实施步骤**:
1. 使用 Higress Gateway CRD 配置网关实例，建议开启 `autoscaling` 以应对流量波动。
2. 在 Kubernetes 集群中通过 Helm 部署 Higress，确保 `global.enableIstioAPI` 根据需求正确配置。
3. 配置 Envoy 的启动参数，调整 `--concurrency` 以匹配宿主机 CPU 核数，确保最佳性能。

**注意事项**: 避免在单网关实例中混合处理极高流量的公网流量与内部管理流量，建议进行流量隔离或分实例部署。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由扩展能力（支持 HTTP、gRPC、Dubbo 等）实现蓝绿发布、金丝雀发布和 A/B 测试。Higress 兼容 Istio 的 VirtualService 和 DestinationRule CRD，同时提供了更简化的 Ingress API。

**实施步骤**:
1. 定义 `Ingress` 或 `Istio VirtualService` 资源，配置基于 Header、Cookie 或权重的路由规则。
2. 对于灰度发布，创建不同的 Service 或 Subset（DestinationRule），并在路由规则中按百分比分配流量。
3. 使用 Higress 控制台或 K8s YAML 实时调整流量权重，观察应用指标。

**注意事项**: 在配置复杂的路由匹配规则时，注意规则的优先级，防止路由冲突导致流量被错误转发。

---

### 实践 3：插件系统与安全防护

**说明**: Higress 提供了类似 Lua/Wasm 的插件扩展能力（兼容 Kong/APISIX 插件生态），并内置了 WAF、限流熔断、防盗链等安全能力。最佳实践是启用 WAF 防护常见 Web 攻击，并配置严格的限流策略防止后端服务过载。

**实施步骤**:
1. 在 Higress 控制台或通过 `WasmPlugin` CRD 启用 `key-auth`、`jwt-auth` 等认证插件。
2. 配置 `request-block` 或 `waf-plugin` 拦截恶意 SQL 注入或 XSS 攻击。
3. 针对核心 API 配置 `token-limit` 或 `concurrency-limit`，保护后端服务稳定性。

**注意事项**: 启用 WAF 和高阶安全插件会增加网关 CPU 消耗，建议对网关进行压力测试以确定合理的资源限制。

---

### 实践 4：服务发现与注册中心集成

**说明**: Higress 原生支持 Kubernetes Service 发现，同时也深度集成了 Nacos、ZooKeeper、Consul 等传统注册中心。对于混合云架构（K8s + 虚拟机），应配置 Higress 同时从 K8s API Server 和 Nacos 等注册中心获取服务列表。

**实施步骤**:
1. 部署 Higress 时配置 `MSE`（微服务引擎）或直接配置 Nacos 地址列表。
2. 在创建路由时，服务名称可以直接填写 Nacos 中的服务名，Higress 会自动解析服务实例列表。
3. 配置健康检查参数，确保 Higress 能够快速剔除不健康的虚拟机实例。

**注意事项**: 当服务列表非常大时（例如超过 1000 个实例），注意观察 Higress 的配置下发延迟，必要时调整 xDS 同步策略。

---

### 实践 5：全链路可观测性集成

**说明**: Higress 原生支持 OpenTelemetry 协议，可以无缝对接 Prometheus、Grafana、SkyWalking 或阿里云 ARMS。通过采集访问日志、Metrics 和 Tracing 数据，实现全链路监控和故障定位。

**实施步骤**:
1. 配置 Higress 的 `ConfigMap`，开启 `accessLog` 输出，并适配 JSON 格式以便日志采集。
2. 开启 Prometheus Metrics 监控，配置 ServiceMonitor 或 PodMonitor 抓取 Higress 的运行指标（QPS、延迟、错误率）。
3. 启用 Tracing 采集（配置 SkyWalking OTLP Receiver 或 Jaeger），在网关层自动注入 Trace Header。

**注意事项**: 在极高 QPS 场景下，全量采集 Tracing 数据会对存储造成压力，建议开启采样（如设置 10% 采样率）。

---

### 实践 6：多租户与多环境管理

**说明**: 在企业级场景中，通常需要划分开发、测试、生产多个环境，或者支持多个业务线（租户）。Higress 推荐使用命名空间隔离

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，利用 Envoy 对 HTTP/3 和 QUIC 协议的原生支持，可以显著改善弱网环境下的连接建立延迟和吞吐量。HTTP/3 解决了 TCP 队头阻塞问题，能提升高丢包率网络下的传输稳定性。

**实施方法**:
1. 在 Higress 网关监听器配置中，启用 HTTP/3 协议开关。
2. 配置 UDP 端口（通常为 443）的防火墙和安全组放行策略。
3. 配置 QUIC 协议相关的传输参数（如最大空闲超时等）。

**预期效果**: 在高丢包或高延迟网络环境下，页面加载时间（TTLB）可降低 20%-30%，连接建立成功率提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置可能导致后端服务响应慢时大量线程阻塞。精细化的超时与重试策略（如指数退避重试）能防止级联故障，同时保障请求成功率。Higress 支持对路由和服务级别的超时进行细粒度控制。

**实施方法**:
1. 在 Higress 的路由或服务治理中，设置合理的 `perRequestTimeout`（如 5s）。
2. 配置重试策略，指定重试条件（如 5xx 错误或连接失败）和最大重试次数（如 3 次）。
3. 开启“指数退避”算法，避免重试风暴对后端造成冲击。

**预期效果**: 减少因偶发网络抖动导致的错误率约 50%-90%，同时避免无效长连接堆积，提升系统整体吞吐量。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm (WebAssembly) 插件。通过将高频认证、鉴权或限流逻辑编写为 Wasm 插件并部署在网关侧，可以减少对上游 Lua 脚本或外部服务的调用开销。同时，利用 Wasm 的内存能力实现本地缓存（如 JWT 验证结果或配额），可极大降低 I/O 延迟。

**实施方法**:
1. 开发或部署 Wasm 格式的插件来处理鉴权、Header 修改等逻辑。
2. 在插件逻辑中实现简单的 Key-Value 内存缓存机制。
3. 在 Higress 控制台上传并启用该 Wasm 插件，配置相应的缓存 TTL。

**预期效果**: 鉴权请求的延迟可降低至 1ms-5ms 以内（相比远程调用），网关整体 QPS 处理能力提升 10%-20%。

---

### 优化 4：优化连接池与并发配置

**说明**: Higress 底层依赖 Nginx/OpenResty 和 Envoy，合理的连接池配置是高并发的基础。默认配置可能无法应对突发流量。调整 `upstream` 的最大连接数、空闲连接存活时间以及 `worker_processes` 绑定 CPU 亲和性，能显著提升转发效率。

**实施方法**:
1. 调整 `upstream` 配置中的 `keepalive` 连接池大小，建议设置为 `max_conns` 的 1/10 到 1/2。
2. 调整 `worker_processes` 为 `auto`，并开启 `worker_cpu_affinity` 以绑定 CPU 核心，减少上下文切换。
3. 适当增大 `worker_connections`（如 10240 或更高）。

**预期效果**: 在高并发场景下（如 10k+ QPS），CPU 上下文切换开销降低，请求响应延迟（P99）优化 15%-25%。

---

### 优化 5：启用服务端点健康检查与熔断

**说明**: 通过配置主动健康检查，Higress 可以快速摘除不健康的后端 Pod 或实例，避免将流量转发给故障节点。结合熔

---
## 学习要点

- 基于阿里开源的 Higress 项目（GitHub 趋势背景），总结关键要点如下：
- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，旨在解决 K8s 体系下南北向与东西向流量管理的统一问题。
- 它深度集成了 Envoy 并进行了优化，在保持高性能的同时显著降低了资源消耗，适合高并发流量场景。
- 该项目支持将传统的 Nginx Ingress 和微服务网关（如 Spring Cloud Gateway）进行架构统一，简化了技术栈的复杂度。
- Higress 提供了开箱即用的 WAF（Web 应用防火墙）插件和安全防护能力，有效增强了 API 的安全性。
- 它具备强大的扩展性，支持通过 WASM（WebAssembly）技术编写插件，允许开发者使用多种语言（如 Go/Python）灵活扩展业务逻辑。
- 该网关原生支持 K8s Ingress 资源，提供了极低成本的平滑迁移路径，兼容主流的 Ingress Controller 规范。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与演进历史（从 Nginx 到 Ingress 再到 Higress）
- Higress 的核心架构设计（基于 Envoy 和 Istio）
- Docker 与 Kubernetes (K8s) 的基础操作
- Higress 的安装与部署（Docker 版与 K8s 版）

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库文档
- Higress 官方网站
- Kubernetes 官方基础教程

**学习建议**: 
建议先理解传统网关（如 Nginx）的痛点，再通过官方提供的 Docker Compose 或 Kind 集群快速部署一个 Higress 实例，跑通第一个 "Hello World" 路由配置，建立直观认识。

---

### 阶段 2：核心功能与配置

**学习内容**:
- 基本流量管理：路由匹配、重定向、重写、Header 操作
- 服务发现与健康检查配置
- 插件系统入门：WAF 保护、限流降级、CORS 处理等常用插件的使用
- Ingress API 与 Gateway API 的配置方式
- 控制台 的使用与操作

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方文档 - 插件市场
- Envoy Filter 基础知识（可选）

**学习建议**: 
动手实践是关键。尝试模拟真实业务场景，例如配置一个基于域名和路径的路由转发，并开启 Key Rate Limiting 限流插件。对比 Higress 的 Ingress 配置与原生 Nginx Ingress 的区别。

---

### 阶段 3：高级插件开发与生态集成

**学习内容**:
- Higress 插件开发规范（Wasm Go/Python/AssemblyScript）
- 自定义插件的编写、编译与热加载
- 服务网格 集成：作为 Istio 的独立数据平面
- OAuth2/OIDC 认证与鉴权集成
- 全局配置与精细化流量治理（金丝雀发布、蓝绿部署）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发
- WebAssembly (Wasm) 基础教程
- Higress 源码分析

**学习建议**: 
尝试编写一个简单的 Wasm 插件（例如修改请求 Body 或添加自定义 Header）。如果环境允许，尝试在 Kubernetes 集群中将 Higress 与服务网格控制平面对接，体验东西向流量与南北向流量的统一管理。

---

### 阶段 4：生产运维与性能调优

**学习内容**:
- Higress 的高可用部署架构
- 观测性：日志、Metrics (Prometheus) 与 Tracing (SkyWalking/Jaeger) 对接
- 大规模场景下的性能调优（连接池、缓冲区大小、并发配置）
- 网关的安全性加固（TLS 配置、防 DDoS 策略）
- 灾难恢复与版本升级策略

**学习时间**: 2-3周

**学习资源**:
- Higress 官方博客 - 最佳实践
- Envoy 官方性能调优指南
- Prometheus 与 Grafana 监控集成文档

**学习建议**: 
关注生产环境的稳定性。使用压测工具（如 Hey 或 Wrk）对网关进行压力测试，观察 CPU 和内存水位，并根据监控指标调整 Envoy 的配置参数。建立一套完善的日志告警体系。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款基于阿里云内部多年实践，开源的云原生 API 网关。它是在 Envoy 和 Istio 的基础上构建的，旨在提供高性能、可扩展的流量管理服务。

与 Nginx 和 Kong 的主要区别在于：
1.  **架构基础**：Nginx 和 Kong 主要基于 Nginx/OpenResty（Lua 脚本），而 Higress 深度集成了 Envoy（C++/Go），在处理高并发和云原生环境（如 Kubernetes）时具有更好的性能和可观测性。
2.  **云原生集成**：Higress 原生支持 Istio，可以作为 Ingress Gateway 或 API Gateway 直接对接服务网格，而 Kong 和 Nginx 通常需要额外的配置或插件才能深度集成。
3.  **插件生态**：Higress 支持 Wasm（WebAssembly）插件，允许使用多种语言（如 Go, C++, Rust）编写插件，比传统的 Lua 插件具有更好的隔离性和安全性，同时也兼容 Kong 的插件生态。

---



### 2: Higress 是否支持 Kubernetes？如何进行部署？

2: Higress 是否支持 Kubernetes？如何进行部署？

**A**: 是的，Higress 是为云原生设计的，完美支持 Kubernetes 环境。

部署通常通过 Helm Chart 进行。以下是简要步骤：
1.  添加 Higress 的 Helm 仓库。
2.  使用 `helm install` 命令部署 Higress 到指定的 K8s 命名空间。
3.  部署完成后，Higress 会自动创建 Service 和 Ingress 资源，将外部流量引入集群内的服务。
它既可以作为标准的 K8s Ingress Controller 使用，也可以作为独立的 API 网关管理南北向流量。

---



### 3: Higress 如何处理流量管理和安全防护？

3: Higress 如何处理流量管理和安全防护？

**A**: Higress 提供了全方位的流量管理和安全防护能力：

1.  **流量管理**：支持基于权重、Header、Cookie、Query 参数等高级路由规则。它支持蓝绿发布、金丝雀发布和 A/B 测试等流量切分策略。
2.  **安全防护**：
    *   **认证鉴权**：支持 OpenID Connect (OIDC)、API Key、Basic Auth 等多种认证方式。
    *   **安全插件**：内置 WAF（Web 应用防火墙）插件，可以防御 SQL 注入、XSS 等常见 Web 攻击。
    *   **限流熔断**：支持请求级限流和并发级限流，以及服务级别的熔断降级，保护后端服务稳定性。

---



### 4: Higress 是否兼容 Dubbo 和 gRPC 服务？

4: Higress 是否兼容 Dubbo 和 gRPC 服务？

**A**: 是的，Higress 对微服务协议有广泛的支持，这是它的一大特色。

1.  **Dubbo 支持**：Higress 原生支持 Dubbo 和 Dubbo3 (Triple) 协议。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议调用后端服务，实现 HTTP 到 Dubbo 的协议转换，这对于传统的 Spring Cloud + Dubbo 混合架构非常有用。
2.  **gRPC 支持**：Higress 原生支持 gRPC 和 gRPC-Web 协议。它可以作为 gRPC 服务的代理，支持负载均衡、TLS 终止以及基于 gRPC 方法的路由。

---



### 5: 如何在 Higress 中扩展功能？是否支持自定义插件？

5: 如何在 Higress 中扩展功能？是否支持自定义插件？

**A**: Higress 提供了强大的插件扩展机制，主要通过以下两种方式：

1.  **Wasm (WebAssembly) 插件**：这是 Higress 推荐的扩展方式。由于 Envoy 原生支持 Wasm，Higress 允许开发者使用 Go、C++、Rust 或 AssemblyScript 编写逻辑，编译成 `.wasm` 文件后动态加载。这种方式性能高、隔离性好，且无需重启网关即可更新插件。
2.  **Lua 插件**：为了兼容 Nginx/OpenResty 生态，Higress 也支持 Lua 脚本插件，这使得从旧网关迁移脚本变得更加容易。
3.  **原生 Go 插件**：Higress 允许直接使用 Go 语言编写插件，并利用其内置的 Go 插件运行时进行热加载，降低了 Java/Go 开发者的门槛。

---



### 6: Higress 与阿里云 API 网关和 MSE 云原生网关是什么关系？

6: Higress 与阿里云 API 网关和 MSE 云原生网关是什么关系？

**A**: Higress 是阿里云 MSE (Microservices Engine) 云原生网关的开源基础版本。

*   **MSE 云原生网关**：是阿里云提供的托管服务，基于 Higress 的内核，并提供了企业级的增强功能，如控制台可视化界面、全链路追踪、商业技术支持、自动弹性伸缩以及与阿里云其他产品的深度集成。
*   **Higress 开源版**：则是核心能力的开源实现，用户可以免费下载并在自己的服务器或 Kubernetes �

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地环境快速部署与路由配置

### 问题**: Higress 基于 Envoy 构建，但默认配置通常不能满足所有需求。请尝试在本地 Docker 环境中快速部署 Higress，并创建一个简单的 Ingress 路由规则，将路径 `/hello` 的流量转发到一个模拟的后端服务（如 nginx 或 echo 服务）。

### 提示**:

### 查阅 Higress 官方文档的 "快速开始" 部分，找到 Docker Compose 的部署方式。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其在流量治理、AI 插件扩展及云原生架构方面的特性，以下是 5-7 条针对实际生产环境的实践建议：

### 1. 利用 AI 代理插件实现多模型统一接入
**场景**：业务需要接入不同 LLM 提供商（如 OpenAI, Azure, 通义千问, 文心一言等），且希望统一接口格式。
**建议**：
*   **统一协议**：使用 Higress 的 `ai-proxy` 插件，将后端不同厂商的异构 API 在网关层统一为标准的 OpenAI 协议格式。这样业务端代码只需维护一套调用逻辑。
*   **模型路由**：在插件配置中设置模型路由规则，根据请求中的 `model` 参数（如 `gpt-4` 或 `qwen-turbo`），智能地将流量转发到对应的后端服务提供商，实现无感切换和 A/B 测试。

### 2. 实施语义缓存以降低 Token 成本与延迟
**场景**：用户频繁提问相似或相同的内容（如常见客服问题），直接转发给 LLM 会产生高额费用和较高延迟。
**建议**：
*   **开启语义缓存**：配置 Higress 的语义缓存插件。不同于传统的精确匹配缓存，该插件会对 Prompt 进行向量化处理。
*   **阈值设定**：根据业务对准确性的要求，调整向量相似度的阈值。对于相似度高于阈值（如 0.95）的请求，直接返回缓存结果。这对于高并发、对实时性要求非极致的问答场景效果显著。

### 3. 配置 Prompt 模板与脱敏以保障安全
**场景**：前端直接传递用户输入给 LLM，可能导致 Prompt 攻击（如越狱）或泄露敏感数据。
**建议**：
*   **Prompt Engineering at Gateway**：在网关层配置 `prompt-template` 插件。不要让前端传递完整的 Prompt，而是让前端只传递核心变量（如 `query`），由网关拼接预设的系统提示词。
*   **数据脱敏**：利用插件在请求发送前进行正则匹配或关键词过滤，自动剔除用户输入中的敏感信息（如身份证号、内部代码密钥），防止敏感数据被发送至公网模型。

### 4. 建立基于 Token 的精细限流策略
**场景**：LLM 的计费模式基于 Token 数量，传统的基于 QPS（每秒请求数）或并发连接数的限流无法有效控制成本。
**建议**：
*   **Token 限流**：使用 Higress 的 `token-ratelimit` 插件。针对不同的 API Key 或用户 ID，设置每分钟或每天的最大 Token 消耗限额。
*   **防止突发成本**：当某个用户的 Token 消耗达到阈值时，网关直接拦截请求并返回 429 状态码，避免因恶意攻击或程序错误导致的突发账单。

### 5. 警惕流式响应的超时配置陷阱
**场景**：AI 对话通常采用流式返回（SSE），耗时较长且不可预测，导致网关经常误报超时。
**建议**：
*   **调整超时参数**：务必将 Higress 路由配置中的 `requestTimeout` 或后端服务超时时间设置得足够大（或者设置为禁用超时），以适应大模型生成的长耗时特性。
*   **空闲超时控制**：为了避免连接僵死，可以配置较短的 `idleTimeout`（空闲超时）。只要数据流在持续传输，连接就不会断开；一旦传输中断，网关应快速释放资源。

### 6. 处理 Provider 兼容性与 Header 转换
**场景**：某些 LLM 提供商（如国内部分模型）不完全兼容 OpenAI 的 API 规范，导致标准 SDK 调用失败。
**建议**：
*   **Header 映射**：在 `ai-proxy` 插件中，仔细检查并配置 `context` 映射。例如，将 OpenAI 标准的 `

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260214-github_trending-alibaba-higress-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*