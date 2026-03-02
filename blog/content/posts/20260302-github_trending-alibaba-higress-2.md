---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-02T05:21:09+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里开源", "Istio", "Envoy", "LLM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的中文总结： 项目概述 **Higress** 是一个由阿里巴巴开源的、**AI 原生** API 网关。该项目基于 **Istio** 和 **Envoy** 构建，采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,600 颗星。 核心定位 Hi"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,604 (+5 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构统一管理流量与服务。它不仅支持传统的 Kubernetes Ingress 和微服务路由，还针对 LLM 应用提供了 AI 网关特性，并集成了 MCP 服务器托管能力，适合需要在云原生环境中集成 AI 能力的开发者。本文将介绍其系统架构、核心组件及主要用例，帮助读者理解如何利用它实现高效、可扩展的 API 管理。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的中文总结：

### 项目概述
**Higress** 是一个由阿里巴巴开源的、**AI 原生** API 网关。该项目基于 **Istio** 和 **Envoy** 构建，采用 **Go** 语言编写，目前在 GitHub 上拥有超过 7,600 颗星。

### 核心定位
Higress 是一个云原生 API 网关，它通过扩展 **WebAssembly (WASM)** 插件能力，将传统的流量管理与新兴的 AI 应用需求相结合。

### 三大核心功能
1.  **AI 网关**
    *   为大语言模型（LLM）应用提供统一 API。
    *   支持对接 30+ 家 LLM 提供商。
    *   具备协议转换、可观测性、缓存和AI安全防护能力。
2.  **MCP 服务器托管**
    *   托管模型上下文协议（MCP）服务器。
    *   使 AI 智能体能够便捷地调用外部工具和服务（如搜索、地图等）。
3.  **标准 API 网关**
    *   提供 Kubernetes Ingress 控制器功能。
    *   兼容 Nginx Ingress 注解，支持微服务路由。

### 架构优势
*   **控制与数据分离**：架构分为控制平面（配置管理）和数据平面（流量处理）。
*   **高性能配置分发**：通过 xDS 协议传播配置变更，延迟仅为毫秒级。
*   **无缝连接**：配置变更过程不中断连接，非常适合 AI 长连接流式响应等场景。

---
## 评论

### 总体评价

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**结合得最彻底的开源项目之一。它不仅仅是一个基于 Istio/Envoy 的网关，更通过 WASM 和 MCP 协议，成功转型为大模型时代的流量入口与编排中枢，具有极高的技术前瞻性与工程实用价值。

---

### 深入评价维度

#### 1. 技术创新性：AI Native 架构与 WASM 的深度融合
*   **事实**：Higress 基于 Envoy 和 Istio 构建，核心差异化在于其 WebAssembly (WASM) 插件系统，并明确提出了 AI Gateway 和 MCP (Model Context Protocol) Server 托管功能。
*   **推断**：Higress 的创新点在于将**业务逻辑处理（WASM）**与**AI 协议处理**进行了底层解耦。传统的 API 网关通常将 LLM 请求视为普通 HTTP 流量，而 Higress 内置了对 AI 协议（如 OpenAI 协议）的理解，实现了诸如 Token 流式处理、Prompt 模板管理、结果缓存等 AI 特有的功能。此外，引入 MCP Server 托管能力，使其成为了 AI Agent 的基础设施，而不仅仅是流量管道，这显著拉高了网关的技术天花板。

#### 2. 实用价值：解决 LLM 落地中的“最后一公里”问题
*   **事实**：文档指出 Higress 提供 Kubernetes Ingress、微服务路由以及 AI Gateway 特性，星标数达到 7,604。
*   **推断**：在 AI 应用爆发前，企业需要两套网关：一套管微服务（如 Nginx/Kong），一套管大模型调用。Higress 的实用价值在于**统一**。
    *   **成本降低**：通过一个控制平面统一管理南北向（外部 API）和东西向（微服务）流量，同时接管 LLM 调用。
    *   **稳定性保障**：AI 服务不稳定是常态，Higress 提供的**重试、降级、多模型切换**（如从 GPT-4 无缝降级到 GPT-3.5）是生产环境刚需。
    *   **安全合规**：在企业内部，Higress 可以作为拦截器，在请求到达 LLM 之前进行敏感词过滤或数据脱敏，这是许多企业接入 AI 的前提条件。

#### 3. 代码质量与架构：云原生标准的控制面与数据面分离
*   **事实**：DeepWiki 提及架构分离了控制平面（配置管理）与数据平面（流量处理），核心语言为 Go。
*   **推断**：选择 Go 语言开发网关控制面是业界标准（利用其高并发特性），而数据面复用 Envoy C++ 内核保证了极致性能。从架构设计看，Higress 遵循了 Kubernetes Operator 模式，通过 CRD（自定义资源）来定义路由和插件配置，符合云原生“声明式 API”的最佳实践。WASM 的引入使得代码扩展性极高，用户可以用 C++/Go/Rust/JS 编写插件而无需重新编译网关主体，这在代码维护性上是一个巨大的进步。

#### 4. 社区活跃度：阿里背书与开源生态的双轮驱动
*   **事实**：项目由阿里巴巴主导，星标数 7,604，且提供了中、日、英多语言文档。
*   **推断**：作为阿里云内部网关产品的开源版本，Higress 继承了阿里巴巴在“双11”流量治理的深厚积累。多语言文档显示了其国际化的野心。虽然相比 Nginx 或 Kong 这样的老牌项目，其生态成熟度略逊一筹，但在“AI + Gateway”这一细分赛道，Higress 的社区活跃度和迭代速度处于领先地位，更新频率通常紧跟 LLM 厂商的 API 变更。

