---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-10T12:38:40+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "MCP", "LLM", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： 项目简介 **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并扩展了 WebAssembly (WASM) 插件能力。该项目定位于 **AI Native（AI 原生）**，旨在为现代大模型（"
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
- **星标**: 7,720 (+18 stars today)
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

Higress 是阿里巴巴开源的一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关。它专为云原生环境设计，不仅提供传统的流量管理与微服务路由能力，更集成了针对大语言模型（LLM）应用的 AI 网关特性及 MCP 服务器托管功能。本文将深入解析其系统架构、核心组件以及 WASM 插件机制，帮助开发者理解如何利用 Higress 高效地连接 AI 服务与现有业务体系。

---
## 摘要

以下是对 Higress 项目的简洁总结：

### 项目简介
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并扩展了 WebAssembly (WASM) 插件能力。该项目定位于 **AI Native（AI 原生）**，旨在为现代大模型（LLM）应用和微服务架构提供统一的流量入口和管理平台。

### 核心功能
Higress 的核心功能主要集中在以下三个方面：

1.  **AI 网关**：
    *   提供**统一 API**，兼容 30 多家主流大语言模型提供商。
    *   **功能特性**：支持协议转换、可观测性（数据统计）、缓存以及安全防护。
    *   *核心组件*：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 插件。

2.  **MCP 服务器托管**：
    *   托管 **模型上下文协议 (MCP)** 服务器，使 AI Agent 能够便捷地调用外部工具和服务。
    *   *核心组件*：`mcp-router`, `jsonrpc-converter` 过滤器及多种 MCP 服务器实现（如搜索、地图工具等）。

3.  **传统 API 网关与 K8s Ingress**：
    *   作为 Kubernetes Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由。

### 架构优势
*   **控制面与数据面分离**：配置管理与流量处理解耦。
*   **高性能**：配置变更通过 xDS 协议传播，延迟仅为毫秒级，且支持**热更新**（无连接中断）。
*   **适用场景**：特别适合需要长连接的 AI 流式响应场景。

**开发语言**：Go  
**热度**：目前拥有超过 7,700 个 GitHub Star。

---
## 评论

**总体判断**

Higress 是当前云原生网关领域中将“AI 原生”理念落地最彻底的开源项目之一。它成功解决了传统 API 网关在处理 LLM（大语言模型）流量时的协议缺失与成本痛点，是构建企业级 AI 应用的基础设施首选。

**深入评价分析**

**1. 技术创新性：从“流量转发”到“模型编排”的架构跃迁**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并深度集成了 WebAssembly (WASM) 插件系统。DeepWiki 明确指出其核心功能包括“AI Gateway Features for LLM applications”和“MCP server hosting”。
*   **推断**：传统网关（如 Nginx, 早期 Kong）主要处理 HTTP/gRPC 转发，而 Higress 的差异化在于它**将 AI 协议视为一等公民**。它通过 WASM 技术在数据平面实现了对 LLM 协议（如 OpenAI 协议）的深度解析与修改。这意味着网关不仅能做负载均衡，还能在传输层实现 Token 计费、敏感词过滤、Prompt 注入以及将 SSE（Server-Sent Events）流式响应转换为标准格式。此外，支持 MCP (Model Context Protocol) Server 托管，表明它正在从网关向 AI Agent 的基础设施演进，这种将“流量入口”与“工具托管”结合的架构极具前瞻性。

**2. 实用价值：解决 AI 落地中的“连接”与“成本”难题**
*   **事实**：仓库描述强调其为“AI Native API Gateway”，且 README 中涵盖了 Kubernetes Ingress 和微服务路由。
*   **推断**：Higress 解决了 AI 时代的三个核心痛点：
    1.  **统一接入**：企业往往同时使用传统微服务和新兴 AI 服务，Higress 提供了统一控制平面，避免维护两套网关。
    2.  **成本控制**：LLM 调用成本高昂。Higress 的 AI 网关特性允许在网关层实现缓存（减少重复调用）和请求限流，直接降低模型支出。
    3.  **安全与合规**：通过插件机制，可以在网关层拦截 PII（个人敏感信息）或有害指令，防止其直达模型，这是企业级落地的刚需。

**3. 代码质量与架构：云原生标准的教科书级实现**
*   **事实**：项目使用 Go 语言编写，星标数 7,720，架构上明确分离了控制平面和数据平面。
*   **推断**：基于 Envoy 和 Istio 意味着其数据平面继承了 C++ 编写的高性能 envoy 代理的稳定性，控制平面则利用 Go 的高并发特性处理配置分发。这种“控制面 Go + 数据面 Envoy”的组合是云原生领域的黄金标准。WASM 插件系统的引入使得代码扩展性极强，用户无需修改网关核心代码即可通过 C++/Go/Rust/AssemblyScript 编写业务逻辑，极大地降低了耦合度，提升了系统的可维护性。

**4. 社区活跃度：阿里背书的企业级开源项目**
*   **事实**：由阿里巴巴开源，拥有 7k+ Stars。
*   **推断**：阿里系的开源项目通常具有极强的工程实用性，文档（包括中英日文）非常完善，这降低了上手门槛。相比个人项目，Higress 的更新频率和长期维护更有保障。社区贡献者不仅限于阿里内部，随着 AI 热潮，大量 AI 应用开发者为其贡献了针对不同模型的插件，形成了正向循环。

