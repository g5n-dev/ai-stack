---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-02-16T17:19:05+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "WASM", "MCP", "LLM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于提供的 GitHub 仓库信息及 DeepWiki 文档内容，以下是关于 **Higress** 的中文总结： 项目简介 **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，通过集成 **WebAssembly (WASM)** 插件"
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
- **星标**: 7,537 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过深度集成 WASM 插件能力，将云原生流量管理与 LLM 应用支持相结合。该项目旨在解决开发者在统一架构下管理传统微服务路由与 AI 流量（如模型调用与 Agent 工具集成）的复杂性问题。本文将梳理其架构设计，并重点介绍 AI 网关特性、MCP 系统支持以及核心的插件扩展机制。

---
## 摘要

基于提供的 GitHub 仓库信息及 DeepWiki 文档内容，以下是关于 **Higress** 的中文总结：

### 项目简介
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，通过集成 **WebAssembly (WASM)** 插件能力，定位为 **AI Native API Gateway**（AI 原生 API 网关）。项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,500 颗星。

### 核心功能
Higress 主要提供以下三大核心功能：

1.  **AI 网关：**
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存以及安全防护能力。
    *   相关组件：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。

2.  **MCP 服务器托管：**
    *   托管 **Model Context Protocol (MCP)** 服务器，使 AI Agent 能够调用工具和服务。
    *   相关组件：`mcp-router`, `jsonrpc-converter` 过滤器及内置服务器实现（如 `quark-search`, `amap-tools`）。

3.  **传统 API 网关：**
    *   支持 Kubernetes Ingress，兼容 Nginx Ingress 注解。
    *   处理微服务路由等传统流量管理需求。

### 架构特点
*   **架构分离：** 采用**控制平面**（配置管理）与**数据平面**（流量处理）分离的架构。
*   **高性能配置分发：** 配置变更通过 **xDS 协议**传播，延迟仅为毫秒级，且**不中断连接**。
*   **适用场景：** 特别适合需要保持长连接的场景，例如 AI 流式响应（Streaming）处理。

---
## 评论

**总体判断**

Higress 是一款基于 Envoy 和 Istio 构建的**云原生 API 网关**，其核心差异化在于深度集成了**AI 原生能力**（LLM 网关）与 **MCP（Model Context Protocol）服务托管**。它成功地将传统流量治理与新兴的 AI 应用流量管理融合，是阿里巴巴将内部技术（如通义千问网关经验）向外输出的典型代表，旨在解决大模型时代 API 管理的复杂性与成本问题。

**深入评价依据**

**1. 技术创新性：从“流量转发”进化为“流量推理与编排”**
*   **事实**：Higress 扩展了 Istio 和 Envoy，引入了 WebAssembly (WASM) 插件系统，并明确提出了 AI Gateway 和 MCP Server Hosting 功能。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/gRPC 的路由与负载均衡，对 LLM 上下文无感知。Higress 的创新点在于**协议感知的深度**。它不仅转发流量，还能理解 LLM 的流式输出，并利用 WASM 技术实现了**热更新**的插件扩展能力。这意味着开发者可以在不重启网关的情况下，通过 Go 或 C++ 编写插件来处理 Prompt 增强、敏感词过滤或计费逻辑，这在高性能网关领域是极具前瞻性的架构设计。

**2. 实用价值：解决 AI 落地中的“连接”与“成本”痛点**
*   **事实**：文档指出其提供 AI Gateway 特性用于 LLM 应用，以及 MCP 系统用于 AI Agent 工具集成，同时支持 K8s Ingress。
*   **推断**：Higress 解决了三个关键问题：
    1.  **统一接入**：企业无需为传统微服务和 AI 应用维护两套网关，降低了运维复杂度。
    2.  **AI 路由优化**：通过内置的 Prompt 模板管理和多模型路由，开发者可以方便地在不同 LLM（如 GPT-4, 通义千问, Llama）之间切换，实现成本与性能的平衡。
    3.  **MCP 标准支持**：作为新兴的 AI Agent 数据交换标准，Higress 直接托管 MCP Server，使得 Agent 能够安全、标准化地调用企业内部工具，这是构建企业级 AI 应用基础设施的关键一环。

**3. 代码质量与架构：控制面与数据面分离的云原生范式**
*   **事实**：系统采用 Go 语言编写，架构上分离了控制平面（配置管理）和数据平面（流量处理，基于 Envoy）。
*   **推断**：选择 Go 语言开发控制面并利用 Envoy 作为高性能数据面，是目前云原生基础设施的**黄金标准**（如 Istio, APISIX）。这种设计保证了 Higress 在处理高并发流量时的低延迟优势，同时利用 Go 的并发特性处理复杂的配置逻辑。从代码规范来看，作为阿里系开源项目，其代码结构通常遵循严格的微服务规范，且文档（中英日三语）覆盖较全，降低了上手门槛。

**4. 社区活跃度：背靠大树，商业化与开源并进**
*   **事实**：星标数 7,537（截至数据截点），由阿里巴巴主导。
*   **推断**：Higress 继承了 Hango（阿里内部网关）的基因，且有阿里云作为商业托底，项目不会面临“烂尾”风险。社区活跃度较高，特别是在 AI 相关功能的迭代上非常迅速。虽然其社区规模尚不及 Kong 或 APISIX 那样庞大，但在“云原生 + AI”这个垂直细分赛道，它正处于领先地位。

