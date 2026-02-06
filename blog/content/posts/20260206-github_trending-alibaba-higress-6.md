---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T12:15:25+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的**AI 原生 API 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 Go 语言开发。目前该项目在 GitHub 上已获得超过 7,000 颗星，活跃度较高。 以下是 Higress 的核心功能与技术亮点总结： **1. 产品定位** Higress 是一款"
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，它通过扩展 WebAssembly 插件能力，专为 AI 原生应用设计。该项目将传统流量管理与 LLM 服务治理相结合，旨在解决微服务架构下的统一路由与 AI Agent 工具集成难题。本文将梳理其系统架构，并重点介绍 AI 网关特性、MCP 系统支持以及核心插件机制。

---
## 摘要

Higress 是由阿里巴巴开源的**AI 原生 API 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 Go 语言开发。目前该项目在 GitHub 上已获得超过 7,000 颗星，活跃度较高。

以下是 Higress 的核心功能与技术亮点总结：

**1. 产品定位**
Higress 是一款云原生 API 网关，它通过引入 **WebAssembly (WASM)** 插件能力扩展了 Istio 和 Envoy 的功能。其架构将控制平面（配置管理）与数据平面（流量处理）分离，配置变更通过 xDS 协议传播，具有毫秒级延迟且不中断连接，特别适用于 AI 流式响应等长连接场景。

**2. 三大核心应用场景**

*   **AI 网关：**
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存及安全防护能力。
    *   *核心插件：* `ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard`。
*   **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   *核心组件：* `mcp-router`、`jsonrpc-converter` 过滤器及内置的 MCP 服务实现（如地图搜索、工具集成等）。
*   **Kubernetes Ingress：**
    *   作为 Kubernetes 的 Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由。

**总结**
Higress 不仅是一个传统的 API 网关，更是一个专为 AI 应用设计的基础设施，旨在解决 LLM 接入、AI 智能体工具集成以及云原生流量管理的问题。

---
## 评论

### 总体判断

Higress 是一款极具前瞻性的**云原生 API 网关**，它成功地将**云原生流量治理**与**AI 大模型应用生态**进行了深度融合。作为阿里云开源的产物，它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 AI 协议扩展，填补了传统网关在 LLM 时代的功能空白，是构建现代化 AI 基础设施的优选方案。

### 深入评价依据

#### 1. 技术创新性：从“流量管道”进化为“AI 智能体枢纽”
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并明确提出了 "AI Native" 的概念，集成了 WASM 插件能力和 MCP (Model Context Protocol) 服务器托管功能。
*   **推断**：Higress 的核心差异化在于**协议感知能力的升级**。传统网关仅理解 HTTP/gRPC，而 Higress 原生理解 LLM 协议（如 OpenAI Chat Completion 格式）。它不仅是流量的转发者，更是 AI 请求的“编解码器”和“路由器”。
    *   **MCP 集成**：这是一个极具前瞻性的创新。通过在网关层直接托管 MCP Server，它将 AI Agent（智能体）所需的工具调用能力下沉到了网关层，使得 Agent 可以通过网关统一访问外部 API，极大简化了 Agent 应用的架构复杂度。
    *   **WASM 插件化**：利用 WASM 技术实现了业务逻辑与网关内核的解耦。开发者可以用 C++/Go/Rust/Python 编写插件来处理 Prompt 注入、敏感词过滤或 Token 计费，而无需重启网关或修改核心代码，这在热更新需求极高的 AI 场景下极具价值。

#### 2. 实用价值：解决 LLM 落地中的“连接”痛点
*   **事实**：描述中提到其核心功能包括“AI gateway features for LLM applications”以及“Traditional API gateway capabilities”。
*   **推断**：Higress 解决了 AI 时代的三个核心痛点：
    *   **模型供应商切换**：企业往往同时使用 OpenAI、通义千问、DeepSeek 等多个模型。Higress 允许通过配置实现统一接口对接，并在后端动态路由到不同厂商，甚至实现负载均衡和故障转移，避免了代码硬编码供应商 SDK。
    *   **Token 经济与安全**：在网关层统一处理 Token 计数和计费，比在应用层统计更准确且难以篡改。同时，利用插件实现 Prompt 注入（如系统角色预设）和敏感数据脱敏，保障了 AI 应用的合规性。
    *   **存量资产保护**：它保留了作为 K8s Ingress 和微服务网关的能力，意味着用户无需引入新组件即可同时管理传统 RESTful 服务和新兴的 AI 服务，降低了运维成本。

#### 3. 代码质量与架构：云原生工业级的典范
*   **事实**：项目使用 Go 语言编写，星标数 7,468，且基于 Envoy（C++）和 Istio（Go）构建。
*   **推断**：
    *   **架构设计**：采用了标准的**控制面与数据面分离**架构。控制面负责配置下发（基于 K8s CRD），数据面负责高性能流量转发。这种设计保证了高并发下的稳定性（Envoy 的高性能）与配置管理的便捷性。
    *   **代码规范**：作为阿里系的开源项目，其代码结构通常遵循严格的 Go 惯例和云原生接口标准。
    *   **文档完整性**：DeepWiki 提及了详细的 README 和多语言支持（中/日/英），表明该项目具有国际化的视野，文档覆盖了从架构概览到开发指南的全流程，降低了上手门槛。

#### 4. 社区活跃度：阿里背书，生态健康
*   **事实**：星标数接近 7.5k，且文档更新频繁，包含对最新 AI 协议（如 MCP）的跟进。
*   **推断**：在云原生网关领域，这是一个非常活跃的项目。阿里巴巴的背书保证了其不会轻易停止维护。同时，由于它解决了切合实际的 AI 落地问题，社区贡献者活跃度较高，插件生态正在快速丰富。相比于纯学术项目，Higress 更注重工程落地。