#### 5. 潜在问题与改进建议
*   **推断**：
    *   **复杂性曲线**：引入 Istio 和 WASM 虽然功能强大，但对于运维团队的知识储备要求极高。排查 WASM 插件的崩溃比排查 Lua 脚本要困难。
    *   **性能损耗**：WASM 插件在每次请求处理时存在一定的启动和执行开销，虽然比 Lua 快，但在极高 QPS 场景下，对延迟极其敏感的业务需要经过严格压测。
    *   **MCP 协议成熟度**：MCP 仍是一个较新的协议标准，Higress 对其托管功能的稳定性尚需时间验证。

#### 6. 对比优势：Higress vs. Kong/APISIX vs. Nginx
*   **推断**：
    *   **对比 Nginx**：Higress 具备动态配置能力（无需 Reload），且原生支持 K8s，Nginx 则需要配合复杂的 Lua 脚本或 OpenResty 才能实现类似功能。
    *   **对比 Kong/APISIX**：这三者都是优秀的云原生网关。但在 **AI 领域**，Kong 和 APISIX 更多是通过插件形式支持 AI，而 Higress 是**内核级**支持。例如，Higress 对 SSE（Server-Sent Events）流式传输的处理更原生，对 AI Token 计费、上下文截断等逻辑的处理更细腻。

---

### 边界条件与验证清单

#### 边界

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 定位为“AI Native API Gateway”，基于 Istio 和 Envoy 构建，旨在解决云原生架构下，特别是 AI 应用场景中的流量管理、服务治理和安全问题。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了标准的 **控制平面 + 数据平面** 分离架构。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制层**：基于 **Istio** 进行了大幅简化和增强。Higress 移除了 Istio 中繁重的 Sidecar 模式，转而采用更适合 API 网关的 **Centralized Ingress/Gateway** 模式。
*   **扩展机制**：核心亮点在于 **WebAssembly (WASM)** 技术的引入。WASM 作为沙箱运行环境，允许开发者使用 C/C++/Go/Rust 等语言编写插件，动态加载到 Envoy 中，实现了业务逻辑与网关内核的解耦。

### 核心模块与关键设计
1.  **Router (路由层)**：基于 Envoy Router Filter，支持 HTTP/gRPC/Dubbo 等协议，并针对 AI 场景扩展了 SSE (Server-Sent Events) 和 WebSocket 的长连接处理。
2.  **WASM Plugin System (插件市场)**：这是 Higress 的“护城河”。它提供了一个开箱即用的插件生态，包括认证鉴权、限流熔断、以及 AI 特有的 Prompt 装饰和 Key 管理。
3.  **MCP (Model Context Protocol) Server**：针对 AI Agent 场景，Higress 内置了 MCP 协议支持，能够作为工具提供方，将后端 API 暴露给 LLM 应用调用，解决了 Agent 与工具集成的复杂性。

### 架构优势
*   **配置热更新**：利用 xDS 协议（Envoy 的控制 API），Higress 可以在毫秒级内将配置变更推送到数据平面，且**不导致任何连接中断**。这对于 AI 流式响应场景至关重要，避免了传统网关 Reload 配置时的服务抖动。
*   **低资源消耗**：相比完整的 Istio，Higress 去除了不必要的 Sidecar 注入复杂性，资源占用极低，更适合单集群高流量吞吐。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI Gateway (AI 网关)**：
    *   **统一模型接入**：将 OpenAI、通义千问、Llama 等多种 LLM 接口标准化为统一格式。
    *   **Token 管理**：提供基于 Token 的计费、流控和多租户密钥管理。
    *   **Prompt 增强**：在网关层动态注入 System Prompt，无需修改后端应用代码即可调整模型行为。
2.  **MCP Server Hosting**：
    *   作为 AI Agent 的“工具箱”，允许 Agent 安全地通过网关调用内部微服务，网关负责处理协议转换和鉴权。
3.  **传统 API 网关**：
    *   K8s Ingress 支持、金丝雀发布、负载均衡、流量镜像。

### 解决的关键问题
*   **AI 供应商锁定**：通过统一适配层，企业可以随时切换底层 LLM 提供商，而无需修改客户端代码。
*   **流式传输的不可控性**：传统网关在处理 SSE 流时难以进行细粒度的拦截或修改（如敏感词过滤）。Higress 的 WASM 插件可以在流式传输过程中实时处理数据块。

### 与同类工具对比
*   **VS Nginx/Kong**：Kong 主要基于 Lua/Nginx，虽然生态成熟，但单进程模型在处理高并发长连接（如 AI 对话）时容易阻塞，且 Lua 的开发调试门槛较高。Higress 基于 Envoy 的多线程架构和 WASM 内存沙箱，在并发安全性和扩展语言支持上更优。
*   **VS Istio Ingress**：原生 Istio Ingress 配置极其复杂，学习曲线陡峭。Higress 提供了极其简化的 K8s CRD 和控制台，降低了运维成本。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM 运行时。为了解决 WASM 访问网络资源的限制（WASM 沙箱特性），Higress 实现了 **Host Calls** 映射，允许 WASM 插件通过宿主机的代理发起外部调用。
*   **配置分发**：Higress 实现了自定义的 Controller，监听 K8s API Server 资源变化，将其转换为 Envoy 的 xDS 配置（LDS/CDS/RDS），并推送给数据平面。