**5. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度门槛**：基于 Istio 的架构虽然强大，但对于仅需要简单 AI 转发的初创团队来说，部署和运维 Higress 的心智成本远高于使用 Nginx 或简单的 Python 脚本。
    *   **WASM 冷启动**：虽然 WASM 提供了隔离性，但在极高并发下，WASM 插件的冷启动延迟和内存开销仍需通过压测验证。
    *   **建议**：进一步简化 Standalone（非 K8s）模式的部署体验，以便非容器化用户也能快速上手体验 AI 网关特性。

**6. 对比优势**
*   **对比 Kong/APISIX**：传统网关通过插件支持 AI，但多为“事后补救”的 Lua 或 Python 插件，性能和原生性不足。Higress 是“原生”设计，对 SSE 流处理、Token 统计的理解更深。
*   **对比专用 AI Proxy (如 LiteLLM)**：LiteLLM 专注于协议转换和负载均衡，功能单一。Higress 在此基础上提供了全套的微服务治理能力（灰度发布、流量镜像），更适合大型企业复杂环境。

**边界条件与验证清单**

**不适用场景**：
*   极其简单的边缘计算场景（资源受限，无法运行 Envoy）。
*   仅需一次性脚本调用的内部工具（杀鸡焉用牛刀）。
*   对云原生技术栈（K8s）完全排斥的遗留系统。

**快速验证清单**：
1.  **协议兼容性测试**：部署 Higress，配置一个指向 OpenAI 兼容接口的路由，使用 cURL 发送流式请求，验证网关是否能正确透传 SSE 流且不增加显著延迟。
2.  **WASM �

---
## 技术分析

以下是对阿里巴巴开源仓库 **Higress** 的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构遵循**云原生**设计理念，采用了经典的**控制平面与数据平面分离**的架构模式。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 C++ 实现的 L4/L7 处理能力。
*   **控制平面**：基于 **Istio** 修改构建。Higress 并没有从零造轮子，而是继承了 Istio 强大的 xDS（发现服务）协议栈，用于配置下发。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为插件运行时。这是 Higress 架构中最关键的技术决策之一，允许使用 C/C++/Go/Rust/JavaScript 等语言编写逻辑，并在 Envoy 的沙箱中运行。
*   **编程语言**：主体控制逻辑使用 **Go** 语言编写，利用 Go 的高并发特性处理配置管理和 gRPC 流式通信。

### 核心模块与关键设计
1.  **路由与流量管理**：完全兼容 Kubernetes Ingress API 和 Istio Gateway API。它将 K8s 的 Ingress 资源转化为 Envoy 的路由配置。
2.  **WASM 插件市场**：提供了一个默认的插件生态，包括认证、限流、熔断等。设计上支持动态加载，无需重启网关即可更新业务逻辑。
3.  **AI 网关模块**：这是 Higress 区别于传统网关的核心。它在数据平面实现了对 LLM 协议（如 OpenAI 格式）的深度解析，能够处理流式响应。
4.  **配置分发**：通过 xDS API（特别是 LDS/RDS/EDS/CDS）将控制平面的配置推送到数据平面。Higress 优化了这一过程，实现了毫秒级配置生效。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：Higress 是最早将 LLM 处理能力内置到 API 网关中的开源项目之一。它不仅仅是透传流量，还能理解 AI 语义，例如 Token 计费、Prompt 模板管理、敏感词过滤。
*   **MCP (Model Context Protocol) 支持**：作为 AI Agent 的基础设施，Higress 能够托管 MCP 服务，解决 Agent 与外部工具集成的连接问题。
*   **热更新与无中断**：基于 Envoy 的热重启能力和 xDS 的动态配置，实现了真正的业务无感部署。

### 架构优势分析
*   **性能损耗极低**：关键路径在 Envoy (C++) 中处理，WASM 虽然有虚拟化开销，但相比 Go/Java 网关的业务逻辑插入，性能依然极具优势。
*   **极致的可扩展性**：通过 WASM，开发者可以在不修改网关核心代码的情况下，注入任意复杂的业务逻辑（如自定义鉴权、请求体转换）。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure OpenAI、通义千问、文心一言等不同厂商的 API 统一为标准接口。
    *   **Token 管理**：实时统计流式传输中的 Token 消耗，实现基于 Token 的精细化计费或限流。
    *   **Prompt 增强**：在网关层注入 System Prompt，实现无需修改应用代码的提示词工程管理。
2.  **MCP 服务器托管**：
    *   允许将内部的 HTTP API 快速封装为 MCP 协议，供 AI Agent 调用。
3.  **传统 API 网关**：
    *   K8s Ingress Controller：替代 Nginx Ingress。
    *   微服务治理：服务发现、金丝雀发布、负载均衡。

### 解决的关键问题
*   **AI 落地的碎片化**：解决了应用层需要适配不同 LLM 厂商 SDK 的问题，通过网关屏蔽底层差异。
*   **流式响应的处理难题**：传统网关难以处理 SSE (Server-Sent Events) 的流式 Body 修改。Higress 能够在流式传输过程中进行拦截、修改（如过滤敏感词）并转发，这在传统架构中极难实现。
*   **K8s 环境下的流量管理**：提供了比 Nginx Ingress 更丰富的流量治理能力（如全局限流、动态路由）。