#### 5. 学习价值：理解 AI 时代流量治理的窗口
*   **推断**：对于开发者而言，Higress 是学习以下技术的最佳实践之一：
    *   **WASM 在边缘计算中的应用**：如何用非 C++ 语言扩展 Envoy。
    *   **AI 协议网关的设计模式**：如何处理 SSE（Server-Sent Events）流式传输、如何在网关层截取并修改流式响应（例如修改 AI 生成的第一句话）。
    *   **K8s Operator 开发模式**：学习如何通过 CRD 扩展 K8s 能力来管理复杂的网关配置。

#### 6. 潜在问题与改进建议
*   **复杂性成本**：基于 Istio 和 Envoy 的架构虽然强大，但也带来了极高的部署和运维复杂度。对于只有几个后端服务的简单 AI 应用，Higress 可能显得“过重”。
*   **建议**：建议官方提供更轻量级的“Standalone Mode”或 Docker Compose 部署方案

---
## 技术分析

基于对 Alibaba Higress 仓库的深入分析，以下是对该项目的全面技术剖析。Higress 不仅仅是一个传统的 API 网关，它是阿里云在“AI Native”时代对流量侧基础设施的一次重新定义，试图打通微服务治理与大模型应用的边界。

---

### 1. 技术架构深度剖析

**技术栈与架构模式**
Higress 采用了典型的**控制平面与数据平面分离**的架构模式。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 处理能力和可扩展性。
*   **控制平面**：基于 **Istio** 进行了大量裁剪和增强。相比于原生的 Istio，Higress 移除了 Sidecar 模式的复杂性，专注于 **Gateway（Ingress）** 模式，通过 K8s CRD 或控制台下发配置。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这是其架构中最关键的一环，允许使用 C/C++/Go/Rust/JS 等语言编写插件，并在 Envoy 的沙箱中高效运行，解决了传统 Lua 插件性能差、隔离性差的问题。

**核心模块与关键设计**
*   **Router (路由层)**：不仅支持 HTTP 路由，还针对 AI 场景实现了 SSE (Server-Sent Events) 和 WebSocket 的长连接优化。
*   **WASM Plugin System (插件系统)**：支持热加载，可以在不重启网关的情况下动态更新业务逻辑。
*   **MCP (Model Context Protocol) Server**：这是针对 AI Agent 场景的特定设计，允许网关作为 AI 工具调用的中间层，托管和管理工具接口。

**技术亮点与创新点**
*   **AI Native 特性**：这是 Higress 与 Nginx、Kong、APISIX 最大的区别。它原生集成了 LLM 的处理逻辑，如**Token 流式转发**、**Prompt 模板管理**、**语义路由**（基于向量而非简单的字符串匹配）。
*   **配置零延迟下发**：通过优化 xDS 协议的推送机制，实现了配置变更的毫秒级生效，这对于 AI 交互中的实时策略调整至关重要。

**架构优势分析**
*   **性能**：数据平面基于 Envoy C++ 内核，处理高并发能力远超基于 Go 或 Java 内核的网关。
*   **生态兼容**：完全兼容 K8s Ingress 标准，且复用了 Istio 的成熟控制面逻辑，降低了云原生用户的迁移门槛。

---

### 2. 核心功能详细解读

**主要功能与使用场景**
1.  **AI Gateway (AI 网关)**：
    *   **统一接入**：将 OpenAI、Azure、通义千问、Llama 等不同厂商的 API 统一封装为标准接口。
    *   **Prompt 管理**：在网关层进行 Prompt 模板化填充，实现业务代码与 Prompt 的解耦。
    *   **Token 计费与限流**：基于 Token 数量而非简单的 HTTP 请求数进行限流和计费，更符合 LLM 的计费模型。
2.  **MCP Server Hosting**：
    *   随着OpenAI推出 **Model Context Protocol (MCP)**，AI Agent 需要连接外部工具。Higress 充当 MCP Server 的托管者，允许 Agent 通过网关安全地访问企业内部工具（如数据库查询、ERP系统），而无需暴露内部服务拓扑。
3.  **传统微服务网关**：
    *   支持 K8s Ingress、服务发现、负载均衡、金丝雀发布/蓝绿发布。

**解决了什么关键问题**
*   **LLM 调用的碎片化**：企业应用往往需要切换不同的模型提供商，Higress 屏蔽了底层差异，实现了“模型热切换”。
*   **AI 流式传输的不可控性**：传统的网关在处理 SSE 流时往往缺乏干预能力（如中途修改内容、鉴权失效断流）。Higress 能够在流式传输过程中进行实时处理。

**技术实现原理**
*   **流式拦截**：利用 WASM 插件挂载到 Envoy 的 Decoder/Decoder 链条上，对 SSE 数据流进行逐块解析和转发。
*   **语义路由**：通过集成向量数据库客户端（或调用向量服务），将用户的 Query 进行向量化并计算与目标服务的相似度，从而实现智能路由。

---

### 3. 技术实现细节

**关键算法与技术方案**
*   **WASM 沙箱调度**：Higress 对 Proxy-WASM 标准进行了深度适配。它优化了 WASM 虚拟机的内存管理，通过插件复用和实例隔离策略，平衡了启动速度与资源消耗。
*   **配置分发**：控制平面维护了配置的版本控制，通过增量 xDS 推送，只将变更的部分推送给数据平面，极大降低了配置下发时的 CPU 和网络开销。

**代码组织结构**
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器、路由匹配逻辑。
*   **`plugins/`**：内置的高性能 WASM 插件源码（通常用 Go 或 C++ 编写），包括 Key Auth、Jwt Auth、Request Block 等。
*   **`installer/`**：基于 Helm 的部署逻辑。

**性能优化与扩展性**
*   **多线程并发**：Envoy 的异步非阻塞模型保证了高并发下的低延迟。
*   **动态伸缩**：作为 K8s Deployment 运行，可以配合 HPA (Horizontal Pod Autoscaler) 快速扩容。