### 代码组织结构
项目主要分为两个大仓库：
1.  **higress (主仓库)**：Go 语言编写。包含控制平面逻辑、K8s Controller、以及用于生成 WASM 插件的 SDK (Go SDK)。
2.  **higress (WASM 插件仓库)**：通常包含具体的插件实现，这些代码被编译为 `.wasm` 文件，通过 ConfigMap 挂载或从 OCI 镜像拉取。

### 性能优化
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **异步处理**：所有插件逻辑（包括 AI 流式处理）均设计为异步 Filter Chain，不会阻塞主 I/O 线程。

---

## 4. 适用场景分析

### 适合使用的场景
1.  **企业级 AI 应用落地**：需要统一管理多个部门的 LLM API Key，并进行成本控制和审计。
2.  **微服务架构的 K8s 入口**：特别是已经使用 Istio 的企业，Higress 可以作为轻量级控制平面直接接管。
3.  **需要高度定制逻辑的网关**：例如需要特殊的签名算法、复杂的请求路由逻辑，且不希望修改网关内核代码，使用 WASM 开发插件是最佳选择。

### 不适合的场景
1.  **极简静态站点托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。
2.  **非 K8s 环境**：虽然 Higress 支持本地模式，但其核心优势在于与 K8s 的深度集成，脱离 K8s 使用会丧失大量动态能力。
3.  **极端低延迟要求**：相比纯 C++ 手写的 Nginx 模块，WASM 插件引入了少量的虚拟机执行开销（通常在毫秒级，但对极高 QPS 的简单路由可能有影响）。

### 集成方式
通常作为 K8s DaemonSet 或 Deployment 部署，通过 Service (LoadBalancer/NodePort) 暴露，并配置 IngressClass 将 K8s Ingress 资源指向 Higress。

---

## 5. 发展趋势展望

### 演进方向
*   **AI Native 深化**：未来将更深入地结合向量数据库、RAG (检索增强生成) 流程的网关层优化，例如在网关层直接进行 Prompt 缓存。
*   **WASM 生态标准化**：推动 Proxy-WASM 标准的落地，使插件在不同网关间通用。

### 社区与改进
*   目前社区活跃度较高，阿里内部支撑了双十一流量，稳定性有保障。
*   **改进空间**：WASM 插件的调试体验目前仍较为原始（主要依赖日志），可视化的调试工具是未来的刚需。

---

## 6. 学习建议

### 适合开发者
*   具备 **Golang** 基础（阅读控制平面代码）。
*   了解 **K8s** 基本概念。
*   对 **Envoy** 有基本认知。

### 学习路径
1.  **入门**：阅读官方 README，使用 Docker Compose 或 Helm Chart 部署一个 Demo。
2.  **进阶**：尝试编写一个简单的 WASM 插件（如添加 HTTP Header），使用 Higress 提供的 Go SDK 编译并部署。
3.  **深入**：研究 `pkg` 目录下的 xDS 转换逻辑，理解配置如何从 K8s CRD 变为 Envoy 配置。

### 实践建议
*   不要在生产环境直接编写复杂的 WASM 插件，先在本地测试内存泄漏和 CPU 占用。

---

## 7. 最佳实践建议

### 正确使用指南
*   **资源限制**：务必为 WASM 插件配置 CPU 和 Memory 限制，防止异常插件拖垮整个网关进程。
*   **插件版本管理**：使用 OCI 镜像仓库存储 WASM 插件，实现插件的版本化控制和灰度发布。

### 常见问题
*   **流式响应截断**：在 WASM 插件中处理流式数据时，必须正确处理 Buffer，否则可能导致数据积压或连接断开。确保使用 `Resume` 方法正确传递控制权。

### 性能优化
*   **全链路 Keep-Alive**：确保网关到后端 Upstream 的连接保持开启，减少握手开销，这对 AI 交互的低延迟至关重要。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在“**流量处理逻辑**”这一层做了极度的抽象。它将复杂性从“**编译进网关内核的 C++ 代码**”转移到了“**运行在沙箱中的 WASM 字节码**”以及“**K8s 的配置管理**”上。
*   **代价**：这种抽象牺牲了一部分极致的性能（WASM 解释执行开销），并要求运维人员必须理解 K8s 和分布式配置的概念。

### 价值取向
*   **可扩展性 > 极致性能**：它默认允许用户为了功能灵活性而接受微小的性能损耗。
*   **标准化 > 自由度**：它强制用户遵循 Envoy 和 K8s 的标准范式，限制了用户使用非标准 hack 手段的空间。

### 工程哲学
Higress 的范式是 **"Platform as a Gateway"（平台即网关）**。它不再仅仅是一个路由器，而是一个**流量计算平台**。它认为流量不仅仅是数据包，而是可以被编程、被 AI 模型理解和处理的信息流。
*   **误用风险**：最容易误用的是将复杂的业务逻辑（如复杂的数据库查询、繁重的计算任务）放入 WASM 插件中。虽然可行，但这会反噬网关的吞吐量，使其成为瓶颈。

### 可证伪的判断
1.  **性能判断**：在开启 10 个复杂 WASM 插件的情况下，Higress 的长连接 P99 延迟增加幅度应低于 5ms。如果超过，说明调度器或 WASM 运行时存在优化缺陷。
2.  **稳定性判断**：在频繁更新 WASM 插件配置（每秒 10 次变更）时，

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则，将请求转发到不同的后端服务
    解决问题：根据请求路径或头信息实现智能路由
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway()
    
    # 添加路由规则：将 /api/v1 请求转发到 service-a
    gateway.add_route(
        path="/api/v1/*",
        destination="service-a:8080",
        methods=["GET", "POST"],
        headers={"X-API-Version": "v1"}
    )
    
    # 添加路由规则：将 /api/v2 请求转发到 service-b
    gateway.add_route(
        path="/api/v2/*",
        destination="service-b:8080",
        methods=["GET"],
        headers={"X-API-Version": "v2"}
    )
    
    return gateway