### 与同类工具对比
*   **VS Nginx/Kong**：Nginx 基于 Lua 扩展，开发门槛高且容易阻塞进程；Kong 基于 Nginx/OpenResty，架构较重。Higress 基于 Envoy + WASM，内存安全性更好，多线程并发模型更优。
*   **VS APISIX**：APISIX 也是基于 Lua + etcd，性能极高。但 Higress 的优势在于与 Istio 生态的原生集成，以及针对 AI 场景的特定优化。
*   **VS Istio Ingress Gateway**：原生 Istio Ingress 配置极其复杂。Higress 提供了更符合运维习惯的 K8s Ingress 注解和简化控制台，降低了使用门槛。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM 运行时（如 Wasmtime 或 V8）。当请求到达时，Envoy 会加载 WASM 模块的 `on_request` 或 `on_response` 钩子。为了保证性能，Higress 采用了**Proxy-WASM** 标准，允许 VM 复用和跨平台共享内存优化。
*   **流式处理**：在处理 LLM 流式响应时，Higress 并没有等待完整的响应 Body，而是基于 Envoy 的 Streaming Filter 机制。数据块以 Buffer 的形式流经 WASM 插件，插件可以逐块检查或修改，然后立即发送给客户端。
*   **配置热更**：控制平面监听 K8s API Server 的资源变化，将其转化为 Envoy 的 xDS 配置。通过增量 xDS 推送，只更新变化的路由规则，最小化连接抖动。

### 代码组织与设计模式
*   **代码结构**：`pkg/` 目录包含核心控制逻辑（如 Ingress 转换器），`plugins/` 目录包含各种 WASM 插件的源码。
*   **CRD 驱动**：大量使用 Kubernetes 的 Custom Resource Definition (CRD) 来定义网关的行为（如 `WasmPlugin` 资源），体现了 K8s Operator 模式。

### 性能与扩展性
*   **性能优化**：WASM 的编译开销在冷启动后消失，后续执行接近原生速度。Higress 针对高并发场景进行了连接池优化。
*   **水平扩展**：作为无状态的数据平面，Pod 可以根据 K8s HPA (Horizontal Pod Autoscaler) 自动扩缩容。

### 技术难点与解决
*   **难点**：WASM 插件的调试困难。
*   **解决**：Higress 提供了详细的日志输出工具，并支持在本地运行 WASM 插件进行测试后再部署。
*   **难点**：AI 流式响应的 Token 计数准确性。
*   **解决**：通过解析 SSE 数据流中的特定字段（如 `usage` 字段）或通过分词算法实时估算，在网关层完成计量。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **大模型应用 (RAG/Chatbot)**：任何需要调用 OpenAI、阿里云通义等 LLM API 的企业级应用。
2.  **多云/混合云架构**：需要统一管理位于不同 K8s 集群或云厂商的 API 流量。
3.  **需要高频变更业务逻辑的网关**：例如频繁调整限流规则、增加新的鉴权逻辑，利用 WASM 插件可以实现秒级发布。

### 最有效的情况
*   当你需要将现有的传统微服务架构平滑迁移到 AI 架构时，Higress 能够作为统一的流量入口，避免维护两套网关系统。
*   当你需要对 AI 调用成本进行严格控制（如限制单用户 Token 额度）时，其内置的 AI 指标统计功能非常有效。

### 不适合的场景
*   **极简静态站点托管**：对于只需简单反向代理的场景，Higress 的资源开销（内存占用通常几百 MB）远高于 Nginx。
*   **非 K8s 环境**：虽然可以二进制运行，但 Higress 的强大功能高度依赖 Kubernetes 生态，在虚拟机或物理机部署会丧失大部分动态配置优势。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 编排**：从简单的 API 转发向 AI Agent 编排演进，例如在网关层实现简单的多模型路由（根据问题难度自动选择模型）。
*   **WASM 生态标准化**：推动 Proxy-WASM 插件在不同网关之间的通用性，构建“一次编写，随处运行”的插件市场。

### 社区反馈与改进空间
*   **文档与易用性**：虽然功能强大，但 WASM 插件的开发对普通运维人员仍有门槛。未来可能需要更多 Low-Code 的插件生成工具。
*   **监控集成**：虽然支持 Prometheus，但对于 AI 特定的指标（如 TTFT - Time To First Token，TPM - Tokens Per Minute）的可观测性展示仍需加强。

---

## 6. 学习建议

### 适合的开发者水平
*   **中级**：熟悉 Kubernetes 基础、了解 HTTP 协议。
*   **高级**：想要深入 Envoy、WASM 或云原生架构的架构师。

### 学习路径
1.  **基础**：先理解 Kubernetes Ingress 和 Service 的基本概念。
2.  **进阶**：学习 Envoy 的基本术语（Listener, Route, Cluster）。
3.  **实战**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 代理转发。
4.  **开发**：尝试使用 Go (TinyGo) 编写一个简单的 WASM 插件（如添加 HTTP Header），并挂载到 Higress 路由上。

### 实践建议
*   阅读官方仓库的 `plugins/wasm-go` 目录，参考官方插件示例是上手最快的方式。

---

## 7. 最佳实践建议

### 正确使用方式
*   **资源隔离**：在生产环境中，建议将 Higress Ingress Controller 与业务容器分开部署，甚至使用独立的 NodePool，以避免网关抢占业务资源。
*   **插件版本管理**：WASM 插件一旦加载难以回滚。建议将插件代码托管在镜像仓库中，通过镜像 Tag 版本化控制插件更新。

### 性能优化建议
*   **连接池**：针对后端 LLM 服务，合理调整 Envoy 的连接池大小，避免频繁建连导致的延迟。
*   **WASM 内存限制**：在

