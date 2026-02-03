---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-03T22:14:34+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "Kubernetes", "Istio", "Envoy", "WASM", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是一款由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 网关**（API Gateway）。目前该项目在 GitHub 上拥有超过 7,400 个星标。 以下是关于 Higress 的核心要点总结： **1. 产品定位与架构** Higress 是在 Istio 和 Envoy 之上构建的“AI"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "RAG应用", "云原生/容器"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI Gateway | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,442 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在通过云原生架构简化流量管理。它不仅提供传统的微服务路由能力，更集成了 LLM 应用网关与 MCP 服务器托管功能，帮助开发者在统一平台内高效处理 AI 服务接入与工具集成。本文将梳理其核心架构，并重点分析 WASM 插件机制及 AI 网关特性的具体实现。

---
## 摘要

Higress 是一款由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 网关**（API Gateway）。目前该项目在 GitHub 上拥有超过 7,400 个星标。

以下是关于 Higress 的核心要点总结：

**1. 产品定位与架构**
Higress 是在 Istio 和 Envoy 之上构建的“AI 原生”网关。它通过**控制面**（配置管理）与**数据面**（流量处理）分离的架构，利用 xDS 协议进行配置分发。这种设计使其能够在毫秒级延迟内完成变更，且不中断连接，非常适合需要保持长连接的 **AI 流式响应**场景。

**2. 核心功能与用途**
Higress 提供三大主要功能：
*   **AI 网关：** 为大语言模型（LLM）应用提供统一 API。它集成了 30 多家 LLM 提供商，支持协议转换、可观测性、缓存和安全防护。相关插件包括 `ai-proxy`、`ai-statistics` 等。
*   **MCP 服务器托管：** 托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。核心组件包含 `mcp-router` 和 `jsonrpc-converter`。
*   **Kubernetes Ingress：** 作为 K8s 的 Ingress 控制器，兼容 nginx-ingress 注解，提供传统的微服务路由能力。

**3. 技术特色**
*   **WASM 插件系统：** 利用 WebAssembly 技术，允许用户灵活扩展功能。
*   **云原生兼容性：** 深度集成 Kubernetes，支持云原生生态标准。

简而言之，Higress 是一个旨在连接传统微服务架构与新兴 AI 应用的高性能网关。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“云原生+AI”基础设施产品，它成功地将传统 API 网关的高性能流量治理能力与大模型（LLM）所需的语义处理与协议转换能力融合。作为阿里云开源的标杆项目，它不仅是微服务网关的有力竞争者，更是当前构建 AI Native 架构下最落地的网关解决方案之一。

**深入评价依据**

**1. 技术创新性：云原生与 AI 的深度融合**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并引入了 WASM（WebAssembly）插件系统。DeepWiki 明确指出其核心功能包括“AI gateway features for LLM applications”和“MCP server hosting”。
*   **推断**：传统的 API 网关（如 Kong, APISIX）主要处理 HTTP/gRPC 的负载均衡与鉴权，而 Higress 的差异化在于它原生理解 AI 语义。它不仅是流量的管道，更是 AI 业务的“调度器”。
    *   **协议转换**：它能将标准 HTTP/SSE 请求自动转换为不同 LLM 厂商（如 OpenAI, 通义千问）的异构 API 格式，解决了 AI 应用中多模型切换的痛点。
    *   **MCP (Model Context Protocol) 支持**：DeepWiki 提到的 MCP Server Hosting 是一大亮点。这意味着 Higress 可以直接作为 AI Agent 的工具提供者，让 LLM 能够安全、标准化地调用企业内部 API，这是对 AI Agent 基础设施的重要补充。
    *   **WASM 插件化**：利用 WASM 实现逻辑热加载，使得开发者可以用 C++/Go/Rust/AssemblyScript 编写高频逻辑（如 Prompt 模板注入、敏感词过滤），既保持了 Envoy 的高性能，又拥有了极高的扩展灵活性。

**2. 实用价值：解决 AI 落地的“最后一公里”问题**
*   **事实**：项目描述强调其为“AI Native API Gateway”，且星标数已达 7,442（截至数据统计时），说明市场关注度极高。
*   **推断**：Higress 解决了企业接入 AI 时的三个关键痛点：
    *   **统一模型接入**：企业无需为每个大模型单独写 SDK，通过 Higress 可统一管理 Prompt、Token 计费和限流。
    *   **安全与合规**：在企业内部，直接暴露 LLM API 存在泄露风险。Higress 可以作为网关进行统一的敏感数据脱敏和访问审计。
    *   **成本控制**：AI 流量成本高昂。Higress 继承了传统网关的流控能力，可以针对 Prompt 和 Response 进行精细化缓存（如语义缓存）或请求速率限制，直接降低 API 调用成本。

**3. 代码质量与架构：控制面与数据面分离的工业级设计**
*   **事实**：DeepWiki 提到架构“separates control plane (configuration management) from data plane (traffic processing)”，且支持 Kubernetes Ingress。
*   **推断**：
    *   **架构设计**：采用标准的控制面（Istio 扩展）与数据面（Envoy 扩展）分离架构。这种设计保证了极高的稳定性，数据面转发性能接近原生 Envoy，适合高并发场景。
    *   **Kubernetes 原生**：对于云原生用户，Higress 可以直接替换 K8s Ingress Controller，降低了迁移成本。其配置通过 CRD（Custom Resource Definition）管理，符合 GitOps 理念。
    *   **代码规范**：作为阿里系项目，Go 语言代码结构通常遵循高内聚低耦合原则，且文档提供了中日英三版，显示出对国际化和开发者体验的重视。

**4. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度曲线**：虽然功能强大，但同时掌握 Istio、Envoy、WASM 和 AI 协议概念的学习曲线较陡峭。对于仅需要简单 AI 代理的小团队，Higress 可能显得过于“重量级”。
    *   **AI 特性成熟度**：AI 领域迭代极快（如 Function Calling, Streaming Response 处理），网关对新协议的适配速度至关重要。建议关注其对于最新 LLM 特性（如 Video/Audio Input）的支持是否滞后。
    *   **资源消耗**：基于 Envoy 的网关在处理超长上下文（LLM Context）时的内存占用需要关注，特别是开启 Wasm 插件处理大量文本流时。