```




```python
# 示例2：Higress 限流配置
def configure_rate_limiting():
    """
    配置 Higress 的限流策略，保护后端服务
    解决问题：防止流量突增导致服务过载
    """
    from higress import RateLimiter
    
    # 创建限流器实例
    limiter = RateLimiter()
    
    # 配置限流规则：每秒最多 100 个请求
    limiter.add_rule(
        path="/api/*",
        rate_limit=100,  # 请求/秒
        burst=20,        # 允许的突发请求数
        key_type="IP"    # 基于客户端 IP 限流
    )
    
    return limiter
```




```python
# 示例3：Higress 插件配置
def configure_plugins():
    """
    配置 Higress 的自定义插件
    解决问题：扩展网关功能，如添加认证、日志记录等
    """
    from higress import PluginManager
    
    # 创建插件管理器
    plugin_manager = PluginManager()
    
    # 添加 JWT 认证插件
    plugin_manager.add_plugin(
        name="jwt-auth",
        config={
            "secret": "your-secret-key",
            "algorithm": "HS256",
            "token_header": "Authorization"
        }
    )
    
    # 添加请求日志插件
    plugin_manager.add_plugin(
        name="request-logger",
        config={
            "log_format": "json",
            "include_headers": True,
            "output": "stdout"
        }
    )
    
    return plugin_manager