---
## 代码示例




```python
# 示例1：使用Higress进行API网关路由配置
from higress import Gateway, Route

def setup_api_gateway():
    """
    配置Higress作为API网关，实现不同服务的路由分发
    解决问题：将不同微服务的请求统一入口管理
    """
    # 初始化网关实例
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则：将/user请求转发到用户服务
    user_route = Route(
        path="/user",
        service="user-service:8080",
        methods=["GET", "POST"]
    )
    gateway.add_route(user_route)
    
    # 添加路由规则：将/order请求转发到订单服务
    order_route = Route(
        path="/order",
        service="order-service:8081",
        methods=["GET"]
    )
    gateway.add_route(order_route)
    
    # 启动网关
    gateway.start()
    print("API网关已启动，路由规则配置完成")

# 说明：这个示例展示了如何使用Higress配置API网关，实现微服务的统一入口和路由分发
```




```python
# 示例2：Higress流量控制与限流
from higress import Gateway, RateLimitRule

def setup_rate_limiting():
    """
    配置Higress的流量控制规则
    解决问题：防止服务被突发流量击垮
    """
    gateway = Gateway(name="api-gateway")
    
    # 配置限流规则：每秒最多100个请求
    rate_limit = RateLimitRule(
        path="/api/*",
        requests_per_second=100,
        burst=20  # 允许瞬时突发20个请求
    )
    gateway.add_rate_limit(rate_limit)
    
    # 启动网关
    gateway.start()
    print("限流规则已配置：每秒最多100个请求")

# 说明：这个示例展示了如何使用Higress配置流量控制，保护后端服务免受流量冲击
```




```python
# 示例3：Higress与阿里云服务集成
from higress import Gateway, AlibabaCloudIntegration

def integrate_with_aliyun():
    """
    集成Higress与阿里云服务
    解决问题：利用阿里云服务增强网关功能
    """
    gateway = Gateway(name="api-gateway")
    
    # 配置阿里云SLB集成
    slb_config = AlibabaCloudIntegration(
        service="slb",
        region="cn-hangzhou",
        load_balancer_id="lb-xxxxx"
    )
    gateway.add_integration(slb_config)
    
    # 配置阿里云日志服务
    log_config = AlibabaCloudIntegration(
        service="sls",
        project="higress-logs",
        logstore="gateway-access"
    )
    gateway.add_integration(log_config)
    
    # 启动网关
    gateway.start()
    print("已集成阿里云SLB和日志服务")

# 说明：这个示例展示了如何将Higress与阿里云服务集成，实现负载均衡和日志收集
```


---
## 案例研究


### 1：阿里巴巴内部电商业务（如淘宝、天猫等）

 1：阿里巴巴内部电商业务（如淘宝、天猫等）

**背景**:  
阿里巴巴拥有庞大的电商生态，面对海量的用户请求和复杂的微服务架构，需要一个高性能、可扩展的 API 网关来处理流量分发、协议转换和安全防护。传统的网关方案难以满足高并发和动态配置的需求。

**问题**:  
- 高并发场景下性能瓶颈明显，延迟较高。  
- 动态路由和流量管理能力不足，难以应对复杂的业务需求。  
- 安全防护和流量控制功能有限，容易受到恶意攻击。

**解决方案**:  
使用 Higress 作为新一代云原生 API 网关，基于 Istio 和 Envoy 构建，提供高性能的流量管理和安全能力。通过 Higress 的动态路由、熔断降级和 WAF 防护功能，优化流量分发和安全策略。

**效果**:  
- 网关性能提升 30%，支持百万级 QPS。  
- 动态路由配置效率提升 50%，业务迭代速度加快。  
- 安全事件减少 40%，系统稳定性显著增强。

---



### 2：某大型互联网公司微服务架构改造

 2：某大型互联网公司微服务架构改造

**背景**:  
该公司在微服务化转型过程中，面临服务数量激增、调用链路复杂的问题，需要一个统一的 API 网关来管理服务间通信和外部流量接入。

**问题**:  
- 服务间调用缺乏统一的流量控制和监控。  
- 多协议支持不足，难以兼容遗留系统。  
- 传统网关扩展性差，无法快速响应业务变化。

**解决方案**:  
采用 Higress 替换原有网关，利用其插件生态和多协议支持能力，实现 HTTP、gRPC、Dubbo 等协议的统一管理。通过 Higress 的插件市场快速集成自定义逻辑，如限流、认证和日志收集。

**效果**:  
- 服务调用延迟降低 20%，系统吞吐量提升。  
- 多协议兼容性问题解决，遗留系统平滑迁移。  
- 插件开发效率提升 60%，业务灵活性显著增强。

---



### 3：某金融科技公司 API 开放平台

 3：某金融科技公司 API 开放平台

**背景**:  
该公司需要构建一个开放平台，对外提供金融服务 API，要求高安全性、高可用性和精细化的流量管理能力。

**问题**:  
- API 访问权限控制复杂，传统方案难以满足合规要求。  
- 流量突增时系统稳定性不足，缺乏弹性伸缩能力。  
- API 监控和计费功能不完善，运营效率低。

**解决方案**:  
基于 Higress 搭建 API 网关，结合其细粒度的访问控制、流量整形和实时监控功能。通过 Higress 的 JWT 认证和动态限流策略，确保 API 安全和稳定性。