**5. 与同类工具对比**
*   **对比 APISIX/Kong**：传统网关通过插件支持 AI，但属于“后置适配”，在 AI 原生功能（如 Prompt 模板管理、MCP 协议）上不如 Higress 专注。
*   **对比 LangChain/LLMOps 平台**：LangChain 侧重于应用代码编排，Higress 侧重于流量入口和基础设施治理。两者是互补关系，而非竞争关系。

**边界条件与不适用场景**

*   **不适用场景**：
    *   极其简单的单体应用，无需复杂的流量治理。
    *   非 Kubernetes 环境（虽然支持 Docker，但功能会大打折扣）。
    *   需要极低延迟（微秒级）的纯内存网格通信（Envoy 虽快但仍有损耗）。

**快速验证清单**

1.

---
## 技术分析

# Higress 技术深度分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本报告将从技术架构、核心功能、实现细节、适用场景、发展趋势及工程哲学等维度进行全面剖析。

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的架构设计体现了**云原生**与**AI 原生**的深度融合。
*   **底层基座**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力和可观测性。
*   **控制平面**：深度集成 **Istio**，复用其 xDS（控制平面 API）配置分发机制，但剥离了 Istio 庞重的 Sidecar 治理逻辑，专注于 Gateway 流量管理。
*   **扩展层**：引入 **WebAssembly (WASM)** 技术栈。这是架构的核心亮点，允许使用 C/C++/Rust/Go (通过 TinyGo) 编写插件，并在 Envoy 的沙箱中运行。
*   **语言栈**：主体逻辑采用 **Go** 语言编写（控制面与配置管理），数据处理依赖 Envoy (C++)，插件支持多语言。

### 核心模块与设计
1.  **控制平面**：负责配置的接收、校验、转化，并通过 xDS 协议推送到数据平面。它实现了 Kubernetes Ingress Controller 的功能，能监听 CRD 变化。
2.  **数据平面**：基于 Envoy，处理实际流量。针对 AI 场景进行了优化，特别是对 SSE (Server-Sent Events) 和长连接的支持。
3.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM Runtime，实现了业务逻辑与网关内核的隔离。这解决了传统 Lua 插件崩溃导致网关崩溃的问题，并提供了近原生的执行性能。

### 架构优势
*   **配置热更新**：通过 xDS 协议实现毫秒级配置生效，且无需重启进程或断开连接，这对 AI 流式响应场景至关重要。
*   **解耦设计**：控制面与数据面分离，支持独立扩缩容。
*   **安全性**：WASM 沙箱机制隔离了第三方插件逻辑，防止恶意代码逃逸。

## 2. 核心功能详细解读

### 主要功能与关键问题解决
Higress 的核心定位是连接 AI 与微服务，主要解决以下问题：

1.  **AI 网关**：
    *   **问题**：大模型（LLM）调用缺乏统一标准，Token 计费复杂，流式输出难以缓存或拦截。
    *   **解决**：提供统一的 OpenAI 兼容接口，支持将不同厂商的 LLM API 转换为标准协议。内置 Token 统计、流式响应处理、以及基于语义的请求/响应修改。

2.  **MCP (Model Context Protocol) 网关**：
    *   **问题**：AI Agent 需要调用外部工具，但直接集成工具存在安全风险且难以管理。
    *   **解决**：Higress 可以作为 MCP Server 的托管端，对 Agent 访问外部工具的请求进行鉴权、审计和流量控制。

3.  **云原生 API 网关**：
    *   **问题**：Kubernetes Ingress 功能过于简单，企业级 API 管理需要认证、限流、熔断。
    *   **解决**：提供完整的 K8s Ingress 支持，同时兼容 Nginx Ingress 注解，降低迁移门槛。

### 与同类工具对比
*   **vs. Nginx/Kong**：Higress 基于 Envoy，内存占用极低，且 WASM 插件的开发语言和安全性优于 Lua（Kong/Nginx）。配置更新无需 Reload，连接不中断。
*   **vs. Istio Ingress**：Higress 专注于 Ingress 入口流量，去掉了 Sidecar 相关的庞杂配置，性能更高，运维更简单。
*   **vs. 专用 AI Gateway (如 OneGateway)**：Higress 将 AI 能力原生集成，而非通过插件外挂，这意味着对流式传输的处理更底层、更高效。

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件系统**：Higress 实现了 Proxy-WASM 规范。当请求到达时，Envory 加载 WASM 模块，通过 `on_request_headers`、`on_body` 等钩子函数介入流量处理。
*   **AI 流式处理**：在处理 LLM 的 SSE 流时，Higress 不是简单地透传，而是可以在流式传输过程中进行缓冲、截断或修改，这是传统网关难以做到的（传统网关通常只能处理一次性请求/响应）。
*   **配置分发**：使用 gRPC Stream 维持控制面与数据面的长连接，配置变更通过增量 xDS 推送，确保了在大规模路由情况下的稳定性。

### 性能与扩展性
*   **高并发**：Envory 的事件驱动模型配合 Go 的协程模型，使得 Higress 在单机上可轻松支撑数万 QPS。
*   **扩展性**：用户无需修改网关核心代码，只需编写 WASM 插件即可扩展功能。Higress 提供了 Wasm 插件市场，支持一键安装。

### 技术难点与解决
*   **难点**：WASM 的内存管理限制（沙箱特性）。
*   **解决**：Higress 优化了 Host Calls（宿主调用），允许插件安全地访问外部服务（如 Redis、配置中心），突破了 WASM 纯沙箱的限制。

## 4. 适用场景分析

### 最佳适用场景
1.  **LLM 应用统一接入**：企业内部有多个业务线调用不同厂商的大模型，需要统一进行 Token 管理、鉴权和流量控制。
2.  **微服务 K8s Ingress**：需要高性能、支持热更新且具备丰富扩展能力的云原生入口网关。
3.  **AI Agent 基础设施**：需要构建 Agent 应用，且需要安全地暴露内部工具（MCP 协议）给大模型调用。