```


---
## 案例研究


### 1：某大型电商平台（阿里系内部）

 1：某大型电商平台（阿里系内部）

**背景**:  
该电商平台面临高并发流量挑战，特别是在大促期间（如双11），API网关需要处理每秒数十万级的请求。原有基于Nginx的定制网关在动态配置更新和扩展性方面存在瓶颈，且维护成本较高。

**问题**:  
- 动态路由配置更新需要重启服务，影响业务连续性  
- 流量治理功能（如限流、熔断）需要通过Lua脚本硬编码，开发效率低  
- 云原生集成能力不足，难以与Kubernetes服务网格无缝对接  

**解决方案**:  
采用Higress作为新一代API网关，基于Istio+Envoy架构实现：  
1. 通过Kubernetes CRD实现路由规则的毫秒级动态更新  
2. 内置流量治理插件（如sentinel限流、自定义鉴权）替代原有Lua脚本  
3. 与Istio服务网格集成，实现东西向与南北向流量统一管理  

**效果**:  
- 配置变更生效时间从分钟级降至秒级  
- 大促期间峰值QPS提升40%，P99延迟降低30%  
- 运维效率提升60%，网关开发成本降低50%  

---



### 2：某跨国物流企业

 2：某跨国物流企业

**背景**:  
该企业拥有遍布全球的微服务架构，原有Spring Cloud Gateway网关在跨区域流量调度和多云部署场景下存在性能瓶颈，且对第三方API集成支持不足。

**问题**:  
- 多区域部署时，网关集群间配置同步延迟导致路由不一致  
- 对接第三方物流API时，协议转换和认证逻辑复杂  
- 传统网关对WebAssembly插件支持有限，难以快速集成新功能  

**解决方案**:  
部署Higress网关集群并实施以下改造：  
1. 基于Nacos实现多集群配置实时同步  
2. 通过Wasm插件扩展功能，开发自定义协议转换插件  
3. 集成Higress的OpenAPI管理能力，统一第三方API接入规范  

**效果**:  
- 跨区域路由同步延迟从5秒降至100ms以内  
- 第三方API集成开发周期缩短70%  
- 网关资源利用率提升35%，年节省成本约200万元  

---



### 3：某金融科技初创公司

 3：某金融科技初创公司

**背景**:  
该公司提供SaaS化金融服务，需要为不同租户提供独立API网关实例，同时严格控制成本。原有Kong网关在多租户隔离和资源控制方面存在局限。

**问题**:  
- 租户间流量相互影响，QoS保障困难  
- 按实例计费模式导致资源浪费  
- 开源版本缺乏高级流量分析功能  

**解决方案**:  
采用Higress的云原生多租户架构：  
1. 基于Kubernetes Namespace实现租户级资源隔离  
2. 通过HPA实现网关实例弹性伸缩，优化资源分配  
3. 集成Prometheus+Grafana构建租户级流量监控看板  

**效果**:  
- 单租户成本降低60%  
- 租户间流量干扰事件降至0  
- 新租户网关开通时间从2天缩短到30分钟

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Rust 插件支持，低延迟 | 高性能，基于 Nginx 和 Lua，适合高并发 | 极高性能，基于 Nginx 和 Lua，优化了路由匹配 |
| 易用性 | 提供图形化控制台和 K8s Ingress 支持，配置简单 | 控制台功能丰富，但配置复杂度较高 | 提供图形化控制台，但学习曲线较陡 |
| 成本 | 开源免费，企业版需付费 | 开源版免费，企业版功能需付费 | 完全开源，无企业版 |
| 扩展性 | 支持 WASM 和 Rust 插件，扩展灵活 | 支持 Lua 和 PDK 插件，生态丰富 | 支持 Lua 和 Go 插件，生态活跃 |
| 社区支持 | 阿里背书，社区活跃但较新 | 社区成熟，插件生态丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API 管理 | 传统 API 网关、混合云 | 高并发、云原生 API 网关 |

### 优势分析

- **高性能与低延迟**：基于 Envoy 和 Rust 插件，性能优于传统 Lua 插件方案。
- **云原生集成**：原生支持 K8s Ingress 和服务网格，适合云原生架构。
- **扩展性强**：支持 WASM 和 Rust 插件，灵活性和安全性更高。
- **阿里生态支持**：与阿里云产品深度集成，适合已有阿里云基础设施的用户。

### 不足分析

- **社区相对较新**：相比 Kong 和 APISIX，社区成熟度和插件生态稍弱。
- **企业版成本**：高级功能需企业版付费，成本可能较高。
- **学习曲线**：对于非阿里云用户，可能需要额外学习其特有配置。
- **文档完善度**：部分功能文档不如 Kong 和 APISIX 详细。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展开发

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许使用 C/C++、Go、Rust 或 JavaScript 等多种语言编写网关插件。相比传统 Lua 插件，WASM 插件具有更好的隔离性、更高的性能以及更丰富的生态支持，是实现复杂业务逻辑（如请求头修改、响应体转换、流量染色）的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 官方提供的 `wasm-assembler` 工具或 SDK 框架进行插件开发。
3. 在本地或 CI/CD 流水线中将代码编译为 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传并部署插件。
5. 在网关路由配置中关联该插件，并配置所需的参数。

**注意事项**: 
- WASM 插件运行在沙箱中，需注意内存和 CPU 的使用限制，避免阻塞主线程。
- 生产环境部署前，务必对 WASM 插件进行充分的性能压测。

---

### 实践 2：服务发现与 Nacos 注册中心集成

**说明**: Higress 原生支持 Nacos 作为服务注册中心，能够实现从注册中心动态获取服务后端地址列表。这使得网关可以自动感知服务的上下线，无需手动修改网关配置，特别适用于微服务架构或 Kubernetes 之外的服务治理场景。

**实施步骤**:
1. 在 Higress 全局配置或源服务配置中，添加 Nacos 注册中心地址。
2. 配置 Nacos 的命名空间 和 AccessKey/SecretKey（如果开启了鉴权）。
3. 在创建 Ingress 或路由规则时，`Service` 字段填写 Nacos 中注册的服务名称。
4. Higress 将自动建立与 Nacos 的长连接，并同步服务节点列表。

**注意事项**: 
- 确保 Higress 所在网络能够访问 Nacos 服务端端口（默认 8848）。
- 如果使用 Nacos 2.x，需注意 gRPC 端口的连通性。

---

### 实践 3：全链路安全防护与 WAF 规则配置

**说明**: 利用 Higress 内置的安全插件或集成第三方 WAF（如 ModSecurity），构建针对 OWASP Top 10 的防护体系。Higress 支持基于 IP、Header、Cookie 等维度的精细访问控制，可以有效防御 SQL 注入、XSS 跨站脚本等常见 Web 攻击。

**实施步骤**:
1. 在插件市场启用 "WAF 插件" 或 "Key Rate Limit" 插件。
2. 配置黑名单/白名单规则，限制恶意 IP 访问。
3. 开启请求体大小限制，防止缓冲区溢出攻击。
4. 针对特定路由配置严格的 CORS（跨域资源共享）策略。
5. 启用 JWT 认证插件，保护后端 API 接口。

**注意事项**: 
- WAF 规则过于严格可能会误拦截正常请求，建议先开启"监控模式"观察一段时间。
- 定期更新 WAF 规则库以应对新出现的漏洞威胁。

---

### 实践 4：精细化流量管理与金丝雀发布

**说明**: Higress 提供了强大的流量路由能力，支持基于 HTTP Header、Query 参数、Cookie 甚至权重比例的流量分流。这是实现蓝绿部署、金丝雀发布和 A/B 测试的最佳实践，能够降低新版本上线的风险。

**实施步骤**:
1. 准备两套后端服务环境（如 v1 和 v2）。
2. 在 Higress 中创建两个服务引用，分别指向 v1 和 v2 的实例。
3. 配置路由规则，设置默认流量指向 v1。
4. 添加一条带匹配条件（如 `x-version: v2` 或 `cookie: beta_user`）的路由规则指向 v2。
5. 若进行灰度发布，可配置基于权重的分流，逐步将流量从 v1 切换到 v2。

**注意事项**: 
- 确保不同版本的服务在 Higress 中配置了正确的健康检查，避免将流量转发至不可用的实例。
- 灰度发布过程中，应密切监控错误率和延迟指标。

---

### 实践 5：高可用部署与热配置更新

**说明**: 在生产环境中，网关组件的高可用至关重要。Higress 采用控制面与数据面分离的架构，支持配置的热更新，可以在不中断业务的情况下动态调整路由规则和插件配置。

**实施步骤**:
1. **部署层面**：在 Kubernetes 中使用 HPA (Horizontal Pod Autoscaler) 基于 CPU/内存使用率自动扩缩容 Higress Gateway Pod，建议副本数至少为 2。
2. **配置层面**：利用 Ingress 或 Gateway API 定义路由，这些资源

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，网络传输层的延迟直接影响整体吞吐。HTTP/3 基于 UDP 协议，解决了 TCP 的队头阻塞问题，能有效减少弱网环境下的丢包重传延迟，并提升连接迁移速度。

**实施方法**:
1. 在 Higress 的网关配置中，检查监听器协议设置，启用 QUIC 或 HTTP/3 监听端口。
2. 确保负载均衡器或上游反向代理（如 ALB/NLB）正确转发 UDP 流量。
3. 调整 `quic` 配置参数，如连接超时时间和最大并发流限制。

**预期效果**: 在高丢包率网络环境下，请求延迟降低 20%-40%，连接建立成功率显著提升。

---

### 优化 2：启用 Wasm 插件与请求体缓存优化

**说明**: Higress 的一大特性是支持 Wasm 插件。如果插件处理逻辑（如鉴权或 Header 修改）需要读取请求体，默认的流式处理会被阻断。通过合理配置请求体缓存或优化 Wasm 内存分配，可减少 CPU 拷贝开销。

**实施方法**:
1. 在编写 Wasm 插件时，尽量仅在必要时才读取 Body。
2. 针对必须读取 Body 的场景，在路由配置中明确开启 `requestBody` 缓存限制，避免无限缓存导致内存溢出。
3. 使用 AOT 编译或 TinyGo 优化 Wasm 文件体积和执行效率。

**预期效果**: 降低单次请求 CPU 消耗约 10%-15%，提升 Wasm 插件处理吞吐量。

---

### 优化 3：配置服务发现与连接池调优

**说明**: 默认的连接池配置可能无法应对突发流量。如果后端服务响应较慢但连接数不足，会导致请求排队。同时，长连接复用率不足会导致频繁握手，增加延迟。

**实施方法**:
1. 修改全局或特定服务的 `Upstream` 配置，调大 `max_connections`（连接池大小）。
2. 启用 HTTP/1.1 的 Keep-Alive 或 HTTP/2 连接复用。
3. 结合 Nacos 或 Kubernetes Service 发现，设置合理的健康检查间隔（如 2秒），避免将流量发送至不健康的实例。

**预期效果**: 在高并发场景下，P99 延迟降低 30%，后端连接建立开销减少 50% 以上。

---

### 优化 4：全链路超时与重试策略精细化

**说明**: 不合理的超时和重试策略会引发“雪崩效应”。过长的超时会导致线程积压，盲目的重试会放大故障影响。

**实施方法**:
1. 根据业务 SLA 设置严格的 `timeout`（如连接超时 3s，读取超时 5s）。
2. 配置指数退避的重试策略，限制最大重试次数（建议 2-3 次）。
3. 开启“熔断”功能，当后端服务错误率超过阈值时，自动快速失败。

**预期效果**: 故障场景下，系统可用性提升，无效资源消耗减少 90% 以上。

---

### 优化 5：日志级别与采样率控制

**说明**: 在高流量下，打印详细的 Access Log 或 Debug 日志会严重消耗磁盘 I/O 和 CPU，成为性能瓶颈。

**实施方法**:
1. 将核心网关日志级别调整为 `info` 或 `warn`，避免 `debug`。
2. 配置日志采样（如仅记录 10% 的正常流量请求，或仅记录状态码非 200 的请求）。
3. 使用异步日志发送插件（如 Kafka/SLS 采集）时，增加批量发送的大小和间隔。

**预期效果**: I/O 写入吞吐量降低 60%-80%，CPU 使用率显著下降。

---
## 学习要点

- 基于您提供的信息（alibaba/higress，来源：GitHub 趋势），以下是关于 Higress 的关键要点总结：
- Higress 是阿里巴巴开源的一款基于 Istio 的云原生 API 网关，旨在解决云原生时代流量治理与入口管理的复杂性问题。
- 它深度集成了 Envoy 作为高性能数据面，并针对 K8s 环境进行了优化，提供比传统 Ingress Controller 更强大的流量管理能力。
- 该项目支持将 K8s Ingress 与 Gateway API 资源转换为统一的配置，实现了从微服务架构到 Serverless 架构的流量管理标准化。
- Higress 提供了强大的 WAF（Web 应用防火墙）插件生态，支持对 HTTP、HTTPS、gRPC 以及 Dubbo 等协议进行安全防护与流量管控。
- 它兼容 Nginx 的 Ingress 注解，并支持将 Nginx 配置直接迁移，极大地降低了用户从传统网关迁移至云原生网关的门槛。
- 通过将服务网格（Istio）的 Sidecar 模式转化为网关模式，Higress 能够以更低的资源消耗提供高可用的南北向流量处理能力。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及 Higress 在微服务架构中的定位（流量入口、南北向流量与东西向流量）。
- **Higress 架构原理**: 学习 Higress 的核心组件，包括 Istio (控制面)、Envoy (数据面) 的集成方式，以及其自研的配置热更新机制。
- **基本安装与部署**: 掌握如何在本地 Docker 环境或 Kubernetes 集群中安装 Higress。
- **控制台操作**: 熟悉 Higress 的原生控制台（Console）界面，进行基础的域名路由配置。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与快速开始章节)
- Higress GitHub 仓库 (README 与 Wiki)
- Docker 与 Kubernetes 基础教程

**学习建议**: 
不要急于进行复杂配置，先跑通一个最简单的 "域名 -> 路由 -> 服务" 的流量转发 Demo。理解 Higress 是如何基于 Ingress 或 Gateway API 资源进行工作的。

---

### 阶段 2：流量治理与路由进阶

**学习内容**:
- **高级路由策略**: 学习基于 Header、Query、Cookie 等条件的复杂路由匹配，以及重定向和重写路径的配置。
- **负载均衡与容错**: 掌握轮询、随机、一致性哈希等负载均衡算法，以及超时、重试和熔断机制的配置。
- **服务发现集成**: 学习如何将 Higress 与 Nacos、Consul、Kubernetes Service 以及固定地址（DNS/IP）的服务进行对接。
- **全链路安全**: 配置 HTTPS 证书管理，以及 Basic Auth、JWT 认证等基础安全插件。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理板块
- Envoy Filter 官方文档 (用于理解底层过滤机制)
- Nacos 注册中心基础教程

**学习建议**: 
尝试搭建一个包含两个服务（如服务 A 和服务 B）的微服务场景，配置 Higress 实现按权重路由（金丝雀发布）和通过服务名进行服务发现。这是实际工作中最常见的场景。

---

### 阶段 3：插件生态与扩展能力

**学习内容**:
- **内置插件使用**: 深入使用 Higress 提供的丰富插件，如限流、跨域 (CORS)、请求/响应头修改、API Key 认证等。
- **Wasm 插件开发**: 学习 Higress 的核心特色——基于 Wasm (WebAssembly) 的插件扩展机制。了解如何使用 Go 或 C++ 开发 Wasm 插件。
- **自定义插件处理**: 掌握如何在控制台上传、启用和配置自定义 Wasm 插件，实现业务逻辑的动态注入。
- **插件市场**: 了解如何对接 Lua 脚本或使用 Higress 插件市场中的现成解决方案。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场与自定义开发
- Higress GitHub - Wasm 插件示例代码
- WebAssembly (Wasm) 基础概念

**学习建议**: 
不要只做配置者，尝试成为一名开发者。阅读官方提供的 Wasm 插件 Demo，尝试编写一个简单的插件（例如：在响应头中添加特定的自定义 Header），并在本地环境编译、加载并测试。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- **可观测性**: 集成 Prometheus 监控指标，配置访问日志采集（对接 SLS、ELK 或 Kafka），以及分布式链路追踪。
- **高可用部署**: 学习 Higress 的高可用架构设计，包括多副本部署、健康检查机制和优雅升级。
- **性能调优**: 理解如何调整连接池、缓冲区大小等参数以应对高并发流量。
- **多租户与多环境管理**: 学习如何在不同环境（测试、预发、生产）管理网关配置，以及基于命名空间的隔离策略。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 运维指南
- Prometheus 与 Grafana 监控搭建教程
- Envoy 性能调优最佳实践

**学习建议**: 
模拟生产环境进行压测（使用 JMeter 或 Hey），观察 Higress 的 CPU/内存表现，并根据监控指标调整配置。重点关注日志的规范化和监控告警的配置。

---

### 阶段 5：源码剖析与架构内功

**学习内容**:
- **源码结构分析**: 深入阅读 Higress 的源码，理解 Router、Filter、Config Controller 等核心模块的实现逻辑。
- **

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在电商、金融等高并发场景下的网关实践经验沉淀而成的。Higress 的前身是阿里云的云原生网关，它于 2022 年开源并捐赠给了 CNCF（云原生计算基金会）。

Higress 旨在解决云原生时代流量治理的痛点，它深度集成了 Envoy 和 Istio，提供了从流量入口（南北向流量）到微服务间通信（东西向流量）的统一治理能力。作为阿里巴巴开源的重要项目之一，它承载了阿里“双十一”等场景下经过验证的稳定性与高性能技术。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”架构和与 Istio 的深度集成，具体体现在以下几个方面：

1.  **标准兼容性**：Higress 兼容 Kubernetes Ingress 标准，同时也支持 Nginx Ingress Annotation。这意味着用户可以从 Nginx 或其他 Ingress Controller 较为平滑地迁移到 Higress，无需大量修改配置。
2.  **服务网格集成**：与 Kong 或 APISIX 不同，Higress 天然支持作为 Istio 的入口网关。它可以与 Istio 控制平面配合，实现从 Ingress 到 Sidecar 的全链路流量管理，统一了南北向和东西向流量的治理配置。
3.  **热更新与插件生态**：基于 Envoy 的高性能架构，Higress 支持配置和插件的热更新，不需要重启网关进程即可生效。它提供了 Wasm 插件市场，支持 Go、C++、AssemblyScript 等多种语言编写插件，扩展能力极强。
4.  **安全防护**：内置了开源版 WAF（Web Application Firewall）功能，提供基础的防 SQL 注入、XSS 等安全能力。

---



### 3: Higress 是否兼容 Nginx 的配置？迁移难度大吗？

3: Higress 是否兼容 Nginx 的配置？迁移难度大吗？

**A**: Higress 对 Nginx 用户非常友好，迁移难度相对较低。

1.  **Annotation 兼容**：Higress 实现了 Kubernetes Nginx Ingress Controller 的核心 Annotation 子集。如果你在 Kubernetes 上使用 Nginx Ingress，通常只需修改 Ingress 资源的 `ingressClassName` 字段指向 Higress，大部分基于 Annotation 的配置（如重写、转发、HTTPS 配置）可以直接复用。
2.  **配置转换**：对于非 Kubernetes 场景或复杂的 Nginx 配置，Higress 社区提供了配置转换工具，可以帮助将传统的 Nginx.conf 转换为 Higress 的路由配置。
3.  **学习曲线**：如果你习惯了 Nginx 的配置文件方式，可能需要适应 Higress 基于 Kubernetes CRD（自定义资源）或控制台（Console）的可视化配置方式，但这符合现代云原生运维的标准操作流程。

---



### 4: Higress 支持哪些协议？是否支持 gRPC 或 Dubbo？

4: Higress 支持哪些协议？是否支持 gRPC 或 Dubbo？

**A**: Higress 是为现代微服务架构设计的，因此对主流的 RPC 和微服务协议有极好的支持：

1.  **HTTP/HTTPS**：完全支持 HTTP 1.1 和 HTTP 2（包括 gRPC Web）。
2.  **gRPC**：原生支持 gRPC 协议的代理与路由，支持基于 gRPC 的流量负载均衡和服务发现。
3.  **Dubbo**：这是 Higress 区分于很多国外开源网关的一大特色。由于阿里巴巴的背景，Higress 对 Apache Dubbo（包括 Dubbo 2 和 Dubbo 3 协议）提供了原生支持。它可以将 HTTP 请求直接转换为 Dubbo 协议调用后端服务，实现了网关对多协议后端的统一接入。
4.  **WebSocket**：支持 WebSocket 协议的代理，适用于实时通讯场景。

---



### 5: Higress 的性能如何？能否支撑高并发场景？

5: Higress 的性能如何？能否支撑高并发场景？

**A**: Higress 的性能表现非常优异，完全能够支撑企业级的高并发场景。

1.  **底层引擎**：Higress 的数据面基于 Envoy 构建。Envoy 是业界公认的高性能 L7 代理，使用 C++ 编写，具有极低的延迟和极高的吞吐量。
2.  **阿里验证**：作为阿里云云原生网关的开源版本，其内核经过了阿里巴巴内部“双十一”等海量流量场景的严苛考验。在开源基准测试中，Higress 的吞吐量（QPS）和延迟表现通常优于基于 OpenResty 或 Go 语言编写的部分传统网关。
3.  **弹性伸缩**：由于它是云原生的，可以结合 Kubernetes 的 HPA（水平自动扩缩容）进行秒级弹性扩容，以应对突发流量。

---



### 6: 如何扩展 Higress 的功能？是否

6: 如何扩展 Higress 的功能？是否

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础路由转发

### 假设你有一个运行在 `http://backend:8080` 的后端服务，请编写一个 Higress 的 Ingress 或 Gateway API 配置（YAML 格式），实现将所有发往网关 `/example` 路径的 HTTP 请求，转发至该后端服务的根路径 `/`。