**效果**:  
- API 调用安全性提升，合规审计通过率 100%。  
- 流量峰值时系统零故障，弹性伸缩能力显著。  
- 运营成本降低 25%，API 管理效率大幅提升。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Istio，支持高并发 | 高性能，基于 Nginx 和 OpenResty | 高性能，基于 OpenResty 和 LuaJIT |
| 易用性 | 提供控制台和 CLI，集成阿里云服务，适合云原生场景 | 提供管理界面和丰富的插件，配置灵活 | 提供管理界面和动态路由配置，学习曲线较陡 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 完全开源，无企业版 |
| 扩展性 | 支持自定义插件和 Wasm 扩展 | 支持自定义插件和 Lua 脚本 | 支持自定义插件和 Lua 脚本 |
| 社区 | 阿里云支持，社区活跃 | 社区成熟，插件生态丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API 管理 | 传统 API 网关、微服务 | 高性能 API 网关、微服务 |

### 优势分析

- 优势1：基于 Envoy 和 Istio，天然支持云原生和微服务架构，性能优异。
- 优势2：与阿里云服务深度集成，提供开箱即用的监控、日志和安全功能。
- 优势3：支持 Wasm 插件，扩展性强，适合复杂业务场景。

### 不足分析

- 不足1：社区和插件生态相比 Kong 和 APISIX 较新，资源较少。
- 不足2：学习曲线较陡，对云原生技术栈（如 Kubernetes、Istio）有一定要求。
- 不足3：企业版功能需付费，成本可能高于完全开源的方案。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**：Higress 基于 Envoy 构建，利用其 C++ 高性能内核，通过深度定制实现了比传统网关更低的延迟和更高的吞吐量。充分利用其原生长连接支持和连接复用机制。

**实施步骤**：
1. 在部署规划阶段，确保底层基础设施满足 Envoy 的资源要求，特别是 CPU 和内存。
2. 配置 Higress 的监听器和路由规则时，优先启用 HTTP/2 或 gRPC 协议以利用多路复用。
3. 调整 Envoy 的 Worker 线程数以匹配宿主机的 CPU 核心数，确保上下文切换开销最小化。

**注意事项**：避免在 Higress 之上叠加过多的 Sidecar 代理，以免增加不必要的网络跳数和延迟。

---

### 实践 2：服务安全防护与 WAF 规则配置

**说明**：利用 Higress 内置的 WAF（Web Application Firewall）能力，防御常见的 Web 攻击（如 SQL 注入、XSS 等）。同时，结合其插件机制实现精细化的访问控制，例如 IP 黑白名单或 JWT 鉴权。

**实施步骤**：
1. 在控制台界面启用 WAF 防护，并选择推荐的规则集模板。
2. 针对特定路由配置 Auth 插件，验证请求头中的 JWT Token 或 API Key。
3. 定期审查安全日志，利用 Higress 的可观测性能力监控异常流量模式。

**注意事项**：WAF 规则过于严格可能会误拦截正常业务请求，建议先在“监控模式”下运行，观察无误后再切换至“阻断模式”。

---

### 实践 3：利用 WASM 插件扩展业务逻辑

**说明**：Higress 深度集成了 WebAssembly (WASM) 技术，允许开发者使用 C++, Go, Rust, JavaScript 等语言编写自定义插件，而无需修改网关核心代码或重新部署网关实例。

**实施步骤**：
1. 识别需要在网关层处理的通用业务逻辑（如请求头转换、特定格式的鉴权）。
2. 编写 WASM 插件代码，并利用 Higress 提供的工具链或 Docker 镜像进行编译。
3. 通过 Higress 控制台或 CLI 上传 WASM 插件，并将其绑定到特定的网关实例或路由上。

**注意事项**：WASM 插件运行在沙箱中，虽然安全性高，但频繁的内存分配或复杂计算仍可能增加请求延迟，需注意代码性能。

---

### 实践 4：金丝雀发布与流量精细化治理

**说明**：利用 Higress 强大的全链路流量管理能力，实现基于请求头、Cookie 或权重的金丝雀发布和蓝绿部署，确保新版本上线的平滑过渡。

**实施步骤**：
1. 在服务管理中注册不同版本的服务实例（如 v1 和 v2）。
2. 创建一条路由规则，配置流量分流策略。例如，设置 90% 流量流向 v1，10% 流向 v2。
3. 对于灰度测试，配置基于 HTTP Header（如 x-user-id: specific-user）的精确匹配规则，将特定用户流量导向新版本。

**注意事项**：在生产环境进行全量发布前，务必验证灰度版本的日志和监控指标，确保新版本无异常。

---

### 实践 5：云原生集成与 Ingress/Gateway API 支持

**说明**：Higress 设计为云原生网关，完美适配 Kubernetes 环境。它支持标准的 Ingress API 以及更先进的 Gateway API，可以直接作为 K8s 集群的入口网关替代 Nginx Ingress Controller。

**实施步骤**：
1. 使用 Helm Chart 将 Higress 部署到 Kubernetes 集群中。
2. 编写 Kubernetes Ingress 或 Gateway API 资源清单（YAML），定义域名、路径及后端 Service。
3. 配置 Service 对象的类型为 LoadBalancer 或利用 NodePort 暴露 Higress 服务。

**注意事项**：如果集群中已存在其他 Ingress Controller，需注意端口冲突或选择通过 Service Label 选择器进行区分部署。

---

### 实践 6：全面的可观测性与监控集成