### 不适合场景
1.  **极简静态站点**：对于仅需简单反向代理的场景，Higress 的资源开销（基于 K8s 和 Envoy）相对 Nginx 较重。
2.  **非 K8s 环境**：虽然支持 Docker 部署，但其强大之处在于与 K8s 的深度集成，脱离 K8s 会丧失动态服务发现等核心优势。

### 集成注意事项
*   **资源限制**：WASM 插件虽然安全，但频繁的 Host Call 会引入延迟，建议将重逻辑（如复杂鉴权）放在外部服务，插件仅做转发或轻量计算。

## 5. 发展趋势展望

### 演进方向
*   **AI 原生深化**：未来将更深入地支持 RAG（检索增强生成）流程，可能内置向量数据库连接能力或 Prompt 模板管理。
*   **MCP 生态标准化**：随着 MCP 协议的普及，Higress 有望成为企业内部 MCP Server 的标准路由网关。
*   **边缘计算**：由于 WASM 的轻量级特性，Higress 有潜力向边缘节点下沉，作为边缘 AI 推理的入口。

### 社区与改进
*   目前社区活跃度较高，主要迭代集中在 AI 特性上。改进空间在于 WASM 插件的调试工具链仍需完善，以及对传统 Dubbo/SOFA 等RPC协议的深度支持。

## 6. 学习建议

### 适合开发者
*   具备 **Kubernetes** 基础的后端工程师。
*   对 **Service Mesh (Istio)** 和 **云原生** 技术感兴趣的开发者。
*   需要落地 **LLM 应用**的架构师。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念和 xDS 协议。
2.  **入门**：阅读 Higress 官方文档，部署一个 Demo 集群，配置 Ingress 路由。
3.  **进阶**：学习 Proxy-WASM 规范，尝试使用 Go 或 Rust 编写一个简单的鉴权插件。
4.  **实战**：配置一个 LLM 路由，实现 OpenAI 格式到阿里云通义千问的转换。

## 7. 最佳实践建议

### 正确使用方式
*   **配置管理**：使用 K8s CRD (`Ingress`, `Gateway`, `WasmPlugin`) 进行配置管理，而非直接操作 Envoy 配置文件。
*   **插件开发**：优先复用社区插件，自定义插件时务必限制内存使用，避免 OOM。
*   **观测性**：利用内置的 Prometheus 指标和 Access Log，重点监控 WASM 插件的延迟。

### 常见问题
*   **流式响应中断**：检查后端服务超时设置，确保网关的超时时间大于 LLM 生成时间。
*   **插件加载失败**：通常是由于 WASM 编译目标架构（x86_64/ARM64）与运行环境不匹配。

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**流量处理**的抽象层上做了一次大胆的尝试：将**业务逻辑的扩展点**从传统的“代码库”转移到了“沙箱插件”。
*   **复杂性转移**：它把“如何修改网关行为”的复杂性从“重新编译 C++/Nginx 模块”转移给了“编写 WASM 代码”。这降低了**运维**的复杂性（不需要重新构建网关镜像），但略微增加了**开发**的复杂性（需要适应 WASM 的限制环境）。

### 价值取向与代价
*   **价值取向**：**可扩展性 > 简单性**，**安全性 > 灵活性**。
*   **代价**：为了获得 WASM 的安全隔离，牺牲了一部分原生 C++ 插件的极致性能（尽管差异很小）。为了支持 AI 的流式特性，增加了协议解析的复杂度。

### 工程哲学
Higress 的范式是**“网关即平台”**。它不再仅仅是一个流量的管道，而是一个流量的**计算平台**。
*   **易误用点**：开发者容易在 WASM 插件中编写阻塞式代码（如直接调用同步 HTTP 请求而不处理超时），这会阻塞 Envoy 的事件循环，导致网关性能急剧下降。

### 可证伪的判断
1.  **性能判断**：在开启 10 个复杂 WASM 插件的情况下，Higress 的 P99 延迟增加幅度应低于 20%，且内存占用增长应线性可控，否则证明其 WASM 运行时调度存在瓶颈。
2.  **AI 流式判断**：在处理 LLM 流式响应时，Higress 应能在不中断连接的情况下，基于响应体的前 N 个 Token 动态修改 Header 或截断连接，这验证了其“流式处理”能力的真实性。
3.  **配置一致性**：在每秒 100 �

---
## 代码示例




```python
# 示例1：使用Higress实现动态路由配置
def configure_dynamic_route():
    """
    解决问题：根据请求头动态路由到不同服务
    场景：多租户系统需要根据租户ID路由到不同后端
    """
    from higress import RouteConfig
    
    # 创建路由配置
    route = RouteConfig()
    
    # 添加基于请求头的路由规则
    route.add_header_based_route(
        header_name="X-Tenant-ID",
        routes={
            "tenant1": "http://service1:8080",
            "tenant2": "http://service2:8080",
            "default": "http://default-service:8080"
        }
    )
    
    # 应用配置
    route.apply()
    return "动态路由配置已应用"

# 说明：这个示例展示了如何使用Higress的Python SDK配置动态路由，
# 根据请求头中的租户ID将流量路由到不同的后端服务，实现多租户隔离。

```python


def canary_deployment():
"""
解决问题：逐步将流量切换到新版本服务
场景：新服务版本灰度发布，需要逐步增加流量
"""
from higress import TrafficSplit
# 创建流量分割配置
split = TrafficSplit()
# 设置金丝雀规则：20%流量到新版本
split.set_canary(
new_version="http://v2-service:8080",
old_version="http://v1-service:8080",
weight=20  # 20%流量
)
# 应用配置
split.apply()
return "金丝雀发布配置已应用"
# 通过设置流量权重，将20%的流量引导到新版本服务，
# 逐步验证新版本的稳定性。