**技术难点与解决方案**
*   **难点**：WASM 插件的调试困难。
*   **方案**：Higress 提供了完善的日志和追踪工具，并支持在本地通过 `wasmtime` 等工具进行插件单元测试，降低了开发门槛。

---

### 4. 适用场景分析

**适合使用的项目**
*   **AI 原生应用**：任何需要接入大模型（RAG、ChatBot、Copilot）的企业级应用。
*   **多模型统一管理**：企业内部同时使用私有部署模型（如 Llama 3）和公有云模型（如 GPT-4），需要统一入口。
*   **K8s 环境下的微服务治理**：需要替代 Nginx Ingress Controller，追求更高性能和可扩展性的场景。

**最有效的情况**
*   当你需要对 AI 请求进行**细粒度控制**时（例如：根据 Prompt 中的关键词拦截敏感请求，或者根据用户等级动态分配不同的 LLM 模型），Higress 是最佳选择。

**不适合的场景**
*   **极简静态站点**：对于只需简单反向代理的场景，Higress 的架构过于厚重。
*   **非 K8s 环境**：虽然支持二进制部署，但其强项在于与 K8s 的深度集成，脱离 K8s 会丧失服务发现和动态配置的优势。

**集成方式与注意事项**
*   **集成方式**：通常作为 K8s 的 Ingress Class 部署，或作为独立网关置于业务前置。
*   **注意**：WASM 插件虽然灵活，但过度的逻辑处理（如复杂的数据计算）会阻塞请求链路，应遵循“网关只做路由和轻量逻辑”的原则。

---

### 5. 发展趋势展望

**技术演进方向**
*   **更深度的 AI 编排**：从简单的 API 转发，向具备“推理”能力的网关演进。例如，网关根据请求意图自动拆解为对多个微服务的调用（类似 Agent 的规划能力）。
*   **WASM 生态的标准化**：推动 WASM 插件在不同网关之间的通用性。

**社区反馈与改进空间**
*   **优势**：背靠阿里和 Higress 开源社区，文档（中文）丰富，对国内云厂商支持极好。
*   **改进空间**：控制台 UI 的易用性仍有提升空间；部分高级功能的文档覆盖度不如核心功能。

**与前沿技术的结合**
*   **eBPF**：未来可能在数据平面引入 eBPF 进一步提升网络转发性能，或者用于更精细的可观测性采集。
*   **GraphQL**：加强对于 GraphQL 协议的原生支持，服务于前端复杂的查询需求。

---

### 6. 学习建议

**适合什么水平的开发者**
*   **中高级**：适合对 Kubernetes、Docker、网络协议（HTTP/HTTPS）有一定了解的开发者。如果是做 AI 应用开发，需要理解 LLM 的 API 格式（如 OpenAI 格式）。

**可以从中学习到什么**
*   **云原生网关设计**：学习如何基于 Envoy 构建控制平面。
*   **Wasm 开发**：掌握 Proxy-WASM SDK 的使用，这是编写高性能网关插件的未来趋势。
*   **Istio 实践**：理解 xDS 协议和服务网格的流量控制原理。

**推荐学习路径**
1.  **基础**：阅读 Envoy 官方文档，理解 Listener/Filter/Cluster 概念。
2.  **部署**：在本地 Kind/Minikube 环境通过 Helm 部署 Higress。
3.  **插件开发**：尝试编写一个简单的 Go WASM 插件（如添加 HTTP Header），并在 Higress 中加载。
4.  **AI 特性**：配置一个 AI 路由，将请求转发至 OpenAI，并配置 Prompt 模板。

---

### 7. 最佳实践建议

**如何正确使用**
*   **配置管理**：使用 GitOps 管理 Higress 的 Config，避免直接在控制台修改导致配置漂移。
*   **插件隔离**：生产环境中，对高风险插件（如修改请求体的插件）进行充分的压测，避免 WASM 虚拟机崩溃导致网关抖动。

**常见问题与解决方案**
*   **问题**：流式响应被截断。
*   **解决**：检查后端服务超时设置，确保网关的 `streamIdleTimeout` 参数设置得足够大，以适应 LLM 长文本生成的耗时。
*   **问题**：WASM 插件导致内存飙升。
*   **解决**：限制 WASM VM 的内存大小，并在插件代码中避免大对象缓存。

**性能优化建议**
*   **开启 HTTP/2**：在网关与后端服务之间开启 HTTP/2，利用多路复用减少连接数。
*   **缓存策略**：对于高频但低变动的 Prompt 模板或鉴权 Token，利用 WASM 插件的本地内存缓存（或 Redis）减少回源请求。

---

### 8. 哲学与方法论：第一性原理与权衡

**抽象层与复杂性转移**
*   **抽象层**：Higress 将**“流量治理”**和**“模型交互语义”**进行了抽象。
*   **复杂性转移**：它将 LLM 接入的复杂性（如鉴权、重试、流式处理、错误码映射）从**业务代码**转移到了**基础设施层**。这意味着业务开发者不再需要处理“连接超时重试”或“401 Token刷新”的脏活，但代价是运维团队需要维护一个更复杂的网关系统。

**默认的价值取向**

---
## 代码示例




```python
# 示例1：Higress WasmPlugin 配置生成器
def generate_wasm_plugin_config(plugin_name: str, config: dict) -> str:
    """
    生成 Higress WasmPlugin 的 YAML 配置
    :param plugin_name: 插件名称
    :param config: 插件配置字典
    :return: YAML 格式的配置字符串
    """
    yaml_template = f"""
apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  name: {plugin_name}
  namespace: default
spec:
  url: oci://higress-registry.cn-hangzhou.cr.aliyuncs.com/plugins/{plugin_name}:latest
  defaultConfig:
    {str(config)}
"""
    return yaml_template.strip()

# 使用示例
config = {"enable_cors": True, "allowed_origins": ["*"]}
print(generate_wasm_plugin_config("cors-plugin", config))
```