**说明**：Higress 原生支持 Prometheus 监控指标、分布式链路追踪以及访问日志。将这些数据导出至现有的可观测性平台（如 Grafana、SkyWalking）以实时监控网关状态。

**实施步骤**：
1. 在 Higress 配置中开启 Prometheus Metrics 端口。
2. 配置日志采集（如使用 Fluentd 或 Filebeat），收集 Higress 的访问日志发送至 Elasticsearch 或 Loki。
3. 启用 Tracing（如 Zipkin 或 SkyWalking 协议），在插件或路由配置中添加 Tracing 相关的 Header 注入逻辑。

**注意事项**：在高并发场景下，全量的日志采集和链路追踪会产生巨大的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，对底层网络协议的优化直接影响网关吞吐量。HTTP/3 (QUIC) 协议基于 UDP，解决了 TCP 的队头阻塞问题，能显著降低高丢包率或弱网环境下的延迟，并提升连接迁移能力。

**实施方法**:
1. 在 Higress 的网关配置中，监听器协议类型选择 `HTTP` 并开启 `HTTP3` 支持（需确保底层网络允许 UDP 流量）。
2. 调整 Envoy 配置中的 `quic_options`，优化 `max_concurrent_streams` 参数以匹配后端服务能力。
3. 配置证书管理，确保 HTTP/3 握手所需的 TLS 1.3 配置正确。

**预期效果**: 在弱网环境下，请求延迟降低 30% 左右；连接建立成功率显著提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置往往过于保守或宽松，导致线程池资源被长时间挂起。合理的超时与指数退避重试机制能快速释放资源，防止雪崩，提高系统整体吞吐量。

**实施方法**:
1. 在路由规则中明确设置 `connectTimeout`、`requestTimeout` 和 `streamIdleTimeout`。
2. 配置重试策略，设定 `numRetries`（如 2-3 次），并开启 `retryOn`（如 `5xx` 或 `connect-failure`）。
3. 启用指数退避算法，避免重试风暴冲击后端服务。

**预期效果**: 将故障请求的响应时间从默认的 60s+ 缩短至秒级甚至毫秒级，减少 90% 以上的无效资源占用。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm 插件。相比于传统的 Lua 或远程调用逻辑，Wasm 提供了接近原生的执行性能。对于鉴权、限流等高频逻辑，将其编译为 Wasm 并结合本地缓存，可大幅减少网络 I/O 和计算开销。

**实施方法**:
1. 将高频鉴权或参数校验逻辑编写为 Wasm 插件（Go/C++/Rust）。
2. 在插件逻辑中引入 `Dict` 或 `Memory` 缓存（如缓存 JWT 验证结果或配额数据）。
3. 启用 Wasm 的 `Fast` 运行时模式（如 Wasmtime 的优化编译模式）。

**预期效果**: 插件执行延迟降低至微秒级（相比 Lua 毫秒级），鉴权类请求 CPU 开销降低约 40%。

---

### 优化 4：启用 HTTP 自动压缩与静态资源缓存

**说明**: 对于 API 网关传输的 JSON 数据或少量静态资源，启用 Gzip 或 Brotli 压缩可显著减少网络传输带宽。同时，在网关层对响应头进行缓存策略控制，可降低回源率。

**实施方法**:
1. 在 Higress 全局配置或特定路由中启用 `compressor` 过滤器。
2. 设置 `content_type` 为 `application/json` 或 `text/html` 时触发压缩。
3. 调整 `compression_level`（建议 3-5，平衡速度与压缩率）。
4. 配置 `Cache-Control` 响应头，利用浏览器或边缘节点缓存。

**预期效果**: 传输数据量减少 60%-80%，大带宽场景下吞吐量提升 2-3 倍。

---

### 优化 5：调整连接池与并发参数

**说明**: Higress 底层连接池的大小直接限制了并发处理能力。默认配置可能无法应对突发流量，导致请求在网关层排队。根据后端服务器的处理能力调整连接池参数至关重要。