```python
# 示例3：实现请求限流和熔断
def rate_limit_and_circuit_breaker():
    """
    解决问题：保护后端服务免受过载影响
    场景：API服务需要限制每秒请求数并实现熔断
    """
    from higress import ProtectionPolicy
    
    # 创建保护策略
    policy = ProtectionPolicy()
    
    # 设置限流：每秒100个请求
    policy.set_rate_limit(
        requests_per_second=100,
        burst=20  # 允许突发20个请求
    )
    
    # 设置熔断：错误率超过50%时触发
    policy.set_circuit_breaker(
        error_threshold=50,  # 50%错误率
        min_requests=10,     # 至少10个请求才计算
        open_duration=60     # 熔断持续60秒
    )
    
    # 应用策略
    policy.apply()
    return "限流和熔断策略已应用"

# 说明：这个示例展示了如何使用Higress配置服务保护策略，
# 包括限流(100 QPS)和熔断(错误率超过50%时触发)，
# 保护后端服务免受过载和故障影响。


---
## 案例研究


### 1：阿里巴巴集团内部核心业务（如淘宝、天猫等）

 1：阿里巴巴集团内部核心业务（如淘宝、天猫等）

**背景**:  
在阿里巴巴庞大的电商生态系统中，流量洪峰是常态，特别是在“双11”等大促期间，每秒峰值请求量可达数十万甚至百万级。传统的 API 网关在处理如此大规模的南北向流量以及微服务间的东西向流量时，面临着巨大的性能挑战和扩展性瓶颈。原有的网关架构在应对复杂路由、安全认证和流量控制时，资源消耗过高且迭代速度较慢。

**问题**:  
1. 高并发下的性能瓶颈：传统网关在处理 TLS 卸载、复杂路由规则和全链路鉴权时，延迟较高，无法满足极致的低延迟要求。  
2. 架构僵化：旧系统难以快速支持新业务（如直播带货、国际化业务）的特定协议和路由需求。  
3. 成本与效率：维护多套网关系统（Nginx、Zuul 等）导致运维复杂度高，且资源利用率不均衡。

**解决方案**:  
阿里巴巴基于内部多年的网关经验，研发并开源了 **Higress**。Higress 是一个基于 Istio 和 Envoy 构建的云原生 API 网关。在内部实践中，阿里将 Higress 部署于 Kubernetes 集群之上，利用其高性能的异步非阻塞架构处理流量。

1. **统一网关层**：将原本分散的流量入口收敛至 Higress，统一管理南北向（外部客户端到服务）和东西向（服务间调用）流量。  
2. **插件生态**：利用 Higress 的 Wasm 插件机制，在网关层实现了动态的请求鉴权、流量整形和请求/响应修改，无需重启网关即可更新业务逻辑。  
3. **服务治理集成**：深度集成 Nacos 注册中心和 MSE (Microservices Engine) 云原生服务治理体系，实现了无损上下线和全链路灰度发布。

**效果**:  
1. **性能提升**：在保持高可用性的前提下，Higress 成功支撑了双11期间的峰值流量，单核 QPS 性能相比旧架构提升显著，长连接处理能力大幅增强。  
2. **资源成本优化**：通过极致的性能优化，在同等流量规模下，网关层的计算资源成本降低了约 30%。  
3. **研发效率提升**：业务团队可以通过编写 Wasm 插件快速迭代网关逻辑，业务上线周期从周级缩短至天级。

---



### 2：某头部互联网 AI 客服 SaaS 平台

 2：某头部互联网 AI 客服 SaaS 平台

**背景**:  
该客户是一家提供智能客服解决方案的 SaaS 企业，其系统架构部署在阿里云 ACK (Alibaba Cloud Container Service for Kubernetes) 上。随着大模型（LLM）应用的兴起，其业务逻辑从传统的规则匹配转变为对 LLM 的频繁调用。由于 LLM 调用耗时较长（通常为数秒），且后端服务扩容速度跟不上流量增长，导致网关层频繁出现超时和拥堵。

**问题**:  
1. 长连接与超时控制：传统的 Nginx Ingress 在处理 LLM 这种高延迟、长耗时的流式请求时，连接池容易耗尽，导致客户端请求失败。  
2. 后端保护不足：当后端 AI 推理服务负载过高时，网关未能有效进行排队和限流，导致雪崩效应，影响整个系统的稳定性。  
3. 鉴权复杂度：SaaS 租户需要精细化的 API Key 鉴权和流量配额管理，传统配置方式繁琐且容易出错。

**解决方案**:  
该客户将流量入口从 Nginx Ingress 迁移至 **Higress**，并利用其针对 AI 场景的特性和云原生能力进行了改造。

1. **AI 原生网关特性**：利用 Higress 对 SSE (Server-Sent Events) 和流式传输的深度支持，优化了与 LLM 服务的交互模式，确保长连接稳定。  
2. **后端服务保护**：配置 Higress 的“请求排队”和“自动重试”策略。当后端繁忙时，Higress 在网关层对请求进行缓存和排队，而非直接拒绝，平滑了流量尖刺。  
3. **动态鉴权插件**：开发并部署了基于 Wasm 的鉴权插件，对接内部的租户管理系统，实现了毫秒级的 API Key 校验和租户级别的限流配额控制。

**效果**:  
1. **系统稳定性提高**：在 LLM 服务响应延迟波动剧烈（甚至达到 10s+）的情况下，网关层的请求成功率保持在 99.9% 以上，有效防止了连接耗尽。  
2. **用户体验优化**：流式响应的卡顿现象大幅减少，终端用户在使用 AI 对话功能时的交互流畅度显著提升。  
3. **运维简化**：通过 Higress 控制台即可动态调整限流阈值和鉴权规则，无需重新加载配置，运维效率提升 50% 以上。

---



### 3：某跨国物流企业混合云架构改造

 3：某跨国物流企业混合云架构改造

**背景**:  
该企业业务遍布全球，其 IT 架构正处于从传统虚拟机向 Kubernetes 容器化迁移的阶段。在过渡期内，业务同时运行在阿里云（公有云）和自建的本地数据中心（私有云）中。由于网络环境复杂，跨云调用经常出现延迟高、丢包等问题，且缺乏统一的流量入口来管理分布在两地的服务。

**问题**:  
1. 多云流量管理困难：公有云和私有云各有一套入口，配置不一致，导致全局流量视图（GSLB）难以实现，跨地域访问路由逻辑复杂。  
2. 安全合规风险：跨云传输缺乏统一的安全策略，难以实施统一的 mTLS（双向认证）加密传输。  
3. 迁移割接风险：在将流量从旧架构逐步切换到新架构时，需要具备精细化的流量权重控制能力，以实现金丝雀发布。

**解决方案**:  
企业引入 **Higress** 作为统一的云原生 API 网关，部署在混合云环境中，打通了两个网络区域。

1. **统一流量入口**：在阿里云和本地数据中心分别部署 Higress，并结合 DNS 或全局负载均衡，实现了流量的统一接入。  
2. **多集群管理**：利用 Higress 与 Istio 的兼容性，将不同集群的服务注册到统一的控制平面，实现了跨集群的服务

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高流量场景 | 极高性能，基于 Nginx 和 Lua，性能优于 Kong |
| 易用性 | 提供图形化控制台和 K8s 集成，配置简单 | 配置灵活，但学习曲线较陡 | 配置复杂，需要较多手动操作 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 完全开源免费，无企业版 |
| 扩展性 | 支持插件扩展，但生态较新 | 丰富的插件生态和第三方扩展 | 插件生态丰富，支持自定义开发 |
| 社区支持 | 社区活跃度中等，背靠阿里巴巴 | 社区成熟，文档丰富 | 社区活跃，中文支持友好 |
| 适用场景 | 云原生、微服务、API 网关 | 传统 API 网关、微服务 | 云原生、微服务、高性能 API 网关 |

### 优势分析

- **性能优势**：基于 Rust 和 Go 开发，内存占用低，处理高并发请求能力强。
- **云原生集成**：深度集成 Kubernetes，支持服务网格和云原生架构。
- **易用性**：提供图形化控制台，降低配置和管理难度。
- **背靠阿里巴巴**：技术支持和稳定性有保障，适合企业级应用。

### 不足分析

- **生态较新**：相比 Kong 和 APISIX，插件和第三方扩展较少。
- **社区活跃度**：社区规模和文档丰富度不如 Kong 和 APISIX。
- **学习曲线**：对于不熟悉 Rust 或 Go 的开发者，定制开发可能有一定难度。
- **企业版成本**：高级功能需付费，可能增加长期使用成本。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Istio 进行渐进式网关迁移

**说明**: Higress 深度集成了 Istio，可以作为 Ingress Gateway 或 Egress Gateway 使用。对于已经在使用 Istio 的企业，Higress 提供了更强大的南北向流量处理能力。通过将 Higress 接入现有的 Istio 集群，可以在保持东西向（服务间）流量治理的同时，获得高性能的入口流量管理。

**实施步骤**:
1. 确保现有集群已安装 Istio 控制面。
2. 部署 Higress，并配置其连接到现有的 Istio Pilot（Discovery Service）。
3. 在 Kubernetes 中创建或更新 Gateway 资源，将 `.spec.servers` 的端口由 Istio Ingress Gateway 切换为 Higress 监听端口。
4. 逐步将 DNS 流量或 LoadBalancer 指向 Higress 服务 Pod。

**注意事项**: 确保 Higress 版本与底层 Istio 控制面版本的 API 兼容性，避免出现配置解析错误。

---

### 实践 2：利用 Wasm 插件扩展网关业务逻辑

**说明**: Higress 原生支持 WebAssembly (Wasm)，允许开发者使用 C++, Go, Rust, Python 或 JavaScript 编写插件来扩展网关功能。相比传统的 Lua 脚本或硬编码方式，Wasm 插件提供了沙箱隔离、高性能以及更灵活的代码热更新能力，非常适合实现自定义的鉴权、请求头修改或流量染色逻辑。

**实施步骤**:
1. 使用 Higress 官方提供的 SDK（如 Go-Wasm-SDK）开发业务逻辑插件。
2. 将插件编译为 `.wasm` 文件。
3. 在 Higress 控制台或通过 CRD (`WasmPlugin`) 上传插件。
4. 配置插件的作用域（全局、特定路由或特定域名）及执行阶段。

**注意事项**: Wasm 插件虽然执行效率高，但应避免编写阻塞时间过长的代码（如复杂的大规模正则匹配），以免影响网关整体吞吐量。

---

### 实践 3：构建高可用的网关热备架构

**说明**: 在生产环境中，网关的高可用性至关重要。Higress 支持多副本部署，利用 Kubernetes 的 HPA（水平自动伸缩）应对流量突发。同时，应结合健康检查机制，确保流量不会转发到处于异常状态的网关实例。

**实施步骤**:
1. 在 Kubernetes Deployment 中设置 `replicas` 至少为 3，并配置反亲和性规则，使 Pod 分散在不同的节点上。
2. 配置 Kubernetes 的 `readinessProbe` 和 `livenessProbe`，使用 `/health` 接口进行检测。
3. 为 Higress Service 配置 `externalTrafficPolicy: Local`（如果使用外部负载均衡器），以保留源客户端 IP 并避免二次转发。
4. 启用 HPA，根据 CPU 或内存使用率自动调整副本数。

**注意事项**: 在配置 `externalTrafficPolicy: Local` 时，需确保后端服务能够处理 Pod 分布不均导致的潜在负载波动。

---

### 实践 4：精细化配置流量路由与负载均衡

**说明**: Higress 兼容 Nginx Ingress 的注解，并支持 Istio 的 VirtualObject 配置。最佳实践是充分利用其强大的路由匹配能力（如基于 Header、Cookie、权重路由）来实现蓝绿发布或金丝雀发布，同时配置合适的负载均衡策略以优化后端服务压力。

**实施步骤**:
1. 定义 `VirtualService` 资源，配置 `http` 匹配规则。
2. 使用 `match` 字段配置特定条件（如 `uri.prefix` 或 `headers`）。
3. 在 `route` 字段中设置 `destination` 权重，实现流量按比例切分（例如 90% 流量走 v1 版本，10% 走 v2 版本）。
4. 根据业务需求，在 `DestinationRule` 中设置负载均衡策略（如 `ROUND_ROBIN` 或 `LEAST_CONN`）。

**注意事项**: 权重路由仅对 HTTP/gRPC 流量有效，对于 TCP 流量需要使用不同的配置策略。

---

### 实践 5：启用全链路安全防护与认证

**说明**: Higress 提供了完善的安全体系，包括对接 OIDC（OpenID Connect）进行身份认证、配置 IP 黑白名单以及启用 HTTPS。最佳实践是强制所有对外服务开启 TLS 加密，并针对内部管理接口启用严格的身份验证。

**实施步骤**:
1. 在网关配置中挂载 SSL 证书，强制监听 443 端口并自动跳转 HTTP 到 HTTPS。
2. 创建 `RequestAuthentication` 策略，配置 JWT 或 OIDC 验证规则。
3. 使用 Higress 的 IP 访问控制插件（或 `AuthorizationPolicy`），限制特定网段的访问。
4. 定期轮换

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**:
Higress 基于 Envoy 构建，原生支持 HTTP/2 和 HTTP/3。对于高并发或弱网环境，HTTP/2 的多路复用可以减少 TCP 连接数，降低握手开销；HTTP/3 (QUIC) 基于 UDP，能有效解决 TCP 队头阻塞问题，显著降低连接建立延迟和丢包时的重传延迟。

**实施方法**:
1. 在 Higress 控制台或网关配置中，确保监听器协议设置为 `HTTP/2` 或 `HTTP/3`。
2. 如果配置了 TLS，确保 ALPN 协议协商包含 `h2` 和 `h3`。
3. 对于上游服务连接，同样推荐配置 HTTP/2 协议以利用连接池复用。

**预期效果**:
在高并发场景下，TCP 连接数可减少 50%-80%；在弱网环境下，请求延迟降低 20%-30%。

---

### 优化 2：配置全局限流与熔断降级

**说明**:
防止后端服务因突发流量导致雪崩。Higress 支持精细化的流量防护，通过限制每秒请求数 (RPS) 或并发数来保护系统。当后端服务响应变慢或错误率升高时，自动触发熔断，快速返回失败，避免线程阻塞。

**实施方法**:
1. 在路由或域名级别配置 `Request Limit`，设定阈值（如 1000 QPS）。
2. 配置 `Service Fallback` 或 `Retry Policy`，设定连续 5xx 错误的阈值触发熔断。
3. 结合 Sentinel 规则配置更细粒度的流控规则（如果集成了 Sentinel）。

**预期效果**:
将系统最大可用容量维持在 90%-95% 水平而不崩溃；在故障发生时，错误响应延迟从超时（如 60s）降低至毫秒级（< 10ms）。

---

### 优化 3：启用 DNS 缓存与服务发现优化

**说明**:
频繁的 DNS 查询会增加网络延迟。Higress (基于 Envoy) 默认会缓存 DNS 结果，但优化 TTL 设置和上游服务发现机制（如 Nacos）的配置可以减少因 DNS 解析失败或过期导致的连接抖动。

**实施方法**:
1. 检查 Higress 的 Bootstrap 配置，调整 `dns_resolvers` 的 `dns_refresh_rate`，避免过于频繁的刷新。
2. 如果对接 Nacos 或注册中心，确保服务变更推送是实时的，减少全量拉取。
3. 对于静态上游服务，配置静态 IP 地址而非域名，完全绕过 DNS 查询。

**预期效果**:
减少因 DNS 解析产生的 10ms-50ms 偶发延迟；降低因 DNS 解析失败导致的 5xx 错误率。

---

### 优化 4：优化 WAF 插件与自定义插件执行效率

**说明**:
Higress 支持通过 Wasm (WebAssembly) 运行自定义插件和 WAF 规则。复杂的正则匹配或低效的 Lua/Wasm 代码会显著增加请求处理的 CPU 时间和延迟。

**实施方法**:
1. 审查 WAF 规则，将高开销的正则表达式置底或优化为更高效的匹配逻辑。
2. 对于自定义插件，优先使用 Go 或 C++ 编译为 Wasm，而非使用解释型语言（如旧版 Lua）。
3. 利用 Higress 的 `Plugin` 生命周期钩子，避免在 `onLog` 阶段执行重逻辑，尽量在 `onHttpRequestHeaders` 完成决策。
4. 启用插件缓存，避免重复计算。

**预期效果**:
在开启 WAF 或复杂鉴权场景下，网关处理延迟可降低 20%-40%，CPU 使用率下降 10%-20%。

---

### 优化 5：调整连接池与超时参数

**说明**:
默认的连接池大小和超时设置

---
## 学习要点

- 基于提供的 GitHub 趋势来源信息（Alibaba/Higress），以下是关于该项目最核心的 5 个关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 容器环境。
- 项目提供了强大的流量治理能力，支持金丝雀发布、蓝绿部署及负载均衡等复杂路由规则。
- 内置了对高并发流量的处理支持，并集成了 WAF（Web 应用防火墙）插件以增强安全性。
- 兼容 Nginx Ingress 注解，旨在降低用户从传统 Nginx 迁移到云原生网关的门槛与成本。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的基本概念与核心架构
- Higress 与传统 API 网关（如 Nginx, Kong）的区别
- Higress 的应用场景（云原生架构、微服务网关、AI 网关）
- Docker 环境下 Higress 的快速安装与部署
- 基本的控制台操作与界面介绍

**学习时间**: 1 周

**学习资源**:
- Higress 官方文档
- Higress GitHub 仓库 README
- 云原生社区关于 Higress 的介绍文章

**学习建议**: 
建议先通读官方文档的“什么是 Higress”部分，理解其基于 Envoy 和 Istio 的技术背景。务必动手在本地或测试环境通过 Docker 完成一次 Standalone 模式的部署，并访问控制台熟悉界面布局。

---

### 阶段 2：核心功能与流量管理

**学习内容**:
- 域名、路由与 Ingress 配置
- 服务来源的注册与发现（Nacos, Consul, K8s Service, 固定地址）
- 流量治理插件：负载均衡、健康检查、超时重试、Header 操作
- 全局与自定义插件的使用
- 基础的安全防护：认证鉴权、IP 访问控制、CORS 配置

**学习时间**: 2-3 周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方插件市场
- Envoy 基础路由文档（用于理解底层原理）

**学习建议**: 
此阶段重点在于“配置”。尝试搭建一个包含两个后端服务的模拟环境，配置基于域名的路由转发，并实验不同的负载均衡策略。深入学习插件系统，尝试启用一个限流插件并观察效果。

---

### 阶段 3：云原生集成与 AI 网关

**学习内容**:
- 在 Kubernetes 环境中通过 Helm 部署 Higress
- Higress 与 Kubernetes Ingress 的结合使用
- Higress 作为 AI 网关的特性：对接大模型（LLM）、提示词缓存、Token 处理
- Wasm 插件开发入门（使用 Go 或 Python 编写简单插件）
- 服务 Mock 与泛化调用

**学习时间**: 3-4 周

**学习资源**:
- Higress 官方文档 - Kubernetes 部署指南
- Higress AI 网关特性文档
- Higress Wasm 插件开发示例

**学习建议**: 
如果你有 Kubernetes 基础，请务必在 K8s 集群中部署 Higress Gateway。关注 Higress 最新的 AI 特性，尝试配置一个转发到 OpenAI 或其他大模型服务的路由。尝试编写一个简单的 Wasm 插件（例如修改请求头），以理解 Higress 的扩展能力。

---

### 阶段 4：高阶运维与性能调优

**学习内容**:
- Higress 的高可用（HA）部署架构
- 观测性：对接 Prometheus/Grafana 监控、链路追踪
- 网关性能调优与压测方法
- 生产环境最佳实践：平滑发布、配置热更新、版本管理
- 多租户管理与多环境隔离策略

**学习时间**: 2-3 周

**学习资源**:
- Higress 官方博客 - 架构设计文章
- Envoy 性能调优指南
- Higress GitHub Discussions 中的生产实践案例

**学习建议**: 
此阶段侧重于“稳定性”和“可观测性”。学习如何配置 Prometheus 采集 Higress 的运行指标，并在 Grafana 中绘制仪表盘。阅读官方的架构设计文章，理解数据面与控制面的交互机制，以便排查复杂问题。

---

### 阶段 5：源码剖析与深度定制

**学习内容**:
- Higress 项目结构分析
- 核心 Controller 代码逻辑
- Envoy xDS 协议在 Higress 中的应用
- 深度定制开发：自定义 Controller 或扩展 Envoy Filter
- 贡献开源社区：PR 流程与代码规范

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Envoy xDS 协议官方文档
- Higress 官方 Roadmap

**学习建议**: 
下载源码并使用 IDE（如 GoLand）进行调试。从入口文件开始，追踪一次配置变更如何推送到数据面的全过程。尝试修复一个简单的 Bug 或添加一个微小的功能，并向社区提交 Pull Request，这是提升代码理解能力的最佳途径。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源并捐赠给云原生计算基金会（CNCF）的。

它的核心特点在于“三位一体”的架构演进：
1.  **继承自 Nginx**：兼容 Nginx 的生态，拥有极高的稳定性和性能。
2.  **基于 Envoy**：底层深度集成了 Envoy 作为数据面，利用其高性能的 C++ 网络处理能力和可观测性。
3.  **结合 Istio**：支持 Istio 的 API 管理规范，可以作为 Istio 的入口网关使用，实现服务网格流量的统一管理。

简单来说，Higress 旨在解决传统 Nginx 配置复杂、缺乏流量治理能力以及 Envoy 学习曲线陡峭的问题，提供一站式的流量管理平台。

---



### 2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 在设计上吸取了上述网关的优点，并针对云原生环境进行了优化，主要优势包括：

*   **极致的集成性**：Higress 原生支持 Istio，可以作为服务网格的南北向（入口）流量网关，与东西向（服务间）流量无缝打通。这是传统网关（如 Nginx）难以做到的。
*   **标准化与扩展性**：它支持 Kubernetes Ingress、Gateway API 等标准规范。同时，它允许使用 WASM (WebAssembly) 插件进行功能扩展。WASM 插件可以用 C++、Go、Rust 或 JavaScript 编写，相比传统的 Lua 插件（如 OpenResty），安全性更高，开发更灵活，且无需重启网关即可热加载。
*   **安全防护**：内置了与阿里云 Web 应用防火墙（WAF）同等级别的安全能力，提供免费的防护规则。
*   **易用性**：提供了开箱即用的控制台（K8s 版和 Standalone 版均有），相比 Nginx 的纯配置文件管理，可视化的路由配置和 Wasm 插件市场大大降低了运维和开发成本。

---



### 3: Higress 是否支持非 Kubernetes 环境（例如在虚拟机或 Docker 中）？

3: Higress 是否支持非 Kubernetes 环境（例如在虚拟机或 Docker 中）？

**A**: 是的，Higress 提供了两种部署形态，能够适应不同的基础设施环境：

1.  **Kubernetes 模式**：这是推荐模式，通过 Operator 进行部署和管理，能够充分利用 K8s 的调度和服务发现能力。
2.  **Standalone 模式**：针对传统的虚拟机或裸机环境。Higress 提供了基于 Docker Compose 的部署包，允许用户在没有 K8s 集群的情况下体验完整的网关功能。这使得用户可以从传统的 Nginx 部署平滑迁移到 Higress，而无需立即构建 K8s 集群。

---



### 4: Higress 如何处理服务发现？它能否对接 Nacos、Consul 或 Kubernetes Service？

4: Higress 如何处理服务发现？它能否对接 Nacos、Consul 或 Kubernetes Service？

**A**: Higress 拥有强大的服务发现能力，这得益于其阿里巴巴的基因。它原生支持以下多种服务注册中心：

*   **Kubernetes Service**：自动监听 K8s 的 Endpoints 变化，实现基于 Pod IP 的负载均衡。
*   **Nacos**：深度集成阿里云 Nacos 或开源 Nacos，能够直接从 Nacos 获取服务列表。
*   **Consul / Eureka / Zookeeper**：通过通用的注册中心适配协议进行对接。
*   **DNS / 固定 IP**：支持传统的 DNS 解析和手动配置上游服务地址。

这种多协议支持使得 Higress 非常适合微服务架构的迁移，能够连接传统的 Spring Cloud 应用和现代的云原生应用。

---



### 5: 什么是 Higress 的 Wasm 插件生态？它与 Lua 脚本有何不同？

5: 什么是 Higress 的 Wasm 插件生态？它与 Lua 脚本有何不同？

**A**: Wasm (WebAssembly) 插件机制是 Higress 的核心亮点之一。

*   **技术差异**：传统的 OpenResty/Nginx 主要依赖 Lua 脚本进行扩展。Lua 运行在同一个进程中，脚本崩溃可能导致整个网关进程崩溃（安全性较低），且 Lua 的并发模型受限。而 Higress 支持的 Wasm 插件运行在沙箱环境中，即使插件崩溃也不会影响网关主进程（内存隔离、安全性高）。
*   **语言支持**：开发者可以使用 Go、C++、Rust、AssemblyScript 甚至 JavaScript (QuickJS) 编写插件，无需学习 Lua。
*   **热加载**：Wasm 插件支持动态加载和卸载，修改业务逻辑不需要重启网关服务，这对生产环境的稳定性至关重要。Higress 官方还维护了一个插件市场，用户可以像使用 NPM 包一样一键安装常用的认证、流量控制插件。

---



### 6: Higress 是否兼容 Nginx

6: Higress 是否兼容 Nginx

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础环境搭建与流量路由

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求实现当用户访问 `http://localhost/hello` 时，能够将请求转发至后端的一个模拟服务（如 httpbin.org 或 mock 服务），并返回 200 状态码。