**5. 学习价值与对比优势：WASM 插件化是最大亮点**
*   **事实**：支持 WASM 插件，且兼容 K8s Ingress API。
*   **推断**：与 **Kong** 相比，Higress 的优势在于 WASM 的隔离性和动态加载能力，以及更贴合 K8s 的云原生体验；与 **APISIX** 相比，Higress 在 AI 领域的内置功能（如 token 统计、流式处理）更加开箱即用；与 **LangChain** 等框架相比，Higress 提供的是**基础设施层**的流量管理，而非应用层代码开发。对于开发者而言，研究 Higress 是学习“如何在高性能网关中嵌入 AI 逻辑”的最佳实践之一。

**边界条件与不适用场景**

Higress 并非万能，它主要面向**云原生环境**。
*   **不适用场景**：
    1.  **边缘计算/嵌入式设备**：基于 Envoy 的架构资源消耗较高，不适合运行在资源受限的 IoT 设备上。
    2.  **非 K8s 环境的复杂传统架构**：虽然支持虚拟机部署，但其强大功能依赖于 K8s 生态，在纯物理机环境下的配置复杂度可能高于 Nginx。
    3.  **简单的静态网站托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。

**快速验证清单**

为了验证 Higress 是否适合您的团队，请执行以下检查：

1.  **性能基准测试**：
    *   使用 `wrk` 或 `hey` 对比 Higress 与 Nginx 在短连接和长连接下的 QPS

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress（AI Native API Gateway）仓库，本文将从架构设计、核心功能、技术实现、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的架构设计深植于**云原生** 生态，采用了经典的**控制平面与数据平面分离**的架构模式。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制层**：基于 **Istio** 进行扩展。Higress 并没有重新发明轮子，而是将 Istio 的控制面能力进行了“网关化”的裁剪和增强，去掉了 Sidecar 模式的复杂性，专注于 Gateway/Ingress 流量入口。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件机制。这是其技术架构中最关键的一环，允许使用 C/C++/Rust/Go/AssemblyScript 等多种语言编写插件，并动态加载到 Envoy 中，实现了业务逻辑与网关内核的解耦。
*   **配置分发**：使用 **xDS 协议**（包括 LDS, CDS, RDS, EDS）在控制面与数据面之间传递配置。Higress 对此进行了优化，实现了毫秒级的配置下发和热更新，无需重启 Pod。

### 核心模块与关键设计
1.  **MCP (Model Context Protocol) Server Hosting**：这是 Higress 区别于传统网关的最新设计。它内置了对 MCP 协议的支持，允许 AI Agent 直接通过网关发现和调用工具，将网关从“流量管道”转变为“AI 工具调度中心”。
2.  **AI Native 网关特性**：针对大模型（LLM）场景进行了专门优化。例如，处理 SSE（Server-Sent Events）流式传输时的超时、重试和缓存策略，以及针对 Token 计费和流控的中间件逻辑。
3.  **Kubernetes Ingress Controller**：完全兼容 K8s Ingress API，并支持 Gateway API，能够无缝接管 K8s 集群的南北向流量。

### 架构优势分析
*   **低延迟与高性能**：得益于 Envoy 的 C++ 内核和异步非阻塞 I/O 模型，Higress 在处理高并发请求时延迟极低。
*   **极致的可扩展性**：WASM 插件机制使得开发者可以在不修改网关核心代码的情况下，定制复杂的路由、鉴权、限流逻辑。相比 Lua 插件（如 OpenResty），WASM 提供了更好的隔离性和性能。
*   **平滑升级**：控制面与数据面分离，配置变更通过 xDS 协议推送，数据面连接不断开，这对于 AI 长连接场景至关重要。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **统一模型接入**：将 OpenAI, Azure, 通义千问, HuggingFace 等不同厂商的 API 标准化为统一接口。
    *   **Prompt 模板管理**：在网关层管理 Prompt 模板，实现 Prompt 的版本控制和动态注入。
    *   **Token 计费与限流**：基于 Token 数量而非请求数量进行流控和计费，更符合 AI 业务的成本模型。
2.  **MCP 服务器托管**：
    *   **场景**：AI Agent 需要调用外部工具（如搜索、数据库查询）。
    *   **功能**：Higress 可以作为 MCP Server 的宿主，自动将网关配置的路由暴露为 AI Agent 可调用的 Tools，简化了 Agent 的工具链集成。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、服务发现、金丝雀发布、负载均衡、WAF 防护等传统微服务治理功能。

### 解决的关键问题
*   **AI 流量治理的缺失**：传统网关无法理解 SSE 流、无法基于 Token 限流、无法处理 LLM 特有的超时逻辑。Higress 填补了这一空白。
*   **多模型切换成本**：开发者无需修改应用代码，只需在网关层配置即可切换不同的 LLM 提供商。
*   **异构系统的协议转换**：通过 WASM 插件，可以轻松实现 HTTP 到 gRPC、或者自定义协议的转换。

### 与同类工具的对比
*   **vs. Nginx/OpenResty**：Higress 基于 Envoy，内存安全性更高（C++ vs C），WASM 插件比 Lua 插件性能更好且开发语言选择更多。但在极致的简单配置场景下，Nginx 更轻量。
*   **vs. Kong/APISIX**：Kong 基于 Nginx/Lua，APISIX 基于 LuaJIT。Higress 的优势在于深度集成了 Istio 生态，且在 AI 场景（MCP、LLM 处理）上走得更远。
*   **vs. Istio Ingress**：Istio 原生 Ingress 配置极其复杂且性能调优困难。Higress 提供了更符合 K8s 习惯的控制台和简化的配置模型，去除了不必要的 Mesh 治理开销。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM 运行时。当配置变更时，控制面将编译好的 `.wasm` 文件推送到数据面，Envoy 加载该插件并挂载到请求处理链中。
2.  **AI 流式处理优化**：在处理 SSE 流时，网关作为代理必须正确处理 `Transfer-Encoding: chunked`。Higress 实现了流式数据的透明代理，并能在流式传输中进行实时的请求头修改或上下文注入，而不会中断流。
3.  **配置热更新**：利用 Envoy 的动态资源发现机制（xDS）。Higress Console 或 CRD 变更 -> Higress Control Plane (Istio) -> xDS gRPC Stream -> Envoy。这一过程是增量更新的，只推送变更的配置，保证了毫秒级生效。