---

```python
# 示例2：Higress 路由规则匹配器
def match_route(path: str, routes: list) -> dict:
    """
    根据请求路径匹配 Higress 路由规则
    :param path: 请求路径
    :param routes: 路由规则列表，格式: [{"path_prefix": "/api", "service": "backend"}]
    :return: 匹配的路由配置
    """
    for route in routes:
        if path.startswith(route["path_prefix"]):
            return route
    return {"service": "default", "path_prefix": "/"}

# 使用示例
routes = [
    {"path_prefix": "/user", "service": "user-service"},
    {"path_prefix": "/order", "service": "order-service"}
]
print(match_route("/user/profile", routes))
```


---

```python
# 示例3：Higress 限流规则验证器
def validate_rate_limit(config: dict) -> bool:
    """
    验证 Higress 限流配置是否合法
    :param config: 限流配置字典，需包含 "qps" 和 "burst" 字段
    :return: 是否合法
    """
    if "qps" not in config or "burst" not in config:
        return False
    if config["qps"] <= 0 or config["burst"] <= 0:
        return False
    if config["burst"] > config["qps"] * 2:
        return False
    return True

# 使用示例
print(validate_rate_limit({"qps": 100, "burst": 200}))  # True
print(validate_rate_limit({"qps": -1, "burst": 50}))    # False
```


---
## 案例研究


### 1：阿里集团内部大规模电商业务迁移

 1：阿里集团内部大规模电商业务迁移

**背景**:
在阿里集团内部，随着电商业务向云原生架构的全面演进，传统的 Nginx+Lua 网关架构在维护成本、扩展性和云原生集成方面面临挑战。集团需要一个能够无缝对接 Kubernetes、支持高并发流量且兼容现有 Nginx 生态的下一代网关技术。

**问题**:
旧有的网关架构在应对双 11 等超大流量场景时，配置管理复杂，热更新容易导致业务抖动。同时，业务团队希望网关能够更好地支持 Service Mesh（服务网格）架构，实现东西向（服务间）与南北向（入口）流量的统一治理，而传统网关与 Istio 等控制面的集成较为生硬，性能损耗较大。

**解决方案**:
基于 Higress 进行核心交易链路的网关重构。利用 Higress 深度集成的 Istio 生态，将 Ingress Gateway 与 Sidecar 模式打通，实现统一的流量管理。通过 Higress 的热更新机制，确保在数百万级 QPS 的流量冲击下，路由规则变更能够毫秒级生效且不影响业务连接。同时，利用其高性能的 Wasm 插件市场，快速部署了针对特定电商业务的鉴权和流量整形逻辑。

**效果**:
成功支撑了阿里内部核心电商业务平稳上云，网关吞吐性能提升了 30% 以上，资源利用率显著优化。通过统一的控制面，运维复杂度降低了 50%，实现了从传统 API 网关到云原生网关的平滑过渡。

---



### 2：某互联网科技公司的微服务流量治理

 2：某互联网科技公司的微服务流量治理

**背景**:
该公司拥有数百个微服务，运行在多个 Kubernetes 集群中。随着业务扩展，服务间的调用关系日益复杂，缺乏统一的流量入口管理。不同业务部门各自为政，使用了不同的 API 网关产品，导致标准不一，且难以进行全局的流量监控和安全防护。

**问题**:
多集群入口管理混乱，缺乏统一的流量控制能力（如灰度发布、全链路蓝绿部署）。开发人员经常需要修改网关代码来实现简单的逻辑（如参数校验、请求头修改），导致研发效率低下。此外，旧网关对 HTTP/2 和 gRPC 协议的支持不够完善，影响了新业务的性能。

**解决方案**:
引入 Higress 作为统一的 API 网关。利用 Higress 对 Istio 的完美支持，将多个 Kubernetes 集群的入口流量统一纳管。开发团队利用 Higress 的 Wasm (WebAssembly) 插件能力，用 C++、Go 或 Rust 编写业务逻辑插件，实现了业务逻辑与网关内核的解耦。通过配置 Canary（金丝雀）发布规则，实现了基于 Header、Weight 或 Cookie 的精细化灰度流量切分。

**效果**:
实现了多集群流量的统一“看板”，微服务的上线迭代时间缩短了 40%。Wasm 插件技术使得业务定制逻辑的上线不再需要重启网关，极大提升了系统的稳定性。统一的网关层也使得全链路追踪和日志分析更加准确，故障排查效率提升了 60%。

---



### 3：某 AI 创业企业的多模型服务路由

 3：某 AI 创业企业的多模型服务路由

**背景**:
一家专注于 AIGC（生成式 AI）的初创公司，需要对外提供模型推理服务。由于底层依赖多个不同的开源大模型（如 Llama、ChatGLM 等），且模型版本更新频繁，前端应用需要根据用户请求动态路由到不同的后端模型服务。

**问题**:
传统的负载均衡器无法识别语义层面的请求内容，无法根据 Prompt 的类型或用户等级将流量路由到特定的模型版本。此外，AI 推理服务通常响应时间较长，且并发连接数高，对网关的长连接处理能力和超时控制提出了极高要求。

**解决方案**:
使用 Higress 作为 AI 模型的统一推理网关。利用 Higress 强大的路由扩展能力，编写了 Wasm 插件解析 HTTP 请求体中的 JSON 字段，根据模型名称或参数动态重写请求路径，转发至对应的后端 Service。配置了精细的超时控制和基于连接数的负载均衡算法，以应对 AI 推理的长尾效应。