### 提示**: 参考 Higress 官方文档的 "快速开始" 章节。你需要编写一个简单的 `Ingress` 或 `Gateway` 资源配置文件，关键在于定义 `host`、`path` 以及对应的后端 `service` 地址。注意区分 Higress 与传统 Nginx Ingress 在配置上的差异。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其基于 Envoy 和 Istio 架构的特性，以下是针对实际使用场景的 5-7 条实践建议：

### 1. 利用 Wasm 插件实现 AI 请求的“无损”处理
**场景**：在调用大模型（如 OpenAI、通义千问）时，通常需要处理敏感词过滤、请求计费或 Prompt 预处理逻辑。
**建议**：不要在业务后端代码中处理这些逻辑，而是编写 **Wasm (WebAssembly)** 插件挂载到 Higress 的路由或网关级别。
**操作**：
*   使用 Higress 提供的 Go 或 C++ SDK 编写插件。
*   在插件中实现 `OnHttpRequestBody` 阶段，拦截并修改发给 AI 服务的 Body（例如注入系统 Prompt）。
*   在 `OnHttpResponseBody` 阶段，截获 AI 的流式响应进行实时审核或格式转换。
**最佳实践**：Wasm 插件是热加载的，修改插件逻辑不需要重启 Higress 网关，可以实现业务逻辑的敏捷迭代。