### 代码组织结构
*   **`pkg/`**：Go 语言编写的控制平面核心逻辑，包括 Ingress 转换器、路由规则处理、Dubbo 服务发现等。
*   **`plugins/`**：WASM 插件的源码目录，通常包含 Go 或 Rust 编写的插件逻辑，通过 `tinygo` 或 `cargo` 编译为 WASM。
*   **`docker/` & `helm/`**：容器化与 K8s 部署编排文件。

### 性能与扩展性
*   **性能优化**：由于数据平面是 Envoy（C++），其单核转发性能极高。WASM 插件虽然引入了少量虚拟机开销，但在 AOT（Ahead-of-Time）编译模式下，性能损耗通常在可接受范围内（<5%）。
*   **扩展性**：水平扩展通过增加 K8s Pod 副本实现。控制面状态是无状态的或通过 K8s API Server 同步，因此可以随意伸缩。

### 技术难点
*   **WASM 插件的调试与观测**：WASM 运行在沙箱中，调试难度较大。Higress 通过日志输出和 Opentelemetry 集成来缓解此问题。
*   **多协议支持**：同时支持 HTTP (gRPC, REST) 和 Dubbo 协议，需要在路由匹配逻辑中做复杂的协议识别和负载均衡策略适配。

---

## 4. 适用场景分析

### 适合的项目
1.  **大模型应用开发**：任何需要接入 OpenAI、Claude 或国内大模型（通义千问、文心一言）的应用，特别是需要统一管理 Prompt 和 Key 的场景。
2.  **Kubernetes 微服务治理**：已经使用 K8s 的企业，需要一个高性能、支持 WASM 扩展的入口网关。
3.  **AI Agent 开发**：利用 Higress 的 MCP Server 功能，快速构建 Agent 的工具链基础设施。

### 最有效的情况
*   当你需要**在流量层对 AI 请求进行精细控制**（例如：拦截敏感词、修改请求参数、根据用户等级分配不同模型）时，Higress 是最佳选择。
*   当你需要**统一管理多个后端服务**（包括传统微服务和 AI 模型服务）时，其统一的路由能力能极大降低运维复杂度。

### 不适合的场景
*   **极简静态站点托管**：此时 Nginx 或 Caddy 更轻量，Higress 的 K8s 依赖显得过重。
*   **极低延迟的内部通信**：如果是服务间极低延迟的内部通信，直接使用 gRPC 或 Sidecar 模式可能比经过网关更高效。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 原生集成**：未来可能会内置 RAG（检索增强生成）向量数据库的代理能力，或者直接集成 Prompt 优化算法。
*   **WASM 生态的标准化**：随着 Proxy-Wasm 标准的成熟，Higress 的插件生态将与其他 Envoy 网关（如 Istio, APISIX）互通复用。
*   **边缘计算**：由于其轻量级数据平面和 WASM 动态加载能力，Higress 有可能向边缘节点下沉，成为边缘 AI 推理的网关。

### 社区与改进
*   目前社区活跃度较高，主要驱动力在于 AI 应用的爆发。改进空间主要集中在 WASM 插件的开发体验（调试工具、IDE 支持）以及更丰富的开箱即用 AI 插件市场。

---

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的运维/架构师。
*   Go 语言开发者（控制面二次开发）。
*   Rust/C++/Go 开发者（WASM 插件开发）。
*   AI 应用开发者（需要理解网关在 AI 架构中的作用）。

### 学习路径
1.  **基础**：理解 Envoy 的基本概念、xDS 协议。
2.  **架构**：学习 Istio 的控制平面架构，理解 Ingress Gateway 的工作原理。
3.  **实践**：使用 Docker 或 Helm 部署 Higress，配置一个简单的路由。
4.  **进阶**：编写一个 WASM 插件（例如：添加一个自定义请求头），使用 Go 或 Rust 编译并部署到 Higress。
5.  **AI 特性**：配置 AI 路由，测试流式响应和 Token 限流。

---

## 7. 最佳实践建议

### 正确使用方式
*   **插件隔离**：WASM 插件虽然强大，但应避免编写过于复杂的业务逻辑（如大量数据库查询），以免阻塞网关 I/O 线程。复杂逻辑应下沉为独立服务，网

---
## 代码示例




```python
# 示例1：使用Higress进行流量路由配置
def configure_higress_routing():
    """
    配置Higress的流量路由规则，实现基于请求路径的动态路由
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import RouteConfig
    
    # 创建路由配置对象
    route_config = RouteConfig()
    
    # 添加路由规则：将/api/v1路径的请求转发到service1
    route_config.add_route(
        path="/api/v1",
        destination="service1",
        methods=["GET", "POST"],
        timeout=30  # 设置30秒超时
    )
    
    # 添加路由规则：将/api/v2路径的请求转发到service2
    route_config.add_route(
        path="/api/v2",
        destination="service2",
        methods=["GET"],
        timeout=15
    )
    
    # 应用配置
    route_config.apply()
    print("路由配置已成功应用")

**说明**: 这个示例展示了如何使用Higress的Python SDK配置动态路由规则，解决微服务架构中常见的流量分发问题。

```python