### 提示**: 关注 Higress 的 Ingress 资源定义中的 `spec.rules.host` 和 `spec.rules.http.paths` 配置，特别是 `pathType` 的选择（如 `Prefix` 或 `Exact`）以及 `backend.service` 的端口名称。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其作为云原生 API 网关的技术特性，以下是针对实际生产环境的 7 条实践建议：

### 1. 利用 Wasm 插件实现 LLM 提示词管理与安全审计
**场景**：在大模型应用中，直接将 Prompt 写在客户端代码中不仅难以维护，还存在泄露 Prompt 工程逻辑的风险。
**建议**：
*   **最佳实践**：编写 Wasm 插件（使用 Go 或 Rust）在网关层注入系统提示词或上下文。这样可以在不修改后端服务的情况下，动态调整发给 LLM 提供商的 Prompt 模板。
*   **安全审计**：利用 Wasm 插件在请求发送前拦截并扫描用户输入，防止恶意 Prompt 攻击（如 Prompt 注入），在网关层直接拦截违规请求，避免后端消耗昂贵的 Token 配额。

### 2. 配置基于 Token 计量的智能限流
**场景**：传统 API 网关通常基于 QPS（每秒请求数）或并发数限流，但 AI 服务的成本主要消耗在 Token 数量上。一个包含大量上下文的请求可能只占用 1 个 QPS，但消耗巨大。
**建议**：
*   **具体操作**：不要仅依赖默认的 QPS 限流。建议结合 Higress 的自定义插件功能，解析请求体预估 Token 消耗（基于字符数估算或调用计数器），并结合 Redis 实现基于“用户+Token 总量”的限流策略。
*   **价值**：防止个别用户通过超长上下文请求耗尽预算，保障服务的成本可控。