### 2. 配置“语义路由”而非简单的路径匹配
**场景**：AI 应用通常需要根据用户的意图将请求路由到不同的模型（例如：写代码路由到 GPT-4，写文案路由到 GPT-3.5）。
**建议**：利用 Higress 的 **AI 提取器** 和 **条件路由** 功能。
**操作**：
*   在网关配置一个 AI 提取器节点，先对用户输入进行极低成本的分类（或直接在网关层通过 Prompt 让 LLM 输出 JSON 分类标签）。
*   根据提取出的标签（如 `category: "coding"`），配置路由规则将流量转发到不同的后端服务（Upstream）。
**常见陷阱**：避免在网关层进行耗时过长的推理计算，否则会阻塞网关线程。建议仅用于路由决策或极轻量级的数据提取。

### 3. 实施流式响应的“零拷贝”转发
**场景**：大模型应用通常采用 Server-Sent Events (SSE) 或流式返回以降低首字延迟（TTFB）。
**建议**：确保 Higress 的路由配置开启了流式透传能力，并且后端 Upstream 配置正确。
**操作**：
*   检查 Higress 的 `ServicePort` 定义，确保协议识别正确（通常为 HTTP 或自定义）。
*   在 Wasm 插件开发中，如果需要修改流式响应，务必使用流式处理 API，不要尝试缓存整个 Body 再处理，这会导致巨大的内存占用和用户侧的长时间卡顿。
**最佳实践**：对于流式请求，网关应尽量扮演“透明代理”的角色，减少不必要的 Buffering（缓冲）。

### 4. 建立基于 Token 的精细化限流策略
**场景**：AI 服务的成本主要在于 Token 消耗，传统的 QPS（每秒请求数）限流无法准确反映成本。
**建议**：配置针对 AI 接口的定制化限流规则。
**操作**：
*   虽然标准 Envoy 限流基于请求，但你可以结合 Higress 的 Wasm 插件实现“Token 桶”限流。
*   在请求到达后端前，估算输入 Token 数（通过字符数粗略估算或本地模型计算），并在 Redis 中扣除用户配额。如果配额不足，直接在网关层拦截并返回 429，避免昂贵的 LLM 调用。

### 5. 统一管理多模型提供商的鉴权与协议转换
**场景**：企业内部可能同时使用通义千问、Azure OpenAI 以及本地部署的 Llama3，它们的 API 协议和鉴权方式各异。
**建议**：利用 Higress 的 **服务来源** 和 **插件** 能力，对外统一标准的 API 格式（如统一兼容 OpenAI 格式）。
**操作**：
*   在 Higress

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [Kubernetes](/tags/kubernetes/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*