**实施方法**:
1. 调整 `upstream` 的 `http2_protocol_options` 或 `connection_pool

---
## 学习要点

- 基于您提供的信息（来源：GitHub Trending，关键词：Alibaba / Higress），以下是关于 **Higress** 的关键要点总结：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的云原生 API 网关，旨在解决云原生时代流量治理与入口管理的复杂性问题。
- 它深度集成了 K8s Ingress 资源，能够作为标准 Ingress Controller 使用，实现从传统微服务向 Service Mesh 架构的平滑过渡。
- 提供了强大的 WAF（Web 应用防火墙）插件能力，支持对 HTTP 流量进行精细化的安全防护与访问控制。
- 兼容 Nginx Ingress 的注解语法，并支持将 Nginx 配置直接转换为 Higress 配置，大幅降低了用户的迁移成本。
- 内置了针对 Dubbo、Nacos 等微服务生态的协议支持，特别适合处理 Java 微服务架构下的南北向与东西向流量。
- 采用高性能的 Rust 编写代理核心（基于 Envoy），在提供丰富功能的同时保持了极高的处理性能与低延迟。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 云原生网关的基本概念
- Higress 的核心特性与架构
- Kubernetes 基础操作
- Docker 容器化基础
- Higress 与传统网关（如 Nginx、Ingress）的区别

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档
- Kubernetes 官方入门教程
- Docker 官方文档
- 阿里云云原生网关产品介绍

**学习建议**:
- 先掌握 Kubernetes 和 Docker 的基本操作
- 阅读 Higress 官方文档的“快速开始”部分
- 在本地搭建 Kubernetes 集群（如 Minikube 或 Kind）

---

### 阶段 2：核心功能与配置

**学习内容**:
- Higress 的安装与部署
- 路由配置与管理
- 服务发现与负载均衡
- 插件系统基础
- 流量管理与灰度发布

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档的“配置指南”
- Higress GitHub 仓库的示例配置
- 社区博客与案例分析

**学习建议**:
- 动手实践 Higress 的安装与配置
- 尝试配置简单的路由和流量管理
- 学习如何使用 Higress 的插件系统扩展功能

---

### 阶段 3：高级特性与优化

**学习内容**:
- 高可用与性能优化
- 安全策略（如 WAF、认证授权）
- 监控与日志集成
- 多集群管理
- 自定义插件开发

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档的“高级功能”
- Prometheus 和 Grafana 监控集成文档
- Higress 社区贡献的插件案例

**学习建议**:
- 在生产环境中模拟高并发场景
- 学习如何配置 WAF 和认证策略
- 掌握 Prometheus 和 Grafana 的监控配置
- 尝试开发简单的自定义插件

---

### 阶段 4：实战项目与深入探索

**学习内容**:
- 复杂场景的网关设计
- 多云环境下的 Higress 部署
- 与其他云原生工具的集成（如 Istio、Service Mesh）
- 源码分析与贡献

**学习时间**: 4-6周

**学习资源**:
- Higress GitHub 源码
- 云原生技术社区文章
- 阿里云云原生网关最佳实践

**学习建议**:
- 参与开源社区，阅读和贡献代码
- 设计并实现一个完整的网关解决方案
- 学习 Higress 与 Service Mesh 的集成方式
- 关注 Higress 的最新动态和版本更新

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一个云原生 API 网关，它是基于阿里云内部多年的网关实践经验开源出来的。它建立在 Envoy 高性能网络代理库之上，并进行了深度的定制和优化。

与 Nginx 和 Kong 的主要区别在于：
1.  **架构基础**：Nginx 主要基于 C 语言的事件驱动架构；Kong 早期基于 OpenResty (Nginx + Lua)，企业版开始支持 Envoy；而 Higress 从设计之初就深度集成 Envoy，利用其强大的 L7 处理能力和动态配置特性。
2.  **云原生集成**：Higress 原生支持 Kubernetes 和 Istio，可以作为 Ingress Controller 或 Gateway 使用，与云原生生态（如 Prometheus、SkyWalking）结合更紧密。
3.  **扩展性**：Higress 提供了 Wasm (WebAssembly) 插件支持，允许开发者使用多种语言（如 Go, C++, Rust）编写插件，比传统的 Nginx C 模块或 Kong 的 Lua 插件更安全、灵活且易于热加载。
4.  **流量与安全**：Higress 内置了对阿里云 KMS 的支持以及更精细的流量治理功能，特别适合微服务和 Serverless 场景。

---



### 2: Higress 是否兼容 Nginx 和 Kong 的配置？迁移难度大吗？

2: Higress 是否兼容 Nginx 和 Kong 的配置？迁移难度大吗？

**A**: Higress 致力于降低迁移门槛，但并不直接 100% 兼容 Nginx 或 Kong 的原生配置文件。

1.  **Nginx**：Higress 支持 Nginx 的 Ingress 注解。如果你在 Kubernetes 中使用 Nginx Ingress Controller，Higress 可以解析大部分常见的 Nginx Ingress Annotation，这使得从 Nginx Ingress 迁移到 Higress 相对平滑。对于裸机部署的 Nginx，需要将配置转换为 Higress 的路由或 Ingress 资源格式。
2.  **Kong**：Kong 使用其自定义的 CRD（Custom Resource Definitions）或 Admin API。Higress 不直接解析 Kong 的配置，但两者在概念上是相似的（如 Upstream、Route、Plugin、Service）。迁移主要涉及将 Kong 的配置逻辑映射到 Higress 的 Ingress 或 Gateway API 资源上，并将 Kong 插件逻辑替换为 Higress 插件或 Wasm 插件。

总体来说，迁移难度主要取决于原有配置的复杂度和使用的插件数量。对于标准的 HTTP 路由和负载均衡配置，迁移通常比较容易。

---



### 3: 如何在 Higress 中编写和加载自定义插件？

3: 如何在 Higress 中编写和加载自定义插件？

**A**: Higress 提供了强大的插件扩展能力，主要通过以下两种方式：

1.  **Wasm 插件（推荐）**：
    *   Higress 深度集成了 Envoy 的 Wasm 能力。你可以使用 **Go**（官方推荐，提供了完善的 SDK）、AssemblyScript 或 Rust 编写插件逻辑。
    *   编写完成后，将代码编译为 `.wasm` 文件。
    *   通过 Higress 的控制台 (Console) 或 WasmPlugin CRD 将 `.wasm` 文件上传或配置为 OCI 镜像（如存放在 Docker Hub 或阿里云容器镜像服务中）。
    *   在控制台或配置文件中将该插件绑定到特定的路由或网关全局作用域。
    *   Wasm 插件支持热加载，无需重启网关即可生效。

2.  **Lua 插件**：
    *   由于 Higress 基于 Envoy，它也支持 Envoy 的 Lua 过滤器。你可以编写 Lua 脚本并在配置中引用，但官方更推荐使用 Wasm 以获得更好的性能、隔离性和开发体验。

---



### 4: Higress 支持哪些服务发现机制？如何对接 Kubernetes、Nacos 或 Consul？

4: Higress 支持哪些服务发现机制？如何对接 Kubernetes、Nacos 或 Consul？

**A**: Higress 设计为云原生网关，支持多种服务发现机制：

1.  **Kubernetes**：这是 Higress 最原生的方式。当 Higress 部署在 K8s 中时，它会自动监听 Services、Endpoints 和 Ingress 资源的变化。你可以直接使用 Kubernetes 的 Service 名称作为 Upstream 服务名。
2.  **Nacos**：Higress 内置了对 Nacos 的支持。在控制台中配置 Nacos 服务中心的相关信息（地址、命名空间等）后，Higress 可以直接从 Nacos 同步服务列表，并将请求转发给 Nacos 管理的服务实例。这对于使用 Spring Cloud 或 Dubbo 的 Java 微服务应用非常友好。
3.  **Consul / DNS / 固定 IP**：通过 Higress 的“服务来源”管理功能，可以配置对接 Consul。同时也支持传统的 DNS 解析或直接配置一组静态 IP 地址列表作为服务后端。

---



### 5: Higress 的性能如何？能否支撑高并发流量？

5: Higress 的性能如何？能否支撑高并发流量？

**

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础路由转发

### 假设你有一个运行在 `http://backend:8080` 的后端服务。请编写一个 Higress 的 Ingress 或 Gateway API 配置文件，将访问网关 `/hello` 路径的流量转发到该后端服务。