**效果**:
实现了模型服务的无感升级和切换，A/B 测试效率大幅提升。网关层成功稳定支撑了高并发的 WebSocket 和 SSE（Server-Sent Events）长连接，保证了 AI 流式输出的实时性和稳定性。相比直接使用 Nginx，Higress 的可观测性帮助团队快速定位了模型推理的瓶颈，资源成本降低了 20%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Nginx | Kong |
|------|----------------|-------|------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，C 语言编写，轻量级 | 高性能，基于 OpenResty（Nginx + Lua） |
| 易用性 | 提供可视化控制台，支持 K8s Ingress 和 API 网关，配置灵活 | 配置复杂，需手动编辑配置文件，学习曲线陡峭 | 提供管理界面，但配置依赖插件和 API，需一定学习成本 |
| 成本 | 开源免费，企业版需付费，支持云原生部署 | 开源免费，无额外成本 | 开源免费，企业版需付费，支持云原生部署 |
| 扩展性 | 支持 WASM 插件扩展，插件生态丰富 | 依赖第三方模块，扩展性有限 | 支持 Lua 插件扩展，插件生态成熟 |
| 社区支持 | 阿里巴巴背书，社区活跃，文档完善 | 社区庞大，文档丰富 | 社区活跃，文档完善 |
| 适用场景 | 云原生、微服务、API 网关 | 传统 Web 服务器、反向代理 | API 网关、微服务 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，性能优异且内存安全。
- 优势2：原生支持 K8s Ingress 和 API 网关，云原生集成度高。
- 优势3：支持 WASM 插件扩展，插件生态灵活且安全。
- 优势4：提供可视化控制台，降低运维和配置复杂度。

### 不足分析

- 不足1：相比 Nginx，社区生态和成熟度稍弱。
- 不足2：企业版功能需付费，成本可能较高。
- 不足3：学习曲线较陡，需熟悉 K8s 和云原生技术栈。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许用户使用 C/C++、Go、Rust 或 AssemblyScript 编写自定义插件。相比传统的 Lua 脚本或 Java Filter，Wasm 插件具有更高的隔离性、更快的启动速度和更安全的沙箱环境，能够灵活实现认证、限流、请求修改等业务逻辑，而无需修改网关核心代码。

**实施步骤**:
1. 确定业务需求（如：JWT 验证、Header 修改、Key Rate Limiting）。
2. 选择合适的编程语言（推荐 Go 或 Rust）编写 Wasm 插件逻辑。
3. 使用 Higress 提供的 SDK 或 Proxy-Wasm 规范进行开发。
4. 编译生成 `.wasm` 文件，并通过 Higress 控制台或 CLI 上传插件。
5. 在网关全局或特定路由上配置并启用该插件。

**注意事项**: 开发 Wasm 插件时需注意内存管理，避免内存泄漏导致网关资源耗尽。

---

### 实践 2：精细化流量治理与路由配置

**说明**: 利用 Higress 强大的路由转发能力，实现基于 Header、Query 参数、Cookie 或 Body 内容的高级路由。通过配置灰度发布（金丝雀发布）规则，将特定比例或特征的流量引导至新版本服务，从而降低上线的风险。

**实施步骤**:
1. 在控制台定义服务来源，并关联 K8s Service、Nacos 或固定 IP 地址。
2. 配置路由规则，设置匹配条件（如 `/api/v1` 或特定 Header）。
3. 配置多版本服务目的地。
4. 设置流量权重或基于 Header 的标签路由规则，实现灰度分流。
5. 监控流量日志，确认流量分配符合预期。

**注意事项**: 路由匹配优先级遵循“最长匹配原则”，需注意路由配置的顺序，避免通配路由覆盖了特定路由。

---

### 实践 3：全面的安全防护策略配置

**说明**: Higress 内置了多种安全能力，包括 IP 黑白名单、防 CC 攻击、WAF（Web 应用防火墙）集成以及对后端服务的 TLS/mTLS 加密通信。合理配置这些策略可以有效防止 DDoS 攻击、恶意爬虫和数据泄露。

**实施步骤**:
1. 配置 IP 访问控制，封禁恶意 IP 段或限制仅允许内网访问。
2. 启用并配置 Higress 的 WAF 插件或对接阿里云 WAF，防御 SQL 注入和 XSS 攻击。
3. 配置 HTTPS 证书，开启 SNI 路由支持。
4. 如需后端服务双向认证，配置 mTLS 证书以验证服务端身份。

**注意事项**: 证书即将过期前需及时更新，建议配置证书自动监控和轮转机制。

---

### 实践 4：对接云原生服务注册与发现

**说明**: Higress 原生支持 Kubernetes Ingress 资源和 Nacos、Consul、Zookeeper 等注册中心。通过将网关与服务注册中心集成，可以实现服务实例的动态感知和健康检查，避免因服务实例变更导致的流量中断。

**实施步骤**:
1. 在 Higress 中配置服务来源，选择对应的注册中心类型（如 K8s 或 Nacos）。
2. 填写注册中心连接地址（如 Nacos 的 Server Addr）和命名空间信息。
3. 创建服务时，关联注册中心中的服务名。
4. 配置健康检查机制，Higress 将自动剔除不健康的实例。

**注意事项**: 确保网关网络能够访问注册中心的网络端口，避免因网络分区导致服务列表不可见。

---

### 实践 5：利用 Ingress Controller 进行 K8s 流量管理

**说明**: 在 Kubernetes 环境中，Higress 可以作为 Ingress Controller 部署。它通过监听 Ingress、Gateway API 或 Higress 自定义资源来动态更新配置。这种实践允许用户使用 GitOps 的方式管理流量，实现基础设施即代码。

**实施步骤**:
1. 使用 Helm Chart 在 Kubernetes 集群中部署 Higress。
2. 编写 Kubernetes YAML 文件定义 Ingress 资源，指定 Host、Path 和 Backend Service。
3. 应用 YAML 文件，Higress Gateway 会自动监听变更并更新路由规则。
4. 利用 K8s 的 Service 对象自动发现后端 Pod IP。