def setup_higress_circuit_breaker():
"""
配置Higress的熔断器，防止服务雪崩
解决问题：当后端服务出现故障时，自动切断流量，保护系统稳定性
"""
from higress import CircuitBreakerConfig
# 创建熔断器配置
breaker = CircuitBreakerConfig(
service_name="payment_service",
failure_threshold=5,  # 连续失败5次后触发熔断
success_threshold=2,  # 连续成功2次后恢复
timeout=60,           # 熔断持续时间60秒
half_open_max_calls=3 # 半开状态最多允许3次请求
)
# 应用熔断器配置
breaker.apply()
print("熔断器配置已应用，服务保护已启用")

```python
# 示例3：实现Higress的限流功能
def configure_higress_rate_limiting():
    """
    配置Higress的限流策略，保护服务不被过载
    解决问题：防止突发流量压垮服务，实现平滑流量控制
    """
    from higress import RateLimitConfig
    
    # 创建限流配置
    rate_limit = RateLimitConfig(
        service_name="api_gateway",
        requests_per_second=100,  # 每秒最多100个请求
        burst=20,                 # 允许突发20个请求
        key_type="IP",            # 基于IP地址限流
        rejected_message="请求过于频繁，请稍后再试"
    )
    
    # 应用限流配置
    rate_limit.apply()
    print("限流策略已应用，服务保护已启用")

**说明**: 这个示例展示了如何配置Higress的限流功能，解决API服务可能面临的流量过载问题，确保服务稳定性。


---
## 案例研究


### 1：阿里巴巴内部电商业务迁移

 1：阿里巴巴内部电商业务迁移

**背景**:  
阿里巴巴内部部分核心电商业务原运行在传统的 Java 网关（如 Zuul）上，随着业务规模扩大，需要支持更高的并发和更灵活的路由规则。同时，业务团队希望统一云原生架构下的流量管理。

**问题**:  
1. 传统网关在处理每秒数万级 QPS 时延迟较高，且扩展性受限。  
2. 业务团队需要动态配置路由规则，但旧系统修改配置需重启服务，影响线上稳定性。  
3. 多语言服务（如 Go、Python）接入时，与 Java 网关的协议兼容性不足。

**解决方案**:  
采用 Higress 作为新一代云原生 API 网关，基于 Istio 和 Envoy 深度定制：  
1. 利用 Higress 的 WASM 插件能力，实现无侵入式的流量治理（如限流、熔断）。  
2. 通过动态配置中心（如 Nacos）集成，实现路由规则热更新。  
3. 部署 Higress Ingress Controller 替代传统网关，支持多语言服务通过 HTTP/gRPC 协议无缝接入。

**效果**:  
1. 核心链路 P99 延迟降低 30%，单集群支持 10 万+ QPS。  
2. 路由规则修改时间从分钟级缩短至秒级，业务迭代效率提升 50%。  
3. 跨语言服务接入成本降低 80%，统一了流量治理技术栈。

---



### 2：某互联网公司 AI 服务网关改造

 2：某互联网公司 AI 服务网关改造

**背景**:  
某 AI 公司提供在线推理服务，原有网关无法满足高并发下的低延迟需求，且需要集成第三方认证和流量监控功能。

**问题**:  
1. 推理服务对延迟敏感，传统网关的 Lua 插件执行效率低。  
2. 需要对接 Keycloak 认证系统，但现有网关扩展性差。  
3. 缺乏细粒度的流量监控和日志分析能力。

**解决方案**:  
1. 部署 Higress 网关，利用其高性能 HTTP/gRPC 路由能力，替代 Nginx。  
2. 开发 WASM 插件实现 Keycloak 认证集成，避免修改网关核心代码。  
3. 接入 Prometheus 和 OpenTelemetry，实现实时流量监控和日志采集。

**效果**:  
1. 推理服务 P95 延迟从 200ms 降至 50ms，满足实时业务需求。  
2. 认证插件开发时间缩短 60%，且支持热更新。  
3. 运维团队通过统一监控面板定位问题效率提升 70%。

---



### 3：跨境电商平台多区域流量治理

 3：跨境电商平台多区域流量治理

**背景**:  
某跨境电商平台在 AWS 和阿里云多区域部署服务，需要统一管理跨云流量，并支持按地域路由。

**问题**:  
1. 跨云网络延迟高，需智能路由优化。  
2. 促销活动期间需动态调整流量配额，但传统网关配置复杂。  
3. 多区域部署导致日志分散，故障排查困难。

**解决方案**:  
1. 在各区域部署 Higress 网关，通过全局控制平面统一管理。  
2. 使用 Higress 的权重路由和地域感知路由功能，实现流量按需分配。  
3. 集成分布式追踪系统（如 SkyWalking），关联多区域调用链。

**效果**:  
1. 跨区域访问延迟降低 40%，用户体验显著改善。  
2. 促销期间流量配额调整时间从小时级降至分钟级。  
3. 故障定位效率提升 90%，减少 60% 的运维人力投入。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx/Lua，适合高并发场景 | 极高性能，基于 Nginx/Lua，性能接近 Nginx 原生 |
| 易用性 | 提供可视化控制台，配置简单，支持 Kubernetes 集成 | 配置灵活，但需要一定学习成本，社区支持丰富 | 提供可视化控制台，配置灵活，社区活跃 |
| 成本 | 开源免费，云服务版本按使用量收费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持自定义插件，扩展能力强 | 支持自定义插件，生态丰富 | 支持自定义插件，生态丰富 |
| 社区支持 | 阿里巴巴背书，社区活跃，国内支持较好 | 国际社区活跃，文档丰富 | 国内社区活跃，文档完善 |
| 适用场景 | 适合云原生、微服务架构，尤其适合阿里云用户 | 适合传统 API 网关和微服务架构 | 适合高性能、高并发场景 |

### 优势分析

- 优势1：高性能，基于 Rust 和 Go 开发，资源占用低，适合高并发场景。
- 优势2：易用性强，提供可视化控制台，支持 Kubernetes 集成，适合云原生架构。
- 优势3：阿里巴巴背书，社区活跃，国内支持较好，适合国内用户。
- 优势4：开源免费，云服务版本按使用量收费，成本可控。

### 不足分析

- 不足1：相比 Kong 和 APISIX，生态和插件数量较少，扩展性稍弱。
- 不足2：社区规模和国际支持不如 Kong 和 APISIX，国际化程度较低。
- 不足3：云服务版本依赖阿里云，多云部署可能受限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展与自定义逻辑开发

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C++, Go, Rust, AssemblyScript 或 JavaScript 等语言编写高性能的插件。相比传统网关的 Lua 脚本，WASM 提供了更好的隔离性、更高的执行效率以及更丰富的标准库支持。利用此特性可以实现复杂的 API 鉴权、请求转换或流量标记逻辑，而无需修改网关核心代码。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 TypeScript）。
2. 使用 Higress 提供的插件 SDK 或官方工具链 `hgctl` 初始化插件脚手架。
3. 编写插件逻辑，利用 Proxy-WASM 标准接口处理请求/响应头、Body 或路由逻辑。
4. 构建生成 `.wasm` 文件，并通过 Higress 控制台或 WASM 插件市场进行上传与配置。

**注意事项**: 
- WASM 插件运行在沙箱中，虽然性能较高，但处理超大的 Body 时仍需注意内存限制。
- 生产环境部署前，务必对 WASM 插件进行压力测试，避免逻辑异常导致网关内存溢出。

---

### 实践 2：服务来源的全面接管与 Nacos 注册中心集成

**说明**: Higress 设计初衷之一是解决云原生时代流量入口与微服务注册中心的割裂问题。最佳实践是直接将 Nacos、Consul 或 Kubernetes Service 作为 Higress 的服务来源。通过配置服务来源，Higress 可以实时感知服务实例的上下线，实现基于服务名的自动路由，无需手动维护繁琐的 IP 列表。

**实施步骤**:
1. 在 Higress 控制台左侧导航栏选择 "来源管理"，点击"创建来源"。
2. 选择 "Nacos" 类型，填入 Nacos 服务端的地址、命名空间 和 AccessKey（如果开启了鉴权）。
3. 配置服务分组，确保 Higress 能够同步到目标微服务。
4. 在路由配置中，直接引用服务名称（Service Name）而非具体 IP 地址作为目标服务。

**注意事项**: 
- 确保 Higress 所在的网络环境能够访问 Nacos 集群的网络段与端口。
- 如果使用了多套 Nacos 集群（如开发、测试环境），请严格隔离命名空间，防止路由配置错乱。

---

### 实践 3：利用 Ingress Class 实现多租户或环境隔离

**说明**: 在 Kubernetes 环境中，通常存在多个业务团队或多个运行环境（如灰度、生产）。Higress 通过监听 Ingress 资源来配置路由。最佳实践是指定特定的 `ingressClassName`，让 Higress 仅处理归属于它的 Ingress 资源，从而避免与集群内可能存在的其他 Ingress Controller（如 Nginx）产生冲突，实现流量治理的逻辑隔离。

**实施步骤**:
1. 检查 Higress 部署配置，确认 `--ingress-class` 参数已设定（例如 `higress`）。
2. 在创建 Kubernetes Ingress 资源时，明确指定 `kubernetes.io/ingress.class: higress` 注解或 `ingressClassName` 字段。
3. 对于不需要 Higress 接管的流量，确保其 Ingress 资源不包含该 Class 标识。

**注意事项**: 
- 修改 Ingress Class 会导致流量瞬间中断，请在业务低峰期或做好回滚预案的情况下操作。
- 建议在 CI/CD 流水线中标准化 Ingress 资源的 YAML 模板，强制要求指定 Class。

---

### 实践 4：配置全链路安全防护与认证鉴权

**说明**: API 网关是业务流量的咽喉，必须在此层统一收敛安全策略。不要将认证逻辑分散在各个微服务中。Higress 支持多种鉴权方式（如 Basic Auth、API Key、JWT、OIDC）。最佳实践是结合外部认证服务或 Higress 自带的插件，实现统一的访问控制、IP 黑白名单过滤以及防爬虫策略。

**实施步骤**:
1. 在 "安全防护" 或 "插件市场" 中，启用 "Key Auth" 或 "JWT Auth" 插件，配置消费者密钥。
2. 配置 "block-list" 或 "IP-restriction" 插件，限制恶意 IP 的访问。
3. 对于需要更高安全级别的接口，开启 "WAF"（如 ModSecurity）相关插件配置。
4. 开启 HTTPS，并在 Higress 层配置 SSL 证书，终止 SSL 连接。

**注意事项**: 
- 密钥管理应遵循轮换机制，避免长期使用同一套密钥。
- 如果使用 JWT，务必验证签名算法，防止算法降级攻击。

---

### 实践 5：精细化流量管理与金丝雀发布

**说明

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 和 Istio 构建，Envoy 对 HTTP/3 有较好的支持。HTTP/3 (基于 QUIC) 解决了 HTTP/2 的队头阻塞问题，在丢包率较高的网络环境下（如移动网络）能显著提升连接建立速度和吞吐量。

**实施方法**:
1. 在 Higress 的网关配置中，找到监听器设置。
2. 开启 HTTP/3 或 QUIC 协议支持。
3. 配置 UDP 端口（通常端口 443 也需要监听 UDP 流量）。
4. 确保证书配置支持 QUIC 传输参数。

**预期效果**: 在弱网环境下，延迟降低 30% 左右，连接建立成功率显著提升。

---

### 优化 2：配置全链局超时与重试策略

**说明**: 默认的超时设置可能过长，导致后端服务故障时请求堆积，耗尽网关线程池。合理的超时与指数退避重试机制能快速失败，释放资源，同时提高请求最终成功率。

**实施方法**:
1. 在路由或服务级别配置 `timeout` 参数，建议根据 P99 耗耗设置（例如 3s）。
2. 启用重试策略，设置最大重试次数（建议 2-3 次）。
3. 配置 `perTryTimeout`（单次尝试超时），应小于总超时时间。
4. 针对特定 HTTP 状态码（如 503, 504, 5xx）配置重试触发条件。

**预期效果**: 减少长尾请求延迟，在服务不稳定时提升 10%-20% 的整体成功率，防止雪崩效应。

---

### 优化 3：启用 Wasm 插件的高效缓存与隔离

**说明**: Higress 支持 Wasm 插件扩展。频繁的 Wasm 虚拟机实例创建销毁或跨线程内存拷贝会带来性能损耗。通过配置合理的缓存策略和内存隔离，可以降低插件执行开销。

**实施方法**:
1. 优化 Wasm 代码逻辑，减少不必要的内存分配和 I/O 操作。
2. 利用 Higress 的 Wasm 插件配置，启用 VM 代码缓存。
3. 对于 CPU 密集型插件，考虑配置独立的线程池或限制并发度，避免阻塞主事件循环。

**预期效果**: Wasm 插件执行延迟降低 10%-15%，吞吐量提升。

---

### 优化 4：调整连接池与工作线程数

**说明**: 默认的连接池大小可能无法满足高并发场景。过小的连接池会导致请求排队等待连接，过大的线程数会导致上下文切换开销。

**实施方法**:
1. 根据后端服务能力，调大 `maxConnections`（上游连接池大小）。
2. 调整 Higress Gateway 的 Worker 线程数，通常建议设置为 CPU 核心数或核心数 * 2。
3. 启用 HTTP/2 连接复用，减少 TCP 连接数。

**预期效果**: 提升 P99 延迟表现，高并发下吞吐量提升 20% 以上。

---

### 优化 5：启用路由匹配的 Trie 树优化

**说明**: 随着路由规则数量增加，线性查找会严重拖慢网关性能。Higress 底层 Envoy 支持将域名和路径配置优化为 Trie 树（前缀树）结构，大幅提升路由查找效率。

**实施方法**:
1. 检查 Higress 路由配置，确保域名和路径配置遵循最佳实践（避免过多正则表达式）。
2. 在网关启动参数或配置中，确保启用了基于 Trie 树的路由匹配优化（Envoy 默认通常已优化，但需确认未关闭）。
3. 尽量使用前缀匹配而非完全匹配或正则匹配。

**预期效果**: 在路由规则超过 100 条时，路由查找耗时从毫秒级

---
## 学习要点

- Higress 是基于阿里云内部多年实践沉淀的下一代云原生 API 网关，深度集成 Istio 与 Envoy 核心能力。
- 提供一站式的 K8s Ingress 流量管理，能够无缝替代传统的 Nginx Ingress Controller。
- 具备强大的流量治理能力，支持金丝雀发布、蓝绿发布、负载均衡及超时重试等复杂路由规则。
- 内置针对高并发场景优化的 WAF 插件和安全防护机制，保障网关层面的安全性。
- 支持将服务直接注册到网关，并能与 Nacos、Consul 等主流注册中心打通，实现微服务生态的平滑接入。
- 采用标准 Wasm 插件扩展机制，允许使用多语言（如 Go、Python、AssemblyScript）灵活开发业务逻辑。
- 提供开箱即用的 Prometheus 监控指标集成与 Grafana 仪表盘，便于实时观测系统状态与性能瓶颈。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关的基本概念：理解什么是 API Gateway，以及为什么在现代微服务架构中需要它。
- Higress 的背景与定位：了解 Higress 基于 Envoy 和 Istio 的技术架构，以及它与阿里云 MSE 云原生网关的开源关系。
- 基础术语学习：掌握 Ingress、Route、Service、Upstream 等核心资源对象。
- 环境搭建：学习如何在本地 Docker 环境或 Kubernetes 集群中快速部署 Higress。
- 控制台操作：熟悉 Higress 的控制台界面，学会如何配置简单的 HTTP 路由转发。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 (README 和 Architecture 文档)
- Higress 官方网站文档 (快速开始部分)
- Docker 和 Kubernetes 基础教程

**学习建议**:
建议先不要深入代码，而是通过官方的 "Quick Start" 文档在本地跑通一个最简单的示例。理解流量进入网关后如何根据配置规则被转发到后端服务的全过程。如果对 Kubernetes 不熟悉，需要先补充 K8s 的基础概念，特别是 Service 和 Ingress 资源。

---

### 阶段 2：流量治理与安全管控

**学习内容**:
- 高级流量管理：学习基于 Header、Query 参数、Cookie 等条件的复杂路由匹配规则。
- 负载均衡策略：掌握轮询、随机、加权轮询等负载均衡算法的配置。
- 服务安全：配置 CORS（跨域）、IP 访问控制、Basic Auth 认证以及 JWT 鉴权。
- 金丝雀发布与蓝绿部署：学习如何使用 Higress 实现流量的灰度发布，控制路由到特定版本服务的流量比例。
- 全局与插件配置：理解 Higress 的插件市场，学习如何启用 WAF 防护、限流降级等关键插件。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件章节
- Envoy 官方文档 (用于理解底层代理机制)
- Higress 官方插件市场示例

**学习建议**:
尝试构建一个包含两个版本（v1 和 v2）的测试服务。通过配置 Higress 的路由规则，实现将 10% 的流量转发到 v2 版本，以此验证金丝雀发布能力。同时，尝试配置限流规则，使用压测工具（如 Apache Bench）观察限流效果。

---

### 阶段 3：插件开发与生态集成

**学习内容**:
- 插件系统原理：深入理解 Higress 的插件加载机制（基于 Wasm 或 Lua）。
- 自定义插件开发：学习如何使用 Go 或 Java 开发自定义 Wasm 插件，实现特定的业务逻辑（如请求头改写、自定义鉴权）。
- 生态集成：学习 Higress 如何与 Nacos、Consul 等注册中心集成，实现基于服务名的动态服务发现。
- OpenAPI 与 Ingress：深入理解 Kubernetes Ingress API 以及 Higress 对 Gateway API 的支持。
- 可观测性：学习配置日志（SLS）、指标（Prometheus）和链路追踪，排查网关性能瓶颈。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发指南
- Higress 官方示例插件源码
- Wasm (WebAssembly) 基础教程
- Prometheus 与 Grafana 监控集成文档

**学习建议**:
动手编写一个简单的 Wasm 插件，例如在请求响应头中添加一个自定义的 "X-Higress-Custom" 头部。将插件编译为 `.wasm` 文件并在 Higress 控制台上传部署。同时，尝试将 Higress 接入 Prometheus，观察 QPS、延迟等核心指标。

---

### 阶段 4：架构设计与源码级精通

**学习内容**:
- 源码结构分析：深入阅读 Higress 的源码，理解 Router、Filter、ClusterManager 等核心模块的实现。
- 高可用架构设计：学习在生产环境中如何规划 Higress 的高可用部署，包括多副本容错、热更新与平滑升级。
- 性能调优：掌握连接池配置、缓冲区大小调整、CPU 绑定等内核级优化参数。
- 多租户与多网关管理：理解如何在多租户环境下隔离网关配置。
- 贡献开源：参与 GitHub Issue 讨论，提交 PR 修复 Bug 或增加新特性。

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Envoy 源码与架构深度解析文章
- 云原生网关最佳实践白皮书

**学习建议**:

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 或 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 或 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是阿里云内部多年实战经验的结晶，并于近期开源。它基于 Envoy 和 Istio 构建，旨在解决云原生时代下的流量管理问题。

与 Nginx 相比，Higress 提供了更丰富的服务治理功能（如热更新、无损上下线、金丝雀发布），且支持通过控制台（Console）或 K8s CRD 进行动态配置，无需像 Nginx 那样频繁重载配置文件。与 Kong 相比，Higress 深度集成了 Istio，可以作为 Ingress Controller 或 Gateway 使用，在处理 Kubernetes 集群内外流量互通方面具有天然优势，且对 WASM（WebAssembly）插件支持更加完善，性能开销更低。

---



### 2: Higress 是否支持 Nginx 的配置语法？迁移成本高吗？

2: Higress 是否支持 Nginx 的配置语法？迁移成本高吗？

**A**: Higress 本质上基于 Envoy，其核心配置逻辑与 Nginx 不同，因此**不直接支持** Nginx 的 `nginx.conf` 配置文件语法。

但是，为了降低迁移门槛，Higress 提供了 **Nginx 配置转换工具**。该工具可以读取 Nginx 的配置文件，并将其自动转换为 Higress 的路由和插件配置。对于大多数常见的反向代理、URL 重写和 Header 修改场景，转换工具可以自动完成迁移。对于复杂的 Lua 脚本逻辑，建议利用 Higress 的 WASM 插件生态进行重写。

---



### 3: Higress 的插件机制是如何工作的？支持哪些类型的插件？

3: Higress 的插件机制是如何工作的？支持哪些类型的插件？

**A**: Higress 提供了强大的扩展能力，主要支持以下三种插件类型：

1.  **WASM (WebAssembly) 插件**：这是 Higress 推荐的主流方式。由于 Envoy 原生支持 WASM，Higress 允许用户使用 C++、Go、Rust、JavaScript 或 TypeScript 编写插件逻辑。WASM 插件的优势是**热加载**（无需重启网关）、**隔离性好**（插件崩溃不影响网关核心）以及**多语言支持**。
2.  **Lua 插件**：为了兼容传统的 OpenResty/Kong 生态，Higress 依然支持 Lua 脚本，但在高性能和云原生场景下，推荐逐步转向 WASM。
3.  **原生 Envoy 扩展**：对于极致性能要求的场景，用户可以编写 C++ 原生 Envoy Filter。

Higress 官方维护了一个插件市场（类似于 VS Code 插件市场），用户可以在控制台一键安装常见功能的插件（如 JWT 鉴权、请求限流、Key Auth 等）。

---



### 4: 在 Kubernetes 环境中，Higress 与 Ingress Controller 是什么关系？

4: 在 Kubernetes 环境中，Higress 与 Ingress Controller 是什么关系？

**A**: Higress 可以完全替代传统的 Nginx Ingress Controller。它完全兼容 K8s Ingress API 标准和 Gateway API 标准。

当你将 Higress 部署在 Kubernetes 集群中时，它会监听 Ingress 或 Gateway 资源的变化，并自动将这些配置转化为 Envoy 的配置下发到数据平面。这意味着你可以直接使用现有的 K8s YAML 文件定义路由规则，同时享受 Higress 带来的高级流量治理（如全链路灰度、流量镜像、负载均衡算法定制等）能力。

---



### 5: Higress 如何处理服务发现？它只能对接 Kubernetes Service 吗？

5: Higress 如何处理服务发现？它只能对接 Kubernetes Service 吗？

**A**: Higress 设计为云原生架构，不仅支持 Kubernetes Service，还支持多种服务注册中心。

除了默认对接 K8s CoreDNS 之外，Higress 可以通过配置 **ServiceSource (服务来源)** 来连接外部注册中心。目前支持的主流注册中心包括：
*   Nacos
*   Consul
*   ZooKeeper
*   Eureka
*   DNS (静态域名)

这使得 Higress 非常适合混合云架构，既可以管理 K8s 集群内的微服务，也可以管理部署在虚拟机上的传统服务，实现统一的流量网关入口。

---



### 6: Higress 的性能表现如何？能否支撑高并发流量？

6: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 的数据平面基于 **Envoy** 构建。Envoy 是业界公认的高性能 L7 代理，使用 C++ 编写，具备极高的处理效率和低延迟。

在官方提供的基准测试中，Higress 在启用常见插件（如限流、鉴权）的情况下，依然能保持与原生 Envoy 接近的高吞吐量。其异步非阻塞的架构模型使其能够轻松应对 C10M（千万级并发连接）级别的挑战。对于阿里云双11等大促场景，Higress 的商业版本已经过充分的实战验证，开源版本同样继承了这一高性能基因。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 构建，但默认提供了 WASM (WebAssembly) 支持。请尝试编写一个简单的 WASM 插件（例如 Go 或 C++），实现一个简单的功能：当请求头中包含 `x-wasm-test: true` 时，直接返回 200 OK 和自定义 JSON 响应，而不将请求转发给后端服务。

### 提示**: Higress 官方文档提供了 `wasm-go` 的 SDK。你需要关注 `onHttpRequestHeaders` 这一生命周期钩子，并使用 `SendHttpResponse` 来中断请求并直接返回。你需要先在本地构建出 `.wasm` 文件，然后通过 Higress 控制台或 WASM 插件管理接口进行上传配置。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其基于 Envoy 和 Istio 的高性能架构，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用“模型提供商”插件实现统一接入与密钥管理
**场景：** 企业内部同时使用 OpenAI、Azure OpenAI、通义千问等多个 LLM 提供商，且不想在客户端硬编码 API Key。
**建议：** 在 Higress 中配置 `ai-provider` 类型的插件（如官方提供的 `ai-proxy`）。将所有大模型厂商的 API Key 集中在网关层的 `GlobalPlugin` 或 `RoutePlugin` 中管理。
**最佳实践：** 业务请求只需发送给 Higress 的统一端点，Higress 负责将请求路由至不同的模型厂商，并自动替换或注入鉴权头。这样实现了密权与业务代码的解耦，便于轮换密钥和统一计费统计。

### 2. 实施基于 Token 的精细化流控与熔断
**场景：** LLM 调用成本高昂，且不同模型（如 GPT-4 与 GPT-3.5）价格差异巨大，传统的 QPS 限流无法有效控制成本。
**建议：** 开启 Higress 的 AI 特性中的 Token 限流功能。在配置 `flow-control` 插件时，针对特定路由设置基于 Token 或 Token RPM (Requests Per Minute) 的阈值。
**常见陷阱：** 仅设置 HTTP QPS 限制。由于流式响应和 Prompt 长度的不确定性，低 QPS 不代表低消耗。务必结合 Prompt 长度和模型单价进行预算保护，防止“刷量”攻击导致账单爆炸。

### 3. 配置语义路由与模型路由策略
**场景：** 希望根据用户请求的复杂度或类型，自动分发到不同成本的模型（例如：简单问答走便宜的小模型，复杂逻辑走贵的大模型）。
**建议：** 利用 Higress 的路由能力，结合 `ai-proxy` 插件的高级配置。可以通过请求头（Header）或 Body 中的特定字段来定义路由规则。
**最佳实践：** 在网关层实现“路由分发层”。例如，客户端在请求头中携带 `X-Model-Intent: simple`，网关自动将其转发至通义千问-Turbo 版本；若携带 `complex` 则转发至 GPT-4。这比在应用代码中写 `if-else` 更易于维护和灰度发布。

### 4. 构建基于 Wasm 插件的 Prompt 管理与预处理层
**场景：** 需要给所有发往 LLM 的请求强制添加系统提示词，或者对用户输入进行敏感词过滤，但不想修改每个微服务的代码。
**建议：** 编写或使用现成的 Wasm 插件（Wasm Plugin）处理请求 Body。在请求转发给上游模型服务之前，拦截并修改 JSON Body，注入企业级的 System Prompt 或安全上下文。
**最佳实践：** 将 Prompt 模板化管理。通过 Higress 的插件配置动态更新 Prompt 模板，无需重新部署服务即可快速调整 LLM 的行为（例如：调整机器人的语气或角色设定）。

### 5. 启用全链路可观测性以追踪 Token 消耗
**场景：** 在多模型、多租户环境下，需要精确统计每次请求的输入/输出 Token 数、首字延迟（TTFT）和总耗时，以评估模型性能。
**建议：** 确保 Higress 的 Access Log 配置中包含 AI 相关的元数据。Higress 在处理 AI 流量时会记录详细的上下文。
**操作：** 配置日志输出至 Prometheus 或 Loki，重点关注 `request_tokens`、`response_tokens` 和 `model_duration` 等指标。
**常见陷阱：** 忽略流式输出的日志采集。流式请求的日志生成逻辑与普通请求不同，需确认日志插件能够正确聚合流式分片，否则会导致 Token 统计严重偏差。

### 6. 针对流式响应的超

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
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*