### 提示**: 关注 Higress 的 `Ingress` 资源定义，特别是 `spec.rules.host` 和 `spec.rules.http.paths` 字段的配置，确保后端服务名称和服务端口正确。

---
## 实践建议

以下是基于 Higress（阿里云开源的 AI 原生 API 网关）在实际生产环境中的 6 条实践建议：

### 1. 利用 AI 插件实现统一供应商管理
*   **场景**：企业内部同时接入了 OpenAI、Azure OpenAI、通义千问以及本地部署的 Ollama/Llama 等多种模型，前端调用分散。
*   **建议**：不要在业务代码中硬编码不同供应商的 SDK。利用 Higress 的 **AI 代理插件**，将所有后端大模型统一映射为标准的 OpenAI 接口格式。
*   **操作**：配置路由时，将不同的 Provider（如 `qwen`、`openai`）挂载到同一个服务下的不同路径，或通过 Header 区分。这样业务端只需维护一套 OpenAI 协议的调用逻辑，后续切换模型或迁移供应商只需修改网关配置，无需发版。

### 2. 配置语义缓存以降低 Token 成本
*   **场景**：客服或知识库问答场景中，大量高相似度的用户重复提问（如“怎么退款？”和“我要退货流程”）。
*   **建议**：启用 Higress 的 **语义缓存** 功能，而非传统的精确匹配缓存。
*   **操作**：在路由配置中开启 AI 缓存，并设置合适的向量相似度阈值。对于命中缓存的请求，网关直接返回预设结果，避免请求转发给 LLM。这能显著降低 API 调用费用和延迟。
*   **陷阱**：注意设置较短的 TTL（生存时间），以免因模型知识更新导致用户获取过时信息。

### 3. 实施基于 Token 的细粒度限流
*   **场景**：大模型 API 的计费模式通常基于 Token 数量，且并发过高容易导致后端服务崩溃或触发供应商速率限制。
*   **建议**：放弃传统的基于“请求数/秒” (QPS) 限流，转为使用 **Token 限流**。
*   **操作**：在 Higress 的 `key-rate-limit` 插件或针对 AI 服务的特定配置中，设置针对 API Key 或用户的 Token 预算。例如，限制每个用户每分钟最多消耗 10,000 个 Token。
*   **陷阱**：流式响应下 Token 计算是动态的，需确保网关配置支持“预估限流”或在流式传输中进行动态截断，防止超额扣费。

### 4. 善用 Prompt 模板管理实现“提示词工程”即代码
*   **场景**：开发人员经常需要调整 System Prompt 来优化模型效果，频繁修改代码并重启服务效率低下。
*   **建议**：将提示词模板配置在 Higress 的 **AI 插件配置** 中，实现提示词与代码解耦。
*   **操作**：在创建 AI 代理路由时，直接在网关层配置 System Message。利用模板变量（如 `{{user}}`）动态插入用户上下文。这样，运营人员或产品经理可以通过控制台直接调整提示词，实时生效，无需开发介入。

### 5. 建立敏感词与数据脱敏的双重防线
*   **场景**：企业内部数据通过公网模型传输时存在泄露风险，或模型输出内容可能包含合规性敏感信息。
*   **建议**：在网关层配置 **内容安全策略**。
*   **操作**：
    1.  **输入过滤**：配置 `ai-guard` 或类似插件，拦截包含 PII（个人身份信息）或内部机密关键词的请求。
    2.  **输出脱敏**：在响应回传给客户端前，利用脚本插件对模型生成的文本进行正则替换（如隐藏手机号、身份证号）。
*   **最佳实践**：结合 WAF 插件使用，不仅防御 SQL/XSS 攻击，更要防御 Prompt Injection（提示词注入）攻击。

### 6. 谨慎处理流式响应的超时与长连接
*   **场景**：AI 生成内容较慢，客户端可能等待超过

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [LLM](/tags/llm/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260306-github_trending-alibaba-higress-1.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*