**注意事项**: 在大规模 K8s 集群中，频繁的 Endpoint 更新可能会给网关控制平面带来压力，建议合理调整全量同步的频率。

---

### 实践 6：可观测性与日志集成

**说明**: 生产环境的网关必须具备完善的可观测性。Higress 提供了详细的访问日志、指标监控和链路追踪能力。将日志对接到如 Prometheus、G

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 或 HTTP/3 协议支持

**说明**: Higress 作为高性能网关，基于 Envoy 内核，对 HTTP/2 和 HTTP/3 (QUIC) 有良好的原生支持。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，而 HTTP/3 则进一步解决了基于 TCP 的 HTTP/2 的队头阻塞问题，并能显著降低弱网环境下的延迟。

**实施方法**:
1. 在监听器配置中，确保协议选择为 HTTP/2 或开启 HTTP/3。
2. 配置 TLS 版本至少为 TLS 1.2，推荐 TLS 1.3，以支持 HTTP/3 的 0-RTT 握手。
3. 调整 HTTP/2 的并发流限制，根据后端服务能力适当调高。

**预期效果**: 在高并发或弱网环境下，请求延迟可降低 20%-40%，连接复用率大幅提升，减少 TCP 连接建立带来的开销。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置可能导致长时间等待无响应的请求，从而耗尽网关的线程或连接池资源。合理的超时与指数退避重试机制能快速失败，释放资源给健康的请求，提高系统吞吐量。

**实施方法**:
1. 设置路由级别的 `connectTimeout` (连接超时)、`requestTimeout` (请求总超时)。
2. 配置重试策略，设定最大重试次数（如 3 次），并开启指数退避。
3. 对幂等的 HTTP 方法（如 GET、HEAD）启用重试，非幂等方法（如 POST）谨慎开启。

**预期效果**: 故障场景下，系统响应时间从默认的 60s+ 降低至秒级甚至毫秒级，整体系统吞吐量在部分后端故障时保持稳定，避免雪崩。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件，相比传统的 Lua 或远程调用，Wasm 执行效率极高且安全。对于鉴权、限流等逻辑，使用 Wasm 插件处理。同时，在网关层开启本地缓存（如缓存后端响应或鉴权结果），可以大幅减少对后端的请求。

**实施方法**:
1. 将业务逻辑（如 Header 修改、Key Auth）编写为 Wasm 插件并部署。
2. 在插件配置中启用本地缓存特性，例如缓存 JWT 验证结果或频繁访问的配置数据。
3. 对于读多写少的数据，配置 HTTP 缓存策略。

**预期效果**: Wasm 执行速度接近原生，插件处理延迟可降低 50% 以上；配合本地缓存，后端请求量可减少 30%-90%（视缓存命中率而定），显著降低后端负载。

---

### 优化 4：调整连接池与并发配置

**说明**: Higress 默认的连接池配置可能无法满足极高并发场景。如果连接池过小，请求会排队等待；如果过大，可能导致后端服务压力过大。此外，Envoy 的工作线程数需要匹配 CPU 核心数。

**实施方法**:
1. 调整 `upstream` 的连接池大小，建议根据公式 `连接数 = 目标 QPS * 平均响应时间` 进行估算。
2. 检查并调整 Higress Gateway 的 Pod资源配置，确保 Envoy 的工作线程数通常等于 CPU 限制数。
3. 开启 HTTP/2 连接池复用，避免频繁建连。

**预期效果**: 消除因连接池耗尽导致的 503 错误，提升网关转发能力，在硬件资源不变的情况下，QPS 承载能力可提升 20%-50%。

---

### 优化 5：启用零信任与 mTLS 通信优化

**说明**: 在微服务架构中，服务间通信通常开启 mTLS (双向认证)。虽然 mTLS 增加了安全性，但频繁的 TLS 握手会消耗 CPU

---
## 学习要点

