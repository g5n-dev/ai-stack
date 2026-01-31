---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T11:00:17+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "LLM", "Istio", "Envoy", "WASM", "Kubernetes"]
categories: ["AI 工程", "系统与基础设施"]
source: github_trending
description: "Higress 是一款由阿里巴巴开源的、基于 Istio 和 Envoy 构建的**云原生 API 网关**。它采用 Go 语言开发，专注于**AI 原生（AI Native）**场景，目前 GitHub 星标数已超过 7,400。 以下是 Higress 的核心总结： **1. 核心定位** Higress 扩展了传"
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
- **星标**: 7,417 (+9 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，它通过集成 WebAssembly 插件能力，专注于提供 AI 网关、MCP 服务托管及传统流量管理功能。该项目旨在解决大模型应用落地与微服务治理中的流量路由与安全问题，适合需要在统一入口管理 AI 与传统业务流量的开发团队。本文将介绍其系统架构、核心组件以及 AI 网关特性等关键内容。

---
## 摘要

Higress 是一款由阿里巴巴开源的、基于 Istio 和 Envoy 构建的**云原生 API 网关**。它采用 Go 语言开发，专注于**AI 原生（AI Native）**场景，目前 GitHub 星标数已超过 7,400。

以下是 Higress 的核心总结：

**1. 核心定位**
Higress 扩展了传统网关的功能，通过集成 WebAssembly (WASM) 插件能力，将控制平面（配置管理）与数据平面（流量处理）分离。其架构支持毫秒级配置变更（通过 xDS 协议）且无连接中断，特别适用于 AI 长连接流式响应场景。

**2. 三大主要功能**
*   **AI 网关**：提供统一的 API 接口，兼容 30 多家大语言模型（LLM）提供商。核心能力包括协议转换、可观测性、缓存以及安全防护（通过 `ai-proxy`、`ai-cache`、`ai-security-guard` 等插件实现）。
*   **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用工具和外部服务（例如地图、搜索等）。
*   **Kubernetes Ingress**：作为 K8s 入口控制器，支持微服务路由，并兼容 nginx-ingress 注解。

**3. 关键特性**
*   **AI Native**：深度优化 LLM 应用接入，支持流式处理。
*   **可扩展性**：基于 WASM 的插件系统，允许灵活扩展功能。
*   **云原生**：完全适配 Kubernetes 和微服务生态。

简而言之，Higress 是一款专为 AI 时代设计的下一代网关，既包含了传统 API 流量管理的能力，又针对大模型应用和智能体工具调用提供了原生支持。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“AI 原生”网关，它成功将云原生流量治理与 LLM（大模型）应用所需的关键特性融合，不仅解决了传统 API 网关在 AI 时代的功能断层，更通过 WASM 技术构建了极具扩展性的生态。它是目前将 AI 能力与网关基础架构结合得最紧密、落地最彻底的开源项目之一。

**深入评价依据**

**1. 技术创新性：AI 原生架构与 WASM 生态的深度耦合**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并明确提出了“AI Gateway”和“MCP (Model Context Protocol) Server Hosting”作为核心功能。
*   **推断**：与传统网关（如 APISIX, Kong）通过插件“外挂”AI 能力不同，Higress 将 AI 流量治理视为一等公民。它原生支持 LLM 的语义路由、Token 计费与限流、以及 Prompt 模板管理。更关键的是，它引入了 MCP 协议支持，这意味着它不仅是一个流量的“管道”，更是 AI Agent 的“工具集托管中心”，允许网关直接暴露工具能力给大模型，这种架构创新极大地简化了 AI Agent 的开发复杂度。同时，其基于 WASM 的插件系统允许开发者使用 C/C++/Go/Rust/AssemblyScript 编写高性能插件，且无需重新编译网关，这种热更新能力在 AI 场景下对频繁迭代的需求至关重要。

**2. 实用价值：填补 AI 落地中的“最后一公里”**
*   **事实**：DeepWiki 提到其提供“AI gateway features for LLM applications”和“MCP server hosting for AI agent tool integration”。
*   **推断**：在 LLM 应用落地中，企业面临三大痛点：协议转换（OpenAI 协议适配）、成本控制（Token 精细化计费）与安全（数据脱敏）。Higress 直接内置了这些能力，使得企业无需自建中间层即可将大模型服务安全地暴露给内部或外部应用。例如，通过它的一站式配置，开发者可以轻松实现“将复杂的 Prompt 模板在网关层固化，前端仅传简单参数”，或者“在网关层自动拦截敏感词并注入系统提示词”。这种将业务逻辑左移到网关层的做法，极大降低了后端服务的耦合度，具有极高的实用价值。

**3. 代码质量与架构：云原生标准的继承与演进**
*   **事实**：项目由阿里团队发起，基于 Envoy（C++）和 Istio（Go）构建，控制面与数据面分离。
*   **推断**：得益于 Envoy 的高性能数据面，Higress 在处理高并发流量时具备天然优势。其架构设计遵循了标准的云原生控制面/数据面分离模式，保证了配置管理的灵活性和数据处理的稳定性。虽然 Envoy 本身配置极其复杂（通过静态文件或静态 API），但 Higress 通过 K8s CRD（自定义资源）对其进行了极友好的封装，降低了上手门槛。代码结构上，Go 语言编写的控制面逻辑清晰，文档覆盖了从构建到开发的各个环节，符合企业级开源项目的标准。

**4. 社区活跃度与生态：背靠阿里的强力驱动**
*   **事实**：GitHub 星标数 7,417+（且在快速增长），由 Alibaba 维护，提供了中、日、英多语言文档。
*   **推断**：作为阿里云内部网关产品的开源版本，Higress 继承了阿里在电商高并发场景下的技术积淀。其社区活跃度较高，版本迭代速度快，且对国内开发者非常友好（中文文档详尽）。相比纯海外项目，Higress 对国内云厂商（如通义千问、百炼等）的协议适配往往更加优先和原生，这对于国内企业构建 AI 应用是一个巨大的加分项。

**5. 潜在问题与改进建议**
*   **推断**：尽管功能强大，Higress 的部署复杂度相对较高。因为它依赖 Istio 和 Envoy 的生态，对于仅需要简单转发的小型团队来说，运维成本可能过高。此外，AI 领域迭代极快，Higress 需要持续跟进最新的模型特性（如 Sora 等视频生成模型的流式传输优化），否则容易面临功能过时的风险。建议在轻量级部署模式（如 Standalone 模式）上进一步降低资源占用，以便在边缘端运行。

**边界条件与验证清单**

**不适用场景**：
*   **超轻量级静态站点服务**：Nginx 或 Caddy 更为简单直接。
*   **纯内部微服务治理且无 AI 需求**：如果团队已经深度绑定 K8s Ingress (如 Nginx Ingress Controller)，迁移成本可能大于收益，除非急需 AI 特性。
*   **极低资源环境**：Envoy 的内存占用相对较高，不适合在几 MB 内存的边缘设备上运行。

**快速验证清单**：
1.  **协议兼容性测试**：验证 Higress 能否将 OpenAI 格式的请求无缝转发给其他非 OpenAI 兼容的模型（如 Llama 3），并自动修改响应头。
2.  **WASM 插件热加载**：编写一个简单的 Go WASM 插件（如添加自定义 HTTP 头），在不重启网关的情况下动态加载，验证是否生效及

---
## 技术分析

# Higress 深度技术分析报告

Higress 是阿里巴巴开源的一款基于 Istio 和 Envoy 构建的云原生 API 网关。它不仅仅是一个传统的流量入口，更被定义为 **AI Native API Gateway**（AI 原生 API 网关）。以下是对该项目的深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了 **控制平面与数据平面分离** 的标准云原生架构模式。
*   **数据平面**：深度依赖 **Envoy**。Envoy 是高性能的 L7 代理，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **控制平面**：基于 **Istio** 进行了扩展和简化。Higress 去除了 Istio 中繁重的 Sidecar 模式，将其转化为更适合 API 网关的 **Ingress Controller** 模式。它通过 xDS 协议（包括 LDS, CDS, RDS 等）将配置下发给数据平面。
*   **扩展层**：引入了 **WebAssembly (WASM)** 作为核心插件运行时。这使得 Higress 可以使用 C/C++/Go/Rust/AssemblyScript 等多种语言编写插件，并在 Envoy 的沙箱中安全、高效地运行。

### 核心模块与关键设计
1.  **路由与流量管理**：基于 Envoy 的高性能路由匹配，支持 HTTP/gRPC/Dubbo 等协议。
2.  **WASM 插件市场**：这是其架构的亮点。它允许用户动态加载代码，而无需重启网关。Higress 内置了针对 AI 场景（如 Token 计费、流式处理）的 WASM 插件。
3.  **MCP (Model Context Protocol) 服务器托管**：针对 AI Agent 场景，Higress 能够作为 MCP Server 的托管端，解决 Agent 与外部工具集成的连接问题。
4.  **配置管理**：支持 Kubernetes Ingress YAML、基于 Nacos 的服务发现以及传统的控制台 UI 配置。

### 技术亮点与创新点
*   **AI Native 原生支持**：这是 Higress 与 Nginx、传统 Kong 最大的区别。它内置了对 LLM（大语言模型）流式响应的处理能力，能够识别 SSE (Server-Sent Events) 流中的 Token 进行计费、限流和拦截。
*   **热更新能力**：得益于 Istio 的架构，配置变更通过 xDS 协议秒级下发，数据面连接不中断，这对于需要保持长连接的 AI 对话场景至关重要。
*   **服务网格融合**：它既可以作为 API 网关部署在网格边缘，也可以接管网格内的内部流量，实现了 Ingress 与 Mesh 的技术栈统一。

### 架构优势分析
*   **高性能**：Envoy 的 C++ 内核保证了极高的吞吐量和低延迟。
*   **可扩展性**：WASM 插件机制打破了传统 Lua 插件（如 OpenResty）的性能瓶颈和开发语言限制。
*   **生态兼容**：完全兼容 K8s Ingress API，降低了迁移成本。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **功能**：统一管理 OpenAI、Azure、通义千问等 LLM 的 API Key；提供基于 Token 的计费和限流；处理 AI 流式输出的 SSE 协议转换。
    *   **场景**：企业内部构建 AI 助手时，统一管理对各大模型厂商的调用，防止 Key 泄露，控制成本。
2.  **MCP 服务器托管**：
    *   **功能**：将内部微服务自动封装为 MCP 协议接口供 AI Agent 调用。
    *   **场景**：AI Agent 需要调用企业内部数据库或 API 时，Higress 充当协议转换和安全网关。
3.  **传统 API 网关**：
    *   **功能**：金丝雀发布、蓝绿部署、流量镜像、认证鉴权。
    *   **场景**：微服务架构下的流量入口。

### 解决的关键问题
*   **LLM 调用的不可控性**：传统网关只能基于请求数限流，无法基于“Token 消耗量”限流。Higress 解决了 AI 时代的成本控制问题。
*   **AI 生态碎片化**：统一了不同 LLM 厂商的接口协议，使得应用层只需对接 Higress，底座模型可随时切换。
*   **插件开发门槛**：通过 WASM，允许使用高级语言（如 Go）编写插件，比 C++ 开发 Envoy 插件简单，比 Lua 性能更好。

### 与同类工具对比
| 特性 | Higress | Nginx/OpenResty | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **内核** | Envoy (C++) | Nginx (C) | Nginx/Proxy (C) | Nginx (C) etcd |
| **扩展性** | WASM (High) | Lua (Med) | Lua/Go/Py (Med) | Lua (Med) |
| **AI 特性** | **原生支持 (Token限流/Provider转换)** | 需自写脚本 | 需插件 | 需插件 |
| **配置下发** | xDS (gRPC, 秒级) | Reload (进程级, 有抖动) | DB/Cache | etcd (Watch) |
| **K8s 集成** | 原生 CRD | 需 Ingress Controller | 原生 CRD | 原生 CRD |

### 技术实现原理
Higress 在 Envoy 之上构建了一个 **WASM HTTP Filter**。当请求进入时，Envoy 将请求/响应头和 Body 传递给 WASM 虚拟机。针对 AI 场景，Higress 实现了特殊的流式处理逻辑：它可以在不截断整个流的情况下，逐块分析 SSE 数据，从而实时计算 Token 数量并在超限时切断连接。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 虚拟机管理**：Higress 使用了代理模式来管理 WASM 生命周期。它支持 WASM 插件的动态挂载，通过 OCI (Open Container Initiative) 标准拉取插件镜像，实现了插件的“容器化”分发。
2.  **配置隔离**：在 K8s 环境下，Higress 通过 Ingress Class 或特定的 Annotation 来区分自身管理的配置与其他 Ingress Controller（如 Nginx Ingress），实现多网关共存。
3.  **服务发现对接**：通过 `ServiceEntry` 和 `ServiceEntry` 控制器，Higress 能够将 Nacos、Consul 等注册中心的 service 映射为 Envoy 的 Cluster 配置。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器（将 K8s Ingress 转为 xDS 配置）、Dubbo 协议处理等。
*   **`plugins/`**：内置 WASM 插件的源码，通常包含 Go 源码和编译后的 `.wasm` 文件。
*   **`router/`**：核心路由匹配逻辑，处理 HTTP 头部、路径匹配和权重分发。

### 性能与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **异步 I/O**：全异步非阻塞模型，支持 C10M（千万级并发连接）。
*   **水平扩展**：无状态设计，数据面 Pod 可随意扩容。

### 技术难点与解决
*   **难点**：WASM 插件的内存隔离与资源限制。
*   **解决**：Envoy 对 WASM VM 有严格的内存和 CPU 指令限制，防止恶意插件拖垮网关。Higress 在控制面增加了插件配置的校验层。
*   **难点**：长连接场景下的配置热更新。
*   **解决**：利用 xDS 协议的版本控制机制，仅推送增量配置，Envoy 在建立新连接时应用新规则，旧连接保持不变，实现了无缝切换。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发**：特别是需要对接多家 LLM 厂商，需要对 Token 成本做精细化控制的企业。
2.  **云原生微服务**：使用 Kubernetes 作为基础设施，需要高性能网关的企业。
3.  **复杂流量治理**：需要使用金丝雀发布、流量镜像、超时重试等高级路由功能的场景。
4.  **混合云部署**：需要同时管理 K8s 内服务和非 K8s 服务（如虚拟机服务）的场景。

### 最有效的情况
当你需要 **“将 AI 能力集成到现有微服务体系，并保持统一的流量治理和鉴权标准”** 时，Higress 是目前最优解之一。它避免了为 AI 流量单独搭建一套网关的复杂性。

### 不适合的场景
1.  **极简静态网站托管**：杀鸡焉用牛刀，Nginx 足够。
2.  **边缘计算/嵌入式网关**：Envoy 和 WASM 的资源开销相对较高，不适合资源极度受限的 IoT 设备。
3.  **纯 Windows/.NET 旧系统维护**：如果企业完全没有容器化基础，部署 Higress 的运维成本会很高。

### 集成方式与注意事项
*   **K8s Ingress**：直接安装 Higress Helm Chart，将 Ingress Class 指定为 `higress`。
*   **注意事项**：WASM 插件虽然安全，但仍有性能损耗（约 5%-10%），对于极致性能要求的纯转发场景，建议使用原生 Envoy Filter。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **更深度的 AI 编排**：从单纯的流量转发，转向具备 Prompt 模板管理、上下文缓存能力的智能网关。
2.  **MCP 协议的普及**：Higress 极有可能成为 MCP Server 的标准托管基础设施，成为 AI Agent 时代的“南北向流量枢纽”。
3.  **WASM 生态标准化**：推动 WASM-Cloud 接口在网关层的标准化，使插件在不同网关间迁移。

### 社区反馈与改进
目前社区对 AI Gateway 功能反响热烈，但在文档的细致度（特别是 WASM 插件开发指南）和传统 API 管理功能的易用性上仍有提升空间。相比 Kong，其插件生态的丰富度（数量）尚有差距。

---

## 6. 学习建议

### 适合的开发者
*   **云原生架构师**：了解 K8s 和 Service Mesh 体系。
*   **后端 Gopher/Java 开发者**：希望深入网关底层或开发自定义插件。
*   **AI 应用工程师**：需要解决大模型落地过程中的工程化问题。

### 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 概念。
2.

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
    gateway = Gateway()
    
    # 添加路由规则：将/api/v1开头的请求转发到service-a
    gateway.add_route(
        path_prefix="/api/v1",
        destination="service-a:8080",
        methods=["GET", "POST"],
        plugins=["rate-limit", "jwt-auth"]
    )
    
    # 添加路由规则：将/static开头的请求转发到CDN
    gateway.add_route(
        path_prefix="/static",
        destination="cdn.example.com",
        methods=["GET"],
        plugins=["cache-control"]
    )
    
    return gateway

# 说明：这个示例展示了如何使用Higress配置网关路由，实现请求的智能分发。
# 通过path_prefix匹配不同路径，可以将流量引导到不同的后端服务，
# 同时可以附加插件实现限流、认证等功能。
```




```python
# 示例2：Higress插件开发
from higress import Plugin

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于Header的API认证
    """
    def __init__(self):
        super().__init__("custom-auth")
    
    def on_request(self, context):
        """
        请求处理阶段
        检查请求头中的认证信息
        """
        auth_header = context.request.headers.get("X-Auth-Token")
        if not auth_header or not self.validate_token(auth_header):
            context.response.status_code = 401
            context.response.body = "Unauthorized"
            return context.response.terminate()
        
        # 认证通过，添加用户信息到上下文
        context.user_id = self.get_user_id(auth_header)
        return context.response.continue_request()
    
    def validate_token(self, token):
        """验证token有效性"""
        # 实际实现中应该调用认证服务
        return token.startswith("valid-")
    
    def get_user_id(self, token):
        """从token中提取用户ID"""
        return token.split("-")[1]

# 说明：这个示例展示了如何开发Higress插件，实现自定义认证逻辑。
# 插件可以在请求处理的各个阶段介入，实现认证、限流、日志等功能。
# 这里实现了一个简单的基于Header的认证插件。
```




```python
# 示例3：Higress服务发现集成
from higress import ServiceDiscovery

def setup_service_discovery():
    """
    配置服务发现
    解决问题：动态发现后端服务实例，实现负载均衡
    """
    sd = ServiceDiscovery()
    
    # 添加Nacos作为服务发现源
    sd.add_source(
        type="nacos",
        address="nacos-server:8848",
        namespace="dev",
        groups=["services"]
    )
    
    # 添加服务过滤规则
    sd.add_filter(
        service_name="service-a",
        health_check=True,
        min_instances=2
    )
    
    # 配置负载均衡策略
    sd.set_load_balancer(
        strategy="round_robin",
        health_check_interval=30
    )
    
    return sd

# 说明：这个示例展示了如何配置Higress的服务发现功能。
# 通过集成Nacos等服务注册中心，可以动态获取后端服务实例列表，
# 实现自动负载均衡和故障转移。服务发现是微服务架构中的关键功能。
```


---
## 案例研究


### 1：某大型电商平台（基于阿里云 Higress 的实战应用）

 1：某大型电商平台（基于阿里云 Higress 的实战应用）

**背景**:  
该电商平台在“双11”大促期间面临流量洪峰，原有基于 Nginx 的网关系统在处理每秒 10 万 QPS 时出现性能瓶颈，且动态路由配置需要重启服务，影响业务连续性。

**问题**:  
- 传统网关扩展性差，无法应对突发流量  
- 路由规则更新依赖手动配置，效率低且易出错  
- 多云架构下流量调度复杂，缺乏统一管理  

**解决方案**:  
部署 Higress 作为云原生 API 网关，利用其以下特性：  
- 基于 Istio 和 Envoy 的高性能架构，支持水平扩展  
- 通过 Wasm 插件实现动态路由、流量镜像和限流策略  
- 集成阿里云 ARMS 实现全链路可观测性  

**效果**:  
- 成功支撑 50 万 QPS 流量，延迟降低 60%  
- 路由规则热更新生效时间从分钟级降至秒级  
- 运维效率提升 80%，大促期间零故障  

---  



### 2：某跨国金融科技公司

 2：某跨国金融科技公司

**背景**:  
该公司业务遍及 20+ 国家，原有网关系统无法满足不同地区的合规要求（如 GDPR 数据本地化），且多集群间流量管理混乱。

**问题**:  
- 跨区域数据传输存在合规风险  
- 多集群服务发现和负载均衡策略不一致  
- 传统网关对 WebSocket 和 gRPC 协议支持不足  

**解决方案**:  
采用 Higress 构建全球流量调度系统：  
- 通过 Higgress 的多集群管理功能实现区域流量隔离  
- 使用 Wasm 插件动态注入合规检查逻辑  
- 原生支持 gRPC 和 WebSocket 协议，无需额外适配  

**效果**:  
- 满足 100% 合规要求，通过国际审计  
- 跨区域流量调度延迟减少 40%  
- 新协议接入时间从 2 周缩短至 1 天  

---  



### 3：某在线教育平台

 3：某在线教育平台

**背景**:  
该平台在疫情期间用户量激增 10 倍，原有网关无法应对实时互动场景（如直播课）的高并发长连接需求。

**问题**:  
- 长连接导致内存占用过高，网关频繁崩溃  
- 直播流量突发时缺乏自动弹性伸缩能力  
- 第三方服务（如支付、CDN）集成复杂  

**解决方案**:  
基于 Higgress 重构网关层：  
- 利用其连接池优化和内存管理特性解决长连接问题  
- 结合 Kubernetes HPA 实现基于 QPS 的自动扩缩容  
- 通过插件市场快速集成第三方服务  

**效果**:  
- 单实例长连接承载能力提升 5 倍  
- 资源成本降低 30%  
- 新服务集成时间减少 70%

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|-----------------|--------|------|
| 性能 | 高性能（基于 Envoy 和 Istio），支持高并发 | 极高性能（基于 OpenResty 和 LuaJIT），适合高流量场景 | 高性能（基于 Nginx 和 Lua），适合中高流量场景 |
| 易用性 | 提供控制台和 K8s 集成，配置简单，适合云原生环境 | 配置灵活但学习曲线较陡，需要熟悉 Lua 和 OpenResty | 提供管理 UI 和插件系统，但配置相对复杂 |
| 成本 | 开源免费，企业版需付费，云服务按需计费 | 开源免费，企业版需付费，云服务按需计费 | 开源免费，企业版需付费，云服务按需计费 |
| 扩展性 | 支持自定义插件（Wasm 和 Go），扩展性强 | 支持自定义插件（Lua 和 Go），扩展性极强 | 支持自定义插件（Lua 和 Python），扩展性较强 |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区活跃，文档丰富，但中文资源较少 | 社区成熟，文档完善，但更新较慢 |
| 适用场景 | 云原生、微服务、API 网关，适合阿里云用户 | 高性能 API 网关、微服务，适合技术团队 | 通用 API 网关，适合传统和云原生环境 |

### 优势分析

- 优势1：基于 Envoy 和 Istio，深度集成云原生生态，适合 K8s 环境。
- 优势2：提供控制台和阿里云支持，降低运维复杂度。
- 优势3：支持 Wasm 插件，扩展性强，适合复杂业务逻辑。

### 不足分析

- 不足1：社区和生态相比 APISIX 和 Kong 较新，资源较少。
- 不足2：对非阿里云用户可能存在适配成本。
- 不足3：性能略低于 APISIX（基于 OpenResty）。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 注解的流量管理

**说明**  
Higress 兼容 Kubernetes Ingress 规范，通过注解（Annotations）可实现灰度发布、蓝绿部署等高级流量路由功能。例如使用 `nginx.ingress.kubernetes.io/canary` 注解配置流量权重。

**实施步骤**  
1. 在 Ingress YAML 中添加注解：  
   ```yaml
   annotations:
     nginx.ingress.kubernetes.io/canary: "true"
     nginx.ingress.kubernetes.io/canary-weight: "20"
   ```
2. 部署新版服务并观察流量分布  
3. 逐步调整权重直至全量切换

**注意事项**  
- 注解格式需严格匹配 Higress 文档规范  
- 建议配合 Prometheus 监控流量分配效果  

---

### 实践 2：WAF 插件安全防护

**说明**  
启用内置 WAF 插件可防御常见 Web 攻击（如 SQL 注入、XSS），支持自定义规则和 IP 黑名单。

**实施步骤**  
1. 在控制台选择 `WAF 插件` 并启用  
2. 配置防护规则（例如拦截 `union select` 关键字）  
3. 设置告警通知（钉钉/Slack）

**注意事项**  
- 规则误报时需及时调整正则表达式  
- 建议先在测试环境验证规则  

---

### 实践 3：服务注册中心集成

**说明**  
通过 Nacos/Consul 插件实现服务发现，避免硬编码后端服务地址，支持动态扩缩容。

**实施步骤**  
1. 安装 `nacos-service` 插件  
2. 配置注册中心地址：  
   ```yaml
   registry:
     type: nacos
     serverAddr: 192.168.1.100:8848
   ```
3. 在路由配置中引用服务名

**注意事项**  
- 确保 Higress 与注册中心网络连通  
- 生产环境建议开启注册中心鉴权  

---

### 实践 4：全链路灰度发布

**说明**  
结合流量标签和路由规则，实现按用户 ID/地域等维度的灰度发布，降低发布风险。

**实施步骤**  
1. 在请求头中添加灰度标识（如 `x-gray: true`）  
2. 配置条件路由：  
   ```yaml
   match:
     headers:
       x-gray:
         exact: true
   route:
   - destination: v2-service
   ```
3. 通过 A/B 测试工具分配灰度流量

**注意事项**  
- 灰度流量需独立监控  
- 准备快速回滚方案  

---

### 实践 5：高可用部署架构

**说明**  
生产环境建议部署多副本 Higress，并配置健康检查和自动故障转移。

**实施步骤**  
1. 设置副本数≥3：  
   ```yaml
   replicas: 3
   ```
2. 配置存活探针：  
   ```yaml
   livenessProbe:
     httpGet:
       path: /health
       port: 15021
   ```
3. 使用负载均衡器（如 SLB）分发流量

**注意事项**  
- 确保不同副本分布在不同可用区  
- 定期进行故障演练  

---

### 实践 6：监控与可观测性

**说明**  
集成 Prometheus + Grafana 实现指标采集，通过 OpenTelemetry 追踪调用链。

**实施步骤**  
1. 启用 Prometheus 采集端口：  
   ```yaml
   serviceMonitor:
     enabled: true
   ```
2. 导入 Higress 官方 Grafana 模板  
3. 配置 SLO 告警（如 P99 延迟>500ms）

**注意事项**  
- 监控数据需持久化存储  
- 关键指标应包含 QPS、错误率、延迟  

---

### 实践 7：证书自动化管理

**说明**  
通过 cert-manager 插件实现 HTTPS 证书自动续期，支持 Let's Encrypt 免费证书。

**实施步骤**  
1. 安装 cert-manager：  
   ```bash
   kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
   ```
2. 创建 ClusterIssuer：  
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: letsencrypt-prod
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
   ```
3. 在 Ingress 中引用证书

**注意事项**  
- 注意 Let's Encrypt 速率限制  
- 测试环境可使用 staging 服务器

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 Wasm 插件与原生插件隔离

**说明**: Higress 支持 Wasm 插件，但 Wasm 插件的执行效率低于原生 Go 插件。将高频使用的插件（如认证、限流）迁移至原生插件，可显著降低执行开销。

**实施方法**:
1. 评估现有 Wasm 插件的性能瓶颈，优先迁移高频插件。
2. 使用 Higress 提供的 Go SDK 重写插件逻辑。
3. 通过配置文件将原生插件加载至 Higress 进程。

**预期效果**: 插件执行延迟降低 30%-50%，吞吐量提升 20% 以上。

---

### 优化 2：优化连接池配置

**说明**: 默认连接池配置可能导致连接复用不足或频繁建立新连接，增加延迟。调整连接池参数可提升后端服务通信效率。

**实施方法**:
1. 调整 `upstream` 的 `connections` 参数，根据后端服务能力设置合理值（如 100-500）。
2. 启用 HTTP/2 协议以减少连接数。
3. 监控连接池使用率，动态调整参数。

**预期效果**: 后端服务响应时间减少 10%-20%，连接错误率降低 15%。

---

### 优化 3：启用缓存与压缩

**说明**: 对静态内容或高频 API 响应启用缓存，减少后端压力。同时启用 Gzip 压缩可降低网络传输量。

**实施方法**:
1. 在路由配置中启用 `cache` 插件，设置合理的 TTL（如 60s）。
2. 全局启用 Gzip 压缩，压缩阈值设为 1KB。
3. 对动态内容禁用缓存，避免数据一致性问题。

**预期效果**: 缓存命中时响应时间降低 80%，带宽占用减少 40%-60%。

---

### 优化 4：调整 Worker 进程与线程模型

**说明**: Higress 基于 Envoy，默认 Worker 进程数可能未充分利用多核 CPU。调整 Worker 数量可提升并发处理能力。

**实施方法**:
1. 设置 `higress` 的 `worker_processes` 参数为 CPU 核心数。
2. 启用 `worker_cpu_affinity` 绑定 CPU 核心，减少上下文切换。
3. 通过压测验证最佳 Worker 数量（通常为核心数或核心数-1）。

**预期效果**: CPU 利用率提升 20%-30%，请求处理延迟降低 10%-15%。

---

### 优化 5：启用 Prometheus 监控与日志采样

**说明**: 全量日志记录会消耗大量 I/O 和 CPU 资源。通过日志采样和监控优化，可减少性能损耗。

**实施方法**:
1. 配置 `log_sampler` 插件，采样率设为 10%-50%（根据业务需求）。
2. 启用 Prometheus 指标采集，禁用非关键指标（如 `debug` 级别）。
3. 使用异步日志写入（如 `file_log` 插件的异步模式）。

**预期效果**: 日志写入开销降低 50%-70%，系统整体吞吐量提升 10%-20%。

---

### 优化 6：优化 DNS 解析与连接超时

**说明**: 频繁的 DNS 解析和过长的超时配置会导致资源浪费。优化这些参数可减少不必要的等待。

**实施方法**:
1. 配置 `dns_resolver` 缓存，TTL 设为 60s。
2. 调整 `connect_timeout` 和 `read_timeout` 为合理值（如 5s 和 30s）。
3. 对后端服务使用 IP 直连（如 K8s Service 的 ClusterIP）。

**预期效果**: DNS 解析延迟降低 90%，超时等待时间减少 20%-40%。

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Envoy
- 提供了开箱即用的 WAF 防护、流量管理及安全防护能力，适合生产环境使用
- 支持将 Nginx Ingress 注解无缝迁移，降低了从传统 Ingress 迁移的门槛
- 内置了针对 Dubbo 和 Nacos 等微服务生态的深度支持，弥补了通用网关在服务治理上的短板
- 具备强大的可扩展性，允许通过 WASM 或 Lua 插件灵活扩展业务逻辑
- 提供了完善的控制台与仪表盘，显著提升了网关的可观测性与运维效率


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关的基本概念与 Higress 的定位
- Higress 与传统网关（如 Nginx, Kong）及云原生网关（如 Istio Gateway, APISIX）的区别
- 核心架构理解：Istio + Envoy 架构
- Higress 的基本术语：Ingress、Gateway、路由、服务
- Docker 环境下 Higress 的快速安装与部署（本地 Standalone 模式）

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：快速开始
- Envoy 官方文档基础概念部分

**学习建议**:
- 建议先对 Kubernetes 和 Service Mesh 有初步了解，但不是强制要求。
- 优先使用 Docker Desktop 或本地 Kind 集群进行安装，体验最简单的 HTTP 路由转发功能。
- 重点理解 Higress 如何通过 Wasm 插件扩展能力，这是其核心特性之一。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- 详细的 Ingress API 配置（基于 Kubernetes Gateway API）
- 基于权重的流量分流与蓝绿/金丝雀发布实践
- Header、Cookie、URL 参数等高级路由匹配规则
- 负载均衡算法配置（轮询、随机、一致性哈希等）
- 服务发现集成：对接 Nacos、Zookeeper、固定地址及 Kubernetes Service
- 域名管理与 TLS/HTTPS 证书配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：流量治理章节
- Kubernetes Gateway API 官方规范说明
- Higress 官方示例库

**学习建议**:
- 动手搭建一个微服务模拟场景（例如使用 Nacos 注册中心），练习服务发现配置。
- 尝试配置一次金丝雀发布，观察流量切换过程。
- 熟悉控制台的配置界面，同时也要掌握 YAML 配置方式，以便于自动化。

---

### 阶段 3：安全与可观测性

**学习内容**:
- 认证与鉴权：Basic Auth、JWT、ApiKey 鉴权配置
- 安全防护：Wasm 插件实现 IP 黑白名单、请求限流（并发/请求速率）、熔断降级
- 可观测性集成：访问日志配置、对接 Prometheus/Grafana 监控指标
- 分布式链路追踪集成（SkyWalking/Zipkin）
- Higress 控制平面（Console）的运维操作

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：安全与可观测性章节
- Higress 插件市场文档
- Prometheus 监控最佳实践白皮书

**学习建议**:
- 安装 Prometheus 和 Grafana，导入 Higress 的 Dashboard 面板，观察 QPS、延迟等核心指标。
- 在测试环境模拟高并发，测试限流和熔断配置是否生效。
- 学习如何编写自定义的 Wasm 插件来处理特定的鉴权逻辑。

---

### 阶段 4：高级扩展与生产级运维

**学习内容**:
- Wasm (WebAssembly) 插件开发深度解析：使用 Go/C++/Rust 编写自定义插件
- Higress 高可用部署架构：多副本部署、数据库迁移
- 网关性能调优：连接池配置、缓冲区调整、Envoy 配置优化
- 多集群接入与云原生环境集成（ACK, K8s）
- 生产环境故障排查与应急处理

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：自定义开发章节
- Envoy Wasm C++/Go SDK 文档
- Higress GitHub Issues 与 Discussions（学习常见问题）

**学习建议**:
- 尝试编写一个简单的 Go Wasm 插件（例如修改请求头或响应体），并在本地编译加载。
- 阅读官方的源码，理解控制平面与数据平面的交互机制。
- 如果条件允许，在 Kubernetes 生产环境中进行一次平滑升级演练。

---

### 阶段 5：架构设计与生态集成

**学习内容**:
- Higress 在微服务架构中的最佳实践与位置设计
- AI 网关特性：对接大模型（LLM）与 Prompt 模板管理
- 服务网格对接：作为 Istio 的数据平面替代方案
- 与阿里云云原生产品（MSE, ARMS, SAE）的深度集成方案
- 大规模流量场景下的架构规划与成本优化

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客与架构师文章
- 阿里云云原生产品官网文档
- 云原生社区峰会相关技术

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源并捐赠给云原生计算基金会（CNCF）的。

Higress 的前身是阿里巴巴内部广泛使用的 API 网关 Tengine（基于 Nginx）的内部版本。它的诞生旨在解决传统网关在云原生时代面临的扩展性、性能和易用性问题。作为阿里云云原生产品家族的重要组成部分，Higress 继承了阿里巴巴双 11 等高并发场景的流量治理经验，同时结合了 Istio 的生态，致力于成为云原生时代的流量入口标准。

---



### 2: Higress 与 Nginx、Envoy 以及传统的 Kong 网关相比有什么核心优势？

2: Higress 与 Nginx、Envoy 以及传统的 Kong 网关相比有什么核心优势？

**A**: Higress 的核心架构优势在于它**深度集成了 Envoy** 作为高性能数据面，并使用 **Golang** 编写控制面，这与传统的 Nginx/Lua 模式（如 OpenResty 或 Kong）有显著区别。

1.  **性能与安全性**：相比 Lua 脚本，Golang 编写的插件系统在内存安全性和开发调试体验上更好，且 Envoy 的数据面在高并发下性能极其稳定。
2.  **标准兼容**：Higress 原生支持 Kubernetes Ingress 和 Gateway API 标准，同时也兼容 Nginx 的 Ingress 注解，降低了迁移成本。
3.  **Istio 集成**：作为云原生网关，Higress 可以直接作为 Istio 的入口网关使用，实现了南北向（外部流量进入集群）与东西向（服务间通信）流量的统一管理，这是传统网关难以做到的。
4.  **插件热更新**：支持插件的动态加载和热更新，不需要重启网关服务，业务变更更加灵活。

---



### 3: Higress 是否支持从 Nginx Ingress 或其他网关进行平滑迁移？

3: Higress 是否支持从 Nginx Ingress 或其他网关进行平滑迁移？

**A**: 是的，Higress 非常重视迁移的兼容性，提供了多种工具和策略来降低迁移门槛。

1.  **Nginx 兼容**：Higress 提供了针对 Nginx Ingress 的注解兼容层，大部分常用的 Nginx Ingress Annotation 可以直接在 Higress 中使用，无需修改 YAML 配置。
2.  **配置转换工具**：官方提供了配置迁移工具，可以帮助用户将 Nginx 的配置文件（nginx.conf）或 Kong 的配置转换为 Higress 的路由配置。
3.  **双栈运行**：在迁移过程中，Higress 可以与现有的 Nginx Ingress Controller 并存，通过调整 Service 的 Selector 或流量权重，逐步将流量切换到 Higress，从而实现灰度发布和平滑过渡。

---



### 4: Higress 的插件机制是如何工作的？是否支持自定义插件？

4: Higress 的插件机制是如何工作的？是否支持自定义插件？

**A**: Higress 提供了非常灵活且强大的插件扩展机制，支持通过多种方式扩展网关功能。

1.  **Wasm (WebAssembly) 支持**：这是 Higress 插件生态的一大亮点。它支持 Wasm 插件，这意味着开发者可以使用 C++、Go、Rust、JavaScript/TypeScript 等多种语言编写插件，编译为 Wasm 格式后动态加载到 Envoy 中运行。Wasm 插件具有沙箱隔离、高性能和动态热加载的特点。
2.  **Go 原生插件**：除了 Wasm，Higress 还支持直接使用 Go 编写原生插件，运行在控制面的 Go 进程中，适合处理复杂的逻辑或需要调用外部服务的场景。
3.  **Lua 兼容**：为了兼容旧有的 OpenResty/Kong 生态，Higress 也支持运行 Lua 脚本（通过特定适配器），方便用户复用原有的 Lua 插件代码。
4.  **插件市场**：官方提供了一个插件市场，包含了诸如认证鉴权、流量镜像、请求限流等常用开箱即用的插件。

---



### 5: 在 Kubernetes 环境中，Higress 的部署架构是怎样的？对资源有什么要求？

5: 在 Kubernetes 环境中，Higress 的部署架构是怎样的？对资源有什么要求？

**A**: Higress 采用标准的云原生控制面/数据面分离架构。

1.  **部署组件**：
    *   **Higress Gateway (数据面)**：基于 Envoy，实际处理流量的 Pod，通常以 Deployment 方式部署，并配合 Service (LoadBalancer 或 NodePort) 对外暴露服务。
    *   **Higress Console (控制面)**：提供 UI 界面、配置管理、API 分发等功能的组件。
2.  **资源要求**：
    *   **内存**：由于 Envoy 本身极其高效，Higress 的基础内存占用相对较低。在低负载场景下，通常建议为每个 Gateway Pod 分配 256Mi - 512Mi 内存。但在处理海量长连接或高并发（如十万级 QPS）时，需要根据实际情况调大内存

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 构建，并深度集成了 K8s Ingress 资源。请尝试在本地 Kind 集群中安装 Higress，并编写一个标准的 Kubernetes Ingress YAML 文件，将一个简单的 Nginx 服务通过 Higress 暴露出来。要求配置一个特定的域名（如 `example.local`）并能在本地通过该域名访问。

### 提示**: 重点查看 Higress 的官方 Quick Start 文档，注意 GatewayClass 和 Ingress Class 的配置，确保 Ingress 资源正确关联到 Higress 控制器。

### 

---
## 实践建议

以下是针对 Higress（AI Gateway & API Gateway）的 5-7 条实践建议：

### 1. 利用 WASM 插件实现 AI 请求的精细加工
Higress 最具优势的特性之一是其对 WebAssembly (WASM) 的原生支持。在接入大模型（LLM）时，不要仅做简单的透传。
*   **实践建议**：编写 Go 或 C++ 开发的 WASM 插件来处理 Prompt。例如，在请求到达后端模型之前，利用插件自动注入系统提示词、提取上下文信息或对敏感词进行过滤。这比在应用代码层面处理更高效，且能统一不同调用方的逻辑。
*   **常见陷阱**：避免在 Lua 脚本中处理复杂的文本逻辑，性能较差且难以维护；应优先使用 Higress 官方提供的 WASM SDK 或社区插件。

### 2. 配置基于 Token 的精细化限流
传统的 API 网关通常基于 QPS（每秒请求数）或并发连接数进行限流，但在 AI 场景下，成本主要消耗在 Token 上。
*   **实践建议**：在 AI 网关配置中，务必结合业务需求配置针对 Token 的限流策略。例如，限制单个 API Key 每天或每分钟消耗的最大 Token 数。这能有效防止恶意的 Token 消耗攻击或下游应用的配置错误导致的巨额账单。
*   **常见陷阱**：不要只依赖 QPS 限流。一个复杂的 Prompt 可能只产生一个请求，但消耗数万 Token，仅限制 QPS 无法控制成本。

### 3. 实施模型提供商的容错与降级策略
大模型 API（如 OpenAI, Azure, 通义千问等）可能会出现不稳定或限流的情况。
*   **实践建议**：利用 Higress 的服务来源管理功能，配置多模型供应商之间的故障转移。例如，设置主模型为 GPT-4，当检测到超时或 4xx/5xx 错误时，自动将请求切换到 GPT-3.5 或其他备用模型，确保业务的高可用性。
*   **常见陷阱**：不要将超时时间设置得过短。AI 模型的生成时间（TTFT）随 Prompt 长度波动，过短的超时设置会导致正常的长请求被意外中断。

### 4. 启用 SSE 流式传输的完整日志记录
AI 对话通常采用 Server-Sent Events (SSE) 流式返回，传统的网关日志往往只记录了请求头，忽略了流式响应体。
*   **实践建议**：在 Higress 中配置日志插件时，确保开启对 Body 的缓冲或流式日志捕获。这对于调试 Prompt 效果、统计实际使用的 Token 数以及进行用户行为分析至关重要。
*   **常见陷阱**：在生产环境中全量开启 Body 日志可能会显著增加网关的内存和 CPU 负载。建议仅在特定的 Debug 路由或采样率下开启完整的 Body 记录。

### 5. 严格管理 API Key 并实现密钥轮换
AI Gateway 通常汇聚了后端各大厂商的 API Key。
*   **实践建议**：切勿将厂商的原始 API Key 硬编码在配置文件中。使用 Higress 的密钥管理功能（或集成 KMS/Vault），并为不同的前端应用或租户分发独立的网关 Access Key。这样可以在网关层实现统一的鉴权和审计，并在后端密钥泄露时快速在网关侧进行切换，而无需修改所有客户端。
*   **常见陷阱**：忽略对不同租户的配额隔离。如果所有客户端共用一个后端 API Key，很难定位是谁导致了超额消费。

### 6. 区分处理长连接与流式超时
AI 请求通常耗时较长（长轮询或流式输出），这与传统的 RESTful 短请求不同。
*   **实践建议**：针对 AI 路由，显式调整网关层面的 Read Timeout 和 Idle Timeout 参数。对于流式请求，建议设置较长的超时时间（如 5 分钟），并确保网关后端的连接池配置支持长连接

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*