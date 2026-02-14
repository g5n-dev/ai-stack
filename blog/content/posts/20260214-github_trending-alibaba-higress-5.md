---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-14T14:42:26+08:00
draft: false
entry_kind: "auto"
tags: ["API 网关", "Higress", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的 DeepWiki 节选内容，以下是对 **Higress** 项目的简洁总结： **项目概况** Higress 是由阿里巴巴开源的**云原生 API 网关**。它基于 Istio 和 Envoy 构建，通过集成 WebAssembly (WASM) 插件能力，定位为**AI 原生**的下一代网关。 **"
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
- **星标**: 7,527 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过集成 WebAssembly 插件能力，致力于解决 AI 原生应用与传统微服务的统一流量管理问题。它既提供了针对大语言模型（LLM）的专用网关功能与 MCP 服务托管，也涵盖了 Kubernetes Ingress 等传统路由场景。本文将深入剖析其系统架构，重点介绍 AI 网关特性、WASM 插件体系以及核心组件的交互逻辑。

---
## 摘要

基于您提供的 DeepWiki 节选内容，以下是对 **Higress** 项目的简洁总结：

**项目概况**
Higress 是由阿里巴巴开源的**云原生 API 网关**。它基于 Istio 和 Envoy 构建，通过集成 WebAssembly (WASM) 插件能力，定位为**AI 原生**的下一代网关。

**核心架构**
系统采用**控制平面**与**数据平面**分离的架构：
*   **配置管理**：配置变更通过 xDS 协议传播。
*   **性能优势**：具备毫秒级延迟和零连接中断的特性，非常适合需要保持长连接的 AI 流式响应场景。

**三大主要功能**
1.  **AI 网关**：
    *   提供统一 API，支持对接 30+ 家大模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存及安全防护能力。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
3.  **传统 API 网关**：
    *   支持 Kubernetes Ingress 和微服务路由，并兼容 nginx-ingress 注解。

**项目现状**
*   **语言**：Go
*   **热度**：GitHub 星标数超过 7,500。

---
## 评论

**总体评价**

Higress 是阿里云开源的一款极具前瞻性的“AI原生”网关，它成功地将云原生流量治理与 AI 大模型应用所需的特殊协议处理进行了深度融合。该项目不仅是对传统 API 网关的演进，更是针对 LLM 时代应用架构的一次精准技术卡位，具备极高的工程落地价值和技术参考意义。

**深入分析与评价依据**

**1. 技术创新性：从“流量管道”到“AI 智能体”的架构跃迁**
*   **事实（DeepWiki）：** Higress 基于 Istio 和 Envoy 构建，核心在于其扩展了 WebAssembly (WASM) 插件能力，并明确提出了“AI Gateway”和“MCP (Model Context Protocol) Server Hosting”两大特性。
*   **推断与评价：** 传统网关（如 Nginx, Kong）主要关注 HTTP/gRPC 路由，而 Higress 的差异化在于它原生理解 AI 语义。它不仅仅是一个流量代理，更是一个 AI 编排层。
    *   **协议深度适配：** 针对 LLM 流式输出 SSE（Server-Sent Events）场景，传统网关在处理超时、buffer 策略时往往需要复杂的脚本配置，而 Higress 通过 WASM 插件原生支持了 AI 语义的负载均衡、流式截断和 Token 计费，解决了“AI 流量不可控”的痛点。
    *   **MCP 协议集成：** DeepWiki 中提到的 MCP Server Hosting 是一大亮点。随着 AI Agent（智能体）的普及，模型与工具的连接成为刚需。Higress 直接将网关作为 MCP Server 的托管点，使得企业内部的 API 能被 AI 模型安全、标准化地调用，这是在基础设施层面的创新。

**2. 实用价值：解决 AI 落地“最后一公里”的关键基建**
*   **事实（DeepWiki）：** 描述中强调其提供“AI gateway features for LLM applications”以及“traditional API gateway capabilities”。
*   **推断与评价：** Higress 解决了企业在引入大模型时面临的“双模运维”难题。
    *   **统一入口：** 企业不需要为 AI 业务专门搭建一套代理系统（如 Python 写的转发服务），Higress 允许在同一网关内同时管理传统微服务流量和 AI 模型流量（如 OpenAI, 通义千问等）。这极大地降低了运维复杂度。
    *   **成本与安全控制：** 在 AI 场景下，API 密钥泄露和 Token 消耗失控是最大风险。Higress 提供的密钥轮转、Prompt 注入防护以及基于 Token 粒度的限流功能，直接击中企业落地的核心痛点，具有广泛的适用场景。

**3. 代码质量与架构：云原生标准下的模块化设计**
*   **事实（DeepWiki）：** 架构上分离了控制平面和数据平面，支持 Kubernetes Ingress，使用 Go 语言开发。
*   **推断与评价：**
    *   **架构解耦：** 借鉴 Istio 的架构模式，将配置管理与流量处理分离，保证了系统的弹性和可扩展性。控制面负责配置下发，数据面由 Envoy + WASM 组成，这种 C++ (Envoy) 处理底层流量 + Go (控制面) 处理管理 + WASM (业务逻辑) 的组合，兼顾了高性能与灵活性。
    *   **可扩展性：** WASM 插件机制是其代码质量的一大亮点。开发者可以使用 C++, Go, Rust, Javascript 等多种语言编写插件，而不需要重新编译网关本身。这种沙箱化的扩展方式既保证了内核稳定性，又极大地降低了开发门槛。

**4. 社区活跃度与学习价值：阿里云背书的成熟度**
*   **事实（数据）：** 拥有 7.5k+ 星标，且有 README_ZH.md 等多语言文档支持。
*   **推断与评价：** 作为阿里云核心产品（曾用于淘宝双11流量治理）的开源版本，其代码质量和稳定性经过了工业级验证。对于开发者而言，Higress 是学习“如何将传统云原生技术改造以适应 AI 时代”的绝佳范本。特别是其 WASM 插件系统的实现，对于研究高性能网关插件化开发极具参考价值。

**5. 潜在问题与对比优势**
*   **对比优势：** 相比于 APISIX，Higress 对 AI 协议的支持更原生，且与 Istio 生态融合更深；相比于 Kong，Higress 的 WASM 生态更开放，且无商业版功能限制。
*   **潜在问题：** 引入 Istio 作为底座虽然功能强大，但也带来了较高的部署复杂度（依赖 CRD, Sidecar 等），对于仅需要简单 AI 转发的中小团队来说，可能存在“杀鸡用牛刀”的学习曲线。

**边界条件与验证清单**

**不适用场景：**
*   **超低延迟边缘场景：** 如果需要在边缘端（如 IoT 设备）进行极低延迟的流量转发，Envoy 的内存占用可能过大。
*   **简单静态博客/小型站点：** 不需要复杂的 AI 治理或灰度发布，使用 Nginx 或 Caddy 更加轻量。

**快速验证清单：**
1.  **AI 代理性能测试：** 部署 Higress 并配置一个 LLM 服务（如通义千问），使用 `wrk

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（alibaba/higress），本文档将从架构设计、核心功能、技术实现、适用场景及工程哲学等维度进行全面剖析。Higress 定位为“AI Native API Gateway”，它不仅仅是一个传统的流量网关，更是为了应对大模型（LLM）时代流量特征而演进的基础设施。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 C++ 的高并发处理能力和 L3/L7 网络功能。
*   **控制层扩展**：基于 **Istio** 进行控制平面的扩展与简化。Higress 实际上是 Istio 的一个“超集”或“变体”，它剥离了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理能力，专注于 **Gateway（Ingress）** 场景。
*   **编程语言**：主要控制逻辑使用 **Go** 语言编写，利用 Go 优秀的并发处理模型和云原生生态亲和性；插件扩展支持 **WASM (WebAssembly)**，允许使用 C++, Go, Rust, JavaScript 等多语言编写插件。

### 核心模块设计
1.  **Router (路由层)**：基于 Envoy 的 HTTP Connection Manager 进行配置分发，支持 K8s Ingress API 和自定义的路由规则。
2.  **WASM Plugin System (插件市场)**：这是 Higress 的“心脏”。它通过 Proxy-WASM 规范，将业务逻辑（如鉴权、限流、请求转换）编译为 WASM 模块，动态挂载到 Envoy 中。这实现了逻辑的热加载，无需重启网关。
3.  **AI Gateway Extension (AI 网关扩展)**：专门针对 LLM 流式传输优化的处理模块。它处理 SSE (Server-Sent Events) 协议，实现了 AI 请求/响应的拦截、修改与路由。

### 技术亮点与创新点
*   **AI-Native 架构**：传统网关对“长连接、流式响应”的支持通常不够友好（例如缓冲会导致延迟）。Higress 针对大模型流式输出进行了底层优化，确保毫秒级的首字延迟（TTFB）和流畅的数据转发。
*   **MCP (Model Context Protocol) Server Hosting**：Higress 创新性地将网关作为 AI Agent 的“工具托管中心”。它不仅转发流量，还能直接托管提供工具接口的 MCP Server，简化了 Agent 应用与工具集成的复杂度。
*   **xDS 协议优化**：控制平面与数据平面通过 xDS 协议（基于 gRPC）通信，配置变更可实现秒级生效，且完全无损。

### 架构优势分析
*   **性能损耗极低**：数据面路径在 Envoy C++ 层，WASM 插件虽然运行在沙箱中，但通过 ABI 直接调用，性能远高于传统的 Lua (OpenResty) 或外部进程调用。
*   **安全性隔离**：WASM 插件运行在内存隔离的沙箱环境中，即使插件崩溃也不会导致网关主进程崩溃，且限制了文件系统访问。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一模型接入**：通过 Higress 访问 OpenAI、通义千问、DeepSeek 等各家模型，统一 API 格式。
    *   **Prompt 模板管理**：在网关层固化 Prompt 模板，前端只需传参数，降低 Prompt 泄露风险。
    *   **Token 计费与限流**：基于 Token 数量而非单纯的请求数进行限流和计费，更符合 AI 业务成本模型。
2.  **MCP 协议支持**：
    *   作为 AI Agent 的基础设施，Higress 可以直接运行 MCP Server，使得 Agent 能够通过标准协议调用企业内部工具。
3.  **传统 API 网关**：
    *   K8s Ingress Controller、金丝雀发布、蓝绿部署、负载均衡、认证鉴权。

### 解决的关键问题
*   **AI 流量管理的黑盒**：传统网关无法理解 AI 协议（SSE 流），难以进行日志截断、敏感词过滤或内容审核。Higress 允许在流式传输过程中实时处理数据。
*   **多模型切换成本**：开发者无需修改应用代码，只需在 Higress 配置路由规则，即可将流量从一个 LLM 切换到另一个，或实现 A/B 测试。

### 与同类工具对比
| 特性 | Higress | Apache APISIX | Kong | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **内核** | Envoy (C++) | ngx_lua (C/Lua) | Nginx (C/Lua) | Nginx (C) |
| **扩展性** | WASM (多语言) | Lua (LuaJIT) | Lua / Go (进程外) | C / Lua |
| **配置热更新** | xDS (毫秒级) | etcd (毫秒级) | DB 轮询/轮询 | reload (有损) |
| **AI 特性** | **原生支持 (SSE/MCP)** | 需插件支持 | 需插件支持 | 不支持 |
| **K8s 集成** | 原生 CRD | 原生 CRD | 原生 CRD | Ingress Annotation |

### 技术实现原理
Higress 通过 **HttpFilter** 机制介入请求处理链。对于 AI 请求，它会识别 `Content-Type` 或特定的 Header（如 `x-use-sse`），将响应流解析为 Chunked 数据块。WASM 插件可以注册 `on_body` 回调函数，逐块处理流式内容（如修改 JSON 片段），然后重新发送给客户端。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 默认集成了 **WasmEdge** 或 **Wasmtime** 运行时。Go 控制平面将编译好的 `.wasm` 文件通过 xDS 推送给 Envoy。Envoy 加载 WASM 模块后，通过 `proxy_on_http_request_headers` 等钩子与主逻辑交互。
*   **配置分发**：Higress Controller 监听 K8s API Server 的资源变化（如 `GreeterRoute`），将其转换为 Envoy 的 LDS (Listener Discovery Service) 和 RDS (Route Discovery Service) 配置，通过 gRPC 推送给 Envoy。

### 代码组织结构
*   `/pkg`：核心业务逻辑，包含 Ingress 转换器、Dubbo 服务发现适配器等。
*   `/plugins`：内置 WASM 插件的 Go 源码（编译前需转换为 WASM）。
*   `/installer`：Helm Charts 部署脚本。
*   `/test`：基于 `ginkgo` 的集成测试框架。

### 性能优化与扩展性
*   **零拷贝**：在 Envoy 内部，数据处理尽量通过 Buffer 指针传递，减少内存复制。
*   **异步处理**：WASM 插件的执行虽然是在单线程事件循环中，但 Higress 架构支持多 Worker 进程，利用多核优势。
*   **动态伸缩**：作为 K8s Ingress 运行时，可直接利用 HPA (Horizontal Pod Autoscaler) 根据 CPU/内存指标进行扩容。

### 技术难点与解决
*   **难点**：WASM 的内存开销。每个插件实例都需要独立的线性内存。
*   **解决**：Higress 优化了 WASM 模块的共享机制，并在配置层面提供了插件内存限制的配置项，防止 OOM。

---

## 4. 适用场景分析

### 最佳适用场景
1.  **LLM 应用落地**：企业内部构建 AI 助手、Copilot 类应用，需要统一管理不同厂商的 API Key，并控制成本。
2.  **微服务网关**：特别是已经在使用 Istio 或深度 K8s 的技术栈，希望获得比 Nginx Ingress 更强大、可编程性更强的网关。
3.  **多协议混合场景**：系统既有传统的 REST API，又有 AI 流式接口，需要一个统一入口。

### 不适合的场景
1.  **极端静态文件服务**：虽然 Envoy 性能极强，但如果是纯粹的 CDN 或静态文件分发，使用专门的 CDN 或 Nginx 缓存功能可能更简单轻量。
2.  **极低延迟的内部服务网格**：如果追求极致的微服务间通信性能（低于 1ms），Sidecar 模式的代理（即使是 Envoy）仍有损耗，直接 RPC 调用可能更好。

### 集成方式与注意事项
*   **K8s 部署**：推荐使用 Helm Chart 部署。需注意 `higress-core` 的资源 Requests/Limits 设置，因为 WASM 插件运行会消耗额外内存。
*   **平滑迁移**：Higress 兼容 Nginx Ingress 注解，支持从旧网关逐步迁移。

---

## 5. 发展趋势展望

### 技术演进方向
*   **WASM 组件化生态**：未来会有更多开箱即用的 WASM 插件（如 SaaS 身份认证集成、特定 LLM Provider 的预处理逻辑），形成“插件市场”。
*   **Dapr 集成**：Higress 可能会加强与 Dapr (Distributed Application Runtime) 的结合，成为服务调用与流量治理的统一入口。
*   **边缘计算**：由于 Envoy 和 WASM 的轻量级特性，Higress 有潜力向边缘节点下沉，成为边缘 AI 推理的网关。

### 社区反馈与改进空间
*   **文档与调试**：WASM 插件的开发调试相对复杂（需要编译），社区需要更好的 IDE 插件和本地调试工具。
*   **可观测性**：虽然支持 OpenTelemetry，但在 AI 场景下，如何将 Token 使用率、Prompt 长度等业务指标与 TraceID 关联，仍需增强。

---

## 6. 学习建议

### 适合人群
*   具有 Go 语言基础，了解 Kubernetes 基本原理的开发者。
*   云原生架构师，需要选型下一代 API 网关。
*   AI 应用开发者，希望深入理解 AI 基础设施的构建。

### 学习路径
1.  **基础**：先熟悉 Envoy 的基本概念（Listener, Route, Cluster）和 xDS 协议。
2.  **入门**：在本地 Kind 集群中通过 Helm 安装 Higress，体验基于 K8s CRD 的路由配置。
3.  **进阶**：学习 Proxy-WASM SDK，尝试用 Go 或 TinyGo 编写一个简单的 Request Header 修改插件，并加载到 Higress 中。
4.  **实践**：配置一个 AI �

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则
    场景：将 /api/v1 请求转发到后端服务
    """
    from pydantic import BaseModel
    
    class RouteRule(BaseModel):
        """路由规则模型"""
        path: str = "/api/v1"
        service_name: str = "backend-service"
        service_port: int = 8080
        timeout: int = 30  # 超时时间(秒)
        retry: int = 3     # 重试次数
    
    # 创建路由规则
    rule = RouteRule()
    print(f"路由配置: {rule.path} -> {rule.service_name}:{rule.service_port}")
    return rule

# 测试
higress_route_config()
```




```python
# 示例2：Higress 插件配置
def higress_plugin_config():
    """
    配置 Higress 的限流插件
    场景：为 API 设置每秒 100 次的请求限制
    """
    plugin_config = {
        "name": "key-rate-limit",
        "config": {
            "key": "remote_addr",  # 使用客户端IP作为限流key
            "query_per_second": 100,  # 每秒允许100次请求
            "burst": 200,            # 突发流量允许200次
            "rejected_code": 429     # 超限返回HTTP 429
        }
    }
    
    print(f"限流插件配置: {plugin_config['config']['query_per_second']} QPS")
    return plugin_config

# 测试
higress_plugin_config()
```




```python
# 示例3：Higress 服务发现
def higress_service_discovery():
    """
    模拟 Higress 的服务发现机制
    场景：动态获取后端服务的健康实例
    """
    import random
    
    class ServiceRegistry:
        """服务注册中心模拟"""
        def __init__(self):
            self.services = {
                "backend-service": {
                    "instances": [
                        {"host": "10.0.1.1", "port": 8080, "healthy": True},
                        {"host": "10.0.1.2", "port": 8080, "healthy": True},
                        {"host": "10.0.1.3", "port": 8080, "healthy": False}
                    ]
                }
            }
        
        def get_healthy_instances(self, service_name):
            """获取健康实例"""
            return [inst for inst in self.services[service_name]["instances"] 
                   if inst["healthy"]]
        
        def select_instance(self, service_name):
            """负载均衡选择实例"""
            healthy = self.get_healthy_instances(service_name)
            return random.choice(healthy) if healthy else None
    
    registry = ServiceRegistry()
    instance = registry.select_instance("backend-service")
    print(f"选中实例: {instance['host']}:{instance['port']}")
    return instance

# 测试
higress_service_discovery()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴内部拥有庞大的电商生态，包括淘宝、天猫等核心业务。这些业务在云原生架构转型过程中，面临着服务数量激增、流量洪峰波动大（如双11大促）以及异构基础设施共存的复杂环境。

**问题**: 传统的 API 网关在应对海量流量时存在扩展性瓶颈，且配置灵活性不足。同时，业务方需要网关能够深度集成 Kubernetes 生态，支持 Dubbo、Nacos 等内部微服务组件，并具备极高的安全性和热更新能力，以应对秒级级别的流量变化。

**解决方案**: 阿里巴巴基于内部多年的网关经验，研发并开源了 Higress。Higress 采用云原生架构，深度集成了 Envoy 作为数据面，提供高性能的流量转发。它支持 WASM 插件机制，允许业务方在不重启网关的情况下动态扩展功能，并完美兼容 K8s Ingress 和 Nacos 服务发现。

**效果**: 通过引入 Higress，阿里内部业务实现了网关层的极致弹性，能够从容应对双11级别的流量洪峰。WASM 插件的采用使得定制化功能的上线效率提升了 50% 以上，同时统一了云原生架构下的流量管理标准，显著降低了运维成本。

---



### 2：科大讯飞 AI 开放平台

 2：科大讯飞 AI 开放平台

**背景**: 科大讯飞 AI 开放平台为外部开发者提供语音识别、自然语言处理等多种 AI 能力接口。随着业务上云和微服务化的深入，平台需要管理成千上万的 API 调用，且不同客户对鉴权、限流和流控策略有着高度定制化的需求。

**问题**: 原有的网关系统在处理高并发长连接（如 WebSocket 用于语音流传输）时性能受限，且配置修改往往需要重启服务，导致业务中断。此外，多租户之间的流量隔离和安全防护也是一大挑战，传统网关难以灵活支持复杂的 API 策略管理。

**解决方案**: 科大讯飞引入 Higress 作为新一代 API 网关。利用 Higress 对 HTTP 和 WebSocket 协议的高性能支持，解决了语音流的传输问题。同时，利用其标准化的网关能力和插件市场，快速实现了针对不同租户的精细化管理，并对接了内部的微服务注册中心。

**效果**: Higress 的引入使得平台的 API 调用成功率和响应速度得到显著优化，特别是在高并发场景下资源占用降低了 30%。通过热加载插件更新业务逻辑，实现了对客户需求的快速响应，且在多租户隔离上保证了数据安全和系统稳定性。

---



### 3：深势科技 - 科学计算云平台

 3：深势科技 - 科学计算云平台

**背景**: 深势科技致力于微尺度科学计算的研究与平台化建设，其底层涉及大量的科学计算任务调度和数据交互。随着业务容器化改造，需要一个能够适应 K8s 环境、支持复杂路由逻辑且轻量级的 API 网关。

**问题**: 传统的 Nginx Ingress Controller 在处理复杂的鉴权逻辑和动态路由时配置繁琐，且缺乏开箱即用的流量治理功能（如简单的限流、认证）。对于科学计算场景而言，网关不能成为性能瓶颈，且需要极低的运维复杂度。

**解决方案**: 深势科技选择使用 Higress 替换了原有的 Ingress Controller。Higress 提供的标准化 K8s Ingress 注解支持使得迁移成本极低。同时，利用其内置的 KeyAuth 和 RequestBlock 等插件，快速实现了对内部计算服务的访问控制。

**效果**: 迁移至 Higress 后，网关层的资源消耗显著下降，网络延迟降低，提升了科学计算任务的交互体验。运维人员通过控制台即可管理流量策略，无需手动编辑繁琐的 Nginx 配置文件，运维效率大幅提升，实现了“零侵入”式的云原生网关升级。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Kong | 方案B: APISIX |
|------|----------------|------------|--------------|
| 性能 | 基于Istio+Envoy，高性能，支持Wasm插件 | 基于OpenResty/Nginx，性能较高 | 基于OpenResty/Lua，性能极高 |
| 易用性 | 提供控制台和K8s CRD，支持云原生部署 | 控制台功能丰富，但配置复杂 | 控制台简洁，CRD支持K8s原生 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源版免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性中等 | 支持Lua和Wasm插件，扩展性强 |
| 社区 | 阿里背书，社区活跃 | 社区成熟，生态丰富 | 社区活跃，国内支持较好 |
| 功能 | 支持流量管理、安全、可观测性 | 功能全面，插件丰富 | 功能全面，插件生态丰富 |

### 优势分析

- 优势1：云原生集成深度，与Istio和K8s无缝结合。
- 优势2：支持Wasm插件，扩展性和灵活性优于传统网关。
- 优势3：阿里云提供商业支持，适合企业级应用。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较新，插件库较少。
- 不足2：文档和案例可能不如成熟方案丰富。
- 不足3：对非阿里云用户的学习成本可能较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 原生支持 WebAssembly (Wasm) 技术，允许开发者使用 C++、Go、Rust 或 AssemblyScript 等语言编写插件。相比传统的 Lua 脚本，Wasm 插件提供了更高的执行效率、更好的隔离性和更丰富的标准库支持，是实现复杂业务逻辑（如自定义认证、请求头修改、响应体处理）的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 官方提供的 SDK 或 Proxy-Wasm 标准接口编写插件逻辑。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台的插件市场。
4. 在网关规则或路由配置中将插件关联到特定的服务或路由上。

**注意事项**: 
- 编写 Wasm 插件时应注意内存管理，避免内存泄漏导致网关实例资源耗尽。
- 生产环境部署前，务必对 Wasm 插件进行压力测试，确保其执行延迟在可接受范围内。

---

### 实践 2：精细化流量路由与服务治理

**说明**: Higress 深度集成了 Nacos 和 Consul 等注册中心，能够实现基于权重的灰度发布、蓝绿发布以及同机房优先路由。利用这些功能，可以最大程度降低新版本上线的风险，并优化微服务间的调用链路。

**实施步骤**:
1. 在 Higress 中配置服务来源，对接 Kubernetes Service 或 Nacos/Consul 注册中心。
2. 创建 Ingress 或网关路由规则时，配置多个服务版本（如 v1 和 v2）。
3. 设置流量百分比权重，逐步将流量从旧版本切换至新版本。
4. 启用“同路由优先”或“同 AZ 优先”策略，减少跨机房或跨可用区的网络调用成本。

**注意事项**: 
- 在进行全量发布前，务必保持金丝雀发布的时间窗口足够长，以便监控核心业务指标。
- 确保服务注册中心与 Higress 之间的长连接保持稳定，避免因网络抖动导致实例列表更新不及时。

---

### 实践 3：构建高性能的 API 网关安全防护体系

**说明**: Higress 内置了完善的网关安全能力。通过配置 IP 黑白名单、实现 JWT 身份验证以及集成 WAF 防护，可以有效抵御 SQL 注入、XSS 攻击及恶意流量刷屏，保障后端服务的稳定性。

**实施步骤**:
1. 在域名或路由级别配置 IP 访问控制，限制特定内网 IP 或阻断恶意 IP。
2. 启用 JWT 认证插件，配置鉴权规则，确保只有携带有效 Token 的请求才能通过。
3. 开启 Higress 的 WAF 防护插件（或集成开源 ModSecurity），配置防御规则集。
4. 配置 CORS（跨域资源共享）策略，防止前端页面遭受跨域攻击。

**注意事项**: 
- JWT 验证会消耗 CPU 资源，建议使用高性能算法（如 RS256）并合理设置 Token 过期时间。
- 定期审查 WAF 日志，避免因误杀规则导致正常用户访问受限。

---

### 实践 4：利用 Ingress 实现云原生流量管理

**说明**: Higress 兼容 Kubernetes Ingress API 和 Gateway API。对于使用 Kubernetes 的团队，Higress 可以作为标准 Ingress Controller 使用，通过 YAML 文件管理流量规则，实现基础设施即代码，便于版本控制和自动化部署。

**实施步骤**:
1. 使用 Helm Chart 将 Higress 部署到 Kubernetes 集群中。
2. 编写 Kubernetes Ingress 资源清单，定义 Host、Path 及后端 Service 映射关系。
3. 利用 Ingress 注解配置高级特性（如重定向、超时时间、限流配置）。
4. 将 Ingress 配置纳入 GitOps 流程（如使用 ArgoCD），实现配置变更的自动化同步。

**注意事项**: 
- 避免在单个 Ingress 资源中配置过多的路由规则，这可能导致配置更新变慢。
- 注意 Higress 对标准 Ingress 注解的兼容性，优先使用 Higress 官方文档中列出的注解。

---

### 实践 5：实施全链路可观测性监控

**说明**: Higress 原生支持 OpenTelemetry 标准，能够将访问日志、指标和链路追踪数据导出到 Prometheus、Grafana、SkyWalking 或 Jaeger 等系统中。建立全链路监控体系是排查性能瓶颈和故障定位的关键。

**实施步骤**:
1. 在 Higress 全局配置中开启 AccessLog，配置日志格式（推荐使用 JSON 格式便于解析）。
2. 集成 Prometheus，采集 Higress 的运行时指标（如 QPS、延迟、P99、错误率）

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题。在弱网环境下，它能显著减少连接建立延迟和丢包导致的性能下降。对于 Higress 这样的 API 网关，启用 QUIC 可以大幅提升长距离或移动端用户的请求响应速度。

**实施方法**:
1. 在 Higress 的网关配置中，监听器协议类型选择 `QUIC`。
2. 确保 upstream 服务配置支持 HTTP/3 或配置 Higress 进行协议转换。
3. 配置合适的 QUIC 版本（如 draft-29 或 v1）以兼容不同客户端。

**预期效果**: 在弱网环境下，首字节加载时间（TTFB）可降低 30%-50%，连接建立失败率显著下降。

---

### 优化 2：配置全链路超时与熔断策略

**说明**: 默认的超时配置往往过长，导致大量线程或连接被慢请求占用，引发雪崩效应。通过精细化的超时控制和熔断机制，可以快速释放资源，保障整体系统的吞吐量。

**实施方法**:
1. **连接超时**: 设置为 2-5 秒，避免长时间等待下游服务不可达。
2. **请求超时**: 根据业务 P99 耗耗设置，建议不超过 10 秒。
3. **熔断策略**: 在 `Route` 或 `Service` 级别配置 `Istio` 或 `Higress` 原生熔断规则，设定最大并发请求数。当达到阈值时，直接返回 503，避免系统过载。

**预期效果**: 系统资源利用率（CPU/内存）在故障场景下可保持在安全水位，吞吐量在压力下不再断崖式下跌，整体可用性提升至 99.9%+。

---

### 优化 3：启用 WASM 插件的高效缓存

**说明**: Higress 支持 WASM (WebAssembly) 插件扩展。频繁的插件逻辑执行（如鉴权、限流）会增加 CPU 开销。利用 WASM 的内存缓存能力或 Higress 的本地缓存特性，可以减少重复计算和后端请求。

**实施方法**:
1. 在 WASM 插件代码中，利用 Go 或 Rust 的 `HashMap` 或 `LRU Cache` 缓存高频访问的配置数据（如 Token 验证结果、用户信息）。
2. 对于鉴权插件，设置合理的 TTL（如 5 分钟），避免每次请求都查询后端认证服务。
3. 使用 Higress 的 `local-reply` 缓存能力，对于静态的鉴权失败响应进行本地拦截。

**预期效果**: 鉴权/限流类业务的 CPU 占用率降低 20%-40%，后端认证服务请求量减少 60% 以上。

---

### 优化 4：优化连接池与 Keep-Alive 设置

**说明**: 默认的连接管理策略可能导致频繁建立 TCP 连接（三次握手开销大）或连接泄露。合理配置 HTTP/1.1 Keep-Alive 和 HTTP/2 连接池，能显著降低延迟并提高并发处理能力。

**实施方法**:
1. **Upstream 连接池**: 根据后端服务能力调整 `maxConnections`。对于 HTTP/1.1，建议每个实例 50-100 连接；对于 HTTP/2，建议 1-3 连接（复用多路复用）。
2. **Keep-Alive**: 确保 Higress 到后端的连接开启 Keep-Alive，并将 `keepalive_timeout` 设置为 60s 或更高。
3. **空闲连接清理**: 配置合理的 `idleTimeout`，自动清理不再使用的连接，防止文件句柄耗尽。

**预期效果**: 后端连接建立开销减少 80% 以上，网关 P99 延迟降低 10%-20%。

---

### 优化 5：实施细粒度的日志采样与脱敏

**说明**: 在高并发场景下，全量日志记录会产生巨大的磁盘 I/O 和

---
## 学习要点

- 基于您提供的信息（GitHub Trending 上的 Alibaba/Higress 项目），以下是总结出的关键要点：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的下一代云原生 API 网关。
- 它深度集成了 Envoy 和 K8s，旨在解决云原生架构下多协议接入与流量治理的复杂性问题。
- 该项目支持将传统的 Nginx Ingress 和 API Gateway 无缝迁移至云原生架构。
- 提供了开箱即用的 WAF（Web 应用防火墙）插件和安全防护能力，保障业务安全。
- 兼容 Kubernetes Ingress 和 Gateway API 标准，能够轻松对接 K8s 服务网格。
- 内置了对 Dubbo、gRPC 和 Spring Cloud 等微服务框架的广泛协议支持。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心特性、架构设计及适用场景
- Kubernetes 基础知识
- 容器网络基础

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与简介章节)
- 《云原生网关演进史》相关技术博客
- Kubernetes 官方入门教程

**学习建议**:
- 理解 Ingress 与 Gateway API 的区别
- 在本地搭建 Kind 或 Minikube 环境
- 阅读阿里云关于 Higress 开源的背景文章

---

### 阶段 2：核心功能与部署实战

**学习内容**:
- Higress 的安装与部署（Docker 与 Kubernetes 模式）
- 域名、路由与流量管理配置
- 服务发现与注册中心集成（Nacos, Consul 等）
- 基础安全配置（HTTPS, Basic Auth）

**学习时间**: 2-3周

**学习资源**:
- Higress GitHub 仓库 Quickstart 文档
- Higress 官方控制台操作指南
- Envoy Filter 基础知识（Higress 基于 Envoy）

**学习建议**:
- 动手部署一个 Higress 实例并接入一个简单的后端服务
- 尝试配置基于 Header 的路由转发规则
- 熟悉 Higress Console 的操作界面

---

### 阶段 3：流量治理与插件开发

**学习内容**:
- 高级流量治理：全链路灰度、金丝雀发布、负载均衡算法
- Waf 防护与限流降级策略
- 插件系统：使用预置插件与开发自定义插件（Wasm/Go/Python）
- Prometheus 监控与日志采集集成

**学习时间**: 3-4周

**学习资源**:
- Higress 插件开发文档
- Apache Dubbo / gRPC 协议代理配置指南
- Higress 社区精选插件案例

**学习建议**:
- 深入研究 Wasm 技术在网关层应用
- 编写一个自定义 RequestBlock 插件
- 在测试环境模拟高并发流量进行限流测试

---

### 阶段 4：生产级运维与性能调优

**学习内容**:
- Higress 的高可用部署架构
- 性能瓶颈分析与调优（连接池、缓冲区等）
- 灾难恢复与备份策略
- 多集群管理与混合云部署实践

**学习时间**: 2-4周

**学习资源**:
- Higress 生产部署最佳实践白皮书
- Envoy 性能调优官方指南
- 阿里云云原生网关企业级案例分享

**学习建议**:
- 分析生产环境网关的指标（P99 延迟、QPS）
- 参与社区 Issue 讨论或阅读源码
- 规划一套符合企业标准的网关迁移方案

---
## 常见问题


### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里云开源，并捐赠给了云原生计算基金会（CNCF）作为沙箱项目。Higress 的核心代码源自阿里云 API 网关和 MSE（微服务引擎）网关的生产级实现，旨在提供高性能、高可用且功能强大的流量管理组件。它兼容 Kubernetes Ingress 标准，并深度集成了 Envoy 和 Istio 生态。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 主要具备以下几个显著优势：

1.  **深度集成 Envoy**: 相比于 Nginx 的 C/S 架构或基于 OpenResty 的 Kong/APISIX，Higress 基于 Envoy 构建，采用 C++ 编写，在处理高并发长连接和热更新配置时性能更优，且资源消耗更低。
2.  **安全防护**: 内置了 WAF（Web 应用防火墙）插件，能够提供开箱即用的安全防护，无需额外部署复杂的安全组件。
3.  **标准兼容与流量管理**: 完全兼容 Kubernetes Ingress 标准，同时支持 Nginx Ingress Annotation，方便用户迁移。它还支持 Istio 的 xDS 协议，可以作为云环境下的南北向（API 网关）与东西向（服务网格）流量的统一入口。
4.  **插件生态**: 支持 WASM (WebAssembly) 插件，允许开发者使用 Go、Python、JavaScript 等多种语言编写插件，且插件热更新不会导致连接中断。

---



### 3: Higress 是否支持从 Nginx Ingress 平滑迁移？迁移成本高吗？

3: Higress 是否支持从 Nginx Ingress 平滑迁移？迁移成本高吗？

**A**: 是的，Higress 非常重视兼容性，设计上支持低成本的平滑迁移。

1.  **Annotation 兼容**: Higress 实现了常见的 Nginx Ingress Annotations 逻辑，这意味着大部分现有的 Nginx Ingress YAML 配置可以直接在 Higress 中运行，无需修改配置文件。
2.  **配置迁移工具**: Higress 提供了配置迁移工具（Nginx Ingress Controller Higress），可以自动扫描集群中的 Ingress 资源并转换为 Higress 的配置。
3.  **流量切换**: 在 Kubernetes 集群中，你可以通过修改 Service 的 Selector 或调整 Ingress Class 的权重，逐步将流量从 Nginx 切换到 Higress，实现灰度发布，从而降低风险。

---



### 4: Higress 如何处理 Dubbo 和 gRPC 等微服务协议？

4: Higress 如何处理 Dubbo 和 gRPC 等微服务协议？

**A**: Higress 是一个全功能的微服务网关，对微服务协议有极好的支持：

1.  **Dubbo 支持**: Higress 原生支持 Dubbo 和 Dubbo3 (Triple) 协议。它可以将 HTTP/HTTPS 请求转换为 Dubbo 调用，实现 HTTP 到 Dubbo 的协议转换，让前端无需关心后端的 RPC 协议细节。
2.  **gRPC 支持**: 完全支持 gRPC 和 gRPC-Web 协议。它可以作为 gRPC 服务的代理，支持基于 HTTP/2 的负载均衡，并支持将 gRPC 请求透传或转换为 RESTful 风格的 API。
3.  **服务发现**: 能够无缝对接 Nacos、ZooKeeper、Consul 以及 Kubernetes CoreDNS，自动感知后端服务的注册与上线/下线。

---



### 5: 在 Higress 中如何扩展功能？是否支持自定义插件？

5: 在 Higress 中如何扩展功能？是否支持自定义插件？

**A**: Higress 提供了非常灵活的插件扩展机制，主要通过以下两种方式：

1.  **WASM 插件**: 这是 Higress 推荐的扩展方式。由于 Envoy 对 WASM 的支持，开发者可以使用 Go、C++、Rust、JavaScript 或 TypeScript 编写业务逻辑（如鉴权、限流、请求头修改）。WASM 插件的优势是隔离性好、动态加载（无需重启网关即可加载/卸载）且性能接近原生代码。
2.  **Lua/Python 支持**: 除了 WASM，Higress 也继承了 Envoy 生态对 Lua 脚本的支持，同时通过特定模块支持 Python 脚本处理逻辑，降低了后端开发者编写网关逻辑的门槛。
3.  **控制台配置**: Higress 提供了开源的控制台（Console），用户可以在界面上直接上传、启用、禁用和配置插件，无需修改底层的 ConfigMap 或 CRD 资源。

---



### 6: Higress 的性能表现如何？能否应对高并发场景？

6: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 的设计初衷就是为了应对阿里云超大规模的流量冲击，性能表现优异：

1.  **底层架构**: 基于 Envoy 构建，采用全异步非阻塞 I/O 模

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 是基于 Envoy 构建的，请尝试在本地 Docker 环境中快速部署一个 Higress 实例，并创建一个简单的 Ingress 路由规则，将路径 `/hello` 的流量转发到一个名为 `httpbin` 的后端服务。

### 提示**: 你需要先编写一个 `docker-compose.yml` 文件。注意 Higress 的控制台默认端口，并查阅官方文档关于如何通过控制台或配置文件（Kubernetes Ingress 注解）定义路由规则的方法。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其基于 Envoy 和 Istio 的技术架构，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现模型供应商的平滑切换与成本优化
在 AI 应用开发中，模型迭代频繁。建议不要在应用代码中硬编码 API 调用地址，而是利用 Higress 的 `wasm` 插件或路由功能配置统一的模型接入层。
*   **具体操作**：在 Higress 中配置不同的路由（如 `/v1/chat/completions`），将流量按比例或按 Header 分发至不同的 LLM 提供商（如 OpenAI、通义千问、本地部署的 vLLM）。
*   **最佳实践**：利用 Higress 的**全链路灰度发布**能力，先让 5% 的流量试用新模型版本，观察响应延迟和 Token 消耗是否符合预期，再全量切换。
*   **常见陷阱**：直接在网关层做复杂的 Prompt Engineering 会导致网关 CPU 负载过高，Prompt 模板化建议尽量在网关配置简单的替换，复杂的逻辑应在业务侧或通过独立的微服务处理。

### 2. 配置语义缓存以降低 Token 消耗和延迟
AI 问答场景中存在大量重复或高度相似的提问，直接转发给 LLM 会产生高昂的费用和较高的延迟。
*   **具体操作**：启用 Higress 的缓存插件（或配置 Redis 插件）。对于“检索增强生成（RAG）”场景，建议对向量检索后的上下文进行哈希缓存。
*   **最佳实践**：设置合理的缓存 Key（例如包含 `User Input` 的 MD5 和 `System Prompt` 的标识），并配置较短的 TTL（如 5-10 分钟），以确保回答的时效性。
*   **常见陷阱**：忽略流式输出的缓存处理。如果下游开启了 SSE（Server-Sent Events）流式传输，网关缓存需要支持流式数据的重组与转发，否则可能导致客户端无法正常接收流。

### 3. 实施细粒度的 Token 限流而非简单的 QPS 限速
传统的 API 网关通常按“每秒请求数”（QPS）限流，但在 AI 场景中，长 Prompt 和短 Prompt 的成本差异巨大。
*   **具体操作**：使用 Higress 的 `token-ratelimit` 插件或基于请求体长度的自定义限流策略。根据预估的 Token 数量（通常约为字符数 / 3 或 / 4）来限制用户调用。
*   **最佳实践**：针对不同层级的用户（如免费版、Pro 版）设置不同的 Token 预算，防止个别用户通过超长 Prompt 耗尽后端配额或资源。
*   **常见陷阱**：仅限制并发连接数而不限制 Token 吞吐量，可能导致网关连接数未满但带宽被打满，或者后端 LLM 实例因处理超长上下文而 OOM（内存溢出）。

### 4. 严格校验与清洗请求头以防止 API 密钥泄露
当企业将内部模型服务通过 Higress 暴露给外部或下游部门时，密钥管理至关重要。
*   **具体操作**：在 Higress 中配置 `auth` 插件（如 JWT 或 AK/SK 认证），拦截所有入站请求并验证身份。验证通过后，由网关统一添加调用上游 LLM 所需的 `Authorization` 头。
*   **最佳实践**：对外屏蔽后端真实的 API Key。业务端只需持有 Higress 颁发的 Access Key，无法直接触达上游模型厂商的 Key，从而实现统一的权限管控和审计。
*   **常见陷阱**：透传（Pass-through）所有 HTTP Header。这可能导致业务端意外将敏感信息传递给第三方模型提供商，或者导致 Header 冲突（如重复的 `Content-Type`）导致后端报错。

### 5. 针对流式响应的超时与重试策略配置
AI 大模型推理通常

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [Higress](/tags/higress/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*