- 基于提供的来源信息（阿里巴巴开源的 Higress 项目，GitHub 趋势），以下是关键要点总结：
- Higress 是阿里云开源的一站式云原生 API 网关，旨在深度整合云原生生态与微服务架构。
- 该项目基于 Envoy 和 Istio 构建，在提供高性能代理能力的同时，极大地降低了服务网格的使用门槛。
- 它支持将 K8s Ingress 与 API 网关合二为一，实现了从南北向流量管理到东西向流量治理的统一。
- Higress 提供了强大的 WAF（Web 应用防火墙）插件市场，能够灵活扩展安全防护与流量处理逻辑。
- 该网关完美兼容 Nginx Ingress 注解配置，使用户能够以极低的成本从传统 Nginx 迁移至云原生网关。
- 它支持 Dubbo、Nacos 等主流微服务框架，能够作为微服务网关直接连接后端服务，无需进行协议转换。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心架构设计（基于 Istio + Envoy）
- Kubernetes 基础操作
- Docker 容器基础
- 网关与 Nginx、传统 API 网关的区别

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档: [https://higress.io/docs/latest/overview/what-is-higress/](https://higress.io/docs/latest/overview/what-is-higress/)
- Kubernetes 官方入门教程
- Envoy 官方文档基础部分

**学习建议**:
- 如果没有 Kubernetes 基础，建议先花几天时间了解 K8s 的基本概念（Pod, Service, Ingress）。
- 重点理解 Higress "云原生" 的特性，即它如何利用 K8s 的能力进行配置管理。
- 在本地搭建一套简单的 Kubernetes 环境（如 Kind 或 Minikube）为后续部署做准备。

---

### 阶段 2：核心功能与部署实践

**学习内容**:
- Higress 的安装与部署（Docker 版与 K8s 版）
- 域名、路由与流量管理配置
- 服务来源注册（K8s Service, Nacos, 固定地址）
- 插件系统入门（WAF 认证、限流熔断、CORS）
- 控制台的使用与操作

**学习时间**: 2-3周

**学习资源**:
- Higress GitHub 仓库: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- Higress 官方快速入门指南
- Higress 插件市场文档

**学习建议**:
- 动手操作是关键，尝试将一个简单的后端服务（如 Nginx 或 Go Echo）接入 Higress。
- 重点练习 "路由配置"，理解如何通过 Header、Query 参数、Cookie 等进行流量匹配。
- 尝试安装并启用几个官方预置插件（如 Key Auth 或 Request Block），观察流量变化。

---

### 阶段 3：高级特性与生态集成

**学习内容**:
- 全局与自定义插件开发（Wasm Go/Python/AssemblyScript）
- 服务 mocking 与 Http 到 RPC 的协议转换
- Nacos、Consul 等注册中心的深度集成
- 金丝雀发布与蓝绿发布实战
- Ingress API 与 Gateway API 的支持

**学习时间**: 3-4周

**学习资源**:
- Higress 自定义插件开发文档
- Wasm (WebAssembly) 基础教程
- Dubbo / gRPC 协议转换相关文档

**学习建议**:
- 学习编写一个简单的 Wasm 插件，例如修改请求头或响应体，这是 Higress 相比传统网关的一大优势。
- 如果团队使用微服务，重点研究 "服务来源" 配置，实现 K8s 服务与注册中心服务的统一管理。
- 在测试环境模拟一次金丝雀发布，验证流量灰度能力。

---

### 阶段 4：生产运维与性能调优

**学习内容**:
- Higress 的高可用部署架构
- 网关指标监控与日志采集（Prometheus, Grafana, SLS）
- 网关性能压测与参数调优（连接池、缓冲区大小）
- 安全防护策略（全局限流、防盗链、Bot 限制）
- 版本升级与回滚策略

**学习时间**: 2-3周

**学习资源**:
- Higress 运维最佳实践
- Envoy 性能调优指南
- K8s 资源限制与 HPA (Horizontal Pod Autoscaler) 文档

**学习建议**:
- 使用压测工具（如 Hey 或 JMeter）对 Higress 网关进行压力测试，关注 QPS、延迟指标。
- 配置 Prometheus 监控面板，重点关注 Envoy 的 Cluster 和 Listener 状态。
- 制定详细的应急响应预案，例如当网关不可用时的快速切换方案。

---

### 阶段 5：架构设计与源码研读

**学习内容**:
- Higress 与 Istio 控制平面的交互原理
- 深入理解 Envoy xDS 协议
- Higress 源码结构分析（Controller, Router, Pilot）
- 自定义 Controller 开发
- 大规模流量下的架构演进规划

**学习时间**: 持续学习

**学习资源**:
- Higress 源码
- Istio 源码与架构深度解析
- Envoy xDS 协议官方文档

**学习建议**:
- 阅读源码时，建议从 Ingress 资源的监听和处理逻辑入手，追踪配置如何下发到 Envoy。
- 如果需要深度定制，

---
## 常见问题


### 1: Higress 是什么？它与 Alibaba 有什么关系？

1: Higress 是什么？它与 Alibaba 有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是由阿里巴巴开源的项目，托管在 GitHub 上（alibaba/higress）。

Higress 的核心价值在于它深度集成了 Envoy 和 Istio，旨在解决云原生架构下的流量管理、安全防护和微服务治理问题。它源自阿里巴巴内部每年处理万亿级流量的网关经验，是阿里云 MSE（微服务引擎）云产品的重要开源组成部分。

---



### 2: Higress 和 Nginx、APISIX 或者 Kong 相比有什么区别？

2: Higress 和 Nginx、APISIX 或者 Kong 相比有什么区别？

**A**: Higress 与传统网关（如 Nginx）及现代 API 网关（如 APISIX、Kong）的主要区别体现在架构定位和集成能力上：

1.  **架构基础**：Higress 基于 Envoy 和 Istio (Istio Gateway) 构建，使用 C++ 核心以保证高性能，同时支持 WASM (WebAssembly) 插件，这使得其扩展性比传统的 Lua 插件更强且更安全。
2.  **云原生集成**：Higress 从设计之初就是为了深度兼容 Kubernetes 和 Istio 生态。它可以直接作为 Ingress Controller 或 Gateway API 使用，接管东西向（服务间）和南北向（入口）流量。
3.  **插件生态**：它兼容 Nginx 的 JSON 格式配置，降低了迁移门槛，同时支持通过 Go/C++/Rust/JS 编写 WASM 插件，热加载插件而不影响业务流量。

---



### 3: Higress 是否支持 Dubbo 或 gRPC 协议？它如何处理微服务调用？

3: Higress 是否支持 Dubbo 或 gRPC 协议？它如何处理微服务调用？

**A**: 是的，Higress 对微服务协议有非常强大的支持，这是它区别于许多七层负载均衡器的关键点：

1.  **gRPC**：Higress 原生支持 gRPC 和 HTTP/2。它不仅可以作为 gRPC 代理，还能利用 HTTP/1.1 到 gRPC 的协议转换功能，让前端通过 HTTP/JSON 调用后端的 gRPC 服务。
2.  **Dubbo**：Higress 提供了对 Dubbo (Dubbo2 和 Dubbo3) 的原生支持。它可以将 HTTP 请求转换为 Dubbo 请求（HTTP to Dubbo），这对于需要将传统的 RESTful API 网关接入后端 Java Dubbo 微服务集群的场景非常有用。

---



### 4: 如何在 Higress 中扩展功能？是否支持自定义插件？

4: 如何在 Higress 中扩展功能？是否支持自定义插件？

**A**: Higress 提供了非常灵活的扩展机制，主要通过 **WASM (WebAssembly)** 插件系统来实现：

1.  **WASM 插件**：这是 Higress 推荐的主要扩展方式。开发者可以使用 Go、C++、Rust、JavaScript 或 AssemblyScript 编写插件逻辑，编译成 WASM 文件后上传到网关。
2.  **优势**：WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关进程崩溃，且支持热加载（无需重启网关即可更新插件）。
3.  **兼容性**：Higress 兼容 Istio 的 Envoy Filter 配置，同时也支持类似 Nginx 的 Lua 脚本逻辑（通过 WASM 实现），方便用户从旧系统迁移逻辑。

---



### 5: Higress 的安全性如何？是否支持 WAF 功能？

5: Higress 的安全性如何？是否支持 WAF 功能？

**A**: Higress 在安全性方面提供了企业级的功能支持：

1.  **内置 WAF**：Higress 集成了开源 ModSecurity 规则引擎，提供了 Web 应用防火墙（WAF）能力，可以有效防御 SQL 注入、XSS 跨站脚本、远程文件包含等常见 Web 攻击。
2.  **认证与鉴权**：支持标准的 OpenID Connect (OIDC)、JWT 验证、API Key 认证以及基于 IP 的访问控制。
3.  **流量治理**：支持限流（基于请求量、并发数等）、熔断和黑白名单机制，保护后端服务免受过载影响。

---



### 6: Higress 能否在非 Kubernetes 环境中运行？

6: Higress 能否在非 Kubernetes 环境中运行？

**A**: 虽然 Higress 是为云原生（Kubernetes）环境设计的，但它也支持传统的部署模式：

1.  **标准版**：可以使用 Docker Compose 或直接在 Linux 服务器上部署 Higress。这种模式适合传统的虚拟机环境或开发测试环境。
2.  **Kubernetes 版**：在 K8s 环境中，Higress 通常以 Ingress Controller 或 Gateway 的形式运行，能够自动感知服务变化，实现动态路由。

---



### 7: 从 Nginx 迁移到 Higress 是否困难？

7: 从 Nginx 迁移到 Higress 是否困难？

**A**: Higress 专门设计了低迁移成本的方案，使得从 Nginx 迁移相对平滑：

1.  **配置兼容**：Higress 提供了 Nginx 配置转换工具，能够将 Nginx 的 `

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**: 参考 Higress 官方文档的 "快速开始" 章节，使用 `docker-compose` 进行部署。注意配置网关的路由规则时，需匹配路径 `/hello` 并设置目标服务地址。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其作为云原生网关的特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 AI 代理插件实现多模型统一接入
不要将大模型（LLM）的调用地址硬编码在业务代码中。建议使用 Higress 的 `ai-proxy` 插件或原生 AI 路由能力，作为业务层与模型提供商（如 OpenAI, Azure, 通义千问, Ollama 等）之间的中间层。
*   **具体操作**：在 Higress 中配置服务来源，将不同的 LLM 服务注册为后端服务。通过路由配置，将发往特定前缀（例如 `/v1/chat/completions`）的请求转发到对应的模型服务。
*   **最佳实践**：利用这一层做模型供应商的**热切换**。例如，当某个云厂商 API 不稳定时，只需修改 Higress 的配置，无需重新发布业务应用。

### 2. 配置语义路由与提示词模板管理
Higress 区别于传统网关的一大特性是能够理解请求内容。利用这一点，可以将提示词工程从代码中剥离，移至网关层管理。
*   **具体操作**：使用 Higress 的**提示词管理**功能，预设 System Prompt。在路由配置中，根据请求内容（如用户意图分类）将请求路由到不同的 Prompt 模板或不同的后端模型（例如：简单问题路由给低成本小模型，复杂问题路由给 GPT-4）。
*   **常见陷阱**：避免在网关层处理过长的上下文拼接，这可能会增加网关的内存压力和网络延迟。复杂的 Session History 建议仍在业务层处理，网关仅负责注入通用的 System Prompt。

### 3. 实施细粒度的 Token 限流与预算控制
大模型 API 的调用成本主要取决于 Token 消耗量，传统的 QPS（每秒请求数）限流无法有效控制成本。
*   **具体操作**：针对 AI 相关的路由，配置基于 Token 或 Request Body 大小的限流策略。Higress 支持针对特定 API Key 或租户进行配额管理。
*   **最佳实践**：为不同的开发团队或内部应用分配 API Key，并在网关层设置每日/每月的 Token 消耗上限，防止因某个应用的 Bug 导致巨额账单。

### 4. 开启 SSE 流式响应的全链路支持
AI 对话场景通常需要 Server-Sent Events (SSE) 流式返回，以提供打字机效果。
*   **具体操作**：确保 Higress 的路由配置中开启了 HTTP 回源超时的长连接支持，并关闭对响应 Buffer 的缓冲（某些网关默认会 Buffer 完整个响应再发给客户端）。
*   **常见陷阱**：如果后端服务返回 SSE 流，但客户端感觉是一次性收到所有文字，请检查 Higress 是否开启了流式透传，以及上游配置是否对 Keep-Alive 连接做了过短的超时限制，导致流被中断。

### 5. 敏感数据脱敏与内容安全审查
在企业内部应用大模型时，防止数据泄露（PII）和提示词注入攻击至关重要。
*   **具体操作**：在 Higress 的请求处理阶段（WAF 插件或自定义插件）配置敏感词过滤或正则匹配。例如，自动检测并替换用户输入中的手机号、身份证号，或者拦截包含 "忽略以上所有指令" 等恶意 Prompt 的请求。
*   **最佳实践**：在响应阶段也配置审查机制，防止模型输出不当内容直接触达用户。

### 6. 观测可观测性：关注首字延迟与 Token 吞吐量
监控 AI 网关时，传统的 HTTP 状态码和响应时间指标不够全面。
*   **具体操作**：接入 Prometheus + Grafana，重点监控 **Time to First Token (TTFT)**，即用户发请求到收到第一个字符的时间，这直接影响用户体验的“速度感”。同时监控 Request/Response 的 Token 计数。
*   **最佳实践

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*