### 3. 实施多模型提供商的故障转移与负载均衡
**场景**：调用 OpenAI、Azure OpenAI 或通义千问等 API 时，常面临网络抖动或服务不可用的情况。
**建议**：
*   **最佳实践**：在 Higress 中配置多个服务来源（Service），利用其服务路由能力，设置主备模型服务商。例如，默认请求转发至 OpenAI，当检测到 HTTP 429/5xx 错误或响应超时时，自动切换至备用的 LLM 提供商。
*   **具体操作**：配置自动重试机制，但需注意幂等性，确保重试不会导致客户端重复扣费或收到重复响应。

### 4. 针对流式响应（SSE）的超时与缓存策略优化
**场景**：AI 对话通常采用 Server-Sent Events (SSE) 流式返回，这与传统 HTTP 短连接处理逻辑不同。
**建议**：
*   **常见陷阱**：错误配置网关的超时时间导致流式传输中断。务必将网关的请求超时时间设置得足够长，或者针对流式接口单独配置超时策略。
*   **缓存策略**：对于完全相同的 Prompt（如知识库问答），可利用 Higress 的缓存插件缓存 LLM 的最终响应。但需注意，流式响应的缓存实现比普通请求复杂，建议仅对非流式（Stream=false）的读请求开启缓存，或使用支持全量回源缓存的高级插件。

### 5. 构建语义路由以实现模型分发
**场景**：并非所有查询都需要昂贵的大模型（如 GPT-4），简单查询（如“今天天气”）可由廉价或小模型（如 Llama 3-8B 或 Hugging Face 模型）处理。
**建议**：
*   **具体操作**：部署一个轻量级的分类模型或基于关键词匹配的 Wasm 插件。在请求路由阶段，根据用户输入的语义复杂度，将请求路由到不同的后端服务（简单路由 -> 小模型/传统规则引擎；复杂路由 -> 大模型）。
*   **价值**：在保证用户体验的前提下，大幅降低 API 调用成本和延迟。

### 6. 敏感信息脱敏与数据过滤
**场景**：企业内部数据通过 AI 网关传输时，可能无意间泄露 IP、PII（个人身份信息）

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*